---
file: NEBians-IOE-Past-Paper-Power-System-Analysis-I-ENEE205-2081-Chaitra.pdf
subject: Power System Analysis I
level: BE · Year II / Part I
code: ENEE 205
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular examination (new course, 2080 batch), BE Electrical Engineering (BEL), Year II / Part I. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
(a) Draw a typical power system network and name its different components. [[6]]

(b) Calculate the string efficiency and individual voltage for 3-unit suspension insulator if the capacitance of each unit to earth and line be 25% and 10% of the self-capacitance of the unit respectively for a voltage level of 25 kV. [[3+3]]

@q 2
(a) Differentiate between stranded and bundled conductors. [[4]]

(b) A 90 MVA 11 kV 3-phase generator has a reactance of 15%. The generator supplies two motors through transformers and transmission line shown in figure below. The transformer T$_1$ is a 3-phase transformer, 100 MVA, 10/132 kV, 6% reactance. The transformer T$_2$ is composed of 3 single phase units each rated at 30 MVA, 66/10 kV with 5% reactance. The connection of T$_1$ and T$_2$ are as shown. The motors rated at 50 MVA and 40 MVA both 10 kV and 20% reactance. Taking the generator rating as base, draw reactance diagram and indicate the reactance in per unit. The reactance of line is 100 Ω. [[8]]

Single-line diagram: generator G (Y, grounded) – T$_1$ (Δ–Y, grounded Y on the line side) – line – T$_2$ (Y grounded on the line side, Δ on the motor side) – bus feeding motor M$_1$ (Y, grounded) and motor M$_2$ (Δ).

@q 3
(a) What is transposition in three phase transmission line? Why it is required for these lines? [[3+3]]

(b) A 3 phase 132 kV, 50 Hz line has ASCR conductors of equivalent copper area 1.5 cm$^2$ and effective diameter 39.8 mm, spaced equilaterally 8 m apart (i) find line parameters (ii) find charging current and charging MVA. Resistivity of copper is $1.73\times10^{-6}$ Ω-cm. [[3+3]]

@q 4
(a) Draw the phasor diagram for a nominal 'Tee' circuit of a transmission line for lagging condition and find it's A, B, C, D parameters. [[4]]

(b) A 280 km long transmission line on a 60 Hz system has line impedance of (33+j104) and a total shunt admittance of $10^{-3}$ mho. The receiving end feeds a load of 80 MW at 220 kV at 0.8 p.f. lagging. Find sending-end voltage, current, power and power factor using (i) & (ii) and comment on results. [[4+4]]

(i) Nominal pi method

(ii) Long lines

@q 5
(a) Briefly explain Ferranti effect and Skin effect. [[4]]

(b) Why is reactive power compensation required in transmission line? Explain the methods used for reactive power compensation. [[4+4]]

<!-- SOLUTIONS -->

@s 1
**(a) A typical power system network.** A power system has four stages: generation, transmission, sub-transmission and distribution, linked by transformers and switching stations.

```figure caption="Question 1(a): single-line block diagram of a typical power system network (voltage levels typical of Nepal)."
fig,ax=flow([("Generating station","hydro / thermal, 11 kV"),("Step-up substation","11 / 132 or 220 kV"),("Transmission line","132 / 220 / 400 kV"),("Grid substation","132 / 33 kV"),("Primary distribution","33 / 11 kV feeders"),("Distribution Tx, consumer","11 kV / 400 V")],figsize=(6.6,2.0))
```

| Component | Function |
|---|---|
| Generating station (alternators, prime movers) | Converts primary energy into electrical energy at 6.6 to 25 kV |
| Step-up transformer | Raises the voltage for economical bulk transmission (less $I^2R$ loss) |
| Transmission lines (overhead / cable), towers, insulators | Carry bulk power over long distances at EHV |
| Receiving / grid substation | Step-down transformers, bus-bars, switchyard |
| Sub-transmission network | Moves power to the load centres at 33 / 66 kV |
| Distribution substation, feeders, distributors | Step down to 11 kV and 400/230 V and deliver to consumers |
| Circuit breakers, isolators, relays, CTs, PTs | Switching, protection and measurement |
| Reactive-power and control equipment | Capacitor banks, reactors, SVCs, tap changers, load-dispatch (SCADA) |
| Consumers | Domestic, commercial, industrial and agricultural loads |

**(b) String efficiency of the 3-unit string.** Let $C$ be the self-capacitance of a unit. Shunt capacitance of each joint to earth $= mC$ with $m = 0.25$; capacitance of each joint to the line $= nC$ with $n = 0.10$. Number the units from the earth end: $V_1$ (unit next to the cross-arm), $V_2$, $V_3$ (next to the line); $V = V_1 + V_2 + V_3 = 25$ kV is taken as the voltage across the string.

*Joint A* (between units 1 and 2, potential $V_1$ above earth). Currents into the joint: through unit 2 ($\omega CV_2$) and from the line through the line capacitance ($n\omega C(V_2 + V_3)$). Currents out: through unit 1 ($\omega CV_1$) and to earth through $m\omega C V_1$:

$$\begin{gathered}V_2 + n(V_2 + V_3) = V_1(1 + m) \\ \Rightarrow \\ 1.25\,V_1 = 1.1\,V_2 + 0.1\,V_3\end{gathered}$$

*Joint B* (between units 2 and 3, potential $V_1 + V_2$). In: through unit 3 ($V_3$) and from the line through $nC$ ($nV_3$). Out: through unit 2 ($V_2$) and to earth ($m(V_1 + V_2)$):

$$\begin{gathered}V_3(1 + n) = V_2 + m(V_1 + V_2) \\ \Rightarrow \\ 1.1\,V_3 = 0.25\,V_1 + 1.25\,V_2\end{gathered}$$

Solving with $V_1 + V_2 + V_3 = 25$ (Cramer's rule / substitution, checked in Python):

$$\begin{gathered}V_1 = 7.380\ \text{kV} \\ V_2 = 7.463\ \text{kV} \\ V_3 = 10.158\ \text{kV}\end{gathered}$$

$$\text{String efficiency} = \frac{V}{3\,V_3} = \frac{25}{3 \times 10.158} = 0.8204 = \mathbf{82.0\,\%}$$

(If 25 kV is the line voltage of the system, the voltages across the units per phase are $1/\sqrt3$ times those above: 4.26, 4.31 and 5.86 kV; the efficiency does not change.) The line capacitance helps equalise the distribution: with $n = 0$ the efficiency would be only 74.7 %.

```figure caption="Question 1(b): voltage across the three units of the string (total 25 kV); the unit next to the line carries the most."
fig,ax=plt.subplots(figsize=(5.0,2.3))
v=[7.380,7.463,10.158]
b=ax.bar(["Unit 1\n(earth end)","Unit 2","Unit 3\n(line end)"],v,color=[SERIES[0],SERIES[0],SERIES[1]],width=0.5)
ax.axhline(25/3,color=MUTED,ls="--",lw=1); ax.text(2.4,25/3-0.9,"ideal 8.33 kV",ha="right",fontsize=8,color=MUTED)
for r,x in zip(b,v): ax.text(r.get_x()+r.get_width()/2,x+0.2,f"{x:.2f} kV",ha="center",fontsize=8)
ax.set_ylim(0,12.5); ax.set_ylabel("voltage (kV)",fontsize=8.5); ax.tick_params(labelsize=8)
for s in ("top","right"): ax.spines[s].set_visible(False)
```

@s 2
**(a) Stranded and bundled conductors.**

| Point | Stranded conductor | Bundled conductor |
|---|---|---|
| Construction | One conductor made of several twisted strands (7, 19, 37, ...) | Two or more separate sub-conductors per phase, held apart by spacers (30 to 45 cm) |
| Purpose | Flexibility, easy handling, more area than a solid wire, fewer breakage problems | Used on EHV lines (above 220 kV) to cut corona and reactance |
| Inductance | Larger | Smaller (larger equivalent GMR) |
| Capacitance | Smaller | Larger (larger equivalent radius) |
| Corona loss, radio noise | Higher | Lower (reduced surface gradient) |
| Surge impedance, power capacity | Higher $Z_c$, lower SIL | Lower $Z_c$, higher SIL and transfer capability |
| Cost, wind and ice loading | Lower | Higher (more conductor, hardware) |

**(b) Reactance diagram.** Base: generator rating, $S_{base} = 90$ MVA, $V_{base} = 11$ kV in the generator zone.

*Base voltages of the zones.*

$$V_{base,line} = 11 \times \frac{132}{10} = 145.2\ \text{kV}$$

T2 is a bank of three single-phase 66/10 kV units connected Y–Δ, so its line-to-line ratio is $66\sqrt3 : 10 = 114.3 : 10$ kV, and its 3-phase rating is $3 \times 30 = 90$ MVA:

$$V_{base,motor} = 145.2 \times \frac{10}{114.3} = 12.70\ \text{kV}$$

*Per-unit reactances.*

| Element | Calculation | p.u. |
|---|---|---|
| Generator | given on its own base | **0.1500** |
| T1 | $0.06 \times \dfrac{90}{100}\left(\dfrac{10}{11}\right)^2$ (the same with $132/145.2$) | **0.0446** |
| Line | $Z_{base} = \dfrac{145.2^2}{90} = 234.26\ \Omega$, so $\dfrac{100}{234.26}$ | **0.4269** |
| T2 | $0.05 \times \dfrac{90}{90}\left(\dfrac{114.3}{145.2}\right)^2$ | **0.0310** |
| Motor M1 | $0.20 \times \dfrac{90}{50}\left(\dfrac{10}{12.70}\right)^2$ | **0.2231** |
| Motor M2 | $0.20 \times \dfrac{90}{40}\left(\dfrac{10}{12.70}\right)^2$ | **0.2789** |

The reactance diagram (magnetising currents and resistances neglected; the Y–Δ phase shift is not shown in a per-unit reactance diagram) is shown below.

```figure caption="Question 2(b): per-unit reactance diagram on 90 MVA (11 kV in the generator zone, 145.2 kV in the line zone, 12.70 kV in the motor zone). E_G, E_M1, E_M2 are the internal emfs."
fig,ax=ckt_canvas(6.6,3.0)
wire(ax,[(0.2,0),(12.8,0)])
vsrc(ax,(0.8,0),(0.8,1.5),"E$_G$",side=-1,off=0.85); wire(ax,[(0.8,1.5),(0.8,2.6)])
ind(ax,(0.8,2.6),(2.6,2.6),"j0.15",side=1,body=1.1); ind(ax,(2.6,2.6),(4.4,2.6),"j0.0446",side=1,body=1.1)
ind(ax,(4.4,2.6),(6.5,2.6),"j0.4269",side=1,body=1.1); ind(ax,(6.5,2.6),(8.3,2.6),"j0.031",side=1,body=1.1)
wire(ax,[(8.3,2.6),(12.0,2.6)])
for x,e,v in ((9.6,"M1","j0.2231"),(11.6,"M2","j0.2789")):
    node(ax,(x,2.6)); ind(ax,(x,2.6),(x,1.4),v,side=1,body=0.9); vsrc(ax,(x,1.4),(x,0),"E$_{%s}$"%e,side=-1,off=0.85)
```

@s 3
**(a) Transposition.** In a three-phase line the conductors are not at the corners of an equilateral triangle (they are in a flat or vertical arrangement), so the three phases have different inductance and capacitance and the voltage drops are unequal, with induced voltages in telephone lines. *Transposition* means interchanging the positions of the three conductors at regular intervals along the line so that each conductor occupies each of the three positions for one third of the length (a complete cycle uses two transposition towers).

*Why it is required:*

1. It makes the average inductance and capacitance of the three phases equal, so the line is balanced and the phase voltages and currents stay symmetrical.
2. It removes the unbalanced voltage drop and the unequal charging currents (reduced neutral displacement).
3. It reduces electromagnetic and electrostatic interference with nearby communication lines.

With transposition, the formulas $L = 2\times10^{-7}\ln(D_{eq}/D_s)$ and $C = 2\pi\varepsilon_0/\ln(D_{eq}/r)$ with $D_{eq} = \sqrt[3]{d_{12}d_{23}d_{31}}$ are exact for the average.

```figure caption="Question 3(a): a complete transposition cycle; conductors a, b, c exchange positions after each third of the line length."
fig,axs=plt.subplots(1,3,figsize=(6.2,1.6))
orders=[("a","b","c"),("c","a","b"),("b","c","a")]
for ax,o,t in zip(axs,orders,("section 1","section 2","section 3")):
    for i,l in enumerate(o):
        ax.add_patch(Circle((i,0),0.2,fc="white",ec=SERIES[i if l=="a" else (1 if l=="b" else 2)] if False else {"a":SERIES[0],"b":SERIES[1],"c":SERIES[2]}[l],lw=2)); ax.text(i,0,l,ha="center",va="center",fontsize=11)
    ax.text(1,-0.7,t,ha="center",fontsize=8.5); ax.set_xlim(-0.6,2.6); ax.set_ylim(-1,0.6); ax.set_aspect("equal"); ax.axis("off")
```

**(b) ASCR line parameters.** Spacing $D = 8$ m (equilateral, so $D_{eq} = 8$ m), effective diameter 39.8 mm, so $r = 19.9$ mm.

**(i) Resistance:** equivalent copper area 1.5 cm$^2$, $\rho = 1.73\times10^{-6}\ \Omega\,$cm:

$$R = \frac{\rho\,l}{A} = \frac{1.73\times10^{-6} \times 1\ \text{km}(=10^5\ \text{cm})}{1.5} = \mathbf{0.1153\ \Omega/km}\ \text{per phase (dc, skin effect neglected)}$$

**Inductance:** the self GMR of the (solid-equivalent) conductor is

$$D_s = 0.7788 \times 0.0199 = 0.01550\ \text{m}$$

so

$$L = 2\times10^{-7}\ln\frac{8}{0.01550} = 2\times10^{-7}\times 6.2465 = 1.249\times10^{-6}\ \text{H/m} = \mathbf{1.249\ mH/km}$$

$$X_L = 2\pi(50)(1.249\times10^{-3}) = \mathbf{0.392\ \Omega/km}$$

**Capacitance:**

$$C = \frac{2\pi\varepsilon_0}{\ln(D/r)} = \frac{2\pi(8.854\times10^{-12})}{\ln(8/0.0199)} = \frac{5.563\times10^{-11}}{5.9965} = 9.28\times10^{-12}\ \text{F/m} = \mathbf{0.00928\ \mu F/km}$$

$$\begin{gathered}X_C = \frac{1}{\omega C} = 0.343\ \text{M}\Omega\cdot\text{km} \\ B = \omega C = 2.915\ \mu\text{S/km}\end{gathered}$$

**(ii) Charging current and charging MVA** (per km of line, per phase voltage $132/\sqrt3 = 76.21$ kV):

$$I_c = \omega C\,V_{ph} = (2.915\times10^{-6})(76.21\times10^3) = \mathbf{0.222\ A/km}$$

$$\text{Charging MVA} = \sqrt3\,V_L I_c = \sqrt3(132)(0.222)\times10^{-3} = \mathbf{0.0508\ MVAr/km}$$

(for a 100 km line: 22.2 A and 5.08 MVAr; the length is not given, so values are per km).

@s 4
**(a) Nominal T circuit.** The total series impedance $Z$ is split into two halves, $Z/2$ on each side of the shunt admittance $Y$ placed at the middle point M.

$$\begin{gathered}V_M = V_R + I_R\frac{Z}{2} \\ I_C = YV_M \\ I_S = I_R + I_C \\ V_S = V_M + I_S\frac{Z}{2}\end{gathered}$$

Substituting:

$$I_S = I_R + Y\left(V_R + \frac{Z}{2}I_R\right) = YV_R + \left(1 + \frac{YZ}{2}\right)I_R$$

$$V_S = V_R + \frac{Z}{2}I_R + \frac{Z}{2}\left[YV_R + \left(1 + \frac{YZ}{2}\right)I_R\right] = \left(1 + \frac{YZ}{2}\right)V_R + Z\left(1 + \frac{YZ}{4}\right)I_R$$

$$\boxed{A = D = 1 + \frac{YZ}{2},\qquad B = Z\left(1 + \frac{YZ}{4}\right),\qquad C = Y}$$

*Phasor diagram (lagging load).* $V_R$ is the reference; $I_R$ lags it. Add $I_R Z/2$ to get $V_M$; $I_C = YV_M$ leads $V_M$ by $90^\circ$; $I_S = I_R + I_C$; add $I_SZ/2$ to $V_M$ to get $V_S$.

```figure caption="Question 4(a): phasor diagram of the nominal T circuit for a lagging load (drawn to an illustrative scale): V_R, I_R; V_M = V_R + I_R Z/2; I_C leads V_M by 90 deg; I_S = I_R + I_C; V_S = V_M + I_S Z/2."
fig,ax=plt.subplots(figsize=(5.8,3.4))
VR=3.0+0j; IR=1.5*np.exp(-1j*np.radians(37)); Z2=0.35+0.85j; Y=0.22j
VM=VR+IR*Z2; IC=Y*VM; IS=IR+IC; VS=VM+IS*Z2
def arr(a,b,c,lw=1.8): ax.annotate("",xy=(b.real,b.imag),xytext=(a.real,a.imag),arrowprops=dict(arrowstyle="-|>",color=c,lw=lw))
arr(0,VR,INK); arr(0,IR*1.0,ACCENT); arr(VR,VM,SERIES[2]); arr(0,VM,SERIES[3]); arr(0,IC*2.2,SERIES[4]); arr(0,IS*1.0,SERIES[5]); arr(VM,VS,SERIES[2]); arr(0,VS,SERIES[1])
t=lambda p,s,c,dx=0.06,dy=0.06: ax.text(p.real+dx,p.imag+dy,s,fontsize=9,color=c)
t(VR,"V$_R$",INK,-0.1,-0.35); t(IR,"I$_R$",ACCENT,0.05,-0.3); t(VM,"V$_M$",SERIES[3]); t(IC*2.2,"I$_C$",SERIES[4]); t(IS,"I$_S$",SERIES[5],0.05,0.05); t(VS,"V$_S$",SERIES[1])
ax.text(VR.real+0.35,VR.imag+0.35,"I$_R$Z/2",fontsize=7.5,color=SERIES[2]); ax.text((VM.real+VS.real)/2-0.2,(VM.imag+VS.imag)/2+0.25,"I$_S$Z/2",fontsize=7.5,color=SERIES[2])
ax.set_xlim(-0.3,5.2); ax.set_ylim(-1.2,2.8); ax.set_aspect("equal"); ax.axis("off")
```

**(b) Sending-end quantities of the 280 km, 60 Hz line.** Total $Z = 33 + j104 = 109.11\angle72.40^\circ\ \Omega$ and $Y = j10^{-3}$ S (the shunt admittance is taken as purely capacitive). Receiving end, per phase:

$$\begin{gathered}V_R = \frac{220\times10^3}{\sqrt3} = 127.02\ \text{kV} \\ I_R = \frac{80\times10^6}{\sqrt3\,(220\times10^3)(0.8)} = 262.4\ \text{A}\ \ \Rightarrow\ \ I_R = 262.4\angle-36.87^\circ\ \text{A}\end{gathered}$$

**(i) Nominal $\pi$ method.**

$$\frac{YZ}{2} = \frac{(10^{-3}\angle90^\circ)(109.11\angle72.40^\circ)}{2} = 0.05456\angle162.40^\circ = -0.05186 + j0.01653$$

$$A = D = 1 + \frac{YZ}{2} = 0.9481 + j0.0165 = 0.9481\angle0.997^\circ$$

$$\begin{gathered}B = Z = 109.11\angle72.40^\circ\ \Omega \\ C = Y\left(1 + \frac{YZ}{4}\right) = 0.974\times10^{-3}\angle90.49^\circ\ \text{S}\end{gathered}$$

$$V_S = AV_R + BI_R = 120.43\angle0.997^\circ + 28.63\angle35.53^\circ\ \text{kV} = 143.71 + j18.73 = 144.93\angle7.43^\circ\ \text{kV}$$

$$\boxed{V_{S(line)} = \sqrt3 \times 144.93 = 251.0\ \text{kV}}$$

$$I_S = CV_R + DI_R = 123.7\angle90.49^\circ + 248.8\angle-35.87^\circ = 201.8\angle-6.29^\circ\ \text{A}$$

The angle between $V_S$ and $I_S$ is $7.43^\circ + 6.29^\circ = 13.71^\circ$:

$$\text{p.f.}_S = \cos13.71^\circ = \mathbf{0.9715\ lagging}$$

$$\begin{gathered}P_S = 3(144.93\times10^3)(201.8)(0.9715) = \mathbf{85.24\ MW} \\ Q_S = \mathbf{20.80\ MVAr}\end{gathered}$$

Regulation $= (144.93/0.9481 - 127.02)/127.02 = 20.3\,\%$; efficiency $= 80/85.24 = 93.9\,\%$.

**(ii) Long-line (rigorous, hyperbolic) method.**

$$\begin{gathered}Z_c = \sqrt{\frac{Z}{Y}} = \sqrt{\frac{109.11\angle72.40^\circ}{10^{-3}\angle90^\circ}} = 330.3\angle-8.80^\circ\ \Omega \\ \gamma l = \sqrt{ZY} = 0.3303\angle81.20^\circ = 0.0505 + j0.3264\end{gathered}$$

$$\cosh\gamma l = \cosh(0.0505)\cos(0.3264) + j\sinh(0.0505)\sin(0.3264) = 0.9484 + j0.0162$$

$$\sinh\gamma l = \sinh(0.0505)\cos(0.3264) + j\cosh(0.0505)\sin(0.3264) = 0.0479 + j0.3211 = 0.3246\angle81.5^\circ$$

$$\begin{gathered}A = D = \cosh\gamma l = 0.9485\angle0.98^\circ \\ B = Z_c\sinh\gamma l = 107.23\angle72.71^\circ\ \Omega \\ C = \frac{\sinh\gamma l}{Z_c} = 0.983\times10^{-3}\angle90.32^\circ\ \text{S}\end{gathered}$$

(check: $A^2 - BC = 1.000$). Then

$$V_S = AV_R + BI_R = 120.48\angle0.98^\circ + 28.14\angle35.84^\circ\ \text{kV} = 143.27 + j18.54 = 144.47\angle7.37^\circ\ \text{kV}$$

$$\boxed{V_{S(line)} = \sqrt3 \times 144.47 = 250.2\ \text{kV}}$$

$$\begin{gathered}I_S = CV_R + DI_R = 202.1\angle-6.00^\circ\ \text{A} \\ \text{p.f.}_S = \cos(7.37^\circ + 6.00^\circ) = \mathbf{0.9729\ lagging}\end{gathered}$$

$$\begin{gathered}P_S = \mathbf{85.21\ MW} \\ Q_S = \mathbf{20.25\ MVAr}\end{gathered}$$

Regulation $= 19.9\,\%$; efficiency $= 80/85.21 = 93.9\,\%$.

**Comparison and comment.**

| Quantity | Nominal $\pi$ | Long line (exact) | Difference |
|---|---|---|---|
| $V_S$ (line) | 251.0 kV | 250.2 kV | 0.3 % |
| $I_S$ | 201.8 A | 202.1 A | 0.1 % |
| $P_S$ | 85.24 MW | 85.21 MW | 0.04 % |
| $Q_S$ | 20.80 MVAr | 20.25 MVAr | 2.7 % |
| p.f. at sending end | 0.9715 | 0.9729 | 0.1 % |

The nominal-$\pi$ result is within about 0.3 % of the exact value for voltage and current, because 280 km is only just above the 250 km limit of the medium-line model. Its only noticeable error is in reactive power (about 3 %), since the lumped capacitance is an approximation of the distributed one. The nominal $\pi$ is therefore adequate here, but for longer lines (above about 300 km) the error grows and the rigorous method must be used.

@s 5
**(a) Ferranti effect and skin effect.**

*Ferranti effect.* On a lightly loaded or open-circuited long line, the receiving-end voltage is **higher** than the sending-end voltage. The line capacitance draws a leading charging current $I_C$ that flows through the series inductance; the voltage drop $jI_CX_L$ is in phase *with* (adds to) the receiving-end voltage rather than opposing it. At no load, $V_R = V_S/A = V_S/\cos\beta l$ for a lossless line, which rises with $l$ and with frequency (for a short line $V_R \approx V_S/(1 - \omega^2LCl^2/2)$). Example: for the 280 km line of Question 4, $1/|A| = 1/0.9485 = 1.054$, a rise of 5.4 %. It is controlled by shunt reactors, which absorb the charging reactive power, and by the lower operating voltage at light load.

*Skin effect.* With alternating current, the current density is largest at the surface of a conductor and smallest at the centre: the central flux linkage makes the inner filaments more inductive, so the current crowds outward. The effective cross-section decreases, so $R_{ac} > R_{dc}$. It grows with the conductor diameter, the frequency, the permeability and the conductivity (skin depth $\delta = \sqrt{2/\omega\mu\sigma}$, about 9.3 mm in copper at 50 Hz and 8.5 mm at 60 Hz). Remedies: stranded or hollow conductors, ACSR (the steel core carries no current), bundled conductors.

**(b) Reactive power compensation.**

*Why it is required.*

1. **Voltage regulation:** $\Delta V \approx (RP + XQ)/V$; reactive flow causes voltage drop in heavy load and rise (Ferranti) in light load, so the voltage must be kept within about $\pm5\,\%$.
2. **Loss reduction:** the reactive current component adds to $I^2R$ loss; supplying $Q$ locally removes it.
3. **Increased capacity:** the line and transformers carry $S = \sqrt{P^2 + Q^2}$; lowering $Q$ frees capacity for real power.
4. **Stability:** the steady-state stability limit $P_{max} = V_SV_R/X$ rises with better voltage support and with lower effective reactance (series compensation); transient stability and voltage stability improve.
5. Power-factor improvement for utility and consumers (lower tariff penalty, better use of generators).
6. Removes over-voltages at light load and under-voltages at peak.

*Methods.*

```figure caption="Question 5(b): compensation devices on a transmission line: series capacitor (in the line), shunt capacitor (heavy load), shunt reactor (light load / long line); SVC and STATCOM provide both."
fig,ax=ckt_canvas(6.4,3.0)
wire(ax,[(0,2.6),(1.0,2.6)]); ind(ax,(1.0,2.6),(2.6,2.6),"line",side=1,body=1.0); cap(ax,(2.6,2.6),(3.8,2.6),"series C",side=1)
ind(ax,(3.8,2.6),(5.4,2.6),"line",side=1,body=1.0); wire(ax,[(5.4,2.6),(10.4,2.6)])
for x,k,t in ((6.2,"c","shunt C"),(8.0,"l","shunt reactor"),(9.8,"s","SVC")):
    node(ax,(x,2.6))
    if k=="c": cap(ax,(x,2.6),(x,1.0),t,side=1,off=0.75)
    elif k=="l": ind(ax,(x,2.6),(x,1.0),t,side=1,body=1.0,off=0.9)
    else:
        ind(ax,(x,2.6),(x,1.7),"",side=1,body=0.5); cap(ax,(x,1.7),(x,1.0),t,side=1,off=0.7)
    gnd(ax,(x,1.0))
```

| Device | Principle | Used for |
|---|---|---|
| **Shunt capacitor bank** | Supplies leading vars at the load end ($Q_C = V^2\omega C$) | Raises voltage and p.f. in heavy load; switched in steps |
| **Shunt reactor** | Absorbs lagging vars ($Q_L = V^2/\omega L$) | Cancels line charging and Ferranti rise on long / lightly loaded EHV lines |
| **Series capacitor** | Cancels part of the line reactance ($X_{net} = X_L - X_C$, typically 25 to 70 %) | Lowers voltage drop, raises power transfer and stability limit; risk of sub-synchronous resonance |
| **Synchronous condenser** | Over-excited synchronous motor running without load: generates vars; under-excited absorbs | Continuous, smooth control and short-circuit support; costly, with losses and maintenance |
| **Static VAr compensator (SVC)** | Thyristor-controlled reactor with fixed or switched capacitors (TCR-FC, TSC-TCR) | Fast, stepless var control, voltage support, damping of oscillations |
| **STATCOM** | Voltage-source converter injecting controllable reactive current | Faster than SVC, works at low voltage, smaller footprint |
| **Tap-changing / regulating transformers** | Change the turns ratio | Voltage adjustment (does not generate vars, only redistributes them) |
| **Phase advancers** | Supply the excitation current to induction motors | Local p.f. correction of large motors |

Shunt compensation is applied at the load end or along the line; series compensation reduces the line reactance. Modern grids use FACTS devices (SVC, STATCOM, TCSC) because they react in a few cycles.
