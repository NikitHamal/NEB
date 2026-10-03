---
subject: Science and Technology
grade: 8
unit: 1
title: Scientific Learning
hours: 0
area: Science and Technology
---

Science is not a list of facts to memorise. It is a way of finding out what is
true: you look carefully, you change one thing at a time, you write down what
you saw, and you check whether your explanation survives the evidence. This
unit is about that way of working — how to stay safe in a laboratory, how to
carry out an experiment, how to run a survey, and how to write up a small piece
of research. Everything in this book depends on these habits.

::: key What this unit asks of you
You should be able to name the safety rules of a science laboratory and say why
each one exists, describe the steps of the scientific method in order, plan a
simple experiment with a control, run a small survey and tabulate its results,
and write a short research report with a title, aim, method, observation,
conclusion and a list of sources.
:::

## 1.1 Science and the scientific method

Science is the organised study of the natural world based on observation and
experiment. The knowledge it produces must be testable: if a statement cannot
be tested by any observation, it is not a scientific statement.

The **scientific method** is the working order that scientists follow.

1. **Observation.** Notice something and describe it exactly. "The ice in the
   glass melted in fifteen minutes in the sun" is an observation. "Ice melts
   fast" is not — fast compared with what, and how fast?
2. **Question.** Turn the observation into a question that can be answered by
   measurement. How does the time taken to melt depend on the amount of ice?
3. **Hypothesis.** Give a testable answer before you start. "Doubling the mass
   of ice doubles the time taken to melt."
4. **Prediction.** Say what you will see if the hypothesis is right. "A 100 g
   piece will take twice as long as a 50 g piece."
5. **Experiment.** Change one thing (the mass), keep everything else the same
   (same glass, same sunlight, same starting temperature) and measure the
   result.
6. **Analysis.** Put the readings in a table, then in a graph, and look for a
   pattern.
7. **Conclusion.** Say whether the hypothesis was supported. Then repeat the
   experiment — one reading proves nothing.

```figure caption="The scientific method is a loop, not a straight line. A result that fails to support the hypothesis is still a result: it sends you back to a better question."
fig, ax = plt.subplots(figsize=(4.9, 3.0))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.4)
ax.axis("off")
steps = [("Observation", 1.2), ("Question", 2.6), ("Hypothesis", 4.0),
         ("Experiment", 5.4), ("Analysis", 6.8), ("Conclusion", 8.2)]
for name, x in steps:
    ax.text(x, 3.4, name, ha="center", va="center", fontsize=7.2, color=INK,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=ACCENT, lw=1.1))
    if x < 8.2:
        ax.annotate("", xy=(x + 0.72, 3.4), xytext=(x + 0.5, 3.4),
                    arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.2))
ax.annotate("", xy=(8.2, 2.4), xytext=(1.2, 2.4),
            arrowprops=dict(arrowstyle="->", color=SERIES[1], lw=1.3))
ax.text(4.7, 1.95, "if the result is unexpected, ask a better question", ha="center",
        fontsize=6.7, color=SERIES[1])
ax.text(4.7, 5.1, "one thing changed at a time, everything else kept the same",
        ha="center", fontsize=6.9, color=MUTED)
fig.tight_layout()
```

### 1.1.1 Variables in an experiment

An experiment has three kinds of quantity, and confusing them is the most common
mistake in school science.

| Kind of variable | Meaning | Example (ice melting) |
|---|---|---|
| Independent | the one you change on purpose | mass of ice: 50 g, 100 g, 150 g |
| Dependent | the one you measure | time taken to melt |
| Controlled | the ones you keep the same | room temperature, size of glass, starting temperature |

::: definition Controlled experiment
A **controlled experiment** is one in which only the independent variable is
changed while every other factor that could affect the result is kept the same.
Without a control you cannot tell which change caused the result.
:::

::: caution Changing two things at once
If you use a bigger piece of ice *and* put it in a warmer room, and it melts
faster, you have learnt nothing about the effect of the mass. Exam answers that
name only the variables but not which one is controlled lose marks.
:::

## 1.2 Laboratory work and safety

A science laboratory is a room built for experiments. It contains glassware,
chemicals, heat sources and electrical equipment, and each of these carries its
own danger. Safety is not a set of rules to memorise for the test; it is the
reason you can do the experiment at all.

### 1.2.1 Hazard signs

Laboratories display warning signs so that a person can recognise a danger
before touching anything.

| Sign means | Where you meet it |
|---|---|
| Flammable | spirit, kerosene, alcohol, LPG cylinder |
| Corrosive | strong acids and alkalis, which burn skin and cloth |
| Toxic or poisonous | mercury, pesticides, some laboratory salts |
| Harmful or irritant | dilute acids, lime, bleaching powder |
| Oxidising | potassium permanganate, hydrogen peroxide |
| Explosive | sodium metal in water, dry ice in a closed bottle |

### 1.2.2 Precautions in the laboratory

- Read the whole instruction **before** you start, and follow it in order.
- Wear an apron and, when working with acids or alkalis, safety goggles.
- Never taste a chemical. To smell a gas, fan it towards your nose with your
  hand; never put your nose over the mouth of the bottle.
- Never point the open end of a test tube at yourself or at a classmate.
- Keep your bench clean and keep bags and water bottles off it.
- Light a burner only after the gas has been turned on and the match is ready;
  turn the gas off at the cylinder as well as at the burner when you finish.
- Leave the apparatus as you found it, and wash your hands with soap.

::: tip The three questions before any experiment
**(1)** What am I trying to find out? **(2)** What is the danger in this
apparatus or chemical? **(3)** What will I do if something goes wrong — a spill,
a burn, a broken glass? A student who can answer all three works safely and
also writes a better report.
:::

## 1.3 Experimental work

An experiment is a controlled test of an idea. A good experimental report has
six parts, and they come in the same order every time.

| Part | What it contains |
|---|---|
| Aim | one sentence: what you are finding out |
| Apparatus and materials | the list, with quantities and sizes |
| Procedure | the steps, in order, each one small enough to follow |
| Observation | the readings in a table, with units in the column head |
| Result and calculation | the working, with the formula written first |
| Conclusion | what the readings show, in one or two sentences |

::: example Worked experiment: the effect of mass on melting time
**Aim.** To find out how the time taken by ice to melt depends on its mass.

**Apparatus.** Three equal glass beakers, ice crushed to the same grain size, a
balance, a stopwatch, a thermometer.

**Procedure.**
1. Weigh 50 g of ice and put it in a beaker.
2. Note the room temperature with the thermometer.
3. Start the stopwatch and stir gently. Stop it when no ice is left.
4. Record the time.
5. Repeat with 100 g and with 150 g, keeping the room, the beaker and the
   starting temperature the same.

**Observation.**

| Mass of ice (g) | Time to melt (s) |
|---|---|
| 50 | 240 |
| 100 | 480 |
| 150 | 720 |

**Result.** The time is in the same ratio as the mass:
$\frac{480}{240}=2$ and $\frac{720}{240}=3$, so time is directly proportional to
mass. In symbols, $t\propto m$.

**Conclusion.** Within the range tested, doubling the mass of ice doubles the
time it takes to melt at the same room temperature. The hypothesis was
supported.

**Precaution.** Ice of different grain size melts at different speeds, so all
three samples must be crushed the same way. Stirring must be equally gentle
each time, because stirring warms the mixture.
:::

## 1.4 Research work

Research is a careful search for an answer to a question that is not yet
settled, using both reading and your own observation. A school research project
is small, but it follows the same steps.

1. **Choose a narrow question.** "How much water does a household in my ward
   use in a day?" can be studied in a week. "How can Nepal solve its water
   problem?" cannot.
2. **Read what is already known.** Look for the CDC textbook, a reliable
   website and a newspaper report. Write down where each fact came from.
3. **Plan how to collect evidence.** Decide whether you will measure, count,
   interview or survey.
4. **Collect the evidence honestly.** Never change a reading to make the story
   neater.
5. **Organise it.** Tables and simple graphs.
6. **Write the report.** A school report of this shape is usually enough:
   title, aim, method, findings, conclusion, and a list of sources.

::: caution Copying is not research
Copying three paragraphs from a website and changing a few words is not
research; it is copying, and it teaches nothing. When you use someone else's
finding, say where it came from in your own list of sources. Your own reading
from the meter or your own count of the households is the part that is yours.
:::

## 1.5 Survey

A **survey** is a way of collecting information from many people or places by
asking the same questions of each. It is used when measuring directly is not
possible — for example, to find how many families in a ward separate their
waste.

### 1.5.1 The steps of a survey

1. **Define the aim.** One clear question, such as "How many households in Ward
   5 have a toilet?"
2. **Choose the population.** All the households of Ward 5.
3. **Choose the sample.** Interviewing all 2,000 households is impossible, so
   choose a sample — 100 households. A sample that is chosen by taking every
   twentieth house down each lane is fairer than one made of your own friends.
4. **Prepare the questionnaire.** Short, clear questions with the same choices
   for everyone.
5. **Collect the data.** Ask, and write the answer exactly as given.
6. **Tabulate and show.** A tally table and a bar chart.
7. **Interpret.** Say what the numbers mean, and admit what they cannot show.

```figure caption="Sampling from a ward. A sample chosen along every lane represents the ward; a sample of classmates represents only the school. The way you choose the sample matters more than its size."
fig, ax = plt.subplots(figsize=(4.8, 2.7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.8)
ax.axis("off")
ax.add_patch(plt.Rectangle((0.4, 1.0), 9.2, 4.2, fill=False, ec=GRID, lw=1.2))
ax.text(5.0, 4.75, "Ward 5 — 2000 households", ha="center", fontsize=7.6, color=INK)
for i in range(5):
    y = 1.55 + i * 0.68
    ax.plot([0.8, 9.2], [y, y], color=GRID, lw=0.9)
    if i % 2 == 0:
        for j in range(6):
            x = 1.2 + j * 1.55
            ax.add_patch(plt.Circle((x, y), 0.16, color=ACCENT, alpha=0.85))
ax.text(5.0, 0.55, "coloured houses = the 100 households in the sample", ha="center",
        fontsize=6.8, color=ACCENT)
fig.tight_layout()
```

::: example Worked survey: waste separation in a sample of households
**Aim.** To find how many households in the sample separate degradable and
non-degradable waste.

**Method.** A sample of 40 households was taken — every fifth house on four
lanes. One question was asked of an adult in each house: "Does your household
separate degradable waste from non-degradable waste?

**Observation.**

| Answer | Tally | Number |
|---|---|---|
| Yes, always | IIII IIII IIII IIII II | 22 |
| Sometimes | IIII IIII II | 12 |
| No | IIII I | 6 |
| **Total** | | **40** |

**Result.** The fraction that separates waste always is
$\frac{22}{40}=0.55$, which is $55\%$.

**Conclusion.** In this sample about 55 % of households separate their waste
always. The survey shows what people *said*; it does not prove that they do it,
and 40 households cannot stand for all 2,000. Both limits belong in the report.
:::

## 1.6 Measurement and units

Every measurement has a number and a unit. A length of "5" means nothing; 5 m
does.

| Quantity | SI unit | Symbol | Instrument |
|---|---|---|---|
| Length | metre | m | ruler, tape |
| Mass | kilogram | kg | beam balance |
| Time | second | s | stopwatch |
| Temperature | kelvin | K | thermometer |
| Electric current | ampere | A | ammeter |

Smaller and larger units are made with prefixes: 1 km = 1000 m, 1 m = 100 cm,
1 cm = 10 mm, 1 kg = 1000 g.

::: tip Two habits that protect every reading
**(1)** Write the unit in the column head of your table, never beside every
number. **(2)** Before you record a reading, ask whether it is sensible: a
classroom is about 8 m long, not 8 cm, and a school bag weighs a few kilograms,
not a few grams. If the number looks impossible, the unit or the instrument is
wrong.
:::

## Chapter summary

- Science works by the **scientific method**: observation, question, hypothesis,
  prediction, controlled experiment, analysis, conclusion — and repeat.
- An experiment changes only the **independent** variable, measures the
  **dependent** variable and keeps the **controlled** variables the same.
- Laboratory safety: read first, wear goggles and apron, never taste a
  chemical, never point a test tube at anyone, keep the bench clear, turn the
  gas off at both ends.
- Hazard signs name the danger: flammable, corrosive, toxic, irritant,
  oxidising, explosive.
- An experimental report has aim, apparatus, procedure, observation, result and
  conclusion, in that order.
- A **survey** uses a fair sample, the same questions for everyone, a tally
  table and an honest statement of its limits.
- Every measurement needs a unit, and every reading should be checked for
  reasonableness.

## Practice questions

**Group A — Objective (1 mark each)**

1. The quantity that you change on purpose in an experiment is called the
   <span class="marks">[1]</span>
   (a) dependent variable (b) independent variable (c) controlled variable
   (d) constant
2. The SI unit of mass is <span class="marks">[1]</span>
   (a) gram (b) newton (c) kilogram (d) litre
3. Which sign warns that a chemical burns the skin? <span class="marks">[1]</span>
   (a) flammable (b) corrosive (c) explosive (d) oxidising
4. The first step of the scientific method is <span class="marks">[1]</span>
   (a) conclusion (b) experiment (c) observation (d) hypothesis
5. In the melting-ice experiment, the mass of ice is the
   <span class="marks">[1]</span>
   (a) independent variable (b) dependent variable (c) controlled variable
   (d) result
6. To smell a gas safely you should <span class="marks">[1]</span>
   (a) put your nose over the bottle (b) fan the gas towards your nose with
   your hand (c) taste it first (d) shake the bottle

::: note Answers to Group A
**1.** (b) — the one you choose and change.
**2.** (c) — the kilogram is the SI base unit; the gram is one thousandth of it.
**3.** (b) — corrosive substances attack skin and cloth.
**4.** (c) — everything begins with noticing something.
**5.** (a) — you decide the mass; you then measure the time.
**6.** (b) — fanning brings only a little vapour to the nose.
:::

**Group B — Short answer (2 marks each)**

1. Write any four safety rules of a science laboratory and give the reason for
   each. <span class="marks">[2]</span>
2. What is a controlled experiment? Give one example from daily life.
   <span class="marks">[2]</span>
3. Write the six parts of an experimental report in order.
   <span class="marks">[2]</span>
4. Why must a sample in a survey be chosen fairly, and how can that be done?
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Any four of: wear goggles and apron (protects eyes and clothes); never
taste a chemical (poisonous); never point a test tube at anyone (boiling liquid
may shoot out); keep the bench clear (spills and trips); turn the gas off at
both the burner and the cylinder (gas leak and fire); wash hands with soap after
work (chemicals left on the skin).
**2.** An experiment in which only the independent variable is changed and all
other factors are kept the same. Example: testing whether a plant grows taller
with more water while keeping the same pot, soil, plant and sunlight.
**3.** Aim, apparatus and materials, procedure, observation, result and
calculation, conclusion.
**4.** A sample is meant to stand for the whole population. It is fair if the
houses or people are chosen by a fixed rule — every fifth house on each lane, or
names drawn at random — and not by who is convenient or friendly.
:::

**Group C — Long answer (4 marks each)**

1. Take the question "Does a black surface warm up faster than a white one in
   the sun?" Write the aim, the variables, the procedure with four steps, and
   the conclusion you would expect. <span class="marks">[4]</span>
2. You have to find how many students in your school walk to school. Describe
   your survey: the aim, the population, the sample, the question, the table
   you would use, and one limit of your result. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Aim.** To find whether a black surface warms faster than a white one in
sunlight. **Independent variable.** The colour of the surface. **Dependent
variable.** The temperature of the surface after a fixed time. **Controlled
variables.** Size and material of the two tins, the amount of water, the time
in the sun, the starting temperature, the place. **Procedure.** (1) Fill two
identical tins with the same amount of water; paint one black and the other
white. (2) Put a thermometer in each and record the starting temperature.
(3) Place both side by side in the sun for 30 minutes. (4) Record both
temperatures again every 5 minutes and tabulate. **Expected conclusion.**
The black tin reaches a higher temperature, so a dark surface absorbs heat
faster; this is why dark clothes feel hotter and solar cookers are painted
black.
**2.** **Aim.** To find the fraction of students who walk to school.
**Population.** All students of the school. **Sample.** One class from each
grade, chosen by a fixed rule, giving about 200 students. **Question.** "How do
you come to school — on foot, by bicycle, by bus or by other?" **Table.** Tally
and number for each answer, with a total and a percentage. **One limit.** The
sample includes only the grades present on the day of the survey, so classes
absent for an exam are not represented.
:::
