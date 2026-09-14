# ADL Consultancy — website build

14 static pages, plus a header and a footer that are their own code.

```
python3 build.py
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
   are recorded so nothing is lost, but they need remapping to the new Squarespace
   URL structure before `dist/wp/` is any use. Until that happens, use `dist/`.

The four hero videos are unaffected — they live on ADL's own YouTube channel
(`@adlconsultancy8840`), not on the website.

---

## Layout

```
build.py                  the whole build, ~140 lines
assets/img/               29 vendored images (recovered from the old WordPress site)
src/
  partials/
    header.html           ← THE header. Edit here, nowhere else.
    footer.html           ← THE footer. Edit here, nowhere else.
    styles.css            ~700 shared lines, every rule scoped under .adl-page
    scripts.js            progressive enhancement only — nothing here is required
    shell.html            the preview document wrapper
  pages/                  14 pages: body content + a <!--meta--> block each
dist/                     GENERATED. Open any file in a browser. Never hand-edit.
dist/wp/                  GENERATED. Body-only paste payloads + shared CSS/JS.
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

| Token | in `dist/` | in `dist/wp/` |
|---|---|---|
| `{{url:iso-27001}}` | `iso-27001.html` | the page's `wp:` slug |
| `{{img:BSI-logo.png}}` | `assets/img/BSI-logo.png` | `WP_ASSET_BASE` + filename |

`WP_ASSET_BASE` is set near the top of `build.py`. Change it once the images have
been uploaded to the new platform, then rebuild.

The build fails loudly on an unknown page key or a missing image, rather than
emitting a broken link.

## Two output trees, and why

`dist/` bakes the header and footer into every page, so any file opens standalone
in a browser for client review.

`dist/wp/` contains body markup only, because on the live site the header and
footer are global. Pasting a full `dist/` page into a site that already has a
global header would render the header **twice**. Also in `dist/wp/`:

- `_shared-styles.css` — paste once, site-wide (Custom CSS)
- `_shared-scripts.js` — enqueue once, site-wide
- `header.html` / `footer.html` — the global header and footer

## Nothing breaks without JavaScript

Content editors on hosted platforms routinely strip inline `<script>`. So:

- the standards panels render **stacked and readable**; JS upgrades them to tabs
- the hero shows its poster frame; JS swaps in the muted looping video
- the mobile menu is only hidden once JS is present to reopen it
- the video lightbox is inert rather than broken

Verified by loading the build with JavaScript disabled.

## Placeholders

9 amber `.adl-placeholder` blocks mark content the client has not supplied —
contact details, the News and Partners hero copy, the truncated ISO 42001 bullet
list, training course details, and the two county pages. Each states exactly what
is needed. Find them all with:

```
grep -rl 'adl-placeholder' dist/*.html
```

## Copy that needs client sign-off

Three blocks were written by us rather than recovered, to bring thin pages up to
the depth of ISO 9001 and ISO 45001. They are marked with `NEW COPY` comments in
`src/pages/`:

- ISO 14001 — "Why invest in ISO 14001?"
- ISO 27001 — "Why invest in ISO 27001?"
- News and Partners — hero H1 and sub-heading
