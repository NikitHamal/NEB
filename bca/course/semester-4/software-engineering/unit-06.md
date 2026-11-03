---
subject: Software Engineering
grade: BCA Semester 4
unit: 6
title: Software Testing and Quality Assurance
hours: 6
area: BCA 252 · Software Engineering · Unit 6
---

Testing can show the presence of bugs, never their absence (Dijkstra). It is still the main way we gain confidence that software works, and it takes about 40 % of development cost. This unit covers verification and validation, black-box and white-box techniques (with executed examples), the levels of testing, test case design, and the quality-management activities and standards that surround testing.

::: key What this unit gives you
- Verification versus validation; inspections.
- Black-box testing (equivalence partitioning, boundary value analysis) and white-box testing (basis path, cyclomatic complexity), with real executed tests.
- Unit, integration, interface, system, alpha, beta and regression testing.
- Quality management, product and process quality; ISO 9000, CMM; reliability numbers.
:::

## 6.1 Verification and validation

- **Verification**: "Are we building the product right?" Does the software conform to its specification? (reviews, inspections, static analysis, testing).
- **Validation**: "Are we building the right product?" Does it meet the customer's real needs? (acceptance testing, prototypes).

**Static techniques** examine the artefacts without executing them: **inspections** (Fagan: a formal, checklist-based review of code or design by a trained team with moderator, author, reader and recorder), **walkthroughs**, desk checks and **static analysers**. Inspections find defects early and often 60 % or more of them. **Dynamic techniques** execute the program with test data.

**Testing vs debugging.** Testing finds the *presence* of a failure; debugging locates and removes the *cause*. A **test case** = inputs + preconditions + expected output; a **fault** (bug) in the code causes a **failure** when executed; an **error** is the human mistake behind it.

## 6.2 Black-box testing

Test against the specification, ignoring the code ("functional testing"). It finds missing functions, interface and behaviour errors.

### Equivalence partitioning

Divide the input domain into **classes** in which the program should behave the same; test one value from each class. For an age field that must accept 18 to 60: valid class 18–60, invalid classes below 18 and above 60, (and non-numeric). This cuts thousands of inputs to a handful.

### Boundary value analysis (BVA)

Errors cluster at the edges (the classic `<` instead of `<=`). Test **just below, on, and just above** each boundary. For 18–60 the boundaries are 18 and 60, giving 17, 18, 19, 59, 60, 61. Real run of a `valid_age(x)` function (`18 <= x <= 60`) on these values:

| Input age | Class | Expected | valid_age() returned |
|---|---|---|---|
| 17 | invalid | reject | reject |
| 18 | valid | accept | accept |
| 19 | valid | accept | accept |
| 59 | valid | accept | accept |
| 60 | valid | accept | accept |
| 61 | invalid | reject | reject |

All six behave as specified. Had the code been `18 < x < 60`, the cases 18 and 60 would have exposed it immediately, while a mid-range value such as 35 never would.

Other black-box techniques: decision tables, state-transition testing, use-case testing, error guessing, random testing.

## 6.3 White-box (structural) testing

Test the internal logic with knowledge of the code. Coverage criteria, weakest to strongest: **statement coverage** (every statement executed), **branch/decision coverage** (every decision both true and false), **condition coverage** (every atomic condition both true and false), **path coverage** (every path, usually impossible for loops).

### Cyclomatic complexity and basis path testing

McCabe's **cyclomatic complexity V(G)** equals the number of linearly independent paths through the control-flow graph, and so the **minimum number of tests** needed to execute every statement and every branch:

- V(G) = E − N + 2P (E edges, N nodes, P connected components, normally 1);
- V(G) = number of **decision points + 1**, where each `if`, `elif`, loop and each `and`/`or` counts as one (a compound condition with *k* operands counts *k* − 1 extra decisions);
- V(G) = number of regions of the planar flow graph.

**Interpretation:** 1–10 simple and low risk; 11–20 moderate; 21–50 complex; above 50 untestable. Many teams limit functions to 10 and refactor above it.

::: example Basis path testing of a grading function
```python
def grade(m):
    if m < 0 or m > 100:
        return "invalid"
    elif m >= 80:
        return "A"
    elif m >= 60:
        return "B"
    elif m >= 40:
        return "C"
    return "F"
```
Decision points counted from the syntax tree: **5** (`if`, the `or` inside it, and three `elif`), so V(G) = 5 + 1 = **6**. Six independent paths need six tests; the table shows each test run through the real function:

| Test m | Independent path | grade(m) returned |
|---|---|---|
| -5 | m < 0 (first operand of or) | invalid |
| 101 | m > 100 (second operand) | invalid |
| 85 | m ≥ 80 | A |
| 65 | 60 ≤ m < 80 | B |
| 45 | 40 ≤ m < 60 | C |
| 20 | m < 40 (falls through) | F |

Every statement and both outcomes of every condition are exercised by these six tests, and V(G) = number of tests needed.
:::

For a larger function the number grows quickly. A triangle classifier has the following structure:

```python
def classify(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return "invalid"
    if a + b <= c or a + c <= b or b + c <= a:
        return "not a triangle"
    if a == b and b == c:
        return "equilateral"
    if a == b or b == c or a == c:
        return "isosceles"
    return "scalene"
```

Counting its decisions (each `or`/`and` operand counts) gives **11** decision points, so V(G) = **12**: twelve independent paths are required for full basis-path coverage. The five tests below reach every `return` statement, but they are *not* a basis set (they do not isolate every condition), which is why a complexity of 12 signals that the function is borderline and should be split.

| Test (a, b, c) | Path exercised | Result |
|---|---|---|
| (0, 4, 5) | a ≤ 0 (first condition) | invalid |
| (3, 4, 9) | a + b ≤ c | not a triangle |
| (5, 5, 5) | all equal | equilateral |
| (5, 5, 8) | a = b only | isosceles |
| (3, 4, 5) | all different | scalene |

## 6.4 Levels of testing

| Level | What is tested | By whom | Technique |
|---|---|---|---|
| **Unit testing** | a single function, class or module in isolation | developer | white-box with stubs/drivers; xUnit frameworks |
| **Integration testing** | interaction of modules | developer/tester | **big-bang**, **top-down** (stubs for lower modules), **bottom-up** (drivers for upper modules), **sandwich** |
| **Interface testing** | calls, parameters, shared memory, message passing between components | tester | parameter, shared-memory and message-passing interface tests; stress |
| **System testing** | the complete integrated system against requirements | independent testers | functional, performance, load/stress, security, recovery, usability, compatibility |
| **Acceptance testing** | whether the customer accepts the system | customer | **alpha** and **beta** |

- **Alpha testing**: by the customer *at the developer's site*, with the developer observing and recording problems, in a controlled environment.
- **Beta testing**: by a sample of real users *at their own sites*, without the developer present, in an uncontrolled environment, who report problems back; widely used for products (public beta of apps).
- **Regression testing**: re-running previous tests after a change to check that nothing that worked has broken. Because it is repeated many times, it is the best candidate for automation, and a continuous-integration server runs the suite on every commit.
- Other kinds: **smoke testing** (is the build stable enough to test further?), **performance/load/stress testing**, **security (penetration) testing**, **usability testing**, **recovery testing**.

## 6.5 Design of test cases

A good test case has a high probability of finding an undiscovered fault. A test-case record has: ID, objective, preconditions, input, expected result, actual result, pass/fail. Strategy: derive tests from the specification with equivalence partitioning and BVA, supplement with white-box tests for uncovered branches, add tests for every defect fixed (regression), and prioritise by risk. **Test-driven development** writes the test before the code.

**Test adequacy.** Track coverage (statement/branch %), **defect-removal efficiency** DRE = defects found before release ÷ (found before + found after). With 80 defects found internally and 20 found by users, DRE = **80 %**. Mutation testing and code-coverage tools judge test quality.

## 6.6 Quality management

**Quality assurance (QA)** establishes a framework of organisational procedures and standards that leads to high-quality products; **quality planning** selects procedures and standards for a project; **quality control (QC)** checks that those are followed (reviews and tests). Quality is *conformance to requirements* (Crosby) and *fitness for use* (Juran).

### Product quality and process quality

- **Product quality** attributes: correctness, reliability, efficiency, integrity/security, usability, maintainability, testability, portability, reusability, interoperability (McCall; ISO/IEC 25010 lists functional suitability, performance efficiency, compatibility, usability, reliability, security, maintainability, portability).
- **Process quality**: a good process is the best predictor of good products in repeatable development (but is less reliable for design-intensive work). Improving the process is the basis of CMM and ISO 9000.

### Reliability measures

**MTTF** (mean time to failure), **MTTR** (mean time to repair), **MTBF = MTTF + MTTR**, **availability A = MTTF/(MTTF + MTTR)**, **failure rate λ = 1/MTTF** (constant-rate model), and **reliability R(t) = e^(−λt)**.

::: example Reliability numbers
A server has MTTF = 1000 hours and MTTR = 2 hours. Availability = 1000/1002 = **99.800 %**, about 17.5 hours of downtime per year (8,760 h). With λ = 0.001 per hour, the probability of running 100 hours without failure is R(100) = e^(−0.1) = **0.9048**.
:::

### Standards: ISO 9000

**ISO 9001** is an international standard for a *quality management system* (QMS): a documented process (plan, do, check, act) covering responsibilities, documented procedures, internal audits, corrective action and continuous improvement. A company is *certified* by an external audit. ISO 9001 shows that an organisation follows *its own* documented process; it does not by itself guarantee product quality. **ISO 9000-3** (now guidance for ISO 9001) interprets it for software.

### Capability Maturity Model (CMM)

The SEI's CMM (now CMMI) assesses the maturity of a software organisation's process on five levels:

| Level | Name | Characteristics |
|---|---|---|
| 1 | **Initial** | ad hoc, chaotic; success depends on individual heroics |
| 2 | **Repeatable** (Managed in CMMI) | basic project management: requirements, planning, tracking, configuration management, QA; earlier success can be repeated |
| 3 | **Defined** | organisation-wide standard documented process; training; peer reviews |
| 4 | **Managed** (Quantitatively Managed) | process and product measured; quantitative quality goals |
| 5 | **Optimising** | continuous process improvement through feedback and innovation |

Moving up takes years: a typical step takes 18 to 24 months. Most offshore software companies seek level 3 or higher (CMMI) to win export contracts.

## 6.7 Testing in pictures: from the first bug to the V-model

Testing cannot prove that a program is correct, but it is the main way of finding out how wrong it still is. Plate 6.1 shows three real objects of testing history; Figures 6.1 to 6.5 draw the V-model, the choice of black-box test data, the control-flow graph used for basis-path testing, a reliability curve and the five levels of the Capability Maturity Model.

```photogrid label="6.1" cols="3" ratio="1.0" caption="Three faces of testing. (a) The moth of 9 September 1947 in the Harvard Mark II logbook: the first 'debugging' that is recorded in writing. (b) A network cable tester: a test instrument applies known inputs (one signal on each wire) and compares the outputs with the expected pattern, which is exactly what a software test case does. (c) The recovered fragment of Ariane 501: the guidance software had been tested on Ariane 4 flight data but never on the faster Ariane 5 trajectory, so the fault was found by the rocket itself at a cost of about 370 million US dollars."
@ photo id="bca252/bug" cap="First recorded debugging"
fit 1.0
focus 0.5 0.55
@ photo id="bca106/tester" cap="Cable tester: input, expected output"
fit 1.0
focus 0.5 0.5
@ photo id="bca252/ariane" cap="Ariane 501 fragment"
fit 1.0
focus 0.5 0.5
```

```svgfig label="6.1" caption="The V-model. The left arm goes down from requirements to coding (verification: are we building the product right?); the right arm goes up through the four levels of testing (validation: are we building the right product?). Each test level is planned against the document on the same row, so acceptance tests are written from the requirements, system tests from the system design, integration tests from the detailed design and unit tests from the code."
f = Fig(580, 240)
left = ["Requirements", "System design", "Detailed design", "Coding"]
right = ["Acceptance test", "System test", "Integration test", "Unit test"]
for i in range(4):
    y = 14 + i * 50
    f.box(10 + 50 * i, y, 126, 36, left[i], fill=BLUE, stroke=NAVY, size=10, bold=True)
    f.box(444 - 50 * i, y, 126, 36, right[i], fill=MINT, stroke=TEAL, size=10, bold=True)
    f.arrow([(136 + 50 * i, y + 18), (444 - 50 * i, y + 18)], color=AMBER, dash=True)
f.text(290, 8, "test plans written early", size=9.5, color=AMBER, bold=True)
f.text(80, 228, "verification (build it right)", size=10, color=NAVY, bold=True)
f.text(500, 228, "validation (right product)", size=10, color=TEAL, bold=True)
```

```svgfig label="6.2" caption="Test data for an input that accepts marks from 0 to 100. Equivalence partitioning gives three classes: below 0 (invalid), 0 to 100 (valid) and above 100 (invalid); one test per class is enough. Boundary value analysis adds the values on and next to each edge: -1, 0, 1, 99, 100 and 101, because programs most often fail at boundaries (for example '<' written instead of '<=')."
f = Fig(580, 200)
f.line(40, 100, 540, 100, color=SLATE, sw=2)
f.box(40, 60, 120, 34, "invalid: below 0", fill=ROSE, stroke=RED, size=10, bold=True)
f.box(230, 60, 120, 34, "valid: 0 to 100", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(420, 60, 120, 34, "invalid: above 100", fill=ROSE, stroke=RED, size=10, bold=True)
tests = [(160, "-1"), (200, "0"), (230, "1"), (350, "99"), (380, "100"), (420, "101")]
xs = {"-1": 150, "0": 205, "1": 245, "99": 335, "100": 375, "101": 430}
for k, v in xs.items():
    ok = k in ("0", "1", "99", "100")
    f.circle(v, 100, 6, fill=(MINT if ok else ROSE), stroke=(TEAL if ok else RED))
    f.text(v, 128, k, size=11, color=(TEAL if ok else RED), bold=True)
f.text(290, 160, "boundary tests: -1 (reject), 0 and 1, 99 and 100 (accept), 101 (reject)", size=10.5, color=SLATE, bold=True)
f.text(290, 182, "equivalence tests: -20, 50, 130 (one per class)", size=10.5, color=SLATE, bold=True)
```

```svgfig label="6.3" caption="The control-flow graph of clamp(x), which returns |x| limited to 100. Nodes 1 to 6 are blocks (1 start, 2 test x < 0, 3 x = -x, 4 test x > 100, 5 x = 100, 6 return). There are 7 edges and 6 nodes, so V(G) = E - N + 2 = 7 - 6 + 2 = 3, which equals the two decisions plus one. Three basis paths need three tests: 1-2-4-6 with x = 50, 1-2-3-4-6 with x = -5, and 1-2-4-5-6 with x = 150."
f = Fig(580, 270)
nodes = {1: (290, 22, "1"), 2: (290, 76, "2 x<0?"), 3: (150, 76, "3 x=-x"), 4: (290, 138, "4 x>100?"), 5: (150, 198, "5 x=100"), 6: (290, 246, "6 return x")}
for k, (x, y, t) in nodes.items():
    f.circle(x, y, 22 if k in (1,) else 24, fill=(SAND if k in (2, 4) else BLUE), stroke=(AMBER if k in (2, 4) else NAVY), label="")
    f.text(x, y + 1, t, size=9, color=NAVY, bold=True, vmid=True)
f.arrow([(290, 44), (290, 52)], color=SLATE)
f.arrow([(266, 76), (174, 76)], color=SLATE, label="yes", lpos=(220, 66), lsize=9)
f.arrow([(150, 100), (270, 130)], color=SLATE)
f.arrow([(290, 100), (290, 114)], color=SLATE, label="no", lpos=(310, 108), lsize=9)
f.arrow([(268, 144), (172, 192)], color=SLATE, label="yes", lpos=(210, 156), lsize=9)
f.arrow([(290, 162), (290, 222)], color=SLATE, label="no", lpos=(310, 192), lsize=9)
f.arrow([(172, 206), (270, 240)], color=SLATE)
f.box(400, 40, 170, 40, "V(G) = 7 - 6 + 2 = 3", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(400, 96, 170, 36, "P1: 1-2-4-6   x = 50", fill="#ffffff", stroke=NAVY, size=9.5, bold=True)
f.box(400, 142, 170, 36, "P2: 1-2-3-4-6   x = -5", fill="#ffffff", stroke=NAVY, size=9.5, bold=True)
f.box(400, 188, 170, 36, "P3: 1-2-4-5-6   x = 150", fill="#ffffff", stroke=NAVY, size=9.5, bold=True)
```

```svgfig label="6.4" caption="Reliability and availability for a system with a mean time to failure (MTTF) of 500 hours and a mean time to repair (MTTR) of 4 hours. The failure rate is 1 / 500 = 0.002 per hour, and the probability of running without failure for t hours is R(t) = exp(-t / 500): R(100) = 0.8187 and R(500) = 0.3679. Availability = MTTF / (MTTF + MTTR) = 500 / 504 = 99.2063%."
import math
f = Fig(580, 240)
f.line(60, 190, 540, 190, color=SLATE, sw=1.5)
f.line(60, 20, 60, 190, color=SLATE, sw=1.5)
pts = []
for i in range(0, 101):
    t = i * 10
    pts.append((60 + t * 0.48, 190 - 160 * math.exp(-t / 500)))
f.raw('<polyline points="' + " ".join(str(round(a, 1)) + "," + str(round(b, 1)) for a, b in pts) + '" fill="none" stroke="#1d4ed8" stroke-width="2.6"/>')
for t in (100, 500):
    x = 60 + t * 0.48
    y = 190 - 160 * math.exp(-t / 500)
    f.circle(x, y, 5, fill=SAND, stroke=RED)
    f.line(x, y, x, 190, color=AMBER, sw=1.2, dash=True)
    f.text(x + 8, y - 8, "R(" + str(t) + ") = " + str(round(math.exp(-t / 500), 4)), size=10.5, color=RED, bold=True, anchor="start")
for t in (0, 250, 500, 750, 1000):
    f.text(60 + t * 0.48, 208, str(t) + " h", size=9.5, color=SLATE)
f.text(300, 232, "operating time t", size=10, color=SLATE, bold=True)
f.text(66, 16, "R(t)", size=10.5, color=NAVY, bold=True, anchor="start")
```

```svgfig label="6.5" caption="The five levels of the Capability Maturity Model (CMM). An organisation climbs from level 1, where success depends on individual heroes, to level 5, where it measures its processes and uses the data to improve them. Each level adds key process areas; levels cannot be skipped."
f = Fig(580, 250)
lv = [("1 Initial", "ad hoc, heroes", ROSE, RED), ("2 Repeatable", "project control", SAND, AMBER), ("3 Defined", "standard process", BLUE, NAVY), ("4 Managed", "measured quality", MINT, TEAL), ("5 Optimizing", "continual change", MINT, TEAL)]
for i, (a, b, fl, st) in enumerate(lv):
    h = 56 + i * 30
    f.box(10 + i * 112, 220 - h, 104, h, a + "\n" + b, fill=fl, stroke=st, size=10, bold=True)
f.text(290, 14, "process maturity rises from left to right", size=10.5, color=NAVY, bold=True)
```

### 6.7.1 Eight principles of software testing

1. **Testing shows the presence of defects, not their absence.** Even after many passed tests a program may still contain faults. Testing reduces the chance of undiscovered defects but can never prove that none remain. The honest report is "no defects found by these tests", not "the program is correct".
2. **Exhaustive testing is impossible.** A function with two 32-bit inputs has about 1.8 x 10 to the power 19 input combinations, which no computer can try. Testers therefore choose a small set of effective tests using equivalence classes, boundary values and risk, as in Figure 6.2. Choosing wisely is the skill of testing.
3. **Test early.** Testing activities begin with the requirements, not after coding, as the V-model in Figure 6.1 shows. A fault found in requirements costs a fraction of one found after release (Figure 1.1). Reviewing the SRS and writing acceptance tests early prevents many defects.
4. **Defects cluster.** A small number of modules usually contain most of the defects, often following the 80-20 rule. Complex or frequently changed modules, found with metrics such as cyclomatic complexity, deserve extra testing. Past defect reports show where to look.
5. **The pesticide paradox.** If the same tests are repeated, they stop finding new defects, as insects become resistant to one pesticide. Test cases must be reviewed and new ones added regularly. Regression tests protect old behaviour, but new tests find new faults.
6. **Testing depends on context.** A game, a hospital system and a banking app are tested differently. Safety-critical software needs formal coverage and independent review, while a short-lived website needs fewer formal tests. The level of testing follows the level of risk, such as the harm a fault can do to a ConnectIPS payment.
7. **Absence of errors is not enough.** A system with no defects can still fail if it does not meet the users' needs. Validation with real users, as in acceptance testing, checks that the right product was built. Passing all the tests of a wrong specification gives a wrong product.
8. **Independent testing finds more.** Authors tend to test what they intended, so an independent tester or team sees what the author misses. Independence can be a colleague, a separate test team or an outside company. It is most important for critical software.

## Formula and fact sheet

- V(G) = E − N + 2P = decisions + 1 = minimum tests for branch coverage.
- BVA: test min−1, min, min+1, max−1, max, max+1.
- Alpha: developer's site. Beta: users' sites. Regression: re-test after change.
- DRE = found before release / (found before + found after).
- A = MTTF/(MTTF + MTTR); R(t) = e^(−λt), λ = 1/MTTF.
- CMM: Initial, Repeatable, Defined, Managed, Optimising.

## Chapter summary

- Verification checks conformance to the specification; validation checks fitness for the user's needs. Inspections are the most cost-effective defect finders.
- Black-box tests (equivalence classes, boundaries) come from the specification; white-box tests from the structure; cyclomatic complexity gives the minimum number of independent-path tests.
- Testing proceeds from units to integration, system and acceptance (alpha, beta), with regression testing after every change.
- Quality management combines product and process quality, measured by reliability numbers and improved through ISO 9001 and CMM maturity levels.

## Practice

1. Distinguish verification from validation and testing from debugging.
2. Apply equivalence partitioning and BVA to a field accepting marks between 0 and 100.
3. Compute V(G) for the `grade` function above and list a test for each independent path.
4. Differentiate alpha and beta testing; why is regression testing automated?
5. Explain top-down and bottom-up integration testing; what are stubs and drivers?
6. What is the difference between statement coverage and branch coverage? Give an example in which 100 % statement coverage misses a bug.
7. A system has MTTF = 500 h and MTTR = 5 h. Find availability and the probability of surviving 50 h.
8. 120 defects were found before release and 30 after. Compute the defect-removal efficiency.
9. Describe the five levels of CMM.
10. What does ISO 9001 certification guarantee?

::: note Answers and worked solutions
**1.** Verification: building the product right (against the specification). Validation: building the right product (customer's needs). Testing finds failures; debugging finds and fixes the fault that caused them.
**2.** Classes: below 0 (invalid), 0 to 100 (valid), above 100 (invalid), non-numeric. BVA values: −1, 0, 1, 99, 100, 101.
**3.** Decisions: 5; V(G) = 6. Tests: −5, 101, 85, 65, 45, 20 give invalid, invalid, A, B, C, F (executed in Section 6.3).
**4.** Alpha: at the developer's site with the developer watching. Beta: at users' sites without the developer. Regression tests are repeated after every change, so automation saves effort and gives fast feedback.
**5.** Top-down starts at the main module and replaces missing lower modules with **stubs**; bottom-up starts with the lowest modules and uses **drivers** to call them. Sandwich combines the two.
**6.** Statement coverage executes each line; branch coverage executes both outcomes of each decision. `if (x > 0) y = 1; z = 10 / y;` with x = 5 covers all statements, but never tests x ≤ 0, where y is undefined: the bug is missed.
**7.** A = 500/505 = 0.990099 = **99.01 %**; λ = 1/500 = 0.002; R(50) = e^(−0.1) = **0.9048**.
**8.** DRE = 120/(120 + 30) = **80 %**.
**9.** Initial (ad hoc), Repeatable (project management), Defined (organisation standard process), Managed (quantitative control), Optimising (continuous improvement).
**10.** That the organisation has a documented quality management system and follows it, as verified by an audit. It does not guarantee that every product is free of defects.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain equivalence partitioning and boundary value analysis. Design test cases for a field that accepts marks from 0 to 100.**

*Introduction.* Both are black-box techniques, which test the behaviour of the program from the specification without looking at the code (section 6.2).

1. **Equivalence partitioning.** The input domain is divided into classes in which the program should behave the same way, and one test per class is enough. Marks have three classes: below 0 (invalid), 0 to 100 (valid) and above 100 (invalid) (Figure 6.2).
2. **Test data for the classes.** -20 (rejected), 50 (accepted), 130 (rejected): three tests.
3. **Boundary value analysis.** Faults concentrate at the edges of classes, so values on and next to each boundary are tested.
4. **Test data for the boundaries.** -1, 0, 1, 99, 100 and 101.

| Test | Input | Expected result |
|---|---|---|
| 1 | -1 | rejected |
| 2 | 0 | accepted |
| 3 | 1 | accepted |
| 4 | 99 | accepted |
| 5 | 100 | accepted |
| 6 | 101 | rejected |

*Conclusion.* Together, the nine cases (three classes plus six boundaries) cover the specification at low cost, and they catch the common error of writing `<` where `<=` is needed.

**Q2 (5 marks). Differentiate between verification and validation. Show the relation with the V-model.**

*Introduction.* Verification asks "Are we building the product right?" and validation asks "Are we building the right product?" (Boehm).

1. **Verification** checks that each work product conforms to its specification, using reviews, walkthroughs, inspections and static analysis. It is done without running the program as a whole.
2. **Validation** checks that the finished product meets the real needs of the user, by executing it in acceptance and system tests, often with real users.
3. **In the V-model** (Figure 6.1) the left arm is verification of each phase against the one before it, and the right arm is validation through unit, integration, system and acceptance testing.
4. **Example.** Reviewing the SRS of a result system for missing rules is verification; letting examiners enter real marks and check the output is validation.

| Aspect | Verification | Validation |
|---|---|---|
| Question | built right? | right product? |
| Method | reviews, inspections | testing, execution |
| Timing | during development | after build |
| Done by | developers, reviewers | testers, users |

*Conclusion.* Both are needed: a product can be built correctly to a wrong specification, and a right idea can be badly built.

**Q3 (10 marks). Explain white-box testing, statement, branch and path coverage, and basis path testing. For the function clamp(x) of Figure 6.3 draw the control-flow graph, compute V(G) and write the test cases.**

*Introduction.* White-box (structural) testing designs tests from the internal logic of the code, so the tester must see the source. It complements black-box testing: black-box finds missing functions, white-box finds untested code.

**Coverage criteria, weakest to strongest.** *Statement coverage* executes every statement at least once. *Branch (decision) coverage* makes every decision true and false at least once; it implies statement coverage. *Condition coverage* makes every simple condition true and false. *Path coverage* executes every path, which is usually impossible when there are loops. *Basis path testing* is the practical compromise: execute a set of independent paths whose size equals the cyclomatic complexity.

**The function.**
```text
def clamp(x):           # 1
    if x < 0:           # 2
        x = -x          # 3
    if x > 100:         # 4
        x = 100         # 5
    return x            # 6
```

**Control-flow graph and V(G).** Nodes: 6; edges: 1-2, 2-3, 2-4, 3-4, 4-5, 4-6, 5-6 = 7. V(G) = E - N + 2 = 7 - 6 + 2 = 3. Check by decisions: two decisions + 1 = 3. By regions: the graph has 2 inner regions + 1 outer = 3. So at least three tests are needed.

**Basis paths and test cases (Figure 6.3).**

| Path | Nodes | Input | Expected output |
|---|---|---|---|
| P1 | 1-2-4-6 | x = 50 | 50 |
| P2 | 1-2-3-4-6 | x = -5 | 5 |
| P3 | 1-2-4-5-6 | x = 150 | 100 |

These three tests give statement coverage (all six nodes) and branch coverage (each decision is true once and false once: x < 0 is true for P2 and false for P1 and P3; x > 100 is true for P3 and false for P1 and P2). A fourth path, 1-2-3-4-5-6 (x = -200, output 100), is not independent: it is a combination of the others, but it is a useful extra test for the combined condition.

**Advantages and limits.** White-box tests find unreachable code, logic errors and missing branches, and the coverage can be measured automatically. They cannot find a missing requirement, and 100% coverage does not mean 100% correct.

*Conclusion.* Cyclomatic complexity tells the tester the minimum number of tests; for clamp(x) it is three, and each is a real test with a known expected output.

**Q4 (10 marks). Explain software quality management. Discuss reliability measures, ISO 9000 and the Capability Maturity Model (CMM).**

*Introduction.* Software quality management makes sure that the product meets its requirements and the process is under control. It has three activities: quality assurance (define standards and processes), quality planning (select the standards for the project) and quality control (check that they are followed, through reviews and testing).

**Product and process quality.** Product quality is judged by the attributes of Figure 1.3 (maintainability, dependability, efficiency, acceptability). Process quality is judged by how well the development process is defined and followed; a good process makes good products more likely, although it does not guarantee them.

**Reliability measures (Figure 6.4).** *Probability of failure on demand* for rarely used systems such as a safety shutdown; *rate of occurrence of failures* (ROCOF); *mean time to failure* (MTTF); *mean time to repair* (MTTR); *availability* = MTTF / (MTTF + MTTR). For MTTF = 500 h and MTTR = 4 h: availability = 500 / 504 = 99.2063%, failure rate = 0.002 per hour and R(100) = exp(-100 / 500) = 0.8187. *Defect removal efficiency* DRE = found before release / (found before + found after): with 90 found before and 10 after, DRE = 90 / 100 = 90%.

**ISO 9000.** A family of international standards for quality management systems; ISO 9001 specifies requirements for the process, and ISO 90003 is the guide for software. It requires documented procedures, quality records, audits and corrective action. An ISO certificate shows that the company follows its own documented process; it does not certify the product itself.

**CMM (Figure 6.5).** Five levels: (1) *Initial*, ad hoc and dependent on individuals; (2) *Repeatable*, basic project management so that earlier successes can be repeated; (3) *Defined*, a standard process documented and used across the organisation; (4) *Managed*, processes and products are measured and controlled using data; (5) *Optimizing*, continuous process improvement using feedback and new ideas.

| Aspect | ISO 9001 | CMM |
|---|---|---|
| Nature | pass/fail certification | five maturity levels |
| Focus | meets documented quality system | continuous improvement path |
| Scope | any industry | software organisations |
| Result | certificate valid for a period | rating from level 1 to 5 |

*Conclusion.* Quality is built into the process, measured with metrics such as reliability and DRE, and improved over time; ISO 9000 shows that a process exists and CMM shows how mature it is.
