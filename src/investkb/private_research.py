"""Create and validate a local-only research workspace without reading it publicly."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class PrivateWorkspaceError(ValueError):
    """Raised when a local private workspace violates the public safety contract."""


@dataclass(frozen=True)
class PrivateWorkspaceSummary:
    watchlist: int
    positions: int
    journal_entries: int


DOCUMENTS: dict[str, dict[str, Any]] = {
    "policy.yaml": {
        "schema_version": 1,
        "base_currency": None,
        "horizon_years": None,
        "maximum_tolerable_drawdown_pct": None,
        "allowed_markets": [],
        "prohibited_actions": ["automatic_trading", "leverage", "short_selling"],
    },
    "watchlist.yaml": {"schema_version": 1, "items": []},
    "positions.yaml": {"schema_version": 1, "as_of": None, "positions": []},
    "decision-journal.yaml": {"schema_version": 1, "entries": []},
}

TOP_LEVEL_FIELDS = {
    "policy.yaml": set(DOCUMENTS["policy.yaml"]),
    "watchlist.yaml": {"schema_version", "items"},
    "positions.yaml": {"schema_version", "as_of", "positions"},
    "decision-journal.yaml": {"schema_version", "entries"},
}
ITEM_FIELDS = {
    "watchlist.yaml": {
        "market",
        "symbol",
        "thesis",
        "disconfirming_evidence",
        "status",
        "added_at",
    },
    "positions.yaml": {
        "market",
        "symbol",
        "quantity",
        "average_cost",
        "cost_currency",
        "acquired_at",
    },
    "decision-journal.yaml": {
        "id",
        "timestamp",
        "market",
        "symbol",
        "decision",
        "thesis",
        "disconfirming_evidence",
        "outcome",
    },
}
LIST_FIELD = {
    "watchlist.yaml": "items",
    "positions.yaml": "positions",
    "decision-journal.yaml": "entries",
}
FORBIDDEN_KEY_FRAGMENTS = {
    "api_key",
    "broker",
    "cookie",
    "credential",
    "order_endpoint",
    "password",
    "secret",
    "token",
    "auto_trade",
}


def _private_directory(root: Path) -> Path:
    root = Path(root)
    directory = root / "private"
    if directory.is_symlink():
        raise PrivateWorkspaceError("private workspace must not be a symlink")
    return directory


def _reject_forbidden_keys(value: Any) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            if any(fragment in normalized for fragment in FORBIDDEN_KEY_FRAGMENTS):
                raise PrivateWorkspaceError(f"forbidden field: {key}")
            _reject_forbidden_keys(child)
    elif isinstance(value, list):
        for child in value:
            _reject_forbidden_keys(child)


def initialize_private_workspace(root: Path) -> PrivateWorkspaceSummary:
    """Create empty, ignored YAML files and refuse all overwrite or symlink behavior."""

    directory = _private_directory(root)
    if directory.exists():
        raise PrivateWorkspaceError("private workspace already exists")
    directory.mkdir(parents=True)
    for name, payload in DOCUMENTS.items():
        destination = directory / name
        destination.write_text(
            yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8"
        )
    return validate_private_workspace(root)


def _load_document(path: Path) -> dict[str, Any]:
    if path.is_symlink():
        raise PrivateWorkspaceError(f"private document must not be a symlink: {path.name}")
    if not path.is_file():
        raise PrivateWorkspaceError(f"missing private document: {path.name}")
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise PrivateWorkspaceError(f"invalid YAML: {path.name}") from exc
    if not isinstance(payload, dict):
        raise PrivateWorkspaceError(f"private document must be a mapping: {path.name}")
    _reject_forbidden_keys(payload)
    if payload.get("schema_version") != 1:
        raise PrivateWorkspaceError(f"unsupported schema_version: {path.name}")
    unexpected = sorted(set(payload) - TOP_LEVEL_FIELDS[path.name])
    if unexpected:
        raise PrivateWorkspaceError(f"unexpected field in {path.name}: {unexpected[0]}")
    return payload


def validate_private_workspace(root: Path) -> PrivateWorkspaceSummary:
    """Validate structure only; never emit private content."""

    directory = _private_directory(root)
    if not directory.is_dir():
        raise PrivateWorkspaceError("private workspace does not exist")
    documents = {name: _load_document(directory / name) for name in DOCUMENTS}
    for name, list_field in LIST_FIELD.items():
        items = documents[name].get(list_field)
        if not isinstance(items, list):
            raise PrivateWorkspaceError(f"{list_field} must be a list: {name}")
        for item in items:
            if not isinstance(item, dict):
                raise PrivateWorkspaceError(f"{list_field} entries must be mappings: {name}")
            unexpected = sorted(set(item) - ITEM_FIELDS[name])
            if unexpected:
                raise PrivateWorkspaceError(f"unexpected field in {name}: {unexpected[0]}")
            _reject_forbidden_keys(item)
    return PrivateWorkspaceSummary(
        watchlist=len(documents["watchlist.yaml"]["items"]),
        positions=len(documents["positions.yaml"]["positions"]),
        journal_entries=len(documents["decision-journal.yaml"]["entries"]),
    )
