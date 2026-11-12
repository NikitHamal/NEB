# Technical Writing — BCA 354 (Semester VI, 2 credits)

Audience and purpose analysis, the writing process and document design; plain-language style and the Flesch Reading Ease, Flesch–Kincaid Grade and Gunning Fog readability indices; software documentation (SRS with a requirement linter, README, user guides, OpenAPI reference with a checker, runbooks, postmortems, commit messages); research proposals, IMRaD, abstracts, literature reviews, APA and IEEE citation with a formatter, plagiarism and similarity; visual communication (tables, charts, the lie factor, WCAG contrast, diagrams, slides); editing, professional email, reports, minutes, CVs and ethics. 45 teaching hours in this reconstruction (the revised list replaces CAEN103/CAEN153 English with BCA 105 and BCA 354).

| Unit | Title | Hours |
|---|---|---|
| 1 | Audience, Purpose and the Writing Process | 5 |
| 2 | Style, Clarity and Readability | 8 |
| 3 | Software Documentation: SRS, README, API Reference, Runbooks and Postmortems | 9 |
| 4 | Research Proposals, Academic Writing and Citation | 8 |
| 5 | Visual Communication: Tables, Charts, Diagrams and Slides | 7 |
| 6 | Editing, Professional Communication and Ethics | 8 |
| 7 | Writing for the Web, Information Reports, Proposals and Group Work | 12 |
| 8 | Instructions, Technical Descriptions and Formal Reports | 10 |

## Verification

`bca/tools/check_techwriting.py` plus `fill_script_outputs.py`: the five executed programs (readability scores on three texts using a hand-labelled syllable table, the requirement linter, the OpenAPI checker, the APA/IEEE formatter and the shingle-similarity measure) have their printed lines recomputed by independent code and `--verify` demands each is present. Token-substituted numbers: the lie factor (5% data change drawn as 100%), pie-chart angles, WCAG contrast ratios from the luminance formula (black 21.00, #767676 4.54, #999999 2.85, red 4.00, blue 8.59 on white) and the concision-edit word counts. All hand-computed practice answers (readability, lie factor, angles, similarity) are asserted too.

## Source and honesty

No TU unit list for BCA 354 was retrieved; the six units are a reconstruction from the topics named in the course brief and a standard technical-writing syllabus. Readability formulas are the published Flesch (1948), Kincaid et al. (1975) and Gunning (1952) definitions with the usual complex-word rule; syllable counts in the program are hand-labelled, not computed. Standards (WCAG 2, IEEE reference style, APA 7th, OpenAPI 3.0) are described from general knowledge; consult the current editions. The reference to the Diátaxis documentation framework and to Tufte's lie factor are from the standard literature.


## Session 21: syllabus gap closed

The published TU outline for Technical Writing (the CSC368 text, which lists 12 teaching units: what technical writing is, audience and purpose, the writing process, brief correspondence, document design and graphics, writing for the web, information reports, instructions, presentations, proposals, formal reports and ethics) names topics that Units 1 to 6 did not cover: **collaborative writing, writing for the web, information reports (summary and abstract, mechanism description, periodic and progress reports, news releases), informal and formal proposals, and group presentations.** They are now Unit 7. Its Python blocks (progress-report arithmetic, proposal budget) are executed by `fill_script_outputs.py`; the examples are invented for illustration. Still thin: *instructions* (only a section in Unit 3) and *formal reports* (Unit 6.4) deserve a full chapter next time.


## Session 22: instructions, definitions and formal reports

NEW Unit 8 (about 6k words, 2 figures, 2 executed Python blocks): full chapter on **instructions** (failure modes, planning, parts, imperative style, the four notice levels after ANSI Z535 / ISO 3864, a worked Install-Python model, usability testing), **technical definitions** (parenthetical, formal *class + differentia*, extended with nine methods) and **descriptions** (mechanism, process, system), **formal reports** (kinds, front matter, letter of transmittal, body, back matter, page numbering), **recommendation and feasibility reports** (weighted decision matrix with sensitivity check, cost table and payback, both recomputed by the executed blocks), a three-way report checklist and the ethics of reporting. Closes the Session 21 gap (instructions and formal reports).
