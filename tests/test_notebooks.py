import json
from pathlib import Path


def test_numbered_beginner_notebooks_are_valid() -> None:
    notebooks = sorted(Path("notebooks").glob("*.ipynb"))

    assert len(notebooks) == 3
    for path in notebooks:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["nbformat"] == 4
        assert payload["cells"]
