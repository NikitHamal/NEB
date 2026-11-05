# Software Engineering — BCA 252 (Semester IV, 3 credits)

Old code CACS253 (2074 curriculum, Semester IV, 3 credits; the revised list numbers it BCA 252 and swaps places with Numerical Methods). 45 teaching hours.

| Unit | Title | Hours |
|---|---|---|
| 1 | Introduction | 4 |
| 2 | Software Development Process Models (waterfall, evolutionary, CBSE, incremental, spiral, agile, XP, RAD, prototyping, RUP, CASE) | 8 |
| 3 | Software Requirement Analysis and Specification | 10 |
| 4 | Software Design | 10 |
| 5 | Coding | 2 |
| 6 | Software Testing and Quality Assurance | 6 |
| 7 | Software Maintenance | 3 |
| 8 | Managing Software Projects | 2 |

## Verification

`bca/tools/check_se.py` recomputes and substitutes every number and table (the `--fill` / `--verify` mechanism is the same as in Numerical Methods): basic COCOMO in all three modes, intermediate COCOMO with an effort adjustment factor, function-point analysis (UFP, VAF, FP, size conversion), cyclomatic complexity (decision points counted from the Python syntax tree) with the independent-path tests **actually executed** (`grade`, six tests; the triangle classifier, five tests), a boundary-value table produced by running `valid_age`, a CPM forward/backward pass (ES, EF, LS, LF, slack, critical path), PERT expected times, variance and deadline probabilities (normal CDF via `math.erf`), earned value measures (CV, SV, CPI, SPI, EAC, ETC, VAC, TCPI), availability and reliability, defect-removal efficiency and density, risk exposure ranking, Henry–Kafura and Halstead figures, and Boehm's annual maintenance effort.

**What the script caught while writing:** (1) the first cyclomatic example used an unsupported "11 − 9 + 2" graph count; the code now counts decisions from the syntax tree, which showed that the five-test triangle table covers every `return` but is *not* a basis set (V(G) = 12), so a smaller `grade()` function (V(G) = 6, six real tests) was added as the basis-path example; (2) PERT expected time (19.67 weeks) is longer than the CPM time (18 weeks) on the same path because the estimates are right-skewed, which was first written as equal; (3) the probability of finishing by week 20 is 57.8 %, not the "about 50 %" a quick reading of μ = 19.67 suggests.

## Source and honesty

Unit titles, topics and hours are the TU **CACS253** syllabus as reproduced on notebahadur.com and ishan12.com.np (see `bca/SOURCES.md`); the revised BCA 252 PDF was not retrievable. The outline follows Sommerville's *Software Engineering* (the order of Units 1–8 matches that book's chapters); all text is original. Unit 8 has only two hours in the syllabus but carries the estimation, scheduling, earned-value and risk calculations because they are standard examination material; the FPA weights are the IFPUG standard values, the COCOMO constants are Boehm's published values, and the 53 lines of Java per function point is a commonly quoted average that varies by source. Process-model descriptions, CMM levels and the ISO 9001 summary are general knowledge, not machine-checkable.

## Layout notes from the PDF QA

See the build record in `bca/course/CHANGELOG_BCA_COURSE.md`.
