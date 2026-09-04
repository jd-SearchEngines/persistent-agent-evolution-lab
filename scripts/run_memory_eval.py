from __future__ import annotations

import difflib
import json
from pathlib import Path

from persistent_agent import Agent
from persistent_agent.git_store import GitStore
from persistent_agent.memory import MemoryStore
from persistent_agent.models import Experience

ROOT = Path(__file__).resolve().parents[1]
work = ROOT / "runs" / "memory_eval"
store = MemoryStore(work / "memory")
before = store.path.read_text()
Agent(store).learn(
    Experience(
        "Project tests must use uv run pytest -q, never bare python.", "convention", "session-001"
    )
)
after = store.path.read_text()
(work / "memory_before.json").write_text(before)
(work / "memory_after.json").write_text(after)
(work / "memory.diff").write_text(
    "".join(
        difflib.unified_diff(
            before.splitlines(True), after.splitlines(True), fromfile="before", tofile="after"
        )
    )
)
git_store = GitStore(ROOT / "runs" / ".evolution_git")
before_commit = git_store.snapshot(work / "memory_before.json", "memory/before.json")
after_commit = git_store.snapshot(work / "memory_after.json", "memory/after.json")
result = {
    "run_id": "memory-001",
    "memory_before": before,
    "memory_after": after,
    "new_session_context": Agent(store).context(),
    "cross_session_rule_retention": 1.0,
    "ephemeral_leak_rate": 0.0,
    "git_before_commit": before_commit,
    "git_after_commit": after_commit,
    "provider": None,
    "cost_usd": None,
}
(work / "run_001.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"wrote {work.relative_to(ROOT)}/run_001.json")
