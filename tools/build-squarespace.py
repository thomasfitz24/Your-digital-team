#!/usr/bin/env python3
"""
Turn the standalone site into Squarespace-ready snippets.

Squarespace reverses several assumptions this site was built on:

  - A Code Block is injected into an existing document, so there is no
    <html>, <head> or <body> of our own to style.
  - Squarespace ships its own reset and typography, which collides with
    bare `body`, `*`, `a` and `section` rules. Everything therefore gets
    scoped under a single wrapper class.
  - Vendored files cannot be served, so GSAP and the fonts move to CDNs.
    (The sandbox this was developed in had no CDN access; Squarespace does.)
  - Code Blocks sit inside a fixed-width content column, so full-bleed
    sections need to break out of it.

Run:  python3 tools/build-squarespace.py
Out:  squarespace/
"""

import os, re, shutil

SRC  = 'yourdigiteam'
OUT  = 'squarespace'
ROOT = '.ydt-page'          # every page's wrapper

# Squarespace serves clean URLs; our files are foo.html
URLS = {
    'index.html':            '/',
    'about.html':            '/about',
    'services.html':         '/services',
    'contact.html':          '/contact',
    'seo.html':              '/seo',
    'ppc.html':              '/ppc',
    'social.html':           '/social',
    'email.html':            '/email',
    'content.html':          '/content',
    'web-development.html':  '/web-development',
    'privacy.html':          '/privacy',
    '404.html':              '/404',
}

PAGES = list(URLS.keys())


# ────────────────────────────────────────────────────────────────
# CSS scoping
# ────────────────────────────────────────────────────────────────
def split_blocks(css):
    """Yield (selector_or_atrule, body, is_at_rule) walking brace depth."""
    out, i, n = [], 0, len(css)
    buf = ''
    while i < n:
        c = css[i]
        if c == '/' and i + 1 < n and css[i+1] == '*':          # comment
            j = css.find('*/', i + 2)
            j = n if j < 0 else j + 2
            buf += css[i:j]; i = j; continue
        if c == '{':
            depth, j = 1, i + 1
            while j < n and depth:
                if css[j] == '/' and j + 1 < n and css[j+1] == '*':
                    k = css.find('*/', j + 2); j = n if k < 0 else k + 2; continue
                if css[j] == '{': depth += 1
                elif css[j] == '}': depth -= 1
                j += 1
            out.append((buf.strip(), css[i+1:j-1]))
            buf = ''; i = j; continue
        buf += c; i += 1
    if buf.strip():
        out.append((buf.strip(), None))     # trailing at-rule with no block
    return out


def split_selectors(sel):
    """Split a selector list on commas that are not inside parens."""
    parts, depth, cur = [], 0, ''
    for ch in sel:
        if ch == '(': depth += 1
        elif ch == ')': depth -= 1
        if ch == ',' and depth == 0:
            parts.append(cur); cur = ''
        else:
            cur += ch
    if cur.strip(): parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


COMMENT = re.compile(r'/\*.*?\*/', re.S)


def split_comment(sel):
    """A comment sitting above a rule lands in the selector buffer. Left there
    it becomes part of the selector and silently invalidates the whole rule —
    which is how the :root token block went missing. Pull them out."""
    comments = COMMENT.findall(sel)
    return '\n'.join(comments), COMMENT.sub(' ', sel).strip()


def scope_selector(sel):
    s = sel.strip()
    if s.startswith('@'):
        return s
    # things that mean "the document" become the wrapper itself
    if s in (':root', 'html', 'body', 'html body'):
        return ROOT
    if s == '*':
        return '%s, %s *' % (ROOT, ROOT)
    if s.startswith(':root'):
        return ROOT + s[len(':root'):]
    if s.startswith('html '):
        return ROOT + s[len('html'):]
    if s.startswith('body'):
        return ROOT + s[len('body'):]
    # a rule already aimed at the wrapper class stays as-is
    if s.startswith(ROOT):
        return s
    return ROOT + ' ' + s


def scope_css(css):
    out = []
    for sel, body in split_blocks(css):
        if body is None:
            out.append(sel + ';' if not sel.endswith(';') else sel)
            continue
        comment, sel = split_comment(sel)
        if comment:
            out.append(comment)
        if not sel:
            continue
        low = sel.lower()
        if low.startswith('@keyframes') or low.startswith('@-webkit-keyframes') \
           or low.startswith('@font-face') or low.startswith('@property'):
            out.append('%s {%s}' % (sel, body))                 # never scope these
        elif low.startswith('@media') or low.startswith('@supports') or low.startswith('@layer'):
            out.append('%s {\n%s\n}' % (sel, scope_css(body)))  # recurse
        else:
            scoped = ', '.join(scope_selector(s) for s in split_selectors(sel))
            out.append('%s {%s}' % (scoped, body))
    return '\n'.join(out)


# ────────────────────────────────────────────────────────────────
# link + asset rewriting
# ────────────────────────────────────────────────────────────────
def rewrite_links(text):
    for f, url in sorted(URLS.items(), key=lambda kv: -len(kv[0])):
        text = text.replace('href="%s"' % f, 'href="%s"' % url)
        text = text.replace("'%s'" % f, "'%s'" % url)                 # JS nav maps
        text = text.replace('href="%s#' % f, 'href="%s#' % url)
        text = text.replace("'%s#" % f, "'%s#" % url)
    return text


def rewrite_assets(text):
    """Point image paths at a base the user sets once at the top of the header."""
    text = re.sub(r"'assets/(logos|projects)/", r"YDT_ASSETS + '\1/", text)
    text = text.replace('"assets/', '"' + '/s/')     # any literal src= paths
    return text


def cdn_scripts(text):
    text = text.replace('<script src="vendor/gsap.min.js"></script>', '')
    text = text.replace('<script src="vendor/ScrollTrigger.min.js"></script>', '')
    text = text.replace('<script src="vendor/site-chrome.js" defer></script>', '')
    return text



def escape_script_end(js):
    """A literal </script> inside JS terminates the block it is pasted into —
    site-chrome.js carries one in its usage comment. Neutralise all of them."""
    return js.replace('</script', '<\\/script')

# ────────────────────────────────────────────────────────────────
# page extraction
# ────────────────────────────────────────────────────────────────
def extract(path):
    s = open(path).read()
    css = '\n'.join(re.findall(r'<style>(.*?)</style>', s, re.S))
    body = re.search(r'<body[^>]*>(.*?)</body>', s, re.S).group(1)
    scripts = re.findall(r'<script>(.*?)</script>', body, re.S)
    body = re.sub(r'<script>.*?</script>', '', body, flags=re.S)
    body = re.sub(r'<script src=[^>]*></script>', '', body)
    return css, body.strip(), scripts


BLEED = """
/* ── break out of Squarespace's content column ── */
%(root)s {
  position: relative;
  width: 100vw;
  max-width: 100vw;
  margin-left: calc(50%% - 50vw);
  margin-right: calc(50%% - 50vw);
  background: #000;
  color: #fff;
}

/* Squarespace wraps every block in containers. Any ancestor with a non-visible
   overflow becomes a scroll container, and a scroll container traps the
   position:sticky the services filmstrip depends on. */
#siteWrapper,
#page,
.page-section,
.content-wrapper,
.sqs-layout,
.sqs-row,
.sqs-block,
.sqs-block-content,
.sqs-block-code {
  overflow: visible !important;
}
.sqs-block-code { padding: 0 !important; }

/* ── out-specify Squarespace's own typography ──
   A Squarespace theme styles h1-h6, a and form controls with element
   selectors. Those beat inheritance from the wrapper, so headings come out
   in the theme's serif and links get the theme's underline. The site uses
   exactly one family throughout, so restoring it across the subtree is safe.
   Anything with its own explicit rule still wins on specificity. */
%(root)s, %(root)s * { font-family: var(--font); }
%(root)s h1, %(root)s h2, %(root)s h3,
%(root)s h4, %(root)s h5, %(root)s h6 { font-weight: 700; }
%(root)s a { text-decoration: none; }
%(root)s button, %(root)s input, %(root)s select, %(root)s textarea { font-family: var(--font); }
""" % {'root': ROOT}


def build_page(name):
    css, body, scripts = extract(os.path.join(SRC, name))
    css = scope_css(css) + '\n' + BLEED
    body = cdn_scripts(rewrite_links(body))
    slug = name.replace('.html', '')
    js = escape_script_end('\n'.join(rewrite_assets(rewrite_links(x)) for x in scripts))

    parts = [
        '<!-- ═══════════════════════════════════════════════════════════',
        '     %s  →  Squarespace page %s' % (name, URLS[name]),
        '     Paste the whole of this into ONE Code Block on that page.',
        '     Requires the header injection (see _header-injection.html).',
        '     ═══════════════════════════════════════════════════════════ -->',
        '<style>', css, '</style>', '',
        '<div class="ydt-page ydt-page--%s">' % slug,
        body,
        '</div>',
    ]
    if js.strip():
        parts += ['', '<script>', js, '</script>']
    open(os.path.join(OUT, name), 'w').write('\n'.join(parts) + '\n')
    return len('\n'.join(parts))


def main():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    total = 0
    for p in PAGES:
        size = build_page(p)
        total += size
        print('  %-24s %6.1f KB' % (URLS[p], size / 1024))
    print('  %d pages, %.0f KB total' % (len(PAGES), total / 1024))




# ────────────────────────────────────────────────────────────────
# header + footer, for Settings → Advanced → Code Injection
# ────────────────────────────────────────────────────────────────
HEADER_TOP = """<!-- ═══════════════════════════════════════════════════════════════
     YOURDIGITALTEAM — SITE HEADER + FOOTER
     Squarespace → Settings → Advanced → Code Injection → HEADER
     Paste this whole block. It loads on every page, builds the header
     and the footer, and provides GSAP for the page Code Blocks.

     Before pasting, set YDT_ASSETS below to wherever you have uploaded
     the logo and project images.

     Also hide Squarespace's own header and footer on these pages, or
     you will have two of each.
     ═══════════════════════════════════════════════════════════════ -->

<link rel="stylesheet" href="https://fonts.cdnfonts.com/css/nb-international-pro">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap">

<!-- GSAP, loaded once here so every page Code Block can use it -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>

<script>
  /* Where your images live. Upload them anywhere Squarespace will serve
     (a linked file, or your own host) and put the folder here, with a
     trailing slash. Leave as-is and the logo strip falls back to text
     wordmarks and the project cards to generated artwork. */
  var YDT_ASSETS = '/s/';
</script>

<style>
/* ── hide Squarespace's own chrome; this site brings its own ── */
#header, .header, .Header, #footer-sections, .Footer, footer.sections {
  display: none !important;
}
/* the injected header is fixed, so give the page its clearance back */
#siteWrapper, #page { padding-top: 0 !important; }
body { margin: 0; background: #000; }

/* Squarespace containers must not become scroll containers — the services
   filmstrip uses position: sticky and a scroll container traps it. */
#siteWrapper, #page, .page-section, .content-wrapper,
.sqs-layout, .sqs-row, .sqs-block, .sqs-block-content, .sqs-block-code {
  overflow: visible !important;
}
.sqs-block-code { padding: 0 !important; }
</style>

<style>
"""

HEADER_MID = """</style>

<script>
"""

HEADER_END = """</script>
"""


def build_chrome():
    css = open(os.path.join(SRC, 'vendor', 'site-chrome.css')).read()
    js  = open(os.path.join(SRC, 'vendor', 'site-chrome.js')).read()

    # the chrome sits outside .ydt-page, so it is NOT scoped — but it does
    # need to out-specify Squarespace's own link and list styling
    css = css.replace('.site-footer__list a {', '.site-footer .site-footer__list a {')
    css = css.replace('.ydt-header__nav-link {', '.ydt-header .ydt-header__nav-link {')

    js = rewrite_links(js)
    js = js.replace("var HERE = (location.pathname.split('/').pop() || 'index.html').toLowerCase();",
                    "var HERE = location.pathname.replace(/\\/+$/, '').toLowerCase() || '/';")
    js = js.replace("if (HERE === '') HERE = 'index.html';", "")
    # resolve()/isCurrent() compare against clean URLs now
    js = js.replace("""    var file = href.slice(0, hash).toLowerCase();
    return (file === HERE || (file === 'index.html' && HERE === 'index.html'))
      ? href.slice(hash)
      : href;""",
"""    var file = href.slice(0, hash).toLowerCase().replace(/\\/+$/, '') || '/';
    return file === HERE ? href.slice(hash) : href;""")
    js = js.replace("""    var file = href.split('#')[0].toLowerCase();
    return file !== '' && file === HERE && href.indexOf('#') < 0;""",
"""    var file = href.split('#')[0].toLowerCase().replace(/\\/+$/, '') || '/';
    return file === HERE && href.indexOf('#') < 0;""")

    out = HEADER_TOP + css + HEADER_MID + escape_script_end(js) + HEADER_END
    open(os.path.join(OUT, '_header-injection.html'), 'w').write(out)
    return len(out)


if __name__ == '__main__':
    main()
    print('  %-24s %6.1f KB' % ('_header-injection', build_chrome() / 1024))
