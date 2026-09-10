# Smart Plus Group — single-file website prototype

`index.html` is a self-contained, viewable prototype of the Smart Plus Group rebrand.
Open it in any browser (double-click; no server needed). All images and logos are
embedded, so it works offline and can be emailed as one file.

## The four pages

| Route (hash)  | Brand               | Header logo          | Accent colour        |
|---------------|---------------------|----------------------|----------------------|
| `#home`       | Smart Plus Group    | group (tri-colour)   | white `#FFFFFF`      |
| `#heating`    | Smart Plus Heating  | HEATING (red)        | red `#E5232A`        |
| `#electrical` | Smart Plus Electric | ELECTRIC (yellow)    | yellow `#F7C719`     |
| `#cooling`    | Smart Plus Aircon   | AIRCON (blue)        | blue `#1E9BE8`       |

Add `/section` to scroll, e.g. `#home/contact`, `#home/reviews`, `#home/brands`,
`#heating/servicing`.

The Heating page carries the boiler-servicing content that was supplied, re-headed
as "Heating & Boilers" so it reads as the brand page; the servicing block is the
`#servicing` section. The Electrical and Cooling pages use the supplied content
as-is (Cooling copy now says "Smart Plus Aircon" to match the logo).

The **Services** dropdown (and the mobile menu) has an "Our Brands" group linking to
the three brand pages, followed by the existing service links. Switching page sets
`<body data-brand="…">`; CSS variables (`--accent`, `--accent-rgb`, `--accent-hover`,
`--accent-ink`) recolour the header CTA, icons, buttons, labels, borders, footer
underlines and focus rings, and a small router swaps every `img.js-brand-logo`.

Links to pages that live on the real site but are not in this prototype
(`/about-us`, `/faq`, `/boiler-installations` …) show a small toast instead of
navigating. That behaviour is one block in the script at the bottom of the file.

## Editing / rebuilding

```
smart-plus-group/
├── index.html            built output (do not edit by hand)
├── src/template.html     the page — markup, CSS, JS, with {{IMG:name}} placeholders
├── src/build.py          python3 src/build.py        -> index.html (base64-embedded)
│                         python3 src/build.py --cdn  -> index.cdn.html (Squarespace CDN URLs)
├── src/cdn-urls.json     name -> original CDN URL map used by --cdn
├── src/assets/           every image, named as referenced in the template
└── src/logo-source/      make_logos.py + font + source artwork used to draw the logos
```

Edit `src/template.html`, then run `python3 src/build.py`.

## Swapping in the real logo files

The four logos in `src/assets/logo-*.png` were rebuilt from the existing Smart Plus
wordmark plus Montserrat Bold for the coloured descriptor. To use the official
artwork, drop the files in with the same names (`logo-group.png`, `logo-heating.png`,
`logo-electric.png`, `logo-aircon.png`; transparent PNG, white wordmark) and rebuild.
Header sizing assumes roughly a 4.5:1 aspect for the sub-brands and about 6:1 for
the group lockup; adjust the `.sh-logo img` heights in the template if the artwork
differs. The group logo's three descriptor words are inherently small in a header,
so a stacked/compact variant for phones would be worth producing with the final
artwork.

## Moving it into Squarespace

* Header: everything inside `<div id="sh-root">…</div>` plus the mobile overlay, and
  the `sh-` CSS block (it keeps `!important` so it survives Squarespace styles).
* Footer: the `<footer class="sf-root">` block and the `sf-` CSS.
* Pages: the `<main id="page-…">` blocks, one per Squarespace page, with the `sp-`
  (home) or `svc-` (service pages) CSS. On each page set `data-brand` on `<body>`
  (or on a wrapper and change the selectors) to pick the accent.
* Replace the `{{IMG:…}}`/data URIs with hosted images via `build.py --cdn`.
