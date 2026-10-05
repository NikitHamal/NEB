---
subject: Compulsory English
grade: 8
unit: 19
title: A Tale of Two Birds / News Report: Pokhara International Airport Inaugurated
hours: 0
area: Units
---

The last unit of the book puts a **folk narrative** beside a **newspaper
report**, and the contrast is deliberate. A folk tale is old, anonymous and
moral; a news report is immediate, named and factual, and it answers six
questions in its first two sentences. The grammar of the unit is the one that
turns a person's words into a report: **reported speech**.

::: key What this unit asks for
By the end you should be able to (1) tell a folk tale with a moral, (2) write a
news report with a headline, a lead and a body, (3) report statements, questions
and orders in indirect speech, and (4) design the front page of a newspaper.
:::

```photo id="eng8/pokhara-airport" caption="The signboard at Pokhara Regional International Airport, inaugurated on 1 January 2023 — Nepal's second international airport." width="68"
```

## 19.1 A Tale of Two Birds

### About the text

The text is a **folk narrative** — the kind of story that has no author because
everybody owns it. Its two birds are usually not simply animals: one has learned
to imitate the worst it has heard and the other the best, and the tale turns on
what happens when a traveller meets each in turn.

### The shape and the moral

| Element | What the tale does |
|---|---|
| Setting | the same tree, or the same forest, and two nests |
| Characters | two birds, alike in appearance and utterly different in speech |
| The test | a traveller or a stranger meets each bird and is treated differently |
| The climax | the traveller wonders how the same tree produced two such birds |
| The moral | what we become is mostly what we have been near |

The device the tale uses is **parallelism**: the same situation is given twice,
with one thing changed, so that the reader compares them without being told to.
Folk tales use this constantly, because it is the easiest way to make an idea
visible to a listener who is hearing the story only once.

The moral — that we are shaped by the company and the words around us — is
stated in some versions and left for the reader to supply in others. In an
answer, quote the moment at which the two birds are compared, and say what the
comparison shows.

### Vocabulary

| Word | Meaning |
|---|---|
| folk tale | an old story handed down by word of mouth |
| to imitate | to copy the way somebody speaks or behaves |
| parallel | two things in the same shape, set side by side |
| moral | the lesson a story teaches |
| to reflect | to show something back, as a mirror does |

::: note Model answers
**1. What makes the two birds different if they are alike?**
Their habits and their speech: each has copied the kind of talk it heard most,
so one treats the traveller kindly and the other drives him away.
**2. What is the moral of the tale, and how does the tale make it clear?**
That we become like the company we keep and the words we hear. The tale makes it
clear by setting the two birds in the same place with the same visitor, so the
only difference the reader can see is what each bird has learned to say.
:::

## 19.2 News Report: Pokhara International Airport Inaugurated

### About the text

The text is a **news report**. A news report is factual, brief and impersonal,
and it is written to answer six questions in its opening: **who, what, where,
when, why and how**. In newspaper language this opening paragraph is called the
**lead** (or *intro*), and it carries the whole story in two or three sentences;
everything after it adds detail of decreasing importance.

### What the text says

**Pokhara Regional International Airport** was inaugurated on **1 January
2023** by the then Prime Minister, Pushpa Kamal Dahal, at Pokhara in Kaski
district. It was Nepal's **second international airport**, after Tribhuvan
International Airport in Kathmandu, and the first in Gandaki Province. The
airport was built by the China CAMC Engineering company under a loan agreement
with China, at a cost of about 22 billion rupees, on about 400 hectares of land
in Chinnedanda, about three kilometres east of Pokhara's city centre.

The main features are a **runway 2,500 metres long and 45 metres wide**, a
**terminal designed to handle about one million passengers a year**, an
apron, a taxiway, a control tower and a cargo building. The runway is shorter
than Kathmandu's and cannot take the largest long-haul aircraft fully loaded,
so the airport is designed mainly for medium-range international flights and
for regional traffic.

The report also gives the hopes and the difficulties. Supporters expect the
airport to bring tourists directly to the Annapurna region, cut connecting
journeys through Kathmandu, and create local employment and freight capacity.
Critics point to the **debt** the loan creates, the number of airlines that must
be persuaded to fly there, the fee the airport must earn to service the loan,
and the fact that an airport built for a million passengers needs a million
passengers to come. Both points of view are part of the story, and a good report
includes both without taking sides.

| News question | Answer in the report |
|---|---|
| Who? | Prime Minister Pushpa Kamal Dahal (inaugurated it) |
| What? | Nepal's second international airport |
| Where? | Chinnedanda, Pokhara, Kaski |
| When? | 1 January 2023 |
| Why? | to bring tourists and trade directly to the region |
| How? | built by CAMC (China) on a Chinese loan of about Rs 22 billion |

```figure caption="The structure of a news report: an inverted pyramid. The lead carries the whole story, and each later paragraph is less essential than the one before it, so that an editor can cut from the bottom."
fig, ax = plt.subplots(figsize=(4.7, 2.7))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.6); ax.axis("off")
widths = [(6.6, "Lead — who, what, where, when", ACCENT),
          (5.2, "Detail — how, how much, features", SERIES[2]),
          (3.8, "Background — why it matters", SERIES[3]),
          (2.2, "Quotes and reactions", SERIES[0])]
y = 4.6
for w, label, colour in widths:
    ax.add_patch(plt.Rectangle((5 - w / 2, y), w, 0.85, fc=colour, ec="none",
                 alpha=0.85))
    ax.text(5.0, y + 0.42, label, ha="center", va="center", fontsize=6.1,
            color="white" if colour != SERIES[3] else INK)
    y -= 0.95
ax.text(5.0, 0.35, "cut from the bottom, never from the top", ha="center",
        fontsize=6.2, color=MUTED)
fig.tight_layout()
```

### Vocabulary

| Word | Meaning |
|---|---|
| inaugurate | to open a building or an office formally |
| terminal | the building where passengers arrive and depart |
| runway | the strip on which aircraft take off and land |
| apron | the paved area where aircraft stand |
| freight | goods carried by a vehicle or an aircraft |
| loan | money borrowed that must be paid back, with interest |
| lead | the opening paragraph of a news report |

::: note Model answers
**1. What are the six questions a news report answers?**
Who, what, where, when, why and how.
**2. Why does the report include the criticisms of the airport as well as the
hopes?**
Because both are part of what happened: the loan must be repaid and the
passengers must be found, so a report that gave only the hopes would be
advertising rather than news.
:::

## 19.3 Grammar and writing tasks of the unit

### Grammar: Reported speech — a summary

| Kind of sentence | Direct | Reported |
|---|---|---|
| Statement | "The airport opened in 2023." | He said (that) the airport **had opened** in 2023. |
| Yes/no question | "Is the runway long enough?" | He asked **if** the runway **was** long enough. |
| Wh- question | "When did it open?" | He asked **when** it **had opened**. |
| Order | "Close the gate." | He **told** us **to** close the gate. |
| Request | "Please help me." | He **asked** me **to** help him. |
| Warning | "Don't go near the edge." | He **warned** us **not to** go near the edge. |

The four changes are always the same: the **reporting verb** changes (*said,
asked, told, warned*); the **tense** moves one step back; the **pronoun**
changes to fit the new speaker; and the **time and place words** change
(*today → that day, tomorrow → the next day, here → there, this → that*).
In a statement the tense may also be left unchanged if what was said is still
true — *He said the airport **is** Nepal's second international airport* — which
is common in news writing.

::: caution Common mistakes
- *He said me that…* ✗ → *He **told** me that…* or *He said that…* ✓
- *She asked that where I lived.* ✗ → *She asked **where** I lived.* ✓
- Reported speech never keeps a question mark or quotation marks.
- *He told to me* ✗ → *He told me* ✓
:::

### Writing: A news report and a front page

A news report needs a **headline** (short, active, no full stop), a **byline**
(*By our correspondent*), a **lead** of two sentences carrying the six
questions, and a body of three or four short paragraphs in order of decreasing
importance. Use the **passive** and the **past tense** freely (*was
inaugurated*, *were invited*), attribute opinions (*according to officials*),
and do not use *I* or *we*.

A front-page design needs a masthead (the newspaper's name and date), one main
headline with its lead, two or three smaller stories in columns, and a picture
with a caption. A caption is a sentence, not a label.

::: note Model answers to the practice questions
**Lead model.** "KATHMANDU — The government announced on Sunday that a new
bridge over the Trishuli will open in Ashad. The 180-metre bridge, built in two
years at a cost of Rs 420 million, will replace a crossing that has been closed
every monsoon for a decade."
:::

## Chapter summary

- A folk tale uses **parallelism** — the same situation twice with one thing
  changed — so that the reader makes the comparison without being told to.
- The moral of "A Tale of Two Birds" is that we become like the company we keep
  and the words we hear.
- A news report answers **who, what, where, when, why and how** in its opening
  paragraph, called the lead.
- Pokhara Regional International Airport was inaugurated on 1 January 2023 by
  Prime Minister Pushpa Kamal Dahal; it is Nepal's second international airport.
- Its runway is 2,500 m long, its terminal is designed for about a million
  passengers a year, and it was built by CAMC on a Chinese loan of about Rs 22
  billion.
- A good report gives both the hopes and the criticisms, without taking sides.
- Reported speech changes the reporting verb, the tense, the pronoun and the
  time and place words; questions are joined with *if* or the question word;
  orders use *told / asked / warned* + *to* + verb.
- News writing uses the passive and the past tense and never uses *I*.

## Practice questions

**Reading**

1. How does the tale show the difference between the two birds? <span class="marks">[2]</span>
2. What is the moral of "A Tale of Two Birds"? <span class="marks">[2]</span>
3. Give four facts about Pokhara Regional International Airport. <span class="marks">[4]</span>
4. Why do news reports put the most important information first? <span class="marks">[2]</span>

::: note Answers
**1.** By parallelism: the same visitor meets each bird in the same place, and
the only difference is what each bird has learned to say, so the reader is shown
the two habits side by side.
**2.** That we become like the company we keep and the words we hear.
**3.** Any four: it is Nepal's second international airport; it was inaugurated
on 1 January 2023; it is in Chinnedanda, Pokhara (Kaski); it was built by CAMC
of China under a loan of about Rs 22 billion; its runway is 2,500 m long and
45 m wide; its terminal is designed for about one million passengers a year.
**4.** Because an editor may have to cut the report to fit the space, so the
least important paragraphs are placed last and can be removed without losing
the story.
:::

**Grammar**

5. Report these sentences. <span class="marks">[5]</span>
   (a) "The airport opened last year," the official said.
   (b) "Have you seen the new terminal?" she asked.
   (c) "Where is the check-in desk?" the passenger asked.
   (d) "Fasten your seat belt," the crew said.
   (e) "Don't stand near the runway," the guard warned.

::: note Answers
**5.** (a) The official said (that) the airport had opened the previous year.
(b) She asked if I had seen the new terminal. (c) The passenger asked where the
check-in desk was. (d) The crew told us to fasten our seat belts. (e) The guard
warned us not to stand near the runway.
:::

**Writing**

6. Write a news report of about 150 words about an event in your school. <span class="marks">[5]</span>
7. Write a story of about 120 words with the moral "we become what we are
   near". <span class="marks">[5]</span>

::: note Answers
**6.** Give a headline without a full stop, a byline, a lead of two sentences
carrying the six questions, then three short paragraphs in order of decreasing
importance, with one quotation attributed to a named person. Use the past tense
and the passive, and do not use *I* or *we*.
**7.** Use parallelism: two children, the same situation, one thing different —
for example the same class, the same teacher, one who listened and one who did
not. Keep to the past simple and end with the difference the reader has already
noticed rather than a moral in bold.
:::
