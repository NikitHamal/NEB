---
subject: Software Project Management
grade: BCA Semester 7
unit: 6
title: Software Quality Management
hours: 5
area: BCA 402 · Software Project Management · Unit 6
---

A mobile banking app that calculates a balance wrongly by one rupee is "almost correct" but unusable. A hospital system that is down every Friday is "mostly available" but dangerous. **Quality** decides whether users trust, adopt and pay for software, and it is far cheaper to build in than to inspect in. This unit defines software quality, explains the ISO 9126 model, shows where quality fits into project planning, and introduces Total Quality Management (TQM) and Six Sigma.

::: key What this unit gives you
- Defining software quality and why it is important; the cost of quality.
- The ISO 9126 quality model: six characteristics and their sub-characteristics.
- The place of quality in software planning: quality plan, reviews, testing, defect-removal efficiency, quality gates.
- TQM principles and PDCA; Six Sigma with DMAIC and sigma levels; SQA and process maturity models (CMMI, ISO 9001).
:::

## 6.1 Software quality: definition and importance

**Quality** has several definitions, all of which are useful:

- **Fitness for use** (Juran): the software does what the user needs, in the user's environment.
- **Conformance to requirements** (Crosby): the product matches its specification; "quality is free" because defects cost more than prevention.
- **IEEE definition:** the degree to which a system, component or process meets specified requirements and customer or user needs or expectations.
- **Product view versus process view.** *Product quality* is a property of the software itself (few defects, fast, usable). *Process quality* is a property of how it is built (reviews, testing, configuration control). A good process makes good products likely but does not guarantee them.

Quality is also **user-defined**: a developer thinks of correct code, a user thinks of ease of use and speed, an operator thinks of maintainability. This is why requirements must state quality needs in **measurable** terms: "the system shall respond within 2 seconds for 95% of search requests with 500 concurrent users" is a quality requirement; "the system shall be fast" is not.

### Why software quality is important

1. **Cost of defects grows with time.** A requirements error that costs 1 unit to fix when found in requirements review costs about 10 times that in coding, and 100 times or more after release.
2. **Safety and money.** Software controls aircraft, medical devices, banks. Failures such as the Ariane 5 (1996) and Therac-25 radiation overdoses show the cost.
3. **Reputation and competitiveness.** Users abandon unreliable apps in days.
4. **Maintenance burden.** Poor quality produces corrective maintenance that eats 40 to 80% of lifetime cost.
5. **Legal and contractual obligations,** for example data-protection and Nepal's Electronic Transactions Act.
6. **Team morale and productivity.** Firefighting defects leaves little time for new features.

### The cost of quality

| Component | Meaning | Examples |
|---|---|---|
| **Prevention** | stop defects happening | training, standards, design reviews, tools |
| **Appraisal** | find defects | testing, inspections, audits |
| **Internal failure** | defects found before delivery | rework, retesting, debugging |
| **External failure** | defects found by the customer | support calls, patches, refunds, lost customers |

Prevention and appraisal are the "cost of conformance"; failures are the "cost of non-conformance." Spending more on prevention reduces the total, because external failure is by far the most expensive.

## 6.2 The ISO 9126 quality model

**ISO/IEC 9126** (1991, revised 2001) was the international standard for software product quality. It has been replaced by **ISO/IEC 25010** (SQuaRE, 2011), which keeps the same structure with two more characteristics (security and compatibility), but ISO 9126 is the model named in the syllabus. It defines **six characteristics**, each broken into sub-characteristics.

```svgfig label="6.1" caption="The six quality characteristics of ISO 9126 with their sub-characteristics."
f = Fig(640, 270)
f.box(240, 8, 160, 34, "Software quality", fill="#ccfbf1", stroke=TEAL, color=NAVY, size=12, bold=True)
chars = [("Functionality", ["suitability", "accuracy", "interoperability", "security"]),
         ("Reliability", ["maturity", "fault tolerance", "recoverability"]),
         ("Usability", ["understandability", "learnability", "operability", "attractiveness"]),
         ("Efficiency", ["time behaviour", "resource use"]),
         ("Maintainability", ["analysability", "changeability", "stability", "testability"]),
         ("Portability", ["adaptability", "installability", "co-existence", "replaceability"])]
for i, (c, subs) in enumerate(chars):
    x = 6 + i * 105
    f.box(x, 74, 100, 32, c, fill=BLUE, color=NAVY, size=10.5, bold=True)
    f.arrow([(320, 42), (320, 58), (x + 50, 58), (x + 50, 74)], color=SLATE, sw=1.2)
    for k, s in enumerate(subs):
        f.box(x + 3, 118 + k * 34, 94, 28, s, fill="#fde68a", stroke=AMBER, color=NAVY, size=9)
```

| Characteristic | Question it answers | Sub-characteristics | Example measure |
|---|---|---|---|
| **Functionality** | Does it provide the functions needed? | suitability, accuracy, interoperability, security, compliance | % of requirements implemented; calculation error rate |
| **Reliability** | Does it keep working? | maturity, fault tolerance, recoverability | MTBF; failures per 1,000 hours; availability |
| **Usability** | Is it easy to learn and use? | understandability, learnability, operability, attractiveness | time to complete a task; error rate of new users |
| **Efficiency** | Is it fast and economical with resources? | time behaviour, resource utilisation | response time; memory used |
| **Maintainability** | How easily can it be changed? | analysability, changeability, stability, testability | mean time to fix; cyclomatic complexity |
| **Portability** | Can it be moved to another environment? | adaptability, installability, co-existence, replaceability | effort to port; number of supported platforms |

ISO 9126 describes three views: **internal quality** (measured on code and design), **external quality** (measured by running the software) and **quality in use** (effectiveness, productivity, safety and satisfaction in real use). The standard also gives **metrics** for each.

### Other quality models

**McCall's model** (1977) groups 11 factors into product operation, product revision and product transition. **Boehm's model** has a hierarchy of general utility, as-is utility, maintainability and portability. **FURPS+** (Hewlett-Packard) lists Functionality, Usability, Reliability, Performance, Supportability. ISO 9126 combines and standardises these.

### Some useful quality metrics

- **Defect density** = defects ÷ size (KLOC or FP). For 34 defects in 12 KLOC the density is 34/12 = **2.83 defects per KLOC**.
- **Availability** = MTTF ÷ (MTTF + MTTR). With MTTF = 400 hours and MTTR = 4 hours, availability = 400/404 = **0.990 = 99.0%**, about 87 hours of downtime per year.
- **Defect removal efficiency (DRE)** = defects found before release ÷ total defects found (before and after). With 90 found in testing and 10 reported by users, DRE = 90/100 = **90%**. Good teams reach 95% or more.
- **Test coverage**, **mean time to repair**, **customer-reported problems per month**.

## 6.3 Place of software quality in software planning

Quality is not a phase at the end: it is planned from the start.

1. **Define quality requirements** for the product in measurable terms (ISO 9126 characteristics, with targets).
2. **Select the process** and standards (coding rules, review rules, documentation templates).
3. **Prepare a quality plan** (below).
4. **Carry out quality activities throughout:** reviews, inspections, testing, audits.
5. **Measure and control** with metrics; use **quality gates** (stage-end checks) before moving on.
6. **Improve** the process using the results (root cause analysis).

### The quality plan

A quality plan (or Software Quality Assurance plan) states: the quality objectives and metrics; the standards and procedures to be used; the reviews and tests, who does them and when; the entry and exit criteria for each stage; defect tracking and reporting; roles and responsibilities; tools; and the criteria for acceptance and release.

### Verification, validation and reviews

- **Verification:** "Are we building the product right?" (conforms to specification; reviews, inspections, static analysis).
- **Validation:** "Are we building the right product?" (meets the user's needs; testing, user acceptance).
- A **walkthrough** is an informal author-led presentation. A **Fagan inspection** is a formal review with defined roles (moderator, author, reader, recorder, inspectors), entry and exit criteria and recorded defects; it finds 60 to 90% of defects at low cost.
- **Testing levels:** unit, integration, system, acceptance; with regression testing after change.

### Quality assurance versus quality control

| Basis | Quality assurance (QA) | Quality control (QC) |
|---|---|---|
| Focus | the **process** | the **product** |
| Aim | prevent defects | detect defects |
| Activities | standards, audits, training, process improvement | testing, inspection, reviews |
| Timing | throughout | at defined points (usually after work is produced) |
| Responsibility | whole team, QA group | testers, reviewers |

## 6.4 Total Quality Management (TQM)

**TQM** is a management philosophy in which **every employee** and every process is involved in continuously improving quality to satisfy customers. It grew from the work of W. Edwards Deming, Joseph Juran and Philip Crosby, and became famous in Japanese manufacturing.

### Principles

1. **Customer focus:** quality is defined by the customer.
2. **Total employee involvement:** everyone owns quality.
3. **Process-centred thinking:** most defects come from the process, not people.
4. **Integrated system and strategic approach:** quality is part of strategy.
5. **Continual improvement (kaizen).**
6. **Fact-based decisions:** use data and metrics.
7. **Communication and leadership:** top-management commitment.
8. **Supplier partnership.**

### PDCA cycle and Deming's ideas

The **Plan-Do-Check-Act (PDCA)** cycle is the engine of continual improvement: *Plan* the change; *Do* it on a small scale; *Check* the result against the plan; *Act* to standardise if it works, or try again. Deming's **14 points** include "cease dependence on inspection," "improve constantly," "institute training," "drive out fear" and "break down barriers between departments." Software examples: retrospectives, blameless post-mortems, automated tests that stop defects early.

### TQM in software

TQM translates into customer involvement in requirements, process definition and metrics, code reviews, defect prevention (root cause analysis), and continuous improvement of the process. Its limits: it needs sustained commitment, and the cultural change takes years.

## 6.5 Six Sigma

**Six Sigma** (Motorola, 1986; popularised by General Electric) is a data-driven approach to reduce defects and variation. The term comes from statistics: **sigma (σ)** measures spread, and a process at "six sigma" has only **3.4 defects per million opportunities (DPMO)**, allowing for a 1.5σ drift of the process mean.

### Sigma levels

| Sigma level | DPMO | Yield (defect-free) |
|---|---|---|
| 1σ | 691,462 | 30.9% |
| 2σ | 308,538 | 69.1% |
| 3σ | 66,807 | 93.3% |
| 4σ | 6,210 | 99.38% |
| 5σ | 233 | 99.977% |
| 6σ | 3.4 | 99.99966% |

**DPMO = (defects ÷ (units × opportunities per unit)) × 1,000,000.**

::: example Worked example: DPMO for a software release
A test of 1,200 delivered transactions, each with 5 opportunities for a defect (wrong amount, wrong account, wrong date, wrong fee, wrong message), finds 34 defects. DPMO = 34 / (1,200 × 5) × 1,000,000 = **5,667**. From the table this is between 4σ (6,210) and 5σ (233), roughly **4.0 sigma**: about 99.43% defect-free.
:::

### DMAIC: improving an existing process

| Phase | Purpose | Typical tools |
|---|---|---|
| **Define** | problem, customer needs (voice of the customer), project goal | project charter, SIPOC |
| **Measure** | collect data on current performance | defect counts, process maps, sampling |
| **Analyse** | find root causes | Pareto chart, cause-and-effect (fishbone) diagram, 5 Whys |
| **Improve** | design and test solutions | pilot, design of experiments |
| **Control** | hold the gains | control charts, standard work, monitoring |

**DMADV** (define, measure, analyse, design, verify), also called DFSS, is used to design a *new* process or product. Six Sigma roles are named by belts: Champion, Master Black Belt, Black Belt, Green Belt, Yellow Belt.

### Six Sigma for software

Software is not manufactured, so defect "opportunities" are less obvious: use defects per KLOC, requirements defects per review, or failed transactions. Applications include reducing escaped defects, shortening the defect-fix cycle, and improving release processes. Critics note that rigid targets can lead to gaming; the approach works best with real data and root-cause analysis.

### TQM versus Six Sigma

| Basis | TQM | Six Sigma |
|---|---|---|
| Nature | broad management philosophy and culture | structured, project-based method |
| Focus | continuous improvement by everyone | defect and variation reduction |
| Target | customer satisfaction | 3.4 DPMO, with financial return |
| Method | PDCA, quality circles | DMAIC, DMADV, statistical tools |
| People | all employees | trained belts lead projects |

## 6.6 Software quality assurance and process maturity

**Software quality assurance (SQA)** is the set of activities that ensure that the software process and the products conform to standards. Typical tasks: audits, reviews, testing oversight, defect tracking, measurement, and reporting to management independent of the development line.

**ISO 9001** is a general quality management standard: the organisation documents its processes, follows them, audits itself and improves (certification by an external body). **ISO/IEC 90003** gives guidance for software.

The **SEI Capability Maturity Model Integration (CMMI)** classifies organisations by process maturity:

| Level | Name | Characteristic |
|---|---|---|
| 1 | Initial | ad hoc, depends on heroes |
| 2 | Managed | basic project management (requirements, planning, tracking, configuration) |
| 3 | Defined | organisation-wide standard processes |
| 4 | Quantitatively managed | processes are measured and controlled with statistics |
| 5 | Optimising | continuous improvement from quantitative feedback |

An organisation at a higher level shows more predictable cost, schedule and quality. Many Nepali outsourcing companies seek CMMI level 3 to win overseas clients.

## Formula and fact sheet

- ISO 9126 characteristics: functionality, reliability, usability, efficiency, maintainability, portability.
- Defect density = defects/KLOC; DRE = found before release ÷ (before + after); availability = MTTF/(MTTF + MTTR).
- DPMO = defects ÷ (units × opportunities) × 10<sup>6</sup>; 6σ = 3.4 DPMO; 3σ = 66,807 DPMO.
- Cost of quality = prevention + appraisal + internal failure + external failure.
- PDCA: plan, do, check, act. DMAIC: define, measure, analyse, improve, control.
- CMMI: 1 initial, 2 managed, 3 defined, 4 quantitatively managed, 5 optimising.

## Chapter summary

- Quality means fitness for use and conformance to measurable requirements; defects cost more the later they are found.
- ISO 9126 divides product quality into six characteristics with sub-characteristics and metrics, and has been succeeded by ISO 25010.
- Quality is planned: quality requirements, a quality plan, reviews and tests, quality gates and metrics such as DRE.
- TQM builds quality into all processes through customer focus, involvement and PDCA; Six Sigma reduces defects statistically with DMAIC.
- SQA, ISO 9001 and CMMI organise quality at the level of the organisation.

## Practice

1. Define software quality. Why is it important?
2. Explain the ISO 9126 model with its characteristics and sub-characteristics.
3. Distinguish quality assurance from quality control.
4. What is the cost of quality? Explain its four components.
5. A system has MTTF = 900 hours and MTTR = 6 hours. Find the availability. 
6. Testing found 114 defects before release and customers reported 6 in the first three months. Find DRE.
7. Explain the place of quality in software planning and the contents of a quality plan.
8. Explain the principles of TQM and the PDCA cycle.
9. What is Six Sigma? Explain DMAIC and compute DPMO for 25 defects in 500 units with 4 opportunities each.
10. Differentiate TQM from Six Sigma. List the CMMI levels.

::: note Answers and worked solutions
**1.** Fitness for use and conformance to requirements; importance: cost of late defects, safety, reputation, maintenance, legal duty, productivity.
**2.** Six characteristics: functionality, reliability, usability, efficiency, maintainability, portability, each with sub-characteristics (see the figure and table of section 6.2), with internal, external and in-use views.
**3.** QA is process-oriented and preventive; QC is product-oriented and detective (testing and inspection).
**4.** Prevention, appraisal, internal failure and external failure costs; spending on prevention lowers the total.
**5.** Availability = 900/(900 + 6) = **0.9934 = 99.34%**.
**6.** DRE = 114/(114 + 6) = **95%**.
**7.** Measurable quality requirements, standards, a quality plan (objectives, reviews, tests, entry and exit criteria, defect tracking, roles), quality gates and metrics.
**8.** Customer focus, total involvement, process approach, continual improvement, fact-based decisions, leadership; PDCA is plan, do, check, act.
**9.** Six Sigma reduces defects to 3.4 per million; DMAIC is define, measure, analyse, improve, control. DPMO = 25/(500 × 4) × 10<sup>6</sup> = **12,500** (between 3σ and 4σ, about 3.7σ).
**10.** TQM is a culture of continual improvement by all; Six Sigma is a statistical, project-based method with a numerical target. CMMI: initial, managed, defined, quantitatively managed, optimising.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the ISO 9126 software quality model.**

*Introduction.* ISO/IEC 9126 is an international standard that defines a framework for evaluating software product quality.

*Characteristics.* **Functionality** (suitability, accuracy, interoperability, security), **reliability** (maturity, fault tolerance, recoverability), **usability** (understandability, learnability, operability, attractiveness), **efficiency** (time behaviour, resource utilisation), **maintainability** (analysability, changeability, stability, testability) and **portability** (adaptability, installability, co-existence, replaceability).

*Views.* Internal quality is measured on the code and design, external quality on the running software, and quality in use in real conditions.

| Characteristic | Sample metric |
|---|---|
| Functionality | % requirements met |
| Reliability | MTBF, availability |
| Usability | task completion time |
| Efficiency | response time |
| Maintainability | mean time to fix |
| Portability | porting effort |

*Conclusion.* The model gives developers and customers a common checklist for specifying and measuring quality; it has been superseded by ISO/IEC 25010, which adds security and compatibility as separate characteristics.

**Q2 (10 marks). What is Six Sigma? Explain DMAIC, sigma levels, and compare it with TQM.**

*Introduction.* Six Sigma is a disciplined, data-driven method of improving process quality by eliminating the causes of defects and variation; the target is not more than 3.4 defects per million opportunities.

*Sigma levels and DPMO.* DPMO = defects/(units × opportunities) × 10<sup>6</sup>. Three sigma means 66,807 DPMO and six sigma 3.4. For 34 defects in 1,200 units with 5 opportunities, DPMO = 5,667, about 4.0 sigma.

*DMAIC.* Define the problem and customer needs; Measure current performance; Analyse root causes with Pareto and fishbone charts; Improve with tested solutions; Control with charts and standard procedures.

*Software use.* Reduce escaped defects, shorten fix times, improve release reliability.

| Basis | TQM | Six Sigma |
|---|---|---|
| Nature | culture, philosophy | method, projects |
| Method | PDCA, circles | DMAIC, statistics |
| Goal | customer satisfaction | 3.4 DPMO |

*Conclusion.* The two are complementary: TQM provides the culture of quality, and Six Sigma provides the statistical tools to achieve measurable improvement.
