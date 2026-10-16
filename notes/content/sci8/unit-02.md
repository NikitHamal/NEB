---
subject: Science and Technology
grade: 8
unit: 2
title: Information and Communication Technology
hours: 0
area: Science and Technology
---

Information and communication technology, or ICT, is the set of tools that
store information, move it from one place to another and let people talk to each
other. A mobile phone, a school computer, a radio mast, a bank's server and the
cable under the sea that joins Nepal to the rest of the internet are all parts
of one system. This unit looks at the tools, at how the internet actually
reaches your handset, at the dangers that come with it, and at three newer
ideas — robotics, virtual reality and artificial intelligence.

::: key What this unit asks of you
You should be able to name the tools of ICT and say what each is for, explain
what an ISP, a website and a search engine are, state the uses and risks of
social networking sites, describe the common forms of cybercrime and the rules
that protect you, and explain in simple words what robotics, virtual reality,
artificial intelligence and cloud computing are used for.
:::

## 2.1 Tools of information and communication technology

ICT tools can be sorted by the job they do.

| Job | Tools | What they do |
|---|---|---|
| Input | keyboard, mouse, microphone, scanner, camera | put information into a machine |
| Processing | computer, mobile phone, tablet, server | change, sort or calculate information |
| Output | monitor, printer, speaker, projector | give information back to a person |
| Storage | hard disk, pen drive, memory card, cloud storage | keep information for later |
| Communication | modem, router, Wi-Fi, optical fibre, mobile network, satellite | carry information from place to place |

Two of these deserve a closer look. **Optical fibre** carries information as
pulses of light through a glass thread thinner than a hair, which is why a
single fibre can carry thousands of telephone calls at once. A **satellite**
does the same job where no cable can go — across the high mountains of Nepal,
for example.

::: definition Information and communication technology
**ICT** is the use of computers, telecommunication devices and networks to
create, store, process, send and receive information.
:::

## 2.2 Search engine, website and ISP

These three words are used together so often that students mix them up.

- A **website** is a set of related pages kept on a computer called a server,
  with its own address. A website is a place where information lives.
- A **search engine** is a website whose job is to find other pages. You type
  words, and it returns a list of pages that contain them. Google, Bing and
  DuckDuckGo are search engines.
- An **ISP**, or internet service provider, is the company that sells you the
  connection itself — WorldLink, Vianet and Nepal Telecom are Nepali examples.
  Without an ISP you can reach the local network but not the world.

### 2.2.1 How the internet reaches your handset

```figure caption="The path an internet page takes to reach a phone. Every link in the chain is somebody's equipment: the ISP's, the country's and finally yours."
fig, ax = plt.subplots(figsize=(5.0, 2.7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.6)
ax.axis("off")
boxes = [("Website's\\nserver", 1.0, "far away"), ("ISP\\nof the site", 3.0, ""),
         ("Optical fibre\\nor satellite", 5.0, ""), ("Your ISP", 7.0, ""),
         ("Router /\\nWi-Fi", 9.0, "")]
for name, x, note in boxes:
    ax.text(x, 3.6, name, ha="center", va="center", fontsize=6.9, color=INK,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=ACCENT, lw=1.0))
    if note:
        ax.text(x, 2.7, note, ha="center", va="center", fontsize=6.3, color=MUTED)
for i in range(4):
    x = 1.0 + i * 2.0
    ax.annotate("", xy=(x + 1.35, 3.6), xytext=(x + 0.62, 3.6),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
ax.text(9.0, 1.5, "your phone", ha="center", fontsize=6.8, color=SERIES[1],
        bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=SERIES[1], lw=1.0))
ax.annotate("", xy=(9.0, 1.95), xytext=(9.0, 3.15),
            arrowprops=dict(arrowstyle="->", color=SERIES[1], lw=1.1))
ax.text(5.0, 0.6, "a break anywhere in this chain stops the page from opening",
        ha="center", fontsize=6.7, color=MUTED)
fig.tight_layout()
```

### 2.2.2 Reading a website address

An address such as `https://www.moecdc.gov.np/content/72/` is read in parts:
`https` is the rule for the conversation (the "s" means the traffic is
encrypted), `www` is the name of the server, `moecdc` is the organisation,
`gov` says it is a government body and `np` says the country is Nepal. The last
part, `/content/72/`, is the page inside the site.

| Ending | Belongs to |
|---|---|
| .gov.np | a Nepali government office |
| .edu.np | a Nepali school, college or university |
| .org.np | a Nepali non-profit organisation |
| .com.np | a Nepali company |
| .com, .org | an international company or organisation |

::: caution A page is not automatically true
Anyone can publish on the internet. Before you use a fact in your report, ask:
who wrote this, when, and what is their source? A government site, a school site
or an encyclopedia with references is more dependable than an anonymous post.
:::

```photo id="sci10/motherboard" caption="A computer motherboard. The processor, memory slots and ports all sit on this single board." width="70"
```

## 2.3 Social networking sites

A **social networking site** lets a person make a profile, put things on it and
connect with others. Facebook, TikTok, Instagram, YouTube and X are the ones
most used by students in Nepal. They are not good or bad in themselves; what
they do depends on how they are used.

| Good uses | Risks |
|---|---|
| staying in touch with family living abroad | wasting study hours without noticing |
| sharing school projects, notes and results | cyberbullying and insulting comments |
| learning skills from free videos | personal information reaching strangers |
| small businesses finding customers | fake accounts in your name |
| news and public notices quickly | wrong news spreading faster than the correction |

::: tip A five-question rule before you post
Would I say this to the person's face? Would I be happy if my teacher and my
parents saw it? Does it give away my address, school, phone number or daily
routine? Will I still be happy about it in one year? If any answer is no, do not
post it. Things put on the internet are very hard to remove.
:::

## 2.4 Cybercrime, code of conduct and internet security

**Cybercrime** is a crime committed using a computer, a mobile phone or the
internet. The law that deals with it in Nepal is the Electronic Transactions
Act, 2063.

| Form of cybercrime | How it works | How to stay safe |
|---|---|---|
| Online fraud | a prize, a lottery or a job offer, then a request for money or details | never pay or send details to someone who contacted you first |
| Phishing | a message that looks like your bank or a government office, asking you to "confirm" a password | banks never ask for a password or PIN |
| Fake profile | someone opens an account in your name with your photograph | keep photographs private; report the account |
| Cyberbullying | repeated insulting or threatening messages | do not reply, save the evidence, tell an adult |
| Hacking | breaking into an account or a computer | strong password, two-step verification, do not use unknown cables or apps |
| Unlawful download | copying films, games or books without permission | use legal sources |
| Cyberstalking | an unknown person tracking your movements and messages | do not share your location; block and report |

### 2.4.1 Code of conduct

A **code of conduct** is the agreed set of behaviour rules for using a computer
or the internet. Your school's computer room will have one. The usual points
are: use the machine for study during study hours; do not open another person's
files; do not install software without permission; do not use someone else's
password; do not copy work and present it as your own; and do not post
photographs of others without their consent.

### 2.4.2 Nine practices that keep an account safe

1. Use a password of at least eight characters with letters, numbers and
   symbols; never use your name or date of birth.
2. Never share a password, not even with a close friend.
3. Turn on two-step verification.
4. Log out, especially on a shared computer.
5. Do not open links or attachments from unknown senders.
6. Keep the phone and computer updated.
7. Check a link before clicking it — university prizes do not arrive by SMS.
8. Use only your own Wi-Fi; do not break into another's.
9. If money or photographs are involved, tell a parent, teacher or the police
   cyber bureau at once. Delay is what the criminal needs.

```figure caption="Two columns, one decision. Almost every online fraud starts in the left column and succeeds because the message creates hurry or excitement in the person reading it."
fig, ax = plt.subplots(figsize=(5.0, 2.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
ax.text(2.6, 5.5, "What the criminal sends", ha="center", fontsize=7.4, color=SERIES[1])
ax.text(7.4, 5.5, "What you do", ha="center", fontsize=7.4, color=ACCENT)
pairs = [("You have won Rs 5 lakh", "Stop. Nobody gives money away"),
         ("Send your bank details", "Banks never ask. Never send"),
         ("Click this link quickly", "Check the address first"),
         ("Your account will close", "The message wants you to hurry"),
         ("A friend needs a loan", "Call the friend on the phone")]
for i, (left, right) in enumerate(pairs):
    y = 4.6 - i * 0.92
    ax.text(2.6, y, left, ha="center", va="center", fontsize=6.5, color=INK,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=SERIES[1], lw=0.8))
    ax.annotate("", xy=(5.4, y), xytext=(4.75, y),
                arrowprops=dict(arrowstyle="->", color=GRID, lw=0.9))
    ax.text(7.4, y, right, ha="center", va="center", fontsize=6.5, color=INK,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=ACCENT, lw=0.8))
fig.tight_layout()
```

::: example Worked case: the prize message
**Situation.** Sunita, a Class 8 student, receives a message: "Congratulations!
Your number has won Rs 5,00,000 in the Ncell anniversary draw. To receive the
money, send your name, your father's mobile number and your bank account number
to this WhatsApp number."

**Analysis.**
1. She never entered any draw, so there was no ticket to win.
2. Real companies publish winners on their own website; they do not ask for a
   bank account to give money.
3. A genuine transfer needs only the account number of the *receiver*. Asking
   for more means the sender wants to take money out, not put it in.
4. The message creates excitement and urgency, which is the standard trick.

**What she should do.** Take a screenshot, do not reply, block the number,
report it to the cyber bureau (the police's cyber section) with her parents, and
tell her classmates so that they recognise the same message.

**What would have happened.** If she had sent the details, the fraudster would
have used the number and account for a "KYC update" call and emptied the
account.
:::

```photo id="sci10/router" caption="A wireless router. It connects the devices of a home or school to the internet." width="62"
```

## 2.5 Robotics and virtual reality

A **robot** is a machine that can sense its surroundings, decide what to do and
act — usually repeating a job with great accuracy. Robots are built from a
controller, sensors, motors and a power supply, and they are programmed by a
person.

| Where robots are used | What they do |
|---|---|
| Industry | welding, painting and assembling, faster and safer than people |
| Hospital | very fine surgery, moving medicine |
| Farm | spraying, planting, picking |
| Home | vacuum cleaners, washing machines with sensors |
| Rescue | entering a collapsed building or a flooded area |
| Space | rovers on Mars and the Moon; Nepal's own first satellite was a CubeSat |

A **drone** is a flying robot. In Nepal drones are used to carry loads to
villages in the high mountains where no road reaches, and to survey land and
crops.

**Virtual reality (VR)** puts a person inside a computer-made world using a
headset, so that the eyes and ears receive a scene that is not really there.
**Augmented reality (AR)** does the opposite: it adds computer-made objects on
top of the real world seen through a phone camera. A student can dissect a frog
in VR without harming a frog, or see a three-dimensional model of the heart on
the desk in AR.

::: caution VR is a tool, not a substitute
A VR laboratory is useful for practice and for showing things that are too
expensive or too dangerous to bring into a school. It cannot teach you to hold
a burette steady in your hand or to notice the smell of a burning wire. Use it
beside the real laboratory, not instead of it.
:::

## 2.6 Artificial intelligence and cloud computing

**Artificial intelligence (AI)** is the branch of computer science that makes a
machine able to do tasks that used to need a human mind: recognising a face,
understanding speech, translating a language, or suggesting what you might want
to watch next.

The commonest kind of AI today is **machine learning**. Instead of being told
the rules, the computer is shown a large number of examples and works out the
pattern itself.

| Task | How the machine learnt it |
|---|---|
| Recognising Nepali handwriting | shown thousands of examples of each letter |
| Translating Nepali into English | shown millions of sentence pairs |
| Suggesting a video | shown what millions of other people watched |
| Detecting a disease from an X-ray | shown thousands of X-rays with the doctor's answer |

**Cloud computing** means using somebody else's computers through the internet
instead of buying your own. When you keep a file in Google Drive, or use an app
that runs on a distant server, you are using the cloud. Its advantages are that
nothing is lost when your phone breaks and you can reach the same file from any
device; its risks are that you need an internet connection, and that somebody
else's computer holds your private information.

::: example Worked reasoning: "is this AI or just a program?"
**Question.** A school keeps the marks of every student in a spreadsheet. It
prints a list of students who got less than 40 % in mathematics. Is this AI?

**Answer.** No. The rule "marks less than 40" was decided by a person and typed
in by a person. The computer only followed the rule.

**Question.** The same school uses an app that watches each student's attendance
and homework submission and gives a warning about students who are likely to
fail. Is this AI?

**Answer.** Probably yes. Nobody wrote the rule "a student who misses Tuesday
mornings and does not submit homework on time will fail". The app was given past
data and worked out which patterns came before failure. That is machine
learning.

**The test.** If a person can write the rule as a sentence, it is ordinary
programming. If the rule is one nobody can write down but the machine found it
in the data, it is machine learning.
:::

## 2.5 Staying safe and useful online

A computer is a tool for study long before it is a tool for entertainment.
Knowing what each part does, and what each risk looks like, is the whole of
this chapter in practice.

| Risk | How it reaches you | What to do |
|---|---|---|
| Malware | a link, a pirated file, an unknown pen drive | install nothing from unknown sources; scan drives |
| Phishing | a message that asks for a password or OTP | no genuine service ever asks for an OTP |
| Weak password | reused, short, guessable | long, mixed, different for each account |
| Over-sharing | address, school, daily routine posted | keep the account private; post nothing live |
| Cyberbullying | messages meant to hurt | keep the evidence, block, tell an adult |
| Eye and posture strain | hours at a screen | the 20-20-20 rule; screen at eye level |

```figure caption="The 20-20-20 rule for screen work: every 20 minutes, look at something 20 feet away for 20 seconds. It is the cheapest protection a student has."
fig, ax = flow([("20 minutes", "of screen work"), ("20 feet", "look far away"),
                ("20 seconds", "let the eyes relax")],
               note="also: screen at eye level, feet flat, back supported")
```

::: example A four-mark answer on safe use
**Question.** Write four rules for the safe use of the internet by a
Grade 8 student.

**Answer.** (i) **Passwords** — keep a long, mixed password, different for
each account, and never share it, not even with a close friend.
(ii) **Personal information** — never post an address, a school name with
a routine, or a live location; keep the account private.
(iii) **Links and files** — do not open a link or attachment from a
stranger, and never enter a one-time password anywhere a message asks you
to. (iv) **Behaviour and help** — do not forward what you have not
verified, do not reply to bullying; save the evidence and tell a parent or
teacher.
:::

## Chapter summary

- ICT is the use of computers and networks to create, store, process and send
  information; its tools divide into input, processing, output, storage and
  communication.
- A **website** is a place holding information, a **search engine** finds pages,
  and an **ISP** sells the connection.
- The internet reaches you through a chain: server, the site's ISP, optical
  fibre or satellite, your ISP, your router and your device.
- Social networking sites give real benefits and real risks; personal
  information, bullying, fake profiles and lost study time are the main dangers.
- Cybercrime includes online fraud, phishing, fake profiles, cyberbullying,
  hacking and cyberstalking. The Electronic Transactions Act, 2063 governs it in
  Nepal.
- A strong password, two-step verification, no unknown links and telling an
  adult quickly are the four habits that prevent most harm.
- Robots sense, decide and act; virtual reality replaces the world, augmented
  reality adds to it.
- AI does by example what people cannot write as a rule; cloud computing uses
  other people's computers through the internet.

## Practice questions

**Group A — Objective (1 mark each)**

1. Which of these is an ISP? <span class="marks">[1]</span>
   (a) Google (b) WorldLink (c) Facebook (d) Wikipedia
2. The part of a computer that gives information back to the user is the
   <span class="marks">[1]</span>
   (a) input device (b) storage device (c) output device (d) processor
3. A website address ending in `.edu.np` belongs to
   <span class="marks">[1]</span>
   (a) a government office (b) an educational institution (c) a company
   (d) an individual
4. Sending a message that pretends to be from a bank in order to obtain a
   password is called <span class="marks">[1]</span>
   (a) hacking (b) phishing (c) cyberbullying (d) spamming
5. Keeping files on a distant server instead of on your own device is called
   <span class="marks">[1]</span>
   (a) cloud computing (b) virtual reality (c) robotics (d) optical fibre
6. A machine that senses its surroundings, decides and acts is a
   <span class="marks">[1]</span>
   (a) printer (b) robot (c) router (d) scanner

::: note Answers to Group A
**1.** (b) — an ISP sells the internet connection itself.
**2.** (c) — a monitor or printer is an output device.
**3.** (b) — `.edu` marks an educational institution.
**4.** (b) — phishing is the fake identity trick.
**5.** (a) — the computing happens on someone else's machine.
**6.** (b) — that is the definition of a robot.
:::

**Group B — Short answer (2 marks each)**

1. Write any four tools of ICT and say what each is used for.
   <span class="marks">[2]</span>
2. What is the difference between a search engine and an ISP?
   <span class="marks">[2]</span>
3. Write any four rules from a school's computer code of conduct.
   <span class="marks">[2]</span>
4. State two good uses and two risks of social networking sites.
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Any four of: keyboard (input of text and numbers); monitor (output of
information); pen drive (storage and carrying files); printer (printing
documents); router (sharing a connection); modem (converting the line signal
for the computer); microphone (input of sound).
**2.** A search engine is a website that finds other pages by the words you
give; an ISP is the company that provides the connection that lets you reach
those pages at all.
**3.** Any four of: use the computer for study during study hours; do not open
another student's files; do not install software without permission; do not use
another person's password; do not copy work and present it as your own; do not
post photographs of others without consent.
**4.** Uses: keeping in touch with relatives abroad; sharing school work and
learning from videos. Risks: cyberbullying; personal information reaching
strangers.
:::

**Group C — Long answer (4 marks each)**

1. A message on your phone says, "Your Facebook account will be closed today.
   Click this link and enter your password to keep it." Explain why this message
   is a fraud, and write the four steps you would take.
   <span class="marks">[4]</span>
2. What is artificial intelligence? Give two real uses of AI in Nepal or for
   Nepali users, and one danger of trusting an AI answer without checking it.
   <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Why it is a fraud.** A real company never asks for a password by
message, because the company already has your account; a link that promises to
"keep" an account is asking you to hand over the key yourself; the words
"today" and "will be closed" are there to create hurry, which is the standard
trick of phishing. **Steps.** (1) Do not click the link; take a screenshot.
(2) Open the site by typing its address yourself or through the official app, and
check whether anything is really wrong. (3) Change the password from inside the
site and turn on two-step verification. (4) Report the message to the site and
tell your parents or teacher; if money is involved, inform the police cyber
bureau.
**2.** **AI** is the branch of computing that makes machines able to do work
that needs human-like judgement, such as understanding speech or recognising
an image. **Two uses.** (i) Nepali speech-to-text and translation, which helps
people use services in their own language. (ii) Crop and weather advice sent to
farmers' phones, and handwriting recognition in school apps. **One danger.** An
AI answer can be confidently wrong: it produces fluent sentences, not verified
facts, so a student who copies it without checking a textbook or a reliable site
can write a fact that is simply false. AI is a helper for finding and shaping
information, not a source of truth.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** Which of these is an input device?
   (a) printer (b) monitor (c) scanner (d) speaker
**2.** The memory whose contents vanish when the power fails is
   (a) ROM (b) RAM (c) hard disk (d) pen drive
**3.** One kilobyte equals
   (a) 1000 bits (b) 1024 bytes (c) 100 bytes (d) 1024 bits
**4.** Which is a web browser?
   (a) Google (b) Firefox (c) Windows (d) Excel
**5.** The safest password of these is
   (a) 123456 (b) your own name (c) Sa#9rLm2!qd (d) password

::: note Objective practice — answers
**1.** (c) — a scanner feeds data in. **2.** (b) — RAM is volatile. **3.** (b) — $2^{10}$ bytes. **4.** (b) — Firefox; Google is a search engine. **5.** (c) — long, mixed and not guessable.
:::
