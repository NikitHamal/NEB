---
subject: Compulsory English
grade: 11
unit: 33
title: 'Free Writing: Essays, Memoirs and Critical Writing'
hours: 7
area: Writing and Skills
---

Question 6 gives you ten marks and, for the first time in the paper, no format to
copy. You are handed a topic and asked to think. That freedom is why the question is
worth the most marks in the writing section, and why it is the one most often thrown
away. Free writing is not writing whatever comes; it is writing to a shape you chose
before you began. This chapter teaches three of those shapes — the essay, the memoir
and the critical response — and the paragraph that all three are built from.

::: key Five minutes of planning buy you ten marks
An examiner can tell within three lines whether an answer was planned. Spend five
minutes making an outline, twenty writing, and five checking. An outlined answer of
250 words beats an unplanned answer of 400 every time.
:::

## 33.1 What Question 6 asks

The paper sets a topic — sometimes a choice of two or three — and expects **250–300
words** in about **thirty minutes**. The ten marks are usually divided like this:

| What is marked | Marks | What the examiner looks for |
|---|---|---|
| Content and ideas | 4 | On the topic; real points, not padding; developed, not listed |
| Organisation | 3 | Introduction, body paragraphs, conclusion; linked; one idea per paragraph |
| Language | 3 | Grammar, spelling, punctuation, range of vocabulary and sentence type |

Notice that **six of the ten marks have nothing to do with how beautifully you write.**
They are for having something to say and arranging it. That is the part you can
control completely, and it is the part planning fixes.

## 33.2 The paragraph: the unit an essay is built from

A paragraph is not "about five sentences". It is **one idea, stated, supported and
closed**. Every paragraph in a good essay could be reduced to a single sentence
without losing its point — that sentence is the **topic sentence**, and in exam
writing it belongs first.

```figure caption="The shape of a paragraph. The middle sentences exist only to make the first one believable."
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
fig, ax = plt.subplots(figsize=(4.9, 2.7))
ax.axis("off")
rows = [
    ("Topic sentence  —  the one claim the paragraph makes", 0.0, 9.0, ACCENT, "#e8f1f9"),
    ("Support 1  —  a reason, stated plainly", 0.7, 8.3, GRID, "#ffffff"),
    ("Support 2  —  a fact, an example, a figure", 0.7, 8.3, GRID, "#ffffff"),
    ("Support 3  —  the strongest point, kept for last", 0.7, 8.3, GRID, "#ffffff"),
    ("Closing sentence  —  the claim, now earned", INK, 9.0, INK, "#eceef1"),
]
y = 5.25
for i, (text, x0, w, edge, face) in enumerate(rows):
    if i == 4:
        x0, w, edge, face = 0.0, 9.0, INK, "#eceef1"
    ax.add_patch(mpatches.FancyBboxPatch((x0, y), w, 0.82,
                 boxstyle="round,pad=0.0,rounding_size=0.10",
                 linewidth=1.1, edgecolor=edge, facecolor=face))
    ax.text(x0 + 0.28, y + 0.41, text, ha="left", va="center",
            fontsize=7.0, color=INK)
    y -= 1.06
ax.annotate("", xy=(-0.35, 1.02), xytext=(-0.35, 5.98),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=1.0))
ax.text(-0.62, 3.5, "order on the page", rotation=90, ha="center", va="center",
        fontsize=6.6, color=MUTED)
ax.set_xlim(-1.1, 9.3)
ax.set_ylim(0.85, 6.35)
```
Two faults kill paragraphs. **Loss of unity** — a sentence that belongs to a different
idea wanders in. **Loss of coherence** — the sentences are all on topic but in no
order, so the reader has to do the arranging. Fix unity by deleting; fix coherence by
numbering your supports before you write them.

## 33.3 The shape of a whole essay

An essay is a paragraph enlarged. It opens wide, narrows to a single claim, defends
that claim one paragraph at a time, and opens out again at the end.

```figure caption="The funnel shape of an essay: wide, narrow, narrow, wide. The thesis sits at the point of the first funnel."
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
fig, ax = plt.subplots(figsize=(4.9, 3.3))
ax.axis("off")
intro = mpatches.Polygon([(0.5, 9.5), (9.5, 9.5), (7.0, 7.1), (3.0, 7.1)],
                         closed=True, facecolor="#e8f1f9", edgecolor=ACCENT, linewidth=1.2)
conc = mpatches.Polygon([(3.0, 2.3), (7.0, 2.3), (9.5, 0.2), (0.5, 0.2)],
                        closed=True, facecolor="#eceef1", edgecolor=INK, linewidth=1.2)
ax.add_patch(intro)
ax.add_patch(conc)
ax.text(5.0, 8.85, "INTRODUCTION", ha="center", va="center", fontsize=7.2, color=ACCENT)
ax.text(5.0, 8.20, "a general opening, narrowing", ha="center", va="center",
        fontsize=6.6, color=INK)
ax.text(5.0, 7.62, "to one sentence: the thesis", ha="center", va="center",
        fontsize=6.6, color=INK)
bodies = [("Body 1  —  first point, then evidence", 5.55),
          ("Body 2  —  second point, then evidence", 4.30),
          ("Body 3  —  the other side, then your answer", 3.05)]
for text, y in bodies:
    ax.add_patch(mpatches.FancyBboxPatch((1.6, y), 6.8, 0.95,
                 boxstyle="round,pad=0.0,rounding_size=0.10",
                 linewidth=1.1, edgecolor=GRID, facecolor="#ffffff"))
    ax.text(5.0, y + 0.47, text, ha="center", va="center", fontsize=6.7, color=INK)
ax.text(5.0, 1.62, "CONCLUSION", ha="center", va="center", fontsize=7.2, color=INK)
ax.text(5.0, 1.00, "the thesis again, then a wider", ha="center", va="center",
        fontsize=6.6, color=INK)
ax.text(5.0, 0.48, "comment. No new point here.", ha="center", va="center",
        fontsize=6.6, color=INK)
for y0, y1 in [(7.05, 6.58), (5.48, 5.30), (4.23, 4.05), (2.98, 2.38)]:
    ax.annotate("", xy=(5.0, y1), xytext=(5.0, y0),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=0.9))
ax.set_xlim(0.2, 9.8)
ax.set_ylim(0.0, 9.9)
```
The **thesis statement** is the single sentence that says what the whole essay will
argue. It is not the topic. *Load-shedding* is a topic; *Load-shedding did more damage
to Nepal's small industries than to its households* is a thesis. Put it at the end of
your first paragraph and every later paragraph has a job: defend it.

A workable plan for 250–300 words is **five paragraphs**: introduction (40 words),
three body paragraphs (60 words each), conclusion (40 words). Write the plan as six
words, not six sentences:

> *hook — thesis / cost / jobs / counter: subsidy / restate — call*

## 33.4 Four kinds of essay, and how each is organised

| Kind | It does this | Order | Typical language |
|---|---|---|---|
| **Narrative** | tells what happened | time order | past tense, *then, later, at last* |
| **Descriptive** | makes the reader see a place or person | space order, or general to detail | present or past, adjectives, the five senses |
| **Expository** | explains, compares, or gives causes | logical: cause then effect, or point by point | present simple, *because, therefore, whereas* |
| **Argumentative** | proves a claim and answers objections | claim, reasons, counter-argument, answer | *should, must, arguably, however, it follows that* |

Read the wording of the question to find which is wanted. *Describe* asks for the
second, *Explain why* for the third, *Do you agree?* for the fourth. Writing a
narrative when the paper asked you to argue costs content marks however good the
story is.

::: example Model answer 33.1 — an argumentative essay (10 marks)
**Question:** *Should mobile phones be allowed in schools? Write an essay of about 250
words giving your opinion.*

**Mobile Phones in School**

Ten years ago a mobile phone in a school bag was unusual; today it is almost the rule.
Teachers confiscate them, parents insist their children carry them, and the same
argument comes round every year. In my view schools should allow phones on the
premises but forbid their use inside the classroom, because a total ban answers a real
problem in the wrong way.

The first reason is safety. Many students in our hills travel an hour or more to
school, on roads that close after heavy rain and during strikes. A parent who cannot
reach a child on such a day is helpless. A phone switched off in a bag costs the
school nothing and gives a family a great deal.

The second reason is that a phone is a library. A student who cannot afford a
dictionary can carry one; past papers, recorded lectures and news in English are all
within reach. Used for twenty minutes with a purpose, the device teaches more than it
distracts.

Against this it is argued, fairly, that phones invite cheating, distraction and
bullying. These are genuine harms. But a ban does not remove them; it moves them to
the corridor and the toilet, where no teacher is watching. A clear rule — phones off
and out of sight from the first bell to the last, with the penalty known in advance —
protects lessons without wasting what the device can do.

Schools exist to prepare students for a world in which these machines are everywhere.
Teaching students when not to use a phone is a better lesson than pretending the phone
does not exist.

*(288 words)*
:::

## 33.5 The memoir

A **memoir** is a true piece of writing about a remembered experience and what it came
to mean. It is not an autobiography: an autobiography covers a life, a memoir covers
one afternoon. Its authority comes from detail only you could know.

Five features mark a memoir:

1. **First person and past tense.** *I was eleven. The bus had already gone.*
2. **A narrow slice of time** — a day, an hour, a single conversation.
3. **Concrete sensory detail** instead of summary. Not *it was frightening*, but *the
   handle was cold and my fingers would not close on it*.
4. **A turning point** — the moment after which something was different.
5. **Reflection at the end** — the grown writer, looking back, saying what it meant.
   This last paragraph is what separates a memoir from a story.

::: example Model answer 33.2 — a memoir (10 marks)
**Question:** *Write a memoir of about 250 words about an experience that changed the
way you think.*

**My Grandmother's Radio**

The radio in my grandmother's room was the size of a brick and the colour of weak tea.
It had one dial, and the dial had a crack in it shaped like a river. Every evening at
seven she turned it on, and every evening at seven the room went quiet, even the
cousins, even me.

I was nine and I thought the ritual was silly. There was a television downstairs with
colour in it. I told her so one evening, standing in the doorway with my arms folded,
and I remember being rather pleased with the sentence.

She did not argue. She moved along the bed and patted the space beside her, and I sat
because I was nine and it was easier to sit than to keep standing. The news came on.
There had been a landslide above Sindhupalchok. The reader said the name of a village,
and my grandmother's hand went still on the blanket, and she said, very quietly, *your
grandfather walked through there in 2018*.

I did not understand what I was being told. I understood only that the little brown
box was not entertainment; it was how she kept the map of her life in one piece.

I have a phone now that can play a thousand stations, and I use it for almost nothing.
What that evening taught me is that a thing is worth what it carries, not what it
costs — and that the quickest way to miss what somebody loves is to compare it with
something newer.

*(263 words)*
:::

## 33.6 Critical writing

**Critical** does not mean hostile. To write critically about a text is to make a
judgement and then show, from the text, why the judgement is fair. The commonest
failure is to retell the plot: a summary earns almost nothing, because it proves only
that you read the story.

A reliable five-part shape for a critical response:

| Part | Length | What goes in |
|---|---|---|
| Introduction | 2 sentences | Title, author, form, and your overall judgement |
| Summary | 2–3 sentences | Only what a reader needs to follow you — no more |
| Analysis | 2 paragraphs | Theme, character, structure, style, symbol — with short quotations |
| Evaluation | 1 paragraph | What works and what does not, each with a reason |
| Conclusion | 1–2 sentences | The judgement again, in one line |

Two habits make the difference. **Quote briefly and exactly** — four or five words
inside quotation marks, not four lines. And after every quotation, write one sentence
beginning *This shows…* or *The effect is…*; evidence without comment is not analysis.

::: example Model answer 33.3 — a critical response (10 marks)
**Question:** *Write a critical appreciation of Oscar Wilde's "The Selfish Giant".*

Oscar Wilde's "The Selfish Giant" is a short fairy tale that uses the simplest
machinery of the form — a garden, a wall, a child — to make a serious claim about
selfishness and its cure. It is a slight story that carries a surprising weight.

The Giant returns after seven years, finds children playing in his garden, and walls
them out with the notice "TRESPASSERS WILL BE PROSECUTED". Spring never comes to the
garden again until the children creep back through a gap, and the Giant, watching a
small boy who cannot reach the branches, knocks the wall down himself.

Wilde's chief device is the personification of the seasons. Snow, Frost, the North
Wind and the Hail move into the garden like tenants, and the reader understands
without being told that the winter is the Giant's own. The wall is equally plain in
its meaning, and the plainness is deliberate: this is a fable, and a fable wants its
symbol visible.

The weakness of the story is its ending. The boy's return, with "the wounds of Love"
on his hands and feet, converts a moral tale into a religious one very abruptly, and
some readers find the shift sentimental. Yet the form protects Wilde. A fairy tale is
allowed a miracle, and the earlier writing has earned this one.

"The Selfish Giant" is therefore best read not as a children's story with a moral
attached, but as a moral argument that has chosen the shape of a children's story
because that shape can say hard things gently.

*(268 words)*
:::

## 33.7 Language that lifts a free-writing answer

**Link your paragraphs.** A cohesive device at the start of a body paragraph tells the
examiner you know what the paragraph is doing.

| Job | Useful expressions |
|---|---|
| Adding | moreover, in addition, what is more, not only … but also |
| Contrasting | however, on the other hand, nevertheless, whereas |
| Giving cause | because, since, owing to, as a result, consequently |
| Giving an example | for instance, to take one example, such as |
| Conceding | admittedly, it is true that, granted that |
| Concluding | on balance, in short, for these reasons |

**Hedge your claims.** *Every Nepali student wastes time on the internet* is easy to
disprove and therefore weak. *Many students appear to lose more time online than they
intend* cannot be knocked down. Words that do this work: *many, most, tends to, often,
appears to, arguably, in general*.

**Vary your sentences.** Three long sentences in a row tire a reader; three short ones
sound like a list. Follow a long sentence with a short one. It works.

::: caution Habits that cost marks every year
- Opening with *In this modern era of science and technology* — say something about
  *your* topic instead.
- Closing with *Last but not the least* — write *Finally* or, better, name the point.
- *~~Nowadays~~* three times in one essay. Use it once or not at all.
- Listing without developing: *There are many advantages. It is cheap. It is fast. It
  is easy.* Four sentences, one mark. Take one advantage and prove it.
- New material in the conclusion. If it matters, it belongs in the body.
- *~~I think~~, ~~I think~~, ~~I think~~.* The essay is yours; the examiner knows the
  opinion is yours. Say *I believe* once, in the thesis.
- Writing 500 words because more looks better. It does not — it multiplies the errors
  in the language mark and leaves no time to check.
:::

::: tip One quotation, one proverb — no more
A well-chosen line from a text or a proverb can sharpen a conclusion. Two of them look
like decoration, and a misquoted one costs more than it gains. If you are not certain
of the words, paraphrase instead.
:::

## 33.8 Checking your own answer

Give the last five minutes to this list. Each line is a mark somebody lost last year.

| # | Check |
|---|---|
| 1 | Does the answer have a **title**? |
| 2 | Is there a **thesis sentence** at the end of paragraph 1? |
| 3 | Does every paragraph begin with its own topic sentence? |
| 4 | Is there **one idea per paragraph** — nothing wandering in? |
| 5 | Have I answered the question actually asked (*describe*, *explain*, *do you agree*)? |
| 6 | Is there a counter-argument, if the question asked for an opinion? |
| 7 | Does the conclusion add no new point? |
| 8 | Subject–verb agreement, articles and tense consistent throughout? |
| 9 | Capital letters, full stops, and paragraph breaks clearly visible? |
| 10 | Roughly 250–300 words — not 150, not 500? |

## Chapter summary

- Question 6 is worth **10 marks**: about 4 for content, 3 for organisation, 3 for
  language. Plan five minutes, write twenty, check five.
- A **paragraph** is one idea: topic sentence, supports in a chosen order, closing
  sentence. Unity and coherence are what the organisation mark measures.
- An **essay** is a funnel: general opening, a one-sentence **thesis**, body paragraphs
  that defend it, a conclusion that widens out and adds nothing new.
- The four kinds — narrative, descriptive, expository, argumentative — are distinguished
  by their **order**. Take the kind from the wording of the question.
- A **memoir** is one remembered slice of time in the first person, built on concrete
  detail, turning on a single moment, and ending with reflection on what it meant.
- **Critical writing** is judgement plus evidence. Summarise in three sentences at most;
  quote briefly; after every quotation, say what it shows.
- Link paragraphs with cohesive devices, hedge large claims, vary sentence length, and
  avoid the stock openings and closings every examiner has read a thousand times.

## Practice questions

**Free writing (10 marks each)**

1. *Should Grade 11 students be required to do community work?* Write an essay of about
   250 words giving your opinion and answering one objection to it.
   <span class="marks">[10]</span>
2. Write a memoir of about 250 words beginning *I had never seen my father lose his
   temper before that afternoon.* <span class="marks">[10]</span>
3. Write a critical appreciation of about 250 words of any one poem you have studied
   this year. <span class="marks">[10]</span>

::: note Model answers
**1.** Full model answer.

**Work That Cannot Be Marked**

Every Grade 11 student in the country is examined on Nepali, English, mathematics and
a science. Not one is examined on whether they are of any use to the street they live
on. I believe community work should be a requirement of the grade — not for the credit
it would carry, but for the one thing it teaches that no subject on the timetable can.

The first argument is simply that the work needs doing. Blocked drains before the
monsoon, a school library with no catalogue, older neighbours who cannot reach a health
post: these are small tasks that fail for want of hands, and a class of forty has
eighty of them.

The second argument matters more. A student who spends four Saturdays helping in a
ward office learns what a municipality actually does, how slowly a form moves, and what
it costs somebody to wait. That is civic education, and it cannot be delivered from a
textbook.

The usual objection is time. Grade 11 is a demanding year, and adding an obligation to
an overloaded student is cruel. The objection is fair, and the answer is to keep the
requirement small — twenty hours in a year, counted honestly, not a weekly burden — and
to let students choose the work.

Requiring community work will not, by itself, produce better citizens. But it puts every
student once inside a problem that is not their own, and almost nobody comes back out
unchanged.

*(246 words)*

**2.** Plan, then write to it. Setting and the ordinary day before the change (40 words)
— the afternoon itself, told slowly, with two or three physical details you can see now:
what was in his hands, what the room smelt of, what somebody said (110 words) — the
moment his temper broke, in short sentences (50 words) — reflection: what you understood
about him, or about adults, that you had not understood at breakfast (50 words). Keep
the whole thing to one afternoon; resist explaining his life.

**3.** Use the five-part shape of §33.6. Introduction: poet, title, form, and your
judgement in one clause. Summary: what the poem says, in two sentences. Analysis:
choose **two** features only — say, the central image and the movement of the last
stanza — and support each with a quotation of four or five words followed by a sentence
beginning *This shows…*. Evaluation: one thing that works and one that is open to
objection, each with a reason. Conclusion: your judgement in a single line. Do not
paraphrase the poem stanza by stanza; that is summary, not appreciation.
:::

**Organisation and paragraphing (1 mark each)**

4. Which sentence is the topic sentence? *(a) Water was rationed to two hours a day.
   (b) Last summer was the hardest our town has had. (c) The taps ran dry in Chaitra.*
   <span class="marks">[1]</span>
5. *Tourism is our largest earner.* Turn this topic into a thesis statement.
   <span class="marks">[1]</span>
6. Which kind of essay does *Explain why so many young Nepalis go abroad to work* ask
   for? <span class="marks">[1]</span>
7. Which kind does *Describe the busiest street in your town* ask for?
   <span class="marks">[1]</span>
8. Name the one thing a conclusion must never contain. <span class="marks">[1]</span>
9. What separates a memoir from a short story? <span class="marks">[1]</span>
10. A critical response spends six of its twelve sentences retelling the plot. What
    mark is at risk, and why? <span class="marks">[1]</span>
11. Correct the register: *Last but not the least, phones are also a big headache for
    teachers.* <span class="marks">[1]</span>

::: note Answers
**4.** (b) — it is the general claim; (a) and (c) are the evidence for it.
**5.** For example: *Tourism is our largest earner, but the money leaves the districts
that produce it.* A thesis must make a claim that could be argued against.
**6.** Expository — *explain why* asks for causes, not opinion.
**7.** Descriptive — arranged in space order, built on sensory detail.
**8.** A new point or new evidence. The conclusion restates and widens; it does not add.
**9.** A memoir is true and ends with the writer's reflection on what the experience
meant; a story is invented and ends with the event.
**10.** The content mark. Summary shows only that the text was read; the marks are for
judgement supported by evidence.
**11.** *~~Last but not the least~~ → **Finally**, phones ~~are also~~ → **create** a
serious difficulty for teachers.* The stock phrase and the vague *headache* both belong
to speech, not to an essay.
:::
