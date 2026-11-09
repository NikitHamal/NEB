# NEC Civil, Civil &amp; Rural Engineering — License Prep

Static study material for the Nepal Engineering Council (NEC) licence examination, for the
**Civil** and **Civil &amp; Rural** engineering programmes.

Everything here is plain, self-contained HTML — no build step, no dependencies, no server.
Open any page in a browser and it works; all logic (scoring, timers, search, progress) runs
client-side.

## Contents

| File | What it is | Size |
|---|---|---|
| [`notes.html`](notes.html) | Ten chapters of high-yield notes, worked numericals, code references, extra revision panels and a 983-question explanation bank. | ~1.6 MB |
| [`practice-1000-mcq.html`](practice-1000-mcq.html) | 1,000 questions in ten timed sets of 100 — ten per chapter, explanations on demand, mistakes pool, flagging. | ~380 KB |
| [`memory-based-mcq.html`](memory-based-mcq.html) | 600 memory-based questions in six sets, compiled from PANA ACADEMY memory-based NEC papers and NEC model sets. | ~250 KB |

`index.html` is the landing page that links the three.

## Using it

- **Progress** is stored in the browser (localStorage), per device and browser. Safari clears
  browser-held records after 7 days.
- **Permanent records:** open a page and use **Save a copy to my computer** / **Download updated
  HTML**, then keep using the downloaded file. A page served from a website cannot be written
  back to in place — the save buttons produce a copy.
- **Printing:** the notes print chapter by chapter (`Print Notes (A4)`); practice sets print cleanly.

## Sources

PANA ACADEMY memory-based NEC question papers (*Mangsir Shift Memory-Based NEC Question Papers*),
the NEC model sets, and the standard codes and texts cited within each chapter
(IS 456, IS 800, IS 2720, IS 4031/1077, IS 1905, IRC, NBC, NDWQS and Nepal's acts and policies).

This is a **refresher pack**, not a substitute for the codes themselves. Verify anything
critical against the governing code or your own course material.

## Author

Abhishek Gubhaju — Nepal Engineering College, Pokhara University.

## Hosting

Served with GitHub Pages from the repository root. `.nojekyll` is present so files are served
verbatim rather than processed by Jekyll.
