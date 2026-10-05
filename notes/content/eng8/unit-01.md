---
subject: Compulsory English
grade: 8
unit: 1
title: A Tour to Central Zoo / A Request Letter
hours: 0
area: Units
---

Two very different kinds of writing open your grade-8 book. The first is a
**guided tour text**: it tells you what you will see when you visit the Central
Zoo, when the animals are fed, and how to plan your day around a printed
schedule. The second is a **letter of request** in which a student asks the
principal for permission to go on that tour. Both are about information you
must actually *use* — read a timetable, find the one row you need, and then ask
politely for what you want. This unit also teaches the modal verbs that make a
request sound polite and the present simple tense that a timetable is written
in.

::: key What this unit asks of you
By the end you should be able to (1) read a timetable or a schedule and answer
questions from it without reading every row, (2) identify **can**, **could** and
**would** and explain how each changes the politeness of a request, (3) write a
request letter in the correct layout with its address, date, salutation, body,
closing and signature, (4) fill in a form neatly, and (5) say which syllable in
a word carries the stress.
:::

## 1.1 A Tour to Central Zoo

### About the text

The text is a **tour guide**, a piece of informative writing whose job is to
tell visitors what is where, what happens when, and what they are allowed to
do. It is written in the **present simple tense** ("the zoo opens at ten"), not
in the past, because it describes a place that is open every day and rules that
are true every day.

### What the text says

The Central Zoo is in Jawalakhel, Lalitpur, on the south-western edge of the
Kathmandu valley. It was opened to the public in 1932 as a private collection
of the Rana rulers and was handed over to the government in 1956; today it is
run by the National Trust for Nature Conservation. Over six hundred animals of
about a hundred species live inside it, including the royal Bengal tiger, the
one-horned rhinoceros, the Himalayan black bear, the sloth bear, the spotted
deer, the hippopotamus, several species of monkey, peacocks, crocodiles and a
large collection of birds and fish in the aquarium.

The guide divides the zoo into areas — the **bird house**, the **aquarium**,
the **reptile house**, the **animal enclosures**, the **children's park** and
the **picnic area** — and gives a suggested walking order so that a visitor
does not walk twice over the same path. It also prints the **feeding times**,
which are the most interesting part of any zoo visit because that is when the
animals move and the keepers talk about them.

| Information the guide gives | Where a question usually comes from |
|---|---|
| Opening and closing hours, and the weekly holiday | "How long is the zoo open on Saturday?" |
| Ticket prices for adults, children, students and foreigners | "How much would a class of 40 pay?" |
| Feeding times for each group of animals | "Which animals are fed at 2 p.m.?" |
| Location of each enclosure, and the suggested route | "Where is the aquarium?" |
| Rules — do not feed the animals, keep the zoo clean | "Why must we not throw plastic inside?" |

### Reading a timetable and a schedule

A **timetable** is a table of times. A **schedule** is the same idea for events
rather than departures. Both are read in the same three steps, and using them
saves you from reading the whole page:

1. **Find the row.** Look down the left-hand column, which holds the thing you
   are asking about — a day, an animal, a class.
2. **Find the column.** Look along the top, which holds the thing you want to
   know — an opening time, a price, a duration.
3. **Read the cell where they meet.** That single cell is the answer.

```figure caption="The three steps of reading a timetable. The row and the column meet in one cell — that cell is the answer, and every other cell is a distraction."
fig, ax = plt.subplots(figsize=(4.9, 2.9))
ax.set_xlim(0, 10); ax.set_ylim(0, 6.6); ax.axis("off")
data = [["Day", "Opens", "Closes", "Feeding"],
        ["Sunday", "10:00", "17:00", "11:00"],
        ["Monday", "—", "—", "closed"],
        ["Saturday", "09:00", "18:00", "14:00"]]
for r, row in enumerate(data):
    for c, cell in enumerate(row):
        hit = (r == 3 and c == 3)
        ax.add_patch(plt.Rectangle((0.6 + c * 2.2, 4.9 - r * 1.05), 2.2, 1.05,
                     fc=(ACCENT if hit else "white"), ec=GRID, lw=1))
        ax.text(1.7 + c * 2.2, 5.42 - r * 1.05, cell, ha="center", va="center",
                fontsize=7.4, color=("white" if hit else INK),
                fontweight=("bold" if hit or r == 0 else "normal"))
ax.annotate("row: Saturday", xy=(1.7, 1.68), xytext=(0.3, 0.5), fontsize=6.6,
            color=SERIES[2], arrowprops=dict(arrowstyle="->", color=SERIES[2], lw=1))
ax.annotate("column: feeding time", xy=(6.1, 2.4), xytext=(4.4, 4.15), fontsize=6.6,
            color=SERIES[0], arrowprops=dict(arrowstyle="->", color=SERIES[0], lw=1))
ax.text(6.1, 1.5, "answer: 14:00", ha="center", fontsize=7,
        color=ACCENT, fontweight="bold")
fig.tight_layout()
```

### Vocabulary

| Word | Meaning in this text |
|---|---|
| enclosure | a fenced area where animals are kept |
| species | a group of animals that can breed together |
| aquarium | a glass tank or building for fish |
| keeper | the person who feeds and looks after the animals |
| picnic area | a place with tables where visitors may eat |
| guided tour | a visit led by a person who explains what you see |
| entry fee | the money you pay to go in |

### Questions and model answers

**1. What is the best time to see the animals moving?**
The feeding times, because the animals come to the front of the enclosure and
the keeper explains them.

**2. Why does the guide give a suggested walking order?**
So that a visitor sees every area without walking twice over the same path.

::: note Model answers
**3. Why is the text written in the present simple tense?**
Because it describes things that are true every day — the zoo opens at the
same time each morning, and the same rules apply to every visitor.
**4. Why must visitors not feed the animals?**
Zoo animals are given a measured diet by the keepers. Food brought from
outside makes them ill and may even kill them, and it teaches them to beg.
:::

## 1.2 A Request Letter

### About the text

A **letter of request** asks somebody in authority to allow something: to go on
a tour, to grant leave, to issue a certificate. It is a formal letter, but a
school letter to the principal is only semi-formal — polite, short and
straightforward, without the stiffness of a government office letter.

### How a request letter is built

A formal letter has a fixed **layout**. Leaving out a part, or putting the
parts in the wrong order, costs marks even when the English is correct.

| Part | What goes there |
|---|---|
| Sender's address | your own address, at the top (in a school letter, often the class and roll number) |
| Date | below the address, written in full |
| Receiver's address | the principal's name and the school's address |
| Salutation | *Dear Sir / Dear Madam,* — followed by a comma |
| Subject | one line saying what the letter is about |
| Body | paragraph 1: why you are writing; paragraph 2: the details; paragraph 3: the request and thanks |
| Closing | *Yours faithfully,* if you began with *Dear Sir*, or *Yours sincerely,* if you used a name |
| Signature | your name, and your class and section below it |

```figure caption="The layout of a formal letter. Everything above the salutation is information; the two short body paragraphs do the actual asking."
fig, ax = plt.subplots(figsize=(4.6, 3.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 8.4); ax.axis("off")
parts = [("Sender's address", 7.8, SERIES[0]), ("Date", 6.9, SERIES[0]),
         ("Receiver's address", 6.0, SERIES[0]), ("Dear Sir,", 5.1, ACCENT),
         ("Subject: Permission for an educational tour", 4.3, SERIES[2]),
         ("Body para 1 — purpose", 3.4, SERIES[3]),
         ("Body para 2 — details, date, number of students", 2.6, SERIES[3]),
         ("Body para 3 — request and thanks", 1.8, SERIES[3]),
         ("Yours faithfully,", 0.95, ACCENT), ("Name, class and section", 0.3, SERIES[0])]
for label, y, colour in parts:
    ax.plot([0.4, 1.0], [y + 0.12, y + 0.12], color=colour, lw=2.2)
    ax.text(1.25, y + 0.12, label, va="center", fontsize=6.9, color=INK)
fig.tight_layout()
```

### Model request letter

> Jawalakhel, Lalitpur
> 14 Baisakh 2082
>
> The Principal
> Shree Saraswati Secondary School
> Lalitpur
>
> **Subject: Request for permission to visit the Central Zoo**
>
> Dear Sir,
>
> I am writing on behalf of the students of class 8 'B' to ask your permission
> for an educational tour to the Central Zoo, Jawalakhel.
>
> Our science teacher has taught us the chapter on living beings and their
> classification. A visit to the zoo would let us observe the animals we have
> only read about, and the keepers have agreed to explain the feeding of the
> animals to us. We would like to go on Friday, 25 Baisakh, from 10 a.m. to
> 2 p.m., with 42 students and two teachers.
>
> We would be grateful if you would kindly grant us permission. We assure you
> that we will obey all the zoo rules and return to school before the last
> period.
>
> Yours faithfully,
> Sunita Tamang
> Class 8 'B', Roll no. 14

::: tip The examiner is looking for
A correct layout (address, date, salutation, subject, closing, signature), a
polite and not demanding tone, and **details** — the date, the time, the number
of students. A letter that says only "please let us go to the zoo" loses the
content marks even if the grammar is perfect.
:::

## 1.3 Grammar and writing tasks of the unit

### Grammar: Modal verbs — can, could, would

**Modal verbs** are helping verbs that do not change their form. They have no
*-s* in the third person and no *-ed* in the past. Three of them — **can**,
**could** and **would** — are the ones you need for asking.

| Modal | Use | Example |
|---|---|---|
| can | ability, or a direct, informal request | I can swim. **Can** you help me? |
| could | a polite request, and past ability | **Could** you open the door, please? |
| would | the most polite request; also a wish | **Would** you please grant me leave? |

The important idea is **politeness**. "Give me a pen" is an order. "Can I have
a pen?" is a request. "Could I have a pen?" is more polite. "Would you mind
giving me a pen?" is the most polite of all. In a letter to your principal,
use **could** or **would**, never **can** on its own.

::: caution Common mistakes
- *He **cans** swim.* ✗ — a modal never takes **-s**: *He **can** swim.* ✓
- *I **could** to go.* ✗ — after a modal use the bare verb: *I **could** go.* ✓
- *Would you please **to** help me?* ✗ — *Would you please **help** me?* ✓
- Using *can* in a formal letter to the principal. Use *could* or *would*.
:::

### Grammar: The present simple tense

The present simple is used for facts, habits and **timetables**.

| Person | Affirmative | Negative | Question |
|---|---|---|---|
| I / You / We / They | visit | do not visit | Do you visit…? |
| He / She / It | visits | does not visit | Does he visit…? |

Add **-s** (or **-es** after *ch, sh, s, x, o*) in the third person singular:
*he watches*, *she goes*, *it closes*. Timetables and schedules are always in
the present simple: *The zoo opens at ten. The train leaves at six.*

::: example Worked example
**Rewrite these sentences using the modal given.**
(1) Open the window. (could) (2) I am able to ride a bicycle. (can)
(3) It is necessary for you to come early. (would — as a polite request)

**Answers.** (1) **Could** you open the window, please? (2) I **can** ride a
bicycle. (3) **Would** you please come early?
:::

### Writing I: Interpreting a timetable

When a question says *"Look at the schedule and answer"*, do not describe the
whole schedule. Answer the question asked, quoting the exact time or price,
and use the present simple:

> Q: When does the zoo close on Saturday and how long is it open?
> A: It opens at 9:00 a.m. and closes at 6:00 p.m., so it is open for nine
> hours.

### Writing II: Filling in a form

A form asks for information in boxes. Write **clearly and completely**:

- write in block capitals if the form asks for it;
- put the date in the order the form shows (day/month/year or year/month/day);
- never leave a required box blank — write *N/A* if it does not apply;
- for a tour form, the usual boxes are name, class and section, roll number,
  guardian's name, contact number, and a signature.

::: note Key to Exercise A
**1.** could **2.** can **3.** cannot **4.** Would **5.** could **6.** can
**7.** Would **8.** can **9.** could **10.** cannot
:::

## Chapter summary

- The Central Zoo is in Jawalakhel, Lalitpur; it opened in 1932 and is now run
  by the National Trust for Nature Conservation.
- A timetable is read in three steps: find the row, find the column, read the
  meeting cell.
- The present simple tense is used for facts, habits and timetables: *the zoo
  opens at ten*.
- **can** = ability or a direct request; **could** = a polite request or past
  ability; **would** = the most polite request.
- A modal verb never takes **-s** and is always followed by the bare verb.
- A formal letter needs the sender's address, the date, the receiver's address,
  the salutation, a subject line, the body, the closing and the signature.
- *Yours faithfully* follows *Dear Sir*; *Yours sincerely* follows a name.
- A request letter must give details — the date, the time and the number of
  people — and must not sound like an order.

## Practice questions

**Reading**

1. Read the following schedule and answer the questions. <span class="marks">[5]</span>

   | Day | Zoo opens | Zoo closes | Bird house feeding |
   |---|---|---|---|
   | Sunday | 10:00 | 17:00 | 11:00 |
   | Monday | closed | closed | — |
   | Friday | 10:00 | 17:00 | 11:00 |
   | Saturday | 09:00 | 18:00 | 14:00 |

   (a) On which day is the zoo closed? (b) How long is the zoo open on
   Saturday? (c) At what time are the birds fed on Saturday? (d) Is the zoo
   open longer on Sunday or on Saturday? (e) A family reaches the gate at
   3 p.m. on Friday. How long can they stay?

2. Why does the tour guide divide the zoo into areas? <span class="marks">[2]</span>
3. Give two rules a visitor to the zoo must follow, and say why each matters. <span class="marks">[2]</span>

::: note Answers
**1.** (a) Monday. (b) From 09:00 to 18:00, nine hours. (c) At 2 p.m.
(d) On Saturday — nine hours against seven. (e) Two hours, from 3 p.m. to
5 p.m.
**2.** So that a visitor sees every area and does not walk twice over the same
path; it also makes the visit shorter and easier to plan.
**3.** Do not feed the animals — outside food makes them ill and teaches them
to beg. Keep the zoo clean — plastic thrown into an enclosure can be eaten by
an animal and kill it.
:::

**Grammar**

4. Fill in the blanks with *can*, *could* or *would*. <span class="marks">[5]</span>
   (a) ______ you please lend me your pen?
   (b) Sara ______ speak three languages.
   (c) ______ you help me with this sum, please?
   (d) When I was five I ______ not read.
   (e) ______ you kindly grant me two days' leave?

5. Rewrite in the third person singular (he / she). <span class="marks">[3]</span>
   (a) They visit the zoo every Saturday. (b) We do not feed the animals.
   (c) Do you open the gate at ten?

::: note Answers
**4.** (a) Could (or Would) (b) can (c) Could (d) could (e) Would
**5.** (a) He visits the zoo every Saturday. (b) She does not feed the
animals. (c) Does he open the gate at ten?
:::

**Writing**

6. Write a letter to your principal asking permission for your class to visit
   a place of historical interest. Give the date, the time and the number of
   students. <span class="marks">[5]</span>
7. Fill in this tour form in block capitals. <span class="marks">[3]</span>

   | Field | Your entry |
   |---|---|
   | Full name | |
   | Class and section | |
   | Roll number | |
   | Guardian's contact number | |
   | Place to visit | |
   | Date of visit | |
   | Signature | |

::: note Answers
**6.** Use the opening "I am writing on behalf of the students of class … to
ask your permission for …". In the second paragraph give the place, the date,
the time and the number of students and teachers. In the third, make the
request and thank the principal. Close with *Yours faithfully* and your name,
class and roll number.
**7.** All entries in block capitals, the roll number and the contact number in
figures, the date in the order the form shows, and a signature in the last box.
:::
