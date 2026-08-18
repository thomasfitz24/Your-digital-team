# yourdigitalteam — site

Eight static pages sharing one header and one footer.

```
index.html        home — hero, services filmstrip, foundation, process, contact
about.html        about
services.html     all services (the filmstrip on its own page)
seo.html          ┐
ppc.html          │
social.html       ├ service pages
email.html        │
content.html      ┘

vendor/site-chrome.css   header + footer styling      ← shared
vendor/site-chrome.js    header + footer markup       ← shared
vendor/gsap.min.js       animation (vendored, no CDN)
vendor/ScrollTrigger.min.js
vendor/fonts/            self-hosted woff2

header-snippet.html      standalone header for pasting into a CMS — see note below
```

## The shared chrome

Every page carries two lines and nothing else:

```html
<link rel="stylesheet" href="vendor/site-chrome.css">
<script src="vendor/site-chrome.js" defer></script>
```

`site-chrome.js` injects the header at the top of `<body>` and the footer at the
bottom, then wires the dropdown, the underline and the scroll spy. If a page
already contains an element with `id="ydtHeader"` the script leaves it alone.

To place the footer somewhere other than the end of the document, put
`<div data-site-footer></div>` where you want it and it will be swapped in.

## Adding or renaming a page

Edit the maps at the top of `vendor/site-chrome.js` — `SERVICES`, `MENU`,
`PILL_NAV`, `COMPANY`. Every page's menu and footer updates from those.

Links are written as `index.html#contact`. When the visitor is already on
`index.html` the script rewrites them to a bare `#contact`, so in-page
scrolling and the underline spy keep working instead of reloading the page.
A link whose file matches the current page gets `aria-current="page"`.

## Known gaps

- **No Web Development page.** The home page's `#foundation` section is the web
  development content, so the Web Dev card and the footer link both point there.
  A dedicated `web-development.html` would slot straight in.
- The five service pages carry placeholder copy in some process steps.
- `assets/logos/` is empty, so the home page marquee shows client names as text
  wordmarks. Drop the artwork in and it swaps over — `assets/logos/README.md`
  lists the exact file names.
- `header-snippet.html` is a *separate copy* for pasting into a CMS that already
  has its own layout. It does not read from `site-chrome.js`, so a nav change
  made here has to be repeated there.
