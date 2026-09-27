# NEBians Study Notes — Session Handoff (for Claude Code on AgentSky)

Date: 2026-09-27. Branch: `resources/neb-notes-11-12` (from `main` @ `a0f5c55`).
Goal: complete chapter-by-chapter study books (PDF) for NEB/CDC Grade 11 & 12
Science stream, plus English (compulsory) and Nepali, built from Markdown
sources in this repo and uploaded to the NEBians library.

## Where things live

- `notes/content/<subj><grade>/unit-NN.md` — chapter sources. Frontmatter:
  `subject, grade, unit, title, hours, area`. Body uses the pipeline's
  Markdown dialect: `::: key/definition/example/caution/tip/memory/note`,
  `## N.N` sections, `**Group A/B/C**` practice + answer keys, and
  ` ```figure caption="..." ` blocks containing real matplotlib code
  (globals provided: `INK, MUTED, GRID, ACCENT, SERIES, np, plt`).
- `notes/pipeline/` — `build_pdf.py` (books via WeasyPrint), `check.py`
  (renders every math expr + figure; must print OK), `preview.py`,
  `md2html.py`, `mathsvg.py`, `figrun.py`, `patchfig.py`, `spine.py`
  (subject roster + `ALL`), `theme.css`, `brand/` (N watermark SVGs),
  `fonts/` (README + install.sh only — fonts are NOT vendored).
- `notes/curriculum/*.md` — per-subject syllabus spines (unit order lives here).
- `notes/pdf/` — built books, committed. Regenerate with the pipeline whenever
  chapters change; never hand-edit a PDF.
- `notes/AUTHORING.md` — the authoring contract (§1–13). Read it fully before
  writing any chapter.

## Build / verify (canonical)

```bash
cd notes/pipeline
python3 check.py ../content/<subj>/unit-NN.md        # must end OK
python3 build_pdf.py <subj><grade>...                # e.g. build_pdf.py phy12
# or all: build_pdf.py phy11 phy12 chem11 chem12 bio11 bio12 math11 math12 cs11 cs12 eng11 eng12 nep11 nep12
```

IMPORTANT layout quirk: `build_pdf.py` resolves the theme as
`<parent-of-pipeline>/build/theme.css`. It runs from a working tree shaped
`nebians/{content,curriculum,build,pdf}` (pipeline files live in `build/`).
To build from this repo, copy `notes/content`, `notes/curriculum` and
`notes/pipeline/*` into a scratch tree as `nebians/{content,curriculum,build}`
and run there; copy resulting PDFs back to `notes/pdf/`. There is a mirror
script pattern for this (`cp -r` content/curriculum, copy pipeline files).

Environment that is PROVEN to build clean: Python 3.12, matplotlib **3.11.2**,
numpy 2.x, reportlab + pypdf, WeasyPrint 70 + Pango/Cairo system libs, and the
5 book fonts (Poppins ×4 weights, Inter, Source Serif 4, Noto Sans Devanagari,
JetBrains Mono — see `pipeline/fonts/install.sh`). `check.py` math validation
is matplotlib-version-sensitive (see Gotchas).

## Coverage right now (units on disk / curriculum total)

| Subject | G11 | G12 |
|---|---|---|
| Physics | 26/26 | 25/25 |
| Chemistry | 17/17 | 21/21 |
| Biology | 8 units | 7 units |
| Mathematics | 21/21 | 16/17 (unit-09 Product of Vectors missing) |
| CS | 4/8 | 7/7 |
| English | 23/35 (units 01–13, 21–30; 14–20 missing) | 0 (not started) |
| Nepali | 13/27 (units 13–25; 01–12 missing) | 0 (not started) |

Built PDFs in `notes/pdf/` (12): all subjects above except eng12/nep12.
`build_pdf.py` prints `chapters=X/Y` per book — partial subjects build fine.

## Gotchas (learned the hard way — do not regress)

1. **Inline `$...$` must never hard-wrap across source lines.** A wrap splits
   delimiters across lines and raw LaTeX reaches the PDF. `check.py` reports
   `UNPAIRED $` and fails the file. Keep each inline formula on one line
   (may span up to ~4 physical lines only via the pipeline's own rules).
2. **`\\command` (double backslash + letters) prints the bare word.** Always
   single backslash for commands; `\\` is a line break only at end of line.
3. **Braced args everywhere the parser needs them**: `\sqrt{3}` not `\sqrt3`,
   `\frac{1}{2}` not `\frac12` (mathsvg fixes `\frac<digit><digit>` only).
   matplotlib 3.10 REJECTS braceless `\sqrt`; 3.11.2 accepts — always write
   the braced form so every environment passes.
4. **matplotlib mathtext has no `\underline`.** Restate without it.
5. **Figure blocks**: one ` ```figure caption="..." ` fence per block, fence
   on its own line. `check.py` renders every figure (`figrun`) — inspect
   each as PNG via `preview.py`, never judge from code alone.
6. **MCQ option runs** `(a) … (b) … (c) … (d) …` become an option grid;
   multi-part questions become stacked parts (pipeline handles layout —
   keep authoring them inline).
7. **Answer keys get one line per answer.** `## Chapter summary` goes in a
   highlighted panel (pipeline).
8. Devanagari (Nepali) content needs Noto Sans Devanagari installed or figures
   silently fall back and `check.py`/`preview.py` print findfont warnings.
9. Branding: site URL is `nebians.consica.com.np`; NEBians N mark is a
   low-opacity page watermark (`pipeline/brand/`).

## Last session state (2026-09-26, Claude Opus 5)

Committed: `1d78b2c` (source+pipeline+spines, 151 files) then `c0846b7`
("fix issue #48 — math rendering, MCQ layout, figures, branding", 63 files:
inline-math wrap fix, UNPAIRED-$ check, `\\command` repair, MCQ grid, answer
keys, chapter-summary panel, URL + watermark branding). Local head
`6a54d59f` is the same content. Uncommitted follow-ups after that (already in
this tree): cs11 units 03–04, eng11 units 01–13 + 21–30, math11 18/21,
math12 13/14, nep11 13–25, bio11 unit-04, chem12 unit-09.

## What "continue the job" means

1. Write the missing units (table above), each passing `check.py` with zero
   math/figure failures and every figure PNG-inspected.
2. Rebuild affected books, verify page counts grow, commit sources + PDFs.
3. Keep issue #48's review standard: teacher/student-facing accuracy first,
   NEB exam pattern (Group A 11×1, B 8×5, C 3×8 for model questions).
