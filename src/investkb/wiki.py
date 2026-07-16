"""Obsidian Wiki 的双链、来源引用与孤儿页检查。"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from investkb.sources import parse_frontmatter, source_ids

WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)


@dataclass(frozen=True)
class WikiLintReport:
    broken_links: list[str]
    missing_sources: list[str]
    orphans: list[str]


def _link_target(raw_link: str) -> str:
    target = raw_link.split("|", maxsplit=1)[0].split("#", maxsplit=1)[0].strip()
    return Path(target).stem


def lint_wiki(wiki_root: str | Path, raw_root: str | Path) -> WikiLintReport:
    """检查 Wiki 的 Obsidian 链接、Raw ID 和入口可达性。"""
    wiki_path = Path(wiki_root)
    pages = sorted(wiki_path.glob("**/*.md"))
    known_sources = source_ids(raw_root)
    names: dict[str, Path] = {}
    metadata_by_path: dict[Path, dict] = {}

    for path in pages:
        metadata = parse_frontmatter(path.read_text(encoding="utf-8"))
        metadata_by_path[path] = metadata
        names[path.stem] = path
        title = metadata.get("title")
        if isinstance(title, str):
            names[title] = path
        for alias in metadata.get("aliases", []):
            names[str(alias)] = path

    broken: list[str] = []
    missing: list[str] = []
    inbound = {path: 0 for path in pages}
    for path in pages:
        text = CODE_FENCE.sub("", path.read_text(encoding="utf-8"))
        for raw_link in WIKILINK.findall(text):
            target = _link_target(raw_link)
            target_path = names.get(target)
            if target_path is None:
                broken.append(f"{path.relative_to(wiki_path)} -> {target}")
            elif target_path != path:
                inbound[target_path] += 1
        for source_id in metadata_by_path[path].get("sources", []):
            if source_id not in known_sources:
                missing.append(f"{path.relative_to(wiki_path)} -> {source_id}")

    exempt = {"dashboard.md", "index.md", "log.md"}
    orphans = [
        str(path.relative_to(wiki_path))
        for path, count in inbound.items()
        if count == 0 and path.name not in exempt
    ]
    return WikiLintReport(sorted(broken), sorted(missing), sorted(orphans))
