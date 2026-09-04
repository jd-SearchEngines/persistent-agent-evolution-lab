from persistent_agent.policy import HarnessPolicy
from persistent_agent.skill_manager import SkillManager


def test_skill_requires_repetition_and_stability(tmp_path):
    manager = SkillManager(tmp_path / "skills")
    steps = ("test", "scan", "verify")
    for i in range(2):
        manager.observe("release", steps, f"p{i}")
    assert not manager.promotion_gate("release")
    manager.observe("release", steps, "p3")
    assert manager.promotion_gate("release")


def test_policy_denies_production_delete():
    result = HarnessPolicy().enforce("rm -rf /production/data", "production")
    assert not result.allowed
