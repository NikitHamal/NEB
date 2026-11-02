# REVIEW_COURSE: review of the BCA course material

Scope: Semester I **Programming in C** (7 units) and **Digital Logic** (5 units), plus the curriculum map. Reviewed after writing, in two passes.

## What was reviewed and how

| Area | Method | Found | Fixed |
|---|---|---|---|
| C programs (26) | `check_c_examples.py`: compile with `gcc -std=c11 -Wall`, run, diff against printed output | **2 real defects**: unit 5 printed `11 21 31` but GCC evaluates call arguments right to left and prints `31 21 11`; unit 6 had a `printf` with `*p` and `*--p` whose output differed from my claim | Both rewritten so output is well-defined (separate statements), and the text now warns that argument evaluation order is unspecified |
| Predict-the-output answers in C units 2–4 | compiled each snippet and compared | answers agreed; **but** three answer keys contained visible self-corrections ("No: …", "? No spaces") | rewritten as clean explanations |
| Digital logic numbers | Python assertions: base conversions, 2's complement, overflow example, IEEE-754 of 10.5, Gray, Hamming (7,4) encode and decode | all correct | none needed |
| K-map answers | SymPy `SOPform` against the written simplifications, including don't-cares | all 5 correct | none needed |
| Counter and FSM designs | bit-level Python simulation of mod-3 JK, Gray D-counter, Johnson counter, "101" overlapping and non-overlapping detectors, "11" detector | all state sequences and outputs correct | none needed |
| Draft-like language | grep and reading | an unfinished sentence in unit 3 ("needs checking against the map"), a muddled decoder answer, a "Recompute" aside in the Hamming decode, contradictory flip-flop counts in the MOD-60 answer, an unsupported claim that TTL is faster than CMOS | each rewritten or removed |
| Curriculum map | two independent college pages for the 2082 curriculum, five pages for the 2074 one | agree on every subject and code listed | none; limitation noted below |
| PDFs | pdftotext scan for raw LaTeX, placeholders, stray `$`; visual inspection of rendered pages | no leaks; layout good | CSS and a placeholder-character bug fixed during the build |

## Limitations (no overclaiming)

- **2 of about 45 subjects are written.** The course is not complete. See `README.md` for what is next.
- The revised TU BCA curriculum PDF was not retrievable; subject lists rest on two cross-checked college pages, and the unit lists of C and Digital Logic rest on the older CACS and TU IOST syllabus PDFs.
- No marks distribution per unit and no TU past-question patterns for these two subjects were found in a primary source, so none is claimed.
- No diagrams: circuits and flowcharts are tables and ASCII.
- Not reviewed by a TU lecturer.

## Update — PDF pipeline and Computer Fundamentals Unit 1

- **Pipeline fixed.** The 6 PDFs committed earlier were built with a stand-alone WeasyPrint stylesheet (flat navy cover, no contents, no watermark, different fonts). All are rebuilt through the house pipeline (`notes/pipeline`), the same as CEE/IOE; checked with `tools/qa_pdf.py` (0 failures) and by eye on rendered pages.
- **Computer Fundamentals Unit 1** (≈3,100 words, 11 pp. PDF): every numeric answer was recomputed. **One wrong key was found and fixed in this pass** (Q13: 1 TB / 700 MB is 1497, not 1498 — 700 × 1498 overflows the disk).
- **Still not done:** Units 2–7 of Computer Fundamentals, the lab component of every subject, and 39 other subjects of the 42 in the revised curriculum (`STATUS.md`). Nothing here has had a subject-teacher review.


## Update — remaining-subject push

What each new subject covers, and where it is honest about limits.

- **Computer Fundamentals (BCA 101), units 2–7**: software and translators, algorithms/flowcharts; OS (scheduling, paging, booting; waits FCFS 7.25, SJF 6.25, RR 10.75 recomputed); DBMS with SQL run on SQLite; networks (Shannon, subnetting, OSI/TCP-IP); Internet/WWW; contemporary technologies. Limit: unit 7's TU sub-topic list was not confirmed; the lab (OS, word, spreadsheet, presentation, photo editing) is described but not taught step by step.
- **Mathematics I (BCA 104)**: single-variable calculus in six units (functions, limits, derivatives, applications, integration, differential equations). All answers checked in SymPy. **Unit division reconstructed; TU's own list not retrievable.**
- **Professional Communication and Ethics (BCA 105)**: communication process, listening/speaking/presentations, professional writing with models, teamwork and etiquette, ethics, IP, privacy and Nepal's cyber-law framework with four case studies. Limit: no code or numbers to verify beyond Flesch scores; legal section numbers/penalties deliberately omitted; structure reconstructed.
- **Hardware Workshop (BCA 106)**: safety, components with selection arithmetic, PC assembly, BIOS/UEFI and OS installation, troubleshooting, printers, T568B cabling. Limit: a lab subject; nothing was bench-tested; header layouts and beep codes vary by vendor.
- **Discrete Structure (BCA 151)**: logic and proofs, sets/relations/functions, counting, induction and recurrences, graphs and trees, number theory with RSA and groups. Every numeric answer recomputed by `check_discrete.py`. Limit: no formal languages/automata; structure reconstructed.
- **OOP in Java (BCA 153)**: 20 Java programs compiled and run on OpenJDK 17 with real output (the Swing and JDBC programs are compile-only). The checker caught two errors of mine: a wrong file-size in the first draft and a missing 42² = 1764 in a stream example; both fixed before the PDF was published. Limit: applets/RMI omitted as obsolete.
- **Mathematics II (BCA 154)**: matrices, linear systems, vector spaces, eigenvalues, 3-D vectors, checked in SymPy. Limit: **unit division reconstructed; syllabus extras (Fourier, vector calculus) not included.**

**Errors found in my own drafts during this pass** (all fixed before shipping): messy self-correcting answers in Discrete Structure Q1 and Mathematics I unit 6 Q3; a wrong expected output in OOP unit 5; three muddled sentences in Mathematics II. The first PDF of Computer Fundamentals was pushed with the wrong fonts because the sandbox lacked the house fonts and Python 3.12; it was rebuilt and re-pushed within the same session (QA showed fonts missing, then 0 failures).

**Not reviewed by a subject teacher. 33 of 42 subjects are still not written.**

## Session 3 additions (Semester II closed out)

**Microprocessor and Computer Architecture (BCA 152, 8 units).** Covers the 8085 (architecture, flags, pins, machine cycles and T-states, interrupts), its instruction set and 13 assembly programs, delay-loop timing with an exact formula, stack and subroutines, interfacing and the 8255; Mano's basic computer (registers, common bus, instruction set, fetch/decode/execute, interrupt cycle); hardwired vs microprogrammed control with Mano's FETCH/ADD/BRANCH/STORE/EXCHANGE microprograms; CPU organisation, addressing modes, RISC/CISC, Booth multiplication, restoring division, IEEE-754; I/O organisation and DMA; memory (address maps, disk, cache mapping and AMAT, virtual memory, page replacement, Belady's anomaly, protection); pipelining, vector processing, multiprocessors, Amdahl.
- *Verification:* `tools/check_mpca.py` (an 8085 assembler + simulator with real opcodes and T-states, 100 checks). It caught three of the author's own arithmetic slips (AMAT 4.5 not 4.4; effective access 20 ns not 19; a page-fault answer) before publication, and a reviewing pass found and fixed wrong F2/F3 micro-operation tables, a wrong 'indirect ADD takes 7 cycles' claim and a garbled nested-delay formula.
- *Gap/judgement:* the official BCA 152 PDF was not retrievable; the unit list comes from the 2074 CACS155 list plus the TU-style BIT151 syllabus, with I/O and memory given their own units. At about 25k raw words it is the longest book so far, because the syllabus is wide and the programs and traces are printed in full. The 8255 interfacing snippet was assembled but not executed. Microprogram routines for BRANCH and EXCHANGE follow Mano but were not run in a simulator.

**UX/UI Design (BCA 155, 8 units).** Follows the published eight-unit TU syllabus: UX vs UI and principles; research, personas, journey maps, ideation; interaction styles, Fitts and Hick with numbers; menus, windows and controls (the 12-hour unit); layout, colour with computed WCAG contrast, typography, responsive design, hierarchy and navigation models; wireframes, prototypes, storyboards and animation; evaluation (DECIDE, heuristics, SUS, KLM, sample size); VUI, dialog management, wearables.
- *Verification:* `tools/check_uxui.py` recomputes the numbers (contrast ratios, Fitts, Hick, SUS, KLM, Nielsen sample-size curve, type scales, grids, metrics). The Figma lab is described, not executed. Emoji and unusual glyphs were removed after checking the PDF fonts.
- *Judgement call:* the claim that Adobe XD is in maintenance mode reflects Adobe's 2023 announcement and may need updating.

**Principles of Management (BCA 156, 1 credit, 6 units).** Organisations and goals, management and Fayol; schools of thought and the environment (with Nepal examples); planning, MBO, SWOT, break-even, decision criteria and trees, critical path/PERT; organising (departmentalisation, span, delegation, structures); leading (leadership, groups, conflict, motivation, communication); control, TQM, Deming, Kaizen, Six Sigma, 5S, global context, Nepal trends.
- *Verification:* `tools/check_management.py` (46 numeric checks); it caught two of the author's slips (EVPI = 10, EOQ = 141).
- *Gap/judgement:* the revised 1-credit syllabus was not retrievable; the book is built from the older TU Introduction to Management / BIM outline and is longer than a 1-credit course strictly needs (the README says which units are core). One syllabus site returned unrelated spam when fetched and was not used beyond a search excerpt.

**Not done in this session:** Semesters III–VIII (24 core subjects), and the 8 project/internship/elective slots. No subject-teacher review of any book has happened.


---

## Session 5 review: Semester III

**Data Structure and Algorithms (BCA 201, 11 units).** All eleven CACS201 units: ADTs; stack with expression conversion and evaluation; queue (linear, circular, priority, deque); array list; linked lists (singly, doubly, circular, stack/queue); recursion with Hanoi and N-queens backtracking; trees (BST with all three deletion cases, AVL with all four rotations, B-tree by example, Huffman, minimax with alpha-beta); sorting with Big-O; searching and hashing; graphs (representations, Warshall, BFS/DFS, Kruskal, round-robin MST, Dijkstra, greedy); algorithm styles (P/NP, divide and conquer with the Master theorem, Amdahl, heuristic and approximate). *Verification:* 21 C programs compiled with gcc and run; outputs are real. The run caught one real mistake in the author's draft (a postfix evaluator that mishandled the two-digit operand 12), now fixed. *Judgement calls:* about 22,000 raw words, far above the 8–14k target, because the syllabus has eleven units and a lab list; no unit was padded but this is the one clear overrun. Three programs were split to avoid blank PDF pages. The syllabus's "Round-Robin algorithm" for minimum spanning trees is interpreted as the round-robin (Sollin-family) tree-merging method.

**Database Management System (BCA 202, 9 units).** E-R design and conversion, relational algebra, FD closure and 1NF–4NF, SQL DDL/DML, procedures, triggers, indexing, query cost with worked join-cost numbers, security (DAC, MAC, encryption, SQL injection), transactions, 2PL, deadlock, multiple granularity, timestamps. *Verification:* every SQL block executed on PostgreSQL 15 with real output, including real error messages; two explanations in the draft (atomicity of a failing procedure; savepoint rollback) were corrected after the real output contradicted them. *Judgement calls:* the syllabus names Oracle and SQL Server; executable code is PostgreSQL with comparison tables, so Oracle/MySQL syntax is not executed. Unit hours come from the bcapoint list; the older CACS255 list is the proxy.

**Web Technology I (BCA 203, 7 units).** Internet/HTTP/DNS, HTML5 with forms and SVG/canvas graphics, JavaScript (DOM, events, validation, regular expressions, promises), CSS (specificity, box model, Flexbox, Grid, media queries), XML (well-formedness, DTD, XSD, XSLT, XPath), jQuery, layout and design issues (contrast computed per WCAG, accessibility, performance, SEO). *Verification:* JS run with Node, jQuery run in jsdom, XML checked with xmllint (DTD example validated). *Gap:* unit hours were not found and are not printed; HTML/CSS/AJAX snippets were not rendered in a browser.

**System Analysis and Design (BCA 204, 5 units).** SDLC and process models, agile/XP, CASE, SOA, OOAD, acquisition, project scheduling (CPM/PERT worked), planning and feasibility (NPV, ROI, payback, BCR, IRR worked), requirements methods, DFDs with rules and balancing, decision tables, E-R/supertypes/business rules/patterns, database and physical design, forms/reports/interfaces, implementation, testing, installation, maintenance. *Verification:* every number recomputed in Python. *Judgement call:* diagrams are described, not drawn; the syllabus follows Valacich et al., and the text is original but follows that order.

**Probability and Statistics (BCA 205, 7 units).** Data and sources, descriptive statistics (raw and grouped), correlation and regression by least squares, probability laws, Bayes, binomial/Poisson/normal, sample survey, SRS/stratified/systematic/cluster/multistage/PPS/ratio estimation, z/t/χ², ANOVA one- and two-way. *Verification:* `tools/check_stats.py` recomputes all worked and practice numbers with NumPy/SciPy. The check caught two author slips (a two-way ANOVA data set with zero error, which was replaced, and a wrong z in a checking script). *Gap:* the SPSS laboratory is not reproduced; stratified ratio estimators are mentioned, not derived.

**Applied Economics (BCA 206, 7 units).** PPF and opportunity cost, demand and supply with tax incidence, all elasticity measures, cardinal and ordinal consumer theory with a Hicksian decomposition, cost and revenue curves, perfect competition, monopoly, price discrimination, monopolistic competition, oligopoly and cartels, national income accounts, money, inflation, banking, NRB, balance of trade and payments. *Verification:* `tools/check_economics.py` recomputes every number. *Judgement call:* the revised subject is 2 credits but the retrievable syllabus is the 3-credit CAEC353 text; the 3-credit unit list is used and flagged. Nepal-specific statements are limited to stable facts, no current statistics.

**Process notes.** The repository clone needed authentication (an unauthenticated clone failed), so the supplied token was passed through a `GIT_ASKPASS` helper reading an environment variable; it is in no file and not in `.git/config`. A grep of tracked files for the token pattern returned nothing before the final push.
