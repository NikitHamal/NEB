# NEBians — BCA (Tribhuvan University), free and open

<!-- COURSE-STATUS -->
## BCA course: real status

**9 of 42 subjects are written, built and QA-checked; 33 are not started.** Full per-subject table: [`course/STATUS.md`](course/STATUS.md). Done so far (102,864 words of study material):

| Sem | Code | Subject | Words | PDF pages | Status |
|---|---|---|---|---|---|
| 1 | BCA 101 | [Computer Fundamentals and Applications](course/semester-1/computer-fundamentals/) | 16,040 | 53 | done |
| 1 | BCA 102 | [Programming in C](course/semester-1/programming-in-c/) | 15,229 | 56 | done |
| 1 | BCA 103 | [Digital Logic](course/semester-1/digital-logic/) | 9,853 | 29 | done |
| 1 | BCA 104 | [Mathematics I](course/semester-1/mathematics-1/) | 11,443 | 33 | done |
| 1 | BCA 105 | [Professional Communication and Ethics](course/semester-1/professional-communication-ethics/) | 10,381 | 34 | done |
| 1 | BCA 106 | [Hardware Workshop](course/semester-1/hardware-workshop/) | 7,838 | 24 | done |
| 2 | BCA 151 | [Discrete Structure](course/semester-2/discrete-structure/) | 12,728 | 34 | done |
| 2 | BCA 153 | [OOP in Java](course/semester-2/oop-in-java/) | 10,096 | 41 | done |
| 2 | BCA 154 | [Mathematics II](course/semester-2/mathematics-2/) | 9,256 | 23 | done |

Everything else in `course/CURRICULUM.md` is mapped only (no notes). Nothing here has had a subject-teacher review.
<!-- /COURSE-STATUS -->


Everything here is Markdown first (readable on GitHub, diffable, forkable) with a printable PDF next to it.

| Part | Where | What |
|---|---|---|
| **Entrance** | [`entrance/`](entrance/README.md) | 4 books: Mathematics, English, GK and IT, three full model papers. 1,332 keyed MCQs. PDFs in `entrance/pdfs/` |
| **Course** | [`course/`](course/README.md) | The 8-semester BCA programme: the verified curriculum map and the subject books written so far, PDFs in `course/semester-N/pdfs/` |
| Reviews | [`entrance/REVIEW_ENTRANCE.md`](entrance/REVIEW_ENTRANCE.md), [`course/REVIEW_COURSE.md`](course/REVIEW_COURSE.md) | What was audited, found, fixed, and what is still open |
| Sources | [`SOURCES.md`](SOURCES.md) | Where the curriculum and exam facts come from, and how reliable each is |
| Tools | [`tools/`](tools/) | `nebpdf.py` (builds PDFs with the NEBians house pipeline), `qa_pdf.py` (visual/structural PDF QA), `sync_entrance.sh`, `check_c_examples.py` |

## Clone

```
git clone --branch claude/bca-entrance-complete https://github.com/NikitHamal/NEB.git
cd NEB/bca
```

## PDFs are committed, not Git LFS

Total PDF size is a few megabytes (text and vector only, no photographs), well under GitHub's limits, so the PDFs are ordinary committed files. Git LFS was not used; it would make a plain `git clone` return pointer files instead of readable PDFs.

## Rebuild the PDFs — same pipeline as CEE, IOE and Grades 8–12

BCA books are built by the **house pipeline in `notes/pipeline/`** (Markdown → HTML → WeasyPrint, `theme.css`, Poppins / Inter / Source Serif 4 / JetBrains Mono, N watermark, linked contents, roman-numbered front matter, matplotlib maths). `bca/tools/nebpdf.py` is only an adapter: it stages `bca/` sources into the shape the pipeline expects, generates a spine for each course book from its unit files (+ `bca/course/books.json`), and calls the pipeline's own `build()`. An earlier stand-alone builder (own CSS, own fonts) produced PDFs that did not match the house style and was removed.

```
sudo apt-get install -y fontconfig poppler-utils libpango-1.0-0 libpangoft2-1.0-0
bash notes/pipeline/fonts/install.sh                       # the 5 book fonts
python3.12 -m venv v && v/bin/pip install weasyprint markdown matplotlib numpy pymupdf pypdf fonttools pillow
v/bin/python bca/tools/nebpdf.py                           # all books  (or: entrance | course | course/semester-1/digital-logic)
v/bin/python bca/tools/qa_pdf.py --png /tmp/qa             # structural QA + PNG contact sheets to eyeball
```
**Python 3.12 is required** (the pipeline uses 3.12 f-string syntax). Tested with WeasyPrint 70, matplotlib 3.11. `qa_pdf.py` fails on: missing cover/contents/links/outline, missing page numbers, house fonts not embedded, text running into the margin, clipped code lines, leaked TeX or stray `$`, stranded headings; and warns on near-empty pages. `nebpdf.py` exits non-zero if any formula or figure falls back to plain text.

Entrance Markdown is canonical in `notes/content/bca-*` and mirrored here by `tools/sync_entrance.sh`; edit both or edit the canonical copy and re-sync.

## Honest status

See `course/README.md` for exactly which subjects are fully written and which are only mapped. Nothing is marked complete that is not.

## Merge log

| Date (UTC) | What |
|---|---|
| 2026-11-02 | `origin/main` (tip `2193bf3f`) merged into `claude/bca-entrance-complete` as commit `9519f189`. Brought in: the IOE entrance track (`backend_python/web/data/study/ioe-*`, `notes/curriculum/ioe-*`, `notes/HANDOFF-IOE.md`, `notes/sources/entrance/IOE-BE-BArch-entrance-syllabus-2083.pdf`), the house PDF pipeline in `notes/pipeline/` (WeasyPrint + `theme.css`), the CEE/Grade 8–12 books in `notes/pdf/`, the Rust desktop app, and the web/auth fixes. One textual conflict (`ENV.md`, added on both sides) — resolved by keeping both: the BCA/IOE probe first, main's desktop probe verbatim as an appendix. Verified after the merge: 0 files deleted and 0 files modified relative to `origin/main` other than `ENV.md`; all 65 pre-merge `bca/` files present. |
