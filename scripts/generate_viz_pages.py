#!/usr/bin/env python3
"""
Generate index.html and v1.html … v11.html from a single theme list.
Run from repo root:  python3 scripts/generate_viz_pages.py
"""

from __future__ import annotations

from pathlib import Path

# Short labels for nav + cards (match your analysis storyline)
VIZ = [
    {
        "n": 1,
        "label": "Peak pickup hours",
        "kicker": "Demand rhythm",
        "blurb": "When does the city call for cabs? Hourly pulse of pickups across NYC.",
        "hero": "https://images.unsplash.com/photo-1518391846015-55a9cc003b25?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 2,
        "label": "Trip distance by hour",
        "kicker": "Distance patterns",
        "blurb": "How trip length shifts from rush hour to late night — box-plot story of the clock.",
        "hero": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 3,
        "label": "Demand by weekday",
        "kicker": "Weekly pulse",
        "blurb": "Which days drive the most rides — workweek vs weekend energy.",
        "hero": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 4,
        "label": "Tips vs total fare",
        "kicker": "Rider generosity",
        "blurb": "Scatter of gratitude — how tips scale with the meter.",
        "hero": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 5,
        "label": "Fare vs trip distance",
        "kicker": "Fare structure",
        "blurb": "Distance and dollars on log scale — the shape of pricing.",
        "hero": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 6,
        "label": "Duration vs traffic",
        "kicker": "Congestion",
        "blurb": "Rush hour vs off-peak — how long trips really take.",
        "hero": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 7,
        "label": "Tips vs distance density",
        "kicker": "Heat of the grid",
        "blurb": "Where tips and miles stack up — 2D density of short hops and big fares.",
        "hero": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 8,
        "label": "Pickup hotspots",
        "kicker": "On the map",
        "blurb": "Spatial story — Manhattan glow and borough shadows.",
        "hero": "https://images.unsplash.com/photo-1514565131-fce0801e5785?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 9,
        "label": "Fare vs traffic status",
        "kicker": "Peak pricing",
        "blurb": "ECDF lens on rush vs crawl — who pays more at the margin.",
        "hero": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 10,
        "label": "Fleet speed by day",
        "kicker": "Throughput",
        "blurb": "Histogram of MPH — congestion measured as motion.",
        "hero": "https://images.unsplash.com/photo-1489824904134-891ab64532f1?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 11,
        "label": "Tips by payment type",
        "kicker": "Cash vs card",
        "blurb": "How tipping behavior shifts when the trip is settled different ways.",
        "hero": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=2000&q=80",
    },
]

HEAD_COMMON = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,600;0,9..40,800;1,9..40,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/site.css">
</head>
"""


def nav(current_file: str) -> str:
    return f"""
<body data-current-file="{current_file}">
  <nav class="site-nav">
    <a class="site-nav__brand" href="index.html">
      <span class="site-nav__logo" aria-hidden="true">🚕</span>
      <span>NYC Taxi Analytics</span>
    </a>
    <div class="site-nav__controls">
      <label for="viz-jump">Go to</label>
      <select id="viz-jump" aria-label="Jump to visualization"></select>
    </div>
  </nav>
"""


def script_labels() -> str:
    labels_js = ", ".join(json_escape(v["label"]) for v in VIZ)
    return f"""
  <script>
    window.VIZ_PAGE_LABELS = [{labels_js}];
  </script>"""


def script_init_nav() -> str:
    return """
  <script src="js/site.js"></script>
  <script>
    document.addEventListener("DOMContentLoaded", function () {
      Site.populateVizDropdown(
        document.getElementById("viz-jump"),
        document.body.getAttribute("data-current-file") || "index.html"
      );
    });
  </script>"""


def scripts_gallery() -> str:
    """Gallery home: no Plotly (fast first paint)."""
    return script_labels() + script_init_nav()


def scripts_viz_page(chart_num: int) -> str:
    """Visualization page: Plotly + chart mount."""
    return (
        script_labels()
        + """
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
"""
        + script_init_nav()
        + f"""
  <script>
    document.addEventListener("DOMContentLoaded", function () {{
      Site.renderVizChart("plot-main", {chart_num});
    }});
  </script>"""
    )


def json_escape(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_index(root: Path) -> None:
    cards = []
    for v in VIZ:
        cards.append(
            f"""
    <a class="viz-card-link" href="v{v['n']}.html">
      <div class="viz-card-link__img" style="background-image: url('{v['hero']}');" role="img" aria-label=""></div>
      <div class="viz-card-link__body">
        <div class="viz-card-link__tag">Visualization {v['n']}</div>
        <h3>{v['label']}</h3>
        <p>{v['blurb']}</p>
      </div>
    </a>"""
        )

    body = f"""
{HEAD_COMMON.format(title="NYC Taxi Analytics — Gallery")}
{nav("index.html")}
  <section class="home-hero" style="background-image: url('https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=2000&q=80');">
    <div class="home-hero__inner">
      <h1>Urban mobility, visualized</h1>
      <p>Eleven interactive chapters on yellow cab demand, fairness, congestion, and geography — each with its own cinematic hero and live Plotly chart.</p>
    </div>
  </section>
  <section class="home-intro">
    <h2>Choose a story</h2>
    <p>Open any card below or use the navigation dropdown on every page to jump between visualizations. Charts load from <code>plot-specs.json</code> (regenerate after notebook runs with <code>python3 scripts/export_plot_specs.py</code>).</p>
  </section>
  <div class="gallery">
    {"".join(cards)}
  </div>
  <footer class="site-footer">
    <p>NYC TLC-inspired student project · Images via Unsplash</p>
  </footer>
{scripts_gallery()}
</body>
</html>
"""
    (root / "index.html").write_text(body.strip() + "\n", encoding="utf-8")


def write_viz_page(root: Path, v: dict, prev_n: int | None, next_n: int | None) -> None:
    n = v["n"]
    prev_link = f'<a href="v{prev_n}.html">← V{prev_n}</a>' if prev_n else '<a href="index.html">← Gallery</a>'
    next_link = f'<a href="v{next_n}.html">V{next_n} →</a>' if next_n else '<span></span>'

    body = f"""
{HEAD_COMMON.format(title=f"V{n}: {v['label']} | NYC Taxi Analytics")}
{nav(f"v{n}.html")}
  <section class="viz-hero" style="background-image: url('{v['hero']}');">
    <div class="viz-hero__inner">
      <div class="viz-hero__kicker">{v['kicker']}</div>
      <h1>V{n}: {v['label']}</h1>
      <p>{v['blurb']}</p>
    </div>
  </section>
  <main class="viz-main">
    <div class="viz-panel">
      <h2>Interactive chart</h2>
      <p class="viz-caption">Pan, zoom, and hover — powered by Plotly in your browser.</p>
      <div id="plot-main" class="plot-container"></div>
    </div>
    <div class="viz-prev-next">
      {prev_link}
      {next_link}
    </div>
  </main>
  <footer class="site-footer">
    <p><a href="index.html">Back to gallery</a> · NYC TLC-inspired project</p>
  </footer>
{scripts_viz_page(n)}
</body>
</html>
"""
    (root / f"v{n}.html").write_text(body.strip() + "\n", encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    write_index(root)
    for i, v in enumerate(VIZ):
        prev_n = VIZ[i - 1]["n"] if i > 0 else None
        next_n = VIZ[i + 1]["n"] if i + 1 < len(VIZ) else None
        write_viz_page(root, v, prev_n, next_n)
    print(f"Wrote index.html and v1.html–v{len(VIZ)}.html → {root}")


if __name__ == "__main__":
    main()
