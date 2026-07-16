from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_global_market_asset_and_sector_hubs_exist() -> None:
    required = [
        "wiki/markets/全球市场.md",
        "wiki/markets/美股市场.md",
        "wiki/markets/韩国股市.md",
        "wiki/assets/黄金.md",
        "wiki/sectors/存储半导体.md",
        "wiki/concepts/汇率风险.md",
        "wiki/products/海外ETF.md",
    ]
    for path in required:
        assert (ROOT / path).is_file(), path


def test_global_hubs_are_reachable_from_primary_indexes() -> None:
    index = (ROOT / "wiki/index.md").read_text(encoding="utf-8")
    dashboard = (ROOT / "wiki/dashboard.md").read_text(encoding="utf-8")

    for link in ("[[全球市场]]", "[[美股市场]]", "[[韩国股市]]", "[[黄金]]", "[[存储半导体]]"):
        assert link in index
    assert "[[全球市场]]" in dashboard
