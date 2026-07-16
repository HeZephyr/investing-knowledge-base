"""Guardrails for publishing a reusable repository without private material."""

from __future__ import annotations

import re
from pathlib import Path

FORBIDDEN_PARTS = {"private", "personal"}
FORBIDDEN_PREFIXES = ("configs/local/", "output/private/", "output/personal/", "data/cache/")
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}
SKIP_DIRS = {".git", ".venv", ".site-docs", "site-build", "build", "dist", "__pycache__"}


def audit_public_tree(root: Path) -> list[str]:
    """Return public-boundary violations without mutating the repository."""
    root = root.resolve()
    findings: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        relative_text = relative.as_posix()
        if any(part in FORBIDDEN_PARTS for part in relative.parts) or relative_text.startswith(
            FORBIDDEN_PREFIXES
        ):
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
    findings = audit_public_tree(root)
    if findings:
        raise SystemExit("Public boundary audit failed:\n- " + "\n- ".join(findings))
    print("PASS: public/private boundary and strong-secret audit")


if __name__ == "__main__":
    main()
