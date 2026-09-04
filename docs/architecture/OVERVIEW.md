# Architecture overview

The harness has four explicit state destinations:

1. `IGNORE`: session-only facts and insufficiently general workflows.
2. `MEMORY`: durable preferences and corrected project conventions.
3. `SKILL_CANDIDATE`: repeated, stable procedures awaiting a promotion gate.
4. `HARNESS_RULE`: safety constraints enforced before model/action execution.

Every long-lived mutation is represented as a file diff or snapshot. The
independent `GitStore` is available for callers that want a separate commit
history without nesting another project repository.
