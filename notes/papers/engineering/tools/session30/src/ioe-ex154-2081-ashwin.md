---
file: NEBians-IOE-Past-Paper-Electronics-Circuit-EX154-2081-Ashwin.pdf
subject: Electronics Circuit
level: BE · Year I / Part II
code: EX 154
year_bs: 2081 Ashwin
cal: BS
year_ad: 2024
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course, 2080 batch). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>


@q 1
a) Explain the small signal model of PN junction diode and derive the expression for its dynamic resistance. [[4]]

b) Describe the operation of a full-wave bridge rectifier with necessary diagrams and waveforms. Also list its advantages over a half-wave rectifier. [[4]]

@q 2
Derive the expression for Z$_{in}$, Z$_{out}$, A$_v$ and A$_i$ in CE amplifier with bypass capacitor. [[6]]

@q 3
Draw the DC load line and determine the Q point of the voltage divider biased transistor circuit as shown in figure. Given: V$_{CC}$ = 15 V, R$_C$ = 2 kΩ, R$_E$ = 1 kΩ, R$_1$ = 10 kΩ, R$_2$ = 5 kΩ and β = 100. [[6]]

%%FIG q3ckt|Question 3: voltage-divider bias, V$_{CC}$ = 15 V, R$_1$ = 10 kΩ, R$_2$ = 5 kΩ, R$_C$ = 2 kΩ, R$_E$ = 1 kΩ, β = 100.%%

@q 4
Explain the construction and working principle of EMOSFET with drain characteristic curve. [[6]]

@q 5
Find the drain current (I$_D$) and drain to source voltage (V$_{DS}$) for the following circuit. The given parameters are V$_t$ = 1 V and k = 0.5 mA/V$^2$. [[6]]

%%FIG q6mos2|Question 5: enhancement MOSFET, V$_{DD}$ = +20 V, R$_1$ = 188 kΩ, R$_2$ = 47 kΩ, R$_D$ = 1.85 kΩ, R$_S$ = 1.65 kΩ.|R1=R$_1$ = 188 kΩ;R2=R$_2$ = 47 kΩ;RD=R$_D$ = 1.85 kΩ;RS=R$_S$ = 1.65 kΩ;VDD=+20 V%%

@q 6
a) What is meant by Virtual Ground in Operational Amplifier? Write the criteria to maintain stability in Oscillation. [[2+2]]

b) Write any four properties of ideal Op-Amp. Derive voltage gain for a non-inverting amplifier using ideal Op-Amp. [[4]]

@q 7
Derive the maximum efficiency for Transformer coupled Class A power amplifier with circuit diagram and characteristics graph. [[6]]

@q 8
Draw the circuit diagram of the transformer coupled class B push-pull amplifier and show that the maximum efficiency is 25π %. [[6]]

@q 9
Explain how Transistor shunt voltage regulator works. [[4]]

@q 10
What is the main purpose of voltage regulator? Find the current flow through the zener diode (I$_Z$) in the given circuit, assuming V$_Z$ = 9 V. [[4]]

%%FIG zen|Question 10: Zener circuit, V$_S$ = 15 V, R$_S$ = 120 Ω, R$_L$ = 160 Ω, V$_Z$ = 9 V.|VS=15 V;RS=120 Ω;VZ=9 V;RL=160 Ω%%
<!-- SOLUTIONS -->

@s 1
**(a) Small-signal model.** Let the diode be biased at a d.c. point Q (V$_D$, I$_D$) in forward conduction and let a small a.c. signal v$_d$ (much smaller than nV$_T$, i.e. below about 10 mV) be superimposed. Then v$_D$ = V$_D$ + v$_d$ and, from the Shockley equation i$_D$ = I$_S$(e$^{v_D/nV_T}$ − 1) with e$^{V_D/nV_T}$ ≫ 1,

$$\begin{gathered}i_D=I_Se^{V_D/nV_T}\,e^{v_d/nV_T}=I_D\,e^{v_d/nV_T} \\
\approx I_D\left(1+\frac{v_d}{nV_T}\right)=I_D+\frac{I_D}{nV_T}\,v_d
\end{gathered}$$

(only the first two terms of the series e$^x$ ≈ 1 + x are kept for |x| ≪ 1). The a.c. part of the current is therefore proportional to the a.c. voltage: i$_d$ = (I$_D$/nV$_T$)v$_d$, i.e. the diode behaves as a **linear resistor** called the **dynamic (incremental) resistance**

$$\boxed{\ r_d=\frac{v_d}{i_d}=\frac{dv_D}{di_D}\Big|_Q=\frac{nV_T}{I_D}\ \approx\ \frac{26\ \text{mV}}{I_D}\ (n=1,\ 300\ \text{K})\ }$$

%%FIG dynres|The dynamic resistance is the reciprocal of the slope of the i-v curve at Q; the small-signal model is the resistor r$_d$.%%

*Example:* I$_D$ = 2 mA gives r$_d$ = 26/2 = 13 Ω; at I$_D$ = 0.1 mA, r$_d$ = 260 Ω. In reverse bias r$_d$ is very large (open circuit). At higher frequency the model also carries the junction (depletion) capacitance C$_j$ in reverse bias and the diffusion capacitance C$_d$ = τ$_T$I$_D$/(nV$_T$) in forward bias, in parallel with r$_d$.

**(b) Full-wave bridge rectifier.** Four diodes D$_1$ to D$_4$ are connected as a bridge across the secondary of the transformer (or directly across the a.c. line). During the **positive half cycle** the upper input terminal is positive: D$_1$ and D$_4$ are forward biased and conduct, D$_2$ and D$_3$ are reverse biased, and the current flows through R$_L$ from top to bottom. During the **negative half cycle** D$_2$ and D$_3$ conduct and D$_1$, D$_4$ are off; the current through R$_L$ again flows from top to bottom. Hence the load always sees the same polarity and the output frequency is 2f.

%%FIG bridge|Bridge rectifier: D$_1$, D$_4$ conduct in the positive half cycle and D$_2$, D$_3$ in the negative half cycle.%%

With an ideal diode and secondary peak voltage V$_m$:

$$\begin{gathered}V_{dc}=\frac{2V_m}{\pi}\ \ (\text{with silicon diodes, }\tfrac{2}{\pi}(V_m-1.4\ \text{V})),\qquad V_{rms}=\frac{V_m}{\sqrt2} \\
r=0.482,\qquad \eta_{max}=81.2\ \text{percent},\qquad \text{PIV}=V_m
\end{gathered}$$

**Advantages over the half-wave rectifier:**

| Property | Half-wave | Bridge full-wave |
|---|---|---|
| V$_{dc}$ | V$_m$/π = 0.318V$_m$ | 2V$_m$/π = 0.636V$_m$ (double) |
| Ripple factor | 1.21 | 0.482 |
| Ripple frequency | f | 2f (easier to filter) |
| Maximum efficiency | 40.6 percent | 81.2 percent |
| Transformer utilisation | 0.287 | 0.812 (no d.c. saturation of the core) |

Compared with the centre-tapped full-wave circuit, the bridge needs no centre-tapped transformer and each diode must withstand only V$_m$ (the centre-tap circuit needs 2V$_m$), at the cost of two diode drops in series.

@s 2
The emitter resistor R$_E$ is bypassed by C$_E$, so the emitter is at a.c. ground. R$_B$ = R$_1$ ∥ R$_2$; r$_π$ = β/g$_m$ = βr$_e$ with g$_m$ = I$_C$/V$_T$; r$_o$ is the output resistance of the transistor.

%%FIG smallsig|Hybrid-π small-signal model of the CE amplifier with bypassed emitter.%%

**Input impedance.** Looking into the circuit from the source:

$$Z_{in}=R_B\parallel r_\pi=R_1\parallel R_2\parallel \beta r_e$$

**Output impedance.** Set v$_i$ = 0; then v$_π$ = 0 and the current source is dead, so only R$_C$ and r$_o$ remain (R$_L$ is the external load and is not counted):

$$Z_{out}=R_C\parallel r_o\approx R_C$$

**Voltage gain.** v$_π$ = v$_i$ and the current g$_m$v$_π$ flows in R$_C$ ∥ R$_L$ ∥ r$_o$ in the direction opposite to v$_o$:

$$A_v=\frac{v_o}{v_i}=-g_m\,(R_C\parallel R_L\parallel r_o)=-\frac{\beta\,(R_C\parallel R_L\parallel r_o)}{r_\pi}\approx-\frac{R_C\parallel R_L}{r_e}$$

**Current gain.** i$_i$ is the current delivered by the source into Z$_{in}$ and i$_o$ the current in R$_L$. By the current divider at the input, i$_b$ = i$_i$R$_B$/(R$_B$ + r$_π$) and at the output i$_o$ = −βi$_b$R$_C$/(R$_C$ + R$_L$) (r$_o$ neglected):

$$A_i=\frac{i_o}{i_i}=-\beta\,\frac{R_B}{R_B+r_\pi}\cdot\frac{R_C}{R_C+R_L}=A_v\frac{Z_{in}}{R_L}$$

All gains are negative: the CE stage gives a 180° phase shift, a medium input resistance, a high output resistance and large voltage and current gains. *Without* the bypass capacitor, R$_E$ appears in the base circuit as (β+1)R$_E$ and the gain falls to A$_v$ ≈ −R$_C$/(r$_e$ + R$_E$): this is why C$_E$ is used. *Example:* β = 100, I$_C$ = 1 mA (r$_e$ = 26 Ω), R$_B$ = 5 kΩ, R$_C$ = 2 kΩ, R$_L$ = 10 kΩ: Z$_{in}$ = 5 k ∥ 2.6 k = 1.71 kΩ, Z$_{out}$ = 2 kΩ, A$_v$ = −(1.667 k)/26 = −64, A$_i$ = −64 × 1.71 k/10 k = −11.

@s 3
**Thevenin equivalent of the base circuit.**

$$\begin{gathered}V_{TH}=V_{CC}\frac{R_2}{R_1+R_2}=15\times\frac{5}{15}=5\ \text{V} \\
R_{TH}=R_1\parallel R_2=\frac{10\times5}{15}=3.333\ \text{k}\Omega
\end{gathered}$$

**Base loop** (V$_{BE}$ = 0.7 V, I$_E$ = (β+1)I$_B$):

$$\begin{gathered}I_B=\frac{V_{TH}-V_{BE}}{R_{TH}+(\beta+1)R_E}=\frac{5-0.7}{3.333+101(1)}\ \text{mA}=41.2\ \mu\text{A} \\
I_C=\beta I_B=4.12\ \text{mA},\qquad I_E=(\beta+1)I_B=4.16\ \text{mA}
\end{gathered}$$

**Collector loop:**

$$V_{CE}=V_{CC}-I_CR_C-I_ER_E=15-4.12(2)-4.16(1)=\boxed{2.59\ \text{V}}$$

**Q point: (V$_{CEQ}$, I$_{CQ}$) = (2.59 V, 4.12 mA)** (I$_B$ = 41.2 µA). *Quick check with the approximate method (R$_{TH}$ neglected):* V$_E$ = 5 − 0.7 = 4.3 V, I$_E$ = 4.3 mA, I$_C$ ≈ 4.26 mA and V$_{CE}$ ≈ 15 − 4.26(2) − 4.3 = 2.19 V. The exact (Thevenin) result is used: the approximation overestimates I$_E$ by about 3 percent because I$_B$ drops 0.14 V across R$_{TH}$.

**DC load line.** The collector-loop equation V$_{CC}$ = I$_C$R$_C$ + V$_{CE}$ + I$_E$R$_E$ with I$_E$ ≈ I$_C$ gives the straight line

$$I_C=\frac{V_{CC}-V_{CE}}{R_C+R_E}=\frac{15-V_{CE}}{3\ \text{k}\Omega}$$

| Point | V$_{CE}$ | I$_C$ |
|---|---|---|
| Cut-off (I$_C$ = 0) | 15 V | 0 |
| Saturation (V$_{CE}$ ≈ 0) | 0 | 15/3 k = 5 mA |
| Q | 2.59 V | 4.12 mA |

%%FIG q3load|DC load line and Q point of the voltage-divider biased stage.%%

The transistor is in the active region (V$_{CE}$ = 2.59 V > V$_{CE(sat)}$ ≈ 0.2 V and V$_{CB}$ = 1.89 V > 0). Since Q lies close to the saturation end of the load line the available output swing is small (about 2.4 V on the negative side): a larger R$_2$/R$_E$ or a smaller R$_C$ would centre Q better.

@s 4
%%INC 143 187%%

@s 5
The gate current is zero, so the gate voltage is given by the divider, and the source resistor gives the d.c. feedback:

$$\begin{gathered}V_G=V_{DD}\frac{R_2}{R_1+R_2}=20\times\frac{47}{188+47}=4.0\ \text{V} \\
V_{GS}=V_G-I_DR_S=4-1.65I_D\qquad(I_D\ \text{in mA}) \\
I_D=k(V_{GS}-V_t)^2=0.5(3-1.65I_D)^2
\end{gathered}$$

Expanding 0.5(9 − 9.9I$_D$ + 2.7225I$_D^2$) = I$_D$ gives the quadratic

$$1.36125I_D^2-5.95I_D+4.5=0\ \Rightarrow\ I_D=\frac{5.95\pm\sqrt{35.4025-24.5025}}{2.7225}=\frac{5.95\pm3.3015}{2.7225}=3.398\ \text{mA or }0.973\ \text{mA}$$

The root 3.398 mA gives V$_{GS}$ = 4 − 1.65(3.398) = −1.61 V, which is below V$_t$ (the device would be cut off), so it is rejected. For I$_D$ = 0.973 mA:

$$\begin{gathered}V_{GS}=4-1.65(0.973)=2.39\ \text{V}>V_t \\
V_{DS}=V_{DD}-I_D(R_D+R_S)=20-0.973(1.85+1.65)=16.6\ \text{V}
\end{gathered}$$

**Check:** V$_{GS}$ − V$_t$ = 1.39 V < V$_{DS}$ = 16.6 V, so the transistor is in saturation and the square law applies.

**Answer: I$_D$ = 0.973 mA ≈ 0.97 mA, V$_{DS}$ = 16.6 V** (V$_{GS}$ = 2.39 V).

@s 6
**(a) Virtual ground.** In an inverting amplifier (non-inverting input grounded) the open-loop gain A is very large, so the output is finite only if the differential input v$_d$ = v$_o$/A ≈ 0. Hence the inverting terminal is at the same potential as the grounded non-inverting terminal, v$_−$ ≈ v$_+$ = 0 V, although no wire connects it to ground. This is the **virtual ground** (a virtual short). No current flows into the input terminal (infinite input resistance), so the input current flows entirely through R$_f$: i = v$_i$/R$_1$ = −v$_o$/R$_f$ and the inverting gain is v$_o$/v$_i$ = −R$_f$/R$_1$. The input resistance seen by the source is R$_1$.

**Criteria for stable oscillation (Barkhausen criteria).** An amplifier of gain A with a positive-feedback network of factor β oscillates at a frequency f$_o$ if, around the loop, (i) the **magnitude** of the loop gain is unity, |Aβ| = 1, and (ii) the **phase shift** around the loop is 0° or 360° (so the feedback is positive), ∠Aβ = 0°. For the oscillation to **start**, |Aβ| must be slightly greater than 1 so that the noise builds up; the amplitude is then limited by the non-linearity of the active device (or an amplitude-stabilising lamp or diode network), which brings |Aβ| down to exactly 1. The criteria must be satisfied at one frequency only, which is fixed by the frequency-selective network (RC, LC or crystal).

**(b) Properties of an ideal op-amp** (any four): infinite open-loop gain; infinite input resistance (i$_+$ = i$_−$ = 0); zero output resistance; infinite bandwidth; infinite CMRR; zero offset voltage and drift; infinite slew rate.

**Non-inverting amplifier.** The input v$_i$ is applied to the non-inverting terminal; the output is fed back to the inverting terminal through the divider R$_f$, R$_1$.

%%FIG noninv|Non-inverting amplifier.%%

Using the virtual short, v$_−$ = v$_+$ = v$_i$. No current enters the inverting terminal, so the same current flows in R$_1$ and R$_f$:

$$\begin{gathered}\frac{v_i}{R_1}=\frac{v_o-v_i}{R_f}\ \Rightarrow\ v_o=v_i\left(1+\frac{R_f}{R_1}\right) \\
\boxed{\ A_v=\frac{v_o}{v_i}=1+\frac{R_f}{R_1}\ }
\end{gathered}$$

The gain is positive (no phase inversion), is never less than 1, depends only on the resistor ratio, and the input resistance is ideally infinite. *Example:* R$_f$ = 9 kΩ, R$_1$ = 1 kΩ gives A$_v$ = 10. If R$_f$ = 0 and R$_1$ = ∞ the circuit becomes the voltage follower with A$_v$ = 1.

@s 7
**Circuit.** The collector load of the transformer-coupled class A stage is the **primary** of an output transformer whose secondary feeds R$_L$. The transformer reflects the load to the primary as R$_L'$ = (N$_1$/N$_2$)$^2$R$_L$ and has negligible d.c. resistance. The base is biased so that Q is at the centre of the a.c. load line.

%%FIG classA_tc|Transformer-coupled class A amplifier: d.c. and a.c. load lines.%%

**Load lines.** Because the primary has no d.c. resistance, the **d.c. load line is vertical** at V$_{CE}$ = V$_{CC}$, and the Q point is (V$_{CC}$, I$_{CQ}$). The **a.c. load line** passes through Q with slope −1/R$_L'$. When the collector current falls to zero the collector voltage reaches 2V$_{CC}$ (the transformer's induced emf adds to V$_{CC}$), so

$$R_L'=\frac{V_{CC}}{I_{CQ}},\qquad I_{C(max)}=2I_{CQ},\qquad V_{CE(max)}=2V_{CC}$$

**Power from the supply** (constant, independent of signal):

$$P_{dc}=V_{CC}I_{CQ}$$

**Maximum a.c. output power.** The largest undistorted swing is V$_{CE}$ from 0 to 2V$_{CC}$ and i$_C$ from 0 to 2I$_{CQ}$, so the peak values are V$_p$ = V$_{CC}$ and I$_p$ = I$_{CQ}$:

$$P_{ac(max)}=\frac{V_pI_p}{2}=\frac{V_{CC}I_{CQ}}{2}=\frac{V_{CC}^2}{2R_L'}$$

$$\boxed{\ \eta_{max}=\frac{P_{ac(max)}}{P_{dc}}=\frac{V_{CC}I_{CQ}/2}{V_{CC}I_{CQ}}=\frac12=50\ \text{percent}\ }$$

For any swing, η = (V$_p$/V$_{CC}$)$^2$/2 × 100 percent, i.e. in terms of the extreme values η = 50 × ((V$_{max}$ − V$_{min}$)/(V$_{max}$ + V$_{min}$))$^2$ percent. The efficiency is twice that of the series-fed (resistive-load) class A stage (25 percent) because no d.c. power is wasted in a load resistor. *Example:* V$_{CC}$ = 10 V and R$_L'$ = 20 Ω give I$_{CQ}$ = 0.5 A, P$_{dc}$ = 5 W, P$_{ac(max)}$ = 2.5 W, and the transistor dissipation is 5 W at no signal and 2.5 W at full signal.

@s 8
%%INC 376 417%%

**Maximum efficiency in the form asked.** At V$_p$ = V$_{CC}$ the efficiency is

$$\eta_{max}=\frac{\pi}{4}=0.7854=\boxed{25\pi\ \text{percent}\ (=78.5\ \text{percent})}$$

which is much higher than the 50 percent of the transformer-coupled class A stage because in class B the transistors draw no quiescent current.

@s 9
**Circuit.** In a shunt regulator the **regulating element is connected in parallel with the load**, and a **series resistor R$_s$** between the unregulated supply V$_{in}$ and the output drops the excess voltage. Here the transistor Q is the shunt element; its base is driven from the output through the Zener D$_Z$ (reverse biased) and R$_B$.

%%FIG shunt|Transistor shunt voltage regulator.%%

**Reference.** When the output voltage is above V$_Z$ + V$_{BE}$, the Zener is in breakdown and carries the base current of Q: the base voltage settles at V$_{BE}$ ≈ 0.7 V across R$_B$, so

$$V_o=V_Z+V_{BE}\approx V_Z+0.7\ \text{V}$$

**Action.** The series current is I$_S$ = (V$_{in}$ − V$_o$)/R$_s$ and it splits into I$_L$ (load) and I$_Q$ (through Q; the small Zener current is added to it): I$_S$ = I$_L$ + I$_Q$.

- If V$_{in}$ **increases** (or I$_L$ decreases), V$_o$ tends to rise; the base drive of Q increases, I$_Q$ rises, the extra current is drawn through R$_s$ and the extra drop in R$_s$ cancels the rise: V$_o$ stays constant.
- If V$_{in}$ **decreases** (or I$_L$ increases), V$_o$ tends to fall; the base drive and I$_Q$ fall, leaving more of I$_S$ for the load, and V$_o$ is restored.

Thus I$_S$ stays nearly constant and the output is regulated against line and load changes, with the transistor's current gain improving the regulation by a factor of about (β+1) compared with a plain Zener shunt. *Properties:* simple; the supply current is limited by R$_s$, so it is **short-circuit proof** (no extra current-limit circuit); but it is **inefficient** because I$_S$ flows all the time and the power V$_o$I$_Q$ is lost in Q even at light load, so it is used for low-power loads. The limit is I$_{L(max)}$ < (V$_{in(min)}$ − V$_o$)/R$_s$.

@s 10
**Purpose of a voltage regulator.** A rectifier-filter gives an output that changes with the **a.c. line voltage**, the **load current** and the **temperature**, and carries **ripple**. The regulator keeps the d.c. output voltage **constant** against these variations (and reduces the ripple), so that electronic circuits, which need a fixed supply, work correctly. Its quality is measured by the line regulation ΔV$_o$/ΔV$_{in}$, the load regulation (V$_{NL}$ − V$_{FL}$)/V$_{FL}$ and the output resistance.

**Zener current.** First find whether the Zener conducts. Remove it and compute the open-circuit load voltage:

$$V_L=V_S\frac{R_L}{R_S+R_L}=15\times\frac{160}{120+160}=8.57\ \text{V}<V_Z=9\ \text{V}$$

The voltage across the Zener is below its breakdown voltage, so the Zener is **not conducting**. (If it were assumed to be on, V$_o$ = 9 V would give I$_L$ = 9/160 = 56.25 mA, but the current available through R$_S$ is only (15 − 9)/120 = 50 mA, which would need I$_Z$ = 50 − 56.25 = −6.25 mA, impossible for a Zener, so that assumption fails.)

$$\boxed{\ I_Z\approx0\ \text{(only the negligible reverse leakage current flows)}\ }$$

The circuit then behaves as a plain divider: V$_o$ = 8.57 V (not regulated), I$_S$ = I$_L$ = 15/280 = 53.6 mA. The Zener would regulate only if V$_S$ were raised above V$_Z$(R$_S$ + R$_L$)/R$_L$ = 9 × 280/160 = 15.75 V.
