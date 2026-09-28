---
subject: Compulsory English
grade: 12
unit: 30
title: Prepositions, Tenses and Relative Clauses
hours: 4
area: Grammar
---

This last grammar unit gathers the three areas that appear most often in Q7 and do
most damage in Q10. **Prepositions** are small, fixed and unforgiving: nothing in
logic explains why we are *good **at** English*, *married **to*** someone and
*angry **with*** them. **Tenses** are the backbone of every sentence you write,
and the errors here are errors of *sequence* rather than of form. **Relative
clauses** let you join two short sentences into one adult sentence — and a single
misplaced comma changes what the sentence means. Take the three in turn.

::: key Three rules that settle most questions
1. **Prepositions of time and place narrow down**: *in* for the largest area,
   *on* for a surface or a named day, *at* for a single point.
2. **A past main verb pulls its subordinate clause into the past** — except for
   universal truths.
3. **Commas decide the meaning of a relative clause.** No commas = the clause
   identifies which one (defining). Commas = the clause merely adds information
   (non-defining), and *that* is then forbidden.
:::

## 30.1 Prepositions of time and place

```figure caption="In, on, at. The same three prepositions serve time and place, and in both they run from the largest container down to a single point."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,4.4))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
GREEN="#0B6A62"; AMBER="#B4690E"
rows=[("IN  —  the largest container",ACCENT,
       "TIME    months, years, seasons, centuries, the morning",
       "PLACE   countries, cities, rooms, enclosed spaces"),
      ("ON  —  a surface or a named day",GREEN,
       "TIME    days, dates, a particular morning",
       "PLACE   surfaces, streets, floors, the bus"),
      ("AT  —  a single point",AMBER,
       "TIME    clock times, night, noon, festivals",
       "PLACE   exact spots, addresses, events")]
y=6.95
for title,col,t,p in rows:
    ax.add_patch(FancyBboxPatch((0.75,y),9.05,2.20,boxstyle="round,pad=0.07",
                                fc="#ffffff",ec=col,lw=1.0))
    ax.text(1.05,y+1.68,title,fontsize=7.2,color=col,ha='left',va='center')
    ax.text(1.05,y+1.02,t,fontsize=6.7,color=INK,ha='left',va='center')
    ax.text(1.05,y+0.38,p,fontsize=6.7,color=MUTED,ha='left',va='center')
    y-=2.70
ax.annotate("",xy=(0.32,1.45),xytext=(0.32,9.10),
            arrowprops=dict(arrowstyle="-|>",color=MUTED,lw=1.0))
ax.text(0.15,0.75,"in Nepal → on Durbar Marg → at the Ghantaghar",
        fontsize=6.9,color=INK,ha='left')
ax.text(0.15,0.15,"in June → on 15 June → at 7 o'clock",
        fontsize=6.9,color=INK,ha='left')
```

| Preposition | Time | Place |
|---|---|---|
| **in** | *in May, in 2026, in winter, in the 19th century, in the morning, in two hours* (= after two hours from now) | *in Nepal, in the box, in bed, in the sky* |
| **on** | *on Sunday, on 5 June, on Monday morning, on my birthday* | *on the table, on the wall, on the second floor, on the bus* |
| **at** | *at 6 o'clock, at night, at noon, at Dashain, at present* | *at the bus stop, at the door, at school, at 25 Durbar Marg* |

**Pairs that are regularly confused.**

| Pair | Difference |
|---|---|
| **since / for** | *since* + a point of time (*since 2019*); *for* + a length (*for three years*) |
| **during / for** | *during* + a noun (*during the holidays*); *for* + a period (*for a week*) |
| **by / until** | *by* = not later than (*Finish it by Friday*); *until* = up to that moment (*Wait until Friday*) |
| **in time / on time** | *in time* = early enough; *on time* = punctually |
| **between / among** | *between* two; *among* more than two |
| **beside / besides** | *beside* = next to; *besides* = in addition to |
| **across / through** | *across* a surface; *through* something you go inside |
| **in front of / opposite** | *in front of* = ahead of; *opposite* = facing |

## 30.2 Fixed prepositions, and verbs that take none

| Adjective + preposition | | Verb + preposition | |
|---|---|---|---|
| good **at**, bad **at** | afraid **of** | depend **on**, rely **on** | consist **of** |
| married **to** | angry **with** (a person) | apologise **to** … **for** | belong **to** |
| interested **in** | angry **at** (a thing) | congratulate **on** | complain **about** |
| famous **for** | proud **of** | accuse **of**, suspect **of** | insist **on** |
| different **from** | capable **of** | prevent **from**, prohibit **from** | succeed **in** |
| similar **to**, superior **to** | aware **of** | blame **for** | object **to** |
| responsible **for** | fond **of** | remind **of** | refer **to** |
| tired **of**, sure **of** | absent **from** | deal **with**, cope **with** | translate **into** |
| grateful **to** (person) **for** (thing) | keen **on** | provide somebody **with** | divide **into** |

**Verbs that need no preposition at all.** These are the ones Nepali speakers add
a preposition to, and every one of them is marked wrong.

| ✗ Wrong | ✓ Correct |
|---|---|
| *discuss **about** the problem* | *discuss the problem* |
| *enter **into** the hall* | *enter the hall* (but *enter into an agreement* is correct) |
| *marry **with** her* | *marry her* / *be married **to** her* |
| *reach **at** the station* | *reach the station* (but *arrive **at** the station*) |
| *return **back** home* | *return home* |
| *repeat **again*** | *repeat* |
| *cope **up** with the pressure* | *cope **with** the pressure* |
| *emphasise **on** the point* | *emphasise the point* / *lay emphasis **on** it* |
| *investigate **into** the case* | *investigate the case* |
| *resemble **to** his father* | *resemble his father* |
| *describe **about** the scene* | *describe the scene* |
| *obey **to** the rules* | *obey the rules* |
| *order **for** a coffee* | *order a coffee* |
| *comprise **of** five members* | *comprise five members* / *consist **of** five members* |

::: caution The preposition errors that cost most marks
✗ *She is good **in** Mathematics.* → ✓ *good **at** Mathematics*
✗ *He is married **with** a teacher.* → ✓ *married **to** a teacher*
✗ *This book is different **than** that one.* → ✓ *different **from** that one*
✗ *I am waiting **your** reply.* → ✓ *waiting **for** your reply*
✗ *He **replied** my letter.* → ✓ *He **replied to** my letter.*
✗ *She **listened** the news.* → ✓ *She **listened to** the news.*
:::

## 30.3 The twelve tenses at a glance

| Tense | Form | Typical signal words |
|---|---|---|
| Simple present | V1 / V1+s | *always, usually, every day, generally* |
| Present continuous | am / is / are + V-ing | *now, at present, at the moment, look!* |
| Present perfect | has / have + V3 | *just, already, yet, ever, never, so far, recently* |
| Present perfect continuous | has / have been + V-ing | *for, since, all day, how long* |
| Simple past | V2 | *yesterday, last week, in 2018, ago* |
| Past continuous | was / were + V-ing | *while, at 5 p.m. yesterday, when … came* |
| Past perfect | had + V3 | *before, after, by the time, already (in the past)* |
| Past perfect continuous | had been + V-ing | *for / since + a past point* |
| Simple future | will / shall + V1 | *tomorrow, next week, soon* |
| Future continuous | will be + V-ing | *at this time tomorrow* |
| Future perfect | will have + V3 | *by next year, by the time* |
| Future perfect continuous | will have been + V-ing | *for + a period, by next month* |

**Sequence of tenses.** When the main verb is in the **past**, the verb in the
subordinate clause is normally past as well.

*He **said** that he **was** unwell.* · *She **asked** what I **wanted**.* · *They
**left** before the guests **arrived**.*

Three exceptions: a **universal truth** stays in the present (*He said that honesty
**is** the best policy*); a **comparison** after *than* may keep its own tense
(*He worked harder than I **do***); and a **habitual present fact** may be kept
(*She told me that she **goes** to the gym every morning*).

::: caution Tense errors in exam scripts
✗ *I **am knowing** the answer.* → ✓ *I **know** the answer.* (stative verbs —
*know, believe, like, want, see, own* — are not used in the continuous)
✗ *He **has gone** to Pokhara last week.* → ✓ *He **went** to Pokhara last week.*
(the present perfect never takes a finished past time)
✗ *I **am working** here since 2020.* → ✓ *I **have been working** here since
2020.*
✗ *When I **reached** the station, the train **left**.* → ✓ *…the train **had
left**.* (the earlier of two past events takes the past perfect)
✗ *If he **will come**, I will meet him.* → ✓ *If he **comes**…*
:::

## 30.4 Relative clauses

A **relative clause** describes a noun and begins with a relative pronoun.

| Pronoun | Used for | Example |
|---|---|---|
| **who** | a person, as subject | *the girl **who** won the prize* |
| **whom** | a person, as object (formal) | *the man **whom** we met* |
| **whose** | possession (people or things) | *the boy **whose** bag was lost* |
| **which** | a thing or animal | *the house **which** stands on the hill* |
| **that** | person or thing, **defining clauses only** | *the bus **that** goes to Bhaktapur* |
| **where** | a place | *the village **where** I was born* |
| **when** | a time | *the day **when** we met* |
| **why** | a reason | *the reason **why** he left* |

```figure caption="Defining or non-defining. The commas are not decoration: they change which students the sentence is talking about, and they decide whether that is allowed."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,4.4))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
GREEN="#0B6A62"; PURPLE="#7A3E9D"
cols=[(0.15,GREEN,"DEFINING","no commas",
       ["The students who had","registered were allowed in.",
        "→ only the registered ones",
        "· that may replace who/which",
        "· object pronoun may be dropped",
        "· never separated by commas"]),
      (5.15,PURPLE,"NON-DEFINING","commas on both sides",
       ["The students, who had","registered, were allowed in.",
        "→ all of them; extra detail",
        "· that is never allowed",
        "· pronoun can never be dropped",
        "· used after proper nouns"])]
for x,col,head,sub,lines in cols:
    ax.add_patch(FancyBboxPatch((x,1.35),4.70,8.10,boxstyle="round,pad=0.07",
                                fc="#ffffff",ec=col,lw=1.0))
    ax.text(x+2.35,8.90,head,ha='center',va='center',fontsize=7.4,color=col)
    ax.text(x+2.35,8.25,sub,ha='center',va='center',fontsize=6.5,color=MUTED)
    ys=[7.60,7.05,5.90,4.75,3.80,2.85]
    for i,(ln,y) in enumerate(zip(lines,ys)):
        c=INK if i<2 else (col if i==2 else MUTED)
        ax.text(x+0.25,y,ln,ha='left',va='center',fontsize=6.6,color=c)
ax.text(0.15,0.70,"Ask: does the clause tell me WHICH one?  Yes → no commas.",
        fontsize=6.9,color=INK,ha='left')
ax.text(0.15,0.15,"No, it only adds information → commas, and never that.",
        fontsize=6.9,color=INK,ha='left')
```

### Defining clauses

A defining clause says **which one** is meant. Without it the sentence is
incomplete in sense, so it takes **no commas**.

*The man **who lives next door** is a doctor.*
*This is the book **that I told you about**.*
*The house **which we bought** needs repair.*

In a defining clause the relative pronoun may be **dropped when it is the object**
of its clause:
*This is the book **(that) I told you about**.*
*The man **(whom) we met** was her uncle.*
It can **never** be dropped when it is the subject:
✗ *The man lives next door is a doctor.* → ✓ *The man **who** lives next door…*

**That** is preferred after superlatives and after *all, any, only, everything,
nothing, the first, the last*:
*This is the best film **that** I have ever seen.*

### Non-defining clauses

A non-defining clause gives **extra information** about a noun that is already
identified. It is enclosed in commas, and **that** cannot be used.

*My uncle, **who lives in Biratnagar**, is visiting us.*
*Mount Everest, **which stands at 8,849 metres**, is the world's highest peak.*
*She passed the examination, **which delighted her parents**.* (here *which*
refers to the whole preceding idea)

### Prepositions, and reduced clauses

A preposition may stand before *whom* or *which* (formal) or at the end of the
clause (normal):
*the officer **to whom** I spoke* = *the officer **whom** I spoke **to*** = *the
officer I spoke **to***
✗ *the officer **to that** I spoke* — *that* never follows a preposition.

A relative clause can often be shortened to a participle:
*the boy **who is standing** at the gate* → *the boy **standing** at the gate*
*the letter **which was written** by him* → *the letter **written** by him*

::: caution Relative-clause errors
✗ *The boy **who he** came yesterday is my cousin.* → ✓ *The boy **who** came
yesterday…* (the pronoun *is* the subject; do not repeat it)
✗ *This is the pen **which I bought it** yesterday.* → ✓ *…**which I bought**
yesterday.*
✗ *My father, **that** is a teacher, retired last year.* → ✓ *My father, **who** is
a teacher, …*
✗ *The house **where** I bought is small.* → ✓ *The house **which / that** I bought
is small.* (*where* is not used when the noun is the **object** of the verb)
✗ *Kathmandu**,** which is the capital**,** …* written without commas — a proper
noun is already identified, so the clause must be non-defining.
:::

::: example Worked item 30.1 — choosing prepositions
**Problem.** Fill in the blanks: *We reached ____ the airport ____ 6 o'clock ____
the morning ____ 5 June, and waited ____ two hours ____ our flight.*

**Solution — one gap at a time.**

1. ***reach*** takes **no preposition**. The gap is filled by nothing — or the
   sentence is rewritten with *arrived **at***. (Examiners set this deliberately;
   if a blank is given, the intended verb is *arrived*.)
2. ***6 o'clock*** is a single point of time → **at**.
3. ***the morning*** is a part of the day → **in**.
4. ***5 June*** is a date → **on**.
5. ***two hours*** is a length of time → **for**.
6. ***wait*** always takes **for** before its object.

**Answer.** *We **arrived at** the airport **at** 6 o'clock **in** the morning
**on** 5 June, and waited **for** two hours **for** our flight.*
:::

::: example Worked item 30.2 — sequence of tenses
**Problem.** Put the verbs into the correct tense: *When I (reach) the hall, the
chief guest already (deliver) his speech, and the audience (clap).*

**Solution — order the events.**

1. **Establish the main time.** The sentence is about the past, so the *when*
   clause takes the **simple past**: *reached*.
2. **Find the earlier event.** The speech was finished *before* I reached — the
   earlier of two past actions takes the **past perfect**: *had already
   delivered*.
3. **Find the action in progress.** The clapping was going on at the moment I
   arrived, so it takes the **past continuous**: *was clapping*.

**Answer.** *When I **reached** the hall, the chief guest **had already
delivered** his speech, and the audience **was clapping**.*
:::

::: example Worked item 30.3 — joining with a relative pronoun
**Problem.** Join each pair with a relative pronoun. *(a) This is the girl. Her
painting won the prize. (b) I met a doctor yesterday. He treated my grandfather.
(c) Pokhara attracts many tourists. It lies beside a lake.*

**Solution — decide the pronoun, then the commas.**

1. **(a)** The link is possession (*her painting*), so the pronoun is **whose**.
   The clause identifies which girl, so it is defining — no commas.
   → ***This is the girl whose painting won the prize.***
2. **(b)** *He* is the subject of the second sentence and refers to a person →
   **who**. *A doctor* is not yet identified, so the clause is defining.
   → ***I met a doctor yesterday who treated my grandfather.*** (better: *The
   doctor whom I met yesterday treated my grandfather.*)
3. **(c)** *Pokhara* is a proper noun, already fully identified, so the clause can
   only be **non-defining**: commas, *which*, and never *that*.
   → ***Pokhara, which lies beside a lake, attracts many tourists.***
:::

## Chapter summary

- *in* → the largest container, *on* → a surface or a named day, *at* → a single
  point, for both time and place.
- *since* + point, *for* + period; *by* = not later than, *until* = up to then;
  *between* two, *among* many.
- Learn adjective + preposition pairs as units: *good at, married to, different
  from, interested in, afraid of, angry with*.
- *Discuss, enter, reach, marry, resemble, obey, describe, emphasise, investigate,
  comprise* take **no** preposition; *return back*, *repeat again* and *cope up
  with* are all wrong.
- A past main verb pulls its subordinate clause into the past, except for
  universal truths.
- The present perfect never takes a finished past time; the earlier of two past
  events takes the past perfect; stative verbs have no continuous form.
- Defining relative clause: no commas, *that* allowed, object pronoun may be
  dropped.
- Non-defining relative clause: commas, *that* forbidden, pronoun never dropped —
  and always non-defining after a proper noun.
- *That* never follows a preposition; use *to whom / in which*, or move the
  preposition to the end.
- A relative clause can be reduced to a participle: *the boy standing there*, *the
  letter written by him*.

## Practice questions

**Fill in the blanks with the correct preposition, or leave it blank where none is needed (1 mark each)**

1. She is very good ____ solving puzzles. <span class="marks">[1]</span>
2. My sister was married ____ an engineer last year. <span class="marks">[1]</span>
3. We discussed ____ the matter for nearly an hour. <span class="marks">[1]</span>
4. The meeting will begin ____ ten o'clock ____ Monday. <span class="marks">[1]</span>
5. He has been living in Butwal ____ 2015. <span class="marks">[1]</span>
6. Please reply ____ my letter as soon as possible. <span class="marks">[1]</span>
7. The committee consists ____ seven members. <span class="marks">[1]</span>
8. She is quite different ____ her twin sister. <span class="marks">[1]</span>
9. They reached ____ the village before sunset. <span class="marks">[1]</span>
10. The guests will arrive ____ the hotel ____ the evening. <span class="marks">[1]</span>

::: note Answers
**1.** at — *good at* + noun or *-ing*.
**2.** to — *married to*, never *with*.
**3.** (no preposition) — *discuss* is transitive; *discuss about* is wrong.
**4.** at … on — a clock time takes *at*, a named day takes *on*.
**5.** since — 2015 is a point of time.
**6.** to — *reply to* someone or something.
**7.** of — *consist of*.
**8.** from — *different from*.
**9.** (no preposition) — *reach the village*; *arrive at the village* would need *at*.
**10.** at … in — *arrive at* a building, *in the evening*.
:::

**Put the verbs in brackets into the correct tense (1 mark each)**

11. He (work) in this office since 2019. <span class="marks">[1]</span>
12. When we reached the theatre, the film already (start). <span class="marks">[1]</span>
13. Look! The children (play) in the rain. <span class="marks">[1]</span>
14. The teacher told us that the sun (rise) in the east. <span class="marks">[1]</span>
15. I (not see) him since last Dashain. <span class="marks">[1]</span>
16. By next June we (complete) our course. <span class="marks">[1]</span>
17. She (know) the answer, but she refused to say it. <span class="marks">[1]</span>

::: note Answers
**11.** has been working — *since* + a point of time with an action continuing to now.
**12.** had already started — the earlier of two past events.
**13.** are playing — *Look!* signals something happening now.
**14.** rises — a universal truth does not shift after a past reporting verb.
**15.** have not seen — present perfect with *since*.
**16.** will have completed — future perfect with *by next June*.
**17.** knew — *know* is stative, so *was knowing* is impossible.
:::

**Join or rewrite as instructed (1 mark each)**

18. *That is the boy. His father is a pilot.* — Join with a relative pronoun. <span class="marks">[1]</span>
19. *Lumbini is visited by thousands of pilgrims. It is the birthplace of the Buddha.* — Join with a non-defining clause. <span class="marks">[1]</span>
20. *The pen is missing. I bought it yesterday.* — Join with a defining clause. <span class="marks">[1]</span>
21. *The girl who is sitting near the window is my cousin.* — Reduce the relative clause. <span class="marks">[1]</span>
22. *This is the officer. I complained to him.* — Join, beginning *This is the officer to …* <span class="marks">[1]</span>

::: note Answers
**18.** **That is the boy whose father is a pilot.** — possession takes *whose*.
**19.** **Lumbini, which is the birthplace of the Buddha, is visited by thousands of pilgrims.** — a proper noun requires commas and *which*.
**20.** **The pen (that) I bought yesterday is missing.** — the pronoun is the object, so it may be dropped.
**21.** **The girl sitting near the window is my cousin.** — *who is* is deleted and the *-ing* form remains.
**22.** **This is the officer to whom I complained.** — a preposition may precede *whom* but never *that*.
:::
