# Sources and how far each can be trusted

| Fact | Source | Reliability |
|---|---|---|
| Entrance pattern: 100 MCQs, 100 marks, 40 English / 50 Maths / 10 GK | edusanjal.com BCA-TU entrance page (reproduces the TU FOHSS notice); hamrocsit.com (June 2026); educatenepal.com; Dean's Office model questions mirrored by divyagyan.edu.np | High for the split and total. **Pass mark (35 vs 40), negative marking and per-chapter counts are unconfirmed** |
| 2083 entrance date 16 Aug 2026, application window 29 Jun – 14 Aug 2026 | edusanjal.com notice listing | Medium (secondary page quoting TU) |
| Eligibility (D and CGPA 1.8 for Grade 12 passed 2079 BS or later; D+ and 2.0 earlier) | educatenepal.com (Jul 2025); thamescollege.edu.np; insightsnp.com (older rule) | Medium |
| Revised BCA curriculum, 2082 batch: semester-wise subjects, codes, credits, electives, 4 projects + internship | texasintl.edu.np (Sept 2026), davcollege.edu.np (Jul 2026), cross-read | Medium: two independent college pages agree, **TU's revised PDF was not retrieved** |
| Old 2074 curriculum (CACS/CAxx codes, 126 credits) | bcanepaltu.com, nplupdates.com, insightsnp.com, divyagyan.edu.np, texasintl.edu.np | High: five pages agree |
| Digital Logic unit list (CACS105) | benchpartner.com, notebahadur.com, neporesult.com micro-syllabus | High for the old code; the new BCA 103 assumed equivalent |
| C Programming unit list | TU IOST "C Programming" and TU B.Math.Sc. BMS 103 syllabus PDFs on portal.tu.edu.np (units: Introduction, Elements, I/O, Control, Arrays/Strings, Functions, Pointers, Structure/Union, File Handling) | High for the TU C family; BCA's own PDF not retrieved |
| Prime Minister / election 2026 | Reuters via NBC News, Tribune (27 Mar 2026) | High |
| Technical content of the course books | written from standard computer-science knowledge; **machine-verified** where possible (26 C programs compiled and run with gcc 12 -Wall; number-system results with Python; K-map minimisation with SymPy; counter and FSM designs by bit-level simulation) | Verified where stated in each subject README; prose explanations are not machine-checkable |

No textbook or paid material was copied. Examples, questions and explanations are original.

## Computer Fundamentals and Applications (BCA 101 / CACS101)

Unit list and hours (16, 3, 4, 8, 10, 6, 13 = 60 theory hours; labs: OS, word processor, spreadsheet, presentation, photo editing) cross-read on four independent syllabus transcriptions of the **2074** CACS101 syllabus — esikhcha.com (Feb 2025), bcastudynepal.blogspot.com (2019), benchpartner.com, notebahadur.com. **Not verified:** the revised 2082-batch BCA 101 outline; it may differ in unit order or content, and TU's own syllabus PDF was not retrieved. The CACS101 textbook cited by those pages is Peter Norton, *Introduction to Computers*, 7th ed. Facts in Unit 1 (generations, memory sizes and speeds, USB/SATA rates) are standard textbook values; speeds and capacities in the hierarchy table are typical ranges, labelled as such.
IOE exam pattern and eligibility (used in `ioe/`): IOE admission page and 2083/84 notice as quoted by collegenp.com, edusanjal.com, icenepal.com (Jun–Aug 2026).


## Update — sources for the subjects written in the remaining-subject push

The revised (2082-batch) per-subject syllabus PDFs could not be retrieved. Sources actually consulted: bcapoint.com and notebahadur.com first-semester pages (subject names, credits, CACS101 unit list), esikhcha.com/benchpartner.com transcriptions (CACS101 hours 16/3/4/8/10/6/13), and standard textbooks for content (Norton, *Introduction to Computers*; Rosen, *Discrete Mathematics and Its Applications*; Strang, *Introduction to Linear Algebra*; Stewart, *Calculus*; Sommerville, *Software Engineering*; the ACM Code of Ethics 2018; CompTIA A+ troubleshooting method). For BCA 104, 105, 106, 151, 153 and 154 the **unit structure is a reconstruction** from subject titles and the usual content of the old CACS equivalents; each subject README says so. Nepali legal references (ETA 2063, Copyright Act 2059, Privacy Act 2075, Muluki Criminal Code 2074) are cited by title and year only.

## BCA 152 Microprocessor and Computer Architecture (session 3)
- https://bcastudynepal.blogspot.com/2019/02/microprocessor-and-computer-architecture.html : TU BCA CACS155 (2074) unit list: fundamentals of microprocessor, 8085 instruction set, counters/delay/interfacing, basic computer architecture, microprogrammed control, CPU, pipeline/vector/multiprocessors.
- https://www.cdcsit.edu.np/wp-content/uploads/2021/06/Microprocessor-and-Computer-Architecture-BIT151.pdf : TU-style BIT151 syllabus (8 units incl. I/O organisation, DMA, memory organisation, cache, virtual memory, RISC/CISC, Flynn's classification, pipelining). The PDF text could not be fully extracted; unit titles were read from the search excerpt. The official BCA 152 PDF itself was not retrievable.
- Reference texts followed for worked examples: M. Morris Mano, Computer System Architecture; R. Gaonkar, Microprocessor Architecture, Programming and Applications with the 8085.
