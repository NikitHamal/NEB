# CHANGELOG — BCA course

## Session 3: remaining subjects, Semester II onward

Word counts are raw (whitespace-split over the unit files, so code listings, tables and answer keys are included) and are the numbers `tools/gen_status.py` prints; they are larger than prose-only counts. **Semester II is now fully done (6 of 6 subjects).**

**Finished this session (each pushed on its own):**

- Semester 2 · BCA 152 · Microprocessor and Computer Architecture: 25,282 raw words (units only; includes code listings and tables), 76 PDF pages, 8 units, QA 0 failures (1 soft warning: a short page at the end of the contents). 13 assembly programs assembled and executed on the 8085 simulator in `tools/check_mpca.py`, which also recomputes Booth, division, IEEE-754, pipeline, cache, paging, disk and Amdahl numbers (100 checks, all pass).
- Semester 2 · BCA 155 · UX/UI Design: 22,095 raw words (units only), 71 PDF pages, 8 units, QA 0 failures (3 soft warnings: short pages at the end of the contents and of two chapters). Theory subject: `tools/check_uxui.py` recomputes 36 numbers (WCAG contrast, Fitts, Hick, SUS, KLM, sample size, type scales, grids).
- Semester 2 · BCA 156 · Principles of Management (1 credit): 15,475 raw words (units only), 50 PDF pages, 6 units, QA 0 failures (1 soft warning: short contents page). `tools/check_management.py` recomputes 46 numbers. Syllabus reconstructed from the older TU Introduction to Management / BIM outline (revised 1-credit PDF not retrievable); see its README.

## Session 2: remaining-subject push

**Finished this session (7 subjects, in order, each pushed on its own):**

- Semester 1 · BCA 101 · Computer Fundamentals and Applications: 16,040 words, 53 PDF pages
- Semester 1 · BCA 104 · Mathematics I: 11,443 words, 33 PDF pages
- Semester 1 · BCA 105 · Professional Communication and Ethics: 10,381 words, 34 PDF pages
- Semester 1 · BCA 106 · Hardware Workshop: 7,838 words, 24 PDF pages
- Semester 2 · BCA 151 · Discrete Structure: 12,728 words, 34 PDF pages
- Semester 2 · BCA 153 · OOP in Java: 10,096 words, 41 PDF pages
- Semester 2 · BCA 154 · Mathematics II: 9,256 words, 23 PDF pages

(Programming in C and Digital Logic were done in earlier sessions and not touched.)

**Not started (exactly):**

- Semester 3 · BCA 201 · Data Structure and Algorithms
- Semester 3 · BCA 202 · Database Management System
- Semester 3 · BCA 203 · Web Technology I
- Semester 3 · BCA 204 · System Analysis and Design
- Semester 3 · BCA 205 · Probability and Statistics
- Semester 3 · BCA 206 · Applied Economics
- Semester 4 · BCA 251 · Operating Systems
- Semester 4 · BCA 252 · Software Engineering
- Semester 4 · BCA 253 · Numerical Methods
- Semester 4 · BCA 254 · Python Programming
- Semester 4 · BCA 255 · Web Technology II
- Semester 4 · BCA 256 · Project I
- Semester 5 · BCA 301 · Computer Network
- Semester 5 · BCA 302 · Artificial Intelligence
- Semester 5 · BCA 303 · Advanced Java Programming
- Semester 5 · BCA 304 · MIS and e-Business
- Semester 5 · BCA 305 · Society and Technology
- Semester 5 · BCA 306 · Project II
- Semester 6 · BCA 351 · Computer Graphics and Animation
- Semester 6 · BCA 352 · Mobile Programming
- Semester 6 · BCA 353 · Cryptography and Network Security
- Semester 6 · BCA 354 · Technical Writing
- Semester 6 · BCA 355 · Distributed System
- Semester 6 · BCA 356 · Project III
- Semester 7 · BCA 401 · Cyber Security and Ethical Hacking
- Semester 7 · BCA 402 · Software Project Management
- Semester 7 · BCA 403 · Financial Accounting
- Semester 7 · BCA 404 · Project IV
- Semester 8 · BCA 451 · Cloud Computing
- Semester 8 · BCA 452 · Internship

Also not started: elective slots BCA 405/406 and 453/454 (see `CURRICULUM.md`). The six project/internship subjects have no study material because they are not taught from notes; a guide for them is a possible later addition.

**Tooling changes:** `tools/check_java_examples.py` (compiles and runs every Java program in a book and compares the printed output), `tools/check_math1.py`, `tools/check_math2.py`, `tools/check_discrete.py` (re-derive the numeric answers). The PDF pipeline itself was not changed. The pipeline needs Python 3.12 (it uses f-string syntax that 3.11 rejects) and the fonts from `notes/pipeline/fonts/install.sh`; see ENV.md.


## Session 5 — Semester III completed (6 of 6 core subjects)

Semester III is now fully done. Accounting note: the repository's own STATUS.md counts 44 slots (the session briefing's "42 / 22 core" undercounted by two); at the start of this session it read 12 done · 24 core missing · 8 project/internship/elective slots. After this session it reads **18 done · 18 core missing · 8 slots**.

| Subject | Code | Units | Raw words | PDF pages | QA |
|---|---|---|---|---|---|
| Data Structure and Algorithms | BCA 201 | 11 | 22,743 | 75 | pass: 0 failures; 1 warning: p3 TOC overflow |
| Database Management System | BCA 202 | 9 | 15,156 | 56 | pass: 0 failures; 3 warnings: p3 TOC overflow; p26, p50 chapter-end answer spill |
| Web Technology I | BCA 203 | 7 | 9,924 | 45 | pass: 0 failures; 2 warnings: p3 TOC overflow; p34 chapter-end answer spill |
| System Analysis and Design | BCA 204 | 5 | 9,919 | 33 | pass: 0 failures; 1 warning: p3 TOC overflow |
| Probability and Statistics | BCA 205 | 7 | 9,323 | 30 | pass: 0 failures; 2 warnings: p3 TOC overflow; p10 chapter-end answer spill |
| Applied Economics | BCA 206 | 7 | 11,390 | 34 | pass: 0 failures; 2 warnings: p3 TOC overflow; p25 chapter-end spill |

Total new material: 78,455 raw words. **Tooling added:** `tools/fill_c_outputs.py` (runs each C program and inserts its real output), `tools/fill_sql_outputs.py` (runs each SQL block on PostgreSQL, real results and error messages), `tools/fill_web_outputs.py` + `tools/jq_runner.js` (Node and jsdom/jQuery outputs, xmllint check of XML), `tools/normalize_md.py` (blank line before lists, which the house Markdown parser needs), `tools/check_stats.py`, `tools/check_economics.py` (recompute every worked and practice number). The PDF pipeline was not changed.

**Layout lesson recorded:** the house CSS makes every `pre` block `break-inside: avoid`, so a program taller than the space left on a page jumps to the next page and leaves a near-empty page behind its heading. Three long programs (stack/postfix, all sorts, graph algorithms) were therefore split into two shorter complete programs each; this removed three blank pages from the Data Structure and Algorithms PDF.

**Not done in this session:** Semesters IV–VIII (18 core subjects: IV 5, V 5, VI 5, VII 2, VIII 1) and the 8 project/internship/elective slots. No subject-teacher review of any book has happened.
