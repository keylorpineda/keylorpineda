"""Builds every static asset in assets/ and writes README.md.

Usage: python scripts/build.py
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from svglib import THEMES, fmt, icon, label_of, paragraph, rng, svg_doc, text, tw, wrap  # noqa: E402
from visuals import v_booth, v_doomsday, v_healthy, v_rag  # noqa: E402

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "assets"
USER = "keylorpineda"
EMAIL = "keylorpineda729@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/keylor-pineda"
RAW = f"https://raw.githubusercontent.com/{USER}/{USER}/output"
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
THEME_NAMES = ("dark", "light")


def write(name, theme, svg):
    (ASSETS / f"{name}-{theme}.svg").write_text(svg)


def pic(name, alt, width=None, height=None, base="assets"):
    size = (f' width="{width}"' if width else "") + (f' height="{height}"' if height else "")
    return (
        f'<picture><source media="(prefers-color-scheme: dark)" srcset="{base}/{name}-dark.svg">'
        f'<img src="{base}/{name}-light.svg" alt="{alt}"{size}></picture>'
    )


def frame(w, h, th, rx=22):
    return f'<rect x=".5" y=".5" width="{fmt(w-1)}" height="{fmt(h-1)}" rx="{rx}" fill="{th["card"]}" stroke="{th["border"]}"/>'


# --------------------------------------------------------------------------- header
K = ["X...X", "X..X.", "X.X..", "XX...", "X.X..", "X..X.", "X...X"]
P = ["XXXX.", "X...X", "X...X", "XXXX.", "X....", "X....", "X...."]


def header(theme):
    th = THEMES[theme]
    W, H = 1000, 470
    b = [frame(W, H, th, 26)]
    b.append(text("SOFTWARE DEVELOPER", 15, 56, 84, th["accent"], "semibold", tracking=2.6))
    x2 = 56 + tw("SOFTWARE DEVELOPER", 15, "semibold", 2.6) + 16
    b.append(f'<circle cx="{fmt(x2)}" cy="79" r="2.5" fill="{th["faint"]}"/>')
    b.append(text("COSTA RICA", 15, x2 + 16, 84, th["muted"], "semibold", tracking=2.6))
    b.append(text("Keylor", 96, 50, 182, th["text"], "display", tracking=-2.6))
    b.append(text("Pineda", 96, 50, 274, th["text"], "display", tracking=-2.6))
    p, _ = paragraph("I build full-stack products and machine learning that runs right on a phone.",
                     22, 56, 330, 470, th["muted"], leading=1.5)
    b.append(p)
    label = "Now building HealthyCropping"
    pw = tw(label, 17, "medium") + 62
    b.append(f'<rect x="56" y="388" width="{fmt(pw)}" height="44" rx="22" fill="{th["card2"]}" stroke="{th["border"]}"/>')
    b.append(f'<circle class="halo" cx="82" cy="410" r="10" fill="#3FA163" opacity=".25"/>')
    b.append('<circle cx="82" cy="410" r="5" fill="#3FA163"/>')
    b.append(text("Now building", 17, 102, 416, th["muted"], "medium"))
    b.append(text("HealthyCropping", 17, 102 + tw("Now building ", 17, "medium"), 416, th["text"], "medium"))

    # KP monogram drawn as a contribution grid
    R = rng(11)
    rows, cols, step, cell = 9, 13, 31, 25
    gx = W - 52 - (cols * step - (step - cell))
    gy = (H - (rows * step - (step - cell))) / 2
    for c in range(cols):
        for r in range(rows):
            lit = False
            if 1 <= r <= 7:
                if 1 <= c <= 5:
                    lit = K[r - 1][c - 1] == "X"
                elif 7 <= c <= 11:
                    lit = P[r - 1][c - 7] == "X"
            x, y = gx + c * step, gy + r * step
            if lit:
                op = R.choice([0.9, 1, 1])
                b.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{cell}" height="{cell}" rx="6" fill="{th["accent"]}" opacity="{op}"/>')
            else:
                faint = R.random() < 0.05
                fill, op = (th["accent"], 0.18) if faint else (th["cell"], 1)
                b.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{cell}" height="{cell}" rx="6" fill="{fill}" opacity="{op}"/>')
            delay = (c * 0.09 + r * 0.05)
            if not lit:
                b.append(f'<rect class="w" style="animation-delay:{delay:.2f}s" x="{fmt(x)}" y="{fmt(y)}" width="{cell}" height="{cell}" rx="6" fill="{th["accent"]}" opacity="0"/>')
    style = (
        ".w{animation:wave 8s ease-in-out infinite}"
        "@keyframes wave{0%,100%{opacity:0}7%{opacity:.3}16%{opacity:0}}"
        ".halo{transform-box:fill-box;transform-origin:center;animation:halo 2.4s ease-out infinite}"
        "@keyframes halo{0%{transform:scale(.6);opacity:.5}100%{transform:scale(2);opacity:0}}" + REDUCED
    )
    write("header", theme, svg_doc(W, H, "".join(b), "Keylor Pineda, software developer from Costa Rica", style))


# --------------------------------------------------------------------------- buttons
def g_mail(th, x, y):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{th["accent"]}" stroke-width="2" stroke-linejoin="round">'
            '<rect x="1" y="3" width="20" height="15" rx="3"/><path d="M2 5l9 7 9-7" stroke-linecap="round"/></g>')


def g_linkedin(th, x, y):
    return (f'<g transform="translate({x} {y}) scale(.9167)"><rect width="24" height="24" rx="5" fill="#0A66C2"/>'
            '<rect x="5" y="9.5" width="3.2" height="9.5" fill="#fff"/><circle cx="6.6" cy="6.2" r="1.9" fill="#fff"/>'
            '<path d="M10.6 9.5h3.1v1.4c.5-.9 1.6-1.7 3.2-1.7 3 0 3.6 1.9 3.6 4.5V19h-3.2v-4.6c0-1.2 0-2.6-1.6-2.6s-1.9 1.2-1.9 2.5V19h-3.2z" fill="#fff"/></g>')


def g_github(th, x, y):
    return icon("github", x, y, 22, th)


def g_arrow(th, x, y):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{th["accent"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M5 17L17 5M8 5h9v9"/></g>')


def button(name, theme, label, glyph, primary=False):
    th = THEMES[theme]
    H = 46
    W = tw(label, 15.5, "semibold") + 82  # noqa
    fill = th["text"] if primary else th["card"]
    fg = th["card"] if primary else th["text"]
    tht = dict(th, accent=th["card"] if primary else th["accent"], text=fg)
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
          "oracle": "Oracle Cloud", "aws": "AWS", "groq": "Groq", "meta": "Llama 3.3", "cohere": "Cohere"}
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
        desc="Point a phone at a coffee leaf and get a diagnosis right there in the plot. A MobileNetV3 model trained on "
        "public coffee datasets runs on the device through TensorFlow Lite, and scans, farms and plots are stored locally "
        "first. Cacao and banana models come next, along with a Gemini RAG layer that explains what to do and cites "
        "official agronomy manuals.",
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
        tagline="Answers grounded only in the documents you upload.",
        status="Open source", visual=v_rag, url=f"https://github.com/{USER}/RAG-Research-Engine",
        desc="Upload documents, ask in any language and get answers based only on what you uploaded. When the context "
        "doesn't hold the answer, it says so instead of making one up. Retrieval favors more recent files, the context is "
        "capped at 4,000 tokens, and every answer shows the passages it came from.",
        tools=["python", "fastapi", "postgresql", "sqlalchemy", "cohere", "groq", "meta", "docker"],
        buttons=[("source-rag", "Source code", f"https://github.com/{USER}/RAG-Research-Engine")],
    ),
    dict(
        name="doomsday", accent="#E0234E", kicker="FULL STACK  ·  API + DASHBOARD", title="Doomsday System",
        tagline="Camps, survivors and supplies in a post-apocalyptic world.",
        status="Full stack", visual=v_doomsday, url=None,
        desc="A management platform for camps, survivors, supplies and the transfers between outposts. The interesting part "
        "is the rules engine, which refuses impossible moves like shipping water a camp doesn't have. NestJS API, React "
        "dashboard, and end to end tests with Playwright on both sides.",
        tools=["nestjs", "typescript", "typeorm", "postgresql", "react", "vite", "tailwindcss", "python", "jest", "playwright", "docker"],
        buttons=[],
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
    write(f"project-{p['name']}", theme, svg_doc(W, H, "".join(b), f"{p['title']}: {p['tagline']}", style + REDUCED))


# --------------------------------------------------------------------------- contact card
def g_pin(th, x, y):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{th["accent"]}" stroke-width="2" stroke-linejoin="round">'
            '<path d="M11 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C18 14.8 11 21 11 21z"/><circle cx="11" cy="9.5" r="2.5"/></g>')


CHANNELS = [
    ("email", g_mail, "EMAIL", EMAIL, f"mailto:{EMAIL}"),
    ("linkedin", g_linkedin, "LINKEDIN", "in/keylor-pineda", LINKEDIN),
    ("github", g_github, "GITHUB", f"@{USER}", f"https://github.com/{USER}"),
]


def contact(theme):
    th = THEMES[theme]
    W, H = 1000, 300
    b = [frame(W, H, th, 26)]
    b.append(text("CONTACT", 15, 48, 78, th["accent"], "semibold", tracking=2.6))
    b.append(text("Let's talk", 52, 46, 140, th["text"], "display", tracking=-1.4))
    p, _ = paragraph("Have a project in mind, a question about something I built, or want to talk about cloud, "
                     "data or security? Write me, I'd like to hear about it.", 21, 48, 190, 560, th["muted"], leading=1.55)
    b.append(p)
    pill = "Costa Rica  ·  UTC−6"
    pw = tw(pill, 16, "medium") + 66
    b.append(f'<rect x="{fmt(W - 48 - pw)}" y="56" width="{fmt(pw)}" height="44" rx="22" fill="{th["card2"]}" stroke="{th["border"]}"/>')
    b.append(g_pin(th, W - 48 - pw + 18, 67))
    b.append(text(pill, 16, W - 48 - pw + 48, 83.5, th["text"], "medium"))
    write("contact", theme, svg_doc(W, H, "".join(b), "Let's talk. Based in Costa Rica, UTC-6"))
    for name, glyph, lab, val, _ in CHANNELS:
        tw_, th_ = 268, 112
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
        b.append(text(k.upper(), 14, 44, y + 38, th["accent"], "semibold", tracking=2))
        b.append(text(v, 22, 250, y + 39, th["text"], "medium"))
    write("about", theme, svg_doc(W, H, "".join(b), "At a glance: " + "; ".join(f"{k} {v}" for k, v in FACTS)))


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
    ("Frontend & mobile", ["react", "reactnative", "expo", "vite", "tailwindcss", "reactquery", "zod"]),
    ("Backend", ["nestjs", "nodedotjs", "fastapi", "springboot", "graphql", "prisma", "typeorm", "sqlalchemy", "pydantic"]),
    ("Data & AI", ["tensorflow", "keras", "tflite", "numpy", "pandas", "scikitlearn", "googlegemini", "kaggle"]),
    ("Databases", ["postgresql", "mariadb", "sqlite", "neon", "firebase"]),
    ("Cloud & DevOps", ["oracle", "googlecloud", "aws", "docker", "githubactions", "vercel", "render", "cloudinary", "linux"]),
    ("Quality & workflow", ["jest", "vitest", "playwright", "pytest", "ruff", "uv", "pnpm", "git", "postman"]),
]


# --------------------------------------------------------------------------- README
def readme():
    md = []
    md.append(pic("header", "Keylor Pineda, software developer from Costa Rica", width="100%"))
    md.append("")
    md.append('<p align="center">')
    md.append(f'  <a href="mailto:{EMAIL}">{pic("btn-email", f"Email {EMAIL}", height=46)}</a>')
    md.append(f'  <a href="{LINKEDIN}">{pic("btn-linkedin", "LinkedIn", height=46)}</a>')
    md.append(f'  <a href="https://github.com/{USER}?tab=repositories">{pic("btn-repos", "Repositories", height=46)}</a>')
    md.append("</p>")
    md.append("")
    md.append("## About me")
    md.append("")
    md.append("I'm Keylor, a software developer from Costa Rica. I like building complete products: the database, the API, "
              "the interface, and the tests and CI that keep everything working.")
    md.append("")
    md.append("Right now most of my time goes into **HealthyCropping**, an Android app that recognizes coffee diseases from "
              "a photo without an internet connection. Before that I built **Booth**, a catalog and ordering tool for small "
              "shops that sell through WhatsApp, and a **RAG engine** that answers questions using only the documents you give it.")
    md.append("")
    md.append("Outside of the code I'm studying cloud and security, which is where the certifications below come from.")
    md.append("")
    md.append(pic("about", "At a glance", width="100%"))
    md.append("")
    md.append("## Selected work")
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
    md.append("<details>")
    md.append("<summary><b>A few more things I've built</b></summary>")
    md.append("<br>")
    md.append("")
    md.append(f"**[Non-Profit Intel Scraper](https://github.com/{USER}/nonprofit_intel_scraper)**  ")
    md.append("Scrapes nonprofit directories, enriches them with IRS 990 data and has Gemini score which ones are worth a sales call, and why.")
    md.append("")
    md.append(chips_md(["python", "playwright", "googlegemini", "pydantic"]))
    md.append("")
    md.append(f"**[HealthyHabits API](https://github.com/{USER}/HealthyHabits-API)**  ")
    md.append("GraphQL API for routines, habits and progress tracking, with JWT auth and role based permissions.")
    md.append("")
    md.append(chips_md(["java", "springboot", "graphql", "mariadb", "docker"]))
    md.append("")
    md.append("</details>")
    md.append("")
    md.append("## Toolbox")
    md.append("")
    for cat, slugs in TOOLBOX:
        md.append(f"**{cat}**")
        md.append("")
        md.append(chips_md(slugs))
        md.append("")
    md.append("## Where I'm heading")
    md.append("")
    for slug, *_ in INTERESTS:
        md.append(pic(f"interest-{slug}", INTERESTS[[i[0] for i in INTERESTS].index(slug)][2], width="100%"))
        md.append("")
    md.append("## Certifications")
    md.append("")
    for c in CERTS:
        md.append(f'<a href="{LINKEDIN}/details/certifications/">{pic(c[0], c[2], width="100%")}</a>')
        md.append("")
    md.append("## Activity")
    md.append("")
    md.append("Pulled from the GitHub API and refreshed every day.")
    md.append("")
    for name, alt in (("activity-stats", "Contribution totals and streaks"), ("activity-calendar", "Contribution calendar for the last year"),
                      ("activity-breakdown", "Commits, pull requests, reviews and issues in the last 12 months"),
                      ("activity-languages", "Top languages across public repositories")):
        md.append(pic(name, alt, width="100%", base=RAW))
        md.append("")
    md.append("## Contact")
    md.append("")
    md.append(f'<a href="mailto:{EMAIL}">{pic("contact", "Let\'s talk. Based in Costa Rica", width="100%")}</a>')
    md.append("")
    md.append('<p align="center">')
    for name, _, lab, val, url in CHANNELS:
        md.append(f'  <a href="{url}">{pic("contact-" + name, f"{lab.title()}: {val}", width=268)}</a>')
    md.append("</p>")
    md.append("")
    md.append('<p align="center"><sub>Thanks for stopping by.</sub></p>')
    md.append("")
    (ROOT / "README.md").write_text("\n".join(md))


def main():
    if ASSETS.exists():
        shutil.rmtree(ASSETS)
    (ASSETS / "chips").mkdir(parents=True)
    readme()  # collects which chips are used
    for theme in THEME_NAMES:
        header(theme)
        about(theme)
        for p in PROJECTS:
            banner(p, theme)
        for i in range(len(INTERESTS)):
            interest(i, theme)
        for c in CERTS:
            cert(c, theme)
        button("email", theme, EMAIL, g_mail)
        button("linkedin", theme, "LinkedIn", g_linkedin)
        button("repos", theme, "All repositories", g_github)
        contact(theme)
        button("demo", theme, "Live demo", g_arrow, primary=True)
        button("source", theme, "Source code", g_github)
        for s in USED_CHIPS:
            (ASSETS / "chips" / f"{s}-{theme}.svg").write_text(chip_svg(s, theme, LABELS.get(s)))
    print("assets:", sum(1 for _ in ASSETS.rglob("*.svg")))


if __name__ == "__main__":
    main()
