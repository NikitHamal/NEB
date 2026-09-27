---
subject: Physics
grade: 12
unit: 14
title: Electrical circuits
hours: 6
area: Electricity and Magnetism
---

Ohm's law alone cannot solve a circuit with two cells in different branches, or a
bridge, or a network that is neither series nor parallel. This unit gives you the
two rules that solve *any* network — Kirchhoff's laws — and then applies them to
the three instruments the NEB paper asks about every year: the Wheatstone bridge,
the metre bridge and the potentiometer. It ends with what current actually *does*
in a resistor: it heats it, according to Joule's law.

::: key What the exam wants from this unit
Group B almost always carries one numerical from the metre bridge or the
potentiometer, and one galvanometer-conversion sum. Group C likes
"derive the balance condition of a Wheatstone bridge" and "describe how a
potentiometer measures the internal resistance of a cell". Learn the four boxed
formulas and you can walk through most of them.
:::

## 14.1 Kirchhoff's law

A **junction** (or node) is a point where three or more conductors meet. A **loop**
is any closed conducting path. Kirchhoff gave one rule for each.

::: definition Kirchhoff's two laws
**First law (junction law).** The algebraic sum of the currents meeting at a
junction is zero:
$$ \sum I = 0 $$
Currents flowing *into* the junction are taken positive, those flowing *out*
negative. This is a statement of **conservation of charge** — charge cannot pile
up at a point.

**Second law (loop law).** Around any closed loop, the algebraic sum of the
e.m.f.s equals the algebraic sum of the potential drops $IR$:
$$ \sum E = \sum IR $$
This is a statement of **conservation of energy** — a unit charge taken once
round a loop returns to the same potential.
:::

**Sign rules that never fail.** Choose a direction to walk round the loop, then:

| Element met while walking round | Term to write |
|---|---|
| Resistor traversed *along* the assumed current | $-IR$ |
| Resistor traversed *against* the assumed current | $+IR$ |
| Cell entered at $-$ and left at $+$ | $+E$ |
| Cell entered at $+$ and left at $-$ | $-E$ |

Set the algebraic sum to zero. If a current comes out negative, its true
direction is opposite to the one you assumed — the magnitude is still right, so
**never go back and redraw**.

```figure caption="Two-cell network. Junction A gives $I_3 = I_1 + I_2$; the two loops give two more equations."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0,2.7))

def wire(pts, lw=1.4):
    p = np.array(pts, dtype=float)
    ax.plot(p[:,0], p[:,1], color=INK, lw=lw, solid_capstyle='round', zorder=2)

def res(x, y, lab, lx, ha):
    ax.add_patch(Rectangle((x-0.14, y-0.42), 0.28, 0.84, fc='white', ec=INK,
                           lw=1.2, zorder=3))
    ax.annotate(lab, (lx, y), ha=ha, va='center', fontsize=8.8, color=INK, zorder=4)

def cell(x, y, lab, lx, ha):
    ax.plot([x-0.32, x+0.32], [y+0.12, y+0.12], color=INK, lw=1.3, zorder=3)
    ax.plot([x-0.16, x+0.16], [y-0.12, y-0.12], color=INK, lw=3.4, zorder=3)
    ax.annotate(lab, (lx, y), ha=ha, va='center', fontsize=8.8, color=INK, zorder=4)

def cur(x, y, ang, lab, off):
    dx, dy = 0.36*np.cos(np.radians(ang)), 0.36*np.sin(np.radians(ang))
    ax.annotate('', xy=(x+dx, y+dy), xytext=(x-dx, y-dy),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.5, mutation_scale=11))
    ax.annotate(lab, (x, y), textcoords='offset points', xytext=off,
                ha='center', color=ACCENT, fontsize=9.0, zorder=5)

wire([(0,0),(0,2.2),(6,2.2),(6,0),(0,0)]); wire([(3,2.2),(3,0)])
cell(0, 1.55, '$E_1 = 10$ V', -0.45, 'right')
res(0, 0.75, r'$r_1 = 2\ \Omega$', -0.28, 'right')
cell(6, 1.55, '$E_2 = 9$ V', 6.45, 'left')
res(6, 0.75, r'$r_2 = 3\ \Omega$', 6.28, 'left')
res(3, 1.10, r'$R = 2\ \Omega$', 3.30, 'left')
for nx, ny, nl, o in [(3,2.2,'A',(0,9)), (3,0,'B',(0,-15))]:
    ax.plot([nx],[ny],'o', color=INK, ms=5.5, zorder=5)
    ax.annotate(nl, (nx,ny), textcoords='offset points', xytext=o, ha='center',
                fontsize=10.5, color=INK, weight='bold')
cur(1.55, 2.2, 0, '$I_1$', (0,8))
cur(4.45, 2.2, 180, '$I_2$', (0,8))
cur(3.0, 1.85, -90, '$I_3$', (-15,-4))
ax.annotate('loop 1', (1.4, 0.45), ha='center', fontsize=8.8, color=MUTED, style='italic')
ax.annotate('loop 2', (4.6, 0.45), ha='center', fontsize=8.8, color=MUTED, style='italic')
ax.set_xlim(-2.3, 8.3); ax.set_ylim(-0.85, 2.85); ax.set_aspect('equal'); ax.axis('off')
```
::: example Worked example 14.1
**Problem.** In the network above, $E_1 = 10\ \text{V}$ with $r_1 = 2\ \Omega$,
$E_2 = 9\ \text{V}$ with $r_2 = 3\ \Omega$, and $R = 2\ \Omega$. Find the current
in each branch.

**Solution.** Let $I_1$ and $I_2$ flow towards junction A through the two cells,
and $I_3$ flow from A to B through $R$.

Junction law at A: $I_3 = I_1 + I_2$.

Loop 1 (left cell and $R$), walking with the currents:
$$ E_1 = I_1 r_1 + I_3 R \;\Rightarrow\; 10 = 2I_1 + 2(I_1 + I_2) = 4I_1 + 2I_2 $$

Loop 2 (right cell and $R$):
$$ E_2 = I_2 r_2 + I_3 R \;\Rightarrow\; 9 = 3I_2 + 2(I_1 + I_2) = 2I_1 + 5I_2 $$

From the first, $I_2 = 5 - 2I_1$. Substituting in the second,
$2I_1 + 5(5 - 2I_1) = 9$, so $-8I_1 = -16$ and

$$ I_1 = 2\ \text{A}, \qquad I_2 = 5 - 4 = 1\ \text{A}, \qquad I_3 = 3\ \text{A} $$

Check: the potential at A is $I_3R = 6\ \text{V}$; the left cell drops
$10 - 6 = 4\ \text{V}$ across $2\ \Omega$ (giving 2 A) and the right cell drops
$9 - 6 = 3\ \text{V}$ across $3\ \Omega$ (giving 1 A). Consistent.
:::

::: caution Do not apply the loop law to an open branch
Every loop equation must be written round a **complete conducting path**. A
branch containing an ideal voltmeter or a galvanometer with no current carries
$I = 0$, so its $IR$ term vanishes — but the branch's e.m.f. and the potential
difference across it do **not** vanish. This is exactly how a balanced bridge
works.
:::

## 14.2 Wheatstone bridge circuit; Meter bridge

Four resistors $P, Q, R, S$ form a quadrilateral $ABCD$. A cell is across one
diagonal $AC$ and a galvanometer across the other, $BD$. The bridge is
**balanced** when the galvanometer shows no deflection.

```figure caption="Wheatstone bridge. At balance $V_B = V_D$, the galvanometer reads zero and $P/Q = R/S$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(4.8,3.2))
A=np.array([0,0]); B=np.array([1.75,1.55]); C=np.array([3.5,0]); D=np.array([1.75,-1.55])

def leg(p, q, lab, side=1):
    p, q = np.array(p,dtype=float), np.array(q,dtype=float)
    ax.plot([p[0],q[0]],[p[1],q[1]], color=INK, lw=1.4, zorder=2)
    m=(p+q)/2; d=q-p; n=np.array([-d[1],d[0]]); n=n/np.hypot(*n)
    ang=np.degrees(np.arctan2(d[1],d[0]))
    ax.add_patch(Rectangle((-0.42,-0.13), 0.84, 0.26, fc='white', ec=INK, lw=1.2,
                 zorder=3, transform=(matplotlib.transforms.Affine2D()
                 .rotate_deg(ang).translate(*m) + ax.transData)))
    ax.annotate(lab, m+side*0.46*n, ha='center', va='center', fontsize=9.4,
                color=INK, zorder=4)

leg(A,B,'$P$',  1); leg(B,C,'$Q$', 1); leg(A,D,'$R$', -1); leg(D,C,'$S$', -1)
# galvanometer across BD
ax.plot([B[0],B[0]],[B[1],0.42], color=INK, lw=1.4, zorder=2)
ax.plot([D[0],D[0]],[D[1],-0.42], color=INK, lw=1.4, zorder=2)
ax.add_patch(Circle((1.75,0), 0.42, fc='white', ec=INK, lw=1.3, zorder=3))
ax.annotate('G', (1.75,0), ha='center', va='center', fontsize=10, color=INK, zorder=4)
# cell across AC, routed below
ax.plot([0,-0.95],[0,0], color=INK, lw=1.4)
ax.plot([-0.95,-0.95],[0,-2.5], color=INK, lw=1.4)
ax.plot([-0.95,3.5],[-2.5,-2.5], color=INK, lw=1.4)
ax.plot([3.5,3.5],[-2.5,0], color=INK, lw=1.4)
ax.plot([1.05,1.05],[-2.72,-2.28], color=INK, lw=1.3)
ax.plot([1.38,1.38],[-2.62,-2.38], color=INK, lw=3.2)
ax.annotate('$E$, key $K$', (1.22,-2.95), ha='center', fontsize=8.8, color=INK)
for p, lab, off in [(A,'A',(-13,2)),(B,'B',(0,10)),(C,'C',(12,2)),(D,'D',(0,-13))]:
    ax.plot([p[0]],[p[1]],'o', color=INK, ms=5, zorder=5)
    ax.annotate(lab, p, textcoords='offset points', xytext=off, ha='center',
                fontsize=10.5, color=INK, weight='bold')
ax.annotate('', xy=(0.55,0.49), xytext=(0.20,0.18),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.5, mutation_scale=11))
ax.annotate('$I_1$', (0.30,0.55), color=ACCENT, fontsize=9)
ax.annotate('', xy=(0.55,-0.49), xytext=(0.20,-0.18),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.5, mutation_scale=11))
ax.annotate('$I_2$', (0.30,-0.75), color=ACCENT, fontsize=9)
ax.set_xlim(-1.9,4.6); ax.set_ylim(-3.35,2.25); ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Balance condition of the Wheatstone bridge
At balance no current flows through the galvanometer, so by the junction law the
current $I_1$ in $P$ also flows through $Q$, and the current $I_2$ in $R$ also
flows through $S$.

Since $I_g = 0$, points B and D are at the **same potential**. Hence

- along $ABD$: $V_A - V_B = V_A - V_D$, so $I_1P = I_2R$ &nbsp;(1)
- along $BCD$: $V_B - V_C = V_D - V_C$, so $I_1Q = I_2S$ &nbsp;(2)

Dividing (1) by (2):

$$ \frac{I_1 P}{I_1 Q} = \frac{I_2 R}{I_2 S} \;\Longrightarrow\; \boxed{\frac{P}{Q} = \frac{R}{S}} $$

If three resistances are known the fourth follows. Note that the condition does
**not** involve $E$, $r$ or the galvanometer resistance — this is why the bridge
is a *null* method and is so accurate.
:::

### The metre bridge

The metre bridge is the Wheatstone bridge built from a single uniform wire. A
manganin or constantan wire exactly $100\ \text{cm}$ long is stretched along a
metre scale between copper strips. The unknown resistance $X$ goes in the left
gap and a resistance box $R$ in the right gap. A jockey slides along the wire
until the galvanometer reads zero at a balance length $l$ from the left end.

```figure caption="Metre bridge. The jockey is moved until $G$ reads zero at length $l$; then $X = R\,l/(100-l)$."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(5.2,2.6))
YS, YW = 2.40, 0.0
# copper strips
for x0, x1 in [(0.30,1.70), (4.35,5.65), (8.30,9.70)]:
    ax.add_patch(Rectangle((x0,YS), x1-x0, 0.26, fc='#cfd6e0', ec=INK, lw=1.0, zorder=3))
# gap resistances
for xc, lab, top in [(3.00,'$X$','unknown'), (7.00,'$R$','resistance box')]:
    ax.plot([xc-1.45,xc+1.45],[YS+0.13,YS+0.13], color=INK, lw=1.3, zorder=2)
    ax.add_patch(Rectangle((xc-0.85,YS-0.09), 1.70, 0.44, fc='white', ec=INK,
                           lw=1.3, zorder=4))
    ax.annotate(lab, (xc,YS+0.13), ha='center', va='center', fontsize=9.6, zorder=5)
    ax.annotate(top, (xc,YS+0.62), ha='center', fontsize=8.2, color=MUTED)
# bridge wire and end connections
ax.plot([0.50,9.50],[YW,YW], color='#8a6a3a', lw=3.0, solid_capstyle='butt', zorder=3)
ax.plot([0.50,0.50],[YW,YS], color=INK, lw=1.3)
ax.plot([9.50,9.50],[YW,YS], color=INK, lw=1.3)
# scale
for k in range(11):
    x = 0.50 + k*0.90
    ax.plot([x,x],[-0.07,-0.21], color=MUTED, lw=0.9)
    ax.annotate(str(10*k), (x,-0.50), ha='center', fontsize=6.8, color=MUTED)
ax.annotate('uniform resistance wire, 100 cm', (5.0,-0.92), ha='center',
            fontsize=8.4, color=MUTED)
# galvanometer hanging from terminal B, then across to the jockey
xj = 0.50 + 0.60*9.0
ax.plot([5.00,5.00],[YS,2.15], color=INK, lw=1.3)
ax.add_patch(Circle((5.00,1.82), 0.33, fc='white', ec=INK, lw=1.3, zorder=4))
ax.annotate('G', (5.00,1.82), ha='center', va='center', fontsize=9.6, zorder=5)
ax.plot([5.00,5.00],[1.49,1.15], color=INK, lw=1.3)
ax.plot([5.00,xj],[1.15,1.15], color=INK, lw=1.3)
ax.plot([xj,xj],[1.15,0.10], color='#A8271F', lw=1.6, zorder=4)
ax.plot([xj],[0.04],'v', color='#A8271F', ms=7, zorder=5)
ax.annotate('jockey', (xj+0.16,0.20), fontsize=8.4, color='#A8271F')
# balance lengths
ax.annotate('', xy=(xj,0.60), xytext=(0.50,0.60),
            arrowprops=dict(arrowstyle='<|-|>', color=ACCENT, lw=1.2, mutation_scale=9))
ax.annotate('$l$', ((0.50+xj)/2,0.76), ha='center', color=ACCENT, fontsize=9.6)
ax.annotate('', xy=(9.50,0.60), xytext=(xj,0.60),
            arrowprops=dict(arrowstyle='<|-|>', color=ACCENT, lw=1.2, mutation_scale=9))
ax.annotate('$100-l$', ((9.50+xj)/2,0.76), ha='center', color=ACCENT, fontsize=8.6)
# driver cell and key
ax.plot([0.50,0.50],[YW,-1.55], color=INK, lw=1.3)
ax.plot([0.50,9.50],[-1.55,-1.55], color=INK, lw=1.3)
ax.plot([9.50,9.50],[-1.55,YW], color=INK, lw=1.3)
ax.plot([4.45,4.45],[-1.87,-1.23], color=INK, lw=1.3)
ax.plot([4.78,4.78],[-1.71,-1.39], color=INK, lw=3.4)
ax.plot([5.60,6.05],[-1.55,-1.28], color=INK, lw=1.3, zorder=4)
ax.plot([5.60],[-1.55],'o', color=INK, ms=3.4, zorder=5)
ax.annotate('$E$', (4.62,-2.18), ha='center', fontsize=9.0)
ax.annotate('$K$', (5.85,-1.92), ha='center', fontsize=9.0)
for x, y, lab, o in [(0.50,YS+0.13,'A',(-13,0)), (5.00,YS+0.13,'B',(0,17)),
                     (9.50,YS+0.13,'C',(13,0))]:
    ax.annotate(lab, (x,y), textcoords='offset points', xytext=o, ha='center',
                va='center', fontsize=10.2, weight='bold', color=INK)
ax.set_xlim(-0.6,10.4); ax.set_ylim(-2.45,3.30); ax.set_aspect('equal'); ax.axis('off')
```
If the wire has resistance $\sigma$ per centimetre, the two parts of the wire
have resistances $\sigma l$ and $\sigma(100-l)$. Applying the balance condition,

$$ \frac{X}{R} = \frac{\sigma l}{\sigma(100-l)} \;\Longrightarrow\;
\boxed{X = R\,\frac{l}{100-l}} $$

::: tip Keep the balance point near the middle
The fractional error in $X$ is smallest when $l \approx 50\ \text{cm}$, so choose
$R$ in the box to bring the null point between about 40 cm and 60 cm. Repeating
the reading with $X$ and $R$ **interchanged** and averaging cancels the error
caused by the end resistances of the copper strips.
:::

::: example Worked example 14.2
**Problem.** In a metre bridge the unknown resistance $X$ is in the left gap and
$R = 4\ \Omega$ in the right gap. The balance point is $60\ \text{cm}$ from the
left end. Find $X$, and the new balance point when $X$ and $R$ are interchanged.

**Solution.**
$$ X = R\,\frac{l}{100-l} = 4 \times \frac{60}{40} = 6\ \Omega $$

On interchanging, $R = 4\ \Omega$ is now on the left, so
$$ \frac{4}{6} = \frac{l'}{100-l'} \;\Rightarrow\; 400 - 4l' = 6l'
\;\Rightarrow\; l' = 40\ \text{cm} $$
The balance point simply moves to $100 - 60 = 40\ \text{cm}$, as symmetry
demands.
:::

## 14.3 Potentiometer: Comparison of e.m.f.; measurement of internal resistance of a cell

A potentiometer is a long uniform wire (usually 4 m or 10 m, wound in 1 m
strips) carrying a steady current from a **driver cell** of e.m.f. $E_0$. The
potential falls uniformly along it, so the potential difference across a length
$l$ is $V = kl$, where the **potential gradient**

$$ k = \frac{V_{AB}}{L} \qquad (\text{volt per metre}) $$

is constant as long as the driver current is steady.

::: key Why a potentiometer beats a voltmeter
At the balance point **no current is drawn from the cell being tested**. The
cell therefore has no internal drop $Ir$, and the potentiometer measures the true
**e.m.f.**, not the terminal p.d. A voltmeter always draws some current, so it
always reads slightly low. A potentiometer behaves like a voltmeter of *infinite*
resistance.
:::

### Comparison of e.m.f. of two cells

Connect the two cells $E_1$ and $E_2$ through a two-way key so that either can be
put in the galvanometer branch, with their positive terminals joined to the same
end A as the driver cell. If they balance at lengths $l_1$ and $l_2$,

$$ E_1 = k l_1, \qquad E_2 = k l_2 \;\Longrightarrow\;
\boxed{\frac{E_1}{E_2} = \frac{l_1}{l_2}} $$

### Internal resistance of a cell

```figure caption="Potentiometer set up to find the internal resistance of the cell $E$. With $K_2$ open the balance length is $l_1$; with $K_2$ closed it falls to $l_2$."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(5.0,3.05))
xj = 0.40 + 0.62*8.20
# potentiometer wire
ax.plot([0.40,8.60],[1.50,1.50], color='#8a6a3a', lw=3.0, solid_capstyle='butt', zorder=3)
ax.annotate('A', (0.40,1.50), textcoords='offset points', xytext=(-14,-3),
            fontsize=10.2, weight='bold')
ax.annotate('B', (8.60,1.50), textcoords='offset points', xytext=(11,-3),
            fontsize=10.2, weight='bold')
# driver (primary) circuit
ax.plot([0.40,0.40],[1.50,3.10], color=INK, lw=1.3)
ax.plot([0.40,8.60],[3.10,3.10], color=INK, lw=1.3)
ax.plot([8.60,8.60],[3.10,1.50], color=INK, lw=1.3)
ax.plot([2.70,2.70],[2.78,3.42], color=INK, lw=1.3)
ax.plot([3.03,3.03],[2.94,3.26], color=INK, lw=3.4)
ax.annotate('$E_0$', (2.86,3.68), ha='center', fontsize=9.2)
ax.plot([4.10,4.55],[3.10,3.40], color=INK, lw=1.3, zorder=4)
ax.plot([4.10],[3.10],'o', color=INK, ms=3.4, zorder=5)
ax.annotate('$K_1$', (4.45,3.68), ha='center', fontsize=9.2)
ax.add_patch(Rectangle((5.90,2.95), 1.00, 0.30, fc='white', ec=INK, lw=1.2, zorder=3))
ax.annotate('Rh', (6.40,3.10), ha='center', va='center', fontsize=8.2, zorder=4)
ax.annotate('primary circuit', (6.40,3.62), ha='center', fontsize=8.2,
            color=MUTED, style='italic')
# jockey and balance length
ax.plot([xj],[1.56],'v', color='#A8271F', ms=7, zorder=5)
ax.plot([xj,xj],[1.50,0.75], color='#A8271F', lw=1.6, zorder=4)
ax.annotate('jockey J', (xj+0.16,1.06), fontsize=8.4, color='#A8271F')
ax.annotate('', xy=(xj,1.98), xytext=(0.40,1.98),
            arrowprops=dict(arrowstyle='<|-|>', color=ACCENT, lw=1.2, mutation_scale=9))
ax.annotate('balance length $l$', ((0.40+xj)/2,2.16), ha='center',
            color=ACCENT, fontsize=8.8)
# secondary circuit: test cell + galvanometer
ax.plot([0.40,0.40],[1.50,-0.60], color=INK, lw=1.3)
ax.plot([0.40,2.60],[-0.60,-0.60], color=INK, lw=1.3)
ax.plot([2.60,2.60],[-0.60,0.75], color=INK, lw=1.3)
ax.plot([2.60,xj],[0.75,0.75], color=INK, lw=1.3)
ax.plot([1.02,1.02],[-0.92,-0.28], color=INK, lw=1.3)
ax.plot([1.35,1.35],[-0.76,-0.44], color=INK, lw=3.4)
ax.annotate('$E$, $r$', (1.18,-1.24), ha='center', fontsize=9.2)
ax.add_patch(Circle((4.05,0.75), 0.34, fc='white', ec=INK, lw=1.3, zorder=4))
ax.annotate('G', (4.05,0.75), ha='center', va='center', fontsize=9.6, zorder=5)
# shunt R with key K2 across the test cell
ax.plot([0.40,0.40],[-0.60,-2.05], color=INK, lw=1.3)
ax.plot([0.40,2.60],[-2.05,-2.05], color=INK, lw=1.3)
ax.plot([2.60,2.60],[-2.05,-0.60], color=INK, lw=1.3)
ax.add_patch(Rectangle((0.78,-2.20), 0.90, 0.30, fc='white', ec=INK, lw=1.2, zorder=3))
ax.annotate('$R$', (1.23,-2.05), ha='center', va='center', fontsize=9.0, zorder=4)
ax.plot([2.05,2.48],[-2.05,-1.78], color=INK, lw=1.3, zorder=4)
ax.plot([2.05],[-2.05],'o', color=INK, ms=3.4, zorder=5)
ax.annotate('$K_2$', (2.30,-2.52), ha='center', fontsize=9.2)
ax.annotate('secondary circuit', (5.6,-0.30), ha='center', fontsize=8.2,
            color=MUTED, style='italic')
ax.set_xlim(-0.9,9.7); ax.set_ylim(-2.85,3.95); ax.set_aspect('equal'); ax.axis('off')
```
::: derivation Internal resistance from two balance lengths
**Step 1 — key $K_2$ open.** No current is drawn from the test cell, so the
potentiometer balances against its full e.m.f.:
$$ E = k l_1 $$

**Step 2 — key $K_2$ closed.** The cell now drives a current through the known
resistance $R$. At the new balance point the potentiometer matches the
*terminal p.d.*:
$$ V = k l_2, \qquad V = \frac{ER}{R+r} $$

**Step 3 — divide.**
$$ \frac{E}{V} = \frac{l_1}{l_2} = \frac{R+r}{R}
\;\Longrightarrow\; \frac{l_1}{l_2} - 1 = \frac{r}{R} $$

$$ \boxed{r = R\left(\frac{l_1 - l_2}{l_2}\right)} $$
:::

::: caution The balance point must exist
If the driver cell's e.m.f. $E_0$ is less than the e.m.f. being measured, the
potential drop over the whole wire is too small and the galvanometer deflects the
*same way* everywhere — there is no null point. Always take $E_0 > E$, and check
that the positive terminals of both cells are connected to the **same** end of
the wire. One-sided deflection at both ends is the classic symptom of a reversed
cell.
:::

::: example Worked example 14.3
**Problem.** A cell balances at $l_1 = 240\ \text{cm}$ on a potentiometer. When a
resistance of $5\ \Omega$ is connected across its terminals the balance length
falls to $l_2 = 200\ \text{cm}$. Find the internal resistance of the cell. If the
potential gradient is $2.0\ \text{mV cm}^{-1}$, find the e.m.f. as well.

**Solution.**
$$ r = R\left(\frac{l_1-l_2}{l_2}\right) = 5\left(\frac{240-200}{200}\right)
= 5 \times 0.2 = 1\ \Omega $$

$$ E = k l_1 = (2.0\times10^{-3}\ \text{V cm}^{-1})(240\ \text{cm}) = 0.48\ \text{V} $$
:::

## 14.4 Super conductors; Perfect conductors

The resistivity of a normal metal falls as it is cooled, because the lattice ions
vibrate less and scatter electrons less. But it never reaches zero: impurities
and defects leave a **residual resistivity** even at $0\ \text{K}$.

Certain materials behave completely differently. Below a sharp **critical
temperature** $T_c$ their resistivity drops abruptly to zero — not "very small",
but zero, as far as any measurement can tell. Kamerlingh Onnes discovered this in
mercury in 1911 at $T_c = 4.2\ \text{K}$.

```figure caption="Resistance against temperature. A normal metal (blue) keeps a residual resistance; a superconductor (red) drops to exactly zero at $T_c$."

import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
T = np.linspace(0, 20, 400); Tc = 7.2
ax.plot(T, 0.22 + 0.052*T, color=ACCENT, lw=1.9, label='normal metal')
ax.plot([0, Tc], [0, 0], color='#A8271F', lw=2.6, zorder=4)
ax.plot([Tc, Tc], [0, 0.052*Tc], color='#A8271F', lw=2.6, zorder=4)
ax.plot(T[T>=Tc], 0.052*T[T>=Tc], color='#A8271F', lw=2.6, label='superconductor')
ax.plot([Tc,Tc],[0,1.35], color=MUTED, lw=0.9, ls=':')
ax.plot([Tc],[0],'o', color='#A8271F', ms=5, zorder=5)
ax.annotate('$T_c$', (Tc,0), textcoords='offset points', xytext=(0,-20),
            ha='center', color='#A8271F', fontsize=10.5)
ax.annotate('residual\nresistance', xy=(0.15,0.23), xytext=(2.4,0.52),
            fontsize=8.2, color=ACCENT, ha='left', va='center',
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.0, mutation_scale=9))
ax.annotate(r'$\rho = 0$', (2.9,0.055), fontsize=9.0, color='#A8271F', ha='center')
ax.set_xlabel('temperature  $T$  (K)'); ax.set_ylabel('resistance  $R$')
ax.set_xlim(0,20); ax.set_ylim(-0.06,1.35)
ax.set_xticks([0,5,10,15,20]); ax.set_yticks([])
ax.spines[['top','right']].set_visible(False); ax.grid(True, axis='x', alpha=.40)
ax.legend(loc='upper left')
```
::: definition Superconductor
A superconductor is a material whose electrical resistivity becomes exactly zero
below a critical temperature $T_c$, and which at the same time expels magnetic
flux from its interior, so that $B = 0$ inside it (the **Meissner effect**).
:::

**Perfect conductor versus superconductor.** A *perfect conductor* is an
idealisation: a material with $\rho = 0$ but with no other special property.
The distinction is not academic, and examiners like it:

| | Perfect conductor (hypothetical) | Superconductor (real) |
|---|---|---|
| Resistivity | zero | zero |
| Defined by | $\rho = 0$ only | $\rho = 0$ **and** $B = 0$ inside |
| Cooled in a magnetic field | *traps* the flux already inside it, because $d\vec{B}/dt = 0$ | *expels* the flux completely (Meissner effect) |
| Final state | depends on the history of cooling and magnetising | same state whatever the order — a true thermodynamic phase |
| Exists? | no | yes, below $T_c$ |

A superconductor is destroyed by too large a magnetic field (the **critical
field** $B_c$, which falls to zero at $T_c$) or by too large a current (the
**critical current**). Both limits matter in real magnets.

**High-temperature superconductors.** In 1986–87 ceramic oxides such as
YBa₂Cu₃O₇ were found to superconduct up to about 92 K — above the boiling point
of liquid nitrogen (77 K), which is cheap. Uses: MRI and NMR magnets,
particle-accelerator magnets, maglev trains, SQUID magnetometers, and
loss-free power cables.

## 14.5 Conversion of galvanometer into voltmeter and ammeter; Ohmmeter

A moving-coil galvanometer has a resistance $G$ and gives full-scale deflection
for a small current $I_g$ (typically a few milliamperes). It is the movement
inside every analogue meter; only the resistor bolted to it changes.

```figure caption="Left: a low shunt $S$ in parallel makes an ammeter. Right: a high resistance $R$ in series makes a voltmeter."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.6))

def galv(ax, x, y, r=0.36):
    ax.add_patch(Circle((x,y), r, fc='white', ec=INK, lw=1.3, zorder=3))
    ax.annotate('G', (x,y), ha='center', va='center', fontsize=9.6, zorder=4)

ax = axes[0]
ax.plot([-1.45,-0.50],[0,0], color=INK, lw=1.4)
ax.plot([0.50,1.45],[0,0], color=INK, lw=1.4)
galv(ax, 0, 0)
ax.plot([-0.50,-0.50],[0,-1.00], color=INK, lw=1.4)
ax.plot([0.50,0.50],[0,-1.00], color=INK, lw=1.4)
ax.plot([-0.50,0.50],[-1.00,-1.00], color=INK, lw=1.4)
ax.add_patch(Rectangle((-0.44,-1.15), 0.88, 0.30, fc='white', ec=INK, lw=1.2, zorder=3))
ax.annotate('$S$', (0,-1.00), ha='center', va='center', fontsize=9.4, zorder=4)
ax.annotate('shunt (low)', (0,-1.52), ha='center', fontsize=8.0, color=MUTED)
for xt in (-1.45, 1.45):
    ax.plot([xt],[0],'o', color=INK, ms=4.5, zorder=4)
ax.annotate('', xy=(-0.80,0.34), xytext=(-1.35,0.34),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.4, mutation_scale=10))
ax.annotate('$I$', (-1.07,0.50), ha='center', color=ACCENT, fontsize=9.4)
ax.annotate('$I_g$', (0,0.52), ha='center', color=ACCENT, fontsize=9.2)
ax.annotate('$I-I_g$', (0,-0.62), ha='center', color=ACCENT, fontsize=9.2)
ax.annotate('$G$', (0.42,0.36), ha='left', fontsize=8.6, color=MUTED)
ax.set_title('ammeter: shunt in parallel', fontsize=8.8)
ax.set_xlim(-1.9,1.9); ax.set_ylim(-2.0,1.0); ax.set_aspect('equal'); ax.axis('off')

ax = axes[1]
ax.plot([-1.65,-0.51],[0,0], color=INK, lw=1.4)
galv(ax, -0.15, 0)
ax.plot([0.21,0.60],[0,0], color=INK, lw=1.4)
ax.add_patch(Rectangle((0.60,-0.15), 0.90, 0.30, fc='white', ec=INK, lw=1.2, zorder=3))
ax.annotate('$R$', (1.05,0.42), ha='center', fontsize=9.4, zorder=4)
ax.annotate('multiplier (high)', (1.05,-0.62), ha='center', fontsize=8.0, color=MUTED)
ax.plot([1.50,2.05],[0,0], color=INK, lw=1.4)
for xt in (-1.65, 2.05):
    ax.plot([xt],[0],'o', color=INK, ms=4.5, zorder=4)
ax.annotate('', xy=(2.05,-1.10), xytext=(-1.65,-1.10),
            arrowprops=dict(arrowstyle='<|-|>', color=ACCENT, lw=1.2, mutation_scale=9))
ax.annotate('p.d. $V$ to be measured', (0.2,-1.52), ha='center',
            color=ACCENT, fontsize=8.4)
ax.annotate('$I_g$', (-0.15,0.52), ha='center', color=ACCENT, fontsize=9.2)
ax.set_title('voltmeter: high $R$ in series', fontsize=8.8)
ax.set_xlim(-2.2,2.6); ax.set_ylim(-2.0,1.0); ax.set_aspect('equal'); ax.axis('off')
```
::: derivation Shunt for an ammeter, multiplier for a voltmeter
**Ammeter.** To read up to a current $I$, a low resistance $S$ (the **shunt**) is
joined in parallel with the galvanometer so that only $I_g$ passes through the
coil and $(I - I_g)$ bypasses it. The p.d. across the parallel pair is the same:

$$ I_g G = (I - I_g)S \;\Longrightarrow\; \boxed{S = \frac{I_g G}{I - I_g}} $$

The resistance of the finished ammeter is $R_A = \dfrac{GS}{G+S}$, which is very
small — an ammeter must be connected **in series** and must not disturb the
current. An ideal ammeter has zero resistance.

**Voltmeter.** To read up to a p.d. $V$, a high resistance $R$ (the
**multiplier**) is joined in series, chosen so that the current is exactly $I_g$
when the p.d. is $V$:

$$ V = I_g(G + R) \;\Longrightarrow\; \boxed{R = \frac{V}{I_g} - G} $$

The resistance of the finished voltmeter is $G + R$, which is very large — a
voltmeter is connected **in parallel** and must draw as little current as
possible. An ideal voltmeter has infinite resistance.
:::

### The ohmmeter

An ohmmeter is a galvanometer, a cell of e.m.f. $E$ and an adjustable resistor
$R$ in series, with two test leads. First the leads are touched together
(zero external resistance) and $R$ is adjusted so that the deflection is exactly
full scale:

$$ I_g = \frac{E}{G + R} $$

With an unknown resistance $X$ between the leads the current becomes

$$ I = \frac{E}{G + R + X} $$

so each deflection corresponds to one value of $X$. Two features follow at once
and are often asked:

- the scale is **non-uniform** (cramped at large $X$), because $I$ is not
  proportional to $X$;
- the scale is **reversed**: zero ohms is at the full-scale end (right) and
  infinite ohms at the zero-current end (left).

::: example Worked example 14.4
**Problem.** A galvanometer of resistance $G = 50\ \Omega$ gives full-scale
deflection for $I_g = 2\ \text{mA}$. How would you convert it into
(a) an ammeter reading $0$–$5\ \text{A}$, and (b) a voltmeter reading
$0$–$10\ \text{V}$? Find the resistance of each finished instrument.

**Solution.**

(a) $I = 5\ \text{A}$, $I_g = 2\times10^{-3}\ \text{A}$:
$$ S = \frac{I_gG}{I-I_g} = \frac{(2\times10^{-3})(50)}{5 - 0.002}
= \frac{0.100}{4.998} = 0.0200\ \Omega $$
A shunt of about $0.02\ \Omega$ is connected **in parallel**. Meter resistance
$$ R_A = \frac{GS}{G+S} = \frac{50 \times 0.0200}{50.02} = 0.0200\ \Omega $$

(b) $V = 10\ \text{V}$:
$$ R = \frac{V}{I_g} - G = \frac{10}{2\times10^{-3}} - 50 = 5000 - 50 = 4950\ \Omega $$
This is connected **in series**; the voltmeter's resistance is
$G + R = 5000\ \Omega$, i.e. $500\ \Omega$ per volt.
:::

## 14.6 Joule's law

When a current passes through a conductor, the ordered drift energy the electrons
gain from the field is handed to the lattice in collisions, and the conductor
warms up.

::: derivation Joule's law of heating
In time $t$ a charge $q = It$ moves through a potential difference $V$. The work
done by the source on this charge is

$$ W = qV = VIt $$

None of it appears as kinetic energy, because the drift velocity stays constant;
all of it appears as heat. Using $V = IR$,

$$ \boxed{H = I^{2}Rt = VIt = \frac{V^{2}}{R}t} $$

and the rate of heating — the power dissipated — is
$P = H/t = I^2R = V^2/R$.
:::

The three statements usually quoted as **Joule's laws** are just the three
proportionalities hidden in $H = I^2Rt$:

1. $H \propto I^{2}$ when $R$ and $t$ are constant;
2. $H \propto R$ when $I$ and $t$ are constant;
3. $H \propto t$ when $I$ and $R$ are constant.

If the heat is wanted in calories, divide by the mechanical equivalent of heat
$J = 4.2\ \text{J cal}^{-1}$: $H = I^2Rt/J$ calories.

::: caution Which formula for resistors in series and in parallel?
For resistors **in series** the current $I$ is common, so use $H = I^2Rt$ and the
**largest** resistance gets hottest. For resistors **in parallel** the voltage
$V$ is common, so use $H = V^2t/R$ and the **smallest** resistance gets hottest.
Picking the wrong form reverses the answer — this is a favourite Group A trap.
:::

**Where it is used.** Heaters, immersion rods, electric irons and incandescent
lamps use a high-resistivity alloy (nichrome, $\rho \approx 1.1\times10^{-6}\
\Omega\,\text{m}$) with a high melting point. A **fuse** does the opposite job:
a short piece of low-melting tin–lead alloy that melts and breaks the circuit
when $I^2R$ heating becomes dangerous. Electrical energy is sold in
**kilowatt-hours**: $1\ \text{kWh} = 1000 \times 3600 = 3.6\times10^{6}\ \text{J}$.

::: example Worked example 14.5
**Problem.** An electric kettle is marked "1500 W, 230 V". It is used to heat
$1.0\ \text{kg}$ of water from $20\,^{\circ}\text{C}$ to $100\,^{\circ}\text{C}$.
If 80 % of the electrical energy reaches the water, how long does it take? Take
the specific heat capacity of water as $4200\ \text{J kg}^{-1}\text{K}^{-1}$.
Also find the resistance of the element.

**Solution.** Heat required by the water:
$$ Q = mc\,\Delta\theta = (1.0)(4200)(100-20) = 3.36\times10^{5}\ \text{J} $$

Useful power delivered $= 0.80 \times 1500 = 1200\ \text{W}$, so

$$ t = \frac{Q}{P_{\text{useful}}} = \frac{3.36\times10^{5}}{1200}
= 280\ \text{s} = 4\ \text{min}\ 40\ \text{s} $$

Resistance of the element at its working temperature:
$$ R = \frac{V^{2}}{P} = \frac{230^{2}}{1500} = \frac{52900}{1500}
= 35.3\ \Omega $$
:::

## Chapter summary

- Kirchhoff's junction law $\sum I = 0$ expresses conservation of charge; the
  loop law $\sum E = \sum IR$ expresses conservation of energy.
- A Wheatstone bridge is balanced when $I_g = 0$, and then $P/Q = R/S$. The
  condition is independent of the cell and of the galvanometer.
- Metre bridge: $X = R\,l/(100-l)$, with $l$ measured from the end next to $X$.
  Keep $l$ near 50 cm and interchange $X$ and $R$ to cancel end errors.
- Potentiometer: $V = kl$ with $k = V_{AB}/L$. Comparison of e.m.f.
  $E_1/E_2 = l_1/l_2$; internal resistance $r = R(l_1-l_2)/l_2$. At balance the
  cell supplies no current, so the true e.m.f. is measured.
- A superconductor has $\rho = 0$ below $T_c$ **and** expels magnetic flux
  (Meissner effect); a merely perfect conductor would trap the flux instead.
- Galvanometer conversions: ammeter $S = I_gG/(I-I_g)$ in parallel;
  voltmeter $R = V/I_g - G$ in series. An ohmmeter has a reversed, non-uniform
  scale.
- Joule's law: $H = I^2Rt = VIt = V^2t/R$; power $P = I^2R = V^2/R$;
  $1\ \text{kWh} = 3.6\times10^{6}\ \text{J}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Kirchhoff's junction law is a consequence of the conservation of <span class="marks">[1]</span>
   (a) energy (b) charge (c) momentum (d) magnetic flux
2. In a balanced Wheatstone bridge, the current through the galvanometer is <span class="marks">[1]</span>
   (a) maximum (b) zero (c) half the main current (d) equal to the main current
3. A potentiometer measures the e.m.f. of a cell more accurately than a voltmeter because at balance it <span class="marks">[1]</span>
   (a) has a very low resistance (b) draws no current from the cell
   (c) uses a longer wire (d) is calibrated in volts
4. To convert a galvanometer into an ammeter, we connect a <span class="marks">[1]</span>
   (a) high resistance in series (b) high resistance in parallel
   (c) low resistance in series (d) low resistance in parallel
5. Two resistors of $2\ \Omega$ and $4\ \Omega$ are joined in parallel across a battery. The ratio of the heat produced in them in a given time is <span class="marks">[1]</span>
   (a) $1:2$ (b) $2:1$ (c) $1:4$ (d) $4:1$
6. Below its critical temperature a superconductor <span class="marks">[1]</span>
   (a) has infinite resistance (b) becomes an insulator
   (c) expels magnetic flux from its interior (d) traps all the flux inside it

::: note Answers to Group A
**1.** (b) — charge cannot accumulate at a junction, so what flows in must flow out.
**2.** (b) — balance is defined by the null (zero) galvanometer deflection.
**3.** (b) — with no current drawn there is no internal drop $Ir$, so the reading is the true e.m.f.
**4.** (d) — the shunt $S = I_gG/(I-I_g)$ is small and goes in parallel.
**5.** (b) — in parallel $V$ is common, so $H = V^2t/R \propto 1/R$, giving $H_2:H_4 = \frac14 : \frac12$ inverted, i.e. $2:1$.
**6.** (c) — the Meissner effect; that, plus $\rho = 0$, defines superconductivity.
:::

**Group B — Short answer (5 marks each)**

1. State Kirchhoff's laws and name the conservation principle behind each.
   Using them, obtain the balance condition of a Wheatstone bridge. <span class="marks">[5]</span>
2. In a metre bridge the unknown resistance $X$ is in the left gap and a
   $6\ \Omega$ resistance in the right gap. The balance point is $40\ \text{cm}$
   from the left end. Find $X$ and the new balance length if the two are
   interchanged. <span class="marks">[5]</span>
3. A cell balances against $150\ \text{cm}$ of a potentiometer wire. When a
   $4\ \Omega$ resistor is connected across the cell, the balance length becomes
   $120\ \text{cm}$. Calculate the internal resistance of the cell. <span class="marks">[5]</span>
4. A galvanometer of resistance $100\ \Omega$ gives full-scale deflection for
   $1\ \text{mA}$. Find the resistance needed to convert it into (a) an ammeter
   reading up to $1\ \text{A}$ and (b) a voltmeter reading up to $5\ \text{V}$. <span class="marks">[5]</span>
5. Distinguish between a perfect conductor and a superconductor. Why is a
   superconducting magnet cooled below $T_c$ *before* the field is switched on? <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Junction law $\sum I = 0$ (conservation of charge); loop law
$\sum E = \sum IR$ (conservation of energy). At balance $I_g = 0$, so $I_1$ flows
through $P$ and $Q$ and $I_2$ through $R$ and $S$, and $V_B = V_D$. Then
$I_1P = I_2R$ and $I_1Q = I_2S$; dividing gives $P/Q = R/S$.

**2.** $X = R\,l/(100-l) = 6 \times 40/60 = 4\ \Omega$. Interchanged, the left gap
holds $6\ \Omega$, so $6/4 = l'/(100-l')$, giving $600 - 6l' = 4l'$ and
$l' = 60\ \text{cm}$.

**3.** $r = R\left(\dfrac{l_1-l_2}{l_2}\right) = 4\left(\dfrac{150-120}{120}\right)
= 4 \times 0.25 = 1\ \Omega$.

**4.** (a) $S = \dfrac{I_gG}{I-I_g} = \dfrac{(10^{-3})(100)}{1-0.001}
= \dfrac{0.1}{0.999} = 0.100\ \Omega$ in parallel.
(b) $R = \dfrac{V}{I_g} - G = \dfrac{5}{10^{-3}} - 100 = 5000 - 100 = 4900\ \Omega$
in series.

**5.** A perfect conductor only has $\rho = 0$; a superconductor also has $B = 0$
inside it. If a perfect conductor were cooled in a field it would trap that flux,
because $d\vec{B}/dt = 0$ inside a resistanceless material; a superconductor
expels the flux (Meissner effect) whatever the order of cooling and magnetising.
In practice the magnet is cooled first so that the whole winding is
superconducting before any current — and hence any $I^2R$ heating at a normal
spot — can appear; a normal region would heat, spread, and "quench" the magnet.
:::

**Group C — Long answer (8 marks each)**

1. (a) Draw a labelled diagram of a potentiometer arranged to compare the e.m.f.s
   of two cells, and derive $E_1/E_2 = l_1/l_2$. <span class="marks">[4]</span>
   (b) A Daniell cell of e.m.f. $1.08\ \text{V}$ balances at $216\ \text{cm}$.
   A second cell balances at $300\ \text{cm}$ on the same wire. Find the e.m.f. of
   the second cell and the potential gradient of the wire. <span class="marks">[4]</span>
2. (a) State and derive Joule's law of heating, and explain why the element of a
   heater glows red while its copper connecting leads stay cool. <span class="marks">[4]</span>
   (b) An electric heater marked "1000 W, 220 V" is used for $5$ hours a day for
   $30$ days. Find its resistance, the current it draws, and the monthly cost of
   running it at NPR 10 per unit. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (b) Since $E \propto l$ for the same wire and driver current,
$$ E_2 = E_1\frac{l_2}{l_1} = 1.08 \times \frac{300}{216} = 1.50\ \text{V} $$
Potential gradient $k = E_1/l_1 = 1.08/216 = 5.0\times10^{-3}\ \text{V cm}^{-1}
= 0.50\ \text{V m}^{-1}$.

**2.** (a) $W = qV = VIt = I^2Rt$, all of which appears as heat since the drift
velocity is unchanged. In a series path the current is the same everywhere, so
$H \propto R$: the nichrome element has a resistance of tens of ohms and a high
melting point, while the thick copper leads have a resistance of a fraction of an
ohm, so almost all the heat is produced in the element.

(b) $R = V^2/P = 220^2/1000 = 48.4\ \Omega$;
$I = P/V = 1000/220 = 4.55\ \text{A}$.
Energy $= 1.0\ \text{kW} \times 5\ \text{h} \times 30 = 150\ \text{kWh}$, so the
cost is $150 \times 10 = $ NPR $1500$ per month.
:::
