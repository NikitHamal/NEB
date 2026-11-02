---
subject: Cyber Security and Ethical Hacking
grade: BCA Semester 7
unit: 1
title: Foundations, the CIA Triad, Threat Modelling and CVSS Scoring
hours: 6
area: BCA 401 · Cyber Security and Ethical Hacking · Unit 1
---

A mobile wallet, a hospital record system and a municipality's property-tax portal have little in common except one fact: each holds something people depend on, and each runs on software that contains mistakes. **Cyber security** is the discipline of protecting information and the systems that handle it so that they keep working for the right people and no one else. This course takes the *defender's* and the *auditor's* point of view. We study how systems are measured, hardened, monitored and lawfully tested; we treat attackers as a source of requirements, not as a subject for recipes.

::: key What this unit gives you
- Core vocabulary: asset, threat, vulnerability, risk, control; the CIA triad and its companions.
- Defence in depth and the economics of security.
- Threat modelling with data-flow diagrams and the STRIDE categories.
- Risk arithmetic: likelihood × impact, DREAD averages and a complete CVSS v3.1 base-score calculator.
:::

## 1.1 Vocabulary

An **asset** is anything of value: data, a service, a reputation. A **vulnerability** is a weakness in design, implementation or operation. A **threat** is a circumstance or actor that could exploit it, and **risk** is the combination of how likely that is and how bad the result would be. A **control** (safeguard, countermeasure) reduces risk. Note the distinction: removing a vulnerability, lowering a threat's likelihood and shrinking the impact are three different ways to treat the same risk.

Typical threat actors are opportunistic criminals, organised fraud groups, insiders (malicious or careless), hacktivists and state-linked groups. Most real incidents in Nepali organisations trace back to ordinary causes: reused passwords, unpatched software, misconfigured cloud storage and phishing, which is why basic hygiene yields more than exotic tools.

## 1.2 The CIA triad and beyond

| Property | Meaning | Typical controls | Failure example |
|---|---|---|---|
| **Confidentiality** | Only authorised parties can read information | Encryption, access control, classification | Customer records published by mistake |
| **Integrity** | Information changes only in authorised ways | Hashing, digital signatures, change control, input validation | A tampered account balance |
| **Availability** | Systems and data are usable when needed | Redundancy, backups, capacity planning, DDoS protection | A bank's mobile app down at salary time |

Related properties: **authenticity** (a party or document is genuine), **accountability** and **non-repudiation** (actions are attributable and cannot be credibly denied; digital signatures and audit logs support this), and **privacy** (control over personal data). The properties can conflict: strong encryption protects confidentiality but a lost key destroys availability; heavy logging aids accountability but collects personal data.

## 1.3 Defence in depth and principles

No single control is perfect, so layers are used: policy and training, physical protection, network segmentation, host hardening, application controls, data encryption and monitoring. Design principles that recur throughout this course are **least privilege**, **fail-safe defaults** (deny unless allowed), **complete mediation** (check every access), **separation of duties**, **economy of mechanism** (keep it simple), **open design** (security should not depend on secrecy of the design) and **psychological acceptability** (controls people will actually use).

## 1.4 Threat modelling

Threat modelling asks four questions: *What are we building? What can go wrong? What are we going to do about it? Did we do a good enough job?* The first step is a **data-flow diagram (DFD)** showing external entities, processes, data stores, data flows and **trust boundaries** (lines where the level of trust changes, such as between a browser and a server). Threats concentrate where data crosses a trust boundary.

**STRIDE** (Microsoft) is a checklist of six categories, each violating a security property:

| Letter | Threat | Property violated | Example defensive control |
|---|---|---|---|
| **S** | Spoofing identity | Authentication | Multi-factor authentication, mutual TLS |
| **T** | Tampering with data | Integrity | Digital signatures, MACs, file integrity monitoring |
| **R** | Repudiation | Non-repudiation | Tamper-evident audit logs, signed receipts |
| **I** | Information disclosure | Confidentiality | Encryption, least privilege |
| **D** | Denial of service | Availability | Rate limiting, autoscaling, redundancy |
| **E** | Elevation of privilege | Authorisation | Least privilege, input validation, sandboxing |

For each element of the DFD you ask which STRIDE categories apply (a data store is subject to T, I and D; an external entity to S and R), record the threats, rate them and choose mitigations.

## 1.5 Rating and ranking risk

A simple **risk matrix** scores likelihood and impact on 1 to 5 scales and multiplies them: the risk register can then be ranked. **DREAD** (Damage, Reproducibility, Exploitability, Affected users, Discoverability) averages five ratings from 0 to 10; it is no longer used inside Microsoft because the ratings are subjective, but it remains a common exam topic and a fair way to start a discussion. Teaching bands used here are: average 7 or more is High, 4 to under 7 Medium, below 4 Low.

```python
ratings = {"Damage": 8, "Reproducibility": 9, "Exploitability": 6, "Affected users": 7, "Discoverability": 5}
avg = sum(ratings.values()) / len(ratings)
band = "High" if avg >= 7 else "Medium" if avg >= 4 else "Low"
print(f"DREAD average {avg:.1f} -> {band}")
risks = {"R1": (4, 5), "R2": (3, 4), "R3": (2, 2)}      # (likelihood, impact), each 1 to 5
ranked = sorted(risks.items(), key=lambda kv: kv[1][0] * kv[1][1], reverse=True)
print("ranked: " + ", ".join(f"{k}={l * i}" for k, (l, i) in ranked))
```
```output
DREAD average 7.0 -> High
ranked: R1=20, R2=12, R3=4
```
The five DREAD ratings sum to 35, an average of 7.0, so this threat is High. The risk matrix ranks R1 (4 × 5 = 20) above R2 (12) and R3 (4): work starts at the top. Subjective numbers are only as good as the discussion behind them, so record the *reasons* with each score.

## 1.6 CVSS v3.1: scoring a known vulnerability

When a vulnerability is published, the **Common Vulnerability Scoring System** (FIRST, version 3.1) gives it a score from 0.0 to 10.0, so that defenders can prioritise patching. The **base score** depends on eight metrics:

- **Exploitability:** Attack Vector (AV: Network 0.85, Adjacent 0.62, Local 0.55, Physical 0.2), Attack Complexity (AC: Low 0.77, High 0.44), Privileges Required (PR: None 0.85, Low 0.62, High 0.27; with changed scope 0.68 and 0.5 for Low and High) and User Interaction (UI: None 0.85, Required 0.62).
- **Scope** (S: Unchanged or Changed): whether the impact crosses a security boundary.
- **Impact:** Confidentiality, Integrity and Availability (each High 0.56, Low 0.22, None 0).

The formulas are:

::: key CVSS v3.1 base score
ISS = 1 − (1 − C)(1 − I)(1 − A). Impact = 6.42 × ISS if scope is unchanged; 7.52 × (ISS − 0.029) − 3.25 × (ISS − 0.02)¹⁵ if changed. Exploitability = 8.22 × AV × AC × PR × UI. If Impact ≤ 0 the score is 0; otherwise unchanged scope gives Roundup(min(Impact + Exploitability, 10)) and changed scope gives Roundup(min(1.08 × (Impact + Exploitability), 10)). Roundup returns the smallest number with one decimal that is greater than or equal to its input.
:::

Severity bands: 0.0 None, 0.1 to 3.9 Low, 4.0 to 6.9 Medium, 7.0 to 8.9 High, 9.0 to 10.0 Critical.

```python
import math
W = {"AV": {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2}, "AC": {"L": 0.77, "H": 0.44},
     "UI": {"N": 0.85, "R": 0.62}, "CIA": {"H": 0.56, "L": 0.22, "N": 0.0}}
PR = {"U": {"N": 0.85, "L": 0.62, "H": 0.27}, "C": {"N": 0.85, "L": 0.68, "H": 0.5}}

def roundup(x):
    i = round(x * 100000)
    return i / 100000.0 if i % 10000 == 0 else (math.floor(i / 10000) + 1) / 10.0

def base_score(vec):
    m = dict(part.split(":") for part in vec.split("/"))
    iss = 1 - (1 - W["CIA"][m["C"]]) * (1 - W["CIA"][m["I"]]) * (1 - W["CIA"][m["A"]])
    if m["S"] == "U":
        impact = 6.42 * iss
    else:
        impact = 7.52 * (iss - 0.029) - 3.25 * (iss - 0.02) ** 15
    expl = 8.22 * W["AV"][m["AV"]] * W["AC"][m["AC"]] * PR[m["S"]][m["PR"]] * W["UI"][m["UI"]]
    if impact <= 0:
        return 0.0
    if m["S"] == "U":
        return roundup(min(impact + expl, 10))
    return roundup(min(1.08 * (impact + expl), 10))

def rating(s):
    return "None" if s == 0 else "Low" if s < 4 else "Medium" if s < 7 else "High" if s < 9 else "Critical"

vectors = ["AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", "AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
           "AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H", "AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
           "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N", "AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N"]
for vec in vectors:
    s = base_score(vec)
    print(f"{vec} -> {s:.1f} ({rating(s)})")
```
```output
AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H -> 9.8 (Critical)
AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H -> 10.0 (Critical)
AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H -> 7.8 (High)
AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N -> 6.1 (Medium)
AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N -> 7.5 (High)
AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N -> 5.9 (Medium)
```
The first vector (network-reachable, easy, no privileges, no user interaction, full loss of confidentiality, integrity and availability) scores 9.8, because ISS is 0.9148 and the exploitability term is large. Changing the scope pushes the same vector to the 10.0 ceiling. The calculator reproduces the published reference scores for all six vectors (9.8, 10.0, 7.8, 6.1, 7.5 and 5.9), which is how it was validated; the checker compares against those published values, not against the program's own logic.

::: caution
CVSS measures the **severity of a vulnerability in general**, not **risk to your organisation**. A 9.8 on a system that is not exposed and holds nothing valuable may matter less than a 6.5 on your internet-facing payment service. Combine CVSS with asset value, exposure and known exploitation to prioritise.
:::

## 1.7 Summary and exercises

Security protects confidentiality, integrity and availability through layered, least-privilege controls; threat modelling with DFDs and STRIDE finds problems before they are built; risk can be ranked with a matrix or DREAD average; and CVSS gives a reproducible severity score that must be combined with context.

1. Define asset, threat, vulnerability, risk and control, and give a Nepali example of each.
2. Match each STRIDE letter to the property it violates and a mitigation.
3. Rate a threat with D=6, R=5, E=4, A=9, D=3 using DREAD. What band results?
4. Compute the ISS for C:L, I:L, A:N and the unchanged-scope Impact.
5. Why can a vulnerability with a lower CVSS score deserve earlier patching?
6. Explain two cases where confidentiality and availability conflict.
