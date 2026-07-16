from pathlib import Path

import pytest

from investkb.sources import SourceFormatError, audit_source_card, parse_frontmatter


def test_source_card_requires_traceability(tmp_path: Path) -> None:
    card = tmp_path / "bad.md"
    card.write_text("---\nid: x\ntitle: X\n---\n", encoding="utf-8")

    errors = audit_source_card(card)

    assert "url" in errors
    assert "retrieved" in errors
    assert "source_grade" in errors


def test_parse_frontmatter_rejects_unclosed_block() -> None:
    with pytest.raises(SourceFormatError, match="closing"):
        parse_frontmatter("---\nid: x\n")


def test_valid_source_card_has_no_errors(tmp_path: Path) -> None:
    card = tmp_path / "good.md"
    card.write_text(
        """---
id: raw-test-001
title: Test
publisher: Example
url: https://example.com
retrieved: 2026-07-16
source_grade: A
markets: [A股]
usage: link-and-summarize
---
# Test
""",
        encoding="utf-8",
    )

    assert audit_source_card(card) == []
