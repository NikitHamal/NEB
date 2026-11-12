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

## Prioritised queue for the next session (rest of BCA, not started this session)
1. Audit every semester against the current TU syllabus (the 2082-batch list in `course/CURRICULUM.md`) for missing topics,
   starting with the thinnest books: BCA 106 Hardware Workshop (13.7k words), BCA 204 System Analysis and Design (16.8k),
   BCA 154 Mathematics II (19.5k), BCA 153 OOP in Java (21.8k), BCA 354 Technical Writing (21.6k), BCA 403 Financial Accounting (22k).
2. BCA 354 Technical Writing overlaps BCA 105 (writing, reports, referencing): cross-check for duplication and consistency.
3. Add more figures to text-heavy books (photogrid/svgfig), then rebuild, `qa_pdf.py`, `export_course_web.py <book>`.
4. Take Django web-reader screenshots of BCA Unit 3 and check the right-hand "On this page" list for clipped labels.
5. Rebuild the other course PDFs only if a sweep flags them; `gen_status.py` showed page counts that differ from earlier tables.
