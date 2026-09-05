#!/usr/bin/env python3
"""Build the distributable versions of the Wonder Sensory page from index.html.

  wonder-sensory-embedded.html    single file, every image inlined as base64
  wonder-sensory-squarespace.html fragment for a Squarespace Code Block: classes
                                  prefixed ws-, all CSS scoped to #wonder-site,
                                  images served from Squarespace's /s/ path
"""
import base64, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
src = open('index.html', encoding='utf-8').read()

# ---------------------------------------------------------------- embedded
MIME = {'webp': 'image/webp', 'png': 'image/png'}
def inline(m):
    path = 'assets/%s.%s' % (m.group(1), m.group(2))
    data = base64.b64encode(open(path, 'rb').read()).decode()
    return 'src="data:%s;base64,%s"' % (MIME[m.group(2)], data)
emb = re.sub(r'src="assets/([^"]+)\.(webp|png)"', inline, src)
assert 'assets/' not in emb
open('wonder-sensory-embedded.html', 'w', encoding='utf-8').write(emb)

# -------------------------------------------------------------- squarespace
PREFIX = 'ws-'
# state tokens toggled from JS or used only in compound selectors: leave as-is
STATE = {'pre', 'open', 'private', 'full', 'hidden', 'today', 'show', 'plain', 'scrolled'}

head = re.search(r'<head>(.*?)</head>', src, re.S).group(1)
style = re.search(r'<style>(.*?)</style>', head, re.S).group(1)
fonts = '\n'.join(re.findall(r'<link[^>]+>', head))
body = re.search(r'<body>(.*?)</body>', src, re.S).group(1)
script = re.search(r'<script>(.*?)</script>', body, re.S).group(1)
markup = body[:body.index('<script>')]

classes = set()
for attr in re.findall(r'class="([^"]*)"', markup):
    classes.update(t for t in attr.split() if t not in STATE)
# classes only created from JS
classes.update({'slot', 'tt-day', 'tt-empty'})

def pfx(name):
    return PREFIX + name if name in classes else name

# 1. class attributes in markup and in JS-built markup
def fix_attr(m):
    return 'class="%s"' % ' '.join(pfx(t) for t in m.group(1).split())
markup = re.sub(r'class="([^"]*)"', fix_attr, markup)
script = re.sub(r'class="([^"]*)"', fix_attr, script)

# 2. selectors in CSS (skip decimals like .75 by requiring a letter/underscore first)
style = re.sub(r'\.(?=[A-Za-z_])([\w-]+)', lambda m: '.' + pfx(m.group(1)), style)

# 3. selectors and class strings inside the script
script = script.replace("querySelector('.header')", "querySelector('.%sheader')" % PREFIX)
script = script.replace("'.chip[data-filter]'", "'.%schip[data-filter]'" % PREFIX)
script = script.replace("var cls='slot '", "var cls='%sslot '" % PREFIX)
script = script.replace("querySelectorAll('.chip", "querySelectorAll('.%schip" % PREFIX)

# 4. semantic header/footer elements become divs so a `header{display:none}` rule can't hit them
markup = markup.replace('<header class="ws-header"', '<div class="ws-header" role="banner"')
markup = markup.replace('</header>', '</div>', 1)
markup = markup.replace('<footer class="ws-footer', '<div class="ws-footer" role="contentinfo"').replace('</footer>', '</div>')
assert '<header' not in markup and '<footer' not in markup

# 5. images from Squarespace's custom-file path
markup = re.sub(r'src="assets/([^"]+)"', r'src="/s/\1"', markup)
files = sorted(set(re.findall(r'/s/([^"]+)', markup)))

# 6. scope every CSS rule under #wonder-site so Squarespace's tag styles lose
SCOPE = '#wonder-site'
def scope_selector(sel):
    sel = sel.strip()
    if not sel:
        return sel
    if sel == ':root':
        return SCOPE
    if sel in ('html', 'html,body', 'html, body'):
        return None  # dropped: cannot style the host document from a block
    if sel == 'body':
        return SCOPE
    if sel.startswith('body'):
        return SCOPE + sel[4:]
    return SCOPE + ' ' + sel

def scope_css(css):
    out, i, n = [], 0, len(css)
    depth, in_keyframes = 0, [False]
    buf = ''
    while i < n:
        c = css[i]
        if c == '{':
            head = buf.strip()
            buf = ''
            if head.startswith('@'):
                out.append(head + '{')
                in_keyframes.append(head.startswith('@keyframes') or in_keyframes[-1])
            else:
                if in_keyframes[-1]:
                    out.append(head + '{')
                else:
                    parts = [scope_selector(p) for p in head.split(',')]
                    parts = [p for p in parts if p]
                    if not parts:  # rule dropped entirely: skip its block
                        j = css.index('}', i)
                        i = j + 1
                        continue
                    out.append(', '.join(parts) + '{')
                in_keyframes.append(in_keyframes[-1])
            depth += 1
        elif c == '}':
            out.append(buf + '}')
            buf = ''
            depth -= 1
            in_keyframes.pop()
        else:
            buf += c
        i += 1
    return ''.join(out)

style = re.sub(r'/\*.*?\*/', '', style, flags=re.S)  # comments would confuse selector matching
style = scope_css(style)
# the scope element replaces body: give it the page ground and font
style = style.replace(SCOPE + '{\n    font-family', SCOPE + '{position:relative;display:block;\n    font-family', 1)
style += '\n  %s .ws-header,%s .ws-footer{display:block!important;visibility:visible!important}\n' % (SCOPE, SCOPE)

note = '''<!--
  WONDER SENSORY - SQUARESPACE CODE BLOCK VERSION

  1. Upload every file from the assets folder in Squarespace (Settings > Files, or any
     link editor > Files). Squarespace serves uploads at /s/<filename>, which is what
     this page expects:
     %s
  2. Add a blank page, drop in a Code Block, set it to HTML, and paste this whole file.
     Code Blocks that contain <script> need the Business plan or higher.
  3. Every class is prefixed "ws-" and every style is scoped to #wonder-site, so hiding
     Squarespace's own header on the page will not hide this one.
-->
''' % '\n     '.join(files)

sq = note + fonts + '\n<style>' + style + '</style>\n<div id="wonder-site">' + markup + '</div>\n<script>' + script + '</script>\n'
assert 'assets/' not in sq and 'data:image' not in sq
# sanity: no unprefixed class from the set survives in markup or CSS
for name in classes:
    assert not re.search(r'class="[^"]*(?<![\w-])%s(?![\w-])' % re.escape(name), sq), name
    assert not re.search(r'\.%s(?![\w-])' % re.escape(name), style), name
open('wonder-sensory-squarespace.html', 'w', encoding='utf-8').write(sq)


# ------------------------------------------------- squarespace, images embedded
def inline_lite(m):
    base = m.group(1).rsplit('.', 1)[0]
    path = 'assets-lite/%s.webp' % base
    data = base64.b64encode(open(path, 'rb').read()).decode()
    return 'src="data:image/webp;base64,%s"' % data
sq_emb = re.sub(r'src="/s/([^"]+)"', inline_lite, sq)
sq_emb = sq_emb.replace('SQUARESPACE CODE BLOCK VERSION', 'SQUARESPACE CODE BLOCK VERSION, IMAGES EMBEDDED', 1)
sq_emb = re.sub(r'  1\. Upload every file.*?\n  2\.', '  1. Nothing to upload: every image is embedded in this file.\n  2.', sq_emb, count=1, flags=re.S)
assert 'src="/s/' not in sq_emb
open('wonder-sensory-squarespace-embedded.html', 'w', encoding='utf-8').write(sq_emb)

for f in ('index.html', 'wonder-sensory-embedded.html', 'wonder-sensory-squarespace.html', 'wonder-sensory-squarespace-embedded.html'):
    print('%-36s %5d KB' % (f, os.path.getsize(f) // 1024))
