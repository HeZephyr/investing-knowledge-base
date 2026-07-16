"""Raw 来源卡的 frontmatter 解析与可追溯性审计。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

REQUIRED_FIELDS = {
    "id",
    "title",
    "publisher",
    "url",
    "retrieved",
    "source_grade",
    "markets",
    "usage",
}


class SourceFormatError(ValueError):
    """来源卡 frontmatter 无法安全解析。"""


def parse_frontmatter(text: str) -> dict[str, Any]:
    """解析 Markdown 文件开头的 YAML frontmatter。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise SourceFormatError("source card must start with '---'")
    try:
        closing = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration as exc:
        raise SourceFormatError("source card is missing the closing '---'") from exc
    try:
        metadata = yaml.safe_load("\n".join(lines[1:closing]))
    except yaml.YAMLError as exc:
        raise SourceFormatError(f"invalid YAML frontmatter: {exc}") from exc
    if not isinstance(metadata, dict):
        raise SourceFormatError("frontmatter root must be a mapping")
    return metadata


def audit_source_card(path: Path) -> list[str]:
    """返回缺失或无效的必填字段名；空列表表示通过。"""
    metadata = parse_frontmatter(path.read_text(encoding="utf-8"))
    errors = set(REQUIRED_FIELDS - metadata.keys())
    for field in REQUIRED_FIELDS & metadata.keys():
        if metadata[field] in (None, "", []):
            errors.add(field)
    if metadata.get("source_grade") not in {"A", "B", "C", "D"}:
        errors.add("source_grade")
    return sorted(errors)


def source_ids(root: str | Path) -> set[str]:
    """读取 Raw 树中所有合法来源卡 ID。"""
    ids: set[str] = set()
    for path in Path(root).glob("**/*.md"):
        if path.name in {"README.md", "catalog.md", "source-catalog.md"}:
            continue
        metadata = parse_frontmatter(path.read_text(encoding="utf-8"))
        source_id = metadata.get("id")
        if isinstance(source_id, str) and source_id:
            ids.add(source_id)
    return ids
