import json
from pathlib import Path

from investkb.site import build_site_docs


ROOT = Path(__file__).parents[1]


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
    assert "actions/configure-pages@v5" in pages
    assert "actions/upload-pages-artifact@v4" in pages
    assert "actions/deploy-pages@v4" in pages
    assert (ROOT / "site/javascripts/app.js").exists()
    assert (ROOT / "site/stylesheets/extra.css").exists()
