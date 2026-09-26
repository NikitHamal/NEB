---
subject: Mathematics
grade: 12
unit: 17
title: "Appendix: Retained Examinable Topics"
hours: 0
area: Computational Methods OR Mechanics
---

**This chapter is an appendix, not a timetabled unit.** The CDC curriculum of
2078 BS allots it $0$ teaching hours, because the topics in it were dropped from
the 2078 syllabus grid. They had been part of the 2076 curriculum, and NEB
question papers have continued to set questions on them — so a candidate who has
never met them can lose marks on the day. Everything here is examinable in
practice even though it carries no teaching hours: work through it after you have
finished your main units, and treat it as revision plus a small amount of new
material.

::: key What is in this appendix and why
- **Elementary group theory** — binary operations, the group axioms, abelian
  groups, finite and infinite groups. Usually a Group B question asking you to
  build a Cayley table and verify the four axioms.
- **Rolle's theorem and the Mean Value Theorem** — the two "verify the theorem
  for $f$ on $[a, b]$ and find $c$" questions. Short, standard, and free marks
  once you know the method.
- **Numerical integration** — the trapezoidal and Simpson's rules, revised here
  as the ordinate table you actually write in the exam, with the error bounds.
:::

## 17.1 Elementary Group Theory: binary operation, group, abelian group, finite and infinite groups

### Binary operations

::: definition Binary operation
A **binary operation** $*$ on a non-empty set $G$ is a rule that assigns to every
**ordered pair** $(a, b)$ of elements of $G$ exactly one element $a * b$
**of $G$**.

The requirement that $a * b$ lies back in $G$ is called **closure**: a binary
operation is by definition a map $G \times G \rightarrow G$.
:::

Ordinary addition is a binary operation on $\mathbb{N}$, but subtraction is not:
$3 - 5 = -2 \notin \mathbb{N}$. Division is a binary operation on
$\mathbb{R} \setminus \{0\}$ but not on $\mathbb{R}$, because $a \div 0$ is
undefined.

::: example Worked example 17.1
**Problem.** State, with a reason, whether each is a binary operation on the set
shown.
(a) $a * b = a + b$ on $\mathbb{N}$  (b) $a * b = a - b$ on $\mathbb{N}$
(c) $a * b = ab$ on $\mathbb{Z}$  (d) $a * b = \dfrac{a}{b}$ on $\mathbb{Z}$

**Solution.**
(a) **Yes.** The sum of two natural numbers is a natural number, so $*$ is closed.

(b) **No.** Take $a = 3$, $b = 5$: $3 - 5 = -2$, which is not in $\mathbb{N}$.
A single counter-example is enough to destroy closure.

(c) **Yes.** The product of two integers is an integer.

(d) **No.** $1 \div 2 = 0.5 \notin \mathbb{Z}$ (and division by $0$ is not
defined either).
:::

### The group axioms

::: key Definition of a group
A non-empty set $G$ with a binary operation $*$ is a **group** $(G, *)$ if:

1. **Closure.** $a * b \in G$ for all $a, b \in G$.
2. **Associativity.** $(a * b) * c = a * (b * c)$ for all $a, b, c \in G$.
3. **Identity.** There is $e \in G$ with $e * a = a * e = a$ for all $a \in G$.
4. **Inverse.** For each $a \in G$ there is $a^{-1} \in G$ with
   $a * a^{-1} = a^{-1} * a = e$.

If in addition $a * b = b * a$ for all $a, b \in G$, the group is **abelian**
(commutative).

A group with finitely many elements is a **finite group**, and the number of
elements is its **order**, written $o(G)$ or $|G|$; otherwise it is an **infinite
group**.
:::

::: definition Cayley table
For a finite group, the **Cayley table** (composition table) lists $a * b$ with
$a$ from the left-hand column and $b$ from the top row. Reading it:

- **closure** — every entry lies in the set;
- **identity** — some row is a copy of the heading row (and the matching column a
  copy of the heading column);
- **inverses** — the identity appears exactly once in every row and column;
- **abelian** — the table is symmetric about the leading diagonal.

Associativity cannot be read off quickly; quote it from the known associativity of
addition, multiplication or composition.
:::

```figure caption="Cayley table of $Z_4 = \{0, 1, 2, 3\}$ under addition modulo $4$. Every entry is in the set (closure), the row for $0$ repeats the heading (identity), the shaded $0$s show each element has an inverse, and the table is symmetric about the leading diagonal, so the group is abelian."
import numpy as np
fig, ax = plt.subplots(figsize=(4.2,3.0))
els = [0, 1, 2, 3]
n = len(els)
tab = [[(a+b) % 4 for b in els] for a in els]
cw, ch = 1.0, 0.72
def cell(i, j, txt, fc='white', bold=False, col=INK, fs=11):
    x, y = j*cw, -i*ch
    ax.add_patch(plt.Rectangle((x, y-ch), cw, ch, facecolor=fc,
                               edgecolor=GRID, lw=1.0))
    ax.text(x+cw/2, y-ch/2, txt, ha='center', va='center', fontsize=fs,
            color=col, fontweight='bold' if bold else 'normal')
cell(0, 0, r'$+_4$', fc='#eef1f5', bold=True, col=ACCENT)
for j, b in enumerate(els):
    cell(0, j+1, f'${b}$', fc='#eef1f5', bold=True, col=ACCENT)
for i, a in enumerate(els):
    cell(i+1, 0, f'${a}$', fc='#eef1f5', bold=True, col=ACCENT)
    for j, b in enumerate(els):
        v = tab[i][j]
        cell(i+1, j+1, f'${v}$', fc='#e4efe6' if v == 0 else 'white',
             col='#2e8b57' if v == 0 else INK)
ax.plot([cw, (n+1)*cw], [-ch, -(n+1)*ch], color='#d9534f', lw=1.1, ls=(0,(4,3)), alpha=0.5)
ax.text((n+1)*cw+0.18, -1.5*ch, 'identity row', fontsize=8.6, color=MUTED, va='center')
ax.annotate('', xy=((n+1)*cw+0.04, -1.5*ch), xytext=((n+1)*cw+0.16, -1.5*ch),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=8))
ax.text((n+1)*cw+0.18, -(n+1)*ch+0.12, 'leading diagonal', fontsize=8.6,
        color='#d9534f', va='center')
ax.set_xlim(-0.15, (n+1)*cw+1.95); ax.set_ylim(-(n+1)*ch-0.35, 0.25)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 17.2
**Problem.** Show that $Z_4 = \{0, 1, 2, 3\}$ is an abelian group under addition
modulo $4$, and state its order.

**Solution.** The Cayley table above is the working. Take the four axioms in turn.

**Closure.** Every entry of the table is $0$, $1$, $2$ or $3$, so $Z_4$ is closed
under $+_4$.

**Associativity.** Addition of integers is associative, and reducing modulo $4$
does not change this: $(a +_4 b) +_4 c$ and $a +_4 (b +_4 c)$ are both the
remainder of $a+b+c$ on division by $4$.

**Identity.** The row headed $0$ reads $0, 1, 2, 3$ — the heading row — and the
column headed $0$ likewise. So $e = 0$.

**Inverse.** The entry $0$ occurs once in each row: $0 +_4 0 = 0$,
$1 +_4 3 = 0$, $2 +_4 2 = 0$, $3 +_4 1 = 0$. Hence
$0^{-1} = 0$, $1^{-1} = 3$, $2^{-1} = 2$, $3^{-1} = 1$.

So $(Z_4, +_4)$ is a group. The table is symmetric about the leading diagonal, so
it is **abelian**, and it is **finite of order 4**.
:::

```figure caption="Left: Cayley table of $G = \{1, -1, i, -i\}$ under multiplication; the shaded $1$s locate the inverses. Right: the same four elements on the Argand diagram — multiplying by $i$ is a quarter-turn anticlockwise, so the group is generated by $i$."
import numpy as np
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.8),
                         gridspec_kw={'width_ratios': [1.25, 1.0]})
ax = axes[0]
els = [1, -1, 1j, -1j]
lab = ['$1$', '$-1$', '$i$', '$-i$']
n = 4
cw, ch = 1.0, 0.74
def cell(i, j, txt, fc='white', bold=False, col=INK):
    x, y = j*cw, -i*ch
    ax.add_patch(plt.Rectangle((x, y-ch), cw, ch, facecolor=fc,
                               edgecolor=GRID, lw=1.0))
    ax.text(x+cw/2, y-ch/2, txt, ha='center', va='center', fontsize=10.5,
            color=col, fontweight='bold' if bold else 'normal')
cell(0, 0, r'$\times$', fc='#eef1f5', bold=True, col=ACCENT)
for j in range(n):
    cell(0, j+1, lab[j], fc='#eef1f5', bold=True, col=ACCENT)
for i in range(n):
    cell(i+1, 0, lab[i], fc='#eef1f5', bold=True, col=ACCENT)
    for j in range(n):
        v = els[i]*els[j]
        k = min(range(n), key=lambda t: abs(els[t]-v))
        cell(i+1, j+1, lab[k], fc='#e4efe6' if k == 0 else 'white',
             col='#2e8b57' if k == 0 else INK)
ax.set_xlim(-0.15, (n+1)*cw+0.15); ax.set_ylim(-(n+1)*ch-0.15, 0.15)
ax.set_aspect('equal'); ax.axis('off')
ax = axes[1]
ax.axhline(0, color=INK, lw=1.0); ax.axvline(0, color=INK, lw=1.0)
th = np.linspace(0, 2*np.pi, 300)
ax.plot(np.cos(th), np.sin(th), color=GRID, lw=1.2)
pts = [(1, 0, '$1$', (0.10, 0.12)), (-1, 0, '$-1$', (-0.42, 0.12)),
       (0, 1, '$i$', (0.10, 0.10)), (0, -1, '$-i$', (0.10, -0.34))]
for x, y, t, off in pts:
    ax.plot([x], [y], 'o', color=ACCENT, ms=6)
    ax.text(x+off[0], y+off[1], t, fontsize=10.5, color=ACCENT)
for a0 in [0, 90, 180, 270]:
    t = np.radians(np.linspace(a0+12, a0+78, 40))
    ax.plot(1.28*np.cos(t), 1.28*np.sin(t), color='#d9534f', lw=1.1)
    te = np.radians(a0+78)
    ax.annotate('', xy=(1.28*np.cos(te+0.05), 1.28*np.sin(te+0.05)),
                xytext=(1.28*np.cos(te), 1.28*np.sin(te)),
                arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.1,
                                mutation_scale=9))
ax.text(1.30, 1.50, r'multiply by $i$', fontsize=9.0, color='#d9534f', ha='center')
ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.75, 1.95)
ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout()
```

::: example Worked example 17.3
**Problem.** Show that $G = \{1, -1, i, -i\}$ is an abelian group under
multiplication of complex numbers, and find the inverse of each element.

**Solution.** Read the table in the figure.

**Closure.** Every product is again one of $1, -1, i, -i$; for instance
$i \times i = i^2 = -1$ and $i \times (-i) = -i^2 = 1$.

**Associativity.** Multiplication of complex numbers is associative.

**Identity.** $e = 1$, since $1 \times z = z \times 1 = z$ for each element.

**Inverses.** The $1$s in the table give
$1^{-1} = 1$, $(-1)^{-1} = -1$, $i^{-1} = -i$, $(-i)^{-1} = i$.

The table is symmetric about the leading diagonal (equivalently, multiplication of
complex numbers is commutative), so $G$ is an **abelian group of order 4**.
:::

::: example Worked example 17.4
**Problem.** Show that $(\mathbb{Z}, +)$ is an infinite abelian group but
$(\mathbb{N}, +)$ is not a group.

**Solution.** For $(\mathbb{Z}, +)$:

- closure: the sum of two integers is an integer;
- associativity: $(a+b)+c = a+(b+c)$ for integers;
- identity: $e = 0$, because $a + 0 = 0 + a = a$;
- inverse: the inverse of $a$ is $-a \in \mathbb{Z}$, since $a + (-a) = 0$;
- commutativity: $a + b = b + a$.

$\mathbb{Z}$ has infinitely many elements, so $(\mathbb{Z}, +)$ is an **infinite
abelian group**.

For $(\mathbb{N}, +)$ the identity $0$ is not in $\mathbb{N}$ (and even taking
$\mathbb{N}$ to contain $0$, the element $3$ would need the inverse $-3$, which is
not a natural number). **Axiom 4 fails**, so $(\mathbb{N}, +)$ is not a group.
:::

::: example Worked example 17.5
**Problem.** Show that $G = \{1, 2, 3, 4\}$ is a group under multiplication
modulo $5$, and find the inverse of each element.

**Solution.** The composition table (computed entry by entry, e.g.
$2 \times_5 3 = 6 \equiv 1$ modulo $5$) is

| $\times_5$ | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| **1** | 1 | 2 | 3 | 4 |
| **2** | 2 | 4 | 1 | 3 |
| **3** | 3 | 1 | 4 | 2 |
| **4** | 4 | 3 | 2 | 1 |

**Closure.** No entry is $0$ and every entry lies in $G$. (This is why $5$ must be
prime: modulo $6$, $2 \times_6 3 = 0 \notin G$.)

**Associativity.** Inherited from multiplication of integers.

**Identity.** The row and column headed $1$ repeat the headings, so $e = 1$.

**Inverses.** The identity $1$ appears once in each row:

$$ 1^{-1} = 1, \qquad 2^{-1} = 3, \qquad 3^{-1} = 2, \qquad 4^{-1} = 4 $$

The table is symmetric, so $G$ is an abelian group of order $4$.
:::

::: example Worked example 17.6
**Problem.** Prove that in any group $(G, *)$ the identity element is unique and
each element has exactly one inverse.

**Solution.** **Identity.** Suppose $e$ and $e'$ are both identities. Treating
$e$ as the identity, $e * e' = e'$. Treating $e'$ as the identity,
$e * e' = e$. Hence $e = e'$.

**Inverse.** Suppose $b$ and $c$ are both inverses of $a$. Then

$$ b = b * e = b * (a * c) = (b * a) * c = e * c = c $$

using in turn the identity axiom, $a*c = e$, associativity, $b*a = e$, and the
identity axiom again. So $b = c$.
:::

```figure caption="Cayley table of the symmetric group $S_3$ under composition ($e$ identity, $r$ a rotation of order $3$, $a$, $b$, $c$ reflections). The entry $r \circ a = c$ and the entry $a \circ r = b$ are shaded: they differ, so the table is not symmetric about the leading diagonal and $S_3$ is the smallest non-abelian group."
import numpy as np
fig, ax = plt.subplots(figsize=(4.6,3.2))
names = ['e', 'r', 'r^2', 'a', 'b', 'c']
perm = {'e': (1,2,3), 'r': (2,3,1), 'r^2': (3,1,2),
        'a': (1,3,2), 'b': (3,2,1), 'c': (2,1,3)}
inv = {v: k for k, v in perm.items()}
def comp(f, g):
    return tuple(f[g[i]-1] for i in range(3))
n = 6
cw, ch = 0.82, 0.62
def cell(i, j, txt, fc='white', bold=False, col=INK, fs=9.5):
    x, y = j*cw, -i*ch
    ax.add_patch(plt.Rectangle((x, y-ch), cw, ch, facecolor=fc,
                               edgecolor=GRID, lw=0.9))
    ax.text(x+cw/2, y-ch/2, txt, ha='center', va='center', fontsize=fs,
            color=col, fontweight='bold' if bold else 'normal')
cell(0, 0, r'$\circ$', fc='#eef1f5', bold=True, col=ACCENT, fs=11)
for j, b in enumerate(names):
    cell(0, j+1, f'${b}$', fc='#eef1f5', bold=True, col=ACCENT)
for i, a in enumerate(names):
    cell(i+1, 0, f'${a}$', fc='#eef1f5', bold=True, col=ACCENT)
    for j, b in enumerate(names):
        v = inv[comp(perm[a], perm[b])]
        hot = (a, b) in [('r', 'a'), ('a', 'r')]
        cell(i+1, j+1, f'${v}$', fc='#fbe3e2' if hot else 'white',
             col='#d9534f' if hot else INK, bold=hot)
ax.plot([cw, (n+1)*cw], [-ch, -(n+1)*ch], color=MUTED, lw=1.0, ls=(0,(4,3)), alpha=0.5)
ax.text((n+1)*cw+0.15, -1.55*ch, r'$r \circ a = c$', fontsize=9.4, color='#d9534f')
ax.text((n+1)*cw+0.15, -4.55*ch, r'$a \circ r = b$', fontsize=9.4, color='#d9534f')
ax.text((n+1)*cw+0.15, -3.05*ch, 'not equal:', fontsize=9.0, color=MUTED)
ax.text((n+1)*cw+0.15, -3.60*ch, 'non-abelian', fontsize=9.0, color=MUTED)
ax.set_xlim(-0.12, (n+1)*cw+1.85); ax.set_ylim(-(n+1)*ch-0.20, 0.20)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 17.7
**Problem.** Using the table above, show that $S_3$ is a non-abelian group of
order $6$, and find $(r \circ a)^{-1}$.

**Solution.** Every entry is one of the six symbols, so $S_3$ is closed;
composition of functions is always associative; the row and column headed $e$
repeat the headings, so $e$ is the identity; and $e$ appears once in every row and
column, so every element has an inverse. Hence $S_3$ is a group of order $6$.

From the table, $r \circ a = c$ but $a \circ r = b$, and $b \ne c$, so

$$ r \circ a \ne a \circ r $$

and the group is **not abelian**. Finally $(r \circ a)^{-1} = c^{-1}$, and the
row for $c$ contains $e$ in the column headed $c$ (that is, $c \circ c = e$), so
$(r \circ a)^{-1} = c$.
:::

::: caution Closure is an axiom, not an afterthought
Most lost marks in this topic come from writing "clearly closed" for a set where
closure fails. Always check it against the table. And remember that the identity
must work on **both** sides, and must itself belong to the set — this is exactly
why $(\mathbb{N}, +)$ and $\{1, 2, 3, 4, 5\}$ under $\times_6$ are not groups.
:::

## 17.2 Rolle's theorem and Mean Value Theorem

::: key Rolle's theorem
If $f$ is
(i) **continuous** on the closed interval $[a, b]$,
(ii) **differentiable** on the open interval $(a, b)$, and
(iii) $f(a) = f(b)$,

then there exists at least one $c \in (a, b)$ such that

$$ f'(c) = 0 $$

Geometrically: a curve that starts and finishes at the same height, with no break
and no corner, must have at least one point where the tangent is horizontal.
:::

::: key Lagrange's Mean Value Theorem (MVT)
If $f$ is continuous on $[a, b]$ and differentiable on $(a, b)$, then there is at
least one $c \in (a, b)$ with

$$ f'(c) = \frac{f(b) - f(a)}{b - a} $$

Geometrically: somewhere in the interval the tangent is **parallel to the chord**
joining the end points. Rolle's theorem is the special case $f(a) = f(b)$.
:::

::: derivation The MVT from Rolle's theorem
Let $f$ satisfy the conditions of the MVT and put

$$ g(x) = f(x) - f(a) - \frac{f(b)-f(a)}{b-a}\,(x - a) $$

$g$ is continuous on $[a, b]$ and differentiable on $(a, b)$, being the
difference of $f$ and a linear function. Also

$$ g(a) = 0, \qquad
g(b) = f(b) - f(a) - \frac{f(b)-f(a)}{b-a}(b-a) = 0 $$

so $g(a) = g(b)$ and Rolle's theorem applies: there is $c \in (a, b)$ with
$g'(c) = 0$. But

$$ g'(x) = f'(x) - \frac{f(b)-f(a)}{b-a} $$

so $g'(c) = 0$ gives $f'(c) = \dfrac{f(b)-f(a)}{b-a}$, as required.
:::

```figure caption="Rolle's theorem for $f(x) = x^2 - 4x + 3$ on $[1, 3]$. Since $f(1) = f(3) = 0$ the chord is horizontal, and the tangent at $c = 2$ is horizontal too: $f'(2) = 0$."
import numpy as np
fig, ax = plt.subplots(figsize=(4.8,2.9))
f = lambda x: x**2 - 4*x + 3
fp = lambda x: 2*x - 4
x = np.linspace(0.55, 3.45, 400)
ax.plot(x, f(x), color=ACCENT, lw=2.2, zorder=4, label='$f(x) = x^2-4x+3$')
ax.axhline(0, color=INK, lw=1.0)
ax.plot([1, 3], [0, 0], color='#d9534f', lw=2.4, zorder=5)
ax.plot([1, 3], [0, 0], 'o', color='#d9534f', ms=6, zorder=6)
c = 2.0
xt = np.linspace(1.15, 2.85, 50)
ax.plot(xt, f(c) + fp(c)*(xt-c), color='#2e8b57', lw=1.8, ls=(0,(5,3)), zorder=5)
ax.plot([c], [f(c)], 'o', color='#2e8b57', ms=6.5, zorder=7)
ax.plot([c, c], [f(c), 0], color=MUTED, lw=0.9, ls=':')
ax.text(c+0.06, f(c)-0.42, r"$(c,\ f(c)) = (2,\ -1)$", fontsize=9.2, color='#2e8b57')
ax.text(2.00, 0.42, r'chord: $f(1)=f(3)=0$', fontsize=9.2, color='#d9534f', ha='center')
ax.text(c-0.07, -0.20, '$c = 2$', fontsize=9.2, color=MUTED, ha='right')
ax.text(0.58, -0.62, r"tangent $f'(c) = 0$", fontsize=9.2, color='#2e8b57')
ax.set_xlim(0.45, 3.65); ax.set_ylim(-1.7, 1.3)
ax.set_xlabel('$x$'); ax.set_ylabel('$f(x)$')
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.32)
```

::: example Worked example 17.8
**Problem.** Verify Rolle's theorem for $f(x) = x^2 - 4x + 3$ on $[1, 3]$ and find
the value of $c$.

**Solution.** **Check the three conditions.**

(i) $f$ is a polynomial, so it is continuous on $[1, 3]$.
(ii) $f$ is a polynomial, so it is differentiable on $(1, 3)$.
(iii) $f(1) = 1 - 4 + 3 = 0$ and $f(3) = 9 - 12 + 3 = 0$, so $f(1) = f(3)$.

All three hold, so Rolle's theorem guarantees a $c \in (1, 3)$ with $f'(c) = 0$.

**Find $c$.** $f'(x) = 2x - 4$, so

$$ 2c - 4 = 0 \;\Longrightarrow\; c = 2 $$

Since $1 < 2 < 3$, the value $c = 2$ lies in the open interval and the theorem is
verified.
:::

::: example Worked example 17.9
**Problem.** Verify Rolle's theorem for $f(x) = x^3 - 4x$ on $[-2, 2]$.

**Solution.** $f$ is a polynomial, hence continuous on $[-2, 2]$ and
differentiable on $(-2, 2)$.

$$ f(-2) = -8 + 8 = 0, \qquad f(2) = 8 - 8 = 0 $$

so $f(-2) = f(2)$ and Rolle's theorem applies. Now $f'(x) = 3x^2 - 4$, so

$$ 3c^2 - 4 = 0 \;\Longrightarrow\; c^2 = \frac43 \;\Longrightarrow\;
c = \pm\frac{2}{\sqrt{3}} = \pm 1.1547 $$

Both values lie in $(-2, 2)$, so there are **two** such points. (The theorem
promises at least one; it does not say only one.)
:::

::: example Worked example 17.10
**Problem.** Explain why Rolle's theorem does not apply to
(a) $f(x) = |x|$ on $[-1, 1]$, (b) $f(x) = \dfrac{1}{x}$ on $[-1, 1]$.

**Solution.** (a) $f(-1) = f(1) = 1$ and $f$ is continuous, but $f$ is **not
differentiable at $x = 0$** — the graph has a corner there. Condition (ii) fails,
and indeed $f'(x) = \pm 1$ is never zero.

(b) $f$ is **not continuous on $[-1, 1]$**: it is not even defined at $x = 0$.
Condition (i) fails. ($f(-1) = -1$ and $f(1) = 1$ are not equal either.)
:::

```figure caption="Mean Value Theorem for $f(x) = \sqrt{x}$ on $[1, 4]$. The chord from $(1, 1)$ to $(4, 2)$ has gradient $\frac{1}{3}$, and the tangent at $c = \frac94$ has the same gradient, so it is parallel to the chord."
import numpy as np
fig, ax = plt.subplots(figsize=(4.9,2.9))
f = lambda x: np.sqrt(x)
fp = lambda x: 0.5/np.sqrt(x)
x = np.linspace(0.55, 4.6, 400)
ax.plot(x, f(x), color=ACCENT, lw=2.2, zorder=4)
ax.plot([1, 4], [1, 2], color='#d9534f', lw=2.0, zorder=5)
ax.plot([1, 4], [1, 2], 'o', color='#d9534f', ms=6, zorder=6)
c = 2.25
xt = np.linspace(1.15, 3.9, 50)
ax.plot(xt, f(c) + fp(c)*(xt-c), color='#2e8b57', lw=1.9, ls=(0,(5,3)), zorder=5)
ax.plot([c], [f(c)], 'o', color='#2e8b57', ms=6.5, zorder=7)
ax.plot([c, c], [0.55, f(c)], color=MUTED, lw=0.9, ls=':')
ax.text(1.06, 0.83, '$(1, 1)$', fontsize=9.2, color='#d9534f')
ax.text(4.06, 1.96, '$(4, 2)$', fontsize=9.2, color='#d9534f')
ax.text(2.35, 1.14, r'chord, gradient $\frac{1}{3}$', fontsize=9.2,
        color='#d9534f', ha='center')
ax.text(2.02, 2.04, r'tangent at $c = \frac{9}{4}$', fontsize=9.2, color='#2e8b57')
ax.text(c, 0.63, r'$c = 2.25$', fontsize=9.0, color=MUTED, ha='center')
ax.text(3.55, 0.95, r'$y = \sqrt{x}$', fontsize=10, color=ACCENT)
ax.set_xlim(0.45, 4.85); ax.set_ylim(0.55, 2.42)
ax.set_xlabel('$x$'); ax.set_ylabel('$f(x)$')
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.32)
```

::: example Worked example 17.11
**Problem.** Verify the Mean Value Theorem for $f(x) = x^2$ on $[1, 3]$.

**Solution.** $f$ is a polynomial, so it is continuous on $[1, 3]$ and
differentiable on $(1, 3)$; the MVT applies.

$$ \frac{f(3) - f(1)}{3 - 1} = \frac{9 - 1}{2} = 4 $$

$f'(x) = 2x$, so $f'(c) = 4$ gives

$$ 2c = 4 \;\Longrightarrow\; c = 2 \in (1, 3) $$

The tangent at $x = 2$ has gradient $4$, the same as the chord.
:::

::: example Worked example 17.12
**Problem.** Verify the Mean Value Theorem for $f(x) = \sqrt{x}$ on $[1, 4]$.

**Solution.** $f$ is continuous on $[1, 4]$ and differentiable on $(1, 4)$
(the only bad point, $x = 0$, is outside the interval).

$$ \frac{f(4) - f(1)}{4 - 1} = \frac{2 - 1}{3} = \frac13 $$

$f'(x) = \dfrac{1}{2\sqrt{x}}$, so $f'(c) = \dfrac13$ gives

$$ \frac{1}{2\sqrt{c}} = \frac13 \;\Longrightarrow\; 2\sqrt{c} = 3
\;\Longrightarrow\; \sqrt{c} = \frac32 \;\Longrightarrow\; c = \frac94 = 2.25 $$

and $1 < 2.25 < 4$, so the theorem is verified.
:::

::: example Worked example 17.13
**Problem.** Verify the Mean Value Theorem for $f(x) = \ln x$ on $[1, e]$.

**Solution.** $\ln x$ is continuous on $[1, e]$ and differentiable on $(1, e)$.

$$ \frac{f(e) - f(1)}{e - 1} = \frac{1 - 0}{e - 1} = \frac{1}{e-1} $$

$f'(x) = \dfrac1x$, so

$$ \frac1c = \frac{1}{e-1} \;\Longrightarrow\; c = e - 1 = 1.718 $$

Since $1 < 1.718 < 2.718$, the value $c = e-1$ lies in $(1, e)$.
:::

::: tip The method is always the same
Check continuity, check differentiability, check $f(a) = f(b)$ (Rolle only), then
**solve one equation**: $f'(c) = 0$ for Rolle, $f'(c) = \frac{f(b)-f(a)}{b-a}$
for the MVT. Always finish by confirming that your $c$ lies in the **open**
interval $(a, b)$ — that sentence is worth a mark.
:::

## 17.3 Numerical integration: trapezoidal and Simpson's rule (revision)

Divide $[a, b]$ into $n$ equal strips of width $h = \dfrac{b-a}{n}$ and label the
ordinates $y_i = f(a + ih)$ for $i = 0, 1, \ldots, n$.

::: key The two rules and their error bounds
**Trapezoidal rule** (any $n$) — join the ordinates by straight lines:

$$ \int_a^b f(x)\,dx \approx \frac{h}{2}\left[(y_0 + y_n)
+ 2(y_1 + y_2 + \cdots + y_{n-1})\right] $$

$$ |E_T| \leq \frac{(b-a)h^2}{12}\max_{[a,b]}|f''(x)| $$

**Simpson's rule** ($n$ **even**) — join the ordinates in threes by parabolas:

$$ \int_a^b f(x)\,dx \approx \frac{h}{3}\left[(y_0 + y_n)
+ 4(y_1 + y_3 + \cdots) + 2(y_2 + y_4 + \cdots)\right] $$

$$ |E_S| \leq \frac{(b-a)h^4}{180}\max_{[a,b]}\left|f^{(4)}(x)\right| $$

The trapezoidal error falls like $h^2$; Simpson's falls like $h^4$, so halving $h$
divides the trapezium error by $4$ but Simpson's by $16$.
:::

```figure caption="Trapezoidal rule for $\int_1^2 \frac{dx}{x}$ with $n = 4$, $h = 0.25$. The five ordinates $y_0, \ldots, y_4$ are joined by straight lines. The sliver between chord and curve (magnified inset) is the error, always an over-estimate here because $y = 1/x$ is concave up."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,2.9))
f = lambda x: 1/x
xs = np.linspace(1, 2, 5)
x = np.linspace(0.95, 2.05, 400)
ax.plot(x, f(x), color=ACCENT, lw=2.2, zorder=5)
for i in range(4):
    xa, xb = xs[i], xs[i+1]
    ax.add_patch(plt.Polygon([(xa, 0), (xa, f(xa)), (xb, f(xb)), (xb, 0)],
                             closed=True, facecolor='#dce7f2', edgecolor=MUTED,
                             lw=0.9, zorder=2))
    xf = np.linspace(xa, xb, 60)
    ch = f(xa) + (f(xb)-f(xa))*(xf-xa)/(xb-xa)
    ax.fill_between(xf, f(xf), ch, color='#d9534f', alpha=0.55, zorder=4, lw=0)
for i, xv in enumerate(xs):
    ax.plot([xv, xv], [0, f(xv)], color=MUTED, lw=1.0, zorder=3)
    ax.plot([xv], [f(xv)], 'o', color=INK, ms=4, zorder=6)
    ax.text(xv, -0.075, f'$y_{i}$', fontsize=9.4, color=INK, ha='center')
ax.annotate('', xy=(1.0, 1.12), xytext=(1.25, 1.12),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=7))
ax.text(1.125, 1.16, '$h = 0.25$', fontsize=9.0, color=INK, ha='center')
ax.text(1.02, 0.42, r'$y = 1/x$', fontsize=10, color=ACCENT)
axi = fig.add_axes([0.585, 0.545, 0.305, 0.325], zorder=9)
axi.set_facecolor('white')
xz = np.linspace(1.25, 1.50, 200)
ch2 = f(1.25) + (f(1.50)-f(1.25))*(xz-1.25)/0.25
axi.fill_between(xz, f(xz), ch2, color='#d9534f', alpha=0.6, lw=0)
axi.plot(xz, f(xz), color=ACCENT, lw=2.0)
axi.plot(xz, ch2, color=MUTED, lw=1.5)
axi.set_title('one strip, magnified', fontsize=7.6, pad=3)
axi.annotate('error', xy=(1.375, 0.7385), xytext=(1.375, 0.688),
             fontsize=7.4, color='#d9534f', ha='center',
             arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=0.8,
                             mutation_scale=7))
axi.set_xlim(1.235, 1.515); axi.set_ylim(0.645, 0.825)
axi.set_xticks([1.25, 1.50]); axi.set_yticks([])
axi.tick_params(labelsize=7, length=2)
for sp in axi.spines.values():
    sp.set_visible(True); sp.set_color(MUTED); sp.set_linewidth(0.8)
ax.axhline(0, color=INK, lw=1.0)
ax.set_xlim(0.92, 2.12); ax.set_ylim(-0.16, 1.30)
ax.set_xticks(list(xs)); ax.set_xlabel('$x$')
ax.spines[['top','right','left']].set_visible(False)
ax.set_yticks([0, 0.5, 1.0]); ax.grid(True, axis='y', alpha=.3)
```

```figure caption="Simpson's rule on the same integral. Each pair of strips is covered by the parabola through three ordinates (dashed); it hugs $y = 1/x$ so closely that the two are hard to tell apart, and from exactly the same five ordinates the error falls from $0.003877$ to $0.000107$."
import numpy as np
fig, ax = plt.subplots(figsize=(5.1,3.0))
f = lambda x: 1/x
xs = np.linspace(1, 2, 5)
x = np.linspace(0.97, 2.03, 500)
ax.plot(x, f(x), color=ACCENT, lw=2.6, zorder=4, label='$y = 1/x$')
for k in range(2):
    i = 2*k
    a3 = xs[i:i+3]; y3 = f(a3)
    co = np.polyfit(a3, y3, 2)
    xf = np.linspace(a3[0], a3[2], 120)
    ax.plot(xf, np.polyval(co, xf), color='#d9534f', lw=1.8, ls=(0,(5,3)),
            zorder=6, label='parabolic arcs' if k == 0 else None)
    ax.fill_between(xf, 0, np.polyval(co, xf), color='#f2dede' if k else '#dce7f2',
                    alpha=0.7, zorder=2, lw=0)
for i, xv in enumerate(xs):
    ax.plot([xv, xv], [0, f(xv)], color=MUTED, lw=1.0, zorder=3)
    ax.plot([xv], [f(xv)], 'o', color=INK, ms=4.5, zorder=7)
    ax.text(xv, -0.085, f'$y_{i}$', fontsize=9.4, color=INK, ha='center')
ax.axhline(0, color=INK, lw=1.0)
ax.text(1.06, 0.33, 'weights  $1, 4, 2, 4, 1$', fontsize=9.2, color=MUTED)
ax.text(1.52, 0.13, 'Simpson error $0.000107$;  trapezium error $0.003877$',
        fontsize=8.6, color=INK, ha='center')
ax.set_xlim(0.94, 2.10); ax.set_ylim(-0.18, 1.18)
ax.set_xticks(list(xs)); ax.set_xlabel('$x$')
ax.spines[['top','right','left']].set_visible(False)
ax.set_yticks([0, 0.5, 1.0]); ax.grid(True, axis='y', alpha=.3)
ax.legend(loc='upper right', fontsize=8.8, handlelength=1.8, framealpha=1.0)
```

::: example Worked example 17.14
**Problem.** Evaluate $\displaystyle\int_1^2 \frac{dx}{x}$ by the trapezoidal rule
with $n = 4$, correct to six decimal places, and state a bound for the error.
Compare with the exact value $\ln 2 = 0.693147$.

**Solution.** $h = \dfrac{2-1}{4} = 0.25$. Make the ordinate table.

| $i$ | $x_i$ | $y_i = 1/x_i$ | end / odd / even |
| --- | --- | --- | --- |
| 0 | 1.00 | 1.000000 | end |
| 1 | 1.25 | 0.800000 | interior |
| 2 | 1.50 | 0.666667 | interior |
| 3 | 1.75 | 0.571429 | interior |
| 4 | 2.00 | 0.500000 | end |

$$ \int_1^2 \frac{dx}{x} \approx \frac{h}{2}\left[(y_0 + y_4)
+ 2(y_1 + y_2 + y_3)\right] $$

$$ = \frac{0.25}{2}\left[1.500000 + 2(0.800000 + 0.666667 + 0.571429)\right] $$
$$ = 0.125\left[1.500000 + 2(2.038096)\right] = 0.125(5.576192) = 0.697024 $$

**Error bound.** $f(x) = x^{-1}$, so $f''(x) = 2x^{-3}$, and on $[1, 2]$ this is
largest at $x = 1$: $\max|f''| = 2$. Hence

$$ |E_T| \leq \frac{(b-a)h^2}{12}\max|f''|
= \frac{1 \times (0.25)^2}{12} \times 2 = 0.010417 $$

**Comparison.** The actual error is $0.697024 - 0.693147 = 0.003877$, comfortably
inside the bound, and the estimate is too large — as expected, since $1/x$ is
concave up and the chords lie above the curve.
:::

::: example Worked example 17.15
**Problem.** Repeat with Simpson's rule, $n = 4$, and state the error bound.

**Solution.** The same five ordinates are used, now with the weights
$1, 4, 2, 4, 1$.

| | $y_0$ | $y_1$ | $y_2$ | $y_3$ | $y_4$ |
| --- | --- | --- | --- | --- | --- |
| ordinate | 1.000000 | 0.800000 | 0.666667 | 0.571429 | 0.500000 |
| weight | 1 | 4 | 2 | 4 | 1 |

$$ \int_1^2 \frac{dx}{x} \approx \frac{h}{3}\left[(y_0+y_4) + 4(y_1+y_3)
+ 2y_2\right] $$

$$ = \frac{0.25}{3}\left[1.500000 + 4(1.371429) + 2(0.666667)\right] $$
$$ = 0.083333\left[1.500000 + 5.485716 + 1.333334\right]
= 0.083333(8.319050) = 0.693254 $$

**Error bound.** $f^{(4)}(x) = 24x^{-5}$, largest at $x = 1$, so
$\max|f^{(4)}| = 24$ and

$$ |E_S| \leq \frac{(b-a)h^4}{180}\max\left|f^{(4)}\right|
= \frac{1 \times (0.25)^4}{180} \times 24 = 0.000521 $$

The actual error is $0.693254 - 0.693147 = 0.000107$ — about $36$ times smaller
than the trapezium error from exactly the same five function values.
:::

::: example Worked example 17.16
**Problem.** Evaluate $\displaystyle\int_0^6 \frac{dx}{1+x}$ by (a) the
trapezoidal rule and (b) Simpson's rule, both with $n = 6$. The exact value is
$\ln 7 = 1.945910$.

**Solution.** $h = \dfrac{6-0}{6} = 1$.

| $i$ | $x_i$ | $y_i = 1/(1+x_i)$ | weight (T) | weight (S) |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1.000000 | 1 | 1 |
| 1 | 1 | 0.500000 | 2 | 4 |
| 2 | 2 | 0.333333 | 2 | 2 |
| 3 | 3 | 0.250000 | 2 | 4 |
| 4 | 4 | 0.200000 | 2 | 2 |
| 5 | 5 | 0.166667 | 2 | 4 |
| 6 | 6 | 0.142857 | 1 | 1 |

(a) Sum of the five interior ordinates $= 0.500000 + 0.333333 + 0.250000
+ 0.200000 + 0.166667 = 1.450000$.

$$ T = \frac{1}{2}\left[1.142857 + 2(1.450000)\right]
= \frac{1}{2}(4.042857) = 2.021429 $$

(b) Odd-numbered ordinates: $0.500000 + 0.250000 + 0.166667 = 0.916667$.
Even interior ordinates: $0.333333 + 0.200000 = 0.533333$.

$$ S = \frac{1}{3}\left[1.142857 + 4(0.916667) + 2(0.533333)\right] $$
$$ = \frac{1}{3}\left[1.142857 + 3.666668 + 1.066666\right]
= \frac{1}{3}(5.876191) = 1.958730 $$

Errors: $2.021429 - 1.945910 = 0.075519$ for the trapezium against
$1.958730 - 1.945910 = 0.012820$ for Simpson's rule. The strips are wide here
($h = 1$), so both errors are large, but Simpson's is nearly six times better.
:::

::: caution Simpson's rule needs an even number of strips
$n$ must be even (an odd number of ordinates), because the ordinates are taken
three at a time. With $n = 5$ Simpson's rule simply does not apply. Also be sure
that the $4$s go on the **odd-numbered** ordinates $y_1, y_3, y_5, \ldots$ and
the $2$s on the even-numbered interior ones.
:::

## Chapter summary

- A **binary operation** on $G$ assigns to each ordered pair $(a, b)$ a unique
  element $a * b$ **of $G$**; the closure requirement is part of the definition.
- $(G, *)$ is a **group** if it is closed, associative, has an identity $e$ and
  every element has an inverse; it is **abelian** if $a*b = b*a$ for all
  $a, b$, and the order $|G|$ is the number of elements.
- The **Cayley table** shows closure (all entries in $G$), the identity (a row
  repeating the heading), inverses (one $e$ in each row and column) and the
  abelian property (symmetry about the leading diagonal).
- Standard examples: $(\mathbb{Z}, +)$ infinite abelian; $(Z_4, +_4)$ and
  $\{1, -1, i, -i\}$ under $\times$ finite abelian of order $4$;
  $(\{1,2,3,4\}, \times_5)$ abelian of order $4$; $S_3$ non-abelian of order $6$.
- In any group the identity and each inverse are **unique**.
- **Rolle's theorem.** $f$ continuous on $[a,b]$, differentiable on $(a,b)$ and
  $f(a) = f(b)$ $\Rightarrow$ there is $c \in (a,b)$ with $f'(c) = 0$.
- **Mean Value Theorem.** $f$ continuous on $[a,b]$ and differentiable on
  $(a,b)$ $\Rightarrow$ there is $c \in (a,b)$ with
  $f'(c) = \dfrac{f(b)-f(a)}{b-a}$; it follows from Rolle applied to
  $g(x) = f(x) - f(a) - \frac{f(b)-f(a)}{b-a}(x-a)$.
- **Trapezoidal rule** $\dfrac{h}{2}[(y_0+y_n) + 2(\text{interior})]$ with
  $|E_T| \leq \dfrac{(b-a)h^2}{12}\max|f''|$; **Simpson's rule** ($n$ even)
  $\dfrac{h}{3}[(y_0+y_n) + 4(\text{odd}) + 2(\text{even})]$ with
  $|E_S| \leq \dfrac{(b-a)h^4}{180}\max|f^{(4)}|$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of these is **not** a binary operation on $\mathbb{N}$? <span class="marks">[1]</span>
   (a) $a+b$ (b) $ab$ (c) $a-b$ (d) $\max(a,b)$
2. The identity element of $(Z_4, +_4)$ is <span class="marks">[1]</span>
   (a) $0$ (b) $1$ (c) $2$ (d) $4$
3. In the group $\{1, -1, i, -i\}$ under multiplication, the inverse of $i$ is <span class="marks">[1]</span>
   (a) $i$ (b) $-i$ (c) $1$ (d) $-1$
4. A Cayley table symmetric about the leading diagonal shows the group is <span class="marks">[1]</span>
   (a) finite (b) infinite (c) abelian (d) non-abelian
5. Rolle's theorem requires, in addition to continuity and differentiability, <span class="marks">[1]</span>
   (a) $f(a) = 0$ (b) $f(a) = f(b)$ (c) $f'(a) = f'(b)$ (d) $f$ increasing
6. For $f(x) = x^2$ on $[0, 2]$, the value of $c$ given by the MVT is <span class="marks">[1]</span>
   (a) $0.5$ (b) $1$ (c) $1.5$ (d) $2$
7. Simpson's rule with $n$ strips requires <span class="marks">[1]</span>
   (a) $n$ odd (b) $n$ even (c) $n$ prime (d) any $n$

::: note Answers to Group A
**1.** (c) — $3 - 5 = -2 \notin \mathbb{N}$, so subtraction is not closed.

**2.** (a) — $0 +_4 a = a$ for every $a$.

**3.** (b) — $i \times (-i) = -i^2 = 1$.

**4.** (c) — symmetry means $a*b = b*a$ for all $a, b$.

**5.** (b) — the end values must be equal.

**6.** (b) — $\dfrac{f(2)-f(0)}{2-0} = \dfrac{4}{2} = 2$ and $f'(c) = 2c = 2$ gives $c = 1$.

**7.** (b) — the ordinates are taken three at a time, so $n$ must be even.
:::

**Group B — Short answer (5 marks each)**

1. Construct the composition table of $Z_4 = \{0,1,2,3\}$ under addition modulo
   $4$ and hence show that it is an abelian group. State the inverse of each
   element. <span class="marks">[5]</span>
2. Show that $G = \{1, -1, i, -i\}$ is a group under multiplication. Is it
   abelian? State the inverse of each element. <span class="marks">[5]</span>
3. Verify Rolle's theorem for $f(x) = x^2 - 5x + 6$ on $[2, 3]$ and find $c$. <span class="marks">[5]</span>
4. Verify the Mean Value Theorem for $f(x) = x^2 + 2x + 3$ on $[1, 2]$ and find
   $c$. <span class="marks">[5]</span>
5. Evaluate $\displaystyle\int_1^2 \frac{dx}{x}$ by the trapezoidal rule with
   $n = 4$ and state a bound for the error. <span class="marks">[5]</span>
6. Use Simpson's rule with $n = 6$ to evaluate
   $\displaystyle\int_0^6 \frac{dx}{1+x}$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.**

| $+_4$ | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| **0** | 0 | 1 | 2 | 3 |
| **1** | 1 | 2 | 3 | 0 |
| **2** | 2 | 3 | 0 | 1 |
| **3** | 3 | 0 | 1 | 2 |

*Closure:* every entry is in $\{0,1,2,3\}$. *Associativity:* inherited from
addition of integers. *Identity:* the row and column headed $0$ repeat the
headings, so $e = 0$. *Inverses:* $0^{-1} = 0$, $1^{-1} = 3$, $2^{-1} = 2$,
$3^{-1} = 1$ (each row contains exactly one $0$). The table is symmetric about
the leading diagonal, so $(Z_4, +_4)$ is an **abelian group of order 4**.

**2.**

| $\times$ | $1$ | $-1$ | $i$ | $-i$ |
| --- | --- | --- | --- | --- |
| **$1$** | $1$ | $-1$ | $i$ | $-i$ |
| **$-1$** | $-1$ | $1$ | $-i$ | $i$ |
| **$i$** | $i$ | $-i$ | $-1$ | $1$ |
| **$-i$** | $-i$ | $i$ | $1$ | $-1$ |

Closed (using $i^2 = -1$); associative, since complex multiplication is
associative; identity $e = 1$; and each row contains one $1$, giving
$1^{-1} = 1$, $(-1)^{-1} = -1$, $i^{-1} = -i$, $(-i)^{-1} = i$. The table is
symmetric, so the group **is abelian**, of order $4$.

**3.** $f$ is a polynomial, hence continuous on $[2, 3]$ and differentiable on
$(2, 3)$.

$$ f(2) = 4 - 10 + 6 = 0, \qquad f(3) = 9 - 15 + 6 = 0 $$

so $f(2) = f(3)$ and Rolle's theorem applies. With $f'(x) = 2x - 5$,

$$ 2c - 5 = 0 \;\Longrightarrow\; c = \frac52 = 2.5 \in (2, 3) $$

Rolle's theorem is verified.

**4.** $f$ is a polynomial, so it is continuous on $[1, 2]$ and differentiable on
$(1, 2)$.

$$ f(1) = 1 + 2 + 3 = 6, \qquad f(2) = 4 + 4 + 3 = 11 $$
$$ \frac{f(2)-f(1)}{2-1} = \frac{11-6}{1} = 5 $$

$f'(x) = 2x + 2$, so $f'(c) = 5$ gives

$$ 2c + 2 = 5 \;\Longrightarrow\; c = \frac32 = 1.5 \in (1, 2) $$

**5.** $h = 0.25$; ordinates $y_0 = 1.000000$, $y_1 = 0.800000$,
$y_2 = 0.666667$, $y_3 = 0.571429$, $y_4 = 0.500000$.

$$ T = \frac{0.25}{2}\left[(1.000000 + 0.500000) + 2(2.038096)\right]
= 0.125(5.576192) = 0.697024 $$

With $f''(x) = 2/x^3$ and $\max_{[1,2]}|f''| = 2$,

$$ |E_T| \leq \frac{(2-1)(0.25)^2}{12}(2) = 0.010417 $$

(The true value is $\ln 2 = 0.693147$, so the actual error $0.003877$ satisfies
the bound.)

**6.** $h = 1$; ordinates $1.000000$, $0.500000$, $0.333333$, $0.250000$,
$0.200000$, $0.166667$, $0.142857$.

Odd ordinates: $0.500000 + 0.250000 + 0.166667 = 0.916667$.
Even interior: $0.333333 + 0.200000 = 0.533333$.

$$ S = \frac13\left[(1.000000 + 0.142857) + 4(0.916667) + 2(0.533333)\right] $$
$$ = \frac13(5.876191) = 1.958730 $$

compared with the exact $\ln 7 = 1.945910$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define a binary operation, a group, an abelian group, and the order of a
   finite group. <span class="marks">[3]</span>
   (b) Show that $G = \{1, 2, 3, 4\}$ is an abelian group under multiplication
   modulo $5$, giving the composition table and the inverse of each element.
   Explain why $\{1, 2, 3, 4, 5\}$ under multiplication modulo $6$ is **not** a
   group. <span class="marks">[5]</span>
2. (a) State Rolle's theorem and the Mean Value Theorem, and deduce the Mean Value
   Theorem from Rolle's theorem. <span class="marks">[5]</span>
   (b) Verify the Mean Value Theorem for $f(x) = x^3$ on $[0, 1]$. <span class="marks">[3]</span>
3. (a) Derive the trapezoidal rule for $n$ strips from the area of a single
   trapezium, and write down Simpson's rule with its error bound. <span class="marks">[4]</span>
   (b) Using $n = 4$, evaluate $\displaystyle\int_0^1 \frac{dx}{1+x^2}$ by both
   rules and hence estimate $\pi$. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) A **binary operation** $*$ on a non-empty set $G$ is a rule assigning
to each ordered pair $(a,b)$ of elements of $G$ a unique element $a*b \in G$.
A **group** $(G,*)$ is a set with a binary operation that is closed and
associative, has an identity element $e$ with $e*a = a*e = a$, and in which every
$a$ has an inverse $a^{-1}$ with $a*a^{-1} = a^{-1}*a = e$. It is **abelian** if
$a*b = b*a$ for all $a, b \in G$. The **order** of a finite group is the number
of its elements.

(b)

| $\times_5$ | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| **1** | 1 | 2 | 3 | 4 |
| **2** | 2 | 4 | 1 | 3 |
| **3** | 3 | 1 | 4 | 2 |
| **4** | 4 | 3 | 2 | 1 |

*Closure:* no entry is $0$ and all lie in $G$. *Associativity:* inherited from
integer multiplication. *Identity:* $e = 1$. *Inverses:* $1^{-1} = 1$,
$2^{-1} = 3$ (since $2 \times 3 = 6 \equiv 1$), $3^{-1} = 2$, $4^{-1} = 4$
(since $16 \equiv 1$). The table is symmetric, so $G$ is abelian, of order $4$.

For $\{1,2,3,4,5\}$ under $\times_6$, closure fails: $2 \times_6 3 = 6 \equiv 0$,
and $0$ is not in the set. (Equivalently $2$ and $3$ are not coprime to $6$ and
have no inverses.) Since $6$ is not prime, the construction breaks down.

**2.** (a) *Rolle's theorem.* If $f$ is continuous on $[a,b]$, differentiable on
$(a,b)$ and $f(a) = f(b)$, then there is at least one $c \in (a,b)$ with
$f'(c) = 0$.

*Mean Value Theorem.* If $f$ is continuous on $[a,b]$ and differentiable on
$(a,b)$, then there is at least one $c \in (a,b)$ with
$f'(c) = \dfrac{f(b)-f(a)}{b-a}$.

*Deduction.* Define

$$ g(x) = f(x) - f(a) - \frac{f(b)-f(a)}{b-a}(x-a) $$

Then $g$ is continuous on $[a,b]$ and differentiable on $(a,b)$, being $f$ minus a
linear function, and

$$ g(a) = 0, \qquad g(b) = f(b)-f(a)-\frac{f(b)-f(a)}{b-a}(b-a) = 0 $$

So $g(a) = g(b)$ and Rolle's theorem gives $c \in (a,b)$ with $g'(c) = 0$. Since
$g'(x) = f'(x) - \dfrac{f(b)-f(a)}{b-a}$, this says

$$ f'(c) = \frac{f(b)-f(a)}{b-a} $$

(b) $f(x) = x^3$ is a polynomial, so it is continuous on $[0,1]$ and
differentiable on $(0,1)$.

$$ \frac{f(1)-f(0)}{1-0} = \frac{1-0}{1} = 1 $$

$f'(x) = 3x^2$, so $3c^2 = 1$ gives $c^2 = \dfrac13$ and

$$ c = \frac{1}{\sqrt{3}} = 0.5774 $$

taking the positive root because $c$ must lie in $(0, 1)$. The theorem is
verified.

**3.** (a) Divide $[a,b]$ into $n$ strips of width $h = \dfrac{b-a}{n}$ with
ordinates $y_0, y_1, \ldots, y_n$. Replacing the curve over the $i$th strip by the
chord makes that strip a trapezium of parallel sides $y_{i-1}$, $y_i$ and width
$h$, of area $\dfrac{h}{2}(y_{i-1} + y_i)$. Adding over $i = 1, \ldots, n$, each
interior ordinate appears in two strips and the two end ordinates in one:

$$ \int_a^b f(x)\,dx \approx \frac{h}{2}\left[(y_0 + y_n)
+ 2(y_1 + y_2 + \cdots + y_{n-1})\right] $$

Simpson's rule, for $n$ even, replaces each pair of strips by a parabola through
three ordinates:

$$ \int_a^b f(x)\,dx \approx \frac{h}{3}\left[(y_0 + y_n)
+ 4(y_1 + y_3 + \cdots) + 2(y_2 + y_4 + \cdots)\right],
\qquad |E_S| \leq \frac{(b-a)h^4}{180}\max\left|f^{(4)}\right| $$

(b) $h = 0.25$ and $f(x) = \dfrac{1}{1+x^2}$:

| $i$ | $x_i$ | $y_i$ |
| --- | --- | --- |
| 0 | 0.00 | 1.000000 |
| 1 | 0.25 | 0.941176 |
| 2 | 0.50 | 0.800000 |
| 3 | 0.75 | 0.640000 |
| 4 | 1.00 | 0.500000 |

*Trapezoidal.* Interior sum $= 0.941176 + 0.800000 + 0.640000 = 2.381176$.

$$ T = \frac{0.25}{2}\left[1.500000 + 2(2.381176)\right] = 0.125(6.262352)
= 0.782794 $$

*Simpson.* $y_1 + y_3 = 1.581176$ and $y_2 = 0.800000$.

$$ S = \frac{0.25}{3}\left[1.500000 + 4(1.581176) + 2(0.800000)\right]
= \frac{9.424704}{12} = 0.785392 $$

Since $\displaystyle\int_0^1 \frac{dx}{1+x^2}
= \left[\tan^{-1}x\right]_0^1 = \frac{\pi}{4}$,

$$ \pi \approx 4T = 3.131176 \qquad\text{and}\qquad \pi \approx 4S = 3.141569 $$

Simpson's rule gives $\pi$ correct to four decimal places from the same five
ordinates ($\pi = 3.141593$).
:::
