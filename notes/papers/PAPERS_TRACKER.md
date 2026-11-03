# Past Papers Pipeline — tracker (read this first in a new session)

Task: rebuild every NEB board paper (all years, all variants) for every class that has a note book in `notes/content`,
as NEBians-branded PDFs with full solutions, so the Library's "Past Paper" filter has real resources. Start from Class 12.
Papers are re-typeset from the published exam; question wording and marks are kept, the layout, watermark and solutions are ours.
No third-party name, watermark or mark appears in any output PDF.

Branch: `resources/past-papers-class12` (from `main`). Push after every paper.

## Layout
```
notes/papers/
  content/<id>.md        one paper: front matter + question paper + <!-- SOLUTIONS --> + solutions
  build_paper.py         content -> pdf/<file>.pdf, and manifest.json (python3 build_paper.py --all)
  paper.css              exam layout (extends pipeline/theme.css, NEBians watermark + Poppins/Source Serif)
  pdf/                   built PDFs (committed)
  manifest.json          one record per PDF: subject, grade, year_bs/ad, stream, code, pages, bytes, category "Board Exam"
  tools/fetch.py         scratch fetcher: draft OCR text + page images into /tmp/psrc (never committed)
```
Id convention: `<grade>-<subject>-<yearBS>-<variant>` e.g. `12-phy-2082-general`.
PDF name: `NEBians-Past-Paper-Grade-12-<Subject>-<yearBS>-<Variant>.pdf`.

## Paper source format
Front matter keys: file, subject, grade, year_bs, year_ad, stream, code, time, marks, students, category.
Question part (before `<!-- SOLUTIONS -->`):
- `## Group 'A'` headings, `<small>..</small>` one-line group rule.
- `@mcq N` then stem line(s), then `@opts a | b | c | d` (or `@opts-col` for long options, stacked).
- `@q N` then parts `(a) ... [[2]]`, sub-parts `(i) ...`; `@or` between alternative sets. `[[n]]` = marks chip.
- Math `$...$` (matplotlib mathtext, see notes/AUTHORING.md section 4). Figures: ```figure caption="..." matplotlib blocks (palette INK/ACCENT/GRID in scope).
Solutions part: `@s N` starts "Question N"; markdown, `$$..$$` display math, tables for the MCQ key.

## Method for each paper (do not skip the checks)
1. `python3 notes/papers/tools/fetch.py <page-url> <cache-key>`; the page text is OCR and is truncated ("Contd... See more") and wrong on exponents/symbols.
2. Open every page image (`read_file` on `/tmp/psrc/<key>/pN.jpg`; symlink `/tmp/psrc` into the file-tool root) and transcribe from the image, never from OCR alone.
3. Re-derive every numerical answer; write full solutions. MCQs get an answer key with a one-line reason.
4. Build, render pages to PNG (pymupdf), look at them. Then commit + push, update the table below.

## Environment notes
- File tool root here was `/home/user/sandbox` (not `/app`); bash sees everything. `ln -sfn /tmp/NEB /home/user/sandbox/neb`, `ln -sfn /tmp/psrc /home/user/sandbox/psrc`. File-tool paths must be relative.
- Git auth: `/tmp/gitenv.sh` (GIT_ASKPASS) echoing `$GH_PAT`; the token is never written to the repo.
- Python 3.11: needs `pip install --user --break-system-packages weasyprint markdown matplotlib numpy pymupdf pillow requests`, `sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 fontconfig`, and `bash notes/pipeline/fonts/install.sh` then `fc-cache -f ~/.local/share/fonts/nebians`.
- `notes/pipeline/md2html.py` had one 3.12-only f-string; patched for 3.11.

## Scope and status
Years: 2080, 2081, 2082 BS (new course) per variant. Science-stream core first (matches note books phy12, chem12, bio12, math12, cs12, eng12, nep12), then the rest of Grade 12, then Grade 11 school-level papers where a board paper exists, then SEE (Grade 10) and Grade 8 where a board/provincial paper exists.
Variants per year: General stream (regular + partial), Technical stream, partial-student English, Optional papers, and every set/province variant a year has. Group A MCQs are published as a separate sheet; we merge them in as Group A.

| Grade | Subject | Year | Variant | Status |
|---|---|---|---|---|
| 12 | Physics | 2082 | General | DONE (11 pp, MCQ key + all solutions) |
| 12 | Chemistry | 2082 | General | sources fetched, not authored |
| 12 | Biology | 2082 | General | sources fetched, not authored |
| 12 | Mathematics | 2082 | General | sources fetched, not authored |
| 12 | Computer Science | 2082 | General | sources fetched, not authored |
| 12 | Compulsory English | 2082 | Regular / Partial | queued |
| 12 | Compulsory Nepali | 2082 | Regular | queued |
| 12 | Physics, Chemistry, Biology, Mathematics, CS, English, Nepali | 2081, 2080 | General | queued |
| 12 | Physics, Chemistry, Biology, Mathematics | 2082, 2081, 2080 | Technical | queued |
| 12 | Management / Humanities / Education / Law | 2082-2080 | all | queued |
| 11 | all science subjects | | | queued (no national board paper before 2082; check) |
| 10, 8 | all | | | queued |

Source index for Grade 12 2082: the aggregator's per-subject pages follow `<Subject>-<Stream>-Question-Paper-2082-2025-of-Class-12-NEB.html`
under `www.dhanraj.com.np/2026/03/` (2081/2080 papers are linked from the same pages). Internal use only: never cite it in a PDF.

## Library registration
`manifest.json` is the import list. Each record is a `Resource` of type `Past Paper`, exam type `Board`, class `12`, subject, year; the
library filter on `/app/past-papers/` (`default_type="Past Paper"`) lists them once uploaded. Uploading to the live site needs the admin; nothing here does that.

## Integrity notes
- Every paper must be checked against its page images before it is marked DONE; the answer keys are ours and must be re-derived.
- Where the printed figure cannot be read with certainty the solution states its assumption (e.g. Physics 2082 Q20c: two nodes read as the second harmonic).
