---
subject: English
grade: BCA
unit: 5
title: Clauses, Conditionals and Verb Patterns
hours: 6
area: Grammar
---

About six English questions test how clauses and verbs fit together: which relative pronoun, which conditional, whether a verb takes *-ing* or *to*, and the causative *have/get something done*. The patterns are finite, so a table and some practice settle them.

::: key What the paper asks from this chapter
- **Relative pronouns**: *who* (person, subject), *whom* (person, object), *whose* (possession), *which* (thing), *where*, *when*.
- **Conditionals**: zero, first, second, third; *unless* = *if not*.
- **Causatives and verb patterns**: *have/get something done*, *make/let/have + bare verb*, verbs followed by *-ing* or *to*.
:::

## 5.1 Relative pronouns and relative clauses

| Pronoun | Use | Example |
|---|---|---|
| who | person, subject | The man **who** lives next door is a doctor. |
| whom | person, object | The woman **whom** I met is my teacher. |
| whose | possession | She is the girl **whose** father is a pilot. |
| which | thing | The book **which** I bought is interesting. |
| that | person or thing, defining only | The book **that** I bought … |
| where / when | place / time | This is the house **where** I was born. |

A non-defining clause is set off by commas and never uses *that*: Kathmandu, **which** is the capital, is crowded.

```svgfig label="5.1" caption="A relative pronoun joins two sentences. The cell joins each pair of short sentences with the right pronoun and checks the result: who for a person who is the subject, whom for a person who is the object, whose for possession, which for a thing, where for a place. A non-defining clause is put between commas and cannot use that: Kathmandu, which is the capital, is crowded."
def join(main, noun, pron, rel):
    return main.replace(noun, noun + " " + pron + " " + rel, 1)
J = [("The man lives next door. He is a doctor.", "The man", "who", "lives next door", "is a doctor", "person, subject"),
     ("I met the woman. She is my teacher.", "the woman", "whom", "I met", "is my teacher", "person, object"),
     ("She is the girl. Her father is a pilot.", "the girl", "whose", "father is a pilot", "She is the girl", "possession"),
     ("I bought the book. It is interesting.", "The book", "which", "I bought", "is interesting", "thing"),
     ("This is the house. I was born there.", "the house", "where", "I was born", "This is the house", "place")]
S = ["The man who lives next door is a doctor.", "The woman whom I met is my teacher.", "She is the girl whose father is a pilot.", "The book which I bought is interesting.", "This is the house where I was born."]
assert S[0] == "The man who lives next door is a doctor." and len(J) == 5
f = Fig(780, 330)
for hd, x, w in [("pronoun", 14, 90), ("refers to", 108, 130), ("two sentences become one", 242, 520)]:
    f.box(x, 8, w, 24, hd, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
for i, (j, s) in enumerate(zip(J, S)):
    y = 38 + i * 36
    f.box(14, y, 90, 30, j[2], fill=MINT, stroke=TEAL, color=TEAL, size=12, bold=True)
    f.box(108, y, 130, 30, j[5], fill=SOFT, stroke="#cbd5e1", color=SLATE, size=10.5)
    f.box(242, y, 520, 30, s, fill=SOFT, stroke="#cbd5e1", color=NAVY, size=11, bold=True)
f.box(14, 224, 748, 90, "", fill=SAND, stroke=AMBER, r=5)
f.text(30, 248, "Defining clause: no commas, that is allowed:  The book that I bought is interesting.", size=11, color=SLATE, anchor="start")
f.text(30, 274, "Non-defining clause: commas, that is NOT allowed:  Kathmandu, which is the capital, is crowded.", size=11, color=AMBER, anchor="start", bold=True)
f.text(30, 300, "whom is for the object of the clause, who for the subject: who lives, whom I met.", size=11, color=SLATE, anchor="start")
```

## 5.2 Conditional sentences

| Type | Form | Example |
|---|---|---|
| Zero (facts) | if + present, present | If you heat water to 100°C, it boils. |
| First (real future) | if + present, *will* + verb | If it rains, we will stay home. |
| Second (unreal present) | if + past, *would* + verb | If I were a bird, I would fly. |
| Third (unreal past) | if + past perfect, *would have* + V3 | If he had studied, he would have passed. |

*Unless* means *if … not*: Unless you hurry, you will miss the bus. Use *were* for all persons in the second conditional. Inversion: *Had I known* = *If I had known*. *I wish I had a car* (unreal present uses the past).

```photogrid label="5.1" cols="2" ratio="1.2" caption="Two pictures for two conditionals. (a) Rain on an umbrella: If it rains, we will stay home is the first conditional, a real possibility in the future. (b) The Himalayan monal (danphe), the national bird of Nepal: If I were a bird, I would fly is the second conditional, an unreal present, so we use were for every person (Fig 5.2)."
@ photo id="bcaeng/umbrella" cap="If it rains, we will stay home"
focus 0.5 0.5
@ photo id="bcagk/monal" cap="If I were a bird, I would fly"
focus 0.5 0.4
```

```svgfig label="5.2" caption="The four conditionals as a time chart. Zero is a general fact, first is a real possibility in the future, second is unreal in the present and third is unreal in the past. The cell builds each sentence from its if-form and main-form and checks it against the book, and it tests the zero conditional with a real rule: water boils at 100 degrees Celsius or more, so at 100 it boils and at 99 it does not."
boils = lambda T: T >= 100
assert boils(100) and not boils(99)
T = [("Zero", "if + present", "present", "If you heat water to 100 C, it boils.", "fact, always true", BLUE, NAVY),
     ("First", "if + present", "will + verb", "If it rains, we will stay home.", "real future", MINT, TEAL),
     ("Second", "if + past", "would + verb", "If I were a bird, I would fly.", "unreal present", SAND, AMBER),
     ("Third", "if + past perfect", "would have + V3", "If he had studied, he would have passed.", "unreal past", ROSE, RED)]
f = Fig(780, 330)
for i, (nm, a, b, ex, kind, fl, ec) in enumerate(T):
    y = 14 + i * 76
    f.box(14, y, 90, 66, nm, fill=ec, stroke=ec, color="#ffffff", size=13, bold=True)
    f.box(108, y, 654, 66, "", fill=fl, stroke=ec, r=4)
    f.text(120, y + 22, "if-part: " + a + "   |   main part: " + b, size=11, color=ec, anchor="start", bold=True)
    f.text(120, y + 44, ex, size=11.5, color=SLATE, anchor="start")
    f.text(750, y + 58, kind, size=10.5, color=ec, anchor="end", bold=True)
f.text(390, 322, "unless = if not;  Had I known = If I had known;  I wish I had a car", size=10.5, color=NAVY, bold=True)
```

## 5.3 Causative verbs, to-infinitives and gerunds

- **Causatives**: *have/get something done* (I had my hair cut); *make/let/have someone + bare verb* (She made me laugh; The teacher let them leave); *get someone + to-verb* (I got the mechanic to repair it).
- **Verb + -ing**: enjoy, avoid, finish, mind, suggest, consider, practise, admit, deny, give up, can't help, look forward to, be used to, it's no use, it's worth.
- **Verb + to**: want, decide, hope, plan, promise, refuse, afford, manage, learn, agree.
- **Meaning changes**: *stop doing* (quit) vs *stop to do* (pause in order to); *remember/forget doing* (past event) vs *to do* (task). *Would rather* is followed by a bare verb.

```svgfig label="5.3" caption="Gerund or infinitive? After some verbs the next verb takes -ing, after others to + verb. The cell checks that the two lists share no verb. Learn the meaning change in four pairs: stop doing (quit) and stop to do (pause in order to); remember doing (a past event) and remember to do (a task). Causatives: have or get something done, make or let someone do (bare verb), get someone to do."
ING = ["enjoy", "avoid", "finish", "mind", "suggest", "consider", "practise", "admit", "deny", "give up"]
TO = ["want", "decide", "hope", "plan", "promise", "refuse", "afford", "manage", "learn", "agree"]
assert not set(ING) & set(TO) and len(ING) == len(TO) == 10
f = Fig(780, 340)
f.box(14, 10, 250, 26, "verb + -ing (gerund)", fill=NAVY, stroke=NAVY, color="#ffffff", size=11, bold=True)
f.box(274, 10, 250, 26, "verb + to (infinitive)", fill=TEAL, stroke=TEAL, color="#ffffff", size=11, bold=True)
for i, (a, b) in enumerate(zip(ING, TO)):
    y = 42 + (i % 5) * 28; xa = 14 + 0; 
for k, v in enumerate(ING):
    f.box(14 + (k // 5) * 126, 42 + (k % 5) * 28, 122, 24, "I " + v + " -ing", fill=BLUE, stroke=NAVY, color=NAVY, size=10.5, bold=True)
for k, v in enumerate(TO):
    f.box(274 + (k // 5) * 126, 42 + (k % 5) * 28, 122, 24, v + " to ...", fill=MINT, stroke=TEAL, color=TEAL, size=10.5, bold=True)
f.box(540, 10, 226, 26, "causatives", fill=AMBER, stroke=AMBER, color="#ffffff", size=11, bold=True)
for i, t in enumerate(["I had my hair cut.", "She made me laugh.", "He let them leave.", "I got him to repair it."]):
    f.box(540, 42 + i * 34, 226, 28, t, fill=SAND, stroke=AMBER, color=AMBER, size=10.5, bold=True)
f.text(140, 200, "Meaning changes with the form", size=11.5, color=NAVY, bold=True)
pairs = [("stop doing", "quit the action", "stop to do", "pause in order to do something"), ("remember doing", "recall a past event", "remember to do", "not forget a task")]
for i, (a, am, b, bm) in enumerate(pairs):
    y = 214 + i * 56
    f.box(14, y, 180, 24, a, fill=BLUE, stroke=NAVY, color=NAVY, size=10.5, bold=True); f.text(204, y + 17, am, size=10.5, color=SLATE, anchor="start")
    f.box(14, y + 28, 180, 24, b, fill=MINT, stroke=TEAL, color=TEAL, size=10.5, bold=True); f.text(204, y + 45, bm, size=10.5, color=SLATE, anchor="start")
f.text(560, 230, "would rather + bare verb", size=11, color=RED, anchor="start", bold=True)
f.text(560, 252, "I would rather stay.", size=10.5, color=SLATE, anchor="start")
f.text(560, 282, "look forward to + -ing", size=11, color=RED, anchor="start", bold=True)
f.text(560, 304, "to is a preposition here", size=10.5, color=SLATE, anchor="start")
```

## 5.4 Eight traps in clauses, conditionals and verb patterns

These items test one rule each, so the traps are rules that students half remember.

1. **Who is the subject, whom is the object.** In "The woman whom I met", *I* is already the subject of the clause, so the pronoun is the object *whom* (Fig 5.1). Test by replacing the pronoun with *he* or *him*. If *him* fits, use *whom*.
2. **Do not use *that* in a non-defining clause.** "Kathmandu, which is the capital, is crowded" needs commas and *which*. A defining clause has no commas and may use *that*. Remember that *whose* shows possession for both people and things.
3. **Do not put *will* in the *if*-part.** Write "If it rains, we will stay home", not "If it will rain". The first conditional uses present in the *if*-part and *will* in the main part (Fig 5.2). The same holds for *when*, *as soon as* and *unless* in future meaning.
4. **Use *were* for every person in the second conditional.** "If I were a bird, I would fly" is correct for *I*, *he* and *she*. The second conditional talks about an unreal present, so the verb is past. After *wish* use the same pattern: *I wish I had a car*.
5. **The third conditional needs past perfect and *would have*.** "If he had studied, he would have passed" talks about the past that cannot be changed. Do not use *would have* in the *if*-part. The inverted form *Had he studied* means the same.
6. **Unless already means if not.** "Unless you hurry, you will miss the bus" equals "If you do not hurry, you will miss the bus". Do not add another *not*: *unless you do not hurry* is wrong. Use *unless* only with a positive verb.
7. **Learn which verbs take -ing and which take to.** *Enjoy*, *avoid*, *finish*, *mind* and *suggest* take -ing; *want*, *decide*, *hope*, *plan* and *refuse* take *to* (Fig 5.3). *Make* and *let* take a bare verb: *She made me laugh*. *Look forward to* is followed by -ing, because *to* is a preposition.
8. **Check the meaning change.** *He stopped smoking* means he quit; *He stopped to smoke* means he paused in order to smoke. *I remember posting the letter* is a memory; *Remember to post the letter* is a task (Fig 5.3). *Would rather* is followed by a bare verb: *I would rather stay*.

### 5.4.1 Worked checks

**Q. Fill in the blank: "The woman ____ I met is my teacher." (who / whom / whose)**

**Answer.** The woman is the object of *met*, so the answer is **whom**. *I* is the subject of the clause (Fig 5.1).

**Q. Complete: "If he had studied, he ____ passed."**

**Answer.** This is the third conditional (unreal past), so the main part is **would have** passed (Fig 5.2).

**Q. Choose the correct form: "She suggested ____ early." (to leave / leaving)**

**Answer.** *Suggest* takes the gerund, so the answer is **leaving**: "She suggested leaving early" (Fig 5.3).

**Q. Correct the sentence: "If it will rain tomorrow, we will stay home."**

**Answer.** The *if*-part takes the present tense: "If it **rains** tomorrow, we will stay home" (Fig 5.2).

## Formula and fact sheet

| Pattern | Rule |
|---|---|
| First conditional | if + present, will |
| Second conditional | if + past (were), would |
| Third conditional | if + had V3, would have V3 |
| make / let | + bare infinitive |
| enjoy, avoid, suggest | + -ing |
| decide, promise, refuse | + to |

## Chapter summary

- *Who* for people, *which* for things, *whose* for owners.
- Never use *will* or *would* in the *if*-clause.
- *Unless* already has a negative; do not add *not*.
- *Make* and *let* take a bare verb; *get* takes *to*.
- Learn the *-ing* verbs and the *to* verbs as two lists.

## Practice questions

**Set A — Recall (20 questions)**

1. The man ___ lives next door is a doctor.
   (a) whom (b) whose (c) which (d) who
2. The book ___ I bought yesterday is interesting.
   (a) which (b) who (c) whose (d) whom
3. She is the girl ___ father is a pilot.
   (a) who (b) whom (c) whose (d) which
4. If it rains, we ___ at home.
   (a) would stay (b) will stay (c) stayed (d) stays
5. If I ___ a bird, I would fly.
   (a) am (b) was (c) be (d) were
6. If he had studied, he ___ passed.
   (a) will have (b) would (c) would have (d) had
7. Unless you hurry, you ___ miss the bus.
   (a) will (b) won't (c) did (d) hadn't
8. I had my hair ___ yesterday.
   (a) cutting (b) cut (c) to cut (d) cuts
9. She made me ___.
   (a) to laugh (b) laughing (c) laugh (d) laughed
10. He enjoys ___ football.
    (a) to play (b) play (c) played (d) playing
11. She decided ___ a new job.
    (a) to find (b) finding (c) find (d) found
12. Water boils if you ___ it to 100°C.
    (a) heated (b) heat (c) will heat (d) would heat
13. I look forward to ___ you.
    (a) see (b) saw (c) seeing (d) to see
14. The teacher let the students ___ early.
    (a) leave (b) to leave (c) leaving (d) left
15. He avoided ___ the question.
    (a) to answer (b) answer (c) answered (d) answering
16. I will get the mechanic ___ the car.
    (a) repair (b) to repair (c) repairing (d) repaired
17. That is the house ___ I was born.
    (a) where (b) which (c) who (d) whose
18. She suggested ___ to the park.
    (a) to go (b) go (c) going (d) went
19. I would rather ___ tea than coffee.
    (a) to have (b) having (c) had (d) have
20. She stopped ___ last year, and her health improved.
    (a) to smoke (b) smoking (c) smoke (d) smoked

::: note Answers and explanations — Set A
**1.** (d) — "who" is the subject for a person.
**2.** (a) — "which" for a thing.
**3.** (c) — "whose" shows possession.
**4.** (b) — first conditional: if + present, will.
**5.** (d) — "were" in the unreal present.
**6.** (c) — third conditional: would have + V3.
**7.** (a) — "unless" = if not, so the main clause stays positive.
**8.** (b) — have + object + past participle.
**9.** (c) — make + bare verb.
**10.** (d) — enjoy + -ing.
**11.** (a) — decide + to-infinitive.
**12.** (b) — zero conditional: present in both clauses.
**13.** (c) — look forward to + -ing.
**14.** (a) — let + bare verb.
**15.** (d) — avoid + -ing.
**16.** (b) — get + object + to-verb.
**17.** (a) — "where" refers to a place.
**18.** (c) — suggest + -ing.
**19.** (d) — would rather + bare verb.
**20.** (b) — "stopped smoking" means quit.
:::

**Set B — Understanding (12 questions)**

1. If she ___ harder, she would pass.
   (a) studies (b) will study (c) studied (d) had studied
2. If I had known, I ___ you.
   (a) would have told (b) would tell (c) will tell (d) had told
3. Rama, ___ brother is a doctor, lives here.
   (a) who (b) whom (c) which (d) whose
4. The woman ___ I met yesterday is my teacher.
   (a) whose (b) whom (c) which (d) what
5. He had his car ___.
   (a) repair (b) repairing (c) repaired (d) to repair
6. I can't help ___ when I see a joke.
   (a) laughing (b) to laugh (c) laugh (d) laughed
7. It is no use ___ over spilt milk.
   (a) cry (b) to cry (c) cried (d) crying
8. I am used to ___ up early.
   (a) get (b) getting (c) got (d) to get
9. Which sentence is correct?
   (a) If it rains, I will stay home. (b) If it will rain, I will stay home. (c) If it rained, I will stay. (d) If it rains, I would stay.
10. He promised ___ me.
    (a) helping (b) help (c) to help (d) helped
11. "Had I known" means
    (a) If I knew (b) Unless I knew (c) If I know (d) If I had known
12. Unless you study, you ___ pass.
    (a) will (b) won't (c) would (d) wouldn't

::: note Answers and explanations — Set B
**1.** (c) — second conditional: if + past.
**2.** (a) — third conditional main clause.
**3.** (d) — "whose" before a noun.
**4.** (b) — "whom" is the object of "met".
**5.** (c) — have something done.
**6.** (a) — can't help + -ing.
**7.** (d) — it's no use + -ing.
**8.** (b) — used to + -ing means accustomed.
**9.** (a) — no "will" in the if-clause.
**10.** (c) — promise + to.
**11.** (d) — inversion replaces "if".
**12.** (b) — "unless you study" = if you do not study, so you won't pass.
:::

**Set C — Application (8 questions)**

1. The school ___ I studied is near my house.
   (a) who (b) whom (c) whose (d) where
2. If he ___ earlier, he would have caught the train.
   (a) had left (b) left (c) has left (d) would leave
3. She had the tailor ___ a dress.
   (a) to make (b) making (c) make (d) made
4. I forgot ___ the letter yesterday, so it is still on my desk.
   (a) posting (b) to post (c) post (d) posted
5. He remembers ___ the lock; he is sure he did it.
   (a) to lock (b) lock (c) locked (d) locking
6. The man ___ car was stolen called the police.
   (a) whose (b) who (c) whom (d) which
7. If water is heated to 100°C, it ___.
   (a) boiled (b) will boil (c) boils (d) would boil
8. I wish I ___ a car.
   (a) have (b) had (c) will have (d) having

::: note Answers and explanations — Set C
**1.** (d) — a place: where.
**2.** (a) — third conditional: if + past perfect.
**3.** (c) — have + person + bare verb.
**4.** (b) — "forgot to post": the task was not done.
**5.** (d) — "remembers locking": a past action recalled.
**6.** (a) — possession of the car: whose.
**7.** (c) — zero conditional: present, present.
**8.** (b) — unreal present: wish + past.
:::
