# BCA Entrance — TU FOHSS

Four books that prepare a student for the Tribhuvan University BCA entrance test, written to the paper's real shape: **100 multiple-choice questions, 100 marks, 2 hours — English grammar 40, Mathematics 50, General Knowledge and IT 10.**

| Book | Folder | Chapters | Keyed MCQs | PDF |
|---|---|---|---|---|
| Mathematics (50 marks) | `mathematics/` | 15 | 600 | `pdfs/NEBians-BCA-Entrance-Mathematics.pdf` |
| English (40 marks) | `english/` | 7 | 272 | `pdfs/NEBians-BCA-Entrance-English.pdf` |
| General Knowledge and IT (10 marks) | `gk-and-it/` | 4 | 160 | `pdfs/NEBians-BCA-Entrance-General-Knowledge-and-IT.pdf` |
| Model Papers and Mock Tests (guide + 3 papers of 100) | `model-papers/` | 4 | 300 | `pdfs/NEBians-BCA-Entrance-Model-Papers-and-Mock-Tests.pdf` |

Start with `model-papers/unit-01.md` (pattern, eligibility, 12-week plan), then work the Mathematics units in order alongside English units 1–4.

## Folder layout

- `<book>/unit-NN.md` — one chapter per file: opening, "What the paper asks", one `## N.k` section per syllabus bullet, formula and fact sheet, chapter summary, then Sets A (recall), B (understanding), C (application), each with a keyed answer box.
- `<book>/SPINE.md` — the syllabus spine the chapters follow, with the estimated number of questions per chapter.
- `pdfs/` — the printable books, rebuilt from the Markdown by `bca/tools/build_pdfs.py`.
- `REVIEW_ENTRANCE.md` — the audit: what was checked, what was found, what was changed.

## Source of truth

`notes/content/bca-{math,eng,gk,mock}/` is the canonical copy because the NEBians reader app and the repo's check tools read it. The folders here are mirrored from it with `bca/tools/sync_entrance.sh`. Edit there, run the script, rebuild the PDFs.

## Rebuild

```
pip install weasyprint markdown pygments        # plus libpango + fonts-liberation + fonts-dejavu
bca/tools/sync_entrance.sh
python3 notes/tools/bcacheck.py notes/content/bca-*/unit-*.md
python3 bca/tools/build_pdfs.py bca/entrance/mathematics bca/entrance/english bca/entrance/gk-and-it bca/entrance/model-papers
```

## Facts that expire

Current-affairs answers in `gk-and-it/unit-01`, `unit-02` and Model Papers questions 91–100 are dated to 2026. Re-check them before every exam year. The 2083 exam was scheduled for 16 August 2026 per the TU notice reproduced on edusanjal.com.
