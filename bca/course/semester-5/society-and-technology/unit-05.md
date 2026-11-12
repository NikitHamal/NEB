---
subject: Society and Technology
grade: BCA Semester 5
unit: 5
title: e-Governance in Nepal
hours: 7
area: BCA 305 · Society and Technology · Unit 5
---

Getting a citizenship-linked service used to mean a journey to the district office, a queue, a photocopy and a stamp. **e-Governance** replaces some of that with a verified record, an online form and a digital signature. This unit explains what e-governance is, how it is measured, the main Nepali systems (the National ID, the Nagarik App, the government data centre and office systems, local-level software) and the cryptographic idea that makes electronic documents trustworthy: the **digital signature**, which you will run on a toy example.

::: key What this unit gives you
- e-Government, e-governance and m-government; stages of maturity; the G2C, G2B, G2G and G2E models.
- An index calculation (UN-style EGDI) and a simple cost-benefit estimate for a service.
- Nepali building blocks: National ID, Nagarik App, GIDC and office systems, Palika IT systems, taxes, procurement and payments.
- Digital signatures and PKI shown with a runnable example; challenges and good practice.
:::

*System names and status below are described in general terms from public sources; features and rollouts change, so verify current services on the official portals.*

## 5.1 Concepts

**e-Government** is the use of ICT by government to deliver services and information. **e-Governance** is wider: using ICT to improve the *process of governing*, including transparency, participation and accountability, not only service delivery. **m-Government** delivers services by mobile. Interaction models: **G2C** (government to citizen: certificates, tax filing), **G2B** (to business: company registration, customs), **G2G** (between agencies: data sharing, office systems) and **G2E** (to employees: payroll, leave). Benefits: faster and cheaper services, fewer visits and less corruption through traceable processes, better data for planning, and wider access. Risks: exclusion of the offline, privacy and surveillance, security failures, vendor dependence and projects that digitise a bad process.

**Maturity stages** (UN-style): **emerging** (information websites), **enhanced** (two-way interaction, downloadable forms), **transactional** (complete services and payments online) and **connected** (integrated, seamless services across agencies). A single department site that lists office hours is stage 1; a person who registers a birth online, pays the fee through a wallet and receives a verifiable certificate is at stage 3 or 4.

### Measuring e-government: an EGDI-style index

The UN **E-Government Development Index (EGDI)** averages three normalised components: the **Online Service Index (OSI)**, the **Telecommunication Infrastructure Index (TII)** and the **Human Capital Index (HCI)**. For a country with OSI = 0.52, TII = 0.41 and HCI = 0.63 (invented), the sum is 1.56 and EGDI = 1.56/3 = **0.520**. The decomposition tells policy: here, infrastructure (TII) is the weakest component, so the investment priority is connectivity, not more online forms.

### A simple cost-benefit estimate

Suppose a service moves online so that each of 1,20,000 applicants avoids 2 visits and each visit costs 3.5 hours of lost time valued at Rs 60 an hour. Visits avoided = **2,40,000**; hours saved = 2,40,000 × 3.5 = **8,40,000**; value = 8,40,000 × 60 = **Rs 5,04,00,000**. If the system costs Rs 45,00,000 a year, the net benefit is **Rs 4,59,00,000**. The benefit is to citizens, not to the agency's budget, which is why such projects need central funding and a shared view of value; the estimate also assumes that every applicant has access, which is rarely true.

## 5.2 Building blocks in Nepal

**National ID (NID).** The National Identity Card programme issues a unique **National Identification Number** to each person, linked to demographic and **biometric** data (fingerprints and photograph) in a national database kept by the Department of National ID and Civil Registration. The aim is a trusted identity for service access, benefit transfers and financial inclusion, reducing duplicate and fake identities. *Design issues:* a single high-value database is a security and privacy risk (breach, misuse, function creep); exclusion of those who lack documents or whose fingerprints cannot be read; and the need for legal safeguards.

**Civil registration and the Nagarik App.** Vital events (birth, death, marriage, migration) are registered at the local level, and digital registration with online verification is being extended. The **Nagarik App** is the Government of Nepal's mobile application that gives citizens access to verified documents and services in one place (with identity verified through the National ID or other official credentials), so that a document shown on the phone can be verified by a service provider. It is an example of *citizen-centric integration* and a G2C front end.

**Government data centre and integration.** The **Government Integrated Data Centre (GIDC)** hosts government applications and a disaster-recovery site so that agencies do not each run their own server room; a **government cloud** and **interoperability framework** (agreed standards for exchanging data between systems) reduce duplicate systems. **Office systems** for digital file movement and decision tracking, such as the Government Integrated Office Management System (GIOMS) named in policy documents, aim to replace paper files with traceable electronic workflows. *Check the current rollout status; the learning point is the architecture: shared hosting, shared identity, shared standards.*

**Taxes, customs, procurement and payments.** The **Inland Revenue Department's** online taxpayer portal handles registration, returns (including VAT) and payment; customs uses an electronic clearance system; **e-procurement** through the **Public Procurement Monitoring Office's** portal publishes tenders and receives bids online, reducing collusion and increasing competition; and bill and fee payments run through the interbank and wallet networks described in *MIS and e-Business*. **Treasury** and budget systems (the Financial Management Information System) track spending across the three tiers.

**Local level (Palika) systems.** Since federalism, the 753 local governments hold most day-to-day citizen services: vital registration, recommendation letters, social security allowance, property and business tax. Municipal software handles registration, taxation and the **social security payment** list (with biometric or bank-account payment replacing cash distribution). Typical difficulties: different software in each Palika that cannot exchange data, thin IT staff, intermittent connectivity at ward offices, and dependence on external vendors.

| Service | Technology | Benefit | Typical weakness |
|---|---|---|---|
| Identity | National ID database | One trusted identity | Privacy and exclusion risk |
| Citizen services | Nagarik App | One place, verified documents | Needs a smartphone and ID |
| Hosting | GIDC, government cloud | Shared, secure infrastructure | Single point of failure unless replicated |
| Tax and customs | Online portals | Faster, traceable | Training of small businesses |
| Procurement | e-bidding portal | Transparency | Bid-rigging outside the system |
| Local government | Palika software | Services near citizens | Non-interoperable systems |

## 5.3 Digital signatures and PKI

Paper documents are authenticated by a handwritten signature and a stamp. An electronic document is only a file, easy to copy and alter; trust needs cryptography. A **digital signature** has three properties: **authentication** (it came from the signer), **integrity** (the document was not changed) and **non-repudiation** (the signer cannot credibly deny it). It combines a **hash** and **public-key cryptography**:

1. **Hash** the document with a one-way function (for example SHA-256) to produce a short fixed-size digest. Any change in the document changes the digest completely.
2. **Sign:** the signer encrypts (transforms) the digest with their **private key**.
3. **Verify:** anyone applies the signer's **public key** to the signature, obtaining a digest, and compares it with a digest freshly computed from the received document. If they match, the document is intact and the signer's private key was used.

To know that a public key *really belongs* to Sita and not an impostor, a **Certifying Authority (CA)** issues a **certificate**: a document, itself signed by the CA, that binds Sita's name to her public key. In Nepal the Controller of Certification licenses the CAs (Unit 4); a **PKI (public-key infrastructure)** is the whole system of keys, certificates, CAs, revocation lists and policies. Verification of a certificate follows the **chain of trust** from the user's certificate up to a trusted root.

The following program signs a message with a **toy RSA key** (about 20 bits, trivially breakable) so that every number can be followed; a real key has 2,048 bits or more and a padding scheme such as RSA-PSS.

```python
import hashlib
p, q = 1009, 1013
n = p * q
phi = (p - 1) * (q - 1)
e = 65537
d = pow(e, -1, phi)
def digest(msg):
    return int.from_bytes(hashlib.sha256(msg.encode()).digest(), "big") % n
doc = "Pay Rs 5,000 to Ram Bahadur"
h = digest(doc)
s = pow(h, d, n)
print("n =", n, " phi =", phi, " d =", d)
print("sha256 mod n =", h)
print("signature =", s)
print("verify original:", pow(s, e, n) == h)
forged = "Pay Rs 50,000 to Ram Bahadur"
print("verify forged :", pow(s, e, n) == digest(forged))
```
```output
n = 1022117  phi = 1020096  d = 832193
sha256 mod n = 563523
signature = 766706
verify original: True
verify forged : False
```
The signature checks against the original but not against the changed amount; with a real hash the chance of a forged document matching is negligible, while with this toy modulus a collision has probability about 1 in a million per attempt. The signing *speed* point: signing the short digest rather than the whole document is why digital signatures are practical.

## 5.4 Challenges and good practice

- **Digital divide and exclusion:** keep assisted channels; design for low-end phones and Nepali.
- **Security and resilience:** hardened systems, regular audits, backups and a disaster-recovery site; security of identity databases above all.
- **Interoperability:** open standards and APIs so that agencies share data instead of asking citizens for the same document repeatedly (*once-only principle*).
- **Privacy and legal basis:** data collected only for a stated purpose and protected by law (Unit 4).
- **Process reengineering:** simplify the procedure before digitising it.
- **Capacity and sustainability:** train staff, budget for maintenance, avoid vendor lock-in, publish open data.
- **Measure outcomes:** time, cost, complaints and corruption, not just the number of online forms.

## 5.5 Seeing the ideas: the front desks, the four models, the index, the savings and the signature

e-Governance is delivered at real counters. Plate 5.1 shows two of them, the gate of the Kathmandu Metropolitan City Office and a rural-municipality ward office, and the kind of cash machine that already connects ordinary people to digital payment rails. A service is only "online" when the counter, the network and the citizen's phone all work.

```photogrid label="5.1" cols="3" ratio="1.25" caption="Where governance meets the citizen. (a) The entrance of the Kathmandu Metropolitan City Office, Bagh Durbar: a local government that issues recommendations, registers vital events and collects taxes. (b) A ward office of a rural municipality: the nearest government counter for most Nepalis, often with thin staff and unstable connectivity. (c) A bank ATM in Nepal: payment infrastructure that e-government fees and allowances can ride on."
@ photo id="bca-st/kmc" cap="Metropolitan City Office"
fit 1.25
focus 0.5 0.5
@ photo id="bca-st/wardoffice" cap="Ward office"
fit 1.25
focus 0.5 0.55
@ photo id="bca101/atm-nepal" cap="Bank ATM"
fit 1.25
focus 0.5 0.5
```

```svgfig label="5.1" caption="The four interaction models of e-government. G2C faces people, G2B faces firms, G2G joins agencies and G2E serves the government's own staff. The examples are typical services, not a list of live systems."
f = Fig(580, 196)
c = [("G2C", "Government to Citizen", "certificates,\ntax filing,\nallowances", MINT, TEAL), ("G2B", "to Business", "company\nregistration,\ncustoms, bids", BLUE, NAVY), ("G2G", "between Agencies", "shared data,\ne-file movement,\ntreasury", SAND, AMBER), ("G2E", "to Employees", "payroll,\nleave, training\nrecords", ROSE, RED)]
f.circle(290, 98, 36, fill="#ffffff", stroke=SLATE, label="Govern-\nment", size=9.5)
pos = [(6, 6), (334, 6), (6, 108), (334, 108)]
for (a, b, s, fl, sk), (x, y) in zip(c, pos):
    f.box(x, y, 240, 82, a + " : " + b + "\n" + s, fill=fl, stroke=sk, size=10.2, bold=True)
```

```svgfig label="5.2" caption="Four stages of maturity (UN-style). Each stage adds a capability. Moving up needs back-office integration, not only a better website: stage 4 is impossible while each agency keeps its own isolated database."
f = Fig(580, 210)
s = [("1 Emerging", "information only:\noffice hours, notices", BLUE, NAVY), ("2 Enhanced", "two-way: download\nforms, e-mail queries", BLUE, NAVY), ("3 Transactional", "complete service and\nfee payment online", MINT, TEAL), ("4 Connected", "one request, many\nagencies, data shared", MINT, TEAL)]
for i, (t, d, fl, sk) in enumerate(s):
    x = 8 + i * 142; h = 50 + i * 28; y = 190 - h - 14
    f.box(x, y, 130, h + 14, "", fill=fl, stroke=sk)
    f.text(x + 65, y + 16, t, size=10.5, color=sk, bold=True)
    f.text(x + 65, y + 36, d, size=9.2, color=SLATE)
f.text(290, 204, "Example: office hours on a website = stage 1; birth registered online, fee paid by wallet, certificate verifiable = stage 3 or 4", size=9, color=RED, bold=True)
```

```svgfig label="5.3" caption="The EGDI-style index of section 5.1 (invented values). EGDI is the mean of the three components: (0.52 + 0.41 + 0.63) / 3 = 0.520. The weakest component, telecommunication infrastructure at 0.41, shows where investment should go first."
f = Fig(580, 168)
rows = [("Online Service Index (OSI)", 0.52, BLUE, NAVY), ("Telecom Infrastructure (TII)", 0.41, ROSE, RED), ("Human Capital (HCI)", 0.63, BLUE, NAVY), ("EGDI = mean of the three", 0.52, MINT, TEAL)]
for i, (n, v, fl, sk) in enumerate(rows):
    y = 12 + i * 36
    f.text(8, y + 14, n, size=10, color=NAVY, bold=True, anchor="start")
    f.box(220, y, v * 330, 24, "", fill=fl, stroke=sk)
    f.text(220 + v * 330 + 6, y + 13, "%.2f" % v, size=10.5, color=sk, bold=True, anchor="start")
f.line(220 + 0.52 * 330, 4, 220 + 0.52 * 330, 156, color=AMBER, dash=True)
f.text(290, 162, "dashed line = EGDI 0.52; TII is the only component below it by a wide margin", size=9.4, color=SLATE)
```

```svgfig label="5.4" caption="Citizen time saved by one online service, from section 5.1: 1,20,000 applicants avoid 2 visits of 3.5 hours at Rs 60 an hour. Benefit Rs 5,04,00,000, cost Rs 45,00,000, net Rs 4,59,00,000 (bars to scale in crore rupees). The benefit goes to citizens, the cost to the agency's budget."
f = Fig(580, 184)
sc = 320 / 5.04
def row(i, n, v, fl, sk, lab):
    y = 12 + i * 46
    f.text(8, y + 16, n, size=10.5, color=NAVY, bold=True, anchor="start")
    f.box(130, y, max(v * sc, 3), 30, "", fill=fl, stroke=sk)
    f.text(130 + v * sc + 8, y + 16, lab, size=10.5, color=sk, bold=True, anchor="start")
row(0, "Benefit", 5.04, MINT, TEAL, "Rs 5.04 crore")
row(1, "Cost a year", 0.45, ROSE, RED, "Rs 0.45 crore")
row(2, "Net benefit", 4.59, BLUE, NAVY, "Rs 4.59 crore")
f.text(290, 172, "benefit / cost = 5.04 / 0.45 = 11.2 to 1, if every applicant can really use the service", size=9.6, color=SLATE)
```

```svgfig label="5.5" caption="The toy RSA signature of section 5.3 with the real numbers printed by the program. The signer hashes the message (563523 after reduction mod n) and raises it to the private exponent d, giving 766706. The verifier raises the signature to e and compares with a fresh hash: true for the original, false for the forged amount."
f = Fig(580, 200)
f.box(6, 12, 150, 56, "Message\nPay Rs 5,000 to Ram", fill=SAND, stroke=AMBER, size=9.8, bold=True)
f.box(206, 12, 150, 56, "Hash (SHA-256 mod n)\nh = 563523", fill=BLUE, stroke=NAVY, size=9.8, bold=True)
f.box(406, 12, 168, 56, "Signature s = h^d mod n\ns = 766706", fill=MINT, stroke=TEAL, size=9.8, bold=True)
f.arrow([(156, 40), (206, 40)], color=SLATE); f.arrow([(356, 40), (406, 40)], color=SLATE, label="private d", lpos=(381, 30))
f.box(6, 104, 268, 46, "Verify original: s^e mod n = 563523\nequals fresh hash  =>  True", fill=MINT, stroke=TEAL, size=9.8, bold=True)
f.box(306, 104, 268, 46, "Verify forged (Rs 50,000): hash differs\ns^e mod n does not match  =>  False", fill=ROSE, stroke=RED, size=9.8, bold=True)
f.arrow([(490, 68), (490, 104)], color=SLATE, dash=True)
f.text(290, 176, "n = 1009 x 1013 = 1022117, e = 65537, d = 832193 (toy key; real keys have 2,048 bits or more)", size=9.4, color=SLATE)
```

### 5.5.1 Eight benefits of e-governance

1. **Faster services.** A citizen who used to wait days for a stamped paper can get a verified document in minutes. Fewer manual steps mean fewer delays. A recommendation letter requested through a ward system can be ready the same day.
2. **Lower cost for citizens.** Each avoided trip saves bus fare, lost wages and time, as the Rs 5,04,00,000 estimate shows. People in distant hill villages gain the most. The saving is real even when the agency's own budget does not change.
3. **Transparency.** An online tender portal publishes bids for everyone to see. Records with times and user names are hard to hide. Public procurement becomes easier to monitor and compare.
4. **Less corruption.** Fewer face-to-face contacts reduce the chance to ask for a small payment. A queue number, a fee receipt and a status page make the process traceable. Complaints can be tied to a record.
5. **Better data for planning.** Digital records show how many people apply, where and how long they wait. Planners can place staff and money where needs are highest. Social security lists with bank payment reduce ghost beneficiaries.
6. **Wider access.** A mobile service reaches people who cannot visit an office easily, such as migrant workers, the elderly and persons with disabilities. Apps like the Nagarik App put verified documents in a pocket. Access still needs a phone, a signal and some skill.
7. **Accountability and trust.** When a service has a published time limit and a digital log, officials can be held to it. Citizens see the status of their file. Trust grows when promises are visible and kept.
8. **Integration across agencies.** Shared identity and shared standards let agencies reuse data instead of asking for the same copy again and again. This is the once-only principle. It saves effort for the citizen and removes duplicate systems.

## Chapter summary

- e-Governance covers service delivery, transparency and participation; models are G2C, G2B, G2G and G2E; maturity runs from emerging to connected.
- EGDI-style indices average service, infrastructure and human-capital components; cost-benefit estimates should count citizens' time and access.
- Nepali building blocks: National ID, Nagarik App, GIDC and office systems, tax, customs and procurement portals, and Palika software.
- A digital signature hashes the document and transforms the digest with the private key; a CA's certificate binds the public key to the identity.
- Success depends on inclusion, security, interoperability, legal safeguards and reengineered processes.

## Practice

1. Differentiate e-government from e-governance and give examples of G2C, G2B, G2G and G2E.
2. Describe the four maturity stages.
3. With OSI = 0.60, TII = 0.30, HCI = 0.75, compute the EGDI. Which component should be improved first?
4. A service avoids 50,000 visits, each costing 4 hours at Rs 50 an hour. Compute the value of time saved.
5. List two benefits and two risks of a biometric National ID.
6. What does the Nagarik App do for a citizen?
7. Explain the three steps of signing and verifying a document.
8. What does a CA certificate prove?
9. Why does the signature program print "False" for the forged document?
10. State the "once-only principle" and why it needs interoperability.

::: note Answers and worked solutions
**1.** e-Government delivers services by ICT; e-governance also covers transparency and participation. G2C: online tax filing; G2B: company registration; G2G: shared data between agencies; G2E: payroll portal.
**2.** Emerging (information), enhanced (two-way interaction), transactional (full services with payment), connected (integrated across agencies).
**3.** (0.60 + 0.30 + 0.75)/3 = 1.65/3 = **0.55**; TII (0.30) is weakest, so improve infrastructure.
**4.** 50,000 × 4 × 50 = **Rs 1,00,00,000**.
**5.** Benefits: unique trusted identity; fewer fake or duplicate beneficiaries. Risks: breach of a central biometric database; exclusion of people whose prints cannot be read or who lack documents.
**6.** It provides verified documents and access to government services from one mobile application.
**7.** Hash the document; transform the digest with the private key (signature); the verifier applies the public key to the signature and compares with a fresh hash of the document.
**8.** That the named person (or organisation) holds the private key that matches the public key in the certificate, as vouched by the CA's own signature.
**9.** Changing the amount changes the SHA-256 digest, so the digest recovered from the signature no longer equals the new one.
**10.** Government should ask citizens for a given piece of data only once and reuse it; agencies can do that only if their systems can securely exchange the data.
:::


## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the four interaction models and the four maturity stages of e-government with Nepali examples.**

*Introduction.* e-Government is the use of ICT by government to deliver services and information. Two classifications describe it: who the service is for (models) and how advanced it is (stages) (section 5.1, Figures 5.1 and 5.2).

1. **G2C (government to citizen).** Certificates, tax filing and allowances, for example verified documents on the Nagarik App.
2. **G2B (government to business).** Company registration, customs clearance and e-procurement bids.
3. **G2G (government to government).** Data sharing and electronic file movement between agencies, hosted on shared infrastructure such as the Government Integrated Data Centre.
4. **G2E (government to employees).** Payroll, leave and training records of staff.

| Stage | Capability | Example |
|---|---|---|
| 1 Emerging | Information only | Website with office hours |
| 2 Enhanced | Two-way: forms, queries | Downloadable application form |
| 3 Transactional | Full service and payment | Online tax return with fee |
| 4 Connected | Integrated across agencies | One request, data reused |

*Remark.* Reaching stage 4 needs shared identity, shared standards and a simplified process, not only a nicer website.

*Conclusion.* Models show whom a service serves; stages show how far it has matured; good planning uses both.

**Q2 (5 marks). A country has OSI = 0.52, TII = 0.41 and HCI = 0.63. Compute its EGDI and say what policy follows. A service moves online for 1,20,000 applicants who each avoid 2 visits of 3.5 hours valued at Rs 60 an hour; it costs Rs 45,00,000 a year. Find the net benefit.**

*Introduction.* Indices and cost-benefit estimates turn e-government into numbers that can be compared (section 5.1, Figures 5.3 and 5.4).

*EGDI.* EGDI = (OSI + TII + HCI) / 3 = (0.52 + 0.41 + 0.63) / 3 = 1.56 / 3 = **0.520**.

*Policy.* The weakest component is TII at 0.41, so investment should go first to connectivity (fibre, towers, affordable data) rather than more online forms. Human capital is the strongest at 0.63.

*Cost-benefit.*

| Step | Calculation | Result |
|---|---|---|
| Visits avoided | 1,20,000 x 2 | 2,40,000 |
| Hours saved | 2,40,000 x 3.5 | 8,40,000 |
| Value | 8,40,000 x Rs 60 | Rs 5,04,00,000 |
| Net benefit | 5,04,00,000 - 45,00,000 | Rs 4,59,00,000 |

The benefit-cost ratio is 5.04 crore / 0.45 crore = **11.2**.

*Caution.* The benefit goes to citizens while the cost falls on the agency's budget, and the estimate assumes every applicant can use the service. An assisted channel is needed for those who cannot.

*Conclusion.* EGDI shows where to invest; the cost-benefit calculation shows why the project is worth funding.

**Q3 (10 marks). Describe e-governance in Nepal. Explain its concepts, the main building blocks, its benefits, the role of digital signatures and the main challenges, with suitable examples.**

*Introduction.* e-Governance uses ICT not only to deliver services but to improve how government works: transparency, participation and accountability. Nepal is building it on identity, shared hosting, integrated services and local-level systems (sections 5.1 to 5.5).

*Concepts.* Interaction models are G2C, G2B, G2G and G2E; maturity runs from emerging to connected (Figures 5.1, 5.2).

*Building blocks.* (1) **National ID**: a unique number linked to biometric data, kept by the Department of National ID and Civil Registration. (2) **Nagarik App**: verified documents and services on a phone, a G2C front end. (3) **GIDC and government cloud**: shared hosting and disaster recovery with agreed data-exchange standards. (4) **Tax, customs and procurement portals**: online returns, electronic clearance and e-bidding. (5) **Palika systems**: the 753 local governments that deliver most daily services.

| Block | Benefit | Typical weakness |
|---|---|---|
| National ID | One trusted identity | Privacy and exclusion |
| Nagarik App | Documents in one place | Needs smartphone and ID |
| GIDC | Shared secure hosting | Single point of failure |
| Procurement portal | Transparency | Bid-rigging outside system |
| Palika software | Services near people | Systems do not interoperate |

*Benefits.* Faster, cheaper and more transparent services, less corruption, better planning data, wider access, accountability and integration (section 5.5.1).

*Digital signatures.* A hash of the document is signed with the private key; anyone verifies with the public key, and a Certifying Authority licensed by the Controller of Certification binds the key to a name. A changed amount fails verification (Figure 5.5).

*Challenges.* Exclusion of the offline, security of high-value identity databases, non-interoperable systems, privacy and legal basis, digitising bad processes, thin staff and vendor lock-in.

*Conclusion.* Nepal's e-governance is moving from isolated websites toward shared identity and services, but its success depends on connectivity, security, privacy safeguards, simplified procedures and keeping an assisted channel for people who are offline.
