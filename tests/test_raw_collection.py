from pathlib import Path

import pytest
import yaml

from investkb.sources import audit_source_card, parse_frontmatter

NON_CARDS = {"README.md", "catalog.md", "source-catalog.md"}


def source_cards() -> list[Path]:
    return [path for path in Path("raw").glob("**/*.md") if path.name not in NON_CARDS]


def section_body(text: str, heading: str, path: Path) -> str:
    marker = f"## {heading}"
    lines = text.splitlines()
    assert marker in lines, f"{path}: missing {marker}"

    start = lines.index(marker) + 1
    end = next(
        (index for index in range(start, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    body = "\n".join(lines[start:end]).strip()
    assert body, f"{path}: empty {marker}"
    return body


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
    assert len(manifest["repositories"]) >= 16


def test_expert_materials_are_artifact_first_not_endorsements() -> None:
    cards = list(Path("raw/experts/cards").glob("*.md"))

    assert len(cards) >= 4
    catalog = Path("raw/experts/catalog.md").read_text(encoding="utf-8")
    assert "不构成认可" in catalog
    assert "Star" not in catalog


@pytest.mark.parametrize(
    ("filename", "source_id"),
    [
        (
            "shiller-yale-financial-markets.md",
            "raw-expert-shiller-yale-financial-markets",
        ),
        ("aqr-data-library.md", "raw-research-aqr-data-library"),
        ("gmo-research-library.md", "raw-expert-gmo-research-library"),
    ],
)
def test_research_stream_cards_disclose_provenance_conflicts_and_limits(
    filename: str, source_id: str
) -> None:
    path = Path("raw/experts/cards") / filename
    assert path.is_file(), path

    text = path.read_text(encoding="utf-8")
    metadata = parse_frontmatter(text)

    assert metadata["id"] == source_id, path
    assert metadata["retrieved"].isoformat() == "2026-07-17", path
    assert metadata["license"], path
    for heading in ("利益冲突", "许可与条款", "局限与失效条件"):
        section_body(text, heading, path)

    if filename == "aqr-data-library.md":
        update_section = section_body(text, "更新频率与数据", path)
        assert "### 字段与频率" in update_section, path
        for term in ("月度", "日度", "假设组合", "时间偏差"):
            assert term in update_section, f"{path}: missing {term} in ## 更新频率与数据"

    if filename == "gmo-research-library.md":
        assert metadata["url"] == "https://www.gmo.com/", path
        terms = section_body(text, "许可与条款", path)
        assert "不深链" in terms, path


def test_aqr_data_library_discloses_terms_restrictions() -> None:
    path = Path("raw/experts/cards/aqr-data-library.md")
    terms = section_body(path.read_text(encoding="utf-8"), "许可与条款", path)

    restriction = "限制未经 AQR 事先书面同意而复制、修改、分发或发布网站信息"
    assert restriction in terms, f"{path}: missing terms restriction in ## 许可与条款"


def test_gmo_research_library_uses_official_market_commentary_label() -> None:
    path = Path("raw/experts/cards/gmo-research-library.md")
    scope = section_body(path.read_text(encoding="utf-8"), "原始材料与范围", path)

    assert "Market Commentary" in scope, path


def test_gmo_research_library_qualifies_archive_guarantees() -> None:
    path = Path("raw/experts/cards/gmo-research-library.md")
    text = path.read_text(encoding="utf-8")
    update_section = section_body(text, "更新频率与数据", path)

    assert "历史档案的完整性、长期可访问性和不可变性没有保证" in update_section, path
    assert "不为其保留可复现历史" not in text, path
