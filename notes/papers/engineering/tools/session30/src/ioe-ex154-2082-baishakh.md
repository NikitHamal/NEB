---
file: NEBians-IOE-Past-Paper-Electronics-Circuit-EX154-2082-Baishakh.pdf
subject: Electronics Circuit
level: BE · Year I / Part II
code: EX 154
year_bs: 2082 Baishakh
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>


@q 1
What are the large signal models of PN junction diode? Explain with necessary figures and examples. [[4]]

@q 2
Explain the operation of light emitting diode (LED). Draw the circuit diagram of center-tapped full wave rectifier. [[4]]

@q 3
Explain the operation of NPN transistor in active mode. Also derive the relationship between α and β. [[6]]

@q 4
Find input impedance, output impedance, and voltage gain for the following amplifier circuit. Given: r$_e$ = 20 Ω, β = 200. [[6]]

%%FIG q4ce|Question 4: voltage-divider biased CE amplifier, V$_{CC}$ = +10 V, R$_1$ = R$_2$ = 10 kΩ, R$_C$ = 2 kΩ, R$_E$ = 4.3 kΩ (bypassed by C$_E$), R$_s$ = 600 Ω, R$_L$ = 10 kΩ.%%

@q 5
Explain the construction and operation of an n-channel depletion type MOSFET with necessary diagrams. [[6]]

@q 6
Find the drain current (I$_D$) and drain to source voltage (V$_{DS}$) for the following circuit. The given parameters are V$_t$ = 1 V and K = 0.5 mA/V$^2$. [[6]]

%%FIG q6mos2|Question 6: enhancement MOSFET, V$_{DD}$ = +10 V, R$_1$ = R$_2$ = 10 MΩ, R$_D$ = 6 kΩ, R$_S$ = 6 kΩ.|R1=R$_1$ = 10 MΩ;R2=R$_2$ = 10 MΩ;RD=R$_D$ = 6 kΩ;RS=R$_S$ = 6 kΩ;VDD=+10 V%%

@q 7
Write any four properties of ideal Op-Amp. Design a circuit diagram for summing amplifier to generate output voltage V$_o$ = 2V$_1$ − 4V$_2$ + 5V$_3$, where V$_1$, V$_2$, V$_3$ are input signals. [[4]]

@q 8
Draw and explain the circuit diagram of Wien bridge oscillator. Also derive the expression for frequency of oscillation. [[4]]

@q 9
Draw the circuit diagram of the series fed class A amplifier and calculate its maximum efficiency. [[6]]

@q 10
Draw a class A tuned amplifier circuit and find its 3 dB bandwidth. [[6]]

@q 11
Find the Zener current in the given circuit. Assume V$_Z$ = 10 V. [[4]]

%%FIG zen|Question 11: Zener shunt circuit, V$_S$ = 18 V, R = 100 Ω, R$_L$ = 1.2 kΩ, V$_o$ = 10 V.|VS=18 V;RS=100 Ω;VZ=10 V;RL=1.2 kΩ%%

@q 12
Draw the series dc voltage regulator with current limiting element and explain how it works. [[4]]
<!-- SOLUTIONS -->

@s 1
**Why a large-signal model is needed.** The diode current follows the Shockley equation i$_D$ = I$_S$(e$^{v_D/nV_T}$ − 1), which is non-linear. When the signal is large compared with the thermal voltage (V$_T$ ≈ 26 mV), the diode cannot be linearised about one Q-point, so the exponential curve is replaced by straight-line (piece-wise linear) approximations called **large-signal models**. Each model is a combination of an ideal diode (a switch that is closed for forward bias and open for reverse bias) with a battery and a resistor.

%%FIG diodemodels|Large-signal models of the PN junction diode compared with the real characteristic.%%

| Model | Forward (v$_D$ > threshold) | Reverse | Use |
|---|---|---|---|
| **Ideal diode** | short circuit, v$_D$ = 0 | open circuit, i$_D$ = 0 | quick hand analysis when the supply is much larger than 0.7 V |
| **Constant-voltage-drop** | ideal diode in series with a battery V$_D$ = 0.7 V (Si) | open circuit | the usual model, error below a few percent |
| **Piece-wise linear** | ideal diode + battery V$_γ$ (cut-in voltage, 0.5 to 0.65 V) + resistor r$_d$ (slope 1/r$_d$) | open circuit | when the forward resistance matters |

**Example.** A silicon diode is in series with R = 1 kΩ and a 5 V supply.

$$\begin{gathered}
\text{Ideal: } I=\frac{5}{1\ \text{k}\Omega}=5.00\ \text{mA} \\
\text{Constant drop: } I=\frac{5-0.7}{1\ \text{k}\Omega}=4.30\ \text{mA} \\
\text{Piece-wise linear } (V_\gamma=0.65\ \text{V},\ r_d=20\ \Omega):\ I=\frac{5-0.65}{1000+20}=4.26\ \text{mA}
\end{gathered}$$

The ideal model is about 16 percent high, while the last two answers agree within 1 percent. With a 1 V supply the ideal model would give 1 mA against 0.30 mA from the constant-drop model, which shows why the drop must be kept for small supplies.

@s 2
**Operation of the LED.** An LED is a p-n junction made of a direct-band-gap compound semiconductor (GaAs, GaAsP, GaP, AlGaInP, GaN). When it is **forward biased**, the barrier falls and electrons from the n-side and holes from the p-side are injected across the junction. Near the junction the injected electrons **recombine** with holes, and in a direct-gap material each recombination releases the energy as a **photon**:

$$\begin{gathered}E=h\nu\approx E_g \\ \lambda\ (\mu\text{m})=\frac{1.24}{E_g\ (\text{eV})}\end{gathered}$$

So the colour is set by the band gap: GaAs (1.4 eV) is infrared, GaAsP red (about 1.8 V forward drop), GaP green, GaN blue (about 3.2 V). In reverse bias no current flows and no light is emitted. An LED needs a **series resistor** to limit the current, R$_S$ = (V$_S$ − V$_F$)/I$_F$; for example V$_S$ = 5 V, V$_F$ = 2 V and I$_F$ = 10 mA give R$_S$ = 300 Ω. The light output is proportional to the forward current; the response is fast (nanoseconds) and the efficiency is high, which is why LEDs are used as indicators, displays, optocouplers and fibre-optic sources.

%%FIG led|LED circuit (left) and recombination at the forward-biased junction (right).%%

**Centre-tapped full-wave rectifier.** The transformer secondary has a centre tap that is the common (zero) reference. Each half of the secondary gives a peak voltage V$_m$ with respect to the tap. During the positive half cycle D$_1$ conducts (D$_2$ is reverse biased), during the negative half cycle D$_2$ conducts, and the current through R$_L$ always has the same direction.

%%FIG ctfw|Centre-tapped full-wave rectifier and its waveforms.%%

$$\begin{gathered}V_{dc}=\frac{2V_m}{\pi}=0.636\,V_m,\qquad V_{rms}=\frac{V_m}{\sqrt2} \\
\text{ripple factor }r=\sqrt{\frac{\pi^2}{8}-1}=0.482,\qquad \eta_{max}=\frac{8}{\pi^2}=81.2\ \text{percent} \\
\text{PIV}=2V_m,\qquad f_{ripple}=2f
\end{gathered}$$

@s 3
**Active mode.** In the active region the emitter-base junction is **forward biased** (V$_{BE}$ ≈ 0.7 V) and the collector-base junction is **reverse biased** (V$_{CB}$ > 0). Operation of the n-p-n transistor:

1. The heavily doped n-type emitter injects a large number of **electrons** into the thin p-type base (I$_{nE}$); a very small number of holes go from base to emitter (I$_{pE}$, made small by the doping ratio).
2. The base is thin and lightly doped, so only a few electrons (a few percent) recombine with holes there. The recombination current and the hole injection form the **base current I$_B$**.
3. The remaining electrons diffuse to the collector-base depletion region, where the strong reverse field sweeps them into the collector. This is the **collector current I$_C$**, which hardly depends on V$_{CB}$.
4. A small reverse saturation current I$_{CBO}$ (thermally generated minority carriers) also flows across the reverse-biased collector junction.

%%FIG npn|Carrier flow in an n-p-n transistor in the active region.%%

**Relation between α and β.** By Kirchhoff's current law for the whole transistor,

$$I_E=I_B+I_C$$

The d.c. current gains are defined as

$$\alpha=\frac{I_C}{I_E}\ (<1,\ 0.95\text{ to }0.995),\qquad \beta=\frac{I_C}{I_B}\ (50\text{ to }300)$$

Dividing I$_E$ = I$_B$ + I$_C$ by I$_C$:

$$\frac{1}{\alpha}=\frac{I_E}{I_C}=\frac{I_B}{I_C}+1=\frac{1}{\beta}+1$$

$$\boxed{\ \beta=\frac{\alpha}{1-\alpha},\qquad \alpha=\frac{\beta}{1+\beta},\qquad I_E=(\beta+1)I_B\ }$$

*Example:* α = 0.98 gives β = 0.98/0.02 = 49; β = 200 gives α = 200/201 = 0.995. Including the leakage, I$_C$ = αI$_E$ + I$_{CBO}$ = βI$_B$ + (β + 1)I$_{CBO}$.

@s 4
The emitter resistor R$_E$ is bypassed by C$_E$, so for a.c. the emitter is grounded and the hybrid-π model of the stage is the one below (r$_o$ is neglected, no value is given).

%%FIG smallsig|Small-signal model of the CE stage (R$_B$ = R$_1$ ∥ R$_2$).%%

**Input impedance.** R$_B$ = R$_1$ ∥ R$_2$ = 10 k ∥ 10 k = 5 kΩ, and the resistance looking into the base is r$_π$ = βr$_e$ = 200 × 20 = 4 kΩ.

$$\begin{gathered}Z_i=R_B\parallel r_\pi=\frac{5\times4}{5+4}\ \text{k}\Omega=2.22\ \text{k}\Omega \\
\text{(seen by the source: } R_s+Z_i=2.82\ \text{k}\Omega\text{)}
\end{gathered}$$

**Output impedance.** Looking back into the collector with v$_s$ = 0, i$_b$ = 0 and the dependent source is dead, so

$$Z_o=R_C\parallel r_o\approx R_C=2\ \text{k}\Omega$$

**Voltage gain.** The a.c. load is R$_C$ ∥ R$_L$ = 2 k ∥ 10 k = 1.667 kΩ. With v$_π$ = v$_i$ and v$_o$ = −g$_m$v$_π$(R$_C$ ∥ R$_L$), g$_m$ = 1/r$_e$ (taking α ≈ 1):

$$A_v=\frac{v_o}{v_i}=-\frac{R_C\parallel R_L}{r_e}=-\frac{1667}{20}=\boxed{-83.3}$$

(negative sign: 180° phase shift). Including the source resistance, the overall gain is

$$A_{vs}=\frac{v_o}{v_s}=A_v\,\frac{Z_i}{Z_i+R_s}=-83.3\times\frac{2222}{2822}=-65.6$$

and the current gain is A$_i$ = A$_v$Z$_i$/R$_L$ = −83.3 × 2.22 k/10 k = −18.5. *Remark:* the d.c. bias gives I$_E$ ≈ (5 − 0.7)/4.3 k = 1 mA, i.e. r$_e$ = 26 Ω; the value r$_e$ = 20 Ω given in the question has been used as instructed (with 26 Ω: Z$_i$ = 2.4 kΩ, A$_v$ = −64).

@s 5
**Construction.** The n-channel depletion-type MOSFET (D-MOSFET) is built on a lightly doped **p-type substrate**. Two heavily doped **n⁺ regions** form the source and the drain, and a thin **n-type channel is diffused between them during manufacture**, so a conducting channel already exists at V$_{GS}$ = 0. A very thin insulating layer of SiO$_2$ covers the channel and carries the **metal gate**, so the gate current is of the order of 10$^{-12}$ A (input resistance 10$^{10}$ to 10$^{15}$ Ω). The substrate is usually joined to the source.

%%FIG depmos|n-channel depletion MOSFET: structure, transfer curve and drain characteristics.%%

**Operation.**

- **V$_{GS}$ = 0, V$_{DS}$ > 0:** electrons flow from source to drain through the built-in channel, giving I$_D$ = I$_{DSS}$.
- **V$_{GS}$ < 0 (depletion mode):** the negative gate repels electrons from the channel and attracts holes, so the channel is **depleted** of carriers, becomes narrower and I$_D$ decreases. At V$_{GS}$ = V$_P$ (the pinch-off voltage, a negative number) the channel is closed and I$_D$ ≈ 0.
- **V$_{GS}$ > 0 (enhancement mode):** the positive gate attracts more electrons into the channel, which widens it, and I$_D$ rises above I$_{DSS}$. (This is the feature that separates it from the JFET.)
- **Effect of V$_{DS}$:** for small V$_{DS}$ the device is an ohmic (triode) resistor controlled by V$_{GS}$; for V$_{DS}$ > V$_{GS}$ − V$_P$ the channel pinches off near the drain and I$_D$ saturates.

In saturation the transfer characteristic is the Shockley square law

$$I_D=I_{DSS}\left(1-\frac{V_{GS}}{V_P}\right)^2,\qquad g_m=\frac{2I_{DSS}}{|V_P|}\left(1-\frac{V_{GS}}{V_P}\right)$$

The symbol has a **solid** channel line (continuous channel) for the depletion type, against the broken line of the enhancement type.

@s 6
The gate current is zero, so the divider sets the gate voltage and the source resistor gives the feedback:

$$\begin{gathered}V_G=V_{DD}\frac{R_2}{R_1+R_2}=10\times\frac{10}{20}=5\ \text{V} \\
V_{GS}=V_G-I_DR_S=5-6I_D\qquad (I_D\text{ in mA, }R_S\text{ in k}\Omega)\\
I_D=K(V_{GS}-V_t)^2=0.5(5-6I_D-1)^2=0.5(4-6I_D)^2
\end{gathered}$$

Expand: I$_D$ = 0.5(16 − 48I$_D$ + 36I$_D^2$) gives

$$18I_D^2-25I_D+8=0\ \Rightarrow\ I_D=\frac{25\pm\sqrt{625-576}}{36}=\frac{25\pm7}{36}=0.889\ \text{mA or }0.5\ \text{mA}$$

For I$_D$ = 0.889 mA the gate-source voltage is V$_{GS}$ = 5 − 6(0.889) = −0.33 V, which is below V$_t$ (the device would be off), so this root is **rejected**. The valid root is

$$\begin{gathered}I_D=0.5\ \text{mA} \\
V_{GS}=5-6(0.5)=2\ \text{V}>V_t \\
V_{DS}=V_{DD}-I_D(R_D+R_S)=10-0.5(6+6)=4\ \text{V}
\end{gathered}$$

**Check of the region:** V$_{GS}$ − V$_t$ = 1 V < V$_{DS}$ = 4 V, so the MOSFET is in **saturation** and the square-law equation was applicable.

**Answer: I$_D$ = 0.5 mA, V$_{DS}$ = 4 V** (V$_{GS}$ = 2 V).

@s 7
**Properties of an ideal op-amp** (any four): (1) infinite open-loop voltage gain A$_{OL}$ = ∞; (2) infinite input impedance (zero input currents); (3) zero output impedance; (4) infinite bandwidth (flat gain from d.c. to any frequency); (5) infinite CMRR and PSRR; (6) zero input offset voltage and zero output when the inputs are equal (v$_1$ = v$_2$ gives v$_o$ = 0); (7) infinite slew rate and no noise or drift. Because A$_{OL}$ = ∞ with finite output, **v$_+$ = v$_−$** (virtual short) and i$_+$ = i$_−$ = 0.

**Design.** A single inverting summer gives only negative coefficients: v$_o$ = −R$_f$(V$_1$/R$_1$ + V$_2$/R$_2$ + V$_3$/R$_3$). Since V$_1$ and V$_3$ have positive weights and V$_2$ has a negative weight, use **two inverting stages**. Stage 1 sums V$_1$ and V$_3$ with inversion:

$$V_a=-R_f\left(\frac{V_1}{R_1}+\frac{V_3}{R_3}\right)=-(2V_1+5V_3)\ \Rightarrow\ \frac{R_f}{R_1}=2,\ \frac{R_f}{R_3}=5$$

Take R$_f$ = 10 kΩ, so R$_1$ = 5 kΩ and R$_3$ = 2 kΩ. Stage 2 sums V$_a$ (weight 1) and V$_2$ (weight 4) with inversion:

$$V_o=-R_f\left(\frac{V_a}{R_a}+\frac{V_2}{R_2}\right)=-(V_a+4V_2)=2V_1-4V_2+5V_3$$

with R$_a$ = 10 kΩ and R$_2$ = R$_f$/4 = 2.5 kΩ.

%%FIG summer|Summing amplifier for V$_o$ = 2V$_1$ − 4V$_2$ + 5V$_3$ (two inverting stages, R$_f$ = 10 kΩ).%%

**Check:** V$_1$ = V$_2$ = V$_3$ = 1 V gives V$_a$ = −7 V and V$_o$ = −(−7 + 4) = 3 V = 2 − 4 + 5. For bias-current balance a resistor equal to the parallel of the input resistors of that stage (5 k ∥ 2 k ∥ 10 k = 1.25 kΩ and 10 k ∥ 2.5 k ∥ 10 k = 1.25 kΩ) can be placed from each non-inverting input to ground.

@s 8
**Wien bridge oscillator.** An op-amp (non-inverting amplifier of gain A = 1 + R$_f$/R$_1$) is combined with a **lead-lag network**: a series R–C branch (Z$_s$) and a parallel R–C branch (Z$_p$). The lead-lag network is the positive-feedback path and the divider R$_f$, R$_1$ is the negative-feedback path that sets the gain. The two arms form a bridge, so the circuit is called a Wien bridge.

%%FIG wien|Wien bridge oscillator.%%

The feedback factor of the lead-lag network (output of the op-amp to the non-inverting input):

$$\begin{gathered}Z_s=R+\frac{1}{j\omega C},\qquad Z_p=\frac{R}{1+j\omega RC} \\
\beta=\frac{Z_p}{Z_s+Z_p}=\frac{1}{3+j\left(\omega RC-\dfrac{1}{\omega RC}\right)}
\end{gathered}$$

The Barkhausen condition requires the loop gain Aβ to be real and equal to 1. The loop phase is zero only if the imaginary part of the denominator vanishes:

$$\omega RC-\frac{1}{\omega RC}=0\ \Rightarrow\ \omega_o=\frac{1}{RC}\quad\Rightarrow\quad\boxed{\ f_o=\frac{1}{2\pi RC}\ }$$

At this frequency β = 1/3 with no phase shift, so oscillations are sustained when A = 3, i.e. **R$_f$ = 2R$_1$** (in practice a slightly larger gain, with a lamp or a diode network to stabilise the amplitude). If the two branches are different, f$_o$ = 1/(2π√(R$_1$R$_2$C$_1$C$_2$)). *Example:* R = 10 kΩ and C = 10 nF give f$_o$ = 1.59 kHz.

@s 9
**Circuit.** The series-fed class A amplifier has the load R$_L$ in series with the collector and the bias resistor R$_B$ from V$_{CC}$ to the base. All the d.c. collector current flows through the load, so the load is also the d.c. load. Q-point at the centre of the load line: V$_{CEQ}$ = V$_{CC}$/2 and I$_{CQ}$ = V$_{CC}$/(2R$_L$).

%%FIG classA_series|Series-fed class A amplifier and its load line.%%

**Power drawn from the supply** (signal independent):

$$P_{dc}=V_{CC}I_{CQ}=\frac{V_{CC}^2}{2R_L}$$

**Maximum signal power.** The largest undistorted swing about Q is V$_{CE}$ from 0 to V$_{CC}$, so the peak output voltage is V$_p$ = V$_{CC}$/2 and the peak current is I$_p$ = I$_{CQ}$ = V$_{CC}$/(2R$_L$):

$$P_{ac(max)}=\frac{V_pI_p}{2}=\frac{1}{2}\cdot\frac{V_{CC}}{2}\cdot\frac{V_{CC}}{2R_L}=\frac{V_{CC}^2}{8R_L}$$

**Efficiency:**

$$\eta_{max}=\frac{P_{ac(max)}}{P_{dc}}=\frac{V_{CC}^2/8R_L}{V_{CC}^2/2R_L}=\frac14=\boxed{25\ \text{percent}}$$

For a smaller swing, η = 25 percent × (V$_p$/(V$_{CC}$/2))$^2$. At no signal the whole P$_{dc}$ is dissipated in the transistor (and load), which is the weakness of the class A series-fed stage. *Example:* V$_{CC}$ = 12 V, R$_L$ = 8 Ω: P$_{dc}$ = 9 W, P$_{ac(max)}$ = 2.25 W, of the 9 W drawn, 2.25 W is useful output and the other 6.75 W is lost as heat in the load and the transistor (at zero signal all 9 W is heat: 4.5 W in the transistor and 4.5 W in R$_L$).

@s 10
%%INC 420 459%%

@s 11
The Zener is assumed to conduct (breakdown). Check: if it were removed, the load voltage would be 18 × 1.2/(0.1 + 1.2) = 16.6 V, which is greater than V$_Z$ = 10 V, so the Zener **is in breakdown** and V$_o$ = V$_Z$ = 10 V.

$$\begin{gathered}I_S=\frac{V_S-V_Z}{R}=\frac{18-10}{100}=80\ \text{mA} \\
I_L=\frac{V_Z}{R_L}=\frac{10}{1.2\ \text{k}\Omega}=8.33\ \text{mA} \\
I_Z=I_S-I_L=80-8.33=\boxed{71.7\ \text{mA}}
\end{gathered}$$

The Zener dissipates P$_Z$ = V$_Z$I$_Z$ = 10 × 71.7 mA = 0.717 W, so a Zener of at least 1 W rating is needed.

@s 12
**Circuit.** The series regulator has a **pass transistor Q$_1$** (emitter follower) in series with the load, a **Zener reference D$_Z$** (biased by R from V$_{in}$) at its base, and a small **sensing resistor R$_{sc}$** in series with the output. A second transistor Q$_2$ with its base-emitter junction across R$_{sc}$ and its collector at the base of Q$_1$ provides the **current limit**.

%%FIG seriesreg|Series voltage regulator with current-limiting transistor Q$_2$ and sense resistor R$_{sc}$.%%

**Regulation.** The Zener holds the base of Q$_1$ at V$_Z$, so V$_o$ = V$_Z$ − V$_{BE1}$ − I$_L$R$_{sc}$ ≈ V$_Z$ − 0.7 V. If V$_{in}$ rises, the extra voltage is dropped across Q$_1$ (V$_{CE1}$ increases) and V$_o$ stays constant. If the load current rises and V$_o$ tends to fall, V$_{BE1}$ increases, so Q$_1$ conducts harder and restores V$_o$ (negative feedback). The line and load regulation are good because the Zener current is nearly constant, and the base current of Q$_1$ is only I$_L$/(β+1).

**Current limiting.** The load current flows through R$_{sc}$ and produces V$_{sc}$ = I$_L$R$_{sc}$, which is the base-emitter voltage of Q$_2$. While V$_{sc}$ < 0.6 V, Q$_2$ is off and plays no part. When the load current reaches

$$I_{L(max)}=\frac{V_{BE2}}{R_{sc}}\approx\frac{0.65\ \text{V}}{R_{sc}}$$

Q$_2$ turns on and **diverts the base current of Q$_1$ to ground** through its collector, so Q$_1$ conducts less and the output current cannot rise further (short-circuit protection). *Example:* R$_{sc}$ = 0.65 Ω limits the output to about 1 A. The price paid is a voltage drop of about 0.65 V in R$_{sc}$ at full load and the power dissipated in Q$_1$ during a short circuit, (V$_{in}$ − 0)·I$_{L(max)}$, so a heat sink is needed.
