#!/usr/bin/env python3
"""Draws the pictures of the profile README: ink lines, a blue fox by the sea, hand lettering.

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

# *…* is written heavier and gets a marker swipe; {products} is the studio's list below.
ABOUT = ("I'm *Umut* — full-stack developer, AI systems researcher and content creator with 6+ years of building "
         "platforms end to end. I'm the founder & CEO of *Codeshare Technology*, the software studio behind {products}. "
         "The company was incorporated in 2025, but most of the products are older than it — the first one dates back "
         "to 2020. The core of every product stays free, and I run all of it myself.")

OPEN_SOURCE = [
    ("MusicBot", "Discord.js v14 music bot — YouTube, Spotify, SoundCloud"),
    ("Seo-Promt-Master", "Google's SEO docs as an AI prompt — audit and fix every page"),
    ("Discord-Bot-Website", "React + Tailwind website theme for Discord bots"),
    ("Personal-Website", "Hand-drawn Next.js portfolio with seven animated worlds to pick from"),
    ("Shroudly", "Free anti-censorship app: opens blocked YouTube, Instagram, X, Facebook, Discord, Telegram, WhatsApp, "
                 "Wikipedia, Roblox, League of Legends and news, without a VPN — Windows 7 to 11, macOS, Linux, Android, "
                 "Android TV, iPhone, iPad and Apple TV"),
    ("v14-discord-bot", "discord.js v14 slash and prefix command boilerplate"),
]

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

# The page draws itself from the top down: every picture waits its turn. Seconds after loading.
START = dict(hero=0.0, links=2.3, about_heading=3.0, about=3.3, stats=4.0, projects_heading=4.6, studio=4.9,
             cards=5.6, stack_heading=7.1, stack=7.3, opensource_heading=7.8, opensource=8.0)
HEADING_START = dict(about="about_heading", projects="projects_heading", stack="stack_heading", opensource="opensource_heading")

# ───────────────────────────── PALETTES ─────────────────────────────
# A blue fox by the sea: the blues of the profile picture, navy ink, and a little coral.
# Transparent pictures, so the page itself is the paper: dark ink on GitHub's light theme,
# pale ink on its dark one. The README picks the file with <picture>.

PALETTES = {
    "light": dict(ink="#14273d", soft="#4d6379", leaf=["#86cfe0", "#4fa9cc", "#b5e2ee"],
                  accent="#2188e0", warm="#ff8559", marker="#bfe2ff", marker_op=".9",
                  wash="#d6ecfa", wash_op=".8", deep="#bcdcf2",
                  fur="#4aa8f2", fur2="#2c7fd6", mask="#f6fbff", paper="#ffffff", dark="#14273d"),
    "dark": dict(ink="#e4eef8", soft="#9db1c6", leaf=["#2f86b3", "#51aad6", "#1f6790"],
                 accent="#47b8f5", warm="#ff9770", marker="#1d5c8f", marker_op=".6",
                 wash="#10283c", wash_op=".85", deep="#15344e",
                 fur="#3f9ff0", fur2="#2a78cf", mask="#eaf4ff", paper="#1b3a55", dark="#0b1826"),
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

def wave(rng, x0, x1, y, amp=6.0, span=110.0, rough=1.2):
    """A sea line: gentle crests, never quite the same twice."""
    pts, x, up = [], x0, rng.choice((-1, 1))
    while x < x1:
        pts.append((x, y + up * amp * rng.uniform(.7, 1.15) + rng.uniform(-rough, rough)))
        x += span / 2 * rng.uniform(.82, 1.2)
        up = -up
    pts.append((x1, y + up * amp * .6))
    return pts

# ─────────────────────────────── INK ────────────────────────────────

STYLE = """
.d{fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;opacity:0;animation:d 1s linear forwards}
@keyframes d{0%{stroke-dashoffset:1;opacity:1}100%{stroke-dashoffset:0;opacity:1}}
.s{fill:none;stroke-linecap:round;stroke-linejoin:round}
.lf{transform:scale(0);animation:lf .9s cubic-bezier(.34,1.56,.64,1) forwards}
@keyframes lf{to{transform:scale(1)}}
.sw{animation:sw 4s ease-in-out infinite alternate}
@keyframes sw{from{transform:rotate(-7deg)}to{transform:rotate(7deg)}}
.bb{opacity:0;animation:bb 4s ease-in infinite}
@keyframes bb{0%{opacity:0;transform:translateY(8px) scale(.6)}18%{opacity:1}80%{opacity:.9}100%{opacity:0;transform:translateY(-30px) scale(1.05)}}
.bob{animation:bob 3.4s ease-in-out infinite alternate}
@keyframes bob{from{transform:translateY(1.5px) rotate(-3.5deg)}to{transform:translateY(-3.5px) rotate(3deg)}}
.wv{animation:wv 7s ease-in-out infinite alternate}
@keyframes wv{from{transform:translateX(-14px)}to{transform:translateX(14px)}}
.cl{animation:cl 11s ease-in-out infinite alternate}
@keyframes cl{from{transform:translateX(-10px)}to{transform:translateX(16px)}}
.br{animation:br 2.8s ease-in-out infinite alternate}
@keyframes br{from{transform:scale(1,1)}to{transform:scale(1.012,1.05)}}
.tl{animation:tl 3.4s ease-in-out infinite alternate}
@keyframes tl{from{transform:rotate(-5deg)}to{transform:rotate(4deg)}}
.zz{opacity:0;animation:zz 3.9s ease-in-out infinite}
@keyframes zz{0%{opacity:0;transform:translate(3px,7px)}35%{opacity:.85}100%{opacity:0;transform:translate(-9px,-17px)}}
.i{opacity:0;animation:i .7s ease forwards}
@keyframes i{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}
.w{stroke-dasharray:1;stroke-dashoffset:1;fill-opacity:0;stroke-linejoin:round;stroke-linecap:round;animation:w 1.2s ease forwards}
@keyframes w{0%{stroke-dashoffset:1;fill-opacity:0}60%{stroke-dashoffset:0;fill-opacity:0}100%{stroke-dashoffset:0;fill-opacity:1}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.d{stroke-dashoffset:0;opacity:1}.lf{transform:none}.i{opacity:1}.w{stroke-dashoffset:0;fill-opacity:1}.zz{opacity:.7}.bb{opacity:.85}}
"""


class Ink:
    """One picture being drawn, in one palette."""

    def __init__(self, w, h, pal, seed, start=0.0):
        self.w, self.h, self.p, self.start = w, h, pal, start
        self.rng = random.Random(seed)
        self.body, self.defs = [], []

    def add(self, s):
        self.body.append(s)

    # a line that draws itself: `at` seconds after the picture's turn comes, taking `dur`
    def stroke(self, d, at=0.0, dur=0.8, width=2.4, color=None, opacity=None):
        self.add(self.line(d, at, dur, width, color, opacity))

    def line(self, d, at=0.0, dur=0.8, width=2.4, color=None, opacity=None):
        op = f' stroke-opacity="{opacity}"' if opacity else ""
        return (f'<path class="d" pathLength="1" d="{d}" stroke="{color or self.p["ink"]}" stroke-width="{width}"{op} '
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

    # ── sea plants ──

    def leaf(self, size):
        """A blade of sea grass pointing along +x from the origin: (outline, midrib)."""
        rng = self.rng
        w, bend = rng.uniform(.17, .27) * size, rng.uniform(-.14, .14) * size
        outline = (f"M0 0C{f(size * .2)} {f(-w * 1.15)} {f(size * .62)} {f(-w * .9 + bend)} {f(size)} {f(bend)}"
                   f"C{f(size * .66)} {f(w * .75 + bend)} {f(size * .24)} {f(w * 1.05)} 0 0Z")
        rib = f"M{f(size * .06)} 0Q{f(size * .5)} {f(bend * .45)} {f(size * .86)} {f(bend * .9)}"
        return outline, rib

    def bubbles(self, x, y, at, n=2, r=(2.6, 5.2)):
        """A few bubbles that keep rising from (x, y) once the picture has got this far."""
        rng, p = self.rng, self.p
        out = []
        for k in range(n):
            rad = rng.uniform(*r)
            bx, by = x + rng.uniform(-9, 9), y + rng.uniform(-6, 6)
            out.append(
                f'<g transform="translate({f(bx)} {f(by)})"><g class="bb" style="animation-duration:{rng.uniform(3.2, 5.6):.1f}s;'
                f'animation-delay:{at + rng.uniform(0, 3.5):.2f}s">'
                f'<circle r="{f(rad)}" fill="{p["mask"]}" fill-opacity=".55" stroke="{p["ink"]}" stroke-width="1.4"/>'
                f'<path class="s" d="M{f(-rad * .45)} {f(-rad * .1)}A{f(rad * .5)} {f(rad * .5)} 0 0 1 {f(-rad * .05)} {f(-rad * .5)}" stroke="{p["ink"]}" stroke-width="1" stroke-opacity=".7"/>'
                f'</g></g>')
        self.add("".join(out))

    def vine(self, guide, at=0.0, speed=300, leaf=30, gap=(46, 70), sway=6.0, side=1, both=True, curl=1, width=2.6,
             lean=(48, 78), taper=.55, first=26, bubbles=0.0):
        """Sea grass that grows along `guide`. Returns the stem's path data and the time it has finished growing."""
        rng, p = self.rng, self.p
        pts = sample(guide, 5)
        total = length(pts)
        wavel, ph1, ph2 = rng.uniform(150, 200), rng.uniform(0, 6.28), rng.uniform(0, 6.28)
        out, s = [], 0.0
        for i, pt in enumerate(pts):
            a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
            tx, ty = b[0] - a[0], b[1] - a[1]
            n = math.hypot(tx, ty) or 1
            if i:
                s += math.dist(pts[i - 1], pt)
            env = min(1, s / 40) * min(1, (total - s) / 30 + .3)
            off = (math.sin(s / wavel * 6.283 + ph1) * sway + math.sin(s / (wavel * .37) * 6.283 + ph2) * sway * .22) * env
            out.append((pt[0] - ty / n * off, pt[1] + tx / n * off, s, math.atan2(ty, tx)))
        if curl:                                      # the tip curls
            x, y, s, ang = out[-1]
            for k in range(26):
                ang += curl * (0.13 + 0.017 * k)
                st = 5.2 * (1 - k / 34)
                x, y, s = x + math.cos(ang) * st, y + math.sin(ang) * st, s + st
                out.append((x, y, s, ang))
        full = out[-1][2]
        stem = smooth([(q[0], q[1]) for q in out[::3]] + [(out[-1][0], out[-1][1])])
        self.stroke(stem, at, full / speed, width)
        nxt, flip, i = first, side, 0                 # blades, each opening as the stem reaches it
        blades = []
        while i < len(out):
            x, y, s, ang = out[i]
            if s >= nxt and s < total - 10:
                k = 1 - (1 - taper) * max(0, (s - total * .55) / (total * .45))
                size = leaf * rng.uniform(.8, 1.2) * k
                turn = ang + flip * math.radians(rng.uniform(*lean))
                blades.append((x, y, turn, size, at + s / speed + .05, rng.choice(p["leaf"])))
                if bubbles and rng.random() < bubbles and s > 40:
                    self.bubbles(x + math.cos(turn) * size * .9, y + math.sin(turn) * size * .9 - 6, at + s / speed + .6, rng.choice((1, 2)))
                nxt = s + rng.uniform(*gap) * (.75 + .25 * k)
                if both:
                    flip = -flip
            i += 1
        for x, y, turn, size, t, fill in blades:
            outline, rib = self.leaf(size)
            self.add(
                f'<g transform="translate({f(x)} {f(y)}) rotate({f(math.degrees(turn))})">'
                f'<g class="lf" style="animation-delay:{t:.2f}s">'
                f'<g class="sw" style="animation-duration:{rng.uniform(3.2, 6.4):.1f}s;animation-delay:-{rng.uniform(0, 6):.1f}s">'
                f'<path d="{outline}" fill="{fill}" transform="translate({f(size * .05)} {f(size * .06)})"/>'
                f'<path class="s" d="{outline}" stroke="{p["ink"]}" stroke-width="{f(width * .8)}"/>'
                f'<path class="s" d="{rib}" stroke="{p["ink"]}" stroke-width="1.1" stroke-opacity=".65"/>'
                f'</g></g></g>')
        return stem, at + full / speed

    def render(self):
        defs = f'<defs>{"".join(self.defs)}</defs>' if self.defs else ""
        body = "".join(self.body)
        if self.start:
            # the whole picture waits for its turn (the sway, which runs from the start, is left alone)
            body = re.sub(r"animation-delay:(\d*\.?\d+)s", lambda m: f"animation-delay:{float(m.group(1)) + self.start:.2f}s", body)
            body = re.sub(r'begin="(\d[\d.]*)s"', lambda m: f'begin="{float(m.group(1)) + self.start:.1f}s"', body)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" fill="none">'
                f'<style>{STYLE.strip()}</style>{defs}{body}</svg>\n')


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


def both(name, draw, w, h, seed, start=0.0):
    """Draws one picture in both palettes, with the same hand (the same seed), starting `start` seconds in."""
    for theme, pal in PALETTES.items():
        ink = Ink(w, h, pal, seed, start)
        draw(ink)
        write(theme, name, ink)
    print(f"  ✓ {name}")


def hash_seed(s):
    return sum((i + 1) * ord(c) for i, c in enumerate(s)) % 9973

# ────────────────────────────── THE FOX ─────────────────────────────
# The fox of the profile picture: a diamond of a face under two tall ears, in its blues.


def fox_head(p, asleep=False, w=2.3):
    """The head, about 52 wide, its middle at the origin."""
    eyes = ("M-14 -5q3.6 3.8 7.2 0M6.8 -5q3.6 3.8 7.2 0" if asleep else "")
    dots = "" if asleep else f'<circle cx="-10" cy="-5" r="2.5" fill="{p["dark"]}"/><circle cx="10" cy="-5" r="2.5" fill="{p["dark"]}"/>'
    return (
        f'<path d="M-21 -13L-25 -43L-5 -19ZM21 -13L25 -43L5 -19Z" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}" stroke-linejoin="round"/>'
        f'<path d="M-19 -19L-21.5 -35L-10 -21ZM19 -19L21.5 -35L10 -21Z" fill="{p["fur2"]}"/>'
        f'<path d="M-27 -2L-15 -19L15 -19L27 -2L0 23Z" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="{w}" stroke-linejoin="round"/>'
        f'<path d="M-25.5 -1.5L-8 5L0 -2L8 5L25.5 -1.5L0 21.5Z" fill="{p["mask"]}"/>'
        f'<path class="s" d="M-27 -2L-15 -19L15 -19L27 -2L0 23Z" stroke="{p["ink"]}" stroke-width="{w}"/>'
        f'<path class="s" d="{eyes}" stroke="{p["dark"]}" stroke-width="2"/>{dots}'
        f'<path d="M-3.2 17.2L3.2 17.2L0 21.2Z" fill="{p["dark"]}" stroke="{p["dark"]}" stroke-width="1.4" stroke-linejoin="round"/>')


def sleeping_fox(ink, cx, base, at):
    """The fox curled up asleep on a line, its tail around it."""
    p, w = ink.p, 2.5
    body = "M-42 1C-50 -26 -30 -43 -2 -43C28 -43 50 -27 48 1Z"
    tail = "M44 -13C62 -9 62 6 40 4C14 2 -8 5 -26 -1C-14 -17 12 -21 30 -18C37 -17 41 -17 44 -13Z"
    tip = "M-26 -1C-18 -11 -8 -15 2 -17.5L5 2.6C-6 2.6 -17 2 -26 -1Z"
    z = "".join(
        f'<g transform="translate({x} {y})"><path class="zz" d="{BOLD.d("z", 0, 0, s)[0]}" fill="{p["soft"]}" style="animation-delay:{at + 1.2 + k * 1.3:.2f}s"/></g>'
        for k, (x, y, s) in enumerate(((-92, -52, 15), (-107, -64, 18), (-123, -76, 21))))
    ink.add(
        f'<g transform="translate({cx} {base})"><g class="i" style="animation-delay:{at:.2f}s">'
        f'<g class="br"><path d="{body}" fill="{p["fur"]}"/>'
        f'<path class="s" d="M6 -43q3 7 1 13M20 -41q3 6 1 12" stroke="{p["fur2"]}" stroke-width="4"/>'
        f'<path class="s" d="{body}" stroke="{p["ink"]}" stroke-width="{w}"/></g>'
        f'<g class="tl"><path d="{tail}" fill="{p["fur"]}"/><path d="{tip}" fill="{p["mask"]}"/>'
        f'<path class="s" d="{tail}" stroke="{p["ink"]}" stroke-width="{w}"/></g>'
        f'<g transform="translate(-46 -24) rotate(-9)">{fox_head(p, asleep=True, w=w)}</g>'
        f'</g>{z}</g>')


def boat(ink, x, y, at, fox=True, k=1.0):
    """A paper boat riding the waves, the fox looking out of it."""
    p = ink.p
    hull = "M-52 -2L52 -2L35 22L-35 22Z"
    sail = "M-17 -2L1 -44L19 -2Z"
    crew = (f'<path d="M30 -2C38 -26 58 -24 54 -6C53 -1 46 1 40 -2Z" fill="{p["fur"]}" stroke="{p["ink"]}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<path d="M46.5 -20.5C54 -20 56.5 -13 54 -6C52 -11 49 -15 44.5 -16.5Z" fill="{p["mask"]}"/>'
            f'<g transform="translate(-33 -19) scale(.86)">{fox_head(p, w=2.5)}</g>') if fox else ""
    ink.add(
        f'<g transform="translate({x} {y}) scale({k})"><g class="i" style="animation-delay:{at:.2f}s"><g class="bob">{crew}'
        f'<path d="{sail}" fill="{p["paper"]}" stroke="{p["ink"]}" stroke-width="2.3" stroke-linejoin="round"/>'
        f'<path class="s" d="M1 -44L1 -58M1 -58L15 -53L1 -48" stroke="{p["ink"]}" stroke-width="2"/><path d="M1 -58L15 -53L1 -48Z" fill="{p["warm"]}"/>'
        f'<path d="{hull}" fill="{p["paper"]}" stroke="{p["ink"]}" stroke-width="2.3" stroke-linejoin="round"/>'
        f'<path class="s" d="M-17 -2L0 22L19 -2" stroke="{p["ink"]}" stroke-width="1.5" stroke-opacity=".55"/>'
        f'</g></g></g>')


def fish_shape(p, color):
    """A small fish swimming towards +x, its middle at the origin."""
    return (f'<path d="M-9 0L-19 -7L-16 0L-19 7Z" fill="{color}" stroke="{p["ink"]}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M-11 0C-6 -8 6 -8 12 0C6 8 -6 8 -11 0Z" fill="{color}" stroke="{p["ink"]}" stroke-width="1.5"/>'
            f'<path class="s" d="M-1 -5.5q3 5.5 0 11" stroke="{p["ink"]}" stroke-width="1.1" stroke-opacity=".6"/>'
            f'<circle cx="6.5" cy="-1.6" r="1.4" fill="{p["dark"]}"/>')


def swimmer(ink, path, begin, dur, color, k=1.0):
    """A fish that swims the path over and over, fading in and out at its ends."""
    ink.add(f'<g opacity="0"><g transform="scale({k})">{fish_shape(ink.p, color)}</g>'
            f'<animateMotion path="{path}" dur="{dur}s" begin="{begin:.1f}s" repeatCount="indefinite" rotate="auto"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.04;0.95;1" dur="{dur}s" begin="{begin:.1f}s" repeatCount="indefinite"/></g>')


def cloud(ink, x, y, k, at):
    p = ink.p
    d = ("M-58 14C-76 14 -78 -8 -58 -10C-58 -30 -30 -36 -20 -20C-10 -42 26 -40 30 -16C48 -24 66 -8 54 8C62 14 56 22 46 20"
         "C30 22 -30 22 -58 14Z")
    ink.add(f'<g transform="translate({x} {y}) scale({k})"><g class="cl" style="animation-delay:-{ink.rng.uniform(0, 8):.1f}s">'
            f'<path class="i" d="{d}" fill="{p["wash"]}" fill-opacity="{p["wash_op"]}" style="animation-delay:{at:.2f}s"/>'
            f'{ink.line(d, at, 1.1, 2.2 / k)}</g></g>')


def gull(ink, x, y, k, at):
    ink.add(f'<g transform="translate({x} {y}) scale({k})">{ink.line("M-13 1Q-7 -9 0 0Q7 -9 13 1", at, .5, 2.2 / k)}</g>')

# ─────────────────────────────── HERO ───────────────────────────────


def hero():
    W, H, SEA = 1200, 548, 440

    def draw(ink):
        p, rng = ink.p, ink.rng
        # the sky
        cloud(ink, 132, 76, 1.0, .3)
        cloud(ink, 1062, 62, .78, .5)
        gull(ink, 874, 104, 1.0, 1.1)
        gull(ink, 918, 84, .72, 1.3)
        gull(ink, 300, 46, .66, 1.5)
        # the name, written letter by letter
        letters, w = NAME_FACE.letters(NAME, W / 2, 238, 138, "middle")
        for k, d in enumerate(letters):
            ink.add(f'<path class="w" pathLength="1" d="{d}" fill="{p["ink"]}" stroke="{p["ink"]}" stroke-width="1.6" '
                    f'style="animation-delay:{.4 + k * .06:.2f}s"/>')
        t = .4 + len(letters) * .06 + .45
        # a wave under it instead of a straight line
        x0, x1 = W / 2 - w / 2 + 30, W / 2 + w / 2 - 10
        ink.stroke(smooth(wave(rng, x0, x1, 280, 5, 74)), t, .6, 4.4, p["accent"])
        ink.stroke(smooth(wave(rng, x0 + (x1 - x0) * .38, x1 - 12, 293, 3.5, 66)), t + .4, .4, 2.8, p["accent"], ".7")
        # what he does
        size, gap = 25.5, 52
        sizes = [TEXT.width(r, size) for r in ROLES]
        x = W / 2 - (sum(sizes) + gap * (len(ROLES) - 1)) / 2
        for k, (r, rw) in enumerate(zip(ROLES, sizes)):
            ink.text(TEXT, r, x, 346, size, t + .3 + k * .15, p["soft"])
            if k < len(ROLES) - 1:
                ink.add(f'<g class="i" style="animation-delay:{t + .4 + k * .15:.2f}s"><g transform="translate({f(x + rw + gap / 2)} 338) scale(.82)">'
                        f'{fish_shape(p, p["leaf"][k % 3])}</g></g>')
            x += rw + gap
        # the sea: its surface drifting a little, deeper water under it
        top = wave(rng, -40, W + 40, SEA, 6.5, 118)
        ink.add(f'<g class="wv"><path class="i" d="{smooth(top)}L{W + 40} {H + 10}L-40 {H + 10}Z" fill="{p["wash"]}" fill-opacity="{p["wash_op"]}" style="animation-delay:.5s"/>'
                f'{ink.line(smooth(top), .2, 1.5, 2.8)}</g>')
        low = wave(rng, -40, W + 40, SEA + 46, 5, 150)
        ink.add(f'<g class="wv" style="animation-duration:9s;animation-delay:-3s">'
                f'<path class="i" d="{smooth(low)}L{W + 40} {H + 10}L-40 {H + 10}Z" fill="{p["deep"]}" fill-opacity=".55" style="animation-delay:.8s"/></g>')
        for a, b, yy in ((150, 320, SEA + 26), (560, 700, SEA + 30), (860, 980, SEA + 24)):
            ink.stroke(smooth(wave(rng, a, b, yy, 3, 60)), 1.4, .5, 1.8, opacity=".45")
        # sea grass growing up from the bottom, left and right
        for gx, top_y, lf, t0, sd in ((54, SEA + 22, 30, 1.0, 1), (112, SEA + 44, 24, 1.3, -1), (176, SEA + 62, 19, 1.5, 1),
                                      (1150, SEA + 26, 29, 1.2, -1), (1092, SEA + 50, 22, 1.5, 1), (742, SEA + 66, 18, 1.7, 1)):
            ink.vine([(gx, H + 12), (gx + rng.uniform(-10, 10), (H + top_y) / 2), (gx + rng.uniform(-12, 12), top_y)], at=t0, speed=110,
                     leaf=lf, sway=4, side=sd, curl=0, width=2.3, gap=(17, 24), first=10, taper=.7, lean=(22, 44), bubbles=.3)
        # fish below, the boat above with the fox aboard
        swimmer(ink, smooth(wave(rng, -40, W + 40, SEA + 58, 9, 190)), 3.2, 46, p["warm"], 1.05)
        swimmer(ink, smooth(wave(rng, -40, W + 40, SEA + 84, 7, 160)), 9.0, 61, p["leaf"][1], .8)
        ink.bubbles(420, SEA + 70, 2.2, 2)
        ink.bubbles(905, SEA + 78, 2.6, 2)
        boat(ink, 1060, SEA - 9, 1.7, k=1.22)

    both("hero.svg", draw, W, H, seed=11, start=START["hero"])

# ───────────────────────────── SMALL PARTS ──────────────────────────


def links():
    for n, (key, label) in enumerate(LINKS):
        size, pad, h = 30, 26, 76
        W = int(BOLD.width(label, size) + pad * 2 + 22)

        def draw(ink, label=label, W=W):
            ink.box(8, 18, W - 22, 48, 23, at=.1, dur=.8, width=2.4)
            ink.text(BOLD, label, 8 + (W - 22) / 2, 52, size, .35, anchor="middle")
            ink.bubbles(W - 14, 20, .7, 2, (2.6, 4.6))     # bubbles off the top right corner

        both(f"links/{key}.svg", draw, W, h, seed=hash_seed(key), start=START["links"] + n * .06)


def headings():
    W, H = 1200, 104
    for n, (key, label) in enumerate(HEADINGS):
        def draw(ink, label=label, n=n):
            p, rng = ink.p, ink.rng
            w = ink.text(BOLD, label, 6, 68, 52, .1)
            ink.stroke(smooth(wave(rng, 4, w + 14, 84, 3.2, 52)), .3, .5, 4.4, p["accent"])
            # the sea running off to the right, something sailing or swimming along it
            x0 = w + 48
            line = wave(rng, x0, 1176, 62, 6, 116)
            ink.stroke(smooth(line), .4, 1.2, 2.3)
            ink.stroke(smooth(wave(rng, x0 + 90, x0 + 250, 82, 3, 60)), 1, .4, 1.6, opacity=".4")
            ink.stroke(smooth(wave(rng, 820, 1010, 84, 3, 60)), 1.1, .4, 1.6, opacity=".4")
            if n % 2 == 0:
                bx = rng.uniform(x0 + 240, 980)
                boat(ink, bx, 52, 1.2, fox=False, k=.5)
            else:
                swimmer(ink, smooth([(q[0], q[1] + 20) for q in line]), 1.6, 40, p["warm"], .95)
            ink.bubbles(rng.uniform(x0 + 60, 1100), 82, 1.4, 2, (2.4, 4.2))

        both(f"headings/{key}.svg", draw, W, H, seed=hash_seed(key) + 3, start=START[HEADING_START[key]])


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
                # a blade or two of sea grass between two numbers, bubbles rising off it
                x = col * k
                ink.vine([(x + ink.rng.uniform(-4, 4), 112), (x + ink.rng.uniform(-7, 7), 80), (x + ink.rng.uniform(-5, 5), 50)],
                         at=.5 + k * .2, speed=130, leaf=24, sway=2.5, side=ink.rng.choice((-1, 1)), curl=0,
                         width=2, gap=(16, 22), first=10, taper=.8, lean=(24, 46))
                ink.bubbles(x, 40, .9 + k * .2, 2, (2.4, 4.4))

    both("stats.svg", draw, W, H, seed=23, start=START["stats"])


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
                # a little wave under each word, each one different
                ink.stroke(smooth(wave(ink.rng, x - 2, x + w + 3, y + 12, 2.4, 40, .6)), .3 + k * .05, .35, 2.8,
                           p["accent"] if k % 3 == 0 else p["leaf"][1])
                x += w + gap
                k += 1

    both("stack.svg", draw, W, H, seed=31, start=START["stack"])

# ────────────────────────────── STUDIO ──────────────────────────────


def studio():
    # The frame starts 96 down: room above it for the sea grass and for the fox, ears and all.
    W, H, TOP = 1200, 440, 96
    s = STUDIO

    def draw(ink):
        p = ink.p
        ink.box(14, TOP, W - 30, H - TOP - 16, 26, at=0, dur=1.6, width=2.8)
        ink.logo("codeshare", 54, TOP + 42, 62, .4, ring=False, ratio=120 / 128)
        ink.text(BOLD, s["title"], 132, TOP + 76, 44, .45)
        w = ink.text(BOLD, s["url"], 134, TOP + 110, 23, .55, p["accent"])
        ink.text(TEXT, "·  " + s["tag"], 134 + w + 14, TOP + 110, 23, .6, p["soft"])
        ink.text(TEXT, s["desc"], 54, TOP + 156, 24, .7, p["soft"], fit=W - 110)
        # the products, as hand-drawn labels in a row
        x = 52
        for k, name in enumerate(s["products"]):
            w = TEXT.width(name, 21.5) + 36
            ink.box(x, TOP + 180, w, 38, 18, at=.7 + k * .07, dur=.5, width=1.9)
            ink.text(TEXT, name, x + w / 2, TOP + 206, 21.5, .8 + k * .07, anchor="middle")
            x += w + 14
        ink.stroke(smooth(wave(ink.rng, 46, W - 48, TOP + 243, 2.2, 150, .8)), 1, .8, 1.8, opacity=".5")
        # the numbers, spread across the bottom
        parts = [(live(v), l) for v, l in s["stats"]]
        widths = [BOLD.width(v, 29) + 11 + TEXT.width(l, 22.5) for v, l in parts]
        space = (W - 104 - sum(widths)) / (len(parts) - 1)
        x = 52
        for k, ((v, l), tw) in enumerate(zip(parts, widths)):
            w = BOLD.width(v, 29)
            ink.marker(x - 2, TOP + 268, x + w + 2, TOP + 294, 1.1 + k * .1)
            ink.text(BOLD, v, x, TOP + 292, 29, 1.15 + k * .1)
            ink.text(TEXT, l, x + w + 11, TOP + 292, 22.5, 1.2 + k * .1, p["soft"])
            x += tw + space
        # sea grass along the top of the frame, growing in from the left, and the fox asleep on the right
        ink.vine([(30, TOP + 4), (190, TOP - 6), (380, TOP + 4), (560, TOP - 8), (700, TOP)], at=1, speed=330, leaf=34, sway=5,
                 side=-1, both=False, curl=-1, width=2.4, gap=(30, 48), lean=(62, 104), first=14, bubbles=.25)
        sleeping_fox(ink, 1016, TOP, 1.5)

    both("studio.svg", draw, W, H, seed=41, start=START["studio"])

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
        # sea grass along the top edge: from the right on one card, from the left on the next
        span = ink.rng.uniform(.44, .64) * W
        if n % 2 == 0:
            guide = [(W - 22, 56), (W - 22 - span * .35, 46), (W - 22 - span * .7, 54), (W - 22 - span, 46)]
            ink.vine(guide, at=.7, speed=250, leaf=31, sway=4, side=1, both=False, curl=1, width=2.2, gap=(28, 44), lean=(62, 104), first=12, bubbles=.28)
        else:
            guide = [(22, 56), (22 + span * .35, 46), (22 + span * .7, 54), (22 + span, 46)]
            ink.vine(guide, at=.7, speed=250, leaf=31, sway=4, side=-1, both=False, curl=-1, width=2.2, gap=(28, 44), lean=(62, 104), first=12, bubbles=.28)

    # two cards to a row: the left one a moment before the right, each row after the one above
    both(f"projects/{key}.svg", draw, W, H, seed=hash_seed(key) + 7, start=START["cards"] + (n // 2) * .35 + (n % 2) * .12)

# ─────────────────────────── WRITTEN PARTS ──────────────────────────


def about_text():
    names = STUDIO["products"]
    return ABOUT.format(products=", ".join(names[:-1]) + " and " + names[-1])


def wrap(text, size, width):
    """Breaks text into lines. A line is [(word, heavy, x, w)], *…* marking the heavy words."""
    tokens = []                                   # (word, heavy, glued to the word before)
    before = " "
    for n, part in enumerate(text.split("*")):
        # glued only when neither side of the * has a space: "*Codeshare Technology*," keeps its comma
        glued = bool(tokens) and not before[-1:].isspace() and not part[:1].isspace()
        for k, word in enumerate(part.split()):
            tokens.append((word, n % 2 == 1, glued and k == 0))
        before = part or before
    space = TEXT.width(" ", size)
    lines, line, x = [], [], 0.0
    i = 0
    while i < len(tokens):
        # a word and whatever is glued to it (a comma after a heavy word) stay together
        group = [tokens[i]]
        while i + len(group) < len(tokens) and tokens[i + len(group)][2]:
            group.append(tokens[i + len(group)])
        gw = sum((BOLD if h else TEXT).width(w, size) for w, h, _ in group)
        if line and x + space + gw > width:
            lines.append(line)
            line, x = [], 0.0
        if line:
            x += space
        for w, h, _ in group:
            ww = (BOLD if h else TEXT).width(w, size)
            line.append((w, h, x, ww))
            x += ww
        i += len(group)
    lines.append(line)
    return lines


def write_lines(ink, lines, x0, y0, size, step, at, color):
    """Writes wrapped lines; heavy words in the ink colour with a marker swipe behind each run of them."""
    p = ink.p
    for n, line in enumerate(lines):
        y, t = y0 + n * step, at + n * .11
        k = 0
        while k < len(line):
            if line[k][1]:
                j = k
                while j + 1 < len(line) and line[j + 1][1]:
                    j += 1
                ink.marker(x0 + line[k][2] - 3, y - size * .78, x0 + line[j][2] + line[j][3] + 3, y + size * .2, t)
                k = j + 1
            else:
                k += 1
        for word, heavy, x, _ in line:
            ink.text(BOLD if heavy else TEXT, word, x0 + x, y, size, t + .05, p["ink"] if heavy else color)


def about():
    W, size, step, x0 = 1200, 27.5, 41, 66
    lines = wrap(about_text(), size, W - x0 - 14)
    H = 34 + step * len(lines) + 14

    def draw(ink):
        # sea grass growing up the margin, bubbles rising off it
        ink.vine([(28, H + 10), (20, H * .68), (36, H * .36), (24, 26)], at=.1, speed=210, leaf=27, sway=4, side=1,
                 curl=1, width=2.2, gap=(26, 38), first=24, taper=.7, lean=(26, 50), bubbles=.3)
        write_lines(ink, lines, x0, 46, size, step, .2, ink.p["soft"])

    both("about.svg", draw, W, H, seed=53, start=START["about"])


def starfish(ink, cx, cy, r, at):
    """Stars are counted in starfish here."""
    rng, p = ink.rng, ink.p
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5 + rng.uniform(-.07, .07)
        rr = (r if k % 2 == 0 else r * .5) * rng.uniform(.93, 1.07)
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d = smooth(pts, closed=True)
    ink.add(f'<g class="i" style="animation-delay:{at:.2f}s"><path d="{d}" fill="{p["warm"]}" transform="translate(1.4 1.3)"/>'
            f'<path d="{d}" fill="none" stroke="{p["ink"]}" stroke-width="1.9" stroke-linejoin="round"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="1.3" fill="{p["ink"]}" fill-opacity=".6"/></g>')


def open_source():
    W, size, step, x0 = 1200, 23.5, 33, 58
    github = LIVE.get("github", {})
    for n, (repo, desc) in enumerate(OPEN_SOURCE):
        lines = wrap(desc, size, W - x0 - 20)
        H = 96 + step * len(lines)

        def draw(ink, repo=repo, lines=lines, H=H, n=n):
            p = ink.p
            # a small fish for a bullet, each a little different
            ink.add(f'<g transform="translate(26 {40 + ink.rng.uniform(-2, 2):.1f}) rotate({ink.rng.uniform(-10, 10):.1f})"><g class="lf" style="animation-delay:.15s">'
                    f'<g class="sw" style="animation-duration:{ink.rng.uniform(2.6, 4.2):.1f}s;animation-delay:-{ink.rng.uniform(0, 4):.1f}s">'
                    f'<g transform="scale(1.12)">{fish_shape(p, p["leaf"][n % 3])}</g></g></g></g>')
            w = ink.text(BOLD, repo, x0, 50, 33, .1)
            ink.stroke(smooth(wave(ink.rng, x0 - 2, x0 + w + 4, 62, 2.4, 44, .6)), .3, .4, 3, p["accent"] if n % 2 == 0 else p["leaf"][1])
            count = github.get(f"{repo} stars")
            if count:
                cw = BOLD.width(count, 25)
                ink.text(BOLD, count, W - 30, 49, 25, .35, anchor="end")
                starfish(ink, W - 30 - cw - 24, 40, 15, .3)
            write_lines(ink, lines, x0, 96, size, step, .3, p["soft"])
            if n < len(OPEN_SOURCE) - 1:
                ink.stroke(smooth(wave(ink.rng, x0 - 4, W - 16, H - 8, 1.8, 170, .6)), .5, .7, 1.5, opacity=".32")

        both(f"opensource/{repo.lower()}.svg", draw, W, H, seed=hash_seed(repo) + 5, start=START["opensource"] + n * .18)


if __name__ == "__main__":
    print("Drawing…")
    hero()
    links()
    headings()
    about()
    stats()
    studio()
    for n, (k, v) in enumerate(PROJECTS.items()):
        project(k, v, n)
    stack()
    open_source()
    print("Done.")
