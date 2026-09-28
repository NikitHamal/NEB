---
subject: Compulsory English
grade: 11
unit: 34
title: Unseen Reading Comprehension Strategy
hours: 7
area: Writing and Skills
---

Question 1 is worth fifteen marks — a fifth of the whole paper — and it is the only
question you cannot revise for. The passage will be one you have never seen. That
sounds like bad news, and every year it is treated as such: students read the passage
once, slowly, panic at the words they do not know, and then hunt for answers they have
already forgotten the location of. The remedy is a **method**, applied in the same
order every time. Method is what you revise for this question.

::: key Read the questions before you read the passage
This single change is worth two or three marks. Questions tell you what to look for;
without them you are reading blind and must read twice. Spend ninety seconds on the
questions first, every time.
:::

## 34.1 What Question 1 looks like

| Feature | What to expect |
|---|---|
| Length of passage | about 350–500 words |
| Kind of passage | factual or argumentative, sometimes narrative |
| Number of questions | usually six to nine, mixed types |
| Marks | 15 in total — normally a block of 1-mark items and a block of 2-mark items |
| Time to allow | about 30–35 minutes of the three hours |

The passage is chosen so that **every answer is decidable from the passage alone**.
Outside knowledge is not rewarded, and it is the single commonest cause of a wrong
true/false answer.

## 34.2 Two reading speeds: skimming and scanning

They are not the same thing and they are not used at the same moment.

- **Skimming** is fast reading for the **shape**: what the passage is about and how it
  is arranged. You read the title, the first and last sentence of each paragraph, and
  nothing else. Thirty seconds.
- **Scanning** is fast reading for **one thing**: a date, a name, a figure, a word. Your
  eye ignores meaning entirely and hunts for the shape of the target. Five seconds.

A newspaper front page is designed around exactly these two habits, which is why it is
the best place to see them.

```photo id="eng11/newspaper" caption="A newspaper front page is built for skimming and scanning. Everything above the body text exists to tell a reader, in under a second, whether the rest is worth reading." width="70"
crop 0.020 0.015 0.975 0.990
mark 0.058 0.951 "1"
mark 0.173 0.591 "2"
mark 0.688 0.574 "3"
mark 0.921 0.330 "4"
key 1 The masthead and, under it, the date line — the first things a reader checks
key 2 The lead paragraph, set in bold. It answers who, what, when and where in two sentences, so that a skimming reader can stop there
key 3 Text set in narrow columns. The eye runs straight down the middle of a column; it never sweeps across the page
key 4 A section heading. Scanning for headings, not for words, is how a reader finds the one story wanted out of forty
```

An exam passage has no headlines, but it has the same skeleton: a first sentence that
announces the subject, one idea to a paragraph, and a last paragraph that judges or
concludes. Skim for that skeleton before you read a word closely.

## 34.3 The five-step method

```figure caption="The order that saves time. Steps 1 and 2 take two minutes together and remove almost all the re-reading."
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
fig, ax = plt.subplots(figsize=(4.8, 3.2))
ax.axis("off")
steps = [
    ("1", "Read the questions", "90 seconds. Underline the key word in each."),
    ("2", "Skim the passage", "30 seconds. Title, first and last lines only."),
    ("3", "Read closely, pencil in hand", "Mark the place each answer lives."),
    ("4", "Answer in the order set", "Easy marks first; leave inference to last."),
    ("5", "Check against the passage", "Every answer must be defensible from the text."),
]
y = 9.1
for num, head, sub in steps:
    ax.add_patch(mpatches.FancyBboxPatch((1.15, y), 8.2, 1.42,
                 boxstyle="round,pad=0.0,rounding_size=0.12",
                 linewidth=1.1, edgecolor=GRID, facecolor="#ffffff"))
    ax.add_patch(mpatches.Circle((0.72, y + 0.71), 0.42,
                 facecolor=ACCENT, edgecolor="none"))
    ax.text(0.72, y + 0.71, num, ha="center", va="center", fontsize=7.2,
            color="white")
    ax.text(1.50, y + 0.95, head, ha="left", va="center", fontsize=7.2, color=INK)
    ax.text(1.50, y + 0.44, sub, ha="left", va="center", fontsize=6.4, color=MUTED)
    y -= 1.80
for y0 in [9.05, 7.25, 5.45, 3.65]:
    ax.annotate("", xy=(5.2, y0 - 0.37), xytext=(5.2, y0 - 0.01),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=0.9))
ax.set_xlim(0.1, 9.6)
ax.set_ylim(1.5, 10.7)
```

Two points inside the method matter more than the rest. In **step 1**, underline the
question word — *why*, *how*, *which*, *what does the writer mean* — because it decides
the shape of your answer. In **step 3**, write the question number in the margin beside
the line that answers it; that mark is what lets you check in step 5 without reading
the passage again.

## 34.4 The question types, and what each one wants

| Type | Typical wording | Rule for answering |
|---|---|---|
| Factual | *Why did the villagers leave?* | The answer is stated. Use the passage's facts, but your own sentence. |
| True / False / Not given | *The scheme was a success. (T/F/NG)* | **True** = the passage says so. **False** = the passage says the opposite. **Not given** = the passage is silent. Nothing else counts. |
| Reference | *What does "it" in the third paragraph refer to?* | Substitute your answer for the word and read the sentence again. If it makes sense, it is right. |
| Vocabulary in context | *Find a word that means "extremely dry".* | Give **one word**, copied exactly, in the form the passage uses. |
| Inference | *Why do you think the writer mentions his father?* | The answer is not stated. Give the answer **and** the line that implies it. |
| Main idea or title | *Suggest a suitable title.* | Three to six words, covering the whole passage, not one paragraph. Not a sentence. |
| Summary or completion | *Complete: The plan failed because ____.* | The passage's own words, fitted grammatically into the gap. |
| Personal response | *Do you agree with the writer? Why?* | Your opinion plus one reason **drawn from the passage**. There is no wrong opinion; there is a wrong reason. |

::: example Worked example 34.1 — reference words
A reference question is free marks if you test your answer by substitution.

> *Farmers in the middle hills have grown maize on terraces for centuries. **It** is a
> crop that tolerates thin soil, and for that reason it has outlasted every attempt to
> replace it.*

**Question:** What does *it* refer to?

A careless answer is *the middle hills*, because that phrase is nearest. Substitute and
test: *The middle hills is a crop that tolerates thin soil* — nonsense. Test the next
candidate: *Maize is a crop that tolerates thin soil* — correct. The answer is **maize**.

Substitution beats proximity. The nearest noun is often not the referent, and the test
takes four seconds.
:::

## 34.5 Worked passage A

::: example Worked passage A — with answers (8 marks)
**Read the passage and answer the questions.**

> Teenagers are often accused of laziness for sleeping late, but the accusation
> misreads the biology. At about the age of thirteen the body clock shifts. The
> hormone that signals the brain to sleep begins to be released roughly two hours
> later than it does in a child or in an adult, so a fifteen-year-old who is wide awake
> at eleven at night is not being difficult; she is being fifteen.
>
> The consequences are not trivial. Sleep is not an interruption of learning but a part
> of it. During the night the brain replays the day's new material and files it, and
> experiments consistently show that a student who sleeps after studying remembers more
> than one who studies for the same length of time and stays awake. Cutting sleep,
> then, does not buy extra study; it spends the study already done.
>
> Most adolescents need between eight and ten hours. Few get them, and the reasons are
> familiar: homework, coaching classes, and a screen that is bright, absorbing and
> within arm's reach. Light in the evening tells the clock that the day is not over,
> and a phone held close to the face is a small, insistent sun.
>
> Some school systems have responded by starting the day later, and where they have,
> attendance has improved and accidents on the way to school have fallen. Such changes
> are expensive and unpopular with parents and bus operators. But the alternative is a
> classroom in which the first period is taught to bodies that, biologically speaking,
> are still asleep.

**Questions**

1. At what age does the body clock begin to shift? <span class="marks">[1]</span>
2. Why does the writer say a fifteen-year-old awake at eleven is "not being difficult"?
   <span class="marks">[1]</span>
3. What does *it* refer to in *"Sleep is not an interruption of learning but a part of
   it"*? <span class="marks">[1]</span>
4. Find a word in the third paragraph that means "holding the attention completely".
   <span class="marks">[1]</span>
5. State whether each is True, False or Not Given.
   (a) Students who sleep after studying remember more than students who stay awake.
   (b) Most adolescents in Nepal sleep fewer than eight hours.
   <span class="marks">[2]</span>
6. Explain the phrase *"a small, insistent sun"*. <span class="marks">[1]</span>
7. Suggest a suitable title for the passage. <span class="marks">[1]</span>

**Answers**

1. At about the age of thirteen.
2. Because at that age the sleep hormone is released about two hours later than in a
   child or an adult, so staying awake is biological, not wilful.
3. *It* refers to **learning**. (Substitute: *Sleep is a part of learning* — sense.
   *A part of sleep* — nonsense.)
4. **Absorbing.** (One word, copied in the form used.)
5. (a) **True** — the passage says experiments consistently show it.
   (b) **Not Given** — the passage says *most adolescents* and *few get them*, but it
   never mentions Nepal. Knowing the answer from your own life is exactly the trap.
6. The phone's screen acts like a small sun held near the face: its light keeps telling
   the body clock that daylight has not ended, so sleep is delayed. *Insistent* shows
   the light will not be ignored.
7. *Why Teenagers Sleep Late* or *Sleep, Screens and the School Day.* Three to six
   words; covers the whole passage; not a sentence.
:::

## 34.6 Worked passage B

::: example Worked passage B — with answers (7 marks)
**Read the passage and answer the questions.**

> The porter who carried our kit to Ghorepani was called Dhan Bahadur, and he was, he
> told us on the first morning, fifty-one. He said it the way a man states a price,
> without complaint and without invitation to admire him, and then he picked up a load
> I could not have lifted to my knee and walked up the hill at a speed that made
> conversation impossible for the rest of us.
>
> At the first tea shop he did not sit with the guides. He drank his tea standing,
> looking back down the valley at the way we had come, and when I asked him what he was
> looking at he said, *my village is behind that ridge; I have not been home since
> Dashain.* Then he put down the glass and lifted the load again before anyone had
> suggested moving.
>
> I have been told since that the trekking season is short and that a porter who rests
> is a porter who is not paid. I did not know it then. What I knew then was only that I
> had been carrying a small day-pack and complaining about it, and that I had asked
> him, that morning, whether the work was hard, and that he had smiled and said it was
> all right.

**Questions**

1. How old was Dhan Bahadur? <span class="marks">[1]</span>
2. What does the comparison "the way a man states a price" tell us about how he spoke?
   <span class="marks">[1]</span>
3. Why did Dhan Bahadur drink his tea standing, do you think? <span class="marks">[2]</span>
4. Find a word in the passage that means "the long ridge of high ground". <span class="marks">[1]</span>
5. What is the writer's feeling in the last paragraph? Support your answer.
   <span class="marks">[2]</span>

**Answers**

1. Fifty-one.
2. It tells us he spoke flatly and factually, as a matter of information — neither
   complaining about his age nor asking to be praised for working at it.
3. Two acceptable lines, each needing evidence. Either: he did not regard the stop as
   his rest, because *a porter who rests is a porter who is not paid* — he stood so as
   to be ready to move, and indeed *lifted the load again before anyone had suggested
   moving*. Or: he did not sit with the guides because he did not see himself as one of
   them; the sentence *he did not sit with the guides* is placed first for that reason.
4. **Ridge.**
5. Shame, or self-reproach — not pity. The evidence is the contrast he draws between
   Dhan Bahadur's load and his own *small day-pack* which he had been *complaining
   about*, and the remembered question *whether the work was hard*, which he now sees
   was a thoughtless thing to ask. The writer never states the feeling; the reader is
   left to draw it, which is why the answer must quote.
:::

## 34.7 The traps, and the checklist

::: caution Six ways marks are lost in Question 1
- **Answering from general knowledge.** *Not Given* means the passage is silent. What
  you happen to know is irrelevant and usually fatal.
- **Copying a whole sentence** for a one-mark factual question. Copying shows you found
  the place; it does not show you understood. Shape the answer yourself.
- **Giving two words** for *find a word which means…*. One word, in the passage's own
  form: if the passage has *absorbing*, do not write *absorb*.
- **Writing a title that is a sentence.** *The passage is about how teenagers sleep* is
  not a title. *Why Teenagers Sleep Late* is.
- **Answering an inference question with a feeling and no evidence.** Half the marks on
  those questions are for the line you point to.
- **Running out of time** because the passage was read three times. Two readings —
  one skim and one close — are all the method allows.
:::

| # | Before you leave Question 1 |
|---|---|
| 1 | Is every question answered — including the 2-mark ones, in full? |
| 2 | Is each answer a sentence of your own, not a copied line? |
| 3 | Did any T/F/NG answer use knowledge from outside the passage? |
| 4 | Is the one-word answer exactly one word, spelt as the passage spells it? |
| 5 | Does each inference answer point to a line? |
| 6 | Is the title three to six words and not a sentence? |
| 7 | Does the number of marks match the length of the answer given? |

The last line is worth dwelling on: **the mark tells you the length.** One mark is one
short sentence. Two marks is two — usually a point and its evidence. Writing a
paragraph for a one-mark question costs you time on Question 6, where it would have
been worth something.

## Chapter summary

- Question 1 is 15 marks on an unseen passage of 350–500 words, with six to nine mixed
  questions, in about 30–35 minutes.
- **Read the questions first.** Then skim for shape, then read closely with a pencil,
  marking where each answer lives.
- **Skimming** finds the shape of a passage; **scanning** finds one item in it. They
  are different speeds for different jobs.
- Each question type has its own rule: substitute-and-test for reference, one exact
  word for vocabulary, evidence-plus-answer for inference, silence-means-Not-Given for
  true/false, three to six words for a title.
- Every answer must be defensible **from the passage**. Outside knowledge is the
  commonest cause of lost marks.
- The number of marks tells you how long the answer should be.

## Practice questions

**Read the passage and answer the questions (15 marks)**

> Plastic was invented to solve a problem of scarcity. Before it, a comb was made of
> horn, a bucket of tin, a bottle of glass — each expensive, each heavy, each made by
> somebody. Plastic made such things cheap enough to be thoughtless about, and being
> thoughtless about them is now the problem.
>
> Nothing about the material itself is wicked. A plastic pipe carries clean water into
> a village for a fraction of the cost of any alternative, and a plastic sheet over a
> seedbed can save a harvest. The difficulty is that we use a material which lasts for
> centuries to make objects intended to last for minutes. A drinking straw is used for
> about four minutes and survives, in one form or another, for perhaps four hundred
> years.
>
> Much of what is thrown away in the hills does not stay there. It is washed into
> streams, carried down to the rivers and eventually to the sea, breaking as it goes
> into fragments too small to collect and small enough to be eaten by fish. Recycling
> helps, but it is often presented as a solution when it is only a delay: most plastics
> can be recycled once or twice, into something of lower quality, and then not again.
>
> The changes that work are unglamorous. Bans on the thinnest carrier bags have reduced
> their use sharply wherever they have been enforced rather than merely announced.
> Refill schemes, deposit charges on bottles and municipal collection that actually
> arrives are worth more than a hundred campaigns asking individuals to feel guilty.
> Guilt is not a waste-management strategy.

1. What were combs, buckets and bottles made of before plastic? <span class="marks">[1]</span>
2. According to the writer, what exactly is "the problem"? <span class="marks">[2]</span>
3. Give two examples from the passage of plastic being genuinely useful. <span class="marks">[2]</span>
4. What does *it* refer to in *"Much of what is thrown away in the hills does not stay
   there. It is washed into streams…"*? <span class="marks">[1]</span>
5. Why does the writer call recycling "only a delay"? <span class="marks">[2]</span>
6. Find a word in the fourth paragraph that means "not exciting or attractive".
   <span class="marks">[1]</span>
7. State whether each is True, False or Not Given.
   (a) A drinking straw takes about four hundred years to break down.
   (b) Nepal has banned plastic carrier bags.
   (c) The writer believes making individuals feel guilty is an effective policy.
   <span class="marks">[3]</span>
8. Explain the last sentence, *"Guilt is not a waste-management strategy."*
   <span class="marks">[2]</span>
9. Suggest a suitable title for the passage. <span class="marks">[1]</span>

::: note Answers
**1.** Horn, tin and glass — a comb of horn, a bucket of tin, a bottle of glass.
**2.** Not plastic itself, but thoughtlessness: because plastic made goods cheap, we
stopped valuing them, and we now make objects meant to last minutes out of a material
that lasts centuries.
**3.** Any two: plastic pipe carries clean water to a village far more cheaply than any
alternative; a plastic sheet over a seedbed can save a harvest.
**4.** *It* refers to **what is thrown away in the hills** (the rubbish, not the hills).
Substitute and test: *the hills are washed into streams* is nonsense.
**5.** Because most plastics can be recycled only once or twice, and each time into
something of lower quality; after that they cannot be recycled again. Recycling
postpones the waste rather than removing it.
**6.** **Unglamorous.**
**7.** (a) **True** — the passage says it survives "for perhaps four hundred years".
(b) **Not Given** — the passage mentions bans on thin carrier bags in general but says
nothing about Nepal. Do not answer from what you know.
(c) **False** — the writer says the opposite: guilt "is not a waste-management strategy"
and practical schemes are "worth more than a hundred campaigns".
**8.** Asking individuals to feel bad about plastic changes nothing by itself; waste is
removed by systems — enforced bans, deposits, refills and collection that works — not
by feelings. The sentence is short and flat on purpose, to end the argument firmly.
**9.** *The Trouble with Plastic*, or *Cheap to Buy, Slow to Vanish*, or *Why Recycling
Is Not Enough*. Three to six words, covering the whole passage.
:::

**Reading skills (1 mark each)**

10. You need to find the year a treaty was signed in a 500-word passage. Are you
    skimming or scanning? <span class="marks">[1]</span>
11. The question is *Find a word from the passage which means "unwilling"*, and the
    passage contains *reluctantly*. What exactly do you write?
    <span class="marks">[1]</span>
12. A statement is the opposite of what the passage says. True, False or Not Given?
    <span class="marks">[1]</span>
13. A statement is something you know to be true but the passage never mentions. True,
    False or Not Given? <span class="marks">[1]</span>
14. How long should an answer to a 2-mark inference question be?
    <span class="marks">[1]</span>
15. What is the first thing you do when Question 1 is turned to?
    <span class="marks">[1]</span>

::: note Answers
**10.** Scanning — you are hunting for one item (four digits), not for meaning.
**11.** **Reluctantly** — copied exactly as the passage has it. *Find a word from the
passage* means the passage's own form; changing it to *reluctant* loses the mark.
**12.** **False.**
**13.** **Not Given.** The passage, not your knowledge, decides.
**14.** Two parts: the answer, and the line in the passage that supports it — about two
sentences.
**15.** Read the questions, underlining the key word in each, before reading the passage.
:::
