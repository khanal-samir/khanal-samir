#!/usr/bin/env python3
"""Validate the profile's vector graphics and README using Python 3."""
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
readme = (ROOT / "README.md").read_text()
references = set(re.findall(r"assets/[\w.-]+", readme))
for asset in references:
    assert (ROOT / asset).is_file(), f"Missing asset: {asset}"
    assert asset.endswith(".svg"), f"Expected vector asset: {asset}"

sources = json.loads((ROOT / "assets/icon-sources.json").read_text())
assert {"openai", "anthropic", "jest", "mastra", "cursor", "opencode", "pi", "email", "portfolio"} <= sources.keys()
for slug in sources:
    badge = ET.parse(ROOT / "assets" / f"{slug}.svg").getroot()
    assert badge.attrib["height"] == "38"
    icon = next(child for child in badge if child.tag.endswith("svg"))
    assert "viewBox" in icon.attrib, f"Unscaled icon: {slug}"
    assert icon.attrib["width"] == icon.attrib["height"] == "18"
    text = next(child for child in badge if child.tag.endswith("text"))
    assert text.attrib["font-size"] == "18"
    if slug in {"email", "portfolio"}:
        assert icon.attrib["fill"] == "none", "Outline icons must not be filled"

for filename in ("hero-dark.svg", "hero-still.svg"):
    path = ROOT / "assets" / filename
    banner = ET.parse(path).getroot()
    assert banner.attrib["viewBox"] == "0 0 1200 320"
    elements = list(banner)
    assert any(element.tag.endswith("rect") and element.attrib.get("fill") == "#0D1117" for element in elements)
    name = next(element for element in elements if element.text == "Samir Khanal" and element.tag.endswith("text"))
    assert name.attrib["font-size"] == "104"
    assert sum(element.tag.endswith("svg") for element in banner.iter()) == 4, "Expected three embedded SVG logos"
    assert path.stat().st_size < 20_000
    assert not any(element.tag.split("}")[-1] in {"script", "foreignObject", "image"} for element in banner.iter())

animated = (ROOT / "assets/hero-dark.svg").read_text()
assert "@keyframes signal" in animated and "@keyframes spin" in animated
assert "prefers-reduced-motion: reduce" in animated
assert "<style>" not in (ROOT / "assets/hero-still.svg").read_text()
assert "prefers-reduced-motion: reduce" in readme and "prefers-color-scheme" not in readme
assert "mailto:khanalsamirwork@gmail.com" in readme
assert "Software Developer · Computer Science Student · Nepal" in readme
assert "Building scalable web applications with a focus on JS/TS architecture." in readme
assert "Open to collaborating on interesting web applications." in readme
assert "<details" not in readme and "BLOG-START" not in readme
assert not (ROOT / ".github/workflows/writing.yml").exists()
print(f"OK: {len(sources)} compact SVG badges, dark animated SVG, reduced-motion fallback, and original bio.")
