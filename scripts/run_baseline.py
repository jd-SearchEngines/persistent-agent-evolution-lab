from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runs" / "baseline" / "run_001.json"
OUT.parent.mkdir(parents=True, exist_ok=True)
result = {
    "run_id": "baseline-001",
    "lane": "A deterministic harness",
    "synthetic_but_executable": True,
    "session_1": {
        "instruction": "Use uv run pytest -q; never use bare python for dependencies.",
        "behavior": "uv run pytest -q",
    },
    "session_2": {
        "task": "fix a bug",
        "context": [],
        "behavior": "python -m pytest",
        "retained": False,
    },
    "metric": {"cross_session_rule_retention": 0.0, "mistake_recurrence": 1.0},
    "provider": None,
    "cost_usd": None,
}
OUT.write_text(json.dumps(result, indent=2) + "\n")
print(f"wrote {OUT.relative_to(ROOT)}")
