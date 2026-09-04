from persistent_agent.git_store import GitStore


def test_git_store_records_before_and_after(tmp_path):
    source = tmp_path / "state.json"
    source.write_text("before\n")
    store = GitStore(tmp_path / "git")
    first = store.snapshot(source, "state/before.json")
    source.write_text("after\n")
    second = store.snapshot(source, "state/after.json")
    assert first != second
