# Season 1 Master Report

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
