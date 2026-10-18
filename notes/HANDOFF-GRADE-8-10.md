# Grade 8 and Grade 10 — state of the library

Branch: `resources/agent-c-grade8-grade10-final` (continued from `resources/grade8-rebuild-grade10-books`). Everything below is built from
the sources in this repo with `notes/pipeline`, and every PDF in `notes/pdf/`
was produced by that pipeline — none is hand-made, so any chapter edit means a
rebuild, never a hand-patch of the PDF.

## What ships

| Book | Units | Pages |
|---|---|---|
| **Grade 8** | | |
| नेपाली | 17 | 173 |
| Mathematics | 21 | 180 |
| Science and Technology | 11 | 132 |
| Compulsory English | 19 | 172 |
| सामाजिक अध्ययन तथा मानव मूल्य शिक्षा | 9 | **216** (rewritten from the CDC text) |
| स्वास्थ्य, शारीरिक तथा सिर्जनात्मक कला | 13 | **200** (rewritten from the CDC text) |
| Question Bank (all six subjects) | 19 | 135 |
| **Grade 10** | | |
| अनिवार्य नेपाली | 17 | 261 |
| Compulsory English | 18 | 281 |
| Mathematics | 18 | 227 |
| Optional Mathematics | 12 | 186 |
| Science and Technology | 19 | 275 |
| सामाजिक अध्ययन तथा मानव मूल्य शिक्षा | 10 | **297** (rewritten from the CDC text) |
| Accountancy | 15 | 188 |
| Economics | 6 | 96 |
| Question Bank | 19 | 247 |
| Commerce Question Bank | 7 | 86 |

`check.py` passes on every chapter in `notes/content/`. The two sets total
about 3,350 pages (grade 8 ≈ 1,210, grade 10 ≈ 2,140).

## The polish pass (what changed after the first build)

- **Predicted questions.** The grade 8 bank now has the ranked, tiered
  predicted-question chapters the grade 10 bank has — six of them, one per
  subject, each explaining *why* a form ranks where it does. Every objective
  chapter opens with a marks-weightage chart, and every answer carries a
  reason.
- **Diagrams.** `figrun` gained a small shape library — `flow()`, `cycle()`,
  `cards()`, `relation()`, `barh_ranked()` — so a chapter asks for a shape
  instead of hand-placing rectangles. The thin hand-drawn diagrams were
  redrawn with it, and bar charts whose category names collided on the x axis
  became ranked horizontal bars.
- **Summaries.** Several Nepali books name the summary पाठको सार or एकाइको
  सार; the frame regex matched neither, so those summaries printed as bare
  bullets. Fixed, and a summary of short points is now set two to a row.
- **Photographs** that had been parked above the summary are distributed
  through the sections they illustrate, and the Latin source line under each
  photograph is dropped from Nepali books (the credits appendix keeps the full
  attribution, with a Nepali note explaining why those lines stay in their
  original form).
- **Page economy.** Headings stay with their text, long tables repeat their
  header, rows do not split, and a long summary flows instead of pushing a
  gap to the next page.
- **Maths and figures.** Inline maths is set at body size and cropped tight;
  display maths is larger; charts are drawn on a larger canvas at the same
  type size. Four display equations that no longer fitted the column were
  split at an `=`.
- **Practice numbering.** Markdown restarts an ordered list at 1, so the extra
  practice questions were numbered 1, 2, 3 against answer keys numbered 4, 5,
  6. They are bold-numbered paragraphs now and keep their numbers.

## The rules that shaped this work

1. **Nepali-medium books are Nepali all the way through.** `nep*`, `soc*` and
   `health*` are published and examined in Nepali, so their furniture is Nepali
   too: cover, running heads, section labels, figure captions, axis labels,
   marks chips and numerals (`i18n.NEPALI_MEDIUM` drives this). The only Latin
   left is in the picture-credit appendix, where each licence requires the file
   title, author and licence code to travel unchanged — a Nepali line on that
   page now says so.
2. **Devanagari needs real shaping.** Three bugs were found by rendering pages
   and looking at them, not by reading code: `letter-spacing` shattered
   conjuncts, Poppins' secondary Devanagari was being used for display type,
   and the `@page` margin boxes fell back to a Latin font. All three are fixed
   in `build_pdf.py`.
3. **A formula written in Nepali words is text, not maths.** matplotlib's
   mathtext places glyphs one at a time and its maths fonts have no Devanagari,
   so `\text{जनघनत्व}` used to print as dummy boxes. `devaeqn.py` now typesets
   any Devanagari-bearing formula as HTML in the book's own font, with stacked
   fractions; `md2html.py` routes to it automatically.
4. **Photographs are embedded as JPEG.** `photo.py` used to composite to
   lossless PNG at 250 dpi, which took Science 10 to 50 MB. It now writes JPEG
   q84 and the source assets are capped at 1200 px: same pages, same quality on
   the page, 10.7 MB.
5. **Every chapter earns its pages.** The grade 8 and grade 10 books were taken
   to the grade 11/12 standard: a data or concept chart in every unit, a
   comparison table, at least one fully worked example, activity and project
   boxes for interactive learning, and an extra practice set with answer keys.

## The second content pass (grade 8)

Every grade 8 book now carries, in each chapter, the things the grade 11/12
books have: a teaching section the first draft lacked, a table, a diagram
drawn with the shape library, at least one fully worked answer, and an
**objective practice set with a reasoned key** — Group A of the Basic Level
paper is ten objective items, and the first draft trained none of them.

- **नेपाली** — a पाठको विश्लेषण table for every lesson (genre, setting,
  characters or imagery, style, message), a structure diagram where it helps,
  and five objective items per lesson. 155 → 173 pp.
- **सामाजिक अध्ययन** — culture and change, values online, elections and
  participation, substance abuse, historical sources, value chains, climate
  zones and hazards, census and vital registration, digital citizenship.
  94 → 107 pp.
- **Science** — measurement and error, a four-step routine for motion
  numericals, the household electricity bill, microscope work and biological
  drawing, energy arithmetic, distances and earthquake preparedness.
  117 → 125 pp.
- **स्वास्थ्य/शारीरिक/कला** — system interdependence, malnutrition,
  vaccination, school health, rest and routine, athletics technique, design
  principles, pranayama, reuse, rhythm. 86 → 105 pp.
- **Mathematics** — Venn method, choosing the mensuration formula, reasons as
  marks in geometry, choosing the right average, plus objective sets.
  166 → 176 pp.
- **English** — reading for purpose, writing from data, instructions,
  narrative shape, persuasion, the anecdote, plus objective sets.
  157 → 162 pp.

### Objective practice is now complete

Group A of the Basic Level paper is ten one-mark items, and the first draft
trained none of them inside the chapters. **Every unit of all six grade 8
books now ends with a five-item objective set whose key gives a reason for
each answer** — 90 units, 450 items. The sets were written against the facts
line of each chapter, so they double as a last-night revision pass.

### Where grade 8 now stands against grade 10

Grade 8 averages about **12 pages a chapter**, grade 10 about 13 — the
remaining difference is subject weight, not neglect. Every unit of every
grade 8 book carries: the syllabus bullets as numbered sections, a data or
concept table, at least one diagram from the shape library, one or more fully
worked answers, activity or project boxes, an extra practice set with answers,
and a five-item objective set with a reasoned key.

## Pipeline notes for the next session

- Build from a scratch tree shaped `nebians/{content,curriculum,build,pdf}`;
  `/workspace/tools/runbuild.sh` syncs the repo into it, builds a queue and
  copies the PDFs back. Launch it as `(setsid runbuild.sh soc10 nep8 &)`.
- Repo I/O goes through the GitHub REST API (`tools/ghapi.py`, `tools/push.py`,
  `tools/rmpath.py`); there is no git credential in the sandbox and
  `actl connector call --body` cannot carry a large payload.
- A single request body over ~50 MB is rejected, so push large PDFs one at a
  time.
- `assets.py get_commons <id> "<File:…>"` fetches and registers a Commons image
  with its credit line; `assets.py verify` checks that every registered id has
  bytes on disk.
- mathtext gotchas: braces always (`\sqrt{3}`), no `\begin{align}`, no
  `\ce{}`, and a command butted against a digit (`\ge1`) needs a space —
  `mathsvg.py` inserts it now.

## What a future session could do next

- **Grade 9** has no sources at all. It is the real hole in the secondary
  series: grade 10 assumes a grade 9 the library does not have.
- The **Optional Mathematics, Accountancy and Economics** books have not had
  the activity-and-project pass the rest of the library has had, and carry no
  objective sets.
- Grade 8 Nepali-medium books could carry more photographs; only a handful of
  `health8/*` assets have been fetched so far, and `soc8` borrows from
  `soc10/*`.
- The grade 10 question banks could use the weightage charts that the grade 8
  bank now opens each objective chapter with.

## Session of 2026-10-17 (agent C, final branch) — rewrite from the CDC textbooks

The owner judged the grade 8 first drafts "very poor" and asked for them to be
recreated. This session rewrote the thin Nepali-medium books **lesson by lesson
from the official CDC textbooks**, to the standard of `soc8/unit-07.md`:
every textbook lesson is a section, every textbook table is reproduced with its
numbers checked (errors fixed and flagged in a `::: caution`), every activity and
project appears, **every textbook अभ्यास question has a full model answer**
(`### पाठको अभ्यास: नमुना उत्तर`), then a summary and a graded practice set
with reasoned keys. Zero Latin script in any Nepali book (prose, tables and
figure labels — the figure check is a separate scan, see below).

| Book | Source | Result |
|---|---|---|
| सामाजिक ८ units 1–9 | CDC 2082, `moecdc.gov.np/content/584` (Preeti text layer) | 9 units, ~65k words, 216 pp |
| स्वास्थ्य, शारीरिक तथा सिर्जनात्मक कला ८ units 1–13 | CDC 2080, `/content/68` — **scanned**, OCR'd with `tesseract -l nep` at 200 dpi | 13 units, ~60k words, 200 pp |
| सामाजिक अध्ययन १० units 1–10 (SEE) | CDC 2082, `/content/591` | 10 units, ~106k words, 297 pp; SEE set क[1]/ख[2]/ग[4]/घ[8] |

Corrections made to the textbooks are listed in `notes/rewrite-logs/` and in
the caution boxes themselves (e.g. census 2078 sex split 48.87/51.13, doubling time 76 years,
BMI example, Stockholm 1972, first UN veto 1946).

### Pipeline fixes found by looking at pages

- **`- १.` bullets printed as `• 1.`** — Python-Markdown's list regex uses `\d`,
  which matches Devanagari digits, so every Nepali-numbered bullet became a
  nested `<ol>` restarting at a Latin "1.". `md2html.py` now escapes the dot
  and marks such items `li.num` (no bullet); plain ordered lists in Nepali
  books count in Devanagari (`html:lang(ne) ol:not([class])`).
- **Photos silently missing** — 14 entries in `assets/credits.json` pointed at
  `.jpg` files while the bytes on disk are `.png` (Science 10 heart, eye,
  nephron, neuron, skeleton, reproductive system; Science 8 onion root;
  Accountancy ledger; Nepali portraits). Repointed; those books were rebuilt.
- Stale English-named duplicates of the Social Studies 8 and 10 PDFs removed.

### Rebuilt and pushed this session
soc8, health8, soc10, nep8, nep10, sci8, sci10, acc10.

### Still open
- Grade 8 question bank (`qbank8`) predates the soc8/health8 rewrite; its
  social and health chapters could be re-derived from the new books.
- Grade 8 नेपाली (2.8k words/lesson), Mathematics, Science and English were
  not rewritten this session; the same CDC-text method applies (textbooks:
  नेपाली `/content/583`, English `/582`, Science `/72`, Maths `/73`).
- Grade 9 still has no books.

### Launch film
A new 18-second mascot film, **Neby**, lives in `tools/video/neby/`
(Skia + numpy, no browser). Master: `tools/video/dist/nebians-neby-launch-16x9.mp4`.
See `tools/video/neby/README.md`.
