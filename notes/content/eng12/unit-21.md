---
subject: Compulsory English
grade: 12
unit: 21
title: Question Tags and Questions
hours: 4
area: Grammar
---

A **question tag** is the short question fixed to the end of a statement — *You
are from Palpa, **aren't you?*** It is the single most predictable item in NEB
Q7, because a tag is not written from feeling: it is calculated from the
statement in front of it. Questions proper — yes/no questions, wh-questions and
indirect questions — are equally mechanical once the word order is fixed in your
mind. This unit gives you the complete paradigm, including every irregular tag
the board has ever set.

::: key Three decisions make every tag
**(1) Which operator?** Repeat the auxiliary or modal from the statement; if
there is none, supply *do / does / did*.
**(2) Which polarity?** Positive statement → negative tag; negative statement →
positive tag.
**(3) Which pronoun?** Replace the subject with the matching personal pronoun.
Operator + polarity + pronoun, in that order, and the tag is finished.
:::

## 21.1 Building a regular tag

The tag has exactly two words (three if you spell out the negative): an
**operator** and a **pronoun**. The operator must be the same tense and person as
the verb in the statement.

| Statement | Operator found | Polarity needed | Tag |
|---|---|---|---|
| She **is** waiting outside. | is | negative | isn't she? |
| They **were** not invited. | were (negative) | positive | were they? |
| Hari **has** passed the test. | has | negative | hasn't he? |
| We **can** meet on Friday. | can | negative | can't we? |
| You **will** help me. | will | negative | won't you? |
| He **should** apologise. | should | negative | shouldn't he? |
| The bus **left** early. | none → did | negative | didn't it? |
| Sita **teaches** at Amar Campus. | none → does | negative | doesn't she? |
| The boys **play** football. | none → do | negative | don't they? |
| She **didn't** come. | did (negative) | positive | did she? |

```figure caption="A tag is built in three moves, always in the same order. The statement supplies the operator and the subject; the polarity is simply flipped."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,3.4))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
def box(x,y,w,h,t,fc,ec,fs=7.8,tc=None,weight='normal'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.11",fc=fc,ec=ec,lw=1.0))
    ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs,color=tc or INK,
            linespacing=1.4,fontweight=weight)
def down(x,y0,y1):
    ax.annotate('', xy=(x,y1), xytext=(x,y0),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=9))
box(0.15,8.45,9.70,1.25,"STATEMENT:   She  has  finished  the  work.","#ffffff",INK,8.4)
down(2.6,8.40,7.75); down(7.4,8.40,7.75)
box(0.15,6.35,4.65,1.40,"1.  Find the operator\nauxiliary / modal, else do-does-did",
    "#eef2fb",ACCENT,7.6,ACCENT)
box(5.20,6.35,4.65,1.40,"has","#ffffff",MUTED,9.0)
down(2.45,6.30,5.10); down(7.5,6.30,5.10)
box(0.15,3.70,4.65,1.40,"2.  Flip the polarity\npositive → negative, and back",
    "#eef2fb",ACCENT,7.6,ACCENT)
box(5.20,3.70,4.65,1.40,"hasn't","#ffffff",MUTED,9.0)
down(2.45,3.65,2.85); down(7.5,3.65,2.85)
box(0.15,1.45,4.65,1.40,"3.  Pronoun for the subject\nSita → she,  this → it,  nobody → they",
    "#eef2fb",ACCENT,7.4,ACCENT)
box(5.20,1.45,4.65,1.40,"hasn't  she","#ffffff",MUTED,9.0)
ax.text(5.0,0.62,"She has finished the work,  hasn't she?",ha='center',va='center',
        fontsize=8.6,color=INK,fontweight='bold')
```

**Contraction is compulsory in a negative tag.** Write *isn't he?*, not *is not
he?* The only exception is the formal first person: *I am right, **am I not?***
is correct but old-fashioned; the ordinary form is *aren't I?*

## 21.2 The complete paradigm, irregulars included

Learn this table. Everything the examiner can set is in it.

| Type of statement | Example | Tag | Why |
|---|---|---|---|
| **I am** + complement | I am your monitor, | **aren't I?** | *amn't* does not exist in standard English |
| **I am not** | I'm not late, | **am I?** | ordinary flip |
| **Let's** (suggestion) | Let's plant a tree, | **shall we?** | *let's* = a proposal, so *shall we* |
| **Let us / Let me** (asking permission) | Let me explain, | **will you?** | you are addressing a second person |
| **Affirmative imperative** | Open the window, | **will you?** (also *won't you? / can you? / would you?*) | a command turned into a request |
| **Negative imperative** | Don't be late, | **will you?** | negative imperatives keep *will you* |
| **There is / are / was** | There is a mistake here, | **isn't there?** | *there* is the grammatical subject |
| **There aren't** | There aren't any seats, | **are there?** | ordinary flip |
| **Nobody / no one / none** | Nobody phoned, | **did they?** | the word is negative; the pronoun is *they* |
| **Everybody / somebody / anyone** | Everyone has left, | **haven't they?** | plural pronoun *they* for a singular verb |
| **Nothing** | Nothing is impossible, | **is it?** | *nothing* takes *it*, and is already negative |
| **Everything / something** | Something is wrong, | **isn't it?** | *it* for a thing |
| **This / That** | This is your seat, | **isn't it?** | *this / that* → *it* |
| **These / Those** | Those are his books, | **aren't they?** | *these / those* → *they* |
| **have to / has to** | We have to pay today, | **don't we?** | *have to* behaves like a full verb |
| **had better** | You'd better rest, | **hadn't you?** | *'d* = *had* |
| **would rather** | You'd rather walk, | **wouldn't you?** | *'d* = *would* |
| **used to** | He used to smoke, | **didn't he?** | past habit, so *did* |
| **ought to** | We ought to help, | **oughtn't we?** / *shouldn't we?* | both accepted |
| **need** (modal) | You needn't worry, | **need you?** | modal *need* repeats itself |
| **must** (obligation) | You must attend, | **mustn't you?** | repeat the modal |
| **must** (deduction) | He must be ill, | **isn't he?** | the real verb is *be* |
| **Negative adverbs** | She hardly ever complains, | **does she?** | *hardly* makes it negative |
| **I think / suppose + clause** | I think he is honest, | **isn't he?** | the tag follows the *inside* clause |
| **I don't think + clause** | I don't think she will come, | **will she?** | the negative is transferred forward |
| **one** as subject | One should keep one's word, | **shouldn't one?** (*shouldn't we?*) | formal *one* |
| **Exclamatory statement** | What a lovely morning it is, | **isn't it?** | tag follows the hidden statement |

::: memory The negative words that flip a tag
*never, hardly, hardly ever, scarcely, barely, seldom, rarely, few, little, no,
none, nobody, no one, nothing, neither, nowhere* — a statement containing any of
these is **negative**, so it takes a **positive** tag. But ***a few*** and ***a
little*** are positive: *He has a little money, **hasn't he / doesn't he?***
:::

::: caution The traps that cost the mark
**Never use *isn't it?* as an all-purpose tag.** This is the commonest Nepali
English habit and it is marked wrong every time.
✗ He is coming tomorrow, isn't it? → ✓ He is coming tomorrow, **isn't he?**
✗ You have finished, isn't it? → ✓ You have finished, **haven't you?**
**Watch the apostrophe-d and apostrophe-s.** *'s* is *is* or *has*; *'d* is
*had* or *would*. *He's gone, **hasn't he?*** but *He's a pilot, **isn't he?***
**Mind the polarity.** Two negatives is wrong: ✗ *She can't swim, can't she?* →
✓ *She can't swim, **can she?***
**Tag the subject, not the nearest noun.** *Sita's brother works in Qatar,
**doesn't he?*** — the subject is *brother*, not *Sita*.
:::

Intonation carries meaning the printed page cannot. Said with a **falling** tone,
a tag asks for agreement (*It's hot today, isn't it?*); said with a **rising**
tone, it is a genuine question (*You locked the gate, didn't you?*).

```photo id="eng12/imperative-sign" caption="An imperative in the wild. Attach a tag to it and it becomes a request: Keep off the grass, will you? An imperative never takes isn't it? — and, as the photograph shows, not every reader obeys." width="82"
crop 0.34 0.20 1.00 1.00
```

## 21.3 Yes/no questions and wh-questions

**Yes/no questions** put the operator in front of the subject. If the statement
has no auxiliary, *do / does / did* is supplied — and the main verb returns to the
base form.

- *She is in Grade 12.* → ***Is** she in Grade 12?*
- *They have submitted the form.* → ***Have** they submitted the form?*
- *He works in Doha.* → ***Does** he **work** in Doha?* (not ~~does he works~~)
- *The train left at six.* → ***Did** the train **leave** at six?*

**Wh-questions** put the question word first and then invert exactly as above:

**wh-word + operator + subject + main verb + rest?**

| Question word | Asks about | Example |
|---|---|---|
| who | a person (subject or object) | Who called you? |
| whom | a person (object, formal) | Whom did you meet? |
| whose | possession | Whose bag is this? |
| what | a thing, an action | What do you want? |
| which | a choice from a known set | Which route is shorter? |
| when | time | When did the class start? |
| where | place | Where are you going? |
| why | reason | Why didn't you inform me? |
| how | manner | How did you reach Jumla? |
| how many / how much | number / quantity | How many students passed? |
| how long / how often / how far / how old | duration / frequency / distance / age | How long have you waited? |

::: key Subject questions take no *do*
When the question word **is itself the subject**, there is no inversion and no
*do / does / did*: the verb simply follows the wh-word.
*Someone broke the window.* → ***Who broke** the window?* (not ~~who did break~~)
*Something happened.* → ***What happened?***
*The red team won.* → ***Which team won?***
Compare the **object** question, which does invert:
*You met someone.* → ***Whom did you meet?*** / *Who did you meet?*
:::

Two more patterns worth knowing:

- **Preposition at the end** is normal in ordinary English: *Who are you waiting
  **for**?* The formal alternative moves it forward: *For whom are you waiting?*
  Never write ~~For whom are you waiting for?~~
- ***What … like?*** asks about character or quality; ***How …?*** asks about
  health or progress. *What is your new teacher like?* — *She is strict but kind.*
  / *How is your mother?* — *She is better, thank you.*

## 21.4 Indirect (embedded) questions

When a question is put inside another sentence — after *Could you tell me…, Do you
know…, I wonder…, Please tell me…* — the inversion is **undone**. The embedded
part goes back to **statement order**, and *do / does / did* disappears.

| Direct question | Embedded in a longer sentence |
|---|---|
| Where is the bus park? | Could you tell me **where the bus park is**? |
| What time does the bank open? | Do you know **what time the bank opens**? |
| Why did she resign? | I wonder **why she resigned**. |
| Has the result been published? | Do you know **whether/if the result has been published**? |
| Is this seat free? | May I ask **if this seat is free**? |

A yes/no question needs ***if*** or ***whether*** as the link; a wh-question keeps
its own wh-word and needs no *that*.

```figure caption="Direct questions invert the subject and the operator; questions embedded inside another sentence do not. The commonest Q7 error is carrying the inversion into the embedded clause."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.0))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
def cell(x,y,w,t,fc,ec,fs=7.8,tc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,1.15,boxstyle="round,pad=0.09",fc=fc,ec=ec,lw=1.0))
    ax.text(x+w/2,y+0.575,t,ha='center',va='center',fontsize=fs,color=tc or INK)
ax.text(0.15,9.45,"DIRECT QUESTION  —  operator jumps in front of the subject",
        fontsize=7.6,color=INK,ha='left',va='center')
cell(0.15,7.90,2.60,"Where","#f4f6f8",MUTED)
cell(2.95,7.90,1.90,"is","#fdf1e7","#B4690E",8.0,"#B4690E")
cell(5.05,7.90,4.80,"the office?","#eef2fb",ACCENT,8.0,ACCENT)
ax.annotate('', xy=(3.90,7.05), xytext=(7.45,7.05),
            arrowprops=dict(arrowstyle='-|>', color="#B4690E", lw=1.1,
                            mutation_scale=9, connectionstyle="arc3,rad=0.30"))
ax.text(5.65,6.05,"operator before subject",fontsize=7.0,color="#B4690E",ha='center')
ax.plot([0.15,9.85],[5.45,5.45],color=GRID,lw=0.9)
ax.text(0.15,4.85,"EMBEDDED QUESTION  —  statement order is restored",
        fontsize=7.6,color=INK,ha='left',va='center')
cell(0.15,3.25,3.20,"Could you tell me","#ffffff",MUTED,7.8)
cell(3.50,3.25,1.60,"where","#f4f6f8",MUTED)
cell(5.25,3.25,2.40,"the office","#eef2fb",ACCENT,8.0,ACCENT)
cell(7.80,3.25,2.05,"is?","#fdf1e7","#B4690E",8.0,"#B4690E")
ax.annotate('', xy=(8.80,2.45), xytext=(6.45,2.45),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.1,
                            mutation_scale=9, connectionstyle="arc3,rad=-0.30"))
ax.text(7.60,1.55,"subject before operator",fontsize=7.0,color=ACCENT,ha='center')
ax.text(0.15,1.20,"✗  Could you tell me where is the office?",fontsize=8.0,color="#9B2C2C",ha='left')
ax.text(0.15,0.42,"✓  Could you tell me where the office is.",fontsize=8.0,color="#0B6A62",ha='left')
```

## 21.5 The mistakes Nepali speakers make most

| ✗ Wrong | ✓ Right | The rule broken |
|---|---|---|
| He is a teacher, isn't it? | He is a teacher, **isn't he?** | the tag pronoun must match the subject |
| You are coming, no? | You are coming, **aren't you?** | *no?* is not an English tag |
| Let's go, will we? | Let's go, **shall we?** | *let's* takes *shall we* |
| Sit down, shall you? | Sit down, **will you?** | imperatives take *will you* |
| I am your friend, isn't it? | I am your friend, **aren't I?** | the *I am* irregular |
| Nobody helped him, didn't they? | Nobody helped him, **did they?** | *nobody* is already negative |
| There is no water, isn't there? | There is no water, **is there?** | *no* makes the statement negative |
| What you are doing here? | **What are you doing here?** | a direct question must invert |
| Why you did not come? | **Why didn't you come?** | *did* + base form, inverted |
| Who did write this poem? | **Who wrote this poem?** | subject questions take no *did* |
| Tell me where is the library. | Tell me **where the library is.** | no inversion when embedded |
| Do you know what is the time? | Do you know **what the time is?** | same rule |
| Does he plays cricket? | **Does he play** cricket? | after *does*, the base form |
| She didn't came, did she? | **She didn't come**, did she? | after *didn't*, the base form |

::: example Worked item 21.1 — a tag with a hidden negative
**Problem.** Add a question tag: *Your brother seldom writes to you, ____ ?*

**Solution — step by step.**

1. **Look for the operator.** *writes* is a simple present verb with no auxiliary,
   so the operator must be supplied: the subject *your brother* is third person
   singular, so *does*.
2. **Decide the polarity.** There is no *not*, but *seldom* means "almost never".
   A statement containing *seldom, rarely, hardly, scarcely, barely* or *never*
   counts as **negative**, so the tag must be **positive**.
3. **Choose the pronoun.** *Your brother* is a male person → *he*.

**Answer.** *Your brother seldom writes to you, **does he?***

A student who ignores *seldom* writes *doesn't he?* and loses the mark.
:::

::: example Worked item 21.2 — the transferred negative
**Problem.** Add a question tag: *I don't think the shop is open on Saturday,
____ ?*

**Solution — step by step.**

1. **Find the clause the tag really belongs to.** With *I think / I suppose / I
   believe / I expect*, the tag is taken from the **inside** clause, not from *I
   think*. The inside clause is *the shop is open on Saturday*.
2. **Check where the negative sits.** English moves the negative forward to the
   reporting verb: *I don't think it is open* means *I think it is not open*. So
   the inside clause is being treated as **negative**.
3. **Build the tag from the inside clause with the polarity already used up.**
   Operator *is*, subject *the shop* → *it*, and because the negative has been
   counted once, the tag stays **positive**.

**Answer.** *I don't think the shop is open on Saturday, **is it?***
:::

::: example Worked item 21.3 — turning a statement into three questions
**Problem.** *Bishnu bought a second-hand laptop in Bhotahity last week.*
(a) Ask about the person who bought it. (b) Ask about the thing he bought.
(c) Rewrite (b) beginning *Could you tell me …*

**Solution.**

**(a)** The question word replaces the **subject**, so there is no inversion and
no *did*, and the verb keeps its past form. **Answer:** *Who bought a second-hand
laptop in Bhotahity last week?*

**(b)** Here the question word replaces the **object**, so the sentence must
invert: *what* + *did* + subject + **base form**. **Answer:** *What did Bishnu
buy in Bhotahity last week?*

**(c)** Embedding removes the inversion and the *did*, and the verb takes back the
tense that *did* was carrying. **Answer:** *Could you tell me what Bishnu bought
in Bhotahity last week?*
:::

## Chapter summary

- A tag = **operator + pronoun**, opposite in polarity to the statement, same
  tense and person as its verb.
- No auxiliary in the statement → supply *do / does / did*.
- Negative tags are always contracted: *isn't he, doesn't she, won't they*.
- Irregulars to memorise: *I am → aren't I*; *I'm not → am I*; *Let's → shall we*;
  *Let me/us (permission) → will you*; imperative → *will you*; *There is → isn't
  there*; *Nobody/Everybody → they*; *Nothing/This/That → it*; *used to → didn't*;
  *had better → hadn't*; *have to → don't*; *ought to → oughtn't/shouldn't*.
- *Never, seldom, rarely, hardly, scarcely, barely, few, little, no, none* make a
  statement negative, so the tag turns positive.
- With *I think / I suppose*, the tag comes from the inside clause; with *I don't
  think*, the tag is positive.
- Direct questions invert: (wh-) + operator + subject + base verb.
- A wh-word that is the **subject** takes no *do/does/did*: *Who wrote it?*
- Embedded questions drop the inversion and the *do*, and yes/no questions inside
  them need *if / whether*.

## Practice questions

**Add suitable question tags (1 mark each)**

1. Your sister works at Bir Hospital, ____ ? <span class="marks">[1]</span>
2. I am the shortest in the class, ____ ? <span class="marks">[1]</span>
3. Let's leave for Pokhara at five, ____ ? <span class="marks">[1]</span>
4. Switch off the fan before you go, ____ ? <span class="marks">[1]</span>
5. There is no electricity in the hostel, ____ ? <span class="marks">[1]</span>
6. Nobody informed the principal, ____ ? <span class="marks">[1]</span>
7. Everybody has paid the examination fee, ____ ? <span class="marks">[1]</span>
8. He used to live in Ilam, ____ ? <span class="marks">[1]</span>
9. We had better book the tickets today, ____ ? <span class="marks">[1]</span>
10. She hardly ever misses her morning walk, ____ ? <span class="marks">[1]</span>
11. Don't tell anyone about this, ____ ? <span class="marks">[1]</span>
12. I don't think he has read the notice, ____ ? <span class="marks">[1]</span>

::: note Answers
**1.** doesn't she? — no auxiliary, third person singular, so *does*; flip to negative.
**2.** aren't I? — the fixed irregular for *I am* in a positive statement.
**3.** shall we? — *let's* proposes something, so the tag is *shall we*.
**4.** will you? — an imperative takes *will you* (also *won't you?*).
**5.** is there? — *no electricity* makes it negative, so the tag is positive, with *there* as subject.
**6.** did they? — *nobody* is negative and is replaced by *they*.
**7.** haven't they? — *everybody* takes a singular verb but the pronoun *they*.
**8.** didn't he? — *used to* is a past form, so the operator is *did*.
**9.** hadn't we? — the *'d* in *had better* is *had*.
**10.** does she? — *hardly ever* makes the statement negative.
**11.** will you? — negative imperatives also take *will you*.
**12.** has he? — the tag follows the inside clause, and the negative has already been used by *don't think*.
:::

**Correct the errors in the following sentences (1 mark each)**

13. The programme starts at ten, isn't it? <span class="marks">[1]</span>
14. She can't drive a car, can't she? <span class="marks">[1]</span>
15. Let's take the night bus, will we? <span class="marks">[1]</span>
16. Please close the gate, shall you? <span class="marks">[1]</span>
17. Nothing was stolen, wasn't it? <span class="marks">[1]</span>
18. Where he has gone since morning? <span class="marks">[1]</span>
19. Who did break this window? <span class="marks">[1]</span>
20. Can you tell me when does the library open? <span class="marks">[1]</span>
21. Does your father works in a bank? <span class="marks">[1]</span>
22. Why you did not attend the meeting? <span class="marks">[1]</span>

::: note Answers
**13.** The programme starts at ten, **doesn't it?** — the subject is a thing, so *it*, not *isn't it*.
**14.** She can't drive a car, **can she?** — a negative statement takes a positive tag.
**15.** Let's take the night bus, **shall we?** — *let's* always takes *shall we*.
**16.** Please close the gate, **will you?** — imperatives take *will you*.
**17.** Nothing was stolen, **was it?** — *nothing* is negative, so the tag is positive.
**18.** **Where has he gone** since morning? — a direct question inverts the operator and the subject.
**19.** **Who broke** this window? — *who* is the subject here, so no *did*.
**20.** Can you tell me **when the library opens**? — an embedded question keeps statement order.
**21.** Does your father **work** in a bank? — after *does*, the base form.
**22.** **Why didn't you attend** the meeting? — the operator must come before the subject.
:::

**Rewrite as instructed (1 mark each)**

23. *Sarita completed the project in three weeks.* — Ask a question about the person who completed it. <span class="marks">[1]</span>
24. *Sarita completed the project in three weeks.* — Ask a question about the time taken, beginning *How long …* <span class="marks">[1]</span>
25. *Where is the ticket counter?* — Rewrite beginning *Could you tell me …* <span class="marks">[1]</span>
26. *Has the result been published?* — Rewrite beginning *Do you know …* <span class="marks">[1]</span>
27. *You met someone at the airport.* — Ask about the person, using *whom*. <span class="marks">[1]</span>
28. *I wonder why she resigned.* — Rewrite as a direct question. <span class="marks">[1]</span>

::: note Answers
**23.** **Who completed the project in three weeks?** — a subject question: no *did*, and the verb keeps the past form.
**24.** **How long did Sarita take to complete the project?** — *did* + base form after the wh-phrase.
**25.** **Could you tell me where the ticket counter is?** — the embedded clause returns to statement order.
**26.** **Do you know if (whether) the result has been published?** — a yes/no question needs *if* or *whether* when embedded.
**27.** **Whom did you meet at the airport?** — an object question inverts and uses *did* + base form.
**28.** **Why did she resign?** — un-embedding restores the inversion and moves the tense onto *did*.
:::
