---
subject: Cyber Security and Ethical Hacking
grade: BCA Semester 7
unit: 7
title: Security Audits, Penetration Testing Rules of Engagement and Nepal Cyber Law
hours: 6
area: BCA 401 · Cyber Security and Ethical Hacking · Unit 7
---

"Ethical hacking" is a short name for a long professional discipline: finding weaknesses in a system *with the owner's written permission*, so that they can be fixed before someone with bad intent finds them. What separates a security professional from an offender is not skill but **authorisation, scope and accountability**. This unit explains how audits and penetration tests are planned and governed, how risk is quantified to justify controls, and what Nepal's law says about computer offences, because every practitioner must know where the legal line runs.

::: key What this unit gives you
- Security audits and assessments: standards, process, evidence and sampling arithmetic.
- Risk quantification (SLE, ARO, ALE, return on security investment) and the four risk treatments.
- Penetration testing as a governed activity: rules of engagement, scope, stop conditions, disclosure.
- Nepal's legal framework: Electronic Transactions Act 2063 (Sections 44, 45, 46, 47 and 52) and the National Cyber Security Policy 2080.
:::

## 7.1 Audits, assessments and tests

- A **security audit** compares systems and processes with a *standard or policy* and reports conformance and gaps. It is typically conducted by an independent party, internal or external.
- A **vulnerability assessment** identifies and rates weaknesses (often with scanners, then manual validation) and produces a prioritised list.
- A **penetration test** goes further under controlled conditions: testers try to show what an adversary could actually achieve by *chaining* weaknesses, with the goal of demonstrating impact to decision makers.
- A **red-team exercise** tests the organisation's *detection and response* against a realistic adversary scenario, while a **purple-team** exercise has attackers and defenders cooperate to improve both.

Common frameworks and standards: **ISO/IEC 27001** (an information security management system, with Annex A controls), **ISO/IEC 27002** (control guidance), the **NIST Cybersecurity Framework** (Govern, Identify, Protect, Detect, Respond, Recover), the **CIS Critical Security Controls**, **COBIT** for IT governance and **PCI DSS** for card data. Banks in Nepal additionally follow directives of Nepal Rastra Bank on IT governance and information security.

## 7.2 The audit process

1. **Planning and scoping:** objectives, criteria, systems in scope, timetable, access, confidentiality.
2. **Evidence gathering:** documents, configuration exports, interviews, observation and automated checks.
3. **Testing:** design effectiveness (would the control work?) and operating effectiveness (did it work over the period?).
4. **Findings and rating:** each finding states condition, criteria, cause, effect and a recommendation, with a risk rating.
5. **Reporting and follow-up:** a report to management, agreed actions with owners and dates, and re-testing.

Auditors cannot test every record, so they **sample**. In *discovery sampling* the auditor wants a given **confidence** that, if the true deviation rate in the population exceeds a **tolerable rate**, the sample would contain at least one deviation. With a large population and zero expected deviations, the smallest sample size *n* satisfies (1 − tolerable rate)ⁿ ≤ 1 − confidence, so n = ⌈ ln(1 − confidence) ÷ ln(1 − tolerable rate) ⌉.

```python
import math
for conf, tol in ((0.95, 0.05), (0.90, 0.10), (0.99, 0.05)):
    n = math.ceil(math.log(1 - conf) / math.log(1 - tol))
    print(f"confidence {conf * 100:.0f}%, tolerable deviation {tol * 100:.0f}%: sample {n}")
```
```output
confidence 95%, tolerable deviation 5%: sample 59
confidence 90%, tolerable deviation 10%: sample 22
confidence 99%, tolerable deviation 5%: sample 90
```
For 95% confidence and a 5% tolerable rate the auditor tests 59 items; relaxing to 90% and 10% needs only 22, while demanding 99% confidence needs 90. If any sampled item shows a deviation, the control cannot be relied upon at that tolerance and the auditor widens testing. The checker found the smallest *n* by exact repeated multiplication rather than the logarithm formula.

## 7.3 Quantifying risk

Management funds controls when benefits are clear. The classic quantitative model uses:

- **Asset value (AV)** and **exposure factor (EF)**, the fraction of the asset lost in one incident;
- **Single loss expectancy** SLE = AV × EF;
- **Annualised rate of occurrence** (ARO), expected incidents per year;
- **Annualised loss expectancy** ALE = SLE × ARO.

A control is worthwhile if the ALE it removes exceeds its annual cost. **Return on security investment** ROSI = (ALE before − ALE after − control cost) ÷ control cost.

```python
asset, ef, aro = 500000, 0.40, 0.25
sle = asset * ef
ale = sle * aro
control_cost, aro_after = 20000, 0.05
ale_after = sle * aro_after
rosi = (ale - ale_after - control_cost) / control_cost
print(f"SLE {sle:.0f}, ALE before {ale:.0f}, ALE after {ale_after:.0f}, ROSI {rosi * 100:.0f}%")
```
```output
SLE 200000, ALE before 50000, ALE after 10000, ROSI 100%
```
An incident costs Rs 2,00,000 and is expected once every four years, an ALE of Rs 50,000. A control costing Rs 20,000 a year that cuts the rate to once in twenty years lowers ALE to Rs 10,000: it saves 40,000 for a 20,000 spend, a ROSI of 100%. The inputs are estimates, so present ranges and sensitivity, not false precision.

The four **risk treatments** are to **reduce** (apply controls), **avoid** (stop the activity), **transfer** (insurance, outsourcing, contracts) and **accept** (formally, by an accountable owner, with review dates). Residual risk after treatment is recorded in the **risk register**.

## 7.4 Penetration testing: rules of engagement

A penetration test is a *controlled, authorised experiment*. The **rules of engagement (ROE)** are the contract between tester and owner and the single most important document. A complete ROE states:

1. **Scope:** exactly which systems, networks, applications and data are in scope and which are **excluded** (for example third-party or life-critical systems).
2. **Authorised signatories:** who in the organisation, with legal authority, approves the test; for third-party hosted systems the provider's permission is also needed.
3. **Testing window:** dates and times, and blackout periods.
4. **Permitted techniques:** and the ones that are forbidden (such as denial-of-service, destructive actions or social engineering of named individuals unless agreed).
5. **Data handling:** how any personal or sensitive data seen during testing is protected, stored and destroyed.
6. **Emergency contacts and stop conditions:** who to call, and the events (a service degradation, evidence of a real attacker) that require stopping.
7. **Reporting and retention:** report format, severity scale, secure delivery and retention period.
8. **Legal indemnity and confidentiality:** the permission in writing, and non-disclosure terms.

```python
required = ["scope", "authorised signatories", "testing window", "permitted techniques", "excluded systems",
            "data handling", "emergency contact", "reporting and retention", "legal indemnity"]
draft = {"scope", "authorised signatories", "testing window", "permitted techniques", "excluded systems",
         "reporting and retention", "legal indemnity"}
missing = [f for f in required if f not in draft]
print(f"ROE completeness: {len(required) - len(missing)} of {len(required)} fields; missing: {missing}")
```
```output
ROE completeness: 7 of 9 fields; missing: ['data handling', 'emergency contact']
```
The checklist reveals a draft that lacks data-handling rules and an emergency contact: the test must not start until both are agreed. Good practice also separates phases (planning, discovery, assessment, reporting, remediation retest), logs every action for later reconciliation with the client's monitoring, and treats any discovered real compromise as an incident to report immediately.

**Professional ethics:** act only within written scope; protect confidentiality; report all findings honestly, including your own mistakes; practise **coordinated vulnerability disclosure** (report to the vendor or owner, allow reasonable time to fix, publish responsibly); and follow your professional body's code of conduct. Bug-bounty programmes extend this with published scope and safe-harbour terms; outside such terms, nobody may assume permission.

## 7.5 Nepal's legal framework

**Electronic Transactions Act, 2063 (2008).** Nepal's principal cyber law gives legal recognition to electronic records and digital signatures, regulates certifying authorities (under the Controller) and, in Chapter 9, defines computer-related offences. The sections you must know, with the maximum penalties as commonly reported (verify the figures against the Act's current gazetted text and any amendments):

| Section | Offence | Reported maximum |
|---|---|---|
| 44 | Pirating, destroying or altering computer source code | 3 years' imprisonment and/or Rs 2,00,000 fine |
| 45 | Unauthorised access to computer material | 3 years' imprisonment and/or Rs 2,00,000 fine |
| 46 | Damage to a computer or information system | 3 years' imprisonment and/or Rs 2,00,000 fine |
| 47 | Publication of illegal material in electronic form (for example obscene or hate-spreading content) | 5 years' imprisonment and/or Rs 1,00,000 fine; enhanced punishment on repeat |
| 52 | Computer fraud | 2 years' imprisonment and/or Rs 1,00,000 fine |

```python
eta = {44: ("source code offences", 3, 200000), 45: ("unauthorised access", 3, 200000),
       46: ("damage to systems", 3, 200000), 47: ("illegal publication", 5, 100000),
       52: ("computer fraud", 2, 100000)}
for sec, (name, yrs, fine) in sorted(eta.items(), key=lambda kv: (-kv[1][1], kv[0])):
    print(f"s{sec} {name}: up to {yrs} years, Rs {fine}")
```
```output
s47 illegal publication: up to 5 years, Rs 100000
s44 source code offences: up to 3 years, Rs 200000
s45 unauthorised access: up to 3 years, Rs 200000
s46 damage to systems: up to 3 years, Rs 200000
s52 computer fraud: up to 2 years, Rs 100000
```
The program ranks the offences by maximum imprisonment. Section 47 carries the longest term, while Sections 44 to 46 carry the highest fine. Secondary sources differ on the label and numbering of some of the later sections (for example, whether Section 52 is described as computer fraud or abetment), so treat this table as a study aid and read the Act itself before giving legal advice.

What this means for a tester: **access without authority is itself the offence.** Section 45 concerns access to computer material without the owner's authorisation; there is no "I only looked" or "I was helping" defence in the text of the offence, and good intentions are no substitute for a signed ROE. Altering or deleting data or disrupting a service can add Section 46; copying or modifying source code, Section 44. Accessing, altering or disclosing personal data also engages the **Individual Privacy Act, 2075** and the **National Penal (Code) Act, 2074**. Cases are investigated by the **Cyber Bureau of Nepal Police** and heard in the district courts.

**National Cyber Security Policy 2080 (2023).** Approved by the Cabinet in 2023 as the country's first dedicated cyber security policy document, it sets a vision and objectives rather than offences. Its main themes are protection of critical information infrastructure (banking, telecommunications, energy, government systems), national incident detection and response capability (a national CERT and a proposed National Cyber Security Centre), a trained workforce, protection of data and privacy, public-private cooperation and a stronger legal framework, with a proposed Information Technology and Cyber Security Bill intended to modernise the 2063 Act. Some provisions, such as proposals for centralised internet gateways, have drawn public debate about surveillance and rights, a reminder that security measures must be balanced with civil liberties. Check for the latest status of the Bill before relying on it.

::: caution
This unit is educational material, not legal advice. Laws, penalties and policies change, and different offences can combine. A professional engagement should always involve counsel reviewing the contract and the ROE.
:::

## 7.6 Seeing the ideas: places under audit, the audit cycle, ALE, the test with its ROE gate and the penalty chart

Audits and the law are about real places and real institutions. Plate 7.1 shows the seat of Nepal's government, where the laws that govern cyber offences are made and applied, and two things an auditor inspects on site: a server room and its physical monitoring.

```photogrid label="7.1" cols="3" ratio="1.15" caption="Context of an audit. (a) Singha Durbar, Kathmandu, the seat of the Government of Nepal, where policy such as the National Cyber Security Policy and laws such as the Electronic Transactions Act are administered. (b) A server room: auditors check cable management, access logs, fire protection and labelling. (c) A dome CCTV camera: physical monitoring is a control that auditors test with evidence such as retained recordings."
@ photo id="bca401/singha" cap="Singha Durbar, Kathmandu"
fit 1.15
focus 0.5 0.5
@ photo id="bca401/serverroom" cap="Server room under audit"
fit 1.15
focus 0.5 0.5
@ photo id="bca401/cctv" cap="CCTV (physical control)"
fit 1.15
focus 0.7 0.45
```

```svgfig label="7.1" caption="The audit cycle. Planning fixes scope and criteria; fieldwork gathers evidence by interview, observation and sampling; findings are rated; the report goes to management; and follow-up checks that fixes were made. Sample sizes come from confidence and tolerable deviation: 59 items at 95% / 5%."
f = Fig(580, 214)
st = [("1 Plan", "scope, standard\n(ISO 27001),\ncriteria"), ("2 Fieldwork", "interviews,\nobservation,\nsampling"), ("3 Findings", "gap, evidence,\nrisk rating"), ("4 Report", "to management,\nagreed actions"), ("5 Follow-up", "re-test fixes,\nclose or escalate")]
for i, (t, s) in enumerate(st):
    x = 6 + i * 115
    f.box(x, 14, 108, 30, t, fill=BLUE, stroke=NAVY, bold=True, size=10.5)
    f.box(x, 50, 108, 60, s, fill=MINT if i % 2 == 0 else SAND, stroke=TEAL if i % 2 == 0 else AMBER, size=9.5)
    if i < 4:
        f.arrow([(x + 108, 29), (x + 115, 29)])
f.box(6, 128, 180, 70, "Sample size (section 7.2)\n95% confidence, 5% deviation: 59\n90%, 10%: 22\n99%, 5%: 90", fill="#f8fafc", stroke=SLATE, size=9.5)
f.box(200, 128, 372, 70, "A single deviation in the sample means the control cannot be relied on.\nGood evidence is dated, attributable and independent: system exports,\nsigned approvals, screenshots with timestamps, not just verbal answers.", fill=ROSE, stroke=RED, size=10)
```

```svgfig label="7.2" caption="Annual loss expectancy before and after a control. An incident costs Rs 2,00,000 and was expected once in 4 years (ALE Rs 50,000). A control that costs Rs 20,000 a year cuts the rate to once in 20 years (ALE Rs 10,000). Saving 40,000 for 20,000 gives a return on security investment of 100%."
f = Fig(580, 214)
sc = 0.0042
f.text(8, 28, "ALE before", size=10.5, color=NAVY, bold=True, anchor="start")
f.box(110, 12, 50000 * sc * 1.2, 28, "Rs 50,000", fill=ROSE, stroke=RED, bold=True, size=10.5)
f.text(8, 68, "ALE after", size=10.5, color=NAVY, bold=True, anchor="start")
f.box(110, 52, 10000 * sc * 1.2, 28, "", fill=MINT, stroke=TEAL)
f.text(110 + 10000 * sc * 1.2 + 6, 66, "Rs 10,000", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(8, 108, "Control cost", size=10.5, color=NAVY, bold=True, anchor="start")
f.box(110, 92, 20000 * sc * 1.2, 28, "", fill=SAND, stroke=AMBER)
f.text(110 + 20000 * sc * 1.2 + 6, 106, "Rs 20,000 per year", size=10.5, color=AMBER, bold=True, anchor="start")
f.box(380, 12, 192, 108, "ALE = SLE x ARO\nbefore: 2,00,000 x 0.25 = 50,000\nafter: 2,00,000 x 0.05 = 10,000\nROSI = (40,000 - 20,000) / 20,000\n= 100%", fill=BLUE, stroke=NAVY, size=10)
f.box(8, 140, 564, 62, "Four treatments: reduce (add controls), avoid (stop the activity), transfer (insurance, outsourcing),\naccept (formally, by an accountable owner with a review date). Numbers justify the choice to management.", fill="#f8fafc", stroke=SLATE, size=10)
```

```svgfig label="7.3" caption="A penetration test is gated by its rules of engagement (ROE). No testing starts until the ROE is complete and signed. The draft in section 7.4 had 7 of 9 fields and lacked data handling and an emergency contact, so the gate stays closed."
f = Fig(580, 214)
f.box(6, 20, 92, 50, "Planning\nscope, authority,\nROE drafted", fill=BLUE, stroke=NAVY, size=9, bold=True)
f.poly([(160, 8), (216, 45), (160, 82), (104, 45)], fill=SAND, stroke=AMBER, label="ROE\ncomplete?", lx=160, ly=45, size=9)
f.box(240, 20, 96, 50, "Discovery and\nassessment", fill=MINT, stroke=TEAL, size=9, bold=True)
f.box(352, 20, 106, 50, "Controlled\nvalidation\n(in scope only)", fill=MINT, stroke=TEAL, size=9, bold=True)
f.box(474, 20, 98, 50, "Report,\nretest after\nfixes", fill=BLUE, stroke=NAVY, size=9, bold=True)
f.arrow([(98, 45), (104, 45)]); f.arrow([(216, 45), (240, 45)], label="yes", lpos=(228, 36)); f.arrow([(336, 45), (352, 45)]); f.arrow([(458, 45), (474, 45)])
f.arrow([(160, 82), (160, 100), (52, 100), (52, 70)], color=RED, label="no: fix the ROE first", lpos=(110, 112))
f.box(6, 128, 564, 74, "Stop immediately if: service degrades, a real attacker is found, or a target outside scope is touched.\nThe ethics: act only within written scope, protect any data seen, report all findings honestly including your\nown mistakes, and use coordinated vulnerability disclosure for flaws found in third-party products.", fill=ROSE, stroke=RED, size=10)
```

```svgfig label="7.4" caption="Reported maximum penalties under Chapter 9 of the Electronic Transactions Act 2063 (study summary; confirm exact wording in the Act). Bars show years of imprisonment; fines are shown at the right."
f = Fig(580, 214)
rows = [("s47 illegal publication", 5, "Rs 1,00,000", RED), ("s44 source code offences", 3, "Rs 2,00,000", AMBER), ("s45 unauthorised access", 3, "Rs 2,00,000", AMBER), ("s46 damage to systems", 3, "Rs 2,00,000", AMBER), ("s52 computer fraud", 2, "Rs 1,00,000", TEAL)]
for i, (t, y, fine, c) in enumerate(rows):
    yy = 14 + i * 34
    f.text(8, yy + 14, t, size=10, color=NAVY, bold=True, anchor="start")
    f.box(170, yy, y * 56, 26, "%d years" % y, fill="#e2e8f0", stroke=c, bold=True, size=10)
    f.text(170 + y * 56 + 8, yy + 14, fine, size=10, color=SLATE, bold=True, anchor="start")
f.text(290, 200, "maximum imprisonment (bar) and maximum fine (label)", size=9.5, color=SLATE)
```

### 7.6.1 Eight benefits of regular security audits

1. **Finding gaps early.** An audit compares real practice with the written policy. A college may find that its backup job has silently failed for months. Finding this during an audit is far better than finding it during a ransomware attack.
2. **Independent assurance.** An outside or internal-independent auditor has no reason to hide problems. Management receives an honest picture instead of a comfortable one. This is the same idea as the financial audit of a bank.
3. **Meeting compliance duties.** Regulators such as Nepal Rastra Bank expect banks to follow information security rules. An audit report is the proof. Failing to show proof can lead to penalties or loss of licence.
4. **Prioritising spending.** Quantifying risk with ALE and ROSI shows where each rupee protects the most. A cheap control with 100% ROSI should come before an expensive one with little effect. Budget requests then rest on evidence.
5. **Building customer trust.** Certification such as ISO/IEC 27001 tells clients that data is handled with discipline. A software company in Kathmandu bidding for a bank project gains an advantage. Trust turns into contracts.
6. **Testing detection and response.** Red-team and purple-team exercises check whether alerts reach people who act. A control that never fires is not working. These tests improve the incident plan.
7. **Improving awareness and ownership.** Every finding gets an owner and a due date. Staff learn what is expected of them. Repeated audits make security a habit rather than a one-time project.
8. **Providing legal protection.** Records of authorised, scoped testing show that work was lawful under the Electronic Transactions Act. A signed rules-of-engagement document protects both tester and owner. Without it, a well-meant test could be treated as unauthorised access.

## 7.7 Summary and exercises

Audits compare practice with standards using sampling and documented evidence; ALE and ROSI turn risk into money; penetration tests are authorised, scoped experiments governed by a complete ROE; and Nepal's Electronic Transactions Act (Sections 44 to 47 and 52) together with the 2080 cyber security policy define the legal environment in which defenders work.

1. Differentiate a vulnerability assessment from a penetration test and from a red-team exercise.
2. Compute the discovery-sampling size for 97.5% confidence and a 3% tolerable rate (use the formula, round up).
3. An asset is worth Rs 8,00,000 with EF 25% and ARO 0.5. Compute SLE and ALE. A control costing Rs 30,000 halves the ARO; compute ROSI.
4. List the eight elements of a rules-of-engagement document, and say which two matter most if the target is a hospital system.
5. State the offences in ETA 2063 Sections 44, 45, 46, 47 and 52 and their reported maximum penalties.
6. A student tests a college's web server "to help" without permission. Explain which provision is engaged and what should have been done instead.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Distinguish between a security audit, a vulnerability assessment, a penetration test and a red-team exercise.**

*Introduction.* These four activities are often confused, but they answer different questions and are used at different times (section 7.1).

| Activity | Question answered | Method | Output |
|---|---|---|---|
| Security audit | Do we follow our policy or standard? | Evidence review, interviews, sampling | Conformance and gaps |
| Vulnerability assessment | Which weaknesses exist? | Scanners, then manual validation | Prioritised list |
| Penetration test | What could an attacker achieve by chaining weaknesses? | Controlled, authorised testing | Demonstrated impact |
| Red-team exercise | Can we detect and respond to a real adversary? | Realistic scenario over weeks | Detection and response findings |

*Points.* An audit is usually done by an independent party against a standard such as ISO/IEC 27001. A vulnerability assessment is broad but shallow, while a penetration test is narrower but deeper. A purple-team exercise has attackers and defenders cooperate so that detection rules improve in real time.

*Example.* A bank may audit itself against NRB guidelines each year, scan monthly, commission a penetration test before launching a new mobile app and run a red-team exercise every second year.

*Conclusion.* Use the right tool for the question; together they give layered assurance.

**Q2 (5 marks). Define SLE, ARO and ALE. An incident costs Rs 2,00,000 and is expected once in 4 years. A control costing Rs 20,000 a year reduces this to once in 20 years. Calculate the return on security investment.**

*Introduction.* Management funds controls when the benefit is clear in money terms. Quantitative risk analysis gives that clarity (section 7.3 and Figure 7.2).

*Definitions.* **SLE** (single loss expectancy) is the cost of one incident. **ARO** (annualised rate of occurrence) is how often it is expected per year. **ALE** (annualised loss expectancy) = SLE x ARO.

*Calculation.*

1. SLE = Rs 2,00,000.
2. ALE before = 2,00,000 x (1/4) = Rs 50,000.
3. ALE after = 2,00,000 x (1/20) = Rs 10,000.
4. Risk reduction = 50,000 - 10,000 = Rs 40,000 per year.
5. Net benefit = 40,000 - 20,000 = Rs 20,000.
6. ROSI = 20,000 / 20,000 = **100%**.

*Interpretation.* Each rupee spent on the control returns one extra rupee in avoided loss, so the control is worth buying. The remaining risk is treated by accepting, transferring (insurance) or further reducing it.

*Limitation.* SLE and ARO are estimates, so show a range and review them yearly.

**Q3 (10 marks). Explain the rules of engagement and professional ethics of a penetration test, and summarise Nepal's legal framework for computer offences.**

*Introduction.* A penetration test uses techniques that would be crimes if done without permission. It is therefore a controlled, authorised experiment, and the **rules of engagement (ROE)** are the contract between tester and owner and the most important document (section 7.4 and Figure 7.3).

*Contents of a complete ROE.*

1. **Scope**, with the systems that are explicitly excluded.
2. **Authorised signatories** who have legal authority; hosted systems also need the provider's consent.
3. **Testing window** and blackout periods.
4. **Permitted and forbidden techniques**, such as no denial-of-service or destructive action.
5. **Data handling**: how any personal data seen is protected and destroyed.
6. **Emergency contacts and stop conditions**.
7. **Reporting and retention** of the findings.
8. **Legal indemnity and confidentiality** in writing.

A checklist of nine required fields found a draft with only 7 of 9, missing data handling and emergency contact, so testing must not start.

*Professional ethics.* Act only within written scope; protect confidentiality; report all findings honestly including your own mistakes; use coordinated vulnerability disclosure, telling the vendor first and giving time to fix.

*Nepal's legal framework.* The **Electronic Transactions Act 2063** recognises electronic records and digital signatures and, in Chapter 9, defines offences (Figure 7.4):

| Section | Offence | Reported maximum |
|---|---|---|
| 47 | Illegal publication | 5 years, Rs 1,00,000 |
| 44 | Source code offences | 3 years, Rs 2,00,000 |
| 45 | Unauthorised access | 3 years, Rs 2,00,000 |
| 46 | Damage to systems | 3 years, Rs 2,00,000 |
| 52 | Computer fraud | 2 years, Rs 1,00,000 |

*Link.* A tester who goes beyond the written scope risks being treated as having made unauthorised access under section 45, which is why the ROE is also a legal shield. This summary is for study and is not legal advice; read the Act itself for exact wording.

*Conclusion.* A lawful and ethical test needs a complete signed ROE, honest reporting and respect for the Act.
