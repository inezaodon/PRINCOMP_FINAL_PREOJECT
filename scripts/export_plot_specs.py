#!/usr/bin/env python3
"""
Extract Plotly figure specs from Jupyter notebook display outputs and write
plot-specs.json for the static dashboard (one spec per chart, order matches v1…v11).

Usage:
  python3 scripts/export_plot_specs.py
  python3 scripts/export_plot_specs.py --notebook Personal_Project_Code_~_Odon.ipynb --output plot-specs.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def split_top_level_args(s: str) -> list[str]:
    args: list[str] = []
    cur: list[str] = []
    depth = 0
    in_str = False
    esc = False
    quote = '"'
    for ch in s:
        if in_str:
            cur.append(ch)
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                in_str = False
            continue
        if ch in ('"', "'"):
            in_str = True
            quote = ch
            cur.append(ch)
            continue
        if ch in "[{(":
            depth += 1
            cur.append(ch)
            continue
        if ch in "]})":
            depth -= 1
            cur.append(ch)
            continue
        if ch == "," and depth == 0:
            args.append("".join(cur).strip())
            cur = []
            continue
        cur.append(ch)
    tail = "".join(cur).strip()
    if tail:
        args.append(tail)
    return args


def extract_newplot_args(html: str) -> tuple[str, str] | None:
    key = "Plotly.newPlot("
    i = html.find(key)
    if i < 0:
        return None
    j = i + len(key)
    depth = 1
    in_str = False
    esc = False
    quote = '"'
    buf: list[str] = []
    while j < len(html):
        ch = html[j]
        if in_str:
            buf.append(ch)
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                in_str = False
            j += 1
            continue
        if ch in ('"', "'"):
            in_str = True
            quote = ch
            buf.append(ch)
            j += 1
            continue
        if ch == "(":
            depth += 1
            buf.append(ch)
            j += 1
            continue
        if ch == ")":
            depth -= 1
            if depth == 0:
                break
            buf.append(ch)
            j += 1
            continue
        buf.append(ch)
        j += 1
    arg_str = "".join(buf)
    args = split_top_level_args(arg_str)
    if len(args) < 3:
        return None
    return args[1], args[2]


def cell_title_from_source(src: str) -> str | None:
    marker = "title='"
    mi = src.find(marker)
    if mi == -1:
        return None
    mj = src.find("'", mi + len(marker))
    if mj == -1:
        return None
    return src[mi + len(marker) : mj]


def extract_charts_from_notebook(nb_path: Path, max_charts: int) -> list[dict]:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    specs: list[dict] = []

    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src_lines = cell.get("source", [])
        src = "".join(src_lines) if isinstance(src_lines, list) else str(src_lines)
        title = cell_title_from_source(src)

        for out in cell.get("outputs", []):
            if out.get("output_type") != "display_data":
                continue
            data = out.get("data", {})
            html_list = data.get("text/html")
            if not html_list:
                continue
            html = "".join(html_list) if isinstance(html_list, list) else str(html_list)
            extracted = extract_newplot_args(html)
            if not extracted:
                continue
            traces_json, layout_json = extracted
            try:
                traces = json.loads(traces_json)
                layout = json.loads(layout_json)
            except json.JSONDecodeError:
                continue
            chart_title = title or layout.get("title", {}).get("text") or "Taxi Visualization"
            specs.append({"title": chart_title, "data": traces, "layout": layout})
            break

        if len(specs) >= max_charts:
            break

    return specs[:max_charts]


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Plotly specs from notebook to plot-specs.json")
    root = Path(__file__).resolve().parent.parent
    parser.add_argument(
        "--notebook",
        type=Path,
        default=root / "Personal_Project_Code_~_Odon.ipynb",
        help="Path to the Jupyter notebook with Plotly display outputs",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "plot-specs.json",
        help="Output JSON path for the dashboard",
    )
    parser.add_argument(
        "--max-charts",
        type=int,
        default=12,
        help="Maximum number of charts to export (default: 12 for v1–v12)",
    )
    args = parser.parse_args()

    nb_path = args.notebook.resolve()
    if not nb_path.is_file():
        raise SystemExit(f"Notebook not found: {nb_path}")

    charts = extract_charts_from_notebook(nb_path, args.max_charts)
    out_path = args.output.resolve()
    out_path.write_text(json.dumps({"charts": charts}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(charts)} chart(s) to {out_path}")


if __name__ == "__main__":
    main()
