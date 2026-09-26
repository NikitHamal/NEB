---
subject: Physics
grade: 12
unit: 22
title: Semiconductor devices
hours: 6
area: Modern Physics
---

A semiconductor on its own is a poor conductor. Add one foreign atom in ten
million and it becomes useful; join a piece doped one way to a piece doped the
other and it becomes a **device**. Every rectifier and logic gate in a phone, an
inverter or a solar charger in a Nepali village rests on the thin layer where
those two pieces meet. This unit follows that layer to the diode, the power
supply and the logic gate.

::: key What the examiner wants
The p-n junction and its two bias conditions, the diode characteristic curve,
the full-wave rectifier (circuit, waveform, and the numbers $V_{dc}=2V_m/\pi$ and
$\eta = 81.2\%$), and the five logic-gate truth tables. Those four items have
appeared in almost every recent paper.
:::

## 22.1 P-N Junction

Pure (intrinsic) silicon or germanium has four valence electrons per atom and few
free carriers. Doping changes that:

| Type | Dopant (valency) | Examples | Majority carriers | Minority carriers |
|---|---|---|---|---|
| n-type | pentavalent (donor) | P, As, Sb | electrons | holes |
| p-type | trivalent (acceptor) | B, Al, Ga, In | holes | electrons |

Both types are electrically **neutral** — doping adds a carrier and its parent
ion together.

A **p-n junction** is a single crystal, one half doped p and the other n. The
moment it is formed, two things happen.

1. **Diffusion.** Holes diffuse from p to n and electrons from n to p, because
   each carrier is far more concentrated on its own side.
2. **Recombination.** Near the boundary they meet and cancel, leaving a thin
   layer with almost no mobile charge — the **depletion region** — but with the
   fixed, charged dopant ions still in place: negative acceptor ions on the p
   side, positive donor ions on the n side.

Those immobile ions set up an electric field pointing from n to p, which opposes
further diffusion. Equilibrium is reached when the field is just strong enough to
stop the net flow. The pd across the layer is the **barrier** (or contact)
potential $V_B$: about $0.3\ \text{V}$ for germanium and $0.7\ \text{V}$ for
silicon at room temperature. The depletion width is typically $0.5\ \mu\text{m}$.

```figure caption="(a) The depletion region of an unbiased p-n junction: immobile ions left behind by diffusion set up a field from n to p. (b) The same junction in energy-band terms — the bands bend by $eV_B$ and the Fermi level $E_F$ is flat right across."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, (ax, bx) = plt.subplots(1, 2, figsize=(5.1,2.7))

ax.add_patch(Rectangle((0,0),4.0,3.0, fc='#eaf1f8', ec=INK, lw=1.1))
ax.add_patch(Rectangle((4.0,0),4.0,3.0, fc='#fdeeed', ec=INK, lw=1.1))
ax.add_patch(Rectangle((3.0,0),2.0,3.0, fc='#ffffff', ec=MUTED, lw=1.0, ls=(0,(4,3))))
ax.text(1.5,3.22,'p-type', fontsize=9, color=SERIES[0], ha='center')
ax.text(6.5,3.22,'n-type', fontsize=9, color=SERIES[1], ha='center')
def ion(x, y, sym, col):
    ax.plot([x],[y], marker='o', mfc='none', mec=col, ms=11, mew=1.0)
    ax.text(x, y+0.01, sym, fontsize=8.0, color=col, ha='center', va='center')
for y in [0.60,1.50,2.40]:
    ion(3.50, y, '–', SERIES[0])
    ion(4.50, y, '+', SERIES[1])
for x in [0.55,1.30,2.05,2.70]:
    for y in [0.75,2.25]:
        ax.text(x,y,'+', fontsize=10, color=MUTED, ha='center', va='center')
for x in [5.35,6.05,6.75,7.45]:
    for y in [0.75,2.25]:
        ax.text(x,y,'–', fontsize=10, color=MUTED, ha='center', va='center')
ax.annotate('', xy=(3.05,-0.45), xytext=(4.95,-0.45),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.5, mutation_scale=11))
ax.text(4.0,-1.12,'field $E$', fontsize=8.2, color='#2e8b57', ha='center')
ax.annotate('', xy=(3.0,3.58), xytext=(5.0,3.58),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=8))
ax.text(4.0,3.74,'$W$', fontsize=9, color=INK, ha='center')
ax.text(1.4,-0.85,'holes', fontsize=8.0, color=MUTED, ha='center')
ax.text(6.6,-0.85,'electrons', fontsize=8.0, color=MUTED, ha='center')
ax.set_xlim(-0.3,8.3); ax.set_ylim(-1.5,4.3); ax.axis('off')
ax.set_title('(a)  depletion region', fontsize=8.8)

x = np.linspace(0,8,400)
step = 1.0/(1+np.exp(-(x-4.0)*2.2))
bx.plot(x, 2.6 - 1.25*step, color=SERIES[0], lw=1.8)
bx.plot(x, 0.7 - 1.25*step, color=SERIES[1], lw=1.8)
bx.axhline(0.98, color=INK, lw=1.0, ls=(0,(4,3)))
bx.text(7.9,1.10,'$E_F$', fontsize=8.6, color=INK, ha='right')
bx.text(0.1,2.75,'$E_C$', fontsize=8.6, color=SERIES[0])
bx.text(0.1,0.28,'$E_V$', fontsize=8.6, color=SERIES[1])
bx.annotate('', xy=(4.0,2.60), xytext=(4.0,1.35),
            arrowprops=dict(arrowstyle='<|-|>', color='#2e8b57', lw=1.1, mutation_scale=8))
bx.text(4.18,1.85,'$eV_B$', fontsize=8.8, color='#2e8b57')
bx.axvline(4.0, color=MUTED, lw=0.7, ls=':')
bx.text(1.6,-0.35,'p', fontsize=9, color=MUTED, ha='center')
bx.text(6.4,-0.35,'n', fontsize=9, color=MUTED, ha='center')
bx.set_xlim(0,8); bx.set_ylim(-0.7,3.2)
bx.set_xticks([]); bx.set_yticks([])
bx.set_ylabel('electron energy', fontsize=8.6)
bx.spines[['top','right','bottom']].set_visible(False)
bx.set_title('(b)  energy bands', fontsize=8.8)
```
**Biasing.** Connect a battery across the junction and the barrier changes.

| | Forward bias (p to +, n to −) | Reverse bias (p to −, n to +) |
|---|---|---|
| Applied field | opposes the barrier field | adds to the barrier field |
| Barrier height | reduced to $V_B - V$ | raised to $V_B + V$ |
| Depletion width | narrows | widens |
| Current | large, by **majority** carriers, mA | tiny, by **minority** carriers, μA |
| Resistance | low (a few ohms) | very high (megohms) |

::: key The one-way street
A p-n junction conducts freely in one direction and hardly at all in the other.
That asymmetry — not any exotic effect — is what makes the junction useful.
:::

::: example Worked example 22.1
**Problem.** A silicon p-n junction has a barrier potential of $0.70\ \text{V}$
across a depletion layer $0.50\ \mu\text{m}$ wide. Find the average electric field
in the depletion layer. What happens to this field when the junction is reverse
biased by $5.0\ \text{V}$, assuming the width stays the same?

**Solution.** The average field is the pd divided by the width:

$$ E = \frac{V_B}{W} = \frac{0.70}{0.50\times10^{-6}} = 1.4\times10^{6}\ \text{V m}^{-1} $$

Under $5.0\ \text{V}$ reverse bias the total pd across the layer is
$0.70 + 5.0 = 5.7\ \text{V}$, so

$$ E' = \frac{5.7}{0.50\times10^{-6}} = 1.14\times10^{7}\ \text{V m}^{-1} $$

an eightfold increase. (In reality $W$ also widens, so the field grows a little
less than this.) Fields of this size explain why a junction eventually breaks
down.
:::

## 22.2 Semiconductor diode: Characteristics in forward and reverse bias

A p-n junction with two leads is a **junction diode**. Its symbol is an arrowhead
(the p side, or **anode**) touching a bar (the n side, or **cathode**); the arrow
points the way conventional current can flow.

To obtain the characteristic, connect the diode in series with a resistor,
a milliammeter and a variable pd; record current against voltage; then reverse
the battery and repeat with a microammeter.

```figure caption="Static characteristic of a junction diode. Note the two different current scales: mA forward, $\\mu$A reverse."
import numpy as np, matplotlib.pyplot as plt
fig = plt.figure(figsize=(4.8,3.0))
gs = fig.add_gridspec(2, 2, width_ratios=[1.0,1.1], height_ratios=[1.1,1.0],
                      wspace=0.0, hspace=0.0)
axf = fig.add_subplot(gs[0,1])
axr = fig.add_subplot(gs[1,0])

V = np.linspace(0, 0.95, 500)
axf.plot(V, np.clip(1.87e-7*np.exp(V/0.045), 0, 30), color=SERIES[0], lw=2.0, label='Si')
axf.plot(V, np.clip(1.87e-7*np.exp((V+0.40)/0.045), 0, 30), color=SERIES[3], lw=1.5,
         ls=(0,(5,2)), label='Ge')
axf.set_xlim(0,0.95); axf.set_ylim(0,30)
axf.set_xticks([0.2,0.4,0.6,0.8]); axf.set_yticks([10,20,30])
axf.set_xlabel('forward bias  $V$  (V)', fontsize=8.6)
axf.set_ylabel('$I$  (mA)', fontsize=8.6)
axf.spines[['top','right']].set_visible(False)
axf.grid(True, alpha=0.4)
axf.legend(loc='upper left', fontsize=8.0)
axf.annotate('knee  0.7 V', (0.72,2.5), xytext=(-24,30), textcoords='offset points',
             fontsize=8.2, color=SERIES[0], ha='center',
             arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.0, mutation_scale=9))

Vr = np.linspace(-10.0, 0, 500)
Ir = np.where(Vr > -7.5, -1.0, -1.0 + 12*(Vr + 7.5))
axr.plot(Vr, np.clip(Ir, -25, 0), color=SERIES[0], lw=2.0)
axr.set_xlim(-10,0); axr.set_ylim(-25,0)
axr.set_xticks([-10,-8,-6,-4,-2]); axr.set_yticks([-20,-10])
axr.set_xlabel('reverse bias  $V$  (V)', fontsize=8.6)
axr.set_ylabel('$I$  ($\mu$A)', fontsize=8.6)
axr.spines[['left','bottom']].set_visible(False)
axr.grid(True, alpha=0.4)
axr.annotate('breakdown', (-7.7,-9), xytext=(12,-12), textcoords='offset points',
             fontsize=8.2, color=SERIES[0],
             arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.0, mutation_scale=9))
axr.text(-9.6,-3.6,'reverse saturation current', fontsize=7.6, color=MUTED)
```
Reading the curve:

- **Forward bias.** Almost no current until the applied voltage cancels most of
  the barrier. Beyond this **knee** (or cut-in) voltage — $0.7\ \text{V}$ for Si,
  $0.3\ \text{V}$ for Ge — the current rises very steeply and is limited only by
  the external resistance. The curve is **non-linear**: a diode does not obey
  Ohm's law.
- **Reverse bias.** A small, almost constant **reverse saturation current** of a
  few microamps, carried by thermally generated minority carriers. It doubles for
  roughly every $10\ ^\circ\text{C}$ rise but hardly changes with voltage.
- **Breakdown.** At a high enough reverse voltage the current suddenly becomes
  large (avalanche or Zener breakdown). An ordinary diode is destroyed; a Zener
  diode is designed to work there and is used as a voltage regulator.

The **dynamic** (a.c.) resistance in the forward region is the reciprocal of the
slope at the working point:

$$ r_d = \frac{\Delta V}{\Delta I} $$

::: caution Do not use $V/I$
The static ratio $V/I$ and the dynamic ratio $\Delta V/\Delta I$ are different
numbers for a diode, because the graph is a curve and not a line through the
origin. Examiners ask for the *dynamic* resistance, so always take a small change
about the stated point.
:::

::: example Worked example 22.2
**Problem.** (a) A silicon diode is joined in series with a $1.0\ \text{k}\Omega$
resistor across a $5.0\ \text{V}$ supply, connected in forward bias. Taking the
diode drop as $0.7\ \text{V}$, find the current and the power dissipated in the
diode. (b) On the forward characteristic, the current rises from $10\ \text{mA}$
to $30\ \text{mA}$ when the voltage goes from $0.70\ \text{V}$ to $0.74\ \text{V}$.
Find the dynamic resistance.

**Solution.**

(a) The resistor carries the whole of the remaining voltage:

$$ I = \frac{V - V_D}{R} = \frac{5.0 - 0.7}{1.0\times10^{3}} = 4.3\times10^{-3}\ \text{A} = 4.3\ \text{mA} $$

$$ P_D = V_D I = 0.7\times4.3\times10^{-3} = 3.0\times10^{-3}\ \text{W} = 3.0\ \text{mW} $$

(b) $r_d = \dfrac{\Delta V}{\Delta I} = \dfrac{0.74-0.70}{(30-10)\times10^{-3}}
= \dfrac{0.04}{0.02} = 2\ \Omega$.

:::

## 22.3 Full wave rectification

**Rectification** is the conversion of alternating current into direct current. A
diode does it by conducting only on the half-cycles that forward bias it.

**Half-wave rectifier.** One diode in series with the load. The negative half of
each cycle is simply thrown away, so the output is a series of gaps.

```figure caption="Half-wave rectifier: circuit (left) and output across the load (right). Only the positive half-cycles appear; the mean value is $V_m/\\pi$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, (ax, bx) = plt.subplots(1, 2, figsize=(5.1,2.4),
                             gridspec_kw={'width_ratios':[1.0,1.05]})
ax.plot([0.5,0.5],[0.4,2.6], color=INK, lw=2.0)
ax.plot([0.85,0.85],[0.4,2.6], color=INK, lw=2.0)
ax.text(0.67,2.90,'a.c. input', fontsize=8.2, color=INK, ha='center')
ax.plot([0.85,2.0],[2.6,2.6], color=INK, lw=1.2)
ax.plot([2.55,3.6,3.6],[2.6,2.6,1.9], color=INK, lw=1.2)
ax.plot([0.85,3.6],[0.4,0.4], color=INK, lw=1.2)
ax.plot([3.6,3.6],[0.4,1.1], color=INK, lw=1.2)
ax.fill([2.0,2.0,2.5],[2.35,2.85,2.6], color=INK)
ax.plot([2.52,2.52],[2.33,2.87], color=INK, lw=2.0)
ax.text(2.25,3.05,'D', fontsize=8.6, color=INK, ha='center')
ax.add_patch(Rectangle((3.32,1.1),0.56,0.8, fill=False, ec=INK, lw=1.2))
ax.text(3.22,1.50,'$R_L$', fontsize=9, color=INK, ha='right', va='center')
ax.annotate('', xy=(4.35,1.9), xytext=(4.35,1.1),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=7))
ax.text(4.50,1.5,'$v_{out}$', fontsize=8.6, color=MUTED, va='center')
ax.set_xlim(0.1,5.4); ax.set_ylim(0.1,3.35); ax.axis('off')

t = np.linspace(0, 3, 700)
v = np.sin(2*np.pi*t)
bx.plot(t, v, color=MUTED, lw=1.0, ls=(0,(4,3)), label='input')
bx.plot(t, np.clip(v, 0, None), color=SERIES[0], lw=1.8, label='output')
bx.axhline(1/np.pi, color='#2e8b57', lw=1.1, ls=(0,(5,2)))
bx.text(3.03, 1/np.pi, '$V_m/π$', fontsize=8.4, color='#2e8b57', va='center')
bx.axhline(0, color=INK, lw=0.9)
bx.set_xlabel('time')
bx.set_xlim(0,3); bx.set_ylim(-1.25,1.45)
bx.set_xticks([]); bx.set_yticks([0,1]); bx.set_yticklabels(['0','$V_m$'])
bx.legend(loc='upper left', fontsize=7.6, ncol=2, columnspacing=1.0)
bx.spines[['top','right','bottom']].set_visible(False)
```
Half-wave rectification wastes half the input. A **full-wave rectifier** uses
both halves; there are two standard circuits.

```figure caption="Full-wave rectifiers. Left: centre-tap circuit — $D_1$ conducts on one half-cycle, $D_2$ on the other. Right: bridge circuit — $D_1D_3$ conduct on one half-cycle, $D_2D_4$ on the other; the load current flows the same way both times."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, (ax, bx) = plt.subplots(1, 2, figsize=(5.1,2.8))

def diode(a, px, py, ang, lab, lo):
    L = 0.34
    c, s = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    R = np.array([[c,-s],[s,c]])
    tri = np.array([[-L/2,-0.21],[-L/2,0.21],[L/2,0.0]]) @ R.T + np.array([px,py])
    a.fill(tri[:,0], tri[:,1], color=INK)
    b0 = np.array([[L/2,-0.23],[L/2,0.23]]) @ R.T + np.array([px,py])
    a.plot(b0[:,0], b0[:,1], color=INK, lw=2.0)
    a.text(px+lo[0], py+lo[1], lab, fontsize=8.2, color=INK, ha='center')

# ---- centre tap ----
ax.plot([0.30,0.30],[0.50,3.10], color=INK, lw=2.0)
ax.plot([0.62,0.62],[1.95,3.10], color=INK, lw=2.0)
ax.plot([0.62,0.62],[0.50,1.65], color=INK, lw=2.0)
ax.text(0.28,3.32,'a.c.', fontsize=8.0, color=INK, ha='center')
ax.plot([0.62,1.55],[3.10,3.10], color=INK, lw=1.2)
ax.plot([0.62,1.55],[0.50,0.50], color=INK, lw=1.2)
diode(ax, 1.80, 3.10, 0, '$D_1$', (0.0,0.30))
diode(ax, 1.80, 0.50, 0, '$D_2$', (0.0,-0.62))
ax.plot([2.05,3.90],[3.10,3.10], color=INK, lw=1.2)
ax.plot([2.05,3.90],[0.50,0.50], color=INK, lw=1.2)
ax.plot([3.90,3.90],[0.50,3.10], color=INK, lw=1.2)
ax.plot([0.62,3.12],[1.80,1.80], color=INK, lw=1.2)
ax.plot([3.68,3.90],[1.80,1.80], color=INK, lw=1.2)
ax.add_patch(Rectangle((3.12,1.52),0.56,0.56, fill=False, ec=INK, lw=1.2))
ax.text(3.40,2.22,'$R_L$', fontsize=9, color=INK, ha='center')
ax.text(1.05,1.62,'centre tap', fontsize=7.4, color=MUTED, ha='left')
ax.set_xlim(0.05,4.25); ax.set_ylim(-0.30,3.70); ax.axis('off')
ax.set_title('centre-tap', fontsize=8.8)

# ---- bridge (load drawn inside the diamond: no crossing wires) ----
bx.plot([0.32,0.32],[0.95,2.55], color=INK, lw=2.0)
bx.plot([0.60,0.60],[0.95,2.55], color=INK, lw=2.0)
bx.text(0.30,2.78,'a.c.', fontsize=8.0, color=INK, ha='center')
cx, cy, r = 2.00, 1.85, 0.85
L=(cx-r,cy); Rg=(cx+r,cy); T=(cx,cy+r); Bm=(cx,cy-r)
for a1,a2 in [(L,T),(T,Rg),(Bm,Rg),(L,Bm)]:
    bx.plot([a1[0],a2[0]],[a1[1],a2[1]], color=INK, lw=1.2)
diode(bx, cx-r/2, cy+r/2,  45, '$D_1$', (-0.30,0.12))
diode(bx, cx+r/2, cy+r/2, 135, '$D_2$', ( 0.32,0.12))
diode(bx, cx+r/2, cy-r/2,  45, '$D_3$', ( 0.32,-0.18))
diode(bx, cx-r/2, cy-r/2, 135, '$D_4$', (-0.30,-0.18))
bx.plot([0.60,0.85,0.85,L[0]],[2.55,2.55,1.85,1.85], color=INK, lw=1.2)
bx.plot([0.60,0.85,0.85,3.35,3.35,Rg[0]],[0.95,0.95,0.40,0.40,1.85,1.85],
        color=INK, lw=1.2)
bx.plot([cx,cx],[T[1],2.12], color=INK, lw=1.2)
bx.plot([cx,cx],[1.58,Bm[1]], color=INK, lw=1.2)
bx.add_patch(Rectangle((cx-0.18,1.58),0.36,0.54, fill=False, ec=INK, lw=1.2))
bx.text(cx-0.28,1.85,'$R_L$', fontsize=9, color=INK, va='center', ha='right')
bx.text(cx-0.12,T[1]+0.10,'+', fontsize=10, color=INK, ha='right')
bx.text(cx-0.12,Bm[1]-0.26,'–', fontsize=10, color=INK, ha='right')
bx.set_xlim(0.05,3.95); bx.set_ylim(-0.30,3.70); bx.axis('off')
bx.set_title('bridge', fontsize=8.8)
```
In the **centre-tap** circuit the transformer secondary is split by an earthed
centre tap, so the two halves always have opposite polarity. $D_1$ conducts while
its half is positive, $D_2$ while the other half is positive; in both cases the
current passes downward through $R_L$. In the **bridge** circuit no centre tap is
needed: the diagonally opposite pairs $D_1D_3$ and $D_2D_4$ conduct alternately,
again sending the current one way through the load.

::: derivation Mean current, rms current and efficiency
Write the load current on a conducting half-cycle as $i = I_m\sin\theta$. For a
full-wave rectifier the load carries current for the whole cycle, so averaging
over half a cycle is enough:

$$ I_{dc} = \frac{1}{\pi}\int_0^{\pi} I_m\sin\theta\, d\theta
= \frac{I_m}{\pi}\left[-\cos\theta\right]_0^{\pi} = \frac{2I_m}{\pi} $$

$$ I_{rms} = \sqrt{\frac{1}{\pi}\int_0^{\pi} I_m^{2}\sin^{2}\theta\, d\theta}
= \frac{I_m}{\sqrt{2}} $$

The rectification **efficiency** is the ratio of d.c. output power to a.c. input
power, with $r_f$ the forward resistance of the diode:

$$ \eta = \frac{I_{dc}^{2}R_L}{I_{rms}^{2}(R_L+r_f)}
= \frac{(2I_m/\pi)^{2}R_L}{(I_m/\sqrt{2})^{2}(R_L+r_f)}
= \frac{8}{\pi^{2}}\cdot\frac{R_L}{R_L+r_f} $$

For $r_f \ll R_L$ this gives $\eta = 8/\pi^{2} = 0.812$, i.e. **81.2%**. The same
working for a half-wave rectifier, averaging over the *whole* cycle, gives
$I_{dc}=I_m/\pi$, $I_{rms}=I_m/2$ and $\eta = 4/\pi^{2} = 40.6\%$.
:::

| Quantity | Half-wave | Full-wave |
|---|---|---|
| $I_{dc}$ | $I_m/\pi$ | $2I_m/\pi$ |
| $V_{dc}$ | $V_m/\pi$ | $2V_m/\pi$ |
| $I_{rms}$ | $I_m/2$ | $I_m/\sqrt{2}$ |
| Max efficiency | 40.6% | 81.2% |
| Ripple factor | 1.21 | 0.48 |
| Output frequency (50 Hz mains) | 50 Hz | 100 Hz |
| PIV per diode | $V_m$ | $2V_m$ (centre-tap), $V_m$ (bridge) |

The output is still lumpy. A **filter** — most simply a large capacitor across
the load — charges to the peak and discharges slowly between peaks, flattening
the ripple.

```figure caption="Full-wave output before and after a capacitor filter. Both halves of the input are used, so the output frequency is twice the input frequency and the mean value is $2V_m/\\pi$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.5))
t = np.linspace(0, 3, 1400)
v = np.abs(np.sin(2*np.pi*t))
ax.plot(t, np.sin(2*np.pi*t), color=MUTED, lw=0.9, ls=(0,(4,3)), label='input')
ax.plot(t, v, color=SERIES[0], lw=1.8, label='full-wave output')
# capacitor-filtered envelope
f = np.empty_like(v); hold = 0.0
for k, val in enumerate(v):
    hold = max(val, hold - 0.0016)
    f[k] = hold
ax.plot(t, f, color='#d9534f', lw=1.5, label='with filter capacitor')
ax.axhline(2/np.pi, color='#2e8b57', lw=1.1, ls=(0,(5,2)))
ax.text(3.03, 2/np.pi, '$2V_m/π$', fontsize=8.4, color='#2e8b57', va='center')
ax.axhline(0, color=INK, lw=0.9)
ax.set_xlabel('time'); ax.set_ylabel('$v_{out}$')
ax.set_xlim(0,3); ax.set_ylim(-1.2,1.5)
ax.set_xticks([]); ax.set_yticks([0,1]); ax.set_yticklabels(['0','$V_m$'])
ax.legend(loc='upper center', fontsize=7.6, ncol=3, columnspacing=0.9)
ax.spines[['top','right','bottom']].set_visible(False)
```

::: example Worked example 22.3
**Problem.** A centre-tap full-wave rectifier feeds a load of $500\ \Omega$. Each
half of the transformer secondary gives a peak voltage of $20\ \text{V}$. Taking
the diodes as ideal, find (a) the peak load current, (b) the d.c. load current
and d.c. output voltage, (c) the rms current, (d) the rectification efficiency,
(e) the peak inverse voltage across each diode, and (f) the output ripple
frequency for a 50 Hz supply.

**Solution.**

(a) $I_m = \dfrac{V_m}{R_L} = \dfrac{20}{500} = 0.040\ \text{A} = 40\ \text{mA}$.

(b) $I_{dc} = \dfrac{2I_m}{\pi} = \dfrac{2\times40}{3.142} = 25.5\ \text{mA}$, and

$$ V_{dc} = I_{dc}R_L = 25.5\times10^{-3}\times500 = 12.7\ \text{V}
\quad\left(=\frac{2V_m}{\pi} = \frac{40}{3.142}\right) $$

(c) $I_{rms} = \dfrac{I_m}{\sqrt{2}} = \dfrac{40}{1.414} = 28.3\ \text{mA}$.

(d) $\eta = \dfrac{I_{dc}^{2}}{I_{rms}^{2}} = \left(\dfrac{25.5}{28.3}\right)^{2}
= 0.812 = 81.2\%$ (diodes ideal, so $r_f = 0$).

(e) When one diode conducts, the other has the whole secondary across it:
$\text{PIV} = 2V_m = 40\ \text{V}$.

(f) Both half-cycles produce an output pulse, so the ripple frequency is
$2\times50 = 100\ \text{Hz}$.
:::

## 22.4 Logic gates: NOT, OR, AND, NAND and NOR

A **logic gate** is a circuit whose input and output voltages are restricted to
two levels, written 1 (high, typically $+5\ \text{V}$) and 0 (low, near
$0\ \text{V}$). Diodes and transistors make the gates; Boolean algebra describes
them.

| Gate | Boolean expression | Read as |
|---|---|---|
| NOT | $Y = \bar{A}$ | inverter |
| OR | $Y = A + B$ | A or B |
| AND | $Y = A\cdot B$ | A and B |
| NAND | $Y = \overline{A\cdot B}$ | AND then NOT |
| NOR | $Y = \overline{A+B}$ | OR then NOT |

The truth tables, which is what the board actually asks you to write:

| $A$ | $Y = \bar{A}$ |
|---|---|
| 0 | 1 |
| 1 | 0 |

| $A$ | $B$ | OR | AND | NAND | NOR |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 |

The NAND column is the AND column inverted, and NOR is OR inverted — that is all
the bar means.

::: memory Reading the tables in one line each
- **OR** — output 0 only when *all* inputs are 0.
- **AND** — output 1 only when *all* inputs are 1.
- **NAND** — output 0 only when *all* inputs are 1.
- **NOR** — output 1 only when *all* inputs are 0.
:::

**Universal gates.** NAND and NOR are called universal because every other gate
can be built from copies of just one of them. With NAND:

| Required gate | How to build it from NAND gates |
|---|---|
| NOT | tie both inputs of one NAND together: $\overline{A\cdot A} = \bar{A}$ |
| AND | a NAND followed by a NAND used as NOT |
| OR | invert both inputs with NANDs, then feed a third NAND: $\overline{\bar{A}\cdot\bar{B}} = A + B$ |

The last line is De Morgan's theorem. Check it: for $A=B=0$,
$\bar{A}\cdot\bar{B}=1$ and the output is 0; for every other combination
$\bar{A}\cdot\bar{B}=0$ and the output is 1 — exactly the OR column.

::: caution NAND is not "NOT then AND"
NAND means AND **then** NOT. Inverting first and then ANDing gives
$\bar{A}\cdot\bar{B}$, which is NOR, not NAND. Order matters.
:::

## 22.5 The junction transistor and its configurations

Two junctions back to back in one crystal make a **bipolar junction transistor**,
n-p-n or p-n-p. The **emitter** is heavily doped and supplies the carriers, the
**base** is very thin and lightly doped, the **collector** is the largest region.
In normal operation the emitter-base junction is **forward** biased and the
collector-base junction **reverse** biased, and because the base is thin over 95%
of the injected carriers sweep straight through to the collector:

$$ I_E = I_B + I_C, \qquad \alpha = \frac{I_C}{I_E}, \qquad
\beta = \frac{I_C}{I_B} = \frac{\alpha}{1-\alpha} $$

```figure caption="The three transistor configurations, drawn for an n-p-n transistor. The terminal common to the input and output loops gives each its name."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(5.1,2.5))

def npn(a):
    a.plot([0.45,1.00],[1.40,1.40], color=INK, lw=1.3)
    a.plot([1.00,1.00],[0.85,1.95], color=INK, lw=2.6)
    a.plot([1.00,1.62],[1.78,2.38], color=INK, lw=1.3)
    a.plot([1.62,1.62],[2.38,2.80], color=INK, lw=1.3)
    a.plot([1.00,1.62],[1.02,0.42], color=INK, lw=1.3)
    a.plot([1.62,1.62],[0.42,0.10], color=INK, lw=1.3)
    a.fill([1.38,1.52,1.28],[0.52,0.66,0.72], color=INK)
    a.text(0.92,1.62,'B', fontsize=8.4, color=INK, ha='right')
    a.text(1.72,2.62,'C', fontsize=8.4, color=INK)
    a.text(1.72,0.22,'E', fontsize=8.4, color=INK)
    return {'B':(0.45,1.40), 'C':(1.62,2.80), 'E':(1.62,0.10)}

def ground(a, x, y):
    a.plot([x,x],[y,y-0.20], color=INK, lw=1.2)
    for w, dy in [(0.24,0.20),(0.15,0.30),(0.07,0.40)]:
        a.plot([x-w,x+w],[y-dy,y-dy], color=INK, lw=1.2)

def port(a, xy, side, lab, col):
    x, y = xy
    if side == 'up':
        a.plot([x,x],[y,y+0.28], color=col, lw=1.4)
        a.annotate('', xy=(x+0.42,y+0.28), xytext=(x,y+0.28),
                   arrowprops=dict(arrowstyle='-|>', color=col, lw=1.4, mutation_scale=9))
        a.text(x+0.20,y+0.42,lab, fontsize=8.2, color=col, ha='center')
    elif side == 'down':
        a.plot([x,x],[y,y-0.28], color=col, lw=1.4)
        a.annotate('', xy=(x+0.42,y-0.28), xytext=(x,y-0.28),
                   arrowprops=dict(arrowstyle='-|>', color=col, lw=1.4, mutation_scale=9))
        a.text(x+0.22,y-0.62,lab, fontsize=8.2, color=col, ha='center')
    else:
        a.annotate('', xy=(x,y), xytext=(x-0.42,y),
                   arrowprops=dict(arrowstyle='-|>', color=col, lw=1.4, mutation_scale=9))
        a.text(x-0.24,y+0.14,lab, fontsize=8.2, color=col, ha='center')

IN, OUT = SERIES[0], SERIES[1]
cfg = [('common base', 'B', ('E','down'), ('C','up')),
       ('common emitter', 'E', ('B','left'), ('C','up')),
       ('common collector', 'C', ('B','left'), ('E','down'))]
for a, (ttl, com, (ipin, iside), (opin, oside)) in zip(axes, cfg):
    tm = npn(a)
    if com == 'B':
        a.plot([0.45,0.20,0.20],[1.40,1.40,1.10], color=INK, lw=1.3); ground(a,0.20,1.10)
    elif com == 'E':
        ground(a, 1.62, 0.10)
    else:
        a.plot([1.62,2.30,2.30],[2.80,2.80,1.30], color=INK, lw=1.3); ground(a,2.30,1.30)
    port(a, tm[ipin], iside, 'input', IN)
    port(a, tm[opin], oside, 'output', OUT)
    a.set_title(ttl, fontsize=8.5)
    a.set_xlim(-0.55,2.75); a.set_ylim(-0.75,3.60); a.axis('off')
```
| Configuration | Common terminal | Current gain | Voltage gain | Main use |
|---|---|---|---|---|
| Common base | base | $\alpha < 1$ | high | high-frequency amplifier |
| Common emitter | emitter | $\beta$, typically 20–500 | high | general-purpose amplifier, switch |
| Common collector | collector | $\approx \beta$ | $< 1$ | impedance matching (emitter follower) |

::: example Worked example 22.4
**Problem.** A transistor has $\alpha = 0.98$ and an emitter current of
$2.0\ \text{mA}$. Find the collector current, the base current and the current
gain $\beta$ in the common-emitter configuration.

**Solution.**

$$ I_C = \alpha I_E = 0.98 \times 2.0 = 1.96\ \text{mA} $$
$$ I_B = I_E - I_C = 2.0 - 1.96 = 0.04\ \text{mA} = 40\ \mu\text{A} $$
$$ \beta = \frac{I_C}{I_B} = \frac{1.96}{0.04} = 49
\quad\left(\text{check: } \frac{\alpha}{1-\alpha} = \frac{0.98}{0.02} = 49\right) $$
:::

## Chapter summary

- Diffusion across a p-n junction leaves a depletion region of immobile ions and
  a barrier potential $V_B$ (0.3 V Ge, 0.7 V Si) that stops further diffusion.
- Forward bias lowers the barrier, narrows the depletion layer and gives a large
  majority-carrier current; reverse bias does the opposite and leaves only a
  microamp reverse saturation current until breakdown.
- The diode characteristic is non-linear: no current below the knee voltage, then
  a steep rise. Dynamic resistance $r_d = \Delta V/\Delta I$.
- Half-wave: $I_{dc}=I_m/\pi$, $\eta_{max}=40.6\%$, ripple 1.21, output 50 Hz.
- Full-wave: $I_{dc}=2I_m/\pi$, $V_{dc}=2V_m/\pi$, $I_{rms}=I_m/\sqrt{2}$,
  $\eta = (8/\pi^{2})R_L/(R_L+r_f)$, maximum $81.2\%$, ripple 0.48, output 100 Hz.
- PIV is $V_m$ for half-wave and bridge, $2V_m$ for the centre-tap circuit.
- Gates: OR gives 0 only for all-zero inputs; AND gives 1 only for all-one
  inputs; NAND and NOR are their complements and are universal gates.
- Transistor: $I_E = I_B + I_C$, $\alpha = I_C/I_E$, $\beta = I_C/I_B = \alpha/(1-\alpha)$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. In a p-type semiconductor the majority charge carriers are <span class="marks">[1]</span>
   (a) electrons (b) holes (c) protons (d) positive ions
2. The barrier potential of a silicon p-n junction at room temperature is about <span class="marks">[1]</span>
   (a) 0.1 V (b) 0.3 V (c) 0.7 V (d) 1.4 V
3. The maximum efficiency of a full-wave rectifier is <span class="marks">[1]</span>
   (a) 40.6% (b) 50% (c) 81.2% (d) 100%
4. The peak inverse voltage across each diode of a centre-tap full-wave rectifier is <span class="marks">[1]</span>
   (a) $V_m$ (b) $2V_m$ (c) $V_m/2$ (d) $V_m/\pi$
5. A two-input NAND gate gives output 0 only when <span class="marks">[1]</span>
   (a) both inputs are 0 (b) both inputs are 1 (c) any one input is 1 (d) any one input is 0
6. For a transistor with $\alpha = 0.95$, the value of $\beta$ is <span class="marks">[1]</span>
   (a) 9.5 (b) 19 (c) 95 (d) 0.95

::: note Answers to Group A
**1.** (b) — trivalent dopants create holes.
**2.** (c) — 0.7 V for Si, 0.3 V for Ge.
**3.** (c) — $\eta_{max} = 8/\pi^{2} = 81.2\%$.
**4.** (b) — the non-conducting diode has the whole secondary across it.
**5.** (b) — NAND is AND inverted, and AND is 1 only for 1,1.
**6.** (b) — $\beta = \alpha/(1-\alpha) = 0.95/0.05 = 19$.
:::

**Group B — Short answer (5 marks each)**

1. Explain how the depletion region and barrier potential are formed at a p-n
   junction, and state what happens to each under forward and reverse bias. <span class="marks">[5]</span>
2. Draw the forward and reverse characteristic curves of a junction diode and
   explain the knee voltage, the reverse saturation current and breakdown. <span class="marks">[5]</span>
3. A silicon diode in series with a resistor $R$ is connected across a
   $9.0\ \text{V}$ battery in forward bias, and the current is $20\ \text{mA}$.
   Find $R$ and the power dissipated in the diode. <span class="marks">[5]</span>
4. A half-wave rectifier delivers current to a $300\ \Omega$ load from a supply of
   peak voltage $30\ \text{V}$. Taking the diode as ideal, find the peak current,
   the d.c. current, the d.c. output voltage and the PIV. <span class="marks">[5]</span>
5. Draw the truth tables of the NAND and NOR gates, and show how a NAND gate can
   be used as a NOT gate. <span class="marks">[5]</span>

::: note Answers to Group B
**3.** The diode drops $0.7\ \text{V}$, so the resistor has $9.0-0.7 = 8.3\ \text{V}$
across it and $R = 8.3/(20\times10^{-3}) = 415\ \Omega$. Power in the diode
$= 0.7\times20\times10^{-3} = 14\ \text{mW}$.

**4.** $I_m = V_m/R_L = 30/300 = 0.10\ \text{A}$;
$I_{dc} = I_m/\pi = 0.10/3.142 = 31.8\ \text{mA}$;
$V_{dc} = I_{dc}R_L = 31.8\times10^{-3}\times300 = 9.55\ \text{V}$ (which is
$V_m/\pi$); $\text{PIV} = V_m = 30\ \text{V}$.

**5.** Outline: write both truth tables from the tables in §22.4. Joining the two
inputs of a NAND gives $Y = \overline{A\cdot A} = \bar{A}$, which is NOT.
:::

**Group C — Long answer (8 marks each)**

1. (a) Draw the circuit of a centre-tap full-wave rectifier and explain its
   action over one complete cycle, sketching the input and output waveforms. <span class="marks">[4]</span>
   (b) Derive expressions for the d.c. current and the rectification efficiency,
   and hence show that the maximum efficiency is $81.2\%$. <span class="marks">[4]</span>
2. A bridge rectifier is supplied from a transformer whose secondary voltage is
   $24\ \text{V}$ rms. The load resistance is $1.0\ \text{k}\Omega$ and the diodes
   may be treated as ideal. Find (a) the peak voltage, (b) the peak current,
   (c) the d.c. output voltage and current, (d) the rms current, (e) the
   efficiency, and (f) the PIV of each diode. State one advantage of the bridge
   circuit over the centre-tap circuit. <span class="marks">[8]</span>

::: note Answer to Group C question 2
(a) $V_m = \sqrt{2}\times24 = 33.9\ \text{V}$.

(b) $I_m = V_m/R_L = 33.9/1000 = 33.9\ \text{mA}$.

(c) $V_{dc} = 2V_m/\pi = (2\times33.9)/3.142 = 21.6\ \text{V}$ and
$I_{dc} = V_{dc}/R_L = 21.6\ \text{mA}$.

(d) $I_{rms} = I_m/\sqrt{2} = 33.9/1.414 = 24.0\ \text{mA}$.

(e) $\eta = (I_{dc}/I_{rms})^{2} = (21.6/24.0)^{2} = 0.81 = 81\%$.

(f) For a bridge, $\text{PIV} = V_m = 33.9\ \text{V}$.

Advantage: no centre-tapped transformer is needed, and the PIV per diode is only
$V_m$ instead of $2V_m$, so cheaper diodes can be used for the same output.
:::
