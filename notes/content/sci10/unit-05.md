---
subject: Science and Technology
grade: 10
unit: 5
title: Physiological Structure and Life Process
hours: 0
area: Science and Technology
---

Your body is a living machine of organ systems that work together. While you read this page, your eyes and brain are working, your heart is pumping blood, your kidneys are cleaning it and your hormones are keeping you alert or calm. This unit studies how the nervous and endocrine systems coordinate the body, how new human beings are born, how blood circulates, how waste is removed, and how the body keeps its inner conditions steady (homeostasis).

::: key What the SEE paper expects from this unit
This is the longest biology unit. Expect labelled diagrams (neuron, reflex arc, human heart, nephron or kidney), functions of glands and their hormones, the menstrual cycle, the path of blood through the heart (double circulation), blood groups, urine formation, and homeostasis of temperature and blood sugar. Draw and label every diagram at least once.
:::

## 5.1 Nervous and endocrine systems

The two systems of **coordination** keep the activities of the body working together and let it respond to changes (stimuli). The nervous system acts quickly through electrical signals; the endocrine system acts slowly through chemical messengers (hormones).

| Nervous system | Endocrine system |
|---|---|
| Messages are electrical impulses carried by nerves | Messages are chemicals (hormones) carried by blood |
| Very fast, in milliseconds | Slower, from seconds to days |
| Effect is short-lived | Effect lasts longer |
| Acts on a specific organ | May act on many organs |

### The nervous system

The nervous system is made of **neurons** (nerve cells). It has two main parts:

- **Central nervous system (CNS):** the **brain** and the **spinal cord**.
- **Peripheral nervous system (PNS):** the **nerves** that join the CNS to all parts of the body (12 pairs of cranial nerves from the brain and 31 pairs of spinal nerves from the spinal cord).

**Neuron.** A neuron has a **cell body** (with nucleus), short branches called **dendrites** that receive impulses, and a long **axon** that carries impulses away; the axon is often covered by an insulating **myelin sheath**. The end of the axon meets the next neuron at a gap called a **synapse**, which the impulse crosses by chemicals (neurotransmitters).

```figure caption="Structure of a neuron. The impulse travels from the dendrites through the cell body and along the axon to the axon terminals."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Ellipse
fig, ax = plt.subplots(figsize=(4.8,2.6))
ax.axis('off'); ax.set_xlim(0,14); ax.set_ylim(0,6)
ax.add_patch(Circle((3.0,3.0),0.9,fc="#cfe0ff",ec=ACCENT,lw=1.3))
ax.add_patch(Circle((3.0,3.0),0.35,fc=ACCENT,ec=ACCENT))
for a in (150,180,210,120,240):
    r=np.deg2rad(a)
    x1,y1=3.0+0.9*np.cos(r),3.0+0.9*np.sin(r)
    x2,y2=3.0+2.0*np.cos(r),3.0+2.0*np.sin(r)
    ax.plot([x1,x2],[y1,y2],color=ACCENT,lw=1.5)
    ax.plot([x2,x2+0.4*np.cos(r+0.5)],[y2,y2+0.4*np.sin(r+0.5)],color=ACCENT,lw=1.2)
    ax.plot([x2,x2+0.4*np.cos(r-0.5)],[y2,y2+0.4*np.sin(r-0.5)],color=ACCENT,lw=1.2)
ax.plot([3.9,12.0],[3.0,3.0],color=ACCENT,lw=2)
for x in np.arange(5.0,11.5,1.8):
    ax.add_patch(Ellipse((x,3.0),1.4,0.7,fc="#f3c34b",ec=INK,lw=0.8))
for dy in (-0.5,0,0.5):
    ax.plot([12.0,12.9],[3.0,3.0+dy],color=ACCENT,lw=1.3)
    ax.add_patch(Circle((12.95,3.0+dy),0.12,fc=ACCENT))
ax.annotate("Dendrites",xy=(1.4,4.2),xytext=(0.4,5.3),fontsize=8,color=INK,arrowprops=dict(arrowstyle="-",color=INK,lw=0.8))
ax.annotate("Cell body\n(with nucleus)",xy=(3.0,2.1),xytext=(3.0,0.6),fontsize=8,color=INK,ha='center',arrowprops=dict(arrowstyle="-",color=INK,lw=0.8))
ax.annotate("Axon",xy=(5.8,3.0),xytext=(5.2,4.7),fontsize=8,color=INK,ha='center',arrowprops=dict(arrowstyle="-",color=INK,lw=0.8))
ax.annotate("Myelin sheath",xy=(8.6,3.35),xytext=(8.6,4.9),fontsize=8,color=INK,ha='center',arrowprops=dict(arrowstyle="-",color=INK,lw=0.8))
ax.annotate("Axon terminals",xy=(12.9,3.0),xytext=(11.6,1.0),fontsize=8,color=INK,ha='center',arrowprops=dict(arrowstyle="-",color=INK,lw=0.8))
ax.annotate("direction of impulse",xy=(11.5,2.35),xytext=(5.2,2.35),fontsize=7.5,color=MUTED,va='center',arrowprops=dict(arrowstyle="->",color=MUTED,lw=1))
```

Neurons are of three kinds:

| Type | Function |
|---|---|
| **Sensory neuron** | Carries impulses from the sense organs (receptors) to the CNS |
| **Motor neuron** | Carries impulses from the CNS to muscles or glands (effectors) |
| **Relay (connecting) neuron** | Joins sensory and motor neurons inside the CNS |

### The brain

The brain is protected by the skull, by three membranes (meninges) and by a fluid (cerebrospinal fluid). It weighs about 1.4 kg and has three main parts.

| Part | Function |
|---|---|
| **Cerebrum** (the largest part, with two hemispheres) | Thinking, memory, intelligence, will, speech, seeing and hearing, voluntary movement |
| **Cerebellum** (behind and below the cerebrum) | Balance of the body, posture and smooth movement |
| **Medulla oblongata** (brain stem, joins the spinal cord) | Controls involuntary actions: heartbeat, breathing, swallowing, vomiting, blood pressure |

Other parts: the **thalamus** relays signals, and the **hypothalamus** controls body temperature, hunger and thirst and links the nervous system with the endocrine system through the pituitary gland.

### Spinal cord, reflex action

The **spinal cord** is a cord of nervous tissue about 45 cm long, inside the backbone. It carries impulses between the brain and the body and is the centre of **reflex actions**.

::: definition Reflex action
A **reflex action** is a quick, automatic response to a stimulus that does not need the will or thought. It is controlled by the spinal cord (or the brainstem) without waiting for the brain.
:::

Examples: pulling the hand away from a hot object; blinking when dust enters the eye; knee jerk; sneezing; coughing.

The path of a reflex action is the **reflex arc**:

**Stimulus → receptor (skin) → sensory neuron → spinal cord (relay neuron) → motor neuron → effector (muscle) → response.**

```figure caption="Reflex arc for withdrawing the hand from a hot object. The impulse reaches the spinal cord and returns without passing through the brain first."
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.6,3.0))
ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,7)
ax.add_patch(Circle((6,3.2),1.6,fc="#eef2f8",ec=INK,lw=1.2))
ax.add_patch(Circle((6,3.2),0.85,fc="#cfe0ff",ec=ACCENT,lw=1.0))
ax.text(6,5.2,"Spinal cord",ha='center',fontsize=8,color=INK)
ax.add_patch(Rectangle((0.3,1.3),1.9,0.9,fc="#ffd9c7",ec=INK,lw=1))
ax.text(1.25,0.7,"Receptor\n(skin)",ha='center',fontsize=8,color=INK,va='top')
ax.add_patch(Rectangle((9.8,1.3),1.9,0.9,fc="#d7f0d0",ec=INK,lw=1))
ax.text(10.75,0.7,"Effector\n(muscle)",ha='center',fontsize=8,color=INK,va='top')
ax.annotate("",xy=(4.6,2.9),xytext=(2.2,1.75),arrowprops=dict(arrowstyle="->",color=ACCENT,lw=1.8))
ax.annotate("",xy=(9.8,1.75),xytext=(7.4,2.9),arrowprops=dict(arrowstyle="->",color=SERIES[1],lw=1.8))
ax.text(3.4,3.6,"Sensory\nneuron",fontsize=8,color=ACCENT,ha='center')
ax.text(8.6,3.6,"Motor\nneuron",fontsize=8,color=SERIES[1],ha='center')
ax.text(6,3.2,"Relay\nneuron",fontsize=7,color=INK,ha='center',va='center')
ax.text(1.25,2.55,"1. Stimulus\n(heat)",fontsize=7.5,color=MUTED,ha='center')
ax.text(10.75,2.55,"5. Response\n(hand pulled)",fontsize=7.5,color=MUTED,ha='center')
```

::: caution Common mistake
Do not say that the brain controls a reflex action. The brain is informed afterwards (that is why you feel the pain after pulling your hand away). The reflex centre is the spinal cord. Reflex action is involuntary; walking or writing are voluntary actions.
:::

### Sense organs

The five sense organs are the **eye** (sight), **ear** (hearing and balance), **nose** (smell), **tongue** (taste) and **skin** (touch, pain, temperature). Each has receptors that turn a stimulus into an impulse.

### The endocrine system

The endocrine system is a set of **ductless glands** that make **hormones** and pour them straight into the blood. Hormones are chemical messengers; they work in tiny amounts and act on **target organs**.

| Gland | Position | Hormone | Function / disorder |
|---|---|---|---|
| **Pituitary** (master gland) | Base of the brain | Growth hormone (GH) | Growth of bones. Too little: dwarfism; too much: gigantism |
| | | TSH, ACTH, FSH, LH | Control other glands |
| | | ADH | Water absorption in kidney; lack causes diabetes insipidus |
| | | Oxytocin | Contraction of uterus at birth; milk release |
| **Thyroid** | Neck, in front of windpipe | Thyroxine (needs iodine) | Controls metabolism. Too little: goitre (in adults), cretinism (in children) |
| **Parathyroid** | Behind the thyroid | Parathormone | Keeps calcium level in blood |
| **Adrenal** | On top of each kidney | Adrenaline | "Fight, flight or fright": raises heartbeat and blood sugar |
| **Pancreas** | Below the stomach | Insulin, glucagon | Control blood sugar. Lack of insulin: diabetes mellitus |
| **Ovary** (female) | Lower abdomen | Oestrogen, progesterone | Female sex characters; menstrual cycle |
| **Testis** (male) | Scrotum | Testosterone | Male sex characters, sperm formation |

Diseases to remember: **goitre** (swollen neck from lack of iodine; prevented by iodised salt), **diabetes mellitus** (high blood sugar, from lack of insulin), **dwarfism** and **gigantism** (growth hormone).

::: tip The master gland
The **pituitary** is called the master gland because it controls most of the other glands. It is, in turn, controlled by the hypothalamus.
:::

## 5.2 Reproduction

**Reproduction** is the production of new individuals of the same kind. Humans reproduce **sexually**: a male gamete (sperm) fuses with a female gamete (egg or ovum) in **fertilisation**.

### Male reproductive system

| Organ | Function |
|---|---|
| **Testes** (a pair, in the scrotum) | Make sperms and the hormone testosterone. The scrotum keeps them about 2–3 °C cooler than the body |
| **Epididymis** | Stores sperms and lets them mature |
| **Vas deferens** | Tube carrying sperms from the epididymis |
| **Seminal vesicle, prostate gland** | Make a fluid that feeds the sperms; with the sperm it forms semen |
| **Urethra and penis** | Carry semen (and urine) out of the body |

### Female reproductive system

| Organ | Function |
|---|---|
| **Ovaries** (a pair) | Produce an egg about every 28 days; make oestrogen and progesterone |
| **Fallopian tubes (oviducts)** | Carry the egg to the uterus; **fertilisation takes place here** |
| **Uterus (womb)** | A pear-shaped muscular organ where the embryo grows |
| **Cervix** | The neck of the uterus |
| **Vagina** | Receives the sperm; the birth canal |

```figure caption="Female reproductive system, side view (schematic)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Circle
fig, ax = plt.subplots(figsize=(4.4,3.2))
ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,8)
ax.add_patch(Polygon([(4.6,6.4),(7.4,6.4),(6.9,3.3),(5.1,3.3)],fc="#f7c6c6",ec=INK,lw=1.2))
ax.add_patch(Polygon([(5.1,3.3),(6.9,3.3),(6.5,0.6),(5.5,0.6)],fc="#f0a8a8",ec=INK,lw=1.0))
ax.plot([4.6,3.4,2.5,2.2],[6.2,6.6,6.4,5.7],color=INK,lw=3.5,solid_capstyle='round',alpha=0.55)
ax.plot([7.4,8.6,9.5,9.8],[6.2,6.6,6.4,5.7],color=INK,lw=3.5,solid_capstyle='round',alpha=0.55)
ax.add_patch(Ellipse((1.9,5.1),1.1,1.3,fc="#f3c34b",ec=INK,lw=1))
ax.add_patch(Ellipse((10.1,5.1),1.1,1.3,fc="#f3c34b",ec=INK,lw=1))
ax.annotate("Fallopian tube\n(fertilisation)",xy=(3.0,6.5),xytext=(0.2,7.5),fontsize=8,color=INK,arrowprops=dict(arrowstyle="-",color=INK,lw=0.8),annotation_clip=False)
ax.annotate("Ovary",xy=(10.5,4.6),xytext=(10.9,2.9),fontsize=8,color=INK,arrowprops=dict(arrowstyle="-",color=INK,lw=0.8))
ax.annotate("Uterus",xy=(6.0,5.0),xytext=(8.2,7.6),fontsize=8,color=INK,arrowprops=dict(arrowstyle="-",color=INK,lw=0.8))
ax.annotate("Cervix",xy=(6.1,3.3),xytext=(8.6,2.4),fontsize=8,color=INK,arrowprops=dict(arrowstyle="-",color=INK,lw=0.8))
ax.annotate("Vagina",xy=(6.1,1.5),xytext=(8.4,0.8),fontsize=8,color=INK,arrowprops=dict(arrowstyle="-",color=INK,lw=0.8))
```

### Puberty, gametes and menstruation

At **puberty** (about 10–14 years in girls, 12–16 in boys), the sex hormones start the secondary sexual characters: in boys, deeper voice, beard and broad shoulders; in girls, breast development and wider hips. A girl begins to have the monthly **menstrual cycle** (first period = **menarche**), and it stops around the age of 45–50 (**menopause**).

### The menstrual cycle

The cycle averages **28 days** and is controlled by FSH and LH from the pituitary and oestrogen and progesterone from the ovary.

| Days | Event |
|---|---|
| 1–5 | **Menstruation**: the lining of the uterus breaks down and leaves the body with blood |
| 6–13 | The uterus lining rebuilds under oestrogen; an egg ripens in the ovary |
| About **14** | **Ovulation**: the ripe egg is released from the ovary (LH peak) |
| 15–28 | The uterus lining thickens under progesterone. If the egg is not fertilised, the hormone level falls and menstruation starts again |

If the egg is fertilised and settles in the uterus wall (**implantation**), menstruation stops and **pregnancy** begins.

```figure caption="The 28-day menstrual cycle. The uterus lining is shed in days 1 to 5, rebuilds, and keeps thickening after ovulation (day 14); if there is no pregnancy it breaks down again."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.7))
d=np.arange(0,29)
thick=np.where(d<=5, 1.5-0.2*d, 0.5+0.12*(d-5))
thick=np.where(d>5, 0.5+0.28*(np.minimum(d,22)-5)-0.0*d, thick)
thick=np.where(d>22, 5.26-0.8*(d-22), thick)
thick=np.clip(thick,0.3,5.2)
ax.fill_between(d,thick,color="#f7c6c6",alpha=0.9)
ax.plot(d,thick,color=SERIES[1],lw=1.5)
ax.axvspan(0,5,color=GRID,alpha=0.6)
ax.axvline(14,color=INK,ls='--',lw=1)
ax.text(2.5,5.2,"Menstruation",ha='center',fontsize=7.5,color=INK)
ax.text(14.4,5.3,"Ovulation (day 14)",fontsize=7.5,color=INK)
ax.set_xlim(0,28); ax.set_ylim(0,6)
ax.set_xlabel("Day of cycle",color=INK); ax.set_ylabel("Thickness of uterus\nlining (relative)",color=INK,fontsize=8)
ax.spines[['top','right']].set_visible(False)
```

::: example Worked example 5.1 (calculating dates)
**Problem.** A woman has a regular 28-day cycle and her last period started on 3 June. Find (a) the expected date of ovulation, (b) the date of the next period.

**Solution.**

(a) Ovulation is about day 14 of the cycle. Day 1 = 3 June, so day 14 = 3 June + 13 days = **16 June**.

(b) The next period starts on day 29 = 3 June + 28 days = **1 July**. (June has 30 days: 3 + 28 = 31, which is 1 July.)
:::

### Fertilisation, pregnancy and birth

1. **Fertilisation:** a sperm fuses with the egg in the fallopian tube to form a **zygote** (2n = 46).
2. The zygote divides repeatedly while moving to the uterus and sinks into the lining (**implantation**) after about 6–7 days. It is now an **embryo**.
3. The **placenta** forms from the embryo and the uterine wall. Through it the mother gives food and oxygen to the baby and takes away wastes; the **umbilical cord** joins the baby to the placenta.
4. The baby floats in the **amniotic fluid** inside the amniotic sac, which protects it from shocks. After the eighth week it is called a **foetus**.
5. **Gestation** lasts about 9 months (about 280 days or 40 weeks). The birth (**parturition**) is helped by oxytocin; the mother's body then makes milk (prolactin).

After birth the mother's breast milk is the best food for the baby, as it has the right nutrients and antibodies.

### Twins

**Identical twins** form when one fertilised egg splits into two embryos; they have the same sex and genes. **Fraternal twins** form from two eggs fertilised by two sperms; they may be of different sex and look no more alike than other brothers and sisters.

### Family planning and reproductive health

Birth control (contraception) methods: barrier methods (condom), hormonal pills and injections, the intrauterine device (copper-T), and surgical methods (vasectomy in men, tubectomy in women). **Condoms** also protect from sexually transmitted infections (STIs) such as HIV/AIDS, syphilis and gonorrhoea. Early marriage and teenage pregnancy are dangerous to the health of both mother and child; in Nepal the legal age of marriage is 20 years. Healthy habits, correct knowledge and regular health check-ups protect reproductive health.

## 5.3 Circulation

The **circulatory system** carries oxygen, digested food, hormones and waste products around the body. It has **blood** (the fluid), the **heart** (the pump) and **blood vessels** (the pipes).

### Blood

An adult has about **5 litres** of blood, which is about 7–8% of the body mass. Blood is made of a liquid, **plasma** (about 55%), and cells (about 45%).

| Component | Feature | Function |
|---|---|---|
| **Plasma** | Pale yellow liquid, 90% water | Carries food, hormones, wastes (urea), carbon dioxide |
| **Red blood cells (RBC, erythrocytes)** | Biconcave discs, no nucleus, contain haemoglobin; 4.5–5.5 million per mm³; live about 120 days; made in the bone marrow | Carry oxygen (as oxyhaemoglobin) |
| **White blood cells (WBC, leucocytes)** | Larger, with a nucleus; 5,000–10,000 per mm³ | Fight germs by eating them or making antibodies |
| **Platelets (thrombocytes)** | Cell fragments; 1.5–4 lakh per mm³ | Help the blood to clot at a wound |

Haemoglobin is an iron-containing red pigment. Lack of iron or of haemoglobin causes **anaemia**. Green vegetables, liver, beans and jaggery (*sakhar*) are rich in iron.

**Blood groups.** In 1901 **Karl Landsteiner** found the **ABO** blood groups, based on the antigens (A, B) on the red cells and antibodies in the plasma. A person with **group O** can donate to all (universal donor) and one with **group AB** can receive from all (universal recipient). The **Rh factor** is another antigen: people with it are Rh⁺, those without are Rh⁻.

| Blood group | Antigen on RBC | Antibody in plasma | Can donate to | Can receive from |
|---|---|---|---|---|
| A | A | anti-B | A, AB | A, O |
| B | B | anti-A | B, AB | B, O |
| AB | A and B | none | AB | A, B, AB, O |
| O | none | anti-A and anti-B | A, B, AB, O | O |

### The heart

The heart is a muscular organ about the size of a fist, between the lungs, a little to the left. It has **four chambers**:

- two upper **atria** (auricles), which receive blood;
- two lower **ventricles**, which pump blood out. The left ventricle has a thicker wall because it pumps blood to the whole body.

**Valves** between atria and ventricles (the bicuspid valve on the left and the tricuspid valve on the right) and at the exits of the ventricles prevent blood from flowing backwards. The heart makes the "lub-dub" sound when the valves close.

The right side carries **deoxygenated** blood and the left side **oxygenated** blood; the septum keeps them from mixing.

| Vessel | Carries blood | From → to |
|---|---|---|
| **Vena cava** (superior and inferior) | Deoxygenated | Body → right atrium |
| **Pulmonary artery** | Deoxygenated | Right ventricle → lungs |
| **Pulmonary vein** | Oxygenated | Lungs → left atrium |
| **Aorta** | Oxygenated | Left ventricle → body |

```figure caption="Plan of the human heart showing the four chambers, the main vessels and the direction of blood flow (red: oxygenated, blue: deoxygenated)."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.6,3.6))
ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,9.4)
BL="#6f9bd8"; RD="#e57373"
ax.add_patch(Rectangle((2.2,4.7),3.3,2.0,fc="#bcd3f2",ec=INK,lw=1.2))
ax.add_patch(Rectangle((6.5,4.7),3.3,2.0,fc="#f6c4c4",ec=INK,lw=1.2))
ax.add_patch(Rectangle((2.2,1.6),3.3,3.0,fc="#9fbfe8",ec=INK,lw=1.2))
ax.add_patch(Rectangle((6.5,1.6),3.3,3.0,fc="#f0a8a8",ec=INK,lw=1.2))
ax.text(3.85,5.7,"Right\natrium",ha='center',va='center',fontsize=8,color=INK)
ax.text(8.15,5.7,"Left\natrium",ha='center',va='center',fontsize=8,color=INK)
ax.text(3.85,3.1,"Right\nventricle",ha='center',va='center',fontsize=8,color=INK)
ax.text(8.15,3.1,"Left\nventricle",ha='center',va='center',fontsize=8,color=INK)
ax.plot([5.9,5.9],[1.6,6.7],color=INK,lw=2)
ax.annotate("",xy=(3.85,6.7),xytext=(3.85,8.6),arrowprops=dict(arrowstyle="->",color=BL,lw=2.2))
ax.text(3.85,9.0,"From body\n(vena cava)",ha='center',fontsize=7.5,color=INK,va='bottom')
ax.annotate("",xy=(0.9,8.0),xytext=(2.2,3.6),arrowprops=dict(arrowstyle="->",color=BL,lw=2.2,connectionstyle="arc3,rad=-0.2"))
ax.text(0.2,8.5,"To lungs\n(pulmonary artery)",ha='left',fontsize=7.5,color=INK,va='bottom')
ax.annotate("",xy=(8.15,6.7),xytext=(11.2,8.0),arrowprops=dict(arrowstyle="->",color=RD,lw=2.2))
ax.text(11.9,8.4,"From lungs\n(pulmonary vein)",ha='right',fontsize=7.5,color=INK,va='bottom')
ax.annotate("",xy=(10.6,1.2),xytext=(9.4,3.2),arrowprops=dict(arrowstyle="->",color=RD,lw=2.2))
ax.text(10.7,0.5,"To body (aorta)",ha='center',fontsize=7.5,color=INK)
ax.text(5.9,0.9,"Septum",ha='center',fontsize=7.5,color=MUTED)
```

### Blood vessels

| Feature | Artery | Vein | Capillary |
|---|---|---|---|
| Direction | Away from heart | Towards heart | Between artery and vein |
| Wall | Thick, elastic | Thin | One cell thick |
| Valves | Absent | Present | Absent |
| Blood pressure | High | Low | Falling |
| Blood (usually) | Oxygenated (except the pulmonary artery) | Deoxygenated (except the pulmonary vein) | Exchange of food, oxygen and waste with cells |

### Double circulation

In human beings the blood passes **twice** through the heart in one complete round, so it is called **double circulation**.

1. **Pulmonary circulation:** right ventricle → pulmonary artery → lungs (blood gets oxygen) → pulmonary vein → left atrium.
2. **Systemic circulation:** left ventricle → aorta → body → vena cava → right atrium.

William Harvey (1628) first described the circulation of blood.

### Pulse, heartbeat and blood pressure

- **Heartbeat.** A resting adult heart beats about **72 times a minute**. The **pulse** felt at the wrist is the stretch of an artery with each beat.
- **Blood pressure** is the force of blood on the vessel wall. Normal adult value is about **120/80 mm Hg** (systolic/diastolic), measured with a sphygmomanometer.
- **Stroke volume** is the blood pumped by one ventricle in one beat (about 70 mL). **Cardiac output** = heart rate × stroke volume.

::: example Worked example 5.2 (cardiac output)
**Problem.** The heart of a resting man beats 72 times per minute and pumps 70 mL of blood at each beat from the left ventricle. Find (a) the volume of blood pumped in one minute, and (b) in one day.

**Solution.**

(a) Cardiac output = 72 × 70 mL = 5,040 mL per minute ≈ **5.04 litres per minute**.

(b) In one day: 5.04 L × 60 × 24 = 5.04 × 1,440 = **7,257.6 litres** (about 7,260 litres).
:::

### Heart diseases and care

- **High blood pressure (hypertension):** caused by stress, too much salt and fat, lack of exercise.
- **Atherosclerosis and heart attack:** fat deposits narrow the arteries and a clot blocks the blood flow to the heart muscle.
- **Stroke:** blockage or bursting of a blood vessel in the brain.

Care: regular exercise, less salt and oil, no smoking, no alcohol, healthy weight, and regular check-ups.

### Lymphatic system

Some fluid leaks out of capillaries to the tissues (tissue fluid). The extra fluid returns to the blood as **lymph**, which flows through thin vessels with **lymph nodes**. Lymph carries fats from the intestine and white cells help to fight infection in the nodes.

## 5.4 Excretion

**Excretion** is the removal of the waste products of metabolism from the body.

| Organ | Excretory product |
|---|---|
| **Kidneys** | Urea, uric acid, excess water and salts (in urine) |
| **Lungs** | Carbon dioxide and water vapour |
| **Skin** | Water, salts and a little urea (in sweat) |
| **Liver** | Bile pigments (from the breakdown of haemoglobin); makes urea from ammonia |

### The urinary system

The **urinary system** has two **kidneys**, two **ureters**, one **urinary bladder** and one **urethra**.

- **Kidneys:** bean-shaped organs about 10 cm long, on either side of the backbone, just under the ribs; they filter the blood.
- **Ureter:** a tube from each kidney to the bladder.
- **Urinary bladder:** a muscular bag that stores urine (up to about 400–500 mL comfortably).
- **Urethra:** carries urine out of the body.

### The nephron

Each kidney has about **one million nephrons**, the structural and functional units of the kidney. A nephron has:

- the **Bowman's capsule**, a cup around a cluster of capillaries called the **glomerulus**;
- a long coiled **renal tubule**: the proximal convoluted tubule, the loop of Henle and the distal convoluted tubule, which opens into a **collecting duct**.

```figure caption="A nephron (schematic): filtration in the glomerulus and Bowman's capsule, reabsorption along the tubule, and urine passing to the collecting duct."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.6,3.4))
ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,9)
ax.add_patch(Circle((3.0,6.7),1.0,fc="#fde7e7",ec=INK,lw=1.2))
t=np.linspace(0,6*np.pi,100)
ax.plot(3.0+0.3*np.cos(t), 6.7+0.3*np.sin(t*1.3), color=SERIES[1], lw=1.4)
ax.plot([2.4,2.4,1.5],[7.55,8.1,8.1],color=SERIES[1],lw=2.2)
ax.plot([3.6,3.6,4.5],[7.55,8.1,8.1],color=SERIES[0],lw=2.2)
ax.plot([3.0,3.0],[5.7,5.2],color=INK,lw=2.2)
xs=np.linspace(1.6,4.6,40); ax.plot(xs,4.9+0.35*np.sin(xs*7),color=INK,lw=2.2)
ax.plot([4.6,5.6],[4.9,4.9],color=INK,lw=2.2)
ax.plot([5.6,5.6],[4.9,1.8],color=INK,lw=2.2)
ax.plot([5.6,6.4],[1.8,1.8],color=INK,lw=2.2)
ax.plot([6.4,6.4],[1.8,5.6],color=INK,lw=2.2)
xs=np.linspace(6.4,8.6,30); ax.plot(xs,5.6+0.3*np.sin((xs-6.4)*7),color=INK,lw=2.2)
ax.plot([8.6,9.6,9.6],[5.6,5.6,2.0],color=INK,lw=3.0)
ax.annotate("Glomerulus",xy=(3.1,6.8),xytext=(6.0,7.3),fontsize=8,color=INK,arrowprops=dict(arrowstyle="-",color=INK,lw=0.8))
ax.annotate("Bowman's\ncapsule",xy=(2.1,6.2),xytext=(0.1,6.0),fontsize=8,color=INK,ha='left',va='top',arrowprops=dict(arrowstyle="-",color=INK,lw=0.8))
ax.text(0.1,8.85,"Afferent\narteriole",fontsize=7.5,color=SERIES[1],va='top')
ax.text(4.6,8.85,"Efferent\narteriole",fontsize=7.5,color=SERIES[0],va='top')
ax.text(0.1,3.8,"Proximal tubule",fontsize=8,color=INK)
ax.text(5.9,0.9,"Loop of Henle",fontsize=8,color=INK)
ax.text(7.0,6.5,"Distal tubule",fontsize=8,color=INK)
ax.text(9.9,3.6,"Collecting\nduct\n(to ureter)",fontsize=8,color=INK)
```

### Urine formation

Urine is made in three steps.

1. **Ultrafiltration** (in the glomerulus): blood in the glomerulus is under high pressure. Water, glucose, salts, amino acids and urea pass into Bowman's capsule. Blood cells and big proteins remain in the blood. About **180 litres** of filtrate is formed per day.
2. **Selective reabsorption** (in the tubule): useful substances (all the glucose, most of the water, amino acids and salts) go back into the blood.
3. **Tubular secretion:** extra wastes (urea, excess salts, drugs) are added to the filtrate by the tubule.

The fluid that reaches the collecting duct is **urine**: about **1.5 litres per day**, pale yellow (the colour is from the pigment urochrome), made of about 95% water, 2% urea and 3% salts and other wastes.

::: example Worked example 5.3 (reabsorption)
**Problem.** The kidneys of a person filter 180 litres of fluid per day and produce 1.5 litres of urine. What percentage of the filtrate is reabsorbed?

**Solution.** Reabsorbed volume = 180 − 1.5 = 178.5 litres.

Percentage = (178.5 / 180) × 100 = **99.2%**.

Only about 0.8% of the filtrate leaves as urine.
:::

### Kidney problems and dialysis

- **Kidney stones:** hard deposits of salts (calcium oxalate) in the kidney or ureter; they cause severe pain. Drinking enough water helps to prevent them.
- **Kidney failure:** the kidneys stop cleaning the blood. Urea builds up in the blood. Treatment is **dialysis** (**haemodialysis**), where the patient's blood passes through a machine with a membrane that removes urea and extra salts and returns the clean blood, or a **kidney transplant** from a donor. Nepal has dialysis and transplant centres, such as the Tribhuvan University Teaching Hospital in Kathmandu.

### Role of the skin and liver

The skin sweats to cool the body, and removes some water and salts. The liver changes harmful ammonia into urea and breaks down old red cells.

## 5.5 Homeostasis

::: definition Homeostasis
**Homeostasis** is the maintenance of a constant internal environment in the body (temperature, water, salts, blood sugar and pH) in spite of changes outside.
:::

Homeostasis works by **negative feedback**: when a condition goes away from its normal value, the body reacts to bring it back. Receptors detect the change, a control centre (often the brain) processes it, and effectors (muscles, glands) correct it.

### Temperature regulation

The normal human body temperature is about **37 °C** (98.6 °F). The control centre is the **hypothalamus**.

| When it is hot | When it is cold |
|---|---|
| Sweat glands make more sweat; evaporation cools the skin | Sweating stops |
| Blood vessels in the skin widen (**vasodilation**), so more heat is lost | Blood vessels in the skin narrow (**vasoconstriction**), so less heat is lost |
| Hair lies flat | Hairs stand up (goose bumps) to trap warm air |
| Less food and activity | **Shivering** makes heat; adrenaline and thyroxine increase metabolism |

```figure caption="Negative feedback in temperature control. A change from 37 C is detected and corrected so that the temperature returns to normal."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,3.0))
ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,7.4)
def bx(x,y,t,w=3.4,fc="#eaf1ff",fs=8):
    ax.add_patch(FancyBboxPatch((x-w/2,y-0.45),w,0.9,boxstyle="round,pad=0.04",fc=fc,ec=ACCENT,lw=1))
    ax.text(x,y,t,ha='center',va='center',fontsize=fs,color=INK)
def ar(x1,y1,x2,y2):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",color=INK,lw=1.1))
bx(6,6.7,"Normal body temperature 37 C",w=5.0,fc="#dbe8ff")
bx(2.6,4.6,"Body too hot",fc="#ffe0d6"); bx(9.4,4.6,"Body too cold",fc="#d6e8ff")
ar(5.0,6.2,3.0,5.1); ar(7.0,6.2,9.0,5.1)
bx(2.6,2.9,"Hypothalamus detects;\nsweating, vasodilation",w=4.6,fs=7.5)
bx(9.4,2.9,"Hypothalamus detects;\nshivering, vasoconstriction",w=4.6,fs=7.5)
ar(2.6,4.15,2.6,3.4); ar(9.4,4.15,9.4,3.4)
bx(2.6,1.2,"Temperature falls",fc="#e3f4e3",w=3.4); bx(9.4,1.2,"Temperature rises",fc="#e3f4e3",w=3.4)
ar(2.6,2.45,2.6,1.7); ar(9.4,2.45,9.4,1.7)
ax.annotate("",xy=(4.6,1.2),xytext=(7.4,1.2),arrowprops=dict(arrowstyle="<->",color=MUTED,lw=1))
```

### Control of blood sugar

The normal blood glucose level is about **70–110 mg per 100 mL** (fasting). The **pancreas** keeps it steady:

| Condition | Pancreas releases | Effect |
|---|---|---|
| Blood sugar high (after a meal) | **Insulin** | Liver and muscles take up glucose and store it as glycogen; sugar falls |
| Blood sugar low (hungry) | **Glucagon** | Liver changes glycogen back to glucose; sugar rises |

If insulin is lacking or does not work, blood sugar stays high: **diabetes mellitus**. Signs: much urine, thirst, tiredness, weight loss. Treatment: diet, exercise, tablets or insulin injections.

### Water and salt balance

The kidney controls water balance under the control of **ADH** from the pituitary. When the body has too little water (hot day, little drinking), the blood becomes concentrated and the pituitary releases more ADH; the kidney reabsorbs more water and passes a **small amount of dark urine**. When we drink much water, less ADH is released and a **large amount of pale urine** is passed.

### Other homeostatic organs

| Organ | Role |
|---|---|
| Brain (hypothalamus) | Temperature, thirst, hunger |
| Kidney | Water, salts, pH, removal of urea |
| Pancreas | Blood glucose |
| Liver | Stores glucose; removes toxins |
| Lungs | Oxygen and carbon dioxide levels |
| Skin | Temperature, water loss |

::: caution Common mistake
Do not confuse **excretion** (removal of metabolic wastes such as urea and CO₂) with **egestion** (removal of undigested food, as faeces). Also, sweating does not warm the body; it is the **evaporation** of sweat that cools it.
:::

## Chapter summary

- The CNS (brain + spinal cord) and the PNS (nerves) coordinate quickly using electrical impulses; the endocrine glands coordinate slowly using hormones.
- Neuron: dendrites, cell body, axon, myelin sheath. Reflex arc: receptor → sensory neuron → spinal cord → motor neuron → effector.
- Brain: cerebrum (thinking), cerebellum (balance), medulla (involuntary actions). Pituitary is the master gland; thyroxine needs iodine; insulin controls blood sugar.
- Human reproduction: sperm and egg meet in the fallopian tube; the zygote implants in the uterus; gestation about 280 days. Menstrual cycle 28 days, ovulation about day 14.
- Blood = plasma + RBC (oxygen) + WBC (defence) + platelets (clotting). Blood groups A, B, AB, O.
- Heart has four chambers; double circulation (pulmonary and systemic). Cardiac output = heart rate × stroke volume; normal BP 120/80 mm Hg.
- Nephron: filtration (glomerulus), reabsorption (tubule), secretion; about 180 L filtered and 1.5 L urine per day. Dialysis treats kidney failure.
- Homeostasis: constant internal conditions by negative feedback: body temperature 37 °C (hypothalamus), blood glucose (insulin and glucagon), water (ADH).

## Practice questions

**Group A — Objective questions (1 mark each)**

1. The part of the brain that controls balance of the body is the <span class="marks">[1]</span>
   (a) cerebrum (b) cerebellum (c) medulla oblongata (d) thalamus
2. The hormone that lowers blood sugar is <span class="marks">[1]</span>
   (a) glucagon (b) adrenaline (c) insulin (d) thyroxine
3. Fertilisation in human beings takes place in the <span class="marks">[1]</span>
   (a) uterus (b) ovary (c) fallopian tube (d) vagina
4. The blood vessel that carries oxygenated blood from the lungs to the heart is the <span class="marks">[1]</span>
   (a) pulmonary artery (b) pulmonary vein (c) aorta (d) vena cava
5. The functional unit of the kidney is the <span class="marks">[1]</span>
   (a) neuron (b) nephron (c) glomerulus (d) ureter
6. The blood group known as the universal donor is <span class="marks">[1]</span>
   (a) A (b) B (c) AB (d) O

::: note Answers to Group A
**1.** (b) — the cerebellum controls balance and posture.
**2.** (c) — insulin lowers blood glucose; glucagon raises it.
**3.** (c) — the egg is fertilised in the fallopian tube.
**4.** (b) — the pulmonary vein is the one vein with oxygenated blood.
**5.** (b) — each kidney has about a million nephrons.
**6.** (d) — group O has no A or B antigens.
:::

**Group B — Short answer (2 marks each)**

1. What is a reflex action? Give two examples. <span class="marks">[2]</span>
2. Why is the pituitary called the master gland? <span class="marks">[2]</span>
3. Write the functions of the placenta. <span class="marks">[2]</span>
4. Differentiate between an artery and a vein (two points). <span class="marks">[2]</span>
5. Define homeostasis. How does sweating help in homeostasis? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A reflex action is a quick, automatic response to a stimulus controlled by the spinal cord without thinking. Examples: pulling the hand from a hot object; blinking.
**2.** It controls the work of many other endocrine glands (thyroid, adrenal, gonads) through its hormones.
**3.** It supplies food and oxygen from the mother to the foetus, removes carbon dioxide and wastes, and makes hormones.
**4.** An artery carries blood away from the heart; its wall is thick and it has no valves. A vein carries blood to the heart; its wall is thin and it has valves.
**5.** Homeostasis is the keeping of a constant internal environment. Sweat evaporates from the skin and takes heat from the body, so the temperature stays near 37 °C.
:::

**Group C — Long answer (4 marks each)**

1. Draw and label a neuron. Describe the path of a reflex arc. <span class="marks">[4]</span>
2. Describe the 28-day menstrual cycle. <span class="marks">[4]</span>
3. A person's heart beats 75 times per minute and pumps 68 mL per beat. Calculate the cardiac output in litres per minute and the blood pumped in one hour. <span class="marks">[4]</span>
4. Explain how urine is formed in the nephron. <span class="marks">[4]</span>
5. Describe how blood sugar is kept constant in the body. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Neuron: dendrites, cell body with nucleus, axon with myelin sheath, axon terminals. Reflex arc: stimulus → receptor → sensory neuron → spinal cord (relay neuron) → motor neuron → effector (muscle) → response.
**2.** Days 1–5: menstruation. Days 6–13: the uterus lining rebuilds and an egg ripens under FSH and oestrogen. Day 14: ovulation. Days 15–28: the lining thickens under progesterone; if there is no fertilisation, hormone levels fall and menstruation begins again.
**3.** Cardiac output = 75 × 68 = 5,100 mL = 5.1 L per minute. In one hour: 5.1 × 60 = 306 litres.
**4.** Ultrafiltration of blood in the glomerulus to Bowman's capsule (about 180 L/day); selective reabsorption of glucose, water, amino acids and salts in the tubule; tubular secretion of extra wastes. The remaining fluid is urine (about 1.5 L/day), sent to the bladder via the ureter.
**5.** When blood sugar rises after a meal, the pancreas releases insulin and the liver stores glucose as glycogen. When blood sugar falls, the pancreas releases glucagon and the liver turns glycogen into glucose. This is negative feedback; lack of insulin causes diabetes.
:::
