---
name: safe-project-release
version: 2
description: Reusable release checks for a project.
trigger: release, publish, or handoff request
---

# Safe Project Release v2

1. Run tests.
2. Scan secrets.
3. Check large files.
4. Verify README and LICENSE.
5. Check git status.
6. Commit.
7. Run the final regression test after commit and before push.
8. Push and verify remote SHA.

Validation: final regression passes and local SHA equals verified remote SHA.
Known pitfalls: never infer remote delivery from a successful local push command.
