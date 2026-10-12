---
subject: Health, Physical and Creative Arts
grade: 8
unit: 1
title: Human Body
hours: 4
area: Health Education
---

The human body works through connected systems. The nervous system receives information and coordinates responses. The reproductive system makes human reproduction possible and changes during adolescence. The endocrine system uses hormones to regulate growth, metabolism and reproduction. Understanding these systems helps us care for the body without fear, shame or misinformation.

::: key What the examination expects
Be able to label the main organs, state their functions, compare nervous and hormonal coordination, and explain healthy practices. Use accurate and respectful terms. A health lesson supports learning; it does not diagnose an illness.
:::

## 1.1 Nervous system

The **nervous system** receives information, interprets it and directs a response. Its basic working unit is the **neuron**, or nerve cell. A neuron has a cell body, branching dendrites that receive signals and a long axon that carries a signal away.

The nervous system has two major divisions:

| Division | Main parts | Main role |
|---|---|---|
| Central nervous system | brain and spinal cord | interprets information and coordinates responses |
| Peripheral nervous system | cranial and spinal nerves | carries messages between the central nervous system and the body |

### Brain

The brain is protected by the skull, three membranes called meninges and cerebrospinal fluid. Three parts are especially important at this level.

| Part | Function | Everyday example |
|---|---|---|
| Cerebrum | thinking, memory, sensation and voluntary movement | solving a problem or lifting a cup |
| Cerebellum | balance and coordination of muscles | cycling or walking on a narrow path |
| Medulla oblongata | controls involuntary activities | breathing and heartbeat |

```figure caption="Major parts of the human brain and their chief functions."
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0, 3.0))
ax.add_patch(Ellipse((3.2, 2.4), 4.3, 2.4, fc="#dbeafe", ec=ACCENT, lw=1.5))
ax.add_patch(Ellipse((4.65, 1.45), 1.3, 0.85, fc="#fed7aa", ec=SERIES[1], lw=1.3))
ax.plot([3.9, 4.15, 4.15], [1.45, 0.75, 0.25], color=SERIES[2], lw=4)
labels = [("Cerebrum\nthinking, memory, movement", 0.15, 3.6, (2.5, 2.65)),
          ("Cerebellum\nbalance and coordination", 0.15, 2.0, (4.65, 1.45)),
          ("Medulla\nbreathing and heartbeat", 0.15, 0.55, (4.12, 0.58))]
for text, tx, ty, target in labels:
    ax.text(tx, ty, text, fontsize=7, va="center", color=INK)
    ax.annotate("", xy=target, xytext=(tx + 2.1, ty), arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
ax.set_xlim(0, 6); ax.set_ylim(0, 4.2); ax.axis("off"); fig.tight_layout()
```

### Spinal cord and nerves

The spinal cord begins at the medulla and passes through the vertebral column. It carries impulses to and from the brain. It also coordinates many reflex actions. In humans, **31 pairs of spinal nerves** arise from the spinal cord. **Twelve pairs of cranial nerves** arise from the brain.

A **reflex action** is a rapid, automatic response to a stimulus. In a withdrawal reflex, a receptor detects danger, a sensory neuron carries the impulse to the spinal cord, a relay neuron passes it onward, and a motor neuron activates a muscle. The brain receives the information too, but the protective movement begins before conscious thought.

```figure caption="Reflex arc when a finger touches a hot surface."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 2.6))
items = [("Receptor", "detects heat"), ("Sensory neuron", "impulse inward"),
         ("Spinal cord", "relay neuron"), ("Motor neuron", "impulse outward"),
         ("Muscle", "hand withdraws")]
for i, (head, tail) in enumerate(items):
    x = i * 1.18
    ax.add_patch(FancyBboxPatch((x, 0.75), 0.98, 0.72, boxstyle="round,pad=0.04", fc="#ecfeff", ec=ACCENT, lw=1.1))
    ax.text(x + 0.49, 1.2, head, ha="center", fontsize=6.7, weight="bold", color=INK)
    ax.text(x + 0.49, 0.94, tail, ha="center", fontsize=6.1, color=MUTED)
    if i < len(items) - 1:
        ax.annotate("", xy=(x + 1.16, 1.1), xytext=(x + 1.0, 1.1), arrowprops=dict(arrowstyle="->", color=SERIES[1]))
ax.text(2.85, 0.25, "The brain is informed while the protective response begins.", ha="center", fontsize=7, color=MUTED)
ax.set_xlim(-0.1, 5.8); ax.set_ylim(0, 1.8); ax.axis("off"); fig.tight_layout()
```

::: example Following a reflex arc
**Situation.** Sita accidentally touches a hot cooking vessel and pulls her hand away.

**Explanation.** Heat receptors in her skin produce an impulse. A sensory neuron carries it to the spinal cord. A relay neuron transfers it to a motor neuron. The motor neuron makes the arm muscles contract, so the hand withdraws. The brain then interprets pain. This is a protective reflex, not a decision made after thinking.
:::

::: caution Protect the nervous system
Never test a reflex using flame, electricity, a sharp object or a blow. Wear a helmet when cycling, avoid diving into unknown water, and seek urgent medical help after a serious head or spinal injury. Do not move a person with a suspected spinal injury unless remaining in place is immediately dangerous.
:::

## 1.2 Reproductive system

The reproductive system produces reproductive cells and hormones and enables reproduction. During puberty, hormones cause the reproductive organs to mature. Puberty begins at different ages for different people; variation is normal.

### Male reproductive organs

| Organ | Main function |
|---|---|
| Testes | produce sperm and the hormone testosterone |
| Scrotum | holds the testes outside the body at a suitable temperature |
| Epididymis | stores and matures sperm |
| Sperm duct | carries sperm from the epididymis |
| Seminal vesicles and prostate gland | add fluids that nourish and protect sperm |
| Penis and urethra | provide a passage for semen; the urethra also carries urine at a different time |

### Female reproductive organs

| Organ | Main function |
|---|---|
| Ovaries | produce ova and the hormones oestrogen and progesterone |
| Oviducts | carry an ovum; fertilisation usually occurs here |
| Uterus | muscular organ where an embryo can develop |
| Cervix | narrow opening between uterus and vagina |
| Vagina | passage connecting the cervix to the outside of the body |

**Fertilisation** is the fusion of the nucleus of a sperm with the nucleus of an ovum, forming a zygote. It is different from implantation, which is the attachment of the developing embryo to the lining of the uterus.

::: example Correcting a common confusion
**Claim.** “A baby develops in the stomach.”

**Correction.** Food is digested in the stomach. After fertilisation, the developing embryo normally implants and grows in the uterus. The stomach and uterus are separate organs with different functions.
:::

Healthy reproductive care includes bathing with clean water, wearing clean underclothes, changing menstrual materials regularly, eating a balanced diet, and seeking qualified care for unusual pain, sores, discharge or other persistent symptoms. Medicines should not be taken on a friend’s advice.

Adolescents also protect these systems through enough sleep, regular physical activity, safe drinking water and avoidance of tobacco, alcohol and other harmful substances. Questions about body changes should be discussed with a trusted adult or trained health worker. Another person’s body and health information are private; curiosity never justifies teasing, touching without permission or spreading rumours.

## 1.3 Endocrine and glandular system

A **gland** is an organ or group of cells that produces a secretion. **Endocrine glands** have no ducts; they release hormones directly into the blood. **Exocrine glands** release their products through ducts, such as salivary and sweat glands. The pancreas is a **mixed gland** because it releases digestive juice through a duct and hormones into the blood.

A **hormone** is a chemical messenger made in a small amount, carried by blood and active in particular target organs.

| Gland | Hormone example | Main effect |
|---|---|---|
| Pituitary | growth hormone | supports body growth; also influences other glands |
| Thyroid | thyroxine | helps regulate metabolism; requires iodine for production |
| Pancreas | insulin and glucagon | helps regulate blood glucose |
| Adrenal glands | adrenaline | prepares the body for an emergency |
| Testes | testosterone | supports male reproductive development |
| Ovaries | oestrogen and progesterone | support female reproductive development and cycles |

Nervous and endocrine coordination work together. A nervous impulse is usually fast, brief and sent along a particular nerve. A hormone travels more slowly through blood, may reach many tissues and often has a longer-lasting effect.

::: example Nervous and hormonal response together
**Situation.** A dog suddenly runs toward Hari.

**Explanation.** Sensory nerves rapidly carry visual and sound information to his central nervous system. At the same time, adrenal glands release adrenaline. His heart beats faster, breathing increases and more blood reaches muscles. The nervous response is rapid and targeted; the hormonal response is slower but affects several organs.
:::

::: caution Hormones are not “strength medicines”
Hormones act in very small amounts. Too much or too little can disturb normal functions. Never use hormonal tablets, injections or bodybuilding products without a qualified clinician’s advice.
:::

## Chapter summary

- The central nervous system consists of the brain and spinal cord; peripheral nerves connect it with the body.
- The cerebrum supports thought, memory, sensation and voluntary movement; the cerebellum coordinates balance; the medulla controls vital involuntary actions.
- A reflex arc produces a rapid automatic response through receptor, sensory neuron, relay neuron, motor neuron and effector.
- Testes produce sperm and testosterone; ovaries produce ova, oestrogen and progesterone.
- Fertilisation usually occurs in an oviduct, while development after implantation occurs in the uterus.
- Endocrine glands release hormones directly into blood; exocrine glands release products through ducts.
- The pancreas is a mixed gland because it has both endocrine and exocrine functions.
- Nervous signals are generally rapid and brief; hormonal effects are generally slower and longer lasting.

## Practice questions

**Group A — Very short answer (1 mark each)**

1. How many pairs of spinal nerves arise from the spinal cord? <span class="marks">[1]</span>
2. Name the part of the brain mainly responsible for balance. <span class="marks">[1]</span>
3. Which two principal hormones are produced by the testes and ovaries respectively? <span class="marks">[1]</span>
4. Why is the pancreas called a mixed gland? <span class="marks">[1]</span>

::: note Answers to Group A
**1.** Thirty-one pairs.  
**2.** Cerebellum.  
**3.** Testosterone by the testes and oestrogen by the ovaries.  
**4.** It releases digestive juice through a duct and hormones directly into blood.
:::

**Group B — Short answer (2 marks each)**

1. Write two differences between nervous and hormonal coordination. <span class="marks">[2]</span>
2. State one function each of the cerebrum and medulla oblongata. <span class="marks">[2]</span>
3. Distinguish fertilisation from implantation. <span class="marks">[2]</span>
4. Write the path of an impulse in a withdrawal reflex. <span class="marks">[2]</span>

::: note Answer outlines to Group B
**1.** Nervous messages travel rapidly along nerves and are usually brief; hormones travel in blood more slowly and often act longer.  
**2.** Cerebrum: thought, memory, sensation or voluntary movement; medulla: heartbeat, breathing or another involuntary activity.  
**3.** Fertilisation is fusion of sperm and ovum, usually in an oviduct; implantation is attachment of the developing embryo to the uterine lining.  
**4.** Receptor → sensory neuron → relay neuron in spinal cord → motor neuron → muscle.
:::

**Group C — Long answer (4 marks each)**

1. Draw a labelled reflex arc and explain how it protects a person touching a hot object. <span class="marks">[4]</span>
2. Name four endocrine glands, give one hormone from each and state one function of each hormone. <span class="marks">[4]</span>

::: note Answer outlines to Group C
**1.** The diagram must show receptor, sensory neuron, spinal cord or relay neuron, motor neuron and muscle with arrows in the correct direction. Explain that the spinal pathway begins withdrawal rapidly while information also reaches the brain.  
**2.** Any four correct gland–hormone–function sets from the chapter table earn credit; each set must match correctly.
:::
