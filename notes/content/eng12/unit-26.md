---
subject: Compulsory English
grade: 12
unit: 26
title: Adjectives, Adverbs and Adjective Order
hours: 4
area: Grammar
---

An **adjective** describes a noun or pronoun; an **adverb** describes a verb, an
adjective, another adverb or a whole sentence. That much is familiar from earlier
grades. What Grade 12 adds is the fussy detail the examiner actually tests: the
fixed **order** in which several adjectives must stand before a noun, the
difference between *bored* and *boring*, the comparatives that take *to* instead
of *than*, and the **position** an adverb is allowed to occupy in a clause. These
are places where a sentence can be perfectly understandable and still be marked
wrong.

::: key Four rules to carry through the unit
1. Several adjectives before a noun follow the order **opinion – size – age –
   shape – colour – origin – material – purpose**.
2. **-ing** describes the thing that causes the feeling; **-ed** describes the
   person who has it. *The lesson was boring; the students were bored.*
3. A **linking verb** (*be, seem, look, feel, taste, sound, smell, become, get*)
   is followed by an **adjective**, not an adverb: *The soup tastes **good***, not
   *tastes well*.
4. An adverb never comes **between a verb and its object**: *She speaks English
   fluently*, not *speaks fluently English*.
:::

## 26.1 Kinds of adjective and where they can stand

| Kind | Examples |
|---|---|
| Quality (descriptive) | *honest, red, Nepali, wooden* |
| Quantity | *much, little, some, enough, whole* |
| Number | *five, many, few, first, several* |
| Demonstrative | *this, that, these, those* |
| Possessive | *my, our, your, his, their* |
| Distributive | *each, every, either, neither* |
| Interrogative | *which, what, whose* |

Most adjectives can stand **before the noun** (attributive: *a **tall** boy*) or
**after a linking verb** (predicative: *the boy is **tall***). A few are fixed in
one position only.

| Predicative only | Attributive only |
|---|---|
| afraid, alive, asleep, alone, ashamed, aware, awake, alike, content, glad, unable | main, only, mere, sheer, chief, former, latter, elder, eldest, inner, outer, utter |

✓ *The child was **asleep**.* ✗ *the **asleep** child* → ✓ *the **sleeping** child*
✓ *my **elder** brother* ✗ *He is **elder** than me* → ✓ *He is **older** than me*

## 26.2 The order of adjectives

When two or more adjectives of **different kinds** come before a noun, English
fixes their order. Native speakers do not learn it as a rule, but they never break
it, and the examiner marks it.

```figure caption="The order of adjectives. Read downwards: any adjectives you use must appear in this sequence between the determiner and the noun."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,4.3))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
GREEN="#0B6A62"; RED="#9B2C2C"
ax.text(0.95,9.55,"DETERMINER",fontsize=6.6,color=MUTED,ha='left')
ax.text(5.20,9.55,"a / the / my / this",fontsize=7.0,color=INK,ha='left')
rows=[("1  Opinion","lovely, ugly, useful"),
      ("2  Size","little, large, tall"),
      ("3  Age","old, new, ancient"),
      ("4  Shape","round, square, flat"),
      ("5  Colour","brown, red, golden"),
      ("6  Origin","Nepali, French, Tibetan"),
      ("7  Material","wooden, silk, plastic"),
      ("8  Purpose","dining, writing, sleeping")]
y=8.55
for lab, ex in rows:
    ax.add_patch(FancyBboxPatch((0.55,y-0.34),4.30,0.70,boxstyle="round,pad=0.06",
                                fc="#eef4fb",ec=ACCENT,lw=0.8))
    ax.text(0.80,y,lab,fontsize=7.0,color=ACCENT,ha='left',va='center')
    ax.text(5.20,y,ex,fontsize=7.0,color=INK,ha='left',va='center')
    y-=0.88
ax.text(0.95,1.62,"NOUN",fontsize=6.6,color=MUTED,ha='left')
ax.text(5.20,1.62,"table, bag, house",fontsize=7.0,color=INK,ha='left')
ax.annotate("",xy=(0.28,1.45),xytext=(0.28,9.35),
            arrowprops=dict(arrowstyle="-|>",color=MUTED,lw=1.0))
ax.plot([0.15,9.85],[1.05,1.05],color=GRID,lw=0.9)
ax.text(0.15,0.60,"✓  a lovely little old round brown Nepali wooden dining table",
        fontsize=7.0,color=GREEN,ha='left')
ax.text(0.15,0.10,"✗  a wooden Nepali brown old table",
        fontsize=7.0,color=RED,ha='left')
```

Two points of detail:

- **Commas.** Adjectives of the **same** kind are separated by commas or *and*:
  *a cold, wet, miserable morning*. Adjectives of **different** kinds take no
  comma: *a small black bag*.
- **Numbers come first.** *the **first three** chapters*, not *the three first
  chapters*.

::: caution Four order and comparison errors
✗ *the three first questions* → ✓ *the **first three** questions*
✗ *a red big ball* → ✓ *a **big red** ball* (size before colour)
✗ *an Italian old leather jacket* → ✓ *an **old Italian leather** jacket*
✗ *a most unique opportunity* → ✓ *a **unique** opportunity* (*unique, perfect,
round, empty, full, ideal* are absolute — they have no degrees)
:::

## 26.3 Participial adjectives: *-ing* and *-ed*

| *-ing* — what causes the feeling | *-ed* — what feels it |
|---|---|
| *The journey was **tiring**.* | *The passengers were **tired**.* |
| *The film was **boring**.* | *We were **bored**.* |
| *The news is **surprising**.* | *I am **surprised** at the news.* |
| *The result was **disappointing**.* | *Her parents were **disappointed**.* |
| *a **frightening** noise* | *a **frightened** child* |
| *an **interesting** lecture* | *an **interested** listener* |
| *a **confusing** map* | *a **confused** tourist* |
| *an **exciting** match* | *the **excited** crowd* |

✗ *I am very interesting in music.* → ✓ *I am very **interested** in music.*
✗ *The students were boring with the lesson.* → ✓ *The students were **bored**
with the lesson.*

## 26.4 Degrees of comparison

| Formation | Positive | Comparative | Superlative |
|---|---|---|---|
| one syllable: + *er / est* | tall | taller | tallest |
| one syllable ending consonant–vowel–consonant: double the consonant | big | bigger | biggest |
| ending in *-y*: *y* → *i* | happy | happier | happiest |
| two syllables or more: *more / most* | beautiful | more beautiful | most beautiful |
| irregular | good / well | better | best |
| irregular | bad / ill | worse | worst |
| irregular | little | less | least |
| irregular | much / many | more | most |
| irregular | far | farther / further | farthest / furthest |
| irregular | late | later / latter | latest / last |
| irregular | old | older / elder | oldest / eldest |

**Comparatives that take *to*, not *than*.** These come from Latin and already
contain the comparison: *superior, inferior, senior, junior, prior, anterior,
posterior, preferable*.
✓ *He is **senior to** me.* ✗ *He is senior than me.*
✓ *Health is **preferable to** wealth.* ✓ *I **prefer** tea **to** coffee.*

**Patterns worth memorising.**

- *He is taller than **any other** boy in the class.* (not *any boy* — that would
  include himself)
- *Kathmandu is **one of the busiest cities** in Nepal.* (superlative + plural noun)
- ***The more** you practise, **the better** you become.*
- *This bag is **twice as** heavy **as** that one.*
- *He is **not so / as** tall **as** his brother.*
- *a **most** interesting book* = a **very** interesting book (formal use of *most*)

::: caution Comparison traps
✗ *more better, most best, more easier* → never combine *more / most* with *-er /
-est*.
✗ *Nepal is larger than any country in South Asia.* → ✓ *…than any **other**
country…*
✗ *The climate of Pokhara is better than Kathmandu.* → ✓ *…better than **that of**
Kathmandu.* (compare like with like)
✗ *He is the taller of the three.* → ✓ *the **tallest** of the three* (comparative
for two, superlative for three or more)
✗ *sufficient enough, return back, repeat again* → say it once: *sufficient*,
*return*, *repeat*.
:::

## 26.5 Adverbs: kinds, forms and false friends

| Kind | Question answered | Examples |
|---|---|---|
| Manner | how? | *carefully, fast, well, hard* |
| Place | where? | *here, outside, upstairs, everywhere* |
| Time | when? | *now, yesterday, soon, already* |
| Frequency | how often? | *always, often, seldom, never, twice* |
| Degree | how much? | *very, quite, almost, too, enough* |
| Sentence (comment) | the speaker's view | *fortunately, certainly, obviously* |

Most adverbs of manner are formed with **-ly**, but three groups break the
pattern.

| Group | Examples |
|---|---|
| Same form as the adjective | *fast, hard, late, early, straight, high, deep, near, well (from good)* |
| **-ly** form with a different meaning | *hardly* = almost not · *lately* = recently · *nearly* = almost · *highly* = very much · *deeply* = profoundly · *shortly* = soon |
| Adjectives ending in *-ly* (never adverbs) | *friendly, lovely, lonely, silly, cowardly, likely, ugly* |

✓ *He works **hard**.* (with effort) ✓ *He **hardly** works.* (almost not at all)
✓ *She came **late**.* ✓ *I have not seen him **lately**.*
✓ *The bird flew **high**.* ✓ *She is **highly** respected.*
For *friendly* and its group, use a phrase: *He spoke **in a friendly way**.*

## 26.6 Where an adverb stands

```figure caption="Adverb position. Manner, place and time follow the object in that order; an adverb may never be wedged between the verb and its object."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.6))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
GREEN="#0B6A62"; RED="#9B2C2C"; AMBER="#B4690E"
cells=[(0.15,1.80,"She sang","VERB",ACCENT),
       (2.10,1.65,"the song","OBJECT",ACCENT),
       (3.90,2.00,"beautifully","MANNER",GREEN),
       (6.05,2.20,"on the stage","PLACE",GREEN),
       (8.40,1.45,"last night","TIME",GREEN)]
for x,w,txt,lab,col in cells:
    ax.add_patch(FancyBboxPatch((x,7.65),w,0.95,boxstyle="round,pad=0.07",
                                fc="#ffffff",ec=col,lw=1.0))
    ax.text(x+w/2,8.13,txt,ha="center",va="center",fontsize=6.9,color=INK)
    ax.text(x+w/2,9.00,lab,ha="center",va="center",fontsize=6.2,color=col)
ax.text(5.0,6.90,"M  →  P  →  T   is the normal order",
        ha='center',fontsize=7.0,color=MUTED)
ax.plot([0.15,9.85],[5.70,5.70],color=GRID,lw=0.9)
ax.text(0.15,5.15,"✗  She sang beautifully the song.",fontsize=7.2,color=RED,ha='left')
ax.text(0.15,4.55,"✗  She sang last night the song on the stage.",fontsize=7.2,color=RED,ha='left')
ax.plot([0.15,9.85],[4.05,4.05],color=GRID,lw=0.9)
ax.text(0.15,3.50,"ADVERBS OF FREQUENCY",fontsize=6.4,color=AMBER,ha='left')
freq=[("after the verb BE","He is always late."),
      ("before a main verb","He always comes late."),
      ("after the first auxiliary","He has always been late.")]
y=2.80
for lab,ex in freq:
    ax.text(0.15,y,lab,fontsize=6.8,color=MUTED,ha='left')
    ax.text(4.30,y,ex,fontsize=7.0,color=INK,ha='left')
    y-=0.80
ax.text(0.15,0.25,"always · usually · often · sometimes · seldom · rarely · never",
        fontsize=6.6,color=MUTED,ha='left')
```

Three further rules of position:

1. **Adverbs of degree** stand immediately before the word they modify: *She is
   **quite** sure*, *He drives **too** fast*. But *enough* follows the adjective
   or adverb: *old **enough***, *clearly **enough***.
2. ***Only*** attaches to whatever follows it, and moving it moves the meaning.
   *Only **I** solved two sums.* (nobody else did) · *I only **solved** two sums.*
   (I did nothing more with them) · *I solved **only two** sums.* (no more than
   two)
3. **Negative adverbials at the front cause inversion** — the auxiliary jumps in
   front of the subject.

| Front position | Sentence |
|---|---|
| Never | ***Never have I** seen such a crowd.* |
| Seldom / Rarely | ***Rarely does he** miss a class.* |
| Hardly … when | ***Hardly had she** spoken **when** the bell rang.* |
| No sooner … than | ***No sooner had we** sat down **than** it rained.* |
| Not only … but also | ***Not only did he** apologise, **but** he **also** paid for the damage.* |
| Little | ***Little did they** know the truth.* |
| Under no circumstances | ***Under no circumstances should you** open this door.* |

## 26.7 Errors Nepali speakers make most often

| ✗ Wrong | ✓ Correct | Why |
|---|---|---|
| *It was very much interesting.* | *It was **very** interesting.* | *very* + adjective; *very much* goes with verbs and comparatives |
| *I am much happy.* | *I am **very** happy.* | *much* modifies comparatives (*much happier*), not the positive |
| *He is more taller than me.* | *He is **taller** than me.* | no double comparative |
| *She is senior than me.* | *She is **senior to** me.* | Latin comparatives take *to* |
| *She sings very nice.* | *She sings very **nicely**.* | a verb needs an adverb |
| *The food tastes well.* | *The food tastes **good**.* | linking verb + adjective |
| *He drives very fastly.* | *He drives very **fast**.* | *fast* has no *-ly* form |
| *He works hardly.* | *He works **hard**.* | *hardly* means "almost not" |
| *This is more preferable.* | *This is **preferable**.* | *preferable* is already comparative |
| *He is elder than his sister.* | *He is **older** than his sister.* | *elder* is attributive only |
| *We have sufficient enough time.* | *We have **enough** time.* | one word is enough |
| *It is the most unique design.* | *It is a **unique** design.* | absolute adjectives take no degree |
| *He speaks English good.* | *He speaks English **well**.* | *good* is an adjective, *well* the adverb |
| *I am feeling very badly.* | *I am feeling very **bad**.* | *feel* here is a linking verb |
| *She read carefully the letter.* | *She read the letter **carefully**.* | nothing between verb and object |

::: example Worked item 26.1 — putting adjectives in order
**Problem.** Rearrange: *(a) a / Nepali / beautiful / woollen / old / shawl.*

**Solution — step by step.**

1. **Sort each word into its slot.** *beautiful* = opinion (1), *old* = age (3),
   *Nepali* = origin (6), *woollen* = material (7).
2. **Put the determiner first**: *a*.
3. **Arrange by slot number**: 1 → 3 → 6 → 7.
4. **End with the noun**: *shawl*.

**Answer.** ***a beautiful old Nepali woollen shawl***

No commas are needed, because every adjective belongs to a different class.
:::

::: example Worked item 26.2 — *-ed* or *-ing*?
**Problem.** Choose: *The three-hour speech was so (bored / boring) that even the
(interested / interesting) listeners looked (tired / tiring).*

**Solution — ask who feels and what causes.**

1. **The speech** causes the feeling, so it takes the *-ing* form: **boring**.
2. **The listeners** experience the feeling, so they take the *-ed* form:
   **interested**.
3. **The listeners** again feel it: **tired**. (*tiring* would mean the listeners
   made other people tired.)

**Answer.** *The three-hour speech was so **boring** that even the **interested**
listeners looked **tired**.*
:::

::: example Worked item 26.3 — transformation with inversion
**Problem.** Rewrite beginning with the word given: *(a) I have never tasted such
sweet mangoes. (Never …) (b) He had hardly reached home when the storm broke.
(Hardly …)*

**Solution — step by step.**

1. **(a)** Move *Never* to the front. Inversion now applies: the auxiliary *have*
   moves before the subject *I*, and the rest of the verb phrase follows
   unchanged. **Answer:** ***Never have I tasted such sweet mangoes.***
2. **(b)** Move *Hardly* to the front. The auxiliary is *had*, so it comes before
   *he*. The *when* clause stays where it is. **Answer:** ***Hardly had he reached
   home when the storm broke.***

Note that inversion uses the **auxiliary only**. If the sentence has no auxiliary,
supply *do / does / did*: *He rarely complains.* → *Rarely **does he** complain.*
:::

## Chapter summary

- Adjective order: **opinion – size – age – shape – colour – origin – material –
  purpose**, after the determiner and before the noun; numbers come before
  descriptive adjectives.
- *afraid, alive, asleep, alone, aware, ashamed* stand only after a verb;
  *main, only, mere, former, elder* only before a noun.
- *-ing* = the cause of a feeling, *-ed* = the person who has it.
- Comparatives: *-er/-est* for short words, *more/most* for long ones; never both.
  *superior, inferior, senior, junior, prior, preferable* take **to**.
- Use *than any other* in comparisons within a group; use *that of* when comparing
  qualities of two things.
- *hard / hardly*, *late / lately*, *near / nearly*, *high / highly* are different
  words, not variants.
- A linking verb takes an adjective; an action verb takes an adverb.
- Order of adverbs after the object: **manner – place – time**; never put an
  adverb between the verb and its object.
- Frequency adverbs go after *be*, before a main verb, and after the first
  auxiliary.
- Negative adverbials at the front (*Never, Rarely, Hardly, No sooner, Little, Not
  only, Under no circumstances*) force inversion of the auxiliary.

## Practice questions

**Choose or supply the correct form (1 mark each)**

1. The lecture was so ____ (bore) that half the class fell asleep. <span class="marks">[1]</span>
2. She speaks English more ____ (fluent) than her brother. <span class="marks">[1]</span>
3. Everest is ____ (high) mountain in the world. <span class="marks">[1]</span>
4. He is two years ____ (senior) me in service. <span class="marks">[1]</span>
5. The porter carried the load quite ____ (easy). <span class="marks">[1]</span>
6. This year's result is ____ (bad) than last year's. <span class="marks">[1]</span>
7. I have not met him ____ (late). <span class="marks">[1]</span>
8. The children were ____ (excite) about the picnic. <span class="marks">[1]</span>
9. She is one of the ____ (talented) singers of her generation. <span class="marks">[1]</span>
10. The ____ (much) you read, the more you learn. <span class="marks">[1]</span>

::: note Answers
**1.** boring — the lecture causes the feeling.
**2.** fluently — an adverb modifies *speaks*; *fluently* is three syllables, so *more fluently*.
**3.** the highest — superlative with *the*.
**4.** senior to — the Latin comparative takes *to*.
**5.** easily — an adverb of manner after the object *the load*.
**6.** worse — irregular comparative of *bad*.
**7.** lately — "recently", used with the present perfect.
**8.** excited — the children have the feeling.
**9.** most talented — *one of the* + superlative + plural noun.
**10.** more — the fixed pattern *the more … the more …*.
:::

**Correct the errors (1 mark each)**

11. He is more stronger than his elder brother. <span class="marks">[1]</span>
12. She read carefully the notice before signing it. <span class="marks">[1]</span>
13. The mangoes of Nepal are sweeter than India. <span class="marks">[1]</span>
14. I am very much interesting in classical music. <span class="marks">[1]</span>
15. He drives very fastly on the highway. <span class="marks">[1]</span>
16. This soup tastes very well. <span class="marks">[1]</span>
17. She bought a Nepali beautiful woollen cap. <span class="marks">[1]</span>
18. Kathmandu is bigger than any city in Nepal. <span class="marks">[1]</span>
19. We have sufficient enough chairs for the guests. <span class="marks">[1]</span>
20. He works hardly from morning till night. <span class="marks">[1]</span>

::: note Answers
**11.** He is **stronger** than his elder brother. — never *more* with *-er*.
**12.** She read **the notice carefully** before signing it. — no adverb between verb and object.
**13.** The mangoes of Nepal are sweeter than **those of** India. — compare mangoes with mangoes.
**14.** I am very much **interested** in classical music. — the person feels it. (*very interested* is equally correct.)
**15.** He drives very **fast** on the highway. — *fast* is both adjective and adverb.
**16.** This soup tastes very **good**. — *taste* is a linking verb here.
**17.** She bought a **beautiful Nepali woollen** cap. — opinion, then origin, then material.
**18.** Kathmandu is bigger than **any other** city in Nepal. — Kathmandu cannot be bigger than itself.
**19.** We have **enough** chairs for the guests. — *sufficient enough* is a double expression.
**20.** He works **hard** from morning till night. — *hardly* would mean "almost not".
:::

**Rewrite as instructed (1 mark each)**

21. *I have never heard such a foolish excuse.* — Begin: *Never …* <span class="marks">[1]</span>
22. *He had no sooner entered the hall than the lights failed.* — Begin: *No sooner …* <span class="marks">[1]</span>
23. *He rarely visits his village.* — Begin: *Rarely …* <span class="marks">[1]</span>
24. *No other student in the class is as sincere as Sita.* — Rewrite using the superlative. <span class="marks">[1]</span>
25. *Ram is not as tall as Hari.* — Rewrite using *taller*. <span class="marks">[1]</span>

::: note Answers
**21.** **Never have I heard such a foolish excuse.** — the auxiliary *have* moves before *I*.
**22.** **No sooner had he entered the hall than the lights failed.** — inversion of *had*.
**23.** **Rarely does he visit his village.** — there is no auxiliary, so *does* is supplied and the main verb returns to its base form.
**24.** **Sita is the most sincere student in the class.** — the negative comparison becomes a superlative.
**25.** **Hari is taller than Ram.** — reverse the subjects and use the comparative.
:::
