---
subject: Physics
grade: 12
unit: 4
title: First Law of Thermodynamics
hours: 6
area: Heat and Thermodynamics
---

Thermodynamics is the book-keeping of energy. A gas trapped in a cylinder can be
heated, compressed, allowed to expand, or left alone — and in every case the
energy that goes in must equal the energy that comes out plus whatever stays
behind inside the gas. That single statement, written carefully, is the first
law. This unit teaches you to write it correctly, to compute the work from a
pressure–volume graph, and to apply it to the four processes that every NEB
paper asks about.

::: key What the exam wants from this unit
Three things repeat every year: (i) state the first law with correct sign
conventions, (ii) derive $C_p - C_v = R$, and (iii) derive $PV^{\gamma} = $
constant and the work done in an isothermal or adiabatic change. Everything else
is numerical substitution into those results.
:::

## 4.1 Thermodynamic systems

A **system** is the definite quantity of matter we choose to study — usually a
fixed mass of gas in a cylinder. Everything outside it that can exchange energy
with it is the **surroundings**. The real or imagined surface separating the two
is the **boundary**.

| Type of system | Exchanges matter? | Exchanges energy? | Example |
|---|---|---|---|
| Open | yes | yes | water boiling in an open pan |
| Closed | no | yes | gas sealed in a metal cylinder |
| Isolated | no | no | hot tea in a perfect thermos flask |

```figure caption="The three kinds of thermodynamic system, classified by what can cross the boundary."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0,2.6))
info = [(1.35,'Open','matter','energy',True,True),
        (4.55,'Closed','matter','energy',False,True),
        (7.75,'Isolated','matter','energy',False,False)]
for x0,title,l1,l2,m_ok,e_ok in info:
    ax.add_patch(Rectangle((x0,0.80),1.45,1.25, fc='#e8f0f8', ec=ACCENT, lw=1.6))
    ax.text(x0+0.725,1.42,'system',ha='center',va='center',color=INK,fontsize=8.6)
    ax.text(x0+0.725,2.42,title,ha='center',va='center',color=INK,fontsize=10)
    for y,lab,ok,col in [(1.74,l1,m_ok,'#2e8b57'),(1.08,l2,e_ok,'#d9534f')]:
        c = col if ok else MUTED
        tip = x0-0.04 if ok else x0-0.26
        ax.annotate('', xy=(tip,y), xytext=(x0-1.20,y),
                    arrowprops=dict(arrowstyle='-|>', color=c, lw=1.5,
                                    linestyle='-' if ok else (0,(2.5,2)),
                                    shrinkA=0, shrinkB=0, mutation_scale=11))
        ax.text(x0-0.70,y+0.17,lab,ha='center',va='bottom',color=c,fontsize=7.8)
        if not ok:
            ax.plot([x0-0.84,x0-0.56],[y-0.13,y+0.13],color='#d9534f',lw=1.6)
            ax.plot([x0-0.84,x0-0.56],[y+0.13,y-0.13],color='#d9534f',lw=1.6)
    if not e_ok:
        ax.add_patch(Rectangle((x0-0.09,0.71),1.63,1.43, fc='none', ec=INK,
                               lw=1.2, ls=(0,(4,2))))
ax.set_xlim(-0.15,9.50); ax.set_ylim(0.45,2.80); ax.axis('off')
```

The condition of a system is fixed by its **state variables** $P$, $V$, $T$ and
the amount of gas $n$. For an ideal gas these are tied together by the equation
of state

$$ PV = nRT, \qquad R = 8.314\ \text{J mol}^{-1}\text{K}^{-1} $$

so only two of them can be chosen freely. That is why a state can be shown as a
single point on a $P$–$V$ graph, and a process as a curve. Such a graph is called
an **indicator diagram**.

A system is in **thermodynamic equilibrium** when it is simultaneously in
mechanical equilibrium (no unbalanced pressure), thermal equilibrium (one uniform
temperature) and chemical equilibrium (no reaction in progress). Only then do $P$
and $T$ have single definite values, and only then can the process be drawn as a
smooth curve. Such an idealised, infinitely slow process is called **quasi-static**.

::: definition State function and path function
A **state function** depends only on the present state, not on how the system got
there — pressure, volume, temperature and internal energy are state functions.
A **path function** depends on the route taken between two states — heat and work
are path functions. This is why we write $\Delta U$ but never "$\Delta Q$".
:::

## 4.2 Work done during volume change

Consider a gas at pressure $P$ inside a cylinder closed by a frictionless piston
of area $A$. The gas pushes the piston with force $F = PA$. If the piston moves
out through a small distance $dx$, so slowly that the pressure stays essentially
constant during the move, the work done **by the gas** is

$$ dW = F\,dx = PA\,dx = P\,dV $$

since $A\,dx = dV$ is the increase in volume. For a finite change from $V_1$ to
$V_2$ we add up all such slices:

$$ W = \int_{V_1}^{V_2} P\,dV $$

```figure caption="Work done by a gas is the area under the $P$–$V$ curve. The narrow strip has area $P\,dV$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
V = np.linspace(1.15, 5.2, 400); P = 8.0/V
ax.plot(V, P, color=ACCENT, lw=2.0, zorder=4)
m = (V>=1.5)&(V<=4.5)
ax.fill_between(V[m], 0, P[m], color=ACCENT, alpha=0.12, zorder=1)
s = np.linspace(2.95, 3.28, 20)
ax.fill_between(s, 0, 8.0/s, color=ACCENT, alpha=0.42, zorder=2)
ax.annotate(r'$P\,dV$', (3.15, 8/3.15), textcoords='offset points', xytext=(26,28),
            color=INK, fontsize=9.2,
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.0, mutation_scale=10))
for v,lab,off in [(1.5,'A',(-13,3)),(4.5,'B',(5,3))]:
    ax.plot([v],[8/v],'o',color=ACCENT,ms=5,zorder=5)
    ax.annotate(lab,(v,8/v),textcoords='offset points',xytext=off,color=INK,fontsize=10)
ax.annotate('', xy=(2.55,8/2.55+0.40), xytext=(1.70,8/1.70+0.40),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.3, mutation_scale=11))
ax.text(1.95,1.35,'$W = $ shaded area',color=INK,fontsize=9.2)
ax.set_xlabel('volume  $V$'); ax.set_ylabel('pressure  $P$')
ax.set_xlim(0.9,5.6); ax.set_ylim(0,7.4)
ax.set_xticks([1.5,4.5]); ax.set_xticklabels(['$V_1$','$V_2$']); ax.set_yticks([])
ax.spines[['top','right']].set_visible(False)
```

So **the work done by a gas equals the area under its $P$–$V$ curve**. Two
consequences follow immediately:

- If the gas expands, $dV > 0$ and $W$ is **positive** — the gas does work on the
  surroundings. If it is compressed, $W$ is **negative**.
- Because different curves joining the same two points enclose different areas,
  the work depends on the *path*, not merely on the end states.

## 4.3 Heat and work; Internal energy and First law of thermodynamics

**Heat** $Q$ is energy that crosses a boundary because of a temperature
difference. **Work** $W$ is energy that crosses because a force moves its point
of application. Both are energy *in transit*; neither is stored in the gas.

What is stored is the **internal energy** $U$ — the total kinetic energy of the
random molecular motion plus the potential energy of intermolecular forces. For
an ideal gas the intermolecular forces are zero, so

$$ U = \frac{f}{2}nRT $$

where $f$ is the number of degrees of freedom. The important consequence is that
**for an ideal gas $U$ depends only on temperature**: no temperature change means
no change in internal energy, whatever happens to $P$ and $V$.

Energy supplied as heat must either raise the internal energy or leave again as
work. That is the first law.

::: definition First law of thermodynamics
The heat supplied to a system is equal to the increase in its internal energy
plus the external work done by the system:

$$ Q = \Delta U + W, \qquad \text{or in differential form} \qquad dQ = dU + dW $$

It is the law of conservation of energy applied to a thermodynamic system, and it
asserts that internal energy is a state function.
:::

| Quantity | Positive when | Negative when |
|---|---|---|
| $Q$ | heat is **absorbed by** the system | heat is rejected by the system |
| $W$ | the gas **expands** (does work) | the gas is compressed |
| $\Delta U$ | temperature rises | temperature falls |

::: caution Sign conventions decide the marks
NEB uses $Q = \Delta U + W$ with $W$ as work done **by** the gas. Some books
write $\Delta U = Q + W$ with $W$ as work done **on** the gas. Both are correct
physics, but mixing them changes the sign of your answer. Pick the NEB form,
write it down first, and stick to it for the whole question.
:::

::: example Worked example 4.1
**Problem.** A gas at a constant pressure of $2.0\times10^{5}\ \text{Pa}$ expands
from $1.0\times10^{-3}\ \text{m}^{3}$ to $3.0\times10^{-3}\ \text{m}^{3}$ while
absorbing $500\ \text{J}$ of heat. Find the work done by the gas and the change
in its internal energy.

**Solution.** At constant pressure the area under the $P$–$V$ line is a rectangle:

$$ W = P\,\Delta V = (2.0\times10^{5})(3.0\times10^{-3} - 1.0\times10^{-3}) = 400\ \text{J} $$

From the first law, $\Delta U = Q - W = 500 - 400 = 100\ \text{J}$.

The internal energy rises by $100\ \text{J}$, so the gas also gets warmer.
:::

## 4.4 Thermodynamic processes: Adiabatic, isochoric, isothermal and isobaric

Four special paths are worth memorising because in each one the first law
collapses to a one-term equation.

| Process | Held constant | Condition | First law becomes | $P$–$V$ curve |
|---|---|---|---|---|
| Isochoric | volume | $dV = 0$ | $Q = \Delta U$ | vertical line |
| Isobaric | pressure | $dP = 0$ | $Q = \Delta U + P\Delta V$ | horizontal line |
| Isothermal | temperature | $\Delta U = 0$ | $Q = W$ | rectangular hyperbola |
| Adiabatic | no heat flow | $Q = 0$ | $\Delta U = -W$ | steeper hyperbola-like curve |

```figure caption="The four standard processes, all starting from the same state A. The adiabatic curve always falls more steeply than the isothermal."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
V0, P0, g = 2.0, 4.0, 1.4
V = np.linspace(2.0, 5.3, 300)
ax.plot(V, P0*V0/V, color=SERIES[0], lw=1.9, label='isothermal  $PV=$ const')
ax.plot(V, P0*(V0/V)**g, color=SERIES[1], lw=1.9, label=r'adiabatic  $PV^{\gamma}=$ const')
ax.plot([V0,5.3],[P0,P0], color=SERIES[2], lw=1.9, label='isobaric  $P=$ const')
ax.plot([V0,V0],[P0,0.55], color=SERIES[3], lw=1.9, label='isochoric  $V=$ const')
ax.plot([V0],[P0],'o',color=INK,ms=5.5,zorder=6)
ax.annotate('A',(V0,P0),textcoords='offset points',xytext=(-6,7),color=INK,fontsize=10)
ax.set_xlabel('volume  $V$'); ax.set_ylabel('pressure  $P$')
ax.set_xlim(1.5,6.4); ax.set_ylim(0,6.3)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='upper right', fontsize=8.0, handlelength=1.6)
```

A fifth case matters for engines: in a **cyclic process** the gas returns to its
starting state, so $\Delta U = 0$ and $Q = W$. The net work equals the area
enclosed by the loop — positive if the loop is traced clockwise, negative if
anticlockwise.

Two more named changes appear in NEB questions. A **free expansion** is the
expansion of a gas into a vacuum inside an insulated vessel: no heat enters
($Q=0$) and there is nothing to push against ($W=0$), so $\Delta U = 0$ and the
temperature of an ideal gas is unchanged. A **throttling process** is a similar
irreversible expansion through a porous plug.

## 4.5 Heat capacities of an ideal gas at constant pressure and volume and relation between them

The **molar heat capacity** of a gas is the heat needed to raise the temperature
of one mole by one kelvin. A gas has two of them, because the answer depends on
whether you let it expand.

```figure caption="Heating one mole through $dT$ at constant volume (left) and at constant pressure (right). The freely moving piston lets the gas do extra work $P\,dV$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axes = plt.subplots(1, 2, figsize=(5.0,3.2))
for ax, const in zip(axes, ['V', 'P']):
    ax.plot([0,0],[0,3.0], color=INK, lw=1.8)
    ax.plot([2,2],[0,3.0], color=INK, lw=1.8)
    ax.plot([0,2],[0,0],   color=INK, lw=1.8)
    top = 1.40
    ax.add_patch(Rectangle((0,0),2,top, fc='#e8f0f8', ec='none'))
    ax.add_patch(Rectangle((0,top),2,0.22, fc='#c3cad6', ec=INK, lw=1.0))
    ax.plot([1,1],[top+0.22,top+0.80], color=INK, lw=1.4)
    ax.text(1,0.62,'gas',ha='center',va='center',color=INK,fontsize=9)
    ax.annotate('', xy=(1,-0.06), xytext=(1,-0.95),
                arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.7,
                                shrinkA=0, shrinkB=0, mutation_scale=12))
    if const == 'V':
        for xa in (-0.26, 2.0):
            ax.add_patch(Rectangle((xa,top-0.04),0.26,0.30, fc=INK, ec='none'))
        ax.text(1,-1.28,r'$dQ = C_v\,dT$',ha='center',color='#d9534f',fontsize=9.2)
        ax.set_title('piston clamped:  $V$ constant', fontsize=9.2)
        ax.text(1,2.55,'$W=0$\n$dQ=dU$',ha='center',va='center',color=INK,fontsize=9)
    else:
        ax.add_patch(Rectangle((0,top+0.52),2,0.22, fc='none', ec=MUTED,
                               lw=1.0, ls=(0,(3,2))))
        ax.annotate('', xy=(1.55,top+0.62), xytext=(1.55,top+0.16),
                    arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.4,
                                    shrinkA=0, shrinkB=0, mutation_scale=10))
        ax.text(1.70,top+0.34,'$dx$',color='#2e8b57',fontsize=9)
        ax.add_patch(Rectangle((0.62,2.20),0.76,0.42, fc='#c3cad6', ec=INK, lw=1.0))
        ax.text(1,-1.28,r'$dQ = C_p\,dT$',ha='center',color='#d9534f',fontsize=9.2)
        ax.set_title('piston free:  $P$ constant', fontsize=9.2)
        ax.text(1,1.05+1.95,'$dQ=dU+P\\,dV$',ha='center',va='center',color=INK,fontsize=9)
    ax.set_xlim(-0.75,2.75); ax.set_ylim(-1.55,3.35)
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(wspace=0.05)
```

- $C_v$ is measured with the piston clamped. No work is done, so all the heat
  raises the internal energy: $dQ = dU = C_v\,dT$ for one mole.
- $C_p$ is measured with the piston free to move. The gas must also push the
  atmosphere back, so more heat is needed for the same rise in temperature.

Hence $C_p > C_v$ always. The exact difference is Mayer's relation.

::: derivation Mayer's relation, $C_p - C_v = R$
Take one mole of an ideal gas and heat it through $dT$.

**At constant volume.** $dV = 0$, so $dW = 0$ and the first law gives

$$ dU = C_v\,dT $$

Because $U$ depends only on $T$, this expression for $dU$ is true for *any*
process, not only the constant-volume one.

**At constant pressure.** Now $dQ = C_p\,dT$ and the gas does work $dW = P\,dV$,
so the first law reads

$$ C_p\,dT = C_v\,dT + P\,dV $$

**Eliminate $P\,dV$.** For one mole, $PV = RT$. Differentiating at constant $P$,

$$ P\,dV = R\,dT $$

Substituting,

$$ C_p\,dT = C_v\,dT + R\,dT \;\Longrightarrow\; \boxed{C_p - C_v = R} $$

In terms of specific heat capacities per kilogram, dividing by the molar mass $M$
gives $c_p - c_v = R/M$.
:::

The ratio $\gamma = C_p/C_v$ is fixed by the number of degrees of freedom $f$,
since $C_v = \frac{f}{2}R$:

| Gas | $f$ | $C_v$ (J mol⁻¹ K⁻¹) | $C_p$ (J mol⁻¹ K⁻¹) | $\gamma$ |
|---|---|---|---|---|
| Monatomic (He, Ar) | 3 | 12.47 | 20.79 | 1.67 |
| Diatomic (N₂, O₂, H₂) | 5 | 20.79 | 29.10 | 1.40 |
| Polyatomic (CO₂, NH₃) | 6 | 24.94 | 33.26 | 1.33 |

::: example Worked example 4.2
**Problem.** For nitrogen gas $\gamma = 1.40$ and the molar mass is
$28\ \text{g mol}^{-1}$. Calculate $C_v$, $C_p$ and the two specific heat
capacities per kilogram. Take $R = 8.314\ \text{J mol}^{-1}\text{K}^{-1}$.

**Solution.** From $C_p - C_v = R$ and $C_p = \gamma C_v$,

$$ \gamma C_v - C_v = R \;\Rightarrow\; C_v = \frac{R}{\gamma - 1}
= \frac{8.314}{0.40} = 20.79\ \text{J mol}^{-1}\text{K}^{-1} $$

$$ C_p = \gamma C_v = 1.40 \times 20.79 = 29.10\ \text{J mol}^{-1}\text{K}^{-1} $$

Dividing by $M = 0.028\ \text{kg mol}^{-1}$:

$$ c_v = \frac{20.79}{0.028} = 742\ \text{J kg}^{-1}\text{K}^{-1}, \qquad
c_p = \frac{29.10}{0.028} = 1039\ \text{J kg}^{-1}\text{K}^{-1} $$

Check: $c_p - c_v = 297 = R/M = 8.314/0.028$. Correct.
:::

## 4.6 Isothermal and Adiabatic processes for an ideal gas

### Isothermal process

The gas is kept at constant temperature, so $PV = $ constant (Boyle's law). In
practice this needs thin, highly conducting walls and a very slow change, so that
heat can flow in or out fast enough to hold $T$ fixed. Since $\Delta U = 0$, all
the heat absorbed reappears as work.

::: derivation Work done in an isothermal change
For $n$ moles, $P = nRT/V$ with $T$ constant. Then

$$ W = \int_{V_1}^{V_2} P\,dV = nRT \int_{V_1}^{V_2}\frac{dV}{V}
 = nRT\left[\ln V\right]_{V_1}^{V_2} $$

$$ W = nRT\ln\!\left(\frac{V_2}{V_1}\right) = 2.303\,nRT\log_{10}\!\left(\frac{V_2}{V_1}\right) $$

Since $P_1V_1 = P_2V_2$, this can also be written
$W = nRT\ln(P_1/P_2)$. Here $Q = W$ and $\Delta U = 0$.
:::

### Adiabatic process

No heat enters or leaves: $Q = 0$. This needs thick insulating walls, or a change
so fast that heat has no time to flow — the compression stroke of a diesel engine
and the propagation of a sound wave are both effectively adiabatic. The first law
gives $\Delta U = -W$: an expanding gas does work at the cost of its own internal
energy, and therefore **cools**.

::: derivation The adiabatic equation $PV^{\gamma} = $ constant
For one mole, $dU = C_v\,dT$ and $dW = P\,dV$. With $dQ = 0$ the first law gives

$$ C_v\,dT + P\,dV = 0 $$

From $PV = RT$, differentiating gives $P\,dV + V\,dP = R\,dT$, so
$dT = (P\,dV + V\,dP)/R$. Substituting,

$$ \frac{C_v}{R}(P\,dV + V\,dP) + P\,dV = 0 $$

Multiply through by $R$ and use $R = C_p - C_v$:

$$ C_v V\,dP + (C_v + C_p - C_v)P\,dV = 0
\;\Longrightarrow\; C_v V\,dP + C_p P\,dV = 0 $$

Divide by $C_v PV$ and write $\gamma = C_p/C_v$:

$$ \frac{dP}{P} + \gamma\,\frac{dV}{V} = 0 $$

Integrating, $\ln P + \gamma \ln V = $ constant, that is

$$ \boxed{PV^{\gamma} = \text{constant}} $$

Using $PV = nRT$ to eliminate $P$ or $V$ gives the two companion forms

$$ TV^{\gamma-1} = \text{constant}, \qquad P^{1-\gamma}T^{\gamma} = \text{constant} $$
:::

::: derivation Work done in an adiabatic change
Let $PV^{\gamma} = K$, so $P = KV^{-\gamma}$. Then

$$ W = \int_{V_1}^{V_2} K V^{-\gamma}\,dV
 = K\left[\frac{V^{1-\gamma}}{1-\gamma}\right]_{V_1}^{V_2}
 = \frac{K V_2^{1-\gamma} - K V_1^{1-\gamma}}{1-\gamma} $$

But $K = P_1V_1^{\gamma} = P_2V_2^{\gamma}$, so $KV_2^{1-\gamma} = P_2V_2$ and
$KV_1^{1-\gamma} = P_1V_1$. Hence

$$ W = \frac{P_2V_2 - P_1V_1}{1-\gamma} = \frac{P_1V_1 - P_2V_2}{\gamma - 1}
 = \frac{nR(T_1 - T_2)}{\gamma - 1} $$
:::

Differentiating the two curves shows why the adiabatic is steeper. For the
isothermal, $P\,dV + V\,dP = 0$ gives slope $dP/dV = -P/V$; for the adiabatic,
$dP/P = -\gamma\,dV/V$ gives slope $-\gamma P/V$. Since $\gamma > 1$, the
adiabatic slope is $\gamma$ times steeper at every point.

```figure caption="Expansion from A to the same final volume. The adiabatic path ends lower and encloses less area, so less work is done by the gas."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
V0, P0, g = 2.0, 4.0, 1.4
V = np.linspace(2.0, 5.0, 300)
Pi, Pa = P0*V0/V, P0*(V0/V)**g
ax.fill_between(V, 0, Pa, color=SERIES[1], alpha=0.22, label='adiabatic work')
ax.fill_between(V, Pa, Pi, color=SERIES[0], alpha=0.20, label='extra isothermal work')
ax.plot(V, Pi, color=SERIES[0], lw=1.9)
ax.plot(V, Pa, color=SERIES[1], lw=1.9)
ax.plot([V0],[P0],'o',color=INK,ms=5.5,zorder=6)
ax.annotate('A',(V0,P0),textcoords='offset points',xytext=(-6,6),color=INK,fontsize=10)
ax.annotate('isothermal',(4.4,P0*V0/4.4),textcoords='offset points',xytext=(6,4),
            color=SERIES[0],fontsize=9)
ax.annotate('adiabatic',(4.4,P0*(V0/4.4)**g),textcoords='offset points',xytext=(6,-10),
            color=SERIES[1],fontsize=9)
ax.set_xlabel('volume  $V$'); ax.set_ylabel('pressure  $P$')
ax.set_xlim(1.6,6.5); ax.set_ylim(0,5.0)
ax.set_xticks([2.0,5.0]); ax.set_xticklabels(['$V_1$','$V_2$']); ax.set_yticks([])
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='upper right', fontsize=8.0)
```

::: example Worked example 4.3
**Problem.** Two moles of an ideal gas at $300\ \text{K}$ expand isothermally to
three times the original volume. Find the work done by the gas and the heat
absorbed. ($\ln 3 = 1.0986$.)

**Solution.**

$$ W = nRT\ln\!\left(\frac{V_2}{V_1}\right)
 = 2 \times 8.314 \times 300 \times 1.0986 $$

$$ W = 4988.4 \times 1.0986 = 5.48\times10^{3}\ \text{J} $$

Because the temperature does not change, $\Delta U = 0$, so by the first law

$$ Q = \Delta U + W = 0 + 5.48\ \text{kJ} = 5.48\ \text{kJ absorbed} $$
:::

::: example Worked example 4.4
**Problem.** One mole of air ($\gamma = 1.40$) at $27\ ^{\circ}\text{C}$ is
compressed adiabatically to one-eighth of its volume. Find the final temperature
and the work done on the gas. ($8^{0.4} = 2.297$.)

**Solution.** $T_1 = 300\ \text{K}$ and $V_1/V_2 = 8$. Using
$TV^{\gamma-1} = $ constant,

$$ T_2 = T_1\left(\frac{V_1}{V_2}\right)^{\gamma-1} = 300 \times 8^{0.4}
 = 300 \times 2.297 = 689\ \text{K} $$

That is $416\ ^{\circ}\text{C}$ — the reason diesel fuel ignites without a spark.
The work done **by** the gas is

$$ W = \frac{nR(T_1-T_2)}{\gamma-1} = \frac{1 \times 8.314 \times (300-689)}{0.40}
 = -8.09\times10^{3}\ \text{J} $$

The negative sign means $8.09\ \text{kJ}$ of work is done **on** the gas; since
$Q = 0$, all of it becomes internal energy, $\Delta U = +8.09\ \text{kJ}$.
:::

## Chapter summary

- A system exchanges matter and energy with its surroundings across a boundary;
  open, closed and isolated systems differ in what may cross it. $P$, $V$, $T$
  and $U$ are state functions; $Q$ and $W$ are path functions.
- Work done by a gas is $W = \int P\,dV$, the area under the $P$–$V$ curve;
  positive for expansion, negative for compression.
- First law: $Q = \Delta U + W$, with $Q$ positive for heat absorbed and $W$
  positive for expansion. For an ideal gas $U$ depends only on $T$.
- Isochoric: $W=0$, $Q=\Delta U$. Isobaric: $W = P\Delta V$. Isothermal:
  $\Delta U = 0$, $Q = W$. Adiabatic: $Q = 0$, $\Delta U = -W$. Cyclic:
  $\Delta U = 0$, $Q = W = $ area of loop.
- Mayer's relation: $C_p - C_v = R$, so $C_v = R/(\gamma-1)$ and
  $C_p = \gamma R/(\gamma-1)$. Here $\gamma = 1.67$, $1.40$ and $1.33$ for mono-,
  di- and polyatomic gases.
- Isothermal: $PV = $ constant and $W = nRT\ln(V_2/V_1)$.
- Adiabatic: $PV^{\gamma} = $ constant, $TV^{\gamma-1} = $ constant, and
  $W = (P_1V_1 - P_2V_2)/(\gamma-1) = nR(T_1-T_2)/(\gamma-1)$.
- At any common point the adiabatic curve is $\gamma$ times steeper than the
  isothermal, so adiabatic expansion cools a gas.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. In an isothermal expansion of an ideal gas, the heat absorbed is <span class="marks">[1]</span>
   (a) zero (b) equal to the work done by the gas (c) equal to the rise in internal energy (d) equal to $C_v\Delta T$
2. For one mole of an ideal gas, $C_p - C_v$ is equal to <span class="marks">[1]</span>
   (a) $R$ (b) $\gamma R$ (c) $R/\gamma$ (d) zero
3. At the same point on an indicator diagram, the slope of the adiabatic curve compared with that of the isothermal is <span class="marks">[1]</span>
   (a) equal (b) $\gamma$ times greater in magnitude (c) $1/\gamma$ times (d) zero
4. In a complete cyclic process the change in internal energy of the gas is <span class="marks">[1]</span>
   (a) equal to $Q$ (b) equal to $W$ (c) zero (d) always negative
5. A gas expands freely into an evacuated insulated vessel. Its temperature <span class="marks">[1]</span>
   (a) rises (b) falls (c) stays the same (d) first rises, then falls

::: note Answers to Group A
**1.** (b) — $\Delta U = 0$ at constant $T$, so the first law gives $Q = W$.
**2.** (a) — Mayer's relation, $C_p - C_v = R$ for one mole.
**3.** (b) — slopes are $-P/V$ and $-\gamma P/V$ respectively.
**4.** (c) — $U$ is a state function and the gas returns to its initial state.
**5.** (c) — $Q = 0$ and $W = 0$, so $\Delta U = 0$; for an ideal gas that means $\Delta T = 0$.
:::

**Group B — Short answer (5 marks each)**

1. Define internal energy. State the first law of thermodynamics, write it in
   differential form, and explain the sign convention used for $Q$ and $W$. <span class="marks">[5]</span>
2. Derive the relation $C_p - C_v = R$ for one mole of an ideal gas, and explain
   physically why $C_p$ must be greater than $C_v$. <span class="marks">[5]</span>
3. A gas expands at a constant pressure of $1.5\times10^{5}\ \text{Pa}$ from
   $2.0\times10^{-3}\ \text{m}^{3}$ to $5.0\times10^{-3}\ \text{m}^{3}$, absorbing
   $800\ \text{J}$ of heat. Calculate the work done and the change in internal
   energy. <span class="marks">[5]</span>
4. One mole of oxygen at $27\ ^{\circ}\text{C}$ expands isothermally to four times
   its volume. Calculate the work done by the gas. ($\ln 4 = 1.386$) <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Internal energy is the total kinetic plus potential energy of the molecules
of a system, measured in its own frame; it is a state function. First law:
$Q = \Delta U + W$, i.e. $dQ = dU + dW$. $Q$ is positive when heat is absorbed,
$W$ is positive when the gas expands, $\Delta U$ is positive when the temperature
rises.

**2.** See the derivation in §4.5. Physically, at constant volume all the heat
goes into internal energy, whereas at constant pressure the gas must additionally
do work $P\,dV = R\,dT$ against the surroundings, so more heat is needed for the
same $dT$.

**3.** $W = P\Delta V = 1.5\times10^{5}\times(5.0-2.0)\times10^{-3} = 450\ \text{J}$.
Then $\Delta U = Q - W = 800 - 450 = 350\ \text{J}$.

**4.** $W = nRT\ln(V_2/V_1) = 1\times8.314\times300\times1.386 = 3.46\times10^{3}\ \text{J}$.
Since $\Delta U = 0$, the gas also absorbs $3.46\ \text{kJ}$ of heat.
:::

**Group C — Long answer (8 marks each)**

1. (a) Show that for a quasi-static change the work done by a gas is
   $W = \int P\,dV$, and hence that it equals the area under the indicator
   diagram. <span class="marks">[3]</span>
   (b) Derive the adiabatic relation $PV^{\gamma} = $ constant for an ideal gas,
   and obtain an expression for the work done during an adiabatic expansion. <span class="marks">[5]</span>
2. A cylinder contains $0.5\ \text{mol}$ of a diatomic ideal gas
   ($\gamma = 1.40$) at $300\ \text{K}$ and $1.0\times10^{5}\ \text{Pa}$.
   The gas is (i) heated at constant volume to $450\ \text{K}$, then (ii) expanded
   isothermally at $450\ \text{K}$ until its pressure returns to
   $1.0\times10^{5}\ \text{Pa}$. Calculate the heat supplied, the work done and
   the change in internal energy for each stage. ($\ln 1.5 = 0.4055$) <span class="marks">[8]</span>

::: note Answer to Group C question 2
**Stage (i) — isochoric.** $C_v = R/(\gamma-1) = 8.314/0.40 = 20.79\ \text{J mol}^{-1}\text{K}^{-1}$.

$$ W_1 = 0, \qquad \Delta U_1 = nC_v\Delta T = 0.5 \times 20.79 \times 150 = 1559\ \text{J} $$

so $Q_1 = \Delta U_1 = 1.56\times10^{3}\ \text{J}$. The pressure rises to
$P = 1.0\times10^{5}\times(450/300) = 1.5\times10^{5}\ \text{Pa}$.

**Stage (ii) — isothermal.** The pressure falls from $1.5\times10^{5}$ to
$1.0\times10^{5}\ \text{Pa}$, so $V_2/V_1 = P_1/P_2 = 1.5$.

$$ W_2 = nRT\ln 1.5 = 0.5 \times 8.314 \times 450 \times 0.4055 = 758\ \text{J} $$

$\Delta U_2 = 0$ and $Q_2 = W_2 = 758\ \text{J}$.

**Totals.** $Q = 1559 + 758 = 2.32\times10^{3}\ \text{J}$,
$W = 758\ \text{J}$, $\Delta U = 1559\ \text{J}$, which satisfies
$Q = \Delta U + W$.
:::
