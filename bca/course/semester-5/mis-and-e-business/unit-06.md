---
subject: MIS and e-Business
grade: BCA Semester 5
unit: 6
title: Security and Control of Information Systems
hours: 4
area: BCA 304 · MIS and e-Business · Unit 6
---

A system that is fast, integrated and loved by users but loses a customer database to a stolen laptop has failed. Security is not an add-on; it is part of the definition of a usable information system. This unit covers the vocabulary of threats, a quantitative way to decide how much to spend on controls (annualised loss expectancy), password strength as entropy, the controls that protect e-commerce, and the legal frame in Nepal.

::: key What this unit gives you
- Confidentiality, integrity, availability; threats, vulnerabilities, risk and controls.
- Risk analysis: SLE, ARO, ALE and the cost-benefit of a safeguard.
- Password entropy numbers; e-commerce controls (TLS, payment verification, fraud rules).
- Disaster recovery, audit and the Electronic Transactions Act 2063 in outline.
:::

## 6.1 Security goals, threats and controls

The **CIA triad**: **confidentiality** (only authorised people read the data), **integrity** (data are accurate and unaltered) and **availability** (the system works when needed). Add **authenticity** and **non-repudiation** (a sender cannot deny sending). A **threat** is a potential cause of harm (a hacker, a fire, a careless employee); a **vulnerability** is a weakness (an unpatched server); **risk** is the chance a threat exploits a vulnerability times the impact; a **control** reduces risk.

| Threat | Example | Typical control |
|---|---|---|
| Malware | Ransomware encrypting the server | Patching, anti-malware, offline backups |
| Phishing and social engineering | Fake "bank" SMS asking for an OTP | Training, MFA, URL filtering |
| Insider misuse | Clerk altering account records | Role-based access, logs, segregation of duties |
| Denial of service | Flood against the booking website | Rate limiting, CDN, redundancy |
| Physical | Theft, fire, flood, power failure | Locks, UPS, generator, offsite copies |
| Application flaws | SQL injection, weak sessions | Secure coding, testing, WAF |

Controls fall into three families: **preventive** (stop it: access control, encryption, firewalls), **detective** (notice it: logs, alerts, audits) and **corrective** (recover: backups, incident response). They are further classified as **technical**, **administrative** (policies, training) and **physical**. Defence in depth layers several of them so that no single failure exposes the asset.

## 6.2 Quantitative risk analysis

Spending on security must be justified. The classic formulae:

- **Single loss expectancy (SLE)** = asset value (AV) × exposure factor (EF), the fraction of the asset lost in one incident.
- **Annualised rate of occurrence (ARO)**: expected incidents per year.
- **Annualised loss expectancy (ALE)** = SLE × ARO.

::: example Is the safeguard worth it?
A customer database is valued at Rs 20,00,000. A breach would destroy 40% of its value, so SLE = 20,00,000 × 0.4 = Rs **8,00,000**. Incidents are expected once in four years (ARO = 0.25), so ALE = **Rs 2,00,000** per year. A safeguard (encrypted backups, MFA, monitoring) costing Rs 70,000 per year cuts the ARO to 0.05, so the new ALE = 8,00,000 × 0.05 = **Rs 40,000**. Risk reduced by Rs 1,60,000; net benefit after paying for the control = 1,60,000 − 70,000 = **Rs 90,000** per year, a **129%** return on the security spend. The control is justified.
:::

The numbers are estimates, so analysts use ranges and compare options; the output is a priority list, not a precise forecast. Alternatives to reducing risk: **accept** it, **transfer** it (insurance), **avoid** it (stop the activity) or **mitigate** it (controls).

## 6.3 Authentication and password strength

Authentication proves identity with something you **know** (password), **have** (phone, token) or **are** (fingerprint); **multi-factor authentication (MFA)** combines at least two. The strength of a password scheme is its **entropy**: H = L × log₂(N) bits for L symbols chosen uniformly at random from an alphabet of N. A guesser needs on average half the space. At 10¹⁰ guesses per second (an offline attack against a weak hash):

| Password scheme | Space size | Entropy (bits) | Average time at 10¹⁰ guesses/s |
|---|---|---|---|
| 8 random lowercase letters | 2.09e+11 | 37.6 | 10.44 seconds |
| 8 random chars from 95 printable ASCII | 6.63e+15 | 52.6 | 3.8 days |
| 12 random lowercase letters | 9.54e+16 | 56.4 | 55.2 days |
| 4 random words from a 2,048-word list | 1.76e+13 | 44.0 | 14.7 minutes |
| 6 random words from a 2,048-word list | 7.38e+19 | 66.0 | 116.9 years |

An 8-character password from the full keyboard (52.6 bits) is weaker than 12 random lowercase letters (56.4 bits), and six random words (66 bits) is stronger than both and easier to remember. These figures assume *random* choice; human-chosen passwords (names plus birth year) have far less entropy, which is why systems must store passwords as **salted, slow hashes** (bcrypt, Argon2) and why a one-time password (OTP) from SMS or an authenticator app is added for payments.

## 6.4 Securing e-commerce

- **Transport security:** HTTPS (TLS) encrypts traffic between browser and server and authenticates the server by a certificate. Check for the padlock and a valid certificate; redirect all HTTP to HTTPS.
- **Do not store card data** you do not need; use a gateway so card numbers never touch your server (and the **PCI DSS** standard applies if you do).
- **Server-side payment verification:** after a gateway callback, confirm the transaction ID, amount, merchant and status through a back-channel call; compare the amount with the order total.
- **Fraud controls:** velocity checks (many orders from one device), address mismatch, OTP, blacklists, manual review of large orders, COD limits for new customers.
- **Application security:** parameterised SQL, output encoding, CSRF tokens, secure session cookies, rate limits, least-privilege database accounts.
- **Digital signatures and certificates** give integrity and non-repudiation (the cryptography is in *Cryptography and Network Security*).
- **Privacy:** collect only what you need, state the purpose, protect and delete data on request where the law requires.

## 6.5 Business continuity, audit and law

A **business continuity plan (BCP)** keeps critical functions running; a **disaster recovery plan (DRP)** restores the IT systems. Key numbers: **RPO** (recovery point objective: how much data you can afford to lose, e.g. 15 minutes) and **RTO** (recovery time objective: how long you can be down, e.g. 4 hours). They determine backup frequency and standby systems: a bank with an RPO near zero replicates to a **disaster recovery site** synchronously. Follow the **3-2-1 rule**: three copies, two media, one offsite (and test restoring them). **IS audit** examines controls: logs, access reviews, change management, and segregation of duties (no one person both creates and approves a payment).

In Nepal the **Electronic Transactions Act, 2063 (2008)** gives legal recognition to electronic records and digital signatures, establishes a Controller of Certification Authorities, and defines computer-related offences (unauthorised access, damage, publishing illegal material) with penalties; its provisions are covered in detail in *Society and Technology*. NRB issues an **IT guideline for banks and financial institutions** requiring policies, access control, audit trails and disaster recovery. Treat any incident as both a technical and a legal event: preserve logs, notify as required, and communicate honestly.

## Chapter summary

- Security aims at confidentiality, integrity and availability; controls are preventive, detective or corrective.
- ALE = AV × EF × ARO; a safeguard is justified when the ALE it removes exceeds its cost.
- Entropy L × log₂ N measures password strength; use MFA and salted slow hashes.
- E-commerce security relies on TLS, a gateway, server-side verification, fraud rules and secure code.
- RPO and RTO drive backup and recovery design; audit and the Electronic Transactions Act supply oversight and legal frame.

## Practice

1. Define CIA and give one threat to each.
2. Differentiate threat, vulnerability and risk.
3. A server worth Rs 10,00,000 has EF = 0.3 and ARO = 0.5. Compute ALE.
4. A control costing Rs 40,000 cuts that ALE by 60%. Is it worthwhile?
5. Compute the entropy of a 10-character random password over 62 symbols (letters and digits).
6. Why is a salted slow hash used for passwords?
7. List three steps that a merchant takes to verify a payment callback.
8. Explain RPO and RTO with an example.
9. State the 3-2-1 backup rule.
10. Why separate the duties of creating and approving a payment?

::: note Answers and worked solutions
**1.** Confidentiality (data theft), integrity (tampered records), availability (denial-of-service).
**2.** Threat: potential cause of harm. Vulnerability: weakness. Risk: likelihood times impact of a threat exploiting a weakness.
**3.** SLE = 10,00,000 × 0.3 = 3,00,000; ALE = 3,00,000 × 0.5 = **Rs 1,50,000**.
**4.** The control saves 0.6 × 1,50,000 = 90,000 per year, net 90,000 − 40,000 = **Rs 50,000**: worthwhile.
**5.** 10 × log₂ 62 = 10 × 5.954 = **59.5 bits**.
**6.** Salt defeats pre-computed tables and makes equal passwords hash differently; a slow hash makes each guess expensive for an attacker.
**7.** Check the transaction ID and status by a server-to-server call; compare amount and currency with the order; ensure each ID is used for one order only.
**8.** RPO is the tolerated data loss (15 minutes means backups or replication at least every 15 minutes); RTO is the tolerated downtime (4 hours means a restore plan that completes within that time).
**9.** Three copies, on two media, one offsite.
**10.** One person acting alone could commit fraud; two people must collude, which is harder to hide.
:::
