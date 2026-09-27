---
subject: Compulsory English
grade: 11
unit: 27
title: Conditional Sentences
hours: 4
area: Grammar
---

A **conditional sentence** has two parts: an *if*-clause stating a condition and a
main clause stating the result. The whole system rests on one idea — how **real**
the speaker thinks the condition is. A real condition uses ordinary tenses; an
unreal one uses a tense one step further back than the time it refers to. NEB Q7
tests conditionals almost every year, usually as *Complete the sentence* or
*Rewrite using "if"*, and the marker is checking one thing: the correct pair of
verb forms across the two clauses.

::: key The one pattern to memorise
A conditional is a **pair**. Learn the two halves together and never write one
without the other:
Type 1 — *if* + present, **will** + V1. Type 2 — *if* + past, **would** + V1.
Type 3 — *if* + had + V3, **would have** + V3. Getting the pairing right is the
mark.
:::

## 27.1 The shape of a conditional sentence

Either clause may come first. When the *if*-clause comes first, put a **comma**
after it; when it comes second, no comma is used.

- ***If it rains tomorrow,** the picnic will be cancelled.* (comma)
- *The picnic will be cancelled **if it rains tomorrow**.* (no comma)

::: caution Never put *will* or *would* in the *if*-clause
This is the commonest conditional error of all.
~~If it will rain, we will stay at home.~~ → **If it rains, we will stay at home.**
~~If I would have money, I would buy a laptop.~~ → **If I had money, I would buy a
laptop.**
~~If he would have come, we would have won.~~ → **If he had come, we would have won.**
The *if*-clause carries the tense; the main clause carries the modal.
(One exception: *will* in an *if*-clause meaning "is willing to" — *If you will wait
here a moment, I'll fetch the file* — is a polite request, not a condition.)
:::

## 27.2 The five types in one table

| Type | *if*-clause | Main clause | Use | Example |
|---|---|---|---|---|
| **0 — zero** | if + simple present | simple present | a fact, a scientific law, something always true | If you heat ice, it **melts**. |
| **1 — first** | if + simple present | will / can / may / must / imperative + V1 | a real, likely future possibility | If the bus **leaves** on time, we **will reach** Pokhara by six. |
| **2 — second** | if + simple past (*were* for all persons) | would / could / might + V1 | unreal or unlikely in the **present or future**; also advice | If I **were** the mayor, I **would clean** the Bagmati. |
| **3 — third** | if + past perfect (had + V3) | would / could / might + **have** + V3 | an impossible, imagined **past**; regret | If she **had studied** harder, she **would have passed**. |
| **mixed (3 → 2)** | if + past perfect | would + V1 (present result) | a past condition with a present result | If I **had taken** the scholarship, I **would be** in Japan now. |
| **mixed (2 → 3)** | if + simple past | would + have + V3 (past result) | a permanent present condition with a past result | If he **were** more careful, he **would not have broken** the screen. |

```figure caption="Choosing the type. First ask whether the condition is real or imagined; then ask which time the imagined condition belongs to. The two mixed types appear when the condition and the result sit in different times."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,4.2))
ax.set_xlim(0,10); ax.set_ylim(0,13.2); ax.axis('off')
def box(x,y,w,h,t,fc,ec,fs=7.8,tc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.12",fc=fc,ec=ec,lw=1.0))
    ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs,color=tc or INK,
            linespacing=1.4)
def arw(x0,y0,x1,y1,lab=None,lx=0.0,ly=0.0):
    ax.annotate('',xy=(x1,y1),xytext=(x0,y0),
                arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.0,mutation_scale=9))
    if lab:
        ax.text((x0+x1)/2+lx,(y0+y1)/2+ly,lab,fontsize=7.0,color=MUTED,
                ha='center',va='center',bbox=dict(fc='white',ec='none',pad=1.2))
box(2.4,11.8,5.2,1.1,"Is the condition REAL?","#ffffff",INK,8.4)
box(0.15,9.3,4.1,1.3,"always true\n(a fact or law)","#eef7f1",'#0B6A62',7.8,'#0B6A62')
box(5.7,9.3,4.1,1.3,"possible in the future","#eef7f1",'#0B6A62',7.8,'#0B6A62')
arw(3.8,11.8,2.2,10.7,"yes",lx=-0.5)
arw(6.2,11.8,7.7,10.7,"yes",lx=0.5)
box(0.15,7.5,4.1,1.2,"TYPE 0\nif + present, present","#ffffff",'#0B6A62',7.8)
box(5.7,7.5,4.1,1.2,"TYPE 1\nif + present, will + V1","#ffffff",'#0B6A62',7.8)
arw(2.2,9.3,2.2,8.8); arw(7.75,9.3,7.75,8.8)
box(1.8,5.4,6.4,1.1,"NO — it is imagined. Which time?","#fdf1e7",'#B4690E',8.0,'#B4690E')
arw(5.0,11.8,5.0,6.6,"no",ly=-2.3)
box(0.15,3.3,3.0,1.4,"now or future","#ffffff",MUTED,7.6)
box(3.5,3.3,3.0,1.4,"the past","#ffffff",MUTED,7.6)
box(6.85,3.3,2.95,1.4,"past cause,\npresent result","#ffffff",MUTED,7.6)
arw(3.4,5.4,1.7,4.7); arw(5.0,5.4,5.0,4.7); arw(6.6,5.4,8.3,4.7)
box(0.15,1.1,3.0,1.5,"TYPE 2\nif + past,\nwould + V1","#eaf0fb",ACCENT,7.6,ACCENT)
box(3.5,1.1,3.0,1.5,"TYPE 3\nif + had + V3,\nwould have + V3","#eaf0fb",ACCENT,7.6,ACCENT)
box(6.85,1.1,2.95,1.5,"MIXED\nif + had + V3,\nwould + V1","#eaf0fb",ACCENT,7.6,ACCENT)
arw(1.65,3.3,1.65,2.7); arw(5.0,3.3,5.0,2.7); arw(8.32,3.3,8.32,2.7)
```

## 27.3 Type 0 — the zero conditional

**Form.** *if* + simple present, simple present. *If* can be replaced by *when* with
no change of meaning, which is the test for a zero conditional.

- *If you **heat** water to 100 °C, it **boils**.*
- *If the Koshi **rises** above the danger mark, the barrage gates **are opened**.*
- *If you **press** this switch, the pump **starts**.*

Use it for laws of nature, machines, rules and habits — anything that happens
**every time**.

## 27.4 Type 1 — the real future conditional

**Form.** *if* + simple present, **will** + V1. Instead of *will* you may use
*can, may, might, must, should* or an imperative, depending on the meaning.

- *If you **revise** every evening, you **will pass** easily.*
- *If the strike **continues**, the vegetables **may rot** in the trucks.*
- *If you **see** Dipesh at the bus park, **tell** him to call me.* (imperative)
- *If it **is** sunny tomorrow, we **can walk** up to Sarangkot.*

Remember: present tense in the *if*-clause even though the meaning is future. The
same applies after *when, as soon as, until, before, after*.

## 27.5 Type 2 — the unreal present conditional

**Form.** *if* + simple past, **would** + V1 (*could* for ability, *might* for
possibility).

Type 2 does **not** talk about the past. The past tense is a signal of
*unreality*, not of past time. Use it when the condition is imaginary, impossible,
or merely unlikely.

- *If I **had** a motorbike, I **would ride** to Dhulikhel every Saturday.*
  (I do not have one.)
- *If Nepal **were** on the sea, trade **would be** much cheaper.* (It is not.)
- *If she **spoke** Japanese, she **could apply** for that job.*

**Were for all persons.** In careful written English the verb *be* in a type-2
*if*-clause is **were** for every subject, including *I, he, she, it*. This is the
old subjunctive, and the NEB marking scheme expects it.

- *If I **were** you, I **would apologise** to the headmaster.*
- *If he **were** here, he **would know** what to do.*

*If I were you …* is the standard formula for giving advice.

## 27.6 Type 3 — the unreal past conditional

**Form.** *if* + had + V3, **would have** + V3 (*could have*, *might have*).

Type 3 talks about something that did **not** happen, and imagines the opposite. It
carries regret or criticism.

- *If we **had left** an hour earlier, we **would have avoided** the jam at
  Koteshwor.* (We did not leave earlier, so we did not avoid it.)
- *If the doctor **had arrived** in time, the patient **might have survived**.*
- *If you **had told** me, I **could have helped** you.*

Every type-3 sentence states the opposite of what really happened. Reading it
backwards is a good check: *If she had studied, she would have passed* means **she
did not study and she did not pass**.

## 27.7 Mixed conditionals

Sometimes the condition belongs to one time and the result to another.

| Mix | *if*-clause | Main clause | Example |
|---|---|---|---|
| **Past condition → present result** | if + had + V3 | would + V1 | *If I **had saved** that money, I **would have** a laptop now.* |
| **Present condition → past result** | if + simple past | would have + V3 | *If Kamal **were** a careful driver, he **would not have hit** the wall.* |

```figure caption="Which part of time each type talks about. Type 2 is about now, not the past, even though its verb is past; type 3 is about the past; a mixed conditional stretches from a past condition to a present result."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,3.8))
ax.set_xlim(0,10); ax.set_ylim(0,12); ax.axis('off')
def bar(x,w,y,t,fc,ec,fs=7.0):
    ax.add_patch(FancyBboxPatch((x,y),w,1.1,boxstyle="round,pad=0.10",
                                fc=fc,ec=ec,lw=1.0))
    ax.text(x+w/2,y+0.55,t,ha='center',va='center',fontsize=fs,color=INK,
            linespacing=1.4)
def lab(y,t,c):
    ax.text(0.15,y,t,ha='left',va='center',fontsize=7.6,color=c)
for xs in (4.35,7.05):
    ax.plot([xs,xs],[1.6,11.0],ls=':',lw=0.8,color=GRID,zorder=0)
ax.annotate('',xy=(9.95,1.6),xytext=(0.05,1.6),
            arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.0,mutation_scale=10))
for xc,t in ((2.2,'PAST'),(5.7,'NOW'),(8.5,'FUTURE')):
    ax.text(xc,0.8,t,ha='center',va='center',fontsize=7.6,color=MUTED)
lab(11.35,'TYPE 1 — a real future possibility',"#0B6A62")
bar(7.20,2.65,9.9,"if + present,\nwill + V1","#eef7f1","#0B6A62")
lab(8.85,'TYPE 2 — unreal NOW or future',ACCENT)
bar(4.50,5.35,7.4,"if + past, would + V1",'#eaf0fb',ACCENT)
lab(6.35,'TYPE 3 — unreal PAST',ACCENT)
bar(0.15,4.05,4.9,"if + had + V3, would have + V3",'#eaf0fb',ACCENT)
lab(3.85,'MIXED — past cause, present result',"#B4690E")
bar(0.15,2.45,2.4,"if + had + V3",'#fdf1e7',"#B4690E")
bar(4.50,2.40,2.4,"would + V1",'#fdf1e7',"#B4690E")
ax.annotate('',xy=(4.55,2.95),xytext=(2.65,2.95),
            arrowprops=dict(arrowstyle='-|>',color="#B4690E",lw=1.0,mutation_scale=9))
```

Look for the time words — *now, today, still* in the result clause signals the first
mix; a permanent characteristic in the *if*-clause signals the second.

## 27.8 Other ways of expressing a condition

| Expression | Meaning | Example |
|---|---|---|
| **unless** | if … not | You will fail **unless** you work harder. |
| provided (that) / providing | only on this condition | You may go **provided that** you return by six. |
| as long as / so long as | only on this condition | I will lend it to you **as long as** you take care of it. |
| on condition that | a strict condition | He was released **on condition that** he report weekly. |
| in case | as a precaution | Take an umbrella **in case** it rains. |
| suppose / supposing | imagine that | **Suppose** you lost your citizenship — what would you do? |
| otherwise / or else | if that does not happen | Hurry up, **otherwise** you will miss the bus. |
| but for | if it were not for | **But for** your help, I would have failed. |
| without | if there were no | **Without** water, nothing would grow. |
| if only | a strong wish or regret | **If only** I had listened to my teacher! |

::: caution *Unless* already contains the negative
*Unless* means "if … not", so a second negative makes the sentence say the opposite
of what you mean.
~~Unless you don't hurry, you will miss the bus.~~ →
**Unless you hurry, you will miss the bus.** (= If you do not hurry …)
Also note that *in case* is not the same as *if*: *Take an umbrella in case it
rains* means take it **now**, as a precaution; *Take an umbrella if it rains* means
take it **only when** it is already raining.
:::

## 27.9 Leaving out *if* — inversion

In formal English the *if* can be dropped and the auxiliary moved to the front.
This appears in NEB rewriting items.

| With *if* | Inverted |
|---|---|
| If I were you, I would accept. | **Were I** you, I would accept. |
| If he had known, he would have come. | **Had he known**, he would have come. |
| If you should need help, call me. | **Should you need** help, call me. |

Only *were*, *had* and *should* invert. Never write ~~Did I know…~~ for *If I knew*.

## 27.10 Unreal forms related to conditionals

The same backshifted tenses appear after *wish*, *if only*, *as if*, *would rather*
and *it's time*.

| Structure | Time referred to | Example |
|---|---|---|
| wish + simple past | a regret about **now** | I **wish** I **knew** her address. |
| wish + *were* | a regret about **now** | I **wish** I **were** taller. |
| wish + would + V1 | annoyance, a wish for change | I **wish** it **would stop** raining. |
| wish + past perfect | a regret about the **past** | I **wish** I **had taken** science. |
| if only + past / past perfect | a stronger regret | **If only** I **had listened** to my father! |
| as if / as though + past | an unreal comparison | He talks **as if** he **owned** the shop. |
| would rather + past | a preference about another person | I'**d rather** you **came** tomorrow. |
| it's time + past | it should already be happening | **It's time** we **left** for the airport. |

::: tip What the Q7 conditional item looks like
Three common shapes. (i) *Complete the sentence*: *If I had known about the
meeting, …* — read the *if*-clause, identify the type from its verb form, then
supply the matching main clause. (ii) *Choose the correct form* with two options in
brackets. (iii) *Rewrite using "if"*: a sentence like *He did not revise, so he
failed* becomes a **type 3**, because both facts are past and you are imagining the
opposite. Always flip the polarity: a positive fact becomes a negative condition,
and a negative fact becomes a positive one.
:::

::: example Worked transformation 27.1 — turning two facts into a conditional
**Problem.** Rewrite using *if*: *Sushma did not set an alarm, so she missed the
6 a.m. bus to Butwal.*

**Solution — step by step.**

1. **Find the two facts and their time.** Fact 1: she did not set an alarm (past).
   Fact 2: she missed the bus (past). Both are finished past facts.
2. **Choose the type.** We are imagining the opposite of a past fact → **type 3**.
3. **Flip the polarity of each fact.** "did not set" → *had set*; "missed" →
   *would not have missed*.
4. **Put them in the type-3 frame:** *if* + had + V3, would have + V3.

**Answer.** *If Sushma **had set** an alarm, she **would not have missed** the
6 a.m. bus to Butwal.*
:::

::: example Worked transformation 27.2 — completing a type-2 sentence
**Problem.** Complete: *If I were the principal of this school, …*

**Solution — step by step.**

1. **Identify the type from the *if*-clause.** *were* is a simple past subjunctive →
   **type 2**, an unreal present.
2. **Recall the matching main clause.** Type 2 pairs with **would / could / might +
   V1** — never *will*, never *would have*.
3. **Write a sensible result in that form.**

**Answer.** *If I were the principal of this school, I **would build** a proper
library and **would start** a science club.*

Writing *I will build* would be a type-1 main clause and would lose the mark;
*I would have built* would be type 3 and refers to the past.
:::

::: example Worked transformation 27.3 — *unless*, inversion and a mixed type
**Problem.** (a) Rewrite with *unless*: *If you do not submit the form today, your
application will be rejected.* (b) Rewrite without *if*: *If I had known about the
strike, I would have started earlier.* (c) Complete: *If Bishal had accepted the
job in Dubai, he … (be) here today.*

**Solution.**

**(a)** *Unless* already means "if … not", so remove the *do not* and keep the verb
positive.
**Answer:** ***Unless you submit** the form today, your application will be
rejected.*

**(b)** Type 3 inverts with *had*: drop *if*, move *had* to the front, keep the rest
unchanged.
**Answer:** ***Had I known** about the strike, I would have started earlier.*

**(c)** The *if*-clause is past perfect (a past condition) but *today* in the result
clause points to the present → a **mixed conditional**. The main clause therefore
takes *would* + V1, and the meaning is negative, because he is in fact here.
**Answer:** *… he **would not be** here today.*
:::

## Chapter summary

- Type 0: *if* + present, present — always true.
- Type 1: *if* + present, **will** + V1 — a real future possibility.
- Type 2: *if* + past (*were* for all persons), **would** + V1 — unreal present.
- Type 3: *if* + had + V3, **would have** + V3 — unreal past, regret.
- Mixed: *if* + had + V3, **would** + V1 (past cause, present result); *if* + past,
  **would have** + V3 (present cause, past result).
- Never put *will* or *would* in the *if*-clause.
- A comma follows the *if*-clause only when it comes first.
- *Unless* = *if … not*, so do not add a second negative.
- *Were I…*, *Had I…*, *Should you…* are the inverted forms with *if* dropped.
- *Wish* + past = a present regret; *wish* + past perfect = a past regret;
  *wish* + *would* = annoyance.

## Practice questions

**Complete the sentences with the correct form of the verb in brackets (1 mark each)**

1. If you heat iron, it ____ . (expand) <span class="marks">[1]</span>
2. If it ____ tomorrow, we will postpone the excursion. (rain) <span class="marks">[1]</span>
3. If I ____ you, I would apologise to her at once. (be) <span class="marks">[1]</span>
4. If she had left home earlier, she ____ the interview. (not miss) <span class="marks">[1]</span>
5. If Nepal ____ a seaport, imports would be much cheaper. (have) <span class="marks">[1]</span>
6. If the villagers ____ the warning, many lives would have been saved. (heed) <span class="marks">[1]</span>
7. If I ____ the scholarship last year, I would be studying in Japan now. (accept) <span class="marks">[1]</span>
8. Unless you ____ your fee by Friday, your name will be struck off. (pay) <span class="marks">[1]</span>
9. I wish I ____ how to swim in the Seti. (know) <span class="marks">[1]</span>
10. It is time we ____ for the bus park. (leave) <span class="marks">[1]</span>

::: note Answers
**1.** expands — a zero conditional: a physical law, present in both clauses.
**2.** rains — type 1: the *if*-clause takes the simple present, never *will*.
**3.** were — type 2 uses *were* for all persons in the *if*-clause.
**4.** would not have missed — type 3: *had* + V3 pairs with *would have* + V3.
**5.** had — type 2: an unreal present condition takes the simple past.
**6.** had heeded — type 3: the main clause *would have been saved* fixes the type.
**7.** had accepted — a mixed conditional: past condition, present result *now*.
**8.** pay — after *unless* use the present, and add no second negative.
**9.** knew — *wish* + simple past expresses a regret about the present.
**10.** left — *it is time* + simple past.
:::

**Rewrite the sentences as instructed (1 mark each)**

11. *He did not work hard, so he failed the examination.* — Rewrite using *if*. <span class="marks">[1]</span>
12. *She is not tall, so she cannot reach the top shelf.* — Rewrite using *if*. <span class="marks">[1]</span>
13. *Study regularly, or you will not pass.* — Rewrite using *unless*. <span class="marks">[1]</span>
14. *If I had known your number, I would have called you.* — Rewrite without *if*. <span class="marks">[1]</span>
15. *If I were the mayor, I would widen this road.* — Rewrite without *if*. <span class="marks">[1]</span>
16. *I am sorry I did not choose science in Grade 11.* — Rewrite beginning *I wish …* <span class="marks">[1]</span>
17. *Take some water with you in case the tap is dry.* — Rewrite using *if*. <span class="marks">[1]</span>
18. *But for your help, I would have been fined.* — Rewrite using *if*. <span class="marks">[1]</span>

::: note Answers
**11.** **If he had worked hard, he would not have failed** the examination. — both facts are past, so type 3, with the polarity flipped.
**12.** **If she were tall, she could reach** the top shelf. — an unreal present, so type 2 with *were*.
**13.** **Unless you study regularly, you will not pass.** — *unless* replaces *if … not*.
**14.** **Had I known** your number, I would have called you. — type-3 inversion with *had*.
**15.** **Were I** the mayor, I would widen this road. — type-2 inversion with *were*.
**16.** **I wish I had chosen science** in Grade 11. — a past regret takes *wish* + past perfect.
**17.** Take some water with you **if the tap is dry** (or *in case it is dry*) — note *in case* means as a precaution beforehand.
**18.** **If you had not helped me**, I would have been fined. — *but for* becomes a negative type-3 *if*-clause.
:::

**Correct the errors in the following sentences (1 mark each)**

19. If it will rain tomorrow, the match will be postponed. <span class="marks">[1]</span>
20. If I would have money, I would buy a new bicycle. <span class="marks">[1]</span>
21. If she would have called me, I would have gone with her. <span class="marks">[1]</span>
22. Unless you don't hurry, you will miss the first bus. <span class="marks">[1]</span>
23. If I was you, I would not sign that paper. <span class="marks">[1]</span>
24. If he had studied harder, he would pass the examination last year. <span class="marks">[1]</span>
25. If you will heat ice, it melts. <span class="marks">[1]</span>
26. I wish I would have taken the earlier flight. <span class="marks">[1]</span>

::: note Answers
**19.** If it **rains** tomorrow … — no *will* in the *if*-clause of a type 1.
**20.** If I **had** money … — type 2 takes the simple past in the *if*-clause.
**21.** If she **had called** me … — type 3 takes *had* + V3, not *would have*.
**22.** Unless you **hurry** … — *unless* already means "if not".
**23.** If I **were** you … — the type-2 subjunctive is *were* for all persons.
**24.** … he **would have passed** the examination last year. — a past result needs *would have* + V3.
**25.** If you **heat** ice, it melts. — a zero conditional uses the present in both clauses.
**26.** I wish I **had taken** the earlier flight. — a past regret takes *wish* + past perfect.
:::
