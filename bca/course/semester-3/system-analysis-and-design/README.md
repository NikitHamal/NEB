# System Analysis and Design — BCA 204 (Semester III, 3 credits)

TU code CACS203 in the older numbering (Semester III, 3 credits, 45 teaching hours). The unit titles and topic lists below are the TU outline as printed on notebahadur.com and ishan12.com.np (re-checked in session 39; the five units and hours are unchanged).

| Unit | Title | Hours | Beyond the outline (added in session 39) |
|---|---|---|---|
| 1 | System Development Fundamentals | 9 | 1.14 UML in depth (use case, class, sequence, state; 4 figures), 1.15 acquisition: TCO and weighted vendor scoring, reuse, 1.16 WBS, project software, earned value |
| 2 | Planning | 7 | (unchanged) |
| 3 | Analysis | 13 | 3.8 level-1 DFD, data dictionary, process specification, CRUD matrix; 3.9 requirement quality, FURPS+, MoSCoW and Kano, traceability matrix |
| 4 | Design | 12 | 4.10 functional dependencies, closure, BCNF, validation and check digits (program); 4.11 golden rules, Fitts's law, wireframe, report types |
| 5 | Implementation and Maintenance | 4 | 5.8 equivalence and boundary tests (program), cyclomatic complexity, stubs and drivers, defect log and DRE; 5.9 change control, versioning, legacy systems, Lehman's laws, data migration |

## Verification

The numbers in the worked examples were recomputed in Python: the critical path (11 weeks, A-C-E-F, slack 1 on B and D), PERT expected time, NPV (+447,697), ROI (150%), simple payback (2.0 years), discounted payback (2.35 years), benefit-cost ratio (1.51), IRR (about 41%) and the decision-table coverage (4 + 2 + 1 + 1 = 8 rules). Session 39 added and checked: five-year TCO of build, package and SaaS (3,150,000; 1,600,000; 1,000,000), weighted vendor scores (350, 395, 345), earned value (PV 500,000, EV 400,000, SV -100,000, SPI 0.80, CV -120,000, CPI 0.77, EAC 1,300,000 and the practice set), the member-number check digit (0173 gives 2; the swapped entry is rejected), Fitts's law times (0.76 s and 0.49 s), the 15 boundary cases of the grade function (executed, all pass), cyclomatic complexity 5 + 1 = 6, DRE 90 per cent, and the migration reconciliation (12,440 rows, Rs 147,870,500).

## Source and honesty

The textbook behind the outline is *Essentials of Systems Analysis and Design* (Valacich, George, Hoffer); the text here is original and follows the book's chapter order. The UML, FURPS+, MoSCoW, Kano, Fitts, Shneiderman, McCabe and Lehman material goes beyond the printed outline because exam answers and projects use it; it is marked as such above. Constants in worked examples (Fitts a and b, project costs, vendor scores) are illustrative, not measured. The revised 2082 BCA 204 syllabus PDF itself was not retrievable; the outline copies on the two sites above still list the same five units.

## Layout notes from the PDF QA

See `bca/BCA_POLISH_STATUS.md` (session 39) for the page count and QA result of the latest build.
