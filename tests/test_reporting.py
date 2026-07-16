from pathlib import Path
import warnings

import pandas as pd

from investkb.backtest.models import BacktestResult
from investkb.reporting import build_report


def result_fixture() -> BacktestResult:
    dates = pd.date_range("2024-01-01", periods=3)
    positions = pd.DataFrame(
        {"date": dates, "shares": [0, 100, 100], "cash": [1000, 0, 0], "equity": [1000, 1050, 1100]}
    )
    trades = pd.DataFrame(
        {
            "date": [dates[1]],
            "side": ["buy"],
            "quantity": [100],
            "price": [10.0],
            "gross": [1000.0],
            "fees": [0.0],
            "cash_after": [0.0],
        }
    )
    return BacktestResult(
        equity=pd.Series([1000.0, 1050.0, 1100.0], index=dates, name="equity"),
        positions=positions,
        orders=trades.copy(),
        trades=trades,
        assumptions={"execution": "next open", "commission_rate": 0.0},
    )


def test_report_contains_reproducibility_sections(tmp_path: Path) -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        path = build_report(
            result_fixture(), tmp_path, reproduction_command="investkb demo backtest --offline"
        )
    assert caught == []
    text = path.read_text(encoding="utf-8")

    for heading in ["数据", "假设", "费用", "基准", "结果", "限制", "复现命令"]:
        assert heading in text
    for name in ["metrics.csv", "equity.csv", "trades.csv", "equity.png"]:
        assert (tmp_path / name).is_file()
