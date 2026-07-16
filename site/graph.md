# 知识图谱

图谱由 Wiki 双链自动生成。搜索概念或按类别筛选，拖动画布、滚轮缩放；点击节点可进入对应页面。

<div class="graph-controls">
  <input id="graph-search" type="search" placeholder="搜索概念，例如：回撤、ETF、复权" aria-label="搜索知识图谱">
  <select id="graph-category" aria-label="筛选类别"><option value="all">全部类别</option></select>
  <span id="graph-status" role="status">正在加载…</span>
</div>
<div class="graph-shell">
  <canvas id="knowledge-graph" aria-label="投资知识图谱"></canvas>
  <div id="graph-empty" hidden>没有匹配节点，请更换关键词或类别。</div>
</div>

颜色代表主题类别，连线代表 Wiki 页面之间的显式引用。图谱适合发现关联，不代表两个概念存在因果关系。
