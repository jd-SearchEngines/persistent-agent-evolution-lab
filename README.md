# Persistent Agent Evolution Lab

An executable, deterministic lab for testing whether an agent turns experience
into durable memory, reusable skills, and runtime rules that change future
behavior. The project is deliberately small: the deterministic lane makes
harness claims reproducible before an optional provider-backed adapter is used.

## Why this exists

“The agent got smarter” is not a metric. This repository tests retention,
ephemeral-information leakage, correction reuse, skill promotion and evolution,
memory bloat, conflict resolution, and safety enforcement with run logs,
diffs, metrics, and retained bad cases.

## Architecture

`Experience → Reflection/classifier → IGNORE | MEMORY | SKILL_CANDIDATE | HARNESS_RULE → persistent state → new-session context → regression`

`MemoryStore` is soft guidance and supports supersession and compaction.
`SkillManager` requires repeated, stable, reusable workflows. `HarnessPolicy`
is a deterministic boundary checked before an action. `AgentModel.respond` is a
provider-shaped interface; no provider is called by default.

## Quickstart

```bash
uv sync --extra dev
uv run pytest -q
uv run ruff check .
uv run python scripts/run_all.py
```

`run_all.py` is the one-command deterministic reproduction. Individual runs are
available as `run_baseline.py`, `run_memory_eval.py`,
`run_reflection_routing_eval.py`, `run_skill_promotion_eval.py`,
`run_skill_evolution_eval.py`, `run_memory_bloat_eval.py`, and
`run_policy_eval.py`.

## Experiments and version evolution

- v0.1: ephemeral baseline; a new session repeats the convention mistake.
- v0.2: explicit persistent memory; a correction is visible in the next session.
- v0.3: four-way reflection routing benchmark.
- v0.4: three stable cross-project workflows promote `safe-project-release`.
- v0.5: a failure updates skill v1 to v2 and reruns regression.
- v0.6: conflict replacement, deduplication, and compaction measure bloat.
- v0.7: production destructive actions are denied by the harness.
- v1.0: the above compose into one auditable loop.

## Evidence and limitations

Start with [docs/HANDOFF_TO_CHATGPT.md](docs/HANDOFF_TO_CHATGPT.md), then use
[docs/content/GRAPHIC_EVIDENCE.md](docs/content/GRAPHIC_EVIDENCE.md) to locate
claims, run IDs, files, metrics, and caveats. The current results are
`synthetic but executable` deterministic cases, not human-quality or production
benchmarks. Provider metrics remain `null` unless a future explicit small-scope
provider run is implemented. The policy matcher is intentionally narrow and is
not a general sandbox.

## Upstream attribution

The conceptual inspiration and inspected files are recorded in
[docs/UPSTREAM_RESEARCH.md](docs/UPSTREAM_RESEARCH.md) and [NOTICE.md](NOTICE.md).
No Letta source, prompt, case, or business example is copied into this project.

## Reproduce and contribute

Keep raw run JSON, diffs, and bad cases with any claimed metric. Run
`uv run pytest -q` and `uv run ruff check .` before opening a change. Real
provider validation must be explicitly gated and must report provider, model,
tokens, latency, and cost or `null`.

## Roadmap

Add pluggable provider adapters, stronger semantic duplicate detection, a real
fixture execution layer, blinded human review, and larger cross-domain cases.
