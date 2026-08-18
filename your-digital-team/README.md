# Your Digital Team — homepage

`homepage.html` is a standalone, previewable page. Open it in a browser to
see the whole thing; the Squarespace-injectable block is delimited inside
the file by:

```
▼▼▼ SQUARESPACE CODE BLOCK STARTS HERE ▼▼▼
...
▲▲▲ SQUARESPACE CODE BLOCK ENDS HERE ▲▲▲
```

Copy everything between those two markers into your code block. Everything
is scoped under `.ydt-page` / `.ydt-projects-standalone`, so it will not
leak into the surrounding Squarespace theme.

## Before you publish — values I could not verify

These are placeholders I wrote to fill the new sections. Replace or delete
them; do not ship them as-is.

| Where | Value | Note |
|---|---|---|
| Hero proof band | `+312%` | Taken from your own method copy ("that's how +312% happens"). Confirm it's attributable and current. |
| Hero proof band | `9` brands | Counted from the client list in the ticker. |
| Hero proof band | `7` days to first report | I invented this. Your method copy says week 1–2 for the audit. |
| Hero proof band | `1` page plan | From your method copy ("One page"). |
| Closing CTA | `hello@yourdigitalteam.co.uk` | **Invented address.** Swap in your real inbox. |
| CTA / hero links | `/contact` | Confirm this route exists. |
| Services grid | `/seo` | Card 01 previously had no link; I pointed it at `/seo`. |

## Design direction

Exaggerated Minimalism — oversized type, extreme negative space, near-black
+ warm off-white, and a single accent (`--accent: #C9F24D`). Section order
follows a Trust & Authority + Conversion structure: hero → proof → offer →
work → services → method → close.

The accent is never used as text on a light surface (it fails AA there) —
only as a fill behind black text, or as text on the near-black surfaces.

## Verified

Checked in headless Chromium at 360/375/390/768/1024/1280/1440/1920 wide:

- no horizontal overflow at any width
- all text meets WCAG AA contrast, including every flooded hover state
  across all 11 accent colours
- no interactive target under 44px
- keyboard reaches every card, and focusing a project card reveals the same
  detail panel a mouse hover does
- reduced-motion renders the whole page in its final readable state
- no JS errors; both image fallbacks (client logos, project art) work
