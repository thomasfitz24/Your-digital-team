#!/usr/bin/env python3
"""
Rebuild the testimonials page: group 30 quotes by the standard they talk about.

The existing 25 quotes are parsed out of the current page and re-emitted
byte-for-byte, so nothing a client said can drift. Five more are recovered from
the old testimonials page, which had 26 entries where the homepage had 25 and
the two sets were not the same set.
"""

import html
import re
import pathlib

SCRATCH = pathlib.Path(__file__).resolve().parent
PAGE = pathlib.Path('/home/user/Your-digital-team/adl-consultancy/src/pages/09-testimonials.html')

ICON = ('<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<use href="#i-{}"/></svg>')
STARS = ('<div class="stars" aria-label="Five out of five">' +
         '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><use href="#i-star"/></svg>' * 5 +
         '</div>')


def esc(s):
    s = html.escape(s, quote=False)
    return (s.replace('’', '&rsquo;').replace('‘', '&lsquo;')
             .replace('“', '&ldquo;').replace('”', '&rdquo;')
             .replace('–', '&ndash;').replace('—', '&mdash;').replace('£', '&pound;'))


# ---- 1. the quotes already on the page, preserved exactly -------------------
existing = re.findall(
    r'<figure class="quote">.*?<blockquote>(.*?)</blockquote>.*?'
    r'<strong>(.*?)</strong><span>(.*?)</span>',
    PAGE.read_text(encoding='utf-8'), re.S)
QUOTES = [dict(body=b.strip(), role=r.strip(), company=c.strip()) for b, r, c in existing]
print(f'parsed {len(QUOTES)} existing quotes')

# ---- 2. the five that were only on the old WordPress page -------------------
text = (SCRATCH / 'source' / 'testimonials.txt').read_text(encoding='utf-8')
lines = [l.strip() for l in text.splitlines() if l.strip()]
recovered = []
i = 0
while i < len(lines):
    if lines[i][0] in '“"':
        body = [lines[i].lstrip('“"')]
        j = i + 1
        while j < len(lines) and not (lines[j].endswith(('”', '"')) or len(lines[j].split()) <= 6):
            body.append(lines[j]); j += 1
        if j < len(lines) and lines[j].endswith(('”', '"')):
            body.append(lines[j]); j += 1
        if j + 1 < len(lines):
            recovered.append(dict(body=' '.join(body).strip('“”" '),
                                  role=lines[j], company=lines[j + 1]))
        i = j + 2
    else:
        i += 1

WANTED = {
    'Intuity Communications', 'Axe Roofing', 'Platform365', 'Prestige DPM Ltd',
    'Southern Communications Group Ltd',
}
have = {(q['company'], q['role']) for q in QUOTES}
added = 0
for r in recovered:
    if r['company'] in WANTED and (r['company'], r['role']) not in have:
        QUOTES.append(dict(body=esc(r['body']), role=esc(r['role']), company=esc(r['company'])))
        have.add((r['company'], r['role']))
        added += 1
        print(f"  + {r['company']} ({r['role']})")
print(f'{len(QUOTES)} quotes total ({added} recovered)')

# ---- 3. group by the standard each client actually talks about -------------
LONG_TERM = {'Southern Communications', 'Contour Fine Tooling Ltd',
             'Amble Electrical Services', 'K2B Ltd'}


def group_of(q):
    blob = (q['body'] + ' ' + q['company']).lower().replace(' ', '')
    if q['company'] in LONG_TERM:
        return 'long-term'
    if 'iso45001' in blob or 'ohsas' in blob or 'health&safety' in blob or 'h&s' in blob:
        return 'safety-environment'
    if 'iso14001' in blob or 'environmental' in blob:
        return 'safety-environment'
    if 'iso27001' in blob or 'iso27001' in blob:
        return 'infosec'
    return 'quality'


GROUPS = {k: [] for k in ('quality', 'infosec', 'safety-environment', 'long-term')}
for q in QUOTES:
    GROUPS[group_of(q)].append(q)
for k, v in GROUPS.items():
    print(f'  {k:20} {len(v)}')

# The featured pull-quote runs above the grids, so lift it out of whichever
# grid it landed in. Match on company and role rather than on a phrase inside
# the quote — the body is entity-encoded by the time we see it here.
FEATURED = None
for name, items in GROUPS.items():
    for q in items:
        if q['company'].startswith('Southern Communications Group') \
                and 'Information Security Officer' in q['role']:
            FEATURED = q
            items.remove(q)
            break
    if FEATURED:
        break
if FEATURED is None:
    raise SystemExit('ERROR: the featured Southern Communications quote was not found')


def quote_html(q, indent='      '):
    return (f'{indent}<figure class="quote">\n'
            f'{indent}  {STARS}\n'
            f'{indent}  <blockquote>{q["body"]}</blockquote>\n'
            f'{indent}  <figcaption class="who"><strong>{q["role"]}</strong>'
            f'<span>{q["company"]}</span></figcaption>\n'
            f'{indent}</figure>')


def grid(name, tint, eyebrow, h2, lead, sid):
    items = GROUPS[name]
    cls = ' class="faqs"' if tint else ''
    return f"""<!-- ===== {h2.upper()} ===== -->
<section{cls} id="{sid}" aria-labelledby="{sid}-t">
  <div class="wrap">
    <div class="sec-head left">
      <span class="eyebrow">{eyebrow}</span>
      <h2 id="{sid}-t">{h2}</h2>
      <p>{lead}</p>
    </div>
    <div class="quotes-grid">
{chr(10).join(quote_html(q) for q in items)}
    </div>
  </div>
</section>
"""


parts = [f"""<!--meta
key: testimonials
out: testimonials.html
wp: /testimonials/
title: Client Testimonials | ADL Consultancy
description: Thirty businesses on what it is like to work with ADL Consultancy, from the first gap analysis to certification and the surveillance visits after it. 100% success rate, no contract.
-->

<!-- ===== HERO ===== -->
<section class="hero" aria-labelledby="h1">
  <div class="hero-media">
    <img src="{{{{img:3556.jpg}}}}" alt="" aria-hidden="true" fetchpriority="high">
  </div>
  <div class="hero-inner">
    <nav aria-label="Breadcrumb">
      <ol class="crumbs">
        <li><a href="{{{{url:home}}}}">Home</a></li>
        <li><span aria-current="page">Testimonials</span></li>
      </ol>
    </nav>
    <span class="pill"><span class="dot" aria-hidden="true"></span> Testimonials</span>
    <h1 id="h1">Our customers trust us because we care</h1>
    <p class="sub">Thirty businesses, in their own words. Some have been with us for close to twenty years. One credits its ISO 9001 registration with saving &pound;420,000.</p>
    <div class="btn-row">
      <a href="{{{{url:contact}}}}" class="btn btn-blue">Talk to a consultant
        {ICON.format('arrow')}
      </a>
      <a href="tel:+441279293007" class="btn btn-ghost-light on-dark">
        {ICON.format('phone')}
        01279 293007
      </a>
    </div>
    <p class="hero-note">
      {ICON.format('check')}
      Every quote below is published exactly as the client wrote it.
    </p>
  </div>
</section>

<!-- ===== NUMBERS ===== -->
<section aria-labelledby="num-t">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Proof</span>
      <h2 id="num-t">The numbers behind the quotes</h2>
    </div>
    <div class="stat-band">
      <div class="stat-item">
        {ICON.format('star')}
        <span class="n">30</span>
        <span class="lbl">Client testimonials on this page</span>
      </div>
      <div class="stat-item">
        {ICON.format('award')}
        <span class="n">100%</span>
        <span class="lbl">Success rate in achieving registration</span>
      </div>
      <div class="stat-item">
        {ICON.format('cal')}
        <span class="n">2002</span>
        <span class="lbl">Trading as a family consultancy since</span>
      </div>
      <div class="stat-item">
        {ICON.format('filex')}
        <span class="n">&pound;420k</span>
        <span class="lbl">Saved by one client&rsquo;s ISO 9001 registration</span>
      </div>
    </div>
  </div>
</section>
"""]

if FEATURED:
    parts.append(f"""<!-- ===== FEATURED ===== -->
<section class="faqs" aria-labelledby="feat-t">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="feat-t">Twenty years with the same consultancy</h2>
      <p>The longest relationship on this page, and the one that says most about how we work.</p>
    </div>
    <figure class="pullquote">
      {STARS}
      <blockquote>{FEATURED['body']}</blockquote>
      <figcaption class="who"><strong>{FEATURED['role']}</strong><span>{FEATURED['company']}</span></figcaption>
    </figure>
  </div>
</section>
""")

parts.append(grid('quality', False, f"{len(GROUPS['quality'])} clients",
                  'Quality management &mdash; ISO 9001 and AS9100',
                  'The standard most of these businesses came to us for first. '
                  '<a href="{{url:iso-9001}}">See our ISO 9001 page</a>.', 'quality'))
parts.append(grid('infosec', True, f"{len(GROUPS['infosec'])} clients",
                  'Information security &mdash; ISO 27001',
                  'Every one of these names David, who is a Lead Auditor with IT Governance. '
                  '<a href="{{url:iso-27001}}">See our ISO 27001 page</a>.', 'infosec'))
parts.append(grid('safety-environment', False, f"{len(GROUPS['safety-environment'])} clients",
                  'Health, safety and the environment &mdash; ISO 45001 and ISO 14001',
                  'Including two migrations from OHSAS 18001. '
                  '<a href="{{url:iso-45001}}">ISO 45001</a> and '
                  '<a href="{{url:iso-14001}}">ISO 14001</a>.', 'safety-environment'))
parts.append(grid('long-term', True, f"{len(GROUPS['long-term'])} clients",
                  'Clients who have stayed with us for years',
                  'Registration is the start of the relationship rather than the end of it.',
                  'long-term'))

parts.append(f"""<!-- ===== NEXT ===== -->
<section aria-labelledby="next-t">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="next-t">Where to go next</h2>
    </div>
    <div class="link-cards">
      <a class="link-card" href="{{{{url:meet-the-family}}}}">
        {ICON.format('users')}
        <h3>Meet the family</h3>
        <p>David, Lucy, Martin and Stephen are named throughout these quotes. Here is who they are.</p>
        <span class="go">Meet the team {ICON.format('arrow')}</span>
      </a>
      <a class="link-card" href="{{{{url:training}}}}">
        {ICON.format('book')}
        <h3>ISO training courses</h3>
        <p>Internal auditor and awareness training, so your team can run the system we build.</p>
        <span class="go">See the courses {ICON.format('arrow')}</span>
      </a>
      <a class="link-card" href="{{{{url:news}}}}">
        {ICON.format('laptop')}
        <h3>From the ADL blog</h3>
        <p>Thirty-eight articles and fourteen videos from the consultants who do the work.</p>
        <span class="go">Read the blog {ICON.format('arrow')}</span>
      </a>
    </div>
  </div>
</section>

<!-- ===== CTA ===== -->
<section class="cta" aria-labelledby="cta-t">
  <div class="cta-inner">
    <h2 id="cta-t">Join them</h2>
    <p>Every business on this page started with one conversation. Tell us what you are being asked for and we&rsquo;ll tell you honestly whether you need certification, and what it would take.</p>
    <div class="btn-row">
      <a href="tel:+441279293007" class="btn btn-white">
        {ICON.format('phone')}
        01279 293007
      </a>
      <a href="{{{{url:contact}}}}" class="btn btn-ghost-light on-dark">Contact us today</a>
    </div>
  </div>
</section>
""")

out = '\n'.join(parts)
PAGE.write_text(out, encoding='utf-8')
print(f"\nwrote {PAGE.name}: {out.count('<section')} sections, {len(out):,} bytes, "
      f"{out.count('<figure class=')} quotes rendered")
