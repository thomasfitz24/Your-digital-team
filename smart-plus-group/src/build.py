#!/usr/bin/env python3
"""
Build smart-plus-group/index.html from src/template.html.

  python3 src/build.py          -> inlines every {{IMG:name}} as a base64 data URI (self-contained file)
  python3 src/build.py --cdn    -> swaps {{IMG:name}} for the original Squarespace CDN URLs
                                   (the four brand logos have no CDN URL yet; upload them and
                                   update src/cdn-urls.json)
"""
import base64, json, os, re, sys

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
ASSETS = os.path.join(SRC, "assets")
MODE = "cdn" if "--cdn" in sys.argv else "data"
OUT = os.path.join(ROOT, "index.html" if MODE == "data" else "index.cdn.html")

with open(os.path.join(SRC, "cdn-urls.json")) as fh:
    CDN = json.load(fh)


def mime(b):
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP":
        return "image/webp"
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if b[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    head = b.lstrip()[:80].lower()
    if head.startswith(b"<?xml") or head.startswith(b"<svg"):
        return "image/svg+xml"
    raise ValueError("unknown image type")


_cache = {}


def resolve(name):
    if MODE == "cdn" and name in CDN:
        return CDN[name]
    if name in _cache:
        return _cache[name]
    matches = [f for f in os.listdir(ASSETS) if os.path.splitext(f)[0] == name]
    if not matches:
        raise FileNotFoundError(name)
    with open(os.path.join(ASSETS, matches[0]), "rb") as fh:
        raw = fh.read()
    uri = "data:%s;base64,%s" % (mime(raw), base64.b64encode(raw).decode("ascii"))
    _cache[name] = uri
    return uri


with open(os.path.join(SRC, "template.html"), encoding="utf-8") as fh:
    template = fh.read()

missing, used = set(), {}


def sub(m):
    name = m.group(1)
    try:
        used[name] = used.get(name, 0) + 1
        return resolve(name)
    except FileNotFoundError:
        missing.add(name)
        return m.group(0)


html = re.sub(r"\{\{IMG:([a-z0-9\-]+)\}\}", sub, template)
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(html)

print("wrote %s (%.2f MB, mode=%s)" % (os.path.relpath(OUT, ROOT), len(html.encode("utf-8")) / 1e6, MODE))
dupes = {k: v for k, v in used.items() if v > 1}
if dupes:
    print("embedded more than once:", dupes)
if missing:
    print("MISSING assets:", sorted(missing))
    sys.exit(1)
