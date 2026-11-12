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

## BCA 105 professional-communication-ethics -- IN PROGRESS (rewrite to the 6-unit TU textbook structure)
Textbook TOC (from student photos): U1 Foundation of Professional Communication, U2 Oral Communication,
U3 Writing Professionally, U4 Interpersonal and Group Communication, U5 Digital Communication, U6 Professional Ethics;
each unit ends with Vocabulary and Grammar + two prescribed Readings with Exercises. ~268 pp in the print book.
