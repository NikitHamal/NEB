---
subject: Science and Technology
grade: 8
unit: 1
title: 'Unit 1: Scientific Learning'
hours: 8
area: Units
---

Science is a disciplined way of asking questions about the world. A scientific conclusion is stronger than a guess because it is based on a fair method, recorded evidence and a reasoned explanation. This unit introduces the inquiry cycle, variables, surveys and honest reporting.

::: key What success looks like
You can turn a broad curiosity into a testable question, plan a fair comparison, record observations in a table and write a conclusion that matches the evidence.
:::

## 1.1 The inquiry cycle

Scientific learning moves forward in connected steps. You may return to an earlier step when evidence shows that the method needs improvement.

```figure caption="Scientific inquiry is a cycle: evidence can lead to a better question or method."
import math
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.4, 2.7))
steps = ['Question', 'Prediction', 'Fair method', 'Observe', 'Explain', 'Share']
for index, step in enumerate(steps):
    angle = 2 * 3.14159 * index / len(steps)
    x, y = 2.55 + 1.75 * math.cos(angle), 1.35 + 0.85 * math.sin(angle)
    ax.add_patch(FancyBboxPatch((x - 0.48, y - 0.2), 0.96, 0.4, boxstyle='round,pad=0.03', fc='#e9f3fb', ec=ACCENT, lw=1.0))
    ax.text(x, y, step, ha='center', va='center', fontsize=8.3, weight='bold')
    next_angle = 2 * 3.14159 * ((index + 1) % len(steps)) / len(steps)
    nx, ny = 2.55 + 1.75 * math.cos(next_angle), 1.35 + 0.85 * math.sin(next_angle)
    ax.annotate('', xy=(nx, ny), xytext=(x, y), arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.0))
ax.set_xlim(0, 5.1); ax.set_ylim(0.1, 2.6); ax.axis('off')
```

| Step | Useful question | Example |
|---|---|---|
| Question | What exactly do I want to find out? | Does light affect bean-seedling growth? |
| Prediction | What do I think may happen? | Seedlings in light may grow greener. |
| Method | What will I change, measure and keep the same? | Change light; measure height; keep seed, soil and water alike. |
| Observation | What did I actually see or measure? | Height and leaf colour each day. |
| Conclusion | Does the evidence support the prediction? | State only what the records show. |

## 1.2 A fair test and variables

A fair test changes one factor at a time. The factor deliberately changed is the **independent variable**. The result measured is the **dependent variable**. The conditions kept alike are **controlled variables**.

::: example Bean-seedling investigation
**Question.** Does amount of light affect seedling growth?

**Independent variable:** amount of light.  
**Dependent variable:** height in centimetres after seven days.  
**Controls:** same seed type, number of seeds, container, soil, water and observation time.

Use at least two similar groups and label them clearly. Never claim that light alone caused a difference if water, soil and seed type also changed.
:::

### Observation table

| Group | Light condition | Height on day 1 | Height on day 7 | Leaf colour | Notes |
|---|---|---:|---:|---|---|
| A | near window | 2.0 cm | 8.1 cm | green | upright |
| B | covered box | 2.0 cm | 4.3 cm | pale | thin stem |

The table is an example of how to record evidence; a real conclusion needs your own repeated observations.

## 1.3 Surveys and research ethics

A survey gathers people’s responses. Ask neutral questions, protect personal information and report answers honestly. For a class survey on water use, do not write someone’s full name next to a sensitive answer. Count responses accurately and state the sample size.

::: caution Correlation is not proof
If two things happen together, one may not cause the other. A survey can show a pattern, but a fair experiment or more evidence is needed before claiming cause and effect.
:::

## Chapter summary

- Scientific learning uses a question, prediction, fair method, observation and evidence-based conclusion.
- A fair test changes one independent variable and controls other important conditions.
- Tables make observations checkable.
- Surveys need neutral questions, privacy and honest reporting.

## Practice questions

1. Put these in a logical inquiry order: observe, conclude, ask a question, plan a method, record data. <span class="marks">[2]</span>
2. In a test of fertiliser amount on plant height, identify the independent and dependent variables. <span class="marks">[2]</span>
3. Name two controls for a test comparing how quickly sugar dissolves in warm and cold water. <span class="marks">[2]</span>
4. Design a three-question anonymous survey about safe internet habits in your class. <span class="marks">[3]</span>

::: note Answers
**1.** Ask a question, plan a method, observe/record data, conclude.  
**2.** Independent: fertiliser amount. Dependent: plant height.  
**3.** Same amount of sugar and same volume of water, for example.  
**4.** Questions should be neutral, relevant and avoid collecting unnecessary personal details.
:::
