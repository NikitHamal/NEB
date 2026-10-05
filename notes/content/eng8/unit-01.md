---
subject: Compulsory English
grade: 8
unit: 1
title: 'Unit 1: Information and Schedules'
hours: 10
area: Units
---

Good communication begins with a simple habit: find the exact information you need, check it, and share it politely. This unit uses an educational tour timetable and a request letter to practise that habit. You will learn to read a schedule, ask for missing details, use *can*, *could* and *would* appropriately, and complete a form accurately.

::: key What success looks like
At the end of this unit, you should be able to read a timetable without confusing arrival, departure and activity time; ask for information politely; and write a short request that gives a clear purpose, date and contact detail.
:::

## 1.1 Reading a timetable: an educational tour

A timetable is a plan that tells us **what happens**, **when it happens** and sometimes **where it happens**. It is not a story to read from top to bottom only once. Scan its time column first, then connect every time with its action.

Imagine that Grade 8 is visiting a zoo for an educational tour. The group arrives at school at 9:00 a.m., boards the bus at 9:15, reaches the zoo at 9:45, explores animals from 10:05 a.m. to 2:00 p.m., and returns to school at 2:40 p.m. The exact timetable matters because a late student can miss the bus, a group that ignores the meeting time can get separated, and teachers need to know where every learner is.

```figure caption="A clear way to turn a tour timetable into a sequence of actions."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
items = [("09:00", "meet"), ("09:15", "board bus"), ("09:45", "arrive"), ("10:05–14:00", "explore"), ("14:10", "return"), ("14:40", "school")]
fig, ax = plt.subplots(figsize=(5.0, 2.5))
ax.set_xlim(-0.2, 5.2); ax.set_ylim(-0.2, 1.2); ax.axis('off')
for index, (time, action) in enumerate(items):
    x = index
    ax.add_patch(FancyBboxPatch((x-0.34, 0.32), 0.68, 0.38, boxstyle="round,pad=0.03", fc="#e9f3fb", ec=ACCENT, lw=1.1))
    ax.text(x, 0.55, time, ha='center', va='center', fontsize=8.3, color=INK, weight='bold')
    ax.text(x, 0.12, action, ha='center', va='center', fontsize=8.1, color=MUTED)
    if index < len(items)-1:
        ax.annotate('', xy=(x+0.63, 0.51), xytext=(x+0.37, 0.51), arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.1))
ax.text(2.5, 1.0, 'Read time first, then action', ha='center', va='center', color=INK, fontsize=10, weight='bold')
```

### The scan-and-check method

| Step | Ask yourself | Example answer |
|---|---|---|
| 1 | What is the event? | An educational tour to a zoo |
| 2 | What is the first fixed time? | Meet at school at 9:00 a.m. |
| 3 | What happens immediately before/after? | Board the bus at 9:15 a.m. |
| 4 | Which activity lasts longest? | Exploring the zoo |
| 5 | What must I prepare? | Be on time, follow the group and bring permitted materials |

::: example Reading between two times
**Problem.** The group reaches the zoo at 9:45 a.m. and enters at 10:05 a.m. How long do they have before entering?

**Solution.** From 9:45 to 10:00 is 15 minutes; from 10:00 to 10:05 is 5 minutes. Total waiting/preparation time = **20 minutes**.
:::

::: caution Do not invent timetable facts
If a timetable says “board the bus at 9:15”, do not answer “the bus leaves at 9:15” unless the table says so. Boarding and departure can be different events. Use the exact verb in the schedule.
:::

## 1.2 Asking for information politely

We ask for information every day: a bus stop, library opening time, homework deadline or event fee. The grammar choice changes the tone.

| Form | Best use | Example |
|---|---|---|
| **Can** | friendly, everyday request | Can you tell me the meeting time? |
| **Could** | more polite request | Could you show me the registration desk? |
| **Would** | polite offer/request | Would you please repeat the bus number? |
| **Do/does** | routine or general fact | Does the zoo open on Saturday? |

For a polite request, begin with a greeting, ask one clear question, and thank the listener. Avoid only saying “Time?” or “Where?”; those are incomplete and can sound rude.

::: example Turning a note into a question
**Problem.** You need the deadline for a tour form. Make a polite question.

**Solution.** “Excuse me, **could you please tell me when the tour form is due?**” The question has a polite opener, a modal verb and the exact information needed.
:::

### Word stress for clear speech

In English, one syllable of a longer word is often said more strongly. Stress helps a listener recognise the word.

| Word | Stress | Say it in a phrase |
|---|---|---|
| timetable | **TIME**-table | Please check the **TIME**-table. |
| information | in-for-**MA**-tion | I need more in-for-**MA**-tion. |
| educational | ed-u-**CA**-tion-al | It is an ed-u-**CA**-tion-al tour. |
| permission | per-**MI**-ssion | Ask for per-**MI**-ssion first. |

## 1.3 Present simple for schedules and habits

The present simple describes repeated actions, routines and fixed schedules.

| Subject | Positive | Negative | Question |
|---|---|---|---|
| I/you/we/they | We **meet** at 9:00. | We **do not meet** at 10:00. | **Do** we meet at 9:00? |
| he/she/it | The bus **leaves** early. | The bus **does not leave** late. | **Does** the bus leave early? |

Remember: after **does**, use the base verb. Write “Does the bus **leave** at 9:15?” not “Does the bus leaves…?”

::: example Schedule language
**Problem.** Correct the sentence: “The students goes to the zoo at 9:15.”

**Solution.** “The students **go** to the zoo at 9:15.” *Students* is plural, so use the base verb *go*.
:::

## 1.4 Filling in a form accurately

A form changes spoken information into a record. Read every label before writing. A name, date, class, contact number and signature each answer a different question.

| Form field | What belongs there | Common mistake to avoid |
|---|---|---|
| Full name | Your complete official name | Writing only a nickname |
| Class/section | Grade and section | Leaving out the section |
| Event | Exact event name | Writing an unrelated activity |
| Date | Day, month and year as asked | Mixing the event date and today’s date |
| Emergency contact | A reliable adult’s number | Giving an unreachable number |

::: tip Before you submit
Read the form once as if you were the teacher. Can the teacher identify you, contact home if needed and know which activity you joined? If not, complete the missing field before signing.
:::

## Chapter summary

- A timetable is read by linking each exact time to its exact action.
- Scan a schedule for the event, first action, sequence, longest activity and preparation.
- Use **can** for friendly requests and **could/would** for more polite requests.
- Present simple describes routines and schedules; use the base verb after **do/does**.
- Clear word stress makes information easier to understand.
- A form needs complete, accurate details because it becomes an official record.

## Practice questions

**Reading and information**

1. A tour bus boards at 8:40 a.m., leaves at 8:50 a.m. and reaches a museum at 9:30 a.m. How much time is available for boarding? <span class="marks">[1]</span>
2. Write two questions you could politely ask a teacher before joining an educational tour. <span class="marks">[2]</span>
3. Why is it useful to read both the time and the action in a timetable? <span class="marks">[2]</span>

**Grammar**

4. Choose the correct form: “Does Rupa ___ (bring/brings) her form today?” <span class="marks">[1]</span>
5. Change into a polite request: “Tell me the return time.” <span class="marks">[1]</span>
6. Complete: “The library ___ (open) at 10:00 a.m. on weekdays.” <span class="marks">[1]</span>

**Writing**

7. Write a short request to the school office asking for a tour-registration form. Include a greeting, your purpose, one specific question and a closing. <span class="marks">[4]</span>
8. Design a six-step timetable for a one-day class visit to a place in your district. Use times and action verbs. <span class="marks">[4]</span>

::: note Answers
**1.** 10 minutes, from 8:40 to 8:50.

**2.** Answers may include: “Could you please tell me the tour fee?” and “What time should we arrive at school?” A good answer is polite and asks one clear detail.

**3.** Time alone does not tell us what to do, and action alone does not tell us when to do it. Linking both prevents mistakes and late arrival.

**4.** **bring** — use the base verb after *does*.

**5.** “Could you please tell me the return time?”

**6.** **opens** — *library* is singular.

**7.** A strong answer has all four requested parts, for example: “Dear Sir/Madam, I would like to join the Grade 8 educational tour. Could you please give me a registration form and tell me the deadline? Thank you. Yours faithfully, …”

**8.** Check that each step has a sensible time, one action and a logical order: meet, travel, arrive, activity, return, reflection.
:::
