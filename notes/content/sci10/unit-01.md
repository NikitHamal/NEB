---
subject: Science and Technology
grade: 10
unit: 1
title: Scientific Learning
hours: 0
area: Science and Technology
---

Science is a way of finding out how the world works. Why does a stone fall? Why does milk turn sour? Why do some seeds grow in a week and others in a month? Scientists do not guess the answers. They observe, ask questions, test their ideas and measure carefully. This unit shows you the steps of that method, how an investigation is planned, how we measure with correct units, and how you can do a small science project of your own. Every later unit in this book uses these skills.

::: key What the SEE paper expects from this unit
Expect a 1-mark question on a unit or instrument, a 2-mark question on the steps of the scientific method, and sometimes a 4-mark question on a numerical (unit conversion, least count) or on how to plan a project. Learn the SI units and the steps in the correct order.
:::

## 1.1 Science and scientific method

### What is science?

The word *science* comes from the Latin word *scientia*, meaning "knowledge". Science is the organised study of nature through observation and experiment.

::: definition Science
Science is the systematic and organised body of knowledge about nature, obtained by observation, experiment and reasoning.
:::

Science has three connected parts:

| Part | Meaning | Example |
|---|---|---|
| Knowledge | Facts, laws and theories already established | Water boils at 100 °C at sea level |
| Method | The way in which the knowledge is found | Heating water and recording the temperature |
| Attitude | The habits of mind of a scientist | Curiosity, honesty, patience |

### Scientific attitude

A person with a scientific attitude:

- is **curious** and asks "why" and "how";
- is **honest** and records what really happened, not what he or she wished to happen;
- is **open-minded** and changes an idea when new evidence appears;
- does not believe something only because someone said so; he or she asks for **evidence**;
- is **patient** and repeats an experiment to be sure;
- is **careful** and works with accuracy.

### Branches of science

Science is divided into branches. In this book you meet **Biology** (living things), **Physics** (matter, energy, force, light, electricity), **Chemistry** (substances and their changes), **Astronomy** (stars, planets and the universe) and **ICT** (information and communication technology). A fuller list is given below.

| Branch | What it studies |
|---|---|
| Botany | Plants |
| Zoology | Animals |
| Physics | Matter, energy and their interactions |
| Chemistry | Composition, properties and reactions of substances |
| Geology | Rocks, minerals and the structure of the Earth |
| Astronomy | Heavenly bodies and the universe |
| Ecology | Living things and their surroundings |
| Genetics | Heredity and variation |

### Science and technology

Science finds knowledge. **Technology** uses that knowledge to make useful things and to solve problems. Scientists found how electric current produces a magnetic field; engineers used it to build electric motors. Science is *knowing*; technology is *doing*. Each helps the other: a better microscope (technology) lets biologists see bacteria (science), and what they learn helps make new medicines (technology).

### The scientific method

The **scientific method** is the step-by-step way in which scientists solve a problem. The steps are:

1. **Identifying the problem** – noticing something and asking a clear question.
2. **Observation and collection of information** – looking carefully and reading what is already known.
3. **Forming a hypothesis** – a possible answer that can be tested.
4. **Experiment** – a fair test to check the hypothesis.
5. **Recording data and analysing it** – tables, graphs, calculation.
6. **Drawing a conclusion** – decide whether the hypothesis is supported.
7. **Reporting the result** – so that others can check the work.

```figure caption="Steps of the scientific method. If the experiment does not support the hypothesis, a new hypothesis is made and tested."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,3.4))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
steps = ["1. Identify the problem","2. Observe and collect information","3. Form a hypothesis","4. Do an experiment","5. Record and analyse data","6. Draw a conclusion","7. Report the result"]
ys = [9.0,7.6,6.2,4.8,3.4,2.0,0.6]
for s,y in zip(steps,ys):
    ax.add_patch(FancyBboxPatch((1.2,y-0.45),5.2,0.9,boxstyle="round,pad=0.05",fc="#eaf1ff",ec=ACCENT,lw=1.2))
    ax.text(3.8,y,s,ha='center',va='center',fontsize=8,color=INK)
for i in range(len(ys)-1):
    ax.annotate("",xy=(3.8,ys[i+1]+0.55),xytext=(3.8,ys[i]-0.55),arrowprops=dict(arrowstyle="->",color=INK,lw=1.1))
ax.plot([6.5,8.6,8.6,6.5],[2.0,2.0,6.2,6.2],color=MUTED,lw=1.1,ls='--')
ax.annotate("",xy=(6.5,6.2),xytext=(7.0,6.2),arrowprops=dict(arrowstyle="->",color=MUTED,lw=1.1))
ax.text(9.0,4.1,"Not supported:\nnew hypothesis",ha='center',va='center',fontsize=7,color=MUTED)
```

::: example Worked example 1.1 (applying the method)
**Problem.** Sita notices that the bean seeds she planted in a dark cupboard grew pale yellow, while those kept near the window were green. Write the steps of the scientific method for her problem.

**Solution.**

1. *Problem:* Does light affect the colour of bean seedlings?
2. *Observation:* Seedlings in the dark are yellow; seedlings in light are green.
3. *Hypothesis:* Light is necessary for the formation of green colour (chlorophyll) in plants.
4. *Experiment:* Plant 10 seeds in each of two identical pots with the same soil and water. Keep one pot in light and the other in the dark for 10 days.
5. *Data:* Count the number of green and yellow seedlings in each pot and record them in a table.
6. *Conclusion:* All seedlings in light are green and all in the dark are yellow, so the hypothesis is supported.
7. *Report:* Write the result with the table and share it in the class.
:::

### Hypothesis, theory and law

| Term | Meaning | Example |
|---|---|---|
| Hypothesis | A testable guess made before the experiment | Plants grow faster with more sunlight |
| Theory | A well-tested explanation supported by much evidence | Cell theory |
| Law | A statement of a pattern found to be always true under given conditions | Ohm's law |

::: caution Common mistake
A hypothesis is not the same as a fact. A hypothesis may turn out wrong. Also, a "theory" in science is not a mere guess; it is an explanation that has passed many tests.
:::

## 1.2 Scientific investigation

A **scientific investigation** is a planned study to answer a question. It is more careful than casual observation, because it controls what changes.

### Variables

A **variable** is anything that can change in an experiment.

| Variable | Meaning | In the bean example |
|---|---|---|
| Independent (manipulated) | The one thing we change on purpose | Amount of light |
| Dependent (responding) | What we measure; it changes because of the independent variable | Colour or height of seedlings |
| Controlled (constant) | Everything we keep the same so the test is fair | Soil, water, seed type, temperature |

A **control group** is the set that is kept in normal conditions (or without the treatment) for comparison. The pot kept in light is the control; the pot in the dark is the experimental group.

### Steps of an investigation

1. State the question or aim.
2. Make a hypothesis and predict the result.
3. List the materials and apparatus.
4. Write the procedure so that someone else can repeat it.
5. Observe and collect data (measurements and notes).
6. Present the data in tables and graphs.
7. Analyse the data and find the pattern.
8. Conclude and discuss errors and improvements.

### Observation and inference

An **observation** is what you see, hear, touch, smell or measure. An **inference** is the meaning you give to it. "The candle goes out under the jar" is an observation. "The candle needs air to burn" is an inference. Keep the two separate in your report.

| Observation | Possible inference |
|---|---|
| Wet clothes dry faster in sunshine | Heat increases the rate of evaporation |
| A magnet attracts a nail but not a coin | The nail is magnetic material; the coin is not |
| Leaves of the plant in the shade are larger | Plants may make larger leaves to catch more light |

### Data and graphs

**Data** are the facts and measurements collected. Two kinds exist: **qualitative** (colour, smell, texture) and **quantitative** (numbers with units). Quantitative data are best shown in a table and then a graph. A graph shows the pattern at a glance.

Rules for a good graph:

- Put the independent variable on the horizontal (x) axis and the dependent variable on the vertical (y) axis.
- Give the graph a title and label each axis with the quantity and unit.
- Choose a suitable scale that uses most of the paper.
- Plot the points clearly and draw a smooth line or best-fit straight line.

```figure caption="Extension of a spring against the load hung on it. The points lie close to a straight line through the origin."
import numpy as np, matplotlib.pyplot as plt
load = np.array([0,50,100,150,200,250])
ext = np.array([0,1.0,2.1,2.9,4.1,5.0])
fig, ax = plt.subplots(figsize=(4.4,2.9))
ax.plot(load, 0.02*load, color=ACCENT, lw=1.3)
ax.scatter(load, ext, color=SERIES[1], zorder=3, s=22)
ax.set_xlabel("Load (g)", color=INK); ax.set_ylabel("Extension (cm)", color=INK)
ax.grid(color=GRID, lw=0.6); ax.spines[['top','right']].set_visible(False)
ax.set_xlim(0,270); ax.set_ylim(0,5.6)
ax.text(20,4.3,"Best-fit line",color=ACCENT,fontsize=8)
```

### Accuracy, precision and error

- **Accuracy** means how close a measurement is to the true value.
- **Precision** means how close repeated measurements are to each other.
- **Error** is the difference between the measured value and the true value.

Errors are of two main kinds. A **systematic error** is always in the same direction (for example, a ruler whose end is worn, or a balance that does not read zero at the start). A **random error** changes unpredictably (for example, reaction time in starting a stopwatch). We reduce random error by taking several readings and finding their **mean**.

::: example Worked example 1.2 (mean of readings)
**Problem.** Four students measure the time for 20 swings of a pendulum: 36.2 s, 36.8 s, 36.4 s and 36.6 s. Find the mean time for 20 swings and the time for one swing (the period).

**Solution.**

Mean time for 20 swings = (36.2 + 36.8 + 36.4 + 36.6) / 4 = 146.0 / 4 = 36.5 s.

Period = 36.5 / 20 = 1.825 s ≈ 1.83 s.

Timing 20 swings and dividing reduces the effect of the small error in starting and stopping the watch.
:::

### Safety in the laboratory

- Wear an apron; tie long hair.
- Never taste or directly smell chemicals; waft the vapour gently towards the nose.
- Add acid to water, never water to acid.
- Handle glass, flames and electricity with care.
- Know where the first-aid box and the fire-extinguisher are.
- Wash hands after the experiment and dispose of waste properly.

## 1.3 Measurement and units

To **measure** is to compare an unknown quantity with a standard quantity of the same kind, called a **unit**. A measurement has two parts: a number and a unit. "5" alone is meaningless; "5 m" is a length.

### Physical quantities

A **physical quantity** is anything that can be measured. **Fundamental quantities** do not depend on other quantities. **Derived quantities** are made by combining fundamental ones.

### SI units

All countries use the **International System of Units (SI)**, so that measurements are understood everywhere. The seven fundamental SI quantities are given in the table; you must know the first six.

| Quantity | SI unit | Symbol |
|---|---|---|
| Length | metre | m |
| Mass | kilogram | kg |
| Time | second | s |
| Temperature | kelvin | K |
| Electric current | ampere | A |
| Luminous intensity | candela | cd |
| Amount of substance | mole | mol |

Some useful derived units:

| Quantity | Formula | SI unit |
|---|---|---|
| Area | length × breadth | m² |
| Volume | length × breadth × height | m³ |
| Density | mass / volume | kg m⁻³ |
| Speed | distance / time | m s⁻¹ |
| Force | mass × acceleration | newton (N) |
| Pressure | force / area | pascal (Pa) |
| Energy | force × distance | joule (J) |
| Power | work / time | watt (W) |

### Prefixes

To write very large or very small numbers we put a prefix before the unit.

| Prefix | Symbol | Multiplies by |
|---|---|---|
| kilo | k | 1000 |
| centi | c | 1/100 = 0.01 |
| milli | m | 1/1000 = 0.001 |
| micro | μ | one millionth |
| mega | M | one million |

::: memory Metric ladder
Going from a bigger unit to a smaller one, **multiply**. Going from a smaller unit to a bigger one, **divide**. So 1 km = 1000 m = 100 000 cm, and 250 g = 0.25 kg.
:::

::: example Worked example 1.3 (unit conversion)
**Problem.** Convert (a) 3.5 km to m, (b) 450 g to kg, (c) 72 km/h to m/s.

**Solution.**

(a) 3.5 km = 3.5 × 1000 m = 3500 m.

(b) 450 g = 450 / 1000 kg = 0.45 kg.

(c) 72 km/h = 72 × 1000 m / 3600 s = 72000 / 3600 = 20 m/s.

Shortcut: to change km/h to m/s, multiply by 5/18.
:::

### Measuring instruments

| Quantity | Instrument |
|---|---|
| Length | Metre rule, measuring tape, vernier calliper, screw gauge |
| Mass | Beam balance, electronic balance |
| Time | Stopwatch, clock |
| Volume of liquid | Measuring cylinder, burette, pipette |
| Temperature | Thermometer |
| Current | Ammeter |

### Least count

The **least count** of an instrument is the smallest value it can measure correctly.

- For a metre rule marked in millimetres, the least count is 1 mm = 0.1 cm.
- For a **vernier calliper**: least count = value of 1 main-scale division − value of 1 vernier-scale division. With 1 main division = 1 mm and 10 vernier divisions equal to 9 main divisions, the least count is 1 mm / 10 = 0.1 mm = 0.01 cm.
- For a **screw gauge**: least count = pitch / number of divisions on the circular scale. The pitch is the distance moved by the screw in one full turn. With pitch 1 mm and 100 divisions, the least count is 0.01 mm.

::: tip Reading a vernier calliper
Total reading = main-scale reading + (vernier division that coincides with a main-scale line × least count). Always check the zero error first and correct for it.
:::

```figure caption="Reading a vernier calliper. The zero of the vernier lies just after the 2.3 cm mark, and the 4th vernier line coincides with a main-scale line."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.8,2.4))
ax.axis('off'); ax.set_xlim(1.8,4.2); ax.set_ylim(-1.3,1.6)
ax.add_patch(Rectangle((1.8,0),2.4,0.6,fc="#f4f4f4",ec=INK,lw=1))
for i in range(19,43):
    x=i/10
    h=0.25 if i%5==0 else 0.15
    ax.plot([x,x],[0,h],color=INK,lw=0.8)
    if i%10==0:
        ax.text(x,0.35,str(i//10),ha='center',fontsize=7,color=INK)
ax.text(1.85,0.85,"Main scale (cm)",fontsize=8,color=MUTED)
x0=2.34
ax.add_patch(Rectangle((x0,-0.6),0.9,0.6,fc="#dbe8ff",ec=ACCENT,lw=1))
for k in range(11):
    x=x0+k*0.09
    ax.plot([x,x],[0,-0.2 if k not in (0,5,10) else -0.3],color=INK,lw=0.8)
    if k in (0,5,10):
        ax.text(x,-0.45,str(k),ha='center',fontsize=7,color=INK)
ax.text(x0+0.45,-0.95,"Vernier scale (0-10)",ha='center',fontsize=8,color=MUTED)
ax.text(3.75,-0.95,"Reading = 2.3 + 4 x 0.01\n= 2.34 cm",fontsize=8,color=ACCENT,ha='center')
```

::: example Worked example 1.4 (vernier reading)
**Problem.** A vernier calliper has 1 main-scale division = 1 mm and 10 vernier divisions = 9 main-scale divisions. While measuring the diameter of a marble, the main-scale reading just before the vernier zero is 1.3 cm and the 6th vernier division coincides with a main-scale line. There is no zero error. Find the diameter.

**Solution.**

Least count = 1 mm − 0.9 mm = 0.1 mm = 0.01 cm.

Diameter = 1.3 cm + 6 × 0.01 cm = 1.3 cm + 0.06 cm = 1.36 cm.
:::

::: example Worked example 1.5 (screw gauge and density)
**Problem.** A screw gauge has pitch 1 mm and 100 circular divisions. A wire reads 0 mm on the main scale and 45 on the circular scale. Find the diameter of the wire. A solid cube of side 2.0 cm has mass 21.6 g. Find its density.

**Solution.**

Least count = 1 mm / 100 = 0.01 mm.

Diameter = 0 mm + 45 × 0.01 mm = 0.45 mm.

Volume of cube = (2.0 cm)³ = 8.0 cm³.

Density = mass / volume = 21.6 / 8.0 = 2.7 g cm⁻³ = 2700 kg m⁻³. (This is the density of aluminium.)
:::

### Measuring volume

To read a measuring cylinder, keep your eye level with the liquid surface and read the bottom of the curved surface (the **meniscus**) of water. Reading from above or below gives an error called **parallax error**. The volume of an irregular solid, such as a stone, is found by lowering it into water: volume of stone = new level − first level.

::: caution Common mistake
Do not write mass in grams in the density formula when the volume is in m³. Convert first, or use g cm⁻³ with cm³. Also do not forget that the SI unit of mass is the kilogram, not the gram.
:::

### Significant figures and rounding

Digits that are known with certainty plus one uncertain digit are called **significant figures**. A reading of 1.36 cm has three. Never give an answer with more digits than the data allow. If a calculator gives 2.7142857 for data with two figures, write 2.7.

## 1.4 Project work

A **project** is a small investigation that you plan and carry out yourself, over some days or weeks, and then report. Project work trains you to solve real problems, to work in a team, and to present results. Under the Grade 10 curriculum it also earns internal marks.

### Steps of a project

1. **Select the topic.** It should be interesting, small enough, safe, and possible with local materials. Examples: the effect of fertiliser on bean growth; types of waste in our school; water quality of the local tap; plants in my neighbourhood used as medicine; the energy used by a home in a month.
2. **Plan.** Write the aim, hypothesis, materials, methods, time table and who does what.
3. **Collect data.** Experiment, survey, interview or observe. Record in a notebook with dates.
4. **Analyse data.** Make tables, graphs, averages and percentages.
5. **Draw conclusions.** Answer the original question honestly.
6. **Report and present.** Write a report and show it to the class or school.

### Parts of a project report

| Part | Content |
|---|---|
| Title page | Title, name, class, school, date |
| Acknowledgement | Thanks to those who helped |
| Introduction and objectives | Why the work was done; what question it answers |
| Methodology | Materials, procedure, sample, place and time |
| Data and analysis | Tables, charts, calculations |
| Findings and conclusion | What was found; limits of the work |
| Recommendations | Suggestions for action |
| References | Books, websites, people consulted |

### Types of project work

- **Experimental project:** a fair test, such as growing plants with and without compost.
- **Survey project:** collecting information from many people or places, such as a study of the use of plastic bags in a bazaar.
- **Model-making project:** building a working model, such as a water filter or a model of the solar system.
- **Collection project:** gathering and identifying specimens, such as leaves or rocks (take only what you need and do not harm nature).

### A sample project plan

**Title:** Effect of plastic mulch on the growth of tomato seedlings.
**Hypothesis:** Seedlings with mulch will grow taller because the soil keeps more water.
**Independent variable:** presence of mulch. **Dependent variable:** height in cm after 3 weeks. **Controlled variables:** soil, seed variety, water volume, sunlight.

| Week | Height without mulch (cm) | Height with mulch (cm) |
|---|---|---|
| 1 | 3.0 | 3.4 |
| 2 | 5.1 | 6.0 |
| 3 | 7.2 | 8.8 |

From the table, the seedlings with mulch grew 8.8 − 7.2 = 1.6 cm more in three weeks, so the hypothesis is supported for this small sample. A good report would also say that more plants and a longer time are needed to be sure.

::: tip Ethics of project work
Report your true data even if it disagrees with your hypothesis. Do not copy from others. Give credit to the sources you used. Respect people's privacy in surveys and ask permission before collecting samples from private land.
:::

## Chapter summary

- Science is the organised study of nature through observation and experiment; technology applies scientific knowledge to solve problems.
- The scientific method: problem → observation → hypothesis → experiment → data analysis → conclusion → report.
- In an experiment there is one independent variable, a dependent variable that we measure, and controlled variables kept constant; a control group is used for comparison.
- Accuracy is closeness to the true value; precision is closeness of repeated readings. Taking the mean of several readings reduces random error.
- SI base units: metre (m), kilogram (kg), second (s), kelvin (K), ampere (A), candela (cd), mole (mol). Going to a smaller unit, multiply; to a bigger unit, divide.
- Least count of a vernier = 1 MSD − 1 VSD (usually 0.01 cm); of a screw gauge = pitch / number of circular divisions (usually 0.01 mm).
- Density = mass / volume; km/h to m/s: multiply by 5/18.
- A project follows these steps: topic, plan, data collection, analysis, conclusion, report. A report has an introduction, methods, analysis, conclusion and references.

## Practice questions

**Group A — Objective questions (1 mark each)**

1. Which one is the correct order of the first three steps of the scientific method? <span class="marks">[1]</span>
   (a) hypothesis, problem, observation (b) problem, observation, hypothesis (c) experiment, hypothesis, problem (d) conclusion, problem, hypothesis
2. The SI unit of temperature is <span class="marks">[1]</span>
   (a) degree Celsius (b) degree Fahrenheit (c) kelvin (d) calorie
3. The least count of a screw gauge with pitch 0.5 mm and 50 circular divisions is <span class="marks">[1]</span>
   (a) 0.1 mm (b) 0.01 mm (c) 0.05 mm (d) 0.001 mm
4. The variable that a scientist keeps the same in a fair test is called the <span class="marks">[1]</span>
   (a) dependent variable (b) independent variable (c) controlled variable (d) random variable
5. Technology is best described as <span class="marks">[1]</span>
   (a) a guess about nature (b) application of scientific knowledge (c) the study of stars (d) a type of experiment
6. Fill in the blank: A testable guess made before an experiment is called a ______. <span class="marks">[1]</span>
   (a) law (b) theory (c) hypothesis (d) result

::: note Answers to Group A
**1.** (b) — we first state the problem, then observe, then form a hypothesis.
**2.** (c) — the kelvin is the SI unit of temperature.
**3.** (b) — 0.5 mm / 50 = 0.01 mm.
**4.** (c) — controlled variables are kept constant so that the test is fair.
**5.** (b) — technology uses knowledge to make useful things.
**6.** (c) — a hypothesis is tested by experiment.
:::

**Group B — Short answer (2 marks each)**

1. Define science and technology. <span class="marks">[2]</span>
2. Differentiate between accuracy and precision. <span class="marks">[2]</span>
3. What is the least count of an instrument? Write the least count of a metre rule marked in millimetres. <span class="marks">[2]</span>
4. Convert 90 km/h into m/s. <span class="marks">[2]</span>
5. What is a control group? Why is it used? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Science is the organised body of knowledge about nature obtained by observation and experiment. Technology is the application of scientific knowledge to make useful things and solve problems.
**2.** Accuracy is how close a measurement is to the true value. Precision is how close repeated measurements are to one another. A measurement can be precise but not accurate if there is a systematic error.
**3.** The least count is the smallest value that an instrument can measure correctly. For a metre rule marked in mm it is 1 mm (0.1 cm).
**4.** 90 × 5/18 = 25 m/s.
**5.** A control group is the set of subjects kept under normal conditions without the change being tested. It is used for comparison, so we can tell whether the change really caused the result.
:::

**Group C — Long answer (4 marks each)**

1. Describe the steps of the scientific method with a suitable example. <span class="marks">[4]</span>
2. A vernier calliper has 10 vernier divisions equal to 9 main-scale divisions, each main division being 1 mm. The main-scale reading is 2.5 cm and the 7th vernier line coincides. Find the least count and the reading. If the instrument has a zero error of +0.02 cm, find the corrected reading. <span class="marks">[4]</span>
3. A stone of mass 150 g is lowered into a measuring cylinder. The water level rises from 40 mL to 100 mL. Find the volume and the density of the stone in g cm⁻³ and in kg m⁻³. <span class="marks">[4]</span>
4. You are asked to do a project on "waste produced in our school". Write the steps you would follow and the parts of the report. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Steps: identify the problem, observe and collect information, form a hypothesis, experiment, record and analyse data, draw a conclusion, report. Example: if seeds are kept with and without water, the problem is "do seeds need water to germinate?", the hypothesis is "seeds need water", two sets are kept with the same conditions except water, germination is counted, and the conclusion is that seeds without water do not germinate.
**2.** Least count = 1 mm − 0.9 mm = 0.1 mm = 0.01 cm. Reading = 2.5 + 7 × 0.01 = 2.57 cm. Corrected reading = 2.57 − 0.02 = 2.55 cm.
**3.** Volume = 100 − 40 = 60 mL = 60 cm³. Density = 150 / 60 = 2.5 g cm⁻³ = 2500 kg m⁻³.
**4.** Steps: choose the topic and aim; plan the methods and time table; collect data by counting and weighing the waste from each class for a week; present the data in tables and bar graphs; analyse which waste is largest; conclude and recommend (for example separate bins and composting). Report parts: title page, acknowledgement, introduction and objectives, methods, data and analysis, findings and conclusion, recommendations, references.
:::
