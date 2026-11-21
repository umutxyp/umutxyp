#!/usr/bin/env python3
"""Draws the pictures of the profile README: ink lines, ivy and hand lettering.

Everything is an SVG written by this file, twice: once in dark ink for GitHub's
light theme (assets/light) and once in pale ink for the dark one (assets/dark).
Lettering is turned into outlines here (fontTools), so the pictures need no font
where they are shown.

Edit the DATA section below, then run:  python3 scripts/generate.py
Needs:  pip install fonttools
"""
import base64
import json
import math
import os
import random
import re
from functools import lru_cache
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# Live numbers scraped from codeshare.me by scripts/fetch_stats.py.
# A stat written as ("page", "Label on codeshare.me") is looked up there;
# a plain string is used as is.
LIVE = json.loads((ROOT / "data" / "stats.json").read_text())["pages"]


def live(v):
    return LIVE[v[0]][v[1]] if isinstance(v, tuple) else v

# ─────────────────────────────── DATA ───────────────────────────────

NAME = "Umut Bayraktar"
ROLES = ["founder of Codeshare", "full-stack developer", "AI systems researcher"]

LINKS = [
    ("codeshare", "codeshare.me"),
    ("portfolio", "portfolio"),
    ("linkedin", "linkedin"),
    ("youtube", "youtube"),
    ("instagram", "instagram"),
    ("tiktok", "tiktok"),
    ("telegram", "telegram"),
    ("x", "x"),
    ("facebook", "facebook"),
    ("email", "email"),
]

# Logos that are a pale mark on nothing: the tile they sit on in their own product.
LOGO_TILE = {"dotrai": "#0d0d0f", "justanime": "#15131d"}

HEADINGS = [("about", "About"), ("projects", "Projects"), ("stack", "Tech stack"), ("opensource", "Open source")]

STACK = ["TypeScript", "JavaScript", "Next.js", "React", "Tailwind", "Node.js", "PostgreSQL",
         "Prisma", "Redis", "MongoDB", "Docker", "Linux", "nginx", "Cloudflare"]

STATS = [
    (("home", "Discord users reached"), "Discord users reached"),
    (("home", "Discord servers"), "Discord servers"),
    (("home", "Minecraft players"), "Minecraft players"),
    (("github", "Stars"), "GitHub stars"),
]

STUDIO = dict(
    title="Codeshare Technology", url="codeshare.me",
    tag="software studio",
    desc="Software for online communities — with the core kept free.",
    products=["Beatra", "Shroudly", "Vanigo", "Sylon", "MCStat", "JustAnime", "JustDiscord", "Dotrai"],
    stats=[(("about", "Products live"), "products live"),
           (("about", "Discord users reached"), "Discord users reached"),
           (("about", "Oldest account we own"), "oldest account"),
           (("about", "Company incorporated"), "incorporated")],
)

PROJECTS = {
    "beatra": dict(
        title="Beatra", url="beatra.app",
        desc=["Music bot for Discord, with a web player —",
              "Spotify, YouTube, Apple Music and more."],
        stats=[(("beatra", "Discord servers"), "servers"), (("beatra", "Discord users"), "users")],
    ),
    # "Running right now" is on its page too, but these cards are redrawn once
    # a day, so a number that means "this minute" would be a day old. The logo
    # is the iOS app icon (apple/App/AppIcon.icon in the Shroudly repo).
    "shroudly": dict(
        title="Shroudly", url="github.com/umutxyp/Shroudly",
        desc=["Opens blocked YouTube, Instagram, X, Discord —",
              "no VPN; Windows 7–11, Mac, Linux, phones, TVs."],
        stats=[(("shroudly", "Downloads"), "downloads"), (("shroudly", "GitHub stars"), "stars")],
    ),
    "vanigo": dict(
        title="Vanigo", url="vanigo.app",
        desc=["Travel app with places, reviews, events and trips —",
              "plus a wallet that pays shops by local QR."],
        stats=[(("vanigo", "Places on the map"), "places"), (("vanigo", "Languages"), "languages")],
    ),
    "sylon": dict(
        title="Sylon", url="sylon.app",
        desc=["AI moderation for Discord that catches ads",
              "and scams in any language, even in images."],
        stats=[(("sylon", "Discord servers"), "servers"), (("sylon", "Discord users"), "users"),
               (("sylon", "Uptime"), "uptime")],
    ),
    "mcstat": dict(
        title="MCStat", url="mcstat.org",
        desc=["Real-time Minecraft server list with live player",
              "counts, vote rankings and player profiles."],
        stats=[(("mcstat", "Servers tracked"), "servers"), (("mcstat", "Player records"), "players"),
               (("mcstat", "Skins archived"), "skins")],
    ),
    "justanime": dict(
        title="JustAnime", url="justanime.me",
        desc=["Anime & manga tracker where every single",
              "episode gets its own rating and review."],
        stats=[(("justanime", "Anime and manga titles"), "titles"), (("justanime", "Character records"), "characters"),
               (("justanime", "Airing schedule entries"), "airing")],
    ),
    "justdiscord": dict(
        title="JustDiscord", url="justdiscord.org",
        desc=["Discord server & bot list built on trust —",
              "real reviews, verified owners, free emojis."],
        stats=[(("justdiscord", "Server listings"), "servers"), (("justdiscord", "Bot listings"), "bots"),
               (("justdiscord", "Emojis and stickers"), "emojis")],
    ),
    "dotrai": dict(
        title="Dotrai", url="dotrai.com",
        desc=["Free AI chat that searches the live web,",
              "runs real code and shows its reasoning."],
        stats=[],
    ),
}

# ───────────────────────────── PALETTES ─────────────────────────────
# Transparent pictures, so the page itself is the paper: dark ink on GitHub's
# light theme, pale ink on its dark one. The README picks the file with <picture>.

PALETTES = {
    "light": dict(ink="#1f2a24", soft="#51605a", leaf=["#8fc79c", "#63a97a", "#b7dcab"], vein="#2f5b40",
                  accent="#d4572f", marker="#ffd75a", marker_op=".62", wash="#eef4ea", bug="#e0492f", bug_ink="#1f2a24"),
    "dark": dict(ink="#ece8da", soft="#a9ad9f", leaf=["#4f9c69", "#6fbf86", "#3b7a52"], vein="#d9efd9",
                 accent="#ff8f63", marker="#f2c94c", marker_op=".2", wash="#16211b", bug="#f0603f", bug_ink="#14110f"),
}

# ───────────────────────────── LETTERING ────────────────────────────


class Face:
    """A font whose text is written out as path data (baseline at y)."""

    def __init__(self, name):
        self.font = TTFont(OUT / "fonts" / name)
        self.upm = self.font["head"].unitsPerEm
        self.cmap = self.font.getBestCmap()
        self.glyphs = self.font.getGlyphSet()
        self.hmtx = self.font["hmtx"]

    @lru_cache(maxsize=None)
    def glyph(self, ch):
        return self.cmap.get(ord(ch)) or self.cmap.get(ord("-")) or ".notdef"

    def width(self, text, size, tracking=0.0):
        s = size / self.upm
        return sum(self.hmtx[self.glyph(c)][0] * s + tracking for c in text) - (tracking if text else 0)

    def letters(self, text, x, y, size, anchor="start", tracking=0.0):
        """One path per letter: [d, ...] and the full width."""
        s = size / self.upm
        w = self.width(text, size, tracking)
        x -= w / 2 if anchor == "middle" else w if anchor == "end" else 0
        out = []
        for ch in text:
            g = self.glyph(ch)
            pen = SVGPathPen(self.glyphs, lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
            self.glyphs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, y)))
            if pen.getCommands():
                out.append(pen.getCommands())
            x += self.hmtx[g][0] * s + tracking
        return out, w

    def d(self, text, x, y, size, anchor="start", tracking=0.0):
        letters, w = self.letters(text, x, y, size, anchor, tracking)
        return "".join(letters), w


NAME_FACE = Face("GochiHand.ttf")
BOLD = Face("ShantellSans-Bold.ttf")
TEXT = Face("ShantellSans-Text.ttf")

# ───────────────────────────── GEOMETRY ─────────────────────────────


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def smooth(points, closed=False):
    """A smooth path through the points (Catmull-Rom as cubic Béziers)."""
    n = len(points)
    get = (lambda i: points[i % n]) if closed else (lambda i: points[max(0, min(n - 1, i))])
    d = [f"M{f(points[0][0])} {f(points[0][1])}"]
    for i in range(n if closed else n - 1):
        p0, p1, p2, p3 = get(i - 1), get(i), get(i + 1), get(i + 2)
        d.append(f"C{f(p1[0] + (p2[0] - p0[0]) / 6)} {f(p1[1] + (p2[1] - p0[1]) / 6)} "
                 f"{f(p2[0] - (p3[0] - p1[0]) / 6)} {f(p2[1] - (p3[1] - p1[1]) / 6)} {f(p2[0])} {f(p2[1])}")
    return "".join(d) + ("Z" if closed else "")


def sample(points, step=5.0):
    """The same curve as `smooth`, as closely spaced points."""
    n, out = len(points), [points[0]]
    for i in range(n - 1):
        p0, p1, p2, p3 = points[max(0, i - 1)], points[i], points[i + 1], points[min(n - 1, i + 2)]
        seg = max(2, int(math.dist(p1, p2) / step))
        for k in range(1, seg + 1):
            t = k / seg
            out.append(tuple(0.5 * (2 * p1[a] + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t * t
                                    + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t ** 3) for a in (0, 1)))
    return out


def length(points):
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


def hand_line(rng, a, b, wobble=1.5, step=44):
    """A straight line as a hand would draw it: nearly straight."""
    dist = math.dist(a, b)
    n = max(2, int(dist / step))
    nx, ny = -(b[1] - a[1]) / dist, (b[0] - a[0]) / dist
    bow = rng.uniform(-1, 1) * wobble * 1.4
    pts = []
    for i in range(n + 1):
        t = i / n
        off = (rng.uniform(-wobble, wobble) if 0 < i < n else 0) + bow * math.sin(math.pi * t)
        pts.append((a[0] + (b[0] - a[0]) * t + nx * off, a[1] + (b[1] - a[1]) * t + ny * off))
    return pts


def hand_box(rng, x, y, w, h, r, wobble=1.4):
    """A rounded box drawn in one go, the pen overshooting where it closes."""
    pts = []

    def side(a, b):
        pts.extend(hand_line(rng, a, b, wobble)[1:-1] or [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)])

    def corner(cx, cy, a0):
        for k in (0.5,):
            a = math.radians(a0 + 90 * k)
            pts.append((cx + math.cos(a) * r + rng.uniform(-.8, .8), cy + math.sin(a) * r + rng.uniform(-.8, .8)))

    start = (x + r + 14, y + rng.uniform(-1, 1))
    pts.append(start)
    pts.append((x + r + 40, y + rng.uniform(-1, 1)))
    side((x + r + 40, y), (x + w - r, y))
    pts.append((x + w - r, y + rng.uniform(-1, 1)))
    corner(x + w - r, y + r, -90)
    pts.append((x + w + rng.uniform(-1, 1), y + r))
    side((x + w, y + r), (x + w, y + h - r))
    pts.append((x + w + rng.uniform(-1, 1), y + h - r))
    corner(x + w - r, y + h - r, 0)
    pts.append((x + w - r, y + h + rng.uniform(-1, 1)))
    side((x + w - r, y + h), (x + r, y + h))
    pts.append((x + r, y + h + rng.uniform(-1, 1)))
    corner(x + r, y + h - r, 90)
    pts.append((x + rng.uniform(-1, 1), y + h - r))
    side((x, y + h - r), (x, y + r))
    pts.append((x + rng.uniform(-1, 1), y + r))
    corner(x + r, y + r, 180)
    pts.append((x + r, y + rng.uniform(-.5, .5)))
    pts.append((x + r + 16, y + rng.uniform(-.7, .3)))         # a short overlap past the start
    pts.append((x + r + 30, y + rng.uniform(-1.6, -.8)))
    return pts


def blob(rng, x0, y0, x1, y1, rough=2.2):
    """A marker swipe: a slanted, slightly uneven bar."""
    pts = [(x0 - 3, y0 + 3), ((x0 + x1) / 2, y0 + rng.uniform(-rough, rough)), (x1 + 2, y0 - 1),
           (x1 + 7, (y0 + y1) / 2), (x1 + 3, y1 + 1), ((x0 + x1) / 2, y1 + rng.uniform(-rough, rough)),
           (x0 - 6, y1 - 2), (x0 - 8, (y0 + y1) / 2)]
    return smooth(pts, closed=True)

# ─────────────────────────────── INK ────────────────────────────────

STYLE = """
.d{fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;opacity:0;animation:d 1s linear forwards}
@keyframes d{0%{stroke-dashoffset:1;opacity:1}100%{stroke-dashoffset:0;opacity:1}}
.s{fill:none;stroke-linecap:round;stroke-linejoin:round}
.lf{transform:scale(0);animation:lf .9s cubic-bezier(.34,1.56,.64,1) forwards}
@keyframes lf{to{transform:scale(1)}}
.sw{animation:sw 4s ease-in-out infinite alternate}
@keyframes sw{from{transform:rotate(-4deg)}to{transform:rotate(4deg)}}
.br{animation:br 2.8s ease-in-out infinite alternate}
@keyframes br{from{transform:scale(1,1)}to{transform:scale(1.012,1.045)}}
.tl{animation:tl 3.4s ease-in-out infinite alternate}
@keyframes tl{from{transform:rotate(-9deg)}to{transform:rotate(7deg)}}
.zz{opacity:0;animation:zz 3.9s ease-in-out infinite}
@keyframes zz{0%{opacity:0;transform:translate(3px,7px)}35%{opacity:.85}100%{opacity:0;transform:translate(-9px,-17px)}}
.i{opacity:0;animation:i .7s ease forwards}
@keyframes i{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}
.w{stroke-dasharray:1;stroke-dashoffset:1;fill-opacity:0;stroke-linejoin:round;stroke-linecap:round;animation:w 1.2s ease forwards}
@keyframes w{0%{stroke-dashoffset:1;fill-opacity:0}60%{stroke-dashoffset:0;fill-opacity:0}100%{stroke-dashoffset:0;fill-opacity:1}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.d{stroke-dashoffset:0;opacity:1}.lf{transform:none}.i{opacity:1}.w{stroke-dashoffset:0;fill-opacity:1}.zz{opacity:.7}}
"""


class Ink:
    """One picture being drawn, in one palette."""

    def __init__(self, w, h, pal, seed):
        self.w, self.h, self.p = w, h, pal
        self.rng = random.Random(seed)
        self.body, self.defs = [], []

    def add(self, s):
        self.body.append(s)

    # a line that draws itself: `at` seconds after the picture loads, taking `dur`
    def stroke(self, d, at=0.0, dur=0.8, width=2.4, color=None, opacity=None):
        op = f' stroke-opacity="{opacity}"' if opacity else ""
        self.add(f'<path class="d" pathLength="1" d="{d}" stroke="{color or self.p["ink"]}" stroke-width="{width}"{op} '
                 f'style="animation-delay:{at:.2f}s;animation-duration:{dur:.2f}s"/>')

    def text(self, face, s, x, y, size, at=0.0, color=None, anchor="start", tracking=0.0, fit=None):
        if fit and face.width(s, size) > fit:
            size *= fit / face.width(s, size)
        d, w = face.d(s, x, y, size, anchor, tracking)
        self.add(f'<path class="i" d="{d}" fill="{color or self.p["ink"]}" style="animation-delay:{at:.2f}s"/>')
        return w

    def box(self, x, y, w, h, r=20, at=0.0, dur=1.1, width=2.4):
        self.stroke(smooth(hand_box(self.rng, x, y, w, h, r)), at, dur, width)

    def marker(self, x0, y0, x1, y1, at=0.0):
        self.add(f'<path class="i" d="{blob(self.rng, x0, y0, x1, y1)}" fill="{self.p["marker"]}" fill-opacity="{self.p["marker_op"]}" '
                 f'style="animation-delay:{at:.2f}s"/>')

    def logo(self, key, x, y, size, at=0.0, ring=True, ratio=1.0):
        data = base64.b64encode((OUT / "logos" / f"{key}.png").read_bytes()).decode()
        cid = f"c{len(self.defs)}"
        w = size * ratio
        self.defs.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{f(w)}" height="{size}" rx="{f(size * .24)}"/></clipPath>')
        if key in LOGO_TILE:
            self.add(f'<rect class="i" x="{x}" y="{y}" width="{f(w)}" height="{size}" rx="{f(size * .24)}" fill="{LOGO_TILE[key]}" style="animation-delay:{at:.2f}s"/>')
        self.add(f'<image class="i" href="data:image/png;base64,{data}" x="{x}" y="{y}" width="{f(w)}" height="{size}" '
                 f'{"clip-path=" + chr(34) + "url(#" + cid + ")" + chr(34) if ring else ""} style="animation-delay:{at:.2f}s"/>')
        if ring:
            self.stroke(smooth(hand_box(self.rng, x - 3, y - 3, w + 6, size + 6, size * .26, wobble=.9)), at + .1, .7, 2)

    # ── ivy ──

    def leaf(self, size):
        """An ivy leaf pointing along +x from its stalk at the origin: (fill, outline, veins)."""
        rng = self.rng
        j = lambda v: v + rng.uniform(-.035, .035)
        lean = rng.uniform(.88, 1.1)
        half = [(.10, 0), (j(-.07), j(-.36)), (j(.27), j(-.31)), (j(.47), j(-.58)), (j(.66), j(-.27)), (1.0, 0)]
        low = [(x, -y * lean) for x, y in reversed(half[1:-1])]
        pts = [(x * size, y * size) for x, y in half + low]
        cx, cy = .42 * size, 0
        d = [f"M{f(pts[0][0])} {f(pts[0][1])}"]
        for a, b in zip(pts, pts[1:] + pts[:1]):
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            ox, oy = mx - cx, my - cy
            k = .11 * size / (math.hypot(ox, oy) or 1)
            d.append(f"Q{f(mx + ox * k)} {f(my + oy * k)} {f(b[0])} {f(b[1])}")
        outline = "".join(d) + "Z"
        tip = lambda i, k: (cx + (pts[i][0] - cx) * k, pts[i][1] * k)
        veins = f"M{f(.12 * size)} 0Q{f(.5 * size)} {f(rng.uniform(-.03, .03) * size)} {f(.84 * size)} 0"
        for i, k, root in ((1, .62, .2), (3, .68, .34), (len(pts) - 1, .62, .2), (len(pts) - 3, .68, .34)):
            t = tip(i, k)
            veins += f"M{f(root * size)} 0L{f(t[0])} {f(t[1])}"
        return outline, veins

    def vine(self, guide, at=0.0, speed=300, leaf=30, gap=(46, 70), sway=6.0, side=1, both=True, curl=1, width=2.6,
             lean=(48, 78), taper=.55, first=26, berries=0.0):
        """Ivy that grows along `guide`. Returns the stem's path data and the time it has finished growing."""
        rng, p = self.rng, self.p
        pts = sample(guide, 5)
        total = length(pts)
        wave, ph1, ph2 = rng.uniform(150, 200), rng.uniform(0, 6.28), rng.uniform(0, 6.28)
        out, s = [], 0.0
        for i, pt in enumerate(pts):
            a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
            tx, ty = b[0] - a[0], b[1] - a[1]
            n = math.hypot(tx, ty) or 1
            if i:
                s += math.dist(pts[i - 1], pt)
            env = min(1, s / 40) * min(1, (total - s) / 30 + .3)
            off = (math.sin(s / wave * 6.283 + ph1) * sway + math.sin(s / (wave * .37) * 6.283 + ph2) * sway * .22) * env
            out.append((pt[0] - ty / n * off, pt[1] + tx / n * off, s, math.atan2(ty, tx)))
        # the tip curls
        if curl:
            x, y, s, ang = out[-1]
            for k in range(26):
                ang += curl * (0.13 + 0.017 * k)
                st = 5.2 * (1 - k / 34)
                x, y, s = x + math.cos(ang) * st, y + math.sin(ang) * st, s + st
                out.append((x, y, s, ang))
        full = out[-1][2]
        stem = smooth([(q[0], q[1]) for q in out[::3]] + [(out[-1][0], out[-1][1])])
        self.stroke(stem, at, full / speed, width)
        # leaves, each opening as the stem reaches it
        nxt, flip, i = first, side, 0
        leaves = []
        while i < len(out):
            x, y, s, ang = out[i]
            if s >= nxt and s < total - 14:
                k = 1 - (1 - taper) * max(0, (s - total * .55) / (total * .45))
                size = leaf * rng.uniform(.78, 1.16) * k
                stalk = size * rng.uniform(.34, .58)
                turn = ang + flip * math.radians(rng.uniform(*lean))
                leaves.append((x, y, turn, size, stalk, at + s / speed + .05, rng.choice(p["leaf"])))
                if berries and rng.random() < berries and s > 60:
                    # a few berries on the other side of the stem
                    b = ang - flip * math.radians(rng.uniform(60, 95)) if both else ang + flip * math.radians(rng.uniform(100, 140))
                    n, r = rng.choice((2, 3, 3)), size * rng.uniform(.13, .17)
                    dots = "".join(
                        f'<circle cx="{f(size * .42 + math.cos(q) * r * 1.25)}" cy="{f(math.sin(q) * r * 1.25)}" r="{f(r)}" '
                        f'fill="{p["accent"]}" stroke="{p["ink"]}" stroke-width="{f(width * .6)}"/>'
                        for q in (k * 6.283 / n + rng.uniform(0, 1) for k in range(n)))
                    self.add(f'<g transform="translate({f(x)} {f(y)}) rotate({f(math.degrees(b))})"><g class="lf" style="animation-delay:{at + s / speed + .25:.2f}s">'
                             f'<path class="s" d="M0 0Q{f(size * .2)} {f(rng.uniform(-3, 3))} {f(size * .36)} 0" stroke="{p["ink"]}" stroke-width="{f(width * .7)}"/>{dots}</g></g>')
                nxt = s + rng.uniform(*gap) * (.75 + .25 * k)
                if both:
                    flip = -flip
            i += 1
        for x, y, turn, size, stalk, t, fill in leaves:
            outline, veins = self.leaf(size)
            bend = rng.uniform(-.25, .25) * stalk
            tilt = rng.uniform(-14, 14)
            self.add(
                f'<g transform="translate({f(x)} {f(y)}) rotate({f(math.degrees(turn))})">'
                f'<g class="lf" style="animation-delay:{t:.2f}s">'
                f'<g class="sw" style="animation-duration:{rng.uniform(3.2, 6.4):.1f}s;animation-delay:-{rng.uniform(0, 6):.1f}s">'
                f'<path class="s" d="M0 0Q{f(stalk * .5)} {f(bend)} {f(stalk)} 0" stroke="{p["ink"]}" stroke-width="{f(width * .8)}"/>'
                f'<g transform="translate({f(stalk)} 0) rotate({f(tilt)})">'
                f'<path d="{outline}" fill="{fill}" transform="translate({f(size * .075)} {f(size * .06)})"/>'
                f'<path class="s" d="{outline}" stroke="{p["ink"]}" stroke-width="{f(width * .82)}"/>'
                f'<path class="s" d="{veins}" stroke="{p["ink"]}" stroke-width="1.1" stroke-opacity=".7"/>'
                f'</g></g></g></g>')
        return stem, at + full / speed

    def render(self):
        defs = f'<defs>{"".join(self.defs)}</defs>' if self.defs else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" fill="none">'
                f'<style>{STYLE.strip()}</style>{defs}{"".join(self.body)}</svg>\n')


# For looking at a moment of the animation in a still picture: PREVIEW_T=6 writes the pictures as they
# are six seconds after loading, into PREVIEW_DIR (never into assets).
PREVIEW_T = float(os.environ.get("PREVIEW_T", 0))
TARGET = Path(os.environ["PREVIEW_DIR"]) if PREVIEW_T else OUT


def write(theme, name, ink):
    path = TARGET / theme / name
    path.parent.mkdir(parents=True, exist_ok=True)
    svg = ink.render()
    if PREVIEW_T:
        svg = re.sub(r"animation-delay:(-?[\d.]+)s", lambda m: f"animation-delay:{float(m.group(1)) - PREVIEW_T:.2f}s", svg)
        svg = re.sub(r'begin="([\d.]+)s"', lambda m: f'begin="{float(m.group(1)) - PREVIEW_T:.2f}s"', svg)
    path.write_text(svg, encoding="utf-8")


def both(name, draw, w, h, seed):
    """Draws one picture in both palettes, with the same hand (the same seed)."""
    for theme, pal in PALETTES.items():
        ink = Ink(w, h, pal, seed)
        draw(ink)
        write(theme, name, ink)
    print(f"  ✓ {name}")

# ─────────────────────────────── HERO ───────────────────────────────


def ladybug(ink, path, begin, dur=64):
    """A ladybird that walks the vine once it has grown, again and again."""
    p = ink.p
    legs = p["ink"]
    ink.add(
        f'<g opacity="0"><g transform="translate(0 -7)">'
        f'<path class="s" d="M4 -1.5L8.5 -5M4 1.5L8.5 5M-1 -3L-2 -7.5M-1 3L-2 7.5M-5 -2.5L-8 -6M-5 2.5L-8 6" stroke="{legs}" stroke-width="1.2"/>'
        f'<ellipse cx="0" cy="0" rx="8.6" ry="6.6" fill="{p["bug"]}" stroke="{p["bug_ink"]}" stroke-width="1.5"/>'
        f'<path d="M5.2 -5.3A7 7 0 0 1 5.2 5.3Z" fill="{p["bug_ink"]}"/>'
        f'<path class="s" d="M-8.4 0L5 0" stroke="{p["bug_ink"]}" stroke-width="1.2"/>'
        f'<circle cx="-3.6" cy="-3" r="1.5" fill="{p["bug_ink"]}"/><circle cx="-3.4" cy="3.1" r="1.5" fill="{p["bug_ink"]}"/>'
        f'<circle cx="1.4" cy="-2.6" r="1.2" fill="{p["bug_ink"]}"/><circle cx="1.6" cy="2.7" r="1.2" fill="{p["bug_ink"]}"/>'
        f'</g>'
        f'<animateMotion path="{path}" dur="{dur}s" begin="{begin:.1f}s" repeatCount="indefinite" rotate="auto"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.02;0.97;1" dur="{dur}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
        f'</g>')


def hero():
    W, H = 1200, 446

    def draw(ink):
        p = ink.p
        # ivy climbing the left side and running along the top
        stem, done = ink.vine([(-10, 470), (52, 388), (76, 278), (60, 176), (104, 88), (236, 52), (404, 68), (570, 46), (708, 62)],
                              at=.2, speed=330, leaf=42, sway=7, side=-1, curl=-1, width=2.9, gap=(54, 82), berries=.3, first=96)
        # ivy hanging down on the right
        ink.vine([(1210, -18), (1144, 50), (1124, 150), (1150, 236), (1128, 296)], at=.9, speed=260, leaf=38, sway=6, side=1,
                 curl=1, width=2.9, gap=(52, 76), berries=.3, first=74)
        # a short one creeping in along the bottom
        ink.vine([(1212, 440), (1100, 404), (980, 414), (872, 400)], at=1.6, speed=240, leaf=26, sway=4, side=1, curl=-1,
                 width=2.4, gap=(42, 62), first=40)
        # the name, written letter by letter
        letters, w = NAME_FACE.letters(NAME, W / 2 + 6, 246, 138, "middle")
        for k, d in enumerate(letters):
            ink.add(f'<path class="w" pathLength="1" d="{d}" fill="{p["ink"]}" stroke="{p["ink"]}" stroke-width="1.6" '
                    f'style="animation-delay:{.5 + k * .09:.2f}s"/>')
        t = .5 + len(letters) * .09 + .5
        # a swoosh under it, drawn twice like a pen going back
        x0, x1 = W / 2 - w / 2 + 34, W / 2 + w / 2 - 6
        ink.stroke(smooth([(x0, 288), (x0 + (x1 - x0) * .3, 281), (x0 + (x1 - x0) * .62, 287), (x1, 276)]), t, .55, 4.4, p["accent"])
        ink.stroke(smooth([(x1 - 8, 285), (x0 + (x1 - x0) * .66, 295), (x0 + (x1 - x0) * .4, 294)]), t + .5, .4, 3, p["accent"])
        # what he does
        size, gap = 25.5, 52
        sizes = [TEXT.width(r, size) for r in ROLES]
        x = W / 2 - 4 - (sum(sizes) + gap * (len(ROLES) - 1)) / 2
        for k, (r, rw) in enumerate(zip(ROLES, sizes)):
            ink.text(TEXT, r, x, 356, size, t + .5 + k * .18, p["soft"])
            if k < len(ROLES) - 1:
                o, v = ink.leaf(15)
                ink.add(f'<g class="i" style="animation-delay:{t + .6 + k * .18:.2f}s"><g transform="translate({f(x + rw + gap / 2 - 6)} 349) rotate(-38)">'
                        f'<path d="{o}" fill="{p["leaf"][k % 3]}" transform="translate(1.4 1.2)"/>'
                        f'<path class="s" d="{o}" stroke="{p["ink"]}" stroke-width="1.5"/></g></g>')
            x += rw + gap
        ladybug(ink, stem, done + .6)

    both("hero.svg", draw, W, H, seed=11)

# ───────────────────────────── SMALL PARTS ──────────────────────────


def hash_seed(s):
    return sum((i + 1) * ord(c) for i, c in enumerate(s)) % 9973


def links():
    for key, label in LINKS:
        size, pad, h = 30, 26, 76
        W = int(BOLD.width(label, size) + pad * 2 + 22)

        def draw(ink, label=label, W=W):
            p = ink.p
            ink.box(8, 16, W - 22, 48, 23, at=.1, dur=.8, width=2.4)
            ink.text(BOLD, label, 8 + (W - 22) / 2, 50, size, .35, anchor="middle")
            # one small leaf growing out of the top right corner
            o, v = ink.leaf(22)
            ink.add(f'<g transform="translate({W - 31} 20) rotate({f(ink.rng.uniform(-62, -34))})"><g class="lf" style="animation-delay:.9s">'
                    f'<g class="sw" style="animation-duration:{ink.rng.uniform(3.4, 5.6):.1f}s;animation-delay:-{ink.rng.uniform(0, 5):.1f}s">'
                    f'<path class="s" d="M0 0L7 0" stroke="{p["ink"]}" stroke-width="2"/><g transform="translate(7 0)">'
                    f'<path d="{o}" fill="{ink.rng.choice(p["leaf"])}" transform="translate(1.6 1.3)"/>'
                    f'<path class="s" d="{o}" stroke="{p["ink"]}" stroke-width="1.9"/>'
                    f'<path class="s" d="{v}" stroke="{p["ink"]}" stroke-width="1" stroke-opacity=".7"/></g></g></g></g>')

        both(f"links/{key}.svg", draw, W, h, seed=hash_seed(key))


def headings():
    W, H = 1200, 100
    for key, label in HEADINGS:
        def draw(ink, label=label):
            w = ink.text(BOLD, label, 6, 68, 52, .1)
            # a pen stroke under the word, then ivy running off to the right
            ink.stroke(smooth(hand_line(ink.rng, (4, 85), (w + 14, 82), 1.6, 60)), .3, .5, 4.4, ink.p["accent"])
            x0 = w + 46
            ink.vine([(x0, 64), (x0 + 220, 56), (x0 + 470, 68), (x0 + 700, 54), (1126, 62)], at=.4, speed=520, leaf=25,
                     sway=5, side=-1, curl=1, width=2.2, gap=(70, 116), first=40, berries=.25)

        both(f"headings/{key}.svg", draw, W, H, seed=hash_seed(key) + 3)


def stats():
    W, H = 1200, 184
    n = len(STATS)

    def draw(ink):
        p = ink.p
        col = W / n
        for k, (val, label) in enumerate(STATS):
            cx = col * k + col / 2
            v = live(val)
            w = BOLD.width(v, 64)
            ink.marker(cx - w / 2 - 6, 58, cx + w / 2 + 6, 100, .15 + k * .14)
            ink.text(BOLD, v, cx, 96, 64, .25 + k * .14, anchor="middle")
            ink.text(TEXT, label, cx, 142, 23.5, .4 + k * .14, p["soft"], anchor="middle", fit=col - 34)
            if k:
                # a little sprig between two numbers
                x = col * k
                ink.vine([(x + ink.rng.uniform(-4, 4), 108), (x + ink.rng.uniform(-7, 7), 80), (x + ink.rng.uniform(-5, 5), 54), (x + ink.rng.uniform(-4, 4), 30)],
                         at=.5 + k * .2, speed=130, leaf=19, sway=2.5, side=ink.rng.choice((-1, 1)), curl=0,
                         width=2, gap=(20, 25), first=22, taper=.8)

    both("stats.svg", draw, W, H, seed=23)


def stack():
    W = 1200
    size, gap, line = 31, 50, 64
    rows, row, used = [], [], 0.0
    for wd in STACK:
        w = BOLD.width(wd, size)
        if row and used + gap + w > W - 110:
            rows.append(row)
            row, used = [], 0.0
        used += (gap if row else 0) + w
        row.append((wd, w))
    rows.append(row)
    H = 44 + line * len(rows)

    def draw(ink):
        p = ink.p
        k = 0
        for r, row in enumerate(rows):
            x = W / 2 - (sum(w for _, w in row) + gap * (len(row) - 1)) / 2
            y = 56 + r * line
            for wd, w in row:
                ink.text(BOLD, wd, x, y, size, .1 + k * .05)
                # a pen stroke under each word, each one a little different
                ink.stroke(smooth(hand_line(ink.rng, (x - 2, y + 12 + ink.rng.uniform(-1, 1)), (x + w + 3, y + 10 + ink.rng.uniform(-1.5, 1.5)), 1.3, 40)),
                           .3 + k * .05, .35, 2.8, p["accent"] if k % 3 == 0 else p["leaf"][1])
                x += w + gap
                k += 1

    both("stack.svg", draw, W, H, seed=31)

# ────────────────────────────── STUDIO ──────────────────────────────


def cat(ink, cx, base, at):
    """A cat asleep on the top edge of the frame."""
    p = ink.p
    light = p is PALETTES["light"]
    fur, shade = ("#f3b888", "#e39a62") if light else ("#c97a45", "#a55f30")
    w = 2.5
    body = "M-47 1C-54 -24 -37 -42 -10 -42L17 -42C41 -42 52 -23 47 1Z"
    head = "M-55 -37C-55 -51 -46 -58 -35 -58C-24 -58 -15 -51 -15 -37C-15 -24 -24 -18 -35 -18C-46 -18 -55 -24 -55 -37Z"
    ears = "M-52 -46L-54 -68L-39 -56ZM-30 -56L-16 -69L-17 -45Z"
    z = "".join(
        f'<g transform="translate({x} {y})"><path class="zz" d="{BOLD.d("z", 0, 0, s)[0]}" fill="{p["soft"]}" style="animation-delay:{at + 1.2 + k * 1.3:.2f}s"/></g>'
        for k, (x, y, s) in enumerate(((-70, -38, 15), (-84, -50, 18), (-99, -62, 21))))
    ink.add(
        f'<g transform="translate({cx} {base})"><g class="i" style="animation-delay:{at:.2f}s">'
        f'<g transform="translate(45 -8)"><g class="tl">'
        f'<path class="s" d="M0 0C21 -3 26 18 15 31C9 38 2 34 4 27" stroke="{p["ink"]}" stroke-width="13.5"/>'
        f'<path class="s" d="M0 0C21 -3 26 18 15 31C9 38 2 34 4 27" stroke="{fur}" stroke-width="8.6"/>'
        f'<path class="s" d="M19 9l7 -3M19 19l7 0" stroke="{shade}" stroke-width="3"/></g></g>'
        f'<g class="br">'
        f'<path d="{body}" fill="{fur}"/><path class="s" d="M-2 -42l2 12M11 -42l1 12M24 -40l-1 11" stroke="{shade}" stroke-width="4.5"/>'
        f'<path class="s" d="{body}" stroke="{p["ink"]}" stroke-width="{w}"/>'
        f'<path d="{ears}" fill="{fur}" stroke="{p["ink"]}" stroke-width="{w}" stroke-linejoin="round"/>'
        f'<path d="{head}" fill="{fur}" stroke="{p["ink"]}" stroke-width="{w}"/>'
        f'<path class="s" d="M-47 -37q4 4.4 8 0M-31 -37q4 4.4 8 0" stroke="{p["bug_ink"] if light else "#1a1512"}" stroke-width="2"/>'
        f'<path class="s" d="M-37 -30.5l2 2l2 -2M-55 -32l-10 -2M-55 -28l-10 2M-15 -32l10 -2M-15 -28l10 2" stroke="{p["bug_ink"] if light else "#1a1512"}" stroke-width="1.4"/>'
        f'</g></g>{z}</g>')


def studio():
    # The frame starts 96 down: room above it for the ivy and for the cat, ears and all.
    W, H, TOP = 1200, 456, 96
    s = STUDIO

    def draw(ink):
        p = ink.p
        ink.box(14, TOP, W - 30, H - TOP - 16, 26, at=0, dur=1.6, width=2.8)
        ink.logo("codeshare", 52, TOP + 40, 108, .4, ring=False, ratio=120 / 128)
        ink.text(BOLD, s["title"], 190, TOP + 86, 47, .45)
        w = ink.text(BOLD, s["url"], 192, TOP + 124, 24, .55, p["accent"])
        ink.text(TEXT, "·  " + s["tag"], 192 + w + 14, TOP + 124, 24, .6, p["soft"])
        ink.text(TEXT, s["desc"], 192, TOP + 164, 24, .7, p["soft"], fit=W - 250)
        # the products, as hand-drawn labels in a row
        x = 52
        for k, name in enumerate(s["products"]):
            w = TEXT.width(name, 21.5) + 36
            ink.box(x, TOP + 194, w, 38, 18, at=.7 + k * .07, dur=.5, width=1.9)
            ink.text(TEXT, name, x + w / 2, TOP + 220, 21.5, .8 + k * .07, anchor="middle")
            x += w + 14
        ink.stroke(smooth(hand_line(ink.rng, (46, TOP + 258), (W - 48, TOP + 256), 1.4, 70)), 1, .8, 1.8, opacity=".5")
        # the numbers, spread across the bottom
        parts = [(live(v), l) for v, l in s["stats"]]
        widths = [BOLD.width(v, 29) + 11 + TEXT.width(l, 22.5) for v, l in parts]
        space = (W - 104 - sum(widths)) / (len(parts) - 1)
        x = 52
        for k, ((v, l), tw) in enumerate(zip(parts, widths)):
            w = BOLD.width(v, 29)
            ink.marker(x - 2, TOP + 282, x + w + 2, TOP + 308, 1.1 + k * .1)
            ink.text(BOLD, v, x, TOP + 306, 29, 1.15 + k * .1)
            ink.text(TEXT, l, x + w + 11, TOP + 306, 22.5, 1.2 + k * .1, p["soft"])
            x += tw + space
        # ivy along the top of the frame, growing in from the left, and a cat asleep on the right
        ink.vine([(30, TOP + 4), (190, TOP - 6), (380, TOP + 4), (560, TOP - 8), (700, TOP)], at=1, speed=330, leaf=29, sway=5,
                 side=-1, both=False, curl=-1, width=2.4, gap=(44, 66), lean=(38, 112), first=18, berries=.3)
        cat(ink, 1010, TOP, 1.5)

    both("studio.svg", draw, W, H, seed=41)

# ───────────────────────────── PROJECTS ─────────────────────────────


def project(key, proj, n):
    W, H = 600, 290

    def draw(ink):
        p = ink.p
        ink.box(10, 50, W - 22, H - 62, 20, at=0, dur=1.2, width=2.5)
        ink.logo(key, 34, 78, 62, .35)
        ink.text(BOLD, proj["title"], 114, 110, 36, .4)
        ink.text(TEXT, proj["url"], 115, 138, 19.5, .5, p["accent"])
        for k, line in enumerate(proj["desc"]):
            ink.text(TEXT, line, 36, 186 + k * 28, 21, .6 + k * .1, p["soft"], fit=W - 76)
        x = 36
        for k, (v, l) in enumerate(proj["stats"]):
            v = live(v)
            w = BOLD.width(v, 21)
            ink.marker(x - 1, 238, x + w + 1, 258, .85 + k * .1)
            ink.text(BOLD, v, x, 257, 21, .9 + k * .1)
            lw = ink.text(TEXT, l, x + w + 8, 257, 19.5, .95 + k * .1, p["soft"])
            x += w + 8 + lw + 28
        # ivy along the top edge: from the right on one card, from the left on the next
        span = ink.rng.uniform(.44, .64) * W
        if n % 2 == 0:
            guide = [(W - 22, 56), (W - 22 - span * .35, 46), (W - 22 - span * .7, 54), (W - 22 - span, 46)]
            ink.vine(guide, at=.7, speed=250, leaf=27, sway=4, side=1, both=False, curl=1, width=2.2, gap=(42, 62), lean=(38, 112), first=16, berries=.28)
        else:
            guide = [(22, 56), (22 + span * .35, 46), (22 + span * .7, 54), (22 + span, 46)]
            ink.vine(guide, at=.7, speed=250, leaf=27, sway=4, side=-1, both=False, curl=-1, width=2.2, gap=(42, 62), lean=(38, 112), first=16, berries=.28)

    both(f"projects/{key}.svg", draw, W, H, seed=hash_seed(key) + 7)


if __name__ == "__main__":
    print("Drawing…")
    hero()
    links()
    headings()
    stats()
    studio()
    for n, (k, v) in enumerate(PROJECTS.items()):
        project(k, v, n)
    stack()
    print("Done.")
