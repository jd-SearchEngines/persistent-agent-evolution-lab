# Upstream research: Letta Code

Research date: 2026-09-04  
Upstream: `https://github.com/letta-ai/letta-code`  
Commit: `feb32e33c4f4badd546e75b70ef202283d6580da`

## Upstream Design

The inspected MemFS prompt describes an agent identity that persists across
conversations, recall memory for experience, editable memory blocks and
external files, skills as procedural memory, and Git-backed synchronization.
It also distinguishes soft memory changes from harness capabilities and says
that committed memory affects later context compilation. The inspected
reflection prompt defines a background reflection role that reviews experience
and can maintain memory and skills.

## Our Interpretation

Persistence is useful only when it changes a future decision. Memory, procedure,
and hard safety enforcement have different failure modes, so they must be
measured as separate routes. Versioned artifacts and raw evidence make a
learning claim auditable; compaction and supersession prevent “persistent” from
meaning “store everything forever.”

## Our Experiment

This repository implements fresh Python code with a deterministic classifier,
JSON memory store, Markdown skill store, independent Git snapshot store, and
hard policy gate. Seven original cases exercise cross-session retention,
ephemeral filtering, correction, promotion, evolution, contradiction, and the
memory/skill/harness boundary. A 40-sample benchmark and three-policy bloat
comparison are executable through `scripts/run_all.py`.

## Deliberate non-copy boundary

The repository does not copy Letta code, prompts, cases, names of business
workflows, or fixture content. Only high-level design inspiration is used.
Upstream file URLs and the exact reviewed SHA are preserved in `NOTICE.md` for
provenance.
