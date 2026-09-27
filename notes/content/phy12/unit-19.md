---
subject: Physics
grade: 12
unit: 19
title: Alternating Currents
hours: 6
area: Electricity and Magnetism
---

The supply from the Nepal Electricity Authority is a sine wave of 230 V, 50 Hz —
its direction reverses one hundred times every second. With a steady current, a
circuit is described by one number, the resistance. With an alternating current,
a capacitor and an inductor also obstruct the flow, and they do it *out of step*
with the voltage. This unit gives you the tools for that: r.m.s. values, reactance,
phasors, impedance, resonance and the power factor.

::: key What the examiner wants here
Almost every paper contains a series LCR numerical — find $Z$, then $I$, then the
phase angle and the power. Group C asks you to *derive* the impedance from a
phasor diagram and then discuss resonance and the quality factor. Learn the two
mnemonics for phase (**CIVIL**: in a **C**apacitor **I** leads **V**, **V** leads
**I** in an **L**) and never add reactances to resistances arithmetically.
:::

## 19.1 Peak and rms value of AC current and voltage

An alternating current reverses direction periodically. The commonest form is
sinusoidal:

$$ i = I_0\sin\omega t, \qquad v = V_0\sin\omega t $$

where $I_0$ and $V_0$ are the **peak** (maximum or amplitude) values,
$\omega = 2\pi f$ is the angular frequency and $f = 1/T$.

The **average value over a full cycle is zero**, because the current spends half
the cycle positive and half negative. Averaging over half a cycle gives a useful
number:

$$ I_{av} = \frac{2I_0}{\pi} = 0.637\,I_0 $$

But the quantity that a meter reads, and the one that matters for heating, is the
**root-mean-square** value.

::: definition Root-mean-square value
The r.m.s. value of an alternating current is that steady direct current which
would produce the same heating effect in a given resistor in the same time.
:::

::: derivation $I_{rms} = I_0/\sqrt{2}$
The instantaneous power dissipated in a resistance $R$ is $p = i^{2}R$. Over one
period the mean square current is

$$ \overline{i^{2}} = \frac{1}{T}\int_0^{T} I_0^{2}\sin^{2}\omega t\,dt
= \frac{I_0^{2}}{T}\int_0^{T}\frac{1-\cos 2\omega t}{2}\,dt $$

The cosine averages to zero over a whole number of cycles, leaving

$$ \overline{i^{2}} = \frac{I_0^{2}}{2} \qquad\Longrightarrow\qquad
I_{rms} = \sqrt{\overline{i^{2}}} = \frac{I_0}{\sqrt{2}} = 0.707\,I_0 $$

The same argument for the voltage gives $V_{rms} = V_0/\sqrt{2}$.
:::

```figure caption="For $i = I_0\sin\omega t$ the square $i^2$ is always positive and averages to $I_0^2/2$; hence $I_{rms} = I_0/\sqrt{2} = 0.707\,I_0$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.8))
t = np.linspace(0, 2, 600)
i = np.sin(2*np.pi*t)
ax.plot(t, i, color=ACCENT, lw=2.0, label=r'$i = I_0\sin\omega t$')
ax.plot(t, i**2, color='#d9534f', lw=1.5, label=r'$i^2$')
ax.fill_between(t, 0, i**2, color='#d9534f', alpha=0.10)
ax.hlines(0.5, 0, 2.02, color='#d9534f', lw=1.1, ls=(0,(4,2)))
ax.hlines(0.7071, 0, 2.02, color='#0B6A62', lw=1.1, ls=(0,(2,2)))
ax.axhline(0, color=INK, lw=0.9)
ax.annotate('mean of $i^2$\n$= I_0^2/2$', (2.06, 0.46), va='center',
            color='#d9534f', fontsize=8.2)
ax.annotate('$I_{rms} = 0.707\\,I_0$', (2.06, 0.84), va='center',
            color='#0B6A62', fontsize=8.2)
ax.annotate('$I_0$', (0.25, 1.08), ha='center', color=ACCENT, fontsize=9.5)
ax.set_xlabel('time in periods  $t/T$'); ax.set_ylabel('normalised value')
ax.set_xlim(0,2.75); ax.set_ylim(-1.25,1.35)
ax.set_xticks([0,0.5,1.0,1.5,2.0])
ax.set_yticks([-1,-0.5,0,0.5,1])
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='lower left', fontsize=8.2, ncol=2)
```
| Quantity | Relation to peak value |
|---|---|
| r.m.s. value | $I_{rms} = I_0/\sqrt{2} = 0.707\,I_0$ |
| Mean over half cycle | $I_{av} = 2I_0/\pi = 0.637\,I_0$ |
| Mean over full cycle | $0$ |
| Form factor | $I_{rms}/I_{av} = 1.11$ |

::: caution 230 V is not the peak
A "230 V" supply is 230 V **r.m.s.** Its peak is
$V_0 = 230\sqrt{2} = 325\ \text{V}$, and insulation must withstand that. Unless a
question says "peak" or "maximum", every a.c. voltage and current quoted is an
r.m.s. value.
:::

::: example Worked example 19.1
**Problem.** An alternating current is given by
$i = 14.14\sin(314\,t)\ \text{A}$. Find (a) the peak value, (b) the r.m.s. value,
(c) the frequency and period, and (d) the mean value over half a cycle.

**Solution.** Comparing with $i = I_0\sin\omega t$: $I_0 = 14.14\ \text{A}$ and
$\omega = 314\ \text{rad s}^{-1}$.

(a) $I_0 = 14.14\ \text{A}$.

(b) $$ I_{rms} = \frac{I_0}{\sqrt{2}} = \frac{14.14}{1.414} = 10.0\ \text{A} $$

(c) $$ f = \frac{\omega}{2\pi} = \frac{314}{6.283} = 50\ \text{Hz}, \qquad T = \frac{1}{f} = 0.02\ \text{s} $$

(d) $$ I_{av} = \frac{2I_0}{\pi} = \frac{2\times14.14}{3.1416} = 9.0\ \text{A} $$
:::

## 19.2 AC through a resistor, a capacitor and an inductor

Take the applied voltage as $v = V_0\sin\omega t$ in each case.

**Pure resistor.** By Ohm's law the current follows the voltage instant by
instant:

$$ i = \frac{v}{R} = \frac{V_0}{R}\sin\omega t = I_0\sin\omega t $$

Current and voltage are **in phase**; the phase difference is zero and the
opposition is simply $R$.

**Pure inductor.** The only voltage in the circuit is the back e.m.f., so
$v = L\,di/dt$:

$$ di = \frac{V_0}{L}\sin\omega t\,dt \;\Longrightarrow\;
i = -\frac{V_0}{\omega L}\cos\omega t = \frac{V_0}{\omega L}\sin\left(\omega t - \frac{\pi}{2}\right) $$

So the current **lags** the voltage by $\pi/2$ (a quarter cycle), and the peak
current is $I_0 = V_0/\omega L$. The quantity

$$ X_L = \omega L = 2\pi f L $$

is the **inductive reactance**, measured in ohms. It is zero for d.c. ($f = 0$)
and grows with frequency — an inductor is a low-pass element, which is why a
**choke** controls a.c. without wasting energy.

**Pure capacitor.** The charge is $q = Cv = CV_0\sin\omega t$, so

$$ i = \frac{dq}{dt} = \omega CV_0\cos\omega t = \omega CV_0\sin\left(\omega t + \frac{\pi}{2}\right) $$

The current **leads** the voltage by $\pi/2$, with $I_0 = \omega CV_0$. The
quantity

$$ X_C = \frac{1}{\omega C} = \frac{1}{2\pi f C} $$

is the **capacitive reactance** in ohms. It is infinite for d.c. (a capacitor
blocks direct current) and falls as frequency rises.

```figure caption="Voltage and current waveforms. In $R$ they are in phase; in $L$ the current lags by $90^\circ$; in $C$ the current leads by $90^\circ$."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(5.1,2.3), sharey=True)
t = np.linspace(0, 2, 500)
v = np.sin(2*np.pi*t)
data = [('Resistor $R$', 0.0), ('Inductor $L$', -np.pi/2), ('Capacitor $C$', np.pi/2)]
for ax, (lab, ph) in zip(axes, data):
    ax.plot(t, v, color=MUTED, lw=1.5, ls=(0,(4,2)), label='$v$')
    ax.plot(t, 0.85*np.sin(2*np.pi*t + ph), color=ACCENT, lw=1.9, label='$i$')
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_title(lab, fontsize=8.6, color=INK, pad=4)
    ax.set_xlim(0,2); ax.set_ylim(-1.5,1.5)
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines[['top','right','bottom','left']].set_visible(False)
    ax.set_xlabel('t', fontsize=8.2)
axes[0].annotate('in phase', (1.0,-1.38), ha='center', color=INK, fontsize=8.0)
axes[1].annotate('i lags v by 90°', (1.0,-1.38), ha='center', color=INK, fontsize=8.0)
axes[2].annotate('i leads v by 90°', (1.0,-1.38), ha='center', color=INK, fontsize=8.0)
axes[2].legend(loc='upper right', fontsize=8.0, ncol=2, handlelength=1.3)
fig.subplots_adjust(wspace=0.08)
```

| Element | Opposition | Phase of $i$ relative to $v$ | Behaviour with $f$ |
|---|---|---|---|
| Resistor $R$ | $R$ (ohm) | in phase | independent of $f$ |
| Inductor $L$ | $X_L = 2\pi f L$ | lags by $90^{\circ}$ | increases with $f$ |
| Capacitor $C$ | $X_C = 1/2\pi f C$ | leads by $90^{\circ}$ | decreases with $f$ |

## 19.3 Phasor diagram

Adding sine functions of different phase by trigonometry is slow. Instead each
sinusoid is represented by a **phasor**: a rotating vector whose length is the
peak (or r.m.s.) value and which rotates anticlockwise with angular velocity
$\omega$. The projection of the phasor on the vertical axis gives the
instantaneous value.

Because every phasor in a circuit rotates at the same $\omega$, the *angles
between* them stay fixed, and the diagram can be drawn frozen at $t = 0$.
Sinusoids of the same frequency then add like vectors — by the parallelogram or
triangle rule.

```figure caption="Phasor diagrams, frozen at one instant; all phasors rotate anticlockwise at $\omega$. $V$ and $I$ are collinear for $R$ (drawn apart for clarity), $I$ is $90^\circ$ behind $V$ for $L$ and $90^\circ$ ahead for $C$."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(5.1,2.3))
cfg = [('Resistor', 0.0, 'I in phase with V'),
       ('Inductor', -90.0, 'I lags V by 90°'),
       ('Capacitor', 90.0, 'I leads V by 90°')]
for ax, (lab, ph, note) in zip(axes, cfg):
    dy = 0.10 if ph == 0 else 0.0
    ax.annotate('', xy=(1.00,dy), xytext=(0,dy),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.9, mutation_scale=13))
    ax.annotate('$V$', (1.05,dy+0.04), color=MUTED, fontsize=9.5, ha='left', va='bottom')
    r = np.radians(ph)
    ax.annotate('', xy=(0.85*np.cos(r), 0.85*np.sin(r)-dy), xytext=(0,-dy),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.9, mutation_scale=13))
    if ph == 0:
        ax.annotate('$I$', (0.90,-dy-0.04), color=ACCENT, fontsize=9.5,
                    ha='left', va='top')
    else:
        ax.annotate('$I$', (0.09, 0.86*np.sign(ph)), color=ACCENT, fontsize=9.5,
                    ha='left', va='center')
        arc = np.linspace(0, r, 40)
        ax.plot(0.42*np.cos(arc), 0.42*np.sin(arc), color='#d9534f', lw=1.0)
        ax.annotate('90°', (0.50*np.cos(r/2), 0.50*np.sin(r/2)), color='#d9534f',
                    fontsize=8.2, ha='left', va='center')
    ax.plot([0],[0],'o',color=INK,ms=3.2)
    ax.annotate(note, (0.10,-1.18), ha='center', color=INK, fontsize=8.0)
    ax.set_title(lab, fontsize=9.0, color=INK, pad=4)
    ax.set_xlim(-1.20,1.45); ax.set_ylim(-1.40,1.15)
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(wspace=0.05)
```
## 19.4 Series circuits containing combination of resistance, capacitance and inductance

In a series circuit the **current is the same everywhere**, so the current phasor
is drawn first and the three voltage phasors are set against it: $V_R$ along the
current, $V_L$ ahead of it by $90^{\circ}$ and $V_C$ behind it by $90^{\circ}$.
Since $V_L$ and $V_C$ are opposite, they subtract.

```figure caption="Series LCR circuit and its phasor diagram. $V_L$ and $V_C$ are antiparallel, so the resultant of $V_R$ and $(V_L - V_C)$ gives the supply voltage $V$ at phase angle $\phi$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, (axc, axp) = plt.subplots(1, 2, figsize=(5.1,2.6),
                               gridspec_kw={'width_ratios':[1.15,1.0]})
axc.plot([0.15,0.55],[1.6,1.6], color=INK, lw=1.2)
axc.add_patch(Rectangle((0.55,1.44), 0.55, 0.32, facecolor='none', edgecolor=INK, lw=1.2))
axc.annotate('R', (0.82,1.90), ha='center', color=INK, fontsize=9)
axc.plot([1.10,1.35],[1.6,1.6], color=INK, lw=1.2)
th = np.linspace(0, 4*np.pi, 200)
axc.plot(1.35+th/(4*np.pi)*0.55, 1.6+0.11*np.sin(th), color=INK, lw=1.2)
axc.annotate('L', (1.62,1.90), ha='center', color=INK, fontsize=9)
axc.plot([1.90,2.20],[1.6,1.6], color=INK, lw=1.2)
axc.plot([2.20,2.20],[1.44,1.76], color=INK, lw=1.4)
axc.plot([2.33,2.33],[1.44,1.76], color=INK, lw=1.4)
axc.annotate('C', (2.27,1.90), ha='center', color=INK, fontsize=9)
axc.plot([2.33,2.75,2.75,1.65],[1.6,1.6,0.55,0.55], color=INK, lw=1.2)
axc.plot([1.25,0.15,0.15],[0.55,0.55,1.6], color=INK, lw=1.2)
from matplotlib.patches import Circle
axc.add_patch(Circle((1.45,0.55), 0.20, facecolor='none', edgecolor=INK, lw=1.2))
sw = np.linspace(-np.pi, np.pi, 60)
axc.plot(1.45+sw*0.042, 0.55+0.075*np.sin(sw), color=INK, lw=1.1)
axc.annotate('$V = V_0\\sin\\omega t$', (1.45,0.12), ha='center', color=INK, fontsize=8.6)
axc.annotate('I', (0.72,0.72), ha='center', color=ACCENT, fontsize=9.5)
axc.annotate('', xy=(0.92,0.55), xytext=(0.52,0.55),
             arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3, mutation_scale=11))
axc.set_xlim(-0.10,2.95); axc.set_ylim(-0.10,2.25)
axc.set_aspect('equal'); axc.axis('off')
VR, VL, VC = 1.32, 2.64, 0.88
s = 0.42
VR, VL, VC = VR*s, VL*s, VC*s
axp.annotate('', xy=(VR,0), xytext=(0,0),
             arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.8, mutation_scale=13))
axp.annotate('$V_R = IR$', (VR*0.5,-0.13), ha='center', va='top', color='#0B6A62', fontsize=8.6)
axp.annotate('', xy=(0,VL), xytext=(0,0),
             arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.8, mutation_scale=13))
axp.annotate('$V_L$', (-0.07,VL*0.72), ha='right', color='#d9534f', fontsize=9.5)
axp.annotate('', xy=(0,-VC), xytext=(0,0),
             arrowprops=dict(arrowstyle='-|>', color='#b8860b', lw=1.8, mutation_scale=13))
axp.annotate('$V_C$', (-0.07,-VC*0.62), ha='right', color='#b8860b', fontsize=9.5)
axp.annotate('', xy=(VR,VL-VC), xytext=(VR,0),
             arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.4,
                             linestyle=(0,(3,2)), mutation_scale=11))
axp.annotate('$V_L-V_C$', (VR+0.06,(VL-VC)*0.55), color=MUTED, fontsize=8.6)
axp.annotate('', xy=(VR,VL-VC), xytext=(0,0),
             arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=2.0, mutation_scale=13))
axp.annotate('$V$', (VR*0.42,(VL-VC)*0.62), ha='right', color=ACCENT, fontsize=10)
arc = np.linspace(0, np.arctan2(VL-VC, VR), 40)
axp.plot(0.22*np.cos(arc), 0.22*np.sin(arc), color=INK, lw=1.0)
axp.annotate(r'$\phi$', (0.27,0.09), color=INK, fontsize=9.5)
axp.annotate('$I$', (VR+0.16,0), va='center', color='#0B6A62', fontsize=9.5)
axp.set_xlim(-0.42,1.05); axp.set_ylim(-0.60,1.30)
axp.set_aspect('equal'); axp.axis('off')
```

::: derivation Impedance of a series LCR circuit
Let the common current be $I$ (r.m.s.). The three voltage magnitudes are

$$ V_R = IR, \qquad V_L = IX_L, \qquad V_C = IX_C $$

$V_L$ and $V_C$ are in antiphase, so their resultant has magnitude
$|V_L - V_C|$ and is perpendicular to $V_R$. By Pythagoras,

$$ V = \sqrt{V_R^{2} + (V_L-V_C)^{2}} = I\sqrt{R^{2}+(X_L-X_C)^{2}} $$

Hence the **impedance** $Z = V/I$ is

$$ Z = \sqrt{R^{2}+\left(\omega L - \frac{1}{\omega C}\right)^{2}} $$

and the current lags the voltage by the **phase angle** $\phi$ where

$$ \tan\phi = \frac{V_L-V_C}{V_R} = \frac{X_L-X_C}{R} $$
:::

- If $X_L > X_C$: $\phi > 0$, the circuit is **inductive** and the current lags.
- If $X_L < X_C$: $\phi < 0$, the circuit is **capacitive** and the current leads.
- If $X_L = X_C$: $\phi = 0$, the circuit behaves as pure resistance — resonance.

Dropping one element gives the special cases $Z = \sqrt{R^2+X_L^2}$ for an LR
circuit and $Z = \sqrt{R^2+X_C^2}$ for a CR circuit.

::: caution Never add $R$, $X_L$ and $X_C$ arithmetically
$Z \ne R + X_L + X_C$. Resistance and reactance are at right angles on the phasor
diagram, so they combine by Pythagoras. In the same way the voltmeter readings
$V_R$, $V_L$ and $V_C$ do not add up to the supply voltage — $V_L$ alone can be
far larger than $V$.
:::

::: example Worked example 19.2
**Problem.** A resistor of $30\ \Omega$, an inductor of $0.191\ \text{H}$ and a
capacitor of $159\ \mu\text{F}$ are connected in series across a
$220\ \text{V}$, $50\ \text{Hz}$ supply. Find the reactances, the impedance, the
current, the phase angle, and the voltage across each element.

**Solution.** $\omega = 2\pi f = 2\pi(50) = 314.2\ \text{rad s}^{-1}$.

$$ X_L = \omega L = 314.2\times0.191 = 60\ \Omega $$
$$ X_C = \frac{1}{\omega C} = \frac{1}{314.2\times159\times10^{-6}} = 20\ \Omega $$
$$ Z = \sqrt{R^{2}+(X_L-X_C)^{2}} = \sqrt{30^{2}+40^{2}} = \sqrt{2500} = 50\ \Omega $$
$$ I = \frac{V}{Z} = \frac{220}{50} = 4.4\ \text{A} $$
$$ \tan\phi = \frac{X_L-X_C}{R} = \frac{40}{30} = 1.333 \;\Rightarrow\; \phi = 53.1^{\circ} $$

Since $X_L > X_C$ the current **lags** the voltage by $53.1^{\circ}$.

$$ V_R = IR = 4.4\times30 = 132\ \text{V}, \quad V_L = 4.4\times60 = 264\ \text{V},
\quad V_C = 4.4\times20 = 88\ \text{V} $$

Check: $\sqrt{132^{2}+(264-88)^{2}} = \sqrt{17424+30976} = \sqrt{48400} = 220\ \text{V}$.
Note that $V_L$ alone exceeds the supply voltage.
:::

## 19.5 Series resonance; quality factor

::: definition Series resonance
A series LCR circuit is in resonance when the inductive and capacitive reactances
are equal, so that the impedance is a minimum ($Z = R$), the current is a maximum
($I_{\max} = V/R$) and the current is exactly in phase with the applied voltage.
:::

Setting $X_L = X_C$:

$$ \omega_0 L = \frac{1}{\omega_0 C} \;\Longrightarrow\; \omega_0 = \frac{1}{\sqrt{LC}}
\qquad\text{and}\qquad f_0 = \frac{1}{2\pi\sqrt{LC}} $$

At resonance the circuit behaves as a pure resistance and draws maximum power.
Because a large current flows, the voltages across $L$ and $C$ can be very much
larger than the supply — they are equal and opposite and cancel each other. For
this reason the series resonant circuit is called an **acceptor** circuit, and it
is used to tune a radio receiver to one station.

```figure caption="Resonance curves for a series LCR circuit. A smaller $R$ gives a taller, sharper peak — a higher quality factor $Q$ and a narrower bandwidth."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
L, C, V = 2.0, 32e-6, 220.0
f = np.linspace(15, 26, 1400)
w = 2*np.pi*f
f0 = 1/(2*np.pi*np.sqrt(L*C))
for R, c, lab in [(10.0, SERIES[0], r'$R = 10\ \Omega$  ($Q = 25$)'),
                  (20.0, SERIES[1], r'$R = 20\ \Omega$  ($Q = 12.5$)'),
                  (40.0, SERIES[2], r'$R = 40\ \Omega$  ($Q = 6.3$)')]:
    Z = np.sqrt(R**2 + (w*L - 1/(w*C))**2)
    ax.plot(f, V/Z, color=c, lw=1.9, label=lab)
R = 10.0
Z = np.sqrt(R**2 + (w*L - 1/(w*C))**2)
half = (V/R)/np.sqrt(2)
sel = V/Z >= half
f1, f2 = f[sel][0], f[sel][-1]
ax.annotate('', xy=(f1,half), xytext=(f2,half),
            arrowprops=dict(arrowstyle='<->', color=INK, lw=1.1, mutation_scale=9))
ax.hlines(half, 15, f1, color=MUTED, lw=0.9, ls=(0,(3,2)))
ax.annotate('$I_{max}/\\sqrt{2}$', (15.3, half+0.8), color=MUTED, fontsize=8.2)
ax.annotate('bandwidth Δf', (f2+0.35, half), va='center', ha='left',
            color=INK, fontsize=8.4)
ax.axvline(f0, color=MUTED, lw=0.9, ls=':')
ax.annotate('$f_0$', (f0+0.15, 0.8), ha='left', color=INK, fontsize=9.5)
ax.set_xlabel('frequency  $f$  (Hz)'); ax.set_ylabel('current  $I$  (A)')
ax.set_xlim(15,26); ax.set_ylim(0,25)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.5)
ax.legend(loc='upper right', fontsize=8.2)
```
The **sharpness** of the peak is measured by the **quality factor**:

$$ Q = \frac{\omega_0 L}{R} = \frac{1}{\omega_0 CR} = \frac{1}{R}\sqrt{\frac{L}{C}}
= \frac{f_0}{\Delta f} $$

where the **bandwidth** $\Delta f = f_2 - f_1$ is the range of frequencies over
which the current stays above $I_{\max}/\sqrt{2}$. Equivalently, $Q$ is the factor
by which the voltage across $L$ (or $C$) at resonance exceeds the supply voltage:
$Q = V_L/V$. A large $Q$ means a sharp, selective circuit.

::: example Worked example 19.3
**Problem.** A series circuit has $L = 2.0\ \text{H}$, $C = 32\ \mu\text{F}$ and
$R = 10\ \Omega$, connected to a $220\ \text{V}$ variable-frequency supply. Find
(a) the resonant angular frequency and frequency, (b) the current at resonance,
(c) the quality factor, (d) the voltage across the inductor at resonance, and
(e) the bandwidth.

**Solution.**

(a) $$ \omega_0 = \frac{1}{\sqrt{LC}} = \frac{1}{\sqrt{2.0\times32\times10^{-6}}}
= \frac{1}{8.0\times10^{-3}} = 125\ \text{rad s}^{-1} $$
$$ f_0 = \frac{\omega_0}{2\pi} = \frac{125}{6.283} = 19.9\ \text{Hz} $$

(b) At resonance $Z = R$, so $$ I = \frac{V}{R} = \frac{220}{10} = 22\ \text{A} $$

(c) $$ Q = \frac{\omega_0 L}{R} = \frac{125\times2.0}{10} = 25 $$

(d) $$ V_L = IX_L = I\omega_0L = 22\times125\times2.0 = 5500\ \text{V} $$

The capacitor voltage is $V_C = I/\omega_0C = 22/(125\times32\times10^{-6}) = 5500\ \text{V}$
as well — equal and opposite, so they cancel. Note
$V_L/V = 5500/220 = 25 = Q$, as expected.

(e) $$ \Delta f = \frac{f_0}{Q} = \frac{19.9}{25} = 0.80\ \text{Hz} $$
:::

## 19.6 Power in AC circuits: power factor

::: derivation Average power and the power factor
With $v = V_0\sin\omega t$ and $i = I_0\sin(\omega t - \phi)$, the instantaneous
power is

$$ p = vi = V_0I_0\sin\omega t\,\sin(\omega t-\phi) $$

Using $2\sin A\sin B = \cos(A-B) - \cos(A+B)$,

$$ p = \frac{V_0I_0}{2}\left[\cos\phi - \cos(2\omega t-\phi)\right] $$

Averaged over a complete cycle the second term vanishes, so

$$ P_{av} = \frac{V_0I_0}{2}\cos\phi = \frac{V_0}{\sqrt{2}}\cdot\frac{I_0}{\sqrt{2}}\cos\phi
= V_{rms}I_{rms}\cos\phi $$
:::

The factor $\cos\phi$ is the **power factor** of the circuit:

$$ \cos\phi = \frac{R}{Z} = \frac{\text{true power}}{\text{apparent power}} $$

The product $V_{rms}I_{rms}$ is the **apparent power**, measured in volt-ampere
(VA); $P_{av}$ is the **true power** in watts.

| Circuit | $\phi$ | Power factor | Average power |
|---|---|---|---|
| Pure resistance | $0$ | $1$ | $V_{rms}I_{rms}$ |
| Pure inductance | $-90^{\circ}$ | $0$ | zero |
| Pure capacitance | $+90^{\circ}$ | $0$ | zero |
| Series LCR | $\tan^{-1}\frac{X_L-X_C}{R}$ | $R/Z$ | $V_{rms}I_{rms}\cos\phi$ |
| LCR at resonance | $0$ | $1$ | $V^{2}/R$ |

A current that flows with $\cos\phi = 0$ delivers no net energy at all: energy is
stored in the field for a quarter cycle and returned in the next. This is called
**wattless current**, and it is why a choke coil is preferred to a rheostat for
controlling a.c. — the choke limits current without dissipating heat.

Industries are charged for apparent power, so a low power factor is expensive. A
factory in Balaju with many induction motors (inductive load, $\cos\phi$ perhaps
$0.6$) connects large capacitors in parallel to cancel the lagging current and
push the power factor towards 1.

::: example Worked example 19.4
**Problem.** A coil connected to a $200\ \text{V}$, $50\ \text{Hz}$ supply draws
a current of $5.0\ \text{A}$ and consumes $600\ \text{W}$. Find its impedance,
resistance, inductive reactance, inductance and power factor. What capacitance in
series would make the power factor unity?

**Solution.**

$$ Z = \frac{V}{I} = \frac{200}{5.0} = 40\ \Omega $$

True power $P = I^{2}R$, so

$$ R = \frac{P}{I^{2}} = \frac{600}{25} = 24\ \Omega $$
$$ X_L = \sqrt{Z^{2}-R^{2}} = \sqrt{1600-576} = \sqrt{1024} = 32\ \Omega $$
$$ L = \frac{X_L}{2\pi f} = \frac{32}{314.2} = 0.102\ \text{H} $$
$$ \cos\phi = \frac{R}{Z} = \frac{24}{40} = 0.60 \quad\text{(lagging)} $$

For unity power factor we need $X_C = X_L = 32\ \Omega$:

$$ C = \frac{1}{2\pi f X_C} = \frac{1}{314.2\times32} = 9.95\times10^{-5}\ \text{F} \approx 100\ \mu\text{F} $$
:::

## Chapter summary

- For $i = I_0\sin\omega t$: $I_{rms} = I_0/\sqrt{2} = 0.707I_0$,
  $I_{av}$ (half cycle) $= 2I_0/\pi = 0.637I_0$, and the full-cycle mean is zero.
  Meters read r.m.s.
- Resistor: $i$ in phase with $v$. Inductor: $i$ lags by $90^{\circ}$,
  $X_L = 2\pi fL$. Capacitor: $i$ leads by $90^{\circ}$, $X_C = 1/2\pi fC$.
- A phasor is a vector of length equal to the peak (or r.m.s.) value, rotating at
  $\omega$; sinusoids of the same frequency add like vectors.
- Series LCR: $Z = \sqrt{R^{2}+(X_L-X_C)^{2}}$ and $\tan\phi = (X_L-X_C)/R$;
  $V = \sqrt{V_R^{2}+(V_L-V_C)^{2}}$.
- Resonance: $X_L = X_C$, so $f_0 = 1/2\pi\sqrt{LC}$, $Z_{\min} = R$,
  $I_{\max} = V/R$ and $\phi = 0$ (acceptor circuit).
- Quality factor $Q = \omega_0L/R = (1/R)\sqrt{L/C} = f_0/\Delta f = V_L/V$; a
  large $Q$ means a sharp resonance and a narrow bandwidth.
- Power: $P_{av} = V_{rms}I_{rms}\cos\phi$, with power factor
  $\cos\phi = R/Z$. Pure $L$ or $C$ consumes no power — wattless current.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The r.m.s. value of the current $i = I_0\sin\omega t$ is <span class="marks">[1]</span>
   (a) $I_0$ (b) $I_0/2$ (c) $I_0/\sqrt{2}$ (d) $2I_0/\pi$
2. In a purely capacitive a.c. circuit, the current <span class="marks">[1]</span>
   (a) is in phase with the voltage (b) leads the voltage by $90^{\circ}$
   (c) lags the voltage by $90^{\circ}$ (d) leads by $45^{\circ}$
3. At series resonance the impedance of an LCR circuit is <span class="marks">[1]</span>
   (a) maximum and equal to $X_L$ (b) zero (c) minimum and equal to $R$ (d) equal to $X_L+X_C$
4. The average power consumed in one cycle by a pure inductor is <span class="marks">[1]</span>
   (a) $V_{rms}I_{rms}$ (b) $V_{rms}I_{rms}/2$ (c) $V_0I_0$ (d) zero
5. The quality factor of a series resonant circuit is <span class="marks">[1]</span>
   (a) $R/\omega_0L$ (b) $\omega_0L/R$ (c) $\omega_0 CR$ (d) $\Delta f/f_0$

::: note Answers to Group A
**1.** (c) — the mean of $\sin^2\omega t$ over a cycle is $\frac12$.
**2.** (b) — $i = \omega CV_0\sin(\omega t+\pi/2)$.
**3.** (c) — $X_L - X_C = 0$, so $Z = \sqrt{R^2+0} = R$.
**4.** (d) — $\phi = 90^{\circ}$, so $\cos\phi = 0$ and energy is only stored and returned.
**5.** (b) — equivalently $1/\omega_0CR$ or $f_0/\Delta f$.
:::

**Group B — Short answer (5 marks each)**

1. Define the r.m.s. value of an alternating current and show that
   $I_{rms} = I_0/\sqrt{2}$ for a sinusoidal current. <span class="marks">[5]</span>
2. Derive an expression for the current when an alternating voltage
   $V_0\sin\omega t$ is applied to a pure inductor. Show that the current lags the
   voltage by $\pi/2$ and define inductive reactance. <span class="marks">[5]</span>
3. A $100\ \Omega$ resistor, a $0.50\ \text{H}$ inductor and a $10\ \mu\text{F}$
   capacitor are joined in series across a $200\ \text{V}$, $50\ \text{Hz}$
   supply. Calculate the impedance and the current. <span class="marks">[5]</span>
4. What is meant by the power factor of an a.c. circuit? Explain what is meant by
   a wattless current, and state why a choke coil is preferred to a resistor for
   controlling alternating current. <span class="marks">[5]</span>
5. A series circuit has $L = 0.50\ \text{H}$, $C = 20\ \mu\text{F}$ and
   $R = 10\ \Omega$. Find the resonant frequency and the quality factor. <span class="marks">[5]</span>

::: note Answers to Group B
**3.** $\omega = 314.2\ \text{rad s}^{-1}$. $X_L = 314.2\times0.50 = 157.1\ \Omega$;
$X_C = 1/(314.2\times10\times10^{-6}) = 318.3\ \Omega$. So
$X_L - X_C = -161.2\ \Omega$ and

$$ Z = \sqrt{100^{2}+161.2^{2}} = \sqrt{10000+25995} = 189.7\ \Omega $$
$$ I = \frac{200}{189.7} = 1.05\ \text{A} $$

The circuit is capacitive, so the current leads the voltage.

**4.** Outline: the power factor is $\cos\phi = R/Z$ = true power / apparent
power. A wattless (idle) current is one flowing at $\cos\phi = 0$, as in a pure
$L$ or $C$: energy is stored for a quarter cycle and returned in the next, so the
net power over a cycle is zero. A choke limits the current by its reactance
$X_L$, which consumes no power, whereas a resistor would waste the same energy as
heat.

**5.** $$ f_0 = \frac{1}{2\pi\sqrt{LC}} = \frac{1}{2\pi\sqrt{0.50\times20\times10^{-6}}}
= \frac{1}{2\pi(3.162\times10^{-3})} = 50.3\ \text{Hz} $$

$\omega_0 = 1/\sqrt{LC} = 1/(3.162\times10^{-3}) = 316.2\ \text{rad s}^{-1}$, so

$$ Q = \frac{\omega_0L}{R} = \frac{316.2\times0.50}{10} = 15.8 $$
:::

**Group C — Long answer (8 marks each)**

1. (a) Draw the phasor diagram for a series LCR circuit carrying an alternating
   current and hence derive expressions for its impedance and the phase angle
   between the current and the applied voltage. <span class="marks">[4]</span>
   (b) What is series resonance? Obtain an expression for the resonant frequency,
   sketch the variation of current with frequency for two different resistances,
   and define the quality factor. <span class="marks">[4]</span>
2. An inductor of $0.20\ \text{H}$ with negligible resistance, a
   $100\ \Omega$ resistor and a $50\ \mu\text{F}$ capacitor are connected in
   series across a $220\ \text{V}$, $50\ \text{Hz}$ supply. Calculate
   (a) the impedance, (b) the current, (c) the phase angle, (d) the power factor
   and (e) the power dissipated. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** Outline: (a) draw $I$ along the reference direction with $V_R$ along $I$,
$V_L$ at $+90^{\circ}$ and $V_C$ at $-90^{\circ}$; the resultant gives
$V = I\sqrt{R^2+(X_L-X_C)^2}$, so $Z = \sqrt{R^2+(X_L-X_C)^2}$ and
$\tan\phi = (X_L-X_C)/R$. (b) Resonance is the condition $X_L = X_C$, giving
$f_0 = 1/2\pi\sqrt{LC}$, $Z = R$ and $I_{\max} = V/R$; sketch the curves of §19.5
showing a sharper peak for smaller $R$; $Q = \omega_0L/R = f_0/\Delta f$.

**2.** $\omega = 2\pi(50) = 314.2\ \text{rad s}^{-1}$.

$$ X_L = 314.2\times0.20 = 62.8\ \Omega, \qquad
X_C = \frac{1}{314.2\times50\times10^{-6}} = 63.66\ \Omega $$

(a) $X_L - X_C = 62.8 - 63.7 = -0.83\ \Omega$, so

$$ Z = \sqrt{100^{2}+(0.83)^{2}} = 100.0\ \Omega $$

(b) $I = 220/100.0 = 2.2\ \text{A}$.

(c) $\tan\phi = -0.83/100 = -0.0083$, so $\phi = -0.48^{\circ}$ — the current leads
very slightly, because the supply is almost exactly at the resonant frequency
($f_0 = 1/2\pi\sqrt{0.20\times50\times10^{-6}} = 50.3\ \text{Hz}$).

(d) $\cos\phi = R/Z = 100/100.0 \approx 1.00$.

(e) $P = I^{2}R = (2.2)^{2}\times100 = 484\ \text{W}$.
:::
