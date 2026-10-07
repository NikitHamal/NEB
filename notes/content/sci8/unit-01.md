---
subject: Science and Technology
grade: 8
unit: 1
title: Scientific Learning
hours: 0
area: Science and Technology
---

Science begins with careful questions about the natural world. A useful investigation does not try to prove a favourite idea; it gathers observations that other people can check. Learning to plan a fair test, record measurements and explain a conclusion helps us make sound decisions at school, at home and in our community.

::: key Ask a testable question
A testable question names something that can be observed or measured. For example, “Does a longer time in sunlight change how quickly a wet cloth dries?” can be investigated. “Is sunlight good?” is too broad until we decide what “good” means and how to measure it.
:::

## 1.1 Questions, observations and hypotheses

An **observation** is information gathered using our senses or an instrument. We can observe that a shadow is longer in the morning than at noon, or measure its length with a ruler. A **question** identifies what we want to find out. A **hypothesis** is a possible explanation or prediction that can be checked with evidence. It is not a guess that must turn out to be correct.

A useful hypothesis links a change to an outcome: “If the same amount of water is placed in wider dishes, then it will evaporate faster because more water surface is exposed to air.” The prediction can be tested by comparing the time for equal amounts of water to evaporate under similar conditions. Other results are possible, so record what happens even when it does not match the prediction.

```figure caption="A simple investigation moves from a question to evidence and a conclusion; unexpected results can lead to a better question."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8, 2.5))
ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis("off")
labels=[("Question",0.4), ("Hypothesis",2.8), ("Fair test",5.2), ("Evidence",7.6), ("Conclusion",10.0)]
for label,x in labels:
    ax.add_patch(FancyBboxPatch((x,1.9),1.65,0.9,boxstyle="round,pad=0.06",fc="#eef3fb",ec=ACCENT,lw=1.0))
    ax.text(x+0.825,2.35,label,ha="center",va="center",fontsize=7.4,color=INK)
for (_,x1),(_,x2) in zip(labels,labels[1:]):
    ax.annotate("",xy=(x2-0.12,2.35),xytext=(x1+1.72,2.35),arrowprops=dict(arrowstyle="->",color=MUTED,lw=1.0))
ax.annotate("revise the question",xy=(1.2,1.55),xytext=(10.8,1.55),ha="center",fontsize=7,color=MUTED,arrowprops=dict(arrowstyle="->",color=SERIES[2],connectionstyle="arc3,rad=-0.22"))
fig.tight_layout()
```

::: example Turn an idea into a hypothesis
**Problem.** A student thinks that warmer water dissolves sugar faster. Write a testable question and a hypothesis.

**Solution.** Question: “How does water temperature affect the time for 5 g of sugar to dissolve?” Hypothesis: “If the water is warmer, then the sugar will dissolve in less time, provided the water volume, sugar mass and stirring are kept the same.” The investigation must measure the dissolving time rather than decide from appearance alone.
:::

## 1.2 Fair investigations, variables and records

A fair test changes one **independent variable**—the factor deliberately changed—and measures a **dependent variable**, the result. Other important conditions are **controlled variables**: they are kept the same so that the comparison is meaningful. Some questions are better answered by observation or a survey than by an experiment; not every factor can safely or fairly be changed.

Use the right instrument and unit. A ruler measures length in millimetres or centimetres; a balance measures mass in grams or kilograms; a thermometer measures temperature in degrees Celsius. Read a scale at eye level, start from zero where appropriate, and record the unit with every measurement. Repeat measurements when possible and note any unusual result instead of silently deleting it.

Organise results in a table with a clear heading for each quantity and its unit. A line graph is useful when the independent variable changes continuously, such as time; a bar graph is useful for comparing separate categories. Label both axes, choose an even scale, plot points carefully and give the graph a title.

```figure caption="An example data graph: as time in sunlight increases, the measured shadow length in this classroom observation decreases."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 2.8))
time=[8,9,10,11,12]
length=[92,76,61,48,42]
ax.plot(time,length,marker="o",color=ACCENT,lw=2)
ax.set_xlabel("Time of observation (hour)"); ax.set_ylabel("Shadow length (cm)")
ax.set_xticks(time); ax.set_ylim(0,105); ax.grid(axis="y",color=GRID,lw=0.7)
ax.spines[["top","right"]].set_visible(False)
fig.tight_layout()
```

::: example Identify the variables
**Problem.** A class compares how far a toy car rolls on smooth card and rough cloth after it is released from the same ramp. Identify the independent variable, a dependent variable and two controlled conditions.

**Solution.** The **surface type** is the independent variable. The **distance rolled** from the end of the ramp is the dependent variable. Keep the ramp height and release point the same; use the same car and release it without a push. Repeat each surface trial and compare the distances.
:::

::: example Choose a suitable graph
**Problem.** Students measure the temperature of water every two minutes as it cools. Which graph is suitable, and what goes on each axis?

**Solution.** Use a line graph because time changes continuously and the measurements show a trend. Put **time (min)** on the horizontal axis and **temperature (°C)** on the vertical axis. Give the graph a title and use a uniform scale. A falling line shows the observed cooling; it does not by itself prove why the water cooled.
:::

## 1.3 Safety, evidence and project reporting

Before practical work, read the instructions, listen to the teacher and identify hazards. Wear the required protective equipment, tie back long hair, keep bags away from walkways, and never taste or directly smell an unknown substance. Handle glass, heat, electricity, tools, plants and animals only as instructed. Report spills, breakages or injuries immediately. A safe investigation may use a model or teacher demonstration instead of a risky activity.

**Evidence** is a measurement or observation relevant to a question. A **conclusion** states what the results suggest and cites that evidence. An **inference** is an explanation of what may have caused an observation; it should be distinguished from what was directly seen. For example, “the liquid became cloudy” is an observation, while “a new substance formed” is an inference that needs more evidence.

A short project report can include the question, hypothesis, materials, method, safety steps, results table or graph, conclusion, limitations and references. Another student should be able to understand the method and repeat it. Be honest about mistakes and uncertainty. Credit a book, website or person when their information is used; do not copy text or present another person's work as your own.

::: example Write a conclusion from data
**Problem.** Three equal wet cloth pieces were dried in the same place. Their masses fell from 40 g to 28 g, 29 g and 27 g after one hour. What can the student conclude?

**Solution.** The three pieces lost 12 g, 11 g and 13 g. The results suggest that water left the cloth during the hour, with an average mass loss of 12 g. The student should not claim that the cloth became completely dry or that one condition caused the loss unless dryness and the relevant conditions were measured. Repeating the test can show how consistent the result is.
:::

::: caution A result is not a failure
If the result does not support the hypothesis, report it accurately. Check whether the method was fair, the instrument was read correctly and enough trials were done. Changing the data to match an expected answer destroys the value of the investigation.
:::

## Chapter summary

- A testable question can be answered with observations or measurements; a hypothesis is a checkable explanation or prediction.
- A fair test changes an independent variable, measures a dependent variable and controls relevant conditions.
- Choose suitable instruments and units; organise results in labelled tables and graphs.
- Follow safety instructions and report hazards, spills and injuries promptly.
- A conclusion uses evidence, names limitations and distinguishes observation from inference.
- A clear project report lets others understand and repeat the method; acknowledge sources honestly.

## Practice questions

1. Which is the most testable question? (a) Is rain beautiful? (b) Do bean seeds sprout faster in warm or cool conditions? (c) Is a garden nice? (d) Are plants important?
2. What is the factor deliberately changed in a fair test called?
3. Name one instrument for measuring temperature and give a suitable unit.
4. Why should a graph have labelled axes?

::: note Answers to questions 1–4
**1.** (b) — sprouting time can be measured under stated conditions.
**2.** The independent variable.
**3.** A thermometer; degrees Celsius (°C) is suitable for ordinary classroom measurements.
**4.** Labels tell the reader which quantities and units the axes represent.
:::

5. A student tests whether a paper towel brand changes how much water it absorbs. Name one independent variable, one dependent variable and two conditions to keep the same.
6. Explain the difference between an observation and an inference, using one example.
7. A class records a surprising measurement once. What should it do before deciding that the value is wrong?
8. List four items that belong in a short investigation report.

::: note Answers to questions 5–8
**5.** Independent variable: towel brand. Dependent variable: volume or mass of water absorbed. Keep towel size and starting water amount the same; use the same soaking and draining time.
**6.** “The leaf has brown spots” is an observation. “A disease caused the spots” is an inference that needs supporting evidence.
**7.** Check the instrument and method, record the result honestly, repeat the measurement if safe, and compare it with other trials. Do not erase it without a reason.
**8.** Any four: question, hypothesis, materials, method, safety, results, graph, conclusion, limitations or references.
:::
