# BCA Course — Tribhuvan University (revised 2082-batch curriculum)

<!-- COURSE-STATUS -->
## BCA course: real status

**25 of 44 subject slots are written, built and QA-checked; 11 core subjects are not started; 8 slots are projects, internship or electives with no notes planned.** Full per-subject table: [`STATUS.md`](STATUS.md). Done so far (378,308 raw words of study material, counted over the unit files, including code listings and tables):

| Sem | Code | Subject | Words | PDF pages | Status |
|---|---|---|---|---|---|
| 1 | BCA 101 | [Computer Fundamentals and Applications](semester-1/computer-fundamentals/) | 16,040 | 53 | done |
| 1 | BCA 102 | [Programming in C](semester-1/programming-in-c/) | 15,229 | 56 | done |
| 1 | BCA 103 | [Digital Logic](semester-1/digital-logic/) | 9,853 | 29 | done |
| 1 | BCA 104 | [Mathematics I](semester-1/mathematics-1/) | 11,443 | 33 | done |
| 1 | BCA 105 | [Professional Communication and Ethics](semester-1/professional-communication-ethics/) | 10,381 | 34 | done |
| 1 | BCA 106 | [Hardware Workshop](semester-1/hardware-workshop/) | 7,838 | 24 | done |
| 2 | BCA 151 | [Discrete Structure](semester-2/discrete-structure/) | 12,728 | 34 | done |
| 2 | BCA 152 | [Microprocessor and Computer Architecture](semester-2/microprocessor-computer-architecture/) | 25,282 | 76 | done |
| 2 | BCA 153 | [OOP in Java](semester-2/oop-in-java/) | 10,096 | 41 | done |
| 2 | BCA 154 | [Mathematics II](semester-2/mathematics-2/) | 9,256 | 23 | done |
| 2 | BCA 155 | [UX/UI Design](semester-2/ux-ui-design/) | 22,095 | 71 | done |
| 2 | BCA 156 | [Principles of Management](semester-2/principles-of-management/) | 15,475 | 50 | done |
| 3 | BCA 201 | [Data Structure and Algorithms](semester-3/data-structure-and-algorithms/) | 22,743 | 75 | done |
| 3 | BCA 202 | [Database Management System](semester-3/dbms/) | 15,156 | 56 | done |
| 3 | BCA 203 | [Web Technology I](semester-3/web-technology-1/) | 9,924 | 45 | done |
| 3 | BCA 204 | [System Analysis and Design](semester-3/system-analysis-and-design/) | 9,919 | 33 | done |
| 3 | BCA 205 | [Probability and Statistics](semester-3/probability-and-statistics/) | 9,323 | 30 | done |
| 3 | BCA 206 | [Applied Economics](semester-3/applied-economics/) | 11,390 | 34 | done |
| 4 | BCA 251 | [Operating Systems](semester-4/operating-systems/) | 27,698 | 85 | done |
| 4 | BCA 252 | [Software Engineering](semester-4/software-engineering/) | 16,608 | 54 | done |
| 4 | BCA 253 | [Numerical Methods](semester-4/numerical-methods/) | 14,925 | 43 | done |
| 4 | BCA 254 | [Python Programming](semester-4/python-programming/) | 15,321 | 79 | done |
| 4 | BCA 255 | [Web Technology II](semester-4/web-technology-2/) | 15,068 | 64 | done |
| 5 | BCA 301 | [Computer Network](semester-5/computer-networking/) | 23,727 | 65 | done |
| 5 | BCA 302 | [Artificial Intelligence](semester-5/artificial-intelligence/) | 20,790 | 59 | done |

Semesters I, II, III and IV are fully done (Semester IV's Project I is a project with no notes by nature). Everything else in `CURRICULUM.md` is mapped only (no notes). Nothing here has had a subject-teacher review.
<!-- /COURSE-STATUS -->


**Read this first: this is not yet the complete BCA course.** Semesters I and II (12 subjects) are written in full. Semesters III–VIII (24 core subjects) are mapped in [`CURRICULUM.md`](CURRICULUM.md) (verified list of subjects, codes, credits, electives, and a code map from the old 2074 curriculum) but have **no notes yet**; 8 further slots are projects, the internship and electives that are not taught from notes. Nothing is padded to look finished.

Folder pattern: `semester-N/<subject>/unit-NN.md` (+ `README.md` with syllabus mapping, verification and honesty notes), PDFs in `semester-N/pdfs/`. Every unit has a "what this gives you" box, worked examples, a formula and fact sheet, a chapter summary and a practice set with worked answers. Programming subjects have compiled-and-run programs; maths and theory subjects have numeric checkers in `../tools/` (`check_*.py`); Microprocessor and Computer Architecture has an 8085 assembler/simulator that runs every assembly program in the book.

## Next in priority order

1. Semester III: Data Structure and Algorithms, DBMS, Web Technology I, System Analysis and Design, Probability and Statistics, Applied Economics.
2. Semesters IV–VIII: Operating Systems, Software Engineering, Numerical Methods, Python, Web Technology II, Computer Network, AI, Advanced Java, MIS, Society and Technology, Graphics, Mobile, Cryptography, Technical Writing, Distributed Systems, Cyber Security, Software Project Management, Financial Accounting, Cloud Computing; then the electives, projects and internship guides.

Mathematics I/II and Probability overlap the entrance Mathematics book (units 3–7, 11–13); students may use it as a bridge until the Probability book exists.

## Documents

- [`CURRICULUM.md`](CURRICULUM.md): the full 8-semester map and the 2074 → 2082 code table.
- [`REVIEW_COURSE.md`](REVIEW_COURSE.md): what was reviewed, found and fixed.
- [`../SOURCES.md`](../SOURCES.md): sources and reliability.

## Tooling

`bca/tools/nebpdf.py` (Markdown → PDF through the house pipeline), `bca/tools/check_c_examples.py` (compile-and-diff every C example). The PDFs are ordinary committed files, not Git LFS.

## Status index (generated)

Every subject, its code, credits and real status is in [`STATUS.md`](STATUS.md), regenerated by `python3 tools/gen_status.py` (it also keeps the status block above and the "In this repo" column of `CURRICULUM.md` in step). `books.json` is the registry `tools/nebpdf.py` reads; adding a subject = add its folder of `unit-NN.md` files and one entry there.
