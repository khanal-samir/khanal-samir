#!/usr/bin/env python3
"""Run with Python 3 + Pillow before publishing profile changes."""
import json
from pathlib import Path
import re
import runpy
import xml.etree.ElementTree as ET

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
readme = (ROOT / "README.md").read_text()
for asset in set(re.findall(r"assets/[\w.-]+", readme)):
    assert (ROOT / asset).is_file(), f"Missing asset: {asset}"

sources = json.loads((ROOT / "assets/icon-sources.json").read_text())
assert {"openai", "anthropic", "jest", "mastra", "cursor", "opencode", "pi"} <= sources.keys()
for slug in sources:
    badge = ET.parse(ROOT / "assets" / f"{slug}.svg").getroot()
    assert badge.attrib["height"] == "40"
    icon = next(child for child in badge if child.tag.endswith("svg"))
    assert "viewBox" in icon.attrib, f"Unscaled icon: {slug}"
    assert not any(element.tag.split("}")[-1] in {"script", "foreignObject"} for element in badge.iter())

for theme in ("dark", "light"):
    with Image.open(ROOT / "assets" / f"hero-{theme}.gif") as banner:
        assert banner.size == (1200, 420)
        assert banner.n_frames > 1
        assert "loop" not in banner.info, "Banner should play once"
    assert (ROOT / "assets" / f"hero-{theme}.gif").stat().st_size < 500_000

assert readme.count("<details") == readme.count("</details>")
assert readme.count("<!-- BLOG-START -->") == readme.count("<!-- BLOG-END -->") == 1
writing = runpy.run_path(str(ROOT / "scripts/update-writing.py"))
links = writing["latest_links"]([{"title": "Hello [world]\n*again*", "url": "https://dev.to/example/post"}])
assert "Hello \\[world\\] \\*again\\*" in links
try:
    writing["latest_links"]([{"title": "Unsafe", "url": "javascript:alert(1)"}])
except ValueError:
    pass
else:
    raise AssertionError("Unsafe article URL accepted")
print(f"OK: {len(sources)} icons, README asset references, both animations, and writing update checks.")
