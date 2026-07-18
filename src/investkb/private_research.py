"""Create and validate a local-only research workspace without reading it publicly."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import math
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
REQUIRED_ITEM_FIELDS = {
    "watchlist.yaml": {"market", "symbol", "thesis", "disconfirming_evidence", "status"},
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
        "decision",
        "thesis",
        "disconfirming_evidence",
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
MANDATORY_PROHIBITED_ACTIONS = {"automatic_trading", "leverage", "short_selling"}


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


def _nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PrivateWorkspaceError(f"{field} must be a non-empty string")
    return value


def _finite_number(value: Any, field: str, *, positive: bool) -> float:
    if isinstance(value, bool):
        raise PrivateWorkspaceError(f"{field} must be a finite number")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise PrivateWorkspaceError(f"{field} must be a finite number") from exc
    valid = math.isfinite(number) and (number > 0 if positive else number >= 0)
    if not valid:
        boundary = "positive" if positive else "non-negative"
        raise PrivateWorkspaceError(f"{field} must be finite and {boundary}")
    return number


def _iso_date_or_datetime(value: Any, field: str) -> None:
    if isinstance(value, (date, datetime)):
        return
    _nonempty_string(value, field)
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        try:
            date.fromisoformat(value)
        except ValueError as exc:
            raise PrivateWorkspaceError(f"{field} must be an ISO date or datetime") from exc


def _validate_policy(policy: dict[str, Any]) -> None:
    currency = policy["base_currency"]
    if currency is not None and (
        not isinstance(currency, str) or len(currency) != 3 or not currency.isupper()
    ):
        raise PrivateWorkspaceError("base_currency must be null or a three-letter uppercase code")
    horizon = policy["horizon_years"]
    if horizon is not None:
        _finite_number(horizon, "horizon_years", positive=True)
    drawdown = policy["maximum_tolerable_drawdown_pct"]
    if drawdown is not None:
        value = _finite_number(drawdown, "maximum_tolerable_drawdown_pct", positive=True)
        if value > 100:
            raise PrivateWorkspaceError("maximum_tolerable_drawdown_pct must not exceed 100")
    markets = policy["allowed_markets"]
    if not isinstance(markets, list) or not all(
        isinstance(item, str) and item.strip() for item in markets
    ):
        raise PrivateWorkspaceError("allowed_markets must be a list of non-empty strings")
    prohibited = policy["prohibited_actions"]
    if not isinstance(prohibited, list) or not all(
        isinstance(item, str) and item.strip() for item in prohibited
    ):
        raise PrivateWorkspaceError("prohibited_actions must be a list of non-empty strings")
    if not MANDATORY_PROHIBITED_ACTIONS <= set(prohibited):
        raise PrivateWorkspaceError("prohibited_actions must preserve mandatory safety boundaries")


def _validate_item(name: str, item: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_ITEM_FIELDS[name] - set(item))
    if missing:
        raise PrivateWorkspaceError(f"missing field in {name}: {missing[0]}")
    for field in ("market", "symbol"):
        if field in item:
            _nonempty_string(item[field], field)
    for field in ("thesis", "disconfirming_evidence"):
        if field in item:
            _nonempty_string(item[field], field)
    if name == "watchlist.yaml":
        status = _nonempty_string(item["status"], "status")
        if status not in {"researching", "monitoring", "rejected", "archived"}:
            raise PrivateWorkspaceError("status is not an allowed watchlist state")
        if "added_at" in item:
            _iso_date_or_datetime(item["added_at"], "added_at")
    elif name == "positions.yaml":
        _finite_number(item["quantity"], "quantity", positive=True)
        _finite_number(item["average_cost"], "average_cost", positive=False)
        currency = _nonempty_string(item["cost_currency"], "cost_currency")
        if len(currency) != 3 or not currency.isupper():
            raise PrivateWorkspaceError("cost_currency must be a three-letter uppercase code")
        _iso_date_or_datetime(item["acquired_at"], "acquired_at")
    else:
        _nonempty_string(item["id"], "id")
        _iso_date_or_datetime(item["timestamp"], "timestamp")
        decision = _nonempty_string(item["decision"], "decision")
        if decision not in {"research", "no_action", "buy", "sell", "hold", "reject"}:
            raise PrivateWorkspaceError("decision is not an allowed journal state")
        if "outcome" in item:
            _nonempty_string(item["outcome"], "outcome")


def validate_private_workspace(root: Path) -> PrivateWorkspaceSummary:
    """Validate structure only; never emit private content."""

    directory = _private_directory(root)
    if not directory.is_dir():
        raise PrivateWorkspaceError("private workspace does not exist")
    unexpected_entries = sorted(
        path.name for path in directory.iterdir() if path.name not in DOCUMENTS
    )
    if unexpected_entries:
        raise PrivateWorkspaceError(f"unexpected private entry: {unexpected_entries[0]}")
    documents = {name: _load_document(directory / name) for name in DOCUMENTS}
    _validate_policy(documents["policy.yaml"])
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
            _validate_item(name, item)
    return PrivateWorkspaceSummary(
        watchlist=len(documents["watchlist.yaml"]["items"]),
        positions=len(documents["positions.yaml"]["positions"]),
        journal_entries=len(documents["decision-journal.yaml"]["entries"]),
    )
