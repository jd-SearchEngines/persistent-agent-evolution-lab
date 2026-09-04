---
name: safe-project-release
version: 1
description: Reusable release checks for a project.
trigger: release, publish, or handoff request
---

# Safe Project Release v1

1. Run tests.
2. Scan secrets.
3. Check large files.
4. Verify README and LICENSE.
5. Check git status.
6. Commit.
7. Push.

Validation: tests pass and remote push is reported.
Known pitfalls: v1 does not run a final regression after pre-push changes.
