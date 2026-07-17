from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

from investkb.coverage import (
    coverage_score,
    load_coverage,
    render_coverage_report,
    validate_coverage,
)


TODAY = date(2026, 7, 17)


def _requirement(
    requirement_id: str = "market-cn-rules",
    *,
    axis: str = "markets",
    status: str = "validated",
    verified: str = "2026-07-17",
    evidence: list[dict[str, str]] | None = None,
    gap: str = "",
) -> dict:
    return {
        "id": requirement_id,
        "axis": axis,
        "title": "A 股市场规则",
        "status": status,
        "verified": verified,
        "evidence": evidence
        if evidence is not None
        else [
            {"path": "wiki/markets/A股市场.md", "kind": "synthesis"},
            {"path": "tests/test_global_scope.py", "kind": "test"},
        ],
        "gap": gap,
    }


def _write_manifest(tmp_path: Path, requirements: list[dict], *, as_of: str = "2026-07-17") -> Path:
    (tmp_path / "wiki/markets").mkdir(parents=True, exist_ok=True)
    (tmp_path / "tests").mkdir(parents=True, exist_ok=True)
    (tmp_path / "wiki/markets/A股市场.md").write_text("market", encoding="utf-8")
    (tmp_path / "tests/test_global_scope.py").write_text("test", encoding="utf-8")
    path = tmp_path / "coverage.yaml"
    path.write_text(
        yaml.safe_dump(
            {"schema_version": 1, "as_of": as_of, "requirements": requirements},
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return path


def test_valid_manifest_loads_and_validates(tmp_path: Path) -> None:
    path = _write_manifest(tmp_path, [_requirement()])

    manifest = load_coverage(path)

    assert manifest.schema_version == 1
    assert manifest.requirements[0].id == "market-cn-rules"
    assert validate_coverage(manifest, tmp_path, TODAY) == []


def test_validation_rejects_duplicate_ids_and_unknown_state(tmp_path: Path) -> None:
    path = _write_manifest(
        tmp_path,
        [_requirement(status="invented"), _requirement(status="reviewed", gap="补复验")],
    )

    errors = validate_coverage(load_coverage(path), tmp_path, TODAY)

    assert any("duplicate requirement id: market-cn-rules" in error for error in errors)
    assert any("unknown status: invented" in error for error in errors)


def test_validation_rejects_future_dates_and_missing_evidence(tmp_path: Path) -> None:
    path = _write_manifest(
        tmp_path,
        [
            _requirement(
                status="reviewed",
                verified="2026-07-18",
                evidence=[{"path": "wiki/missing.md", "kind": "synthesis"}],
                gap="补自动复验",
            )
        ],
        as_of="2026-07-18",
    )

    errors = validate_coverage(load_coverage(path), tmp_path, TODAY)

    assert any("as_of is in the future" in error for error in errors)
    assert any("verified date is in the future" in error for error in errors)
    assert any("evidence path does not exist: wiki/missing.md" in error for error in errors)


def test_validated_requires_two_distinct_evidence_kinds(tmp_path: Path) -> None:
    path = _write_manifest(
        tmp_path,
        [
            _requirement(
                evidence=[
                    {"path": "wiki/markets/A股市场.md", "kind": "synthesis"},
                    {"path": "wiki/markets/A股市场.md", "kind": "synthesis"},
                ]
            )
        ],
    )

    errors = validate_coverage(load_coverage(path), tmp_path, TODAY)

    assert any("validated requires at least two evidence kinds" in error for error in errors)


def test_validation_rejects_unknown_evidence_kind(tmp_path: Path) -> None:
    path = _write_manifest(
        tmp_path,
        [
            _requirement(
                status="reviewed",
                evidence=[{"path": "wiki/markets/A股市场.md", "kind": "invented"}],
                gap="补复验",
            )
        ],
    )

    errors = validate_coverage(load_coverage(path), tmp_path, TODAY)

    assert any("unknown evidence kind: invented" in error for error in errors)


def test_score_uses_declared_state_weights(tmp_path: Path) -> None:
    requirements = [
        _requirement("missing", status="missing", evidence=[], gap="尚未开始"),
        _requirement("seed", status="seed", gap="补来源与复验"),
        _requirement("reviewed", status="reviewed", gap="补可复现输出"),
        _requirement("validated"),
    ]
    manifest = load_coverage(_write_manifest(tmp_path, requirements))

    assert coverage_score(manifest) == 47.5


def test_report_is_deterministic_and_discloses_gaps(tmp_path: Path) -> None:
    requirements = [
        _requirement("market-cn-rules"),
        _requirement(
            "market-japan-rules",
            status="missing",
            evidence=[],
            gap="缺日本交易所与监管来源",
        ),
    ]
    manifest = load_coverage(_write_manifest(tmp_path, requirements))

    first = render_coverage_report(manifest)
    second = render_coverage_report(manifest)

    assert first == second
    assert "仓库就绪度，不是预期收益" in first
    assert "50.0%" in first
    assert "缺日本交易所与监管来源" in first


def test_repository_manifest_covers_every_declared_axis() -> None:
    root = Path(__file__).parents[1]
    manifest = load_coverage(root / "config/knowledge-coverage.yaml")

    assert validate_coverage(manifest, root, TODAY) == []
    assert {item.axis for item in manifest.requirements} == {
        "markets",
        "assets",
        "sectors",
        "methods",
        "engineering",
    }
