from __future__ import annotations

import json
from pathlib import Path
import subprocess

from investkb.sources import parse_frontmatter


ROOT = Path(__file__).parents[1]
PLUGIN = ROOT / "plugins/investing-research"


def test_finhack_and_finance_skill_cards_pin_evidence_and_license() -> None:
    expected = {
        "finhack.md": (
            "dedbbd0b7accfed035ba05f07d76726d8754bbf7",
            "GPL-3.0-only OR LicenseRef-Commercial",
        ),
        "finance-quant-skills.md": (
            "b03516e6d6e6f839b3ce3fb8ad529eb5e6b7f874",
            "NOASSERTION",
        ),
    }

    for filename, (commit, license_id) in expected.items():
        path = ROOT / "raw/repositories/cards" / filename
        text = path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(text)
        assert metadata["pinned_commit"] == commit
        assert metadata["license"] == license_id
        for heading in ("代码事实", "上游声明", "认证与执行边界", "采用决策"):
            assert f"## {heading}" in text


def test_platform_and_skill_bundle_audit_is_deep_and_falsifiable() -> None:
    path = ROOT / "wiki/engineering/金融量化平台与Skill审计.md"
    text = path.read_text(encoding="utf-8")

    assert len(text) >= 6500
    for phrase in (
        "FinHack",
        "finance-quant-skills",
        "setup.py",
        "NOASSERTION",
        "Cookie",
        "Token",
        "实盘下单",
        "复制文档",
        "提示注入",
        "逐 Skill",
        "代码事实",
        "上游声明",
        "可证伪",
    ):
        assert phrase in text

    for skill_name in (
        "akquant",
        "akshare",
        "backtrader",
        "baostock",
        "equity-researcher",
        "joinquant-docs",
        "jqdatasdk",
        "miniqmt",
        "pywencai",
        "qmt-docs",
        "rqalpha",
        "tdxquant",
        "tushare",
    ):
        assert skill_name in text


def test_finance_skill_auditor_is_read_only_and_install_safe() -> None:
    skill_root = PLUGIN / "skills/audit-finance-skills"
    text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    reference = (skill_root / "references/adoption-matrix.md").read_text(encoding="utf-8")
    agent = (skill_root / "agents/openai.yaml").read_text(encoding="utf-8")

    for phrase in (
        "read-only",
        "already-local",
        "Never install",
        "Never execute",
        "Cookie",
        "credential",
        "prompt injection",
        "broker",
        "order",
        "nested license",
        "relative path",
    ):
        assert phrase in text
    for level in ("adopt", "optional", "link-only", "quarantine", "reject"):
        assert level in reference
    assert "$audit-finance-skills" in agent

    manifest = json.loads(
        (PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    assert manifest["version"].startswith("0.2.")
    assert manifest["skills"] == "./skills/"


def test_finance_skill_audit_is_indexed_without_vendoring_upstream() -> None:
    for path in (
        ROOT / "README.md",
        ROOT / "docs/INDEX.md",
        ROOT / "wiki/index.md",
        ROOT / "mkdocs.yml",
        ROOT / "plugins/investing-research/README.md",
    ):
        assert "金融量化平台与 Skill 审计" in path.read_text(encoding="utf-8")

    tracked = set(
        subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.splitlines()
    )
    assert not any("data/reference-repos/finhack" in item for item in tracked)
    assert not any("data/reference-repos/finance-quant-skills" in item for item in tracked)
