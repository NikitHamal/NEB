---
subject: Physics
grade: 12
unit: 5
title: Second Law of Thermodynamics
hours: 6
area: Heat and Thermodynamics
---

The first law says energy is conserved, but not which way things go. It would be
perfectly happy if the water in a glass froze while the glass grew hot, or if a
stone cooled slightly and leapt into the air. Nature refuses. The second law
fixes the *direction* of every real process, and from it follow the limits on
every engine and every refrigerator ever built.

::: key What the exam wants from this unit
The two statements of the second law (Kelvin–Planck and Clausius), the heat
engine formula $\eta = 1 - Q_2/Q_1$, the Carnot cycle with its derivation of
$\eta = 1 - T_2/T_1$, and the coefficient of performance of a refrigerator.
Numerical questions almost always reduce to those four results.
:::

## 5.1 Thermodynamic systems and direction of thermodynamic processes

Every process you have watched runs one way only. Heat flows from hot tea to the
cold cup, never back. A gas released from a cylinder fills the room and never
gathers itself up again. A dropped ball bounces lower each time, but a warm floor
never cools slightly and launches a ball upwards. Each reverse process would
conserve energy perfectly, so the first law does not forbid it. Something else
does.

::: definition Reversible and irreversible processes
A **reversible process** is one that can be made to retrace its path exactly, so
that both the system *and* its surroundings return to their initial states,
leaving no trace anywhere. Any process that cannot is **irreversible**.
:::

A process is reversible only if it is **quasi-static** (carried out infinitely
slowly through a succession of equilibrium states) and free of all **dissipative
effects** — friction, viscosity, electrical resistance, or heat flow across a
finite temperature difference.

| Reversible (idealised) | Irreversible (real) |
|---|---|
| infinitely slow, always in equilibrium | finite rate, passes through non-equilibrium states |
| no friction, viscosity or turbulence | dissipative forces always present |
| Carnot cycle | free expansion; burning fuel; rubbing hands |

No real process is reversible. Reversibility is a limiting ideal, useful because
it fixes the best performance any real machine could approach.

## 5.2 Second law of thermodynamics

There are two classical statements. They look quite different but each can be
shown to imply the other.

::: definition Kelvin–Planck statement (engine statement)
It is impossible to construct a device that, operating in a cycle, produces **no
effect other than** the extraction of heat from a single reservoir and the
performance of an equivalent amount of work.
:::

::: definition Clausius statement (refrigerator statement)
It is impossible for any self-acting device, operating in a cycle, to transfer
heat from a colder body to a hotter body **without any external work** being done
on it.
:::

In plain terms: Kelvin–Planck forbids a 100 % efficient engine, Clausius forbids
a refrigerator that needs no power supply. The two are equivalent. Suppose a
device violated Clausius and moved $Q_2$ from sink to source for free. Couple it
to an ordinary engine that takes $Q_1$ from the source and rejects exactly $Q_2$.
The sink then gains and loses $Q_2$ each cycle, so it can be removed altogether,
leaving an engine that draws $Q_1 - Q_2$ from one reservoir and converts it
entirely into work — a violation of Kelvin–Planck.

::: caution "Heat cannot be fully converted into work" — read the small print
In an isothermal expansion of an ideal gas, $\Delta U = 0$, so $Q = W$: *all* the
heat does become work. The second law is not violated because the gas has been
left in an expanded state — the conversion was not the **sole** effect, and the
process cannot be repeated in a cycle. The word "cycle" in both statements is
doing real work; never drop it.
:::

## 5.3 Heat engines

::: definition Heat engine
A heat engine is a device that converts heat into mechanical work continuously,
by taking a working substance repeatedly around a cycle: it absorbs heat $Q_1$
from a **source** (hot reservoir) at $T_1$, converts part of it into work $W$,
and rejects the rest $Q_2$ to a **sink** (cold reservoir) at $T_2$.
:::

```figure caption="Energy flow in a heat engine. Of the heat $Q_1$ drawn from the source, only $W = Q_1 - Q_2$ leaves as work; the rest is dumped in the sink."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(4.6,3.4))
ax.add_patch(Rectangle((0.5,5.55),3.4,0.95, fc='#fae3e1', ec='#d9534f', lw=1.5))
ax.text(2.2,6.02,'SOURCE at $T_1$',ha='center',va='center',color=INK,fontsize=9.2)
ax.add_patch(Rectangle((0.5,0.90),3.4,0.95, fc='#dfeaf6', ec=ACCENT, lw=1.5))
ax.text(2.2,1.37,'SINK at $T_2$',ha='center',va='center',color=INK,fontsize=9.2)
ax.add_patch(Circle((2.2,3.70),0.80, fc='#eef1f5', ec=INK, lw=1.5))
ax.text(2.2,3.70,'engine',ha='center',va='center',color=INK,fontsize=9.0)
ax.annotate('', xy=(2.2,4.54), xytext=(2.2,5.53),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=2.4,
                            shrinkA=0, shrinkB=0, mutation_scale=15))
ax.text(2.05,5.04,'$Q_1$',ha='right',va='center',color='#d9534f',fontsize=10)
ax.annotate('', xy=(2.2,1.87), xytext=(2.2,2.86),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=2.0,
                            shrinkA=0, shrinkB=0, mutation_scale=14))
ax.text(2.05,2.37,'$Q_2$',ha='right',va='center',color=ACCENT,fontsize=10)
ax.annotate('', xy=(5.55,3.70), xytext=(3.02,3.70),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=2.2,
                            shrinkA=0, shrinkB=0, mutation_scale=15))
ax.text(4.28,3.92,'$W=Q_1-Q_2$',ha='center',va='bottom',color='#2e8b57',fontsize=9.6)
ax.set_xlim(0.2,6.2); ax.set_ylim(0.6,6.85)
ax.set_aspect('equal'); ax.axis('off')
```

Because the working substance returns to its initial state every cycle,
$\Delta U = 0$, and the first law gives

$$ W = Q_1 - Q_2 $$

The **thermal efficiency** is the fraction of the heat paid for that comes out as
useful work:

$$ \eta = \frac{W}{Q_1} = \frac{Q_1 - Q_2}{Q_1} = 1 - \frac{Q_2}{Q_1} $$

Efficiency equals 1 only if $Q_2 = 0$, exactly what Kelvin–Planck forbids.
**Every heat engine must have a sink**, so $\eta$ is always below 100 %.

Engines are classified by where the fuel burns: outside the working cylinder in
an **external combustion engine** (steam turbine), inside it in an **internal
combustion engine** (petrol, diesel), where the burning mixture is itself the
working substance.

::: example Worked example 5.1
**Problem.** A heat engine absorbs $2000\ \text{J}$ of heat per cycle from a
source at $500\ \text{K}$ and rejects $1400\ \text{J}$ to a sink at
$300\ \text{K}$. Find the work done per cycle and the efficiency. Is such an
engine possible?

**Solution.** Per cycle, $W = Q_1 - Q_2 = 2000 - 1400 = 600\ \text{J}$, so

$$ \eta = \frac{W}{Q_1} = \frac{600}{2000} = 0.30 = 30\ \% $$

The best possible efficiency between these temperatures is that of a Carnot
engine,

$$ \eta_{\max} = 1 - \frac{T_2}{T_1} = 1 - \frac{300}{500} = 0.40 = 40\ \% $$

Since $30\ \% < 40\ \%$, the engine does not violate the second law and is
possible (though not reversible).
:::

## 5.4 Internal combustion engines: Otto cycle, Diesel cycle, Carnot cycle

### The Otto cycle — the ideal petrol engine

The four-stroke petrol engine is modelled by the **Otto cycle** — two adiabatics
and two isochorics.

| Step | Process | What happens |
|---|---|---|
| 1 → 2 | adiabatic compression | piston compresses the fuel–air mixture; $T$ rises |
| 2 → 3 | isochoric heat input $Q_1$ | spark plug fires; pressure jumps at constant volume |
| 3 → 4 | adiabatic expansion | the power stroke; the gas drives the piston out |
| 4 → 1 | isochoric heat rejection $Q_2$ | exhaust valve opens; pressure drops |

With the **compression ratio** $r = V_1/V_2$, and $Q = nC_v\Delta T$ on both
isochoric steps, the ideal efficiency is

$$ \eta_{\text{Otto}} = 1 - \frac{1}{r^{\gamma-1}} $$

It depends only on $r$ and $\gamma$, not on how much fuel is burnt. Petrol
engines are limited to $r \approx 8$–$10$: above that the mixture ignites on its
own before the spark (knocking).

### The Diesel cycle

A diesel engine compresses **air alone**, so there is no knocking limit and $r$
can be $15$–$22$. The compressed air becomes hot enough (Worked example 4.4) to
ignite fuel sprayed in at the top of the stroke, so heat is added at roughly
constant **pressure**:

$$ \eta_{\text{Diesel}} = 1 - \frac{1}{\gamma\, r^{\gamma-1}}
\left[\frac{\rho^{\gamma}-1}{\rho-1}\right] $$

where $\rho = V_3/V_2$ is the cut-off ratio. For the same $r$ the diesel cycle is
slightly less efficient than the Otto cycle, but because $r$ can be made much
larger the real diesel engine wins comfortably.

```figure caption="Indicator diagrams of the Otto cycle (heat added at constant volume) and the Diesel cycle (heat added at constant pressure). Both reject heat at constant volume. Drawn schematically: real compression ratios are larger."
import numpy as np, matplotlib.pyplot as plt
g = 1.4
fig, axes = plt.subplots(1, 2, figsize=(5.1,2.8))

def adiab(Va, Pa, Vb, n=160):
    V = np.linspace(Va, Vb, n)
    return V, Pa*(Va/V)**g

def tag(ax, v, p, lab, off):
    ax.plot([v],[p],'o',color=INK,ms=3.8,zorder=6)
    ax.annotate(lab,(v,p),textcoords='offset points',xytext=off,color=INK,fontsize=9)

ax = axes[0]                                  # Otto
V1, V2, P1 = 3.0, 1.0, 1.0
P2 = P1*(V1/V2)**g; P3 = 3.5*P2; P4 = P3*(V2/V1)**g
ax.plot(*adiab(V1, P1, V2), color=INK, lw=1.8)
ax.plot([V2,V2],[P2,P3], color='#d9534f', lw=2.4)
ax.plot(*adiab(V2, P3, V1), color=INK, lw=1.8)
ax.plot([V1,V1],[P4,P1], color=ACCENT, lw=2.4)
tag(ax,V1,P1,'1',(5,-10)); tag(ax,V2,P2,'2',(-12,-4))
tag(ax,V2,P3,'3',(-12,-1)); tag(ax,V1,P4,'4',(5,2))
ax.text(V2+0.10,(P2+P3)/2,'$Q_1$',color='#d9534f',fontsize=9.2)
ax.text(V1-0.62,(P1+P4)/2,'$Q_2$',color=ACCENT,fontsize=9.2,ha='right')
ax.set_title('Otto cycle', fontsize=9.6)
ax.set_xlim(0.45,3.75); ax.set_ylim(0,P3*1.14)

ax = axes[1]                                  # Diesel
V1, V2, V3, P1 = 5.0, 1.0, 2.0, 1.0
P2 = P1*(V1/V2)**g; P4 = P2*(V3/V1)**g
ax.plot(*adiab(V1, P1, V2), color=INK, lw=1.8)
ax.plot([V2,V3],[P2,P2], color='#d9534f', lw=2.4)
ax.plot(*adiab(V3, P2, V1), color=INK, lw=1.8)
ax.plot([V1,V1],[P4,P1], color=ACCENT, lw=2.4)
tag(ax,V1,P1,'1',(5,-10)); tag(ax,V2,P2,'2',(-12,-2))
tag(ax,V3,P2,'3',(3,5)); tag(ax,V1,P4,'4',(5,2))
ax.text((V2+V3)/2,P2*1.09,'$Q_1$',color='#d9534f',fontsize=9.2,ha='center')
ax.text(V1-0.95,(P1+P4)/2,'$Q_2$',color=ACCENT,fontsize=9.2,ha='right')
ax.set_title('Diesel cycle', fontsize=9.6)
ax.set_xlim(0.4,6.1); ax.set_ylim(0,P2*1.30)

for ax in axes:
    ax.set_xlabel('$V$'); ax.set_xticks([]); ax.set_yticks([])
    ax.spines[['top','right']].set_visible(False)
axes[0].set_ylabel('$P$')
fig.subplots_adjust(wspace=0.18)
```

### The Carnot cycle

Sadi Carnot asked the deepest question: what is the *greatest* efficiency any
engine working between two given temperatures can have? His answer is an
imaginary, perfectly reversible engine running the cycle below.

```figure caption="The Carnot cycle: isothermal expansion A to B at $T_1$, adiabatic expansion B to C, isothermal compression C to D at $T_2$, adiabatic compression D to A. The enclosed area is the net work $W$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.2))
g, KH, KC = 2.2, 12.0, 6.0
A=(1.0,12.0); B=(2.2,5.4545); C=(3.9203,1.5305); D=(1.7818,3.3673)
ab = np.linspace(A[0],B[0],90);  Pab = KH/ab
bc = np.linspace(B[0],C[0],110); Pbc = B[1]*(B[0]/bc)**g
cd = np.linspace(C[0],D[0],90);  Pcd = KC/cd
da = np.linspace(D[0],A[0],110); Pda = A[1]*(A[0]/da)**g
ax.fill(np.concatenate([ab,bc,cd,da]), np.concatenate([Pab,Pbc,Pcd,Pda]),
        color=ACCENT, alpha=0.10)
ax.plot(ab,Pab,color='#d9534f',lw=2.2)
ax.plot(bc,Pbc,color=INK,lw=2.0)
ax.plot(cd,Pcd,color=ACCENT,lw=2.2)
ax.plot(da,Pda,color=INK,lw=2.0)
for (v,p),lab,off in [(A,'A',(-14,2)),(B,'B',(5,5)),(C,'C',(6,0)),(D,'D',(-15,-4))]:
    ax.plot([v],[p],'o',color=INK,ms=4.8,zorder=6)
    ax.annotate(lab,(v,p),textcoords='offset points',xytext=off,color=INK,fontsize=10)
for (v0,v1,K,col) in [(1.35,1.60,KH,'#d9534f'),(3.35,3.05,KC,ACCENT)]:
    ax.annotate('', xy=(v1,K/v1), xytext=(v0,K/v0),
                arrowprops=dict(arrowstyle='-|>',color=col,lw=1.4,mutation_scale=12))
ax.annotate('isothermal at $T_1$   ($Q_1$ in)',(1.75,KH/1.75),
            textcoords='offset points',xytext=(26,24),color='#d9534f',fontsize=8.6,
            arrowprops=dict(arrowstyle='-|>',color='#d9534f',lw=1.0,mutation_scale=9))
ax.annotate('isothermal at $T_2$   ($Q_2$ out)',(2.70,KC/2.70),
            textcoords='offset points',xytext=(12,-28),color=ACCENT,fontsize=8.6,
            arrowprops=dict(arrowstyle='-|>',color=ACCENT,lw=1.0,mutation_scale=9))
ax.annotate('adiabatic',(3.05,B[1]*(B[0]/3.05)**g),textcoords='offset points',
            xytext=(16,14),color=INK,fontsize=8.6,
            arrowprops=dict(arrowstyle='-|>',color=INK,lw=0.9,mutation_scale=9))
ax.annotate('adiabatic',(1.32,A[1]*(A[0]/1.32)**g),textcoords='offset points',
            xytext=(-56,-12),color=INK,fontsize=8.6,
            arrowprops=dict(arrowstyle='-|>',color=INK,lw=0.9,mutation_scale=9))
ax.text(1.94,4.30,'$W$',color=INK,fontsize=12,ha='center')
ax.set_xlabel('volume  $V$'); ax.set_ylabel('pressure  $P$')
ax.set_xlim(0.30,5.55); ax.set_ylim(0,14.2)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top','right']].set_visible(False)
```

::: derivation Efficiency of the Carnot engine
Take $n$ moles of an ideal gas round the cycle.

**A → B, isothermal expansion at $T_1$.** $\Delta U = 0$, so the heat absorbed is

$$ Q_1 = W_{AB} = nRT_1\ln\!\left(\frac{V_2}{V_1}\right) $$

**C → D, isothermal compression at $T_2$.** Similarly the heat rejected is

$$ Q_2 = nRT_2\ln\!\left(\frac{V_3}{V_4}\right) $$

**The two adiabatics.** Using $TV^{\gamma-1} = $ constant on B → C and on D → A,

$$ T_1V_2^{\gamma-1} = T_2V_3^{\gamma-1}, \qquad T_1V_1^{\gamma-1} = T_2V_4^{\gamma-1} $$

Dividing one by the other,

$$ \left(\frac{V_2}{V_1}\right)^{\gamma-1} = \left(\frac{V_3}{V_4}\right)^{\gamma-1}
\;\Longrightarrow\; \frac{V_2}{V_1} = \frac{V_3}{V_4} $$

**Result.** The two logarithms are therefore equal and cancel:

$$ \frac{Q_2}{Q_1} = \frac{T_2}{T_1}
\;\Longrightarrow\; \boxed{\eta = 1 - \frac{T_2}{T_1}} $$
:::

Notice that the result contains no property of the working substance — air,
steam or helium give the same answer — and that it reaches 1 only if
$T_2 = 0\ \text{K}$, which is unattainable.

::: definition Carnot's theorem
(a) No engine working between two given temperatures can be more efficient than a
reversible engine working between the same two temperatures.
(b) All reversible engines working between the same two temperatures have the
same efficiency, whatever the working substance.
:::

::: example Worked example 5.2
**Problem.** A Carnot engine operates between a source at $227\ ^{\circ}\text{C}$
and a sink at $27\ ^{\circ}\text{C}$, absorbing $6000\ \text{J}$ per cycle.
Find its efficiency, the work done and the heat rejected.

**Solution.** Convert to kelvin: $T_1 = 227 + 273 = 500\ \text{K}$,
$T_2 = 27 + 273 = 300\ \text{K}$.

$$ \eta = 1 - \frac{T_2}{T_1} = 1 - \frac{300}{500} = 0.40 = 40\ \% $$

$$ W = \eta Q_1 = 0.40 \times 6000 = 2400\ \text{J} $$

$$ Q_2 = Q_1 - W = 6000 - 2400 = 3600\ \text{J} $$

Check: $Q_2/Q_1 = 3600/6000 = 0.60 = T_2/T_1$. Consistent.
:::

::: example Worked example 5.3
**Problem.** A petrol engine working on the Otto cycle has a compression ratio of
$8$. Taking $\gamma = 1.40$, find its ideal efficiency. What would it become if
the compression ratio were raised to $10$? ($8^{0.4} = 2.297$, $10^{0.4} = 2.512$.)

**Solution.**

$$ \eta = 1 - \frac{1}{r^{\gamma-1}} = 1 - \frac{1}{8^{0.4}}
 = 1 - \frac{1}{2.297} = 1 - 0.435 = 0.565 = 56.5\ \% $$

For $r = 10$,

$$ \eta = 1 - \frac{1}{2.512} = 1 - 0.398 = 0.602 = 60.2\ \% $$

Real petrol engines reach only $25$–$30\ \%$, because of friction, heat loss and
incomplete combustion.
:::

## 5.5 Refrigerator

A refrigerator is a heat engine run backwards. A compressor supplies work $W$;
the machine extracts heat $Q_2$ from the cold interior and dumps $Q_1 = Q_2 + W$
into the kitchen through the coils at the back. The Clausius statement is exactly
the assertion that $W$ cannot be zero.

```figure caption="Energy flow in a refrigerator. Work $W$ is supplied so that heat $Q_2$ can be pumped from the cold interior into the warmer surroundings."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(4.6,3.4))
ax.add_patch(Rectangle((0.5,5.55),3.4,0.95, fc='#fae3e1', ec='#d9534f', lw=1.5))
ax.text(2.2,6.02,'SURROUNDINGS at $T_1$',ha='center',va='center',color=INK,fontsize=8.6)
ax.add_patch(Rectangle((0.5,0.90),3.4,0.95, fc='#dfeaf6', ec=ACCENT, lw=1.5))
ax.text(2.2,1.37,'COLD SPACE at $T_2$',ha='center',va='center',color=INK,fontsize=8.6)
ax.add_patch(Circle((2.2,3.70),0.80, fc='#eef1f5', ec=INK, lw=1.5))
ax.text(2.2,3.70,'fridge',ha='center',va='center',color=INK,fontsize=9.0)
ax.annotate('', xy=(2.2,5.53), xytext=(2.2,4.54),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=2.4,
                            shrinkA=0, shrinkB=0, mutation_scale=15))
ax.text(2.05,5.04,'$Q_1=Q_2+W$',ha='right',va='center',color='#d9534f',fontsize=9.2)
ax.annotate('', xy=(2.2,2.86), xytext=(2.2,1.87),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=2.0,
                            shrinkA=0, shrinkB=0, mutation_scale=14))
ax.text(2.05,2.37,'$Q_2$',ha='right',va='center',color=ACCENT,fontsize=10)
ax.annotate('', xy=(3.02,3.70), xytext=(5.35,3.70),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=2.2,
                            shrinkA=0, shrinkB=0, mutation_scale=15))
ax.text(4.20,3.92,'$W$ (compressor)',ha='center',va='bottom',color='#2e8b57',fontsize=9.2)
ax.set_xlim(0.2,6.2); ax.set_ylim(0.6,6.85)
ax.set_aspect('equal'); ax.axis('off')
```

The useful output is the heat removed from the cold space and the cost is the
work supplied, so the performance figure is

$$ \beta = \frac{Q_2}{W} = \frac{Q_2}{Q_1 - Q_2} $$

called the **coefficient of performance** (COP). It is not an efficiency, because
it is usually greater than 1: a good refrigerator moves four or five joules of
heat per joule of electrical work. For a reversible (Carnot) refrigerator
$Q_2/Q_1 = T_2/T_1$, so

$$ \beta_{\max} = \frac{T_2}{T_1 - T_2} $$

Comparing with the engine formula gives $\beta = (1-\eta)/\eta$. Note that
$\beta$ falls as the temperature difference grows: a deep freezer costs far more
to run than a chiller.

In a domestic refrigerator the working substance is a volatile refrigerant. The
**compressor** compresses its vapour, which condenses in the **condenser** coils
at the back, giving out $Q_1$ to the kitchen; the liquid then passes through a
**throttle valve**, where it expands and cools sharply, and evaporates in the
**evaporator** coils inside the cabinet, absorbing $Q_2$ from the food. A **heat
pump** is the same machine used for its hot end, with COP $= Q_1/W$.

::: example Worked example 5.4
**Problem.** A refrigerator maintains its freezer at $-13\ ^{\circ}\text{C}$ in a
kitchen at $27\ ^{\circ}\text{C}$. Assuming ideal (reversible) operation, find its
coefficient of performance, the work needed to remove $1300\ \text{J}$ of heat,
and the heat delivered to the kitchen.

**Solution.** $T_2 = -13 + 273 = 260\ \text{K}$, $T_1 = 27 + 273 = 300\ \text{K}$.

$$ \beta = \frac{T_2}{T_1 - T_2} = \frac{260}{300-260} = \frac{260}{40} = 6.5 $$

$$ W = \frac{Q_2}{\beta} = \frac{1300}{6.5} = 200\ \text{J} $$

$$ Q_1 = Q_2 + W = 1300 + 200 = 1500\ \text{J} $$

So leaving the fridge door open warms the room by $200\ \text{J}$ for every
$1300\ \text{J}$ moved, rather than cooling it.
:::

## 5.6 Entropy and disorder (introduction only)

Clausius found a state function that turns the second law into an equation rather
than a prohibition. For a reversible transfer of heat $dQ$ at absolute
temperature $T$, the change in **entropy** is

$$ dS = \frac{dQ_{\text{rev}}}{T}, \qquad
\Delta S = \int \frac{dQ_{\text{rev}}}{T} $$

Its SI unit is J K⁻¹. Entropy is a **state function**: round any cycle it returns
to its starting value. Check this on the Carnot cycle — the gas gains $Q_1/T_1$
and loses $Q_2/T_2$, and these are equal since $Q_2/Q_1 = T_2/T_1$.

For a change at constant temperature (melting, boiling) the integral is trivial:

$$ \Delta S = \frac{Q}{T} = \frac{mL}{T} $$

::: key The second law as an inequality
In any process, the total entropy of the system together with its surroundings
never decreases:

$$ \Delta S_{\text{universe}} \ge 0 $$

The equality holds only for a reversible process. Every real process increases
the entropy of the universe.
:::

Entropy measures **disorder** — more exactly, the number of microscopic
arrangements of the molecules that look the same from outside. Ice has its
molecules locked in a lattice (low entropy), water has them tumbling freely
(higher), steam higher still. Heat flowing from hot to cold raises the total
entropy, which is why it happens; the reverse would lower it, which is why it
does not.

::: example Worked example 5.5
**Problem.** One kilogram of ice at $0\ ^{\circ}\text{C}$ melts completely into
water at $0\ ^{\circ}\text{C}$. Find the change in entropy of the ice. Take the
latent heat of fusion as $3.34\times10^{5}\ \text{J kg}^{-1}$.

**Solution.** Melting happens at a constant temperature of
$T = 0 + 273 = 273\ \text{K}$, and the heat absorbed is

$$ Q = mL = 1 \times 3.34\times10^{5} = 3.34\times10^{5}\ \text{J} $$

$$ \Delta S = \frac{Q}{T} = \frac{3.34\times10^{5}}{273} = 1.22\times10^{3}\ \text{J K}^{-1} $$

The entropy increases, as it must: liquid water is more disordered than ice.
:::

## Chapter summary

- Real processes run one way only. A reversible process is quasi-static and free
  of all dissipative effects; no real process is reversible.
- Kelvin–Planck: no cyclic device can convert heat from a single reservoir
  entirely into work. Clausius: no self-acting cyclic device can move heat from a
  colder to a hotter body. The two statements are equivalent.
- Heat engine: $W = Q_1 - Q_2$ and $\eta = W/Q_1 = 1 - Q_2/Q_1$. A sink is
  compulsory, so $\eta < 1$ always.
- Otto cycle (petrol): two adiabatics and two isochorics,
  $\eta = 1 - r^{-(\gamma-1)}$. Diesel cycle: heat added isobarically, allowing a
  much larger $r$.
- Carnot cycle: two isothermals and two adiabatics, all reversible, with
  $\eta = 1 - T_2/T_1$ — the maximum possible for the given temperatures, and
  independent of the working substance (Carnot's theorem).
- Refrigerator: $Q_1 = Q_2 + W$, $\beta = Q_2/W = Q_2/(Q_1-Q_2)$, and for the
  ideal case $\beta_{\max} = T_2/(T_1-T_2) = (1-\eta)/\eta$.
- Entropy $dS = dQ_{\text{rev}}/T$ is a state function measured in J K⁻¹, and for
  an isothermal change $\Delta S = Q/T$. The second law states
  $\Delta S_{\text{universe}} \ge 0$; entropy is a measure of disorder.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The efficiency of a Carnot engine working between $27\ ^{\circ}\text{C}$ and $327\ ^{\circ}\text{C}$ is <span class="marks">[1]</span>
   (a) 50 % (b) 25 % (c) 75 % (d) 92 %
2. The Clausius statement of the second law forbids <span class="marks">[1]</span>
   (a) an engine of 100 % efficiency (b) a self-acting device that moves heat from a cold body to a hot body (c) the conversion of work into heat (d) adiabatic expansion
3. In the ideal Otto cycle, heat is supplied at constant <span class="marks">[1]</span>
   (a) pressure (b) volume (c) temperature (d) entropy
4. The maximum coefficient of performance of a refrigerator working between $250\ \text{K}$ and $300\ \text{K}$ is <span class="marks">[1]</span>
   (a) 5 (b) 6 (c) 0.2 (d) 1.2
5. In every real (irreversible) process, the entropy of the universe <span class="marks">[1]</span>
   (a) decreases (b) remains constant (c) increases (d) becomes zero

::: note Answers to Group A
**1.** (a) — $T_1 = 600\ \text{K}$, $T_2 = 300\ \text{K}$, so $\eta = 1 - 300/600 = 0.5$.
**2.** (b) — the Clausius prohibition; (a) is the Kelvin–Planck one.
**3.** (b) — the spark fires while the piston is at the top, so the volume is fixed.
**4.** (a) — $\beta_{\max} = T_2/(T_1-T_2) = 250/50 = 5$.
**5.** (c) — $\Delta S_{\text{universe}} > 0$ for irreversible changes.
:::

**Group B — Short answer (5 marks each)**

1. State the Kelvin–Planck and Clausius statements of the second law, and show
   that a violation of one implies a violation of the other. <span class="marks">[5]</span>
2. What is a heat engine? Draw its energy-flow diagram, derive
   $\eta = 1 - Q_2/Q_1$, and explain why $\eta$ can never be 100 %. <span class="marks">[5]</span>
3. A Carnot engine has an efficiency of $40\ \%$ when its sink is at
   $27\ ^{\circ}\text{C}$. Find the temperature of the source. To what temperature
   must the source be raised to obtain an efficiency of $50\ \%$, the sink being
   unchanged? <span class="marks">[5]</span>
4. Define the coefficient of performance of a refrigerator. A refrigerator with a
   COP of $5$ extracts $600\ \text{J}$ of heat per cycle from the cold chamber.
   Find the work done per cycle and the heat rejected to the surroundings. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Statements and the equivalence argument as in §5.2.

**2.** $\Delta U = 0$ over a cycle gives $W = Q_1 - Q_2$, hence
$\eta = W/Q_1 = 1 - Q_2/Q_1$. Here $\eta = 1$ needs $Q_2 = 0$, an engine with no
sink, which Kelvin–Planck forbids.

**3.** $\eta = 1 - T_2/T_1$ gives $0.40 = 1 - 300/T_1$, so
$T_1 = 300/0.60 = 500\ \text{K}$ ($227\ ^{\circ}\text{C}$). For $\eta = 0.50$,
$T_1 = 300/0.50 = 600\ \text{K}$ ($327\ ^{\circ}\text{C}$) — a rise of
$100\ \text{K}$.

**4.** COP is the ratio of the heat extracted from the cold body to the work
supplied, $\beta = Q_2/W$. Here $W = Q_2/\beta = 600/5 = 120\ \text{J}$ and
$Q_1 = Q_2 + W = 600 + 120 = 720\ \text{J}$.
:::

**Group C — Long answer (8 marks each)**

1. Describe the Carnot cycle with the help of an indicator diagram, naming the
   four processes, and derive the expression $\eta = 1 - T_2/T_1$ for its
   efficiency. State Carnot's theorem. <span class="marks">[8]</span>
2. A petrol engine working on the ideal Otto cycle has a compression ratio of
   $9$ and uses a gas with $\gamma = 1.40$. ($9^{0.4} = 2.408$)
   (a) Calculate its ideal efficiency. <span class="marks">[3]</span>
   (b) If it absorbs $2000\ \text{J}$ of heat per cycle, find the work output and
   the heat rejected. <span class="marks">[3]</span>
   (c) A Carnot engine works between the same extreme temperatures,
   $1500\ \text{K}$ and $300\ \text{K}$. Compare the two efficiencies and comment. <span class="marks">[2]</span>

::: note Answer to Group C question 2
(a) $\eta = 1 - 1/r^{\gamma-1} = 1 - 1/9^{0.4} = 1 - 1/2.408 = 1 - 0.415 = 0.585$,
that is $58.5\ \%$.

(b) $W = \eta Q_1 = 0.585 \times 2000 = 1.17\times10^{3}\ \text{J}$, and
$Q_2 = Q_1 - W = 2000 - 1170 = 830\ \text{J}$.

(c) $\eta_{\text{Carnot}} = 1 - 300/1500 = 0.80 = 80\ \%$. The Otto cycle falls
well short because it absorbs and rejects heat over a *range* of temperatures
rather than at the two extremes.
:::
