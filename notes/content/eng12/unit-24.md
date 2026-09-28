---
subject: Compulsory English
grade: 12
unit: 24
title: Subject-Verb Agreement and Miscellaneous Agreements
hours: 4
area: Grammar
---

**Agreement** (also called **concord**) means that words which belong together
must match in number and person: a singular subject takes a singular verb, a
plural antecedent takes a plural pronoun. The rule sounds trivial — *He goes*,
*They go* — but NEB Q7 never tests the trivial case. It tests the sentence in
which a long phrase stands between the subject and the verb, or in which a
plural-looking noun is really singular. This unit lists every pattern the board
uses, and ends with the other agreements — pronoun, demonstrative and
number-compound — that the same question can turn on.

::: key Find the subject before you choose the verb
The verb agrees with the **head noun of the subject**, never with the noun
standing closest to it. Cross out every phrase beginning with *of, with, along
with, as well as, including, besides, in addition to* and every relative clause;
what is left is the subject.
*The **quality** of the mangoes sold in the market **was** excellent.*
:::

## 24.1 The basic rule and the words that hide it

A singular subject takes the verb form ending in **-s** in the present tense
(*he works*); a plural subject takes the bare form (*they work*). In the past
tense only *be* changes (*was / were*).

```figure caption="The verb agrees with the head noun of the subject. The material in between — an of-phrase, a participle phrase, or an along-with phrase — never changes the number."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.4))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
GREEN="#0B6A62"; AMBER="#B4690E"
def cell(x,y,w,h,t,fc,ec,fs=7.4,tc=None,ls='-'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.09",fc=fc,ec=ec,
                                lw=1.0,linestyle=ls))
    ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs,color=tc or INK,
            linespacing=1.4)
def link(x0,x1,y,col):
    ax.annotate('', xy=(x1,y), xytext=(x0,y),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.1, mutation_scale=9,
                                connectionstyle="arc3,rad=0.18"))
cell(0.15,7.95,2.45,1.05,"The quality","#e8f3ee",GREEN,7.8,GREEN)
cell(2.80,7.95,4.45,1.05,"of the mangoes sold\nin the market","#f4f6f8",MUTED,6.9,MUTED,'--')
cell(7.45,7.95,2.40,1.05,"was excellent.","#fdf1e7",AMBER,7.8,AMBER)
link(1.38,8.65,7.72,AMBER)
ax.text(5.00,6.15,"the verb agrees with the head noun, not with mangoes or market",
        fontsize=7.0,color=AMBER,ha='center')
cell(0.15,4.35,2.45,1.05,"Ram","#e8f3ee",GREEN,7.8,GREEN)
cell(2.80,4.35,4.45,1.05,"along with his three\nbrothers,","#f4f6f8",MUTED,6.9,MUTED,'--')
cell(7.45,4.35,2.40,1.05,"was present.","#fdf1e7",AMBER,7.8,AMBER)
link(1.38,8.65,4.12,AMBER)
ax.text(5.00,2.60,"subject = Ram (singular), so was, never were",
        fontsize=7.0,color=AMBER,ha='center')
ax.plot([0.15,9.85],[2.00,2.00],color=GRID,lw=0.9)
ax.text(0.15,1.35,"Phrases that never change the number of the subject:",
        fontsize=7.2,color=INK,ha='left')
ax.text(0.15,0.55,"along with · together with · as well as · besides · in addition to · including",
        fontsize=7.0,color=ACCENT,ha='left')
```

- *The **list** of candidates **has** been published.* (not ~~have~~)
- *The **causes** of this accident **are** still unknown.*
- *One of my **friends** **lives** in Dhangadhi.* (subject = *one*)
- *The **boy** who won the prizes **is** from Surkhet.*

## 24.2 Two or more subjects joined together

| Pattern | Verb | Example |
|---|---|---|
| A **and** B (two different things) | plural | *Sita **and** Gita **are** cousins.* |
| A **and** B naming **one** thing or one person | singular | *Bread and butter **is** a cheap breakfast.* / *The Principal and Manager **is** on leave.* (one person) |
| The A **and the** B (two people) | plural | *The Principal **and the** Manager **are** on leave.* |
| **Each / Every** A and **each / every** B | singular | *Every boy and every girl **was** given a badge.* |
| A **as well as / along with / together with / besides / in addition to** B | agrees with **A** | *The captain, as well as the players, **was** praised.* |
| **Either** A **or** B / **Neither** A **nor** B | agrees with the **nearer** subject | *Neither the teacher nor the students **were** present.* |
| **Not only** A **but also** B | agrees with the **nearer** subject | *Not only the boys but also the girl **was** late.* |
| A **or** B | agrees with the **nearer** subject | *Two pens or a pencil **is** enough.* |

```figure caption="The proximity rule. With either-or, neither-nor and not only-but also, the verb copies the subject standing next to it — so reversing the two subjects changes the verb."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.2))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
AMBER="#B4690E"
def cell(x,y,w,t,fc,ec,fs=7.4,tc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,1.00,boxstyle="round,pad=0.09",fc=fc,ec=ec,lw=1.0))
    ax.text(x+w/2,y+0.50,t,ha='center',va='center',fontsize=fs,color=tc or INK)
def row(y, lead, near, verb, note):
    cell(0.15,y,3.95,lead,"#ffffff",MUTED,7.3)
    cell(4.30,y,2.55,near,"#eef2fb",ACCENT,7.3,ACCENT)
    cell(7.05,y,2.80,verb,"#fdf1e7",AMBER,7.3,AMBER)
    ax.annotate('', xy=(8.45,y-0.40), xytext=(5.55,y-0.40),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.0,
                                mutation_scale=8, connectionstyle="arc3,rad=0.30"))
    ax.text(5.00, y-1.55, note, fontsize=7.0, color=MUTED, ha='center', va='center')
ax.text(0.15, 9.45, "either … or   ·   neither … nor   ·   not only … but also",
        fontsize=7.6, color=INK, ha='left')
ax.plot([0.15,9.85],[8.95,8.95],color=GRID,lw=0.9)
row(7.40, "Neither the teacher nor", "the students", "were present.",
    "nearer subject plural  →  plural verb")
row(3.60, "Neither the students nor", "the teacher", "was present.",
    "nearer subject singular  →  singular verb")
ax.text(5.00, 0.75, "Either you or I  am  to blame.  —  the person follows the nearer subject too",
        fontsize=7.0, color=INK, ha='center')
```

::: caution *As well as* is not *and*
*And* makes a plural subject; *as well as* does not — it only adds extra
information.
✗ *Hari as well as his friends were absent.* → ✓ *Hari as well as his friends
**was** absent.*
✗ *The teacher along with the students have arrived.* → ✓ *The teacher along with
the students **has** arrived.*
:::

## 24.3 Pronouns and distributives as subjects

**Always singular:** *each, every, either, neither, one, everyone, everybody,
everything, someone, somebody, something, anyone, anybody, anything, no one,
nobody, nothing, many a, more than one*.

- *Each of the candidates **has** been interviewed.*
- *Neither of the two answers **is** correct.*
- *Everybody in the hostel **was** asleep.*
- *Many a student **has** failed in this paper.*
- *More than one house **was** damaged.* (singular, although the sense is plural)

**Always plural:** *both, few, a few, many, several, others*.

- *Both of the roads **are** blocked.* *Several **were** missing.*

**It depends on the noun after *of*:** *some, all, most, half, none, a lot,
plenty, the rest*, and all fractions and percentages.

- *Half of the apple **is** rotten.* / *Half of the apples **are** rotten.*
- *Two-thirds of the land **is** barren.* / *Two-thirds of the farmers **are**
  landless.*
- *Most of the water **has** dried up.* / *Most of the students **have** paid.*
- *None of the boys **was** selected.* (formal writing keeps the singular)

**The two number phrases that behave differently:**

- ***A number of*** + plural noun → **plural** verb: *A number of tourists **are**
  waiting.*
- ***The number of*** + plural noun → **singular** verb: *The number of tourists
  **is** rising.*

## 24.4 Nouns whose number is not what it looks

| Group | Verb | Examples |
|---|---|---|
| Subjects and diseases ending in -s | singular | *Mathematics **is** easy. Physics, economics, politics, statistics, civics, ethics, news, measles, mumps, athletics.* |
| Tools and clothes in two parts | plural | *The scissors **are** blunt. Trousers, spectacles, binoculars, pliers, jeans.* |
| *a pair of* + those nouns | singular | *A pair of scissors **is** missing.* |
| Nouns plural in meaning without -s | plural | *The police **are** investigating. Cattle, people, vermin, poultry, gentry.* |
| Titles of books, plays and newspapers | singular | *Gulliver's Travels **is** a satire. The Kathmandu Post **is** a daily.* |
| Names of countries and organisations | singular | *The United States **is** a federal republic. The Philippines, the United Nations.* |
| Money, distance, time and weight as one amount | singular | *Twenty rupees **is** not much. Ten kilometres **is** a long walk. Five years **is** a long time.* |
| Collective nouns acting as one body | singular | *The committee **has** taken a decision. The team, the jury, the family, the government, the audience, the class.* |
| The same nouns when the members act separately | plural | *The jury **were** divided in their opinion.* |
| *The* + adjective (a whole class of people) | plural | *The rich **are** not always happy. The poor, the blind, the Nepalese.* |
| A gerund, an infinitive or a clause as subject | singular | *Swimming **is** good exercise. To err **is** human. What she needs **is** two days' rest.* |

*Statistics* and *politics* change with the meaning: *Statistics **is** a branch
of mathematics* (the subject) but *These statistics **are** misleading* (the
figures).

## 24.5 Word order that hides the subject

- **There is / There are** — the verb agrees with the noun that **follows** it:
  *There **is** a temple on the hill.* / *There **are** two temples on the hill.*
  With a mixed list, it agrees with the nearer noun: *There **is** a pen and two
  erasers in the box.*
- **Here comes / Here come** — same rule: *Here **comes** the bus.*
- **Inverted sentences** — the subject is after the verb: *On the wall **hang**
  three old photographs.*
- **Relative clauses** — the verb inside the clause agrees with the antecedent:
  *He is one of the boys who **have** passed.* (the boys passed) but *He is the
  only one of the boys who **has** passed.* (only he passed)

## 24.6 Miscellaneous agreements

Agreement is not only between subject and verb.

**Pronoun and antecedent.** A pronoun matches its antecedent in number, person
and gender.

- *Every student must bring **his or her** admit card.* (formal written English;
  *their* is now widely accepted and is common in speech)
- *Each of the girls has finished **her** work.*
- *The committee announced **its** decision.* (one body) / *The committee took
  **their** seats.* (members)
- *Neither Ram nor Hari has brought **his** book.*

**Demonstrative and noun.** *This / that* with a singular noun, *these / those*
with a plural one, and the same for *kind* and *sort*:

- *This **kind** of book **is** useful.* / *These **kinds** of books **are**
  useful.* (never ~~these kind of books~~)

**Number compounds used as adjectives** stay singular and take hyphens:

- *a **five-year-old** boy* (but *the boy is five **years** old*)
- *a **ten-rupee** note*, *a **two-hour** journey*, *a **500-metre** race*
- *two **dozen** eggs*, *three **hundred** students* — no -s after a number, but
  *dozens of eggs*, *hundreds of students*

**Sequence of tenses.** A past-tense main verb normally pulls the subordinate
clause into the past: *He said that he **was** busy.* The exception is a universal
truth: *The teacher told us that the earth **moves** round the sun.*

::: caution The agreement errors that appear in every script
✗ *One of my friend are coming.* → ✓ *One of my **friends is** coming.*
✗ *Each of the students have submitted.* → ✓ *Each of the students **has**
submitted.*
✗ *The police is searching for him.* → ✓ *The police **are** searching for him.*
✗ *Mathematics are my favourite subject.* → ✓ *Mathematics **is** my favourite
subject.*
✗ *There is many problems in this plan.* → ✓ *There **are** many problems …*
✗ *The number of accidents are increasing.* → ✓ *The number of accidents **is**
increasing.*
✗ *Five years are a long time.* → ✓ *Five years **is** a long time.*
✗ *These kind of mistakes are common.* → ✓ *These **kinds** of mistakes are
common.*
:::

::: example Worked item 24.1 — a long phrase between subject and verb
**Problem.** Choose the correct verb: *The list of the students who passed the
board examination (has / have) been pasted on the notice board.*

**Solution — step by step.**

1. **Strike out the modifiers.** *of the students* is an of-phrase; *who passed
   the board examination* is a relative clause describing *students*. Neither can
   be the subject.
2. **What is left?** *The list*, a singular noun.
3. **Match the verb.** A singular subject needs *has*.

**Answer.** *The list of the students who passed the board examination **has**
been pasted on the notice board.*
:::

::: example Worked item 24.2 — the proximity rule in both directions
**Problem.** Fill in with the correct form of *be* in the present tense:
*(a) Neither the principal nor the teachers ____ willing to change the routine.
(b) Neither the teachers nor the principal ____ willing to change the routine.*

**Solution — step by step.**

1. **Identify the construction.** Both sentences use *neither … nor*, so the
   proximity rule applies: the verb agrees with whichever subject stands **nearer**
   to it.
2. **(a)** The nearer subject is *the teachers*, which is plural. **Answer:**
   ***are** willing*.
3. **(b)** The nearer subject is *the principal*, which is singular. **Answer:**
   ***is** willing*.

The two sentences mean the same thing but take different verbs — which is exactly
why the examiner sets them.
:::

::: example Worked item 24.3 — several agreement faults in one sentence
**Problem.** Correct: *Each of the boy in these kind of classes have their own
tablet, and the number of such classes are growing.*

**Solution — one fault at a time.**

1. *Each of the boy* — *each of* must be followed by a **plural** noun → *each of
   the **boys***.
2. *these kind of classes* — *these* is plural, so *kind* must be plural →
   ***these kinds of** classes*.
3. *have* — the subject is *each*, which is always **singular** → ***has***.
4. *their own tablet* — the antecedent *each* is singular, so formal writing uses
   ***his or her** own tablet*.
5. *the number of such classes are* — *the number of* always takes a **singular**
   verb → ***is** growing*.

**Answer.** *Each of the **boys** in **these kinds** of classes **has his or her**
own tablet, and the number of such classes **is** growing.*
:::

## Chapter summary

- The verb agrees with the **head noun** of the subject; of-phrases, participle
  phrases and relative clauses in between change nothing.
- *And* joins two subjects into a plural — unless they name one thing or one
  person (*Bread and butter is …*), or are preceded by *each / every*.
- *As well as, along with, together with, besides, in addition to* keep the verb
  agreeing with the **first** subject.
- *Either … or, neither … nor, not only … but also, or* follow the **proximity
  rule**: the verb matches the nearer subject.
- Singular always: *each, every, either, neither, one, everyone, nobody, many a,
  more than one*. Plural always: *both, few, many, several*.
- *Some, all, most, half, none* and fractions take their number from the noun
  after *of*.
- *A number of* + plural verb; *the number of* + singular verb.
- *Mathematics, physics, news, politics* are singular; *scissors, trousers,
  police, cattle, people* are plural.
- Money, distance and time treated as one amount take a singular verb.
- *There is / are* and *Here comes / come* agree with what follows them.
- Pronouns match their antecedents; *these kinds of books*, not *these kind of
  books*; and a number compound used as an adjective stays singular
  (*a ten-rupee note*).

## Practice questions

**Fill in the blanks with the correct form of the verb in brackets (1 mark each)**

1. The quality of these shoes ____ very good. (be — present) <span class="marks">[1]</span>
2. One of my cousins ____ in Australia. (live) <span class="marks">[1]</span>
3. Neither of the two candidates ____ the required marks. (have) <span class="marks">[1]</span>
4. Mathematics ____ always been my favourite subject. (have) <span class="marks">[1]</span>
5. The police ____ still looking for the missing girl. (be — present) <span class="marks">[1]</span>
6. Twenty thousand rupees ____ a large sum for a student. (be — present) <span class="marks">[1]</span>
7. Either the manager or his assistants ____ to attend the meeting. (have) <span class="marks">[1]</span>
8. A number of houses ____ damaged by the landslide. (be — past) <span class="marks">[1]</span>
9. The number of road accidents ____ rising every year. (be — present) <span class="marks">[1]</span>
10. Each of the participants ____ given a certificate. (be — past) <span class="marks">[1]</span>

::: note Answers
**1.** is — the subject is *the quality*, not *shoes*.
**2.** lives — the subject is *one*, which is singular.
**3.** has — *neither of* takes a singular verb.
**4.** has — *mathematics* is singular in spite of the -s.
**5.** are — *police* is a plural noun.
**6.** is — a sum of money treated as one amount is singular.
**7.** have — the proximity rule: *his assistants* stands nearer.
**8.** were — *a number of* + plural noun takes a plural verb.
**9.** is — *the number of* takes a singular verb.
**10.** was — *each of* is singular.
:::

**Correct the errors in the following sentences (1 mark each)**

11. The list of selected candidates have been published. <span class="marks">[1]</span>
12. Hari as well as his brothers were invited to the wedding. <span class="marks">[1]</span>
13. There is many reasons for this failure. <span class="marks">[1]</span>
14. These kind of questions are asked every year. <span class="marks">[1]</span>
15. Ten kilometres are not a short distance. <span class="marks">[1]</span>
16. Every boy and every girl were given a school bag. <span class="marks">[1]</span>
17. He is one of the students who has topped the district. <span class="marks">[1]</span>
18. The committee have announced their decision unanimously. <span class="marks">[1]</span>
19. Each of the girls have brought her own lunch. <span class="marks">[1]</span>
20. My trousers is too tight for me now. <span class="marks">[1]</span>

::: note Answers
**11.** The list of selected candidates **has** been published. — the subject is *the list*.
**12.** Hari as well as his brothers **was** invited … — *as well as* does not make the subject plural.
**13.** There **are** many reasons for this failure. — the verb agrees with *reasons*.
**14.** **These kinds** of questions are asked every year. — *these* needs a plural noun.
**15.** Ten kilometres **is** not a short distance. — one distance, so a singular verb.
**16.** Every boy and every girl **was** given a school bag. — *every … and every …* stays singular.
**17.** He is one of the students who **have** topped the district. — the clause describes *students*.
**18.** The committee **has** announced **its** decision unanimously. — acting as one body, and *unanimously* shows it.
**19.** Each of the girls **has** brought her own lunch. — *each of* is singular.
**20.** My trousers **are** too tight for me now. — *trousers* is a plural noun.
:::

**Rewrite as instructed (1 mark each)**

21. *The teachers and the principal were present.* — Rewrite beginning *Not only the teachers but also …* <span class="marks">[1]</span>
22. *All the students have paid the fee.* — Rewrite beginning *Each …* <span class="marks">[1]</span>
23. *There are two temples and a pond in the village.* — Rewrite beginning *There … a pond and …* <span class="marks">[1]</span>
24. *Both the answers are wrong.* — Rewrite beginning *Neither …* <span class="marks">[1]</span>
25. *Politics does not interest him.* — Rewrite beginning *He …* <span class="marks">[1]</span>

::: note Answers
**21.** **Not only the teachers but also the principal was present.** — the proximity rule makes the verb singular.
**22.** **Each of the students has paid the fee.** — *each of* + plural noun + singular verb.
**23.** **There is a pond and two temples in the village.** — with a mixed list the verb follows the nearer noun.
**24.** **Neither of the answers is correct.** — *neither of* + plural noun takes a singular verb.
**25.** **He is not interested in politics.** — *politics* stays singular whichever way the sentence is turned.
:::
