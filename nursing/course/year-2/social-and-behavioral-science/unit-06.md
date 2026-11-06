---
subject: Social and Behavioral Science
grade: BSc Nursing Year 2
unit: 6
title: Stress, Mental Hygiene, Human Relations and Leadership for the Nurse
hours: 12
area: BSN 16 · Social and Behavioral Science · Unit 6
---

It is the fourth night duty in a row. A staff nurse in a busy Kathmandu ward has slept five hours a day, her senior has just shouted at her in front of a patient's family, and she has stopped feeling anything when a patient cries. She is not "weak": she is in **stress** that is moving toward **burnout**. This unit teaches the nurse to understand and manage **stress**, to apply the principles of **mental hygiene**, to build **human relations** (communication, assertiveness, the **Johari window**, conflict resolution) and to **lead** a team. These skills protect the nurse and, through her, every patient.

::: key What this unit gives you
- Real images: **Hans Selye**, **Clifford Beers**, a bronze relief of **Kurt Lewin**, the **Hawthorne Works** plant, a **historical portrait of a Nepali nurse** and a group gathering in Nepal; SVG figures on the General Adaptation Syndrome, Nepali nurse burnout data, the Johari window and the Blake-Mouton leadership grid.
- **Stress**: Selye's alarm-resistance-exhaustion, Lazarus's appraisal and coping, the **PSS-10** scored in Python.
- **Burnout** (Maslach) with **Nepali studies** (TUTH, Birtamode), a confidence interval and eight stress-management actions.
- **Mental hygiene**, mental health in Nepal, Jahoda's criteria; **human relations**, Hawthorne, Berne, assertiveness, Johari, conflict modes.
- **Leadership**: Lewin's styles, Blake-Mouton, Hersey-Blanchard, delegation and a **ward staffing calculation**; a long burnout case with a NANDA-I plan.
:::

## 6.1 Stress and how the body and mind respond

**Stress** is the body's and mind's response to any **demand (stressor)** that seems to exceed or test one's resources. **Selye** (1936) called it "the non-specific response of the body to any demand". **Eustress** is healthy, motivating stress (an exam, a new job); **distress** is harmful stress (loss, overwork, threat). **Stressors** may be **physical** (noise, heat, pain), **psychological** (fear, conflict), **social** (poverty, migration, bereavement) or **occupational** (shift work, high patient load, violence, lack of equipment). The **Holmes-Rahe scale** (see Nursing Concepts, Unit 1) ranks life events by stress value.

```photogrid label="6.1" cols="3" ratio="1.0" caption="Founders of the field. (a) Hans Selye (1907-1982) in his Montreal laboratory in 1956; he described the General Adaptation Syndrome. (b) Clifford W. Beers (1876-1943), founder of the American mental-hygiene movement after his book A Mind That Found Itself (1908). (c) A bronze relief portrait of Kurt Lewin (1890-1947), who defined autocratic, democratic and laissez-faire leadership styles. Wikimedia Commons (public domain and CC BY-SA)."
@ photo id="nur10/selye" cap="Hans Selye, 1956"
fit 1.0
focus 0.5 0.6
mark 0.45 0.72 "1"
mark 0.82 0.40 "2"
key 1 (a) Selye: stress as a general adaptation response
key 2 (a) Laboratory microscope: Selye's rat experiments
@ photo id="nur10/beers" cap="Clifford W. Beers"
fit 1.0
focus 0.5 0.6
mark 0.50 0.32 "3"
key 3 (b) Beers: began the mental-hygiene movement (1908)
@ photo id="nur10/lewin" cap="Kurt Lewin (bronze relief)"
fit 1.0
focus 0.5 0.5
mark 0.50 0.60 "4"
key 4 (c) Lewin: leadership styles and group dynamics
```

**General Adaptation Syndrome (GAS, Figure 6.2).** (1) **Alarm:** the **sympathetic nervous system** and adrenal medulla release adrenaline: heart rate, blood pressure and glucose rise ("fight or flight"). (2) **Resistance:** the **hypothalamus-pituitary-adrenal (HPA) axis** releases CRH, ACTH and **cortisol**; the body adapts but uses reserves. (3) **Exhaustion:** if the stressor continues, resistance falls and illness appears (hypertension, ulcer, infection, depression, burnout).

```svgfig label="6.2" caption="Selye's General Adaptation Syndrome. Resistance to the stressor first falls (alarm: shock, then counter-shock), then rises above normal (resistance), and finally collapses if the stress is prolonged (exhaustion). The nurse's aim is to end or reduce the stressor during the resistance stage, before exhaustion. Right: the HPA axis that supplies cortisol."
f = Fig(760, 300)
pts = [(30, 150), (90, 215), (150, 90), (230, 70), (390, 62), (480, 85), (540, 150), (600, 235)]
f.line(30, 150, 730, 150, color=SLATE, sw=1.2, dash=True)
f.text(715, 140, "Normal", size=10, color=SLATE, anchor="end")
for a, b in zip(pts, pts[1:]): f.line(a[0], a[1], b[0], b[1], color=NAVY, sw=3.2)
f.box(40, 250, 120, 36, "1 ALARM", fill=ROSE, stroke=RED, size=11.5, bold=True)
f.box(200, 250, 300, 36, "2 RESISTANCE (adaptation)", fill=MINT, stroke=TEAL, size=11.5, bold=True)
f.box(520, 250, 120, 36, "3 EXHAUSTION", fill=SAND, stroke=AMBER, size=11.5, bold=True)
f.text(110, 232, "shock", size=10, color=RED); f.text(180, 66, "counter-shock", size=10, color=RED)
f.text(30, 18, "Resistance to stress", size=11, color=NAVY, bold=True, anchor="start")
f.box(640, 20, 110, 28, "Hypothalamus (CRH)", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(640, 70, 110, 28, "Pituitary (ACTH)", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(640, 120, 110, 28, "Adrenal (cortisol)", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.arrow([(695, 48), (695, 70)], color=SLATE, sw=1.8); f.arrow([(695, 98), (695, 120)], color=SLATE, sw=1.8)
```

**Appraisal and coping (Lazarus and Folkman).** The same event stresses people differently because of **appraisal**: **primary** ("Is this a threat or a challenge?") and **secondary** ("Do I have the resources to cope?"). **Coping** is the effort to manage the demand. **Problem-focused coping** changes the situation (asking for help, planning, learning a skill); **emotion-focused coping** changes the feeling (talking, prayer, exercise, music); **avoidant coping** (alcohol, denial) gives short relief and long harm. Good coping uses **both** problem- and emotion-focused methods, plus **social support** (family, friends, colleagues), which was the most useful buffer reported by Nepali health workers.

**Measuring stress: the Perceived Stress Scale (PSS-10).** The nurse rates ten items from 0 (never) to 4 (very often) for the last month; the **positively worded items 4, 5, 7 and 8 are reverse-scored (4 minus rating)**. Total 0-13 is low, **14-26 moderate** and **27-40 high** perceived stress.

```python
raw = [3, 3, 4, 1, 2, 3, 1, 2, 3, 3]                 # one nurse's ratings (0-4) on the 10 items
reverse = [3, 4, 6, 7]                                # items 4, 5, 7, 8 (0-based positions)
scored = [4 - x if i in reverse else x for i, x in enumerate(raw)]
band = lambda s: "low" if s <= 13 else ("moderate" if s <= 26 else "high")
print(f"Raw sum = {sum(raw)} ({band(sum(raw))}); scored items = {scored}")
print(f"PSS-10 total = {sum(scored)} of 40 -> {band(sum(scored))} perceived stress")
```

```text
Raw sum = 25 (moderate); scored items = [3, 3, 4, 3, 2, 3, 3, 2, 3, 3]
PSS-10 total = 29 of 40 -> high perceived stress
```

After reversing items 4, 5, 7 and 8, the nurse scores **29**, **high** stress; without the reversal she would appear only **moderate (25)**, a missed warning.

## 6.2 Burnout and the stress of the nurse

**Burnout** (Maslach) is a syndrome of chronic work stress with **three parts**: **emotional exhaustion** (drained, no energy), **depersonalisation / cynicism** (treating patients as objects, "numbness") and **reduced personal accomplishment** (feeling useless). **Causes:** heavy workload, long and night shifts, low staffing, poor pay and recognition, lack of control, conflict with seniors and relatives, violence, and moral distress. **Nepali evidence:** in a study of **246 nurses** at the **Tribhuwan University Teaching Hospital (TUTH)**, **78.5% had burnout** (88.2% disengaged, 82.9% exhausted) and **58.9% had poor sleep**; **staff nurses had six times higher odds** of burnout than nursing officers or supervisors (PLOS Global Public Health 2025). In Birtamode, burnout was **36%** of 401 nurses, and Shrestha et al. (2021) found moderate burnout in **92.2%** of nurses, with **time pressure (22.2%)**, administrative work and dealing with relatives as main sources, and **family support (29.1%)** as the commonest remedy.

```svgfig label="6.3" caption="Burnout and sleep problems among 246 nurses at TUTH, Kathmandu (OLBI and PSQI; PLOS Global Public Health 2025), against the lower Birtamode figure of 36% (401 nurses). The bars show how common each problem was; a 95% confidence interval for burnout at TUTH is 73.4% to 83.6%, so the true rate is very probably above 70%."
f = Fig(760, 270)
rows = [("Disengagement", 88.2, ROSE, RED), ("Exhaustion", 82.9, ROSE, RED), ("Burnout (both)", 78.5, ROSE, RED), ("Poor sleep quality", 58.9, SAND, AMBER), ("Burnout, Birtamode", 36.0, MINT, TEAL)]
for i, (n, v, fl, sk) in enumerate(rows):
    y = 14 + i * 46
    f.text(190, y + 17, n, size=11.5, color=SLATE, bold=True, anchor="end", vmid=True)
    f.box(200, y, v * 5.4, 34, f"{v:.1f}%", fill=fl, stroke=sk, size=12, bold=True)
f.line(200, 6, 200, 246, color=SLATE, sw=1.4)
f.text(470, 262, "Percent of nurses (TUTH n = 246; Birtamode n = 401)", size=10.5, color=NAVY, bold=True)
```

```python
n, p = 246, 0.785                                      # TUTH nurses, proportion with burnout
cases = round(p * n)
se = (p * (1 - p) / n) ** 0.5
low, high = (p - 1.96 * se) * 100, (p + 1.96 * se) * 100
print(f"Burnout cases = {cases} of {n}; standard error = {se * 100:.2f}%")
print(f"95% CI = {low:.1f}% to {high:.1f}%")
```

```text
Burnout cases = 193 of 246; standard error = 2.62%
95% CI = 73.4% to 83.6%
```

About **193 nurses** had burnout; the **95% confidence interval is 73.4% to 83.6%**, so even the lower limit shows that most nurses in this hospital were affected.

**Eight ways a nurse can manage stress and prevent burnout.**

1. **Recognise the early warning signs.** Constant tiredness, irritability, headaches, poor sleep, loss of interest and a "don't care" feeling are early signals. Write them down and check them against the PSS-10 or Maslach list every month. Early action works far better than late rescue.
2. **Protect sleep.** Poor sleep was found in nearly six in ten nurses at TUTH. Keep a fixed sleep window after nights, use a dark room, avoid tea and screens before sleep, and plan a recovery day. Raise the matter of the roster with the nursing supervisor; sleep is a safety issue.
3. **Use problem-focused skills.** Plan the shift, prioritise (ABC: airway, breathing, circulation first), delegate and ask for help early. Break big tasks into steps. A written to-do list reduces anxiety about forgetting.
4. **Use emotion-focused skills.** Slow breathing (4-second in, 6-second out), progressive muscle relaxation, short walks, music, prayer or meditation lower arousal within minutes. Practise daily, not only in crisis. Regular exercise of 30 minutes on most days helps mood and sleep.
5. **Build social support.** In the Nepali study family (29.1%), friends (21.2%) and hobbies (15.4%) were the most useful remedies. Talk with a trusted colleague after a hard event (peer debriefing). Share the load; do not hide stress for fear of being called weak.
6. **Keep healthy habits.** Eat regular meals, drink water, avoid using alcohol, tobacco or sedatives to cope, and see a doctor for a persistent illness. Substance use is the commonest unhealthy coping route and worsens burnout. Keep a hobby and time with family.
7. **Set boundaries and manage time.** Learn to say "no" politely to extra work that is unsafe. Take your leave and breaks. Leave work thoughts at the ward door through a small ritual (changing clothes, a walk home).
8. **Use organisational help.** Ask for fair rosters and enough staff, report violence, join staff welfare committees and seek counselling or the national helpline 1166. Managers must monitor workload and hold debriefings. Prevention of burnout is partly an organisational duty, and the NNC Code of Ethics supports safe working conditions.

## 6.3 Mental hygiene and mental health

**Mental health** (WHO) is a state of mental well-being that enables people to **cope with the stresses of life, realise their abilities, learn and work well, and contribute to their community**. **Mental hygiene** is the science and practice of **keeping and improving mental health** and preventing mental illness. It began with **Clifford Beers**, who after his own hospital treatment wrote **A Mind That Found Itself** (1908) and founded the first mental-hygiene committee (1909; Plate 6.1b). **Jahoda's criteria** for positive mental health: a **healthy attitude to self**, **growth and self-actualisation**, **integration** (balance of drives), **autonomy**, **accurate perception of reality** and **environmental mastery** (work, love, play and adapting to change). The mentally healthy person is not free of problems; she **copes**, relates to others, accepts her limits and keeps hope.

**Levels of mental-hygiene work.** **Promotive:** build strengths (parenting, school life skills, work-life balance). **Preventive:** *primary* (stop illness: stress management, family support), *secondary* (early case-finding with PHQ-9, GAD-7, referral by health post nurses and FCHVs) and *tertiary* (rehabilitation and relapse prevention). **Curative:** treatment under the mhGAP and psychiatric services (see Psychiatric Nursing). **Settings:** the **family** (love, security and discipline without violence), the **school** (guidance counsellors, anti-bullying), the **workplace** (fair load, grievance route) and the **community** (peer groups, mothers' groups, helplines). Nepal's **National Mental Health Survey 2020** (NHRC, see Psychiatric Nursing, Unit 1) shows that mental disorders are common and most people receive no treatment, so mental hygiene must reach villages and workplaces, not only hospitals.

**Eight principles of daily mental hygiene.**

1. **Know and accept yourself.** Write your strengths and limits honestly and accept both. People who accept themselves cope better with failure. Avoid constant comparison with others.
2. **Keep a balanced routine.** Fixed times for sleep, meals, work, study, rest and play protect the brain. Chaos and long unbroken work raise stress hormones. Balance is a daily habit, not a holiday.
3. **Build close relationships.** Share feelings with at least two trusted people. Social support buffers stress and reduces depression and suicide. Make time for family and friends even when busy.
4. **Express emotions in healthy ways.** Talk, write, draw, sing, pray or exercise rather than hiding anger or sadness. Suppressed feelings come out as headache, sleeplessness or outbursts. Learn to name feelings: "I feel hurt", "I feel afraid".
5. **Develop interests and purpose.** A hobby, a faith, service to others and small goals give meaning. People with purpose recover faster from loss. Volunteer, learn a skill, join a club.
6. **Practise problem-solving.** Define the problem, list options, weigh each, try one and review. This turns worry into action. Ask for advice early.
7. **Avoid harmful escapes.** Alcohol, tobacco, sedatives and gambling relieve stress briefly and worsen it later. Choose exercise, relaxation and talking instead. Seek help if you cannot stop.
8. **Seek help early.** Asking for help is a sign of strength. Know the local doctor, counsellor, psychosocial worker and helpline 1166. Treat mental illness like any illness, and support others without judgement.

## 6.4 Human relations

**Human relations** are the ways people communicate, cooperate and resolve differences at work. The **Hawthorne studies** (Mayo and Roethlisberger, Western Electric Hawthorne Works, USA, 1924-1932; Plate 6.4a) first showed that **output rose when workers felt noticed, valued and part of a group**, whatever the lighting or rest-pause. The lessons: **informal groups** have strong norms; **attention and participation** motivate; people are not machines. The **human relations school** led to modern ideas of **team building, motivation (Maslow, Herzberg) and participative management**, and it is why a nurse manager asks, "How are you?" before "Why is the chart incomplete?"

```photogrid label="6.4" cols="3" ratio="1.0" caption="Relations at work and in the community. (a) The Western Electric Hawthorne Works, Illinois, in 1925, where the Hawthorne studies of worker behaviour began. (b) A historical portrait of a nurse in the uniform used in Nepal; the profession's culture of caring and discipline is a social institution. (c) People seated together at a community gathering in Nepal: shared practice and group belonging are sources of social support. Wikimedia Commons (public domain, no known restrictions, CC BY)."
@ photo id="nur10/hawthorne" cap="Hawthorne Works, 1925"
fit 1.0
focus 0.55 0.5
mark 0.55 0.55 "1"
key 1 (a) Large factory complex where the studies were done
@ photo id="nur10/nepnurse" cap="Nurse in Nepal uniform (historical)"
fit 1.0
focus 0.5 0.7
mark 0.50 0.78 "2"
key 2 (b) The nurse's cap and white uniform: professional identity
@ photo id="nur10/meditate" cap="Community gathering, Nepal"
fit 1.0
focus 0.5 0.5
mark 0.50 0.62 "3"
key 3 (c) Group seated together: belonging and social support
```

**Transactional analysis (Berne).** Every person has three **ego states**: **Parent** (rules, "should", care or control), **Adult** (facts, reason) and **Child** (feelings, play, rebellion). A **complementary** transaction (Adult to Adult) keeps communication open; a **crossed** transaction ("What time is the drug round?" / "Why are you always checking on me?") causes conflict. Aim for **Adult-Adult** exchanges. **Assertiveness** is stating your needs and rights **clearly and respectfully**: **passive** (gives in, resentful), **aggressive** (wins by hurting) and **assertive** (honest, direct, fair). Use an **"I" statement**: "When the drug trolley is not checked (event), I feel worried (feeling) because errors can harm patients (reason); please check it with me (request)."

**Johari window (Luft and Ingham, 1955)** shows how well we and others know us (Figure 6.5). The **open arena** is known to self and others; the **blind spot** is known only to others; the **hidden (façade)** is known only to self; the **unknown** is known to nobody. **Self-disclosure** shrinks the hidden area and **feedback** shrinks the blind spot; as the open arena grows, trust and teamwork grow.

```svgfig label="6.5" caption="The Johari window. Known to self (left column) and not known to self (right column), crossed with known to others (top row) and not known to others (bottom row). Feedback moves things from blind spot to open arena; self-disclosure moves them from hidden to open; reflection and new experience reveal the unknown. A good team has a large open arena."
f = Fig(760, 310)
f.text(255, 18, "KNOWN TO SELF", size=11, color=NAVY, bold=True); f.text(555, 18, "NOT KNOWN TO SELF", size=11, color=NAVY, bold=True)
f.text(60, 100, "KNOWN TO", size=10.5, color=NAVY, bold=True); f.text(60, 114, "OTHERS", size=10.5, color=NAVY, bold=True)
f.text(60, 230, "NOT KNOWN", size=10.5, color=NAVY, bold=True); f.text(60, 244, "TO OTHERS", size=10.5, color=NAVY, bold=True)
f.box(110, 30, 290, 125, "1 OPEN ARENA\nPublic: skills, role, habits\nWe both see it", fill=MINT, stroke=TEAL, size=12, bold=True)
f.box(410, 30, 290, 125, "2 BLIND SPOT\nOthers notice, I do not\n(a sharp tone, late arrival)", fill=SAND, stroke=AMBER, size=12, bold=True)
f.box(110, 165, 290, 125, "3 HIDDEN (FACADE)\nI know, others do not\n(fear, a secret, an unspoken wish)", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(410, 165, 290, 125, "4 UNKNOWN\nNeither knows yet\n(hidden talents, deep fears)", fill=ROSE, stroke=RED, size=12, bold=True)
f.arrow([(560, 155), (400, 120)], color=TEAL, sw=2, label="FEEDBACK", lpos=(480, 130))
f.arrow([(385, 185), (385, 135)], color=TEAL, sw=2)
f.text(325, 180, "DISCLOSURE", size=9.5, color=TEAL, bold=True)
```

**Conflict management (Thomas and Kilmann).** Five modes combine **assertiveness** and **cooperativeness**: **competing** (win-lose; use in an emergency), **collaborating** (win-win; best for important issues), **compromising** (half each; for equal power and time limits), **avoiding** (postpone; for trivial issues or cooling off) and **accommodating** (give way; to keep peace). Steps: **listen**, **state the problem without blame**, **find common goals**, **generate options** and **agree an action**; involve the **supervisor** and the **grievance route** if talks fail. **Emotional intelligence** (Goleman: self-awareness, self-regulation, motivation, empathy, social skill) helps all steps.

**Eight habits of good human relations on the ward.**

1. **Greet and learn names.** Use patients' and colleagues' names and a respectful "ji" or "didi/dai" as custom suggests. A greeting costs nothing and builds trust. Remembering a name shows that a person matters.
2. **Listen fully.** Give attention, do not interrupt and reflect back what you heard ("You are worried about the night shift"). Most conflicts begin with feeling unheard. Active listening is the base of all communication.
3. **Give and receive feedback kindly.** Praise in public and correct in private, using facts and "I" statements. Ask for feedback to shrink your blind spot. Thank people who tell you the truth.
4. **Respect diversity.** Caste, gender, language, religion and disability must not change the quality of care or teamwork. Avoid jokes or labels that hurt. The NNC Code of Ethics requires non-discrimination.
5. **Be assertive, not passive or aggressive.** Say "no" when a request is unsafe and "yes" when it is reasonable. Speak calmly and look at the person. Assertiveness protects patients and yourself.
6. **Resolve conflict early.** Do not let anger grow for days. Choose a private place and time, aim for a solution and not for blame. Use the collaborating mode for important problems.
7. **Work as a team.** Share information at handover (SBAR), offer help and recognise others' efforts. Teams that share credit achieve more. Avoid gossip and cliques, which damage morale.
8. **Show empathy and keep confidentiality.** Try to see the situation from the other person's side. Never discuss a patient or a colleague's problem in public. Trust is the base of every relation in health care.

## 6.5 Leadership in nursing

**Leadership** is **influencing a group to reach a shared goal**; **management** is **planning, organising, staffing, directing and controlling** resources. A nurse leader is often both: the ward in-charge leads people and manages beds, drugs and rosters. **Theories:** **Trait** (born leaders: honesty, vision), **behavioural** (what leaders do) and **situational** (the best style depends on the situation).

**Lewin's three styles** (Plate 6.1c): **Autocratic** (leader decides; fast, good in an emergency or cardiac arrest, but low morale); **Democratic / participative** (group shares in decisions; best for planning, quality, complex care); **Laissez-faire** (leader leaves the group alone; works only with highly skilled, motivated staff, otherwise chaos). **Blake and Mouton's Managerial Grid** rates **concern for people** and **concern for production** from 1 to 9 (Figure 6.6). **Hersey-Blanchard** matches style to the **readiness** of the follower: **telling** (S1, low ability and willingness), **selling** (S2), **participating** (S3) and **delegating** (S4, high readiness). **Transformational** leaders inspire, give vision and develop people; **transactional** leaders use rewards and rules. Nursing needs both.

```svgfig label="6.6" caption="The Blake-Mouton Managerial Grid. Concern for production runs along the horizontal axis and concern for people along the vertical axis, each from 1 to 9. The team style (9,9) combines high output with high care for staff and is the usual target for a ward in-charge. Impoverished (1,1) and country club (1,9) styles fail on results; authority-compliance (9,1) fails on morale."
f = Fig(760, 330)
f.line(110, 20, 110, 290, color=SLATE, sw=2); f.line(110, 290, 540, 290, color=SLATE, sw=2)
f.text(325, 318, "CONCERN FOR PRODUCTION  (1 low ... 9 high)", size=11, color=NAVY, bold=True)
f.text(40, 150, "CONCERN", size=10.5, color=NAVY, bold=True); f.text(40, 164, "FOR PEOPLE", size=10.5, color=NAVY, bold=True)
f.box(115, 25, 120, 70, "COUNTRY CLUB\n(1,9)\nHappy staff,\nweak results", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(415, 25, 120, 70, "TEAM\n(9,9)\nHigh output,\nhigh morale", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(265, 125, 120, 70, "MIDDLE ROAD\n(5,5)\nAdequate,\ncompromise", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(115, 215, 120, 70, "IMPOVERISHED\n(1,1)\nMinimum\neffort", fill=ROSE, stroke=RED, size=10, bold=True)
f.box(415, 215, 120, 70, "AUTHORITY-\nCOMPLIANCE\n(9,1)\nResults at any cost", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(570, 25, 180, 120, "WARD IN-CHARGE CHECK\nDo I plan the work AND care for\nthe staff? Aim for (9,9):\nclear goals, shared decisions,\nfeedback and recognition", fill=SOFT, stroke=NAVY, size=10)
f.arrow([(570, 85), (537, 70)], color=TEAL, sw=2)
```

**Delegation** is giving a task to another person while keeping the **accountability**. The **five rights of delegation:** the right **task**, the right **circumstance**, the right **person**, the right **direction and communication**, and the right **supervision and evaluation**. A staff nurse may delegate bed-making or vital signs to a trained assistant, but not assessment, planning or evaluation. **Staffing** uses **nursing hours per patient day (NHPPD)**: for a 30-bed ward with 80% occupancy (24 patients) and 3.5 hours of care per patient per day, the ward needs 24 x 3.5 = **84 hours**; with 6 productive hours per nurse-shift that is **14 nurse-shifts** a day, and with **20% added for leave, sickness and relief**, about **16.8, rounded up to 17**.

**Eight qualities and actions of a good nurse leader.**

1. **Have a clear vision and goals.** Tell the team what the ward is aiming for ("zero bed sores, every patient with a name band"). Goals must be specific and measurable. People work harder when they know why.
2. **Lead by example.** Wash hands, arrive on time, follow protocols and treat everyone with respect. Staff copy what leaders do, not what they say (Bandura). One good example is worth many orders.
3. **Communicate openly.** Hold short briefings at each shift, explain changes, and listen to ideas. Use SBAR for handover. Open communication reduces rumour and error.
4. **Involve staff in decisions.** Use the democratic style for planning and quality issues, and the autocratic style only in emergencies. Participation raises ownership. Invite quiet staff to speak.
5. **Delegate wisely and develop people.** Give tasks that match skill, supervise, and give feedback and training. Support juniors to grow into leaders. Delegation is trust with responsibility.
6. **Be fair and ethical.** Share duty rosters and leave justly, avoid favouritism and follow the NNC Code of Ethics. Fairness builds trust. Protect whistle-blowers who raise safety concerns.
7. **Manage conflict and stress in the team.** Notice tired and distressed staff, give rest and listen, and settle conflicts early. Arrange peer debriefing after a death or an assault. A leader who protects her team protects her patients.
8. **Recognise effort and keep learning.** Thank staff publicly, report good work to management and keep updating skills through CPD. Recognition is a cheap, powerful motivator. A leader must remain a learner.

## Formula and fact sheet

- GAS: alarm (adrenaline, sympathetic) - resistance (HPA axis, cortisol) - exhaustion. Appraisal: primary (threat?) and secondary (resources?).
- PSS-10: items 0-4; reverse items 4, 5, 7, 8 (4 minus rating); 0-13 low, 14-26 moderate, 27-40 high.
- Burnout (Maslach): emotional exhaustion, depersonalisation, reduced personal accomplishment. 95% CI for a proportion = p +/- 1.96 x sqrt(p(1 - p) / n).
- Johari: open, blind, hidden, unknown; feedback shrinks blind spot, disclosure shrinks hidden.
- Thomas-Kilmann: competing, collaborating, compromising, avoiding, accommodating. Berne: Parent, Adult, Child.
- Lewin: autocratic, democratic, laissez-faire. Blake-Mouton (9,9) = team. Hersey-Blanchard: telling, selling, participating, delegating.
- Nurse-shifts needed = patients x NHPPD / productive hours per shift; add relief percentage and round up.
- Sleep debt = (need - actual) x nights; weekly hours = shifts x hours; Labour Act 2074 normal limit 8 h a day and 48 h a week.

## Chapter summary

- Stress is the response to a demand; Selye's GAS has alarm, resistance and exhaustion; appraisal and coping decide the outcome; the PSS-10 measures it.
- Burnout has three parts and is very common among Nepali nurses (78.5% at TUTH); prevention uses sleep, coping skills, support, boundaries and fair workloads.
- Mental hygiene promotes, prevents and treats; Jahoda's criteria describe positive mental health.
- Good human relations use Adult-Adult transactions, assertiveness, feedback (Johari) and collaborative conflict resolution.
- Leaders match style to the situation, aim for (9,9), delegate with the five rights and use NHPPD for staffing.

## Practice

```python
import math
raw = [3, 3, 4, 1, 2, 3, 1, 2, 3, 3]
scored = [4 - x if i in (3, 4, 6, 7) else x for i, x in enumerate(raw)]
band = lambda s: "low" if s <= 13 else ("moderate" if s <= 26 else "high")
patients = 30 * 0.8
hours = patients * 3.5
shifts = hours / 6
relief = shifts * 1.2
debt = (7.5 - 5.0) * 5
week = 5 * 12
p, n = 0.785, 246
se = (p * (1 - p) / n) ** 0.5
print(f"MCQ2 raw = {sum(raw)} ({band(sum(raw))}); scored = {sum(scored)} ({band(sum(scored))})")
print(f"MCQ4 patients = {patients:.0f}; hours = {hours:.0f}; nurse-shifts = {shifts:.0f}; with 20% relief = {relief:.1f} -> {math.ceil(relief)}")
print(f"TUTH 95% CI = {(p - 1.96 * se) * 100:.1f}% to {(p + 1.96 * se) * 100:.1f}%")
print(f"Case: sleep debt = {debt:.1f} h a week; weekly hours = {week} against 48 = {week - 48} h over ({week / 48 * 100:.1f}% of the limit)")
```

```text
MCQ2 raw = 25 (moderate); scored = 29 (high)
MCQ4 patients = 24; hours = 84; nurse-shifts = 14; with 20% relief = 16.8 -> 17
TUTH 95% CI = 73.4% to 83.6%
Case: sleep debt = 12.5 h a week; weekly hours = 60 against 48 = 12 h over (125.0% of the limit)
```

**MCQs (with reasons)**

1. In Selye's General Adaptation Syndrome, the stage in which the HPA axis releases cortisol and the body adapts to a continuing stressor is: (a) alarm (b) resistance (c) exhaustion (d) recovery.
2. A nurse's PSS-10 raw total is 25, and after reversing items 4, 5, 7 and 8 it is 29. Her perceived stress is: (a) low (b) moderate (c) high (d) cannot be classified.
3. Colleagues notice that a nurse speaks sharply at handover, but she does not know it. In the Johari window this is her: (a) open arena (b) blind spot (c) hidden area (d) unknown area.
4. A 30-bed ward has 80% occupancy and needs 3.5 nursing hours per patient per day; a nurse gives 6 productive hours per shift. With 20% added for relief, the nurse-shifts needed per day are: (a) 14 (b) 16 (c) 17 (d) 21.
5. The best leadership style during a cardiac arrest on the ward is: (a) laissez-faire (b) democratic (c) autocratic (d) country club.

::: note Answers and rationales
**1. (b).** Resistance is the adaptation stage in which cortisol from the HPA axis keeps the body coping. Alarm is the first adrenaline surge and exhaustion is the collapse that follows prolonged stress.
**2. (c).** The correct score is the reversed total, 29, which is above 26 and so is high. The raw sum of 25 would wrongly be called moderate because four items are positively worded.
**3. (b).** A trait known to others but not to the person is the blind spot; feedback reduces it. The hidden area is the opposite: known to self only.
**4. (c).** 24 patients x 3.5 = 84 hours; 84 / 6 = 14 nurse-shifts; 14 x 1.2 = 16.8, rounded up to 17. Rounding down would leave the ward short.
**5. (c).** An emergency needs one clear leader to give quick orders; this is a justified use of the autocratic style. Democratic discussion wastes time and laissez-faire leaves the team without direction.
:::

**Short answer (3 marks): Name the three components of burnout.** Burnout (Maslach) has **emotional exhaustion** (feeling drained and without energy), **depersonalisation or cynicism** (treating patients as objects or becoming numb) and **reduced personal accomplishment** (feeling ineffective). It results from chronic work stress such as heavy load, night shifts and poor support. In a TUTH study 78.5% of nurses had burnout. Prevention needs sleep, coping skills, social support and fair staffing.

**Medium answer (5 marks): Describe Selye's General Adaptation Syndrome.** Selye (1936) described the body's general response to any stressor in three stages (Figure 6.2). **Alarm:** the hypothalamus triggers the sympathetic nervous system and adrenal medulla, giving adrenaline-driven "fight or flight" with fast heart rate, raised blood pressure, glucose and alertness; resistance first dips (shock) and then rises (counter-shock). **Resistance:** if the stressor continues, the HPA axis releases CRH, ACTH and cortisol; the body adapts and appears to cope, but uses up reserves. **Exhaustion:** if stress is prolonged, resistance falls; signs include hypertension, peptic ulcer, infections, depression and burnout. The nurse recognises the stage and acts: remove or reduce the stressor in the resistance stage, teach relaxation and coping, and refer those near exhaustion. Chronic cortisol raises blood glucose and lowers immunity, which links stress to disease.

**Medium answer (5 marks): Explain the Johari window and its use in nursing.** The Johari window (Luft and Ingham, 1955) is a four-part model of self-awareness and communication (Figure 6.5). The **open arena** is known to self and others; the **blind spot** is known to others but not to self; the **hidden (facade)** is known to self but not to others; the **unknown** is known to neither. **Feedback** from others reduces the blind spot, and **self-disclosure** reduces the hidden area, so the open arena grows. In nursing, a larger open arena means better trust, communication and teamwork: a nurse who asks for feedback learns that her tone sounds sharp; a nurse who shares her workload worries receives help; a manager who encourages open discussion lowers errors. Students use it to build self-awareness during clinical placement, and teams use it in debriefings.

**Long answer (10 marks): Sunita Thapa, 26 years, a staff nurse in the ICU of a tertiary hospital in Kathmandu, has worked five night shifts of 12 hours this week, sleeps only 5 hours in the day (she needs 7.5), and scores 29 on the PSS-10. She says: "I feel nothing when a patient dies. I snap at my colleagues and I cannot sleep even when I am tired." Using the unit: (a) identify her stage of stress and the problem, (b) calculate her sleep debt and working hours, and (c) write the nursing care plan for the nurse, and the actions of her supervisor.**

*Analysis.* She is in the **exhaustion stage** of the GAS, with burnout: **emotional exhaustion** (tired but sleepless), **depersonalisation** ("I feel nothing") and irritability, which her colleagues see as a **blind spot** in the Johari window. Her **PSS-10 of 29 is high** (raw 25 would have missed it). Her **staff-nurse position, night work and poor sleep** match the TUTH risk factors (staff nurses had six times the odds of burnout; 58.9% had poor sleep).

*Calculations.* Sleep debt = (7.5 - 5.0) x 5 days = **12.5 hours a week**. Weekly hours = 5 x 12 = **60 hours**, which is **12 hours over** the 48-hour weekly limit of the Labour Act 2074 (125% of the limit), a safety and legal concern for the hospital. At ICU level she needs good rest, because fatigue raises medication errors.

*Supervisor's actions.* Reduce consecutive night shifts, correct the roster to the legal limit, add relief staff (for a 30-bed ward 14 nurse-shifts need about 17 with relief), arrange a **peer debriefing** after deaths, offer a counselling referral, and use a **democratic style** to involve staff in the new roster. Use **assertive "I" statements** to resolve conflict with colleagues.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I cannot sleep even when I am tired." **O:** sleep 5 h against need 7.5 h; sleep debt 12.5 h a week. | **Disturbed sleep pattern** related to rotating night shifts and stress. | **Sleep:** sleeps 7 hours in 24 within 2 weeks. | Teach sleep hygiene: dark room, fixed sleep window, no tea or screens before sleep (improves sleep quality); ask supervisor for no more than 3 consecutive nights (restores recovery). | Sleeps 7 hours; feels rested. |
| **S:** "I feel nothing when a patient dies." **O:** PSS-10 of 29 (high); irritability. | **Burnout (exhaustion, depersonalisation)**; **ineffective coping** related to chronic work stress. | **Stress level:** PSS-10 below 27 in 1 month; names two coping strategies. | Active listening and a non-judging talk (reduces isolation); teach 4-6 breathing and muscle relaxation (lowers arousal); peer debriefing after deaths (processes grief); refer to counsellor (professional support). | PSS-10 falls; uses strategies. |
| **O:** snaps at colleagues; conflict at handover. | **Impaired social interaction** related to fatigue and irritability. | **Social interaction skills:** uses "I" statements in 2 weeks and has no reported conflict. | Teach assertive "I" statements and Adult-Adult transactions (clear, respectful communication); ask for feedback to reduce blind spot (self-awareness); mediate with the colleague (collaborating style). | No new conflict. |
| **O:** 60 hours a week; 12 h overtime. | **Risk for injury / risk-prone health behaviour** related to fatigue and overwork. | **Safety behaviour:** works within 48 hours a week by next roster. | Report the roster to the nursing supervisor with a written request (organisational action); use double-check for high-risk drugs (prevents error); schedule leave and rest days. | Roster corrected; no errors. |
| **S:** "I don't talk to anyone at home." **O:** low social support. | **Social isolation / inadequate support** related to shift work and shame. | **Social support:** names two support people and contacts one weekly. | Encourage family and friends contact and a hobby (family support was the main remedy in Nepali nurses); invite her to the staff welfare group; give the helpline number 1166 (access to help). | Contacts weekly; uses support. |
