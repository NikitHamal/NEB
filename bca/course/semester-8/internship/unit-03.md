---
subject: Internship
grade: BCA Semester 8
unit: 3
title: Working the Weeks: Learning Plan, Daily Log and Weekly Review
area: BCA 452 · Internship · Unit 3
---

By day three Anisha has a laptop, a login and a task. By day ten she has forgotten what she did on day four. Eight weeks is long enough to learn a great deal and short enough to waste. The difference lies in three small habits: **plan the weeks, record each day, review each week**. They cost about fifteen minutes a day and they produce, almost for free, the evidence that the report in Unit 5 needs.

::: key What this unit gives you
- An **eight-week learning plan** that moves from observing to contributing to presenting.
- The anatomy of a good **daily log entry** and why vague entries ("worked on website") fail.
- The **weekly review** with Keep, Stop, Try and the supervisor's signature.
- An executed analysis of a simulated 40-day log: hours per week, time per activity, and a check against objective L3.
- Photographs of boards and pair work, and eight rules for logs that pass a supervisor's eye.
:::

## 3.1 Plan the eight weeks

Without a plan, interns drift toward whatever is urgent for others. A plan does not need to be rigid; it needs to **name the shape** of the placement. Three phases work for most firms.

| Weeks | Phase | What you do | Evidence |
|---|---|---|---|
| 1 to 2 | **Observe and set up** | tools, code base tour, shadowing, small fixes | setup notes, first log pages |
| 3 to 6 | **Contribute** | tickets of rising difficulty, code review, tests (Unit 4) | merged changes, review comments |
| 7 | **Own and demonstrate** | a small deliverable end to end, client or team demo | demo, user feedback |
| 8 | **Hand over and reflect** | documentation, hand-over notes, report draft, viva practice | hand-over page, draft report |

Share the plan with your supervisor in week one and adjust it together. A mentor who has seen the plan can offer the right task at the right time, and a plan that is visibly **behind** in week four can be rescued in week five, not discovered in week eight.

## 3.2 The daily log

The **daily log** is a short factual record of what you did, how long it took, what you learned and what blocked you. Colleges usually require it; supervisors sign it weekly. Treat it as a professional habit, not as homework: engineers keep work journals to recall decisions, write status reports and prove effort.

A good entry has six fields and takes five minutes to write at the end of the day.

| Field | Example (day 12) |
|---|---|
| Date and hours | Sunday 4 Falgun, 7.0 h |
| Task | Fix ticket HD-31: invoice VAT rounds wrongly |
| What I did | Reproduced bug with three amounts; found `round()` applied before adding VAT; wrote 3 tests |
| Outcome | Fix pushed to branch `fix/vat-rounding`, review requested |
| What I learned | Always round money once, at the end; use `Decimal` for currency |
| Blocker / next | Waiting for review from Sanjay; next: HD-34 |

**Bad:** "Worked on website, 8 hours." That entry shows no learning, cannot be checked and could have been written without going to work. **Good:** one verb, one object, one result, one learning. Write the entry the same day; a log filled in on Friday for the whole week is fiction.

## 3.3 The weekly review

At the end of each week spend twenty minutes with the log. Count the hours, list the tasks closed and then answer three questions: **Keep** (what worked and should continue), **Stop** (what wasted time) and **Try** (one change for next week). Then compare the week with the plan and the objectives: are L1 to L3 on track? Bring the one-page review to the weekly meeting with your supervisor, who signs the log. The signature is more than a formality: it is the supervisor's testimony that the log is true, which is the heart of the placement letter later.

## 3.4 Analysing the log

A log is data. The script below builds a **simulated** 40-day log for Anisha (seed 452, eight weeks of five working days, hours rounded to half hours, one day of fever leave) and answers four questions: hours per week, hours per activity, hours spent waiting, and whether objective L3 ("at least 6 hours' work for 40 days") was met. Six activities are tracked: coding, learning, meetings, testing, documents and waiting. The base profile follows the three phases of Section 3.1, with random noise added.

```python
import numpy as np
rng = np.random.default_rng(452)
acts = ["code", "learn", "meet", "test", "docs", "wait"]
prof = [[.5, 3, 1, 0, 1, 1], [1.5, 2.5, 1, .5, .5, .5], [3, 1.5, 1, .5, .5, .5],
        [3.5, 1, 1, 1, .5, .5], [3.5, .5, 1, 1, .75, .5], [3.5, .5, .75, 1.5, .75, .5],
        [2.5, .5, 1.5, 1, 1.5, .5], [1, .5, 1, .5, 2.5, .25]]
days = []
for w in range(8):
    for d in range(5):
        h = np.round((np.array(prof[w]) + rng.normal(0, .45, 6)) * 2) / 2
        days.append(np.clip(h, 0, None))
days = np.array(days)
days[16] = 0          # day 17: fever leave, honestly logged as zero
wk = days.reshape(8, 5, 6).sum(axis=1)
print("week  hours  " + "  ".join(f"{a:>5}" for a in acts))
for i, row in enumerate(wk, 1):
    print(f"{i:>4}  {row.sum():>5.1f}  " + "  ".join(f"{v:>5.1f}" for v in row))
tot = wk.sum(axis=0)
print(f"all   {tot.sum():>5.1f}  " + "  ".join(f"{v:>5.1f}" for v in tot))
share = tot / tot.sum() * 100
print("share % " + ", ".join(f"{a} {s:.0f}" for a, s in zip(acts, share)))
daily = days.sum(axis=1)
ok = int((daily >= 6).sum())
print(f"days with >= 6 h: {ok} of 40; zero-hour days: {int((daily == 0).sum())}")
print(f"mean hours on worked days: {daily[daily > 0].mean():.2f}")
print("L3 met:", ok == 40)
```
```output
week  hours   code  learn   meet   test   docs   wait
   1   33.0    3.5   15.0    4.5    1.0    3.5    5.5
   2   35.5    9.0   12.5    5.5    2.0    4.0    2.5
   3   35.0   15.5    8.5    4.5    3.0    2.5    1.0
   4   28.0   14.0    4.5    3.0    2.0    2.0    2.5
   5   33.5   17.0    2.0    6.0    3.5    2.5    2.5
   6   41.0   17.0    2.0    6.0    8.5    4.5    3.0
   7   38.5   12.5    4.0    7.0    6.0    8.5    0.5
   8   32.0    5.5    4.0    4.5    3.5   13.0    1.5
all   276.5   94.0   52.5   41.0   29.5   40.5   19.0
share % code 34, learn 19, meet 15, test 11, docs 15, wait 7
days with >= 6 h: 33 of 40; zero-hour days: 1
mean hours on worked days: 7.09
L3 met: False
```

*Reading the output.* Anisha logged **276.5 hours** over 40 days; on the 39 days she worked, the mean was 7.09 hours. The shape of the placement is visible in the table. In week 1 the biggest block is **learning** (15.0 of 33.0 hours) and coding is only 3.5; by weeks 5 and 6 coding rises to 17.0 and learning falls to 2.0; in week 8 **documents** take 13.0 hours because the hand-over notes and report draft are being written. This is exactly the observe, contribute, hand-over curve of Section 3.1. Overall, coding is 34 percent of the time, learning 19, meetings 15, documents 15, testing 11 and waiting 7.

The last lines are the honest part. **Objective L3 was not met**: only 33 of 40 days reached six hours, one of the seven short days being the fever leave (a zero-hour day). The right response is not to edit the log. It is to record the result, explain it in the report, and show the learning: next time, write the objective as "at least 6 hours on 90 percent of working days". A log that always matches the objective is a log that was written to match.

```svgfig label="3.1" caption="Hours per week by activity, drawn from the script output (week 1 on the left). Learning (blue) shrinks as coding (green) grows, testing (amber) peaks in week 6, and documents (grey) dominate the final week. Waiting time (red) is highest in week 1, while access and set-up were pending."
f = Fig(580, 250)
data = [(3.5, 15.0, 4.5, 1.0, 3.5, 5.5), (9.0, 12.5, 5.5, 2.0, 4.0, 2.5), (15.5, 8.5, 4.5, 3.0, 2.5, 1.0), (14.0, 4.5, 3.0, 2.0, 2.0, 2.5),
        (17.0, 2.0, 6.0, 3.5, 2.5, 2.5), (17.0, 2.0, 6.0, 8.5, 4.5, 3.0), (12.5, 4.0, 7.0, 6.0, 8.5, 0.5), (5.5, 4.0, 4.5, 3.5, 13.0, 1.5)]
cols = ["#86efac", "#93c5fd", "#c7d2fe", "#fde68a", "#cbd5e1", "#fca5a5"]
names = ["code", "learn", "meet", "test", "docs", "wait"]
f.line(50, 200, 440, 200, color=SLATE); f.line(50, 30, 50, 200, color=SLATE)
for v in (0, 10, 20, 30, 40):
    y = 200 - v * 4
    f.line(46, y, 50, y, color=SLATE); f.text(42, y, str(v), size=9, color=SLATE, anchor="end", vmid=True)
for i, row in enumerate(data):
    x = 62 + i * 47
    y = 200
    for v, c in zip(row, cols):
        h = v * 4
        f.box(x, y - h, 34, h, "", fill=c, stroke=SLATE)
        y -= h
    f.text(x + 17, 216, f"W{i+1}", size=10, color=NAVY, bold=True)
    f.text(x + 17, y - 7, f"{sum(row):g}", size=9.5, color=NAVY, bold=True)
for i, (n, c) in enumerate(zip(names, cols)):
    f.box(470, 40 + i * 24, 14, 14, "", fill=c, stroke=SLATE)
    f.text(492, 47 + i * 24, n, size=10.5, color=NAVY, anchor="start", vmid=True)
f.text(245, 238, "hours per week", size=10, color=SLATE, italic=True)
```

```svgfig label="3.2" caption="The eight-week plan as a chart. Phases overlap: contribution starts while set-up is finishing, and documentation grows from week 5 so that week 8 is not a panic. The two demos (weeks 4 and 7) match objective L2."
f = Fig(580, 215)
f.line(130, 36, 570, 36, color=SLATE)
for w in range(8):
    f.text(130 + w * 55 + 27, 24, f"W{w+1}", size=10, color=NAVY, bold=True)
bars = [("Set-up, shadowing", 0, 2, BLUE, NAVY), ("Small fixes (tickets)", 1, 4, SOFT, TEAL), ("Feature work", 3, 7, "#bbf7d0", TEAL),
        ("Testing and review", 2, 7, "#fde68a", AMBER), ("Documentation", 4, 8, "#e2e8f0", SLATE), ("Report and viva prep", 6, 8, "#fecaca", RED)]
for i, (n, a, b, fl, st) in enumerate(bars):
    y = 48 + i * 25
    f.text(124, y + 10, n, size=10, color=NAVY, anchor="end", vmid=True)
    f.box(130 + a * 55, y, (b - a) * 55, 20, "", fill=fl, stroke=st)
for w, lab in ((3, "demo 1"), (6, "demo 2")):
    x = 130 + w * 55 + 27
    f.line(x, 42, x, 200, color=RED, dash=True)
    f.text(x, 208, lab, size=10, color=RED, bold=True)
```

```photogrid label="3.1" cols="3" ratio="1.0" caption="Tools for working the weeks. (a) A three-column task board: a ticket moves from To do to Doing to Done, which is the same story as the daily log. (b) Pair work at one screen: one person drives, the other reviews aloud; interns learn fastest this way. (c) One daily-log entry drawn as a card with the six fields of Section 3.2."
@ photo id="bca256/kanban" cap="Task board"
fit 1.0
focus 0.5 0.5
call 0.5 0.85 0.5 0.65 "To do, Doing, Done"
@ photo id="bca256/pair" cap="Pair working"
fit 1.0
focus 0.5 0.5
call 0.5 0.85 0.5 0.65 "driver and reviewer"
@ svg cap="A log entry"
f = Fig(300, 300)
f.box(8, 8, 284, 284, "", fill="#ffffff", stroke=NAVY)
fl = [("When", "Sun 4 Falgun, 7 h"), ("Task", "HD-31 VAT rounding"), ("Did", "reproduced, 3 tests"), ("Outcome", "fix pushed, review asked"), ("Learned", "round money once"), ("Next", "HD-34 after review")]
for i, (a, b) in enumerate(fl):
    y = 18 + i * 45
    f.box(16, y, 82, 38, a, fill=BLUE, stroke=NAVY, size=12.5, color=NAVY, bold=True)
    f.box(102, y, 182, 38, b, fill=SOFT, stroke=TEAL, size=12.5, color=NAVY)
```

## 3.5 Eight rules for a log that passes a supervisor's eye

1. **Write the same day.** Memory fades in hours, and a log written on Friday for the whole week is fiction. Set a calendar reminder for the last fifteen minutes of the day. Five honest minutes beat an hour of reconstruction.
2. **Use a verb, an object and a result.** "Fixed VAT rounding in invoice total; 3 tests added" says what happened. "Worked on website" says nothing. A specific entry also helps you answer viva questions weeks later.
3. **Record time truthfully.** Count the hours you actually worked, including waiting and learning, and mark leave as leave. Supervisors sign many logs and they notice a perfect eight hours every day. Honest numbers like Anisha's 33 of 40 days are believable.
4. **Capture one learning per day.** Write the sentence "I learned that..." even on slow days. Over eight weeks these form your skills section and your reflection chapter. Learning that is not written is quickly forgotten.
5. **Name blockers and who can unblock them.** "Waiting for staging access from Sanjay" tells the supervisor what to fix. Blockers repeated three days in a row are a signal to raise the issue, politely, in the weekly meeting.
6. **Link entries to evidence.** Add the ticket number, commit hash or a screenshot name. Evidence turns a claim into a proof, and the report can cite it. Never include secrets or client data in the log.
7. **Review weekly with Keep, Stop, Try.** Spend twenty minutes counting hours and comparing the week with the plan. One change per week is enough. The weekly meeting then becomes a conversation about progress, not a surprise.
8. **Get it signed and keep a copy.** The supervisor's weekly signature proves the log is true. Photograph or scan each signed page, and back up the digital log. A lost log in week eight cannot be rebuilt.

## Formula and fact sheet

| Item | Rule or fact |
|---|---|
| Plan phases | observe (W1-2), contribute (W3-6), own and demo (W7), hand over (W8) |
| Log entry fields | date and hours, task, what I did, outcome, learned, blocker or next |
| Weekly review | Keep, Stop, Try, compared with plan and objectives |
| Share of time | activity hours ÷ total hours × 100 |
| Mean hours | total hours ÷ days actually worked |
| Honest log | misses stay visible; objectives are rewritten, logs are not |

## Chapter summary

- Plan the placement as **observe, contribute, own, hand over** and share the plan with your supervisor.
- A daily log has six fields; the entry must be specific, same-day and truthful.
- The weekly review (Keep, Stop, Try) keeps the placement on track and produces the supervisor's signature.
- Log data can be analysed: in the example, coding 34 percent, learning 19, and one honest miss against L3.
- Never adjust the log to fit the objective; adjust the objective next time and explain the gap.

## Practice

1. Name the four phases of the eight-week plan and one output of each.
2. List the six fields of a daily log entry.
3. Rewrite "worked on login" as a good entry.
4. From Section 3.4, what percentage of Anisha's hours were documents? (40.5 of 276.5)
5. Verify the mean of 7.09 hours on worked days.
6. Why should a zero-hour day be logged as zero?
7. What do Keep, Stop and Try mean?
8. Give two reasons the supervisor's weekly signature matters.
9. Why did learning hours fall and coding hours rise between weeks 1 and 6?
10. L3 failed in the example. Write a better version of the objective.

::: note Answers and worked solutions
**1.** Observe and set up (setup notes), contribute (merged tickets), own and demonstrate (demo), hand over and reflect (hand-over page, report draft).
**2.** Date and hours; task; what I did; outcome; what I learned; blocker or next step.
**3.** "Implemented login form validation for email and password; 4 tests added; ticket HD-22 in review; learned to hash passwords with bcrypt."
**4.** 40.5 ÷ 276.5 = 0.1465, about **15 percent**.
**5.** Total 276.5 hours over 39 worked days: 276.5 ÷ 39 = 7.09.
**6.** It is the truth, and hiding leave makes the whole log doubtful; the supervisor may know about the leave.
**7.** Keep: what worked; Stop: what wasted time; Try: one change for next week.
**8.** It is the supervisor's testimony that the log is true, and the college relies on it for marks; it also forces a weekly conversation.
**9.** The plan moves from learning the tools in weeks 1 and 2 to producing code in weeks 3 to 6, so learning falls from 15.0 to 2.0 hours and coding rises from 3.5 to 17.0.
**10.** "Log at least 6 hours of work on 90 percent of working days, with leave days marked."
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is a daily log in an internship? Describe its fields with an example and explain why it matters.**

*Introduction.* A daily log is a short, factual, same-day record of work done during the placement. Colleges require it and supervisors sign it weekly; it is the main evidence of what the intern actually did.

*Fields.*

1. **Date and hours** show when and how long, including leave days as zero.
2. **Task** names the ticket or job.
3. **What I did** states the actions in specific terms.
4. **Outcome** records what was delivered or still pending.
5. **What I learned** captures one skill or lesson.
6. **Blocker or next step** shows what is stopping progress and what comes next.

*Example.* "Sun 4 Falgun, 7.0 h. HD-31 VAT rounding. Reproduced with three amounts, found rounding before VAT, wrote 3 tests. Fix pushed, review requested. Learned: round money once, at the end. Next: HD-34."

*Importance.* It proves effort, supports the weekly review, helps in the viva and feeds the report. *Conclusion.* A specific, honest log is the cheapest evidence an intern can produce.

**Q2 (5 marks). Explain the weekly review and how it keeps an internship on track.**

*Introduction.* The weekly review is a twenty-minute reflection at the end of each week, comparing the log with the plan and with the learning objectives.

*Steps.*

1. Count the week's hours and list closed tasks.
2. Write **Keep** (what worked), **Stop** (what wasted time) and **Try** (one change).
3. Check the plan: is the contribution phase on schedule?
4. Check objectives L1 to L3: any at risk?
5. Present the one-page review to the supervisor in the weekly meeting and obtain the signature.

*Benefit.* A delay is noticed in week four rather than week eight; the supervisor can adjust tasks; and the signed pages become proof. *Example.* In week 4 Anisha's hours drop to 28.0; the review shows two days lost waiting for access, so she asks for access to be fixed, and week 5 recovers to 33.5. *Conclusion.* A short weekly habit turns a drifting placement into a managed one.

**Q3 (10 marks). Explain how an intern should plan, record and review work during an eight-week internship, using the log analysis as an example.**

*Introduction.* An eight-week placement passes quickly. Planning, recording and reviewing keep it purposeful and create the evidence for the report. Figures 3.1 and 3.2 show both the plan and the result for the running example.

*Plan.*

1. **Three phases.** Observe and set up (weeks 1 and 2), contribute (3 to 6), own and demonstrate (7), hand over (8).
2. **Share the plan.** Agree it with the supervisor in week one and adjust it together.
3. **Add demos and deadlines.** Two demos (weeks 4 and 7) turn objective L2 into dates.

*Record.*

4. **Daily log with six fields.** Specific, same-day, truthful, with one learning per day.
5. **Evidence links.** Ticket numbers, commits and screenshots, never secrets.

*Review.*

6. **Weekly Keep, Stop, Try** compared with plan and objectives, signed by the supervisor.
7. **Analyse the log as data.** In the example, 276.5 hours: coding 34 percent, learning 19, meetings 15, documents 15, testing 11, waiting 7; mean 7.09 hours on 39 worked days.
8. **Report honestly.** L3 was missed (33 of 40 days at six hours or more), so the report says so and rewrites the objective.

| Week | Hours | Main activity | Review note |
|---|---|---|---|
| 1 | 33.0 | learning (15.0) | waiting 5.5 h for access, raise it |
| 4 | 28.0 | coding (14.0) | two days lost, ask for staging |
| 6 | 41.0 | coding and testing | too long, protect rest |
| 8 | 32.0 | documents (13.0) | hand-over notes complete |

*Example.* The curve from learning to coding to documents in Figure 3.1 is the plan of Figure 3.2 made real. *Conclusion.* Plan, record and review form a loop; interns who run it finish with evidence, confidence and an honest report.
