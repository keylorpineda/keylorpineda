"""Render the activity card from live GitHub data.

Usage: GITHUB_TOKEN=... python scripts/stats.py <out_dir> [--mock]
"""

import datetime as dt
import json
import os
import random
import sys
import urllib.request
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from svglib import THEMES, fmt, svg_doc, text, tw  # noqa: E402

LOGIN = os.environ.get("PROFILE_LOGIN", "keylorpineda")
API = "https://api.github.com/graphql"

PROFILE_QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""

YEAR_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      totalIssueContributions
      totalRepositoryContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}
"""


def gql(query, variables):
    token = os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if payload.get("errors"):
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]


def collect(span_from, span_to):
    data = gql(YEAR_QUERY, {"login": LOGIN, "from": span_from.isoformat() + "Z", "to": span_to.isoformat() + "Z"})
    return data["user"]["contributionsCollection"]


def fetch():
    profile = gql(PROFILE_QUERY, {"login": LOGIN})["user"]
    now = dt.datetime.now(dt.UTC).replace(microsecond=0, tzinfo=None)
    last_year = collect(now - dt.timedelta(days=365), now)

    # All-time calendar, one year at a time (the API caps each window at a year).
    created = dt.datetime.fromisoformat(profile["createdAt"].rstrip("Z"))
    days = {}
    start = created
    while start < now:
        end = min(start + dt.timedelta(days=365), now)
        cal = collect(start, end)["contributionCalendar"]
        for w in cal["weeks"]:
            for d in w["contributionDays"]:
                days[d["date"]] = d["contributionCount"]
        start = end

    langs = Counter()
    colors = {}
    for repo in profile["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] += e["size"]
            colors[e["node"]["name"]] = e["node"]["color"] or "#8C959F"

    return dict(
        created=created.date(),
        today=now.date(),
        repos=profile["repositories"]["totalCount"],
        stars=sum(r["stargazerCount"] for r in profile["repositories"]["nodes"]),
        followers=profile["followers"]["totalCount"],
        year=last_year,
        days=days,
        langs=langs,
        colors=colors,
    )


def mock():
    r = random.Random(3)
    today = dt.date(2026, 10, 21)
    created = dt.date(2024, 3, 23)
    days, weeks = {}, []
    d = created
    while d <= today:
        days[d.isoformat()] = 0 if r.random() < 0.45 else r.randint(1, 18)
        d += dt.timedelta(days=1)
    start = today - dt.timedelta(days=364 + (today.weekday() + 1) % 7)
    d = start
    week = []
    while d <= today:
        c = days.get(d.isoformat(), 0)
        lv = "NONE" if c == 0 else ["FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"][min(c // 5, 3)]
        week.append({"date": d.isoformat(), "contributionCount": c, "contributionLevel": lv})
        if len(week) == 7:
            weeks.append({"contributionDays": week})
            week = []
        d += dt.timedelta(days=1)
    if week:
        weeks.append({"contributionDays": week})
    total = sum(x["contributionCount"] for w in weeks for x in w["contributionDays"])
    year = dict(
        totalCommitContributions=int(total * 0.8), totalPullRequestContributions=96, totalPullRequestReviewContributions=31,
        totalIssueContributions=58, totalRepositoryContributions=9, restrictedContributionsCount=0,
        contributionCalendar={"totalContributions": total, "weeks": weeks},
    )
    langs = Counter({"TypeScript": 900000, "Python": 520000, "Java": 210000, "CSS": 80000, "JavaScript": 60000, "Shell": 9000, "Dockerfile": 4000})
    colors = {"TypeScript": "#3178c6", "Python": "#3572A5", "Java": "#b07219", "CSS": "#663399", "JavaScript": "#f1e05a", "Shell": "#89e051", "Dockerfile": "#384d54"}
    return dict(created=created, today=today, repos=8, stars=5, followers=7, year=year, days=days, langs=langs, colors=colors)


def streaks(days, today):
    dates = sorted(days)
    longest, run, run_start, best = 0, 0, None, (None, None)
    for ds in dates:
        if days[ds] > 0:
            if run == 0:
                run_start = ds
            run += 1
            if run > longest:
                longest, best = run, (run_start, ds)
        else:
            run = 0
    # Current streak: today may still be empty without breaking it.
    cur, d = 0, today
    if days.get(d.isoformat(), 0) == 0:
        d -= dt.timedelta(days=1)
    cur_end = d
    while days.get(d.isoformat(), 0) > 0:
        cur += 1
        d -= dt.timedelta(days=1)
    cur_start = d + dt.timedelta(days=1)
    return cur, (cur_start, cur_end), longest, best


def short(d):
    if isinstance(d, str):
        d = dt.date.fromisoformat(d)
    return d.strftime("%b %-d, %Y")


def card(W, H, th):
    return f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="24" fill="{th["card"]}" stroke="{th["border"]}"/>'


REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
GROW = (
    ".bar{transform-box:fill-box;transform-origin:left center;animation:grow 1.4s cubic-bezier(.2,.8,.2,1) backwards}"
    "@keyframes grow{from{transform:scaleX(0)}}"
    ".fade{animation:fade .8s ease-out backwards}@keyframes fade{from{opacity:0;transform:translateY(6px)}}"
)
STYLE = (
    ".rv{transform-box:fill-box;transform-origin:center;animation:rv .55s cubic-bezier(.2,.8,.3,1.3) backwards}"
    "@keyframes rv{from{opacity:0;transform:scale(.2)}}"
    ".w{animation:wave 10s ease-in-out infinite backwards}"
    "@keyframes wave{0%,100%{opacity:0}4%{opacity:.4}10%{opacity:0}}"
    ".ring{transform-box:fill-box;transform-origin:center;animation:ring 2.2s ease-out infinite}"
    "@keyframes ring{0%{transform:scale(1);opacity:.9}100%{transform:scale(2.3);opacity:0}}"
    + REDUCED
)


def odometer(num, size, x, y, fill, delay=0.0):
    """Digits roll up from 0 to their value. Static viewers see the final number."""
    from svglib import F

    out, cx = [], x
    lh = size * 1.15
    for i, ch in enumerate(num):
        w = F["display"].width(ch, size) - 1.2 * (1 if i < len(num) - 1 else 0)
        if not ch.isdigit():
            out.append(text(ch, size, cx, y, fill, "display"))
            cx += w
            continue
        dgt = int(ch)
        cid = f"od{abs(hash((num, i, x, y))) % 10**8}"
        out.append(f'<clipPath id="{cid}"><rect x="{fmt(cx - 2)}" y="{fmt(y - size * 0.9)}" width="{fmt(w + 4)}" height="{fmt(size * 1.12)}"/></clipPath>')
        col = "".join(text(str(k), size, cx + (w - F["display"].width(str(k), size)) / 2, y + k * lh, fill, "display") for k in range(10))
        d = delay + (len(num) - i) * 0.12
        out.append(f'<g clip-path="url(#{cid})"><g class="od" style="--t:translateY({fmt(-dgt * lh)}px);animation-delay:{d:.2f}s" transform="translate(0 {fmt(-dgt * lh)})">{col}</g></g>')
        cx += w
    return "".join(out), cx - x


ODO = (
    ".od{animation:roll 1.8s cubic-bezier(.15,.85,.25,1) backwards}"
    "@keyframes roll{from{transform:translateY(0)}to{transform:var(--t)}}"
)


def render(s, theme):
    th = THEMES[theme]
    W = 1000
    year = s["year"]
    cal = year["contributionCalendar"]
    weeks = cal["weeks"]
    all_time = sum(s["days"].values())
    cur, (cs, ce), longest, (ls, le) = streaks(s["days"], s["today"])
    files = {}

    # ---- stat tiles, 2 x 2
    tiles = [
        (f"{cal['totalContributions']:,}", "", "Contributions", "in the last 12 months"),
        (f"{all_time:,}", "", "All time", f"since {s['created'].strftime('%b %Y')}"),
        (f"{cur}", "day" if cur == 1 else "days", "Current streak", f"since {short(cs)}" if cur else "starts with the next commit"),
        (f"{longest}", "day" if longest == 1 else "days", "Longest streak", f"{short(ls)} to {short(le)}" if longest else "no streak yet"),
    ]
    gap = 16
    tw_, th_ = (W - gap) / 2, 150
    b = []
    for i, (num, unit, lab, sub) in enumerate(tiles):
        x = (i % 2) * (tw_ + gap)
        y = (i // 2) * (th_ + gap)
        b.append(f'<rect x="{fmt(x+.5)}" y="{fmt(y+.5)}" width="{fmt(tw_-1)}" height="{th_-1}" rx="22" fill="{th["card"]}" stroke="{th["border"]}"/>')
        b.append(text(lab.upper(), 14, x + 34, y + 44, th["accent"] if i == 2 else th["muted"], "semibold", tracking=2.2))
        od, odw = odometer(num, 54, x + 31, y + 104, th["text"], delay=0.15 * i)
        b.append(od)
        if unit:
            b.append(text(unit, 21, x + 31 + odw + 10, y + 104, th["muted"], "medium", extra=f'class="fade" style="animation-delay:{1.2 + .15*i:.2f}s"'))
        if i == 2 and cur:
            b.append(f'<g transform="translate({fmt(x + tw_ - 64)} {y + 30})"><circle class="ring" cx="12" cy="12" r="6" fill="{th["accent"]}" opacity=".5"/>'
                     f'<circle cx="12" cy="12" r="6" fill="{th["accent"]}"/></g>')
        b.append(text(sub, 16, x + 34, y + 130, th["faint"], "medium"))
    H = 2 * th_ + gap
    files["activity-stats"] = svg_doc(W, H, "".join(b), f"{cal['totalContributions']} contributions in the last year, {all_time} all time, current streak {cur} days, longest streak {longest} days", ODO + GROW + STYLE)

    # ---- calendar
    cell, step = 14, 17
    grid_w = len(weeks) * step - (step - cell)
    hx = W - 32 - grid_w
    b = []
    b.append(text(f"{cal['totalContributions']:,} contributions in the last year", 21, 32, 52, th["text"], "semibold"))
    levels = {"NONE": (th["cell"], 1), "FIRST_QUARTILE": (th["accent"], 0.3), "SECOND_QUARTILE": (th["accent"], 0.52),
              "THIRD_QUARTILE": (th["accent"], 0.76), "FOURTH_QUARTILE": (th["accent"], 1)}
    gy = 108
    last_month = None
    weekday_counts = Counter()
    busiest = ("", 0)
    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            date = dt.date.fromisoformat(d["date"])
            wd = (date.weekday() + 1) % 7
            weekday_counts[date.strftime("%A")] += d["contributionCount"]
            if d["contributionCount"] > busiest[1]:
                busiest = (d["date"], d["contributionCount"])
            x, y = hx + wi * step, gy + wd * step
            c, o = levels.get(d["contributionLevel"], levels["NONE"])
            rd = wi * 0.022 + wd * 0.015
            if d["contributionCount"]:
                b.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{cell}" height="{cell}" rx="3.5" fill="{th["cell"]}"/>')
            b.append(f'<rect class="rv" style="animation-delay:{rd:.2f}s" x="{fmt(x)}" y="{fmt(y)}" width="{cell}" height="{cell}" rx="3.5" fill="{c}" opacity="{o}"/>')
            if d["contributionCount"]:
                b.append(f'<rect class="w" style="animation-delay:{2 + wi*0.045 + wd*0.03:.2f}s" x="{fmt(x)}" y="{fmt(y)}" width="{cell}" height="{cell}" rx="3.5" fill="{th["text"]}" opacity="0"/>')
            if d["date"] == s["today"].isoformat():
                today_xy = (x, y)
            if date.day <= 7 and wd == 0 and date.month != last_month:
                last_month = date.month
                if wi < len(weeks) - 2:
                    b.append(text(date.strftime("%b"), 14, x, gy - 14, th["muted"], "medium"))
    if "today_xy" in locals():
        tx, ty = today_xy
        b.append(f'<rect class="ring" x="{fmt(tx)}" y="{fmt(ty)}" width="{cell}" height="{cell}" rx="3.5" fill="none" stroke="{th["accent"]}" stroke-width="2"/>')
    for wd, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        b.append(text(name, 13, hx - 10, gy + wd * step + 11.5, th["faint"], "medium", "end"))
    ly = gy + 7 * step + 34
    fav = weekday_counts.most_common(1)[0][0] if weekday_counts and weekday_counts.most_common(1)[0][1] else None
    facts = []
    if busiest[1]:
        facts.append(f"Busiest day: {short(busiest[0])}, {busiest[1]} contributions")
    if fav:
        facts.append(f"Most active on {fav}s")
    b.append(text("   ·   ".join(facts), 15, 32, ly, th["muted"], "medium"))
    lx = W - 32
    b.append(text("More", 14, lx, ly, th["faint"], "medium", "end"))
    lx -= tw("More", 14, "medium") + 8 + 5 * 18 - 4
    for i, k in enumerate(levels):
        c, o = levels[k]
        b.append(f'<rect x="{fmt(lx + i*18)}" y="{ly-12}" width="14" height="14" rx="3.5" fill="{c}" opacity="{o}"/>')
    b.append(text("Less", 14, lx - 8, ly, th["faint"], "medium", "end"))
    H = ly + 32
    files["activity-calendar"] = svg_doc(W, H, card(W, H, th) + "".join(b), f"Contribution calendar: {cal['totalContributions']} contributions in the last year", STYLE)

    # ---- breakdown
    rows = [
        ("Commits", year["totalCommitContributions"] + year["restrictedContributionsCount"]),
        ("Pull requests", year["totalPullRequestContributions"]),
        ("Issues", year["totalIssueContributions"]),
        ("Code reviews", year["totalPullRequestReviewContributions"]),
        ("New repositories", year["totalRepositoryContributions"]),
    ]
    b = [text("LAST 12 MONTHS", 15, 36, 54, th["muted"], "semibold", tracking=2.2)]
    mx = max(v for _, v in rows) or 1
    for i, (lab, v) in enumerate(rows):
        yy = 104 + i * 48
        b.append(text(lab, 20, 36, yy, th["text"], "medium"))
        bx, bwid = 260, W - 260 - 140
        b.append(f'<rect x="{bx}" y="{yy-12}" width="{fmt(bwid)}" height="10" rx="5" fill="{th["cell"]}"/>')
        b.append(f'<rect class="bar" style="animation-delay:{.2 + i*.12:.2f}s" x="{bx}" y="{yy-12}" width="{fmt(max(bwid * v / mx, 10 if v else 0))}" height="10" rx="5" fill="{th["accent"]}"/>')
        b.append(text(f"{v:,}", 20, W - 36, yy, th["text"], "semibold", "end"))
    H = 104 + len(rows) * 48 - 12
    files["activity-breakdown"] = svg_doc(W, H, card(W, H, th) + "".join(b), "Contribution breakdown: " + ", ".join(f"{k} {v}" for k, v in rows), GROW + REDUCED)

    # ---- languages
    total = sum(s["langs"].values()) or 1
    top = s["langs"].most_common(6)
    b = [text("TOP LANGUAGES IN PUBLIC REPOS", 15, 36, 54, th["muted"], "semibold", tracking=2.2)]
    bx, bwid = 36, W - 72
    b.append(f'<clipPath id="lb"><rect x="{bx}" y="76" width="{bwid}" height="14" rx="7"/></clipPath><g clip-path="url(#lb)">')
    b.append(f'<rect x="{bx}" y="76" width="{bwid}" height="14" fill="{th["cell"]}"/>')
    cx = bx
    for name, size in top:
        w = bwid * size / total
        b.append(f'<rect class="bar" style="animation-delay:{.15 + top.index((name, size))*.18:.2f}s" x="{fmt(cx)}" y="76" width="{fmt(w)}" height="14" fill="{s["colors"][name]}"/>')
        cx += w
    b.append("</g>")
    colw = bwid / 3
    for i, (name, size) in enumerate(top):
        xx = bx + (i % 3) * colw
        yy = 138 + (i // 3) * 46
        b.append(f'<circle cx="{fmt(xx+8)}" cy="{yy-7}" r="7" fill="{s["colors"][name]}"/>')
        b.append(text(name, 19, xx + 26, yy, th["text"], "medium"))
        b.append(text(f"{100*size/total:.1f}%", 19, xx + colw - 30, yy, th["muted"], "medium", "end"))
    yy = 138 + ((len(top) + 2) // 3) * 46 + 2
    b.append(f'<path d="M36 {yy-18}H{W-36}" stroke="{th["border"]}"/>')
    b.append(text(f"{s['repos']} public repositories  ·  {s['stars']} stars  ·  {s['followers']} followers", 16, 36, yy + 16, th["muted"], "medium"))
    b.append(text(f"Updated {short(s['today'])}", 16, W - 36, yy + 16, th["faint"], "medium", "end"))
    H = yy + 44
    files["activity-languages"] = svg_doc(W, H, card(W, H, th) + "".join(b), "Top languages: " + ", ".join(f"{n} {100*v/total:.1f}%" for n, v in top), GROW + REDUCED)
    return files


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    out.mkdir(parents=True, exist_ok=True)
    data = mock() if "--mock" in sys.argv else fetch()
    for theme in ("dark", "light"):
        for name, svg in render(data, theme).items():
            (out / f"{name}-{theme}.svg").write_text(svg)
    print("activity cards written to", out)


if __name__ == "__main__":
    main()
