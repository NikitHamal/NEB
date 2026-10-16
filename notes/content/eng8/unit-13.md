---
subject: Compulsory English
grade: 8
unit: 13
title: Nepal is the First Country to Double its Tiger Population / Drama: A Mousetrap
hours: 0
area: Units
---

The first text is a **data text**: it reports a result in numbers, and shows
them in a chart. Reading it means reading the figures as carefully as the
sentences. The second is a **one-act drama** — a short play written to be acted,
with a setting, a list of characters, dialogue and stage directions. Between
them they teach the two things this unit's grammar is about: how much and how
many, and how to express quantity exactly.

::: key What this unit asks of you
By the end you should be able to (1) read a table or graph and describe what it
shows, (2) write a description of data without copying the numbers in the order
they appear, (3) explain how a drama differs from a story, and (4) use *much,
many, some, any, a few, a little, a lot of, plenty of* correctly.
:::

```photo id="eng8/bengal-tiger" caption="A royal Bengal tiger in Chitwan National Park. Nepal's camera-trap surveys identify each animal by its stripe pattern, which is unique to that tiger." width="92"
```

## 13.1 Nepal is the First Country to Double its Tiger Population

### About the text

The text is **reporting writing** about a conservation result. It states the
achievement, gives the numbers behind it, explains how the count was made, and
says why the result matters beyond Nepal.

### What the text says

In 2010 the thirteen countries that share the tiger's range met in St
Petersburg and set themselves a target — **TX2**: to double the number of wild
tigers by 2022, the next Chinese Year of the Tiger. In 2022 Nepal announced that
it had reached the target, the first of the thirteen countries to do so.

The numbers behind the announcement come from the **National Tiger and Prey
Survey**. Nepal's estimate rose from about **121 tigers in 2009** to about
**198 in 2013**, then to **235 in 2018**, and to **355 in 2022** — close to
three times the 2009 figure. The survey is not a single census: teams walk
transects, record signs and prey animals, and combine the photographs from
hundreds of camera traps, using the stripe pattern of each animal, which is
unique to that tiger, to identify individuals.

| Survey year | Estimated tigers in Nepal |
|---|---|
| 2009 | about 121 |
| 2013 | about 198 |
| 2018 | about 235 |
| 2022 | about 355 |

Three things made the result possible. First, **protected areas were enlarged
and connected**: Chitwan, Bardia, Banke, Shuklaphanta and Parsa national parks
and the forests between them, linked by corridors so that a young tiger can
walk from one park to another. Second, **prey and habitat were restored** —
grassland managed by cutting and burning, wetlands cleared of invasive plants,
and community forests handed to local user groups. Third, **poaching was
suppressed** by anti-poaching units, informer networks and joint patrols with
the army and the community, with zero-poaching years achieved in several parks.

The success is real and incomplete. Tigers need about 100 square kilometres
each, so a growing population presses against the boundary of every park;
livestock and people are killed each year at the edges. A tiger may be worth a
great deal to tourism, but it is worth more to the ecosystem as an **apex
predator**, keeping the numbers of deer and wild boar in balance and so keeping
the forest the way it is. The question the report leaves the reader with is
whether the next decade can hold the number steady while also keeping the people
who live beside the parks safe.

```figure caption="The TX2 result in one picture. Nepal's estimate rose from about 121 tigers in 2009 to about 355 in 2022 — and the surveys behind the figures are counts of individuals identified by their stripes, not guesses."
fig, ax = plt.subplots(figsize=(4.9, 2.6))
years = ["2009", "2013", "2018", "2022"]
vals = [121, 198, 235, 355]
bars = ax.bar(years, vals, width=0.55, color=[SERIES[1], SERIES[1], SERIES[1], ACCENT])
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 8, str(v), ha="center",
            fontsize=7.5, color=INK, fontweight="bold")
ax.set_ylabel("estimated tigers", fontsize=8)
ax.tick_params(labelsize=8)
ax.set_ylim(0, 400)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

### Describing data

A description of data does **not** walk through the table row by row. It does
four things:

1. **The overall direction** first: *The number of tigers rose steadily between
   2009 and 2022.*
2. **The starting point and the end point**, with the change: *from about 121 to
   about 355, an increase of about 234.*
3. **The sharpest movement**: *The largest jump came between 2018 and 2022, when
   the estimate rose by about 120.*
4. **The reason or the conclusion**: *The increase followed the linking of
   protected areas and the suppression of poaching.*

Words you will need: *rose, increased, went up, fell, decreased, dropped,
remained steady, doubled, nearly tripled, peaked, the highest, the lowest,
whereas, compared with*.

### Vocabulary

| Word | Meaning |
|---|---|
| estimate | a figure worked out from samples rather than counted exactly |
| census | an official count of every individual |
| transect | a fixed line along which a survey team records what it finds |
| camera trap | a camera that photographs an animal as it passes |
| corridor | a strip of habitat that lets animals move between two areas |
| apex predator | the animal at the top of the food chain |
| poaching | illegal hunting |

::: note Model answers
**1. How do scientists know how many tigers there are?**
They walk transects and record signs and prey, and they set hundreds of camera
traps. Because every tiger's stripe pattern is unique, each photographed animal
can be identified as an individual, and the number of different individuals gives
the estimate.
**2. Why is a tiger called an apex predator, and why does that matter?**
Because nothing hunts it. It controls the numbers of deer and wild boar, and so
protects the vegetation they would otherwise overgraze — removing it changes the
whole forest.
:::

## 13.2 Drama: A Mousetrap

### About the text

The second text is a **one-act drama** — a short play. Drama is written to be
**performed**, not read silently, and that single fact explains almost every
difference between a play and a story.

| Feature | A story | A drama |
|---|---|---|
| How it tells | the narrator describes and explains | the characters speak and act |
| How you learn about a character | the narrator tells you | you infer it from what they say and do |
| Setting | described in the text | given in the stage directions and the set |
| Time | can jump about freely | happens in front of the audience, in order |
| What carries the meaning | description and comment | dialogue, pause, movement, silence |
| The reader's job | to follow a narrator | to imagine watching |

In a play, the **stage directions** matter as much as the dialogue. When a
direction says *(pause)*, or *(she turns away)*, or *(the lights go down)*, it
is telling the actor how the line is meant. A line that reads flatly on the page
can be a joke, a threat or a sadness, and the stage direction decides which.

Every drama contains a **conflict** — a problem that the characters struggle
with — and the conflict is what makes the audience stay. It can be between two
people, between a person and a situation, or inside one person.

### Vocabulary

| Word | Meaning |
|---|---|
| drama | a play, written to be performed by actors |
| dialogue | the words the characters speak |
| stage direction | a note in the script telling the actor or the director what to do |
| scene | a division of a play marked by a change of place or time |
| conflict | the struggle between opposing forces in a play or story |
| mousetrap | a trap for catching mice — here, the title's central image |

::: note Model answers
**1. How is a drama different from a story?**
In a story a narrator describes the events and tells the reader what characters
are like; in a drama the characters speak and act, and the reader learns what
they are like from their dialogue and their behaviour.
**2. Why are stage directions important?**
Because they tell the actor how a line is meant to be spoken and where the
character moves, so they decide whether a line is funny, threatening or sad.
Without them the same words could be performed in completely different ways.
:::

## 13.3 Grammar and writing tasks of the unit

### Grammar: much, many, some, any, and expressing quantity

| Word | Used with | In which sentences | Example |
|---|---|---|---|
| many | countable plurals | questions and negatives (and formal positives) | How **many** tigers are there? |
| much | uncountable nouns | questions and negatives | There isn't **much** water. |
| a lot of / lots of | both | all kinds of sentence | **A lot of** birds come here. |
| some | both | positive sentences; offers and requests | We saw **some** deer. |
| any | both | negatives and questions | We didn't see **any** tigers. |
| a few / few | countable plurals | *a few* = some; *few* = almost none | **A few** visitors came. |
| a little / little | uncountable | *a little* = some; *little* = almost none | There is **a little** hope. |
| plenty of | both | more than enough | There is **plenty of** grassland. |
| each / every | singular countable | all of a group, taken one by one | **Every** park has a boundary. |

::: caution Common mistakes
- *How much tigers are there?* ✗ (tigers are countable) → *How **many** tigers
  are there?* ✓
- *There are much people.* ✗ → *There are **many** people.* / *There are **a lot
  of** people.* ✓
- *I have some money?* ✗ as a question → *Do you have **any** money?* ✓
- *Few people came* (= almost nobody) is not the same as *A few people came*
  (= some people). ✓ Note the difference: it changes the meaning.
:::

### Writing: Describing data and presenting it in a graph

For a data question: write the overall trend first, then the figures that prove
it, then one exception or turning point, then the conclusion. If you must draw
the graph, label both axes, give the graph a title, and choose a scale that uses
the paper — a bar chart for separate years, a line graph for a trend over time.

::: note Model answers to the practice questions
**Data description model.** "The number of tigers in Nepal rose in every survey
between 2009 and 2022. It began at about 121 and ended at about 355, an
increase of about 234, or nearly three times the original estimate. The largest
single rise came between 2018 and 2022, when about 120 animals were added,
whereas the rise between 2013 and 2018 had been only about 37. The survey
figures are estimates from camera-trap photographs, not exact counts."
:::

## 13.5 Writing about data and conservation

Conservation questions almost always come with a number. Using it well is what
separates a four-mark answer from a two-mark one.

```figure caption="Nepal's wild tiger count. A number used in an answer should always carry its year and its source — that is what makes it evidence rather than decoration."
yrs = ["2009", "2013", "2018", "2022"]
tigers = [121, 198, 235, 355]
fig, ax = plt.subplots(figsize=(5.0, 2.8))
ax.plot(yrs, tigers, color=SERIES[2], marker="o", markersize=6, linewidth=2.2)
ax.fill_between(range(len(yrs)), tigers, color=SERIES[2], alpha=0.14)
for i, v in enumerate(tigers):
    ax.text(i, v + 12, str(v), ha="center", color=INK, fontsize=9)
ax.set_ylabel("wild tigers", color=MUTED)
ax.set_ylim(0, 420)
ax.grid(axis="y", color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(colors=MUTED)
```

| Weak sentence | Stronger sentence |
|---|---|
| *Tigers have increased a lot.* | *Nepal's wild tiger count rose from 121 in 2009 to 355 in 2022.* |
| *Community forestry is good.* | *Community forests now cover about a third of Nepal's forest area and are managed by nearly 23,000 user groups.* |
| *People and tigers have problems.* | *As the count rose, so did encounters: conservation now has to protect people as well as tigers.* |

::: example A four-mark answer built on evidence
**Question.** How did Nepal double its tiger population? Write four points.

**Answer.** (i) **Protection** — soldiers and rangers patrolled the Tarai
parks, and anti-poaching units worked with local informers, so poaching fell
to near zero in several years. (ii) **Habitat corridors** — community forests
joined Chitwan, Bardiya, Parsa, Banke and Shuklaphanta, so young tigers could
move and find territory instead of dying at the edges. (iii) **Local benefit**
— village programmes compensated livestock losses and shared tourism income,
so farmers reported tigers instead of poisoning them. (iv) **Measurement** —
camera-trap surveys every four years showed the count rising from 121 in 2009
to 355 in 2022, which kept the funding and the policy in place.
:::

::: note Activity — a conservation fact file
Choose one protected species of Nepal (one-horned rhinoceros, snow leopard,
red panda, gharial, Bengal florican). Make a one-page fact file: where it
lives, how many are left, the main threats, what is being done, and one
sentence on what a student can do. Use at least two numbers with their years.
:::

## Chapter summary

- Nepal was the first of the thirteen tiger-range countries to double its wild
  tiger population under the **TX2** target set in 2010.
- The estimates rose from about 121 tigers in 2009 to about 355 in 2022.
- The figures come from the National Tiger and Prey Survey, which identifies
  individual tigers by their unique stripe patterns in camera-trap photographs.
- The increase followed the linking of protected areas, the restoration of prey
  and grassland, and the suppression of poaching.
- The success brings a new problem: tigers need large territories, so a growing
  population presses against the parks' boundaries.
- A **drama** is written to be performed; the audience learns about characters
  from dialogue and stage directions, not from a narrator.
- A data description gives the overall trend first, then the figures, then the
  turning point, then the conclusion.
- **many** with countable plurals; **much** with uncountables; **some** in
  positives; **any** in negatives and questions; **a few / a little** = some,
  **few / little** = almost none.

## Practice questions

**Reading**

1. What was the TX2 target and who set it? <span class="marks">[2]</span>
2. How is a tiger survey actually carried out? <span class="marks">[3]</span>
3. Give two problems that come with a growing tiger population. <span class="marks">[2]</span>
4. How is a drama different from a story? Give two differences. <span class="marks">[2]</span>

::: note Answers
**1.** It was the target, agreed in 2010 at St Petersburg by the thirteen
tiger-range countries, of doubling the number of wild tigers by 2022; Nepal was
the first country to reach it.
**2.** Survey teams walk fixed transects recording signs and prey animals, and
hundreds of camera traps photograph tigers as they pass; because each tiger's
stripe pattern is unique, every photographed animal can be identified as an
individual, and the number of different individuals gives the estimate.
**3.** Tigers need very large territories, so a growing population moves beyond
the parks, and livestock and people are attacked at the edges.
**4.** A drama is written to be performed and tells its story through dialogue
and stage directions, while a story is told by a narrator; and the reader of a
drama must infer what a character is like, while a story can state it.
:::

**Grammar**

5. Fill in *much, many, some, any, a few* or *a little*. <span class="marks">[5]</span>
   (a) How ______ tigers are left in the park?
   (b) We did not see ______ deer today.
   (c) There is ______ water left in the bottle.
   (d) ______ visitors came in the morning.
   (e) There isn't ______ grass in the enclosure.

::: note Answers
**5.** (a) many (b) any (c) a little (d) A few (e) much
:::

**Writing**

6. Describe the tiger figures in the table above in about 100 words. <span class="marks">[5]</span>
7. Write a short scene of about 120 words between two students who have found a
   stray dog in the school compound. Include stage directions. <span class="marks">[5]</span>

::: note Answers
**6.** Start with the overall trend, then give the first and last figures and
the size of the change, then point out the largest rise (2018–2022), then say
where the figures come from (camera-trap estimates) and what the conclusion is.
**7.** Give a heading, a list of characters and a setting, then the dialogue.
Use stage directions in brackets — *(looks around)*, *(whispers)*, *(the bell
rings)* — to show how the lines are meant. Make sure the scene contains a small
conflict, for example one student wants to keep the dog and the other is afraid
of the caretaker.
:::

**Extra practice**

**Group B (2 marks each)**

**11.** Rewrite with evidence: *Many tourists visit Chitwan.*
**12.** Use *poaching* and *corridor* in sentences of your own.

**Group C (4 marks)**

**13.** Write a news report of about 120 words on a tiger count released by the
    government.

::: note Extra practice — answers
**11.** e.g. *Chitwan National Park drew more than 170,000 visitors in 2023,
about a fifth of them Nepali school groups.*
**12.** e.g. *Poaching fell sharply after the army began joint patrols.* /
*The forest corridor lets young tigers move between Chitwan and Parsa.*
**13.** Marks: a factual headline; a place-and-date line; a lead sentence
answering what, where, when and who; the figures with their years; a
quotation from an official or a local resident; a closing sentence on what
happens next. Third person, past tense, no personal opinion.
:::
