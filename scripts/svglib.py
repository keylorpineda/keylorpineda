"""Small toolkit to draw README SVGs with text converted to Inter outlines."""

import json
import random
from functools import lru_cache
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).parent / "fonts"
ICONS = json.loads((Path(__file__).parent / "icons.json").read_text())

THEMES = {
    "dark": dict(
        card="#0F141B", card2="#161C25", border="#262D38", text="#E8ECF1",
        muted="#9BA3AE", faint="#5C6570", cell="#1A212B", accent="#E3A857",
    ),
    "light": dict(
        card="#FFFFFF", card2="#F5F7F9", border="#DCE1E6", text="#1A1F26",
        muted="#57606A", faint="#8C959F", cell="#EDF0F3", accent="#A86B12",
    ),
}


def fmt(n: float) -> str:
    s = f"{n:.1f}"
    return s[:-2] if s.endswith(".0") else s


class Font:
    def __init__(self, filename: str):
        path = FONT_DIR / filename
        self.tt = TTFont(path)
        self.glyphs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.upem = self.tt["head"].unitsPerEm
        blob = hb.Blob.from_file_path(str(path))
        self.hbfont = hb.Font(hb.Face(blob))

    @lru_cache(maxsize=4096)
    def shape(self, text: str):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {"kern": True, "liga": True, "calt": True})
        return [(i.codepoint, p.x_advance, p.x_offset) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]

    def width(self, text: str, size: float, tracking: float = 0) -> float:
        adv = sum(a for _, a, _ in self.shape(text)) * size / self.upem
        return adv + tracking * max(len(text) - 1, 0)

    def path(self, text: str, size: float, x: float, y: float, anchor: str = "start", tracking: float = 0) -> str:
        w = self.width(text, size, tracking)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        s = size / self.upem
        pen = SVGPathPen(self.glyphs, ntos=fmt)
        cx = x
        for gid, adv, xoff in self.shape(text):
            name = self.order[gid]
            tp = TransformPen(pen, (s, 0, 0, -s, cx + xoff * s, y))
            self.glyphs[name].draw(tp)
            cx += adv * s + tracking
        return pen.getCommands()


F = {
    "regular": Font("Inter-Regular.otf"),
    "medium": Font("Inter-Medium.otf"),
    "semibold": Font("Inter-SemiBold.otf"),
    "display": Font("InterDisplay-Bold.otf"),
}


_DEFS = {}


def text(t, size, x, y, fill, weight="regular", anchor="start", tracking=0, extra=""):
    """Text as outlines; glyphs are defined once per document and reused with <use>."""
    f = F[weight]
    w = f.width(t, size, tracking)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    s = size / f.upem
    uses, cx = [], 0.0
    for gid, adv, xoff in f.shape(t):
        key = f"{weight[:2]}{gid}"
        if key not in _DEFS:
            pen = SVGPathPen(f.glyphs, ntos=lambda n: str(round(n)))
            f.glyphs[f.order[gid]].draw(pen)
            _DEFS[key] = pen.getCommands()
        if _DEFS[key]:
            uses.append(f'<use href="#{key}" x="{round(cx + xoff)}"/>')
        cx += adv + tracking / s
    return f'<g fill="{fill}" {extra} transform="translate({fmt(x)} {fmt(y)}) scale({s:.5f} {-s:.5f})">{"".join(uses)}</g>'


def tw(t, size, weight="regular", tracking=0):
    return F[weight].width(t, size, tracking)


def wrap(t, size, width, weight="regular"):
    lines, cur = [], ""
    for word in t.split():
        trial = f"{cur} {word}".strip()
        if tw(trial, size, weight) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def paragraph(t, size, x, y, width, fill, weight="regular", leading=1.5):
    out = []
    for i, line in enumerate(wrap(t, size, width, weight)):
        out.append(text(line, size, x, y + i * size * leading, fill, weight))
    n = len(wrap(t, size, width, weight))
    return "".join(out), n * size * leading


def _lum(hexc):
    hexc = hexc.lstrip("#")
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


CUSTOM = {
    "aws": ("AWS", "#FF9900"),
    "oracle": ("Oracle Cloud", "#C74634"),
    "playwright": ("Playwright", "#2EAD33"),
    "cohere": ("Cohere", "#39594D"),
    "groq": ("Groq", "#F55036"),
    "reactnative": ("React Native", "#61DAFB"),
    "tflite": ("TensorFlow Lite", "#FF6F00"),
    "sql": ("SQL", "#336791"),
    "sqlalchemyx": ("SQLAlchemy", "#B5361F"),
    "kagglex": ("Kaggle", "#20BEFF"),
}


def icon(slug, x, y, size, th):
    """Brand icon drawn inside a size x size box at (x, y)."""
    s = size / 24
    g = f'<g transform="translate({fmt(x)} {fmt(y)}) scale({s:.4f})">'
    if slug in ("sqlalchemy", "kaggle"):
        slug += "x"
    if slug in ICONS:
        color = "#" + ICONS[slug]["hex"]
        if contrast(color, th["card2"]) < 2.0:
            color = th["text"]
        return f'{g}<path fill="{color}" d="{ICONS[slug]["path"]}"/></g>'
    if slug == "reactnative":
        return icon("react", x, y, size, th)
    if slug == "tflite":
        return icon("tensorflow", x, y, size, th)
    if slug == "aws":
        return (
            f'{g}{text("aws", 11.5, 12, 13.2, th["text"], "semibold", "middle", -0.2)}'
            '<path d="M3.2 16.4c5.4 3.3 12.2 3.3 17.4 0" fill="none" stroke="#FF9900" stroke-width="1.7" stroke-linecap="round"/>'
            '<path d="M18.2 15.2l2.6 1.1-1.1 2.6" fill="none" stroke="#FF9900" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></g>'
        )
    if slug == "googleg":
        return (
            f'<g transform="translate({fmt(x)} {fmt(y)}) scale({size / 48:.4f})">'
            '<path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>'
            '<path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>'
            '<path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>'
            '<path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></g>'
        )
    if slug == "oracle":
        return f'{g}<rect x="1.8" y="6.2" width="20.4" height="11.6" rx="5.8" fill="none" stroke="#C74634" stroke-width="2.8"/></g>'
    name, color = CUSTOM[slug]
    initials = {"SQLAlchemy": "SA", "Kaggle": "K", "Playwright": "PW", "Cohere": "Co", "Groq": "Gq", "SQL": "SQL"}.get(name, name[:2])
    return (
        f'{g}<rect x="1" y="1" width="22" height="22" rx="6" fill="{color}"/>'
        f'{text(initials, 10 if len(initials) < 3 else 8, 12, 15.6, "#FFFFFF", "semibold", "middle")}</g>'
    )


def label_of(slug):
    if slug in ICONS:
        return ICONS[slug]["title"]
    if slug + "x" in CUSTOM:
        return CUSTOM[slug + "x"][0]
    return CUSTOM[slug][0]


def chip(slug, x, y, th, h=38, fs=15, label=None, fill=None):
    """Returns (svg, width)."""
    label = label or label_of(slug)
    isz = h * 0.47
    pad = h * 0.34
    w = pad + isz + 9 + tw(label, fs, "medium") + pad + 2
    svg = (
        f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{h}" rx="{h/2}" fill="{fill or th["card2"]}" stroke="{th["border"]}"/>'
        + icon(slug, x + pad, y + (h - isz) / 2, isz, th)
        + text(label, fs, x + pad + isz + 9, y + h / 2 + fs * 0.36, th["text"], "medium")
    )
    return svg, w


def chips(slugs, x, y, maxw, th, h=38, fs=15, gap=10, labels=None, fill=None):
    out, cx, cy = [], x, y
    labels = labels or {}
    for slug in slugs:
        lab = labels.get(slug)
        _, w = chip(slug, 0, 0, th, h, fs, lab)
        if cx + w > x + maxw and cx > x:
            cx, cy = x, cy + h + gap
        svg, w = chip(slug, cx, cy, th, h, fs, lab, fill)
        out.append(svg)
        cx += w + gap
    return "".join(out), cy + h - y


def svg_doc(w, h, body, title, style="", width=None):
    defs = "".join(f'<path id="{k}" d="{d}"/>' for k, d in _DEFS.items() if d)
    _DEFS.clear()
    size = f'width="{width}" height="{fmt(h * width / w)}"' if width else f'width="{fmt(w)}" height="{fmt(h)}"'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" {size} viewBox="0 0 {fmt(w)} {fmt(h)}" role="img" aria-label="{title}">'
        f"<title>{title}</title><defs>{defs}</defs>"
        + (f"<style>{style}</style>" if style else "")
        + body
        + "</svg>"
    )


def frame(w, h, th, rx=20):
    return f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="{th["card"]}" stroke="{th["border"]}"/>'


def rng(seed):
    return random.Random(seed)
