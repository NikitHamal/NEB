---
subject: English
grade: BCA
unit: 3
title: Articles, Tenses and Subject-Verb Agreement
hours: 7
area: Grammar
---

This is the heaviest unit of the English paper, with about seven questions and the core of what the Dean's Office model tests: "She is ___ obedient student" (an), "Ramesh ___ here for the last seven years" (has worked), "Neither of them ___ a problem" (anticipates). Three skills decide it: choose the article by *sound*, choose the tense by the time signal, and make the verb agree with the real subject.

::: key What the paper asks from this chapter
- **Articles**: *a/an* by sound; *the* for unique or specific things; zero article for meals, languages, games.
- **Tenses**: *for/since* with the present perfect, past time words with the simple past, past perfect for the earlier of two past actions.
- **Agreement**: *each, every, either, neither, one of* take singular verbs; *a number of* is plural, *the number of* singular.
:::

## 3.1 Use of articles

- **a / an** depend on the *sound*: *an* hour, an honest man, an MP, an umbrella; *a* university, a European, a one-rupee note.
- **the**: unique things (the sun, the moon), superlatives (the highest peak), rivers, ranges and oceans (the Koshi, the Himalayas, the Pacific), nationalities (the Nepalese), when both speaker and listener know which one.
- **no article**: meals (have breakfast), languages (speak English), games (play cricket), general plurals and uncountables (water boils), names, and institutions in their normal use (go to school, go to bed).

```photogrid label="3.1" cols="3" ratio="1.0" caption="Articles follow sound and meaning. (a) The Big Ben clock: we say an hour because the word begins with the vowel sound ow, although h is a consonant letter. (b) An umbrella begins with a vowel sound, so it takes an. (c) Mount Everest: we say the highest peak because a superlative and a unique thing take the (Fig 3.1)."
@ photo id="bcamath/bigben" cap="an hour (silent h)"
focus 0.5 0.5
@ photo id="bcaeng/umbrella" cap="an umbrella (vowel sound)"
focus 0.5 0.5
@ photo id="bcagk/everest" cap="the highest peak (superlative)"
focus 0.5 0.5
```

```svgfig label="3.1" caption="Choosing an article in three questions. First ask whether the listener already knows which one you mean (unique, already mentioned, superlative, river or range): if so use the. If not, ask whether the noun is singular and countable: if it is plural, uncountable, a meal, a language or a game, use no article. Otherwise decide by the first SOUND of the next word: vowel sound gives an, consonant sound gives a. The table applies the sound rule in the cell to seven words, and note that university and one-rupee begin with the consonant sounds yoo and wun."
snd = {"hour": ("ow-er", True), "honest": ("on-ist", True), "MP": ("em-pee", True), "umbrella": ("um-brel-a", True), "university": ("yoo-ni-ver-si-ti", False), "European": ("yoor-o-pee-an", False), "one-rupee": ("wun roo-pee", False)}
art = {w: ("an" if v else "a") for w, (s, v) in snd.items()}
assert art == {"hour": "an", "honest": "an", "MP": "an", "umbrella": "an", "university": "a", "European": "a", "one-rupee": "a"}
f = Fig(780, 340)
f.box(14, 14, 250, 66, "Does the listener know which one?\n(unique, mentioned, superlative,\nriver, range)", fill=BLUE, stroke=NAVY, size=10.5)
f.box(14, 120, 250, 56, "Is it singular and countable?", fill=BLUE, stroke=NAVY, size=10.5)
f.box(14, 220, 250, 56, "Does the next SOUND start\nwith a vowel sound?", fill=BLUE, stroke=NAVY, size=10.5)
f.box(320, 22, 110, 44, "the", fill=MINT, stroke=TEAL, color=TEAL, size=16, bold=True)
f.box(320, 124, 140, 48, "no article\n(plural, meals)", fill=SAND, stroke=AMBER, color=AMBER, size=10.5, bold=True)
f.box(320, 214, 70, 34, "an", fill=MINT, stroke=TEAL, color=TEAL, size=14, bold=True)
f.box(320, 258, 70, 34, "a", fill=MINT, stroke=TEAL, color=TEAL, size=14, bold=True)
f.arrow([(264, 44), (320, 44)], color=TEAL); f.text(292, 36, "yes", size=10.5, color=TEAL, bold=True)
f.arrow([(139, 80), (139, 120)], color=RED); f.text(155, 104, "no", size=10.5, color=RED, bold=True, anchor="start")
f.arrow([(264, 148), (320, 148)], color=AMBER); f.text(292, 140, "no", size=10.5, color=RED, bold=True)
f.arrow([(139, 176), (139, 220)], color=TEAL); f.text(155, 202, "yes", size=10.5, color=TEAL, bold=True, anchor="start")
f.arrow([(264, 238), (320, 231)], color=TEAL); f.text(292, 218, "yes", size=10.5, color=TEAL, bold=True)
f.arrow([(264, 262), (320, 275)], color=RED); f.text(292, 276, "no", size=10.5, color=RED, bold=True)
for hd, hx, hw in [("word", 490, 84), ("sound", 578, 100), ("article", 682, 88)]:
    f.box(hx, 14, hw, 24, hd, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
for i, (w, (s, v)) in enumerate(snd.items()):
    y = 42 + i * 28
    f.box(490, y, 84, 24, w, fill=SOFT, stroke="#cbd5e1", color=SLATE, size=10.5, bold=True)
    f.box(578, y, 100, 24, s, fill=SOFT, stroke="#cbd5e1", color=SLATE, size=9.5)
    f.box(682, y, 88, 24, art[w] + " " + w.split()[0], fill=(MINT if v else SAND), stroke=(TEAL if v else AMBER), color=(TEAL if v else AMBER), size=10.5, bold=True)
f.text(630, 262, "the letter does not matter,", size=10.5, color=RED, bold=True); f.text(630, 282, "only the first sound", size=10.5, color=RED, bold=True)
```

```svgfig label="3.2" caption="All twelve tenses of one verb, built by the cell from four forms: write, wrote, written, writing. Rows are past, present and future; columns are simple, continuous, perfect and perfect continuous. Read the grid by pairing time with aspect: perfect means finished before a point, continuous means in progress, perfect continuous means in progress up to a point. The cell asserts the standard forms, for example she has been writing and she will have written."
V1, V2, V3, ING = "write", "wrote", "written", "writing"
G = {("past", "simple"): V2, ("past", "continuous"): "was " + ING, ("past", "perfect"): "had " + V3, ("past", "perfect continuous"): "had been " + ING,
     ("present", "simple"): V1 + "s", ("present", "continuous"): "is " + ING, ("present", "perfect"): "has " + V3, ("present", "perfect continuous"): "has been " + ING,
     ("future", "simple"): "will " + V1, ("future", "continuous"): "will be " + ING, ("future", "perfect"): "will have " + V3, ("future", "perfect continuous"): "will have been " + ING}
assert len(G) == 12 and G[("present", "perfect continuous")] == "has been writing" and G[("future", "perfect")] == "will have written" and G[("past", "perfect")] == "had written"
HINT = {"simple": "habit, fact, finished time", "continuous": "in progress at that time", "perfect": "finished before a point", "perfect continuous": "progress up to a point"}
f = Fig(780, 330)
cols = ["simple", "continuous", "perfect", "perfect continuous"]
for j, c in enumerate(cols):
    f.box(100 + j * 170, 10, 166, 26, c, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
fills = {"past": (SAND, AMBER), "present": (MINT, TEAL), "future": (BLUE, NAVY)}
for i, t in enumerate(["past", "present", "future"]):
    y = 42 + i * 92
    f.box(14, y, 82, 86, t, fill=fills[t][1], stroke=fills[t][1], color="#ffffff", size=12, bold=True)
    for j, c in enumerate(cols):
        f.box(100 + j * 170, y, 166, 86, "", fill=fills[t][0], stroke=fills[t][1], r=4)
        f.text(183 + j * 170, y + 34, "she " + G[(t, c)], size=10.5, color=fills[t][1], bold=True)
        f.text(183 + j * 170, y + 58, HINT[c], size=9.5, color=SLATE)
f.text(390, 322, "time (past, present, future) x aspect (simple, continuous, perfect, perfect continuous) = 12", size=10.5, color=NAVY, bold=True)
```

## 3.2 Use of tenses

| Tense | Signals and example |
|---|---|
| Simple present | habits and facts: Water boils at 100°C. |
| Present continuous | now: She is reading. |
| Present perfect | *for, since, already, yet, just, ever*: He has lived here since 2010. |
| Present perfect continuous | duration up to now: I have been waiting since morning. |
| Simple past | finished time: She went to Pokhara yesterday. |
| Past continuous | action in progress when another happened: I was watching TV when the phone rang. |
| Past perfect | the earlier of two past actions: The film had started when we arrived. |
| Future perfect | by a future time: By next year he will have completed his degree. |

**for / since.** *For* a length of time (for three days); *since* a starting point (since 2015). Both take the present perfect. Do not use the present perfect with *yesterday, last year, ago*.

```svgfig label="3.3" caption="Three tense questions drawn on a time line, with the numbers computed. (a) Past perfect: the film started at 6:00 and we arrived at 6:15, so the earlier action takes had started and the later one takes arrived. (b) Past continuous: I was watching TV from 7:00 to 8:00 when the phone rang at 7:30, half way through the programme. (c) Present perfect continuous: waiting since 8 a.m. at 11 a.m. is for 3 hours, so since gives the start and for gives the length."
t = lambda h, m: h * 60 + m
assert t(6, 15) - t(6, 0) == 15 and t(7, 30) - t(7, 0) == 30 and t(8, 0) - t(7, 0) == 60 and (t(11, 0) - t(8, 0)) // 60 == 3
f = Fig(780, 330)
def row(y, title, a0, a1):
    f.text(14, y - 34, title, size=11.5, color=NAVY, anchor="start", bold=True)
    f.arrow([(a0, y), (a1, y)], color=SLATE, sw=1.8)
row(60, "(a) Past perfect: the earlier of two past actions", 40, 740)
f.circle(160, 60, 6, fill="#fde68a", stroke=AMBER); f.text(160, 46, "6:00 film had started", size=10.5, color=AMBER, bold=True)
f.circle(420, 60, 6, fill="#bbf7d0", stroke=TEAL); f.text(420, 46, "6:15 we arrived", size=10.5, color=TEAL, bold=True)
f.arrow([(166, 80), (414, 80)], color=RED, both=True); f.text(290, 98, "15 minutes", size=10.5, color=RED, bold=True)
row(170, "(b) Past continuous: in progress when something else happened", 40, 740)
f.box(160, 154, 300, 26, "", fill=BLUE, stroke=NAVY); f.text(168, 171, "was watching TV", size=10.5, color=NAVY, anchor="start", bold=True); f.text(452, 171, "7:00 to 8:00", size=10.5, color=NAVY, anchor="end", bold=True)
f.circle(310, 170, 6, fill="#fecaca", stroke=RED); f.text(310, 204, "7:30 the phone rang (half way)", size=10.5, color=RED, bold=True)
row(270, "(c) Present perfect continuous: since the start, for the length", 40, 740)
f.circle(160, 270, 6, fill="#fde68a", stroke=AMBER); f.text(160, 256, "since 8 a.m.", size=10.5, color=AMBER, bold=True)
f.circle(520, 270, 6, fill="#bbf7d0", stroke=TEAL); f.text(520, 256, "now: 11 a.m.", size=10.5, color=TEAL, bold=True)
f.arrow([(166, 290), (514, 290)], color=RED, both=True); f.text(340, 312, "for 3 hours: I have been waiting since 8 a.m.", size=10.5, color=RED, bold=True)
```

## 3.3 Subject-verb agreement

- **Singular**: each, every, either, neither, one of the + plural noun, everyone, nobody; *mathematics, physics, news, economics*; the number of; distances and sums treated as one (two-thirds of the land *is*).
- **Plural**: a number of, both, few, many; *scissors, trousers, spectacles*; the poor, the rich.
- *along with, together with, as well as, besides* do not change the verb: Ram, along with his friends, **is** going.
- *either … or, neither … nor, not only … but also*: the verb agrees with the **nearer** subject.
- *There is/are*: the verb agrees with the noun after it.

```svgfig label="3.4" caption="Subject-verb agreement, decided by rule. The cell applies each rule to a phrase and checks the verb. Either-or and neither-nor take the verb of the NEARER subject; along with and as well as do not change the verb; a number of is plural but the number of is singular; each, every and everyone are singular; the verb after there is agrees with the noun that follows."
def verb(rule, a_pl, b_pl=None):
    if rule == "near": return "are" if b_pl else "is"
    if rule == "first": return "are" if a_pl else "is"
    if rule == "plural": return "are"
    if rule == "singular": return "is"
rows = [("Neither the teacher nor the students", "nearer subject (students)", verb("near", False, True), "are"), ("Neither the students nor the teacher", "nearer subject (teacher)", verb("near", True, False), "is"),
        ("Ram, along with his friends,", "first subject only", verb("first", False), "is"), ("A number of students", "a number of = plural", verb("plural", True), "are"),
        ("The number of students", "the number of = singular", verb("singular", False), "is"), ("Each of the boys", "each = singular", verb("singular", False), "is"),
        ("Mathematics", "subject name = singular", verb("singular", False), "is"), ("Scissors", "pair noun = plural", verb("plural", True), "are")]
assert all(r[2] == r[3] for r in rows)
f = Fig(780, 330)
for j, (hd, x, w) in enumerate([("phrase", 14, 300), ("rule", 318, 250), ("verb", 572, 90)]):
    f.box(x, 10, w, 26, hd, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
for i, (a, b, c, d) in enumerate(rows):
    y = 42 + i * 34
    f.box(14, y, 300, 30, a, fill=SOFT, stroke="#cbd5e1", color=SLATE, size=10.5, bold=True)
    f.box(318, y, 250, 30, b, fill=SOFT, stroke="#cbd5e1", color=SLATE, size=10.5)
    f.box(572, y, 90, 30, c, fill=(MINT if c == "is" else SAND), stroke=(TEAL if c == "is" else AMBER), color=(TEAL if c == "is" else AMBER), size=12, bold=True)
f.text(724, 120, "is = singular", size=10.5, color=TEAL, bold=True); f.text(724, 142, "are = plural", size=10.5, color=AMBER, bold=True)
f.text(724, 190, "find the real", size=10.5, color=RED, bold=True); f.text(724, 208, "subject, ignore", size=10.5, color=RED, bold=True); f.text(724, 226, "the words between", size=10.5, color=RED, bold=True)
```

## 3.4 Eight traps in articles, tenses and agreement

These three topics produce most of the grammar marks, and the wrong options are built from the same eight mistakes.

1. **Sound decides *a* or *an*, not the letter.** We say *an hour* and *an honest man* because the first sound is a vowel, and *a university* and *a one-rupee note* because the first sound is a consonant (Fig 3.1). Say the word aloud. Do not look at the first letter alone.
2. **Use *the* for unique and superlative things.** *The sun*, *the highest peak*, *the Koshi*, *the Himalayas* and *the Nepalese* all take *the*. Meals, languages and games take no article: *have breakfast*, *speak Nepali*, *play cricket*. The phrase *go to school* has no article when you go to study.
3. **Do not use the present perfect with a finished time.** *He has gone yesterday* is wrong; use *He went yesterday*. Words such as *yesterday*, *last year* and *ago* need the simple past (Fig 3.2). The present perfect goes with *for*, *since*, *already*, *yet*, *just* and *ever*.
4. **Since gives the start and for gives the length.** *I have been waiting since 8 a.m.* and *I have been waiting for three hours* mean the same thing (Fig 3.3). Both take the present perfect or present perfect continuous. Never write *since three hours*.
5. **Past perfect marks the earlier action.** In "The film had started when we arrived", the film started first, so it takes *had started* (Fig 3.3). Only use it when two past actions are in the same sentence. A single past action needs the simple past.
6. **Find the real subject.** In "Ram, along with his friends, is going", the subject is Ram, so the verb is singular. *Along with*, *together with* and *as well as* do not change the verb (Fig 3.4). Ignore the words between the subject and the verb.
7. **Either-or and neither-nor use the nearer subject.** "Neither the teacher nor the students *are* present" uses *are* because *students* is nearer. Swap the order and the verb changes to *is*. For *there is/are*, look at the noun after the verb.
8. **Know the singular surprises.** *Mathematics*, *physics*, *news*, *economics* and *the number of* are singular. *A number of*, *scissors*, *trousers* and *spectacles* are plural. *Each*, *every*, *either*, *neither* and *everyone* always take a singular verb.

### 3.4.1 Worked checks

**Q. Fill in the blank: "She is ____ honest girl." (a / an / the)**

**Answer.** *Honest* begins with the vowel sound *on*, because h is silent, so the answer is **an**: "She is an honest girl" (Fig 3.1).

**Q. Correct the sentence: "He has gone to Pokhara yesterday."**

**Answer.** *Yesterday* is a finished time, so the present perfect is wrong. The correct sentence is "He **went** to Pokhara yesterday" (Fig 3.2).

**Q. Choose the verb: "The number of students ____ increasing. (is / are)"**

**Answer.** *The number of* is singular, so the verb is **is**. With *a number of students* the verb would be *are* (Fig 3.4).

**Q. Choose the tense: "The film ____ when we reached the hall. (started / had started)"**

**Answer.** The film began before we reached the hall, so use the past perfect: "The film **had started** when we reached the hall" (Fig 3.3).

## Formula and fact sheet

| Item | Rule |
|---|---|
| an | before a vowel *sound* |
| since / for | point / duration |
| each, every, neither | singular verb |
| a number of / the number of | plural / singular |
| either … or | nearer subject |

## Chapter summary

- Say the word aloud: the first sound, not the first letter, picks *a* or *an*.
- The present perfect is for a time up to now; the simple past is for a finished time.
- The past perfect marks the earlier of two past actions.
- *Each of, neither of, one of* + plural noun → singular verb.
- *Along with* does not make a subject plural.

## Practice questions

**Set A — Recall (20 questions)**

1. She is ___ obedient student.
   (a) a (b) the (c) an (d) no article
2. ___ sun rises in the east.
   (a) A (b) An (c) No article (d) The
3. He is ___ honest man.
   (a) an (b) a (c) the (d) no article
4. Ramesh ___ here for the last seven years.
   (a) worked (b) has worked (c) is working (d) works
5. He has been ill ___ three days.
   (a) since (b) from (c) at (d) for
6. Mount Everest is ___ highest peak in the world.
   (a) a (b) an (c) the (d) no article
7. Neither of the boys ___ present.
   (a) are (b) is (c) were (d) have
8. Each of the students ___ a prize.
   (a) has (b) have (c) are (d) were
9. She ___ to Pokhara yesterday.
   (a) goes (b) has gone (c) went (d) gone
10. I ___ my homework before my mother came home.
    (a) had finished (b) have finished (c) finish (d) was finish
11. Mathematics ___ my favourite subject.
    (a) are (b) were (c) have (d) is
12. The news ___ true.
    (a) are (b) is (c) were (d) have
13. He is ___ European.
    (a) an (b) the (c) a (d) no article
14. Water ___ at 100°C.
    (a) is boiling (b) boiled (c) has boiled (d) boils
15. I ___ TV when the phone rang.
    (a) was watching (b) watched (c) am watching (d) have watched
16. There ___ many books on the table.
    (a) is (b) are (c) was (d) has
17. He plays ___ cricket every evening.
    (a) a (b) the (c) no article (d) an
18. I have ___ umbrella.
    (a) an (b) a (c) the (d) no article
19. By next year, he ___ his degree.
    (a) completes (b) completed (c) will complete (d) will have completed
20. The Koshi is ___ longest river in Nepal.
    (a) a (b) the (c) an (d) no article

::: note Answers and explanations — Set A
**1.** (c) — "obedient" starts with a vowel sound.
**2.** (d) — the sun is unique.
**3.** (a) — "honest" starts with a vowel sound (silent h).
**4.** (b) — "for the last seven years" needs the present perfect.
**5.** (d) — for + a length of time.
**6.** (c) — superlative takes the.
**7.** (b) — neither of takes a singular verb.
**8.** (a) — each takes a singular verb.
**9.** (c) — "yesterday" needs the simple past.
**10.** (a) — finishing came before her arrival: past perfect.
**11.** (d) — a subject name is singular.
**12.** (b) — news is singular.
**13.** (c) — "European" starts with a "y" sound.
**14.** (d) — a general truth: simple present.
**15.** (a) — an action in progress when the phone rang.
**16.** (b) — plural noun "books" follows.
**17.** (c) — no article with games.
**18.** (a) — "umbrella" starts with a vowel sound.
**19.** (d) — by next year: future perfect.
**20.** (b) — a superlative takes the.
:::

**Set B — Understanding (12 questions)**

1. A number of students ___ absent today.
   (a) is (b) was (c) are (d) has
2. The number of students ___ increasing.
   (a) is (b) are (c) were (d) have
3. Ram, along with his friends, ___ going to Pokhara.
   (a) are (b) were (c) have (d) is
4. Either Hari or his brothers ___ responsible.
   (a) is (b) are (c) was (d) has
5. By the time we reached, the film ___.
   (a) started (b) has started (c) had started (d) was starting
6. I ___ for him since morning.
   (a) have been waiting (b) am waiting (c) waited (d) wait
7. He said he ___ the book already.
   (a) read (b) reads (c) has read (d) had read
8. One of my friends ___ a doctor.
   (a) are (b) is (c) were (d) have
9. The poor ___ always been neglected.
   (a) have (b) has (c) is (d) was
10. Choose the correct sentence.
    (a) He don't know the answer. (b) He doesn't knows the answer. (c) He doesn't know the answer. (d) He don't knows the answer.
11. He is ___ MP from Kaski.
    (a) a (b) the (c) no article (d) an
12. The scissors ___ on the table.
    (a) is (b) are (c) has (d) was

::: note Answers and explanations — Set B
**1.** (c) — a number of takes a plural verb.
**2.** (a) — the number of takes a singular verb.
**3.** (d) — "along with" does not change the verb.
**4.** (b) — the nearer subject, brothers, is plural.
**5.** (c) — the film started before we reached: past perfect.
**6.** (a) — "since morning" with an action still going on.
**7.** (d) — backshifted past perfect.
**8.** (b) — one of takes a singular verb.
**9.** (a) — "the poor" is plural.
**10.** (c) — doesn't + base verb.
**11.** (d) — "MP" is pronounced "em-pee", a vowel sound.
**12.** (b) — scissors is plural.
:::

**Set C — Application (8 questions)**

1. Each boy and each girl ___ a book.
   (a) have (b) were (c) are (d) has
2. He ___ in Kathmandu since 2010.
   (a) has lived (b) lived (c) is living (d) lives
3. I ___ him last week.
   (a) have met (b) meet (c) met (d) had meet
4. The sun ___ in the east.
   (a) rose (b) rises (c) is rising (d) has risen
5. Not only the students but also the teacher ___ present.
   (a) were (b) are (c) have (d) was
6. She ___ for two hours when I arrived.
   (a) had been waiting (b) has waited (c) was wait (d) waits
7. ___ university is a place of learning.
   (a) An (b) A (c) The (d) No article
8. Two-thirds of the land ___ under water.
   (a) are (b) were (c) is (d) have

::: note Answers and explanations — Set C
**1.** (d) — each and each: singular.
**2.** (a) — since + a starting point: present perfect.
**3.** (c) — "last week" is a finished time.
**4.** (b) — a universal truth.
**5.** (d) — nearer subject "teacher" is singular.
**6.** (a) — an action that had been going on before another past event.
**7.** (b) — "university" begins with a "y" sound.
**8.** (c) — "land" is singular, so is.
:::
