---
subject: Social Studies
grade: 8
unit: 1
title: 'Unit 1: We and Our Society'
hours: 10
area: Units
---

Development is not only a new road or large building. It is the sustained improvement of people’s opportunities, safety, services and participation. This unit connects infrastructure, skilled people and federal government to the development that learners can observe in their own province.

::: key What success looks like
You can distinguish physical infrastructure from human resources, explain why both are needed for development, and investigate one development project in your province using reliable local evidence.
:::

## 1.1 Development is connected work

An irrigation canal without trained users may not help farms. A trained nurse without a health post lacks a place to serve. Development works when services, resources and people support one another.

```figure caption="Development grows through connected inputs, not a single construction project."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 2.5))
items = [('Infrastructure', 'roads, water, schools'), ('People', 'skills, care, leadership'), ('Participation', 'planning, oversight'), ('Wellbeing', 'fairer opportunities')]
for index, (title, detail) in enumerate(items):
    x = index * 1.62
    ax.add_patch(FancyBboxPatch((x, 0.55), 1.28, 0.72, boxstyle='round,pad=0.05', fc='#e9f3fb', ec=ACCENT, lw=1.0))
    ax.text(x + 0.64, 1.0, title, ha='center', va='center', weight='bold', fontsize=8.8)
    ax.text(x + 0.64, 0.22, detail, ha='center', va='center', fontsize=7.7, color=MUTED)
    if index < len(items)-1:
        ax.annotate('', xy=(x + 1.57, 0.91), xytext=(x + 1.3, 0.91), arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.1))
ax.set_xlim(-0.15, 6.1); ax.set_ylim(0, 1.6); ax.axis('off')
```

| Development input | Local example | Question to ask |
|---|---|---|
| Physical infrastructure | road, bridge, school, water supply, internet | Does it work safely for everyone? |
| Human resources | teachers, farmers, health workers, technicians | Do people have the skills and support to serve? |
| Natural resources | water, forests, soil, tourism landscape | Is it being used without damaging future needs? |
| Good governance | transparent plan, public meeting, fair budget | Can citizens ask questions and monitor work? |

## 1.2 Federalism and local responsibility

Nepal’s federal system shares responsibilities among federal, provincial and local governments. A learner need not memorise a long list first; begin by asking which level is closest to a daily issue. For example, a local path or waste collection may involve the municipality or rural municipality, while a national highway needs wider coordination.

::: example Investigate, do not guess
Choose one visible project: a drinking-water tap, school building, road, health post or park. Record its name, purpose, users, benefit, problem and source of information. Speak respectfully to a responsible adult or use an official noticeboard. Separate a verified fact from your own suggestion.
:::

::: tip A good development question
Instead of asking only “Was the project built?”, ask “Who can use it safely, who is left out, and how will it be maintained?” These questions make your social-study answer analytical.
:::

## Chapter summary

- Development improves people’s lives through connected services, skills, resources and participation.
- Infrastructure alone is not enough; trained people and fair management are essential.
- Federalism shares public responsibilities across levels of government.
- Local evidence and respectful interviews make a project report reliable.

## Practice questions

1. Define development in one or two sentences. <span class="marks">[2]</span>
2. Give one example each of physical infrastructure and human resource. <span class="marks">[2]</span>
3. Explain why a new health post also needs trained health workers. <span class="marks">[2]</span>
4. Prepare a six-point observation sheet for a development project near your home or school. <span class="marks">[4]</span>

::: note Answers
**1.** Development is planned improvement in people’s wellbeing, opportunities and services, not only construction.  
**2.** Examples: bridge or water supply; nurse or engineer.  
**3.** A building cannot diagnose, treat or guide people by itself; trained workers make the service useful and safe.  
**4.** Include name, place, purpose, users, benefit, problem and information source; any six relevant points earn credit.
:::
