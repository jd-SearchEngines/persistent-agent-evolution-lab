from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    rule: str
    reason: str


class HarnessPolicy:
    """Hard boundary: deterministic rules execute before a model/action."""

    def __init__(self):
        self.rules = {"deny destructive production operation"}

    def add_rule(self, rule: str) -> None:
        self.rules.add(rule.lower())

    def enforce(self, command: str, environment: str = "development") -> PolicyDecision:
        lowered = command.lower()
        if environment.lower() == "production" and any(
            word in lowered for word in ("rm -rf", "drop database", "delete production", "truncate")
        ):
            return PolicyDecision(
                False,
                "deny destructive production operation",
                "harness policy denied high-risk action",
            )
        return PolicyDecision(True, "none", "no hard policy matched")
