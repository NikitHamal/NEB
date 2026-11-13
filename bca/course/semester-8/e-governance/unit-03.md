---
subject: E-Governance
grade: BCA Semester 8 (Elective III)
unit: 3
title: E-Governance Infrastructure, Stages in Evolution and Strategies for Success
hours: 8
area: BCA 453 · E-Governance · Unit 3
---

A portal is the visible one per cent of an e-governance project. Under it lie registers that must be accurate, laws that must recognise electronic records, offices that must own the service, people who must run it and networks that must stay up. Projects fail when the one per cent is built and the ninety-nine are assumed. **E-readiness** is the habit of checking the ninety-nine first. This unit covers the five infrastructures in the TU outline, the evolutionary stages through which e-governance passes, and the strategies that separate the few successes from the many failures.

::: key What this unit gives you
- E-readiness and its five parts: **data system**, **legal**, **institutional**, **human** and **technological** infrastructure, each with the questions to ask and Nepali examples.
- A composite readiness score computed in code, with the weakest-link idea.
- The **evolutionary stages** of e-governance from computerisation to transformation, and how to place a project on them.
- **Strategies for success**: critical success factors, process redesign, change management, interoperability, security, partnerships, financing, and Heeks's design-reality gap scored with ITPOSMO.
- A cost-benefit program (NPV, benefit-cost ratio, payback and the effect of low adoption).
:::

## 3.1 E-readiness

### 3.1.1 What e-readiness means

**E-readiness** is the degree to which a country, a government or an organisation is prepared to take part in and benefit from ICT-enabled governance. It is measured before a project (to decide what to fix first) and after (to see progress). Global indices such as the UN's EGDI (Unit 1) and the Network Readiness Index measure countries; a ministry can measure itself with a checklist like the one in this section.

```svgfig label="3.1" caption="The five infrastructures of e-readiness as pillars under the e-services roof. If one pillar is missing the roof tilts; a strong portal does not repair a weak register."
f = Fig(680, 320)
f.poly([(40, 80), (340, 20), (640, 80)], fill=SAND, stroke=AMBER, label="E-services and e-governance outcomes", lx=340, ly=62, size=12, color=AMBER)
pillars = [("Data system", "registers, IDs,\nquality, standards", NAVY, BLUE), ("Legal", "e-records, RTI,\nprivacy, cyber law", RED, ROSE), ("Institutional", "mandate, CIO,\nfunding, coordination", AMBER, SAND),
           ("Human", "skills, literacy,\nchange readiness", TEAL, MINT), ("Technological", "network, data centre,\ndevices, security", NAVY, BLUE)]
for i, (a, b, col, fill) in enumerate(pillars):
    x = 40 + i * 120
    f.box(x, 95, 100, 175, "", fill=fill, stroke=col)
    f.text(x + 50, 125, a, size=10.5, color=col, bold=True)
    f.text(x + 50, 175, b, size=9, color=SLATE)
f.box(30, 275, 620, 30, "Foundation: political will, citizen demand, sustained budget", fill=SOFT, stroke=SLATE, size=10.5, color=SLATE)
```

### 3.1.2 Data system infrastructure

Everything an e-service does is a read or a write on a **register**: the population register, the land register, the vehicle register, the taxpayer register. If these are on paper, or digital but wrong, duplicated or coded differently in each office, no portal can deliver.

- **Digitised, clean registers**: legacy paper records scanned and, more important, **keyed in and verified** as structured data; scans alone cannot be searched or checked.
- **Unique identifiers**: a person, a parcel, a business and a vehicle each need one key that every agency uses (in Nepal the National ID number is intended as such a key for persons).
- **Data quality**: accuracy, completeness, timeliness and consistency (the same name spelt the same way). Dirty data become wrong decisions at scale.
- **Standards and metadata**: common codes for districts and wards, date formats, names in Nepali and English, definitions of every field.
- **Storage, backup and ownership**: a government data centre, a disaster-recovery copy, named data owners and custodians.
- **Data sharing rules**: which agency may read which field, for what purpose and with what consent.

### 3.1.3 Legal infrastructural preparedness

Law decides whether an electronic act counts. The questions: is an electronic record or signature valid in court? is a digital copy accepted in place of paper? who is liable when data leak? are cyber offences defined? can citizens demand information? For Nepal the **Electronic Transactions Act, 2063** recognises electronic records and digital signatures and defines computer offences; the **Right to Information Act, 2064** gives the information right; the **Individual Privacy Act, 2075** (2018) addresses personal data; a cyber security policy and an information technology bill have been drafted and revised over the years (check the current status). Sector rules must follow: if the land law still says "stamped paper", the digital land record has no standing. A frequent finding is that the law exists but **offices do not apply it**, so legal readiness also means circulars, rules and training that bring practice in line.

### 3.1.4 Institutional infrastructural preparedness

Institutions give e-governance an owner, a mandate and money. Typical elements: a **national ICT body** and a ministry for policy (in Nepal the Ministry of Communication and Information Technology, with the National Information Technology Centre and the Department of Information Technology for operations and hosting); **chief information officers** and IT units in each agency; a steering committee that can settle disputes between agencies; **budget rules** that fund maintenance and not only purchase; procurement rules that let agencies buy cloud and services; and, in a federation, clear **roles for the three tiers** of government. Without a body that can say "use the common platform", every ministry builds its own and the citizen meets the cost of the duplication.

### 3.1.5 Human infrastructural preparedness

People are both the users and the operators. The question has three layers: **citizens** (literacy, digital skills, trust); **officials** (skills to use, run and improve systems; willingness to change work habits; incentives to share data); and **IT professionals** (enough trained developers, analysts and security specialists, and a career path that keeps them in the public service). Literacy matters as a base: the 2021 census gave Nepal's literacy rate of people aged five and above as roughly 76 per cent, with a clear gap between men and women and between urban and rural areas (check the census tables for the exact figures). Government staff transfers are a hidden risk: the trained officer leaves, the system loses its owner. The remedies are training that is tied to real tasks, ward-level facilitators, and documentation that outlives individuals.

### 3.1.6 Technological infrastructural preparedness

Network (fibre backbone, mobile coverage, last-mile links to ward offices), **computing** (servers or cloud, a government data centre with back-up), **devices** (computers at the counter, smartphones for citizens), **platforms** (identity, payment gateway, messaging, digital signature, shared directory), **security** (authentication, encryption, logging, incident response) and **power** (electricity with back-up). A single missing piece can stall a service: a ward office with a computer but no stable link cannot print a certificate.

### 3.1.7 Measuring readiness: a weakest-link score

The program scores a hypothetical municipality on the five infrastructures. A plain average hides a missing pillar, so it also reports the **weakest-link** score (the minimum) and a blended index that weights the minimum heavily; what a project plan needs is the list of what to fix first.

```python
pillars = {
    "Data system":   {"registers digitised": 40, "unique ID used": 30, "data quality": 45, "standards": 35},
    "Legal":         {"e-records valid": 70, "privacy rules": 50, "offices apply law": 40},
    "Institutional": {"owner and mandate": 55, "budget for upkeep": 35, "inter-agency forum": 45},
    "Human":         {"staff skills": 45, "citizen digital skills": 40, "retention of trained staff": 30},
    "Technological": {"network at wards": 60, "data centre and backup": 65, "security": 50, "power backup": 55},
}
score = {p: sum(v.values()) / len(v) for p, v in pillars.items()}
for p, s in score.items():
    print("%-14s %5.1f %s" % (p, s, "#" * int(s // 5)))
avg = sum(score.values()) / len(score)
low = min(score.values())
blend = 0.4 * avg + 0.6 * low
print("\naverage of pillars : %.1f" % avg)
print("weakest pillar     : %s (%.1f)" % (min(score, key=score.get), low))
print("blended readiness  : %.1f / 100  (0.4 x average + 0.6 x weakest)" % blend)
items = sorted(((v, p, k) for p, d in pillars.items() for k, v in d.items()))[:4]
print("fix first:", "; ".join("%s / %s (%d)" % (p, k, v) for v, p, k in items))
```
```output
Data system     37.5 #######
Legal           53.3 ##########
Institutional   45.0 #########
Human           38.3 #######
Technological   57.5 ###########

average of pillars : 46.3
weakest pillar     : Data system (37.5)
blended readiness  : 41.0 / 100  (0.4 x average + 0.6 x weakest)
fix first: Data system / unique ID used (30); Human / retention of trained staff (30); Data system / standards (35); Institutional / budget for upkeep (35)
```
The blended score (41.0) is lower than the average (46.3) because the weakest pillars, data system (37.5) and human (38.3), pull it down. The unique ID (30) and the retention of trained staff (30) head the fix-first list, and neither is a purchase. That is the practical meaning of e-readiness: a sequence of non-technical tasks that decide whether technology will be used.

## 3.2 Evolutionary stages in e-governance

### 3.2.1 The stages

E-governance does not appear in a single step. Governments move through stages, and a stage cannot be skipped without risk, because each rests on the one below. The stages, in the form commonly given with this syllabus, are:

```svgfig label="3.2" caption="Evolutionary stages of e-governance with a Nepali illustration for each. The citizen-facing value rises with each stage, and so does the dependence on the stages below."
f = Fig(680, 300)
st = [("1 Computerisation", "payroll and census\non computers", SOFT, SLATE), ("2 Networking", "office LANs, email,\nwide-area links", BLUE, NAVY), ("3 Online presence", "ministry websites,\nnotices, forms to read", MINT, TEAL),
      ("4 Interaction", "download forms, RTI\nrequests, e-mail replies", SAND, AMBER), ("5 Transaction", "online PAN, tax,\nbids, payments", ROSE, RED), ("6 Transformation", "one identity, shared data,\nNagarik App, one-stop", BLUE, NAVY)]
for i, (a, b, fill, col) in enumerate(st):
    x = 12 + i * 111
    h = 60 + i * 38
    f.box(x, 285 - h, 104, h, "", fill=fill, stroke=col)
    f.text(x + 52, 285 - h + 16, a, size=9, color=col, bold=True)
    f.text(x + 52, 285 - h + 42, b, size=8, color=SLATE)
```

| Stage | What exists | Citizen's experience | Main risk |
|---|---|---|---|
| 1 Computerisation | PCs and standalone applications in departments | None; office speed improves | Islands of data |
| 2 Networking | LAN, WAN, email, intranet, shared servers | Little; faster replies from staff | Standards missing, no security |
| 3 Online presence | Websites with information | Can read notices and download forms | Out-of-date content |
| 4 Online interaction | Forms submitted, queries answered, status checked | Fewer visits | Back office still on paper |
| 5 Online transaction | Payments, licences, bids completed online | Full service without a visit | Identity, security, legal validity |
| 6 Transformation | Integrated back office, common identity and data, services built around life events | Government appears as one; proactive services | Governance of shared data, privacy |

### 3.2.2 Using the stages

Place each service, not the whole government, on the scale: a country can be at stage 5 for tax and stage 1 for land. The stage of a project is the stage at which the **citizen can finish the task**, which is lower than the stage of its marketing. A "paperless" service that still demands a stamped copy is at stage 4. Moving up the scale demands **back-office work before front-end work**: you cannot offer stage 5 over a stage 1 register. The idea that jumping to a high stage is possible with a donor-funded portal is the cause of many failures.

## 3.3 Strategies for success

### 3.3.1 Why most projects fail

Studies by Heeks of e-government projects in developing countries found that roughly one project in three was a total failure (never used, or dropped at once), about half were partial failures (some goals met, others missed, or benefits not shared), and only a small share was a clear success. The **design-reality gap** explains most cases: the design carries assumptions about the seven dimensions of **ITPOSMO**, and the real organisation differs.

| Letter | Dimension | Question |
|---|---|---|
| I | Information | Are the data the system expects available and accurate? |
| T | Technology | Does the hardware, software and network fit the site? |
| P | Processes | Do the actual work procedures match the new ones? |
| O | Objectives and values | Do the users share the goals of the designers? |
| S | Staffing and skills | Are there enough people with the skills needed? |
| M | Management systems and structures | Does the organisation have the authority and routines to run it? |
| O | Other resources | Time and money, including after the grant ends |

The program rates a proposed land-record system on each dimension, once for the design assumption and once for reality, on a scale of 0 to 10. The gap on each dimension is the difference; the larger the total gap, the greater the risk.

```python
# dimension: (what the design assumes, what the site really has)
itposmo = {
    "Information":                 (9, 4),   # records assumed clean; many are handwritten and disputed
    "Technology":                  (8, 6),
    "Processes":                   (9, 3),   # design replaces 5 steps with 1; clerks still run 5
    "Objectives and values":       (8, 5),
    "Staffing and skills":         (7, 3),
    "Management systems":          (8, 5),
    "Other resources (time, money)": (8, 4),
}
total = 0
print("%-32s %7s %8s %5s" % ("dimension", "design", "reality", "gap"))
for k, (d, r) in itposmo.items():
    total += d - r
    print("%-32s %7d %8d %5d" % (k, d, r, d - r))
mean_gap = total / len(itposmo)
risk = "low" if mean_gap < 2 else "moderate" if mean_gap < 4 else "high"
print("\ntotal gap %d, mean gap %.1f (of 10) -> failure risk: %s" % (total, mean_gap, risk))
print("worst gap:", max(itposmo, key=lambda k: itposmo[k][0] - itposmo[k][1]))
```
```output
dimension                         design  reality   gap
Information                            9        4     5
Technology                             8        6     2
Processes                              9        3     6
Objectives and values                  8        5     3
Staffing and skills                    7        3     4
Management systems                     8        5     3
Other resources (time, money)          8        4     4

total gap 27, mean gap 3.9 (of 10) -> failure risk: moderate
worst gap: Processes
```
The thresholds in the code (2 and 4) are a teaching rule, not a published constant. The use of the exercise is the **list of worst gaps**: here Processes and Information, so the project should first redesign the work and clean the records, then start the software.

### 3.3.2 Strategies that work

1. **Start from a citizen problem and a measurable objective** (for example "issue a recommendation letter in one day at any ward"), not from a technology.
2. **Redesign the process before automating it.** Remove steps, signatures and documents that have no purpose (business process re-engineering); automate the improved process.
3. **Leadership and ownership.** A named senior champion, a project team with authority, and a service owner after launch. Many failures have no owner.
4. **Think big, start small, scale fast.** An architecture for the whole, a pilot in a few offices, evaluation, then expansion. A pilot that is never evaluated is a demonstration.
5. **Standards and interoperability.** Common codes, open standards, shared identity and payment services, and an interoperability framework (Nepal has worked on a government interoperability framework, NeGIF) so that systems can exchange data instead of being rebuilt.
6. **Change management and training.** Involve users in design, train on real tasks, and align incentives so that staff gain from the new system, not only lose a source of power.
7. **Security and privacy by design.** Role-based access, logging, encryption, backup, and data-minimisation, with a plan for incidents. A single breach can destroy trust.
8. **Choose delivery channels for the real citizen**: assisted service centres, kiosks, mobile and SMS, voice, local languages; keep a counter option for those not connected.
9. **Partnerships with care.** Public-private partnership or outsourcing can bring skill and funds, but the contract must protect data ownership, source code or escrow, service levels and an exit route.
10. **Financing and sustainability.** Budget the **total cost of ownership** for five to ten years (licences, hosting, upkeep, training, replacement), not the purchase alone; consider user fees, savings and revenue gains that return to the project.
11. **Measure and publish results.** Baselines before launch, then time, cost, error rate, use and satisfaction.
12. **Legal and policy support.** Rules that recognise the electronic process, and enforcement that makes offices use it.

### 3.3.3 Costs and benefits

Project approval needs numbers. The program evaluates an online certificate platform for a municipality over five years at a 10 per cent discount rate. It shows two views: the **government's cash view** (costs against staff savings and extra revenue) and the **social view**, which adds the time and travel the citizens save (the Unit 1 model, NPR 1,700 per user). Adoption starts low and grows. The last lines show what happens if adoption stalls at half of the plan.

```python
rate = 0.10
capex, opex = 12.0, 2.0                       # NPR million: year-0 build; yearly running cost
users = 12000
saving_per_user = 1700 / 1e6                  # NPR million per transaction (Unit 1 model)
adoption = [0.30, 0.50, 0.70, 0.80, 0.85]     # years 1..5, planned share of users who go online
staff_saving = [0.0, 0.48, 0.96, 0.96, 0.96]  # NPR million: clerk time freed, from year 2
extra_revenue = [0.0, 1.0, 1.5, 1.5, 1.5]     # NPR million: better tax and fee collection

def run(scale=1.0):
    gov, soc = [-capex], [-capex]
    for t in range(5):
        a = adoption[t] * scale
        g = staff_saving[t] * scale + extra_revenue[t] * scale - opex
        c = users * a * saving_per_user
        gov.append(g); soc.append(g + c)
    return gov, soc
def npv(cf):
    return sum(v / (1 + rate) ** i for i, v in enumerate(cf))
def payback(cf):
    cum = 0.0
    for i, v in enumerate(cf):
        cum += v
        if cum >= 0:
            return i
    return None
for label, scale in (("planned adoption", 1.0), ("adoption at 50% of plan", 0.5)):
    gov, soc = run(scale)
    pv_costs = capex + sum(opex / (1 + rate) ** t for t in range(1, 6))
    bcr = (npv(soc) + pv_costs) / pv_costs
    print("%-24s government NPV %6.2f   social NPV %6.2f   social B/C %.2f   payback (social): %s"
          % (label, npv(gov), npv(soc), bcr, payback(soc) if payback(soc) is not None else "beyond year 5"))
```
```output
planned adoption         government NPV -13.30   social NPV  33.33   social B/C 2.70   payback (social): 2
adoption at 50% of plan  government NPV -16.44   social NPV   6.88   social B/C 1.35   payback (social): 4
```
Two readings follow. First, the **government's own cash flow** is negative even with full adoption: most of the benefit is the citizens' time. Funding therefore needs a public decision (a budget line, a donor, a shared-service model), not an expectation that the project will pay for itself. Second, the benefit depends on **adoption**: when half the planned citizens use the service, the social NPV falls sharply, which is why training, assisted counters and channel choice count as part of the project budget.

## 3.4 Summary and exercises

**Summary.** E-readiness asks whether the foundations exist: a **data system** of clean registers with unique identifiers and standards; **legal** recognition of electronic records, information rights and privacy; **institutions** with mandate, ownership and funds; **human** skills and willingness among citizens, officials and IT staff; and **technological** networks, data centres, platforms and security. Services evolve from computerisation through networking, online presence, interaction and transaction to transformation, and each stage depends on the one below. Success strategies include a citizen-centred objective, process redesign before automation, ownership, phased scaling, standards, change management, security, suitable channels, careful partnerships, whole-life financing and measurement. Heeks's design-reality gap, scored with ITPOSMO, explains why most projects fail.

1. Define e-readiness. Why is it measured before a project?
2. Explain the five infrastructures of e-readiness with an example of each from Nepal.
3. Why is scanning paper records not enough for data system readiness? What else is needed?
4. What does it mean that law may exist but practice may not follow? Give an example.
5. List the institutional elements an e-governance programme needs, and say why a national body matters.
6. A readiness checklist gives the pillar scores 60, 40, 50, 30 and 70. Find the average, the weakest score and the blended index 0.4 x average + 0.6 x weakest.
7. Describe the six evolutionary stages of e-governance with an example of each.
8. A tax portal lets users file and pay online, but the invoice data are keyed in by clerks from paper. At which stage is the service in practice, and what should be done next?
9. State the design-reality gap. Name the seven ITPOSMO dimensions.
10. Design scores for four dimensions are 9, 8, 7 and 9 and reality scores are 5, 6, 3 and 4. Compute each gap and the mean gap.
11. List eight strategies for success in e-governance and justify any three.
12. Explain how a project may be right for society and negative for the government's cash flow. What follows for funding?
13. A project costs NPR 10 million now and returns NPR 3 million a year for five years. Find the NPV at 10 per cent and the simple payback time.
14. Explain why adoption matters more than software features, with an example.
15. Discuss the strategies by which Nepal can improve the e-governance readiness of its municipalities.

**Answers to the numerical items.** (6) Average = (60 + 40 + 50 + 30 + 70)/5 = **50**; weakest = **30**; blended = 0.4 x 50 + 0.6 x 30 = 20 + 18 = **38**. (8) **Stage 4 (interaction) in practice**, because the back office is on paper; automate the invoice data capture (e-invoice or data upload) before adding more online features. (10) Gaps: 4, 2, 4, 5; mean = 15/4 = **3.75**. (13) Annuity factor for 5 years at 10 per cent = (1 - 1.1^-5)/0.1 = 3.7908; PV of benefits = 3 x 3.7908 = 11.372; **NPV = 11.372 - 10 = NPR 1.37 million**; simple payback = 10/3 = **3.33 years**.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is e-readiness? Explain its components.**

E-readiness is the degree to which a country or government is prepared to take part in and benefit from ICT-enabled governance. Components: (1) data system infrastructure (digitised, accurate registers, unique identifiers, standards, storage and back-up); (2) legal infrastructure (laws that recognise electronic records and signatures, information and privacy rights, cyber offences); (3) institutional infrastructure (mandate, ownership, funding, coordination among agencies and tiers); (4) human infrastructure (skills and attitudes of citizens, officials and IT professionals); (5) technological infrastructure (networks, data centres, platforms, devices, security, power). A weak pillar limits the others, so readiness is judged by the weakest area as well as the average.

**Q2 (5 marks). Explain the evolutionary stages of e-governance.**

Stages: computerisation, networking, online presence, interaction, transaction and transformation. For each give what exists, the citizen's experience and an example (payroll on computers; office networks and email; ministry websites; downloadable forms and status check; online tax and bids; integrated identity and one-stop services such as the Nagarik App). Add that each stage rests on the one below, that services (not countries) are placed on the scale, and that the stage of a service is the stage at which the citizen can finish the task.

**Q3 (10 marks). Why do many e-governance projects fail? Suggest strategies for success.**

Open with the quantitative picture (about one in three total failures, half partial, a small share of successes in developing countries) and explain the design-reality gap by the seven ITPOSMO dimensions with a one-line example each. Then give the strategies: citizen-centred objective, process redesign, ownership and leadership, phased scaling with evaluated pilots, standards and interoperability, change management and training, security and privacy, suitable channels, careful partnerships, whole-life financing, measurement and legal support. Illustrate with a Nepali example (a portal built over paper registers, or a trained officer transferred away). Conclude that the technical part of a project is small, and that success is decided by the institutional and human parts.

**Q4 (10 marks). Describe the infrastructure needed for e-governance in a developing country such as Nepal.**

Describe each of the five infrastructures with the specific needs and the Nepali position: registers, the National ID key, data quality, standards and the government data centre; the Electronic Transactions Act, the RTI Act, the Individual Privacy Act and gaps in practice; the Ministry of Communication and Information Technology, NITC and DoIT, and the roles of three tiers of government after federalism; literacy, digital skills of citizens and staff, and retention of trained officials; networks to wards, mobile coverage, data centre, power and security. Add the weakest-link reasoning and the readiness score idea, and close with the first three actions a municipality should take (clean the registers, train and retain staff, ensure a reliable link and back-up).
