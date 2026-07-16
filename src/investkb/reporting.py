"""把回测结果输出为可复现的 Markdown、CSV 与图表。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from investkb.backtest.models import BacktestResult
from investkb.metrics import performance_summary


def _display(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def build_report(
    result: BacktestResult,
    output_directory: str | Path,
    *,
    title: str = "策略研究报告",
    data_description: str = "由调用方提供的标准化日线数据",
    benchmark_description: str = "未提供独立基准；正式研究不得省略",
    limitations: list[str] | None = None,
    reproduction_command: str,
) -> Path:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    metrics = performance_summary(result.equity)
    pd.DataFrame([{"metric": key, "value": value} for key, value in metrics.items()]).to_csv(
        output / "metrics.csv", index=False
    )
    result.equity.rename("equity").to_csv(output / "equity.csv")
    result.trades.to_csv(output / "trades.csv", index=False)

    figure, axis = plt.subplots(figsize=(9, 4.5))
    result.equity.plot(ax=axis, title="Equity Curve")
    axis.set_ylabel("Equity")
    axis.grid(alpha=0.25)
    figure.tight_layout()
    figure.savefig(output / "equity.png", dpi=150)
    plt.close(figure)

    fee_items = {
        key: value
        for key, value in result.assumptions.items()
        if key in {"commission_rate", "minimum_commission", "stamp_duty_rate", "slippage_bps"}
    }
    limits = limitations or [
        "历史回测不代表未来表现。",
        "示例未建模容量、盘口深度和所有公司行动。",
        "结果只用于学习与研究，不构成投资建议。",
    ]
    metric_rows = "\n".join(f"| {key} | {_display(value)} |" for key, value in metrics.items())
    assumption_rows = "\n".join(
        f"- `{key}`: {_display(value)}" for key, value in result.assumptions.items()
    )
    fee_rows = (
        "\n".join(f"- `{key}`: {_display(value)}" for key, value in fee_items.items())
        or "- 未单独提供"
    )
    limit_rows = "\n".join(f"- {item}" for item in limits)
    report = f"""# {title}

## 数据

{data_description}

## 假设

{assumption_rows}

## 费用

{fee_rows}

## 基准

{benchmark_description}

## 结果

| 指标 | 数值 |
|---|---:|
{metric_rows}

![净值曲线](equity.png)

## 限制

{limit_rows}

## 复现命令

```bash
{reproduction_command}
```
"""
    path = output / "report.md"
    path.write_text(report, encoding="utf-8")
    return path
