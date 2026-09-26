---
subject: Mathematics
grade: 11
unit: 1
title: Logic and Set
hours: 8
area: Algebra
---

Every theorem you will meet this year has the same shape: *given* something, *therefore*
something else. Logic is the study of that word "therefore" — the rules that let you move
from one true statement to the next without error. Sets are the language those statements
are written in. This unit is short on computation and heavy on precision, so read the
definitions slowly: a single misplaced "or" changes the answer.

::: key What the exam asks for
Three things recur in every paper: (i) build a **truth table** and name the result
(tautology / contradiction), (ii) **prove** a set identity either by element-chasing or by
Venn diagram, and (iii) a **survey word problem** using $n(A \cup B)$ or the three-set
formula. Group A usually takes one mark from truth values and one from cardinality.
:::

## 1.1 Statements; logical connectives

::: definition Statement (proposition)
A **statement** is a declarative sentence which is either **true** or **false**, but not
both. Whether it is true or false is called its **truth value**, written T or F.
:::

Commands, questions, exclamations and opinions are not statements. Neither is a sentence
containing an unknown, because its truth depends on the unknown.

| Sentence | Statement? | Why |
|---|---|---|
| Kathmandu is the capital of Nepal. | Yes (T) | Definitely true |
| $3 + 4 = 9$ | Yes (F) | Definitely false |
| Every prime number is odd. | Yes (F) | $2$ is an even prime |
| Close the door. | No | A command |
| Where do you live? | No | A question |
| $x + 2 = 5$ | No | Truth value depends on $x$ |
| Mathematics is beautiful. | No | An opinion |

A sentence like $x + 2 = 5$ is called an **open sentence**. The set of values that make it
true — here $\{3\}$ — is its **truth set**.

A statement carrying no connective is **simple**; statements joined by connectives are
**compound**. Simple statements are labelled $p, q, r, \dots$

::: key The five connectives
| Name | Symbol | Read as | Called |
|---|---|---|---|
| Negation | $\sim p$ | "not $p$" | — |
| Conjunction | $p \wedge q$ | "$p$ **and** $q$" | conjuncts |
| Disjunction | $p \vee q$ | "$p$ **or** $q$" (inclusive) | disjuncts |
| Conditional | $p \rightarrow q$ | "**if** $p$ **then** $q$" | $p$ antecedent, $q$ consequent |
| Biconditional | $p \leftrightarrow q$ | "$p$ **if and only if** $q$" | — |
:::

The mathematical "or" is **inclusive**: $p \vee q$ is true when $p$ is true, when $q$ is
true, and when both are true. Everyday Nepali and English often mean "or" exclusively
("tea or coffee"); mathematics never does.

The conditional $p \rightarrow q$ is the one students find strange. It claims only that
$q$ cannot fail while $p$ holds. So it is **false in exactly one case**: $p$ true and $q$
false. If $p$ is false the whole conditional is automatically true (the promise was never
tested). The statement "if $2 = 3$ then the moon is square" is true.

### Related conditionals

From $p \rightarrow q$ three further conditionals are formed.

| Name | Form |
|---|---|
| Converse | $q \rightarrow p$ |
| Inverse | $\sim p \rightarrow \sim q$ |
| Contrapositive | $\sim q \rightarrow \sim p$ |

```figure caption="The four related conditionals. Statements joined by the dashed diagonals are logically equivalent; the horizontal and vertical pairs are not."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,2.9))
box = dict(boxstyle='round,pad=0.30', fc='#eef4fa', ec=ACCENT, lw=1.0)
box2 = dict(boxstyle='round,pad=0.30', fc='#f6f6f8', ec=MUTED, lw=1.0)
pos = {'orig':(0,1),'conv':(1,1),'inv':(0,0),'cont':(1,0)}
lab = {'orig':'Original\n$p \\rightarrow q$','conv':'Converse\n$q \\rightarrow p$',
       'inv':'Inverse\n$\\sim p \\rightarrow \\sim q$','cont':'Contrapositive\n$\\sim q \\rightarrow \\sim p$'}
for k,(X,Y) in pos.items():
    ax.text(X, Y, lab[k], ha='center', va='center', fontsize=9,
            color=INK, bbox=(box if k in ('orig','cont') else box2))
ax.annotate('', xy=(0.82,0.16), xytext=(0.18,0.84),
            arrowprops=dict(arrowstyle='<|-|>', color=ACCENT, lw=1.3, ls=(0,(4,2)),
                            mutation_scale=11, shrinkA=6, shrinkB=6))
ax.annotate('', xy=(0.18,0.16), xytext=(0.82,0.84),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.3, ls=(0,(4,2)),
                            mutation_scale=11, shrinkA=6, shrinkB=6))
ax.text(0.5,0.52,'equivalent', fontsize=8.4, color=ACCENT, ha='center',
        rotation=-38, backgroundcolor='white')
ax.set_xlim(-0.42,1.42); ax.set_ylim(-0.32,1.32); ax.axis('off')
```

::: caution Converse is not the same as the original
"If a number is divisible by $6$, then it is divisible by $3$" is **true**. Its converse,
"if a number is divisible by $3$ then it is divisible by $6$", is **false** ($9$ is a
counter-example). Only the **contrapositive** always has the same truth value as the
original — which is why proof by contrapositive is legal and "proof by converse" is not.
:::

### Quantifiers

- **Universal quantifier** $\forall$ — "for all". $\forall x \in \mathbb{R},\ x^2 \geq 0$.
- **Existential quantifier** $\exists$ — "there exists". $\exists x \in \mathbb{R}$ such that $x^2 = 4$.

Negation swaps them: $\sim(\forall x,\ p(x)) \equiv \exists x,\ \sim p(x)$ and
$\sim(\exists x,\ p(x)) \equiv \forall x,\ \sim p(x)$. "Not every student passed" means
"some student failed".

::: example Worked example 1.1
**Problem.** Let $p$: "Sita is a doctor" and $q$: "Sita is a singer". Write in symbols:
(a) Sita is a doctor but not a singer. (b) If Sita is not a doctor then she is a singer.
(c) Sita is neither a doctor nor a singer.

**Solution.**

(a) "but" is just **and**, so this is $p \wedge \sim q$.

(b) The antecedent is "$\sim p$" and the consequent is "$q$": $\sim p \rightarrow q$.

(c) "Neither $A$ nor $B$" means "not $A$ **and** not $B$": $\sim p \wedge \sim q$.
By De Morgan's law this is the same as $\sim(p \vee q)$.
:::

::: example Worked example 1.2
**Problem.** Write the converse, inverse and contrapositive of: "If a triangle is
equilateral, then it is isosceles." State the truth value of each.

**Solution.** Let $p$: the triangle is equilateral; $q$: the triangle is isosceles.
The given statement is $p \rightarrow q$, which is **true** (all three sides equal implies
at least two equal).

- **Converse** ($q \rightarrow p$): "If a triangle is isosceles, then it is equilateral."
  **False** — a triangle with sides $5, 5, 8$ is isosceles but not equilateral.
- **Inverse** ($\sim p \rightarrow \sim q$): "If a triangle is not equilateral, then it is
  not isosceles." **False** — same counter-example.
- **Contrapositive** ($\sim q \rightarrow \sim p$): "If a triangle is not isosceles, then
  it is not equilateral." **True**, as it must be, being equivalent to the original.
:::

## 1.2 Truth tables

A **truth table** lists every possible combination of truth values of the simple
statements and works out the truth value of the compound statement in each case. With $n$
simple statements there are $2^n$ rows: $2$ rows for one letter, $4$ for two, $8$ for
three. Fill the input columns in a fixed order so you never miss a row.

::: key The five basic truth tables
| $p$ | $q$ | $\sim p$ | $p \wedge q$ | $p \vee q$ | $p \rightarrow q$ | $p \leftrightarrow q$ |
|---|---|---|---|---|---|---|
| T | T | F | T | T | T | T |
| T | F | F | F | T | **F** | F |
| F | T | T | F | T | T | F |
| F | F | T | F | F | T | T |

$p \wedge q$ is true **only** in row 1. $p \vee q$ is false **only** in row 4.
$p \rightarrow q$ is false **only** in row 2. $p \leftrightarrow q$ is true exactly when
the two truth values agree.
:::

::: definition Tautology, contradiction, contingency
A compound statement whose last column is **all T** is a **tautology**; all **F** is a
**contradiction**; a mixture is a **contingency**. Two statements are **logically
equivalent** (written $\equiv$) when their final columns are identical, i.e. when the
biconditional between them is a tautology.
:::

**Example table 1 — a tautology.** $(p \wedge q) \rightarrow p$

| $p$ | $q$ | $p \wedge q$ | $(p \wedge q) \rightarrow p$ |
|---|---|---|---|
| T | T | T | T |
| T | F | F | T |
| F | T | F | T |
| F | F | F | T |

Every entry in the last column is T, so it is a tautology.

**Example table 2 — a contradiction.** $p \wedge \sim p$

| $p$ | $\sim p$ | $p \wedge \sim p$ |
|---|---|---|
| T | F | F |
| F | T | F |

**Example table 3 — the conditional rewritten.** $p \rightarrow q \equiv \sim p \vee q$

| $p$ | $q$ | $\sim p$ | $p \rightarrow q$ | $\sim p \vee q$ |
|---|---|---|---|---|
| T | T | F | T | T |
| T | F | F | F | F |
| F | T | T | T | T |
| F | F | T | T | T |

The last two columns agree in all four rows, so the two statements are equivalent. This
is how a conditional is removed when simplifying.

**Example table 4 — contrapositive, converse and inverse.**

| $p$ | $q$ | $\sim p$ | $\sim q$ | $p \rightarrow q$ | $\sim q \rightarrow \sim p$ | $q \rightarrow p$ | $\sim p \rightarrow \sim q$ |
|---|---|---|---|---|---|---|---|
| T | T | F | F | T | T | T | T |
| T | F | F | T | F | F | T | T |
| F | T | T | F | T | T | F | F |
| F | F | T | T | T | T | T | T |

Columns 5 and 6 are identical: **a conditional is equivalent to its contrapositive**.
Columns 7 and 8 are identical: **the converse is equivalent to the inverse**. Columns 5
and 7 differ in rows 2 and 3, so a conditional is *not* equivalent to its converse.

::: example Worked example 1.3
**Problem.** Using a truth table, prove De Morgan's law
$\sim(p \vee q) \equiv \sim p \wedge \sim q$.

**Solution.** Two letters, so four rows.

| $p$ | $q$ | $p \vee q$ | $\sim(p \vee q)$ | $\sim p$ | $\sim q$ | $\sim p \wedge \sim q$ |
|---|---|---|---|---|---|---|
| T | T | T | F | F | F | F |
| T | F | T | F | F | T | F |
| F | T | T | F | T | F | F |
| F | F | F | T | T | T | T |

Column 4 and column 7 are identical (F, F, F, T), so the two statements are logically
equivalent. Hence $\sim(p \vee q) \leftrightarrow (\sim p \wedge \sim q)$ is a tautology.
:::

::: example Worked example 1.4
**Problem.** Construct the truth table for $p \vee (q \wedge r)$ and for
$(p \vee q) \wedge (p \vee r)$, and hence verify the distributive law.

**Solution.** Three letters, so $2^3 = 8$ rows.

| $p$ | $q$ | $r$ | $q \wedge r$ | $p \vee (q \wedge r)$ | $p \vee q$ | $p \vee r$ | $(p \vee q) \wedge (p \vee r)$ |
|---|---|---|---|---|---|---|---|
| T | T | T | T | T | T | T | T |
| T | T | F | F | T | T | T | T |
| T | F | T | F | T | T | T | T |
| T | F | F | F | T | T | T | T |
| F | T | T | T | T | T | T | T |
| F | T | F | F | F | T | F | F |
| F | F | T | F | F | F | T | F |
| F | F | F | F | F | F | F | F |

Columns 5 and 8 agree row by row (T,T,T,T,T,F,F,F), so
$p \vee (q \wedge r) \equiv (p \vee q) \wedge (p \vee r)$.
:::

::: example Worked example 1.5
**Problem.** Test whether $(p \rightarrow q) \wedge (q \rightarrow p)$ is equivalent to
$p \leftrightarrow q$.

**Solution.**

| $p$ | $q$ | $p \rightarrow q$ | $q \rightarrow p$ | $(p \rightarrow q) \wedge (q \rightarrow p)$ | $p \leftrightarrow q$ |
|---|---|---|---|---|---|
| T | T | T | T | T | T |
| T | F | F | T | F | F |
| F | T | T | F | F | F |
| F | F | T | T | T | T |

The last two columns are identical, so the two are equivalent. This is why proving "if and
only if" means proving **both** directions.
:::

::: memory Laws of logic worth memorising
With $t$ a tautology and $c$ a contradiction:

- Idempotent: $p \vee p \equiv p$, $p \wedge p \equiv p$
- Commutative: $p \vee q \equiv q \vee p$, $p \wedge q \equiv q \wedge p$
- Associative: $(p \vee q) \vee r \equiv p \vee (q \vee r)$
- Distributive: $p \wedge (q \vee r) \equiv (p \wedge q) \vee (p \wedge r)$
- De Morgan: $\sim(p \vee q) \equiv \sim p \wedge \sim q$, $\sim(p \wedge q) \equiv \sim p \vee \sim q$
- Identity: $p \vee c \equiv p$, $p \wedge t \equiv p$
- Complement: $p \vee \sim p \equiv t$, $p \wedge \sim p \equiv c$, $\sim(\sim p) \equiv p$
- Conditional: $p \rightarrow q \equiv \sim p \vee q \equiv \sim q \rightarrow \sim p$
:::

## 1.3 Theorems based on set operations

A **set** is a well-defined collection of distinct objects, its **elements**. Written in
**roster form** $A = \{2, 3, 5, 7\}$ or **set-builder form**
$A = \{x : x \text{ is a prime} , x < 10\}$. Write $x \in A$ if $x$ belongs to $A$ and
$x \notin A$ otherwise. The number of elements of a finite set $A$ is its **cardinal
number** $n(A)$.

| Term | Meaning |
|---|---|
| Empty set $\emptyset$ | the set with no element; $n(\emptyset) = 0$ |
| Subset $A \subseteq B$ | every element of $A$ is in $B$ |
| Proper subset $A \subset B$ | $A \subseteq B$ and $A \ne B$ |
| Equal sets $A = B$ | $A \subseteq B$ and $B \subseteq A$ |
| Universal set $U$ | the set of all elements under discussion |
| Power set $P(A)$ | the set of **all** subsets of $A$; $n(P(A)) = 2^{n(A)}$ |

::: definition The four set operations
For subsets $A, B$ of a universal set $U$:

$$ A \cup B = \{x : x \in A \text{ or } x \in B\} $$
$$ A \cap B = \{x : x \in A \text{ and } x \in B\} $$
$$ A - B = \{x : x \in A \text{ and } x \notin B\} $$
$$ A^c = A' = U - A = \{x : x \in U \text{ and } x \notin A\} $$

$A$ and $B$ are **disjoint** when $A \cap B = \emptyset$. The **symmetric difference** is
$A \triangle B = (A - B) \cup (B - A)$.
:::

```figure caption="The four set operations. In each panel the shaded region is the named set; the outer rectangle is the universal set $U$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, axes = plt.subplots(2, 2, figsize=(5.0,3.4))
cA, cB, r = (-0.42, 0.0), (0.42, 0.0), 0.84
def inA(X, Y): return (X-cA[0])**2 + (Y-cA[1])**2 <= r*r
def inB(X, Y): return (X-cB[0])**2 + (Y-cB[1])**2 <= r*r
xs = np.linspace(-2.0, 2.0, 520); ys = np.linspace(-1.25, 1.25, 340)
X, Y = np.meshgrid(xs, ys)
specs = [('$A \\cup B$', inA(X,Y) | inB(X,Y)),
         ('$A \\cap B$', inA(X,Y) & inB(X,Y)),
         ('$A - B$',     inA(X,Y) & ~inB(X,Y)),
         ('$A^c$',       ~inA(X,Y))]
for ax, (t, M) in zip(axes.ravel(), specs):
    ax.add_patch(Rectangle((-2.0,-1.25), 4.0, 2.5, fill=False, ec=MUTED, lw=0.9))
    ax.contourf(X, Y, M.astype(float), levels=[0.5,1.5], colors=[ACCENT], alpha=0.30)
    ax.add_patch(Circle(cA, r, fill=False, ec=INK, lw=1.2))
    ax.add_patch(Circle(cB, r, fill=False, ec=INK, lw=1.2))
    ax.text(-0.95, 0.98, 'A', fontsize=9.8, color=INK, style='italic', ha='center')
    ax.text(0.95, 0.98, 'B', fontsize=9.8, color=INK, style='italic', ha='center')
    ax.text(-1.90, 1.00, 'U', fontsize=8.6, color=MUTED, style='italic')
    ax.set_title(t, fontsize=9.8, pad=3)
    ax.set_xlim(-2.06, 2.06); ax.set_ylim(-1.31, 1.31)
    ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(h_pad=0.4)
```

```figure caption="Special positions: $A \subseteq B$ (left) and disjoint sets $A \cap B = \emptyset$ (right)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, axes = plt.subplots(1, 2, figsize=(4.8,2.4))
ax = axes[0]
ax.add_patch(Rectangle((-1.8,-1.15), 3.6, 2.3, fill=False, ec=MUTED, lw=0.9))
ax.add_patch(Circle((0,0), 1.0, fc=ACCENT, alpha=0.13, ec=INK, lw=1.2))
ax.add_patch(Circle((-0.20,-0.05), 0.48, fc=ACCENT, alpha=0.30, ec=INK, lw=1.2))
ax.text(-0.22,-0.09,'A', fontsize=9.5, color=INK, ha='center', style='italic')
ax.text(0.62, 0.62,'B', fontsize=9.5, color=INK, style='italic')
ax.set_title('$A \\subseteq B$', fontsize=9.8, pad=3)
ax = axes[1]
ax.add_patch(Rectangle((-1.8,-1.15), 3.6, 2.3, fill=False, ec=MUTED, lw=0.9))
ax.add_patch(Circle((-0.75,0), 0.62, fc=ACCENT, alpha=0.24, ec=INK, lw=1.2))
ax.add_patch(Circle((0.75,0), 0.62, fc=SERIES[2], alpha=0.24, ec=INK, lw=1.2))
ax.text(-0.75,-0.03,'A', fontsize=9.5, color=INK, ha='center', style='italic')
ax.text(0.75,-0.03,'B', fontsize=9.5, color=INK, ha='center', style='italic')
ax.set_title('$A \\cap B = \\emptyset$', fontsize=9.8, pad=3)
for ax in axes:
    ax.text(-1.70, 0.90, 'U', fontsize=8.6, color=MUTED, style='italic')
    ax.set_xlim(-1.86,1.86); ax.set_ylim(-1.21,1.21)
    ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout()
```

::: key Laws of set operations
For any subsets $A, B, C$ of a universal set $U$:

| Law | Union form | Intersection form |
|---|---|---|
| Idempotent | $A \cup A = A$ | $A \cap A = A$ |
| Identity | $A \cup \emptyset = A$ | $A \cap U = A$ |
| Domination | $A \cup U = U$ | $A \cap \emptyset = \emptyset$ |
| Commutative | $A \cup B = B \cup A$ | $A \cap B = B \cap A$ |
| Associative | $(A \cup B) \cup C = A \cup (B \cup C)$ | $(A \cap B) \cap C = A \cap (B \cap C)$ |
| Distributive | $A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$ | $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$ |
| De Morgan | $(A \cup B)^c = A^c \cap B^c$ | $(A \cap B)^c = A^c \cup B^c$ |
| Complement | $A \cup A^c = U$ | $A \cap A^c = \emptyset$ |

Also $(A^c)^c = A$, $A - B = A \cap B^c$, and $A \subseteq B \Leftrightarrow A \cup B = B \Leftrightarrow A \cap B = A$.
:::

### Proving a set identity

There are two accepted methods, and NEB awards marks for either.

1. **Element-chasing.** Show $x \in \text{LHS} \Rightarrow x \in \text{RHS}$, then the
   reverse. Two inclusions give equality.
2. **Venn diagram.** Shade both sides and show the shaded regions coincide.

Method 1 is a proof; method 2 is a verification, so use method 1 when the question says
"prove" and method 2 when it says "verify" or "illustrate".

::: derivation Distributive law: $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$
**Step 1 — LHS $\subseteq$ RHS.** Let $x \in A \cap (B \cup C)$.
Then $x \in A$ and $x \in B \cup C$, i.e. $x \in A$, and ($x \in B$ or $x \in C$).

- If $x \in B$: then $x \in A$ and $x \in B$, so $x \in A \cap B$.
- If $x \in C$: then $x \in A$ and $x \in C$, so $x \in A \cap C$.

In either case $x \in (A \cap B) \cup (A \cap C)$. Hence
$A \cap (B \cup C) \subseteq (A \cap B) \cup (A \cap C)$.

**Step 2 — RHS $\subseteq$ LHS.** Let $x \in (A \cap B) \cup (A \cap C)$.
Then $x \in A \cap B$ or $x \in A \cap C$. Either way $x \in A$; and either $x \in B$ or
$x \in C$, so $x \in B \cup C$. Hence $x \in A \cap (B \cup C)$, giving
$(A \cap B) \cup (A \cap C) \subseteq A \cap (B \cup C)$.

**Step 3.** Both inclusions hold, therefore the two sets are equal. $\blacksquare$
:::

```figure caption="Verification of $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$: the shaded regions in the two panels are identical."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, axes = plt.subplots(1, 2, figsize=(5.0,2.8))
cA, cB, cC, r = (0.0, 0.46), (-0.44, -0.34), (0.44, -0.34), 0.78
xs = np.linspace(-1.75, 1.75, 520); ys = np.linspace(-1.45, 1.55, 470)
X, Y = np.meshgrid(xs, ys)
def ins(c): return (X-c[0])**2 + (Y-c[1])**2 <= r*r
A, B, C = ins(cA), ins(cB), ins(cC)
specs = [('$A \\cap (B \\cup C)$', A & (B | C)),
         ('$(A \\cap B) \\cup (A \\cap C)$', (A & B) | (A & C))]
for ax, (t, M) in zip(axes, specs):
    ax.add_patch(Rectangle((-1.72,-1.42), 3.44, 2.94, fill=False, ec=MUTED, lw=0.9))
    ax.contourf(X, Y, M.astype(float), levels=[0.5,1.5], colors=[ACCENT], alpha=0.34)
    for c, lab, off in [(cA,'A',(0,1.02)), (cB,'B',(-0.98,-0.86)), (cC,'C',(0.92,-0.86))]:
        ax.add_patch(Circle(c, r, fill=False, ec=INK, lw=1.2))
        ax.text(off[0], off[1], lab, fontsize=9.5, color=INK, style='italic')
    ax.text(-1.62, 1.28, 'U', fontsize=8.6, color=MUTED, style='italic')
    ax.set_title(t, fontsize=9.4, pad=4)
    ax.set_xlim(-1.78,1.78); ax.set_ylim(-1.48,1.58)
    ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout()
```

::: derivation De Morgan's law: $(A \cup B)^c = A^c \cap B^c$
Let $x \in (A \cup B)^c$. Then $x \in U$ and $x \notin A \cup B$. If $x$ belonged to $A$
it would belong to $A \cup B$, so $x \notin A$; likewise $x \notin B$. Hence $x \in A^c$
and $x \in B^c$, i.e. $x \in A^c \cap B^c$. So $(A \cup B)^c \subseteq A^c \cap B^c$.

Conversely let $x \in A^c \cap B^c$. Then $x \notin A$ and $x \notin B$, so $x$ is in
neither set and therefore $x \notin A \cup B$. Since $x \in U$, $x \in (A \cup B)^c$. So
$A^c \cap B^c \subseteq (A \cup B)^c$.

Both inclusions hold, hence $(A \cup B)^c = A^c \cap B^c$. $\blacksquare$

Replacing $A$ by $A^c$ and $B$ by $B^c$ and taking complements gives the second form,
$(A \cap B)^c = A^c \cup B^c$.
:::

```figure caption="De Morgan's law $(A \cup B)^c = A^c \cap B^c$. Left: everything outside $A \cup B$. Right: the overlap of the two outsides — the same region."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, axes = plt.subplots(1, 2, figsize=(5.0,2.4))
cA, cB, r = (-0.42, 0.0), (0.42, 0.0), 0.84
xs = np.linspace(-2.0, 2.0, 520); ys = np.linspace(-1.25, 1.25, 340)
X, Y = np.meshgrid(xs, ys)
A = (X-cA[0])**2 + (Y-cA[1])**2 <= r*r
B = (X-cB[0])**2 + (Y-cB[1])**2 <= r*r
for ax, (t, M) in zip(axes, [('$(A \\cup B)^c$', ~(A | B)),
                             ('$A^c \\cap B^c$', (~A) & (~B))]):
    ax.add_patch(Rectangle((-2.0,-1.25), 4.0, 2.5, fill=False, ec=MUTED, lw=0.9))
    ax.contourf(X, Y, M.astype(float), levels=[0.5,1.5], colors=[SERIES[1]], alpha=0.28)
    ax.add_patch(Circle(cA, r, fill=False, ec=INK, lw=1.2))
    ax.add_patch(Circle(cB, r, fill=False, ec=INK, lw=1.2))
    ax.text(-0.95, 0.98, 'A', fontsize=9.8, color=INK, style='italic', ha='center')
    ax.text(0.95, 0.98, 'B', fontsize=9.8, color=INK, style='italic', ha='center')
    ax.text(-1.90, 1.00, 'U', fontsize=8.6, color=MUTED, style='italic')
    ax.set_title(t, fontsize=9.8, pad=3)
    ax.set_xlim(-2.06,2.06); ax.set_ylim(-1.31,1.31)
    ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout()
```

::: example Worked example 1.6
**Problem.** If $A = \{a, b, c\}$, write down $P(A)$ and verify $n(P(A)) = 2^{n(A)}$.

**Solution.** List subsets by size:

- size $0$: $\emptyset$
- size $1$: $\{a\}, \{b\}, \{c\}$
- size $2$: $\{a,b\}, \{a,c\}, \{b,c\}$
- size $3$: $\{a,b,c\}$

$$ P(A) = \{\emptyset, \{a\}, \{b\}, \{c\}, \{a,b\}, \{a,c\}, \{b,c\}, \{a,b,c\}\} $$

So $n(P(A)) = 1+3+3+1 = 8$ and $2^{n(A)} = 2^3 = 8$. They agree. (The count is $2^n$
because each of the $n$ elements is independently either in or out of a subset.)
:::

::: example Worked example 1.7
**Problem.** Let $A = \{1,2,3,4,5\}$, $B = \{2,4,6,8\}$ and $C = \{3,4,5,6\}$. Verify
$A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$.

**Solution.** **Left side.** $B \cup C = \{2,3,4,5,6,8\}$, so

$$ A \cap (B \cup C) = \{1,2,3,4,5\} \cap \{2,3,4,5,6,8\} = \{2,3,4,5\} $$

**Right side.** $A \cap B = \{2,4\}$ and $A \cap C = \{3,4,5\}$, so

$$ (A \cap B) \cup (A \cap C) = \{2,4\} \cup \{3,4,5\} = \{2,3,4,5\} $$

The two sides are equal, which verifies the law for these sets.
:::

::: example Worked example 1.8
**Problem.** Let $U = \{1,2,\dots,10\}$, $A = \{1,2,3,4,5\}$ and $B = \{4,5,6,7\}$.
Verify both De Morgan laws.

**Solution.** First the complements: $A^c = \{6,7,8,9,10\}$ and $B^c = \{1,2,3,8,9,10\}$.

**First law.** $A \cup B = \{1,2,3,4,5,6,7\}$, so $(A \cup B)^c = \{8,9,10\}$. And
$A^c \cap B^c = \{6,7,8,9,10\} \cap \{1,2,3,8,9,10\} = \{8,9,10\}$. Equal.

**Second law.** $A \cap B = \{4,5\}$, so $(A \cap B)^c = \{1,2,3,6,7,8,9,10\}$. And
$A^c \cup B^c = \{6,7,8,9,10\} \cup \{1,2,3,8,9,10\} = \{1,2,3,6,7,8,9,10\}$. Equal.
:::

### Cardinality of a union

::: derivation The two-set and three-set counting formulas
Adding $n(A)$ and $n(B)$ counts every element of $A \cap B$ **twice** — once in each set.
Subtracting the overlap once restores the correct count:

$$ n(A \cup B) = n(A) + n(B) - n(A \cap B) $$

For three sets, $n(A)+n(B)+n(C)$ double-counts each pairwise overlap and triple-counts
$A \cap B \cap C$. Subtracting the three pairwise overlaps removes the double counting but
also removes the triple overlap three times, having added it three times — so it must be
added back once:

$$ n(A \cup B \cup C) = n(A)+n(B)+n(C)-n(A \cap B)-n(B \cap C)-n(C \cap A)+n(A \cap B \cap C) $$

For elements outside every set, $n\!\left((A \cup B)^c\right) = n(U) - n(A \cup B)$.
:::

```figure caption="The eight regions of a three-set Venn diagram, filled with the numbers from Worked example 1.10. $K$ = Kantipur, $G$ = Gorkhapatra, $H$ = The Himalayan Times. The central region always holds $n(K \\cap G \\cap H)$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, ax = plt.subplots(figsize=(4.4,3.3))
cK, cG, cH, r = (0.0, 0.50), (-0.48, -0.36), (0.48, -0.36), 0.86
ax.add_patch(Rectangle((-1.85,-1.55), 3.70, 3.25, fill=False, ec=MUTED, lw=0.9))
for c, col in [(cK, ACCENT), (cG, SERIES[2]), (cH, SERIES[1])]:
    ax.add_patch(Circle(c, r, fc=col, alpha=0.11, ec=INK, lw=1.2))
nums = [(0.0, 0.95, '28'), (-0.88, -0.74, '18'), (0.88, -0.74, '10'),
        (-0.40, 0.28, '12'), (0.40, 0.28, '17'), (0.0, -0.62, '7'),
        (0.0, 0.03, '8')]
for X, Y, s in nums:
    ax.text(X, Y, s, fontsize=10.5, color=INK, ha='center', va='center', weight='bold')
ax.text(0.0, 1.52, 'K', fontsize=10.5, color=INK, ha='center', style='italic')
ax.text(-1.48, -0.98, 'G', fontsize=10.5, color=INK, ha='center', style='italic')
ax.text(1.48, -0.98, 'H', fontsize=10.5, color=INK, ha='center', style='italic')
ax.text(1.52, 1.38, '20', fontsize=10.5, color=INK, ha='center', va='center', weight='bold')
ax.text(-1.80, 1.64, 'U = 120', fontsize=8.6, color=MUTED, ha='left', va='top')
ax.set_xlim(-1.92,1.92); ax.set_ylim(-1.62,1.78)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 1.9
**Problem.** In a group of $60$ students of a school in Butwal, $35$ like mathematics,
$28$ like physics and $10$ like neither subject. How many like (a) both subjects,
(b) exactly one subject, (c) mathematics only?

**Solution.** Let $M$ and $P$ be the sets of students who like mathematics and physics.
Given $n(U) = 60$, $n(M) = 35$, $n(P) = 28$, $n\!\left((M \cup P)^c\right) = 10$.

**(a)** Those who like at least one subject are
$n(M \cup P) = 60 - 10 = 50$. From the two-set formula,

$$ n(M \cap P) = n(M) + n(P) - n(M \cup P) = 35 + 28 - 50 = 13 $$

**(b)** Exactly one $= n(M \cup P) - n(M \cap P) = 50 - 13 = 37$.

**(c)** $n(M - P) = n(M) - n(M \cap P) = 35 - 13 = 22$.

*Check:* $22 + 13 + (28-13) + 10 = 22+13+15+10 = 60$. Correct.
:::

::: example Worked example 1.10
**Problem.** Of $120$ readers surveyed in Pokhara, $65$ read *Kantipur*, $45$ read
*Gorkhapatra*, $42$ read *The Himalayan Times*, $20$ read both *Kantipur* and
*Gorkhapatra*, $25$ read *Kantipur* and *The Himalayan Times*, $15$ read *Gorkhapatra*
and *The Himalayan Times*, and $8$ read all three. Find how many read (a) at least one
paper, (b) no paper, (c) exactly one paper, (d) exactly two papers.

**Solution.** Write $K, G, H$ for the three sets.

**(a)** By the three-set formula,

$$ n(K \cup G \cup H) = 65+45+42-20-25-15+8 = 152 - 60 + 8 = 100 $$

**(b)** None $= n(U) - n(K \cup G \cup H) = 120 - 100 = 20$.

**(c)** Work outwards from the centre. *Kantipur* only is $K$ minus the two overlaps, with
the centre added back because it was removed twice:

$$ 65 - 20 - 25 + 8 = 28 $$
$$ \text{Gorkhapatra only} = 45 - 20 - 15 + 8 = 18 $$
$$ \text{Himalayan only} = 42 - 25 - 15 + 8 = 10 $$

Exactly one $= 28 + 18 + 10 = 56$.

**(d)** Exactly two $= (20-8)+(25-8)+(15-8) = 12+17+7 = 36$.

*Check:* $56 + 36 + 8 = 100 = n(K \cup G \cup H)$, and $100 + 20 = 120$. Correct.
:::

::: caution "Both" already includes "all three"
In survey questions the phrase "$20$ read both $K$ and $G$" means $n(K \cap G) = 20$ —
the $8$ who read all three are **inside** that $20$. Only when a question says "exactly
two" or "only $K$ and $G$" do you subtract the centre. Reading this wrongly is the single
biggest source of lost marks in this unit.
:::

::: example Worked example 1.11
**Problem.** Prove that $A - (B \cup C) = (A - B) \cap (A - C)$.

**Solution.** Convert differences to intersections with complements and use De Morgan:

$$ A - (B \cup C) = A \cap (B \cup C)^c = A \cap (B^c \cap C^c) $$

Since $A \cap A = A$, we may write $A \cap B^c \cap C^c = (A \cap B^c) \cap (A \cap C^c)$,
which is $(A - B) \cap (A - C)$. Each step is an equality, so the result follows.

**Justification of the middle step.** $x \in A \cap B^c \cap C^c$ means $x \in A$,
$x \notin B$, $x \notin C$. That is exactly the condition "$x \in A$ and $x \notin B$"
**and** "$x \in A$ and $x \notin C$", i.e. $x \in (A-B) \cap (A-C)$. $\blacksquare$
:::

::: example Worked example 1.12
**Problem.** If $n(A) = 18$, $n(B) = 24$ and $n(A \cup B) = 32$, find $n(A \cap B)$,
$n(A - B)$ and $n(A \triangle B)$.

**Solution.** From $n(A \cup B) = n(A)+n(B)-n(A \cap B)$,

$$ n(A \cap B) = 18 + 24 - 32 = 10 $$

Then $n(A-B) = n(A) - n(A \cap B) = 18 - 10 = 8$ and
$n(B-A) = 24 - 10 = 14$, so

$$ n(A \triangle B) = n(A-B) + n(B-A) = 8 + 14 = 22 $$

Equivalently $n(A \triangle B) = n(A \cup B) - n(A \cap B) = 32 - 10 = 22$.
:::

## Chapter summary

- A **statement** has exactly one truth value, T or F. Open sentences are not statements.
- $p \wedge q$ is true only when both are true; $p \vee q$ is false only when both are
  false; $p \rightarrow q$ is false only when $p$ is T and $q$ is F.
- $p \rightarrow q \equiv \sim p \vee q \equiv \sim q \rightarrow \sim p$. The converse
  $q \rightarrow p$ is equivalent to the inverse, **not** to the original.
- A truth table on $n$ letters has $2^n$ rows. All T = tautology, all F = contradiction,
  identical final columns = logical equivalence.
- De Morgan, in logic and in sets: $\sim(p \vee q) \equiv \sim p \wedge \sim q$ and
  $(A \cup B)^c = A^c \cap B^c$; $(A \cap B)^c = A^c \cup B^c$.
- $A - B = A \cap B^c$; $n(P(A)) = 2^{n(A)}$; $A = B$ is proved by the two inclusions
  $A \subseteq B$ and $B \subseteq A$.
- $n(A \cup B) = n(A)+n(B)-n(A \cap B)$ and
  $n(A \cup B \cup C) = \sum n(A) - \sum n(A \cap B) + n(A \cap B \cap C)$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is a statement? <span class="marks">[1]</span>
   (a) Shut the window. (b) $x - 1 = 0$ (c) $7$ is an even number. (d) How old are you?
2. The statement $p \rightarrow q$ is false only when <span class="marks">[1]</span>
   (a) $p$ is F, $q$ is T (b) $p$ is T, $q$ is F (c) both are T (d) both are F
3. $p \rightarrow q$ is logically equivalent to <span class="marks">[1]</span>
   (a) $q \rightarrow p$ (b) $\sim p \rightarrow \sim q$ (c) $\sim q \rightarrow \sim p$ (d) $p \wedge \sim q$
4. If $n(A) = 5$, the number of subsets of $A$ is <span class="marks">[1]</span>
   (a) $10$ (b) $25$ (c) $32$ (d) $31$
5. $(A \cap B)^c$ equals <span class="marks">[1]</span>
   (a) $A^c \cap B^c$ (b) $A^c \cup B^c$ (c) $A \cup B$ (d) $(A \cup B)^c$
6. If $n(A) = 12$, $n(B) = 9$ and $n(A \cap B) = 4$, then $n(A \cup B)$ is <span class="marks">[1]</span>
   (a) $25$ (b) $21$ (c) $17$ (d) $13$
7. $A - B$ is the same as <span class="marks">[1]</span>
   (a) $A \cap B^c$ (b) $A^c \cap B$ (c) $A \cup B^c$ (d) $B - A$

::: note Answers to Group A
**1.** (c) — it is a declarative sentence with a definite truth value (false). (a) is a command, (d) a question, (b) an open sentence.

**2.** (b) — a conditional fails only when a true antecedent leads to a false consequent.

**3.** (c) — a conditional is equivalent to its contrapositive; the converse (a) and inverse (b) are not.

**4.** (c) — $n(P(A)) = 2^{5} = 32$.

**5.** (b) — De Morgan's second law: complement turns $\cap$ into $\cup$.

**6.** (c) — $12 + 9 - 4 = 17$.

**7.** (a) — "in $A$ and not in $B$" is $A \cap B^c$.
:::

**Group B — Short answer (5 marks each)**

1. Define a statement and a tautology. Construct the truth table of
   $(p \wedge \sim q) \vee q$ and state whether it is a tautology, a contradiction or
   neither. <span class="marks">[5]</span>
2. Write the converse, inverse and contrapositive of "If $x$ is divisible by $10$, then
   $x$ is divisible by $5$", and state the truth value of each with a reason. <span class="marks">[5]</span>
3. Using a truth table, prove that $\sim(p \wedge q) \equiv \sim p \vee \sim q$. <span class="marks">[5]</span>
4. Prove that $(A \cap B)^c = A^c \cup B^c$ by the element-chasing method. <span class="marks">[5]</span>
5. In a class of $80$ students, $45$ play football, $30$ play volleyball and $12$ play
   both. How many play (a) at least one game, (b) neither game, (c) exactly one game? <span class="marks">[5]</span>
6. If $A = \{x : x \in \mathbb{N} , x \le 8\}$, $B = \{2,4,6,8,10\}$ and
   $C = \{1,3,5,7,9\}$ with $U = \{1,2,\dots,10\}$, find
   $(A \cup B)^c$, $A - (B \cup C)$ and $n(A \triangle B)$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** A *statement* is a declarative sentence with exactly one truth value, T or F. A
*tautology* is a compound statement that is true for every assignment of truth values.

| $p$ | $q$ | $\sim q$ | $p \wedge \sim q$ | $(p \wedge \sim q) \vee q$ |
|---|---|---|---|---|
| T | T | F | F | T |
| T | F | T | T | T |
| F | T | F | F | T |
| F | F | T | F | F |

The last column is T, T, T, F — not all T and not all F, so it is **neither** a tautology
nor a contradiction (it is a contingency). In fact it is equivalent to $p \vee q$.

**2.** Let $p$: $x$ is divisible by $10$; $q$: $x$ is divisible by $5$. The original
$p \rightarrow q$ is **true**, since $x = 10k = 5(2k)$.

- Converse $q \rightarrow p$: "If $x$ is divisible by $5$ then $x$ is divisible by $10$."
  **False** — $x = 15$ is divisible by $5$ but not by $10$.
- Inverse $\sim p \rightarrow \sim q$: "If $x$ is not divisible by $10$ then $x$ is not
  divisible by $5$." **False** — same counter-example $x = 15$.
- Contrapositive $\sim q \rightarrow \sim p$: "If $x$ is not divisible by $5$ then $x$ is
  not divisible by $10$." **True**, being equivalent to the original.

**3.**

| $p$ | $q$ | $p \wedge q$ | $\sim(p \wedge q)$ | $\sim p$ | $\sim q$ | $\sim p \vee \sim q$ |
|---|---|---|---|---|---|---|
| T | T | T | F | F | F | F |
| T | F | F | T | F | T | T |
| F | T | F | T | T | F | T |
| F | F | F | T | T | T | T |

Column 4 and column 7 are both F, T, T, T. Identical columns, so the statements are
logically equivalent.

**4.** Let $x \in (A \cap B)^c$. Then $x \in U$ and $x \notin A \cap B$, so $x$ fails to
be in at least one of $A, B$ — that is, $x \notin A$ or $x \notin B$, i.e. $x \in A^c$ or
$x \in B^c$, i.e. $x \in A^c \cup B^c$. Hence $(A \cap B)^c \subseteq A^c \cup B^c$.

Conversely let $x \in A^c \cup B^c$. Then $x \notin A$ or $x \notin B$. In either case $x$
cannot be in both $A$ and $B$, so $x \notin A \cap B$, and since $x \in U$ we get
$x \in (A \cap B)^c$. Hence $A^c \cup B^c \subseteq (A \cap B)^c$.

Both inclusions hold, so $(A \cap B)^c = A^c \cup B^c$.

**5.** $n(U) = 80$, $n(F) = 45$, $n(V) = 30$, $n(F \cap V) = 12$.

(a) $n(F \cup V) = 45 + 30 - 12 = 63$.

(b) Neither $= 80 - 63 = 17$.

(c) Exactly one $= 63 - 12 = 51$ (football only $45-12 = 33$, volleyball only
$30-12 = 18$, and $33+18 = 51$).

**6.** $A = \{1,2,3,4,5,6,7,8\}$.

$A \cup B = \{1,2,3,4,5,6,7,8,10\}$, so $(A \cup B)^c = \{9\}$.

$B \cup C = \{1,2,3,4,5,6,7,8,9,10\} = U$, so $A - (B \cup C) = \emptyset$.

$A \cap B = \{2,4,6,8\}$, so $A - B = \{1,3,5,7\}$ and $B - A = \{10\}$. Hence
$A \triangle B = \{1,3,5,7,10\}$ and $n(A \triangle B) = 5$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Construct the truth table of $p \vee (q \wedge r)$ and of
   $(p \vee q) \wedge (p \vee r)$, and hence state the law verified. <span class="marks">[5]</span>
   (b) Show with a truth table that $(p \rightarrow q) \wedge (q \rightarrow r) \rightarrow (p \rightarrow r)$
   is a tautology. <span class="marks">[3]</span>
2. In a survey of $200$ households in Biratnagar, $120$ own a television, $90$ own a
   refrigerator, $70$ own a motorcycle, $50$ own a television and a refrigerator, $40$
   own a television and a motorcycle, $30$ own a refrigerator and a motorcycle, and $20$
   own all three. <span class="marks">[8]</span>
   Using a Venn diagram find how many households own (a) at least one of the three,
   (b) none of the three, (c) exactly one item, (d) exactly two items.

::: note Answers to Group C
**1. (a)** See Worked example 1.4 for the full eight-row table. Both final columns read
T, T, T, T, T, F, F, F, so
$p \vee (q \wedge r) \equiv (p \vee q) \wedge (p \vee r)$ — the **distributive law of
disjunction over conjunction**.

**1. (b)** Write $S = (p \rightarrow q) \wedge (q \rightarrow r)$ and
$T = p \rightarrow r$.

| $p$ | $q$ | $r$ | $p \rightarrow q$ | $q \rightarrow r$ | $S$ | $T$ | $S \rightarrow T$ |
|---|---|---|---|---|---|---|---|
| T | T | T | T | T | T | T | T |
| T | T | F | T | F | F | F | T |
| T | F | T | F | T | F | T | T |
| T | F | F | F | T | F | F | T |
| F | T | T | T | T | T | T | T |
| F | T | F | T | F | F | T | T |
| F | F | T | T | T | T | T | T |
| F | F | F | T | T | T | T | T |

The last column is T in all eight rows, so the statement is a tautology. (This is the
**law of syllogism**, the rule that lets you chain implications in a proof.)

**2.** Let $T, R, M$ be the sets of television, refrigerator and motorcycle owners.
Given $n(U) = 200$, $n(T) = 120$, $n(R) = 90$, $n(M) = 70$, $n(T \cap R) = 50$,
$n(T \cap M) = 40$, $n(R \cap M) = 30$, $n(T \cap R \cap M) = 20$.

(a) $n(T \cup R \cup M) = 120+90+70-50-40-30+20 = 280 - 120 + 20 = 180$.

(b) None $= 200 - 180 = 20$.

(c) Filling the Venn diagram from the centre outwards:

$$ \text{T only} = 120-50-40+20 = 50 $$
$$ \text{R only} = 90-50-30+20 = 30 $$
$$ \text{M only} = 70-40-30+20 = 20 $$

Exactly one $= 50+30+20 = 100$.

(d) Exactly two $= (50-20)+(40-20)+(30-20) = 30+20+10 = 60$.

*Check:* $100 + 60 + 20 = 180$, and $180 + 20 = 200$. Consistent.
:::
