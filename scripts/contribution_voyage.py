#!/usr/bin/env python3
"""Draw the contribution calendar as a sea chart: every contribution is a
treasure tile and a pirate ship sails the year plundering them one by one.

Usage: contribution_voyage.py [github_user] [output.svg]
Uses the GraphQL API when GITHUB_TOKEN is set, otherwise the public
contributions page. Standard library only.
"""
import datetime as dt
import json
import math
import os
import random
import re
import sys
import urllib.request

USER = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GH_USER", "sonyrp")
OUT = sys.argv[2] if len(sys.argv) > 2 else "dist/contribution-voyage.svg"
TOKEN = os.environ.get("GITHUB_TOKEN")

LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2,
          "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
TILE = {1: "#2a7fb8", 2: "#4fb3a5", 3: "#f4a261", 4: "#f4c430"}
CELL, PITCH, W = 14, 18, 1100
Y0 = 104


def fetch_graphql():
    query = """query($login:String!){user(login:$login){contributionsCollection{
      contributionCalendar{totalContributions weeks{contributionDays{
      date contributionLevel}}}}}}"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "User-Agent": "contribution-voyage"})
    with urllib.request.urlopen(req, timeout=30) as r:
        cal = json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [(dt.date.fromisoformat(d["date"]), LEVELS[d["contributionLevel"]])
            for w in cal["weeks"] for d in w["contributionDays"]]
    return days, cal["totalContributions"]


def fetch_html():
    req = urllib.request.Request(f"https://github.com/users/{USER}/contributions",
                                 headers={"User-Agent": "contribution-voyage"})
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8", "replace")
    days = []
    for tag in re.findall(r"<td[^>]*>", html):
        d = re.search(r'data-date="(\d{4}-\d\d-\d\d)"', tag)
        lv = re.search(r'data-level="(\d)"', tag)
        if d and lv:
            days.append((dt.date.fromisoformat(d.group(1)), int(lv.group(1))))
    m = re.search(r"([\d,]+)\s+contributions?\s+in", html)
    total = int(m.group(1).replace(",", "")) if m else sum(1 for _, lv in days if lv)
    return days, total


def build(days, total):
    days.sort()
    first = days[0][0]
    wd0 = (first.weekday() + 1) % 7                      # Sunday = row 0
    cells = [(((d - first).days + wd0) // 7, (d.weekday() + 1) % 7, d, lv) for d, lv in days]
    cols = max(c for c, *_ in cells) + 1
    grid_w = cols * PITCH - (PITCH - CELL)
    x0 = (W - grid_w) / 2
    H = Y0 + 7 * PITCH + 58
    mid_y = Y0 + 3 * PITCH + CELL / 2

    def center(c, r):
        return x0 + c * PITCH + CELL / 2, Y0 + r * PITCH + CELL / 2

    # Route: column by column, sweeping each column from the nearer end.
    pts, loot, y = [(x0 - 46, mid_y)], {}, mid_y
    for c in range(cols):
        rows = sorted(r for cc, r, _, lv in cells if cc == c and lv)
        if not rows:
            continue
        if abs(center(c, rows[-1])[1] - y) < abs(center(c, rows[0])[1] - y):
            rows.reverse()
        for r in rows:
            pts.append(center(c, r))
            loot[(c, r)] = len(pts) - 1
        y = pts[-1][1]
    pts.append((x0 + grid_w + 46, mid_y))
    dist = [0.0]
    for a, b in zip(pts, pts[1:]):
        dist.append(dist[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    length = dist[-1]
    T = round(max(18.0, length / 55), 1)

    rnd = random.Random(1997)
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    o.append(f"""<defs>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1d33"/><stop offset="1" stop-color="#0d2b4a"/></linearGradient>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<style>
text{{font-family:Georgia,'Times New Roman',serif}}
.loot{{animation:loot {T}s linear infinite}}
@keyframes loot{{0%,86%{{opacity:0}}94%,100%{{opacity:1}}}}
.x{{transform-box:fill-box;transform-origin:center;animation:pop {T}s linear infinite}}
@keyframes pop{{0%{{transform:scale(0)}}2%{{transform:scale(1.7)}}4%,100%{{transform:scale(1)}}}}
.tw{{animation:tw 4s ease-in-out infinite}}
@keyframes tw{{0%,100%{{opacity:1}}50%{{opacity:.45}}}}
.coin{{animation:coin 2.2s ease-in-out infinite}}
@keyframes coin{{0%,100%{{opacity:.25}}50%{{opacity:.95}}}}
.bob{{animation:bob 1.6s ease-in-out infinite}}
@keyframes bob{{0%,100%{{transform:rotate(-5deg)}}50%{{transform:rotate(5deg) translateY(-1.5px)}}}}
.wv{{animation:wv 8s linear infinite}}
@keyframes wv{{to{{transform:translateX(-200px)}}}}
</style></defs>""")
    o.append('<g clip-path="url(#frame)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#sea)"/>')
    wave = "q50 -10 100 0 " + "t100 0 " * 13
    o.append(f'<g class="wv"><path d="M0 {H - 12} {wave}V{H} H0 Z" fill="#12507f" opacity=".7"/></g>')

    o.append(f'<text x="{x0:.0f}" y="44" font-size="23" font-weight="700" fill="#f4c430" letter-spacing="3">THE GRAND LINE LOGBOOK</text>')
    o.append(f'<text x="{x0:.0f}" y="65" font-size="13" font-style="italic" fill="#f1dfb5">every contribution is a treasure, and my ship plunders them all</text>')
    o.append(f'<text x="{x0 + grid_w:.0f}" y="48" text-anchor="end" font-size="19" font-weight="700" fill="#f1dfb5">'
             f'<tspan fill="#f4c430">{total:,}</tspan> treasures in the last year</text>')

    # month labels
    last_month, last_col = None, -9
    for c in range(cols):
        top = min((d for cc, _, d, _ in cells if cc == c), default=None)
        if top and top.month != last_month:
            if c - last_col >= 3:
                o.append(f'<text x="{x0 + c * PITCH:.0f}" y="{Y0 - 9}" font-size="11" fill="#9fb3c8" letter-spacing="1">{top.strftime("%b").upper()}</text>')
                last_col = c
            last_month = top.month

    # tiles
    for c, r, d, lv in cells:
        x, y = x0 + c * PITCH, Y0 + r * PITCH
        if not lv:
            tw = f' class="tw" style="animation-delay:{rnd.uniform(0, 4):.1f}s"' if rnd.random() < .12 else ""
            o.append(f'<rect{tw} x="{x:.1f}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="#12355b"/>')
            continue
        delay = f"{T * dist[loot[(c, r)]] / length:.2f}s"
        cx, cy = x + CELL / 2, y + CELL / 2
        shine = (f'<circle class="coin" cx="{cx:.1f}" cy="{cy}" r="3" fill="#fff8e1" style="animation-delay:{rnd.uniform(0, 2):.1f}s"/>'
                 if lv >= 3 else "")
        o.append(
            f'<rect x="{x:.1f}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="#0e2a47"/>'
            f'<path class="x" style="animation-delay:{delay}" d="M{cx - 3.5:.1f} {cy - 3.5}l7 7m0 -7l-7 7" stroke="#e63946" stroke-width="2" stroke-linecap="round"/>'
            f'<g class="loot" style="animation-delay:{delay}"><rect x="{x:.1f}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{TILE[lv]}"/>{shine}</g>')

    # legend
    lx, ly = x0 + grid_w - 5 * PITCH - 62, Y0 + 7 * PITCH + 12
    o.append(f'<text x="{lx - 8:.0f}" y="{ly + 11}" text-anchor="end" font-size="11" font-style="italic" fill="#9fb3c8">calm sea</text>')
    for i, col in enumerate(["#12355b", TILE[1], TILE[2], TILE[3], TILE[4]]):
        o.append(f'<rect x="{lx + i * PITCH:.1f}" y="{ly}" width="{CELL}" height="{CELL}" rx="3" fill="{col}"/>')
    o.append(f'<text x="{lx + 5 * PITCH + 4:.0f}" y="{ly + 11}" font-size="11" font-style="italic" fill="#9fb3c8">treasure</text>')
    o.append(f'<path d="M{x0:.0f} {ly + 3}l8 8m0 -8l-8 8" stroke="#e63946" stroke-width="2" stroke-linecap="round"/>')
    o.append(f'<text x="{x0 + 14:.0f}" y="{ly + 11}" font-size="11" font-style="italic" fill="#9fb3c8">already plundered</text>')

    # the ship
    path = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    o.append(f"""<g><g class="bob" transform="translate(0 2)">
<path d="M-12 0 h24 q-2 8 -8 9 h-9 q-5 -1 -7 -9 Z" fill="#5a3a1e" stroke="#2b1a0c" stroke-width="1"/>
<path d="M-10 3 h20" stroke="#f4c430" stroke-width="1.2"/>
<path d="M0 0 V-23" stroke="#2b1a0c" stroke-width="1.6"/>
<path d="M1 -21 q12 4 10 18 h-10 Z M-1 -18 q-9 4 -8 15 h8 Z" fill="#fbf1d3" stroke="#2b1a0c" stroke-width="1"/>
<path d="M3 -15 q5 2 6 0 M3 -10 q5 2 7 0" fill="none" stroke="#e63946" stroke-width="1.4"/>
<path d="M0 -23 h9 l-2 3 l2 3 h-9 Z" fill="#111"/><circle cx="4" cy="-20" r="1.3" fill="#fff"/>
</g><animateMotion dur="{T}s" repeatCount="indefinite" path="{path}"/></g>""")
    o.append("</g></svg>")
    return "\n".join(o)


def main():
    days, total = fetch_graphql() if TOKEN else fetch_html()
    if not days:
        sys.exit("no contribution data found")
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(build(days, total))
    print(f"{USER}: {len(days)} days, {total} contributions -> {OUT}")


if __name__ == "__main__":
    main()
