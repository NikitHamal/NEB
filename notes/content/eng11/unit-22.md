---
subject: Compulsory English
grade: 11
unit: 22
title: 'Tenses: Present, Past and Future'
hours: 4
area: Grammar
---

Tense is how an English verb shows **time**; aspect is how it shows whether the
action is finished, still going on, or both. Together they give twelve verb forms,
and almost every NEB Q7 paper contains two or three tense items — usually a blank
with the base verb in brackets (*She ____ in Biratnagar since 2015. (live)*) or a
sentence to correct. The whole area is learnable because each tense has one fixed
structure and a small set of signal words that give it away.

::: key The three questions that pick a tense
**(1) When?** past, present or future — that is the tense.
**(2) Is it in progress?** if yes, use a continuous form (*be* + V-ing).
**(3) Is it completed before the time we are talking about?** if yes, use a
perfect form (*have/has/had* + V3). Answer the three and the form writes itself.
:::

## 22.1 The twelve tenses at a glance

In the structures below, **V1** is the base form, **V2** the past form, **V3** the
past participle and **V-ing** the present participle. `s/es` is added only for
third-person singular subjects (*he, she, it*, a singular noun).

| Tense | Structure | Example | Main use |
|---|---|---|---|
| Simple present | S + V1 (+ s/es) | Sita **goes** to college at nine. | habits, routines, general truths, timetables |
| Present continuous | S + am/is/are + V-ing | She **is writing** her assignment now. | happening now, temporary, fixed near-future plans |
| Present perfect | S + have/has + V3 | I **have visited** Lumbini twice. | past action with present result; unfinished time |
| Present perfect continuous | S + have/has been + V-ing | It **has been raining** since morning. | action started in the past and still going on |
| Simple past | S + V2 | We **went** to Chitwan last year. | a finished action at a finished past time |
| Past continuous | S + was/were + V-ing | He **was cooking** when I arrived. | an action in progress at a past moment |
| Past perfect | S + had + V3 | The bus **had left** before we reached. | the earlier of two past actions |
| Past perfect continuous | S + had been + V-ing | She **had been waiting** for two hours. | duration up to a point in the past |
| Simple future | S + will + V1 | I **will call** you tomorrow. | prediction, instant decision, promise |
| Future continuous | S + will be + V-ing | At 8 p.m. I **will be studying**. | in progress at a future moment |
| Future perfect | S + will have + V3 | By 2030 he **will have retired**. | finished before a future moment |
| Future perfect continuous | S + will have been + V-ing | By May she **will have been teaching** for ten years. | duration up to a future moment |

```figure caption="The twelve tenses on one timeline. A dot is a single completed action, a wavy span is an action in progress, and an arrow shows a result carried forward to the reference time."
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots(figsize=(5.2,3.4))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
# main time axis
ax.annotate('', xy=(9.9,1.0), xytext=(0.15,1.0),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.4, mutation_scale=12))
for x, lab in [(2.0,'PAST'), (5.3,'NOW'), (8.6,'FUTURE')]:
    ax.plot([x,x],[0.80,1.20], color=INK, lw=1.4)
    ax.text(x, 0.40, lab, ha='center', va='center', fontsize=8.6, color=INK)
def wavy(x0, x1, y, c):
    t = np.linspace(x0, x1, 160)
    ax.plot(t, y + 0.10*np.sin(14*(t-x0)), color=c, lw=1.5)
def lab(x, y, s, c, ha='center'):
    ax.text(x, y, s, ha=ha, va='center', fontsize=7.6, color=c)
# ---- past band
y = 2.4
ax.plot([2.0],[y],'o', color=SERIES[0], ms=6, mec='white', mew=0.9, zorder=5)
lab(2.0, y+0.55, 'simple past', SERIES[0])
wavy(1.1, 2.9, y+1.55, SERIES[1])
lab(2.0, y+2.10, 'past continuous', SERIES[1])
ax.plot([0.7],[y+3.05],'o', color=SERIES[2], ms=6)
ax.annotate('', xy=(1.95,y+3.05), xytext=(0.78,y+3.05),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.1, mutation_scale=9))
lab(1.4, y+3.60, 'past perfect', SERIES[2])
# ---- present band
wavy(3.1, 5.3, 2.4, SERIES[3])
ax.plot([5.3],[2.4],'o', color=SERIES[3], ms=5, mec='white', mew=0.9, zorder=5)
lab(4.2, 2.95, 'present perfect cont.', SERIES[3])
ax.plot([3.4],[3.95],'o', color=SERIES[4], ms=6)
ax.annotate('', xy=(5.25,3.95), xytext=(3.5,3.95),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[4], lw=1.1, mutation_scale=9))
lab(4.3, 4.50, 'present perfect', SERIES[4])
wavy(4.6, 6.0, 5.5, ACCENT)
lab(5.3, 6.05, 'present continuous', ACCENT)
ax.plot([4.3],[6.9],'o',color=MUTED, ms=4.5)
ax.plot([5.3],[6.9],'o',color=MUTED, ms=4.5)
ax.plot([6.3],[6.9],'o',color=MUTED, ms=4.5)
lab(5.3, 7.45, 'simple present  (repeated habit)', MUTED)
# ---- future band
ax.plot([8.6],[2.4],'o', color=SERIES[0], ms=6, mec='white', mew=0.9, zorder=5)
lab(8.6, 2.95, 'simple future', SERIES[0])
wavy(7.7, 9.5, 3.95, SERIES[1])
lab(8.6, 4.50, 'future continuous', SERIES[1])
ax.plot([7.1],[5.5],'o', color=SERIES[2], ms=6)
ax.annotate('', xy=(8.55,5.5), xytext=(7.2,5.5),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.1, mutation_scale=9))
lab(7.9, 6.05, 'future perfect', SERIES[2])
ax.plot([8.6,8.6],[1.2,5.5], color=GRID, lw=0.8, ls=':', zorder=0)
ax.plot([2.0,2.0],[1.2,5.45], color=GRID, lw=0.8, ls=':', zorder=0)
ax.plot([5.3,5.3],[1.2,6.8], color=GRID, lw=0.8, ls=':', zorder=0)
ax.text(0.15, 9.3, 'dot = one completed act    wave = in progress    arrow = result carried forward',
        fontsize=7.4, color=MUTED, ha='left', va='center')
```

## 22.2 The present tenses

### Simple present

**Structure.** Subject + V1; add **-s/-es** for *he, she, it* and singular nouns.
Questions and negatives use *do/does* + V1.

**Rules and uses.**

1. **Habits and repeated actions.** *Ramesh **catches** the 7 a.m. bus to
   Kalanki every day.* / *We **celebrate** Dashain in Ashwin.*
2. **General truths and permanent states.** *The Koshi **flows** into the Ganges.*
   / *Water **boils** at 100 °C.*
3. **Timetables and scheduled future events.** *The flight to Simara **leaves** at
   6.15 tomorrow.*
4. **Commentary, instructions and narration of a story's plot.** *He **passes** the
   ball to Kiran, who **shoots**.*
5. **In time clauses after *when, if, before, after, as soon as, until*** — the
   future is expressed by the present. *I will ring you as soon as the bus
   **reaches** Mugling.*

::: caution The third-person -s under exam pressure
The single commonest one-mark loss in Q7. *He **go** to school* is wrong; *He
**goes** to school* is right. Check every present-tense verb in your answer whose
subject is *he, she, it*, a name, or a singular noun. Also remember the -s is
**gone** after *does/doesn't*: *She **doesn't go**,* never ~~doesn't goes~~.
:::

### Present continuous

**Structure.** am/is/are + V-ing.

1. **Happening at this moment.** *Look — it **is snowing** in Jomsom.*
2. **Temporary situation around now.** *I **am staying** with my aunt in Lalitpur
   this month.*
3. **A definite future arrangement.** *We **are flying** to Nepalgunj on Sunday.*
4. **A changing situation.** *The population of Kathmandu **is growing** fast.*
5. **With *always*, a complaint about repetition.** *He **is always losing** his
   pen.*

::: caution Stative verbs take no continuous form
Verbs of **possession** (*have, own, belong, possess*), **thinking** (*know,
believe, understand, remember, mean, agree*), **feeling** (*like, love, hate,
want, prefer, need*) and **the senses** (*see, hear, smell, taste, seem, appear*)
describe states, not actions, and normally have no *-ing* form.
~~He is having a car~~ → **He has a car.**
~~I am agree with you~~ → **I agree with you.** (*agree* is a verb, not an adjective)
~~I am knowing the answer~~ → **I know the answer.**
~~She is wanting a new phone~~ → **She wants a new phone.**
*Have* **can** be continuous when it means an activity, not possession:
*We **are having** dinner* / *He **is having** a bath* are both correct.
:::

### Present perfect

**Structure.** have/has + V3.

1. **A past action whose result matters now.** *I **have lost** my citizenship
   certificate.* (so I do not have it now)
2. **Experience at an unstated time.** *She **has climbed** Kala Patthar.*
3. **An action in a period of time that is not yet over** — *today, this week,
   this year*. *We **have had** three tests this month.*
4. **With *just, already, yet, ever, never, so far, recently, lately***.
   *The results **have just** been published.*
5. **With *since* (a point) and *for* (a length)** when the state continues.
   *He **has worked** at the bank **since** 2019 / **for** six years.*

### Present perfect continuous

**Structure.** have/has been + V-ing. It stresses the **duration** of an activity
that began earlier and is still going on (or has just stopped).

- *It **has been raining** since Tuesday.* (and it is still raining)
- *They **have been building** the new road for two years.*

| | Present perfect | Present perfect continuous |
|---|---|---|
| Focus | the result, the completed amount | the activity and how long it lasted |
| Example | I **have read** forty pages. | I **have been reading** all afternoon. |
| Typical words | already, just, yet, twice, ever | for, since, all day, how long |

::: caution Simple past or present perfect?
A **finished past time expression** — *yesterday, last night, in 2018, two days
ago, when I was a child* — forces the **simple past**.
~~I have met him yesterday~~ → **I met him yesterday.**
~~When did you have come?~~ → **When did you come?**
Conversely, *since*, *for* + up-to-now, *just*, *already*, *yet* and *so far*
force the present perfect: *He has been in Doha **since** last Dashain*.
:::

## 22.3 The past tenses

### Simple past

**Structure.** Subject + V2 for all persons; questions and negatives use *did* +
**V1**.

1. **A finished action at a stated or understood past time.** *The earthquake
   **struck** Nepal on 25 April 2015.*
2. **A sequence of finished past actions in a story.** *He **opened** the gate,
   **parked** the bike and **went** inside.*
3. **A past habit**, often with *used to* or *would*. *My grandfather **walked**
   to Ilam every week.*

::: caution Never put the past tense after *did*
*Did* already carries the past. The main verb goes back to V1.
~~Did you went to Bhaktapur?~~ → **Did you go to Bhaktapur?**
~~She didn't came.~~ → **She didn't come.**
~~Where did he bought it?~~ → **Where did he buy it?**
The same rule applies to *does* and *do*: ~~Does he plays?~~ → **Does he play?**
:::

### Past continuous

**Structure.** was/were + V-ing.

1. **In progress at a stated past moment.** *At 6 o'clock yesterday I **was
   watching** the news.*
2. **A longer background action interrupted by a shorter one** — the long one is
   continuous, the short one is simple past, joined by *when* or *while*.
   *While we **were crossing** the Bagmati bridge, the rain **started**.*
3. **Two actions going on together**, joined by *while*. *Mother **was cooking**
   while father **was reading** the newspaper.*

### Past perfect

**Structure.** had + V3, for every subject.

Use it for **the earlier of two past actions**, when making the order clear
matters. The later action is in the simple past.

- *The train **had already left** when we reached the station.*
- *She told me that she **had seen** that film before.*
- *After the guests **had gone**, we cleared the table.*

If the order is already obvious from *before* or *after*, the simple past is also
acceptable — but the past perfect is never wrong in that position.

### Past perfect continuous

**Structure.** had been + V-ing. It gives the **duration** of an activity up to a
past point.

- *He **had been driving** for nine hours before he stopped at Mugling.*
- *They **had been waiting** at the bus park since dawn when the strike was
  announced.*

## 22.4 The future tenses and other ways of talking about the future

### Simple future

**Structure.** will + V1 (*shall* is now used mainly with *I/we* in offers and
suggestions: *Shall I open the window?*).

1. **Prediction based on opinion.** *I think Nepal **will win** the match.*
2. **A decision taken at the moment of speaking.** *The bell has rung — I **will
   go** now.*
3. **Promise, offer, refusal, threat.** *I **will** help you with the project.*

### Future continuous

**Structure.** will be + V-ing — an action in progress at a stated future moment.

- *This time tomorrow we **will be travelling** to Janakpur.*
- *Do not ring at eight; she **will be teaching** then.*

### Future perfect and future perfect continuous

**Structure.** will have + V3 / will have been + V-ing. Both need a **deadline**,
usually introduced by *by*.

- *By the end of Chaitra the contractor **will have completed** the culvert.*
- *By next July I **will have been living** in Pokhara for five years.*

### Three other future forms you must recognise

| Form | Meaning | Example |
|---|---|---|
| be going to + V1 | intention already decided, or a prediction from present evidence | *Look at those clouds — it **is going to** rain.* |
| present continuous | a fixed arrangement with a time and place | *We **are meeting** the principal at four.* |
| simple present | a timetable or programme | *The Sajha bus **departs** at 6.30.* |

::: caution No *will* inside a time clause
After *when, until, before, after, as soon as, by the time, if* (condition), use
the **present**, not *will*.
~~I will call you when I will reach home.~~ → **I will call you when I reach home.**
~~We will start as soon as he will come.~~ → **We will start as soon as he comes.**
:::

## 22.5 Signal words — the fastest way to spot the tense

```figure caption="A two-step route from a blank to a tense. Ask about time first, then about aspect; the signal words on the right settle most Q7 items in a few seconds."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,3.3))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
def box(x, y, w, h, text, fc, ec, fs=7.8, tc=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                                fc=fc, ec=ec, lw=1.0))
    ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=fs,
            color=tc or INK, linespacing=1.35)
def arrow(x0,y0,x1,y1,c=MUTED):
    ax.annotate('', xy=(x1,y1), xytext=(x0,y0),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.0, mutation_scale=9))
box(2.9, 8.6, 4.2, 1.1, "Which time is meant?", "#ffffff", INK, 8.6)
box(0.1, 6.3, 2.7, 1.0, "PAST", "#eef2fb", ACCENT, 8.4, ACCENT)
box(3.6, 6.3, 2.8, 1.0, "PRESENT", "#eef2fb", ACCENT, 8.4, ACCENT)
box(7.2, 6.3, 2.7, 1.0, "FUTURE", "#eef2fb", ACCENT, 8.4, ACCENT)
arrow(4.4, 8.6, 1.4, 7.4); arrow(5.0, 8.6, 5.0, 7.4); arrow(5.6, 8.6, 8.6, 7.4)
box(1.5, 4.5, 7.0, 1.1, "Finished, in progress, or completed-before?",
    "#ffffff", INK, 8.4)
arrow(1.4, 6.2, 3.4, 5.7); arrow(5.0, 6.2, 5.0, 5.7); arrow(8.6, 6.2, 6.7, 5.7)
box(0.1, 2.5, 3.0, 1.6, "finished\n→ SIMPLE", "#f4f6f8", MUTED, 8.0)
box(3.5, 2.5, 3.0, 1.6, "in progress\n→ CONTINUOUS", "#f4f6f8", MUTED, 8.0)
box(6.9, 2.5, 3.0, 1.6, "completed before\n→ PERFECT", "#f4f6f8", MUTED, 8.0)
arrow(3.4, 4.4, 1.6, 4.2); arrow(5.0, 4.4, 5.0, 4.2); arrow(6.6, 4.4, 8.4, 4.2)
ax.text(5.0, 1.35,
        "signals:  yesterday / ago / last  →  past simple\n"
        "since / for / just / already / yet  →  present perfect\n"
        "now / at the moment / look!  →  continuous",
        ha='center', va='center', fontsize=7.6, color=INK, linespacing=1.5)
```

| Signal words | Tense they point to |
|---|---|
| always, usually, often, every day, generally, never (habit) | simple present |
| now, right now, at the moment, look!, listen!, these days | present continuous |
| just, already, yet, ever, never, so far, recently, this week | present perfect |
| since, for, how long, all day (and still going) | present perfect continuous |
| yesterday, last night, ago, in 2015, then, once | simple past |
| while, when (with a longer action), at 5 o'clock yesterday | past continuous |
| before, after, by the time, already (in the past) | past perfect |
| tomorrow, next week, soon, in future | simple future |
| this time tomorrow, at 9 p.m. tomorrow | future continuous |
| by + future time, by then, by the end of | future perfect |

## 22.6 Worked transformations

::: example Worked transformation 22.1 — fill in with the correct tense
**Problem.** *My elder sister ____ in a hospital in Dharan since 2018. (work)*

**Solution — step by step.**

1. **Read the time marker.** *since 2018* means the period starts in the past and
   runs up to now. That rules out the simple past.
2. **Time = present, reaching back.** So the tense must be a **perfect** present
   form.
3. **Is it still going on?** Yes — she still works there. With *since* plus a
   continuing state, both present perfect and present perfect continuous are used;
   with a long-term job, the **present perfect** is the standard answer.
4. **Fit the subject.** *My elder sister* is third-person singular → *has*.

**Answer.** *My elder sister **has worked** (or **has been working**) in a hospital
in Dharan since 2018.*
:::

::: example Worked transformation 22.2 — two past actions in the right order
**Problem.** Join into one sentence using the correct tenses:
*The doctor arrived. The patient died before that.*

**Solution — step by step.**

1. **List the two events and put them in real time order.** (i) the patient died —
   earlier; (ii) the doctor arrived — later.
2. **Rule:** the **earlier** past event takes the **past perfect**; the later one
   takes the **simple past**.
3. **Choose the joining word.** *before* goes after the later event, or *by the
   time* starts the later event.
4. **Write it.**

**Answer.** *The patient **had died** before the doctor **arrived**.*
(Equally: *By the time the doctor **arrived**, the patient **had died**.*)

A common wrong answer is *The patient died before the doctor had arrived*, which
reverses the order and says the arrival was earlier.
:::

::: example Worked transformation 22.3 — correcting a tense error
**Problem.** Correct: *When I reached the bus park, the bus already left, so I am
waiting there for two hours.*

**Solution — step by step.**

1. **Check clause 1.** *When I reached* — a finished past time. Simple past is
   correct. Leave it.
2. **Check clause 2.** The bus left **before** I reached; two past events, the
   earlier one needs the **past perfect**: *had already left*.
3. **Check clause 3.** *for two hours*, and the waiting happened in the past, up to
   a past point — so past perfect continuous is wrong (the waiting came *after*),
   and the present *am waiting* is wrong because the whole sentence is past. The
   waiting was a past duration: **waited** (simple past) or **had to wait**.

**Answer.** *When I reached the bus park, the bus **had** already left, so I
**waited** there for two hours.*
:::

## Chapter summary

- Tense = time; aspect = simple / continuous / perfect / perfect continuous. Three
  times × four aspects = twelve forms.
- Structures: V1(+s) · am-is-are + V-ing · have/has + V3 · have/has been + V-ing ·
  V2 · was/were + V-ing · had + V3 · had been + V-ing · will + V1 · will be +
  V-ing · will have + V3 · will have been + V-ing.
- Third-person singular takes **-s** in the simple present, and loses it after
  *does/doesn't*.
- After *did / didn't / does / doesn't*, the main verb is always **V1**.
- A finished past time word (*yesterday, ago, last year*) forces the simple past;
  *since, for, just, already, yet* force the present perfect.
- Stative verbs (*have* = own, know, like, agree, understand, see, belong) take no
  continuous form.
- Use the **present**, not *will*, after *when, until, as soon as, before, after,
  by the time* and in an *if*-clause of condition.
- Of two past actions, the earlier takes the **past perfect**.

## Practice questions

**Fill in the blanks with the correct tense of the verb in brackets (1 mark each)**

1. My father ____ to the temple every morning before breakfast. (go) <span class="marks">[1]</span>
2. Look! The children ____ in the rain. (play) <span class="marks">[1]</span>
3. We ____ each other since we were in Grade Six. (know) <span class="marks">[1]</span>
4. It ____ heavily since last night, so the road to Nagarkot is closed. (rain) <span class="marks">[1]</span>
5. The earthquake ____ Nepal on 25 April 2015. (strike) <span class="marks">[1]</span>
6. While she ____ the vegetables, the power went off. (cut) <span class="marks">[1]</span>
7. By the time we reached the hall, the programme ____ . (begin) <span class="marks">[1]</span>
8. This time next week I ____ my SEE certificate from the school. (collect) <span class="marks">[1]</span>
9. By 2030 the tunnel ____ the journey to Hetauda by two hours. (shorten) <span class="marks">[1]</span>
10. Water ____ at 100 °C at sea level. (boil) <span class="marks">[1]</span>

::: note Answers
**1.** goes — *every morning* signals a habit, and a singular subject needs -s.
**2.** are playing — *Look!* signals an action happening at this moment.
**3.** have known — *since* + a continuing state takes the present perfect (*know* is stative, so no continuous).
**4.** has been raining — *since last night* plus an activity still going on takes the present perfect continuous.
**5.** struck — a finished action at a stated past date takes the simple past.
**6.** was cutting — the longer background action interrupted by a shorter one.
**7.** had begun — the earlier of two past actions takes the past perfect.
**8.** will be collecting — *this time next week* marks an action in progress at a future moment.
**9.** will have shortened — *by 2030* is a future deadline, so future perfect.
**10.** boils — a general scientific truth takes the simple present.
:::

**Correct the errors in the following sentences (1 mark each)**

11. He is having a motorbike and a bicycle. <span class="marks">[1]</span>
12. I am agree with what the headmaster said. <span class="marks">[1]</span>
13. Did you saw the match between Nepal and Oman? <span class="marks">[1]</span>
14. She don't like milk tea in the morning. <span class="marks">[1]</span>
15. I have met my cousin yesterday at Ratna Park. <span class="marks">[1]</span>
16. I will telephone you when I will reach Nepalgunj. <span class="marks">[1]</span>
17. My brother go to the gym three times a week. <span class="marks">[1]</span>
18. They are knowing the answer but they keep quiet. <span class="marks">[1]</span>
19. The train already left when we arrived at the platform. <span class="marks">[1]</span>
20. She is living in Kathmandu since 2016. <span class="marks">[1]</span>

::: note Answers
**11.** He **has** a motorbike and a bicycle. — *have* meaning "own" is stative; no continuous form.
**12.** I **agree** with what the headmaster said. — *agree* is a verb, so it needs no *am*.
**13.** Did you **see** the match …? — after *did*, the main verb returns to V1.
**14.** She **doesn't** like milk tea … — a third-person singular subject needs *does*.
**15.** I **met** my cousin yesterday … — *yesterday* is a finished past time, so simple past.
**16.** … when I **reach** Nepalgunj. — no *will* inside a time clause.
**17.** My brother **goes** to the gym … — third-person singular -s.
**18.** They **know** the answer … — *know* is stative.
**19.** The train **had** already left when we arrived … — the earlier past action takes the past perfect.
**20.** She **has been living** (or **has lived**) in Kathmandu since 2016. — *since* + up-to-now needs a present perfect form.
:::

**Rewrite as instructed (1 mark each)**

21. *The guests left. Then we cleaned the room.* — Join with *after*, using the past perfect. <span class="marks">[1]</span>
22. *He started teaching in 2014. He still teaches.* — Rewrite as one sentence with *for*. <span class="marks">[1]</span>
23. *It is five years since I last visited Janakpur.* — Rewrite beginning *I have …* <span class="marks">[1]</span>
24. *She will finish the report before Friday.* — Rewrite using *by Friday* and the future perfect. <span class="marks">[1]</span>
25. *I am writing my assignment at the moment.* — Rewrite in the past continuous, beginning *At nine last night …* <span class="marks">[1]</span>

::: note Answers
**21.** **After the guests had left, we cleaned the room.** — the earlier action takes *had* + V3.
**22.** **He has been teaching since 2014** (or *for more than ten years*). — an activity continuing to now.
**23.** **I have not visited Janakpur for five years.** — *It is … since* converts to a present perfect with *for*.
**24.** **She will have finished the report by Friday.** — *by* + future time takes *will have* + V3.
**25.** **At nine last night I was writing my assignment.** — a past moment needs *was* + V-ing.
:::
