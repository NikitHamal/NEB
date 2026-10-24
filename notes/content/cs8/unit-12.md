---
subject: Computer Science
grade: 8
unit: 12
title: Computer Ethics and Cyber Law
hours: 0
area: Web, Communication and Society
---

The Internet lets you learn, play and talk with anyone, but the same tools can be used to cheat, steal and hurt people. Some wrong actions are only **unethical**: your conscience, your teachers and your friends tell you not to do them. Others are **crimes**: the law of Nepal punishes them with fines and prison. This lesson explains the rules of good behaviour with computers, the common cyber crimes, the rights of people who create books, music and software, Nepal's cyber law — the **Electronic Transactions Act, 2063** — and how to be a safe, responsible citizen of the digital world.

::: key What the examination asks from this lesson
Expect **definitions** (computer ethics, cyber crime, hacking, phishing, cyber bullying, identity theft, software piracy, copyright, plagiarism, cyber law, digital citizen, netiquette), **the Ten Commandments** (list and explain any four or six), **two-point differences** (ethics and law, copyright and plagiarism, active and passive digital footprint), and **the ETA 2063**: its full name and year, its aims, and two or three offences with their sections and punishments. Scenario questions ask you to name the crime in a story and the section of the Act that applies.
:::

## 12.1 Computer ethics: meaning and the Ten Commandments of computer ethics

::: definition Computer ethics
**Ethics** are the moral principles that tell us what is right and wrong. **Computer ethics** is the set of moral principles that guide how we use computers, networks and the Internet: to respect other people's privacy, property and work, and never to use technology to harm anyone.
:::

Ethics and law are related but not the same. A **law** is made by the state, applies to everyone and is enforced with punishment. **Ethics** come from conscience and society; nobody goes to prison for breaking an ethical rule, but you lose trust and respect, and your school may punish you under its own rules.

| Ethics | Law |
|---|---|
| moral rules of right and wrong | rules made by the government and passed by Parliament |
| followed by choice, from conscience | must be obeyed by everyone |
| breaking them brings shame or loss of trust | breaking them brings a fine, prison or both |
| may differ a little between societies | written down and the same for all citizens |
| example: copying a friend's homework is unethical | example: hacking a bank account is a crime under the ETA 2063 |

Every cyber crime is unethical, but not every unethical act is a crime.

```figure caption="Ethics and law. Every cyber crime lies inside the larger region of unethical acts, but many unethical acts are not crimes. The crimes shown are punished under the Electronic Transactions Act, 2063 (section numbers in brackets)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
fig, ax = plt.subplots(figsize=(5.0, 3.0))
ax.add_patch(Ellipse((0.5, 0.5), 0.98, 0.94, fc="#fdf1dc", ec=SERIES[3], lw=1.3, zorder=1))
ax.add_patch(Ellipse((0.665, 0.47), 0.50, 0.70, fc="#f9dddc", ec=SERIES[1], lw=1.3, zorder=2))
ax.text(0.5, 0.905, "Unethical use of computers", ha="center", va="center", fontsize=9, fontweight="bold", color=SERIES[3])
ax.text(0.665, 0.74, "Cyber crimes:\nalso illegal", ha="center", va="center", fontsize=8.6, fontweight="bold", color=SERIES[1], linespacing=1.15)
for y, t in [(0.62, "copying a friend's\nhomework"), (0.42, "a rude comment\nin a group chat"), (0.22, "playing games in\nclass on the lab PC")]:
    ax.text(0.215, y, t, ha="center", va="center", fontsize=7.5, color=INK, linespacing=1.15)
for y, t in [(0.55, "hacking an account (45)"), (0.42, "posting hateful or\nobscene material (47)"), (0.27, "fraud with someone's\nATM card (52)")]:
    ax.text(0.665, y, t, ha="center", va="center", fontsize=7.5, color=INK, linespacing=1.15)
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
```

### The Ten Commandments of computer ethics

In 1992 the **Computer Ethics Institute**, a group in Washington, D.C., published ten short rules for the ethical use of computers, written by Ramon C. Barquin in the old style of the biblical Ten Commandments ("Thou shalt not…"). The first eight say what *not* to do; the last two say what we *should* do.

| No. | The commandment in plain words | Breaking it looks like this |
|---|---|---|
| 1 | Do not use a computer to harm other people. | posting a photo to embarrass a classmate |
| 2 | Do not interfere with other people's computer work. | switching off a friend's computer while she types her project |
| 3 | Do not snoop around in other people's computer files. | opening a classmate's folder on the lab computer to read his diary |
| 4 | Do not use a computer to steal. | sending money from someone's wallet with a stolen PIN |
| 5 | Do not use a computer to bear false witness (to tell lies). | spreading a false rumour about a teacher on TikTok |
| 6 | Do not copy or use paid (proprietary) software you have not paid for. | installing a cracked copy of a paid game |
| 7 | Do not use other people's computer resources without permission or proper payment. | printing 200 pages of your own notes on the office printer without asking |
| 8 | Do not take other people's intellectual work as your own. | submitting an essay copied from a website |
| 9 | Think about the effects on society of the programs you write and the systems you design. | a game designer adding gambling features for children |
| 10 | Always use a computer in ways that show consideration and respect for other people. | insulting someone in the comments |

::: memory Eight "don'ts" and two "do's"
Don't **harm**, **interfere**, **snoop**, **steal**, **lie**, **copy** paid software, **use** others' resources or **take** others' work. Do **think** about society, and do **respect** people.
:::

::: example Worked example 12.1 — which commandment is broken?
**Problem.** Name the commandment broken in each case. (a) Bikash downloads a cracked copy of a paid photo editor. (b) Anita forwards a made-up story that a shop sells fake medicine. (c) Suman reads the files his friend left open on the lab computer. (d) Puja copies a Wikipedia paragraph into her project without saying where it came from.

**Solution.** (a) Commandment **6** — using paid software without paying. (b) Commandment **5** — telling lies (bearing false witness); it also harms the shopkeeper (commandment 1). (c) Commandment **3** — snooping in other people's files. (d) Commandment **8** — taking other people's work as your own (plagiarism, section 12.3).
:::

## 12.2 Cyber crime: hacking, phishing, cyber bullying, identity theft and software piracy

::: definition Cyber crime
**Cyber crime** is any illegal act carried out by means of a computer, a mobile phone, a network or the Internet. The computer may be the **tool** of the crime (sending a threat, stealing money) or its **target** (breaking into it, damaging its data).
:::

### Hacking

**Hacking** means getting into a computer, a network or an online account **without the owner's permission**, by guessing or stealing a password or by using a weakness in the software. A person who does it is a **hacker**. Some hackers break in to steal data or money, change records or deface websites; this is a crime under sections 45 and 46 of the ETA 2063. **Ethical hackers** are security experts whom a company *invites* to test its systems; they work with written permission and report the weaknesses so that they can be fixed.

::: caution "I only looked, I did not change anything" is no excuse
Students often think that logging in to a friend's account "just to see" is harmless. Under section 45 of the ETA, using a computer or account **without the owner's permission** to get at its programs or data is itself an offence, even if nothing is changed or stolen.
:::

### Phishing

**Phishing** (said like "fishing") is tricking people into giving away their passwords, PINs, OTPs or card numbers by sending a **fake message** that seems to come from a trusted bank, wallet, school or company. The message usually contains a link to a look-alike website that records whatever the victim types. When the trick is played by phone call it is called **vishing**, and by SMS **smishing**.

```figure caption="How a phishing attack steals an account. It can be stopped at the first two steps: check who really sent the message, and never open its link or type an OTP or password into the page it opens."
fig, ax = flow([("1. Bait", "fake SMS or e-mail:\n'account blocked'"), ("2. Click", "link opens a\nlook-alike website"), ("3. Hook", "victim types\npassword and OTP"), ("4. Steal", "criminal logs in\nand moves money")], note="Stop it at step 1 or 2: a real bank or wallet never asks for your password, MPIN or OTP.")
```

```photo id="cs8/eth-phishing-email" caption="A made-up phishing e-mail prepared for teaching. The numbered marks show its warning signs." width="78"
mark 0.60 0.916 "1"
mark 0.31 0.579 "2"
mark 0.815 0.528 "3"
mark 0.56 0.24 "4"
mark 0.25 0.089 "5"
key 1 The sender's address is not the bank's real web address.
key 2 No name: a real bank uses your name, not "Dear account holder".
key 3 A spelling mistake ("divice").
key 4 An urgent order with a link to a look-alike website.
key 5 The name in the signature does not match the name in the logo.
```

### Cyber bullying

**Cyber bullying** is using phones, chat apps, games or social media to **repeatedly hurt, threaten, shame or frighten** someone: sending insulting messages, posting embarrassing photos or edited pictures, making a fake profile in someone's name, or leaving a person out of a class group on purpose. It is serious because it can follow a victim home at any hour and is seen by many people. If it happens to you or a friend: **do not reply**, **keep the evidence** (screenshots with the date), **block and report** the account on the app, and **tell a parent or teacher**. Serious cases can be reported to the police; publishing obscene or hateful material is an offence under section 47 of the ETA.

### Identity theft

**Identity theft** is stealing someone's personal details — name, photos, date of birth, citizenship or account numbers, passwords — and **pretending to be that person**, for example to open a fake Facebook profile and ask their friends for money, to take a loan, or to buy things online. Protect your identity by keeping such details private, never posting photos of your citizenship card, ID card or bank cards, and using strong, different passwords.

### Software piracy

**Software piracy** is copying, selling, sharing or using software **without the licence** (permission) of its owner: cracked copies of paid programs, shared serial keys, or paid apps downloaded free from unofficial sites. It cheats the programmers who made the software, and pirated copies often carry **viruses** (Lesson 13) and get no security updates. In Nepal a computer program is a protected "work" under the **Copyright Act, 2059**. The honest alternatives are to buy a licence or to use **free and open-source software** such as LibreOffice, GIMP and Firefox.

| Cyber crime | What it is | Example | Protection |
|---|---|---|---|
| Hacking | entering a computer or account without permission | breaking into a school's result system to change marks | strong passwords, MFA, software updates |
| Phishing | a fake message that tricks you into giving passwords or OTPs | an SMS "your eSewa account is blocked, verify here" | never click unknown links; never share an OTP |
| Cyber bullying | repeatedly hurting someone online | a fake profile made to mock a classmate | block, report, keep evidence, tell an adult |
| Identity theft | pretending to be someone using their details | a fake profile asking the victim's friends for money | keep personal details and ID photos private |
| Software piracy | using or sharing software without a licence | selling cracked Windows on a pen drive | buy licences or use free software |

Other cyber crimes include **online fraud** (fake shops and "lottery prize" calls), **cyber stalking** (following and frightening someone online) and spreading **viruses**.

::: example Worked example 12.2 — is this message phishing?
**Problem.** Ramesh gets this SMS: "Dear Customer, your eSewa account will be BLOCKED in 2 hours due to incomplete KYC. Verify now: http://esewa-kyc-update.info and enter your ID and MPIN." Give four warning signs and say what he should do.

**Solution.** Warning signs: (1) the web address is not eSewa's real site; (2) it creates **panic** with a short deadline; (3) it asks for the **MPIN**, which no real company ever asks for; (4) it greets him as "Dear Customer", not by name. **What to do:** do not open the link or reply; delete the message; if in doubt, open the official eSewa app himself or call the company's number from its official website; and warn his family, who may get the same message.
:::

## 12.3 Intellectual property, copyright and plagiarism

::: definition Intellectual property
**Intellectual property (IP)** is a creation of the mind: a story, a song, a photograph, a film, a computer program, an invention, a design or a brand name. **Intellectual property rights (IPR)** are the legal rights that let the creator decide, for a fixed time, who may copy, use or sell that creation.
:::

| Kind of IPR | Protects | Example | In Nepal |
|---|---|---|---|
| Copyright | literary, artistic and musical works, films, photos and computer programs | a Nepali song, a textbook, a mobile app | Copyright Act, 2059; Nepal Copyright Registrar's Office |
| Patent | a new invention | a new kind of water filter | Patent, Design and Trademark Act, 2022; Department of Industry |
| Trademark | the name, logo or sign of a business | the logo of a Nepali noodle brand | same Act; Department of Industry |
| Industrial design | the shape or look of a product | the shape of a bottle | same Act; Department of Industry |

### Copyright

::: definition Copyright
**Copyright** is the legal right of the creator of an original work to copy, publish, perform, translate, adapt and sell it, and to stop others from doing so without permission. It belongs to the creator **automatically** as soon as the work is made; registering it is optional. The symbol is ©.
:::

Under Nepal's **Copyright Act, 2059 (2002)**, copyright normally lasts for the **whole life of the author and 50 years after the author's death**, and the Act lists computer programs among the protected works. Using a small part of a work for study, comment or news, with the source named, is generally allowed; copying a whole book, film or program without permission is not.

Some creators *choose* to let everyone reuse their work. A **Creative Commons (CC)** licence tells you exactly what you may do: **BY** means you must credit the creator, **SA** (share-alike) means you must share your new version under the same licence, **NC** forbids commercial use and **ND** forbids changes. Work in the **public domain** (PD or CC0) is free for anyone. Every photograph in this book is used under such a licence, which is why a "Source" line is printed under each one.

```photo id="cs8/eth-cc-spectrum" caption="The Creative Commons licences, from the most open (public domain, top) to the least open (all rights reserved, bottom). The icons on the left show what each group allows: share, remix (change), or use commercially." width="50"
```

### Plagiarism

::: definition Plagiarism
**Plagiarism** is presenting someone else's words, ideas, pictures, code or work as your own **without giving them credit**.
:::

Copying a paragraph from a website into your project, submitting a friend's homework, or handing in an essay written by an AI tool as if you wrote it are all plagiarism. To avoid it: **write in your own words**; when you use someone's exact words, put them in "quotation marks" and **name the source**; list the books and websites you used at the end of your project (a **bibliography**); and ask permission before using someone's photo.

| Copyright infringement | Plagiarism |
|---|---|
| copying or using a work **without permission** | using a work **without giving credit** |
| a legal matter; can be punished under the Copyright Act | an ethical and academic matter; punished by the school |
| giving credit does not make it legal | getting permission does not make it honest unless you also credit |
| example: uploading a whole Nepali film to YouTube | example: copying a Wikipedia paragraph into your project as your own words |

::: caution Changing a few words is still plagiarism
Swapping a few words for synonyms, or changing the order of sentences, does not make someone's paragraph yours. The idea and the structure are still theirs. Either quote it exactly and name the source, or close the book and explain it in your own words, then name the source anyway.
:::

::: example Worked example 12.3 — copyright, plagiarism or piracy?
**Problem.** Classify each case. (a) A shop in New Road sells pen drives loaded with cracked games. (b) Sunita copies three paragraphs from a news website into her report without quotation marks or the website's name. (c) A YouTube channel uploads a new Nepali film the day after it is released. (d) Arjun quotes two lines of a poem by Laxmi Prasad Devkota in his essay, in quotation marks, with the poet's name.

**Solution.** (a) **Software piracy** (copyright infringement of programs). (b) **Plagiarism**. (c) **Copyright infringement** (film piracy). (d) **Acceptable**: a short quotation, marked and credited, is fair use.
:::

## 12.4 Cyber law in Nepal: the Electronic Transactions Act, 2063

::: definition Cyber law
**Cyber law** is the body of law that deals with the use of computers, the Internet and electronic records: it gives electronic documents and signatures legal value and defines and punishes cyber crimes. It is often called the **law of the Internet**.
:::

Nepal's cyber law is the **Electronic Transactions Act, 2063**. Its official English title is "The Electronic Transactions Act, 2063 (2008)". It was **authenticated and published on 22 Mansir 2063 BS (8 December 2006)** as Act number 27 of 2063, and is treated as in force from 24 Bhadra 2063, because an ordinance with the same rules was already in force. It has **12 chapters and 80 sections**.

**Aims of the Act.** It was made (1) to give legal recognition to **electronic records** and **digital signatures**, so that a document kept or signed electronically is as valid as one on paper (sections 4 and 5); (2) to make electronic transactions such as online banking and shopping **reliable and secure**; (3) to set up a **Controller** and licensed **Certifying Authorities** that issue digital signature certificates; and (4) to **control computer crimes** by defining them and fixing punishments.

**Main parts.** Chapter 9, "Offence Relating to Computer" (sections 44 to 59), lists the crimes. Chapter 10 provides for a three-member **Information Technology Tribunal** — one member each from law, information technology and commerce, with the law member as chairperson — to hear these cases, and Chapter 11 for an **Appellate Tribunal** to hear appeals.

| Section | Offence | Maximum punishment |
|---|---|---|
| 44 | pirating, destroying or altering computer source code | up to 3 years in prison, or a fine up to Rs 2 lakh, or both |
| 45 | unauthorised access: using a computer, its programs or data without the owner's permission (hacking) | a fine up to Rs 2 lakh, or up to 3 years, or both, by the seriousness of the offence |
| 46 | damage to a computer or information system: deleting, altering or disrupting its data to cause loss | a fine up to Rs 2 lakh, or up to 3 years, or both |
| 47 | publishing illegal material in electronic form: material banned by law, against public morality or decent behaviour, spreading hatred, or harming harmony between castes, tribes and communities | a fine up to Rs 1 lakh, or up to 5 years, or both; heavier each time it is repeated |
| 48 | revealing confidential records obtained under the Act | a fine up to Rs 10,000, or up to 2 years, or both |
| 49 | giving false information to the Controller or a Certifying Authority | a fine up to Rs 1 lakh, or up to 2 years, or both |
| 52 | computer fraud, such as using someone's account or ATM card dishonestly | the money gained is recovered for the victim, plus a fine up to Rs 1 lakh, or up to 2 years, or both |
| 53 | abetting, attempting or conspiring to commit a computer offence | a fine up to Rs 50,000, or up to 6 months, or both |
| 54 | helping as an accomplice | half the punishment of the main offender |

(1 lakh = 1,00,000 = one hundred thousand rupees.) Section 55 lets a case be filed in Nepal even when the offence was committed from abroad, if it involves a computer system in Nepal, and section 56 lets the computers, disks and software used in a crime be **confiscated** (taken by the state).

::: caution Two mistakes about the ETA
**The year.** 2063 is a Bikram Sambat year; the Act was authenticated on 22 Mansir 2063, which was 8 December 2006. The "(2008)" in the English title is not the date it was passed. In the examination write "Electronic Transactions Act, 2063". **Section 46.** Some English copies of the Act print the fine for section 46 as "two thousand rupees". The Nepali text says दुई लाख, two lakh rupees; write **Rs 2 lakh**.
:::

**Where to complain.** Cyber crimes are reported to the **Cyber Bureau of Nepal Police** at Bhotahiti, Kathmandu, or to the nearest police office. Keep screenshots, links, phone numbers and dates as evidence.

**Other laws and policies.** The **Copyright Act, 2059 (2002)** protects creative works and software; the **Individual Privacy Act, 2075 (2018)** protects personal information; and the government adopted a **National Cyber Security Policy, 2080** on 8 August 2023. A new Information Technology and Cyber Security Bill has been prepared to replace the ETA, but until Parliament passes such a law, the ETA 2063 remains Nepal's cyber law.

::: example Worked example 12.4 — name the offence and the section
**Problem.** Under which section of the ETA 2063 does each act fall, and what is the maximum punishment? (a) Kiran guesses his neighbour's Facebook password and logs in to read her messages. (b) A man posts edited obscene pictures of a woman on a website. (c) A former employee deletes all the records on a cooperative's server to cause it loss. (d) Someone uses another person's ATM card details to pay his own bills.

**Solution.** (a) Unauthorised access, **section 45**: a fine up to Rs 2 lakh, or up to 3 years, or both. (b) Publication of illegal (obscene) material, **section 47**: a fine up to Rs 1 lakh, or up to 5 years, or both. (c) Damage to a computer and information system, **section 46**: a fine up to Rs 2 lakh, or up to 3 years, or both. (d) Computer fraud, **section 52**: the money is recovered for the victim, plus a fine up to Rs 1 lakh, or up to 2 years, or both.
:::

::: tip Writing about the ETA in a long question
Start with the full name and year, "Electronic Transactions Act, 2063", and one line on why it was made. Then give **two aims** and **two or three offences**, each with its **section number** and **punishment**. A table of section, offence and punishment earns the marks quickly and is easy for the marker to check.
:::

## 12.5 Digital citizenship and safe use of social media

::: definition Digital citizen
A **digital citizen** is a person who uses the Internet and digital technology **responsibly, safely and respectfully**: who protects their own data, respects other people online, obeys the law, and uses technology to learn and to help others.
:::

```figure caption="Six habits of a good digital citizen."
fig, ax = cards([("Respect", "follow netiquette;\nnever bully"), ("Safety", "strong passwords,\nMFA, updates"), ("Privacy", "keep personal\ndetails private"), ("Truth", "check facts\nbefore sharing"), ("Footprint", "think before you post:\nit stays online"), ("Balance", "limit screen time;\nsleep, play, read")], cols=3)
```

### Netiquette

**Netiquette** (from *network* and *etiquette*) is the set of rules of good manners online. Be polite and respectful; do not write in ALL CAPITALS (it reads as shouting); do not send spam or flood a group with forwards; respect other people's privacy and never share their photos or numbers without permission; give credit when you share someone's work; think before posting; report abusive behaviour; and accept polite criticism.

### Your digital footprint

Your **digital footprint** is the record of everything you do online: posts, photos, comments, likes, searches, purchases and the places your phone has been. An **active footprint** is what you share on purpose, such as a post or a comment. A **passive footprint** is collected without you noticing, such as your search history, your location or the websites you visit. A footprint is hard to erase: a deleted post may already have been copied, and a school or an employer may see it years later.

| Active digital footprint | Passive digital footprint |
|---|---|
| left knowingly | collected without your knowledge |
| you choose what to share | websites and apps record it |
| examples: posts, comments, photos, e-mails | examples: search history, location data, cookies, online shopping records |

### Safe use of social media

Facebook, Instagram, TikTok and Snapchat require users to be **at least 13 years old**. Whatever your age, follow these rules.

1. **Lock your account**: a long, unique password for every account, and **multi-factor authentication (MFA)**, which asks for a second proof of identity — something you *know* (password, PIN), something you *have* (your phone receiving a code) or something you *are* (fingerprint, face).
2. **Set your profile to private** and accept friend requests only from people you know in real life.
3. **Keep personal details private**: your address, phone number, school timetable, live location, and photos of your ID card or citizenship.
4. **Think before you post**: would you be happy for your parents, teachers or a future employer to see it?
5. **Check before you share**: is the news from a trusted source? Fake news and edited pictures spread fastest.
6. **Never meet an online friend alone**; tell a parent if anyone online makes you uncomfortable or asks for photos.
7. **Never share an OTP, MPIN or password**, and log out of shared computers.
8. **Browse safely**: look for `https` and the padlock in the address bar before typing a password, and keep apps and the operating system updated.
9. **Block and report** bullies, scammers and fake accounts, and keep screenshots as evidence.

```photo id="cs8/eth-https-padlock" caption="The padlock and https:// at the start of a web address show that the connection is encrypted: what you type travels in secret code. A phishing site can also have a padlock, so check the spelling of the address as well." width="62"
```

::: example Worked example 12.5 — a strong password and a safe post
**Problem.** (a) Rita's password is `rita2010`. Why is it weak? Suggest a strong one. (b) She wants to post a photo of her new school ID card, with her name, class, school and her father's phone number on it. What should she do?

**Solution.** (a) It is short, uses her own name and probably her birth year, and has no capital letters or symbols, so it can be guessed in seconds. A strong password is long and unpredictable, for example a passphrase of unrelated words with symbols and numbers such as `Tea-Kite-Rhino-47!Mango`; she should use it only for one account and switch on MFA. (b) She should **not** post the ID card: it shows her identity, school and a phone number that a stranger could use to find or cheat her family. She can post a photo of herself at school without the card, shared only with friends.
:::

::: note Activity 12.1 — a digital-safety check-up
Work in pairs. (1) With a parent's permission, open the privacy settings of one app your family uses and note who can see posts, photos and the friend list. (2) Write five warning signs of a phishing message on a chart and stick it near the computer lab. (3) Collect three news items forwarded in your family groups this week and check one of them on a trusted news website. Was it true? (4) Make a poster of the Ten Commandments of computer ethics with an example of each, drawn from your own school life.
:::

## Chapter summary

- **Computer ethics** are the moral rules for using computers; **laws** are enforced by the state. Every cyber crime is unethical, but not every unethical act is a crime.
- The **Ten Commandments** (Computer Ethics Institute, 1992): do not harm, interfere, snoop, steal, lie, copy paid software, use others' resources or take others' work; think about society; respect others.
- **Cyber crime** is any illegal act done with a computer or the Internet: hacking, phishing, cyber bullying, identity theft, software piracy, online fraud.
- **Intellectual property** is protected by copyright, patents, trademarks and designs. In Nepal copyright lasts for the author's life plus 50 years (Copyright Act, 2059); **plagiarism** is using work without credit.
- Nepal's cyber law is the **Electronic Transactions Act, 2063**, authenticated 22 Mansir 2063 (8 December 2006): 12 chapters, 80 sections, offences in sections 44–59.
- Key punishments: s.44 source code and s.45 unauthorised access and s.46 damage — up to Rs 2 lakh or 3 years or both; s.47 illegal material — up to Rs 1 lakh or 5 years or both; s.52 fraud — Rs 1 lakh or 2 years or both. Report to the **Cyber Bureau** of Nepal Police.
- A **digital citizen** follows netiquette, protects privacy, uses strong passwords and MFA, thinks before posting, checks facts and manages a **digital footprint** (active and passive).

## Practice questions

**Group A — Objective (1 mark each)**

1. Computer ethics means <span class="marks">[1]</span>
   (a) the laws about computers (b) moral principles for using computers (c) the history of computers (d) a kind of computer virus
2. The Ten Commandments of Computer Ethics were published by the <span class="marks">[1]</span>
   (a) Computer Ethics Institute (b) Nepal Telecom (c) Microsoft (d) United Nations
3. "Do not snoop around in other people's computer files" means you should not <span class="marks">[1]</span>
   (a) delete your own files (b) look into others' files without permission (c) back up your files (d) share your own files
4. Getting into someone's computer or account without permission is <span class="marks">[1]</span>
   (a) phishing (b) hacking (c) plagiarism (d) netiquette
5. A fake message that tricks you into giving your password or OTP is called <span class="marks">[1]</span>
   (a) a firewall (b) phishing (c) a cookie (d) a backup
6. Copying and selling a paid program without its licence is <span class="marks">[1]</span>
   (a) freeware (b) software piracy (c) open source (d) shareware
7. Submitting a classmate's assignment as your own is <span class="marks">[1]</span>
   (a) plagiarism (b) a patent (c) a trademark (d) a digital signature
8. In Nepal, copyright normally lasts for <span class="marks">[1]</span>
   (a) 10 years (b) the author's life plus 50 years (c) 100 years after publication (d) for ever
9. The cyber law of Nepal is the <span class="marks">[1]</span>
   (a) Copyright Act, 2059 (b) Electronic Transactions Act, 2063 (c) Individual Privacy Act, 2075 (d) Patent, Design and Trademark Act, 2022
10. Under section 47 of the ETA, publishing hateful or obscene material online can be punished with up to <span class="marks">[1]</span>
    (a) Rs 10,000 or 6 months (b) Rs 1 lakh or 5 years or both (c) Rs 50,000 or 1 year (d) a warning only
11. Complaints about cyber crime in Nepal are taken by the <span class="marks">[1]</span>
    (a) Cyber Bureau of Nepal Police (b) Nepal Rastra Bank (c) Election Commission (d) Department of Passports
12. The record of everything you do online is your <span class="marks">[1]</span>
    (a) digital divide (b) digital footprint (c) digital signature (d) digital wallet
13. Which is the strongest password? <span class="marks">[1]</span>
    (a) 123456 (b) ramesh2010 (c) password (d) Kite-Rhino-47!Mango

::: note Answers to Group A
**1.** (b) — ethics are moral rules; laws are made by the state.
**2.** (a) — Computer Ethics Institute, Washington, D.C., 1992.
**3.** (b) — commandment 3: do not look into others' files.
**4.** (b) — hacking; punished under section 45 of the ETA.
**5.** (b) — phishing pretends to be a trusted company.
**6.** (b) — software piracy breaks the copyright in a computer program.
**7.** (a) — plagiarism is using work without credit.
**8.** (b) — Copyright Act, 2059: life of the author plus 50 years.
**9.** (b) — the ETA 2063 deals with electronic records and computer crimes.
**10.** (b) — section 47: up to Rs 1 lakh or 5 years or both.
**11.** (a) — the Cyber Bureau of Nepal Police, Bhotahiti.
**12.** (b) — the digital footprint; it can be active or passive.
**13.** (d) — long, mixed characters and not a name or a sequence.
:::

**Group B — Short answer (2 marks each)**

1. What is computer ethics? Write any two commandments of computer ethics. <span class="marks">[2]</span>
2. Differentiate between ethics and law with two points. <span class="marks">[2]</span>
3. What is hacking? Under which section of the ETA 2063 is unauthorised access punished, and what is the maximum punishment? <span class="marks">[2]</span>
4. What is phishing? Write any two signs of a phishing message. <span class="marks">[2]</span>
5. What is cyber bullying? Write two things a student should do if bullied online. <span class="marks">[2]</span>
6. Differentiate between copyright infringement and plagiarism. <span class="marks">[2]</span>
7. What is software piracy? Write two harms of it. <span class="marks">[2]</span>
8. Write the full name of Nepal's cyber law and the date it was authenticated. Name two things to which it gives legal recognition. <span class="marks">[2]</span>
9. What is a digital footprint? Give one example each of an active and a passive footprint. <span class="marks">[2]</span>
10. Write any four rules for the safe use of social media. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Computer ethics is the set of moral principles that guide how we use computers, networks and the Internet. Commandments (any two): do not use a computer to harm other people; do not snoop in other people's files; do not use a computer to steal; do not copy or use paid software you have not paid for; always use a computer with respect for others.

**2.** Ethics are moral rules followed by choice, from conscience; laws are made by the state and everyone must obey them. Breaking an ethical rule brings shame or loss of trust; breaking a law brings a fine, prison or both.

**3.** Hacking is getting into a computer, network or account without the owner's permission. Unauthorised access is punished under **section 45** of the ETA 2063, with a fine up to **Rs 2 lakh**, or prison up to **3 years**, or both.

**4.** Phishing is tricking people into giving their passwords, PINs, OTPs or card numbers through a fake message that seems to come from a trusted company. Signs (any two): a strange or misspelt web address; a demand for a password, MPIN or OTP; panic and a short deadline; "Dear customer" instead of your name; spelling mistakes; a prize that is too good to be true.

**5.** Cyber bullying is using phones, chat or social media to repeatedly hurt, threaten or shame someone. The student should (any two): not reply; keep screenshots as evidence; block and report the bully on the app; tell a parent or teacher (and the police in serious cases).

**6.** Copyright infringement is copying or using a work without the owner's permission; it is a legal offence under the Copyright Act. Plagiarism is using someone's work without giving credit; it is an ethical and academic offence. (Giving credit does not make unlicensed copying legal; permission does not make uncredited copying honest.)

**7.** Software piracy is copying, selling or using software without the owner's licence. Harms (any two): the programmers lose the money they earned; pirated copies often carry viruses; they get no security updates; it is illegal under the Copyright Act.

**8.** The **Electronic Transactions Act, 2063**, authenticated and published on **22 Mansir 2063 BS (8 December 2006)**. It gives legal recognition to **electronic records** and **digital signatures**.

**9.** A digital footprint is the record of everything a person does online. Active: a post, comment or photo you share on purpose. Passive: your search history, location data or cookies recorded without your notice.

**10.** Any four: use a strong, unique password and MFA; keep the profile private and accept only people you know; never share your address, phone number, location or ID card; think before posting; check facts before sharing; never share an OTP or MPIN; never meet an online friend alone; block and report bullies and fake accounts.
:::

**Group C — Long answer (4 marks each)**

1. What is computer ethics? Explain any six of the Ten Commandments of computer ethics with an example of each. <span class="marks">[1+3]</span>
2. What is cyber crime? Explain any three cyber crimes, with an example and one way of protection for each. <span class="marks">[1+3]</span>
3. Describe the Electronic Transactions Act, 2063: when it was made, its aims, and any three offences with their punishments. <span class="marks">[4]</span>
4. What is intellectual property? Explain copyright and plagiarism. How can a student avoid plagiarism in a project? <span class="marks">[1+2+1]</span>
5. Who is a digital citizen? Explain netiquette and any four rules for the safe use of social media. <span class="marks">[1+3]</span>

::: note Answers to Group C
**1.** Computer ethics is the set of moral principles that guide the use of computers, networks and the Internet (1 mark). Any six, half a mark each: (1) do not use a computer to harm others — e.g. posting a photo to embarrass a classmate; (2) do not interfere with others' computer work — e.g. switching off a friend's computer while she works; (3) do not snoop in others' files — e.g. opening a classmate's folder; (4) do not use a computer to steal — e.g. moving money with a stolen PIN; (5) do not tell lies with a computer — e.g. spreading a false rumour; (6) do not use paid software you have not paid for — e.g. a cracked game; (7) do not use others' computer resources without permission — e.g. printing your notes on the office printer without asking; (8) do not take others' work as your own — e.g. submitting a copied essay; (9) think about the social effects of your programs; (10) respect other people online.

**2.** Cyber crime is any illegal act done by means of a computer, phone, network or the Internet (1 mark). Any three (1 mark each): *Hacking* — entering a computer or account without permission, e.g. breaking into a result system to change marks; protect with strong passwords, MFA and updates. *Phishing* — fake messages that trick people into giving passwords or OTPs, e.g. "your eSewa account is blocked, verify here"; never click unknown links or share an OTP. *Cyber bullying* — repeatedly hurting someone online, e.g. a fake profile to mock a classmate; block, report, keep evidence and tell an adult. *Identity theft* — pretending to be someone using their details, e.g. a fake profile asking friends for money; keep personal details private. *Software piracy* — using software without a licence, e.g. cracked Windows; buy licences or use free software.

**3.** The **Electronic Transactions Act, 2063** is Nepal's cyber law. It was authenticated and published on **22 Mansir 2063 BS (8 December 2006)** and has 12 chapters and 80 sections (1 mark). *Aims* (1 mark): to give legal recognition to electronic records and digital signatures; to make electronic transactions secure and reliable; to set up a Controller and Certifying Authorities for digital signature certificates; to control computer crimes. *Offences* (2 marks, any three): s.44 pirating, destroying or altering source code — up to 3 years or Rs 2 lakh or both; s.45 unauthorised access — up to Rs 2 lakh or 3 years or both; s.46 damage to a computer and information system — up to Rs 2 lakh or 3 years or both; s.47 publishing illegal material in electronic form — up to Rs 1 lakh or 5 years or both; s.52 computer fraud — recovery of the money plus up to Rs 1 lakh or 2 years or both. Cases go to a three-member IT Tribunal (law, IT, commerce).

**4.** Intellectual property is a creation of the mind, such as a book, song, photo, program, invention or brand name; the rights that protect it are intellectual property rights (1 mark). *Copyright* is the legal right of a creator to copy, publish and sell an original work and stop others; it is automatic, and in Nepal lasts for the author's life plus 50 years under the Copyright Act, 2059, which also protects computer programs. *Plagiarism* is presenting someone else's words, ideas or work as your own without credit, e.g. copying a website paragraph into a project (2 marks). *To avoid plagiarism* (1 mark): write in your own words; put exact words in quotation marks and name the source; list all sources in a bibliography; ask permission before using others' photos.

**5.** A digital citizen is a person who uses the Internet and digital technology responsibly, safely and respectfully (1 mark). *Netiquette* is good manners online: be polite, do not write in capitals, do not spam, respect others' privacy, give credit, think before posting (1 mark). *Safe use of social media* (2 marks, any four): strong unique passwords and MFA; private profile and friends you know; keep address, phone, location and ID private; think before posting; check facts before sharing; never share an OTP or MPIN; never meet online friends alone; block and report bullies and keep evidence.
:::
