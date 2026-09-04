from __future__ import annotations

import subprocess
from pathlib import Path


class GitStore:
    """Independent Git-backed snapshot store, separate from the experiment repo."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        if not (self.root / ".git").exists():
            subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)

    def snapshot(self, source: str | Path, label: str) -> str:
        source = Path(source)
        destination = self.root / label
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(source.read_text())
        subprocess.run(["git", "add", label], cwd=self.root, check=True)
        status = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=self.root)
        if status.returncode != 0:
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=lab",
                    "-c",
                    "user.email=lab@example.invalid",
                    "commit",
                    "-q",
                    "-m",
                    f"snapshot: {label}",
                ],
                cwd=self.root,
                check=True,
            )
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=self.root, text=True
        ).strip()
