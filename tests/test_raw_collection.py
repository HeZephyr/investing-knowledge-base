from pathlib import Path

import yaml

from investkb.sources import audit_source_card, parse_frontmatter

NON_CARDS = {"README.md", "catalog.md", "source-catalog.md"}


def source_cards() -> list[Path]:
    return [path for path in Path("raw").glob("**/*.md") if path.name not in NON_CARDS]


def test_raw_collection_has_minimum_coverage() -> None:
    cards = source_cards()

    assert len(cards) >= 30
    assert all(not audit_source_card(path) for path in cards)


def test_raw_collection_covers_both_markets_and_source_types() -> None:
    metadata = [parse_frontmatter(path.read_text(encoding="utf-8")) for path in source_cards()]
    markets = {market for item in metadata for market in item["markets"]}

    assert {"A股", "港股"} <= markets
    assert len(list(Path("raw/official").glob("**/*.md"))) >= 16
    assert len(list(Path("raw/repositories/cards").glob("*.md"))) >= 8


def test_reference_repo_cards_record_license_and_commit() -> None:
    for path in Path("raw/repositories/cards").glob("*.md"):
        metadata = parse_frontmatter(path.read_text(encoding="utf-8"))
        assert metadata["license"]
        assert metadata["pinned_commit"]


def test_reference_manifest_is_parseable() -> None:
    manifest = yaml.safe_load(Path("raw/repositories/manifest.yaml").read_text(encoding="utf-8"))
    assert len(manifest["repositories"]) >= 8
