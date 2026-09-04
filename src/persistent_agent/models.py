from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class Route(StrEnum):
    IGNORE = "IGNORE"
    MEMORY = "MEMORY"
    SKILL_CANDIDATE = "SKILL_CANDIDATE"
    HARNESS_RULE = "HARNESS_RULE"


@dataclass(frozen=True)
class Experience:
    experience: str
    category: str = "unknown"
    session_id: str = "session-unknown"
    project: str | None = None
    steps: tuple[str, ...] = ()
    correction: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Decision:
    route: Route
    reason: str
    key: str


@dataclass
class MemoryItem:
    key: str
    content: str
    category: str
    source_session: str
    supersedes: str | None = None
    active: bool = True
    created_at: str = ""


@dataclass(frozen=True)
class ExecutionResult:
    ok: bool
    steps: tuple[str, ...] = ()
    error: str | None = None
    denied: bool = False
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    source_experience: str
    decision: str
    target: str
    before_hash: str
    after_hash: str
    reason: str


def stable_key(text: str) -> str:
    normalized = " ".join(text.lower().split())
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def content_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str).encode()
    return hashlib.sha256(payload).hexdigest()[:16]


def to_json(value: Any) -> dict[str, Any]:
    return asdict(value)
