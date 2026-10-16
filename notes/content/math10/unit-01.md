---
subject: Mathematics
grade: 10
unit: 1
title: Sets
hours: 0
area: Compulsory Mathematics
---

A set is a well-defined collection of objects, and almost every counting question in everyday life — how many students play football, how many families own a radio, how many people speak two languages — is really a question about sets. In Grade 10 you meet the one idea that makes these questions easy: **a Venn diagram, filled in from the middle outwards**. This chapter revises the language of sets, builds the two formulas for $n(A\cup B)$ and $n(A\cup B\cup C)$, and then solves the word problems that appear in the SEE paper almost every year.

::: key What the SEE asks from this chapter
Expect one question of 3 or 4 marks that gives you a survey ("In a class of 40 students …") and asks you to **find the number who like both**, **draw a Venn diagram**, and **find the number who like exactly one**. A second, shorter question asks you to verify a set law such as $(A\cup B)' = A'\cap B'$ using given sets. Every mark is for a clear step: write the formula, substitute, solve, then label the Venn diagram.
:::

## 1.1 Sets: concepts, formulas and worked problems

### Language of sets — a quick revision

A **set** is a collection of well-defined objects. The objects are its **elements** (or members). We write $x\in A$ for "$x$ belongs to $A$" and $x\notin A$ for "$x$ does not belong to $A$".

Two ways to describe a set:

- **Roster (listing) method:** $A=\{2,4,6,8\}$.
- **Set-builder (rule) method:** $A=\{x: x \text{ is an even natural number}, x<10\}$.

| Term | Meaning | Example |
|---|---|---|
| Finite set | has a countable number of elements | $\{1,3,5\}$ |
| Empty set $\emptyset$ | has no elements, $n(\emptyset)=0$ | primes between 23 and 29 |
| Universal set $U$ | the set of everything we are talking about | $U=\{1,2,3,\dots,10\}$ |
| Subset $A\subseteq B$ | every element of $A$ is also in $B$ | $\{2,4\}\subseteq\{2,4,6\}$ |
| Equal sets | same elements | $\{1,2,3\}=\{3,1,2\}$ |
| Disjoint sets | no common element, $A\cap B=\emptyset$ | $\{1,2\}$ and $\{5,6\}$ |
| $n(A)$ | the number of elements of $A$ | $n(\{a,e,i\})=3$ |

A set with $n$ elements has $2^n$ subsets. For example $\{a,b,c\}$ has $2^3=8$ subsets.

### The four operations

::: definition Union, intersection, difference, complement
Let $A$ and $B$ be subsets of a universal set $U$.

- **Union** $A\cup B=\{x: x\in A \text{ or } x\in B\}$ — everything in at least one of the sets.
- **Intersection** $A\cap B=\{x: x\in A \text{ and } x\in B\}$ — only what is in both.
- **Difference** $A-B=\{x: x\in A \text{ and } x\notin B\}$ — what is in $A$ but not in $B$.
- **Complement** $A'=U-A=\{x: x\in U \text{ and } x\notin A\}$ — everything in $U$ outside $A$.
:::

```figure caption="Shaded regions of the four operations on two overlapping sets inside the universal set $U$ (the rectangle)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, axes = plt.subplots(2, 2, figsize=(4.8, 3.4))
def panel(ax, title, mode):
    ax.add_patch(Rectangle((-2.2,-1.45), 4.4, 2.9, fc='white', ec=INK, lw=1.0))
    A = Circle((-0.6,0), 1.0, fc='none', ec=INK, lw=1.0)
    col = ACCENT
    if mode == 'union':
        ax.add_patch(Circle((-0.6,0), 1.0, fc=col, alpha=0.35, ec='none'))
        ax.add_patch(Circle((0.6,0), 1.0, fc=col, alpha=0.35, ec='none'))
    elif mode == 'inter':
        ax.add_patch(A)
        p = Circle((0.6,0), 1.0, fc=col, alpha=0.35, ec='none')
        ax.add_patch(p); p.set_clip_path(A)
    elif mode == 'diff':
        ax.add_patch(Circle((-0.6,0), 1.0, fc=col, alpha=0.35, ec='none'))
        ax.add_patch(Circle((0.6,0), 1.0, fc='white', ec='none', zorder=2))
    elif mode == 'comp':
        ax.add_patch(Rectangle((-2.2,-1.45), 4.4, 2.9, fc=col, alpha=0.35, ec='none'))
        ax.add_patch(Circle((-0.6,0), 1.0, fc='white', ec='none', zorder=2))
    for c in (Circle((-0.6,0), 1.0, fc='none', ec=INK, lw=1.0, zorder=3),
              Circle((0.6,0), 1.0, fc='none', ec=INK, lw=1.0, zorder=3)):
        ax.add_patch(c)
    ax.text(-1.15, 0, 'A', fontsize=9, ha='center', va='center', zorder=4)
    ax.text(1.15, 0, 'B', fontsize=9, ha='center', va='center', zorder=4)
    ax.text(-2.05, 1.2, 'U', fontsize=8, color=MUTED, ha='left', va='center')
    ax.set_title(title, fontsize=9, pad=2)
    ax.set_xlim(-2.3,2.3); ax.set_ylim(-1.55,1.55)
    ax.set_aspect('equal'); ax.axis('off')
panel(axes[0,0], r'$A\cup B$', 'union')
panel(axes[0,1], r'$A\cap B$', 'inter')
panel(axes[1,0], r'$A-B$', 'diff')
panel(axes[1,1], "$A'$", 'comp')
fig.tight_layout(pad=0.4)
```

::: example Operations on listed sets
**Problem.** Let $U=\{1,2,3,\dots,10\}$, $A=\{2,4,6,8,10\}$ and $B=\{3,6,9\}$. Find $A\cup B$, $A\cap B$, $A-B$, $B-A$, $A'$, and verify that $n(A\cup B)=n(A)+n(B)-n(A\cap B)$.

**Solution.**

$A\cup B=\{2,3,4,6,8,9,10\}$ (list every element once).

$A\cap B=\{6\}$ (only 6 is in both).

$A-B=\{2,4,8,10\}$ (remove 6 from $A$).

$B-A=\{3,9\}$ (remove 6 from $B$).

$A'=U-A=\{1,3,5,7,9\}$.

Verification: $n(A)=5$, $n(B)=3$, $n(A\cap B)=1$, so $n(A)+n(B)-n(A\cap B)=5+3-1=7$. Counting $A\cup B$ directly gives 7 elements. ✓
:::

### Two sets: the formula and the Venn diagram

When we add $n(A)$ and $n(B)$, the elements in $A\cap B$ are counted twice. To count each element once we subtract the overlap one time.

::: key Formulas for two sets
$$ n(A\cup B) = n(A) + n(B) - n(A\cap B) $$

- Only $A$: $n(A) - n(A\cap B)$.
- Only $B$: $n(B) - n(A\cap B)$.
- Neither: $n(U) - n(A\cup B)$.
- If $A$ and $B$ are disjoint, $n(A\cap B)=0$ and $n(A\cup B)=n(A)+n(B)$.
:::

```figure caption="Two-set Venn diagram. The four regions are 'only A', 'both', 'only B' and 'neither'; their counts add up to $n(U)$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, ax = plt.subplots(figsize=(4.6, 2.8))
ax.add_patch(Rectangle((-2.6,-1.55), 5.2, 3.1, fc='white', ec=INK, lw=1.1))
ax.add_patch(Circle((-0.7,0), 1.1, fc=SERIES[0], alpha=0.18, ec=INK, lw=1.1))
ax.add_patch(Circle((0.7,0), 1.1, fc=SERIES[1], alpha=0.18, ec=INK, lw=1.1))
ax.text(-1.25, 0, 'only A', fontsize=7, ha='center', va='center')
ax.text(0, 0, 'both', fontsize=7, ha='center', va='center')
ax.text(1.25, 0, 'only B', fontsize=7, ha='center', va='center')
ax.text(-1.7, 1.0, 'A', fontsize=10, fontweight='bold', ha='center')
ax.text(1.7, 1.0, 'B', fontsize=10, fontweight='bold', ha='center')
ax.text(2.45, 1.35, 'U', fontsize=9, color=MUTED, ha='right', va='center')
ax.text(0, -1.33, 'neither', fontsize=7, color=MUTED, ha='center', va='center')
ax.set_xlim(-2.7,2.7); ax.set_ylim(-1.65,1.65)
ax.set_aspect('equal'); ax.axis('off')
```

::: tip Always fill the middle first
In every Venn-diagram word problem, the number in the **overlap** is the one that is hard to find and the one everything else depends on. Find it (or take it from the question), write it in the middle, and then obtain each "only" region by subtraction. Never write the full $n(A)$ in the circle of $A$ when the circles overlap.
:::

::: example Finding the number who like both
**Problem.** In a class of 40 students, 25 like cricket, 20 like football and 5 like neither game. (i) How many like both games? (ii) Draw a Venn diagram. (iii) How many like cricket only?

**Solution.** Let $C$ = students who like cricket, $F$ = students who like football.

$n(U)=40$, $n(C)=25$, $n(F)=20$, $n(\text{neither})=5$.

Students who like at least one game: $n(C\cup F)=40-5=35$.

(i) Use $n(C\cup F)=n(C)+n(F)-n(C\cap F)$:

$$ 35 = 25 + 20 - n(C\cap F) \;\Rightarrow\; n(C\cap F) = 45 - 35 = 10 $$

**10 students like both games.**

(ii) Cricket only $=25-10=15$. Football only $=20-10=10$. Neither $=5$. Check: $15+10+10+5=40$ ✓. Write 15, 10, 10 in the three regions of the two circles and 5 outside the circles but inside the rectangle.

(iii) Cricket only $=15$ students.
:::

::: example Using a given overlap
**Problem.** In a group of 100 people, 70 speak Nepali, 45 speak Newari and 20 speak neither language. Find the number who speak both and the number who speak Nepali only.

**Solution.** $n(N\cup W)=100-20=80$.

$$ n(N\cap W) = n(N)+n(W)-n(N\cup W) = 70+45-80 = 35 $$

Both languages: **35** people. Nepali only $=70-35=35$ people. (Newari only $=45-35=10$; check $35+35+10+20=100$ ✓.)
:::

::: example Percentages
**Problem.** In a town, 75% of the people like tea, 60% like coffee and 10% like neither. Find the percentage who like both. If the town has 2,000 people, how many like both?

**Solution.** Take $n(U)=100\%$. People who like at least one drink: $100-10=90\%$.

$$ n(T\cap C) = 75 + 60 - 90 = 45\% $$

Number of people $=\dfrac{45}{100}\times 2000 = 900$.

**45% like both; 900 people.**
:::

::: example Forming and solving an equation
**Problem.** Of 80 students, 12 like both tea and coffee and 8 like neither. The number who like tea only is three times the number who like coffee only. Find how many like tea only and how many like coffee in all.

**Solution.** Let coffee only $=y$, so tea only $=3y$.

The four regions add to the total:

$$ 3y + 12 + y + 8 = 80 $$
$$ 4y = 60 \;\Rightarrow\; y = 15 $$

Tea only $=3\times 15=45$. Coffee only $=15$, so all who like coffee $=15+12=27$.

**Tea only: 45 students; coffee in all: 27 students.**
:::

::: caution Common mistakes
- Writing $n(A\cup B)=n(A)+n(B)$ when the sets overlap. The plus-only form is correct **only** for disjoint sets.
- Forgetting the students who like **neither**. They lie inside $U$ but outside both circles, and must be added back when you check the total.
- Putting $n(A)$ inside the $A$-circle without subtracting the overlap, so the circle then adds up to more than $n(A)$.
:::

### Three sets

For three sets the same inclusion–exclusion idea gives a longer formula. Adding $n(A)+n(B)+n(C)$ counts each pairwise overlap twice, so we subtract them; but that removes the triple overlap three times (after adding it three times), so we add it back once.

::: key Formula for three sets
$$ n(A\cup B\cup C) = n(A)+n(B)+n(C) $$

$$ -\ n(A\cap B) - n(B\cap C) - n(A\cap C) + n(A\cap B\cap C) $$

Seven regions, found **from the centre outwards**:

1. Centre: $n(A\cap B\cap C)$.
2. "Exactly two" regions: $n(A\cap B)-n(A\cap B\cap C)$, and the same for the other two pairs.
3. "Only one" regions: $n(A)$ minus the centre minus the two "exactly two" regions touching $A$.
4. Outside all three circles: $n(U)-n(A\cup B\cup C)$.
:::

::: example Three sets, filled in from the centre
**Problem.** Of 120 people, 60 like tea ($T$), 50 like coffee ($C$) and 40 like milk ($M$). Also 20 like $T$ and $C$, 15 like $C$ and $M$, 18 like $T$ and $M$, and 8 like all three. Find (i) how many like none of the drinks, (ii) how many like tea only.

**Solution.** Start with the centre: $n(T\cap C\cap M)=8$.

Exactly two drinks:

- $T$ and $C$ only $=20-8=12$
- $C$ and $M$ only $=15-8=7$
- $T$ and $M$ only $=18-8=10$

Exactly one drink:

- $T$ only $=60-12-10-8=30$
- $C$ only $=50-12-7-8=23$
- $M$ only $=40-10-7-8=15$

Total who like at least one drink:

$$ 30+23+15+12+7+10+8 = 105 $$

(Formula check: $60+50+40-20-15-18+8=105$ ✓.)

(i) None $=120-105=15$ people.

(ii) Tea only $=30$ people.
:::

```figure caption="Venn diagram for the tea, coffee and milk survey. Regions are filled from the centre outwards; the 15 outside all circles like none."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, ax = plt.subplots(figsize=(4.6, 3.3))
ax.add_patch(Rectangle((-2.7,-2.15), 5.4, 4.5, fc='white', ec=INK, lw=1.1))
r = 1.25
cs = {'T': (-0.75, 0.55), 'C': (0.75, 0.55), 'M': (0.0, -0.75)}
for (k, (x, y)), col in zip(cs.items(), SERIES[:3]):
    ax.add_patch(Circle((x, y), r, fc=col, alpha=0.17, ec=INK, lw=1.1))
lab = [(-1.2, 0.9, '30'), (1.2, 0.9, '23'), (0.0, -1.35, '15'),
       (0.0, 1.05, '12'), (-0.62, -0.28, '10'), (0.62, -0.28, '7'), (0.0, 0.1, '8')]
for x, y, s in lab:
    ax.text(x, y, s, fontsize=9, ha='center', va='center', color=INK, fontweight='bold')
ax.text(-2.0, 1.75, 'T (tea)', fontsize=8, ha='center')
ax.text(2.0, 1.75, 'C (coffee)', fontsize=8, ha='center')
ax.text(1.55, -1.95, 'M (milk)', fontsize=8, ha='center')
ax.text(-2.55, -1.9, 'none: 15', fontsize=8, color=MUTED, ha='left')
ax.text(2.6, 2.1, 'U = 120', fontsize=8, color=MUTED, ha='right', va='center')
ax.set_xlim(-2.8,2.8); ax.set_ylim(-2.25,2.45)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Exactly one, exactly two, none
**Problem.** Of 80 students, 40 play football ($F$), 35 play volleyball ($V$) and 30 play basketball ($B$). Also 15 play $F$ and $V$, 12 play $V$ and $B$, 10 play $F$ and $B$, and 5 play all three. Find the number who play (i) none, (ii) exactly two games, (iii) exactly one game.

**Solution.**

$$ n(F\cup V\cup B)=40+35+30-15-12-10+5=73 $$

(i) None $=80-73=7$.

(ii) Exactly two: $(15-5)+(12-5)+(10-5)=10+7+5=22$.

(iii) Exactly one $=73-22-5=46$.

Check by regions: $F$ only $=40-10-5-5=20$, $V$ only $=35-10-7-5=13$, $B$ only $=30-7-5-5=13$, and $20+13+13=46$ ✓.
:::

### Set laws verified with given sets

::: definition Laws used in SEE verification questions
- **Commutative:** $A\cup B=B\cup A$, $A\cap B=B\cap A$.
- **Distributive:** $A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$ and $A\cup(B\cap C)=(A\cup B)\cap(A\cup C)$.
- **De Morgan's laws:** $(A\cup B)'=A'\cap B'$ and $(A\cap B)'=A'\cup B'$.
:::

To **verify** a law, evaluate the left-hand side and the right-hand side separately for the given sets and show they are the same set.

::: example Verifying De Morgan's law
**Problem.** If $U=\{1,2,3,4,5,6,7,8\}$, $A=\{1,2,3,4\}$ and $B=\{3,4,5,6\}$, verify that $(A\cup B)'=A'\cap B'$.

**Solution.**

LHS: $A\cup B=\{1,2,3,4,5,6\}$, so $(A\cup B)'=\{7,8\}$.

RHS: $A'=\{5,6,7,8\}$ and $B'=\{1,2,7,8\}$, so $A'\cap B'=\{7,8\}$.

LHS $=$ RHS $=\{7,8\}$. Hence $(A\cup B)'=A'\cap B'$. ✓
:::

::: example Verifying the distributive law
**Problem.** For $A=\{1,2,3,4,5\}$, $B=\{2,4,6\}$ and $C=\{3,4,7\}$, verify $A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$.

**Solution.**

LHS: $B\cup C=\{2,3,4,6,7\}$, so $A\cap(B\cup C)=\{2,3,4\}$.

RHS: $A\cap B=\{2,4\}$ and $A\cap C=\{3,4\}$, so $(A\cap B)\cup(A\cap C)=\{2,3,4\}$.

LHS $=$ RHS, so the law is verified. ✓
:::

::: example Finding unknown counts from the formula
**Problem.** If $n(A)=22$, $n(B)=18$ and $n(A\cup B)=35$, find $n(A\cap B)$, $n(A-B)$ and $n(B-A)$.

**Solution.** $n(A\cap B)=22+18-35=5$.

$n(A-B)=22-5=17$ and $n(B-A)=18-5=13$.

Check: $17+5+13=35=n(A\cup B)$ ✓.
:::

## 1.2 Exercises of the SEE type

### Method for any survey question

1. Name the sets ($T$, $C$, …) and write each given number with its $n(\;)$ symbol.
2. If "neither" is given, find $n(A\cup B)=n(U)-n(\text{neither})$.
3. Use the formula to find the overlap.
4. Draw the Venn diagram; fill the middle, then the "only" regions, then the outside.
5. Add all regions to check you get $n(U)$.
6. Answer the specific question in a sentence.

::: tip Diagrams carry marks
In a 4-mark SEE question, 1 mark is typically for the Venn diagram. Draw the rectangle for $U$, two or three overlapping circles, and label every region with a number — even the region outside the circles.
:::

## Chapter summary

- $n(A\cup B)=n(A)+n(B)-n(A\cap B)$; for disjoint sets $n(A\cap B)=0$.
- Only $A$: $n(A)-n(A\cap B)$. Neither: $n(U)-n(A\cup B)$.
- $n(A\cup B\cup C)=n(A)+n(B)+n(C)-n(A\cap B)-n(B\cap C)-n(A\cap C)+n(A\cap B\cap C)$.
- Fill a three-set Venn diagram from the centre outwards; check that all regions add to $n(U)$.
- Exactly two $=\sum n(\text{pair})-3\,n(A\cap B\cap C)$; exactly one $=n(A\cup B\cup C)-(\text{exactly two})-n(A\cap B\cap C)$.
- $A-B=A\cap B'$ and $A'=U-A$.
- De Morgan: $(A\cup B)'=A'\cap B'$, $(A\cap B)'=A'\cup B'$.
- Distributive: $A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. If $n(A)=12$, $n(B)=9$ and $n(A\cap B)=4$, then $n(A\cup B)$ is <span class="marks">[1]</span>
   (a) 25 (b) 17 (c) 21 (d) 13
2. In set notation, "elements of $A$ that are not in $B$" is <span class="marks">[1]</span>
   (a) $A\cup B$ (b) $A\cap B$ (c) $A\cap B'$ (d) $A'\cap B$
3. If $U=\{1,2,3,\dots,10\}$ and $A=\{2,3,5,7\}$, then $n(A')$ is <span class="marks">[1]</span>
   (a) 4 (b) 5 (c) 6 (d) 10
4. If $A\subseteq B$, then $A\cup B$ equals <span class="marks">[1]</span>
   (a) $A$ (b) $B$ (c) $\emptyset$ (d) $U$
5. $n(P\cup Q)=n(P)+n(Q)$ holds when <span class="marks">[1]</span>
   (a) $P\subseteq Q$ (b) $P=Q$ (c) $P$ and $Q$ are disjoint (d) $P'=Q$

::: note Answers to Group A
**1.** (b) — $12+9-4=17$.
**2.** (c) — $A-B=A\cap B'$.
**3.** (c) — $n(U)-n(A)=10-4=6$.
**4.** (b) — every element of $A$ is already in $B$.
**5.** (c) — nothing is counted twice only when $P\cap Q=\emptyset$.
:::

**Group B — Short answer (2 marks each)**

1. If $n(A)=22$, $n(B)=18$ and $n(A\cup B)=35$, find $n(A\cap B)$. <span class="marks">[2]</span>
2. Draw a Venn diagram and shade the region $A'\cap B$. <span class="marks">[2]</span>
3. If $U=\{x: x\in\mathbb{N}, x\le 12\}$, $A=\{3,6,9,12\}$ and $B=\{2,4,6,8,10,12\}$, find $A\cap B$ and $A-B$. <span class="marks">[2]</span>
4. In a class of 30 students every student plays at least one of football and volleyball. If 20 play football and 15 play volleyball, how many play both? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $n(A\cap B)=n(A)+n(B)-n(A\cup B)=22+18-35=5$.
**2.** Draw $U$ as a rectangle with overlapping circles $A$ and $B$. $A'\cap B$ is the part of $B$ that lies outside $A$ — the crescent of circle $B$ not overlapped by $A$ (the "only $B$" region).
**3.** $A\cap B=\{6,12\}$ and $A-B=\{3,9\}$.
**4.** All 30 are in $F\cup V$: $30=20+15-n(F\cap V)$, so $n(F\cap V)=35-30=5$ students.
:::

**Group C — Short answer (3 marks each)**

1. Of 100 students, 60 study Mathematics, 50 study Science and 20 study neither. Find how many study both, and how many study Mathematics only. <span class="marks">[3]</span>
2. In a group of 50 people, 30 drink milk, 25 drink tea and 10 drink neither. Find how many drink tea only. <span class="marks">[3]</span>
3. In a village, 70% of the families have a radio, 55% have a television and 20% have neither. Find the percentage that have both. If there are 400 families, how many have both? <span class="marks">[3]</span>
4. If $A=\{1,2,3,4,5\}$, $B=\{2,4,6\}$ and $C=\{3,4,7\}$, verify $A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $n(M\cup S)=100-20=80$. $n(M\cap S)=60+50-80=30$. Mathematics only $=60-30=30$.
**2.** $n(M\cup T)=50-10=40$. $n(M\cap T)=30+25-40=15$. Tea only $=25-15=10$.
**3.** $n(R\cup T)=100-20=80\%$. Both $=70+55-80=45\%$. For 400 families: $\frac{45}{100}\times 400=180$ families.
**4.** $B\cup C=\{2,3,4,6,7\}$, so LHS $=\{2,3,4\}$. $A\cap B=\{2,4\}$, $A\cap C=\{3,4\}$, so RHS $=\{2,3,4\}$. LHS $=$ RHS. ✓
:::

**Group D — Long answer (4 marks each)**

1. In a survey of 100 students, 48 like English, 42 like Nepali and 36 like Mathematics. Also 18 like English and Nepali, 14 like Nepali and Mathematics, 12 like English and Mathematics, and 6 like all three. Draw a Venn diagram and find how many like (a) none of the subjects, (b) exactly one subject. <span class="marks">[4]</span>
2. In a group of 80 students, 12 like both tea and coffee and 8 like neither. The number who like tea only is three times the number who like coffee only. Find the number who like coffee. <span class="marks">[4]</span>
3. If $U=\{1,2,3,\dots,12\}$, $A=\{1,3,5,7,9,11\}$ and $B=\{2,3,5,7,11\}$, verify De Morgan's law $(A\cup B)'=A'\cap B'$. <span class="marks">[4]</span>
4. Of 80 students, 40 play football, 35 volleyball and 30 basketball; 15 play football and volleyball, 12 volleyball and basketball, 10 football and basketball; 5 play all three. Find how many play exactly two games. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** Centre $=6$. Exactly two: $E,N$ only $=18-6=12$; $N,M$ only $=14-6=8$; $E,M$ only $=12-6=6$.
**1 (cont.)** Exactly one: $E$ only $=48-12-6-6=24$; $N$ only $=42-12-8-6=16$; $M$ only $=36-8-6-6=16$. Union $=24+16+16+12+8+6+6=88$ (formula: $48+42+36-18-14-12+6=88$ ✓). (a) None $=100-88=12$. (b) Exactly one $=24+16+16=56$.
**2.** Let coffee only $=y$, tea only $=3y$. $3y+12+y+8=80$, so $4y=60$ and $y=15$. Students who like coffee $=15+12=27$.
**3.** $A\cup B=\{1,2,3,5,7,9,11\}$, so $(A\cup B)'=\{4,6,8,10,12\}$. $A'=\{2,4,6,8,10,12\}$, $B'=\{1,4,6,8,9,10,12\}$, so $A'\cap B'=\{4,6,8,10,12\}$. The two sides are equal. ✓
**4.** Exactly two $=(15-5)+(12-5)+(10-5)=10+7+5=22$ students.
:::
