"""Illustrations used inside the project banners."""

from svglib import THEMES, fmt, text, tw

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


