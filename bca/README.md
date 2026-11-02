# NEBians — BCA (Tribhuvan University), free and open

<!-- COURSE-STATUS -->
## BCA course: real status

**28 of 44 subject slots are written, built and QA-checked; 8 core subjects are not started; 8 slots are projects, internship or electives with no notes planned.** Full per-subject table: [`STATUS.md`](STATUS.md). Done so far (423,766 raw words of study material, counted over the unit files, including code listings and tables):

| Sem | Code | Subject | Words | PDF pages | Status |
|---|---|---|---|---|---|
| 1 | BCA 101 | [Computer Fundamentals and Applications](course/semester-1/computer-fundamentals/) | 16,040 | 53 | done |
| 1 | BCA 102 | [Programming in C](course/semester-1/programming-in-c/) | 15,229 | 56 | done |
| 1 | BCA 103 | [Digital Logic](course/semester-1/digital-logic/) | 9,853 | 29 | done |
| 1 | BCA 104 | [Mathematics I](course/semester-1/mathematics-1/) | 11,443 | 33 | done |
| 1 | BCA 105 | [Professional Communication and Ethics](course/semester-1/professional-communication-ethics/) | 10,381 | 34 | done |
| 1 | BCA 106 | [Hardware Workshop](course/semester-1/hardware-workshop/) | 7,838 | 24 | done |
| 2 | BCA 151 | [Discrete Structure](course/semester-2/discrete-structure/) | 12,728 | 34 | done |
| 2 | BCA 152 | [Microprocessor and Computer Architecture](course/semester-2/microprocessor-computer-architecture/) | 25,282 | 76 | done |
| 2 | BCA 153 | [OOP in Java](course/semester-2/oop-in-java/) | 10,096 | 41 | done |
| 2 | BCA 154 | [Mathematics II](course/semester-2/mathematics-2/) | 9,256 | 23 | done |
| 2 | BCA 155 | [UX/UI Design](course/semester-2/ux-ui-design/) | 22,095 | 71 | done |
| 2 | BCA 156 | [Principles of Management](course/semester-2/principles-of-management/) | 15,475 | 50 | done |
| 3 | BCA 201 | [Data Structure and Algorithms](course/semester-3/data-structure-and-algorithms/) | 22,743 | 75 | done |
| 3 | BCA 202 | [Database Management System](course/semester-3/dbms/) | 15,156 | 56 | done |
| 3 | BCA 203 | [Web Technology I](course/semester-3/web-technology-1/) | 9,924 | 45 | done |
| 3 | BCA 204 | [System Analysis and Design](course/semester-3/system-analysis-and-design/) | 9,919 | 33 | done |
| 3 | BCA 205 | [Probability and Statistics](course/semester-3/probability-and-statistics/) | 9,323 | 30 | done |
| 3 | BCA 206 | [Applied Economics](course/semester-3/applied-economics/) | 11,390 | 34 | done |
| 4 | BCA 251 | [Operating Systems](course/semester-4/operating-systems/) | 27,698 | 85 | done |
| 4 | BCA 252 | [Software Engineering](course/semester-4/software-engineering/) | 16,608 | 54 | done |
| 4 | BCA 253 | [Numerical Methods](course/semester-4/numerical-methods/) | 14,925 | 43 | done |
| 4 | BCA 254 | [Python Programming](course/semester-4/python-programming/) | 15,321 | 79 | done |
| 4 | BCA 255 | [Web Technology II](course/semester-4/web-technology-2/) | 15,068 | 64 | done |
| 5 | BCA 301 | [Computer Network](course/semester-5/computer-networking/) | 23,727 | 65 | done |
| 5 | BCA 302 | [Artificial Intelligence](course/semester-5/artificial-intelligence/) | 20,790 | 59 | done |
| 5 | BCA 303 | [Advanced Java Programming](course/semester-5/advanced-java/) | 16,715 | 61 | done |
| 5 | BCA 304 | [MIS and e-Business](course/semester-5/mis-and-e-business/) | 14,480 | 45 | done |
| 5 | BCA 305 | [Society and Technology](course/semester-5/society-and-technology/) | 14,263 | 44 | done |

Semesters I, II, III and IV are fully done (Semester IV's Project I is a project with no notes by nature). Everything else in `course/CURRICULUM.md` is mapped only (no notes). Nothing here has had a subject-teacher review.
<!-- /COURSE-STATUS -->


Everything here is Markdown first (readable on GitHub, diffable, forkable) with a printable PDF next to it.

| Part | Where | What |
|---|---|---|
| **Entrance** | [`entrance/`](entrance/README.md) | 4 books: Mathematics, English, GK and IT, three full model papers. 1,332 keyed MCQs. PDFs in `entrance/pdfs/` |
| **Course** | [`course/`](course/README.md) | The 8-semester BCA programme: the verified curriculum map and the subject books written so far, PDFs in `course/semester-N/pdfs/` |
| Reviews | [`entrance/REVIEW_ENTRANCE.md`](entrance/REVIEW_ENTRANCE.md), [`course/REVIEW_COURSE.md`](course/REVIEW_COURSE.md) | What was audited, found, fixed, and what is still open |
| Sources | [`SOURCES.md`](SOURCES.md) | Where the curriculum and exam facts come from, and how reliable each is |
| Tools | [`tools/`](tools/) | `nebpdf.py` (builds PDFs with the NEBians house pipeline), `qa_pdf.py` (visual/structural PDF QA), `sync_entrance.sh`, `gen_status.py` (status tables), `check_*.py` (per-subject verifiers: compile-and-diff C and Java, SymPy maths, an 8085 simulator, numeric checkers) |

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
