#!/usr/bin/env python3
"""
Generate index.html and v1.html … v12.html from a single theme list.
Run from repo root:  python3 scripts/generate_viz_pages.py
"""

from __future__ import annotations

from pathlib import Path

# Main page only — why the portfolio exists (no chart spoilers).
PROJECT_SIGNIFICANCE_PARAGRAPHS = [
    "For-hire vehicle trip records are more than receipts: they are a sensor on how a city moves, who it serves well, and where friction shows up as lost time, uneven access, or opaque earnings. This project treats TLC-style yellow cab data as a public-interest dataset—connecting raw trips to questions urban planners, operators, and policymakers routinely ask about peaks, equity, and cost.",
    "The significance is methodological as well as civic. By grounding each view in an explicit analytical question—temporal demand, distance and fare structure, tipping and payment behavior, congestion proxies, and geography—you can separate what you measure from what you find. The interactive charts let readers explore outcomes themselves; the narrative here stays focused on intent, stakes, and why each lens matters.",
    "Together, twelve complementary visualizations form a structured tour of urban mobility analytics: from rhythm-of-the-day problems to fairness and efficiency implications, without front-loading conclusions. Use the gallery to choose a question; use the chart on each page to see how the data answers it.",
]


def significance_section_html() -> str:
    paras = "\n".join(f"      <p>{p}</p>" for p in PROJECT_SIGNIFICANCE_PARAGRAPHS)
    return f"""
  <section class="home-significance">
    <div class="home-significance__inner">
      <h2>Why this project matters</h2>
{paras}
    </div>
  </section>"""


# Nav labels + gallery/detail copy: "analysis" frames the question and stakes only (no results).
VIZ = [
    {
        "n": 1,
        "label": "Peak pickup hours",
        "kicker": "Demand rhythm",
        "analysis": "Hourly demand shapes staffing, congestion policy, and expectations for when the street network is most stressed. This view uses pickup timestamps to ask how intensity varies across the clock—letting the data reveal peaks and troughs rather than naming them here.",
        "hero": "https://images.unsplash.com/photo-1518391846015-55a9cc003b25?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 2,
        "label": "Trip distance by hour",
        "kicker": "Distance patterns",
        "analysis": "Trip length is not constant over the day; commuters, nightlife, and airport patterns can all change the distribution of miles. Box plots by hour summarize median, spread, and outliers so you can compare shapes of distance at different times—without stating which hour wins.",
        "hero": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 3,
        "label": "Demand by weekday",
        "kicker": "Weekly pulse",
        "analysis": "Calendar structure (workweek vs weekend) affects transit complementary services and driver income stability. Aggregating pickups by weekday tests whether demand has a repeatable weekly signature—significant for scheduling and policy baselines, independent of which day is busiest.",
        "hero": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 4,
        "label": "Tips vs total fare",
        "kicker": "Rider generosity",
        "analysis": "Tips sit at the intersection of social norms, service quality perception, and how payments are recorded. A fare–tip scatter invites questions about proportionality, clustering at certain fare bands, and zeros that may reflect cash tips not logged—analytically important for driver livelihood discussions.",
        "hero": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 5,
        "label": "Fare vs trip distance",
        "kicker": "Fare structure",
        "analysis": "Metered fares should relate to distance in a principled way; surcharges, minimums, and long-haul behavior show up in log–log space. This plot examines the structural relationship between miles and dollars so readers can judge linearity, floors, and anomalies for themselves.",
        "hero": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 6,
        "label": "Duration vs traffic",
        "kicker": "Congestion",
        "analysis": "Trip duration is a direct congestion signal once distance is held in mind. Labeling trips by a simple rush vs off-peak scheme (from pickup time) asks whether time-in-traffic distributions widen or shift—a policy-relevant comparison we do not pre-empt with numeric conclusions.",
        "hero": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 7,
        "label": "Tips vs distance density",
        "kicker": "Heat of the grid",
        "analysis": "Two-dimensional density links how far people travel with how much they tip, surfacing where probability mass lives in the fare ecosystem. It is useful for discussing short-hop dominance versus long-run tails without spelling out where the brightest cells fall.",
        "hero": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 8,
        "label": "Pickup hotspots",
        "kicker": "On the map",
        "analysis": "Geography tests whether opportunity concentrates in a core or spreads across neighborhoods—central to service equity and infrastructure investment. Mapping pickups encodes spatial demand without narrating which blocks lead the distribution; interpretation stays with the reader.",
        "hero": "https://images.unsplash.com/photo-1514565131-fce0801e5785?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 9,
        "label": "Fare vs traffic status",
        "kicker": "Peak pricing",
        "analysis": "Empirical CDFs compare entire fare distributions under different traffic regimes, not just averages. That supports questions about whether congestion periods shift the whole payment experience (tails included)—a richer policy lens than a single summary statistic.",
        "hero": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 10,
        "label": "Fleet speed by day",
        "kicker": "Throughput",
        "analysis": "Implied speed from distance and duration operationalizes how fluidly traffic is moving when taxis are working. Histograms by weekday ask whether the speed profile is stable or shifts with weekly rhythms—relevant to congestion narratives without naming which day is slowest here.",
        "hero": "https://images.unsplash.com/photo-1489824904134-891ab64532f1?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 11,
        "label": "Tips by payment type",
        "kicker": "Cash vs card",
        "analysis": "Payment channel may correlate with how tips are suggested, recorded, or rounded. Comparing tip behavior across payment types helps separate cultural norms from data artifacts—significant for fairness and regulation—without asserting which mode yields higher tips on this page.",
        "hero": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=2000&q=80",
    },
    {
        "n": 12,
        "label": "Passengers per trip",
        "kicker": "Fleet utilization",
        "analysis": "Reported passenger counts encode whether rides are overwhelmingly single-occupancy or occasionally shared—information relevant to capacity planning, emissions per rider, and how TLC records differ from curb reality. Histogramming the field tests the shape of that distribution without stating the modal group here.",
        "hero": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&w=2000&q=80",
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
        <p class="viz-card-analysis">{v['analysis']}</p>
      </div>
    </a>"""
        )

    body = f"""
{HEAD_COMMON.format(title="NYC Taxi Analytics — Gallery")}
{nav("index.html")}
  <section class="home-hero" style="background-image: url('https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=2000&q=80');">
    <div class="home-hero__inner">
      <h1>Urban mobility, visualized</h1>
      <p>Twelve analytical lenses on NYC for-hire trip data—each with its own page, hero art, and interactive chart. Below, learn why the work matters and what each visualization is designed to explore (without spoiling what the figures show).</p>
    </div>
  </section>
{significance_section_html()}
  <section class="home-intro">
    <h2>Explore the gallery</h2>
    <p>Each card states the <strong>analytical purpose</strong> of that view—questions, methods, and real-world stakes—not the empirical outcome (that is for the chart). Open a page from the grid or use the <strong>Go to</strong> menu. Charts are loaded from <code>plot-specs.json</code>; after re-running your notebook, refresh specs with <code>python3 scripts/export_plot_specs.py</code>.</p>
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
      <p>{v['analysis']}</p>
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
