"""Builds every static asset in assets/ and writes README.md.

Usage: python scripts/build.py
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from svglib import THEMES, fmt, icon, label_of, paragraph, rng, svg_doc, text, tw, wrap  # noqa: E402
from visuals import v_booth, v_healthy, v_rag  # noqa: E402

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "assets"
USER = "keylorpineda"
EMAIL = "keylorpineda729@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/keylor-pineda"
SITE = "https://keylorpineda.dev"
RAW = f"https://raw.githubusercontent.com/{USER}/{USER}/output"
STAMP = __import__("datetime").datetime.now(__import__("datetime").UTC).strftime("%Y%m%d%H%M")
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
THEME_NAMES = ("dark", "light")


def write(name, theme, svg):
    (ASSETS / f"{name}-{theme}.svg").write_text(svg, encoding="utf-8", newline="\n")


def pic(name, alt, width=None, height=None, base="assets"):
    size = (f' width="{width}"' if width else "") + (f' height="{height}"' if height else "")
    return (
        f'<picture><source media="(prefers-color-scheme: dark)" srcset="{base}/{name}-dark.svg">'
        f'<img src="{base}/{name}-light.svg" alt="{alt}"{size}></picture>'
    )


def frame(w, h, th, rx=22):
    return f'<rect x=".5" y=".5" width="{fmt(w-1)}" height="{fmt(h-1)}" rx="{rx}" fill="{th["card"]}" stroke="{th["border"]}"/>'


# --------------------------------------------------------------------------- header
EASE = "cubic-bezier(.22,1,.36,1)"


def letters(t, size, x, y, fill, cls, delay, step=0.045, tracking=0.0):
    """Display text drawn one letter at a time, so each letter can animate on its own."""
    out = []
    for i, ch in enumerate(t):
        if ch == " ":
            continue
        cx = x + (tw(t[:i], size, "display", tracking) + tracking if i else 0)
        out.append(text(ch, size, cx, y, fill, "display", extra=f'class="{cls}" style="animation-delay:{delay + i * step:.3f}s"'))
    return "".join(out), delay + len(t) * step


def sun(th, cx, cy, r, gid="sun"):
    """The low amber sun from the site, clipped by the card it sits in."""
    return (
        f'<radialGradient id="{gid}"><stop offset="0" stop-color="{th["fill"]}" stop-opacity=".62"/>'
        f'<stop offset=".62" stop-color="{th["fill"]}" stop-opacity=".14"/><stop offset="1" stop-color="{th["fill"]}" stop-opacity="0"/></radialGradient>'
        f'<circle class="sun" cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})"/>'
    )


SUN_CSS = (
    ".sun{transform-box:fill-box;transform-origin:center;animation:sun 9s ease-in-out infinite alternate}"
    "@keyframes sun{from{transform:scale(.86)}to{transform:scale(1.08)}}"
)


def mini_window(th, tint, kind):
    """A small app window, 280 x 186, centred on the origin."""
    w, h = 280, 186
    x, y = -w / 2, -h / 2
    b = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{th["card2"]}" stroke="{th["border"]}"/>']
    b.append(f'<path d="M{x} {y + 28}H{x + w}" stroke="{th["border"]}"/>')
    for i, col in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        b.append(f'<circle cx="{x + 18 + i * 14}" cy="{y + 14}" r="4" fill="{col}"/>')
    b.append(f'<rect x="{-46}" y="{y + 8}" width="92" height="12" rx="6" fill="{th["cell"]}"/>')
    top = y + 40
    if kind == "store":  # Booth: a cover, the shop's name and three products
        b.append(f'<rect x="{x + 14}" y="{top}" width="{w - 28}" height="40" rx="8" fill="{tint}" opacity=".85"/>')
        b.append(f'<rect x="{x + 14}" y="{top + 50}" width="110" height="9" rx="4.5" fill="{th["text"]}"/>')
        b.append(f'<rect x="{x + 14}" y="{top + 66}" width="170" height="6" rx="3" fill="{th["faint"]}"/>')
        for i in range(3):
            b.append(f'<rect x="{x + 14 + i * 86}" y="{top + 84}" width="80" height="48" rx="8" fill="{th["cell"]}" stroke="{th["border"]}"/>')
            b.append(f'<circle cx="{x + 82 + i * 86}" cy="{top + 120}" r="6" fill="{tint}"/>')
    elif kind == "answer":  # Research Engine: a question, an answer with citations and its sources
        b.append(f'<rect x="{x + 14}" y="{top}" width="{w - 28}" height="30" rx="8" fill="{th["cell"]}" stroke="{th["border"]}"/>')
        b.append(f'<rect x="{x + 24}" y="{top + 11}" width="120" height="7" rx="3.5" fill="{th["muted"]}"/>')
        b.append(f'<rect x="{x + w - 62}" y="{top + 6}" width="42" height="18" rx="6" fill="{tint}"/>')
        for i, lw in enumerate((150, 132, 144, 96)):
            b.append(f'<rect x="{x + 14}" y="{top + 44 + i * 14}" width="{lw}" height="6" rx="3" fill="{th["faint"] if i else th["text"]}"/>')
        for i in range(3):
            b.append(f'<rect x="{x + 180}" y="{top + 42 + i * 30}" width="86" height="24" rx="6" fill="{th["cell"]}" stroke="{th["border"]}"/>')
            b.append(f'<rect x="{x + 188}" y="{top + 51 + i * 30}" width="{44 - i * 8}" height="5" rx="2.5" fill="{tint}"/>')
        b.append(f'<rect x="{x + 14}" y="{top + 108}" width="150" height="5" rx="2.5" fill="{th["cell"]}"/>')
        b.append(f'<rect x="{x + 14}" y="{top + 108}" width="92" height="5" rx="2.5" fill="{tint}"/>')
    else:  # HealthyCropping: a leaf under the scanner and the result
        b.append(f'<rect x="{x + 14}" y="{top}" width="112" height="{h - 54}" rx="10" fill="{th["cell"]}" stroke="{th["border"]}"/>')
        b.append(f'<path transform="translate({x + 70} {top + 66}) rotate(-18) scale(.52)" d="M0 -88C52 -60 62 10 0 86C-62 10 -52 -60 0 -88Z" fill="{tint}"/>')
        b.append(f'<circle cx="{x + 78}" cy="{top + 58}" r="5" fill="#E0962E"/><circle cx="{x + 62}" cy="{top + 80}" r="3.5" fill="#E0962E"/>')
        b.append(f'<rect x="{x + 140}" y="{top + 4}" width="96" height="9" rx="4.5" fill="{th["text"]}"/>')
        for i, lw in enumerate((120, 104, 112)):
            b.append(f'<rect x="{x + 140}" y="{top + 26 + i * 14}" width="{lw}" height="6" rx="3" fill="{th["faint"]}"/>')
        b.append(f'<rect x="{x + 140}" y="{top + 80}" width="126" height="34" rx="9" fill="{th["card"]}" stroke="{th["border"]}"/>')
        b.append(f'<rect x="{x + 150}" y="{top + 94}" width="106" height="6" rx="3" fill="{th["cell"]}"/>')
        b.append(f'<rect x="{x + 150}" y="{top + 94}" width="66" height="6" rx="3" fill="{tint}"/>')
    return "".join(b)


def header(theme):
    """One card for everything at the top: the name and role, three project windows,
    the key facts, and the site as the amber base of the card."""
    th = THEMES[theme]
    W, H, BAND = 1000, 660, 168
    ink = th["on_fill"]
    R = rng(7)
    b = [f'<clipPath id="card"><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="28"/></clipPath>', frame(W, H, th, 28)]

    # Texture: a field of dots that thins out toward the name, with a few of them glinting.
    b.append(
        f'<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="1.3" fill="{th["border"]}"/></pattern>'
        '<linearGradient id="fade" x1="0" x2="1"><stop offset=".3" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>'
        f'<mask id="thin"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>'
    )
    glints = "".join(
        f'<circle class="glint" style="animation-delay:{R.uniform(0, 7):.1f}s;animation-duration:{R.uniform(4, 8):.1f}s" '
        f'cx="{3 + 24 * R.randrange(18, 41)}" cy="{3 + 24 * R.randrange(1, 19)}" r="2.2" fill="{th["fill"]}"/>'
        for _ in range(16)
    )
    b.append(f'<g clip-path="url(#card)"><rect width="{W}" height="{H - BAND}" fill="url(#dots)" mask="url(#thin)"/>{glints}{sun(th, 742, 560, 330)}</g>')

    # The name, one letter at a time, then the role right under it.
    size = 118
    assert 52 + tw("Pineda.", size, "display", -3) < 520, "the name must stay clear of the windows"
    l1, t = letters("Keylor", size, 52, 160, th["text"], "l", 0.15, tracking=-3)
    l2, t = letters("Pineda.", size, 52, 268, th["accent_big"], "l", t + 0.05, tracking=-3)
    b += [l1, l2]
    b.append(text("Software developer", 35, 55, 328, th["text"], "display", tracking=-0.8, extra=f'class="up" style="animation-delay:{t + 0.1:.2f}s"'))
    rx = 55 + tw("Software developer", 35, "display", -0.8) + 18
    b.append(text("COSTA RICA", 13, rx, 326, th["faint"], "semibold", tracking=2.4, extra=f'class="up" style="animation-delay:{t + 0.2:.2f}s"'))

    # Three projects as windows: they open like a hand of cards, then keep floating.
    cx, cy = 742, 196
    fan = [
        ("leaf", "#17B877", -122, 20, -10, "fl", 0.9),
        ("answer", "#1FA37F", 122, 20, 10, "fr", 1.0),
        ("store", "#5B54F0", 0, -6, 0, "fc", 0.8),
    ]
    for kind, tint, dx, dy, rot, cls, delay in fan:
        b.append(
            f'<g transform="translate({cx + dx} {cy + dy}) rotate({rot}) scale(1.12)"><g class="float" style="animation-delay:{-delay * 3:.1f}s">'
            f'<g class="{cls}" style="animation-delay:{delay:.2f}s">{mini_window(th, tint, kind)}</g></g></g>'
        )

    # The facts, as four tiles across the card.
    tiles = [("3", "products shipped"), ("4", "cloud and AI certifications"), ("UTC−6", "Costa Rica"), ("Now", "building HealthyCropping")]
    tx, ty, gap = 52, 372, 12
    tile_w = (W - 2 * tx - gap * (len(tiles) - 1)) / len(tiles)
    for i, (big, small) in enumerate(tiles):
        x = tx + i * (tile_w + gap)
        tile = (
            f'<rect x="{fmt(x)}" y="{ty}" width="{fmt(tile_w)}" height="92" rx="16" fill="{th["card2"]}" stroke="{th["border"]}"/>'
            + text(big, 34, x + 18, ty + 46, th["text"], "display", tracking=-0.8)
            + text(small, 13.5, x + 18, ty + 72, th["muted"], "medium")
        )
        b.append(f'<g class="up" style="animation-delay:{t + 0.3 + i * 0.08:.2f}s">{tile}</g>')

    # The site is the base of the card: a solid amber band with a light that keeps crossing it.
    by = H - BAND
    band = [
        f'<linearGradient id="amber" x1="0" x2="1"><stop offset="0" stop-color="{th["fill"]}"/><stop offset="1" stop-color="#FFB627"/></linearGradient>'
        f'<rect x="0" y="{by}" width="{W}" height="{BAND}" fill="url(#amber)"/>'
        f'<rect class="sweep" x="-260" y="{by - 30}" width="170" height="{BAND + 60}" fill="#FFFFFF" opacity=".36" transform="skewX(-18)"/>'
    ]
    b.append(f'<g clip-path="url(#card)">{"".join(band)}</g>')
    b.append(text("THE FULL PORTFOLIO", 13.5, 55, by + 48, ink, "semibold", tracking=2.6))
    b.append(text("keylorpineda.dev", 64, 51, by + 112, ink, "display", tracking=-1.8))
    b.append(text("Scroll-driven scenes, live captures of every project, English and Spanish, light and dark.", 16.5, 55, by + 143, ink, "medium"))
    b.append(
        f'<g class="go"><circle cx="{W - 100}" cy="{by + BAND / 2}" r="42" fill="{ink}"/>'
        f'<g transform="translate({W - 113} {by + BAND / 2 - 13})" fill="none" stroke="{th["fill"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 21L21 5M9 5h12v12"/></g></g>'
    )

    style = (
        f".l,.up,.fl,.fr,.fc{{transform-box:fill-box;animation-duration:1.1s;animation-timing-function:{EASE};animation-fill-mode:backwards}}"
        ".l{transform-origin:0 100%;animation-name:letter}"
        "@keyframes letter{from{opacity:0;transform:translateY(46px) rotate(9deg)}}"
        ".up{animation-name:up}"
        "@keyframes up{from{opacity:0;transform:translateY(18px)}}"
        ".fl,.fr,.fc{transform-origin:center;animation-duration:1.5s}"
        ".fc{animation-name:fc}.fl{animation-name:fl}.fr{animation-name:fr}"
        "@keyframes fc{from{opacity:0;transform:translateY(150px) scale(.7)}}"
        "@keyframes fl{from{opacity:0;transform:translate(122px,150px) rotate(10deg) scale(.7)}}"
        "@keyframes fr{from{opacity:0;transform:translate(-122px,150px) rotate(-10deg) scale(.7)}}"
        ".float{animation:float 7s ease-in-out infinite alternate}"
        "@keyframes float{from{transform:translateY(-5px)}to{transform:translateY(6px)}}"
        ".glint{opacity:0;animation:glint 6s ease-in-out infinite}"
        "@keyframes glint{0%,100%{opacity:0}50%{opacity:.9}}"
        ".sweep{animation:sweep 5.5s cubic-bezier(.4,0,.2,1) infinite}"
        "@keyframes sweep{0%,35%{translate:0 0}75%,100%{translate:1500px 0}}"
        ".go{transform-box:fill-box;transform-origin:center;animation:go 2.8s ease-in-out infinite}"
        "@keyframes go{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}" + SUN_CSS + REDUCED
    )
    title = "Keylor Pineda, software developer from Costa Rica. 3 products shipped, 4 cloud and AI certifications. Portfolio: keylorpineda.dev"
    write("header", theme, svg_doc(W, H, "".join(b), title, style))


# --------------------------------------------------------------------------- section titles
SECTIONS = ["About me", "Selected work", "Certifications", "Activity", "Toolbox", "Where I'm heading", "Contact"]


def section(i, theme):
    """A numbered title with a rule that draws itself and a spark that keeps running along it."""
    th = THEMES[theme]
    W, H = 1000, 86
    title = SECTIONS[i]
    num = f"{i + 1:02d}"
    b = [text(num, 14, 2, 30, th["accent"], "semibold", tracking=2.4)]
    b.append(text(title, 44, 0, 74, th["text"], "display", tracking=-1.4, extra='class="t"'))
    x0 = tw(title, 44, "display", -1.4) + 26
    b.append(f'<rect class="rule" x="{fmt(x0)}" y="60" width="{fmt(W - x0)}" height="1.5" fill="{th["border"]}"/>')
    b.append(f'<rect class="spark" x="{fmt(x0)}" y="58.500" width="46" height="4.500" rx="2.250" fill="{th["fill"]}" style="--run:{fmt(W - x0 - 46)}px"/>')
    style = (
        f".t{{transform-box:fill-box;animation:rise 1s {EASE} backwards}}"
        "@keyframes rise{from{opacity:0;transform:translateY(22px)}}"
        f".rule{{transform-box:fill-box;transform-origin:0 50%;animation:rule 1.4s {EASE} .2s backwards}}"
        "@keyframes rule{from{transform:scaleX(0)}}"
        ".spark{animation:spark 6s cubic-bezier(.5,0,.5,1) infinite}"
        "@keyframes spark{0%{translate:0 0;opacity:0}8%{opacity:1}46%{opacity:1}54%,100%{translate:var(--run) 0;opacity:0}}" + REDUCED
    )
    write(f"section-{i + 1}", theme, svg_doc(W, H, "".join(b), title, style))


# --------------------------------------------------------------------------- buttons
def g_mail(th, x, y):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{th["accent"]}" stroke-width="2" stroke-linejoin="round">'
            '<rect x="1" y="3" width="20" height="15" rx="3"/><path d="M2 5l9 7 9-7" stroke-linecap="round"/></g>')


def g_linkedin(th, x, y):
    return (f'<g transform="translate({x} {y}) scale(.9167)"><rect width="24" height="24" rx="5" fill="#0A66C2"/>'
            '<rect x="5" y="9.5" width="3.2" height="9.5" fill="#fff"/><circle cx="6.6" cy="6.2" r="1.9" fill="#fff"/>'
            '<path d="M10.6 9.5h3.1v1.4c.5-.9 1.6-1.7 3.2-1.7 3 0 3.6 1.9 3.6 4.5V19h-3.2v-4.6c0-1.2 0-2.6-1.6-2.6s-1.9 1.2-1.9 2.5V19h-3.2z" fill="#fff"/></g>')


def g_globe(th, x, y):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{th["accent"]}" stroke-width="1.9" stroke-linecap="round">'
            '<circle cx="11" cy="11" r="9.5"/><path d="M1.5 11h19M11 1.5c3 3.2 3 15.8 0 19M11 1.5c-3 3.2-3 15.8 0 19"/></g>')


def g_github(th, x, y):
    return icon("github", x, y, 22, th)


def g_arrow(th, x, y):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{th["accent"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M5 17L17 5M8 5h9v9"/></g>')


def button(name, theme, label, glyph, primary=False):
    th = THEMES[theme]
    H = 46
    W = tw(label, 15.5, "semibold") + 82  # noqa
    fill = th["fill"] if primary else th["card"]
    fg = th["on_fill"] if primary else th["text"]
    tht = dict(th, accent=th["on_fill"] if primary else th["accent"], text=fg)
    body = (
        f'<rect x="1" y=".5" width="{fmt(W-2)}" height="{H-1}" rx="{(H-1)/2}" fill="{fill}" stroke="{fill if primary else th["border"]}"/>'
        + glyph(tht, 22, 12)
        + text(label, 15.5, 56, 29, fg, "semibold")
    )
    write(f"btn-{name}", theme, svg_doc(W, H, body, label))


# --------------------------------------------------------------------------- chips
def chip_svg(slug, theme, label=None):
    th = THEMES[theme]
    label = label or label_of(slug)
    h, fs, isz, gut = 30, 13.5, 16, 3
    H = h + 2 * gut
    w = 12 + isz + 8 + tw(label, fs, "medium") + 14
    W = w + 2 * gut  # transparent gutter so inline chips breathe
    body = (
        f'<rect x="{gut}" y="{gut+.5}" width="{fmt(w)}" height="{h-1}" rx="{(h-1)/2}" fill="{th["card2"]}" stroke="{th["border"]}"/>'
        + icon(slug, gut + 12, gut + (h - isz) / 2, isz, dict(th))
        + text(label, fs, gut + 12 + isz + 8, gut + h / 2 + fs * 0.36, th["text"], "medium")
    )
    return svg_doc(W, H, body, label)


LABELS = {"java": "Java", "gnubash": "Bash", "nodedotjs": "Node.js", "reactquery": "TanStack Query",
          "oracle": "Oracle Cloud", "aws": "AWS", "groq": "Groq", "meta": "Llama 3.3", "cohere": "Cohere Rerank"}
USED_CHIPS = set()


def chips_md(slugs):
    out = []
    for s in slugs:
        USED_CHIPS.add(s)
        out.append(pic(f"chips/{s}", LABELS.get(s, label_of(s)), height=36))
    return "\n".join(out)


# --------------------------------------------------------------------------- project banners
PROJECTS = [
    dict(
        name="healthycropping", accent="#3FA163", kicker="ANDROID  ·  ON-DEVICE ML", title="HealthyCropping",
        tagline="Crop disease detection that works in the field, with no signal.",
        status="In development", visual=v_healthy, url=f"https://github.com/{USER}/healthycropping",
        desc="Point a phone at a coffee leaf, a cacao pod or a banana leaf and get a diagnosis right there in the plot. "
        "Each crop has its own MobileNetV3 model running on the device through TensorFlow Lite, and scans, farms and plots "
        "are stored locally first. Next up: sync and a Gemini RAG layer that explains what to do and cites official "
        "agronomy manuals.",
        tools=["reactnative", "expo", "typescript", "tflite", "python", "fastapi", "firebase", "sqlite", "googlegemini"],
        buttons=[("source-hc", "Source code", f"https://github.com/{USER}/healthycropping")],
    ),
    dict(
        name="booth", accent="#6366F1", kicker="WEB APP  ·  COMMERCE", title="Booth",
        tagline="An online catalog for small shops, with orders through WhatsApp.",
        status="Live demo", visual=v_booth, url=f"https://github.com/{USER}/booth",
        desc="Small businesses already sell through WhatsApp, one chat at a time. Booth gives each store a single link with "
        "its catalog, turns the cart into a clean WhatsApp message, reserves stock atomically and uses Gemini to read "
        "transfer receipts, so owners know what to check before confirming a payment.",
        tools=["react", "typescript", "vite", "tailwindcss", "reactquery", "nestjs", "prisma", "postgresql", "zod", "googlegemini", "vercel", "render", "neon", "playwright"],
        buttons=[("demo-booth", "Live demo", "https://booth-tawny.vercel.app/s/panaderia-demo"),
                 ("source-booth", "Source code", f"https://github.com/{USER}/booth")],
    ),
    dict(
        name="rag", accent="#1F9E98", kicker="AI  ·  RETRIEVAL", title="RAG Research Engine",
        tagline="Answers from your documents, with sources, and no answer when the evidence is missing.",
        status="Live demo  ·  benchmarked in CI", visual=v_rag, url=f"https://github.com/{USER}/RAG-Research-Engine",
        desc="Upload PDFs and notes, ask in English or Spanish, and get answers that cite the exact passages they use. "
        "Retrieval fuses pgvector and Postgres full-text search with Reciprocal Rank Fusion, an optional Cohere reranker "
        "reorders the results, and a calibrated gate refuses before the model is called when the documents don't hold the "
        "answer. An Angular web app shows each answer next to its sources, and a benchmark runs on every pull request and "
        "fails if quality drops.",
        tools=["python", "fastapi", "postgresql", "sqlalchemy", "angular", "cohere", "groq", "docker", "pytest", "vercel", "render", "neon"],
        buttons=[("demo-rag", "Live demo", "https://research-engine-omega.vercel.app"),
                 ("source-rag", "Source code", f"https://github.com/{USER}/RAG-Research-Engine")],
    ),
]


def banner(p, theme):
    th = THEMES[theme]
    W, H = 1000, 440
    b = [frame(W, H, th, 26)]
    acc = p["accent"]
    b.append(text(p["kicker"], 15, 48, 82, acc, "semibold", tracking=2.4))
    lines = wrap(p["title"], 54, 420, "display")
    y = 148
    for ln in lines:
        b.append(text(ln, 54, 46, y, th["text"], "display", tracking=-1.4))
        y += 60
    tl, th_ = paragraph(p["tagline"], 22, 48, y + 6, 400, th["muted"], leading=1.5)
    b.append(tl)
    sw = tw(p["status"], 15, "medium") + 46
    b.append(f'<rect x="48" y="{H-84}" width="{fmt(sw)}" height="38" rx="19" fill="{th["card2"]}" stroke="{th["border"]}"/>')
    b.append(f'<circle cx="68" cy="{H-65}" r="5" fill="{acc}"/>')
    b.append(text(p["status"], 15, 82, H - 59.5, th["text"], "medium"))
    vx, vy, vw, vh = 500, 30, 470, H - 60
    b.append(f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="18" fill="{th["card2"]}" stroke="{th["border"]}"/>')
    vis, style = p["visual"](th, acc, vx, vy, vw, vh)
    b.append(vis)
    for i, col in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        b.append(f'<circle cx="{vx + 22 + i * 16}" cy="{vy + 20}" r="5" fill="{col}"/>')
    write(f"project-{p['name']}", theme, svg_doc(W, H, "".join(b), f"{p['title']}: {p['tagline']}", style + REDUCED))


# --------------------------------------------------------------------------- contact card
def g_pin(th, x, y):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{th["accent"]}" stroke-width="2" stroke-linejoin="round">'
            '<path d="M11 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C18 14.8 11 21 11 21z"/><circle cx="11" cy="9.5" r="2.5"/></g>')


CHANNELS = [
    ("portfolio", g_globe, "PORTFOLIO", "keylorpineda.dev", SITE),
    ("email", g_mail, "EMAIL", EMAIL, f"mailto:{EMAIL}"),
    ("linkedin", g_linkedin, "LINKEDIN", "in/keylor-pineda", LINKEDIN),
    ("github", g_github, "GITHUB", f"@{USER}", f"https://github.com/{USER}"),
]


def contact(theme):
    th = THEMES[theme]
    W, H = 1000, 340
    b = [f'<clipPath id="card"><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="26"/></clipPath>', frame(W, H, th, 26)]
    b.append(f'<g clip-path="url(#card)">{sun(th, 800, 430, 300)}</g>')
    l1, t = letters("Let's build", 78, 48, 124, th["text"], "l", 0.1, tracking=-2)
    l2, t = letters("something.", 78, 48, 202, th["accent_big"], "l", t + 0.05, tracking=-2)
    b += [l1, l2]
    p, _ = paragraph("Have a project in mind, a question about something I built, or want to talk about cloud, "
                     "data or security? Write me, I'd like to hear about it.", 20, 50, 252, 560, th["muted"], leading=1.55)
    b.append(p)
    pill = "Costa Rica  ·  UTC−6"
    pw = tw(pill, 16, "medium") + 66
    b.append(f'<rect x="{fmt(W - 48 - pw)}" y="48" width="{fmt(pw)}" height="44" rx="14" fill="{th["card2"]}" stroke="{th["border"]}"/>')
    b.append(g_pin(th, W - 48 - pw + 18, 59))
    b.append(text(pill, 16, W - 48 - pw + 48, 75.5, th["text"], "medium"))
    style = (
        f".l{{transform-box:fill-box;transform-origin:0 100%;animation:letter 1.1s {EASE} backwards}}"
        "@keyframes letter{from{opacity:0;transform:translateY(40px) rotate(9deg)}}" + SUN_CSS + REDUCED
    )
    write("contact", theme, svg_doc(W, H, "".join(b), "Let's build something. Based in Costa Rica, UTC-6", style))
    for name, glyph, lab, val, _ in CHANNELS:
        tw_, th_ = 400, 112
        t = [f'<rect x="4" y="4" width="{tw_ - 8}" height="{th_ - 8}" rx="20" fill="{th["card"]}" stroke="{th["border"]}"/>']
        t.append(f'<rect x="22" y="22" width="40" height="40" rx="12" fill="{th["card2"]}" stroke="{th["border"]}"/>')
        t.append(glyph(th, 31, 31))
        t.append(text(lab, 12.5, 76, 47, th["faint"], "semibold", tracking=2))
        t.append(g_arrow(dict(th, accent=th["muted"]), tw_ - 46, 26))
        t.append(text(val, 15.5, 24, 89, th["text"], "medium"))
        write(f"contact-{name}", theme, svg_doc(tw_, th_, "".join(t), f"{lab.title()}: {val}"))


# --------------------------------------------------------------------------- about card
FACTS = [
    ("Based in", "Costa Rica"),
    ("Building", "HealthyCropping, offline crop disease detection"),
    ("Work across", "Web, Android, APIs and machine learning"),
    ("Learning", "AWS, Databricks and cybersecurity"),
    ("Certified", "Oracle Cloud (x2), Google Cloud, AWS GenAI"),
]


def about(theme):
    th = THEMES[theme]
    W = 1000
    rowh = 62
    H = 40 + rowh * len(FACTS) + 20
    b = [frame(W, H, th, 26)]
    for i, (k, v) in enumerate(FACTS):
        y = 40 + i * rowh
        if i:
            b.append(f'<path d="M40 {y}H{W-40}" stroke="{th["border"]}"/>')
        # an amber marker walks down the rows, one at a time
        b.append(f'<rect class="m" style="animation-delay:{i * 0.9:.1f}s" x="44" y="{y + 26}" width="9" height="13" rx="2" fill="{th["fill"]}"/>')
        b.append(text(k.upper(), 14, 66, y + 38, th["accent"], "semibold", tracking=2))
        b.append(text(v, 22, 262, y + 39, th["text"], "medium"))
    style = (
        f".m{{animation:mark {len(FACTS) * 0.9:.1f}s ease-in-out infinite}}"
        "@keyframes mark{0%,100%{opacity:.28}8%,18%{opacity:1}30%{opacity:.28}}" + REDUCED
    )
    write("about", theme, svg_doc(W, H, "".join(b), "At a glance: " + "; ".join(f"{k} {v}" for k, v in FACTS), style))


# --------------------------------------------------------------------------- interests
INTERESTS = [
    ("aws", "#FF9900", "AWS", "CLOUD ARCHITECTURE",
     "Where I want to grow next. I started with generative AI on AWS and I'm going deeper into the core services."),
    ("databricks", "#FF3621", "Databricks", "DATA ENGINEERING",
     "Data engineering at scale: Spark, Delta Lake and the lakehouse model behind modern data platforms."),
    ("shield", "#4C9BE8", "Cybersecurity", "NETWORK & APP SECURITY",
     "How systems get attacked, from the network to the application, so I can build ones that hold up."),
]


def interest(i, theme):
    slug, col, name, kind, desc = INTERESTS[i]
    th = THEMES[theme]
    W = 1000
    lines = wrap(desc, 21, 760)
    H = 120 + len(lines) * 32 + 22
    b = [f'<clipPath id="c"><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="24"/></clipPath>', frame(W, H, th, 24)]
    b.append(f'<rect clip-path="url(#c)" x="0" y="0" width="6" height="{H}" fill="{col}"/>')
    b.append(f'<rect x="40" y="36" width="88" height="88" rx="22" fill="{th["card2"]}" stroke="{th["border"]}"/>')
    if slug == "shield":
        b.append(f'<g transform="translate(62 58) scale(1.6)" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round">'
                 '<path d="M14 1.5 3 6v8c0 6.5 4.7 11 11 13 6.3-2 11-6.5 11-13V6z"/><path d="M9 14l3.6 3.6L19.5 10.5"/></g>')
    else:
        b.append(icon(slug, 62, 58, 44, th))
    b.append(text(kind, 14, 160, 62, col, "semibold", tracking=2.2))
    b.append(text(name, 34, 158, 102, th["text"], "display", tracking=-0.6))
    for j, ln in enumerate(lines):
        b.append(text(ln, 21, 160, 140 + j * 32, th["muted"]))
    write(f"interest-{slug}", theme, svg_doc(W, H, "".join(b), f"{name}: {desc}"))


# --------------------------------------------------------------------------- certifications
CERTS = [
    ("cert-oci-architect", "oracle", "Oracle Cloud Infrastructure Certified Architect Associate", "Oracle",
     "Issued Oct 2026  ·  Expires Oct 2028", "103563028OCI26CAA", ["Cloud-Native Architecture", "Network Security"]),
    ("cert-oci-ai", "oracle", "Oracle Cloud Infrastructure Certified AI Foundations Associate", "Oracle",
     "Issued Oct 2026  ·  Expires Oct 2028", "103563028OCI26AICFA", ["Artificial Intelligence", "Machine Learning"]),
    ("cert-gcp", "googleg", "Google Cloud Computing Foundations Certificate", "Google", "Issued Oct 2026", None,
     ["Google Cloud", "Big Data"]),
    ("cert-aws", "aws", "Advanced Generative AI Implementation on AWS", "Amazon Web Services", "Issued Sep 2025", None,
     ["Generative AI", "Machine Learning"]),
]


def cert(c, theme):
    name, slug, title, issuer, dates, cid, tags = c
    th = THEMES[theme]
    W = 1000
    tx = 168
    lines = wrap(title, 27, W - tx - 90, "semibold")
    y = 66
    b = []
    for ln in lines:
        b.append(text(ln, 27, tx, y, th["text"], "semibold"))
        y += 36
    y += 4
    b.append(text(issuer, 19, tx, y, th["text"], "medium"))
    b.append(text(dates, 19, tx + tw(issuer, 19, "medium") + 14, y, th["muted"]))
    if cid:
        y += 32
        b.append(text("Credential ID", 16, tx, y, th["faint"], "medium"))
        b.append(text(cid, 16, tx + tw("Credential ID", 16, "medium") + 10, y, th["muted"], "medium", tracking=0.8))
    y += 22
    cx = tx
    for tg in tags:
        ww = tw(tg, 15, "medium") + 30
        b.append(f'<rect x="{fmt(cx)}" y="{y}" width="{fmt(ww)}" height="34" rx="10" fill="{th["card2"]}" stroke="{th["border"]}"/>')
        b.append(text(tg, 15, cx + 15, y + 22, th["muted"], "medium"))
        cx += ww + 10
    H = y + 34 + 38
    body = [frame(W, H, th, 24)]
    body.append(f'<rect x="40" y="40" width="96" height="96" rx="24" fill="{th["card2"]}" stroke="{th["border"]}"/>')
    body.append(icon(slug, 64, 64, 48, th))
    body.append(f'<g transform="translate({W-70} 36)"><circle cx="15" cy="15" r="15" fill="{th["accent"]}" opacity=".16"/>'
                f'<path d="M8.5 15.3l4.2 4.2 8.4-8.7" fill="none" stroke="{th["accent"]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></g>')
    write(name, theme, svg_doc(W, H, "".join(body + b), f"{title}, {issuer}, {dates}"))


# --------------------------------------------------------------------------- toolbox
TOOLBOX = [
    ("Languages", ["typescript", "javascript", "python", "java", "gnubash", "sql"]),
    ("Frontend & mobile", ["react", "reactnative", "expo", "angular", "vite", "tailwindcss", "reactquery", "zod"]),
    ("Backend", ["nestjs", "nodedotjs", "fastapi", "springboot", "graphql", "prisma", "typeorm", "sqlalchemy", "pydantic"]),
    ("Data & AI", ["tensorflow", "keras", "tflite", "numpy", "pandas", "scikitlearn", "googlegemini", "kaggle"]),
    ("Databases", ["postgresql", "mariadb", "sqlite", "neon", "firebase"]),
    ("Cloud & DevOps", ["oracle", "googlecloud", "aws", "docker", "githubactions", "vercel", "render", "cloudinary", "linux"]),
    ("Quality & workflow", ["jest", "vitest", "playwright", "pytest", "ruff", "uv", "pnpm", "git", "postman"]),
]


# --------------------------------------------------------------------------- README
def heading(i):
    return pic(f"section-{i}", SECTIONS[i - 1], width="100%")


def readme():
    md = []
    md.append(f'<a href="{SITE}">{pic("header", "Keylor Pineda, software developer from Costa Rica. The full portfolio is at keylorpineda.dev", width="100%")}</a>')
    md.append("")
    md.append('<p align="center">')
    md.append(f'  <a href="mailto:{EMAIL}">{pic("btn-email", f"Email {EMAIL}", height=46)}</a>')
    md.append(f'  <a href="{LINKEDIN}">{pic("btn-linkedin", "LinkedIn", height=46)}</a>')
    md.append("</p>")
    md.append("")
    md.append(heading(1))
    md.append("")
    md.append("I'm Keylor, a software developer from Costa Rica. I like building complete products: the database, the API, "
              "the interface, and the tests and CI that keep everything working.")
    md.append("")
    md.append("Right now most of my time goes into **HealthyCropping**, an Android app that recognizes coffee, cacao and banana diseases from "
              "a photo without an internet connection. Before that I built **Booth**, a catalog and ordering tool for small "
              "shops that sell through WhatsApp, and a **RAG engine** that answers questions using only the documents you give it.")
    md.append("")
    md.append("Outside of the code I'm studying cloud and security, which is where the certifications below come from.")
    md.append("")
    md.append(f"Everything here, with live captures of each project, is at **[keylorpineda.dev]({SITE})**.")
    md.append("")
    md.append(pic("about", "At a glance", width="100%"))
    md.append("")
    md.append(heading(2))
    for p in PROJECTS:
        md.append("")
        img = pic(f"project-{p['name']}", f"{p['title']}: {p['tagline']}", width="100%")
        md.append(f'<a href="{p["url"]}">{img}</a>' if p["url"] else img)
        md.append("")
        md.append(p["desc"])
        md.append("")
        md.append('<p>')
        md.append(chips_md(p["tools"]))
        md.append('</p>')
        if p["buttons"]:
            md.append("")
            md.append("<p>")
            for name, label, url in p["buttons"]:
                md.append(f'<a href="{url}">{pic("btn-" + name.split("-")[0], label, height=46)}</a>')
            md.append("</p>")
        md.append("")
        md.append("<br>")
    md.append("")
    md.append(heading(3))
    md.append("")
    for c in CERTS:
        md.append(f'<a href="{LINKEDIN}/details/certifications/">{pic(c[0], c[2], width="100%")}</a>')
        md.append("")
    md.append(heading(4))
    md.append("")
    md.append("Pulled from the GitHub API and refreshed every day.")
    md.append("")
    activity = [
        ("activity-stats", "Contribution totals and streaks"),
        ("activity-calendar", "Contribution calendar for the last year"),
        ("activity-months", "Contributions per month over the last year"),
        ("activity-breakdown", "Commits, pull requests, reviews and issues in the last 12 months"),
        ("activity-repos", "My most active repositories in the last 12 months"),
        ("activity-languages", "Top languages across public repositories"),
    ]
    for i, (name, alt) in enumerate(activity):
        if i == 3:
            md.append("<details>")
            md.append("<summary><b>More activity: breakdown, most active repositories and languages</b></summary>")
            md.append("<br>")
            md.append("")
        md.append(pic(name, alt, width="100%", base=RAW).replace(".svg", f".svg?v={STAMP}"))
        md.append("")
    md.append("</details>")
    md.append("")
    md.append(heading(5))
    md.append("")
    md.append("<details>")
    md.append("<summary><b>Languages, frameworks, data, cloud and tooling I work with</b></summary>")
    md.append("<br>")
    md.append("")
    for cat, slugs in TOOLBOX:
        md.append(f"**{cat}**")
        md.append("")
        md.append(chips_md(slugs))
        md.append("")
    md.append("</details>")
    md.append("")
    md.append(heading(6))
    md.append("")
    md.append("<details>")
    md.append("<summary><b>AWS, Databricks and cybersecurity</b></summary>")
    md.append("<br>")
    md.append("")
    for slug, _, name, *_ in INTERESTS:
        md.append(pic(f"interest-{slug}", name, width="100%"))
        md.append("")
    md.append("</details>")
    md.append("")
    md.append(heading(7))
    md.append("")
    contact_card = pic("contact", "Let's build something. Based in Costa Rica", width="100%")
    md.append(f'<a href="mailto:{EMAIL}">{contact_card}</a>')
    md.append("")
    md.append('<p align="center">')
    for name, _, lab, val, url in CHANNELS:
        md.append(f'  <a href="{url}">{pic("contact-" + name, f"{lab.title()}: {val}", width=400)}</a>')
    md.append("</p>")
    md.append("")
    md.append(f'<p align="center"><sub>Thanks for stopping by. The rest is at <a href="{SITE}">keylorpineda.dev</a>.</sub></p>')
    md.append("")
    (ROOT / "README.md").write_text("\n".join(md), encoding="utf-8", newline="\n")


def main():
    if ASSETS.exists():
        shutil.rmtree(ASSETS)
    (ASSETS / "chips").mkdir(parents=True)
    readme()  # collects which chips are used
    for theme in THEME_NAMES:
        header(theme)
        for i in range(len(SECTIONS)):
            section(i, theme)
        about(theme)
        for p in PROJECTS:
            banner(p, theme)
        for i in range(len(INTERESTS)):
            interest(i, theme)
        for c in CERTS:
            cert(c, theme)
        button("email", theme, EMAIL, g_mail)
        button("linkedin", theme, "LinkedIn", g_linkedin)
        contact(theme)
        button("demo", theme, "Live demo", g_arrow, primary=True)
        button("source", theme, "Source code", g_github)
        for s in USED_CHIPS:
            (ASSETS / "chips" / f"{s}-{theme}.svg").write_text(chip_svg(s, theme, LABELS.get(s)), encoding="utf-8", newline="\n")
    print("assets:", sum(1 for _ in ASSETS.rglob("*.svg")))


if __name__ == "__main__":
    main()
