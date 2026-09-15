#!/usr/bin/env python3
"""
Two answers to "the images don't show up on Squarespace".

The pages reference /assets/img/NAME, which only exists in this repo. On
Squarespace that path is nothing, so every image is a broken icon until the
files are uploaded somewhere and the paths point at them.

This script produces:

  assets/img-web/                optimised copies — about half the bytes, no
                                 visible quality loss. Upload THESE, not the
                                 originals. The originals stay untouched because
                                 they are the only surviving copies of the old
                                 site's photography.

  dist/squarespace/pages-embedded/   every image inlined as a data URI, so the
                                 page needs no upload at all. Paste and it works.
                                 Costs page weight — see the printed table.

Upload is better for a live site: Squarespace serves its own files from a CDN and
the browser caches them across pages. Embedding is better for getting something
on screen today.
"""

import base64
import io
import mimetypes
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets" / "img"
WEB = ROOT / "assets" / "img-web"
PAGES = ROOT / "dist" / "squarespace" / "pages"
OUT = ROOT / "dist" / "squarespace" / "pages-embedded"

MAX_EDGE = 1600      # nothing on the site is displayed wider than this
QUALITY = 80


def optimise():
    WEB.mkdir(parents=True, exist_ok=True)
    before = after = 0
    for p in sorted(SRC.iterdir()):
        if p.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        im = Image.open(p)
        if max(im.size) > MAX_EDGE:
            im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
        target = WEB / p.name
        # Keep PNGs as PNGs — several are logos with transparency.
        if p.suffix.lower() == ".png" and im.mode in ("RGBA", "LA", "P"):
            im.save(target, "PNG", optimize=True)
        else:
            im.convert("RGB").save(target, "JPEG", quality=QUALITY,
                                   optimize=True, progressive=True)
        before += p.stat().st_size
        after += target.stat().st_size
    print(f"  {before/1024/1024:.2f} MB -> {after/1024/1024:.2f} MB "
          f"({100 - after/before*100:.0f}% smaller)  -> assets/img-web/")


def embed():
    OUT.mkdir(parents=True, exist_ok=True)
    cache = {}

    def data_uri(name):
        if name not in cache:
            f = WEB / name
            mime = mimetypes.guess_type(name)[0] or "image/jpeg"
            cache[name] = f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()
        return cache[name]

    # Also build copies that carry the stylesheet AS WELL as the images, so a
    # page is genuinely standalone: paste it and it looks right, with no header,
    # no footer and no code injection anywhere.
    styled_src = ROOT / "dist" / "squarespace" / "pages-self-styled"
    both = ROOT / "dist" / "squarespace" / "pages-embedded-styled"
    both.mkdir(parents=True, exist_ok=True)
    for page in sorted(styled_src.glob("*.html")):
        text = re.sub(r"/assets/img/([^\"')]+)", lambda m: data_uri(m.group(1)),
                      page.read_text(encoding="utf-8"))
        (both / page.name).write_text(
            "<!-- Stylesheet AND images are both inside this file. Paste it into a\n"
            "     Code Block and the page looks right on its own. You still need the\n"
            "     header and footer file somewhere for the navigation. -->\n" + text,
            encoding="utf-8")

    print(f"\n  {'PAGE':<36}{'IMAGES ONLY':>13}{'+ CSS':>9}")
    for page in sorted(PAGES.glob("*.html")):
        text = page.read_text(encoding="utf-8")
        text = re.sub(r"/assets/img/([^\"')]+)", lambda m: data_uri(m.group(1)), text)
        header = ("<!-- Images are embedded in this file, so it works with no upload.\n"
                  "     That makes it large. For a live site, upload assets/img-web/ to\n"
                  "     Squarespace and use ../pages/ instead — Squarespace serves its own\n"
                  "     files from a CDN and the browser caches them between pages. -->\n")
        (OUT / page.name).write_text(header + text, encoding="utf-8")
        b = both / page.name
        print(f"  {page.name:<36}{(OUT/page.name).stat().st_size/1024:>12.0f}K"
              f"{b.stat().st_size/1024:>8.0f}K")


def embed_chrome():
    """The header carries the logo, the footer the accreditation badges. If the
    pages are embedded, these must be too, or the site is half broken."""
    import base64, mimetypes
    sqs = ROOT / "dist" / "squarespace"

    def uri(name):
        f = WEB / name
        mime = mimetypes.guess_type(name)[0] or "image/jpeg"
        return f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()

    for name in ("SELF-CONTAINED-HEADER.html", "SELF-CONTAINED-FOOTER.html"):
        src = sqs / name
        if not src.exists():
            continue
        text = re.sub(r"/assets/img/([^\"')]+)", lambda m: uri(m.group(1)),
                      src.read_text(encoding="utf-8"))
        out = sqs / name.replace(".html", "-EMBEDDED.html")
        out.write_text(text, encoding="utf-8")
        print(f"  {out.name:<44}{out.stat().st_size/1024:>8.0f}K")


if __name__ == "__main__":
    optimise()
    embed()
    print()
    embed_chrome()
