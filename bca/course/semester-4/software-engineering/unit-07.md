---
subject: Software Engineering
grade: BCA Semester 4
unit: 7
title: Software Maintenance
hours: 3
area: BCA 252 · Software Engineering · Unit 7
---

Software that is used must be changed: laws change (a new tax rate), platforms change (a new Android version), users ask for features, and bugs surface. Surveys of long-lived systems put maintenance at more than half of total lifetime cost. This unit explains the evolving nature of software, the types of maintenance, how to predict and estimate it, re-engineering, and configuration management, which keeps changes under control.

::: key What this unit gives you
- Evolution of software and Lehman's laws.
- The types of maintenance: fault repair, adaptation, functionality addition or modification (and preventive).
- Maintenance prediction and cost estimation; re-engineering.
- Configuration management: configuration items, versioning, change control.
:::

## 7.1 The evolving nature of software

Software is never finished while it is used. **Lehman's laws** (from studies of large systems such as IBM's OS/360) state that: (1) a system that is used must be **continually changed** or becomes progressively less useful; (2) as it changes its **complexity increases** unless work is done to reduce it; (3) large systems have a **self-regulating evolution**, with a roughly constant rate of change; (4) the organisational work rate tends to be constant over a system's life; (5) the content of successive releases is roughly constant (new features per release do not rise indefinitely); (6) the user satisfaction declines unless the system is adapted; (7) quality seems to decline unless rigorously maintained. These explain why a neglected system rots: "code decay".

The **spiral of change**: change requests arrive → impact analysis → planning of a release → implementation → validation → release; urgent faults may jump the queue (emergency repair), which usually leaves a design that is worse than before.

## 7.2 Types of maintenance

| Type | Purpose | Share of effort (typical surveys) | Example |
|---|---|---|---|
| **Corrective (fault repair)** | fix coding, design and requirement errors | about 20 % | a rounding error in interest calculation |
| **Adaptive (software adaptation)** | modify for a changed environment: OS, hardware, law, other systems | about 20 % | support a new payment gateway API, a changed VAT rate |
| **Perfective (functionality addition or modification)** | add or improve features, performance, usability on user request | about 50 % | add a report, speed up search |
| **Preventive** | restructure to make future maintenance easier (refactoring, documentation) | about 5 % | splitting a 2,000-line function |

The percentages vary between studies; the robust finding is that **fault repair is a minority of the work**: most maintenance is changing the software to do new things. "Maintenance" is thus a misleading word; *evolution* is more accurate.

## 7.3 Maintenance cost and its factors

Maintenance is costlier per line than development because:

- **Team stability**: developers move on; new staff must learn the system.
- **Contractual responsibility**: the developer may have no incentive to design for change.
- **Staff skills**: maintenance is often given to juniors.
- **Program age and structure**: the code degrades, and documentation is out of date.

### Estimating maintenance effort (Boehm)

Annual change traffic **ACT** = fraction of the code changed (added or modified) per year. The **annual maintenance effort** is **AME = ACT × SDE**, where SDE is the software development effort.

::: example Annual maintenance for a 32 KLOC system
The organic-mode COCOMO estimate for 32 KLOC is SDE = 91.3 person-months (Unit 8). If 15 % of the code changes each year (ACT = 0.15), AME = 0.15 × 91.3 = **13.7 person-months per year**. Over a ten-year life that is about ten times that figure: comparable to or larger than the original effort, matching the claim in Unit 1.
:::

### Maintenance prediction

Predict **which parts** will need change and **how much** it will cost: *number of change requests* (a spike after release suggests low initial quality), *interface coupling* (tightly coupled components change together), *process metrics* (average time to fix, backlog of requests), and *complexity* (high cyclomatic complexity predicts defects, Unit 6). Decide whether the system is worth maintaining or should be replaced: measure business value against technical quality.

## 7.4 Re-engineering and reverse engineering

**Re-engineering** improves a legacy system *without changing its functionality* so that it is easier to maintain: re-document, restructure and translate the code (for example COBOL to Java), reorganise or normalise data, and modularise. **Reverse engineering** analyses the existing code to recover its design and specification (tools build call graphs, class diagrams, data dictionaries). **Forward engineering** then builds the new system. Re-engineering costs less than rewriting because the existing code embodies years of business knowledge. **Refactoring** is the same idea at a small scale, applied continuously with tests as a safety net.

| Option | When |
|---|---|
| Continue maintaining | system is stable, change is small |
| Re-engineer | quality is low but business value is high |
| Replace (buy or rewrite) | maintenance cost is above the cost of a new system |
| Discard | the business function is no longer needed |

## 7.5 Configuration management (CM)

Many people change many files; without control, no one knows what is in the released product. **Configuration management** is the discipline of managing change to the products of software development.

**Importance of CM:** it allows several developers to work in parallel without overwriting each other's work, reproduces any past release (for fixing a customer's old version), tracks who changed what and why, controls which changes enter a release, and builds the system reliably.

### Configuration items and baselines

A **configuration item (CI)** is anything placed under change control: source files, requirements and design documents, test cases, build scripts, libraries, user manuals. A **baseline** is a reviewed and agreed *version of a set of CIs* that serves as a basis for further development and can be changed only through a formal procedure.

### Versioning

Each CI has a **version** identified by number (and often a branch); modern systems use Git. A common numbering scheme is **MAJOR.MINOR.PATCH** (semantic versioning): MAJOR for incompatible changes, MINOR for compatible new features, PATCH for compatible fixes (2.4.1 → 2.4.2 is a bug fix; 2.4.1 → 2.5.0 adds a feature; 3.0.0 breaks compatibility). **Branches** let work proceed in parallel (feature, release, hotfix) and **merges** combine them; **tags** mark releases.

### Change management

1. A **change request** is submitted (what, why, who, severity).
2. **Impact analysis** estimates the affected components, effort and risk.
3. A **change control board (CCB)** approves, defers or rejects.
4. The change is made on a branch, tested and reviewed.
5. The CIs are updated and a new version released; the request is closed with traceability from request to commit.

Other CM activities: **system building** (automatically compile and link a given version, with a repeatable build), **release management** (what goes to customers, with release notes and migration), and **configuration audits**.

## 7.6 Maintenance in pictures: old machines, new demands

Software is never finished. Plate 7.1 shows three reminders of long-lived systems, and Figures 7.1 to 7.5 show the share of each type of maintenance, a Boehm estimate worked in person-months, the re-engineering cycle, a version history and the change-control process.

```photogrid label="7.1" cols="3" ratio="1.0" caption="Long-lived systems. (a) An IBM 1401 computer of the kind used for the 2028 BS (1971) census of Nepal; its programs were punched on cards and later copied to newer machines, a first example of migration. (b) The 'Y2K compliant' sticker of 1999: thousands of programs written decades earlier had to be changed before 1 January 2000, the largest adaptive-maintenance exercise in history. (c) A server room: a system that is still in use must be patched, backed up and moved to new hardware many times during its life."
@ photo id="bca101/ibm1401" cap="IBM 1401 (census era)"
fit 1.0
focus 0.5 0.5
@ photo id="bca252/y2k" cap="Y2K compliance sticker"
fit 1.0
focus 0.5 0.5
@ photo id="bca401/serverroom" cap="Server room"
fit 1.0
focus 0.5 0.5
```

```svgfig label="7.1" caption="Where maintenance effort goes. In classic surveys (Lientz and Swanson, 1980) about 21% of maintenance was corrective (fixing faults), 25% adaptive (new platform, law or environment), 50% perfective (new features and improvements) and 4% preventive (restructuring to avoid future problems). Only one fifth is fault repair; most maintenance is the software growing with its users."
f = Fig(580, 230)
data = [("Corrective: fix faults", 21, ROSE, RED), ("Adaptive: new environment", 25, SAND, AMBER), ("Perfective: new features", 50, MINT, TEAL), ("Preventive: restructure", 4, BLUE, NAVY)]
f.text(290, 14, "share of maintenance effort", size=11, color=NAVY, bold=True)
for i, (n, v, fl, st) in enumerate(data):
    y = 30 + i * 46
    f.text(190, y + 24, n, size=10.5, color=SLATE, bold=True, anchor="end")
    f.box(200, y + 6, v * 6, 32, "", fill=fl, stroke=st)
    f.text(200 + v * 6 + 8, y + 26, str(v) + "%", size=11, color=st, bold=True, anchor="start")
f.text(290, 220, "21 + 25 + 50 + 4 = 100", size=10, color=SLATE)
```

```svgfig label="7.2" caption="Boehm's estimate worked for one system. Development took 120 person-months. The annual change traffic (ACT), the fraction of the code changed each year, is 0.15, so the annual maintenance effort is AME = ACT x development effort = 0.15 x 120 = 18 person-months. Over 8 years maintenance totals 8 x 18 = 144 person-months, which is 144 / 264 = 54.5% of the lifetime effort, more than the whole development."
f = Fig(580, 200)
f.box(40, 40, 120 * 1.2, 50, "Development 120 pm", fill=BLUE, stroke=NAVY, size=11, bold=True)
for y in range(8):
    f.box(40 + 144 + y * 18 * 1.2, 40, 18 * 1.2, 50, "", fill=SAND, stroke=AMBER)
    f.text(40 + 144 + y * 18 * 1.2 + 10.8, 108, str(y + 1), size=9.5, color=AMBER, bold=True)
f.text(40 + 144 + 4 * 21.6, 128, "years of maintenance, 18 pm each (total 144 pm)", size=10.5, color=AMBER, bold=True)
f.text(290, 22, "lifetime effort: 120 + 144 = 264 person-months", size=11, color=NAVY, bold=True)
f.text(290, 170, "maintenance share = 144 / 264 = 54.5%", size=11, color=RED, bold=True)
```

```svgfig label="7.3" caption="The re-engineering cycle. Reverse engineering recovers a design and then a specification from the old code; restructuring cleans the code and data without changing behaviour; forward engineering builds the new system from the improved design. The vertical axis is the level of abstraction, so the cycle climbs up the left side and comes down the right."
f = Fig(580, 240)
f.box(20, 170, 130, 50, "Old system\n(code)", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(160, 110, 130, 40, "Recovered design", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(290, 50, 130, 40, "Specification", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(430, 110, 130, 40, "New design", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(430, 170, 130, 50, "New system\n(code)", fill=MINT, stroke=TEAL, size=11, bold=True)
f.arrow([(85, 170), (200, 150)], color=SLATE)
f.arrow([(225, 110), (330, 90)], color=SLATE)
f.arrow([(390, 90), (480, 110)], color=SLATE)
f.arrow([(495, 150), (495, 170)], color=SLATE)
f.text(100, 100, "reverse", size=10.5, color=AMBER, bold=True)
f.text(100, 116, "engineering", size=10.5, color=AMBER, bold=True)
f.text(500, 60, "forward", size=10.5, color=TEAL, bold=True)
f.text(500, 76, "engineering", size=10.5, color=TEAL, bold=True)
f.arrow([(150, 205), (430, 205)], color=SLATE, dash=True, label="restructuring and data re-engineering", lpos=(290, 224), lsize=9.5)
```

```svgfig label="7.4" caption="A version history. Releases 1.0 and 1.1 follow the main line; a bug-fix branch is cut from 1.1 for urgent patches while version 2.0 is developed on the main line. The fix is merged back so that 2.0 also has it. Every circle is a commit, every tag is a baseline that can be rebuilt exactly."
f = Fig(580, 200)
f.line(30, 60, 550, 60, color=NAVY, sw=2.4)
main = [(60, ""), (140, "v1.0"), (220, ""), (300, "v1.1"), (400, ""), (500, "v2.0")]
for x, t in main:
    f.circle(x, 60, 8, fill=(SAND if t else BLUE), stroke=(RED if t else NAVY))
    if t:
        f.text(x, 38, t, size=11, color=RED, bold=True)
f.line(300, 68, 340, 130, color=TEAL, sw=2.2)
f.line(340, 130, 440, 130, color=TEAL, sw=2.2)
for x in (340, 390, 440):
    f.circle(x, 130, 7, fill=MINT, stroke=TEAL)
f.text(390, 156, "branch: bug fixes for 1.1 (becomes 1.1.1)", size=10.5, color=TEAL, bold=True)
f.arrow([(447, 124), (492, 70)], color=TEAL, dash=True)
f.text(500, 100, "merge", size=10.5, color=TEAL, bold=True)
f.text(290, 188, "main line = development; tags = baselines", size=10.5, color=SLATE)
```

```svgfig label="7.5" caption="The change-control process. Every change request is logged, its impact on code, tests, documents and cost is analysed, and a change control board (CCB) approves, defers or rejects it. Approved changes are implemented on a branch, tested (including regression tests) and released as a new baseline; rejected requests are recorded with the reason."
f = Fig(580, 230)
steps = [("Change\nrequest", BLUE, NAVY), ("Impact\nanalysis", MINT, TEAL), ("CCB\ndecision", SAND, AMBER), ("Implement\non branch", MINT, TEAL), ("Regression\ntest", MINT, TEAL), ("New\nbaseline", ROSE, RED)]
for i, (t, fl, st) in enumerate(steps):
    x = 8 + i * 96
    f.box(x, 50, 84, 52, t, fill=fl, stroke=st, size=10, bold=True)
    if i < 5:
        f.arrow([(x + 84, 76), (x + 96, 76)], color=SLATE)
f.arrow([(234, 102), (234, 160), (60, 160)], color=RED, dash=True, label="rejected: record the reason", lpos=(150, 178), lsize=10)
f.arrow([(426, 102), (426, 150), (330, 150), (330, 102)], color=AMBER, dash=True, label="test fails", lpos=(378, 166), lsize=10)
```

### 7.6.1 Eight reasons why software maintenance is costly

1. **Maintainers must first understand the code.** Most of the effort of a change goes into reading, not typing, and the maintainer is often not the author. A change that takes ten minutes to type can take two days to understand. Good names, structure and documentation, as in Unit 5, cut this cost.
2. **Documentation is missing or out of date.** When the design documents were not updated, the source code is the only truth. Without them, a person fixing a bank's interest routine must guess what the original rule was. Keeping documents current is cheaper than rediscovering them.
3. **Staff change.** The programmers who knew the system leave for other jobs, especially in a market like Kathmandu where good developers move often. Knowledge walks out of the door with them. Handover notes, code reviews and shared ownership reduce the loss.
4. **Changes cause ripple effects.** A small change in one module can break another that depends on it, so every change needs impact analysis and regression testing. The stronger the coupling (Figure 4.2), the larger the ripple. This is why maintainers are careful and slow.
5. **Program structure decays with age.** Each quick fix adds a little disorder, so old programs become tangled and every later change is harder. This is the deterioration of Figure 1.2. Refactoring and re-engineering (Figure 7.3) are the remedies.
6. **The environment keeps changing.** Laws change (for example VAT or tax rules), browsers and operating systems are updated, and hardware ages, as the Y2K case in Plate 7.1 showed. Each change forces adaptive maintenance, which was 25% of the effort in Figure 7.1.
7. **Users keep asking for more.** Successful software attracts new requests, and perfective maintenance, about half of the total, is the largest share. Every new feature needs analysis, coding and testing like a small project. The cost grows with the number of users.
8. **Maintenance is often undervalued and badly contracted.** Many organisations give the work to junior staff and budget too little for it, although Figure 7.2 shows that it can exceed development effort. A separate development team and no warranty plan make the problem worse. Planning maintenance at design time is the best prevention.

## Formula and fact sheet

- Lehman: continuing change, increasing complexity, declining quality unless maintained.
- Maintenance types: corrective, adaptive, perfective, (preventive). Perfective is the largest share.
- AME = ACT × SDE.
- Re-engineering keeps functionality; reverse engineering recovers design; refactoring restructures code with tests.
- CM: configuration items, baselines, versioning (MAJOR.MINOR.PATCH), change control board.

## Chapter summary

- Used software must evolve; ignoring evolution causes decay (Lehman's laws).
- Maintenance is corrective, adaptive, perfective or preventive, with most effort spent on new or changed functionality, not on fixing faults.
- Maintenance is costly, and effort can be estimated from annual change traffic; re-engineering or replacement is chosen by comparing value and cost.
- Configuration management with baselines, versions and controlled change keeps releases reproducible and traceable.

## Practice

1. State four of Lehman's laws of software evolution.
2. Distinguish corrective, adaptive and perfective maintenance with examples.
3. Why does maintenance cost more per line than development?
4. A 32 KLOC system has development effort 91.3 person-months and 15 % annual change traffic. Estimate yearly maintenance effort.
5. Differentiate re-engineering, reverse engineering and refactoring.
6. Define configuration item and baseline; why is CM important?
7. Explain semantic versioning: what changes when a bug is fixed, a feature is added, and an incompatible change is made?
8. Describe the change-control process.

::: note Answers and worked solutions
**1.** Continuing change (a used system must change); increasing complexity (unless work is done to reduce it); self-regulation (stable rate of change); declining quality (unless adapted); also conservation of familiarity and organisational stability.
**2.** Corrective: fix a defect (wrong interest calculation). Adaptive: adjust to a changed environment (new tax rate, new OS version). Perfective: add or improve features (new report, faster search).
**3.** Team turnover and learning cost, no design-for-change incentive, junior staff, degraded structure and outdated documentation of old programs.
**4.** AME = ACT × SDE = 0.15 × 91.3 = **13.7 person-months per year** (see computation in 7.3).
**5.** Re-engineering: restructure and rebuild a legacy system without changing its functions. Reverse engineering: analyse code to recover design/specification. Refactoring: small, behaviour-preserving restructuring of code, backed by tests.
**6.** A configuration item is any work product under change control; a baseline is an approved version of a set of CIs that can be changed only formally. CM lets many people work in parallel, reproduces old releases and tracks every change.
**7.** MAJOR.MINOR.PATCH: a bug fix raises PATCH (2.4.1 → 2.4.2); a compatible new feature raises MINOR and resets PATCH (→ 2.5.0); an incompatible change raises MAJOR (→ 3.0.0).
**8.** Submit a change request; impact analysis; approval by the change control board; implement and test on a branch; update configuration items and release a new version; close the request with traceability.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the four types of software maintenance with examples.**

*Introduction.* Maintenance is the modification of software after delivery to correct faults, improve performance or adapt it to a changed environment (section 7.2).

1. **Corrective maintenance** fixes faults found in use. Example: a result system that shows a wrong GPA for students with a re-totalled mark is repaired. It was about 21% of effort in surveys (Figure 7.1).
2. **Adaptive maintenance** changes the software for a new environment: operating system, hardware, law or other systems. Example: adding the new 13% VAT rate or moving a billing system to a new database. About 25%.
3. **Perfective maintenance** adds features or improves performance and usability at the request of users. Example: adding a QR payment option to a fee system. The largest share, about 50%.
4. **Preventive maintenance** (software re-engineering or refactoring) improves structure and documentation so that future changes are easier, without changing behaviour. About 4%.

| Type | Trigger | Example |
|---|---|---|
| Corrective | fault report | fix wrong GPA |
| Adaptive | environment change | new VAT rate |
| Perfective | user request | QR payment |
| Preventive | foreseen problem | refactor code |

*Conclusion.* Most maintenance (perfective and adaptive) is not repair but evolution, which is why systems cost more to maintain than to build.

**Q2 (5 marks). What is software configuration management? Explain baselines, version control and change control.**

*Introduction.* Configuration management (CM) identifies and controls the items of a project (code, documents, test data) and every change to them, so that the team always knows exactly what is in each release.

1. **Configuration items.** Every product of the project that is under control: source files, the SRS, design documents, test plans and build scripts.
2. **Baselines.** A baseline is a reviewed and approved version of the items that can be changed only through formal change control, such as release 1.1 (Figure 7.4).
3. **Version control.** A tool such as Git stores every version, who changed it and why; branches allow parallel work and merges combine it.
4. **Change control.** A change request is analysed, approved by the change control board, implemented and tested, and issued as a new baseline (Figure 7.5).
5. **Benefits.** No lost work, easy rollback, reproducible builds and an audit trail of all changes.

*Conclusion.* Without CM, maintenance of a system with many versions and users becomes chaos.

**Q3 (10 marks). Explain software maintenance, its types, the factors that affect its cost and Boehm's method for estimating maintenance effort. Use the example of a 120 person-month system.**

*Introduction.* Software maintenance is the process of modifying a software system after it has been delivered. Unlike hardware, software does not wear out, but its environment and users' needs change, so a long-lived system is maintained for years; for most of its life it costs more than the original development.

**Types.** Corrective, adaptive, perfective and preventive (answer Q1; Figure 7.1 gives the typical shares 21%, 25%, 50% and 4%).

**Factors that raise the cost.** (1) Poor understanding of the program by the maintainer; (2) missing or old documentation; (3) staff turnover; (4) high coupling, so that changes ripple; (5) old, decayed structure; (6) an unstable environment and laws; (7) user demand; (8) weak maintenance contracts and planning (section 7.6.1).

**Boehm's estimate.** The annual maintenance effort is AME = ACT x SDE, where SDE is the software development effort in person-months and ACT is the *annual change traffic*, the fraction of the code that is added or modified in a year. For SDE = 120 person-months and ACT = 0.15: AME = 0.15 x 120 = 18 person-months per year. Over eight years the maintenance effort is 8 x 18 = 144 person-months, so the lifetime effort is 120 + 144 = 264 and the maintenance share is 144 / 264 = 54.5% (Figure 7.2). If the team has 3 maintainers, the yearly work is 18 / 3 = 6 months each.

**Maintenance prediction.** To decide how much maintenance will be needed, count the number of change requests per module, the number of interfaces and the complexity. Modules with high complexity and many change requests are the most costly, and they are candidates for re-engineering.

| Factor | Effect on cost | Remedy |
|---|---|---|
| poor documentation | more time to understand | keep documents current |
| high coupling | ripple effects | modular design |
| staff turnover | knowledge loss | reviews, handover |
| unstable environment | more adaptive work | configuration management |

*Conclusion.* Maintenance is a planned part of the life cycle, not an accident; estimating it with Boehm's model (Figure 7.2) and designing for change are the best ways to control it.

**Q4 (10 marks). Explain re-engineering and reverse engineering. Draw the re-engineering cycle and say when a system should be re-engineered instead of replaced.**

*Introduction.* Re-engineering is the process of restructuring or rewriting part or all of a legacy system, without changing its functionality, so that it becomes easier to maintain. Reverse engineering is the process of analysing a system to recover its design and specification from its code.

**Activities (Figure 7.3).**
1. **Source code translation.** Convert the program to a newer language or version, for example from an old COBOL to a modern language.
2. **Reverse engineering.** Analyse the program and produce a design and a specification, with tools that draw call graphs and data models.
3. **Program structure improvement.** Restructure the control flow and remove dead code and duplication.
4. **Program modularisation.** Group related parts and remove redundancy, increasing cohesion.
5. **Data re-engineering.** Clean and convert the data, and change formats and database schemas.
6. **Forward engineering.** Build the new system from the recovered, improved design.

**Forward, reverse and re-engineering compared.**

| Aspect | Forward | Reverse | Re-engineering |
|---|---|---|---|
| Direction | specification to code | code to specification | code, up and back down |
| Input | requirements | existing code | existing system |
| Output | new system | design, specification | restructured system |
| Changes functions? | yes, new | no | no |

**Re-engineer or replace?** Plot each system by *quality* (how many failures, how hard to change) and *business value* (how much the organisation depends on it). Low quality and low value: scrap it. Low quality and high value: re-engineer or replace, whichever is cheaper. High quality and high value: keep and maintain. High quality and low value: maintain only at low cost, or scrap when it fails. Re-engineering is preferred when the data and rules are valuable but the code is unstructured; it costs less and has less risk than a full rewrite.

**Benefits and risks.** Re-engineering reduces risk, since the functions are kept, and often costs less than a new system; but it has limits, as the structure from an old design cannot always be improved, and a mistake in reverse engineering is carried into the new system.

*Conclusion.* Re-engineering, with reverse engineering as its first step, extends the life of valuable legacy systems at a lower risk than replacing them.
