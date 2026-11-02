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
