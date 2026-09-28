---
subject: Compulsory English
grade: 12
unit: 27
title: Reported Speech
hours: 4
area: Grammar
---

**Direct speech** gives a speaker's exact words inside quotation marks: *Sita
said, "I am busy today."* **Indirect** or **reported speech** gives the same
message in the reporter's own frame: *Sita said that she was busy that day.*
Turning one into the other is a mechanical operation, and the examiner sets it
every year. Four things may change — the **reporting verb and link word**, the
**pronouns**, the **tense**, and the **words of time and place** — and a fifth
thing, the **word order** of questions, changes too. Work through them in that
order every single time and the transformation becomes almost automatic.

::: key The standard procedure
1. Remove the inverted commas, the comma after the reporting verb and the
   question or exclamation mark.
2. Choose the **reporting verb** and the **link word** according to the type of
   sentence (that / if / whether / a wh-word / *to* + verb).
3. Change the **pronouns** to fit the new speaker and listener.
4. Move the **tense one step back** — unless the reporting verb is in the present
   or future, or the words state a universal truth.
5. Change the **words of time and place** (*now → then, here → there, tomorrow →
   the next day*).
:::

## 27.1 The tense shift

```figure caption="The backshift ladder. When the reporting verb is in the past, every tense in the quoted words moves one step further back; the past perfect has nowhere further to go, so it stays."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,4.1))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
GREEN="#0B6A62"; AMBER="#B4690E"
ax.text(0.15,9.50,"DIRECT",fontsize=6.6,color=MUTED,ha='left')
ax.text(5.05,9.50,"REPORTED",fontsize=6.6,color=MUTED,ha='left')
ax.plot([0.15,9.85],[9.15,9.15],color=GRID,lw=0.9)
rows=[("simple present","simple past","works → worked"),
      ("present continuous","past continuous","is working → was working"),
      ("present perfect","past perfect","has worked → had worked"),
      ("present perfect cont.","past perfect cont.","has been working → had been"),
      ("simple past","past perfect","worked → had worked"),
      ("past continuous","past perfect cont.","was working → had been working"),
      ("past perfect","past perfect","had worked → had worked"),
      ("will / shall","would / should","will go → would go"),
      ("can / may / must","could / might / had to","can go → could go")]
y=8.45
for a,b,ex in rows:
    ax.text(0.15,y,a,fontsize=6.9,color=INK,ha='left',va='center')
    ax.annotate("",xy=(4.90,y),xytext=(4.10,y),
                arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=0.9))
    ax.text(5.05,y,b,fontsize=6.9,color=ACCENT,ha='left',va='center')
    y-=0.78
ax.plot([0.15,9.85],[1.55,1.55],color=GRID,lw=0.9)
ax.text(0.15,1.05,"NO SHIFT:  reporting verb in the present or future;",
        fontsize=6.9,color=GREEN,ha='left')
ax.text(0.15,0.50,"universal truths;  would, could, might, should, ought to, used to",
        fontsize=6.9,color=GREEN,ha='left')
ax.text(0.15,0.00,"must stays when it states a rule that is still in force",
        fontsize=6.6,color=AMBER,ha='left')
```

| Direct | Reported |
|---|---|
| *"I **write** letters."* | *He said that he **wrote** letters.* |
| *"I **am writing**."* | *He said that he **was writing**.* |
| *"I **have written**."* | *He said that he **had written**.* |
| *"I **have been writing**."* | *He said that he **had been writing**.* |
| *"I **wrote** a letter."* | *He said that he **had written** a letter.* |
| *"I **was writing**."* | *He said that he **had been writing**.* |
| *"I **had written**."* | *He said that he **had written**.* (no change) |
| *"I **will write**."* | *He said that he **would write**.* |
| *"I **shall write**."* | *He said that he **would** (or **should**) **write**.* |

### Modals in reported speech

| Direct | Reported | Example |
|---|---|---|
| can | could | *"I **can** swim."* → *She said she **could** swim.* |
| may (permission / possibility) | might | *"You **may** go."* → *He said I **might** go.* |
| must (obligation) | had to | *"You **must** leave."* → *He said I **had to** leave.* |
| must (rule still true, or deduction) | must | *He said that water **must** boil at 100 °C.* |
| shall (future) | would | *"We **shall** win."* → *They said they **would** win.* |
| shall (suggestion, offer) | should | *"**Shall** I carry it?"* → *He asked whether he **should** carry it.* |
| will | would | *"I **will** help."* → *He said he **would** help.* |
| **no change:** would, could, might, should, ought to, used to, had better, would rather, need not | | *"You **should** rest."* → *She said I **should** rest.* |

## 27.2 Pronouns, time words and place words

**Pronouns — the rule.** First person (*I, we, my, our, us*) changes to agree with
the **subject** of the reporting verb. Second person (*you, your*) changes to
agree with its **object**. Third person (*he, she, they, it*) does not change.

*He said to me, "**I** have finished **your** work."* → *He told me that **he**
had finished **my** work.*

| Direct | Reported | Direct | Reported |
|---|---|---|---|
| now | then | here | there |
| today | that day | this | that |
| tonight | that night | these | those |
| yesterday | the previous day / the day before | come | go |
| tomorrow | the next day / the following day | bring | take |
| last night | the previous night | hence | thence |
| next week | the following week | thus | so |
| last month | the previous month | ago | before |
| the day before yesterday | two days before | just | then |

*"I met him **here yesterday**,"* she said. → *She said that she had met him
**there the previous day**.*

## 27.3 Reporting each type of sentence

```figure caption="The router. The type of the quoted sentence decides the reporting verb, the link word and the form of the verb that follows."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,4.4))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
GREEN="#0B6A62"; AMBER="#B4690E"; PURPLE="#7A3E9D"
rows=[("STATEMENT",ACCENT,"say / tell + that + shifted clause",
       '"I am tired." → He said that he was tired.'),
      ("YES/NO QUESTION",GREEN,"ask + if / whether + statement order",
       '"Are you ready?" → He asked if I was ready.'),
      ("WH- QUESTION",GREEN,"ask + wh-word + statement order",
       '"Where do you live?" → He asked where I lived.'),
      ("COMMAND",AMBER,"order / tell + object + to + V1",
       '"Get out!" → He ordered me to get out.'),
      ("REQUEST / ADVICE",AMBER,"request / advise + object + to + V1",
       '"Please wait." → He requested me to wait.'),
      ("PROHIBITION",AMBER,"tell + object + not to + V1",
       '"Don\'t shout." → He told me not to shout.'),
      ("EXCLAMATION",PURPLE,"exclaim + that + shifted clause",
       '"What a view!" → He exclaimed that it was a fine view.')]
y=9.05
for lab,col,pat,ex in rows:
    ax.add_patch(FancyBboxPatch((0.15,y-0.42),2.75,0.60,boxstyle="round,pad=0.05",
                                fc="#ffffff",ec=col,lw=0.9))
    ax.text(1.525,y-0.12,lab,ha='center',va='center',fontsize=6.3,color=col)
    ax.text(3.15,y,pat,ha='left',va='center',fontsize=6.9,color=col)
    ax.text(3.15,y-0.56,ex,ha='left',va='center',fontsize=6.4,color=MUTED)
    y-=1.32
```

### Statements

Use **said** when there is no listener mentioned, **told** when there is.

| Direct | Reported |
|---|---|
| *He **said**, "I am ill."* | *He **said that** he was ill.* |
| *He **said to me**, "I am ill."* | *He **told me that** he was ill.* |
| *She said, "We won the match."* | *She said that they **had won** the match.* |

### Questions

Three things happen: the reporting verb becomes **ask / enquire / want to know**;
the question changes to **statement word order**; and *do, does, did* disappear.

| Direct | Reported |
|---|---|
| *He said, "Are you coming?"* | *He **asked whether / if** I **was** coming.* |
| *He said, "Do you like tea?"* | *He asked **whether I liked** tea.* |
| *He said, "Where **did you go**?"* | *He asked **where I had gone**.* |
| *She said, "What is your name?"* | *She asked **what my name was**.* |
| *"Who broke the glass?" he asked.* | *He asked **who had broken** the glass.* (a subject question keeps its order) |

### Commands, requests and advice

The imperative becomes an **infinitive**: reporting verb + object + *to* + base
verb. A negative imperative takes **not to**.

| Direct | Reporting verb | Reported |
|---|---|---|
| *"Stand up," the teacher said to us.* | order / command / tell | *The teacher **ordered us to stand** up.* |
| *"Please lend me your pen," he said.* | request | *He **requested me to lend** him my pen.* |
| *"You should see a doctor," she said.* | advise | *She **advised me to see** a doctor.* |
| *"Don't touch the wires," he said.* | warn / tell | *He **warned me not to touch** the wires.* |
| *"Let's go for a walk," she said.* | suggest / propose | *She **suggested going** for a walk.* / *She proposed that we **should go** for a walk.* |
| *"Let him come in," he said.* | — | *He said that he **might come** in.* |

### Exclamations, wishes and fixed expressions

| Direct | Reported |
|---|---|
| *"What a beautiful garden!" he said.* | *He **exclaimed that** it was a very beautiful garden.* |
| *"Alas! I have lost my purse," she said.* | *She **exclaimed with sorrow that** she had lost her purse.* |
| *"Hurrah! We have won," they said.* | *They **exclaimed with joy that** they had won.* |
| *"May you live long!" he said.* | *He **prayed that** I **might** live long.* |
| *"Good morning," she said to him.* | *She **greeted** him.* |
| *"Thank you," he said to her.* | *He **thanked** her.* |
| *"Yes," he said.* | *He **replied in the affirmative**.* / *He agreed.* |
| *"No," he said.* | *He **replied in the negative**.* / *He refused.* |

## 27.4 When the tense does **not** shift

1. **The reporting verb is in the present, present perfect or future.**
   *He **says** that he **is** busy.* · *She **has told** me that she **will**
   come.*
2. **Universal truths and permanent facts.**
   *The teacher said that the earth **revolves** round the sun.*
   *He said that Kathmandu **is** the capital of Nepal.*
3. **The verb is already past perfect** — there is no further step back.
4. **Second and third conditionals, and *wish* clauses**, which are already
   unreal.
   *"If I **were** rich, I **would** travel," he said.* → *He said that if he
   **were** rich, he **would** travel.*
   *"I wish I **knew** the answer," she said.* → *She said she wished she **knew**
   the answer.*
5. **Modals that have no past form**: *would, could, might, should, ought to,
   used to, had better, would rather, need not*.
6. **A past tense tied to a stated past time**, where a shift would sound absurd:
   *He said that he **was born** in 2005.*

::: caution The six mistakes that cost marks
✗ *He **said me** that he was ill.* → ✓ *He **told me*** or ✓ *He **said to me***.
✗ *He **told to me** the truth.* → ✓ *He **told me** the truth.* (*tell* takes no
*to* before the listener)
✗ *He asked me **that where** I was going.* → ✓ *He asked me **where** I was
going.* (never use *that* with a wh-word or with *if / whether*)
✗ *He asked **where was I** going.* → ✓ *He asked **where I was** going.* (reported
questions take statement order)
✗ *He asked if I **am** free**?*** → ✓ *He asked if I **was** free**.*** (no
question mark in reported speech)
✗ *He said that he **will** come the next day.* → ✓ *…that he **would** come the
next day.* (backshift after a past reporting verb)
:::

## 27.5 *Say, tell, speak, ask*

| Verb | Pattern | Example |
|---|---|---|
| say | say (**to** somebody) **that** … | *He said **to me that** he was late.* |
| tell | tell **somebody that** … (no *to*) | *He **told me that** he was late.* |
| tell | also: *tell a lie / the truth / a story / the time* | *Don't **tell lies**.* |
| speak | speak **to** somebody · speak a language | *I **spoke to** the principal.* |
| ask | ask **somebody about / for** something | *She **asked for** water.* |

::: example Worked item 27.1 — a statement with several changes
**Problem.** Report: *Ramesh said to me, "I bought this book here yesterday and I
am reading it now."*

**Solution — follow the five steps.**

1. **Reporting verb and link word.** There is a listener (*to me*), so *said to
   me* becomes **told me**, and the link word is **that**.
2. **Pronouns.** *I* refers to the subject *Ramesh* → **he**. There is no *you*.
3. **Tense.** *bought* (simple past) → **had bought**; *am reading* (present
   continuous) → **was reading**.
4. **Time and place.** *here* → **there**; *yesterday* → **the previous day**;
   *now* → **then**.
5. **Other pointers.** *this book* → **that book**.

**Answer.** ***Ramesh told me that he had bought that book there the previous day
and that he was reading it then.***
:::

::: example Worked item 27.2 — a question and a command together
**Problem.** Report: *"Where are you going? Don't forget your umbrella," my mother
said to me.*

**Solution — report each sentence in its own pattern.**

1. **The first sentence is a wh-question.** Reporting verb → **asked**; link word
   → the wh-word **where**; word order becomes statement order (*I was going*);
   *you* → *I*; *are going* → *was going*.
   → *My mother asked me where I was going*
2. **The second is a negative imperative.** Reporting verb → **told** (or
   *reminded*); pattern → object + **not to** + base verb; *your* → *my*.
   → *and told me not to forget my umbrella*
3. **Join them with *and***, keeping the object *me* in both.

**Answer.** ***My mother asked me where I was going and told me not to forget my
umbrella.***
:::

::: example Worked item 27.3 — no backshift
**Problem.** Report: *The teacher said, "The sun rises in the east, and I told you
this yesterday."*

**Solution — decide clause by clause.**

1. **First clause: a universal truth.** *The sun rises in the east* is always
   true, so the present tense is **kept**.
2. **Second clause: an ordinary past statement.** *told* shifts to **had told**.
3. **Pronouns.** *I* → *he* (the teacher); *you* → *us* (assuming the reporter was
   in the class).
4. **Time word.** *yesterday* → **the previous day**; *this* → **that**.

**Answer.** ***The teacher said that the sun rises in the east and that he had
told us that the previous day.***

A universal truth stays in the present even though everything around it shifts.
:::

## Chapter summary

- Reported speech changes the reporting verb and link word, the pronouns, the
  tense, the time and place words, and the word order of questions.
- Backshift: present → past, past → past perfect, *will → would*, *can → could*,
  *may → might*, *must → had to*. The past perfect does not move.
- No backshift after a present or future reporting verb, for universal truths, for
  unreal conditionals and *wish*, and for *would, could, might, should, ought to,
  used to*.
- Pronouns: first person follows the subject of the reporting verb, second person
  follows its object, third person is unchanged.
- Statements take *that*; yes/no questions take *if / whether*; wh-questions keep
  their wh-word; imperatives become *to* + base verb, with *not to* for negatives.
- A reported question has **statement word order**, no *do / does / did*, and no
  question mark.
- *say that* / *say to somebody that* / *tell somebody that* — *tell* never takes
  *to* before the listener, and *that* is never used with a wh-word or *if*.
- Exclamations use *exclaim with joy / sorrow that*; greetings, thanks, yes and no
  have their own reporting verbs.

## Practice questions

**Change into indirect speech (1 mark each)**

1. He said, "I am writing a letter." <span class="marks">[1]</span>
2. She said to me, "I saw your brother yesterday." <span class="marks">[1]</span>
3. The guide said, "The Himalayas lie to the north of Nepal." <span class="marks">[1]</span>
4. "Are you free this evening?" he asked me. <span class="marks">[1]</span>
5. The teacher said to the boys, "Why are you making noise?" <span class="marks">[1]</span>
6. "Please give me a glass of water," the old man said to her. <span class="marks">[1]</span>
7. "Don't play on the road," my father said to us. <span class="marks">[1]</span>
8. "What a lovely morning it is!" she said. <span class="marks">[1]</span>
9. He said, "I shall go to Pokhara tomorrow." <span class="marks">[1]</span>
10. "May God bless you!" the priest said to the pilgrims. <span class="marks">[1]</span>

::: note Answers
**1.** **He said that he was writing a letter.** — present continuous → past continuous.
**2.** **She told me that she had seen my brother the previous day.** — *said to me* → *told me*; *saw* → *had seen*; *your* → *my*; *yesterday* → *the previous day*.
**3.** **The guide said that the Himalayas lie to the north of Nepal.** — a permanent geographical fact does not shift.
**4.** **He asked me whether (if) I was free that evening.** — yes/no question → *whether*; *this evening* → *that evening*.
**5.** **The teacher asked the boys why they were making noise.** — wh-word kept, statement order, no question mark.
**6.** **The old man requested her to give him a glass of water.** — request → *requested* + object + *to* + base verb.
**7.** **My father told us not to play on the road.** — negative imperative → *not to* + base verb.
**8.** **She exclaimed that it was a very lovely morning.** — exclamation → *exclaimed that*, with *very* replacing *what a*.
**9.** **He said that he would go to Pokhara the next day.** — *shall* (future) → *would*; *tomorrow* → *the next day*.
**10.** **The priest prayed that God might bless the pilgrims.** — an optative is reported with *prayed that* + *might*.
:::

**Correct the errors (1 mark each)**

11. He said me that he was busy. <span class="marks">[1]</span>
12. She told to me that she would come. <span class="marks">[1]</span>
13. He asked me that where I lived. <span class="marks">[1]</span>
14. She asked me what was my name. <span class="marks">[1]</span>
15. He said that he will meet me the next day. <span class="marks">[1]</span>
16. The teacher said that the earth moved round the sun. <span class="marks">[1]</span>
17. He asked me if I am ready? <span class="marks">[1]</span>
18. She told me to not open the window. <span class="marks">[1]</span>

::: note Answers
**11.** He **told me** that he was busy. (or *He said to me that…*)
**12.** She **told me** that she would come. — *tell* takes no *to* before the listener.
**13.** He asked me **where** I lived. — no *that* with a wh-word.
**14.** She asked me **what my name was**. — statement order.
**15.** He said that he **would** meet me the next day. — backshift after a past reporting verb.
**16.** The teacher said that the earth **moves** round the sun. — a universal truth stays in the present.
**17.** He asked me **whether (if) I was ready.** — no question mark, and the tense shifts.
**18.** She told me **not to open** the window. — *not* comes before *to*.
:::

**Change into direct speech (1 mark each)**

19. He told me that he had finished his homework. <span class="marks">[1]</span>
20. She asked me where I had put the keys. <span class="marks">[1]</span>
21. The officer ordered the peon to bring the file at once. <span class="marks">[1]</span>
22. He exclaimed with sorrow that he had failed the test. <span class="marks">[1]</span>

::: note Answers
**19.** He said to me, **"I have finished my homework."** — the past perfect becomes the present perfect.
**20.** She said to me, **"Where have you put the keys?"** — restore question order and the question mark.
**21.** The officer said to the peon, **"Bring the file at once."** — the infinitive becomes an imperative.
**22.** He said, **"Alas! I have failed the test."** — *with sorrow* signals the interjection *Alas!*
:::
