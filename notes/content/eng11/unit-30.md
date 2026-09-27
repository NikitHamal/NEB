---
subject: Compulsory English
grade: 11
unit: 30
title: Prepositions, Adjectives and Adverbs
hours: 4
area: Grammar
---

Prepositions show the relationship of a noun to the rest of the sentence — in time,
in space, or in a fixed partnership with a particular verb or adjective. Adjectives
describe nouns; adverbs describe verbs, adjectives and other adverbs. Together these
three classes supply a large share of NEB Q7: *Fill in the blanks with suitable
prepositions*, *Use the correct form of the adjective in brackets*, and
*Choose the correct word*. Much of it is memory work, so the tables below are meant
to be learnt, not just read.

::: key Two kinds of preposition question
Some prepositions follow **logic** — *in* a city, *on* Monday, *at* six o'clock.
Others follow **habit**: *depend on*, *good at*, *afraid of*. The first kind you can
work out; the second kind you must memorise as a pair, exactly as you memorise a
new word.
:::

## 30.1 Prepositions of time

| Preposition | Used for | Examples |
|---|---|---|
| **at** | clock times, festivals, *night, noon, midnight* | at 5 o'clock, at Dashain, at night |
| **on** | days and dates | on Sunday, on 15 Baisakh, on my birthday |
| **in** | months, seasons, years, centuries, parts of the day | in Asar, in the monsoon, in 2081, in the morning |
| **by** | not later than | Submit the form **by** Friday. |
| **until / till** | up to a point, and then it stops | The shop stays open **until** eight. |
| **since** | the starting point of a period | She has taught here **since** 2075. |
| **for** | the length of a period | She has taught here **for** six years. |
| **during** | within a period | It rains heavily **during** the monsoon. |
| **from … to / till** | start and end | The class runs **from** ten **to** twelve. |
| **within** | before the end of | Reply **within** seven days. |
| **ago** | counting back from now (after the phrase) | He left two hours **ago**. |
| **in** (future) | after a period from now | She will return **in** a week. |

::: caution *By* is not *until*; *since* is not *for*
*Finish it **by** six* = at any moment before six. *Wait **until** six* = go on waiting
right up to six.
*Since* is followed by a **point** in time, *for* by a **length** of time.
~~I have lived here since five years.~~ → **for five years** / **since 2076**.
Also: *in the morning* but ***at** night*; and nothing at all before *last, next,
this, every*: ~~on last Sunday~~ → **last Sunday**.
:::

```figure caption="At, on and in narrow down in the same way for time and for place: in is the widest container, on is a surface or a named day, and at is a single point."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,3.2))
ax.set_xlim(0,10); ax.set_ylim(0,9.4); ax.axis('off')
def band(x,y,w,h,t,fc,ec,fs=7.6,tc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.10",fc=fc,ec=ec,lw=1.0))
    ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs,color=tc or INK,
            linespacing=1.4)
ax.text(2.45,9.05,"TIME",ha='center',va='center',fontsize=8.2,color=INK)
ax.text(7.55,9.05,"PLACE",ha='center',va='center',fontsize=8.2,color=INK)
band(0.10,5.95,4.70,2.55,"IN\na year, a month, a season\n(in 2081, in Asar)",
     "#eef7f1","#0B6A62")
band(5.20,5.95,4.70,2.55,"IN\na country, a city, a room\n(in Nepal, in Butwal)",
     "#eef7f1","#0B6A62")
band(0.55,3.35,3.80,2.20,"ON\na day or a date\n(on Sunday)","#eaf0fb",ACCENT,7.6,ACCENT)
band(5.65,3.35,3.80,2.20,"ON\na surface or a street\n(on the shelf)","#eaf0fb",
     ACCENT,7.6,ACCENT)
band(1.05,1.05,2.80,1.85,"AT\na clock time\n(at 6 p.m.)","#fdf1e7","#B4690E",7.6,"#B4690E")
band(6.15,1.05,2.80,1.85,"AT\na point\n(at the gate)","#fdf1e7","#B4690E",7.6,"#B4690E")
ax.text(0.05,0.30,"each box narrows the one above it",fontsize=7.0,color=MUTED,
        ha='left',va='center')
```

## 30.2 Prepositions of place and direction

| Preposition | Meaning | Example |
|---|---|---|
| **at** | a point | Wait **at** the bus stop. |
| **on** | a surface, a line | The map is **on** the wall; Bharatpur is **on** the Narayani. |
| **in** | inside an area or container | She lives **in** Dharan. |
| **above / over** | higher than (*over* = directly above or covering) | The plane flew **over** Everest. |
| **below / under** | lower than (*under* = directly beneath) | The boat passed **under** the bridge. |
| **between** | among two | Chitwan lies **between** Nawalpur and Makwanpur. |
| **among** | among three or more | Divide the sweets **among** the children. |
| **beside** | next to | Sit **beside** me. |
| **besides** | in addition to | **Besides** Nepali, he speaks Maithili. |
| **across** | from one side to the other | They swam **across** the river. |
| **through** | in at one end, out at the other | The road runs **through** a tunnel. |
| **into / onto** | movement to inside / onto a surface | He jumped **into** the pond. |
| **opposite** | facing | The bank is **opposite** the post office. |
| **behind / in front of** | at the back / at the front | A jeep was parked **in front of** the gate. |
| **towards** | in the direction of | The crowd moved **towards** the stage. |
| **from … to** | starting point and destination | The bus runs **from** Kakarbhitta **to** Kathmandu. |

```figure caption="The commonest place prepositions shown as positions relative to one box. Notice that in means inside, on means touching the top surface, and over or above means higher with a gap."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
fig, ax = plt.subplots(figsize=(4.6,3.2))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
ax.add_patch(Rectangle((3.3,3.4),3.4,2.6,fc="#f2f4f7",ec=INK,lw=1.2))
ax.text(5.0,3.05,"the box",ha='center',va='center',fontsize=7.0,color=MUTED)
def ball(x,y,lab,lx,ly,ha='center',col=None):
    c = col or ACCENT
    ax.plot([x],[y],'o',ms=7,color=c,mec='white',mew=0.9,zorder=5)
    ax.text(lx,ly,lab,ha=ha,va='center',fontsize=7.4,color=c)
ball(5.0,8.35,"above / over",5.0,9.05)
ball(5.0,6.00,"on",5.45,6.55,ha='left')
ball(5.0,5.05,"in / inside",5.0,4.25,col="#0B6A62")
ball(5.0,1.85,"under / below",5.0,1.15)
ball(8.40,4.70,"beside / next to",8.40,5.45)
ball(1.55,4.70,"near",1.55,5.45)
```

## 30.3 Prepositions fixed to a word

These pairs are learnt by heart. They are the ones NEB sets most often.

**Verb + preposition**

| | | |
|---|---|---|
| depend **on** | listen **to** | belong **to** |
| agree **with** (a person) | agree **to** (a plan) | apologise **to** (a person) **for** (a thing) |
| believe **in** | consist **of** | complain **about / to** |
| congratulate **on** | die **of / from** | insist **on** |
| laugh **at** | look **after / for / at** | object **to** |
| prevent **from** | rely **on** | suffer **from** |
| succeed **in** | think **of / about** | wait **for** |

**Adjective + preposition**

| | | |
|---|---|---|
| good / bad **at** | afraid **of** | interested **in** |
| famous **for** | proud **of** | jealous **of** |
| angry **with** (a person) | angry **about** (a thing) | kind **to** |
| married **to** | similar **to** | different **from** |
| full **of** | tired **of** | keen **on** |
| responsible **for** | capable **of** | aware **of** |

**Noun + preposition:** *reason for, cause of, solution to, answer to, increase in,
effect on, demand for, need for, respect for, invitation to*.

::: caution Verbs that take no preposition at all
These English verbs are transitive: the object follows directly, with nothing in
between. The Nepali equivalent often has a postposition, which is why the mistake is
so common.
~~discuss about the problem~~ → **discuss the problem**
~~enter into the classroom~~ → **enter the classroom**
~~marry with her~~ → **marry her** (but *get married **to** her*)
~~reach at the station~~ → **reach the station**
~~return back home~~ → **return home**
~~cope up with the pressure~~ → **cope with the pressure**
~~request for a leave~~ → **request a leave** / **ask for leave**
~~resemble to his father~~ → **resemble his father**
~~answer to the question~~ → **answer the question**
~~attack on the village~~ → **attack the village** (as a verb)
Also ~~repeat again~~, ~~join together~~ and ~~revert back~~ say the same thing twice.
:::

## 30.4 Adjectives: kinds and order

Adjectives come **before** the noun (*a red shawl*) or after a linking verb
(*the shawl is red*). When several are used together, English follows a fixed order:

**opinion → size → age → shape → colour → origin → material → purpose → NOUN**

- *a beautiful **small old round black Nepali woollen** cap*
- *a lovely little wooden table*

Numbers and determiners come before all of these: *those two beautiful old temples*.

## 30.5 Degrees of comparison

| Type of adjective | Comparative | Superlative |
|---|---|---|
| one syllable (tall) | tall**er** | the tall**est** |
| one syllable ending consonant-vowel-consonant (big) | big**ger** | the big**gest** |
| ending in -y (easy) | eas**ier** | the eas**iest** |
| two or more syllables (careful) | **more** careful | **the most** careful |
| good / well | better | the best |
| bad / badly | worse | the worst |
| much / many | more | the most |
| little | less | the least |
| far | farther / further | the farthest / furthest |

Patterns to learn:

- **as + adjective + as** for equality: *Pokhara is **as beautiful as** Bandipur.*
- **not as / so … as** for inequality: *Today is **not as cold as** yesterday.*
- **comparative + than**: *The Koshi is **longer than** the Bagmati.*
- **the + comparative, the + comparative**: ***The sooner** you start, **the better**
  it is.*
- **comparative + and + comparative** for change: *The queue grew **longer and
  longer**.*
- **one of the + superlative + plural noun**: *Everest is **one of the highest
  mountains** in the world.*

::: caution Comparison errors
- **Double comparison.** ~~more better~~, ~~most funniest~~ → **better**, **funniest**.
- ***Than*, not *then*.** ~~He is taller then me.~~ → **taller than I am / than me**.
- **Latin comparatives take *to*, not *than*:** *senior **to** me*, *junior **to**
  him*, *superior **to** this*, *inferior **to** that*, *prefer tea **to** coffee*.
- **Compare like with like.** ~~The climate of Pokhara is better than Kathmandu.~~ →
  **… better than that of Kathmandu.**
- **Use the comparative for two, the superlative for three or more.** *She is the
  **taller** of the two sisters.*
:::

## 30.6 Adverbs

An adverb tells **how, when, where, how often** or **to what degree**.

| Kind | Question answered | Examples |
|---|---|---|
| manner | how? | slowly, carefully, well, fast |
| time | when? | yesterday, soon, already, then |
| place | where? | here, upstairs, outside, everywhere |
| frequency | how often? | always, usually, often, sometimes, never |
| degree | how much? | very, quite, rather, too, almost, enough |

**Formation.** Most adverbs of manner add *-ly* to the adjective: *careful →
carefully*, *happy → happily*, *true → truly*. Some adjectives already end in *-ly*
(*friendly, lovely, silly*) and have no adverb form; use *in a friendly way*.

**Position.** Adverbs of frequency go **before the main verb** but **after** the verb
*be*:

- *She **always** comes late.* / *She **is always** late.*
- *I have **never** been to Rara.* (after the first auxiliary)

*Enough* goes **after** an adjective or adverb but **before** a noun: *old **enough**
to vote*, ***enough** money*.

::: caution Adjective or adverb? And the -ly traps
- **After a linking verb use an adjective**, not an adverb: *The soup tastes
  **good**.* *She looks **tired**.* But: *She sang **beautifully**.*
- **Pairs that change meaning with -ly:**
  *hard* = with effort / *hardly* = almost not — *He works **hard**.* vs *He
  **hardly** works.*
  *late* = not on time / *lately* = recently.
  *near* = close / *nearly* = almost.
  *most* = the greatest / *mostly* = mainly.
- ***Too* is not *very*.** *Too* means more than is acceptable: *The tea is **too**
  hot to drink* (I cannot drink it). *The tea is **very** hot* (but I can).
- ***So* + adjective; *such* + (a) + adjective + noun.** *It was **so** cold.* /
  *It was **such a** cold night.*
:::

::: tip Attacking these items in the exam
Prepositions are usually a gap-fill with no bracket cue, so first ask: is this gap
about **time**, about **place**, or is it **glued to the word before it**? If the
word before the gap is a verb or an adjective from the lists in 30.3, the answer is
the fixed partner, whatever the meaning looks like. Adjective items normally show a
cue in brackets — *(good)*, *(much)* — and a nearby *than*, *the* or *as* tells you
which degree to use: *than* means comparative, *the* with *in/of* means superlative,
*as … as* means keep the base form.
:::

::: example Worked transformation 30.1 — choosing the preposition
**Problem.** Fill in the blanks: *(a) She has been living in Dhangadhi ____ 2074.
(b) Our team is confident ____ winning. (c) Divide the prize money ____ the five
players.*

**Solution.**

**(a)** *2074* is a **point** in time, not a length, so the answer is *since*, not
*for*. **Answer:** *since 2074.*

**(b)** *Confident* is an adjective with a fixed partner. The pair is *confident
**of***, and after a preposition the verb takes *-ing*. **Answer:** *confident of
winning.*

**(c)** There are five players, that is more than two, so *among* — *between* is used
for two. **Answer:** *among the five players.*
:::

::: example Worked transformation 30.2 — degrees of comparison
**Problem.** Rewrite without changing the meaning.
(a) *No other peak in Nepal is as high as Everest.* (use a superlative)
(b) *Sarita is the more intelligent of the two sisters.* (use *not as … as*)

**Solution.**

**(a)** *No other … as high as X* means X is higher than all the rest, so the
superlative form is required, with *the* and a following *in Nepal*.
**Answer:** *Everest is **the highest peak in Nepal**.*

**(b)** If Sarita is the more intelligent, then the other sister is the less
intelligent. Turn it round with *not as … as*, keeping the adjective in its base
form.
**Answer:** *The other sister is **not as intelligent as** Sarita.*
:::

::: example Worked transformation 30.3 — correcting a sentence with several faults
**Problem.** Correct: *Although he entered into the hall lately, he discussed about
the problem more better than any student.*

**Solution — one fault at a time.**

1. *enter* takes no preposition → *entered the hall*.
2. *lately* means "recently"; the meaning here is "not on time" → *late*.
3. *discuss* takes no preposition → *discussed the problem*.
4. *more better* is a double comparative → *better*.
5. *than any student* would include himself; a comparative comparing one member with
   the rest needs *any other* → *than any other student*.

**Answer.** *Although he entered the hall **late**, he **discussed the problem
better than any other student**.*
:::

## Chapter summary

- Time: *at* a clock time, *on* a day or date, *in* a month, season or year;
  *since* + point, *for* + length, *by* = not later than, *until* = up to.
- Place: *at* a point, *on* a surface, *in* an area; *between* two, *among* more than
  two; *beside* = next to, *besides* = in addition.
- Many verbs, adjectives and nouns have a fixed preposition — learn the pair.
- *Discuss, enter, marry, reach, resemble, answer, request, attack* take no
  preposition; avoid *return back*, *cope up with*, *repeat again*.
- Adjective order: opinion, size, age, shape, colour, origin, material, purpose.
- One syllable → *-er / -est*; two or more → *more / most*; never both.
- *Senior, junior, superior, inferior, prefer* take *to*, not *than*.
- Adverbs of frequency go before the main verb but after *be*.
- *Hard / hardly*, *late / lately*, *near / nearly* are different words.
- *Too* = more than is acceptable; *very* is only an intensifier.

## Practice questions

**Fill in the blanks with a suitable preposition (1 mark each)**

1. The programme will begin ____ ten o'clock. <span class="marks">[1]</span>
2. We have been waiting ____ the counter for an hour. <span class="marks">[1]</span>
3. My uncle has lived in Jhapa ____ 2070. <span class="marks">[1]</span>
4. She is very good ____ mathematics. <span class="marks">[1]</span>
5. Everything depends ____ the weather on Saturday. <span class="marks">[1]</span>
6. The money was divided ____ the two brothers. <span class="marks">[1]</span>
7. He is afraid ____ dogs. <span class="marks">[1]</span>
8. Please submit the application ____ Friday at the latest. <span class="marks">[1]</span>
9. ____ Nepali, she also speaks Bhojpuri and English. <span class="marks">[1]</span>
10. Ilam is famous ____ its tea gardens. <span class="marks">[1]</span>

::: note Answers
**1.** at — clock times take *at*.
**2.** at — a bus counter is treated as a point, not an area.
**3.** since — 2070 is a starting point, so *since*, not *for*.
**4.** at — the fixed pair is *good at*.
**5.** on — the fixed pair is *depend on*.
**6.** between — *between* is used for two.
**7.** of — the fixed pair is *afraid of*.
**8.** by — *by* means not later than that day.
**9.** Besides — *besides* means "in addition to"; *beside* would mean "next to".
**10.** for — the fixed pair is *famous for*.
:::

**Use the correct form of the word in brackets (1 mark each)**

11. Everest is the ____ mountain in the world. (high) <span class="marks">[1]</span>
12. This road is ____ than the one through Mugling. (bad) <span class="marks">[1]</span>
13. She sings ____ than her sister. (sweet) <span class="marks">[1]</span>
14. Today is not as ____ as yesterday. (cold) <span class="marks">[1]</span>
15. He is one of the ____ players in the district. (good) <span class="marks">[1]</span>
16. The ____ we leave, the better. (soon) <span class="marks">[1]</span>
17. She drives very ____ . (careful) <span class="marks">[1]</span>
18. He is ____ than his brother by three years. (senior) <span class="marks">[1]</span>

::: note Answers
**11.** highest — a superlative with *the* and *in the world*.
**12.** worse — the irregular comparative of *bad*.
**13.** more sweetly — the verb needs an adverb, and two syllables take *more*.
**14.** cold — *as … as* keeps the base form.
**15.** best — *one of the* is followed by a superlative and a plural noun.
**16.** sooner — the *the + comparative, the + comparative* pattern.
**17.** carefully — an adverb is needed to describe *drives*.
**18.** senior to (senior … to his brother) — Latin comparatives take *to*, not *than*.
:::

**Correct the errors in the following sentences (1 mark each)**

19. We discussed about the new syllabus in the meeting. <span class="marks">[1]</span>
20. He entered into the office without knocking. <span class="marks">[1]</span>
21. Please return back my book tomorrow. <span class="marks">[1]</span>
22. She is more taller than her cousin. <span class="marks">[1]</span>
23. I have been living here since five years. <span class="marks">[1]</span>
24. The bus reached at Birgunj at midnight. <span class="marks">[1]</span>
25. He is very tired to walk any further. <span class="marks">[1]</span>
26. The soup tastes deliciously. <span class="marks">[1]</span>

::: note Answers
**19.** We **discussed the new syllabus** in the meeting. — *discuss* takes no preposition.
**20.** He **entered the office** without knocking. — *enter* takes a direct object.
**21.** Please **return my book** tomorrow. — *return* already means "give back".
**22.** She is **taller** than her cousin. — never use *more* with an *-er* form.
**23.** I have been living here **for five years** (or *since 2076*). — *for* goes with a length of time.
**24.** The bus **reached Birgunj** at midnight. — *reach* takes no preposition.
**25.** He is **too tired** to walk any further. — *too … to* shows an impossible result; *very* cannot be used here.
**26.** The soup tastes **delicious**. — after a linking verb use an adjective.
:::
