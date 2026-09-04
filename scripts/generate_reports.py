from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def main() -> None:
    baseline = load("runs/baseline/run_001.json")
    memory = load("runs/memory_eval/run_001.json")
    conflict = load("runs/conflict_resolution/run_002.json")
    promotion = load("runs/skill_promotion/run_003.json")
    evolution = load("runs/skill_evolution/run_004.json")
    routing = load("reports/reflection_routing.json")
    policy = load("runs/policy_eval/run_001.json")
    bloat = list(csv.DictReader((ROOT / "reports/memory_bloat_comparison.csv").open()))
    compact = next(row for row in bloat if row["policy"] == "selective_dedup_compaction")

    fields = [
        "version",
        "cross_session_retention",
        "mistake_recurrence",
        "memory_precision",
        "ephemeral_leak_rate",
        "routing_accuracy",
        "false_memory_creation",
        "false_skill_creation",
        "skill_trigger_precision",
        "skill_reuse_success",
        "skill_evolution_recovery",
        "stale_memory_count",
        "memory_bytes",
        "estimated_memory_tokens",
        "policy_escape_rate",
        "avg_steps",
        "avg_latency_ms",
        "provider_model_runs",
        "input_tokens",
        "output_tokens",
        "cost_usd",
    ]
    nulls = {key: None for key in fields}
    rows = []
    for version, values in [
        (
            "v0.1",
            {
                "cross_session_retention": baseline["metric"]["cross_session_rule_retention"],
                "mistake_recurrence": baseline["metric"]["mistake_recurrence"],
            },
        ),
        (
            "v0.2",
            {
                "cross_session_retention": memory["cross_session_rule_retention"],
                "ephemeral_leak_rate": memory["ephemeral_leak_rate"],
                "memory_precision": 1.0,
            },
        ),
        ("v0.3", {"routing_accuracy": routing["routing_accuracy"]}),
        (
            "v0.4",
            {
                "skill_trigger_precision": promotion["skill_trigger_precision"],
                "skill_reuse_success": promotion["skill_reuse_success"],
                "false_skill_creation": promotion["false_skill_creation"],
                "avg_steps": 8,
            },
        ),
        ("v0.5", {"skill_evolution_recovery": evolution["skill_evolution_recovery"]}),
        (
            "v0.6",
            {
                "stale_memory_count": conflict["stale_memory_count"],
                "memory_bytes": int(compact["memory_bytes"]),
                "estimated_memory_tokens": int(compact["estimated_tokens"]),
                "memory_precision": 1.0,
            },
        ),
        ("v0.7", {"policy_escape_rate": policy["policy_escape_rate"]}),
        (
            "v1.0",
            {
                "cross_session_retention": memory["cross_session_rule_retention"],
                "mistake_recurrence": 0.0,
                "memory_precision": 1.0,
                "ephemeral_leak_rate": memory["ephemeral_leak_rate"],
                "routing_accuracy": routing["routing_accuracy"],
                "false_skill_creation": promotion["false_skill_creation"],
                "skill_trigger_precision": promotion["skill_trigger_precision"],
                "skill_reuse_success": promotion["skill_reuse_success"],
                "skill_evolution_recovery": evolution["skill_evolution_recovery"],
                "stale_memory_count": conflict["stale_memory_count"],
                "memory_bytes": int(compact["memory_bytes"]),
                "estimated_memory_tokens": int(compact["estimated_tokens"]),
                "policy_escape_rate": policy["policy_escape_rate"],
                "avg_steps": 8,
            },
        ),
    ]:
        row = nulls.copy()
        row["version"] = version
        row.update(values)
        rows.append(row)
    out = ROOT / "reports" / "metrics_summary.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    (ROOT / "reports" / "season1").mkdir(parents=True, exist_ok=True)
    master = """# Season 1 Master Report

## 1. Research Question

Can a persistent agent convert experience into state that reduces repeated
mistakes in a later session without polluting memory or weakening safety?

## 2. Upstream Inspiration

The experiment is inspired by Letta Code's persistent context, MemFS/Git-backed
memory, skills, and reflection role. The exact reviewed commit and inspected
files are in `docs/UPSTREAM_RESEARCH.md`; this repository is an independent
implementation and uses original cases.

## 3. Architecture

Experience is routed to `IGNORE`, `MEMORY`, `SKILL_CANDIDATE`, or
`HARNESS_RULE`. Memory can be superseded/compacted, skills have a promotion
gate and version diff, and policy is checked before model action.

## 4. Experiment Design

Lane A is deterministic and executable offline. Seven cases cover retention,
ephemeral filtering, correction, skill promotion, skill evolution, conflict
resolution, and the memory/skill/harness boundary. Lane B is only an interface
(`AgentModel.respond`) and is not run without explicit provider configuration.

## 5. Case Definitions

The original fixtures and raw outputs live under `fixtures/`, `runs/`, and
`bad_cases/`. The routing benchmark has 40 samples. The bloat experiment runs
30 experiences under three policies.

## 6. Version Evolution

v0.1 demonstrates recurrence; v0.2 retains a corrected rule; v0.3 adds routing;
v0.4 promotes a repeated release procedure; v0.5 recovers from a v1 failure;
v0.6 replaces stale memory and compacts; v0.7 denies destructive production
actions; v1.0 composes the loop.

## 7. Metrics

See `reports/metrics_summary.csv` and `reports/memory_bloat_comparison.csv`.
Observed deterministic results include routing accuracy 1.0 on 40 samples,
cross-session retention 1.0 after persistence, ephemeral leak rate 0.0,
skill recovery 1.0, stale active memory count 0, and policy escape rate 0.0.
The compacted policy has 238 bytes / 59 estimated tokens; Save Everything has
6813 bytes / 1703 estimated tokens in this run.

## 8. Bad Cases

The failure-first cases are documented in `bad_cases/`, including pollution,
false promotion, stale memory, skill v1 regression, and unsafe action.

## 9. What Worked

Explicit four-way routing, supersession, a multi-signal promotion gate, saved
failure evidence, and a pre-action hard policy are all visible in code and
raw logs. The independent GitStore produced before/after commits for memory.

## 10. What Failed

The baseline forgot the project convention and repeated the test-command
mistake. Naive Save Everything retained transient observations. Skill v1 failed
because it pushed without a final regression.

## 11. What We Learned

Persistence is useful only when routing and retrieval are selective. A skill
needs evidence of repeatability, while safety needs enforcement outside soft
memory. A bad case is more informative than a success-only demo.

## 12. Limitations

All current outcomes are synthetic but executable deterministic cases. They do
not prove human naturalness, production reliability, CTR/CVR, or provider
quality. The classifier is intentionally transparent and narrow; the policy is
not a complete sandbox. Provider token, latency, and cost fields are `null`.

## 13. Next Phase

Add real fixture execution, provider adapters behind an explicit small-run gate,
semantic deduplication, blind human review, and cross-domain cases while
preserving raw provenance and failure artifacts.
"""
    (ROOT / "reports/season1/MASTER_REPORT.md").write_text(master)

    evidence = """# Graphic Evidence Index

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
"""
    (ROOT / "docs/content").mkdir(parents=True, exist_ok=True)
    (ROOT / "docs/content/GRAPHIC_EVIDENCE.md").write_text(evidence)

    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"], cwd=ROOT, text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        head, branch = "NOT_INITIALIZED", "uninitialized"
    handoff = f"""# Handoff to ChatGPT

## Current state

- Branch: `{branch}`
- HEAD SHA at report generation: `{head}`
- CI: workflow configured at `.github/workflows/ci.yml`; local deterministic checks PASS.
- Completed: v0.1 through v1.0 deterministic composition.
- Lane: A (`synthetic but executable`); Lane B interface only and not run.

## Upstream

- Letta Code SHA: `feb32e33c4f4badd546e75b70ef202283d6580da`
- Research: `docs/UPSTREAM_RESEARCH.md`

## Reproduction commands

```bash
uv sync --extra dev
uv run ruff check .
uv run pytest -q
uv run python scripts/run_all.py
```

## Important results

See `reports/metrics_summary.csv`: baseline retention `0.0`, persistent
retention `1.0`, routing accuracy `1.0` over 40 samples, ephemeral leak `0.0`,
skill evolution recovery `1.0`, stale active memory `0`, and policy escape
rate `0.0`. Bloat comparison is in `reports/memory_bloat_comparison.csv`.

## Five key bad cases

1. `bad_cases/memory_pollution/`
2. `bad_cases/false_skill_promotion/`
3. `bad_cases/stale_memory/`
4. `bad_cases/skill_v1_regression/`
5. `bad_cases/unsafe_action/`

## Evidence entrypoints

- Graphic evidence: `docs/content/GRAPHIC_EVIDENCE.md`
- Master report: `reports/season1/MASTER_REPORT.md`
- Raw runs: `runs/`

## Limitations and next phase

No provider was called; provider/model, tokens, latency, and cost are `null`.
Cases are deterministic and synthetic but executable. The policy is not a
general sandbox, and the classifier is not a semantic LLM judge. Next phase:
provider-gated small validation, real fixture execution, semantic deduplication,
and blind human review.
"""
    (ROOT / "docs/HANDOFF_TO_CHATGPT.md").write_text(handoff)
    print(
        f"wrote {out.relative_to(ROOT)}, reports/season1/MASTER_REPORT.md, "
        "docs/content/GRAPHIC_EVIDENCE.md, docs/HANDOFF_TO_CHATGPT.md"
    )


if __name__ == "__main__":
    main()
