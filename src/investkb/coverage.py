"""机器可审计的知识覆盖清单、证据验证与公开报告。"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

ALLOWED_AXES = (
    "foundations",
    "markets",
    "assets",
    "sectors",
    "company",
    "methods",
    "portfolio",
    "engineering",
)
ALLOWED_STAGES = (
    "content-ready",
    "exercise-tested",
    "case-validated",
    "maintenance-live",
)
ALLOWED_STATES = ("missing", "seed", "reviewed", "validated")
STATE_WEIGHTS = {"missing": 0.0, "seed": 0.25, "reviewed": 0.65, "validated": 1.0}
EVIDENCE_ROOTS = {
    "wiki",
    "raw",
    "output",
    "tests",
    "src",
    ".github",
    "docs",
    "config",
    "site",
    "skills",
}
EVIDENCE_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".toml", ".json"}
ROOT_EVIDENCE_FILES = {"AGENTS.md", "README.md", "mkdocs.yml", "pyproject.toml"}
ALLOWED_EVIDENCE_KINDS = {
    "source",
    "synthesis",
    "template",
    "report",
    "implementation",
    "test",
    "workflow",
    "configuration",
    "runtime",
}
AXIS_LABELS = {
    "foundations": "基础学科",
    "markets": "市场",
    "assets": "资产与产品",
    "sectors": "行业",
    "company": "公司研究",
    "methods": "研究方法",
    "portfolio": "组合与风控",
    "engineering": "工程与维护",
}
STAGE_LABELS = {
    "content-ready": "内容就绪",
    "exercise-tested": "练习已测",
    "case-validated": "案例验证",
    "maintenance-live": "维护在线",
}
STAGE_EVIDENCE_OPTIONS = {
    "content-ready": (frozenset({"source", "synthesis"}),),
    "exercise-tested": (
        frozenset({"implementation", "test"}),
        frozenset({"synthesis", "test"}),
    ),
    "case-validated": (frozenset({"source", "report", "test"}),),
    "maintenance-live": (frozenset({"workflow", "test"}),),
}


class CoverageFormatError(ValueError):
    """覆盖清单无法安全解析。"""


@dataclass(frozen=True)
class Evidence:
    path: str
    kind: str


@dataclass(frozen=True)
class CoverageRequirement:
    id: str
    axis: str
    stage: str
    title: str
    status: str
    verified: date
    evidence: tuple[Evidence, ...]
    gap: str


@dataclass(frozen=True)
class CoverageManifest:
    schema_version: int
    as_of: date
    requirements: tuple[CoverageRequirement, ...]


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CoverageFormatError(f"{label} must be a mapping")
    return value


def _text(mapping: dict[str, Any], key: str, label: str, *, allow_empty: bool = False) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise CoverageFormatError(f"{label}.{key} must be a string")
    return value.strip()


def _date(value: Any, label: str) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError as exc:
            raise CoverageFormatError(f"{label} must be an ISO date") from exc
    raise CoverageFormatError(f"{label} must be an ISO date")


def load_coverage(path: str | Path) -> CoverageManifest:
    """从 YAML 加载覆盖清单；结构错误立即失败。"""
    source = Path(path)
    try:
        data = yaml.safe_load(source.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise CoverageFormatError(f"cannot read coverage manifest: {exc}") from exc
    root = _mapping(data, "manifest")
    if root.get("schema_version") != 2:
        raise CoverageFormatError("schema_version must be 2")
    raw_requirements = root.get("requirements")
    if not isinstance(raw_requirements, list):
        raise CoverageFormatError("requirements must be a list")

    requirements: list[CoverageRequirement] = []
    for index, raw_requirement in enumerate(raw_requirements):
        label = f"requirements[{index}]"
        item = _mapping(raw_requirement, label)
        raw_evidence = item.get("evidence")
        if not isinstance(raw_evidence, list):
            raise CoverageFormatError(f"{label}.evidence must be a list")
        evidence: list[Evidence] = []
        for evidence_index, raw_item in enumerate(raw_evidence):
            evidence_label = f"{label}.evidence[{evidence_index}]"
            evidence_item = _mapping(raw_item, evidence_label)
            evidence.append(
                Evidence(
                    path=_text(evidence_item, "path", evidence_label),
                    kind=_text(evidence_item, "kind", evidence_label),
                )
            )
        requirements.append(
            CoverageRequirement(
                id=_text(item, "id", label),
                axis=_text(item, "axis", label),
                stage=_text(item, "stage", label),
                title=_text(item, "title", label),
                status=_text(item, "status", label),
                verified=_date(item.get("verified"), f"{label}.verified"),
                evidence=tuple(evidence),
                gap=_text(item, "gap", label, allow_empty=True),
            )
        )
    return CoverageManifest(
        schema_version=2,
        as_of=_date(root.get("as_of"), "as_of"),
        requirements=tuple(requirements),
    )


def _valid_evidence_path(raw_path: str) -> bool:
    path = PurePosixPath(raw_path)
    return (
        not path.is_absolute()
        and ".." not in path.parts
        and bool(path.parts)
        and (path.parts[0] in EVIDENCE_ROOTS or raw_path in ROOT_EVIDENCE_FILES)
        and path.suffix in EVIDENCE_SUFFIXES
    )


def validate_coverage(
    manifest: CoverageManifest, root: str | Path, today: date | None = None
) -> list[str]:
    """返回所有覆盖清单错误；空列表表示可进入报告。"""
    repository = Path(root)
    reference_date = today or date.today()
    errors: list[str] = []
    if manifest.as_of > reference_date:
        errors.append(f"as_of is in the future: {manifest.as_of.isoformat()}")

    seen: set[str] = set()
    for requirement in manifest.requirements:
        prefix = requirement.id
        if requirement.id in seen:
            errors.append(f"duplicate requirement id: {requirement.id}")
        seen.add(requirement.id)
        if requirement.axis not in ALLOWED_AXES:
            errors.append(f"{prefix}: unknown axis: {requirement.axis}")
        if requirement.stage not in ALLOWED_STAGES:
            errors.append(f"{prefix}: unknown stage: {requirement.stage}")
        if requirement.status not in ALLOWED_STATES:
            errors.append(f"{prefix}: unknown status: {requirement.status}")
        if requirement.verified > reference_date:
            errors.append(f"{prefix}: verified date is in the future: {requirement.verified}")

        evidence_kinds: set[str] = set()
        for evidence in requirement.evidence:
            evidence_kinds.add(evidence.kind)
            if evidence.kind not in ALLOWED_EVIDENCE_KINDS:
                errors.append(f"{prefix}: unknown evidence kind: {evidence.kind}")
            if not _valid_evidence_path(evidence.path):
                errors.append(f"{prefix}: invalid evidence path: {evidence.path}")
            elif not (repository / evidence.path).is_file():
                errors.append(f"{prefix}: evidence path does not exist: {evidence.path}")

        if requirement.status == "seed" and not requirement.evidence:
            errors.append(f"{prefix}: seed requires at least one evidence item")
        if requirement.status == "reviewed" and not requirement.evidence:
            errors.append(f"{prefix}: reviewed requires at least one evidence item")
        stage_options = STAGE_EVIDENCE_OPTIONS.get(requirement.stage)
        if (
            requirement.status == "validated"
            and stage_options is not None
            and not any(option <= evidence_kinds for option in stage_options)
        ):
            descriptions = " or ".join(
                "+".join(sorted(option)) for option in stage_options
            )
            errors.append(
                f"{prefix}: validated stage {requirement.stage} requires one of: "
                f"{descriptions}"
            )
        if requirement.status == "validated" and requirement.gap:
            errors.append(f"{prefix}: validated requirement must have an empty gap")
        if requirement.status != "validated" and not requirement.gap:
            errors.append(f"{prefix}: incomplete requirement must describe its gap")
    return sorted(errors)


def coverage_score(manifest: CoverageManifest) -> float:
    """计算证据状态加权的仓库就绪度。"""
    if not manifest.requirements:
        return 0.0
    total = sum(STATE_WEIGHTS.get(item.status, 0.0) for item in manifest.requirements)
    return round(total / len(manifest.requirements) * 100, 1)


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_coverage_report(manifest: CoverageManifest) -> str:
    """渲染确定性的公开 Markdown 覆盖报告。"""
    score = coverage_score(manifest)
    lines = [
        "# 知识库覆盖审计",
        "",
        f"- 清单日期：{manifest.as_of.isoformat()}",
        f"- 仓库就绪度，不是预期收益：**{score:.1f}%**",
        f"- 需求总数：{len(manifest.requirements)}",
        "",
        "> validated 只表示当前清单所列证据通过仓库规则；不保证投资收益，也不免除后续更新。",
        "",
        "## 分轴状态",
        "",
        "| 维度 | missing | seed | reviewed | validated | 就绪度 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for axis in ALLOWED_AXES:
        items = [item for item in manifest.requirements if item.axis == axis]
        counts = {state: sum(item.status == state for item in items) for state in ALLOWED_STATES}
        axis_manifest = CoverageManifest(2, manifest.as_of, tuple(items))
        lines.append(
            f"| {AXIS_LABELS[axis]} | {counts['missing']} | {counts['seed']} | "
            f"{counts['reviewed']} | {counts['validated']} | {coverage_score(axis_manifest):.1f}% |"
        )

    lines.extend(
        [
            "",
            "## 分能力阶段状态",
            "",
            "| 阶段 | 含义 | missing | seed | reviewed | validated | 就绪度 |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for stage in ALLOWED_STAGES:
        items = [item for item in manifest.requirements if item.stage == stage]
        counts = {state: sum(item.status == state for item in items) for state in ALLOWED_STATES}
        stage_manifest = CoverageManifest(2, manifest.as_of, tuple(items))
        lines.append(
            f"| `{stage}` | {STAGE_LABELS[stage]} | {counts['missing']} | {counts['seed']} | "
            f"{counts['reviewed']} | {counts['validated']} | "
            f"{coverage_score(stage_manifest):.1f}% |"
        )

    lines.extend(
        [
            "",
            "## 逐项证据与缺口",
            "",
            "| ID | 维度 | 阶段 | 要求 | 状态 | 最后核验 | 证据 | 缺口 |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for item in sorted(manifest.requirements, key=lambda value: (value.axis, value.id)):
        evidence = "<br>".join(f"`{entry.kind}:{entry.path}`" for entry in item.evidence) or "—"
        gap = _escape_cell(item.gap) if item.gap else "—"
        lines.append(
            f"| `{item.id}` | {AXIS_LABELS.get(item.axis, item.axis)} | "
            f"`{item.stage}` | {_escape_cell(item.title)} | {item.status} | "
            f"{item.verified.isoformat()} | "
            f"{evidence} | {gap} |"
        )
    lines.append("")
    return "\n".join(lines)
