# Your Digital Team

Static marketing site for **yourdigiteam.com** — a growth marketing / SEO
agency. No build step, no framework, no package manager. Plain HTML, CSS and
vanilla JS that you open in a browser.

Work lives in `yourdigiteam/`. (`kemp-services/` is a separate, older project —
leave it alone unless asked.)

## Running it

Open `yourdigiteam/index.html` in a browser. That is the whole workflow —
every path is relative and GSAP and the fonts are vendored locally, so it
runs off disk with no server and no network.

For clean URLs: `cd yourdigiteam && python3 -m http.server 8000`.

## The pages

```
index.html     home — hero, logo marquee, services filmstrip, foundation, process, CTA
about.html     about
services.html  all services (the filmstrip on its own page)
contact.html   contact + enquiry form
seo.html  ppc.html  social.html  email.html  content.html
```

## Shared chrome — read this before touching the header or footer

The header and footer are **not** in the page files. They live in
`vendor/site-chrome.css` and `vendor/site-chrome.js`, and every page includes
them with two lines:

```html
<link rel="stylesheet" href="vendor/site-chrome.css">
<script src="vendor/site-chrome.js" defer></script>
```

`site-chrome.js` injects the header at the top of `<body>` and the footer at
the bottom, then wires the dropdown, the underline and the scroll spy.

Navigation comes from the `SERVICES`, `MENU`, `PILL_NAV` and `COMPANY` arrays
at the top of that file. **Change nav there, not in the pages.** Links are
written as `index.html#contact`; when the visitor is already on `index.html`
the script rewrites them to a bare `#contact` so in-page scrolling and the
underline spy still work.

`header-snippet.html` is a *separate standalone copy* of the header for
pasting into a CMS. It does not read from `site-chrome.js`, so a nav change
has to be made in both places.

## Design language

Dark, restrained, motion-led. Established over many rounds with the owner —
match it rather than reinventing it.

- **Tokens** are duplicated in each page's `:root` (`--black`, `--white`,
  `--w25`, `--w30`, `--gray5`, `--gray6`, `--line`, `--card-bg`,
  `--card-line`, `--ease`, `--font`, `--header-h`). Keep them in step across
  files. `--ease` is `cubic-bezier(0.22, 1, 0.36, 1)` everywhere.
- **Titles are sentence case, not caps.** The owner asked for this explicitly.
- Glass surfaces: `rgba(255,255,255,0.02–0.08)` + `backdrop-filter: blur()`.
  Always pair with `-webkit-backdrop-filter`.
- Hairlines, not borders: `1px solid var(--line)`.
- Reveal primitives: `[data-reveal]` and `.clip > .slide`, driven by an
  IntersectionObserver that adds `.in-view`.
- Every animation needs a `prefers-reduced-motion: reduce` fallback, and
  hover effects need an `@media (hover: none)` path.

## Gotchas that have already bitten

- **`body { overflow-x: clip }` — never `hidden`.** The services filmstrip
  uses `position: sticky`, and `overflow-x: hidden` creates a scroll container
  that traps it. This has broken twice.
- **GSAP is vendored** to `vendor/`, not loaded from a CDN. The sandbox has no
  CDN access. Do not swap it back to a `<script src="https://...">`.
- **NB International Pro is CDN-loaded** and unreachable in the sandbox, so
  screenshots render in the Inter fallback. That is expected, not a bug.
- **Animate panels to a measured height**, not a guessed one — the dropdown
  sets `maxHeight = scrollHeight + 'px'` so it finishes in step with the icon.
- **Do not duplicate DOM with `innerHTML` or `cloneNode`** if listeners are
  attached — both drop them. The logo marquee builds each repeat group fresh
  for exactly this reason.
- Card heights: measure the element, do not compute from hardcoded padding.

## Verifying changes

There are no tests. Changes are checked in headless Chromium with
playwright-core against `/opt/pw-browsers/chromium`, by screenshotting at
several scroll positions and asserting computed values (rotation degrees,
panel heights, resolved hrefs, `scrollWidth > innerWidth`). Do this rather
than assuming a change worked — most bugs in this project were visual.

## Open items

- `assets/logos/` is empty, so the home page marquee falls back to text
  wordmarks. See `yourdigiteam/assets/logos/README.md` for the file names.
- The phone number and hours on `contact.html` are placeholders.
- Some process-step copy on ppc/social/email/content is placeholder text
  awaiting the owner's real wording.
- Service naming is inconsistent between pages ("Content Creation" vs "SEO
  Content Creation"; "Web Development" vs "Web Development & Analytics").
- There is no `web-development.html`; that card points at `index.html#foundation`.

## Conventions

- British English in all copy.
- Comments explain *why*, not what. Match the existing density — sparse.
- Commit to the working branch; do not open a PR unless asked.
