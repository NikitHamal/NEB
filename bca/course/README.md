# BCA Course — Tribhuvan University (revised 2082-batch curriculum)

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

`bca/tools/build_pdfs.py` (Markdown → PDF with WeasyPrint), `bca/tools/check_c_examples.py` (compile-and-diff every C example). The PDFs are ordinary committed files, not Git LFS.
