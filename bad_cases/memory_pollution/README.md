# Bad case: memory pollution

input: `This session's debug port is 49173 and scratch directory is temporary.`

expected: `IGNORE`; actual: a Save Everything policy would persist it.

root_cause: no reflection or routing gate.

fix: selective four-way routing rejects temporary state.

rerun_result: `ephemeral_leak_rate=0.0` in `runs/memory_eval/run_001.json`.
