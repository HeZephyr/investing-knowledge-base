from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

from investkb.coverage import load_coverage
from investkb.sources import parse_frontmatter


ROOT = Path(__file__).parents[1]
PLUGIN = ROOT / "plugins/investing-research"
SCRIPT = PLUGIN / "scripts/audit_repository.py"


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def test_plugin_manifest_marketplace_and_skill_are_complete() -> None:
    manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    marketplace = json.loads(
        (ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
    )
    skill = (PLUGIN / "skills/audit-finance-repositories/SKILL.md").read_text(encoding="utf-8")

    assert manifest["name"] == "investing-research"
    assert manifest["version"].startswith("0.1.0")
    assert manifest["license"] == "MIT"
    assert (ROOT / "LICENSE").read_text(encoding="utf-8").startswith("MIT License")
    assert manifest["skills"] == "./skills/"
    assert "mcpServers" not in manifest
    assert "apps" not in manifest
    assert "hooks" not in manifest
    assert "[TODO:" not in json.dumps(manifest)

    entry = next(item for item in marketplace["plugins"] if item["name"] == manifest["name"])
    assert entry["source"] == {
        "source": "local",
        "path": "./plugins/investing-research",
    }
    assert entry["policy"] == {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    }
    assert entry["category"] == "Productivity"

    for phrase in (
        "read-only",
        "offline",
        "Cookie",
        "Token",
        "broker",
        "license",
        "pinned commit",
        "不下单",
    ):
        assert phrase in skill


def test_audit_script_is_offline_read_only_and_redacts_sensitive_files(tmp_path: Path) -> None:
    repository = tmp_path / "sample-repository"
    repository.mkdir()
    (repository / "LICENSE").write_text("Apache License Version 2.0", encoding="utf-8")
    (repository / "provider.py").write_text(
        "def adjusted_price():\n    return 'backtest transaction_cost timezone'\n",
        encoding="utf-8",
    )
    (repository / "trade.py").write_text(
        "def place_order():\n    return 'automatic trading'\n",
        encoding="utf-8",
    )
    secret = "DO_NOT_EXPOSE_THIS_TOKEN"
    (repository / ".env").write_text(f"API_TOKEN={secret}\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
    subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=repository)
    subprocess.run(["git", "config", "user.name", "Fixture"], cwd=repository)
    subprocess.run(["git", "add", "LICENSE", "provider.py", "trade.py"], cwd=repository, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repository, check=True)
    before = _tree_hash(repository)

    completed = subprocess.run(
        [sys.executable, str(SCRIPT), str(repository)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    after = _tree_hash(repository)

    assert completed.returncode == 0, completed.stderr
    assert before == after
    assert secret not in completed.stdout
    assert str(tmp_path) not in completed.stdout
    report = json.loads(completed.stdout)
    assert len(report["head_commit"]) == 40
    assert report["license_candidates"] == ["LICENSE"]
    assert report["signals"]["providers"]["count"] >= 1
    assert report["signals"]["auto_trading"]["count"] >= 1
    assert ".env" not in json.dumps(report)

    script_text = SCRIPT.read_text(encoding="utf-8")
    for network_module in ("requests", "urllib", "http.client", "socket"):
        assert network_module not in script_text


def test_repository_audit_cards_and_matrix_pin_scope_and_license() -> None:
    expected = {
        "openbb.md": ("ebee248ed0bccca65bdfc78e7faae676488f4e5b", "AGPL-3.0-only"),
        "myhhub-stock.md": ("b6e0ca2268cfbadd02f5ed052159c187b6670231", "Apache-2.0"),
        "ai-trader.md": ("d03ff6c056b32ced735adf7c19ed8175adb1c8df", "NOASSERTION"),
        "ai-quant-trade.md": ("275b62509340ce2a730886886ed2618e1bb0ca97", "Apache-2.0"),
    }
    for filename, (commit, license_id) in expected.items():
        path = ROOT / "raw/repositories/cards" / filename
        text = path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(text)
        assert metadata["pinned_commit"] == commit
        assert metadata["license"] == license_id
        for heading in ("代码事实", "上游声明", "认证与数据边界", "采用决策"):
            assert f"## {heading}" in text, f"{path}: missing {heading}"

    matrix = (ROOT / "wiki/engineering/金融研究代码库审计.md").read_text(encoding="utf-8")
    for name in ("OpenBB", "myhhub/stock", "AI-Trader", "ai_quant_trade"):
        assert name in matrix
    for term in ("Star", "Cookie", "自动下单", "可证伪", "许可证"):
        assert term in matrix


def test_plugin_is_indexed_and_coverage_validated() -> None:
    readme = (PLUGIN / "README.md").read_text(encoding="utf-8")
    for heading in ("安装", "更新", "卸载", "认证隔离", "离线示例"):
        assert f"## {heading}" in readme
    assert "codex plugin marketplace add" in readme
    assert "codex plugin add" in readme
    assert "codex plugin remove" in readme

    manifest = load_coverage(ROOT / "config/knowledge-coverage.yaml")
    requirement = next(
        item for item in manifest.requirements if item.id == "engineering-audit-plugin"
    )
    assert requirement.status == "validated"
    assert {item.kind for item in requirement.evidence} >= {"implementation", "test"}

    for index_path in ("README.md", "docs/INDEX.md", "wiki/index.md", "mkdocs.yml"):
        assert "金融研究代码库审计" in (ROOT / index_path).read_text(encoding="utf-8")
