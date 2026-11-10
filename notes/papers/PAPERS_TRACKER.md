# Engineering Past Papers - Research Tracker (read this first)

Branch: `claude/engineering` (from `main`). Raw files + manifests live in `notes/papers/engineering/` (see its README.md; per-collection counts in INVENTORY.md).
Phase 1 (research + download) is DONE for the sources below. Phase 2 (extract/normalise/author app content) has NOT started.

## A. Collected (status DONE unless noted)
| # | University / body | Source | What / coverage | Dest under `engineering/sources/` | Manifest |
|---|---|---|---|---|---|
| 1 | TU IOE | tu.edu.np / ioe.tu.edu.np curricula | 462 syllabus PDFs, all 12+ programs, new curriculum | tu-ioe/curriculum | tu-ioe-curriculum |
| 2 | TU IOE | subeshyadav.com.np (Drive) | past Qs BAE/BCE/BCT/BEE/BEX/BGE/BArch/BAG sem1-8 (94) + extra ~89 from the big Drive folder (deduped) | tu-ioe/past-questions, tu-ioe/past-questions-subesh | tu-ioe-pastq-subeshyadav, agg-subesh-ioe |
| 3 | TU IOE | bani.com.np/ioe-question-collection | 257 papers (New+Old course) sem 1-8 + Elective I/II/III; 192 Drive + 65 SharePoint (1 SP link dead) | tu-ioe/past-questions-bani | agg-bani-ioe |
| 4 | TU IOE | ioeqnbank.ngp.com.np | 9 unique papers after dedupe | tu-ioe/ioeqnbank | agg-ioeqnbank |
| 5 | TU IOE | GitHub waraunika PYQ 5th/6th, ProJ-Yeet PYQ 7th, itsbhupesh00 os-ioe, iamshishirgaire syllabus data, xpsaroj/ioe-drive (index only) | sorted PYQs sem5-7 BEI/BCT/BEX | github/* | github-repos, github-repos-2 |
| 6 | Pokhara Univ (PU/POU) | Drive collection via wapnepal | BE old questions 2005-2015 all branches (1033 doc/docx) + new-syllabus BE Computer/Software sem1-4 | pokhara-university/* | pokhara-university |
| 7 | Pokhara Univ | github ujjwalnp (Ultimate-Notes... "BE Old questions") | Final/UT/Assessment questions sem 1-8 (~1800 docs, 260 dups removed) | github/ujjwalnp__PU-BE-Old-questions | github-ujjwalnp-pu |
| 8 | Pokhara Univ | GitHub pujandhakal, pramesh61, Just-Binod, harmless-beep, pranit-mishra, adhikari-arpan, ujjwalnp cpp-old-question-solution | BESE / BECE / BE Comp notes + PYQs | github/* | github-repos(-2) |
| 9 | Pokhara Univ | hamro-sathi.blogspot.com | 2003-2009 BE questions (docs) | pokhara-university/hamro-sathi | misc-pu-pokhara-entrance |
| 10 | Purbanchal Univ | entrance.puexam.edu.np, thearyanschool.edu.np | BE entrance model Q 2079; BE Civil semester model Qs 2022-23 | purbanchal-university/* | misc-pu-pokhara-entrance |
| 11 | Purbanchal Univ | GitHub Prashznt (CE syllabus), studywithnpandey-commits/puexam | syllabus + 2 PDFs | github/* | github-repos(-2) |
| 12 | Kathmandu Univ | seee.ku.edu.np Drive folder | 13 old-question/question-bank files (COMP116, MATH104, PHYS102, ENGG112, ENVE101, ENGT105, SEEE I-II 2019/2022) | kathmandu-university/seee-study-resources | ku-seee |
| 13 | IOE entrance | ndds.com.np, bpooja.com.np | model Qs 2080 + syllabus; 2073-2077 sets (a few links) | ndds-ioe-entrance, ioe-entrance | agg-ndds, misc-* |
| 14 | NEC licence | GitHub SamirWagle/NECPrep (1,380 Qs, JSON/MD), Abhishek-Gubhaju civil, Sandesh3769 | question banks as data | github/* | github-repos-2 |
| 15 | CTEVT | ctevtnepal.blogspot, dhanraj.com.np | HTML dumps only (PDF links are inline images) | ctevt/* | - |

## B. Tried and FAILED / blocked (do not retry blindly)
- ioe.promod.com.np (Purbanchal Q banks Civil/Computer, IOE entrance solutions): PDFs on `blog.promod.com.np/pdf/...` host is dead; Wayback gave 429 / no snapshot (`agg-promod*.jsonl`). Retry with `wayback_fetch.py` + 20 s sleeps only if desperate.
- ioenotes.edu.np "Questions collection all semester" (Civil/Computer/Electronics): Drive ids 404 / not file.
- ravidhami.com (Pokhara civil 2016-2019), sudipkhadka.com.np (PU civil), ervivekshah.com.np (links = `#`): hosts unreachable or links empty.
- meroenotes.com PU BE civil/computer 2023-2025: page says "contact us for PDF" - no files. Studocu/Scribd/CourseHero: login walled.
- KU seee.ku.edu.np: all 8 semester buttons point to the SAME Drive folder (gdown lists ~255 items, only the 13 question files were kept).

## C. LEADS not yet downloaded (next research session starts here)
1. **Lok Sewa / PSC engineering** (civil, electrical, computer, mechanical) old papers - NOT searched yet (psc.gov.np, lokseva sites). Highest-value gap.
2. IOE entrance past sets 2073-2081: Everest "Success Entrance Book" (researchgate), scribd sets (login), ioe.edu.np/entrance notices; collect only direct PDFs.
3. NEC licence past papers: quicknec.com, neclicenseexam.vercel.app/past-questions, ezexplanation.com/nec, bctengineeringnotes.blogspot.com/2023/04/nepal-engineering-council.html, reddit r/IOENepal Drive ids `1t8idOPgAGocvj8SVWghZYoxjpyNfN2H4`, doc `1mgFMar9-K63ynvWYRnbHRfCsUNKDS1erGzXklhMoRrM`.
4. KU: civilfornepal.com/topic/4-1st-semester-... Drive folder `1xH0q73tYO5LtzRJH1TUUF3kO5F7CQcNI` (sem1 ALL-IN-ONE), sem2 page (topic/7), cdn.ku.edu.np syllabus tokens.
5. CTEVT diploma (Civil/Computer/Electrical/IT/Geomatics/Hydropower): ctevtnote.com/p/engineering.html (sub-pages), ctevtnepal.blogspot.com per-subject posts (PDFs inside Drive), rohitks77.com.np, saysaathi.blogspot.com, dhanraj.com.np (per-year question posts 2071-2077).
6. IOE extras: importantedunotes.com model questions (I/I, I/II new syllabus 2082), ioenotes.bikrampparajuli.com.np, official ioe.tu.edu.np exam pages (exam.ioe.edu.np), TU `portal.tu.edu.np/downloads` year-wise.
7. PU: puexam.edu.np official (entrance + exam notices), suzanwrites.blogspot.com PU BE Civil/Computer (Drive buttons are JS), PU new-syllabus 2018+ Qs on studocu (blocked).
8. Other universities not yet touched: Far Western Univ, Mid-West Univ, Lumbini Technical Univ, Nepal Open Univ, Madan Bhandari (MBMU) - check for engineering past Qs.
9. GitHub repos NOT yet cloned: ujjwalnp/WT-old-question-solution, Devrawatsuresh/C-Programs-, roshanbhatt420/OLDWTQUESTIONS, pratikkhatri574/CPP_BIT_II_PU (all tiny, Pokhara solutions), ABChapagain/mca-pu (336 MB, MCA not BE), BijayaKhadka0/MIT (master's IT, 26 MB), gautamsudip/NEC_Exam_Preparation_App (40 MB), the008killer/VHDL-Embedded-System.
10. Sorted-by-subject duplicates exist between sources 2/3/4 (same IOE paper from several aggregators) - dedupe by text hash in Phase 2, not only file sha.

## D. Phase 2 plan (the "work")
1. Run `tools/inventory.py`; make a subject->paper index (program, semester, subject, year, course new/old) from file/folder names + first-page text (`pymupdf`).
2. OCR scanned PDFs lacking a text layer (many IOE ones are image scans) - tesseract not installed in the research sandbox; install it or use cloud OCR.
3. Convert .doc/.docx (Pokhara, ~2500 files) with LibreOffice/pandoc; build per-subject question JSON for the app.
4. Prefer official TU curricula (source 1) as the subject master list; map papers to it.

## E. GitHub lead scan results (auto, `HAVE` = already in repo)
| repo | size | stars | status | description |
|---|---|---|---|---|
| waraunika/PYQ-5th-sem | 25 MB | 7 | HAVE | Past year questions of IoE, TU (Nepal) organized, and documented throu |
| shivajichalise/malp | 0 MB | 6 | new | ALP solutions of old Pokhara University Questions |
| ABChapagain/mca-pu | 336 MB | 6 | new | Open-source collection of MCA (Purbanchal University) learning materia |
| waraunika/PYQ-6th-sem | 162 MB | 3 | HAVE | This is a collection of sorted past year questions (PYQs) for BEI cour |
| ujjwalnp/cpp-old-question-solution | 53 MB | 2 | new | The solution of all coding questions asked in Pokhara University from  |
| SamirWagle/NECPrep | 2 MB | 2 | new | Open-source NEC license exam preparation with 1,380+ questions, mock t |
| xpsaroj/ioe-drive | 1 MB | 1 | new | A collaborative platform for IOE (Institute of Engineering, Nepal) stu |
| ProJ-Yeet/PYQ-7th-sem | 786 MB | 1 | HAVE | Sorted past-year questions (PYQ) for IOE 7th semester: AI, DSAP, O&M,  |
| aakrity17/Web_Tech_5th_sem_Old_Questions_Solved | 0 MB | 1 | new | During the fifth semester of BCA(Pokhara University), I attempted to s |
| tech-noob/ioe-hub-files | 0 MB | 0 | new | Repo for past questions and notes |
| the008killer/VHDL-Embedded-System | 0 MB | 0 | new | This repo includes the solution of past IOE questions related to VHDL. |
| itsbhupesh00/os-ioe | 32 MB | 0 | HAVE | Interactive IOE Operating System (OS) past exam question bank with cha |
| sulav789/ExamGen | 1 MB | 0 | new | NEBPrep is a free exam preparation platform for Nepal's Grade 11 and 1 |
| ujjwalnp/WT-old-question-solution | 0 MB | 0 | new | A Github repo of solved past year questions for "Web Technology" under |
| Devrawatsuresh/C-Programs- | 0 MB | 0 | new | Pokhara University exam old question solution and extra question solut |
| roshanbhatt420/OLDWTQUESTIONS | 0 MB | 0 | new | Everyone this is repo of solved question of the Pokhara University of  |
| BijayaKhadka0/MIT | 25 MB | 0 | new | Past Questions / Old Questions papers of MIT (Master of Information Te |
| studywithnpandey-commits/puexam | 2 MB | 0 | new | Purbanchal university for old questions, note and other study material |
| pratikkhatri574/CPP_BIT_II_PU | 0 MB | 0 | new | C Plus Plus (C++) notes and Old Question solutions based on the syllab |
| antimashrestha31/E-Learning-Web-Application | 65 MB | 0 | new | This project on E-Learning entitled PUgyancenter is a web-based platfo |
| Sandesh3769/NEC-License-Exam-Portal | 0 MB | 0 | new | Engineering license preparation questions mcq with detailed explanatio |
| gautamsudip/NEC_Exam_Preparation_App | 40 MB | 0 | new | 🚀 NEC Quiz App – A simple quiz app to help you prepare for the Nepal E |
| Abhishek-Gubhaju/nec-civil-civil-rural-license-prep | 2 MB | 0 | new | Nepal Engineering Council (NEC) licence exam preparation for Civil and |
## F. Phase 2 progress (see `engineering/PHASE2_STATUS.md`)
- Catalog built: `engineering/catalog.json`, `catalog-tree.json`, `CATALOG.md` (4,086 papers indexed).
- Typeset + fully solved (`engineering/content/*.md` -> `engineering/pdf/`), 27 papers (session 5 added Numerical Methods ENSH 202 x3 [2082 Chaitra, 2082 Kartik, 2081 Chaitra] and Probability and Statistics ENSH 253 x2 [2083 Baishakh, 2082 Bhadra]); first 22:
  - IOE Engineering Mathematics I: 2081 Baishakh (SH 101), 2081 Kartik (SH 101), 2081 Chaitra (ENSH 101).
  - IOE Engineering Mathematics II: 2081 Ashwin (SH 151), 2082 Bhadra (ENSH 151), 2083 Baishakh (ENSH 151).
  - IOE Engineering Physics: 2081 Baishakh (SH 102), 2081 Chaitra (ENSH 102); Part II: 2081 Ashwin (SH 152), 2082 Baishakh (SH 152, back), 2082 Bhadra (ENSH 152), 2083 Baishakh (ENSH 152, back).
  - IOE Engineering Chemistry: 2081 Baishakh (SH 103), 2081 Kartik (SH 103, back), 2081 Chaitra (ENSH 103); Part II: 2081 Ashwin (SH 153), 2082 Baishakh (SH 153, back), 2082 Bhadra (ENSH 153), 2083 Baishakh (ENSH 153, back).
  - IOE Engineering Mathematics III: 2081 Chaitra, 2082 Kartik (back), 2082 Chaitra (ENSH 201).
- Bundles (`engineering/bundle_engineering.py` -> `engineering/pdf/bundles/`): `engineering-mathematics-i-2081.pdf`, `engineering-mathematics-ii-2081-2083.pdf`, `engineering-mathematics-iii-2081-2082.pdf`, `engineering-physics-2081-2083.pdf`, `engineering-chemistry-2081-2083.pdf`, `engineering-numerical-methods-2081-2082.pdf`, `engineering-probability-and-statistics-2082-2083.pdf`, `NEBians-Engineering-All-In-One-Book.pdf` (master, 27 papers / 366 pp, regenerated on every run).
- Next: see "Next paper candidates" in `engineering/PHASE2_STATUS.md` (Basic Electrical and Electronics, Engineering Mechanics, Fluid Mechanics, Hydraulics, Soil Mechanics, ...).
- Session 6: Basic Electrical and Electronics Engineering (IOE 1st sem) 2081 Baishakh, Kartik, Chaitra typeset with full solutions. New bundle `engineering-basic-electrical-and-electronics-engineering-2081.pdf`; master All-in-One 30 papers / 408 pp. Circuit-drawing helpers added in `notes/pipeline/ckt.py`.
- Session 7: Fundamental of Electrical and Electronics Engineering (EX/ENEX 101) 2081 Baishakh and 2081 Chaitra typeset with full solutions. New bundle `engineering-fundamental-of-electrical-and-electronics-engineering-2081.pdf`; master All-in-One 32 papers / 448 pp.
- Session 7b: Engineering Geology I (IOE 1st sem, BCE; CE 102 / ENCE 102) 2081 Baishakh, Kartik (back) and Chaitra typeset with full solutions. New bundle `engineering-geology-i-2081.pdf`; master All-in-One 35 papers / 483 pp.
- Session 7c: Object Oriented Programming (ENCT 151) 2083 Baishakh (back) and 2082 Bhadra typeset with full solutions and compiled C++ programs. New bundle `engineering-object-oriented-programming-2082-2083.pdf`; master All-in-One 37 papers. Remaining OOP papers (2082 Baishakh, 2081 Ashwin) are next.
- Session 8: Object Oriented Programming CT 151 2082 Baishakh (back) and 2081 Ashwin (regular, 2080 batch) added; OOP bundle `engineering-object-oriented-programming-2081-2083.pdf` (4 papers); master All-in-One now 39 papers / 544 pp. Next: 2nd-sem Electrical Circuits and Machines, Electronic Device and Circuits, Strength of Materials, Survey I (see PHASE2_STATUS.md).
- Session 8b: Strength of Materials ENCE 151 2082 Bhadra and CE 151 2081 Ashwin added; bundle `engineering-strength-of-materials-2081-2082.pdf`; master All-in-One now 41 papers / 579 pp. Next: 2nd-sem Electrical Circuits and Machines, Electronic Device and Circuits, Survey I.
- Session 9: Digital Logic (ENEX/EX 152) 2083 Baishakh (back), 2082 Bhadra, 2082 Baishakh (back) and 2081 Ashwin typeset with full solutions (K-maps, auto-drawn circuits, timing diagrams, state machines). New bundle `engineering-digital-logic-2081-2083.pdf`; master All-in-One now 45 papers / 642 pp. Next: Electrical Circuits and Machines, Electronic Device and Circuits, Advanced Computer Programming, Survey I, Engineering Mechanics, Fluid Mechanics, Hydraulics, Soil Mechanics (see `engineering/PHASE2_STATUS.md`).
- Session 9b: Advanced Computer Programming (ENCT 153) 2083 Baishakh (back) typeset with executed Python solutions; bundle `engineering-advanced-computer-programming-2083.pdf`; master All-in-One now 46 papers. Next: pages 2-4 of the same ACP scan (3 more papers).
- Session 10: Advanced Computer Programming ENCT/CT 153 2082 Bhadra, 2082 Baishakh (back) and 2081 Ashwin (2080 batch) added with executed Python solutions; ACP bundle `engineering-advanced-computer-programming-2081-2083.pdf` (4 papers); master All-in-One now 49 papers / 689 pp. Next: Electrical Circuits and Machines, Electronic Device and Circuits, Survey I, Engineering Mechanics, Fluid Mechanics (see PHASE2_STATUS.md).
- Session 10b: Electronic Device and Circuits (ENEX/EX 151) 2083 Baishakh (back), 2082 Bhadra, 2082 Baishakh (back) and 2081 Ashwin typeset with full solutions, 26 circuit/characteristic figures and Python-solved numerics; bundle `engineering-electronic-device-and-circuits-2081-2083.pdf`; master All-in-One now 53 papers. Next: Electrical Circuits and Machines, Survey I, Engineering Mechanics, Fluid Mechanics (see PHASE2_STATUS.md).
- Session 11: Electric Circuits and Machines (EE 460) 2081 Chaitra (back) and 2080 Chaitra (regular) typeset with full solutions; bundle `engineering-electric-circuits-and-machines-2080-2081.pdf`; master All-in-One 55 papers / 777 pp. Four more ECM sittings remain in the same scan (2079 Chaitra p5-6, p7-p12 unread).
- Session 11b: Electric Circuits and Machines (EE 460) 2079 Chaitra added (3 ECM papers now); bundle `engineering-electric-circuits-and-machines-2079-2081.pdf` replaces the 2080-2081 file; master All-in-One 56 papers / 790 pp. ECM scan pages p7-p12 (three more sittings) still unread.
- Session 11c: ECM EE 460 2078 Chaitra added (4 ECM papers); bundle `engineering-electric-circuits-and-machines-2078-2081.pdf`; ECM scan p7-p8 duplicate p5-p6; only p11-p12 remain unread.
- Session 12: Electric Circuits and Machines (EE 460) 2077 Chaitra added, ECM complete (5 papers); bundle `engineering-electric-circuits-and-machines-2077-2081.pdf`; master All-in-One 58 papers / 818 pp.
- Session 12b: Operating System (ENCT 254, BCT 4th sem) 2083 Baishakh (back) and 2082 Bhadra typeset with full solutions (Gantt charts, Banker's, page replacement); bundle `engineering-operating-system-2082-2083.pdf`; master All-in-One now 60 papers.
- Session 12c: Discrete Structure (ENCT 251) 2083 Baishakh (back) typeset with full solutions (13 questions, graph/automata figures, Prim, max flow); no subject bundle yet (needs a second sitting); master All-in-One 61 papers. Scan p3-p4 (another sitting) next.
- Session 13: Discrete Structure (ENCT 251) 2082 Bhadra (regular) added; Discrete Structure complete (2 papers); bundle `engineering-discrete-structure-2082-2083.pdf`; master All-in-One 62 papers / 875 pp. Next: DSA, Computer Organization, Electromagnetics (see PHASE2_STATUS.md).
- Session 13b: Data Structure and Algorithm (ENCT 252) 2083 Baishakh (back) and 2082 Bhadra (regular) added with compiled C programs, AVL/B-tree/heap/hash/graph figures; bundle `engineering-data-structure-and-algorithm-2082-2083.pdf`; master All-in-One 64 papers.
- Session 13c: Computer Organization and Architecture (ENEX 253) 2083 Baishakh (back) and 2082 Bhadra (regular) added with Booth traces, cache/page-replacement traces and 8 block diagrams; bundle `engineering-computer-organization-and-architecture-2082-2083.pdf`; master All-in-One 66 papers.

- Session 14: IOE Electromagnetics ENEX 254 (2083 Baishakh, 2082 Bhadra) and Control System ENEE 251 (2083 Baishakh, 2082 Bhadra) solved and bundled; master All-in-One book now 70 papers. See `engineering/PHASE2_STATUS.md`.
- Session 15: Microprocessors and Microcontrollers (ENEX 251) 2083 Baishakh (back) and 2082 Bhadra (regular) solved (8085/8086/8051 programs verified on a simulator, decoder and timing figures); bundle `engineering-microprocessors-and-microcontrollers-2082-2083.pdf`; master All-in-One 72 papers / 1021 pp. Scope rule: only the last 4-5 years of official papers. See `engineering/PHASE2_STATUS.md`.
- Session 15b: Data Communication (ENCT 253) 2083 Baishakh (back) and 2082 Bhadra (regular) solved with computed Shannon-Fano / Huffman / Hamming / LBC / CRC / CDMA / checksum results and 9 figures; bundle `engineering-data-communication-2082-2083.pdf`; master All-in-One 74 papers. See `engineering/PHASE2_STATUS.md`.
- Session 15c: Signals and Systems (ENEX 255) 2083 Baishakh (back) and 2082 Bhadra (regular) solved (numerics asserted in code, 12 figures); bundle `engineering-signals-and-systems-2082-2083.pdf`; master All-in-One 76 papers. See `engineering/PHASE2_STATUS.md`.
- Session 16: Theory of Computation (ENCT 203) 2082 Chaitra, 2082 Kartik (back) and 2081 Chaitra solved with machine-verified DFA/PDA/TM traces, CNF conversions and 30+ state-diagram/parse-tree figures; bundle `engineering-theory-of-computation-2081-2082.pdf`; master All-in-One 79 papers / 1126 pp. Scope rule: only the last 4-5 years of official papers; the 1,400+ other PDFs in the repo are not typeset. See `engineering/PHASE2_STATUS.md`.
- Session 16b: Computer Graphics and Visualization (ENCT 201) 2082 Kartik (back) and 2081 Chaitra solved (all questions, Python-checked numerics, 18 figures); bundle `engineering-computer-graphics-and-visualization-2081-2082.pdf`; master All-in-One 81 papers. See `engineering/PHASE2_STATUS.md`.
- Session 17 (this run): Foundation of Data Science ENCT 202 (2081 Chaitra), Microprocessor ENEX 201 x3 (2082 Chaitra, 2082 Kartik, 2081 Chaitra), Communication English ENSH 204 x2 (2082 Kartik, 2081 Chaitra) and ENSH 251 x2 (2083 Baishakh, 2082 Bhadra) typeset with full solutions (every Q and OR). New bundles `engineering-microprocessor-2081-2082.pdf`, `engineering-communication-english-2081-2082.pdf`, `engineering-communication-english-part-ii-2082-2083.pdf`; master All-in-One 89 papers / 1266 pp. See PHASE2_STATUS.md for the next list.
- Session 18: five 3rd-year Part I regular papers (2082 Chaitra) typeset with full solutions: Probability and Statistics ENSH 304, Digital Signal Processing and Application ENEX 304, Propagation and Antenna ENEX 303, Digital Control Systems ENEE 304, Filter Design ENEX 301 (every Q and OR). The 5th-semester scan file names (Artificial Intelligence, Embedded Systems, Digital Control, DSP, Propogation) do not match their contents, see `engineering/PHASE2_STATUS.md`. Master All-in-One book now 94 papers.
- Session 19: Engineering Mechanics CE 101 (2081 Baishakh, 2081 Kartik) and Civil Engineering Materials CE 103 / ENCE 103 (2081 Baishakh, Kartik, Chaitra) solved; new bundles `engineering-mechanics-2081.pdf`, `engineering-civil-engineering-materials-2081.pdf`; master All-in-One 99 papers / 1411 pp. Engineering Mechanics scan p7-p9 unread. See `engineering/PHASE2_STATUS.md`.
- Session 20: Fluid Mechanics ENCE 201 (BCE, 3rd sem) 2082 Chaitra, 2082 Kartik (back) and 2081 Chaitra solved (every Q and OR, 12 figures, Python-verified numerics); new bundle `engineering-fluid-mechanics-2081-2082.pdf`; master All-in-One 102 papers / 1454 pp. See `engineering/PHASE2_STATUS.md` (Session 20) for the assumptions and the next list.
- Session 20b: Engineering Mechanics ENCE 101 2081 Chaitra solved (9 questions, 3D wrench, frame, truss, kinematics); EM bundle now 3 papers; master All-in-One 103 papers. Master PDF is ~51 MB (size warning in PHASE2_STATUS.md).


### Section F addendum (session 21, IOE/BE last 5 years only)
Built with full worked solutions and pushed: Soil Mechanics ENCE 253 (2083 Baishakh, 2082 Bhadra), Hydraulics ENCE 251 (2083 Baishakh, 2082 Bhadra), Theory of Structures I ENCE 202 (2082 Chaitra, 2081 Chaitra). New bundles: engineering-soil-mechanics-2082-2083, engineering-hydraulics-2082-2083, engineering-theory-of-structures-i-2081-2082; master All-in-One book regenerated. See engineering/PHASE2_STATUS.md for what is next (Survey I/II, Water Supply, Building Technology, Concrete Technology, PSA, 5th-semester scans).

### Section F addendum (session 22, IOE/BE last 5 years only)
Built with full worked solutions and pushed: Engineering Survey I (ENCE 153 2083 Baishakh back, CE 153 2082 Baishakh back, CE 153 2081 Ashwin regular, ENCE 153 2082 Bhadra regular): Survey I is COMPLETE (4 papers). Bundle engineering-survey-i-2081-2083; master All-in-One book now 113 papers. Next: Survey II, Water Supply, Building Tech, Concrete Tech. See engineering/PHASE2_STATUS.md Session 22.

### Section F addendum (session 23, IOE/BE last 5 years only)
- Engineering Survey II (ENCE 203, BE Civil Year II / Part I): 2082 Chaitra (regular), 2082 Kartik (back) and 2081 Chaitra (regular) typeset with full solutions (every question and sub-question, Python-checked: traverse balancing and DMD area, Tienstra resection, Rankine curve tables, parabolic vertical curves). Bundle `engineering-survey-ii-2081-2082.pdf` (3 papers); master All-in-One now 116 papers / 1656 pp. Next in `engineering/PHASE2_STATUS.md` (Water Supply, Building Technology, Concrete Technology, Theory of Structures II, ...).
