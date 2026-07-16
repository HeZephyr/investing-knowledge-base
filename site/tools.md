# 互动投资工具

这些计算器全部在浏览器本地运行，不发送输入。结果用于建立数量感，不代表收益预测。

<div class="tool-grid">
  <section class="tool-card" data-calculator="compound">
    <h2>复利情景</h2>
    <label>初始本金（元）<input name="principal" type="number" min="0" step="100" value="100000"></label>
    <label>每月投入（元）<input name="monthly" type="number" min="0" step="100" value="2000"></label>
    <label>假设年化收益率（%）<input name="rate" type="number" step="0.1" value="6"></label>
    <label>年数<input name="years" type="number" min="1" max="60" value="10"></label>
    <button class="md-button md-button--primary" type="button">计算</button>
    <output aria-live="polite"></output>
  </section>

  <section class="tool-card" data-calculator="cost">
    <h2>交易成本拖累</h2>
    <label>组合金额（元）<input name="capital" type="number" min="0" step="100" value="100000"></label>
    <label>单边综合费率（%）<input name="fee" type="number" min="0" step="0.001" value="0.1"></label>
    <label>每年完整换手次数<input name="turnovers" type="number" min="0" step="0.5" value="4"></label>
    <button class="md-button md-button--primary" type="button">计算</button>
    <output aria-live="polite"></output>
  </section>

  <section class="tool-card" data-calculator="drawdown">
    <h2>回撤修复</h2>
    <label>当前回撤（%）<input name="drawdown" type="number" min="0.1" max="99" step="0.1" value="20"></label>
    <button class="md-button md-button--primary" type="button">计算</button>
    <output aria-live="polite"></output>
  </section>
</div>

## 怎么理解结果

- 收益率只是情景参数，不能把过去的市场回报直接当成未来假设。
- 买入和卖出都会产生成本；高换手策略还会遇到滑点、冲击成本和无法成交。
- 下跌与修复不对称：亏损 50% 后，需要上涨 100% 才能回到原点。
