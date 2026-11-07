---
subject: Community Health Nursing
grade: BSc Nursing Year 1
unit: 3
title: Communicable Disease Control, Immunisation, Tuberculosis and Vector-borne Disease
hours: 30
area: BSN 6-7 · Community Health Nursing · Unit 3
---

Infectious disease is still the daily work of a Nepali health post: diarrhoea, pneumonia, typhoid, tuberculosis, dengue, scrub typhus and malaria. The nurse's strongest tool is not a drug but **immunisation**, which in Nepal has taken smallpox and polio out of the country and brought measles and neonatal tetanus under control. This unit gives the chain of infection, the National Immunization Programme (NIP) schedule and cold chain, DOTS for tuberculosis and vector control, with the calculations that make a session plan.

::: key What this unit gives you
- Real photographs of a vaccine carrier with temperature loggers, a Nepal immunisation clinic, an AFB-stained sputum smear and the mosquito vectors of malaria and dengue.
- The chain of infection, the current NIP schedule, the cold chain and the shake test.
- Vaccine efficacy, herd immunity threshold, vaccine need with wastage, coverage and dropout, DOTS tablet counts, and vector indices, all worked step by step.
- Eight points on the nurse's responsibilities in an immunisation session, and model answers with a measles outbreak case and care plan.
:::

## 3.1 The chain of infection and levels of control

Infection spreads through a **chain of six links**: the infectious agent, its reservoir (human, animal, water, soil), the portal of exit, the mode of transmission (direct contact, droplet, airborne, vehicle such as water or food, vector such as a mosquito), the portal of entry and the susceptible host. Cutting any link stops spread. Control therefore has three parts: control of the **source** (find, treat and isolate cases), interruption of **transmission** (sanitation, masks, vector control) and protection of the **susceptible** (immunisation, nutrition, chemoprophylaxis). **Notifiable diseases** such as measles, cholera, AFP (polio), neonatal tetanus and COVID-19 are reported immediately to the Epidemiology and Disease Control Division through the early warning and reporting system (EWARS).

```svgfig label="3.1" caption="The chain of infection and the control measure that breaks each link."
f = Fig(760, 250)
ln = [("Agent", "Treat cases,\nantibiotics", ROSE, RED), ("Reservoir", "Isolate,\nclean water", SAND, AMBER), ("Exit", "Cough etiquette,\nsafe disposal", BLUE, NAVY), ("Transmission", "Hand wash, mask,\nvector control", MINT, TEAL), ("Entry", "Wound care,\nsterile technique", BLUE, NAVY), ("Host", "Vaccine,\nnutrition", SAND, AMBER)]
for i, (t_, d_, fc, sc) in enumerate(ln):
    x = 8 + i * 124
    f.box(x, 30, 112, 40, t_, fill=fc, stroke=sc, size=11, bold=True)
    f.box(x, 100, 112, 56, d_, fill=SOFT, stroke=sc, size=10)
    if i < 5: f.arrow([(x + 112, 50), (x + 124, 50)], color=SLATE, sw=2)
    f.arrow([(x + 56, 70), (x + 56, 100)], color=sc, sw=1.5)
f.text(380, 190, "Break any one link and the chain stops", size=12, color=NAVY, bold=True)
f.text(380, 215, "Source control  +  transmission control  +  protect the susceptible", size=10.5, color=TEAL, bold=True)
```

## 3.2 The National Immunization Programme and the cold chain

The NIP began in 1977 (2034 BS) as the Expanded Programme on Immunization and is a priority-one programme of the MoHP. All vaccines are free. The current routine schedule, as published by the MoHP (check the latest circular for any change such as the HPV schedule), is:

| Age | Vaccine | Route and site |
|---|---|---|
| Birth | BCG | Intradermal, right upper arm |
| 6, 10, 14 weeks | DPT-HepB-Hib (pentavalent) | Intramuscular, left mid-thigh |
| 6, 10, 14 weeks | OPV (oral polio) | 2 drops by mouth |
| 6, 10 weeks | Rotavirus | Oral |
| 6, 10 weeks and 9 months | PCV (pneumococcal) | Intramuscular, right mid-thigh |
| 14 weeks and 9 months | fIPV (fractional inactivated polio) | Intradermal, right upper arm |
| 9 and 15 months | MR (measles-rubella) | Subcutaneous, right upper arm |
| 12 months | JE (Japanese encephalitis) | Subcutaneous, left upper arm |
| 15 months | Typhoid conjugate vaccine | Intramuscular |
| Pregnancy | Td (tetanus-diphtheria), 2 doses or boosters | Intramuscular, upper arm |
| Adolescent girls (grades 6-10) | HPV | Intramuscular, upper arm |

A child is **fully immunised** after BCG, three pentavalent, three OPV, two fIPV and one MR by the first birthday. Vaccines are heat- or freeze-sensitive: the **cold chain** keeps them between **+2 °C and +8 °C** from the manufacturer to the child. Nepal's chain runs from the central store through regional and district stores to the health post's ice-lined refrigerator and the **vaccine carrier** with four frozen ice packs used in outreach. Freeze-sensitive vaccines (pentavalent, PCV, Td, Hep B, IPV) are checked by the **shake test**; BCG, OPV and MR are heat-sensitive. Use the vaccine vial monitor (VVM), keep an open-vial policy (BCG and MR are discarded after 6 hours or at the end of the session), and record the temperature twice a day.

```photogrid label="3.1" cols="3" ratio="1.0" caption="Immunisation in practice. (a) A vaccine carrier with two temperature loggers (yellow): the cold chain is checked, not assumed. (b) A mother's card is filled in at the District Public Health Office immunisation clinic, Pokhara. (c) A vaccine is given to an infant in the same clinic."
@ photo id="nur3/carrier" cap="Vaccine carrier with data loggers"
fit 1.0
focus 0.5 0.5
mark 0.42 0.62 "1"
mark 0.25 0.22 "2"
key 1 (a) Yellow electronic temperature logger: records +2 to +8 °C compliance
key 2 (a) Blue insulated cold box: the lid keeps the frozen ice packs cold
@ photo id="nur3/imm1" cap="Immunisation card, Pokhara"
fit 1.0
focus 0.5 0.5
mark 0.30 0.55 "3"
mark 0.60 0.40 "4"
key 3 (b) The immunisation card: the record that tells the next visit date
key 4 (b) The mother holds the infant for the vaccinator
@ photo id="nur3/imm2" cap="Giving a vaccine to an infant"
fit 1.0
focus 0.5 0.5
mark 0.30 0.62 "5"
mark 0.62 0.45 "6"
key 5 (c) The vaccinator's hands: the limb is held firmly before the needle goes in
key 6 (c) The infant is held in the mother's lap for safety
```

```python
# vaccine efficacy: 20 per 1000 unvaccinated vs 2 per 1000 vaccinated
ve = (0.02 - 0.002) / 0.02 * 100
print(f"Vaccine efficacy = {ve:.0f}%")
# herd immunity threshold = 1 - 1/R0
print(f"Measles (R0 15): {(1 - 1 / 15) * 100:.1f}%; polio (R0 6): {(1 - 1 / 6) * 100:.1f}%")
# vaccine need for 840 infants: doses = target x doses x wastage factor, wastage factor = 1 / (1 - rate)
bcg = 840 * 1 / (1 - 0.5); mr = 840 * 2 / (1 - 0.25)
print(f"BCG: {bcg:,.0f} doses = {bcg / 20:.0f} vials of 20 doses (wastage 50%)")
print(f"MR: {mr:,.0f} doses = {mr / 10:.0f} vials of 10 doses (wastage 25%)")
# coverage and dropout: Penta1 826, Penta3 780, MR1 744, fully immunised 672 of 840
print(f"Fully immunised coverage = {672 / 840 * 100:.0f}%")
print(f"Penta1-Penta3 dropout = {(826 - 780) / 826 * 100:.1f}%")
print(f"Penta1-MR1 dropout = {(826 - 744) / 826 * 100:.1f}%")
```

```text
Vaccine efficacy = 90%
Measles (R0 15): 93.3%; polio (R0 6): 83.3%
BCG: 1,680 doses = 84 vials of 20 doses (wastage 50%)
MR: 2,240 doses = 224 vials of 10 doses (wastage 25%)
Fully immunised coverage = 80%
Penta1-Penta3 dropout = 5.6%
Penta1-MR1 dropout = 9.9%
```

A vaccine that cuts the attack rate from 20 to 2 per 1000 has an **efficacy of 90%**. The **herd immunity threshold** is 1 − 1/R₀: **93.3%** for measles (R₀ 15, the reason two MR doses and campaign catch-up are needed) and **83.3%** for polio (R₀ 6). Vaccine need is planned with the **wastage factor** = 1 ÷ (1 − wastage rate): for 840 infants BCG needs **1,680 doses = 84 vials** (the 20-dose vial and many open-vial losses give 50% wastage) and two MR doses need **2,240 doses = 224 vials**. If 672 of 840 infants are fully immunised the coverage is **80%**, which matches NDHS 2022 (80%). Pentavalent 1 (826) to 3 (780) gives a **dropout of 5.6%** (an access and follow-up problem) and Penta 1 to MR1 (744) gives **9.9%**; a dropout above 10% needs defaulter tracing by the FCHV.

## 3.3 Tuberculosis and DOTS

TB is caused by *Mycobacterium tuberculosis* and spreads by droplet nuclei when a person with lung TB coughs. Nepal has a high burden: the National Tuberculosis Programme (NTP) estimates that tens of thousands fall ill each year and about a third are never notified. A person with **cough for 2 weeks or more**, fever, night sweats, weight loss or blood in sputum is a presumptive case and is tested with **Xpert MTB/RIF** (preferred, also detects rifampicin resistance) or **sputum smear microscopy** by Ziehl-Neelsen stain, with chest X-ray where available. Children are screened by contact history, symptoms, tuberculin test and X-ray. HIV testing is offered to every TB patient.

Treatment is **DOTS** (directly observed treatment, short course): a trained observer (health worker, FCHV or family member) watches the patient swallow every dose. A new drug-sensitive case gets **2 months of isoniazid, rifampicin, pyrazinamide and ethambutol (2HRZE) followed by 4 months of isoniazid and rifampicin (4HR)**, in fixed-dose combination tablets given by weight band (40-54 kg three tablets, 55-70 kg four tablets, as in the NTP guideline). Smear follow-up is done at the end of month 2 (or 3) and month 5 and at completion. The five elements of DOTS are political commitment, quality-assured diagnosis, standard short-course treatment with observation, uninterrupted drug supply and a recording and reporting system. Outcomes are cured, treatment completed, failed, died, lost to follow-up and not evaluated; drug-resistant TB (MDR/RR-TB) needs referral to the treatment centres and the shorter all-oral regimens.

```svgfig label="3.2" caption="DOTS pathway for pulmonary TB in a Nepal health post: find, test, treat under observation, and follow up to cure."
f = Fig(760, 210)
b = [("Cough 2 weeks\nor more\n(presumptive TB)", SAND, AMBER), ("Xpert MTB/RIF\nor sputum\nAFB smear", BLUE, NAVY), ("Positive:\nregister, HIV test,\nweigh, start FDC", ROSE, RED), ("2HRZE: 56 days\nthen 4HR: 112 days\nunder DOT", MINT, TEAL), ("Smear at\nmonth 2, 5, 6:\ncured / completed", SAND, AMBER)]
for i, (t_, fc, sc) in enumerate(b):
    x = 6 + i * 150
    f.box(x, 40, 134, 76, t_, fill=fc, stroke=sc, size=10, bold=True)
    if i < 4: f.arrow([(x + 134, 78), (x + 150, 78)], color=SLATE, sw=2)
f.text(380, 22, "Test > Treat > Observe > Follow up", size=11.5, color=NAVY, bold=True)
f.text(380, 150, "Negative with symptoms: X-ray, clinical review, antibiotics, re-test or refer", size=10, color=SLATE)
f.text(380, 185, "Trace contacts, give TB preventive therapy to children under 5 and people with HIV", size=10.5, color=TEAL, bold=True)
```

## 3.4 Vector-borne diseases: malaria, dengue, kala-azar, scrub typhus

**Malaria** (*Plasmodium vivax* mostly, some *falciparum*) is carried by the female *Anopheles* mosquito, which bites at night; it now remains in a few Terai and border districts, and Nepal aims to eliminate it. Diagnosis is by a rapid diagnostic test or blood smear, treatment of *vivax* is chloroquine for 3 days plus primaquine for 14 days after a G6PD check (as the national guideline directs), and prevention uses long-lasting insecticidal nets, indoor spraying and early treatment. **Dengue** is carried by the day-biting *Aedes aegypti* and *albopictus*, which breed in clean stored water in tyres, pots and coolers; it has spread to hill districts and Kathmandu since 2019. Fever with severe headache, pain behind the eyes and a falling platelet count is dengue until proven otherwise; warning signs (abdominal pain, vomiting, bleeding, restlessness) need admission and careful fluid, and aspirin and ibuprofen are avoided. **Kala-azar** (sandfly), **scrub typhus** (chigger mite) and **Japanese encephalitis** (*Culex*, pigs) are other local vector diseases.

```photogrid label="3.2" cols="3" ratio="1.0" caption="Finding the cause and the carrier. (a) A real sputum smear from a tuberculosis patient: acid-fast bacilli stain red against a blue background. (b) A female Anopheles mosquito feeding: the body angle is slanted, with the head down (CDC). (c) Aedes aegypti, the dengue vector, with white bands on its black legs (CDC)."
@ photo id="nur3/afb" cap="AFB in sputum (Ziehl-Neelsen)"
fit 1.0
focus 0.5 0.5
mark 0.38 0.55 "1"
mark 0.82 0.60 "2"
key 1 (a) Red rods: acid-fast bacilli of Mycobacterium tuberculosis
key 2 (a) A cluster of red bacilli: report as 1+, 2+ or 3+ by number
@ photo id="nur3/anoph" cap="Anopheles mosquito (malaria)"
fit 1.0
focus 0.5 0.5
mark 0.62 0.62 "3"
mark 0.30 0.50 "4"
key 3 (b) Body held at an angle to the skin, typical of Anopheles
key 4 (b) Long palps next to the proboscis: a feature of the genus
@ photo id="nur3/aedes" cap="Aedes aegypti (dengue)"
fit 1.0
focus 0.5 0.5
mark 0.40 0.65 "5"
mark 0.30 0.30 "6"
key 5 (c) Black body with white scale patterns on thorax and legs
key 6 (c) Bites in the daytime, so nets alone do not protect: use repellent
```

Vector control is judged by **entomological indices**. The **house index** is the percentage of houses with larvae, the **container index** the percentage of water containers with larvae, and the **Breteau index (BI)** the number of positive containers per 100 houses. Malaria is monitored by the **slide positivity rate (SPR)** (positive slides per 100 examined) and the **annual parasite incidence (API)** (confirmed cases per 1000 population per year).

```python
# dengue survey: 80 houses, 10 with larvae, 60 containers of which 12 positive
houses, pos_houses, containers, pos_cont = 80, 10, 60, 12
print(f"House index = {pos_houses / houses * 100:.1f}%")
print(f"Container index = {pos_cont / containers * 100:.0f}%")
print(f"Breteau index = {pos_cont / houses * 100:.0f} per 100 houses")
# malaria: 400 slides, 36 positive; 45 cases in 15,000 people
print(f"Slide positivity rate = {36 / 400 * 100:.0f}%")
print(f"API = {45 / 15000 * 1000:.1f} per 1000")
# DOTS tablets for a 62 kg patient (4 FDC tablets a day)
ip, cp = 56 * 4, 112 * 4
print(f"Intensive phase = {ip} tablets, continuation = {cp} tablets, doses = {56 + 112}")
```

```text
House index = 12.5%
Container index = 20%
Breteau index = 15 per 100 houses
Slide positivity rate = 9%
API = 3.0 per 1000
Intensive phase = 224 tablets, continuation = 448 tablets, doses = 168
```

The survey gives a **house index of 12.5%**, a **container index of 20%** and a **Breteau index of 15**: a BI above 5 shows a risk of dengue spread, so the ward needs source reduction (empty, scrub, cover and dry containers weekly). The malaria area has an **SPR of 9%** and an **API of 3.0** per 1000. A 62-kg TB patient on 4 tablets a day takes **224** tablets in the 56-day intensive phase and **448** in the 112-day continuation phase, with **168 observed doses** in all; each missed dose is traced the same day.

## 3.5 Nursing responsibilities in an immunisation session: eight points

The monthly outreach or clinic session is the nurse's main chance to protect a whole birth cohort. These eight responsibilities are asked as a standard ten-mark question.

1. **Plan and prepare the session.** List the children due from the register and estimate vaccine with the wastage factor. Check that the vaccine carrier, four ice packs, syringes, safety box, cards and tally sheets are ready. Inform the FCHVs and mothers' group a day earlier so that the children come.
2. **Maintain the cold chain.** Keep vaccines at +2 °C to +8 °C, with the carrier closed except when taking a vial and the thermometer inside. Never freeze the pentavalent or PCV vials, and never keep vaccines with anything else. Check the VVM and the expiry date before every use.
3. **Screen the child and give the right dose.** Ask about fever, convulsions and earlier reactions, check the card, and find which vaccine is due. Mild illness, cough or diarrhoea is not a reason to postpone. Only a severe reaction to a previous dose is a true contraindication.
4. **Give the vaccine with a safe technique.** Wash hands, use one sterile syringe and needle for each child, and use the correct route and site: intradermal for BCG and fIPV, intramuscular in the thigh for pentavalent and PCV, subcutaneous for MR and JE. Never recap a needle; drop it into the safety box. Reconstituted BCG and MR vials are discarded after 6 hours.
5. **Give clear advice to the mother.** Say which diseases were prevented, the next visit date, and the usual mild effects such as fever and a sore leg. Advise paracetamol for fever and a cool cloth over the site. Tell her to return at once for convulsions, high fever or swelling that spreads.
6. **Record and report.** Write the date on the card, the register and the tally sheet before the child leaves, and mark the next date. Send the monthly report through HMIS and DHIS2. Accurate records are the base for coverage and dropout rates.
7. **Manage adverse events following immunisation (AEFI).** Keep adrenaline, a syringe and oxygen ready and observe each child for 30 minutes. Treat anaphylaxis with intramuscular adrenaline 0.01 mg/kg, and report any serious AEFI to the district within 24 hours. Most reactions are minor and need only reassurance.
8. **Dispose of waste and trace defaulters.** Collect used syringes in a safety box and dispose of it by burning and burying as per the health-care waste guideline. Give the list of children who missed doses to the FCHV and visit them within a week. Zero-dose children, those who never received a vaccine, are the first priority.

## Formula and fact sheet

- Chain of infection: agent, reservoir, exit, transmission, entry, host. Cold chain +2 to +8 °C; shake test for freeze-sensitive vaccines.
- NIP: BCG at birth; penta, OPV 6-10-14 weeks; PCV 6-10 weeks and 9 months; rotavirus 6-10 weeks; fIPV 14 weeks and 9 months; MR 9 and 15 months; JE 12 months; typhoid 15 months; Td in pregnancy.
- Vaccine efficacy = (ARU − ARV) ÷ ARU × 100. Herd immunity threshold = 1 − 1/R₀ (measles 93.3%).
- Wastage factor = 1 ÷ (1 − wastage rate); doses = target × doses per child × factor. Dropout = (first dose − last dose) ÷ first dose × 100.
- TB: 2HRZE + 4HR, 56 + 112 days. Breteau index = positive containers per 100 houses; SPR = positives per 100 slides; API = cases per 1000 per year.

## Chapter summary

- Immunisation, DOTS and vector control break the links of the chain of infection.
- The NIP gives free vaccines on a fixed schedule; the cold chain and correct technique protect their potency.
- Vaccine need is planned with the wastage factor; coverage and dropout show where children are missed.
- TB is found by Xpert or smear and cured by 6 months of observed treatment.
- Malaria and dengue are controlled by vector control, early diagnosis and community action; indices measure the risk.

## Practice

**MCQs (with reasons)**

1. The temperature range for vaccine storage is: (a) −15 to −25 °C (b) 0 to +2 °C (c) +2 to +8 °C (d) +8 to +15 °C.
2. The herd immunity threshold for measles with R₀ = 15 is about: (a) 50% (b) 83% (c) 93% (d) 99.9%.
3. A health post uses 840 BCG doses with 50% wastage. Doses to order are: (a) 840 (b) 1,260 (c) 1,680 (d) 2,520.
4. A TB patient on DOTS takes the continuation phase for: (a) 2 months (b) 4 months (c) 6 months (d) 9 months.
5. A Breteau index measures: (a) larvae per person (b) positive containers per 100 houses (c) houses with mosquitoes (d) parasite cases per 1000.

::: note Answers and rationales
**1. (c).** Vaccines are kept between +2 and +8 °C; below 0 °C freeze-sensitive vaccines lose potency, and above 8 °C all lose it.
**2. (c).** 1 − 1/15 = 93.3%; 83% is the threshold for polio (R₀ 6).
**3. (c).** Wastage factor = 1 ÷ (1 − 0.5) = 2, so 840 × 2 = 1,680 doses (84 vials of 20).
**4. (b).** DOTS has 2 months intensive and 4 months continuation (6 months in all).
**5. (b).** BI is positive containers per 100 houses; the house index is the percentage of houses with larvae.
:::

**Short answer (3 marks): Cold chain.** The cold chain is the system of storage and transport that keeps vaccines between +2 °C and +8 °C from the manufacturer to the child. It uses cold rooms, ice-lined refrigerators, cold boxes and vaccine carriers with frozen ice packs, with temperature recording twice a day. Freeze-sensitive vaccines are checked by the shake test and all vials by the VVM. Failure of the cold chain destroys potency, and children are left unprotected.

**Medium answer (5 marks): Explain the DOTS strategy for tuberculosis (Figure 3.2).** DOTS is the WHO strategy used in Nepal by the NTP. Its five elements are political commitment; diagnosis by Xpert MTB/RIF or sputum microscopy; standard short-course treatment with direct observation; a regular supply of quality drugs; and a recording and reporting system. A new patient takes 2 months of HRZE and then 4 months of HR in fixed-dose tablets by weight, with an observer (health worker, FCHV or family member) watching every dose. Smear is checked at the end of the intensive phase, in month 5 and at the end. The nurse registers the case, tests for HIV, traces contacts, counsels on completing treatment and finds defaulters on the same day. The outcome is recorded as cured, completed, failed, died, lost or not evaluated.

**Long answer (10 marks): In a ward of 1,200 children under 15 years, a measles outbreak is reported: 48 children have fever with rash, and 3 have died. Of the 900 vaccinated children, 12 fell ill; of the 300 unvaccinated, 36 fell ill. Calculate the rates and plan outbreak control and care.**

*Analysis.* The **overall attack rate** is 48 ÷ 1200 = **4.0%** and the **case fatality rate** is 3 ÷ 48 = **6.25%**. The attack rate in the vaccinated is 12 ÷ 900 = **1.33%** and in the unvaccinated 36 ÷ 300 = **12.0%**, so the **vaccine effectiveness** is (12.0 − 1.33) ÷ 12.0 = **88.9%**. The vaccine works well, but with 300 unprotected children (25%) the community is below the 93% needed for herd immunity, which allowed the outbreak. Measles spreads by airborne droplets and is infectious 4 days before to 4 days after the rash.

*Control.* Notify the district office the same day (EWARS), confirm with IgM serology on samples, line-list the cases and draw an epidemic curve. Isolate cases at home until 4 days after the rash, and vaccinate all children aged 6 months to 14 years in the ward within 72 hours (an outbreak-response campaign), with a fresh dose for those who are unvaccinated. Give **vitamin A 200,000 IU on days 1 and 2** (100,000 IU under 12 months), treat pneumonia and diarrhoea, feed well and continue breastfeeding. Educate families, work with FCHVs to find missed children and check the cold chain of the campaign.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** mother says "he has fever and red spots for 3 days, will not eat." **O:** temp 39.5 °C, maculopapular rash, cough, conjunctivitis, Koplik spots. | **Hyperthermia** related to viral infection, as evidenced by temperature 39.5 °C and flushed skin. | **Thermoregulation:** temperature below 38 °C in 24 hours. | 1. Tepid sponging, light clothes, paracetamol 15 mg/kg as ordered; *lowers temperature and comfort.* 2. Extra fluids and breastfeeding; *replaces fluid lost in fever.* 3. Monitor temperature every 4 hours; *detects convulsion risk.* | Temperature chart; goal met at below 38 °C. |
| **O:** vitamin A not taken in 6 months, weight 11 kg, loose stool twice. | **Risk for imbalanced nutrition: less than body requirements** and **risk for deficient fluid volume** related to anorexia and diarrhoea. | **Nutritional status:** intake of 3 small feeds a day and no dehydration in 3 days. | 1. Vitamin A 200,000 IU on days 1 and 2; *prevents eye damage and cuts mortality.* 2. ORS after each loose stool; *prevents dehydration.* 3. Small frequent soft feeds; *eases appetite and healing.* | Weigh at day 3 and day 7; check skin pinch. |
| **O:** 12 siblings and neighbours in close contact, 300 unvaccinated children in the ward. | **Risk for infection (spread)** related to non-immunised contacts and airborne transmission. | **Immunisation behaviour:** 95% of children aged 6 months-14 years vaccinated in 72 hours. | 1. Isolate cases for 4 days after rash; *breaks the chain.* 2. Ward-wide MR campaign with FCHVs; *restores herd immunity.* 3. Teach hand and cough hygiene and danger signs; *families act early.* | Coverage survey after the campaign; no new case for 2 incubation periods (about 3 weeks). |

::: tip Exam tip
In an outbreak question, always compute attack rate, case fatality and vaccine effectiveness first, then list control under source, transmission and susceptible, and finish with vitamin A and campaign details.
:::
