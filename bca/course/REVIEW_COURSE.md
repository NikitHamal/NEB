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
- **Still not done:** Units 2–7 of Computer Fundamentals, the lab component of every subject, and ~43 other subjects (`STATUS.md`). Nothing here has had a subject-teacher review.
