#!/usr/bin/env python3
"""Regenerate the profile's checked-in graphics (Python 3 + Pillow)."""
from concurrent.futures import ThreadPoolExecutor
from html import escape
from pathlib import Path
import json
import math
import urllib.request
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFilter, ImageFont

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
    icon.attrib.update(x="12", y="10", width="20", height="20")
    icon.attrib.setdefault("fill", color)
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
    bg, ink, muted, ridge, accent = ("#101D2C", "#EDF2FA", "#A8BACF", "#35546D", "#7DD3E8") if dark else ("#EAF1F8", "#1D3047", "#526981", "#ABC2D4", "#247893")
    title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 78)
    small = ImageFont.truetype("/usr/share/fonts/truetype/firacode/FiraCode-Regular.ttf", 17)
    points = [(772, 236), (852, 144), (887, 175), (959, 88), (1024, 177), (1063, 133), (1150, 236)]
    lengths = [math.dist(a, b) for a, b in zip(points, points[1:])]
    frames = []
    for step in range(64):
        phase = (1 - math.cos(2 * math.pi * step / 64)) / 2
        image = Image.new("RGB", (1200, 300), bg)
        d = ImageDraw.Draw(image)
        for x in range(778, 1170, 24):
            for y in range(44, 274, 24):
                d.point((x, y), fill=ridge)
        for offset in (18, 36):
            d.line([(x, y + offset) for x, y in points], fill=ridge, width=1)
        d.line(points, fill=ridge, width=2)
        remaining = phase * sum(lengths)
        trail = [points[0]]
        for a, b, length in zip(points, points[1:], lengths):
            if remaining >= length:
                trail.append(b)
                remaining -= length
            else:
                fraction = remaining / length
                trail.append((a[0] + (b[0]-a[0])*fraction, a[1] + (b[1]-a[1])*fraction))
                break
        d.line(trail, fill=accent, width=3)
        x, y = trail[-1]
        glow = Image.new("RGB", image.size, bg)
        gd = ImageDraw.Draw(glow)
        gd.ellipse((x-11, y-11, x+11, y+11), fill=accent)
        image = Image.blend(image, glow.filter(ImageFilter.GaussianBlur(12)), .15)
        d = ImageDraw.Draw(image)
        d.ellipse((x-4, y-4, x+4, y+4), fill=accent)
        d.text((54, 54), "NEPAL  /  JAVASCRIPT + TYPESCRIPT", font=small, fill=muted)
        d.text((48, 99), "Samir Khanal", font=title, fill=ink)
        d.line((54, 222, 677, 222), fill=ridge, width=1)
        # The underline and ridge move together; the name never disappears.
        start = 54 + int(phase * 553)
        d.line((start, 222, start+70, 222), fill="#F2BD6B" if dark else "#A45E17", width=3)
        frames.append(image)
    frames[32].save(ASSETS / f"hero-{theme}.png", optimize=True)
    palette = frames[32].quantize(colors=96)
    frames = [frame.quantize(palette=palette, dither=0) for frame in frames]
    frames[0].save(ASSETS / f"hero-{theme}.gif", save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=True)


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(badge, TOOLS.items()))
    (ASSETS / "icon-sources.json").write_text(json.dumps({slug: {"label": label, "source": url} for slug, (label, url, _) in TOOLS.items()}, indent=2) + "\n")
    for theme in ("dark", "light"):
        banner(theme)
    print(f"Generated {len(TOOLS)} branded badges and light/dark banners.")
