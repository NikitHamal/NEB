---
subject: MIS and e-Business
grade: BCA Semester 5
unit: 8
title: Security and Control of Information Systems
hours: 4
area: BCA 304 · MIS and e-Business · Unit 8
---

A system that is fast, integrated and loved by users but loses a customer database to a stolen laptop has failed. Security is not an add-on; it is part of the definition of a usable information system. This unit covers the vocabulary of threats, a quantitative way to decide how much to spend on controls (annualised loss expectancy), password strength as entropy, the controls that protect e-commerce, and the legal frame in Nepal.

::: key What this unit gives you
- Confidentiality, integrity, availability; threats, vulnerabilities, risk and controls.
- Risk analysis: SLE, ARO, ALE and the cost-benefit of a safeguard.
- Password entropy numbers; e-commerce controls (TLS, payment verification, fraud rules).
- Disaster recovery, audit and the Electronic Transactions Act 2063 in outline.
:::

## 8.1 Security goals, threats and controls

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

## 8.2 Quantitative risk analysis

Spending on security must be justified. The classic formulae:

- **Single loss expectancy (SLE)** = asset value (AV) × exposure factor (EF), the fraction of the asset lost in one incident.
- **Annualised rate of occurrence (ARO)**: expected incidents per year.
- **Annualised loss expectancy (ALE)** = SLE × ARO.

::: example Is the safeguard worth it?
A customer database is valued at Rs 20,00,000. A breach would destroy 40% of its value, so SLE = 20,00,000 × 0.4 = Rs **8,00,000**. Incidents are expected once in four years (ARO = 0.25), so ALE = **Rs 2,00,000** per year. A safeguard (encrypted backups, MFA, monitoring) costing Rs 70,000 per year cuts the ARO to 0.05, so the new ALE = 8,00,000 × 0.05 = **Rs 40,000**. Risk reduced by Rs 1,60,000; net benefit after paying for the control = 1,60,000 − 70,000 = **Rs 90,000** per year, a **129%** return on the security spend. The control is justified.
:::

The numbers are estimates, so analysts use ranges and compare options; the output is a priority list, not a precise forecast. Alternatives to reducing risk: **accept** it, **transfer** it (insurance), **avoid** it (stop the activity) or **mitigate** it (controls).

## 8.3 Authentication and password strength

Authentication proves identity with something you **know** (password), **have** (phone, token) or **are** (fingerprint); **multi-factor authentication (MFA)** combines at least two. The strength of a password scheme is its **entropy**: H = L × log₂(N) bits for L symbols chosen uniformly at random from an alphabet of N. A guesser needs on average half the space. At 10¹⁰ guesses per second (an offline attack against a weak hash):

| Password scheme | Space size | Entropy (bits) | Average time at 10¹⁰ guesses/s |
|---|---|---|---|
| 8 random lowercase letters | 2.09e+11 | 37.6 | 10.44 seconds |
| 8 random chars from 95 printable ASCII | 6.63e+15 | 52.6 | 3.8 days |
| 12 random lowercase letters | 9.54e+16 | 56.4 | 55.2 days |
| 4 random words from a 2,048-word list | 1.76e+13 | 44.0 | 14.7 minutes |
| 6 random words from a 2,048-word list | 7.38e+19 | 66.0 | 116.9 years |

An 8-character password from the full keyboard (52.6 bits) is weaker than 12 random lowercase letters (56.4 bits), and six random words (66 bits) is stronger than both and easier to remember. These figures assume *random* choice; human-chosen passwords (names plus birth year) have far less entropy, which is why systems must store passwords as **salted, slow hashes** (bcrypt, Argon2) and why a one-time password (OTP) from SMS or an authenticator app is added for payments.

## 8.4 Securing e-commerce

- **Transport security:** HTTPS (TLS) encrypts traffic between browser and server and authenticates the server by a certificate. Check for the padlock and a valid certificate; redirect all HTTP to HTTPS.
- **Do not store card data** you do not need; use a gateway so card numbers never touch your server (and the **PCI DSS** standard applies if you do).
- **Server-side payment verification:** after a gateway callback, confirm the transaction ID, amount, merchant and status through a back-channel call; compare the amount with the order total.
- **Fraud controls:** velocity checks (many orders from one device), address mismatch, OTP, blacklists, manual review of large orders, COD limits for new customers.
- **Application security:** parameterised SQL, output encoding, CSRF tokens, secure session cookies, rate limits, least-privilege database accounts.
- **Digital signatures and certificates** give integrity and non-repudiation (the cryptography is in *Cryptography and Network Security*).
- **Privacy:** collect only what you need, state the purpose, protect and delete data on request where the law requires.

## 8.5 Business continuity, audit and law

A **business continuity plan (BCP)** keeps critical functions running; a **disaster recovery plan (DRP)** restores the IT systems. Key numbers: **RPO** (recovery point objective: how much data you can afford to lose, e.g. 15 minutes) and **RTO** (recovery time objective: how long you can be down, e.g. 4 hours). They determine backup frequency and standby systems: a bank with an RPO near zero replicates to a **disaster recovery site** synchronously. Follow the **3-2-1 rule**: three copies, two media, one offsite (and test restoring them). **IS audit** examines controls: logs, access reviews, change management, and segregation of duties (no one person both creates and approves a payment).

In Nepal the **Electronic Transactions Act, 2063 (2008)** gives legal recognition to electronic records and digital signatures, establishes a Controller of Certification Authorities, and defines computer-related offences (unauthorised access, damage, publishing illegal material) with penalties; its provisions are covered in detail in *Society and Technology*. NRB issues an **IT guideline for banks and financial institutions** requiring policies, access control, audit trails and disaster recovery. Treat any incident as both a technical and a legal event: preserve logs, notify as required, and communicate honestly.

## 8.6 E-commerce security terminology and requirements

Security work begins with exact words.

| Term | Meaning |
|---|---|
| **Asset** | Anything of value: customer data, the website, payment records, brand reputation |
| **Vulnerability** | A weakness that can be exploited, such as an unpatched server or a weak password |
| **Threat** | A possible cause of harm |
| **Exploit** | A method or tool that uses a vulnerability |
| **Attack** | A deliberate attempt to harm an asset; the person is the **attacker** |
| **Risk** | Likelihood of an attack succeeding multiplied by its impact |
| **Zero-day** | A vulnerability that is exploited before a fix exists |
| **Countermeasure (control)** | Anything that reduces risk |

**Types of attacker.** *Hackers* is a wide word: **white-hat** hackers test systems with permission, **black-hat** hackers attack for gain or harm, and **grey-hat** hackers act without permission but without harmful intent. *Script kiddies* run ready-made tools without understanding them. *Insiders* are employees or contractors with legitimate access and cause a large share of losses. *Organised criminals* run fraud and ransomware for profit, *hacktivists* attack for a cause and *state-sponsored* groups attack for espionage or sabotage.

### The six security requirements

| Requirement | Question it answers | Typical mechanism |
|---|---|---|
| **Confidentiality** | Can only authorised people read it? | Encryption, access control |
| **Integrity** | Is it unaltered? | Hashes, digital signatures, checksums |
| **Availability** | Is the service there when needed? | Redundancy, backups, DDoS protection |
| **Authentication** | Who are you really? | Passwords, OTP, biometrics, digital certificates |
| **Authorisation** | What are you allowed to do? | Roles, permissions, least privilege |
| **Non-repudiation** | Can you deny doing it? | Digital signature, signed logs, receipts |

The first three are the **CIA triad**; the last three are often grouped as **AAA** (authentication, authorisation and accounting or audit). Example: when a customer pays, the shop authenticates the user with an OTP, authorises the payment against the balance, keeps confidentiality by TLS, ensures integrity with the signed gateway response and keeps a logged receipt so that neither side can later deny the transaction.

## 8.7 Technical attacks

**Technical attacks** use software and network weaknesses.

### Malware: viruses, worms and Trojan horses

**Malware** is software designed to harm. A **virus** attaches itself to a file or program and spreads when the host is run or shared; it needs a user action. A **worm** is self-contained and spreads across networks on its own, often exploiting a flaw, so it can infect thousands of machines quickly. A **Trojan horse** pretends to be useful (a free game, a cracked tool) while doing something harmful, such as opening a backdoor; it does not copy itself. Other kinds are **spyware**, **keyloggers**, **adware**, **rootkits** and **ransomware**.

**Ransomware** encrypts a victim's files and demands payment, usually in cryptocurrency, for the key. The 2013 **CryptoLocker** attack (written "CryptoBlocker" in some syllabus lists) popularised the method. Best protection: offline backups, patching, mail filtering and staff training; paying the ransom does not guarantee recovery.

### Heartbleed

**Heartbleed** (CVE-2014-0160, disclosed in April 2014) was a flaw in the **OpenSSL** library's "heartbeat" extension, which lets one side check that the other is alive. The code did not check the length a client claimed, so a client could ask for up to 64 KB of the server's memory in each reply. That memory could contain **private keys, session cookies and passwords**. Nothing in the logs showed it. Roughly half a million secure web servers, about 17 percent of those on the Internet, were reported vulnerable before the fix (OpenSSL 1.0.1g). Lesson: fix, then revoke and reissue certificates and reset passwords, because the old ones may have leaked.

::: example How much can Heartbleed leak?
Each malicious request returns up to 64 KB (65,535 bytes). A script making 1,000 requests collects 1,000 × 64 KB = 64,000 KB, about **64 MB** of memory contents, in seconds, without logging in.
:::

### Denial of service and botnets

A **denial-of-service (DoS)** attack makes a service unavailable by flooding it with requests or exploiting a flaw. In a **distributed DoS (DDoS)** the traffic comes from thousands of machines. These are usually part of a **botnet**: computers, phones or IoT cameras infected with malware (**bots** or **zombies**) and controlled by an attacker through a **command-and-control (C&C)** server. The Mirai botnet of 2016 used default-password cameras and routers to produce traffic of hundreds of Gbps. Types: volumetric (fill the bandwidth), protocol (exhaust server tables, for example SYN floods) and application-layer (many costly requests to a search or login page).

::: example Why DDoS works
A shop's link carries 1 Gbps. A botnet of 10,000 devices each sending 1 Mbps produces 10 Gbps, ten times the capacity. Only about 1 in 10 packets can pass, so roughly **90 percent** of requests, including genuine customers, are lost. Defences: a CDN or scrubbing service that absorbs traffic, rate limiting, upstream filtering by the ISP and spare capacity.
:::

```svgfig label="8.1" caption="A DDoS attack. The attacker controls a command-and-control server, which instructs thousands of infected devices (bots). Each bot sends a small amount of traffic, but together they send ten times the capacity of the shop's 1 Gbps link, so genuine customers cannot get through. A CDN or scrubbing service in front of the shop filters the flood."
f = Fig(580, 200)
f.box(10, 76, 90, 44, "Attacker", fill=ROSE, stroke=RED, size=11, bold=True, color=RED, r=5)
f.box(130, 76, 100, 44, "C&C server", fill=SAND, stroke=AMBER, size=11, bold=True, color=AMBER, r=5)
f.arrow([(100, 98), (130, 98)], color=RED)
for i in range(4):
    y = 14 + i * 46
    f.box(270, y, 80, 32, "Bot " + str(i + 1), fill=SOFT, stroke=SLATE, size=10.5, bold=True, color=SLATE, r=4)
    f.arrow([(230, 98), (270, y + 16)], color=AMBER)
    f.arrow([(350, y + 16), (440, 98)], color=RED)
f.text(310, 196, "10,000 bots x 1 Mbps = 10 Gbps", size=10.5, color=RED, bold=True)
f.box(440, 70, 130, 56, "Shop\nlink 1 Gbps", fill=BLUE, stroke=NAVY, size=11, bold=True, color=NAVY, r=5)
```

### Other technical attacks

| Attack | How it works | Defence |
|---|---|---|
| **Sniffing** | A tool captures packets on a shared or wireless network and reads unencrypted data | TLS, VPN, switched networks |
| **Page hijacking (pagejacking)** | The attacker copies a popular page, gets it indexed, and redirects visitors to a fake or malicious site | Monitor your brand in search, report copies, use HTTPS and canonical tags |
| **Malvertising** | Malicious code is placed in an advertisement served on a legitimate site; a click, or just a view, may install malware | Ad-network vetting, ad blockers, patched browsers |
| **SQL injection** | User input changes a database query | Parameterised queries, input validation |
| **Cross-site scripting (XSS)** | A script planted in a page runs in other users' browsers | Output encoding, content security policy |
| **Man-in-the-middle** | The attacker relays and alters messages | TLS with certificate checks |
| **Brute force and credential stuffing** | Many guesses, or leaked passwords tried on other sites | MFA, lockout, unique passwords |

## 8.8 Non-technical attacks and fraud

**Non-technical attacks** target people and processes. **Social engineering** persuades someone to give access or information.

| Form | Description |
|---|---|
| **Phishing** | Mass fake emails, SMS or web pages that imitate a bank or shop to steal logins and OTPs |
| **Spear phishing and whaling** | Targeted messages to one person, or to a senior executive |
| **Vishing and smishing** | Voice-call and SMS versions |
| **Pretexting** | An invented story ("I am from IT, tell me your password") |
| **Baiting** | A tempting object, such as an infected USB drive left in a car park |
| **Tailgating and shoulder surfing** | Following someone through a door; watching a PIN being typed |
| **Insider abuse** | A staff member sells data or alters accounts |

**Common e-commerce frauds.** *Identity theft* (using another person's details to open accounts or buy), *card-not-present fraud* with stolen numbers, *fake online shops* that take payment and never deliver, *friendly fraud* (a buyer receives goods and then disputes the charge), *advance-fee scams* (a promised prize in return for a fee), *click fraud* (bots or workers click ads to waste the advertiser's budget) and *account takeover*.

**Protection.** For customers: check the address, never share an OTP, use unique passwords with MFA and prefer known shops. For merchants: address and security-code checks, 3-D Secure, limits on orders from new accounts, manual review of high-risk orders, fraud scoring from the gateway, and clear refund and dispute processes. For staff: awareness training and simulated phishing, a rule that no one asks for a password by phone or email, and separation of duties for payments.

```svgfig label="8.2" caption="A taxonomy of e-commerce attacks. Technical attacks (malware, ransomware, Heartbleed-type flaws, DDoS and botnets, sniffing, page hijacking, malvertising, injection) exploit software and networks. Non-technical attacks (phishing, pretexting, baiting, insider abuse and fraud) exploit people and process. Most real incidents combine both: a phishing email installs ransomware."
f = Fig(580, 200)
f.box(220, 6, 140, 34, "E-commerce attacks", fill=BLUE, stroke=NAVY, size=12, bold=True, color=NAVY, r=5)
f.box(20, 70, 250, 30, "Technical", fill=MINT, stroke=TEAL, size=12, bold=True, color=TEAL, r=5)
f.box(310, 70, 250, 30, "Non-technical", fill=SAND, stroke=AMBER, size=12, bold=True, color=AMBER, r=5)
f.arrow([(260, 40), (145, 70)], color=SLATE); f.arrow([(320, 40), (435, 70)], color=SLATE)
t = ["Malware, worms, Trojans", "Ransomware, Heartbleed", "DDoS and botnets", "Sniffing, page hijacking", "Malvertising, injection"]
n = ["Phishing and spear phishing", "Pretexting, baiting", "Insider abuse", "Identity theft, card fraud", "Fake shops, friendly fraud"]
for i in range(5):
    y = 108 + i * 18
    f.text(30, y + 8, t[i], size=10.5, color=SLATE, bold=True, anchor="start")
    f.text(320, y + 8, n[i], size=10.5, color=SLATE, bold=True, anchor="start")
```

## 8.9 Seeing security: factors, risk arithmetic, entropy and recovery

Security decisions are built on three questions: who is it, how likely is the loss, and how fast can we recover. The plate shows the three kinds of proof of identity; the figures put numbers to risk, passwords and recovery.

```photogrid label="8.1" cols="3" ratio="1.0" caption="Three factors of authentication. (a) Something you are: a fingerprint sensor reads a biometric. (b) Something you have: a hardware security key such as the YubiKey proves possession of a device. (c) Something you know: a password or PIN; a password alone is the weakest factor because it can be guessed or stolen. Multi-factor authentication combines at least two different kinds, so a stolen password alone does not open the account."
@ photo id="bca401/fingerprint" cap="Are: fingerprint sensor"
fit 1.0
focus 0.5 0.5
@ photo id="bca401/yubikey" cap="Have: security key"
fit 1.0
focus 0.5 0.5
@ svg cap="Know: the password"
f = Fig(300, 300)
f.box(30, 40, 240, 46, "Username", fill=SOFT, stroke=SLATE, size=13, bold=True, color=SLATE)
f.box(30, 100, 240, 46, "Password  ********", fill=SOFT, stroke=SLATE, size=13, bold=True, color=SLATE)
f.box(30, 164, 110, 40, "Log in", fill=MINT, stroke=TEAL, size=13, bold=True)
f.text(150, 240, "Weakest factor:", size=13, color=RED, bold=True)
f.text(150, 262, "guessed, phished, reused", size=13, color=RED, bold=True)
```

```svgfig label="8.3" caption="The CIA triad and some threats to each goal. Confidentiality means only authorised people see the data (threats: phishing, eavesdropping, theft of a laptop; controls: encryption, access control). Integrity means data is correct and unaltered (threats: tampering, malware, mistakes; controls: hashes, digital signatures, audit trails). Availability means systems work when needed (threats: denial of service, power failure, ransomware; controls: backups, redundancy, firewalls). Every control in the unit protects at least one of these three goals."
f = Fig(580, 200)
f.poly([(290, 8), (400, 160), (180, 160)], fill=BLUE, stroke=NAVY, sw=1.6)
f.text(290, 70, "Information", size=11, color=NAVY, bold=True); f.text(290, 88, "security", size=11, color=NAVY, bold=True)
g = [("Confidentiality", 20, 20, "phishing, theft\nencryption, access control", TEAL, MINT), ("Integrity", 410, 20, "tampering, malware\nhashes, signatures", AMBER, SAND), ("Availability", 215, 168, "DoS, power cut, ransomware\nbackups, redundancy", RED, ROSE)]
f.box(10, 14, 190, 54, "", fill=MINT, stroke=TEAL); f.text(105, 30, "Confidentiality", size=11, color=TEAL, bold=True); f.text(105, 48, "phishing, theft: encryption", size=9.5, color=SLATE, bold=True)
f.box(380, 14, 190, 54, "", fill=SAND, stroke=AMBER); f.text(475, 30, "Integrity", size=11, color=AMBER, bold=True); f.text(475, 48, "tampering: hashes, signatures", size=9.5, color=SLATE, bold=True)
f.box(180, 168, 220, 28, "Availability: DoS, ransomware: backups", fill=ROSE, stroke=RED, size=9.5, bold=True)
```

```svgfig label="8.4" caption="Is the safeguard worth it? A customer database worth Rs 20,00,000 loses 40 percent in a breach, so SLE = 20,00,000 x 0.4 = Rs 8,00,000. With one incident in four years (ARO 0.25) the ALE is Rs 2,00,000. A safeguard costing Rs 70,000 a year cuts ARO to 0.05, so the new ALE is 8,00,000 x 0.05 = Rs 40,000. Risk reduction is 2,00,000 - 40,000 = Rs 1,60,000, and the net benefit after the cost is 1,60,000 - 70,000 = Rs 90,000 a year, so the safeguard is worth buying."
f = Fig(580, 170)
f.text(10, 28, "ALE before", size=10.5, color=SLATE, bold=True, anchor="start"); f.box(110, 12, 200000 / 500, 28, "Rs 2,00,000", fill=ROSE, stroke=RED, color=RED, size=10.5, bold=True, r=3)
f.text(10, 68, "ALE after", size=10.5, color=SLATE, bold=True, anchor="start"); f.box(110, 52, 40000 / 500, 28, "", fill=MINT, stroke=TEAL, r=3); f.text(110 + 40000 / 500 + 6, 66, "Rs 40,000", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(10, 108, "Safeguard", size=10.5, color=SLATE, bold=True, anchor="start"); f.box(110, 92, 70000 / 500, 28, "", fill=SAND, stroke=AMBER, r=3); f.text(110 + 70000 / 500 + 6, 106, "Rs 70,000 per year", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(290, 150, "Net benefit = 1,60,000 - 70,000 = Rs 90,000 per year", size=11.5, color=NAVY, bold=True)
```

```svgfig label="8.5" caption="Password strength as entropy, H = L x log2(N) bits. Eight random lowercase letters give 37.6 bits (about 10 seconds on average at 10 billion guesses a second); eight random printable characters 52.6 bits (3.8 days); twelve random lowercase letters 56.4 bits (55 days); four random words from a 2,048-word list 44.0 bits (15 minutes); six random words 66.0 bits (about 117 years). Each extra bit doubles the work, so six random words are stronger than a complicated eight-character password and easier to remember, but only if the words are chosen at random, not by a person."
f = Fig(580, 200)
dt = [("8 random lowercase", 37.6, RED, ROSE), ("4 random words", 44.0, AMBER, SAND), ("8 random printable", 52.6, AMBER, SAND), ("12 random lowercase", 56.4, TEAL, MINT), ("6 random words", 66.0, TEAL, MINT)]
for i, (n, h, c, fl) in enumerate(dt):
    y = 8 + i * 37
    f.text(10, y + 17, n, size=10.5, color=SLATE, bold=True, anchor="start")
    f.box(160, y, h * 6.2, 28, f"{h} bits", fill=fl, stroke=c, color=c, size=11, bold=True, r=3)
```

```svgfig label="8.6" caption="Recovery objectives on a timeline. A shop takes a backup every night at 02:00. The server fails at 15:00, so up to 13 hours of transactions since the last backup are lost: the recovery point objective (RPO) actually achieved is 13 hours. If the restore takes 4 hours the service returns at 19:00 and the recovery time objective (RTO) achieved is 4 hours. To lower the RPO, back up more often or replicate continuously; to lower the RTO, keep a standby system ready. Both targets are business decisions set by how much a lost hour costs."
f = Fig(580, 150)
f.line(30, 80, 560, 80, color=SLATE)
for t, x, c, lab in [("02:00", 60, TEAL, "last backup"), ("15:00", 330, RED, "failure"), ("19:00", 480, NAVY, "service restored")]:
    f.circle(x, 80, 6, fill=c, stroke=c); f.text(x, 100, t, size=10.5, color=c, bold=True); f.text(x, 116, lab, size=10, color=SLATE, bold=True)
f.arrow([(330, 56), (60, 56)], color=RED, label="data lost: RPO 13 h", lpos=(195, 44))
f.arrow([(330, 36), (480, 36)], color=NAVY, label="downtime: RTO 4 h", lpos=(405, 24)) if False else None
f.arrow([(330, 60), (480, 60)], color=NAVY, label="downtime: RTO 4 h", lpos=(405, 48))
```

### 8.9.1 Eight good security practices for an e-business

1. **Use multi-factor authentication.** Ask for a password and a second factor such as a one-time code or a security key. A stolen password alone then cannot open the account. Banks and wallets in Nepal send an OTP for this purpose.
2. **Encrypt data in transit and at rest.** Use HTTPS for every page and encrypt databases and backups. A lost laptop or stolen backup tape then exposes nothing readable. Encryption is cheap compared with the loss from a leak.
3. **Store passwords as salted slow hashes.** Never keep passwords in plain text; use bcrypt or Argon2 with a unique salt. If the database is stolen the passwords are still hard to recover. This protects users who reuse passwords on other sites.
4. **Patch and update quickly.** Install security updates for the operating system, the web server and libraries. Most attacks use known weaknesses that have fixes. A shop that delays updates for months is an easy target.
5. **Give least privilege.** Each person and program gets only the access needed for the work. A cashier cannot change prices and a report tool cannot delete records. This limits damage from mistakes and insiders.
6. **Back up and test recovery.** Keep copies offline or in a separate location and test that the restore works. Define the RPO and RTO, as in Figure 8.6. A backup never tested is only a hope.
7. **Train people.** Phishing and weak habits are the most common cause of breaches. Teach staff to check links, report suspicious email and use a password manager. A short drill each year is far cheaper than a breach.
8. **Monitor, log and plan the response.** Keep logs, watch for unusual activity and have a written incident plan with named contacts. Report serious incidents as the law requires. Fast response reduces the damage and the loss of trust.

## Chapter summary

- Security aims at confidentiality, integrity and availability; controls are preventive, detective or corrective.
- ALE = AV × EF × ARO; a safeguard is justified when the ALE it removes exceeds its cost.
- Entropy L × log₂ N measures password strength; use MFA and salted slow hashes.
- E-commerce security relies on TLS, a gateway, server-side verification, fraud rules and secure code.
- RPO and RTO drive backup and recovery design; audit and the Electronic Transactions Act supply oversight and legal frame.
- Security requirements are confidentiality, integrity, availability, authentication, authorisation and non-repudiation.
- Technical attacks: viruses, worms, Trojans, ransomware (CryptoLocker), Heartbleed, DDoS and botnets, sniffing, page hijacking, malvertising and injection; non-technical attacks are social engineering (phishing, pretexting, baiting), insider abuse and fraud.

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
11. Differentiate a virus, a worm and a Trojan horse.
12. What was Heartbleed and what had to be done after it was disclosed?
13. A botnet of 5,000 devices each sends 2 Mbps to a 1 Gbps link. What fraction of the traffic can pass?
14. Differentiate authentication, authorisation and non-repudiation with one example each.
15. Explain page hijacking, malvertising and sniffing in one line each, with a defence.
16. List four forms of social engineering and four protections.

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
**11.** A virus attaches to a host file and needs a user action to spread; a worm spreads by itself across networks; a Trojan horse pretends to be useful and does not copy itself.
**12.** A flaw in OpenSSL's heartbeat feature let a client read up to 64 KB of server memory per request, possibly keys and passwords. Fix: upgrade OpenSSL, revoke and reissue certificates, reset passwords.
**13.** Offered load = 5,000 × 2 Mbps = 10,000 Mbps = 10 Gbps. Capacity 1 Gbps, so **10 percent** passes and 90 percent is dropped.
**14.** Authentication: proving who you are (OTP). Authorisation: what you may do (a cashier cannot change prices). Non-repudiation: cannot deny an action (digitally signed order).
**15.** Page hijacking: a copied page redirects visitors to a fake site (monitor search results). Malvertising: malware in an ad (ad vetting, updated browsers). Sniffing: capturing packets (TLS, VPN).
**16.** Phishing, pretexting, baiting, tailgating or vishing. Protection: check links, never share OTPs, training and simulated phishing, and separation of duties.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). A customer database worth Rs 20,00,000 would lose 40 percent of its value in a breach, expected once in four years. A safeguard costing Rs 70,000 a year reduces the rate to once in twenty years. Is it worth buying?**

*Introduction.* Quantitative risk analysis compares the expected annual loss with and without a safeguard (section 8.2, Figure 8.4).

1. **SLE.** Asset value x exposure factor = 20,00,000 x 0.4 = **Rs 8,00,000**.
2. **ALE before.** ARO = 1/4 = 0.25, so ALE = 8,00,000 x 0.25 = **Rs 2,00,000** a year.
3. **ALE after.** ARO = 1/20 = 0.05, so ALE = 8,00,000 x 0.05 = **Rs 40,000**.
4. **Risk reduction.** 2,00,000 - 40,000 = Rs 1,60,000 a year.
5. **Net benefit.** 1,60,000 - 70,000 = **Rs 90,000** a year.
6. **Decision.** The benefit is greater than the cost, so the safeguard is worth buying. Other responses are accept, transfer (insurance), avoid or mitigate.

*Conclusion.* The calculation shows the safeguard returns more than it costs, but the inputs are estimates, so ranges should be tested.

**Q2 (5 marks). Define password entropy. Compare 8 random lowercase letters, 8 random printable characters and 6 random words from a list of 2,048 words.**

*Introduction.* Entropy measures how unpredictable a randomly chosen password is; each additional bit doubles the number of guesses needed (section 8.3, Figure 8.5).

1. **Formula.** H = L x log2(N), where L is the number of symbols and N the size of the alphabet.
2. **8 lowercase letters.** 8 x log2(26) = 8 x 4.70 = **37.6 bits**, about 2.09 x 10^11 combinations.
3. **8 printable characters.** 8 x log2(95) = 8 x 6.57 = **52.6 bits**, about 6.63 x 10^15.
4. **6 random words.** 6 x log2(2048) = 6 x 11 = **66 bits**, about 7.4 x 10^19.
5. **Time.** At 10^10 guesses a second, on average half the space is searched: about 10 seconds, 3.8 days and 117 years respectively.
6. **Conclusion for users.** Random words beat short complex passwords and are easier to remember, but human-chosen passwords have far less entropy than these figures, so systems also need MFA and slow hashing.

*Conclusion.* Length and true randomness matter more than complicated character rules.

**Q3 (10 marks). Explain the security threats to information systems and e-commerce and the controls used against them. Describe authentication, encryption, and business continuity measures.**

*Introduction.* Information systems hold the money, records and reputation of an organisation, so their protection is a management duty and not only a technical task. Security aims to protect confidentiality, integrity and availability (the CIA triad) against threats from outside and inside (sections 6.1 to 6.5, Figures 6.1 to 6.4).

1. **Threats.** Malware and ransomware, phishing and social engineering, hacking and denial of service, insider misuse, theft or loss of devices, and natural disasters or power failure.
2. **Risk analysis.** SLE = asset value x exposure factor, ALE = SLE x ARO; compare the ALE reduction with the cost of the control.
3. **Authentication.** Something you know, have or are; MFA combines at least two. Passwords must be long and random and stored as salted slow hashes.
4. **Access control.** Least privilege, role-based access and logs of who did what.
5. **Encryption.** Symmetric encryption (AES) for bulk data; asymmetric encryption and digital signatures for key exchange and proof of origin; TLS secures web traffic and padlock-protected payment pages.
6. **Network controls.** Firewalls, intrusion detection, patching and segmented networks.
7. **Business continuity.** Backups, disaster recovery sites, and defined RPO and RTO; tested plans, as in Figure 8.6.
8. **Audit and law.** Regular audits and logs, and compliance with the Electronic Transactions Act, 2063 (2008) and bank rules.

| Goal | Threat | Control |
|---|---|---|
| Confidentiality | Phishing, theft | Encryption, MFA |
| Integrity | Tampering, malware | Hashes, signatures, audit trail |
| Availability | DoS, ransomware | Backups, redundancy |

*Conclusion.* Security is a layered, risk-based process: identify the threats, estimate the loss, choose controls whose cost is below the risk reduction and test recovery. A technical control without trained people and tested backups is not enough.
