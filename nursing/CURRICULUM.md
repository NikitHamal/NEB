# BSc Nursing (Nepal) - Master Curriculum Queue

Branch `claude/bsc-nursing`. Registry for the build tools is `nursing/books.json` (same data, machine-readable).

## Sources (researched Session 1)

- **Course structure (TU / IOM 4-year BSN, codes BSN 1-30):** IOM/TU curriculum as reproduced by importantedunotes.com (Oct 2025) and the NAMS BSN curriculum PDF. Hours per course are from those tables. **Unit-level headings inside each course are reconstructed from these secondary sources plus standard nursing texts (Kozier & Erb, Potter & Perry, Park's PSM, Dutta, Nelson, NANDA-I, NIC, NOC); verify against your campus copy of the IOM curriculum.**
- **Entrance (MECEE-BL, Medical Education Commission):** one 3-hour paper, 200 MCQs, +1 / -0.25. Zoology 40, Botany 40, Chemistry 50, Physics 50, Mental Agility Test 20 (verbal 5, numerical 5, logical sequencing 5, spatial/abstract 5). Eligibility: +2 Science (PCB + English) with 50% aggregate. Source: MEC CEE syllabus as reproduced by careerkyt.com, entrancenepal.net, noticenp.com; confirm each year's MEC notice (the syllabus was revised in April 2026).
- **Nepal context used in every unit:** MoHP, Nepal Nursing Council (NNC Act 2052, Code of Ethics), NIP schedule, IMNCI, Aama Surakshya, NTP/DOTS, HMIS/DHIS2.

## Day-1 polish standard (every unit)
1. Real open-licensed photographs, cropped and labelled (`assets.py` licence-gated, credits auto-generated).
2. Horizontal photogrid strips (2-up/3-up/4-up) and photo + SVG pairs.
3. 2-4 SVG diagrams per unit (`svgfig`).
4. Every number computed in `nursing/tools/check_<slug>.py` (`--fill/--verify` via `tokcommon.py`).
5. 7-8 point x 3-4 sentence explanations for indications, nursing responsibilities, complications, prevention, health education.
6. Unit ends with MCQs (with rationales), SAQ, 5-mark, 10-15-mark answer with 5-column NANDA-I plan.

## Queue

| Year | Code | Book | Hours | Path | Status |
|---|---|---|---|---|---|
| 1 | BSN 4-5 | Fundamentals of Nursing | T100+P510 h | `course/year-1/fundamentals-of-nursing` | **done (session 1)** |
| 1 | BSN 1 | Integrated Health Sciences I | T150 h | `course/year-1/integrated-health-sciences-1` | **done (session 2)** |
| 1 | BSN 2-3 | Integrated Health Sciences II | T150+P120 h | `course/year-1/integrated-health-sciences-2` | **done (session 3)** |
| 1 | BSN 6-7 | Community Health Nursing | T100+P180 h | `course/year-1/community-health-nursing` | **done (session 4)** |
| 1 | BSN 8 | Nutrition and Diet Therapy | T50 h | `course/year-1/nutrition-and-diet-therapy` | **done (session 5)** |
| 2 | BSN 9 | Adult Nursing I | T100 h | `course/year-2/adult-nursing-1` | queued |
| 2 | BSN 10 | Adult Nursing II | T100 h | `course/year-2/adult-nursing-2` | queued |
| 2 | BSN 11 | Geriatric Nursing | T40 h | `course/year-2/geriatric-nursing` | queued |
| 2 | BSN 13-14 | Psychiatric Nursing | T70+P90 h | `course/year-2/psychiatric-nursing` | queued |
| 2 | BSN 15 | Nursing Concepts | T60 h | `course/year-2/nursing-concepts` | queued |
| 2 | BSN 16 | Social and Behavioral Science | T60 h | `course/year-2/social-and-behavioral-science` | queued |
| 3 | BSN 17-18 | Midwifery I | T70+P180 h | `course/year-3/midwifery-1` | queued |
| 3 | BSN 19-20 | Midwifery II | T130+P420 h | `course/year-3/midwifery-2` | queued |
| 3 | BSN 21-22 | Child Health Nursing | T90+P150 h | `course/year-3/child-health-nursing` | queued |
| 3 | BSN 23-24 | Family and Reproductive Health Nursing | T100+P240 h | `course/year-3/family-and-reproductive-health-nursing` | queued |
| 4 | BSN 25-26 | Management and Health Economics | T150+P360 h | `course/year-4/management-and-health-economics` | queued |
| 4 | BSN 27-28 | Educational Science | T90+P360 h | `course/year-4/educational-science` | queued |
| 4 | BSN 29-30 | Research and Biostatistics | T100+P324 h | `course/year-4/research-and-biostatistics` | queued |
| E | CEE-ZOO | MECEE Zoology for Nursing | 40 marks | `entrance/zoology` | queued |
| E | CEE-BOT | MECEE Botany for Nursing | 40 marks | `entrance/botany` | queued |
| E | CEE-CHE | MECEE Chemistry for Nursing | 50 marks | `entrance/chemistry` | queued |
| E | CEE-PHY | MECEE Physics for Nursing | 50 marks | `entrance/physics` | queued |
| E | CEE-MAT | MECEE Mental Agility Test | 20 marks | `entrance/mental-agility` | queued |
