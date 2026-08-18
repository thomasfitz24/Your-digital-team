# Squarespace build

Generated from the standalone site by `tools/build-squarespace.py`. Do not edit
these files by hand — change the source in `yourdigiteam/` and re-run the
script, or your edits are lost on the next build.

```
python3 tools/build-squarespace.py
```

## What goes where

**1. The header and footer — once, site-wide.**
`_header-injection.html` → Squarespace → **Settings → Advanced → Code
Injection → HEADER**. Paste the whole file. It loads the fonts, loads GSAP for
every page, hides Squarespace's own header and footer, and builds ours.

**2. Each page — one Code Block per page.**
Create the page at the URL in the table, add a single **Code Block**, paste the
matching file, and set the block to full width.

| File | Squarespace page URL |
| --- | --- |
| `index.html` | `/` (set as home page) |
| `about.html` | `/about` |
| `services.html` | `/services` |
| `contact.html` | `/contact` |
| `seo.html` | `/seo` |
| `ppc.html` | `/ppc` |
| `social.html` | `/social` |
| `email.html` | `/email` |
| `content.html` | `/content` |
| `web-development.html` | `/web-development` |
| `privacy.html` | `/privacy` |
| `404.html` | `/404` |

**The URLs must match exactly.** Navigation, the active-page underline and the
footer's current-page marker all key off `location.pathname`. A page at
`/seo-services` instead of `/seo` still loads, but the header will not know
which page you are on.

## Before you paste

Set `YDT_ASSETS` at the top of the header injection to wherever you upload the
logo and project images, with a trailing slash. Until then the logo strip shows
text wordmarks and the project cards show generated artwork — both by design,
neither looks broken.

## What the script changes, and why

- **Everything is scoped under `.ydt-page`.** The site's CSS styles `body`,
  `*`, `a` and `section` directly, which would fight Squarespace's own reset
  across the whole page. Scoping confines it to our block.
- **Squarespace's typography is out-specified.** Themes style `h1`–`h6` and
  `a` with element selectors, which beat inheritance — without this the
  headings come out in the theme's serif.
- **Full-bleed.** A Code Block sits in a fixed-width column; the wrapper breaks
  out with `width: 100vw; margin-left: calc(50% - 50vw)`.
- **Overflow is forced visible** on Squarespace's containers. Any ancestor with
  a non-visible overflow becomes a scroll container, and a scroll container
  traps the `position: sticky` the services filmstrip depends on.
- **GSAP and the fonts move to CDNs.** They are vendored locally in the
  standalone site because it was built in a sandbox with no CDN access.
- **`.html` links become clean URLs**, in the markup and in the JS nav maps.
- **`</script>` inside JS is escaped.** `site-chrome.js` carries one in a usage
  comment, which would otherwise end the injected block early — this bit.

## Known limits

- **Scripts often do not run in Squarespace's editor preview.** Save and view
  the live page before concluding something is broken.
- **These are big blocks** — the home page is ~68KB and web development ~62KB.
  That is fine to paste, but Squarespace's editor gets sluggish with them.
- **The contact form still needs an endpoint.** Same as the standalone site:
  set `data-endpoint` on the form, or it falls back to opening a mail client.
- **`404.html` is a normal page here.** Squarespace's own 404 handling is set
  separately under Design → Pages.
