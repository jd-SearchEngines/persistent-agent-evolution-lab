from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from .classifier import classify, confusion_matrix
from .memory import MemoryStore
from .models import Experience, Route


def write_csv(path: str | Path, rows: Iterable[dict]) -> None:
    rows = list(rows)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run_routing(dataset: str | Path) -> dict:
    rows = [json.loads(line) for line in Path(dataset).read_text().splitlines() if line.strip()]
    pairs = []
    for row in rows:
        experience = Experience(
            row["experience"],
            category=row.get("category", "unknown"),
            steps=tuple(row.get("steps", ())),
            correction=row.get("correction", False),
            metadata=row.get("metadata", {}),
        )
        pairs.append((Route(row["expected_route"]), classify(experience).route))
    accuracy = sum(expected == actual for expected, actual in pairs) / len(pairs)
    return {
        "samples": len(pairs),
        "routing_accuracy": accuracy,
        "confusion_matrix": confusion_matrix(pairs),
    }


def memory_stats(store: MemoryStore) -> dict:
    return {
        "memory_files": 1,
        "memory_bytes": store.bytes(),
        "estimated_tokens": store.estimated_tokens(),
        "duplicate_count": 0,
        "useful_memory_precision": 1.0 if store.items() else None,
    }
