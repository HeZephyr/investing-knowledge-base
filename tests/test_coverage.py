from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
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
    stage: str = "exercise-tested",
    status: str = "validated",
    verified: str = "2026-07-17",
    evidence: list[dict[str, str]] | None = None,
    gap: str = "",
) -> dict:
    return {
        "id": requirement_id,
        "axis": axis,
        "stage": stage,
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
            {"schema_version": 2, "as_of": as_of, "requirements": requirements},
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return path


def test_valid_manifest_loads_and_validates(tmp_path: Path) -> None:
    path = _write_manifest(tmp_path, [_requirement()])

    manifest = load_coverage(path)

    assert manifest.schema_version == 2
    assert manifest.requirements[0].id == "market-cn-rules"
    assert manifest.requirements[0].stage == "exercise-tested"
    assert validate_coverage(manifest, tmp_path, TODAY) == []


def test_load_rejects_schema_v1(tmp_path: Path) -> None:
    path = _write_manifest(tmp_path, [_requirement()])
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    payload["schema_version"] = 1
    path.write_text(yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8")

    with pytest.raises(ValueError, match="schema_version must be 2"):
        load_coverage(path)


def test_validation_rejects_duplicate_ids_unknown_state_and_stage(tmp_path: Path) -> None:
    path = _write_manifest(
        tmp_path,
        [
            _requirement(status="invented", stage="invented"),
            _requirement(status="reviewed", gap="补复验"),
        ],
    )

    errors = validate_coverage(load_coverage(path), tmp_path, TODAY)

    assert any("duplicate requirement id: market-cn-rules" in error for error in errors)
    assert any("unknown status: invented" in error for error in errors)
    assert any("unknown stage: invented" in error for error in errors)


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


def _stage_evidence(tmp_path: Path) -> dict[str, dict[str, str]]:
    files = {
        "source": "raw/source.md",
        "synthesis": "wiki/markets/A股市场.md",
        "report": "output/report.md",
        "implementation": "src/implementation.py",
        "test": "tests/test_global_scope.py",
        "workflow": ".github/workflows/ci.yml",
    }
    for relative_path in files.values():
        path = tmp_path / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("evidence", encoding="utf-8")
    return {kind: {"path": path, "kind": kind} for kind, path in files.items()}


@pytest.mark.parametrize(
    ("stage", "required_kinds"),
    [
        ("content-ready", {"source", "synthesis"}),
        ("exercise-tested", {"implementation", "test"}),
        ("case-validated", {"source", "report", "test"}),
        ("maintenance-live", {"workflow", "test"}),
    ],
)
def test_validated_stage_requires_matching_evidence(
    tmp_path: Path, stage: str, required_kinds: set[str]
) -> None:
    evidence = _stage_evidence(tmp_path)
    incomplete = sorted(required_kinds)[:-1]
    path = _write_manifest(
        tmp_path,
        [_requirement(stage=stage, evidence=[evidence[kind] for kind in incomplete])],
    )

    errors = validate_coverage(load_coverage(path), tmp_path, TODAY)

    assert any(f"validated stage {stage} requires one of" in error for error in errors)

    path = _write_manifest(
        tmp_path,
        [_requirement(stage=stage, evidence=[evidence[kind] for kind in required_kinds])],
    )
    errors = validate_coverage(load_coverage(path), tmp_path, TODAY)
    assert not any("validated stage" in error for error in errors)


def test_exercise_stage_accepts_synthesis_and_test(tmp_path: Path) -> None:
    evidence = _stage_evidence(tmp_path)
    path = _write_manifest(
        tmp_path,
        [
            _requirement(
                stage="exercise-tested",
                evidence=[evidence["synthesis"], evidence["test"]],
            )
        ],
    )

    assert validate_coverage(load_coverage(path), tmp_path, TODAY) == []


def test_exercise_stage_accepts_versioned_plugin_implementation(tmp_path: Path) -> None:
    plugin = tmp_path / "plugins/investing-research/scripts/audit_repository.py"
    plugin.parent.mkdir(parents=True)
    plugin.write_text("# offline implementation", encoding="utf-8")
    path = _write_manifest(
        tmp_path,
        [
            _requirement(
                stage="exercise-tested",
                evidence=[
                    {"path": str(plugin.relative_to(tmp_path)), "kind": "implementation"},
                    {"path": "tests/test_global_scope.py", "kind": "test"},
                ],
            )
        ],
    )

    assert validate_coverage(load_coverage(path), tmp_path, TODAY) == []


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
    assert "v2 基线变更" in first
    assert "50.0%" in first
    assert "缺日本交易所与监管来源" in first
    assert "## 分能力阶段状态" in first
    for stage in ("content-ready", "exercise-tested", "case-validated", "maintenance-live"):
        assert stage in first
    assert "| ID | 维度 | 阶段 | 要求 |" in first


def test_repository_manifest_covers_every_declared_axis() -> None:
    root = Path(__file__).parents[1]
    manifest = load_coverage(root / "config/knowledge-coverage.yaml")

    assert validate_coverage(manifest, root, TODAY) == []
    assert len(manifest.requirements) == 135
    assert {item.axis for item in manifest.requirements} == {
        "foundations",
        "markets",
        "assets",
        "sectors",
        "company",
        "methods",
        "portfolio",
        "engineering",
    }
    assert {item.stage for item in manifest.requirements} == {
        "content-ready",
        "exercise-tested",
        "case-validated",
        "maintenance-live",
    }
