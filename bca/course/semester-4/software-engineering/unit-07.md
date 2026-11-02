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
