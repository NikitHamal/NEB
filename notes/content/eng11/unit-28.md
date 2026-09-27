---
subject: Compulsory English
grade: 11
unit: 28
title: Relative Clauses and Connectives
hours: 4
area: Grammar
---

A **relative clause** is a clause that describes a noun, joined to it by a relative
pronoun such as *who, which* or *that*. A **connective** (or linking word) is a word
or phrase that joins ideas and shows the relationship between them — addition,
contrast, cause, result, purpose. Both belong to the same skill: turning short
sentences into longer, better-organised ones. NEB Q7 tests them as *Join the
sentences using a relative pronoun*, *Fill in the blank with a suitable
connective*, or *Choose the correct linker from the brackets*.

::: key Two things to check in every item
For a relative clause: **which pronoun** (person or thing, subject or object,
possession?) and **commas or no commas**. For a connective: **what relationship**
the two ideas have, and **what kind of word** the blank needs — a conjunction, a
preposition or an adverb. Most lost marks come from putting an adverb where a
conjunction is needed (*despite* vs *although*).

:::

## 28.1 Relative pronouns

| Pronoun | Refers to | Function | Example |
|---|---|---|---|
| **who** | people | subject | The girl **who** won the prize is from Ilam. |
| **whom** | people | object (formal) | The teacher **whom** we met is retiring. |
| **whose** | people and things | possession | The boy **whose** bicycle was stolen is crying. |
| **which** | things and animals | subject or object | The bus **which** goes to Jumla leaves at five. |
| **that** | people or things | subject or object, **defining clauses only** | The book **that** you lent me is excellent. |
| **where** | places | place | This is the village **where** I was born. |
| **when** | times | time | I remember the day **when** the earthquake struck. |
| **why** | reasons | reason | Tell me the reason **why** you were absent. |

The relative pronoun always stands **immediately after the noun it describes**.

- *The man **who lives next door** teaches at Padma Kanya Campus.*
- *Kathmandu, **which lies in a valley**, has poor air in winter.*

```figure caption="Joining two sentences with a relative pronoun. The repeated noun in the second sentence is replaced by who / which / whose, and the whole clause is lifted in immediately after that noun in the first sentence."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.3))
ax.set_xlim(0,10); ax.set_ylim(0,9.0); ax.axis('off')
def box(x,y,w,h,t,fc,ec,fs=8.0,tc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.10",fc=fc,ec=ec,lw=1.0))
    ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs,color=tc or INK)
def step(y,t):
    ax.text(0.1,y,t,fontsize=7.4,color=MUTED,ha='left',va='center')
step(8.70,"Step 1   two separate sentences")
box(0.10,7.20,4.55,1.15,"I met a doctor.","#ffffff",MUTED)
box(5.25,7.20,4.65,1.15,"The doctor works in Dang.","#ffffff",MUTED)
step(6.55,"Step 2   replace the repeated noun  (The doctor \u2192 who)")
ax.annotate('',xy=(7.55,5.55),xytext=(7.55,6.10),
            arrowprops=dict(arrowstyle='-|>',color="#0B6A62",lw=1.1,mutation_scale=10))
box(5.25,4.30,4.65,1.15,"who works in Dang","#eef7f1","#0B6A62",8.0,"#0B6A62")
step(3.65,"Step 3   put the clause straight after the noun it describes")
box(0.10,1.90,2.55,1.15,"I met a doctor","#ffffff",MUTED)
box(2.95,1.90,4.00,1.15,"who works in Dang.","#eaf0fb",ACCENT,8.0,ACCENT)
ax.text(0.15,1.05,"\u2192 the relative clause sits immediately after its noun",
        fontsize=7.4,color=ACCENT,ha='left',va='center')
```

## 28.2 Defining relative clauses

A **defining** (restrictive) clause tells you *which one*. Without it the sentence
does not identify anything. It takes **no commas**.

- *The students **who scored above 80** will get a scholarship.* (only those
  students, not all)
- *The trekking route **that passes through Ghorepani** is the most popular one.*
- *A blacksmith is a person **who works with iron**.*

In a defining clause, *that* may replace *who* or *which*.

## 28.3 Non-defining relative clauses

A **non-defining** clause adds extra information about a noun that is already
identified. It is always separated by **commas**, and **that** can never be used.

- *My father, **who retired last year**, now keeps bees in Nuwakot.*
- *Mount Everest, **which stands on the Nepal–China border**, was climbed in 1953.*
- *Pokhara, **where I spent my childhood**, is full of tourists in October.*

Compare the pair carefully:

| Sentence | Meaning |
|---|---|
| My brother **who lives in Biratnagar** is a doctor. | I have more than one brother; this is the Biratnagar one. |
| My brother, **who lives in Biratnagar**, is a doctor. | I have one brother; he happens to live in Biratnagar. |

::: caution Three errors with relative clauses
1. **Using *that* after a comma.** ~~Janakpur, that is famous for its temple, …~~ →
   **Janakpur, which is famous for its temple, …**
2. **Keeping the old pronoun as well.** ~~This is the man who I met him yesterday.~~
   → **This is the man whom I met yesterday.** The relative pronoun *is* the object;
   do not repeat it.
3. **Separating the clause from its noun.** ~~The letter was lying on the table
   which I wrote.~~ → **The letter which I wrote was lying on the table.**
:::

## 28.4 When the relative pronoun may be left out

The pronoun can be dropped only when it is the **object** of the defining clause,
never when it is the subject, and never in a non-defining clause.

| Sentence | Pronoun | May it be dropped? |
|---|---|---|
| The film **that we watched** was boring. | object | Yes — *The film we watched was boring.* |
| The film **that won the award** was Nepali. | subject | No |
| Mira, **whom I met in Ilam**, has moved. | non-defining | No |

- *The mobile **(which) I bought in Ratnapark** stopped working.*
- *The man **who sold it to me** has disappeared.* (subject — keep *who*)

```figure caption="A decision route for relative clauses: first decide whether the clause is needed to identify the noun, then choose the pronoun and the punctuation."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.9,3.6))
ax.set_xlim(0,10); ax.set_ylim(0,10.6); ax.axis('off')
def box(x,y,w,h,t,fc,ec,fs=7.6,tc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.11",fc=fc,ec=ec,lw=1.0))
    ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs,color=tc or INK,
            linespacing=1.4)
def arw(x0,y0,x1,y1,lab=None,lx=0.0,ly=0.0):
    ax.annotate('',xy=(x1,y1),xytext=(x0,y0),
                arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.0,mutation_scale=9))
    if lab:
        ax.text((x0+x1)/2+lx,(y0+y1)/2+ly,lab,fontsize=7.0,color=MUTED,
                ha='center',va='center',bbox=dict(fc='white',ec='none',pad=1.2))
box(1.35,9.25,7.3,1.1,"Is the clause needed to say WHICH one?","#ffffff",INK,8.0)
box(0.10,6.45,4.55,1.3,"YES — DEFINING\nno commas","#eef7f1","#0B6A62",7.8,"#0B6A62")
box(5.35,6.45,4.55,1.3,"NO — NON-DEFINING\ncommas both sides","#fdf1e7","#B4690E",7.8,"#B4690E")
arw(3.6,9.25,2.4,7.85); arw(6.4,9.25,7.6,7.85)
box(0.10,3.75,4.55,1.9,"who / whom / which /\nthat / whose\n(that is allowed)",
    "#ffffff",MUTED,7.6)
box(5.35,3.75,4.55,1.9,"who / whom / which /\nwhose\n(never that)",
    "#ffffff",MUTED,7.6)
arw(2.38,6.45,2.38,5.75); arw(7.63,6.45,7.63,5.75)
box(0.10,1.05,4.55,1.9,"pronoun may be dropped\nif it is the OBJECT\n(the film I saw)",
    "#eaf0fb",ACCENT,7.6,ACCENT)
box(5.35,1.05,4.55,1.9,"pronoun can never\nbe dropped","#eaf0fb",ACCENT,7.6,ACCENT)
arw(2.38,3.75,2.38,3.05); arw(7.63,3.75,7.63,3.05)
```

## 28.5 *Whose*, *where*, *when* and *why*

**whose** shows possession and works for people and for things.

- *The farmer **whose** buffalo died has applied for compensation.*
- *I live in a house **whose** roof leaks every monsoon.*

**where, when, why** replace a preposition + *which*.

| Long form | Short form |
|---|---|
| the town **in which** I grew up | the town **where** I grew up |
| the year **in which** he was born | the year **when** he was born |
| the reason **for which** she left | the reason **why** she left |

## 28.6 Prepositions in relative clauses

The preposition may come at the end (normal English) or before the pronoun (formal
English). Before *whom* and *which* the formal order is common; *that* never follows
a preposition.

- *This is the friend **whom** I travelled with.* → formal: *This is the friend
  **with whom** I travelled.*
- *The village **which** we walked to* → *the village **to which** we walked*
- Not: ~~the village to that we walked~~

## 28.7 Reduced relative clauses

A relative clause with *be* can often be shortened to a participle phrase. This is
common in reading passages, so learn to recognise it.

| Full clause | Reduced |
|---|---|
| the man **who is standing** at the gate | the man **standing** at the gate |
| the houses **which were damaged** by the quake | the houses **damaged** by the quake |
| the first student **who arrived** | the first student **to arrive** |

## 28.8 Connectives by function

| Relationship | Conjunctions (join two clauses) | Adverbs / phrases (usually start a new sentence) | Prepositions (before a noun) |
|---|---|---|---|
| **Addition** | and, not only … but also | moreover, furthermore, besides, in addition | as well as, along with |
| **Contrast** | but, although, though, even though, whereas, while | however, nevertheless, on the other hand, on the contrary | despite, in spite of |
| **Cause / reason** | because, since, as | — | because of, due to, owing to, on account of |
| **Result** | so, so … that, such … that | therefore, thus, consequently, as a result, hence | — |
| **Purpose** | so that, in order that, lest | — | to, in order to, so as to, for |
| **Condition** | if, unless, provided that, as long as | otherwise | in case of |
| **Time** | when, while, before, after, as soon as, until, since | meanwhile, afterwards, then | during, by, until |
| **Example** | — | for example, for instance, namely | such as, like |
| **Summary** | — | in short, to sum up, in conclusion, altogether | — |

Examples of each kind in a sentence:

- **Contrast, conjunction:** *Although the road was blocked, the ambulance reached
  the hospital.*
- **Contrast, adverb:** *The road was blocked; **however**, the ambulance reached the
  hospital.*
- **Contrast, preposition:** ***Despite** the blocked road, the ambulance reached the
  hospital.*
- **Cause:** *The flight was cancelled **because** the weather was bad.* /
  *The flight was cancelled **because of** the bad weather.*
- **Result:** *The weather was so bad **that** the flight was cancelled.*
- **Purpose:** *He woke at four **so that** he could catch the first bus.*

::: caution The connective errors that cost marks
- **Two joiners in one sentence.** Nepali and Hindi allow it; English does not.
  ~~Although he was tired, but he finished the work.~~ → **Although he was tired, he
  finished the work.** / **He was tired, but he finished the work.**
  The same applies to ~~Because he was late, so he missed the bus.~~
- ***Despite* / *in spite of* take a noun, not a clause.**
  ~~Despite he was ill, he came.~~ → **Despite his illness, he came.** /
  **In spite of being ill, he came.** / **Although he was ill, he came.**
  Also ~~in spite of~~ never becomes ~~inspite of~~, and *despite* takes no *of*.
- ***Because of* takes a noun; *because* takes a clause.**
  ~~The match stopped because of it rained.~~ → **because it rained** /
  **because of the rain**.
- ***However* is not a conjunction.** ~~He tried hard, however he failed.~~ →
  **He tried hard; however, he failed.** or **He tried hard. However, he failed.**
- ***As well as* is not *and*.** The verb agrees with the first subject:
  *Ramesh, **as well as** his brothers, **is** going.*
:::

::: tip How the Q7 items are set
*Join the following sentences using a relative pronoun* — find the noun that appears
in both sentences, replace the second occurrence with the right pronoun, and slot the
clause in right after the noun. *Fill in the blank with a suitable connective* —
read both halves first and name the relationship (contrast? cause? result?), then
check what word class fits: a clause after it needs *although/because*, a noun after
it needs *despite/because of*, a full stop or semicolon before it needs
*however/therefore*. Never leave the blank filled with *and* out of habit.
:::

::: example Worked transformation 28.1 — joining with a relative pronoun
**Problem.** Join into one sentence: *I bought a second-hand laptop. The laptop
stopped working after a week.*

**Solution — step by step.**

1. **Find the repeated noun.** *laptop* appears in both sentences.
2. **Decide which sentence carries the main idea.** The important news is that it
   stopped working, so that becomes the main clause and the first sentence becomes
   the relative clause.
3. **Choose the pronoun.** *laptop* is a thing and is the **object** of *bought*, so
   use *which* or *that*.
4. **Place the clause immediately after the noun.**

**Answer.** *The laptop **which I bought second-hand** stopped working after a week.*

Because the pronoun is the object, it may also be dropped: *The laptop I bought
second-hand stopped working after a week.*
:::

::: example Worked transformation 28.2 — defining or non-defining?
**Problem.** Join, and punctuate correctly: *Lumbini attracts thousands of pilgrims
a year. Lumbini is the birthplace of the Buddha.*

**Solution — step by step.**

1. **Repeated noun:** *Lumbini*.
2. **Is the clause needed to identify it?** No — *Lumbini* is a proper noun and is
   already fully identified. The clause only adds information.
3. **Therefore it is non-defining:** commas on both sides, and *that* is forbidden.
4. **Choose the pronoun:** a place treated as a thing → *which*.

**Answer.** *Lumbini, **which is the birthplace of the Buddha**, attracts thousands
of pilgrims a year.*

If the pronoun replaced the *place* meaning rather than the noun itself, *where*
would be used: *Lumbini, **where the Buddha was born**, attracts thousands of
pilgrims a year.*
:::

::: example Worked transformation 28.3 — rewriting with a different connective
**Problem.** Rewrite each sentence with the word in brackets, keeping the meaning.
(a) *Although it was raining heavily, the programme continued.* (**despite**)
(b) *He missed the bus because he got up late.* (**because of**)
(c) *The soup was very salty. Nobody could eat it.* (**so … that**)

**Solution.**

**(a)** *Despite* is a preposition, so the clause *it was raining heavily* must
become a noun phrase: *the heavy rain*.
**Answer:** ***Despite the heavy rain**, the programme continued.*

**(b)** *Because of* also needs a noun phrase: *he got up late* → *his getting up
late* or *his late rising*.
**Answer:** *He missed the bus **because of his getting up late**.*

**(c)** The *so … that* pattern is *so* + adjective + *that* + result clause. Put
the adjective *salty* after *so* and attach the second sentence with *that*.
**Answer:** *The soup was **so salty that** nobody could eat it.*
:::

## Chapter summary

- A relative clause goes immediately after the noun it describes.
- *who/whom* for people, *which* for things, *whose* for possession, *where/when/why*
  for place, time and reason.
- Defining clause: identifies the noun, no commas, *that* allowed, object pronoun may
  be dropped.
- Non-defining clause: extra information, commas both sides, *that* forbidden,
  pronoun never dropped.
- Do not repeat the noun or its pronoun inside the relative clause.
- A connective must match both the **relationship** and the **word class**:
  *although* + clause, *despite* + noun, *however* + new sentence.
- Never use two joiners for one relationship: *although … but*, *because … so* are
  wrong in English.
- *As well as* does not make a plural subject.

## Practice questions

**Join each pair of sentences using a suitable relative pronoun (1 mark each)**

1. I know a girl. The girl speaks four languages. <span class="marks">[1]</span>
2. This is the house. My grandfather built it in 2020 BS. <span class="marks">[1]</span>
3. The farmer is worried. His maize crop failed. <span class="marks">[1]</span>
4. Chitwan is famous for its rhinos. Chitwan lies in the Terai. <span class="marks">[1]</span>
5. I still remember the day. The earthquake struck on that day. <span class="marks">[1]</span>
6. That is the shop. I bought my school bag from it. <span class="marks">[1]</span>

::: note Answers
**1.** I know a girl **who speaks four languages.** — a person as subject of the defining clause.
**2.** This is the house **which/that my grandfather built in 2020 BS.** — a thing as object; the pronoun could also be dropped.
**3.** The farmer **whose maize crop failed** is worried. — *whose* shows possession and sits next to *farmer*.
**4.** Chitwan, **which lies in the Terai,** is famous for its rhinos. — a proper noun, so non-defining with commas and never *that*.
**5.** I still remember the day **when the earthquake struck.** — *when* replaces *on which* for time.
**6.** That is the shop **where I bought my school bag** (or *from which I bought…*). — *where* replaces *from which* for place.
:::

**Fill in the blanks with a suitable connective (1 mark each)**

7. ____ he had studied all night, he could not answer the last question. <span class="marks">[1]</span>
8. The flight to Lukla was cancelled ____ the bad weather. <span class="marks">[1]</span>
9. She revised every formula; ____ , she scored full marks in the test. <span class="marks">[1]</span>
10. Put on a helmet ____ you may be fined at the checkpoint. <span class="marks">[1]</span>
11. He got up at four ____ he could catch the first bus to Janakpur. <span class="marks">[1]</span>
12. ____ his poor eyesight, he refused to wear spectacles. <span class="marks">[1]</span>
13. The room was ____ cold that we could not sleep. <span class="marks">[1]</span>
14. Nepal exports many farm products, ____ tea, cardamom and ginger. <span class="marks">[1]</span>

::: note Answers
**7.** Although / Even though / Though — a contrast between effort and result, joining two clauses.
**8.** because of / due to / owing to — a noun phrase follows, so a preposition is needed, not *because*.
**9.** therefore / consequently / as a result — a result adverb after a semicolon.
**10.** otherwise / or else — the second clause states what happens if the first is not done.
**11.** so that / in order that — purpose, followed by a clause with *could*.
**12.** Despite / In spite of — a noun phrase follows, so the preposition form of contrast.
**13.** so — the *so + adjective + that* result pattern.
**14.** such as / namely / for example — introducing examples of the farm products.
:::

**Rewrite the sentences as instructed (1 mark each)**

15. *Although he was ill, he attended the meeting.* — Rewrite using **in spite of**. <span class="marks">[1]</span>
16. *Because of the strike, the schools remained closed.* — Rewrite using **because**. <span class="marks">[1]</span>
17. *The tea was too hot for me to drink.* — Rewrite using **so … that**. <span class="marks">[1]</span>
18. *He is poor. He is honest.* — Join with a suitable connective of contrast. <span class="marks">[1]</span>
19. *The boy is my cousin. He won the essay competition.* — Join with a relative pronoun. <span class="marks">[1]</span>

::: note Answers
**15.** **In spite of his illness** (or *being ill*), he attended the meeting. — *in spite of* takes a noun or gerund.
**16.** **Because there was a strike,** the schools remained closed. — *because* takes a full clause.
**17.** The tea was **so hot that I could not drink it.** — *too … to* becomes *so … that* with a negative result clause.
**18.** He is poor **but honest** (or *Although he is poor, he is honest*). — a single contrast joiner only.
**19.** The boy **who won the essay competition** is my cousin. — subject pronoun *who*, placed next to *boy*.
:::

**Correct the errors in the following sentences (1 mark each)**

20. Although he worked hard, but he failed. <span class="marks">[1]</span>
21. Despite he was tired, he kept walking. <span class="marks">[1]</span>
22. This is the boy who I met him in Butwal. <span class="marks">[1]</span>
23. Kathmandu, that is the capital of Nepal, is crowded. <span class="marks">[1]</span>
24. Because it was raining, so the match was stopped. <span class="marks">[1]</span>
25. He is the man which helped us during the flood. <span class="marks">[1]</span>
26. The pen was lying on the desk which my uncle gave me. <span class="marks">[1]</span>

::: note Answers
**20.** Although he worked hard, he failed. — drop *but*; one contrast joiner is enough.
**21.** **Although** he was tired, he kept walking. — a clause follows, so use the conjunction, not *despite*.
**22.** This is the boy **whom I met** in Butwal. — the relative pronoun is already the object; do not add *him*.
**23.** Kathmandu, **which** is the capital of Nepal, is crowded. — *that* is never used in a non-defining clause.
**24.** Because it was raining, the match was stopped. — drop *so*; *because* alone shows the cause.
**25.** He is the man **who** helped us during the flood. — *which* cannot refer to a person.
**26.** The pen **which my uncle gave me** was lying on the desk. — the clause must stand next to its own noun.
:::
