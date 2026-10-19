---
subject: Compulsory English
grade: 8
unit: 13
title: Nepal is the First Country to Double its Tiger Population / Drama: A Mousetrap
hours: 0
area: Units
---

Unit 13 is about **reading and presenting information** and about **helping
others**. Reading I is a report from the National Trust for Nature Conservation
(NTNC) on how Nepal became the first country to double its wild tiger
population. Reading II is a short play, *A Mousetrap*, in which farm animals
refuse to help a frightened mouse — and pay for it. The grammar is
**quantifiers** (*much, many, some, any, a few, a little…*) and a review of
**present tenses**. In writing you interpret a chart and describe a process
from a flowchart.

::: key What the exam asks from this unit
(1) Read numbers and trends from a report or chart. (2) Use quantifiers with
countable and uncountable nouns, *some* in positive sentences and *any* in
questions and negatives. (3) Choose present simple, present continuous, present
perfect or present perfect continuous. (4) Describe a chart (overview → main
figures → comparison) and a process (passive voice, sequence words).
:::

```photo id="eng8/bengal-tiger" caption="A Royal Bengal tiger in Chitwan National Park. In Nepal's surveys, camera traps identify each tiger by its stripe pattern, which is unique." width="92"
```

## 13.1 Reading I: Nepal is the first country to double its tiger population

### Summary

- Nepal's **fourth tiger and prey survey** began in December (2021), led by the
  **DNPWC** and the **Department of Forests and Soil Conservation**. Surveys are
  held every four years.
- Earlier counts: **121 (2009), 198 (2013), 235 (2018)**. The 2022 count
  (announced on 29 July 2022, Global Tiger Day) was **355** — nearly **three
  times** the 2009 figure.
- Dr. Chiranjibi P. Pokharel of NTNC calls this "historical": tigers are **apex
  predators** at the top of the **food chain**, so their numbers show the health
  of forests and ecosystems.
- A century ago about **100,000** tigers lived in Asia; by 2010 they had fallen
  by **97%** to about **3,200**, mainly because of **habitat loss and
  poaching**. In 2010 the **13 tiger-range countries** signed the **St.
  Petersburg Declaration** (Russia), pledging to double tigers by 2022
  (**TX2**).
- Nepal's steps: new habitat (**Banke National Park**, extension of **Parsa
  National Park**); the **National Tiger Conservation Committee** chaired by the
  **Prime Minister**; **Wildlife Crime Control Bureau** units from centre to
  district; **over 450 community-based anti-poaching units**; partnerships and
  investment from national and international **stakeholders**.
- Future threats: poaching, illegal wildlife trade, climate change,
  human–tiger conflict. Needed: protect prey (gaur, swamp deer, sambar, nilgai,
  wild buffalo), involve communities, use good science, make development
  **wildlife-friendly**, and manage **corridors** linking habitats.

(The textbook misprints NTNC as the "National Trust for Nature
*Conversation*"; it is **Conservation**.)

```figure caption="Tiger numbers in Nepal from the four national surveys. 2009 to 2022: 121 → 355, almost three times."
fig, ax = plt.subplots(figsize=(4.6, 2.8))
years = ["2009", "2013", "2018", "2022"]
vals = [121, 198, 235, 355]
bars = ax.bar(years, vals, color=[SERIES[0]]*3 + [ACCENT], width=0.55)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width()/2, v + 8, str(v), ha="center",
            fontsize=8.5, color=INK)
ax.set_ylabel("Number of tigers", fontsize=8.5, color=INK)
ax.set_ylim(0, 400)
ax.spines[['top', 'right']].set_visible(False)
ax.tick_params(labelsize=8.5)
ax.grid(axis="y", color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

### Vocabulary (Exercise A)

a–iv (nationwide), b–vi (intricately), c–ii (poaching), d–i (enforcement),
e–iii (coexistence), f–v (dispersal)

### Gap filling (Exercise B)

a. **235** b. **food** c. **the Prime Minister** d. **stakeholders**
e. **wildlife-friendly**

### Comprehension (Exercise C) — model answers

**a. How many tiger surveys have been conducted?** Four — in 2009, 2013, 2018
and the fourth begun in December 2021.

**b. What was the percentage of tigers in 2010 in Asia?** The population had
fallen by 97%, so only about **3%** of the tigers of a century earlier were
left — about 3,200.

**c. When was the St. Petersburg Declaration made?** In 2010.

**d. Mention one initiative Nepal adopted.** It established Banke National Park
and extended Parsa National Park to give tigers more habitat. (Also: the
committee chaired by the Prime Minister, WCCB units, over 450 community
anti-poaching units.)

**e. What are the threats to tiger conservation?** Poaching, illegal wildlife
trade and the impacts of climate change (also human–tiger conflict and loss of
habitat).

## 13.2 Writing I: Interpreting charts, graphs and tables

**Plan:** (1) *Introduction* — what the chart shows, where and when. (2)
*Overview* — the main trend in one sentence. (3) *Details* — highest, lowest,
key numbers, comparisons. (4) *Conclusion* (optional). Use the trend
vocabulary below and do **not** give opinions not supported by the data.

| Trend | Verbs / nouns | Adverbs |
|---|---|---|
| up | rise, increase, climb, grow, shoot up, a rise | sharply, rapidly, steadily, gradually |
| down | fall, decrease, drop, decline, a fall | slightly, considerably, dramatically |
| no change | remain stable / steady / constant | — |

::: example Model answer — Tiger numbers in Nepal (the bar graph above)
The bar graph shows the number of wild tigers in Nepal in the four national
surveys from 2009 to 2022. Overall, the number rose steadily and almost tripled
over the period.

In 2009 there were only 121 tigers. The number increased sharply to 198 in 2013,
and then rose slightly to 235 in 2018. The largest jump came between 2018 and
2022, when it shot up by 120 to 355. Thus Nepal more than doubled its tiger
population and achieved its TX2 target.
:::

The textbook's Writing I chart (men and women studying engineering) appears as
a picture; use the same plan — e.g. *"The chart shows the number of male and
female engineering students… Men outnumber women in every year, but the number
of women is rising gradually…"*

## 13.3 Grammar I: Quantifiers — much/many, some/any

| With countable nouns (*eggs, tomatoes*) | With uncountable nouns (*milk, work, time*) | With both |
|---|---|---|
| many, a few, few, several, each, either, neither, both, fewer | much, a little, little, a bit of, less | some, any, a lot of, lots of, enough, all, most, no, more |

- **some** in positive sentences and in **offers/requests**: *Would you like
  some tea?* **any** in negatives and questions: *Did you see any friends?*
- **much** mostly in negatives/questions: *Do we have much time?* In positive
  sentences prefer **a lot of**: *I used to drink a lot of milk.*
- **no** = not any: *There's **no** milk.* (not *There's not no milk*).
- **a few / a little** = some (positive); **few / little** = almost none
  (negative feeling).

### Textbook answers (Grammar I B)

a. no b. less c. some d. enough e. a lot of f. a lot of g. some (*much* cannot
go with countable *eggs*; *any* would be the most natural) h. some

::: caution Common mistakes
- *many milk / much books* ✗ → *much milk, many books* ✓
- *less people* → *fewer people* (countable) ✓
- *I have some money? / I don't have some money* ✗ → *Do you have **any**
  money? / I don't have **any** money* ✓
:::

## 13.4 Reading II: Drama — A Mousetrap

### Characters and plot

**Characters:** Man, Woman, Doctor, Mouse, Chicken, Lamb, Buffalo.

1. A mouse peeps through the wall as a man and a woman open a package — it is a
   **mousetrap**. The horrified mouse runs to warn the others.
2. The **chicken**: "it is a big problem for you, but I don't care."
3. The **lamb**: "the mousetrap is not for me… I can only pray."
4. The **buffalo**: "That won't hurt me. Am I in danger? I don't think so."
5. That night the trap catches the **tail of a deadly snake**; in the dark the
   woman goes to look and the snake **bites** her. She faints; the doctor
   advises **chicken soup** for her fever — the chicken is cooked.
6. Friends and neighbours visit; to feed them the man cooks the **lamb**.
7. When she recovers, the couple hold a party for well-wishers and the
   **buffalo** becomes "the main dish".
8. Only the mouse is saved. **Moral:** help others when they ask, because we
   never know when we will be in the same situation; a problem for one member
   of a community is a problem for all.

**Features of drama:** a list of characters; **dialogue** with the speaker's
name in capitals; **stage directions** in brackets and italics, describing
actions and setting (*The woman fainted. The man called the doctor.*).

### Vocabulary (Exercise A)

a. **package** – a parcel; something wrapped for sending or carrying b. **worried**
– anxious, unhappy about a problem c. **ingredient** – one of the things used to
make a dish d. **delicious** – very tasty e. **celebrate** – mark a happy event with
a party or ceremony

### Order of events (Exercise B)

**c → g → a → b → e → f → d**

### Comprehension (Exercise C) — model answers

**a. Why was the mouse shocked?** Because the package was a mousetrap, and he
was afraid he would be trapped and killed.

**b. Who did the mouse tell about the mousetrap?** The chicken, the lamb and
the buffalo.

**c. What did the lamb reply?** That the mousetrap was not for him, there was
nothing he could do, but he would pray for the mouse.

**d. What happened to the woman in the dark?** A deadly snake caught in the trap
bit her, and she fainted.

**e. Why did the couple kill the buffalo?** To feed their friends and neighbours
at the party they gave to celebrate the woman's recovery.

## 13.5 Grammar II: Present tenses (review)

| Tense | Form | Use | Signal words |
|---|---|---|---|
| Present simple | V / V-s | habits, facts, states | always, every day, usually |
| Present continuous | am/is/are + V-ing | happening now; temporary | now, Look!, Listen!, at the moment |
| Present perfect | has/have + V3 | result now; experience | just, already, yet, ever |
| Present perfect continuous | has/have been + V-ing | started in the past and still continuing | for, since, all day |

**Stative verbs** (*know, belong, remember, like, want*) are not normally used
in continuous forms: *We **know** him well* (not *are knowing*).

### Textbook answers

**Grammar II A:** a. is – present simple b. shows – present simple c. Look –
imperative; is running – present continuous d. 've found – present perfect
e. 'd been studying – past perfect continuous; were born – past simple

**Grammar II B:** a. i give b. i are c. i get up d. ii is raining e. iii has
cleaned f. ii is playing g. iv have been living (iii *have lived* also
acceptable) h. i reads i. i know j. i remembers

**Grammar II C:** a. belongs b. is calling c. play d. is taking e. is carrying
f. have lost g. has been dancing h. Have … heard i. am living j. has been
teaching (or *has taught*)

## 13.6 Writing II: Describing a process from a flowchart

Use the **passive voice** (the doer is not important) and **sequence words**
(*first, then, next, after that, finally*).

::: example Model answer — Making orange juice (textbook Writing I)
The flowchart shows how orange juice is made. First, the oranges are received
from the farms or the market. Then the best oranges are selected and the bad
ones are thrown away. After that, the selected oranges are cleaned thoroughly.
Next, the juice is extracted from the oranges, and it is filtered to remove the
seeds and pulp. Finally, the fresh juice is served in a glass.
:::

The tea process (Speaking B) can be described the same way: *First, the tea
leaves are **picked**. Then they are **withered**, **fermented** and **dried**.
After that, they are **sorted**, and finally the tea is **stored and packed**.*

## 13.7 Speaking, pronunciation and project work

**Reading a table (Speaking A):** *Which is the largest state? — Texas
(695,621 km²). Which state has the most people? — California (34 million).
Which became a state first? — New York (1788).*

**Words for charts:** 'constant, 'rising, trend, a'scend, de'scend,
de'crease (verb) / 'decrease (noun), de'cline, 'steadily, 'rapidly,
pro'portion.

**Project work:** count the boys and girls in classes 6–8 and draw a bar graph.

## Chapter summary

- Nepal's tigers: 121 (2009) → 198 (2013) → 235 (2018) → 355 (2022); TX2
  target from the 2010 St. Petersburg Declaration; Banke NP, Parsa extension,
  PM-chaired committee, WCCB, 450+ anti-poaching units.
- Drama *A Mousetrap*: chicken, lamb and buffalo refuse to help and are all
  eaten; moral — help others in need.
- Countable: many, a few, fewer; uncountable: much, a little, less; both:
  some, any, a lot of, enough, no.
- *some* in positives and offers; *any* in negatives and questions.
- Describing a chart: introduction, overview, details with numbers, trend words.
- Process description: passive + *first, then, next, finally*.

## Practice questions

**Reading**

1. Answer from the texts. <span class="marks">[5]</span>
   (a) Who led the fourth tiger survey? (b) What does TX2 mean? (c) How many
   tiger-range countries signed the 2010 declaration? (d) What did the doctor
   suggest for the woman? (e) Which animal was saved at the end?

::: note Answers — Reading
**1.** (a) The DNPWC and the Department of Forests and Soil Conservation.
(b) Doubling the wild tiger population by 2022. (c) Thirteen. (d) Chicken soup.
(e) The mouse.
:::

**Grammar**

2. Fill in with *much, many, some, any, a few* or *a little*. <span class="marks">[5]</span>
   (a) How ___ students are there? (b) There isn't ___ sugar left. (c) Would you
   like ___ tea? (d) I have ___ friends in Pokhara. (e) Add ___ salt to the soup.
3. Use the correct present tense. <span class="marks">[3]</span>
   (a) Listen! Someone (knock) at the door. (b) She (live) here since 2075.
   (c) Water (boil) at 100 °C.

::: note Answers — Grammar
**2.** (a) many (b) much/any (c) some (d) a few (e) a little
**3.** (a) is knocking (b) has lived / has been living (c) boils
:::

**Writing**

4. The table shows SEE pass rates of a school: 2078 – 62%, 2079 – 70%, 2080 –
   68%, 2081 – 85%. Write a description. <span class="marks">[5]</span>

::: note Answer — Writing
**4.** Model: *The table shows the SEE pass rate of the school from 2078 to
2081. Overall, the rate improved by 23 percentage points. It rose from 62% in
2078 to 70% in 2079, fell slightly to 68% in 2080, and then jumped sharply to
85% in 2081, the highest in the period.*
:::
