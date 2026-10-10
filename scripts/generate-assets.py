#!/usr/bin/env python3
"""Regenerate the profile's self-contained SVG assets with Python 3."""
from concurrent.futures import ThreadPoolExecutor
from html import escape
from pathlib import Path
import json
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
ET.register_namespace("", "http://www.w3.org/2000/svg")
SI = "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/"
DEV = "https://raw.githubusercontent.com/devicons/devicon/master/icons/"
LOBE = "https://raw.githubusercontent.com/lobehub/lobe-icons/master/packages/static-svg/icons/"
LUCIDE = "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/"
# Keep icon provenance beside the assets; brand marks belong to their owners.
TOOLS = {
    "portfolio": ("samirkhanal.is-a.dev", LUCIDE + "globe.svg", "#7DD3E8"),
    "email": ("khanalsamirwork@gmail.com", LUCIDE + "mail.svg", "#F2BD6B"),
    "html5": ("HTML5", SI + "html5.svg", "#E34F26"),
    "css3": ("CSS3", DEV + "css3/css3-original.svg", "#1572B6"),
    "javascript": ("JavaScript", SI + "javascript.svg", "#F7DF1E"),
    "typescript": ("TypeScript", SI + "typescript.svg", "#3178C6"),
    "bash": ("Bash", SI + "gnubash.svg", "#89B991"),
    "react": ("React", SI + "react.svg", "#61DAFB"),
    "nextjs": ("Next.js", SI + "nextdotjs.svg", "#FFFFFF"),
    "tailwind": ("Tailwind CSS", SI + "tailwindcss.svg", "#38BDF8"),
    "redux": ("Redux", SI + "redux.svg", "#A78BFA"),
    "nodejs": ("Node.js", SI + "nodedotjs.svg", "#73C78D"),
    "express": ("Express", SI + "express.svg", "#FFFFFF"),
    "hono": ("Hono", SI + "hono.svg", "#E36002"),
    "nestjs": ("NestJS", SI + "nestjs.svg", "#E0234E"),
    "postgresql": ("PostgreSQL", SI + "postgresql.svg", "#78ACDB"),
    "mongodb": ("MongoDB", SI + "mongodb.svg", "#47A248"),
    "supabase": ("Supabase", SI + "supabase.svg", "#3ECF8E"),
    "appwrite": ("Appwrite", SI + "appwrite.svg", "#FD366E"),
    "convex": ("Convex", SI + "convex.svg", "#EE342F"),
    "vitest": ("Vitest", SI + "vitest.svg", "#A3C75C"),
    "jest": ("Jest", DEV + "jest/jest-plain.svg", "#C96B87"),
    "githubactions": ("GitHub Actions", SI + "githubactions.svg", "#58A6FF"),
    "docker": ("Docker", SI + "docker.svg", "#2496ED"),
    "aws": ("AWS", DEV + "amazonwebservices/amazonwebservices-original-wordmark.svg", "#FF9900"),
    "digitalocean": ("DigitalOcean", SI + "digitalocean.svg", "#0080FF"),
    "render": ("Render", SI + "render.svg", "#FFFFFF"),
    "git": ("Git", SI + "git.svg", "#F05032"),
    "figma": ("Figma", SI + "figma.svg", "#F24E1E"),
    "openai": ("OpenAI", LOBE + "openai.svg", "#FFFFFF"),
    "anthropic": ("Anthropic", SI + "anthropic.svg", "#D6AE91"),
    "mastra": ("Mastra", "https://mastra.ai/favicon/new-brand/icon.svg", "#FFFFFF"),
    "cursor": ("Cursor", SI + "cursor.svg", "#FFFFFF"),
    "opencode": ("OpenCode", "https://raw.githubusercontent.com/sst/opencode/dev/packages/ui/src/assets/favicon/favicon.svg", "#FFFFFF"),
    "pi": ("Pi", "https://pi.dev/logo-auto.svg", "#F1BE58"),
    "github": ("GitHub", SI + "github.svg", "#FFFFFF"),
    "linkedin": ("LinkedIn", DEV + "linkedin/linkedin-original.svg", "#0A66C2"),
    "x": ("X", SI + "x.svg", "#FFFFFF"),
    "devto": ("dev.to", SI + "devdotto.svg", "#FFFFFF"),
    "hashnode": ("Hashnode", SI + "hashnode.svg", "#7293FF"),
    "discord": ("Discord", SI + "discord.svg", "#8891F2"),
}


def badge(item):
    slug, (label, url, color) = item
    request = urllib.request.Request(url, headers={"User-Agent": "samir-profile-assets"})
    with urllib.request.urlopen(request, timeout=30) as response:
        icon = ET.fromstring(response.read())
    if "viewBox" not in icon.attrib:
        icon = next(child for child in icon if child.tag.endswith("svg") and "viewBox" in child.attrib)
    icon.attrib.update(x="14", y="11", width="26", height="26")
    icon.attrib.setdefault("fill", color)
    icon.attrib.pop("style", None)
    for element in icon.iter():
        for key, value in list(element.attrib.items()):
            if value == "currentColor":
                element.set(key, color)
            elif slug == "aws" and value.lower() == "#252f3e":
                element.set(key, "#F0F6FC")
            elif slug == "jest" and value.lower() == "#99425b":
                element.set(key, color)
        if element.tag.split("}")[-1] in {"script", "foreignObject"}:
            raise ValueError(f"Unsafe SVG: {slug}")
    width = 68 + len(label) * 11
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="48" viewBox="0 0 {width} 48" role="img" aria-label="{escape(label)}">
<title>{escape(label)}</title><rect x=".5" y=".5" width="{width-1}" height="47" rx="8" fill="#151B23" stroke="#303D4E"/>
{ET.tostring(icon, encoding="unicode")}
<text x="50" y="31" fill="#F0F6FC" font-family="Verdana,Arial,sans-serif" font-size="18">{escape(label)}</text></svg>'''
    (ASSETS / f"{slug}.svg").write_text(svg)


def banner():
    marks = []
    for slug, x, y, size in [("typescript", 892, 198, 56), ("react", 996, 66, 68), ("nodejs", 1078, 196, 60)]:
        badge_svg = ET.parse(ASSETS / f"{slug}.svg").getroot()
        icon = next(child for child in badge_svg if child.tag.endswith("svg"))
        icon.attrib.update(x=str(x), y=str(y), width=str(size), height=str(size))
        marks.append(f'<g class="{slug}-mark">{ET.tostring(icon, encoding="unicode")}</g>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-labelledby="title description">
<title id="title">Samir Khanal</title>
<desc id="description">Software developer in Nepal. Animated TypeScript, React and Node.js brand marks beside a large name.</desc>
<style>
  .signal {{ animation: signal 6s linear infinite; }}
  .react-mark {{ transform-box: fill-box; transform-origin: center; animation: spin 28s linear infinite; }}
  @keyframes signal {{ to {{ stroke-dashoffset: -128; }} }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  @media (prefers-reduced-motion: reduce) {{ .signal, .react-mark {{ animation: none; }} }}
</style>
<rect x="1" y="1" width="1198" height="318" rx="18" fill="#0D1117" stroke="#303D4E" stroke-width="2"/>
<text x="56" y="65" fill="#BAC5D3" font-family="Verdana,Arial,sans-serif" font-size="24">JavaScript / TypeScript</text>
<text x="50" y="172" fill="#F0F6FC" font-family="DejaVu Sans,Arial,sans-serif" font-size="104" font-weight="700" letter-spacing="-4">Samir Khanal</text>
<text x="56" y="227" fill="#BAC5D3" font-family="Verdana,Arial,sans-serif" font-size="28">Software Developer · Nepal</text>
<path d="M56 266H760" fill="none" stroke="#253142" stroke-width="2"/>
<path class="signal" d="M56 266H760" fill="none" stroke="#58A6FF" stroke-width="3" stroke-dasharray="14 50"/>
<path d="M920 226Q900 135 1030 100Q1144 128 1108 226Q1018 288 920 226Z" fill="none" stroke="#303D4E" stroke-width="2"/>
<path class="signal" d="M920 226Q900 135 1030 100Q1144 128 1108 226Q1018 288 920 226Z" fill="none" stroke="#58A6FF" stroke-width="2" stroke-dasharray="14 50"/>
<circle cx="920" cy="226" r="48" fill="#151B23" stroke="#303D4E" stroke-width="2"/>
<circle cx="1030" cy="100" r="54" fill="#151B23" stroke="#303D4E" stroke-width="2"/>
<circle cx="1108" cy="226" r="48" fill="#151B23" stroke="#303D4E" stroke-width="2"/>
{''.join(marks)}
</svg>'''
    (ASSETS / "hero-dark.svg").write_text(svg)
    # The static version stays dark too; no JavaScript or raster images needed.
    start = svg.index("<style>")
    end = svg.index("</style>", start) + len("</style>")
    (ASSETS / "hero-still.svg").write_text((svg[:start] + svg[end:]).replace("Animated TypeScript", "TypeScript"))


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(badge, TOOLS.items()))
    (ASSETS / "icon-sources.json").write_text(json.dumps({slug: {"label": label, "source": url} for slug, (label, url, _) in TOOLS.items()}, indent=2) + "\n")
    banner()
    print(f"Generated {len(TOOLS)} larger SVG badges and the dark SVG banner.")
