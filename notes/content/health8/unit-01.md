---
subject: Health, Physical and Creative Arts
grade: 8
unit: 1
title: 'Unit 1: Human Body'
hours: 8
area: Units
---

Your body works as connected systems. The nervous system receives information and coordinates responses, the endocrine system releases chemical messengers, and the reproductive system changes through puberty. Learning these systems accurately supports health, respect and safe choices.

::: key What success looks like
You can describe the basic role of the brain, spinal cord and nerves; explain that hormones carry chemical messages; and discuss puberty and reproductive health using respectful, factual language.
:::

## 1.1 Nervous system: receive, decide, respond

The nervous system helps the body notice changes and respond. The **brain** processes information, the **spinal cord** carries messages and helps with some quick reflexes, and **nerves** connect these centres with the rest of the body.

```figure caption="A simplified signal path: receptor to nervous system to response."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 2.25))
items = [('Receptor', 'skin or eye'), ('Sensory nerve', 'message in'), ('Brain / spinal cord', 'process'), ('Motor nerve', 'message out'), ('Muscle', 'response')]
for index, (title, detail) in enumerate(items):
    x = index * 1.16
    ax.add_patch(FancyBboxPatch((x, 0.72), 0.94, 0.5, boxstyle='round,pad=0.03', fc='#e9f3fb', ec=ACCENT, lw=1.0))
    ax.text(x + 0.47, 1.01, title, ha='center', va='center', fontsize=7.5, weight='bold')
    ax.text(x + 0.47, 0.37, detail, ha='center', va='center', fontsize=7.3, color=MUTED)
    if index < len(items)-1:
        ax.annotate('', xy=(x + 1.1, 0.97), xytext=(x + 0.96, 0.97), arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.0))
ax.set_xlim(-0.1, 5.65); ax.set_ylim(0, 1.55); ax.axis('off')
```

**Example.** You touch a hot object. Receptors in the skin detect heat; nerves carry a message; the body rapidly moves the hand away. The safe lesson is not to test a reflex with heat or sharp objects. Tell an adult and cool a minor burn under clean running water as advised by a health professional.

## 1.2 Endocrine system and hormones

Glands release **hormones** into the blood. Hormones are chemical messengers that influence growth, energy use, mood and other body functions. The pituitary gland helps coordinate several other glands; the thyroid affects metabolism; the pancreas helps regulate blood glucose. These are simplified roles, not a reason to self-diagnose. Persistent health concerns require a qualified health worker.

| System | Main communication method | Example role |
|---|---|---|
| Nervous system | fast electrical messages through nerves | quick movement and sensation |
| Endocrine system | hormones carried in blood | growth and longer-term regulation |

## 1.3 Puberty and respectful health learning

Puberty is a normal stage in which bodies and feelings change at different times and in different ways. Reliable information, privacy, hygiene and respectful conversation matter. Never tease someone about body changes. Seek support from a trusted adult, teacher or health professional when worried.

::: key Respectful language
Use correct body and health terms, listen without laughing, do not share another person’s private information, and never pressure anyone to discuss something personal.
:::

::: caution Health content is not a substitute for care
This chapter supports learning. It cannot diagnose illness or replace a health worker. Urgent injury, severe pain, unsafe contact or mental distress should be shared promptly with a trusted adult or appropriate health service.
:::

## Chapter summary

- Brain, spinal cord and nerves coordinate information and responses.
- Hormones are chemical messages released by glands and carried in blood.
- Puberty varies from person to person and deserves privacy and respect.
- Accurate information and trusted professional support are safer than rumours.

## Practice questions

1. Name the three main parts of the nervous system introduced in this chapter. <span class="marks">[3]</span>
2. Compare one difference between nervous and endocrine communication. <span class="marks">[2]</span>
3. Why is it wrong to tease a classmate about puberty? Give two reasons. <span class="marks">[2]</span>
4. Draw and label the simplified signal path in the figure, then write one safe response to a minor injury. <span class="marks">[3]</span>

::: note Answers
**1.** Brain, spinal cord and nerves.  
**2.** Nervous messages travel quickly through nerves; endocrine messages are hormones carried in blood.  
**3.** It harms dignity and may stop someone from seeking accurate support; other respectful reasons are acceptable.  
**4.** Labels should be in the correct sequence. A safe response can include telling an adult and following suitable first-aid guidance.
:::
