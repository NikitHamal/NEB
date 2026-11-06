---
subject: Nursing Concepts
grade: BSc Nursing Year 2
unit: 5
title: Holistic Nursing, Complementary Therapies, Ayurveda and Creativity in Nursing
hours: 16
area: BSN 15 · Nursing Concepts · Units 6 and 8
---

Mrs Laxmi Shrestha, 40, a schoolteacher in Bhaktapur, has had headaches for six months. Scans are normal. She sleeps badly, worries about her son abroad and her mother-in-law's illness, and her shoulders are tight. Medicine alone gives only partial relief. Her family also takes her to an *Ayurveda* clinic for oil massage, and she wants to know whether it is safe to combine it with the tablets. A **holistic** nurse sees a whole person, in a family and a culture, and knows which complementary methods help, which are unproven and which are harmful. This unit covers Unit 6 (Holistic Approaches, 8 h) and Unit 8 (Creativity, 8 h) of BSN 15.

::: key What this unit gives you
- Real images: **acupuncture needles**, a **Reiki** session and an **Ayurveda Panchakarma** treatment room; with SVG figures on the holistic person and the four stages of creative problem solving.
- **Holistic health and holistic nursing**; **therapeutic touch, Reiki, acupuncture and acupressure, biofeedback, relaxation, meditation and yoga**; **Ayurveda** (tridosha, panchakarma, Nepal's Ayurveda services).
- **Creativity**: definition, personality traits, Wallas's four stages, and methods of being creative in nursing, with the WHO low-cost hand-rub formula worked in millilitres.
- Slow-breathing and stress-score mathematics; eight points each on safe use of complementary therapies and on creative methods; model answers and a 5-column NANDA-I plan for stress and tension headache.
:::

## 5.1 Holistic health and holistic nursing

**Holism** means that a person is more than the sum of body parts: **body, mind, emotions, social life and spirit** act together and with the **environment** (Figure 5.1). **Holistic health** is a state of balance among these dimensions, and **holistic nursing** (American Holistic Nurses Association) is *all nursing practice that has healing the whole person as its goal*. Its five core values are **holistic philosophy and education, holistic ethics, theory and research, holistic nursing practice, and holistic communication, environment and cultural diversity**, with **self-care of the nurse** itself. The nurse assesses all dimensions, values the person's beliefs, uses the **therapeutic use of self** and chooses safe, evidence-based care, conventional and complementary.

```svgfig label="5.1" caption="The holistic person. Body, mind, emotions, social relationships and spirit are connected, and all lie within the family, culture and environment. A change in one dimension affects the others, for example grief (emotion) causes poor sleep (body) and withdrawal (social). Holistic assessment asks about all five."
f = Fig(760, 300)
f.circle(380, 150, 125, fill="#ecfdf5", stroke=TEAL, sw=2)
f.text(380, 40, "FAMILY, CULTURE, ENVIRONMENT", size=10.5, color=TEAL, bold=True)
f.circle(380, 150, 36, fill="#fde68a", stroke=AMBER, label="PERSON", size=11, color=NAVY)
f.box(300, 70, 160, 34, "BODY: pain, sleep, food", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(180, 125, 140, 34, "MIND: thoughts", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(440, 125, 150, 34, "EMOTION: fear, hope", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(200, 205, 150, 34, "SOCIAL: family, work", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(410, 205, 170, 34, "SPIRIT: meaning, faith", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.text(650, 150, "All five are", size=11, color=NAVY, bold=True)
f.text(650, 168, "assessed and", size=11, color=NAVY, bold=True)
f.text(650, 186, "cared for", size=11, color=NAVY, bold=True)
```

## 5.2 Holistic practices used by nurses

**Therapeutic touch (TT).** Developed by Dolores Krieger (a nurse) and Dora Kunz in the 1970s, TT is done with the hands held a few centimetres above the body. Five steps: **centring** (the nurse calms herself), **assessment** (hands scan for differences), **unruffling** (smoothing the field), **treatment** (directing calm) and **evaluation**. It lowers anxiety, but the evidence for an "energy field" is weak. **Reiki** (Mikao Usui, Japan, 1922) uses light hand positions on or above the body for 20-30 minutes to promote relaxation; trials show comfort and less anxiety but no proof of cure. **Acupuncture** (traditional Chinese medicine) uses fine sterile needles at points along **meridians** to influence **qi**; it has evidence for chronic pain, nausea and migraine, for instance the **PC6 (Neiguan) point** two finger-widths above the wrist crease for nausea. **Acupressure** uses finger pressure (1-3 minutes per point) without needles and is safe for family teaching. **Biofeedback** uses sensors that show muscle tension (EMG), skin temperature, heart rate or breathing, so that the person learns to change them; it helps tension headache, migraine and hypertension. **Relaxation** includes **Jacobson's progressive muscle relaxation** (tense and release each muscle group), **guided imagery** and **slow breathing**; **meditation** trains attention (for example breath awareness or mantra); **yoga** (Patanjali's eight limbs) joins postures (*asana*), breath control (*pranayama*) and meditation (*dhyana*), and has evidence for back pain, anxiety and blood pressure.

```python
rr_normal, rr_slow = 18, 6                       # breaths per minute, usual and slow yogic breathing
per_hour_normal = rr_normal * 60
per_hour_slow = rr_slow * 60
drop = (rr_normal - rr_slow) / rr_normal * 100
inhale_s, exhale_s = 4, 6
cycle_s = inhale_s + exhale_s
print(f"Breaths per hour: {per_hour_normal} usual vs {per_hour_slow} slow; fewer by {drop:.1f}%")
print(f"A 4 s in + 6 s out cycle = {cycle_s} s = {60 // cycle_s} breaths a minute")
```

```text
Breaths per hour: 1080 usual vs 360 slow; fewer by 66.7%
A 4 s in + 6 s out cycle = 10 s = 6 breaths a minute
```

Slow breathing at **6 breaths per minute** instead of 18 means **360 breaths an hour instead of 1080**, which is **66.7% fewer**. A cycle of 4 seconds in and 6 seconds out gives exactly **6 breaths a minute**. Slow breathing raises vagal tone, lowers heart rate and BP, and calms the mind.

```photogrid label="5.2" cols="3" ratio="1.0" caption="Complementary methods in real images. (a) Acupuncture needles beside a one-cent coin for scale: very fine, sterile, single-use. (b) A Reiki session: the practitioner's hands rest lightly on the abdomen of a clothed, relaxed client. (c) An Ayurveda treatment room set up for Panchakarma/oil therapy, with a wooden table and an overhead vessel for dripping warm oil."
@ photo id="nur9/acu" cap="Acupuncture needles"
fit 1.0
focus 0.5 0.45
mark 0.30 0.78 "1"
mark 0.28 0.35 "2"
key 1 (a) One-cent coin: shows how fine the needles are
key 2 (a) Needle shaft and handle: single-use, sterile
@ photo id="nur9/reiki" cap="Reiki session"
fit 1.0
focus 0.5 0.5
mark 0.45 0.60 "3"
mark 0.70 0.30 "4"
key 3 (b) Practitioner's hands on the client's abdomen
key 4 (b) Client lies clothed and relaxed on a couch
@ photo id="nur9/panch" cap="Ayurveda treatment room"
fit 1.0
focus 0.5 0.5
mark 0.45 0.60 "5"
mark 0.60 0.25 "6"
key 5 (c) Frame and vessel above the table: warm oil is dripped in treatment
key 6 (c) Wooden treatment table (droni)
```

## 5.3 Ayurveda and its use in Nepal

**Ayurveda** (*ayus* = life, *veda* = knowledge) is a traditional Indian system, in Nepal the oldest and most popular traditional medicine. Its base is the **five great elements** (*panchamahabhuta*: earth, water, fire, air, space) which combine as the three **doshas**: **vata** (air and space: movement, nerves), **pitta** (fire and water: digestion, metabolism) and **kapha** (water and earth: structure, lubrication). Health is balance of the doshas, the seven **dhatus** (tissues: rasa, rakta, mamsa, meda, asthi, majja, shukra), three **malas** (wastes), good digestion (*agni*) and a happy mind. Treatment includes diet, daily and seasonal routines (*dinacharya*, *ritucharya*), herbs, massage, yoga and **Panchakarma** (five cleansing procedures: *vamana*, *virechana*, *basti*, *nasya*, *raktamokshana*). Common Nepali herbs include **turmeric (*besar*), tulsi, ginger, neem, timur, ashwagandha and triphala**. The Government of Nepal runs Ayurveda services through the **Department of Ayurveda and Alternative Medicine (DoAAM)**: as reported for FY 2080/81, **6 public Ayurveda hospitals, 77 district Ayurveda health centres and 305 Ayurveda dispensaries (*aushadhalaya*)**, and the National Ayurveda Health Policy dates from 1996.

**Eight nursing responsibilities with complementary and Ayurvedic therapies.**

1. **Ask every patient.** Many do not volunteer that they use herbs or healers. Ask without judgement: "Are you taking any other medicine, herb or treatment?" Record the answers. This shows hidden interactions.
2. **Respect culture and belief.** Treat the patient's beliefs as part of the person. Do not laugh or scold. Trust makes honest sharing possible.
3. **Know the evidence.** Support methods with good evidence (slow breathing, acupressure at PC6, yoga for back pain, relaxation). Be honest about methods with weak evidence (therapeutic touch, Reiki). Never tell a patient that they cure cancer or diabetes.
4. **Check for harm and interaction.** Some herbs interact with drugs: for example, turmeric and ginger in high doses with anticoagulants, ashwagandha with thyroid drugs and sedatives, and some preparations have contained heavy metals. Report to the doctor and pharmacist. Advise caution in pregnancy and children.
5. **Never replace life-saving treatment.** A child with diarrhoea needs ORS and zinc, a diabetic needs insulin and a TB patient needs DOTS. Complementary care is added to, not in place of, proven treatment. Delay in seeking care can kill.
6. **Practise within competence and law.** Do only what you are trained and permitted to do, follow hospital policy, and use only registered, licensed products and practitioners. Needles must be sterile and single-use. Record consent.
7. **Teach safe self-care.** Teach slow breathing, relaxation, simple yoga and acupressure that families can do at home. Provide written steps. Check the person's understanding.
8. **Evaluate and document.** Record the method, time, response and any adverse effect, and reassess outcomes such as pain, anxiety and sleep. Share findings with the team. Review and stop if there is harm.

## 5.4 Creativity in nursing

**Creativity** is the ability to produce new, useful ideas or solutions. In nursing it means finding a better way to meet a patient's need with the resources available. **Personality characteristics** linked to creativity: **curiosity, flexibility, fluency (many ideas), originality, independence, tolerance of ambiguity, willingness to take risks, persistence, a sense of humour and open-mindedness**. **Graham Wallas (1926)** described **four stages of creative problem solving** (Figure 5.2): **preparation** (define the problem, collect facts), **incubation** (step back; the mind works unconsciously), **illumination** (the idea appears) and **verification** (test, refine and implement).

```svgfig label="5.2" caption="The four stages of creative problem solving (Wallas) with a nursing example. The nurse notices that a ward runs out of alcohol hand-rub. Preparation: count the usage and the cost. Incubation: leave the problem and talk with colleagues. Illumination: she remembers the WHO local formula. Verification: the pharmacy prepares a small batch, tests it and the ward trial shows compliance rises."
f = Fig(760, 230)
f.box(10, 30, 170, 80, "1 PREPARATION\ndefine the problem,\ncollect facts", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(200, 30, 170, 80, "2 INCUBATION\nstep back, talk,\nlet ideas settle", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(390, 30, 170, 80, "3 ILLUMINATION\nthe new idea\nappears", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(580, 30, 170, 80, "4 VERIFICATION\ntest, refine,\nimplement", fill=ROSE, stroke=RED, color=RED, size=10.5, bold=True)
f.arrow([(180, 70), (200, 70)], sw=2); f.arrow([(370, 70), (390, 70)], sw=2); f.arrow([(560, 70), (580, 70)], sw=2)
f.box(10, 140, 740, 70, "Example: no alcohol hand-rub on the ward -> count use and cost -> discuss with pharmacist -> WHO formula I -> make 10 L, test, audit hand-hygiene compliance", fill=BLUE, stroke=NAVY, size=10.5)
```

**Eight methods of being creative in nursing.**

1. **Ask "why" and "what if".** Question routines kindly. Many good ideas start with "why do we always do it this way?" Write down your questions.
2. **Brainstorm with the team.** Collect as many ideas as possible without criticism, then choose. Quantity gives quality. Include the patient and the FCHV.
3. **Use SCAMPER.** Ask: Substitute, Combine, Adapt, Modify, Put to another use, Eliminate, Reverse. A bamboo stick can become a drip stand; a picture chart can replace a long talk.
4. **Learn from other fields and places.** Visit another ward, read, watch, ask the community. Ideas from outside break habits. Share what you learn.
5. **Use low-cost local materials.** Use clean cloth for slings, local foods for diet charts, mobile phone voice messages for reminders, and songs or street drama for health education. Cost is a barrier, not a stop.
6. **Draw, map and role-play.** Flow charts, posters, models and role play show a problem from a new side. Children and patients with low literacy learn from pictures.
7. **Make time and safe space.** Creativity needs rest, support and permission to fail. Leaders should welcome ideas. Record and thank good suggestions.
8. **Test, measure and share.** Try a small pilot, collect numbers, adjust and then spread it with a short report. A tested idea convinces the manager. Evidence turns creativity into policy.

**A real low-cost example: the WHO local hand-rub formula I.** For each **1,000 mL** of final product: ethanol 96% **833.3 mL**, hydrogen peroxide 3% **41.7 mL**, glycerol 98% **14.5 mL**, then sterile or boiled-and-cooled water to the 1,000 mL mark. The result is about 80% ethanol, 1.45% glycerol and 0.125% hydrogen peroxide. Mix in the alcohol and glycerol first, add peroxide last, never in a naked-flame area.

```python
batch_ml = 10_000                                   # a 10-litre batch
ethanol = 833.3 * batch_ml / 1000
peroxide = 41.7 * batch_ml / 1000
glycerol = 14.5 * batch_ml / 1000
water = batch_ml - round(ethanol) - round(peroxide) - round(glycerol)
final_ethanol = ethanol * 0.96 / batch_ml * 100
print(f"Ethanol 96% = {ethanol:.0f} mL; hydrogen peroxide 3% = {peroxide:.0f} mL; glycerol 98% = {glycerol:.0f} mL; water to make up = {water:.0f} mL")
print(f"Final ethanol = {final_ethanol:.1f}% v/v")
```

```text
Ethanol 96% = 8333 mL; hydrogen peroxide 3% = 417 mL; glycerol 98% = 145 mL; water to make up = 1105 mL
Final ethanol = 80.0% v/v
```

For a 10-litre batch the nurse and pharmacist measure **8333 mL** of 96% ethanol, **417 mL** of 3% hydrogen peroxide and **145 mL** of 98% glycerol, then add water (**1105 mL**) to the 10-litre mark; the final strength is **80.0% ethanol**.

## Formula and fact sheet

- Holistic: body, mind, emotion, social, spirit, environment; TT has 5 steps; Reiki (Usui 1922); acupuncture PC6 for nausea; PMR (Jacobson), yoga (asana, pranayama, dhyana).
- Ayurveda: 5 elements, 3 doshas (vata, pitta, kapha), 7 dhatus, 3 malas, 5 panchakarma; Nepal: 6 hospitals, 77 district centres, 305 dispensaries (FY 2080/81).
- Wallas: preparation, incubation, illumination, verification. WHO hand-rub per litre: ethanol 96% 833.3 mL, H2O2 3% 41.7 mL, glycerol 98% 14.5 mL, water to 1,000 mL.
- PSS-10 (0-40): 0-13 low, 14-26 moderate, 27-40 high stress.

## Chapter summary

- Holistic nursing treats the whole person within family and culture and uses complementary methods safely beside proven treatment.
- Relaxation, slow breathing, acupressure and yoga have good evidence; therapeutic touch and Reiki are comforting but unproven; herbs may interact with drugs.
- Ayurveda is the main traditional system in Nepal; nurses ask about its use, respect belief and watch for harm.
- Creativity follows preparation, incubation, illumination and verification and can be learned; the WHO hand-rub formula is a model of low-cost creative problem solving.

## Practice

```python
m1 = 6 * 60                                      # MCQ1 breaths per hour at 6/min
m2 = round(833.3 * 5)                            # MCQ2 mL of ethanol 96% for 5 L (833.3 per litre)
pss = [3, 4, 3, 2, 3, 3, 2, 3, 2, 3]             # Mrs Laxmi Shrestha PSS-10 items after reverse scoring
c_pss = sum(pss)
c_band = "low" if c_pss <= 13 else "moderate" if c_pss <= 26 else "high"
c_slow = (18 - 6) / 18 * 100
c_sess = 3 * 20                                  # three 20-minute relaxation sessions a day
print(f"MCQ1 = {m1}; MCQ2 = {m2} mL")
print(f"Mrs Shrestha: PSS-10 = {c_pss} ({c_band}); slow breathing cuts the rate by {c_slow:.1f}%; practice time = {c_sess} min a day")
```

```text
MCQ1 = 360; MCQ2 = 4166 mL
Mrs Shrestha: PSS-10 = 28 (high); slow breathing cuts the rate by 66.7%; practice time = 60 min a day
```

**MCQs (with reasons)**

1. A person breathing 6 times a minute takes how many breaths in one hour? (a) 180 (b) 360 (c) 720 (d) 1,080.
2. Which method has the best evidence for post-operative nausea? (a) acupressure at PC6 (b) Reiki (c) therapeutic touch (d) none.
3. In Wallas's model the stage in which the idea appears is: (a) preparation (b) incubation (c) illumination (d) verification.
4. A patient on warfarin takes high-dose turmeric and ginger capsules. The nurse should: (a) say nothing (b) tell the patient to stop immediately without telling the doctor (c) report to the doctor and pharmacist (d) double the warfarin.
5. In Ayurveda the dosha linked to digestion and metabolism is: (a) vata (b) pitta (c) kapha (d) agni.

::: note Answers and rationales
**1. (c).** 6 × 60 = 360; the options of 180 and 720 are 3 and 12 breaths a minute; 1,080 is 18 per minute.
**2. (a).** Stimulating PC6 reduces nausea and vomiting in several trials; Reiki and therapeutic touch lack such evidence.
**3. (c).** Illumination is the "aha" moment; preparation is fact finding, incubation is rest, verification is testing.
**4. (c).** The nurse reports a possible interaction that raises bleeding risk; only the doctor changes the drug dose.
**5. (b).** Pitta governs digestion and metabolism; agni is the digestive fire, not a dosha.
:::

**Short answer (3 marks): Define holistic nursing and list four complementary therapies.** Holistic nursing is care that treats the whole person (body, mind, emotions, social life and spirit) within the family and environment. Four therapies are acupuncture or acupressure, relaxation and meditation, yoga and biofeedback; others are therapeutic touch, Reiki and Ayurveda. They are used alongside, not instead of, medical treatment.

**Medium answer (5 marks): Describe the stages of creative problem solving (Figure 5.2).** Wallas (1926) described four stages. **Preparation:** the problem is defined and information is collected. **Incubation:** the person steps back and the mind works on the problem without effort. **Illumination:** a new idea appears suddenly. **Verification:** the idea is tested, refined and put into practice. In nursing, a ward that runs out of hand-rub counts use and cost (preparation), discusses with colleagues (incubation), finds the WHO local formula (illumination) and makes and audits a batch (verification). Creative people show curiosity, flexibility, fluency, originality and persistence.

**Long answer (10 marks): Mrs Laxmi Shrestha, 40 years, a teacher from Bhaktapur, has had tension-type headache for 6 months, sleeps 4 hours, and worries about her son abroad. Her PSS-10 score is 28, her neck muscles are tight and she uses oil massage from an Ayurvedic clinic and ibuprofen. Calculate the relaxation plan and write the nursing care plan.**

*Calculations.* The PSS-10 items add to **28** (high stress band is 27 or more). Slow breathing from 18 to 6 per minute cuts the rate by **66.7%**. Three 20-minute practice sessions make **60 minutes a day**.

*Care.* The nurse takes a holistic history of body (sleep, pain, food, ibuprofen use), mind (worry), emotion (fear), social (son abroad, mother-in-law) and spiritual needs (prayer). She asks about the Ayurvedic oil and tablets and checks for herbal-drug interactions and for ibuprofen overuse (stomach, kidney), refers to the doctor to exclude red-flag headache, and respects the family's wish to continue oil massage if the oils are safe and not applied to broken skin. She teaches **slow breathing 4 in, 6 out** (6 breaths a minute), progressive muscle relaxation, neck stretches, gentle yoga (with a trained instructor), a fixed bedtime and acupressure on the neck and temples. She encourages talking with a friend or counsellor, a daily walk and breaks from screens. She records baseline and follows up at 2 weeks for headache days, sleep and PSS-10.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "My head hurts every day." **O:** tight neck, PSS-10 28. | **Chronic pain** related to muscle tension and stress, as evidenced by daily headache. | **Pain control:** headaches fewer than 2 days a week in 4 weeks. | Teach slow breathing 6 per minute, 3 times a day (calms the nervous system); progressive muscle relaxation (loosens muscles); warm pack to the neck; limit ibuprofen to prescribed use (protects stomach and kidney). | Fewer than 2 headache days. |
| **S:** "I sleep only 4 hours." **O:** worry at night. | **Insomnia** related to anxiety. | **Sleep:** sleeps 6-7 hours in 3 weeks. | Fixed bedtime and wake time (resets rhythm); no tea or screens after 8 p.m. (reduces arousal); relaxation in bed (lowers tension). | Sleeps 6 h. |
| **S:** "I worry all the time." **O:** PSS-10 28. | **Anxiety** and **ineffective coping** related to family worries. | **Coping:** PSS-10 below 20 in 4 weeks. | Active listening (relieves emotion); teach problem-focused steps and a worry diary; arrange counselling; encourage talking with friends. | PSS-10 falls to 18. |
| **S:** "I use Ayurvedic oil and tablets." **O:** unnamed herbal pills. | **Deficient knowledge** about interaction of herbs and drugs. | **Knowledge:** names every product and states one precaution. | Ask about all products (finds hidden risks); inform the doctor and pharmacist; explain that herbs do not replace treatment; respect belief. | Lists products; follows advice. |
| **O:** no exercise, spends the day indoors. | **Sedentary lifestyle** related to work and low motivation. | **Activity:** walks 30 minutes on 5 days a week. | Set a simple walking plan; link with a yoga class (movement lowers stress); praise progress. | Walks 5 days a week. |
