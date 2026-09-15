#!/usr/bin/env python3
"""
Rebuild the news index: group 38 posts by topic and add the video library.

The posts are parsed out of the current page and re-emitted with their date,
title, excerpt and link intact. Two defects are fixed on the way through: an
unescaped ampersand in one title, and excerpts that begin with a raw YouTube
URL because the post embedded a video in its first line.
"""

import html
import json
import re
import pathlib

SCRATCH = pathlib.Path(__file__).resolve().parent
PAGE = pathlib.Path('/home/user/Your-digital-team/adl-consultancy/src/pages/10-news.html')

ICON = ('<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<use href="#i-{}"/></svg>')

# ---- parse the existing cards ----------------------------------------------
raw = PAGE.read_text(encoding='utf-8')
posts = []
for m in re.finditer(
        r'<article class="post">\s*<span class="date">(.*?)</span>\s*<h3>(.*?)</h3>\s*'
        r'<p>(.*?)</p>\s*<a class="more" href="(.*?)">', raw, re.S):
    date, title, excerpt, href = (x.strip() for x in m.groups())

    # An unescaped & is invalid and can swallow the following text as an entity.
    title = re.sub(r'&(?!(?:[a-zA-Z]+|#\d+);)', '&amp;', title)

    # Some posts embedded a video in their first line, so the excerpt the
    # indexer took begins with a bare URL. Drop it — the video library below
    # is where those belong.
    excerpt = re.sub(r'^https?://\S+\s*', '', excerpt).strip()
    excerpt = re.sub(r'&(?!(?:[a-zA-Z]+|#\d+);)', '&amp;', excerpt)

    slug = href.rstrip('/').rsplit('/', 1)[-1]
    posts.append(dict(date=date, title=title, excerpt=excerpt, href=href, slug=slug))

print(f'parsed {len(posts)} posts')

# ---- topic grouping ---------------------------------------------------------
# Slug-driven, so it is inspectable and stable rather than a guess from prose.
TOPICS = [
    ('infosec', 'Information security and cyber', 'lock', False, '{{url:iso-27001}}',
     'The standard your enterprise clients ask about first.', [
         'dangers-of-social-engineering-lego-animation', 'cyber-essentials',
         'how-a-scammer-thinks', 'why-employ-a-clear-screen-policy',
         'what-makes-a-strong-password', 'how-big-is-your-data-footprint',
         'phishing', 'password', 'gdpr', 'data-breach']),
    ('ai', 'AI and the new ISO 42001 standard', 'cpu', True, '{{url:iso-42001}}',
     'Very few UK businesses hold it yet.', [
         'deepfakes-iso-27001', 'should-small-businesses-embrace-ai',
         'iso-42001-artificial-intelligence']),
    ('quality', 'Quality, risk and continual improvement', 'award', False, '{{url:iso-9001}}',
     'The standard most tenders ask for.', [
         'customer-complaints', 'january-iso',
         'why-training-should-be-your-culture-adl-paul-animation',
         'objectives-that-mean-something', 'chairing-productive-meetings',
         'think-risk', 'leadership', 'internal-audit', 'management-review',
         'nonconformity', 'continual-improvement']),
    ('safety', 'Health, safety and the environment', 'hard', True, '{{url:iso-45001}}',
     'For teams on site, on the road or at client premises.', [
         'construction-safety-audit-myths',
         'spring-into-safety-mitigating-seasonal-workplace-risks',
         'covid-19-risk-assessment', 'health-and-safety-said-so',
         'environment', 'sustainab', 'net-zero']),
]


def topic_of(p):
    for key, _, _, _, _, _, slugs in TOPICS:
        for s in slugs:
            if s in p['slug']:
                return key
    return 'inside-adl'


GROUPS = {k: [] for k, *_ in TOPICS}
GROUPS['inside-adl'] = []
for p in posts:
    GROUPS[topic_of(p)].append(p)
for k, v in GROUPS.items():
    print(f'  {k:12} {len(v)}')

# ---- the video library, verified against the database this session ----------
VIDEOS = [
    ('0grNnOaBneM', 'What makes a strong password?'),
    ('smHLiOuEN2Y', 'Leadership'),
    ('ZgwDAIfIZS0', 'Why employ a clear screen policy?'),
    ('s5rvMdQdyj0', 'How a scammer thinks'),
    ('6hehS_Kl_Io', 'Introducing Joseph'),
    ('I65o_d3o8WE', 'Think risk'),
    ('c1O4_ibZQKo', 'Chairing productive meetings'),
    ('lUjnxVUU5F0', 'Why training should be your culture'),
    ('KVUZLfR3U7s', 'Introducing Sarah'),
    ('4evl6FAzCOY', 'Throw back to our beginning'),
    ('IAFCGTM5mHY', 'The dangers of social engineering'),
    ('J5_Tl7UZFxw', 'Going limited: the directors in conversation'),
    ('ZuHKM0eNHUI', 'Deepfakes and ISO 27001'),
    ('wvXwOp_0_7o', 'Turning customer complaints into improvement'),
]


FAMILY_RUN = re.compile(r'family[\s-]run', re.I)


def post_html(p):
    # These excerpts are ADL's own published wording. Where one says "family-run"
    # we leave it alone rather than edit a published article, and mark it so the
    # house-style check knows this is a quotation, not our copy.
    marker = ''
    if FAMILY_RUN.search(p['title'] + p['excerpt']):
        marker = ("      <!-- verbatim: excerpt quoted from ADL's own published post. "
                  "Their wording, left as written. -->\n")
    return f"""{marker}      <article class="post">
        <span class="date">{p['date']}</span>
        <h3>{p['title']}</h3>
        <p>{p['excerpt']}</p>
        <a class="more" href="{p['href']}">Read more &rarr;</a>
      </article>"""


parts = [f"""<!--meta
key: news
out: news.html
wp: /news/
title: News &amp; Insight | ADL Consultancy
description: Thirty-eight articles and fourteen videos from the ADL Consultancy team on ISO 9001, 14001, 27001, 42001 and 45001, grouped by topic so you can find what applies to you.
-->

<!-- ===== HERO ===== -->
<section class="hero" aria-labelledby="h1">
  <div class="hero-media">
    <img src="{{{{img:3589.jpg}}}}" alt="" aria-hidden="true" fetchpriority="high">
  </div>
  <div class="hero-inner">
    <nav aria-label="Breadcrumb">
      <ol class="crumbs">
        <li><a href="{{{{url:home}}}}">Home</a></li>
        <li><span aria-current="page">News</span></li>
      </ol>
    </nav>
    <span class="pill"><span class="dot" aria-hidden="true"></span> News &amp; insight</span>
    <h1 id="h1">A word from our consultants</h1>
    <p class="sub">Thirty-eight articles and fourteen videos, written and filmed by the consultants who do the work. Information security, quality, safety, AI &mdash; and the occasional look inside a family consultancy.</p>
    <div class="btn-row">
      <a href="#topics" class="btn btn-blue">Browse by topic
        {ICON.format('arrow')}
      </a>
      <a href="#videos" class="btn btn-ghost-light on-dark">
        {ICON.format('play')}
        Watch the videos
      </a>
    </div>
    <p class="hero-note">
      {ICON.format('check')}
      Written by the consultant who does the work, not by a marketing agency.
    </p>
  </div>
</section>

<!-- ===== NUMBERS ===== -->
<section aria-labelledby="num-t">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">The archive</span>
      <h2 id="num-t">The archive in numbers</h2>
    </div>
    <div class="stat-band">
      <div class="stat-item">
        {ICON.format('book')}
        <span class="n">38</span>
        <span class="lbl">Published articles</span>
      </div>
      <div class="stat-item">
        {ICON.format('play')}
        <span class="n">14</span>
        <span class="lbl">Videos, animations and podcasts</span>
      </div>
      <div class="stat-item">
        {ICON.format('sliders')}
        <span class="n">5</span>
        <span class="lbl">Topics, from information security to AI</span>
      </div>
      <div class="stat-item">
        {ICON.format('cal')}
        <span class="n">2019</span>
        <span class="lbl">Publishing since</span>
      </div>
    </div>
  </div>
</section>
"""]

# ---- topic picker -----------------------------------------------------------
cards = []
for key, label, icon, _, _, blurb, _ in TOPICS:
    cards.append(f"""      <a class="link-card" href="#{key}">
        {ICON.format(icon)}
        <h3>{label}</h3>
        <p>{blurb} {len(GROUPS[key])} article{'s' if len(GROUPS[key]) != 1 else ''}.</p>
        <span class="go">Read them {ICON.format('arrow')}</span>
      </a>""")
cards.append(f"""      <a class="link-card" href="#inside-adl">
        {ICON.format('users')}
        <h3>Inside the family consultancy</h3>
        <p>New faces, milestones and how the business is run. {len(GROUPS['inside-adl'])} articles.</p>
        <span class="go">Read them {ICON.format('arrow')}</span>
      </a>""")
cards.append(f"""      <a class="link-card" href="#videos">
        {ICON.format('play')}
        <h3>The video library</h3>
        <p>Animations, explainers and podcasts, including the LEGO series. 14 videos.</p>
        <span class="go">Watch them {ICON.format('arrow')}</span>
      </a>""")

parts.append(f"""<!-- ===== TOPICS ===== -->
<section class="faqs" id="topics" aria-labelledby="top-t">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="top-t">Find what applies to you</h2>
      <p>Six ways in. Every article was written by one of our consultants.</p>
    </div>
    <div class="link-cards">
{chr(10).join(cards)}
    </div>
  </div>
</section>
""")

# ---- one section per topic --------------------------------------------------
for key, label, icon, tint, link, blurb, _ in TOPICS:
    items = GROUPS[key]
    if not items:
        continue
    cls = ' class="faqs"' if tint else ''
    parts.append(f"""<!-- ===== {label.upper()} ===== -->
<section{cls} id="{key}" aria-labelledby="{key}-t">
  <div class="wrap">
    <div class="sec-head left">
      <span class="eyebrow">{len(items)} article{'s' if len(items) != 1 else ''}</span>
      <h2 id="{key}-t">{label}</h2>
      <p>{blurb} <a href="{link}">See the standard</a>.</p>
    </div>
    <div class="posts">
{chr(10).join(post_html(p) for p in items)}
    </div>
  </div>
</section>
""")

items = GROUPS['inside-adl']
parts.append(f"""<!-- ===== INSIDE ADL ===== -->
<section id="inside-adl" aria-labelledby="inside-t">
  <div class="wrap">
    <div class="sec-head left">
      <span class="eyebrow">{len(items)} articles</span>
      <h2 id="inside-t">Inside the family consultancy</h2>
      <p>New faces, milestones, and how the business is run. <a href="{{{{url:meet-the-family}}}}">Meet the family</a>.</p>
    </div>
    <div class="posts">
{chr(10).join(post_html(p) for p in items)}
    </div>
  </div>
</section>
""")

# ---- video library ----------------------------------------------------------
vids = '\n'.join(f"""      <a class="link-card" href="#" data-play="{vid}">
        {ICON.format('play')}
        <h3>{title}</h3>
        <span class="go">Watch {ICON.format('arrow')}</span>
      </a>""" for vid, title in VIDEOS)
parts.append(f"""<!-- ===== VIDEOS ===== -->
<section class="faqs" id="videos" aria-labelledby="vid-t">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">14 videos</span>
      <h2 id="vid-t">Watch: the ADL video library</h2>
      <p>Animations, explainers and podcasts. The LEGO series featuring ADL Paul started as a way to lighten up a presentation and is now used as training material by our ISO 27001 clients.</p>
    </div>
    <div class="link-cards">
{vids}
    </div>
  </div>
</section>

<!-- ===== CTA ===== -->
<section class="cta" aria-labelledby="cta-t">
  <div class="cta-inner">
    <h2 id="cta-t">Turn the advice into a system that works</h2>
    <p>Everything above is what our consultants tell clients anyway. A conversation is where it stops being reading and starts being your management system.</p>
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
rendered = out.count('<article class="post">')
assert rendered == len(posts), f'lost posts: {rendered} rendered, {len(posts)} parsed'
print(f"\nwrote {PAGE.name}: {out.count('<section')} sections, {len(out):,} bytes, "
      f'{rendered} posts, {len(VIDEOS)} videos')
