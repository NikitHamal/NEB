---
subject: Compulsory English
grade: 12
unit: 35
title: 'Vocabulary, Sounds, Spelling and Idioms'
hours: 6
area: Writing and Skills
---

Question 8 carries only five marks, and it is the cheapest five marks on the paper.
Every item in it — a prefix, a phrasal verb, a homophone, an idiom, a stressed syllable
— is something that can be learnt in advance and cannot be reasoned out on the day. A
candidate who has spent twenty evenings on this unit answers the whole question in four
minutes and walks into Question 1 with time in hand.

::: key Learn words in families, not in lists
*Beautiful* memorised alone is one word. *Beauty, beautify, beautiful, beautifully,
beautician* learnt together is five words, four suffixes and a spelling rule — and it
costs no more effort.
:::

## 35.1 What Question 8 asks

Five one-mark items, drawn from this pool:

| Item | Looks like |
|---|---|
| Word formation | *Make a noun from **decide**.* |
| Prefix or suffix | *Add a prefix to **legal** to give the opposite.* |
| Phrasal verb | *Replace **tolerate** with a phrasal verb using **put**.* |
| Collocation | *Choose: he ___ a decision (made / did / took).* |
| Homophone / confusable | *Choose the right word: The **affect / effect** was immediate.* |
| Spelling | *Correct the spelling: **recieve**, **occured**.* |
| Stress | *Mark the stressed syllable: **increase** (verb).* |
| Sound | *Which word has a different vowel sound: **bird, word, board**?* |
| Idiom or proverb | *What does **burn the midnight oil** mean?* |

## 35.2 How English words are built

Almost every long English word is a root with something screwed on at each end. Take
the root apart and the meaning falls out.

::: example Model answer 35.2 — a word-formation item
**Question.** Complete the sentence with the correct form of the word in brackets:
*The committee's (decide) was announced on Friday, and nobody was (satisfy) with it.*
<span class="marks">[1]</span>

**Model answer.** *decision* and *satisfied*.

**Why it scores.** The first gap follows *committee's* and precedes a verb, so it must
be a **noun**: *decide* takes *-ion*, and *decide + ion* gives *decision*, not
~~decidation~~. The second gap follows *was* and describes people, so it must be a past
participle used as an **adjective**: *satisfied*, not *satisfying* — a thing is
satisfying, a person is satisfied. Deciding the part of speech before choosing the
suffix is the whole method.
:::

```figure caption="One Latin root, six English words. Knowing that port means carry turns six separate spellings into one idea with six wrappers."
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
fig, ax = plt.subplots(figsize=(5.0, 3.4))
ax.axis("off")
ax.text(0.85, 8.05, "Latin root  PORT  —  'to carry'",
        fontsize=7.0, color=ACCENT, ha="left")
rows = [(["im", "port"], "carry in — bring goods into a country"),
        (["ex", "port"], "carry out — send goods abroad"),
        (["trans", "port"], "carry across — move from place to place"),
        (["sup", "port"], "carry from under — hold up, help"),
        (["port", "able"], "able to be carried — light enough to move"),
        (["re", "port", "er"], "one who carries back — a news writer")]
ys = [7.1, 6.0, 4.9, 3.8, 2.7, 1.6]
for (parts, gloss), y in zip(rows, ys):
    x = 0.85
    for pt in parts:
        w = 0.069 * len(pt) + 0.45
        is_root = (pt == "port")
        ax.add_patch(mpatches.FancyBboxPatch((x, y - 0.27), w, 0.56,
                     boxstyle="round,pad=0.0,rounding_size=0.08",
                     linewidth=1.0, edgecolor=ACCENT if is_root else GRID,
                     facecolor=ACCENT if is_root else "#ffffff"))
        ax.text(x + w / 2, y, pt, ha="center", va="center", fontsize=6.6,
                color="white" if is_root else INK)
        x += w + 0.08
    ax.text(3.35, y, "→", ha="center", va="center", fontsize=6.6, color=MUTED)
    ax.text(3.65, y, gloss, ha="left", va="center", fontsize=6.3, color=INK)
ax.set_xlim(0.5, 8.5)
ax.set_ylim(1.0, 8.4)
```

**Prefixes change the meaning; suffixes change the part of speech.**

| Prefix | Sense | Examples |
|---|---|---|
| un-, in-, im-, il-, ir-, dis-, non- | not | unfair, incomplete, impossible, illegal, irregular, disagree, non-stop |
| mis- | wrongly | misunderstand, misspell, misjudge |
| re- | again | rebuild, reconsider, reunite |
| over- / under- | too much / too little | overcharge, overslept / underpaid, underestimate |
| pre- / post- | before / after | prepaid, precaution / postpone, post-war |
| co- / inter- / trans- | together / between / across | co-worker, international, transplant |
| anti- / auto- / multi- | against / self / many | antiseptic, autobiography, multilingual |

::: tip Which negative prefix?
**im-** before *m* and *p* (immature, impatient); **il-** before *l* (illegal,
illiterate); **ir-** before *r* (irregular, irresponsible); **in-** before most others
(inactive, invisible); **un-** with most plain English words (unhappy, unknown). When
in doubt, *un-* is the safest guess.
:::

| Suffix | Makes a | Examples |
|---|---|---|
| -ment, -ion, -ity, -ness, -ance, -ship | noun | judgement, decision, ability, kindness, performance, friendship |
| -er, -or, -ist, -ian | person noun | teacher, actor, novelist, musician |
| -ise / -ize, -fy, -en | verb | modernise, simplify, strengthen |
| -ful, -less, -ous, -al, -ive, -able | adjective | useful, careless, famous, national, attractive, readable |
| -ly | adverb | quickly, hardly, carefully |

## 35.3 Collocations

A collocation is a pair of words that English happens to put together. There is no rule;
there is only usage, and an examiner can hear the wrong one at once.

| Verb | Goes with |
|---|---|
| **make** | a decision, a mistake, progress, an effort, arrangements, friends, noise |
| **do** | homework, the dishes, a favour, business, research, one's best |
| **take** | a photograph, an examination, part, care, a risk, medicine, a seat |
| **have** | a bath, breakfast, a look, a word with, an argument, fun |
| **give** | a speech, permission, advice, a hand, an example |
| **pay** | attention, a visit, a compliment, a fine, respect |
| **heavy** | rain, traffic, smoker, loss |
| **strong** | tea, coffee, wind, opinion, accent |

::: caution Six collocations Nepali candidates reverse
*~~do a mistake~~* → **make** a mistake · *~~give an exam~~* → **take** an exam ·
*~~take a decision~~* is British but *~~do a decision~~* is not English ·
*~~say a lie~~* → **tell** a lie · *~~open the light~~* → **turn on** the light ·
*~~strong rain~~* → **heavy** rain.
:::

## 35.4 Phrasal verbs

| Phrasal verb | Meaning | Example |
|---|---|---|
| put up with | tolerate | *We put up with the noise for a year.* |
| put off | postpone | *The meeting was put off till Sunday.* |
| call off | cancel | *The match was called off because of rain.* |
| look into | investigate | *The ward office promised to look into it.* |
| look after | take care of | *She looks after her grandmother.* |
| bring up | raise (a child, a topic) | *He was brought up in Ilam.* |
| break down | stop working; lose control | *The bus broke down at Mugling.* |
| turn down | reject | *They turned down my application.* |
| carry out | perform | *The team carried out a survey.* |
| come across | meet or find by chance | *I came across an old photograph.* |
| get over | recover from | *It took him a month to get over the fever.* |
| give in | surrender | *He argued for an hour and then gave in.* |
| run out of | have no more left | *We ran out of petrol at Dumre.* |
| take after | resemble (a relative) | *She takes after her mother.* |
| set up | establish | *They set up a cooperative in 2078.* |

::: tip Separable or not?
Most phrasal verbs with an object may be split — *turn the offer down*, *turn down the
offer* — but if the object is a **pronoun**, the split is compulsory: *turn it down*,
never ~~turn down it~~. Verbs with two particles (*put up with*, *run out of*) are
never split.
:::

## 35.5 Words that are easy to confuse

| Pair | The difference |
|---|---|
| **affect / effect** | *affect* is the verb, *effect* the noun: *the rain affected the crop; the effect was severe* |
| **advice / advise** | noun with *c*, verb with *s* |
| **practice / practise** | same rule: *daily practice* (n.), *to practise* (v.) |
| **principal / principle** | the principal is a person or the chief thing; a principle is a rule |
| **stationary / stationery** | *stationary* = not moving; *stationery* = paper and pens |
| **complement / compliment** | complete it / praise it |
| **lose / loose** | *lose* a match; a *loose* knot |
| **its / it's** | possessive / *it is* |
| **their / there / they're** | belonging to them / in that place / they are |
| **accept / except** | receive / leave out |
| **weather / whether** | rain and sun / if |
| **desert / dessert** | sand; to abandon / the sweet course |
| **lie / lay** | *lie* down (no object); *lay* the book down (object) |
| **beside / besides** | next to / in addition to |
| **later / latter** | afterwards / the second of two |

**Homophones** sound identical and are spelt differently: *to / too / two*, *there /
their*, *hear / here*, *write / right / rite*, *piece / peace*, *flour / flower*,
*son / sun*, *sea / see*, *knew / new*, *whole / hole*, *bear / bare*, *wait / weight*.

## 35.6 Spelling rules that actually pay

1. **i before e except after c**, when the sound is *ee*: bel**ie**ve, ach**ie**ve,
   f**ie**ld — but rec**ei**ve, dec**ei**ve, c**ei**ling. *Exceptions:* seize, weird,
   either, neither, protein.
2. **Doubling.** In a word of one syllable ending consonant–vowel–consonant, double the
   final letter before *-ing*, *-ed*, *-er*: stop → stopping, big → bigger. In a longer
   word, double only if the **last** syllable is stressed: beGIN → beginning, preFER →
   preferred, but ENter → entering, BENefit → benefited.
3. **Silent e.** Drop it before a vowel suffix, keep it before a consonant suffix:
   hope → hoping but hopeful; use → usable but useful. *Keep* the *e* after *c* or *g*
   to protect the soft sound: notice → noticeable, courage → courageous.
4. **y to i.** After a consonant, *y* becomes *i*: happy → happiness, carry → carried,
   beauty → beautiful. After a vowel it does not: play → played, enjoy → enjoyed.
5. **-ful** as a suffix has one *l*: careful, useful, beautiful — though *full* as a
   word has two.
6. **all-, well-, till-** lose a letter in compounds: always, almost, welcome, until.

::: caution The eighteen most misspelt words in NEB answer books
*accommodation · necessary · occurred · separate · definitely · received ·
beginning · committee · embarrass · immediately · government · privilege ·
maintenance · recommend · occasion · questionnaire · rhythm · conscience*
:::

## 35.7 Sounds: what the symbols mean

English spelling is unreliable, so dictionaries describe sounds with the International
Phonetic Alphabet. You are not expected to transcribe; you are expected to recognise
the common symbols and to hear the contrasts that Nepali does not make.

```photo id="eng12/ipa-vowels" caption="The IPA vowel chart. The four corners are the extremes of tongue position: close means the tongue is high in the mouth, open means it is low; front and back say where along the mouth the hump of the tongue sits. English uses only about a dozen of these positions." width="88"
crop 0.02 0.02 0.98 0.98
```

| Symbol | As in | Nepali speakers often say instead |
|---|---|---|
| /θ/ | **th**ink, ba**th** | थ — an aspirated *t*, giving *tink* |
| /ð/ | **th**is, mo**th**er | द — a hard *d*, giving *dis* |
| /v/ | **v**ery, ha**v**e | व as *w*, giving *wery* |
| /z/ | **z**oo, ro**s**e | ज, giving *joo*, *roj* |
| /f/ | **f**an, o**ff**ice | फ, giving *phan* |
| /æ/ | b**a**d, c**a**t | /e/, so that *bad* and *bed* sound alike |
| /ɜː/ | b**ir**d, w**or**d | a full *r*, giving *burd* |
| /ə/ | **a**bout, teach**er** | a full vowel — the schwa disappears |

Two other habits worth naming. English allows consonant clusters that Nepali does not,
so a vowel creeps in: *film* becomes *fil-um*, *school* becomes *is-cool*. And English
word endings matter: the *-ed* of *walked* is /t/, of *played* is /d/, and of *wanted*
is /ɪd/ — three different sounds from one spelling.

## 35.8 Stress, and the noun–verb shift

Every English word of more than one syllable has one syllable said louder, longer and
higher. Put it in the wrong place and a listener may not recognise the word at all.

```figure caption="The same spelling, two stress patterns. When these words are nouns the stress falls on the first syllable; when they are verbs it moves to the second."
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
fig, ax = plt.subplots(figsize=(5.0, 2.8))
ax.axis("off")
words = [("RE", "cord"), ("PRE", "sent"), ("EX", "port"), ("CON", "duct")]
labels = ["record", "present", "export", "conduct"]
centres = [2.8, 5.0, 7.2, 9.4]
def chip(x, y, t, on):
    w = 0.90
    ax.add_patch(mpatches.FancyBboxPatch((x, y), w, 0.60,
                 boxstyle="round,pad=0.0,rounding_size=0.08",
                 linewidth=1.0, edgecolor=ACCENT if on else GRID,
                 facecolor=ACCENT if on else "#ffffff"))
    ax.text(x + w / 2, y + 0.30, t, ha="center", va="center", fontsize=6.0,
            color="white" if on else MUTED)
ax.text(0.55, 5.20, "noun", fontsize=6.6, color=INK, ha="left", va="center")
ax.text(0.55, 2.90, "verb", fontsize=6.6, color=INK, ha="left", va="center")
for (a, b), lab, cx in zip(words, labels, centres):
    chip(cx - 0.95, 4.90, a, True)
    chip(cx + 0.05, 4.90, b, False)
    chip(cx - 0.95, 2.60, a, False)
    chip(cx + 0.05, 2.60, b, True)
    ax.annotate("", xy=(cx + 0.50, 3.34), xytext=(cx - 0.50, 4.76),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.8,
                                mutation_scale=7))
    ax.text(cx, 1.80, lab, fontsize=6.4, color=INK, ha="center", va="center")
ax.set_xlim(0.3, 10.6)
ax.set_ylim(1.3, 5.9)
```

::: example Model answer 35.3 — a stress item
**Question.** Mark the stressed syllable in *present* in each of these sentences.
*(a) They gave him a present. (b) The head will present the prizes.*
<span class="marks">[1]</span>

**Model answer.** (a) **PRE**sent (b) pre**SENT**

**Why it scores.** In (a) the word follows *a* and is the object of *gave*, so it is a
noun, and a two-syllable noun of this pair takes its stress on the first syllable. In
(b) it follows the auxiliary *will*, so it is a verb, and the stress moves to the
second. The test is never the spelling; it is the job the word is doing in that
sentence.
:::

Other pairs that behave the same way: *increase, object, subject, permit, rebel, contrast,
suspect, insult, progress, protest, desert, produce, project*.

**Three suffixes that pull the stress** to the syllable immediately before them:

| Suffix | Pattern | Examples |
|---|---|---|
| -ion, -ial, -ious | stress the syllable before | eduCAtion, inDUStrial, inDUStrious |
| -ity, -ical, -ic | stress the syllable before | aBIlity, eCOnomical, sciEntific |
| -graphy, -logy, -ometer | stress the syllable before | phoTOgraphy, bioLOgy, thermOmeter |

Suffixes that do **not** move the stress: *-ness, -ment, -ly, -ful, -less, -er, -ing,
-ed*. So *HAPpy → HAPpiness*, *GOVern → GOVernment*.

## 35.9 Forty-four idioms and proverbs

::: example Model answer 35.1 — how an idiom question is answered
**Question.** Explain the meaning of *a blessing in disguise* and use it in a sentence.
<span class="marks">[1]</span>

**Model answer.** It means something that seems unfortunate at first but turns out to
be lucky. *Missing the early bus was a blessing in disguise, because it skidded off the
road above Mugling.*

**Why it scores.** The meaning is given in a full clause, not as a synonym; the example
sentence makes the meaning visible without repeating the explanation; and the idiom is
used in its fixed form, with no word changed.
:::

**Everyday idioms**

| Idiom | Meaning | Example |
|---|---|---|
| a blessing in disguise | a misfortune that turns out well | *Losing that job was a blessing in disguise.* |
| break the ice | start a conversation in an awkward moment | *He broke the ice by asking about our school.* |
| burn the midnight oil | study or work far into the night | *She burnt the midnight oil all Chaitra.* |
| call it a day | stop work for the time being | *After nine hours we called it a day.* |
| cut corners | do a job cheaply and badly | *The contractor cut corners and the wall fell.* |
| once in a blue moon | very rarely indeed | *My uncle visits once in a blue moon.* |
| let the cat out of the bag | give away a secret by accident | *Sujata let the cat out of the bag about the party.* |
| the ball is in your court | it is now your turn to act | *I have replied; the ball is in their court.* |
| bite off more than you can chew | take on more than you can manage | *He took five tuitions and bit off more than he could chew.* |
| under the weather | slightly unwell | *She stayed at home, feeling under the weather.* |
| hit the nail on the head | say exactly the right thing | *You hit the nail on the head about the timetable.* |
| sit on the fence | refuse to take either side | *The committee sat on the fence for three meetings.* |

**Idioms of trouble and effort**

| Idiom | Meaning | Example |
|---|---|---|
| a drop in the ocean | far too little for what is needed | *Rs 5,000 is a drop in the ocean when the roof costs three lakh.* |
| face the music | accept the unpleasant consequences | *He copied, and had to face the music.* |
| beat about the bush | avoid coming to the point | *Stop beating about the bush and name the fee.* |
| in the same boat | in the same difficulty as others | *We are all in the same boat this week.* |
| get cold feet | lose one's nerve at the last moment | *He got cold feet the night before the interview.* |
| cost an arm and a leg | be extremely expensive | *That laptop cost an arm and a leg.* |
| go the extra mile | do more than is required | *The nurse went the extra mile and carried the medicine up.* |
| the last straw | the small trouble that makes it unbearable | *The cancelled bus was the last straw.* |
| a wild goose chase | a hopeless and wasteful search | *Finding the office without an address was a wild goose chase.* |
| throw in the towel | give up | *He threw in the towel after the third attempt.* |
| add fuel to the fire | make a bad situation worse | *His apology only added fuel to the fire.* |
| on thin ice | in a risky position | *After two warnings he is on thin ice.* |
| make ends meet | earn just enough to live on | *With two jobs she barely makes ends meet.* |
| at the eleventh hour | at the very last moment | *The funds arrived at the eleventh hour.* |

**Idioms of people and judgement**

| Idiom | Meaning | Example |
|---|---|---|
| pull someone's leg | tease playfully | *Do not worry, he was pulling your leg.* |
| turn a blind eye | pretend not to notice | *The invigilator turned a blind eye.* |
| a storm in a teacup | a great fuss about a trifle | *The row over the badge was a storm in a teacup.* |
| take with a pinch of salt | not believe entirely | *Take his account of the marks with a pinch of salt.* |
| read between the lines | grasp what is implied but unsaid | *Read between the lines: the letter is a refusal.* |
| see eye to eye | agree completely | *The brothers rarely see eye to eye about the land.* |
| let sleeping dogs lie | leave an old quarrel alone | *Do not raise the boundary case; let sleeping dogs lie.* |
| bury the hatchet | end a quarrel and be friends | *After ten years the families buried the hatchet.* |
| steal someone's thunder | take the credit meant for another | *She announced it first and stole his thunder.* |
| keep at arm's length | avoid becoming close to | *She keeps campus politics at arm's length.* |
| out of the blue | completely unexpectedly | *A letter came out of the blue from my old teacher.* |
| put the cart before the horse | do things in the wrong order | *Buying furniture before renting the shop is putting the cart before the horse.* |
| jump on the bandwagon | join a thing because it is popular | *Every shop jumped on the bandwagon and sold momos.* |
| a piece of cake | very easy | *The vocabulary section was a piece of cake.* |
| play it by ear | decide as you go along | *We had no plan for Pokhara; we played it by ear.* |
| keep one's fingers crossed | hope for good luck | *I am keeping my fingers crossed for the result.* |

**Proverbs**

| Proverb | What it teaches |
|---|---|
| A stitch in time saves nine. | Repair a small fault now and you avoid a large one later. |
| Don't count your chickens before they hatch. | Do not rely on a result before you have it. |
| Too many cooks spoil the broth. | Too many people managing one job ruin it. |
| Where there is a will there is a way. | Determination finds a method. |
| Rome was not built in a day. | Anything worth building takes time. |
| Empty vessels make the most noise. | Those who know least talk loudest. |
| A rolling stone gathers no moss. | Constant moving prevents you from settling or saving. |
| Necessity is the mother of invention. | Hardship forces people to think of new ways. |
| Look before you leap. | Consider the consequences before acting. |
| Birds of a feather flock together. | People of similar kinds keep company. |
| Make hay while the sun shines. | Use an opportunity while it lasts. |
| Actions speak louder than words. | What people do proves more than what they say. |

::: caution An idiom is a fixed form
You may not change its words. *~~Burn the midnight lamp~~*, *~~a piece of pie~~*,
*~~hit the nail on its head~~*, *~~once in a red moon~~* — each is worth nothing.
Learn the exact wording or leave the idiom out.
:::

## 35.10 Marking checklist for Question 8

| | Check | Mark at risk |
|---|---|---|
| 1 | Is my answer the **part of speech** the question asked for? | Word formation |
| 2 | Have I spelt the derived word correctly after the suffix rule (*happy → happiness*)? | Spelling |
| 3 | Negative prefix: *im-* before m/p, *il-* before l, *ir-* before r? | Prefix |
| 4 | Phrasal verb with a pronoun object — have I split it (*turn it down*)? | Phrasal verb |
| 5 | Collocation: *make* a mistake, *take* an exam, *tell* a lie, *heavy* rain? | Collocation |
| 6 | Confusables: *advice/advise*, *affect/effect*, *its/it's*, *principal/principle*? | Vocabulary |
| 7 | Stress: is the word a noun or a verb in this sentence? | Stress |
| 8 | Have I written the idiom in its exact fixed form? | Idiom |
| 9 | Does my example sentence show the meaning rather than repeat it? | Idiom |
| 10 | Have I answered all five items? None of them is worth skipping. | All |

## Chapter summary

- Question 8 is 5 one-mark items: word formation, prefix or suffix, phrasal verb,
  collocation, confusable, spelling, stress, sound, idiom.
- Prefixes change meaning; suffixes change part of speech. Learn one root and its whole
  family together.
- *im-* before *m* and *p*, *il-* before *l*, *ir-* before *r*, *in-* otherwise, *un-*
  with plain English words.
- Collocations have no rules, only usage: *make* a mistake, *do* homework, *take* an
  exam, *tell* a lie, *heavy* rain, *strong* tea.
- A phrasal verb with a pronoun object must be split: *turn it down*. Three-word phrasal
  verbs are never split.
- Spelling: *i* before *e* except after *c*; double the final consonant only when the
  last syllable is stressed; drop silent *e* before a vowel suffix; *y* → *i* after a
  consonant.
- Nepali speakers substitute for /θ, ð, v, z, f, æ, ɜː/ and lose the schwa; the *-ed*
  ending has three sounds — /t/, /d/, /ɪd/.
- Two-syllable noun–verb pairs shift stress: **RE**cord (n.) but re**CORD** (v.).
  *-ion, -ity, -ic, -graphy, -logy* pull the stress to the syllable before them.
- An idiom is a fixed form. Change one word and it is no longer an idiom.

## Practice questions

**Vocabulary and word formation (1 mark each)**

1. Make a noun from **decide**. <span class="marks">[1]</span>
2. Make an adjective from **courage**. <span class="marks">[1]</span>
3. Add a prefix to **responsible** to give the opposite. <span class="marks">[1]</span>
4. Add a prefix to **mature** to give the opposite. <span class="marks">[1]</span>
5. Choose: *She ___ a serious mistake.* (did / made / took) <span class="marks">[1]</span>
6. Choose: *May I ___ your advice?* (have / do / make) <span class="marks">[1]</span>
7. Replace **tolerate** with a phrasal verb using **put**. <span class="marks">[1]</span>
8. Replace **investigate** with a phrasal verb using **look**. <span class="marks">[1]</span>

**Spelling, sounds and stress (1 mark each)**

9. Correct: *recieve, occured, seperate* <span class="marks">[1]</span>
10. Add *-ing*: **begin**, **enter**, **hope** <span class="marks">[1]</span>
11. Add *-ness*: **happy**, **lonely** <span class="marks">[1]</span>
12. Which word has a different vowel sound: **bird, word, board**?
    <span class="marks">[1]</span>
13. Mark the stressed syllable: **increase** used as a verb. <span class="marks">[1]</span>
14. Mark the stressed syllable: **photograph**, **photographer**, **photographic**.
    <span class="marks">[1]</span>
15. How is the *-ed* pronounced in **wanted**, **walked**, **played**?
    <span class="marks">[1]</span>

**Confusables and idioms (1 mark each)**

16. Choose: *The medicine had no ___.* (affect / effect) <span class="marks">[1]</span>
17. Choose: *Our ___ addressed the assembly.* (principal / principle)
    <span class="marks">[1]</span>
18. Give the meaning of **burn the midnight oil** and use it in a sentence.
    <span class="marks">[1]</span>
19. Give the meaning of **a drop in the ocean** and use it in a sentence.
    <span class="marks">[1]</span>
20. Complete the proverb and explain it: *Too many cooks ___.*
    <span class="marks">[1]</span>

::: note Answers
**1.** decision. **2.** courageous — the *e* is kept to protect the soft *g*.
**3.** irresponsible — *ir-* before *r*. **4.** immature — *im-* before *m*.
**5.** made — *make a mistake*. **6.** have — *have a word*, *have your advice*; the usual collocation is *take advice* or *have your advice*.
**7.** put up with. **8.** look into.
**9.** receive, occurred, separate.
**10.** beginning (last syllable stressed, so doubled), entering (first syllable stressed, so not doubled), hoping (silent *e* dropped).
**11.** happiness (*y* → *i* after a consonant), loneliness.
**12.** **board** — *bird* and *word* are both /ɜː/; *board* is /ɔː/.
**13.** in**CREASE** — the verb takes second-syllable stress.
**14.** PHOtograph · phoTOgrapher · photoGRAPHic — the stress moves each time because the suffix changes.
**15.** wanted /ɪd/, walked /t/, played /d/.
**16.** effect — it is a noun here. **17.** principal — a person.
**18.** To work or study late into the night. *He burnt the midnight oil for a month before the board examination.*
**19.** An amount far too small for what is needed. *A hundred sacks of rice was a drop in the ocean after the flood.*
**20.** *…spoil the broth.* When too many people manage one piece of work, they ruin it.
:::
