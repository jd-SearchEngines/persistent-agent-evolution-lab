# Bad case: skill v1 regression

input: v1 release workflow pushes without a final regression after changes.

expected: failure is retained, v1 is updated, and rerun passes.

root_cause: the v1 procedure ended at push.

fix: v2 inserts final regression and remote-SHA verification before/at push.

rerun_result: `runs/skill_evolution/run_004.json`, recovery `1.0`.
