#!/usr/bin/env python3
"""
Split the stylesheet into three buckets, so the header file carries header CSS,
the footer file carries footer CSS, and the page files carry page CSS.

Splitting by hand invites drift, so this parses the stylesheet into rules and
classifies each by its selector. Anything it cannot place goes in the shared
base, which every file gets — the safe direction to fail.

    python3 sqs_split_css.py      # prints the split, writes nothing
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSS = ROOT / "src" / "partials" / "styles.css"

HEADER_SEL = (".adl-header", ".mobile-menu", ".mobile-nav", ".mobile-foot",
              ".skip-link", "menu-open", ".hamburger", ".header-")
FOOTER_SEL = (".adl-footer", ".vmodal")
# Tokens, reset, typography, buttons, icons — everything all three need.
BASE_EXACT = (".adl-page", ":root")   # the token block itself
BASE_SEL = ( ".adl-page *", ".adl-page a", ".adl-page button",
            ".adl-page summary", ".adl-page img", ".adl-page h1", ".adl-page h2",
            ".adl-page h3", ".adl-page h4", ".adl-page .visually-hidden",
            ".adl-page .icon", ".adl-page .btn", ".adl-page .pill",
            ".adl-page .on-dark", ".adl-page [id]", ":root")


def split_rules(css):
    """Yield (selector, block) pairs, keeping @media blocks whole."""
    out, i, n = [], 0, len(css)
    while i < n:
        if css[i] in " \n\t":
            i += 1
            continue
        if css.startswith("/*", i):
            i = css.index("*/", i) + 2
            continue
        if css.startswith("@import", i):
            # The font URL contains semicolons (wght@400;500;600), so the first
            # ";" is not the end of the statement. The statement is one line.
            end = css.index("\n", i)
            out.append(("@import", css[i:end]))
            i = end
            continue
        brace = css.index("{", i)
        sel = css[i:brace].strip()
        depth, j = 0, brace
        while j < n:
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        out.append((sel, css[i:j + 1]))
        i = j + 1
    return out


def classify(sel, block):
    # The token declaration is the selector ".adl-page" on its own. Everything
    # downstream reads var(--blue) etc from it, so it must be in the shared base
    # or the header and footer come out unstyled.
    if sel.strip() in BASE_EXACT:
        return "base"
    probe = sel + block if sel.startswith("@media") else sel
    if any(s in probe for s in HEADER_SEL):
        return "header"
    if any(s in probe for s in FOOTER_SEL):
        return "footer"
    if any(probe.startswith(s) or s in probe for s in BASE_SEL):
        return "base"
    return "page"


def split():
    css = CSS.read_text(encoding="utf-8")
    buckets = {"base": [], "header": [], "footer": [], "page": []}
    for sel, block in split_rules(css):
        if sel == "@import":
            buckets["base"].append(block)
            continue
        # A @media block can hold rules for more than one bucket. Split inside it
        # rather than dumping the whole thing in one place.
        if sel.startswith("@media"):
            inner = block[block.index("{") + 1:block.rindex("}")]
            per = {}
            for s2, b2 in split_rules(inner):
                per.setdefault(classify(s2, b2), []).append(b2)
            for where, rules in per.items():
                buckets[where].append(sel + "{" + "\n".join(rules) + "}")
            continue
        buckets[classify(sel, block)].append(block)
    return {k: "\n".join(v) for k, v in buckets.items()}


if __name__ == "__main__":
    b = split()
    total = sum(len(v) for v in b.values())
    print(f"{'BUCKET':<10}{'BYTES':>9}   goes into")
    for k, where in (("base", "all three"), ("header", "header file"),
                     ("footer", "footer file"), ("page", "page files")):
        print(f"{k:<10}{len(b[k]):>9}   {where}")
    print(f"{'TOTAL':<10}{total:>9}   (stylesheet is {CSS.stat().st_size})")
    print(f"\nheader file CSS: {len(b['base']) + len(b['header']):>6} bytes")
    print(f"footer file CSS: {len(b['base']) + len(b['footer']):>6} bytes")
    print(f"page file CSS:   {len(b['base']) + len(b['page']):>6} bytes")
