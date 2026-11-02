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
