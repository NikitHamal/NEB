"""Shared answer blocks, part A: BJT biasing, small-signal models, FET/MOSFET theory.
Tokens <<fig:name>> are replaced by figure blocks in gen.py."""
import math

T = {}

# ---------------------------------------------------------------- BJT vs FET carriers
T['bipolar_unipolar'] = r'''
**Why a BJT is bipolar and a FET is unipolar.** In a BJT (npn or pnp) the collector current is carried by **both types of charge carriers**: electrons are injected from the emitter into the p-type base (minority carriers), and at the same time holes flow from the base into the emitter (this forms the base current). Both electrons and holes take part in conduction across the two p-n junctions, hence *bi-polar*. In a FET the current flows through a single semiconductor **channel** (n-type in an n-channel device, p-type in a p-channel device) between source and drain, and is carried **only by the majority carriers** of that channel (electrons in n-channel, holes in p-channel); the gate voltage only changes the width of the channel through the electric field. Only one polarity of carrier conducts, hence *uni-polar*.

| BJT | FET |
|---|---|
| Bipolar: electrons and holes | Unipolar: majority carriers only |
| Current controlled device (I$_B$ controls I$_C$) | Voltage controlled device (V$_{GS}$ controls I$_D$) |
| Low input resistance (kΩ) | Very high input resistance (MΩ to TΩ) |
| More temperature dependent (minority carriers, thermal runaway) | Less noisy and more thermally stable |
'''

# ---------------------------------------------------------------- bias design (beta independent)
def design_div(Vcc, IE_mA, beta, VE, VCE, with_rc=True):
    IE = IE_mA * 1e-3
    IC = IE * beta / (beta + 1)
    RE = VE / IE
    VB = VE + 0.7
    R2 = 0.1 * beta * RE
    R1 = Vcc * R2 / VB - R2
    RC = (Vcc - VE - VCE) / IC
    RB = R1 * R2 / (R1 + R2)
    IB = IC / beta
    s = r'''
**Design rules for a β-independent (stiff) voltage-divider bias.** Choose (i) V$_E$ = V$_{CC}$/10 so that V$_{BE}$ variations are small compared with V$_E$, (ii) V$_{CE}$ ≈ V$_{CC}$/2 for maximum undistorted swing, (iii) the divider current much larger than I$_B$, which is ensured by R$_2$ ≤ 0.1βR$_E$ (stiff divider; then V$_B$ is nearly independent of β).

Given: V$_{CC}$ = %g V, I$_E$ ≈ I$_C$ = %g mA, β = %g.

$$\begin{gathered}
V_E=\frac{V_{CC}}{10}=%.2f\ \text{V}, \qquad R_E=\frac{V_E}{I_E}=\frac{%.2f}{%g\ \text{mA}}=%.2f\ \text{k}\Omega \\
V_B=V_E+V_{BE}=%.2f+0.7=%.2f\ \text{V} \\
R_2\le 0.1\beta R_E=0.1(%g)(%.2f\ \text{k}\Omega)=%.2f\ \text{k}\Omega\ \ \Rightarrow\ \ R_2=%.2f\ \text{k}\Omega \\
\frac{R_2}{R_1+R_2}V_{CC}=V_B\ \Rightarrow\ R_1=R_2\left(\frac{V_{CC}}{V_B}-1\right)=%.2f\ \text{k}\Omega \\
R_C=\frac{V_{CC}-V_E-V_{CE}}{I_C}=\frac{%g-%.2f-%.2f}{%.3f\ \text{mA}}=%.2f\ \text{k}\Omega
\end{gathered}$$

Use the nearest standard values: R$_1$ ≈ %.0f kΩ, R$_2$ ≈ %.0f kΩ, R$_E$ ≈ %.2f kΩ, R$_C$ ≈ %.1f kΩ.

*Check of stiffness.* Thevenin resistance R$_B$ = R$_1$ ∥ R$_2$ = %.2f kΩ, and I$_B$ = I$_C$/β = %.1f µA. The voltage lost in R$_B$ is I$_B$R$_B$ = %.2f V, only a small fraction of V$_B$; so I$_E$ = (V$_{BB}$ − V$_{BE}$)/(R$_E$ + R$_B$/(β+1)) changes by about %.1f percent when β changes from β to 2β, i.e. the Q-point is practically β-independent. With I$_C$ = %g mA the quiescent voltages are V$_{CE}$ = %.2f V and V$_C$ = %.2f V (transistor in the active region).
''' % (Vcc, IE_mA, beta, VE, VE, IE_mA, RE/1e3, VE, VB, beta, RE/1e3, R2/1e3, round(R2/1e3,1),
       R2*(Vcc/VB-1)/1e3, Vcc, VE, VCE, IC*1e3, RC/1e3, round(R1/1e3), round(R2/1e3), RE/1e3, RC/1e3, RB/1e3, IB*1e6, IB*RB, 100*abs(1/(RE+RB/(beta+1)) - 1/(RE+RB/(2*beta+1)))/(1/(RE+RB/(beta+1))), IC*1e3, VCE, VE+VCE)
    return s

def design_cc(Vcc, IC_mA, beta):
    IE = IC_mA * 1e-3 * (beta + 1) / beta
    VE = Vcc / 2
    RE = VE / IE
    VB = VE + 0.7
    R2 = 0.1 * beta * RE
    R1 = Vcc * R2 / VB - R2
    re = 0.026 / IE
    Zi = (R1 * R2 / (R1 + R2)) * ((beta + 1) * (re + RE)) / ((R1 * R2 / (R1 + R2)) + (beta + 1) * (re + RE))
    return r'''
**Design of the β-independent common-collector (emitter-follower) amplifier by firm (voltage-divider) biasing.** The collector is tied directly to V$_{CC}$ (a.c. ground); the load resistor R$_E$ is in the emitter. For the largest symmetrical output swing the emitter is biased at half the supply, V$_E$ = V$_{CC}$/2 (so V$_{CE}$ = V$_{CC}$/2).

Given V$_{CC}$ = %g V, I$_C$ = %g mA, β = %g, so I$_E$ = I$_C$(β+1)/β = %.3f mA.

$$\begin{gathered}
V_E=\frac{V_{CC}}{2}=%.1f\ \text{V}, \qquad R_E=\frac{V_E}{I_E}=\frac{%.1f}{%.3f\ \text{mA}}=%.2f\ \text{k}\Omega\ \approx\ %.1f\ \text{k}\Omega \\
V_B=V_E+V_{BE}=%.1f+0.7=%.1f\ \text{V} \\
R_2\le 0.1\beta R_E=0.1(%g)(%.2f\ \text{k}\Omega)=%.1f\ \text{k}\Omega\ \ (\text{take }R_2=%.0f\ \text{k}\Omega) \\
R_1=R_2\left(\frac{V_{CC}}{V_B}-1\right)=%.1f\ \text{k}\Omega\ \ (\text{use }%.0f\ \text{k}\Omega)
\end{gathered}$$

Because R$_2$ ≤ 0.1βR$_E$ the divider is stiff: V$_B$ ≈ V$_{CC}$R$_2$/(R$_1$+R$_2$) = %.2f V irrespective of β, so I$_E$ = (V$_B$ − 0.7)/R$_E$ is set by the resistors alone (β-independent). Small-signal check: r$_e$ = 26 mV/I$_E$ = %.1f Ω, voltage gain A$_v$ = R$_E$/(R$_E$+r$_e$) ≈ %.3f ≈ 1, input resistance Z$_i$ = R$_1$∥R$_2$∥(β+1)(r$_e$+R$_E$) ≈ %.1f kΩ. Coupling capacitors C$_1$, C$_2$ (about 10 µF) and no bypass capacitor are used.

<<fig:cc_design>>
''' % (Vcc, IC_mA, beta, IE*1e3, VE, VE, IE*1e3, RE/1e3, round(RE/1e3,1), VE, VB, beta, RE/1e3, R2/1e3, round(R2/1e3), R2*(Vcc/VB-1)/1e3, round(R1/1e3), Vcc*round(R2/1e3)*1e3/(round(R1/1e3)*1e3+round(R2/1e3)*1e3), re, RE/(RE+re), Zi/1e3)

# ---------------------------------------------------------------- small signal models
T['cb'] = r'''
**Role of the bypass capacitor.** A bypass capacitor (for example C$_E$ across R$_E$ in a CE stage) offers a very small reactance X$_C$ = 1/(2πfC) at the signal frequency, so it **short-circuits the a.c. signal to ground** around the resistor while it is an open circuit for d.c. Hence (i) the biasing resistor R$_E$ keeps the Q-point stable (d.c. negative feedback) and (ii) the signal sees no emitter degeneration, so the full gain is obtained (A$_v$ = −R$_C$/r$_e$ instead of −R$_C$/(r$_e$+R$_E$)). In the common-base amplifier the base capacitor C$_B$ is a bypass capacitor that holds the base at a.c. ground. It is chosen so that X$_C$ ≤ R/10 at the lowest signal frequency.

**Small-signal equivalent of the common-base amplifier.** With the base at a.c. ground, the emitter is the input and the collector the output. Using the r$_e$ model (r$_e$ = V$_T$/I$_E$ = 26 mV/I$_E$; the collector current is a source αi$_e$ in parallel with the large output resistance r$_o$, neglected):

<<fig:cb_ss>>

$$\begin{gathered}
Z_i = R_E \parallel r_e \approx r_e \qquad (\text{a few ohms to tens of ohms}) \\
Z_o = R_C \parallel r_o \approx R_C \\
v_o=-\alpha i_e R_C,\ \ v_i=-i_e r_e\ \Rightarrow\ A_v=\frac{v_o}{v_i}=\frac{\alpha R_C}{r_e}\approx\frac{R_C}{r_e}
\end{gathered}$$

With a load R$_L$ the gain is A$_v$ ≈ (R$_C$∥R$_L$)/r$_e$. The gain is positive (no phase shift between input and output), the current gain A$_i$ = α ≈ 1, the input resistance is very low and the output resistance high, so the CB stage is used as a current buffer and at high frequencies (no Miller effect). Example: I$_E$ = 2 mA, r$_e$ = 13 Ω, R$_C$ = 4 kΩ gives A$_v$ ≈ 308 and Z$_i$ ≈ 13 Ω.
'''

T['ce'] = r'''
**Role of the coupling capacitors.** A coupling capacitor (C$_1$ at the input, C$_2$ at the output) is connected in series with the signal path. Its reactance X$_C$ = 1/(2πfC) is small at the signal frequency so the **a.c. signal passes**, while it **blocks d.c.** Hence the d.c. bias point of the stage is not disturbed by the source or by the next stage (or load), and the stages can be cascaded. They are chosen so that X$_C$ ≤ 0.1 × (the resistance seen) at the lowest frequency; together with the resistances they set the **lower cut-off frequency** f$_L$ = 1/(2π R C).

**Small-signal equivalent of the common-emitter amplifier** (voltage-divider bias, emitter bypassed so that R$_E$ is short-circuited for a.c.; capacitors short, V$_{CC}$ at a.c. ground; R$_B$ = R$_1$∥R$_2$). In the hybrid-π model r$_π$ = β r$_e$ and the collector source is g$_m$v$_{be}$ = βi$_b$ in parallel with r$_o$:

<<fig:ce_ss>>

(The figure includes an un-bypassed R$_E$; for a bypassed emitter R$_E$ = 0.) For the bypassed case:

$$\begin{gathered}
Z_i = R_B \parallel r_\pi = R_1\parallel R_2\parallel \beta r_e \\
Z_o = R_C \parallel r_o \approx R_C \\
v_o=-\beta i_b\,(r_o\parallel R_C\parallel R_L),\quad v_i=i_b r_\pi \ \Rightarrow\ A_v=-\frac{\beta (R_C\parallel R_L)}{\beta r_e}=-\frac{R_C\parallel R_L}{r_e}
\end{gathered}$$

The negative sign is the **180° phase shift** between v$_o$ and v$_i$. Without the bypass capacitor the gain falls to A$_v$ ≈ −(R$_C$∥R$_L$)/(r$_e$ + R$_E$) and Z$_i$ rises to R$_B$∥β(r$_e$+R$_E$). Example: for the design of Question 1 (I$_E$ = 1 mA, r$_e$ = 26 Ω, β = 100, R$_C$ = 6.2 kΩ, R$_B$ = 87 kΩ∥15 kΩ = 12.8 kΩ): Z$_i$ = 12.8 kΩ ∥ 2.6 kΩ ≈ 2.2 kΩ, Z$_o$ ≈ 6.2 kΩ and A$_v$ ≈ −6.2 kΩ/26 Ω ≈ −238.
'''

T['cc'] = r'''
**Why the common-collector amplifier is called an emitter follower.** The output is taken from the emitter and the emitter voltage **follows the input** in magnitude and phase: v$_o$ = v$_i$ − V$_{BE}$, so the voltage gain is close to 1 (slightly less) and there is no phase reversal. The emitter "follows" the base.

**Small-signal model** (collector at a.c. ground, r$_o$ neglected):

<<fig:cc_ss>>

Input loop: v$_i$ = i$_b$r$_π$ + i$_e$R$_E$ with i$_e$ = (β+1)i$_b$ and r$_π$ = βr$_e$, so the resistance looking into the base is

$$Z_b=\frac{v_i}{i_b}=r_\pi+(\beta+1)R_E\approx\beta\,(r_e+R_E),\qquad Z_i=R_B\parallel Z_b$$

Voltage gain: v$_o$ = i$_e$R$_E$ = (β+1)i$_b$R$_E$, hence

$$A_v=\frac{v_o}{v_i}=\frac{(\beta+1)R_E}{r_\pi+(\beta+1)R_E}=\frac{R_E}{R_E+r_e}\ \lesssim\ 1$$

Current gain (load R$_L$ connected, R$_E$' = R$_E$∥R$_L$; i$_o$ is the current in R$_L$):

$$A_i=\frac{i_o}{i_i}=\frac{i_o}{i_b}\cdot\frac{i_b}{i_i}=(\beta+1)\frac{R_E}{R_E+R_L}\cdot\frac{R_B}{R_B+Z_b}\approx(\beta+1)\ \text{(large)}$$

Output resistance Z$_o$ = R$_E$ ∥ (r$_e$ + R$_s'$/(β+1)), where R$_s'$ = R$_s$∥R$_B$ is the source resistance seen by the base; it is **very low**. So the emitter follower has high input resistance, low output resistance, unity voltage gain and large current gain: it is a buffer used for impedance matching.
'''

T['gm_bjt'] = r'''
**Transconductance** is the change of collector current per unit change of base-emitter voltage at a fixed V$_{CE}$:

$$g_m=\left.\frac{\partial i_C}{\partial v_{BE}}\right|_{V_{CE}}$$

The collector current of a forward-active BJT follows the Shockley (Ebers-Moll) relation

$$i_C=I_S\,e^{\,v_{BE}/V_T},\qquad V_T=\frac{kT}{q}\approx 26\ \text{mV at }300\ \text{K}$$

Differentiating with respect to v$_{BE}$ at the Q-point (I$_C$, V$_{BE}$):

$$g_m=\frac{d}{dv_{BE}}\left(I_S e^{v_{BE}/V_T}\right)=\frac{I_S e^{V_{BE}/V_T}}{V_T}=\frac{I_C}{V_T}\approx 40\,I_C$$

So g$_m$ is directly proportional to the d.c. collector current (about 40 mS per mA). Related quantities: r$_e$ = V$_T$/I$_E$ = α/g$_m$ ≈ 1/g$_m$, r$_π$ = β/g$_m$ = βr$_e$ and the small-signal collector current is i$_c$ = g$_m$v$_{be}$. Example: I$_C$ = 1.5 mA gives g$_m$ = 1.5 mA/26 mV = 57.7 mS and r$_e$ = 17.3 Ω.
'''

T['bjt_switch'] = r'''
A BJT works as an electronic switch when it is driven between **cut-off** (switch OFF, open) and **saturation** (switch ON, closed); the active region is only passed through quickly.

<<fig:bjt_switch>>

- **Cut-off (OFF).** If the input is low (V$_i$ < 0.5 V, say 0 V) the base-emitter junction is not forward biased, I$_B$ = 0, I$_C$ ≈ I$_{CEO}$ ≈ 0, so V$_{CE}$ = V$_{CC}$ and V$_o$ ≈ V$_{CC}$: the collector-emitter path behaves as an **open switch** (high resistance).
- **Saturation (ON).** If the input is high (V$_i$ = V$_H$), a base current large enough to satisfy I$_B$ ≥ I$_{C(sat)}$/β drives both junctions forward, V$_{CE}$ falls to V$_{CE(sat)}$ ≈ 0.1 to 0.2 V and I$_C$ = I$_{C(sat)}$ = (V$_{CC}$ − V$_{CE(sat)}$)/R$_C$ ≈ V$_{CC}$/R$_C$: a **closed switch** (low resistance) with output V$_o$ ≈ 0.2 V. The base resistor is R$_B$ = (V$_H$ − 0.7)/I$_B$ with I$_B$ made about 2 to 5 times the minimum value to ensure hard saturation.
- The load line joins (V$_{CC}$, 0) and (0, V$_{CC}$/R$_C$); the two operating points are the ends of this line.

*Example.* V$_{CC}$ = 10 V, R$_C$ = 2.5 kΩ, β = 100, V$_H$ = 5 V: I$_{C(sat)}$ ≈ 4 mA, so I$_{B(min)}$ = 40 µA; take I$_B$ = 0.2 mA (5 times), R$_B$ = (5 − 0.7)/0.2 mA = 21.5 kΩ ≈ 22 kΩ.

The stage is also a **NOT gate (inverter)**: input high gives output low and vice versa. Switching speed is limited by the storage time and the delay, rise and fall times (t$_{on}$ = t$_d$ + t$_r$, t$_{off}$ = t$_s$ + t$_f$).
'''

# ---------------------------------------------------------------- FET theory
T['jfet'] = r'''
**Construction.** An n-channel JFET is a bar of n-type silicon with an ohmic contact at each end: the **source (S)** and the **drain (D)**. Two heavily doped p-type regions are diffused on both sides of the bar and joined together as the **gate (G)**. The n-region between the two p-n junctions is the **channel** through which the majority carriers (electrons) flow from S to D. The gate-channel junctions are always **reverse biased** in operation, so the gate current is practically zero (I$_G$ ≈ pA) and the input resistance is very high.

<<fig:jfet_char>>

**Working principle.**
1. *V$_{GS}$ = 0, small V$_{DS}$:* the channel is wide; the drain current rises linearly with V$_{DS}$ (the channel acts as an ohmic resistor).
2. *V$_{GS}$ = 0, V$_{DS}$ increasing:* the reverse bias across the gate junctions is larger near the drain, so the depletion regions widen unequally and the channel narrows toward the drain. At **V$_{DS}$ = V$_P$** (pinch-off voltage in magnitude) the two depletion regions almost touch. Beyond this the current stops increasing and stays at **I$_{DSS}$** (the saturation or pinch-off region); the channel is pinched but carriers still cross it, so I$_D$ is nearly independent of V$_{DS}$ and the JFET behaves as a constant-current source.
3. *V$_{GS}$ negative:* the additional reverse bias widens the depletion layers, narrows the channel, and the pinch-off occurs at the lower voltage V$_{DS(sat)}$ = V$_{GS}$ − V$_P$ (that is, V$_{DS}$ = V$_P$ − |V$_{GS}$|). I$_D$ decreases. At **V$_{GS}$ = V$_P$** (negative, for example −4 V) the channel is completely closed and I$_D$ = 0 (cut-off).

**Characteristics.** *Drain characteristics* (I$_D$ against V$_{DS}$ for steps of V$_{GS}$) have an ohmic region (V$_{DS}$ < V$_{GS}$ − V$_P$), a saturation (constant-current or pinch-off) region used for amplification, and a breakdown region at high V$_{DS}$. The *transfer characteristic* is a parabola from V$_P$ to 0.

**Mathematical expressions.**

$$\begin{gathered}
\text{Shockley equation (saturation):}\quad I_D=I_{DSS}\left(1-\frac{V_{GS}}{V_P}\right)^2,\qquad V_P\le V_{GS}\le 0 \\
\text{Ohmic region:}\quad I_D\approx\frac{2I_{DSS}}{V_P^2}\left[(V_{GS}-V_P)V_{DS}-\frac{V_{DS}^2}{2}\right]\ \ (V_{DS}<V_{GS}-V_P) \\
\text{Transconductance:}\quad g_m=\frac{\partial I_D}{\partial V_{GS}}=g_{m0}\left(1-\frac{V_{GS}}{V_P}\right),\qquad g_{m0}=\frac{2I_{DSS}}{|V_P|} \\
\text{Drain resistance:}\quad r_d=\frac{\Delta V_{DS}}{\Delta I_D}\bigg|_{V_{GS}},\qquad \text{amplification factor }\mu=g_m r_d
\end{gathered}$$
'''

T['dmos'] = r'''
**Construction.** The n-channel depletion-type MOSFET (D-MOSFET) is built on a lightly doped **p-type substrate** (SS) in which two heavily doped **n⁺ regions** are diffused for the source and the drain. A thin **n-type channel is physically built in** between them (by diffusion or implantation). A very thin layer of **SiO$_2$** (about 10 to 100 nm) covers the channel, and the metal **gate** is deposited on the oxide. Source and drain have metal contacts; the substrate is usually connected to the source. Because the gate is insulated by the oxide, the gate current is practically zero (input resistance about 10$^{10}$ to 10$^{15}$ Ω).

<<fig:dmos_char>>

**Working principle.**
- **V$_{GS}$ = 0:** the built-in channel already exists, so for V$_{DS}$ > 0 the electrons flow from S to D and a drain current I$_{DSS}$ flows (at pinch-off).
- **V$_{GS}$ negative (depletion mode):** the negative gate charge repels the electrons of the channel, and the channel is depleted of carriers (narrower), so I$_D$ falls. At V$_{GS}$ = V$_P$ (negative, for example −4 V) the channel is fully depleted and I$_D$ = 0.
- **V$_{GS}$ positive (enhancement mode):** the positive gate attracts more electrons into the channel, enhancing it, and I$_D$ rises above I$_{DSS}$. The D-MOSFET can therefore be operated with either polarity of gate voltage (unlike the JFET).
- **Effect of V$_{DS}$:** as V$_{DS}$ is raised the channel narrows near the drain end and pinches off at V$_{DS}$ = V$_{GS}$ − V$_P$; beyond this I$_D$ is nearly constant (saturation).

**Characteristics.** The *transfer curve* is the Shockley parabola that extends from V$_P$ through I$_{DSS}$ (at V$_{GS}$ = 0) into positive V$_{GS}$; the *drain characteristics* have an ohmic (triode) region and a flat saturation region for each V$_{GS}$ (curves for V$_{GS}$ > 0, = 0 and < 0).

**Mathematical expressions.**

$$\begin{gathered}
I_D=I_{DSS}\left(1-\frac{V_{GS}}{V_P}\right)^2\quad(\text{saturation, }V_{DS}\ge V_{GS}-V_P) \\
I_D=\frac{2I_{DSS}}{V_P^2}\left[(V_{GS}-V_P)V_{DS}-\frac{V_{DS}^2}{2}\right]\quad(\text{triode, }V_{DS}<V_{GS}-V_P) \\
g_m=\frac{2I_{DSS}}{|V_P|}\left(1-\frac{V_{GS}}{V_P}\right)=\frac{2}{|V_P|}\sqrt{I_{DSS}I_D}
\end{gathered}$$
'''

T['emos'] = r'''
**Construction.** The n-channel enhancement MOSFET (E-MOSFET) has a lightly doped **p-type substrate** with two heavily doped **n⁺ islands** (source and drain). A thin **SiO$_2$ layer** covers the surface between them and carries the metal **gate**. Unlike the depletion type there is **no built-in channel**: between the n⁺ regions lies p-type material (two back-to-back p-n junctions), so for V$_{GS}$ = 0 no current flows.

<<fig:emos_char>>

**Working principle.**
1. *V$_{GS}$ = 0 (or below the threshold V$_T$):* the p-region separates source and drain; I$_D$ ≈ 0 (cut-off).
2. *V$_{GS}$ > 0:* the positive gate repels the holes of the p-substrate from the surface and attracts minority electrons, forming first a depletion layer. When V$_{GS}$ exceeds the **threshold voltage V$_T$** (about 1 to 4 V), a thin **inversion layer of electrons (induced n-channel)** connects source and drain. Increasing V$_{GS}$ further widens this channel and increases I$_D$ (the device is "enhanced").
3. *Effect of V$_{DS}$:* for small V$_{DS}$ the channel behaves as a resistor (ohmic or triode region). As V$_{DS}$ increases the channel at the drain end thins (the gate-to-channel voltage there is V$_{GD}$ = V$_{GS}$ − V$_{DS}$), and at V$_{DS}$ = V$_{GS}$ − V$_T$ the channel **pinches off** at the drain; for larger V$_{DS}$ the current saturates.

**Drain characteristic.** Plot of I$_D$ against V$_{DS}$ for V$_{GS}$ = V$_T$ + 1, + 2, ... V: each curve rises (ohmic region, the parabola) up to V$_{DS(sat)}$ = V$_{GS}$ − V$_T$, then is flat (saturation region, constant-current), and the locus of the pinch-off points is the parabola I$_D$ = k V$_{DS}^2$. For V$_{GS}$ ≤ V$_T$ the device is cut off.

**Mathematical expressions.**

$$\begin{gathered}
I_D=k\,(V_{GS}-V_T)^2\quad(\text{saturation, }V_{DS}\ge V_{GS}-V_T,\ V_{GS}>V_T) \\
I_D=2k\left[(V_{GS}-V_T)V_{DS}-\frac{V_{DS}^2}{2}\right]\quad(\text{triode, }V_{DS}<V_{GS}-V_T) \\
k=\frac{I_{D(on)}}{(V_{GS(on)}-V_T)^2}=\frac{1}{2}\mu_nC_{ox}\frac{W}{L},\qquad g_m=\frac{\partial I_D}{\partial V_{GS}}=2k(V_{GS}-V_T)
\end{gathered}$$
'''
