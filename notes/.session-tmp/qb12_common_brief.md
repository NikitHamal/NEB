# COMMON BRIEF — NEBians "Question Bank, Grade 12" chapters

You are writing ONE chapter of a printed NEB Grade 12 question-bank book (free PDF
study material, nebians.consica.com.np). Grade 12 is the board exam that decides
university admission. This book is pure exam practice: past questions, important
questions and predicted questions, ALL fully solved.

## STEP 0 — read these before writing a single line

1. `/data/workspace/NEB/notes/AUTHORING.md` — the binding contract, ALL 14
   sections. Read it fully, do not skim. §4 (mathtext, NOT LaTeX), §7 (practice
   question formatting), §10 (matrices/determinants MUST be figures via `mateq`),
   §12 (figure visual QA), §13 (derivations), §14 (real photos).
2. `/data/workspace/NEB/notes/curriculum/qbank12.md` — the spine for THIS book.
   It is law: `title` verbatim, `area` from the `# PART:` line.
3. The subject syllabus spine you are banking (`bio12.md` or `math12.md`) —
   your bank must be organised unit by unit and cover EVERY unit.
4. The recently written chapter in that subject's own book
   (`content/math12/unit-09.md` or `content/bio12/unit-02.md`) so your notation,
   symbols and terminology match what a student reads alongside this book.
5. Your research brief: `/tmp/qb12_bio_research.md` or
   `/tmp/qb12_math_research.md`. These contain **verbatim transcriptions of the
   real NEB papers 2079, 2080, 2081, 2082 and the CDC model questions**, obtained
   from scans. They are your source of truth for year tags and for the exam
   pattern. READ YOUR SUBJECT'S BRIEF IN FULL.

## Frontmatter — exactly this shape

```
---
subject: Question Bank
grade: 12
unit: <N>
title: <verbatim from qbank12.md, including the "Subject: " prefix>
hours: 0
area: <Biology or Mathematics — the # PART: line above your unit>
---
```

`hours: 0` because the qbank12 spine tags every unit `[R]` (revision, no hours).
Do not quote the title; the parser splits on the first colon only, so a title
containing a colon is fine. Do NOT reword the title.

## Year tags — the honesty rule, this is non-negotiable

Tag a question `(NEB 2080)` **only** when that question genuinely appears in the
verbatim transcription in your research brief for that year. The brief marks each
paper HIGH CONFIDENCE (scan-verified) or MEDIUM. Only tag from HIGH CONFIDENCE
material, and tag the year the brief gives.

- An unverified question carries **no tag at all**. Keep the question, drop the tag.
- Never invent a year. Never tag a question you wrote yourself.
- Where a question is close to but not identical with a real one, either quote the
  real one and tag it, or write your own and leave it untagged. Do not tag a
  paraphrase as if it were the paper's wording.
- You may write `(NEB 2080, 2081)` when the brief documents the same question in
  both years — the brief has a "cross-year repetition" list for exactly this.

## Formatting rules that break the build if you get them wrong

- Math is matplotlib **mathtext**, not LaTeX. No `\begin{align}`, no `\mathbf`,
  no `\ce{}`, no `pmatrix`/`bmatrix`/`vmatrix`, no `\overset`, no `\xrightarrow`,
  no `\substack`, no `\lvert`/`\rvert` (use plain `|`).
- Write `\approx`, never `\\approx`.
- Inline math `$...$` must pair. `check.py` reports `UNPAIRED $` and fails.
  Beware of a bare `$` in prose. Inline math may wrap across up to 4 source
  lines but must not cross a blank line or a block boundary.
- **Display equations that are too wide fail the check.** Split them at an `=`
  into two `$$…$$` blocks. Keep display math short.
- Matrices and determinants: **never typeset them.** Draw them as a figure using
  `mateq([...])` — see AUTHORING §10. `("det", [[...],[...]])` gives a
  determinant with vertical bars.
- Chemical/biological equations are plain text with Unicode
  (`6CO₂ + 12H₂O → C₆H₁₂O₆ + 6O₂ + 6H₂O`), never math mode.
- Inside ```figure code, matplotlib text is NOT rewritten: `\ge`, `\le`, `\ne`,
  `\to` will crash `savefig`. Use Unicode (≥ ≤ ≠ →) in figure labels.
- `np.trapz` is gone; use `np.trapezoid`.
- MCQ options go on ONE line right after the question — the build splits them
  into an option grid itself. Never hand-build a table or list of options:

```
1. The degree of the differential equation … is <span class="marks">[1]</span>
   (a) 1 (b) 2 (c) 3 (d) 4
```

- Answer keys: a `::: note` box with `**1.** …` on consecutive lines; the build
  gives each its own line.
- Number each question group from **1** again, and reference answers by that
  number.
- Marks always as `<span class="marks">[N]</span>`.

## Callout boxes available

`key`, `definition`, `derivation`, `example`, `caution`, `tip`, `note`, `memory`.
Syntax:

```
::: tip Title here
Body markdown.
:::
```

## Figures — the owner specifically praised the drawn Maths figures

Use ```figure blocks wherever a question needs one: curves and the area under
them, conic sections, vector diagrams, direction fields, cell-division stages,
genetic crosses, the Calvin cycle, ECG traces, the nephron. Rules:

- Code runs at build time, must leave a `Figure` in a variable named `fig`.
  Never call `plt.show()` or `savefig`.
- Already in scope: `plt`, `np`, `matplotlib`, `INK`, `MUTED`, `GRID`, `ACCENT`,
  `SERIES` (6-colour list), `mateq`, `matrix`. Use the palette, not defaults.
- `figsize` width 4.0–5.2 in, height 2.2–3.4 in (diagrams up to 4.6 in tall).
- `ax.spines[['top','right']].set_visible(False)`, light grid, no chartjunk.
- Caption is auto-numbered — do not write "Figure 3." yourself.
- Every figure must carry information the text cannot. No decoration.

## THE QA GATE — you are not done until all of this passes

```
cd /data/workspace/NEB/notes/pipeline
python3 check.py ../content/qbank12/unit-NN.md     # must print OK
python3 preview.py ../content/qbank12/unit-NN.md /tmp/qb12bm
```

- `check.py` must print `OK`. Fix every failure and re-run until clean.
- Render EVERY drawn figure with `preview.py` and **Read each PNG** with the Read
  tool, checking it against AUTHORING §12: no text overlapping text/arrows/lines/
  shaded regions, nothing clipped, no arrow starting or ending inside a label,
  no legend over data, labels moved to clear space rather than boxed over busy
  areas. Fix and re-render until each one is clean. A figure that renders is not
  a figure that is done.
- If you use ```photo blocks, run
  `python3 photoprev.py ../content/qbank12/unit-NN.md /tmp/qb12bm` and Read every
  photo PNG too. Overlay coordinates are guesses until you have looked.

## Scope

Touch ONLY your own file under `/data/workspace/NEB/notes/content/qbank12/` and
`/data/workspace/NEB/notes/assets/` (via `assets.py`). Do not touch any other
file. Do not git commit. Do not create report/summary .md files.

## Accuracy

- **Mathematics: recompute every answer yourself with python3/sympy before you
  write it.** A wrong answer key is worse than no key. Run the numbers.
- **Biology: verify every binomial name, every ratio, every count.** Italicise
  binomials (`*Drosophila melanogaster*`). Use CDC/NEB terminology.
- Write plainly for a 16–18 year old who may be reading in a second language.
  Short sentences. Define jargon at first use. Do not pad.

## Your final report back

Report: file path, title, word count, question counts, number of figures, number
of photos, the exact `check.py` output line, which figures you rendered and
inspected, and anything you could not verify.
