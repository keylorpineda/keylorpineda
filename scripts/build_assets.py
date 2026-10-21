import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from svglib import THEMES, chips, fmt, frame, icon, paragraph, rng, svg_doc, text, tw, wrap  # noqa: E402

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent.parent / "assets")
OUT.mkdir(parents=True, exist_ok=True)

REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def write(name, theme, svg):
    (OUT / f"{name}-{theme}.svg").write_text(svg)


# --------------------------------------------------------------------------- header
def header(theme):
    th = THEMES[theme]
    W, H = 1200, 400
    b = [frame(W, H, th, 24)]
    b.append(text("SOFTWARE DEVELOPER", 13, 64, 88, th["accent"], "semibold", tracking=2.4))
    x2 = 64 + tw("SOFTWARE DEVELOPER", 13, "semibold", 2.4) + 16
    b.append(f'<circle cx="{fmt(x2)}" cy="83.5" r="2.2" fill="{th["faint"]}"/>')
    b.append(text("COSTA RICA", 13, x2 + 16, 88, th["muted"], "semibold", tracking=2.4))
    b.append(text("Keylor Pineda", 74, 60, 172, th["text"], "display", tracking=-1.6))
    p, ph = paragraph(
        "I build complete products, from the database and the API to the interface and the "
        "tests around them. Lately that includes machine learning models that run right on a phone.",
        20, 64, 224, 590, th["muted"], leading=1.55,
    )
    b.append(p)
    # now building
    y = 338
    b.append(f'<rect x="64" y="{y-25}" width="{fmt(tw("Now building HealthyCropping, offline crop disease detection", 15, "medium") + 58)}" height="38" rx="19" fill="{th["card2"]}" stroke="{th["border"]}"/>')
    b.append(f'<circle cx="86" cy="{y-6}" r="9" fill="#3FA163" opacity=".25" class="halo"/>')
    b.append(f'<circle cx="86" cy="{y-6}" r="4.5" fill="#3FA163"/>')
    b.append(text("Now building", 15, 104, y - 1, th["muted"], "medium"))
    b.append(text("HealthyCropping, offline crop disease detection", 15, 104 + tw("Now building ", 15, "medium"), y - 1, th["text"], "medium"))

    # contribution style grid
    R = rng(7)
    cols, rows, cell, step = 13, 7, 20, 26
    gx = 700 + (436 - (cols * step - 6)) / 2
    gy = 112
    levels = [th["cell"]] + [th["accent"]] * 4
    ops = [1, 0.28, 0.5, 0.74, 1]
    cells = []
    for c in range(cols):
        for r in range(rows):
            weight = 0.35 + 0.65 * (c / cols)
            v = R.random() * weight
            lv = 0 if v < 0.16 else 1 if v < 0.3 else 2 if v < 0.45 else 3 if v < 0.6 else 4
            x, yy = gx + c * step, gy + r * step
            cells.append(f'<rect x="{fmt(x)}" y="{fmt(yy)}" width="{cell}" height="{cell}" rx="5" fill="{levels[lv]}" opacity="{ops[lv]}"/>')
            delay = (c + r) * 0.11
            cells.append(f'<rect class="w" style="animation-delay:{delay:.2f}s" x="{fmt(x)}" y="{fmt(yy)}" width="{cell}" height="{cell}" rx="5" fill="{th["accent"]}" opacity="0"/>')
    b += cells
    style = (
        ".w{animation:wave 9s ease-in-out infinite}"
        "@keyframes wave{0%,100%{opacity:0}6%{opacity:.85}16%{opacity:0}}"
        ".halo{transform-box:fill-box;transform-origin:center;animation:halo 2.4s ease-out infinite}"
        "@keyframes halo{0%{transform:scale(.6);opacity:.5}100%{transform:scale(2);opacity:0}}" + REDUCED
    )
    write("header", theme, svg_doc(W, H, "".join(b), "Keylor Pineda, software developer from Costa Rica", style))


# --------------------------------------------------------------------------- project cards
def card(name, theme, accent, kicker, title, desc, tools, status, visual, labels=None):
    th = THEMES[theme]
    W = 1200
    L, LW = 64, 548
    b = []
    b.append(text(kicker, 12.5, L, 92, accent, "semibold", tracking=2.2))
    b.append(text(title, 44, L - 2, 150, th["text"], "display", tracking=-0.9))
    p, ph = paragraph(desc, 18, L, 196, LW, th["muted"], leading=1.6)
    b.append(p)
    y = 196 + ph + 14
    b.append(text("BUILT WITH", 11.5, L, y, th["faint"], "semibold", tracking=2))
    c, chh = chips(tools, L, y + 16, LW, th, h=34, fs=14, gap=9, labels=labels)
    b.append(c)
    content_bottom = y + 16 + chh
    H = max(int(content_bottom + 64), 470)
    shift = max((H - (content_bottom - 70)) / 2 - 70 - 4, 0) if H == 470 else 0
    b = [f'<g transform="translate(0 {fmt(shift)})">'] + b + ["</g>"]
    # status pill
    sw = tw(status, 13, "medium") + 40
    b.append(f'<rect x="{fmt(L)}" y="{H-58}" width="0" height="0"/>')
    vx, vy, vw, vh = 680, 40, 480, H - 80
    b.append(f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="18" fill="{th["card2"]}" stroke="{th["border"]}"/>')
    vis, style = visual(th, accent, vx, vy, vw, vh)
    b.append(vis)
    px = vx + vw - 18 - sw
    b.append(f'<rect x="{fmt(px)}" y="{vy+18}" width="{fmt(sw)}" height="30" rx="15" fill="{th["card"]}" stroke="{th["border"]}"/>')
    b.append(f'<circle cx="{fmt(px+16)}" cy="{vy+33}" r="4" fill="{accent}"/>')
    b.append(text(status, 13, px + 27, vy + 37.5, th["text"], "medium"))
    body = frame(W, H, th, 24) + "".join(b)
    write(f"project-{name}", theme, svg_doc(W, H, body, f"{title}: {desc}", style + REDUCED))


def v_healthy(th, accent, x, y, w, h):
    cx = x + w / 2
    pw, phh = 214, min(h - 56, 330)
    px, py = cx - pw / 2, y + (h - phh) / 2 + 6
    b = []
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{phh}" rx="30" fill="{th["card"]}" stroke="{th["border"]}" stroke-width="1.5"/>')
    b.append(f'<rect x="{cx-28}" y="{py+12}" width="56" height="6" rx="3" fill="{th["border"]}"/>')
    # leaf
    lx, ly = cx, py + 120
    leaf = "M0 -88 C 52 -60 62 10 0 86 C -62 10 -52 -60 0 -88 Z"
    b.append(f'<g transform="translate({lx} {ly}) rotate(-18)">')
    b.append(f'<path d="{leaf}" fill="#3FA163"/>')
    b.append('<path d="M0 -84 L0 92" stroke="#2C7A48" stroke-width="2.4" stroke-linecap="round"/>')
    for i, yy in enumerate((-50, -22, 6, 34)):
        sp = 36 - i * 4
        b.append(f'<path d="M0 {yy} Q {sp*0.6} {yy-12} {sp} {yy-26}" fill="none" stroke="#2C7A48" stroke-width="1.6"/>')
        b.append(f'<path d="M0 {yy} Q {-sp*0.6} {yy-12} {-sp} {yy-26}" fill="none" stroke="#2C7A48" stroke-width="1.6"/>')
    for sx, sy, r in ((16, -30, 7), (24, -12, 4.5), (-18, 14, 6), (-8, 40, 4), (14, 26, 5.5), (-22, -40, 3.5)):
        b.append(f'<circle cx="{sx}" cy="{sy}" r="{r}" fill="#E0962E" opacity=".9"/>')
        b.append(f'<circle cx="{sx}" cy="{sy}" r="{r*1.7}" fill="#E0962E" opacity=".22"/>')
    b.append("</g>")
    # scan brackets
    bx0, by0, bx1, by1 = cx - 84, ly - 96, cx + 84, ly + 96
    s = 18
    for (ax, ay, dx, dy) in ((bx0, by0, 1, 1), (bx1, by0, -1, 1), (bx0, by1, 1, -1), (bx1, by1, -1, -1)):
        b.append(f'<path d="M{ax} {ay+dy*s} L{ax} {ay} L{ax+dx*s} {ay}" fill="none" stroke="{th["text"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>')
    b.append(f'<rect class="scan" x="{bx0+6}" y="{by0}" width="{bx1-bx0-12}" height="2.5" rx="1.25" fill="{accent}"/>')
    # result card
    ry = py + phh - 92
    b.append(f'<rect x="{px+14}" y="{ry}" width="{pw-28}" height="78" rx="14" fill="{th["card2"]}" stroke="{th["border"]}"/>')
    b.append(text("Leaf rust", 15, px + 28, ry + 26, th["text"], "semibold"))
    b.append(text("Act now", 11.5, px + pw - 28, ry + 26, "#E0962E", "semibold", "end"))
    b.append(text("Coffee  ·  severity", 12, px + 28, ry + 46, th["muted"]))
    b.append(f'<rect x="{px+28}" y="{ry+58}" width="{pw-56}" height="6" rx="3" fill="{th["border"]}"/>')
    b.append(f'<rect class="bar" x="{px+28}" y="{ry+58}" width="{(pw-56)*0.62}" height="6" rx="3" fill="#E0962E"/>')
    # floating badges
    def badge(bx, by, label, glyph):
        bw = tw(label, 13, "medium") + 46
        return (
            f'<g><rect x="{bx}" y="{by}" width="{fmt(bw)}" height="34" rx="17" fill="{th["card"]}" stroke="{th["border"]}"/>'
            + glyph(bx + 14, by + 9)
            + text(label, 13, bx + 36, by + 22, th["text"], "medium")
            + "</g>", bw
        )

    def nosignal(gx, gy):
        return (
            f'<g transform="translate({gx} {gy})" fill="none" stroke="{th["muted"]}" stroke-width="1.8" stroke-linecap="round">'
            '<path d="M1 6.5a11 11 0 0 1 14 0"/><path d="M4 10a6.5 6.5 0 0 1 8 0"/><circle cx="8" cy="13.5" r=".8" fill="currentColor"/>'
            f'<path d="M1.5 1.5l13 14" stroke="{accent}"/></g>'
        )

    def book(gx, gy):
        return (
            f'<g transform="translate({gx} {gy})" fill="none" stroke="{th["muted"]}" stroke-width="1.7" stroke-linejoin="round">'
            '<path d="M1 2.5h5a2.5 2.5 0 0 1 2.5 2.5v11a2 2 0 0 0-2-2H1z"/><path d="M16 2.5h-5A2.5 2.5 0 0 0 8.5 5v11a2 2 0 0 1 2-2H16z"/></g>'
        )

    g1, w1 = badge(x + 22, py + 64, "Works offline", nosignal)
    g2, w2 = badge(x + w - 22 - (tw("Runs on device", 13, "medium") + 46), py + 196, "Runs on device", book)
    b += [g1, g2]
    style = (
        f".scan{{animation:scan 3.2s ease-in-out infinite}}"
        f"@keyframes scan{{0%{{transform:translateY(8px);opacity:0}}10%{{opacity:1}}50%{{transform:translateY({by1-by0-10}px);opacity:1}}60%{{opacity:0}}100%{{transform:translateY({by1-by0-10}px);opacity:0}}}}"
    )
    return "".join(b), style


def v_booth(th, accent, x, y, w, h):
    b = []
    # storefront window
    sx, sy, sw, sh = x + 28, y + 64, 300, h - 104
    b.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="14" fill="{th["card"]}" stroke="{th["border"]}"/>')
    for i, c in enumerate(("#E5534B", "#E3A857", "#3FA163")):
        b.append(f'<circle cx="{sx+18+i*14}" cy="{sy+18}" r="4" fill="{c}" opacity=".8"/>')
    b.append(f'<rect x="{sx+66}" y="{sy+11}" width="{sw-84}" height="14" rx="7" fill="{th["card2"]}"/>')
    b.append(text("booth.app/s/panaderia", 9.5, sx + 76, sy + 21.5, th["muted"], "medium"))
    b.append(f'<rect x="{sx+16}" y="{sy+40}" width="34" height="34" rx="10" fill="{accent}"/>')
    b.append(text("Panadería La Esquina", 14, sx + 60, sy + 55, th["text"], "semibold"))
    b.append(text("Open until 7 pm", 11, sx + 60, sy + 71, th["muted"]))
    items = [("Pan de yema", "₡1,200", "#D9A35B"), ("Café chorreado", "₡1,500", "#7A5236"), ("Empanada", "₡900", "#C9853F"), ("Tres leches", "₡2,100", "#EADBC4")]
    iw, ih = (sw - 44) / 2, 92
    for i, (n, pr, col) in enumerate(items):
        ix = sx + 16 + (i % 2) * (iw + 12)
        iy = sy + 90 + (i // 2) * (ih + 12)
        if iy + ih > sy + sh - 10:
            break
        b.append(f'<rect x="{fmt(ix)}" y="{iy}" width="{fmt(iw)}" height="{ih}" rx="10" fill="{th["card2"]}" stroke="{th["border"]}"/>')
        b.append(f'<rect x="{fmt(ix+8)}" y="{iy+8}" width="{fmt(iw-16)}" height="42" rx="7" fill="{col}" opacity=".85"/>')
        b.append(text(n, 11.5, ix + 10, iy + 68, th["text"], "semibold"))
        b.append(text(pr, 11, ix + 10, iy + 84, th["muted"], "medium"))
        b.append(f'<circle cx="{fmt(ix+iw-18)}" cy="{iy+78}" r="9" fill="{accent}"/>')
        b.append(f'<path d="M{fmt(ix+iw-22)} {iy+78}h8M{fmt(ix+iw-18)} {iy+74}v8" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>')
    # whatsapp bubble
    bub_fill = "#144D37" if th is THEMES["dark"] else "#D9FDD3"
    bub_text = "#E9F5EE" if th is THEMES["dark"] else "#13321F"
    bub_muted = "#9CC9AE" if th is THEMES["dark"] else "#4C7A5C"
    bw, bh = 236, 172
    bx, by = x + w - bw - 24, y + h - bh - 30
    g = [f'<g class="pop">']
    g.append(f'<path d="M{bx} {by+14}a14 14 0 0 1 14-14h{bw-28}a14 14 0 0 1 14 14v{bh-28}a14 14 0 0 1-14 14H{bx+14}a14 14 0 0 1-14-14z" fill="{bub_fill}"/>')
    g.append(f'<path d="M{bx+bw-6} {by+bh-18} l16 14 -22 -2z" fill="{bub_fill}"/>')
    lines = [("Hi! I'd like to order:", bub_text, "medium"), ("2× Pan de yema", bub_text, "regular"), ("1× Café chorreado", bub_text, "regular")]
    for i, (t, c, wgt) in enumerate(lines):
        g.append(text(t, 12.5, bx + 16, by + 28 + i * 21, c, wgt))
    g.append(text("₡2,400", 12.5, bx + bw - 16, by + 49, bub_muted, "medium", "end"))
    g.append(text("₡1,500", 12.5, bx + bw - 16, by + 70, bub_muted, "medium", "end"))
    g.append(f'<path d="M{bx+16} {by+86}h{bw-32}" stroke="{bub_muted}" stroke-opacity=".5"/>')
    g.append(text("Total", 13, bx + 16, by + 108, bub_text, "semibold"))
    g.append(text("₡3,900", 13, bx + bw - 16, by + 108, bub_text, "semibold", "end"))
    g.append(text("Track your order", 11.5, bx + 16, by + 134, "#53BDEB", "medium"))
    g.append(text("SINPE Móvil  ·  receipt checked", 11, bx + 16, by + 154, bub_muted))
    g.append(f'<path d="M{bx+bw-38} {by+150}l3 3 6-6M{bx+bw-30} {by+150}l3 3 6-6" fill="none" stroke="#53BDEB" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    g.append("</g>")
    b += g
    style = (
        ".pop{transform-box:fill-box;transform-origin:right bottom;animation:pop 7s ease-out infinite}"
        "@keyframes pop{0%,84%{transform:none;opacity:1}90%{transform:scale(.9) translateY(8px);opacity:0}94%{transform:scale(.9) translateY(8px);opacity:0}100%{transform:none;opacity:1}}"
    )
    return "".join(b), style


def v_rag(th, accent, x, y, w, h):
    b = []
    cx0, cw = x + 28, w - 56
    # docs stack
    dy = y + 78
    for i, (n, sc) in enumerate((("handbook.pdf", "0.9"), ("policies.docx", "0.65"), ("notes.txt", "0.35"))):
        dx = cx0 + i * 146
        b.append(f'<rect x="{dx}" y="{dy}" width="136" height="54" rx="10" fill="{th["card"]}" stroke="{th["border"]}"/>')
        b.append(f'<path d="M{dx+14} {dy+13}h12l5 5v17h-17z" fill="none" stroke="{th["muted"]}" stroke-width="1.5" stroke-linejoin="round"/>')
        b.append(text(n, 10.5, dx + 40, dy + 24, th["text"], "medium"))
        b.append(f'<rect x="{dx+40}" y="{dy+33}" width="80" height="5" rx="2.5" fill="{th["border"]}"/>')
        b.append(f'<rect class="fill{i}" x="{dx+40}" y="{dy+33}" width="{80*float(sc):.1f}" height="5" rx="2.5" fill="{accent}" opacity="{1 - i*0.3}"/>')
    # question
    q = "What is the refund window?"
    qw = tw(q, 13, "medium") + 32
    qy = dy + 78
    b.append(f'<rect x="{fmt(cx0+cw-qw)}" y="{qy}" width="{fmt(qw)}" height="38" rx="19" fill="{accent}"/>')
    b.append(text(q, 13, cx0 + cw - 16, qy + 24, "#FFFFFF", "medium", "end"))
    # answer
    ay = qy + 54
    ah = 118
    b.append(f'<g class="ans"><rect x="{cx0}" y="{ay}" width="{cw-40}" height="{ah}" rx="14" fill="{th["card"]}" stroke="{th["border"]}"/>')
    lines = ["Refunds are accepted within 30 days of", "purchase [1]. The documents don't mention", "international orders, so I can't answer that."]
    for i, l in enumerate(lines):
        b.append(text(l, 13, cx0 + 18, ay + 28 + i * 21, th["text"]))
    cit = "[1] handbook.pdf  ·  page 4"
    b.append(f'<rect x="{cx0+18}" y="{ay+ah-34}" width="{fmt(tw(cit, 11, "medium")+20)}" height="22" rx="6" fill="{th["card2"]}" stroke="{th["border"]}"/>')
    b.append(text(cit, 11, cx0 + 28, ay + ah - 19, accent, "medium"))
    meta = "Answers only from your documents"
    b.append(f'<circle cx="{cx0+5}" cy="{ay+ah+31}" r="3.5" fill="{accent}"/>')
    b.append(text(meta, 11.5, cx0 + 16, ay + ah + 35, th["muted"], "medium"))
    b.append("</g>")
    style = (
        ".ans{animation:ans 6s ease-out infinite}"
        "@keyframes ans{0%,82%{opacity:1;transform:none}88%,92%{opacity:0;transform:translateY(6px)}100%{opacity:1;transform:none}}"
    )
    return "".join(b), style


def v_doomsday(th, accent, x, y, w, h):
    b = []
    cx0, cw = x + 28, w - 56
    b.append(text("OUTPOSTS", 11, cx0, y + 40, th["faint"], "semibold", tracking=2))
    camps = [("Camp Alpha", 42, (0.82, 0.64, 0.35)), ("Camp Delta", 17, (0.12, 0.48, 0.71)), ("Camp Orion", 28, (0.58, 0.27, 0.66))]
    res = [("Water", "#4C9BE8"), ("Food", "#E3A857"), ("Meds", "#3FA163")]
    ry = y + 64 + max((h - 64 - 300) / 2, 0)
    for i, (n, ppl, vals) in enumerate(camps):
        yy = ry + i * 70
        b.append(f'<rect x="{cx0}" y="{yy}" width="{cw}" height="58" rx="12" fill="{th["card"]}" stroke="{th["border"]}"/>')
        b.append(text(n, 13.5, cx0 + 16, yy + 25, th["text"], "semibold"))
        b.append(text(f"{ppl} survivors", 11, cx0 + 16, yy + 43, th["muted"]))
        bx = cx0 + 150
        bw = (cw - 150 - 16 - 2 * 14) / 3
        for j, ((rn, col), v) in enumerate(zip(res, vals)):
            xx = bx + j * (bw + 14)
            b.append(text(rn, 10.5, xx, yy + 24, th["muted"], "medium"))
            b.append(f'<rect x="{fmt(xx)}" y="{yy+32}" width="{fmt(bw)}" height="7" rx="3.5" fill="{th["border"]}"/>')
            c = "#E5534B" if v < 0.2 else col
            b.append(f'<rect x="{fmt(xx)}" y="{yy+32}" width="{fmt(bw*v)}" height="7" rx="3.5" fill="{c}"/>')
    # toast
    ty = ry + 3 * 70 + 6
    th_ = 62
    if ty + th_ < y + h - 10:
        b.append(f'<g class="toast"><rect x="{cx0}" y="{ty}" width="{cw}" height="{th_}" rx="12" fill="{th["card"]}" stroke="{th["border"]}"/>')
        b.append(f'<rect x="{cx0}" y="{ty+12}" width="3.5" height="{th_-24}" rx="1.75" fill="{accent}"/>')
        b.append(text("Transfer rejected", 13, cx0 + 18, ty + 26, th["text"], "semibold"))
        b.append(text("Camp Delta has 40 L of water. You requested 120 L.", 11.5, cx0 + 18, ty + 45, th["muted"]))
        b.append("</g>")
    style = (
        ".toast{animation:toast 6s ease-out infinite}"
        "@keyframes toast{0%,82%{opacity:1;transform:none}88%,92%{opacity:0;transform:translateY(8px)}100%{opacity:1;transform:none}}"
    )
    return "".join(b), style


PROJECTS = [
    dict(
        name="healthycropping", accent="#3FA163", kicker="ANDROID APP  ·  ON-DEVICE ML",
        title="HealthyCropping",
        desc="Point a phone at a coffee leaf and get a diagnosis right there in the field, with no signal. "
        "A MobileNetV3 model trained on public coffee datasets runs on the device through TensorFlow Lite. "
        "Cacao and banana models come next, along with a Gemini RAG layer that explains what to do and cites official manuals.",
        tools=["reactnative", "expo", "typescript", "tflite", "python", "fastapi", "firebase", "sqlite", "googlegemini", "cloudinary"],
        status="In active development", visual=v_healthy,
    ),
    dict(
        name="booth", accent="#6366F1", kicker="WEB APP  ·  COMMERCE",
        title="Booth",
        desc="Small shops in Latin America already sell through WhatsApp, one chat at a time. Booth gives each store "
        "a single link with its catalog, turns the cart into a clean WhatsApp message, reserves stock atomically "
        "and uses Gemini to read transfer receipts so owners know what to check before confirming a payment.",
        tools=["react", "typescript", "vite", "tailwindcss", "reactquery", "nestjs", "prisma", "postgresql", "zod", "googlegemini", "vercel", "render", "neon", "playwright"],
        labels={"reactquery": "TanStack Query"},
        status="Live demo", visual=v_booth,
    ),
    dict(
        name="rag", accent="#1F9E98", kicker="AI  ·  RETRIEVAL AUGMENTED GENERATION",
        title="RAG Research Engine",
        desc="Upload your documents, ask in any language and get answers grounded only in what you uploaded. "
        "When the context doesn't hold the answer it says so instead of making one up. Retrieval favors more recent "
        "files, the context is capped at 4,000 tokens, and every answer shows the passages it came from.",
        tools=["python", "fastapi", "postgresql", "sqlalchemy", "cohere", "groq", "meta", "docker"],
        labels={"groq": "Groq", "meta": "Llama 3.3 70B", "cohere": "Cohere Embed"},
        status="Open source", visual=v_rag,
    ),
    dict(
        name="doomsday", accent="#E0234E", kicker="FULL STACK  ·  API + DASHBOARD",
        title="Doomsday System",
        desc="A management platform for a post-apocalyptic world: camps, survivors, supplies and the transfers between "
        "outposts. The interesting part is the rules engine, which refuses impossible moves like shipping water a camp "
        "doesn't have. NestJS API, React dashboard and end to end tests on both sides.",
        tools=["nestjs", "typescript", "typeorm", "postgresql", "react", "vite", "tailwindcss", "python", "jest", "vitest", "playwright", "docker", "swagger", "render", "vercel"],
        status="Deployed", visual=v_doomsday,
    ),
]


# --------------------------------------------------------------------------- toolbox
TOOLBOX = [
    ("Languages", ["typescript", "javascript", "python", "openjdk", "gnubash", "sql"]),
    ("Frontend & mobile", ["react", "reactnative", "expo", "vite", "tailwindcss", "reactquery", "zod"]),
    ("Backend", ["nestjs", "nodedotjs", "fastapi", "springboot", "graphql", "prisma", "typeorm", "sqlalchemy", "pydantic"]),
    ("Data & AI", ["tensorflow", "keras", "tflite", "numpy", "pandas", "scikitlearn", "googlegemini", "kaggle"]),
    ("Databases", ["postgresql", "mariadb", "sqlite", "neon", "firebase"]),
    ("Cloud & DevOps", ["oracle", "googlecloud", "aws", "docker", "githubactions", "vercel", "render", "cloudinary", "linux"]),
    ("Quality & workflow", ["jest", "vitest", "playwright", "pytest", "ruff", "uv", "pnpm", "git", "postman"]),
]


def toolbox(theme):
    th = THEMES[theme]
    W = 1200
    L = 56
    lab_w = 210
    b = []
    y = 52
    labels = {"openjdk": "Java", "gnubash": "Bash", "nodedotjs": "Node.js", "reactquery": "TanStack Query", "oracle": "Oracle Cloud", "aws": "AWS"}
    for i, (cat, slugs) in enumerate(TOOLBOX):
        c, chh = chips(slugs, L + lab_w, y, W - L * 2 - lab_w, th, h=38, fs=14.5, gap=10, labels=labels)
        b.append(text(cat, 15, L, y + 24, th["text"], "semibold"))
        b.append(c)
        y += chh
        if i < len(TOOLBOX) - 1:
            b.append(f'<path d="M{L} {y+19}H{W-L}" stroke="{th["border"]}"/>')
            y += 38
    H = y + 52
    write("toolbox", theme, svg_doc(W, H, frame(W, H, th, 24) + "".join(b), "Toolbox: languages, frameworks, data, cloud and tooling I use"))


# --------------------------------------------------------------------------- interests
INTERESTS = [
    ("aws", "#FF9900", "AWS", "Cloud architecture",
     "Where I want to grow next. I started with generative AI on AWS and I'm going deeper into the core services."),
    ("databricks", "#FF3621", "Databricks", "Data engineering",
     "Data engineering at scale: Spark, Delta Lake and the lakehouse model behind modern data platforms."),
    ("shield", "#4C9BE8", "Cybersecurity", "Network & app security",
     "Understanding how systems get attacked, from the network to the application, to build ones that hold up."),
]


def interests(theme):
    th = THEMES[theme]
    W, gap = 1200, 20
    tw_ = (W - 2 * gap) / 3
    H = 270
    b = []
    for i, (slug, col, name, kind, desc) in enumerate(INTERESTS):
        x = i * (tw_ + gap)
        b.append(f'<rect x="{fmt(x+.5)}" y=".5" width="{fmt(tw_-1)}" height="{H-1}" rx="20" fill="{th["card"]}" stroke="{th["border"]}"/>')
        b.append(f'<clipPath id="c{i}"><rect x="{fmt(x+.5)}" y=".5" width="{fmt(tw_-1)}" height="{H-1}" rx="20"/></clipPath>')
        b.append(f'<rect clip-path="url(#c{i})" x="{fmt(x)}" y="0" width="{fmt(tw_)}" height="4" fill="{col}" opacity=".9"/>')
        b.append(f'<rect x="{fmt(x+32)}" y="36" width="52" height="52" rx="14" fill="{th["card2"]}" stroke="{th["border"]}"/>')
        if slug == "shield":
            b.append(
                f'<g transform="translate({fmt(x+44)} 48)" fill="none" stroke="{col}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">'
                '<path d="M14 1.5 3 6v8c0 6.5 4.7 11 11 13 6.3-2 11-6.5 11-13V6z"/><path d="M9 14l3.6 3.6L19.5 10.5"/></g>'
            )
        else:
            b.append(icon(slug, x + 44, 50, 28, th))
        b.append(text(kind.upper(), 11.5, x + 32, 124, col, "semibold", tracking=1.8))
        b.append(text(name, 26, x + 31, 158, th["text"], "display", tracking=-0.4))
        p, _ = paragraph(desc, 15, x + 32, 192, tw_ - 64, th["muted"], leading=1.55)
        b.append(p)
    write("interests", theme, svg_doc(W, H, "".join(b), "Interests: AWS, Databricks and cybersecurity"))


# --------------------------------------------------------------------------- certifications
CERTS = [
    ("oracle", "Oracle Cloud Infrastructure", "Certified Architect Associate", "Oracle", "Issued Oct 2026  ·  Expires Oct 2028",
     "103563028OCI26CAA", ["Cloud-Native Architecture", "Network Security"]),
    ("oracle", "Oracle Cloud Infrastructure", "Certified AI Foundations Associate", "Oracle", "Issued Oct 2026  ·  Expires Oct 2028",
     "103563028OCI26AICFA", ["Artificial Intelligence", "Machine Learning"]),
    ("googleg", "Google Cloud Computing", "Foundations Certificate", "Google", "Issued Oct 2026",
     None, ["Google Cloud", "Big Data"]),
    ("aws", "Advanced Generative AI", "Implementation on AWS", "Amazon Web Services", "Issued Sep 2025",
     None, ["Generative AI", "Machine Learning"]),
]


def certs(theme):
    th = THEMES[theme]
    W, gap = 1200, 20
    cw, ch = (W - gap) / 2, 210
    H = ch * 2 + gap
    b = []
    for i, (slug, t1, t2, issuer, dates, cid, tags) in enumerate(CERTS):
        x = (i % 2) * (cw + gap)
        y = (i // 2) * (ch + gap)
        b.append(f'<rect x="{fmt(x+.5)}" y="{fmt(y+.5)}" width="{fmt(cw-1)}" height="{ch-1}" rx="20" fill="{th["card"]}" stroke="{th["border"]}"/>')
        b.append(f'<rect x="{fmt(x+30)}" y="{y+30}" width="60" height="60" rx="16" fill="{th["card2"]}" stroke="{th["border"]}"/>')
        b.append(icon(slug, x + 44, y + 44, 32, th))
        tx = x + 112
        b.append(text(t1, 19, tx, y + 52, th["text"], "semibold"))
        b.append(text(t2, 19, tx, y + 77, th["text"], "semibold"))
        b.append(text(issuer, 14, tx, y + 106, th["text"], "medium"))
        b.append(text(dates, 13.5, tx + tw(issuer, 14, "medium") + 12, y + 106, th["muted"]))
        if cid:
            b.append(text("Credential ID", 12, tx, y + 130, th["faint"], "medium"))
            b.append(text(cid, 12.5, tx + tw("Credential ID", 12, "medium") + 8, y + 130, th["muted"], "medium", tracking=0.6))
        cx = tx
        ty = y + 152 if cid else y + 128
        for tg in tags:
            ww = tw(tg, 12.5, "medium") + 24
            b.append(f'<rect x="{fmt(cx)}" y="{ty}" width="{fmt(ww)}" height="28" rx="8" fill="{th["card2"]}" stroke="{th["border"]}"/>')
            b.append(text(tg, 12.5, cx + 12, ty + 18.5, th["muted"], "medium"))
            cx += ww + 8
        # verified tick
        b.append(f'<g transform="translate({fmt(x+cw-50)} {y+30})"><circle cx="10" cy="10" r="10" fill="{th["accent"]}" opacity=".16"/>'
                 f'<path d="M5.8 10.2l2.8 2.8 5.6-5.8" fill="none" stroke="{th["accent"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>')
    write("certifications", theme, svg_doc(W, H, "".join(b), "Certifications: Oracle Cloud Infrastructure Architect Associate, OCI AI Foundations Associate, Google Cloud Computing Foundations, Advanced Generative AI on AWS"))


# --------------------------------------------------------------------------- contact buttons
def button(name, theme, label, glyph):
    th = THEMES[theme]
    H = 52
    W = int(tw(label, 16, "semibold") + 84)
    body = (
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{(H-1)/2}" fill="{th["card"]}" stroke="{th["border"]}"/>'
        + glyph(th)
        + text(label, 16, 60, 32, th["text"], "semibold")
    )
    write(f"btn-{name}", theme, svg_doc(W, H, body, label))


def g_mail(th):
    return (f'<g transform="translate(24 16)" fill="none" stroke="{th["accent"]}" stroke-width="2" stroke-linejoin="round">'
            '<rect x="1" y="2" width="22" height="16" rx="3"/><path d="M2 4l10 7.5L22 4" stroke-linecap="round"/></g>')


def g_linkedin(th):
    return (f'<g transform="translate(24 14)"><rect width="24" height="24" rx="5" fill="#0A66C2"/>'
            '<rect x="5" y="9.5" width="3.2" height="9.5" fill="#fff"/><circle cx="6.6" cy="6.2" r="1.9" fill="#fff"/>'
            '<path d="M10.6 9.5h3.1v1.4c.5-.9 1.6-1.7 3.2-1.7 3 0 3.6 1.9 3.6 4.5V19h-3.2v-4.6c0-1.2 0-2.6-1.6-2.6s-1.9 1.2-1.9 2.5V19h-3.2z" fill="#fff"/></g>')


def g_github(th):
    from svglib import ICONS
    return f'<g transform="translate(24 14)"><path fill="{th["text"]}" transform="scale(1)" d="{ICONS.get("github", {}).get("path", "")}"/></g>'


for theme in ("dark", "light"):
    header(theme)
    for p in PROJECTS:
        card(p["name"], theme, p["accent"], p["kicker"], p["title"], p["desc"], p["tools"], p["status"], p["visual"], p.get("labels"))
    toolbox(theme)
    interests(theme)
    certs(theme)
    button("email", theme, "keylorpineda729@gmail.com", g_mail)
    button("linkedin", theme, "LinkedIn", g_linkedin)

print("ok", sorted(f.name for f in OUT.iterdir()))
