const filterSelect = document.getElementById("chart-filter");
const dashboardGrid = document.getElementById("dashboard-grid");

async function loadSpecs() {
  const response = await fetch("plot-specs.json", { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Failed to load plot-specs.json");
  }
  return response.json();
}

function cleanLayout(layout) {
  const next = { ...(layout || {}) };
  next.template = "plotly_white";
  next.paper_bgcolor = "#ffffff";
  next.plot_bgcolor = "#ffffff";
  next.margin = { l: 50, r: 30, t: 70, b: 50, ...(next.margin || {}) };
  next.font = { family: "Inter, Arial, sans-serif", size: 13, ...(next.font || {}) };
  next.showlegend = next.showlegend !== false;
  return next;
}

function buildChartCard(chart, idx) {
  const section = document.createElement("section");
  section.className = "viz-card";
  section.dataset.chartIndex = String(idx + 1);

  const title = document.createElement("h3");
  title.className = "viz-title";
  title.textContent = `V${idx + 1}: ${chart.title || "Taxi Visualization"}`;

  const plotDiv = document.createElement("div");
  plotDiv.className = "plot-container";
  plotDiv.id = `plot-${idx + 1}`;

  section.appendChild(title);
  section.appendChild(plotDiv);
  dashboardGrid.appendChild(section);

  Plotly.newPlot(plotDiv.id, chart.data || [], cleanLayout(chart.layout), {
    responsive: true,
    displaylogo: false,
  });
}

function wireFilter(count) {
  for (let i = 1; i <= count; i += 1) {
    const opt = document.createElement("option");
    opt.value = String(i);
    opt.textContent = `V${i}`;
    filterSelect.appendChild(opt);
  }

  filterSelect.addEventListener("change", () => {
    const value = filterSelect.value;
    const cards = dashboardGrid.querySelectorAll(".viz-card");
    cards.forEach((card) => {
      card.style.display = value === "all" || card.dataset.chartIndex === value ? "block" : "none";
    });
  });
}

(async () => {
  try {
    const specs = await loadSpecs();
    const charts = specs.charts || [];
    charts.forEach(buildChartCard);
    wireFilter(charts.length);
  } catch (err) {
    dashboardGrid.innerHTML = `<section class="viz-card"><h3 class="viz-title">Dashboard failed to load</h3><p>${err.message}</p></section>`;
    console.error(err);
  }
})();
