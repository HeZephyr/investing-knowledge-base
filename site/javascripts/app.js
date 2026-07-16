(() => {
  "use strict";
  const scriptUrl = new URL(document.currentScript.src);
  const siteRoot = new URL("../", scriptUrl);
  const money = new Intl.NumberFormat("zh-CN", { style: "currency", currency: "CNY", maximumFractionDigits: 0 });
  const progressKey = "investkb.completed.v1";

  async function loadJson(path) {
    const response = await fetch(new URL(path, siteRoot));
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }

  function number(card, name) { return Number(card.querySelector(`[name="${name}"]`).value); }
  function valid(values) { return values.every(Number.isFinite); }

  function setupCalculators() {
    document.querySelectorAll("[data-calculator]").forEach((card) => {
      const output = card.querySelector("output");
      const calculate = () => {
        let headline = "", note = "";
        if (card.dataset.calculator === "compound") {
          const p = number(card, "principal"), m = number(card, "monthly"), r = number(card, "rate") / 1200, y = number(card, "years");
          if (!valid([p, m, r, y]) || p < 0 || m < 0 || y <= 0) return output.textContent = "请输入有效的非负金额和正年数。";
          const months = Math.round(y * 12);
          const future = r === 0 ? p + m * months : p * (1 + r) ** months + m * ((1 + r) ** months - 1) / r;
          const invested = p + m * months;
          headline = money.format(future); note = `累计投入 ${money.format(invested)}，情景收益 ${money.format(future - invested)}。`;
        } else if (card.dataset.calculator === "cost") {
          const capital = number(card, "capital"), fee = number(card, "fee") / 100, turns = number(card, "turnovers");
          if (!valid([capital, fee, turns]) || capital < 0 || fee < 0 || turns < 0) return output.textContent = "请输入有效的非负数值。";
          const annual = capital * fee * 2 * turns;
          headline = `${money.format(annual)} / 年`; note = `约占本金 ${(fee * 2 * turns * 100).toFixed(2)}%，尚未计滑点和冲击成本。`;
        } else {
          const drawdown = number(card, "drawdown");
          if (!Number.isFinite(drawdown) || drawdown <= 0 || drawdown >= 100) return output.textContent = "回撤需大于 0% 且小于 100%。";
          const recovery = drawdown / (100 - drawdown) * 100;
          headline = `需要上涨 ${recovery.toFixed(2)}%`; note = `从回撤 ${drawdown.toFixed(1)}% 后的净值恢复至原高点。`;
        }
        output.innerHTML = `<span class="result-big">${headline}</span><span class="result-note">${note}</span>`;
      };
      card.querySelector("button").addEventListener("click", calculate);
      calculate();
    });
  }

  function completed() { try { return new Set(JSON.parse(localStorage.getItem(progressKey) || "[]")); } catch { return new Set(); } }
  function saveCompleted(items) { localStorage.setItem(progressKey, JSON.stringify([...items])); updateProgress(items); }
  async function updateProgress(items = completed()) {
    const panels = document.querySelectorAll("[data-progress-panel]");
    if (!panels.length) return;
    try {
      const graph = await loadJson("assets/data/knowledge-graph.json");
      const total = graph.nodes.length, done = [...items].filter((id) => graph.nodes.some((n) => n.id === id)).length;
      panels.forEach((panel) => {
        panel.querySelector("[data-progress-label]").textContent = `${done} / ${total}`;
        panel.querySelector("[data-progress-bar]").style.width = `${total ? done / total * 100 : 0}%`;
      });
    } catch { panels.forEach((panel) => panel.querySelector("[data-progress-label]").textContent = "暂不可用"); }
  }

  function setupPageProgress() {
    const match = location.pathname.match(/\/wiki\/(?:[^/]+\/)*([^/]+)\/?$/);
    const article = document.querySelector("article.md-content__inner");
    if (!match || !article) return;
    const id = decodeURIComponent(match[1]), items = completed();
    const box = document.createElement("div"); box.className = "page-progress";
    const button = document.createElement("button"); button.className = "md-button";
    const render = () => { button.textContent = items.has(id) ? "✓ 已学完（点击取消）" : "标记为已学完"; };
    button.addEventListener("click", () => { items.has(id) ? items.delete(id) : items.add(id); saveCompleted(items); render(); });
    render(); box.append("学习记录：", button); article.append(box);
  }

  async function setupStats() {
    const cards = document.querySelectorAll("#content-stats strong"); if (!cards.length) return;
    try { const s = await loadJson("assets/data/content-summary.json"); [s.wiki_pages, s.raw_pages, s.output_pages].forEach((v, i) => cards[i].textContent = v); } catch { cards.forEach((c) => c.textContent = "—"); }
  }

  async function setupGraph() {
    const canvas = document.querySelector("#knowledge-graph"); if (!canvas) return;
    const ctx = canvas.getContext("2d"), shell = canvas.parentElement, status = document.querySelector("#graph-status"), empty = document.querySelector("#graph-empty");
    const search = document.querySelector("#graph-search"), category = document.querySelector("#graph-category");
    const colors = { navigation: "#f59e0b", risk: "#ef4444", markets: "#3b82f6", products: "#8b5cf6", assets: "#eab308", sectors: "#ec4899", quant: "#14b8a6", concepts: "#22c55e", other: "#64748b" };
    let graph;
    try { graph = await loadJson("assets/data/knowledge-graph.json"); } catch (error) { status.textContent = `加载失败：${error.message}`; return; }
    [...new Set(graph.nodes.map((n) => n.category))].sort().forEach((value) => category.add(new Option(value, value)));
    let scale = 1, offsetX = 0, offsetY = 0, drag = null, visible = [];
    function resize() { const dpr = devicePixelRatio || 1; canvas.width = shell.clientWidth * dpr; canvas.height = canvas.clientHeight * dpr; ctx.setTransform(dpr,0,0,dpr,0,0); draw(); }
    function filter() {
      const q = search.value.trim().toLowerCase(), cat = category.value;
      visible = graph.nodes.filter((n) => (!q || `${n.label} ${n.id}`.toLowerCase().includes(q)) && (cat === "all" || n.category === cat));
      const cols = Math.ceil(Math.sqrt(Math.max(visible.length, 1)));
      visible.forEach((n, i) => { if (n.x == null) { n.x = 90 + (i % cols) * 125 + Math.random() * 25; n.y = 75 + Math.floor(i / cols) * 95 + Math.random() * 20; } });
      empty.hidden = visible.length > 0; status.textContent = `${visible.length} 个节点 · ${graph.links.length} 条连接`; draw();
    }
    function point(event) { const r = canvas.getBoundingClientRect(); return { x:(event.clientX-r.left-offsetX)/scale, y:(event.clientY-r.top-offsetY)/scale }; }
    function hit(p) { return [...visible].reverse().find((n) => Math.hypot(n.x-p.x,n.y-p.y) < 18); }
    function draw() {
      const w = canvas.clientWidth, h = canvas.clientHeight; ctx.clearRect(0,0,w,h); ctx.save(); ctx.translate(offsetX,offsetY); ctx.scale(scale,scale);
      const ids = new Set(visible.map((n) => n.id)), byId = new Map(graph.nodes.map((n) => [n.id,n]));
      ctx.strokeStyle = "rgba(100,116,139,.28)"; ctx.lineWidth = 1;
      graph.links.forEach((e) => { if (!ids.has(e.source)||!ids.has(e.target)) return; const a=byId.get(e.source),b=byId.get(e.target); ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke(); });
      visible.forEach((n) => { ctx.beginPath();ctx.fillStyle=colors[n.category]||colors.other;ctx.arc(n.x,n.y,8,0,Math.PI*2);ctx.fill();ctx.font="12px system-ui";ctx.fillStyle=getComputedStyle(document.body).color;ctx.fillText(n.label,n.x+13,n.y+4); }); ctx.restore();
    }
    canvas.addEventListener("pointerdown", (e) => { const p=point(e),node=hit(p);drag={node,startX:e.clientX,startY:e.clientY,ox:offsetX,oy:offsetY};canvas.setPointerCapture(e.pointerId); });
    canvas.addEventListener("pointermove", (e) => { if(!drag)return; if(drag.node){const p=point(e);drag.node.x=p.x;drag.node.y=p.y;}else{offsetX=drag.ox+e.clientX-drag.startX;offsetY=drag.oy+e.clientY-drag.startY;}draw(); });
    canvas.addEventListener("pointerup", (e) => { if(drag?.node && Math.hypot(e.clientX-drag.startX,e.clientY-drag.startY)<5) location.href=new URL(drag.node.url,siteRoot); drag=null; });
    canvas.addEventListener("wheel", (e) => { e.preventDefault(); scale=Math.min(2.5,Math.max(.45,scale*(e.deltaY<0?1.1:.9)));draw(); }, {passive:false});
    search.addEventListener("input",filter); category.addEventListener("change",filter); addEventListener("resize",resize); filter(); resize();
  }

  function boot() { setupCalculators(); setupStats(); setupPageProgress(); updateProgress(); setupGraph(); }
  if (typeof document$ !== "undefined") document$.subscribe(boot);
  else document.addEventListener("DOMContentLoaded", boot);
})();
