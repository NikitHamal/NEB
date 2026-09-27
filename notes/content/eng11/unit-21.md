---
subject: Compulsory English
grade: 11
unit: 21
title: Word Classes, Contracted Forms and Dictionary Use
hours: 4
area: Grammar
---

Every word in English belongs to a **word class** (also called a part of speech),
and the class decides where the word may stand in a sentence and what shape it may
take. Question 7 of the NEB paper is ten one-mark grammar items, and several of
them turn on class: you are asked to put the right *form* of a word in a blank
(`The ____ of the bridge took two years. (construct)`), to identify what a word is
doing, or to correct a sentence in which a noun has been used where an adjective
was needed. This chapter also covers contracted forms — tested in rewriting and in
dialogue-completion items — and how to pull grammar information out of a
dictionary, which is what the CDC syllabus means by "dictionary use".

::: key What Q7 actually rewards
Q7 gives you ten separate one-mark sentences. There are no part-marks. A sentence
is either fully right or fully wrong, so the tiny things — a final **-s**, an
apostrophe, an article — are the whole mark. Read every item twice before writing.
:::

## 21.1 The eight word classes

English words sort into eight classes. Learn the class, the question it answers,
and one test that identifies it.

| Class | What it does | Test | Examples |
|---|---|---|---|
| Noun | names a person, place, thing, idea | can follow *the* / *a* | Pokhara, student, honesty, rice |
| Pronoun | stands in place of a noun | can replace a whole noun phrase | he, them, ours, which, myself |
| Verb | states an action or a state | can change tense (*walk / walked*) | run, is, seem, arrive, believe |
| Adjective | describes a noun | fits "a very ____ thing" | cold, Nepali, useful, tall |
| Adverb | describes a verb, adjective or another adverb | answers how / when / where / how often | slowly, yesterday, here, very |
| Preposition | shows relation of a noun to the rest | is followed by a noun phrase | in, on, at, between, despite |
| Conjunction | joins words, phrases or clauses | sits between the two joined parts | and, but, because, although |
| Determiner | limits or points to a noun | comes before the noun, before adjectives | the, this, my, some, three |

Interjections (*Oh! Alas! Hurray!*) are usually counted as a ninth, minor class.

```figure caption="The same sentence labelled by word class. Notice that a determiner always comes first in the noun phrase, and the adjective sits between the determiner and the noun."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.6))
words = ["The", "young", "farmer", "quickly", "sold", "his", "maize", "in", "Birgunj"]
tags  = ["det", "adj", "noun", "adv", "verb", "det", "noun", "prep", "noun"]
cols  = [MUTED, SERIES[2], ACCENT, SERIES[1], SERIES[0], MUTED, ACCENT, SERIES[3], ACCENT]
ax.set_xlim(0, 1); ax.set_ylim(0.18, 0.98)
fig.canvas.draw()
rend = fig.canvas.get_renderer()
inv = ax.transAxes.inverted()
def axwidth(s, fs):
    t = ax.text(0, -9, s, fontsize=fs)
    bb = t.get_window_extent(renderer=rend); t.remove()
    return inv.transform((bb.width, 0))[0] - inv.transform((0, 0))[0]
# shrink the type until the whole labelled sentence fits the axes with clear gaps
for FS in (10.0, 9.5, 9.0, 8.5, 8.0, 7.5):
    ws = [max(axwidth(a, FS), axwidth(b, FS - 1.4)) for a, b in zip(words, tags)]
    gap = axwidth("nn", FS)
    tot = sum(ws) + gap * (len(ws) - 1)
    if tot <= 0.96:
        break
edges, x = [], (1.0 - tot) / 2
for ww in ws:
    edges.append((x, x + ww)); x += ww + gap
for (a, b), word, tag, c in zip(edges, words, tags, cols):
    cx = (a + b) / 2
    ax.text(cx, 0.60, word, ha='center', va='center', fontsize=FS, color=INK)
    ax.text(cx, 0.30, tag, ha='center', va='center', fontsize=FS - 1.4, color=c)
    ax.plot([cx, cx], [0.42, 0.51], color=c, lw=1.0)
def brace(i, j, label):
    x0 = edges[i][0] - 0.012
    x1 = edges[j][1] + 0.012
    ax.plot([x0, x1], [0.78, 0.78], color=MUTED, lw=1.0)
    ax.plot([x0, x0], [0.74, 0.78], color=MUTED, lw=1.0)
    ax.plot([x1, x1], [0.74, 0.78], color=MUTED, lw=1.0)
    ax.text((x0 + x1) / 2, 0.88, label, ha='center', va='center',
            fontsize=8.4, color=MUTED)
brace(0, 2, 'noun phrase')
brace(7, 8, 'prepositional phrase')
ax.axis('off')
```

## 21.2 Nouns: countable, uncountable and the forms Nepali learners mix up

A **countable noun** can be counted, so it has a plural and takes *a/an* in the
singular: *a book, two books; a rupee, five hundred rupees*. An **uncountable
noun** cannot be counted directly, has no plural, and never takes *a/an*:
*water, rice, money, furniture, luggage, information, advice, news, work,
equipment, homework, traffic, weather, progress, machinery, scenery*.

- **Right:** She gave me some useful *information* about the scholarship.
- **Right:** The teacher gave us three *pieces of advice*.
- **Right:** There is heavy *traffic* on the Ring Road every morning.

To count an uncountable noun, use a **partitive**: *a piece of information, a bit
of advice, an item of news, a glass of water, a kilo of rice, a sack of cement*.

::: caution "Informations", "advices", "furnitures"
These are the single commonest noun errors in Nepali student writing, because the
Nepali equivalents are countable. English does not pluralise them.
Write **much information / a lot of information**, not ~~many informations~~;
**a piece of advice**, not ~~an advice~~; **furniture**, not ~~furnitures~~.
The same goes for *luggage, equipment, machinery, scenery, poetry, staff* (as a
mass), *bread, hair* (on the head) and *work*.
:::

Some nouns are plural in form and take a plural verb: *scissors, trousers,
spectacles, clothes, goods, belongings, premises, cattle, police*. Say *The police
**have** arrested him*, not ~~has~~.

Some look plural but are singular: *news, mathematics, physics, economics, politics
(as a subject), measles, innings*. Say *The news **is** good*.

**Possessive nouns.** Add *'s* to a singular (*Sita's bag*, *the boy's shoes*) and
just an apostrophe to a regular plural (*the students' hostel*, *the teachers'
room*). Irregular plurals take *'s*: *the children's park*, *the women's college*.

## 21.3 Pronouns

| Type | Forms | Example |
|---|---|---|
| Subject | I, we, you, he, she, it, they | **They** live in Dharan. |
| Object | me, us, you, him, her, it, them | Ram invited **us**. |
| Possessive adjective | my, our, your, his, her, its, their | This is **my** notebook. |
| Possessive pronoun | mine, ours, yours, his, hers, theirs | This notebook is **mine**. |
| Reflexive | myself, ourselves, yourself, yourselves, himself, herself, itself, themselves | She cut **herself**. |
| Relative | who, whom, whose, which, that | the man **who** called |
| Demonstrative | this, that, these, those | **Those** are my books. |
| Indefinite | someone, anybody, nothing, each, either, none, all | **Everyone** was present. |

*Its* is a possessive adjective; *it's* is a contraction of *it is* or *it has*.
They are never interchangeable.

- The tiger licked **its** paw. (possessive — no apostrophe)
- **It's** raining in Kathmandu again. (= it is)

## 21.4 Verbs: main, auxiliary and the five forms

Every regular verb has five forms. Learn them as a row, because tense, passive and
perfect constructions all pick one of them.

| Base (V1) | -s form | Past (V2) | Past participle (V3) | -ing form |
|---|---|---|---|---|
| walk | walks | walked | walked | walking |
| write | writes | wrote | written | writing |
| go | goes | went | gone | going |
| bring | brings | brought | brought | bringing |
| take | takes | took | taken | taking |
| choose | chooses | chose | chosen | choosing |
| lie (recline) | lies | lay | lain | lying |
| lay (put down) | lays | laid | laid | laying |

**Auxiliary verbs** (*be, do, have*) help a main verb build a tense, a question, a
negative or a passive. **Modal auxiliaries** (*can, may, must, should* …) add
meaning such as ability or obligation; they are Unit 24.

**Transitive verbs** take an object (*She wrote **a letter***); **intransitive
verbs** do not (*The baby slept*). Only transitive verbs can be made passive.

::: caution Verbs that already contain the preposition
Nepali learners often add a preposition English does not want:
~~discuss about~~ → **discuss** the problem; ~~return back~~ → **return**;
~~cope up with~~ → **cope with**; ~~request for~~ → **request** (but *ask for*);
~~order for~~ → **order**; ~~emphasise on~~ → **emphasise**;
~~investigate about~~ → **investigate**; ~~reach at~~ → **reach**;
~~enter into a room~~ → **enter** a room; ~~marry with~~ → **marry**;
~~resemble to~~ → **resemble**; ~~comprise of~~ → **comprise**.
And the reverse: ~~explain me~~ → **explain to me**; ~~listen the radio~~ →
**listen to the radio**.
:::

## 21.5 Adjectives and adverbs

An **adjective** modifies a noun; an **adverb** modifies a verb, an adjective or
another adverb. Many adverbs are made by adding *-ly*, but not all: *fast, hard,
late, early, well, straight* are both adjective and adverb with no *-ly*.

- He is a **careful** driver. → He drives **carefully**.
- The Koshi is a **dangerous** river in August. → It floods **dangerously** fast.

Beware the pairs whose *-ly* form means something different: *hard* (with effort)
vs *hardly* (almost not); *late* vs *lately* (recently); *near* vs *nearly*
(almost). *She worked hard* ≠ *She hardly worked*.

## 21.6 Words that change class

The same spelling often serves two classes. What decides the class is the job the
word is doing in that sentence, not the word itself.

| Word | As noun | As verb | As adjective |
|---|---|---|---|
| water | The **water** is cold. | **Water** the plants. | a **water** pump |
| light | Turn on the **light**. | **Light** the lamp. | a **light** bag |
| well | He drew water from the **well**. | Tears **welled** up. | I am **well**. |
| fast | He kept a **fast** on Ekadashi. | Muslims **fast** in Ramadan. | a **fast** bus |

This matters because Q7 often gives you a cue word in brackets and expects you to
convert it: *(decide) → decision / decisive / decisively*.

| Verb | Noun | Adjective | Adverb |
|---|---|---|---|
| decide | decision | decisive | decisively |
| succeed | success | successful | successfully |
| know | knowledge | knowledgeable | knowledgeably |
| strengthen | strength | strong | strongly |
| advise | advice | advisable | advisably |
| apply | application | applicable | — |
| develop | development | developed / developing | — |
| please | pleasure | pleasant | pleasantly |

::: example Worked transformation 21.1 — choosing the right derived form
**Problem.** Fill in the blank: *The ____ of the Melamchi project changed
Kathmandu's water supply. (complete)*

**Solution — four steps.**

1. **Find the slot.** The blank comes after *The* and before *of*. A slot after a
   determiner is a **noun** slot.
2. **Confirm with the verb.** The sentence already has a finite verb, *changed*.
   So the blank is not the verb; it is the subject head noun.
3. **Build the noun from the cue.** *complete* → noun *completion*.
4. **Check number and article.** Singular, definite: *The completion*.

**Answer.** *The **completion** of the Melamchi project changed Kathmandu's water
supply.*

Writing *completed* would give a subject with no head noun; writing *completely*
would put an adverb after *the*, which is impossible.
:::

## 21.7 Contracted forms

A **contraction** joins two words and replaces the missing letters with an
apostrophe. Contractions belong to speech and informal writing — dialogue, personal
letters, emails to friends. Keep full forms in essays, formal letters and
applications.

| Full form | Contraction | Full form | Contraction |
|---|---|---|---|
| I am | I'm | I have | I've |
| you are | you're | we have | we've |
| he is / he has | he's | I had / I would | I'd |
| she is / she has | she's | you will | you'll |
| it is / it has | it's | they will | they'll |
| we are | we're | I shall / I will | I'll |
| they are | they're | let us | let's |
| is not | isn't | was not | wasn't |
| are not | aren't | were not | weren't |
| do not | don't | does not | doesn't |
| did not | didn't | have not | haven't |
| has not | hasn't | had not | hadn't |
| cannot | can't | could not | couldn't |
| will not | won't | would not | wouldn't |
| shall not | shan't | should not | shouldn't |
| must not | mustn't | need not | needn't |
| ought not | oughtn't | am not (question) | aren't I? |

Three points that carry marks:

1. **`'s` is ambiguous.** *He's gone* = *he has gone*; *He's angry* = *he is
   angry*. Expand it by looking at what follows: a past participle means *has*.
2. **`'d` is ambiguous too.** *I'd finished* = *I had*; *I'd like tea* = *I would*.
3. **Two irregular spellings:** *will not* → **won't** (not ~~willn't~~) and
   *shall not* → **shan't**.

::: caution Apostrophe placement
The apostrophe replaces the *missing letters*, so it goes where they were:
*do not* → *do n't* → **don't**, not ~~do'nt~~. And never write ~~amn't~~ — in a
question English uses *aren't I?* (*I'm late, aren't I?*).
:::

## 21.8 Using a dictionary

A dictionary entry is not only a meaning. It carries four pieces of grammar you
need for Q7 and Q8.

```figure caption="Anatomy of a dictionary entry. The four boxed labels are the grammar information — word class, countability, verb pattern and register — that a Q7 item usually turns on."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,3.4))
ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
L = 0.04
# --- callout labels, all in a clear band at the top ---
ax.text(0.04, 0.985, "headword", fontsize=8.0, color=MUTED, ha='left', va='top')
ax.text(0.30, 0.985, "pronunciation", fontsize=8.0, color=MUTED, ha='left', va='top')
ax.text(0.615, 0.985, "class + countability", fontsize=8.0, color=ACCENT,
        ha='left', va='top')
for x0, x1, c in [(0.085, 0.085, MUTED), (0.355, 0.325, MUTED), (0.715, 0.585, ACCENT)]:
    ax.annotate("", xy=(x1, 0.845), xytext=(x0, 0.925),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=0.9, mutation_scale=8))
# --- the entry itself ---
ax.text(L, 0.79, "ad·vice", fontsize=12.5, color=INK, fontweight='bold')
ax.text(0.26, 0.795, "/ədˈvaɪs/", fontsize=9.5, color=MUTED)
ax.text(0.52, 0.795, "noun  [U]", fontsize=9.5, color=ACCENT)
ax.text(L, 0.665, "an opinion about what somebody should do", fontsize=9.2, color=INK)
ax.text(L, 0.585, "• She gave me some good advice.", fontsize=8.8, color=MUTED,
        style='italic')
ax.text(L, 0.495, "→ advise  verb [T]   advise sb to do sth", fontsize=9.2, color=INK)
ax.text(L, 0.410, "→ advisable  adj.  (formal)", fontsize=9.2, color=INK)
ax.annotate("verb pattern:\nwhat must follow it", xy=(0.545,0.487), xytext=(0.60,0.295),
            fontsize=8.0, color=SERIES[0], ha='left', va='center',
            arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=0.9, mutation_scale=8))
ax.annotate("register label", xy=(0.335,0.400), xytext=(0.06,0.300),
            fontsize=8.0, color=SERIES[2], ha='left', va='center',
            arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=0.9, mutation_scale=8))
ax.plot([L,0.97],[0.215,0.215], color=GRID, lw=1.0)
ax.text(L, 0.145, "[C] countable   [U] uncountable   [T] transitive   [I] intransitive",
        fontsize=8.3, color=INK)
ax.text(L, 0.055, "sb = somebody   sth = something   (fml) formal   (infml) informal",
        fontsize=8.3, color=MUTED)
```

**How to read the entry.**

- **Headword and syllables.** *ad·vice* shows where the word breaks at a line end
  and where the stress may fall.
- **Pronunciation** is in IPA between slashes. The mark ˈ comes *before* the
  stressed syllable: /ədˈvaɪs/ is stressed on the second syllable.
- **Word class label**, with **[C]** or **[U]** for nouns and **[T]** or **[I]**
  for verbs. This one label tells you whether *an advice* is possible. It is not.
- **Verb pattern**, e.g. *advise sb to do sth*, *succeed in doing sth*,
  *prevent sb from doing sth*. Copy the pattern exactly and the preposition
  errors in §21.4 disappear.
- **Register label**: *(formal)*, *(informal)*, *(old-fashioned)*, *(offensive)*,
  *(British/American)*. Useful in Q8 vocabulary items that ask for a word of the
  same meaning "in formal English".

Words are listed in **alphabetical order**, letter by letter to the end of the
word: *cheap, check, cheek, cheer, cheese*. The **guide words** at the top corners
of a printed page show the first and last headword on it, so you can find a page
without scanning every entry.

::: tip Reading the cue in brackets
When Q7 gives `(construct)` or `(happy)`, ask two questions in this order:
**(1) Which class does the slot need?** — look at what stands immediately before
and after it. **(2) Which form of the cue is that class?** Only then write. Blanks
after *the / a / my / some* need a **noun**; blanks after *be / seem / become* or
before a noun need an **adjective**; blanks modifying a verb need an **adverb**.
:::

::: example Worked transformation 21.2 — expanding contractions in formal rewriting
**Problem.** Rewrite formally: *They've told us they won't come, so we'd better
start without them.*

**Solution — step by step.**

1. **Mark every apostrophe:** *They've*, *won't*, *we'd*.
2. **Expand each, deciding the ambiguous ones from what follows.** *They've* + past
   participle *told* = *they have*. *won't* = *will not* (irregular). *we'd* +
   *better* = *we had* (the fixed phrase is *had better*).
3. **Rewrite, keeping everything else unchanged.**

**Answer.** *They **have** told us they **will not** come, so we **had** better
start without them.*
:::

::: example Worked transformation 21.3 — labelling word class in a test sentence
**Problem.** State the word class of each underlined word: *Unfortunately, the
**bus** from Pokhara **arrived** very **late** **because** of the landslide.*

**Solution.**

| Word | Test applied | Class |
|---|---|---|
| bus | follows the determiner *the*; is the thing doing the arriving | **noun** |
| arrived | carries the tense; can become *arrives / will arrive* | **verb** |
| late | tells us *when* about the verb *arrived*; not describing a noun | **adverb** |
| because | joins the main clause to the reason that follows | **conjunction** |

Note that *late* would be an **adjective** in *the late bus*, where it describes
the noun. Always test the word in its own sentence.
:::

## Chapter summary

- The eight classes are noun, pronoun, verb, adjective, adverb, preposition,
  conjunction and determiner; class is decided by the job the word does in *that*
  sentence, not by its spelling.
- Uncountable nouns — *information, advice, furniture, luggage, equipment, news,
  work, traffic* — have no plural and take no *a/an*; count them with *a piece of*.
- Every verb has five forms: V1, -s, V2, V3, -ing. Learn irregulars as a row.
- Only transitive verbs have objects, and only transitive verbs can be made passive.
- Do not add prepositions English does not want: *discuss, return, reach, enter,
  marry, resemble, emphasise, comprise* take a direct object.
- Contractions replace missing letters with an apostrophe: *'s* = is/has,
  *'d* = had/would; *won't* and *shan't* are irregular; *its* ≠ *it's*.
- A dictionary entry gives class, countability [C]/[U], transitivity [T]/[I], verb
  pattern and register — all the grammar a Q7 item can test.

## Practice questions

**Fill in the blanks with the correct form of the word in brackets (1 mark each)**

1. The ____ of the new bridge over the Trishuli took eighteen months. (construct) <span class="marks">[1]</span>
2. She spoke ____ about the problems of her village. (passion) <span class="marks">[1]</span>
3. His ____ to help the flood victims impressed everyone. (will) <span class="marks">[1]</span>
4. The medicine is not ____ for children under five. (advise) <span class="marks">[1]</span>
5. Tourism has ____ the economy of Pokhara. (strength) <span class="marks">[1]</span>
6. We were given very little ____ about the scholarship. (inform) <span class="marks">[1]</span>
7. The teacher explained the lesson ____ so that everyone understood. (clear) <span class="marks">[1]</span>
8. Dashain is the most widely ____ festival in Nepal. (celebrate) <span class="marks">[1]</span>

::: note Answers
**1.** construction — a noun is needed after *The* and before *of*.
**2.** passionately — an adverb modifying the verb *spoke*.
**3.** willingness — a noun is needed as the subject head after *His*.
**4.** advisable — an adjective is needed after the linking verb *is*.
**5.** strengthened — the slot after *has* needs a past participle (verb).
**6.** information — an uncountable noun after the quantifier *very little*.
**7.** clearly — an adverb telling us *how* he explained.
**8.** celebrated — a past participle used as an adjective before the noun *festival*.
:::

**Correct the errors in the following sentences (1 mark each)**

9. He gave me many useful informations about the college. <span class="marks">[1]</span>
10. We discussed about the flood relief programme for two hours. <span class="marks">[1]</span>
11. The police has arrested the two suspects. <span class="marks">[1]</span>
12. Please return back my dictionary tomorrow. <span class="marks">[1]</span>
13. She is my best friend and I like her advices. <span class="marks">[1]</span>
14. The bus reached at Butwal at seven o'clock. <span class="marks">[1]</span>
15. My uncle has bought two new furnitures for the shop. <span class="marks">[1]</span>
16. The dog wagged it's tail when it saw the child. <span class="marks">[1]</span>
17. He could not cope up with the pressure of the examination. <span class="marks">[1]</span>
18. Can you please explain me this rule once more? <span class="marks">[1]</span>

::: note Answers
**9.** He gave me much useful **information** about the college. — *information* is uncountable, so no plural and no *many*.
**10.** We **discussed** the flood relief programme for two hours. — *discuss* is transitive; it takes no *about*.
**11.** The police **have** arrested the two suspects. — *police* is a plural noun.
**12.** Please **return** my dictionary tomorrow. — *return* already means "give back"; *back* is redundant.
**13.** … I like her **advice**. — *advice* is uncountable; for units say *pieces of advice*.
**14.** The bus **reached** Butwal at seven o'clock. — *reach* takes a direct object, *arrive* takes *at/in*.
**15.** … two new **pieces of furniture** … — *furniture* is uncountable.
**16.** The dog wagged **its** tail … — possessive *its* has no apostrophe.
**17.** He could not **cope with** the pressure … — the verb is *cope with*, not *cope up with*.
**18.** Can you please **explain this rule to me** once more? — *explain* cannot take an indirect object without *to*.
:::

**Rewrite as instructed (1 mark each)**

19. *I've never seen such a crowd at Pashupatinath.* — Rewrite using full forms. <span class="marks">[1]</span>
20. *She is not coming because she does not feel well.* — Rewrite using contractions. <span class="marks">[1]</span>
21. *He's finished his homework.* — Expand the contraction correctly. <span class="marks">[1]</span>
22. *We'd rather travel by bus.* — Expand the contraction correctly. <span class="marks">[1]</span>
23. *I am late, ____ I?* — Complete with the correct contracted question form. <span class="marks">[1]</span>
24. *The students hostel is behind the library.* — Insert the apostrophe correctly. <span class="marks">[1]</span>

::: note Answers
**19.** **I have** never seen such a crowd at Pashupatinath. — *'ve* is always *have*.
**20.** She **isn't** coming because she **doesn't** feel well. — standard negative contractions.
**21.** **He has** finished his homework. — *'s* before a past participle is *has*.
**22.** **We would** rather travel by bus. — the fixed phrase is *would rather*.
**23.** aren't — English uses *aren't I?* because *amn't* does not exist.
**24.** The **students'** hostel is behind the library. — plural possessive: apostrophe after the -s.
:::

**Identify the word class of the word in bold (1 mark each)**

25. The **light** in the classroom was too dim. <span class="marks">[1]</span>
26. Please **light** the lamp before the puja begins. <span class="marks">[1]</span>
27. He carried a **light** bag up to Sarangkot. <span class="marks">[1]</span>
28. She hardly **ever** visits her village now. <span class="marks">[1]</span>
29. The shop is **between** the bank and the post office. <span class="marks">[1]</span>
30. **Although** it was raining, the match continued. <span class="marks">[1]</span>

::: note Answers
**25.** Noun — it follows the determiner *The* and is the subject.
**26.** Verb — it is the imperative, the action being ordered.
**27.** Adjective — it describes the noun *bag*.
**28.** Adverb — *ever* modifies the verb *visits* (frequency).
**29.** Preposition — it relates the noun phrase *the bank and the post office* to *the shop*.
**30.** Conjunction — it joins a subordinate clause to the main clause.
:::
