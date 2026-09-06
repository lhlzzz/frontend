const grid = document.querySelector("#agent-grid");
const detail = document.querySelector("#detail");

const escapeHtml = (value) => String(value ?? "")
  .replaceAll("&", "&amp;").replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;").replaceAll('"', "&quot;");

async function getJson(url) {
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) throw new Error("无法读取平台代理状态。");
  return response.json();
}

function renderAgents(items) {
  grid.innerHTML = items.map((item) => `
    <button class="agent" type="button" data-key="${item.agent.key}">
      <span class="key">${escapeHtml(item.agent.key)}</span>
      <h2>${escapeHtml(item.agent.name)}</h2>
      <p>${escapeHtml(item.agent.role)}</p>
      <footer>
        <small>${escapeHtml(item.agent.workspace)} 独立数据</small>
        <span class="state ${escapeHtml(item.state)}">${escapeHtml(item.state)}</span>
      </footer>
    </button>
  `).join("");
}

function renderDetail(item) {
  const snapshot = item.snapshot;
  detail.hidden = false;
  if (!snapshot) {
    detail.innerHTML = `<div class="detail-head"><div><p>${escapeHtml(item.agent.key)}</p><h2>${escapeHtml(item.agent.name)}</h2></div><strong class="state ${escapeHtml(item.state)}">${escapeHtml(item.state)}</strong></div><p>尚未连接该平台的内部只读适配器；未显示任何模拟数据。</p>`;
    return;
  }
  const metrics = snapshot.metrics || {};
  const records = snapshot.records || [];
  detail.innerHTML = `
    <div class="detail-head"><div><p>${escapeHtml(item.agent.key)}</p><h2>${escapeHtml(item.agent.name)}</h2><p>${escapeHtml(snapshot.voice || "")}</p></div><strong class="state connected">connected</strong></div>
    <div class="metrics">${Object.entries(metrics).map(([key, value]) => `<div><span>${escapeHtml(key)}</span><strong>${escapeHtml(value)}</strong></div>`).join("")}</div>
    <div class="records"><p>${escapeHtml(snapshot.boundary || "")}</p>${records.length ? records.map((record) => `<div class="record"><strong>${escapeHtml(record.title || record.id)}</strong><span>${escapeHtml(record.review_outcome || record.status || "已读取")}</span></div>`).join("") : "<p>当前没有记录。</p>"}</div>
  `;
}

grid.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-key]");
  if (!button) return;
  detail.hidden = false;
  detail.textContent = "正在读取平台数据。";
  try { renderDetail(await getJson(`/api/agents/${button.dataset.key}`)); }
  catch (error) { detail.textContent = error.message; }
});

getJson("/api/agents").then(renderAgents).catch((error) => {
  grid.innerHTML = `<p class="loading">${escapeHtml(error.message)}</p>`;
});
