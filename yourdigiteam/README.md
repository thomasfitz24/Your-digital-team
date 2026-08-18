# yourdigitalteam — site

Eight static pages sharing one header and one footer.

```
index.html        home — hero, services filmstrip, foundation, process, contact
about.html        about
services.html     all services (the filmstrip on its own page)
contact.html      contact page + enquiry form
privacy.html      privacy policy
404.html          not-found page
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

## The contact form

`contact.html` has no back end. It works two ways, set by the form's
`data-endpoint` attribute:

- **Empty (the default).** The fields are composed into a prefilled email and
  the visitor's mail client opens with everything written out. Works today,
  nothing to set up.
- **Set to a form endpoint** (Formspree, Basin, Netlify Forms, your own
  handler). The fields POST there as JSON and the confirmation panel shows on
  success. Set it on the `<form id="contactForm" data-endpoint="">` tag.

Validation, the honeypot and the confirmation panel behave the same either way.

## Analytics

Off by default — the site sets no cookies and shows no banner. To switch it on,
put your GA4 measurement ID in `GA_ID` near the bottom of `vendor/site-chrome.js`.
The consent banner then appears and nothing loads until the visitor accepts;
the choice is stored in localStorage and can be reset from `privacy.html`.

A cookieless tool (Plausible, Fathom) needs no banner at all — swap the body of
`loadAnalytics` for their script and drop the `consentBanner()` call in `mount`.

## SEO furniture

Canonical, Open Graph, Twitter card and icon tags are injected per page. JSON-LD
lives in each page's `<head>`: `ProfessionalService` + `WebSite` on the home
page, `ProfessionalService` + `BreadcrumbList` on about/services/contact, and
`Service` + `BreadcrumbList` on the five service pages. `sitemap.xml` and
`robots.txt` both hardcode `https://www.yourdigiteam.com` — change them together
if the domain changes.

## Known gaps

- **No Web Development page.** The home page's `#foundation` section is the web
  development content, so the Web Dev card and the footer link both point there.
  A dedicated `web-development.html` would slot straight in.
- The five service pages carry placeholder copy in some process steps.
- **The office hours on `contact.html` are a guess** (Mon-Fri, 9am-5:30pm).
- **`privacy.html` needs the proprietor's legal name and an address for
  service** before launch, and `PROPRIETOR` / `SERVICE_ADDRESS` in
  `vendor/site-chrome.js` need the same so the footer carries them.
- **The NB International Pro licence is unverified.** It is loading from
  cdnfonts; it is a commercial Neubau typeface. Confirm a web licence before
  the site goes live commercially.
- `assets/logos/` is empty, so the home page marquee shows client names as text
  wordmarks. Drop the artwork in and it swaps over — `assets/logos/README.md`
  lists the exact file names.
- `header-snippet.html` is a *separate copy* for pasting into a CMS that already
  has its own layout. It does not read from `site-chrome.js`, so a nav change
  made here has to be repeated there.
