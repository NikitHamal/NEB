# BCA polish status (web reader + TU textbook-depth rewrite)

Continues `bca/POLISH_STATUS.md` (older 5-pillar tracker; do not duplicate). Source of this task: student feedback
"Story haru kei xainata. Matlab readings" -- BCA 105 had 5 short units / 55 pp and none of the prescribed readings.

## Web reader fixes (done, session 16)
- `notes/pipeline/md2html.py::_split_question`: an inline `(a) ... (b) ...` run after a stem ending in `:` whose parts
  are sentences ("Correct the sentences: (a) "..." ") is now typeset as exercise parts, not as MCQ option cells
  (this produced the giant bordered box with only item a).
- `study-reader.css`: `.opts` grid no longer stretches rows; `.opts.c3` added; sidebar TOC links clamp at 3 lines.
- `nebpdf.py::stage`: the "Formula and fact sheet" heading becomes "Key facts at a glance" for every subject not in
  `FORMULA_BOOKS` (PDF + web sidebar both follow, because the web export stages through nebpdf).

## BCA 105 professional-communication-ethics -- DONE (session 17): 6 units in the TU textbook order
Textbook TOC (from student photos): U1 Foundation of Professional Communication, U2 Oral Communication, U3 Writing
Professionally, U4 Interpersonal and Group Communication, U5 Digital Communication, U6 Professional Ethics; each unit ends
with Vocabulary and Grammar + two prescribed Readings with Exercises.

| Unit | Words | Readings covered (summary, themes, analysis, solved exercises; no reprint of the texts) |
|---|---|---|
| 1 | 7.4k | "Mother Tongue" (Tan), "The Letter" (Dhumaketu; hunter/separation detail corrected) |
| 2 | 7.3k | "Death by Powerpoint" (Garber, 2001), "Our world on fire needs you" (Ressa, Harvard 23 May 2024); both re-checked against sources |
| 3 | 7.9k | "Gateman's Gift" (REWRITTEN to the real plot: models left for the accountant, registered letter, commendation + cheque, gives up modelling), "My School" (Tagore) |
| 4 | 8.4k | "Computer and the Pursuit of Happiness" (Gelernter, Commentary 2001), "The Collapse of the Family and the Community" (Harari, Sapiens ch. 18) |
| 5 | 8.8k | "Cat Pictures Please" (Kritzer; checked against the full story), "ChatGPT May Be Eroding Critical Thinking Skills" (Chow, TIME 17 Jun 2025, MIT Media Lab study) |
| 6 | 10.5k | "The Necklace" (Maupassant), "The Digital Citizen" (Ceccarini, 2021; summary built from the book's argument and abstract, flagged as such) |

- PDF: `bca/course/semester-1/pdfs/NEBians-BCA-Course-Semester-1-Professional-Communication-and-Ethics.pdf`, `pdfinfo` = **148 pages**
  (was 48-55), `qa_pdf.py` = **fails=0 warns=10** (tiny text in a photo credit, a few short pages before chapters).
- Web data re-exported (`export_course_web.py semester-1/professional-communication-ethics`): 6 units, 45 topics.
- Pipeline fixes this session: `md2html._LABEL` now handles parts (a) to (h) (a sixth part used to stay inline); long
  vocabulary tables are split in the source (a 26-row table caused two blank pages); svgfig code must not use `WHITE` (use "#ffffff").
- Authoring gotcha: inside heredocs do not write `\"`; the shell keeps the backslash.
- Honest gaps: textbook sub-lists for 4.7 were out of frame, so grammar topics there are chosen by the book (README says so);
  "The Digital Citizen" extract was not available, check the student's copy; no Django screenshots of the web reader were
  taken this session (data and CSS fixes from session 16 are in place; verify visually next time).

## Session 18 results

### Web reader verified visually (Django on :8765, headless Chromium)
- BCA 105 now shows the 6 textbook units in the left rail; the right "On this page" list has no "Formula and fact sheet" entry and no clipped labels.
- Exercise 6.7.2 "Correct the errors" (unit 6) typesets as parts (a) to (e), no giant bordered box. The original bug text (`it's database`) lives in this item.
- New book renders: BCA 402 Unit 2 with sidebar of all 7 units, tables and a working "On this page" list. SPM keeps the "Formula and fact sheet" heading because it has formulas (added to `FORMULA_BOOKS` in `nebpdf.py`).
- Minor, not fixed: wide tables in worked-example callouts stop short of the callout width on the web (cosmetic).

### BCA 402 Software Project Management: NEW book (was wrongly classed as a "project slot" by `gen_status.py`)
- 7 units after the TU CACS407 syllabus (concepts, scheduling, estimation, evaluation and costing, risk, quality, SCM), 24.8k words,
  14 figures (all label-linted with `svgkit.lint`: 0 warnings), every worked number recomputed in Python (see its README).
- PDF `bca/course/semester-7/pdfs/NEBians-BCA-Course-Semester-7-Software-Project-Management.pdf`: `pdfinfo` = **84 pages**,
  `qa_pdf.py` = **fails=0 warns=2** (two near-empty pages p16, p72 at chapter ends). Web data exported: 7 units, 38 topics.
- `books.json`, `CURRICULUM.md`, `STATUS.md`, READMEs regenerated (`gen_status.py`): 42 books done, 0 core subjects missing.
- Pages inspected as PNG: contents (p3), CPM network (p21), risk matrix (p56), change-control flow (p78, labels were clipped, fixed and re-rendered), triangle (p7).

### Verified numbers (this session)
BCA 105 PDF 148 pp (qa 0 fail, from session 17); BCA 402 PDF 84 pp. All other BCA PDFs untouched this session.

### BCA 354 Technical Writing vs BCA 105 (queue item 2): checked
354 is documentation-centred (requirements, README, API docs, runbooks, IMRaD, citation, charts). Overlap with 105 is limited to
email/CV/cover letter (354 6.3-6.4), plagiarism and citation (354 4.4-4.5; 105 5.4) and readability. It is reinforcement in a different
setting (technical vs professional), not duplication; no change made.

## Prioritised queue for the next session
1. Audit the thinnest books against the current TU syllabus and add depth and figures: BCA 106 Hardware Workshop (13.7k words, 42 pp),
   BCA 204 System Analysis and Design (18k, 60 pp), BCA 154 Mathematics II (21.8k, 57 pp), BCA 153 OOP in Java (21.8k, 79 pp),
   BCA 354 (23.6k, 71 pp), BCA 403 Financial Accounting (24.8k, 76 pp), BCA 256/306/356/404 project books (18-27k).
2. Run the label-overflow lint (`svgkit.lint`, see the snippet idea in this file's history: render each svgfig block and print `svgkit.WARN`)
   over ALL course books: the build log hides lint warnings when the figure cache hits. Fix clipped labels with `\n` line breaks.
3. Electives (BCA 405/406, 453/454) remain unwritten slots; pick the most common (Machine Learning, E-Commerce, Linux, DBA).
4. Take web screenshots of one text-heavy and one math-heavy BCA subject to compare reader spacing; optionally widen tables in callouts.
5. Environment recipe is in the section above; the sandbox needs `pypdf` too (reading payload step).

## Session 19 (in progress)
- Re-verified BCA 105: PDF 148 pp (`pdfinfo`), `qa_pdf.py` fails=0; 6 textbook units and every TOC sub-heading (1.1.1-1.1.6, 2.3 meetings/agendas/minutes, 4.4 virtual/successful teams, 6.4 malpractice) present in the unit files.
- FOUND: BCA 106 Hardware Workshop was a *reconstructed* 4-unit book. The real TU syllabus has 9 units (1 Electronic components, 2 Networking components and cabling, 3 Desktop/laptop hardware identification, 4 PC and laptop assembly, 5 Network device deployment + printers, 6 Basic networking configuration, 7 Problem solving, 8 Maintenance and upgrade, 9 Final practical assessment; source hamronotes.com/bca/semester-1/hardware-workshop/chapters). Rewriting the book to those 9 units (see below for progress).
