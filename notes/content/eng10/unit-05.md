---
subject: Compulsory English
grade: 10
unit: 5
title: 'Unit 5: Science and Experiment'
hours: 0
area: Units
---

Science begins with a question and an experiment. In this unit a popular-science article answers a surprising question — can water boil without being hot? — and an American poem lets the rain itself explain the cycle that science calls evaporation and condensation. You will learn to talk about possible and imaginary situations with **conditional sentences**, to write **instructions** and to write a **letter of complaint to the editor**.

::: key What the SEE paper asks from this unit
Reading: words from the text, completing sentences, short answers about the experiment; for the poem, word meanings, summary completion and personification. Grammar: conditional sentences (zero, first, second, third, *unless*, *provided that*). Writing: instructions and a letter to the editor.
:::

## 5.1 Yes, You Can Boil Water at Room Temperature

### About the text

This is a **popular-science article**. It takes a common belief — "water boils at 100 °C" — and shows that this is true only at one particular pressure. The writer calls the belief a **factoid** (a piece of unreliable information that is repeated so often that people accept it as fact) and explains, step by step, why boiling depends on *pressure* as well as *temperature*. The style is clear and explanatory: it asks questions, gives a reason, then proves it with an experiment anyone can imagine.

### What the text says

1. **What boiling is.** Water is made of **molecules** that are always moving; this random movement is called **thermal motion**. At any temperature some molecules move faster than others. When water is heated, more molecules gain enough energy to escape from the liquid as vapour.
2. **Bubbles.** Boiling is the point at which **bubbles of vapour** form *inside* the liquid. A bubble can form only if the vapour pressure inside it is high enough to push back the water around it. So water boils when its **vapour pressure equals the external pressure** on it.
3. **External pressure.** The pressure on a bubble comes from two sources: the weight of the water above it (it depends on the depth and the density of the water) and the **atmosphere** pressing on the water surface.
4. **Change the pressure, change the boiling point.** At sea level, atmospheric pressure is high, and water boils at 100 °C. At higher **altitude** the air above is thinner, so the pressure is lower and water boils at a lower temperature. If the pressure above the water is reduced even more, the water can boil at room temperature.
5. **The plunger experiment.** Put some warm water in a syringe, seal its nozzle and pull the plunger out sharply. The space above the water becomes close to a **vacuum**; the pressure falls; the water starts to boil, with bubbles, at a temperature far below 100 °C. When the plunger is pushed back, the vapour **condenses** again and boiling stops.
6. **Balance.** Boiling stops when the vapour pressure and the outside pressure are in **equilibrium**.

The article's lesson: boiling is not only a matter of "how hot", but of "how hot *compared with the pressure*".

### Why it matters — some real numbers

| Place | Approximate height | Water boils at about |
|---|---|---|
| Sea level | 0 m | 100 °C |
| Kathmandu | 1,400 m | 95 °C |
| Namche Bazaar | 3,440 m | 89 °C |
| Summit of Mount Everest | 8,849 m | about 71 °C |

(The boiling point falls roughly 1 °C for every 300 m of height. The values are approximate.) This is why rice takes longer to cook in the mountains and why a **pressure cooker**, which *raises* the pressure so that water boils above 100 °C, saves fuel and time in Nepali kitchens.

```figure caption="Approximate boiling point of water falls as altitude rises (about 1 °C for each 300 m)."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 2.8))
h = np.linspace(0, 9000, 50)
bp = 100 - h/300
ax.plot(h, bp, color=ACCENT, lw=2)
for x, name in [(0, "Sea level"), (1400, "Kathmandu"), (3440, "Namche"), (8849, "Everest")]:
    y = 100 - x/300
    ax.plot([x], [y], "o", color=INK, ms=4)
    ax.annotate(name, (x, y), textcoords="offset points", xytext=(6, 6), fontsize=7.5, color=INK)
ax.set_xlabel("Altitude (m)", fontsize=8.5)
ax.set_ylabel("Boiling point of water (°C)", fontsize=8.5)
ax.grid(color=GRID, lw=0.6)
ax.spines[['top', 'right']].set_visible(False)
ax.tick_params(labelsize=8)
```

### Vocabulary

| Word | Meaning | Example |
|---|---|---|
| altitude | height above sea level | Altitude sickness affects climbers. |
| molecule | a group of atoms bonded together | A water molecule is H₂O. |
| equilibrium | a state in which opposing forces are balanced | The two forces are in equilibrium. |
| condense | to change from gas or vapour to liquid | Steam condenses on a cold lid. |
| factoid | an unreliable "fact" repeated so often that it is accepted | That we use 10 % of our brain is a factoid. |
| vacuum | a space with the air removed | There is almost a vacuum in the syringe. |
| plunger | a device that is pushed and pulled (here, in a syringe) | He pulled the plunger back. |
| induce | to cause or bring about | Certain chemicals can induce sleep. |

### Questions and model answers

**Objective questions (1 mark each)**

1. Water boils when its vapour pressure is equal to <span class="marks">[1]</span>
   (a) room temperature (b) the external pressure (c) its density (d) its volume
2. As altitude increases, the boiling point of water <span class="marks">[1]</span>
   (a) rises (b) falls (c) stays the same (d) becomes 100 °C
3. The random motion of molecules is called <span class="marks">[1]</span>
   (a) thermal motion (b) gravity (c) condensation (d) equilibrium
4. "Factoid" means <span class="marks">[1]</span>
   (a) a proved fact (b) a false belief repeated as a fact (c) a small fact (d) a fraction

::: note Answers
**1.** (b). **2.** (b). **3.** (a). **4.** (b).
:::

**Short-answer questions (2 marks each)**

1. How are bubbles formed in boiling water? <span class="marks">[2]</span>
2. Mention two things on which external pressure depends. <span class="marks">[2]</span>
3. How is the atmosphere related to the pressure in water? <span class="marks">[2]</span>
4. What would happen if the atmospheric pressure on liquid water were decreased? <span class="marks">[2]</span>
5. What would the experimenter gain by pulling the plunger out? <span class="marks">[2]</span>

::: note Model answers
**1.** Bubbles form when water molecules gain enough energy to turn to vapour inside the liquid, and the vapour pressure is strong enough to push back the surrounding water.
**2.** It depends on the depth of the water and the density of the water (and on the pressure of the air above it).
**3.** The atmosphere presses on the surface of the water, and this pressure adds to the pressure inside the liquid.
**4.** Boiling bubbles would form at a lower temperature, so the water would boil below 100 °C.
**5.** Pulling the plunger lowers the pressure above the water, so the water starts to boil even at room temperature.
:::

**Long-answer question (4 marks)**

1. Explain why water boils at room temperature in a syringe when the plunger is pulled. <span class="marks">[4]</span>

::: note Model answer
**1.** Water boils when its vapour pressure equals the pressure outside it. In a closed syringe the pressure above the water is that of the air. When the plunger is pulled out sharply, the space above the water becomes almost a vacuum, so the outside pressure falls greatly. The warm water's vapour pressure is now higher than the pressure outside, so vapour bubbles form inside it — the water boils, even though it is far below 100 °C. When the plunger is released, the pressure rises again, the vapour condenses and the boiling stops.
:::

## 5.2 The Voice of the Rain

### About the poet and the poem

```photo id="eng10/whitman" caption="Walt Whitman (1819–1892), photographed in 1887." width="60"
```

**Walt Whitman** (1819–1892) is one of America's greatest poets. His long collection *Leaves of Grass*, which he revised all his life, celebrates ordinary people, nature and democracy in **free verse** — verse without rhyme or regular metre. "The Voice of the Rain" is a short poem in this style. Its form is a **dialogue**: the poet asks a question and the rain answers in its own voice.

### The poem

> And who art thou? said I to the soft-falling shower,
> Which, strange to tell, gave me an answer, as here translated:
> I am the Poem of Earth, said the voice of the rain,
> Eternal I rise impalpable out of the land and the bottomless sea,
> Upward to heaven, whence, vaguely form'd, altogether changed, and yet the same,
> I descend to lave the droughts, atomies, dust-layers of the globe,
> And all that in them without me were seeds only, latent, unborn;
> And forever, by day and night, I give back life to my own origin, and make pure and beautify it;
> (For song, issuing from its birthplace, after fulfilment, wandering,
> Reck'd or unreck'd, duly with love returns.)

### Meaning

- **Lines 1–3: the question.** The poet asks the gentle shower who it is. The rain answers, "I am the Poem of Earth": a poem of the earth, made by the earth itself.
- **Lines 4–5: the upward journey.** The rain *rises*, as invisible vapour, from land and the "bottomless sea" to heaven, where it takes shape as cloud — changed in form, "yet the same". (This is **evaporation** and **cloud formation**.)
- **Lines 6–8: the return.** It *descends* to wash the dry land and its dust, and gives life to seeds that without it would stay "latent, unborn". It returns to its origin to purify and beautify the earth. (This is **precipitation**.)
- **Lines 9–10: the comparison with song.** A song leaves the singer, travels, is heard or not heard ("reck'd or unreck'd"), and in time returns to the heart with love, just like rain returning to the earth. Rain and poetry, both are cycles of giving and returning.

### The water cycle in the poem

```figure caption="The water cycle that Whitman's rain describes: it rises, forms clouds, falls and returns."
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
fig, ax = plt.subplots(figsize=(4.6, 2.9))
ax.add_patch(Rectangle((0, 0), 10, 1.0, fc="#9ec5e8", ec="none"))
ax.add_patch(Rectangle((0, 1.0), 10, 0.5, fc="#b5a37a", ec="none"))
for cx, cy in [(6.2, 4.6), (7.4, 4.8), (8.5, 4.5)]:
    ax.add_patch(Ellipse((cx, cy), 2.0, 1.0, fc="#e6e9ee", ec=MUTED, lw=0.8))
ax.annotate("", xy=(5.3, 4.2), xytext=(2.0, 1.7), arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.6))
ax.text(2.2, 3.1, "Evaporation\n(rises as vapour)", fontsize=8, color=ACCENT, ha="center")
ax.annotate("", xy=(8.6, 1.7), xytext=(8.6, 3.9), arrowprops=dict(arrowstyle="-|>", color="#2f6fb0", lw=1.6))
ax.text(9.35, 2.9, "Rain\n(falls)", fontsize=8, color="#2f6fb0", ha="center")
ax.text(7.3, 5.55, "Condensation → cloud", fontsize=8, color=INK, ha="center")
ax.text(5.0, 0.45, "sea and land", fontsize=8, color=INK, ha="center")
ax.set_xlim(0, 10.4); ax.set_ylim(0, 6)
ax.axis("off")
```

### Poetic devices

| Device | Example | Effect |
|---|---|---|
| Personification | the rain speaks and says "I am the Poem of Earth" | Nature is given a voice and personality |
| Metaphor | "I am the Poem of Earth" | Rain is described as a poem — beautiful and life-giving |
| Simile-like comparison | song returns "with love" as rain returns to earth | Joins nature and art |
| Free verse | no rhyme, long lines | A natural, flowing speech-like rhythm |
| Antithesis (opposites) | rise / descend; day / night; seeds / unborn | Shows the complete cycle |
| Parenthesis | the last two lines in brackets | Adds an afterthought that explains the comparison |

### Vocabulary

| Word | Meaning |
|---|---|
| eternal | never-ending |
| impalpable | that cannot be touched or felt; very fine |
| vaguely | not clearly |
| descend | to come down |
| lave | to wash or pour over |
| atomies | tiny particles of dust (also *atomizes* in some texts) |
| latent | present but hidden and not yet active |
| reck | to care about or take notice of |
| drought | a long period without rain |
| globe | the Earth |
| beautify | to make beautiful |

### Questions and model answers

**Objective questions (1 mark each)**

1. Who wrote "The Voice of the Rain"? <span class="marks">[1]</span>
   (a) Rabindranath Tagore (b) Walt Whitman (c) William Wordsworth (d) Amy Lowell
2. "Impalpable" means <span class="marks">[1]</span>
   (a) heavy (b) not able to be touched or felt (c) loud (d) bright
3. According to the poem, the rain is the <span class="marks">[1]</span>
   (a) Song of the Sea (b) Poem of Earth (c) Voice of God (d) Queen of Clouds
4. The figure of speech in "The rain said, 'I am the Poem of Earth'" is <span class="marks">[1]</span>
   (a) personification (b) alliteration (c) hyperbole (d) onomatopoeia

::: note Answers
**1.** (b). **2.** (b). **3.** (b). **4.** (a) — the rain speaks like a person.
:::

**Short-answer questions (2 marks each)**

1. What are the two voices in the poem? Who do they belong to? <span class="marks">[2]</span>
2. How is the cyclic movement of the rain shown in the poem? <span class="marks">[2]</span>
3. Why are showers necessary for the earth? <span class="marks">[2]</span>
4. How are the rain and a song similar? <span class="marks">[2]</span>
5. List some pairs of opposite words from the poem. <span class="marks">[2]</span>

::: note Model answers
**1.** The two voices are the poet's (who asks) and the rain's (who answers).
**2.** The rain rises as vapour from land and sea to heaven, changes form as cloud, then descends to the earth and returns to its origin.
**3.** Showers wash the dust and drought of the land and bring life to seeds that would otherwise remain hidden.
**4.** A song leaves its birthplace and, after wandering, returns with love, just as the rain rises and returns to the earth; both give life and beauty.
**5.** rise / descend; day / night; seeds / unborn; fulfilment / wandering; reck'd / unreck'd.
:::

**Long-answer questions (4 marks each)**

1. Summarise the poem in your own words. <span class="marks">[4]</span>
2. What might happen on the earth if it does not rain for a long time? <span class="marks">[4]</span>

::: note Model answers
**1.** The poet asks the soft shower who it is, and the rain answers that it is "the Poem of Earth". It explains that it rises invisibly from land and sea to the sky, changes shape and then comes down again to wash the dry earth and wake the seeds that are waiting to be born. In this way it keeps returning life to its own source. Like a song, which comes from its birthplace, wanders and at last comes back with love, rain is a gift that always returns.
**2.** If it does not rain for a long time, rivers, ponds and wells will dry up. Crops will fail and there will be drought and famine. Animals and people will lack drinking water and may fall ill. Forests will become dry and catch fire easily. People may have to leave their land and migrate. This shows how much life on earth depends on rain.
:::

## 5.3 Grammar and writing tasks of the unit

### Grammar I: Zero and first conditional

A **conditional sentence** has an **if-clause** (the condition) and a **main clause** (the result). When the if-clause comes first, put a comma after it.

| Type | Use | If-clause | Main clause | Example |
|---|---|---|---|---|
| Zero | general truths, science | if + present simple | present simple | If you heat water, it boils. |
| First | real, likely future | if + present simple | will / can / may + base verb | If it is cold, I will wear a coat. |

#### Other words that work like *if*

| Word | Meaning | Example |
|---|---|---|
| unless | if … not | The horse won't kick you unless you go behind it. |
| provided (that) / providing | only if | Provided that you consent, I will take leave. |
| as long as | only if | As long as they communicate well, the problem may be solved. |
| in case | because it may happen | Take an umbrella in case it rains. |

::: caution Common mistake
Never use *will* in the if-clause. Write *If it rains, we will stay home*, not *If it will rain, we will stay home*. Also, *unless* already means "if not", so do not add another negative: *Unless you hurry, you will be late* (not *Unless you don't hurry*).
:::

::: example Worked example
**Problem.** Complete: "If Purna helps with the housework, his mother ____ (have) more time for him."

**Solution.** First conditional → *will + base verb*. *If Purna helps with the housework, his mother will have more time for him.*
:::

::: example Worked example
**Problem.** Rewrite with *unless*: "If you don't study, you will fail."

**Solution.** *Unless you study, you will fail.*
:::

#### Exercise A — Complete with the correct form

1. If it is cold, I ____ (wear) a coat.
2. If Purna helps with the housework, his mother ____ (have) more time for him.
3. You ____ (save) petrol if you drove more carefully. (second conditional — look carefully)
4. Say "hello" if you ____ (see) her.
5. Provided that you ____ (consent), I will take a few days' leave next week.
6. What happens if you ____ (heat) water?
7. Take care of the pence and the pounds ____ (take) care of themselves.

::: note Key to Exercise A
**1.** will wear. **2.** will have. **3.** would save (the clause is "if you drove", so the main verb is *would*). **4.** see. **5.** consent. **6.** heat (zero conditional: "it changes into steam"). **7.** will take care of themselves (a proverb).
:::

#### Exercise B — Match the halves

(a) If you go to Taplejung, (b) You will get well soon (c) The horse won't kick you (d) What happens (e) As long as they communicate well,

(i) if you follow the doctor's advice. (ii) unless you go behind it. (iii) you can see the Pathibhara temple. (iv) if you heat water? (v) the problem might be solved.

::: note Key to Exercise B
(a)–(iii), (b)–(i), (c)–(ii), (d)–(iv), (e)–(v).
:::

### Grammar II: Second and third conditional

| Type | Use | If-clause | Main clause | Example |
|---|---|---|---|---|
| Second | unreal, imaginary or unlikely *present/future* | if + past simple (*were* for all persons) | would / could / might + base verb | If I were a bird, I would see the land below. |
| Third | unreal *past*: things that did not happen | if + past perfect | would / could / might + have + past participle | If he had not come to Nepal, he would not have seen Mt Everest. |

**Formal inverted forms** (leave out *if* and put the verb first):

| Normal | Inverted |
|---|---|
| If you had arrived earlier, you would have seen Manashi. | Had you arrived earlier, you would have seen Manashi. |
| If Rijisa were in the USA, she would be working for a company. | Were Rijisa in the USA, she would be working for a company. |
| If he were to see me, he would know me at once. | (*were to* shows an unlikely future) |

::: caution Common mistakes
Do not write *If I would be rich, I would help you*. The if-clause takes the past (second conditional): *If I were rich…*. Do not mix up the second and third conditionals: *would have* belongs with the past perfect only.
:::

::: example Worked example
**Problem.** "If Gaurab ____ (be) the captain, the team ____ (play) better."

**Solution.** Unreal present → second conditional. *If Gaurab were the captain, the team would play better.*
:::

::: example Worked example
**Problem.** "I ____ (call) you had I known you were in Nepal."

**Solution.** *Had I known* = *if I had known* → third conditional; main clause *would have + past participle*. *I would have called you had I known you were in Nepal.*
:::

#### Exercise C — Complete with the correct form of the verb

1. If Gaurab were the captain, the team ____ (play) better.
2. I ____ (call) you had I known you were in Nepal.
3. If he ____ (not come) to Nepal, he would not have seen Mt Everest.
4. Had you arrived a bit earlier, you ____ (see) Manashi.
5. We could slow down global warming if we ____ (reduce) energy consumption.
6. Were Rijisa in the USA, she ____ (be) working for a company.
7. How would you feel if someone ____ (ask) you for an autograph?
8. What ____ (you / do) if Keshab had proposed to you? (past)
9. If I ____ (have) a life jacket, I could certainly swim across the river.

::: note Key to Exercise C
**1.** would play. **2.** would have called. **3.** had not come (didn't come is also accepted in the text's key). **4.** would have seen. **5.** reduced. **6.** would be. **7.** asked. **8.** would you have done. **9.** had.
:::

#### Exercise D — Complete the sentences with your own clauses

1. If you don't leave soon, ____.
2. If it rains in winter, ____.
3. I will help you as long as ____.
4. A country cannot develop unless ____.
5. What will you do if ____?

::: note Suggested answers
**1.** you will miss the bus. **2.** the roads will be slippery. **3.** you tell the truth. **4.** it invests in education. **5.** they insult you.
:::

### Writing I: Instructions

**Instructions** tell the reader how to do something in order. Features: a title (*How to…*); a list of materials; numbered steps; **imperative verbs** in the correct order; sequence words (*first, next, then, after that, finally*); short sentences.

::: example Model instructions — How to draw a jellyfish
**Materials:** a pencil, an eraser, paper, coloured pencils.

1. First, draw a large half-circle for the jellyfish's bell (head).
2. Next, draw a wavy line along the bottom of the half-circle to close the bell.
3. Then draw four or five long, wavy lines hanging down from the bell for the tentacles.
4. After that, draw two small circles for eyes and a gentle curve for a smile.
5. Add a few small curves inside the bell for decoration.
6. Finally, colour the jellyfish and shade the tentacles lightly.
:::

::: example Model instructions — How to boil water at room temperature (syringe experiment)
**Materials:** a plastic syringe (without needle), warm water (about 50 °C), an adult to help.

1. Fill the syringe one-third with warm water.
2. Push the plunger in to remove most of the air.
3. Cover the nozzle tightly with your finger.
4. Pull the plunger back sharply and hold it.
5. Watch the bubbles that appear: the water is boiling.
6. Release the plunger, and the bubbles disappear.
:::

### Writing II: A letter to the editor

A **letter to the editor** is a formal letter addressed to a newspaper. The writer gives an address and date, addresses *The Editor*, writes a **subject line**, states the problem, gives its causes and effects with evidence, suggests solutions and thanks the editor. A complaint should be polite, factual and constructive.

**Task.** Write a letter of complaint about unmanaged garbage in your locality. Mention the hazards to health and suggest measures.

::: example Model letter
Gaindakot-4, Nawalpur
1 Shrawan 2082

The Editor
*The Kathmandu Post*
Kathmandu

**Subject: Unmanaged garbage in Gaindakot-4**

Dear Sir/Madam,

Through the columns of your newspaper I would like to draw the attention of the municipality to the heaps of uncollected garbage in our locality.

Garbage has been lying on the roadside for more than two weeks. It attracts flies, mosquitoes, dogs and rats, which spread diseases such as diarrhoea, dysentery and dengue. The smell is unbearable, and children walking to school have to cover their noses. In the monsoon, rain washes the waste into the drains and blocks them.

I request the authorities to (1) collect garbage at least three times a week, (2) place covered bins at all street corners, (3) run an awareness campaign on separating waste, and (4) fine people who throw garbage in public places.

I hope that you will publish this letter and that the municipality will act soon.

Yours faithfully,
Dibas Dauliya
:::

## Chapter summary

- *Yes, You Can Boil Water at Room Temperature*: water boils when vapour pressure equals external pressure; lower pressure (altitude, a vacuum, a pulled syringe plunger) means a lower boiling point.
- Key words: altitude, molecule, equilibrium, condense, factoid, vacuum, plunger.
- *The Voice of the Rain* (Walt Whitman, free verse): the rain says it is "the Poem of Earth"; it rises, changes form, descends, revives seeds and returns, like a song.
- Devices: personification, metaphor, free verse, antithesis.
- Conditionals: zero (if + present, present); first (if + present, will); second (if + past, would); third (if + past perfect, would have + pp). *Unless* = if not; *provided that / as long as* = only if. No *will* in the if-clause.
- Instructions: title, materials, numbered imperative steps, sequence words. A letter to the editor: address, date, subject, problem, causes and effects, solutions, thanks.

## Practice questions

**Objective questions (1 mark each)**

1. Water boils at a lower temperature on a mountain because <span class="marks">[1]</span>
   (a) the air pressure is lower (b) the sun is hotter (c) water is purer (d) the wind is stronger
2. "Lave" in the poem means <span class="marks">[1]</span>
   (a) to wash (b) to burn (c) to dry (d) to lift
3. "If I ____ rich, I would build a school." <span class="marks">[1]</span>
   (a) am (b) was being (c) were (d) will be
4. "Unless you work hard, you will fail" means <span class="marks">[1]</span>
   (a) If you work hard, you will fail (b) If you don't work hard, you will fail (c) You never work (d) You will pass

::: note Answers
**1.** (a). **2.** (a). **3.** (c). **4.** (b).
:::

**Short answer questions (2 marks each)**

1. What is a vacuum? <span class="marks">[2]</span>
2. How does the poet suggest that rain is a cycle? <span class="marks">[2]</span>
3. Rewrite using the third conditional: "I did not know the answer, so I did not tell you." <span class="marks">[2]</span>
4. Rewrite in inverted form: "If he had studied, he would have passed." <span class="marks">[2]</span>

::: note Answers
**1.** A space or container from which the air has been removed.
**2.** The rain says that it rises from earth to heaven and descends again to give life and then returns to its origin.
**3.** If I had known the answer, I would have told you.
**4.** Had he studied, he would have passed.
:::

**Long answer questions (4 marks each)**

1. Write instructions on "How to make a cup of tea". <span class="marks">[4]</span>
2. Write a letter to the editor about the shortage of drinking water in your locality. <span class="marks">[4]</span>

::: note Answers
**1.** *Outline:* title; materials (water, tea leaves, milk, sugar, pan, strainer, cup); numbered steps — boil water, add tea, add milk and sugar, boil again, strain, serve; use *first, then, after that, finally*.
**2.** *Outline:* address and date; The Editor; subject (*Shortage of drinking water in Dhankuta-6*); problem and since when; effects (women and children walking far, illness, absence from school); causes (leaking pipes, poor distribution); suggestions (repair pipes, extra tanker supply, rainwater harvesting); polite close.
:::
