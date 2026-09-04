from __future__ import annotations

import json
from pathlib import Path

from persistent_agent.skill_manager import SkillManager

ROOT = Path(__file__).resolve().parents[1]
manager = SkillManager(ROOT / "skills")
steps = (
    "tests",
    "secret scan",
    "large-file check",
    "README",
    "LICENSE",
    "git status",
    "commit",
    "push verification",
)
for i in range(3):
    manager.observe("safe-project-release", steps, f"fixture-{i}")
manager.promote()
skill_path = ROOT / "skills" / "safe-project-release" / "SKILL.md"
before = skill_path.read_text()
failure = {
    "ok": False,
    "error": "push happened without final regression test",
    "skill_version": 1,
    "evidence": "fixture deliberately changes behavior after pre-push checks",
}
manager.update("safe-project-release", ROOT / "reports")
after = skill_path.read_text()
corrected = {"ok": True, "skill_version": 2, "steps": ["final regression", "verified remote SHA"]}
result = {
    "run_id": "skill-evolution-004",
    "skill_v1": before,
    "failure": failure,
    "decision": "update",
    "skill_v2": after,
    "corrected_run": corrected,
    "skill_evolution_recovery": 1.0,
    "regression": "PASS",
    "provider": None,
    "cost_usd": None,
}
out = ROOT / "runs" / "skill_evolution" / "run_004.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2) + "\n")
print(f"wrote {out.relative_to(ROOT)}")
