"""Build the static documentation tree used by MkDocs and GitHub Pages."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import yaml

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")
CONTENT_DIRS = ("wiki", "raw", "output")


def _frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        return {}
    try:
        _, header, _ = text.split("---", 2)
        return yaml.safe_load(header) or {}
    except (ValueError, yaml.YAMLError):
        return {}


def _wiki_index(root: Path) -> dict[str, Path]:
    pages = sorted((root / "wiki").rglob("*.md"))
    index: dict[str, Path] = {}
    for page in pages:
        metadata = _frontmatter(page.read_text(encoding="utf-8"))
        names = {page.stem, str(metadata.get("title", page.stem))}
        names.update(str(alias) for alias in metadata.get("aliases", []) or [])
        for name in names:
            index[name] = page
    return index


def _rewrite_wikilinks(text: str, source: Path, root: Path, index: dict[str, Path]) -> str:
    def replace(match: re.Match[str]) -> str:
        target_name, label = match.groups()
        target = index.get(target_name.strip())
        if target is None:
            return label or target_name
        relative = Path(
            __import__("os").path.relpath(target.relative_to(root), source.parent.relative_to(root))
        ).as_posix()
        return f"[{label or target_name}]({relative})"

    return WIKILINK.sub(replace, text)


def _build_graph(root: Path, index: dict[str, Path]) -> dict[str, list[dict[str, str]]]:
    nodes: list[dict[str, str]] = []
    links: list[dict[str, str]] = []
    seen_links: set[tuple[str, str]] = set()
    canonical = {path: path.stem for path in set(index.values())}

    for path in sorted(canonical, key=lambda item: item.as_posix()):
        text = path.read_text(encoding="utf-8")
        metadata = _frontmatter(text)
        node_id = canonical[path]
        nodes.append(
            {
                "id": node_id,
                "label": str(metadata.get("title", node_id)),
                "category": str(metadata.get("category", "other")),
                "level": str(metadata.get("level", "all")),
                "url": f"{path.relative_to(root).with_suffix('').as_posix()}/",
            }
        )
        for match in WIKILINK.finditer(text):
            target = index.get(match.group(1).strip())
            if target is None or target == path:
                continue
            edge = (node_id, canonical[target])
            if edge not in seen_links:
                links.append({"source": edge[0], "target": edge[1]})
                seen_links.add(edge)
    return {"nodes": nodes, "links": links}


def build_site_docs(root: Path, destination: Path) -> dict[str, int]:
    """Create a disposable MkDocs document tree and return content counts."""
    root = root.resolve()
    destination = destination.resolve()
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)

    index = _wiki_index(root)
    for source_dir in CONTENT_DIRS:
        for source in (root / source_dir).rglob("*"):
            if not source.is_file():
                continue
            target = destination / source.relative_to(root)
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.suffix.lower() == ".md":
                text = source.read_text(encoding="utf-8")
                target.write_text(_rewrite_wikilinks(text, source, root, index), encoding="utf-8")
            else:
                shutil.copy2(source, target)

    shutil.copytree(root / "site", destination, dirs_exist_ok=True)
    graph_path = destination / "assets/data/knowledge-graph.json"
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(
        json.dumps(_build_graph(root, index), ensure_ascii=False, indent=2), encoding="utf-8"
    )

    summary = {
        "wiki_pages": len(list((root / "wiki").rglob("*.md"))),
        "raw_pages": len(list((root / "raw").rglob("*.md"))),
        "output_pages": len(list((root / "output").rglob("*.md"))),
    }
    (destination / "assets/data/content-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def main() -> None:
    root = Path(__file__).parents[2]
    summary = build_site_docs(root, root / ".site-docs")
    print(
        f"Site docs ready: {summary['wiki_pages']} wiki, "
        f"{summary['raw_pages']} raw, {summary['output_pages']} output pages"
    )


if __name__ == "__main__":
    main()
