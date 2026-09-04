from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .classifier import classify
from .memory import MemoryStore
from .models import ExecutionResult, Experience, Route
from .policy import HarnessPolicy


class AgentModel(Protocol):
    def respond(self, prompt: str, context: dict[str, Any]) -> str: ...


@dataclass
class ScriptedModel:
    """Provider-shaped adapter used only for deterministic tests."""

    def respond(self, prompt: str, context: dict[str, Any]) -> str:
        return "scripted-response"


class Agent:
    def __init__(
        self,
        memory: MemoryStore,
        policy: HarnessPolicy | None = None,
        model: AgentModel | None = None,
        ephemeral: bool = False,
    ):
        self.memory = memory
        self.policy = policy or HarnessPolicy()
        self.model = model or ScriptedModel()
        self.ephemeral = ephemeral

    def context(self) -> list[str]:
        return [item.content for item in self.memory.items()]

    def learn(self, experience: Experience):
        decision = classify(experience)
        if self.ephemeral or decision.route != Route.MEMORY:
            return decision
        self.memory.upsert(experience)
        return decision

    def act(
        self, task: str, command: str | None = None, environment: str = "development"
    ) -> ExecutionResult:
        if command:
            decision = self.policy.enforce(command, environment)
            if not decision.allowed:
                return ExecutionResult(
                    False,
                    error=decision.reason,
                    denied=True,
                    evidence={"rule": decision.rule, "command": command},
                )
        response = self.model.respond(task, {"memory": self.context()})
        return ExecutionResult(True, steps=(response,), evidence={"memory_context": self.context()})
