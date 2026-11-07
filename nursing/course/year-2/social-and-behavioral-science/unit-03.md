---
subject: Social and Behavioral Science
grade: BSc Nursing Year 2
unit: 3
title: Psychology for Nursing: Learning, Memory, Motivation, Intelligence and Personality
hours: 16
area: BSN 16 · Social and Behavioral Science · Unit 3
---

A five-year-old in Dang cries the moment she sees the white coat at the immunisation table, though no needle is in sight. Her brother, last week, would not touch his school bag until his mother promised sweets. A grandmother forgets the instructions for her tablets by the time she reaches the bus. All three are **psychology** at work: **learning, motivation and memory**. **Psychology** is the scientific study of behaviour (what we do) and mental processes (what we think and feel). This unit teaches the core ideas a nurse uses every day to understand, teach and care for people.

::: key What this unit gives you
- Real images: **portraits of Wundt, Pavlov, Freud and Maslow**; a **preserved Pavlov dog**, a **Skinner-type operant chamber** and **Kohs blocks** used in Wechsler tests; SVG figures on conditioning, Maslow's pyramid and the forgetting and IQ curves.
- Definition, goals, **schools of psychology** and methods; relevance to nursing.
- **Learning**: classical and operant conditioning, reinforcement schedules, social learning; **memory** stages and the Ebbinghaus forgetting curve (worked out).
- **Motivation and emotion** (Maslow, drive, James-Lange and Cannon-Bard); **intelligence** (ratio and deviation IQ, normal curve, intellectual disability); **personality** (Freud, Erikson, Big Five).
- Eight applications of learning in nursing, eight ways to make teaching stick, model answers and a 5-column NANDA-I plan for a child with mild intellectual disability.
:::

## 3.1 What is psychology? Schools and methods

The word comes from Greek *psyche* (mind, soul) and *logos* (study). **Wilhelm Wundt** opened the first psychology laboratory in Leipzig in **1879**, which marks psychology as a science. Its **goals** are to **describe, explain, predict and control** (or modify) behaviour. **Branches** include clinical, counselling, health, developmental, social, educational and industrial psychology; **health psychology** and **clinical psychology** matter most to nurses.

```photogrid label="3.1" cols="4" ratio="1.0" caption="Pioneers of psychology. (a) Wilhelm Wundt (1832-1920), founder of the Leipzig laboratory. (b) Ivan Pavlov (1849-1936), discoverer of classical conditioning. (c) Sigmund Freud (1856-1939), founder of psychoanalysis, photographed by Max Halberstadt. (d) Abraham Maslow (1908-1970), humanistic psychologist. Public-domain images from Wikimedia Commons."
@ photo id="nur10/wundt" cap="Wilhelm Wundt"
fit 1.0
focus 0.5 0.7
mark 0.50 0.66 "1"
key 1 (a) Wundt: structuralism, introspection, the first laboratory (1879)
@ photo id="nur10/pavlov" cap="Ivan Pavlov"
fit 1.0
focus 0.5 0.6
mark 0.45 0.68 "2"
key 2 (b) Pavlov: salivation of dogs, the conditioned reflex
@ photo id="nur10/freud" cap="Sigmund Freud"
fit 1.0
focus 0.5 0.8
mark 0.45 0.68 "3"
key 3 (c) Freud: unconscious mind, id, ego, superego, defence mechanisms
@ photo id="nur10/maslow" cap="Abraham Maslow"
fit 1.0
focus 0.5 0.5
mark 0.45 0.55 "4"
key 4 (d) Maslow: hierarchy of needs, self-actualisation
```

| School | Founder | Main idea | Use in nursing |
|---|---|---|---|
| Structuralism | Wundt, Titchener | Break the mind into elements by introspection | Patient's own report of sensations (pain) |
| Functionalism | William James | Study the purpose of mind in adapting | Coping and adjustment to illness |
| Behaviourism | Watson, Skinner | Only observable behaviour; learning by conditioning | Habit change, phobia treatment, rewards |
| Psychoanalysis | Freud | Unconscious drives and childhood shape behaviour | Defence mechanisms, therapeutic listening |
| Humanistic | Maslow, Rogers | Free will, needs, growth, unconditional regard | Patient-centred care, empathy |
| Cognitive | Piaget, Beck | Thinking shapes feeling and action | CBT, health education, memory |
| Biological | Many | Brain, genes and hormones drive behaviour | Drug therapy, delirium, dementia |

**Methods:** **experimental** (control variables, test cause and effect), **observation** (naturalistic or participant), **survey and questionnaire**, **interview**, **case study** (one person deeply, as in clinical practice), **correlation** (relation, not cause) and **psychological testing**. **Ethics in research**: informed consent, no harm, confidentiality, debriefing and the right to withdraw.

## 3.2 Learning

**Learning** is a relatively lasting change in behaviour produced by experience. It is not a change from drugs, illness or fatigue. There are three major kinds.

**Classical conditioning (Pavlov).** A neutral stimulus (bell) is paired again and again with an unconditioned stimulus (food) that naturally causes an unconditioned response (salivation). In time the bell alone (now the **conditioned stimulus**) causes the **conditioned response**. Key terms: **acquisition**, **extinction** (response fades when the pairing stops), **spontaneous recovery**, **generalisation** (similar stimuli work) and **discrimination**. The child who fears the white coat has been conditioned: the coat was paired with the painful needle. **Counter-conditioning** and **systematic desensitisation** (Wolpe) pair the coat with calm, step by step.

**Operant conditioning (Thorndike, Skinner).** Behaviour is shaped by its **consequences**. **Positive reinforcement** adds a pleasant result (praise, sticker); **negative reinforcement** removes an unpleasant one (pain stops when the limb is moved correctly); both **increase** behaviour. **Punishment** decreases behaviour (adding something unpleasant, or removing something pleasant) and is the weakest tool because it teaches fear. **Shaping** rewards steps towards the goal.

```svgfig label="3.2" caption="Two basic kinds of learning. Top: classical conditioning in three stages (before, during, after). The bell is neutral until it is paired with food; then the bell alone makes the dog salivate. Bottom: operant conditioning. A behaviour followed by a pleasant consequence is repeated; one followed by an unpleasant consequence is dropped. Nursing example: the child fears the coat (classical) and cooperates for a sticker (operant)."
f = Fig(760, 300)
f.box(10, 10, 230, 60, "BEFORE: food (US)\n-> salivation (UR)\nbell (NS) -> no response", fill=BLUE, stroke=NAVY, size=10.5)
f.box(265, 10, 230, 60, "DURING: bell + food (repeated)\n-> salivation", fill=SAND, stroke=AMBER, size=10.5)
f.box(520, 10, 230, 60, "AFTER: bell (CS) alone\n-> salivation (CR)", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(240, 40), (265, 40)], color=SLATE, sw=2); f.arrow([(495, 40), (520, 40)], color=SLATE, sw=2)
f.box(10, 110, 170, 50, "BEHAVIOUR\n(child holds still)", fill=SOFT, stroke=NAVY, size=10.5, bold=True)
f.box(240, 100, 230, 32, "Pleasant result: sticker, praise", fill=MINT, stroke=TEAL, size=10.5)
f.box(240, 146, 230, 32, "Unpleasant result: scolding", fill=ROSE, stroke=RED, size=10.5)
f.arrow([(180, 135), (240, 116)], color=TEAL, sw=2); f.arrow([(180, 135), (240, 162)], color=RED, sw=2)
f.box(520, 100, 230, 32, "Behaviour INCREASES (reinforced)", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(520, 146, 230, 32, "Behaviour DECREASES (punished)", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(470, 116), (520, 116)], color=TEAL, sw=2); f.arrow([(470, 162), (520, 162)], color=RED, sw=2)
f.box(10, 205, 740, 80, "Reinforcement schedules: FIXED RATIO (every 5th response, fast and steady) | VARIABLE RATIO (unpredictable, strongest, like gambling) |\nFIXED INTERVAL (after set time, rises before the reward) | VARIABLE INTERVAL (random time, slow and steady, like checking messages)", fill=SOFT, stroke=SLATE, size=10.5)
```

**Social (observational) learning (Bandura).** People learn by **watching models** and imitating them when they see the model rewarded; the stages are **attention, retention, reproduction and motivation**. This is why a student nurse copies a senior's hand-washing, and why children copy parents who smoke. **Cognitive learning** includes insight (Kohler) and latent learning (Tolman).

**Eight applications of learning principles in nursing.**

1. **Treat fear with desensitisation.** For needle or hospital fear, build a ladder: see the coat, hold the syringe cap, touch the arm, then the vaccine. Each step is done only when the child is calm. Fear fades by extinction.
2. **Reinforce desired behaviour at once.** Praise, a smile or a sticker immediately after a child holds still or a patient walks makes it more likely again. Delayed praise works poorly. Always notice effort, not only success.
3. **Use shaping for rehabilitation.** A stroke patient is rewarded for each small movement, then for a bigger one. Goals are broken into small steps. This keeps motivation high.
4. **Use the nurse as a model.** Patients and students copy what we do. Wash hands in front of mothers; do not smoke near the ward. Modelling teaches more than lectures.
5. **Use a token economy and contracts.** In psychiatric wards and for children, points for self-care are exchanged for privileges. A written contract for diet or exercise sets clear rules. Consistency matters.
6. **Avoid punishment.** Scolding a patient who missed medicines teaches hiding, not taking. Find the reason, remove the barrier and reward adherence. Punishment also harms the relationship.
7. **Plan practice and feedback.** Skills (injection, insulin technique, BP) are learnt by demonstration, return demonstration and feedback until safe. Practice must be repeated. Learning is checked by doing, not asking.
8. **Break conditioned links.** A patient who feels nauseated at the sight of the chemotherapy ward shows a conditioned response. Give anti-emetics early, use relaxation and keep the setting pleasant. This stops the link from growing.

## 3.3 Memory and forgetting

**Memory** has three steps: **encoding** (taking in), **storage** and **retrieval**. Stages (Atkinson-Shiffrin): **sensory memory** (under 1-2 seconds), **short-term memory** (about 7 +/- 2 items, 15-30 seconds unless rehearsed) and **long-term memory** (unlimited; **explicit** facts and events, **implicit** skills and habits). **Forgetting** comes from decay, interference (old versus new), retrieval failure and motivated forgetting (repression). **Ebbinghaus** (1885) showed that retention falls steeply at first and then slowly: **R = e^(-t/S)**, where R is retention, t is time and S is memory strength (here in days). Review makes S larger.

```python
import math
S = 2.0                                        # memory strength in days (teaching value)
for t in (1, 2, 7):
    print(f"Day {t}: retention {math.exp(-t / S) * 100:.1f}%")
S2 = S * 2                                     # one review doubles the strength
print(f"Day 7 with a review that doubles S: {math.exp(-7 / S2) * 100:.1f}%")
print(f"FR-5 schedule: 20 responses give {20 // 5} reinforcers")
```

```text
Day 1: retention 60.7%
Day 2: retention 36.8%
Day 7: retention 3.0%
Day 7 with a review that doubles S: 17.4%
FR-5 schedule: 20 responses give 4 reinforcers
```

With S = 2 days the patient keeps **60.7%** after one day, **36.8%** after two and only **3.0%** after a week; one review that doubles S lifts day-7 retention to **17.4%**. A fixed-ratio 5 schedule gives **4** reinforcers for 20 responses. The lesson: **teach the key message, repeat it within 24 hours, and review later**.

**Eight ways to make patient teaching stick.**

1. **Give the most important point first.** People remember the first and last items best (primacy and recency). Say the key message at the start and end. Limit to three main points.
2. **Use simple Nepali words and pictures.** Avoid jargon; draw the dose on a card (sun for morning, moon for night). About one adult in four cannot read, so pictures are essential. Pictures stay in memory longer than words.
3. **Chunk the information.** Break a long plan into small groups, such as 3 or 4 items. Short-term memory is small. Chunks fit in it.
4. **Link new to old.** Tie the tablet time to a daily habit (after morning tea). Linking creates retrieval cues. Habits carry the memory.
5. **Teach in the right setting.** Choose a quiet place, not during severe pain or anxiety. Stress blocks encoding. Wait until the patient is comfortable.
6. **Use teach-back and return demonstration.** Ask, "Please show me how you will give the medicine." Correct at once. This tests memory and makes it stronger.
7. **Repeat and review.** Repeat within 24 hours, at discharge and at the first follow-up. Spaced review slows forgetting (Ebbinghaus curve, Figure 3.5). Give a written or picture card to take home.
8. **Involve the family and use mnemonics.** The caregiver is a second memory. Mnemonics help the nurse as well as the patient (for example, "RICE" for sprains). Shared memory means fewer missed doses.

```photogrid label="3.3" cols="3" ratio="1.0" caption="Tools of the behavioural laboratory. (a) A preserved dog from the Pavlov museum, with the salivary fistula still visible at the cheek (the tube tip hangs at the jaw). (b) A modern operant chamber of the Skinner type, with a floor grid, levers and feeder behind the door. (c) Kohs blocks, red-and-white cubes used in Wechsler performance tests to copy the pattern on the card. Wikimedia Commons (CC BY-SA)."
@ photo id="nur10/pdog" cap="Pavlov's dog"
fit 1.0
focus 0.6 0.5
mark 0.50 0.62 "1"
key 1 (a) Preserved dog: fistula tube at the cheek measured saliva drops
@ photo id="nur10/skinner" cap="Operant chamber"
fit 1.0
focus 0.5 0.5
mark 0.48 0.35 "2"
key 2 (b) Chamber floor and levers where animals learn by consequences
@ photo id="nur10/kohs" cap="Kohs blocks"
fit 1.0
focus 0.5 0.5
mark 0.62 0.72 "3"
mark 0.82 0.28 "4"
key 3 (c) Blocks in a box: faces are red, white or half and half
key 4 (c) Pattern card the child must copy with four blocks
```

## 3.4 Motivation and emotion

**Motivation** is the inner state that starts, directs and keeps up behaviour towards a goal. The **motivational cycle**: **need** (a lack) creates a **drive** (tension), which pushes **behaviour** towards an **incentive**; reaching it gives a **reward** and reduces the drive. Motives are **physiological** (hunger, thirst, sleep, sex, pain avoidance) and **psychological or social** (affiliation, achievement, power, curiosity). Theories: **instinct** (McDougall), **drive-reduction** (Hull), **arousal** (Yerkes-Dodson: moderate arousal gives best performance), **incentive** and **Maslow's hierarchy** (Figure 3.4). **Conflict of motives**: approach-approach, avoidance-avoidance, approach-avoidance (a patient who wants surgery but fears it).

```svgfig label="3.4" caption="Maslow's hierarchy of needs with a Nepali nursing example at each level. Lower needs must be mostly met before higher ones become strong. A hungry, cold, frightened patient will not listen to health education; first meet the base of the pyramid."
f = Fig(760, 310)
levels = [("SELF-ACTUALISATION: grow, use skills", "Nurse upgrades to BSc, teaches others", "#ede9fe", "#6d28d9", 150, 40),
          ("ESTEEM: respect, achievement", "Called by name, praised, given a role", BLUE, NAVY, 210, 40),
          ("LOVE AND BELONGING: family, friends", "Family at bedside, mothers' group", MINT, TEAL, 270, 40),
          ("SAFETY: security, health, shelter", "Safe ward, no violence, bed rails", SAND, AMBER, 330, 40),
          ("PHYSIOLOGICAL: air, food, water, sleep", "Oxygen, ORS, warm blanket, rest", ROSE, RED, 390, 40)]
w0 = 130
for i, (a, b, fl, st, wd, hh) in enumerate(levels):
    x = 10 + (390 - wd) / 2 + 0
    y = 10 + i * 58
    f.box(x, y, wd + 10 + i * 0, 50, a.split(":")[0], fill=fl, stroke=st, size=10.5, bold=True)
    f.box(430, y, 320, 50, b, fill=SOFT, stroke=st, size=10.5)
    f.arrow([(x + wd + 10, y + 25), (430, y + 25)], color=st, sw=1.4, dash=True)
f.text(380, 302, "Meet the base first, then climb", size=10.5, color=NAVY, bold=True)
```

**Emotion** is a state of arousal with a feeling, a bodily change and an expression. **James-Lange:** the body reacts first, and the feeling comes from that (I tremble, so I am afraid). **Cannon-Bard:** the thalamus sends signals at the same moment to the cortex (feeling) and the body. **Schachter-Singer** (two-factor): arousal plus the thought we give to it. **Emotional intelligence** (Goleman) has five parts: self-awareness, self-regulation, motivation, empathy and social skills; it predicts good nursing, teamwork and calm in emergencies.

## 3.5 Intelligence

**Intelligence** is the capacity to learn from experience, reason, solve problems and adapt to the environment (Wechsler: to act purposefully, think rationally and deal effectively with the environment). Theories: **Spearman** (a general factor *g* plus specific factors), **Thurstone** (seven primary abilities), **Gardner** (multiple intelligences: linguistic, logical, spatial, musical, bodily, interpersonal, intrapersonal, naturalist), **Sternberg** (triarchic). **Binet and Simon** made the first test in 1905; **Stanford-Binet** and the **Wechsler scales** (WAIS for adults, WISC for children) are used today; the Kohs blocks (Plate 3.3) test performance skills. Tests may be **verbal or performance**, **individual or group**.

**Ratio IQ** (Stern) = mental age / chronological age x 100. **Deviation IQ** (Wechsler) = 100 + 15 x z, where z = (score - mean) / SD. IQ is normally distributed with mean 100 and SD 15, so 68% of people lie between 85 and 115 and 95% between 70 and 130 (Figure 3.5).

```python
import math
def phi(z):                                   # normal cumulative probability
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))
ma, ca = 60, 96                                # mental and chronological age in months
ratio_iq = ma / ca * 100
z = (ratio_iq - 100) / 15
print(f"Ratio IQ = {ratio_iq:.1f}; z = {z:.1f}; percentile = {phi(z) * 100:.2f}%")
print(f"IQ 70: {phi(-2) * 100:.2f}% below; IQ 130: {phi(2) * 100:.2f}% below")
print(f"Share between IQ 85 and 115 = {(phi(1) - phi(-1)) * 100:.2f}%")
```

```text
Ratio IQ = 62.5; z = -2.5; percentile = 0.62%
IQ 70: 2.28% below; IQ 130: 97.72% below
Share between IQ 85 and 115 = 68.27%
```

An IQ of 62.5 (z = -2.5) lies at the **0.62th percentile**, meaning that only about 6 in 1,000 children score lower; IQ 70 is the **2.28%** point, IQ 130 the **97.72%** point and **68.27%** of people fall between 85 and 115.

```svgfig label="3.5" caption="Left: the Ebbinghaus forgetting curve (retention = e to the power minus t over S) for S = 2 days (steep fall) and after a review that doubles S to 4 days (slower fall). Right: the normal curve of IQ with mean 100 and SD 15; 68% lie within 1 SD, 95% within 2 SD; below 70 is the zone of intellectual disability."
import math
f = Fig(760, 280)
ox, oy, W, H = 50, 230, 300, 180
f.line(ox, oy, ox + W, oy, color=SLATE, sw=1.5); f.line(ox, oy, ox, oy - H, color=SLATE, sw=1.5)
def curve(S, col):
    pts = [(ox + W * t / 7, oy - H * math.exp(-t / S)) for t in [i / 10 for i in range(0, 71)]]
    for i in range(len(pts) - 1):
        f.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], color=col, sw=2.4)
curve(2.0, RED); curve(4.0, TEAL)
f.text(ox + W / 2, oy + 28, "Days after teaching (0 to 7)", size=10.5)
f.text(ox + 8, oy - H - 8, "Retention (100%)", size=10.5, anchor="start")
f.text(ox + 150, oy - 50, "S = 2 days: 3% at day 7", size=10, color=RED, bold=True, anchor="start")
f.text(ox + 120, oy - 120, "Review: S = 4, 17% at day 7", size=10, color=TEAL, bold=True, anchor="start")
cx, cy, cw, ch = 420, 230, 320, 170
f.line(cx, cy, cx + cw, cy, color=SLATE, sw=1.5)
def g(z): return math.exp(-z * z / 2)
pts = [(cx + cw * (z + 3.5) / 7, cy - ch * g(z)) for z in [i / 20 - 3.5 for i in range(0, 141)]]
for i in range(len(pts) - 1):
    f.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], color=NAVY, sw=2.4)
for z, lab in [(-2, "70"), (-1, "85"), (0, "100"), (1, "115"), (2, "130")]:
    x = cx + cw * (z + 3.5) / 7
    f.line(x, cy, x, cy - ch * g(z), color=SLATE, sw=1.0, dash=True)
    f.text(x, cy + 16, lab, size=10.5, bold=True)
f.text(cx + cw / 2, oy - H - 8, "IQ (mean 100, SD 15)", size=10.5)
f.text(cx + cw / 2, cy - ch * 0.35, "68%", size=12, color=NAVY, bold=True)
f.text(cx + cw * 0.12, cy - 22, "2.3%", size=10, color=RED, bold=True)
f.text(cx + cw * 0.88, cy - 22, "2.3%", size=10, color=RED, bold=True)
```

**Intellectual disability (ICD-10 bands):** **mild** IQ 50-69 (about 85% of cases; can learn reading, simple work and live with support), **moderate** 35-49, **severe** 20-34, **profound** below 20; diagnosis needs **both** low IQ (below 70) **and** poor adaptive behaviour from childhood. Causes: genetic (Down syndrome, fragile X), iodine deficiency (cretinism; iodised salt in Nepal prevents this), birth asphyxia, infections (meningitis), lead and malnutrition. A **mentally gifted** child has IQ 130 or more. Nepal's Act Relating to Rights of Persons with Disabilities 2074 lists intellectual disability among the disabilities that are entitled to an identity card and services.

## 3.6 Personality

**Personality** is the stable pattern of thoughts, feelings and behaviour that makes each person unique (Allport: the dynamic organisation within the individual of the psychophysical systems that determine his unique adjustments). **Determinants:** **heredity** (temperament, genes), **environment** (family, culture, school, caste and society) and **situation**. **Approaches:**

- **Psychodynamic (Freud).** The mind has **id** (pleasure principle, instinct), **ego** (reality principle, mediator) and **superego** (conscience). Levels: conscious, preconscious, unconscious. **Psychosexual stages:** oral (0-1 y), anal (1-3 y), phallic (3-6 y), latency (6-12 y), genital (12 y on). **Erikson** extended to eight psychosocial crises from trust vs mistrust (infancy) to integrity vs despair (old age). Defence mechanisms (repression, denial, projection, displacement, regression, sublimation) protect the ego from anxiety.
- **Trait approach.** **Allport** (cardinal, central, secondary traits), **Cattell** (16 PF), **Eysenck** (introversion-extraversion, neuroticism, psychoticism) and the **Big Five (OCEAN)**: openness, conscientiousness, extraversion, agreeableness, neuroticism.
- **Humanistic (Rogers).** The **self-concept** and the gap between real and ideal self; healthy growth needs unconditional positive regard.
- **Assessment:** **inventories** (MMPI, 16 PF), **projective tests** (Rorschach inkblot, Thematic Apperception Test), interviews and observation.

## Formula and fact sheet

- Psychology: scientific study of behaviour and mental processes; first laboratory Wundt, Leipzig 1879. Goals: describe, explain, predict, control.
- Classical conditioning: NS + US -> CS gives CR (Pavlov); operant: reinforcement increases, punishment decreases behaviour (Skinner); social learning: observation of models (Bandura).
- Forgetting: R = e^(-t/S); reviews increase S. Reinforcement schedules: FR, VR, FI, VI.
- Ratio IQ = MA / CA x 100; deviation IQ = 100 + 15z. ICD-10: mild 50-69, moderate 35-49, severe 20-34, profound under 20.
- Maslow: physiological, safety, love and belonging, esteem, self-actualisation. Big Five = OCEAN.

## Chapter summary

- Psychology studies behaviour and mind using experiment, observation, survey, case study and tests.
- Learning happens by association (classical), by consequences (operant) and by watching others (social); nurses apply these to fear, habits and teaching.
- Memory fades along an exponential curve unless reviewed; motivation follows Maslow's needs; intelligence is normally distributed and mild disability is the most common form.
- Personality results from heredity, environment and situation and is explained by psychodynamic, trait and humanistic theories.

## Practice

```python
import math
def phi(z): return 0.5 * (1 + math.erf(z / math.sqrt(2)))
m2 = 50 // 10                                   # MCQ2: FR-10 and 50 responses
m3 = round(10 / 12 * 100, 1)                    # MCQ3: MA 10 y, CA 12 y
m4 = round(100 + 15 * -2.5, 1)                  # MCQ4: z = -2.5 as deviation IQ
print(f"MCQ2 = {m2}; MCQ3 = {m3}; MCQ4 = {m4}")
print(f"Case: ratio IQ {60 / 96 * 100:.1f}, percentile {phi(-2.5) * 100:.2f}%, mild range 50-69: {50 <= 60 / 96 * 100 <= 69}")
```

```text
MCQ2 = 5; MCQ3 = 83.3; MCQ4 = 62.5
Case: ratio IQ 62.5, percentile 0.62%, mild range 50-69: True
```

**MCQs (with reasons)**

1. The first psychology laboratory was set up in 1879 by: (a) Freud (b) Wundt (c) Pavlov (d) Skinner.
2. On a fixed-ratio 10 schedule, 50 responses give how many reinforcers? (a) 2 (b) 5 (c) 10 (d) 50.
3. A child with mental age 10 years and chronological age 12 years has a ratio IQ of about: (a) 83 (b) 100 (c) 120 (d) 60.
4. A Wechsler score with z = -2.5 gives a deviation IQ of: (a) 62.5 (b) 77.5 (c) 85 (d) 100.
5. A child who fears the white coat after painful injections shows: (a) operant punishment (b) classical conditioning (c) social learning (d) insight.

::: note Answers and rationales
**1. (b).** Wilhelm Wundt opened the Leipzig laboratory in 1879. Freud founded psychoanalysis, Pavlov studied conditioned reflexes and Skinner studied operant behaviour.
**2. (b).** Every 10th response is reinforced, so 50 / 10 = 5. Reinforcers are not given for each response, so 50 is wrong.
**3. (a).** Ratio IQ = 10 / 12 x 100 = 83.3. 100 would need equal ages, and 120 would mean the mental age is above the chronological age.
**4. (a).** Deviation IQ = 100 + 15 x (-2.5) = 62.5. 77.5 would be z = -1.5, and 85 would be z = -1.
**5. (b).** The white coat (neutral) was paired with the painful needle (unconditioned), so the coat alone now causes fear. Operant learning depends on consequences of behaviour, not on pairing of stimuli.
:::

**Short answer (3 marks): Define classical conditioning with a nursing example.** Classical conditioning is learning by association: a neutral stimulus paired repeatedly with an unconditioned stimulus comes to cause a conditioned response (Pavlov). In nursing, a child who has had painful injections fears the white coat. Systematic desensitisation and a friendly approach can extinguish the response.

**Medium answer (5 marks): Describe Maslow's hierarchy of needs and its use in nursing.** Maslow (1943) arranged human needs in five levels (Figure 3.4): physiological (air, food, water, sleep), safety, love and belonging, esteem and self-actualisation. Lower needs must be mostly met before higher needs motivate. The nurse therefore gives oxygen, fluids, pain relief and warmth first; then a safe bed and protection; then family contact and belonging; then respect, privacy and praise; and finally teaches and supports growth, such as self-care in diabetes. Needs are met in different order by different people, and in illness a person falls down the pyramid. The hierarchy guides priority setting and the nursing process: assess the unmet need, plan and evaluate.

**Long answer (10 marks): Rajan Tamang, 8 years, is brought by his mother to the health post. His teacher says he cannot read or keep up in class. Mental age on a psychological assessment is 5 years (60 months) and chronological age is 8 years (96 months). He dresses and feeds himself, but cannot manage money or road safety. Calculate his IQ, interpret and write the nursing care plan.**

*Calculation.* Ratio IQ = 60 / 96 x 100 = **62.5**; z = (62.5 - 100) / 15 = **-2.5**, the **0.62th percentile**. An IQ of 50-69 with reduced adaptive skills means **mild intellectual disability** (ICD-10), which needs a full medical and developmental assessment to find a cause (iodine deficiency, hearing loss, thyroid, anaemia, epilepsy) and to exclude other problems, since one test is not diagnosis.

*Psychology applied.* Use **operant** learning (shaping with praise and tokens), **social learning** (a peer model), small steps and **repetition with review** (Ebbinghaus). Meet **Maslow's** base first (nutrition, safety), then belonging and esteem (inclusion in class and games). Family teaching reduces blame and stigma, and the mother can apply for the disability identity card under the 2074 Act.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **O:** IQ 62.5, cannot read, class level behind. | **Impaired verbal communication / delayed growth and development** related to intellectual disability. | **Child development: middle childhood:** learns 10 sight words and own name in 3 months. | Break tasks into small steps and repeat daily (limited short-term memory); use pictures and demonstration (concrete thinking); praise at once (reinforcement); coordinate with the teacher for an individual plan. | Reads own name and 10 words. |
| **O:** cannot handle money, road safety. | **Self-care deficit (instrumental) / risk for injury** related to cognitive limits. | **Safety behaviour:** crosses road with a rule and holds the adult's hand; names coins. | Teach one skill at a time with role play (modelling); use a picture rule for crossing; practice with the family (generalisation); supervise outside. | Safe crossing in 4 of 5 trials. |
| **S:** Mother: "He is a curse; neighbours laugh." | **Caregiver role strain / ineffective family coping** related to stigma and lack of knowledge. | **Caregiver emotional health:** states cause, strengths and a support plan. | Explain that disability is not a curse and iodised salt and early care help (corrects belief); link with a parent group and disability organisation (peer support); help to get the disability card (benefits). | Mother attends group; speaks hopefully. |
| **O:** teacher reports teasing and isolation. | **Situational low self-esteem** related to peer rejection. | **Self-esteem:** joins a group activity and names two things he does well. | Give tasks he can do and praise them (success experience); teach classmates (reduces stigma); use tokens for cooperative play (operant). | Takes part in games. |
| **O:** no cause investigated; Hb and hearing not tested. | **Ineffective health management** related to lack of assessment. | **Health status:** referral done; Hb, TSH and hearing checked within 1 month. | Refer to district hospital/paediatrician for medical work-up (find treatable causes); give iron if anaemic; confirm iodised salt in the home; schedule review (continuity). | Tests done; plan updated. |
