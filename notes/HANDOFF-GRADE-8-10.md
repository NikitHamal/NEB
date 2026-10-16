# Grade 8 and Grade 10 — state of the library

Branch: `resources/grade8-rebuild-grade10-books`. Everything below is built from
the sources in this repo with `notes/pipeline`, and every PDF in `notes/pdf/`
was produced by that pipeline — none is hand-made, so any chapter edit means a
rebuild, never a hand-patch of the PDF.

## What ships

| Book | Units | Pages |
|---|---|---|
| **Grade 8** | | |
| नेपाली | 17 | 155 |
| Mathematics | 21 | 166 |
| Science and Technology | 11 | 119 |
| Compulsory English | 19 | 157 |
| सामाजिक अध्ययन तथा मानव मूल्य शिक्षा | 9 | 94 |
| स्वास्थ्य, शारीरिक तथा सिर्जनात्मक कला | 13 | 90 |
| Question Bank (all six subjects) | 19 | 122 |
| **Grade 10** | | |
| अनिवार्य नेपाली | 17 | 256 |
| Compulsory English | 19 | 281 |
| Mathematics | 16 | 222 |
| Optional Mathematics | 14 | — |
| Science and Technology | 19 | 275 |
| सामाजिक अध्ययन तथा मानव मूल्य शिक्षा | 10 | 126 |
| Accountancy | 15 | 192 |
| Economics | 6 | 97 |
| Question Bank | 19 | 248 |
| Commerce Question Bank | 7 | 86 |

`check.py` passes on every chapter in `notes/content/`.

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

- Grade 9 (the other half of the secondary level) has no sources yet.
- Grade 8 Nepali-medium books could carry more photographs; only a handful of
  `health8/*` assets have been fetched so far.
- The Optional Mathematics and Accountancy books would benefit from the same
  activity-and-project pass the rest of the library has had.
