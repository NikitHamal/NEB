# NEBians — BCA (Tribhuvan University), free and open

Everything here is Markdown first (readable on GitHub, diffable, forkable) with a printable PDF next to it.

| Part | Where | What |
|---|---|---|
| **Entrance** | [`entrance/`](entrance/README.md) | 4 books: Mathematics, English, GK and IT, three full model papers. 1,332 keyed MCQs. PDFs in `entrance/pdfs/` |
| **Course** | [`course/`](course/README.md) | The 8-semester BCA programme: the verified curriculum map and the subject books written so far, PDFs in `course/semester-N/pdfs/` |
| Reviews | [`entrance/REVIEW_ENTRANCE.md`](entrance/REVIEW_ENTRANCE.md), [`course/REVIEW_COURSE.md`](course/REVIEW_COURSE.md) | What was audited, found, fixed, and what is still open |
| Sources | [`SOURCES.md`](SOURCES.md) | Where the curriculum and exam facts come from, and how reliable each is |
| Tools | [`tools/`](tools/) | `build_pdfs.py` (Markdown → PDF), `sync_entrance.sh`, `check_c_examples.py` |

## Clone

```
git clone --branch claude/bca-entrance-complete https://github.com/NikitHamal/NEB.git
cd NEB/bca
```

## PDFs are committed, not Git LFS

Total PDF size is a few megabytes (text and vector only, no photographs), well under GitHub's limits, so the PDFs are ordinary committed files. Git LFS was not used; it would make a plain `git clone` return pointer files instead of readable PDFs.

## Rebuild the PDFs

```
pip install weasyprint markdown pygments     # + libpango-1.0-0 libpangoft2-1.0-0 fonts-liberation fonts-dejavu
python3 bca/tools/build_pdfs.py              # every book under bca/
```
Any directory containing `unit-NN.md` files is a book. Tested with WeasyPrint 70 on Python 3.11.

## Honest status

See `course/README.md` for exactly which subjects are fully written and which are only mapped. Nothing is marked complete that is not.

## Merge log

| Date (UTC) | What |
|---|---|
| 2026-11-02 | `origin/main` (tip `2193bf3f`) merged into `claude/bca-entrance-complete` as commit `9519f189`. Brought in: the IOE entrance track (`backend_python/web/data/study/ioe-*`, `notes/curriculum/ioe-*`, `notes/HANDOFF-IOE.md`, `notes/sources/entrance/IOE-BE-BArch-entrance-syllabus-2083.pdf`), the house PDF pipeline in `notes/pipeline/` (WeasyPrint + `theme.css`), the CEE/Grade 8–12 books in `notes/pdf/`, the Rust desktop app, and the web/auth fixes. One textual conflict (`ENV.md`, added on both sides) — resolved by keeping both: the BCA/IOE probe first, main's desktop probe verbatim as an appendix. Verified after the merge: 0 files deleted and 0 files modified relative to `origin/main` other than `ENV.md`; all 65 pre-merge `bca/` files present. |
