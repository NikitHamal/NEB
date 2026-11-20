---
subject: Physics
grade: IOE
unit: 5
title: Electricity and Magnetism
hours: 7
area: Physics
---

Electricity and magnetism carry about **7 questions**, second only to mechanics. Seven sub-areas share them: electrostatics and capacitors, DC circuits, thermoelectricity, magnetic force and fields, magnetic materials, induction, and AC. Most numerical questions are a single formula; Section B ones chain two (a cell with internal resistance, an RLC power factor, a charge in a magnetic field).

::: key What the paper asks from this chapter
- Coulomb $F=\frac{kq_1q_2}{r^2}$, field and potential of a point charge, Gauss's law, field of sphere / sheet / line.
- Capacitors: $C=\frac{\varepsilon_0A}{d}$, series $\frac{1}{C}=\sum\frac{1}{C_i}$, parallel $\sum C_i$, $U=\frac{1}{2}CV^2$, dielectric $K$.
- DC: $R=\rho\frac{l}{A}$, $P=I^2R=\frac{V^2}{R}$, internal resistance $V=\varepsilon-Ir$, Kirchhoff, Wheatstone, shunt and multiplier.
- Magnetism: $F=qvB\sin\theta$, $F=BIl$, torque $NIAB$, Biot–Savart, solenoid $\mu_0nI$, wires $\frac{\mu_0I_1I_2}{2\pi d}$, Hall effect.
- Induction: $\varepsilon=-N\frac{d\Phi}{dt}$, motional emf $Blv$, $L$, $M$, $U=\frac{1}{2}LI^2$, transformer.
- AC: $I_{rms}=\frac{I_0}{\sqrt{2}}$, $X_L=\omega L$, $X_C=\frac{1}{\omega C}$, $Z$, resonance $f=\frac{1}{2\pi\sqrt{LC}}$, $\cos\phi=\frac{R}{Z}$.
:::

## 5.1 Electrostatics

**Coulomb's law:** $F=\dfrac{1}{4\pi\varepsilon_0}\dfrac{q_1q_2}{r^2}$, $k=9\times10^9$ N m² C⁻²; in a medium divide by $\varepsilon_r$. Two charges of 1 µC at 1 m: $9\times10^{-3}$ N. **Electric field** $E=\frac{F}{q}=\frac{kQ}{r^2}$ (lines start on positive charges, never cross, are perpendicular to conductors' surfaces); between plates $E=\frac{V}{d}$. **Dipole:** $p=qd$; torque $pE\sin\theta$; energy $-pE\cos\theta$; axial field $\frac{2kp}{r^3}$, equatorial $\frac{kp}{r^3}$.

**Gauss's law:** $\oint\vec E\cdot d\vec A=\frac{q_{enc}}{\varepsilon_0}$. Results: infinite line $\frac{\lambda}{2\pi\varepsilon_0r}$; infinite sheet $\frac{\sigma}{2\varepsilon_0}$; conductor surface $\frac{\sigma}{\varepsilon_0}$; charged sphere outside $\frac{kQ}{r^2}$, inside a conductor 0, inside a uniformly charged solid sphere $\frac{kQr}{R^3}$.

**Potential** $V=\frac{kQ}{r}$ (scalar; adds algebraically); $E=-\frac{dV}{dr}$; work $W=q(V_A-V_B)$; potential energy of two charges $\frac{kq_1q_2}{r}$; equipotential surfaces are perpendicular to field lines. 1 eV $=1.6\times10^{-19}$ J. Point-charge zero field between like charges $4\mu$C and $1\mu$C 30 cm apart is at 20 cm from the larger one.

**Capacitors.** $C=\frac{Q}{V}$; parallel plate $C=\frac{\varepsilon_0A}{d}$ (with a dielectric $K\frac{\varepsilon_0A}{d}$); sphere $4\pi\varepsilon_0R$; cylindrical, spherical shells. Series: $\frac{1}{C}=\frac{1}{C_1}+\frac{1}{C_2}$, same charge; parallel: $C=C_1+C_2$, same voltage. Energy $U=\frac{1}{2}CV^2=\frac{Q^2}{2C}=\frac{1}{2}QV$; energy density $\frac{1}{2}\varepsilon_0E^2$. **Dielectric** (inserted with the battery off): $C\to KC$, $V\to\frac{V}{K}$, $E\to\frac{E}{K}$, $Q$ constant, $U\to\frac{U}{K}$; (battery on: $V$ same, $Q\to KQ$). Polarisation reduces the field inside the dielectric; displacement $D=\varepsilon E$. Types: paper, mica, electrolytic (polarised), variable. Sharing charge between capacitors: common $V=\frac{C_1V_1+C_2V_2}{C_1+C_2}$, with an energy loss.

## 5.2 DC circuits

**Ohm's law** $V=IR$; **resistivity** $R=\rho\frac{l}{A}$ ($\rho$ rises with $T$ for metals, falls for semiconductors); drift velocity $v_d=\frac{I}{nAe}$; conductivity $\sigma=\frac{1}{\rho}$. $R_t=R_0(1+\alpha t)$. Series $R=\sum R_i$; parallel $\frac{1}{R}=\sum\frac{1}{R_i}$ (6 Ω ∥ 3 Ω = 2 Ω). **Power** $P=VI=I^2R=\frac{V^2}{R}$; a 100 W, 220 V bulb has $R=484\ \Omega$ and, on 110 V, gives 25 W. Energy $=Pt$; $H=I^2Rt$ (**Joule's law**).

**Cell:** $\varepsilon=V+Ir$; current $I=\frac{\varepsilon}{R+r}$; terminal voltage $V=\varepsilon-Ir$ (cell of 2 V, $r=0.5$ Ω, $R=4.5$ Ω: 1.8 V). Maximum power transfer when $R=r$. Series of $n$ cells $n\varepsilon$, $nr$; parallel $\varepsilon$, $\frac{r}{n}$.

**Kirchhoff:** junction rule $\sum I=0$ (charge conservation); loop rule $\sum\varepsilon=\sum IR$ (energy). **Wheatstone bridge** balances when $\frac{P}{Q}=\frac{R}{S}$. **Meter bridge**, **potentiometer** (compare emfs, $\frac{\varepsilon_1}{\varepsilon_2}=\frac{l_1}{l_2}$; measures without drawing current). **Galvanometer** (moving coil, $\theta\propto I$): ammeter by a parallel **shunt** $S=\frac{I_gG}{I-I_g}$; voltmeter by a series **multiplier** $R=\frac{V}{I}_g-G$; an ideal ammeter has zero resistance, an ideal voltmeter infinite. **Ohmmeter** uses a cell with the galvanometer and a series resistor (zero at right end).

## 5.3 Thermoelectric effect

**Seebeck effect:** a loop of two different metals with junctions at different temperatures carries an emf, $\varepsilon=aT+\frac{1}{2}bT^2$ (a **thermocouple**). The neutral temperature is where $\frac{d\varepsilon}{dT}=0$, the inversion temperature is $2T_n-T_c$. A **thermopile** (several couples in series) detects small radiation. **Peltier effect:** current through a junction absorbs or releases heat ($\Pi$), the reverse of Seebeck; it makes thermoelectric coolers. **Thomson effect:** heat is absorbed or released along a single conductor with a temperature gradient. Applications: thermometry of very high and low temperatures, refrigeration.

## 5.4 Magnetic effect of current

**Force on a charge:** $\vec F=q\vec v\times\vec B$ (no work done); in a perpendicular field the path is a circle of radius $r=\frac{mv}{qB}$, period $T=\frac{2\pi m}{qB}$ (independent of speed: the cyclotron); with $\vec E$ also: Lorentz $q(\vec E+\vec v\times\vec B)$. A proton at $10^6$ m s⁻¹ in 0.1 T: $r\approx10$ cm. **Force on a conductor:** $F=BIl\sin\theta$. **Torque on a coil:** $\tau=NIAB\sin\theta$ (moving-coil galvanometer); magnetic moment $m=NIA$. **Hall effect:** $V_H=\frac{BI}{nqt}$ gives the sign and density of the carriers and measures $B$.

**Biot–Savart:** $dB=\frac{\mu_0}{4\pi}\frac{I\,dl\sin\theta}{r^2}$, $\mu_0=4\pi\times10^{-7}$ T m A⁻¹. Long straight wire $B=\frac{\mu_0I}{2\pi r}$ (5 A at 0.1 m: $10^{-5}$ T); centre of a circular loop $\frac{\mu_0NI}{2R}$; on the axis $\frac{\mu_0IR^2}{2(R^2+x^2)^{3/2}}$; solenoid $B=\mu_0nI$ ($n$ turns per metre), toroid $\frac{\mu_0NI}{2\pi r}$. **Ampère's law:** $\oint\vec B\cdot d\vec l=\mu_0I_{enc}$. **Parallel wires:** force per length $\frac{\mu_0I_1I_2}{2\pi d}$, attractive for currents in the same direction (defines the ampere). 10 A and 20 A at 10 cm: $4\times10^{-4}$ N m⁻¹.

## 5.5 Magnetic properties of matter

**Earth's magnetism:** declination, dip (inclination) $\delta$, horizontal component $B_H$; $\tan\delta=\frac{B_V}{B_H}$; dip is 0 at the magnetic equator and $90^\circ$ at the poles. **Materials:** diamagnetic ($\chi$ small negative, weakly repelled: Bi, Cu, water); paramagnetic ($\chi$ small positive, $\chi\propto\frac{1}{T}$ Curie: Al, Pt); ferromagnetic ($\chi$ large positive, domains, lose ferromagnetism above the Curie temperature: Fe, Co, Ni). $\mu=\mu_0\mu_r$, $\mu_r=1+\chi$, $B=\mu_0(H+M)$. **Hysteresis:** the $B$–$H$ loop; retentivity, coercivity; the **loop area is the energy lost per cycle per volume**. Soft iron (narrow loop, low retentivity) is for transformer cores and electromagnets; steel (wide loop) for permanent magnets.

## 5.6 Electromagnetic induction

**Faraday:** $\varepsilon=-N\frac{d\Phi}{dt}$, $\Phi=BA\cos\theta$ (weber); **Lenz's law** (the sign: the induced current opposes the change; conservation of energy). **Motional emf** $\varepsilon=Blv$ (a rod of 0.5 m at 4 m s⁻¹ in 0.2 T: 0.4 V); rotating rod $\frac{1}{2}B\omega l^2$. Induced charge $\frac{\Delta\Phi}{R}$. Eddy currents (braking, induction furnace, laminated cores to reduce them).

**AC generator:** coil of $N$ turns, area $A$, rotating at $\omega$: $\varepsilon=NBA\omega\sin\omega t$. **Self-inductance** $\varepsilon=-L\frac{dI}{dt}$, $\Phi=LI$; solenoid $L=\mu_0n^2Al$; energy $U=\frac{1}{2}LI^2$ (2 H, 0 to 5 A in 0.1 s: emf 100 V, energy 25 J). **Mutual inductance** $\varepsilon_2=-M\frac{dI_1}{dt}$. **Transformer** (ideal): $\frac{V_s}{V_p}=\frac{N_s}{N_p}=\frac{I_p}{I_s}$; step-up raises voltage and lowers current; losses: copper, iron (eddy, hysteresis), flux leakage; efficiency $\frac{P_s}{P_p}$. High-voltage transmission lowers $I^2R$ loss.

## 5.7 Alternating currents

$I=I_0\sin\omega t$; $I_{rms}=\frac{I_0}{\sqrt{2}}=0.707I_0$ (220 V mains has a peak of 311 V; Nepal's supply is 220 V, 50 Hz); mean value over a half cycle $\frac{2I_0}{\pi}$. **Reactances** $X_L=\omega L$ (the voltage leads current by $90^\circ$), $X_C=\frac{1}{\omega C}$ (the voltage lags by $90^\circ$); resistor in phase. **Series LCR:** $Z=\sqrt{R^2+(X_L-X_C)^2}$, $\tan\phi=\frac{X_L-X_C}{R}$. Resonance at $\omega_0=\frac{1}{\sqrt{LC}}$ ($L=1$ mH, $C=1\,\mu$F: 5 kHz): $Z=R$, current maximum, phase zero. **Quality factor** $Q=\frac{\omega_0L}{R}=\frac{1}{R}\sqrt{\frac{L}{C}}$ (sharpness of resonance). **Power** $P=V_{rms}I_{rms}\cos\phi$; **power factor** $\cos\phi=\frac{R}{Z}$ (R = 30 Ω, $X_L=60$, $X_C=20$: $Z=50$, $\cos\phi=0.6$); a pure L or C draws no average power (wattless current). Choke coil lowers current with little loss; the LC circuit oscillates with $f=\frac{1}{2\pi\sqrt{LC}}$.

::: caution Electromagnetism traps
Potential is a scalar and field a vector; when charges are shared, charge is conserved but energy is not. A dielectric inserted with the battery *disconnected* lowers $V$; with it *connected* raises $Q$. In AC problems use rms values unless asked for the peak. The voltage rating of a ceramic capacitor is its limit; the force between parallel wires is attractive for *parallel* currents.
:::

```photogrid label="5.1" cols="2" ratio="1.2" caption="Why a Van de Graaff generator has a big smooth sphere. (a) A demonstration generator: charge carried up a belt spreads over the outside of the hollow sphere, and the visitor's hair stands up because every strand gets the same sign of charge. (b) Dry air breaks down when the field at the surface reaches about $3\\times10^{6}$ V per m. Since $E = V/R$ at the surface of a sphere, the largest potential is $V = 3\\times10^{6}R$, and the charge that holds it is $Q = 4\\pi\\varepsilon_0 R V$. Computed for three radii."
@ photo id="ioephy/vdg" cap="A Van de Graaff generator at a science museum"
fit 1.2
focus 0.5 0.5
@ svg cap="Largest potential before air sparks"
import math
k = 8.99e9; Emax = 3e6
rows = []
for R in (0.10, 0.15, 0.25):
    V = Emax * R; Q = V * R / k; rows.append((R, V, Q))
assert abs(rows[1][1] - 450e3) < 1 and abs(rows[1][2] * 1e6 - 7.5) < 0.05
f = Fig(300, 236)
f.text(150, 14, "dry air limit E = 3 MV/m", size=10.5, color=NAVY, bold=True)
for i, (R, V, Q) in enumerate(rows):
    y = 34 + i * 48; w = 200 * V / 750e3
    f.text(8, y, "radius %d cm" % round(R * 100), size=10.5, color=TEAL, bold=True, anchor="start")
    f.box(8, y + 6, w, 20, "", fill=MINT, stroke=TEAL, r=3, sw=1)
    f.text(min(w + 14, 214), y + 16, "%d kV" % round(V / 1000), size=10.5, color=NAVY if w > 200 else TEAL, bold=True, anchor="start", vmid=True)
    f.text(292, y, "Q = %.1f µC" % (Q * 1e6), size=10.5, color=SLATE, anchor="end")
f.text(150, 192, "V = E R,  Q = V R / k,  k = 8.99e9", size=10.5, color=SLATE)
f.text(150, 212, "doubling R doubles V and quadruples Q", size=10.5, color=AMBER, bold=True)
assert abs(rows[2][2] / rows[0][2] - 6.25) < 1e-6
f.text(150, 230, "sharp points leak charge: use a smooth sphere", size=10.5, color=RED, bold=True)
```

## Formula and fact sheet

| Topic | Result |
|---|---|
| Coulomb | $9\times10^9\frac{q_1q_2}{r^2}$ |
| $E$, $V$ (point) | $\frac{kQ}{r^2}$, $\frac{kQ}{r}$ |
| capacitor | $\frac{\varepsilon_0A}{d}$; $U=\frac{1}{2}CV^2$ |
| internal resistance | $V=\varepsilon-Ir$ |
| shunt | $\frac{I_gG}{I-I_g}$ |
| wire / solenoid | $\frac{\mu_0I}{2\pi r}$ / $\mu_0nI$ |
| Lorentz radius | $\frac{mv}{qB}$ |
| emf | $N\frac{d\Phi}{dt}$; $Blv$ |
| transformer | $\frac{V_s}{V_p}=\frac{N_s}{N_p}$ |
| RLC | $Z=\sqrt{R^2+(X_L-X_C)^2}$; $\cos\phi=\frac{R}{Z}$ |

## Chapter summary

- $E=\frac{kQ}{r^2}$, $V=\frac{kQ}{r}$; Gauss's law gives symmetric fields.
- Series capacitors share charge; parallel share voltage; energy $\frac{1}{2}CV^2$.
- Terminal voltage is $\varepsilon-Ir$; shunts go in parallel, multipliers in series.
- Moving charges in $B$ go in circles; parallel currents attract.
- Para-, dia- and ferro-magnetism differ in sign and size of $\chi$.
- Induced emf opposes the change (Lenz); transformers trade voltage for current.
- RLC: $Z$, resonance at $\frac{1}{2\pi\sqrt{LC}}$ and power factor $\frac{R}{Z}$.

## Practice questions

**Set A — Recall (12 questions)**

1. The force between two 1 µC charges 1 m apart in air is
   (a) 9 N (b) 1 N (c) $9\times10^{-3}$ N (d) $9\times10^{-6}$ N
2. Capacitors of 2 µF and 3 µF connected in series have a combined capacitance of
   (a) 1.2 µF (b) 5 µF (c) 1.5 µF (d) 6 µF
3. The energy stored in a 10 µF capacitor charged to 100 V is
   (a) 0.5 J (b) 5 J (c) 0.5 mJ (d) 0.05 J
4. The equivalent resistance of 6 Ω and 3 Ω in parallel is
   (a) 9 Ω (b) 2 Ω (c) 3 Ω (d) 4.5 Ω
5. The resistance of a 220 V, 100 W bulb is
   (a) 484 Ω (b) 2.2 Ω (c) 22000 Ω (d) 220 Ω
6. The magnetic field 0.1 m from a long straight wire carrying 5 A is
   (a) $10^{-6}$ T (b) $10^{-4}$ T (c) $10^{-5}$ T (d) $2\times10^{-6}$ T
7. A 0.5 m conductor carrying 4 A is perpendicular to a 0.2 T field. The force on it is
   (a) 0.1 N (b) 0.8 N (c) 1.6 N (d) 0.4 N
8. A coil of 100 turns has its flux changed by 0.01 Wb in 0.1 s. The induced emf is
   (a) 1 V (b) 10 V (c) 100 V (d) 0.1 V
9. A transformer has 100 primary and 1000 secondary turns; 220 V is applied to the primary. The secondary voltage is
   (a) 2200 V (b) 22 V (c) 22000 V (d) 220 V
10. The rms value of an AC of peak voltage 311 V is nearly
    (a) 311 V (b) 440 V (c) 220 V (d) 155 V
11. The resonant frequency of a series LC circuit with $L=1$ mH and $C=1\ \mu$F is nearly
    (a) 159 Hz (b) 1 kHz (c) 31.6 kHz (d) 5033 Hz
12. A material with a small positive magnetic susceptibility is
    (a) diamagnetic (b) paramagnetic (c) ferromagnetic (d) superconducting

::: note Answers and explanations — Set A
**1.** (c) — $9\times10^9\times10^{-12}/1$.
**2.** (a) — $\frac{2\times3}{2+3}=1.2$.
**3.** (d) — $\frac{1}{2}\times10^{-5}\times10^4=0.05$ J.
**4.** (b) — $\frac{6\times3}{9}=2$.
**5.** (a) — $R=\frac{V^2}{P}=\frac{48400}{100}$.
**6.** (c) — $\frac{\mu_0I}{2\pi r}=\frac{2\times10^{-7}\times5}{0.1}$.
**7.** (d) — $BIl=0.2\times4\times0.5$.
**8.** (b) — $N\frac{\Delta\Phi}{\Delta t}=100\times0.1$.
**9.** (a) — $220\times\frac{1000}{100}$.
**10.** (c) — $\frac{311}{\sqrt{2}}$.
**11.** (d) — $\frac{1}{2\pi\sqrt{10^{-9}}}=5033$ Hz.
**12.** (b) — paramagnetic; diamagnetic $\chi<0$, ferromagnetic $\chi\gg1$.
:::

**Set B — Understanding (8 questions)**

1. Charges $+4\ \mu$C and $+1\ \mu$C are 30 cm apart. The electric field is zero on the line between them at a distance from the $4\ \mu$C charge of
   (a) 10 cm (b) 15 cm (c) 25 cm (d) 20 cm
2. The potential at a distance of 0.9 m from a 2 µC point charge is
   (a) $2\times10^4$ V (b) $2\times10^3$ V (c) $2\times10^5$ V (d) $1.8\times10^4$ V
3. A parallel-plate capacitor has plate area 100 cm² and separation 1 mm in air ($\varepsilon_0=8.85\times10^{-12}$). Its capacitance is
   (a) 8.85 pF (b) 88.5 pF (c) 885 pF (d) 8.85 nF
4. A cell of emf 2 V and internal resistance 0.5 Ω is connected to a 4.5 Ω resistor. The terminal voltage is
   (a) 2.0 V (b) 1.6 V (c) 1.8 V (d) 0.2 V
5. A galvanometer of 100 Ω and full-scale current 1 mA is to read 1 A. The shunt needed is about
   (a) 0.1 Ω (b) 1 Ω (c) 10 Ω (d) 100 Ω
6. A coil of 50 turns, area 0.02 m² carries 2 A in a 0.5 T field. The maximum torque is
   (a) 0.5 N m (b) 2 N m (c) 10 N m (d) 1 N m
7. A 2 H inductor's current rises from 0 to 5 A in 0.1 s. The average induced emf is
   (a) 10 V (b) 100 V (c) 50 V (d) 200 V
8. In a series circuit $R=30\ \Omega$, $X_L=60\ \Omega$, $X_C=20\ \Omega$. The power factor is
   (a) 0.8 (b) 0.5 (c) 0.6 (d) 1

::: note Answers and explanations — Set B
**1.** (d) — $\frac{x}{0.3-x}=\sqrt{\frac{4}{1}}=2$, $x=0.2$ m.
**2.** (a) — $\frac{9\times10^9\times2\times10^{-6}}{0.9}$.
**3.** (b) — $\frac{8.85\times10^{-12}\times10^{-2}}{10^{-3}}=8.85\times10^{-11}$ F.
**4.** (c) — $I=\frac{2}{5}=0.4$ A; $V=2-0.4\times0.5=1.8$ V.
**5.** (a) — $S=\frac{0.001\times100}{0.999}\approx0.1\ \Omega$.
**6.** (d) — $NIAB=50\times2\times0.02\times0.5$.
**7.** (b) — $L\frac{\Delta I}{\Delta t}=2\times50$.
**8.** (c) — $Z=\sqrt{30^2+40^2}=50$; $\cos\phi=\frac{30}{50}$.
:::

**Set C — Application (6 questions)**

1. A 100 W, 220 V lamp is run on 110 V. Its power is
   (a) 50 W (b) 100 W (c) 12.5 W (d) 25 W
2. In a balanced Wheatstone bridge $P=10\ \Omega$, $Q=20\ \Omega$, $R=30\ \Omega$. The fourth arm $S$ is
   (a) 15 Ω (b) 40 Ω (c) 60 Ω (d) 20 Ω
3. Two long parallel wires 10 cm apart carry 10 A and 20 A in the same direction. The force per unit length is
   (a) $4\times10^{-4}$ N m⁻¹, attractive (b) $4\times10^{-4}$ N m⁻¹, repulsive (c) $2\times10^{-4}$ N m⁻¹, attractive (d) $4\times10^{-5}$ N m⁻¹, attractive
4. A proton ($m=1.67\times10^{-27}$ kg) moves at $10^6$ m s⁻¹ perpendicular to a 0.1 T field. The radius of its path is nearly
   (a) 1 cm (b) 10 cm (c) 1 m (d) 0.1 mm
5. A series RLC circuit has $R=10\ \Omega$, $L=0.1$ H and $C=100\ \mu$F. Its quality factor is nearly
   (a) 31.6 (b) 316 (c) 3.16 (d) 0.316
6. A 0.5 m rod moves at 4 m s⁻¹ perpendicular to a 0.2 T field. The emf across its ends is
   (a) 0.1 V (b) 4 V (c) 0.8 V (d) 0.4 V

::: note Answers and explanations — Set C
**1.** (d) — $P\propto V^2$, $\frac{1}{4}\times100$.
**2.** (c) — $\frac{P}{Q}=\frac{R}{S}$: $S=\frac{RQ}{P}=60$.
**3.** (a) — $\frac{2\times10^{-7}\times10\times20}{0.1}=4\times10^{-4}$; same-direction currents attract.
**4.** (b) — $r=\frac{mv}{qB}=\frac{1.67\times10^{-27}\times10^6}{1.6\times10^{-19}\times0.1}=0.104$ m.
**5.** (c) — $\omega_0=316$ rad s⁻¹, $Q=\frac{\omega_0L}{R}=\frac{31.6}{10}$.
**6.** (d) — $Blv=0.2\times0.5\times4$.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. State Coulomb's law, define electric field and potential, and explain capacitors in series and parallel with the energy stored. <span class="marks">[10]</span>
2. State Kirchhoff's laws; explain internal resistance, the Wheatstone bridge and the potentiometer, with numericals. <span class="marks">[10]</span>
3. Explain electromagnetic induction, the transformer and the series LCR circuit with resonance and power factor. <span class="marks">[10]</span>

```photogrid label="5.H" cols="5" ratio="1.1" caption="Electricity and magnetism. (a) Capacitors store charge and energy. (b) A transformer changes AC voltage by electromagnetic induction. (c) A Van de Graaff generator builds up a very high potential. (d) A galvanometer detects small currents through the torque on a coil. (e) Lightning is a natural electrostatic discharge."
@ photo id="ceephy/capacitors" cap="(a) Capacitors"
fit 1.1
focus 0.5 0.5
@ photo id="phy12b/transformer" cap="(b) Transformer"
fit 1.1
focus 0.5 0.5
@ photo id="ioephy/vdg" cap="(c) Van de Graaff"
fit 1.1
focus 0.5 0.5
@ photo id="phy12/galvanometer" cap="(d) Galvanometer"
fit 1.1
focus 0.5 0.5
@ photo id="phy12b/lightning" cap="(e) Lightning"
fit 1.1
focus 0.5 0.5
```

### Model answer D1: Electrostatics and capacitors (10 marks)

**Introduction.** **Coulomb's law:** the force between two point charges in vacuum is $F = \frac{1}{4\pi\varepsilon_0}\frac{q_1q_2}{r^2}$, along the line joining them, with $\frac{1}{4\pi\varepsilon_0} = 9\times10^9\ \text{N m}^2\text{C}^{-2}$. For $2\ \mu\text{C}$ and $3\ \mu\text{C}$ at $0.3\ \text{m}$: $F = 9\times10^9\times\frac{6\times10^{-12}}{0.09} = 0.6\ \text{N}$.

**Field and potential.**

1. **Electric field** $E = F/q_0 = \frac{kQ}{r^2}$ (unit N C⁻¹ or V m⁻¹).
2. **Potential** $V = \frac{kQ}{r}$ (a scalar); $E = -\frac{dV}{dr}$.
3. **Gauss's law:** $\oint E\cdot dA = \frac{Q}{\varepsilon_0}$; inside a charged conducting sphere the field is zero.
4. **Potential energy** of two charges $U = \frac{kq_1q_2}{r}$.

**Capacitor.** $C = \frac{Q}{V}$; a parallel-plate capacitor has $C = \frac{\varepsilon_0A}{d}$, and a dielectric of constant $K$ multiplies it by $K$.

| Arrangement | Equivalent capacitance | Charge and voltage |
|---|---|---|
| Series | $\frac{1}{C} = \frac{1}{C_1} + \frac{1}{C_2}$ | Same $Q$, voltages add |
| Parallel | $C = C_1 + C_2$ | Same $V$, charges add |

For $4\ \mu\text{F}$ and $12\ \mu\text{F}$: series $= \frac{4\times12}{16} = 3\ \mu\text{F}$ and parallel $= 16\ \mu\text{F}$.

**Energy stored.** $U = \frac{1}{2}CV^2 = \frac{Q^2}{2C} = \frac{1}{2}QV$. For the $3\ \mu\text{F}$ combination charged to $12\ \text{V}$: $U = \frac{1}{2}\times3\times10^{-6}\times144 = 216\ \mu\text{J}$. The energy density is $\frac{1}{2}\varepsilon_0E^2$.

**Conclusion.** Charges create fields and potentials, and capacitors store energy in the field between their plates.

### Model answer D2: DC circuits (10 marks)

**Introduction.** Ohm's law ($V = IR$) is not enough for a network, so Kirchhoff's laws are used.

**Kirchhoff's laws.**

1. **Junction (current) law:** the sum of currents entering a junction equals the sum leaving ($\sum I = 0$), which expresses conservation of charge.
2. **Loop (voltage) law:** around a closed loop $\sum E = \sum IR$, which expresses conservation of energy.

**Internal resistance.** A cell of emf $E$ and internal resistance $r$ gives $I = \frac{E}{R + r}$ and a terminal voltage $V = E - Ir$. For $E = 12\ \text{V}$, $r = 1\ \Omega$, $R = 5\ \Omega$: $I = 2\ \text{A}$ and $V = 10\ \text{V}$. Maximum power goes to the load when $R = r$.

**Wheatstone bridge.** Four resistances $P, Q, R, S$ are balanced when no current flows in the galvanometer: $\frac{P}{Q} = \frac{R}{S}$. For $P = 10\ \Omega$, $Q = 15\ \Omega$, $R = 20\ \Omega$: $S = \frac{RQ}{P} = 30\ \Omega$. The **meter bridge** is the practical form, using $S = R\,\frac{100 - l}{l}$.

**Potentiometer.** A long uniform wire carries a steady current. A cell is balanced at length $l$ where the potential difference equals its emf, so no current is drawn. Uses: (a) **compare emfs** $\frac{E_1}{E_2} = \frac{l_1}{l_2}$; (b) find the internal resistance $r = R\left(\frac{l_1}{l_2} - 1\right)$. It is more accurate than a voltmeter.

**Series and parallel.** Series: $R = R_1 + R_2$; parallel: $\frac{1}{R} = \frac{1}{R_1} + \frac{1}{R_2}$.

| Instrument | Principle | Advantage |
|---|---|---|
| Wheatstone bridge | Balanced ratio | Accurate $R$ |
| Potentiometer | Null deflection | No current drawn from the cell |
| Voltmeter | Deflection | Draws some current |

**Conclusion.** Kirchhoff's laws solve any network, and null-deflection methods give accurate measurements.

### Model answer D3: Electromagnetic induction, transformer and AC circuits (10 marks)

**Introduction.** **Faraday's law:** the induced emf is $E = -\frac{d\Phi}{dt}$, and **Lenz's law** (the minus sign) says that the induced current opposes the change that produces it, so energy is conserved.

**Transformer.** It has primary and secondary coils on a soft-iron core, and works only with AC. $\frac{V_s}{V_p} = \frac{N_s}{N_p} = \frac{I_p}{I_s}$ (ideal). A step-down transformer from $11{,}000\ \text{V}$ to $230\ \text{V}$ has turns ratio $\frac{11000}{230} = 47.8$. Losses: copper loss, eddy currents (laminated core), hysteresis and flux leakage.

**Series LCR circuit.** The reactances are $X_L = \omega L$ and $X_C = \frac{1}{\omega C}$, so $Z = \sqrt{R^2 + (X_L - X_C)^2}$ and $\tan\phi = \frac{X_L - X_C}{R}$. **Numerical:** $R = 40\ \Omega$, $L = 0.2\ \text{H}$, $C = 100\ \mu\text{F}$, $230\ \text{V}$, $50\ \text{Hz}$.

| Quantity | Working | Value |
|---|---|---|
| $X_L$ | $2\pi\times50\times0.2$ | $62.8\ \Omega$ |
| $X_C$ | $\frac{1}{2\pi\times50\times10^{-4}}$ | $31.8\ \Omega$ |
| $Z$ | $\sqrt{40^2 + 31.0^2}$ | $50.6\ \Omega$ |
| $I_{rms}$ | $230/50.6$ | $4.54\ \text{A}$ |
| Phase angle | $\tan^{-1}(31.0/40)$ | $37.8^\circ$ (voltage leads) |
| Power factor | $R/Z$ | $0.79$ |
| Power | $VI\cos\phi = I^2R$ | $826\ \text{W}$ |

**Resonance.** When $X_L = X_C$, $Z = R$ (minimum), the current is maximum and the power factor is 1. The resonant frequency is $f_0 = \frac{1}{2\pi\sqrt{LC}}$; here $f_0 = 35.6\ \text{Hz}$. This is how a radio is tuned to a station.

**Conclusion.** Changing flux induces emf, transformers use it to change voltage, and in an AC circuit the average power depends on the power factor.
