#!/usr/bin/env python3
"""Offline, read-only signal inventory for an already-local repository.

The scanner reports relative paths and category counts, never matched source lines.
String hits are review leads, not proof that a feature works or a risk is present.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys


TEXT_SUFFIXES = {
    ".cfg",
    ".go",
    ".ini",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".py",
    ".rs",
    ".rst",
    ".sh",
    ".sql",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}
EXCLUDED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "site-packages",
    "venv",
}
SENSITIVE_FILE_MARKERS = ("cookie", "credential", "secret", "token")
MAX_TEXT_BYTES = 1_000_000
SIGNALS = {
    "providers": (r"provider", r"data[ _-]?source", r"fetch[ _-]?data", r"api[ _-]?client"),
    "authentication": (r"api[ _-]?key", r"authorization", r"oauth", r"bearer"),
    "cache": (r"\bcache\b", r"parquet", r"sqlite", r"local[ _-]?store"),
    "corporate_actions": (r"corporate[ _-]?action", r"dividend", r"split", r"delist"),
    "timezone": (r"timezone", r"tz_localize", r"utc_offset", r"zoneinfo"),
    "adjustment": (r"adjusted[ _-]?price", r"adjust[ _-]?factor", r"复权", r"前复权", r"后复权"),
    "backtest": (r"backtest", r"回测", r"paper[ _-]?trad"),
    "costs": (r"transaction[ _-]?cost", r"commission", r"slippage", r"手续费", r"滑点"),
    "lookahead": (r"look[ _-]?ahead", r"future[ _-]?leak", r"未来函数", r"data[ _-]?leak"),
    "auto_trading": (r"place[ _-]?order", r"auto(matic)?[ _-]?trad", r"copy[ _-]?trad", r"自动交易"),
    "tests": (r"\bpytest\b", r"\bunittest\b", r"describe\(", r"测试"),
    "docs": (r"documentation", r"readthedocs", r"mkdocs", r"使用说明"),
}
COMPILED_SIGNALS = {
    name: tuple(re.compile(pattern, re.IGNORECASE) for pattern in patterns)
    for name, patterns in SIGNALS.items()
}


def _is_sensitive(path: Path) -> bool:
    name = path.name.lower()
    return name.startswith(".env") or any(marker in name for marker in SENSITIVE_FILE_MARKERS)


def _candidate_files(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRECTORIES for part in relative.parts):
            continue
        if _is_sensitive(relative) or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            if path.stat().st_size > MAX_TEXT_BYTES:
                continue
        except OSError:
            continue
        candidates.append(path)
    return sorted(candidates, key=lambda item: item.relative_to(root).as_posix())


def _head_commit(root: Path) -> str | None:
    environment = os.environ.copy()
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    completed = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=False,
        env=environment,
    )
    commit = completed.stdout.strip()
    return commit if completed.returncode == 0 and re.fullmatch(r"[0-9a-fA-F]{40}", commit) else None


def audit_repository(root: Path) -> dict[str, object]:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError("repository path must be an existing directory")

    files = _candidate_files(root)
    matches: dict[str, set[str]] = {name: set() for name in SIGNALS}
    scanned = 0
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scanned += 1
        relative = path.relative_to(root).as_posix()
        for category, patterns in COMPILED_SIGNALS.items():
            if any(pattern.search(relative) or pattern.search(text) for pattern in patterns):
                matches[category].add(relative)

    licenses = sorted(
        path.relative_to(root).as_posix()
        for path in root.iterdir()
        if path.is_file() and path.name.lower().startswith(("license", "copying"))
    )
    return {
        "repository": root.name,
        "head_commit": _head_commit(root),
        "license_candidates": licenses,
        "scanned_text_files": scanned,
        "signals": {
            category: {"count": len(paths), "paths": sorted(paths)}
            for category, paths in matches.items()
        },
        "limitations": [
            "Keyword matches are review leads, not verified capabilities or defects.",
            "Sensitive filenames, binary/data files, generated directories, and large files are not read.",
            "No network request, dependency import, broker action, or write to the audited repository occurs.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path, help="Already-local repository directory")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()
    try:
        report = audit_repository(args.repository)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    payload = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
