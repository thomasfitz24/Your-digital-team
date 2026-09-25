#!/usr/bin/env python3
"""Build single-file versions of the Wonder Sensory site.

The site itself is plain multi-page HTML: index.html, cafe.html and contact.html
all link assets/site.css and assets/site.js. That is what gets deployed.

This script produces a self-contained copy of each page, with the stylesheet, the
script and every image inlined, so a page can be emailed or opened from a USB
stick with nothing else alongside it:

    dist/index.html
    dist/cafe.html
    dist/contact.html

Run it after editing any page, the CSS or the JS:

    python3 build.py
"""
import base64, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

PAGES = ['index.html', 'cafe.html', 'contact.html']
OUT = 'dist'
MIME = {'webp': 'image/webp', 'png': 'image/png', 'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg', 'svg': 'image/svg+xml'}


def data_uri(path):
    ext = path.rsplit('.', 1)[-1].lower()
    with open(path, 'rb') as fh:
        return 'data:%s;base64,%s' % (MIME[ext], base64.b64encode(fh.read()).decode())


def build(page):
    html = open(page, encoding='utf-8').read()

    # 1. inline the stylesheet
    css = open('assets/site.css', encoding='utf-8').read()
    # the CSS may only use inline data: URLs (the paper grain), never a file
    assert not re.search(r"url\((?![\"']?data:)", css.replace("url(%23", "")), 'site.css gained a file url() — inline it here too'
    html = html.replace(
        '<link rel="stylesheet" href="assets/site.css">',
        '<style>\n' + css + '\n</style>'
    )

    # 2. inline the script
    js = open('assets/site.js', encoding='utf-8').read()
    html = html.replace(
        '<script src="assets/site.js"></script>',
        '<script>\n' + js + '\n</script>'
    )

    # 3. inline every local image, favicon included
    def repl(m):
        attr, path = m.group(1), m.group(2)
        return '%s="%s"' % (attr, data_uri(path))
    html = re.sub(r'(src|href)="((?:assets|assets-lite)/[^"]+\.(?:webp|png|jpe?g|svg))"', repl, html)

    # 4. no RELATIVE asset reference may survive. Absolute https:// ones stay as
    #    they are: the og:image tags must point at a real public URL, not a data URI.
    leftovers = [m for m in re.findall(r'(?:src|href)="([^"]*(?:assets|assets-lite)/[^"]+)"', html)
                 if not m.startswith('http')]
    assert not leftovers, 'relative asset references survived: %s' % leftovers

    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, page)
    open(dest, 'w', encoding='utf-8').write(html)
    return dest


if __name__ == '__main__':
    print('%-26s %10s  %10s' % ('page', 'source', 'single-file'))
    print('-' * 50)
    for page in PAGES:
        dest = build(page)
        print('%-26s %7d KB  %7d KB' % (
            page, os.path.getsize(page) // 1024, os.path.getsize(dest) // 1024))
    print('-' * 50)
    print('single-file copies written to %s/' % OUT)
