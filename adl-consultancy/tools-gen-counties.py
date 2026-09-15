#!/usr/bin/env python3
"""
Generate the five county pages from one skeleton.

They differ only in copy, so writing them by hand is how they drifted apart in
the first place: section counts, paragraph counts and hero lengths all varied
for no editorial reason, while the last two sections were byte-identical on all
five. One generator, one skeleton, per-county content.

Benefit-card copy is read back out of the current pages (it came from the
WordPress database and is genuinely unique per county). Testimonials are read
out of the recovered testimonials file so they are verbatim.
"""

import html
import json
import re
import pathlib

SCRATCH = pathlib.Path(__file__).resolve().parent
PAGES = pathlib.Path('/home/user/Your-digital-team/adl-consultancy/src/pages')

CARDS = json.loads((SCRATCH / 'county_cards.json').read_text())

# ---- testimonials, verbatim from the recovered page -------------------------
def load_quotes():
    text = (SCRATCH / 'source' / 'testimonials.txt').read_text()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    quotes = {}
    for i, line in enumerate(lines):
        if line[0] in '“"' and i + 2 < len(lines):
            body = line.strip('“”"')
            role, company = lines[i + 1], lines[i + 2]
            quotes[company] = (body, role)
    return quotes

QUOTES = load_quotes()


def esc(s):
    """Plain text -> HTML entities, matching the house style of the other pages."""
    s = html.escape(s, quote=False)
    return (s.replace('’', '&rsquo;').replace('‘', '&lsquo;')
             .replace('“', '&ldquo;').replace('”', '&rdquo;')
             .replace('–', '&ndash;').replace('—', '&mdash;').replace('£', '&pound;'))


def abridge(body, limit=300):
    """Cut a long testimonial to the first sentences that fit, never mid-sentence."""
    out = ''
    for sentence in re.split(r'(?<=[.!?])\s+', body):
        if out and len(out) + len(sentence) > limit:
            break
        out = (out + ' ' + sentence).strip()
    return out


ICON = ('<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<use href="#i-{}"/></svg>')
STAR = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
        '<use href="#i-star"/></svg>')

# Icons for the four standard cards, in the order the cards appear.
CARD_ICONS = ['award', 'leaf', 'lock', 'hard']

VIDEOS = [
    ('6LkqgRt29Dg', 'ISO 9001'),
    ('I1cfaYcBNOo', 'ISO 14001'),
    ('_C7X1AgSZOk', 'ISO 27001'),
    ('E4SPtnSjCOU', 'ISO 45001'),
]

# The six things ADL actually does, from the unused services page (wp_posts 109).
SERVICE = [
    'Gap analysis, so you know where you stand before you commit to anything',
    'Process mapping, and the improvements that fall out of it',
    'Document creation &mdash; building and refining your systems',
    'Training for your team, delivered at your premises',
    'Internal auditing and management review meetings',
    'Support during assessment visits, and afterwards',
]

COUNTIES = [
    dict(
        file='13-hertfordshire', key='hertfordshire', county='Hertfordshire',
        out='iso-consultants-hertfordshire.html', wp='/iso-consultants-in-hertfordshire/',
        title='ISO Consultants in Hertfordshire | ADL Consultancy',
        desc='ISO 9001, 14001, 27001 and 45001 consultants for Hertfordshire businesses. Based just across the border in Harlow, with a 100% success rate and no contract to sign.',
        img='3586.jpg',
        img_alt='The ADL Consultancy team outside their Harlow office',
        sub='ISO certification is becoming increasingly important for today&rsquo;s businesses, particularly those who wish to expand by winning larger contracts with both private and public sector organisations. We are based just across the border, so a site visit is a short drive rather than a day out.',
        note='Based in Harlow &mdash; minutes from the Hertfordshire border, and on site when you need us.',
        local=[
            'Based just across the border in Harlow, our ISO experts are perfectly placed to assist Herts-based companies who understand the value in achieving professional certification but would like advice and guidance as they navigate the registration process.',
            'Prove to your prospects that you are committed to investing in quality solutions. Let your stakeholders know you&rsquo;re doing everything you can to continually improve your systems and processes. Demonstrate your willingness to explore smarter, more effective ways of working, whilst meeting your safety, security, and sustainability obligations.',
        ],
        sectors=['Manufacturing', 'Engineering', 'Construction', 'Technology',
                 'Pharmaceuticals', 'Logistics', 'Professional services', 'Recruitment'],
        callout=('Closer than you think',
                 'Harlow sits on the Hertfordshire border, so most of the county is inside an hour. '
                 'That matters more than it sounds: the consultants who write your system are the '
                 'ones who come back to audit it.'),
        quote='Denward Pharmacy Equipment',
        cta_h2='Based in Hertfordshire?',
        cta_p='Tell us what a client or a tender has asked you for, and we&rsquo;ll tell you honestly what it would take to get there.',
    ),
    dict(
        file='14-suffolk', key='suffolk', county='Suffolk',
        out='iso-consultants-suffolk.html', wp='/iso-consultants-in-suffolk/',
        title='ISO Consultants in Suffolk | ADL Consultancy',
        desc='ISO 9001, 14001, 27001 and 45001 consultants for Suffolk businesses. Paperless by default, with specific experience in technology, construction, manufacturing and engineering.',
        img='3587.jpg',
        img_alt='The ADL team around a boardroom table with a client',
        sub='Receive comprehensive guidance from a trusted ISO consultancy servicing small and medium sized businesses in Suffolk. We work paperless wherever we can, which keeps the travelling down and the system usable.',
        note='Paperless by default &mdash; no special software to buy, and no folders to store.',
        local=[
            'The team here at ADL Consultancy has many years&rsquo; experience in helping local organisations improve their systems and realise their truest potential by achieving ISO certification.',
            'Professional, personable, and with a focus on implementing paperless policies wherever possible, our Suffolk ISO consultants can adapt their approach to meet the needs of any business, in any situation. Our way of working ensures we can support companies in a huge range of sectors, though we do have specific expertise in helping firms within the technology, construction, manufacturing, and engineering niches.',
        ],
        sectors=['Technology', 'Construction', 'Manufacturing', 'Engineering',
                 'Agriculture &amp; food', 'Ports &amp; logistics', 'Energy', 'Professional services'],
        callout=('Four sectors we know particularly well',
                 'Technology, construction, manufacturing and engineering. If you are in one of them, '
                 'we have almost certainly seen your processes before &mdash; which shortens the gap '
                 'analysis considerably.'),
        quote='Applied Measurements Ltd',
        cta_h2='Based in Suffolk?',
        cta_p='Tell us which standard you are being asked for, and we&rsquo;ll tell you what registration would genuinely involve for a business your size.',
    ),
    dict(
        file='15-cambridgeshire', key='cambridgeshire', county='Cambridgeshire',
        out='iso-consultants-cambridgeshire.html', wp='/iso-consultants-in-cambridgeshire/',
        title='ISO Consultants in Cambridgeshire | ADL Consultancy',
        desc='ISO 9001, 14001, 27001 and 45001 consultants for Cambridgeshire businesses. We build the system around how you already work, with a 100% success rate and no contract to sign.',
        img='3637.jpg',
        img_alt='An ADL consultant leading a management review meeting with a client team',
        sub='You already understand what ISO registration does for your credibility and your ability to compete for larger contracts. What is less obvious is how much difference it makes to have experienced consultants alongside you while you get there.',
        note='Your system is built around how you already work &mdash; not dropped on top of it.',
        local=[
            'Having a team of dedicated ISO experts in your corner is a sure-fire way to ensure you implement the best possible systems and processes; you meet all ISO requirements without confusion or delay; and you navigate your journey to registration effectively and cost-efficiently, in a way that enhances your operations, not hinders them.',
            'We work with research-led and technical businesses as readily as with contractors and manufacturers. What does not change is the method: we map how the work actually flows before we write a word of it down.',
        ],
        sectors=['Technology &amp; software', 'Life sciences', 'Research &amp; development',
                 'Engineering', 'Manufacturing', 'Construction', 'Agriculture', 'Professional services'],
        callout=('Certifying more than one standard?',
                 'We integrate them into a single management system on one audit cycle, rather than '
                 'running them in parallel. One of our clients holds four standards this way.'),
        quote='Plumis Ltd',
        cta_h2='Based in Cambridgeshire?',
        cta_p='Talk to us about where your systems sit today, and what the standard you are being asked for would actually require.',
    ),
    dict(
        file='16-kent', key='kent', county='Kent',
        out='iso-consultants-kent.html', wp='/iso-consultants-in-kent/',
        title='ISO Consultants in Kent | ADL Consultancy',
        desc='ISO 9001, 14001, 27001 and 45001 consultants for Kent businesses. UKAS accredited certification, a 100% success rate, and no contract to sign.',
        img='DD.jpg',
        img_alt='Two people talking in an informal break-out area',
        sub='Take your business to the next level by gaining UKAS accredited certification with the support of our Kent ISO consultants. Whatever your size or sector, the method is the same: understand how you work, then build the system around it.',
        note='UKAS accredited certification &mdash; the kind your clients will actually check.',
        local=[
            'ADL Consultancy specialises in helping small to medium sized businesses leverage the potential of today&rsquo;s standards. Regardless of your size or the industry you&rsquo;re in, we can help you transform your operations with tried-and-tested ISO methodologies that will improve your systems, enhance your reputation, and enable you to become more competitive in your marketplace.',
            'Registration is worth having only if the certificate is. We work exclusively with UKAS approved registration bodies, so the certificate on your wall stands up when a procurement team looks it up.',
        ],
        sectors=['Construction', 'Manufacturing', 'Logistics &amp; freight', 'Engineering',
                 'Facilities management', 'Technology', 'Recruitment', 'Professional services'],
        callout=('Why UKAS accreditation matters',
                 'Not every certificate is issued by an accredited body, and buyers are increasingly '
                 'checking. Every client we have taken through registration has been certified by a '
                 'UKAS approved body.'),
        quote='Adder',
        cta_h2='Based in Kent?',
        cta_p='Tell us which standard you need and why, and we&rsquo;ll give you an honest view of what it would take &mdash; including if the answer is not yet.',
    ),
    dict(
        file='17-norfolk', key='norfolk', county='Norfolk',
        out='iso-consultants-norfolk.html', wp='/iso-consultants-in-norfolk/',
        title='ISO Consultants in Norfolk | ADL Consultancy',
        desc='ISO 9001, 14001, 27001 and 45001 consultants for Norfolk businesses. A family consultancy with expertise across a wide range of industries and a 100% success rate.',
        img='3803.jpg',
        img_alt='Three people at an ADL training session',
        sub='ADL Consultancy is a family consultancy that has been assisting clients with their ISO requirements in Norfolk and the surrounding counties for many years. Distance has never been the obstacle people expect it to be.',
        note='A family consultancy, working across Norfolk and the surrounding counties since 2002.',
        local=[
            'With expertise in a wide range of industries, our Norfolk ISO consultants are well placed to help any small to medium sized business owners in the local area steer their company through the registration process with ease.',
            'Norfolk is the furthest of the counties we cover, and we would rather be straight about what that means: we plan visits so each one earns its journey, and we do as much as possible paperless in between. Clients tell us the rhythm suits them better than a consultant who drops in weekly with little to show for it.',
        ],
        sectors=['Agriculture &amp; food', 'Manufacturing', 'Engineering', 'Construction',
                 'Energy &amp; offshore', 'Logistics', 'Charities', 'Professional services'],
        callout=('Further away, and it has never been a problem',
                 'We schedule visits so each trip does a full day of work, and handle the rest '
                 'digitally. That is the same paperless approach we take everywhere &mdash; it just '
                 'matters more at this distance.'),
        quote='Refuge',
        cta_h2='Based in Norfolk?',
        cta_p='Distance is not the obstacle it looks like. Tell us what you need and we&rsquo;ll be straight with you about how we would run it.',
    ),
]


def render(c):
    cards = CARDS[c['file']]
    body, role = QUOTES[c['quote']]
    quote = esc(abridge(body))

    parts = []
    A = parts.append

    A(f"""<!--meta
key: {c['key']}
out: {c['out']}
wp: {c['wp']}
title: {c['title']}
description: {c['desc']}
-->
""")

    # --- 1. hero ------------------------------------------------------------
    A(f"""<!-- ===== HERO ===== -->
<section class="hero" aria-labelledby="h1">
  <div class="hero-media">
    <img src="{{{{img:{c['img']}}}}}" alt="" aria-hidden="true" fetchpriority="high">
  </div>
  <div class="hero-inner">
    <nav aria-label="Breadcrumb">
      <ol class="crumbs">
        <li><a href="{{{{url:home}}}}">Home</a></li>
        <li><span aria-current="page">ISO consultants in {c['county']}</span></li>
      </ol>
    </nav>
    <span class="pill"><span class="dot" aria-hidden="true"></span> {c['county']}</span>
    <h1 id="h1">ISO consultants in {c['county']}</h1>
    <p class="sub">{c['sub']}</p>
    <div class="btn-row">
      <a href="{{{{url:contact}}}}" class="btn btn-blue">Contact us today
        {ICON.format('arrow')}
      </a>
      <a href="tel:+441279293007" class="btn btn-ghost-light on-dark">
        {ICON.format('phone')}
        01279 293007
      </a>
    </div>
    <p class="hero-note">
      {ICON.format('check')}
      {c['note']}
    </p>
    <div class="hero-standards">
      <span class="lbl">Standards we take clients through</span>
      <a href="{{{{url:iso-9001}}}}">ISO 9001 &amp; AS9100</a>
      <a href="{{{{url:iso-14001}}}}">ISO 14001</a>
      <a href="{{{{url:iso-27001}}}}">ISO 27001</a>
      <a href="{{{{url:iso-42001}}}}">ISO 42001</a>
      <a href="{{{{url:iso-45001}}}}">ISO 45001</a>
      <span class="stat">
        {ICON.format('award')}
        100% success rate
      </span>
    </div>
  </div>
</section>
""")

    # --- 2. registration bodies --------------------------------------------
    A(f"""<!-- ===== REGISTRATION BODIES ===== -->
<section class="wall" aria-labelledby="wall-t">
  <p id="wall-t">We have a <b>100% success rate</b> in achieving registration for {c['county']} businesses with these UKAS approved registration bodies</p>
  <div class="wall-logos">
    <img src="{{{{img:BSI-logo.png}}}}" alt="BSI" loading="lazy">
    <img src="{{{{img:nqa-logo.jpg}}}}" alt="NQA" loading="lazy">
    <img src="{{{{img:lrqa.jpg}}}}" alt="LRQA" loading="lazy">
    <img src="{{{{img:BAB-logo.jpg}}}}" alt="British Assessment Bureau" loading="lazy">
    <img src="{{{{img:BRE-logo1.jpg}}}}" alt="BRE" loading="lazy">
    <img src="{{{{img:auva.jpg}}}}" alt="Auva" loading="lazy">
  </div>
</section>
""")

    # --- 3. local -----------------------------------------------------------
    chips = '\n'.join(f'      <li>{s}</li>' for s in c['sectors'])
    prose = '\n'.join(f'      <p>{p}</p>' for p in c['local'])
    A(f"""<!-- ===== LOCAL ===== -->
<section aria-labelledby="local-t">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">{c['county']}</span>
      <h2 id="local-t">ISO certification support in {c['county']}</h2>
    </div>
    <div class="prose">
{prose}
    </div>
    <ul class="ind-list">
{chips}
    </ul>
  </div>
</section>
""")

    # --- 4. standards -------------------------------------------------------
    card_html = []
    for (h3, p), icon in zip(cards, CARD_ICONS):
        h3 = h3.replace('ISO27001 - Information', 'ISO27001 &ndash; Information')
        card_html.append(f"""      <article class="benefit">
        {ICON.format(icon)}
        <h3>{h3}</h3>
        <p>{p}</p>
      </article>""")
    A(f"""<!-- ===== STANDARDS ===== -->
<section class="standards" aria-labelledby="std-t">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="std-t">We help businesses in {c['county']} achieve the following ISO standards</h2>
    </div>
    <div class="benefits four">
{chr(10).join(card_html)}
    </div>
    <div class="callout">
      {ICON.format('cpu')}
      <div>
        <h4>Also available: ISO 42001 for artificial intelligence</h4>
        <p>The newest standard on our list, and the one fewest UK businesses hold. If your {c['county']} business builds or resells AI, early certification is a real advantage. <a href="{{{{url:iso-42001}}}}">See our ISO 42001 page</a>.</p>
      </div>
    </div>
  </div>
</section>
""")

    # --- 5. service ---------------------------------------------------------
    items = '\n'.join(f'      <li>{ICON.format("check")} {s}</li>' for s in SERVICE)
    ch, cp = c['callout']
    A(f"""<!-- ===== WHAT WE DO ===== -->
<section aria-labelledby="serv-t">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">How we work</span>
      <h2 id="serv-t">What working with us actually involves</h2>
      <p>The same six things on every project, whichever standard you are going for.</p>
    </div>
    <ul class="check-cols">
{items}
    </ul>
    <div class="callout">
      {ICON.format('pin')}
      <div>
        <h4>{ch}</h4>
        <p>{cp}</p>
      </div>
    </div>
  </div>
</section>
""")

    # --- 6. video -----------------------------------------------------------
    buttons = '\n'.join(
        f'        <a href="#" class="btn btn-outline" data-play="{vid}">{ICON.format("play")} {label}</a>'
        for vid, label in VIDEOS)
    A(f"""<!-- ===== VIDEO ===== -->
<section aria-labelledby="vid-t">
  <div class="split">
    <div>
      <span class="eyebrow">In their own words</span>
      <h2 id="vid-t">Four short films on what each standard involves</h2>
      <p>We made these for clients who wanted to understand a standard before committing to it. Each runs a few minutes and is free of jargon.</p>
      <div class="btn-row">
{buttons}
      </div>
    </div>
    <img src="{{{{img:adl_video_placeholder-scaled.jpg}}}}" alt="" aria-hidden="true" loading="lazy">
  </div>
</section>
""")

    # --- 7. proof -----------------------------------------------------------
    A(f"""<!-- ===== PROOF ===== -->
<section aria-labelledby="proof-t">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Testimonials</span>
      <h2 id="proof-t">What it is like to work with us</h2>
    </div>
    <figure class="pullquote">
      <div class="stars" aria-label="Five out of five">{STAR * 5}</div>
      <blockquote>&ldquo;{quote}&rdquo;</blockquote>
      <figcaption class="who"><strong>{esc(role)}</strong><span>{esc(c['quote'])}</span></figcaption>
    </figure>
    <div class="quotes-foot">
      <a href="{{{{url:testimonials}}}}" class="btn btn-outline">Read all our client testimonials
        {ICON.format('arrow')}
      </a>
    </div>
  </div>
</section>
""")

    # --- 8. related ---------------------------------------------------------
    siblings = [o for o in COUNTIES if o['key'] != c['key']]
    sib_cards = '\n'.join(f"""      <a class="link-card" href="{{{{url:{s['key']}}}}}">
        {ICON.format('pin')}
        <h3>ISO consultants in {s['county']}</h3>
        <p>We cover {s['county']} from the same Harlow base, with the same consultants.</p>
        <span class="go">See the {s['county']} page {ICON.format('arrow')}</span>
      </a>""" for s in siblings)
    A(f"""<!-- ===== RELATED ===== -->
<section class="standards" aria-labelledby="rel-t">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="rel-t">Other areas we cover, and where to go next</h2>
      <p>We work across Essex, London, Middlesex and the surrounding counties.</p>
    </div>
    <div class="link-cards">
{sib_cards}
      <a class="link-card" href="{{{{url:meet-the-family}}}}">
        {ICON.format('users')}
        <h3>Meet the family</h3>
        <p>The eight people who would actually be working on your system, and what each of them is qualified in.</p>
        <span class="go">Meet the team {ICON.format('arrow')}</span>
      </a>
      <a class="link-card" href="{{{{url:training}}}}">
        {ICON.format('book')}
        <h3>ISO training courses</h3>
        <p>Internal auditor, management awareness and staff awareness training, delivered at your premises around your own procedures.</p>
        <span class="go">See the courses {ICON.format('arrow')}</span>
      </a>
    </div>
  </div>
</section>
""")

    # --- 9. cta -------------------------------------------------------------
    A(f"""<!-- ===== CTA ===== -->
<section class="cta" aria-labelledby="cta-t">
  <div class="cta-inner">
    <h2 id="cta-t">{c['cta_h2']}</h2>
    <p>{c['cta_p']}</p>
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

    return '\n'.join(parts)


for c in COUNTIES:
    path = PAGES / f"{c['file']}.html"
    text = render(c)
    path.write_text(text, encoding='utf-8')
    print(f"{c['file']:22} {text.count('<section'):2} sections  {len(text):6,} bytes")
