---
subject: English
grade: BCA
unit: 4
title: Voice, Narration and Question Tags
hours: 5
area: Grammar
---

Voice, reported speech and question tags are all rule-driven, so every question here can be answered correctly with the rules below. The Dean's Office model asks the passive of "We celebrate Democracy Day on Falgun seven" and the tag for "Let us go". Five questions in the paper come from this unit.

::: key What the paper asks from this chapter
- **Passive voice**: object becomes subject, *be* in the tense of the active verb + past participle.
- **Reported speech**: back-shift the tense, change pronouns and time words, use *if/whether* for yes/no questions.
- **Question tags**: opposite polarity; special cases (*I am* → aren't I; *Let us* → shall we; imperative → will you).
:::

## 4.1 Active and passive voice

| Tense | Active | Passive |
|---|---|---|
| Simple present | She writes a letter. | A letter is written by her. |
| Present continuous | They are building a bridge. | A bridge is being built by them. |
| Present perfect | He has finished the work. | The work has been finished by him. |
| Simple past | The boy broke the window. | The window was broken by the boy. |
| Past perfect | He had done it. | It had been done by him. |
| Simple future | They will complete it. | It will be completed by them. |
| Modal | You must obey the rules. | The rules must be obeyed. |

Imperatives: *Open the door* → *Let the door be opened.* Questions: *Who wrote this book?* → *By whom was this book written?* Intransitive verbs have no passive.

```photogrid label="4.1" cols="3" ratio="1.0" caption="Voice depends on who or what we want to put first. (a) The Taj Mahal: The Taj Mahal was built by Shah Jahan puts the building first, because the building is the topic. (b) Tenzing Norgay, who with Edmund Hillary first climbed Everest in 1953: Everest was first climbed by Tenzing and Hillary is the passive. (c) A telephone: reported speech tells what someone said on the phone without quoting the exact words (Fig 4.2)."
@ photo id="bcaeng/taj" cap="Passive: built by Shah Jahan"
focus 0.5 0.5
@ photo id="bcagk/tenzing" cap="Everest was climbed in 1953"
focus 0.5 0.3
@ photo id="bca105/phone" cap="Reported speech: what was said"
focus 0.5 0.5
```

```svgfig label="4.1" caption="Active to passive by swapping. The object of the active sentence becomes the subject, the verb becomes be + past participle (V3) in the same tense, and the old subject goes after by. The table builds each passive from its parts in the cell (object + be-form + V3 + by-phrase) and asserts that it equals the sentence in the book, from simple present to the modal must."
rows = [("Simple present", "She writes a letter.", "a letter", "is written", "her"), ("Present continuous", "They are building a bridge.", "a bridge", "is being built", "them"),
        ("Present perfect", "He has finished the work.", "the work", "has been finished", "him"), ("Simple past", "The boy broke the window.", "the window", "was broken", "the boy"),
        ("Past perfect", "He had done it.", "it", "had been done", "him"), ("Simple future", "They will complete it.", "it", "will be completed", "them"),
        ("Modal", "You must obey the rules.", "the rules", "must be obeyed", None)]
exp = ["A letter is written by her.", "A bridge is being built by them.", "The work has been finished by him.", "The window was broken by the boy.", "It had been done by him.", "It will be completed by them.", "The rules must be obeyed."]
def make(o, aux, by):
    s = o[0].upper() + o[1:] + " " + aux
    return s + (" by " + by if by else "") + "."
assert [make(r[2], r[3], r[4]) for r in rows] == exp
f = Fig(780, 340)
for k, (x, w, t, c) in enumerate([(20, 110, "She", NAVY), (140, 110, "writes", TEAL), (260, 130, "a letter", RED)]):
    f.box(x, 24, w, 28, t, fill=BLUE, stroke=c, color=c, size=11.5, bold=True)
for k, (x, w, t, c) in enumerate([(430, 130, "A letter", RED), (570, 120, "is written", TEAL), (700, 70, "by her", NAVY)]):
    f.box(x, 24, w, 28, t, fill=MINT, stroke=c, color=c, size=11.5, bold=True)
f.arrow([(325, 52), (325, 70), (495, 70), (495, 54)], color=RED); f.arrow([(75, 52), (75, 84), (735, 84), (735, 54)], color=NAVY)
f.text(210, 18, "ACTIVE", size=10.5, color=SLATE, bold=True); f.text(600, 18, "PASSIVE", size=10.5, color=SLATE, bold=True)
f.text(410, 104, "object moves to the front; verb = be + V3; subject goes after by", size=10.5, color=RED, bold=True)
for j, (hd, x, w) in enumerate([("tense", 14, 140), ("active", 158, 260), ("passive (built in the cell)", 422, 340)]):
    f.box(x, 118, w, 24, hd, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
for i, r in enumerate(rows):
    y = 146 + i * 27
    f.box(14, y, 140, 25, r[0], fill=SOFT, stroke="#cbd5e1", color=SLATE, size=10.5, bold=True)
    f.box(158, y, 260, 25, r[1], fill=SOFT, stroke="#cbd5e1", color=SLATE, size=10.5)
    f.box(422, y, 340, 25, make(r[2], r[3], r[4]), fill=MINT, stroke=TEAL, color=TEAL, size=10.5, bold=True)
```

## 4.2 Reported speech

- **Back-shift**: simple present → simple past; present continuous → past continuous; present perfect → past perfect; simple past → past perfect; *will* → *would*; *can* → *could*. A **universal truth** does not shift (The teacher said that the earth moves round the sun).
- **Words**: now → then; today → that day; tomorrow → the next day; yesterday → the day before; here → there; this → that.
- **Statements** use *said/told that*; **yes–no questions** use *asked + if/whether* with normal word order (She asked whether he would help her); **wh-questions** keep the wh-word (He asked where I was going); **commands** use *told/ordered + to*; **exclamations** use *exclaimed with joy/sorrow that*.

```svgfig label="4.2" caption="Reported speech steps one tense back. The cell moves each pronoun, verb and time word with a small dictionary and checks the results: I am happy now becomes he was happy then; I will come tomorrow becomes he would come the next day; I can swim here becomes he could swim there. A universal truth does not shift: the teacher said that the earth moves round the sun."
mp = {"I": "he", "am": "was", "will": "would", "can": "could", "now": "then", "tomorrow": "the next day", "here": "there", "yesterday": "the day before", "today": "that day"}
def rep(s): return " ".join(mp.get(w, w) for w in s.split())
ex = [("I am happy now", "he was happy then"), ("I will come tomorrow", "he would come the next day"), ("I can swim here", "he could swim there")]
assert all(rep(a) == b for a, b in ex)
f = Fig(780, 340)
f.text(190, 20, "Verbs step back one tense", size=11.5, color=NAVY, bold=True)
pairs = [("simple present", "simple past"), ("present continuous", "past continuous"), ("present perfect", "past perfect"), ("simple past", "past perfect"), ("will", "would"), ("can", "could")]
for i, (a, b) in enumerate(pairs):
    y = 34 + i * 38
    f.box(14, y, 150, 28, a, fill=BLUE, stroke=NAVY, color=NAVY, size=10.5, bold=True); f.arrow([(166, y + 14), (214, y + 14)], color=RED)
    f.box(216, y, 150, 28, b, fill=SAND, stroke=AMBER, color=AMBER, size=10.5, bold=True)
f.text(590, 20, "Words change too", size=11.5, color=NAVY, bold=True)
words = [("now", "then"), ("today", "that day"), ("tomorrow", "the next day"), ("yesterday", "the day before"), ("here", "there"), ("this", "that")]
for i, (a, b) in enumerate(words):
    y = 34 + i * 26
    f.box(420, y, 130, 22, a, fill=SOFT, stroke="#cbd5e1", color=SLATE, size=10.5, bold=True); f.text(566, y + 15, "to", size=10.5, color=RED, bold=True)
    f.box(588, y, 170, 22, b, fill=MINT, stroke=TEAL, color=TEAL, size=10.5, bold=True)
for i, (a, b) in enumerate(ex):
    f.text(20, 280 + i * 18, 'He said, "' + a + '"  =  He said that ' + b, size=10.5, color=SLATE, anchor="start", bold=(i == 0))
f.text(420, 232, "no back-shift for a universal truth:", size=10.5, color=RED, anchor="start", bold=True)
f.text(420, 252, "the teacher said that the earth moves round the sun", size=10.5, color=SLATE, anchor="start")
f.text(420, 290, "statement: said that;  yes/no: asked if or whether", size=10.5, color=NAVY, anchor="start", bold=True)
f.text(420, 310, "command: told + to;  wh-question keeps the wh-word", size=10.5, color=NAVY, anchor="start", bold=True)
```

## 4.3 Question tags

- Positive statement → negative tag; negative → positive. The tag repeats the auxiliary (none → *do/does/did*).
- Special: *I am* → **aren't I?**; *Let us / Let's* → **shall we?**; imperatives → **will you?**; *there is* → **isn't there?**; *nobody, everyone, someone* → **they**; *used to* → **didn't**; *had better* → **hadn't**; *ought to* → **oughtn't**.
- Negative-meaning words (*never, hardly, seldom, rarely, nobody, neither*) make the statement negative, so the tag is **positive**: He never lies, does he?

```svgfig label="4.3" caption="Question tags flip the polarity. A positive statement takes a negative tag and a negative statement takes a positive tag; the tag repeats the auxiliary and uses a pronoun. The cell builds the regular tags (is to isn't she, plays to doesn't he, went to didn't you) and checks them, then lists the special ones: I am takes aren't I, let's takes shall we, a command takes will you, and a negative word such as never or nobody makes the statement negative, so the tag is positive."
CON = {"is": "isn't", "are": "aren't", "was": "wasn't", "has": "hasn't", "have": "haven't", "does": "doesn't", "do": "don't", "did": "didn't", "will": "won't", "can": "can't"}
INV = {v: k for k, v in CON.items()}
def tag(pron, aux, neg):
    return ("%s %s?" % (INV[aux] if neg else CON[aux], pron))
assert tag("she", "is", False) == "isn't she?" and tag("they", "don't", True) == "do they?" and tag("he", "does", False) == "doesn't he?" and tag("you", "did", False) == "didn't you?"
rows = [("She is clever,", tag("she", "is", False), "positive, negative tag"), ("They don't play,", tag("they", "don't", True), "negative, positive tag"), ("He plays cricket,", tag("he", "does", False), "no auxiliary: use does"),
        ("You went to Pokhara,", tag("you", "did", False), "past: didn't"), ("He never lies,", "does he?", "never is negative"), ("Nobody came,", "did they?", "nobody: negative, they"),
        ("I am late,", "aren't I?", "special"), ("Let's go,", "shall we?", "special"), ("Open the door,", "will you?", "command")]
f = Fig(780, 330)
for hd, x, w in [("statement", 14, 260), ("tag", 278, 200), ("why", 482, 280)]:
    f.box(x, 8, w, 24, hd, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
for i, (a, b, c) in enumerate(rows):
    y = 36 + i * 31
    sp = i >= 4
    f.box(14, y, 260, 27, a, fill=SOFT, stroke="#cbd5e1", color=SLATE, size=10.5, bold=True)
    f.box(278, y, 200, 27, b, fill=(SAND if sp else MINT), stroke=(AMBER if sp else TEAL), color=(AMBER if sp else TEAL), size=11, bold=True)
    f.box(482, y, 280, 27, c, fill=SOFT, stroke="#cbd5e1", color=SLATE, size=10.5)
```

## 4.4 Eight traps in voice, narration and tags

These topics are rule-based, so a careful check of each step removes almost every error. The eight traps below are the ones that appear most often as wrong options.

1. **Keep the tense when you change the voice.** *She writes a letter* becomes *A letter is written by her*, still present simple (Fig 4.1). Use *be* in the same tense plus the past participle. Changing the tense is the most common error.
2. **Change the pronoun form.** *He* becomes *by him*, *they* becomes *by them* and *I* becomes *by me*. The subject of the passive is the old object, so *me* becomes *I*. Check every pronoun when you swap.
3. **Intransitive verbs have no passive.** *He sleeps* and *The sun rises* have no object, so no passive can be formed. The verbs *arrive*, *go* and *seem* are in the same group. If there is no object, the option with a passive is wrong.
4. **Present continuous and perfect need *being* and *been*.** *They are building a bridge* becomes *A bridge is being built*, and *He has finished the work* becomes *The work has been finished* (Fig 4.1). A modal keeps *be*: *must be obeyed*. Students often drop *being* or *been*.
5. **Back-shift one tense in reported speech.** Direct *I am happy* becomes *he was happy*, *will* becomes *would* and *can* becomes *could* (Fig 4.2). If the reporting verb is present (*He says*), no shift is needed. A universal truth also stays in the present: *He said that the earth moves round the sun*.
6. **Change the time and place words.** *Now* becomes *then*, *today* becomes *that day*, *tomorrow* becomes *the next day*, *here* becomes *there* and *this* becomes *that*. The change depends on the moment of reporting. Do not forget to change the pronoun also.
7. **Questions become statements in reported speech.** A yes-no question uses *asked if/whether* and normal order: *She asked whether he would help her*. A wh-question keeps the wh-word: *He asked where I was going*. Remove the question mark and the auxiliary inversion.
8. **The tag flips the polarity.** A positive statement has a negative tag and a negative statement has a positive tag (Fig 4.3). Remember *I am* → *aren't I?*, *Let's* → *shall we?*, commands → *will you?*, and *nobody* or *never* give a positive tag. The tag pronoun for *everyone* and *nobody* is *they*.

### 4.4.1 Worked checks

**Q. Change into the passive: "They are building a bridge."**

**Answer.** The tense is present continuous, so the passive is **A bridge is being built by them** (Fig 4.1).

**Q. Change into indirect speech: He said, "I will come tomorrow."**

**Answer.** *I* becomes *he*, *will* becomes *would* and *tomorrow* becomes *the next day*. The result is **He said that he would come the next day** (Fig 4.2).

**Q. Add a question tag: "Nobody came, ____?"**

**Answer.** *Nobody* has a negative meaning, so the tag is positive and uses *they*: "Nobody came, **did they**?" (Fig 4.3).

**Q. Add a question tag: "I am late, ____?"**

**Answer.** The special form is **aren't I?** (Fig 4.3).

## Formula and fact sheet

| Item | Rule |
|---|---|
| Passive | *be* (in the active tense) + past participle |
| said → | told + object; asked + if/whether |
| Tag polarity | opposite; hardly/never → positive tag |
| Tag exceptions | aren't I; shall we; will you |

## Chapter summary

- Passive: keep the tense of *be*, use the third form of the main verb.
- Questions in reported speech lose the question word order.
- Do not back-shift a universal truth.
- Tags are the opposite of the statement's polarity.
- *Hardly, never, nobody* count as negatives.

## Practice questions

**Set A — Recall (20 questions)**

1. The passive of "She writes a letter" is
   (a) A letter wrote by her. (b) A letter is written by her. (c) A letter was written by her. (d) A letter is being written by her.
2. The passive of "They are building a bridge" is
   (a) A bridge is built by them. (b) A bridge was built by them. (c) A bridge has been built by them. (d) A bridge is being built by them.
3. The passive of "He has finished the work" is
   (a) The work has been finished by him. (b) The work was finished by him. (c) The work is finished by him. (d) The work had been finished by him.
4. Let us go, ___
   (a) will we? (b) do we? (c) shall we? (d) don't we?
5. She is a teacher, ___
   (a) is she? (b) isn't she? (c) doesn't she? (d) wasn't she?
6. You can swim, ___
   (a) don't you? (b) can you? (c) won't you? (d) can't you?
7. "He said, 'I am happy.'" becomes: He said that
   (a) he is happy. (b) I was happy. (c) he was happy. (d) he has been happy.
8. He never lies, ___
   (a) does he? (b) doesn't he? (c) is he? (d) did he?
9. I am late, ___
   (a) am I not? (b) isn't I? (c) amn't I? (d) aren't I?
10. "He said, 'I will come tomorrow.'" becomes: He said that
    (a) he will come tomorrow. (b) he would come the next day. (c) he would come tomorrow. (d) he will come the next day.
11. The passive of "Open the door." is
    (a) The door opened. (b) Let the door open. (c) Let the door be opened. (d) The door is opened.
12. Nobody called, ___
    (a) did they? (b) didn't they? (c) did he? (d) didn't he?
13. "She said, 'I live in Pokhara.'" becomes: She said that she
    (a) lives in Pokhara. (b) lived in Pokhara. (c) had lived in Pokhara. (d) was living in Pokhara.
14. Open the window, ___
    (a) shall we? (b) don't you? (c) will you? (d) won't we?
15. The passive of "Who wrote this book?" is
    (a) Who was this book written? (b) By who this book was written? (c) By whom is this book written? (d) By whom was this book written?
16. "He said, 'I have finished.'" becomes: He said that he
    (a) had finished. (b) has finished. (c) finished. (d) have finished.
17. There is a problem, ___
    (a) is there? (b) isn't there? (c) isn't it? (d) doesn't there?
18. "She asked, 'Where do you live?'" becomes: She asked me where I
    (a) live. (b) do live. (c) am living. (d) lived.
19. The passive of "People speak English all over the world." is
    (a) English was spoken all over the world. (b) English speaks all over the world. (c) English is spoken all over the world. (d) English has spoken all over the world.
20. "He said to me, 'Close the door.'" becomes: He ___ me to close the door.
    (a) told (b) said (c) asked to (d) ordered at

::: note Answers and explanations — Set A
**1.** (b) — simple present passive: is written.
**2.** (d) — present continuous passive: is being built.
**3.** (a) — present perfect passive: has been finished.
**4.** (c) — "Let us" takes "shall we".
**5.** (b) — positive statement, negative tag with "is".
**6.** (d) — repeat the modal: can't you.
**7.** (c) — am → was.
**8.** (a) — "never" is negative, so a positive tag.
**9.** (d) — "I am" takes "aren't I".
**10.** (b) — will → would; tomorrow → the next day.
**11.** (c) — the imperative passive uses "Let … be …".
**12.** (a) — "nobody" is negative and takes "they".
**13.** (b) — simple present shifts to simple past.
**14.** (c) — imperatives take "will you".
**15.** (d) — "By whom was this book written?"
**16.** (a) — present perfect shifts to past perfect.
**17.** (b) — "there is" takes "isn't there".
**18.** (d) — normal order and back-shift: where I lived.
**19.** (c) — is spoken, simple present passive.
**20.** (a) — said to + command becomes told + to.
:::

**Set B — Understanding (12 questions)**

1. He hardly works, ___
   (a) doesn't he? (b) is he? (c) does he? (d) hasn't he?
2. The teacher said, "The earth moves round the sun." The teacher said that the earth
   (a) moves round the sun. (b) moved round the sun. (c) had moved round the sun. (d) was moving round the sun.
3. The passive of "The boy broke the window" is
   (a) The window is broken by the boy. (b) The window has been broken by the boy. (c) The window broke the boy. (d) The window was broken by the boy.
4. "He said, 'I am reading a book.'" becomes: He said that he
   (a) is reading a book. (b) was reading a book. (c) had read a book. (d) read a book.
5. Everyone came, ___
   (a) didn't he? (b) did they? (c) didn't they? (d) wasn't they?
6. "She said to him, 'Will you help me?'" becomes: She asked him
   (a) whether he would help her. (b) that he would help her. (c) if will he help her. (d) would he help her.
7. The passive of "They will complete the project" is
   (a) The project is completed by them. (b) The project will complete by them. (c) The project would be completed. (d) The project will be completed by them.
8. She used to live here, ___
   (a) wasn't she? (b) didn't she? (c) did she? (d) doesn't she?
9. "He said, 'I saw her yesterday.'" becomes: He said that he had seen her
   (a) the day before. (b) yesterday. (c) the next day. (d) that day.
10. The passive of "Someone has stolen my bag" is
    (a) My bag was stolen. (b) My bag is stolen. (c) My bag has been stolen. (d) My bag had been stolen.
11. "He said, 'I can swim.'" becomes: He said that he
    (a) can swim. (b) will swim. (c) would swim. (d) could swim.
12. You had better go, ___
    (a) didn't you? (b) hadn't you? (c) wouldn't you? (d) shouldn't you?

::: note Answers and explanations — Set B
**1.** (c) — "hardly" is negative, so the tag is positive.
**2.** (a) — a universal truth keeps the present tense.
**3.** (d) — simple past passive.
**4.** (b) — present continuous becomes past continuous.
**5.** (c) — "everyone" takes "they".
**6.** (a) — a yes/no question uses whether and statement order.
**7.** (d) — will be + past participle.
**8.** (b) — "used to" takes "didn't".
**9.** (a) — yesterday becomes the day before.
**10.** (c) — present perfect passive.
**11.** (d) — can becomes could.
**12.** (b) — "had better" takes "hadn't".
:::

**Set C — Application (8 questions)**

1. "She said, 'I am going tomorrow.'" becomes: She said that she was going
   (a) tomorrow. (b) today. (c) yesterday. (d) the next day.
2. The passive of "Who has broken the glass?" is
   (a) By whom has the glass been broken? (b) Who was the glass broken by? (c) By whom had the glass broken? (d) By who has the glass broken?
3. "He said, 'Where are you going?'" becomes: He asked me where
   (a) was I going. (b) am I going. (c) I was going. (d) I am going.
4. Mother said, "Do not play in the sun." Indirect speech:
   (a) Mother said me not play in the sun. (b) Mother told me not to play in the sun. (c) Mother told me do not play. (d) Mother said that I not to play.
5. Neither of them came, ___
   (a) didn't they? (b) did he? (c) didn't he? (d) did they?
6. The passive of "The chef is cooking dinner" is
   (a) Dinner is being cooked by the chef. (b) Dinner was cooked by the chef. (c) Dinner is cooked by the chef. (d) Dinner has been cooked by the chef.
7. "He said, 'Alas! I am ruined.'" becomes: He exclaimed with sorrow that he
   (a) is ruined. (b) were ruined. (c) was ruined. (d) had ruined.
8. He ought to go, ___
   (a) isn't he? (b) oughtn't he? (c) doesn't he? (d) shouldn't he?

::: note Answers and explanations — Set C
**1.** (d) — tomorrow becomes the next day.
**2.** (a) — present perfect passive in a question.
**3.** (c) — statement word order and back-shift.
**4.** (b) — a negative command: told + not to.
**5.** (d) — "neither" is negative, so a positive tag with "they".
**6.** (a) — present continuous passive.
**7.** (c) — exclamation with back-shift.
**8.** (b) — repeat "ought" with n't.
:::
