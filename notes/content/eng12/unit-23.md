---
subject: Compulsory English
grade: 12
unit: 23
title: Determiners and Quantifiers
hours: 4
area: Grammar
---

A **determiner** is the word that opens a noun phrase and tells you *which* or
*how many*: *a* pen, *the* pen, *this* pen, *my* pen, *every* pen, *few* pens,
*much* ink. **Quantifiers** are the determiners that answer "how much / how many".
Nepali has no articles at all, which is why *a*, *an* and *the* are the marks most
often lost in Q7 and in the writing questions. The whole area is a matter of
matching the determiner to the **kind of noun** that follows it, so that is what
this unit drills.

::: key Two questions before you choose a determiner
**(1) Is the noun countable or uncountable?** *Books* can be counted; *bread,
information, furniture, advice* cannot.
**(2) Is it singular or plural?** *Much* goes only with uncountables, *many* only
with plural countables, *a/an* only with singular countables. Get these two right
and half of the item is already answered.
:::

## 23.1 The classes of determiner

| Class | Members | Example |
|---|---|---|
| Articles | a, an, the, (zero) | **the** tallest boy |
| Demonstratives | this, that, these, those | **those** notebooks |
| Possessives | my, your, his, her, its, our, their, Ram's | **her** results |
| Quantifiers | some, any, much, many, (a) few, (a) little, several, enough, a lot of | **several** villages |
| Distributives | each, every, either, neither, both, all, half | **each** candidate |
| Numerals | one, two … ; first, second … | **the second** chance |
| Interrogatives | which, what, whose | **whose** bag |
| Negative | no, none of, neither | **no** water |
| Pre-determiners | all, both, half, such, what (a) | **all the** students |

Determiners come in a fixed order: **pre-determiner + central determiner +
post-determiner**, as in *all the three other candidates*. Only **one central
determiner** is allowed, which is why *my this book* is wrong. Say ***this book
of mine***.

## 23.2 Articles: a, an, the and zero

**A or an is decided by sound, not by spelling.** Use *an* before a vowel
**sound**, *a* before a consonant **sound**.

| Use *a* | Because the sound is | Use *an* | Because the sound is |
|---|---|---|---|
| a university, a uniform, a useful map | /juː/ — a consonant sound | an umbrella, an uncle | /ʌ/ |
| a European country | /juː/ | an hour, an honest man, an heir | the *h* is silent |
| a one-rupee coin, a one-way street | /w/ | an MA, an MP, an SLC certificate | the letter is read *em, em, es* |
| a horse, a hotel, a historic day | the *h* is pronounced | an X-ray, an FM station, an NGO | *eks, ef, en* |

**The** is used when the listener can tell exactly which one is meant:

1. mentioned before — *I bought a shawl. **The** shawl was of pashmina.*
2. unique things — *the sun, the moon, the earth, the sky*
3. superlatives and ordinals — *the best answer, the first bench*
4. rivers, seas, oceans, ranges, deserts, groups of islands — *the Koshi, the Bay
   of Bengal, the Himalayas, the Terai*
5. plural country names and organisations — *the Netherlands, the USA, the UN*
6. newspapers, holy books, historical periods — *the Kathmandu Post, the Gita,
   the Rana regime*
7. musical instruments and inventions — *play **the** madal, **the** telephone*
8. an adjective used as a noun, and a whole community — *the poor, the Nepalese*
9. with *only, same, whole, entire* and with a comparative pair — *the only son,
   **the** sooner **the** better*

**Zero article** (no article at all):

- plural or uncountable nouns used in general — *Books are cheap in Bhotahity.*
  *Honesty pays.*
- proper names of people, cities, single mountains, lakes, countries, continents
  — *Sita, Birgunj, Everest, Phewa Lake, Nepal, Asia*
- languages, school subjects, games, meals, festivals, months, days — *He teaches
  Nepali. They play volleyball. We had lunch. during Tihar*
- institutions used for their purpose — *go to school, in hospital, go to bed, in
  prison* (but *go to **the** school to meet the principal* — the building)
- means of transport after *by* — *by bus, by air, on foot*

```figure caption="Three questions settle almost every article item. Work down the chain: the first question whose answer is yes gives the article."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.6))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
def box(x,y,w,h,t,fc,ec,fs=7.4,tc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.11",fc=fc,ec=ec,lw=1.0))
    ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs,color=tc or INK,
            linespacing=1.4)
def right(y):
    ax.annotate('', xy=(5.55,y), xytext=(5.02,y),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=8))
    ax.text(5.28,y+0.34,"yes",fontsize=6.6,color=MUTED,ha='center')
def down(y0,y1):
    ax.annotate('', xy=(2.50,y1), xytext=(2.50,y0),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=8))
    ax.text(2.85,(y0+y1)/2,"no",fontsize=6.6,color=MUTED,ha='left',va='center')
box(0.20,7.55,4.70,1.45,"1.  A proper name, or a plural /\nuncountable noun meant in general?",
    "#ffffff",INK)
box(5.70,7.75,4.10,1.05,"NO ARTICLE\nNepal · Milk is good.","#f4f6f8",MUTED,7.4,MUTED)
right(8.28); down(7.44,6.71)
box(0.20,5.15,4.70,1.45,"2.  Can the reader tell exactly\nwhich one is meant?",
    "#ffffff",INK)
box(5.70,5.35,4.10,1.05,"THE\nthe sun · the best boy","#e8f3ee","#0B6A62",7.4,"#0B6A62")
right(5.88); down(5.04,4.31)
box(0.20,2.75,4.70,1.45,"3.  One countable thing,\nmentioned for the first time?",
    "#ffffff",INK)
box(5.70,2.95,4.10,1.05,"A / AN\na pen · an hour","#eef2fb",ACCENT,7.4,ACCENT)
right(3.48)
ax.plot([0.20,9.80],[2.05,2.05],color=GRID,lw=0.9)
ax.text(0.20,1.35,"a / an follows the SOUND:  a university, a one-way street,",
        fontsize=7.0,color=INK,ha='left',va='center')
ax.text(0.20,0.65,"an hour, an honest man, an MP, an X-ray",
        fontsize=7.0,color=INK,ha='left',va='center')
```

## 23.3 Which determiner goes with which noun

This grid is the heart of the unit. A tick means the combination is correct.

| Determiner | Singular countable (*book*) | Plural countable (*books*) | Uncountable (*information*) |
|---|---|---|---|
| a / an | ✓ a book | ✗ | ✗ |
| the | ✓ | ✓ | ✓ |
| this / that | ✓ | ✗ | ✓ this information |
| these / those | ✗ | ✓ | ✗ |
| my, your, his … | ✓ | ✓ | ✓ |
| some / any | ✗ (except *some day*) | ✓ | ✓ |
| much | ✗ | ✗ | ✓ much time |
| many | ✗ | ✓ many books | ✗ |
| a lot of / lots of / plenty of | ✗ | ✓ | ✓ |
| (a) few, fewer, several | ✗ | ✓ a few books | ✗ |
| (a) little, less | ✗ | ✗ | ✓ a little milk |
| a great deal of, a large amount of | ✗ | ✗ | ✓ |
| a large number of, a great many | ✗ | ✓ | ✗ |
| each, every, either, neither | ✓ each boy | ✗ | ✗ |
| both | ✗ | ✓ both hands | ✗ |
| all | ✗ (except *all day*) | ✓ | ✓ |
| enough | ✗ | ✓ | ✓ |
| no | ✓ | ✓ | ✓ |

Notes on the trickier rows:

- **much / many** are normal in **negatives and questions** (*Is there much
  water?*). In plain positive statements *a lot of* sounds better: *We have a lot
  of work* rather than *much work*.
- **some / any.** *Some* in positive statements and in offers or requests
  expecting yes (*Would you like **some** tea?*); *any* in negatives and ordinary
  questions (*I haven't **any** change. Have you **any** doubt?*). *Any* in a
  positive statement means "it does not matter which": *Take **any** seat.*
- **each / every.** Both take a **singular** noun and a **singular** verb. *Each*
  looks at the members one by one and can be used of two; *every* looks at the
  whole group and needs three or more. *Each of / every one of* is followed by a
  **plural** noun: *each of the **students** was present*.
- **either / neither** are used of **two**: *Either road leads to Tansen.*
  *Neither answer is correct.*
- **both / all.** *Both* for two, *all* for more than two. *All (of) the students*
  — *of* is optional before *the*, compulsory before a pronoun: *all of them*.
- **fewer / less.** *Fewer* counts (*fewer students*), *less* measures (*less
  sugar*). Shop signs saying "10 items or less" are wrong.
- **none of** + plural noun takes a singular or plural verb; in the exam write
  the singular: *None of the boys **was** selected.*

```figure caption="Few and little mean almost none and sound negative; a few and a little mean some and sound positive. The top line counts, the bottom line measures."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,3.2))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
RED="#9B2C2C"; GREEN="#0B6A62"
def scale(y, title, pts, example):
    ax.text(0.15, y+1.55, title, fontsize=7.6, color=INK, ha='left', va='center')
    ax.annotate('', xy=(9.55,y), xytext=(0.55,y),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1, mutation_scale=9))
    ax.text(0.15, y-0.62, "none", fontsize=6.8, color=MUTED, ha='left')
    ax.text(9.65, y-0.62, "all", fontsize=6.8, color=MUTED, ha='right')
    for x, lab, col in pts:
        ax.plot([x],[y],'o',ms=6,color=col,mec='white',mew=0.9,zorder=5)
        ax.text(x, y+0.55, lab, fontsize=7.2, color=col, ha='center', va='center')
    ax.text(0.15, y-1.45, example, fontsize=7.0, color=MUTED, ha='left', va='center')
scale(7.30, "COUNTABLE  —  how many?",
      [(1.75,"few\n(negative)",RED),(4.10,"a few\n(positive)",GREEN),
       (6.35,"several",MUTED),(8.70,"many",ACCENT)],
      "He has few friends = he is lonely.    He has a few friends = enough to be happy.")
scale(2.55, "UNCOUNTABLE  —  how much?",
      [(1.75,"little\n(negative)",RED),(4.10,"a little\n(positive)",GREEN),
       (6.35,"some",MUTED),(8.70,"much",ACCENT)],
      "There is little hope = almost none.    There is a little hope = some hope.")
```

## 23.4 Countable and uncountable nouns

These nouns are **uncountable** in English even though their Nepali equivalents
can be counted. They take **no -s**, **no a/an**, a **singular verb**, and *much /
a little / a great deal of* rather than *many / a few*:

*information, advice, news, furniture, luggage, baggage, equipment, machinery,
stationery, scenery, poetry, music, knowledge, work, homework, research,
progress, evidence, traffic, weather, money, bread, rice, sugar, hair,
jewellery, crockery, permission, accommodation, damage, fun, behaviour.*

To count them, use a **measure phrase**:

| Instead of | Say |
|---|---|
| ✗ two informations | ✓ two **pieces of** information / two **items of** information |
| ✗ many advices | ✓ much advice / several **pieces of** advice |
| ✗ some furnitures | ✓ some furniture / three **items of** furniture |
| ✗ a good news | ✓ good news / **a piece of** good news |
| ✗ three luggages | ✓ three **pieces of** luggage |
| ✗ lightnings, thunders | ✓ **a flash of** lightning, **a clap of** thunder |
| ✗ a bread | ✓ **a loaf of** bread / **a slice of** bread |

Some nouns are **plural only** and take a plural verb: *scissors, trousers,
jeans, spectacles, binoculars, pliers, clothes, goods, premises, surroundings,
belongings, earnings, thanks, cattle, police, people*. To count them, use *a pair
of*: *two **pairs of** trousers*. And note *news* is **singular** in spite of its
-s: *The news **is** encouraging.*

::: caution The determiner errors in every NEB script
✗ *He gave me many advices.* → ✓ *He gave me **much advice** (or several pieces
of advice).*
✗ *She has a long hair.* → ✓ *She has **long hair**.*
✗ *I have a good news for you.* → ✓ *I have **good news** for you.*
✗ *Less students came today.* → ✓ ***Fewer** students came today.*
✗ *Much people were waiting.* → ✓ ***Many** people were waiting.*
✗ *Every students must attend.* → ✓ ***Every student** must attend.*
✗ *Each of the boy got a prize.* → ✓ *Each of the **boys** got a prize.*
✗ *One of my friend lives in Dhangadhi.* → ✓ *One of my **friends** lives …*
✗ *My this pen is new.* → ✓ ***This pen of mine** is new.*
✗ *The most of the students passed.* → ✓ ***Most of the** students passed.*
:::

## 23.5 The articles a Nepali speaker forgets

Nepali marks definiteness with word order and with *-euta / -ta*, not with a
separate word, so articles are simply left out. Check every singular countable
noun in your answer: it must have **some** determiner in front of it.

| ✗ Wrong | ✓ Right | Why |
|---|---|---|
| He is best student in class. | He is **the** best student in **the** class. | superlative, and a known class |
| Nepal is beautiful country. | Nepal is **a** beautiful country. | singular countable, first mention |
| She is honest girl. | She is **an** honest girl. | *honest* begins with a vowel sound |
| He is an university student. | He is **a** university student. | *university* begins with /juː/ |
| I saw elephant in Chitwan. | I saw **an** elephant in Chitwan. | first mention |
| The Everest is in Nepal. | **Everest** is in Nepal. | single mountains take no *the* |
| He plays guitar very well. | He plays **the** guitar very well. | musical instruments take *the* |
| Poor are not always unhappy. | **The** poor are not always unhappy. | adjective used as a noun |
| She goes to the school by bus. | She goes to school by bus. | *school* here means study, not the building |
| Give me water in the glass. | Give me **some** water in **a** glass. | uncountable needs *some*, not *a* |

::: example Worked item 23.1 — much, many, few or little?
**Problem.** Fill in the blanks: *(a) There is very ____ sugar left, so make the
tea without it. (b) ____ students attended the extra class because of the strike.
(c) He has ____ friends in Biratnagar, so he is never lonely there.*

**Solution — step by step.**

**(a)** *Sugar* is uncountable, so the choice is between *little* and *a little*.
The second half of the sentence says the tea must be made without it, so the
amount is nearly none, which is the **negative** word. **Answer:** *very **little**
sugar*.

**(b)** *Students* is a plural countable noun, so *few* or *a few*. The strike
means attendance was poor, so again the negative word is needed. **Answer:**
***Few** students attended*.

**(c)** *Friends* is plural countable, and the sense is positive — he is never
lonely. **Answer:** ***a few** friends*.
:::

::: example Worked item 23.2 — supplying the missing articles
**Problem.** Insert articles where they are needed: *Yesterday I met old friend
of my father at bus park. He is engineer and works for government.*

**Solution — noun by noun.**

1. *old friend* — a singular countable noun, mentioned for the first time, and
   *old* begins with a vowel sound → ***an** old friend*.
2. *bus park* — both speaker and listener know which bus park is meant → ***the**
   bus park*.
3. *engineer* — a job title after *be* takes *a / an*, and *engineer* begins with
   a vowel sound → ***an** engineer*.
4. *government* — there is only one government here, so it is definite → ***the**
   government*.

**Answer.** *Yesterday I met **an** old friend of my father at **the** bus park.
He is **an** engineer and works for **the** government.*
:::

::: example Worked item 23.3 — correcting quantifier and number errors
**Problem.** Correct: *The teacher gave us many useful informations and two
advices, but each of the student had different doubt.*

**Solution — one fault at a time.**

1. *informations* — *information* is uncountable, so no -s, and *many* must become
   *much* (or use a measure phrase).
2. *two advices* — *advice* is uncountable → *two **pieces of** advice*.
3. *each of the student* — *each of* is always followed by a **plural** noun →
   *each of the **students***.
4. *had different doubt* — *doubt* here is a singular countable noun and needs a
   determiner → *a different doubt*.

**Answer.** *The teacher gave us **much useful information** and two **pieces of
advice**, but **each of the students** had **a** different doubt.*
:::

## Chapter summary

- A determiner opens the noun phrase; only **one central determiner** is allowed,
  so write *this book of mine*, never *my this book*.
- *A / an* is chosen by **sound**: *a university, a one-way street; an hour, an
  honest man, an MP*.
- *The* = the reader knows which one: second mention, unique things,
  superlatives, ordinals, rivers, ranges, plural country names, instruments,
  adjectives used as nouns.
- Zero article with proper names, generic plurals and uncountables, languages,
  games, meals, festivals, *by bus*, and institutions used for their purpose.
- *Much / (a) little / a great deal of* + uncountable; *many / (a) few / a large
  number of* + plural countable; *a lot of* with either.
- *Few / little* = almost none (negative); *a few / a little* = some (positive).
- *Each, every, either, neither* + singular noun + singular verb; *each of / one
  of* + plural noun.
- *Fewer* counts, *less* measures.
- *Information, advice, furniture, luggage, equipment, news, work, money, hair*
  are uncountable: no -s, and counted with *a piece of / an item of*.
- *Scissors, trousers, spectacles, clothes, police, cattle, people* are plural and
  take a plural verb.

## Practice questions

**Fill in the blanks with a suitable determiner or quantifier (1 mark each)**

1. She is ____ honest and hard-working officer. <span class="marks">[1]</span>
2. ____ Himalayas protect Nepal from the cold winds of the north. <span class="marks">[1]</span>
3. How ____ money do you need for the excursion? <span class="marks">[1]</span>
4. There were ____ passengers in the bus, so I got a seat easily. <span class="marks">[1]</span>
5. ____ of the two roads leads to Gorkha Bazaar. <span class="marks">[1]</span>
6. ____ student must bring his or her admit card. <span class="marks">[1]</span>
7. We could not buy the tickets because we had ____ time. <span class="marks">[1]</span>
8. He speaks ____ English, so he can manage in Delhi. <span class="marks">[1]</span>
9. ____ of the students has been informed about the test. <span class="marks">[1]</span>
10. There is not ____ water in the tank today. <span class="marks">[1]</span>

::: note Answers
**1.** an — *honest* begins with a vowel sound.
**2.** The — mountain ranges take *the*.
**3.** much — *money* is uncountable.
**4.** few — a plural countable noun, and the sense is "hardly any", which is why a seat was free.
**5.** Either — *either* is used of two, with a singular verb.
**6.** Every (or Each) — a singular countable noun follows.
**7.** little — *time* is uncountable and the meaning is negative.
**8.** a little — a positive amount of an uncountable noun.
**9.** Each (or Every one) — *each of* + plural noun + singular verb *has*.
**10.** much — *much* is normal in a negative sentence with an uncountable noun.
:::

**Correct the errors in the following sentences (1 mark each)**

11. The teacher gave us many informations about the scholarship. <span class="marks">[1]</span>
12. I have a good news for you. <span class="marks">[1]</span>
13. Less people attended the meeting this year. <span class="marks">[1]</span>
14. He bought three furnitures for his new flat. <span class="marks">[1]</span>
15. Each of the boy was given a certificate. <span class="marks">[1]</span>
16. She is best singer in our school. <span class="marks">[1]</span>
17. My this bag was bought in Bhairahawa. <span class="marks">[1]</span>
18. One of my friend has gone to Japan. <span class="marks">[1]</span>
19. He is an European by birth. <span class="marks">[1]</span>
20. The most of the villagers depend on farming. <span class="marks">[1]</span>

::: note Answers
**11.** … gave us **much information** about the scholarship. — *information* is uncountable.
**12.** I have **good news** (or **a piece of good news**) for you. — *news* is uncountable.
**13.** **Fewer** people attended … — *fewer* is used with countable nouns.
**14.** He bought three **pieces of furniture** … — *furniture* is uncountable.
**15.** **Each of the boys** was given a certificate. — *each of* takes a plural noun.
**16.** She is **the best singer in the** school. — superlative, and a known school.
**17.** **This bag of mine** was bought in Bhairahawa. — two central determiners cannot stand together.
**18.** One of my **friends** has gone to Japan. — *one of* + plural noun.
**19.** He is **a** European by birth. — *European* begins with the consonant sound /juː/.
**20.** **Most of the** villagers depend on farming. — no *the* before *most of*.
:::

**Rewrite as instructed (1 mark each)**

21. *He has little money, so he cannot buy the book.* — Rewrite using *enough*. <span class="marks">[1]</span>
22. *All the students were present.* — Rewrite beginning *None …* <span class="marks">[1]</span>
23. *There is some milk in the jug.* — Rewrite in the negative. <span class="marks">[1]</span>
24. *Both the sisters are studying medicine.* — Rewrite using *Each …* <span class="marks">[1]</span>
25. *I need a few more minutes.* — Rewrite using *a little*. <span class="marks">[1]</span>

::: note Answers
**21.** **He does not have enough money to buy the book.** — *enough* fits both countable and uncountable nouns.
**22.** **None of the students was absent.** — the opposite statement; *none of* takes a singular verb in formal writing.
**23.** **There is not any milk in the jug.** (or *There is no milk in the jug.*) — *some* becomes *any* in the negative.
**24.** **Each of the sisters is studying medicine.** — *each of* + plural noun + singular verb.
**25.** **I need a little more time.** — *a little* needs an uncountable noun, so *minutes* becomes *time*.
:::
