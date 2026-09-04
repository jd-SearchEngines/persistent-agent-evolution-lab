from persistent_agent.agent import Agent
from persistent_agent.memory import MemoryStore
from persistent_agent.models import Experience


def test_ephemeral_agent_does_not_persist(tmp_path):
    store = MemoryStore(tmp_path / "memory")
    Agent(store, ephemeral=True).learn(Experience("Use uv run pytest -q.", "convention"))
    assert store.items() == []


def test_new_session_receives_persisted_context(tmp_path):
    store = MemoryStore(tmp_path / "memory")
    Agent(store).learn(Experience("Use uv run pytest -q.", "convention"))
    assert "Use uv run pytest -q." in Agent(store).context()
