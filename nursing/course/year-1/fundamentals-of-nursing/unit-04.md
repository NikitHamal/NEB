---
subject: Fundamentals of Nursing
grade: BSc Nursing Year 1
unit: 4
title: Infection Prevention and Control
hours: 16
area: BSN 4 · Fundamentals of Nursing · Unit 4
---

A hospital should heal, yet WHO estimates that about 15 of every 100 hospitalised patients in low- and middle-income countries pick up a new infection during care. The nurse's hands, gloves, injections and dressings are the main route. This unit teaches the chain of infection, hand hygiene, PPE, disinfection and sterilisation, safe sharps and waste, the chlorine-solution sums every ward nurse needs, and what to do after a needle-stick.

::: key What this unit gives you
- The six links of the chain of infection and the five moments of hand hygiene (WHO).
- Standard and transmission-based precautions; the order of putting on and removing PPE.
- Disinfection versus sterilisation, and the Spaulding classification.
- Chlorine solution 0.5% and 0.1%, calculated and verified; needle-stick risk figures.
- Eight nursing responsibilities in preventing health-care-associated infection and a full care plan.
:::

## 4.1 The chain of infection

Infection needs six links. Break **any one** and the chain fails.

```svgfig label="4.1" caption="The chain of infection and one way to break each link. Hand hygiene breaks the mode-of-transmission link, vaccination breaks the host link."
f = Fig(760, 270)
links = [("1 Agent", "bacteria, virus,\nfungus, parasite", "disinfect, sterilise"), ("2 Reservoir", "patient, staff,\nwater, equipment", "clean, treat source"), ("3 Portal of exit", "blood, sputum,\nstool, wound", "cover wounds, cough etiquette"),
         ("4 Transmission", "contact, droplet,\nairborne, vehicle", "hand hygiene, PPE"), ("5 Portal of entry", "cut, catheter,\ncannula, mouth", "aseptic technique"), ("6 Susceptible host", "newborn, elderly,\ndiabetic, HIV", "vaccinate, nutrition")]
for i, (a, b, c) in enumerate(links):
    x = 8 + i * 125
    f.box(x, 20, 115, 36, a, fill=BLUE, stroke=NAVY, size=10.5, bold=True, color=NAVY)
    f.box(x, 62, 115, 52, b, fill=SOFT, stroke="#cbd5e1", size=10, color=SLATE)
    f.arrow([(x + 57, 118), (x + 57, 150)], color=RED, sw=1.8)
    f.box(x, 154, 115, 54, c, fill=MINT, stroke=TEAL, size=10, color=NAVY)
f.text(380, 236, "Top: the link.  Middle: examples.  Bottom: the nursing action that breaks it.", size=11, color=SLATE)
```

A **health-care-associated infection (HAI)** is an infection that was not present or incubating at admission. The four commonest are catheter-associated urinary tract infection (CAUTI), central-line bloodstream infection, surgical site infection (SSI) and ventilator-associated pneumonia.

## 4.2 Hand hygiene

The hands of staff carry most hospital organisms from patient to patient. WHO's **five moments**: (1) before touching a patient, (2) before a clean or aseptic procedure, (3) after body-fluid exposure risk, (4) after touching a patient, (5) after touching the patient's surroundings. **Alcohol-based hand rub takes 20-30 seconds; soap and running water takes 40-60 seconds** and is preferred when hands are visibly soiled and after contact with spore-forming organisms (such as *C. difficile*). Where piped water is scarce, a low-cost gravity-fed container with a tap works, as Plate 4.1(b) shows.

```photogrid label="4.1" cols="3" ratio="1.0" caption="Three real tools of infection control. (a) A puncture-resistant sharps collector with biohazard label. (b) Hand washing with soap using a low-cost gravity-fed water container, usable where piped water is unavailable. (c) A health worker arranging sterilised surgical instruments, wearing a head cover."
@ photo id="nur4/sharps" cap="Sharps container"
fit 1.0
mark 0.45 0.80 "1"
mark 0.50 0.40 "2"
mark 0.22 0.30 "3"
key 1 Narrow opening, closed lid
key 2 Biohazard label and fill line
key 3 Rigid, puncture-proof body
@ photo id="nur4/handwash" cap="Hand washing with soap"
fit 1.0
mark 0.68 0.78 "1"
mark 0.74 0.30 "2"
key 1 Gravity-fed water container
key 2 Wet hands then soap and rub
@ photo id="nur4/autoclave" cap="Sterile instruments"
fit 1.0
mark 0.70 0.88 "1"
mark 0.28 0.18 "2"
key 1 Head cover
key 2 Sterilised instrument roll
```

## 4.3 Standard and transmission-based precautions

**Standard precautions** apply to **every** patient because infection is not always visible: hand hygiene, gloves for blood and body fluids, mask, eye protection and gown when splashes are likely, safe sharps, clean environment, safe waste, and respiratory etiquette. **Transmission-based precautions** are added: **contact** (gown and gloves; scabies, MRSA, diarrhoea), **droplet** (surgical mask within 1 metre; influenza, meningococcal disease, pertussis) and **airborne** (N95 respirator and a negative-pressure or well-ventilated room; pulmonary TB, measles, chickenpox).

```svgfig label="4.2" caption="Order of putting on (donning) and taking off (doffing) PPE. The dirtiest items come off first; hand hygiene follows removal."
f = Fig(760, 220)
f.text(60, 18, "DON", size=12, color=TEAL, bold=True)
for i, t in enumerate(["Gown", "Mask / N95", "Goggles", "Gloves"]):
    f.box(20 + i * 180, 28, 140, 40, f"{i+1}  {t}", fill=MINT, stroke=TEAL, size=11.5, bold=True, color=NAVY)
    if i < 3: f.arrow([(160 + i * 180, 48), (198 + i * 180, 48)], color=TEAL, sw=2)
f.text(60, 108, "DOFF", size=12, color=RED, bold=True)
for i, t in enumerate(["Gloves", "Goggles", "Gown", "Mask / N95"]):
    f.box(20 + i * 180, 118, 140, 40, f"{i+1}  {t}", fill=ROSE, stroke=RED, size=11.5, bold=True, color=NAVY)
    if i < 3: f.arrow([(160 + i * 180, 138), (198 + i * 180, 138)], color=RED, sw=2)
f.text(380, 192, "Then wash hands. Remove the mask last, from behind, in the anteroom or at the door.", size=11, color=SLATE)
```

## 4.4 Cleaning, disinfection and sterilisation

**Cleaning** removes dirt and organic matter and must come first. **Disinfection** kills most microbes but not all spores. **Sterilisation** kills all microbes including spores. By the **Spaulding classification**: *critical* items entering sterile tissue or blood (surgical instruments, needles, cannulae) must be **sterilised**; *semi-critical* items touching mucous membrane (endoscopes, laryngoscope blades) need **high-level disinfection**; *non-critical* items touching intact skin (BP cuff, stethoscope, bed rails) need cleaning or **low-level disinfection**. Moist heat in an **autoclave** (121 °C at 15 psi for 20-30 minutes for wrapped packs) is the standard method in Nepali hospitals; use an indicator tape on each pack.

**Chlorine solutions.** The usual strengths are **0.5%** (5000 ppm) for blood spills and instrument decontamination and **0.1%** (1000 ppm) for general surfaces and non-critical items.

::: example Worked example: chlorine solutions
**(a) From bleaching powder with 35% available chlorine**, 0.5% solution: grams per litre = 0.5 ÷ 35 × 1000 = **14.29 g/L**. **(b) From liquid bleach with 5% available chlorine**, to make 0.5%: dilution factor 5 ÷ 0.5 = 10, so 1 part bleach + **9 parts water**; for 10 litres, use **1 litre** of bleach and 9 litres of water. **(c) 0.1% solution from 5% stock:** 5 ÷ 0.1 = 50 parts, so for 5 litres use 5000 × 0.1 ÷ 5 = **100 mL** of stock plus 4900 mL of water. Make fresh daily: chlorine decays in light and when mixed with organic matter.
:::

## 4.5 Sharps, waste and needle-stick injury

Never recap a used needle; put the syringe and needle straight into the sharps container, which is closed when three-quarters full and sent for treatment. Segregate waste at the bedside into infectious, non-infectious and sharps streams as set out in the MoHP **Health Care Waste Management guideline** and your hospital's plan.

**Risk after a needle-stick from an infected source** (WHO estimates): hepatitis B 6-30% if the nurse is unvaccinated, hepatitis C about 1.8%, HIV about 0.3%. If 500 injuries occurred with HIV-positive sources, expected infections = 500 × 0.003 = **1.5**; per 1000 injuries, **3**. Small risk per injury, large risk over a career: vaccinate every student against hepatitis B.

**Immediate steps:** let the wound bleed, wash with soap and running water (do not squeeze or scrub, do not use bleach on skin), flush splashes to eyes and mouth with water, report to the infection control nurse, record the incident, and get risk assessment within hours. HIV post-exposure prophylaxis should start as soon as possible, ideally within 2 hours and no later than 72 hours, under the national HIV guideline.

## 4.6 Nursing responsibilities in preventing HAI: eight points

1. **Hand hygiene at the five moments.** Rub hands with alcohol or wash with soap and water at each moment. Keep nails short, remove rings and watches. This single habit prevents more infection than any drug.
2. **Use PPE correctly.** Choose gloves, mask, eye protection and gown according to the risk of splash. Remove gloves between patients and wash hands after. Gloves do not replace hand hygiene.
3. **Aseptic technique for every invasive procedure.** Use sterile gloves and a no-touch method for catheterisation, IV cannulation and dressings. Check the expiry and the indicator tape on each pack. A broken sterile field means start again.
4. **Safe injection and sharps practice.** One sterile needle and syringe for each injection, never recap, and use the sharps box at the point of use. Check that the box is not overfilled. This protects the patient from hepatitis and HIV, and the nurse from needle-stick.
5. **Care of devices.** Remove urinary catheters and cannulae as soon as they are not needed, and change cannula sites as per policy (on signs of phlebitis). Keep the urine bag below the bladder and never open the closed system. Most CAUTI and line infections come from devices left too long.
6. **Clean environment and equipment.** Wipe the bed, locker and equipment with 0.1% chlorine or detergent daily, and spills with 0.5% chlorine. Clean the stethoscope between patients. Separate clean and dirty utility rooms.
7. **Isolation and visitors.** Place patients with airborne or contact disease in the right room, teach visitors hand hygiene and mask use, and label the door. Limit visitors in neonatal and burn units. Isolation should never mean neglect.
8. **Staff health and education.** Complete the hepatitis B vaccine series, report your own fever or diarrhoea, and teach patients cough etiquette and hand washing. Record every injury and every HAI for the hospital's HMIS and infection committee. An informed patient and a healthy nurse stop spread.

## Formula and fact sheet

- Alcohol rub 20-30 s; soap and water 40-60 s.
- Autoclave 121 °C, 15 psi, 20-30 min (wrapped packs).
- Chlorine: g/L of powder = (desired % ÷ available %) × 1000; parts water = (stock % ÷ desired %) − 1.
- Needle-stick risk: HBV 6-30%, HCV about 1.8%, HIV about 0.3%.

## Chapter summary

- Break one link of the chain and infection does not occur.
- Hand hygiene at the five moments is the most effective single measure.
- Sterilise critical items, disinfect semi-critical items, clean non-critical items.
- Make chlorine solutions by calculation, fresh each day.
- After a needle-stick: wash, report, assess, and start PEP early.

## Practice

**MCQs (with reasons)**

1. Which item must be sterilised? (a) BP cuff (b) surgical scalpel (c) bed rail (d) stethoscope.
2. To make 0.5% chlorine from 5% liquid bleach, the dilution is: (a) 1 part + 4 parts water (b) 1 part + 9 parts water (c) 1 part + 49 parts water (d) 1 part + 99 parts water.
3. PPE is removed in the order: (a) mask, gown, gloves (b) gloves, goggles, gown, mask (c) gown, gloves, mask (d) any order.
4. Airborne precautions are needed for: (a) influenza (b) scabies (c) pulmonary tuberculosis (d) cholera.
5. Alcohol hand rub should be rubbed for: (a) 5 s (b) 10 s (c) 20-30 s (d) 2 minutes.

::: note Answers and rationales
**1. (b).** A scalpel enters sterile tissue (critical item). Cuff, rail and stethoscope touch intact skin or surroundings.
**2. (b).** 5 ÷ 0.5 = 10 total parts, i.e. 1 part bleach and 9 parts water. 1:4 gives 1%, 1:49 gives 0.1%.
**3. (b).** The most contaminated items (gloves, then goggles, then gown) go first and the mask last, then hands are washed.
**4. (c).** TB spreads on droplet nuclei that stay in the air. Influenza is droplet, scabies contact and cholera faeco-oral.
**5. (c).** Less than 20 s does not give enough contact time.
:::

**Short answer (3 marks): Spaulding classification.** Critical items enter sterile tissue or the bloodstream (surgical instruments, cannulae) and must be sterilised, for example by autoclaving. Semi-critical items touch mucous membranes or non-intact skin (laryngoscope blade, endoscope) and need at least high-level disinfection. Non-critical items touch only intact skin (BP cuff, bed rail) and need cleaning or low-level disinfection with 0.1% chlorine or alcohol.

**Medium answer (5 marks): Explain the chain of infection and how the nurse breaks it (Figure 4.1).** The chain has six links. The **agent** (microorganism) lives in a **reservoir** (patient, carrier, water, equipment). It leaves through a **portal of exit** (blood, sputum, stool, wound drainage), is carried by a **mode of transmission** (contact, droplet, airborne, vehicle or vector) and enters by a **portal of entry** (broken skin, catheter, respiratory or GI tract) to infect a **susceptible host** (newborn, elderly, malnourished, immunosuppressed). The nurse breaks the chain by sterilising equipment, treating the source, covering wounds, performing hand hygiene and wearing PPE, using aseptic technique, and protecting the host by immunisation and nutrition. Example: for a catheterised patient the nurse removes the catheter early, uses a closed drainage system and washes hands, which blocks the entry and transmission links.

**Long answer (10 marks): Mr Karki, 66, is catheterised after prostate surgery in the surgical ward. On day 4 he has a temperature of 38.2 °C, cloudy urine and suprapubic pain. Describe how HAI is prevented and prepare a care plan.**

*Introduction.* The picture suggests **CAUTI**, the commonest HAI. Organisms such as *E. coli* travel along or inside the catheter, and the risk rises every day the catheter remains. Prevention is a bundle: insert only when indicated, use strict asepsis, keep the closed system, keep the bag below the bladder, give daily meatal care, and remove at the earliest opportunity. Management: tell the doctor, send a urine culture from the sampling port (not the bag) before antibiotics, give antibiotics as prescribed, and review the need for the catheter.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I have burning and pain in my lower belly." **O:** Indwelling catheter day 4, T 38.2 °C, cloudy urine, tenderness above pubis. | **Risk for infection** has become actual: **Infection** related to indwelling urinary catheter, as evidenced by fever 38.2 °C and cloudy urine. | **Infection severity:** temperature below 37.5 °C and clear urine within 72 h. | 1. Hand hygiene and sterile technique for every catheter contact; *keeps organisms out.* 2. Collect urine culture aseptically from the port; *identifies the organism.* 3. Give antibiotic on time; *kills bacteria.* 4. Keep the closed system and the bag below the bladder, never on the floor; *prevents reflux.* 5. Meatal care twice daily with soap and water; *reduces colonisation.* 6. Oral fluids 2-3 L if allowed; *flushes the tract.* 7. Ask the doctor daily about removal; *the shortest catheter time is the best prevention.* | Temperature, urine colour and pain reviewed each shift; culture result followed; catheter removed when the order is given. |
| **O:** Patient and wife unaware of catheter care. | **Deficient knowledge** (catheter care) related to no previous exposure. | Patient and wife state 3 care rules before discharge. | Teach hand washing, bag position, no pulling, and signs to report; *home care depends on the family.* | Teach-back done and recorded. |

:::tip Exam tip
For any infection question draw or mention the chain of infection and say which link each nursing action breaks. It organises the answer and gains the marks for prevention.
:::
