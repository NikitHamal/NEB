---
subject: Science and Technology
grade: 8
unit: 1
title: Scientific Learning
hours: 0
area: Science and Technology
---

Scientists learn about nature by doing things: they observe, test, do research,
carry out surveys, make models and do project work. These activities can be
done inside a laboratory or outside it, in a garden, a field or a village.
Facts, theories and rules of science are discovered through such work. This
unit teaches you how to do each kind of work safely, how to record what you
find, and how to write a short report at the end. Every later unit of this book
uses these skills.

::: key What this unit asks of you
You should be able to: list the safety rules of a science laboratory and give
the reason for each; define **observation**, **test**, **experiment**,
**research** and **survey** and tell them apart; write the steps of research and
of a survey in order; and write a report with a title, objective, materials,
method, observation (or analysis) and conclusion.
:::

## 1.1 Science and the scientific method

**Science** is organised knowledge about the natural world that is gained by
observation and testing. A statement is scientific only if it can be checked by
observation or experiment.

The CDC textbook names the main **activities of scientific learning**:

| Activity | What you do | Example |
|---|---|---|
| Observation | study an object or event carefully with the sense organs (and instruments) | watching a caterpillar turn into a butterfly |
| Test | check whether a guess (hypothesis) is right by a fixed procedure | testing lemon juice with litmus paper |
| Experiment | use observation, tests and model making to check a theory or principle | showing that a plant needs sunlight to make starch |
| Research | study a question in depth, step by step, to find its answer | finding what makes algae grow in a pond |
| Survey | collect information directly from people or places and draw a conclusion | asking 50 households how they manage waste |
| Project work and model making | plan and complete a longer piece of work, or build a model | a model of the solar system |

### 1.1.1 The scientific method

Most scientific work follows the same order, called the **scientific method**.

1. **Observation.** Notice something and describe it exactly.
2. **Question.** Turn it into a question that can be answered. *Does a plant
   need sunlight to make food?*
3. **Hypothesis.** Make a guess that can be tested. *A leaf kept in the dark
   will not make starch.* In scientific learning, a guess or inference made from
   an observation is called a **hypothesis**.
4. **Test or experiment.** Change one thing, keep everything else the same, and
   record what happens.
5. **Analysis.** Arrange the results in a table or graph and look for a pattern.
6. **Conclusion.** Say whether the hypothesis is right. If it is wrong, find the
   weakness, improve the hypothesis and try again.

```figure caption="The scientific method is a loop. If the result does not support the hypothesis, the scientist improves the hypothesis and tests again."
fig, ax = plt.subplots(figsize=(5.0, 2.2))
ax.set_xlim(0, 10)
ax.set_ylim(2.25, 3.5)
ax.axis("off")
steps = ["Observation", "Question", "Hypothesis", "Test /\nexperiment", "Analysis", "Conclusion"]
xs = [0.85, 2.5, 4.15, 5.8, 7.45, 9.1]
for name, x in zip(steps, xs):
    ax.text(x, 3.2, name, ha="center", va="center", fontsize=7.6, color=INK,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=ACCENT, lw=1.1))
for a, b in zip(xs[:-1], xs[1:]):
    ax.annotate("", xy=(b - 0.78, 3.2), xytext=(a + 0.78, 3.2),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
ax.annotate("", xy=(4.15, 2.9), xytext=(9.1, 2.9),
            arrowprops=dict(arrowstyle="->", color=SERIES[1], lw=1.3,
                            connectionstyle="arc3,rad=-0.22"))
ax.text(6.6, 2.4, "hypothesis not supported: improve it and test again",
        ha="center", fontsize=7.4, color=SERIES[1])
fig.tight_layout()
```

### 1.1.2 Variables in an experiment

| Kind of variable | Meaning | Example (plant and sunlight) |
|---|---|---|
| Independent | the one you change on purpose | light or dark |
| Dependent | the one you measure or observe | whether the leaf has starch |
| Controlled | the ones you keep the same | kind of plant, water, soil, temperature |

::: definition Controlled experiment
A **controlled experiment** is one in which only one factor is changed and every
other factor that could affect the result is kept the same. Only then can we
say which change caused the result.
:::

::: caution Changing two things at once
If one plant is kept in the dark *and* given less water, and it does badly, you
cannot say whether darkness or dryness was the cause. Change only one factor.
:::

## 1.2 Laboratory work and safety

A **science laboratory** is a special room for scientific study and experiments.
The equipment and chemicals needed for study and research are kept there.
Working carelessly in a laboratory can cause accidents, and it can also spoil
the results of observations, tests and experiments. So everyone must follow the
safety rules.

### 1.2.1 Hazard signs

A notice with warning signs is pasted in the laboratory. Each sign tells you
the danger *before* you touch a bottle.

| Sign | Meaning | Examples |
|---|---|---|
| Flame | catches fire easily (flammable) | spirit, kerosene, alcohol |
| Test tube dripping on a hand | corrosive: burns skin, eats cloth and metal | concentrated acids, caustic soda |
| Skull and crossbones | toxic (poisonous) | mercury, some pesticides |
| Exclamation mark | harmful or irritant | dilute acids, bleaching powder |
| Flame over a circle | oxidising: makes other things burn fiercely | potassium permanganate |
| Exploding ball | explosive | sodium metal with water |

### 1.2.2 Safety rules in the laboratory

These are the rules given in the textbook. The reason is what an examiner wants
when the question says "why".

| Rule | Reason |
|---|---|
| Do not handle materials carelessly. | glass breaks and chemicals spill |
| Wear masks, gloves and goggles with harmful chemicals. | protects the nose, skin and eyes |
| Wear an apron or lab coat. | protects body and clothes from chemicals |
| Know where the emergency exit is. | you can leave quickly in a fire |
| Wash hands with soap after the work. | removes chemicals and germs |
| Do not eat or drink in the laboratory. | food may pick up chemicals |
| Never taste or directly smell a chemical. | many chemicals are poisonous or corrosive |
| No playing or teasing. | causes spills, burns and broken glass |
| Follow the prescribed method. | wrong steps can be dangerous and give wrong results |
| Take special care with burners and hot objects. | prevents burns and fire |
| Do not put hot apparatus directly on the table. | it can burn the table or crack |

Two more rules are often asked: **hold a test tube with a test-tube holder**
while heating it and never point its mouth at anyone; and **do any reaction that
gives off fumes in a fume hood** (a cupboard with a fan that takes the fumes
outside), or at least near an open window.

::: tip To smell a substance safely
If the teacher asks you to note a smell, do not put your nose over the mouth of
the bottle. Hold it away from your face and wave a little of the vapour towards
your nose with your hand.
:::

## 1.3 Experimental work: observation, test and conclusion

**Experimentation** is drawing conclusions by using science process skills such
as observation, research, tests and model making, in order to check theories
and principles. If the expected result is not obtained, other ways are tried.
An experiment may be done inside or outside the laboratory, but the safety
rules must always be followed.

### 1.3.1 Observation

::: definition Observation
**Observation** is the process of experiencing an object, event or process very
carefully using the sense organs.
:::

We observe by seeing with the eyes, hearing with the ears, smelling with the
nose, touching with the skin and tasting with the tongue (tasting is never
allowed with laboratory chemicals). When the sense organs are not enough, we use
instruments such as a **hand lens** or a **microscope**.

*Example from the textbook.* Mamta kept a caterpillar on a leaf in an open jar
and gave it fresh soft leaves every day. After 15–16 days it became a pupa and
stopped eating. After another 13–14 days a yellow butterfly with black spots came
out. By careful, day-by-day observation she learnt the life cycle herself.

Observation is not limited to the laboratory. We can also observe at home, in
the school garden, in a zoo, a botanical garden or a factory. Before observing,
be clear about **what** to observe, **why**, and **how** you will present the
information.

```photo id="sci10/microscope" caption="A compound microscope. When the eye alone cannot see the detail, a microscope extends the sense of sight." width="58"
```

::: example Report of an observation (Activity 1.1): observation of fungi
**Title.** Observation of fungi.

**Objective.** To study the structure of fungi.

**Materials.** Bread, water, forceps, glass slide, cover slip, methylene blue,
microscope.

**Method.** (i) A piece of bread was taken, a little water was sprinkled on it
and it was kept covered in a moist place. (ii) A little water was sprinkled every
day. (iii) After a few days fungus appeared on the bread. (iv) Some threads of the
fungus were placed in a drop of methylene blue on a slide with forceps, covered
with a cover slip and observed under the microscope.

**Result.** (i) No green pigment was seen. (ii) Root-like threads (rhizoids) were
seen. (iii) Stem-like threads called hyphae were seen; the network of hyphae is
the mycelium. (iv) Round sporangia were seen at the tips of long, upright hyphae.

**Precautions.** Forceps are sharp, so use them carefully. Do not let the fungus
get into the mouth or eyes.
:::

### 1.3.2 Scientific test

Observation alone cannot tell us everything. From an observation we make a
guess (hypothesis). A **test** is a scientific procedure, done inside or outside
the laboratory, to check whether the hypothesis is true. Testing is also a kind
of experimental work. Before a test, be clear about what is being tested, what
the hypothesis is, which materials are needed and how the results will be shown.

::: example Report of a test (Activity 1.3): acids, bases and salts
**Title.** Test of acids, bases and salts.

**Objective.** To identify whether the given substances are acids, bases or
salts with the help of indicators.

**Materials.** Lemon juice, soap water, salt water, red and blue litmus paper,
three test tubes.

**Method.** The three liquids were put in separate test tubes. Red and blue
litmus paper were dipped in each one by one and the colour change was noted.

**Observation.**

| Indicator | Lemon juice | Soap water | Salt water |
|---|---|---|---|
| Red litmus | no change | turns blue | no change |
| Blue litmus | turns red | no change | no change |

**Conclusion.** Lemon juice is an **acid** because it turns blue litmus red. Soap
water is a **base** because it turns red litmus blue. Salt water is **neutral**
(a salt solution) because neither paper changes colour.
:::

```photo id="sci10/litmus" caption="Litmus paper. Blue litmus turns red in an acid; red litmus turns blue in a base." width="56"
```

### 1.3.3 Recording observations and drawing conclusions

- Record readings **at the time** you take them, in a table, with the unit in
  the column heading.
- Write what you actually saw, not what you expected.
- The **conclusion** answers the objective in one or two sentences, using the
  evidence. *Example:* "Lemon juice is acidic because it turned blue litmus red."
- A report is written after every observation, test, experiment or survey so
  that others can understand, repeat and check the work.

## 1.4 Research work

Research begins with a question or curiosity. **Research** is a study in depth
to find the answer to a question. All discoveries are the results of such
study. A researcher must work patiently by a fixed procedure. If the work fails,
the researcher finds the weakness, improves it and tries again.

::: memory Steps of research work (textbook order)
1. Goal setting (fixing the objective)
2. Making a hypothesis (inference)
3. Choosing the method of collecting data
4. Preparing the required materials
5. Collecting data
6. Analysing the data
7. Conclusion
:::

### 1.4.1 An example of research: what makes algae grow?

Rusa and Samprit wondered how manure used in fields can pollute water. Plants do
not take up all the fertiliser. Rain washes the extra fertiliser into rivers,
lakes and ponds. There it makes **algae** grow fast. The algae use up the
dissolved oxygen, so fish and other water animals suffer. They tested this idea.

::: example Research report (Activity 1.6): effect of fertiliser and acid on algae
**Research title.** Effects of chemical fertiliser and acid on the growth of algae.

**Objective.** To find out the role of chemical fertiliser and acid in the growth
of algae.

**Materials.** Pond water containing algae, three glass bottles, chemical
fertiliser, vinegar.

**Method.** (i) Pond water with algae was brought from a nearby pond. (ii) Three
bottles were half filled with equal amounts of it. (iii) Nothing was added to the
first bottle (labelled *pond water*). (iv) A little fertiliser was added to the
second (labelled *water with fertiliser*). (v) A little vinegar was added to the
third (labelled *water with vinegar*). (vi) The bottles were observed every five
days for 15–20 days.

**Observation.**

| Time | Bottle 1 (pond water only) | Bottle 2 (fertiliser) | Bottle 3 (vinegar) |
|---|---|---|---|
| Start | about the same in all three | about the same | about the same |
| After 15–20 days | some growth | much faster growth | algae started to die |

**Conclusion.** Chemical fertiliser **helps** the growth of algae (positive
role), while acid **harms** it (negative role).
:::

Bottle 1 is the **control**: it shows what happens when nothing is added, so we
can compare the other two with it.

::: note Activity 1.7 — black or white?
Take two identical tins with the same amount of water and the same starting
temperature. Paint (or wrap) one black and the other white. Keep both in the sun
for 30 minutes and read the temperature every 5 minutes. The water in the black
tin becomes warmer. **Conclusion:** a black surface absorbs more heat than a
white one. This is why dark clothes feel hotter in summer and solar cookers are
painted black inside.
:::

::: caution Copying is not research
Copying from a website or a guidebook is not research. Your own measurements and
your own counts are the research; any fact you take from a book must be named
in the report.
:::

## 1.5 Survey

::: definition Survey
A **survey** is the process of collecting data about a topic or problem directly
(from people, households or places) and drawing a conclusion from it.
:::

A survey is used when the information is spread among many people or places
and cannot be found in a laboratory — for example, whether farmers of an area use
more chemical or organic fertiliser, or how families store food.

**Survey tools** are the means used to collect data: a **questionnaire** (a
written list of questions), an **interview** (asking questions face to face), a
**discussion** with a group, and **observation** of the place.

::: memory Steps of a survey (textbook order)
1. Selecting the objective
2. Choosing the data collection method
3. Collecting the data
4. Analysing the data
5. Conclusion (and suggestions)
:::

The survey report contains the **title**, **background**, **objective**,
**method/tools of data collection**, **analysis of data**, **conclusion and
suggestions**, and the questionnaire as an annex.

### 1.5.1 Sample and sampling

Usually we cannot ask everyone, so we ask a **sample** — a part chosen to stand
for the whole group (the **population**). The sample should be chosen fairly,
for example every fifth house along each lane, not only the houses of friends.

### 1.5.2 Example: survey on solid waste management (Activity 1.8)

**Title.** A study of solid waste management in a village of Kathmandu.
**Objective.** To study how households manage their solid waste.
**Method.** A questionnaire was prepared and 50 households were surveyed.

**Analysis of data.**

| What the household does | Percentage | Number of houses (out of 50) |
|---|---|---|
| gives all waste to the municipality vehicle without separating | 50 % | 25 |
| makes compost from degradable waste | 30 % | 15 |
| makes compost from degradable waste and reuses non-degradable waste | 20 % | 10 |
| **Total** | **100 %** | **50** |

The number of houses is found as percentage × 50 ÷ 100; for example
$\frac{30\times50}{100}=15$.

```figure caption="Bar diagram of the solid-waste survey of 50 households (textbook Activity 1.8)."
fig, ax = plt.subplots(figsize=(4.8, 2.6))
labels = ["not separated", "compost from\ndegradable waste", "compost + reuse of\nnon-degradable"]
vals = [50, 30, 20]
bars = ax.bar(range(3), vals, color=[SERIES[1], SERIES[2], ACCENT], width=0.55)
for i, v in enumerate(vals):
    ax.text(i, v + 1.5, f"{v} %", ha="center", fontsize=8, color=INK)
ax.set_xticks(range(3))
ax.set_xticklabels(labels, fontsize=7.6)
ax.set_ylabel("percentage of houses", fontsize=8)
ax.set_ylim(0, 60)
ax.tick_params(axis="y", labelsize=7.6)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

**Conclusion.** Half the houses still mix their waste, but the other half have
started composting and reusing waste. **Suggestion:** the municipality should
teach every household to separate degradable and non-degradable waste.

**Annex — part of the questionnaire.** (1) What do you do with the solid waste
from your house? (a) give it to the collectors (b) manage part at home and give
the rest (c) manage all at home. (2) What do you do with biodegradable waste?
(a) make compost (b) throw it on the road or in the river (c) give it to the
collectors. (3) What do you do with non-biodegradable waste? (a) make other
things from it (b) give it to the collection agency (c) burn or bury it.

## 1.6 Measurement and units; project work

Every result in science needs a measurement, and every measurement has a
**number and a unit**. "5" means nothing; "5 m" does.

| Quantity | SI unit | Symbol | Instrument |
|---|---|---|---|
| Length | metre | m | metre rule, measuring tape |
| Mass | kilogram | kg | beam balance, digital balance |
| Time | second | s | stopwatch |
| Temperature | kelvin (°C in daily use) | K | thermometer |
| Electric current | ampere | A | ammeter |
| Volume of a liquid | cubic metre (litre, ml in daily use) | m³ | measuring cylinder |

Useful conversions: 1 km = 1000 m, 1 m = 100 cm, 1 cm = 10 mm, 1 kg = 1000 g,
1 l = 1000 ml, 1 ml = 1 cm³.

**Honest readings.** Read a scale with the eye level with the mark (otherwise
you get a *parallax error*); take three readings and use the average; never
change a reading to make the result look better.

::: example Measuring the volume and density of a stone
**Problem.** A stone of mass 84 g is lowered into a measuring cylinder holding
40 ml of water. The level rises to 72 ml. Find the volume and the density of the
stone. Will it float in water?

**Solution.**
Volume of stone = 72 ml − 40 ml = 32 ml = 32 cm³.
Density $=\frac{\text{mass}}{\text{volume}}=\frac{84\ \text{g}}{32\ \text{cm}^3}=2.625$ g/cm³.
Water has density 1 g/cm³. The stone is denser than water, so it **sinks**.
:::

::: example Average of repeated readings
**Problem.** Three students measured the length of a bench as 152 cm, 150 cm and
151 cm. Find the average length in metres.

**Solution.** Average $=\frac{152+150+151}{3}=\frac{453}{3}=151$ cm $=1.51$ m.
:::

**Project work** is a longer piece of work done over days or weeks — for example
growing seeds under different conditions, making a model of a solar cooker, or
surveying the water sources of a ward. A project is planned like research
(objective, method, materials, time plan), and ends with a report and a
presentation in class.

## Chapter summary

- Scientific learning uses **observation, test, experiment, research, survey,
  project work and model making**.
- **Observation** is experiencing an object, event or process carefully with the
  sense organs; a hand lens or microscope helps. It is the first step of any
  scientific study.
- A **hypothesis** is a guess made from observation; a **test** checks whether it
  is true. In an experiment only one factor is changed.
- Laboratory rules: apron/lab coat, gloves and goggles with harmful chemicals,
  no eating, drinking, tasting or direct smelling, no playing, test-tube holder
  for heating, fumes in a fume hood, wash hands after work.
- **Research** steps: goal setting → hypothesis → choice of data-collection
  method → materials → data collection → analysis → conclusion.
- **Survey** steps: objective → method → data collection → analysis →
  conclusion; tools are questionnaire, interview, discussion and observation.
- Every activity ends with a **report**: title, objective, materials, method,
  observation/analysis, conclusion.
- Every measurement needs a number and a unit; density = mass ÷ volume.

## Practice questions

**Group A — Multiple choice (1 mark each)** *(Questions 1–5 are the textbook exercise.)*

1. What is the process of experiencing an object, event or process carefully through the sense organs? <span class="marks">[1]</span>
   (a) test (b) hypothesis (c) curiosity (d) observation
2. Which method suits a study of whether the farmers of a region use more chemical or organic fertiliser? <span class="marks">[1]</span>
   (a) observation (b) test (c) research (d) survey
3. Which of these would you stop your friend from doing in the laboratory? <span class="marks">[1]</span>
   (a) tasting or smelling laboratory chemicals (b) wearing a lab coat (c) boiling water in a beaker (d) using a test-tube holder while heating
4. What should be done while performing a chemical reaction that produces fumes? <span class="marks">[1]</span>
   (a) keep hands away (b) do it on a table (c) keep it on a stand (d) do it in a fume hood
5. Which is the first step of a scientific study? <span class="marks">[1]</span>
   (a) investigation (b) observation (c) testing (d) experimentation
6. In the algae research, the bottle with only pond water is the <span class="marks">[1]</span>
   (a) control (b) hypothesis (c) conclusion (d) questionnaire

::: note Answers to Group A
**1.** (d) — this is the definition of observation.
**2.** (d) — the data must be collected directly from many farmers.
**3.** (a) — chemicals may be poisonous or corrosive.
**4.** (d) — a fume hood carries harmful fumes out of the room.
**5.** (b) — every study begins by noticing something.
**6.** (a) — nothing is added to it, so the others are compared with it.
:::

**Group B — Short answer (2 marks each)** *(Textbook exercise questions 2–4.)*

1. Distinguish between (a) observation and test (b) research and survey. <span class="marks">[2]</span>
2. Give reasons: (a) Precautions should be taken while doing experimental work. (b) A report is prepared after an experiment or survey. (c) Observation is the first step in scientific learning. <span class="marks">[3]</span>
3. What is observation? Why is it important in scientific work? <span class="marks">[2]</span>
4. What is done in scientific work when observation does not give enough information? <span class="marks">[2]</span>
5. What precautions should be taken while carrying out a scientific experiment? <span class="marks">[2]</span>
6. List the things that should be done and should not be done in the laboratory. <span class="marks">[2]</span>
7. What should we pay attention to while doing research? <span class="marks">[2]</span>
8. In what conditions is a survey conducted? What are survey tools? Give examples. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** (a) *Observation* is studying an object or event carefully with the sense organs (or instruments) without changing it; it gives information and leads to a guess. A *test* is a fixed scientific procedure to check whether that guess (hypothesis) is true, e.g. dipping litmus in lemon juice. (b) *Research* is an in-depth study of a question, often with experiments, following steps from goal setting to conclusion; it may be done in a laboratory. A *survey* collects data directly from people or places through questionnaires, interviews, discussion or observation, and draws a conclusion from them.
**2.** (a) Laboratory chemicals, glass and burners can cause injury, fire or poisoning, and careless work also gives wrong results. (b) A report records the objective, method, results and conclusion so that others can understand, check and repeat the work, and so that the findings can be used. (c) All scientific work starts from something noticed; observation gives the information from which questions and hypotheses are made.
**3.** Observation is the process of experiencing an object, event or process very carefully using the sense organs. It is important because it gives the first information about a thing, helps us make hypotheses and records the results of tests and experiments.
**4.** A hypothesis is made from the observation, and a test or experiment is carried out to check it. Instruments such as a hand lens or microscope may also be used to observe more closely.
**5.** Follow the given method; wear an apron, gloves and goggles; never taste or directly smell chemicals; use a test-tube holder and point the tube away from people; take care with burners and hot objects; do reactions that give fumes in a fume hood; keep hot apparatus off the bare table; wash hands afterwards.
**6.** *Do:* wear a lab coat, follow instructions, know the emergency exit, use holders and tongs, keep the bench clean, wash hands after work. *Do not:* eat or drink, taste or smell chemicals, play or tease, handle materials carelessly, put hot apparatus directly on the table.
**7.** Have a clear question and objective; follow the steps in order; collect data honestly; keep a control for comparison; repeat if it fails and improve the method; be patient; write a report and name the sources used.
**8.** A survey is done when the information is spread among many people, households or places (e.g. waste management in a community, use of fertiliser by farmers) and must be collected directly. Survey tools are the means of collecting data: questionnaire, interview, group discussion and observation.
:::

**Group C — Long answer (4 marks each)** *(Textbook exercise 4 (i) and (j), plus one more.)*

1. Elina wants to study whether green plants need sunlight. Suggest a clear method for her. <span class="marks">[4]</span>
2. A class must be held in the absence of the science teacher. Prepare a worksheet for a practical class on the study of plant and animal cells. <span class="marks">[4]</span>
3. Plan a survey of 30 families on the methods they use to preserve food. Write the objective, method, three questionnaire items and the parts of the report. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Objective:** to find whether sunlight is needed for a green plant to make starch. **Materials:** a potted plant, black paper, clips, alcohol, beaker, water bath, iodine solution, dropper. **Method:** (i) Keep the plant in the dark for 2 days so that its leaves lose their starch. (ii) Cover part of one leaf on both sides with black paper. (iii) Keep the plant in sunlight for 5–6 hours. (iv) Pluck the leaf, boil it in water, then warm it in alcohol on a water bath to remove the green colour. (v) Wash it and add iodine solution. **Observation:** the uncovered part turns blue-black; the covered part does not. **Conclusion:** starch is made only in the part that got sunlight, so sunlight is necessary for photosynthesis. **Precaution:** never heat alcohol over a direct flame; use a water bath.
**2.** **Title:** Study of plant and animal cells. **Objective:** to observe and draw an onion-peel cell and a human cheek cell. **Materials:** onion, clean toothpick, slides, cover slips, iodine or methylene blue, water, forceps, needle, microscope. **Steps:** (i) Peel a thin layer from the inside of an onion scale, place it in a drop of water on a slide, add a drop of iodine, cover gently. (ii) Scrape the inside of your cheek gently with the flat end of a clean toothpick, spread it on another slide, add methylene blue and cover. (iii) Observe both under low power then high power. **Questions for the worksheet:** Draw and label each cell. Which cell has a cell wall? Which shows a large vacuole? Write two differences between the two cells. **Precautions:** avoid air bubbles under the cover slip; use a fresh toothpick; wash hands.
**3.** **Objective:** to find the methods families use to preserve food. **Method:** questionnaire and interview of 30 families chosen fairly (e.g. every third house). **Questionnaire:** (1) Which foods do you preserve? (2) Which method do you use — drying, salting, pickling, refrigeration, smoking, other? (3) How long does the food stay good? **Report parts:** title, background, objective, data collection method, analysis (table and bar diagram of methods), conclusion and suggestions, annex (questionnaire).
:::
