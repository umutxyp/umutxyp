#!/usr/bin/env python3
"""Builds the animated SVGs used by the profile README.

Edit the DATA section below, then run:  python3 scripts/generate.py
All files are written to ./assets.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# ─────────────────────────────── DATA ───────────────────────────────

NAME = "Umut Bayraktar"
ROLES = [
    "Full-Stack Developer",
    "AI Systems Researcher",
    "Building Beatra · MCStat · JustDiscord",
]

STATS = [
    ("2.1M+", "Discord users"),
    ("250K+", "daily players"),
    ("16K+", "listings"),
    ("44K+", "followers"),
]

PROJECTS = {
    "mcstat": dict(
        title="MCStat", url="mcstat.org", icon="cube",
        desc=["Real-time Minecraft server list with live player",
              "counts, vote rankings and 50K+ player profiles."],
        stats=[("6.7K", "servers"), ("250K", "daily peak")],
    ),
    "beatra": dict(
        title="Beatra", url="beatra.app", icon="eq",
        desc=["Music bot for Discord, web and desktop —",
              "Spotify, YouTube, Apple Music and more."],
        stats=[("32.8K", "servers"), ("2.1M+", "users")],
    ),
    "justdiscord": dict(
        title="JustDiscord", url="justdiscord.org", icon="chat",
        desc=["Discord server & bot list built on trust —",
              "real reviews, verified owners, free emojis."],
        stats=[("16K+", "listings"), ("91K", "emojis")],
    ),
    "sylon": dict(
        title="Sylon", url="sylon.app", icon="shield",
        desc=["AI moderation for Discord that catches ads",
              "and scams in any language, even in images."],
        stats=[("33K+", "users"), ("99.9%", "uptime")],
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
        x = i * (cw + gap)
        out.append(f'''<g class="up" style="animation-delay:{i * .12:.2f}s">
  <rect x="{x + 1:.1f}" y="1" width="{cw - 2:.1f}" height="{H - 2}" rx="18" fill="{CARD}" stroke="{LINE}" stroke-width="1.5"/>
  <text x="{x + cw / 2:.1f}" y="70" text-anchor="middle" font-family="{SANS}" font-size="40" font-weight="800" fill="{BLUE}">{val}</text>
  <text x="{x + cw / 2:.1f}" y="100" text-anchor="middle" font-family="{SANS}" font-size="16" fill="{MUTED}">{esc(label)}</text>
</g>''')
    write("stats.svg", svg(W, H, "\n".join(out), FADE_UP))


# ───────────────────────────── PROJECTS ─────────────────────────────

def icon(kind):
    if kind == "eq":
        return "".join(
            f'<rect x="{-17 + k * 9}" y="-14" width="6" height="28" rx="3" fill="{BLUE}" class="eq" '
            f'style="animation-delay:-{0.2 * k:.1f}s"/>' for k in range(4))
    if kind == "cube":
        return (f'<path d="M0 -18 L16 -9 L0 0 L-16 -9 Z" fill="{BLUE_L}"/>'
                f'<path d="M-16 -9 L0 0 L0 18 L-16 9 Z" fill="{BLUE_D}"/>'
                f'<path d="M16 -9 L0 0 L0 18 L16 9 Z" fill="{BLUE}"/>')
    if kind == "chat":
        return (f'<path d="M-18 -14 Q-18 -18 -14 -18 H14 Q18 -18 18 -14 V4 Q18 8 14 8 H-3 L-11 16 V8 H-14 Q-18 8 -18 4 Z" fill="{BLUE}"/>'
                f'<path d="M0 -12 L2 -7 L7 -7 L3 -4 L4.5 1 L0 -2 L-4.5 1 L-3 -4 L-7 -7 L-2 -7 Z" fill="{BG}"/>')
    return (f'<path d="M0 -19 L16 -12 V0 Q16 13 0 20 Q-16 13 -16 0 V-12 Z" fill="{BLUE}"/>'
            f'<path d="M-6 1 L-1.5 5.5 L7 -4" stroke="{BG}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


def project(key, p):
    W, H = 600, 230
    per = 2 * (W - 4 + H - 4)
    out = [f'''<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="20" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="20" stroke="{BLUE}" stroke-width="2" stroke-linecap="round" class="run"/>
<g transform="translate(58 60)"><rect x="-28" y="-28" width="56" height="56" rx="14" fill="{BLUE}" fill-opacity=".1"/>{icon(p["icon"])}</g>
<text x="104" y="56" font-family="{SANS}" font-size="28" font-weight="700" fill="#f0f9ff">{esc(p["title"])}</text>
<text x="104" y="82" font-family="{MONO}" font-size="15" fill="{BLUE}">{esc(p["url"])}</text>''']
    for k, line in enumerate(p["desc"]):
        out.append(f'<text x="30" y="{128 + k * 25}" font-family="{SANS}" font-size="17" fill="{MUTED}">{esc(line)}</text>')
    x = 30
    for v, l in p["stats"]:
        out.append(f'<text x="{x}" y="{H - 30}" font-family="{SANS}" font-size="17"><tspan font-weight="700" fill="{BLUE_L}">{esc(v)}</tspan>'
                   f'<tspan fill="{MUTED}"> {esc(l)}</tspan></text>')
        x += 180
    style = f'''.run{{stroke-dasharray:140 {per - 140};animation:run 8s linear infinite}}
@keyframes run{{to{{stroke-dashoffset:-{per}}}}}
.eq{{transform-box:fill-box;transform-origin:center bottom;animation:eq .8s ease-in-out infinite alternate}}
@keyframes eq{{from{{transform:scaleY(.3)}}to{{transform:scaleY(1)}}}}'''
    write(f"projects/{key}.svg", svg(W, H, "\n".join(out), style))


if __name__ == "__main__":
    print("Generating assets…")
    hero()
    stats()
    for k, v in PROJECTS.items():
        project(k, v)
    print("Done.")
