---
subject: Health, Physical and Creative Arts
grade: 8
unit: 2
title: Community Health and Mental Health
hours: 7
area: Health Education
---

Health is shaped not only by personal habits but also by water, toilets, waste management, housing, relationships and access to care. A community becomes healthier when people identify shared problems and act together. Mental health is part of the same picture: a safe, supportive community helps people think, feel and cope well.

::: key High-value examination idea
A strong answer links a health problem to its cause, effect and practical community-level solution. For mental health questions, use respectful language, identify warning signs and recommend support rather than blame.
:::

## 2.1 Community health

**Community health** is the organised effort of people and services to protect and improve the health of everyone living in a particular area. It includes prevention, health education, treatment, rehabilitation and a healthy environment.

Important community health services in Nepal include immunisation, antenatal and postnatal care, growth monitoring, nutrition counselling, family-planning information, treatment of common illnesses, disease surveillance, school health programmes and referral. Health posts, basic hospitals, female community health volunteers, schools, municipalities, water-user groups and families all have roles.

| Community health problem | Possible causes | Community response |
|---|---|---|
| diarrhoeal disease | unsafe water, open defecation, unwashed hands | protect the source, treat water, use toilets, wash hands |
| mosquito-borne disease | stagnant water and unmanaged containers | remove breeding sites, use nets, seek timely care |
| respiratory illness | smoke, dust, poor ventilation | cleaner stoves, ventilation, smoke-free homes |
| malnutrition | poor diet, illness, food insecurity | growth monitoring, diverse local foods, treatment and support |
| injury | unsafe roads, buildings or work | hazard mapping, safety rules, first-aid readiness |

### Community diagnosis and participation

A **community diagnosis** is a systematic study of a community’s health problems, resources and priorities. Students can contribute safely through observation, interviews supervised by a teacher and review of public records.

1. Define the area and population.
2. Collect information about health problems and available services.
3. Identify causes and groups most affected.
4. Rank problems by seriousness, number affected and possibility of action.
5. Plan a realistic response with responsible people and a time frame.
6. Carry out the plan and evaluate whether conditions improved.

```figure caption="A community-health action cycle: evidence leads to action and review."
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots(figsize=(4.8, 3.1))
labels = ["Observe", "Identify\nproblem", "Plan", "Act", "Review"]
angles = np.linspace(np.pi/2, np.pi/2 - 2*np.pi, len(labels), endpoint=False)
for i, (label, angle) in enumerate(zip(labels, angles)):
    x, y = 2.5 + 1.55*np.cos(angle), 1.7 + 1.15*np.sin(angle)
    ax.text(x, y, label, ha="center", va="center", fontsize=7.2, color=INK,
            bbox=dict(boxstyle="round,pad=0.35", fc="#ecfeff", ec=SERIES[i % len(SERIES)], lw=1.2))
    angle2 = angles[(i+1) % len(labels)]
    x2, y2 = 2.5 + 1.55*np.cos(angle2), 1.7 + 1.15*np.sin(angle2)
    ax.annotate("", xy=(x2, y2), xytext=(x, y), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.15, shrinkA=22, shrinkB=22, connectionstyle="arc3,rad=-0.12"))
ax.text(2.5, 1.7, "Participation", ha="center", va="center", fontsize=8, color=ACCENT, weight="bold")
ax.set_xlim(0.2, 4.8); ax.set_ylim(0.15, 3.35); ax.axis("off"); fig.tight_layout()
```

::: example Prioritising a local problem
**Situation.** A survey finds scattered plastic waste, two uncovered water tanks and frequent diarrhoea in one neighbourhood.

**Response.** Students should not claim that plastic alone caused the illness. They can report the evidence, help adults cover and clean tanks, promote handwashing and safe water, arrange waste separation with the municipality, and compare diarrhoea reports before and after action. This connects evidence, prevention and evaluation.
:::

## 2.2 Total sanitation and safe toilet use

**Sanitation** means safe management of human excreta, wastewater and solid waste together with hygienic behaviour. **Total sanitation** goes beyond constructing toilets. It aims for sustained hygienic behaviour in every household, school and public place.

Key elements include:

- regular use of an improved toilet by every person;
- handwashing with soap at critical times;
- safe drinking-water collection, treatment, transport and storage;
- hygienic preparation and storage of food;
- safe management of solid and liquid waste;
- clean homes, schools, animal sheds and surroundings;
- menstrual hygiene and accessible facilities for all users.

Critical times for handwashing with soap are after defecation, after cleaning a child, before preparing food, before eating or feeding someone, and after contact with waste or animals.

### Safe toilet use

A toilet separates faeces from people, flies, soil and water. Use it every time, put cleansing material in the correct place, flush or pour water as designed, close the lid where present, wash hands with soap and report damage. Keep the floor dry and clean. Do not put plastic, cloth, sanitary pads or other items into a pit or pipe unless the system is designed for them.

Children, older people and persons with disabilities need privacy, a reachable latch, adequate space, safe paths, handrails where needed and nearby handwashing facilities. A toilet is not truly safe if some community members cannot use it.

```figure caption="The faecal–oral transmission routes and barriers that break them."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 3.0))
left = (0.25, 1.25); right = (4.35, 1.25)
ax.text(*left, "Faeces", ha="center", va="center", fontsize=8, weight="bold", color="#991b1b",
        bbox=dict(boxstyle="round,pad=0.35", fc="#fee2e2", ec="#ef4444"))
ax.text(*right, "Mouth", ha="center", va="center", fontsize=8, weight="bold", color="#166534",
        bbox=dict(boxstyle="round,pad=0.35", fc="#dcfce7", ec="#22c55e"))
routes = [("Fluids", 2.45), ("Fingers", 1.85), ("Flies", 1.25), ("Fields", 0.65)]
for label, y in routes:
    ax.annotate("", xy=(4.0, y), xytext=(0.65, y), arrowprops=dict(arrowstyle="->", color=GRID, lw=1.2))
    ax.text(1.45, y+0.1, label, fontsize=6.8, color=MUTED)
barriers = [("Safe toilet", 0.95), ("Soap", 1.75), ("Cover food", 2.55), ("Safe water", 3.35)]
for label, x in barriers:
    ax.plot([x, x], [0.4, 2.7], color=ACCENT, lw=3, alpha=0.7)
    ax.text(x, 2.82, label, ha="center", fontsize=6.3, color=ACCENT)
ax.set_xlim(-0.2, 4.8); ax.set_ylim(0.2, 3.2); ax.axis("off"); fig.tight_layout()
```

::: example Making stored water safer
**Problem.** A family boils drinking water but repeatedly dips an unwashed cup into the storage vessel.

**Solution.** Boiling can kill many disease-causing organisms, but unsafe handling can contaminate water again. Let treated water cool in a covered vessel, use a clean narrow-necked container or tap, avoid hand contact, and clean the vessel regularly.
:::

::: caution Never mix cleaning chemicals
Bleach or toilet cleaner must never be mixed with acid, ammonia or another cleaner. Dangerous gas can form. Read the label, use ventilation, keep chemicals away from children and ask an adult to handle concentrated products.
:::

## 2.3 Mental health

**Mental health** is a state of emotional, psychological and social well-being that helps a person learn, build relationships, cope with ordinary stress and contribute to the community. It does not mean feeling happy all the time. Sadness, worry and anger can be normal responses; the concern grows when symptoms are intense, continue for a long time or disrupt daily life.

### Factors that influence mental health

Protective factors include caring relationships, safety, sleep, exercise, meaningful activity, problem-solving skills, inclusion and access to support. Risk factors include violence, bullying, discrimination, isolation, harmful substance use, severe academic pressure, family conflict, disaster, chronic illness and poverty. A risk factor does not guarantee illness, and a mental-health problem is never proof of weak character.

| Possible warning sign | Helpful first response |
|---|---|
| lasting sadness, fear or irritability | listen privately and without judgement |
| withdrawal from friends or usual activities | check in and involve a trusted adult |
| major changes in sleep, appetite or school work | encourage professional assessment |
| repeated unexplained physical complaints | take the concern seriously; seek health advice |
| talk of self-harm, death or hopelessness | stay with the person and get urgent adult/professional help |

### Healthy coping and support

Useful coping strategies include a regular sleep schedule, physical activity, slow breathing, breaking a large task into small steps, talking to a trusted person, limiting distressing media and avoiding alcohol, tobacco and drugs. Coping does not replace treatment when a problem is severe or persistent.

To support a friend: choose a private safe place; listen more than you speak; say what you noticed; do not promise secrecy if safety is at risk; involve a trusted adult, counsellor or health worker; and continue ordinary friendship. Do not diagnose, shame, threaten or circulate their story.

::: example Responding to exam stress
**Situation.** Arun has slept poorly for two weeks, cannot concentrate and says he feels useless before examinations.

**Support plan.** A friend can listen, encourage Arun to tell a parent or teacher, help divide revision into small sessions, include breaks and sleep, and seek a counsellor or health worker if symptoms continue. If Arun mentions self-harm, the friend must stay with him and obtain urgent adult help rather than keeping it secret.
:::

::: key Psychological first aid after a distressing event
**Look** for safety and urgent needs. **Listen** calmly without forcing the person to retell the event. **Link** the person with family, practical help and qualified services. Do not make promises you cannot keep.
:::

## Chapter summary

- Community health combines organised prevention, care, education and environmental action.
- Community diagnosis follows observation, problem identification, priority setting, action and evaluation.
- Total sanitation includes toilet use, handwashing, safe water and food, waste management and inclusive clean surroundings.
- A toilet prevents disease only when it is consistently used, maintained and linked with handwashing.
- Treated water can be contaminated again during unsafe storage or handling.
- Mental health includes the ability to learn, relate, cope and participate; it is not constant happiness.
- Warning signs that persist or disrupt life deserve support from a trusted adult or qualified professional.
- Talk of self-harm requires immediate safety, supervision and urgent help.

## Practice questions

**Group A — Very short answer (1 mark each)**

1. What is community health? <span class="marks">[1]</span>
2. State one critical time for washing hands with soap. <span class="marks">[1]</span>
3. What is total sanitation? <span class="marks">[1]</span>
4. Write one protective factor for mental health. <span class="marks">[1]</span>

::: note Answers to Group A
**1.** Organised efforts to protect and improve the health of people in a defined community.  
**2.** Any valid time, such as after defecation or before preparing food.  
**3.** Sustained safe sanitation and hygiene behaviour covering toilets, hands, water, food, waste and surroundings.  
**4.** Any valid factor, such as supportive relationships, adequate sleep or safety.
:::

**Group B — Short answer (2 marks each)**

1. Give two reasons why merely constructing a toilet does not achieve total sanitation. <span class="marks">[2]</span>
2. Write two ways to prevent recontamination of treated drinking water. <span class="marks">[2]</span>
3. Mention two differences between ordinary short-term sadness and a possible mental-health problem. <span class="marks">[2]</span>
4. How should a student support a distressed friend? Write two actions. <span class="marks">[2]</span>

::: note Answer outlines to Group B
**1.** The toilet must be used and maintained, and hygiene also requires handwashing, safe water, food and waste management.  
**2.** Store covered; use a tap or clean pouring method; avoid dipping hands or dirty utensils; clean the vessel.  
**3.** A concerning problem may be intense, persistent and disruptive to sleep, learning, relationships or daily activities.  
**4.** Listen without judgement and connect the friend with a trusted adult or professional; never promise secrecy when safety is at risk.
:::

**Group C — Long answer (4 marks each)**

1. Your community reports repeated diarrhoea after monsoon flooding. Describe four coordinated actions that address the transmission route. <span class="marks">[4]</span>
2. Explain four steps a school should take when a learner shows persistent distress and mentions self-harm. <span class="marks">[4]</span>

::: note Answer outlines to Group C
**1.** Protect and treat drinking water, ensure toilet use and safe excreta disposal, provide handwashing with soap, protect food, clean flood contamination and connect ill people with care. Award any four explained actions.  
**2.** Take the statement seriously, keep the learner with a safe adult, reduce immediate danger, inform the designated guardian or safeguarding lead, obtain urgent professional help and follow up. Award four safe, relevant steps.
:::
