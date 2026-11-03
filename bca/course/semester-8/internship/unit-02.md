---
subject: Internship
grade: BCA Semester 8
unit: 2
title: Workplace Conduct: First Day, Etiquette, Confidentiality and Safety
area: BCA 452 · Internship · Unit 2
---

The offer letter is signed and Anisha's first Sunday in Magh is a week away. Nobody at Himal Digital will examine her on algorithms during the first week. They will watch something simpler: **does she arrive on time, listen, ask good questions, and handle other people's information with care?** Technical skill can be taught in a month; trust takes a lifetime to rebuild once it is lost. This unit is about the habits that earn it.

::: key What this unit gives you
- A first-day and first-week checklist, and the unwritten rules of office communication.
- How to ask for help without wasting your supervisor's time: the **15-minute rule**.
- **Confidentiality**: what an NDA means, the four information levels, and an executed **secrets scanner** that finds passwords and personal data before they leave your laptop.
- Safe working: hours, posture, harassment and digital hygiene, with Nepali legal pointers.
- Real photographs of a shared work lounge and an ID badge, and eight habits that make interns trusted.
:::

## 2.1 The first day and the first week

A new workplace feels like an exam you did not revise for. Reduce the stress by treating the first week as a **checklist**. Arrive 15 minutes early on day one, carry your ID, a notebook and the college letter, and expect to wait; the supervisor may be in a client call.

| When | What to do | Why |
|---|---|---|
| Day 1 morning | meet supervisor, sign attendance, receive badge or access | confirms who you report to |
| Day 1 | get logins, ask which tools and chat channels are used | avoids a lost first week |
| Day 1 | read the office rules: hours, leave, dress, internet use | rules differ in each firm |
| Day 2 to 3 | shadow a developer; ask for one small starter task | learn the workflow |
| Day 3 | write the first log entry (Unit 3) and agree weekly meeting time | builds the habit early |
| End of week 1 | meet supervisor: confirm objectives L1 to L3 against real tasks | catches a mismatch while it can be fixed |

The last row matters most. If the firm cannot give you work that meets your objectives, say so politely in week one, and agree on a change. Silence turns a fixable mismatch into a failed internship.

## 2.2 Etiquette and communication

Offices run on small agreements that nobody writes down. Learn them by observing, and by asking once.

**Time.** Be at your desk at the start time, not at the door. Tell your supervisor before, not after, if you will be late or absent. Under the Labour Act 2074 the normal working day is eight hours and the week 48 hours at most; an internship should respect the hours agreed in writing, and extra hours should be your choice, not a silent expectation.

**Choosing the channel.** Use a chat message for a quick question with a short answer, email for anything that needs a record (decisions, files, client matters), a call or a desk visit for something confusing, and a meeting only when several people must decide. A good message is **complete in itself**: "The login page returns 500 after I submit. Log line attached. I have tried clearing the cache. Can you spare five minutes after lunch?" beats "it is not working".

**Meetings.** Arrive with a notebook. Write the decision and the action with your name against it. Speak when you have something specific; silence for six weeks is a lost opportunity.

**Asking for help: the 15-minute rule.** Try alone for 15 minutes with a clear notes page, then ask. Asking at minute two wastes the mentor's time; asking at hour three wastes yours. When you ask, show what you tried and what you expect.

**Feedback.** Say "thank you, I will fix that" and write it down. A review comment is about the code, not about you. Reply on the same day with the change made.

## 2.3 Confidentiality and data handling

Every organisation holds information it must not leak: client lists, source code, passwords, salaries, and personal data of customers. As an intern you will see all of it within a week. A **Non-Disclosure Agreement (NDA)** is a signed promise not to share such information. Even without an NDA, the duty exists in good practice and, for personal data, in law (the Individual Privacy Act 2075 and the Electronic Transactions Act 2063 give general pointers; ask your supervisor what the firm requires).

Sort information into four levels, as in Figure 2.1: **public** (published website text), **internal** (meeting notes, tickets), **confidential** (client data, source code) and **restricted** (passwords, keys, citizenship numbers). The higher the level, the fewer people, the fewer tools and the shorter the time it may live on your laptop. Never paste confidential code into a public chat tool or an online AI service without permission, and never put a real password in a Git commit.

That last mistake is common in beginners' repositories. A simple scanner can catch it before commit. The program below checks a small invented "diff" for four patterns: password assignments, API keys, Nepali mobile numbers and citizenship-style numbers. It prints the line number, the type found and a **masked** excerpt, because a scanner that prints the secret in its log has only moved the leak.

```python
import re
diff = '''\
+ def connect():
+     DB_PASSWORD = "Himal@2082!"
+     api_key = "sk_live_51HxQ2zAbCdEfGh"
+     return mysql.connect(host=DB_HOST)
+ # contact for the school: 9841234567
+ client_citizenship = "27-01-72-12345"
+ total = price * 1.13
'''
rules = [("password", r'(?i)password\s*=\s*"[^"]+"'),
         ("api key", r'(?i)api_?key\s*=\s*"[^"]+"'),
         ("mobile no.", r"\b9[78]\d{8}\b"),
         ("citizenship", r"\b\d{2}-\d{2}-\d{2}-\d{5}\b")]
def mask(text):
    return text[:6] + "*" * max(len(text) - 8, 3) + text[-2:]
hits = 0
for n, line in enumerate(diff.splitlines(), 1):
    for kind, pat in rules:
        m = re.search(pat, line)
        if m:
            hits += 1
            print(f"line {n}: {kind:<12} {mask(m.group())}")
print("findings:", hits, "-> block the commit" if hits else "-> clean")
```
```output
line 2: password     PASSWO****************!"
line 3: api key      api_ke***************************h"
line 5: mobile no.   984123***67
line 6: citizenship  27-01-******45
findings: 4 -> block the commit
```

*Reading the output.* Four of the seven lines are flagged: the password (line 2), the API key (line 3), the mobile number (line 5) and the citizenship-style number (line 6). The harmless lines, including `total = price * 1.13` (the 13 percent VAT rate), pass. Every excerpt is masked, so the log itself is safe to share. The right fix is **not** to delete the line and commit again, because Git history keeps the old version. The correct steps are: remove the secret from the code, read it from an environment variable, **change the leaked password**, and tell your supervisor the same day. Reporting your own slip quickly is a mark of a professional; hiding it is the failure.

```svgfig label="2.1" caption="Four information levels. The more sensitive the level, the fewer people may see it and the fewer places it may be stored. Restricted items such as passwords and citizenship numbers never go into code, chat or screenshots."
f = Fig(580, 230)
lv = [("Public", "website text,\nblog posts", "anyone", SOFT, TEAL), ("Internal", "meeting notes,\ntickets, wiki", "staff and interns", BLUE, NAVY),
      ("Confidential", "client data,\nsource code", "named team only", "#fde68a", AMBER), ("Restricted", "passwords, keys,\nIDs, salaries", "owner and admin", "#fecaca", RED)]
for i, (n, ex, who, fl, st) in enumerate(lv):
    x = 12 + i * 142
    h = 70 + i * 28
    f.box(x, 190 - h, 130, h, "", fill=fl, stroke=st)
    f.text(x + 65, 190 - h + 18, n, size=12, color=NAVY, bold=True)
    f.text(x + 65, 190 - h + 40, ex.split("\n")[0], size=9.5, color=NAVY)
    f.text(x + 65, 190 - h + 54, ex.split("\n")[1], size=9.5, color=NAVY)
    f.text(x + 65, 207, "Who: " + who, size=9.5, color=NAVY, bold=True)
f.arrow([(14, 24), (566, 24)], color=SLATE)
f.text(290, 12, "more sensitive: fewer people, fewer tools, shorter time on your laptop", size=10, color=NAVY, bold=True)
f.text(290, 224, "When unsure, treat it one level higher and ask.", size=9.5, color=SLATE, italic=True)
```

```photogrid label="2.1" cols="3" ratio="1.0" caption="Belonging and boundaries. (a) A shared lounge in a modern office: informal corners are good for quick questions, but screens facing the walkway can leak client data. (b) An ID badge on a lanyard: wear it where the firm requires, never lend it, and report loss the same day. (c) A reply-time guide: match the channel to the urgency."
@ photo id="bca452/cowork" cap="Shared office lounge"
fit 1.0
focus 0.5 0.5
call 0.5 0.85 0.5 0.65 "quiet corners to ask"
@ photo id="bca452/lanyard" cap="ID badge and lanyard"
fit 1.0
focus 0.5 0.5
call 0.5 0.85 0.5 0.65 "never lend your badge"
@ svg cap="Channel guide"
f = Fig(300, 300)
rows = [("Urgent, blocks others", "call or visit", "#fecaca", RED), ("Quick question", "chat message", "#fde68a", AMBER),
        ("Needs a record", "email + file", BLUE, NAVY), ("Several must decide", "short meeting", SOFT, TEAL)]
for i, (a, b, fl, st) in enumerate(rows):
    y = 20 + i * 68
    f.box(10, y, 280, 58, "", fill=fl, stroke=st)
    f.text(150, y + 20, a, size=13.5, color=NAVY, bold=True)
    f.text(150, y + 42, "use: " + b, size=13, color=NAVY)
```

## 2.4 Rights, safety and digital hygiene

**Your rights.** An intern is a learner, not free labour. Hours, tasks and any stipend should be written in the placement letter or an agreement; the Labour Act 2074 sets the general frame (the normal day is eight hours, overtime is paid, and discrimination and harassment are forbidden for workers). Ask your college coordinator what applies to interns, and keep copies of every signed paper.

**Respect and harassment.** Treat everyone, including cleaners and guards, with the same courtesy. Jokes about caste, gender, religion or appearance are never "just jokes". If you experience or see harassment, note the date and words, tell your coordinator or a trusted senior, and do not stay silent for fear of losing the placement. A placement that punishes a complaint is not worth finishing.

**Physical safety.** Sit with feet flat, screen at eye level, wrists straight, and take a two-minute break every 40 minutes. Know where the fire exit and first-aid kit are. For travel to a site visit, tell your supervisor the plan and return time.

**Digital hygiene.** Use the firm's accounts, not personal email, for work; lock the screen when you leave the desk (Windows + L); use unique passwords with a password manager and two-step verification; and never plug in an unknown USB drive. Public Wi-Fi is not for client work without a VPN.

```svgfig label="2.2" caption="The 15-minute rule as a flowchart. Try alone with notes first, search, then ask with your evidence; record the answer in the log so you never ask the same thing twice."
f = Fig(580, 170)
f.box(10, 60, 90, 50, "Stuck on\na task", fill=BLUE, stroke=NAVY, size=10.5, color=NAVY)
f.box(125, 60, 100, 50, "Try 15 min,\nwrite what\nyou tried", fill=SOFT, stroke=TEAL, size=10, color=NAVY)
f.box(250, 60, 90, 50, "Search docs,\nerror text", fill=SOFT, stroke=TEAL, size=10, color=NAVY)
f.box(365, 60, 100, 50, "Ask with\nevidence and\nexpected result", fill="#fde68a", stroke=AMBER, size=10, color=NAVY)
f.box(490, 60, 82, 50, "Log the\nanswer", fill=BLUE, stroke=NAVY, size=10.5, color=NAVY)
for a, b in ((100, 125), (225, 250), (340, 365), (465, 490)):
    f.arrow([(a, 85), (b, 85)], color=SLATE)
f.arrow([(295, 60), (295, 30), (75, 30), (75, 60)], color=TEAL, dash=True)
f.text(185, 22, "solved? go back to work", size=10, color=TEAL, bold=True)
f.text(290, 140, "Never: ask at minute 2, or hide for 3 hours.", size=10, color=SLATE, italic=True)
```

## 2.5 Eight habits that make an intern trusted

1. **Punctuality in small things.** Be on time for the start, for meetings and for promised deliveries. If you will be late, send one line before the time passes. A person who is reliable in small things is given bigger tasks, which is exactly what you came for.
2. **Write things down.** Keep one notebook for tasks, names, decisions and commands. When the supervisor explains the deployment steps once, you should never need to ask the same thing again. Notes also feed your daily log in Unit 3.
3. **Ask early, ask well.** Follow the 15-minute rule and include what you tried. Good questions show thinking and are answered faster. A supervisor remembers the intern who asked three sharp questions, not the one who asked thirty vague ones.
4. **Say "I do not know yet".** Pretending to know is dangerous in a live system. Say "I have not used this; can I have one hour to learn it?" and then do so. Honest learners are welcomed; bluffers are watched.
5. **Protect information.** Lock the screen, use the firm's accounts, and keep secrets out of code, chat and screenshots. If you make a slip, report it at once. Clients forgive an honest early report far more easily than a leak found later.
6. **Take feedback without arguing.** Write the comment, say thanks, fix it, and reply "done". Learn from repeated comments and avoid the same one twice. Code review is a gift of someone's time, not an attack.
7. **Finish what you start, and show it.** Small tasks finished and demonstrated beat big tasks half-done. Tell your supervisor when a task is complete and what you tested. A visible finish builds your portfolio and your reference letter.
8. **Be kind and visible.** Greet people, offer help with tasks outside your own, and thank those who helped you. Interns who are friendly with the whole team get better references and more chances to join real work.

## Formula and fact sheet

| Item | Rule or fact |
|---|---|
| First week | meet supervisor, logins, rules, shadow, first log, confirm objectives |
| 15-minute rule | try alone 15 min with notes, search, then ask with evidence |
| Channels | urgent: call; quick: chat; record: email; decision: meeting |
| NDA | signed promise not to disclose confidential information |
| Information levels | public, internal, confidential, restricted |
| Working time (Labour Act 2074, general) | 8 hours a day, 48 hours a week; overtime is paid |
| Leaked secret | remove, move to environment variable, **change it**, report |

## Chapter summary

- The first week is a checklist; confirm in week one that real tasks match your objectives.
- Good communication means the **right channel**, a complete message and a record of decisions.
- Use the **15-minute rule** to balance independence with asking for help.
- Information has four levels; restricted data (passwords, IDs) never lives in code or chat.
- A leaked secret must be **changed**, not just deleted, and reported immediately.
- You have rights to a clear agreement, respect and safety; use your coordinator if they are not met.

## Practice

1. List four things to do on the first day of an internship.
2. State the 15-minute rule and one reason for each half.
3. Choose the right channel for: (a) the server is down, (b) the file name of a template, (c) a client's approval of a design.
4. What is an NDA? Name two kinds of information it usually covers.
5. Name the four information levels and give one example of each.
6. Why does deleting a password from the latest commit not make the repository safe?
7. State the normal working day and week under the Labour Act 2074 as a general pointer.
8. What should you do if you witness harassment?
9. List three digital hygiene habits.
10. Why should you ask a question with the evidence of what you tried?

::: note Answers and worked solutions
**1.** Meet the supervisor and sign attendance; get logins and tool access; read the rules on hours, leave and internet use; write the first log entry or agree the weekly meeting.
**2.** Try alone for 15 minutes with notes, then ask. Trying first builds skill and respects the mentor's time; asking at 15 minutes avoids wasting your own.
**3.** (a) Call or visit (urgent, blocks others). (b) Chat (quick). (c) Email (needs a record).
**4.** A Non-Disclosure Agreement is a signed promise not to share confidential information. It covers client data, source code, prices, passwords and internal plans.
**5.** Public (published web text), internal (meeting notes), confidential (client data), restricted (passwords, citizenship numbers).
**6.** Git keeps history; the old commit still contains the password. It must be changed, and the history cleaned if needed.
**7.** Eight hours a day and 48 hours a week, with overtime paid (check the current text).
**8.** Note the date and words, report it to the coordinator or a trusted senior, and do not stay silent.
**9.** Lock the screen, use unique passwords with two-step verification, avoid unknown USB drives and public Wi-Fi for client work.
**10.** It shows effort, saves time, and lets the mentor see where your understanding breaks.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is confidentiality in an internship? Explain the four information levels and the right action when a secret is leaked.**

*Introduction.* Confidentiality is the duty not to disclose information that an organisation or its clients have entrusted to you. Interns see sensitive data from day one, so the duty is real even if the placement is short. An NDA records it in writing.

*The four levels (Figure 2.1).*

1. **Public** information may be seen by anyone, such as published web text.
2. **Internal** information is for staff and interns, such as meeting notes and tickets.
3. **Confidential** information is for the named team only, such as client data and source code.
4. **Restricted** information is for the owner or administrator, such as passwords, keys and citizenship numbers.

*Handling a leak.* If a secret is committed or sent by mistake: remove it from the code and read it from an environment variable, **change the password or key**, because history and copies may remain, and tell your supervisor the same day. A scanner like the one in Section 2.3 can catch such lines before commit. *Conclusion.* Confidentiality protects clients, the firm and the intern's own reputation.

**Q2 (5 marks). Explain professional communication at the workplace: choice of channel, meetings and the 15-minute rule.**

*Introduction.* Good communication saves the firm's time and shows the intern's maturity. It has three parts.

*Choosing the channel.* Urgent matters need a call or a visit; quick questions need chat; anything needing a record goes by email; meetings are for decisions by several people (Plate 2.1c).

*Complete messages.* A useful message gives the problem, the evidence (error line or screenshot), what was tried and what is wanted: "Login returns 500 after submit; log attached; cache cleared; can you spare five minutes after lunch?".

*Meetings.* Write the decision and the action beside your name; speak with something specific.

*15-minute rule.* Try alone for 15 minutes with notes, search, then ask with evidence (Figure 2.2), and log the answer. *Conclusion.* The right channel and a complete message turn an intern's questions from interruptions into signs of good thinking.

**Q3 (10 marks). Describe the professional conduct expected from an intern during a BCA internship.**

*Introduction.* An internship is a trial of character as much as skill. A supervisor can teach a tool in a week but cannot teach reliability. Conduct can be grouped under time, communication, information, safety and growth.

*Expected conduct.*

1. **Punctuality.** Arrive at the start time, inform in advance of absence, and respect the agreed eight-hour day.
2. **First-week discipline.** Collect logins, read rules, shadow, write the first log and confirm objectives with the supervisor.
3. **Clear communication.** Choose the right channel; send complete messages; record decisions in email.
4. **Independence with humility.** Follow the 15-minute rule; say "I do not know yet" rather than bluff.
5. **Confidentiality.** Protect data at four levels, never commit secrets, and report mistakes immediately.
6. **Respect and safety.** Treat all staff with courtesy, refuse and report harassment, and use safe posture and digital hygiene.
7. **Feedback and ownership.** Accept review comments, fix them the same day and finish what is started.
8. **Rights awareness.** Keep a written agreement, ask the coordinator when hours or tasks drift.

| Area | Good conduct | Poor conduct |
|---|---|---|
| Time | informs before lateness | silent absence |
| Questions | evidence and 15-minute rule | "it is not working" |
| Data | masked, protected, reported | secrets in code or chat |
| Feedback | thanks, fix, reply "done" | argues or ignores |
| People | courteous to everyone | rude, jokes about others |

*Example.* Anisha finds a database password in a config file she was asked to commit, replaces it with an environment variable, tells her supervisor, and the password is changed within the hour; the firm trusts her with a client repository in week three. *Conclusion.* Professional conduct is a set of small, consistent habits. Together they decide whether an intern is remembered, recommended and hired.
