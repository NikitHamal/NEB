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