from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
scripts = [
    "run_baseline.py",
    "run_memory_eval.py",
    "run_conflict_eval.py",
    "run_reflection_routing_eval.py",
    "run_skill_promotion_eval.py",
    "run_skill_evolution_eval.py",
    "run_memory_bloat_eval.py",
    "run_policy_eval.py",
]
for script in scripts:
    subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT, check=True)
subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "generate_reports.py")], cwd=ROOT, check=True
)
print("PASS: full deterministic regression")
