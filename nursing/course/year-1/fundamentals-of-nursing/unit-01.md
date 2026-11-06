---
subject: Fundamentals of Nursing
grade: BSc Nursing Year 1
unit: 1
title: Nursing as a Profession: History, Roles, Ethics and the Nepal Nursing Council
hours: 12
area: BSN 4 · Fundamentals of Nursing · Unit 1
---

Every nurse starts here: what nursing is, where it came from, what a nurse is allowed and expected to do, and which law and code protect both nurse and patient in Nepal. This unit is short on procedures but heavy on exam marks, because "Define nursing", "Roles of a nurse" and "Code of ethics" appear almost every year.

::: key What this unit gives you
- Definitions of nursing (Nightingale, Henderson, ICN) and its scope in prevention, promotion, cure and rehabilitation.
- Florence Nightingale and the timeline of nursing in Nepal (1956 school of nursing to the generic BSc).
- Eight roles of the nurse, each explained in plain words.
- The Nepal Nursing Council Act 2052 (1996), the NNC Code of Ethics and the seven ethical principles.
- A worked nursing-workload calculation (NHPPD) and full-length model answers with a NANDA-I care plan.
:::

## 1.1 What is nursing?

**Nightingale (1859):** nursing is "putting the patient in the best condition for nature to act upon him". **Virginia Henderson (1966):** the nurse helps the individual, sick or well, to perform activities that contribute to health, recovery or a peaceful death, which the person would do unaided if he had the strength, will or knowledge. **ICN (2002):** nursing covers autonomous and collaborative care of people of all ages, families, groups and communities, sick or well, in all settings; it includes promotion of health, prevention of illness, and care of the ill, disabled and dying, plus advocacy, a safe environment, research, health policy and education.

::: definition Nursing in one exam line
Nursing is both an **art** (caring, communication, touch), a **science** (evidence-based knowledge of body, mind and society) and a **profession** (a registered body of practitioners with a code of ethics and a licence to practise).
:::

**Scope.** Promotive (nutrition and hygiene teaching), preventive (immunisation under the National Immunisation Programme), curative (medicines, wound care), rehabilitative (mobility after stroke) and palliative care. The nurse works at a health post, a PHCC, a municipal hospital, a provincial hospital, and a federal centre such as Bir Hospital, TU Teaching Hospital, Patan, BPKIHS or Teku.

```photogrid label="1.1" cols="2" ratio="1.0" caption="Where nursing came from. (a) Florence Nightingale, founder of modern nursing (coloured lithograph, public domain). (b) Milestones of nursing in Nepal, from the first school of nursing to the generic BSc."
@ photo id="nur4/nightingale" cap="Florence Nightingale (1820-1910)"
fit 1.0
focus 0.5 0.4
call 0.50 0.93 0.50 0.72 "Lady with the Lamp"
@ svg cap="Nepal nursing timeline"
f = Fig(250, 330)
f.line(44, 14, 44, 316, color=SLATE, sw=2)
rows = [("1952", "Two women to India\nfor RN training (WHO)"), ("1956", "School of Nursing opens\n(now Maharajgunj)"),
        ("1972", "Nursing joins TU,\nInstitute of Medicine"), ("1976", "Post-basic BN begins\nat IOM"),
        ("1996", "NNC Act 2052:\nCouncil is set up"), ("2005", "Generic 4-year BSc\nstarts at IOM, KU")]
y = 32
for yr, t in rows:
    f.circle(44, y, 6, fill=TEAL, stroke=TEAL)
    f.text(20, y - 14, yr, size=11.5, color=NAVY, bold=True)
    f.text(58, y, t, size=11.5, color=SLATE, anchor="start", vmid=True)
    y += 50
```

## 1.2 Florence Nightingale and modern nursing

Nightingale nursed British soldiers in the Crimean War (1854-56), cut the hospital death rate by cleaning wards, ventilation, nutrition and records, and used statistics (the "coxcomb" chart) to persuade the government. In 1860 she opened the Nightingale School at St Thomas' Hospital, London. Her *Notes on Nursing* (1859) is the first nursing textbook. Henderson, Orem, Roy, Peplau and Watson later built the nursing theories you will meet in the second-year Nursing Concepts course.

## 1.3 Nursing in Nepal

Early maternity help came from birth attendants; a few Nepali women were sent to India for 18 months of midwifery training (sources date this between 1928 and 1936). In 1952 two women went to India for registered-nurse training on WHO scholarships, and in **1956** the first School of Nursing opened under the Ministry of Health (today Maharajgunj Nursing Campus). The Trained Nurses Association of Nepal formed in 1961. With the **1972** education plan, nursing moved to Tribhuvan University's Institute of Medicine; the post-basic BN started in 1976, the Master of Nursing in 1995 and the generic BSc in 2005. Formal nursing education admitted men from 1986. Today the BSc is entered through the MEC entrance (MECEE-BL).

## 1.4 Roles and functions of the nurse: eight points

1. **Caregiver.** The nurse meets physical needs such as hygiene, feeding, mobility and medicines, and emotional needs such as comfort and listening. Care is planned with the nursing process, not done at random. Good care keeps the patient safe, clean, dry and dignified.
2. **Communicator.** The nurse talks with patients, families and the team, and records and reports what happened. Clear handover prevents errors between shifts. Listening is part of communication, and so is silence.
3. **Teacher / health educator.** The nurse teaches diabetic foot care, safe drinking water, ORS preparation, family planning and breastfeeding. Teaching uses simple words and a demonstration. Health education is the cheapest way to prevent disease in Nepal.
4. **Advocate.** The nurse speaks for patients who cannot speak for themselves and protects their rights to information and consent. She reports unsafe practice. Advocacy is a duty in the NNC Code of Ethics.
5. **Counsellor.** The nurse helps a patient cope with a new diagnosis such as HIV, cancer or amputation. She gives emotional support without judging. She refers when the problem is beyond her competence.
6. **Manager / coordinator.** The nurse plans shift duties, supplies, beds and the work of the assistant staff. She coordinates with doctors, laboratory, pharmacy and community health workers. Good management makes the ward safe even when staff are few.
7. **Researcher.** The nurse questions old routines and uses evidence, for example about hand hygiene or wound dressing. She collects data and may take part in studies. Research turns experience into knowledge.
8. **Change agent / leader.** The nurse introduces better practice, from a new handover sheet to a local mothers' group. She leads by example. Nurses are the largest group of health workers in Nepal and so have the largest power to change care.

## 1.5 The Nepal Nursing Council (NNC)

The **Nepal Nursing Council Act 2052 (1996)** created the NNC, an autonomous statutory body, to regulate nursing education and practice. Its main functions are to fix the standards of nursing programmes, **register** qualified nurses (a licence is needed to practise), run the **licensing examination**, renew registration, discipline misconduct, and publish the **Code of Ethics**. Working without NNC registration is an offence. Every BSc graduate applies for registration, and the registration number goes on the nurse's identity card and on every drug chart she signs.

```svgfig label="1.1" caption="The seven ethical principles around the patient. Every ethical question on the ward is solved by asking which of these is at stake."
f = Fig(760, 300)
f.circle(380, 150, 52, fill=MINT, stroke=TEAL, label="Patient\ndignity", size=12, color=NAVY)
items = [("Autonomy\nright to decide", 40, 20), ("Beneficence\ndo good", 300, 8), ("Non-maleficence\ndo no harm", 560, 20),
         ("Justice\nfair share of care", 600, 125), ("Veracity\ntell the truth", 560, 232), ("Confidentiality\nkeep secrets", 300, 244), ("Fidelity\nkeep promises", 40, 232)]
for t, x, y in items:
    f.box(x, y, 170, 46, t, fill=BLUE, stroke=NAVY, size=10.5, color=NAVY)
    f.arrow([(x + 85 if abs(x - 380) > 120 else x + 85, y + (46 if y < 100 else 0)), (380 + (x - 300) * 0.28, 150 + (y - 150) * 0.30)], color=SLATE, sw=1.2)
```

**Code of Ethics (NNC), summary.** The nurse respects life and human dignity without discrimination by caste, sex, religion or politics; keeps patient information confidential; obtains informed consent; maintains competence through learning; reports unsafe practice; never accepts gifts that influence care; and upholds the honour of the profession. A breach can lead to warning, suspension or removal from the register.

::: example Worked example: nursing workload (NHPPD)
A 24-bed surgical ward runs at 75% occupancy. The recommended nursing time is 4.0 hours per patient per day (NHPPD). Patients = 24 × 0.75 = **18**; nursing hours per day = 18 × 4.0 = **72 h**; with 8-hour shifts that is 72 ÷ 8 = **9 nurse-shifts** per day (3 per shift if spread evenly). Add leave and sickness allowance on top when you roster.
:::

```svgfig label="1.2" caption="Levels of health care in Nepal and where the nurse works. Referral goes up the pyramid, feedback comes down."
f = Fig(760, 270)
tiers = [("Federal / specialised: Bir, TUTH, Teku, BPKIHS, Patan", 90, 20, 580), ("Provincial and district hospitals", 150, 78, 460), ("Municipal hospital, PHCC, urban health centre", 205, 136, 350), ("Health post and community units (FCHV, PHC outreach)", 255, 194, 250)]
cols = [ROSE, SAND, MINT, BLUE]
for (t, x, y, w), c in zip(tiers, cols):
    f.box(x + 40, y, w, 50, t, fill=c, stroke=NAVY, size=10.5, color=NAVY)
f.arrow([(40, 235), (40, 50)], color=TEAL, sw=2)
f.text(40, 250, "referral up", size=10.5, color=TEAL, bold=True)
f.arrow([(720, 50), (720, 235)], color=AMBER, sw=2)
f.text(720, 250, "feedback down", size=10.5, color=AMBER, bold=True)
```

## 1.6 Common exam traps

::: caution Common mistakes
- Writing "NNC Act 2053": the Act is **2052 (1996)**.
- Mixing up the **BSc** (generic, from 2005) with the post-basic **BN** (from 1976).
- Listing only "caregiver" as the nurse's role; the marks are in the eight roles.
:::

## Formula and fact sheet

- NHPPD: patients × NHPPD ÷ shift length = nurse-shifts per day.
- Nightingale 1860 (school), Nepal school of nursing 1956, TU/IOM 1972, NNC Act 2052 (1996), generic BSc 2005.
- Ethical principles: autonomy, beneficence, non-maleficence, justice, veracity, confidentiality, fidelity.

## Chapter summary

- Nursing is an art, a science and a regulated profession.
- Nepal's nursing began with the 1956 school and now offers diploma to PhD level.
- The nurse has eight roles; the NNC registers her and enforces the Code of Ethics.
- Ethical decisions rest on seven principles.

## Practice

**MCQs (with reasons)**

1. The Nepal Nursing Council Act was passed in: (a) 2042 (b) 2052 (c) 2062 (d) 2072.
2. Refusing to share a patient's HIV status with the neighbour is: (a) beneficence (b) justice (c) confidentiality (d) veracity.
3. A nurse who teaches ORS preparation to a mother is acting mainly as: (a) manager (b) educator (c) researcher (d) counsellor.
4. "Primum non nocere" corresponds to: (a) autonomy (b) non-maleficence (c) fidelity (d) justice.
5. The first School of Nursing in Nepal opened in: (a) 1928 (b) 1952 (c) 1956 (d) 1972.

::: note Answers and rationales
**1. (b).** The NNC Act 2052 (1996) created the Council. 2042 and 2062 are distractors; 2072 is the year of the 2015 earthquake era, unrelated.
**2. (c).** Confidentiality means protecting private health information. Veracity is truth-telling to the patient, not secrecy from others.
**3. (b).** Teaching is the educator role. A manager organises resources, a researcher collects data and a counsellor supports feelings.
**4. (b).** "First, do no harm" is non-maleficence. Beneficence is the positive duty to do good.
**5. (c).** The School of Nursing started in 1956. 1952 is when two women were sent abroad to train, and 1972 is the move to TU.
:::

**Short answer (3 marks): Write the functions of the Nepal Nursing Council.** The NNC is the statutory regulator under the NNC Act 2052. It (1) sets the standard of nursing curricula and recognises institutions, (2) registers qualified nurses and issues the licence, (3) conducts the licensing examination, (4) renews registration, (5) investigates complaints and punishes misconduct, and (6) publishes the Code of Ethics. Without registration nobody may practise as a nurse in Nepal.

**Medium answer (5 marks): Describe the roles of a nurse (see Figure 1.2 for where each role is practised).** The nurse is first a **caregiver**, giving hygiene, comfort, medicines and wound care through the nursing process. As **communicator** she records, reports and hands over so that care is continuous across shifts. As **teacher** she demonstrates ORS, hand washing and family planning. As **advocate** she protects the patient's right to consent and information. As **counsellor** she supports patients facing HIV, cancer or loss. As **manager** she organises beds, staff and supplies; as **researcher** she applies and produces evidence; as **change agent / leader** she introduces better practice. In a health post the nurse may perform all eight roles in one day, whereas in a federal hospital roles are more specialised. Example: a TUTH ward nurse who teaches a diabetic patient insulin self-injection is caregiver, teacher and advocate at once.

**Long answer (10 marks): Mr Ram Bahadur, 68, admitted to Bir Hospital with a gangrenous toe, refuses the doctor's advice of amputation. He understands the risks but says he wants to go home. Discuss the nurse's ethical responsibility and prepare a nursing care plan.**

*Ethical analysis.* This is a conflict between **autonomy** (a competent adult may refuse treatment) and **beneficence** (the team wants to save life). The nurse first checks that the patient is **competent** and that consent or refusal is **informed**: has the surgeon explained the diagnosis, the options (debridement, antibiotics, amputation) and the consequence of refusal (sepsis, death) in Nepali he understands? If not, she asks for the explanation again. She does not force, trick or threaten. She explores fear (loss of work, cost, body image, family), involves the family only with his permission (**confidentiality**), and documents the discussion honestly (**veracity**). If he still refuses, his choice is respected, he is offered the best alternative care, a refusal form is signed with a witness, and the nurse continues to give care without prejudice (**justice**, **fidelity**). She acts as **advocate** by telling the team of his concerns.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I will not lose my leg. Who will plough my field?" Fearful, worried about cost. **O:** Gangrenous left great toe, T 38.1 °C, pulse 98/min, anxious, asks to go home. | **Decisional conflict** related to unclear values and fear of amputation, as evidenced by refusal of surgery and verbalised uncertainty. | **Decision-making:** within 24 h the patient states the options and risks in his own words and makes a documented choice. | 1. Ensure private, quiet space and use Nepali; *trust grows when privacy is protected.* 2. Ask the surgeon to repeat the explanation with the nurse present; *informed choice needs understanding.* 3. Use teach-back to check understanding; *confirms comprehension.* 4. Explore fears and finances, refer to the medical social worker; *removing practical barriers often changes the decision.* 5. Involve family with his consent; *support without breaching confidentiality.* 6. Document and give a witnessed refusal form if he still declines; *legal and ethical record.* | Patient repeats the three options and states a choice. If he accepts, preoperative care starts; if he refuses, care continues and the plan is reviewed daily. |
| **O:** Painful, foul-smelling wound, dressing soaked. | **Risk for infection** (spread) related to gangrenous tissue. | **Infection severity:** temperature below 37.5 °C and no spreading redness in 72 h. | Aseptic dressing daily, give prescribed antibiotics on time, monitor temperature 4-hourly; *controls bacterial load and detects sepsis early.* | Temperature, pain and wound reviewed each shift. |

:::tip Exam tip
In ethics cases name the **principle in conflict** in the first line, then show the steps (competence, information, consent, documentation). Markers reward the structure more than the final decision.
:::
