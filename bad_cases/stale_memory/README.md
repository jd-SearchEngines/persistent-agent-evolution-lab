# Bad case: stale memory

input: `Use npm` followed by an explicit migration to `pnpm`.

expected: only pnpm remains active; actual under append-only storage: both.

root_cause: no supersession relation.

fix: `MemoryStore.upsert` deactivates the matching old project rule and records
`supersedes` for audit.

rerun_result: `stale_memory_count=0` is reported by the generated scorecard.
