---
subject: Compulsory English
grade: 11
unit: 26
title: Reported Speech
hours: 4
area: Grammar
---

**Direct speech** repeats a speaker's exact words inside quotation marks; **reported
(indirect) speech** puts those words into your own sentence with no quotation marks.
NEB Q7 sets one or two items every year, worded "Change into indirect speech" or
"Report the following sentence". The change is completely mechanical: pick the right
reporting verb, backshift the tense, change the pronouns, and change the words for
time and place. Do those four things in that order and the item cannot go wrong.

::: key The four changes, always in this order
**1. Reporting verb and link.** *said* / *told* / *asked* / *ordered* / *requested*
/ *exclaimed*, plus *that*, *if/whether*, a wh- word, or *to* + V1.
**2. Tense.** Shift the reported verb one step back into the past.
**3. Pronouns.** Change them to match the new speaker and listener.
**4. Words of time and place.** *now → then*, *today → that day*, *here → there*.
:::

## 26.1 The reporting verb and the link word

| Kind of sentence | Reporting verb | Link | Verb form in the reported clause |
|---|---|---|---|
| Statement | said / said to / told | that | finite verb, backshifted |
| Wh- question | asked / enquired | the same wh- word | finite verb, statement order |
| Yes/no question | asked / enquired | if / whether | finite verb, statement order |
| Command, order | ordered / told / commanded | — | **to** + V1 |
| Negative command | told / ordered / forbade | — | **not to** + V1 |
| Request | requested / asked | — | **to** + V1 |
| Advice, suggestion | advised / suggested | — | to + V1 / that … should |
| Exclamation | exclaimed with joy / sorrow / wonder | that | finite verb, backshifted |
| Wish, prayer | wished / prayed | that | finite verb, backshifted |

**said** and **told** are not interchangeable. *Told* must be followed by a person;
*said* must not be, unless you add *to*.

- *He **said that** he was tired.* ✔  *He **told me that** he was tired.* ✔
- *He **said to me that** he was tired.* ✔  ~~He **told that** he was tired.~~ ✘
- ~~He **said me that** he was tired.~~ ✘

When the reporting verb is in the **present, present perfect or future**
(*says, has said, will say*), you make **no tense change at all** — only pronouns
and, if needed, place words change.

*He says, "I am busy."* → *He says **that he is busy**.*

## 26.2 The complete backshift table

When the reporting verb is in the past (*said, told, asked*), every verb in the
reported clause moves one step further back in time.

```figure caption="Backshift as a ladder. Each present form steps down to the matching past form; the past forms step down once more to the perfect, and the past perfect has nowhere further to go, so it stays where it is."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,4.0))
ax.set_xlim(0,10); ax.set_ylim(0,12.4); ax.axis('off')
pairs = [
    ("simple present  (write / writes)", "simple past  (wrote)"),
    ("present continuous  (am writing)", "past continuous  (was writing)"),
    ("present perfect  (have written)", "past perfect  (had written)"),
    ("simple past  (wrote)", "past perfect  (had written)"),
    ("past continuous  (was writing)", "past perfect continuous"),
    ("will / shall  (will write)", "would  (would write)"),
    ("can / may / must", "could / might / had to"),
]
y0 = 11.1
for i, (a, b) in enumerate(pairs):
    y = y0 - i * 1.42
    ax.add_patch(FancyBboxPatch((0.1, y-0.42), 4.35, 0.88,
                                boxstyle="round,pad=0.08", fc="#eaf0fb",
                                ec=ACCENT, lw=0.9))
    ax.text(2.27, y, a, ha='center', va='center', fontsize=7.0, color=INK)
    ax.annotate('', xy=(5.45, y), xytext=(4.62, y),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0,
                                mutation_scale=8))
    ax.add_patch(FancyBboxPatch((5.6, y-0.42), 4.3, 0.88,
                                boxstyle="round,pad=0.08", fc="#eef7f1",
                                ec='#0B6A62', lw=0.9))
    ax.text(7.75, y, b, ha='center', va='center', fontsize=7.0, color=INK)
ylast = y0 - 7 * 1.42
ax.add_patch(FancyBboxPatch((0.1, ylast-0.42), 9.8, 0.88,
                            boxstyle="round,pad=0.08", fc="#f6f7f9",
                            ec=MUTED, lw=0.9))
ax.text(5.0, ylast, "past perfect  (had written)  —  does not change",
        ha='center', va='center', fontsize=7.6, color=INK)
ax.text(2.27, 12.05, "DIRECT", ha='center', va='center', fontsize=8.2, color=ACCENT)
ax.text(7.75, 12.05, "REPORTED", ha='center', va='center', fontsize=8.2,
        color='#0B6A62')
```

| Direct speech | Reported speech |
|---|---|
| simple present — *works* | simple past — *worked* |
| present continuous — *is working* | past continuous — *was working* |
| present perfect — *has worked* | past perfect — *had worked* |
| present perfect continuous — *has been working* | past perfect continuous — *had been working* |
| simple past — *worked* | past perfect — *had worked* |
| past continuous — *was working* | past perfect continuous — *had been working* |
| past perfect — *had worked* | past perfect — *had worked* (no change) |
| past perfect continuous — *had been working* | no change |
| will / shall | would |
| can | could |
| may | might |
| must (obligation) | had to / must |
| shall (offer) | should |
| should, would, could, might, ought to, used to, had better | no change |

::: caution No backshift in these four cases
**1. A universal truth or a permanent fact.**
*The teacher said, "The earth revolves round the sun."* → *The teacher said that the
earth **revolves** round the sun.*
**2. A situation that is still true now.**
*She said, "My brother lives in Dharan."* → *She said that her brother **lives** (or
**lived**) in Dharan.*
**3. A past time clause with a stated past time.**
*He said, "I was born in 2005."* → *He said that he **was born** in 2005.*
**4. Second and third conditionals, and *wish* clauses**, which are already unreal.
*He said, "If I were rich, I would help them."* → *He said that if he **were** rich
he **would** help them.*
:::

## 26.3 Pronoun changes

Pronouns change to keep the meaning from the **reporter's** point of view. The rule
is easy to remember as **SON**: the **S**ubject of the reporting verb governs the
first person, the **O**bject governs the second person, and the third person is
**N**ot changed.

| In direct speech | Becomes | Governed by |
|---|---|---|
| I, me, my, mine, myself | he/she, him/her, his/her, his/hers, himself/herself | the speaker |
| we, us, our, ours, ourselves | they, them, their, theirs, themselves | the speaker |
| you, your, yours, yourself | he/she/they, his/her/their…, himself… | the listener |
| he, she, it, they, his, her, its, their | no change | — |

- *Ramesh said to Sita, "**I** will bring **your** book **tomorrow**."*
  → *Ramesh told Sita that **he** would bring **her** book **the next day**.*
- *They said, "**We** have finished **our** work."*
  → *They said that **they** had finished **their** work.*

## 26.4 Changes of time and place

| Direct | Reported | Direct | Reported |
|---|---|---|---|
| now | then | today | that day |
| just now | at that moment | tonight | that night |
| ago | before | yesterday | the previous day / the day before |
| here | there | last night | the previous night |
| this | that | tomorrow | the next day / the following day |
| these | those | next week | the following week |
| hence | thence | last week | the previous week |
| thus | so | the day before yesterday | two days before |
| come | go | the day after tomorrow | in two days' time |

Change these words only when the change is needed. If you report a friend's words
*in the same place on the same day*, *here* and *today* may stay as they are.

## 26.5 Reporting statements

**Rule.** reporting verb (said / told + person) + **that** + backshifted clause.

- *"I am reading the newspaper," said my father.*
  → *My father said that he **was reading** the newspaper.*
- *Bina said to me, "I have lost my purse in the bus."*
  → *Bina told me that she **had lost** her purse in the bus.*
- *The guide said, "Annapurna is visible from Poon Hill."*
  → *The guide said that Annapurna **is** visible from Poon Hill.* (still true)

*That* may be left out after *say* and *tell* in informal English, but write it in
the exam.

## 26.6 Reporting questions

Two things happen in every reported question: the word order becomes **statement
order** (subject before verb), and the question mark disappears. The helping verbs
*do, does, did* are dropped and their tense goes onto the main verb.

```figure caption="Reporting a question. The wh- word or *if/whether* takes the place of the question's inverted word order, the auxiliary *do/does/did* disappears into the main verb, and the question mark becomes a full stop."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.0))
ax.set_xlim(0,10); ax.set_ylim(0,8.2); ax.axis('off')
def chip(x,y,w,t,c,fc,fs=8.0):
    ax.add_patch(FancyBboxPatch((x,y),w,0.9,boxstyle="round,pad=0.09",
                                fc=fc,ec=c,lw=1.0))
    ax.text(x+w/2,y+0.45,t,ha='center',va='center',fontsize=fs,color=c)
ax.text(0.1,7.75,'DIRECT',fontsize=8.0,color=MUTED,ha='left',va='center')
chip(0.3,6.5,1.6,'Where',ACCENT,'#eaf0fb')
chip(2.1,6.5,1.3,'did',  '#A8271F','#fbeceb')
chip(3.6,6.5,1.5,'you',  '#0B6A62','#eef7f1')
chip(5.3,6.5,1.4,'go',   '#B4690E','#fdf1e7')
ax.text(7.1,6.95,'?',fontsize=13,color='#A8271F',ha='center',va='center')
ax.text(0.1,3.9,'REPORTED',fontsize=8.0,color=MUTED,ha='left',va='center')
chip(0.3,2.6,2.4,'He asked me',MUTED,'#f6f7f9')
chip(2.9,2.6,1.6,'where',ACCENT,'#eaf0fb')
chip(4.7,2.6,1.3,'I','#0B6A62','#eef7f1')
chip(6.2,2.6,2.0,'had gone','#B4690E','#fdf1e7')
ax.text(8.5,3.05,'.',fontsize=13,color=INK,ha='center',va='center')
for x0,x1,c in [(1.1,3.7,ACCENT),(4.35,5.35,'#0B6A62'),(6.0,7.2,'#B4690E')]:
    ax.annotate('',xy=(x1,3.6),xytext=(x0,6.4),
                arrowprops=dict(arrowstyle='-|>',color=c,lw=1.0,mutation_scale=9,
                                connectionstyle="arc3,rad=0.12"))
ax.annotate('',xy=(2.75,5.35),xytext=(2.75,6.4),
            arrowprops=dict(arrowstyle='-|>',color='#A8271F',lw=1.0,mutation_scale=9))
ax.text(2.85,5.05,'"did" is dropped — its past tense moves into the main verb',
        fontsize=7.2,color='#A8271F',ha='left',va='center')
ax.text(5.0,1.25,'no inversion   •   no question mark   •   no do / does / did',
        fontsize=7.8,color=INK,ha='center',va='center')
```

**Wh- questions.** reporting verb + *asked* + the same wh- word + statement order.

- *"Where do you live?" he asked me.*
  → *He asked me where I **lived**.*
- *The officer said to her, "Why have you come so late?"*
  → *The officer asked her why she **had come** so late.*

**Yes/no questions.** Use **if** or **whether** in place of a wh- word.

- *"Have you finished your project?" the teacher asked.*
  → *The teacher asked **whether** I **had finished** my project.*
- *She said to him, "Will you come to the picnic?"*
  → *She asked him **if** he **would** come to the picnic.*

Use **whether** (not *if*) before *or not* placed immediately after it, and before
a *to*-infinitive: *He asked **whether or not** I was coming.*

## 26.7 Reporting commands, requests, advice and suggestions

**Rule.** The imperative becomes **to + V1**; the negative imperative becomes
**not to + V1**. Choose the reporting verb to match the force of the original.

| Original | Reporting verb | Reported form |
|---|---|---|
| "Shut the gate." | ordered / told | He **ordered** the guard **to shut** the gate. |
| "Please help me." | requested | She **requested** me **to help** her. |
| "Don't touch the wires." | warned / told | He **warned** us **not to touch** the wires. |
| "You should rest." | advised | The doctor **advised** him **to rest**. |
| "Let's go to Nagarkot." | suggested / proposed | He **suggested** going to Nagarkot. / He **suggested that** we **should go** to Nagarkot. |
| "Let him come in." | requested / suggested | She **suggested that** he **should be** allowed in. |
| "Do come to my house." | invited | She **invited** me **to come** to her house. |

A *please* in the original disappears and becomes the reporting verb *requested*.

## 26.8 Reporting exclamations and wishes

**Rule.** Name the feeling in the reporting verb, then use *that* + a plain
statement. The exclamation mark goes.

| Direct | Reported |
|---|---|
| He said, "What a beautiful sunrise!" | He **exclaimed with wonder that** it was a very beautiful sunrise. |
| She said, "Alas! I have failed." | She **exclaimed with sorrow that** she had failed. |
| They said, "Hurrah! We have won the match." | They **exclaimed with joy that** they had won the match. |
| He said, "Bravo! You have done well." | He **applauded** me, saying that I had done well. |
| She said, "May God bless you!" | She **prayed that** God might bless me. |
| He said, "Good morning, sir." | He **greeted** his teacher respectfully. |
| He said, "Thank you." | He **thanked** me. |
| She said, "Sorry." | She **apologised**. |

Note how *What a …!* and *How …!* are unpacked: *what a beautiful sunrise* becomes
*a very beautiful sunrise*, and *How cold it is!* becomes *that it was very cold*.

::: tip How the Q7 item is usually worded
The instruction is "Change into indirect speech" with a single sentence. Work in
this order every time: (i) look at the punctuation inside the quotation marks — a
question mark, an exclamation mark or a full stop tells you the sentence type;
(ii) write the reporting verb and link for that type; (iii) backshift; (iv) fix the
pronouns; (v) fix the time and place words. Then read your answer once and check
there is no question mark and no quotation mark left.
:::

::: example Worked transformation 26.1 — a statement
**Problem.** Change into indirect speech: *Ram said to his sister, "I am going to
Kathmandu tomorrow to buy books for you."*

**Solution — the four changes.**

1. **Reporting verb and link.** It is a statement, and there is a listener, so
   *said to* → **told**, and the link is **that**.
2. **Tense.** *am going* is present continuous, and the reporting verb *said* is
   past → backshift to past continuous: **was going**.
3. **Pronouns.** *I* is the speaker Ram → **he**. *you* is the listener, his sister
   → **her**.
4. **Time words.** *tomorrow* → **the next day**.

**Answer.** *Ram **told** his sister **that he was going** to Kathmandu **the next
day** to buy books for **her**.*
:::

::: example Worked transformation 26.2 — a yes/no question
**Problem.** Change into indirect speech: *The conductor said to me, "Did you buy a
ticket at the counter?"*

**Solution — step by step.**

1. **Sentence type.** The question mark and the auxiliary *Did* at the front make it
   a **yes/no question** → reporting verb **asked**, link **if / whether**.
2. **Word order.** Reported questions use statement order, so *you buy* becomes
   *I … buy* with no inversion.
3. **Drop the auxiliary.** *Did* disappears; its past tense goes onto the main verb,
   which then backshifts one further step: *buy* → *bought* → **had bought**.
4. **Pronouns.** *you* is the listener, who is *me* → **I**.
5. **Remove the question mark.**

**Answer.** *The conductor **asked me if (whether) I had bought** a ticket at the
counter.*
:::

::: example Worked transformation 26.3 — a command and an exclamation together
**Problem.** Change into indirect speech: *"Don't waste water, children!" said the
teacher. "What a precious thing it is!"*

**Solution — step by step.**

1. **First sentence is a negative command.** Reporting verb **told** (or *ordered*);
   the imperative becomes **not to + V1**: *not to waste*.
2. **The addressee** *children* becomes the object of the reporting verb: *told the
   children*.
3. **Second sentence is an exclamation.** Reporting verb **exclaimed**, or better,
   *added, exclaiming*. Unpack *What a precious thing* into *a very precious thing*
   and add the link **that**.
4. **Backshift the exclamation clause.** *is* → **was**.

**Answer.** *The teacher **told the children not to waste** water and **exclaimed
that** it **was a very precious thing**.*
:::

## Chapter summary

- Four changes, in order: reporting verb and link → tense → pronouns → time and
  place words.
- *Tell* needs a person after it; *say* does not take one unless you add *to*.
- No backshift when the reporting verb is present or future, when the statement is a
  universal truth or still true, when a past time is stated, or in unreal
  conditionals and *wish* clauses.
- Backshift ladder: present → past; present perfect and simple past → past perfect;
  will → would; can → could; may → might; must → had to. Past perfect does not move.
- Statements take *that*; wh- questions keep the wh- word; yes/no questions take
  *if/whether*; commands and requests take *to* / *not to* + V1.
- Reported questions use **statement word order**, drop *do/does/did*, and lose the
  question mark.
- Exclamations are reported by naming the feeling: *exclaimed with joy / sorrow /
  wonder that …*.
- Pronouns follow SON: first person matches the **S**ubject of the reporting verb,
  second person matches the **O**bject, third person is **N**ot changed.

## Practice questions

**Change the following into indirect speech (1 mark each)**

1. She said, "I am preparing for the NEB examination." <span class="marks">[1]</span>
2. He said to me, "I saw your brother at Ratna Park yesterday." <span class="marks">[1]</span>
3. The teacher said, "Water boils at 100 °C." <span class="marks">[1]</span>
4. Mohan said to Gita, "I will help you with your project tomorrow." <span class="marks">[1]</span>
5. My mother said, "I have already cooked the dinner." <span class="marks">[1]</span>
6. "Where are you going?" the policeman asked the boy. <span class="marks">[1]</span>
7. "Have you ever visited Lumbini?" she asked me. <span class="marks">[1]</span>
8. The manager said to the clerk, "Bring the file at once." <span class="marks">[1]</span>
9. "Please lend me your umbrella," said Sunita to her friend. <span class="marks">[1]</span>
10. The doctor said to the patient, "Don't eat oily food." <span class="marks">[1]</span>
11. He said, "Alas! I have missed the last bus." <span class="marks">[1]</span>
12. "What a wonderful view of Machhapuchhre!" said the tourist. <span class="marks">[1]</span>
13. He said to her, "May you pass with distinction!" <span class="marks">[1]</span>
14. "Let's visit the Patan Museum," said Anil. <span class="marks">[1]</span>

::: note Answers
**1.** She said that she **was preparing** for the NEB examination. — present continuous backshifts.
**2.** He told me that he **had seen** my brother at Ratna Park **the previous day**. — simple past → past perfect; *your* → *my*; *yesterday* → *the previous day*.
**3.** The teacher said that water **boils** at 100 °C. — a universal truth is not backshifted.
**4.** Mohan told Gita that he **would** help her with her project **the next day**. — *will* → *would*.
**5.** My mother said that she **had already cooked** the dinner. — present perfect → past perfect.
**6.** The policeman asked the boy **where he was going**. — wh- question, statement order.
**7.** She asked me **if (whether) I had ever visited** Lumbini. — yes/no question takes *if/whether*.
**8.** The manager **ordered** the clerk **to bring** the file at once. — command → *to* + V1.
**9.** Sunita **requested** her friend **to lend** her her umbrella. — *please* becomes *requested*.
**10.** The doctor **advised** the patient **not to eat** oily food. — negative command → *not to* + V1.
**11.** He **exclaimed with sorrow that** he **had missed** the last bus. — exclamation with *Alas!*.
**12.** The tourist **exclaimed with wonder that** it was **a very wonderful** view of Machhapuchhre. — *What a …!* is unpacked.
**13.** He **prayed that** she **might** pass with distinction. — a wish is reported with *prayed that* and *might*.
**14.** Anil **suggested visiting** the Patan Museum. (or *suggested that they should visit …*) — *Let's* is a suggestion.
:::

**Change the following into direct speech (1 mark each)**

15. He told me that he was feeling unwell that day. <span class="marks">[1]</span>
16. She asked me whether I had finished my homework. <span class="marks">[1]</span>
17. The guard ordered us not to park there. <span class="marks">[1]</span>
18. The old man asked the boy where he lived. <span class="marks">[1]</span>

::: note Answers
**15.** He said to me, "I am feeling unwell today." — reverse the backshift and the time word.
**16.** She said to me, "Have you finished your homework?" — *whether* signals a yes/no question.
**17.** He said to us, "Don't park here." — *not to* + V1 becomes a negative imperative; *there* → *here*.
**18.** The old man said to the boy, "Where do you live?" — the wh- question regains its inversion and *do*.
:::

**Correct the errors in the following sentences (1 mark each)**

19. He told that he would come on Sunday. <span class="marks">[1]</span>
20. She said me that she was busy. <span class="marks">[1]</span>
21. The teacher asked us where were we going. <span class="marks">[1]</span>
22. He asked me that I had seen the film. <span class="marks">[1]</span>
23. She asked me if did I need any help. <span class="marks">[1]</span>
24. He ordered them do not make noise. <span class="marks">[1]</span>
25. My friend said that he will meet me the next day. <span class="marks">[1]</span>
26. She said that the sun rose in the east. <span class="marks">[1]</span>

::: note Answers
**19.** He **said** that he would come on Sunday. (or *He told me that …*) — *tell* needs a person after it.
**20.** She **said to me** (or **told me**) that she was busy. — *say* takes *to* before a person.
**21.** The teacher asked us **where we were going**. — a reported question uses statement order.
**22.** He asked me **if (whether)** I had seen the film. — a yes/no question takes *if*, not *that*.
**23.** She asked me **if I needed** any help. — no *did* and no inversion in a reported question.
**24.** He ordered them **not to make** noise. — a negative command becomes *not to* + V1.
**25.** My friend said that he **would** meet me the next day. — *will* backshifts to *would*.
**26.** She said that the sun **rises** in the east. — a universal truth keeps the present tense.
:::
