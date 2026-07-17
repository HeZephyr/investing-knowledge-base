from __future__ import annotations

from pathlib import Path

import pytest

from investkb.coverage import load_coverage
from investkb.sources import parse_frontmatter


ROOT = Path(__file__).parents[1]
RAW_CARDS = {
    "raw/official/united-states/eia-open-data.md": "raw-us-eia-open-data",
    "raw/official/global/opec-annual-statistical-bulletin.md": "raw-global-opec-asb",
    "raw/official/global/bis-basel-framework.md": "raw-global-bis-basel-framework",
    "raw/official/united-states/fdic-bankfind-call-reports.md": (
        "raw-us-fdic-bankfind-call-reports"
    ),
    "raw/official/united-states/census-monthly-retail-trade.md": (
        "raw-us-census-monthly-retail-trade"
    ),
    "raw/official/mainland/nbs-retail-sales-methodology.md": (
        "raw-cn-nbs-retail-sales-methodology"
    ),
}
WIKI_PAGES = {
    "wiki/sectors/能源.md": {"raw-us-eia-open-data", "raw-global-opec-asb"},
    "wiki/sectors/金融.md": {
        "raw-global-bis-basel-framework",
        "raw-us-fdic-bankfind-call-reports",
    },
    "wiki/sectors/消费.md": {
        "raw-us-census-monthly-retail-trade",
        "raw-cn-nbs-retail-sales-methodology",
    },
}
OUTPUT_TEMPLATES = {
    "output/templates/能源周期证据卡.md",
    "output/templates/银行资产负债表证据卡.md",
    "output/templates/消费单位经济证据卡.md",
}


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


@pytest.mark.parametrize(("relative_path", "source_id"), RAW_CARDS.items())
def test_sector_raw_cards_disclose_provenance_and_limits(
    relative_path: str, source_id: str
) -> None:
    path = ROOT / relative_path
    assert path.is_file(), path

    text = path.read_text(encoding="utf-8")
    metadata = parse_frontmatter(text)

    assert metadata["id"] == source_id
    assert metadata["retrieved"].isoformat() == "2026-07-17"
    assert metadata["source_grade"] == "A"
    assert metadata["usage"] == "link-and-summarize"
    for heading in (
        "权威性与用途",
        "更新频率与字段",
        "许可与使用边界",
        "利益冲突",
        "历史修订",
        "局限与失效条件",
    ):
        section_body(text, heading, path)


@pytest.mark.parametrize(("relative_path", "source_ids"), WIKI_PAGES.items())
def test_sector_wiki_pages_cover_research_contract(
    relative_path: str, source_ids: set[str]
) -> None:
    path = ROOT / relative_path
    assert path.is_file(), path

    text = path.read_text(encoding="utf-8")
    metadata = parse_frontmatter(text)
    assert source_ids <= set(metadata["sources"])
    for heading in (
        "定义与边界",
        "产业链与商业模式",
        "指标树与时序",
        "财务映射",
        "估值",
        "跨市场差异",
        "反例与失败模式",
        "研究检查清单",
        "来源说明",
    ):
        section_body(text, heading, path)


@pytest.mark.parametrize("relative_path", OUTPUT_TEMPLATES)
def test_sector_output_templates_preregister_evidence(relative_path: str) -> None:
    path = ROOT / relative_path
    assert path.is_file(), path
    text = path.read_text(encoding="utf-8")

    for field in (
        "数据截止日",
        "历史可得日",
        "内容 SHA-256",
        "基准",
        "预设失效条件",
        "替代解释",
    ):
        assert field in text, f"{path}: missing {field}"
    assert "```bash" in text, f"{path}: missing reproduction command"


def test_sector_packs_are_reachable_from_curated_indexes() -> None:
    wiki_index = (ROOT / "wiki/index.md").read_text(encoding="utf-8")
    dashboard = (ROOT / "wiki/dashboard.md").read_text(encoding="utf-8")
    output_index = (ROOT / "output/README.md").read_text(encoding="utf-8")
    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

    for name in ("能源", "金融", "消费"):
        assert f"[[{name}]]" in wiki_index
        assert f"[[{name}]]" in dashboard
        assert f"wiki/sectors/{name}.md" in mkdocs
    for path in OUTPUT_TEMPLATES:
        assert path.removeprefix("output/") in output_index


def test_sector_coverage_records_reviewed_evidence_without_fake_validation() -> None:
    manifest = load_coverage(ROOT / "config/knowledge-coverage.yaml")
    requirements = {item.id: item for item in manifest.requirements}

    for requirement_id in ("sector-energy", "sector-financials", "sector-consumer"):
        requirement = requirements[requirement_id]
        assert requirement.status == "reviewed"
        assert {item.kind for item in requirement.evidence} == {
            "synthesis",
            "source",
            "template",
        }
        assert requirement.gap

    framework = requirements["sector-framework"]
    assert framework.status == "reviewed"
    assert framework.gap
