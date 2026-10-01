#!/usr/bin/env python3
"""Builds the animated SVGs used by the profile README.

Edit the DATA section below, then run:  python3 scripts/generate.py
All files are written to ./assets.
"""
import base64
import json
from pathlib import Path

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
ROLES = [
    "Founder & CEO @ Codeshare Technology",
    "Full-Stack Developer",
    "AI Systems Researcher",
]

STATS = [
    (("home", "Discord users reached"), "Discord users reached"),
    (("home", "Discord servers"), "Discord servers"),
    (("home", "Minecraft players"), "Minecraft players"),
    ("44K+", "followers"),
]

STUDIO = dict(
    title="Codeshare Technology", url="codeshare.me",
    tag="Software studio · London",
    desc="Software for online communities — with the core kept free.",
    products=["Beatra", "Sylon", "MCStat", "JustDiscord", "JustAnime", "Dotrai"],
    stats=[(("about", "Products live"), "products live"),
           (("about", "Discord users reached"), "Discord users reached"),
           (("about", "Oldest account we own"), "oldest account"),
           (("about", "Company incorporated"), "incorporated")],
)

PROJECTS = {
    "mcstat": dict(
        title="MCStat", url="mcstat.org",
        desc=["Real-time Minecraft server list with live player",
              "counts, vote rankings and 50K+ player profiles."],
        stats=[(("mcstat", "Servers tracked"), "servers"), (("mcstat", "Player records"), "player records"),
               (("mcstat", "Skins archived"), "skins")],
    ),
    "beatra": dict(
        title="Beatra", url="beatra.app",
        desc=["Music bot for Discord, web and desktop —",
              "Spotify, YouTube, Apple Music and more."],
        stats=[(("beatra", "Discord servers"), "servers"), (("beatra", "Discord users"), "users")],
    ),
    "justdiscord": dict(
        title="JustDiscord", url="justdiscord.org",
        desc=["Discord server & bot list built on trust —",
              "real reviews, verified owners, free emojis."],
        stats=[(("justdiscord", "Server listings"), "servers"), (("justdiscord", "Bot listings"), "bots"),
               (("justdiscord", "Emojis and stickers"), "emojis")],
    ),
    "sylon": dict(
        title="Sylon", url="sylon.app",
        desc=["AI moderation for Discord that catches ads",
              "and scams in any language, even in images."],
        stats=[(("sylon", "Discord servers"), "servers"), (("sylon", "Discord users"), "users"),
               (("sylon", "Uptime"), "uptime")],
    ),
    "justanime": dict(
        title="JustAnime", url="justanime.me",
        desc=["Anime & manga tracker where every single",
              "episode gets its own rating and review."],
        stats=[(("justanime", "Anime and manga titles"), "titles"), (("justanime", "Character records"), "characters"),
               (("justanime", "Airing schedule entries"), "airing")],
    ),
    "dotrai": dict(
        title="Dotrai", url="dotrai.com",
        desc=["Free AI chat that searches the live web,",
              "runs real code and shows its reasoning."],
        stats=[],
    ),
}

# ───────────────────────────── THEME ────────────────────────────────

SANS = "'Segoe UI', Inter, 'Helvetica Neue', Ubuntu, Roboto, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
BG = "#07111f"
CARD = "#0a1628"
LINE = "#14304f"
BLUE = "#38bdf8"
BLUE_D = "#0284c7"
BLUE_L = "#bae6fd"
MUTED = "#7b93ad"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, style=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" fill="none">\n<style>{style}</style>\n{body}\n</svg>\n'
    )


def write(name, content):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  ✓ {path.relative_to(ROOT)}")


def logo(key):
    """Original logo from assets/logos, embedded so it renders inside an <img>."""
    data = base64.b64encode((OUT / "logos" / f"{key}.png").read_bytes()).decode()
    return f"data:image/png;base64,{data}"


def running_border(w, h, rx, dash, dur):
    """A thin card border with a short blue light travelling around it."""
    per = 2 * (w - 4 + h - 4)
    body = (f'<rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="{rx}" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>\n'
            f'<rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="{rx}" stroke="{BLUE}" stroke-width="2" stroke-linecap="round" class="run"/>')
    style = (f'.run{{stroke-dasharray:{dash} {per - dash};animation:run {dur}s linear infinite}}\n'
             f'@keyframes run{{to{{stroke-dashoffset:-{per}}}}}')
    return body, style


FADE_UP = '''.up{opacity:0;animation:up .9s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}'''

# ─────────────────────────────── HERO ───────────────────────────────

def hero():
    W, H = 1200, 320
    n = len(ROLES)
    roles = "".join(
        f'<text class="role" x="{W / 2}" y="214" text-anchor="middle" '
        f'style="animation-delay:{i * 3}s;animation-duration:{n * 3}s">{esc(r)}</text>'
        for i, r in enumerate(ROLES)
    )
    body = f'''<defs>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="24"/></clipPath>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="70"/></filter>
  <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.2" fill="{BLUE}"/></pattern>
  <radialGradient id="fade" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
  <mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <linearGradient id="name" x1="0" y1="0" x2="900" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="reflect">
    <stop offset="0" stop-color="{BLUE_L}"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{BLUE_D}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="0 0;900 0" dur="5s" repeatCount="indefinite"/>
  </linearGradient>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <g filter="url(#blur)" opacity=".5">
    <circle class="b1" cx="300" cy="80" r="170" fill="{BLUE_D}"/>
    <circle class="b2" cx="900" cy="260" r="190" fill="#1d4ed8"/>
  </g>
  <rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#m)"/>
  <text class="up" x="{W / 2}" y="152" text-anchor="middle" font-family="{SANS}" font-size="76" font-weight="800" letter-spacing="1" fill="url(#name)">{esc(NAME)}</text>
  <g class="up" style="animation-delay:.3s" font-family="{MONO}" font-size="22" fill="{BLUE_L}">{roles}</g>
  <rect width="{W}" height="{H}" rx="24" stroke="{LINE}" stroke-width="2"/>
</g>'''
    style = FADE_UP + '''
.b1{animation:d1 16s ease-in-out infinite alternate}
.b2{animation:d2 20s ease-in-out infinite alternate}
@keyframes d1{to{transform:translate(240px,60px)}}
@keyframes d2{to{transform:translate(-260px,-50px)}}
.role{opacity:0;animation-name:role;animation-iteration-count:infinite;animation-fill-mode:backwards}
@keyframes role{0%{opacity:0;transform:translateY(10px)}6%,27%{opacity:1;transform:none}33%,100%{opacity:0;transform:translateY(-10px)}}'''
    write("hero.svg", svg(W, H, body, style))


# ─────────────────────────────── STATS ──────────────────────────────

def stats():
    W, H = 1200, 130
    n = len(STATS)
    gap = 16
    cw = (W - gap * (n - 1)) / n
    out = []
    for i, (val, label) in enumerate(STATS):
        val = live(val)
        x = i * (cw + gap)
        out.append(f'''<g class="up" style="animation-delay:{i * .12:.2f}s">
  <rect x="{x + 1:.1f}" y="1" width="{cw - 2:.1f}" height="{H - 2}" rx="18" fill="{CARD}" stroke="{LINE}" stroke-width="1.5"/>
  <text x="{x + cw / 2:.1f}" y="70" text-anchor="middle" font-family="{SANS}" font-size="40" font-weight="800" fill="{BLUE}">{val}</text>
  <text x="{x + cw / 2:.1f}" y="100" text-anchor="middle" font-family="{SANS}" font-size="16" fill="{MUTED}">{esc(label)}</text>
</g>''')
    write("stats.svg", svg(W, H, "\n".join(out), FADE_UP))


# ────────────────────────────── STUDIO ──────────────────────────────

def studio():
    W, H = 1200, 260
    p = STUDIO
    border, style = running_border(W, H, 22, 220, 10)
    out = [border, f'''<image href="{logo("codeshare")}" x="40" y="44" width="104" height="112"/>
<text x="176" y="80" font-family="{SANS}" font-size="34" font-weight="800" fill="#f0f9ff">{esc(p["title"])}</text>
<text x="176" y="112" font-family="{MONO}" font-size="16" fill="{BLUE}">{esc(p["url"])}<tspan fill="{MUTED}">  ·  {esc(p["tag"])}</tspan></text>
<text x="176" y="148" font-family="{SANS}" font-size="18" fill="{MUTED}">{esc(p["desc"])}</text>''']
    half = (len(p["products"]) + 1) // 2
    for r, row in enumerate([p["products"][:half], p["products"][half:]]):
        x = W - 40
        for name in reversed(row):
            w = len(name) * 9 + 28
            x -= w
            out.append(f'<rect x="{x}" y="{58 + r * 46}" width="{w}" height="32" rx="16" fill="{BLUE}" fill-opacity=".1" stroke="{LINE}"/>'
                       f'<text x="{x + w / 2}" y="{79 + r * 46}" text-anchor="middle" font-family="{SANS}" font-size="15" fill="{BLUE_L}">{esc(name)}</text>')
            x -= 10
    out.append(f'<line x1="40" y1="186" x2="{W - 40}" y2="186" stroke="{LINE}"/>')
    cw = (W - 80) / len(p["stats"])
    for k, (v, l) in enumerate(p["stats"]):
        v = live(v)
        out.append(f'<text x="{40 + k * cw}" y="226" font-family="{SANS}" font-size="20"><tspan font-weight="800" fill="{BLUE}">{esc(v)}</tspan>'
                   f'<tspan fill="{MUTED}" font-size="16">  {esc(l)}</tspan></text>')
    write("studio.svg", svg(W, H, "\n".join(out), style))


# ───────────────────────────── PROJECTS ─────────────────────────────

def project(key, p):
    W, H = 600, 230
    border, style = running_border(W, H, 20, 140, 8)
    out = [border, f'''<clipPath id="lc"><rect x="26" y="26" width="64" height="64" rx="16"/></clipPath>
<image href="{logo(key)}" x="26" y="26" width="64" height="64" clip-path="url(#lc)"/>
<text x="108" y="56" font-family="{SANS}" font-size="28" font-weight="700" fill="#f0f9ff">{esc(p["title"])}</text>
<text x="108" y="82" font-family="{MONO}" font-size="15" fill="{BLUE}">{esc(p["url"])}</text>''']
    for k, line in enumerate(p["desc"]):
        out.append(f'<text x="30" y="{134 + k * 25}" font-family="{SANS}" font-size="17" fill="{MUTED}">{esc(line)}</text>')
    for k, (v, l) in enumerate(p["stats"]):
        v = live(v)
        out.append(f'<text x="{30 + k * 186}" y="{H - 30}" font-family="{SANS}" font-size="17"><tspan font-weight="700" fill="{BLUE_L}">{esc(v)}</tspan>'
                   f'<tspan fill="{MUTED}"> {esc(l)}</tspan></text>')
    write(f"projects/{key}.svg", svg(W, H, "\n".join(out), style))


if __name__ == "__main__":
    print("Generating assets…")
    hero()
    stats()
    studio()
    for k, v in PROJECTS.items():
        project(k, v)
    print("Done.")
