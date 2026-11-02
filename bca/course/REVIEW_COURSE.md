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
