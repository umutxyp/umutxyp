#!/usr/bin/env python3
"""Builds every animated SVG used by the profile README.

Edit the DATA section below, then run:  python3 scripts/generate.py
All files are written to ./assets.
"""
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# ─────────────────────────────── DATA ───────────────────────────────

NAME = "UMUT BAYRAKTAR"
ROLES = [
    "full-stack developer",
    "founder of beatra · mcstat · justdiscord",
    "ai systems researcher",
    "building for millions of users",
]

STATS = [
    # value, label, sub-label, accent
    ("2.1M+", "DISCORD USERS", "Beatra", "#c084fc"),
    ("250K+", "DAILY PLAYERS", "MCStat", "#4ade80"),
    ("16K+", "LISTINGS", "JustDiscord", "#818cf8"),
    ("2.7K+", "GITHUB STARS", "Open source", "#facc15"),
    ("44K+", "FOLLOWERS", "Social", "#f472b6"),
]

PROJECTS = {
    "mcstat": dict(
        title="MCStat",
        url="mcstat.org",
        tag="Minecraft server & player platform",
        desc=[
            "Real-time server list with live player counts,",
            "uptime history, vote rankings & 50K+ player",
            "profiles. A signed-telemetry plugin feeds it.",
        ],
        stats=[("6.7K", "servers"), ("227K", "online now"), ("250K", "daily peak")],
        tech=["Next.js", "TypeScript", "PostgreSQL", "Redis"],
        c1="#4ade80", c2="#16a34a", icon="cube",
    ),
    "beatra": dict(
        title="Beatra",
        url="beatra.app",
        tag="Multi-platform music for Discord",
        desc=[
            "Discord, web, desktop & Activities. YouTube,",
            "Spotify, Apple Music, Deezer, Tidal and more —",
            "smart autoplay, filters & Beatra Wrapped.",
        ],
        stats=[("32.8K", "servers"), ("2.1M+", "users"), ("99%", "uptime")],
        tech=["Discord.js", "React", "Electron", "Lavalink"],
        c1="#c084fc", c2="#db2777", icon="eq",
    ),
    "justdiscord": dict(
        title="JustDiscord",
        url="justdiscord.org",
        tag="Discord server & bot list built on trust",
        desc=[
            "Scored listings with reviews that explain the",
            "score, Discord-verified ownership, a huge free",
            "emoji library and a public API with webhooks.",
        ],
        stats=[("8.1K", "servers"), ("8.2K", "bots"), ("91K", "emojis")],
        tech=["Next.js", "PostgreSQL", "Prisma", "Edge"],
        c1="#818cf8", c2="#4f46e5", icon="chat",
    ),
    "sylon": dict(
        title="Sylon",
        url="sylon.app",
        tag="AI-powered Discord moderation",
        desc=[
            "Catches ads, invites & scams in any language —",
            "even text hidden inside images. Tickets, anti-",
            "raid, leveling, giveaways & a web dashboard.",
        ],
        stats=[("33K+", "users"), ("AI", "vision"), ("99.9%", "uptime")],
        tech=["Node.js", "Discord API", "MongoDB", "AI/ML"],
        c1="#22d3ee", c2="#0284c7", icon="shield",
    ),
}

SECTIONS = {
    "about": ("01", "ABOUT ME", "whoami"),
    "stats": ("02", "BY THE NUMBERS", "impact"),
    "projects": ("03", "WHAT I'M BUILDING", "live in production"),
    "stack": ("04", "TECH STACK", "tools of the trade"),
    "oss": ("05", "OPEN SOURCE", "free for everyone"),
    "activity": ("06", "GITHUB ACTIVITY", "commit log"),
}

TERMINAL = [
    ("cmd", "whoami"),
    ("out", [("Umut Bayraktar", "#e2e8f0"), (" — full-stack developer & product builder", "#94a3b8")]),
    ("cmd", "cat profile.yml"),
    ("kv", "name", "Umut Bayraktar  (@umutxyp)"),
    ("kv", "born", "2005-09-15 · Antalya, TR"),
    ("kv", "building", "Beatra · MCStat · JustDiscord · Sylon"),
    ("kv", "stack", "Next.js · TypeScript · Node.js · PostgreSQL · Redis"),
    ("kv", "focus", "high-traffic platforms · AI systems · Discord · SEO"),
    ("kv", "community", "6+ years · 44K+ followers"),
    ("kv", "status", "open to collaborations ✓"),
]

# ───────────────────────────── HELPERS ──────────────────────────────

SANS = "'Segoe UI', Inter, 'Helvetica Neue', Ubuntu, Roboto, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', 'Cascadia Code', Consolas, 'Liberation Mono', Menlo, monospace"
BG = "#05070d"


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
    print(f"  ✓ {path.relative_to(ROOT)}  ({len(content) / 1024:.1f} KB)")


# ─────────────────────────────── HERO ───────────────────────────────

def hero():
    W, H = 1200, 460
    rnd = random.Random(7)
    horizon, bottom = 300, H
    out = []

    out.append(f'''<defs>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="28"/></clipPath>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="10" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <linearGradient id="name" x1="0" y1="0" x2="1200" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="repeat">
    <stop offset="0" stop-color="#22d3ee"/><stop offset="0.25" stop-color="#a78bfa"/>
    <stop offset="0.5" stop-color="#f472b6"/><stop offset="0.75" stop-color="#a78bfa"/>
    <stop offset="1" stop-color="#22d3ee"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1200 0;0 0" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="gridFade" x1="0" y1="{horizon}" x2="0" y2="{bottom}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.35" stop-color="#fff" stop-opacity="0.55"/>
    <stop offset="1" stop-color="#fff" stop-opacity="1"/>
  </linearGradient>
  <mask id="gridMask"><rect x="0" y="{horizon}" width="{W}" height="{bottom - horizon}" fill="url(#gridFade)"/></mask>
  <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f472b6"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="vignette" cx="0.5" cy="0.45" r="0.75">
    <stop offset="0.55" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}" stop-opacity="0.9"/>
  </radialGradient>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{BG}"/>''')

    # aurora blobs
    blobs = [(220, 120, 210, "#0891b2", "a1", 18), (980, 90, 230, "#7c3aed", "a2", 22),
             (620, 40, 180, "#db2777", "a3", 16), (420, 360, 160, "#4f46e5", "a4", 20)]
    out.append('<g filter="url(#blur)" opacity="0.55">')
    for x, y, r, c, cls, _ in blobs:
        out.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="{r}" fill="{c}"/>')
    out.append('</g>')

    # stars
    out.append('<g>')
    for i in range(90):
        x, y = rnd.uniform(10, W - 10), rnd.uniform(8, horizon - 20)
        r = rnd.choice([0.6, 0.8, 1, 1.2, 1.6])
        d, dl = rnd.uniform(2, 5), rnd.uniform(0, 5)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#e0f2fe" class="tw" '
                   f'style="animation-duration:{d:.1f}s;animation-delay:-{dl:.1f}s"/>')
    out.append('</g>')

    # shooting stars
    for i, (x, y, dl) in enumerate([(300, 40, 1), (900, 20, 5.5), (650, 70, 9)]):
        out.append(f'<line class="shoot" x1="{x}" y1="{y}" x2="{x - 90}" y2="{y + 45}" stroke="url(#sun)" '
                   f'stroke-width="2" stroke-linecap="round" style="animation-delay:{dl}s"/>')

    # synthwave sun behind horizon
    out.append(f'<g opacity="0.35"><circle cx="{W / 2}" cy="{horizon + 10}" r="110" fill="url(#sun)"/>')
    for k in range(6):
        yy = horizon - 56 + k * 12
        out.append(f'<rect x="{W / 2 - 130}" y="{yy}" width="260" height="{2 + k * 1.2:.1f}" fill="{BG}"/>')
    out.append('</g>')

    # perspective grid
    out.append(f'<g mask="url(#gridMask)" stroke="#38bdf8" stroke-width="1.2">')
    cx = W / 2
    for k in range(-24, 25):
        x2 = cx + k * 110
        out.append(f'<line x1="{cx + k * 6:.1f}" y1="{horizon}" x2="{x2:.1f}" y2="{bottom}" stroke-opacity="0.5"/>')
    N, dur = 12, 3.2
    span = bottom - horizon
    for i in range(N):
        vals = []
        for s in range(9):
            t = (i + s / 8) / N
            vals.append(f"{horizon + span * t * t:.1f}")
        v = ";".join(vals)
        out.append(f'<line x1="0" x2="{W}" y1="{vals[0]}" y2="{vals[0]}" stroke-opacity="0.7">'
                   f'<animate attributeName="y1" values="{v}" dur="{dur}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="y2" values="{v}" dur="{dur}s" repeatCount="indefinite"/></line>')
    out.append(f'</g><line x1="0" x2="{W}" y1="{horizon}" y2="{horizon}" stroke="#f472b6" stroke-opacity="0.6" stroke-width="1.5"/>')

    out.append(f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')

    # status pill
    out.append(f'''<g class="up" style="animation-delay:.1s">
  <rect x="{W / 2 - 118}" y="62" width="236" height="34" rx="17" fill="#0b1220" fill-opacity="0.75" stroke="#4ade80" stroke-opacity="0.45"/>
  <circle cx="{W / 2 - 94}" cy="79" r="5" fill="#4ade80"/>
  <circle cx="{W / 2 - 94}" cy="79" r="5" fill="none" stroke="#4ade80" class="ping"/>
  <text x="{W / 2 + 10}" y="84.5" text-anchor="middle" font-family="{MONO}" font-size="14" fill="#bbf7d0" letter-spacing="1">OPEN TO COLLABORATE</text>
</g>''')

    # name
    out.append(f'''<g class="up" style="animation-delay:.3s">
  <text x="{W / 2}" y="190" text-anchor="middle" font-family="{SANS}" font-size="92" font-weight="900" letter-spacing="6" fill="url(#name)" filter="url(#glow)" opacity="0.55">{NAME}</text>
  <text x="{W / 2}" y="190" text-anchor="middle" font-family="{SANS}" font-size="92" font-weight="900" letter-spacing="6" fill="url(#name)">{NAME}</text>
</g>''')

    # rotating roles
    n = len(ROLES)
    out.append(f'<g class="up" style="animation-delay:.55s" font-family="{MONO}" font-size="24">')
    for i, r in enumerate(ROLES):
        out.append(f'<g class="role" style="animation-delay:{i * 3}s;animation-duration:{n * 3}s">'
                   f'<text x="{W / 2}" y="246" text-anchor="middle"><tspan fill="#f472b6">&gt; </tspan>'
                   f'<tspan fill="#e0f2fe">{esc(r)}</tspan><tspan fill="#22d3ee" class="cur">▍</tspan></text></g>')
    out.append('</g>')

    out.append(f'<rect width="{W}" height="{H}" rx="28" stroke="#1e293b" stroke-width="2" fill="none"/></g>')

    style = f'''
.a1{{animation:d1 18s ease-in-out infinite alternate}}
.a2{{animation:d2 22s ease-in-out infinite alternate}}
.a3{{animation:d3 16s ease-in-out infinite alternate}}
.a4{{animation:d1 20s ease-in-out infinite alternate-reverse}}
@keyframes d1{{to{{transform:translate(260px,60px)}}}}
@keyframes d2{{to{{transform:translate(-300px,90px)}}}}
@keyframes d3{{to{{transform:translate(-200px,120px)}}}}
.tw{{animation:tw 3s ease-in-out infinite}}
@keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:1}}}}
.shoot{{opacity:0;animation:shoot 12s linear infinite}}
@keyframes shoot{{0%{{opacity:0;transform:translate(0,0)}}2%{{opacity:1}}8%{{opacity:0;transform:translate(-260px,130px)}}100%{{opacity:0}}}}
.up{{opacity:0;animation:up 1s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(24px)}}to{{opacity:1;transform:none}}}}
.ping{{transform-box:fill-box;transform-origin:center;animation:ping 1.6s ease-out infinite}}
@keyframes ping{{from{{transform:scale(1);opacity:.9}}to{{transform:scale(3.2);opacity:0}}}}
.role{{opacity:0;animation-name:role;animation-iteration-count:infinite;animation-fill-mode:backwards;animation-timing-function:ease}}
@keyframes role{{0%{{opacity:0;transform:translateY(14px)}}4%,21%{{opacity:1;transform:none}}25%,100%{{opacity:0;transform:translateY(-14px)}}}}
.cur{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
'''
    write("hero.svg", svg(W, H, "\n".join(out), style))


# ───────────────────────────── SECTIONS ─────────────────────────────

def section(key, num, title, hint):
    W, H = 1200, 84
    tw = len(title) * 19 + 20
    body = f'''<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="#0a0f1a" stroke="#1e293b" stroke-width="1.5"/>
<g transform="translate(28 0)">
<defs>
  <linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset=".5" stop-color="#a78bfa"/><stop offset="1" stop-color="#f472b6" stop-opacity="0"/></linearGradient>
  <linearGradient id="tx" x1="0" x2="1"><stop offset="0" stop-color="#e0f2fe"/><stop offset="1" stop-color="#a5b4fc"/></linearGradient>
</defs>
<text x="2" y="52" font-family="{MONO}" font-size="20" fill="#f472b6" class="f" style="animation-delay:0s">{num}</text>
<text x="40" y="52" font-family="{MONO}" font-size="20" fill="#475569" class="f" style="animation-delay:.1s">/</text>
<text x="64" y="54" font-family="{SANS}" font-size="30" font-weight="800" letter-spacing="4" fill="url(#tx)" class="f" style="animation-delay:.2s">{esc(title)}</text>
<line x1="{64 + tw}" y1="44" x2="{W - 290}" y2="44" stroke="url(#ln)" stroke-width="2" class="draw"/>
<circle r="3.5" cy="44" fill="#fff" class="dot" style="filter:drop-shadow(0 0 6px #22d3ee)"><animate attributeName="cx" values="{64 + tw};{W - 290}" dur="3s" begin="1s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" dur="3s" begin="1s" repeatCount="indefinite"/></circle>
<text x="{W - 60}" y="50" text-anchor="end" font-family="{MONO}" font-size="16" fill="#64748b" class="f" style="animation-delay:.5s">// {esc(hint)}</text>
</g>'''
    L = W - 290 - (64 + tw)
    style = f'''.f{{opacity:0;animation:f .7s ease forwards}}
@keyframes f{{from{{opacity:0;transform:translateX(-12px)}}to{{opacity:1;transform:none}}}}
.draw{{stroke-dasharray:{L};stroke-dashoffset:{L};animation:dr 1.4s .4s cubic-bezier(.6,0,.2,1) forwards}}
@keyframes dr{{to{{stroke-dashoffset:0}}}}'''
    write(f"sections/{key}.svg", svg(W, H, body, style))


# ───────────────────────────── TERMINAL ─────────────────────────────

def terminal():
    W, LH, top = 1200, 34, 86
    H = top + LH * len(TERMINAL) + 30
    t, out = 0.6, []
    out.append(f'''<defs>
  <linearGradient id="bd" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#22d3ee"/><stop offset=".5" stop-color="#a78bfa"/><stop offset="1" stop-color="#f472b6"/>
  </linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22d3ee" stop-opacity="0"/><stop offset="1" stop-color="#22d3ee" stop-opacity=".07"/></linearGradient>
  <clipPath id="win"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18"/></clipPath>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="#0a0f1a"/>
<g clip-path="url(#win)">
  <rect width="{W}" height="52" fill="#0f172a"/>
  <line x1="0" y1="52" x2="{W}" y2="52" stroke="#1e293b"/>
  <circle cx="30" cy="26" r="7" fill="#ff5f57"/><circle cx="54" cy="26" r="7" fill="#febc2e"/><circle cx="78" cy="26" r="7" fill="#28c840"/>
  <text x="{W / 2}" y="31" text-anchor="middle" font-family="{MONO}" font-size="14" fill="#64748b">umut@dev — ~/profile — zsh</text>
  <rect class="scan" x="0" y="-120" width="{W}" height="120" fill="url(#scan)"/>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" stroke="url(#bd)" stroke-opacity=".55" stroke-width="2"/>''')

    def prompt(y):
        return (f'<tspan fill="#4ade80">umut</tspan><tspan fill="#64748b">@</tspan><tspan fill="#22d3ee">dev</tspan>'
                f'<tspan fill="#64748b">:</tspan><tspan fill="#a78bfa">~</tspan><tspan fill="#64748b">$ </tspan>')

    cw = 12.6  # approx monospace char width at 21px
    pw = len("umut@dev:~$ ") * cw
    y = top
    for i, row in enumerate(TERMINAL):
        if row[0] == "cmd":
            cmd = row[1]
            typing = max(0.35, len(cmd) * 0.06)
            out.append(f'<g class="ln" style="animation-delay:{t:.2f}s"><text x="32" y="{y}" font-family="{MONO}" font-size="21">{prompt(y)}</text></g>')
            out.append(f'<clipPath id="c{i}"><rect x="{32 + pw}" y="{y - 26}" height="36" width="0">'
                       f'<animate attributeName="width" from="0" to="{len(cmd) * cw + 4:.0f}" begin="{t + 0.25:.2f}s" dur="{typing:.2f}s" '
                       f'fill="freeze" calcMode="discrete" keyTimes="{";".join(f"{k / len(cmd):.3f}" for k in range(len(cmd)))}" '
                       f'values="{";".join(f"{(k + 1) * cw + 4:.1f}" for k in range(len(cmd)))}"/></rect></clipPath>')
            out.append(f'<text x="{32 + pw:.0f}" y="{y}" font-family="{MONO}" font-size="21" fill="#f8fafc" clip-path="url(#c{i})">{esc(cmd)}</text>')
            t += 0.25 + typing + 0.25
        elif row[0] == "out":
            spans = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in row[1])
            out.append(f'<g class="ln" style="animation-delay:{t:.2f}s"><text x="32" y="{y}" font-family="{MONO}" font-size="21">{spans}</text></g>')
            t += 0.25
        else:
            _, k, v = row
            pad = " " * (11 - len(k))
            ok = v.endswith("✓")
            vc = "#4ade80" if ok else "#e2e8f0"
            out.append(f'<g class="ln" style="animation-delay:{t:.2f}s"><text x="32" y="{y}" font-family="{MONO}" font-size="21" xml:space="preserve">'
                       f'<tspan fill="#f472b6">{k}</tspan><tspan fill="#64748b">:{pad}</tspan><tspan fill="{vc}">{esc(v)}</tspan></text></g>')
            t += 0.14
        y += LH
    out.append(f'<g class="ln" style="animation-delay:{t:.2f}s"><text x="32" y="{y}" font-family="{MONO}" font-size="21">{prompt(y)}</text>'
               f'<rect x="{32 + pw + 2:.0f}" y="{y - 19}" width="12" height="24" fill="#22d3ee" class="cur"/></g>')

    style = '''.ln{opacity:0;animation:ln .01s forwards}
@keyframes ln{to{opacity:1}}
.cur{animation:blink 1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.scan{animation:scan 6s linear infinite}
@keyframes scan{to{transform:translateY(''' + str(H + 240) + '''px)}}'''
    write("terminal.svg", svg(W, H, "\n".join(out), style))


# ─────────────────────────────── STATS ──────────────────────────────

def stats():
    W, H = 1200, 210
    n = len(STATS)
    gap = 16
    cw = (W - gap * (n - 1)) / n
    fs, dh = 50, 72  # number font size, digit cell height
    out = ['<defs>']
    for i, (_, _, _, c) in enumerate(STATS):
        out.append(f'<linearGradient id="g{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c}" stop-opacity=".22"/>'
                   f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></linearGradient>')
    out.append('</defs>')

    for i, (val, label, sub, c) in enumerate(STATS):
        x0 = i * (cw + gap)
        delay = 0.15 * i
        out.append(f'<g class="pop" style="animation-delay:{delay:.2f}s">')
        out.append(f'<rect x="{x0 + 1:.1f}" y="1" width="{cw - 2:.1f}" height="{H - 2}" rx="18" fill="#0a0f1a" stroke="#1e293b" stroke-width="1.5"/>')
        out.append(f'<rect x="{x0 + 1:.1f}" y="1" width="{cw - 2:.1f}" height="{H / 2}" rx="18" fill="url(#g{i})"/>')
        out.append(f'<rect x="{x0 + 30:.1f}" y="0" width="{cw - 60:.1f}" height="3" rx="1.5" fill="{c}" class="bar" style="animation-delay:{delay + .4:.2f}s"/>')

        # odometer number
        widths = {".": 15, "+": 30, "M": 44, "K": 34}
        total = sum(widths.get(ch, 30) for ch in val)
        x = x0 + cw / 2 - total / 2
        base = 108
        out.append(f'<clipPath id="nc{i}"><rect x="{x0}" y="{base - 42}" width="{cw}" height="52"/></clipPath>')
        out.append(f'<g clip-path="url(#nc{i})" font-family="{SANS}" font-weight="800" font-size="{fs}" fill="#f8fafc">')
        for j, ch in enumerate(val):
            w = widths.get(ch, 30)
            if ch.isdigit():
                d = int(ch)
                seq = list(range(10)) + list(range(d + 1))  # roll one full turn then land
                col = "".join(f'<text x="{x + w / 2:.1f}" y="{base + k * dh}" text-anchor="middle">{s}</text>' for k, s in enumerate(seq))
                land = -(len(seq) - 1) * dh
                b = 0.5 + delay + j * 0.12
                out.append(f'<g transform="translate(0 {land})">'
                           f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {land}" '
                           f'dur="{1.6 + j * 0.15:.2f}s" begin="{b:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".15 .7 .1 1"/>'
                           f'<set attributeName="transform" to="translate(0 0)" begin="0s" dur="{b:.2f}s"/>{col}</g>')
            else:
                fill = c if ch in "+MK" else "#f8fafc"
                out.append(f'<text x="{x + w / 2:.1f}" y="{base}" text-anchor="middle" fill="{fill}">{ch}</text>')
            x += w
        out.append('</g>')
        out.append(f'<text x="{x0 + cw / 2:.1f}" y="148" text-anchor="middle" font-family="{MONO}" font-size="14" letter-spacing="2" fill="#cbd5e1">{label}</text>')
        out.append(f'<text x="{x0 + cw / 2:.1f}" y="176" text-anchor="middle" font-family="{SANS}" font-size="15" fill="{c}">{sub}</text>')
        out.append('</g>')

    style = '''.pop{opacity:0;animation:pop .8s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes pop{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
.bar{transform-box:fill-box;transform-origin:center;transform:scaleX(0);animation:bar 1s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes bar{to{transform:scaleX(1)}}'''
    write("stats.svg", svg(W, H, "\n".join(out), style))


# ───────────────────────────── PROJECTS ─────────────────────────────

def icon(kind, c1, c2):
    if kind == "eq":
        bars = []
        for k in range(5):
            d = 0.7 + 0.13 * k
            bars.append(f'<rect x="{-22 + k * 10}" y="-18" width="6" height="36" rx="3" fill="url(#ac)" class="eq" '
                        f'style="animation-duration:{d:.2f}s;animation-delay:-{0.17 * k:.2f}s"/>')
        return "".join(bars)
    if kind == "cube":
        return ('<g class="float"><path d="M0 -24 L22 -12 L0 0 L-22 -12 Z" fill="url(#ac)"/>'
                f'<path d="M-22 -12 L0 0 L0 24 L-22 12 Z" fill="{c2}"/>'
                f'<path d="M22 -12 L0 0 L0 24 L22 12 Z" fill="{c1}" fill-opacity=".55"/>'
                '<path d="M-11 -18 L0 -12 L11 -18" stroke="#052e16" stroke-opacity=".35" stroke-width="2"/></g>')
    if kind == "chat":
        star = "M0 -9 L2.6 -2.8 L9 -2.8 L3.8 1.2 L5.6 7.6 L0 3.8 L-5.6 7.6 L-3.8 1.2 L-9 -2.8 L-2.6 -2.8 Z"
        return (f'<path d="M-24 -18 Q-24 -24 -18 -24 H18 Q24 -24 24 -18 V6 Q24 12 18 12 H-4 L-14 22 V12 H-18 Q-24 12 -24 6 Z" fill="url(#ac)"/>'
                f'<path d="{star}" fill="#fff" transform="translate(0 -6)" class="spin"/>')
    # shield
    return (f'<clipPath id="sh"><path d="M0 -26 L22 -17 V0 Q22 18 0 27 Q-22 18 -22 0 V-17 Z"/></clipPath>'
            f'<path d="M0 -26 L22 -17 V0 Q22 18 0 27 Q-22 18 -22 0 V-17 Z" fill="url(#ac)"/>'
            f'<g clip-path="url(#sh)"><rect x="-24" y="-30" width="48" height="5" fill="#fff" opacity=".7" class="scanY"/></g>'
            '<path d="M-8 1 L-2 7 L10 -6" stroke="#fff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')


def project(key, p):
    W, H = 600, 366
    c1, c2 = p["c1"], p["c2"]
    P = 2 * (W - 4 + H - 4)
    out = [f'''<defs>
  <linearGradient id="ac" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
  <radialGradient id="glow" cx="0.12" cy="0.1" r="0.8"><stop offset="0" stop-color="{c1}" stop-opacity=".22"/><stop offset="1" stop-color="{c1}" stop-opacity="0"/></radialGradient>
  <linearGradient id="run" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c1}" stop-opacity="0"/><stop offset=".5" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#94a3b8" fill-opacity=".12"/></pattern>
</defs>
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="22" fill="#0a0f1a"/>
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="22" fill="url(#dots)"/>
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="22" fill="url(#glow)"/>
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="22" stroke="#1e293b" stroke-width="2"/>
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="22" stroke="{c1}" stroke-width="2.5" stroke-linecap="round" class="snake"/>''']

    # icon tile
    out.append(f'<g transform="translate(64 70)"><rect x="-34" y="-34" width="68" height="68" rx="18" fill="{c1}" fill-opacity=".1" stroke="{c1}" stroke-opacity=".35"/>'
               f'{icon(p["icon"], c1, c2)}</g>')

    # title + url + live badge
    out.append(f'<text x="118" y="66" font-family="{SANS}" font-size="32" font-weight="800" fill="#f8fafc">{esc(p["title"])}</text>')
    out.append(f'<text x="118" y="94" font-family="{MONO}" font-size="15" fill="{c1}">↗ {esc(p["url"])}</text>')
    out.append(f'<g transform="translate({W - 96} 44)"><rect width="66" height="26" rx="13" fill="#052e16" stroke="#4ade80" stroke-opacity=".5"/>'
               f'<circle cx="16" cy="13" r="4" fill="#4ade80" class="live"/>'
               f'<text x="27" y="17.5" font-family="{MONO}" font-size="12" fill="#86efac" letter-spacing="1">LIVE</text></g>')

    out.append(f'<text x="34" y="140" font-family="{SANS}" font-size="17" font-weight="700" fill="#e2e8f0">{esc(p["tag"])}</text>')
    for k, line in enumerate(p["desc"]):
        out.append(f'<text x="34" y="{168 + k * 24}" font-family="{SANS}" font-size="16.5" fill="#94a3b8">{esc(line)}</text>')

    # stats row
    sy = 262
    out.append(f'<line x1="34" y1="{sy - 22}" x2="{W - 34}" y2="{sy - 22}" stroke="#1e293b"/>')
    colw = (W - 68) / 3
    for k, (v, l) in enumerate(p["stats"]):
        x = 34 + k * colw
        out.append(f'<g class="rise" style="animation-delay:{0.3 + 0.15 * k:.2f}s"><text x="{x}" y="{sy + 6}" font-family="{SANS}" font-size="24" font-weight="800" fill="url(#ac)">{esc(v)}</text>'
                   f'<text x="{x}" y="{sy + 28}" font-family="{MONO}" font-size="12" letter-spacing="1" fill="#64748b">{esc(l.upper())}</text></g>')

    # tech chips
    x = 34
    for tch in p["tech"]:
        w = len(tch) * 7.6 + 22
        out.append(f'<rect x="{x}" y="{H - 52}" width="{w:.0f}" height="24" rx="12" fill="{c1}" fill-opacity=".08" stroke="{c1}" stroke-opacity=".3"/>'
                   f'<text x="{x + w / 2:.1f}" y="{H - 35.5}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#cbd5e1">{esc(tch)}</text>')
        x += w + 8

    style = f'''.snake{{stroke-dasharray:180 {P - 180};animation:snake 7s linear infinite}}
@keyframes snake{{to{{stroke-dashoffset:-{P}}}}}
.eq{{transform-box:fill-box;transform-origin:center bottom;animation:eq .8s ease-in-out infinite alternate}}
@keyframes eq{{0%{{transform:scaleY(.25)}}100%{{transform:scaleY(1)}}}}
.float{{animation:fl 3s ease-in-out infinite}}
@keyframes fl{{50%{{transform:translateY(-4px)}}}}
.spin{{transform-box:fill-box;transform-origin:center;animation:spin 4s cubic-bezier(.6,0,.4,1) infinite}}
@keyframes spin{{0%,40%{{transform:translate(0,-6px) rotate(0)}}60%,100%{{transform:translate(0,-6px) rotate(144deg)}}}}
.scanY{{animation:sy 2.4s ease-in-out infinite}}
@keyframes sy{{0%{{transform:translateY(0)}}50%{{transform:translateY(55px)}}100%{{transform:translateY(0)}}}}
.live{{animation:live 1.4s ease-in-out infinite}}
@keyframes live{{50%{{opacity:.25}}}}
.rise{{opacity:0;animation:rise .8s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}'''
    write(f"projects/{key}.svg", svg(W, H, "\n".join(out), style))


# ─────────────────────────────── FOOTER ─────────────────────────────

def footer():
    W, H = 1200, 220

    def wave(amp, length, y, phase=0):
        pts = []
        for x in range(0, W * 2 + 1, 20):
            pts.append(f"{x},{y + amp * math.sin((x / length) * 2 * math.pi + phase):.1f}")
        return f'M0,{H} L' + " L".join(pts) + f' L{W * 2},{H} Z'

    body = f'''<defs>
  <linearGradient id="w1" x1="0" x2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>
  <linearGradient id="w2" x1="0" x2="1"><stop offset="0" stop-color="#a78bfa"/><stop offset="1" stop-color="#f472b6"/></linearGradient>
  <linearGradient id="tx" x1="0" x2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset=".5" stop-color="#a78bfa"/><stop offset="1" stop-color="#f472b6"/></linearGradient>
  <clipPath id="fr"><rect width="{W}" height="{H}" rx="28"/></clipPath>
</defs>
<g clip-path="url(#fr)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<path d="{wave(14, 600, 150)}" fill="url(#w1)" opacity=".18" class="wv" style="animation-duration:14s"/>
<path d="{wave(18, 400, 165, 1)}" fill="url(#w2)" opacity=".22" class="wv" style="animation-duration:9s;animation-direction:reverse"/>
<path d="{wave(10, 300, 182, 2)}" fill="url(#w1)" opacity=".35" class="wv" style="animation-duration:6s"/>
<text x="{W / 2}" y="82" text-anchor="middle" font-family="{SANS}" font-size="34" font-weight="800" fill="url(#tx)">Let's build something people actually use.</text>
<text x="{W / 2}" y="118" text-anchor="middle" font-family="{MONO}" font-size="16" fill="#94a3b8">thanks for stopping by <tspan fill="#f472b6" class="hb">♥</tspan> umutxyp</text>
</g>'''
    style = '''.wv{animation:wv linear infinite}
@keyframes wv{to{transform:translateX(-1200px)}}
.hb{transform-box:fill-box;transform-origin:center;animation:hb 1.2s ease-in-out infinite}
@keyframes hb{0%,100%{transform:scale(1)}20%{transform:scale(1.35)}40%{transform:scale(1)}}'''
    write("footer.svg", svg(W, H, body, style))


if __name__ == "__main__":
    print("Generating assets…")
    hero()
    terminal()
    stats()
    for k, v in SECTIONS.items():
        section(k, *v)
    for k, v in PROJECTS.items():
        project(k, v)
    footer()
    print("Done.")
