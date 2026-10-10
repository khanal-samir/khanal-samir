#!/usr/bin/env python3
"""Run with Python 3 + Pillow before publishing profile changes."""
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
readme = (ROOT / "README.md").read_text()
for asset in set(re.findall(r"assets/[\w.-]+", readme)):
    assert (ROOT / asset).is_file(), f"Missing asset: {asset}"

sources = json.loads((ROOT / "assets/icon-sources.json").read_text())
assert {"openai", "anthropic", "jest", "mastra", "cursor", "opencode", "pi", "email", "portfolio"} <= sources.keys()
for slug in sources:
    badge = ET.parse(ROOT / "assets" / f"{slug}.svg").getroot()
    assert badge.attrib["height"] == "40"
    icon = next(child for child in badge if child.tag.endswith("svg"))
    assert "viewBox" in icon.attrib, f"Unscaled icon: {slug}"
    assert not any(element.tag.split("}")[-1] in {"script", "foreignObject"} for element in badge.iter())
    if slug in {"email", "portfolio"}:
        assert icon.attrib["fill"] == "none", "Outline icons must not be filled"

for theme in ("dark", "light"):
    path = ROOT / "assets" / f"hero-{theme}.gif"
    with Image.open(path) as banner:
        assert banner.size == (1200, 300)
        assert banner.n_frames == 64
        assert banner.info["loop"] == 0, "Banner should loop seamlessly"
        first = banner.convert("RGB")
        banner.seek(32)
        middle = banner.convert("RGB")
        assert ImageChops.difference(first, middle).getbbox(), "Banner is not animated"
        # Keep the name legible and stationary throughout the animation.
        assert not ImageChops.difference(first.crop((48, 95, 700, 205)), middle.crop((48, 95, 700, 205))).getbbox()
    assert path.stat().st_size < 500_000

assert readme.count("prefers-reduced-motion: reduce") == 2
assert "mailto:khanalsamirwork@gmail.com" in readme
assert "Software Developer · Computer Science Student · Nepal" in readme
assert "Building scalable web applications with a focus on JS/TS architecture." in readme
assert "Open to collaborating on interesting web applications." in readme
assert "<details" not in readme and "BLOG-START" not in readme
assert not (ROOT / ".github/workflows/writing.yml").exists()
print(f"OK: {len(sources)} icons, contact badges, original bio, looping banners, and reduced-motion sources.")
