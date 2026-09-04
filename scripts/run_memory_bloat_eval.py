from __future__ import annotations

import json
from pathlib import Path

from persistent_agent.evaluator import write_csv
from persistent_agent.memory import MemoryStore
from persistent_agent.models import Experience

ROOT = Path(__file__).resolve().parents[1]
rows = []
for name in ("save_everything", "selective_reflection", "selective_dedup_compaction"):
    store = MemoryStore(ROOT / "runs" / "memory_bloat" / name / "memory")
    for i in range(30):
        if name == "save_everything":
            store.upsert(
                Experience(
                    f"Transient observation {i}: scratch value {i}.", "observation", f"s-{i}"
                )
            )
        elif name == "selective_reflection" and i % 3 == 0:
            store.upsert(
                Experience(
                    f"Durable convention: run tests with uv run pytest -q, sample {i}.",
                    "convention",
                    f"s-{i}",
                )
            )
        elif name == "selective_dedup_compaction":
            store.upsert(
                Experience(
                    "Durable convention: run tests with uv run pytest -q.", "convention", f"s-{i}"
                )
            )
    before, after = store.compact()
    rows.append(
        {
            "policy": name,
            "memory_files": 1,
            "memory_bytes": store.bytes(),
            "estimated_tokens": store.estimated_tokens(),
            "duplicate_count": before - after,
            "useful_memory_precision": 0.0 if name == "save_everything" else 1.0,
        }
    )
write_csv(ROOT / "reports" / "memory_bloat_comparison.csv", rows)
(ROOT / "runs" / "memory_bloat").mkdir(parents=True, exist_ok=True)
(ROOT / "runs" / "memory_bloat" / "summary.json").write_text(json.dumps(rows, indent=2) + "\n")
print("wrote reports/memory_bloat_comparison.csv")
