from __future__ import annotations

import json
from pathlib import Path

from persistent_agent.memory import MemoryStore
from persistent_agent.models import Experience

ROOT = Path(__file__).resolve().parents[1]
work = ROOT / "runs" / "conflict_resolution"
store = MemoryStore(work / "memory")
store.upsert(Experience("Use npm for this repository.", "project_rule", "session-001"))
store.upsert(
    Experience(
        "Use pnpm for this repository after migration; it supersedes npm.",
        "project_rule",
        "session-002",
        correction=True,
    )
)
active = store.items()
result = {
    "run_id": "conflict-002",
    "active_memory": [item.__dict__ for item in active],
    "stale_memory_count": max(0, len(active) - 1),
    "superseded_record_count": 1,
    "provider": None,
    "cost_usd": None,
}
out = work / "run_002.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2) + "\n")
print(f"wrote {out.relative_to(ROOT)}")
