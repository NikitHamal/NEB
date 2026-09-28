---
subject: Compulsory English
grade: 11
unit: 17
title: Scientific Research is a Token of Humankind's Survival
hours: 3
area: Literature — Essays
---

A scientist who spent his working life studying how the earth shakes explains why
he chose a badly paid profession, and then tells the one story that answers the
question. In 1960, at the worst moment of the Cold War, his mathematics about
seismic waves turned out to be the thing that allowed enemies to sign a treaty.
That is the essay: a personal defence of science that becomes an argument about
whether our species survives.

::: key What the exam wants from this essay
Three things. The **Geneva episode** — what the problem was, why seismology
solved it, and what the scientists on both sides of the Iron Curtain had in
common. The **argument that scientists are the most practical people in the
world**, with the author's own list of examples. And the **technique** — the
quotations that head the sections, the rhetorical question that opens the essay,
the first-person narrative used as evidence, and the modest final qualification
that science is "not the beginning and the end".
:::

## 17.1 About the author

**Vladimir Isaakovich Keilis-Borok (1921–2013)** was a Russian mathematical
geophysicist — one of the founders of the modern mathematical study of
earthquakes. He was born in Moscow and spent his career at the Institute of
Earthquake Prediction Theory and Mathematical Geophysics of the Russian Academy
of Sciences, of which he was the director for many years. In later life he also
taught at the University of California, Los Angeles (UCLA), in the United States.
He was Co-director and founder of the research programme on non-linear dynamics
and earthquake prediction at the Abdus Salam International Centre for Theoretical
Physics in Trieste, Italy.

```photo id="eng11/keilis-borok" caption="Vladimir Keilis-Borok (1921–2013), the Russian mathematical geophysicist whose work on seismic waves made it possible to tell an underground nuclear explosion from an earthquake — the technical problem at the centre of this essay." width="40"
```

His scientific subject was **seismology**: the study of the waves that travel
through the earth when it moves. That sounds like a narrow, academic speciality —
and the essay begins by admitting that the young Keilis-Borok thought of it in
exactly that way, as a beautiful mathematical puzzle with no connection to real
life. His whole point is what happened next.

In 1960 he was called to Geneva as one of the technical experts advising the
negotiations on banning nuclear weapon tests. The scientists' work there fed
directly into the treaty process, and this experience shaped everything he
believed afterwards about what science is for. He remained convinced, for the
rest of his life, that the international community of scientists is one of the
few forces holding the world together.

::: definition Seismology and seismic waves
**Seismology** is the branch of science that studies earthquakes and the waves
they send through the earth. A **seismic wave** is the vibration that travels
outwards from the place where the ground breaks or where an explosion goes off. A
**seismograph** is the instrument that records those vibrations as a wiggly line
called a **seismogram**. Reading a seismogram is how a scientist in Moscow can
tell that something happened under the ground in Nevada.
:::

::: caution Who is Frank Press?
**Frank Press** (1924–2020) was the American geophysicist who quoted
Keilis-Borok's work while arguing with the Moscow experts in Geneva — which is
how Keilis-Borok found himself summoned there. He later became science adviser to
President Carter and President of the US National Academy of Sciences. The second
epigraph in the essay — "An instant understanding, the efficiency of thought and
action, and a good feeling that comes when the like-minded people work together"
— is quoted from him, and it describes exactly the experience the Geneva story
goes on to narrate.
:::

## 17.2 The context: the Cold War and the test ban

After the Second World War the United States and the Soviet Union, with their
allies, were locked in a long hostility called the **Cold War** — "cold" because
the two sides never fought each other directly, but armed, spied and threatened
without stopping. The boundary between the communist bloc and the West was known
as the **Iron Curtain**. Both sides built and tested nuclear weapons, each test
producing a better bomb than the last.

The essay explains the logic of that period with painful clarity. Each superpower
had more than enough bombs to destroy the other in a first strike — but the
rockets took about twenty minutes to arrive, which was long enough for the victim
to launch its own missiles before they landed. So neither side could attack
without also dying. This doctrine was called **Mutually Assured Destruction**,
and its acronym, as the author notes with grim satisfaction, is **MAD**. That
single "thin thread" was all that protected the human race.

Because every new test upset the balance further, the three nuclear powers of the
time — the Soviet Union, the United States and the United Kingdom — were willing
to consider a ban on testing. But a treaty is only worth signing if cheating can
be detected, and that is where the scientists came in.

## 17.3 The essay, step by step

### The opening question: "If you are so clever, why are you so poor?"

The essay begins with a popular taunt used as an epigraph, and then turns it into
a serious question: why does anybody become a scientist when businessmen, lawyers
and doctors earn far more? The author answers by way of Leo Tolstoy, who wrote
that a writer is not simply someone who writes but someone who **cannot live
without writing**. The same, Keilis-Borok says, is true of a scientist.

Then comes the list of what a scientist receives in place of money:

- **freedom, camaraderie, independence**;
- honours and promotions that depend on **yourself** more than in other
  occupations;
- and "the overwhelming feeling of uncovering yet another one of nature's
  mysteries".

Above all, science is "an exciting adventure where major reward comes from the
discovery itself." The reward is internal. That claim has to be taken on trust at
this stage of the essay — and the rest of the essay is the evidence for it.

### 1960: the summons

The narrative begins flatly: "It was 1960, the height of the cold war." He is in
Moscow, working on the theory of seismic waves, absorbed in the mathematics,
giving no thought at all to how it might connect with real life. Note how
carefully he establishes his own innocence here; the point of the story depends on
it.

Then the summons comes from the President of the Soviet Academy of Sciences, with
a message from the Palace of Nations in Geneva, where technical experts of the
three nuclear powers were meeting behind closed doors. The letter reveals that an
American scientist, Frank Press, had quoted Keilis-Borok's work while arguing with
the Moscow experts. The understatement that follows is the best sentence in the
essay: "And, to my great surprise, I found myself in Geneva."

### The problem, stated formally

The author sets out the difficulty like a mathematician, in two suppositions and
a question. Suppose the nuclear powers sign an agreement to stop testing; and
suppose one of them breaks it and secretly explodes a bomb underground. **How can
the others detect the violation?**

The connection to his own field was direct. An underground nuclear explosion
makes the earth tremble in much the same way an earthquake does, and both are
recorded as wiggles on a seismogram thousands of kilometres away. So the treaty
depended on a single technical question: can you tell the two apart? "Suddenly,"
he writes, "my theoretical knowledge had a direct application in the area of
survival of the humankind."

```figure caption="The Geneva problem in one picture. An earthquake and an underground explosion both shake the ground, but they shake it differently: the explosion pushes outward in every direction at once and dies away quickly, while an earthquake is a slipping crack that keeps radiating. Telling these two traces apart was what made a test-ban treaty checkable."
import numpy as np, matplotlib.pyplot as plt

rng = np.random.default_rng(7)
t = np.linspace(0, 10, 1400)

def wiggle(env, freq, seed):
    r = np.random.default_rng(seed)
    n = np.convolve(r.normal(0, 1, t.size), np.ones(4) / 4, mode="same")
    return env * (np.sin(2 * np.pi * freq * t) * 0.55 + n * 0.45)

# explosion: one sharp onset, fast decay, no clear second arrival
p = np.where(t > 2.0, np.exp(-(t - 2.0) * 1.35), 0)
ex = wiggle(p, 2.6, 3)

# earthquake: P arrival, then a larger S arrival, then a long coda
p2 = np.where(t > 2.0, np.exp(-(t - 2.0) * 1.9), 0) * 0.45
s2 = np.where(t > 4.3, np.exp(-(t - 4.3) * 0.32), 0)
eq = wiggle(p2 + s2, 1.7, 11)

fig, axes = plt.subplots(2, 1, figsize=(5.1, 3.3), sharex=True)

axes[0].plot(t, ex / np.abs(ex).max(), color=ACCENT, lw=0.7)
axes[0].set_title("underground explosion", fontsize=7.6, color=INK, loc="left", pad=3)
axes[0].annotate("sharp onset,\nquick decay", xy=(2.2, 0.75), xytext=(4.4, 0.78),
                 fontsize=6.6, color=MUTED, va="center",
                 arrowprops=dict(arrowstyle="-", color=GRID, lw=0.9))

axes[1].plot(t, eq / np.abs(eq).max(), color=INK, lw=0.7)
axes[1].set_title("earthquake", fontsize=7.6, color=INK, loc="left", pad=3)
axes[1].annotate("P", xy=(2.1, 0.42), xytext=(1.5, 0.85), fontsize=7.0, color=MUTED,
                 arrowprops=dict(arrowstyle="-", color=GRID, lw=0.9))
axes[1].annotate("S", xy=(4.4, 0.85), xytext=(3.7, 0.92), fontsize=7.0, color=MUTED,
                 arrowprops=dict(arrowstyle="-", color=GRID, lw=0.9))
axes[1].annotate("long, slowly fading coda", xy=(7.4, -0.55), xytext=(6.0, -1.02),
                 fontsize=6.6, color=MUTED,
                 arrowprops=dict(arrowstyle="-", color=GRID, lw=0.9))

for a in axes:
    a.set_ylim(-1.25, 1.25)
    a.set_yticks([])
    for s in ("top", "right", "left"):
        a.spines[s].set_visible(False)
    a.spines["bottom"].set_color(GRID)
    a.tick_params(colors=MUTED, labelsize=6.6, length=2)

axes[1].set_xlabel("time recorded at a distant station (schematic)",
                   fontsize=6.8, color=MUTED)
fig.tight_layout()
```

### What the scientists had in common

This is the moral centre of the essay. In an atmosphere of political tension,
with the two blocs hostile to each other, experts from opposite sides of the Iron
Curtain had to find a solution that "outwardly seemed impossible, given all our
differences in cultural background."

What saved them, he says, was a clear and obvious distinction: **they were all
scientists.** They could construct a common language, and he names its three
grammatical rules:

1. **respect for hard evidence**;
2. **undisputable ranking by expertise only** — not by rank, nationality or
   politics;
3. **persistent self-criticism**.

Those three habits, he argues, are what make science international. Because of
them the experts produced a solution, and the solution "eventually allowed
politicians to reach one of the most important decisions of their times: nuclear
test ban."

The episode taught him three lessons, and he lists them in rising order:

- that as a scientist he has people all over the world who think and interact as
  he does;
- that he need **never feel lonely abroad**;
- and, above all, "that while there is science, there is hope of survival and
  well-being for all of us."

### Scientists are the most practical people in the world

Keilis-Borok now turns to a prejudice: the "common lore" that a person immersed
in science has no practical sense. He concedes the joke — a very great
mathematician of our time was sometimes so lost in a problem that he left home
wearing shoes from two different pairs — and then reverses it completely.

All new technologies and all new branches of industry, from defence to
entertainment, grow out of **fundamental research**. His examples from the past
are antibiotics, electronics, biotechnology, synthetic fibres, the green
revolution and genetic forensic diagnosis. His examples of what only basic
research can still deliver are new sources of energy, new mineral deposits,
efficient defence against terrorism, a cure for cancer and new forms of
transport. And he adds a practical note aimed straight at a student: people
trained in theoretical physics are head-hunted by financial institutions, and
those trained at the frontiers of biology become founders and directors of
pharmaceutical companies. "So, knowledge of basic science will give you a head
start in whatever career you choose."

### The dangers, and where the hope lies

The final movement widens from one man's career to the survival of civilisation.
The threats he lists are both natural and man-made: earthquakes, the
self-inflicted destruction of megacities, environmental catastrophes, and
economic and social crises. A single modern disaster — a massive release of
radioactivity from a nuclear waste dump, an earthquake in the middle of a
megalopolis, an outburst of mass violence — can cause up to a million casualties,
make a large part of the world uninhabitable, trigger a global depression, or set
off a war in a "hot" region. And these dangers keep growing although trillions of
dollars a year are spent to contain them.

Then the key sentence of the argument: the hope and the responsibility for
breaking the **stalemate** rest "not on the money but on intellectual
resources" — even though money is the more popular of the two, as the French
proverb says: "Nobody is satisfied with his wealth, everybody is satisfied with
his wisdom." Only basic research can create a springboard for a new
disaster-preparedness industry.

### The ending, and its qualification

After a third epigraph from McGeorge Bundy — "Ours is the time of contest over
issues not completely understood" — the essay states its title as a proposition:
scientific research is "an exciting venture into the great unknown and the token
of humankind's survival", and it is the scientists with their tools who are up to
the challenge.

But Keilis-Borok refuses to end on a boast. His last paragraph is a deliberate
step backwards: "science is not the beginning and the end." More important for
humankind, and for each individual, are the **human qualities**. Science is their
servant: "if humanly used, science is their indispensable guardian and caretaker."
The two conditions in that sentence — *if humanly used* — carry the whole weight
of the ending, and they are what separate this essay from simple propaganda for
science.

```figure caption="How the essay widens. Each step takes the same claim to a larger scale, so that a question about one man's salary ends as a question about the survival of the species."
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(5.1, 3.4))
ax.set_xlim(0, 10.6); ax.set_ylim(0, 7.2); ax.axis("off")

steps = [
    (0.30, 0.35, "THE PERSON", "why be a scientist at all?"),
    (1.85, 1.65, "THE EPISODE", "Geneva, 1960"),
    (3.40, 2.95, "THE PROFESSION", "scientists are the most\npractical people"),
    (4.95, 4.25, "THE PLANET", "disasters, and the money\nthat cannot stop them"),
    (6.50, 5.55, "THE LIMIT", "\"science is not the\nbeginning and the end\""),
]

for x, y, head, body in steps:
    fc = "#eef3f9" if head != "THE LIMIT" else "#ffffff"
    ec = ACCENT if head != "THE LIMIT" else MUTED
    ax.add_patch(FancyBboxPatch((x, y), 3.85, 1.30,
                                boxstyle="round,pad=0.06",
                                fc=fc, ec=ec, lw=1.0))
    ax.text(x + 0.22, y + 1.00, head, fontsize=6.3, color=MUTED,
            ha="left", va="center")
    ax.text(x + 0.22, y + 0.46, body, fontsize=7.0, color=INK,
            ha="left", va="center", linespacing=1.4)

for i in range(4):
    x0 = steps[i][0] + 1.0
    y0 = steps[i][1] + 1.30
    ax.annotate("", xy=(x0 + 0.52, y0 + 0.35), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0))

ax.text(0.30, 7.00, "scale of the claim", fontsize=6.6, color=MUTED,
        ha="left", va="center")
```

## 17.4 The argument in summary

Reduced to its bones, the essay makes four connected claims.

1. **Science pays in a different currency.** Freedom, camaraderie, independence,
   self-earned advancement, and the pleasure of discovery are the scientist's
   real wages.
2. **Science is a universal language.** Because it ranks people by expertise
   alone, respects only hard evidence and criticises itself relentlessly, it
   allows people who are politically enemies to work together honestly.
3. **Science is the most practical thing there is.** Every industry and every
   technology begins in fundamental research, however useless that research
   looks at the time. Keilis-Borok's own seismic theory is the proof: pure
   mathematics one year, an instrument of world peace the next.
4. **Science is therefore a condition of survival.** Our dangers are now so large
   that money alone cannot contain them; only intellectual resources can. But
   science must be *humanly used*, because human qualities matter more than
   science itself.

## 17.5 Themes

**Science as a form of international brotherhood.** The Geneva story is chosen
precisely because the political conditions were as bad as they could be. If
Soviet and American experts could build a common language in 1960, the claim is
proved at its hardest case.

**Pure research and its unexpected uses.** The young man who "did not give much
thought to how it connects with the real life" becomes the man whose work helps
end atmospheric bomb testing. The essay is an argument against judging knowledge
by its immediate usefulness.

**Intellect against money.** This opposition runs from the first line ("If you
are so clever, why are you so poor?") to the last movement ("not on the money but
on intellectual resources"). The essay begins by conceding that scientists are
poor and ends by showing that wealth is the weaker of the two forces.

**Survival.** The word in the title is not decoration. Nuclear war, earthquakes
in megacities, radioactive waste, environmental collapse, mass violence — the
essay's list of what could destroy us is long, and its claim is that research is
the only reliable defence.

**Humility.** The last paragraph withdraws just enough of the claim to make the
rest believable. Science is a **guardian and caretaker**, not a master; both
words describe a servant who protects.

## 17.6 Style and technique

**Epigraphs.** Three quotations are set like headings at the joints of the essay:
the popular expression "If you are so clever, why are you so poor?", Frank
Press's description of like-minded people working together, and McGeorge Bundy's
"Ours is the time of contest over issues not completely understood." Each one
opens the section that follows, states its subject in someone else's voice, and
lends the author borrowed authority. The Tolstoy comparison works the same way.
Together they also quietly demonstrate the essay's own thesis — that thinking is
a shared, international activity.

**Personal narrative as evidence.** The middle of the essay is a story with a
date, a place, a named character and a surprise. This is far more persuasive than
assertion: instead of claiming that science serves humanity, the author shows one
occasion on which it did, and he is careful to make himself an unwitting
participant rather than a hero.

**Understatement.** "And, to my great surprise, I found myself in Geneva." The
passive, almost accidental phrasing — as though he had simply looked up and found
himself there — conveys astonishment far better than exclamation would, and keeps
the scientist modest while the achievement grows.

**Concession and reversal.** Twice he grants his opponent's point before
overturning it: scientists really are poorer than lawyers; scientists really can
be absent-minded enough to wear odd shoes. Admitting the weaker case first makes
the counter-argument look honest rather than defensive.

**Cataloguing.** Lists do much of the work — antibiotics, electronics,
biotechnology, synthetic fibres, the green revolution, genetic forensics; energy,
minerals, defence against terrorism, cancer, transport; earthquakes, megacities,
environmental catastrophe, economic and social crisis. The sheer length of each
list is the argument.

| Device | Example | What it does |
|---|---|---|
| Rhetorical question | "If you are so clever, why are you so poor?" | Opens with the reader's own objection instead of hiding from it |
| Epigraph / quotation | Tolstoy, Frank Press, McGeorge Bundy, the French proverb | Frames each section and shows thought as a shared enterprise |
| Analogy | a scientist is like Tolstoy's writer, who "cannot live without writing" | Redefines science as a compulsion, not a career choice |
| Anecdote | the 1960 summons to Geneva | Turns an abstract claim into verifiable experience |
| Understatement | "I found myself in Geneva" | Modesty that makes the astonishment more vivid |
| Acronym and irony | "Mutually Assured Destruction," with ominous acronym "MAD" | The abbreviation passes judgement on the policy |
| Concession | "It is true that on occasions a greatest mathematician… wearing shoes from two different pairs" | Disarms the reader before the reversal |
| Catalogue | "antibiotics, electronics, biotechnology, synthetic fibres…" | Accumulated proof that basic research pays |
| Metaphor | "springboard", "thin thread", "guardian and caretaker" | Compresses whole arguments into single images |
| Qualification | "science is not the beginning and the end… if humanly used" | Prevents the essay from becoming propaganda |

## 17.7 Glossary

| Word | Meaning |
|---|---|
| acronym | a word made from the first letters of a name, e.g. MAD |
| annihilation | complete destruction |
| camaraderie | close friendship and trust among people who work together |
| cold war | intense political, military and ideological conflict without open fighting |
| forensic | relating to scientific methods of investigating crime |
| head start | an advantage at the beginning of a competition or career |
| head-hunted | actively recruited for a job by another employer |
| indisputable | so clearly true that it cannot be argued with |
| Iron Curtain | the political boundary said to divide communist Eastern Europe from the West |
| lore | traditional belief or common talk about a subject |
| megalopolis | a very large city or continuous urban region |
| ominous | suggesting that something bad is going to happen |
| retaliation | a counter-attack; revenge |
| seismic waves | vibrations that travel through the earth after an earthquake or explosion |
| self-inflicted | caused by oneself |
| springboard | something that gives a strong start to an activity |
| stalemate | a deadlock; a situation in which no side can move forward |
| standoff | a situation in which two opposing sides balance each other; a standstill |
| summons | an order to come or appear |
| venture | a new activity that involves risk |

::: tip Three sentences worth memorising
"Science is an exciting adventure where major reward comes from the discovery
itself." — for the opening argument. "What saved us was a clear and obvious
distinction. We were all scientists." — for the Geneva episode. "If humanly used,
science is their indispensable guardian and caretaker." — for the ending. Learn
these three and you can answer almost any question on the essay accurately.
:::

## Chapter summary

- The essay is by **Vladimir Keilis-Borok (1921–2013)**, a Russian mathematical
  geophysicist of the Russian Academy of Sciences, later at UCLA, and founder and
  co-director of the earthquake-prediction programme at the ICTP in Trieste.
- It opens with the taunt "If you are so clever, why are you so poor?" and
  answers with Tolstoy: a scientist, like a writer, is someone who **cannot live
  without** the work. In place of money come freedom, camaraderie, independence,
  self-earned promotion and the joy of discovery.
- In **1960**, at the height of the Cold War, the author was summoned from Moscow
  to Geneva because the American scientist **Frank Press** had quoted his work.
- The problem: if the powers ban nuclear tests and one of them cheats with a
  secret **underground** explosion, how can the others detect it? The answer lay
  in seismology — explosions and earthquakes shake the ground differently.
- Experts from both sides of the **Iron Curtain** succeeded because they were all
  scientists, sharing a language built on **hard evidence, ranking by expertise
  alone, and persistent self-criticism**. Their solution let politicians reach the
  **nuclear test ban**.
- The lesson: a scientist is never lonely abroad, and "while there is science,
  there is hope of survival and well-being for all of us."
- Scientists are the **most practical people in the world**: antibiotics,
  electronics, biotechnology, synthetic fibres, the green revolution and genetic
  forensics all came out of fundamental research, and basic science gives a head
  start in any career.
- Modern disasters — nuclear waste, an earthquake in a megacity, mass violence —
  could kill a million people, and trillions of dollars have not contained them.
  The hope rests "not on the money but on intellectual resources."
- The essay ends with a qualification: science is **not** the beginning and the
  end; **human qualities** matter more, and science, "if humanly used", is their
  indispensable guardian and caretaker.

## Practice questions

**Short answer questions (2 marks each)**

1. What does a scientist get instead of big money? <span class="marks">[2]</span>
2. What was the problem that the nuclear powers had faced? <span class="marks">[2]</span>
3. In which area did Keilis-Borok's theoretical knowledge have a direct
   application? <span class="marks">[2]</span>
4. What was the important decision that the politicians were able to take as a
   result of the Geneva talks? <span class="marks">[2]</span>
5. What are the natural and man-made disasters mentioned by the author? <span class="marks">[2]</span>
6. The professional addressed as "you" in "If you are so clever, why are you so
   poor?" refers to a (i) lawyer (ii) doctor (iii) scientist (iv) businessman.
   Justify your choice. <span class="marks">[2]</span>
7. The writer says, "I found myself in Geneva." What does it express? <span class="marks">[2]</span>

::: note Model answers — short questions
**1.** Instead of a large income a scientist receives freedom, camaraderie and
independence; honours and promotions that depend on his own ability far more than
in other occupations; and, above all, "the overwhelming feeling of uncovering yet
another one of nature's mysteries." As the essay puts it, science is an exciting
adventure in which the major reward comes from the discovery itself — the
satisfaction of the work is the payment.

**2.** The three nuclear powers — the Soviet Union, the United States and the
United Kingdom — wanted to ban the testing of new nuclear weapons, but a ban is
useless if it cannot be policed. Their problem was therefore one of verification:
suppose the powers sign an agreement to stop testing, and suppose one of them
breaks it by secretly setting off an underground nuclear explosion — how can the
others detect the violation? Underground explosions shake the earth in much the
same way earthquakes do, so the difficulty was telling the two apart.

**3.** In the survival of humankind — specifically, in the detection of secret
underground nuclear tests. Keilis-Borok had been working in Moscow on the pure
theory of seismic waves, with no thought of any practical use. Because an
underground explosion produces tremors similar to those of an earthquake, his
theory became the means of distinguishing a cheat's bomb from a natural event,
and so made a verifiable test-ban treaty possible.

**4.** The **nuclear test ban**. The scientists at Geneva worked out a technical
solution to the detection problem, and that solution, in the author's words,
"eventually allowed politicians to reach one of the most important decisions of
their times: nuclear test ban." The order of events matters: the experts met
first, and the political decision followed from what they were able to show could
be done.

**5.** The author names both kinds together as threats to the survival of
civilisation: **earthquakes** (natural), and, as man-made ones, the
self-inflicted destruction of megacities, environmental catastrophes, and
economic and social crises. He then gives examples of what a single modern
disaster could be — a massive release of radioactivity from a nuclear waste
disposal site, an earthquake in the middle of a megalopolis, or an outburst of
mass violence — any of which could cause up to a million casualties, make a large
part of the world uninhabitable, or trigger a global depression or a war.

**6.** The answer is **(iii) scientist**. The sentence is the essay's opening
epigraph and is immediately explained by the question that follows it: why do
some of us still decide to become scientists, "despite the fact that businessmen,
lawyers, and doctors enjoy a much higher income"? Lawyers, doctors and businessmen
are therefore named as the *rich* professions and cannot be the "you" of the
taunt. The person who is clever but poor is the scientist, and the whole essay is
his reply.

**7.** It expresses surprise, suddenness and a pleasing sense of being carried
along by events rather than directing them. The passive construction — he does
not say "I went to Geneva" but "I found myself in Geneva" — makes it sound as
though he looked up one day and was simply there. It also expresses the essay's
larger theme in miniature: a man absorbed in abstract mathematics, with no
thought of the real world, is suddenly lifted out of his study and set down in the
middle of international politics, because his work turned out to matter.
:::

**Long answer questions (5 marks each)**

1. How does the essayist justify that scientific research is the token of
   humankind's survival? <span class="marks">[5]</span>
2. Discuss and illustrate the writer's stand that scientists are the most
   practical people in the world. <span class="marks">[5]</span>
3. What can be the purpose of the essayist in using quotations in the essay?
   Discuss with reference to at least three of them. <span class="marks">[5]</span>
4. "While there is science, there is hope of survival and well-being for all of
   us." Explain this statement, and say whether you find science a blessing or a
   curse. <span class="marks">[5]</span>

::: note Model answers — long questions
**1.** The word **token** in the title means a sign and a guarantee — something
that both shows survival is possible and helps bring it about. Keilis-Borok
justifies the claim in three stages.

First, by **narrative proof**. In 1960 the human race was protected from
extinction by nothing better than the arithmetic of Mutually Assured Destruction
— a "thin thread", as he calls it, since each superpower could destroy the other
and each had twenty minutes in which to retaliate. The one way out was a treaty
banning tests, and the treaty was impossible until somebody could tell a secret
underground explosion from an earthquake. Seismology answered that question.
Research done for pure mathematical pleasure therefore became a direct instrument
of survival, and the test ban followed. This is not an argument but a case, and it
is the strongest thing in the essay.

Second, by pointing to the **community** that science creates. The Geneva experts
came from opposite sides of the Iron Curtain, with every cultural and political
reason to distrust each other, and yet they succeeded, because "we were all
scientists" and could build a common language out of respect for hard evidence,
ranking by expertise alone, and persistent self-criticism. Science thus supplies
the one channel of honest communication that survives when politics has broken
down — and a species that can still talk to itself can still be saved. Hence his
conclusion: "while there is science, there is hope of survival and well-being for
all of us."

Third, by examining the **present danger**. The threats now are earthquakes in
megacities, environmental catastrophe, nuclear waste, mass violence, economic
collapse — each capable of a million casualties — and they keep growing although
trillions of dollars a year are spent against them. Money, therefore, has already
been tried and has failed; what remains is intellectual resource. "The hope and
the responsibility for breaking the stalemate rest not on the money but on
intellectual resources," and only basic research can create the springboard for a
new disaster-preparedness industry.

Finally he guards the claim from overstatement. Science is "not the beginning and
the end"; human qualities matter more, and science is only their guardian and
caretaker — and only "if humanly used." The token is a promise, not a magic
charm: it works if we do.

**2.** The writer takes up a familiar prejudice — the "common lore" that a person
immersed in science has no practical sense — and turns it upside down.

He begins by **granting the joke**, which is a shrewd move. It is true, he says,
that one of the greatest mathematicians of our time was sometimes so lost in a
current problem that he left home wearing shoes from two different pairs. Having
conceded the comic surface, he asks the reader to look carefully at the other
side.

His first illustration is **historical**: all new technologies and all new
branches of industry, from defence to entertainment, stem from fundamental
research. He lists the past yield — antibiotics, electronics, biotechnology,
synthetic fibres, the green revolution, genetic forensic diagnosis. Each of these
began as abstract enquiry and now underlies an entire industry. Antibiotics were
not invented by someone looking for a marketable product; electronics came out of
the physics of the atom; genetic forensics came out of curiosity about DNA.
Nothing could be more practical than the things that make everything else
possible.

His second illustration is the **future**: only basic research can now give us
new sources of energy, new mineral deposits, efficient defence against terrorism,
a cure for cancer and new forms of transportation. These are exactly the problems
the practical world most wants solved, and none of them has a shortcut.

His third illustration is **personal and economic**, and it is aimed at a student
deciding what to study. People trained in theoretical physics are head-hunted by
financial institutions; those trained at the frontiers of biology become founders
and directors of pharmaceutical companies. "Knowledge of basic science will give
you a head start in whatever career you choose."

The unstated illustration, of course, is the author's own story. A man doing
mathematics on seismic waves with no thought of the real world turned out to hold
the key to a nuclear test ban. Defining "practical" as *producing real effects in
the world*, rather than as *looking sensible*, the scientist in odd shoes is the
most practical person alive, because the work he does while apparently dreaming is
what everyone else will be standing on in fifty years.

**3.** The essay is unusually full of other people's words. There are four that
matter: the popular expression "If you are so clever, why are you so poor?";
Tolstoy on the writer who cannot live without writing; Frank Press on the good
feeling of like-minded people working together; the French proverb "Nobody is
satisfied with his wealth, everybody is satisfied with his wisdom"; and McGeorge
Bundy's "Ours is the time of contest over issues not completely understood." They
serve several purposes at once.

**They organise the essay.** Three of them are printed as epigraphs at the joints
of the text, each announcing the section it stands before. The popular expression
introduces the defence of a poorly paid profession; the Press quotation introduces
the Geneva story about collaboration; the Bundy quotation introduces the closing
movement about dangers we do not yet understand. They work as signposts in an
essay that has no other headings.

**They let the author voice the objection without owning it.** Beginning with a
taunt aimed at himself is disarming: the reader's own scepticism has been spoken
aloud, so it no longer has to be defended, and the author can proceed to answer
it.

**They borrow authority.** A geophysicist arguing that scientists are admirable
is an interested party. Tolstoy speaking about vocation, an American presidential
adviser speaking about uncertainty, and a leading American geophysicist speaking
about the pleasures of teamwork are all witnesses from outside the case. The
Press quotation is especially well chosen: Press is an American, which makes him
the ideal witness for a claim about cooperation across the Iron Curtain.

**They give compression and memorability.** The French proverb makes the point
about money and wisdom in one line that would otherwise need a paragraph, and its
irony — everyone thinks himself wise enough and no one thinks himself rich enough
— carries the argument further than plain statement could.

**And they enact the thesis.** The essay claims that thinking is a shared,
international, cross-generational activity; a text built out of a Russian
novelist, an American scientist, an American statesman and an anonymous French
proverb is a small demonstration of that claim.

**4.** *(Explanation followed by a short argued essay.)*

**Explanation.** The sentence is the third and greatest of the lessons
Keilis-Borok drew from Geneva. He means that science is a permanent, functioning
channel of honest cooperation between human beings, which stays open even when
every other channel has closed. In 1960 politics had failed: the two blocs could
not trust each other and the world was held together by the threat of mutual
extinction. Yet the scientists in that closed room could still work together,
because their profession runs on evidence rather than loyalty, ranks people by
expertise rather than nationality, and criticises itself without mercy. That
shared discipline produced a technical answer, and the answer let the politicians
sign. So long as such a community exists, he is saying, there is always somewhere
for a solution to come from — not only for war, but for disease, hunger, energy
and disaster. "Well-being" matters as much as "survival" in his sentence: science
is not merely what saves us from catastrophe but what makes a decent life
possible.

**Is science a blessing or a curse?** The honest answer is that science is
neither; it is power, and power takes its character from the hands that hold it.
The same understanding of the atomic nucleus produced the bomb that threatened the
world in 1960 and the medical isotopes that treat cancer today. The same chemistry
gave us fertilisers that feed billions and the pollution that poisons our rivers.
The same networks that spread knowledge instantly to a student in Nepal spread
lies just as fast.

But the balance, on the evidence, is strongly positive. Science has roughly
doubled human life expectancy in a century; it has ended smallpox; it has fed a
population that older methods could not have fed; it warns us of earthquakes and
storms; it gives an ordinary student access to a library that no king once
possessed. Against this, its harms — nuclear weapons, environmental damage,
surveillance — are real, but each is a harm of *use*, not of *knowledge*.
Knowing how the nucleus works does not oblige anyone to build a bomb, and, as
Keilis-Borok's own story shows, the same knowledge that made the bomb detectable
made the ban on testing possible.

That is exactly why the essay ends as it does. Science is "not the beginning and
the end"; human qualities matter more, and science, "if humanly used", is their
indispensable guardian and caretaker. A blessing or a curse is therefore the
wrong question. The right question is who is using it, and for what — and that is
a question about honesty, courage and conscience, not about laboratories.
:::

**Reference to the context**

1. "What saved us was a clear and obvious distinction. We were all scientists. We
   were able to work out a common language, based on respect to hard evidence,
   undisputable ranking by expertise only, and persistent self-criticism."
   (a) Who are "we", and where are they? (b) What had to be "saved", and from
   what? (c) Explain each of the three foundations of the common language.
   (d) What did this common language finally make possible? <span class="marks">[5]</span>
2. Are the following statements true, and why?
   (i) Money is more powerful than intellectual resources. (ii) Intellectual
   resources help the survival of humankind. (iii) Basic research is a way of
   stalling disasters. <span class="marks">[5]</span>

::: note Model answers — reference to the context
**1.** (a) "We" are the technical experts of the three nuclear powers of the time
— the Soviet Union, the United States and the United Kingdom — meeting behind
closed doors at the Palace of Nations in Geneva in 1960, with the author among
them as a Soviet specialist in seismic waves.
(b) What had to be saved was, in the first place, the negotiation itself. The
experts came from opposite sides of the Iron Curtain, and the political tension
of the Cold War hung over their heads; agreement "outwardly seemed impossible,
given all our differences in cultural background." Beyond that, what was at stake
was the test-ban treaty, and beyond that the human race, since at the time every
man, woman and child lived under the threat of annihilation.
(c) **Respect for hard evidence** means that a claim is settled by measurement
and not by who makes it, so a Soviet seismogram and an American one can be laid
side by side and argued about honestly. **Undisputable ranking by expertise only**
means that authority in the room came from what a person knew, not from rank,
nationality or political backing — which is precisely what allowed enemies to
defer to each other without humiliation. **Persistent self-criticism** means that
each side was in the habit of attacking its own conclusions before anyone else
could, so no one had to defend a weak position out of pride. Taken together the
three make a professional culture in which people can be opponents politically
and colleagues intellectually at the same time.
(d) It made a technical solution possible — a method of distinguishing an
underground nuclear explosion from an earthquake — and that solution "eventually
allowed politicians to reach one of the most important decisions of their times:
nuclear test ban." It also taught the author personally that he had like-minded
people all over the world and need never feel lonely abroad.

**2.** (i) **Not true, according to the essay — though the author admits money is
the more popular belief.** He states plainly that "the hope and the responsibility
for breaking the stalemate rest not on the money but on intellectual resources."
His evidence is that trillions of dollars a year are already being spent to
contain modern disasters by all known techniques, and the dangers keep growing.
Money can only buy more of what already exists; when what exists is not enough,
only new knowledge can help. He quotes the French proverb — "Nobody is satisfied
with his wealth, everybody is satisfied with his wisdom" — to explain why people
nevertheless go on believing in money: we always feel short of wealth and never
short of wisdom, which is exactly the wrong way round.

(ii) **True.** This is the essay's central claim and the meaning of its title.
Intellect saved the world in 1960, when a piece of pure seismic theory made a
nuclear test ban verifiable and therefore signable. Intellect is also the source
of everything that has improved human life — antibiotics, electronics, the green
revolution — and it is the only resource capable of answering the dangers that
now threaten civilisation. Hence: "while there is science, there is hope of
survival and well-being for all of us." The author adds one condition, which
should be included in a full answer: intellect must be *humanly used*, since
"science is not the beginning and the end" and human qualities matter more.

(iii) **True, with a precise meaning of "stalling".** To stall a disaster is to
hold it off, and that is exactly what basic research does, in two ways. It
supplies the means of *prediction and detection* — the author's own field,
earthquake prediction, exists for that reason, and the detection of secret nuclear
tests stalled an arms race. And it supplies the means of *preparation*: "only the
basic research can create a springboard for developing new disaster preparedness
industry." What it does not do is abolish danger. Earthquakes will still happen;
research only decides whether they kill a million people or a hundred. The claim
is therefore modest and defensible — research buys us time and warning, which is
all that can honestly be promised.
:::
