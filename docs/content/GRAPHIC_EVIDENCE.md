# Graphic Evidence Index

All claims below are deterministic, synthetic but executable, and trace to raw
files. Use this file as the sole index for content production.

## Card 1 — Hook

Claim: an ephemeral session forgets the project test convention and repeats the mistake.
Source File: `runs/baseline/run_001.json`  
Run ID: `baseline-001`  
Commit: captured in final handoff  
Metric: `cross_session_rule_retention=0.0`, `mistake_recurrence=1.0`  
Code Path: `scripts/run_baseline.py`  
Recommended Screenshot: session_1/session_2 JSON  
Caveat: deterministic synthetic lane.

## Card 2 — Memory

Claim: explicit reflection persistence changes the next session's context.
Source File: `runs/memory_eval/memory.diff`, `runs/memory_eval/run_001.json`  
Run ID: `memory-001`  
Commit: GitStore before/after SHAs are in the run JSON  
Metric: retention `0.0 → 1.0`; ephemeral leak `0.0`  
Code Path: `MemoryStore.upsert`, `Agent.learn`  
Recommended Screenshot: `memory.diff` and new_session_context  
Caveat: no provider model invoked.

## Card 3 — Reflection Routing

Claim: four destinations are measurable rather than a binary remember/forget switch.
Source File: `reports/reflection_routing.json`, `fixtures/reflection_dataset.jsonl`  
Run ID: `routing-040`  
Commit: captured in final handoff  
Metric: 40 samples, routing accuracy `1.0`, confusion matrix in JSON  
Code Path: `classifier.classify`, `evaluator.run_routing`  
Recommended Screenshot: confusion matrix  
Caveat: labels and rules are deterministic.

## Card 4 — Skill Promotion

Claim: three stable cross-project release observations pass promotion and
trigger on a fourth project.
Source File: `runs/skill_promotion/run_003.json`, `skills/safe-project-release/SKILL.md`  
Run ID: `skill-promotion-003`  
Commit: captured in final handoff  
Metric: trigger precision `1.0`, reuse `1.0`, false skill creation `0.0`  
Code Path: `SkillManager.observe`, `promotion_gate`, `promote`  
Recommended Screenshot: observations and SKILL.md  
Caveat: not a production release or remote push.

## Card 5 — Skill Evolution

Claim: a real v1 bad case creates evidence, updates the skill, and recovers on rerun.
Source File: `runs/skill_evolution/run_004.json`, `reports/skill_evolution_v1_v2.diff`  
Run ID: `skill-evolution-004`  
Commit: captured in final handoff  
Metric: recovery `1.0`; regression `PASS`  
Code Path: `SkillManager.update`  
Recommended Screenshot: v1 → failure → diff → v2  
Caveat: the failure is a controlled fixture.

## Card 6 — Memory Bloat

Claim: selective reflection plus compaction materially reduces stored state.
Source File: `reports/memory_bloat_comparison.csv`  
Run ID: `bloat-030`  
Commit: captured in final handoff  
Metric: Save Everything `6813/1703`; compacted `238/59` bytes/tokens  
Code Path: `MemoryStore.compact`, `scripts/run_memory_bloat_eval.py`  
Recommended Screenshot: CSV table  
Caveat: 30 deterministic experiences, not a long-running production corpus.

## Card 7 — Memory / Skill / Harness Boundary

Claim: preference routes to memory, repeated workflow to skill, safety to
harness; the dangerous action is denied.
Source File: `runs/policy_eval/run_001.json`  
Run ID: `policy-001`  
Commit: captured in final handoff  
Metric: policy escape rate `0.0`  
Code Path: `classifier.classify`, `HarnessPolicy.enforce`, `Agent.act`  
Recommended Screenshot: routes plus denial object  
Caveat: policy matcher intentionally covers a narrow destructive-command set.

## Card 8 — Final Scorecard

Claim: the composed v1.0 loop has auditable gains over the ephemeral baseline.
Source File: `reports/metrics_summary.csv`, `reports/season1/MASTER_REPORT.md`  
Run ID: `full-deterministic-regression`  
Commit: captured in final handoff  
Metric: v0.1 → v1.0 rows in CSV  
Code Path: `scripts/run_all.py`, `scripts/generate_reports.py`  
Recommended Screenshot: scorecard table and architecture arrow  
Caveat: proven only for this deterministic fixture suite.
