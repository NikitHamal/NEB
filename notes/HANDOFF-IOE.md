# IOE entrance books — handoff (start here)

Written at the end of the session that imported the IOE B.E./B.Arch. set into this repo
(Nov 2 2026). Read this first, then `AUTHORING-ENTRANCE.md` (the contract) and
`HANDOFF-ENTRANCE.md` (the entrance-track architecture).

## State

| Book slug | Spine | Chapters | MCQs | check.py | mcqcheck |
|---|---|---|---|---|---|
| ioe-math | `curriculum/ioe-math.md` (7 units, 35 Q, 50 marks) | 7 of 7 | 192 | OK | all keyed |
| ioe-phy | `curriculum/ioe-phy.md` (6 units, 27 Q, 40 marks) | 6 of 6 | 142 | OK | all keyed |
| ioe-chem | `curriculum/ioe-chem.md` (3 units, 22 Q, 30 marks) | 3 of 3 | 90 | OK | all keyed |
| ioe-eng | `curriculum/ioe-eng.md` (4 units, 16 Q, 20 marks) | 4 of 4 | 113 | OK | all keyed |
| ioe-mock | `curriculum/ioe-mock.md` (guide + 2 model papers) | 3 of 3 | 210 | OK | all keyed |

Everything is in the NEBians authoring format (frontmatter, `::: key / note / caution / tip`
boxes, `**Set A — …**` MCQ lists with `::: note Answers …` boxes, `$…$` LaTeX).

**Where the content came from.** The chapters and the four spines were authored in an earlier
session in a sibling workspace and imported here. The `ioe-mock` spine did not exist and was
written for this repo; `ioe-mock/unit-01.md` is that workspace's exam guide, promoted to the
guide chapter so the book matches `cee-mock` (guide as unit 1, model papers after).

## What was fixed on import

1. **Math that matplotlib rejects (417 failures → 0).** The chapters use valid LaTeX shorthand
   that mathtext does not accept: `\frac ab`, `\sqrt2`, `\mathbb N`, `\operatorname{sech}`,
   `\begin{pmatrix}`. KaTeX (the web and app reader) renders all of it, so this only ever
   blocked the PDF build. A recursive normaliser braced every argument, rewrote `\mathbb` /
   `\operatorname` to `\mathrm` and flattened matrix environments to `(det | … |)`. Every
   expression was meaning-preserving; see `notes/tools/` history for the script shape.
   **Before writing new IOE chapters, read §4 of `AUTHORING.md` — write `\frac{a}{b}` with
   braces from the start.**
2. **One over-wide display equation** (`ioe-math/unit-05`, 185 mm) split into two `$$…$$`.
3. **One over-long MCQ option** (`ioe-mock/unit-02` Q97, 101 characters) shortened to fit the
   option grid.
4. **A dead key letter.** `ioe-eng/unit-04` never used `(b)` as the key in any of its five
   answer boxes. Five option pairs were swapped so `(b)` now carries 5 of 25 keys; the whole
   book is a 26.9 / 24.0 / 26.3 / 22.8 spread across a/b/c/d.
5. **A "check the rules" MCQ set** added to the guide chapter, matching `cee-mock/unit-01`.

## What is still missing (be honest with students)

- **Figures: 0 in every chapter.** `AUTHORING-ENTRANCE.md` asks for 1–4 per chapter. The
  sibling workspace produced prose, tables and equations only. Priority: projectile and
  `v`–`t` graphs, ray diagrams, circuit schematics, conics, a p–n junction I–V curve.
- **MCQ counts are below the contract.** `AUTHORING-ENTRANCE.md` requires at least 40 per
  chapter (50 for a chapter carrying 3+ questions); these run 18–34. Extend each chapter
  with a **Set D** rather than rewriting Sets A–C. Priority order: Algebra, Calculus,
  Mechanics, Electricity and Magnetism, Physical Chemistry, Organic Chemistry.
- **Two of five model papers.** `ioe-mock` has units 2 and 3. Add units 4–6 in the same
  format (numbered straight through 1–100, subject sections, one answer box per section).
  Each must differ from the others in questions, numbers and facts.
- **The reader cannot score IOE's two weights.** `study-exam.js` and `StudyReaderPage.kt`
  both apply `+1` right and `−negative` wrong for *every* question. IOE deducts 10 % of the
  question's own marks, so Section B should lose 0.2, not 0.1. `export_study.py` ships only
  `{"minutes", "negative"}` from `spine.TRACKS`. Extend the exported `exam` to
  `{"minutes":120,"negative":0.1,"weights":{"1-60":1,"61-100":2},"negativeMode":"fraction"}`
  and score `right*w − 0.1*w*wrong`. Until then the timed test under-penalises Section B;
  the chapter text states the true rule and gives the self-scoring formula, and the guide
  chapter explains it, so nothing a student reads is wrong.
- **No PDFs.** Every other book in the repo ships one. `python notes/pipeline/build_pdf.py
  ioe-phy` (and the other four) after the figures land.
- **Not reviewed by IOE faculty.** Every question is original practice written to the
  official 2083 syllabus; none claims to be a past question. If you find a wrong key,
  correct the Markdown and re-run the exporters.

## Sources

| Source | Used for |
|---|---|
| IOE *Detail Syllabus of B.E./B.Arch. Entrance Examination-2083* (`sources/entrance/IOE-BE-BArch-entrance-syllabus-2083.pdf`) | the whole spine: 7 + 6 + 3 + 4 areas, subject marks 50 / 40 / 30 / 20, the 19 model questions |
| IOE B.E./B.Arch. booklet 2083 (as quoted by IOE-facing sites) | computer-based, 2 hours, 100 questions, 140 marks, Section A 60 × 1, Section B 40 × 2, 10 % of a question's marks deducted |
| IOE entrance notice 2083/84 (published July 2026) | exam dates in Shrawan 2083, four centres, mouse-only rule, no way to clear a selected option |
| IOE admission page (ioe.tu.edu.np) | mode, 140 marks, 100 questions, 2 hours, 10 % negative marking |

**Not official, and labelled as such in the books:** the split of the 100 questions between
subjects (Maths 20+15, Physics 14+13, Chemistry 14+8, English 12+4), the chapter-wise
question counts `[n]` in the spines, and every fee figure.

## Verification done on import

- `notes/pipeline/check.py` on all 23 chapters: **23/23 OK**, zero math failures, zero
  over-wide display equations.
- `notes/tools/mcqcheck.py` on all 23 chapters: **exit 0**, 737 MCQs, every one keyed, no
  problem flagged (no unkeyed list, no over-long option, no non-contiguous answer box, no
  run of five identical keys, no letter above 36 %).
- Both exporters re-run: `export_syllabus.py` → 5 new `ioe-*.json` plus `index.json`;
  `export_study.py` → 23 chapters in 5 new `web/data/study/ioe-*/`. No school-grade file
  moved (the exporters now pass `newline="\n"`, so a Windows export is diffable).
- Django suites: `web` 159 tests / 2 failures and `api` 240 / 7 — both sets are exactly the
  failures AGENTS.md already records as pre-existing. Zero regressions.
- Rendered pages: the syllabus hub lists the IOE track with all five subjects; every subject
  page links every unit; both model papers render with the 120-minute banner and the 0.1
  negative-marking rule and keyed MCQs; the guide renders with no timer;
  `/api/syllabus/v2/ioe/*` reports 6/6, 3/3, 7/7, 4/4 and 3/3 chapters present;
  `/sitemap-pages.xml` lists all five IOE subject URLs.

## Next steps (keep ordered)

1. Add figures (above), then build the five PDFs.
2. Extend every chapter to 40+ MCQs with a Set D.
3. Write model papers 3–5 (`ioe-mock` units 4–6).
4. Teach the readers IOE's two-weight negative marking.
5. Then CSIT (`csit-*`, incl. `csit-comp`) and BCA (`bca-math`, `bca-eng`, `bca-gk`, mocks),
   which need no code — a track appears once its spines and a chapter exist.
