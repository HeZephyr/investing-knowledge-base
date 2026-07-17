import json
import re
from pathlib import Path

import pytest

from investkb.site import build_site_docs


ROOT = Path(__file__).parents[1]


def assert_action_minimum_major(workflow: str, action: str, minimum_major: int) -> None:
    match = re.search(rf"uses:\s+{re.escape(action)}@v(\d+)\b", workflow)
    assert match is not None, f"{action} must use an official @vN release"
    assert int(match.group(1)) >= minimum_major, (
        f"{action} must use v{minimum_major} or newer, got v{match.group(1)}"
    )


def test_build_site_docs_copies_content_and_rewrites_wikilinks(tmp_path: Path) -> None:
    summary = build_site_docs(ROOT, tmp_path)

    index = (tmp_path / "wiki/index.md").read_text(encoding="utf-8")
    assert "[[" not in index
    assert "[投资学习仪表盘](dashboard.md)" in index
    assert (tmp_path / "raw/repositories/cards/explorefinance.md").exists()
    assert (tmp_path / "output/templates/公司分析.md").exists()
    assert summary["wiki_pages"] >= 38
    assert summary["raw_pages"] >= 33


def test_build_site_docs_generates_linked_knowledge_graph(tmp_path: Path) -> None:
    build_site_docs(ROOT, tmp_path)

    graph = json.loads((tmp_path / "assets/data/knowledge-graph.json").read_text(encoding="utf-8"))
    node_ids = {node["id"] for node in graph["nodes"]}
    assert {"index", "dashboard", "最大回撤"}.issubset(node_ids)
    assert any(
        link["source"] == "index" and link["target"] == "dashboard" for link in graph["links"]
    )
    assert all(node["url"].startswith("wiki/") for node in graph["nodes"])


def test_site_configuration_and_assets_are_present() -> None:
    config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    pages = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")

    assert "material" in config
    assert "language: zh" in config
    assert "search:" in config
    assert_action_minimum_major(pages, "actions/configure-pages", 5)
    assert_action_minimum_major(pages, "actions/upload-pages-artifact", 4)
    assert_action_minimum_major(pages, "actions/deploy-pages", 4)
    assert (ROOT / "site/javascripts/app.js").exists()
    assert (ROOT / "site/stylesheets/extra.css").exists()


def test_site_action_contract_accepts_newer_major_versions() -> None:
    pages = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
    upgraded = (
        pages.replace("actions/configure-pages@v5", "actions/configure-pages@v6")
        .replace("actions/upload-pages-artifact@v4", "actions/upload-pages-artifact@v5")
        .replace("actions/deploy-pages@v4", "actions/deploy-pages@v5")
    )

    assert_action_minimum_major(upgraded, "actions/configure-pages", 5)
    assert_action_minimum_major(upgraded, "actions/upload-pages-artifact", 4)
    assert_action_minimum_major(upgraded, "actions/deploy-pages", 4)


@pytest.mark.parametrize(
    ("workflow", "action", "minimum_major"),
    [
        ("uses: actions/configure-pages@v4", "actions/configure-pages", 5),
        ("uses: fork/configure-pages@v6", "actions/configure-pages", 5),
        ("uses: actions/deploy-pages@main", "actions/deploy-pages", 4),
    ],
)
def test_site_action_contract_rejects_unsafe_references(
    workflow: str, action: str, minimum_major: int
) -> None:
    with pytest.raises(AssertionError):
        assert_action_minimum_major(workflow, action, minimum_major)
