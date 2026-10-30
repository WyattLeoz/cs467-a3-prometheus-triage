#!/usr/bin/env python3
"""Remove evaluation data and Git history from the disposable agent checkout.

The trusted precheck has already produced timestamp-filtered evidence outside the
checkout. Keep only runtime instructions/scripts and an empty Git baseline for
gh-aw's bookkeeping; never expose the original object database to the model.
"""
import os
import shutil
import subprocess
from pathlib import Path


def isolate_workspace(workspace):
    """Replace an ephemeral checkout's history and remove non-runtime root paths."""
    root = Path(workspace).resolve(strict=True)
    git_dir = root / ".git"
    if not git_dir.is_dir() or git_dir.is_symlink():
        raise ValueError("requires a disposable standalone checkout, not a worktree")
    if not (root / "AGENTS.md").is_file() or not (root / ".claude/skills/prometheus-issue-triage/SKILL.md").is_file():
        raise ValueError("runtime instructions missing")
    for child in root.iterdir():
        if child.name in {".claude", "AGENTS.md"}:
            continue
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
    # gh-aw configures origin before/after inference. A fresh, empty baseline
    # supports that without keeping any original blobs, refs, packs or reflogs.
    def git(*args):
        subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
    git("init", "--initial-branch=isolated-runtime")
    git("-c", "user.name=Runtime isolation", "-c", "user.email=runtime@example.invalid",
        "commit", "--allow-empty", "-m", "Ephemeral runtime baseline")
    # The framework replaces this placeholder with the triggering repository URL.
    git("remote", "add", "origin", "https://github.com/example/isolated-runtime.git")


def main():
    """Run only inside a GitHub Actions checkout; refuse accidental local invocation."""
    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise SystemExit("Refusing to isolate a non-Actions checkout")
    root = Path(os.environ["GITHUB_WORKSPACE"]).resolve(strict=True)
    if root != Path.cwd().resolve():
        raise SystemExit("Working directory must equal GITHUB_WORKSPACE")
    isolate_workspace(root)
    print("Isolation complete: original corpus and Git object database removed")


if __name__ == "__main__":
    main()
