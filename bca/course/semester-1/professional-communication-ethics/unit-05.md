---
subject: Professional Communication and Ethics
grade: BCA Semester 1
unit: 5
title: Professional Ethics, Intellectual Property and Cyber Law
area: BCA 105 · Professional Communication and Ethics · Unit 5
---

Software now controls aircraft, money, medical devices, elections and the data of whole populations. Those who build it carry responsibility. This unit gives you the vocabulary of ethics, the main professional codes, the law of intellectual property and privacy, the Nepali cyber-law framework, and real cases where ethical failure had consequences.

::: key What this unit gives you
- Ethical theories and a step-by-step method for deciding hard cases.
- The ACM Code of Ethics; professional responsibility and whistle-blowing.
- Intellectual property: copyright, patents, trademarks, trade secrets, software licences.
- Privacy and data protection; AI and algorithmic fairness.
- Nepal's cyber-related laws, and four case studies.
:::

## 5.1 Ethics and professionalism

**Ethics** is the study of what is right and wrong and how we ought to act. **Morals** are personal beliefs; **law** is the set of rules the state enforces; **professional ethics** are the standards a profession sets for its members. Something can be legal but unethical (selling users' data in an undisclosed way where no law prohibits it) or illegal but arguably ethical (civil disobedience). A professional must check both.

A **profession** has specialised knowledge, a code of conduct, public trust and responsibility. Engineers and doctors are licensed; software work in most countries is not, so *personal* ethics matter even more.

**Main ethical theories**

| Theory | Question it asks | Example |
|---|---|---|
| **Utilitarianism** (consequences) | which action produces the greatest good for the greatest number? | release a security patch quickly because it protects 1 million users, even though a rare bug may affect a few |
| **Deontology** (duty, rules) | which action follows the moral rule or duty regardless of outcome? | never lie to a client about a defect, even if the truth loses the sale |
| **Virtue ethics** (character) | what would an honest, fair, courageous person do? | admit a mistake in your own code |
| **Rights-based** | does the action respect people's rights? | users' right to privacy |
| **Justice / fairness** | are benefits and burdens distributed fairly? | a hiring algorithm must not disadvantage a caste, gender or region |

## 5.2 A method for ethical decisions

1. **Identify the facts**: who, what, when; separate what you know from what you assume.
2. **Identify the ethical issue** and the **stakeholders**: users, client, employer, colleagues, the public.
3. **List the options**, including "do nothing".
4. **Test each option**: Is it legal? Does it follow the code of ethics? Who is helped and harmed? Would I be comfortable if my family, a journalist or my professor read about it (the **newspaper test**)? Would it be acceptable if everyone did it (**universality test**)?
5. **Decide and act**, document the decision, seek advice (a mentor, the professional body, a lawyer) before drastic steps.
6. **Review** the result and learn from it.

::: example Worked example: a client asks you to hide a defect
*Situation:* the day before launch, you discover that the online-payment module sometimes charges a customer twice. Your manager says "Launch anyway; we will fix it next month. Don't tell the client."
*Facts:* double charges happen about 1 in 200 transactions. *Stakeholders:* customers (financial loss), client (reputation, legal liability), your employer, you. *Options:* (a) obey silently; (b) launch but tell the client and fix within a week; (c) delay the launch and fix; (d) escalate to a senior manager or ethics channel. *Test:* (a) fails the newspaper test and harms the public; breaches honesty and avoid-harm principles (ACM 1.2 and 1.3). (b) is acceptable only if customers are warned and refunds are guaranteed. (c) is safest. **Decision:** (c), or (b) with the client's informed consent; record your objection in writing, and escalate if overruled.
:::

## 5.3 Codes of ethics

The **ACM Code of Ethics and Professional Conduct** (2018) is the most used code for computing. Its general principles:

| # | Principle | In practice |
|---|---|---|
| 1.1 | Contribute to society and to human well-being | consider the effect of a system on all people |
| 1.2 | Avoid harm | test safety-critical software thoroughly; report risks |
| 1.3 | Be honest and trustworthy | do not exaggerate skills; admit errors; no hidden functions |
| 1.4 | Be fair and take action not to discriminate | check software for bias; make it accessible |
| 1.5 | Respect the work required to produce new ideas, inventions, creative works | credit sources; honour licences |
| 1.6 | Respect privacy | collect only necessary data; secure it |
| 1.7 | Honour confidentiality | do not disclose client or employer secrets |

The code also covers **professional responsibilities** (high-quality work, keep skills current, give honest peer review, access resources only when authorised) and **leadership** (clear responsibility, manage so quality of working life improves). The **IEEE** and **BCS** codes, and the **ACM/IEEE Software Engineering Code**, are similar; in Nepal, the *Nepal Engineering Council* governs licensed engineering, and the *Computer Association of Nepal (CAN)* is the main IT body.

**Whistle-blowing** is reporting wrongdoing inside an organisation to someone who can stop it. Order of steps: raise it internally (supervisor, then ethics or compliance channel); document facts carefully; only if that fails, and public safety is at stake, go to a regulator or the public. Check the legal protections first; retaliation is a real risk.

**Conflicts of interest** arise when personal interests (a relative's company bidding for a contract you evaluate) could bias professional judgement; declare them.

## 5.4 Intellectual property (IP)

| Type | Protects | Duration (typical) | Software example |
|---|---|---|---|
| **Copyright** | expression: source code, documentation, music, images, text; automatic on creation; not ideas | author's life plus 50 years in Nepal's Act; 70 in many countries | your program's source and the app's graphics |
| **Patent** | a new, non-obvious, useful invention | about 20 years | a novel compression method (software patents differ widely by country) |
| **Trademark** | brand names, logos, slogans | renewable | "Daraz", a logo |
| **Trade secret** | confidential commercially valuable information | as long as secret | an algorithm or customer list kept confidential |
| **Industrial design** | appearance of a product | limited | a UI icon set design |

Nepal's **Copyright Act, 2059 (2002)** protects literary and artistic works, including computer programs, and the **Patent, Design and Trademark Act, 2022** covers inventions, designs and marks. Details and durations change, so check the current text.

**Software licences**

| Licence | Rights | Obligations |
|---|---|---|
| Proprietary (EULA) | use only | no copying, modifying or resale |
| **MIT / BSD** (permissive) | use, change, redistribute, even in closed products | keep the copyright notice |
| **Apache 2.0** | like MIT plus a patent grant | notices; state changes |
| **GPL** (copyleft) | use, change, redistribute | derivative works must be released under GPL with source |
| Creative Commons (CC BY, CC BY-SA …) | content, not software | attribution; share-alike if SA |

**Fair use / fair dealing** allows limited use for criticism, review, teaching or research, with attribution. **Piracy**, using cracked software or copying paid course material, harms creators and exposes you to malware.

**Plagiarism in code:** copying another student's program or taking code from a repository without respecting its licence and crediting it. Use the licence of the code you reuse, cite sources in comments, and write what you submit.

## 5.5 Privacy, security and responsible data use

**Privacy** is the right to control information about oneself. **Personal data** is anything identifying a person (name, citizenship number, phone number, IP address, photo, location, biometric data). **Sensitive** data (health, religion, finances) deserves extra care.

**Principles of responsible data handling** (found in the EU GDPR and most laws, including Nepal's Privacy Act): collect only what you need (**data minimisation**), tell people why (**purpose limitation**, **consent**), keep it accurate, keep it only as long as necessary, secure it (encryption, access control), allow people to see and correct their data, and report breaches.

**Security is an ethical duty**: store passwords as salted hashes, never in plain text; patch known vulnerabilities; do not leave default passwords; apply least privilege. **Ethical hacking** is allowed only with written permission and a defined scope; testing a system you do not own is a crime even with good intent.

**Surveillance and monitoring.** Employers may monitor work accounts with notice; secret monitoring of private messages is unethical and usually illegal. Facial recognition, location tracking and profiling raise proportionality questions: is the intrusion needed and the least intrusive way?

**AI and algorithmic ethics:** bias in training data leads to unfair outcomes (for example a loan or hiring model that disfavours some groups); demand transparency, human oversight, testing for bias across groups, and a way to appeal. Generative AI adds issues of copyright, deepfakes and misinformation: disclose AI use where it matters, verify output, and never use it to deceive or to submit others' work as your own.

**Digital divide, accessibility and sustainability**: design for slow connections and low-end phones, support Nepali (Unicode) and accessibility needs (screen readers, contrast), and reduce wasteful computing and e-waste.

## 5.6 Cyber law in Nepal

| Law | Relevance |
|---|---|
| **Electronic Transactions Act, 2063 (BS)** | legal recognition of electronic records, digital signatures and certifying authorities; offences such as unauthorised access, damaging computers, publishing illegal material in electronic form, computer fraud; provision for a Cyber Appellate Tribunal |
| **Copyright Act, 2059** | protects software and digital content |
| **Individual Privacy Act, 2075 (2018)** | rights to privacy of person, home, documents, correspondence, data; rules on collecting and using personal information |
| **Constitution of Nepal (2072), Art. 28** | right to privacy; Art. 17 freedom of opinion and expression with limits |
| **Muluki Criminal Code, 2074 (2017)** | general criminal offences, including defamation and fraud, which also apply online |
| **Banking and payment regulation (Nepal Rastra Bank)** | rules for digital payment providers; cryptocurrency trading is not permitted |
| **Workplace sexual harassment act, 2071** | harassment, including by electronic means, at work |

Nepal Police's **Cyber Bureau** investigates cybercrime. The government has also issued directives on social media use and registration of platforms; they have changed repeatedly, so check the current notices. **Penalties and section numbers are deliberately not quoted here because amendments change them; read the current Act on lawcommission.gov.np before relying on it.**

**Common cyber offences:** hacking, phishing and online fraud, identity theft, cyber-stalking and harassment, circulation of private images without consent, spreading hate or defamatory material, piracy, ransomware, and spreading malware. If you are a victim: save screenshots and URLs, do not delete evidence, report to the platform and to the Cyber Bureau, and tell a trusted adult or colleague.

## 5.7 Case studies

**Therac-25 (1985–87).** A radiation therapy machine delivered massive overdoses in at least six accidents, with several deaths, because of a software race condition and the removal of hardware safety interlocks. *Lessons:* safety-critical software needs independent hardware safeguards, rigorous testing and honest incident reporting; the manufacturer's early denial made it worse.

**Volkswagen emissions scandal (2015).** Software detected laboratory emission tests and reduced emissions only then ("defeat device"). Engineers and managers were prosecuted and the company paid billions in penalties. *Lessons:* writing code you know deceives regulators breaches honesty and public-good duties; "I was told to" is not a defence.

**Boeing 737 MAX (2018–19).** The MCAS flight-control software relied on a single sensor; two crashes killed 346 people. Problems included pilots not being told of the system and pressure to ship quickly. *Lessons:* disclose critical behaviour, design for sensor failure, do not let schedule override safety, and protect engineers who raise concerns.

**Equifax data breach (2017).** Personal data of about 147 million people leaked after a known vulnerability was not patched. *Lessons:* patch management is an ethical duty; collecting sensitive data creates a responsibility to protect it.

## Formula and fact sheet

- Theories: utilitarian (outcomes), deontological (duty), virtue (character), rights, justice.
- Decision steps: facts → issue/stakeholders → options → tests (legal, code, harm, newspaper, universality) → decide and document → review.
- ACM 1.1 to 1.7: well-being, avoid harm, honesty, fairness, respect IP, respect privacy, confidentiality.
- IP: copyright (expression), patent (invention), trademark (brand), trade secret (confidential).
- MIT/BSD permissive; GPL copyleft.
- Data minimisation, purpose limitation, consent, security, access, breach reporting.
- Nepal: ETA 2063, Copyright Act 2059, Privacy Act 2075, Muluki Criminal Code 2074.

## Chapter summary

- Ethics asks what we ought to do; law sets the minimum, and professionals are expected to exceed it.
- A structured method and a code such as ACM's turn vague unease into a defensible decision.
- Copyright, patents, trademarks, trade secrets and licences define what you may do with others' work; plagiarism and piracy violate them.
- Responsible practice means protecting privacy, securing data, testing for bias and speaking up about danger.
- Real failures (Therac-25, VW, 737 MAX, Equifax) show what happens when these duties are ignored.

## Practice

1. Differentiate ethics, morals and law with an example where a legal action is unethical.
2. Explain utilitarianism and deontology with one software example each.
3. State and explain any five principles of the ACM Code of Ethics.
4. Your employer asks you to copy a colleague's licensed library into your product without paying. Apply the decision method.
5. Differentiate copyright, patent, trademark and trade secret.
6. Differentiate MIT and GPL licences. Which would you pick for a library that you want companies to adopt freely?
7. List six principles of responsible personal data handling.
8. Why is storing passwords in plain text unethical? What should be done?
9. List four laws relevant to cyber activity in Nepal and one offence each addresses.
10. Analyse the Boeing 737 MAX case under ACM principles 1.2 and 1.3.
11. A model that screens CVs rejects most women applicants because past hiring favoured men. What went wrong and how can it be fixed?
12. A friend asks you to test a website's security without telling the owner. What do you do?

::: note Answers and worked solutions
**1.** Ethics is the systematic study of right and wrong; morals are personal values; law is state-enforced rules. Example: legally selling users' contact lists when the privacy policy is silent can be unethical.
**2.** Utilitarianism: choose the option with the best overall outcome, such as shipping a patch that protects most users. Deontology: follow the duty regardless of outcome, such as always disclosing a known defect to the client.
**3.** Any five of 1.1 to 1.7 as in the table, with a line of practice each.
**4.** Facts: using licensed code without payment infringes copyright. Stakeholders: the library author, employer, customers. Options: refuse, ask for a licence, replace with an open-source alternative, write your own. The newspaper test fails for copying. Decision: propose buying a licence or using an open-source library, and document your objection.
**5.** Copyright: expression, automatic; patent: invention, granted; trademark: brand identity; trade secret: confidential information.
**6.** MIT permits any use with notice kept; GPL requires derived works to be released with source under GPL. For free adoption by companies choose **MIT** (or Apache 2.0).
**7.** Minimisation, purpose limitation, consent, accuracy, limited retention, security, access/correction, breach reporting.
**8.** If the database leaks, every account is exposed and users who reuse passwords are harmed. Store salted hashes (bcrypt, Argon2), enforce strong passwords and offer two-factor authentication.
**9.** ETA 2063: hacking or computer fraud; Copyright Act 2059: software piracy; Privacy Act 2075: misuse of personal data; Muluki Criminal Code 2074: defamation or fraud online.
**10.** 1.2 (avoid harm): the design depended on a single sensor and failure modes were not safe. 1.3 (honesty): pilots and regulators were not given full information. Engineers should have raised and documented concerns and managers should not have put schedule above safety.
**11.** The training data encoded historical bias, so the model learned it. Fix: audit outcomes by group, remove proxies, rebalance or reweight data, test fairness metrics, add human review, and allow appeals.
**12.** Decline unless the owner gives written permission and a scope. Unauthorised testing is a crime and breaches ethical-hacking norms. Offer to help set up a legal test, for example on a lab you control or through a bug-bounty programme.
:::
