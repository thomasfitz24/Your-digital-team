# Homepage — version 15 (prototype)

A redesign built to compare against v14, not to replace it yet. Same two
files (`homepage.html`, `homepage.css`), same header, footer and menu, same
palette, same fail-safes. Nothing live is touched.

## The idea

One visitor: a UK business owner who suspects they are wasting money on
marketing and does not trust agencies. One job: get them to ask for the free
growth plan. Everything on the page either moves them toward that or is cut.

Nine sections became five:

1. **Proof** — the hero is a report, not a poster. "Growth you can audit."
   next to a client dashboard panel: tracked keyword, the position journey
   (#12 → #3), a 12-month curve, three KPIs. Four client tabs; it cycles on
   its own until someone touches it. It looks like the product because it is
   drawn from it.
2. **Trusted by** — the logo strip from v14.1.
3. **How we work** — the four steps and the three promises in one section, as
   a rail that fills as you read. Every step ends with what you hold: *You
   get — a written audit, yours to keep.*
4. **Results** — three builds with one number each (9,000+ boilers; #1 for
   "caravan storage costa brava"; #1 for "chimney sweep essex") and a link to
   all nine on the web development page.
5. **Services** — an index, not a brochure: seven rows, one line each. They
   have their own pages; the homepage's job is routing.
6. **Start** — the question pills feed a three-field form *on the page*. It
   posts to your existing `/api/contact` with the same payload the contact
   page sends (honeypot and timing check included), shows the reference on
   success, and falls back to email on error. One step instead of two.

Dropped from the homepage: the bento of decorative instruments, the six
service cards, the journal, the standalone app promo (the app is now the
hero), the spotlight, grain and magnetic buttons.

## Typography

Headlines are set in **Bricolage Grotesque** (Google Fonts, loaded in the
head) so the page has a face of its own; Inter stays for body, IBM Plex Mono
for data. This is a proposal — swap the `--display` token in the CSS to
revert to Inter everywhere.

## The numbers

Keyword positions and climbs are the ones from your v13 app mock. Everything
else in the report panel is illustrative and the panel says so ("Sample
view" in the bar, "Figures are illustrative until a client shares theirs" in
the foot). All four client views live in one table at the top of the script
(`CLIENTS`); replace the figures with real ones and the panel, the counters
and the chart follow.

## Verified

Rendered in Chromium at 1440 and 390: no console errors or warnings, nothing
left invisible after scrolling, no horizontal overflow, no text under 10px,
no off-palette colour, all three typefaces loaded, tap targets ≥36px on
phone. Tabs switch, pills fill the form, empty fields are caught, and a
stubbed `/api/contact` returns the success state. The no-CDN fallback shows
the page fully with tabs still working; reduced motion shows everything with
no transforms.

## Installing

Same as v14: replace `homepage.html` / `homepage.css`. The form posts to
`/api/contact` on the same origin, so it only works once the page is served
from yourdigiteam.com.
