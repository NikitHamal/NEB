---
subject: Community Health Nursing
grade: BSc Nursing Year 1
unit: 5
title: Environmental Health, WASH, Occupational Health, Health Education and Disaster
hours: 25
area: BSN 6-7 · Community Health Nursing · Unit 5
---

Most of the diseases in Units 3 and 4 begin in the environment: unsafe water, open defecation, smoky kitchens, unsafe workplaces and unprepared communities. The 2015 earthquake, the yearly floods and landslides and the kitchen-smoke deaths of women show how the environment decides health in Nepal. The community nurse is the person who tests the well, teaches the school, inspects the health-care waste and runs the first aid post when disaster strikes.

::: key What this unit gives you
- Real photographs of a village tap in a Nepal WASH project, a woman washing hands at a tap stand and a school handwashing lesson, with labelled marks.
- Water safety, the F-diagram of faecal-oral spread, well chlorination, handwashing and sanitation, with the chlorine dose calculated.
- Household air pollution, occupational hazards and noise, health-care waste colour codes, disaster triage and health education.
- Eight points on the nurse's role in preventing diarrhoeal disease, and model answers with a school health case and care plan.
:::

## 5.1 Safe water, sanitation and hygiene (WASH)

Safe water is free from germs and harmful chemicals, clear, tasteless and has a **free residual chlorine of 0.2-0.5 mg/L** after treatment. Nepal's drinking water standard is checked for coliform bacteria, turbidity, pH, arsenic (Terai) and nitrate. The home treatment options are boiling for one minute, chlorine solution (Piyush, as labelled), SODIS (solar disinfection in clear PET bottles for 6 hours), ceramic or biosand filters, and storage in a clean covered container with a tap. Basic water supply means 20 litres a person a day within 30 minutes; the emergency minimum (Sphere standard) is 15 litres and good practice is 45 litres or more. For 1,000 people this is **45,000 litres a day** (45 L) and **15,000 litres** at the emergency minimum.

Excreta disposal by a sanitary latrine breaks the faecal-oral route. Nepal was declared open-defecation free in 2019, and the aim now is safe, used, clean and maintained toilets. Hand hygiene is the cheapest intervention of all: washing with soap after the toilet and before food cuts diarrhoea by about 30%. Out of 1,000 episodes in a community, a 30% reduction means **700 episodes** and **300 are prevented**.

```photogrid label="5.1" cols="3" ratio="1.0" caption="WASH in a Nepal community. (a) A boy drinks from a tap of a community water scheme (NEWAH, Udayapur). (b) A woman washes her hands at the tap stand of a village scheme in Parbat. (c) A school handwashing lesson: the steps are demonstrated by the teacher while the students watch (Udayapur)."
@ photo id="nur3/tap" cap="Community tap, Udayapur"
fit 1.0
focus 0.4 0.5
mark 0.62 0.72 "1"
mark 0.30 0.35 "2"
key 1 (a) The tap of a gravity-flow scheme: piped water near the home saves hours of carrying
key 2 (a) Cupped hands: safe to drink only if the source is protected and tested
@ photo id="nur3/wash" cap="Hand washing at a tap stand, Parbat"
fit 1.0
focus 0.5 0.45
mark 0.72 0.60 "3"
mark 0.45 0.35 "4"
key 3 (b) Running water from the tap: the best way to rinse off soap and germs
key 4 (b) Hands scrubbed between the fingers and under the nails for 20 seconds
@ photo id="nur3/teach" cap="Handwashing lesson at school"
fit 1.0
focus 0.5 0.5
mark 0.45 0.45 "5"
mark 0.82 0.60 "6"
key 5 (c) The teacher demonstrates the steps on her own hands in front of the class
key 6 (c) Students learn by watching and copying; they teach their families later
```

The classic **F-diagram** shows the five routes by which faeces reach the mouth: **f**ingers, **f**lies, **f**luids (water), **f**ields (soil, crops) and **f**ood. Two barriers, sanitation (stops faeces entering the environment) and hygiene with safe water (stops them reaching the mouth), break all five routes.

```svgfig label="5.1" caption="F-diagram of faecal-oral transmission. A primary barrier (sanitary latrine) stops faeces reaching fields, flies and fluids; a secondary barrier (safe water, handwashing, food hygiene) protects the mouth."
f = Fig(760, 250)
f.box(10, 100, 100, 50, "Faeces", fill=SAND, stroke=AMBER, size=12, bold=True)
f.box(330, 100, 100, 50, "New host\n(mouth)", fill=ROSE, stroke=RED, size=11, bold=True)
rt = [("Fluids", 20), ("Flies", 70), ("Fields", 120), ("Fingers", 170), ("Food", 220)]
for n_, y in [("Fluids", 6), ("Flies", 62), ("Fields", 118), ("Fingers", 174), ("Food", 206)]:
    pass
ys = [10, 60, 110, 160, 205]
for (n_, _), y in zip(rt, ys):
    f.box(160, y, 110, 32, n_, fill=BLUE, stroke=NAVY, size=11, bold=True)
    f.arrow([(110, 125), (160, y + 16)], color=SLATE, sw=1.3)
    f.arrow([(270, y + 16), (330, 125)], color=SLATE, sw=1.3)
f.box(470, 20, 280, 82, "PRIMARY barrier (sanitation)\nSanitary latrine, safe disposal\nof child faeces, no open\ndefecation", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(470, 120, 280, 98, "SECONDARY barrier (hygiene)\nSafe water (boil, chlorinate, filter),\nhandwashing with soap,\ncovered food, fly control", fill=SAND, stroke=AMBER, size=10.5, bold=True)
```

**Chlorination of a well** is the nurse's practical task after floods or an outbreak. The volume of a round well is π r² h. The required chlorine dose (here 2 mg/L, high enough for the demand) is multiplied by the volume, and the weight of **bleaching powder** (33% available chlorine) is the chlorine weight ÷ 0.33. For a 0.5% chlorine solution used to disinfect surfaces and spills, 5 g of chlorine per litre is needed, which means **15.2 g of bleaching powder per litre**.

```python
import math
r, h = 1.0, 4.0                       # well radius and water depth, metres
litres = math.pi * r ** 2 * h * 1000
chlorine_g = litres * 2 / 1000        # 2 mg per litre
powder_g = chlorine_g / 0.33          # bleaching powder 33% available chlorine
print(f"Volume = {litres:,.0f} L")
print(f"Chlorine needed = {chlorine_g:.1f} g")
print(f"Bleaching powder = {powder_g:.1f} g")
print(f"0.5% solution: {5 / 0.33:.1f} g powder per litre")
print(f"1000 people at 45 L = {1000 * 45:,} L/day; at 15 L = {1000 * 15:,} L/day")
print(f"Diarrhoea episodes prevented by 30% cut = {1000 - 1000 * 0.7:.0f} of 1000")
```

```text
Volume = 12,566 L
Chlorine needed = 25.1 g
Bleaching powder = 76.2 g
0.5% solution: 15.2 g powder per litre
1000 people at 45 L = 45,000 L/day; at 15 L = 15,000 L/day
Diarrhoea episodes prevented by 30% cut = 300 of 1000
```

The well holds **12,566 litres**, needs **25.1 g of chlorine**, which is **76.2 g of bleaching powder**. The powder is made into a thin paste in a bucket, the clear liquid is poured into the well, mixed by lowering and raising the bucket, left for 30 minutes and tested for 0.2-0.5 mg/L free chlorine.

## 5.2 Housing, household air pollution and occupational health

Many Nepali households still cook on open fires of wood, dung or kerosene. **Household air pollution** causes chronic bronchitis and COPD in women, pneumonia in children, low birth weight and eye disease. Prevention is an **improved cookstove with a chimney**, a smoke hood or vent, clean fuel (LPG, biogas, electric induction), cooking outdoors when possible and keeping children away from the fire. Good housing has enough space, light, ventilation, a dry floor and a separate cooking area.

**Occupational health** protects workers. In Nepal the main groups at risk are farmers (pesticide poisoning, snake bite, back pain), porters (musculoskeletal injury, falls), brick-kiln workers (silicosis, heat, child labour), carpet and garment workers (dust, byssinosis, posture), construction workers (falls, noise), health workers (needle-stick, TB, back strain) and migrant workers abroad. Diseases are prevented by the **hierarchy of controls**: eliminate the hazard, substitute, engineering control (ventilation, guards), administrative control (rotation, training) and finally personal protective equipment. **Noise** is a common hazard: sound levels in decibels add logarithmically, and the safe exposure limit is 85 dB for 8 hours, halving for every 3 dB increase.

```python
import math
# two machines of 90 dB each
total = 10 * math.log10(10 ** 9 + 10 ** 9)
print(f"Two machines of 90 dB = {total:.1f} dB")
# allowed time at 94 dB with limit 85 dB for 8 h and 3 dB exchange rate
print(f"Safe time at 94 dB = {8 / 2 ** ((94 - 85) / 3):.1f} h")
# health-care waste: 50 beds x 0.5 kg per bed per day, 15% hazardous
waste = 50 * 0.5
print(f"Waste = {waste:.0f} kg/day; hazardous = {waste * 0.15:.2f} kg/day")
# mass casualty: 120 injured, triage by 15/25/55/5 per cent
for name, p in (("Red", 0.15), ("Yellow", 0.25), ("Green", 0.55), ("Black", 0.05)):
    print(f"{name}: {120 * p:.0f}")
```

```text
Two machines of 90 dB = 93.0 dB
Safe time at 94 dB = 1.0 h
Waste = 25 kg/day; hazardous = 3.75 kg/day
Red: 18
Yellow: 30
Green: 66
Black: 6
```

Two machines of 90 dB together produce **93.0 dB**, not 180, and a worker exposed at 94 dB may stay only **1.0 hour** a day without ear protection. The Nepal laws behind these protections are the Labour Act and the Occupational Safety and Health Act 2074 (2018). The nurse screens workers, teaches protective equipment, gives tetanus and hepatitis B vaccines and reports occupational disease.

## 5.3 Health-care waste management

A hospital or health post produces about 0.5 kg of waste per bed a day, and about **15% is hazardous** (infectious, sharp, chemical or pharmaceutical). A 50-bed hospital makes **25 kg a day**, of which **3.75 kg** is hazardous. **Segregation at the point of generation** is the first and most important step, followed by collection in colour-coded bins, safe storage under 48 hours, treatment (autoclave, incineration or burial pit) and final disposal. Health workers must take hepatitis B vaccination and use puncture-resistant containers for sharps.

```svgfig label="5.2" caption="Colour-coded health-care waste segregation, as in the Nepal health-care waste management guideline. Sharps go to the safety box immediately and are never recapped."
f = Fig(760, 200)
cl = [("Yellow", "Infectious waste:\ndressings, swabs,\nblood-soaked cotton", SAND, AMBER), ("Red", "Plastics:\ntubing, bags,\nsyringes (no needle)", ROSE, RED), ("Blue / white", "Sharps:\nneedles, blades,\nbroken glass", BLUE, NAVY), ("Black", "General waste:\npaper, food,\npackaging", SOFT, SLATE), ("Green", "Organic /\ncompost:\nkitchen waste", MINT, TEAL)]
for i, (t_, d_, fc, sc) in enumerate(cl):
    x = 6 + i * 150
    f.box(x, 22, 134, 36, t_, fill=fc, stroke=sc, size=11.5, bold=True)
    f.box(x, 66, 134, 70, d_, fill=SOFT, stroke=sc, size=10)
f.text(380, 164, "Segregate at source > collect > store under 48 h > treat > dispose; keep a waste register", size=10.5, color=NAVY, bold=True)
f.text(380, 188, "The person who produces the waste is responsible for putting it in the right bin", size=10.5, color=TEAL, bold=True)
```

## 5.4 Disaster management and triage

Nepal is exposed to earthquakes, floods, landslides, fires, epidemics and glacial lake outburst. The 2015 Gorkha earthquake killed about 9,000 people and injured more than 22,000 and damaged hundreds of health facilities. The **disaster cycle** has four phases: **mitigation and prevention** (building codes, safe schools), **preparedness** (plans, drills, emergency kits, early warning, stockpiles), **response** (search and rescue, triage, first aid, shelter, water, food, disease surveillance) and **recovery** (rebuilding, psychosocial care). The Disaster Risk Reduction and Management Act 2074 (2017) gives local governments the leading role, and the health cluster is led by the MoHP.

**Triage** sorts casualties to do the greatest good for the greatest number: **Red** (immediate: airway obstruction, severe bleeding, shock), **Yellow** (delayed: fractures, stable burns), **Green** (minor: walking wounded) and **Black** (dead or expectant). The START method uses walking, breathing (over 30 breaths a minute is red), circulation (capillary refill over 2 seconds is red) and mental status (cannot follow commands is red). In a mass casualty of 120 with 15% red, 25% yellow, 55% green and 5% black the numbers are **18 red, 30 yellow, 66 green and 6 black**, so the first team plans 18 stretchers and priority transport. After disaster the nurse also watches for diarrhoea, measles and respiratory infection in camps, and gives psychological first aid.

## 5.5 Health education and behaviour change

**Health education** is the process of giving people the knowledge, skill and motivation to protect and improve their health. It follows the **communication process**: sender, message, channel, receiver and feedback. Methods are individual (counselling, home visit), group (demonstration, role play, group discussion, mothers' group) and mass (radio, FM, posters, street drama, mobile messages). Good messages are accurate, simple, local, repeated and tested. The **stages of change** model describes how people move from precontemplation to contemplation, preparation, action and maintenance; the nurse matches her advice to the stage, so a smoker who is not yet ready needs awareness, not instructions. **Adult learners** learn best by doing and by relating the topic to their life, so demonstration with return demonstration beats a lecture.

## 5.6 The nurse's role in preventing diarrhoeal disease: eight points

Diarrhoea still causes illness in about 10% of Nepali children under five in any two-week period (NDHS 2022), and only 48% of them get ORS. The community nurse uses these eight points.

1. **Promote safe drinking water.** Teach boiling, chlorination, filtration or SODIS, and storage in a clean covered vessel with a tap. Test the community source for coliforms and chlorine. In floods and after earthquakes, chlorinate wells first.
2. **Build and use sanitary latrines.** Support the ward in keeping every household toilet clean and in use, including the school and health post. Teach safe disposal of the faeces of small children, which are as dangerous as adult faeces. Open defecation anywhere breaks the primary barrier.
3. **Teach handwashing with soap.** Wash after using the toilet or cleaning a child, and before cooking, serving and eating, for 20 seconds, scrubbing all parts. Put a soap and water point near the toilet. Teach by demonstration with return demonstration.
4. **Promote food hygiene.** Cook food well, eat it hot, cover it, wash fruit and vegetables, and keep raw and cooked food apart. Use clean utensils for infant feeding rather than a bottle. Keep flies away from food and waste.
5. **Promote exclusive breastfeeding and rotavirus vaccine.** Breast milk protects the child, and bottles are a common source of infection. Rotavirus vaccine at 6 and 10 weeks and measles vaccine reduce the severity of diarrhoea. Teach the mother not to stop breastfeeding when the child has diarrhoea.
6. **Teach home management with ORS and zinc.** Show how to mix the ORS packet in 1 litre of clean water and to give it by cup and spoon after every loose stool. Give zinc 20 mg daily for 10 days. Continue feeding and increase the feeds after recovery.
7. **Teach danger signs for early referral.** The family must bring the child at once if he cannot drink, vomits everything, has blood in the stool, repeated watery stools, high fever or sunken eyes. Give the child ORS on the way. Early referral prevents deaths from severe dehydration.
8. **Organise community action and surveillance.** Work with the ward committee, school clubs, FCHVs and the water user committee to protect sources and clean the surroundings. Report a cluster of cases or cholera-like illness to the district office the same day. Keep ORS corners at the health post and in the ward.

## Formula and fact sheet

- Residual chlorine 0.2-0.5 mg/L after 30 minutes. Chlorine g = litres × dose (mg/L) ÷ 1000; bleaching powder g = chlorine g ÷ 0.33. 0.5% solution = 15.2 g powder per litre.
- Well volume = π r² h × 1000 litres: r = 1 m, h = 4 m gives 12,566 L, 25.1 g chlorine, 76.2 g powder.
- F-diagram: fingers, flies, fluids, fields, food. Handwashing cuts diarrhoea by about 30%.
- Noise: 85 dB for 8 h, halve the time for each +3 dB; 90 + 90 dB = 93.0 dB. Hazardous waste about 15% of health-care waste.
- Triage: red, yellow, green, black. Disaster cycle: mitigation, preparedness, response, recovery.

## Chapter summary

- Safe water, sanitation and hygiene break the faecal-oral routes of the F-diagram.
- Chlorination is calculated from the volume of the well, the dose and the strength of the powder.
- Indoor smoke, workplace hazards and noise are prevented by controls, not by blaming the worker.
- Health-care waste is segregated by colour at the source; triage and the disaster cycle organise the response.
- Health education uses simple, repeated messages and demonstration to change behaviour.

## Practice

**MCQs (with reasons)**

1. The free residual chlorine at the point of use should be: (a) 0.02-0.05 mg/L (b) 0.2-0.5 mg/L (c) 2-5 mg/L (d) 20-50 mg/L.
2. In the F-diagram which is NOT one of the five F's? (a) Flies (b) Fluids (c) Fever (d) Fingers.
3. Two machines of 90 dB each together give about: (a) 180 dB (b) 93 dB (c) 95 dB (d) 90 dB.
4. A casualty with a respiratory rate of 36 per minute in START triage is: (a) green (b) yellow (c) red (d) black.
5. In health-care waste, needles are placed in the: (a) yellow bag (b) red bag (c) puncture-resistant blue or white container (d) black bin.

::: note Answers and rationales
**1. (b).** 0.2-0.5 mg/L gives protection against recontamination without a bad taste; lower levels are not protective and higher levels are unpleasant.
**2. (c).** The five F's are fingers, flies, fluids, fields and food.
**3. (b).** Decibels add logarithmically: 10 log₁₀(2 × 10⁹) = 93.0 dB, an increase of 3 dB only.
**4. (c).** A respiratory rate above 30 per minute is red (immediate) in START triage.
**5. (c).** Sharps go into puncture-resistant containers at once without recapping, to prevent needle-stick injury.
:::

**Short answer (3 marks): Chlorination of a well.** First find the volume (π r² h). Multiply by the dose, for example 2 mg/L, to get the grams of chlorine; for a well of 12,566 L this is 25.1 g. Divide by 0.33 for bleaching powder (76.2 g). Mix the powder into a paste, pour the clear liquid into the well, mix, wait 30 minutes and test the residual chlorine for 0.2-0.5 mg/L.

**Medium answer (5 marks): Explain the F-diagram and the measures to break faecal-oral transmission (Figure 5.1).** The F-diagram shows the routes by which faeces reach a new host: fluids (water), flies, fields (soil and crops), fingers and food. A **primary barrier** stops faeces from entering the environment: a sanitary latrine, safe disposal of child faeces and no open defecation. A **secondary barrier** stops faeces from reaching the mouth: safe water by boiling or chlorination, handwashing with soap, food hygiene and fly control. Nepal's open-defecation-free declaration of 2019 supports the primary barrier. The nurse teaches the barriers, tests water sources and supports ORS and zinc for the sick. Handwashing alone reduces diarrhoea by about 30%.

**Long answer (10 marks): Nurse Anita Gurung is the school health nurse for a hill school of 400 children where the well water showed coliform bacteria and 12 children had diarrhoea last week. Plan the response, including the chlorination of a round well of radius 1 m and water depth 4 m, and a health education plan.**

*Calculation.* The volume is π × 1² × 4 × 1000 = **12,566 litres**; at 2 mg/L the chlorine needed is 12,566 × 2 ÷ 1000 = **25.1 g**, and with 33% bleaching powder the weight is 25.1 ÷ 0.33 = **76.2 g**. For disinfecting toilets and surfaces a 0.5% solution needs **15.2 g** of powder per litre. A drinking-water need of 15 litres a child for 400 children is 6,000 litres a day, and the school should aim at a safe water point within 30 minutes of walk.

*Plan.* (1) Treat the 12 children with ORS and zinc, check for dehydration and send those with danger signs to the health post. (2) Chlorinate the well as above, wait 30 minutes and test the residual chlorine (0.2-0.5 mg/L); repeat weekly until the source is made safe and protected with a cover and a platform. (3) Inspect the toilets and hand-washing stations, and make sure that soap and water are available. (4) Teach handwashing with soap in each class with demonstration; if it cuts diarrhoea by 30%, 12 weekly cases would fall to about 8. (5) Form a school health club in which students check the toilets and water every day, and give messages to their families. (6) Report the cluster to the district office and monitor absenteeism and cases for 2 weeks. (7) Link to the ward water user committee and the local government for long-term protection of the source.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **O:** coliform positive well, 12 children with diarrhoea, 400 students, no soap at the toilet. | **Risk for infection** (faecal-oral) related to contaminated water and poor hygiene. | **Infection status:** no new diarrhoea case for 2 weeks and 0 coliform in 7 days. | 1. Chlorinate the well with 76.2 g bleaching powder and check residual chlorine; *kills coliforms.* 2. Provide a covered, protected source; *prevents recontamination.* 3. Provide soap and water at the toilets; *makes handwashing possible.* | Test the water weekly; count cases daily. |
| **S:** a child says "we do not wash hands before eating." **O:** only 3 of 10 observed children wash with soap. | **Deficient knowledge** about hand hygiene related to lack of teaching, as evidenced by poor practice. | **Knowledge: health behaviour:** 80% of children demonstrate correct handwashing in 1 month. | 1. Demonstrate the 20-second handwashing with return demonstration; *learning by doing lasts.* 2. School health club monitors; *peer support sustains habits.* 3. Songs, posters and parent messages; *spread to homes.* | Observe handwashing in 1 month; goal met at 80%. |
| **O:** 4 children mildly dehydrated, drink eagerly. | **Risk for deficient fluid volume** related to diarrhoea. | **Hydration:** no signs of dehydration within 4 hours. | 1. ORS by cup, 75 mL/kg over 4 hours if some dehydration; *replaces losses safely.* 2. Zinc 20 mg for 10 days (10 mg under 6 months); *shortens illness.* 3. Teach danger signs and referral; *early help for the worse.* | Reassess at 4 hours and next day. |

::: tip Exam tip
In a community question, always show the calculation (volume, dose, powder), then structure the answer into water, sanitation, hygiene, education and surveillance, and mention a Nepal link such as the open-defecation-free declaration or the school health programme.
:::
