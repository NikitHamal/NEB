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

## Session 19 results

- BCA 105 re-verified: PDF 148 pp (`pdfinfo`), `qa_pdf.py` fails=0; all 6 textbook units and TOC sub-headings present.
- **BCA 106 Hardware Workshop rewritten to the real 9-unit TU syllabus** (source: hamronotes.com chapter list; the earlier 4-unit book was a reconstruction).

| Unit | Title | New content this session |
|---|---|---|
| 1 | Electronic components | done earlier in the session (5.5k words) |
| 2 | Networking components | NEW: devices by OSI layer, UTP/coax/fibre, T568A/B, straight/crossover/rollover, crimping, cable tests (3.4k words, 2 figures) |
| 3 | Hardware identification | + RAM generations, ROM family, north/southbridge and buses, storage interfaces, fake SSD test, I/O devices, full PSU section (rails, 24-pin figure, paperclip test, 80 PLUS) |
| 4 | PC and laptop assembly | + POST and beep codes, POST card, drivers, virtual/real printer install, Windows/Linux/cross-platform commands |
| 5 | Network devices and deployment | NEW: identification, topologies (figure), file/folder/printer sharing, printer technologies, install and maintenance |
| 6 | Networking configuration | NEW: IP classes, private ranges, subnetting (all examples checked with `ipaddress`), Cisco CLI, AP setup, RSSI, ping/tracert/ipconfig/netstat/arp/nslookup/route/netsh, mini LAN task |
| 7 | Problem solving | NEW: Identify-Test-Isolate-Fix-Verify, visual inspection, elimination, log |
| 8 | Maintenance and upgrade | NEW: compatibility, RAM/SSD/GPU/CPU, cleaning, paste, battery, BIOS flashing, SMART, MemTest86+ |
| 9 | Final practical assessment | NEW: five stations, checklists, sample 50-mark scheme (flagged as a practice model), 40 viva Q&A |

- PDF `bca/course/semester-1/pdfs/NEBians-BCA-Course-Semester-1-Hardware-Workshop.pdf`: `pdfinfo` = **109 pages** (was 42), `qa_pdf.py` = **fails=0 warns=29** (tiny text in the old Fig 3.1 and photo credits). 11 new figures.
- Web data exported (`export_course_web.py semester-1/hardware-workshop`): 9 units, 80 topics.
- Pages inspected as PNG: contents (9 units), Fig 2.1, 24-pin ATX (3.3), topology figure (5.1, fixed: arrows covered node labels, mesh clipped at the right edge), subnet figure (6.1), LAN figure (6.2).
- Pipeline lessons: `R1 + 2R2` in prose is auto-detected as math and falls back; write R₁, R₂. MathJax server needs `cd notes/pipeline/mathjax && npm ci` in a fresh sandbox. `git add -A bca` misses `backend_python/web/data/study`; use `git add -A`.
- Not done / honest gaps: Django web-reader screenshots were NOT taken this session (the session 18 verification still stands); unit 6.2 figure 6.2 pushes to a new page leaving white space on p79; old Fig 3.1 has 6 pt labels (p31).

## Prioritised queue for the next session
1. Take Django + headless Chromium screenshots of BCA 105 Unit 6 and BCA 106 Unit 6 in the web reader (exercise parts, sidebar labels).
2. Fix Fig 3.1 small labels; reduce the white space after Fig 6.2.
3. Thin books vs current TU syllabus: BCA 204 System Analysis and Design (60 pp), BCA 154 Mathematics II (57 pp), BCA 153 OOP in Java (79 pp), BCA 354 (71 pp), BCA 403 Financial Accounting (76 pp), project books BCA 256/306/356/404.
4. Run `svgkit.lint` over all course books (the build hides label overflow warnings when the figure cache hits).
5. Electives BCA 405/406, 453/454 are still unwritten slots.
6. Check BCA 106 against the student's printed lab manual if available (hours per unit unknown).

## Session 20
- Fresh sandbox rebuilt from the recipe: `pip install --break-system-packages weasyprint markdown matplotlib numpy pymupdf pyyaml pillow pypdf sympy fonttools pandas scipy playwright -r backend_python/requirements.txt`; `sudo apt-get install poppler-utils libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 chromium`; `bash notes/pipeline/fonts/install.sh`; `cd notes/pipeline/mathjax && npm ci`.
- BCA 105 rebuilt from source: `pdfinfo` 148 pp, `qa_pdf.py` fails=0 warns=10 (reproducible).
- Web reader verified in Django (:8765, Playwright + system chromium, `executable_path=/usr/bin/chromium`): BCA 105 Unit 3 and Unit 6 show the six textbook units in the left rail, a clean "On this page" list (no "Formula and fact sheet"), and Exercise 6.7.2 "Correct the errors" typesets as parts (a) to (e) with no giant box.

## Session 21 results (syllabus-gap audit, new units, web reader re-verified)

Fresh sandbox recipe that worked (the older one failed: pip needs a venv, apt needs `sudo apt-get update` first):
`sudo apt-get update; sudo apt-get install -y python3.11-venv poppler-utils libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 chromium default-jdk-headless; python3 -m venv /tmp/v; /tmp/v/bin/pip install weasyprint markdown matplotlib numpy pymupdf pyyaml pillow pypdf sympy fonttools pandas scipy playwright -r backend_python/requirements.txt; (cd notes/pipeline/mathjax && npm ci)`; build with `NEB_PY=/tmp/v/bin/python /tmp/v/bin/python bca/tools/nebpdf.py course/<sem>/<slug>`, then `export_course_web.py <sem>/<slug>`.
Django for screenshots: `cd backend_python; DB_ENGINE=sqlite DEBUG=True SECRET_KEY=<any long string> python manage.py runserver 127.0.0.1:8765 --noreload`; URL `/app/syllabus/bca-course/<slug>/unit-N/`. Headless scrolling: scroll the window in 1500 px steps, wait, then scrollTo the heading (jumping straight far down renders blank).

### BCA 105 Professional Communication and Ethics (student feedback)
Verified again against the textbook TOC (every numbered section 1.1.1 to 6.8.2, Vocabulary and Grammar, two Readings and Exercises per unit): complete. Rebuilt: **151 pp** (`pdfinfo`), `qa_pdf.py` fails=0 warns=26 (6 pt text inside figures and photo credits).
Web reader inspected in Django + headless Chromium: left rail lists the 6 textbook units; right rail has no "Formula and fact sheet"; Unit 6 Exercise 6.7.2 item 2 "Correct the errors" (the screenshot bug, `it's database`) now typesets as plain parts (a), (b), (c) with no giant bordered box.

### Gaps found against the current TU syllabus and closed
| Book | Gap | Fix | Pages (before -> after), qa |
|---|---|---|---|
| BCA 153 OOP in Java | design patterns, copy constructors, inner classes, jagged arrays | NEW Unit 7 (singleton, factory, observer, shallow/deep copy, 4 nested kinds, jagged arrays, varargs, lambdas/Optional checklist); 8 programs compiled and run by `fill_java_outputs.py`; 1 figure | 79 -> **95**, fails=0 warns=116 (old figures have 6 pt labels) |
| BCA 403 Financial Accounting | whole company-accounts unit missing; accounting policies, capital/revenue, contingent items, stock taking, manufacturing account | NEW Unit 8 (company, share capital layers, shares vs debentures, issue with over-subscription, forfeiture and re-issue, debentures, redemption of preference shares; 4 worked examples verified in Python; 2 figures) + sections 1.7, 2.8, 5.7, 6.8 | 76 -> **94**, fails=0 warns=7 |
| BCA 354 Technical Writing | collaboration, web writing, information reports, proposals, group presentations | NEW Unit 7 (2 executed Python blocks, 1 figure, model answers) | 71 -> **83**, fails=0 warns=6 |

Also fixed: Financial Accounting Unit 2 title had literal quote marks that showed in the web rail. Web data re-exported for all three books; `gen_status.py` regenerated STATUS/README.
Honest gaps: Nepal-specific company-law thresholds (101 shareholders, seven founders, CRR practice) are as commonly taught, not checked against the Act text; FA Figure 8.1 leaves white space on p80; the TW syllabus "instructions" and "formal reports" topics only have short sections (Unit 3, 6.4). Not re-audited this session: all other BCA books (see queue).

## Prioritised queue for the next session
1. Audit remaining books against the live TU outline the same way (grep for syllabus keywords, then add a unit): BCA 204 SAD (already extended in session 20), BCA 154 Mathematics II, BCA 205 Statistics, BCA 206 Applied Economics, BCA 304 MIS, BCA 305 Society and Technology, BCA 401, 451, projects 256/306/356/404.
2. BCA 354: full chapters on instructions and formal reports (TU units 8 and 11).
3. BCA 153: the TU unit order is 8 units; the book keeps its own order. Consider splitting collections/generics and file handling into separate units, and add RandomAccessFile, deadlock program, and a Swing-free replacement for the old GUI section.
4. Fix 6 pt labels in old figures (OOP Java p17, Hardware Workshop Fig 3.1, BCA 105 pp12/21); run `svgkit.lint` over all books.
5. Electives BCA 405/406, 453/454 remain unwritten slots.

## Session 22/23 results (350+ continuation: BCA 354 Unit 8 built, BCA 154 syllabus gaps closed)

Picked up from sessions 16-21 (no duplicate tracker). Sandbox recipe from session 21 worked unchanged (venv at `/tmp/v`, `sudo apt-get update` first, `cd notes/pipeline/mathjax && npm ci`).

### Re-verified, no change needed
- **BCA 105** (student feedback): still 6 textbook units, 151 pp. Web reader re-checked in Django + headless Chromium: Unit 3 left rail shows the six textbook units, right rail has no "Formula and fact sheet"; Unit 6 Exercise 6.7.2 "Correct the errors" (`it's database`) typesets as plain parts (a) to (e), no giant box.
- Keyword audit against the published TU outlines: **BCA 204 SAD** (all syllabus topics present: CASE, RAD, SOA, XP, BPP, JAD, decision tables, supertypes, normalisation, usability, testing, documentation, maintenance) and **BCA 205 Probability and Statistics** (questionnaire, non-sampling error, PPS, one/two-way ANOVA with m observations per cell, ratio/regression estimation) have no gaps.

### BCA 354 Technical Writing: Unit 8 built
Source (instructions, technical definitions and descriptions, formal reports, recommendation/feasibility reports, checklist) had been committed last session without a build. `check_techwriting.py --verify` = 26 tokens, 0 unfilled; PDF **83 -> 103 pp** (`pdfinfo`), `qa_pdf.py` fails=0 warns=6 (photo credit 6.2 pt, one near-empty page p69); web data 8 units / 49 topics; manifest refreshed. Pages viewed: contents (p3), instructions table (p84), recommendation-report table and checklist (p96).

### BCA 154 Mathematics II: gaps vs the revised TU outline closed
Checked the CAMT154 outline (units 1-6). Missing and now added, each with worked examples, executed code, practice with solutions and a model answer:
| Unit | New section | Notes |
|---|---|---|
| 2 | 2.7 inverse circular and hyperbolic derivatives (proofs, table, tanh/sigmoid in neural nets, catenary); 2.8 partial derivatives (mixed, chain rule, total differential, Laplace, gradient descent) | 2 figures (hyperbolic curves, contour + descent path), 2 executed blocks, sympy-checked |
| 4 | 4.8 surface of revolution (cone, sphere, paraboloid); 4.9 numerical integration (trapezoidal, Simpson 1/3 and 3/8, error bounds, table data) | figure 4.3, executed block (errors 2.6e-3 vs 6e-6) |
| 5 | 5.8 Bernoulli equation + logistic model; 5.9 partial differential equations (forming, direct integration, heat/wave/Laplace, separation of variables) | executed Euler check and sympy PDE check |
- Old "Eight uses" sections renumbered (2.9, 4.10, 5.10). Unit 6 heading `6.5 ... $f(x) = 0$` had raw TeX leaking into the running header (qa FAIL): fixed by plain text.
- PDF **57 -> 97 pp**, `qa_pdf.py` fails=0 warns=87 (old figures with 5-6 pt labels). Web data 6 units / 47 topics. Pages viewed: hyperbolic page (p24), numerical integration (p61), Bernoulli/logistic (p78), PDE + heat equation (p79); web reader Unit 5 shows the new sections in "On this page".
- **Pipeline lesson**: `md2html._inline_one` and `mathsvg.derive` auto-break any formula with 2+ `=`/implication links (and comma lists) into an aligned block, so `$$a = b, \quad c = d$$` or `X'' + ... \Rightarrow X = ..., \qquad T' = ...` renders as garbage. Write each equation as its own `$$...$$`; keep chains for real step-by-step derivations only. A `$...$` inside a `##` heading leaks into the running page header (qa FAIL "leaked TeX").

### Pushed commits (this session)
`84e0c7e` (354 normalize), `0c62d5d` (354 build + manifest), `64eb0b5` (Math II source), `20d9ca8` (Math II PDF/web/manifest), plus the final tracker commit.

## Prioritised queue for the next session
1. Audit not yet done against live TU outlines (grep keywords, then add units/sections): BCA 206 Applied Economics, BCA 304 MIS, BCA 305 Society and Technology, BCA 401, BCA 451 Cloud, BCA 156 Principles of Management, BCA 151 Discrete Structure; project books 256/306/356/404.
2. BCA 153: TU unit order is 8; book has 7 own-order units. Split collections/generics and file handling, add RandomAccessFile and a deadlock program.
3. Fix 5-6 pt labels in old figures (Mathematics II Fig 5.x p45, OOP Java p17, Hardware Workshop Fig 3.1, BCA 105 pp12/21); run `svgkit.lint` over all books.
4. Mathematics II lab part: TU lists Mathematica/Excel/Matlab labs per unit; add a short Python/Excel lab list for each unit.
5. Electives BCA 405/406, 453/454 remain unwritten slots.
6. Run `tools/publish/update_books.py --only <slug>` with server credentials for 354 and 154 (manifest already refreshed locally).

## Session 24 results (BCA 305 finished to the TU outline, BCA 103 lab/PLD gaps closed, web reader re-verified)

Sandbox recipe from session 21 worked again, with one fix: the pip line must use `-r backend_python/requirements.txt` (not a /tmp path). Build: `NEB_PY=/tmp/v/bin/python /tmp/v/bin/python bca/tools/nebpdf.py course/<sem>/<slug>` detached, poll the log (output appears only at the end, about 25 s).

### Re-verified (BCA 105, student feedback; no change needed)
`pdfinfo` = **151 pp**, `qa_pdf.py` fails=0 warns=26. Six textbook units present. Web reader (Django :8765 + Playwright): left rail lists the six units, right rail has no "Formula and fact sheet", Unit 3 "My School" exercise renders cleanly, and Unit 6 exercise "Correct the errors" (the `it's database` item from the bug report) typesets as plain parts (a) to (e), no giant bordered box (element screenshot taken).

### BCA 305 Society and Technology (continued from commit 48f1246)
TU outline (CACS102, checked against notebahadur.com, bcanotenepal.com, bcanotesnepal.com): Unit 1 sociology, 2 organizing social life, 3 social system and stratification of Nepalese societies, 4 society and technology. Book now has 11 units: 1-3 and 8 follow the TU outline, 4-7 and 9-11 are the technology extension (README states this).
- Unit 3 finished: new 3.6 religion-based and ecology-based stratification (Census 2021 shares), 3.7 national integration (1768 to 2015), Figure 3.2, summary, 12 practice questions with answers, 3 model answers (5000 words).
- Unit 8 NEW (5000 words): technological society (Bell, Toffler, Ellul, Castells, McLuhan, Winner), technological change in Third World societies (transfer, dependency, appropriate technology, leapfrogging), social and cultural bases of change, diffusion process and patterns, consequences on Nepalese society (including the September 2025 social-media ban protests, flagged as "state what you are sure of"), accountability of computer professionals, research in social science; Figure 8.1; practice and four model answers.
- PDF `bca/course/semester-5/pdfs/NEBians-BCA-Course-Semester-5-Society-and-Technology.pdf`: **133 pp** (`pdfinfo`), `qa_pdf.py` fails=0 warns=7 (photo credit 6.2 pt). `check_society.py --verify unit-*.md`: 88 tokens, 0 unfilled. Web data: 11 units, 69 topics.
- Pages inspected as PNG: contents (11 units), p36 (Figure 3.2 and chapter summary), p90-91 (Figure 8.1 and the consequences table; first build left a half-empty page because the long table jumped to the next page, so it was split into two tables). Web reader unit 8 rail shows all 11 units and the new section list.
- Honest gaps: Census 2021 shares (religion, ecology) are from memory of published tables and should be re-checked against the CBS tables; the September 2025 paragraph is deliberately short.

### BCA 103 Digital Logic (keyword audit against the TU CACS105 outline)
Gaps found and closed: EPROM and PAL/PLA were one paragraph; no "implementation of logical functions using multiplexers"; no 16:1 MUX / 1:16 DEMUX; no gates from active and passive elements; no practical list.
- Unit 3: 3.6 extended (PROM, EPROM/EEPROM/flash, PAL, PLA, fuse-map reading, PROM full adder, PLA sharing example, Figure 3.4), new 3.7 (MUX with n and n-1 selects, a 4-variable worked example, decoder + NAND full adder; all checked in Python), 3.8 (16:1 MUX from five 4:1, 1:16 DEMUX; Figure 3.5), 3.9 (diode AND/OR, transistor NOT, DTL, RTL; inverter current check), old 3.7 renumbered 3.10, 6 new practice questions, 2 model answers.
- Unit 5: new 5.7 laboratory works (all six TU labs with parts, procedure, expected result, viva; 555 frequency 1.05 Hz and mod-60 clock checked).
- PDF `NEBians-BCA-Course-Semester-1-Digital-Logic.pdf`: **65 -> 74 pp**, `qa_pdf.py` fails=0 warns=216 (old figures with 5-6 pt labels, see queue). Web data 5 units, 32 topics.
- Pages inspected as PNG: p36 (Figure 3.4), p39-40 (Figure 3.5, split gates table, lab procedure box).

### Pushed commits this session
`d21bf29` (305 source), `4c22ba2` (305 PDF/web), `cc7cc16` (103 source), `79bea4b` (103 PDF/web), plus the tracker commit.

## Prioritised queue for the next session
1. Audit still not done against live TU outlines (keyword grep, then add sections): BCA 206 Applied Economics, BCA 304 MIS, BCA 401, BCA 451, BCA 156 Principles of Management, BCA 151 Discrete Structure, BCA 101/102/104, projects 256/306/356/404.
2. Digital Logic: 5-6 pt labels in old figures (216 qa warnings); check lab outline against the student's printed lab manual.
3. BCA 153: split collections/generics and file handling into their own units, add RandomAccessFile and a deadlock program.
4. Fix old tiny figure labels (Math II, OOP Java p17, Hardware Workshop Fig 3.1, BCA 105 pp12/21); run `svgkit.lint` over all books.
5. Electives BCA 405/406, 453/454 are still unwritten slots (pick Machine Learning, E-Commerce, Linux, DBA).
6. Run `tools/publish/update_books.py --only <slug>` with server credentials for 305, 103, 354, 154.

## Session 25 results (BCA 304 MIS and e-Business brought to the real TU outline; BCA 105 re-verified)

Picked up from sessions 16-24 (this file; no duplicate tracker). Sandbox recipe from session 21 worked unchanged (venv `/tmp/v`, apt, `npm ci` in `notes/pipeline/mathjax`, fonts). Project root in the sandbox was `/home/user/sandbox`.

### BCA 105 Professional Communication and Ethics (student feedback): re-verified, no change needed
- Heading audit of `unit-01.md` to `unit-06.md` against the textbook TOC photos: every numbered section 1.1.1 to 6.8.2, each unit's Vocabulary and Grammar and both Readings with Exercises are present; 52k words, PDF 151 pp (session 24 `pdfinfo`/`qa_pdf.py`).
- Web reader checked again in Django (:8765) + headless Chromium: Unit 6 shows the six textbook units in the left rail, the right rail has no "Formula and fact sheet", and Exercise 6.7.2 item 2 "Correct the errors" (the screenshot bug text `it's database`) renders as clean parts (a) to (e), no giant box (`shots/web105_u6.png`, inspected).

### BCA 304 MIS and e-Business: gap audit against the TU outline (CACS, six units; source notebahadur.com)
The README said no TU outline had been retrieved and the book had no Unit 2 at all. Keyword grep found WAP, I-Way, WiMAX, cPanel, SEO, Heartbleed, ACH, micropayments and crypto missing. Closed:

| Unit | New or extended content |
|---|---|
| 2 NEW (3.8k words) | I-Way and components, Internet as e-commerce infrastructure (packet switching, DNS, IXP, intranet/extranet), WAP architecture, stack and working, ADSL/Wi-Fi/WiMAX/UMTS/LTE/5G NR table, 100 MB download-time example, wireless security (evil twin, SIM swap, WAP gap); 3 figures, 11 practice questions, model answers |
| 5 | 5.6 international information systems, outsourcing vs offshoring (cost example); 5.7 enterprise-system implementation challenges and how to manage them (payback example); 4 more practice items |
| 7 | 7.6 payment cards (credit, charge, debit, prepaid, smart; four-party model, 3-D Secure, PCI DSS, fee example), 7.7 micropayments, e-checks, ACH, 7.8 mobile wallets/QR/NFC and international payments, 7.9 virtual currency and cryptocurrency (NRB position), 7.10 Nepal case study of emerging trends; 5 new practice items; figure 7.1 (card cycle), old figures renumbered 7.2 to 7.4 |
| 8 | 8.6 security terminology and the six requirements, 8.7 technical attacks (virus/worm/Trojan, ransomware, Heartbleed, DDoS and botnets, sniffing, page hijacking, malvertising, injection), 8.8 social engineering and fraud; 2 figures (DDoS, attack taxonomy), 6 new practice items; figures renumbered |
| 10 NEW (4.5k words) | Business plan, cost-benefit and risks, funding, model selection, building process and site hierarchy, domain/DNS/hosting, cPanel walk-through, content and catalogue management, site map, grid, colour, usability, Core Web Vitals, payment implementation, SEO, conversion example; 3 figures, 14 practice questions, 2 model answers |

- README now maps units to the TU outline (units 4, 6, 9 are labelled extensions).
- PDF `bca/course/semester-5/pdfs/NEBians-BCA-Course-Semester-5-MIS-and-e-Business.pdf`: `pdfinfo` **84 -> 140 pages**, `qa_pdf.py` fails=0 warns=9 (6.2 pt photo credits). Web data re-exported: **10 units, 81 topics**; `gen_status.py` regenerated.
- Pages inspected as PNG: p23 (Fig 2.1; "regional network" overflowed, fixed with a line break), p25 (WAP figure and stack table), p86 (card cycle figure), p105 (DDoS figure), p107 (attack taxonomy), p129 (site hierarchy), p133 (12-column grid), p136 (conversion funnel). Web reader MIS Unit 10 inspected (`shots/web304_u10.png`): left rail lists all 10 units, right rail lists 10.1 to 10.7, summary, practice, model answers.
- Figures renumbered so that new figures that sit earlier in the text carry lower numbers (unit 7 and unit 8).
- Honest gaps: `check_mis.py` was not extended to the new calculations (they were checked by hand: download times, break-even 40 orders, payback 7.5 months, fee Rs 220, DDoS 10 percent pass, outsourcing saving Rs 60,000, funnel 480 orders / 2.4 percent); card interchange rates are labelled illustrative; Nepal payment trends, the NRB crypto stance and cross-border QR links are general knowledge flagged "verify current status"; TU outline hours (7/8/8/10/6/10) are not copied into the unit front matter; the `hours` of units 1 and 3 to 9 still follow the older reconstructed split.

## Prioritised queue for the next session
1. Same keyword audit against the live TU outline for: BCA 206 Applied Economics, BCA 401 Cyber Security, BCA 451 Cloud, BCA 156 Principles of Management, BCA 151 Discrete Structure, BCA 101/102/104, projects 256/306/356/404 (search the TU outline on notebahadur.com, grep for each topic, add units or sections, rebuild, `qa_pdf.py`).
2. Extend `bca/tools/check_mis.py` to the new MIS numbers (download time, fee split, DDoS load, funnel).
3. BCA 153: split collections/generics and file handling into their own units; add RandomAccessFile and a deadlock program.
4. Old figures with 5-6 pt labels (Math II, OOP Java p17, Hardware Workshop Fig 3.1, BCA 105 pp12/21, Digital Logic); run `svgkit.lint` over all books.
5. Electives BCA 405/406 and 453/454 are still unwritten slots (Machine Learning, E-Commerce, Linux, DBA are the likely picks); note that the new MIS unit 10 overlaps an E-Commerce elective, so pick another first.
6. Run `tools/publish/update_books.py --only <slug>` with server credentials for 304, 305, 103, 354, 154.

## Session 26 (in progress)
Picked up from sessions 16-25 (this file; no duplicate tracker). Fresh sandbox again needed the session-21 recipe (venv `/tmp/v`, apt, `npm ci`, fonts); project root was `/app`.
Plan: re-verify BCA 105 and web reader with screenshots, then continue queue items 3 and 4 (BCA 153 collections/file-handling units, label lint).

## Session 27 results (BCA 105 re-verified, NEW elective book BCA 405 Machine Learning)

Picked up from sessions 16-26 (this file; no duplicate tracker). Sandbox recipe from session 21 worked unchanged (venv `/tmp/v`, `sudo apt-get update` first, `npm ci` in `notes/pipeline/mathjax`, fonts). Project root in the sandbox was `/app`.

### BCA 105 Professional Communication and Ethics (student feedback): re-verified by script
A keyword audit of the markdown headings against the 60 textbook-TOC entries (sections 1.1.1 to 6.8.2, Vocabulary and Grammar, both Readings and Exercises of every unit) found 0 missing; 6 units, 52k words. PDF and web-reader fixes (exercise parts instead of the giant MCQ box, no "Formula and fact sheet" outside formula books, 3-line clamp in the TOC rail) are unchanged from sessions 16-25. Not rebuilt this session; the last verified build is 151 pp (session 24). The student's phone copy (55 pp) is the OLD published PDF: the new PDF must be published with `tools/publish/update_books.py --only professional-communication-ethics` using server credentials, which this sandbox does not have.

### BCA 405 Machine Learning (Elective I): NEW book, was an unwritten slot
Source of the units and hours: TU CACS456 outline (notebahadur.com): U1 Introduction (10 h), U2 Supervised learning (11 h), U3 Bayesian and instance-based learning (11 h), U4 Unsupervised learning and dimensionality reduction (10 h), U5 Performance evaluation (8 h, hours estimated).
- ~19.5k words, 12 python programs executed by `fill_script_outputs.py` (NumPy only, fixed seeds), 9 figures, 5 units each with summary, exercises and model answers; hand answers re-checked (Hoeffding N = 738, least squares, perceptron trace, PlayTennis gains 0.247/0.152/0.048/0.029, SVM margin 2.83, naive Bayes 0.795/0.90, alarm network 0.284, k-NN k-sweep, k-means trace, PCA 30.385/6.615, ROC AUC 0.84, confidence intervals).
- Mistakes caught while writing: ill-conditioned degree-9 fit (changed to degree 5), a wrong k-NN distance table and tie (query moved to (2.5, 3.5)), a wrong perceptron epoch count and naive-Bayes product in model answers, `svgkit.Fig.arrow(lpos=...)` takes an (x, y) point, not a fraction.
- PDF `bca/course/semester-7/pdfs/NEBians-BCA-Course-Semester-7-Machine-Learning.pdf`: `pdfinfo` **61 pages**, `qa_pdf.py` **fails=0 warns=0**. Web data exported (`export_course_web.py semester-7/machine-learning`): 5 units, 46 topics, `index.json` entry added. `books.json`, `CURRICULUM.md` (BCA 405 split from 406), STATUS and READMEs regenerated with `gen_status.py`.
- Pages inspected as PNG: contents (title with a colon wrapped badly; fixed by removing the colon), Fig 1.1 neuron (arrow labels overlapped, replaced by a caption line), Fig 2.2 decision tree, Fig 3.2 k-NN, Fig 4.1 dendrogram, Fig 5.1 ROC (axis labels overlapped the ticks, fixed), p55 regression measures (R squared now display math).
- Honest gaps: Django web-reader screenshots were not taken this session (the Session 25 verification stands, only a new book was added); the book is shorter than the other 24-60k-word books (19.5k words) and could take more worked problems, a figure for the SVM margin and an XOR network diagram; Figure 4.2 (elbow) and Figure 3.1 (alarm network) were not rendered to PNG; Unit 5 hours are an estimate; the lab data sets are described, not supplied.

## Prioritised queue for the next session
1. Publish updated PDFs with server credentials (`update_books.py --only <slug>`): 105, 304, 305, 103, 354, 154, 405.
2. Deepen BCA 405 (SVM margin figure, network diagram, more numerical practice) and write the other electives: BCA 405 alternatives (E-Commerce overlaps MIS Unit 10), Linux, Database Administration; Elective II DotNet, Software Testing; III and IV as in `CURRICULUM.md`.
3. Keyword audit against the live TU outline for: BCA 401 Cyber Security, 451 Cloud, 156 Principles of Management, 151 Discrete Structure, 101/102/104, projects 256/306/356/404 (BCA 206 Applied Economics was re-checked this session against CAEC353: all 7 units match).
4. Django + Chromium screenshot of BCA 405 Unit 2 (code outputs, formulas) in the web reader.
5. BCA 153 split of collections/file handling; fix 5-6 pt figure labels (Math II, OOP Java p17, Hardware Workshop Fig 3.1, Digital Logic); run `svgkit.lint` over all books; extend `check_mis.py`.

## Session 28 results (student feedback re-verified; BCA 401 and BCA 451 brought to the real TU outlines)

Picked up from sessions 16-27 (this file; no duplicate tracker). Fresh sandbox `/home/user/sandbox`; session-21 recipe worked (add `python3-venv`; `cd notes/pipeline/mathjax && npm ci`; fonts installer).

### BCA 105 Professional Communication and Ethics (student feedback): re-verified
- Heading audit of the six `unit-0N.md` against 36 textbook-TOC keywords (every 1.1.1 to 6.8.2 sub-section, Vocabulary and Grammar, both Readings per unit): 0 missing. `pdfinfo` of the committed PDF: **151 pages** (qa fails=0, session 24). The student's phone copy (55 pp) is the OLD published file; publish with `tools/publish/update_books.py --only professional-communication-ethics` (needs server credentials, not available here).
- Web reader inspected in Django :8765 + headless Chromium: left rail lists the six textbook units; right rail has no "Formula and fact sheet"; Unit 6 Exercise 6.7.2 item 2 ("Correct the errors", the `it's database` text from the bug report) renders as plain parts (a) to (e) with no giant box; Unit 3 intro and rail render cleanly (screenshots inspected, then deleted).

### BCA 401 Cyber Security and Ethical Hacking: NEW Unit 8 (the TU outline is CEH-style; the book had no attack-methodology unit)
- Unit 8 "Ethical Hacking Methodology, Attack Categories and Their Defences" (7.7k words): hats and five phases (kill chain, ATT&CK), footprinting, scanning and enumeration (scan types, service leaks, detector), system hacking and password attacks, malware (SI worm model), sniffing and session hijacking, social engineering, DoS/DDoS (amplification, SYN flood), OWASP Top 10, wireless/mobile/IoT/cloud, evasion and honeypots, cryptographic attacks; 3 figures, 6 executed Python blocks (output filled by `fill_script_outputs.py`, numbers re-checked by hand), 15 exercises, 5 model answers. Still defensive: no payloads or attack commands.
- PDF `NEBians-BCA-Course-Semester-7-Cyber-Security-and-Ethical-Hacking.pdf`: `pdfinfo` **110 pages** (was about 80), `qa_pdf.py` fails=0 warns=9 (photo credits 6.2 pt). `check_cybersec.py --verify`: 39 tokens, 0 unfilled. Web data 8 units / 67 topics.
- Pages inspected as PNG: contents (8 units), Fig 8.1 (label overlapped the boxes, spacing fixed), Fig 8.2 (literal `\n` and clipped footer, fixed), Fig 8.3 (curve label hit the axis title, moved).

### BCA 451 Cloud Computing: NEW Units 8 and 9 (TU outline: Map Reduce unit, SOA, platforms, applications, security topics were missing)
- Unit 8 "Parallel Computing and the MapReduce Model" (about 6k words): parallelism, Flynn, speedup/efficiency, Amdahl and Gustafson, map/shuffle/reduce, combiner and partitioner, applications, cost model with stragglers, Hadoop HDFS/YARN, fault tolerance; 2 figures, 5 executed blocks (job 800 s vs 62,000 s serial, speedup 77.5; combiner 16 GB to 0.32 GB; 1 GB file = 24 block replicas), 14 exercises, 4 model answers.
- Unit 9 "Service-Oriented Architecture, Cloud Platforms, Applications and Security Practice" (about 5k words): SOA principles, SOAP/WSDL/UDDI vs REST, composed availability (98.31%, 148 h/yr), Google App Engine, Azure, Aneka, scientific/business/consumer applications, SaaS/application/VM/data security, monitoring, trust and privacy, adoption sequence, field-visit report outline; 2 figures, 15 exercises, 5 model answers.
- PDF `NEBians-BCA-Course-Semester-8-Cloud-Computing.pdf`: `pdfinfo` **104 pages** (was about 74), `qa_pdf.py` fails=0 warns=12. `check_cloud.py --verify`: 44 tokens, 0 unfilled. Web data 9 units / 68 topics.
- Pages inspected as PNG: Fig 8.1 and 8.2 (Amdahl curve labels collided with the axis title and the 0.95 curve, moved and re-rendered), Fig 9.1 and 9.2.

### Honest gaps
- Aneka, App Engine and Azure details come from public descriptions (Buyya et al. 2013; vendor documentation), not from the student's textbook; check the printed chapter. The old TU 2074 cloud outline was used (benchpartner.com); the 2082 revised outline for BCA 451 was not retrievable.
- BCA 401 unit hours are my estimate (8); MapReduce hours (8) and platforms (12) follow the TU outline.
- Not re-audited this session: BCA 156, 151, 101/102/104 and project books; the 6 pt labels in older figures remain; PDFs are not published to the server.

### Pushed commits this session
`7b33e34` (tracker), `6c67ed1` (401 source), `65369b2` (401 PDF/web), `c9b3ae5` (451 unit 8 source), `b314982` (451 unit 9 source), `4ea3463` (451 PDF/web), plus the final tracker commit.

## Prioritised queue for the next session
1. Publish updated PDFs (`update_books.py --only <slug>`): 105, 401, 451, 304, 305, 103, 354, 154, 405.
2. Keyword audits against live TU outlines still pending: BCA 156 Principles of Management, 151 Discrete Structure, 101/102/104, projects 256/306/356/404; BCA 353 (check the CACS459-style Information Security items: Miller-Rabin, Galois fields, HMAC, S/MIME, PGP, IPsec).
3. Electives: BCA 406/453/454 (E-Commerce overlaps MIS Unit 10; Linux, Database Administration, DotNet, Software Testing) are still unwritten slots; deepen BCA 405 (SVM margin figure, network diagram).
4. BCA 153 split of collections and file handling; fix 5-6 pt labels in old figures; run `svgkit.lint` over all books.
5. Web: wide tables in worked-example callouts stop short of the callout width (cosmetic).

## Session 29 results (BCA 105 re-checked, BCA 156 brought to the revised TU outline)

Picked up from sessions 16-28 (this file; no duplicate tracker). Fresh sandbox `/home/user/sandbox`; the session-21 recipe worked unchanged (`/tmp/setup.sh`: apt, venv `/tmp/v`, pip, `npm ci` in `notes/pipeline/mathjax`, fonts). Note: other agents push to `main` concurrently; use `git pull --rebase origin main` before pushing.

### BCA 105 Professional Communication and Ethics (student feedback): heading check
`unit-01..06.md` headings still follow the textbook TOC (Units 1-6, sections x.1 to x.8, Vocabulary and Grammar, both prescribed Readings with Exercises per unit; 52k words). Nothing changed this session. The student's 55-page copy is the OLD published PDF; publishing needs server credentials (`tools/publish/update_books.py --only professional-communication-ethics`).

### BCA 156 Principles of Management: NEW Unit 7
Audit: the book followed the older BBS-style outline (6 units). The revised outline (hamronotes chapter list: Introduction, Planning and Decision Making, Organizing, Leading) names topics the book lacked: forms of business, integrated management framework, role of IT in management/planning/decisions, job design/description/specification, forms of organisational design, generic/situational/emerging leadership, managing teams in crisis, leadership challenges in IT organisations.
- Unit 7 "IT in Management, Forms of Business, Job Design and Leadership Approaches" (7.2k words): 9 sections, 2 figures (integrated framework; functional/divisional/matrix), a payback worked example (Rs 3,00,000 system: 2.17 years), liability worked example, complete sample job description and specification, Managerial Grid, Fiedler, Hersey-Blanchard, path-goal, VYJ, transformational/servant/authentic, crisis case, IT leadership table; 15 exercises with answers, 4 model answers. Numbers recomputed by hand (2.17, 2.73 years, 4.5 years pessimistic case).
- PDF `NEBians-BCA-Course-Semester-2-Principles-of-Management.pdf`: `pdfinfo` **113 pages** (was about 97), `qa_pdf.py` fails=0 warns=11. Web data: 7 units / 51 topics.
- Pages inspected as PNG: Fig 7.1 (ok), Fig 7.2 (first build: matrix part overlapped the divisional part and the rule-of-thumb box was one clipped line; fixed with new coordinates and `\n` breaks, re-rendered).
- Honest gaps: Nepali legal details (101 shareholders for a private company, seven promoters for a public company, Partnership Act 2020, Companies Act 2063, Cooperatives Act 2074) are as commonly taught and not checked against the Act text; the full revised BCA 156 syllabus page was seen only as a search excerpt; no Django screenshots this session (data schema unchanged, session 28 verification stands).

### BCA 151 Discrete Structure: NEW Unit 7 (audit against the TU BIT152 outline from hamronotes.com)
Gaps found by keyword grep (0 hits): vacuous/trivial/uniqueness proofs and mistakes in proofs, Boolean functions, n-ary relations and database operations, well-ordering, correctness of recursive algorithms, octal/hexadecimal and arithmetic algorithms, permutations with indistinguishable objects, next-permutation, random variables/expected value/variance/Bayes/randomized algorithms, graph models/tournaments/mixed graphs/isomorphism/matching/TSP.
- Unit 7 "Proof Pitfalls, Boolean Functions, Databases, Probability and Algorithms" (7.1k words): 7 sections, 14 executed Python blocks (output filled by `fill_script_outputs.py`: n^2+n+41 fails at 40 = 41 x 41, SUCCESS 420, MISSISSIPPI 34,650, next permutation after 362541 = 364125, E(two dice) = 7, V = 35/6, P(spam|prize) = 0.882, birthday 0.5073, TSP best 80), 2 figures (3-cube, matching), 19 exercises with answers (all hand answers re-checked), key facts, summary.
- PDF `NEBians-BCA-Course-Semester-2-Discrete-Structure.pdf`: `pdfinfo` **97 pages** (was 75), `qa_pdf.py` fails=0 (warns=331, same as before: 6 pt labels in old figures). Web data 7 units. Figures 7.1 and 7.2 inspected as PNG (ok).
- Honest gaps: `check_discrete.py` was not extended for Unit 7 (the numbers come from the embedded executed programs and hand re-checks); BCA 151 outline is assumed to equal BIT152 (the BCA 151 PDF was not retrievable); Unit 4 (number theory in the outline) lives in book Unit 6, and units 1 to 6 keep the original order.

### Web reader verified (Django :8765 + headless Chromium, screenshots inspected then deleted)
- BCA 105 Unit 3 and Unit 6: left rail lists the six textbook units, right rail has no "Formula and fact sheet" entry, no clipped labels, the "My School" and "The Necklace" readings and exercises render with proper headings and lists.
- BCA 156 Unit 7: seven units in the rail, tables and the worked-example callout render, right rail lists 7.1 to 7.9, Key facts, Summary, Practice, Model answers.
- BCA 151 Unit 7: executed code and output blocks, inline math (minterms, exponentials) and the rail all render. Minor: a 4-line rail label ("7.7 ... salesman problem") is clamped to 3 lines with an ellipsis (by design).

## Prioritised queue for the next session
1. Publish updated PDFs (`update_books.py --only <slug>`): 105, 156, 401, 451, 304, 305, 103, 354, 154, 405.
2. Keyword audits against live TU outlines still pending: 101/102/104, projects 256/306/356/404; BCA 353 (Miller-Rabin, Galois fields, HMAC, S/MIME, PGP, IPsec).
3. Electives BCA 406/453/454 (E-Commerce overlaps MIS Unit 10; Linux, Database Administration, DotNet, Software Testing) remain unwritten slots; deepen BCA 405.
4. BCA 153 split of collections and file handling; fix 5-6 pt labels in old figures; run `svgkit.lint` over all books.

## Session 30 results (BCA 102, 353 and 101 extended; BCA 105 and 104 left as-is)

Picked up from sessions 16-29 (this file; no duplicate tracker). Fresh sandbox `/home/user/sandbox`. Recipe: session-21 apt/venv/pip/`npm ci` line **plus `bash notes/pipeline/fonts/install.sh; fc-cache -f`** (without the fonts `qa_pdf.py` reports 2 FAILs "house font not embedded: Poppins/SourceSerif4" and page counts differ by about 3). Detached build and `export_course_web.py` worked unchanged.

### BCA 102 Programming in C: NEW Unit 8 (audit against the 10-unit TU outline on hamronotes.com)
Gaps (0 or 1 keyword hits before): preprocessor in depth (macros vs functions, `#`/`##`, `#elif`, `#undef`, `#pragma`), the build process, odd loop, comma operator, bit-fields, `argc/argv`, self-referential structures and linked list, table lookup, function pointers, lab work list.
- Unit 8 "The Preprocessor, the Build Process, Bit Operations and Linked Structures" (about 4k words, 8 sections), 10 complete C programs compiled and run (`fill_c_outputs.py`, `check_c_examples.py`: 10 programs, 0 problems), Figure 8.1 (build stages), lab checklist mapped to outline units 1-10, fact sheet, 17 practice items with answers, 3 model answers.
- PDF `NEBians-BCA-Course-Semester-1-Programming-in-C.pdf`: **103 -> 120 pp** (`pdfinfo`), `qa_pdf.py` fails=0 warns=251 (6 pt labels in old figures). Web data: 8 units, 49 topics. Figure page 105 inspected as PNG.
- Authoring lessons: `fill_c_outputs.py` does not feed stdin, so for programs with an ```input fence run it first, then add the input fence and hand-write the output after it (order must be c, input, output). `Fig.arrow` takes a list of points, not four coordinates. Do not put undefined-behaviour examples (`SQUARE(i++)`) in a program that is run; describe them in prose.
- BCA 104 Mathematics I checked: the book follows the revised linear-algebra/conics outline (not the old Indian "calculus" BCA-101 lists seen in search results); no change.
- Honest gaps: the revised BCA 102 syllabus PDF itself was not retrieved (the hamronotes list is the BIT sibling outline).

### BCA 353 Cryptography and Network Security: NEW Unit 8
Keyword audit: steganography 0 hits, malware/virus 7, intrusion 6, SNMP/SET none. Unit 8 (about 4k words, 7 sections): malware taxonomy and cases (Morris 1988, ILOVEYOU 2000, Stuxnet, WannaCry 2017), intruder classes, password arithmetic and salted slow hashing (executed Python), steganography and LSB embedding (executed, recovers "Hi"), watermarking, SNMP v1/v2c/v3, SET dual signature (Figure 8.1 plus executed hashlib demo), cyber law (Nepal Electronic Transactions Act 2063, Privacy Act 2075, flagged as "check the current text"), cloud/mobile/e-mail briefly, 12 practice items with answers, 2 model answers.
- PDF `NEBians-BCA-Course-Semester-6-Cryptography-and-Network-Security.pdf`: **93 -> 104 pp**, `qa_pdf.py` fails=0 warns=15. Web data 8 units. Figure page 99 inspected as PNG.
- Honest gaps: statute details and the 1988/2000/2017 case facts are from memory of well-known accounts; `check_crypto.py` not extended (outputs come from the embedded executed programs).

### BCA 101 Computer Fundamentals and Applications: NEW Unit 8 (laboratory applications)
The README said the practical half (word processor, spreadsheet, presentation, photo editing) was "not in the PDF"; the TU outline lists it explicitly. Keyword audit: goal seek, scenario manager, data table, amortisation, data validation, mail merge, dithering, interlaced, anti-aliasing all 0 hits. Unit 8 (about 5k words): word processor (styles, layout, tables, mail merge with executed demo, macros and macro-virus risk), spreadsheet (references, functions, templates, protection, charts, validation, loan amortisation, data table, goal seek, scenario manager, consolidation, database functions, pivot table), presentation, photo editing (bitmap vs vector figure, resolution, colour depth with executed size table, formats, lossy/lossless, interlaced, dithering, anti-aliasing, selections, layers), lab checklist, 12 practice items with answers, 2 model answers. All numbers from executed Python (PMT 11,122.22; total interest 167,333.43; pivot total 438,000).
- PDF `NEBians-BCA-Course-Semester-1-Computer-Fundamentals-and-Applications.pdf`: **152 -> 165 pp**, `qa_pdf.py` fails=0 warns=413 (old 6 pt figure labels). Web data 8 units. Figure page 156 inspected as PNG.
- Honest gaps: menu paths follow current Microsoft Office/LibreOffice names; no screenshots of the packages themselves (copyright-free captures were not prepared).

## Prioritised queue for the next session
1. Publish updated PDFs (`update_books.py --only <slug>`): 102, 105, 156, 401, 451, 304, 305, 103, 354, 154, 405.
2. Keyword audits still pending: projects 256/306/356/404 (BCA 101 done, session 30).
3. Electives BCA 406/453/454 remain unwritten slots; deepen BCA 405.
4. BCA 153 split of collections and file handling; fix 5-6 pt labels in old figures; run `svgkit.lint` over all books.

## Session 31 results (NEW elective book BCA 406 DotNet Technology; BCA 105 and the other done books left as-is)

Picked up from sessions 16-30 (this file; no duplicate tracker). Per the user: BCA 105 and the books after it are already done, so this session only extended the queue. Fresh sandbox `/home/user/sandbox`; the session-21 recipe worked (apt, venv `/tmp/v`, `npm ci`, fonts), plus `sudo apt-get install mono-mcs mono-runtime mono-devel libmono-system-data4.0-cil libmono-sqlite4.0-cil libmono-system-windows-forms4.0-cil libmono-system-drawing4.0-cil libmono-system-numerics4.0-cil libmono-system-core4.0-cil` for C#.

### BCA 406 DotNet Technology (Elective II): NEW book, was an unwritten slot
Source: TU CACS302 outline (notebahadur.com, edu-mate.com): U1 Introducing C# and the .NET Framework (7 h), U2 C# Language Basics (12 h), U3 Creating Types in C# (12 h), U4 Advanced C# (14 h). Every outline topic has its own section (README maps them).
- ~30k words, 4 units, 42 C# programs compiled with Mono `mcs` and 40 run by the NEW `bca/tools/fill_cs_outputs.py` (markers `// noexec`, `// compile-only`, `// stdin: ...`); ADO.NET programs run for real against in-memory SQLite (`Mono.Data.Sqlite`); a middleware-pipeline program built from delegates shows ASP.NET Core's pipeline order; 11 figures (heap and generations, compile/CLR flow, platform layers, type tree, class hierarchy, access matrix, generics, ADO.NET, MVC).
- PDF `bca/course/semester-7/pdfs/NEBians-BCA-Course-Semester-7-DotNet-Technology.pdf`: `pdfinfo` **120 pages**, `qa_pdf.py` **fails=0 warns=0**. Web data exported (`export_course_web.py semester-7/dotnet-technology`): 4 units, 47 topics, `index.json` entry added; `books.json`, `CURRICULUM.md` (row BCA 406 renamed), STATUS and READMEs regenerated with `gen_status.py` (44 books done).
- Pages inspected as PNG: contents, Fig 1.1 (the "freed" label overlapped the box edge, fixed), Fig 2.1, precedence table (escaped `\|` showed a backslash in the PDF, rewritten with words), Fig 3.1 (figure moved after the output so the page is no longer nearly empty), Fig 3.2, Fig 4.1, Fig 4.2.
- Mono limits (the reason for `// noexec`): C# 7 only, so no switch expressions, ranges, `??=`, records, top-level statements, local functions, `readonly struct` or default interface methods; SGen numbers GC generations differently, so the one GC demo (1.4) carries hand-written typical .NET output, labelled as such.
- Honest gaps: Windows Forms is compiled only; ASP.NET Core, EF Core and Web Forms code is `noexec` (no .NET SDK in the sandbox); .NET/C# version facts up to .NET 10 / C# 14 are stated from public release notes (check the current LTS); no Django screenshot of the new book (data exporter is the same as sessions 18-25); the lab list in 4.9 is mapped from the outline's laboratory paragraph, not from a printed college manual.

## Prioritised queue for the next session
1. Publish updated PDFs (`update_books.py --only <slug>` with server credentials): 105, 101, 102, 353, 304, 305, 103, 354, 154, 405, 406.
2. Electives still unwritten: BCA 453/454 (Elective III and IV) and the other Elective I/II options; Software Testing and QA, Database Administration, Linux are the next likely picks. Reuse `fill_cs_outputs.py`-style runners for code verification.
3. Keyword audits still pending: projects 256/306/356/404.
4. BCA 153 split of collections and file handling; fix 5-6 pt labels in old figures; run `svgkit.lint` over all books.
5. Deepen BCA 405 (SVM margin figure, XOR network, more numeric practice).

## Session 32 results (BCA 405 Machine Learning deepened; BCA 105 left as-is per the user)

Picked up from sessions 16-31 (this file; no duplicate tracker). Project root `/app`; the session-21 recipe worked unchanged (apt, venv `/tmp/v`, `npm ci`, fonts). BCA 105 and all books up to BCA 406 are done; BCA 105 PDF is still 151 pp in the repo (`pdfinfo`).

### BCA 405 Machine Learning: queue item "deepen" closed for Unit 2
- NEW Figure 2.2 (XOR as a two-layer network, step units OR/AND/output, weights and biases labelled) with a hand-built example and an executed truth table; NEW Figure 2.4 (SVM margin figure for the worked three-point example: boundary, margin lines, support vectors, margin 2.83); decision-tree figure renumbered 2.3.
- NEW one-step back-propagation example on a sigmoid unit (executed: z -0.5, yhat 0.3775, loss 0.1937, delta -0.1463, new w (0.5731, -0.3537), b 0.0731, yhat 0.4847; hand-checked); exercises 10 to 13 and model answers Q6 (XOR network), Q7 (back-prop step), Q8 (max-margin line for (2,2),(3,3) vs (0,0): w=(0.5,0.5), b=-1, margin 2.83).
- Fixed ugly numpy 2 repr (`np.float64(3.0)`) and `b = -1.9999999999999998` in the SVM program output.
- PDF `pdfinfo` **61 -> 63 pages**, `qa_pdf.py` fails=0 warns=0. Pages inspected as PNG: XOR figure (p20), SVM figure (p25); an orphan page was removed by tightening the model answers. Web data re-exported.

### Honest gaps
- Elective III and IV (BCA 453/454), Business Intelligence, Software Testing and QA, Data Visualization, Linux, DBA are still unwritten: no TU-specific outline text for them was found (search returned generic ISTQB/SPPU outlines), so no book was invented. Write them only after the outline is located.
- Project books (256/306/356/404): TU publishes no unit list, so there is no outline to audit against; they stay companion handbooks.
- Django web-reader screenshots were not retaken this session (only one book changed, same exporter).

## Prioritised queue for the next session
1. Publish updated PDFs with server credentials (`update_books.py --only <slug>`): 105, 101, 102, 353, 304, 305, 103, 354, 154, 405, 406.
2. Locate the TU outlines for the remaining electives (Elective I-IV lists in `CURRICULUM.md`) and write the most common ones.
3. BCA 153 split of collections/file handling; fix 5-6 pt labels in old figures; run `svgkit.lint` over all books; extend `check_mis.py`.
