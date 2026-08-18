# Client logos

The "Trusted by" marquee on the home page loads its artwork from this folder.

## Adding a logo

1. Drop the file in here using the exact name below.
2. That's it — the marquee picks it up. Until the file exists, the client's
   name shows as a text wordmark instead, so the row never looks broken.

| Client                | File                       |
| --------------------- | -------------------------- |
| Senttr                | `senttr.svg`               |
| Fitzgerald Capital    | `fitzgerald-capital.svg`   |
| SVD                   | `svd.svg`                  |
| Punt Caravan Parking  | `punt-caravan-parking.svg` |
| PilotQ                | `pilotq.svg`               |
| Gutters.co.uk         | `gutters-co-uk.svg`        |
| 911 Backdate          | `911-backdate.svg`         |
| Heating               | `heating.svg`              |

To add, remove or reorder clients, edit the `clients` array in `index.html`
(search for `CLIENT LOGO MARQUEE`). One line per client.

## What the files should be

- **SVG preferred.** It stays sharp at any size and weighs almost nothing.
  PNG works too — change the extension in the `clients` array to match. Use a
  transparent background and roughly 4x the display height (so ~150px tall).
- **Colour does not matter.** Every logo is flattened to a single white
  silhouette with `filter: brightness(0) invert(1)`, so the black wordmarks,
  the red Heating mark and the near-white SVD monogram all read identically
  against the black background. This is deliberate — a row of logos in their
  own clashing brand colours is the thing that makes a client strip look
  cheap.
- **Trim the whitespace** around the mark before exporting. Built-in padding
  makes one logo look smaller than its neighbours.
- **Wide lockups** are capped at 190px so a long horizontal logo cannot
  dominate the row.

## Note

The red "HEATING" logo was supplied cropped — the company name above the word
"HEATING" was cut off. It is listed as "Heating" for now; rename it in the
`clients` array once the full name is known.
