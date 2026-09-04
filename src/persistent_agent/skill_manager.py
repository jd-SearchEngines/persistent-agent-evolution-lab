from __future__ import annotations

import difflib
from pathlib import Path

SAFE_RELEASE_V1 = """---
name: safe-project-release
version: 1
description: Reusable release checks for a project.
trigger: release, publish, or handoff request
---

# Safe Project Release v1

1. Run tests.
2. Scan secrets.
3. Check large files.
4. Verify README and LICENSE.
5. Check git status.
6. Commit.
7. Push.

Validation: tests pass and remote push is reported.
Known pitfalls: v1 does not run a final regression after pre-push changes.
"""

SAFE_RELEASE_V2 = """---
name: safe-project-release
version: 2
description: Reusable release checks for a project.
trigger: release, publish, or handoff request
---

# Safe Project Release v2

1. Run tests.
2. Scan secrets.
3. Check large files.
4. Verify README and LICENSE.
5. Check git status.
6. Commit.
7. Run the final regression test after commit and before push.
8. Push and verify remote SHA.

Validation: final regression passes and local SHA equals verified remote SHA.
Known pitfalls: never infer remote delivery from a successful local push command.
"""


class SkillManager:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.candidates: dict[str, list[tuple[str, ...]]] = {}

    def observe(self, name: str, steps: tuple[str, ...], project: str) -> dict:
        records = self.candidates.setdefault(name, [])
        records.append(steps)
        stable = len({record for record in records}) == 1
        return {"name": name, "occurrences": len(records), "stable": stable, "projects": [project]}

    def promotion_gate(self, name: str, reusable: bool = True, one_off: bool = False) -> bool:
        records = self.candidates.get(name, [])
        return len(records) >= 3 and len(set(records)) == 1 and reusable and not one_off

    def promote(self, name: str = "safe-project-release") -> Path:
        if not self.promotion_gate(name):
            raise ValueError("promotion gate not satisfied")
        target = self.root / name
        (target / "v1").mkdir(parents=True, exist_ok=True)
        (target / "v1" / "SKILL.md").write_text(SAFE_RELEASE_V1)
        (target / "SKILL.md").write_text(SAFE_RELEASE_V1)
        return target / "SKILL.md"

    def update(self, name: str, report_dir: str | Path) -> Path:
        target = self.root / name
        current = target / "SKILL.md"
        before = current.read_text()
        versioned = target / "v2" / "SKILL.md"
        versioned.parent.mkdir(parents=True, exist_ok=True)
        versioned.write_text(SAFE_RELEASE_V2)
        current.write_text(SAFE_RELEASE_V2)
        report = Path(report_dir)
        report.mkdir(parents=True, exist_ok=True)
        diff = "".join(
            difflib.unified_diff(
                before.splitlines(True),
                SAFE_RELEASE_V2.splitlines(True),
                fromfile="safe-project-release v1",
                tofile="safe-project-release v2",
            )
        )
        (report / "skill_evolution_v1_v2.diff").write_text(diff)
        return current
