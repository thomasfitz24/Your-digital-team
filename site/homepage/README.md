# Homepage — version 14 (motion)

Two files, same shape as the ones you sent: `homepage.html` and `homepage.css`.
Content, layout and copy are unchanged; the motion layer is rebuilt.

## What changed

**One engine.** v13 had four separate motion systems fighting each other
(an IntersectionObserver reveal system, a CSS marquee, a "motion enhancer"
script and a "legacy enhancer" script). All of it is replaced by GSAP +
ScrollTrigger + Flip + CustomEase, driven from one script at the end of the
page block, with one custom ease (`signal`, your brand curve) shared by every
movement. Native scrolling is never taken over: nothing is pinned, nothing
snaps, no smooth-scroll library. Scroll-linked motion is a scrub of the real
scrollbar; entrances play once.

**What moves now**

- Hero — one choreographed load: header, eyebrow, masked headline lines, copy,
  buttons, the console rising in 3D with its counters, chart and chips, the
  orbit rails drawing themselves, the stats settling. The headline word cycles
  and the line re-centres smoothly. On scroll the copy lifts away faster than
  the console (depth), the glow swells.
- The console is **interactive**: the five channel chips are real buttons.
  Pick one and the KPIs re-count, the chart morphs, the labels swap. It cycles
  on its own every 5.5s until someone touches it. All five views come from one
  data table in the script (`CHANNELS`), and every chart is generated from its
  series, so a view can never disagree with itself.
- Trusted — the logo marquee runs on the engine and reacts to how fast you
  scroll (speeds up and skews with velocity, settles back). Hovering slows it.
- Section titles — word-by-word masked reveals; eyebrow mark pops, copy follows.
- What you get — cards arrive staggered and each boots its own instrument
  (bars grow, the note stack deals in — and swaps on hover — the curve draws
  with a pulsing endpoint, channel tiles pop from the centre and wave on
  hover, plan rows slide in and the "this week" arrow nudges).
- Selected work — the counters count, cards stagger in, and on desktop the
  three columns travel at slightly different speeds for depth. Hover pans and
  zooms the screenshot.
- How it works — cards still stack natively (CSS sticky), but the dimming is
  now engine-driven; a progress rail fills down the left (≥1300px) and the
  current step's number lights up.
- The app — copy and mock arrive from either side in 3D, then the keyword
  table **re-ranks live** (Flip): positions wobble up and down with an upward
  bias; the featured "boiler installation dartford" keyword holds its #3 so
  the note in "what you get" stays true.
- Final call — questions gather from the centre, the bar arrives, the
  placeholder cycles; clicking a question feeds it into the bar (kept).
- Global — scroll progress bar, lerped cursor spotlight, elastic magnetic
  buttons, the nav underline follows the pointer and rests on Services while
  that section is in view.

**v14.1 — after your notes**

- Hero: the orbit rings and their travelling pulse are gone, and so is the
  arc "horizon" line. In their place a soft red glow drifts on long,
  out-of-phase paths behind the headline (it never visibly repeats), and the
  four stats float free with a slow bob and a little depth against the
  pointer. The console's three dots fade in instead of bouncing.
- Trusted: the label is just "Trusted by"; the panel and border are gone;
  the logos sit in a clean strip sized by height, evenly spaced, fading at
  both edges — still velocity-reactive.
- Selected work: counters on one quiet line; no badge over the screenshot,
  no tag pills, no dark overlay — sector / title / one line / url, with the
  index in the foot; the column offsets are gone so the grid stays aligned.

**Two bugs fixed along the way**

- Your export called `arrow()` in the journal script without defining it, so
  the blog cards threw before they rendered. Defined now.
- `.hero { overflow: hidden }` with a 190vw glow inside makes the hero a
  scroll container — a tap on a control could pan the whole hero sideways.
  Now `overflow: clip`.

## Fail-safe

The page sets `<html class="ydt-js">` just before paint; only then is anything
hidden pre-animation. If GSAP does not load within 3.5s, or the visitor
prefers reduced motion, the class is removed and the page is simply visible —
the console still switches (instantly), the question pills still work, the
marquee falls back to CSS. The four CDN scripts are pinned to GSAP 3.13.0
with integrity hashes: a tampered file fails closed to the visible page.

## Verified

Rendered in Chromium at 1440 and 390 and measured: no horizontal overflow,
nothing left invisible after scrolling (also when arriving via `#contact` or
reloading mid-page), no text under 10px, no off-palette colour, no console
errors; reduced-motion shows everything with no transforms; the no-CDN
fallback shows everything and the channel switch still works.

## Installing

Replace the previous `homepage.html` / `homepage.css` with these. The GSAP
`<script>` tags live inside the page block next to the motion script, so if
you only move the block into your CMS, take those tags with it — and keep the
small gate `<script>` that opens the block, it must run before the page
paints.
