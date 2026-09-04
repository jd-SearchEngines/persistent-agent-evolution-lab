# Handoff to ChatGPT

## Current state

- Branch: `main`
- HEAD SHA at report generation: `c58a5bc5dc86ceb5994101867e08242caff531c9`
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
