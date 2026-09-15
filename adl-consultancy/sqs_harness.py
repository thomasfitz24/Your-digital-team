#!/usr/bin/env python3
"""
Wrap the Squarespace deliverable in a simulation of Squarespace's own page, so
the paste-ready files can be tested in a browser before anyone pastes them.

This is an APPROXIMATION, not a guarantee. It reproduces the parts of Squarespace
7.1 that our code actually collides with:

  - the container chain  .page-section > .content-wrapper > .fluid-engine
                         > .sqs-block.sqs-block-code > .sqs-block-content
  - the --sqs-site-max-width / --sqs-site-gutter custom properties that set the
    page's max width and side gutter
  - Fluid Engine writing its grid placement as INLINE styles on the block, which
    is why our overrides need !important
  - a stand-in native header and footer, so we can prove ours replaces them
  - base typography on body/h1-h6/p/a/ul, so we can prove our .adl-page scoping
    still wins

It does NOT reproduce Squarespace's full stylesheet, its JavaScript, or its
announcement bar. Anything it passes still needs a look on a real staging site.

    python3 sqs_harness.py          # writes dist/sqs-test/
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SQS = ROOT / "dist" / "squarespace"
OUT = ROOT / "dist" / "sqs-test"

read = lambda p: p.read_text(encoding="utf-8")
strip_comments = lambda s: re.sub(r"<!--.*?-->", "", s, flags=re.S)

# Squarespace's own base styles, deliberately aggressive, so that anything of
# ours that is not properly scoped shows up as a failure here rather than live.
SQS_BASE = """
:root{
  --sqs-site-max-width: 1200px;
  --sqs-site-gutter: 4vw;
  --sqs-mobile-site-gutter: 6vw;
}
*{box-sizing:border-box}
body{margin:0;font-family:Georgia,'Times New Roman',serif;font-size:16px;
     line-height:1.7;color:#3b3b3b;background:#fff}
h1,h2,h3,h4,h5,h6{font-family:Georgia,serif;font-weight:400;line-height:1.3;
     letter-spacing:0;margin:0 0 .6em}
h1{font-size:3rem} h2{font-size:2.25rem} h3{font-size:1.5rem}
p{margin:0 0 1.2em;font-size:1rem}
a{color:#b04a2f;text-decoration:underline}
ul,ol{margin:0 0 1.2em;padding-left:1.4em}
img{max-width:100%}

/* native chrome — ours is supposed to replace both of these */
#header{position:sticky;top:0;z-index:9000;background:#fffbe6;border-bottom:2px solid #d6c27a;
        padding:18px var(--sqs-site-gutter);font-family:Georgia,serif}
#footer-sections{background:#f3efe1;border-top:2px solid #d6c27a;
        padding:40px var(--sqs-site-gutter);font-family:Georgia,serif}

/* the container chain a code block actually sits inside */
.page-section{padding:6vw 0}
.content-wrapper{max-width:var(--sqs-site-max-width);margin:0 auto;
        padding-left:var(--sqs-site-gutter);padding-right:var(--sqs-site-gutter)}
.fluid-engine{display:grid;grid-template-columns:repeat(24,1fr);gap:11px;
        max-width:var(--sqs-site-max-width);margin:0 auto}
.sqs-block{padding-bottom:17px}
.sqs-block-content{max-width:100%}
@media (max-width:767px){
  .content-wrapper{padding-left:var(--sqs-mobile-site-gutter);
                   padding-right:var(--sqs-mobile-site-gutter)}
  .fluid-engine{grid-template-columns:repeat(8,1fr)}
}
"""


def build():
    if not SQS.exists():
        raise SystemExit("ERROR: run `python3 sqs_build.py` first")

    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob("*.html"):
        stale.unlink()

    head_inject = strip_comments(read(SQS / "1-code-injection-HEADER.html"))
    foot_inject = strip_comments(read(SQS / "2-code-injection-FOOTER.html"))
    custom_css = read(SQS / "3-custom-css.css")

    # Images resolve one level up, the same way they will once uploaded.
    foot_inject = foot_inject.replace('src="/assets/img/', 'src="../assets/img/')

    n = 0
    for page in sorted((SQS / "pages").glob("*.html")):
        block = strip_comments(read(page)).replace('src="/assets/img/', 'src="../assets/img/')

        (OUT / page.name).write_text(f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SQS harness — {page.stem}</title>

<style>{SQS_BASE}</style>

<!-- Code Injection > HEADER -->
{head_inject}

<!-- Design > Custom CSS -->
<style>
{custom_css}
</style>
</head>
<body>
<div id="siteWrapper">

  <header id="header">
    <strong>Squarespace native header</strong> — our CSS must hide this
  </header>

  <main id="page">
    <!-- Fluid Engine section. The inline style on the block is the thing that
         only !important can beat, which is why it is reproduced here. -->
    <section id="adl-section" class="page-section" data-section-id="sqs-fake-{n}">
      <div class="content-wrapper">
        <div class="fluid-engine">
          <div class="sqs-block sqs-block-code"
               style="grid-area: 1 / 1 / 2 / 25; padding-left: 11px; padding-right: 11px;">
            <div class="sqs-block-content">
{block}
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer id="footer-sections">
    <strong>Squarespace native footer</strong> — our CSS must hide this
  </footer>

</div>

<!-- Code Injection > FOOTER -->
{foot_inject}
</body>
</html>
""", encoding="utf-8")
        n += 1

    print(f"  {n} harness pages -> dist/sqs-test/   (an approximation, not a guarantee)")


if __name__ == "__main__":
    build()
