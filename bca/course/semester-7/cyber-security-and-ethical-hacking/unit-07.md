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

## 7.6 Summary and exercises

Audits compare practice with standards using sampling and documented evidence; ALE and ROSI turn risk into money; penetration tests are authorised, scoped experiments governed by a complete ROE; and Nepal's Electronic Transactions Act (Sections 44 to 47 and 52) together with the 2080 cyber security policy define the legal environment in which defenders work.

1. Differentiate a vulnerability assessment from a penetration test and from a red-team exercise.
2. Compute the discovery-sampling size for 97.5% confidence and a 3% tolerable rate (use the formula, round up).
3. An asset is worth Rs 8,00,000 with EF 25% and ARO 0.5. Compute SLE and ALE. A control costing Rs 30,000 halves the ARO; compute ROSI.
4. List the eight elements of a rules-of-engagement document, and say which two matter most if the target is a hospital system.
5. State the offences in ETA 2063 Sections 44, 45, 46, 47 and 52 and their reported maximum penalties.
6. A student tests a college's web server "to help" without permission. Explain which provision is engaged and what should have been done instead.
