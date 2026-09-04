from __future__ import annotations

import json
from pathlib import Path

from persistent_agent.evaluator import run_routing

ROOT = Path(__file__).resolve().parents[1]
result = run_routing(ROOT / "fixtures" / "reflection_dataset.jsonl")
out = ROOT / "reports" / "reflection_routing.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2) + "\n")
print(
    f"wrote {out.relative_to(ROOT)} ({result['samples']} samples, "
    f"accuracy={result['routing_accuracy']:.3f})"
)
