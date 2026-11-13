---
subject: E-Governance
grade: BCA Semester 8 (Elective III)
unit: 1
title: Introduction
hours: 6
area: BCA 453 · E-Governance · Unit 1
---

In 2021 a student in Biratnagar could open a phone, sign in with a citizenship number and see a police clearance report, a PAN number and a voter card in one place, without queuing at three offices. Twenty years earlier the same errands meant three days, several photocopies and, too often, a small payment to a clerk to make a file move. The change did not come from the phone alone. It came from a long, uneven effort to rebuild how the state collects data, takes decisions and serves people. That effort is called **e-governance**, and this unit explains what it is, why governments pursue it, what stands in its way, how it developed, and where Nepal stands.

::: key What this unit gives you
- Exact definitions of e-governance, e-government and governance, and the four interaction types G2C, G2B, G2G and G2E.
- The objectives and benefits of e-governance, with the numbers a good answer should quote.
- The issues in e-governance applications and a measurable view of the digital divide.
- The evolution, scope and content of e-governance, from computerisation to AI-assisted services.
- Present global trends, including the UN E-Government Development Index (EGDI), computed in code.
- E-governance applications by sector and the Nepali initiatives from the 2000 IT policy to the Nagarik App.
:::

## 1.1 E-governance: an overview

### 1.1.1 Governance, government and e-governance

**Governance** is the way power is used to manage a country's economic and social resources: the rules, processes and institutions through which decisions are made and carried out and through which citizens and groups voice interests and hold officials to account. **Government** is one actor in governance (the institutions that make and enforce public decisions). The private sector, civil society, the media and citizens are the others.

**E-governance** is the use of information and communication technology (ICT) by government, and by those who deal with it, to improve the processes of governance: delivery of public services, internal administration, citizen participation and accountability. **E-government** (the term used in the UN survey) is narrower: it stresses the government's own use of ICT to deliver information and services. A common classroom definition is the one from the textbook, C. S. R. Prabhu: e-governance is the application of ICT to government functioning in order to achieve **SMART** governance, which means *Simple, Moral, Accountable, Responsive and Transparent*.

| Term | Focus | Example |
|---|---|---|
| Governance | How decisions are made and enforced, by whom | A ward committee approving a budget in public |
| Government | The institutions of the state | Ministry, municipality, court |
| E-government | The state's online services and internal systems | Online driving licence renewal |
| E-governance | Governance processes and relationships changed by ICT | Citizens commenting on a draft law online; budget dashboards |
| Digital transformation | Re-designing services around data and user needs | One citizen identity used across agencies |

E-governance is **not** buying computers. A ministry that scans paper forms and then asks the citizen to bring a printed copy has automated a form, not changed governance. The test is whether a rule, a process or a relationship became simpler, faster or more open.

### 1.1.2 The four interaction types

The government deals with four kinds of partner, and every e-governance application can be placed in one of these cells.

```svgfig label="1.1" caption="The four interaction types of e-governance, drawn around the government: citizens (G2C), businesses (G2B), other government bodies (G2G) and employees (G2E). Examples are from Nepal."
f = Fig(680, 330)
f.box(250, 125, 180, 80, "Government\n(three tiers)", fill=SOFT, stroke=NAVY, size=13, bold=True)
f.box(20, 20, 200, 70, "Citizens (G2C)\nNagarik App, online PAN,\nvoter list lookup", fill=MINT, stroke=TEAL, size=10)
f.box(460, 20, 200, 70, "Businesses (G2B)\nCompany registration,\ne-procurement (PPMO)", fill=SAND, stroke=AMBER, size=10)
f.box(20, 240, 200, 70, "Employees (G2E)\nPersonnel records, payroll,\ne-attendance, training", fill=ROSE, stroke=RED, size=10)
f.box(460, 240, 200, 70, "Other government (G2G)\nSuTRA treasury data between\nfinance ministry and local levels", fill=BLUE, stroke=NAVY, size=10)
f.arrow([(220, 70), (270, 125)], color=TEAL, both=True)
f.arrow([(460, 70), (410, 125)], color=AMBER, both=True)
f.arrow([(220, 260), (270, 205)], color=RED, both=True)
f.arrow([(460, 260), (410, 205)], color=NAVY, both=True)
```

- **G2C (government to citizen)** covers services and information: applications, certificates, tax payments, grievances. It is the most visible type.
- **G2B (government to business)** covers company registration, licences, tax and customs, and public procurement. Businesses meet the state more often than most citizens do, so G2B savings are large.
- **G2G (government to government)** covers data and workflow exchange between agencies and between the federal, provincial and local levels. Poor G2G is the reason a citizen has to carry the same document from office to office.
- **G2E (government to employee)** covers the state as employer: payroll, pension, training, leave and performance records.

Some authors add C2G (citizen to government: complaints, feedback, voting) and B2G (supplier bids). For the exam, remember G2C, G2B, G2G and G2E, and mention that interaction runs both ways.

### 1.1.3 Components of an e-governance system

Every working system has five parts: **people** (citizens, officials, IT staff); **process** (rules and workflows after redesign); **data** (registers such as citizenship, land, vehicles); **technology** (network, servers, applications, payment and identity services); and **law and policy** (the legal force of electronic records, data protection, standards). Failures usually come from the first, second and fifth parts, not from the technology. This idea returns in Unit 3.

## 1.2 Why e-governance

### 1.2.1 Objectives

1. **Better service delivery**: faster, cheaper, available at any hour and from any place.
2. **Transparency**: rules, files and decisions visible, so that discretion and bribery shrink.
3. **Accountability**: every action leaves a time-stamped record that can be audited.
4. **Efficiency**: fewer repeated data entries, fewer paper movements, lower cost per transaction.
5. **Inclusion and reach**: services for a citizen in Humla as for one in Kathmandu.
6. **Participation**: citizens can inform, consult and co-decide, not only receive services.
7. **Evidence-based policy**: data from the services feed planning (Unit 4).

### 1.2.2 Benefits, with numbers

A saving is easy to claim and hard to measure, so examiners like a worked example. The program below compares a manual counter with an online service for one municipal certificate, using illustrative but plausible figures for a district town: travel cost, lost wages, and the waiting time of the citizen. It is a model, not a survey result.

```python
# Cost to the citizen of one certificate: counter versus online (illustrative inputs).
visits_manual, visits_online = 3, 0          # trips to the office
bus_fare = 60                                # NPR per round trip
wage_per_hour = 125                          # NPR, a daily wage of NPR 1,000 over 8 hours
hours_per_visit = 4                          # travel plus queue
photocopies, copy_cost = 6, 5                # NPR per page
fee = 100                                    # official fee in NPR, same either way
online_extra = 10                            # NPR, data and payment gateway charge

manual = visits_manual * (bus_fare + hours_per_visit * wage_per_hour) + photocopies * copy_cost + fee
online = fee + online_extra
print("manual total  : NPR", manual)
print("online total  : NPR", online)
print("saving        : NPR", manual - online, "(%.0f%%)" % (100 * (manual - online) / manual))
users = 12000                                # certificates a year in a large municipality
print("saving for %d users a year: NPR %.2f million" % (users, users * (manual - online) / 1e6))
```
```output
manual total  : NPR 1810
online total  : NPR 110
saving        : NPR 1700 (94%)
saving for 12000 users a year: NPR 20.40 million
```
The saving to the citizen (about 94 per cent in this model) is larger than the saving to the office. This is the usual pattern: the strongest argument for e-governance is the time and travel returned to the citizen.

::: key Remember
Quote benefits under four heads: **cost** (citizen and state), **time** (waiting, processing), **quality** (accuracy, consistency) and **trust** (transparency, less corruption). Then give one measured example, such as the Bhoomi and CARD figures in Unit 5.
:::

## 1.3 Issues in e-governance applications and the digital divide

### 1.3.1 Issues that decide success or failure

| Issue | What goes wrong | Typical symptom |
|---|---|---|
| Infrastructure | Power cuts, slow links, no data centre back-up | Counter staff say "the system is down" |
| Legal | Electronic records or signatures not accepted; no data protection law | An office demands a stamped paper copy of a digital certificate |
| Process | Old rules copied into software | Seven signatures, now seven clicks |
| People | Few trained staff, resistance to change, high turnover | Trained officer is transferred; system is unused |
| Interoperability | Each agency builds its own database and codes | Same person with three spellings, no common key |
| Security and privacy | Weak passwords, shared accounts, no audit log | Leak of citizens' records |
| Cost and sustainability | Donor project ends, no maintenance budget | Portal stops updating after two years |
| Trust and usability | Services hard to find or in a language the user does not read | Citizens go back to the agent |
| Digital divide | Many cannot access or use the service | Services designed only for the connected |

Richard Heeks, who has studied hundreds of cases, found that most e-government projects in developing countries end as **total failures** (never used or abandoned) or **partial failures** (major goals missed), and only a minority as successes. His explanation is the **design-reality gap**: the distance between what the system assumes (data, technology, processes, objectives and values, staffing and skills, management and structures, other resources) and the reality of the organisation where it lands. Unit 3 uses this ITPOSMO checklist to score a project.

### 1.3.2 The digital divide

The **digital divide** is the gap between those who can use ICT effectively and those who cannot. It has three layers:

1. **Access divide**: no device, no network, no electricity.
2. **Skills divide**: access exists but the person cannot use it well (digital literacy, language, literacy).
3. **Outcome (usage) divide**: even equal skill gives unequal benefit, because the services themselves, or the capacity to benefit, differ.

It follows income, gender, age, geography (hill and mountain districts), disability and language. In Nepal, mobile subscriptions are numerous (the regulator's count is around or above one per person, because many people hold two SIMs), so the telecommunication index of the UN survey is the strongest of Nepal's three components; the weaker parts are online services and human capital. Having a SIM is not the same as being able to file a tax return.

The idea that a service reaches only the people who pass **every** hurdle can be written as a product: reach = access × skill × affordability × trust, each as a fraction. The program uses made-up fractions to show why a service that looks 80 per cent available to a group may effectively serve only a quarter of it.

```python
groups = {
    # name: (access, skill, affordability, trust) as fractions of the group
    "Urban young adults": (0.95, 0.90, 0.90, 0.85),
    "Urban women 40+":    (0.80, 0.55, 0.85, 0.70),
    "Rural hill farmers": (0.70, 0.40, 0.65, 0.60),
    "Elderly rural":      (0.35, 0.15, 0.60, 0.50),
    "Mountain remote":    (0.45, 0.35, 0.40, 0.55),
}
print("%-20s %6s %6s %6s %6s %9s" % ("group", "acc", "skill", "afford", "trust", "reach"))
best = None
for g, v in groups.items():
    r = 1.0
    for x in v:
        r *= x
    best = max(best or 0, r)
    print("%-20s %6.2f %6.2f %6.2f %6.2f %8.1f%%" % ((g,) + v + (100 * r,)))
print("\ndivide ratio best/worst: %.1f" % (best / min(1.0 * a * b * c * d for a, b, c, d in groups.values())))
# Which single hurdle lifts the 'Rural hill farmers' reach most if raised by 0.10?
a, b, c, d = groups["Rural hill farmers"]
base = a * b * c * d
for name, k in zip(("access", "skill", "afford", "trust"), range(4)):
    v = list((a, b, c, d)); v[k] = min(1, v[k] + 0.10)
    p = v[0] * v[1] * v[2] * v[3]
    print("raise %-7s by 0.10 -> reach %.1f%% (+%.1f points)" % (name, 100 * p, 100 * (p - base)))
```
```output
group                   acc  skill afford  trust     reach
Urban young adults     0.95   0.90   0.90   0.85     65.4%
Urban women 40+        0.80   0.55   0.85   0.70     26.2%
Rural hill farmers     0.70   0.40   0.65   0.60     10.9%
Elderly rural          0.35   0.15   0.60   0.50      1.6%
Mountain remote        0.45   0.35   0.40   0.55      3.5%

divide ratio best/worst: 41.5
raise access  by 0.10 -> reach 12.5% (+1.6 points)
raise skill   by 0.10 -> reach 13.6% (+2.7 points)
raise afford  by 0.10 -> reach 12.6% (+1.7 points)
raise trust   by 0.10 -> reach 12.7% (+1.8 points)
```
The last lines carry the policy lesson: improve the **weakest** factor first. For rural hill farmers the skill factor (0.40) is the bottleneck, so training and assisted-service counters (a Common Service Centre, a ward-office help desk) beat another round of mobile-app features.

::: caution Exam trap
Do not write that the divide is "only a lack of internet". The question usually wants access, skills and usage, plus at least two causes (income, geography, gender, age, language, disability) and two remedies (community access points, local-language services, training, low-bandwidth design).
:::

## 1.4 Evolution, scope and content of e-governance

### 1.4.1 Evolution

| Period | Stage | What the government did | Example |
|---|---|---|---|
| 1960s to 1980s | Computerisation | Mainframes for census, payroll, accounts inside departments | Census tabulation |
| 1980s to 1990s | Networking and office automation | PCs, LANs, first national networks | NICNET in India (1987) |
| 1995 to 2005 | Web presence | Departments publish forms and notices on websites | Ministry websites |
| 2000 to 2010 | Interaction and transaction | Forms download, status check, online payment | Online tax filing, passport forms |
| 2010 to 2020 | Integration and mobile | One login, shared data between agencies, apps | Aadhaar, UPI, Nagarik App |
| 2020 onward | Data-driven and AI-assisted | Analytics, chatbots, automated decisions with safeguards | Open data, e-ID wallets |

The sequence matters because each stage depends on the earlier one. A transaction portal fails if the back-office registers are still on paper; a chatbot is of no use if the website has no reliable answers.

### 1.4.2 Scope and content

Scope means *how far* e-governance reaches; content means *what it contains*. Both can be arranged as four layers:

- **e-Administration**: improving internal processes (file movement, payroll, records, intranet).
- **e-Services**: connecting citizens and businesses to services (certificates, licences, payments).
- **e-Society**: building relationships among government, citizens, business and civil society (e-participation, consultation, open data).
- **e-Democracy**: the use of ICT in electoral and legislative processes (voter registers, online petitions, live broadcast of the parliament).

Content includes **information** (laws, notices, budgets), **transactions** (applications, payments), **communication** (email, grievance systems, SMS alerts) and **participation** (polls, comments, social media).

## 1.5 Present global trends of growth in e-governance

### 1.5.1 Measuring it: the UN E-Government Development Index

The UN E-Government Survey, published every two years, ranks 193 member states on the **EGDI**, the simple average of three normalised indices:

$$\text{EGDI}=\frac{\text{OSI}+\text{TII}+\text{HCI}}{3}$$

- **OSI** (Online Service Index): the quality and scope of national online services, assessed by researchers.
- **TII** (Telecommunication Infrastructure Index): internet users, mobile and fixed broadband subscriptions per head.
- **HCI** (Human Capital Index): adult literacy, school enrolment and expected years of schooling.

Each runs from 0 to 1. In the 2024 survey Nepal had OSI 0.4481, TII 0.7653 and HCI 0.5210, which gives EGDI 0.5781 and rank 119 of 193, placing it in the "High" EGDI group (H1 class). Denmark (0.9847), Estonia (0.9727) and Singapore (0.9691) led the table. The code checks the arithmetic and shows where Nepal would gain most.

```python
osi, tii, hci = 0.4481, 0.7653, 0.5210            # Nepal, UN E-Government Survey 2024 (as reported)
egdi = (osi + tii + hci) / 3
print("EGDI (Nepal 2024) = %.4f" % egdi)

# Reported EGDI values of Nepal in recent surveys (as quoted in Nepali journal reviews)
series = {2014: 0.2344, 2018: 0.4748, 2020: 0.4699, 2022: 0.5117, 2024: 0.5781}
years = sorted(series)
for a, b in zip(years, years[1:]):
    print("%d -> %d : %+.4f  (%.1f%% change)" % (a, b, series[b] - series[a], 100 * (series[b] / series[a] - 1)))

# What if one component improves by 0.10 (the others unchanged)?
for name, v in (("OSI", osi), ("TII", tii), ("HCI", hci)):
    up = min(1.0, v + 0.10)
    new = (egdi * 3 - v + up) / 3
    print("+0.10 on %s -> EGDI %.4f (+%.4f)" % (name, new, new - egdi))
gap = {"OSI": 1 - osi, "TII": 1 - tii, "HCI": 1 - hci}
print("largest gap to 1.0:", max(gap, key=gap.get), "=", round(max(gap.values()), 4))
```
```output
EGDI (Nepal 2024) = 0.5781
2014 -> 2018 : +0.2404  (102.6% change)
2018 -> 2020 : -0.0049  (-1.0% change)
2020 -> 2022 : +0.0418  (8.9% change)
2022 -> 2024 : +0.0664  (13.0% change)
+0.10 on OSI -> EGDI 0.6115 (+0.0333)
+0.10 on TII -> EGDI 0.6115 (+0.0333)
+0.10 on HCI -> EGDI 0.6115 (+0.0333)
largest gap to 1.0: OSI = 0.5519
```
An equal rise in any component adds 0.0333 to the EGDI, so the useful question is which one is cheapest to raise. For Nepal the largest gap lies in the Online Service Index, which a government controls directly through the services it builds, unlike telecom coverage or schooling, which take years.

```svgfig label="1.2" caption="Nepal's three EGDI components in the UN E-Government Survey 2024 (as reported). Telecommunication is the strongest; the online services index is the weakest and the one that policy can move fastest."
f = Fig(680, 190)
hbars(f, [("Online services (OSI)", 0.4481), ("Telecom infrastructure (TII)", 0.7653), ("Human capital (HCI)", 0.5210), ("EGDI (average)", 0.5781)], x0=190, y0=20, bw=400, vmax=1.0, fmt="%.4f", colors=[AMBER, TEAL, NAVY, RED])
```

## 1.6 E-governance applications

An application is best described by four facts: **who** uses it, **what** service it gives, **which back-end register** it depends on, and **what changed** compared with the paper process.

| Sector | Typical applications | Back-end register or system |
|---|---|---|
| Civil registration and identity | Birth, marriage, citizenship, national ID, voter list | Civil register, national ID database |
| Taxation and revenue | PAN, VAT and income-tax returns, customs declaration | Taxpayer register, customs system |
| Land and property | Land records, mutation, parcel maps, encumbrance check | Land register and cadastre |
| Transport | Driving licence, vehicle registration, tax payment | Vehicle and licence register |
| Procurement | Online tender notice, bid submission, award notice | e-procurement portal |
| Health | Patient records, reporting of diseases, vaccination registry | Health information system (HMIS, DHIS2) |
| Education | Result publication, scholarship, school census, e-library | Education management information system |
| Agriculture | Market prices, advisory, subsidy, farmer registry | Agricultural statistics and farmer lists |
| Justice and police | Case tracking, e-filing, police clearance, crime records | Court and police databases |
| Local government | Ward services, recommendation letters, property tax, grievance | Municipal databases |
| Social protection | Pension and allowance payments, social security fund | Beneficiary register |

A single service often stands on several registers. Issuing a police clearance online needs identity (citizenship), a payment gateway, a police record check and a digital signature or QR code for verification. Each missing link sends the citizen back to the counter.

## 1.7 E-governance initiatives in Nepal

### 1.7.1 Timeline

```svgfig label="1.3" caption="Milestones of e-governance in Nepal, from the first IT policy to the Nagarik App and the UN index rank of 2024."
f = Fig(680, 250)
f.line(40, 120, 640, 120, color=SLATE, sw=2.4)
pts = [(60, "2000", "IT Policy", NAVY), (150, "2006", "e-Government\nMaster Plan", TEAL), (240, "2007", "RTI Act", AMBER), (330, "2015", "ICT Policy;\nConstitution", NAVY),
       (420, "2019", "Digital Nepal\nFramework", TEAL), (510, "2021", "Nagarik App\n(full launch)", RED), (600, "2024", "EGDI rank 119", AMBER)]
for i, (x, yr, lab, col) in enumerate(pts):
    f.circle(x, 120, 7, fill=SOFT, stroke=col, sw=2)
    up = i % 2 == 0
    f.text(x, 98 if up else 150, yr, size=11, color=col, bold=True)
    f.text(x, 66 if up else 182, lab, size=9.5, color=SLATE)
```

### 1.7.2 The main steps

- **IT Policy 2000** (2057 BS) set the first national vision for ICT; it was revised in 2004 and again as the **ICT Policy 2015**, which names "Digital Nepal" and aims at e-government services at every level.
- **E-Government Master Plan (eGMP), 2006**: prepared with Korean assistance (the Korea IT Industry Promotion Agency), it set the vision and strategy, proposed a portfolio of projects (a Government Integrated Data Centre, a national network, citizen service projects) and a road map. Implementation was slower than the plan; an updated master plan followed in the mid-2010s.
- **Electronic Transactions Act, 2063 BS** (commonly dated 2006; some sources say 2008) gives legal force to electronic records and signatures and punishes computer offences; the **Right to Information Act, 2064** (2007) obliges public bodies to disclose information, which e-governance makes cheap.
- **Constitution of Nepal 2015** guarantees the right to information and sets up the three tiers of government. Federalism raised the demand for G2G integration: 753 local governments now run their own services and need shared systems.
- **Digital Nepal Framework (2019)**, summarised as **1 nation, 8 sectors, 80 initiatives**: the sectors are digital foundation, agriculture, health, education, energy, tourism, finance and urban infrastructure. It identifies cross-cutting enablers (policy, skills, trust).
- **Services in operation**: online PAN and tax filing, customs and the National Single Window, online public procurement, online passport and driving-licence applications, civil registration systems, **Hello Sarkar** (the Prime Minister's office grievance line), and the **Nagarik App** (Unit 5).
- **Weak points** repeatedly named in studies: duplicated systems in separate ministries, thin back-end integration, limited rural connectivity and digital skills, uneven local capacity, and offices that still ask for paper even when a digital record exists.

::: example Quick calculation for the exam
Nepal's EGDI rank moved from 165 (2014) to 119 (2024): 46 places in ten years. In the same period the index value rose from 0.2344 to 0.5781, a rise of 0.3437, or about 147 per cent. Good answers add that rank is relative (other countries also improved) while the index value is absolute progress.
:::

## 1.8 Summary and exercises

**Summary.** Governance is how a society decides and enforces; e-governance uses ICT to make that process simpler, more open and more accountable (SMART). It works through G2C, G2B, G2G and G2E interactions on top of people, process, data, technology and law. Benefits show up as saved cost and time for citizens and as transparency; the main issues are infrastructure, law, process, skills, interoperability, security, sustainability and the digital divide of access, skills and usage. E-governance evolved from computerisation to networking, web presence, transaction, integration and data-driven services. The EGDI averages OSI, TII and HCI; Nepal stood at 0.5781 (rank 119) in 2024. Nepal's path runs through the IT Policy 2000, eGMP 2006, ETA and RTI, the ICT Policy 2015, the Digital Nepal Framework 2019 and the Nagarik App.

1. Define governance, government, e-government and e-governance. What does SMART stand for?
2. Explain G2C, G2B, G2G and G2E with one Nepali example of each.
3. List five objectives of e-governance and explain two with examples.
4. In the cost model of 1.2.2, the citizen makes four visits instead of three and the fee is NPR 150. Recompute the manual cost.
5. State five issues in e-governance applications. Which are legal and which are about people?
6. What is Heeks's design-reality gap? Name four of the seven ITPOSMO dimensions.
7. Define the digital divide. Distinguish the access, skills and usage divides and suggest two remedies.
8. A group has access 0.9, skill 0.5, affordability 0.8 and trust 0.7. Compute the effective reach and say which factor to raise first.
9. Trace the evolution of e-governance in six stages, with an example for each.
10. Differentiate e-administration, e-services, e-society and e-democracy.
11. Write the EGDI formula. Compute it for OSI 0.30, TII 0.60 and HCI 0.45.
12. Nepal's TII is 0.7653 and OSI 0.4481. If OSI rose to 0.6481, what would EGDI become (HCI 0.5210)?
13. Describe five e-governance applications by sector with the back-end register each depends on.
14. Describe the Digital Nepal Framework. What does 1:8:80 mean?
15. Discuss the e-governance initiatives of Nepal and the problems they face.

**Answers to the numerical items.** (4) Manual cost = 4 x (60 + 4 x 125) + 6 x 5 + 150 = 4 x 560 + 30 + 150 = **NPR 2,420** (the original was 3 x 560 + 30 + 100 = 1,810; the online cost is 110). (8) Reach = 0.9 x 0.5 x 0.8 x 0.7 = **0.252, or 25.2 per cent**; raise **skill** (0.5), the weakest factor. (11) EGDI = (0.30 + 0.60 + 0.45)/3 = 1.35/3 = **0.45**. (12) The sum rises by 0.20, so EGDI = 0.5781 + 0.20/3 = 0.5781 + 0.0667 = **0.6448**.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is e-governance? Explain its objectives.**

E-governance is the application of ICT to the processes of government and governance so as to deliver services, run the administration and involve citizens in a way that is simple, moral, accountable, responsive and transparent (SMART). It covers G2C, G2B, G2G and G2E interactions. Objectives: (1) better and faster service delivery to citizens and businesses; (2) transparency, because decisions and records are visible; (3) accountability through audit trails; (4) efficiency and lower cost through shared data and paperless work; (5) inclusion, by reaching remote people; (6) participation through consultation and feedback; (7) evidence-based policy using data. A good answer closes with one measured example (a saving of travel and time to the citizen).

**Q2 (5 marks). Explain the digital divide and how to reduce it.**

The digital divide is the gap between people who can use ICT effectively and those who cannot. Layers: access (devices, network, power), skills (literacy, digital skills, language) and usage or outcome (unequal benefit). It follows income, geography, gender, age, language and disability. Reach is the product of access, skill, affordability and trust, so a service with high coverage can still serve few. Remedies: community access points and ward help desks, local-language and low-bandwidth services, digital literacy training, subsidised data and devices, assisted service by trained operators, and keeping an offline option while the divide persists.

**Q3 (10 marks). Describe the e-governance initiatives of Nepal and discuss the problems.**

Cover the timeline: IT Policy 2000 (revised 2004), e-Government Master Plan 2006 prepared with Korean support, Electronic Transactions Act and RTI Act 2007, the Constitution of 2015 and the ICT Policy 2015, the Digital Nepal Framework 2019 (1 nation, 8 sectors, 80 initiatives), and services such as online PAN and tax, customs single window, e-procurement, Hello Sarkar and the Nagarik App. Give the index evidence: EGDI 0.5781, rank 119 in 2024, up from rank 165 in 2014; telecom 0.7653 is stronger than online services 0.4481. Problems: weak integration among agencies, duplicated systems, poor rural connectivity, low digital skills, limited capacity in local governments, resistance to change, offices that still demand paper, security and privacy gaps, and weak sustainability after donor projects. Conclude with remedies: shared platforms and standards, national ID as a common key, training, and legal recognition of digital records in practice.
