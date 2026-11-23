#!/usr/bin/env python3
"""v1.2 think-cell-inspired atlas: structural and arithmetic checks (no external deps)."""
from pathlib import Path
import json
import math
import re
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "thinkcell" / "catalog.json"
ANNOT = ROOT / "thinkcell" / "annotations.json"
GALLERY = ROOT / "assets" / "thinkcell-chart-gallery.html"
FAILURES = []


def check(ok, message):
    if not ok:
        FAILURES.append(message)


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        FAILURES.append(f"{path.name} invalid: {exc}")
        return {}


def main():
    c, a = load(CATALOG), load(ANNOT)
    menu, variants, annotations = c.get("menu", []), c.get("variants", []), a.get("features", [])
    check(c.get("version") == "1.2.0", "catalog version")
    check(len(menu) == 16 and c.get("menu_count") == 16, "expected 16 insertion menu entries")
    check(len(variants) == 48 and c.get("variant_count") == 48, "expected 48 variants")
    check(len(annotations) == 19 and a.get("count") == 19, "expected 19 features")

    menu_ids = [v.get("id") for v in menu]
    variant_ids = [v.get("id") for v in variants]
    annot_ids = [v.get("id") for v in annotations]
    check(len(set(menu_ids)) == len(menu_ids), "duplicate menu id")
    check(len(set(variant_ids)) == len(variant_ids), "duplicate variant id")
    check(len(set(annot_ids)) == len(annot_ids), "duplicate feature id")
    check(not set(menu_ids).intersection(variant_ids), "duplicate menu/variant id")
    for m in menu:
        for key in ("id", "name_zh", "name_en", "family", "fields", "encoding", "risk", "source_url"):
            check(bool(m.get(key)), f"{m.get('id')} missing {key}")
        check(m.get("evidence") == "official-menu-or-product-icon", f"{m.get('id')} wrong evidence")
    for v in variants:
        check(v.get("parent_menu_id") in menu_ids, f"{v.get('id')} unknown parent")
        check(v.get("evidence") in ("documented-variant", "documented-application"), f"{v.get('id')} invalid origin")
        check(v.get("is_separate_insertion_button") is False, f"{v.get('id')} misleading separate menu flag")
        check(bool(v.get("fields")) and bool(v.get("rule")) and bool(v.get("source_url")), f"{v.get('id')} missing fields/rule/source")
    for a1 in annotations:
        check(a1.get("is_chart_type") is False, f"{a1.get('id')} must be an annotation, not chart type")
        check(bool(a1.get("rule")) and bool(a1.get("source_url")), f"{a1.get('id')} missing source/rule")

    unit = next((m for m in menu if m["id"] == "mekko-unit"), {})
    check("x_extent" in unit.get("fields", []), "Mekko unit axis must specify independent X extent")
    # Numerical regression tests for invariants stated in references.
    baseline, deltas, endpoint = 180, [42, -16, 25, -13], 218
    check(baseline + sum(deltas) == endpoint, "waterfall conservation")
    values = [[30, 20], [25, 25], [10, 40]]
    totals = [sum(row) for row in values]
    grand = sum(totals)
    for i, row in enumerate(values):
        for v in row:
            width, height = totals[i] / grand, v / totals[i]
            check(math.isclose(width * height, v / grand, abs_tol=1e-12), "percent-Mekko area invariance")
    check(math.isclose((160 ** .5) / (40 ** .5), 2), "bubble area/radius rule")
    check(math.isclose((121 / 100) ** (1 / 2) - 1, .1, abs_tol=1e-10), "CAGR test")
    check(date.fromisoformat("2026-12-08") >= date.fromisoformat("2026-12-02"), "Gantt date invariant")

    try:
        html = GALLERY.read_text(encoding="utf-8")
        for mid in menu_ids:
            check(('"'+mid+'"') in html, f"gallery missing chart {mid}")
        check('const DRAW=' in html, "SVG gallery missing renderer map")
        check('role="img"' in html, "SVG a11y label missing")
    except OSError as exc:
        FAILURES.append(f"SVG gallery missing: {exc}")
    for filename in ["thinkcell/README.md", "references/11-thinkcell-source-audit.md",
                     "references/12-thinkcell-web-engineering.md", "references/13-thinkcell-retail-recipes.md"]:
        check((ROOT / filename).is_file(), f"missing {filename}")

    if FAILURES:
        for failure in FAILURES:
            print("FAIL:", failure)
        raise SystemExit(1)
    print(f"PASS: {len(menu)} menu types, {len(variants)} variants, {len(annotations)} features, 16 SVG demos; arithmetic checks OK")


if __name__ == "__main__":
    main()
