---
subject: Network Administration
grade: BCA Semester 8 (Elective III)
unit: 5
title: Procurement Plan for an Enterprise Network
hours: 6
area: BCA 453 · Network Administration · Unit 5
---

The previous units described what a good network looks like. Somebody must now **buy** it: choose the equipment and services, justify the budget, write the document that vendors answer, compare their offers and sign a contract that the organisation can enforce. In this unit you prepare a **procurement plan and document** for an enterprise-level network, using one running case from start to finish.

::: key What this unit gives you
- The procurement process and its documents (RFI, RFQ, RFP, tender, BoQ), with a note on public procurement in Nepal.
- From requirements to a **bill of quantities**, computed by program for the case study, with the budget, VAT, contingency and a five-year cost of ownership.
- The structure of a procurement document: technical specification, compliance matrix, evaluation criteria, SLA, warranty, delivery, payment, acceptance tests, training and penalties.
- Bid evaluation by weighted scoring, implementation planning and handover.
:::

## 5.1 The procurement process

### 5.1.1 Why a plan and a document

Buying a network by walking into a shop gives you products, not a solution, and leaves the organisation with no leverage if the system does not work. A **procurement plan** turns needs into a buying decision in a way that is **fair** (vendors compete on equal terms), **transparent** (the criteria are known beforehand), **economical** (lowest total cost for the required quality) and **enforceable** (the contract states what must be delivered and what happens if it is not).

### 5.1.2 Stages

```svgfig label="5.1" caption="The procurement process from need to handover. Technical requirements and evaluation criteria are fixed before any vendor is contacted."
f = Fig(680, 250)
labels = ["1 Need and\nbudget\napproval", "2 Requirements\nand design", "3 Procurement\ndocument\n(RFQ / RFP)", "4 Invite bids\nand clarify", "5 Evaluate\nand select", "6 Contract,\ndeliver,\ninstall", "7 Acceptance,\ntraining,\nhandover"]
for i, t in enumerate(labels):
    x = 8 + i * 96
    f.box(x, 40, 86, 70, t, fill=SAND if i in (2, 4) else BLUE, stroke=AMBER if i in (2, 4) else NAVY, size=9)
    if i < 6:
        f.arrow([(x + 86, 75), (x + 96, 75)], color=NAVY)
f.arrow([(630, 110), (630, 170), (50, 170), (50, 110)], color=SLATE, dash=True, label="support, SLA review, refresh planning", lpos=(340, 185))
f.text(340, 225, "Shaded stages decide the outcome: weak documents and vague criteria cannot be repaired later.", size=10, color=SLATE)
```

### 5.1.3 Documents in the buying chain

| Document | Meaning | When used |
|---|---|---|
| **RFI** (request for information) | Asks vendors what solutions exist, without commitment | Early, when the technology or market is unclear |
| **RFQ** (request for quotation) | Asks for **prices** for precisely specified items | Standard goods (switches, access points, UPS) |
| **RFP** (request for proposal) | Asks for a **solution** and price against stated requirements | Complex projects (a complete campus network) |
| **Tender / bid document** | Formal, usually public, competitive process with rules, bid security and a deadline | Large purchases, and by law for public bodies |
| **BoQ** (bill of quantities) | Table of items, quantities, unit and total prices | Part of every bid |
| **Purchase order / contract** | Binding agreement with terms and schedule | After selection |

### 5.1.4 Public procurement in Nepal

Government bodies, public universities and many publicly funded institutions in Nepal buy under the **Public Procurement Act, 2063 (2007)** and the **Public Procurement Rules, 2064 (2007)**, supervised by the **Public Procurement Monitoring Office (PPMO)**. Bids above the thresholds are invited through the **e-GP (e-Government Procurement) system** (Bolpatra). The documents include a standard bidding document, bid security, performance security, qualification criteria and price evaluation rules. A private company is free to use a simpler process, but the same principles apply. (The thresholds, forms and rules are amended from time to time: always check the current text and the PPMO's standard documents before preparing a real tender.)

## 5.2 The case study: requirements and design

**Himalaya Institute of Technology** has two buildings 120 m apart on one campus (Block A, three floors; Block B, two floors), a hostel, 1,200 students, 110 staff and 150 lab computers. The management wants a new network for the next five years. It has these needs (collected as in Section 2.3.2):

| Area | Requirement |
|---|---|
| **Users and devices** | 1,200 students and 110 staff, with an average 1.8 devices each at peak in Wi-Fi; 150 lab PCs; 40 IP phones; 30 CCTV cameras; 12 printers |
| **Coverage** | Wi-Fi in all classrooms, labs, library, administration, hostel; 1 access point per 40 simultaneous clients, plus corridor coverage |
| **Wired** | 150 lab ports; 110 staff ports; 40 phone ports through the same PCs; 12 printers; 30 camera ports (PoE) |
| **Services** | Servers for directory and DNS/DHCP, file storage, learning-management system, admission and fee portal, mail (hosted), backup; central firewall |
| **Availability** | Fee portal 99.9% in working hours; network core redundant; UPS 30 minutes; generator already exists |
| **Internet** | 300 Mbit/s primary fibre and 100 Mbit/s secondary from a second ISP |
| **Security** | Segmented VLANs, 802.1X for staff Wi-Fi, guest isolation, firewall with intrusion prevention, logs kept 6 months |
| **Management** | Central monitoring, configuration backup, documentation, training for two staff |
| **Budget** | Approved ceiling NPR 12,000,000 including VAT; five-year support contract |
| **Timeline** | Delivered and accepted within 12 weeks, between two terms |

### 5.2.1 From requirements to quantities

The design follows Unit 3: two core switches in Block A (collapsed core), a distribution/access switch stack in each floor closet, fibre between blocks and to the hostel, PoE access switches for access points, phones and cameras, a firewall pair at the internet edge, a server room with two virtualisation hosts and a NAS, and a monitoring and backup stack. The program computes quantities from the requirements and prices them (unit prices are illustrative planning figures for 2025, in NPR, not quotations).

```python
import math
# 1. Quantities from requirements
wifi_devices = int(1310 * 1.8 * 0.55)           # 55% of users connected at the peak
aps_capacity = math.ceil(wifi_devices / 40)
aps_coverage = 62                               # from the predictive site survey (rooms, corridors, hostel)
aps = max(aps_capacity, aps_coverage)
wired_ports = 150 + 110 + 12 + 30 + aps         # labs, staff, printers, cameras, access points
spare = 0.25
ports_needed = math.ceil(wired_ports * (1 + spare))
sw48 = math.ceil(ports_needed / 48)
print("simultaneous Wi-Fi devices :", wifi_devices, "-> APs by capacity", aps_capacity, ", by coverage", aps_coverage, "-> buy", aps)
print("wired ports needed         :", wired_ports, "+25%% spare = %d -> 48-port switches: %d" % (ports_needed, sw48))
poe_watts = (aps * 15.4 + 30 * 8 + 40 * 7) / 0.85   # APs, cameras, phones; margin for efficiency
print("PoE budget                 : %.0f W" % poe_watts)

# 2. Bill of quantities
boq = [
 ("Core switch, 24 x 10G SFP+, layer 3",             2, 420000),
 ("Access switch 48 x 1G PoE+, 4 x 10G uplinks",     sw48, 150000),
 ("Wi-Fi 6 access point, indoor",                    aps, 19000),
 ("Wireless controller licence (per AP, 5 years)",   aps, 4500),
 ("Next-generation firewall pair, IPS, 5-year licence", 2, 520000),
 ("Rack server 2 x 16-core, 256 GB, redundant PSU",  2, 480000),
 ("NAS 8-bay, 8 x 8 TB, snapshots",                  1, 420000),
 ("Backup appliance / disk, 40 TB usable",           1, 380000),
 ("UPS 10 kVA online, 30 min battery",               2, 350000),
 ("Racks 42U, PDUs, cable management",               4, 95000),
 ("Fibre 12-core armoured, per 100 m, with installation", 4, 60000),
 ("Cat 6A structured cabling per point, installed",  wired_ports, 3600),
 ("Monitoring and logging servers (software free)",  1, 150000),
 ("Installation, configuration, testing (lump sum)", 1, 550000),
 ("Training and documentation (2 staff, 5 days)",    1, 120000),
]
subtotal = 0
for name, q, price in boq:
    line = q * price
    subtotal += line
    print("%-54s %3d x %8d = %10d" % (name, q, price, line))
contingency = 0.05 * subtotal
vat = 0.13 * (subtotal + contingency)
total = subtotal + contingency + vat
print("subtotal                 : %12d" % subtotal)
print("contingency 5%%           : %12d" % contingency)
print("VAT 13%%                  : %12d" % vat)
print("total                    : %12d   (ceiling 12,000,000: %s)" % (total, "within" if total <= 12_000_000 else "OVER"))
```
```output
simultaneous Wi-Fi devices : 1296 -> APs by capacity 33 , by coverage 62 -> buy 62
wired ports needed         : 364 +25% spare = 455 -> 48-port switches: 10
PoE budget                 : 1735 W
Core switch, 24 x 10G SFP+, layer 3                      2 x   420000 =     840000
Access switch 48 x 1G PoE+, 4 x 10G uplinks             10 x   150000 =    1500000
Wi-Fi 6 access point, indoor                            62 x    19000 =    1178000
Wireless controller licence (per AP, 5 years)           62 x     4500 =     279000
Next-generation firewall pair, IPS, 5-year licence       2 x   520000 =    1040000
Rack server 2 x 16-core, 256 GB, redundant PSU           2 x   480000 =     960000
NAS 8-bay, 8 x 8 TB, snapshots                           1 x   420000 =     420000
Backup appliance / disk, 40 TB usable                    1 x   380000 =     380000
UPS 10 kVA online, 30 min battery                        2 x   350000 =     700000
Racks 42U, PDUs, cable management                        4 x    95000 =     380000
Fibre 12-core armoured, per 100 m, with installation     4 x    60000 =     240000
Cat 6A structured cabling per point, installed         364 x     3600 =    1310400
Monitoring and logging servers (software free)           1 x   150000 =     150000
Installation, configuration, testing (lump sum)          1 x   550000 =     550000
Training and documentation (2 staff, 5 days)             1 x   120000 =     120000
subtotal                 :     10047400
contingency 5%           :       502370
VAT 13%                  :      1371470
total                    :     11921240   (ceiling 12,000,000: within)
```
The first result shows that **coverage, not capacity, decides the number of access points**; the plan buys the larger figure. The total must be compared with the approved ceiling *before* the document is issued; if it is over, the design (not the quality of the specification) is reduced, for example by delaying the hostel link.

### 5.2.2 Total cost of ownership

The purchase price is only part of the cost. Over five years the institute also pays for electricity, support contracts, licence renewals, staff time, and replacement of items that fail or become obsolete. Compare bids on **total cost of ownership (TCO)**, not on the lowest price.

```python
# Five-year TCO of two competing bids (illustrative)
years = 5
bids = {
 "Vendor A": dict(capex=10_400_000, support_per_year=350_000,   power_kw=11.0, spares=250_000),
 "Vendor B": dict(capex=9_100_000,  support_per_year=720_000,   power_kw=15.5, spares=600_000),
}
rate = 14.0   # NPR per kWh
for name, b in bids.items():
    power = b["power_kw"] * 24 * 365 * rate * years
    tco = b["capex"] + b["support_per_year"] * years + power + b["spares"]
    print("%s: purchase %9d  support %9d  power %9d  spares %8d  TCO %10d" %
          (name, b["capex"], b["support_per_year"] * years, power, b["spares"], tco))
```
```output
Vendor A: purchase  10400000  support   1750000  power   6745200  spares   250000  TCO   19145200
Vendor B: purchase   9100000  support   3600000  power   9504600  spares   600000  TCO   22804600
```
The cheaper purchase (Vendor B) is the costlier system over five years once support, electricity and spares are added, a result the evaluation criteria must be able to capture.

## 5.3 The procurement document

A procurement document (RFP or bidding document) is a contract in preparation. Its structure, applied to the case study:

| Section | Content |
|---|---|
| **1 Invitation and summary** | Who is buying, what, delivery place, deadline for questions and for bids, contact person, bid security amount |
| **2 Instructions to bidders** | Eligibility (registered company, VAT and PAN registration, tax clearance), language, currency, validity of the bid (for example 90 days), how to submit, how to ask questions, site visit, rules on alternatives |
| **3 Background and scope** | Short description of the institute, the buildings, the present network and the goals; what is *in* the scope (supply, installation, configuration, training, support) and what is *out* |
| **4 Technical specifications** | Item-by-item requirements: **mandatory** (must) and **desirable** (should) features, written so that more than one vendor can meet them |
| **5 Compliance matrix** | A table the bidder fills in: requirement, complies yes/no/partly, product part number, page of the datasheet that proves it |
| **6 Commercial terms** | Prices in a **BoQ** with VAT shown separately, payment schedule, delivery period, warranty, support, penalties, performance guarantee |
| **7 Service levels** | Response and fix times by severity, support hours, spare policy, escalation, reporting |
| **8 Implementation and acceptance** | Project plan, site survey duty, test plan, acceptance criteria, documentation, training |
| **9 Evaluation criteria** | Eligibility pass/fail, technical score, price score and their weights, how ties and errors are handled |
| **10 Forms and annexes** | Bid form, price schedule, bid security form, experience forms, manufacturer authorisation |

### 5.3.1 Writing technical specifications

A good specification states the **need and the measure**, not a brand: write "48 x 10/100/1000 Mbit/s IEEE 802.3at PoE+ ports, 740 W PoE budget or more, 4 x 10G SFP+ uplinks, 176 Gbit/s switching capacity or more, IPv6 support, 802.1Q, 802.1X, RSTP, LACP, SNMPv3, SSH, stackable or MLAG" instead of "Brand X model Y". Naming a brand without "or equivalent" locks out competitors and, in public purchases, may be illegal. Other rules:

- **Separate mandatory from desirable** features; give marks for desirable ones.
- Use **standards** (IEEE, IETF, ISO) and **measurable values** (throughput, capacity, MTBF, noise), not adjectives like "high-quality".
- Require **evidence**: datasheets, certificates, test reports, and **manufacturer authorisation** to prove the bidder can supply and support the product locally.
- Ask for **compatibility** with existing equipment, and for **open management interfaces** (SNMP, syslog, APIs).
- Include **lifecycle** requirements: end-of-sale and end-of-support dates not earlier than five years from delivery, firmware updates for the warranty period.
- State **environmental conditions** (voltage 230 V 50 Hz, temperature, humidity) and **safety** certification.
- Ask for **spares and a local service centre** with response times.

::: example Specification extract: wireless access point
Mandatory: IEEE 802.11ax (Wi-Fi 6), dual band 2.4 and 5 GHz, 2 x 2 MIMO or better, at least 1.7 Gbit/s combined data rate, one 2.5 Gbit/s Ethernet port, PoE 802.3at, WPA3 and 802.1X, central management by the offered controller, at least 200 simultaneous clients, ceiling and wall mounting kit included, five-year warranty. Desirable (extra marks): 6 GHz support, integrated BLE, spectrum analysis, per-client airtime fairness, plenum rating. Evidence: datasheet page numbers and manufacturer authorisation.
:::

### 5.3.2 Commercial and legal terms

| Term | Purpose | Typical practice |
|---|---|---|
| **Bid validity** | Time during which the offer cannot be withdrawn | 60-120 days |
| **Bid security (earnest money)** | Protects against frivolous bids | A small percentage of the estimate (a bank guarantee or deposit); returned after contract signing |
| **Performance guarantee** | Protects against non-performance | A percentage of the contract value held for the contract period |
| **Delivery schedule** | Dates and milestones | Weeks from order, by phase |
| **Payment schedule** | Ties money to progress | For example 30% on delivery, 40% on installation and testing, 20% on acceptance, 10% after the first warranty year |
| **Liquidated damages** | Fixed daily penalty for delay | A small percentage of the delayed part per week, with a cap |
| **Warranty and support** | Repair or replace faulty items | Three to five years; defined response times |
| **Intellectual property and licences** | Who owns configurations and documents | Documents and configurations belong to the buyer; licences are in the buyer's name |
| **Confidentiality** | Protects network designs and passwords | A signed non-disclosure agreement |
| **Termination and disputes** | How to end or resolve | Notice periods, arbitration in Nepal under the Arbitration Act |

(Check the specific percentages and procedures against the current rules and the advice of the institution's legal officer.)

### 5.3.3 Service-level terms

An SLA turns support into numbers.

| Severity | Definition | Response | Fix or workaround |
|---|---|---|---|
| **1 Critical** | Core, firewall or internet down; fee portal unavailable | 30 minutes, 24 x 7 | 4 hours |
| **2 High** | Major part degraded (one building, one VLAN) | 2 hours, working hours | 1 working day |
| **3 Medium** | A single user or device | Next working day | 3 working days |
| **4 Low** | Information request, minor change | 2 working days | By agreement |

Add **reporting** (monthly tickets and availability), **spares** (cold spare of each critical device on site), **preventive maintenance visits** and **penalties or service credits** when the levels are missed.

## 5.4 Evaluating bids

### 5.4.1 The stages

1. **Opening and checking**: record the bids received before the deadline; late bids are rejected.
2. **Preliminary (eligibility) check**: registration and tax documents, bid security, forms signed, validity: pass or fail.
3. **Technical evaluation**: check each mandatory item against the compliance matrix and evidence; all mandatory items must pass; desirable items earn marks. Ask clarification questions in writing; allow demonstrations or a proof of concept of key items if the document says so.
4. **Financial evaluation**: correct arithmetic errors by the stated rule, convert to a common basis (with VAT, with five-year support and a TCO adjustment), compare.
5. **Combined score**: in **quality-and-cost-based selection (QCBS)** a weighted sum of technical and price scores; in **least-cost selection** the lowest price among technically qualified bidders wins. The method and the weights are announced in the document.
6. **Reference checks** with other customers, and a **negotiation** only within the rules.
7. **Recommendation, approval and notification**; keep a record of the reasons.

Standard formula for the price score: **price score = 100 x (lowest evaluated price / bidder's evaluated price)**.

```python
# Weighted evaluation of three bids: 70% technical, 30% price (illustrative)
bids = {
 "Vendor A": dict(mandatory_ok=True, tech=84, price=19_100_000),
 "Vendor B": dict(mandatory_ok=True, tech=71, price=22_800_000),
 "Vendor C": dict(mandatory_ok=False, tech=90, price=18_000_000),   # fails a mandatory item
}
wt, wp = 0.70, 0.30
qualified = {k: v for k, v in bids.items() if v["mandatory_ok"]}
lowest = min(v["price"] for v in qualified.values())
rows = []
for name, v in qualified.items():
    ps = 100 * lowest / v["price"]
    total = wt * v["tech"] + wp * ps
    rows.append((total, name, v["tech"], ps))
for total, name, t, ps in sorted(rows, reverse=True):
    print("%-9s technical %5.1f  price score %5.1f  combined %5.1f" % (name, t, ps, total))
for name, v in bids.items():
    if not v["mandatory_ok"]:
        print("%-9s rejected: mandatory requirement not met (cheapest and highest technical score are irrelevant)" % name)
print("recommended:", sorted(rows, reverse=True)[0][1])
```
```output
Vendor A  technical  84.0  price score 100.0  combined  88.8
Vendor B  technical  71.0  price score  83.8  combined  74.8
Vendor C  rejected: mandatory requirement not met (cheapest and highest technical score are irrelevant)
recommended: Vendor A
```
The result shows two principles: a bid that fails a **mandatory** requirement is rejected whatever its price or score, and the price score rewards the lowest price but a better technical score can outweigh a modest price difference.

### 5.4.2 Common mistakes

| Mistake | Consequence |
|---|---|
| Specifying a brand | Fewer bidders, higher prices, complaints |
| Vague requirements | Incomparable bids; arguments at acceptance |
| Evaluating on purchase price only | Choosing the system that costs most to run |
| No acceptance tests | Disputes about "does it work?" |
| Forgetting cabling, installation, power, cooling and training | Hidden extra cost, delays |
| No licence and renewal plan | Features switch off after a year |
| Single vendor lock-in with no exit | Weak position at renewal |
| Ignoring local support | Failures last for weeks while parts are imported |
| Rushing the schedule | Errors found by users, not by tests |

## 5.5 Implementation plan, acceptance and handover

A contract is only the start; the project must be managed. The plan for the case study (12 weeks):

| Weeks | Activity | Output |
|---|---|---|
| 1-2 | Contract signature, kick-off, detailed site survey, final design | Approved design, VLAN and address plan, bill of materials confirmed |
| 3-6 | Delivery, cabling and fibre, racks, power and UPS | Cabling certification reports, rack elevations |
| 5-8 | Install and configure core, access, wireless, firewall, servers, storage | Configurations in version control |
| 8-9 | Services: directory, DHCP/DNS, monitoring, backup | Service checklists |
| 9-10 | Testing: functional, performance, failover, security | Test report |
| 10-11 | Pilot with one block; then migration of the rest during a break | Migration log |
| 11-12 | Training, documentation, acceptance, handover | Signed acceptance, as-built documents |

**Acceptance tests** are written before the contract is signed and attached to it:

1. **Inventory check**: all items delivered, serial numbers recorded, warranty start dates documented.
2. **Cabling**: each permanent link certified (length, attenuation, crosstalk) with a printed report; all ports labelled.
3. **Functional**: every VLAN reaches only what it should; DHCP, DNS, directory login, printing, Wi-Fi roaming, guest isolation.
4. **Performance**: throughput between blocks and to the internet with `iperf3`; Wi-Fi signal and speed at sampled points against the survey.
5. **Resilience**: pull one core link, one power supply and one internet link in turn; the service must continue and failover time must be inside the stated limit.
6. **Security**: scan for open ports, test firewall rules, check default passwords removed, MFA and logging working.
7. **Monitoring and backup**: all devices visible, alerts reach the team, a backup restores.
8. **Documentation**: as-built diagrams, address plan, configurations, passwords in a vault, runbooks.
9. **Training**: sessions held and attended; a hands-on exercise passed.

Only after all tests pass is the **acceptance certificate** signed and the retained payment released. Afterwards the support period begins; the contract should provide a **review after the first year** and a refresh plan for year five.

## 5.6 Summary and exercises

Procurement turns requirements into an enforceable purchase. The process runs from need, requirements and design, to a procurement document (RFQ for goods, RFP for solutions, a tender for formal public purchases), bids, evaluation, contract, delivery and acceptance. Quantities come from requirements (capacity and coverage for Wi-Fi, ports with spare, PoE budget) and are entered in a BoQ with VAT, contingency and the budget ceiling. Specifications are measurable, brand-neutral and divided into mandatory and desirable items; commercial terms cover validity, bid security, performance guarantee, payment, delay damages, warranty and SLAs. Bids are evaluated by eligibility, technical compliance, price and a combined score, preferably on five-year TCO. Implementation follows a phased plan with written acceptance tests, training and documentation, and payment is tied to acceptance.

1. Define procurement. State four principles that a good procurement process follows.
2. Distinguish RFI, RFQ, RFP, tender and BoQ.
3. Describe the stages of procurement from need to handover.
4. What does the Public Procurement Act, 2063 provide, and what is e-GP? (State that rules must be checked in their current form.)
5. How do you convert requirements into quantities of access points, switches and PoE budget? Explain why coverage can exceed capacity.
6. Why should a specification not name a brand? What is the phrase "or equivalent" for?
7. Write a technical specification for a 48-port PoE access switch and a firewall, separating mandatory and desirable items.
8. List the parts of a procurement document and the purpose of the compliance matrix.
9. Explain bid security, performance guarantee, liquidated damages and payment schedule.
10. Draft an SLA with four severity levels for the case study network.
11. Describe the evaluation of bids. Why is a bid that fails a mandatory requirement rejected whatever its price?
12. What is TCO? Why is the lowest purchase price not always the best choice?
13. Prepare the implementation plan and acceptance tests for a network installation.
14. Prepare a complete procurement plan for a 300-user bank branch network (requirements, BoQ outline, evaluation method, schedule).
15. Vendor A scores technical 80 at NPR 9,000,000; Vendor B scores technical 70 at NPR 7,500,000; weights 70% technical, 30% price. Who wins? A project needs 300 devices on Wi-Fi with 30 clients per access point by capacity, and the survey says 14 for coverage: how many access points?

**Answers to the numerical items.** (15) Lowest price 7,500,000: B's price score 100, A's price score = 100 x 7.5/9.0 = 83.3. Combined A = 0.7 x 80 + 0.3 x 83.3 = 56 + 25 = 81.0; B = 0.7 x 70 + 0.3 x 100 = 49 + 30 = 79.0. Vendor A wins. Access points: 300/30 = 10 by capacity, 14 by coverage, so buy 14. For the case study the program of Section 5.2.1 prints the quantities and a total of NPR 11.92 million, just inside the NPR 12 million ceiling.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the contents of a procurement (bidding) document.**

It contains an invitation with deadlines, instructions to bidders (eligibility, validity, submission), background and scope, technical specifications with mandatory and desirable items, a compliance matrix where the bidder states and proves how each requirement is met, commercial terms (BoQ, payment schedule, delivery, warranty, penalties, guarantees), service levels, an implementation and acceptance section, evaluation criteria with weights, and forms. The aim is that all bidders answer the same questions on equal terms so that their offers can be compared and later enforced as the contract.

**Q2 (5 marks). Why compare bids on total cost of ownership?**

Purchase price is only part of the cost of a network over its life. Support contracts, licence renewals, electricity, spare parts, staff time and downtime may exceed the saving of a cheaper purchase. In the example, a bid that is NPR 1.3 million cheaper to buy costs NPR 3.7 million more over five years. TCO is calculated from the bids' stated support charges, power use and spares, and the evaluation criteria announce that it will be used, so the comparison is fair.

**Q3 (10 marks). Prepare a procurement plan for the network of a two-building college with 1,200 students.**

Requirements: users and devices (1,310 users, 150 lab PCs, 40 phones, 30 cameras, 12 printers), Wi-Fi coverage in all areas, services (directory, DNS/DHCP, LMS, fee portal, hosted mail, backup), availability (99.9% for the portal, redundant core, 30-minute UPS), internet with two ISPs, security (VLANs, 802.1X, firewall with IPS, logs), management and training, budget ceiling and schedule.

Design and quantities: collapsed core of two layer-3 switches, PoE access switches in each floor closet sized from ports with 25% spare (the program gives 10 switches of 48 ports), 62 access points chosen by coverage rather than capacity, fibre between blocks, a firewall pair, two virtualisation hosts, a NAS and a backup appliance, UPS, racks and certified cabling. A BoQ with prices, contingency, VAT and total is compared with the ceiling.

Document: invitation, instructions, scope, brand-neutral specifications with mandatory and desirable items, compliance matrix, commercial terms (validity, bid security, performance guarantee, payment tied to milestones, liquidated damages), SLA with four severity levels, acceptance tests and evaluation criteria (eligibility pass/fail, mandatory items pass/fail, 70% technical and 30% price on a five-year TCO basis).

Evaluation and award: open bids, check eligibility and mandatory items, score, calculate price scores, check references, recommend and record reasons.

Implementation: twelve-week phased plan between terms, with pilot, migration, acceptance tests (inventory, cabling certification, functional, performance, failover, security, monitoring and backup restore, documentation, training), signed acceptance and retained payment released after it.

Conclusion: a clear, measurable and fair document, a realistic budget, and written acceptance tests are what make the purchase succeed.
