/**
 * Shared site logic: load plot-specs.json, Plotly layout cleanup, nav dropdown.
 */

const VIZ_COUNT = 12;

async function loadSpecs() {
  const response = await fetch("plot-specs.json", { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Could not load plot-specs.json — run: python3 scripts/export_plot_specs.py");
  }
  return response.json();
}

function cleanLayout(layout) {
  const next = { ...(layout || {}) };
  next.template = "plotly_white";
  next.paper_bgcolor = "#ffffff";
  next.plot_bgcolor = "#ffffff";
  next.margin = { l: 50, r: 30, t: 70, b: 50, ...(next.margin || {}) };
  next.font = { family: "'DM Sans', Arial, sans-serif", size: 13, ...(next.font || {}) };
  if (next.showlegend === undefined) {
    next.showlegend = true;
  }
  return next;
}

/**
 * @param {HTMLSelectElement} select
 * @param {string} currentFile - "index.html" or "v5.html"
 */
function populateVizDropdown(select, currentFile) {
  if (!select) return;
  const labels = window.VIZ_PAGE_LABELS || [];
  const baseOptions = [
    { value: "index.html", label: "Home — gallery" },
    ...Array.from({ length: VIZ_COUNT }, (_, i) => {
      const n = i + 1;
      const short = labels[i] || `Visualization ${n}`;
      return { value: `v${n}.html`, label: `V${n} — ${short}` };
    }),
  ];

  select.innerHTML = "";
  for (const opt of baseOptions) {
    const el = document.createElement("option");
    el.value = opt.value;
    el.textContent = opt.label;
    if (opt.value === currentFile) {
      el.selected = true;
    }
    select.appendChild(el);
  }

  select.addEventListener("change", () => {
    if (select.value) {
      window.location.href = select.value;
    }
  });
}

/**
 * @param {string} plotElId
 * @param {number} oneBasedIndex - 1..VIZ_COUNT
 */
async function renderVizChart(plotElId, oneBasedIndex) {
  const el = document.getElementById(plotElId);
  if (!el) return;

  try {
    const specs = await loadSpecs();
    const charts = specs.charts || [];
    const chart = charts[oneBasedIndex - 1];
    if (!chart) {
      el.innerHTML = `<div class="viz-error">No chart data at index ${oneBasedIndex}. Re-export with <code>python3 scripts/export_plot_specs.py</code>.</div>`;
      return;
    }
    await Plotly.newPlot(plotElId, chart.data || [], cleanLayout(chart.layout), {
      responsive: true,
      displaylogo: false,
    });
  } catch (err) {
    el.innerHTML = `<div class="viz-error">${String(err.message || err)}</div>`;
    console.error(err);
  }
}

window.Site = {
  loadSpecs,
  cleanLayout,
  populateVizDropdown,
  renderVizChart,
  VIZ_COUNT,
};
