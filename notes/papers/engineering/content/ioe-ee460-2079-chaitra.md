---
file: NEBians-IOE-Past-Paper-Electric-Circuits-and-Machines-EE460-2079-Chaitra.pdf
subject: Electric Circuits and Machines
level: BE · Year I / Part II
code: EE 460
year_bs: 2079 Chaitra
cal: BS
year_ad: 2023
stream: BEI
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular. Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · All questions carry equal marks · Assume suitable data if necessary</small>

@q 1
(a) Explain the phenomenon of resonance of a parallel ac circuit in term of phasor diagram and also derive the expression for the resonance frequency. [[8]]
(b) Obtain the value of i$_1$, i$_2$, di$_1$/dt, di$_2$/dt, d²i$_1$/dt², d²i$_2$/dt² at t = 0⁺ if the switch is closed at t = 0 in the circuit shown in figure. [[8]]

```figure caption="Circuit of Question 1(b): 12 V, switch (t = 0), 1 H, 10 Ω shared, 10 Ω, 1 F; mesh currents i1 and i2."
fig,ax=ckt_canvas(5.6,3.0,xlim=(-1.6,8.6),ylim=(-0.5,4.0))
batt(ax,(0,0.7),(0,2.0),"12 V",side=-1); wire(ax,[(0,2.0),(0,3)]); wire(ax,[(0,0.7),(0,0)])
switch(ax,(0,3),(2.0,3),"t = 0",side=1); ind(ax,(2.0,3),(4.4,3),"1 H",side=-1)
node(ax,(4.4,3)); res(ax,(4.4,3),(4.4,0),"10 Ω",side=-1)
res(ax,(4.4,3),(7,3),"10 Ω",side=1); cap(ax,(7,3),(7,0),"1 F",side=1)
wire(ax,[(0,0),(7,0)]); node(ax,(4.4,0)); mesh(ax,(2.2,1.5),0.6,"i$_1$"); mesh(ax,(5.7,1.5),0.6,"i$_2$")
```

@q 2
(a) Find the expression of current and voltage across inductor for t > 0 using direct solution method. [[8]]

```figure caption="Circuit of Question 2(a): 60 V, switch (t = 0), 2 Ω, then the 10 Ω + 1 H branch in parallel with 1/9 F."
fig,ax=ckt_canvas(5.4,3.0,xlim=(-1.6,9.4),ylim=(-0.5,4.0))
vsrc(ax,(0,0),(0,3),"60 V",side=-1); switch(ax,(0,3),(2.2,3),"t = 0",side=1)
res(ax,(2.2,3),(5,3),"2 Ω",side=1); node(ax,(5,3)); wire(ax,[(5,3),(8,3)])
res(ax,(5,3),(5,1.6),"10 Ω",side=-1,body=0.9); ind(ax,(5,1.6),(5,0),"1 H",side=-1,body=1.0)
cap(ax,(8,3),(8,0),"1/9 F",side=1); wire(ax,[(0,0),(8,0)]); node(ax,(5,0))
```

(b) In the network shown below a steady state is reached with the switch k open with V = 90 V, R$_1$ = 10 Ω, R$_2$ = 20 Ω, R$_3$ = 20 Ω, L = 1 H and C = 1 μF at time t = 0, the switch is closed. Evaluate the current i$_1$ and i$_2$ using Laplace transform method for t > 0. [[8]]

```figure caption="Circuit of Question 2(b): switch K across R1, R2 + L (i1) and R3 + C (i2) in parallel."
fig,ax=ckt_canvas(5.6,3.1,xlim=(-1.6,9.4),ylim=(-0.5,5.0))
batt(ax,(0,0.7),(0,2.0),"V",side=-1); wire(ax,[(0,2.0),(0,3),(1.2,3)]); wire(ax,[(0,0.7),(0,0)])
res(ax,(1.2,3),(3.6,3),"R$_1$",side=-1)
wire(ax,[(1.2,3),(1.2,4.2)]); switch(ax,(1.2,4.2),(3.6,4.2),"K",side=1); wire(ax,[(3.6,4.2),(3.6,3)])
node(ax,(1.2,3)); node(ax,(3.6,3)); wire(ax,[(3.6,3),(8,3)]); node(ax,(5,3))
res(ax,(5,3),(5,1.6),"R$_2$",side=1,body=0.9); ind(ax,(5,1.6),(5,0),"L",side=1,body=1.0)
res(ax,(8,3),(8,1.6),"R$_3$",side=1,body=0.9); cap(ax,(8,1.6),(8,0),"C",side=1)
wire(ax,[(0,0),(8,0)]); arrow(ax,(4.5,2.6),(4.5,1.8),"i$_1$",off=-0.3); arrow(ax,(7.5,2.6),(7.5,1.8),"i$_2$",off=-0.3); arrow(ax,(3.9,3.4),(4.7,3.4),"i",off=0.2)
```

@q 3
(a) Obtain the open circuit parameter of the network shown below. Convert the obtained parameter into h-Parameter. [[8]]

```figure caption="Network of Question 3(a): 3 Ω and 6 Ω series arms, 15 Ω shunt arm and a 9 Ω bridge between the two top terminals."
fig,ax=ckt_canvas(5.4,3.0,xlim=(-0.9,8.9),ylim=(-0.8,4.2))
terminal(ax,(0,2)); terminal(ax,(8,2)); terminal(ax,(0,0)); terminal(ax,(8,0))
wire(ax,[(0,2),(1,2)]); res(ax,(1,2),(3.5,2),"3 Ω",side=-1); res(ax,(3.5,2),(6,2),"6 Ω",side=-1); wire(ax,[(6,2),(8,2)])
wire(ax,[(1,2),(1,3.4)]); res(ax,(1,3.4),(6,3.4),"9 Ω",side=1); wire(ax,[(6,3.4),(6,2)])
node(ax,(1,2)); node(ax,(6,2)); node(ax,(3.5,2)); res(ax,(3.5,2),(3.5,0),"15 Ω",side=1)
wire(ax,[(0,0),(8,0)]); node(ax,(3.5,0)); label(ax,(-0.5,1.0),"1",size=9); label(ax,(8.5,1.0),"2",size=9)
```

(b) A wrought iron bar 40 cm long and 2 cm in diameter is bent into a circular shape. It is then wound with 500 turns of wire. Calculate the current required to produce a flux of 0.5 mWb in magnetic circuit with an air gap of 1 mm; μ$_r$(iron) = 4000. [[8]]

@q 4
(a) Describe different types of losses on the transformer and how the efficiency is calculated? Derive the condition at which the efficiency of transformer will be maximum. [[8]]
(b) A dc shunt generator has an output of 10 kW at 500 V; the speed being 1000 rpm. The armature circuit resistance is 0.5 ohm and the field resistance is 250 ohm. Calculate the generated voltage at this case and also calculate speed when running as a shunt motor taking 50 kW at 500 V. [[8]]

@q 5
(a) How the speed of dc motor can be adjusted according to our desire? Explain the method for both shunt and series motor. [[8]]
(b) Write short notes on: [[4+4]]
(i) Double field revolving theory
(ii) Stepper motor
<!-- SOLUTIONS -->

@s 1
**(a) Parallel resonance in terms of the phasor diagram.**

Consider a practical coil ($R$ in series with $L$) in parallel with a capacitor $C$ across a supply $V$ of variable frequency (the ideal $L \parallel C$ is the case $R = 0$). The coil current $I_L = \dfrac{V}{\sqrt{R^{2} + \omega^{2}L^{2}}}$ lags $V$ by $\phi = \tan^{-1}\dfrac{\omega L}{R}$ and the capacitor current $I_C = \omega CV$ leads $V$ by $90^\circ$.

```figure caption="Phasor diagram at parallel resonance: the reactive component of the coil current I_L sin φ cancels I_C and the line current I = I_L cos φ is in phase with V."
import numpy as _np
from matplotlib.patches import Arc
fig,ax=plt.subplots(figsize=(4.8,2.8)); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.6,6.4); ax.set_ylim(-3.6,4.4)
def ar(p,q,c,lw=1.7): ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="-|>",color=c,lw=lw))
ar((0,0),(5.8,0),INK,1.9); ax.text(5.9,-0.3,"V",fontsize=10)
phi=_np.radians(65); IL=4.0
ar((0,0),(IL*_np.cos(phi),-IL*_np.sin(phi)),"#d9534f"); ax.text(1.9,-3.4,"I$_L$ (lags V by $\\phi$)",fontsize=8,color="#d9534f")
ar((0,0),(IL*_np.cos(phi),IL*_np.sin(phi)),ACCENT); ax.text(1.9,3.9,"I$_C$ (leads V by 90°)",fontsize=8,color=ACCENT)
ar((0,0),(IL*_np.cos(phi),0),"#2a9d4a",2.4); ax.text(0.3,0.3,"I = I$_L$cos$\\phi$ (minimum)",fontsize=8,color="#2a9d4a")
ax.plot([IL*_np.cos(phi)]*2,[-IL*_np.sin(phi),IL*_np.sin(phi)],ls=":",color="#888")
ax.add_patch(Arc((0,0),1.8,1.8,theta1=-65,theta2=0,color=INK,lw=0.9)); ax.text(1.0,-0.55,"$\\phi$",fontsize=9)
ax.text(2.0,-1.2,"I$_L$sin$\\phi$ = I$_C$",fontsize=8,color="#555",rotation=0)
```

*Explanation.* Resolve $I_L$ into an in-phase component $I_L\cos\phi$ and a quadrature (lagging) component $I_L\sin\phi$. The line current is the phasor sum of $I_L$ and $I_C$. The circuit is in **resonance** when the line current is in phase with the supply voltage (unity power factor), that is when the leading capacitor current exactly cancels the lagging reactive component of the coil current:

$$I_C = I_L\sin\phi$$

The line current is then only the in-phase component $I = I_L\cos\phi$, which is the **minimum** possible value, so the impedance is maximum ($Z_d = L/CR$) and the currents circulating between coil and capacitor can be many times the line current (current magnification, $Q = \omega_0L/R$). Below the resonant frequency the circuit is inductive (the net current lags), above it the capacitor current dominates (the net current leads).

*Resonant frequency.*

$$\omega_0C\cdot V = \frac{V}{\sqrt{R^{2} + \omega_0^{2}L^{2}}}\cdot\frac{\omega_0L}{\sqrt{R^{2} + \omega_0^{2}L^{2}}} \;\Rightarrow\; C = \frac{L}{R^{2} + \omega_0^{2}L^{2}}$$

$$\omega_0^{2}L^{2} = \frac{L}{C} - R^{2}$$

$$\boxed{\,\omega_0 = \sqrt{\frac{1}{LC} - \frac{R^{2}}{L^{2}}},\qquad f_0 = \frac{1}{2\pi}\sqrt{\frac{1}{LC} - \frac{R^{2}}{L^{2}}}\,}$$

For $R \to 0$ (ideal coil) this becomes $f_0 = \dfrac{1}{2\pi\sqrt{LC}}$. Resonance exists only if $R < \sqrt{L/C}$. The same result follows by setting the imaginary part of the admittance $Y = j\omega C + \dfrac{1}{R + j\omega L}$ to zero. At resonance $I_{min} = \dfrac{VCR}{L}$ and $Z_d = \dfrac{L}{CR}$.

**(b) Initial values at $t = 0^+$.**

Before closing, the circuit is dead: $i_1(0^-) = 0$ (inductor) and $v_C(0^-) = 0$, with no stored energy. Mesh equations for $t > 0$ (mesh 1: source, 1 H, shared 10 Ω; mesh 2: shared 10 Ω, series 10 Ω, 1 F):

$$12 = \frac{di_1}{dt} + 10(i_1 - i_2) \quad (1)$$

$$\begin{gathered}0 = 10(i_2 - i_1) + 10i_2 + v_C \\ \frac{dv_C}{dt} = \frac{i_2}{C} = i_2 \quad (2)\end{gathered}$$

*Currents at $0^+$.* $i_1(0^+) = 0$ (inductor current continuous). In (2) $v_C(0^+) = 0$: $20i_2 - 10i_1 = 0$, so $i_2(0^+) = 0$.

*First derivatives.* From (1): $\dfrac{di_1}{dt}\Big|_{0^+} = 12 - 10(0 - 0) = 12$ A/s. Differentiating (2): $20i_2' - 10i_1' + i_2/C = 0$ so

$$i_2'(0^+) = \frac{10(12) - 0}{20} = 6\ \text{A/s}$$

*Second derivatives.* Differentiate (1): $0 = i_1'' + 10(i_1' - i_2')$, so $i_1''(0^+) = -10(12 - 6) = -60$ A/s². Differentiate (2) twice: $20i_2'' - 10i_1'' + i_2'/C = 0$:

$$i_2''(0^+) = \frac{10(-60) - 6}{20} = -30.3\ \text{A/s}^{2}$$

| $i_1$ | $i_2$ | $di_1/dt$ | $di_2/dt$ | $d^2i_1/dt^2$ | $d^2i_2/dt^2$ |
|---|---|---|---|---|---|
| 0 A | 0 A | 12 A/s | 6 A/s | −60 A/s² | −30.3 A/s² |

@s 2
**(a) Inductor current and voltage (direct / classical solution).**

Initially $i_L(0^-) = 0$ and $v_C(0^-) = 0$. Let $v$ be the voltage across the parallel combination, $i$ the source current and $i_L$ the inductor current, $C = 1/9$ F.

$$\begin{gathered}60 = 2i + v \\ i = C\frac{dv}{dt} + i_L \\ v = 10i_L + \frac{di_L}{dt}\end{gathered}$$

Eliminating $v$ and $i$:

$$60 = \tfrac29\left(i_L'' + 10i_L'\right) + 2i_L + 10i_L + i_L' \;\Rightarrow\; i_L'' + 14.5\,i_L' + 54\,i_L = 270$$

*Forced response:* $i_{L,f} = 270/54 = 5$ A (equal to $60/(2 + 10)$, DC steady state).

*Natural response:* $s^{2} + 14.5s + 54 = 0$ gives $s = -7.25 \pm j1.199$ (discriminant $14.5^{2} - 216 = -5.75 < 0$): **under-damped**, $\alpha = 7.25$ s$^{-1}$, $\omega_d = 1.199$ rad/s.

$$i_L(t) = 5 + e^{-7.25t}(A\cos1.199t + B\sin1.199t)$$

*Initial conditions:* $i_L(0) = 0 \Rightarrow A = -5$; $i_L'(0) = v(0) - 10i_L(0) = 0 \Rightarrow -7.25A + 1.199B = 0 \Rightarrow B = -30.23$.

$$\boxed{\,i_L(t) = 5 - e^{-7.25t}\left(5\cos1.199t + 30.23\sin1.199t\right)\ \text{A}\,}$$

$$\boxed{\,v_L(t) = L\frac{di_L}{dt} = 225.2\,e^{-7.25t}\sin1.199t\ \text{V}\,}$$

*Checks:* $i_L(0) = 0$, $v_L(0) = 0$ (since $i_L'(0) = 0$), $i_L(\infty) = 5$ A, $v_L(\infty) = 0$. The source current at $0^+$ is $60/2 = 30$ A (uncharged capacitor is a short).

**(b) Switch closing across $R_1$ (Laplace method).**

*Before $t = 0$ (switch open, steady state, DC).* The inductor is short and the capacitor open:

$$\begin{gathered}i_1(0^-) = \frac{V}{R_1 + R_2} = \frac{90}{10 + 20} = 3\ \text{A} \\ i_2(0^-) = 0\end{gathered}$$

The voltage across the capacitor equals the voltage of the node, $v_C(0^-) = i_1R_2 = 3\times20 = 60$ V (no drop in $R_3$ because $i_2 = 0$).

*After the switch closes* $R_1$ is short-circuited and $V = 90$ V is applied directly across both parallel branches, which are independent.

*Branch 1 ($R_2$ + $L$, initial current 3 A):*

$$\frac{90}{s} = (R_2 + sL)I_1 - Li_1(0^-) = (20 + s)I_1 - 3 \;\Rightarrow\; I_1(s) = \frac{90/s + 3}{s + 20} = \frac{4.5}{s} - \frac{1.5}{s + 20}$$

$$\boxed{\,i_1(t) = 4.5 - 1.5e^{-20t}\ \text{A}\,}$$

*Branch 2 ($R_3$ + $C$, initial voltage 60 V):*

$$\frac{90}{s} = R_3I_2 + \frac{I_2}{sC} + \frac{v_C(0^-)}{s} \;\Rightarrow\; I_2(s)\left(20 + \frac{10^{6}}{s}\right) = \frac{90 - 60}{s} \;\Rightarrow\; I_2(s) = \frac{30}{20s + 10^{6}} = \frac{1.5}{s + 50\,000}$$

$$\boxed{\,i_2(t) = 1.5e^{-50\,000t}\ \text{A}\,}$$

(Time constant of branch 2: $R_3C = 20\ \mu$s.) The source current is $i = i_1 + i_2 = 4.5 - 1.5e^{-20t} + 1.5e^{-50\,000t}$ A, with $i(0^+) = 3 + 1.5 = 4.5$ A ($i_1(0) = 3$ A and $i_2(0) = 1.5$ A $= (90 - 60)/20$). In the steady state $i_1 = 4.5$ A and $i_2 = 0$.

@s 3
**(a) Open-circuit (z) parameters and conversion to h-parameters.**

*$z_{11}$ ($I_2 = 0$).* From port 1 the 3 Ω arm is in parallel with the 9 Ω bridge plus 6 Ω (15 Ω), and then the 15 Ω shunt is in series: $z_{11} = (3\parallel15) + 15 = 2.5 + 15 = 17.5\ \Omega$.

*$z_{22}$ ($I_1 = 0$).* From port 2: 6 Ω in parallel with (9 + 3) Ω, then 15 Ω: $z_{22} = (6\parallel12) + 15 = 4 + 15 = 19\ \Omega$.

*$z_{21}$ ($I_2 = 0$).* The node voltage is $V_N = V_1\dfrac{15}{17.5} = 0.857V_1$ and the open-port voltage is $V_2 = V_N + 6\dfrac{V_1 - V_N}{15} = 0.9143V_1$, so $z_{21} = 0.9143\times17.5 = 16\ \Omega$; the network is reciprocal, $z_{12} = z_{21} = 16\ \Omega$.

$$[z] = \begin{bmatrix}17.5 & 16\\ 16 & 19\end{bmatrix}\ \Omega,\qquad \Delta z = 17.5(19) - 16^{2} = 76.5\ \Omega^{2}$$

*Conversion.* $V_1 = h_{11}I_1 + h_{12}V_2$, $I_2 = h_{21}I_1 + h_{22}V_2$. From $I_2 = (V_2 - z_{21}I_1)/z_{22}$:

$$\begin{gathered}h_{11} = \frac{\Delta z}{z_{22}} = \frac{76.5}{19} = 4.026\ \Omega \\ h_{12} = \frac{z_{12}}{z_{22}} = \frac{16}{19} = 0.842\end{gathered}$$

$$\begin{gathered}h_{21} = -\frac{z_{21}}{z_{22}} = -0.842 \\ h_{22} = \frac{1}{z_{22}} = 0.0526\ \text{S}\end{gathered}$$

$$\boxed{[h] = \begin{bmatrix}4.026\ \Omega & 0.842\\ -0.842 & 0.0526\ \text{S}\end{bmatrix}}$$

(Check: reciprocity $h_{12} = -h_{21}$ ✓.)

**(b) Current for the bent iron bar with an air gap.**

```figure caption="Wrought iron bar bent into a ring with a 1 mm air gap and 500 turns."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(3.6,2.7)); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2.4,2.4); ax.set_ylim(-1.7,1.8)
ax.add_patch(mp.Arc((0,0),2.8,2.8,theta1=6,theta2=354,lw=4,color=INK))
for yy in _np.linspace(-0.55,0.55,7): ax.add_patch(mp.Ellipse((-1.4,yy),0.35,0.14,fill=False,ec=ACCENT,lw=1.2))
ax.text(-2.3,0.0,"500\nturns",fontsize=8,ha="center",va="center"); ax.annotate("1 mm gap",xy=(1.4,0.0),xytext=(1.6,1.1),fontsize=8,arrowprops=dict(arrowstyle="->",lw=0.8))
ax.text(0,0,"$\\phi$ = 0.5 mWb\nl = 40 cm\nd = 2 cm",fontsize=8,ha="center",va="center")
```

*Data.* Area $A = \dfrac{\pi}{4}(0.02)^{2} = 3.1416\times10^{-4}$ m². The iron length is $l_i = 0.40 - 0.001 = 0.399$ m (the 40 cm bar is bent so that its ends are 1 mm apart; using 0.40 m changes the answer by under 0.03 percent). Gap $l_g = 10^{-3}$ m. $\phi = 0.5\times10^{-3}$ Wb everywhere (no leakage stated).

*Flux density:* $B = \dfrac{\phi}{A} = \dfrac{0.5\times10^{-3}}{3.1416\times10^{-4}} = 1.59$ T.

*Reluctances:*

$$S_i = \frac{l_i}{\mu_0\mu_rA} = \frac{0.399}{4\pi\times10^{-7}\times4000\times3.1416\times10^{-4}} = 2.527\times10^{5}\ \text{AT/Wb}$$

$$S_g = \frac{l_g}{\mu_0A} = \frac{10^{-3}}{4\pi\times10^{-7}\times3.1416\times10^{-4}} = 2.533\times10^{6}\ \text{AT/Wb}$$

$$NI = \phi(S_i + S_g) = 0.5\times10^{-3}(2.527\times10^{5} + 2.533\times10^{6}) = 126 + 1267 = 1393\ \text{AT}$$

$$\boxed{I = \frac{1393}{500} = 2.79\ \text{A}}$$

The 1 mm gap needs about ten times the ampere-turns of the whole iron path (1267 AT against 126 AT).

@s 4
**(a) Losses and efficiency of a transformer.**

A transformer has no moving parts, so there are only electrical losses:

1. **Core (iron) losses $P_i$**, which depend on the supply voltage and frequency and are practically constant from no load to full load:
   - *Hysteresis loss* $P_h = k_hB_m^{1.6}fV$ (energy lost in re-orienting the magnetic domains each cycle; reduced by silicon steel).
   - *Eddy-current loss* $P_e = k_eB_m^{2}f^{2}t^{2}V$ (circulating currents in the core; reduced by thin laminations of thickness $t$).
2. **Copper losses $P_{cu}$**: $I_1^{2}R_1 + I_2^{2}R_2 = I_2^{2}R_{02}$, which vary as the **square of the load current**.
3. **Stray load and dielectric losses**: leakage-flux eddy currents in the tank and conductors, and insulation (dielectric) losses, usually small.

*Efficiency.* Practical value from the O.C. and S.C. tests:

$$\eta = \frac{\text{output}}{\text{input}} = \frac{V_2I_2\cos\phi_2}{V_2I_2\cos\phi_2 + P_i + P_{cu}}$$

For a fraction $x$ of the full-load kVA $S$ (copper loss $P_{cu}$ at full load):

$$\eta = \frac{xS\cos\phi}{xS\cos\phi + P_i + x^{2}P_{cu}}$$

*Condition for maximum efficiency.* With $V_2$ and $\cos\phi$ constant, $\eta = \dfrac{V_2I_2\cos\phi}{V_2I_2\cos\phi + P_i + I_2^{2}R_{02}}$ is maximum when the denominator divided by $I_2$ is minimum:

$$\frac{d}{dI_2}\left[V_2\cos\phi + \frac{P_i}{I_2} + I_2R_{02}\right] = 0 \;\Rightarrow\; -\frac{P_i}{I_2^{2}} + R_{02} = 0 \;\Rightarrow\; P_i = I_2^{2}R_{02}$$

$$\boxed{\text{Iron loss} = \text{copper loss}\ (P_i = P_{cu}\text{ at that load}),\qquad x_{\eta,max} = \sqrt{\frac{P_i}{P_{cu,fl}}}}$$

The maximum efficiency is $\eta_{max} = \dfrac{xS\cos\phi}{xS\cos\phi + 2P_i}$, and the load current at which it occurs is $I_2 = \sqrt{P_i/R_{02}}$.

```figure caption="Efficiency against load: the maximum occurs where copper loss equals iron loss (here x = 0.6)."
import numpy as _np
fig,ax=plt.subplots(figsize=(4.6,2.5)); x=_np.linspace(0.02,1.4,300); Pi=0.36; Pc=1.0; S=100
eta=100*x*S*0.8/(x*S*0.8+Pi*S*0.01*10+x**2*Pc*S*0.01*10); ax.plot(x,eta,color=ACCENT,lw=1.8)
xm=_np.sqrt(Pi/Pc); ax.axvline(xm,color="#888",ls=":",lw=0.9); ax.text(xm+0.03,eta.min()+2,"P$_{cu}$ = P$_i$",fontsize=8)
ax.set_xlabel("load as a fraction of full load, x",fontsize=8); ax.set_ylabel("efficiency %",fontsize=8); ax.tick_params(labelsize=7)
for sp_ in ("top","right"): ax.spines[sp_].set_visible(False)
```

**(b) DC shunt generator and motor.**

*Generator:* $I_L = \dfrac{10\,000}{500} = 20$ A, $I_{sh} = \dfrac{500}{250} = 2$ A, $I_a = 20 + 2 = 22$ A.

$$E_g = V + I_aR_a = 500 + 22(0.5) = 511\ \text{V}$$

*Motor:* input 50 kW at 500 V, $I_L = \dfrac{50\,000}{500} = 100$ A, $I_{sh} = 2$ A (same field, same flux), $I_a = 100 - 2 = 98$ A.

$$E_b = V - I_aR_a = 500 - 98(0.5) = 451\ \text{V}$$

With the flux constant, $E \propto N$:

$$N_m = 1000\times\frac{451}{511} = \boxed{882.6\ \text{rpm}}$$

@s 5
**(a) Speed control of DC motors.** From the emf and torque relations

$$N = \frac{V - I_aR_a}{k\,\phi} = k'\frac{E_b}{\phi},$$

the speed can be changed by varying the flux $\phi$, the armature-circuit resistance, or the armature terminal voltage $V$.

*DC shunt motor.*

1. **Flux (field) control**: a rheostat $R_{sh}$ in series with the shunt field reduces $I_{sh}$ and $\phi$, so the speed rises above the base speed ($N \propto 1/\phi$). Simple, efficient (small field loss) and the commonest method; the range is limited by commutation and stability (about 1:3 to 1:5), and the armature current rises for constant torque.
2. **Armature (rheostatic) control**: a resistance $R_x$ in series with the armature lowers the voltage across the armature so the speed falls *below* the base speed: $N \propto V - I_a(R_a + R_x)$. The speed varies with load, and the resistor wastes power, so it is used only for short-time control.
3. **Armature voltage control**: a variable voltage on the armature with a constant field (Ward–Leonard system with motor-generator set, or a thyristor/chopper drive) gives smooth speed control from zero up to base speed at constant torque, with high efficiency; the field control above base speed gives a very wide range.

*DC series motor* (the flux is proportional to the armature current).

1. **Flux control**: (a) *field diverter* (a resistance in parallel with the series field) reduces the field current and raises the speed, (b) *armature diverter* (a resistance across the armature) lowers the flux needed for a given torque and raises or lowers the speed as the torque is constant, (c) *tapped field control*: the number of series turns is changed by taps, fewer turns give a higher speed (used in electric traction and fans).
2. **Armature (rheostatic) control**: a variable resistance in series with the armature and field lowers the voltage and reduces the speed below normal; the speed falls at the cost of $I^{2}R$ loss (used in cranes and for starting).
3. **Series-parallel control**: two motors in a traction drive are connected in series (each at half the voltage, half speed) or in parallel (full voltage, full speed).
4. **Supply-voltage control** (chopper or tap-changing) is also used.

**(b) Short notes.**

**(i) Double field revolving theory.** A single-phase winding carries a current that produces a **pulsating** (alternating, stationary-axis) mmf $F(\theta, t) = F_m\cos\omega t\cos\theta$. This is resolved into two rotating fields of equal magnitude $F_m/2$ rotating at synchronous speed in opposite directions:

$$F_m\cos\omega t\cos\theta = \frac{F_m}{2}\cos(\theta - \omega t) + \frac{F_m}{2}\cos(\theta + \omega t)$$

The forward field $\phi_f$ and the backward field $\phi_b$ each induce rotor emfs and torques $T_f$ and $T_b$ in the rotor. At standstill the slip is 1 for both fields, $T_f = T_b$ and the **net starting torque is zero**: a single-phase induction motor is not self-starting. If the rotor is turned in either direction (or a starting winding supplies a quadrature field) the forward torque exceeds the backward torque (the rotor slip is $s$ relative to the forward field and $2 - s$ relative to the backward field) and the motor accelerates:

$$T = T_f - T_b$$

```figure caption="Forward and backward torque-slip curves of a single-phase induction motor and their difference (zero at standstill)."
import numpy as _np
fig,ax=plt.subplots(figsize=(4.8,2.6)); n=_np.linspace(-1,1,400); R=0.25
def tq(s): return s*R/(R**2+(s*0.5)**2)
sf=1-n; sb=1+n
ax.plot(n,tq(sf)/2,color=ACCENT,lw=1.3,label="T$_f$"); ax.plot(n,-tq(sb)/2,color="#d9534f",lw=1.3,label="T$_b$"); ax.plot(n,(tq(sf)-tq(sb))/2,color=INK,lw=2,label="T = T$_f$ − T$_b$")
ax.axhline(0,color="#888",lw=0.7); ax.axvline(0,color="#888",lw=0.7,ls=":"); ax.set_xlabel("rotor speed  N / N$_s$",fontsize=8); ax.set_ylabel("torque",fontsize=8); ax.set_yticks([]); ax.tick_params(labelsize=7); ax.legend(fontsize=7,frameon=False)
for sp_ in ("top","right"): ax.spines[sp_].set_visible(False)
```

**(ii) Stepper motor.** A stepper motor is a brushless synchronous motor that converts electrical pulses into **discrete angular steps** (open-loop position control). Each pulse that switches the stator excitation turns the shaft by a fixed **step angle**.

*Types.* (1) *Variable-reluctance (VR)*: soft-iron toothed rotor, wound stator poles; the rotor aligns itself to the position of minimum reluctance with the excited phase. (2) *Permanent-magnet (PM)*: a magnetised rotor aligns with the excited stator poles. (3) *Hybrid*: combines both, with small step angles (1.8° or 0.9°) and high torque.

*Principle (VR, 3-phase).* The stator has 6 poles (three phases A, A′; B, B′; C, C′) and the rotor has 4 teeth. Exciting A attracts the nearest rotor teeth; switching A → B → C → A makes the rotor move one step each time:

$$\begin{gathered}\text{step angle } \beta = \frac{360^\circ}{m\,N_r} = \frac{360^\circ}{3\times4} = 30^\circ \\ \text{speed} = \frac{\beta\times\text{pulse rate (steps/s)}}{360}\ \text{rev/s}\end{gathered}$$

The direction is reversed by reversing the excitation sequence; the speed is set by the pulse frequency; the position is set by the number of pulses.

*Advantages:* no feedback needed, accurate positioning without cumulative error, holding torque at standstill, simple digital interface. *Limits:* resonance and loss of steps at high speed or overload, low efficiency. *Applications:* printers, CNC machines, 3-D printers, robotics, disk drives, clocks, valve control and instrumentation.
