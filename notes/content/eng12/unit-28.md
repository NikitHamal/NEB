---
subject: Compulsory English
grade: 12
unit: 28
title: Conditional Sentences
hours: 4
area: Grammar
---

A **conditional sentence** has two parts: an **if-clause**, which states the
condition, and a **main clause**, which states the result. *If it rains, the match
will be cancelled.* The whole of the grammar lies in one question — **how real is
the condition?** English answers that question by choosing a tense, and the tense
it chooses is often *not* the tense of the time being talked about: a sentence
about the future can use the present, and a sentence about the present can use the
past. That is why conditionals are worth learning as four fixed patterns rather
than reasoning them out each time.

::: key The four patterns
| Type | If-clause | Main clause |
|---|---|---|
| **0** general truth | if + present simple | present simple |
| **1** real / likely | if + present simple | will / can / may / must + base verb |
| **2** unreal present or future | if + past simple (*were* for all persons) | would / could / might + base verb |
| **3** impossible past | if + past perfect | would / could / might + **have** + past participle |

Two rules hold for all four: **never use *will* or *would* in the if-clause**, and
the if-clause takes a comma only when it comes **first**.
:::

## 28.1 The four types in detail

```figure caption="The reality scale. Reading downwards, each type moves one step further from fact — and the verb in the if-clause moves one step further back in time to signal it."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,4.5))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
GREEN="#0B6A62"; AMBER="#B4690E"; PURPLE="#7A3E9D"
ax.text(0.70,9.62,"REAL",fontsize=6.6,color=GREEN,ha='left')
ax.text(9.85,9.62,"read downwards",fontsize=6.4,color=MUTED,ha='right')
boxes=[("TYPE 0  ·  always true",GREEN,
        "if + present simple,  present simple",
        "If you heat ice, it melts."),
       ("TYPE 1  ·  likely to happen",ACCENT,
        "if + present simple,  will + base verb",
        "If it rains, we will stay at home."),
       ("TYPE 2  ·  untrue now, or unlikely",AMBER,
        "if + past simple,  would + base verb",
        "If I had wings, I would fly to Jumla."),
       ("TYPE 3  ·  impossible — it is over",PURPLE,
        "if + past perfect,  would have + V3",
        "If I had left early, I would have caught the bus.")]
y=7.55
for title,col,form,ex in boxes:
    ax.add_patch(FancyBboxPatch((0.70,y),9.10,1.78,boxstyle="round,pad=0.07",
                                fc="#ffffff",ec=col,lw=1.0))
    ax.text(0.95,y+1.38,title,fontsize=7.0,color=col,ha='left',va='center')
    ax.text(0.95,y+0.85,form,fontsize=6.8,color=INK,ha='left',va='center')
    ax.text(0.95,y+0.33,ex,fontsize=6.8,color=MUTED,ha='left',va='center')
    y-=2.05
ax.annotate("",xy=(0.30,0.95),xytext=(0.30,9.45),
            arrowprops=dict(arrowstyle="-|>",color=MUTED,lw=1.0))
ax.text(0.70,0.30,"UNREAL",fontsize=6.6,color=PURPLE,ha='left')
ax.text(9.85,0.30,"never will or would after if",fontsize=6.4,color=MUTED,ha='right')
```

**Type 0** — a fact that is always true. Here *if* can be replaced by *when* or
*whenever*.
*If you mix blue and yellow, you **get** green.*
*If the temperature **falls** below zero, water **freezes**.*

**Type 1** — a real possibility in the present or future.
*If you **work** hard, you **will pass**.*
*If she **calls**, **tell** her I am out.* (imperative in the main clause)
*If you **have finished** the paper, you **may leave**.* (present perfect in the
if-clause is allowed)
*If he **misses** the bus, he **can take** a taxi.*

**Type 2** — the condition is untrue now, or very unlikely. The past tense here
has **no past meaning**; it is a signal of unreality. With *be*, formal English
uses **were** for every person.
*If I **knew** his number, I **would ring** him.* (I do not know it)
*If I **were** you, I **would apologise**.* (the fixed advice formula)
*If we **had** more time, we **could visit** Lumbini.*

**Type 3** — the condition was not fulfilled, and the time is finished. Nothing
can change it now.
*If she **had revised**, she **would have scored** better.* (she did not revise)
*If the driver **had been** careful, the accident **would not have happened**.*
*If I **had known** you were ill, I **would have visited** you.*

## 28.2 Mixed conditionals

Real life does not always keep the two clauses in the same time. A **mixed
conditional** takes the if-clause from one type and the main clause from another.

```figure caption="Mixed conditionals. Take the if-clause from one type and the main clause from another when the condition and the result belong to different times."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.5))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
AMBER="#B4690E"; PURPLE="#7A3E9D"
ax.text(2.55,9.45,"IF-CLAUSE",fontsize=6.5,color=MUTED,ha='center')
ax.text(7.55,9.45,"MAIN CLAUSE",fontsize=6.5,color=MUTED,ha='center')
def pair(y,l1,l2,c1,r1,r2,c2,note):
    ax.add_patch(FancyBboxPatch((0.15,y),4.80,1.40,boxstyle="round,pad=0.07",
                                fc="#ffffff",ec=c1,lw=1.0))
    ax.text(2.55,y+0.95,l1,fontsize=6.6,color=c1,ha='center',va='center')
    ax.text(2.55,y+0.42,l2,fontsize=6.9,color=INK,ha='center',va='center')
    ax.add_patch(FancyBboxPatch((5.20,y),4.65,1.40,boxstyle="round,pad=0.07",
                                fc="#ffffff",ec=c2,lw=1.0))
    ax.text(7.55,y+0.95,r1,fontsize=6.6,color=c2,ha='center',va='center')
    ax.text(7.55,y+0.42,r2,fontsize=6.9,color=INK,ha='center',va='center')
    ax.text(0.15,y-0.60,note,fontsize=6.7,color=MUTED,ha='left')
pair(7.05,"past condition (type 3)","If I had taken the job,",PURPLE,
     "present result (type 2)","I would be rich today.",AMBER,
     "a past action that still shapes the present")
pair(3.35,"present condition (type 2)","If he were careful,",AMBER,
     "past result (type 3)","he would not have fallen.",PURPLE,
     "a permanent state that explains a past event")
ax.plot([0.15,9.85],[2.05,2.05],color=GRID,lw=0.9)
ax.text(0.15,1.45,"had + V3  →  the condition is in the PAST",
        fontsize=6.9,color=PURPLE,ha='left')
ax.text(0.15,0.80,"would + V3  →  the result is in the PAST",
        fontsize=6.9,color=PURPLE,ha='left')
ax.text(0.15,0.15,"would + base verb  →  the result is NOW",
        fontsize=6.9,color=AMBER,ha='left')
```

| Mix | Example | Meaning |
|---|---|---|
| Type 3 if-clause + Type 2 main clause | *If I **had studied** medicine, I **would be** a doctor now.* | past cause, present result |
| Type 2 if-clause + Type 3 main clause | *If he **were** honest, he **would not have cheated** in the test.* | present state, past result |

## 28.3 Conditionals without *if*

**Inversion.** In formal English the *if* can be dropped and the auxiliary moved
in front of the subject. This is available in three patterns only.

| With *if* | Inverted |
|---|---|
| *If I **were** you…* | ***Were I** you…* |
| *If he **had** told me…* | ***Had he** told me…* |
| *If you **should** need help…* | ***Should you** need help…* |

✗ *If had I known…* — once *if* is removed, it must not come back.

**Other conditional connectives.**

| Connective | Meaning | Example |
|---|---|---|
| unless | if … not | *You will fail **unless** you work hard.* |
| provided (that) / providing | on the single condition that | *I will lend it **provided that** you return it by Friday.* |
| as long as / so long as | on condition that | *You may stay **as long as** you keep quiet.* |
| on condition that | formal condition | *He was released **on condition that** he reported weekly.* |
| in case | as a precaution (**not** the same as *if*) | *Take an umbrella **in case** it rains.* |
| even if | the result holds anyway | *I will go **even if** it rains.* |
| suppose / supposing | imagine that | ***Supposing** you lost your passport, what would you do?* |
| but for | if it had not been for | ***But for** your help, I would have failed.* |
| otherwise / or else | if that does not happen | *Hurry up, **otherwise** you will be late.* |
| whether … or not | both conditions | *I shall go **whether** it rains **or not**.* |

## 28.4 Four places where *will*, *would* and *should* may follow *if*

The rule "no *will* after *if*" applies to **conditions**. There are four
recognised exceptions, and knowing them stops you from over-correcting.

| Case | Meaning of the auxiliary | Example |
|---|---|---|
| Willingness | *will / would* = "be kind enough to" | *If you **will** wait here, I **will** call the manager.* · *If you **would** sign here, please.* |
| Insistence | stressed *will* = "insist on doing" | *If you **will** eat so much sugar, you must expect toothache.* |
| Remote possibility | *should* = "by any chance" | *If you **should** meet him, give him my regards.* · *If I **were to** fail, I would try again.* |
| Not a condition at all | *if* = *whether*, after *ask, wonder, know, see* | *I wonder **if** he **will** come.* · *Ask her **if** she **will** join us.* |

In every other case the if-clause of a type 1 sentence takes the **present
simple**, however clearly it refers to the future.

::: caution The six conditional errors examiners look for
✗ *If it **will** rain, we will stay at home.* → ✓ *If it **rains**, we will stay
at home.* (no *will* in the if-clause)
✗ *If I **would have** known, I would have come.* → ✓ *If I **had** known…*
✗ *If I **was** you, I would accept.* → ✓ *If I **were** you…*
✗ *Unless you **don't** hurry, you will miss it.* → ✓ *Unless you **hurry**…*
(*unless* already contains the negative)
✗ *Take a coat in case it **will** be cold.* → ✓ *…in case it **is** cold.*
✗ *If he **would be** here, he would help us.* → ✓ *If he **were** here…*
:::

## 28.5 *Wish*, *if only* and other unreal patterns

*Wish* and *if only* behave like a type 2 or type 3 if-clause: the tense goes one
step back to show that the thing is not so.

| Pattern | Meaning | Example |
|---|---|---|
| wish + past simple | regret about **now** | *I **wish** I **knew** the answer.* (I don't) |
| wish + *were* | regret about a present state | *I **wish** I **were** taller.* |
| wish + could | regret about present ability | *I **wish** I **could** swim.* |
| wish + past perfect | regret about the **past** | *I **wish** I **had listened** to you.* |
| wish + would | annoyance, or a wish for change | *I **wish** you **would stop** shouting.* |
| if only | the same, but stronger | ***If only** I **had known** earlier!* |
| It is (high) time + past | something overdue | *It is high time we **left**.* |
| would rather + past | preference about someone else | *I **would rather** you **came** tomorrow.* |
| as if / as though + past | an untrue comparison | *He talks **as if** he **knew** everything.* |

✗ *I wish I would have gone.* → ✓ *I wish I **had** gone.*
✗ *It is time we go.* → ✓ *It is time we **went**.* (or *It is time **for us to
go***.)

::: example Worked item 28.1 — choosing the type
**Problem.** Put the verbs into the correct form. *(a) If you (boil) water, it
(turn) into steam. (b) If she (come) tomorrow, I (meet) her at the airport.
(c) If I (be) the mayor, I (ban) plastic bags. (d) If they (start) earlier, they
(reach) the summit.* — (d) refers to a climb that failed yesterday.

**Solution — identify the reality of each condition.**

1. **(a)** A scientific fact: **type 0**, present simple in both clauses.
   → *If you **boil** water, it **turns** into steam.*
2. **(b)** A real future possibility: **type 1**, present simple in the if-clause,
   *will* in the main clause. → *If she **comes** tomorrow, I **will meet** her at
   the airport.*
3. **(c)** I am not the mayor: **type 2**, past simple (*were*) + *would*.
   → *If I **were** the mayor, I **would ban** plastic bags.*
4. **(d)** The climb is over and they did not start early: **type 3**, past
   perfect + *would have* + past participle. → *If they **had started** earlier,
   they **would have reached** the summit.*
:::

::: example Worked item 28.2 — rewriting with *unless*, *but for* and inversion
**Problem.** Rewrite each sentence as instructed.
*(a) If you do not apologise, he will not forgive you.* — Use *unless*.
*(b) If your brother had not warned me, I would have signed the paper.* — Begin
*But for …*
*(c) If I had seen the notice, I would have applied.* — Begin *Had …*

**Solution — step by step.**

1. **(a)** *Unless* already means *if … not*, so the negative in the if-clause is
   dropped and nothing else changes. → ***Unless you apologise, he will not
   forgive you.***
2. **(b)** *But for* is followed by a **noun phrase**, not a clause. *Your brother
   had not warned me* becomes *your brother's warning*. The main clause is
   unchanged. → ***But for your brother's warning, I would have signed the
   paper.***
3. **(c)** For inversion, delete *if* and move the auxiliary *had* in front of the
   subject *I*. → ***Had I seen the notice, I would have applied.***
:::

::: example Worked item 28.3 — a mixed conditional
**Problem.** Complete: *He missed the train this morning, so he is not at the
meeting now.* — Rewrite as a conditional beginning *If he …*

**Solution — two different times.**

1. **When is the condition?** Missing the train happened **this morning** — it is
   finished. A finished unreal past takes **had + past participle**: *If he **had
   not missed** the train…*
2. **When is the result?** *He is not at the meeting* describes **now**. A present
   unreal result takes **would + base verb**, not *would have*: *…he **would be**
   at the meeting now.*
3. **Check the polarity.** The facts are negative (he missed it, he is absent), so
   the unreal version reverses both.

**Answer.** ***If he had not missed the train, he would be at the meeting now.***
:::

## Chapter summary

- Type 0: *if* + present, present — a general truth.
- Type 1: *if* + present, *will / can / may* + base verb — a real possibility.
- Type 2: *if* + past (*were* for all persons), *would / could / might* + base
  verb — untrue or unlikely now.
- Type 3: *if* + past perfect, *would / could / might have* + past participle —
  impossible, because the time is past.
- Never put *will* or *would* in the if-clause; a fronted if-clause takes a comma.
- Mixed conditionals join a past condition to a present result (*had* + V3 …
  *would* + base) or a present condition to a past result.
- *If* can be dropped in three inverted patterns: *Were I…*, *Had I…*, *Should
  you…*
- *Unless* = *if not*; *in case* means "as a precaution" and takes the present;
  *but for* takes a noun phrase.
- *Wish / if only* + past = regret about now; + past perfect = regret about the
  past; + *would* = annoyance or a wish for change.
- *It is high time* and *would rather* (with a new subject) both take the past
  tense.

## Practice questions

**Put the verbs in brackets into the correct form (1 mark each)**

1. If you (heat) iron, it expands. <span class="marks">[1]</span>
2. If it rains tomorrow, we (postpone) the picnic. <span class="marks">[1]</span>
3. If I (be) you, I would consult a doctor. <span class="marks">[1]</span>
4. If she had taken the medicine, she (recover) by now. <span class="marks">[1]</span>
5. If the bus (not come) on time, we would have missed the flight. <span class="marks">[1]</span>
6. I wish I (know) how to drive. <span class="marks">[1]</span>
7. If only he (listen) to his teachers when he was young! <span class="marks">[1]</span>
8. It is high time you (start) revising for the examination. <span class="marks">[1]</span>
9. Unless you (hurry), you will miss the last bus. <span class="marks">[1]</span>
10. He behaves as if he (own) the whole building. <span class="marks">[1]</span>

::: note Answers
**1.** heat — type 0; both clauses in the present simple.
**2.** will postpone — type 1; *will* goes in the main clause.
**3.** were — type 2; *were* is used for all persons in the unreal past.
**4.** would have recovered — type 3; the condition and the result are both past and unfulfilled. (*would be well by now* would be the mixed form.)
**5.** had not come — type 3 if-clause; past perfect.
**6.** knew — *wish* + past simple for a present regret.
**7.** had listened — *if only* + past perfect for a past regret.
**8.** started — *It is high time* takes the past tense.
**9.** hurry — *unless* already means "if not", so no extra negative.
**10.** owned — *as if* + past simple for an untrue comparison.
:::

**Correct the errors (1 mark each)**

11. If it will rain, the programme will be cancelled. <span class="marks">[1]</span>
12. If I would have known, I would have told you. <span class="marks">[1]</span>
13. Unless you don't work hard, you cannot succeed. <span class="marks">[1]</span>
14. If I was a bird, I would fly over the Himalayas. <span class="marks">[1]</span>
15. I wish I would have attended the seminar. <span class="marks">[1]</span>
16. Take a torch in case the power will go off. <span class="marks">[1]</span>
17. If had he apologised, she would have forgiven him. <span class="marks">[1]</span>
18. It is time we go home. <span class="marks">[1]</span>

::: note Answers
**11.** If it **rains**, the programme will be cancelled. — no *will* in the if-clause.
**12.** If I **had** known, I would have told you. — type 3 uses the past perfect.
**13.** Unless you **work** hard, you cannot succeed. — *unless* carries the negative.
**14.** If I **were** a bird, I would fly over the Himalayas. — unreal *were*.
**15.** I wish I **had attended** the seminar. — *wish* + past perfect for a past regret.
**16.** Take a torch in case the power **goes** off. — *in case* takes the present simple.
**17.** **Had he apologised**, she would have forgiven him. — with inversion, *if* is deleted.
**18.** It is time we **went** home. — *It is time* + past tense.
:::

**Rewrite as instructed (1 mark each)**

19. *If you do not water the plants, they will die.* — Use *unless*. <span class="marks">[1]</span>
20. *If she had not helped me, I would have been in trouble.* — Begin: *But for …* <span class="marks">[1]</span>
21. *If I were rich, I would build a school in my village.* — Begin: *Were …* <span class="marks">[1]</span>
22. *He did not take my advice, so he is in difficulty now.* — Rewrite as a conditional. <span class="marks">[1]</span>
23. *I am sorry I did not book the ticket in advance.* — Begin: *I wish …* <span class="marks">[1]</span>

::: note Answers
**19.** **Unless you water the plants, they will die.** — the negative disappears with *unless*.
**20.** **But for her help, I would have been in trouble.** — *but for* is followed by a noun phrase.
**21.** **Were I rich, I would build a school in my village.** — *if* is deleted and *were* moves in front of the subject.
**22.** **If he had taken my advice, he would not be in difficulty now.** — a mixed conditional: past condition, present result.
**23.** **I wish I had booked the ticket in advance.** — regret about the past takes *wish* + past perfect.
:::
