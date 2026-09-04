from persistent_agent.memory import MemoryStore
from persistent_agent.models import Experience


def test_memory_persists_and_supersedes(tmp_path):
    store = MemoryStore(tmp_path / "memory")
    store.upsert(Experience("Use npm for this repository.", "project_rule", "s1"))
    store.upsert(
        Experience(
            "Use pnpm for this repository; it supersedes npm.",
            "project_rule",
            "s2",
            correction=True,
        )
    )
    assert [item.content for item in store.items()] == [
        "Use pnpm for this repository; it supersedes npm."
    ]
    assert store.active_conflicts() == 1


def test_compaction_removes_exact_duplicates(tmp_path):
    store = MemoryStore(tmp_path / "memory")
    for i in range(3):
        store.upsert(Experience("The team prefers deterministic fixtures.", "preference", f"s{i}"))
    before, after = store.compact()
    assert before >= after
    assert len(store.items()) == 1
