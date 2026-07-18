from pathlib import Path

import pytest
import yaml

from investkb.private_research import (
    PrivateWorkspaceError,
    initialize_private_workspace,
    validate_private_workspace,
)


def test_private_workspace_initializes_empty_holdings_and_validates(tmp_path: Path) -> None:
    summary = initialize_private_workspace(tmp_path)

    assert summary.positions == 0
    assert summary.watchlist == 0
    assert summary.journal_entries == 0
    assert sorted(path.name for path in (tmp_path / "private").iterdir()) == [
        "decision-journal.yaml",
        "policy.yaml",
        "positions.yaml",
        "watchlist.yaml",
    ]
    assert validate_private_workspace(tmp_path) == summary


def test_initializer_refuses_to_overwrite_existing_private_research(tmp_path: Path) -> None:
    initialize_private_workspace(tmp_path)

    with pytest.raises(PrivateWorkspaceError, match="already exists"):
        initialize_private_workspace(tmp_path)


def test_private_validator_rejects_credential_and_order_fields(tmp_path: Path) -> None:
    initialize_private_workspace(tmp_path)
    watchlist = tmp_path / "private/watchlist.yaml"
    payload = yaml.safe_load(watchlist.read_text(encoding="utf-8"))
    payload["cookie"] = "session material must never be accepted"
    watchlist.write_text(yaml.safe_dump(payload), encoding="utf-8")

    with pytest.raises(PrivateWorkspaceError, match="forbidden field: cookie"):
        validate_private_workspace(tmp_path)


def test_private_validator_rejects_symlink_escape(tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    (tmp_path / "private").symlink_to(outside, target_is_directory=True)

    with pytest.raises(PrivateWorkspaceError, match="symlink"):
        validate_private_workspace(tmp_path)


def test_private_validator_accepts_documented_watchlist_without_positions(tmp_path: Path) -> None:
    initialize_private_workspace(tmp_path)
    watchlist = tmp_path / "private/watchlist.yaml"
    payload = yaml.safe_load(watchlist.read_text(encoding="utf-8"))
    payload["items"] = [
        {
            "market": "HK",
            "symbol": "SYNTHETIC",
            "thesis": "教学占位，不是证券建议",
            "disconfirming_evidence": "公开证据与原命题相反",
            "status": "researching",
        }
    ]
    watchlist.write_text(yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8")

    summary = validate_private_workspace(tmp_path)

    assert summary.watchlist == 1
    assert summary.positions == 0


@pytest.mark.parametrize(
    ("document", "field", "value", "message"),
    [
        ("watchlist.yaml", "items", [{}], "missing field"),
        (
            "positions.yaml",
            "positions",
            [
                {
                    "market": "US",
                    "symbol": "SYNTHETIC",
                    "quantity": -1,
                    "average_cost": 10,
                    "cost_currency": "USD",
                    "acquired_at": "2026-07-18",
                }
            ],
            "quantity",
        ),
        ("decision-journal.yaml", "entries", [{}], "missing field"),
    ],
)
def test_private_validator_enforces_required_fields_and_domains(
    tmp_path: Path, document: str, field: str, value, message: str
) -> None:
    initialize_private_workspace(tmp_path)
    path = tmp_path / "private" / document
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    payload[field] = value
    path.write_text(yaml.safe_dump(payload), encoding="utf-8")

    with pytest.raises(PrivateWorkspaceError, match=message):
        validate_private_workspace(tmp_path)


def test_private_validator_preserves_mandatory_policy_prohibitions(tmp_path: Path) -> None:
    initialize_private_workspace(tmp_path)
    policy = tmp_path / "private/policy.yaml"
    payload = yaml.safe_load(policy.read_text(encoding="utf-8"))
    payload["prohibited_actions"] = []
    policy.write_text(yaml.safe_dump(payload), encoding="utf-8")

    with pytest.raises(PrivateWorkspaceError, match="prohibited_actions"):
        validate_private_workspace(tmp_path)


def test_private_validator_reports_missing_top_level_fields_cleanly(tmp_path: Path) -> None:
    initialize_private_workspace(tmp_path)
    policy = tmp_path / "private/policy.yaml"
    payload = yaml.safe_load(policy.read_text(encoding="utf-8"))
    del payload["base_currency"]
    policy.write_text(yaml.safe_dump(payload), encoding="utf-8")

    with pytest.raises(PrivateWorkspaceError, match="missing field in policy.yaml: base_currency"):
        validate_private_workspace(tmp_path)


def test_private_validator_rejects_unknown_workspace_entries(tmp_path: Path) -> None:
    initialize_private_workspace(tmp_path)
    (tmp_path / "private/credentials.yaml").write_text("schema_version: 1\n", encoding="utf-8")

    with pytest.raises(PrivateWorkspaceError, match="unexpected private entry"):
        validate_private_workspace(tmp_path)
