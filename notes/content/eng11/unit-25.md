---
subject: Compulsory English
grade: 11
unit: 25
title: Passive Voice and Causatives
hours: 4
area: Grammar
---

**Voice** tells you whether the subject of the sentence *does* the action or
*receives* it. In the active voice the doer is the subject (*The committee
approved the plan*); in the passive the receiver becomes the subject (*The plan was
approved by the committee*). NEB Q7 almost always contains one voice item, phrased
"Change into passive voice" or "Change into active voice". Causatives — *get the
house painted*, *have my hair cut* — are the passive's close relative and are
tested in the same question.

::: key The passive is only possible with a transitive verb
A verb with no object has nothing to promote to subject. *He slept*, *She arrived*,
*The baby laughed* have **no passive form**. If a question asks you to make an
intransitive sentence passive, the answer is that it cannot be done.
:::

## 25.1 The five steps of the transformation

```figure caption="Active to passive in five moves. The object of the active sentence becomes the subject of the passive, the verb becomes *be* + past participle in the same tense, and the old subject becomes the agent after *by*."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.2))
ax.set_xlim(0,10); ax.set_ylim(0,8.6); ax.axis('off')
def chip(x,y,w,t,c,fc,fs=8.4):
    ax.add_patch(FancyBboxPatch((x,y),w,0.95,boxstyle="round,pad=0.10",
                                fc=fc, ec=c, lw=1.1))
    ax.text(x+w/2,y+0.475,t,ha='center',va='center',fontsize=fs,color=c)
# active row
ax.text(0.1,7.9,"ACTIVE",fontsize=8.2,color=MUTED,ha='left',va='center')
chip(0.6,6.7,2.6,"The farmers",'#0B6A62',"#eef7f1")
chip(3.6,6.7,2.0,"planted",ACCENT,"#eaf0fb")
chip(6.0,6.7,3.4,"the paddy",'#B4690E',"#fdf1e7")
# passive row
ax.text(0.1,2.6,"PASSIVE",fontsize=8.2,color=MUTED,ha='left',va='center')
chip(0.6,1.4,2.6,"The paddy",'#B4690E',"#fdf1e7")
chip(3.6,1.4,2.6,"was planted",ACCENT,"#eaf0fb")
chip(6.6,1.4,2.8,"by the farmers",'#0B6A62',"#eef7f1")
# swap arrows
ax.annotate('',xy=(1.9,2.45),xytext=(7.7,6.6),
            arrowprops=dict(arrowstyle='-|>',color='#B4690E',lw=1.2,
                            mutation_scale=10,connectionstyle="arc3,rad=0.22"))
ax.annotate('',xy=(8.0,2.45),xytext=(1.9,6.6),
            arrowprops=dict(arrowstyle='-|>',color='#0B6A62',lw=1.2,
                            mutation_scale=10,connectionstyle="arc3,rad=0.22"))
ax.annotate('',xy=(4.9,2.45),xytext=(4.6,6.6),
            arrowprops=dict(arrowstyle='-|>',color=ACCENT,lw=1.2,mutation_scale=10))
ax.text(3.15,4.55,"object → subject",fontsize=7.4,color='#B4690E',ha='right',
        va='center')
ax.text(6.85,4.55,"subject → agent",fontsize=7.4,color='#0B6A62',ha='left',
        va='center')
ax.text(5.05,4.95,"V2 → was + V3",fontsize=7.4,color=ACCENT,ha='left',va='center')
ax.text(5.0,0.45,"the agent may be dropped when it is unknown, obvious or unimportant",
        fontsize=7.4,color=MUTED,ha='center',va='center')
```

1. **Find the object of the active sentence.** Ask *what?* or *whom?* after the
   verb. No object means no passive.
2. **Move that object to the front** and make it the subject. Change its case if it
   is a pronoun: *me → I*, *him → he*, *them → they*.
3. **Change the verb to the matching form of *be* + the past participle (V3).** The
   *be* keeps the **tense and number of the original verb** — the tense never
   changes in a voice transformation.
4. **Move the old subject to the end after *by***, changing its case: *I → by me*,
   *she → by her*, *we → by us*.
5. **Decide whether to drop the agent.** Leave out *by …* when the doer is
   unknown (*My purse was stolen*), obvious (*The thief was arrested*), or a vague
   *people / they / somebody* (*Nepali is spoken here*).

## 25.2 The passive of every tense

Take the active sentence *They repair the road* and run it through all twelve
tenses. **S** is the new subject.

| Tense | Active | Passive structure | Passive example |
|---|---|---|---|
| Simple present | They repair the road. | S + am/is/are + V3 | The road **is repaired**. |
| Present continuous | They are repairing the road. | S + am/is/are + being + V3 | The road **is being repaired**. |
| Present perfect | They have repaired the road. | S + have/has + been + V3 | The road **has been repaired**. |
| Present perfect continuous | They have been repairing the road. | — | **no passive form in normal use** |
| Simple past | They repaired the road. | S + was/were + V3 | The road **was repaired**. |
| Past continuous | They were repairing the road. | S + was/were + being + V3 | The road **was being repaired**. |
| Past perfect | They had repaired the road. | S + had + been + V3 | The road **had been repaired**. |
| Past perfect continuous | They had been repairing the road. | — | **no passive form in normal use** |
| Simple future | They will repair the road. | S + will + be + V3 | The road **will be repaired**. |
| Future continuous | They will be repairing the road. | — | **no passive form in normal use** |
| Future perfect | They will have repaired the road. | S + will + have been + V3 | The road **will have been repaired**. |
| Future perfect continuous | They will have been repairing the road. | — | **no passive form in normal use** |

::: caution The four tenses with no passive
The **perfect continuous** tenses (present, past, future) and the **future
continuous** have no passive in ordinary English, because forms such as *has been
being repaired* are too clumsy to use. If an exam sentence is in one of these
tenses, either the question is faulty or you are expected to shift it to the
matching simple or perfect passive. Never invent *will be being written*.
:::

## 25.3 Modals, infinitives and gerunds in the passive

| Active pattern | Passive pattern | Example |
|---|---|---|
| modal + V1 | modal + be + V3 | You must submit the form. → The form **must be submitted**. |
| modal + have + V3 | modal + have been + V3 | She should have paid it. → It **should have been paid**. |
| to + V1 | to be + V3 | He wants to invite her. → She wants **to be invited**. |
| V-ing | being + V3 | I like people praising my work. → I like my work **being praised**. |
| have to / used to / going to | + be + V3 | We have to finish it. → It **has to be finished**. |

## 25.4 Verbs with two objects

Verbs such as *give, send, offer, teach, tell, show, lend, pay, promise, buy,
bring* take an **indirect object** (a person) and a **direct object** (a thing).
Either can become the subject, so two passives are possible — and the person one is
the more natural.

**Active:** *The principal gave Sarita a certificate.*

- **Passive 1 (person first):** *Sarita **was given** a certificate by the
  principal.*
- **Passive 2 (thing first):** *A certificate **was given to** Sarita by the
  principal.*

Note that when the thing becomes the subject, the person needs **to** (or **for**
with *buy, make, get*): *A new bag was bought **for** the child.*

## 25.5 Questions, imperatives and other special sentences

| Active type | Rule | Example |
|---|---|---|
| Yes/no question | Begin the passive with the auxiliary | Did he write the letter? → **Was** the letter **written** by him? |
| Wh- question (object) | Keep the wh- word first | What did you buy? → What **was bought** by you? |
| *Who* as subject | *Who* becomes *By whom* | Who broke the window? → **By whom was** the window **broken**? |
| *Whom* as object | *Whom* becomes *Who* | Whom did they select? → **Who was selected** by them? |
| Imperative (order) | Let + object + be + V3 | Shut the door. → **Let the door be shut.** |
| Imperative (request) | You are requested to… | Please help me. → **You are requested to help me.** |
| Imperative (advice) | Should / must be + V3 | Do not waste water. → Water **should not be wasted.** |
| *Let* + object | Let + object + be + V3 | Let him do it. → **Let it be done by him.** |

**The impersonal passive.** Sentences beginning *People say / They believe /
Everyone knows* have two standard passives:

*People say that he is very rich.*
→ **It is said that he is very rich.**
→ **He is said to be very rich.**

If the that-clause is in an earlier tense, the second form uses *to have* + V3:
*People believe that she wrote the letter* → **She is believed to have written the
letter.**

## 25.6 When and why the passive is used

- The doer is **unknown**: *Three motorcycles **were stolen** from the parking lot.*
- The doer is **obvious or unimportant**: *The suspect **was released** on bail.*
- The **receiver matters more** than the doer: *Nepal **was struck** by a major
  earthquake in 2015.*
- **Formal, scientific and official writing**, where the process matters more than
  the person: *The sample **was heated** to 80 °C.* *Applications **must be
  submitted** by Chaitra 15.*
- **Notices and rules**: *Visitors **are requested** not to feed the animals.*

::: caution Don't change the tense, and don't lose the agent's case
Two errors cost most of the marks in this question.
(i) ~~The letter is written by him yesterday~~ → **was written** — the tense of the
original must survive.
(ii) ~~The song was sung by she~~ → **by her** — after *by* the pronoun takes the
object form (*me, us, him, her, them, whom*).
Also keep the number right: *The books **were** kept*, not ~~was kept~~.
:::

## 25.7 Causative verbs

A **causative** says that the subject *arranges* for something to be done rather
than doing it personally. There are two families.

**Family 1 — causing a thing to be done (the passive causative).**

| Structure | Meaning | Example |
|---|---|---|
| have + object + V3 | arrange a service, neutral | I **had** my bike **serviced** at Balaju. |
| get + object + V3 | the same, more informal; also "manage to" | She **got** her passport **renewed**. |
| get / have + object + V3 | something unpleasant that happened to you | He **had** his phone **stolen** in the bus. |
| want / need + object + V3 | a need | We **need** the roof **repaired** before Shrawan. |

The word order is fixed: **have/get + the thing + past participle**.
~~I had cut my hair~~ (= I cut it myself) is different from *I **had my hair
cut*** (= the barber cut it).

**Family 2 — causing a person to act.**

| Structure | Meaning | Example |
|---|---|---|
| make + person + **V1** | force, compel | The teacher **made** us **rewrite** the essay. |
| let + person + **V1** | allow | My father **let** me **use** his laptop. |
| have + person + **V1** | give an instruction to someone under you | I **had** the tailor **shorten** the trousers. |
| get + person + **to** + V1 | persuade | She **got** her brother **to drive** her to Kalanki. |
| help + person + (to) + V1 | help; *to* is optional | He **helped** me **carry** the sack. |

```figure caption="The two causative word orders. When the middle slot is a **thing**, the verb goes into the past participle; when it is a **person**, the verb stays in the base form (and *get* alone needs *to*)."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,3.1))
ax.set_xlim(0,10); ax.set_ylim(0,8.8); ax.axis('off')
def slot(x,y,w,t,c,fc,fs=8.4):
    ax.add_patch(FancyBboxPatch((x,y),w,0.95,boxstyle="round,pad=0.09",
                                fc=fc,ec=c,lw=1.0))
    ax.text(x+w/2,y+0.475,t,ha='center',va='center',fontsize=fs,color=c)
def row(y, head, a, b, cvb, ex):
    ax.text(0.15, y+2.05, head, fontsize=8.0, color=INK, ha='left', va='center')
    slot(0.25, y+0.6, 2.85, a[0], ACCENT, "#eaf0fb", 8.0)
    slot(3.35, y+0.6, 3.0, a[1], a[2], a[3])
    slot(6.6, y+0.6, 3.15, b, cvb[0], cvb[1])
    ax.text(5.0, y-0.1, ex, fontsize=7.4, color=MUTED, ha='center', va='center',
            style='italic')
row(5.0, "THING in the middle  →  past participle (V3)",
    ("have / get", "my hair", '#B4690E', "#fdf1e7"), "cut  (V3)",
    ('#0B6A62', "#eef7f1"),
    "I had my hair cut at Baneshwor.   /   She got her passport renewed.")
row(1.0, "PERSON in the middle  →  base form (V1)",
    ("make / let / have", "the tailor", '#A8271F', "#fbeceb"), "shorten  (V1)",
    ('#0B6A62', "#eef7f1"),
    "The teacher made us rewrite it.   /   She got her brother TO drive her.")
ax.plot([0.15,9.85],[4.35,4.35], color=GRID, lw=0.9)
```

::: caution *make* takes the bare infinitive in the active but *to* in the passive
Active: *They **made** him **sign** the paper.* (no *to*)
Passive: *He **was made to sign** the paper.* (*to* appears)
This reappearing *to* is a favourite exam trap. *Let* has no passive of its own;
use *be allowed to*: *He **was allowed to** go.*
:::

::: example Worked transformation 25.1 — active to passive, step by step
**Problem.** Change into the passive: *The municipality has cleared the garbage
from the riverbank.*

**Solution — the five steps.**

1. **Find the object.** *has cleared **what**?* → *the garbage from the riverbank*.
   The head of the object is *the garbage*.
2. **Move it to the front.** *The garbage from the riverbank …*
3. **Change the verb.** The active is **present perfect** (*has cleared*), so the
   passive is *have/has + been + V3*. The new subject *garbage* is singular →
   **has been cleared**.
4. **Attach the agent.** Old subject *the municipality* → *by the municipality*.
5. **Keep or drop the agent?** It is specific and informative, so keep it.

**Answer.** *The garbage **has been cleared** from the riverbank **by the
municipality**.*
:::

::: example Worked transformation 25.2 — passive of a question
**Problem.** Change into the passive: *Who wrote this poem?*

**Solution — step by step.**

1. **Identify the parts.** Subject = *Who*; verb = *wrote* (simple past); object =
   *this poem*.
2. **The object becomes the subject.** *This poem …*
3. **Change the verb.** Simple past → *was/were* + V3. *Poem* is singular →
   **was written**.
4. **The subject *who* becomes the agent.** After *by*, *who* becomes *whom*:
   *by whom*.
5. **Keep it a question.** A wh- question begins with the wh- element, so *By whom*
   comes first and the auxiliary comes before the subject.

**Answer.** ***By whom was this poem written?***

(*Who was this poem written by?* is the informal version and is also accepted.)
:::

::: example Worked transformation 25.3 — passive to active, and a causative
**Problem.** (a) Change into the active: *The injured were being carried to the
hospital by the volunteers.* (b) Rewrite using a causative: *A mechanic repaired my
scooter yesterday.*

**Solution.**

**(a)** 1. The agent *by the volunteers* becomes the subject → *The volunteers*.
2. The passive verb *were being carried* is **past continuous**, so the active is
*was/were* + V-ing → *were carrying*. 3. The passive subject *the injured* becomes
the object.
**Answer:** *The volunteers **were carrying** the injured to the hospital.*

**(b)** 1. The service was done for me by someone else, so use *have/get + object +
V3*. 2. The time is past, so *have* becomes *had*. 3. Order: *had* + *my scooter* +
*repaired*.
**Answer:** *I **had my scooter repaired** yesterday.* (Or *I **got** my scooter
**repaired** yesterday.*)
:::

## Chapter summary

- Passive = subject + correct form of **be** + **V3** (+ *by* + agent). Only
  transitive verbs have a passive.
- The tense never changes in a voice transformation; only the form of *be* does.
- Passive forms: is/are + V3 · is/are being + V3 · has/have been + V3 · was/were +
  V3 · was/were being + V3 · had been + V3 · will be + V3 · will have been + V3.
- The four **continuous-perfect** and **future continuous** tenses have no passive.
- Modals: modal + **be** + V3; past modals: modal + **have been** + V3.
- Verbs with two objects give two passives; the person-first one is more natural,
  and the thing-first one needs *to/for* before the person.
- Imperatives become *Let + object + be + V3*, or *You are requested to …*.
- *Who* → *By whom* in the passive question; pronouns after *by* take the object
  form.
- Causatives: *have/get + thing + V3* (a service), *make/let/have + person + V1*,
  *get + person + to + V1*. In the passive, *make* takes *to*.

## Practice questions

**Change the following sentences into the passive voice (1 mark each)**

1. The students of Grade 11 organised a blood donation programme. <span class="marks">[1]</span>
2. Sabina is writing an article for the school magazine. <span class="marks">[1]</span>
3. The government has banned single-use plastic in the valley. <span class="marks">[1]</span>
4. The flood had damaged three suspension bridges. <span class="marks">[1]</span>
5. They will announce the results next Sunday. <span class="marks">[1]</span>
6. You must return the library books by Friday. <span class="marks">[1]</span>
7. Close all the windows before you leave. <span class="marks">[1]</span>
8. Who broke this window? <span class="marks">[1]</span>
9. My uncle gave me a bicycle on my birthday. <span class="marks">[1]</span>
10. People say that Janakpur is the birthplace of Sita. <span class="marks">[1]</span>

::: note Answers
**1.** A blood donation programme **was organised** by the students of Grade 11. — simple past → was/were + V3.
**2.** An article **is being written** for the school magazine by Sabina. — present continuous → is being + V3.
**3.** Single-use plastic **has been banned** in the valley by the government. — present perfect → has been + V3.
**4.** Three suspension bridges **had been damaged** by the flood. — past perfect → had been + V3.
**5.** The results **will be announced** next Sunday. — the vague agent *they* is dropped.
**6.** The library books **must be returned** by Friday. — modal → modal + be + V3.
**7.** **Let all the windows be closed** before you leave. — an imperative order becomes *Let … be* + V3.
**8.** **By whom was this window broken?** — *who* becomes *by whom* and moves to the front.
**9.** I **was given** a bicycle by my uncle on my birthday. (or *A bicycle was given to me …*) — two objects, two passives.
**10.** **It is said that** Janakpur is the birthplace of Sita. (or *Janakpur **is said to be** the birthplace of Sita.*) — impersonal passive.
:::

**Change the following sentences into the active voice (1 mark each)**

11. The fields are ploughed by the oxen every Baisakh. <span class="marks">[1]</span>
12. A new health post is being built by the ward office. <span class="marks">[1]</span>
13. The thief had been caught by the neighbours before the police arrived. <span class="marks">[1]</span>
14. The report will have been submitted by the committee by Chaitra. <span class="marks">[1]</span>
15. Let the gate be locked at nine. <span class="marks">[1]</span>
16. By whom was this letter posted? <span class="marks">[1]</span>

::: note Answers
**11.** The oxen **plough** the fields every Baisakh. — is/are + V3 → simple present.
**12.** The ward office **is building** a new health post. — is being + V3 → present continuous.
**13.** The neighbours **had caught** the thief before the police arrived. — had been + V3 → past perfect.
**14.** The committee **will have submitted** the report by Chaitra. — will have been + V3 → future perfect.
**15.** **Lock** the gate at nine. — *Let … be* + V3 goes back to an imperative.
**16.** **Who posted this letter?** — *by whom* becomes the subject *who*.
:::

**Rewrite the following using a causative structure, or correct the error (1 mark each)**

17. A carpenter repaired our main door last week. — Rewrite with *had*. <span class="marks">[1]</span>
18. The barber is cutting Bibek's hair at the moment. — Rewrite with *is having*. <span class="marks">[1]</span>
19. Someone stole my wallet in the micro. — Rewrite with *had*. <span class="marks">[1]</span>
20. She persuaded her father to buy a laptop. — Rewrite with *got*. <span class="marks">[1]</span>
21. The teacher made us to copy the notes again. — Correct the error. <span class="marks">[1]</span>
22. We were made clean the whole classroom. — Correct the error. <span class="marks">[1]</span>
23. He was not let to enter the hall. — Correct the error. <span class="marks">[1]</span>
24. The road is repairing by the contractor these days. — Correct the error. <span class="marks">[1]</span>
25. The letter was wrote by my elder sister. — Correct the error. <span class="marks">[1]</span>
26. This song was sung by she at the Saraswati Puja programme. — Correct the error. <span class="marks">[1]</span>

::: note Answers
**17.** We **had our main door repaired** last week. — *have* + thing + V3.
**18.** Bibek **is having his hair cut** at the moment. — the causative in the present continuous.
**19.** I **had my wallet stolen** in the micro. — *have* + thing + V3 for something unpleasant.
**20.** She **got her father to buy** a laptop. — *get* + person + *to* + V1.
**21.** The teacher made us **copy** the notes again. — active *make* takes the bare infinitive.
**22.** We **were made to clean** the whole classroom. — passive *make* takes *to*.
**23.** He **was not allowed to enter** the hall. — *let* has no passive; use *be allowed to*.
**24.** The road **is being repaired** by the contractor these days. — the passive needs *being* + V3.
**25.** The letter was **written** by my elder sister. — the passive uses V3, not V2.
**26.** This song was sung by **her** … — a pronoun after *by* takes the object form.
:::
