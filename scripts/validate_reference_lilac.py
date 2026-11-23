#!/usr/bin/env python3
"""Validate screenshot-grounded visual contract and original interactive SVG page."""
from __future__ import annotations

import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "design-languages/reference-lilac/manifest.json"
PATTERNS = ROOT / "patterns/observed-editorial-charts.json"
EXAMPLES = ROOT / "examples/reference-lilac-demo-data.json"
HTML = ROOT / "assets/reference-lilac-dashboard.html"
TEMPLATE = ROOT / "templates/google-ai-studio-interactive-dashboard/template.json"
REGISTRY = ROOT / "templates/registry.json"
FAILURES = []

def check(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)

class AuditHTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.svg_ids: set[str] = set()
        self.scripts: list[str] = []
        self.in_script = False
        self.buttons = []
    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if "id" in attr:
            check(attr["id"] not in self.ids, f"duplicate HTML ID {attr['id']}")
            self.ids.add(attr["id"])
            if tag == "svg":
                self.svg_ids.add(attr["id"])
        if tag == "button":
            self.buttons.append(attr)
        if tag == "script" and not attr.get("src"):
            self.in_script = True
    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
    def handle_data(self, data):
        if self.in_script:
            self.scripts.append(data)

def main() -> None:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    p = json.loads(PATTERNS.read_text(encoding="utf-8"))
    data = json.loads(EXAMPLES.read_text(encoding="utf-8"))
    tpl = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    html = HTML.read_text(encoding="utf-8")
    check(m.get("status") == "reviewed-screenshot", "manifest must identify screenshot evidence")
    check(m.get("online_source_verified") is False, "don't claim original website code was verified")
    check(tpl.get("evidence_status") == "reviewed-screenshot", "T001 should reflect screenshot evidence")
    check(tpl.get("visual_preset_default") == "design-languages/reference-lilac/manifest.json", "T001 default preset")
    check(reg.get("version") == "1.3.0", "registry version")
    check(reg["templates"][0]["id"] == "T001", "must preserve T001")
    check(reg["templates"][0]["evidence_status"] == "reviewed-screenshot", "registry screenshot evidence")
    check(set(["T002", "T003", "T004"]).issubset(set(reg.get("reserved_slots", []))), "future template slots")
    expected = {"unit-matrix", "diverging-likert", "stacked-column-scrollytelling", "paired-dumbbell"}
    pattern_ids = {x["id"] for x in p["patterns"]}
    check(pattern_ids == expected, "four distinct structural chart patterns")
    check(set(tpl.get("verified_original_patterns", [])) == expected, "T001 observed chart mapping")
    for item in p["patterns"]:
        check(item.get("provenance") == "reviewed-screenshot", f"{item['id']}: provenance")
        check(bool(item.get("geometry")) and bool(item.get("interaction")) and bool(item.get("validation")), f"{item['id']}: spec incomplete")
    colors = {
        "canvas": "#E8E6EF", "ink": "#121116", "violet": "#7C63FF",
        "red": "#E2492C", "magenta": "#C04BD9", "salmon": "#F2A391",
        "violetSoft": "#B9ABFB", "grid": "#CFCBD9"
    }
    for key, value in colors.items():
        check(m["palette"].get(key) == value, f"palette mismatch: {key}")
        check(value in html, f"HTML missing palette {value}")
    groups = data["unit_matrix"]["groups"]
    check(sum(g["n"] for g in groups) == 412, "unit matrix group sum")
    check(sum(g["n"] for g in groups) == data["unit_matrix"]["denominator"], "unit matrix denominator")
    check([g["n"] for g in groups] == [148, 121, 87, 56], "unit-matrix screenshot counts")
    for row in data["likert"]["rows"]:
        values = [row[key] for key in data["likert"]["bins"]]
        check(sum(values) == 100, f"Likert not 100%: {row['statement']}")
        negative = values[0] + values[1]
        neutral = values[2]
        positive = values[3] + values[4]
        check(negative + neutral / 2 + neutral / 2 + positive == 100, "Likert neutral split")
    stack = data["stacked"]
    totals = [sum(series["values"][i] for series in stack["series"]) for i in range(len(stack["years"]))]
    check(totals == stack["totals"], "stacked total does not match every year")
    check(totals[-1] == 1840, "estimated 2026 total should be 1,840")
    for d in data["dumbbell"]["rows"]:
        check(isinstance(d["before"], (int, float)) and isinstance(d["after"], (int, float)), "dumbbell numeric inputs")
        check(0 <= d["before"] <= 100 and 0 <= d["after"] <= 100, "dumbbell percent range")
    check(data["dumbbell"]["rows"][0]["after"] - data["dumbbell"]["rows"][0]["before"] == 31, "2024-2026 +31 pp")
    check(any(x["after"] < x["before"] for x in data["dumbbell"]["rows"]), "a negative dumbbell change is required")

    parser = AuditHTML()
    parser.feed(html)
    check(parser.svg_ids == {"unit-svg", "likert-svg", "stack-svg", "dumb-svg"}, "must have 4 independent SVG figures")
    check(all('aria-label' in attrs or 'aria-pressed' in attrs for attrs in parser.buttons), "button accessibility")
    check(len(parser.scripts) == 1, "expect a single standalone inline JS script")
    js = "\n".join(parser.scripts)
    for token in ["renderMatrix()", "renderLikert()", "renderStack()", "renderDumb()",
                  'patternTransform:"rotate(45)"', "bins[2]/2", "r[2]-r[1]",
                  'stackMode==="share"', 'selectedSeries.size===1',
                  'tabindex":0', "aria-label", "viewBox"]:
        check(token in js or token in html, f"missing required geometry / interaction code: {token}")

    # Check that the inline JS parses under the Node version available in GitHub Actions.
    proc = subprocess.run(["node", "--check", "-"], input=js, capture_output=True, text=True)
    check(proc.returncode == 0, "JavaScript syntax failed:\n" + proc.stderr)
    if FAILURES:
        for item in FAILURES:
            print("FAIL:", item)
        raise SystemExit(1)
    print("PASS: 4 screenshot-derived charts, 8 reference colors, 412 record squares, "
          "Likert center, stacked 1840, +/- pp, interactive SVG markup, JS syntax")

if __name__ == "__main__":
    main()
