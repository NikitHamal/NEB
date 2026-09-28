---
subject: Compulsory English
grade: 12
unit: 25
title: Connectives and Discourse Markers
hours: 4
area: Grammar
---

A **connective** is any word or phrase that shows how one idea is related to
another — *and, but, because, although, however, therefore, in spite of*. When
the connective joins clauses inside a sentence we call it a **conjunction**; when
it opens a sentence and points back to the one before, it is a **discourse
marker** (also called a linking or transitional word). Q7 sets them as gap-fills
and as joining exercises, and the writing questions are marked partly on them. The
trick is that connectives of the same meaning need **different grammar**: *because*
takes a clause, *because of* takes a noun, and *therefore* needs a full stop or a
semicolon in front of it.

::: key Meaning is not enough — check what must follow
Before you write a connective, ask what comes after it.
**Subordinating conjunction** (*because, although, when, if*) + a **clause**:
*because the road was blocked*.
**Coordinating conjunction** (*and, but, so, or*) + a **clause**, with a comma
before it: *, so we returned*.
**Discourse marker** (*however, therefore, moreover*) — a new sentence or a
semicolon before it, a comma after: *; therefore, we returned.*
**Preposition** (*because of, in spite of, despite*) + a **noun or -ing form**:
*in spite of the rain*.
:::

## 25.1 The three grammatical types

| Type | Members | Position | Punctuation |
|---|---|---|---|
| **Coordinating conjunctions** (FANBOYS) | for, and, nor, but, or, yet, so | between two equal clauses | comma **before** the conjunction: *It rained, **but** we played.* |
| **Subordinating conjunctions** | because, since, as, although, though, even though, while, whereas, when, before, after, until, unless, if, so that, in case, as soon as, provided that, as long as | at the front of the dependent clause, which may come first or second | comma only when the dependent clause comes **first**: *Although it rained, we played.* |
| **Conjunctive adverbs / discourse markers** | however, therefore, moreover, furthermore, nevertheless, consequently, hence, thus, otherwise, meanwhile, instead, besides, in fact, for example, on the other hand, in short | at the front of a new sentence, or after a semicolon | *It rained. **However**, we played.* / *It rained; **however**, we played.* |

```figure caption="One relation, four grammars. Cause and result can be shown with a subordinator, a coordinator, a discourse marker or a preposition — and each demands its own punctuation."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.4))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
GREEN="#0B6A62"; AMBER="#B4690E"
ax.text(0.15,9.45,"THE ROAD WAS BLOCKED.  +  WE RETURNED HOME.",
        fontsize=7.6,color=INK,ha='left')
ax.plot([0.15,9.85],[8.95,8.95],color=GRID,lw=0.9)
rows=[("because","subordinator","We returned home because the road was blocked.",ACCENT,7.55),
      ("so","coordinator","The road was blocked, so we returned home.",GREEN,5.75),
      ("therefore","discourse marker","The road was blocked; therefore, we returned home.",AMBER,3.95),
      ("because of","preposition","We returned home because of the blocked road.","#7A3E9D",2.15)]
for word, kind, sent, col, y in rows:
    ax.add_patch(FancyBboxPatch((0.15,y),2.30,0.92,boxstyle="round,pad=0.08",
                                fc="#ffffff",ec=col,lw=1.0))
    ax.text(1.30,y+0.46,word,ha='center',va='center',fontsize=7.6,color=col)
    ax.text(2.70,y+0.62,kind,ha='left',va='center',fontsize=6.8,color=MUTED)
    ax.text(2.70,y+0.18,sent,ha='left',va='center',fontsize=7.2,color=INK)
ax.text(0.15,1.25,"followed by a CLAUSE:  because, so, therefore",
        fontsize=7.0,color=MUTED,ha='left')
ax.text(0.15,0.55,"followed by a NOUN or -ING form:  because of, owing to, due to",
        fontsize=7.0,color=MUTED,ha='left')
```

## 25.2 Connectives grouped by meaning

| Relation | Subordinators (+ clause) | Coordinators | Discourse markers | Prepositions (+ noun / -ing) |
|---|---|---|---|---|
| **Addition** | — | and, nor | moreover, furthermore, besides, in addition, what is more | in addition to, besides |
| **Contrast / concession** | although, though, even though, while, whereas | but, yet | however, nevertheless, nonetheless, on the other hand, on the contrary, instead | in spite of, despite, notwithstanding |
| **Cause / reason** | because, since, as, seeing that | for | — | because of, owing to, due to, on account of, thanks to |
| **Result / effect** | so … that, such … that | so | therefore, consequently, hence, thus, as a result, accordingly | — |
| **Purpose** | so that, in order that, lest | — | — | to, in order to, so as to, for |
| **Condition** | if, unless, provided (that), as long as, in case, on condition that | or (else) | otherwise | without, but for |
| **Time / sequence** | when, while, before, after, until, as soon as, no sooner … than, hardly … when | — | then, meanwhile, afterwards, later, finally, at last, first of all | during, prior to, after |
| **Example** | — | — | for example, for instance, namely, that is | such as, like |
| **Comparison** | as … as, than, just as | — | similarly, likewise, in the same way | like, unlike |
| **Emphasis** | — | — | indeed, in fact, as a matter of fact, above all | — |
| **Summary** | — | — | in short, to sum up, in conclusion, on the whole, all in all | — |

## 25.3 Paired (correlative) connectives

These come in two halves, and both halves must be present and in the right place.

| Pair | Example | Point to watch |
|---|---|---|
| both … and | *She is **both** intelligent **and** hard-working.* | plural verb |
| either … or | ***Either** Ram **or** Shyam has taken it.* | verb follows the nearer subject |
| neither … nor | ***Neither** the pen **nor** the book **is** mine.* | never use *or* after *neither* |
| not only … but also | *He **not only** sings **but also** plays the sarangi.* | the two halves must have the same grammatical shape |
| whether … or | *I do not know **whether** he will come **or** not.* | *if* cannot be used before *or not* in this pattern |
| no sooner … than | ***No sooner had** the bell rung **than** the children ran out.* | inversion after *no sooner*; *than*, never *then* |
| hardly / scarcely … when (or *before*) | ***Hardly had** I sat down **when** the phone rang.* | inversion; *when*, not *than* |
| so … that | *He was **so** tired **that** he fell asleep at once.* | *so* + adjective / adverb |
| such … that | *It was **such** a cold night **that** the pipes froze.* | *such* + (a) + adjective + noun |
| too … to | *The box is **too** heavy **to** lift.* | already negative — never add *not* |
| as … as | *Pokhara is **as** beautiful **as** Bandipur.* | base form of the adjective |
| lest … should | *Work hard **lest** you **should** fail.* | *lest* is already negative — never add *not* |

```figure caption="The concession family. All five say the same thing, but two take a full clause, two take a noun or an -ing form, and one needs a sentence break in front of it."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.4))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
GREEN="#0B6A62"; RED="#9B2C2C"
ax.text(0.15,9.45,"IT WAS RAINING.  +  WE WENT OUT.",fontsize=7.6,color=INK,ha='left')
ax.plot([0.15,9.85],[8.95,8.95],color=GRID,lw=0.9)
rows=[("Although","+ CLAUSE",  "Although it was raining, we went out.",ACCENT),
      ("but",     "+ CLAUSE",  "It was raining, but we went out.",ACCENT),
      ("However", "new sentence","It was raining. However, we went out.",GREEN),
      ("In spite of","+ NOUN", "In spite of the rain, we went out.","#7A3E9D"),
      ("Despite", "+ -ING",    "Despite being wet, we went out.","#7A3E9D")]
y=7.70
for word, need, sent, col in rows:
    ax.add_patch(FancyBboxPatch((0.15,y),2.05,0.78,boxstyle="round,pad=0.07",
                                fc="#ffffff",ec=col,lw=1.0))
    ax.text(1.175,y+0.39,word,ha='center',va='center',fontsize=7.4,color=col)
    ax.text(2.45,y+0.39,need,ha='left',va='center',fontsize=6.8,color=col)
    ax.text(4.35,y+0.39,sent,ha='left',va='center',fontsize=7.0,color=INK)
    y-=1.28
ax.plot([0.15,9.85],[2.35,2.35],color=GRID,lw=0.9)
ax.text(0.15,1.65,"✗  Although it was raining, but we went out.",
        fontsize=7.4,color=RED,ha='left')
ax.text(0.15,0.95,"✗  In spite of it was raining, we went out.",
        fontsize=7.4,color=RED,ha='left')
ax.text(0.15,0.25,"one connective only — and give it the form it asks for",
        fontsize=7.0,color=MUTED,ha='left')
```

## 25.4 Punctuation the examiner checks

1. **Comma before a coordinating conjunction** that joins two full clauses:
   *The power went off, **and** the fans stopped.* No comma when there is no
   second subject: *He opened the gate and went in.*
2. **Comma after a fronted subordinate clause**: *When the bell rang, the
   children rushed out.* No comma the other way round: *The children rushed out
   when the bell rang.*
3. **A discourse marker cannot join two clauses by itself.** Use a full stop or a
   semicolon before it and a comma after it.
   ✗ *It was late, however we continued the meeting.*
   ✓ *It was late. **However,** we continued the meeting.*
   ✓ *It was late**; however,** we continued the meeting.*
4. **Never double the connective.** English uses one, Nepali-influenced English
   often uses two.

::: caution Doubled and mismatched connectives
✗ *Although he was ill, **but** he attended the class.* → ✓ *Although he was ill,
he attended the class.* / ✓ *He was ill, **but** he attended the class.*
✗ ***Because** it was raining, **so** we stayed at home.* → ✓ *Because it was
raining, we stayed at home.* / ✓ *It was raining, **so** we stayed at home.*
✗ *Though he is rich, **yet** he is unhappy.* → ✓ *Though he is rich, he is
unhappy.* (*yet* alone is acceptable in formal writing, but never write *though …
but*)
✗ *No sooner had he left **then** it rained.* → ✓ *No sooner had he left **than**
it rained.*
✗ *Unless you **don't** work hard, you will fail.* → ✓ *Unless you work hard, you
will fail.* (*unless* already means *if not*)
✗ *Work hard lest you should **not** fail.* → ✓ *Work hard lest you should fail.*
✗ *Despite **of** the rain, the match went on.* → ✓ ***Despite** the rain* / ✓
***In spite of** the rain*.
:::

## 25.5 Choosing between look-alikes

| Pair | Difference | Example |
|---|---|---|
| **because / because of** | *because* + clause; *because of* + noun | *because **he was ill*** / *because of **his illness*** |
| **although / in spite of** | *although* + clause; *in spite of* + noun or -ing | *although **he was poor*** / *in spite of **his poverty*** |
| **beside / besides** | *beside* = next to; *besides* = in addition to | *Sit **beside** me.* / ***Besides** Nepali, he speaks Maithili.* |
| **however / but** | *however* needs a sentence break; *but* joins with a comma | *…rained. **However**, …* / *…rained, **but** …* |
| **so / such** | *so* + adjective; *such* + (a) + adjective + noun | *so cold* / *such a cold night* |
| **too / very** | *too* = more than is acceptable | *too hot to drink* / *very hot* |
| **on the other hand / on the contrary** | two sides of an issue / correcting a wrong idea | *He is strict; **on the other hand**, he is fair.* / *He is not lazy; **on the contrary**, he works all night.* |
| **while / whereas** | *while* = at the same time, or contrast; *whereas* = contrast only | *Kathmandu is crowded, **whereas** Jumla is empty.* |
| **since / for** | *since* + point of time or reason; *for* + length of time | ***Since** you are here, help me.* |

## 25.6 Joining sentences — the patterns NEB sets

| Instruction | Example pair | Joined |
|---|---|---|
| Use *although* | *He was tired. He finished the work.* | *Although he was tired, he finished the work.* |
| Use *so … that* | *The tea was very hot. I could not drink it.* | *The tea was so hot that I could not drink it.* |
| Use *too … to* | *The tea was very hot. I could not drink it.* | *The tea was too hot to drink.* |
| Use *no sooner … than* | *He reached the stop. The bus left.* | *No sooner had he reached the stop than the bus left.* |
| Use *as soon as* | same pair | *As soon as he reached the stop, the bus left.* |
| Use *so that* (purpose) | *She got up early. She wanted to catch the first bus.* | *She got up early so that she could catch the first bus.* |
| Use *unless* | *Work hard. Otherwise you will fail.* | *Unless you work hard, you will fail.* |
| Use *in spite of* | *He was ill. He attended the class.* | *In spite of his illness, he attended the class.* |

::: example Worked item 25.1 — choosing the right form of the connective
**Problem.** Fill in the blanks: *(a) The flight was cancelled ____ the bad
weather. (b) ____ the weather was bad, the flight was cancelled. (c) The weather
was bad; ____, the flight was cancelled.*

**Solution — step by step.**

1. **(a)** What follows is *the bad weather*, a **noun phrase**. A noun phrase
   needs a preposition, not a conjunction. **Answer:** *because of* (also *owing
   to / due to / on account of*).
2. **(b)** What follows is *the weather was bad*, a **clause** with its own
   subject and verb, and the gap is at the front of the sentence. That calls for a
   **subordinating conjunction**. **Answer:** *Because* (also *As / Since*).
3. **(c)** There is a **semicolon** in front of the gap and a comma after it, so
   the word must be a **discourse marker** of result. **Answer:** *therefore*
   (also *consequently / hence / as a result*).
:::

::: example Worked item 25.2 — joining with *no sooner … than*
**Problem.** Join into one sentence using *no sooner … than*: *The teacher entered
the class. The students stood up.*

**Solution — step by step.**

1. **Put the earlier event after *no sooner*.** The entering came first.
2. **Invert the auxiliary.** A sentence beginning with *no sooner* must be
   inverted: the auxiliary comes before the subject. The tense is past, and
   *no sooner* takes the **past perfect** for the earlier event: *No sooner **had
   the teacher entered*** …
3. **Join the second clause with *than*** — not *then*, and not *when*.
4. **Keep the later event in the simple past.**

**Answer.** ***No sooner had the teacher entered the class than the students stood
up.***

With *hardly / scarcely* the second half takes *when*: *Hardly had the teacher
entered the class **when** the students stood up.*
:::

::: example Worked item 25.3 — repairing doubled connectives
**Problem.** Correct: *Although he had little money, but he helped the flood
victims, because of he is generous, and despite of his own losses.*

**Solution — one fault at a time.**

1. *Although … but* doubles the connective. Keep *although* and delete *but*.
2. *because of he is generous* — *he is generous* is a clause, so the preposition
   *because of* must become the conjunction *because*.
3. *despite of* — *despite* never takes *of*.
4. *his own losses* is a noun phrase, which *despite* correctly governs, so only
   the *of* is removed.

**Answer.** *Although he had little money, he helped the flood victims, **because**
he is generous, **despite** his own losses.*
:::

## Chapter summary

- Connectives fall into four grammatical types, each with its own requirement:
  subordinator + clause, coordinator + clause (comma before), discourse marker +
  new sentence or semicolon, preposition + noun or -ing.
- FANBOYS = *for, and, nor, but, or, yet, so* — the seven coordinating
  conjunctions.
- A fronted subordinate clause takes a comma; the same clause at the end does not.
- *However, therefore, moreover, nevertheless, consequently* cannot join two
  clauses with a comma — that is a comma splice.
- Never double a connective: *although … but*, *because … so*, *though … yet* are
  all wrong.
- *No sooner … than* (with inversion), *hardly / scarcely … when*, *so … that*,
  *such a … that*, *too … to*, *lest … should*.
- *Unless* already means *if not*; *lest* and *too … to* are already negative — do
  not add another *not*.
- *Despite* takes no *of*; *in spite of* does.
- *Because / although / while* take clauses; *because of / in spite of / despite*
  take nouns or -ing forms.
- *Beside* = next to; *besides* = in addition to.

## Practice questions

**Fill in the blanks with a suitable connective (1 mark each)**

1. ____ he worked hard, he could not pass the examination. <span class="marks">[1]</span>
2. The match was postponed ____ the heavy rain. <span class="marks">[1]</span>
3. She is very busy today; ____, she has agreed to meet us. <span class="marks">[1]</span>
4. Hurry up, ____ you will miss the last bus. <span class="marks">[1]</span>
5. ____ had the programme started ____ the power went off. <span class="marks">[1]</span>
6. He saved money ____ he could buy a laptop. <span class="marks">[1]</span>
7. ____ Nepali, she can speak Maithili and Hindi fluently. <span class="marks">[1]</span>
8. The soup was ____ salty that nobody could eat it. <span class="marks">[1]</span>
9. Kathmandu is crowded, ____ Jumla is almost empty. <span class="marks">[1]</span>
10. ____ you apologise, he will not talk to you. <span class="marks">[1]</span>

::: note Answers
**1.** Although (or Though / Even though) — a clause of concession follows.
**2.** because of (or owing to / due to) — a noun phrase follows, so a preposition is needed.
**3.** however (or nevertheless) — a discourse marker after a semicolon.
**4.** or (or *otherwise*) — a warning about the alternative result.
**5.** No sooner … than — the fixed pair, with inversion after *no sooner*.
**6.** so that — purpose, followed by *could*.
**7.** Besides (or In addition to) — "in addition to Nepali".
**8.** so — *so* + adjective + *that*.
**9.** whereas (or while) — direct contrast between two places.
**10.** Unless — *unless* means "if … not", so no extra negative is used.
:::

**Correct the errors in the following sentences (1 mark each)**

11. Although he was ill, but he came to college. <span class="marks">[1]</span>
12. Because the shop was closed, so we returned empty-handed. <span class="marks">[1]</span>
13. Despite of his age, he walks five kilometres every day. <span class="marks">[1]</span>
14. No sooner had the bell rung then the students rushed out. <span class="marks">[1]</span>
15. Unless you don't hurry, you will be late. <span class="marks">[1]</span>
16. He ran fast lest he should not miss the train. <span class="marks">[1]</span>
17. It was raining heavily, however the programme continued. <span class="marks">[1]</span>
18. She was too tired that she could not walk further. <span class="marks">[1]</span>
19. Beside tea, they also served biscuits. <span class="marks">[1]</span>
20. He failed because of he did not revise the lessons. <span class="marks">[1]</span>

::: note Answers
**11.** **Although he was ill, he came to college.** — one connective only.
**12.** **Because the shop was closed, we returned empty-handed.** — delete *so*.
**13.** **Despite his age**, he walks five kilometres every day. — *despite* takes no *of*.
**14.** No sooner had the bell rung **than** the students rushed out. — the pair is *no sooner … than*.
**15.** **Unless you hurry**, you will be late. — *unless* already contains the negative.
**16.** He ran fast **lest he should miss** the train. — *lest* is already negative.
**17.** It was raining heavily**; however,** the programme continued. — a discourse marker needs a semicolon or a full stop.
**18.** She was **so tired that** she could not walk further. (or *too tired to walk further*) — *too* pairs with *to*, not *that*.
**19.** **Besides** tea, they also served biscuits. — *besides* means "in addition to".
**20.** He failed **because he did not revise** the lessons. — a clause needs *because*, not *because of*.
:::

**Join the following pairs as instructed (1 mark each)**

21. *He was very weak. He could not stand.* — Use *so … that*. <span class="marks">[1]</span>
22. *He was very weak. He could not stand.* — Use *too … to*. <span class="marks">[1]</span>
23. *She switched on the fan. The room was hot.* — Use *because*. <span class="marks">[1]</span>
24. *He started early. He wanted to avoid the traffic.* — Use *so that*. <span class="marks">[1]</span>
25. *I reached the counter. The last ticket was sold.* — Use *hardly … when*. <span class="marks">[1]</span>
26. *It was a very interesting film. We watched it twice.* — Use *such … that*. <span class="marks">[1]</span>

::: note Answers
**21.** **He was so weak that he could not stand.** — *so* + adjective + *that* + clause.
**22.** **He was too weak to stand.** — *too … to* carries the negative sense by itself.
**23.** **She switched on the fan because the room was hot.** — reason clause after the main clause, so no comma.
**24.** **He started early so that he could avoid the traffic.** — purpose clause with *could*.
**25.** **Hardly had I reached the counter when the last ticket was sold.** — inversion, past perfect, then *when*.
**26.** **It was such an interesting film that we watched it twice.** — *such* + *a/an* + adjective + noun + *that*.
:::
