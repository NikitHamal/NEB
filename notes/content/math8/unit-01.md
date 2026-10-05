---
subject: Mathematics
grade: 8
unit: 1
title: 'Unit 1: Sets'
hours: 7
area: Units
---

Sets organise information without double-counting it. They are useful when a class survey asks who plays football, who plays volleyball, and who plays both. In this unit you will identify disjoint, overlapping and subset relationships and turn a word situation into a correct Venn diagram.

::: key What success looks like
You can say whether two sets overlap, decide whether one set is a subset of another, and fill a two-set Venn diagram by writing the common part first.
:::

## 1.1 The language of sets

A **set** is a well-defined collection. Its objects are called **elements**. We write $x\in A$ when $x$ belongs to $A$ and $x\notin A$ when it does not.

| Idea | Meaning | Example |
|---|---|---|
| Empty set | no elements | $\{\}$ or $\emptyset$ |
| Universal set $U$ | all objects being discussed | all 40 learners in a class |
| Subset $A\subseteq B$ | every element of $A$ is also in $B$ | $\{2,4\}\subseteq\{2,4,6\}$ |
| Disjoint sets | no common element | even numbers and odd numbers |
| Overlapping sets | at least one common element | learners who sing and learners who dance |

::: example Decide the relationship
Let $A=\{a,e,i,o,u\}$ and $B=\{a,i\}$. Every member of $B$ is in $A$, so $B\subseteq A$. The sets overlap because their common elements are $\{a,i\}$.
:::

## 1.2 Reading a Venn diagram

In a Venn diagram, the rectangle is $U$. A circle is a set. The lens-shaped middle is the intersection: the learners counted in **both** sets.

```figure caption="A two-set Venn diagram. Always fill the middle (both) region before the two 'only' regions."
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, ax = plt.subplots(figsize=(4.8, 2.8))
ax.add_patch(Rectangle((-2.45, -1.35), 4.9, 2.7, fc='white', ec=INK, lw=1.1))
ax.add_patch(Circle((-0.72, 0), 1.02, fc=SERIES[0], alpha=0.18, ec=INK, lw=1.1))
ax.add_patch(Circle((0.72, 0), 1.02, fc=SERIES[1], alpha=0.18, ec=INK, lw=1.1))
ax.text(-1.35, 0, 'only A', ha='center', va='center', fontsize=9)
ax.text(0, 0, 'both', ha='center', va='center', fontsize=9, weight='bold')
ax.text(1.35, 0, 'only B', ha='center', va='center', fontsize=9)
ax.text(-1.3, 0.93, 'A', ha='center', fontsize=10, weight='bold')
ax.text(1.3, 0.93, 'B', ha='center', fontsize=10, weight='bold')
ax.text(2.25, 1.12, 'U', ha='right', color=MUTED, fontsize=9)
ax.text(0, -1.08, 'neither', ha='center', color=MUTED, fontsize=9)
ax.set_xlim(-2.6, 2.6); ax.set_ylim(-1.5, 1.5); ax.set_aspect('equal'); ax.axis('off')
```

::: example Fill a survey diagram
**Problem.** In a class of 30, 18 like football, 12 like volleyball and 5 like both. Find the number who like only football, only volleyball and neither.

**Solution.** Write 5 in the middle first. Only football $=18-5=13$. Only volleyball $=12-5=7$. At least one $=13+5+7=25$. Neither $=30-25=5$.
:::

::: caution Do not place 18 in the 'only football' region
The number 18 already includes the 5 learners who like both games. Subtract the overlap before writing an 'only' number.
:::

## Chapter summary

- A subset is fully contained inside another set.
- Disjoint sets have no shared element; overlapping sets have one or more.
- In a Venn survey, complete the common region first, then the only regions, then neither.

## Practice questions

1. Let $P=\{2,4,6,8\}$ and $Q=\{4,8\}$. Is $Q\subseteq P$? Explain. <span class="marks">[1]</span>
2. Are the sets of multiples of 2 and multiples of 3 disjoint? Give one reason. <span class="marks">[1]</span>
3. Of 40 learners, 22 read stories, 16 read poems and 8 read both. Find the number who read only stories, only poems and neither. <span class="marks">[3]</span>
4. Draw a Venn diagram for question 3 and label all four regions. <span class="marks">[2]</span>

::: note Answers
**1.** Yes; 4 and 8 are both elements of $P$.  
**2.** No. For example, 6 is a multiple of both 2 and 3.  
**3.** Only stories $=14$, only poems $=8$, neither $=10$.  
**4.** Middle 8, story only 14, poem only 8, outside 10.
:::
