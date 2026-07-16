from pathlib import Path

from investkb.wiki import lint_wiki


def test_wiki_has_no_broken_links_or_missing_sources() -> None:
    report = lint_wiki("wiki", "raw")

    assert report.broken_links == []
    assert report.missing_sources == []
    assert report.orphans == []


def test_wiki_has_beginner_content_baseline() -> None:
    pages = list(Path("wiki").glob("**/*.md"))

    assert len(pages) >= 35
