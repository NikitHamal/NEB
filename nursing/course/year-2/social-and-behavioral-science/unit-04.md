---
subject: Social and Behavioral Science
grade: BSc Nursing Year 2
unit: 4
title: Social Psychology: Attitudes, Social Influence, Groups and Health Behaviour Change
hours: 14
area: BSN 16 · Social and Behavioral Science · Unit 4
---

A junior nurse sees a senior prepare a drug dose that looks ten times too large. She says nothing: "The senior must know." In an Asch room, three out of four people give an answer they know is wrong to match a group. Elsewhere, a man in Kathmandu smokes 20 cigarettes a day although he has read every warning. **Social psychology** is the scientific study of how people **think about, influence and relate to one another**. This unit covers social perception, **attitudes**, **conformity, compliance and obedience**, prosocial behaviour, aggression, groups, and the models that change **health behaviour**.

::: key What this unit gives you
- Real images: **Albert Bandura**, the **Asch line cards** and the **original 1962 Milgram recruitment notice**; SVG figures on the ABC model and cognitive dissonance, a bar chart of the classic experiments, and the stages-of-change model.
- **Social cognition**: schema, attribution, stereotype, prejudice, discrimination; self, identity and **gender**.
- **Attitudes**: components, formation, change, Festinger's dissonance, **Likert scale scoring** and KAP categories computed in Python.
- **Social influence**: Asch, Sherif, Milgram, Zimbardo and what they teach about **speaking up** in a ward; **bystander effect**, **aggression** and groups.
- **Health behaviour**: Health Belief Model, **Transtheoretical Model**, the 5 A's; eight nursing lessons; a long tobacco-cessation case with pack-year and cost maths.
:::

## 4.1 Social cognition, perception and the self

**Social cognition** is how we notice, interpret and remember information about people. A **schema** is a mental frame built from past experience (the "nurse schema" makes us expect a white uniform). Schemas speed thinking but cause errors: **stereotypes** (fixed beliefs about a group), **prejudice** (a negative attitude), **discrimination** (unfair action) and **halo effect** (one good trait colours all). **Attribution** (Heider) explains behaviour by **dispositional** causes (character) or **situational** causes (circumstances); the **fundamental attribution error** blames character too often ("the patient is lazy" when he has no money for transport), and the **self-serving bias** takes credit for success and blames others for failure. **First impressions** and **non-verbal cues** (gaze, posture, touch) form social perception within seconds.

**The self.** **Self-concept** (what I think I am), **self-esteem** (how I value myself), **self-efficacy** (Bandura: belief that I can do a task) and **social identity** (the groups I belong to: nurse, Tamang, woman) are built through **introspection**, feedback from others and **social comparison** (Festinger). **Sex** is biological; **gender** is the social meaning given to being male or female; **gender stereotypes** (men decide, women care) and **gender roles** affect health: women eat last and delay care; men avoid help-seeking and drink more.

## 4.2 Attitudes

An **attitude** is a learned, lasting tendency to evaluate a person, object or idea favourably or unfavourably. It has three parts (the **ABC model**, Figure 4.2): **Affective** (feeling: "I fear injections"), **Behavioural** (action tendency: "I avoid the clinic") and **Cognitive** (belief: "vaccines cause illness"). **Formation:** direct experience, family and culture, peers, media, and classical and operant learning. **Change:** by **persuasion** (source: expert, trusted and likeable; message: clear, two-sided, with emotion plus facts; audience: age, education), by **contact** (the contact hypothesis reduces prejudice) and by **dissonance** (Festinger): when behaviour and belief clash, the tension is reduced by changing one of them.

```svgfig label="4.2" caption="Left: the ABC model of attitude (Affective, Behavioural, Cognitive), with a smoker's example. Right: cognitive dissonance. 'I smoke' and 'smoking kills' clash and create tension. The tension is reduced in three ways: change behaviour (quit), change belief (deny the harm), or add a justification (it calms me). The nurse's job is to make the first route easier."
f = Fig(760, 290)
f.box(100, 10, 170, 44, "ATTITUDE\n(toward tobacco)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(10, 100, 150, 70, "A: AFFECT\n\"Cigarettes relax\nme\"", fill=ROSE, stroke=RED, size=10.5)
f.box(210, 100, 150, 70, "C: COGNITION\n\"It is only a\nproblem for old men\"", fill=SAND, stroke=AMBER, size=10.5)
f.box(110, 200, 150, 70, "B: BEHAVIOUR\nBuys a pack each\nmorning", fill=MINT, stroke=TEAL, size=10.5)
f.arrow([(150, 54), (90, 100)], color=SLATE, sw=1.6); f.arrow([(220, 54), (270, 100)], color=SLATE, sw=1.6); f.arrow([(110, 170), (160, 200)], color=SLATE, sw=1.6); f.arrow([(270, 170), (220, 200)], color=SLATE, sw=1.6)
f.box(420, 10, 160, 50, "\"I smoke\"", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(600, 10, 150, 50, "\"Smoking kills\"", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(500, 60), (560, 100)], color=RED, sw=2.2, both=True); f.arrow([(670, 60), (620, 100)], color=RED, sw=2.2)
f.box(470, 100, 220, 40, "DISSONANCE (tension)", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(410, 175, 105, 90, "Change\nbehaviour:\nQUIT", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(527, 175, 105, 90, "Change belief:\n\"It is not\nthat bad\"", fill=ROSE, stroke=RED, size=10.5)
f.box(644, 175, 105, 90, "Add excuse:\n\"It calms my\nnerves\"", fill=ROSE, stroke=RED, size=10.5)
f.arrow([(520, 140), (462, 175)], color=TEAL, sw=1.8); f.arrow([(580, 140), (580, 175)], color=RED, sw=1.8); f.arrow([(640, 140), (696, 175)], color=RED, sw=1.8)
```

**Measuring attitude: the Likert scale.** Respondents rate items from 1 (strongly disagree) to 5 (strongly agree). **Negatively worded items are reverse-scored (6 minus the rating)** before adding. Many Nepali KAP studies convert the total to a percentage and use **Bloom's cut-offs**: 80% or more = **good/positive**, 60-79% = **moderate**, below 60% = **poor/negative**.

```python
raw = [4, 5, 2, 4, 5, 1, 4, 2, 5, 4]                  # one respondent's ratings (1-5) on 10 items
negative_items = [2, 5, 7]                            # positions of negatively worded items (0-based)
scored = [6 - x if i in negative_items else x for i, x in enumerate(raw)]
total, maximum = sum(scored), 5 * len(raw)
pct = total / maximum * 100
band = "good" if pct >= 80 else ("moderate" if pct >= 60 else "poor")
print(f"Scored items = {scored}")
print(f"Total = {total}/{maximum} = {pct:.0f}% -> {band} attitude")
```

```text
Scored items = [4, 5, 4, 4, 5, 5, 4, 4, 5, 4]
Total = 44/50 = 88% -> good attitude
```

After reversing items 3, 6 and 8, the respondent scores **44 of 50 = 88%**, a **good** attitude on Bloom's scale. Without the reversal she would have scored 36, wrongly lower.

## 4.3 Social influence: conformity, compliance and obedience

**Conformity** is changing behaviour or belief to match a group. **Sherif** (1935, autokinetic effect): in an ambiguous task, people's estimates converge on a group norm (**informational influence**). **Asch** (1951): a person judges which of three lines matches a standard line; confederates give the wrong answer, and about **75% of subjects conformed at least once** and about **37% of critical trials** were wrong in the group condition, against under 1% alone (**normative influence**). Conformity falls when **one ally** breaks the majority, and rises with group size up to about 3-5, unanimity, difficulty and low self-confidence. **Compliance** is yielding to a request; **Cialdini's principles**: reciprocity, commitment/consistency, social proof, liking, authority and scarcity (with **foot-in-the-door** and **door-in-the-face** techniques). **Obedience** is following a direct order from an authority. **Milgram** (1961-63, Yale): ordinary adults were told to give increasing electric shocks to a learner; in the baseline study **26 of 40 (65%)** went to the maximum 450 volts. Obedience fell when the authority was absent, when the victim was close or when other "teachers" refused. **Zimbardo** (Stanford prison, 1971) showed how assigned roles and a setting can lead to cruelty (the experiment is much criticised for its method).

```photogrid label="4.1" cols="3" ratio="1.0" caption="Pioneers and apparatus of social psychology. (a) Albert Bandura (1925-2021), social learning theory and self-efficacy. (b) The Asch cards: the standard line on the left and comparison lines A, B and C on the right; subjects had to name the matching line. (c) The original 1962 'Public Announcement' recruiting New Haven men for 'a study of memory and learning' for 4 dollars an hour at Yale, which hid the true purpose of the study. Wikimedia Commons (public domain and CC BY)."
@ photo id="nur10/bandura" cap="Albert Bandura"
fit 1.0
focus 0.5 0.7
mark 0.50 0.62 "1"
key 1 (a) Bandura: observational learning, self-efficacy
@ photo id="nur10/asch" cap="The Asch cards"
fit 1.0
focus 0.5 0.5
mark 0.24 0.50 "2"
mark 0.84 0.62 "3"
key 2 (b) Standard line on the first card
key 3 (b) Comparison lines A, B, C on the second card: only one matches
@ photo id="nur10/milgram" cap="Milgram recruitment notice (1962)"
fit 1.0
focus 0.5 0.9
mark 0.10 0.80 "4"
key 4 (c) Headline offering 4 dollars for one hour for a 'study of memory'
```

```svgfig label="4.3" caption="What the classic experiments found. Asch: 75% conformed at least once. Milgram: 65% obeyed to the end in the baseline. Darley and Latane (bystander): the more people present, the fewer helped (85% with one other person, 62% with two, 31% with five). The lesson: the presence of others and of authority can silence conscience, so teams need rules that allow anyone to speak up."
f = Fig(760, 260)
data = [("Asch: conformed\nat least once", 75, AMBER), ("Milgram: obeyed\nto 450 V", 65, RED), ("Bystander: help,\n2 people", 85, TEAL), ("Bystander: help,\n3 people", 62, TEAL), ("Bystander: help,\n6 people", 31, TEAL)]
for i, (lab, v, col) in enumerate(data):
    x = 25 + i * 145
    h = v * 1.7
    f.box(x, 200 - h, 105, h, f"{v}%", fill=SOFT, stroke=col, size=13, color=col, bold=True)
    f.text(x + 52, 228, lab, size=10, color=SLATE)
f.line(15, 200, 745, 200, color=SLATE, sw=1.4)
f.text(380, 15, "Percent of subjects showing the effect", size=11, color=NAVY, bold=True)
```

**Eight nursing lessons from social influence.**

1. **Speak up when something is wrong.** Asch showed that one dissenter frees others to speak. If a dose, a site or a patient identity looks wrong, say so, using SBAR. Patient safety comes before hierarchy.
2. **Question orders respectfully.** Milgram's subjects obeyed a calm authority even against their conscience. A nurse is not a robot: check the order, ask "Please confirm", and use the chain of command. The NNC Code of Ethics holds the nurse responsible for her own acts.
3. **Beware groupthink in teams.** A united, confident team can overlook risk. Invite a "devil's advocate" at handover and ask, "What could go wrong?". Diversity of views is protective.
4. **Be a good role model.** Students copy seniors (Bandura). Correct hand hygiene by a senior teaches more than any lecture. Poor habits spread in the same way.
5. **Use social proof in health education.** People follow what peers do. "Eight of ten mothers in this ward breastfed within an hour" persuades more than a rule. Female Community Health Volunteers (FCHVs) work because they are peers.
6. **Use commitment and reciprocity ethically.** A patient who signs a written goal is more likely to keep it. Small, free help creates goodwill. Never use these methods to mislead or pressure patients.
7. **Prevent bystander inaction.** In an emergency, give a person a direct task ("You, call the doctor"). Responsibility is diffused in crowds, so name the person. Practise this in BLS drills.
8. **Respect informed consent.** Milgram's study led to modern research ethics: consent, no deception that causes harm, debriefing and the right to withdraw. Nepal's health research council (NHRC) applies these rules to every study.

## 4.4 Prosocial behaviour, aggression and groups

**Prosocial behaviour** is action meant to help others (donating blood, nursing, giving first aid). Motives: **empathy-altruism** (Batson), **social exchange** (costs and rewards), **social norms** (reciprocity, responsibility) and kin selection. **Steps (Latane and Darley):** notice the event, interpret it as an emergency, take responsibility, know how to help, and act. The **bystander effect** arises from **diffusion of responsibility** and **pluralistic ignorance** (everyone looks calm, so I assume it is fine); helping is more likely if the victim is known, the bystander is trained and in a good mood, and the setting is not hurried.

**Aggression** is behaviour meant to harm another person. **Theories:** **instinct** (Freud, Lorenz), **frustration-aggression** (Dollard), **social learning** (Bandura's Bobo doll: children copy violent models) and the **general aggression model**. **Causes:** biological (testosterone, low serotonin, brain injury, alcohol), social (poverty, crowding, domestic violence), cultural (norms of honour) and situational (heat, provocation, weapons). **Prevention:** early parenting and school programmes, controlling alcohol, laws and enforcement, anger-management and conflict training, non-violent role models and media guidance. In Nepal NDHS 2022 found physical violence since age 15 in **23%** of women, and in the Criminal Code and the Domestic Violence Act 2066 offences carry penalties; OCMC and the helpline (1145) give support.

**Groups.** A **social group** has interaction, shared goals, norms and roles. **Social facilitation** (Zajonc): an audience improves simple or well-learned tasks and worsens difficult ones; **social loafing**: individuals work less in a group when effort is not identifiable (so give each nurse a named task); **groupthink** (Janis): the wish for harmony suppresses doubt (cohesive group, strong leader, isolation); **group polarisation**: discussion pushes views to the extreme; **leadership styles**: autocratic, democratic (best for complex care) and laissez-faire. Good teams use clear roles, open communication, shared goals and structured handover (SBAR).

## 4.5 Health behaviour and how to change it

**Health behaviour** is any action that protects or harms health (handwashing, smoking, helmet use, adherence). The **Health Belief Model** (Rosenstock) predicts action from: **perceived susceptibility** ("I could get it"), **severity**, **benefits**, **barriers**, **cues to action** (a reminder, a symptom, a radio message) and **self-efficacy**. The **Theory of Planned Behaviour** (Ajzen) adds **attitude, subjective norm and perceived control** leading to **intention**. The **Transtheoretical Model** (Prochaska and DiClemente) describes six **stages of change** (Figure 4.4); matching the intervention to the stage works better than giving the same advice to everyone.

```svgfig label="4.4" caption="The stages of change (Transtheoretical Model) with the matching nursing action at each stage, shown with a tobacco user. Relapse is common and is a return to an earlier stage, not failure: most people need several attempts."
f = Fig(760, 300)
st = [("PRE-CONTEMPLATION", "No plan to quit\n(next 6 months)", "Raise awareness:\nask, advise, personalise risk", ROSE, RED),
      ("CONTEMPLATION", "Thinking of quitting\n(within 6 months)", "Weigh pros and cons;\nbuild confidence", SAND, AMBER),
      ("PREPARATION", "Plans to quit\n(within 30 days)", "Set a quit date;\nagree a written plan", BLUE, NAVY),
      ("ACTION", "Quit, under\n6 months", "Support, nicotine\nreplacement, coping skills", MINT, TEAL),
      ("MAINTENANCE", "Quit 6 months\nor more", "Prevent relapse;\nreward; avoid triggers", MINT, TEAL)]
for i, (a, b, c, fl, sk) in enumerate(st):
    x = 8 + i * 149
    f.box(x, 10, 140, 40, a, fill=fl, stroke=sk, size=9.5, bold=True)
    f.box(x, 62, 140, 62, b, fill=SOFT, stroke=sk, size=10)
    f.box(x, 136, 140, 62, c, fill=SOFT, stroke=sk, size=10, bold=True)
    if i < 4: f.arrow([(x + 140, 30), (x + 149, 30)], color=SLATE, sw=2)
f.text(76, 215, "Patient's state", size=10, color=SLATE)
f.arrow([(600, 255), (80, 255)], color=RED, sw=2.2, label="RELAPSE: return to an earlier stage, then try again", lpos=(340, 242))
f.text(380, 285, "Stage 6, termination (no temptation), is rarely reached for tobacco", size=10, color=NAVY)
```

**The 5 A's of brief tobacco intervention:** **Ask** every patient about tobacco; **Advise** to quit in a clear, personal way; **Assess** readiness; **Assist** (quit plan, counselling, nicotine replacement, helpline); **Arrange** follow-up. Nepal's **Tobacco Product (Control and Regulation) Act 2068 (2011)** bans smoking in public places, bans sale to minors and requires large pictorial health warnings on packs. Nurses are the largest health workforce and are role models: a smoking nurse weakens the message.

**Eight actions in tobacco-cessation counselling.**

1. **Ask and record tobacco use at every contact.** One short question takes 30 seconds and doubles quit attempts when asked routinely. Record cigarettes per day, years of use and other forms (khaini, hukka, bidi). This builds a picture of risk.
2. **Advise clearly, kindly and personally.** "Quitting is the best thing you can do for your lungs and your children." Link to the person's own cough, finances or family. Avoid blame.
3. **Assess the stage of change and dependence.** Ask, "Are you thinking of quitting?" Use time to first cigarette (within 5 minutes means high dependence). Match advice to the stage (Figure 4.4).
4. **Build motivation (the 5 R's) for those not ready.** Relevance, Risks, Rewards, Roadblocks and Repetition. Use open questions and reflective listening, not argument. Respect the person's right to decide.
5. **Plan the quit date with coping skills.** Set a date within 2 weeks, tell the family, remove cigarettes and ashtrays, and plan for triggers (tea, stress, alcohol). Teach the 4 D's: delay, deep breathing, drink water, do something else. Plans work better when written.
6. **Offer medicine where available.** Nicotine replacement (patch, gum) or other medicines doubles success in people with higher dependence; follow doctor and hospital protocol. Teach correct use and side effects. Refer to a cessation clinic or the helpline.
7. **Use social support.** Family, friends and FCHVs help; a quit buddy increases success. Teach the household to avoid smoking indoors. Support groups use social norms.
8. **Follow up and expect relapse.** Contact within a week, at one month and at three months. A slip is not a failure; review triggers and set a new date. Praise every smoke-free day (reinforcement).

## Formula and fact sheet

- Attitude = Affect + Behaviour + Cognition; dissonance reduced by changing behaviour, belief or adding justification.
- Likert: reverse negative items (6 minus score); Bloom: 80% or more good, 60-79% moderate, below 60% poor.
- Asch: 75% conformed at least once; Milgram: 26/40 = 65% obeyed to 450 V; bystander: 85% with 2 people, 62% with 3, 31% with 6.
- Health Belief Model: susceptibility, severity, benefits, barriers, cues, self-efficacy. Stages: pre-contemplation, contemplation, preparation, action, maintenance (termination).
- Pack-years = (cigarettes per day / 20) x years smoked.

## Chapter summary

- Social psychology studies how people perceive, influence and relate to one another; schemas, stereotypes and attribution errors shape care.
- Attitudes have affect, behaviour and cognition; they change through persuasion, contact and dissonance; Likert scales measure them.
- Conformity, compliance and obedience explain silence in teams, and nurses must speak up; the bystander effect is reduced by naming a person.
- Behaviour change follows the Health Belief Model and the stages of change; the 5 A's and relapse-friendly follow-up work for tobacco.

## Practice

```python
pack_years = 20 / 20 * 25
cost_year = 20 * 15 * 365                     # assumed price Rs 15 per cigarette
patches = (6 + 2 + 2) * 7                     # 21 mg x 6 weeks, 14 mg x 2 weeks, 7 mg x 2 weeks
m2 = 10 / 20 * 30
m3 = (85 - 31) / 85 * 100
asch_errors = 12 * 0.37
print(f"Pack-years = {pack_years:.0f}; cost = Rs {cost_year:,} a year, Rs {cost_year * 10:,} in 10 years")
print(f"Patch course = {patches} patches over {patches // 7} weeks")
print(f"MCQ2 = {m2:.0f} pack-years; MCQ3 = {m3:.1f}% fall; Asch errors in 12 trials = {asch_errors:.1f}; Milgram = {26 / 40 * 100:.0f}%")
```

```text
Pack-years = 25; cost = Rs 109,500 a year, Rs 1,095,000 in 10 years
Patch course = 70 patches over 10 weeks
MCQ2 = 15 pack-years; MCQ3 = 63.5% fall; Asch errors in 12 trials = 4.4; Milgram = 65%
```

**MCQs (with reasons)**

1. The experiment in which subjects judged line lengths against a majority was done by: (a) Milgram (b) Asch (c) Zimbardo (d) Bandura.
2. A person who smokes 10 cigarettes a day for 30 years has: (a) 3 pack-years (b) 15 pack-years (c) 30 pack-years (d) 300 pack-years.
3. A man who says, "I will quit within the next 30 days and have bought a plan," is in the stage of: (a) contemplation (b) preparation (c) action (d) maintenance.
4. Helping falls from 85% to 31% as more bystanders are present. The percentage fall is about: (a) 31% (b) 54% (c) 63.5% (d) 85%.
5. On a Likert scale a negatively worded item rated 2 out of 5 is scored as: (a) 2 (b) 3 (c) 4 (d) 5.

::: note Answers and rationales
**1. (b).** Solomon Asch used line cards and confederates. Milgram studied obedience with shocks, Zimbardo studied roles in a mock prison and Bandura studied observational learning.
**2. (b).** Pack-years = 10 / 20 x 30 = 15. A pack holds 20 cigarettes, so 10 a day is half a pack; 30 would count one full pack per day.
**3. (b).** A firm plan within 30 days is preparation; contemplation is thinking within 6 months and action is already quitting. The 30-day mark defines preparation.
**4. (c).** (85 - 31) / 85 x 100 = 63.5%. The fall in percentage points is 54, but the relative fall is 63.5%; 31% is only the final level.
**5. (c).** A negative item is reversed as 6 - 2 = 4, so that a high score always means a favourable attitude. Leaving it at 2 would understate the attitude.
:::

**Short answer (3 marks): Name the three components of an attitude with an example.** An attitude has an affective part (feeling, "I fear injections"), a behavioural part (tendency to act, "I avoid the clinic") and a cognitive part (belief, "vaccines make children ill"). The three usually agree, and dissonance appears when they do not. Health education targets all three, not only knowledge.

**Medium answer (5 marks): Explain Milgram's experiment and its lessons for nurses.** Milgram (1961-63, Yale) told volunteers to give increasing electric shocks to a learner when he failed a memory task, with a calm experimenter insisting, "The experiment requires that you continue." In the baseline, 26 of 40 (65%) went to 450 volts, although they were distressed. Obedience was lower when the authority was absent, when the victim was close and when others refused (Figure 4.3). The lessons: ordinary people obey authority against conscience; the nurse remains responsible for her act; she should question unsafe orders using SBAR and the chain of command; teams need a culture where anyone may speak up. The study also led to ethical rules of consent, protection from harm and debriefing.

**Long answer (10 marks): Mr Dil Bahadur Gurung, 45 years, a bus conductor, smokes 20 cigarettes a day for 25 years and has a morning cough. He says, "I know it is bad, but I cannot manage stress without it. Maybe next year." His time to first cigarette is 5 minutes. Calculate pack-years and cost (assume Rs 15 a cigarette), name his stage, and write the nursing care plan.**

*Calculations.* Pack-years = 20 / 20 x 25 = **25**. Cost a day = 20 x 15 = Rs 300; a year = 300 x 365 = **Rs 109,500**, and in 10 years **Rs 1,095,000**. If the doctor prescribes nicotine patches for more than 10 cigarettes a day, a standard course is 21 mg for 6 weeks, 14 mg for 2 weeks and 7 mg for 2 weeks, which is **70 patches over 10 weeks** (follow hospital protocol).

*Psychology applied.* He is in **contemplation** ("maybe next year", knows it is bad): he feels **dissonance** between behaviour and belief and holds a **cognitive** excuse (stress). Use the **Health Belief Model** (raise perceived susceptibility with his cough and spirometry; increase perceived benefits with the money saved) and the **5 A's** and **5 R's**; as a bus conductor he works in a smoking culture, so use **social norms** and a buddy.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I cannot manage stress without it." **O:** 25 pack-years, morning cough, high dependence. | **Ineffective health management / risk-prone health behaviour** related to nicotine dependence and low readiness. | **Smoking cessation behaviour:** sets a quit date and tells one family member within 1 month. | 5 A's and motivational interviewing with open questions (builds intrinsic motivation); show his own cost of Rs 109,500 a year (personal reward); offer a quit date plan in writing (commitment). | Quit date chosen. |
| **S:** "I know it is bad, but maybe next year." | **Deficient knowledge / dissonance** about the link of smoking with cough and lung disease. | **Knowledge: health behaviour:** names three harms and three benefits of quitting. | Explain that cough is an early warning (cognition); arrange spirometry or chest X-ray (concrete evidence); give a picture leaflet (retention). | States harms and benefits correctly. |
| **S:** "Stress from the job." **O:** smokes at stops with colleagues. | **Ineffective coping** related to stress and a smoking peer group. | **Coping:** uses two non-smoking stress strategies for 2 weeks. | Teach deep breathing, delay, water and walking (replace the behaviour); plan for triggers (tea breaks, peers); find a quit buddy and a smoke-free colleague (social support). | Reports strategies work. |
| **O:** time to first cigarette 5 minutes; withdrawal risk. | **Risk for ineffective withdrawal management** related to high dependence. | **Substance withdrawal severity:** mild irritability only; no relapse for 4 weeks. | Discuss nicotine replacement with the doctor (21 mg patch, 70 patches in 10 weeks) (doubles quit rate); teach proper use; follow up by phone at 1 week, 1 month and 3 months (support through relapse). | Smoke-free at 4 weeks. |
| **O:** household has children; smokes indoors. | **Risk for impaired parenting / ineffective family health** related to second-hand smoke. | **Family health:** home becomes smoke-free within 1 week. | Teach harm of second-hand smoke to children (protects family); declare the home smoke-free (norm setting); praise each smoke-free day (reinforcement). | Home smoke-free; cough in children reduced. |
