---
subject: English
grade: BCA
unit: 7
title: Reading Comprehension
hours: 5
area: Reading
---

The reading section has four or five questions on one or two passages; the Dean's Office model had a passage on genetic engineering with questions on tone, detail and what is "not true". The passage is the easiest part of the English paper to prepare for, because the answer is always *in the text*. This chapter gives the method and then four original passages with eight questions each.

::: key What the paper asks from this chapter
- **Main idea** and **purpose**: what the whole passage is for.
- **Detail**: a fact stated in the text; **NOT/EXCEPT** questions.
- **Inference**: what must follow from what is stated.
- **Vocabulary in context**: the meaning the word has *here*.
- **Tone** and **attitude**.
:::

## 7.1 Passage reading: main idea, detail, inference, vocabulary in context, tone

1. **Read the questions first**, then the passage once at normal speed. Mark names, numbers and contrast words (*but, however, although*).
2. **Main idea** is in the first and last sentences, and the options that are too narrow (one detail) or too broad (a whole subject) are wrong.
3. **Detail questions**: find the sentence, then compare it word by word with the option. A *NOT* question has three true statements and one false or absent one.
4. **Inference**: the answer must follow from the text; extreme words (*always, never, only, all*) are usually wrong.
5. **Vocabulary in context**: substitute each option into the sentence and keep the one that fits the surrounding meaning.
6. **Tone**: words such as *worrying, hopeful, mocking* in the text give the attitude; a factual passage has an informative tone.

::: tip Time plan
About 8 minutes for a 120-word passage with five questions: 2 minutes reading, 1 minute per question, and leave the hardest inference for last.
:::

## 7.2 One passage, annotated

Passage 1 in Set A is about glaciers and rivers. Before you answer any question, split the passage into sentences and give each sentence a job: topic, detail, set-up, pivot or conclusion. The pictures below show the real places the passage talks about, and Fig 7.1 marks up the text.

```photogrid label="7.1" cols="3" ratio="1.0" caption="The places in Passage 1. (a) The debris-covered Ngozumpa Glacier in the Khumbu region: the ice stores winter water. (b) The Kali Gandaki valley, where the Gandaki begins its run from the high Himalaya. (c) The Koshi River at the barrage, where the water reaches boatmen and farmers on the plains. Pictures help you hold the topic in mind: snow and ice, then rivers, then people (Fig 7.1)."
@ photo id="bcaeng/glacier" cap="(a) glacier: stored ice"
focus 0.4 0.5
@ photo id="bcaeng/gandaki" cap="(b) river: slow release"
focus 0.5 0.5
@ photo id="bcaeng/barrage" cap="(c) plains: people downstream"
focus 0.35 0.45
```

```svgfig label="7.1" caption="Passage 1 annotated. The cell splits the passage into its six sentences, counts the words (123 in all), finds the four proper names (Himalaya, Koshi, Gandaki, Karnali) and the signal words, and gives each sentence a job. The first sentence names the topic, the pivot sentence starts with But, and the last sentence (with therefore) states the main idea, which is why Question 1 is answered from the first and last sentences."
import textwrap
S = ["Nepal's rivers begin as snow and ice.",
     "In the high Himalaya, glaciers store water in winter and release it slowly through the warm months, so that the Koshi, the Gandaki and the Karnali keep flowing long after the monsoon has ended.",
     "Scientists who study these glaciers report that most of them are shrinking as the climate warms.",
     "For a few decades the melt may even raise river flows, which can look like good news.",
     "But a glacier that has thinned cannot be refilled quickly, and in the long run less ice means less water in the dry season.",
     "Farmers in the hills and the plains therefore have a stake in what happens on the peaks, even if they have never seen a glacier."]
roles = [("topic", NAVY, BLUE), ("detail + names", TEAL, MINT), ("detail: who says", TEAL, MINT),
         ("set-up (hedge)", AMBER, SAND), ("pivot: But", RED, ROSE), ("conclusion =\nmain idea", NAVY, BLUE)]
words = [len(s.split()) for s in S]
assert len(S) == 6 and words == [7, 34, 16, 17, 24, 25] and sum(words) == 123
names = []
for s in S:
    for k, w in enumerate(s.replace(",", "").replace(".", "").split()):
        if w[0].isupper() and k > 0: names.append(w)
assert names == ["Himalaya", "Koshi", "Gandaki", "Karnali"], names
SIG = ("but", "therefore", "even", "may", "can", "most")
rows = []
for s in S:
    lines = textwrap.wrap(s, 70)
    rows.append((lines, max(38, 14 * len(lines) + 14)))
H = 40 + sum(h + 6 for _, h in rows) + 54
f = Fig(780, H)
f.box(14, 6, 112, 24, "job", fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
f.box(130, 6, 500, 24, "sentence", fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
f.box(634, 6, 132, 24, "words, clues", fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
y = 36
for i, (lines, h) in enumerate(rows):
    r, c, bg = roles[i]
    f.box(14, y, 112, h, r, fill=bg, stroke=c, color=c, size=10.5, bold=True)
    f.box(130, y, 500, h, "", fill=SOFT, stroke="#cbd5e1")
    f.text(138, y + h / 2, "\n".join(lines), size=10.5, color=SLATE, anchor="start", vmid=True)
    sig = [w for w in SIG if w in [x.strip(",.").lower() for x in S[i].split()]]
    clue = str(words[i]) + " words" + ("\n" + ", ".join(sig) if sig else "")
    f.box(634, y, 132, h, clue, fill=SOFT, stroke="#cbd5e1", color=NAVY, size=10.5)
    y += h + 6
f.box(14, y + 2, 752, 40, "", fill=BLUE, stroke=NAVY, r=5)
f.text(28, y + 22, "Main idea = sentence 1 (topic) + sentence 6 (therefore): shrinking glaciers matter to farmers downstream.", size=10.5, color=NAVY, anchor="start", bold=True, vmid=True)
```

```svgfig label="7.2" caption="An 8-minute plan for one passage with five questions: 2 minutes reading, 1 minute for each question, 1 minute to check (2 + 5 + 1 = 8). Below it, the four options of Question 1 are filtered. The cell checks that beauty, climb and length never appear in the passage, and that the correct option (c) uses the word downstream, which is not in the passage either: a correct answer paraphrases, so do not hunt for the same words."
P = ("Nepal's rivers begin as snow and ice. In the high Himalaya, glaciers store water in winter and release it slowly through the warm months, "
     "so that the Koshi, the Gandaki and the Karnali keep flowing long after the monsoon has ended. Scientists who study these glaciers report that most of them are shrinking as the climate warms. "
     "For a few decades the melt may even raise river flows, which can look like good news. But a glacier that has thinned cannot be refilled quickly, and in the long run less ice means less water in the dry season. "
     "Farmers in the hills and the plains therefore have a stake in what happens on the peaks, even if they have never seen a glacier.").lower()
plan = [("read\nquestions,\nthen passage", 2)] + [("Q%d" % k, 1) for k in range(1, 6)] + [("check", 1)]
assert sum(m for _, m in plan) == 8
for w in ("beauty", "climb", "length", "downstream"):
    assert w not in P, w
assert "glaciers" in P and "farmers" in P
f = Fig(780, 330)
f.text(390, 14, "8 minutes for 5 questions: hardest inference last", size=11.5, color=NAVY, bold=True)
x = 20
cols = [NAVY, TEAL, TEAL, TEAL, TEAL, TEAL, AMBER]
for (lab, m), c in zip(plan, cols):
    w = m * 92
    f.box(x, 26, w - 4, 52, lab, fill=c, stroke=c, color="#ffffff", size=10.5, bold=True)
    x += w
f.text(20, 98, "0", size=10.5)
f.text(204, 98, "2 min", size=10.5)
f.text(756, 98, "8 min", size=10.5, anchor="end")
f.text(390, 130, "Filter Question 1: The passage is mainly about ...", size=11.5, color=NAVY, bold=True)
opts = [("(a) the beauty of\nHimalayan peaks", "off topic: beauty is\nnot in the text", ROSE, RED),
        ("(b) how to climb\nglaciers", "off topic: climbing is\nnot in the text", ROSE, RED),
        ("(c) why shrinking glaciers\nmatter to people downstream", "paraphrase of sentences\n1 and 6: CORRECT", MINT, TEAL),
        ("(d) the length of\nNepal's rivers", "too narrow: length is\nnever stated", SAND, AMBER)]
for i, (o, v, bg, c) in enumerate(opts):
    x = 14 + i * 190
    f.box(x, 144, 182, 64, o, fill=bg, stroke=c, color=SLATE, size=10.5, bold=(i == 2))
    f.box(x, 214, 182, 54, v, fill=SOFT, stroke=c, color=c, size=10.5, bold=True)
f.text(390, 296, "Too narrow (one detail), too broad (the whole subject) or off topic: reject. Keep the paraphrase.", size=10.5, color=SLATE)
```

## 7.3 Vocabulary in context and the extreme-word filter

Two quick tests settle many questions. For a word in context, put each option into the sentence and keep the one that fits both grammar and meaning. For an inference or detail question, scan the options for extreme words such as *only*, *always*, *never* and *all*: if the passage does not say it, the option is probably wrong.

```svgfig label="7.3" caption="Two tests. Top: the word stake in the last sentence, tried with each option; only interest gives a sentence that makes sense and fits therefore. Bottom: the extreme-word scan applied to Question 2 and Question 4 of Passage 1. The cell flags every option that contains only, always, never or all; all four flagged options are wrong and the unflagged answers (a) and (b) are correct. A flag is a warning, not a proof, so always check the text."
import re
tests = [("a pole", "Farmers have a pole in what happens on the peaks.", "no: farmers do not hold a pole", False),
         ("a bet", "Farmers have a bet in what happens on the peaks.", "odd: you bet ON something", False),
         ("an interest", "Farmers have an interest in what happens on the peaks.", "yes: a share in the outcome", True),
         ("a danger", "Farmers have a danger in what happens on the peaks.", "no: breaks the sense", False)]
assert [t[0] for t in tests if t[3]] == ["an interest"]
Q2 = ["after the monsoon has ended", "only during the monsoon", "only in winter", "only on the plains"]
Q4 = ["more floods only", "less water in the dry season", "more snow", "no change"]
flag = lambda s: bool(re.search(r"\b(only|always|never|all)\b", s))
assert [flag(o) for o in Q2] == [False, True, True, True]
assert [flag(o) for o in Q4] == [True, False, False, False]
f = Fig(780, 380)
f.text(390, 14, "Test 1: put each option in place of stake", size=11.5, color=NAVY, bold=True)
for i, (o, s, v, ok) in enumerate(tests):
    y = 28 + i * 40
    c = TEAL if ok else RED
    f.box(14, y, 96, 34, o, fill=MINT if ok else ROSE, stroke=c, color=c, size=11, bold=True)
    f.box(114, y, 380, 34, s, fill=SOFT, stroke="#cbd5e1", color=SLATE, size=10.5, anchor="start")
    f.box(498, y, 268, 34, v, fill=SOFT, stroke=c, color=c, size=10.5)
f.text(390, 206, "Test 2: scan the options for extreme words (Q2 and Q4)", size=11.5, color=NAVY, bold=True)
for r, (lab, Q, ans) in enumerate([("Q2", Q2, 0), ("Q4", Q4, 1)]):
    y = 222 + r * 70
    for i, o in enumerate(Q):
        x = 14 + i * 190
        fl = flag(o)
        c = RED if fl else (TEAL if i == ans else SLATE)
        bg = ROSE if fl else (MINT if i == ans else SOFT)
        f.box(x, y, 182, 40, __import__("textwrap").fill("(%s) %s" % ("abcd"[i], o), 24), fill=bg, stroke=c, color=c, size=10.5, bold=(i == ans))
        f.text(x + 91, y + 54, "flag: extreme word" if fl else ("correct" if i == ans else "no flag"), size=10, color=c)
```

## 7.4 Eight traps in reading comprehension

Each trap below is a way the paper makes a wrong option look right. The examples use Passage 1 from Set A.

1. **Read the questions before the passage.** Two minutes of reading and one minute for each question is enough for a 120-word passage (Fig 7.2). Knowing the questions tells you what to underline: names, numbers and the words *but* and *therefore*.
2. **The correct main idea is a paraphrase.** Question 1 is answered by "why shrinking glaciers matter to people downstream", yet the word *downstream* is not in the passage (Fig 7.2). Join the first and last sentences, then pick the option that says the same thing in other words.
3. **Reject options that are too narrow or too broad.** "The length of Nepal's rivers" picks up a detail the text never states, and "the beauty of Himalayan peaks" is another subject. A main idea covers the whole passage, no more and no less.
4. **Compare detail options word by word.** The text says *most* glaciers are shrinking, not all of them, and rivers keep flowing *after* the monsoon, not *only during* it (Fig 7.3). One changed word makes an option false.
5. **A NOT question has three true options.** For "Which river is NOT mentioned?" check each river against the sentence: Koshi, Gandaki and Karnali are named, so the answer is the Brahmaputra (Fig 7.1). Do not choose an option just because it is true in real life.
6. **Do not go beyond the text in an inference.** The melt "may even raise" river flows; it does not always do so. An inference must follow from the words, so hedges such as *may* and *can* matter, and options with *only* or *always* are suspect (Fig 7.3).
7. **Test vocabulary in context by substitution.** *Stake* has several meanings, but only *interest* fits "have a stake in what happens on the peaks" (Fig 7.3). Do not choose the meaning you know best; choose the one the sentence needs.
8. **Read tone from the signal words.** *Scientists report*, *good news*, *But* and *therefore* show a concerned and informative tone. An angry, humorous or indifferent tone needs words in the text that show it, and none appear here.

### 7.4.1 Worked checks

**Q. Which river is NOT mentioned in Passage 1? (Koshi / Gandaki / Karnali / Brahmaputra)**

**Answer.** The names in the text are the Koshi, the Gandaki and the Karnali, so the answer is the **Brahmaputra** (Fig 7.1).

**Q. In the sentence "Farmers ... have a stake in what happens on the peaks", the word stake means (a pole / a bet / an interest / a danger).**

**Answer.** Substituting each option shows that only **an interest** gives a sensible sentence (Fig 7.3).

**Q. Why might the melt look like good news for a few decades?**

**Answer.** Because the melt **may raise river flows** for a while (sentence 4, Fig 7.1). The next sentence begins with *But* and explains why this is only temporary.

**Q. Choose the main idea: (a) beauty of peaks / (b) how to climb glaciers / (c) why shrinking glaciers matter downstream / (d) length of rivers.**

**Answer.** Option **(c)** joins sentence 1 (snow and ice feed rivers) and sentence 6 (farmers have a stake); the other options are off topic or too narrow (Fig 7.2).


## Formula and fact sheet

| Question type | Where the answer is |
|---|---|
| Main idea | first + last sentences |
| Detail | one sentence in the text |
| NOT / EXCEPT | three options are in the text |
| Inference | follows from the text, never beyond it |
| Vocabulary | the surrounding sentence |

## Chapter summary

- Read the questions first.
- The answer is in the passage, not in your opinion.
- Reject options with *always, never, only* unless the text says so.
- Test vocabulary options by substitution.
- "NOT" means three options are true.

## Practice questions

**Set A — Passage 1**

Nepal's rivers begin as snow and ice. In the high Himalaya, glaciers store water in winter and release it slowly through the warm months, so that the Koshi, the Gandaki and the Karnali keep flowing long after the monsoon has ended. Scientists who study these glaciers report that most of them are shrinking as the climate warms. For a few decades the melt may even raise river flows, which can look like good news. But a glacier that has thinned cannot be refilled quickly, and in the long run less ice means less water in the dry season. Farmers in the hills and the plains therefore have a stake in what happens on the peaks, even if they have never seen a glacier.

1. The passage is mainly about
   (a) the beauty of Himalayan peaks (b) how to climb glaciers (c) why shrinking glaciers matter to people downstream (d) the length of Nepal's rivers
2. According to the passage, glaciers keep rivers flowing
   (a) after the monsoon has ended (b) only during the monsoon (c) only in winter (d) only on the plains
3. Why might the melt look like good news for a few decades?
   (a) glaciers grow bigger (b) farmers stop using water (c) rainfall increases (d) river flows may rise at first
4. In the long run, less ice means
   (a) more floods only (b) less water in the dry season (c) more snow (d) no change
5. The word "stake" in the passage means
   (a) a pole (b) a bet (c) an interest (d) a danger
6. Which river is NOT mentioned in the passage?
   (a) the Koshi (b) the Gandaki (c) the Karnali (d) the Brahmaputra
7. The author's tone is
   (a) concerned and informative (b) humorous (c) angry (d) indifferent
8. We can infer that a glacier that has thinned
   (a) refills in one season (b) recovers only slowly (c) turns into a river (d) is unaffected

::: note Answers and explanations — Set A
**1.** (c) — the passage links glacier loss to farmers downstream.
**2.** (a) — "long after the monsoon has ended".
**3.** (d) — "the melt may even raise river flows".
**4.** (b) — "less ice means less water in the dry season".
**5.** (c) — "have a stake" means have an interest.
**6.** (d) — only the Koshi, Gandaki and Karnali are named.
**7.** (a) — factual with an undercurrent of worry.
**8.** (b) — "cannot be refilled quickly".
:::

**Set B — Passage 2**

Most beginners believe that programming is a talent that some people are born with. In practice it is closer to learning a musical instrument. A student who writes a small program every day, reads the error messages carefully and fixes one bug at a time improves steadily, while a student who copies long programs without understanding them stalls. Good programmers are not those who never make mistakes; they are the ones who find their mistakes quickly. They break a large problem into small steps, test each step, and keep notes about what failed. Patience, rather than brilliance, is the quality that separates those who continue from those who give up.

1. The passage compares programming to
   (a) cooking (b) learning a musical instrument (c) playing football (d) painting
2. Which student improves steadily?
   (a) one who copies long programs (b) one who never writes code (c) one who avoids errors (d) one who writes a small program daily
3. Good programmers are those who
   (a) find their mistakes quickly (b) never make mistakes (c) memorise code (d) work alone
4. The word "stalls" means
   (a) speeds up (b) ends happily (c) stops progressing (d) turns back
5. What separates those who continue from those who give up?
   (a) talent (b) luck (c) money (d) patience
6. The author's attitude is
   (a) discouraging (b) encouraging (c) sarcastic (d) neutral
7. Which is NOT advice given in the passage?
   (a) test each step (b) keep notes on what failed (c) avoid reading error messages (d) break a problem into small steps
8. "Brilliance" is contrasted with
   (a) patience (b) talent (c) practice (d) notes

::: note Answers and explanations — Set B
**1.** (b) — "closer to learning a musical instrument".
**2.** (d) — small daily programs improve steadily.
**3.** (a) — "they are the ones who find their mistakes quickly".
**4.** (c) — copying without understanding stops progress.
**5.** (d) — the last sentence names patience.
**6.** (b) — it tells beginners how to improve.
**7.** (c) — the passage says to read error messages carefully.
**8.** (a) — "patience, rather than brilliance".
:::

**Set C — Passage 3**

Walk through the middle hills of Nepal and the slopes look like giant staircases. These terraces were cut by generations of farmers who needed flat ground to grow rice and millet on steep land. A terrace holds soil in place during the monsoon, and it lets water move slowly from one level to the next so that each field gets a share. The work is hard, because walls must be repaired every year and many young people have left for cities or abroad. When a terrace is abandoned, the wall collapses within a few seasons and the soil that took centuries to build washes away. Keeping the terraces alive is therefore not only about food but also about protecting the hillside itself.

1. Terraces were built to
   (a) hold religious festivals (b) store water in lakes (c) mark village boundaries (d) create flat land for farming on steep slopes
2. During the monsoon a terrace helps by
   (a) holding the soil in place (b) stopping all rain (c) growing trees (d) storing grain
3. Why are terraces being abandoned?
   (a) rice is unprofitable (b) there is too much rain (c) many young people have moved away (d) laws forbid them
4. What happens when a terrace is abandoned?
   (a) it becomes fertile (b) the wall collapses and soil washes away (c) it floods at once (d) nothing changes
5. "Generations" in the passage means
   (a) governments (b) villages (c) lessons (d) successive groups of family members
6. The main idea of the passage is that terraces
   (a) matter for food and for protecting the hillside (b) are a tourist attraction (c) are cheap to maintain (d) are used only for rice
7. Which crop is mentioned?
   (a) wheat (b) tea (c) millet (d) maize
8. The author's tone is
   (a) mocking (b) appreciative and concerned (c) bored (d) hostile

::: note Answers and explanations — Set C
**1.** (d) — "needed flat ground to grow rice and millet on steep land".
**2.** (a) — "holds soil in place during the monsoon".
**3.** (c) — "many young people have left".
**4.** (b) — the wall collapses and soil washes away.
**5.** (d) — generations of farmers, one after another.
**6.** (a) — the last sentence.
**7.** (c) — rice and millet are named; millet is the option present.
**8.** (b) — respect for the work and worry for its loss.
:::

**Set D — Passage 4**

A library card costs nothing, yet many students never get one. They say they have no time to read, but the same students spend hours each day scrolling through short videos. Reading a book is slower and asks more of the mind, and that is exactly why it helps. A reader must follow an argument across many pages, hold ideas in memory and notice how sentences are built. Those habits carry over to every subject and to every examination. A student who reads even twenty pages a day finishes more than twenty books in a year.

1. Students who avoid libraries say they have
   (a) no time (b) no money (c) no books at home (d) no interest in videos
2. The same students spend hours each day on
   (a) homework (b) sport (c) short videos (d) library books
3. According to the passage, reading helps because it
   (a) is quick (b) asks more of the mind (c) costs nothing (d) needs no effort
4. Which skill is NOT mentioned as a benefit of reading?
   (a) following an argument (b) holding ideas in memory (c) noticing how sentences are built (d) typing quickly
5. "Carry over" means
   (a) lift (b) forget (c) transfer (d) end
6. A student who reads twenty pages a day
   (a) finishes more than twenty books in a year (b) finishes one book a year (c) reads too little to matter (d) will fail
7. The author's purpose is to
   (a) entertain (b) describe a library (c) criticise teachers (d) persuade students to read
8. The cost of a library card is
   (a) high (b) nothing (c) a small fee (d) not stated

::: note Answers and explanations — Set D
**1.** (a) — "they say they have no time to read".
**2.** (c) — "scrolling through short videos".
**3.** (b) — "asks more of the mind, and that is exactly why it helps".
**4.** (d) — typing is not mentioned.
**5.** (c) — habits transfer to other subjects.
**6.** (a) — 20 pages × 365 days is 7,300 pages, over twenty books of about 300 pages.
**7.** (d) — the passage urges students to read.
**8.** (b) — "costs nothing".
:::
