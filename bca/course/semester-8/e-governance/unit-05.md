---
subject: E-Governance
grade: BCA Semester 8 (Elective III)
unit: 5
title: Case Studies
hours: 16
area: BCA 453 · E-Governance · Unit 5
---

Models and checklists become real when you read what a district office or a land registry actually did. This unit covers the case studies of the TU outline in its order: **Nepal** (the e-Government Master Plan, e-governance in local government, the Nagarik App), **India** (fifteen projects from NICNET to the information services of the National Informatics Centre), and **other countries** (the USA, China, Brazil and Sri Lanka). The Indian cases follow the textbook by C. S. R. Prabhu, an official of the National Informatics Centre (NIC) who worked on many of them.

::: caution How to read the numbers in this unit
The cases were described in textbooks and reports at the time the projects were new; figures (offices covered, records computerised, fees) are those published then and some systems have since been replaced by national platforms. In an examination, give the **idea and the structure** of the case, and quote one or two figures with the phrase "as reported". Where a figure here is uncertain it is marked *check the current text*.
:::

::: key What this unit gives you
- A five-question frame for analysing any e-governance case: problem, design, results, lessons, transferability.
- Nepal: eGMP 2006, local-government digitalisation after federalism, and the Nagarik App, with a working toy model of its identity check and QR verification.
- India: the fifteen outline cases, each with what the project did, how, the benefit and the lesson, plus arithmetic for CARD and Bhoomi.
- USA, China, Brazil and Sri Lanka, and a comparison table of lessons across all cases.
:::

## 5.1 How to analyse an e-governance case

Use the same five questions for every case; an examiner can award marks for each.

1. **Problem.** What was wrong before? (delay, cost, corruption, access, poor data). Quote a number if there is one.
2. **Design.** What was built? Which **register or data** sits at its centre, which **technology**, which **delivery channel** (office counter, kiosk, web, mobile), and which **process change** came with it?
3. **Results.** What changed for the citizen and for the office? Time, cost, errors, income, trust.
4. **Lessons.** Why did it work, or what limited it? (law, political support, staff buy-in, standards, sustainability).
5. **Transferability.** Could it be applied in Nepal? What would need to change (law, language, connectivity, scale)?

Success patterns repeat across the cases of this unit: a **focused problem** (a single document or counter), a **powerful champion** (a collector, a minister), **legal backing** (the electronic record declared valid and the manual one withdrawn), **back-office computerisation first**, a **fee or a saving** that sustains operation, and **staff involvement**. Failure patterns repeat too: pilots without evaluation, duplicated systems, and services that stop at the portal.

## 5.2 Nepal

### 5.2.1 The e-Government Master Plan of Nepal

**Background.** Until the early 2000s ICT in Nepal's government meant scattered computers; each ministry had its own information system and nothing could talk to anything else. After the IT Policy of 2000 the government, with Korean assistance (the Korea IT Industry Promotion Agency), prepared the **e-Government Master Plan (eGMP)**, finalised in November 2006.

**Content.** The plan stated a vision of transparent, ICT-enabled services that improve livelihoods; analysed the readiness of infrastructure, laws, institutions and people; and proposed a portfolio of projects (the plan lists dozens, from which a few were marked as priority) and a roadmap with the institutions that would carry it out. Typical elements were a government network and **integrated data centre**, a national portal, a common ID and registry foundation, and citizen services such as online registration and tax. The plan also recommended the restructuring of the legal framework, which is how the Electronic Transactions Act came to be linked with it.

**Result and lessons.** Parts were built (the government data centre, a government network and several e-services) but implementation was slower than planned; evaluations repeatedly name weak ownership across ministries, funding gaps, political change and limited capacity. An update of the master plan was prepared in the mid-2010s and the **Digital Nepal Framework (2019)** later set the current direction. For the exam the lesson is that **a plan without an owner and a budget line is a report**, and that a master plan must be updated as the country changes (the 2015 constitution created three tiers of government and the plan had to follow).

### 5.2.2 E-governance in the local governments of Nepal

**Background.** Since 2017 Nepal has **753 local levels** (6 metropolitan cities, 11 sub-metropolitan cities, 276 municipalities and 460 rural municipalities) that deliver the services closest to people: civil registration, recommendation letters, property and business tax, social-security allowances, water and local roads. The Local Government Operation Act, 2074, gives them wide powers and their own records.

**What exists.** Websites and notice boards for each local level; software for civil registration (births, deaths, marriages, migration) and for allowance distribution; revenue and property-tax software; accounts through the national treasury applications (SuTRA for the sub-national treasury); complaints through ward complaint desks and the national Hello Sarkar line; and the e-procurement portal for bidding. Many ward offices act as digital service points for citizens who cannot use online services themselves.

**Problems named by studies.** Uneven capacity (a metropolitan city and a remote rural municipality have very different budgets and staff); intermittent connectivity and electricity in remote wards; few trained IT staff and frequent transfers; systems that do not exchange data (each service has its own login and records); low digital skills among citizens; and legal rules that still ask for paper. Surveys of provincial local levels have found that many remain only partly ready.

**Lessons and direction.** Shared national platforms (a common civil register, a common revenue module) avoid 753 separate purchases; municipalities of similar size can share an IT team; ward-level facilitators bridge the skills divide; and a national ID gives local systems a common key. This is the same readiness logic as Unit 3, applied to a federation.

### 5.2.3 The Nagarik App

**What it is.** The **Nagarik App** is the Government of Nepal's mobile (and web) platform for citizens' services, built under the Digital Nepal Framework by the Ministry of Communication and Information Technology with the National Information Technology Centre (NITC) hosting and supporting it. A **beta version was launched on 15 January 2021** (Magh 2, 2077) by the then communications minister, covering services of about 40 of 64 identified government bodies, and a fuller version was released in the following months; the app later received an international digital-government award.

**Design.** The digital identity of a citizen is built on **existing registers**: citizenship records of the Ministry of Home Affairs (reported as about 21.5 million citizens) and fingerprints and photographs held by the Election Commission (about 15.5 million). To register, the citizen supplies a **mobile number linked to her citizenship number** and passes verification (a one-time code to the registered phone and, for fuller access, identity checks); thereafter the app can request documents and services from the agencies' own systems through a gateway, with the citizen's consent.

**Services.** Document wallet and verification (citizenship, PAN, voter card, driving licence, passport details, academic certificates, social security and provident-fund records), police clearance report, PAN registration and tax information, local-government information, Citizen Investment Trust, health insurance, and a growing list of payments and applications.

```svgfig label="5.1" caption="Simplified architecture of the Nagarik App: the citizen authenticates, the gateway at NITC verifies identity against national registers and calls the service systems of the agencies; documents carry a QR code that any office can verify online."
f = Fig(680, 300)
f.box(15, 100, 110, 80, "Citizen\nphone app\nand web", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(165, 90, 130, 100, "Authentication\nphone number +\ncitizenship no.\n+ OTP, consent", fill=SAND, stroke=AMBER, size=10)
f.box(335, 90, 130, 100, "Service gateway\n(NITC, government\ndata centre)", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(505, 15, 160, 50, "Home Affairs: citizenship", fill=SOFT, stroke=NAVY, size=9.5)
f.box(505, 75, 160, 50, "Election Commission:\nvoter data, biometrics", fill=SOFT, stroke=NAVY, size=9.5)
f.box(505, 135, 160, 50, "Inland Revenue: PAN, tax", fill=SOFT, stroke=NAVY, size=9.5)
f.box(505, 195, 160, 50, "Police, Transport,\nPassport, SSF, CIT", fill=SOFT, stroke=NAVY, size=9.5)
f.arrow([(125, 140), (165, 140)], color=TEAL, both=True)
f.arrow([(295, 140), (335, 140)], color=AMBER, both=True)
for y in (40, 100, 160, 220):
    f.arrow([(465, 140), (505, y)], color=NAVY, both=True)
f.box(165, 235, 300, 45, "Verified output: PDF with dynamic QR code; the office scans it and checks the record online", fill=ROSE, stroke=RED, size=9.5)
f.arrow([(400, 190), (340, 235)], color=RED)
```

**Results and limits.** A single sign-in replaces many counters, and QR-verified documents (such as the police clearance report) are harder to forge than a rubber stamp. Reports in 2026 nevertheless describe a gap between capability and adoption: many offices, banks and agencies still demand the physical document, because rules, habits or distrust require it; the app's own officials say it is mainly for digital verification and cannot yet replace the printed citizenship card in every setting. That is the "law exists, practice lags" problem of 3.1.3 in a real service.

The toy model below shows the two technical ideas behind such a service with invented data: **registration by matching a phone number to a citizenship record plus a one-time code**, and **tamper-evident documents with a signed QR payload** (an HMAC; the real system uses its own keys and formats).

```python
import hmac, hashlib, random
registry = {"27-01-71-00123": {"name": "A. Sharma", "phone": "9841000001"},     # invented citizens
            "12-02-68-00456": {"name": "B. Gurung", "phone": "9851000002"}}
rnd = random.Random(5)
def register(citizenship_no, phone):
    rec = registry.get(citizenship_no)
    if rec is None or rec["phone"] != phone:
        return None, "identity not matched"
    return "%06d" % rnd.randrange(10**6), "OTP sent to %s" % phone
otp, msg = register("27-01-71-00123", "9841000001"); print("valid user      :", msg)
print("wrong phone     :", register("27-01-71-00123", "9800000000")[1])
print("unknown citizen :", register("00-00-00-00000", "9841000001")[1])
KEY = b"agency-signing-key"                                  # held by the issuing agency only
def issue(doc_id, holder, valid_to):
    payload = "%s|%s|%s" % (doc_id, holder, valid_to)
    tag = hmac.new(KEY, payload.encode(), hashlib.sha256).hexdigest()[:16]
    return payload + "|" + tag
def verify(qr):
    payload, tag = qr.rsplit("|", 1)
    good = hmac.new(KEY, payload.encode(), hashlib.sha256).hexdigest()[:16]
    return hmac.compare_digest(tag, good)
qr = issue("PCR-2026-0001", "A. Sharma", "2026-12-31")
print("QR payload      :", qr)
print("verify original :", verify(qr))
print("verify tampered :", verify(qr.replace("A. Sharma", "C. Thapa")))
```
```output
valid user      : OTP sent to 9841000001
wrong phone     : identity not matched
unknown citizen : identity not matched
QR payload      : PCR-2026-0001|A. Sharma|2026-12-31|b84ee7a200e991e2
verify original : True
verify tampered : False
```
The second half is the point: any change to a field, even one letter, breaks the tag, so a clerk can trust a printed certificate by **checking online** instead of looking at a stamp. The first half shows why registration needs a **linked phone record**: the match, not the password, is the identity proof.

## 5.3 India

India began early because it had a central technical agency, the **National Informatics Centre (NIC)**, established in 1976 under the Planning Commission and present in every state and district. Most of the cases below were built by NIC units with state governments. The Government of India later grouped them under the **National e-Governance Plan (NeGP, 2006)**, with mission-mode projects for land records, registration, courts, treasuries, municipalities and others, and then under **Digital India (2015)**. The cases below are given in the order of the TU outline.

### 5.3.1 NICNET: the role of nationwide networking in e-governance

**Problem.** In the 1980s district administrations and state capitals had no data link to the centre; statistics, plans and parliamentary questions moved on paper over weeks.

**What was done.** NIC built **NICNET**, a satellite-based nationwide network launched in 1987 (VSAT and later terrestrial links) that connected the capital with every state capital and then every district headquarters. It carried email, file transfer, database access (the District Information System, DISNIC), electronic data interchange, video conferencing and later web hosting for government sites. NIC computer centres at district level were staffed by NIC officers who built applications for the collectors.

**Lesson.** Networking came **before** applications: a shared, government-owned backbone and a trained technical cadre in each district made all the later cases possible. For Nepal the comparison is the government network and the National Information Technology Centre.

### 5.3.2 Collectorate 2000

**Problem.** The district **Collector** is the head of the district administration (land revenue, arms licences, civil supplies, relief, welfare pensions, grievances). The Collectorate's files moved slowly between sections, and the Collector could not easily see the position of any file or scheme.

**What was done.** NIC computerised the sections of the Collectorate as one integrated package: file movement tracking, land revenue demand and collection, arms licences, welfare payments, public grievances and statistics, on a local network and linked to the state head office. The textbook presents it as a model of **office automation at district level** that was replicated in other districts. *Check the textbook for the module list and the districts covered.*

**Lesson.** Computerising a whole office around the head's needs (monitoring of files and schemes), not a single task, gains the head's support.

### 5.3.3 CARD: Computer-aided Administration of Registration Department

**Problem.** Property registration in Andhra Pradesh took days or weeks. Documents were hand-copied into bound volumes; searching for an encumbrance certificate meant browsing registers; middlemen and delays were common; documents could be tampered with.

**What was done.** Launched in 1998 at 387 sub-registrar offices (SROs), CARD put all registration on computers: the deed is **typed and printed at the counter, scanned, and stored in a database**; parties and witnesses are photographed and sign on the spot; a computer value for stamp duty is calculated from the **market value** table; certified copies and encumbrance certificates are produced by search of the database. Registration of a standard deed was reported to take about an hour against days. Six months after launch, about 80 per cent of registrations were done on the system, and both the Registration Department and the citizen gained. The department also collected more stamp-duty revenue because valuations were applied uniformly.

**Lesson.** CARD is the standard example of **re-engineering plus computerisation**: the process (sale deed, valuation, signing, copy) was redesigned around a single counter; the legal change (the electronic copy has the same validity) and a revenue gain meant the department wanted it.

### 5.3.4 Smart Nagarpalika: computerisation of urban local bodies

**Problem.** Municipalities in Andhra Pradesh issued birth and death certificates, collected property tax, granted trade licences and building permits, ran water supply and handled grievances manually, with long queues and poor records.

**What was done.** **Smart Nagarpalika** (a NIC product, *nagarpalika* = municipality) is an integrated package of municipal modules: birth and death registration, property tax assessment and collection, water charges, trade licences, building plan approvals, accounts, grievance tracking and management reports for the commissioner. Citizens receive services at a computerised counter and, later, over the web.

**Lesson.** Local bodies cannot each write software, so **one package, many municipalities** is the economical route. This is the same argument as the shared platforms for Nepal's 753 local levels in 5.2.2.

### 5.3.5 National Reservoir Level and Capacity Monitoring System

**Problem.** Water-resource planners, drought and flood managers and the public need a regular, reliable picture of how much water is stored in the major reservoirs of the country. Reports came by letter or fax from many agencies.

**What was done.** NIC and the water-resource authorities built a system in which each reservoir reports its **level and live storage** (daily or weekly) from the field into one national database; the data are compared with capacity, last year's levels and normal levels, and published as tables and maps for planners and the public. *Check the current text for the number of reservoirs and the agencies.*

**Lesson.** A **monitoring** (G2G) application: standard formats, clear data owners and a fixed reporting schedule turn many local figures into national information. It is a ready example of a national data warehouse (Unit 4).

### 5.3.6 Computerisation in the Andhra Pradesh State Trading Corporation (APSTC)

**Problem.** A state trading corporation buys and sells goods in bulk (fertiliser, commodities, imports). Stock, purchase orders, bills, payments and the accounts were kept by hand, so stock-outs, delays in payment and errors were frequent.

**What was done.** NIC computerised the corporation's trading operations: purchase and sales orders, stock position, invoicing, payment and the accounts, with management reports. Its value was **business management**, not citizen service.

**Lesson.** E-governance includes G2G and government-owned business: even a trading company is an e-governance problem when it belongs to the state, and the gain is control of stock and cash.

### 5.3.7 Ekal Seva Kendra

**Problem.** A citizen who needs several department services (certificates, licences, bill payment, applications) must visit a different counter at a different place for each.

**What was done.** The **Ekal Seva Kendra** (*ekal* = single) brings several services under one roof and one queue, with a computerised front office that receives applications and payments for many departments and returns the results at the same counter. *Check the textbook for the state and the list of services of this centre.*

**Lesson.** The **single-window** idea: the citizen sees one government. It is the Indian counterpart of Brazil's Poupatempo (5.4.3) and, in Nepal, of the idea of the ward office as a service centre.

### 5.3.8 Sachivalaya Vahini: e-governance in the Secretariat

**Problem.** The **Secretariat** is where policy is made and files travel between ministers, secretaries and departments. Files were slow and lost, and nobody could say where a file was or who was holding it up.

**What was done.** The Andhra Pradesh Secretariat built an intranet-based system (*vahini* = carrier) that links departments and the heads of departments, with **file tracking, electronic movement of notes, e-mail, and a database of government orders**, a messaging service and video conferencing with districts. Each file's position and delay can be seen by the supervising officer.

**Lesson.** Making delay **visible** changes behaviour: a tracked file moves faster, and e-governance can start inside government before it faces the citizen.

The two figures reported for CARD (an hour against days, and 80 per cent of deeds in six months) can be used for a short quantitative case. The program models the **time saved by the citizen** from CARD and the **fee recovery** of a counter service, with illustrative inputs. It is labelled a model, not a result.

```python
# CARD-style registration: time and cost to the citizen, before and after (illustrative inputs)
before_days, after_hours = 5, 1                 # reported order of magnitude: days versus about one hour
workday_hours = 8
wage_per_day = 400                              # rupees, an average earner (illustrative)
agent_fee_before, agent_fee_after = 800, 0      # middleman cost avoided (illustrative)
time_cost_before = before_days * wage_per_day
time_cost_after = after_hours / workday_hours * wage_per_day
saving = (time_cost_before + agent_fee_before) - (time_cost_after + agent_fee_after)
print("cost to a citizen before : Rs %.0f" % (time_cost_before + agent_fee_before))
print("cost to a citizen after  : Rs %.0f" % (time_cost_after + agent_fee_after))
print("saving per deed          : Rs %.0f (%.0f%%)" % (saving, 100 * saving / (time_cost_before + agent_fee_before)))
deeds = 387 * 20 * 300                          # 387 offices x 20 deeds a day x 300 days (illustrative)
print("deeds a year             : %d" % deeds)
print("citizen saving in a year : Rs %.0f crore" % (saving * deeds / 1e7))
```
```output
cost to a citizen before : Rs 2800
cost to a citizen after  : Rs 50
saving per deed          : Rs 2750 (98%)
deeds a year             : 2322000
citizen saving in a year : Rs 639 crore
```
The scale (about Rs 640 crore of citizen time a year in this model, from the invented 2.3 million deeds) is why registration, land and tax services are the usual first choices: **high volume, document-based, a single register behind them**.

### 5.3.9 Bhoomi: computerised land records in Karnataka

**Problem.** In Karnataka land records were kept by about 9,000 village accountants, each for a cluster of villages. A farmer needed the **Record of Rights, Tenancy and Crops (RTC)** to get a bank loan, prove ownership or sell; getting it meant finding the accountant, waiting, and often paying an unofficial amount. Records could be altered at the village level, and disputes were frequent.

**What was done.** The Revenue Department, with NIC Bangalore, computerised about **20 million records of about 6.7 million farmers** and set up **Bhoomi kiosks** in about 177 taluk offices. A farmer gives the owner's name or survey number and receives a printed, signed RTC in minutes for a fee of **Rs 15**; a second screen faces the farmer so that the transaction is seen. Operators log in with **biometric authentication**; the audit trail records who changed what. Mutation (change of ownership) requests are tracked, with notice to the parties and a time limit. The decisive rule was that **manually written RTCs were declared invalid taluk by taluk** as the computerised system started, so the old and new systems could not run in parallel.

**Results (as reported).** Delivery of RTCs in minutes; bank lending on RTCs became easier; surveys at the time found that unofficial payments, common under the manual system, became rare at the kiosks, though many users did not receive a receipt for the fee; the user fee roughly covered the running cost, so the project sustained itself.

**Lesson.** Open, signed, auditable records reduce the power of the middle layer; the **legal switch** (manual copies no longer valid) and political support were as important as the software.

The cost-recovery logic of the fee can be worked as a break-even calculation. The published estimate was about Rs 13 to produce one RTC at 2 million RTCs a year, of which Rs 2 was running cost (paper, cartridges, power); the rest is the spread of the fixed cost (hardware over 5 years).

```python
fee, variable = 15.0, 2.0
volume_ref, cost_ref = 2_000_000, 13.0
fixed_total = (cost_ref - variable) * volume_ref          # yearly fixed cost implied by the estimate
print("implied yearly fixed cost: Rs %.0f million" % (fixed_total / 1e6))
breakeven = fixed_total / (fee - variable)
print("break-even volume at fee Rs %.0f: %.2f million RTCs a year" % (fee, breakeven / 1e6))
for v in (1_000_000, 1_700_000, 2_000_000, 3_000_000):
    unit = fixed_total / v + variable
    print("volume %.1f million -> cost per RTC Rs %5.2f, surplus per RTC Rs %5.2f, total surplus Rs %6.2f million"
          % (v / 1e6, unit, fee - unit, v * (fee - unit) / 1e6))
```
```output
implied yearly fixed cost: Rs 22 million
break-even volume at fee Rs 15: 1.69 million RTCs a year
volume 1.0 million -> cost per RTC Rs 24.00, surplus per RTC Rs -9.00, total surplus Rs  -9.00 million
volume 1.7 million -> cost per RTC Rs 14.94, surplus per RTC Rs  0.06, total surplus Rs   0.10 million
volume 2.0 million -> cost per RTC Rs 13.00, surplus per RTC Rs  2.00, total surplus Rs   4.00 million
volume 3.0 million -> cost per RTC Rs  9.33, surplus per RTC Rs  5.67, total surplus Rs  17.00 million
```
Below about 1.7 million RTCs a year the kiosks would not recover their cost: **the self-financing claim depends on volume**, which is why demand (and a legal requirement to use the system) matter.

### 5.3.10 IT in the Indian judiciary

**Problem.** Courts carry millions of pending cases; cause lists, case status and orders were on paper; lawyers and litigants went to the court to learn the next date.

**What was done.** The **e-Courts mission mode project** (from 2007 under the national plan) computerised district and subordinate courts with a **Case Information System** (developed by NIC) that records filing, listing, orders and judgments; case status, cause lists and judgments are published through the e-Courts services and a **National Judicial Data Grid** that shows pending and disposed cases, by court and by age of case, in near real time. Later phases added e-filing, e-payment of court fees, video conferencing for hearings and digitisation of records.

**Lesson.** Digital data make **pendency visible**, which supports management of the courts (critical flow and comparative models of Unit 2), but judicial independence needs the system to inform, not to direct, decisions.

### 5.3.11 E-Khazana: computerisation of the government treasury, Andhra Pradesh

**Problem.** The **treasury** receives government revenue, pays salaries, pensions and bills, and compiles the accounts. Paper vouchers, manual cash books and reconciliation with banks made payments slow and accounts late; errors and fraud were hard to detect.

**What was done.** E-Khazana (*khazana* = treasury) put the treasury's processes online: **bills from drawing officers are submitted and validated against budget** in the system, payments are authorised electronically and made through the banking network (direct credit to employees and suppliers), and accounts and reports are produced automatically with consistent codes. Pensioners, employees and offices see the status of their bills.

**Lesson.** Money is the backbone of government; a **budget-checked, bank-linked** payment system gives accountability and cash visibility. In Nepal the corresponding systems are the treasury and the SuTRA application for sub-national governments.

### 5.3.12 E-governance in the Directorate General of Foreign Trade (DGFT)

**Problem.** Exporters and importers applied for licences and authorisations in person, at regional offices of the DGFT, with large paper files and long waiting times, and each document had to be checked by hand.

**What was done.** The DGFT put the **application, processing and issue of licences online**: an exporter files over the Internet with a digital signature, fees are paid electronically, the application is processed by rule with an audit trail, and the result is downloaded and is linked electronically to customs for clearing. The registration number of the importer-exporter became the common key.

**Lesson.** G2B services gain most from **electronic filing and links to partner agencies** (customs, banks), because the businessman's real cost is delay at the border. Nepal's National Single Window follows the same logic.

### 5.3.13 PRAJA: rural e-Seva, a new paradigm in citizen services

**Problem.** Rural citizens had to go to the tehsil or district centre for certificates, records and bill payments, losing days and wages.

**What was done.** In the West Godavari district of Andhra Pradesh the district administration set up **PRAJA** (*praja* = the people) centres: rural **e-Seva** kiosks run by local entrepreneurs, connected to the district network, that deliver government and utility services (certificates, land records, bill payment, forms) near the village for a small fee. The same model was later offered in other places, and the urban e-Seva centres of Hyderabad and Secunderabad provided a one-stop payment and certificate service.

**Lesson.** **Franchised access points** solve the last-mile problem and the skills divide: the operator reads the form and uses the computer for the citizen. In India the national equivalent is the Common Service Centre; in Nepal, community information centres and ward help desks.

### 5.3.14 E-Panchayat and the General Information Services of NIC

**E-Panchayat.** A **panchayat** is the village-level elected local government (the nearest equivalent in Nepal is the ward or rural municipality). The *Electronic Knowledge-based Panchayat* project computerised the data and functions of these bodies: the village's resource and planning data, the beneficiaries and accounts of schemes, tax and fee collection and certificates, with a computer in the panchayat office and linked to the block and district. The lesson is that the **local body** is the unit where data are born, so unless the village office keeps correct data the district and the state statistics are weak. (Under the national programme it was later extended by e-Gram Swaraj, a portal for planning and accounts of panchayats.)

**General Information Services of NIC.** NIC runs the **national information infrastructure**: web hosting and a portal framework for central and state departments, email and messaging, the national government portal, video-conferencing across states and districts, a **national data centre**, databases (district information, census-based maps, parliament questions) and, more recently, cloud and common applications (e-office). It is a **shared service**: one expert agency serves hundreds of departments.

**Lesson.** A central technical agency with field presence is a critical success factor: it supplies skills, standards and economy of scale (compare Nepal's NITC).

#### Summary of the Indian cases

| Case | Core idea | Citizen or user | Key success factor |
|---|---|---|---|
| NICNET | National network | Government offices | Government-owned backbone and technical cadre |
| Collectorate 2000 | District office automation | Collector and staff | Head's need for monitoring |
| CARD | Registration at one counter | Property buyers | Process re-engineering, legal validity |
| Smart Nagarpalika | Municipal package | Urban citizens | One package, many municipalities |
| Reservoir monitoring | National data collection | Planners, public | Standard formats and schedule |
| APSTC | Trading business | Corporation | Stock and cash control |
| Ekal Seva Kendra | Single window | Citizens | One queue for many departments |
| Sachivalaya Vahini | Secretariat intranet and file tracking | Ministers, secretaries | Visible delay |
| Bhoomi | Land records and RTC | Farmers | Legal switch, fee recovery, audit trail |
| e-Courts | Case information and data grid | Litigants, courts | Visible pendency |
| E-Khazana | Treasury and payments | Departments, employees | Budget-checked, bank-linked payment |
| DGFT | Online licences | Exporters and importers | Electronic filing, customs link |
| PRAJA | Rural e-Seva kiosks | Villagers | Local operator, nearby access |
| E-Panchayat and NIC services | Local data; shared infrastructure | Village bodies, departments | Local data ownership; central agency |

## 5.4 Other countries

### 5.4.1 E-governance in the United States of America

**Background.** The USA moved from the 1990s "reinventing government" reviews to a legal and institutional frame for e-government. The **Government Paperwork Elimination Act (1998)** required agencies to accept electronic forms and signatures; **FirstGov.gov** (September 2000, now **USA.gov**) became the single portal to federal information and services; the **E-Government Act of 2002** created the Office of E-Government in the budget office (OMB), the post of **Federal Chief Information Officer**, and rules on information security and privacy. Cross-agency initiatives followed: Grants.gov (one place for all federal grants), **Regulations.gov** (citizens read and comment on proposed rules, a G2C2G interactive case), IRS Free File, Recreation.gov, and later **Data.gov** (open data, 2009) and **login.gov** (one sign-in).

**A famous failure and its lesson.** The launch of the HealthCare.gov insurance marketplace in October 2013 failed under load, with no end-to-end testing and many contractors. The rescue led to the **US Digital Service** and **18F**, small teams of designers and engineers who bring user-centred, agile methods into agencies. The lesson is that **a law and a CIO do not replace testing, a service owner and design for the user**.

**Features to remember.** Federal structure (agencies keep their systems but follow shared standards), strong legal base, privacy law, heavy use of contractors, wide use of the Internet by citizens.

### 5.4.2 E-governance in China: the Beijing Business E-Park

**Background.** China set up the **Government Online Project** in 1999 to put departments of the state on the Internet, followed by an official central portal and local portals. Cities tried **one-window portals for enterprises**, because registration, tax and permits needed many stamps.

**Beijing Business E-Park.** The Beijing Business E-Park is presented in the textbook as a municipal portal for firms: a company applies online for the registrations, certificates and approvals that were scattered across bureaus, and the system routes the request to the departments and returns the result, in a set time limit. It combined an information portal (rules, procedures, forms), an application and tracking service, and links among the participating departments. *Check the textbook for the list of departments and the dates.*

**Later development.** Cities such as Hangzhou and the province of Zhejiang later set the target of **"run at most once"** for citizens and firms, using shared data across departments, and the national platform integrates many local ones. Mobile payments and identity apps make services reachable by phone.

**Lesson.** G2B one-window service, a **time limit** that departments must meet, and sharing data between departments are the crux; strong administrative authority (and limited concern for privacy by some criteria) made the integration faster than in federal systems, a point on which comparison with the USA and India is possible.

### 5.4.3 Brazil: Poupatempo

**Problem.** In São Paulo citizens needed many documents (identity card, driving licence, employment record, certificates) from many separate offices with long queues; issuing an identity card could take two months.

**What was done.** **Poupatempo** ("time saver") was launched by the São Paulo state government in **1997**, under Governor Mário Covas, with its first unit in the Sé district; a state law of 1998 made it permanent. A unit places the state and municipal agencies' counters in **one building near public transport**, with a single reception, queue management, scanners, a common information system and trained staff. The network grew to over two hundred units offering **400 or more services**, with an app and WhatsApp for remote services. Issue time for an identity card fell, in the figures usually quoted, from about 60 days to a few days, and user surveys reported satisfaction above 90 per cent.

**Lesson.** The model works because it **moves the integration to the front office** where the citizen is, even when back offices remain separate, and it **bypasses** the old counters instead of reforming them, while keeping the old option. Observers also note a risk: the quality of some services (for example the medical exam for a licence) declined as volumes rose.

### 5.4.4 Sri Lanka: the Kothmale Community Radio Internet Project

**Problem.** Rural hill areas of Sri Lanka had no Internet access, low computer literacy and no local-language content.

**What was done.** The Kothmale community radio station (in the hills of the Kandy district) was chosen by **UNESCO**, with the Sri Lankan ministry and regulator, the broadcasting corporation and the University of Colombo, for a pilot in 1998 and 1999 that connected the studio to the Internet. The presenter used **"radio browsing"**: listeners phoned in with a question (a crop disease, a school-exam syllabus, a pension rule) and the presenter searched the Internet and answered **on air**. Local people formed an Internet club, built web pages of local information, and the station set up a telecentre where villagers could use computers.

**Lesson.** Where the Internet cannot reach people, **an established community medium** can act as an interface, which makes the Internet useful to people who cannot read English or use a keyboard. The project influenced similar community multimedia centres in several regions, and later national telecentre programmes in Sri Lanka.

## 5.5 Comparison and lessons

The code lists, for each of the twenty-two cases, the success factors that the published accounts stress, and counts them. The coding is a judgement for teaching, not a research result, but it makes the pattern visible.

```python
from collections import Counter
cases = {
    "Nepal eGMP":      {"plan", "donor-led", "weak ownership"},
    "Nepal local":     {"federal", "uneven capacity", "shared platform"},
    "Nagarik App":     {"existing registers", "single sign-on", "legal acceptance gap"},
    "NICNET":          {"backbone", "technical cadre"},
    "Collectorate":    {"head's support", "office automation"},
    "CARD":            {"process redesign", "legal validity", "revenue gain"},
    "Smart Nagarpalika": {"shared platform", "one package"},
    "Reservoir":       {"standard formats", "data owner"},
    "APSTC":           {"business control"},
    "Ekal Seva":       {"single window"},
    "Sachivalaya":     {"visible delay", "head's support"},
    "Bhoomi":          {"legal validity", "fee recovery", "audit trail", "political support"},
    "e-Courts":        {"visible delay", "standard formats"},
    "E-Khazana":       {"bank link", "process redesign"},
    "DGFT":            {"electronic filing", "agency link"},
    "PRAJA":           {"local operator", "nearby access"},
    "E-Panchayat":     {"local data", "shared platform"},
    "NIC services":    {"technical cadre", "shared platform", "backbone"},
    "USA":             {"legal base", "federal CIO", "user testing gap"},
    "China (E-Park)":  {"single window", "time limit", "agency link"},
    "Brazil":          {"single window", "front-office integration", "political support"},
    "Sri Lanka":       {"local operator", "community medium", "nearby access"},
}
count = Counter(f for fs in cases.values() for f in fs)
print("cases analysed:", len(cases))
for f, c in count.most_common(8):
    print("%-22s %d  %s" % (f, c, "#" * c))
shared = [k for k, v in cases.items() if "shared platform" in v]
print("shared-platform cases:", ", ".join(shared))
```
```output
cases analysed: 22
shared platform        4  ####
single window          3  ###
backbone               2  ##
technical cadre        2  ##
head's support         2  ##
process redesign       2  ##
legal validity         2  ##
standard formats       2  ##
shared-platform cases: Nepal local, Smart Nagarpalika, E-Panchayat, NIC services
```
Four themes stand out. (1) **Shared platforms and agencies** (NIC, NITC, one municipal package) bring skill and scale. (2) **Single window and nearby access** (Ekal Seva, PRAJA, Poupatempo, Beijing, Kothmale) address the citizen's experience and the digital divide. (3) **Legal validity and political support** (CARD, Bhoomi) turn a system into the only valid process. (4) **Visibility** (file tracking, the Judicial Data Grid, audit trails) changes behaviour inside the state.

| Dimension | Nepal | India | USA | China | Brazil | Sri Lanka |
|---|---|---|---|---|---|---|
| Starting point | Scattered systems; plan in 2006 | Technical agency (NIC) and networks from 1987 | Strong law and portals from 2000 | Government Online 1999; city portals | One-stop centres, 1997 | Community radio and telecentres |
| Main design idea | National identity, app and shared platforms | Task-specific applications by NIC with state governments | Federal standards, portals, user teams | Single window for firms, data sharing | Front-office integration | Local medium as interface |
| Chief strength | Federal opportunity and ID registers | Scale, reusable cases | Law, open data, later user-centred teams | Speed of integration | Citizen satisfaction | Inclusion of villagers |
| Chief weakness | Capacity, integration, practice behind law | Pilots that did not scale; variation among states | Fragmentation and contractor risk | Privacy and openness concerns | Quality at high volume | Limited scale and funding |

## 5.6 Laboratory work and the course project

The outline carries one hour a week of practical work. A suggested plan of eight sessions:

| Session | Task | Unit |
|---|---|---|
| 1 | Compute EGDI from component scores; chart three countries | 1 |
| 2 | Digital-divide reach model for a ward; propose a remedy | 1 |
| 3 | Build the grievance log and service-level report; add escalation rules | 2 |
| 4 | Score a municipality on the maturity self-assessment and on the good-governance scorecard | 2 |
| 5 | Score a failed project with ITPOSMO; compute NPV with and without adoption | 3 |
| 6 | Build a star schema for a public dataset (prices or school enrolment) and run roll-up and slice queries | 4 |
| 7 | Anomaly and k-anonymity checks on a synthetic extract | 4 |
| 8 | Case analysis: present one case with the five-question frame | 5 |

**Project ideas.** (a) *Ward service desk:* design the forms, data fields and complaint flow for recommendation letters in a ward of Nepal. (b) *Price dashboard:* build a warehouse of the weekly price of ten commodities and a dashboard with a spike alert. (c) *Case study:* choose a Nepali service (for example vehicle tax) and map it to the stages, maturity levels and ITPOSMO gaps.

## 5.7 Summary and exercises

**Summary.** Each case answers a clear problem with a design around one register or counter, a process change and a delivery channel. **Nepal:** the eGMP 2006 gave the plan, but execution was slow; local governments need shared platforms; the Nagarik App (beta 15 January 2021) turns existing registers into one citizen identity and verified documents, but practice still asks for paper. **India:** NICNET gave the network; CARD, Bhoomi and e-Khazana rebuilt registration, land and treasury processes with legal backing; Smart Nagarpalika, e-Panchayat and NIC services show shared platforms; Ekal Seva Kendra, PRAJA and Sachivalaya Vahini show single window, nearby access and visible delay; e-Courts and DGFT show digital case data and B2G filing. **Abroad:** the USA (law, CIO, portals, digital teams), China (one-window portals for firms), Brazil (Poupatempo) and Sri Lanka (Kothmale radio browsing).

1. State the five questions for analysing an e-governance case and apply them to any one case.
2. Describe the e-Government Master Plan of Nepal and explain why its implementation was slow.
3. Discuss e-governance in the local governments of Nepal: what exists, the problems and the way ahead.
4. Describe the Nagarik App: purpose, design, services, benefits and limits.
5. Explain how a signed QR code makes a printed document verifiable. Why must the signing key stay with the issuing agency?
6. What was NICNET? Why is networking a precondition for applications?
7. Describe CARD with its problem, design, results and lessons.
8. A deed costs a citizen five days of wages at Rs 400 a day and Rs 800 to an agent before CARD, and one hour (of an 8-hour day) after. Compute the saving per deed.
9. Explain the Smart Nagarpalika package and why one package for many municipalities is economical.
10. Describe Sachivalaya Vahini and the National Reservoir Level and Capacity Monitoring System.
11. Describe the Bhoomi project and the part played by the legal change that made manual RTCs invalid.
12. A kiosk system has yearly fixed cost Rs 22 million and variable cost Rs 2 per record, with a fee of Rs 15. Find the break-even number of records.
13. Describe the e-Courts project and the National Judicial Data Grid.
14. Explain E-Khazana and DGFT, stating the main benefit of each.
15. What is PRAJA? How does it overcome the digital divide?
16. Write notes on e-Panchayat and the General Information Services of NIC.
17. Describe the e-government initiatives of the USA and the lessons of HealthCare.gov.
18. Explain the Beijing Business E-Park as a G2B case.
19. Describe Poupatempo of Brazil with its results and risks.
20. Describe the Kothmale Community Radio Internet Project. Why was radio used?
21. Compare Nepal and India in e-governance, with three similarities and three differences.
22. Which cases are best examples of the single-window idea? Of legal validity? Of shared platforms? Give reasons.

**Answers to the numerical items.** (8) Before: 5 x 400 + 800 = 2,800; after: (1/8) x 400 = 50; **saving = Rs 2,750 per deed (98 per cent)**. (12) Break-even volume = fixed cost / (fee - variable cost) = 22,000,000 / (15 - 2) = **about 1.69 million records a year**.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Describe the Nagarik App.**

The Nagarik App is the Government of Nepal's mobile and web platform that brings citizens' services into one place. Built under the Digital Nepal Framework by the Ministry of Communication and Information Technology with the National Information Technology Centre, it was launched in beta on 15 January 2021. Identity rests on existing registers (citizenship records of the Ministry of Home Affairs and biometric data of the Election Commission); a citizen registers with a mobile number linked to the citizenship number and a one-time code. Services: document wallet and verification, police clearance, PAN and tax, local-government information, social security and provident fund. Benefits: one sign-in, fewer queues, QR-verifiable documents. Limits: many offices still ask for physical documents; coverage of services is incomplete; digital divide.

**Q2 (5 marks). Explain CARD of Andhra Pradesh.**

CARD (Computer-aided Administration of Registration Department) computerised the registration of property documents at 387 sub-registrar offices from 1998. The deed is typed and printed at the counter, scanned and stored, with photographs and signatures of the parties; stamp duty is computed from a market-value table; certified copies and encumbrance certificates come from the database. Registration that took days took about an hour, about 80 per cent of registrations were electronic six months after launch, middlemen lost their role and revenue rose through uniform valuation. Lessons: process re-engineering, legal validity of electronic copies, and a departmental revenue gain.

**Q3 (10 marks). Describe the Bhoomi project and list the lessons.**

Give the problem (9,000 village accountants, the RTC needed for loans and ownership, delay and bribes), the design (about 20 million records of 6.7 million farmers; kiosks in about 177 taluk offices; a printed RTC for Rs 15; biometric authentication of operators; audit trail; online mutation), the implementation rule (manual RTCs declared invalid taluk by taluk), the results (RTC in minutes, easier bank loans, fewer unofficial payments, cost recovery through the fee) and the lessons: legal switch, political support, staff involvement, fee that covers cost depends on volume (break-even about 1.7 million RTCs a year), a receipt and monitoring are needed to prevent unofficial charges, and records in the public domain empower farmers.

**Q4 (10 marks). Discuss e-governance in the local governments of Nepal.**

Describe the 753 local levels and their services; the existing systems (websites, civil registration, allowance and revenue software, treasury applications, e-procurement, Hello Sarkar); the problems (uneven capacity, connectivity and power, IT staff and transfers, siloed systems, low digital skills, paper rules); and the way ahead (shared national platforms, shared IT teams among small municipalities, ward facilitators, national ID as a common key, training and legal recognition in practice). Tie the argument to the readiness model of Unit 3 and to the Indian examples of Smart Nagarpalika and PRAJA.

**Q5 (10 marks). Compare the e-governance experiences of two or more countries.**

Use the comparison table of 5.5: starting point, design idea, chief strength and weakness for Nepal, India, the USA, China, Brazil and Sri Lanka. Draw four themes: shared platforms and technical agencies, single window and nearby access, legal validity with political support, visibility inside the state. Conclude with the lessons for Nepal: fix registers and identity first, integrate at the front office while the back office improves, give services legal force, plan for adoption and the digital divide, and fund sustainability.
