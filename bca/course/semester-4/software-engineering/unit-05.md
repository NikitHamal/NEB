---
subject: Software Engineering
grade: BCA Semester 4
unit: 5
title: Coding
hours: 2
area: BCA 252 · Software Engineering · Unit 5
---

Coding turns the design into executable code. Surveys show that programmers spend far more time *reading* code than writing it, so the aim of good coding is code that other people (and you, in six months) can understand and change. This short unit covers language and tool choice and the practices that make code good, with a few metrics.

::: key What this unit gives you
- Programming languages and development tools; how to select them.
- Good programming practices: naming, structure, comments, standards, defensive programming, reviews.
- Simple code metrics (LOC, Halstead) and their limits.
:::

## 5.1 Programming languages and development tools

**Language generations:** machine code (1GL), assembly (2GL), high-level procedural and object-oriented languages (3GL: C, Java, Python), and 4GLs (SQL, report generators). Scripting languages (Python, JavaScript, PHP) favour speed of development; systems languages (C, C++, Rust) favour control and speed of execution.

**Development tools:** editors and **IDEs** (VS Code, IntelliJ, Eclipse), **compilers/interpreters**, **debuggers**, **version control** (Git), **build tools** (Make, Maven, npm), **static analysers and linters**, **profilers**, **unit-test frameworks** (JUnit, pytest), **issue trackers**, and **continuous-integration** servers.

### Selecting languages and tools

| Factor | Question |
|---|---|
| Problem domain | web (JavaScript, PHP, Python), systems (C), data analysis (Python), Android (Kotlin/Java) |
| Performance | hard real-time or heavy computation may require C/C++ |
| Team skills and hiring | prefer what the team knows and the market supplies |
| Platform and integration | must run on the target and call existing libraries |
| Ecosystem | libraries, frameworks, community support, documentation |
| Maintainability | readability, static typing, long-term support |
| Cost and licence | open source or commercial |
| Existing standards | customer or organisation mandates |

## 5.2 Good programming practices

1. **Follow a coding standard**: agreed layout, naming and commenting rules (PEP 8 for Python, Google Java style). Consistency matters more than any particular choice.
2. **Use meaningful names**: `total_marks` rather than `tm`; constants in capitals (`MAX_LOANS`); functions as verbs, variables as nouns.
3. **Keep functions short** and single-purpose (functional cohesion, Unit 4): if you cannot name it with one verb, split it.
4. **Avoid magic numbers**: define `MAX_LOANS = 5` instead of scattering `5`.
5. **Avoid global variables** and deeply nested conditions (use guard clauses / early returns).
6. **Comment the *why*, not the *what***: the code shows what happens; the comment explains the reason or the unusual constraint. Keep comments in step with the code.
7. **Handle errors explicitly**: validate inputs, check return values, use exceptions, never silently ignore failures. This is **defensive programming**.
8. **Don't repeat yourself (DRY)**: copy-and-paste duplicates bugs; extract a function.
9. **Test as you code**: write unit tests with the code, ideally first (Unit 2, XP).
10. **Use version control** with small commits and clear messages.
11. **Refactor** regularly to keep the design clean, with tests as the safety net.
12. **Review code**: peer review or pair programming finds defects much more cheaply than testing.

::: example Before and after
Before:
```text
f(a):  if a>=40: if a>=60: if a>=80: r='A' else: r='B' else: r='C' else: r='F'
```
After (clear names, flat structure, no magic numbers hidden):
```text
GRADE_BANDS = [(80, 'A'), (60, 'B'), (40, 'C')]
def letter_grade(marks):
    for cutoff, letter in GRADE_BANDS:
        if marks >= cutoff: return letter
    return 'F'
```
The second version separates data (bands) from logic, so changing a cutoff is a one-line edit and cannot break the control flow.
:::

## 5.3 Code metrics

### Lines of code (LOC)

Easy to count, but depends on language and style: the same function takes far fewer lines in Python than in C. Used for estimating (COCOMO, Unit 8) and for normalising defect rates. **Defect density** = defects ÷ KLOC; for example 45 defects in 32 KLOC is 1.41 defects per KLOC.

### Halstead's measures

Count the **operators** and **operands** in a program: n₁ distinct operators, n₂ distinct operands, N₁ and N₂ their total occurrences. Then:

- Vocabulary n = n₁ + n₂; length N = N₁ + N₂;
- **Volume V = N log₂ n** (bits needed to write the program);
- **Difficulty D = (n₁/2) × (N₂/n₂)**; **Effort E = D × V**;
- Estimated bugs B ≈ V/3000.

For a small routine with n₁ = 10, n₂ = 7, N₁ = 24, N₂ = 15: n = 17, N = 39, V = 159.4, D = 10.71, E = 1708 and B ≈ 0.053. Halstead's measures capture size and "mental effort" but depend on how tokens are counted, and their predictive value is limited.

### Cyclomatic complexity

McCabe's measure of the number of independent paths; computed and used in Unit 6.

::: caution Metrics inform; they do not judge
A function with high complexity is a candidate for review, not automatically bad. Never reward programmers by lines of code: it encourages bloated code. Use metrics for trends and for finding hot-spots.
:::

## Formula and fact sheet

- Halstead: n = n₁ + n₂; N = N₁ + N₂; V = N log₂ n; D = (n₁/2)(N₂/n₂); E = DV.
- Defect density = defects / KLOC.
- Practices: standard, naming, short functions, no magic numbers, defensive programming, DRY, reviews, version control, tests.

## Chapter summary

- Language and tool selection depends on problem, performance, team skill, platform, ecosystem and cost.
- Good code follows a standard, uses clear names, is short and cohesive, handles errors, and is reviewed and tested.
- LOC and Halstead measures describe size and effort but must be interpreted with care.

## Practice

1. List six factors for choosing a programming language for a project.
2. Explain five good programming practices.
3. What is defensive programming? Give an example.
4. Compute Halstead volume for n₁ = 10, n₂ = 7, N₁ = 24, N₂ = 15.
5. Why are lines of code a poor measure of programmer productivity?
6. What is a magic number and why should it be avoided?
7. Why is code review effective?

::: note Answers and worked solutions
**1.** Problem domain, performance needs, team skills, target platform and integration, library ecosystem, maintainability, cost/licence, and customer standards.
**2.** Any five: coding standards; meaningful names; short single-purpose functions; no magic numbers; comments explaining *why*; DRY; explicit error handling; version control; unit tests; refactoring; reviews.
**3.** Writing code that anticipates misuse and failure: validate inputs, check return codes, handle exceptions. Example: checking that a divisor is non-zero and that a file opened successfully before using them.
**4.** n = 17, N = 39, V = N log₂ n = 39 × 4.087 = **159.4** bits.
**5.** LOC depends on language and style, and rewards verbose code; it ignores design quality, testing and reuse. A skilled programmer may solve a problem with fewer lines.
**6.** A literal number whose meaning is unclear (`if (x > 5)`). It hides intent and must be changed everywhere when the value changes; use a named constant instead.
**7.** Reviewers find defects early, when they are cheap to fix, spread knowledge and enforce standards; inspections typically find more defects per hour than testing.
:::
