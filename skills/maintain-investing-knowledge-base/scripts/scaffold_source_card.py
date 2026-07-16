#!/usr/bin/env python3
"""Create a source-card skeleton without silently overwriting existing evidence."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("path", type=Path, help="Destination below the repository raw directory")
    result.add_argument("--id", required=True)
    result.add_argument("--title", required=True)
    result.add_argument("--publisher", required=True)
    result.add_argument("--url", required=True)
    result.add_argument("--grade", choices=("A", "B", "C", "D"), required=True)
    result.add_argument("--markets", required=True, help="Comma-separated market labels")
    result.add_argument("--usage", default="link-and-summarize")
    result.add_argument("--retrieved", default=date.today().isoformat())
    return result


def validate(args: argparse.Namespace) -> None:
    if not re.fullmatch(r"raw-[a-z0-9-]+", args.id):
        raise SystemExit("--id must match raw-[a-z0-9-]+")
    parsed = urlparse(args.url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise SystemExit("--url must be a canonical HTTPS URL")
    try:
        date.fromisoformat(args.retrieved)
    except ValueError as error:
        raise SystemExit("--retrieved must use YYYY-MM-DD") from error
    if args.path.suffix != ".md" or args.path.is_absolute() or ".." in args.path.parts:
        raise SystemExit("path must be a relative Markdown path below raw/")


def render(args: argparse.Namespace) -> str:
    markets = ", ".join(item.strip() for item in args.markets.split(",") if item.strip())
    if not markets:
        raise SystemExit("--markets must contain at least one market")
    return f"""---
id: {args.id}
title: {args.title}
publisher: {args.publisher}
url: {args.url}
retrieved: {args.retrieved}
source_grade: {args.grade}
markets: [{markets}]
usage: {args.usage}
---
# {args.title}

## 可采纳内容

TODO：只记录可核验摘要，不复制受版权保护的长段正文。

## 限制

TODO：记录适用日期、方法、许可、利益冲突和已知缺口。
"""


def main() -> None:
    args = parser().parse_args()
    validate(args)
    target = Path("raw") / args.path
    if target.exists():
        raise SystemExit(f"refusing to overwrite existing source card: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render(args), encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
