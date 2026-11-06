---
subject: English
grade: BCA
unit: 6
title: Pronouns, Determiners, Modals, Comparison and Error Spotting
hours: 5
area: Grammar
---

This unit gathers the rest of grammar: pronoun forms, quantifiers, modal verbs, comparison, conjunctions and the "find the error" type. The Dean's Office model includes "Two ladies had ___ hand bags stolen" (their) and "There is someone in the room ___ I certainly heard a great noise" (for). Five questions in the paper come from here.

::: key What the paper asks from this chapter
- **Pronouns**: subject/object/possessive/reflexive; a possessive agrees with its owner.
- **Determiners**: *few / a few*, *little / a little*, *much / many*, *less / fewer*.
- **Modals**: obligation, prohibition, advice, deduction.
- **Comparison and conjunctions**: *than/to*, *no sooner … than*, *hardly … when*.
- **Error spotting**: the usual errors (uncountable plurals, wrong comparison, subject–verb).
:::

## 6.1 Pronouns and determiners

- Possessive adjectives: my, your, his, her, **its**, our, their (*its* has no apostrophe; *it's* = it is). *Each of the boys has done his homework.* Reflexives end in *-self/-selves* (himself, themselves). *Each other* for two, *one another* for more.
- *Few / many* (countable) and *little / much* (uncountable). **A few / a little** = some (positive); **few / little** = hardly any (negative). **Fewer** with countable nouns, **less** with uncountable.
- **Both** takes a plural verb; **either / neither / each** take a singular verb. Information, advice, furniture, news, luggage and equipment are uncountable: *some information*, never *informations*.

```svgfig label="6.1" caption="Pronoun forms in one table. Each row is one person; the cell checks the table: every reflexive ends in -self or -selves, no possessive has an apostrophe, and the two possessive pronouns that do not end in s are mine and his. Its (possessive) has no apostrophe: The dog wagged its tail. It's always means it is or it has. Say My friend and I went, with the other person first and the subject form I."
P = [("I", "I", "me", "my", "mine", "myself"), ("you", "you", "you", "your", "yours", "yourself"),
     ("he", "he", "him", "his", "his", "himself"), ("she", "she", "her", "her", "hers", "herself"),
     ("it", "it", "it", "its", "-", "itself"), ("we", "we", "us", "our", "ours", "ourselves"),
     ("they", "they", "them", "their", "theirs", "themselves")]
assert len(P) == 7
assert all(r[5].endswith(("self", "selves")) for r in P)
assert all("'" not in c for r in P for c in r)
assert [r[4] for r in P if r[4] != "-" and not r[4].endswith("s")] == ["mine"]
assert [r[0] for r in P if r[3] == r[4]] == ["he"]
f = Fig(780, 340)
x0 = [88, 224, 360, 496, 632]
hd = ["subject", "object", "possessive\nadjective", "possessive\npronoun", "reflexive"]
cl = [NAVY, NAVY, TEAL, TEAL, AMBER]
for h, x, c in zip(hd, x0, cl):
    f.box(x, 8, 132, 34, h, fill=c, stroke=c, color="#ffffff", size=10.5, bold=True)
fills = [BLUE, BLUE, MINT, MINT, SAND]
strokes = [NAVY, NAVY, TEAL, TEAL, AMBER]
for i, r in enumerate(P):
    y = 48 + i * 30
    f.box(14, y, 70, 26, r[0], fill=SOFT, stroke="#94a3b8", color=NAVY, size=11, bold=True)
    for j in range(5):
        f.box(x0[j], y, 132, 26, r[j + 1], fill=fills[j], stroke=strokes[j], color=SLATE, size=11.5, bold=(r[j + 1] in ("its", "mine", "himself", "themselves")))
f.box(14, 262, 752, 66, "", fill=ROSE, stroke=RED, r=5)
f.text(28, 280, "Never: hisself, theirselves, it's tail, her's, their's, me and my friend went.", size=11, color=RED, anchor="start", bold=True)
f.text(28, 300, "Between you and me (object after a preposition). He is taller than I (am) (subject after than).", size=11, color=SLATE, anchor="start")
f.text(28, 318, "Each other is for two persons, one another for more. Each of the boys has done his homework.", size=11, color=SLATE, anchor="start")
```

```svgfig label="6.2" caption="Determiners by noun type. Countable nouns (students, friends, errors) take many, a few, few and fewer; uncountable nouns (water, time, noise) take much, a little, little and less. A few and a little are positive (some); few and little are negative (hardly any). The cell builds each example sentence and checks that the determiner matches the noun type."
COUNT = ["students", "friends", "errors"]
UNC = ["water", "time", "noise"]
D = [("many", "countable", "a large number", "Many students were absent.", COUNT),
     ("much", "uncountable", "a large amount", "There is not much water.", UNC),
     ("a few", "countable", "some (positive)", "A few friends came to help.", COUNT),
     ("few", "countable", "hardly any (negative)", "Few friends came; I felt sad.", COUNT),
     ("a little", "uncountable", "some (positive)", "Give me a little time.", UNC),
     ("little", "uncountable", "hardly any (negative)", "There is little time left.", UNC),
     ("fewer", "countable", "a smaller number", "Fewer errors this week.", COUNT),
     ("less", "uncountable", "a smaller amount", "Less noise, please.", UNC)]
for d, k, m, s, nouns in D:
    assert any(n in s for n in nouns), s
    assert (k == "countable") == (nouns is COUNT)
assert sum(1 for d in D if d[1] == "countable") == 4
f = Fig(780, 330)
cx = [(14, 100, "determiner"), (118, 120, "goes with"), (242, 200, "meaning"), (446, 320, "example")]
for x, w, h in cx:
    f.box(x, 8, w, 24, h, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
for i, (d, k, m, s, nn) in enumerate(D):
    y = 36 + i * 28
    c = TEAL if k == "countable" else AMBER
    bg = MINT if k == "countable" else SAND
    f.box(14, y, 100, 24, d, fill=bg, stroke=c, color=c, size=12, bold=True)
    f.box(118, y, 120, 24, k, fill=bg, stroke=c, color=c, size=11)
    f.box(242, y, 200, 24, m, fill=SOFT, stroke="#cbd5e1", color=SLATE, size=11)
    f.box(446, y, 320, 24, s, fill=SOFT, stroke="#cbd5e1", color=NAVY, size=11, anchor="start")
f.box(14, 266, 752, 50, "", fill=BLUE, stroke=NAVY, r=5)
f.text(28, 284, "Both takes a plural verb; each, either and neither take a singular verb.", size=11, color=SLATE, anchor="start")
f.text(28, 303, "The number of students IS increasing (the number); a number of students ARE absent (several).", size=11, color=SLATE, anchor="start")
```

## 6.2 Modal verbs

| Modal | Meaning |
|---|---|
| can / could | ability, permission |
| may / might | permission, possibility |
| must | strong obligation, strong deduction (He must be at home) |
| mustn't | prohibition |
| needn't / don't have to | no obligation |
| should / ought to | advice, duty |
| would rather | preference + bare verb |

*should have + V3* is criticism of a past act; *must have + V3* is a past deduction.

```photogrid label="6.1" cols="2" ratio="1.0" caption="Two signs, two modal verbs. (a) A hard-hat sign on a building site (Fig 6.3): Hard hats must be worn is strong obligation (must). (b) A no-smoking sign (cropped from a larger photo of a lamp post): You mustn't smoke here is prohibition (mustn't), whereas You needn't pay now means no obligation (Fig 6.3)."
@ photo id="bcaeng/hardhat" cap="must: strong obligation"
focus 0.5 0.6
@ photo id="bcaeng/nosmoke" cap="mustn't: prohibition"
focus 0.5 0.5
```

```svgfig label="6.3" caption="Modal verbs on two ladders. Left: present duty, from strong must to prohibition mustn't, with needn't meaning no duty. Right: modal + have + V3 looks at the past: must have = sure it happened, may or might have = maybe, can't have = sure it did not happen, should have = criticism of an act that did not happen. The cell checks that must have goes with lost (V3 of lose) and counts the rows."
V3 = {"lose": "lost", "leave": "left", "tell": "told"}
past = [("must have", "lose", "sure it happened"), ("may / might have", "leave", "maybe it happened"),
        ("can't have", "leave", "sure it did not happen"), ("should have", "tell", "criticism: it did not happen")]
S = ["I must have lost my keys.", "She may have left already.", "He can't have left; his bag is here.", "You should have told me earlier."]
assert past[0][0].split()[0] == "must" and V3[past[0][1]] == "lost"
assert len(past) == 4 and S[3].endswith("earlier.") and "told" in S[3]
now = [("must", "strong duty", "Hard hats must be worn."), ("have to", "rule from outside", "I have to wake up at five."),
       ("should /\nought to", "advice", "You should see a doctor."), ("needn't", "no duty", "You needn't pay now."),
       ("mustn't", "prohibition", "You mustn't smoke here.")]
assert len(now) == 5
f = Fig(780, 330)
f.text(190, 14, "Now: duty, advice, prohibition", size=11.5, color=NAVY, bold=True)
f.text(576, 14, "Past: modal + have + V3", size=11.5, color=NAVY, bold=True)
cols = [NAVY, NAVY, TEAL, AMBER, RED]
bgs = [BLUE, BLUE, MINT, SAND, ROSE]
for i, (m, k, e) in enumerate(now):
    y = 30 + i * 58
    f.box(14, y, 112, 50, m, fill=cols[i], stroke=cols[i], color="#ffffff", size=11, bold=True)
    f.box(130, y, 250, 50, k + "\n" + e, fill=bgs[i], stroke=cols[i], color=SLATE, size=11)
for i, (m, v, k) in enumerate(past):
    y = 30 + i * 70
    f.box(396, y, 130, 60, m, fill=cols[i], stroke=cols[i], color="#ffffff", size=11, bold=True)
    f.box(530, y, 236, 60, k + "\n" + S[i], fill=bgs[i], stroke=cols[i], color=SLATE, size=10.5)
f.text(576, 322, "Would rather + bare verb: I would rather stay.", size=11, color=SLATE)
```

## 6.3 Degrees of comparison, conjunctions and word order

- Adjectives: tall–taller–tallest; good–better–best; bad–worse–worst; far–farther/further–farthest/furthest. **Of two**, use the comparative (the taller of the two). Never use a double comparative (*more taller*). *The more you practise, the better you become.*
- *Senior, junior, superior, inferior, prefer* take **to**, not *than*.
- Conjunctions: *although/though* (concession; never with *but*), *because* (clause) vs *because of* (noun), *yet/but* (contrast), *so* (result), *for* (reason, formal), *neither … nor*, *not only … but also*, **no sooner … than**, **hardly/scarcely … when**.
- Adverb of *good* is **well**.

```photogrid label="6.2" cols="3" ratio="1.0" caption="Comparison with three real peaks. (a) Mount Everest (8,849 m) is the highest of the three, so we use the superlative. (b) K2 (8,611 m) is higher than Kangchenjunga: the comparative takes than. (c) Kangchenjunga (8,586 m) from the south-east. Of the two, K2 is the higher, because for two things we use the comparative (Fig 6.4)."
@ photo id="bcagk/everest" cap="the highest (superlative)"
focus 0.5 0.5
@ photo id="bcaeng/k2" cap="higher than (comparative)"
focus 0.5 0.5
@ photo id="bcaeng/kangch" cap="the third highest"
focus 0.5 0.5
```

```svgfig label="6.4" caption="Degrees of comparison. Regular adjectives follow three spelling rules (add -er and -est; change y to i; double the last consonant after a short vowel); long adjectives take more and most; a few irregular adjectives must be learned. The cell builds the regular forms by rule and checks them, then checks the mountain heights: Everest is 238 m higher than K2, and K2 is 25 m higher than Kangchenjunga."
def deg(a):
    if a.endswith("y"): return a[:-1] + "ier", a[:-1] + "iest"
    if a in ("big", "hot", "thin"): return a + a[-1] + "er", a + a[-1] + "est"
    return a + "er", a + "est"
assert deg("tall") == ("taller", "tallest") and deg("happy") == ("happier", "happiest") and deg("big") == ("bigger", "biggest")
H = {"Everest": 8849, "K2": 8611, "Kangchenjunga": 8586}
assert H["Everest"] - H["K2"] == 238 and H["K2"] - H["Kangchenjunga"] == 25
assert sorted(H, key=H.get)[-1] == "Everest"
R = [("tall", "taller", "tallest", "add -er / -est"), ("happy", "happier", "happiest", "y becomes i"),
     ("big", "bigger", "biggest", "double the consonant"),
     ("beautiful", "more beautiful", "most beautiful", "long word: more / most"),
     ("good / well", "better", "best", "irregular"), ("bad", "worse", "worst", "irregular"),
     ("far", "farther / further", "farthest / furthest", "irregular (distance / extra)"),
     ("little", "less", "least", "irregular"), ("many / much", "more", "most", "irregular"),
     ("old", "older / elder", "oldest / eldest", "elder / eldest only for family")]
for a, c, s, rule in R[:3]:
    assert (c, s) == deg(a)
assert len(R) == 10
f = Fig(780, 440)
for x, w, h in [(14, 118, "positive"), (136, 170, "comparative"), (310, 170, "superlative"), (484, 282, "rule")]:
    f.box(x, 8, w, 24, h, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
for i, (a, c, s, rule) in enumerate(R):
    y = 36 + i * 28
    irr = i >= 4
    col = AMBER if irr else TEAL
    bg = SAND if irr else MINT
    f.box(14, y, 118, 24, a, fill=bg, stroke=col, color=col, size=11, bold=True)
    f.box(136, y, 170, 24, c, fill=bg, stroke=col, color=SLATE, size=11)
    f.box(310, y, 170, 24, s, fill=bg, stroke=col, color=SLATE, size=11)
    f.box(484, y, 282, 24, rule, fill=SOFT, stroke="#cbd5e1", color=SLATE, size=11, anchor="start")
f.box(14, 326, 752, 100, "", fill=BLUE, stroke=NAVY, r=5)
f.text(28, 346, "Everest 8,849 m  >  K2 8,611 m  >  Kangchenjunga 8,586 m", size=11.5, color=NAVY, anchor="start", bold=True)
f.text(28, 368, "Everest is the highest of the three. K2 is higher than Kangchenjunga (by 25 m).", size=11, color=SLATE, anchor="start")
f.text(28, 388, "Of the two, K2 is the higher.  The higher you climb, the colder it becomes.", size=11, color=SLATE, anchor="start")
f.text(28, 408, "Never: more taller, most tallest. Senior, junior, superior, prefer take to, not than.", size=11, color=RED, anchor="start", bold=True)
```

## 6.4 Spotting and correcting errors

| Wrong | Right |
|---|---|
| He gave me many informations. | He gave me some information. |
| She don't know. | She doesn't know. |
| Me and my friend went. | My friend and I went. |
| He is more taller than me. | He is taller than I am. |
| The number of students are increasing. | The number of students is increasing. |
| Fewer / less confusion | fewer people, less water |

```svgfig label="6.5" caption="Error spotting as a checklist: eight categories cover most find-the-error items. For each, read the sentence for the tell (the clue that gives the error away). The cell runs eight small pattern rules over the wrong sentences and the right ones: every wrong sentence is caught by its own rule and none of the corrected sentences is flagged."
import re
W = ["The number of students are increasing.", "He gave me many informations.", "Me and my friend went home.",
     "He is more taller than me.", "She is senior than me.", "He has gone yesterday.",
     "He studies in an university.", "Although it rained, but we played."]
Rt = ["The number of students is increasing.", "He gave me some information.", "My friend and I went home.",
      "He is taller than I am.", "She is senior to me.", "He went yesterday.",
      "He studies in a university.", "Although it rained, we played."]
rules = [r"\bnumber of \w+ are\b", r"\b(informations|advices|furnitures|luggages)\b", r"^Me and\b",
         r"\b(more|most) \w+(er|est)\b", r"\b(senior|junior|superior|inferior|prefer\w*) than\b",
         r"\b(has|have) \w+ (yesterday|last \w+)\b", r"\ban (university|European|one)\b",
         r"\bAlthough\b.*\bbut\b"]
for w, r_ in zip(W, rules):
    assert re.search(r_, w), (w, r_)
for s in Rt:
    assert not any(re.search(r_, s) for r_ in rules), s
assert len(W) == len(Rt) == len(rules) == 8
T = [("1  Agreement", "the NUMBER of ... is"), ("2  Uncountable plural", "information, advice, furniture"),
     ("3  Pronoun case", "other person first, then I"), ("4  Double comparison", "-er or more, never both"),
     ("5  to or than", "senior / junior / prefer + to"), ("6  Tense and time word", "yesterday needs past simple"),
     ("7  Article by sound", "a university (y-sound)"), ("8  Paired words", "although, no but")]
f = Fig(780, 400)
for i in range(8):
    col, row = i % 2, i // 2
    x, y = 14 + col * 380, 8 + row * 96
    f.box(x, y, 372, 88, "", fill=SOFT, stroke="#94a3b8", r=5)
    f.text(x + 10, y + 16, T[i][0], size=11.5, color=NAVY, anchor="start", bold=True)
    f.text(x + 10, y + 36, "X  " + W[i], size=10.5, color=RED, anchor="start")
    f.text(x + 10, y + 55, "OK  " + Rt[i], size=10.5, color=TEAL, anchor="start", bold=True)
    f.text(x + 10, y + 75, "tell: " + T[i][1], size=10.5, color=SLATE, anchor="start", italic=True)
```

## 6.5 Eight traps in pronouns, modals, comparison and error spotting

Each trap below is a rule that students half remember, so the paper can turn it into a wrong option.

1. **Its has no apostrophe.** The dog wagged *its* tail; *it's* means *it is* (Fig 6.1). The same holds for *hers*, *ours*, *yours* and *theirs*. A reflexive never takes *hisself* or *theirselves*: use *himself* and *themselves*.
2. **Few and little are negative; a few and a little are positive.** "He has little money" says he is almost broke; "He has a little money" says he can manage (Fig 6.2). The words *few/fewer* go with countable nouns and *little/less/much* with uncountable ones.
3. **Fewer for numbers, less for amounts.** Write *fewer people* but *less water*. A shop sign that says "ten items or less" is common, yet the exam expects *fewer items*. Measures of time, money and distance are treated as one amount: *less than ten minutes*.
4. **Mustn't forbids; needn't does not require.** "You mustn't smoke here" is a ban; "You needn't pay now" means you may pay later (Fig 6.3). *Don't have to* has the same meaning as *needn't*. Never use *must not* for lack of need.
5. **Choose the modal by the time and the feeling.** *Must have lost* is a sure guess about the past; *can't have left* is a sure negative guess; *should have told* is criticism of something that did not happen (Fig 6.3). Use the past participle (V3) after *have*, never the base form.
6. **Two things take the comparative; three or more take the superlative.** "K2 is the higher of the two" but "Everest is the highest of the three" (Fig 6.4). Never double a comparison: *more taller* and *most tallest* are wrong. *Senior, junior, superior* and *prefer* take *to*, not *than*.
7. **Do not pair although with but.** "Although it rained, we played" is correct, and *but* is added only in "It rained, but we played" (Fig 6.5). Remember the fixed pairs: *no sooner ... than*, *hardly ... when*, *neither ... nor*, *not only ... but also*.
8. **Check the pronoun case.** After a preposition use the object form: *between you and me*. After *than* the subject form is formal: *taller than I (am)*. With a compound subject put the other person first: *My friend and I went*. *Each, either, neither* take a singular verb, *both* a plural verb.

### 6.5.1 Worked checks

**Q. Fill in the blank: "Two ladies had ____ handbags stolen." (its / their / her)**

**Answer.** *Ladies* is plural, so the possessive adjective is **their** (Fig 6.1).

**Q. Choose the correct preposition: "He is senior ____ me." (than / to / from)**

**Answer.** *Senior* is followed by **to**: "He is senior to me" (Fig 6.4).

**Q. Complete: "I cannot find my keys. I ____ have lost them." (can / must / need)**

**Answer.** This is a strong guess about the past, so the answer is **must**: "I must have lost them" (Fig 6.3).

**Q. Correct the sentence: "He gave me many informations."**

**Answer.** *Information* is uncountable and has no plural, so the sentence becomes "He gave me **some information**" (Figs 6.2 and 6.5).


## Formula and fact sheet

| Item | Rule |
|---|---|
| few / a few | negative / positive |
| fewer / less | countable / uncountable |
| senior, junior, prefer | + to |
| no sooner … than; hardly … when | past perfect after the first part |

## Chapter summary

- *Its* is possessive, *it's* is "it is".
- *A few* is positive, *few* is almost none.
- *Mustn't* forbids; *needn't* does not require.
- Do not combine *although* with *but*.
- Information, advice and furniture never take *-s*.

## Practice questions

**Set A — Recall (20 questions)**

1. Two ladies had ___ handbags stolen.
   (a) its (b) their (c) her (d) they
2. He hurt ___ while playing.
   (a) him (b) his (c) itself (d) himself
3. She is taller ___ her sister.
   (a) than (b) from (c) to (d) as
4. This is the ___ book I have read.
   (a) good (b) better (c) best (d) well
5. He has ___ money left; he is almost broke.
   (a) a little (b) little (c) few (d) a few
6. There are ___ students in the library, so we can sit.
   (a) little (b) much (c) a little (d) a few
7. You ___ smoke here; it is prohibited.
   (a) needn't (b) don't have to (c) mustn't (d) may
8. You look ill. You ___ see a doctor.
   (a) should (b) can't (c) mustn't (d) dare
9. The party was cancelled ___ the rain.
   (a) because (b) although (c) despite (d) because of
10. ___ he was tired, he kept working.
    (a) Because (b) Although (c) Unless (d) So
11. No sooner had he arrived ___ it began to rain.
    (a) when (b) then (c) than (d) that
12. Hardly had she left ___ the phone rang.
    (a) when (b) than (c) then (d) as
13. Neither Ram ___ Hari came.
    (a) or (b) nor (c) and (d) but
14. He is the ___ of the two brothers.
    (a) tall (b) tallest (c) more tall (d) taller
15. Choose the correct sentence.
    (a) He gave me an information. (b) He gave me many informations. (c) He gave me some information. (d) He gave me informations.
16. ___ the roads lead to Pokhara.
    (a) Both (b) Either (c) Neither (d) Each
17. I would rather ___ at home.
    (a) to stay (b) staying (c) stayed (d) stay
18. She sings ___.
    (a) good (b) well (c) goodly (d) best
19. Each of the boys has done ___ homework.
    (a) their (b) its (c) his (d) our
20. The dog wagged ___ tail.
    (a) its (b) it's (c) their (d) his

::: note Answers and explanations — Set A
**1.** (b) — "ladies" is plural, so their.
**2.** (d) — a reflexive pronoun for the same person.
**3.** (a) — comparative + than.
**4.** (c) — superlative after "the".
**5.** (b) — "little" = hardly any; "almost broke" is negative.
**6.** (d) — "a few" = some, a positive sense.
**7.** (c) — prohibition.
**8.** (a) — advice.
**9.** (d) — "because of" before a noun.
**10.** (b) — concession.
**11.** (c) — no sooner … than.
**12.** (a) — hardly … when.
**13.** (b) — neither … nor.
**14.** (d) — comparative for two.
**15.** (c) — information is uncountable.
**16.** (a) — "both" with a plural verb.
**17.** (d) — would rather + bare verb.
**18.** (b) — the adverb of good is well.
**19.** (c) — "each" is singular and boys are male.
**20.** (a) — possessive "its" has no apostrophe.
:::

**Set B — Understanding (12 questions)**

1. I will go for a walk ___ it rains.
   (a) if (b) because (c) unless (d) until
2. He is junior ___ me.
   (a) to (b) than (c) from (d) of
3. My brother is ___ than I.
   (a) oldest (b) more old (c) elder (d) older
4. Choose the correct sentence.
   (a) He is more taller than me. (b) He is taller than I am. (c) He is most tall. (d) He taller.
5. You ___ pay now; you can pay later.
   (a) mustn't (b) shouldn't (c) needn't (d) can't
6. She ___ speak four languages.
   (a) can (b) must (c) need (d) ought
7. Choose the incorrect sentence.
   (a) He gave me good advice. (b) She is wiser than I. (c) We need some furniture. (d) He gave me many advices.
8. Choose the correct sentence.
   (a) Me and my friend went to the market. (b) My friend and I went to the market. (c) Me and I went to the market. (d) Myself and friend went to the market.
9. Not only the boy ___ also the girl was late.
   (a) but (b) and (c) or (d) nor
10. She is ___ intelligent than her sister.
    (a) most (b) much (c) more (d) very
11. He worked hard ___ he failed.
    (a) so (b) because (c) therefore (d) yet
12. There are ___ people in the hall than yesterday.
    (a) less (b) fewer (c) little (d) lesser

::: note Answers and explanations — Set B
**1.** (c) — "unless it rains" = if it does not rain.
**2.** (a) — junior to.
**3.** (d) — "than" needs the comparative older.
**4.** (b) — no double comparative.
**5.** (c) — no obligation.
**6.** (a) — ability.
**7.** (d) — advice is uncountable.
**8.** (b) — the subject form "I", with the other person first.
**9.** (a) — not only … but also.
**10.** (c) — comparative with a long adjective.
**11.** (d) — yet marks a contrast.
**12.** (b) — fewer with countable people.
:::

**Set C — Application (8 questions)**

1. The more you practise, ___ you become.
   (a) better (b) more better (c) best (d) the better
2. I would rather you ___ here.
   (a) stayed (b) stay (c) will stay (d) staying
3. He ran fast ___ he missed the bus.
   (a) so (b) because (c) but (d) therefore
4. Choose the correct sentence.
   (a) She is senior than me. (b) She is senior to me. (c) She is more senior than me. (d) She is senior from me.
5. Scarcely had he reached the station ___ the train left.
   (a) than (b) then (c) that (d) when
6. You ___ have told me earlier! (criticism)
   (a) should (b) must (c) will (d) would
7. I can't find my keys. I ___ have lost them.
   (a) can (b) need (c) must (d) shall
8. The superlative of "bad" is
   (a) badder (b) worst (c) worse (d) most bad

::: note Answers and explanations — Set C
**1.** (d) — the + comparative … the + comparative.
**2.** (a) — "would rather" + subject takes the past.
**3.** (c) — contrast: but.
**4.** (b) — senior to.
**5.** (d) — scarcely … when.
**6.** (a) — "should have told" criticises a past omission.
**7.** (c) — "must have lost" is a strong deduction.
**8.** (b) — bad, worse, worst.
:::
