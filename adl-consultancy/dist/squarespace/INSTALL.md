# Putting this on Squarespace 7.1

Do these in order. Steps 1–3 are done once for the whole site; step 4 is per page.

You need a **Core plan or above** — JavaScript in code blocks and Code Injection
are premium features. The dropdown, mobile menu, standards tabs and video
lightbox all need JavaScript.

---

## 1. The stylesheet

**Settings ▸ Advanced ▸ Code Injection ▸ HEADER**

Paste the whole of `1-code-injection-HEADER.html`, `<style>` tags included.

That field writes into `<head>`, which is where a stylesheet belongs. Do not put
any visible markup in it — markup in `<head>` does not render.

## 2. The header, footer, icons and scripts

**Settings ▸ Advanced ▸ Code Injection ▸ FOOTER**

Paste the whole of `2-code-injection-FOOTER.html`.

That field writes just before `</body>`, which is the only place a site-wide
custom header and footer can live. Step 3 pins the header to the top.

The icon sprite is in this file too. **Without it every icon on the site renders
blank** — there are over 300 references to it.

## 3. Hide Squarespace's header and footer

**Design ▸ Custom CSS**

Paste the whole of `3-custom-css.css`.

This hides Squarespace's own header and footer (ours replaces both), pins our
header, and opens the Fluid Engine grid so full-bleed sections reach the screen
edge.

## 4. Each page

18 pages, one file each, in `pages/`.

For each one:

1. Create the page in Squarespace.
2. Add a section, then add a **Code Block** to it.
3. Paste the matching file from `pages/` into the code block.
4. **Set the section's ID to `adl-section`** — Edit section ▸ ⋯ ▸ Section ID.
   Without this the section keeps Squarespace's gutter and nothing goes
   edge to edge.
5. Stretch the code block to the full width of the grid (drag its handles, or
   press `G` to show the grid).

## 5. Upload the images

All 31 are in `dist/assets/img/`. Upload them, then find and replace
`/assets/img/` in the pasted pages with whatever URL Squarespace gives them.
Until you do, every image on the site is a broken icon.

---

## Things that will bite you

- **Don't paste any `<script>` into a page code block.** A script inside a Fluid
  Engine code block makes the block taller than its content and leaves a gap.
  All the JavaScript is already in step 2.
- **Fluid Engine writes its layout as inline styles**, and an inline style can
  only be beaten by `!important`. That is why the Custom CSS uses it. Keep the
  `#adl-section` scoping so the rest of the site is unaffected.
- **Upgrading a section to Fluid Engine cannot be undone**, and it changes the
  section's id. If a section stops going edge to edge after an edit, re-check
  its Section ID first.
- **The links between pages still use the old WordPress URLs** and will 404.
  Once the pages exist in Squarespace, send us the new URLs and we will remap
  them, or find and replace them yourself in the pasted markup.

## Checking it worked

On a phone, or a narrow browser window:

- The header shows the logo, a blue phone button and a hamburger.
- Tapping the phone button starts a call — this is the main thing people do.
- Opening the menu shows the standards with their code chips, and **both** the
  "Contact us" and "01279 293007" buttons are visible at the bottom without
  scrolling.
- Nothing scrolls sideways on any page.
- Icons are visible, not blank. If they are all blank, step 2 did not save.
