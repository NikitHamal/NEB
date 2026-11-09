"""Shared answer blocks, part B: oscillators, current sources, power amplifiers, regulators."""
import math

U = {}

U['barkhausen'] = r'''
**Barkhausen criteria.** An amplifier with gain A and a feedback network with feedback factor β (positive feedback) sustains oscillation at a frequency f$_o$ if the loop gain Aβ satisfies

$$\begin{gathered}
|A\beta|=1 \quad(\text{magnitude condition: the loop gain is unity}) \\
\angle A\beta = 0^\circ\ \text{or}\ 360^\circ\quad(\text{phase condition: total phase shift around the loop is zero})
\end{gathered}$$

The closed-loop gain A$_f$ = A/(1 − Aβ) becomes infinite, so an output exists without any input. Oscillations start from noise when |Aβ| is slightly greater than 1 initially; the amplitude then limits (non-linearity or an amplitude-stabilising element) so that |Aβ| settles at 1.
'''

U['rc_vs_lc'] = r'''
| RC oscillators | LC oscillators |
|---|---|
| Frequency determined by resistors and capacitors, f = 1/(2πRC) (times a constant) | Frequency determined by an inductor-capacitor tank, f = 1/(2π√(LC)) |
| Used for **audio and low frequencies** (a few Hz up to about 1 MHz): function generators, audio signal sources | Used for **radio frequencies** (100 kHz to hundreds of MHz): RF carriers in transmitters, local oscillators in receivers |
| Inductors are not needed, so they are small, cheap and easy to integrate | Bulky inductors, but high Q and good frequency stability at RF |
| Phase-shift, Wien bridge | Hartley, Colpitts, Clapp (crystal for best stability) |
'''

U['wien'] = r'''
**Wien bridge oscillator.** A non-inverting op-amp amplifier (gain A$_v$ = 1 + R$_f$/R$_1$) is combined with a **lead-lag network** (series R–C in series arm, parallel R–C in shunt arm) which gives the positive feedback to the non-inverting input. The resistor divider R$_f$, R$_1$ gives the negative feedback that sets the gain.

<<fig:wien>>

Let Z$_s$ = R + 1/(jωC) and Z$_p$ = R/(1 + jωRC) (R∥C). The feedback factor of the lead-lag network is

$$\beta=\frac{Z_p}{Z_s+Z_p}=\frac{1}{3+j\left(\omega RC-\dfrac{1}{\omega RC}\right)}$$

The phase of β is zero when the imaginary part vanishes, ωRC = 1/(ωRC), that is at

$$\omega_o=\frac{1}{RC}\ \ \Rightarrow\ \ f_o=\frac{1}{2\pi RC},\qquad |\beta|=\frac13\ \ \text{at}\ f_o$$

The amplifier gives no phase shift, so the phase condition holds at f$_o$. The magnitude condition |Aβ| ≥ 1 requires

$$A_v=1+\frac{R_f}{R_1}\ \ge\ 3\ \ \Rightarrow\ \ R_f\ge 2R_1$$

In practice R$_f$ is made slightly larger than 2R$_1$ (or a lamp/thermistor/diode limiter is used in R$_f$) so that oscillation starts and the amplitude is then stabilised at A$_v$ = 3. *Example:* R = 10 kΩ, C = 16 nF gives f$_o$ = 1/(2π × 10 k × 16 n) = 995 Hz ≈ 1 kHz with R$_1$ = 10 kΩ, R$_f$ ≈ 20 kΩ+.
'''

U['rcphase'] = r'''
**RC phase-shift oscillator.** An inverting amplifier (phase shift 180°) is followed by a feedback network of **three identical RC sections** which supplies a further 180° (60° per section) at one frequency, so the total phase around the loop is 360°.

<<fig:rcphase>>

For the three-section network (op-amp virtual ground at the end, the last R is the input resistor) the analysis of the loop equations gives the transfer function

$$\frac{v_f}{v_o}=\frac{1}{1-5\alpha^2-j(6\alpha-\alpha^3)},\qquad \alpha=\frac{1}{\omega RC}$$

The phase shift is 180° when the imaginary part is zero: 6α − α³ = 0, so α² = 6:

$$f_o=\frac{1}{2\pi RC\sqrt{6}}$$

At this frequency the real part is 1 − 5(6) = −29, so |β| = 1/29 and the amplifier must provide at least A$_v$ = 29 in magnitude (negative, inverting):

$$|A_v|=\frac{R_f}{R}\ \ge\ 29\ \ \Rightarrow\ \ R_f\ge 29R$$

(for a BJT version, h$_{fe}$ ≥ 29 + 23R$_C$/R + 4R/R$_C$ ≥ 44.5). Each section is loaded by the next, so the three sections are not independent. The circuit is simple and cheap and used for audio frequencies; its output is a good sine wave but its frequency is not easily varied (three components must be changed together). *Example:* R = 10 kΩ, C = 10 nF gives f$_o$ = 1/(2π × 10⁴ × 10⁻⁸ × 2.449) = 650 Hz, R$_f$ ≥ 290 kΩ.
'''

U['hartley'] = r'''
**Hartley oscillator.** The tank circuit consists of a capacitor C in parallel with **two inductors L$_1$ and L$_2$ in series; the junction (tap) is at a.c. ground**. Feedback is taken from the inductor tap: the voltage across L$_2$ is applied to the base and, since the tap is grounded, it is 180° out of phase with the collector voltage across L$_1$. The CE amplifier gives another 180°, so the loop phase is 0°.

<<fig:hartley>>

The tank resonates when the total reactance in the loop is zero: with mutual inductance M between the coils the equivalent inductance is L$_{eq}$ = L$_1$ + L$_2$ + 2M, so

$$f_o=\frac{1}{2\pi\sqrt{(L_1+L_2+2M)\,C}}\qquad(\text{for no mutual coupling, }M=0:\ f_o=\frac{1}{2\pi\sqrt{(L_1+L_2)C}})$$

Derivation (M = 0): in the tank the current circulates through C and L$_1$+L$_2$; resonance is when ωL$_{eq}$ = 1/(ωC), that is ω² = 1/(L$_{eq}$C). The feedback fraction is β = −L$_2$/L$_1$, and the amplifier gain magnitude is A = h$_{fe}$R$_C$/h$_{ie}$ (approximately), so oscillation needs

$$|A\beta|\ge1\ \ \Rightarrow\ \ h_{fe}\ge\frac{L_1}{L_2}\ (\text{BJT, light load})\qquad \left(\text{FET: }g_m r_d\ge \frac{L_1}{L_2}\right)$$

Frequency is varied with a variable capacitor C. Used in radio receivers as local oscillator (about 1 MHz to 100 MHz). *Example:* L$_1$ = 1 mH, L$_2$ = 1 mH, C = 100 pF: f$_o$ = 1/(2π√(2×10⁻³ × 10⁻¹⁰)) = 356 kHz.
'''

U['colpitts'] = r'''
**Colpitts oscillator.** The tank is an inductor L in parallel with **two capacitors C$_1$ and C$_2$ in series; their junction is at a.c. ground**. The voltage across C$_2$ gives the feedback to the base; being referred to the grounded junction it is 180° out of phase with the collector voltage across C$_1$, which together with the 180° of the CE amplifier gives zero total phase shift.

<<fig:colpitts>>

The two capacitors in series act as the tank capacitance

$$C_{eq}=\frac{C_1C_2}{C_1+C_2}\qquad\Rightarrow\qquad f_o=\frac{1}{2\pi\sqrt{L\,C_{eq}}}=\frac{1}{2\pi\sqrt{L\dfrac{C_1C_2}{C_1+C_2}}}$$

The feedback factor is β = −C$_1$/C$_2$ and the amplifier gain is A ≈ h$_{fe}$R$_C$/h$_{ie}$, so the sustained-oscillation condition is

$$h_{fe}\ \ge\ \frac{C_2}{C_1}\qquad(\text{FET: }g_m r_d\ge C_2/C_1)$$

*Example:* L = 100 µH, C$_1$ = 1 nF, C$_2$ = 1 nF: C$_{eq}$ = 0.5 nF, f$_o$ = 1/(2π√(100×10⁻⁶ × 0.5×10⁻⁹)) = 711.8 kHz.
'''

U['mirror_comp'] = r'''
**Simple current mirror.** Two identical transistors Q$_1$, Q$_2$ have the same V$_{BE}$, so their collector currents are equal: I$_{C2}$ = I$_{C1}$. The reference current, however, also supplies the two base currents:

$$I_{REF}=I_{C1}+2I_B=I_O\left(1+\frac{2}{\beta}\right)\ \Rightarrow\ I_O=\frac{I_{REF}}{1+2/\beta}$$

The difference between I$_O$ and I$_{REF}$ is the **base-current error** 2I$_B$ (for β = 100 it is 2 percent, and it is worse for low β).

**Base-current compensation.** An emitter-follower transistor Q$_3$ is added: its base is connected to the collector of Q$_1$, its emitter feeds the two bases (the node of Q$_1$, Q$_2$) and its collector goes to V$_{CC}$.

<<fig:mirror_comp>>

Now the two base currents are supplied by the emitter of Q$_3$, so Q$_3$'s base current is smaller by the factor (β+1) and only that much is taken from I$_{REF}$:

$$I_{B3}=\frac{2I_B}{\beta+1}=\frac{2I_O}{\beta(\beta+1)}$$

$$I_{REF}=I_{C1}+I_{B3}=I_O+\frac{2I_O}{\beta(\beta+1)}\ \Rightarrow\ I_O=\frac{I_{REF}}{1+\dfrac{2}{\beta(\beta+1)}}$$

For β = 100 the error is 2/(100 × 101) = 0.0198 percent (I$_O$ = 0.9998 I$_{REF}$) compared with 2 percent (I$_O$ = 0.9804 I$_{REF}$) for the simple mirror: the difference between I$_O$ and I$_{REF}$ is reduced by a factor of about (β+1), and it becomes almost β-independent. Q$_3$ must be a high-β transistor; it also needs V$_{CE3}$ > 0, so the minimum supply is 2V$_{BE}$ + V$_{CE(sat)}$ (slightly more than the simple mirror).
'''

U['widlar'] = r'''
**Widlar current source.** It is a current mirror with a resistor R$_E$ added in the emitter of the output transistor Q$_2$; this allows **small output currents (µA) with modest resistors**.

<<fig:widlar>>

*Relation between I$_O$ and I$_{REF}$.* Q$_1$ is diode-connected and the bases are common, so V$_{BE1}$ = V$_{BE2}$ + I$_{E2}$R$_E$. Using V$_{BE}$ = V$_T$ ln(I$_C$/I$_S$) for identical transistors:

$$V_{BE1}-V_{BE2}=V_T\ln\frac{I_{REF}}{I_O}=I_OR_E\ \ \Rightarrow\ \ R_E=\frac{V_T}{I_O}\ln\frac{I_{REF}}{I_O}\qquad(\text{taking }I_{E2}\approx I_O)$$

and I$_{REF}$ = (V$_{CC}$ − V$_{BE1}$)/R. *Example:* I$_{REF}$ = 1 mA, I$_O$ = 10 µA: R$_E$ = (25.85 mV/10 µA) ln(100) = 11.9 kΩ (a simple mirror would need a 100:1 ratio of device areas or resistors for the same current ratio).

*Output resistance.* Looking into the collector of Q$_2$ (small-signal model, with r$_o$ the transistor output resistance, g$_m$ = I$_O$/V$_T$, and r$_{π2}$ = β/g$_m$): the emitter resistance seen by Q$_2$ is R$_E$ in parallel with r$_{π}$ and the diode resistance 1/g$_{m1}$ of Q$_1$ (through the base node), i.e. R$_E$' = R$_E$ ∥ (r$_π$ + 1/g$_{m1}$ in the base branch) ≈ R$_E$ ∥ r$_π$ (since 1/g$_{m1}$ is small). A resistor R$_E$' in the emitter raises the output resistance (current-series feedback):

$$R_o=\frac{v_x}{i_x}\approx r_o\left[1+\frac{g_m R_E'}{1+R_E'/r_\pi}\right]\ \approx\ r_o\left[1+g_m\,(R_E\parallel r_\pi)\right]$$

For R$_E$ ≫ r$_π$ this tends to r$_o$(1 + β) — much larger than r$_o$ of the simple mirror (R$_o$ = r$_o$). Hence the Widlar source (i) gives small currents with small resistors (small chip area), (ii) has a high output resistance, so the output current is almost independent of the load voltage, and (iii) the output current is less sensitive to supply variations, but it has a temperature dependence proportional to T (I$_O$ is a PTAT-type current).
'''

# ---------------------------------------------------------------- power amplifiers
U['classA_tc'] = r'''
**Transformer-coupled class A amplifier.** The collector load is the primary of an output transformer whose secondary feeds the load R$_L$; the transistor is biased at a point Q in the middle of the active region so that it conducts for the full 360° of the input cycle. The transformer matches the load: the resistance seen in the collector is R$_L'$ = (N$_1$/N$_2$)²R$_L$. Because the d.c. resistance of the primary is almost zero, the **d.c. load line is vertical** (V$_{CE}$ = V$_{CC}$ for all I$_C$); the **a.c. load line** passes through Q with slope −1/R$_L'$ and swings between 0 and 2V$_{CC}$.

<<fig:classA_tc>>

**General efficiency.** Let the collector-emitter voltage swing between V$_{CE(max)}$ and V$_{CE(min)}$ (peak-to-peak V$_{pp}$ = V$_{CE(max)}$ − V$_{CE(min)}$) and V$_{CEQ}$ = V$_{CC}$:

$$\begin{gathered}
P_{dc}=V_{CC}I_{CQ} \\
P_{ac}=\frac{V_{p}I_{p}}{2}=\frac{V_{pp}\,I_{pp}}{8}=\frac{(V_{CE(max)}-V_{CE(min)})(I_{C(max)}-I_{C(min)})}{8}
\end{gathered}$$

With V$_{CE(max)}$ + V$_{CE(min)}$ = 2V$_{CC}$ and I$_{CQ}$ = V$_{CC}$/R$_L'$: I$_{pp}$ = V$_{pp}$/R$_L'$, so P$_{ac}$ = V$_{pp}^2$/(8R$_L'$) and

$$\eta=\frac{P_{ac}}{P_{dc}}=\frac{V_{pp}^2/(8R_L')}{V_{CC}^2/R_L'}=\frac{1}{8}\left(\frac{V_{pp}}{V_{CC}}\right)^2=\frac{1}{2}\left(\frac{V_p}{V_{CC}}\right)^2\qquad\left(=50\left(\frac{V_{CE(max)}-V_{CE(min)}}{V_{CE(max)}+V_{CE(min)}}\right)^2\ \text{percent}\right)$$

**Maximum efficiency.** The largest possible swing is V$_p$ = V$_{CC}$ (V$_{CE(min)}$ = 0, V$_{CE(max)}$ = 2V$_{CC}$): **η$_{max}$ = 50 percent**, compared with 25 percent for the series-fed (resistive-load) class A stage. The maximum output power is P$_{ac(max)}$ = V$_{CC}^2$/(2R$_L'$) = V$_{CC}I_{CQ}$/2, and the transistor dissipation is largest with no signal, P$_D$ = V$_{CC}I_{CQ}$ = 2P$_{ac(max)}$.
'''

U['classA_series'] = r'''
**Series-fed class A amplifier.** The load R$_C$ is connected in series with the collector from V$_{CC}$ and the transistor is biased (R$_B$) at the middle of the d.c. load line: I$_{CQ}$ = V$_{CC}$/(2R$_C$), V$_{CEQ}$ = V$_{CC}$/2. The same resistor R$_C$ (the load) carries the d.c. current.

$$\begin{gathered}
P_{dc}=V_{CC}I_{CQ}\quad(\text{input power from the supply}) \\
P_{ac}=\frac{V_{CE(p\text{-}p)}\,I_{C(p\text{-}p)}}{8}=\frac{I_{C(p\text{-}p)}^2R_C}{8}\ \ \left(\text{with }V_{CE(p\text{-}p)}=I_{C(p\text{-}p)}R_C\right)
\end{gathered}$$

$$\eta=\frac{P_{ac}}{P_{dc}}\times100=\frac{V_{CE(p\text{-}p)}I_{C(p\text{-}p)}/8}{V_{CC}I_{CQ}}\times100$$

For the maximum symmetrical swing: V$_{CE(p\text{-}p)}$ = V$_{CC}$ (V$_{CE}$ from 0 to V$_{CC}$) and I$_{C(p\text{-}p)}$ = 2I$_{CQ}$ = V$_{CC}$/R$_C$, so

$$P_{ac(max)}=\frac{V_{CC}\cdot 2I_{CQ}}{8}=\frac{V_{CC}I_{CQ}}{4}\ \ \Rightarrow\ \ \eta_{max}=\frac{V_{CC}I_{CQ}/4}{V_{CC}I_{CQ}}=\mathbf{25\ percent}$$

In general η = 25 (V$_{pp}$/V$_{CC}$)² percent, where V$_{pp}$ = V$_{CE(max)}$ − V$_{CE(min)}$. The poor efficiency is because the d.c. current flows through the load (a constant power V$_{CC}I_{CQ}$ is drawn even without a signal), so at most one quarter of it can be converted to a.c. power.
'''

U['classB_tc'] = r'''
**Transformer-coupled class B push-pull amplifier.** Two identical transistors Q$_1$, Q$_2$ are biased at cut-off. The input transformer (centre-tapped secondary) feeds the two bases in anti-phase; each transistor conducts for 180° (one half cycle); the centre-tapped output transformer primary combines the two half cycles in the load.

<<fig:classB_pp>>

**General efficiency.** Let the peak collector current be I$_p$ = V$_p$/R$_L'$ (V$_p$ = peak collector voltage swing, V$_p$ ≤ V$_{CC}$). Each transistor carries a half-sine pulse, so the average supply current is the sum of the two average currents:

$$\begin{gathered}
I_{dc}=2\cdot\frac{I_p}{\pi}=\frac{2V_p}{\pi R_L'},\qquad P_{dc}=V_{CC}I_{dc}=\frac{2V_{CC}V_p}{\pi R_L'} \\
P_{ac}=\frac{V_pI_p}{2}=\frac{V_p^2}{2R_L'} \\
\eta=\frac{P_{ac}}{P_{dc}}=\frac{V_p^2/(2R_L')}{2V_{CC}V_p/(\pi R_L')}=\frac{\pi}{4}\,\frac{V_p}{V_{CC}}\ \ (\times100\ \text{percent})
\end{gathered}$$

**Maximum efficiency** (V$_p$ = V$_{CC}$): η$_{max}$ = π/4 = **78.5 percent**, with P$_{ac(max)}$ = V$_{CC}^2$/(2R$_L'$) and P$_{dc}$ = 2V$_{CC}^2$/(πR$_L'$). The efficiency is **smallest (zero) at no signal** and increases linearly with V$_p$; no power is drawn from the supply when there is no signal.

**Power dissipation and the worst-case point.** P$_{D}$ (both transistors) = P$_{dc}$ − P$_{ac}$ = 2V$_{CC}$V$_p$/(πR$_L'$) − V$_p^2$/(2R$_L'$). Setting dP$_D$/dV$_p$ = 0: 2V$_{CC}$/(πR$_L'$) − V$_p$/R$_L'$ = 0, so the dissipation is **maximum at V$_p$ = 2V$_{CC}$/π ≈ 0.636V$_{CC}$**, where η = (π/4)(2/π) = 50 percent and

$$P_{D(max)}=\frac{2V_{CC}^2}{\pi^2R_L'}\ \ \text{(for both transistors; half in each)}$$

so each transistor must be rated for at least P$_{D(max)}$/2 = V$_{CC}^2$/(π²R$_L'$), which is about 0.2 P$_{ac(max)}$ (because P$_{ac(max)}$ = V$_{CC}^2$/(2R$_L'$)).
'''

U['crossover'] = r'''
**Crossover distortion.** In a class B push-pull stage each transistor conducts only when its base-emitter voltage exceeds the cut-in voltage (about 0.5 to 0.7 V for silicon). Near the zero crossing of the input, when −0.7 V < v$_i$ < +0.7 V, **neither transistor conducts**, so the output stays at zero for that interval (a dead band). The output waveform is therefore distorted at the point where the output passes from one transistor to the other: this is called **crossover distortion**. It is most serious for small signals and gives odd harmonics.

<<fig:crossover>>

**Class AB operation removes it.** The two transistors are given a small forward bias (V$_{BE}$ slightly above cut-in) from two series diodes or a V$_{BE}$-multiplier connected between the bases (the diodes track the transistors with temperature and avoid thermal runaway), so each device has a small quiescent current I$_{CQ}$ and conducts for slightly more than 180° (180° < θ < 360°). The two transfer characteristics then overlap around the origin, and the sum of the two collector currents is linear through zero. The price is a small quiescent power dissipation, so the efficiency is between class A (50 percent) and class B (78.5 percent). In an actual stage a resistor R$_E$ of about 0.5 Ω in each emitter limits the quiescent current.
'''

U['classB_numeric'] = r'''
Given V$_{CC}$ = %(vcc)s V, R$_L$ = 16 Ω. The two transistors of the push-pull stage give

$$\begin{gathered}
I_{p}=\frac{V_p}{R_L},\qquad I_{dc}=\frac{2I_p}{\pi},\qquad P_{in}=V_{CC}I_{dc}=\frac{2V_{CC}V_p}{\pi R_L} \\
P_o=\frac{V_p^2}{2R_L},\qquad \eta=\frac{P_o}{P_{in}}=\frac{\pi}{4}\frac{V_p}{V_{CC}}
\end{gathered}$$
'''
