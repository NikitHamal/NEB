---
subject: Society and Technology
grade: BCA Semester 5
unit: 4
title: Cyber and IT Law in Nepal
hours: 8
area: BCA 305 · Society and Technology · Unit 4
---

A student in Butwal posts an edited photo of a classmate with an insulting caption; a clerk uses a colleague's password to change a record; a company copies a competitor's source code; a shop owner sends a "bank officer" message to collect an OTP. Each act is harmful, and each fits somewhere in Nepal's legal framework. This unit explains the main statutes, concentrating on the **Electronic Transactions Act, 2063 (2008)**, then summarises privacy, copyright and the cyber security policy. It is a study of the law *as it affects computing professionals*; it is not legal advice, and statutes are amended, so the current text must always be checked.

::: key What this unit gives you
- Why law lags technology, and the Nepali sources of cyber law.
- The Electronic Transactions Act 2063: recognition of electronic records and signatures, certifying authorities, offences and penalties (tabulated).
- The Individual Privacy Act 2075, the Copyright Act 2059, the Muluki Criminal Code 2074 and the National Cyber Security Policy 2080.
- How to apply the law to cases, and what a computing professional must do.
:::

## 4.1 The need for cyber law

Cyber law addresses three problems. **Legal recognition:** can a contract made by email be enforced? Is an electronic signature valid? **Crime:** conduct such as unauthorised access, data damage, fraud and illegal content that older laws did not name. **Rights and duties:** privacy, intellectual property, consumer protection and the responsibilities of service providers. Two difficulties recur: **jurisdiction** (the offender may be abroad) and **evidence** (digital evidence is easy to alter, so it needs proper collection and preservation). Many countries based their laws on the **UNCITRAL Model Law on Electronic Commerce (1996)** and on the **Budapest Convention on Cybercrime (2001)**; Nepal's Act follows the model-law approach of *functional equivalence*: an electronic record can satisfy a legal requirement for writing if it is accessible and reliable.

| Source | Role |
|---|---|
| **Constitution of Nepal (2015)** | Fundamental rights including freedom of expression, the right to privacy and the right to information |
| **Electronic Transactions Act, 2063 (2008)** | Electronic records, digital signatures, certifying authorities, computer offences |
| **Individual Privacy Act, 2075 (2018)** | Protection of personal information, communications and privacy |
| **Copyright Act, 2059 (2002)** | Protects authors' rights including computer programs |
| **Muluki Criminal Code, 2074 (2017)** | General offences (forgery, defamation, privacy offences) applied to online conduct |
| **National Cyber Security Policy, 2080 (2023)** | Policy for the security of national digital infrastructure |
| **Sectoral rules** | NRB directives for banks and payments, NTA licences for telecoms, the Right to Information Act 2064 |

## 4.2 The Electronic Transactions Act, 2063

The Act (authenticated in late 2063 B.S., 2008 A.D.) has four jobs.

**1. Legal recognition of electronic records and signatures.** An electronic record is valid where the law requires a document in writing, if it is accessible for later reference; a **digital signature** (created with a private key and verified with the matching public key, the *public-key infrastructure* in Unit 5 of this book and in *Cryptography and Network Security*) satisfies a legal requirement for a signature when it meets the conditions of the Act. Government bodies may accept filings, issue licences and receive payments electronically. The Act also covers when an electronic message is deemed sent and received, and the validity of electronic **contracts**.

**2. Certification.** The Act creates the **Controller of Certification** (a government office), who licenses **Certifying Authorities (CAs)**, which issue **digital signature certificates** binding a public key to a person's identity. The Controller supervises the CAs and maintains the root of trust. Subscribers must keep the private key secure and report compromise.

**3. Computer offences.** The Act's chapter on computer offences defines the offences and sets maximum penalties. The table lists the sections on which the sources consulted agree; maxima are *upper limits* set by the court within the Act.

| Section | Offence | Maximum imprisonment | Maximum fine (Rs) |
|---|---|---|---|
| 44 | Pirating, destroying or altering computer source code | 3 years | 2,00,000 |
| 45 | Unauthorised access to computer material | 3 years | 2,00,000 |
| 46 | Damage to a computer or information system | 3 years | 2,00,000 |
| 47 | Publication of illegal material in electronic form | 5 years | 1,00,000 |
| 52 | Computer fraud | 2 years | 1,00,000 |

Reading it: the three "system" offences (sections 44, 45, 46: source code, unauthorised access, damage) share the same ceiling of 3 years and Rs 2,00,000, while the *content* offence (section 47) allows the longest prison term, 5 years, but a lower fine. Adding the five ceilings gives 16 years and Rs 8,00,000 as the theoretical sum, which no single case would reach. Other sections (for example breach of confidentiality, false information to obtain a certificate, abetment, offences committed outside Nepal) also exist but are *not tabulated here*, because the secondary sources checked disagree on their amounts; consult the Act's text.

::: example Applying the table
A clerk uses a colleague's password (section 45) and, from inside, publishes defamatory material on the department's page (section 47). The maximum exposure under these two sections is 3 + 5 = **8 years** and Rs 2,00,000 + 1,00,000 = **Rs 3,00,000**, if the court imposes both maxima in full, which is rare; the actual penalty depends on gravity, intent and the court. Separate offences may also arise under the Criminal Code. The case turns on **evidence**: server logs, the account used, the IP address and the device.
:::

**4. Other provisions.** Powers of **investigation and search** (police cyber units; the **Nepal Police Cyber Bureau** handles complaints), a **special tribunal** system for cyber cases, and rules on service providers' duties. Offences committed *outside* Nepal that involve a computer or network in Nepal can be prosecuted (extra-territorial reach, as the Act's section on this is usually described).

### What counts as "illegal material"?

Section 47 targets electronic publication that is contrary to **public morality or decent behaviour**, spreads **hatred or jealousy** against a person or community, jeopardises **harmonious relations** among castes, religions or communities, or is otherwise prohibited by law. Critics note that these phrases are broad and have been used against satire and criticism, which raises freedom-of-expression concerns. Responsible practice: understand the limits, think before you post, keep records of abuse you receive, and report through platforms and the police cyber unit.

## 4.3 Privacy: the Individual Privacy Act, 2075

The Constitution (Article 28) guarantees the privacy of a person, their home, property, documents, data, correspondence and character. The **Individual Privacy Act, 2075 (2018)** gives effect to this. It protects personal information, defines the circumstances in which **personal information** (including health, identity and financial data) may be collected, used or published, regulates **surveillance** and recording of private conversations, and prescribes remedies. For computing professionals the key principles are the universal data protection principles: **lawful and fair collection with consent**, **purpose limitation** (use data only for the stated purpose), **data minimisation**, **accuracy**, **security**, **retention limits**, and **individual rights** (access, correction). Nepal has no single comprehensive data-protection authority comparable to the EU's GDPR at the time of writing; obligations come from this Act, sector rules (banking secrecy, health) and the ETA. Practical duties: obtain consent, publish a privacy notice, encrypt and restrict access, log access, and plan for breach reporting.

## 4.4 Copyright and software

The **Copyright Act, 2059 (2002)** protects original works of authorship: literary, artistic and scientific works, and **computer programs** and databases. Rights include reproduction, adaptation, distribution and public performance; protection arises automatically (registration is optional but useful as evidence) and lasts for the life of the author plus a period specified in the Act (50 years after death for most works). *Ideas and algorithms are not protected, only their expression.* **Licences** decide what you may do: **proprietary** (use under terms), **open source** (permissive licences such as MIT and Apache; copyleft such as GPL, which requires derived works to be shared under the same terms) and **Creative Commons** for content. **Software piracy** (using unlicensed copies, or breaking licences) is both an infringement and a security risk (cracked software often carries malware). Related regimes: **patents** (inventions), **trademarks** (names and logos, registered with the Department of Industry) and **trade secrets** (protected by confidentiality). When using code from the web: check the licence, keep the notice, and do not paste proprietary code into assignments or products.

## 4.5 National Cyber Security Policy, 2080

Nepal's first cyber security policy dates from 2012 and a new **National Cyber Security Policy** was approved in 2080 B.S. (2023). Policies of this type usually set out: protection of **critical information infrastructure** (banking, power, telecom, government systems), a national **computer emergency response team (CERT)** and sector teams, incident reporting, standards and audits, capacity building and research, and international cooperation. They guide agencies but do not by themselves create offences; binding duties need Acts and rules. Nepal's **government CERT (NPCERT)** under the Ministry of Communication and Information Technology coordinates incident response. Banks must also follow NRB's IT guideline and information-security rules.

## 4.6 Professional duties

A computing professional should: know the offences, so never access systems without written permission (an ethical hacker works under **scope and authorisation**); preserve logs and evidence correctly; protect personal data as a duty; respect licences; refuse to build systems for unlawful surveillance or fraud; and report incidents to the right authority. If you are a victim: **do not delete evidence**, take screenshots with URLs and times, change passwords and enable MFA, report to the platform, then to the police cyber bureau (or the nearest police office), and inform your bank at once for financial fraud.

## 4.7 Seeing the ideas: the institutions, the penalty ceilings, the trust chain and the first hour

Law is made real by institutions. Plate 4.1 shows three of them: the Nepal Police Cyber Bureau that receives complaints, the Supreme Court that decides the hardest questions, and the gavel that stands for the judge's final word. Digital evidence travels the same path from a victim's phone to a courtroom.

```photogrid label="4.1" cols="3" ratio="1.25" caption="Where cyber law is enforced. (a) The signboard of the Cyber Bureau of the Nepal Police, Bhotahity, Kathmandu: the office that takes complaints about online fraud, abuse and hacking. (b) The Supreme Court of Nepal: the final authority on how the Electronic Transactions Act and the Constitution are read. (c) A judge's gavel, the symbol of a final judgment. A complaint begins with evidence and ends, if it is serious, with a court order."
@ photo id="bca-st/cyberbureau" cap="Cyber Bureau, Nepal Police"
fit 1.25
focus 0.5 0.5
@ photo id="bca-st/supremecourt" cap="Supreme Court of Nepal"
fit 1.25
focus 0.5 0.5
@ photo id="bca-st/gavel" cap="The gavel"
fit 1.25
focus 0.5 0.5
```

```svgfig label="4.1" caption="From an offence to a decision. Every step depends on evidence: logs, screenshots, the account used and the device. Evidence that was deleted, edited or never saved cannot be recovered later, which is why victims are told to preserve it first."
f = Fig(580, 150)
st = [("1. Incident", "fraud, abuse,\nhacking", ROSE, RED), ("2. Evidence", "screenshots,\nURLs, logs", SAND, AMBER), ("3. Complaint", "Cyber Bureau or\npolice office", BLUE, NAVY), ("4. Investigation", "device, log and\nIP analysis", BLUE, NAVY), ("5. Case", "prosecution\nunder ETA, Code", MINT, TEAL)]
for i, (t, s, fl, sk) in enumerate(st):
    x = 6 + i * 115
    f.box(x, 14, 104, 78, t + "\n" + s, fill=fl, stroke=sk, size=9.6, bold=True)
    if i < 4:
        f.arrow([(x + 104, 53), (x + 115, 53)], color=SLATE)
f.box(6, 106, 568, 36, "Weak points: delay (logs are overwritten), foreign servers (jurisdiction), shared accounts (who typed it?)", fill="#f8fafc", stroke=SLATE, size=10)
```

```svgfig label="4.2" caption="Maximum penalties of the five tabulated ETA 2063 offences, drawn to scale from the table in section 4.2. Bars show the upper limit; courts set the actual penalty below it according to gravity and intent. The content offence (s. 47) has the longest prison ceiling but a lower fine than the system offences."
f = Fig(580, 218)
rows = [("s. 44 source code", 3, 2), ("s. 45 unauthorised access", 3, 2), ("s. 46 damage to system", 3, 2), ("s. 47 illegal material", 5, 1), ("s. 52 computer fraud", 2, 1)]
f.text(170, 12, "maximum imprisonment (years)", size=9.5, color=NAVY, bold=True)
f.text(440, 12, "maximum fine (Rs lakh)", size=9.5, color=TEAL, bold=True)
for i, (n, y, r) in enumerate(rows):
    yy = 24 + i * 34
    f.text(6, yy + 15, n, size=9.6, color=SLATE, bold=True, anchor="start")
    f.box(150, yy + 3, y * 24, 20, "", fill=BLUE, stroke=NAVY)
    f.text(150 + y * 24 + 6, yy + 14, "%d yr" % y, size=10, color=NAVY, bold=True, anchor="start")
    f.box(390, yy + 3, r * 40, 20, "", fill=MINT, stroke=TEAL)
    f.text(390 + r * 40 + 6, yy + 14, "Rs %d,00,000" % r, size=10, color=TEAL, bold=True, anchor="start")
f.text(290, 204, "Sum of the five ceilings: 16 years and Rs 8,00,000 (theoretical only)", size=10, color=RED, bold=True)
```

```svgfig label="4.3" caption="The trust chain behind a legally valid digital signature. The Controller of Certification licenses a Certifying Authority; the CA signs a certificate that binds a public key to a named person; the person signs a document with the private key; anyone can verify it with the public key. If the private key leaks, the subscriber must report it so the certificate is revoked."
f = Fig(580, 196)
f.box(8, 14, 150, 52, "Controller of\nCertification", fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
f.box(215, 14, 150, 52, "Certifying Authority\n(licensed)", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(422, 14, 150, 52, "Certificate: name +\npublic key, CA-signed", fill=MINT, stroke=TEAL, size=10, bold=True)
f.arrow([(158, 40), (215, 40)], color=SLATE, label="licenses", lpos=(186, 30))
f.arrow([(365, 40), (422, 40)], color=SLATE, label="issues", lpos=(394, 30))
f.box(8, 108, 170, 52, "Signer: private key\nsigns the document", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(205, 108, 170, 52, "Signed record\n(document + signature)", fill="#f8fafc", stroke=SLATE, size=10, bold=True)
f.box(402, 108, 170, 52, "Verifier: public key\nchecks the signature", fill=MINT, stroke=TEAL, size=10, bold=True)
f.arrow([(178, 134), (205, 134)], color=SLATE); f.arrow([(375, 134), (402, 134)], color=SLATE)
f.arrow([(497, 66), (497, 108)], color=TEAL, dash=True)
f.text(290, 184, "Valid only if the certificate is current, not revoked and chains up to a licensed CA", size=9.6, color=RED, bold=True)
```

```svgfig label="4.4" caption="The first hour after online fraud. The order matters: save evidence before anything is deleted, stop the loss at the bank, secure the accounts, then report. Each step has a reason, shown beside it."
f = Fig(580, 214)
st = [("1. Save evidence", "screenshots with URL, time,\nphone number, transaction ID", SAND, AMBER), ("2. Call the bank", "block card or wallet, ask for a\nhold or recall of the transfer", ROSE, RED), ("3. Secure accounts", "change passwords, switch on MFA,\nlog out other devices", BLUE, NAVY), ("4. Report", "platform, then Cyber Bureau\nor nearest police office", MINT, TEAL)]
for i, (t, s, fl, sk) in enumerate(st):
    y = 8 + i * 51
    f.box(8, y, 150, 42, t, fill=fl, stroke=sk, size=10.6, bold=True)
    f.box(170, y, 400, 42, s, fill="#f8fafc", stroke=SLATE, size=10.2)
    if i < 3:
        f.arrow([(83, y + 42), (83, y + 51)], color=SLATE)
```

### 4.7.1 Eight duties of a computing professional under Nepali cyber law

1. **Work only with written authorisation.** Access without permission is an offence under section 45 even if the intention is good. A penetration tester therefore signs a scope document naming the systems, dates and methods. A student who tests a college portal without asking can still be charged.
2. **Protect personal data as a duty.** The Individual Privacy Act 2075 and the Constitution treat data about health, identity and money as private. Collect only what you need and keep it only as long as you need it. A school app that stores citizenship photos on an open folder breaks this duty.
3. **Preserve logs and evidence.** Digital evidence is easy to change, so keep server logs, backups and records with times. A system administrator who wipes logs after an incident may destroy the proof the police need. Write down who copied what and when.
4. **Keep private keys and credentials safe.** A digital signature is legally valid only if the key stays under the signer's control. Never share a signing token or a password with a colleague. Report a lost token at once so the certificate is revoked.
5. **Respect licences and copyright.** The Copyright Act 2059 protects programs and databases. Use open-source code under its licence terms and keep attributions. Copying a competitor's source code can also fall under section 44.
6. **Do not publish or forward illegal material.** Section 47 covers content that spreads hatred or breaks public morality. Think before you post, and report abuse instead of passing it on. Know that the wording is broad and use judgement and the law's text.
7. **Refuse to build unlawful systems.** Software that spies on people without a legal basis, or that tricks them out of money, is wrong whoever pays for it. A professional can decline and explain why in writing. Ethics and law point the same way here.
8. **Report incidents to the right authority.** Tell your organisation, the bank or regulator where money is involved, and the Cyber Bureau where a crime is likely. Early reports limit the damage for others. Keeping silent to protect reputation usually makes the harm worse.

## Chapter summary

- Cyber law supplies recognition (records, signatures), crime definitions and rights; jurisdiction and evidence are enduring difficulties.
- The ETA 2063 recognises electronic records and digital signatures, creates the Controller of Certification and Certifying Authorities, and defines computer offences.
- Sections 44, 45 and 46 carry up to 3 years and Rs 2,00,000; section 47 up to 5 years and Rs 1,00,000; section 52 (computer fraud) up to 2 years and Rs 1,00,000.
- The Individual Privacy Act 2075, the Copyright Act 2059, the Criminal Code 2074 and the 2080 cyber security policy complete the framework.
- Professionals act within authorisation, protect data, respect licences and preserve evidence.

## Practice

1. Why do cyber laws need a rule of "functional equivalence"?
2. State the maximum imprisonment and fine for ETA sections 45 and 47.
3. A person damages a company's database (s. 46) and commits computer fraud (s. 52). What is the theoretical maximum combined imprisonment and fine?
4. What are the roles of the Controller of Certification and of a Certifying Authority?
5. Why is section 47 criticised?
6. List four data protection principles relevant to a software developer.
7. Does copyright protect an algorithm? Explain.
8. Differentiate permissive and copyleft open-source licences.
9. What should a victim of online fraud do in the first hour?
10. Why must an ethical hacker have written authorisation?

::: note Answers and worked solutions
**1.** To let an electronic record or signature meet a legal requirement for writing or signing so that electronic contracts and filings are valid.
**2.** Section 45: 3 years and Rs 2,00,000 (either or both, as the court decides). Section 47: 5 years and Rs 1,00,000.
**3.** 3 + 2 = **5 years** and Rs 2,00,000 + 1,00,000 = **Rs 3,00,000**.
**4.** The Controller licenses and supervises CAs and maintains the root of trust; a CA issues certificates binding public keys to identities.
**5.** Its wording (public morality, decent behaviour, hatred) is broad and can be used to restrict legitimate criticism and satire.
**6.** Consent, purpose limitation, data minimisation, security (also accuracy and retention limits).
**7.** No; copyright protects the expression (the code), not the underlying idea or algorithm.
**8.** Permissive (MIT, Apache) allow reuse in proprietary products with attribution; copyleft (GPL) requires derivative works to be released under the same licence.
**9.** Preserve evidence (screenshots), contact the bank to block the account or card, change passwords and enable MFA, and report to the police cyber unit.
**10.** Without authorisation, access is an offence (unauthorised access); authorisation and scope make the test lawful.
:::


## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain how the Electronic Transactions Act 2063 gives legal recognition to electronic records and digital signatures. What do the Controller of Certification and a Certifying Authority do?**

*Introduction.* Before the Act, a contract, licence or filing had to be on paper with a handwritten signature to be safe in court. The Electronic Transactions Act 2063 (2008) removed that doubt (section 4.2, Figure 4.3).

1. **Electronic records.** Where the law requires a document in writing, an electronic record is valid if it can be accessed later for reference. This is called functional equivalence. An emailed contract or an online tax filing is therefore enforceable.
2. **Digital signatures.** A signature made with a private key and verified with the matching public key satisfies a legal requirement for a signature when the Act's conditions are met. The signature shows who signed and that the text has not changed.
3. **Controller of Certification.** A government office that licenses Certifying Authorities, supervises them and maintains the root of trust for the country.
4. **Certifying Authority (CA).** A licensed body that issues digital signature certificates, each binding a public key to a named person or organisation.
5. **Duties of the subscriber.** The key holder must keep the private key safe and report any compromise so that the certificate can be revoked.

| Actor | Role |
|---|---|
| Controller of Certification | Licenses and supervises CAs |
| Certifying Authority | Issues certificates |
| Subscriber | Signs; protects the private key |
| Verifier | Checks signature and certificate |

*Example.* A company files its annual return online with a director's digital signature. The office verifies the signature against the CA's certificate and accepts the filing.

*Conclusion.* The Act makes electronic dealings as valid as paper ones, but only when keys and certificates are managed properly.

**Q2 (5 marks). List the computer offences of the ETA 2063 with their maximum penalties. A student logs in to a classmate's account without permission, deletes her files and then posts an insulting message about her. Which offences arise and what is the maximum exposure?**

*Introduction.* The Act's chapter on computer offences sets upper limits; the court chooses the actual penalty (section 4.2 and Figure 4.2).

| Section | Offence | Maximum imprisonment | Maximum fine |
|---|---|---|---|
| 44 | Pirating, destroying or altering source code | 3 years | Rs 2,00,000 |
| 45 | Unauthorised access | 3 years | Rs 2,00,000 |
| 46 | Damage to a computer or information system | 3 years | Rs 2,00,000 |
| 47 | Publication of illegal material | 5 years | Rs 1,00,000 |
| 52 | Computer fraud | 2 years | Rs 1,00,000 |

*Application.* (a) Logging in without permission is **section 45**: up to 3 years and Rs 2,00,000. (b) Deleting her files damages information in a system: **section 46**, up to 3 years and Rs 2,00,000. (c) The insulting post may fall under **section 47** if it is illegal material, up to 5 years and Rs 1,00,000, and also under the Criminal Code on defamation.

*Maximum exposure under the ETA.* Imprisonment 3 + 3 + 5 = **11 years**; fine 2,00,000 + 2,00,000 + 1,00,000 = **Rs 5,00,000**. This is a theoretical ceiling; real penalties are lower and depend on gravity and intent.

*Evidence.* The case would rest on login logs, the IP address, the device and the account history.

*Conclusion.* One act can break several sections, so a professional must treat every access and every post as legally significant.

**Q3 (10 marks). Describe the cyber law framework of Nepal. Explain the need for cyber law, the main statutes, the offences and penalties under the ETA 2063 and the duties of a computing professional.**

*Introduction.* Cyber law is the body of rules that gives legal effect to electronic dealings, defines computer crime and protects rights online. Nepal has no single code; it combines the Constitution, several Acts and a policy (section 4.1).

*Need for cyber law.* Three problems drive it: legal recognition (is an email contract valid?), crime that older laws did not name (unauthorised access, data damage) and rights and duties (privacy, copyright, service providers). Two difficulties remain: jurisdiction, because offenders can be abroad, and evidence, because digital proof is easy to alter.

*The framework (see the table).*

| Source | Contribution |
|---|---|
| Constitution 2015 | Freedom of expression, privacy (Article 28), right to information |
| ETA 2063 | Records, signatures, CAs, computer offences |
| Individual Privacy Act 2075 | Protects personal information and communications |
| Copyright Act 2059 | Protects programs and databases |
| Muluki Criminal Code 2074 | Forgery, defamation and privacy offences applied online |
| National Cyber Security Policy 2080 | Protects critical information infrastructure; CERT |

*The ETA 2063 in detail.* It recognises electronic records and digital signatures, creates the Controller of Certification and licensed Certifying Authorities, and lists offences: sections 44, 45 and 46 carry up to 3 years and Rs 2,00,000; section 47 up to 5 years and Rs 1,00,000; section 52 up to 2 years and Rs 1,00,000. It also provides for investigation, special tribunals and prosecution of offences abroad that involve a computer in Nepal. Section 47 is criticised because "public morality" and "decent behaviour" are wide terms that can be used against satire and criticism.

*Duties of a professional.* Work only with written authorisation; protect personal data; preserve logs and evidence; guard private keys; respect licences; refuse unlawful systems; report incidents to the right authority (section 4.7.1). A victim should save evidence, call the bank, secure accounts and report to the Cyber Bureau (Figure 4.4).

*Conclusion.* Nepal's framework recognises electronic dealings and punishes misuse, but it is spread across several laws and some terms are broad, so professionals must read the current text and act within authorisation, privacy and licence limits.
