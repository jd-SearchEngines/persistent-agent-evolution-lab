from __future__ import annotations

import json
from pathlib import Path

from .models import AuditEvent, Experience, MemoryItem, content_hash, stable_key


class MemoryStore:
    """JSON-backed soft memory with supersession, deduplication, and compaction."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.path = self.root / "core" / "rules.json"
        self.root.mkdir(parents=True, exist_ok=True)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    def _read(self) -> list[MemoryItem]:
        return [MemoryItem(**row) for row in json.loads(self.path.read_text())]

    def _write(self, items: list[MemoryItem]) -> None:
        self.path.write_text(
            json.dumps([item.__dict__ for item in items], indent=2, ensure_ascii=False) + "\n"
        )

    def items(self, active_only: bool = True) -> list[MemoryItem]:
        items = self._read()
        return [item for item in items if item.active] if active_only else items

    def snapshot(self) -> list[dict]:
        return [item.__dict__ for item in self._read()]

    def upsert(self, experience: Experience, content: str | None = None) -> AuditEvent:
        items = self._read()
        key = stable_key(experience.experience.split("->")[0].strip())
        value = content or experience.experience
        before = content_hash([item.__dict__ for item in items])
        # A project rule with the same concept supersedes the prior value.
        tokens = set(experience.experience.lower().replace(".", " ").split())
        superseded = None
        for item in items:
            if item.active and item.category == experience.category:
                old_tokens = set(item.content.lower().replace(".", " ").split())
                if len(tokens & old_tokens) >= 2 and (
                    "use" in tokens or "must" in tokens or experience.correction
                ):
                    item.active = False
                    superseded = item.key
        existing = next((item for item in items if item.key == key and item.active), None)
        if existing:
            existing.content = value
        else:
            items.append(
                MemoryItem(key, value, experience.category, experience.session_id, superseded)
            )
        self._write(items)
        after = content_hash([item.__dict__ for item in items])
        return AuditEvent(
            key,
            experience.experience,
            "MEMORY",
            str(self.path),
            before,
            after,
            "persisted durable rule; stale conflicting rule superseded",
        )

    def compact(self) -> tuple[int, int]:
        items = self._read()
        before = len(items)
        seen: set[tuple[str, str]] = set()
        compacted: list[MemoryItem] = []
        for item in reversed(items):
            marker = (item.key, item.content.strip().lower())
            if marker in seen:
                continue
            seen.add(marker)
            compacted.append(item)
        compacted.reverse()
        self._write(compacted)
        return before, len(compacted)

    def bytes(self) -> int:
        return self.path.stat().st_size

    def estimated_tokens(self) -> int:
        return max(1, self.bytes() // 4)

    def active_conflicts(self) -> int:
        active = self.items()
        return sum(1 for item in active if item.supersedes)
