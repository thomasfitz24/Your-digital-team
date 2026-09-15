#!/usr/bin/env python3
"""
The final Squarespace deliverable: three kinds of file, each carrying exactly
what it needs and nothing it doesn't.

  FINAL/header.html      header markup + header CSS + logo + the scripts
  FINAL/footer.html      footer markup + footer CSS + badges + the scripts
  FINAL/pages/*.html     page markup + page CSS + that page's images

Every file is standalone: paste it and it renders correctly with nothing else
present. Using several together is safe — the icon sprite keeps only its first
copy and the scripts refuse to initialise twice.

    python3 build.py && python3 sqs_images.py && python3 sqs_final.py
"""

import base64
import mimetypes
import re
from pathlib import Path

from sqs_split_css import split

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
WEB = ROOT / "assets" / "img-web"
OUT = DIST / "squarespace" / "FINAL"

read = lambda p: p.read_text(encoding="utf-8")
_cache = {}


def embed(text):
    """Swap every /assets/img/NAME for the optimised file, inline."""
    def sub(m):
        name = m.group(1)
        if name not in _cache:
            f = WEB / name
            mime = mimetypes.guess_type(name)[0] or "image/jpeg"
            _cache[name] = f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()
        return _cache[name]
    return re.sub(r"/assets/img/([^\"')]+)", sub, text)


# Only the part of the Squarespace CSS each file actually needs.
SQS_HEADER = """
/* Squarespace: hide its own header, and pin ours. */
#header, .header, .sqs-announcement-bar-dropzone { display: none !important; }
.adl-header { position: fixed !important; top: 0; left: 0; right: 0; margin-bottom: 0 !important; }
"""

SQS_FOOTER = """
/* Squarespace: hide its own footer. Ours replaces it. */
#footer-sections { display: none !important; }
"""

SQS_PAGE = """
/* Squarespace: let this section reach the edge of the screen. Fluid Engine
   writes its layout inline, and only !important beats an inline style. Set the
   section's ID to "adl-section" for this to apply. */
#adl-section .fluid-engine { --sqs-site-max-width: 100vw; --sqs-site-gutter: 0vw; --sqs-mobile-site-gutter: 0vw; }
#adl-section .sqs-block, #adl-section .sqs-block-code, #adl-section .sqs-block-content {
  padding: 0 !important; margin: 0 !important; max-width: none !important; }
#adl-section .page-section, #adl-section .content-wrapper {
  padding-left: 0 !important; padding-right: 0 !important; max-width: none !important; }
#adl-section { padding-top: 0 !important; padding-bottom: 0 !important; }
body { overflow-x: hidden; }
"""

SPRITE_GUARD = """<script>
/* Each file carries a sprite so any one of them works alone. Two copies in one
   document would mean duplicate ids, so keep only the first. */
(function () {
  var s = document.querySelectorAll('[data-adl-icons]');
  for (var i = 1; i < s.length; i++) s[i].remove();
})();
</script>"""


def wrap_script(scripts):
    return ("<script>\n/* Runs once, however many of these files are on the page. */\n"
            "if (!window.__adlInit) {\n  window.__adlInit = true;\n"
            + scripts + "\n}\n</script>")


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "pages").mkdir(exist_ok=True)

    css = split()
    icons = read(DIST / "_icons.html").replace("<svg", "<svg data-adl-icons", 1)
    scripts = read(DIST / "_shared-scripts.js")

    def file(name, css_text, markup, note):
        text = f"""<!-- ADL Consultancy — {note}
     Self-contained: the CSS and images it needs are inside this file.
     Paste the whole thing into a Squarespace Code Block or Code Injection.
     Safe to use alongside the other ADL files. -->
<style>
{css_text}
</style>

{icons}
{SPRITE_GUARD}

{markup}

{wrap_script(scripts)}
"""
        (OUT / name).write_text(embed(text), encoding="utf-8")
        return (OUT / name).stat().st_size

    h = file("header.html", css["base"] + css["header"] + SQS_HEADER,
             read(DIST / "header.html"), "SITE HEADER")
    f = file("footer.html", css["base"] + css["footer"] + SQS_FOOTER,
             read(DIST / "footer.html"), "SITE FOOTER")

    print(f"  {'FILE':<38}{'SIZE':>8}")
    print(f"  {'header.html':<38}{h/1024:>7.0f}K")
    print(f"  {'footer.html':<38}{f/1024:>7.0f}K")

    page_css = css["base"] + css["page"] + SQS_PAGE
    for page in sorted(DIST.glob("*.html")):
        if page.name.startswith("_") or page.name in ("header.html", "footer.html"):
            continue
        body = re.sub(r"^<!--.*?-->\s*", "", read(page), flags=re.S)
        text = f"""<!-- ADL Consultancy — {page.stem}
     Self-contained: this page's CSS and images are inside this file.
     Paste into a Code Block, then set the section's ID to "adl-section"
     (Edit section > ... > Section ID) so it runs edge to edge. -->
<style>
{page_css}
</style>

{icons}
{SPRITE_GUARD}

{body}
"""
        out = OUT / "pages" / page.name
        out.write_text(embed(text), encoding="utf-8")
        print(f"  pages/{page.name:<32}{out.stat().st_size/1024:>7.0f}K")


if __name__ == "__main__":
    build()
