---
subject: Compulsory English
grade: 12
unit: 29
title: Passive Voice
hours: 4
area: Grammar
---

A verb is in the **active voice** when the subject performs the action — *The
gardener planted the roses* — and in the **passive voice** when the subject
receives it — *The roses were planted by the gardener*. The passive is not a
decoration. English uses it whenever the doer is unknown, obvious, unimportant or
deliberately hidden: *My bicycle **has been stolen**. Rice **is grown** in the
Terai. Applications **must be submitted** by Friday.* Notices, rules, reports and
scientific writing run on it, which is why Q7 tests it and why every formal letter
you write in Q10 will need it.

::: key The three moves
1. The **object** of the active sentence becomes the **subject** of the passive.
2. The verb becomes **be + past participle**, and *be* is put into **the same
   tense** as the active verb.
3. The old subject becomes the **agent** with **by** — and is dropped whenever it
   is unknown, obvious or unimportant.

Only a verb that has an object (a **transitive** verb) can be made passive.
:::

## 29.1 The transformation

```figure caption="The three moves. The object crosses over to become the subject, the old subject becomes the by-agent, and the verb is rebuilt as be + past participle in the original tense."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,4.2))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
GREEN="#0B6A62"; AMBER="#B4690E"
top=[(1.35,2.60,"SUBJECT","The gardener",ACCENT),
     (4.15,2.50,"VERB","planted",AMBER),
     (6.85,3.00,"OBJECT","the roses",GREEN)]
bot=[(1.35,2.60,"SUBJECT","The roses",GREEN),
     (4.15,2.50,"be + V3","were planted",AMBER),
     (6.85,3.00,"AGENT","by the gardener",ACCENT)]
for x,w,lab,txt,col in top:
    ax.add_patch(FancyBboxPatch((x,7.95),w,1.05,boxstyle="round,pad=0.07",
                                fc="#ffffff",ec=col,lw=1.0))
    ax.text(x+w/2,8.72,lab,ha='center',va='center',fontsize=6.2,color=col)
    ax.text(x+w/2,8.27,txt,ha='center',va='center',fontsize=7.1,color=INK)
for x,w,lab,txt,col in bot:
    ax.add_patch(FancyBboxPatch((x,3.15),w,1.05,boxstyle="round,pad=0.07",
                                fc="#ffffff",ec=col,lw=1.0))
    ax.text(x+w/2,3.92,lab,ha='center',va='center',fontsize=6.2,color=col)
    ax.text(x+w/2,3.47,txt,ha='center',va='center',fontsize=7.1,color=INK)
ax.annotate("",xy=(8.35,4.45),xytext=(2.65,7.80),
            arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.0,
                            connectionstyle="arc3,rad=0.20"))
ax.annotate("",xy=(2.65,4.45),xytext=(8.35,7.80),
            arrowprops=dict(arrowstyle="-|>",color=GREEN,lw=1.0,
                            connectionstyle="arc3,rad=0.20"))
ax.text(0.55,8.48,"ACTIVE",rotation=90,ha='center',va='center',fontsize=6.6,color=MUTED)
ax.text(0.55,3.68,"PASSIVE",rotation=90,ha='center',va='center',fontsize=6.6,color=MUTED)
ax.plot([0.15,9.85],[2.65,2.65],color=GRID,lw=0.9)
ax.text(0.15,2.05,"be takes the tense the active verb had:",fontsize=6.9,color=MUTED,ha='left')
ax.text(0.15,1.40,"plants → is planted · is planting → is being planted",
        fontsize=6.9,color=INK,ha='left')
ax.text(0.15,0.75,"has planted → has been planted · will plant → will be planted",
        fontsize=6.9,color=INK,ha='left')
ax.text(0.15,0.10,"drop by + agent when it is unknown, obvious or unimportant",
        fontsize=6.9,color=MUTED,ha='left')
```

## 29.2 The passive of every tense

| Tense | Active | Passive |
|---|---|---|
| Simple present | *He **writes** a letter.* | *A letter **is written** by him.* |
| Present continuous | *He **is writing** a letter.* | *A letter **is being written** by him.* |
| Present perfect | *He **has written** a letter.* | *A letter **has been written** by him.* |
| Simple past | *He **wrote** a letter.* | *A letter **was written** by him.* |
| Past continuous | *He **was writing** a letter.* | *A letter **was being written** by him.* |
| Past perfect | *He **had written** a letter.* | *A letter **had been written** by him.* |
| Simple future | *He **will write** a letter.* | *A letter **will be written** by him.* |
| Future perfect | *He **will have written** a letter.* | *A letter **will have been written** by him.* |
| *going to* | *He **is going to write** a letter.* | *A letter **is going to be written** by him.* |
| Modal | *He **must write** a letter.* | *A letter **must be written** by him.* |
| Perfect modal | *He **must have written** a letter.* | *A letter **must have been written** by him.* |
| Infinitive | *He wants **to write** a letter.* | *He wants a letter **to be written**.* |
| Gerund | *I remember **writing** it.* | *I remember **its being written**.* |

**Four tenses have no ordinary passive**: present perfect continuous, past perfect
continuous, future continuous and future perfect continuous. *The mechanic has
been repairing the car* is simply left in the active.

::: caution Five passive errors
✗ *A letter **has written** by him.* → ✓ *…**has been written**…* (the *be* cannot
be dropped)
✗ *The window **was broke**.* → ✓ *The window **was broken**.* (past participle,
not past tense)
✗ *He **was died** last year.* → ✓ *He **died** last year.* (*die* is
intransitive — no passive)
✗ *The matter **was discussed about** in the meeting.* → ✓ *The matter **was
discussed** in the meeting.*
✗ *The letter was written **by a pen**.* → ✓ *…**with** a pen.* (*by* = the doer,
*with* = the instrument)
:::

```photo id="eng12/passive-sign" caption="A passive in public service. VIOLATORS WILL BE PROSECUTED is will + be + past participle — the future passive. The agent (the police, the courts, the owner) is deliberately left out, because a warning is stronger when nobody in particular has to be named." width="80"
crop 0.28 0.32 0.68 0.72
```

## 29.3 Verbs with two objects

*Give, send, offer, teach, tell, show, lend, pay, promise, hand* and *award* take
an indirect object (a person) and a direct object (a thing), so each of them has
**two** possible passives. English prefers the one that begins with the person.

| Active | Passive 1 (person first — preferred) | Passive 2 (thing first) |
|---|---|---|
| *They gave **me a prize**.* | *I **was given** a prize.* | *A prize **was given to me**.* |
| *He taught **the boys English**.* | *The boys **were taught** English.* | *English **was taught to** the boys.* |
| *She sent **him a card**.* | *He **was sent** a card.* | *A card **was sent to** him.* |

With *buy, make, get, cook, find, order* the second passive takes **for**:
*He bought **his sister a watch**.* → *A watch **was bought for** his sister.*

## 29.4 Imperatives, infinitives and impersonal passives

### Imperative sentences

| Active | Passive |
|---|---|
| *Open the door.* | ***Let** the door **be opened**.* / *You **are requested to** open the door.* |
| *Post this letter.* | ***Let** this letter **be posted**.* |
| *Do not touch the wires.* | ***Let not** the wires **be touched**.* / *You **are warned not to** touch the wires.* |
| *Please help the poor.* | *You **are requested to** help the poor.* |
| *Work hard.* | *You **are advised to** work hard.* |

### *make, let, see, hear, help*

In the active these verbs take a bare infinitive; in the passive the **to**
reappears.

| Active | Passive |
|---|---|
| *They **made** him **work** overtime.* | *He **was made to work** overtime.* |
| *They **let** him **go**.* | *He **was allowed to go**.* |
| *I **saw** him **enter** the shop.* | *He **was seen to enter** the shop.* |
| *We **heard** her **sing**.* | *She **was heard to sing**.* |
| *They **helped** me **carry** the box.* | *I **was helped to carry** the box.* |

### Impersonal passives: *It is said that …*

```figure caption="Two routes out of an impersonal active. Keep the that-clause and open with It, or lift the inner subject to the front and turn its verb into an infinitive."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.8))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
GREEN="#0B6A62"; AMBER="#B4690E"
ax.add_patch(FancyBboxPatch((2.20,8.00),5.60,1.20,boxstyle="round,pad=0.07",
                            fc="#ffffff",ec=MUTED,lw=1.0))
ax.text(5.00,8.88,"ACTIVE",ha='center',va='center',fontsize=6.2,color=MUTED)
ax.text(5.00,8.38,"People say that he is honest.",ha='center',va='center',
        fontsize=7.1,color=INK)
ax.annotate("",xy=(2.50,6.20),xytext=(4.10,7.90),
            arrowprops=dict(arrowstyle="-|>",color=GREEN,lw=1.0))
ax.annotate("",xy=(7.50,6.20),xytext=(5.90,7.90),
            arrowprops=dict(arrowstyle="-|>",color=AMBER,lw=1.0))
ax.add_patch(FancyBboxPatch((0.15,4.60),4.70,1.45,boxstyle="round,pad=0.07",
                            fc="#ffffff",ec=GREEN,lw=1.0))
ax.text(2.50,5.65,"ROUTE 1  ·  keep the clause",ha='center',va='center',
        fontsize=6.3,color=GREEN)
ax.text(2.50,5.05,"It is said that he is honest.",ha='center',va='center',
        fontsize=7.0,color=INK)
ax.add_patch(FancyBboxPatch((5.15,4.60),4.70,1.45,boxstyle="round,pad=0.07",
                            fc="#ffffff",ec=AMBER,lw=1.0))
ax.text(7.50,5.65,"ROUTE 2  ·  raise the subject",ha='center',va='center',
        fontsize=6.3,color=AMBER)
ax.text(7.50,5.05,"He is said to be honest.",ha='center',va='center',
        fontsize=7.0,color=INK)
ax.plot([0.15,9.85],[4.05,4.05],color=GRID,lw=0.9)
ax.text(0.15,3.45,"say · believe · think · report · know · consider · suppose",
        fontsize=6.8,color=MUTED,ha='left')
ax.text(0.15,2.70,"if the inner clause is PRESENT  →  to + base verb",
        fontsize=6.8,color=INK,ha='left')
ax.text(0.15,2.05,"He is said to be honest.",fontsize=6.8,color=AMBER,ha='left')
ax.text(0.15,1.30,"if the inner clause is PAST  →  to have + past participle",
        fontsize=6.8,color=INK,ha='left')
ax.text(0.15,0.65,"He is said to have left the country.",
        fontsize=6.8,color=AMBER,ha='left')
```

| Active | Route 1 | Route 2 |
|---|---|---|
| *People believe that she is innocent.* | *It is believed that she is innocent.* | *She is believed to be innocent.* |
| *They report that the bridge collapsed.* | *It is reported that the bridge collapsed.* | *The bridge is reported to have collapsed.* |
| *Everyone knows that he works hard.* | *It is known that he works hard.* | *He is known to work hard.* |

## 29.5 Questions, prepositional verbs and verbs with no passive

**Questions.** Convert the sentence first, then put it back into question form.

| Active | Passive |
|---|---|
| *Did he write the letter?* | ***Was** the letter **written** by him?* |
| *Has she paid the bill?* | ***Has** the bill **been paid** by her?* |
| *Who broke the window?* | ***By whom was** the window **broken**?* |
| *What did they discuss?* | ***What was discussed** by them?* |
| *Why did the police arrest him?* | ***Why was** he **arrested** by the police?* |

**Prepositional verbs keep their preposition.** It stays attached to the verb even
though its object has moved to the front.

| Active | Passive |
|---|---|
| *They laughed **at** him.* | *He was laughed **at**.* |
| *Somebody must look **after** the baby.* | *The baby must be looked **after**.* |
| *They sent **for** the doctor.* | *The doctor was sent **for**.* |
| *The surgeon operated **on** him.* | *He was operated **on**.* |
| *Nobody listened **to** her.* | *She was not listened **to**.* |

**Verbs that have no passive.**

| Group | Examples |
|---|---|
| Intransitive verbs | *come, go, die, sleep, arrive, happen, occur, rise, fall, laugh* |
| Stative verbs | *have* (= possess), *resemble, lack, suit, fit, become* (= suit), *hold* (= contain), *cost, weigh, mean* |
| Reflexive and reciprocal objects | *He hurt **himself**.* · *They know **each other**.* |

✗ *The accident **was happened** at midnight.* → ✓ *The accident **happened** at
midnight.*
✗ *This shirt **is suited** you.* → ✓ *This shirt **suits** you.*

**Prepositions other than *by*.** A few passive participles take a fixed
preposition: *known **to**, pleased **with**, surprised **at**, filled **with**,
covered **with**, crowded **with**, contained **in**, interested **in**, tired
**of**, annoyed **with**.*
*The hall was **crowded with** students.* *He is **known to** everyone here.*

## 29.6 Choosing the voice

Changing voice is an exercise; choosing one is a skill, and the writing questions
reward it. Prefer the **active** as your normal setting — it is shorter and
clearer — and switch to the **passive** for one of these six reasons.

| Reason | Example |
|---|---|
| The doer is **unknown** | *My purse **was stolen** in the bus.* |
| The doer is **obvious** | *The thief **was arrested** yesterday.* (by the police — who else?) |
| The doer is **unimportant**, as in a process | *The tea leaves **are plucked**, dried and then **packed**.* |
| A **rule or notice** applies to everybody | *Mobile phones **must be switched off** inside the hall.* |
| The **receiver** is the real topic | *The Dharahara **was rebuilt** after the earthquake.* |
| The writer wants to be **impersonal** | *It **has been decided** that the examination will be postponed.* |

Notice the last one. *We have decided* names a decision-maker; *It has been
decided* does not. That is exactly why official Nepali English — circulars,
notices, minutes — is full of passives, and why the same habit makes student
essays sound heavy when it is used everywhere. Use the passive because you have a
reason, not out of formality.

**Keep the agent only when it carries information.** *Hamlet **was written by
Shakespeare*** needs the agent; *The road **was repaired by workers*** does not,
because no reader expected anyone else.

::: example Worked item 29.1 — a continuous tense with a double object
**Problem.** Change into the passive: *The principal was giving the students
certificates.*

**Solution — step by step.**

1. **Find the verb and its tense.** *was giving* — past continuous, so the passive
   frame is *was / were **being** + past participle*.
2. **Find the objects.** Indirect object *the students* (person), direct object
   *certificates* (thing).
3. **Prefer the person as the new subject.** *The students* is plural, so *be*
   becomes *were*.
4. **Assemble**: *The students were being given certificates by the principal.*
5. **The alternative** starts with the thing and keeps *to*: *Certificates were
   being given to the students by the principal.*

**Answer.** ***The students were being given certificates by the principal.***
:::

::: example Worked item 29.2 — an imperative and a prepositional verb
**Problem.** Change into the passive: *(a) Shut all the windows before you leave.
(b) They have already dealt with the complaint.*

**Solution — step by step.**

1. **(a)** This is a command. The standard passive of an imperative is *Let +
   object + be + past participle*. The subordinate clause *before you leave* has
   its own subject and is left untouched.
   **Answer:** ***Let all the windows be shut before you leave.*** (Also
   acceptable: *You are requested to shut all the windows before you leave.*)
2. **(b)** *deal with* is a prepositional verb; *the complaint* is its object.
   The tense is present perfect, so the frame is *has / have **been** + V3*. The
   preposition *with* stays at the end.
   **Answer:** ***The complaint has already been dealt with.***
:::

::: example Worked item 29.3 — the impersonal passive
**Problem.** Rewrite in two ways: *People say that the old temple was built in the
twelfth century.*

**Solution — apply the two routes.**

1. **Route 1** keeps the that-clause and supplies the empty subject *it*: *It is
   said that the old temple was built in the twelfth century.*
2. **Route 2** raises the inner subject *the old temple* to the front. Its verb
   *was built* is **past** relative to *is said*, so the infinitive must be the
   perfect passive infinitive **to have been built**.
3. Note that the inner verb here is itself passive, which is why the form is *to
   have been built* and not *to have built*.

**Answer.** *(i) **It is said that the old temple was built in the twelfth
century.** (ii) **The old temple is said to have been built in the twelfth
century.***
:::

## Chapter summary

- Passive = **be + past participle**, with *be* carrying the tense of the original
  verb; only transitive verbs have a passive.
- The object becomes the subject; the subject becomes the *by*-agent, and the
  agent is dropped when it is unknown, obvious or unimportant.
- Present perfect continuous, past perfect continuous, future continuous and
  future perfect continuous have no ordinary passive.
- Modals: *must be done*, *can be seen*, *should have been finished*.
- Two-object verbs give two passives; the one beginning with the person is
  preferred, and the other inserts *to* (or *for* with *buy, make, cook*).
- Imperatives become *Let + object + be + V3*, or *You are requested / advised /
  warned to …*
- *make, let, see, hear, help* take a bare infinitive in the active but *to* in the
  passive: *He was made to wait.*
- Impersonal actives give *It is said that …* or *He is said to be / to have
  been …*
- A prepositional verb keeps its preposition: *The baby was looked after.*
- *by* marks the doer, *with* the instrument; *die, happen, arrive, resemble,
  suit, lack* have no passive at all.

## Practice questions

**Change into the passive voice (1 mark each)**

1. The postman delivers the letters every morning. <span class="marks">[1]</span>
2. They are repairing the road near our school. <span class="marks">[1]</span>
3. Someone has stolen my bicycle. <span class="marks">[1]</span>
4. The committee will announce the results tomorrow. <span class="marks">[1]</span>
5. You must submit the application before Friday. <span class="marks">[1]</span>
6. The teacher gave Sita a prize. <span class="marks">[1]</span>
7. Shut the gate at once. <span class="marks">[1]</span>
8. Who wrote this poem? <span class="marks">[1]</span>
9. They made him sign the paper. <span class="marks">[1]</span>
10. The villagers are looking after the orphans. <span class="marks">[1]</span>

::: note Answers
**1.** **The letters are delivered (by the postman) every morning.** — simple present: *are* + V3.
**2.** **The road near our school is being repaired.** — present continuous: *is being* + V3; the vague agent *they* is dropped.
**3.** **My bicycle has been stolen.** — present perfect; *someone* is unknown, so no agent.
**4.** **The results will be announced by the committee tomorrow.** — future: *will be* + V3.
**5.** **The application must be submitted before Friday.** — modal: *must be* + V3.
**6.** **Sita was given a prize by the teacher.** (or *A prize was given to Sita by the teacher.*) — the person-first passive is preferred.
**7.** **Let the gate be shut at once.** — imperative passive.
**8.** **By whom was this poem written?** — *who* becomes *by whom* and the auxiliary follows it.
**9.** **He was made to sign the paper.** — *make* takes *to* in the passive.
**10.** **The orphans are being looked after by the villagers.** — the preposition *after* stays with the verb.
:::

**Change into the active voice (1 mark each)**

11. The window was broken by the boys. <span class="marks">[1]</span>
12. A new hospital is going to be built here. <span class="marks">[1]</span>
13. Let the lights be switched off. <span class="marks">[1]</span>
14. He is said to be very generous. <span class="marks">[1]</span>

::: note Answers
**11.** **The boys broke the window.** — the agent becomes the subject.
**12.** **They are going to build a new hospital here.** — supply a general subject when no agent is given.
**13.** **Switch off the lights.** — *Let … be* + V3 is the passive of an imperative.
**14.** **People say that he is very generous.** — Route 2 reversed.
:::

**Correct the errors (1 mark each)**

15. The letter has written by the secretary. <span class="marks">[1]</span>
16. He was died in a road accident. <span class="marks">[1]</span>
17. The problem was discussed about for two hours. <span class="marks">[1]</span>
18. The glass was broke by the cat. <span class="marks">[1]</span>
19. The poem was written by a blue pen. <span class="marks">[1]</span>
20. The hall was crowded by students. <span class="marks">[1]</span>

::: note Answers
**15.** The letter **has been written** by the secretary. — the passive needs *been*.
**16.** He **died** in a road accident. — *die* is intransitive and has no passive.
**17.** The problem **was discussed** for two hours. — *discuss* takes no *about*.
**18.** The glass **was broken** by the cat. — past participle, not past tense.
**19.** The poem was written **with** a blue pen. — *with* marks the instrument.
**20.** The hall was crowded **with** students. — *crowded* takes *with*.
:::
