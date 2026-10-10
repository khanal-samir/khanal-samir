#!/usr/bin/env python3
"""Refresh the latest dev.to links; leave the README unchanged on API failure."""
import json
from pathlib import Path
import re
import urllib.request

README = Path(__file__).resolve().parents[1] / "README.md"
START, END = "<!-- BLOG-START -->", "<!-- BLOG-END -->"


def latest_links(articles):
    links = []
    for article in articles[:3]:
        url = article["url"]
        if not url.startswith("https://dev.to/"):
            raise ValueError("Unexpected article URL")
        title = re.sub(r"\s+", " ", article["title"])
        title = re.sub(r"([\\`*_{}\[\]<>()!|])", r"\\\1", title)
        links.append(f"- [{title}]({url})")
    links.append("\n[All posts on dev.to ↗](https://www.dev.to/khanalsamir) · [Hashnode ↗](https://samir-khanal.hashnode.dev)")
    return "\n".join(links)


if __name__ == "__main__":
    request = urllib.request.Request(
        "https://dev.to/api/articles?username=khanalsamir&per_page=3",
        headers={"User-Agent": "samir-profile", "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        articles = json.load(response)
    if articles:
        text = README.read_text()
        assert text.count(START) == text.count(END) == 1, "Missing or duplicate blog markers"
        before, rest = text.split(START)
        _, after = rest.split(END)
        README.write_text(before + START + "\n" + latest_links(articles) + "\n" + END + after)
    else:
        print("No public dev.to articles found; keeping the existing writing links.")
