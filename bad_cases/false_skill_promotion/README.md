# Bad case: false skill promotion

input: one release-like workflow with three steps.

expected: no skill; actual under the naive policy: a promoted skill.

root_cause: counting one occurrence instead of repetition, stability, and reuse.

fix: `SkillManager.promotion_gate` requires three identical observations and
explicit reusable/non-one-off flags.

rerun_result: the one-off fixture remains `IGNORE`; only the three-project
stable workflow promotes.
