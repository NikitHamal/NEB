---
subject: Physics
grade: CEE
unit: 21
title: Semiconductors and Logic Gates
hours: 2
area: Modern Physics
---

This is the chapter behind every phone charger, solar panel and calculator in Nepal.
Modern Physics carries **12 of the 50 Physics questions** (official MEC weightage),
and we estimate about **2** come from here. The paper asks three kinds of question:
one fact about bands or doping (which carrier is in the majority, what a donor
does), one about the diode (which way it conducts, what the reverse current is, what
a rectifier puts out), and one about a gate (read a truth table, identify a gate from
its output, or know which gates are universal). Almost nothing here needs a long
calculation — but the definitions must be exact, because the distractors are built
from half-remembered versions of them.

::: key What the paper asks from this chapter
- Band picture: a full valence band, an empty conduction band, and the gap between them; $E_g\\approx0$ for a metal, about 1 eV for a semiconductor, more than 3 eV for an insulator.
- Intrinsic: $n_e=n_h=n_i$, conduction by electron–hole pairs, resistance **falls** as temperature rises.
- Extrinsic: pentavalent donor gives n-type (electrons majority), trivalent acceptor gives p-type (holes majority); the donor level sits just below the conduction band, the acceptor level just above the valence band.
- Mass action law $n_en_h=n_i^2$; charge neutrality; conductivity $\sigma=e(n_e\mu_e+n_h\mu_h)$.
- The p–n junction: diffusion, recombination, the depletion layer of immobile ions, the barrier potential (Si 0.7 V, Ge 0.3 V).
- Forward bias narrows the depletion layer and lowers the barrier; reverse bias widens it and raises it. Reverse current is **minority-carrier drift**, small but not zero.
- Rectifiers: one diode for half-wave, two (centre tap) or four (bridge) for full-wave; output frequency $f$ or $2f$; average $V_0/\pi$ or $2V_0/\pi$.
- Gates AND, OR, NOT, NAND, NOR with truth tables; NAND and NOR are **universal**; XOR is not.
:::

## 21.1 Energy bands in metals, semiconductors and insulators; intrinsic and extrinsic semiconductors

### 21.1.1 From atomic levels to bands

An isolated atom has sharp energy levels. In a solid, a vast number of atoms are
packed within a few nanometres, and the Pauli exclusion principle forbids two
electrons from sharing the same state. Each atomic level therefore splits into a
**band** of closely spaced levels — so closely spaced that the electron sees an
almost continuous range of allowed energies.

Two bands matter:

- the **valence band**, formed from the outer electrons that are bound to atoms;
- the **conduction band**, the next band up, in which electrons are free to move
  through the crystal and carry current.

Between them lies the **forbidden energy gap** $E_g$, where no electron state exists.
The size of that gap decides what the material is.

```figure caption="The band picture of the three classes of solid. A metal has a partly filled conduction band (or overlapping bands); a semiconductor has a small gap of about 1 eV; an insulator has a gap of several eV, so almost no electron can cross it at room temperature."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.1))
panels = [(1.5,'metal',0.0),(4.5,'semiconductor',0.55),(7.5,'insulator',1.45)]
for xc, name, gap in panels:
    ax.add_patch(plt.Rectangle((xc-0.85,0.60),1.7,0.90, fc='#C9D8EC', ec=ACCENT, lw=1.0))
    ax.add_patch(plt.Rectangle((xc-0.85,1.50+gap),1.7,0.90, fc='#EDF2F9', ec=ACCENT, lw=1.0, ls='--'))
    ax.text(xc,2.55+gap,name,ha='center',va='bottom',fontsize=9.5,color=INK)
    ax.text(xc,1.05,'full',ha='center',va='center',fontsize=8,color=INK)
    lab = 'partly full' if gap == 0 else 'empty'
    ax.text(xc,1.95+gap,lab,ha='center',va='center',fontsize=8,color=INK)
ax.text(0.14,1.05,'valence band',rotation=90,ha='center',va='center',fontsize=8,color=INK)
ax.text(0.14,3.35,'conduction band',rotation=90,ha='center',va='center',fontsize=8,color=INK)
ax.annotate('', xy=(3.42,1.50), xytext=(3.42,2.05),
            arrowprops=dict(arrowstyle='<|-|>',color='#A8271F',lw=0.9,mutation_scale=7))
ax.text(3.32,1.78,'$E_g$',ha='right',va='center',fontsize=9,color='#A8271F')
ax.annotate('', xy=(6.42,1.50), xytext=(6.42,2.95),
            arrowprops=dict(arrowstyle='<|-|>',color='#A8271F',lw=0.9,mutation_scale=7))
ax.text(6.32,2.22,'$E_g$',ha='right',va='center',fontsize=9,color='#A8271F')
ax.text(1.5,0.28,'$E_g\\approx0$',ha='center',fontsize=8.5,color=INK)
ax.text(4.5,0.28,'$E_g\\approx1$ eV',ha='center',fontsize=8.5,color=INK)
ax.text(7.5,0.28,'$E_g>3$ eV',ha='center',fontsize=8.5,color=INK)
ax.set_xlim(0.0,9.0); ax.set_ylim(0.0,4.35)
ax.axis('off')
```

| Solid | $E_g$ | Conduction at room temperature | Resistance when heated |
|---|---|---|---|
| Metal (Cu, Ag, Al) | zero — bands overlap or the top band is partly full | abundant free electrons | **increases** (lattice vibrations scatter them) |
| Semiconductor (Ge, Si) | 0.7 eV (Ge), 1.1 eV (Si) | small but useful; a few electrons per $10^{9}$ atoms are free | **decreases** (many more carriers are freed) |
| Insulator (diamond, glass) | about 5.5 eV (diamond), more than 3 eV generally | effectively none | stays negligible until breakdown |

The different sign of the temperature coefficient is the fastest way to tell a
semiconductor from a metal in an exam question: a metal gets worse when hot, a
semiconductor gets better.

### 21.1.2 Intrinsic semiconductors

A **pure** semiconductor is called **intrinsic**. At absolute zero every electron
sits in the valence band, the conduction band is empty, and the crystal is an
insulator. At room temperature thermal energy frees a small number of electrons,
each leaving behind a vacancy in a covalent bond. That vacancy behaves as a
**positive** carrier called a **hole**: an electron from a neighbouring bond can move
into it, so the hole appears to move the other way.

In a pure crystal every freed electron leaves one hole, so

$$ n_e=n_h=n_i $$

where $n_i$ is the **intrinsic carrier concentration**. For silicon at 300 K it is
about $1.5\times10^{16}$ m⁻³ — tiny compared with the $5\times10^{28}$ atoms per cubic
metre, which is why pure silicon is a poor conductor.

Two consequences worth memorising:

- conduction in an intrinsic semiconductor is **by electrons and holes together**,
  and the two currents add;
- as the temperature rises, $n_i$ rises very rapidly (roughly doubling every 10 K
  near room temperature), so the resistance **falls**.

### 21.1.3 Extrinsic semiconductors: doping

A controlled tiny addition of an impurity — about one atom in $10^{6}$ — raises the
carrier concentration enormously. This is **doping**, and the result is an
**extrinsic** semiconductor.

**n-type.** Add a **pentavalent** atom (phosphorus, arsenic, antimony) to silicon.
Four of its five outer electrons form covalent bonds; the fifth is loosely bound and
needs only about 0.01–0.05 eV to enter the conduction band. The impurity **donates**
an electron, so it is a **donor**, and the crystal becomes **n-type**: electrons are
the **majority carriers** and holes the **minority carriers**. The donor level lies
just below the conduction band. The crystal stays electrically neutral — every donor
also leaves a fixed positive ion behind.

**p-type.** Add a **trivalent** atom (boron, aluminium, gallium, indium). It has one
bond too few, so it **accepts** an electron from a neighbouring bond, creating a hole.
The impurity is an **acceptor**, and the crystal becomes **p-type**: holes are the
majority carriers, electrons the minority. The acceptor level lies just above the
valence band.

| | n-type | p-type |
|---|---|---|
| Dopant | pentavalent (P, As, Sb) | trivalent (B, Al, Ga, In) |
| Impurity called | donor | acceptor |
| Majority carrier | electrons | holes |
| Minority carrier | holes | electrons |
| Impurity level | just below the conduction band | just above the valence band |
| Net charge of the crystal | zero | zero |

::: caution Doping does not charge the crystal
A doped crystal is **neutral**. Each donor atom gives a free electron *and* leaves a
positive ion; each acceptor takes an electron *and* leaves a negative ion. The two
charges cancel. Students often write "n-type is negatively charged" — that is wrong,
and it is a standard distractor.
:::

### 21.1.4 Mass action law and conductivity

In thermal equilibrium the product of the two carrier concentrations is fixed by the
temperature and the material:

$$ n_en_h=n_i^2 $$

This is the **mass action law**. It says that if doping increases one kind of
carrier, the other must fall by the same factor. Dope silicon ($n_i=1.5\times10^{16}$
m⁻³) so that $n_e=4.5\times10^{22}$ m⁻³, and the hole concentration drops to

$$ n_h=\frac{(1.5\times10^{16})^2}{4.5\times10^{22}}=5.0\times10^{9}\ \text{m}^{-3} $$

The conductivity of a semiconductor is the sum of the two contributions:

$$ \sigma=e(n_e\mu_e+n_h\mu_h), \qquad \rho=\frac{1}{\sigma} $$

where $\mu_e$ and $\mu_h$ are the mobilities (m² V⁻¹ s⁻¹). In an n-type material the
first term dominates; in a p-type material the second does. Because electrons move
more easily than holes, $\mu_e>\mu_h$ in both silicon and germanium.

::: example Worked example 21.1 — conductivity of a doped crystal
**Problem.** A silicon sample is doped so that $n_e=5.0\times10^{22}$ m⁻³. Taking
$\mu_e=0.05$ m² V⁻¹ s⁻¹, find its conductivity and resistivity. (The hole
contribution is negligible here.)

**Solution.** $\sigma=en_e\mu_e=(1.6\times10^{-19})(5.0\times10^{22})(0.05)
=400$ S m⁻¹.

$\rho=1/\sigma=1/400=2.5\times10^{-3}$ Ω m.

**Check.** Intrinsic silicon has $\sigma$ of order $10^{-3}$ S m⁻¹, so doping has
raised the conductivity by about six powers of ten. That is why a doped crystal is
useful and a pure one is not.
:::

## 21.2 The p–n junction diode, its biasing and its use as a rectifier

### 21.2.1 How the junction forms

Join a p-type and an n-type crystal. At the boundary, holes diffuse from p to n and
electrons diffuse from n to p, because each side has far more of its own carrier than
the other. The carriers that cross **recombine**, so a thin layer on each side is left
with no free carriers but with the fixed ions the dopants left behind: negative
acceptor ions on the p side, positive donor ions on the n side.

This is the **depletion region** (or depletion layer). It contains a built-in electric
field pointing from the positive ions to the negative ions — that is, from n to p —
and a corresponding **potential barrier** that opposes further diffusion. Equilibrium
is reached when the drift of the few remaining carriers exactly balances the
diffusion. The barrier height is about **0.7 V for silicon** and **0.3 V for
germanium**.

### 21.2.2 Forward and reverse bias

**Forward bias.** Connect the p side to the positive terminal and the n side to the
negative terminal. The applied field opposes the built-in field, so the barrier is
**lowered**, the depletion region **narrows**, and majority carriers are pushed
towards the junction in large numbers. Once the applied voltage exceeds the barrier,
the current rises very steeply. The diode behaves like a closed switch with a small
resistance.

**Reverse bias.** Connect the p side to the negative terminal and the n side to the
positive terminal. The applied field adds to the built-in field, the barrier is
**raised**, and the depletion region **widens**. Majority carriers are pulled away
from the junction and cannot cross. Only the **minority carriers** — the few holes on
the n side and electrons on the p side — are swept across by the field, giving a tiny
**reverse saturation current**. It is of order microamperes in germanium and
nanoamperes in silicon, and it hardly changes with the applied voltage because it
depends on how many minority carriers exist, not on how hard they are pushed.

```figure caption="The same junction under the two biases. Forward bias narrows the depletion layer and lowers the barrier, so the diode conducts; reverse bias widens it and raises the barrier, leaving only a small minority-carrier current."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1,2,figsize=(5.1,2.9))
for ax,(w,top,bot) in zip(axes,[(1.4,'p to +, n to −','barrier lowered'),
                                  (2.6,'p to −, n to +','barrier raised')]):
    ax.add_patch(plt.Rectangle((0.3,1.3),5.0-w/2-0.3,2.5, fc='#F6DEDA', ec='#A8271F', lw=1.0))
    ax.add_patch(plt.Rectangle((5.0+w/2,1.3),9.7-(5.0+w/2),2.5, fc='#DCE6F4', ec=ACCENT, lw=1.0))
    ax.add_patch(plt.Rectangle((5.0-w/2,1.3),w,2.5, fc='#F2F2F2', ec=MUTED, lw=0.8, ls='--'))
    ax.text(2.3,3.95,'p',ha='center',fontsize=11,color='#A8271F')
    ax.text(7.7,3.95,'n',ha='center',fontsize=11,color=ACCENT)
    ax.text(5.0,0.55,'depletion layer',ha='center',fontsize=8,color=MUTED)
    ax.annotate('', xy=(5.0,1.22), xytext=(5.0,0.75),
                arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=0.8,mutation_scale=7))
    ax.text(5.0,5.05,top,ha='center',fontsize=8.2,color=INK)
    ax.text(5.0,4.45,bot,ha='center',fontsize=8.2,color=INK,style='italic')
    ax.set_xlim(0,10); ax.set_ylim(0.3,5.4); ax.axis('off')
axes[0].text(4.55,2.55,'−',ha='center',va='center',fontsize=12,color=INK)
axes[0].text(5.45,2.55,'+',ha='center',va='center',fontsize=12,color=INK)
axes[1].text(3.95,2.55,'−',ha='center',va='center',fontsize=12,color=INK)
axes[1].text(6.05,2.55,'+',ha='center',va='center',fontsize=12,color=INK)
fig.text(0.27,0.045,'(a) forward bias',ha='center',fontsize=8.5,color=INK)
fig.text(0.75,0.045,'(b) reverse bias',ha='center',fontsize=8.5,color=INK)
```

### 21.2.3 The I–V characteristic

| Region | Behaviour | Why |
|---|---|---|
| Forward, $V$ below about 0.5 V (Si) | almost no current | the applied voltage has not yet cancelled the barrier |
| Forward, $V$ above the knee (0.7 V for Si, 0.3 V for Ge) | current rises exponentially | the barrier is gone and the junction conducts freely |
| Reverse, small $V$ | tiny current, nearly constant | minority carriers only |
| Reverse, beyond the breakdown voltage | current increases sharply | avalanche or Zener breakdown |

Two things follow that questions test constantly:

- a diode is **not** a resistor: its resistance is very large in reverse and very
  small in forward, and it changes with the applied voltage;
- the **reverse saturation current is not zero**. It is the drift of minority
  carriers, and it is the reason a reverse-biased diode still leaks a little.

**Breakdown.** At a large reverse voltage the field in the depletion region becomes
strong enough to do one of two things. In **avalanche breakdown** (lightly doped
junctions, higher voltages) the few accelerated carriers knock more electrons out of
atoms, and the number multiplies. In **Zener breakdown** (heavily doped junctions,
below about 6 V) the field is strong enough to pull electrons straight out of their
bonds by tunnelling. Both are reversible if the current is limited, which is why a
Zener diode is used as a voltage reference.

### 21.2.4 The diode as a rectifier

A **rectifier** converts alternating current into direct current by letting one half
of each cycle through and blocking the other. The diode is ideal for the job because
it conducts in one direction only.

**Half-wave rectifier.** One diode in series with the load. Current flows only during
the half cycle in which the diode is forward biased; the other half is blocked, so the
output is a series of pulses with gaps.

**Full-wave rectifier.** Either two diodes with a centre-tapped transformer, or four
diodes in a bridge. Both halves of the input reach the load in the **same direction**,
so the gaps are filled and the output pulses come twice as often.

```figure caption="Rectifier output. Half-wave rectification keeps one pulse per cycle; full-wave rectification folds the negative half up, giving two pulses per cycle and a much easier waveform to smooth."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(2,1,figsize=(4.9,3.2),sharex=True)
t = np.linspace(0,40e-3,2000)
v = 12*np.sin(2*np.pi*50*t)
for ax, out, lab in [(axes[0], np.maximum(v,0), 'half-wave'),
                     (axes[1], np.abs(v), 'full-wave')]:
    ax.plot(t*1000, v, color=MUTED, lw=1.0, ls='--')
    ax.plot(t*1000, out, color=ACCENT, lw=1.8)
    ax.axhline(0, color=INK, lw=0.7)
    ax.set_ylabel('voltage (V)', fontsize=8)
    ax.set_ylim(-15,17)
    ax.set_yticks([-12,0,12])
    ax.text(20.5,16.2,lab,fontsize=8.2,color=INK,ha='left',va='top')
    ax.spines[['top','right']].set_visible(False)
    ax.grid(True, alpha=.35)
axes[1].set_xlabel('time (ms)')
axes[1].set_xlim(0,41)
fig.tight_layout()
```

| | Half-wave | Full-wave (centre tap) | Full-wave (bridge) |
|---|---|---|---|
| Diodes | 1 | 2 | 4 |
| Conducts on | one half cycle | both half cycles | both half cycles |
| Output frequency | $f$ | $2f$ | $2f$ |
| Average output | $V_0/\pi\approx0.318V_0$ | $2V_0/\pi\approx0.637V_0$ | $2V_0/\pi\approx0.637V_0$ |
| Ripple factor | 1.21 | 0.48 | 0.48 |
| Efficiency (maximum) | 40.6 % | 81.2 % | 81.2 % |

Here $V_0$ is the **peak** value of the input. The average is not $V_0/\sqrt{2}$: that
is the rms value of a full sine wave, and it belongs to a different question.

::: caution What a rectifier does not do
The output is **pulsating DC**, not the steady voltage of a battery. A reservoir
capacitor across the load charges to the peak and fills the gaps, which is why a real
charger gives a nearly steady output. Also: a rectifier does not change the
**frequency of the supply** into anything other than the pulse rate — the output
pulses are at $f$ (half-wave) or $2f$ (full-wave).
:::

::: example Worked example 21.2 — current through a forward-biased diode
**Problem.** A silicon diode (barrier 0.7 V) is in series with a 100 Ω resistor and a
5.0 V battery. Find the current.

**Solution.** The diode drops about 0.7 V, so the voltage across the resistor is
$5.0-0.7=4.3$ V.

$I=\dfrac{4.3}{100}=0.043$ A $=43$ mA.

**Check.** If the diode were reversed, the current would be only the reverse
saturation current — microamperes — and the answer would be about a million times
smaller.
:::

## 21.3 Logic gates: AND, OR, NOT, NAND and NOR

### 21.3.1 Boolean variables and truth tables

A **logic gate** is a circuit with one output and one or more inputs, where every
signal is either **0** (low, about 0 V) or **1** (high, about 5 V). A **truth table**
lists the output for every possible combination of inputs. With $n$ inputs there are
$2^n$ rows.

### 21.3.2 The five gates

**AND.** The output is 1 only when **all** inputs are 1. Written $Y=A\cdot B$. Think
of two switches in series: the lamp lights only if both are closed.

**OR.** The output is 1 when **at least one** input is 1. Written $Y=A+B$. Two
switches in parallel.

**NOT.** One input, and the output is its opposite: $Y=\bar A$. It is also called an
**inverter**.

**NAND.** AND followed by NOT: $Y=\overline{A\cdot B}$. Its output is 0 only when all
inputs are 1.

**NOR.** OR followed by NOT: $Y=\overline{A+B}$. Its output is 1 only when all inputs
are 0.

```figure caption="Truth tables of the five basic gates. NAND and NOR are each the negation of a gate the paper expects you to know cold; reading down the NAND and NOR columns is the fastest check in the exam."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.5))
cols = ['A','B','AND','OR','NAND','NOR']
rows = [('0','0','0','0','1','1'),
        ('0','1','0','1','1','0'),
        ('1','0','0','1','1','0'),
        ('1','1','1','1','0','0')]
xs = [0.55,1.35,2.45,3.35,4.35,5.35]
ax.add_patch(plt.Rectangle((0.10,2.62),5.85,0.55, fc='#EDF2F9', ec='none'))
for x,c in zip(xs,cols):
    ax.text(x,2.89,c,ha='center',va='center',fontsize=9.5,color=INK)
for i,r in enumerate(rows):
    y = 2.35 - 0.55*i
    for x,v in zip(xs,r):
        ax.text(x,y,v,ha='center',va='center',fontsize=9.5,color=INK)
for y in [3.17,2.62,2.07,1.52,0.97,0.42]:
    ax.plot([0.10,5.95],[y,y],color=MUTED,lw=0.7)
for x in [0.10,0.95,1.85,2.90,3.85,4.85,5.95]:
    ax.plot([x,x],[0.42,3.17],color=MUTED,lw=0.7)
ax.set_xlim(0,6.05); ax.set_ylim(0.25,3.30)
ax.axis('off')
```

### 21.3.3 Universal gates

A gate is **universal** if any other gate can be built from copies of it alone.
**NAND and NOR are universal; AND, OR and XOR are not.**

- **NOT from NAND:** join both inputs together. Then
  $Y=\overline{A\cdot A}=\bar A$.
- **AND from NAND:** a NAND followed by a NAND used as a NOT.
- **OR from NAND:** invert both inputs first, then NAND them:
  $\overline{\bar A\cdot\bar B}=A+B$ by De Morgan.

**De Morgan's theorems** make these manipulations possible:

$$ \overline{A\cdot B}=\bar A+\bar B, \qquad \overline{A+B}=\bar A\cdot\bar B $$

::: memory NAND and NOR in one line each
NAND is "not all ones": output 0 only for 11.
NOR is "not any one": output 1 only for 00.
:::

### 21.3.4 A worked combination: XOR from four NAND gates

The **XOR** (exclusive-OR) gate gives 1 when the inputs are **different** and 0 when
they are the same. Its expression is

$$ Y=A\bar B+\bar AB=A\oplus B $$

It is the gate that adds without carrying, and it is the heart of a half adder.

**Build it from four NAND gates.** Label the gates N1 to N4.

1. $N_1=\overline{AB}$ — the NAND of the inputs.
2. $N_2=\overline{A\cdot N_1}=\overline{A\cdot\overline{AB}}$
3. $N_3=\overline{B\cdot N_1}=\overline{B\cdot\overline{AB}}$
4. $Y=N_4=\overline{N_2\cdot N_3}$

Check the four cases:

| $A$ | $B$ | $N_1$ | $N_2$ | $N_3$ | $Y$ |
|---|---|---|---|---|---|
| 0 | 0 | 1 | 1 | 1 | 0 |
| 0 | 1 | 1 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 | 1 | 0 |

The output column is 0, 1, 1, 0: exactly XOR. Algebraically,
$\overline{N_2N_3}=\overline{\bar A\bar B\cdot\bar AB}=A\bar B+\bar AB$, which is the
XOR expression.

::: tip Two facts the paper loves
**NAND is universal, XOR is not.** Four NAND gates make an XOR; no number of XOR
gates can make an AND or an OR, because XOR always gives 0 for equal inputs.
And a two-input XOR with both inputs joined gives a constant 0 — it cannot even invert.
:::

::: example Worked example 21.3 — reading a circuit
**Problem.** A signal $A$ is fed to both inputs of a NAND gate. The output then goes
to one input of an AND gate, whose other input is $B$. Write the final output and
evaluate it for $A=1$, $B=1$.

**Solution.** The NAND with joined inputs is a NOT, so its output is $\bar A$. The AND
gate then gives $Y=\bar A\cdot B$.

For $A=1$, $B=1$: $\bar A=0$, so $Y=0\cdot1=0$.
:::

```photogrid label="21.1" cols="2" ratio="1.2" caption="A NAND gate in transistors. (a) The die of a 74HC00 holds four two-input NAND gates, sixteen transistors in all. (b) Each gate has two p-type transistors in parallel (pull-up) and two n-type in series (pull-down). For every input pair exactly one network conducts, giving Y = 1 unless A = B = 1. Because NAND is universal, a NOT needs 1 NAND, an AND needs 2 and an OR needs 3; the cell checks every case. This is why one cheap chip can build any logic circuit."
@ photo id="ceephy/nand" cap="Microphotograph of a 74HC00 chip: four NAND gates etched in silicon"
fit 1.2
focus 0.5 0.5
@ svg cap="CMOS NAND truth table from its two networks"
def nand(A, B):
    pun = (A == 0) or (B == 0); pdn = (A == 1) and (B == 1)
    assert pun != pdn
    return (1 if pun else 0), pun, pdn
rows = [(A, B) + nand(A, B) for A in (0, 1) for B in (0, 1)]
assert [r[2] for r in rows] == [1, 1, 1, 0]
N = lambda a, b: 1 - (a & b); NOT = lambda a: N(a, a); AND = lambda a, b: NOT(N(a, b)); OR = lambda a, b: N(NOT(a), NOT(b))
assert all(NOT(a) == 1 - a and AND(a, b) == (a & b) and OR(a, b) == (a | b) for a in (0, 1) for b in (0, 1))
facts = dict(nn=1, na=2, no=3)
f = Fig(300, 236)
f.text(150, 14, "Two-input CMOS NAND", size=10.5, color=NAVY, bold=True)
heads = ("A", "B", "pull-up", "pull-down", "Y")
xs = (20, 56, 92, 150, 220); ws = (36, 36, 58, 70, 60)
for x, w, h in zip(xs, ws, heads): f.box(x, 28, w, 24, label=h, fill=BLUE, stroke=NAVY, size=10.5, bold=True, r=2)
for i, (A, B, Y, pun, pdn) in enumerate(rows):
    y = 56 + i * 28
    vals = ("%d" % A, "%d" % B, "ON" if pun else "off", "ON" if pdn else "off", "%d" % Y)
    for x, w, v in zip(xs, ws, vals):
        on = v == "ON"
        f.box(x, y, w, 24, label=v, fill=MINT if on else SOFT, stroke=TEAL if on else SLATE, size=10.5, bold=on or v in ("0", "1"), r=2, color=TEAL if on else SLATE)
f.text(150, 186, "exactly one network is ON each row", size=10.5, color=NAVY, bold=True)
f.text(150, 204, "NOT = 1 NAND, AND = 2, OR = 3", size=10.5, color=NAVY, bold=True)
f.text(150, 222, "74HC00: 4 gates x 4 transistors = 16", size=10.5, color=NAVY, bold=True)
```

```photogrid label="21.2" cols="2" ratio="1.2" caption="From alternating to direct current. (a) A bridge package holds four diodes in one block, with two AC terminals and a positive and a negative output. (b) The cell follows a 12 V rms supply: its peak is 16.97 V, and since two diodes in series each drop about 0.7 V, the output peaks at 15.57 V. A 2200 microfarad capacitor supplying 0.5 A at the full-wave frequency of 100 Hz lets the voltage sag by the ripple I / (2 f C) = 2.27 V, so the output swings between 13.30 V and 15.57 V with a mean near 14.43 V. A larger capacitor or a smaller load current makes the output smoother."
@ photo id="ceephy3/bridge" cap="A diode bridge rectifier package"
fit 1.2
focus 0.5 0.5
@ svg cap="Full-wave bridge rectifier with a filter capacitor"
import math
Vrms = 12.0
Vpk = Vrms * math.sqrt(2)
Vd = Vpk - 2 * 0.7
I, fr, C = 0.5, 50.0, 2200e-6
rip = I / (2 * fr * C)
rows = [("AC rms", Vrms), ("AC peak", Vpk), ("after diodes", Vd), ("DC mean", Vd - rip / 2), ("trough", Vd - rip)]
assert round(Vpk, 2) == 16.97 and round(rip, 2) == 2.27
f = Fig(300, 236)
f.text(150, 12, "12 V transformer, bridge, 2200 uF, volts", size=10.5, color=NAVY, bold=True)
hbars(f, rows, vmax=18, fmt="%.2f", x0=84, y0=30, bw=150, gap=26,
      colors=[(BLUE, NAVY), (BLUE, NAVY), (MINT, TEAL), (SAND, AMBER), (ROSE, RED)])
f.text(150, 176, "two diodes conduct at a time: drop 2 x 0.7 V", size=10, color=SLATE, bold=True)
f.text(150, 196, "ripple = I / (2 f C) = %.2f V (V p-p)" % rip, size=10.5, color=NAVY, bold=True)
f.text(150, 214, "full wave: ripple at 100 Hz, half of half-wave's", size=10, color=SLATE, bold=True)
facts = dict(pk=Vpk, vd=Vd, rip=rip, dc=Vd - rip / 2, tr=Vd - rip)
```

## Formula and fact sheet

| Item | Fact or formula |
|---|---|
| Band gap | metal $\approx0$; Ge 0.7 eV, Si 1.1 eV, GaAs 1.4 eV; insulator > 3 eV (diamond 5.5 eV) |
| Gap and wavelength | $E_g=hc/\lambda$, so $\lambda_{max}=1240/E_g(\text{eV})$ nm |
| Intrinsic | $n_e=n_h=n_i$; Si $n_i\approx1.5\times10^{16}$ m⁻³ at 300 K; resistance falls with temperature |
| n-type | pentavalent donor (P, As, Sb); electrons majority; donor level just below $E_c$ |
| p-type | trivalent acceptor (B, Al, Ga, In); holes majority; acceptor level just above $E_v$ |
| Mass action | $n_en_h=n_i^2$ |
| Conductivity | $\sigma=e(n_e\mu_e+n_h\mu_h)$, $\rho=1/\sigma$ |
| Junction | diffusion → recombination → depletion layer of immobile ions → barrier |
| Barrier potential | Si 0.7 V, Ge 0.3 V |
| Forward bias | p to +, depletion narrows, barrier falls, current large |
| Reverse bias | p to −, depletion widens, barrier rises, current = minority-carrier drift (µA or nA) |
| Breakdown | avalanche (impact ionisation) or Zener (tunnelling, heavily doped, < 6 V) |
| Half-wave | 1 diode; output at $f$; average $V_0/\pi=0.318V_0$; ripple factor 1.21; efficiency 40.6 % |
| Full-wave | 2 diodes (centre tap) or 4 (bridge); output at $2f$; average $2V_0/\pi=0.637V_0$; ripple 0.48; efficiency 81.2 % |
| Gate expressions | AND $A\cdot B$; OR $A+B$; NOT $\bar A$; NAND $\overline{AB}$; NOR $\overline{A+B}$; XOR $A\bar B+\bar AB$ |
| Gate outputs | AND: 1 only for 11. OR: 1 for 01, 10, 11. NAND: 0 only for 11. NOR: 1 only for 00 |
| Universal gates | NAND and NOR only |
| De Morgan | $\overline{AB}=\bar A+\bar B$; $\overline{A+B}=\bar A\cdot\bar B$ |
| XOR from NAND | 4 NAND gates; half-adder: sum = XOR, carry = AND |

## Chapter summary

- In a solid the atomic levels broaden into bands; the valence band is full, the
  conduction band is where moving electrons live, and the gap between them decides
  the class of the solid.
- Metals have no gap (or overlapping bands) and their resistance **rises** with
  temperature; semiconductors have $E_g$ of about 1 eV and their resistance **falls**;
  insulators have $E_g>3$ eV.
- In an intrinsic semiconductor $n_e=n_h=n_i$, and conduction is by electron–hole
  pairs created by thermal energy.
- A pentavalent donor makes an n-type crystal (electrons majority); a trivalent
  acceptor makes a p-type crystal (holes majority). The crystal stays neutral, and
  $n_en_h=n_i^2$.
- At a p–n junction, diffusion and recombination leave a depletion layer of fixed ions
  and a barrier of 0.7 V (Si) or 0.3 V (Ge).
- Forward bias narrows the depletion layer and lowers the barrier; reverse bias widens
  it and raises it. The reverse current is a small **minority-carrier drift**, not
  zero, and a diode's resistance is not constant.
- A diode rectifies: one diode gives half-wave output at $f$ with average
  $0.318V_0$; two or four give full-wave output at $2f$ with average $0.637V_0$.
- AND gives 1 only for 11; OR gives 1 for any 1; NOT inverts; NAND is the negation of
  AND; NOR the negation of OR.
- NAND and NOR are universal. XOR ($A\bar B+\bar AB$) is not, and it takes four NAND
  gates to build one.

## Practice questions

**Set A — Recall (24 questions)**

1. In a metal at room temperature the conduction band is
   (a) completely empty (b) completely full (c) partly filled (d) separated by a gap of 3 eV
2. The forbidden energy gap of a typical insulator is
   (a) about 0.1 eV (b) more than 3 eV (c) about 1.1 eV (d) zero
3. The energy gaps of silicon and germanium are about
   (a) 0.7 eV and 1.1 eV (b) 5.5 eV and 3.0 eV (c) 1.1 eV and 5.5 eV (d) 1.1 eV and 0.7 eV
4. Doping silicon with phosphorus produces
   (a) an n-type semiconductor (b) a p-type semiconductor (c) an intrinsic semiconductor (d) an insulator
5. In a p-type semiconductor the majority carriers are
   (a) electrons (b) positive ions (c) holes (d) protons
6. A pentavalent impurity atom in silicon is called
   (a) an acceptor (b) a donor (c) a recombination centre (d) an intrinsic carrier
7. The mass action law for a semiconductor in equilibrium is
   (a) $n_en_h=n_i$ (b) $n_e+n_h=n_i^2$ (c) $n_e/n_h=n_i^2$ (d) $n_en_h=n_i^2$
8. The barrier potential of a silicon p–n junction is about
   (a) 0.7 V (b) 0.3 V (c) 1.1 V (d) 5.0 V
9. In forward bias the p-side of a diode is connected to the
   (a) negative terminal (b) positive terminal (c) earth (d) case
10. When a p–n junction is reverse biased, the depletion region
   (a) disappears (b) narrows (c) widens (d) stays the same width
11. The reverse saturation current of a diode is carried by
   (a) minority carriers (b) majority carriers (c) the fixed ions (d) the battery only
12. A half-wave rectifier uses
   (a) four diodes (b) two diodes (c) no diode (d) one diode
13. A full-wave rectifier is fed with 60 Hz AC. Its output pulses are at
   (a) 30 Hz (b) 60 Hz (c) 120 Hz (d) 240 Hz
14. The Boolean expression for an AND gate is
   (a) $A+B$ (b) $\bar A$ (c) $A\cdot B$ (d) $\overline{A\cdot B}$
15. The output of a NOR gate is 1 when
   (a) both inputs are 0 (b) both inputs are 1 (c) at least one input is 1 (d) the inputs are different
16. Which of the following is a universal gate?
   (a) AND (b) OR (c) XOR (d) NAND
17. The number of NAND gates needed to build an XOR gate is
   (a) two (b) four (c) three (d) six
18. A NOT gate is also called
   (a) an inverter (b) a buffer (c) an adder (d) a rectifier
19. A two-input gate gives output 1 only when both inputs are 1. The gate is
   (a) OR (b) NOR (c) AND (d) NAND
20. De Morgan's theorem may be written as
   (a) $\overline{A+B}=\bar A+\bar B$ (b) $A\cdot B=A+B$ (c) $A+0=1$ (d) $\overline{A\cdot B}=\bar A+\bar B$
21. In an intrinsic semiconductor, the number of holes is
   (a) equal to the number of conduction electrons (b) greater than the number of electrons (c) less than the number of electrons (d) zero at all temperatures
22. As the temperature of a semiconductor rises, its resistance
   (a) increases (b) decreases (c) stays the same (d) becomes infinite
23. A hole in a semiconductor is
   (a) a free proton (b) a positive ion (c) a vacant bond that behaves as a positive charge (d) a positron
24. At absolute zero the conduction band of a pure semiconductor is
   (a) half filled (b) completely full (c) partly filled (d) completely empty

::: note Answers and explanations — Set A
**1.** (c) — in a metal the highest band is only partly occupied (or two bands overlap), so electrons can move into empty states just above the filled ones. That is why metals conduct well.
**2.** (b) — insulators such as diamond have gaps of several electron volts (diamond about 5.5 eV), far more than thermal energy at room temperature.
**3.** (d) — silicon 1.1 eV, germanium 0.7 eV. Germanium's smaller gap is why it conducts more at the same temperature.
**4.** (a) — phosphorus is pentavalent: it donates its fifth electron, so electrons become the majority carriers and the crystal is n-type.
**5.** (c) — the trivalent acceptor takes an electron and leaves a hole, so holes dominate in p-type material.
**6.** (b) — a pentavalent atom donates an electron to the conduction band, hence "donor".
**7.** (d) — in equilibrium the product of the concentrations is fixed: $n_en_h=n_i^2$.
**8.** (a) — 0.7 V for silicon, 0.3 V for germanium. The barrier is set by the material, not by the applied voltage.
**9.** (b) — forward bias means p to the positive terminal, which lowers the barrier and lets holes and electrons flow towards the junction.
**10.** (c) — the applied field adds to the built-in field and pulls majority carriers away, so the depletion layer widens.
**11.** (a) — only minority carriers are available to be swept across in reverse bias, so the current is tiny.
**12.** (d) — one diode blocks one half of each cycle; two (centre tap) or four (bridge) are needed for full-wave.
**13.** (c) — both halves are used, so there are two pulses per cycle: $2\times60=120$ Hz.
**14.** (c) — AND is logical multiplication, $Y=A\cdot B$; $A+B$ is OR and $\overline{A\cdot B}$ is NAND.
**15.** (a) — NOR is the negation of OR, and OR is 0 only when both inputs are 0, so NOR is 1 only for 00.
**16.** (d) — NAND (like NOR) can build every other gate, so it is universal; AND, OR and XOR cannot.
**17.** (b) — four NAND gates: one to form $\overline{AB}$ and three to combine it into $A\bar B+\bar AB$.
**18.** (a) — the NOT gate inverts its single input, hence "inverter".
**19.** (c) — that is the definition of AND. NAND gives 0 for 11, and OR gives 1 for 01 and 10 as well.
**20.** (d) — the NAND of $A$ and $B$ equals $\bar A+\bar B$; the dual form is $\overline{A+B}=\bar A\cdot\bar B$, not $\bar A+\bar B$.
**21.** (a) — every thermally freed electron leaves one hole, so the two concentrations are equal in a pure crystal.
**22.** (b) — heating frees many more electron–hole pairs, and the rise in carriers outweighs the extra scattering, so resistance falls.
**23.** (c) — a hole is not a particle but a missing electron in a covalent bond; it behaves as a positive carrier because neighbouring electrons move into it.
**24.** (d) — at 0 K no electron has enough thermal energy to cross the gap, so the conduction band is empty and the crystal behaves as an insulator.
:::

**Set B — Understanding (14 questions)**

1. The energy gap of a semiconductor is much smaller than that of an insulator. The practical result at room temperature is that
   (a) no electrons can ever cross the gap (b) a small fraction of electrons is thermally excited across it (c) the valence band becomes empty (d) the material becomes a metal
2. Adding a trivalent impurity to silicon makes it p-type because the impurity atom
   (a) donates an extra electron (b) has one electron too many (c) repels electrons (d) accepts an electron and leaves a hole
3. In an n-type semiconductor the donor level lies
   (a) just below the conduction band (b) just above the valence band (c) at the centre of the gap (d) inside the conduction band
4. When a p–n junction is formed, the electrons and holes near the boundary
   (a) are pushed apart by the battery (b) stay where they are (c) diffuse across and recombine, leaving fixed ions (d) form a metal layer
5. A reverse-biased diode carries only a very small current because
   (a) the barrier disappears (b) only minority carriers are available to cross (c) the junction becomes an insulator (d) the battery is disconnected
6. The resistance of a forward-biased diode is
   (a) very large and constant (b) infinite (c) equal to that of the wire (d) small and not constant
7. In the output of a half-wave rectifier, the current is zero during
   (a) no part of the cycle (b) a quarter of each cycle (c) one half of each cycle (d) the whole cycle
8. If one diode of a bridge rectifier is connected the wrong way round, the output is
   (a) zero, and the supply may be shorted (b) half-wave rectified (c) unchanged (d) doubled
9. An XOR gate gives output 1 when
   (a) both inputs are 1 (b) the two inputs are different (c) both inputs are 0 (d) at least one input is 1
10. A NAND gate with both inputs joined together acts as
   (a) an OR gate (b) an AND gate (c) a buffer (d) a NOT gate
11. The output of a two-input NAND gate with inputs 1 and 0 is
   (a) 1 (b) 0 (c) undefined (d) equal to the input 1
12. Compared with a half-wave rectifier, a full-wave rectifier produces output pulses at
   (a) half the frequency (b) the same frequency (c) twice the frequency (d) four times the frequency
13. A germanium diode conducts at a lower forward voltage than a silicon diode because germanium has
   (a) a larger band gap (b) a smaller band gap (c) more free electrons than silicon at 0 K (d) no depletion region
14. The output of an AND gate is 1 only when
   (a) any one input is 1 (b) no input is 1 (c) exactly one input is 1 (d) all its inputs are 1

::: note Answers and explanations — Set B
**1.** (b) — the gap is only about 1 eV, and thermal energy at 300 K is enough to lift a small fraction of electrons across it. An insulator's gap of several eV is not bridged at all.
**2.** (d) — the trivalent atom has only three valence electrons for four bonds, so it takes an electron from a neighbour and leaves a hole; that is an acceptor.
**3.** (a) — a donor's extra electron is only loosely bound, so its level sits just below the conduction band and is easily ionised.
**4.** (c) — majority carriers diffuse down their concentration gradient, recombine, and leave behind the immobile dopant ions that form the depletion layer.
**5.** (b) — the barrier is raised, so majority carriers cannot cross; only the few minority carriers present are swept across.
**6.** (d) — the diode is highly non-ohmic: its resistance falls sharply as the forward voltage passes the knee, so it is small but not constant.
**7.** (c) — the diode is reverse biased for one half of every cycle, so that half is blocked entirely.
**8.** (a) — reversing one diode makes it block the half cycle in which it should conduct, and it short-circuits the other path, so no useful output appears.
**9.** (b) — exclusive-OR is 1 for 01 and 10 and 0 for 00 and 11: it detects a difference.
**10.** (d) — with both inputs the same, $Y=\overline{A\cdot A}=\bar A$, which is inversion.
**11.** (a) — NAND is 0 only when both inputs are 1; for 1 and 0 the output is 1.
**12.** (c) — the full-wave output has a pulse every half cycle, so its pulse rate, and therefore its ripple frequency, is $2f$.
**13.** (b) — the barrier is roughly the band gap per electron, and germanium's 0.7 eV gap gives a 0.3 V barrier against silicon's 0.7 V.
**14.** (d) — AND requires every input to be 1; OR is the gate that accepts any one.
:::

**Set C — Application (10 questions)**

1. For silicon, with $E_g=1.1$ eV, the longest wavelength of light that can raise an electron across the gap is about
   (a) 620 nm (b) 886 nm (c) 1127 nm (d) 1771 nm
2. A silicon sample at 300 K has $n_i=1.5\times10^{16}$ m⁻³ and is doped so that $n_e=4.5\times10^{22}$ m⁻³. The hole concentration is
   (a) $5.0\times10^{9}$ m⁻³ (b) $5.0\times10^{10}$ m⁻³ (c) $3.0\times10^{38}$ m⁻³ (d) $3.3\times10^{-7}$ m⁻³
3. A doped sample has $n_e=5.0\times10^{22}$ m⁻³ and electron mobility 0.05 m² V⁻¹ s⁻¹. Its conductivity is
   (a) 40 S m⁻¹ (b) $4.0\times10^{3}$ S m⁻¹ (c) 0.4 S m⁻¹ (d) 400 S m⁻¹
4. A silicon diode (0.7 V barrier) is in series with a 100 Ω resistor and a 5.0 V supply. The current is
   (a) 50 mA (b) 43 mA (c) 5.7 mA (d) 0.43 mA
5. A full-wave rectifier is fed with a sine wave of peak value 12 V. The average output voltage is about
   (a) 3.8 V (b) 12 V (c) 7.6 V (d) 8.5 V
6. A half-wave rectifier is fed with a sine wave of peak value 12 V. The average output voltage is about
   (a) 3.8 V (b) 7.6 V (c) 12 V (d) 6.0 V
7. A 1 kHz square wave is applied to one input of an AND gate while the other input is held at 1. The output frequency is
   (a) 500 Hz (b) 1 kHz (c) 2 kHz (d) 0
8. A NOR gate has both inputs at 0, and its output is fed to a NOT gate. The final output is
   (a) 1 (b) 0 (c) undefined (d) equal to the input
9. The output of a full-wave rectifier has a peak value of 10 V. Its rms value is about
   (a) 10 V (b) 5.0 V (c) 7.1 V (d) 6.4 V
10. A silicon diode (0.7 V barrier) is in series with a 200 Ω resistor and a 10 V supply. The current is
   (a) 50 mA (b) 20 mA (c) 5.0 mA (d) 46.5 mA

::: note Answers and explanations — Set C
**1.** (c) — $\lambda=1240/1.1=1127$ nm, in the near infrared. 620 nm would need a gap of 2.0 eV, and 1771 nm is germanium's 0.7 eV gap.
**2.** (a) — $n_h=n_i^2/n_e=(1.5\times10^{16})^2/(4.5\times10^{22})=2.25\times10^{32}/4.5\times10^{22}=5.0\times10^{9}$ m⁻³. Doping with electrons has suppressed the holes.
**3.** (d) — $\sigma=en_e\mu_e=1.6\times10^{-19}\times5.0\times10^{22}\times0.05=400$ S m⁻¹.
**4.** (b) — the resistor takes $5.0-0.7=4.3$ V, so $I=4.3/100=43$ mA. Option (a) forgets the diode drop.
**5.** (c) — $V_{av}=2V_0/\pi=2(12)/\pi=7.6$ V.
**6.** (a) — $V_{av}=V_0/\pi=12/\pi=3.8$ V, exactly half the full-wave value.
**7.** (b) — with one input held at 1 the AND gate passes the other input unchanged, so the output has the same 1 kHz frequency.
**8.** (b) — NOR of 0 and 0 is 1, and the NOT gate turns that into 0.
**9.** (c) — for a full-wave rectified sine the rms value is $V_0/\sqrt{2}=10/1.414=7.1$ V.
**10.** (d) — the resistor takes $10-0.7=9.3$ V, so $I=9.3/200=46.5$ mA. Option (a) is $10/200$, which ignores the diode.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Explain the formation of a p-n junction, its forward and reverse characteristics and its use as a rectifier. <span class="marks">[10]</span>
2. Explain the action of a transistor as an amplifier and the logic gates, showing that NAND is a universal gate. <span class="marks">[10]</span>

```photogrid label="21.H" cols="2" ratio="1.4" caption="Electronics hardware. (a) A NAND gate integrated circuit, the building block of digital logic. (b) Light-emitting diodes: p-n junctions that emit light when forward biased."
@ photo id="ceephy/nand" cap="(a) NAND gate IC"
fit 1.4
focus 0.5 0.5
@ photo id="ceephy2/leds" cap="(b) LEDs"
fit 1.4
focus 0.5 0.5
```

### Model answer D1: the p-n junction diode and rectification (10 marks)

**Introduction.** A **semiconductor** has a resistivity between that of conductors and insulators, which falls as the temperature rises. In **n-type** silicon, pentavalent impurities (P, As) give free electrons (majority carriers). In **p-type**, trivalent impurities (B, Al) give holes.

**Formation of the junction.** When p and n regions are joined, electrons diffuse from n to p and holes from p to n. The fixed ions left behind form a **depletion layer** with a **barrier potential** of about $0.7\ \text{V}$ for silicon and $0.3\ \text{V}$ for germanium. It stops further diffusion.

**Biasing.**

1. **Forward bias** (p to positive): the barrier is lowered, the depletion layer narrows and the current rises exponentially after the knee voltage. The forward resistance is small.
2. **Reverse bias:** the depletion layer widens, and only a tiny leakage current (microampere) of minority carriers flows. The resistance is very large, until the **breakdown** (Zener or avalanche) voltage.

**Rectifier.**

| Feature | Half-wave | Full-wave |
|---|---|---|
| Diodes | 1 | 2 (centre-tap) or 4 (bridge) |
| Output frequency | 50 Hz | 100 Hz |
| Maximum efficiency | $40.6\%$ | $81.2\%$ |
| Ripple | high | low |
| DC value | $I_0/\pi$ | $2I_0/\pi$ |

A capacitor filter smooths the output, and a Zener diode in reverse breakdown holds the voltage constant (regulator).

**Other diodes.** An LED emits light in forward bias, a photodiode works in reverse bias and converts light to current, and a solar cell generates a voltage without any bias.

**Numerical.** A full-wave rectifier works from a $50\ \text{Hz}$ supply, so the output ripple frequency is $100\ \text{Hz}$. For a silicon diode in series with a $1\ \text{k}\Omega$ resistor and a $5.7\ \text{V}$ battery in forward bias, $I = \dfrac{5.7 - 0.7}{1000} = 5\ \text{mA}$.

**Conclusion.** A p-n junction conducts mainly in the forward direction, which allows it to convert AC to DC.

### Model answer D2: transistor and logic gates (10 marks)

**Introduction.** A **transistor** has three layers (npn or pnp): the emitter (heavily doped), the thin base (lightly doped) and the collector (largest). The emitter-base junction is forward biased and the collector-base junction is reverse biased.

**Currents.** $I_E = I_B + I_C$. The current gains are $\alpha = I_C/I_E$ (about $0.98$) and $\beta = I_C/I_B$ (about $50$ to $200$), with $\beta = \dfrac{\alpha}{1 - \alpha}$.

**Common-emitter amplifier.** A small change in base current gives a large change in collector current. The voltage gain is $A_v = -\beta\dfrac{R_C}{R_{in}}$, and the output is $180^{\circ}$ out of phase with the input. The transistor is also a **switch**: in cut-off it is OFF and in saturation it is ON.

**Logic gates.**

| Gate | Boolean expression | Output is 1 when |
|---|---|---|
| OR | $A + B$ | at least one input is 1 |
| AND | $A\cdot B$ | both inputs are 1 |
| NOT | $\bar A$ | the input is 0 |
| NAND | $\overline{A\cdot B}$ | not both inputs are 1 |
| NOR | $\overline{A + B}$ | both inputs are 0 |
| XOR | $A \oplus B$ | the inputs differ |

**NAND as a universal gate.** NOT: join both inputs, $\overline{A\cdot A} = \bar A$. AND: a NAND followed by a NOT-NAND. OR: invert each input, then NAND them, $\overline{\bar A\cdot\bar B} = A + B$ (De Morgan). So any logic circuit can be made from NAND gates alone. NOR is also universal.

**De Morgan's theorems.** $\overline{A + B} = \bar A\cdot\bar B$ and $\overline{A\cdot B} = \bar A + \bar B$.

**Numerical.** If $I_B = 40\ \mu\text{A}$ and $\beta = 100$, then $I_C = 4\ \text{mA}$ and $I_E = 4.04\ \text{mA}$, so $\alpha = 4/4.04 = 0.99$. If the collector load is $2\ \text{k}\Omega$ and the base-circuit input resistance is $1\ \text{k}\Omega$, the voltage gain is $100\times2 = 200$ in magnitude.

**Conclusion.** The transistor amplifies and switches, and NAND or NOR gates alone are enough to build any digital circuit.
