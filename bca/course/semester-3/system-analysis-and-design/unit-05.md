---
subject: System Analysis and Design
grade: BCA Semester 3
unit: 5
title: Implementation and Maintenance
hours: 4
area: BCA 204 · System Analysis and Design · Unit 5
---

The design is finished; now the system must be built, tested, installed, documented, taught to its users and kept alive for years. In practice **maintenance consumes more effort than all earlier phases together**.

::: key What this unit gives you
- The implementation activities: coding, testing, installation, documentation, training and support.
- Software testing levels and techniques, with a worked test-case example.
- Installation strategies; documentation; organisational issues.
- Types of maintenance, how it is carried out, and its cost.
:::

## 5.1 System implementation

Implementation activities: **coding** (programming to the design standards), **testing**, **installation** (converting from the old system), **documentation** (system and user), **training** and **support**, and then a **post-implementation review**. The deliverable is a working system accepted by users.

### Software application testing

Testing is running the software to find errors; it can show the presence of bugs, never their absence. **Verification** asks "are we building the product right?" (meets design); **validation** asks "are we building the right product?" (meets user need).

| Level | What is tested | By whom |
|---|---|---|
| **Unit (module) test** | one program/function in isolation, using stubs/drivers | programmer |
| **Integration test** | modules working together (top-down, bottom-up, big-bang) | developers/testers |
| **System test** | the whole system: functions, performance, security, recovery | test team |
| **Acceptance test** | against the user's requirements: **alpha** (in-house) and **beta** (selected real users); also user acceptance test (UAT) | users |

**Techniques:** **black-box** (from specifications: test inputs and outputs without looking at code; equivalence classes, boundary values), **white-box** (from the code: cover statements, branches, paths). Others: **regression testing** (re-run old tests after a change), **stress/load testing**, **usability testing**, **security testing**. A **test case** lists the input, the steps, the expected result and the actual result. Test both **valid and invalid** data.

::: example Worked example: boundary-value test cases
Requirement: marks are an integer from 0 to 100; 40 or above is a pass.
Equivalence classes: below 0 (invalid), 0–39 (fail), 40–100 (pass), above 100 (invalid), non-numeric (invalid).
Boundary values to test: −1, 0, 1, 39, 40, 41, 99, 100, 101, plus "abc" and blank.
Expected results: −1 → "invalid"; 0 → fail; 39 → fail; 40 → pass; 100 → pass; 101 → "invalid"; "abc" → "invalid". Eleven well-chosen cases cover the rule far better than hundreds of random numbers, because defects cluster at the edges (`>=` mistyped as `>` is caught only by testing exactly 40).
:::

**Test planning:** a **test plan** sets scope, strategy, schedule, roles, environment and exit criteria; defects are logged with severity, steps to reproduce and status and tracked to closure.

### Installation

**Installation** replaces the old system with the new one, along with converting data, training, and sometimes hardware.

| Strategy | Description | Risk | Cost | Best when |
|---|---|---|---|---|
| **Direct (cold turkey)** | switch off old, switch on new at a date | **highest** | lowest | system is not critical, or old one is failing |
| **Parallel** | run old and new together until the new is trusted | lowest | **highest** (double work) | critical systems (payroll, banking) |
| **Phased (staged)** | introduce module by module or function by function | medium | medium | large systems that divide into parts |
| **Pilot (single location)** | install at one branch or department first | low | medium | many similar sites |

Installation also covers **data conversion** (cleaning, mapping, loading and reconciling data from the old system), **site preparation**, a **cutover plan** with a **back-out plan**, and a **go-live** support team.

### Documenting the system

**System documentation** (for maintainers): requirements, DFDs and ERDs, design specifications, data dictionary, program source with comments, test plans and results. **User documentation** (for users): user manual, quick-start guide, tutorials, FAQs, **online help** and **context-sensitive help**, release notes. Good documentation is written for its reader, is kept up to date with the system, and uses screenshots and examples. In agile projects it is "just enough", with working code and tests as the primary documentation.

### Training and supporting users

**Training** types: formal classroom, one-to-one, **on-the-job**, computer-based/e-learning and videos, and **train-the-trainer**. Training content: system purpose, how to do each task, error handling, who to call. **Support:** a **help desk** (phone, chat, ticketing), an **information centre**, power users in each department, FAQs and a **knowledge base**, plus a feedback channel for change requests. Plan training before go-live, with practice on a training copy of the system.

### Organisational issues in implementation

A technically perfect system fails if people reject it. Issues: **resistance to change** (fear of job loss, extra work, loss of status); **user involvement** and sponsor support; **management of expectations**; **data ownership and security** issues; **cost and time overruns**; and the effect on jobs and workflow. Measures: involve users from analysis onward, communicate honestly and early, train well, run a pilot, and reward adoption. A **post-implementation review** after a few months compares the achieved benefits and costs with the plan (Unit 2) and lists lessons learned. **System success** is measured by use, user satisfaction, quality of information, and impact on the organisation.

## 5.2 System maintenance

**Maintenance** is everything done after installation to keep the system useful. Software does not wear out, but business, law and technology change around it. Typically 60–80% of total system cost over its life is maintenance.

| Type | Purpose | Typical share | Example |
|---|---|---|---|
| **Corrective** | fix defects | ~20% | wrong fee total on a report |
| **Adaptive** | adapt to a changed environment | ~20% | new tax rate, new operating system or database version |
| **Perfective** | add or improve functions, performance, usability | **~50%** | a new report, faster search |
| **Preventive** | restructure to avoid future problems | ~5% | refactoring, updating documentation |

### Conducting systems maintenance

The maintenance process mirrors a small SDLC: (1) **obtain a maintenance request** (a change request form describing the problem or need); (2) **analyse** it: classify, judge impact and cost, **prioritise** (emergency fixes first); (3) **design** the change and its effect on other parts; (4) **implement and test** (including regression tests); (5) **deliver and update documentation** and inform users. Organisations use a **change control board** to approve changes.

**Configuration management** keeps track of every version of every component (**version control** such as Git), **builds** and **releases**, so a faulty change can be rolled back and the production system is reproducible. **Factors affecting maintenance cost:** number and quality of **documentation**, code **complexity** and structure, staff experience and turnover, the **age** of the system, use of standards, the **number of users**, and the quality of the original development. The best way to cut maintenance cost is to invest in **quality at analysis and design**. Eventually a system reaches the end of its useful life: when the cost of change exceeds the cost of **replacement**, a new project starts at Unit 2.

## Formula and fact sheet

- Testing levels: unit → integration → system → acceptance (alpha, beta, UAT). Black-box vs white-box.
- Boundary-value testing: test at, just below and just above every limit.
- Installation: direct (riskiest), parallel (safest, costliest), phased, pilot.
- Maintenance types: corrective, adaptive, perfective (largest share), preventive. Maintenance is the majority of lifetime cost.

## Chapter summary

- Implementation covers coding, multi-level testing, installation, documentation, training and support, and must manage organisational change.
- Installation strategies trade risk against cost; documentation serves maintainers and users.
- Maintenance (corrective, adaptive, perfective, preventive) is the longest and costliest phase, governed by change control and configuration management.

## Practice

1. Differentiate verification and validation.
2. Describe unit, integration, system and acceptance testing.
3. Differentiate black-box and white-box testing; write boundary test values for an age field accepting 18 to 60.
4. Compare direct, parallel, phased and pilot installation; which is suited to a payroll system?
5. List system and user documentation items.
6. Suggest four reasons for user resistance and how to reduce it.
7. Explain the four types of maintenance with examples.
8. Why is maintenance often the biggest cost?
9. What is configuration management and why is it needed?

::: note Answers and worked solutions
**1.** Verification: the product conforms to its specification (built right). Validation: it satisfies the user's real need (right product).
**2.** Unit: single module in isolation. Integration: modules together. System: complete system against the requirements and non-functional needs. Acceptance: users confirm it meets their needs.
**3.** Black-box tests behaviour from the specification; white-box tests internal logic. Boundary values: 17, 18, 19, 59, 60, 61 (plus a non-numeric and blank).
**4.** See the installation table. Payroll is critical, so **parallel** (compare old and new results for a few pay cycles).
**5.** System: requirements, DFDs/ERDs, design specs, data dictionary, source, test plans. User: manual, quick guide, tutorials, FAQ, help.
**6.** Fear of job loss, extra workload, loss of control, dislike of change. Reduce by early involvement, communication, training, a pilot and visible management support.
**7.** Corrective (fix a defect), adaptive (new tax rate), perfective (new report or speed-up), preventive (refactoring for future ease).
**8.** The system lives for years while the business, laws and technology change, and each change must be analysed, built, tested and documented; poor design and documentation make each change costlier.
**9.** Control of versions and changes to all components so any version can be rebuilt or rolled back, and changes are authorised and traceable.
:::
