---
subject: English
grade: BCA
unit: 2
title: Idioms, Phrasal Verbs and Prepositions
hours: 6
area: Vocabulary
---

Idioms, phrasal verbs and prepositions are about 6 of the 40 English marks, and the Dean's Office model tests all three: "abide ___ their promise" (by), "will ___ his position" (take over), and "a Lion's share". These are memory items: the preposition after a word, the particle after a verb, the meaning of a fixed phrase. The tables below cover the ones that recur.

::: key What the paper asks from this chapter
- **Idioms**: the figurative meaning of a fixed phrase.
- **Phrasal verbs**: verb + particle with a meaning of its own (take over, put off).
- **Prepositions**: fixed pairs (good at, fond of) and time/place use (in, on, at, since, for).
:::

## 2.1 Idioms and phrases

| Idiom | Meaning |
|---|---|
| lion's share | the largest part |
| a piece of cake | something very easy |
| break the ice | ease the initial awkwardness |
| once in a blue moon | very rarely |
| spill the beans | reveal a secret |
| hit the nail on the head | be exactly right |
| under the weather | slightly ill |
| cost an arm and a leg | be very expensive |
| burn the midnight oil | work late at night |
| let the cat out of the bag | reveal a secret by mistake |
| bite the bullet | face something unpleasant bravely |
| call it a day | stop working |
| a blessing in disguise | a misfortune that turns out well |
| beat around the bush | avoid the main point |
| in the nick of time | just in time |
| add fuel to the fire | make a bad situation worse |
| turn a blind eye | pretend not to see |
| caught red-handed | caught in the act |

```photogrid label="2.1" cols="3" ratio="1.0" caption="Idioms start as pictures. (a) William Shakespeare, whose plays contain many phrases we still use, such as break the ice. (b) A piece of cake, which is where the idiom a piece of cake (something very easy) comes from: a slice of cake takes no effort. (c) The Finnish icebreaker Sampo (1898) literally breaking the ice; to break the ice in conversation means to ease the first awkward moment. The literal picture helps you remember the meaning (Fig 2.1)."
@ photo id="bcaeng/shakes" cap="Shakespeare: phrases that last"
focus 0.5 0.3
@ photo id="bcaeng/cake" cap="A piece of cake: very easy"
focus 0.5 0.5
@ photo id="bcaeng/icebreaker" cap="Break the ice: start a talk"
focus 0.5 0.6
```

```svgfig label="2.1" caption="Sixteen idioms from the list, sorted by meaning instead of alphabetically. Sorting by theme is the fastest way to learn them: secrets and honesty, time and work, amount and condition, and facing situations. The cell checks that each idiom appears once, so no idiom is lost between the groups."
groups = [("Secrets and honesty", [("spill the beans", "reveal a secret"), ("let the cat out of the bag", "reveal a secret by mistake"), ("caught red-handed", "caught in the act"), ("turn a blind eye", "pretend not to see")]),
          ("Time and work", [("once in a blue moon", "very rarely"), ("burn the midnight oil", "work late at night"), ("in the nick of time", "just in time"), ("call it a day", "stop working")]),
          ("Amount and condition", [("lion's share", "the largest part"), ("cost an arm and a leg", "be very expensive"), ("a piece of cake", "something very easy"), ("under the weather", "slightly ill")]),
          ("Facing situations", [("bite the bullet", "face something unpleasant"), ("break the ice", "ease the awkward start"), ("beat around the bush", "avoid the main point"), ("hit the nail on the head", "be exactly right")])]
allid = [a for g in groups for a, b in g[1]]
assert len(allid) == 16 and len(set(allid)) == 16
f = Fig(780, 330)
cols = [BLUE, SAND, MINT, ROSE]; edges = [NAVY, AMBER, TEAL, RED]
for i, (t, items) in enumerate(groups):
    x = 10 + i * 192
    f.box(x, 10, 184, 310, "", fill=cols[i], stroke=edges[i], r=5)
    f.text(x + 92, 34, t, size=11.5, color=edges[i], bold=True)
    for j, (a, b) in enumerate(items):
        y = 70 + j * 62
        f.text(x + 10, y, a, size=10.5, color=SLATE, anchor="start", bold=True)
        f.text(x + 10, y + 18, "= " + b, size=10.5, color=SLATE, anchor="start")
```

## 2.2 Phrasal verbs

| Phrasal verb | Meaning |
|---|---|
| take over | assume control or a position |
| take after | resemble (a parent) |
| take off | leave the ground; remove |
| give up | quit |
| look after | take care of |
| look forward to (+ -ing) | await eagerly |
| put off | postpone |
| call off | cancel |
| carry on | continue |
| run out of | have no more |
| break down | stop working |
| turn down | reject |
| come across | find by chance |
| get along with | be on good terms |
| set off | begin a journey |
| bring up | raise (a child) |

```svgfig label="2.2" caption="Two verbs that make many phrasal verbs. The same verb changes its meaning completely with the particle: take over (assume control), take after (resemble a parent), take off (leave the ground), take in (deceive or understand), take up (begin a habit); look after (care for), look into (investigate), look up to (respect), look down on (despise), look forward to (await eagerly, followed by -ing). Treat each phrasal verb as one word with one meaning."
f = Fig(780, 340)
hubs = [("take", 200, [("over", "assume control"), ("after", "resemble a parent"), ("off", "leave the ground"), ("in", "deceive; understand"), ("up", "begin a habit")]),
        ("look", 580, [("after", "care for"), ("into", "investigate"), ("up to", "respect"), ("down on", "despise"), ("forward to", "await eagerly (+ing)")])]
import math
for nm, cx, sp in hubs:
    cy = 170
    for k, (p, m) in enumerate(sp):
        a = math.radians(-90 + k * 72 + 36 - 36)
        x = cx + 120 * math.cos(a); y = cy + 120 * math.sin(a)
        f.line(cx, cy, x, y, color="#94a3b8", sw=1.4)
    f.circle(cx, cy, 34, fill=NAVY, stroke=NAVY, label=nm, size=15, color="#ffffff")
    for k, (p, m) in enumerate(sp):
        a = math.radians(-90 + k * 72)
        x = cx + 120 * math.cos(a); y = cy + 120 * math.sin(a)
        f.box(x - 52, y - 20, 104, 40, "", fill=BLUE, stroke=NAVY, r=5)
        f.text(x, y - 3, nm + " " + p, size=10.5, color=NAVY, bold=True)
        f.text(x, y + 13, m, size=9.5, color=SLATE)
```

## 2.3 Words followed by prepositions, and the use of prepositions

| Word | Preposition |
|---|---|
| abide | by |
| accused / guilty / capable / fond / proud / afraid / jealous | of |
| good / clever / bad / surprised | at |
| interested / succeed / believe | in |
| depend / insist / rely | on |
| married / superior / inferior / prefer | to |
| different / differ | from |
| angry | with (a person), at (a thing) |
| congratulate | on |
| famous / responsible | for |
| comply / agree / sympathise | with |

**Time and place.** *at* a clock time or point (at 10 a.m., at the gate); *on* days and dates (on Sunday, on 5 May); *in* months, years, longer periods (in July, in 2026). *Since* a point in time, *for* a duration. *Between* two, *among* more than two. *By* a deadline, *till/until* a continuing action. *During* a period, *within* a time limit.

```svgfig label="2.3" caption="Prepositions of time as nested boxes: at is the smallest (a clock time or a point), on is a day or a date, in is a month, year or long period. Since gives the starting point and for gives the length: since 2020 means for 6 years in 2026, which the cell computes. Between is used for two things, among for more than two."
yr0, yr1 = 2020, 2026
assert yr1 - yr0 == 6
f = Fig(780, 330)
f.box(14, 14, 380, 300, "", fill=BLUE, stroke=NAVY, r=6); f.text(204, 40, "IN: months, years, seasons, long periods", size=11, color=NAVY, bold=True)
f.text(204, 62, "in July, in 2026, in winter, in the morning", size=10.5, color=SLATE)
f.box(44, 82, 320, 190, "", fill=SAND, stroke=AMBER, r=6); f.text(204, 108, "ON: days and dates", size=11, color=AMBER, bold=True)
f.text(204, 130, "on Sunday, on 5 May, on my birthday", size=10.5, color=SLATE)
f.box(84, 150, 240, 100, "", fill=MINT, stroke=TEAL, r=6); f.text(204, 176, "AT: clock times, points", size=11, color=TEAL, bold=True)
f.text(204, 198, "at 10 a.m., at noon, at night,", size=10.5, color=SLATE); f.text(204, 216, "at the gate, at the bus park", size=10.5, color=SLATE)
f.text(580, 30, "since and for", size=12, color=NAVY, bold=True)
f.arrow([(430, 120), (750, 120)], color=SLATE, sw=2)
for y in range(2020, 2027):
    x = 450 + (y - 2020) * 48
    f.circle(x, 120, 4.5, fill=(NAVY if y in (2020, 2026) else "#ffffff"), stroke=NAVY); f.text(x, 146, str(y), size=10.5, color=SLATE, bold=True)
f.arrow([(450, 84), (738, 84)], color=TEAL, sw=2, both=True)
f.text(594, 74, "for 6 years (duration)", size=11, color=TEAL, bold=True)
f.text(450, 190, "since 2020 (starting point)", size=11, color=RED, bold=True, anchor="start")
f.text(430, 232, "I have lived in Pokhara since 2020.", size=10.5, color=SLATE, anchor="start")
f.text(430, 252, "I have lived in Pokhara for 6 years.", size=10.5, color=SLATE, anchor="start")
f.text(430, 286, "between = two (between Kathmandu and Pokhara)", size=10.5, color=NAVY, anchor="start", bold=True)
f.text(430, 308, "among = more than two (among the 77 districts)", size=10.5, color=NAVY, anchor="start", bold=True)
```

## 2.4 Eight traps in idioms, phrasal verbs and prepositions

These items depend on exact wording, so one wrong small word changes the answer. Learn the exact forms below.

1. **An idiom has one meaning, and the literal meaning is wrong.** *Spill the beans* has nothing to do with food: it means reveal a secret (Fig 2.1). If an option describes the literal picture, it is the trap. Choose the option that matches the figurative meaning.
2. **Do not change the words of an idiom.** It is *hit the nail on the head*, not "hit the nail in the head", and *let the cat out of the bag*, not "let the cat out of the box". Idiom questions often include a version with one word changed. Learn each idiom as a block.
3. **Two idioms can mean almost the same.** *Spill the beans* and *let the cat out of the bag* both mean revealing a secret, but the second suggests it happened by mistake. Read the sentence for words such as "accidentally". Check the small difference before you choose.
4. **The particle changes the verb.** *Take after* means resemble, *take off* means leave the ground, and *take over* means assume control (Fig 2.2). Never guess from the verb alone. Learn each phrasal verb as one word.
5. **A phrasal verb can be split, but not always.** You can say *put off the meeting* or *put the meeting off*, but with a pronoun you must say *put it off*. Some, like *look after*, cannot be split at all. In the sentence-completion questions check whether the order is correct.
6. **After *look forward to* use -ing.** "I look forward to meeting you" is correct; "I look forward to meet you" is wrong, because *to* is a preposition here, not part of an infinitive. The same applies to *used to* (being used to *walking*). Look at the word after *to*.
7. **Learn the fixed preposition pairs.** *Depend on*, *interested in*, *good at*, *proud of*, *different from*, *married to* and *superior to* are fixed (Fig 2.3). Do not use *than* after *superior* or *inferior*. Remember that you *prefer* tea *to* coffee, not "than coffee".
8. **At, on, in go from small to large; since and for are not the same.** Use *at* for a clock time, *on* for a day or date, and *in* for a month or year (Fig 2.3). *Since* names a starting point (since 2020) and *for* gives a length of time (for six years). Use *between* for two and *among* for more than two.

### 2.4.1 Worked checks

**Q. What does "a piece of cake" mean?**

**Answer.** It means something very easy, because eating a piece of cake needs no effort (Fig 2.1). It does not mean something sweet or a small portion.

**Q. Choose the correct phrasal verb: "She ____ her mother." (takes after / takes off)**

**Answer.** **Takes after** means resembles a parent, so the sentence is "She takes after her mother." *Takes off* would mean removes or leaves the ground (Fig 2.2).

**Q. Correct the sentence: "I am looking forward to meet you."**

**Answer.** The word *to* is a preposition here, so the verb takes -ing: "I am looking forward to **meeting** you."

**Q. Fill in the blank: "I have lived here ____ 2020." (since / for)**

**Answer.** 2020 is a starting point, so use **since**. With a length of time use *for*: "I have lived here for six years" (Fig 2.3).

## Formula and fact sheet

| Pattern | Example |
|---|---|
| since + point | since 2015 |
| for + duration | for three days |
| between / among | between two, among many |
| prefer A to B | prefers tea to coffee |
| look forward to + -ing | looking forward to meeting |

## Chapter summary

- Learn the preposition with the word: abide by, fond of, good at.
- Prefer *to*, superior *to*, inferior *to*: never *than*.
- Phrasal verbs often have a one-word equivalent (put off = postpone).
- *Since* with a point, *for* with a length.
- Idioms are never read literally.

## Practice questions

**Set A — Recall (20 questions)**

1. Sincere people abide ___ their promise.
   (a) by (b) of (c) at (d) on
2. The new manager will ___ his position on Monday.
   (a) take off (b) take out (c) take over (d) take after
3. The idiom "a piece of cake" means
   (a) a dessert (b) something very easy (c) a small portion (d) a party
4. "The lion's share" means
   (a) no share (b) a small share (c) an equal share (d) the largest part
5. He is fond ___ music.
   (a) in (b) at (c) of (d) for
6. "Once in a blue moon" means
   (a) very rarely (b) every month (c) at night (d) often
7. She is good ___ mathematics.
   (a) in (b) on (c) of (d) at
8. "To break the ice" means
   (a) to melt ice (b) to ease initial awkwardness (c) to break a rule (d) to cool down
9. I am looking forward ___ meeting you.
   (a) to (b) for (c) at (d) in
10. The phrasal verb "give up" means
    (a) donate (b) win (c) lift (d) quit
11. He is afraid ___ dogs.
    (a) from (b) at (c) of (d) with
12. "To spill the beans" means
    (a) to cook (b) to reveal a secret (c) to waste food (d) to tell a lie
13. The match was called ___ because of rain.
    (a) in (b) out (c) off (d) up
14. She was born ___ 5 May.
    (a) on (b) at (c) in (d) by
15. He has lived here ___ 2015.
    (a) for (b) from (c) during (d) since
16. The meeting is ___ 10 a.m.
    (a) in (b) at (c) on (d) by
17. He succeeded ___ passing the exam.
    (a) in (b) at (c) on (d) of
18. "A blessing in disguise" means
    (a) a hidden gift (b) a prayer (c) a misfortune that turns out well (d) a costume
19. We must put ___ the meeting till Monday.
    (a) on (b) up (c) out (d) off
20. She insisted ___ paying the bill.
    (a) for (b) on (c) to (d) at

::: note Answers and explanations — Set A
**1.** (a) — abide by means obey.
**2.** (c) — take over means assume control.
**3.** (b) — a very easy task.
**4.** (d) — the largest portion.
**5.** (c) — fond of.
**6.** (a) — very rarely.
**7.** (d) — good at a subject.
**8.** (b) — to relieve social tension.
**9.** (a) — look forward to, followed by -ing.
**10.** (d) — to quit or surrender.
**11.** (c) — afraid of.
**12.** (b) — to disclose a secret.
**13.** (c) — call off means cancel.
**14.** (a) — on with dates.
**15.** (d) — since with a starting point.
**16.** (b) — at with clock time.
**17.** (a) — succeed in.
**18.** (c) — a bad thing that proves good.
**19.** (d) — put off means postpone.
**20.** (b) — insist on.
:::

**Set B — Understanding (12 questions)**

1. "Abide by" means
   (a) live with (b) obey (c) wait for (d) stay at
2. He takes ___ his father in looks.
   (a) up (b) on (c) off (d) after
3. "Caught red-handed" means
   (a) caught while committing the act (b) injured (c) painted red (d) chased for a long time
4. He is superior ___ me in rank.
   (a) than (b) from (c) to (d) over
5. She is married ___ a doctor.
   (a) with (b) to (c) by (d) from
6. She is capable ___ solving the problem.
   (a) to (b) in (c) for (d) of
7. "To burn the midnight oil" means
   (a) to waste fuel (b) to light a lamp (c) to work late at night (d) to cause a fire
8. We ran ___ of sugar.
   (a) out (b) off (c) down (d) over
9. He is jealous ___ his friend's success.
   (a) at (b) with (c) for (d) of
10. He shared the sweets ___ the three children.
    (a) between (b) among (c) with (d) in
11. The car broke ___ on the highway.
    (a) down (b) off (c) in (d) away
12. The minister will arrive ___ Sunday morning.
    (a) at (b) in (c) on (d) by

::: note Answers and explanations — Set B
**1.** (b) — abide by a rule or promise.
**2.** (d) — take after means resemble.
**3.** (a) — caught in the act.
**4.** (c) — superior to, never "than".
**5.** (b) — married to.
**6.** (d) — capable of.
**7.** (c) — work late.
**8.** (a) — run out of.
**9.** (d) — jealous of.
**10.** (b) — among for more than two.
**11.** (a) — break down means stop working.
**12.** (c) — on with a day.
:::

**Set C — Application (8 questions)**

1. "To cost an arm and a leg" means
   (a) to cause injury (b) to be cheap (c) to be painful (d) to be very expensive
2. The teacher told him to ___ with his studies.
   (a) carry on (b) carry out (c) carry off (d) carry up
3. I came ___ an old friend in the market.
   (a) over (b) on (c) across (d) at
4. "To turn down an offer" means
   (a) to accept it (b) to reject it (c) to fold it (d) to reduce its volume
5. He is accused ___ theft.
   (a) for (b) with (c) at (d) of
6. The book is different ___ the film.
   (a) from (b) than (c) to (d) with
7. "To hit the nail on the head" means
   (a) to injure (b) to be exactly right (c) to build (d) to fail
8. She prefers tea ___ coffee.
   (a) than (b) from (c) to (d) over

::: note Answers and explanations — Set C
**1.** (d) — very costly.
**2.** (a) — carry on means continue.
**3.** (c) — come across means find by chance.
**4.** (b) — reject.
**5.** (d) — accused of.
**6.** (a) — different from.
**7.** (b) — be exactly right.
**8.** (c) — prefer A to B.
:::
