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

```svgfig label="5.1" caption="A six-step method for an ethical decision. Walk through the steps in order and write the answers down. The newspaper test in step 4 asks whether you would be comfortable if your family, a journalist or your teacher read about the decision."
f = Fig(760, 250)
steps = [("1 Facts", "who, what, when;\nknown vs assumed"), ("2 Issue and\nstakeholders", "users, client,\nemployer, public"), ("3 Options", "include\n\"do nothing\""), ("4 Test each", "legal? code of ethics?\nwho is harmed?"), ("5 Decide\nand act", "document it,\nseek advice"), ("6 Review", "what did we\nlearn?")]
for i, (t, d) in enumerate(steps):
    x = 10 + i * 125
    f.box(x, 24, 112, 78, "", fill=BLUE if i % 2 == 0 else SOFT, stroke=NAVY)
    for j, ln in enumerate(t.split("\n")): f.text(x + 56, 46 + j * 15, ln, size=11.5, color=NAVY, bold=True)
    for j, ln in enumerate(d.split("\n")): f.text(x + 56, 100 + 18 + j * 13, ln, size=9.5, color=SLATE)
    if i < 5: f.arrow([(x + 112, 63), (x + 125, 63)], color=TEAL, sw=2)
f.box(10, 170, 740, 60, "", fill=SAND, stroke=AMBER)
f.text(380, 192, "NEWSPAPER TEST (step 4): would I be comfortable if my family, a journalist or my professor read about this?", size=11, color=AMBER, bold=True)
f.text(380, 212, "Example: a manager says \"launch the payment module even though it sometimes charges twice, and do not tell the client\" - the answer is NO.", size=10, color=SLATE)
```

```svgfig label="5.2" caption="Forms of intellectual property (top) and software licences from most restrictive to most open (bottom). Copyright arises automatically when a work is created; a licence is the permission the owner gives to others. Durations differ by country and law, so check the current Act."
f = Fig(760, 330)
cards = [("Copyright", "expression: code,\ntext, images, music", "program source, app art"), ("Patent", "new, useful\ninvention", "novel compression method"), ("Trademark", "brand names,\nlogos", "\"Daraz\" and its logo"), ("Trade secret", "confidential\nbusiness know-how", "private algorithm"), ("Design", "look of a\nproduct", "icon set design")]
for i, (t, p, e) in enumerate(cards):
    x = 10 + i * 150
    f.box(x, 10, 140, 130, "", fill=BLUE if i % 2 == 0 else SOFT, stroke=NAVY)
    f.text(x + 70, 32, t, size=12.5, color=NAVY, bold=True)
    for j, ln in enumerate(p.split("\n")): f.text(x + 70, 56 + j * 14, ln, size=10, color=SLATE)
    f.text(x + 70, 100, "e.g.", size=9, color=TEAL, bold=True); f.text(x + 70, 114, e, size=9, color=TEAL)
f.text(380, 172, "Software licences", size=12, color=NAVY, bold=True)
f.arrow([(40, 190), (720, 190)], color=SLATE, sw=2, both=True); f.text(40, 206, "more restricted", size=9.5, color=RED, bold=True, anchor="start"); f.text(720, 206, "more open", size=9.5, color=TEAL, bold=True, anchor="end")
lic = [("Proprietary\n(EULA)", "use only", ROSE, RED), ("MIT / BSD", "use, change,\nsell; keep notice", MINT, TEAL), ("Apache 2.0", "like MIT + patent\ngrant", MINT, TEAL), ("GPL\n(copyleft)", "derivatives must\nstay GPL + source", SAND, AMBER), ("Creative\nCommons", "for content;\nCC BY needs credit", BLUE, NAVY)]
for i, (t, d, fl, st) in enumerate(lic):
    x = 10 + i * 150
    f.box(x, 220, 140, 100, "", fill=fl, stroke=st)
    for j, ln in enumerate(t.split("\n")): f.text(x + 70, 242 + j * 14, ln, size=11.5, color=st, bold=True)
    for j, ln in enumerate(d.split("\n")): f.text(x + 70, 286 + j * 13, ln, size=9.5, color=SLATE)
```

## 5.8 Eight responsibilities of an IT professional

1. **Honesty and integrity.** A professional tells the truth about what a system can do and about its defects. Hiding a bug, as in the double-charge example, harms customers and ends careers. Honest reports build long-term trust with clients.
2. **Competence and continuous learning.** Accept only work you are able to do, and keep skills up to date. Technology changes fast, so reading, courses and practice are a duty. Poor work in banking or health software can hurt many people.
3. **Respect for privacy and confidentiality.** Data of customers, such as phone numbers, citizenship numbers and bank details, must be used only for the stated purpose. Collect the minimum, store it safely and do not share it. A leak from one ConnectIPS-type service could affect thousands.
4. **Respect for intellectual property.** Use only licensed software, follow open-source licence terms and credit the authors of code and content. Do not use cracked software or copy a friend's project. This protects creators and keeps your own work credible.
5. **Security and safety of users.** Design with passwords hashed, input checked and updates applied. A professional thinks of how the system can be attacked or misused, and fixes weaknesses before release. Safety-critical software, such as hospital systems, needs extra care.
6. **Obeying the law.** Know the basics of the Electronic Transactions Act, the Copyright Act and the Privacy rules relevant to your work, and never help in hacking, fraud or harassment online. Ignorance of the law is not a defence. If a request seems illegal, refuse and seek advice.
7. **Fairness and respect for people.** Treat colleagues, users and clients without discrimination by gender, caste, religion, language or ability. Make software that is accessible, for example with Nepali-language support and readable text. Fairness widens the number of people who can benefit.
8. **Accountability and whistle-blowing.** Accept responsibility for your decisions and mistakes, and report serious wrongdoing through proper channels when the public may be harmed. Keep records of your decisions. Courage to speak up is part of professional ethics.

```photogrid label="5.1" cols="2" ratio="1.4" caption="Anonymous data is often not anonymous. (a) A national identity card: name, birth date and sex are enough to point at one person. (b) A simulated list (seeded random numbers, no real people) describes each person only by ward (32 values), birth year (60 values) and gender (2 values), with no names. In a group of 1,000 people, 768 of them (76.8 per cent) are the only person with their combination, so anyone who knows a neighbour's ward, age and gender can find that row; in a city of 10,000 the share of unique rows is 7.4 per cent because many more people share each combination. Ward alone makes nobody unique. The lesson for an IT professional is that removing names is not enough: collect only the fields you need, group ages into bands, and test how many rows are unique before releasing a data set (the idea of k-anonymity)."
@ photo id="bcapc/idcard" cap="An identity card: three fields can identify a person"
fit 1.4
focus 0.5 0.5
@ svg cap="Share of people unique on ward + birth year + gender"
import numpy as np
rng = np.random.default_rng(2081)
res = []
for pop in (1000, 10000):
    w = rng.integers(1, 33, pop); y = rng.integers(0, 60, pop); g = rng.integers(0, 2, pop)
    key = w * 1000 + y * 10 + g
    u, c = np.unique(key, return_counts=True)
    uw, cw = np.unique(w, return_counts=True)
    res.append((int((c == 1).sum()), pop, int((cw == 1).sum())))
assert res[0][0] == 768 and res[1][0] == 741 and res[0][2] == 0 and res[1][2] == 0
f = Fig(300, 240)
f.text(150, 14, "32 wards x 60 birth years x 2 = 3,840 combos", size=10.5, color=NAVY, bold=True)
for i, ((k, pop, _), col) in enumerate(zip(res, ["#b91c1c", "#0f766e"])):
    y = 34 + i * 62
    f.text(10, y + 6, f"{pop:,} people", size=10.5, color=NAVY, anchor="start", bold=True)
    f.box(10, y + 14, 240, 18, "", fill="#f1f5f9", stroke=SLATE, r=0, sw=1)
    f.box(10, y + 14, 240 * k / pop, 18, "", fill=col, stroke=col, r=0)
    f.text(10, y + 46, f"{k} unique = {k / pop * 100:.1f}%", size=10.5, color=col, anchor="start", bold=True)
f.text(150, 176, "ward alone: 0 unique rows in both groups", size=10.5, color=SLATE)
f.text(150, 196, "smaller groups are easier to re-identify", size=10.5, color=RED, bold=True)
f.text(150, 216, "fix: age bands, fewer fields, test first", size=10.5, color=TEAL, bold=True)
```

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Compare the MIT licence and the GNU GPL. Which would you choose for (a) a library you want everyone to use freely and (b) a program whose improvements you want kept open?**

A **software licence** is the permission the copyright owner gives to others to use, copy, change and share the software. Open-source licences fall into two groups: *permissive* (few conditions) and *copyleft* (conditions that keep derived work open).

| Point | MIT (permissive) | GPL (copyleft) |
|---|---|---|
| Use and modify | allowed | allowed |
| Redistribute | allowed | allowed |
| Use inside closed, paid products | allowed | not allowed: derivative works must also be GPL |
| Obligation | keep the copyright and licence notice | release source of derivatives under the GPL |
| Effect | maximum adoption | keeps improvements open to all |
| Examples | many JavaScript libraries | the Linux kernel |

**Choice.** (a) For a library that everyone, including companies, should be free to use, the **MIT** licence is best because it does not restrict commercial use. (b) For a program whose improvements should stay open, the **GPL** is best, because anyone who distributes a modified version must share its source. *Conclusion:* the choice depends on whether the owner values wide adoption or guaranteed openness. Whatever the licence, the user must read it, keep the notices and give credit.

**Q (10 marks). Define professional ethics. Explain the steps of an ethical decision, illustrate with the example of hiding a software defect, and discuss intellectual property and cyber law as part of the professional's duty in Nepal.**

**Introduction.** **Ethics** is the study of what is right and wrong; **professional ethics** are the standards of conduct that a profession expects of its members: honesty, competence, confidentiality, fairness and responsibility to the public. Law sets the minimum, while ethics asks what we should do beyond it. Codes of ethics (such as the ACM and IEEE codes) guide computing professionals.

**Ethical decision method (Figure 5.1).** (1) Identify the facts. (2) Identify the issue and the stakeholders. (3) List the options, including doing nothing. (4) Test each option: is it legal, is it consistent with the code of ethics, who is helped or harmed, and does it pass the newspaper test? (5) Decide, act, document and seek advice. (6) Review the result.

**Example.** The day before launch you find that the payment module charges customers twice about once in 200 transactions, and your manager says "Launch anyway, do not tell the client". The stakeholders are customers (money lost), the client (reputation, liability), the employer and you. The options are: obey silently, launch with a clear warning and a quick fix, or delay the launch. Silent launch is harmful and fails the newspaper test; the ethical choice is to inform the client, fix or delay, and record the decision, escalating if necessary.

**Intellectual property (Figure 5.2).** Copyright protects expression (code, text, images) automatically; a patent protects a new useful invention; a trademark protects brand names and logos; a trade secret protects confidential know-how. Nepal's Copyright Act, 2059 (2002) covers computer programs, and the Patent, Design and Trademark Act, 2022 covers inventions, designs and marks. Licences such as MIT, Apache, GPL and Creative Commons tell others what they may do. Piracy and code plagiarism are unethical and illegal.

**Cyber law in Nepal.** The **Electronic Transactions Act, 2063 (2008)** gives legal recognition to electronic records and digital signatures and defines computer-related offences such as unauthorised access, damage to computer systems and publishing unlawful material. Specific penalties and sections change, so check the current text. Professionals must also protect personal data and follow the privacy rules that apply.

**Conclusion.** Professionals should not stop at "is it legal?": they should ask whether a decision is honest, fair and safe for everyone affected. A clear method, respect for intellectual property and knowledge of cyber law help students make such decisions with confidence.
