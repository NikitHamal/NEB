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

## 1.7 Seeing the ideas: real hardware, the triad, STRIDE and the risk matrix

Security is not only software. Plate 1.1 shows three physical things a defender must think about: the machine room that holds the assets, the cipher machine that made confidentiality famous, and the camera that deters a physical threat.

```photogrid label="1.1" cols="3" ratio="1.15" caption="Security starts with assets and places. (a) A server room: every cable and rack is an asset with a threat model of its own. (b) A Swiss Army Enigma-K cipher machine, an early device built for confidentiality of messages. (c) A dome CCTV camera with a warning sign: a detective and deterrent physical control."
@ photo id="bca401/serverroom" cap="Server room (assets)"
fit 1.15
focus 0.5 0.5
@ photo id="bca401/enigma" cap="Enigma-K cipher machine (confidentiality)"
fit 1.15
focus 0.5 0.45
@ photo id="bca401/cctv" cap="CCTV dome and sign (deterrence)"
fit 1.15
focus 0.7 0.45
```

```svgfig label="1.1" caption="The CIA triad. Each goal has typical controls and a typical failure. The three goals pull against each other: strong encryption protects confidentiality but a lost key destroys availability."
f = Fig(580, 232)
f.poly([(115, 24), (30, 190), (200, 190)], fill="#f8fafc", stroke=SLATE, sw=1.6)
f.circle(115, 24, 18, fill=BLUE, stroke=NAVY, label="C", size=13)
f.circle(30, 190, 18, fill=MINT, stroke=TEAL, label="I", size=13)
f.circle(200, 190, 18, fill=SAND, stroke=AMBER, label="A", size=13)
f.text(115, 112, "Security", size=11, color=NAVY, bold=True)
f.text(115, 128, "goals", size=11, color=NAVY, bold=True)
f.box(250, 8, 322, 66, "Confidentiality: only authorised people read it\nControls: encryption, access control, MFA\nFailure: customer records published by mistake", fill=BLUE, stroke=NAVY, size=10)
f.box(250, 83, 322, 66, "Integrity: it changes only in authorised ways\nControls: hashing, signatures, change control\nFailure: a tampered balance or exam result", fill=MINT, stroke=TEAL, size=10)
f.box(250, 158, 322, 66, "Availability: usable when needed\nControls: backups, redundancy, DDoS protection\nFailure: a bank app down on salary day", fill=SAND, stroke=AMBER, size=10)
```

```svgfig label="1.2" caption="STRIDE on a data-flow diagram of a municipal tax portal. The dashed line is the trust boundary. Badges show which threats apply to which element: S spoofing, T tampering, R repudiation, I information disclosure, D denial of service, E elevation of privilege."
f = Fig(580, 236)
f.box(8, 66, 90, 46, "Taxpayer\n(external entity)", fill=SAND, stroke=AMBER, size=10, bold=True)
f.circle(238, 89, 40, fill=BLUE, stroke=NAVY, label="Portal\nprocess", size=10)
f.box(420, 66, 112, 46, "Tax database\n(data store)", fill=MINT, stroke=TEAL, size=10, bold=True)
f.arrow([(98, 89), (198, 89)], label="login, payment", lpos=(148, 74))
f.arrow([(278, 89), (420, 89)], label="queries, updates", lpos=(349, 74))
for (x1, y1, x2, y2) in [(150, 20, 480, 20), (480, 20, 480, 160), (480, 160, 150, 160), (150, 160, 150, 20)]:
    f.line(x1, y1, x2, y2, color=RED, sw=1.6, dash=True)
f.text(315, 36, "trust boundary (our servers)", size=9.5, color=RED, bold=True)
for (x, y, s) in [(30, 128, "S"), (56, 128, "R"), (148, 108, "T"), (172, 108, "I"), (214, 138, "S"), (238, 138, "D"), (262, 138, "E"), (410, 128, "T"), (436, 128, "I"), (462, 128, "D")]:
    f.circle(x, y, 10, fill=ROSE, stroke=RED, label=s, size=9.5, color=RED)
f.box(8, 182, 564, 46, "S Spoofing breaks authenticity | T Tampering breaks integrity | R Repudiation breaks non-repudiation\nI Information disclosure breaks confidentiality | D Denial of service breaks availability | E Elevation breaks authorisation", fill="#f8fafc", stroke=SLATE, size=9.5)
```

```svgfig label="1.3" caption="A 5 x 5 risk matrix (likelihood x impact). Cell value = likelihood x impact. R1 (5 x 4 = 20) is critical, R2 (3 x 4 = 12) is high and R3 (2 x 2 = 4) is low, so the team fixes R1 first."
f = Fig(580, 262)
def col(v):
    return MINT if v <= 4 else ("#fde68a" if v <= 9 else ("#fdba74" if v <= 16 else ROSE))
for l in range(1, 6):
    for i in range(1, 6):
        f.box(60 + (i - 1) * 44, 14 + (5 - l) * 44, 44, 44, str(l * i), fill=col(l * i), stroke=SLATE, size=10)
for (l, i, n) in [(5, 4, "R1"), (3, 4, "R2"), (2, 2, "R3")]:
    f.circle(60 + (i - 1) * 44 + 22, 14 + (5 - l) * 44 + 22, 13, fill=NAVY, stroke=NAVY, label=n, size=9.5, color="#ffffff")
f.text(170, 252, "Impact (1 negligible ... 5 severe)", size=10.5, color=NAVY, bold=True)
f.text(30, 124, "Likelihood", size=10.5, color=NAVY, bold=True)
f.box(330, 20, 240, 40, "1-4 Low: accept and monitor", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(330, 68, 240, 40, "5-9 Medium: plan a fix", fill="#fde68a", stroke=AMBER, size=10.5, bold=True)
f.box(330, 116, 240, 40, "10-16 High: fix this quarter", fill="#fdba74", stroke=AMBER, size=10.5, bold=True)
f.box(330, 164, 240, 40, "17-25 Critical: fix now", fill=ROSE, stroke=RED, size=10.5, bold=True)
```

### 1.7.1 Eight principles of secure design

1. **Least privilege.** Every user and program gets only the access needed for the job. A clerk in a municipality needs to read tax files, not delete them. If that account is stolen, the damage stays small.
2. **Defence in depth.** Several different layers protect an asset, so one failure is not fatal. A bank uses guards, firewalls, encryption and monitoring together. An attacker must beat every layer, not just one.
3. **Fail-safe defaults.** Access is denied unless it is clearly allowed. A new Wi-Fi router should reject strangers until a password is set. This is safer than a system that allows everything until someone blocks it.
4. **Economy of mechanism.** Simple designs have fewer hidden mistakes. A login form with one clear check is easier to audit than five tangled ones. Small, clear code is easier for a student team to review.
5. **Complete mediation.** Every request is checked every time, not only the first one. Fonepay-style apps should recheck the session before each transfer. Caching an old "allowed" answer lets stolen sessions slip through.
6. **Separation of duties.** One person should not control a whole sensitive process. The person who creates a payment should not also approve it. This stops both fraud and honest mistakes from passing unnoticed.
7. **Open design.** Security must not depend on keeping the method secret, only the key. Public algorithms such as AES and TLS are trusted because experts have tested them for years. A secret homemade cipher is usually broken quickly.
8. **Psychological acceptability.** If a control is too hard, people work around it. Staff who must change a password daily will write it on a sticky note. Good security fits the way people actually work, for example a fingerprint unlock on a phone.

## 1.8 Summary and exercises

Security protects confidentiality, integrity and availability through layered, least-privilege controls; threat modelling with DFDs and STRIDE finds problems before they are built; risk can be ranked with a matrix or DREAD average; and CVSS gives a reproducible severity score that must be combined with context.

1. Define asset, threat, vulnerability, risk and control, and give a Nepali example of each.
2. Match each STRIDE letter to the property it violates and a mitigation.
3. Rate a threat with D=6, R=5, E=4, A=9, D=3 using DREAD. What band results?
4. Compute the ISS for C:L, I:L, A:N and the unchanged-scope Impact.
5. Why can a vulnerability with a lower CVSS score deserve earlier patching?
6. Explain two cases where confidentiality and availability conflict.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the CIA triad with examples and controls.**

*Introduction.* The CIA triad is the base model of information security. It names three goals that every control tries to protect: confidentiality, integrity and availability (Figure 1.1).

1. **Confidentiality** means only authorised people can read the information. A hospital record must be seen by the treating doctor, not by every staff member. Controls are encryption, access control lists and multi-factor login.
2. **Integrity** means data changes only in authorised and detectable ways. A student's exam mark must not be edited silently. Controls are hashing, digital signatures, input validation and change control with audit logs.
3. **Availability** means the system works when users need it. A bank app that is down on salary day fails this goal even if no data leaks. Controls are backups, redundant servers, capacity planning and DDoS protection.

| Goal | Threat example | Control example |
|---|---|---|
| Confidentiality | Records published by mistake | Encrypt data, restrict access |
| Integrity | Tampered balance | SHA-256 hash, signed logs |
| Availability | Server outage | Backup site, load balancer |

*Conclusion.* The goals can conflict: strong encryption helps confidentiality, but a lost key ruins availability. A good design balances all three for the value of the asset.

**Q2 (5 marks). What is threat modelling? Describe the STRIDE categories using a data-flow diagram.**

*Introduction.* Threat modelling is a structured way to find what can go wrong in a design before the system is built. Fixing a design flaw on paper costs far less than fixing it after launch (section 1.4).

*Method.* The team draws a data-flow diagram (DFD) with external entities, processes, data stores, data flows and a trust boundary. Each element is then checked against the six STRIDE threats (Figure 1.2).

| Letter | Threat | Property broken | Typical mitigation |
|---|---|---|---|
| S | Spoofing | Authenticity | Strong login, MFA |
| T | Tampering | Integrity | Hashes, signatures, TLS |
| R | Repudiation | Non-repudiation | Audit logs, signatures |
| I | Information disclosure | Confidentiality | Encryption, access control |
| D | Denial of service | Availability | Rate limits, redundancy |
| E | Elevation of privilege | Authorisation | Least privilege, input checks |

*Example.* In a municipal tax portal, the taxpayer-to-portal flow crosses the trust boundary, so tampering and disclosure are checked first. The database element is checked for tampering, disclosure and denial of service. Each threat found is written down with a mitigation and an owner.

*Conclusion.* Threat modelling turns a vague worry into a checklist the team can fix and test.

**Q3 (10 marks). Explain how a security team assesses and ranks the risk of a web portal using the risk matrix, DREAD and CVSS.**

*Introduction.* A portal such as a tax-payment site has more weaknesses than a team can fix at once. Risk assessment ranks them so that limited time is spent on the dangers that matter most. Risk is the combination of how likely an event is and how bad the result would be (sections 1.5 and 1.6).

*Step 1: list assets, threats and vulnerabilities.* The assets are taxpayer records, payment data and the portal's availability. STRIDE on the data-flow diagram (Figure 1.2) gives the threats, and scanning and code review give the vulnerabilities.

*Step 2: qualitative ranking with a matrix.* Each risk gets a likelihood and an impact from 1 to 5, and the product is its score (Figure 1.3). In the example R1 is 5 x 4 = 20 (critical), R2 is 3 x 4 = 12 (high) and R3 is 2 x 2 = 4 (low). The order of work is therefore R1, R2, R3.

*Step 3: DREAD average.* The team scores Damage, Reproducibility, Exploitability, Affected users and Discoverability from 0 to 10 and takes the mean. A threat with 6, 5, 4, 9 and 3 has an average of 5.4, which is a medium rating. DREAD is easy but subjective, so two reviewers should score separately and compare.

*Step 4: CVSS for known vulnerabilities.* CVSS v3.1 turns a vector into a repeatable score. For AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H the impact sub-score is ISS = 1 - (0.44 x 0.44 x 0.44) = 0.9148, so Impact = 6.42 x 0.9148 = 5.873. Exploitability is 8.22 x 0.85 x 0.77 x 0.85 x 0.85 = 3.887. The base score is the round-up of 5.873 + 3.887 = 9.76, which is **9.8 (Critical)**.

*Step 5: decide the treatment.*

| Option | Meaning | Example |
|---|---|---|
| Mitigate | Add controls to cut the risk | Patch and add a web application firewall |
| Transfer | Share the cost with another party | Cyber insurance, managed provider |
| Avoid | Stop the risky activity | Remove an unused upload page |
| Accept | Live with a small risk | Low-score issue on an internal tool |

*Caution.* CVSS measures the severity of a flaw in general, not risk to your organisation. A 9.8 on an unreachable test server may matter less than a 6.5 on the public payment service, so context always adjusts the order.

*Conclusion.* A defensible ranking uses several tools: STRIDE to find threats, the matrix and DREAD to compare them, CVSS for known flaws, and business context to decide. The result is a written risk register that the management can approve.
