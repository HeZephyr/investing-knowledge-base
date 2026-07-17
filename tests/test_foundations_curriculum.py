from __future__ import annotations

from pathlib import Path

from investkb.coverage import load_coverage
from investkb.sources import parse_frontmatter


ROOT = Path(__file__).parents[1]
MODULES = {
    "复利与贴现.md": {"raw-book-openstax-principles-finance"},
    "概率与收益分布.md": {"raw-book-openintro-statistics"},
    "抽样与估计.md": {"raw-book-openintro-statistics", "raw-official-nist-stat-handbook"},
    "假设检验与多重比较.md": {"raw-book-openintro-statistics", "raw-book-islp"},
    "回归与诊断.md": {"raw-book-islp", "raw-repo-statsmodels"},
    "时间序列与预测.md": {"raw-book-fpp3"},
    "债券与利率基础.md": {"raw-course-mit-finance-theory"},
    "公司金融基础.md": {
        "raw-book-openstax-principles-finance",
        "raw-course-mit-finance-theory",
    },
    "论文阅读与复现.md": {"raw-book-islp", "raw-repo-islp-labs"},
}
HEADINGS = (
    "学习目标",
    "核心概念",
    "手算例",
    "Python 实验",
    "投资场景",
    "常见误用",
    "检查清单",
    "来源说明",
)


def test_foundation_modules_are_deep_traceable_and_executable() -> None:
    for filename, required_sources in MODULES.items():
        path = ROOT / "wiki/foundations" / filename
        text = path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(text)

        assert len(text) >= 1500, f"{path}: module is too shallow"
        assert required_sources <= set(metadata["sources"]), path
        for heading in HEADINGS:
            assert f"## {heading}" in text, f"{path}: missing {heading}"
        assert "from investkb.education import" in text, f"{path}: missing executable example"
        assert "不构成投资建议" in text, f"{path}: missing safety boundary"


def test_curriculum_hub_and_modules_are_reachable() -> None:
    hub = (ROOT / "wiki/foundations/金融与统计基础.md").read_text(encoding="utf-8")
    learning_path = (ROOT / "wiki/learning-path.md").read_text(encoding="utf-8")
    wiki_index = (ROOT / "wiki/index.md").read_text(encoding="utf-8")
    dashboard = (ROOT / "wiki/dashboard.md").read_text(encoding="utf-8")
    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

    for filename in MODULES:
        title = filename.removesuffix(".md")
        assert f"[[{title}]]" in hub
        assert f"wiki/foundations/{filename}" in mkdocs
    for index in (learning_path, wiki_index, dashboard):
        assert "[[金融与统计基础]]" in index


def test_curriculum_sources_and_repositories_are_catalogued() -> None:
    expected_cards = (
        "raw/books-and-papers/openintro-statistics.md",
        "raw/books-and-papers/openstax-principles-finance.md",
        "raw/books-and-papers/forecasting-principles-practice.md",
        "raw/books-and-papers/islp.md",
        "raw/official/united-states/nist-statistical-handbook.md",
        "raw/courses/mit-finance-theory.md",
        "raw/repositories/cards/scipy.md",
        "raw/repositories/cards/statsmodels.md",
        "raw/repositories/cards/islp-labs.md",
        "raw/repositories/cards/quantecon-python-intro.md",
    )
    raw_catalog = (ROOT / "raw/source-catalog.md").read_text(encoding="utf-8")
    repo_catalog = (ROOT / "raw/repositories/catalog.md").read_text(encoding="utf-8")

    for relative_path in expected_cards:
        path = ROOT / relative_path
        assert path.is_file(), path
        assert not path.is_symlink(), path
        catalog = repo_catalog if "/repositories/" in relative_path else raw_catalog
        assert path.name in catalog or path.stem in catalog, f"{path}: missing from catalog"


def test_coverage_separates_curriculum_content_from_exercises_and_cases() -> None:
    manifest = load_coverage(ROOT / "config/knowledge-coverage.yaml")
    requirements = {item.id: item for item in manifest.requirements}

    validated = {
        "foundation-tvm": "content-ready",
        "foundation-compounding": "exercise-tested",
        "foundation-probability": "content-ready",
        "foundation-random-variables": "content-ready",
        "foundation-distributions": "content-ready",
        "foundation-sampling": "content-ready",
        "foundation-estimation": "exercise-tested",
        "foundation-hypothesis": "exercise-tested",
        "foundation-regression": "exercise-tested",
        "foundation-corporate-finance": "content-ready",
        "foundation-reading-papers": "exercise-tested",
        "foundation-statistical-coding": "exercise-tested",
        "asset-government-bonds": "content-ready",
        "asset-bond-math": "exercise-tested",
    }
    for requirement_id, stage in validated.items():
        requirement = requirements[requirement_id]
        assert requirement.stage == stage
        assert requirement.status == "validated"
        assert not requirement.gap

    assert requirements["method-negative-results"].status == "missing"
    assert requirements["method-negative-results"].stage == "case-validated"
