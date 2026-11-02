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
