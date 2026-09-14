#!/usr/bin/env python3
"""
ADL Consultancy — source validator.

Checks every file in src/pages/ against the rules this build has to hold to.
Run it before `python3 build.py`; run it again after editing any page.

    python3 check.py            # all pages
    python3 check.py 05-iso-27001.html   # just one

Exit status is 0 only when every check passes.
"""

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "src" / "pages"
PARTIALS = ROOT / "src" / "partials"
ASSETS = ROOT / "assets" / "img"

# A page is body markup only — the header and footer are their own files, so
# none of these may appear inside one. <script> is here because hosted CMS
# editors strip inline scripts silently: anything that depends on one is a
# feature that will vanish without an error.
FORBIDDEN_TAGS = ("<html", "<head", "<body", "<header", "<footer", "<script", "<nav")

MIN_SECTIONS = 7          # the homepage runs 8; nothing should be thinner than 7
DESC_MIN, DESC_MAX = 110, 200
META_KEYS = ("key", "out", "wp", "title", "description")

META_RE = re.compile(r"^<!--meta\s*(.*?)-->\s*", re.S)
URL_RE = re.compile(r"\{\{url:([a-z0-9-]+)\}\}")
IMG_RE = re.compile(r"\{\{img:([^}]+)\}\}")
USE_RE = re.compile(r'<use\s+href="#([^"]+)"')
SVG_RE = re.compile(r"<svg\b[^>]*>")
ID_RE = re.compile(r'\sid="([^"]+)"')
H1_RE = re.compile(r"<h1\b", re.I)
SECTION_RE = re.compile(r"<section\b", re.I)
ENTITY_RE = re.compile(r"&[a-zA-Z]+;|&#\d+;")
# Deliberately not \b-anchored on the right: catches "family-run business" too.
FAMILY_RUN_RE = re.compile(r"family[\s-]run", re.I)


def parse_meta(raw, errs):
    match = META_RE.match(raw)
    if not match:
        errs.append("no <!--meta ... --> block at the top of the file")
        return {}, raw
    meta = {}
    for line in match.group(1).strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            errs.append(f"meta line is not 'key: value' -> {line!r}")
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    for required in META_KEYS:
        if required not in meta:
            errs.append(f"meta is missing '{required}'")
    return meta, raw[match.end():]


def check_page(path, page_keys, icon_ids, images):
    errs, warns = [], []
    raw = path.read_text(encoding="utf-8")
    meta, body = parse_meta(raw, errs)

    # ---- meta -------------------------------------------------------------
    desc = meta.get("description", "")
    if desc:
        if ENTITY_RE.search(desc):
            errs.append("meta description contains HTML entities — it is plain text, not markup")
        if not DESC_MIN <= len(desc) <= DESC_MAX:
            errs.append(f"meta description is {len(desc)} chars, want {DESC_MIN}-{DESC_MAX}")
        # A description recovered from the database and cut at a character
        # limit ends mid-word. Catch it before it ships.
        if re.search(r"\b(?:for|with|and|the|to|of|in|a|acquiring ISO)\s+\w{1,4}$", desc):
            errs.append(f"meta description looks truncated mid-sentence: ...{desc[-40:]!r}")
    if meta.get("out") and not meta["out"].endswith(".html"):
        errs.append(f"meta out is not an .html filename: {meta['out']!r}")
    if meta.get("wp") and not meta["wp"].startswith("/"):
        errs.append(f"meta wp slug does not start with '/': {meta['wp']!r}")

    # ---- structure --------------------------------------------------------
    for tag in FORBIDDEN_TAGS:
        if tag in body.lower():
            errs.append(f"contains {tag}> — pages are body markup only, and inline JS gets stripped")

    h1s = len(H1_RE.findall(body))
    if h1s != 1:
        errs.append(f"{h1s} <h1> elements, want exactly 1")

    sections = len(SECTION_RE.findall(body))
    if sections < MIN_SECTIONS:
        errs.append(f"{sections} <section> elements, want at least {MIN_SECTIONS}")

    ids = ID_RE.findall(body)
    for dupe, count in Counter(ids).items():
        if count > 1:
            errs.append(f"id=\"{dupe}\" used {count} times — ids must be unique within a page")

    # ---- tokens resolve ---------------------------------------------------
    for key in sorted(set(URL_RE.findall(body))):
        if key not in page_keys:
            errs.append(f"{{{{url:{key}}}}} — no page declares that key")
    for name in sorted(set(IMG_RE.findall(body))):
        if name not in images:
            errs.append(f"{{{{img:{name}}}}} — no such file in assets/img/")

    # ---- svg sprite -------------------------------------------------------
    for icon in sorted(set(USE_RE.findall(body))):
        if icon not in icon_ids:
            errs.append(f'<use href="#{icon}"> — not defined in src/partials/icons.html')
    for tag in SVG_RE.findall(body):
        if "viewBox" not in tag:
            errs.append(f"<svg> without a viewBox (it will render clipped): {tag[:70]}")

    # ---- house style ------------------------------------------------------
    # The client asked for "family consultancy". The one sanctioned exception is
    # a verbatim quote from ADL's own news post, which we do not rewrite.
    for match in FAMILY_RUN_RE.finditer(body):
        line = body[:match.start()].count("\n") + 1
        context = body[max(0, match.start() - 90):match.start() + 40]
        if "<!-- verbatim:" in context:
            continue
        errs.append(f"line {line}: {match.group(0)!r} — the client asked for 'family consultancy'")
    if desc and FAMILY_RUN_RE.search(desc):
        errs.append("meta description says 'family run' — the client asked for 'family consultancy'")

    if 'style="' in body:
        n = body.count('style="')
        warns.append(f"{n} inline style attribute(s) — prefer a class in styles.css")

    return meta, errs, warns


def main():
    icons_src = (PARTIALS / "icons.html").read_text(encoding="utf-8")
    icon_ids = set(re.findall(r'<(?:g|symbol|path)[^>]*\sid="([^"]+)"', icons_src))
    images = {p.name for p in ASSETS.iterdir() if p.is_file()}

    wanted = sys.argv[1:]
    paths = sorted(PAGES.glob("*.html"))
    if not paths:
        sys.exit("ERROR: no pages in src/pages/")

    page_keys = set()
    for path in paths:
        match = META_RE.match(path.read_text(encoding="utf-8"))
        if match:
            for line in match.group(1).splitlines():
                if line.strip().startswith("key:"):
                    page_keys.add(line.split(":", 1)[1].strip())

    if wanted:
        paths = [p for p in paths if p.name in wanted]
        if not paths:
            sys.exit(f"ERROR: no page matches {wanted}")

    total_errs = total_warns = 0
    outs, keys = Counter(), Counter()

    for path in paths:
        meta, errs, warns = check_page(path, page_keys, icon_ids, images)
        outs[meta.get("out", "?")] += 1
        keys[meta.get("key", "?")] += 1
        total_errs += len(errs)
        total_warns += len(warns)
        if errs or warns:
            print(f"\n{path.name}")
            for e in errs:
                print(f"  FAIL  {e}")
            for w in warns:
                print(f"  warn  {w}")

    # Duplicates are only meaningful across the whole set, so check them here.
    if not wanted:
        for label, counter in (("key", keys), ("out", outs)):
            for value, count in counter.items():
                if count > 1:
                    print(f"\nFAIL  duplicate meta {label}: {value!r} on {count} pages")
                    total_errs += 1

    print(f"\n{len(paths)} page(s) checked — {total_errs} error(s), {total_warns} warning(s)")
    sys.exit(1 if total_errs else 0)


if __name__ == "__main__":
    main()
