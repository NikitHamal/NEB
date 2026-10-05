---
subject: Compulsory English
grade: 8
unit: 3
title: Public Announcements / How to Wash Clothes in a Washing Machine
hours: 0
area: Units
---

This unit is about two kinds of writing that tell people what to do. A **public
announcement** tells a large number of people one piece of information in a
hurry — a cancellation, a meeting, a lost article. A set of **instructions**
tells one person, step by step, how to do a job — here, how to wash clothes in
a washing machine. Both have to be clear the first time they are read, because
nobody re-reads an announcement and nobody wants to guess a step. The unit also
teaches how to report a yes/no question in indirect speech.

::: key What this unit asks of you
By the end you should be able to (1) write an announcement that answers what,
where, when, who and what to do, (2) write instructions in the correct order
using the imperative, (3) turn a direct yes/no question into reported speech
with *if* or *whether*, and (4) pronounce the letter **r** correctly — sounded
where it is followed by a vowel, silent where it is not.
:::

## 3.1 Public Announcements

### About the text

An announcement is a short, public notice. It is written to be read at a
glance, so it uses short lines, a heading and sometimes a box. You meet
announcements on a school notice board, at a bus park, in a hospital, on the
radio and in a supermarket.

An announcement is **not** an essay. It does not discuss, explain or tell a
story. It gives one piece of information and, usually, one action.

### What a good announcement contains

| Question | What the announcement must give | Example |
|---|---|---|
| What? | the event or the change | "The morning assembly is cancelled." |
| Where? | the place, precisely | "in the main hall" |
| When? | date and time | "on Sunday, 12 Bhadra, at 8 a.m." |
| Who? | who must attend or who is affected | "all students of classes 8 and 9" |
| What to do? | the action, and whom to contact | "report to your class teacher" |
| Who said it? | the issuer and the date | "By order of the Principal" |

An announcement has no greeting and no *Dear students*. It begins with the
heading, gives the information, and ends with the issuer's name. Any question it
does not answer — a wrong date, a missing room — is a fault, because the reader
cannot ask you back.

```figure caption="The five questions every announcement answers. If one is missing, the reader has to ask somebody — and an announcement that has to be explained has failed."
fig, ax = plt.subplots(figsize=(4.8, 2.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.6); ax.axis("off")
cards = [("WHAT", "assembly cancelled", SERIES[0]),
         ("WHERE", "main hall", SERIES[1]),
         ("WHEN", "Sunday, 8 a.m.", SERIES[2]),
         ("WHO", "classes 8 and 9", SERIES[3]),
         ("DO", "report to class teacher", SERIES[4])]
for i, (head, note, colour) in enumerate(cards):
    x = 0.3 + i * 1.92
    ax.add_patch(plt.Rectangle((x, 2.4), 1.74, 1.7, fc="white", ec=colour, lw=1.4))
    ax.text(x + 0.87, 3.7, head, ha="center", fontsize=6.6, color=colour,
            fontweight="bold")
    ax.text(x + 0.87, 3.05, note, ha="center", fontsize=5.6, color=MUTED)
ax.text(5.0, 1.6, "heading · information · issuer and date", ha="center",
        fontsize=6.8, color=INK)
fig.tight_layout()
```

### Model announcement

> **NOTICE**
> **INTER-HOUSE VOLLEYBALL TRIALS**
> All students of classes 8, 9 and 10 who wish to play in the inter-house
> volleyball tournament must attend the trials.
> **Date:** Saturday, 18 Bhadra 2082
> **Time:** 7:00 a.m. — 9:00 a.m.
> **Place:** School playground
> Bring your sports dress and a water bottle. Students who do not attend the
> trials will not be selected.
> — Prakash Adhikari, Sports Teacher

### Vocabulary

| Word | Meaning |
|---|---|
| announcement | a public statement giving information |
| notice | a written announcement put on a board |
| cancelled | stopped from happening |
| trials | a test to choose players for a team |
| by order of | as instructed by (used in official announcements) |
| venue | the place where something happens |

::: note Model answers
**1. Why does an announcement use short lines rather than full paragraphs?**
Because it must be understood in a few seconds by a reader who is standing up
or walking past, and a short line can be taken in at one glance.
**2. An announcement says "the exam will be held next week". Name the two
pieces of information it is missing.**
The exact day and the exact time (and also the room, if it is not the usual
one).
:::

## 3.2 How to Wash Clothes in a Washing Machine

### About the text

This text is a set of **instructions** — sometimes called a procedure. It tells
one person how to carry out a task, in order. Instructions use the
**imperative**: *check*, *put*, *add*, *close*, *start*.

### The order of the steps

Instructions only work if they are in the right order. Read the list below not
as words but as a **sequence**, and notice that each step depends on the one
before it: you cannot add detergent before the clothes are in the drum, and you
cannot start the machine before the door is shut.

1. **Check the pockets** of every item and empty them. A coin or a pen left in
   a pocket stains the whole load and can damage the drum.
2. **Sort the clothes** into whites, coloureds and dark items. Sort by fabric
   too: heavy towels and jeans are washed separately from light shirts.
3. **Read the care label** on each garment for a temperature limit and a
   hand-wash-only warning.
4. **Load the drum** loosely. A drum that is stuffed will not clean the clothes
   and can strain the motor.
5. **Add detergent** to the detergent drawer — not more than the manufacturer
   recommends. Too much soap leaves a residue and makes the machine overflow.
6. **Close the door firmly** until it clicks.
7. **Choose the programme** and the temperature, then press **Start**.
8. **Wait** until the machine signals that the cycle has finished. Never force
   the door open mid-cycle while the drum may be full of water.
9. **Unload and hang the clothes** in the sun immediately, so that creases and
   damp smells do not set in.

```figure caption="Instructions are a chain, not a list. Each step uses the result of the step before it, so moving one step changes the meaning of the whole set."
fig, ax = plt.subplots(figsize=(4.5, 3.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 8.4); ax.axis("off")
steps = ["1. Empty the pockets", "2. Sort by colour and fabric",
         "3. Read the care label", "4. Load the drum loosely",
         "5. Add detergent", "6. Close the door",
         "7. Choose programme, start", "8. Unload and hang out"]
for i, s in enumerate(steps):
    y = 7.7 - i * 0.95
    ax.add_patch(plt.Rectangle((1.6, y - 0.3), 6.8, 0.62, fc="white",
                 ec=(ACCENT if i in (4, 6) else GRID), lw=1.2))
    ax.text(1.85, y, s, va="center", fontsize=6.8, color=INK)
    if i < len(steps) - 1:
        ax.annotate("", xy=(1.6, y - 0.62), xytext=(1.6, y - 0.34),
                    arrowprops=dict(arrowstyle="->", color=GRID, lw=1.2))
ax.text(5.0, 0.28, "order matters: a step cannot come before its cause",
        ha="center", fontsize=6.3, color=MUTED)
fig.tight_layout()
```

### Vocabulary

| Word | Meaning |
|---|---|
| detergent | soap powder or liquid used for washing |
| drum | the round part of the machine that turns |
| load | the quantity of clothes washed at one time |
| cycle | one complete wash programme |
| care label | the small label sewn inside a garment |
| residue | a small amount left behind after washing |

## 3.3 Grammar and writing tasks of the unit

### Grammar: Reported speech — yes/no questions

When you report a **yes/no** question, you do not use the question word order
and you do not use a question mark. Instead you join the two parts with **if**
or **whether**. The tense usually moves back one step.

| Direct | Reported |
|---|---|
| She said, "Are you ready?" | She asked **if** I was ready. |
| He said, "Do you like tea?" | He asked **whether** I liked tea. |
| The teacher said, "Have you finished?" | The teacher asked **if** we had finished. |
| Mother said, "Can you help me?" | Mother asked **if** I could help her. |
| Ram said, "Will you come tomorrow?" | Ram asked **if** I would come the next day. |

Three changes happen every time: the **tense** moves back, the **pronoun**
changes to fit the new speaker, and the **time word** may change (*tomorrow* →
*the next day*, *now* → *then*, *here* → *there*). The question word order
disappears — "Are you ready" becomes "I was ready", with the subject first.

::: caution Common mistakes
- *She asked if was I ready.* ✗ — reported speech is a statement: *She asked
  if **I was** ready.* ✓
- *He asked if I liked tea?* ✗ — there is no question mark in reported speech.
- *He said if I liked tea.* ✗ — with a question use **asked**, not *said*.
:::

### Writing: An announcement

Write in the order *heading → information → action → issuer*. Use the present
simple (*the trial takes place*), the future (*will be held*) or the imperative
(*report to…*). Do not use *Dear* or *Yours faithfully*, and do not thank
anybody.

::: example Worked example
**Announcement.** **NOTICE — WATER SUPPLY INTERRUPTION.** The main water tank
of the school hostel will be cleaned on Wednesday, 21 Bhadra 2082, from 9 a.m.
to 2 p.m. There will be no water supply in the hostel during these hours.
Students should fill their buckets the previous evening. — Hostel Warden.
:::

### Writing: A set of instructions

Give a title, then number the steps and begin each with a verb in the
imperative. Add one short *why* wherever a reader might be tempted to skip the
step — "close the door firmly **so that water does not leak**". A warning goes
before the step it applies to, never after it.

## Chapter summary

- An announcement gives one piece of information in a hurry and answers what,
  where, when, who and what to do.
- It has a heading, the information, the action and the issuer — and no
  greeting or closing.
- Instructions use the imperative and must be in the correct order, because
  each step depends on the one before it.
- Reported yes/no questions are joined with **if** or **whether**, lose the
  question mark and use statement word order.
- Reported speech moves the tense one step back and changes the pronoun and the
  time words.
- The letter **r** is pronounced when a vowel follows it (*red*, *road*) and is
  silent when it is at the end of a word or before a consonant (*car*, *park*
  in standard British English).

## Practice questions

**Reading**

1. What are the five questions every announcement must answer? <span class="marks">[5]</span>
2. Why should you read the care label before washing a garment? <span class="marks">[2]</span>
3. Give two reasons why the drum should not be overloaded. <span class="marks">[2]</span>

::: note Answers
**1.** What is happening; where; when; who is affected; and what they should do
(plus who issued it and the date).
**2.** The label gives the highest temperature the fabric can take and warns
about garments that must not be machine-washed at all. Ignoring it shrinks or
ruins the garment.
**3.** An overloaded drum does not let the clothes move, so they stay dirty; and
the extra weight strains the motor and can damage the machine.
:::

**Grammar**

4. Report these questions, beginning with *He asked…*. <span class="marks">[5]</span>
   (a) "Are you coming to the meeting?" (b) "Do you know the answer?"
   (c) "Have you seen my bag?" (d) "Can you swim?" (e) "Will you help me
   tomorrow?"

5. Punctuate these sentences correctly. <span class="marks">[3]</span>
   (a) where are you going asked Mira (b) the machine is not working he said
   (c) do not touch the drum said the technician it is still turning

::: note Answers
**4.** (a) He asked if I was coming to the meeting. (b) He asked if I knew the
answer. (c) He asked if I had seen his bag. (d) He asked if I could swim.
(e) He asked if I would help him the next day.
**5.** (a) "Where are you going?" asked Mira. (b) "The machine is not working,"
he said. (c) "Do not touch the drum," said the technician. "It is still
turning."
:::

**Writing**

6. Write an announcement for your school notice board informing students that
   the school is closed for three days for Dashain. <span class="marks">[5]</span>
7. Write six numbered instructions for charging a mobile phone safely. <span class="marks">[4]</span>

::: note Answers
**6.** Include a heading (DASHAIN HOLIDAY), the dates on which the school is
closed and the date on which it reopens, the fact that all classes are
cancelled and that extra classes will be held afterwards, and the issuer.
**7.** Sample: 1. Use the charger that came with the phone. 2. Check that the
cable is not cut or frayed. 3. Plug the charger into the socket first, then
into the phone. 4. Do not leave the phone charging overnight on a bed or a
pillow. 5. Unplug the charger when the battery reaches 100 %. 6. Never charge a
phone while it is inside a bag where heat cannot escape.
:::
