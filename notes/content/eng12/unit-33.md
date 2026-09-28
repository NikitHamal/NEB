---
subject: Compulsory English
grade: 12
unit: 33
title: 'Free Writing: Essays and Memoirs'
hours: 7
area: Writing and Skills
---

Question 6 gives you ten marks and a choice of topics, and then leaves you alone. That
freedom is exactly what makes it the question most often wasted. A candidate who
begins writing the moment the topic is chosen produces four paragraphs that say the
same thing four times; a candidate who spends four minutes on a plan produces four
paragraphs that each move the argument one step further. The planning is the essay.

::: key An essay answers a question; a memoir answers a memory
If the topic is a question or a statement — *Do you agree?*, *Discuss* — you owe the
examiner a **position** and reasons for it. If the topic is *An unforgettable day*,
*The person who shaped me*, you owe him a **scene** and what you now understand about
it. Deciding which of the two you have been given is the first minute's work.
:::

## 33.1 What Question 6 asks, and how the ten marks fall

| What is credited | Marks | What that means |
|---|---|---|
| **Content** | 4 | A clear position or a clear centre; ideas developed, not merely listed; specific detail |
| **Organisation** | 3 | Introduction, three or four body paragraphs, conclusion; each paragraph on one idea; visible links |
| **Language** | 3 | Range of sentence types and vocabulary; accurate tenses, articles, punctuation |

**Length 300–400 words. Time about thirty minutes:** four to plan, twenty-two to write,
four to check. Four hundred careful words beat six hundred careless ones, because the
language mark is a mark for accuracy, not for quantity.

## 33.2 The five kinds of essay

| Kind | The topic sounds like | What the examiner wants | Dominant tense |
|---|---|---|---|
| **Argumentative** | *Do you agree? · Should Nepal …?* | a stated position, reasons, and one honest counter-argument answered | present simple |
| **Expository** | *Explain why … · Discuss the causes of …* | causes or stages set out in order, no opinion | present simple |
| **Descriptive** | *A monsoon morning in my village* | one place, one hour, and the five senses | past or present |
| **Narrative** | *An incident that changed me* | one event, told in scenes, with a turning point | past simple |
| **Reflective** | *What failure taught me* | an experience **plus** the thought it produced | past for the event, present for the thought |

A memoir is a narrative essay with the reflection built in. Grade 12 asks for it
often, and Section 33.7 treats it separately.

## 33.3 The thesis statement

A thesis is one sentence, usually the last of the introduction, that states your
position **and** signposts your reasons. It is what an examiner looks for before
anything else.

| Not a thesis | A thesis |
|---|---|
| *In this essay I will discuss examinations.* (announcement) | *Examinations measure memory rather than understanding, and the fear they create does more damage to learning than the discipline they impose is worth.* |
| *Examinations are a very important topic.* (no position) | |
| *Examinations are good and bad.* (no position) | |

Build it with a template until you no longer need one:

- **Position + because**: *Nepal should make cycle lanes compulsory in every
  municipality, because the cost is small, the health gain is large and the alternative
  is another decade of unbreathable air.*
- **Although + main clause**: *Although foreign employment has kept many families
  fed, it has emptied our villages of exactly the people who could have rebuilt them.*

::: tip Test your thesis in one move
Can a reasonable person disagree with it? If not, it is a fact, not a thesis, and the
essay has nothing to prove. *Water is necessary for life* cannot be argued with;
*bottled water should be taxed* can.
:::

## 33.4 The shape of the whole essay

```figure caption="The hourglass. The introduction narrows from a general opening to the thesis; the conclusion widens from the restated thesis back out to the world. The body is the straight part, and it is the longest."
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
fig, ax = plt.subplots(figsize=(5.0, 4.4))
ax.axis("off")
ax.add_patch(mpatches.Polygon([(0.55, 9.4), (5.85, 9.4), (4.85, 7.35), (1.55, 7.35)],
             closed=True, facecolor="#e8f1f9", edgecolor=ACCENT, linewidth=1.1))
ax.add_patch(mpatches.Rectangle((1.55, 2.55), 3.30, 4.62,
             facecolor="#ffffff", edgecolor=ACCENT, linewidth=1.1))
ax.add_patch(mpatches.Polygon([(1.55, 2.37), (4.85, 2.37), (5.85, 0.32), (0.55, 0.32)],
             closed=True, facecolor="#e8f1f9", edgecolor=ACCENT, linewidth=1.1))
ax.text(3.20, 8.85, "General opening", ha="center", fontsize=6.6, color=INK)
ax.text(3.20, 8.35, "Narrow to the issue", ha="center", fontsize=6.3, color=MUTED)
ax.text(3.20, 7.72, "THESIS", ha="center", fontsize=6.8, color=ACCENT)
for y, t in [(6.55, "Reason 1"), (5.45, "Reason 2"),
             (4.35, "Reason 3"), (3.20, "Counter-argument,\nanswered")]:
    ax.text(3.20, y, t, ha="center", va="center", fontsize=6.3,
            color=INK, linespacing=1.5)
    if y > 3.4:
        ax.plot([1.95, 4.45], [y - 0.42, y - 0.42], lw=0.7, color=GRID)
ax.text(3.20, 1.82, "Restated in new words", ha="center", fontsize=6.3, color=ACCENT)
ax.text(3.20, 1.33, "What follows from it", ha="center", fontsize=6.3, color=MUTED)
ax.text(3.20, 0.76, "A last line worth remembering", ha="center", fontsize=6.3, color=INK)
def side(y, t):
    ax.plot([6.05, 6.45], [y, y], lw=0.8, color=GRID)
    ax.text(6.58, y, t, fontsize=6.2, color=MUTED, ha="left", va="center")
side(8.38, "Introduction  ·  50–60 words")
side(4.85, "Body  ·  200–260 words")
side(1.35, "Conclusion  ·  50–60 words")
ax.set_xlim(0.2, 11.5)
ax.set_ylim(0.1, 9.7)
```

**Each body paragraph is built the same way.** Learn the four moves as a habit and you
will never again write a paragraph that wanders.

```figure caption="The four moves of a body paragraph. Most candidates write the first two and stop; the third is where the content marks are, and the fourth is where the organisation marks are."
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
fig, ax = plt.subplots(figsize=(5.0, 3.1))
ax.axis("off")
rows = [("Point", "The topic sentence. One idea, stated flatly.",
         "\"Examinations reward memory, not understanding.\""),
        ("Evidence", "An example, a fact, a case, a comparison.",
         "\"A student can score full marks on a definition he cannot use.\""),
        ("Explain", "Why the evidence proves the point.",
         "\"What is tested, then, is recall under pressure.\""),
        ("Link", "A bridge to the next paragraph.",
         "\"The cost of that pressure is the next question.\"")]
y = 7.6
for name, what, sample in rows:
    ax.add_patch(mpatches.FancyBboxPatch((1.25, y), 8.3, 1.62,
                 boxstyle="round,pad=0.0,rounding_size=0.10",
                 linewidth=1.0, edgecolor=GRID, facecolor="#ffffff"))
    ax.add_patch(mpatches.Rectangle((1.25, y), 0.14, 1.62,
                 facecolor=ACCENT, edgecolor="none"))
    ax.text(1.62, y + 1.12, name + " — " + what, fontsize=6.4, color=INK,
            ha="left", va="center")
    ax.text(1.62, y + 0.47, sample, fontsize=6.0, color=MUTED,
            ha="left", va="center", style="italic")
    y -= 2.02
for yy in [7.42, 5.40, 3.38]:
    ax.annotate("", xy=(5.4, yy - 0.38), xytext=(5.4, yy),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.9,
                                mutation_scale=8))
ax.set_xlim(1.0, 9.8)
ax.set_ylim(1.3, 9.4)
```

**Cohesion** is what turns four paragraphs into one essay. Vary the connectives; the
same *moreover* three times is itself an error of style.

| Job | Choose from |
|---|---|
| adding | furthermore, what is more, in addition, equally important |
| contrasting | however, by contrast, on the other hand, and yet, admittedly |
| causing | consequently, as a result, which is why, hence |
| giving an example | for instance, take the case of, consider |
| conceding then turning | granted that …, it is true that … but |
| concluding | in short, on balance, the upshot is |

## 33.5 Openings and endings that are not clichés

::: caution Six openings an examiner has already read a thousand times
*Since time immemorial…* · *Man is a social animal…* · *In today's modern world of
science and technology…* · *The dictionary defines education as…* · *Every coin has two
sides.* · *In this essay I am going to discuss…*
Each of them wastes the first sentence, which is the only sentence guaranteed to be
read with full attention.
:::

Replace them with one of these four:

| Opening | Example |
|---|---|
| **A concrete scene** | *At six in the morning the corridor outside the examination hall smells of fear and hair oil.* |
| **A number or a fact** | *A Grade 12 student sits roughly thirty formal tests in two years.* |
| **A contradiction** | *We say we value understanding, and then we measure it with a stopwatch.* |
| **A question you will answer** | *What exactly is an examination for?* |

Conclusions fail in the opposite way: they either repeat the introduction word for word
or introduce a brand-new idea. A good conclusion does three small things — restates the
position **in different words**, says what should follow from it, and ends on a short
sentence. Never begin one with *Last but not the least*; never end one with *So, this
is my essay.*

::: example Model answer 33.1 — an argumentative essay
**Question.** *Examinations do more harm than good.* Do you agree? Write an essay in
about 350 words. <span class="marks">[10]</span>

**Model answer — Thirty Tests and One Question**

We say that we value understanding, and then we measure it with a stopwatch. For three
hours in Chaitra, a student's two years are converted into a grade, and everything he
has learnt that cannot be written down in that time is treated as though it did not
happen. Examinations are not useless — a country of thirty million needs some fair way
of deciding who enters which college — but as they are set at present they measure
memory rather than understanding, and the fear they produce costs more learning than
their discipline is worth.

The first charge against them is that they test recall, not thought. A student can
score full marks on the definition of photosynthesis and still be unable to explain why
a plant on a dark window sill turns yellow. Our question papers reward the sentence
that has been memorised in the exact words of the textbook, and our answer keys
frequently punish the student who puts the same idea in his own. What is being
measured, then, is speed of recall under pressure — a real skill, but a narrow one, and
not the one the syllabus claims to teach.

The second charge is heavier. Fear is a poor teacher. In the six months before the
board examination, learning in most classrooms stops and revision begins: past papers,
guess papers, model sets. Curiosity is postponed because curiosity is not on the
marking scheme. A student who might have spent an evening taking a radio apart spends
it instead copying the ten most probable questions, and the habit of asking why quietly
dies.

It must be granted that examinations do some good. They impose a deadline, and most of
us work only to deadlines. They are also, for all their faults, blind: the examiner in
Kathmandu does not know whose son is writing. That fairness is worth defending, and
nobody who argues against examinations should pretend otherwise.

But fairness is an argument for examinations of some kind, not for these. A paper that
asked students to apply an idea to a situation they had never seen would be just as
blind, just as fair, and would test something worth testing. Until we set that paper,
we shall go on grading memory and calling it education.

**Why it scores.** The thesis is in the last sentence of the introduction and concedes
something before it argues; each body paragraph opens with a flat topic sentence and
then earns it with a concrete case; the fourth paragraph gives the other side properly
before answering it; the conclusion proposes a remedy instead of repeating paragraph
one; and the sentence lengths vary from three words to thirty.
:::

## 33.6 The expository essay

An expository essay explains rather than argues. It is not permitted an opinion, and
its organisation must therefore come from the material itself: causes and effects,
stages in order, kinds and sub-kinds, or problem and solution. Announce that
organisation in the introduction — *three things drive this* — and then keep to it.

::: example Model answer 33.2 — an expository essay
**Question.** Explain why so many young people leave the hill villages of Nepal, and
what a village loses when they go. Write about 350 words. <span class="marks">[10]</span>

**Model answer — What the Hills Send Away**

Walk through a hill village in Gandaki at midday and you will meet children, mothers
and the very old, and almost nobody between eighteen and forty-five. The absence is not
an accident. Three forces pull the young out of these villages — work, schooling and
the shape of the land itself — and what is left behind loses more than a pair of hands.

Work is the first and the plainest. A terraced field of eight ropanis will feed a
family for part of the year and pay for almost nothing else: no fees, no medicines, no
roof of corrugated sheet. Wages in the Gulf, in Malaysia or simply in Pokhara are
earned in cash, every month, and cash is what a household needs the moment it wants
anything the village cannot grow. A young man does not leave because he dislikes
farming; he leaves because farming has no salary.

Schooling is the second. Primary classes exist in nearly every ward, but the campus
that offers Grade 11 is often three hours away on foot. Once a student boards in the
district headquarters at sixteen, the village becomes a place he visits in Dashain.
Education, which the village paid for, has taught him a way of living the village
cannot supply.

The third force is the land. Hill soil is thin, the plots are small and divided again
at every inheritance, and a single monsoon landslide can remove a year's work in an
afternoon. Where the road has not come, the cost of carrying anything to market eats
the profit of selling it.

What a village loses is not only labour. It loses the age group that repairs trails,
carries the sick to the health post and argues in the ward assembly. Fields fall out of
cultivation and the forest creeps back over them; festivals thin; a school with eleven
pupils closes and the next family leaves because the school has closed. The money sent
home builds better houses, but the houses stand empty most of the year.

The hills, in short, are exporting exactly the people who could have rebuilt them, and
each departure makes the next one easier.

**Why it scores.** The introduction names the three causes and so promises a shape; each
body paragraph takes one cause and supports it with a concrete detail (eight ropanis,
three hours on foot, eleven pupils); the fourth paragraph turns from causes to
consequences as the question required; there is no opinion anywhere; and the closing
sentence states a pattern rather than a preference.
:::

## 33.7 The memoir

A memoir is not an autobiography. An autobiography covers a life; a memoir takes **one
remembered episode** and tells it so that the reader understands why it is still
remembered. Five features are expected at Grade 12:

1. **First person, past tense** — *I*, and events that are over.
2. **A single, narrow slice of time** — a morning, a journey, one afternoon.
3. **Sensory detail**: what could be seen, heard, smelt, touched. This is where a
   memoir earns its content marks.
4. **The double voice** — the person it happened to, and the older person telling it.
   The second voice is what makes it a memoir and not a story.
5. **A turning point and a reflection**: something changed, and you now know what.

```figure caption="The double voice of a memoir. The lower track is the episode as it happened; the upper track is the writer, years later, understanding it. A memoir keeps crossing between the two."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1, 2.9))
ax.axis("off")
ax.text(1.0, 8.15, "NOW \u2014 the writer looking back, present tense",
        fontsize=6.4, color=ACCENT, ha="left")
ax.plot([1.0, 9.8], [6.4, 6.4], lw=1.4, color=ACCENT)
for x, t in [(3.0, "\"I did not know\nyet that\u2026\""),
             (7.8, "\"What I remember\nis not the fear\u2026\"")]:
    ax.plot([x], [6.4], marker="o", ms=5.0, color=ACCENT)
    ax.text(x, 6.68, t, fontsize=6.0, color=INK, ha="center", va="bottom",
            linespacing=1.5, style="italic")
    ax.plot([x, x], [6.16, 2.86], lw=0.8, color=GRID, linestyle=(0, (3, 3)))
ax.plot([1.0, 9.8], [2.6, 2.6], lw=1.4, color=MUTED)
for x, t in [(1.7, "the bus\nnever came"), (4.3, "the walk\nbegins"),
             (6.6, "the lift from\na milk truck"), (9.0, "the hall,\nlate")]:
    ax.plot([x], [2.6], marker="o", ms=5.0, color=MUTED)
    ax.text(x, 2.88, t, fontsize=6.0, color=INK, ha="center", va="bottom",
            linespacing=1.5)
ax.text(1.0, 1.95, "THEN \u2014 the episode, past tense",
        fontsize=6.4, color=MUTED, ha="left")
ax.set_xlim(0.8, 10.2)
ax.set_ylim(1.6, 8.6)
```

::: example Model answer 33.3 — a memoir
**Question.** Write a memoir of an incident from your school days that you still think
about. Write in about 350 words. <span class="marks">[10]</span>

**Model answer — The Morning the Bus Did Not Come**

I was fifteen, and the bus that took us from Bhanu to the examination centre at Damauli
left the chautari at half past five. On the morning of the compulsory mathematics paper
I was there at twenty past, with my admit card in a polythene bag inside my shirt
because the sky had that low grey look that means rain before nine. At six o'clock the
bus had not come. At half past six the tea-shop man said, without looking up from his
kettle, that the drivers were on strike.

I remember exactly three things about the hour that followed: the smell of wet dust as
the first drops came down, the sound of my own breathing, and a boy from the year below
me crying quietly by the milestone. I remember no fear at all, which surprises me now.
There was simply a distance — nineteen kilometres — and three hours in which to cover
it, and it did not occur to me that the two might not fit together.

So I walked. For the first hour I walked fast and alone; then two other boys caught up
and we walked together without saying much. At Byas a milk truck stopped of its own
accord, and the driver, who asked nothing and was told nothing, moved four steel cans
to make room for us on the tray. We sat among them with the rain coming sideways, and I
held the polythene bag against my chest with both hands the whole way.

I reached the hall at twenty-five past nine, twenty-five minutes late, soaked to the
knee. The invigilator looked at my admit card, looked at my trousers, and said nothing.
He gave me the paper. I scored 71.

What I think about now is not the walk, and not the mark. It is the milk-truck driver,
whose name I never asked and whose face I could not describe. He lost twenty minutes of
his morning for three boys he would never see again, and he did it without the smallest
suggestion that he was doing anything. I have been trying, ever since, to be somebody's
milk truck.

**Why it scores.** One morning, not a whole school career; the detail is physical (the
polythene bag, the steel cans, the rain sideways) rather than emotional; the older
voice appears twice — *which surprises me now*, *What I think about now* — and the last
line turns a private memory into something a reader can use.
:::

## 33.8 Marking checklist for Question 6

| | Check | Mark at risk |
|---|---|---|
| 1 | Is my **position** or **centre** in one sentence at the end of paragraph one? | Content |
| 2 | Have I given the other side once, and answered it? | Content |
| 3 | Does every body paragraph begin with a topic sentence? | Organisation |
| 4 | Does every body paragraph contain one concrete example, number or case? | Content |
| 5 | Is the conclusion in **different words** from the introduction? | Organisation |
| 6 | Have I introduced a new idea in the conclusion? Remove it. | Organisation |
| 7 | Any *since time immemorial*, *last but not the least*, *every coin has two sides*? | Language |
| 8 | Have I used the same connective twice? Change one. | Language |
| 9 | For a memoir: is it one episode, in the past, with sensory detail? | Content |
| 10 | For a memoir: does the older voice appear at least twice? | Content |
| 11 | One tense per stretch; subject and verb agreeing; articles in place? | Language |
| 12 | Between 300 and 400 words, with a title? | Organisation |

## Chapter summary

- Question 6 is 10 marks: content 4, organisation 3, language 3. Write 300–400 words in
  about thirty minutes, four of them on a plan.
- Decide first whether the topic wants an argument or a memory.
- The thesis is one sentence at the end of the introduction; it must be something a
  reasonable person could disagree with.
- The essay is an hourglass: general opening narrowing to the thesis, a straight body,
  a conclusion widening back out.
- Every body paragraph: point, evidence, explanation, link. The explanation is where
  the content marks are.
- An argumentative essay must concede one point to the other side and then answer it.
- An expository essay takes its shape from the material — causes, stages, kinds — and
  allows no opinion.
- A memoir is one episode, first person, past tense, heavy in sensory detail, told in
  two voices: the person it happened to and the person remembering.
- Open with a scene, a fact, a contradiction or a question. Never with *since time
  immemorial*.

## Practice questions

**Free writing — essays (10 marks each)**

1. *Social media has made us better informed and worse at listening.* Do you agree?
   <span class="marks">[10]</span>
2. Explain the causes of air pollution in the Kathmandu Valley and suggest what a
   student can realistically do about it. <span class="marks">[10]</span>
3. Write a descriptive essay on a market place on the first morning of a festival.
   <span class="marks">[10]</span>
4. *The best thing my school ever did was something that was not on the timetable.*
   Write a reflective essay. <span class="marks">[10]</span>

**Free writing — memoir (10 marks)**

5. Write a memoir of a day on which you were trusted with something you did not feel
   ready for. <span class="marks">[10]</span>

::: note Plan for question 1
**Position:** agree with the first half, agree with the second, and argue that the
second is caused by the first.
**Thesis:** *Social media has given us more information than any generation has ever
had and, in the same movement, has taught us to reply before we have finished reading.*
**Para 2 — better informed:** a landslide in Sindhupalchok is known in Butwal in nine
minutes; the flood of 2078 was mapped by ordinary people with phones.
**Para 3 — worse at listening:** the reply button sits under the post, so answering
costs less effort than understanding; a comment written in four seconds gets the same
weight on the screen as an argument written in four hours.
**Para 4 — counter-argument:** it is said that the fault is ours, not the platform's;
answer that a tool which rewards speed will produce speed.
**Conclusion:** the remedy is small and personal — read to the end before typing.
**Opening line:** *I know what happened in Sindhupalchok this morning. I could not tell
you what my neighbour thinks about it.*
:::

**Short free-writing skills (1 mark each)**

6. Turn into a thesis: *This essay is about the importance of trees.*
   <span class="marks">[1]</span>
7. Name the fault: *Firstly, secondly, thirdly, and last but not the least…*
   <span class="marks">[1]</span>
8. Which kind of essay is *Discuss the stages by which a bill becomes law*?
   <span class="marks">[1]</span>
9. Rewrite as a topic sentence: *Now I will talk about the second reason.*
   <span class="marks">[1]</span>
10. Give a connective that concedes and then turns. <span class="marks">[1]</span>
11. What makes a memoir different from a short story? <span class="marks">[1]</span>
12. Improve: *In conclusion, I conclude that examinations are bad as I said above.*
    <span class="marks">[1]</span>

::: note Answers
**6.** *A town that plants trees along its highways is buying shade, quieter air and lower repair bills, and it is buying them cheaply.* — a position, not a subject.
**7.** *Last but not the least* is a cliché, and numbering every paragraph replaces real linking.
**8.** Expository — it explains a process and takes no position.
**9.** *The second cost of the examination system is paid by teachers.* — a topic sentence states the idea, it does not announce it.
**10.** *Granted that… / It is true that… but / Admittedly…*
**11.** A memoir is true and is told by the person it happened to, and it includes that person's later understanding of it.
**12.** *We shall go on grading memory, then, until we are willing to set a harder kind of paper.* — restate in new words and end on something forward-looking.
:::
