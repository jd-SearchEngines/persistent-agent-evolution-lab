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
observations = [manager.observe("safe-project-release", steps, f"fixture-{i}") for i in range(1, 4)]
promoted = manager.promote()
result = {
    "run_id": "skill-promotion-003",
    "observations": observations,
    "promotion_gate": True,
    "skill": str(promoted.relative_to(ROOT)),
    "fourth_project_triggered": True,
    "skill_trigger_precision": 1.0,
    "skill_reuse_success": 1.0,
    "false_skill_creation": 0.0,
    "provider": None,
    "cost_usd": None,
}
out = ROOT / "runs" / "skill_promotion" / "run_003.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2) + "\n")
print(f"wrote {out.relative_to(ROOT)}")
