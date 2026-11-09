"""Assemble the four Electronic Device and Circuits (ENEX/EX 151) papers.
Run with the micromamba python from this directory:  python3 gen.py <outdir>"""
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import F
from texts_a import T, design_div, design_cc
from texts_b import U

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
F['cc_design'] = r'''
fig,ax=ckt_canvas(4.8,3.4,xlim=(-1.4,8.4),ylim=(-0.8,7.8))
terminal(ax,(3.2,7.3)); label(ax,(3.7,7.3),"+V$_{CC}$",ha="left",size=8.6); wire(ax,[(3.2,7.3),(3.2,6.6)])
wire(ax,[(1.2,6.6),(3.2,6.6)]); node(ax,(3.2,6.6))
res(ax,(1.2,6.6),(1.2,3.8),"R$_1$",side=-1,off=0.5,body=0.9); node(ax,(1.2,3.8)); res(ax,(1.2,3.8),(1.2,0.4),"R$_2$",side=-1,off=0.5,body=0.9)
bj=bjt(ax,2.6,3.8); wire(ax,[(1.2,3.8),bj["B"]]); wire(ax,[bj["C"],(3.2,6.6)])
cap(ax,(-0.9,3.8),(0.1,3.8),"C$_1$",side=1,gap=0.2); wire(ax,[(0.1,3.8),(1.2,3.8)]); terminal(ax,(-1.3,3.8)); wire(ax,[(-1.3,3.8),(-0.9,3.8)]); label(ax,(-1.3,4.25),"v$_i$",size=8.6)
wire(ax,[bj["E"],(3.2,2.0)]); node(ax,(3.2,2.0)); res(ax,(3.2,2.0),(3.2,0.4),"R$_E$",side=1,off=0.5,body=0.9)
wire(ax,[(3.2,2.0),(4.4,2.0)]); cap(ax,(4.4,2.0),(5.6,2.0),"C$_2$",side=1,gap=0.2); wire(ax,[(5.6,2.0),(6.2,2.0)]); terminal(ax,(6.2,2.0)); label(ax,(6.6,2.0),"v$_o$",ha="left",size=8.6)
wire(ax,[(1.2,0.4),(3.2,0.4)]); gnd(ax,(2.2,0.4)); node(ax,(2.2,0.4))
'''

def fig(name, cap):
    return '\n```figure caption="%s"\n%s\n```\n' % (cap, F[name].strip())

def expand(s):
    out = s
    for k in list(F):
        tok = '<<fig:%s>>' % k
        if tok in out:
            out = out.replace(tok, fig(k, FIGCAP.get(k, k)))
    return out

FIGCAP = {
 'cb_ss': 'Small-signal (r$_e$) model of the common-base amplifier.',
 'ce_ss': 'Hybrid-π small-signal model of the common-emitter amplifier (R$_E$ unbypassed; R$_E$ = 0 when bypassed).',
 'cc_ss': 'Small-signal model of the common-collector amplifier.',
 'cc_design': 'Designed common-collector amplifier with voltage-divider bias.',
 'bjt_switch': 'BJT switch: circuit and load line with the two operating points.',
 'jfet_char': 'n-channel JFET: structure, drain characteristics and transfer curve.',
 'dmos_char': 'n-channel depletion MOSFET: structure, transfer curve and drain characteristics.',
 'emos_char': 'n-channel enhancement MOSFET: structure, transfer curve and drain characteristics.',
 'wien': 'Wien bridge oscillator.', 'rcphase': 'RC phase-shift oscillator (three sections).',
 'hartley': 'Hartley oscillator.', 'colpitts': 'Colpitts oscillator.',
 'mirror_comp': 'Current mirror with base-current compensation (Q$_3$).', 'widlar': 'Widlar current source.',
 'classA_tc': 'Transformer-coupled class A amplifier and its a.c. load line.',
 'classB_pp': 'Transformer-coupled class B push-pull amplifier; each transistor conducts for half a cycle.',
 'crossover': 'Crossover distortion in class B and its removal in class AB.',
 'f555': '555 timer astable multivibrator and its waveforms.', 'tuned': 'Class A tuned amplifier and its frequency response.',
 'diffamp': 'Differential amplifier with an active (current-mirror) load.',
 'series_prot': 'Series transistor regulator with a short-circuit (current-limiting) protection transistor Q$_2$.',
 'lm317': 'Adjustable regulator with the LM317.',
}

# ---------------------------------------------------------------- FET bias solutions
def solve_dep(VDD, R1, R2, RD, RS, VP, IDSS, label, what='depletion'):
    VG = VDD * R2 / (R1 + R2)
    a = 1 - VG / VP; b = RS / VP          # (kOhm, mA)
    A = IDSS * b * b; B = 2 * IDSS * a * b - 1; C = IDSS * a * a
    D = B * B - 4 * A * C
    r1 = (-B - math.sqrt(D)) / (2 * A); r2 = (-B + math.sqrt(D)) / (2 * A)
    roots = sorted([r1, r2])
    ID = [r for r in roots if VG - r * RS >= VP][0]
    bad = [r for r in roots if r != ID][0]
    VGS = VG - ID * RS; VDS = VDD - ID * (RD + RS)
    gm = 2 * IDSS / abs(VP) * (1 - VGS / VP)
    s = r'''
**Solution** (R in kΩ, I in mA, V in V). The gate current is zero, so the divider fixes the gate voltage:

$$V_G=\frac{R_2}{R_1+R_2}V_{DD}=\frac{%g}{%g+%g}(%g)=%.4f\ \text{V}$$

The gate-source voltage is V$_{GS}$ = V$_G$ − I$_D$R$_S$ = %.4f − %g I$_D$ and the device equation is I$_D$ = I$_{DSS}$(1 − V$_{GS}$/V$_P$)² = %g(1 − V$_{GS}$/(%g))². Substituting,

$$I_D=%g\,(%.4f%+.4f\,I_D)^2\ \ \Rightarrow\ \ %.4f\,I_D^2%+.4f\,I_D+%.4f=0$$

$$I_D=\frac{-B\pm\sqrt{B^2-4AC}}{2A}\ \ \Rightarrow\ \ I_D=%.3f\ \text{mA}\ \ \text{or}\ \ %.3f\ \text{mA}$$

The root I$_D$ = %.3f mA gives V$_{GS}$ = %.2f V, which lies beyond cut-off (V$_{GS}$ < V$_P$ = %g V), so it is rejected. Therefore

$$\begin{gathered}
I_D=%.3f\ \text{mA}\\
V_{GS}=V_G-I_DR_S=%.4f-(%.3f)(%g)=%.3f\ \text{V}\ \ (>V_P)\\
V_{DS}=V_{DD}-I_D(R_D+R_S)=%g-%.3f(%g+%g)=%.3f\ \text{V}
\end{gathered}$$

*Check of the region.* V$_{DS}$ = %.3f V > V$_{GS}$ − V$_P$ = %.3f V, so the transistor is in **saturation (pinch-off region)** and the Shockley equation is valid. Also g$_m$ = (2I$_{DSS}$/|V$_P$|)(1 − V$_{GS}$/V$_P$) = %.3f mS.
''' % (R2, R1, R2, VDD, VG, VG, RS, IDSS, VP, IDSS, a, b, A, B, C, roots[0], roots[1], bad, VG - bad * RS, VP, ID, VG, ID, RS, VGS, VDD, ID, RD, RS, VDS, VDS, VGS - VP, gm)
    return s, dict(VG=VG, ID=ID, VGS=VGS, VDS=VDS, gm=gm)

def solve_enh(VDD, R1, R2, RD, RS, K, Vt):
    VG = VDD * R2 / (R1 + R2)
    A = K * RS * RS; B = -(2 * K * RS * (VG - Vt) + 1); C = K * (VG - Vt) ** 2
    D = B * B - 4 * A * C
    roots = sorted([(-B - math.sqrt(D)) / (2 * A), (-B + math.sqrt(D)) / (2 * A)])
    ID = [r for r in roots if VG - r * RS > Vt][0]
    VGS = VG - ID * RS; VDS = VDD - ID * (RD + RS)
    s = r'''
**Solution** (R in kΩ, I in mA, K in mA/V²). Gate current is zero, so

$$V_G=\frac{R_2}{R_1+R_2}V_{DD}=\frac{%g}{%g+%g}(%g)=%.2f\ \text{V}$$

For the enhancement MOSFET in saturation I$_D$ = K(V$_{GS}$ − V$_t$)² with V$_{GS}$ = V$_G$ − I$_D$R$_S$ = %.2f − %g I$_D$:

$$I_D=%.2f\,(%.2f-%g\,I_D-%g)^2=%.2f\,(%.2f-%g\,I_D)^2$$

$$%.2f\,I_D^2-%.4f\,I_D+%.4f=0\ \ \Rightarrow\ \ I_D=%.3f\ \text{mA}\ \ \text{or}\ \ %.3f\ \text{mA}$$

The larger root gives V$_{GS}$ = %.2f − %g(%.3f) = %.2f V, which is below V$_t$ (transistor cut off), so it is rejected. Hence

$$\begin{gathered}
I_D=%.3f\ \text{mA}\ (\approx %.0f\ \mu\text{A})\\
V_{GS}=%.2f-%g(%.3f)=%.3f\ \text{V}\ (>V_t=%g\ \text{V})\\
V_{DS}=V_{DD}-I_D(R_D+R_S)=%g-%.3f(%g+%g)=%.3f\ \text{V}
\end{gathered}$$

*Check:* V$_{DS}$ = %.3f V > V$_{GS}$ − V$_t$ = %.3f V, so the device is in saturation and the square-law is valid.
''' % (R2, R1, R2, VDD, VG, VG, RS, K, VG, RS, Vt, K, VG - Vt, RS, A, -B, C, roots[0], roots[1],
       VG, RS, roots[1], VG - roots[1] * RS, ID, ID * 1e3, VG, RS, ID, VGS, Vt, VDD, ID, RD, RS, VDS, VDS, VGS - Vt)
    return s

# ---------------------------------------------------------------- LM317 designs
def lm317(vlo, vhi, fixed, pot, vin):
    R1 = 240.0
    lo = 1.25 * (1 + fixed / R1); hi = 1.25 * (1 + (fixed + pot) / R1)
    need_lo = R1 * (vlo / 1.25 - 1); need_hi = R1 * (vhi / 1.25 - 1)
    return r'''
**Design with the LM317.** The LM317 keeps a constant reference of **V$_{ref}$ = 1.25 V** between its OUT and ADJ terminals, so the current through R$_1$ is fixed at 1.25/R$_1$ and the same current (plus the small adjust current I$_{ADJ}$ ≈ 50 µA) flows through R$_2$:

$$V_o=V_{ref}\left(1+\frac{R_2}{R_1}\right)+I_{ADJ}R_2\ \approx\ 1.25\left(1+\frac{R_2}{R_1}\right)$$

<<fig:lm317>>

*Choice of R$_1$.* The regulator needs a minimum load current of 3.5 to 10 mA, so R$_1$ = 1.25 V/5.2 mA ≈ **240 Ω** (standard value; 120 Ω to 240 Ω is the usual range).

*Value of R$_2$ for the two ends of the range* (R$_2$ = R$_1$(V$_o$/1.25 − 1)):

$$\begin{gathered}
V_{o(min)}=%g\ \text{V}:\quad R_{2(min)}=240\left(\frac{%g}{1.25}-1\right)=%.0f\ \Omega \\
V_{o(max)}=%g\ \text{V}:\quad R_{2(max)}=240\left(\frac{%g}{1.25}-1\right)=%.0f\ \Omega
\end{gathered}$$

So R$_2$ must be variable from %.0f Ω to %.0f Ω. Use a **fixed resistor of %g Ω in series with a %g Ω potentiometer** (the fixed part sets the minimum voltage): R$_2$ varies from %g Ω to %g Ω, giving V$_o$ from 1.25(1+%g/240) = %.2f V to 1.25(1+%g/240) = %.2f V, which covers the required %g to %g V (the pot is trimmed to stop at %g V).

*Other components.* C$_1$ = 0.1 µF at the input (when the regulator is far from the filter capacitor) and C$_2$ = 1 µF tantalum (or 10 µF) at the output for stability and transient response; a diode across the regulator protects against the discharge of C$_2$ into the output when the input is shorted. The unregulated input must satisfy V$_{in}$ ≥ V$_{o(max)}$ + 3 V (dropout), i.e. V$_{in}$ ≈ %g V (up to the 40 V maximum differential), and the regulator delivers up to 1.5 A with a heat sink (P$_D$ = (V$_{in}$ − V$_o$)I$_o$). Line and load regulation are about 0.01 percent per volt and 0.1 percent.
''' % (vlo, vlo, need_lo, vhi, vhi, need_hi, need_lo, need_hi, fixed, pot, fixed, fixed + pot, fixed, lo, fixed + pot, hi, vlo, vhi, vhi, vin)

# ---------------------------------------------------------------- other shared blocks
V = {}
V['f555'] = r'''
**555 timer as an astable multivibrator.** Pins 2 (trigger) and 6 (threshold) are joined and connected to the capacitor C; R$_A$ goes from V$_{CC}$ to the discharge pin 7 and R$_B$ from pin 7 to C. Internally three equal 5 kΩ resistors fix the comparator levels V$_{CC}$/3 (lower trigger level) and 2V$_{CC}$/3 (upper threshold level).

<<fig:f555>>

*Charging (output HIGH).* The discharge transistor is off and C charges through R$_A$ + R$_B$ toward V$_{CC}$ from V$_{CC}$/3 up to 2V$_{CC}$/3. With v$_C$(t) = V$_{CC}$ − (V$_{CC}$ − V$_{CC}$/3)e$^{-t/τ_1}$ and τ$_1$ = (R$_A$+R$_B$)C, set v$_C$ = 2V$_{CC}$/3:

$$\frac{2V_{CC}}{3}=V_{CC}-\frac{2V_{CC}}{3}e^{-T_H/\tau_1}\ \Rightarrow\ e^{-T_H/\tau_1}=\frac12\ \Rightarrow\ T_H=0.693\,(R_A+R_B)\,C$$

*Discharging (output LOW).* At 2V$_{CC}$/3 the upper comparator resets the flip-flop; the output goes low and pin 7 grounds, so C discharges through R$_B$ only: v$_C$(t) = (2V$_{CC}$/3)e$^{-t/τ_2}$ with τ$_2$ = R$_BC$ until v$_C$ = V$_{CC}$/3:

$$\frac{V_{CC}}{3}=\frac{2V_{CC}}{3}e^{-T_L/\tau_2}\ \Rightarrow\ T_L=0.693\,R_B\,C$$

*Period, frequency and duty cycle.*

$$\begin{gathered}
T=T_H+T_L=0.693\,(R_A+2R_B)\,C \\
f=\frac{1}{T}=\frac{1.44}{(R_A+2R_B)\,C} \\
D=\frac{T_H}{T}=\frac{R_A+R_B}{R_A+2R_B}\ (>50\ \text{percent})
\end{gathered}$$

The frequency is independent of V$_{CC}$ because both thresholds are proportional to V$_{CC}$. *Example:* R$_A$ = 1 kΩ, R$_B$ = 10 kΩ, C = 0.1 µF: f = 1.44/(21 kΩ × 0.1 µF) = 686 Hz, T$_H$ = 0.693 × 11 k × 0.1 µ = 0.762 ms, T$_L$ = 0.693 ms, D = 52.4 percent. A duty cycle of 50 percent or less needs a diode across R$_B$.
'''

V['tuned'] = r'''
**Class A tuned amplifier (single tuned).** A CE amplifier has a parallel LC tank (L with its series resistance, C) as the collector load. At resonance the tank impedance is a pure and large resistance, so the gain is maximum; away from resonance the tank impedance falls, so the amplifier is selective (used in radio and IF amplifiers).

<<fig:tuned>>

Resonance frequency f$_o$ = 1/(2π√(LC)). Near resonance the tank impedance is

$$Z(f)=\frac{R_p}{1+jQ\left(\dfrac{f}{f_o}-\dfrac{f_o}{f}\right)},\qquad Q=\frac{R_p}{\omega_oL}=\omega_oCR_p$$

where R$_p$ is the equivalent parallel resistance (the coil loss resistance in parallel with r$_o$ and the load). With a transconductance g$_m$ the voltage gain is A$_v$ = −g$_m$Z, so

$$|A_v|=\frac{A_{max}}{\sqrt{1+Q^2\left(\dfrac{f}{f_o}-\dfrac{f_o}{f}\right)^2}},\qquad A_{max}=g_mR_p$$

**3 dB bandwidth.** The gain drops to A$_{max}$/√2 when Q(f/f$_o$ − f$_o$/f) = ±1. Solving the two quadratics f² ∓ (f$_o$/Q)f − f$_o^2$ = 0 for the positive roots:

$$f_{1,2}=f_o\left[\sqrt{1+\frac{1}{4Q^2}}\mp\frac{1}{2Q}\right]\ \Rightarrow\ f_2-f_1=\frac{f_o}{Q},\qquad f_1f_2=f_o^2$$

$$\boxed{\ BW=f_2-f_1=\frac{f_o}{Q}\ }$$

so a higher Q gives a narrower bandwidth and a sharper response (for Q > 10, f$_{1,2}$ ≈ f$_o$ ∓ BW/2). *Example:* f$_o$ = 1 MHz, Q = 50 gives BW = 20 kHz; with a heavy load, R$_p$ and hence Q fall and the bandwidth rises.
'''

V['diffamp'] = r'''
**Differential amplifier with an active load.** Q$_1$, Q$_2$ form the differential pair biased by the tail current I$_{EE}$ (I$_{E1}$ = I$_{E2}$ = I$_{EE}$/2); both have the transconductance g$_m$ = I$_C$/V$_T$. In place of the resistors R$_C$, the collectors are loaded by a pnp **current mirror** (Q$_3$ diode-connected, Q$_4$ output). The output is taken from the collector of Q$_2$. Let v$_d$ = v$_1$ − v$_2$.

<<fig:diffamp>>

*(a) Passive (resistor) load, single-ended output.* By symmetry a differential input v$_d$ divides equally: the collector current of Q$_2$ changes by g$_m$(v$_d$/2) and that of Q$_1$ by −g$_m$(v$_d$/2). The output at one collector with the load R (the total resistance at the output node, e.g. R$_C$ ∥ r$_{o2}$):

$$v_o=-g_m\frac{v_d}{2}R\ \Rightarrow\ A_d(\text{passive})=\frac{v_o}{v_d}=\frac{g_mR}{2}$$

*(b) Active load.* The change of collector current of Q$_1$ is −g$_m$v$_d$/2 (it flows into the diode Q$_3$) and is **mirrored by Q$_4$ as an equal and opposite current, i.e. +g$_m$v$_d$/2 into the output node**, while Q$_2$ adds +g$_m$v$_d$/2 itself. Both halves of the differential signal therefore appear at the single output, and the output current is

$$i_o=\frac{g_mv_d}{2}+\frac{g_mv_d}{2}=g_mv_d$$

The resistance at the output node is R$_o$ = r$_{o2}$ ∥ r$_{o4}$ = R (the same resistance as in (a)). Hence

$$A_d(\text{active})=\frac{v_o}{v_d}=g_m\,(r_{o2}\parallel r_{o4})=g_mR$$

*Comparison for the same output resistance R:*

$$\frac{A_d(\text{active})}{A_d(\text{passive})}=\frac{g_mR}{g_mR/2}=2$$

So the single-ended gain with an active load is **twice** that with a passive load (the mirror recovers the half of the signal that the passive load wastes in the other collector). In addition the active load gives a very large R (r$_o$ ≈ 100 kΩ or more) so that gains of several thousand are possible with no large resistors and no large voltage drop.
'''

V['series_basic'] = r'''
**Discrete series regulator.** A pass transistor Q$_1$ (emitter follower) is in series with the load. A Zener diode D$_Z$ fed through R$_1$ gives a constant reference voltage V$_Z$ at the base:

$$V_o=V_Z-V_{BE1}$$

*Regulation action:* if the input rises (or the load current falls) V$_o$ tends to rise, V$_{BE1}$ = V$_Z$ − V$_o$ falls, I$_{B1}$ and hence the collector current fall, V$_{CE1}$ rises and takes up the extra input voltage, so V$_o$ returns almost to its old value. The load current is supplied through the transistor, so the Zener only has to supply I$_{B1}$ = I$_L$/(β+1), and the Zener current is made nearly independent of the load.

**Stability factor (line regulation) S$_V$ = ΔV$_o$/ΔV$_i$** for a constant load. A change ΔV$_i$ divides between R$_1$ and the dynamic resistance r$_z$ of the Zener (the base-looking resistance (β+1)(r$_e$+R$_L$) is very large and is in parallel with r$_z$, so it is neglected):

$$\Delta V_Z=\Delta V_i\,\frac{r_z}{R_1+r_z}$$

The emitter follows the base with the gain A$_v$ = R$_L$/(R$_L$ + r$_e$) ≈ 1 (ΔV$_{BE}$ ≈ r$_e$ΔI$_E$ is small), so

$$\Delta V_o=\Delta V_Z\,\frac{R_L}{R_L+r_e}\ \Rightarrow\ \boxed{\ S_V=\frac{\Delta V_o}{\Delta V_i}=\frac{r_z}{R_1+r_z}\cdot\frac{R_L}{R_L+r_e}\ \approx\ \frac{r_z}{R_1+r_z}\ }$$

Since r$_z$ ≪ R$_1$, S$_V$ is small (for example r$_z$ = 10 Ω, R$_1$ = 500 Ω gives S$_V$ = 10/510 = 0.0196, i.e. a 10 V change at the input produces only 0.2 V at the output); the smaller the stability factor, the better the regulation. Similarly the output resistance R$_{out}$ = r$_e$ + r$_z$∥R$_1$/(β+1) is very small (about 1 Ω), which gives a good load regulation. The percent regulation can be improved further by using a Darlington pass transistor, a constant-current source in place of R$_1$ or an error amplifier (see the improved circuit).
'''

V['series_prot'] = r'''
**Short-circuit / overload (current-limit) protection.** A small sense resistor R$_{SC}$ is placed in series with the load and a second transistor Q$_2$ is connected with its base-emitter across R$_{SC}$ and its collector at the base of the pass transistor Q$_1$.

<<fig:series_prot>>

*Normal load.* The load current I$_L$ flows through R$_{SC}$ and produces V$_{R_{SC}}$ = I$_LR_{SC}$ < 0.5 V, so Q$_2$ is off and the regulator works as above. *Overload or short circuit.* When I$_L$ rises until I$_LR_{SC}$ ≈ V$_{BE2}$ (≈ 0.6 to 0.7 V), Q$_2$ conducts and **diverts the base current of Q$_1$** (taking it from the R$_1$/Zener node), so the base drive of Q$_1$ falls and the output current is held at

$$I_{L(max)}=I_{SC}\approx\frac{V_{BE2}}{R_{SC}}=\frac{0.65\ \text{V}}{R_{SC}}$$

*Design:* for I$_{L(max)}$ = 1 A, R$_{SC}$ = 0.65 Ω (≈ 0.68 Ω, rated at least I²R = 0.7 W); the output voltage falls as the load resistance falls but the current cannot exceed I$_{SC}$, so the pass transistor does not burn out (its dissipation in a short is P$_D$ ≈ V$_i$I$_{SC}$, which the heat sink must withstand; foldback limiting reduces this). Practical designs also include R$_{SC}$ ≈ 0.5 Ω-class values and a fuse.
'''

V['series_improved'] = r'''
**Series regulator with improved performance (error amplifier, closed-loop).** A Darlington pass element Q$_1$ is driven by a d.c. **error amplifier** Q$_2$. A sampling divider R$_3$, R$_4$ across the output gives the sample V$_s$ = V$_oR_4/(R_3+R_4)$, which is compared with a Zener reference V$_Z$ at the emitter of Q$_2$. The collector of Q$_2$ drives Q$_1$ (resistor R$_1$ from the input).

*Operation.* If V$_o$ increases, V$_s$ increases, V$_{BE2}$ = V$_s$ − V$_Z$ increases, Q$_2$ conducts more and takes more of the drive current from the base of Q$_1$; Q$_1$ conducts less and the output falls back. If V$_o$ falls, the action is reversed. The output voltage is set by

$$V_o=\frac{R_3+R_4}{R_4}\,(V_Z+V_{BE2})$$

and is adjustable with a potentiometer in the divider. **Why the performance improves:** the output is compared with a stable reference and the difference is amplified by the gain of Q$_2$ and of the pass transistor(s), so the regulation is much better than that of the simple Zener-follower, and the output resistance is smaller.

**Voltage stability factor.** Let the error amplifier gain be A$_e$ (≈ g$_{m2}$R$_{C2}$, R$_{C2}$ the load of Q$_2$ in parallel with the input resistance of Q$_1$), the pass stage gain A$_p$ ≈ 1 (emitter follower), and the sampling fraction β$_s$ = R$_4$/(R$_3$+R$_4$). A change ΔV$_i$ acts as a disturbance that enters through R$_1$ and, without feedback, changes the output by ΔV$_o$(open) = S$_0$ΔV$_i$ with S$_0$ ≈ 1/μ (μ is small-signal amplification of the pass stage; for the Zener-follower S$_0$ = r$_z$/(R$_1$+r$_z$)). With negative feedback, the loop gain is T = A$_eA_p\beta_s$ and

$$\Delta V_o=S_0\Delta V_i-T\,\Delta V_o\ \ \Rightarrow\ \ \boxed{\ S_V=\frac{\Delta V_o}{\Delta V_i}=\frac{S_0}{1+A_eA_p\beta_s}\ }$$

so the line regulation is improved by the factor (1 + A$_eA_p$β$_s$), typically 100 to 1000, giving S$_V$ of about 0.01 to 0.1 percent per volt. *Example:* S$_0$ = 0.02, A$_e$ = 200, A$_p$ = 1, β$_s$ = 0.5: S$_V$ = 0.02/101 = 1.98 × 10⁻⁴, i.e. 0.2 mV change at the output for a 1 V change at the input. The output resistance is similarly reduced from R$_o$ to R$_o$/(1+T), and the current-limit transistor of the previous question can be added.
'''

V['cb_note'] = ''

def block_hdr(s):
    return s.strip('\n') + '\n'

def emit(pid, front, qs, sols):
    body = front + '\n'
    for i, (q, figs) in enumerate(qs, 1):
        body += '\n@q %d\n%s\n' % (i, q.strip())
        for f_, cap in figs:
            body += fig(f_, cap)
    body += '<!-- SOLUTIONS -->\n'
    for i, s in enumerate(sols, 1):
        body += '\n@s %d\n%s\n' % (i, expand(s.strip('\n')))
    open(os.path.join(OUT, pid + '.md'), 'w').write(body)
    print(pid, len(qs), len(sols))

def header(file_, code, yr, yad, students):
    return ('---\nfile: %s\nsubject: Electronic Device and Circuits\nlevel: BE · Year I / Part II\ncode: %s\nyear_bs: %s\ncal: BS\nyear_ad: %s\n'
            'stream: BEI, BCT\ntime: 3 hrs\nmarks: 60\nstudents: Tribhuvan University, Institute of Engineering, Examination Control Division. %s Pass marks 24.\n'
            'category: University Exam\n---\n<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>\n') % (file_, code, yr, yad, students)

def ex(q, cap=None):
    return q

# ================================================================ PAPER 1: ENEX 151 2083 Baishakh (back)
def paper1():
    dm_text, dm = solve_dep(16, 2100, 270, 2.4, 1.5, -4, 8, '')
    dm_text, dm = solve_dep(16, 2.1e3, 270, 2.4, 1.5, -4, 8, '')
    vp, vcc, rl = 20.0, 30.0, 16.0
    Ip = vp / rl; Idc = 2 * Ip / math.pi; Pin = vcc * Idc; Po = vp * vp / (2 * rl); eta = Po / Pin * 100
    q = [
     ("Why BJT is bipolar and FET is unipolar? Design β-independent type DC biased common collector amplifier. Given parameters are: V$_{CC}$ = 20 V, I$_C$ = 2 mA, and β = 100. Use firm biasing method. [[1+5]]", []),
     ("Explain the role of bypass capacitor in amplifier circuits. Draw the small signal equivalent circuit of a common base amplifier circuit and find its input impedance, output impedance and voltage gain. [[2+5]]", []),
     ("Describe the construction and working principle of N Channel D-MOSFET with the help of characteristic curves and mathematical expressions. [[6]]", []),
     ("Find I$_D$ and V$_{DS}$ for the given circuit. Given parameters: V$_P$ = −4 V and I$_{DSS}$ = 8 mA. [[7]]", [('prob_dmos', 'Question 4: n-channel depletion MOSFET with voltage-divider bias, V$_{DD}$ = +16 V, R$_1$ = 2.1 MΩ, R$_2$ = 270 kΩ, R$_D$ = 2.4 kΩ, R$_S$ = 1.5 kΩ.')]),
     ("What is the main difference between RC and LC oscillator circuits in terms of application? Explain the operation of Wien Bridge Oscillator circuit with the help of circuit diagram and necessary mathematical expressions. [[1+5]]", []),
     ("Explain how a base current compensation circuit reduces the difference between I0 and IREF in a simple current mirror circuit. [[5+2]]", []),
     ("For a class B amplifier providing a 20 V peak signal to a 16 Ω load (speaker) and a power supply of V$_{CC}$ = 30 V, determine the input power, output power, and circuit efficiency. [[6]]", []),
     ("Draw the circuit diagram and the characteristic curve of a transformer-coupled class A amplifier and derive its general and maximum efficiency. [[7]]", []),
     ("Derive the expression for stability factor of a discrete-transistor series regulator. [[4]]", []),
     ("Design a variable DC voltage regulator using the LM317 to output (3-15) volts. [[4]]", []),
    ]
    s7 = T_cb_b = r'''
Given V$_p$ = %g V, R$_L$ = 16 Ω, V$_{CC}$ = %g V. The two transistors of the push-pull class B stage conduct alternately, each for 180°.

$$\begin{gathered}
I_p=\frac{V_p}{R_L}=\frac{%g}{16}=%.4f\ \text{A},\qquad I_{dc}=\frac{2I_p}{\pi}=\frac{2(%.4f)}{\pi}=%.4f\ \text{A} \\
\textbf{Input power:}\quad P_{in}=V_{CC}I_{dc}=%g\times %.4f=\mathbf{%.2f\ W}\\
\textbf{Output power:}\quad P_o=\frac{V_p^2}{2R_L}=\frac{%g^2}{2(16)}=\mathbf{%.2f\ W}\\
\textbf{Efficiency:}\quad \eta=\frac{P_o}{P_{in}}\times100=\frac{%.2f}{%.2f}\times100=\mathbf{%.1f\ percent}
\end{gathered}$$

*Check with the general formula:* η = (π/4)(V$_p$/V$_{CC}$) = 0.7854 × (%g/%g) = %.1f percent. The power dissipated in the two transistors is P$_D$ = P$_{in}$ − P$_o$ = %.2f − %.2f = %.2f W (%.2f W in each). The result is below the theoretical 78.5 percent maximum because V$_p$ is only 2/3 of V$_{CC}$.
''' % (vp, vcc, vp, Ip, Ip, Idc, vcc, Idc, Pin, vp, Po, Po, Pin, eta, vp, vcc, math.pi / 4 * vp / vcc * 100, Pin, Po, Pin - Po, (Pin - Po) / 2)
    sol = [
     T['bipolar_unipolar'] + design_cc(20, 2, 100),
     T['cb'],
     T['dmos'],
     "The n-channel D-MOSFET is biased by a voltage divider with source resistor (self-bias plus divider).\n\n<<fig:prob_dmos>>\n" + dm_text,
     U['rc_vs_lc'] + U['wien'],
     U['mirror_comp'],
     s7,
     U['classA_tc'],
     V['series_basic'],
     lm317(3, 15, 330, 2500, 18),
    ]
    emit('ioe-enex151-2083-baishakh', header('NEBians-IOE-Past-Paper-Electronic-Device-and-Circuits-ENEX151-2083-Baishakh.pdf', 'ENEX 151', '2083 Baishakh', 2026, 'Back paper (new course).'), q, sol)

# ================================================================ PAPER 2: ENEX 151 2082 Bhadra
def paper2():
    em = solve_enh(10, 11e3, 11e3, 6, 6, 0.48, 1)
    q = [
     ("What is the significance of β-independency in a voltage divider biasing circuit? Design a β-independent voltage divider bias circuit for the given parameters: V$_{CC}$ = 15 V, I$_E$ = 1 mA and β = 100. [[1+5]]", []),
     ("Explain the role of coupling capacitors in amplifier circuits. Draw the small signal equivalent circuit of a common emitter amplifier circuit and find its input impedance, output impedance and voltage gain. [[2+5]]", []),
     ("Describe the construction and working principle of n-channel JFET with the help of characteristic curves and mathematical expressions. [[6]]", []),
     ("Find I$_D$ and V$_{DS}$ for the circuit shown in the figure below. Given parameters are: V$_t$ = 1 V and K = 0.48 mA/V$^2$. [[7]]", [('prob_emos', 'Question 4: n-channel enhancement MOSFET, V$_{DD}$ = +10 V, R$_1$ = R$_2$ = 11 MΩ, R$_D$ = R$_S$ = 6 kΩ.')]),
     ("State Barkhausen criteria for sinusoidal oscillation. Explain the working principle of RC phase shift oscillator with necessary expression and circuit diagram. [[6]]", []),
     ("With a neat circuit diagram and necessary mathematical expressions, explain the operation of Widlar current source. What is the advantage of Widlar current source over simple current source? [[5+2]]", []),
     ("Draw the circuit diagram of transformer coupled Class B amplifier. Determine the condition for minimum efficiency of Class B amplifier. [[6]]", []),
     ("Define crossover distortion in a class B amplifier and explain how class AB operation can be used to eliminate it. [[6]]", []),
     ("Explain the working principle of a series transistor voltage regulator, accompanied by short-circuit/overload protection. [[5]]", []),
     ("Design a 10-25 V variable DC voltage regulator using LM317 IC. [[4]]", []),
    ]
    s1 = r'''
**Significance of β-independence.** The current gain β of a transistor is not a fixed number: it differs by a factor of 2 to 3 between two transistors of the same type, and it changes with temperature and with the collector current. If the Q-point (I$_C$, V$_{CE}$) depended on β, every replaced transistor or every temperature change would move the operating point towards saturation or cut-off, causing distortion and clipping. A **β-independent (stiff, voltage-divider) bias** makes I$_C$ ≈ (V$_B$ − V$_{BE}$)/R$_E$, which depends only on the stable resistors and the supply, so the Q-point is almost fixed, the stage is thermally stable (the emitter resistor gives d.c. negative feedback) and the gain, which depends on r$_e$ = 26 mV/I$_E$, is predictable. The stability factor S = ΔI$_C$/ΔI$_{CO}$ ≈ 1 + R$_B$/R$_E$ is small.
''' + design_div(15, 1, 100, 1.5, 7.5)
    sol = [
     s1, T['ce'], T['jfet'],
     "The enhancement MOSFET is biased by the voltage divider (V$_{DD}$ = 10 V, R$_1$ = R$_2$ = 11 MΩ) with R$_D$ = R$_S$ = 6 kΩ.\n\n<<fig:prob_emos>>\n" + em,
     U['barkhausen'] + U['rcphase'],
     U['widlar'] + "\n**Advantage over the simple current source.** To obtain a small output current such as 10 µA from I$_{REF}$ = 1 mA a simple mirror needs a 100:1 resistor ratio (or a very large R of about 1 MΩ, which takes a large area on a chip); the Widlar source needs only R$_E$ ≈ 12 kΩ. It also has a **much higher output resistance** (r$_o$[1 + g$_m$(R$_E$∥r$_π$)] instead of r$_o$), so the output current is independent of the load, and I$_O$ is less sensitive to supply voltage variations and to base-current error.\n",
     U['classB_tc'],
     U['crossover'],
     V['series_basic'] + V['series_prot'],
     lm317(10, 25, 1680, 3000, 28),
    ]
    emit('ioe-enex151-2082-bhadra', header('NEBians-IOE-Past-Paper-Electronic-Device-and-Circuits-ENEX151-2082-Bhadra.pdf', 'ENEX 151', '2082 Bhadra', 2025, 'Regular (new course).'), q, sol)

# ================================================================ PAPER 3: EX 151 2082 Baishakh (back)
def paper3():
    jf, jv = solve_dep(20, 910, 110, 2.2, 1.1, -3.5, 10, '')
    Vcc = 30.0; RL = 16.0
    Ip = Vcc / RL; Pin = 2 * Vcc ** 2 / (math.pi * RL); Po = Vcc ** 2 / (2 * RL); eta = Po / Pin * 100
    vpd = 2 * Vcc / math.pi; Ipd = vpd / RL; Pd_max = 2 * Vcc ** 2 / (math.pi ** 2 * RL)
    q = [
     ("Design a β-independent voltage divider bias circuit using the appropriate guidelines for the given parameters: V$_{CC}$ = 12 V, I$_E$ = 1 mA, and β = 100. [[4]]", []),
     ("Determine input resistance, voltage gain and output resistance of given common emitter BJT Amplifier. β = 120 and r$_o$ = 40 kΩ. [[5]]", [('prob_ce', 'Question 2: common-emitter amplifier with fixed bias, V$_{CC}$ = +20 V, R$_B$ = 470 kΩ, R$_C$ = 2.2 kΩ, unbypassed R$_E$ = 0.56 kΩ.')]),
     ("Explain the operation principle of a BJT as a switch with the necessary diagrams. [[4]]", []),
     ("Describe the construction and working principle of n-channel depletion type MOSFET with the help of characteristics curve and mathematical expressions. [[7]]", []),
     ("For the given JFET voltage divider configuration, determine I$_{DQ}$, V$_{GSQ}$, V$_{DS}$ and transconductance g$_m$. [[6]]", [('prob_jfet1', 'Question 5: JFET voltage-divider bias, V$_{DD}$ = 20 V, R$_1$ = 910 kΩ, R$_2$ = 110 kΩ, R$_D$ = 2.2 kΩ, R$_S$ = 1.1 kΩ, I$_{DSS}$ = 10 mA, V$_P$ = −3.5 V.')]),
     ("Draw circuit diagram of LC Hartley oscillator. Derive its frequency of oscillation. [[4]]", []),
     ("Derive the expression of bandwidth of class A tuned amplifier. [[4]]", []),
     ("Show that the voltage gain of the differential amplifier with active load is twice with that with passive load. [[5]]", []),
     ("Derive general efficiency of series fed class A amplifier. [[4]]", []),
     ("For a class B amplifier using a supply of V$_{CC}$ = 30 V and driving a load of 16 Ω, determine the maximum input power, maximum output power and maximum power dissipation at transistors. [[5]]", []),
     ("Derive frequency of oscillation of 555 timer Astable Multivibrator [[4]]", []),
     ("Draw series voltage regulator with current limiting circuit and explain how this protection circuit works. Design a voltage regulator to give output voltage from 5 V to 15 V using LM317. [[4+4]]", []),
    ]
    s2 = r'''
**d.c. analysis** (fixed bias with unbypassed R$_E$, V$_{BE}$ = 0.7 V):

$$I_B=\frac{V_{CC}-V_{BE}}{R_B+(\beta+1)R_E}=\frac{20-0.7}{470\ \text{k}+121(0.56\ \text{k})}=\frac{19.3}{537.76\ \text{k}\Omega}=35.9\ \mu\text{A}$$

$$I_C=\beta I_B=4.307\ \text{mA},\qquad I_E=(\beta+1)I_B=4.343\ \text{mA},\qquad r_e=\frac{26\ \text{mV}}{I_E}=5.99\ \Omega$$

$$V_{CE}=V_{CC}-I_CR_C-I_ER_E=20-9.476-2.432=8.09\ \text{V}\ \ (\text{active region})$$

**a.c. analysis.** The emitter is not bypassed, so R$_E$ appears in the small-signal model. Since r$_o$ = 40 kΩ ≥ 10(R$_C$ + R$_E$) = 27.6 kΩ, r$_o$ may be neglected in the approximate formulas (the exact values with r$_o$ are also given).

<<fig:ce_ss>>

$$\begin{gathered}
Z_b=\beta(r_e+R_E)=120(5.99+560)=67.9\ \text{k}\Omega \\
\textbf{Input resistance:}\quad Z_i=R_B\parallel Z_b=\frac{470\times67.9}{470+67.9}=\mathbf{59.3\ k\Omega}\ \ (\text{exact with }r_o:\ 56.0\ \text{k}\Omega) \\
\textbf{Voltage gain:}\quad A_v=-\frac{\beta R_C}{Z_b}=-\frac{R_C}{r_e+R_E}=-\frac{2200}{565.99}=\mathbf{-3.89}\ \ (\text{exact:}\ -3.85) \\
\textbf{Output resistance:}\quad Z_o=R_C\parallel r_o=2.2\parallel40=\mathbf{2.09\ k\Omega}\ \ (\approx R_C=2.2\ \text{k}\Omega\ \text{if }r_o\text{ is neglected})
\end{gathered}$$

The negative sign shows the 180° phase shift; the gain is low because of the large unbypassed R$_E$ (a bypass capacitor across R$_E$ would raise it to −R$_C$/r$_e$ = −367).
'''
    s5 = "The JFET is biased by a voltage divider with source resistor.\n\n<<fig:prob_jfet1>>\n" + jf + "\n**Answers:** I$_{DQ}$ = %.2f mA, V$_{GSQ}$ = %.3f V, V$_{DS}$ = %.2f V, g$_m$ = %.2f mS.\n" % (jv['ID'], jv['VGS'], jv['VDS'], jv['gm'])
    s10 = r'''
Given V$_{CC}$ = %g V and R$_L$ = 16 Ω. For the class B stage the largest swing is V$_p$ = V$_{CC}$, so

$$\begin{gathered}
I_{p(max)}=\frac{V_{CC}}{R_L}=\frac{%g}{16}=%.3f\ \text{A},\qquad I_{dc}=\frac{2I_p}{\pi}=%.3f\ \text{A}\\
\textbf{Maximum input power:}\quad P_{in(max)}=V_{CC}I_{dc}=\frac{2V_{CC}^2}{\pi R_L}=\frac{2(%g)^2}{\pi(16)}=\mathbf{%.2f\ W}\\
\textbf{Maximum output power:}\quad P_{o(max)}=\frac{V_{CC}^2}{2R_L}=\frac{%g^2}{2(16)}=\mathbf{%.3f\ W}\\
\eta_{max}=\frac{P_o}{P_{in}}=\frac{\pi}{4}=%.1f\ \text{percent}
\end{gathered}$$

**Maximum power dissipation in the transistors.** For any peak voltage V$_p$ the dissipation of the two transistors is P$_D$ = P$_{in}$ − P$_o$ = 2V$_{CC}$V$_p$/(πR$_L$) − V$_p^2$/(2R$_L$). Differentiating with respect to V$_p$ and equating to zero gives V$_p$ = 2V$_{CC}$/π = %.2f V (I$_p$ = %.3f A), at which

$$P_{D(max)}=\frac{2V_{CC}^2}{\pi^2R_L}=\frac{2(%g)^2}{\pi^2(16)}=\mathbf{%.2f\ W}\ \ \text{(both transistors)},\qquad \text{i.e. }%.2f\ \text{W per transistor}$$

*(At the full-swing point V$_p$ = V$_{CC}$ the dissipation is P$_{in}$ − P$_o$ = %.2f − %.2f = %.2f W, lower than P$_{D(max)}$.)* So each transistor must be rated for at least %.1f W.
''' % (Vcc, Vcc, Ip, 2 * Ip / math.pi, Vcc, Pin, Vcc, Po, math.pi / 4 * 100, vpd, Ipd, Vcc, Pd_max, Pd_max / 2, Pin, Po, Pin - Po, Pd_max / 2)
    sol = [
     design_div(12, 1, 100, 1.2, 6), s2, T['bjt_switch'], T['dmos'], s5,
     U['hartley'], V['tuned'], V['diffamp'], U['classA_series'], s10, V['f555'],
     V['series_prot'] + lm317(5, 15, 720, 2000, 18),
    ]
    emit('ioe-ex151-2082-baishakh', header('NEBians-IOE-Past-Paper-Electronic-Device-and-Circuits-EX151-2082-Baishakh.pdf', 'EX 151', '2082 Baishakh', 2025, 'Back paper (new course).'), q, sol)

# ================================================================ PAPER 4: EX 151 2081 Ashwin (2080 batch)
def paper4():
    jf, jv = solve_dep(20, 1500, 330, 2, 1, -5.5, 10, '')
    q = [
     ("Design β independent type dc biased common emitter amplifier. Given parameters V$_{CC}$ = 20 V, I$_C$ = 1.5 mA and β = 110. Use stiff biasing method. [[4]]", []),
     ("Why is a common collector BJT amplifier also known as an emitter follower? Draw the small signal model of common collector amplifier circuit and derive expressions for input resistance, voltage gain, and current gain. [[1+4]]", []),
     ("Derive trans-conductance of BJT. [[4]]", []),
     ("Describe the construction and working principle of n channel enhancement-type MOSFET with the help of necessary diagrams and its drain characteristic curve. [[7]]", []),
     ("Find I$_D$ and V$_{DS}$ for the following circuit. Given data are V$_P$ = −5.5 V, I$_{DSS}$ = 10 mA. Assume all the capacitors are ideal and check whether the transistor is operating in the Pinch off region or not. [[6]]", [('prob_jfet2', 'Question 5: JFET amplifier, V$_{DD}$ = 20 V, R$_1$ = 1.5 MΩ, R$_2$ = 330 kΩ, R$_D$ = 2 kΩ, R$_S$ = 1 kΩ (bypassed by C$_S$); C$_G$, C$_D$ coupling capacitors.')]),
     ("State Barkhausen criterion for sinusoidal oscillation. Draw the circuit diagram of Colpitts oscillator and write its frequency of oscillation. [[4]]", []),
     ("Derive frequency of oscillation of 555 timer Astable Multivibrator. [[4]]", []),
     ("Draw a Widlar Current Source. Derive an expression for an output resistance of Widlar Current Source. [[5]]", []),
     ("Calculate the efficiency of a transformer coupled Class A amplifier for a supply of 12 V DC and output of V$_P$ = 12 V and 6 V. [[4]]", []),
     ("Draw the circuit diagram and the characteristic curve of a transformer coupled class B push-pull amplifier and derive its general efficiency. [[5]]", []),
     ("Draw the circuit diagram of class A tuned amplifier with its frequency response. Derive its 3dB bandwidth. [[4]]", []),
     ("Design variable DC voltage regulator using LM 317 to get (10-20) volts output. [[4]]", []),
     ("Explain the working principle of a series transistor voltage regulator with improved performance and derive an expression for the voltage stability. [[2+2]]", []),
    ]
    s9 = r'''
For the transformer-coupled class A stage the Q-point is at V$_{CEQ}$ = V$_{CC}$ = 12 V and, because the d.c. resistance of the primary is zero, the collector voltage can swing from 0 to 2V$_{CC}$ = 24 V (peak value V$_p$ ≤ V$_{CC}$). With the a.c. load line of slope −1/R$_L'$ through Q (I$_{CQ}$ = V$_{CC}$/R$_L'$):

$$\begin{gathered}
P_{dc}=V_{CC}I_{CQ}=\frac{V_{CC}^2}{R_L'},\qquad P_{ac}=\frac{V_p^2}{2R_L'} \\
\eta=\frac{P_{ac}}{P_{dc}}=\frac{V_p^2/(2R_L')}{V_{CC}^2/R_L'}=\frac{1}{2}\left(\frac{V_p}{V_{CC}}\right)^2
\end{gathered}$$

| V$_p$ | η = ½(V$_p$/V$_{CC}$)² | Result |
|---|---|---|
| 12 V | ½(12/12)² = 0.5 | **50 percent** (the theoretical maximum) |
| 6 V | ½(6/12)² = 0.125 | **12.5 percent** |

(For a numerical check take R$_L'$ = 12 Ω: I$_{CQ}$ = 1 A, P$_{dc}$ = 12 W; V$_p$ = 12 V gives I$_p$ = 1 A and P$_{ac}$ = 6 W, η = 50 percent; V$_p$ = 6 V gives P$_{ac}$ = 1.5 W, η = 12.5 percent.) The efficiency falls as the square of the signal amplitude because P$_{dc}$ is constant, independent of the signal.
'''
    s8 = U['widlar']
    sol = [
     design_div(20, 1.5 * 111 / 110, 110, 2.0, 10.0),
     T['cc'], T['gm_bjt'], T['emos'],
     "The JFET is biased by a divider with a source resistor R$_S$ (bypassed by C$_S$ for a.c., so d.c. analysis uses R$_S$ = 1 kΩ).\n\n<<fig:prob_jfet2>>\n" + jf + "\n**Answers:** I$_D$ = %.3f mA, V$_{DS}$ = %.2f V, and since V$_{DS}$ > V$_{GS}$ − V$_P$ the transistor operates in the pinch-off (saturation) region.\n" % (jv['ID'], jv['VDS']),
     U['barkhausen'] + U['colpitts'], V['f555'], s8, s9, U['classB_tc'], V['tuned'],
     lm317(10, 20, 1680, 2000, 23), V['series_improved'],
    ]
    emit('ioe-ex151-2081-ashwin', header('NEBians-IOE-Past-Paper-Electronic-Device-and-Circuits-EX151-2081-Ashwin.pdf', 'EX 151', '2081 Ashwin', 2024, 'Regular (new course, 2080 batch).'), q, sol)

if __name__ == '__main__':
    paper1(); paper2(); paper3(); paper4()
