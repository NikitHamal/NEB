---
subject: Compulsory English
grade: 11
unit: 29
title: Question Tags, Questions and Subject-Verb Agreement
hours: 4
area: Grammar
---

This unit covers three closely related things, all of which depend on the
**auxiliary verb**: how questions are formed, how question tags are added, and how
the verb agrees with its subject. NEB Q7 almost always carries at least one question
tag and one agreement item, usually as *Add a suitable question tag*, *Change into a
question*, or *Fill in the blank with the correct form of the verb*. Every one of
them is decided by a fixed rule, so these are the easiest marks in the paper.

::: key Find the auxiliary first
Questions and tags are both built from the auxiliary (*is, are, was, were, have,
has, had, will, can, must …*). If the sentence has no auxiliary, the verb supplies
one: present simple → *do / does*, past simple → *did*. Everything else follows.
:::

## 29.1 The four kinds of question

| Kind | What it asks for | Example |
|---|---|---|
| **Yes / no** | confirmation | **Is** the library open on Saturday? |
| **Wh-** | information | **Where** does this bus go? |
| **Choice (alternative)** | one of two given options | Do you want tea **or** coffee? |
| **Tag** | agreement with a statement | You are from Dhangadhi, **aren't you**? |

## 29.2 Yes / no questions

**Rule.** Move the auxiliary in front of the subject. If there is no auxiliary,
insert *do / does / did* and put the main verb back into its base form (V1).

| Statement | Question |
|---|---|
| She **is** working in Qatar. | **Is** she working in Qatar? |
| They **have** finished the project. | **Have** they finished the project? |
| He **can** speak Newari. | **Can** he speak Newari? |
| Sita **teaches** in Biratnagar. | **Does** Sita **teach** in Biratnagar? |
| They **reached** Namche yesterday. | **Did** they **reach** Namche yesterday? |

::: caution Never keep the tense twice
After *do, does* or *did* the main verb goes back to V1.
~~Did you went to the temple?~~ → **Did you go to the temple?**
~~Does she plays the madal?~~ → **Does she play the madal?**
The auxiliary already carries the tense and the person.
:::

## 29.3 Wh- questions

**Rule.** Wh-word + auxiliary + subject + main verb.

- ***Where did** you buy this dhaka topi?*
- ***Why has** the bus stopped at Mugling?*
- ***How many** students **are** attending the extra class?*

**The subject question exception.** When the wh-word is itself the subject, there is
no inversion and no *do / does / did*.

| Question | Type |
|---|---|
| **Who** broke the window? | subject question — no *did* |
| **Who did** you meet at the fair? | object question — *did* needed |
| **What** happened in Dharan? | subject question |
| **What did** the teacher say? | object question |

```figure caption="Word order in questions. A direct question inverts the subject and the auxiliary; an embedded or reported question does not, and it needs no question mark."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.2))
ax.set_xlim(0,10.2); ax.set_ylim(0,9.6); ax.axis('off')
def slot(x,y,w,t,sub,fc,ec,tc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,1.05,boxstyle="round,pad=0.09",
                                fc=fc,ec=ec,lw=1.0))
    ax.text(x+w/2,y+0.52,t,ha='center',va='center',fontsize=7.8,color=tc or INK)
    ax.text(x+w/2,y-0.45,sub,ha='center',va='center',fontsize=6.8,color=MUTED)
ax.text(0.1,9.25,"DIRECT question  —  auxiliary comes BEFORE the subject",
        fontsize=7.6,color="#0B6A62",ha='left',va='center')
slot(0.10,6.55,1.85,"Where","wh-word","#eef7f1","#0B6A62")
slot(2.20,6.55,1.55,"did","auxiliary","#eef7f1","#0B6A62")
slot(4.00,6.55,1.55,"you","subject","#ffffff",MUTED)
slot(5.80,6.55,1.35,"go","V1","#ffffff",MUTED)
slot(7.40,6.55,2.70,"yesterday?","rest","#ffffff",MUTED)
ax.annotate('',xy=(2.98,7.90),xytext=(4.78,7.90),
            arrowprops=dict(arrowstyle='-|>',color="#0B6A62",lw=1.0,
                            connectionstyle="arc3,rad=0.35",mutation_scale=9))
ax.text(0.1,3.95,"EMBEDDED question  —  auxiliary stays AFTER the subject",
        fontsize=7.6,color="#B4690E",ha='left',va='center')
slot(0.10,2.05,2.95,"Tell me","introducer","#fdf1e7","#B4690E")
slot(3.30,2.05,1.85,"where","wh-word","#fdf1e7","#B4690E")
slot(5.40,2.05,1.55,"you","subject","#ffffff",MUTED)
slot(7.20,2.05,2.90,"went yesterday.","verb + rest","#eaf0fb",ACCENT,ACCENT)
ax.text(0.15,0.60,"no inversion, no did, and a full stop instead of a question mark",
        fontsize=7.2,color=ACCENT,ha='left',va='center')
```

## 29.4 Indirect and embedded questions

When a question is placed inside another sentence — after *Tell me…, I wonder…, Do
you know…, Could you tell me…* — the word order becomes that of a **statement**.

| Direct | Embedded |
|---|---|
| Where is the post office? | Could you tell me **where the post office is**? |
| What does she want? | I wonder **what she wants**. |
| Did he pass? | Do you know **whether/if he passed**? |

Note that a yes/no question becomes *if* or *whether*, and *do/does/did* disappears.

::: caution The commonest embedded-question error
~~Could you tell me where is the bank?~~ → **Could you tell me where the bank is?**
~~I don't know what does he want.~~ → **I don't know what he wants.**
Once the question is inside another sentence, stop inverting.
:::

## 29.5 Question tags — the basic rule

A tag is a short question added to a statement to ask for agreement. Three steps:

1. **Take the auxiliary from the statement.** If there is none, use *do / does /
   did*.
2. **Reverse the polarity.** A positive statement takes a negative tag; a negative
   statement takes a positive tag.
3. **Use a pronoun** for the subject, and keep the same tense.

- *Ramesh **is** studying in Kathmandu, **isn't he**?*
- *You **haven't** paid the fee, **have you**?*
- *She **works** at the health post, **doesn't she**?*
- *They **went** to Lumbini last week, **didn't they**?*

```figure caption="Building a question tag in three steps. The polarity always flips, the auxiliary is copied from the statement, and the subject becomes a pronoun."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,3.0))
ax.set_xlim(0,10); ax.set_ylim(0,8.2); ax.axis('off')
def box(x,y,w,h,t,fc,ec,fs=7.8,tc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.10",fc=fc,ec=ec,lw=1.0))
    ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs,color=tc or INK,
            linespacing=1.4)
ax.add_patch(FancyBboxPatch((0.10,6.55),9.80,1.15,boxstyle="round,pad=0.10",
                            fc="#ffffff",ec=INK,lw=1.0))
for x,w in ((1.15,"Sita"),(2.55,"has"),(4.15,"finished"),(6.25,"her homework"),
            (8.85,",  ______ ?")):
    ax.text(x,7.12,w,ha='center',va='center',fontsize=8.4,color=INK)
for x,lab,col in ((1.15,"subject",MUTED),(2.55,"auxiliary","#0B6A62")):
    ax.text(x,5.95,lab,fontsize=6.9,color=col,ha='center',va='center')
    ax.plot([x,x],[6.25,6.45],lw=0.8,color=col)
ax.text(9.90,5.95,"the statement is positive",fontsize=6.9,color="#B4690E",
        ha='right',va='center')
def rule(y,n,t,ex,col):
    ax.add_patch(FancyBboxPatch((0.10,y),1.05,1.05,boxstyle="circle,pad=0.02",
                                fc=col,ec=col,lw=1.0))
    ax.text(0.62,y+0.52,n,ha='center',va='center',fontsize=8.0,color='white')
    ax.text(1.45,y+0.52,t,ha='left',va='center',fontsize=7.8,color=INK)
    ax.text(9.90,y+0.52,ex,ha='right',va='center',fontsize=7.8,color=col)
rule(4.10,"1","copy the auxiliary","has","#0B6A62")
rule(2.60,"2","flip the polarity","has → hasn't","#B4690E")
rule(1.10,"3","subject → pronoun","Sita → she",ACCENT)
box(0.10,-0.60,9.80,1.15,"Sita has finished her homework, hasn't she ?",
    "#eaf0fb",ACCENT,8.4,ACCENT)
ax.set_ylim(-0.9,8.2)
```

## 29.6 Special tags you must memorise

| Statement | Tag | Note |
|---|---|---|
| I **am** late, | **aren't I**? | never *amn't I* |
| I **am not** late, | **am I**? | |
| **Let's** go to Nagarkot, | **shall we**? | suggestion |
| **Open** the window, | **will you / won't you**? | imperative |
| **Don't** shout, | **will you**? | negative imperative |
| **There is** no water, | **is there**? | *there* repeats as the subject |
| **Everyone** has come, | **haven't they**? | *everyone/somebody* → *they* |
| **Nothing** is wrong, | **is it**? | *nothing/nobody* is already negative |
| **Nobody** came, | **did they**? | |
| **This / That** is your bag, | **isn't it**? | *this/that* → *it* |
| **These / Those** are old, | **aren't they**? | *these/those* → *they* |
| He **never** comes on time, | **does he**? | *never* makes it negative |
| She **hardly / scarcely / seldom / rarely** speaks, | **does she**? | these words are negative |
| **Few** students attended, | **did they**? | *few*, *little* are negative |
| It **has to** be done, | **doesn't it**? | *have to* uses *do* |
| He **used to** live here, | **didn't he**? | |
| You **had better** go, | **hadn't you**? | |
| **Nothing** can stop him, | **can it**? | |

::: caution Tag traps
- **Hidden negatives.** *Never, hardly, scarcely, seldom, rarely, few, little,
  neither, no one, nothing* already make a sentence negative, so the tag must be
  **positive**: *He rarely visits us, **does he**?* — not ~~doesn't he~~.
- **Pronoun, not the noun.** ~~My uncle works in Qatar, doesn't my uncle?~~ →
  **doesn't he?**
- **Same tense.** ~~She came yesterday, doesn't she?~~ → **didn't she?**
- ***I am*** takes ***aren't I***, which is irregular but standard.
:::

## 29.7 Subject–verb agreement: the core rules

The verb must agree with the subject in **number** and **person**. In the simple
present, a singular third-person subject takes **-s** and everything else does not.

**Rule 1 — Find the real subject.** Words between the subject and the verb do not
change the agreement.

- *The **box** of old books **is** in the store room.* (not ~~are~~)
- *The **teacher**, along with all her students, **was** present.*

Phrases like *with, along with, as well as, together with, in addition to,
including, accompanied by* do **not** make the subject plural.

**Rule 2 — *and* makes a plural subject.**

- *Ram **and** Shyam **are** waiting outside.*

But when the two nouns name one thing or one idea, the verb is singular:
*Bread and butter **is** my usual breakfast.*

**Rule 3 — *or / nor* : the verb agrees with the nearer subject.**

- *Neither the students nor the **teacher was** informed.*
- *Neither the teacher nor the **students were** informed.*
- *Either Sita or her **brothers have** taken it.*

**Rule 4 — *each, every, either, neither, one of* take a singular verb.**

- ***Each** of the boys **has** a bicycle.*
- ***Every** student and every teacher **was** given a badge.*
- ***One of** my **friends lives** in Nepalgunj.* (plural noun, singular verb)

**Rule 5 — Uncountable nouns are singular.**

- *This **information is** useful.* *The **news was** shocking.*
- ***Mathematics is** my favourite subject.* (also *physics, politics,
  economics, statistics* as subjects, *measles, mumps*)

**Rule 6 — Plural-only nouns take a plural verb**, but *a pair of* makes them
singular.

- *My **trousers are** torn.* / *A **pair** of trousers **is** enough.*
- *These **scissors are** blunt.*

**Rule 7 — Collective nouns.** *Team, family, government, committee, class, jury,
crowd, police* take a singular verb when the group acts as one, and a plural verb
when its members act separately. *Police* is normally plural.

- *The committee **has** taken a decision.* (one body)
- *The committee **are** divided among themselves.* (individuals)
- *The **police have** arrested two men.*

**Rule 8 — Amounts, distances, times and money are one unit, so singular.**

- *Twenty kilometres **is** a long walk.*
- *Rs 500 **is** not enough for the books.*
- *Two hours **is** the maximum time allowed.*

**Rule 9 — *a number of* vs *the number of*.**

- ***A number of** students **were** absent.* (= many, plural)
- ***The number of** students **is** increasing.* (= the figure, singular)

**Rule 10 — *There is / there are* agrees with the noun that follows.**

- *There **is** a temple near the bridge.*
- *There **are** many temples in Bhaktapur.*

**Rule 11 — *The* + adjective as a plural group.**

- *The **poor are** the worst affected by inflation.*

**Rule 12 — In a relative clause, the verb agrees with the antecedent.**

- *She is one of those students **who work** hard.* (*who* = *students*)
- *He is the only one of the boys **who has** passed.* (*who* = *one*)

**Rule 13 — Titles and proper names of one thing are singular.**

- ***The Arabian Nights is** a famous collection of tales.*

::: caution Agreement errors Nepali learners make most
- **Losing the third-person -s under pressure.** ~~He go to school at nine.~~ →
  **He goes to school at nine.**
- **Treating *information, advice, furniture, luggage, equipment, machinery* as
  plural.** ~~These informations are useful.~~ → **This information is useful.**
  ~~He gave me many advices.~~ → **He gave me a lot of advice.**
- **Pluralising after *one of*.** ~~One of my friend is a pilot.~~ →
  **One of my friends is a pilot.** The noun is plural, the verb singular.
- **Making the verb agree with the nearest noun instead of the subject.**
  ~~The quality of the mangoes were poor.~~ → **The quality of the mangoes was
  poor.**
- **Plural verb after *each* or *every*.** ~~Each of the students have a book.~~ →
  **Each of the students has a book.**
:::

::: tip How these items appear in the paper
Tags are printed as *Add a suitable question tag:* followed by a statement and a
blank — look for a hidden negative first, then copy the auxiliary. Agreement is
usually *Fill in the blank with the correct form of the verb in brackets* — cross
out everything between the subject and the blank with your pencil, and the right
form becomes obvious. Question formation is *Change into a question* or *Frame a
question to get the underlined part as the answer* — if the underlined part is the
subject, use *who/what* with no *do/does/did*.
:::

::: example Worked transformation 29.1 — a tag with a hidden negative
**Problem.** Add a question tag: *Hari hardly ever attends the morning class, ____ ?*

**Solution — step by step.**

1. **Find the auxiliary.** There is none; *attends* is a present simple verb with a
   third-person singular subject → the auxiliary is **does**.
2. **Check the polarity.** *Hardly ever* is a negative adverb, so although the
   sentence has no *not*, it counts as **negative**.
3. **Flip it.** A negative statement takes a **positive** tag → *does*.
4. **Pronoun.** *Hari* → *he*.

**Answer.** *Hari hardly ever attends the morning class, **does he**?*

Writing *doesn't he* would be the standard error, because the negative is hidden in
*hardly*.
:::

::: example Worked transformation 29.2 — framing a question
**Problem.** Frame questions to get the underlined answers.
(a) *<u>Sabina</u> won the debate competition.*
(b) *They reached Pokhara <u>at six o'clock</u>.*

**Solution.**

**(a)** The underlined part is the **subject** of the sentence. A subject question
takes no *did* and no inversion: simply replace the subject with *who* and leave the
verb exactly as it is.
**Answer:** ***Who won** the debate competition?*

**(b)** The underlined part is an adverbial of time, so the question word is *when*
(or *what time*). The verb *reached* is past simple with no auxiliary, so insert
*did* and change the verb back to V1.
**Answer:** ***When did** they **reach** Pokhara?*
:::

::: example Worked transformation 29.3 — choosing the verb form
**Problem.** Choose the correct verb. (a) *The list of candidates (has / have) been
published.* (b) *Neither the principal nor the teachers (was / were) willing to
speak.* (c) *One of the mobiles that (is / are) displayed here (is / are) mine.*

**Solution.**

**(a)** Cross out the phrase *of candidates*. The subject is *the list*, singular.
**Answer:** *has been published.*

**(b)** With *neither … nor*, the verb agrees with the nearer subject, which is
*teachers*, plural.
**Answer:** *were willing to speak.*

**(c)** Two verbs, two subjects. Inside the relative clause, *that* refers to
*mobiles* (plural) → *are displayed*. The main subject is *one*, singular → *is
mine*.
**Answer:** *One of the mobiles that **are** displayed here **is** mine.*
:::

## Chapter summary

- Questions invert the auxiliary and the subject; without an auxiliary, insert
  *do / does / did* and use V1.
- A subject question (*Who came?*) takes no *do / does / did* and no inversion.
- An embedded question keeps statement word order and needs no question mark.
- A tag = auxiliary + (n't) + pronoun, with the polarity reversed.
- Memorise: *I am → aren't I*, *Let's → shall we*, imperative *→ will you*,
  *There is → is there*, *everyone → they*, *nothing → it*.
- *Never, hardly, seldom, rarely, few, little* are negatives and take a positive tag.
- The verb agrees with the real subject, not with the nearest noun.
- *Each, every, either, neither, one of* + singular verb; *a number of* + plural,
  *the number of* + singular.
- *As well as, along with, together with* do not make a subject plural.
- Amounts of money, time and distance take a singular verb.

## Practice questions

**Add a suitable question tag (1 mark each)**

1. Sarita is preparing for the entrance examination, ____ ? <span class="marks">[1]</span>
2. You haven't seen my calculator anywhere, ____ ? <span class="marks">[1]</span>
3. Let's leave for Bandipur early tomorrow, ____ ? <span class="marks">[1]</span>
4. Nobody informed the head teacher, ____ ? <span class="marks">[1]</span>
5. I am your class monitor, ____ ? <span class="marks">[1]</span>
6. He rarely goes to the temple, ____ ? <span class="marks">[1]</span>
7. Close the door, ____ ? <span class="marks">[1]</span>
8. There is little milk in the jug, ____ ? <span class="marks">[1]</span>
9. Everyone has submitted the assignment, ____ ? <span class="marks">[1]</span>
10. Your brother used to play for the district team, ____ ? <span class="marks">[1]</span>

::: note Answers
**1.** isn't she — positive statement, so a negative tag with the same auxiliary *is*.
**2.** have you — a negative statement takes a positive tag.
**3.** shall we — the fixed tag after *Let's*.
**4.** did they — *nobody* is negative, so a positive tag, and *nobody* is answered by *they*.
**5.** aren't I — the standard irregular tag for *I am*.
**6.** does he — *rarely* is a hidden negative, so the tag is positive.
**7.** will you — the fixed tag after an imperative.
**8.** is there — *little* is negative, and *there* repeats as the subject.
**9.** haven't they — *everyone* takes a plural pronoun *they* in the tag.
**10.** didn't he — *used to* forms its tag with *did*.
:::

**Fill in the blanks with the correct form of the verb in brackets (1 mark each)**

11. The list of selected students ____ on the notice board. (be, present) <span class="marks">[1]</span>
12. Each of the girls ____ her own bag. (have) <span class="marks">[1]</span>
13. Neither Gopal nor his brothers ____ interested in farming. (be, present) <span class="marks">[1]</span>
14. Twenty kilometres ____ too far to walk in one day. (be, present) <span class="marks">[1]</span>
15. The news from the border ____ worrying. (be, past) <span class="marks">[1]</span>
16. A number of passengers ____ waiting at the bus park. (be, past) <span class="marks">[1]</span>
17. Mathematics ____ easier than she expected. (be, past) <span class="marks">[1]</span>
18. The police ____ already arrested the suspect. (have) <span class="marks">[1]</span>
19. One of my cousins ____ in Ilam. (live) <span class="marks">[1]</span>
20. The teacher, as well as the students, ____ invited to the programme. (be, past) <span class="marks">[1]</span>

::: note Answers
**11.** is — the subject is *the list*, singular; *of selected students* does not count.
**12.** has — *each of* always takes a singular verb.
**13.** are — with *neither … nor*, the verb agrees with the nearer subject *brothers*.
**14.** is — a distance is treated as a single unit.
**15.** was — *news* is uncountable and singular.
**16.** were — *a number of* means "many" and takes a plural verb.
**17.** was — subjects ending in *-ics* are singular.
**18.** have — *police* takes a plural verb.
**19.** lives — the subject is *one*, singular, though *cousins* is plural.
**20.** was — *as well as* does not make the subject plural.
:::

**Change the sentences into questions as instructed (1 mark each)**

21. *Sujata teaches English at a school in Hetauda.* — Change into a yes/no question. <span class="marks">[1]</span>
22. *They visited the Pashupatinath temple last Saturday.* — Change into a yes/no question. <span class="marks">[1]</span>
23. *<u>Bikash</u> repaired the water pump.* — Frame a question to get the underlined answer. <span class="marks">[1]</span>
24. *She left the office <u>because she was unwell</u>.* — Frame a question to get the underlined answer. <span class="marks">[1]</span>
25. *Where does he live?* — Rewrite beginning *Do you know …* <span class="marks">[1]</span>
26. *Did she pass the test?* — Rewrite beginning *I wonder …* <span class="marks">[1]</span>

::: note Answers
**21.** **Does Sujata teach** English at a school in Hetauda? — insert *does* and return the verb to V1.
**22.** **Did they visit** the Pashupatinath temple last Saturday? — past simple, so *did* + V1.
**23.** **Who repaired** the water pump? — a subject question, so no *did* and no inversion.
**24.** **Why did she leave** the office? — a reason is asked with *why*, and *did* + V1 is needed.
**25.** Do you know **where he lives**? — an embedded question keeps statement order and drops *does*.
**26.** I wonder **whether/if she passed** the test. — a yes/no question embeds with *if* or *whether*.
:::
