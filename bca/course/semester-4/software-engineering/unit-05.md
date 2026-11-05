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

## 5.4 Coding in pictures: from punched cards to code review

Coding is the step where a design becomes instructions the computer can run, but the program is read many more times than it is written. Plate 5.1 shows how programming has changed and what has stayed the same; Figures 5.1 to 5.3 show readable code, a quality pipeline and the Halstead numbers for a routine.

```photogrid label="5.1" cols="3" ratio="1.0" caption="Three eras of coding. (a) An 80-column punched card: one card held one line of a COBOL program, so a program was a box of cards and a typing error meant punching a new card. (b) A PDP-11 minicomputer, the machine on which the C language and early UNIX were developed in the early 1970s. (c) Pair programming: two programmers share one screen, one writing and one reviewing, which is today's quickest way to catch mistakes. The tools changed, but the aims of Unit 5 did not: code that is correct, readable and easy to change."
@ photo id="bca252/card" cap="COBOL punched card"
fit 1.0
focus 0.3 0.5
@ photo id="bca102/pdp11" cap="PDP-11 minicomputer"
fit 1.0
focus 0.5 0.5
@ photo id="bca256/pair" cap="Pair programming"
fit 1.0
focus 0.5 0.5
```

```svgfig label="5.1" caption="The same calculation written badly and well. Both give the same answer, Rs 1,130 for a price of Rs 1,000 with Nepal's 13% value added tax (VAT), but only the right-hand version tells a reader what it does. It uses meaningful names, a named constant instead of the 'magic number' 0.13, one small function for one job, and a comment that explains why, not what."
f = Fig(580, 230)
f.box(8, 10, 270, 170, "", fill=ROSE, stroke=RED)
f.text(143, 30, "Hard to read", size=11, color=RED, bold=True)
for i, s in enumerate(["def f(a, b):", "\u00a0\u00a0\u00a0\u00a0x = a * 0.13", "\u00a0\u00a0\u00a0\u00a0y = a + x", "\u00a0\u00a0\u00a0\u00a0return y", "", "print(f(1000, 5))"]):
    f.text(22, 56 + i * 18, s, size=10.5, color=SLATE, anchor="start")
f.box(302, 10, 270, 170, "", fill=MINT, stroke=TEAL)
f.text(437, 30, "Easy to read", size=11, color=TEAL, bold=True)
for i, s in enumerate(["VAT_RATE = 0.13  # Nepal standard rate", "", "def price_with_vat(price):", "\u00a0\u00a0\u00a0\u00a0vat = price * VAT_RATE", "\u00a0\u00a0\u00a0\u00a0return price + vat", "", "print(price_with_vat(1000))"]):
    f.text(314, 56 + i * 18, s, size=10, color=SLATE, anchor="start")
f.text(143, 204, "unclear names, magic number, unused argument", size=10, color=RED, bold=True)
f.text(437, 204, "clear names, named constant, one job", size=10, color=TEAL, bold=True)
```

```svgfig label="5.2" caption="A coding quality pipeline. Each change passes through cheap automatic checks before the expensive human check: the formatter and linter enforce the coding standard, the unit tests check behaviour, a peer reviews design and clarity, and only then is the change merged into the shared repository. A failure at any stage sends the change back to its author."
f = Fig(580, 170)
steps = [("Write code\nin small steps", BLUE, NAVY), ("Format and\nlint", MINT, TEAL), ("Run unit\ntests", MINT, TEAL), ("Peer code\nreview", SAND, AMBER), ("Merge to\nrepository", ROSE, RED)]
for i, (t, fl, st) in enumerate(steps):
    x = 8 + i * 116
    f.box(x, 40, 100, 56, t, fill=fl, stroke=st, size=10.5, bold=True)
    if i < 4:
        f.arrow([(x + 100, 68), (x + 116, 68)], color=SLATE)
f.arrow([(380, 96), (380, 140), (58, 140), (58, 96)], color=RED, dash=True)
f.text(220, 132, "failure: fix and try again", size=10, color=RED, bold=True)
f.text(116, 22, "automatic checks", size=10, color=TEAL, bold=True)
f.text(446, 22, "human check", size=10, color=AMBER, bold=True)
```

```svgfig label="5.3" caption="Halstead's measures for a routine with 12 distinct operators, 8 distinct operands, 35 operator occurrences and 22 operand occurrences. Vocabulary n = 20, length N = 57, volume V = N log2 n = 246.3, difficulty D = (n1 / 2)(N2 / n2) = 16.5, effort E = D x V = 4064 and estimated bugs B = V / 3000 = 0.082. A hundred such routines would be expected to hide about eight bugs."
f = Fig(580, 230)
f.text(290, 14, "Halstead measures of one routine", size=11, color=NAVY, bold=True)
vals = [("vocabulary n", 20, BLUE, NAVY), ("length N", 57, BLUE, NAVY), ("volume V", 246.3, MINT, TEAL), ("difficulty D", 16.5, SAND, AMBER)]
mx = 260
for i, (nm, v, fl, st) in enumerate(vals):
    y = 30 + i * 42
    f.text(120, y + 20, nm, size=10.5, color=SLATE, bold=True, anchor="end")
    f.box(130, y + 4, 300 * v / mx, 28, "", fill=fl, stroke=st)
    f.text(130 + 300 * v / mx + 8, y + 22, str(v), size=10.5, color=st, bold=True, anchor="start")
f.text(290, 212, "effort E = 4064   estimated bugs B = 0.082", size=11, color=RED, bold=True)
```

### 5.4.1 Eight rules for readable and maintainable code

1. **Use meaningful names.** A name like `price_with_vat` tells the reader the purpose without a comment, while `f` and `x` force them to guess. Programs are read far more often than they are written, so a minute spent on a good name saves hours later. Follow the naming style of the language and the team.
2. **Keep functions small and single-purpose.** A function that does one thing is easy to test, reuse and understand, and it has high cohesion. If you cannot describe it in one sentence without "and", split it. A bank's interest routine should not also print the statement.
3. **Avoid magic numbers.** Replace a bare 0.13 or 40 by a named constant such as `VAT_RATE` or `PASS_MARKS`. When the law or rule changes, the value is edited in one place and cannot be missed elsewhere. This one habit prevents many bugs in billing and result systems.
4. **Follow a coding standard.** Agree on indentation, naming, file layout and comment style, and let a formatter and linter enforce it (Figure 5.2). Consistent code reads like one author wrote it, so a new team member is productive sooner. Arguments about style disappear.
5. **Comment why, not what.** The code shows what happens; a comment should explain the reason, such as "rounding follows the University rule". Out-of-date comments are worse than none, so keep them short and next to the code they explain. Avoid commenting the obvious.
6. **Handle errors and check inputs.** Validate every value from a user or another system, and decide what to do when a file is missing or a network call fails. A program that fails with a clear message is much easier to repair than one that silently produces wrong results. The Ariane 501 failure came from an unchecked conversion.
7. **Use version control with small commits.** Each commit changes one thing and has a clear message, so a fault can be traced to the change that caused it and undone. Branches let people work in parallel without breaking each other. Git is used by almost every software team in Nepal.
8. **Review code before merging.** A second pair of eyes finds mistakes, shares knowledge and spreads good habits, as Plate 5.1c shows. Reviews are cheaper than finding the same fault in testing or after release. Keep reviews short, polite and focused on the code, not the person.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What are coding standards and guidelines? Why are they used? Give five examples.**

*Introduction.* A coding standard is a set of rules that every programmer on a project must follow when writing code; guidelines are recommendations that explain good practice (section 5.2).

1. **Naming.** Variables and functions have meaningful names in one style, for example `total_marks`, not `tm`.
2. **Layout.** Indentation, line length and brace placement are the same everywhere, normally enforced by a formatter.
3. **Comments and headers.** Each file and function states its purpose, inputs and outputs; comments explain why.
4. **Constants and limits.** No magic numbers; a function has a limited size and number of parameters.
5. **Error handling and prohibited constructs.** Inputs are validated, errors are reported in one agreed way, and unsafe features (such as unrestricted `goto` or global variables) are banned.
6. **Why used.** Standards make code uniform and easy to read, reduce defects, make reviews faster, help new members and keep maintenance cost low (Figure 5.1).

*Conclusion.* Because most of the life of software is maintenance, a coding standard saves more time than it costs.

**Q2 (5 marks). Explain Halstead's software science measures. For a program with n1 = 12, n2 = 8, N1 = 35 and N2 = 22 calculate the vocabulary, length, volume, difficulty, effort and estimated bugs.**

*Introduction.* Halstead (1977) measured a program by counting its operators and operands. Operators are symbols and keywords that act (`+`, `if`, `=`); operands are the data they act on (variables and constants).

1. **Vocabulary and length.** n = n1 + n2 = 12 + 8 = 20; N = N1 + N2 = 35 + 22 = 57.
2. **Volume.** V = N log2 n = 57 x log2 20 = 57 x 4.3219 = 246.3 bits, the size of the program in an information sense.
3. **Difficulty.** D = (n1 / 2) x (N2 / n2) = (12 / 2) x (22 / 8) = 16.5, which grows when many operators are used and operands are reused.
4. **Effort.** E = D x V = 16.5 x 246.3 = 4064, the number of elementary mental decisions needed to write the program.
5. **Bugs.** B = V / 3000 = 0.082, so about one bug in twelve such routines.

| Measure | Formula | Value |
|---|---|---|
| Vocabulary | n1 + n2 | 20 |
| Length | N1 + N2 | 57 |
| Volume | N log2 n | 246.3 |
| Difficulty | (n1/2)(N2/n2) | 16.5 |
| Effort | D x V | 4064 |
| Bugs | V/3000 | 0.082 |

*Conclusion.* Halstead's numbers are easy to calculate and good for comparing routines, but they depend on how operators and operands are counted and ignore program structure, so they inform rather than judge (Figure 5.3).

**Q3 (10 marks). Explain good programming practices and the main code metrics (LOC, Halstead, cyclomatic complexity). How do they help to improve software quality?**

*Introduction.* Coding turns the design into executable code. Because a program is read many times and changed throughout its life, quality at the coding stage is measured by how easy the code is to understand, test and change, not only by whether it runs.

**Good programming practices.**
1. Use meaningful names and a consistent style (coding standard).
2. Write small functions with one purpose and high cohesion, using structured control flow only.
3. Replace magic numbers by named constants (`VAT_RATE = 0.13`, Figure 5.1).
4. Comment the reason, not the obvious, and keep comments current.
5. Validate inputs and handle errors explicitly.
6. Use version control and small commits.
7. Review code, and run automatic checks first (Figure 5.2).
8. Avoid duplicated code, because a fault must then be fixed in many places.

**Code metrics.**
*Lines of code (LOC).* The simplest size measure; easy to count but depends on language and style, so it is used only for estimation (COCOMO in Unit 8) and for defect density (defects per KLOC). *Halstead measures.* From operator and operand counts: vocabulary, length, volume V = N log2 n, difficulty, effort and estimated bugs (Figure 5.3: V = 246.3, E = 4064, B = 0.082). *Cyclomatic complexity.* V(G) = E - N + 2 for the control-flow graph, equal to the number of decisions plus one; it gives the minimum number of tests (Unit 6). A function with V(G) above 10 is usually split.

| Metric | Measures | Used for |
|---|---|---|
| LOC / KLOC | size | effort estimate, defect density |
| Halstead | size, difficulty, effort | comparing routines, bug estimate |
| Cyclomatic V(G) | logical complexity | number of tests, refactoring |

**How they improve quality.** Metrics find hot spots: a routine with high volume and high complexity is likely to contain faults, so it is reviewed and tested more. Trends over time show whether the code is getting harder to maintain. However, metrics must not be used to rate programmers; rewarding lines of code only produces bloated programs.

*Conclusion.* Disciplined coding gives code that others can maintain, and metrics give the evidence to decide where to review, test and refactor; both reduce the high cost of maintenance.
