import json
from pathlib import Path

from persistent_agent.classifier import classify
from persistent_agent.models import Experience, Route


def test_dataset_has_forty_samples_and_routes_correctly():
    path = Path(__file__).parents[1] / "fixtures" / "reflection_dataset.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    assert len(rows) >= 40
    for row in rows:
        item = Experience(
            row["experience"],
            row.get("category", "unknown"),
            steps=tuple(row.get("steps", ())),
            correction=row.get("correction", False),
            metadata=row.get("metadata", {}),
        )
        assert classify(item).route == Route(row["expected_route"]), row


def test_safety_is_not_soft_memory():
    assert classify("Never delete production data.", "safety").route == Route.HARNESS_RULE
