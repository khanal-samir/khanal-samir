#!/usr/bin/env python3
"""Draw assets/contributions.svg (contribution heatmap + consistency stats).

Usage:
  GH_TOKEN=... GH_USER=khanal-samir python scripts/update_contributions.py   # real data
  python scripts/update_contributions.py --empty -o assets/contributions.svg   # placeholder
  python scripts/update_contributions.py --sample -o /tmp/preview.svg          # fake data, preview only

No third-party packages needed. Counts are public contributions unless the token
can read private ones (use a PAT with read:user and "include private contributions" enabled).
"""
import argparse, datetime as dt, json, os, random, urllib.request
from html import escape as E

FONT = "Inter,'Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"
LEVELS = ["#18181b", "#0e4429", "#006d32", "#26a641", "#39d353"]
QUERY = ("query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{"
         "totalContributions weeks{contributionDays{date contributionCount weekday}}}}}}")


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "contributions-graph"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("errors"):
        raise SystemExit(f"GitHub API error: {data['errors']}")
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return [[(d["date"], d["contributionCount"], d["weekday"]) for d in w["contributionDays"]] for w in cal["weeks"]]


def blank_weeks(sample):
    today = dt.date.today()
    start = today - dt.timedelta(days=364)
    start -= dt.timedelta(days=(start.weekday() + 1) % 7)  # back to Sunday
    rnd = random.Random(3)
    weeks, d = [], start
    while d <= today:
        week = []
        for _ in range(7):
            if d <= today:
                wd = (d.weekday() + 1) % 7
                n = 0
                if sample:
                    gap = 150 < (d - start).days < 175
                    if not gap and rnd.random() < (0.78 if 0 < wd < 6 else 0.3):
                        n = rnd.choice([1, 2, 3, 4, 6, 8, 11, 15])
                week.append((d.isoformat(), n, wd))
            d += dt.timedelta(days=1)
        weeks.append(week)
    return weeks


def stats(weeks):
    days = [x for w in weeks for x in w]
    counts = [c for _, c, _ in days]
    cur, i = 0, len(counts) - 1
    if i >= 0 and counts[i] == 0:
        i -= 1  # today may not have a contribution yet
    while i >= 0 and counts[i] > 0:
        cur += 1
        i -= 1
    best = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0
        best = max(best, run)
    return sum(counts), cur, best, sum(1 for c in counts if c > 0)


def level(c, mx):
    if c <= 0 or mx <= 0:
        return 0
    q = c / mx
    return 1 if q <= .25 else 2 if q <= .5 else 3 if q <= .75 else 4


def build(weeks, empty=False, sample=False):
    total, cur, best, active = stats(weeks)
    mx = max((c for w in weeks for _, c, _ in w), default=0)
    W, H, X0, Y0, P = 880, 300, 60, 168, 15
    tiles = [("Contributions", total, ""), ("Current streak", cur, "days"), ("Longest streak", best, "days"), ("Active days", active, "")]
    t = ""
    for i, (k, v, u) in enumerate(tiles):
        x = 28 + i * 208
        val = "-" if empty else f"{v:,}"
        unit = f'<tspan font-size="13" font-weight="500" fill="#71717a" dx="6" letter-spacing="0">{u}</tspan>' if u and not empty else ""
        t += f'<text x="{x}" y="76" font-size="12" fill="#71717a">{k}</text><text x="{x}" y="108" font-size="28" font-weight="600" letter-spacing="-1" fill="#fafafa">{val}{unit}</text>'
    for r, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        t += f'<text x="28" y="{Y0 + r * P + 10}" font-size="10.5" fill="#71717a">{lab}</text>'
    cols, last_m, last_x = "", None, -99
    for c, week in enumerate(weeks):
        first = dt.date.fromisoformat(week[0][0])
        if first.month != last_m and c - last_x >= 3 and (c > 0 or len(weeks) > 3):
            t += f'<text x="{X0 + c * P}" y="{Y0 - 10}" font-size="10.5" fill="#71717a">{first.strftime("%b")}</text>'
            last_x = c
        last_m = first.month
        cells = "".join(
            f'<rect x="{X0 + c * P}" y="{Y0 + wd * P}" width="12" height="12" rx="2.5" fill="{LEVELS[level(n, mx)]}"/>'
            for _, n, wd in week)
        cols += f'<g class="c" style="animation-delay:{c * .012:.3f}s">{cells}</g>'
    lx = W - 28 - (5 * P + 62)
    legend = f'<text x="{lx}" y="{H - 16}" font-size="10.5" fill="#71717a">Less</text>' + "".join(
        f'<rect x="{lx + 28 + i * P}" y="{H - 26}" width="12" height="12" rx="2.5" fill="{LEVELS[i]}"/>' for i in range(5)
    ) + f'<text x="{lx + 28 + 5 * P + 3}" y="{H - 16}" font-size="10.5" fill="#71717a">More</text>'
    right = "Syncing - updates daily" if empty else "Last 12 months"
    desc = ("Contribution graph. Data syncs daily." if empty else
            f"{total} contributions in the last year, current streak {cur} days, longest streak {best} days, {active} active days.")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">GitHub contributions</title><desc id="d">{E(desc)}</desc>
<style>text{{font-family:{FONT}}}.c{{animation:f .5s ease-out backwards}}@keyframes f{{from{{opacity:0}}}}.in{{animation:in .8s cubic-bezier(.16,1,.3,1) backwards}}@keyframes in{{from{{opacity:0;transform:translateY(10px)}}}}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<g class="in"><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="#09090b" stroke="#27272a"/>
<text x="28" y="34" font-size="13" font-weight="600" fill="#fafafa">Contributions</text><text x="{W - 28}" y="34" font-size="12" fill="#71717a" text-anchor="end">{right}</text>
<line x1="0" x2="{W}" y1="48" y2="48" stroke="#27272a"/>{t}<line x1="28" x2="{W - 28}" y1="128" y2="128" stroke="#18181b"/></g>
{cols}{legend}</svg>'''


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="assets/contributions.svg")
    ap.add_argument("--sample", action="store_true")
    ap.add_argument("--empty", action="store_true")
    a = ap.parse_args()
    if a.sample or a.empty:
        weeks = blank_weeks(a.sample)
    else:
        weeks = fetch(os.environ["GH_USER"], os.environ["GH_TOKEN"])
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(build(weeks, empty=a.empty, sample=a.sample))
    print("wrote", a.out)
