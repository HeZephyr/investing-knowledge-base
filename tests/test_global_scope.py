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
        "wiki/methods/公开投资框架.md",
    ]
    for path in required:
        assert (ROOT / path).is_file(), path


def test_global_hubs_are_reachable_from_primary_indexes() -> None:
    index = (ROOT / "wiki/index.md").read_text(encoding="utf-8")
    dashboard = (ROOT / "wiki/dashboard.md").read_text(encoding="utf-8")

    for link in ("[[全球市场]]", "[[美股市场]]", "[[韩国股市]]", "[[黄金]]", "[[存储半导体]]"):
        assert link in index
    assert "[[公开投资框架]]" in index
    assert "[[全球市场]]" in dashboard


def test_research_evidence_matrix_and_output_template_are_reachable() -> None:
    matrix_path = ROOT / "wiki/methods/投资研究证据矩阵.md"
    template_path = ROOT / "output/templates/实证证据卡.md"
    assert matrix_path.is_file(), matrix_path
    assert template_path.is_file(), template_path

    for index_path in ("wiki/index.md", "wiki/dashboard.md"):
        path = ROOT / index_path
        index = path.read_text(encoding="utf-8")
        assert "[[投资研究证据矩阵]]" in index, path

    output_readme_path = ROOT / "output/README.md"
    output_readme = output_readme_path.read_text(encoding="utf-8")
    assert "templates/实证证据卡.md" in output_readme, output_readme_path
