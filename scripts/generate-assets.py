#!/usr/bin/env python3
"""Regenerate the profile's checked-in graphics (Python 3 + Pillow)."""
from concurrent.futures import ThreadPoolExecutor
from html import escape
from pathlib import Path
import json
import urllib.request
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
ET.register_namespace("", "http://www.w3.org/2000/svg")
SI = "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/"
DEV = "https://raw.githubusercontent.com/devicons/devicon/master/icons/"
LOBE = "https://raw.githubusercontent.com/lobehub/lobe-icons/master/packages/static-svg/icons/"
# Keep icon provenance beside the assets; brand marks belong to their owners.
TOOLS = {
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
    icon.attrib.update(x="12", y="10", width="20", height="20", fill=color)
    icon.attrib.pop("style", None)
    for element in icon.iter():
        for key, value in list(element.attrib.items()):
            if value == "currentColor":
                element.set(key, color)
        if element.tag.split("}")[-1] in {"script", "foreignObject"}:
            raise ValueError(f"Unsafe SVG: {slug}")
    width = 48 + len(label) * 8
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="40" viewBox="0 0 {width} 40" role="img" aria-label="{escape(label)}">
<title>{escape(label)}</title><rect x=".5" y=".5" width="{width-1}" height="39" rx="8" fill="#172435" stroke="#33465D"/>
{ET.tostring(icon, encoding="unicode")}
<text x="40" y="25" fill="#EDF2FA" font-family="Verdana,Arial,sans-serif" font-size="12">{escape(label)}</text></svg>'''
    (ASSETS / f"{slug}.svg").write_text(svg)


def banner(theme):
    dark = theme == "dark"
    bg, panel, ink, muted, accent = ("#101D2C", "#172435", "#EDF2FA", "#A8BACF", "#F2BD6B") if dark else ("#EAF1F8", "#FFFFFF", "#1D3047", "#526981", "#A45E17")
    font_dir = Path("/usr/share/fonts/truetype/firacode")
    regular = ImageFont.truetype(str(font_dir / "FiraCode-Regular.ttf"), 20)
    small = ImageFont.truetype(str(font_dir / "FiraCode-Regular.ttf"), 14)
    title = ImageFont.truetype(str(font_dir / "FiraCode-Bold.ttf"), 47)
    lines = ["$ whoami", "Software developer / CS student / Nepal", "$ building", "Web applications with JS/TS architecture."]
    frames = []
    for step in range(33):
        image = Image.new("RGB", (1200, 420), bg)
        d = ImageDraw.Draw(image)
        d.polygon([(735, 420), (883, 181), (933, 256), (1024, 101), (1200, 420)], fill="#223A53" if dark else "#D6E3EF")
        d.line([(745, 409), (883, 181), (933, 256), (1024, 101), (1190, 400)], fill="#486A88" if dark else "#9BB5CD", width=2)
        d.text((48, 25), "SAMIR KHANAL / DEVELOPER WORKSPACE", font=small, fill=muted)
        d.text((48, 61), "Code. Build. Iterate.", font=title, fill=ink)
        d.rounded_rectangle((48, 142, 870, 343), radius=14, fill=panel, outline="#33465D" if dark else "#C8D6E5", width=1)
        for i, c in enumerate(["#EF8C85", "#F2BD6B", "#79BCAA"]):
            d.ellipse((69 + i*19, 159, 78 + i*19, 168), fill=c)
        d.text((144, 154), "samir@nepal ~", font=small, fill=muted)
        for index, line in enumerate(lines):
            count = max(0, min(len(line), (step-index*7)*6))
            d.text((70, 191 + index*33), line[:count], font=regular, fill=accent if index % 2 == 0 else ink)
            if index*7 <= step < (index+1)*7:
                x = 70 + int(d.textlength(line[:count], font=regular))
                d.rectangle((x+3, 193 + index*33, x+12, 212 + index*33), fill=accent)
        d.text((48, 373), "EXPLORE THE STACK BELOW / OPEN THE PORTFOLIO FOR MORE", font=small, fill=muted)
        frames.append(image)
    frames[-1].save(ASSETS / f"hero-{theme}.png", optimize=True)
    # A shared palette keeps unchanged areas small across frames.
    palette = frames[-1].quantize(colors=64)
    frames = [frame.quantize(palette=palette, dither=0) for frame in frames]
    # Play once, then rest on the fully readable final frame. No flashing loop.
    frames[0].save(ASSETS / f"hero-{theme}.gif", save_all=True, append_images=frames[1:], duration=[100]*32+[8000], optimize=True)


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(badge, TOOLS.items()))
    (ASSETS / "icon-sources.json").write_text(json.dumps({slug: {"label": label, "source": url} for slug, (label, url, _) in TOOLS.items()}, indent=2) + "\n")
    for theme in ("dark", "light"):
        banner(theme)
    print(f"Generated {len(TOOLS)} branded badges and light/dark banners.")
