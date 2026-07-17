import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).parents[1]
SKILL = ROOT / "skills/maintain-investing-knowledge-base"
SCRIPT = SKILL / "scripts/scaffold_source_card.py"


def test_knowledge_skill_has_valid_metadata_and_resources() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    _, frontmatter, _ = text.split("---", 2)
    metadata = yaml.safe_load(frontmatter)

    assert metadata["name"] == "maintain-investing-knowledge-base"
    assert "Use when" in metadata["description"]
    assert (SKILL / "agents/openai.yaml").is_file()
    assert len(list((SKILL / "references").glob("*.md"))) == 3


def test_knowledge_skill_requires_coverage_and_lessons_updates() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    assert "config/knowledge-coverage.yaml" in text
    assert "coverage validate" in text
    assert "经验与失败教训" in text
    for stage in (
        "content-ready",
        "exercise-tested",
        "case-validated",
        "maintenance-live",
    ):
        assert stage in text


def test_source_card_scaffold_creates_valid_card_and_refuses_overwrite(tmp_path: Path) -> None:
    command = [
        sys.executable,
        str(SCRIPT),
        "official/example.md",
        "--id",
        "raw-official-example",
        "--title",
        "Example Source",
        "--publisher",
        "Example Authority",
        "--url",
        "https://example.com/source",
        "--grade",
        "A",
        "--markets",
        "全球,美股",
        "--retrieved",
        "2026-07-16",
    ]

    first = subprocess.run(command, cwd=tmp_path, text=True, capture_output=True, check=False)
    second = subprocess.run(command, cwd=tmp_path, text=True, capture_output=True, check=False)

    assert first.returncode == 0
    card = (tmp_path / "raw/official/example.md").read_text(encoding="utf-8")
    assert "markets: [全球, 美股]" in card
    assert "retrieved: 2026-07-16" in card
    assert second.returncode != 0
    assert "refusing to overwrite" in second.stderr
