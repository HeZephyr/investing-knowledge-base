"""Guardrails for publishing a reusable repository without private material."""

from __future__ import annotations

import re
from pathlib import Path
import subprocess

FORBIDDEN_PARTS = {"private", "personal"}
FORBIDDEN_PREFIXES = ("configs/local/", "output/private/", "output/personal/", "data/cache/")
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}
SKIP_DIRS = {".git", ".venv", ".site-docs", "site-build", "build", "dist", "__pycache__"}


def _tracked_paths(root: Path) -> set[str] | None:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return {
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    }


def audit_public_tree(root: Path, *, allow_local_private: bool = False) -> list[str]:
    """Return public violations; optionally skip ignored private layers without reading them."""
    root = root.resolve()
    findings: list[str] = []
    tracked = _tracked_paths(root) if allow_local_private else None
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        relative_text = relative.as_posix()
        is_private = any(
            part in FORBIDDEN_PARTS for part in relative.parts
        ) or relative_text.startswith(FORBIDDEN_PREFIXES)
        if is_private and allow_local_private:
            if tracked is None:
                findings.append("cannot verify tracked private paths: not a Git worktree")
                tracked = set()
            elif relative_text in tracked:
                findings.append(f"tracked private path: {relative_text}")
            continue
        if is_private:
            findings.append(f"forbidden private path: {relative_text}")
            continue
        if path.stat().st_size > 2_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"possible {label}: {relative_text}")
    return findings


def main() -> None:
    root = Path(__file__).parents[2]
    findings = audit_public_tree(root, allow_local_private=True)
    if findings:
        raise SystemExit("Public boundary audit failed:\n- " + "\n- ".join(findings))
    print("PASS: public/private boundary and strong-secret audit")


if __name__ == "__main__":
    main()
