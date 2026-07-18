from pathlib import Path
import subprocess

from investkb.publication import audit_public_tree
from investkb.private_research import initialize_private_workspace


ROOT = Path(__file__).parents[1]


def test_repository_passes_public_boundary_audit() -> None:
    assert audit_public_tree(ROOT, allow_local_private=True) == []


def test_public_boundary_rejects_private_paths_and_strong_secrets(tmp_path: Path) -> None:
    private = tmp_path / "private/positions.md"
    private.parent.mkdir()
    private.write_text("我的持仓", encoding="utf-8")
    leaked = tmp_path / "notes.md"
    leaked.write_text("ghp_" + "abcdefghijklmnopqrstuvwxyz1234567890", encoding="utf-8")

    findings = audit_public_tree(tmp_path)

    assert any("private/positions.md" in finding for finding in findings)
    assert any("GitHub token" in finding for finding in findings)


def test_repository_mode_skips_local_private_content_entirely(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / ".gitignore").write_text("private/\n", encoding="utf-8")
    initialize_private_workspace(tmp_path)
    assert audit_public_tree(tmp_path, allow_local_private=True) == []

    private = tmp_path / "private/positions.yaml"
    private.write_text("token: do-not-read-or-publish", encoding="utf-8")

    subprocess.run(["git", "add", "-f", "private/positions.yaml"], cwd=tmp_path, check=True)
    findings = audit_public_tree(tmp_path, allow_local_private=True)

    assert any("tracked private path: private/positions.yaml" in finding for finding in findings)


def test_collaboration_and_governance_files_exist() -> None:
    required = [
        "CONTRIBUTING.md",
        "GOVERNANCE.md",
        "SECURITY.md",
        "docs/INDEX.md",
        "docs/architecture/content-layers.md",
        ".github/CODEOWNERS",
        ".github/pull_request_template.md",
        ".github/ISSUE_TEMPLATE/config.yml",
        ".github/ISSUE_TEMPLATE/content.yml",
        ".github/ISSUE_TEMPLATE/bug.yml",
        ".github/ISSUE_TEMPLATE/feature.yml",
    ]
    for path in required:
        assert (ROOT / path).is_file(), path
