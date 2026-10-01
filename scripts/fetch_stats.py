#!/usr/bin/env python3
"""Pulls the live numbers shown on codeshare.me into data/stats.json.

Every stat on codeshare.me is a value followed by its label, e.g. "40.6K" then
"Discord servers". Each page is scraped into {label: value}. If a page fails
to load, or a label disappears, the previous value is kept so the README
never loses a number because of one bad request.

Run:  python3 scripts/fetch_stats.py   (then python3 scripts/generate.py)
"""
import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "stats.json"
BASE = "https://codeshare.me"
PAGES = {
    "home": "/",
    "about": "/about",
    "beatra": "/projects/beatra",
    "sylon": "/projects/sylon",
    "mcstat": "/projects/mcstat",
    "justdiscord": "/projects/justdiscord",
    "justanime": "/projects/justanime",
}
# A stat value: "6", "2.9M", "6,752", "99.9%" — but not step numbers ("01") or company numbers.
VALUE = re.compile(r"(?!0\d)\d[\d.,]{0,6}[KMB]?\+?%?")


def fetch(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "umutxyp-readme-stats/1.0"})
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read().decode("utf-8", "replace")


def scrape(page):
    text = re.sub(r"<script.*?</script>|<style.*?</style>", "", page, flags=re.S)
    lines = [l.strip() for l in html.unescape(re.sub(r"<[^>]+>", "\n", text)).split("\n") if l.strip()]
    stats = {}
    for value, label in zip(lines, lines[1:]):
        # Labels are short phrases; skip the footer, timeline years and step numbers.
        if VALUE.fullmatch(value) and re.fullmatch(r"[A-Za-z][A-Za-z &]{2,40}", label) and label.upper() != label:
            stats.setdefault(label, value)
    return stats


def main():
    old = json.loads(DATA.read_text()) if DATA.exists() else {"pages": {}}
    pages, failed = {}, []
    for key, path in PAGES.items():
        merged = dict(old["pages"].get(key, {}))
        try:
            merged.update(scrape(fetch(path)))
        except Exception as exc:  # keep the previous numbers for this page
            failed.append(f"{key}: {exc}")
        pages[key] = merged
    if pages != old["pages"]:
        DATA.parent.mkdir(exist_ok=True)
        out = {"updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "pages": pages}
        DATA.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
        print("stats.json updated")
    else:
        print("no changes")
    for f in failed:
        print("warning:", f, file=sys.stderr)


if __name__ == "__main__":
    main()
