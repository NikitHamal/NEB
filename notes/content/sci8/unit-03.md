---
subject: Science and Technology
grade: 8
unit: 3
title: Living Beings and Their Structure
hours: 0
area: Science and Technology
---

A living thing may be a single cell too small to see without a microscope, or a large plant or animal made of many specialised parts. Cells carry out the basic activities of life. In a multicellular organism, similar cells work together as tissues, tissues form organs, and organs cooperate in systems. Understanding this organisation helps explain how a leaf makes food, how a heart moves blood and why living things need suitable habitats.

::: key Remember the levels of organisation
**Cell → tissue → organ → organ system → organism.** Each larger level is built from smaller parts that work together. In Nepali: **कोशिका → तन्तु → अङ्ग → अङ्ग प्रणाली → जीव।**
:::

## 3.1 Living things and cells

Living things grow, use energy, respond to their surroundings and produce new living things. A crystal can grow larger, but it does not take in food, respire or reproduce as a living organism does. Viruses are unusual and are not usually treated as complete cells; they reproduce only inside host cells.

A **cell** is the smallest structural and functional unit of a living organism. Some organisms, such as many bacteria and Amoeba, are **unicellular**: one cell performs all essential life functions. Plants, animals and fungi are generally **multicellular**. Their cells specialise, so a muscle cell contracts, a root hair cell absorbs water and a nerve cell carries signals. Specialisation makes it possible for large organisms to perform many tasks efficiently.

```photo id="sci10/amoeba" caption="Amoeba is a single-celled organism. It moves and surrounds food by changing the shape of its cell membrane to form temporary extensions." width="66"
```

A microscope uses lenses to make small objects appear larger. Begin with the lowest-power objective lens, place the slide safely, and focus slowly. Never press the lens against the slide. A drawing of a specimen should be large, clear, labelled with straight lines and based on what is visible—not what you expect to see.

## 3.2 Parts of a cell

Most cells have a **cell membrane**, **cytoplasm** and **nucleus**. The membrane forms the cell's boundary and controls many substances entering and leaving. The cytoplasm is the jelly-like material where many chemical reactions occur. The nucleus contains genetic material and helps control cell activities.

Plant cells have additional structures. A strong **cell wall** outside the membrane supports and protects the cell. Many plant cells contain **chloroplasts**, which have chlorophyll for capturing light in photosynthesis. A large **vacuole** stores cell sap and helps keep the cell firm. Not every plant cell has chloroplasts: for example, ordinary root cells usually grow underground and do not photosynthesise.

Animal cells do not have a cell wall or chloroplasts. Their outer boundary is the cell membrane, and their vacuoles, if present, are usually smaller than the large central vacuole of a typical plant cell.

| Structure | Main job | Found in |
|---|---|---|
| Cell membrane | Controls exchange with the surroundings | Plant and animal cells |
| Cytoplasm | Site of many cell reactions | Plant and animal cells |
| Nucleus | Contains genetic material; helps control activities | Most plant and animal cells |
| Cell wall | Supports and protects the cell | Plant cells |
| Chloroplast | Captures light for photosynthesis | Many green plant cells |
| Large vacuole | Stores cell sap and helps keep the cell firm | Typical plant cells |

```figure caption="Typical plant and animal cells share a membrane, cytoplasm and nucleus; plant cells have a wall and often chloroplasts and a large vacuole. Diagrams are simplified and not to scale."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse
fig, ax = plt.subplots(figsize=(5.0, 3.1))
ax.set_xlim(0, 12); ax.set_ylim(0, 7); ax.axis("off")
# Plant cell: rigid outer wall and inner membrane.
ax.add_patch(Rectangle((0.6, 1.0), 5.1, 4.8, fc="#eef5e8", ec=INK, lw=2.0))
ax.add_patch(Rectangle((0.82, 1.22), 4.66, 4.36, fc="none", ec=ACCENT, lw=1.1))
ax.add_patch(Ellipse((3.45, 3.2), 2.5, 2.5, fc="#e1efff", ec=ACCENT, lw=1.0))
ax.text(3.45, 3.2, "Large\nvacuole", ha="center", va="center", fontsize=8, color=INK)
ax.add_patch(Circle((1.65, 4.55), 0.48, fc="#e6dafa", ec=SERIES[4], lw=1.0))
ax.text(1.65, 4.55, "Nucleus", ha="center", va="center", fontsize=6.8, color=INK)
for x,y in [(1.55,1.75),(4.85,1.65),(4.85,4.85)]:
    ax.add_patch(Ellipse((x,y),0.72,0.38,fc="#d9efcc",ec=SERIES[2],lw=1.0))
ax.text(3.15, 6.35, "Plant cell", ha="center", fontsize=9, weight="bold", color=INK)
ax.text(3.15, 0.55, "Wall outside membrane", ha="center", fontsize=7, color=MUTED)
# Animal cell: flexible boundary, nucleus, cytoplasm.
ax.add_patch(Ellipse((9.0, 3.35), 4.5, 4.25, fc="#fff2e8", ec=INK, lw=1.6))
ax.add_patch(Circle((8.45, 3.45), 0.62, fc="#e6dafa", ec=SERIES[4], lw=1.0))
ax.text(8.45,3.45,"Nucleus",ha="center",va="center",fontsize=7,color=INK)
ax.text(9.55, 2.6, "Cytoplasm", ha="center", fontsize=7.5, color=INK)
ax.text(9.0, 6.0, "Animal cell", ha="center", fontsize=9, weight="bold", color=INK)
fig.tight_layout()
```

::: caution Avoid two common errors
The cell wall is outside the cell membrane in a plant cell. Also, a chloroplast is not present in every plant cell; it is common in green cells exposed to light. Describe the cell shown, not a rule that has exceptions.
:::

## 3.3 From cells to organs

A **tissue** is a group of similar cells working together. Examples include muscle tissue, which contracts, and xylem tissue in plants, which transports water. An **organ** contains different tissues that work together for a larger task. A leaf contains tissues that support it, protect it and help it make food. A **system** is a group of organs cooperating; the digestive system processes food, while the circulatory system transports materials around the body.

```figure caption="A leaf is an organ made of different tissues; organs cooperate in systems that keep an organism alive."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8, 2.5))
ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis("off")
labels=[("Cell",0.35),("Tissue",2.75),("Leaf\n(organ)",5.15),("Plant\nsystem",7.75),("Plant\norganism",10.05)]
for label,x in labels:
    ax.add_patch(FancyBboxPatch((x,1.8),1.65,1.1,boxstyle="round,pad=0.06",fc="#eef5e8",ec=SERIES[2],lw=1.0))
    ax.text(x+0.825,2.35,label,ha="center",va="center",fontsize=7.5,color=INK)
for (_,x1),(_,x2) in zip(labels,labels[1:]):
    ax.annotate("",xy=(x2-0.12,2.35),xytext=(x1+1.7,2.35),arrowprops=dict(arrowstyle="->",color=ACCENT,lw=1.1))
ax.text(6,0.9,"Cells with related jobs build larger working parts.",ha="center",fontsize=7.2,color=MUTED)
fig.tight_layout()
```

::: example Put the levels in order
**Problem.** Put these terms in order from smallest to largest: heart, muscle cell, circulatory system, muscle tissue, human.

**Solution.** A muscle cell is one cell. Many similar muscle cells form muscle tissue. The heart is an organ containing several tissues. The circulatory system includes the heart and blood vessels. The human is the organism. So the order is **muscle cell → muscle tissue → heart → circulatory system → human**.
:::

## 3.4 Structure is related to function

A structure's shape often helps it perform a job. A root hair has a long extension that increases the area touching moist soil. A red blood cell is small and flexible so it can travel through narrow blood vessels; its haemoglobin carries oxygen. A leaf is broad and thin, helping it receive light and exchange gases. These are examples of **adaptations**—features that help organisms survive in particular surroundings. An adaptation is useful in a specific environment; it is not a conscious choice made by the organism.

::: example Match a cell to its job
**Problem.** A cell has a long, thin projection and branches at one end. Which type of cell is it likely to be, and how does the shape help?

**Solution.** It is likely a nerve cell. Its long projection can carry a signal over a distance, and the branches help it connect with other cells. The diagram or observation is evidence for the likely function; a single visible shape does not reveal every detail of the cell.
:::

A hibiscus plant is multicellular. Its root, stem and leaves are organs with different jobs, yet they depend on one another. Roots absorb water and minerals, stems support the plant and transport materials, and leaves make food using light. If one part is badly damaged, other parts may not receive what they need.

```photo id="sci10/hibiscus" caption="A hibiscus flower is one visible part of a multicellular plant. The flower helps the plant reproduce; leaves, stems and roots carry out other functions." width="62"
```

## 3.5 Observe cells responsibly

Use prepared slides where possible. If the teacher asks you to prepare one, use a clean slide and cover slip, a tiny sample and the approved stain. Do not collect blood or cut living tissue. Return microscopes and slides safely, and wash hands after the activity. Draw only what you can see; label the visible structures and note the magnification or method if it is required.

::: example Select a sensible observation
**Problem.** A student wants to compare the shapes of onion epidermal cells and cheek cells. State one fair procedure and one difference the student may observe.

**Solution.** Use the same microscope magnification for each slide, adjust the light carefully and examine several cells rather than selecting one unusual cell. Onion epidermal cells are often rectangular and arranged in rows; cheek cells are usually more rounded or irregular. A prepared slide may look different depending on the stain and how it was made, so the drawing should match the actual view.
:::

## Chapter summary

- A cell is the smallest structural and functional unit of life; unicellular organisms have one cell, while multicellular organisms have many specialised cells.
- Cell membrane, cytoplasm and nucleus are common structures. Plant cells also have a wall; many green plant cells have chloroplasts and a large vacuole.
- Similar cells form tissues; tissues form organs; organs work together in systems within an organism.
- Cell and body structures are related to their functions and surroundings.
- Use microscopes carefully, record what you observe and do not collect or harm living tissue for a school activity.

## Practice questions

1. Which structure controls many substances entering and leaving a cell? (a) cell wall (b) cell membrane (c) vacuole (d) chloroplast
2. Name one structure found in typical plant cells but not animal cells.
3. Arrange cell, organ, tissue and organ system from smallest to largest.
4. Why do we say that a muscle cell is specialised?

::: note Answers to questions 1–4
**1.** (b) — the cell membrane controls exchange with the surroundings.
**2.** Cell wall or chloroplast; a large central vacuole is also characteristic of a typical plant cell. Chloroplasts occur in many, not all, plant cells.
**3.** Cell → tissue → organ → organ system.
**4.** Its structure supports its job of contracting to produce movement.
:::

5. Compare a plant cell and an animal cell using two similarities and two differences.
6. Explain why a root hair cell has a long extension.
7. A tissue is damaged in an organ. Explain one way this might affect the organ's work.
8. Why should a biological drawing show the structures actually observed instead of a memorised ideal picture?

::: note Answers to questions 5–8
**5.** Similarities: both have a cell membrane and cytoplasm; most have a nucleus. Differences: plant cells have a cell wall and may contain chloroplasts and a large vacuole; animal cells do not have a wall or chloroplasts.
**6.** The long extension increases the surface area in contact with soil, helping absorption of water and minerals.
**7.** The organ may perform its function less effectively because its tissues depend on one another. For example, damage to leaf tissue can reduce food-making or transport.
**8.** A drawing is a record of evidence. Adding unseen structures would misrepresent the observation and make the result difficult to check.
:::
