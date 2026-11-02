# BCA Course — Tribhuvan University (revised 2082-batch curriculum)

<!-- COURSE-STATUS -->
## BCA course: real status

**9 of 42 subjects are written, built and QA-checked; 33 are not started.** Full per-subject table: [`STATUS.md`](STATUS.md). Done so far (102,864 words of study material):

| Sem | Code | Subject | Words | PDF pages | Status |
|---|---|---|---|---|---|
| 1 | BCA 101 | [Computer Fundamentals and Applications](semester-1/computer-fundamentals/) | 16,040 | 53 | done |
| 1 | BCA 102 | [Programming in C](semester-1/programming-in-c/) | 15,229 | 56 | done |
| 1 | BCA 103 | [Digital Logic](semester-1/digital-logic/) | 9,853 | 29 | done |
| 1 | BCA 104 | [Mathematics I](semester-1/mathematics-1/) | 11,443 | 33 | done |
| 1 | BCA 105 | [Professional Communication and Ethics](semester-1/professional-communication-ethics/) | 10,381 | 34 | done |
| 1 | BCA 106 | [Hardware Workshop](semester-1/hardware-workshop/) | 7,838 | 24 | done |
| 2 | BCA 151 | [Discrete Structure](semester-2/discrete-structure/) | 12,728 | 34 | done |
| 2 | BCA 153 | [OOP in Java](semester-2/oop-in-java/) | 10,096 | 41 | done |
| 2 | BCA 154 | [Mathematics II](semester-2/mathematics-2/) | 9,256 | 23 | done |

Everything else in `course/CURRICULUM.md` is mapped only (no notes). Nothing here has had a subject-teacher review.
<!-- /COURSE-STATUS -->


**Read this first: this is not yet the complete BCA course.** The programme has about 45 subject slots over 8 semesters. Two subject books, both in Semester I, are written in full. Everything else is mapped in [`CURRICULUM.md`](CURRICULUM.md) (verified list of subjects, codes, credits, electives, and a code map from the old 2074 curriculum) but has **no notes yet**. Nothing is padded to look finished.

## Written in full

| Sem | Subject | Units | Words | Verification | PDF |
|---|---|---|---|---|---|
| I | **Programming in C** (BCA 102 / CACS151) | 7 | 15087 | all 26 programs compiled and run, output diffed against the text | [`semester-1/pdfs/NEBians-BCA-Course-Semester-1-Programming-in-C.pdf`](semester-1/pdfs/) |
| I | **Digital Logic** (BCA 103 / CACS105) | 5 | 9676 | numbers, K-maps and FSM designs checked by script | [`semester-1/pdfs/NEBians-BCA-Course-Semester-1-Digital-Logic.pdf`](semester-1/pdfs/) |

Folder pattern: `semester-N/<subject>/unit-NN.md` (+ `README.md` with syllabus mapping and honesty notes), PDFs in `semester-N/pdfs/`. Every unit has a "what this gives you" box, worked examples, a formula and fact sheet, a chapter summary and a practice set with worked answers.

## Not yet written (next in priority order)

1. Semester I: Computer Fundamentals and Applications, Mathematics I, Professional Communication and Ethics, Hardware Workshop.
2. Semester II: Discrete Structure, Microprocessor and Computer Architecture, OOP in Java, Mathematics II, UX/UI Design, Principles of Management.
3. Semester III: Data Structure and Algorithms, DBMS, Web Technology I, System Analysis and Design, Probability and Statistics, Applied Economics.
4. Semesters IV–VIII: Operating Systems, Software Engineering, Numerical Methods, Python, Web Technology II, Computer Network, AI, Advanced Java, MIS, Society and Technology, Graphics, Mobile, Cryptography, Technical Writing, Distributed Systems, Cyber Security, Software Project Management, Financial Accounting, Cloud Computing, four electives; projects and internship (these have no notes by nature).

Mathematics I/II and Probability overlap the entrance Mathematics book (units 3–7, 11–13); students may use it as a bridge until those books exist.

## Documents

- [`CURRICULUM.md`](CURRICULUM.md): the full 8-semester map and the 2074 → 2082 code table.
- [`REVIEW_COURSE.md`](REVIEW_COURSE.md): what was reviewed, found and fixed.
- [`../SOURCES.md`](../SOURCES.md): sources and reliability.

## Tooling

`bca/tools/nebpdf.py` (Markdown → PDF through the house pipeline), `bca/tools/check_c_examples.py` (compile-and-diff every C example). The PDFs are ordinary committed files, not Git LFS.

## Status index (generated)

Every subject, its code, credits and real status is in [`STATUS.md`](STATUS.md). Short version: **2 subjects done** (Programming in C, Digital Logic), **1 in progress** (Computer Fundamentals and Applications — Unit 1 of 7, written to full depth and verified), the rest **missing**. The 39 remaining subjects were not written in the last session either; no subject is marked done unless every unit exists.

`books.json` is the registry `tools/nebpdf.py` reads; adding a subject = add its folder of `unit-NN.md` files and one line there.
