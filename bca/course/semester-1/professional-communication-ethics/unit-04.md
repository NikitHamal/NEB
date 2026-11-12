---
subject: Professional Communication and Ethics
grade: BCA Semester 1
unit: 4
title: Workplace Communication, Teamwork and Etiquette
area: BCA 105 · Professional Communication and Ethics · Unit 4
---

Software is built by teams. This unit covers how teams form and work, how to handle disagreement, how to give and take feedback, how to manage time, and the etiquette that makes someone good to work with. It also treats customer communication, which is where many IT careers begin.

::: key What this unit gives you
- Team stages and roles; effective teamwork in software projects.
- Conflict resolution, negotiation, giving and receiving feedback.
- Time management and a way to prioritise work.
- Customer communication, workplace etiquette and remote-work habits.
:::

## 4.1 Teams and teamwork

A **team** is a small group with a shared goal, complementary skills and mutual accountability. **Tuckman's stages**: *forming* (polite, unsure), *storming* (conflict over roles and methods), *norming* (rules and trust develop), *performing* (productive), *adjourning* (project ends).

**Belbin-style roles** (a simplified list): leader/coordinator, idea generator, implementer, completer-finisher, evaluator, team worker, specialist. A balanced team needs all of them, though one person plays several.

**Software team roles:** product owner, project manager or scrum master, developers (front end, back end), UI/UX designer, tester (QA), DevOps/administrator, business analyst.

**Practices that make teams work**

1. Agree the **goal and definition of done** in writing.
2. Divide work by clear ownership; track tasks on a board (Trello, Jira, GitHub Projects).
3. Short **stand-up** each day or week: *What did I do? What will I do? What blocks me?*
4. Use version control; review each other's code; keep a shared decision log.
5. Communicate problems early: a delay reported on day 2 can be fixed; one reported on day 14 cannot.
6. Credit others publicly; share the blame, never single anyone out.

**Social loafing**: the tendency of some members to reduce effort in groups. Fix it with visible individual tasks, peer review and small subgroups.

```photogrid label="4.1" cols="2" ratio="1.5" caption="Teams. (a) A work crew holds a short stand-up briefing before starting: everyone hears the plan, the risks and who does what. Software teams hold the same daily stand-up. (b) Tuckman's four stages of team development: performance dips during storming and then rises as the team agrees on rules."
@ photo id="bca105/scrum" cap="A team briefing before work starts"
fit 1.5
focus 0.5 0.55
call 0.5 0.92 0.35 0.62 "Everyone hears the plan"
@ svg cap="Tuckman's stages: team performance over time"
import math
f = Fig(420, 280)
a = Axes(f, 30, 20, 370, 190, (0, 4), (0, 1.1)); a.axes("time", "performance")
a.curve(lambda t: 0.35 + 0.3 * t / 1 if t < 1 else (0.65 - 0.25 * math.sin((t - 1) * math.pi) if t < 2 else 0.65 + 0.3 * (1 - math.exp(-(t - 2) * 1.6))), 0, 4, color=NAVY, sw=2.8, n=300)
for i, (n, c) in enumerate([("Forming", AMBER), ("Storming", RED), ("Norming", TEAL), ("Performing", NAVY)]):
    f.text(a.X(i + 0.5), 232, n, size=10.5, color=c, bold=True)
    if i: a.vline(i, 0, 1.1, color="#94a3b8")
f.text(210, 254, "polite  -  conflict  -  rules and trust  -  results", size=9.5, color=SLATE)
```

```svgfig label="4.1" caption="The Eisenhower matrix for time management. Sort every task by urgency and importance: do it now, schedule it, delegate it or delete it. Most students waste time in the lower-left box and neglect the upper-right box (studying early, practising skills), which prevents emergencies later."
f = Fig(700, 280)
f.box(110, 10, 280, 120, "", fill=ROSE, stroke=RED); f.box(400, 10, 280, 120, "", fill=MINT, stroke=TEAL)
f.box(110, 140, 280, 120, "", fill=SAND, stroke=AMBER); f.box(400, 140, 280, 120, "", fill=SOFT, stroke=SLATE)
for x, y, h, t, c in [(250, 34, "1 DO NOW", "urgent + important", RED), (540, 34, "2 SCHEDULE", "important, not urgent", TEAL), (250, 164, "3 DELEGATE / BATCH", "urgent, not important", AMBER), (540, 164, "4 DELETE / LIMIT", "neither", SLATE)]: f.text(x, y, h, size=13, color=c, bold=True); f.text(x, y + 18, t, size=10, color=SLATE, italic=True)
for x, y, s in [(250, 80, "assignment due tomorrow"), (250, 98, "server down in the lab"), (540, 80, "study plan, exercise, learning C"), (540, 98, "update CV, practise projects"), (250, 210, "most phone calls, some emails"), (250, 228, "a friend's quick request"), (540, 210, "endless scrolling, idle chat"), (540, 228, "unneeded notifications")]: f.text(x, y, s, size=10.5, color=NAVY)
f.text(100, 75, "URGENT", size=10, color=SLATE, bold=True, anchor="end"); f.text(100, 205, "NOT URGENT", size=10, color=SLATE, bold=True, anchor="end"); f.text(250, 275, "IMPORTANT", size=10, color=SLATE, bold=True); f.text(540, 275, "NOT IMPORTANT", size=10, color=SLATE, bold=True)
```

## 4.2 Conflict and negotiation

Conflict is normal; badly handled conflict is the problem. Common sources: unclear roles, unequal workload, different priorities, personality clashes, scarce resources.

| Style | Approach | Use when |
|---|---|---|
| Competing | win at the other's cost | an emergency needs a quick decision |
| Collaborating | find a solution that satisfies both | the issue is important and time exists |
| Compromising | each gives up something | a quick middle-way will do |
| Avoiding | postpone or ignore | the issue is trivial or emotions need to cool |
| Accommodating | give way | the issue matters more to the other side |

**A simple method:** (1) cool down, (2) listen to the other side's view first, (3) separate the **person** from the **problem**, (4) agree on the facts, (5) focus on **interests** (what each side needs) rather than **positions** (what they demand), (6) list options, (7) agree on a fair criterion and a written action.

**Negotiation** is the same, with offers. Know your **BATNA** (best alternative to a negotiated agreement); aim for a win–win outcome. Example: a client wants three extra features at the same price; instead of refusing, offer a phased plan: the most valuable feature now within budget, the others in phase 2 with a separate quotation.

## 4.3 Feedback

**Giving feedback (SBI model):** describe the **Situation** (when and where), the **Behaviour** (observable, not personality), and the **Impact** (effect on the team or project); then suggest what to do next.

*Poor:* "You are careless." *Better:* "In yesterday's code review (S), three functions had no error checks (B); that caused the demo crash and cost us an hour (I). Could we add a checklist before merging?"

Praise specifically ("The way you documented the API saved the tester two days") as well as correcting. Give feedback promptly and privately for criticism, publicly for praise.

**Receiving feedback:** listen without interrupting, thank the giver, ask for examples, do not argue or justify at once, decide what to act on, and follow up.

## 4.4 Time management

**Eisenhower matrix**

| | Urgent | Not urgent |
|---|---|---|
| **Important** | **Do now** (a crash in the live system, tomorrow's submission) | **Schedule** (learning, planning, exercise, refactoring) |
| **Not important** | **Delegate or minimise** (some emails, interruptions) | **Drop** (endless scrolling) |

**Techniques:** to-do list with three priorities a day; **time-boxing** (assign a fixed block to a task); **Pomodoro** (25 minutes work, 5 minutes break; longer break after four); batching email checks; saying a polite "no"; estimating honestly and adding buffer.

**Parkinson's law:** work expands to fill the time available, so set shorter deadlines for yourself. **Procrastination** fades when you start with a five-minute version of the task.

::: example Worked example: planning a project week
A student has a database assignment due Friday (4 hours of work), a Java lab report due Thursday (3 h), exam revision (6 h across the week), and a friend's birthday on Wednesday. Plan: Monday: lab report draft (2 h) + revision (1 h); Tuesday: lab report finish (1 h), assignment tables (2 h); Wednesday: revision (2 h), birthday in the evening; Thursday: submit report, revision (2 h); Friday morning: assignment queries and test (2 h), submit. Total 13 hours, all deadlines met with a margin of one day for the assignment's first half.
:::

## 4.5 Customer communication and support

- **Listen first**: let the customer finish; note the problem in their words; paraphrase it back.
- **Empathise without blaming**: "I understand this is frustrating; let's fix it."
- **Use their language, not yours**: no jargon; say what you will do and by when.
- **Own the problem**: "I will find out and call you by 3 pm."
- **Close the loop**: confirm the fix works and record it (ticket).
- Never promise what you cannot deliver; if you do not know, say so.

**Handling an angry customer (LAST):** **L**isten, **A**pologise for the experience, **S**olve, **T**hank. Keep your voice calm and slow; do not take it personally.

**Writing a support reply:** thank the customer; restate the problem; give the solution in numbered steps; offer further help; sign with a name.

## 4.6 Workplace etiquette and remote work

- **Punctuality** (arrive and join meetings on time), **dress** suited to the organisation, **respect** for everyone regardless of role, gender, caste, ethnicity, religion or disability.
- **Phone discipline:** silent in meetings; personal calls away from colleagues.
- **Shared spaces:** clean up after yourself, keep voices down in open offices, label food in the fridge.
- **Confidentiality:** do not discuss client data or salaries outside the people who need to know; log out and lock the screen when away.
- **Dining and social events:** moderate behaviour; do not gossip; no discussion of religion or politics unless the setting is suitable.
- **Social media:** your posts reflect on the employer; never share confidential work or criticise colleagues publicly.
- **Remote work:** define working hours; update status; write short daily progress notes; prefer written decisions; turn on cameras when asked; keep a quiet place and test your internet link; respect other time zones when scheduling.

**Workplace harassment.** Unwelcome sexual, discriminatory or abusive conduct is never acceptable. Nepal's Sexual Harassment at Workplace Prevention Act, 2071 (2014) requires organisations to have a complaint mechanism. Report to the designated committee or HR, and keep a record.

## 4.7 Eight characteristics of an effective team

1. **A shared, clear goal.** Every member can state in one sentence what the team is building and why. The goal is written down together with the "definition of done". Without it, five talented students pull in five directions.
2. **Clear roles and ownership.** Each task has one owner, such as front end, back end, testing or documentation. People know who decides what, so work is not duplicated or forgotten. A Trello board in the lab makes ownership visible.
3. **Open and honest communication.** Members report progress and problems early, in plain words. A delay told on day 2 can be solved, but one told on day 14 cannot. Honesty needs a team where nobody is punished for bad news.
4. **Mutual trust and respect.** Members believe that others will do their work and listen to different opinions. Respect for age, gender, language and ethnic differences, which are many in Nepali classes, strengthens this trust. Trust is built through small kept promises.
5. **Constructive handling of conflict.** Disagreement about design or deadlines is healthy when it is about the problem, not the person. The team states the issue, listens to every view and agrees on a test or a vote. Hidden conflict does far more damage than open discussion.
6. **Shared responsibility and accountability.** Success is shared, and so is the blame. Everyone accepts that they are accountable for their part. Peer review and visible tasks reduce social loafing.
7. **Regular meetings and feedback.** A short daily or weekly stand-up asks: what did I do, what will I do, what blocks me? Feedback is specific, timely and kind. The team reviews its own method after each milestone.
8. **Skills that complement each other.** A good team mixes a leader, an idea generator, a careful finisher and a specialist. Members learn from each other and cover each other's weak points. Diversity of skills makes the final product stronger than any single member could.

```photogrid label="4.2" cols="2" ratio="1.0" caption="Why big teams need structure. (a) A rowing eight: nine people (eight rowers and a cox) must keep one rhythm, which works because the roles are fixed and the cox speaks for the crew. (b) In a team of n people there are n(n - 1) / 2 possible pairs who may need to talk. Three people have 3 channels; five have 10; the nine-person boat has 36; twelve have 66; twenty have 190. Doubling the team from 9 to 18 would raise the channels from 36 to 153, more than four times. This is why a project with 20 programmers is split into squads of five or six with a lead each, and why Brooks's law warns that adding people to a late project can make it later. Clear roles, a short stand-up and a shared task board keep the number of conversations manageable."
@ photo id="bcapc/rowing" cap="A rowing eight with its cox"
fit 1.0
focus 0.5 0.5
@ svg cap="Communication channels n(n-1)/2"
ns = [3, 5, 9, 12, 20]
ch = [n * (n - 1) // 2 for n in ns]
assert ch == [3, 10, 36, 66, 190] and 18 * 17 // 2 == 153 and round(153 / 36, 2) == 4.25
f = Fig(300, 240)
f.text(150, 14, "possible pairs in a team of n", size=10.5, color=NAVY, bold=True)
base, sc = 176, 130 / 190
for i, (n, c) in enumerate(zip(ns, ch)):
    x = 18 + i * 54; h = c * sc
    f.box(x, base - h, 40, max(h, 2), "", fill="#1d6fb8" if n != 9 else "#d97706", stroke=NAVY, r=0, sw=1)
    f.text(x + 20, base - h - 8, str(c), size=10.5, color=NAVY, bold=True)
    f.text(x + 20, base + 14, f"n = {n}", size=10.5, color=SLATE)
f.line(10, base, 292, base, color=SLATE, sw=1.2)
f.text(150, 210, "nine in the boat: 36 pairs (amber)", size=10.5, color="#b45309", bold=True)
f.text(150, 228, "9 -> 18 people: 36 -> 153 channels (4.25x)", size=10.5, color=RED, bold=True)
```

## Formula and fact sheet

- Tuckman: forming → storming → norming → performing → adjourning.
- Conflict styles: competing, collaborating, compromising, avoiding, accommodating.
- SBI feedback: Situation, Behaviour, Impact.
- Eisenhower: do (urgent + important), schedule, delegate, drop.
- LAST: Listen, Apologise, Solve, Thank.
- Stand-up: yesterday, today, blockers.

## Chapter summary

- Teams pass through predictable stages; clear goals, owners, rituals and early reporting make them productive.
- Conflicts are managed by listening, focusing on interests and agreeing on written actions.
- Feedback is most useful when specific, timely and about behaviour, not personality.
- Time management is the art of choosing what matters and protecting time for it.
- Courtesy, confidentiality and punctuality define professional reputation, in office and online.

## Practice

1. Explain Tuckman's stages with a software-project example.
2. List five practices of an effective software team.
3. Two team members each want a different database. Describe how you would resolve it.
4. Give SBI feedback to a teammate who regularly misses stand-ups.
5. A customer phones angry that the payroll report is wrong. Write what you would say using LAST.
6. Place these in the Eisenhower matrix: a server outage, a LinkedIn course, a colleague's casual chat, a bug report due tomorrow.
7. Write a stand-up update for a developer who finished the login page, is starting the profile page, and is blocked on an API key.
8. List ten rules of workplace etiquette.
9. What is social loafing and how do you reduce it?
10. What is a BATNA? Give an example from a freelance contract.

::: note Answers and worked solutions
**1.** Forming: students agree on a project; storming: argument over language and roles; norming: they set a Git workflow and meeting times; performing: features ship; adjourning: final demo and retrospective.
**2.** Clear goal and done criteria, task board, daily stand-ups, version control and code review, early problem reporting, shared credit.
**3.** Listen to each reason; list criteria (data size, team skill, hosting cost, support); evaluate against them or run a small test; decide jointly; record the decision.
**4.** "In the last three stand-ups (S) you were not present or sent no update (B), so I did not know whether the API task was done and the tester waited (I). Could you send a two-line update by 10 am if you cannot join?"
**5.** Listen without interrupting; "I am sorry the report was wrong, I understand it affects salary day. Please send me the figures that look wrong. I will check and call you by 3 pm. Thank you for telling us."
**6.** Outage: do now. Bug report due tomorrow: do now. LinkedIn course: schedule. Casual chat: minimise or drop (be polite).
**7.** "Yesterday I finished the login page. Today I am starting the profile page. I am blocked on the payment API key and need it from the client."
**8.** Be punctual, respect others, dress suitably, silence the phone in meetings, keep confidence, tidy shared space, write courteous email, don't gossip, give credit, report harassment.
**9.** Reduced effort by individuals in a group. Reduce it through visible personal tasks, peer review and small subgroups.
**10.** The best option if negotiation fails, for example another client offering Rs 40,000 for similar work, which you accept if the first client will not go above Rs 35,000.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Explain Tuckman's stages of team development with a software-project example.**

Bruce Tuckman described how a new group becomes an effective team in four stages (a fifth, *adjourning*, was added later). Performance does not rise in a straight line: it dips when the team argues about how to work (Plate 4.1b).

1. **Forming.** Members meet, are polite and unsure of their roles. They depend on the leader. *Example:* four BCA students are told to build a library system and agree on a group name.
2. **Storming.** Opinions clash about roles, tools and deadlines. Some members dominate or withdraw, and tension is high. *Example:* two members want PHP and two want Java; one person has done no work.
3. **Norming.** The team agrees on rules, roles and methods, trust grows and members give feedback. *Example:* they choose Java, split modules, set a weekly stand-up and use Git.
4. **Performing.** The team works smoothly towards the goal, solves problems itself and delivers quality. *Example:* modules are integrated, tested and demonstrated on time.
5. **Adjourning.** The project ends; the team reviews and celebrates.

**Role of the leader:** direct in forming, mediate in storming, coach in norming and delegate in performing. **Conclusion:** storming is normal, and a team that handles it openly reaches the performing stage sooner.

**Q (10 marks). Describe how a student team should work together: team roles, conflict handling, feedback using the SBI model, and time management with the Eisenhower matrix.**

**Introduction.** A team is a small group with a shared goal, complementary skills and mutual accountability. Software is almost always made by teams, so teamwork is a professional skill, not an extra.

**1. Roles and practices.** Typical software roles are product owner, project manager or scrum master, developers, UI/UX designer, tester and business analyst. Good practice: agree the goal and definition of done in writing, give each task one owner on a board, hold a short stand-up (*What did I do? What will I do? What blocks me?*), use version control with code review, and report problems early.

**2. Conflict handling.** Conflict is normal, especially in the storming stage. Five common styles are *competing* (win-lose), *collaborating* (win-win), *compromising* (split the difference), *avoiding* and *accommodating*. For important issues the best style is collaboration: separate the person from the problem, listen to each view, state shared interests, list options and agree on a test or a fair rule. Escalate to a supervisor only after the team has tried.

**3. Feedback (SBI model).** Describe the **Situation** (when and where), the **Behaviour** (what was seen, not personality) and the **Impact** (its effect). *Example:* "In Tuesday's stand-up (S), you did not report that the login module was late (B), so the testers waited two days (I). Could you tell us earlier next time?" Feedback should be specific, timely, private for criticism and ends with a request.

**4. Time management (Figure 4.1).**

| Box | Task type | Action |
|---|---|---|
| 1 | urgent + important | do now |
| 2 | important, not urgent | schedule (study, practice) |
| 3 | urgent, not important | delegate or batch |
| 4 | neither | delete or limit |

Other tools: a weekly plan, deadlines with buffer time, one task at a time and removing distractions such as notifications.

**5. Effective team characteristics.** Shared goal, clear roles, honest communication, trust, healthy conflict, shared accountability, regular feedback and complementary skills.

**Conclusion.** A team that agrees its goal and roles, handles conflict openly, gives SBI feedback and manages its time with priorities will deliver better software than the same people working alone.
