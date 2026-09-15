# ADL Consultancy — website build

18 static pages, plus a header and a footer that are their own code.
Every page runs 8-11 sections; the homepage, which the client approved, is the bar.

```
python3 check.py     # validate src/ — fails on anything that must not ship
python3 build.py     # assemble dist/ and dist/preview/
```

No dependencies. Python 3 standard library only.

---

## ⚠️ Read this first: the live site moved to Squarespace

The content inventory this build was written from was captured on **3 September 2026**,
when adlconsultancy.com ran WordPress + Avada. As of **14 September 2026** the live
site returns `server: Squarespace`, and:

- every `/wp-content/uploads/…` image URL now **404s**
- every WordPress slug now **404s** — `/contact-us/`, `/meet-the-family/`,
  `/iso-9001-as9100-quality-aerospace/`, `/training/`, `/news/`, `/partners/`, and all the rest
- there is no Avada Global Header/Footer to paste into any more

Two consequences for this build:

1. **Images are vendored, not hotlinked.** All 29 are in `assets/img/`, recovered
   before the old site went down. They are the only surviving copies we have.
2. **The `wp:` slugs in each page's meta block are the *old* WordPress URLs.** They
   are recorded so nothing is lost, and the deliverable's internal links are built
   from them — so they need remapping to the new URL structure before launch.
   `dist/preview/` uses local filenames instead and is unaffected.

The four hero videos are unaffected — they live on ADL's own YouTube channel
(`@adlconsultancy8840`), not on the website.

---

## Layout

```
build.py                  the whole build, ~170 lines
check.py                  source validator — run it before build.py
tools-gen-counties.py     regenerates the five county pages from one skeleton
tools-gen-testimonials.py regroups the 30 testimonials by standard
tools-gen-news.py         regroups the 38 news posts by topic
assets/img/               31 vendored images (recovered from the old WordPress site)
src/
  partials/
    header.html           ← THE header. Edit here, nowhere else.
    footer.html           ← THE footer. Edit here, nowhere else.
    icons.html            the 25-icon SVG sprite, shared by everything
    styles.css            ~700 shared lines, every rule scoped under .adl-page
    scripts.js            progressive enhancement only — nothing here is required
    shell.html            the preview document wrapper
  pages/                  18 pages: body content + a <!--meta--> block each
dist/                     GENERATED — the deliverable. Never hand-edit.
dist/preview/             GENERATED — review only. Do NOT hand these off.
```

Edit `src/`. Run `python3 build.py`. Both output trees regenerate.

## Page meta block

Every file in `src/pages/` starts with:

```html
<!--meta
key: iso-27001                          unique id, used by {{url:…}}
out: iso-27001.html                     filename in dist/
wp: /iso-27001-information-security/    live slug (currently stale — see above)
title: …                                <title>
description: …                          meta description
-->
```

## Tokens

| Token | in `dist/preview/` | in `dist/` (deliverable) |
|---|---|---|
| `{{url:iso-27001}}` | `iso-27001.html` | the page's `wp:` slug |
| `{{img:BSI-logo.png}}` | `../assets/img/BSI-logo.png` | `WP_ASSET_BASE` + filename |

`WP_ASSET_BASE` is set near the top of `build.py`. Change it once the images have
been uploaded to the new platform, then rebuild.

The build fails loudly on an unknown page key or a missing image, rather than
emitting a broken link.

## What to hand off

`dist/` is the deliverable. **Every page file is body markup only** — no header,
no footer, no `<html>`/`<head>`/`<body>` wrapper — because the header and footer
are their own files.

| File | Where it goes |
|---|---|
| `header.html` | the site's global header — **once**, site-wide |
| `footer.html` | the site's global footer — **once**, site-wide |
| `_icons.html` | **once**, site-wide, before the content (see below) |
| `_shared-styles.css` | once, site-wide (a Custom CSS box, or enqueued) |
| `_shared-scripts.js` | once, site-wide |
| `index.html`, `iso-27001.html`, … | one per page, into that page's content area |

Each page file's opening comment names its target URL.

### `_icons.html` is not optional

All 25 SVG icon definitions live in one sprite. The header, the footer and every
page reference it — **343 `<use>` references** in total. It used to sit inside
`header.html`, which meant the pages silently depended on the ADL header being
present; if anyone used a different global header, every icon on the site would
render blank with no error. It is now its own file so that coupling is explicit.
Add it once, site-wide, before the content.

### `dist/preview/`

The same pages with header, footer and sprite assembled in, so they open in a
browser for review. **Do not hand these off** — pasting one into a site that
already has a global header gives you two headers.

## Nothing breaks without JavaScript

Content editors on hosted platforms routinely strip inline `<script>`. So:

- the standards panels render **stacked and readable**; JS upgrades them to tabs
- the hero shows its poster frame; JS swaps in the muted looping video
- the mobile menu is only hidden once JS is present to reopen it
- the video lightbox is inert rather than broken

Verified by loading the build with JavaScript disabled.

## Placeholders

**3** amber `.adl-placeholder` blocks remain. Each one was searched for
exhaustively across `wp_posts`, `wp_options` and the old site before being left
open — these are genuinely absent, not merely unfound:

| Page | Missing |
|---|---|
| Contact | full postal address + company registration number |
| Training | pricing, duration, delivery format, booking route |
| Privacy policy | registered office, company number, ICO number, retention period |

The privacy policy is now its own page (`18-privacy-policy.html`), built from
the real Privacy Notice and Cookie statement recovered from the contact page,
and the footer links to it. That closes the third of the original nine.

Find them with:

```
grep -rl 'adl-placeholder' dist/*.html
```

## Recovered from the database

The old WordPress dump filled in most of what the content inventory could not
reach, because the site had already moved to Squarespace and was 404ing:

- **Every real hero H1 and sub-heading**, pulled from the Fusion slider's
  `pyre_heading` / `pyre_caption` meta. News is "A word from our consultants",
  Partners "Meet our partners", Contact "Why not get in touch?" — all three were
  guesses before.
- **The real enquiry form**: full name, telephone, email, enquiry, a privacy
  opt-in, and a "Let's Talk" button. Submissions went to
  `customerservices@adlconsultancy.com`. The mock-up we had invented a company
  field and a standards dropdown that never existed.
- **All 38 news posts** with real slugs and dates. The inventory had 14, six of
  them with no recoverable URL.
- **The two missing ISO 42001 focus areas** — "Security and safety" and "Ethical
  AI development". The indexed copy was truncated after three of five.
- **Full Hertfordshire and Suffolk page content**, so both are now real pages
  rather than one orphan paragraph behind a placeholder.
- **The true homepage hero**: a self-hosted `/videos/Website.mp4`, muted and
  looping, with `adl_video_placeholder-scaled.jpg` as its poster. The MP4 itself
  404s now — it did not survive the migration. The build uses ADL's own YouTube
  "Home Page Intro" in its place, with the original poster frame restored.

### Five county pages, all built

The database revealed **five** `/iso-consultants-in-{county}/` pages, not the two
the content inventory knew about. All five are now built from their real copy:
Hertfordshire, Suffolk, Cambridgeshire, Kent and Norfolk. Each carries its own
intro, four standard blocks (9001/AS9100, 14001, 27001, 45001) and a "How we can
help" close, and all five are linked from the footer.

Worth repeating the caveat from the keyword work: none of these county terms has
any search volume — `iso consultants hertfordshire` and `iso consultants suffolk`
both return **zero** in Semrush's UK database. They are useful as sales collateral
to link to directly, not as pages that will attract traffic on their own.

## Copy that needs client sign-off

Two blocks were written by us rather than recovered, to bring thin pages up to
the depth of ISO 9001 and ISO 45001. They are marked with `NEW COPY` comments in
`src/pages/`:

- ISO 14001 — "Why invest in ISO 14001?"
- ISO 27001 — "Why invest in ISO 27001?"

(The News and Partners hero copy was on this list until the database arrived —
both are now ADL's own wording, so they no longer need sign-off.)
