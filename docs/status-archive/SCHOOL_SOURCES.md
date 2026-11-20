# SCHOOL_SOURCES.md

Access date for every URL below: **2026-11-02** (sandbox clock). "Weight" = how much I rely on it: **primary** (CDC/Govt of Nepal document or a verbatim copy of it), **secondary** (third-party site quoting the syllabus/textbook list), **weak** (commercial "guide" site; used only to cross-check, never alone).

## Class 8
| What | URL | Version | Weight |
|---|---|---|---|
| CDC Class 8 textbook list (Nepali, English, Maths, Science, Social, Health — no standalone Computer book) | https://pragyapath.com/tools/cdc-textbooks.html (links to moecdc.gov.np) | CDC editions 2076–2080 | secondary |
| Class 8 Computer course still has QBASIC as Chapter 20 ("Updated" Nov 2024) | https://abcsir.blogspot.com/p/class-8.html | Shuvarambha / Sunrise books | secondary |
| Ocean Computer-8 (CDC-aligned) with QBASIC chapters, published 19 Jan 2023 | https://fliphtml5.com/nrhva/gkjv/Computer_Science_Textbook_for_Class_8/ | 2023 | secondary |
| Study of Nepal CS curricula (Dec 2024): CDC officer says Office apps are in Grade 8 *Science*; CDC "wants to retain QBasic"; Python is only a *suggested* revision | https://www.researchgate.net/publication/387456686 | Dec 2024 | secondary |
| CDC basic curriculum 2076 (class 6–8), e-library ids 3727/3728 | https://lib.moecdc.gov.np/ | 2076 | primary — **could not be opened** (SSL handshake failure from the sandbox; moecdc.gov.np/storage/gallery/*.pdf returned 404) |

## Class 9–10 (used to settle Class 10 CS)
| What | URL | Weight |
|---|---|---|
| Class 9 (2082) and Class 10 (2083) CS: Python replaces QBASIC; 5 Class-10 chapters | https://computerkite.com/notes/computer-science-class-9-10-new-syllabus/ | secondary |
| Class 10 CS Programming-in-Python 4.1–4.6 syllabus text | https://shikshasanjal.com/syllabus/class-10-computer-science-syllabus ; https://readersnepal.com/posts/see-class-10-computer-science-new-curriculum-and-syllabus | secondary |
| CDC Computer Science Grade 9 textbook, first ed. 2081 BS (curriculum 2080) | https://giwmscdnone.gov.np/media/pdf_upload/Computer%20Science%20Grade%209_r12pxcl.pdf | primary |
| Class 10 Science & Technology (2080 textbook, English translation): 19 units | https://www.bhojrajbhurtel.com.np/2025/09/new-textbook-of-science-technology.html ; https://webnotee.com/see-class-10-science-guide-2082/ | secondary (textbook contents) |
| Class 10 Mathematics, Govt of Nepal textbook PDF, contents: 18 chapters | https://s3.veda-app.com/veda-app/assets/122/downloads/2025-11-18/9cUCrtK4DtLpuSi6-1763455199.pdf | primary (copy of CDC book) |

## Class 11–12
| What | URL | Weight |
|---|---|---|
| NEB CS 11 units + hours (20/11/12/5/8/8/6/8) | https://www.examkura.com/neb-class-11-computer-guide/ | weak (sums to 78 h, official total is 80) |
| NEB Chemistry 11 units + hours | https://sajhanotes.com/neb-grade-11-chemistry-syllabus/ ; https://www.examkura.com/neb-class-11-chemistry-guide/ | secondary |
| NEB Physics 11/12 units + hours | https://readersnepal.com/posts/neb-class-11-and-12-physics-new-curriculum-and-syllabus | secondary |

## Sources rejected / contradicted
- examkura.com "SEE Class 10 Computer Science Guide 2082" says Class 10 CS uses QBASIC and lists 10 chapters. This contradicts the CDC Grade 9 textbook notice and every other source; treated as stale.
- nneducation.com says Physics 12 "Recent Trends" was added in the latest revision; the repo already carries a Physics 11 "Recent Trends" unit and 25 Physics 12 units, matching the readersnepal list. Not acted on (weak).

## Factual corrections made
| Where | Was | Now | Basis |
|---|---|---|---|
| eng10 unit 4, model job-application letter by a "twenty years old" applicant | "After passing my SLC" | "After passing my SEE" | SLC was replaced by SEE (last SLC 2072 BS, first SEE 2073 BS). **From general knowledge — I did not fetch a source for this specific date this session.** A 20-year-old writer today cannot have sat the SLC. |

## Session 3 (continuation)
**Class 8 Computer — QBASIC removed, Python added.** Basis for the change: the user's direct confirmation, from a working Class 8 teacher, that QBASIC is no longer in the current Class 8 Computer syllabus and Python is. I did **not** find any independent written source for this: every publisher outline I could reach still lists QBASIC for Class 8 (abcsir.blogspot.com/p/class-8.html, Nov 2024; mero.school Computer Class 8, Oct 2024; Ocean Computer-8, fliphtml5, Jan 2023; Smart Computer Science 8 and Trijyoti, 2022) — consistent with publisher lag, not evidence against the teacher. The CDC curriculum PDF was not hunted (per instruction). So this change is **teacher-confirmed, not document-verified**.
**Depth of the Python content** was set from the CDC Computer Science Grade 9 textbook (first ed. 2081 BS), fetched this session from https://giwmscdnone.gov.np/media/pdf_upload/Computer%20Science%20Grade%209_r12pxcl.pdf (primary): its Python chapter covers intro/installing, comments, keywords, I/O and string formatting, identifiers and variables, data types, operators, if/nested if, for, while, lists, dictionaries, library functions. Class 8 therefore stops at the foundation (intro, tokens and types, operators, I/O, built-in functions, selection, loops, debugging); lists, dictionaries and user-defined functions are left to Class 9. Unit list is my judgement from that progression and generic Class 8 Python outlines, **not** from a Class 8 CDC document.
**Not done this session:** retrying CDC/NEB curriculum PDFs for Classes 8, 11, 12; checking the Class 10 2083 editions (English, Nepali, Social, Optional Maths). No new sources were consulted for them.
