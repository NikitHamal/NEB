# CHANGELOG — BCA course

## Session 3: remaining subjects, Semester II onward (running log)

**Finished this session (each pushed on its own):**

- Semester 2 · BCA 152 · Microprocessor and Computer Architecture: 24,493 raw words (units only; includes code listings and tables), 76 PDF pages, 8 units, QA 0 failures (1 soft warning: a short page at the end of the contents). 13 assembly programs assembled and executed on the 8085 simulator in `tools/check_mpca.py`, which also recomputes Booth, division, IEEE-754, pipeline, cache, paging, disk and Amdahl numbers (100 checks, all pass).
- Semester 2 · BCA 155 · UX/UI Design: 21,732 raw words (units only), 71 PDF pages, 8 units, QA 0 failures (3 soft warnings: short pages at the end of the contents and of two chapters). Theory subject: `tools/check_uxui.py` recomputes 36 numbers (WCAG contrast, Fitts, Hick, SUS, KLM, sample size, type scales, grids).

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

- Semester 2 · BCA 156 · Principles of Management
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
