---
subject: Optional Mathematics
grade: 8
unit: 1
title: Relation and Function
hours: 0
---

A class register pairs every roll number with a name. A price list pairs every item with its price. A map pairs every place with a position. Mathematics needs a careful language for such pairings, because the order of the two things matters: roll number 7 with 45 marks is not the same record as roll number 45 with 7 marks. This chapter builds that language step by step. We start with **ordered pairs**, combine two sets into their **Cartesian product**, pick out the pairs that obey a rule to make a **relation**, and finally meet the most important kind of relation in all of mathematics, the **function**, in which every input has exactly one output.

::: key What your examination asks from this chapter
Expect these question types: (i) find $x$ and $y$ from two **equal ordered pairs**; (ii) write $A\times B$ and $B\times A$ and find $n(A\times B)$; (iii) list a **relation** from a rule, show it in an arrow diagram, and state its **domain**, **range** and **inverse**; (iv) decide whether an arrow diagram or a set of ordered pairs is a **function**, with a reason; (v) find $f(a)$, a **pre-image**, or the constants $a$ and $b$ in $f(x)=ax+b$; (vi) use the **vertical line test** on a graph. A reason written in words ("2 has two images") is part of the answer.
:::

## 1.1 Ordered pairs and equal ordered pairs

Suppose Sita has roll number 7 and scored 45 marks in a test. We can record this as $(7,45)$. The pair $(45,7)$ would tell a different story: roll number 45 with 7 marks. When two objects are written together and **the order matters**, we call them an ordered pair.

::: definition Ordered pair
Two objects $a$ and $b$ written in a definite order inside small brackets, $(a,b)$, form an **ordered pair**. The object $a$ is the **first component** (first element) and $b$ is the **second component** (second element). The pairs $(a,b)$ and $(b,a)$ are different unless $a=b$.
:::

You have used ordered pairs for years without the name: the coordinates of a point. The point $(2,3)$ is 2 units along the $x$-axis and 3 units up; the point $(3,2)$ is 3 units along and 2 units up. The figure below shows that they are two different points.

```figure caption="The ordered pairs $(2,3)$ and $(3,2)$ name two different points. The first component is always read along the $x$-axis and the second along the $y$-axis."
fig, ax = plt.subplots(figsize=(4.4, 2.9))
ax.set_xlim(-0.2, 5.4); ax.set_ylim(-0.2, 4.4)
ax.set_xticks(range(0, 6)); ax.set_yticks(range(0, 5))
ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False)
for (px, py), c, lab, dx, dy in [((2, 3), ACCENT, 'P(2, 3)', 0.15, 0.18), ((3, 2), SERIES[1], 'Q(3, 2)', 0.15, -0.42)]:
    ax.plot([px, px], [0, py], ls='--', color=c, lw=1.0)
    ax.plot([0, px], [py, py], ls='--', color=c, lw=1.0)
    ax.plot(px, py, 'o', color=c, ms=6)
    ax.text(px + dx, py + dy, lab, color=c, fontsize=9.5)
ax.set_xlabel('x : first component', fontsize=9)
ax.set_ylabel('y : second component', fontsize=9)
ax.tick_params(labelsize=8.5)
fig.tight_layout(pad=0.4)
```

An ordered pair is not the same thing as a set of two members. The table shows the differences.

| Feature | Set $\{2,3\}$ | Ordered pair $(2,3)$ |
|---|---|---|
| Brackets | curly brackets $\{\ \}$ | small brackets $(\ )$ |
| Does order matter? | no: $\{2,3\}=\{3,2\}$ | yes: $(2,3)\neq(3,2)$ |
| Can a member repeat? | $\{2,2\}$ is just $\{2\}$, one member | $(2,2)$ is a proper pair, like the point $(2,2)$ |
| What it records | which objects belong | which object comes first and which second |

### Equal ordered pairs

::: definition Equal ordered pairs
Two ordered pairs are **equal** when their first components are equal **and** their second components are equal:
$$ (a,b)=(c,d)\quad\Longleftrightarrow\quad a=c\ \text{and}\ b=d $$
:::

So one statement about equal ordered pairs gives **two equations**: first component = first component, second component = second component. This is the most common one-mark and two-mark question of the chapter.

::: example Equal ordered pairs, one unknown in each component
**Problem.** Find $x$ and $y$ if $(x+3,\ 7)=(8,\ 2y-1)$.

**Solution.** Equate the first components and then the second components.

First components: $x+3=8$, so $x=8-3=5$.

Second components: $7=2y-1$, so $2y=8$ and $y=4$.

**Check.** $(5+3,\ 7)=(8,7)$ and $(8,\ 2\times4-1)=(8,7)$. ✓
:::

::: example Both unknowns in each component
**Problem.** If $(2x-y,\ x+y)=(7,\ 8)$, find $x$ and $y$.

**Solution.** The two equations are
$$ 2x-y=7 \qquad \text{(i)} \qquad\qquad x+y=8 \qquad \text{(ii)} $$
Adding (i) and (ii): $3x=15$, so $x=5$. From (ii): $y=8-5=3$.

**Check.** $2(5)-3=7$ ✓ and $5+3=8$ ✓. So $x=5$, $y=3$.
:::

::: example Unknowns on both sides
**Problem.** Find $x$ and $y$ if $(3x-2,\ y+5)=(x+6,\ 2y-1)$.

**Solution.** First components: $3x-2=x+6$, so $2x=8$ and $x=4$.

Second components: $y+5=2y-1$, so $5+1=2y-y$ and $y=6$.

**Check.** Left pair $(3\times4-2,\ 6+5)=(10,11)$; right pair $(4+6,\ 2\times6-1)=(10,11)$. ✓
:::

::: caution Match first with first, second with second
A student who writes $x+3=2y-1$ for the first example has joined a first component to a second component. That equation is not given by the question. Draw two short arrows in your rough work, first to first and second to second, before you write any equation.
:::

## 1.2 Cartesian product of two sets

A tea shop in Butwal sells two drinks, $D=\{\text{tea},\ \text{coffee}\}$, and three snacks, $S=\{\text{samosa},\ \text{sel roti},\ \text{biscuit}\}$. A customer who chooses one drink **and then** one snack can make these orders:

(tea, samosa), (tea, sel roti), (tea, biscuit), (coffee, samosa), (coffee, sel roti), (coffee, biscuit).

There are $2\times3=6$ possible orders. The set of all of them is the **Cartesian product** $D\times S$, named after the French mathematician René Descartes, who also gave us coordinates.

::: definition Cartesian product
The **Cartesian product** of two non-empty sets $A$ and $B$, written $A\times B$ and read "$A$ cross $B$", is the set of all ordered pairs whose first component is from $A$ and whose second component is from $B$:
$$ A\times B=\{(a,b): a\in A \text{ and } b\in B\} $$
:::

::: example Writing A × B and B × A
**Problem.** If $A=\{1,2,3\}$ and $B=\{x,y\}$, find $A\times B$ and $B\times A$. Are they equal?

**Solution.** Take each member of $A$ in turn and pair it with every member of $B$:
$$ A\times B=\{(1,x),(1,y),(2,x),(2,y),(3,x),(3,y)\} $$
Now take each member of $B$ first:
$$ B\times A=\{(x,1),(x,2),(x,3),(y,1),(y,2),(y,3)\} $$
Both have 6 members, but $(1,x)\in A\times B$ while $(1,x)\notin B\times A$. So $A\times B\neq B\times A$.
:::

### Ways of showing a Cartesian product

The same product can be shown in five ways. For $A=\{1,2,3\}$ and $B=\{4,5\}$:

| Method | What you draw or write |
|---|---|
| Listing | $A\times B=\{(1,4),(1,5),(2,4),(2,5),(3,4),(3,5)\}$ |
| Tree diagram | three branches 1, 2, 3; from each, two branches 4 and 5; read each path as a pair |
| Table | rows labelled 1, 2, 3, columns labelled 4, 5; each cell holds a pair |
| Arrow diagram | two ovals; an arrow from every member of $A$ to every member of $B$ |
| Graph | the six points $(1,4),\ldots,(3,5)$ plotted as a lattice of dots |

```figure caption="Two pictures of $A\times B$ for $A=\{1,2,3\}$ and $B=\{4,5\}$. Left: an arrow diagram, with an arrow from every member of $A$ to every member of $B$. Right: the graph, a lattice of $3\times2=6$ points."
from matplotlib.patches import Ellipse
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.8))
ax1.set_xlim(0, 10); ax1.set_ylim(0, 10); ax1.axis('off')
ax1.add_patch(Ellipse((2.3, 4.8), 2.8, 7.6, fc='#eaf2fb', ec=ACCENT, lw=1.2))
ax1.add_patch(Ellipse((7.7, 4.8), 2.8, 7.6, fc='#fbecec', ec=SERIES[1], lw=1.2))
ax1.text(2.3, 9.3, 'A', ha='center', fontsize=10, color=ACCENT)
ax1.text(7.7, 9.3, 'B', ha='center', fontsize=10, color=SERIES[1])
ya = {1: 7.0, 2: 4.8, 3: 2.6}; yb = {4: 6.1, 5: 3.5}
for a, yy in ya.items():
    ax1.text(2.3, yy, str(a), ha='center', va='center', fontsize=10)
for b, yy in yb.items():
    ax1.text(7.7, yy, str(b), ha='center', va='center', fontsize=10)
for a, y1 in ya.items():
    for b, y2 in yb.items():
        ax1.annotate('', xy=(7.2, y2), xytext=(2.8, y1), arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9))
pts = [(a, b) for a in (1, 2, 3) for b in (4, 5)]
ax2.plot([p[0] for p in pts], [p[1] for p in pts], 'o', color=ACCENT, ms=5)
for p in pts:
    ax2.text(p[0] + 0.08, p[1] + 0.12, f'({p[0]}, {p[1]})', fontsize=7.8, color=INK)
ax2.set_xlim(0, 4); ax2.set_ylim(3, 5.8)
ax2.set_xticks([1, 2, 3]); ax2.set_yticks([3, 4, 5])
ax2.set_xlabel('member of A', fontsize=8.5); ax2.set_ylabel('member of B', fontsize=8.5)
ax2.grid(True, color=GRID, lw=0.6); ax2.set_axisbelow(True)
ax2.spines[['top', 'right']].set_visible(False); ax2.tick_params(labelsize=8)
fig.tight_layout(pad=0.4)
```

::: key Facts about the Cartesian product
- $n(A\times B)=n(A)\times n(B)$: every member of $A$ is paired with every member of $B$.
- $A\times B\neq B\times A$ in general, although $n(A\times B)=n(B\times A)$. They are equal only when $A=B$.
- $A\times A$ is also written $A^2$. For example $\{0,1\}^2=\{(0,0),(0,1),(1,0),(1,1)\}$.
:::

::: example Recovering the sets from the product
**Problem.** If $A\times B=\{(a,1),(a,2),(a,3),(b,1),(b,2),(b,3)\}$, find $A$, $B$ and check that $n(A\times B)=n(A)\times n(B)$.

**Solution.** $A$ is the set of first components and $B$ is the set of second components:
$$ A=\{a,b\},\qquad B=\{1,2,3\} $$
Then $n(A)\times n(B)=2\times3=6$, and $A\times B$ has 6 pairs. ✓
:::

::: example Using n(A × B)
**Problem.** (i) If $n(A)=4$ and $n(A\times B)=20$, find $n(B)$. (ii) If $P=\{2,3\}$, list $P\times P$.

**Solution.** (i) $n(A\times B)=n(A)\times n(B)$ gives $20=4\times n(B)$, so $n(B)=5$.

(ii) $P\times P=\{(2,2),(2,3),(3,2),(3,3)\}$. It has $2\times2=4$ pairs. Notice that $(2,3)$ and $(3,2)$ are both present and are different pairs.
:::

## 1.3 Relation: meaning, representation (ordered pairs, table, arrow diagram, graph), domain and range, inverse relation

A Cartesian product contains every possible pair. Usually we are interested in only some of them, the ones that obey a rule. Take $A=\{1,2,3,4\}$ and $B=\{2,3,4,5,6\}$. The product $A\times B$ has $4\times5=20$ pairs. The rule "$y$ is 2 more than $x$" picks out just four of them:
$$ R=\{(1,3),(2,4),(3,5),(4,6)\} $$
This set of chosen pairs is a **relation**.

::: definition Relation
A **relation** $R$ from a set $A$ to a set $B$ is any **subset** of $A\times B$. If $(a,b)\in R$ we say "$a$ is related to $b$" and may write $a\,R\,b$. A relation from $A$ to $A$ itself is called a relation **on** $A$.
:::

Because a relation is a subset of $A\times B$, the empty set and $A\times B$ itself are also relations, although not interesting ones.

### Representing a relation

The relation "$y=x+2$" from $A=\{1,2,3,4\}$ to $B=\{2,3,4,5,6\}$ can be shown in five ways. All five carry the same information.

| Form | The relation $y=x+2$ |
|---|---|
| Ordered pairs (roster) | $R=\{(1,3),(2,4),(3,5),(4,6)\}$ |
| Set-builder | $R=\{(x,y): y=x+2,\ x\in A,\ y\in B\}$ |
| Table | $x$: 1, 2, 3, 4 and below it $y$: 3, 4, 5, 6 |
| Arrow diagram | arrows $1\rightarrow3$, $2\rightarrow4$, $3\rightarrow5$, $4\rightarrow6$ between two ovals |
| Graph | the four points $(1,3)$, $(2,4)$, $(3,5)$, $(4,6)$ |

```figure caption="The relation $R=\{(x,y): y=x+2\}$ from $A=\{1,2,3,4\}$ to $B=\{2,3,4,5,6\}$. Left: arrow diagram; the member 2 of $B$ receives no arrow, so it is not in the range. Right: the graph of the same four ordered pairs."
from matplotlib.patches import Ellipse
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.9))
ax1.set_xlim(0, 10); ax1.set_ylim(0, 10.4); ax1.axis('off')
ax1.add_patch(Ellipse((2.3, 4.9), 2.8, 8.6, fc='#eaf2fb', ec=ACCENT, lw=1.2))
ax1.add_patch(Ellipse((7.7, 4.9), 2.8, 8.6, fc='#fbecec', ec=SERIES[1], lw=1.2))
ax1.text(2.3, 9.8, 'A', ha='center', fontsize=10, color=ACCENT)
ax1.text(7.7, 9.8, 'B', ha='center', fontsize=10, color=SERIES[1])
ya = {1: 7.9, 2: 5.9, 3: 3.9, 4: 1.9}
yb = {2: 8.3, 3: 6.7, 4: 5.0, 5: 3.3, 6: 1.6}
for a, yy in ya.items():
    ax1.text(2.3, yy, str(a), ha='center', va='center', fontsize=10)
for b, yy in yb.items():
    ax1.text(7.7, yy, str(b), ha='center', va='center', fontsize=10, color=(MUTED if b == 2 else INK))
for a, y1 in ya.items():
    ax1.annotate('', xy=(7.25, yb[a + 2]), xytext=(2.75, y1), arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.1))
ax1.text(5.0, 0.0, 'y = x + 2', ha='center', fontsize=9, color=INK)
xs = [1, 2, 3, 4]
ax2.plot(xs, [v + 2 for v in xs], 'o', color=ACCENT, ms=5)
for v in xs:
    ax2.text(v - 0.15, v + 2 + 0.28, f'({v}, {v + 2})', fontsize=7.8, ha='right')
ax2.set_xlim(0, 4.6); ax2.set_ylim(0, 7)
ax2.set_xticks(range(0, 5)); ax2.set_yticks(range(0, 8))
ax2.set_xlabel('x (domain)', fontsize=8.5); ax2.set_ylabel('y (range)', fontsize=8.5)
ax2.grid(True, color=GRID, lw=0.6); ax2.set_axisbelow(True)
ax2.spines[['top', 'right']].set_visible(False); ax2.tick_params(labelsize=8)
fig.tight_layout(pad=0.4)
```

### Domain and range

::: definition Domain and range of a relation
The **domain** of a relation is the set of all **first components** of its ordered pairs. The **range** is the set of all **second components**.
:::

For $R=\{(1,3),(2,4),(3,5),(4,6)\}$ the domain is $\{1,2,3,4\}$ and the range is $\{3,4,5,6\}$. The member 2 of $B$ is not in the range, because no arrow reaches it in the arrow diagram above.

::: example A relation "is a factor of"
**Problem.** Let $A=\{2,3,5\}$ and $B=\{6,7,10,15\}$. Write the relation $R=\{(x,y): x \text{ is a factor of } y\}$ from $A$ to $B$ as a set of ordered pairs, and find its domain and range.

**Solution.** Test every member of $A$ against every member of $B$:

- 2 is a factor of 6 and 10, but not of 7 or 15.
- 3 is a factor of 6 and 15, but not of 7 or 10.
- 5 is a factor of 10 and 15, but not of 6 or 7.

$$ R=\{(2,6),(2,10),(3,6),(3,15),(5,10),(5,15)\} $$
Domain $=\{2,3,5\}$. Range $=\{6,10,15\}$. The number 7 is in $B$ but not in the range, because none of 2, 3, 5 divides 7.
:::

::: example A relation on one set
**Problem.** On the set $A=\{1,2,3,4\}$, write the relation "$x$ is less than $y$" as ordered pairs and find its domain and range.

**Solution.** We need all pairs $(x,y)$ from $A\times A$ with $x<y$:
$$ R=\{(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)\} $$
Domain $=\{1,2,3\}$ (4 is not less than any member of $A$). Range $=\{2,3,4\}$ (nothing in $A$ is less than 1).
:::

### Inverse relation

If Ram is the brother of Gita, then Gita is the sister of Ram: the same link read backwards. Reading every pair of a relation backwards gives its **inverse**.

::: definition Inverse relation
The **inverse** of a relation $R$ from $A$ to $B$ is the relation $R^{-1}$ from $B$ to $A$ obtained by **interchanging the components** of every ordered pair of $R$:
$$ R^{-1}=\{(y,x): (x,y)\in R\} $$
The domain of $R^{-1}$ is the range of $R$, and the range of $R^{-1}$ is the domain of $R$.
:::

In an arrow diagram, the inverse is drawn by reversing every arrow.

::: example Finding an inverse relation
**Problem.** Let $A=\{1,2,3\}$ and $B=\{1,4,9,16\}$, and $R=\{(x,y): y=x^2,\ x\in A,\ y\in B\}$. List $R$ and $R^{-1}$ and state the domain and range of each.

**Solution.** Squaring each member of $A$: $1^2=1$, $2^2=4$, $3^2=9$.
$$ R=\{(1,1),(2,4),(3,9)\} \qquad R^{-1}=\{(1,1),(4,2),(9,3)\} $$

| | Domain | Range |
|---|---|---|
| $R$ | $\{1,2,3\}$ | $\{1,4,9\}$ |
| $R^{-1}$ | $\{1,4,9\}$ | $\{1,2,3\}$ |

The rule of $R$ is "square $x$"; the rule of $R^{-1}$ is "take the positive square root of $x$". 16 is in $B$ but has no partner, because 4 is not in $A$.
:::

::: tip How many relations are possible?
A relation from $A$ to $B$ is a subset of $A\times B$, and a set with $k$ members has $2^k$ subsets. So if $n(A\times B)=k$, there are $2^k$ relations from $A$ to $B$. For $A=\{1,2\}$ and $B=\{a\}$, $A\times B=\{(1,a),(2,a)\}$ has 2 members, so there are $2^2=4$ relations: $\{\ \}$, $\{(1,a)\}$, $\{(2,a)\}$ and $\{(1,a),(2,a)\}$.
:::

## 1.4 Function: meaning and notation, domain, co-domain and range, image and pre-image

Three friends in Dhangadhi, Aayush, Binita and Chiran, were asked which games they like. Aayush likes football and chess, Binita likes cricket, and Chiran likes football. The relation "likes" is
$$ \{(\text{Aayush},\text{football}),(\text{Aayush},\text{chess}),(\text{Binita},\text{cricket}),(\text{Chiran},\text{football})\} $$
Now ask instead for each friend's **date of birth**. Every friend has one date of birth, never two. A relation like "has the date of birth", in which every member of the first set has **exactly one** partner, is a **function**. The relation "likes" is not a function, because Aayush has two partners.

::: definition Function
A **function** $f$ from a set $A$ to a set $B$ is a relation from $A$ to $B$ in which **every** member of $A$ is related to **exactly one** member of $B$. We write
$$ f: A\rightarrow B \qquad \text{and} \qquad y=f(x) $$
read "$f$ maps $A$ to $B$" and "$y$ equals $f$ of $x$".
:::

So a relation is a function when both of these hold:

1. **No member of $A$ is left out**: every member of $A$ has an arrow.
2. **No member of $A$ has two arrows**: no member of $A$ has two different partners.

Members of $B$ are free: some may receive no arrow and some may receive several.

### The words used with a function

| Word | Meaning | For $f(x)=2x+1$ on $A=\{0,1,2,3\}$ |
|---|---|---|
| Domain | the set $A$ of inputs | $\{0,1,2,3\}$ |
| Co-domain | the set $B$ in which outputs are allowed to lie | $B=\{1,2,3,4,5,6,7,8\}$ |
| Image of $x$ | the output $f(x)$ paired with $x$ | the image of 2 is $f(2)=5$ |
| Pre-image of $y$ | the input whose image is $y$ | the pre-image of 7 is 3 |
| Range | the set of all images, a subset of the co-domain | $\{1,3,5,7\}$ |

Think of a function as a machine. You feed in $x$; the machine applies its rule; out comes one value $f(x)$. A machine that sometimes gave two different answers for the same input would be broken, and so would a relation that gives one input two images.

```figure caption="Four arrow diagrams from $A=\{1,2,3\}$ to $B=\{a,b,c\}$. The first two are functions: every member of $A$ sends exactly one arrow. The third fails because 1 sends two arrows; the fourth fails because 3 sends none."
from matplotlib.patches import Ellipse
fig, axs = plt.subplots(2, 2, figsize=(5.0, 3.9))
cases = [([(1, 'a'), (2, 'b'), (3, 'c')], 'function (one-to-one)', SERIES[2]),
         ([(1, 'a'), (2, 'a'), (3, 'b')], 'function (many-to-one)', SERIES[2]),
         ([(1, 'a'), (1, 'b'), (2, 'c'), (3, 'c')], 'not a function: 1 has two images', SERIES[1]),
         ([(1, 'a'), (2, 'b')], 'not a function: 3 has no image', SERIES[1])]
ya = {1: 7.4, 2: 5.0, 3: 2.6}; yb = {'a': 7.4, 'b': 5.0, 'c': 2.6}
for ax, (arrows, title, col) in zip(axs.flat, cases):
    ax.set_xlim(0, 10); ax.set_ylim(0, 11); ax.axis('off')
    ax.add_patch(Ellipse((2.4, 5.0), 2.6, 7.8, fc='#eaf2fb', ec=ACCENT, lw=1.0))
    ax.add_patch(Ellipse((7.6, 5.0), 2.6, 7.8, fc='#fbecec', ec=SERIES[1], lw=1.0))
    for k, v in ya.items():
        ax.text(2.4, v, str(k), ha='center', va='center', fontsize=9)
    for k, v in yb.items():
        ax.text(7.6, v, k, ha='center', va='center', fontsize=9)
    for p, q in arrows:
        ax.annotate('', xy=(7.1, yb[q]), xytext=(2.9, ya[p]), arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.0))
    ax.text(5.0, 10.3, title, ha='center', fontsize=8, color=col)
fig.tight_layout(pad=0.3)
```

::: example Images, range and pre-images
**Problem.** A function $f: A\rightarrow B$ is defined by $f(x)=2x+1$, where $A=\{0,1,2,3\}$ and $B=\{1,2,3,4,5,6,7,8\}$. Find the image of each member of $A$, the range of $f$, and the pre-image of 5. Which members of $B$ have no pre-image?

**Solution.** Substitute each member of the domain into the rule:
$$ f(0)=2(0)+1=1,\quad f(1)=3,\quad f(2)=5,\quad f(3)=7 $$
Range $=\{1,3,5,7\}$, which is a subset of the co-domain $B$.

The pre-image of 5 is the $x$ with $2x+1=5$, that is $x=2$.

The members 2, 4, 6 and 8 of $B$ receive no arrow, so they have no pre-image. This is allowed: only the members of the **domain** must all be used.
:::

::: example Values of a function and a many-to-one function
**Problem.** If $f(x)=x^2-3x+2$, find $f(0)$, $f(1)$, $f(-2)$ and $f(3)$. Then find the pre-images of 0.

**Solution.**
$$ f(0)=0-0+2=2,\qquad f(1)=1-3+2=0 $$
$$ f(-2)=(-2)^2-3(-2)+2=4+6+2=12,\qquad f(3)=9-9+2=2 $$
For the pre-images of 0, solve $x^2-3x+2=0$, i.e. $(x-1)(x-2)=0$, so $x=1$ or $x=2$.

Notice that $f(0)=f(3)=2$: two inputs share one image. That is allowed in a function (it is **many-to-one**). What is never allowed is one input with two images.
:::

::: example Finding the rule of a linear function
**Problem.** A function is defined by $f(x)=ax+b$. If $f(1)=5$ and $f(3)=11$, find $a$ and $b$. Hence find $f(5)$.

**Solution.** Put $x=1$ and $x=3$ in the rule:
$$ a+b=5 \qquad \text{(i)} \qquad\qquad 3a+b=11 \qquad \text{(ii)} $$
Subtract (i) from (ii): $2a=6$, so $a=3$. From (i): $b=5-3=2$. So $f(x)=3x+2$ and $f(5)=3(5)+2=17$.

**Check.** $f(1)=3+2=5$ ✓ and $f(3)=9+2=11$ ✓.
:::

::: caution Range is not the same as co-domain
The **co-domain** is the whole set $B$ named in $f: A\rightarrow B$. The **range** is only the part of $B$ that is actually hit by arrows. In the first example above the co-domain has 8 members but the range has only 4. When a question asks for the range, list the images, not the whole of $B$.
:::

## 1.5 Representation of a function and the vertical line test

A function can be given in any of the forms used for a relation. Here is $f(x)=2x-1$ with domain $\{-1,0,1,2,3\}$ in each form.

| Form | $f(x)=2x-1$ on $\{-1,0,1,2,3\}$ |
|---|---|
| Formula | $f(x)=2x-1$, or $y=2x-1$ |
| Table | $x$: $-1$, 0, 1, 2, 3 and $y$: $-3$, $-1$, 1, 3, 5 |
| Ordered pairs | $\{(-1,-3),(0,-1),(1,1),(2,3),(3,5)\}$ |
| Arrow diagram | $-1\rightarrow-3$, $0\rightarrow-1$, $1\rightarrow1$, $2\rightarrow3$, $3\rightarrow5$ |
| Graph | the five points plotted; they lie on one straight line |

In the ordered-pair form a function is easy to recognise: **no first component appears twice**. The set $\{(1,2),(2,3),(1,5)\}$ is not a function, because 1 appears as a first component with two different second components.

### The vertical line test

On a graph, all points with the same first component lie on one **vertical** line. If a vertical line cuts a graph twice, the input at that line has two outputs, and the graph is not a function.

::: key Vertical line test
A graph is the graph of a function of $x$ if **no vertical line meets it at more than one point**. If even one vertical line meets the graph twice or more, the graph is not a function.
:::

```figure caption="The vertical line test. A dashed vertical line is drawn on each graph. It meets the straight line $y=2x-1$ and the curve $y=x^2-2$ only once, so both are functions; it meets the circle $x^2+y^2=9$ and the curve $x=y^2$ twice, so these are not functions."
fig, axs = plt.subplots(2, 2, figsize=(5.0, 4.0))
t = np.linspace(-3.2, 3.2, 300)
panels = [('y = 2x − 1 : function', SERIES[2]), ('y = x² − 2 : function', SERIES[2]),
          ('x² + y² = 9 : not a function', SERIES[1]), ('x = y² : not a function', SERIES[1])]
for k, (ax, (title, col)) in enumerate(zip(axs.flat, panels)):
    ax.axhline(0, color=MUTED, lw=0.7); ax.axvline(0, color=MUTED, lw=0.7)
    ax.set_xlim(-3.6, 3.6); ax.set_ylim(-3.6, 3.6); ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title(title, fontsize=8, color=col, pad=2)
    xv = 1.0
    if k == 0:
        xs = np.linspace(-1.2, 2.2, 50); ax.plot(xs, 2*xs - 1, color=ACCENT)
        hits = [(xv, 2*xv - 1)]
    elif k == 1:
        xs = np.linspace(-2.3, 2.3, 200); ax.plot(xs, xs**2 - 2, color=ACCENT)
        hits = [(xv, xv**2 - 2)]
    elif k == 2:
        a = np.linspace(0, 2*np.pi, 300); ax.plot(3*np.cos(a), 3*np.sin(a), color=ACCENT)
        hits = [(xv, np.sqrt(9 - xv**2)), (xv, -np.sqrt(9 - xv**2))]
    else:
        ys = np.linspace(-1.85, 1.85, 200); ax.plot(ys**2, ys, color=ACCENT)
        hits = [(xv, 1.0), (xv, -1.0)]
    ax.plot([xv, xv], [-3.5, 3.5], ls='--', color=SERIES[3], lw=1.1)
    for hx, hy in hits:
        ax.plot(hx, hy, 'o', color=SERIES[1], ms=5)
fig.tight_layout(pad=0.4)
```

::: example Applying the test to sets of ordered pairs
**Problem.** Which of these relations are functions? Give a reason for each.
(i) $R_1=\{(-1,1),(0,0),(1,1),(2,4)\}$ (ii) $R_2=\{(1,1),(1,-1),(4,2),(4,-2)\}$

**Solution.** (i) The first components $-1, 0, 1, 2$ are all different, so each input has exactly one output. $R_1$ **is a function** (its rule is $y=x^2$). Two inputs, $-1$ and $1$, share the output 1, which is allowed.

(ii) The first component 1 appears with 1 and with $-1$, so the input 1 has two outputs. $R_2$ **is not a function**. On a graph, the vertical line $x=1$ would pass through both $(1,1)$ and $(1,-1)$.
:::

::: example From a table to a graph
**Problem.** For $f(x)=2x-1$ with domain $\{-1,0,1,2,3\}$, make a table, list the range and say why the graph passes the vertical line test.

**Solution.**

| $x$ | $-1$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|
| $f(x)=2x-1$ | $-3$ | $-1$ | 1 | 3 | 5 |

Range $=\{-3,-1,1,3,5\}$. The graph is five points, each with a different $x$-coordinate, so every vertical line meets the graph at most once. It is the graph of a function.
:::

::: tip Writing a reason that earns the mark
A bare "yes" or "no" rarely earns the full mark. Write the reason in the language of the definition: "It is a function because every member of $A$ has exactly one image", or "It is not a function because 2 has two images, 6 and 7", or "It is not a function because 3 has no image".
:::

::: note Activity — the class birthday function
Make a table of six classmates and the month in which each was born. (1) Draw the arrow diagram from the set of students to the set of twelve months. Is it a function? (It must be: nobody has two birth months.) (2) Which months form the range? Which members of the co-domain have no pre-image? (3) Now reverse the arrows to get the inverse relation, from months to students. Is the inverse a function? It fails if two friends share a month, or if some month has no friend. (4) Finally, hold a ruler upright and slide it across the four graphs of the vertical line test to see the vertical line test for yourself.
:::

## Chapter summary

- An **ordered pair** $(a,b)$ has a first and a second component; $(a,b)=(c,d)$ exactly when $a=c$ and $b=d$.
- The **Cartesian product** $A\times B=\{(a,b): a\in A,\ b\in B\}$; $n(A\times B)=n(A)\times n(B)$; $A\times B\neq B\times A$ unless $A=B$.
- A **relation** from $A$ to $B$ is a subset of $A\times B$; it can be shown by ordered pairs, set-builder form, a table, an arrow diagram or a graph.
- **Domain** = set of first components; **range** = set of second components.
- The **inverse** $R^{-1}=\{(y,x): (x,y)\in R\}$ swaps the domain and the range.
- A **function** $f: A\rightarrow B$ is a relation in which every member of $A$ has **exactly one** image; members of $B$ may have none or several pre-images.
- For $y=f(x)$: $y$ is the **image** of $x$, $x$ is the **pre-image** of $y$; the range is a subset of the **co-domain**.
- **Vertical line test:** a graph is a function of $x$ if no vertical line meets it more than once.

## Practice questions

**Group A — Objective (1 mark each)**

1. If $(x-2,\ 5)=(3,\ y+1)$, then $(x,y)$ is <span class="marks">[1]</span>
   (a) $(1,4)$ (b) $(5,4)$ (c) $(5,6)$ (d) $(1,6)$
2. If $n(A)=3$ and $n(B)=4$, then $n(A\times B)$ is <span class="marks">[1]</span>
   (a) 7 (b) 12 (c) 64 (d) 81
3. If $A=\{1,2\}$ and $B=\{3\}$, then $A\times B$ is <span class="marks">[1]</span>
   (a) $\{(1,3),(2,3)\}$ (b) $\{(3,1),(3,2)\}$ (c) $\{1,2,3\}$ (d) $\{(1,2),(2,3)\}$
4. A relation from a set $A$ to a set $B$ is always <span class="marks">[1]</span>
   (a) a subset of $A\times B$ (b) a subset of $A$ (c) equal to $A\times B$ (d) a subset of $B$
5. The domain of $R=\{(1,4),(2,5),(3,4)\}$ is <span class="marks">[1]</span>
   (a) $\{4,5\}$ (b) $\{1,2,3\}$ (c) $\{1,2,3,4,5\}$ (d) $\{1,4\}$
6. The inverse of $R=\{(2,5),(3,7)\}$ is <span class="marks">[1]</span>
   (a) $\{(5,2),(7,3)\}$ (b) $\{(2,7),(3,5)\}$ (c) $\{(-2,-5),(-3,-7)\}$ (d) $\{(5,7),(2,3)\}$
7. Which of these relations is a function? <span class="marks">[1]</span>
   (a) $\{(1,2),(1,3)\}$ (b) $\{(1,2),(2,2),(3,2)\}$ (c) $\{(2,1),(2,3),(4,5)\}$ (d) $\{(1,1),(1,-1)\}$
8. If $f(x)=3x-5$, then $f(4)$ is <span class="marks">[1]</span>
   (a) 7 (b) 12 (c) 17 (d) $-7$
9. If $f(x)=2x+3$ and $f(a)=11$, then $a$ is <span class="marks">[1]</span>
   (a) 4 (b) 7 (c) 25 (d) 3
10. For a function $f: A\rightarrow B$, the set $B$ is called the <span class="marks">[1]</span>
    (a) domain (b) range (c) co-domain (d) pre-image
11. A graph represents a function of $x$ if every vertical line meets it <span class="marks">[1]</span>
    (a) at least twice (b) at most once (c) exactly twice (d) never
12. If $A\times B=\{(a,1),(a,2),(b,1),(b,2)\}$, then $B$ is <span class="marks">[1]</span>
    (a) $\{a,b\}$ (b) $\{1,2\}$ (c) $\{a,1\}$ (d) $\{(1,2)\}$

::: note Answers to Group A
**1.** (b) — $x-2=3$ gives $x=5$; $5=y+1$ gives $y=4$.
**2.** (b) — $n(A\times B)=3\times4=12$.
**3.** (a) — first components from $A$, second from $B$.
**4.** (a) — a relation is any subset of $A\times B$.
**5.** (b) — the domain is the set of first components.
**6.** (a) — interchange the components of each pair.
**7.** (b) — each first component appears once; the others repeat a first component.
**8.** (a) — $3(4)-5=12-5=7$.
**9.** (a) — $2a+3=11$, so $2a=8$ and $a=4$.
**10.** (c) — $B$ is the co-domain; the range is the part of $B$ that is used.
**11.** (b) — two meeting points would give one input two outputs.
**12.** (b) — $B$ is the set of second components.
:::

**Group B — Short answer (2 marks each)**

1. Find $x$ and $y$ if $(2x+1,\ y-3)=(7,\ 2)$. <span class="marks">[2]</span>
2. If $A=\{a,b\}$ and $B=\{1,2,3\}$, find $A\times B$ and $n(A\times B)$. <span class="marks">[2]</span>
3. If $A=\{2,4\}$ and $B=\{1,3\}$, find $B\times A$ and show that $A\times B\neq B\times A$. <span class="marks">[2]</span>
4. If $n(A\times B)=6$ and $n(B)=3$, find $n(A)$ and the number of relations from $A$ to $B$. <span class="marks">[2]</span>
5. If $A=\{1,2,3\}$, $B=\{2,3,4,5,6\}$ and $R=\{(x,y): y=2x\}$ from $A$ to $B$, list $R$ and find its domain and range. <span class="marks">[2]</span>
6. Find the inverse of $R=\{(1,2),(2,4),(3,6)\}$ and state its domain and range. <span class="marks">[2]</span>
7. If $f(x)=x^2+1$, find $f(-2)$ and $f(3)$. <span class="marks">[2]</span>
8. If $f(x)=4x-3$, find the pre-image of 9. <span class="marks">[2]</span>
9. State, with a reason, whether $\{(1,5),(2,6),(2,7),(3,8)\}$ is a function. <span class="marks">[2]</span>
10. A function $f: A\rightarrow B$ is defined by $f(x)=x+3$, where $A=\{-1,0,1,2\}$. Find its range. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** First components: $2x+1=7$, so $x=3$. Second components: $y-3=2$, so $y=5$.
**2.** $A\times B=\{(a,1),(a,2),(a,3),(b,1),(b,2),(b,3)\}$; $n(A\times B)=2\times3=6$.
**3.** $B\times A=\{(1,2),(1,4),(3,2),(3,4)\}$ and $A\times B=\{(2,1),(2,3),(4,1),(4,3)\}$. The pair $(1,2)$ is in $B\times A$ but not in $A\times B$, so the sets are not equal.
**4.** $n(A)\times3=6$, so $n(A)=2$. A relation is a subset of $A\times B$, which has 6 members, so there are $2^6=64$ relations.
**5.** $R=\{(1,2),(2,4),(3,6)\}$; domain $=\{1,2,3\}$; range $=\{2,4,6\}$.
**6.** $R^{-1}=\{(2,1),(4,2),(6,3)\}$; domain of $R^{-1}=\{2,4,6\}$; range of $R^{-1}=\{1,2,3\}$.
**7.** $f(-2)=(-2)^2+1=5$ and $f(3)=3^2+1=10$.
**8.** $4x-3=9$, so $4x=12$ and $x=3$. The pre-image of 9 is 3.
**9.** It is **not** a function, because the first component 2 has two images, 6 and 7.
**10.** $f(-1)=2$, $f(0)=3$, $f(1)=4$, $f(2)=5$, so the range is $\{2,3,4,5\}$.
:::

**Group C — Long answer (4 marks each)**

1. If $(x+y,\ 3)=(7,\ x-y)$, find $x$ and $y$. Taking $A=\{x,y\}$ and $B=\{1,2\}$, find $A\times B$ and $B\times A$, and verify that $n(A\times B)=n(B\times A)$. <span class="marks">[4]</span>
2. Let $A=\{1,2,3,4\}$ and $B=\{1,3,5,7,9\}$, and let $R=\{(x,y): y=2x-1,\ x\in A,\ y\in B\}$. (i) List $R$. (ii) Show it in an arrow diagram. (iii) Find its domain and range. (iv) Find $R^{-1}$. Is $R$ a function from $A$ to $B$? <span class="marks">[4]</span>
3. A function is defined by $f(x)=ax+b$. If $f(1)=1$ and $f(3)=7$, find $a$ and $b$. Then find $f(5)$ and the pre-image of 10. <span class="marks">[4]</span>
4. For $f(x)=2x-1$ with domain $\{-1,0,1,2,3\}$: (i) make a table of values, (ii) write $f$ as a set of ordered pairs, (iii) find the range, (iv) plot the points and explain why they pass the vertical line test. <span class="marks">[4]</span>
5. Let $A=\{1,2,3\}$ and $B=\{4,5,6\}$. For each relation below, draw an arrow diagram and say whether it is a function from $A$ to $B$, giving a reason: $R_1=\{(1,4),(2,5),(3,6)\}$, $R_2=\{(1,4),(2,4),(3,4)\}$, $R_3=\{(1,4),(1,5),(2,6),(3,6)\}$, $R_4=\{(1,5),(2,6)\}$. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Equating components: $x+y=7$ and $x-y=3$. Adding, $2x=10$, so $x=5$ and $y=2$. Then $A=\{2,5\}$ and $B=\{1,2\}$. $A\times B=\{(2,1),(2,2),(5,1),(5,2)\}$ and $B\times A=\{(1,2),(1,5),(2,2),(2,5)\}$. Each has 4 members, so $n(A\times B)=n(B\times A)=4=2\times2$, although the two sets are different.
**2.** (i) $y=2x-1$ gives $1\rightarrow1$, $2\rightarrow3$, $3\rightarrow5$, $4\rightarrow7$, so $R=\{(1,1),(2,3),(3,5),(4,7)\}$. (ii) Two ovals with 1, 2, 3, 4 on the left and 1, 3, 5, 7, 9 on the right, with the four arrows above; 9 receives no arrow. (iii) Domain $=\{1,2,3,4\}$; range $=\{1,3,5,7\}$. (iv) $R^{-1}=\{(1,1),(3,2),(5,3),(7,4)\}$. $R$ **is a function**, because every member of $A$ has exactly one image.
**3.** $f(1)=a+b=1$ and $f(3)=3a+b=7$. Subtracting, $2a=6$, so $a=3$ and $b=1-3=-2$. Thus $f(x)=3x-2$, so $f(5)=15-2=13$. For the pre-image of 10: $3x-2=10$, so $3x=12$ and $x=4$. Check: $f(1)=1$ ✓, $f(3)=7$ ✓.
**4.** (i) $x$: $-1, 0, 1, 2, 3$ give $f(x)$: $-3, -1, 1, 3, 5$. (ii) $f=\{(-1,-3),(0,-1),(1,1),(2,3),(3,5)\}$. (iii) Range $=\{-3,-1,1,3,5\}$. (iv) The five points lie on a straight line rising 2 units for every 1 unit to the right. Their $x$-coordinates are all different, so any vertical line passes through at most one of them: the graph passes the test, as a function must.
**5.** $R_1$: function, one-to-one; each of 1, 2, 3 has exactly one image. $R_2$: function, many-to-one; each member of $A$ has exactly one image, all equal to 4 (a constant function). $R_3$: **not** a function; 1 has two images, 4 and 5. $R_4$: **not** a function; 3 has no image.
:::
