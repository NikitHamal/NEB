# Entrance-examination and bachelor books — handoff (start here)

Branch: **`resources/entrance-and-bachelor`** (from `main` @ `1dafb80d`). Push with
`notes/tools/lockpush.sh "message" <paths…>` (serialised commit + push of only the
paths named; the clone's `origin` already carries a token). Never `git add -A`:
`notes/figures/` is the render cache and is excluded locally.

Started 2026-10-24 ~20:00 UTC by an AgentSky Claude session. The owner's brief:
research and write the best free preparation material in Nepal for **CEE (MECEE-BL)**
first, then the **other entrance examinations** (IOE engineering, BSc CSIT, BCA, …),
then **bachelor courses** (BCA, CSIT, …) — notes, PDFs, syllabus, interactive
practice, practice sets, explained solutions, predicted and model papers. Push often;
keep this file current so a new session can continue mid-stream.

## What exists (update the table as work lands)

| Book slug | Spine | Chapters written | PDF | Web export |
|---|---|---|---|---|
| cee-phy | `notes/curriculum/cee-phy.md` (22 ch, 50 Qs) | see `notes/content/cee-phy/` | — | — |
| cee-chem | `cee-chem.md` (22 ch, 50 Qs) | | — | — |
| cee-zoo | `cee-zoo.md` (14 ch, 40 Qs) | | — | — |
| cee-bot | `cee-bot.md` (15 ch, 40 Qs) | | — | — |
| cee-mat | `cee-mat.md` (5 ch, 20 Qs) | | — | — |
| cee-mock | `cee-mock.md` (guide + 5 model papers of 200) | | — | — |
| ioe-* | not yet | | | |
| csit-* / bca-* | not yet | | | |

Always check reality with `ls notes/content/<slug>/` and `git log --oneline`.

## Sources (authoritative; copies in `notes/sources/entrance/`)

- **MEC syllabus, third revision 2083-01-15 (28 Apr 2026)** —
  `MEC-MECEE-BL-syllabus-3rd-revision-2026-04-28.pdf` (mirrored by edusanjal
  `media.edusanjal.com/c/New%20Syllabus%20MECEE-BL%20Entrance%20Examination.pdf`;
  mec.gov.np returns 502 from this pod). 200 MCQs, 3 h, −0.25 per wrong answer, merit
  from the 50th percentile, recall:understanding:application 50:30:20, stems ≤ 60
  words. Group I (MBBS/BDS/BSc Nursing/BASLP/B Perfusion): Zoology 40 (3/4/4/6/15/4/2/2),
  Botany 40 (2/9/4/5/6/3/6/2/3), Chemistry 50 (17/10/17/3/3), Physics 50
  (10/7/8/9/4/12), MAT 20 (5/5/5/5). Group II (BAMS, BPharm, MLT…) Chemistry 40,
  Physics 40 + 20 PCL-specific. The second revision (2082-05-02) had different domains —
  do not use it.
- **IOE BE/BArch entrance syllabus 2083** — `IOE-BE-BArch-entrance-syllabus-2083.pdf`
  (same as 2081/2082 except the year). Booklet 2083 (Preeti-encoded; decode with
  `notes/tools/preeti2unicode.py`): computer-based, 2 hours, 100 questions = 60 × 1 +
  40 × 2 = 140 marks, 10 % of a question's marks deducted for a wrong answer.
  Mathematics 50, Physics 40, Chemistry 30, English 20. The per-subject split of
  1- and 2-mark questions is not in the official document (third-party sites:
  Maths 20+15, Physics 14+13, Chemistry 14+8, English 12+4 — consistent with 60/40).
- **BSc CSIT (IOST) model question** — `IOST-BSc-CSIT-entrance-model-question.pdf`:
  100 MCQs, 2 hours, Mathematics 25, Physics 25, Chemistry 25, English 15, Computer 10.
- **BCA (FOHSS)**: 100 MCQs, 2 hours; Mathematics 50, English 40, GK & IT 10 (third
  party, consistent across sites; confirm on entrance.tufohss.edu.np when reachable).

## How the books are made

- Contract: `notes/AUTHORING-ENTRANCE.md` (on top of `notes/AUTHORING.md`).
- Slugs `<track>-<subject>`; `notes/pipeline/spine.py` `TRACKS` / `TRACK_SUBJECTS`
  (cover line, exam minutes and negative marking); `i18n.ENTRANCE_EN` (book furniture:
  "Chapter", "questions in the paper"); `spine.pdf_name()` →
  `notes/pdf/NEBians-CEE-Entrance-Physics.pdf` etc.
- Spine `[n]` = questions in the paper for that chapter (area totals official,
  per-chapter split = our estimate, stated in the spine header and the book).
- Checks per chapter: `cd notes/pipeline && python3 check.py ../content/<slug>/unit-NN.md`
  (must print OK) and `python3 notes/tools/mcqcheck.py notes/content/<slug>/unit-NN.md`
  (every MCQ keyed; key-letter spread).
- Build a book: `cd notes/pipeline && python3 build_pdf.py cee-phy` → `notes/pdf/`.
- Web/app export (after a book changes): `python3 notes/tools/export_syllabus.py` and
  `python3 notes/tools/export_study.py cee-phy …` (entrance books key MCQ lists that start
  at any number from a later answer box — `export_study._mcq_keys(far=True)`).

## Process that works

Parallel writer subagents (Agent tool), 4–5 at a time, each given 3–6 chapters of one
book with the brief in this file's "Writer brief" section; each writes → check.py →
mcqcheck → looks at figure PNGs → `lockpush.sh` per chapter. The coordinator reviews
(spot-checks keys by recomputing), builds PDFs one book at a time, exports for the
web, updates this file, pushes.

## Writer brief (paste into an Agent prompt, fill in the slug and units)

> You are writing chapters of a free entrance-preparation book in the NEBians repo at
> /data/workspace/NEB (branch resources/entrance-and-bachelor, environment ready:
> matplotlib, fonts, check.py). Book: <slug>; write units <list>, in this order, one at a
> time. Read fully first: notes/AUTHORING-ENTRANCE.md, then notes/AUTHORING.md §3–6,
> §11–12 (§14 for biology), the spine notes/curriculum/<slug>.md, and the official
> syllabus text (CEE: notes/sources/entrance/MEC-…pdf, or the extracted text in
> /data/workspace/task/sources/mec-2026.txt). Use the NEBians Grade 11/12 book chapters
> (notes/content/phy11, phy12, chem11, chem12, bio11, bio12, math11, math12) for
> curriculum terms, but write denser, MCQ-first material. After each chapter: check.py
> OK, mcqcheck OK, figures PNG-inspected, then lockpush it. Verify every numerical key
> in Python. Do not start a new chapter after <deadline UTC> (`date -u`); finish and
> push the one in progress. Report briefly per chapter: words, figures, MCQs, status.

## Next steps (keep ordered)

1. Finish CEE: all chapters of cee-phy, cee-chem, cee-zoo, cee-bot, cee-mat; cee-mock
   unit 1 (exam guide) and five model papers.
2. Build the six CEE PDFs; export syllabus + study JSON; check the reader keys.
3. IOE spines (`ioe-math`, `ioe-phy`, `ioe-chem`, `ioe-eng`, `ioe-mock`) from the 2083
   syllabus → chapters → PDFs → export.
4. CSIT (`csit-*`, incl. `csit-comp`) and BCA (`bca-math`, `bca-eng`, `bca-gk`, mocks).
5. Bachelor programmes (first semesters of BSc CSIT and BCA first), as new tracks.
6. Web + Android: entrance tracks in the syllabus hub (API `tracks` key for
   backward compatibility), timed model-paper mode in the reader.

## Session log

- 2026-10-24 20:00–20:45 UTC — recon, toolchain (WeasyPrint 70, matplotlib 3.11.2,
  fonts), official syllabi found and saved, pipeline track support, CEE spines,
  authoring contract, mcqcheck, lockpush; first wave of writers dispatched.
