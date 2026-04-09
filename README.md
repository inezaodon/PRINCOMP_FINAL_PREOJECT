# NYC Taxi Analytics

Static gallery and twelve visualization pages for NYC TLC–style yellow cab trip analysis. Each view has its own HTML page with a hero image and an interactive **Plotly** chart loaded from `plot-specs.json` (no server-side rendering).

## What’s in the repo

| Path | Role |
|------|------|
| `index.html` | Landing page with gallery and project framing |
| `v1.html`–`v12.html` | One page per visualization (chart + navigation) |
| `plot-specs.json` | Serialized Plotly traces and layouts for the browser |
| `css/site.css`, `js/site.js` | Shared layout, gallery, and chart mounting |
| `Personal_Project_Code_~_Odon.ipynb` | Analysis notebook; figures should be executed so outputs export cleanly |
| `scripts/export_plot_specs.py` | Reads notebook display outputs → writes `plot-specs.json` |
| `scripts/generate_viz_pages.py` | Regenerates `index.html` and `v1.html`–`v12.html` from a single theme list (titles, copy, Unsplash hero URLs) |

Hero images are hotlinked from [Unsplash](https://unsplash.com) with crop/quality parameters consistent across pages.

## View locally

From the repository root:

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000` and use `index.html` as the entry point. A simple static host avoids browser restrictions on `file://` and matches how the site is deployed (e.g. GitHub Pages or Vercel).

## Refresh charts after changing the notebook

1. Run the notebook cells so Plotly figures are displayed (the exporter looks for `Plotly.newPlot` in saved `display_data` HTML).
2. From the repo root:

```bash
python3 scripts/export_plot_specs.py
```

Optional flags:

```bash
python3 scripts/export_plot_specs.py --notebook Personal_Project_Code_~_Odon.ipynb --output plot-specs.json --max-charts 12
```

Commit the updated `plot-specs.json` when you want the live site to show the new figures.

## Regenerate HTML pages

If you edit visualization titles, analytical blurbs, or hero image URLs, change the `VIZ` list in `scripts/generate_viz_pages.py`, then run:

```bash
python3 scripts/generate_viz_pages.py
```

That overwrites `index.html` and `v1.html`–`v12.html` from that single source.

## Project context

This is a student project inspired by NYC TLC trip-level data: temporal demand, fare and tip behavior, congestion proxies, geography, and fleet utilization. The site copy is written to describe *what each view is for*, not to front-load empirical results—readers explore outcomes in the charts.
