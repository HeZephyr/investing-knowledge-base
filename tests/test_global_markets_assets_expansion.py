from __future__ import annotations

from pathlib import Path

from investkb.coverage import load_coverage
from investkb.sources import parse_frontmatter


ROOT = Path(__file__).parents[1]
MODULES = {
    "wiki/markets/日本市场.md": {
        "raw-official-jpx-trading-clearing",
        "raw-official-fsa-edinet",
    },
    "wiki/markets/欧盟市场.md": {
        "raw-official-esma-trading",
        "raw-official-eu-transparency-settlement",
        "raw-official-eu-investment-funds-ucits",
    },
    "wiki/markets/新兴市场访问.md": {
        "raw-official-imf-areaer",
        "raw-official-world-bank-gfdd",
        "raw-official-bis-debt-statistics",
    },
    "wiki/products/债券.md": {
        "raw-official-sec-bond-bulletins",
        "raw-official-bis-debt-statistics",
    },
    "wiki/assets/大宗商品.md": {
        "raw-official-cftc-futures-basics",
        "raw-us-eia-open-data",
    },
}
HEADINGS = (
    "新手先知道",
    "制度或现金流地图",
    "数据与历史时点",
    "可执行练习",
    "常见失败模式",
    "研究检查清单",
    "案例骨架",
    "来源与许可",
)


def test_market_and_asset_modules_are_deep_traceable_and_executable() -> None:
    for relative_path, required_sources in MODULES.items():
        path = ROOT / relative_path
        text = path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(text)

        assert len(text) >= 2200, f"{path}: module is too shallow"
        assert required_sources <= set(metadata["sources"]), path
        for heading in HEADINGS:
            assert f"## {heading}" in text, f"{path}: missing {heading}"
        assert "不构成投资建议" in text, f"{path}: missing safety boundary"


def test_new_sources_are_catalogued_with_dynamic_boundaries() -> None:
    expected_cards = (
        "raw/official/japan/jpx-trading-clearing.md",
        "raw/official/japan/fsa-edinet.md",
        "raw/official/europe/esma-trading.md",
        "raw/official/europe/eu-transparency-settlement.md",
        "raw/official/europe/eu-investment-funds-ucits.md",
        "raw/official/global/imf-areaer.md",
        "raw/official/global/world-bank-gfdd.md",
        "raw/official/global/bis-debt-statistics.md",
        "raw/official/united-states/sec-bond-bulletins.md",
        "raw/official/united-states/cftc-futures-basics.md",
    )
    catalog = (ROOT / "raw/source-catalog.md").read_text(encoding="utf-8")

    for relative_path in expected_cards:
        path = ROOT / relative_path
        text = path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(text)
        assert metadata["retrieved"].isoformat() == "2026-07-17", path
        assert metadata["usage"] == "link-and-summarize", path
        assert "失效" in text or "修订" in text, path
        assert path.name in catalog, f"{path}: missing from catalog"


def test_market_asset_cross_index_is_reachable() -> None:
    global_market = (ROOT / "wiki/markets/全球市场.md").read_text(encoding="utf-8")
    index = (ROOT / "wiki/index.md").read_text(encoding="utf-8")
    dashboard = (ROOT / "wiki/dashboard.md").read_text(encoding="utf-8")
    learning_path = (ROOT / "wiki/learning-path.md").read_text(encoding="utf-8")
    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

    for title in ("日本市场", "欧盟市场", "新兴市场访问", "债券", "大宗商品"):
        assert f"[[{title}]]" in global_market
        assert f"[[{title}]]" in index
        assert title in dashboard
        assert title in learning_path
        assert title in mkdocs
    assert "市场 × 资产" in global_market


def test_coverage_only_upgrades_supported_atomic_capabilities() -> None:
    manifest = load_coverage(ROOT / "config/knowledge-coverage.yaml")
    requirements = {item.id: item for item in manifest.requirements}

    for requirement_id in (
        "market-japan-rules",
        "market-europe-rules",
        "market-emerging-rules",
        "asset-credit-bonds",
        "asset-commodities",
    ):
        assert requirements[requirement_id].status == "validated"
        assert not requirements[requirement_id].gap
    assert requirements["asset-bond-math"].status == "validated"
    assert requirements["asset-futures"].status == "reviewed"
    assert requirements["market-calendar-monitor"].status == "missing"
