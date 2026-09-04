from __future__ import annotations

from .models import Decision, Experience, Route, stable_key


def classify(item: Experience | str, category: str = "unknown") -> Decision:
    """Classify an experience with explicit, inspectable rules.

    This is intentionally not a language model. It isolates routing quality from
    provider variance and makes every benchmark result replayable.
    """
    if isinstance(item, str):
        item = Experience(item, category=category)
    text = item.experience.lower()
    key = stable_key(item.experience)
    ephemeral = (
        "temporary" in text
        or "临时" in text
        or "one-off" in text
        or "only for this run" in text
        or "debug port" in text
    )
    safety = "production" in text and any(
        word in text for word in ("delete", "destructive", "drop", "rm -rf", "truncate")
    )
    workflow = (
        len(item.steps) >= 3
        or item.category in {"repeated_workflow", "skill"}
        or any(
            word in text
            for word in ("release checklist", "publish workflow", "发布流程", "workflow")
        )
    )
    repeated = item.metadata.get("repeated", False) or item.category in {
        "repeated_workflow",
        "skill",
    }
    correction = item.correction or any(
        word in text for word in ("以后", "always", "must now", "regression")
    )
    preference = item.category in {"preference", "convention", "correction"}

    if safety or item.category == "safety":
        return Decision(
            Route.HARNESS_RULE,
            "destructive production behavior requires deterministic enforcement",
            key,
        )
    if ephemeral:
        return Decision(Route.IGNORE, "temporary run state has no future reuse value", key)
    if workflow and repeated:
        return Decision(
            Route.SKILL_CANDIDATE, "stable workflow repeated across tasks can be reusable", key
        )
    if workflow and not repeated:
        return Decision(Route.IGNORE, "one-off workflow is not enough evidence for a skill", key)
    if preference or correction or item.category in {"project_rule", "fact"}:
        return Decision(
            Route.MEMORY, "durable preference or corrected project rule belongs in soft memory", key
        )
    if any(word in text for word in ("secret", "credential", "permission", "deny")):
        return Decision(Route.HARNESS_RULE, "security boundary should not depend on recall", key)
    return Decision(Route.IGNORE, "insufficient evidence of durable cross-task value", key)


def confusion_matrix(rows: list[tuple[Route, Route]]) -> dict[str, dict[str, int]]:
    labels = [route.value for route in Route]
    matrix = {expected: {actual: 0 for actual in labels} for expected in labels}
    for expected, actual in rows:
        matrix[expected.value][actual.value] += 1
    return matrix
