---
file: NEBians-IOE-Past-Paper-Electric-Circuits-and-Machines-EE460-2077-Chaitra.pdf
subject: Electric Circuits and Machines
level: BE · Year I / Part II
code: EE 460
year_bs: 2077 Chaitra
cal: BS
year_ad: 2021
stream: BEI
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular. Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · All questions carry equal marks · Assume suitable data if necessary</small>

@q 1
Explain the phenomena of resonance in parallel circuit and also derive the expression for resonance frequency and the impedance at resonance. [[8]]

@q 2
Find currents and voltages across each elements at t = 0+. Also find dV$_c$/dt and dI$_L$/dt for t = 0+. [[8]]

```figure caption="Circuit of Question 2: 45 V source, 4 H and 2 Ω in series, a 2 F capacitor to the common line, and a 1 Ω branch with the switch (t = 0) and a 60 V source."
fig,ax=ckt_canvas(6.2,3.0,xlim=(-2.6,12.4),ylim=(-0.5,4.4))
vsrc(ax,(0,0),(0,3),"45 V",side=1,off=1.2); ind(ax,(0,3),(2.6,3),"4 H",side=1); res(ax,(2.6,3),(5.2,3),"2 Ω",side=1)
node(ax,(5.2,3)); cap(ax,(5.2,3),(5.2,0),"2 F",side=-1,off=1.0)
res(ax,(5.2,3),(7.4,3),"1 Ω",side=1); switch(ax,(7.4,3),(9.4,3),"t = 0",side=1)
vsrc(ax,(9.4,0),(9.4,3),"60 V",side=-1,off=1.2)
wire(ax,[(0,0),(9.4,0)]); node(ax,(5.2,0))
```

@q 3
Find the expression of current and voltage across inductor for t > 0 using direct solution method. [[8]]

```figure caption="Circuit of Question 3: 12 V source, switch (t = 0) and 2.75 Ω in series, feeding a 1/4 Ω + 1/3 H branch in parallel with a 1 F capacitor."
fig,ax=ckt_canvas(6.0,3.0,xlim=(-2.6,10.6),ylim=(-0.5,4.4))
vsrc(ax,(0,0),(0,3),"12 V",side=1,off=1.2); wire(ax,[(0,3),(1.0,3)]); switch(ax,(1.0,3),(2.8,3),"t = 0",side=1)
res(ax,(2.8,3),(5.0,3),"2.75 Ω",side=1); wire(ax,[(5.0,3),(8,3)]); node(ax,(5.0,3))
res(ax,(5.0,3),(5.0,1.6),"1/4 Ω",side=1,body=0.9,off=1.0); ind(ax,(5.0,1.6),(5.0,0),"1/3 H",side=1,body=1.0,off=1.0)
cap(ax,(8,3),(8,0),"1 F",side=1,off=1.0); wire(ax,[(0,0),(8,0)]); node(ax,(5.0,0))
```

@q 4
In the network shown, the switch is closed at t = 0, with the network previously unenergised. For the element value given on diagram, find the expression for mesh currents i$_1$(t) and i$_2$(t), by Laplace Transformation method. [[8]]

```figure caption="Circuit of Question 4: 100 V source, switch K (t = 0) and 1 H in mesh 1; 5 Ω is the shared branch; mesh 2 holds a 5 Ω and a 2 μF capacitor."
fig,ax=ckt_canvas(6.2,3.0,xlim=(-2.6,11.2),ylim=(-0.5,4.4))
vsrc(ax,(0,0),(0,3),"100 V",side=1,off=1.3); wire(ax,[(0,3),(0.6,3)]); switch(ax,(0.6,3),(2.4,3),"K  (t = 0)",side=1)
ind(ax,(2.4,3),(4.6,3),"1 H",side=1); node(ax,(4.6,3)); res(ax,(4.6,3),(4.6,0),"5 Ω",side=-1,off=1.0)
res(ax,(4.6,3),(7.2,3),"5 Ω",side=1); wire(ax,[(7.2,3),(8.8,3)]); cap(ax,(8.8,3),(8.8,0),"2 μF",side=1,off=1.2)
wire(ax,[(0,0),(8.8,0)]); node(ax,(4.6,0))
label(ax,(2.3,1.5),"i$_1$",size=10); label(ax,(6.7,1.5),"i$_2$",size=10)
```

@q 5
Find Z parameters of the two port network shown and check its reciprocity. [[8]]

```figure caption="Two-port of Question 5: 2 Ω shunt at port 1, 1 Ω series, dependent current source 4V1 (pointing down), 2 Ω series and 1 Ω shunt at port 2."
fig,ax=ckt_canvas(6.4,2.8,xlim=(-1.4,10.2),ylim=(-0.8,4.2))
terminal(ax,(0,3)); terminal(ax,(0,0)); label(ax,(-0.9,1.5),"V$_1$",size=9); label(ax,(0.9,3.5),"I$_1$",size=9)
wire(ax,[(0,3),(1.6,3)]); node(ax,(1.6,3)); res(ax,(1.6,3),(1.6,0),"2 Ω",side=1,off=1.0)
res(ax,(1.6,3),(4.2,3),"1 Ω",side=1); node(ax,(4.2,3)); isrc(ax,(4.2,3),(4.2,0),"4V$_1$",side=1,off=1.2)
res(ax,(4.2,3),(6.8,3),"2 Ω",side=1); node(ax,(6.8,3)); res(ax,(6.8,3),(6.8,0),"1 Ω",side=1,off=1.0)
wire(ax,[(6.8,3),(8.4,3)]); terminal(ax,(8.4,3)); terminal(ax,(8.4,0)); label(ax,(9.3,1.5),"V$_2$",size=9); label(ax,(7.6,3.5),"I$_2$",size=9)
wire(ax,[(0,0),(8.4,0)]); node(ax,(1.6,0)); node(ax,(4.2,0)); node(ax,(6.8,0))
```

@q 6
A wrought iron bar 40 cm long and 3 cm in diameter is bent into a circular shape as in following figure. It is then wound with 800 turns of wire. Calculate the current required to produce a flux of 0.35 mWb in the magnetic circuit in the following cases. [[8]]

(a) No air gap

(b) With an air gap of 1 mm; assume the following data for the magnetization iron

| H in AT/m | 2500 | 3000 | 3500 | 4000 |
|---|---|---|---|---|
| B in T | 1.55 | 1.59 | 1.6 | 1.615 |

```figure caption="Question 6: the wrought-iron bar bent into a ring (mean length 40 cm, 3 cm diameter) with an 800-turn winding; case (b) has a 1 mm air gap."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(3.6,3.0)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Wedge((0,0),1.0,8,352,width=0.26,facecolor="#c9d3e6",edgecolor=INK,lw=1.2))
for k in range(12):
    a=_np.radians(40+k*22); ax.plot([0.74*_np.cos(a)-0.0,1.02*_np.cos(a)],[0.74*_np.sin(a),1.02*_np.sin(a)],color=ACCENT,lw=1.0)
ax.annotate("air gap  1 mm",xy=(0.87,0.0),xytext=(1.15,0.55),fontsize=8,arrowprops=dict(arrowstyle="->",lw=0.8,color=INK))
ax.text(0,0,"N = 800 turns\nΦ = 0.35 mWb\nl = 40 cm, d = 3 cm",ha="center",va="center",fontsize=8)
ax.annotate("",xy=(0,0.86),xytext=(-0.3,0.84),arrowprops=dict(arrowstyle="->",color="#b00020",lw=1.2)); ax.text(-0.12,0.64,"Φ",fontsize=9,color="#b00020")
ax.set_xlim(-1.2,1.9); ax.set_ylim(-1.15,1.15)
```

@q 7
A 10 kVA, 200/400 V, 50 Hz single phase transformer gave the following test results: [[8]]

| Test | Voltage | Current | Power |
|---|---|---|---|
| OC test (hv winding open) | 220 V | 1.3 A | 120 W |
| SC test (lv winding short-circuited) | 22 V | 30 A | 200 W |

Find parameters of equivalent circuit as referred to lv winding.

@q 8
Derive the emf equation and torque equation of dc machine, defining corresponding terms involved. [[8]]

@q 9
Describe the torque speed characteristic of three phase induction motor showing starting torque, maximum torque and operating region. Also show the effect of rotor resistance in the T-S characteristics with a conclusion. [[8]]

@q 10
What are initial conditions? Explain the procedure to evaluate the initial condition. [[8]]
<!-- SOLUTIONS -->

@s 1
**Parallel resonance.** A circuit with a coil and a capacitor in parallel is in **resonance** when the supply voltage and the line current are in phase: the net susceptance is zero, the power factor is unity and the circuit behaves as a pure resistance. At resonance the energy swings between the magnetic field of the coil and the electric field of the capacitor, so the supply only supplies the losses (the coil resistance).

*Practical circuit.* The branch currents are $I_{coil} = \dfrac{V}{R + j\omega L}$ and $I_C = j\omega CV$. The admittance is

$$Y = j\omega C + \frac{1}{R + j\omega L} = \underbrace{\frac{R}{R^{2} + \omega^{2}L^{2}}}_{G} + j\underbrace{\left[\omega C - \frac{\omega L}{R^{2} + \omega^{2}L^{2}}\right]}_{B}$$

**Resonant frequency.** Resonance means $B = 0$ (the line current is in phase with $V$):

$$C = \frac{L}{R^{2} + \omega_0^{2}L^{2}} \;\Rightarrow\; \omega_0^{2} = \frac{1}{LC} - \frac{R^{2}}{L^{2}}$$

$$\boxed{\,\omega_0 = \sqrt{\frac{1}{LC} - \frac{R^{2}}{L^{2}}}\ \text{rad/s},\qquad f_0 = \frac{1}{2\pi}\sqrt{\frac{1}{LC} - \frac{R^{2}}{L^{2}}}\,}$$

If $R \ll \omega_0L$ (high-$Q$ coil) this reduces to $f_0 \approx \dfrac{1}{2\pi\sqrt{LC}}$. Resonance exists only when $R < \sqrt{L/C}$ (otherwise $\omega_0$ is imaginary). For an ideal coil ($R = 0$) it is exactly $1/\sqrt{LC}$.

**Impedance at resonance (dynamic impedance).** With $B = 0$ the admittance is the conductance $G_0 = \dfrac{R}{R^{2} + \omega_0^{2}L^{2}}$, and using $R^{2} + \omega_0^{2}L^{2} = L/C$:

$$\boxed{\,Z_0 = \frac{1}{G_0} = \frac{R^{2} + \omega_0^{2}L^{2}}{R} = \frac{L}{CR} = Z_d\,}$$

It is purely resistive and **maximum** (minimum line current $I_0 = V/Z_d$), the opposite of a series circuit. In terms of the coil quality factor $Q_0 = \omega_0L/R$: $Z_d = R(1 + Q_0^{2}) \approx Q_0\omega_0L$.

*Circulating current.* At resonance the coil current and the capacitor current are each $Q_0$ times the line current (current magnification), which is why the parallel resonant circuit is called a *rejector*; the bandwidth is $BW = f_0/Q_0 = R/(2\pi L)$.

```figure caption="Parallel resonance: (a) phasor diagram at resonance - the capacitor current IC cancels the reactive part of the coil current IL, so the line current I = V/Zd is in phase with V; (b) impedance against frequency, maximum at f0."
import numpy as _np
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.6,2.7))
a1.annotate("",xy=(3,0),xytext=(0,0),arrowprops=dict(arrowstyle="->",color=INK,lw=1.6)); a1.text(3.05,-0.12,"V",fontsize=9)
a1.annotate("",xy=(1.4,-2.0),xytext=(0,0),arrowprops=dict(arrowstyle="->",color=ACCENT,lw=1.6)); a1.text(1.5,-2.05,"I$_L$",fontsize=9,color=ACCENT)
a1.annotate("",xy=(1.4,2.0),xytext=(0,0),arrowprops=dict(arrowstyle="->",color="#2a7a4b",lw=1.6)); a1.text(1.5,2.0,"I$_C$",fontsize=9,color="#2a7a4b")
a1.annotate("",xy=(1.4,0.0),xytext=(0,0),arrowprops=dict(arrowstyle="->",color="#b00020",lw=2.2)); a1.text(1.4,0.18,"I = I$_L$cosφ$_L$",fontsize=8,color="#b00020")
a1.plot([1.4,1.4],[-2.0,2.0],ls=":",color="#888",lw=0.8); a1.set_xlim(-0.3,4.1); a1.set_ylim(-2.6,2.6); a1.axis("off"); a1.set_title("(a) phasors at resonance",fontsize=9)
L=1e-3;C=1e-6;R=10.0; f=_np.linspace(2000,8000,800); w=2*_np.pi*f
Z=_np.abs(1/(1j*w*C+1/(R+1j*w*L))); a2.plot(f/1000,Z,color=ACCENT,lw=1.8)
f0=_np.sqrt(1/(L*C)-R**2/L**2)/(2*_np.pi); a2.axvline(f0/1000,color="#888",ls=":",lw=0.9); a2.text(f0/1000+0.1,Z.max()*0.5,"f$_0$",fontsize=9)
a2.set_xlabel("f (kHz)",fontsize=8); a2.set_ylabel("|Z| (Ω)",fontsize=8); a2.tick_params(labelsize=8); a2.set_title("(b) |Z| = L/(CR) at f$_0$",fontsize=9)
for sp_ in ("top","right"): a2.spines[sp_].set_visible(False)
fig.tight_layout()
```

@s 2
The switch (marked $t = 0$) is in the 1 Ω branch with the 60 V source. It is drawn open, so it **closes at $t = 0$** (the opposite case, a switch that opens, is also worked at the end).

*Before $t = 0$ (switch open, DC steady state).* The inductor behaves as a short and the capacitor as an open circuit, so no current flows in the 45 V loop:

$$\begin{gathered}i_L(0^-) = 0 \\ v_C(0^-) = 45\ \text{V (no drop in 4 H or 2 Ω)}\end{gathered}$$

*At $t = 0^+$.* The inductor current and capacitor voltage cannot jump: $i_L(0^+) = 0$ and $v_C(0^+) = 45$ V. The 60 V source is now connected through 1 Ω to the node:

$$i_{1\Omega}(0^+) = \frac{60 - 45}{1} = 15\ \text{A}$$

KCL at the node: $i_C = i_{1\Omega} - i_L = 15 - 0 = 15$ A. The 2 Ω carries $i_L = 0$ so $v_{2\Omega} = 0$, and KVL in the left loop gives $v_L = 45 - 0 - v_C = 45 - 0 - 45 = 0$ V.

| Element | Current at $0^+$ | Voltage at $0^+$ |
|---|---|---|
| 45 V source | 0 A | 45 V |
| 4 H inductor | 0 A | $0$ V |
| 2 Ω | 0 A | 0 V |
| 2 F capacitor | 15 A (downwards) | 45 V |
| 1 Ω | 15 A (towards the node) | 15 V |
| 60 V source | 15 A | 60 V |
| Switch | 15 A | 0 V |

**Derivatives at $0^+$.**

$$\boxed{\,\frac{dv_C}{dt}\bigg|_{0^+} = \frac{i_C(0^+)}{C} = \frac{15}{2} = 7.5\ \text{V/s},\qquad \frac{di_L}{dt}\bigg|_{0^+} = \frac{v_L(0^+)}{L} = \frac{0}{4} = 0\ \text{A/s}\,}$$

*If the switch were closed for a long time and opens at $t = 0$:* before $t = 0$ the capacitor is open, the loop $60\to1\ \Omega\to$ node $\to2\ \Omega\to4\ \text{H}\to45$ V carries $i_L(0^-) = \dfrac{60 - 45}{1 + 2} = 5$ A and $v_C(0^-) = 60 - 5 = 55$ V. At $0^+$: $i_L = 5$ A, $v_C = 55$ V, the 1 Ω branch carries 0, so the whole $i_L$ charges the capacitor: $i_C = 5$ A. Then $v_{2\Omega} = 10$ V, $v_L = 45 - 10 - 55 = -20$ V, so $\dfrac{dv_C}{dt} = \dfrac{5}{2} = 2.5$ V/s and $\dfrac{di_L}{dt} = \dfrac{-20}{4} = -5$ A/s.

@s 3
**Which case.** The 12 V source is in series with 2.75 Ω and the switch. With the switch closed for a long time (DC steady state) the inductor is a short and the capacitor an open circuit, which gives clean values ($2.75 + 0.25 = 3\ \Omega$), so the switch is read as **opening at $t = 0$** (the source-free response). The case of a switch that closes on a de-energised network is given at the end.

**Initial conditions ($t = 0^-$).**

$$\begin{gathered}i_L(0^-) = \frac{12}{2.75 + 0.25} = 4\ \text{A} \\ v_C(0^-) = 0.25\times4 = 1\ \text{V}\end{gathered}$$

**Network equation for $t > 0$.** The source is disconnected. The capacitor discharges into the $R$–$L$ branch: with the loop current $i = i_L$ (taken out of the capacitor),

$$\begin{gathered}v_C = Ri + L\frac{di}{dt} \\ i = -C\frac{dv_C}{dt}\end{gathered}$$

Eliminating $v_C$:

$$LC\frac{d^{2}i}{dt^{2}} + RC\frac{di}{dt} + i = 0 \;\Rightarrow\; \frac{1}{3}\frac{d^{2}i}{dt^{2}} + \frac{1}{4}\frac{di}{dt} + i = 0 \;\Rightarrow\; \frac{d^{2}i}{dt^{2}} + 0.75\frac{di}{dt} + 3i = 0$$

**Complementary function (direct solution).** Characteristic equation $s^{2} + 0.75s + 3 = 0$:

$$s = -0.375 \pm j\sqrt{3 - 0.375^{2}} = -0.375 \pm j1.691$$

Complex roots, so the circuit is under-damped ($\alpha = 0.375$ s$^{-1}$, $\omega_d = 1.691$ rad/s). There is no source, so the particular integral is zero:

$$i_L(t) = e^{-0.375t}\left(K_1\cos1.691t + K_2\sin1.691t\right)$$

**Constants.** $i_L(0^+) = 4 \Rightarrow K_1 = 4$. For the derivative: $L\dfrac{di}{dt}\Big|_{0^+} = v_C(0^+) - Ri(0^+) = 1 - 0.25\times4 = 0$, so $\dfrac{di}{dt}\Big|_{0^+} = 0$:

$$-0.375K_1 + 1.691K_2 = 0 \;\Rightarrow\; K_2 = \frac{0.375\times4}{1.691} = 0.887$$

$$\boxed{\,i_L(t) = e^{-0.375t}\left(4\cos1.691t + 0.887\sin1.691t\right)\ \text{A},\quad t \ge 0\,}$$

**Voltage across the inductor.**

$$\frac{di}{dt} = e^{-0.375t}\left[(-0.375\times4 + 1.691\times0.887)\cos1.691t - (0.375\times0.887 + 1.691\times4)\sin1.691t\right] = -7.097\,e^{-0.375t}\sin1.691t$$

$$\boxed{\,v_L(t) = L\frac{di}{dt} = -2.366\,e^{-0.375t}\sin1.691t\ \text{V},\quad t \ge 0\,}$$

*Check:* $v_L(0^+) = 0$ ✓ (equal to $v_C - Ri = 1 - 1$), and the response was also verified by numerical integration of the two state equations (for example $i_L(1) = 0.276$ A).

*If the switch instead closes at $t = 0$ on a de-energised network* ($i_L(0) = 0$, $v_C(0) = 0$): the state equations are $C\dot v = \dfrac{12 - v}{2.75} - i$ and $L\dot i = v - 0.25i$, giving $s^{2} + 1.1136s + 3.2727 = 0$, $s = -0.557 \pm j1.721$. The final values are $i = 4$ A, $v = 1$ V, so

$$i_L(t) = 4 - e^{-0.557t}\left(4\cos1.721t + 1.294\sin1.721t\right)\ \text{A}$$

```figure caption="Question 3: inductor current and voltage after the switch opens (under-damped, alpha = 0.375 s-1, omega_d = 1.691 rad/s)."
import numpy as _np
t=_np.linspace(0,14,600); i=_np.exp(-0.375*t)*(4*_np.cos(1.691*t)+0.887*_np.sin(1.691*t)); v=-2.366*_np.exp(-0.375*t)*_np.sin(1.691*t)
fig,ax=plt.subplots(figsize=(4.8,2.5)); ax.plot(t,i,color=ACCENT,lw=1.8,label="i$_L$ (A)"); ax.plot(t,v,color="#2a7a4b",lw=1.5,label="v$_L$ (V)")
ax.plot(t,4*_np.exp(-0.375*t),color="#999",ls=":",lw=0.9); ax.axhline(0,color="#888",lw=0.6)
ax.set_xlabel("t (s)",fontsize=8); ax.tick_params(labelsize=8); ax.legend(fontsize=8,frameon=False)
for sp_ in ("top","right"): ax.spines[sp_].set_visible(False)
```

@s 4
**Laplace model ($t > 0$, zero initial conditions).** $C = 2\ \mu\text{F}$, so $\dfrac{1}{sC} = \dfrac{5\times10^{5}}{s}$. Mesh 1 contains $V$, $sL = s$ and the shared 5 Ω; mesh 2 contains 5 Ω, the shared 5 Ω and the capacitor.

$$\begin{gathered}(s + 5)I_1 - 5I_2 = \frac{100}{s} \\ -5I_1 + \left(10 + \frac{5\times10^{5}}{s}\right)I_2 = 0\end{gathered}$$

**Solve for $I_2$ in terms of $I_1$.**

$$I_2 = \frac{5I_1}{10 + 5\times10^{5}/s} = \frac{sI_1}{2s + 10^{5}}$$

Substituting in the first equation:

$$I_1\left[(s + 5) - \frac{5s}{2s + 10^{5}}\right] = \frac{100}{s} \;\Rightarrow\; I_1(s) = \frac{200(s + 50000)}{s\,(2s^{2} + 100005s + 500000)}$$

$$I_2(s) = \frac{sI_1}{2s + 10^{5}} = \frac{100}{2s^{2} + 100005s + 500000}$$

**Poles.** $2s^{2} + 100005s + 500000 = 0$ gives $s_1 = -49997.50$ and $s_2 = -5.00025$ (real and widely separated: the fast pole belongs to the 2 μF with the 10 Ω, the slow one to $L/R$).

**Mesh current $i_2$.**

$$I_2(s) = \frac{50}{(s + 49997.5)(s + 5.00025)} = \frac{1.0001\times10^{-3}}{s + 5.00025} - \frac{1.0001\times10^{-3}}{s + 49997.5}$$

$$\boxed{\,i_2(t) = 1.0\times10^{-3}\left(e^{-5.0t} - e^{-49997.5t}\right)\ \text{A}\ \approx\ 1\ \text{mA}\cdot e^{-5t}\ \text{for}\ t \gg 20\ \mu\text{s}\,}$$

**Mesh current $i_1$.** Partial fractions of $I_1(s)$:

$$I_1(s) = \frac{20}{s} + \frac{1.0\times10^{-7}}{s + 49997.5} - \frac{20.0}{s + 5.00025}$$

$$\boxed{\,i_1(t) = 20 - 20.0\,e^{-5.00025t} + 1.0\times10^{-7}e^{-49997.5t}\ \text{A} \approx 20\left(1 - e^{-5t}\right)\ \text{A}\,}$$

**Checks.** (i) $i_1(0) = 20 - 20 + 10^{-7} \approx 0$ ✓ and $i_2(0) = 0$ ✓. (ii) $\dfrac{di_1}{dt}\Big|_0 = 20\times5.00025 - 0.005 = 100$ A/s $= V/L$ ✓ (all of 100 V appears across the inductor at $t = 0^+$). (iii) Final values: the inductor is a short and the capacitor blocks, so $i_2(\infty) = 0$ and $i_1(\infty) = \dfrac{100}{5} = 20$ A ✓. Time constants: $L/R_{eq}$ with $R_{eq} = 5\ \Omega$ gives the 0.2 s mode ($s = -5$), and $10\ \Omega\times2\ \mu\text{F} = 20\ \mu\text{s}$ the fast one.

@s 5
Label the nodes: node 1 is at port 1 ($V_1$), node M follows the 1 Ω series arm, node 2 is at port 2 ($V_2$). The dependent current source $4V_1$ leaves node M towards the common line (the arrow points down). Both $I_1$ and $I_2$ enter the network.

**Node equations.**

$$\begin{gathered}\text{Node 1:}\quad I_1 = \frac{V_1}{2} + \frac{V_1 - V_M}{1} \\ \text{Node M:}\quad \frac{V_1 - V_M}{1} = \frac{V_M - V_2}{2} + 4V_1 \\ \text{Node 2:}\quad I_2 = \frac{V_2}{1} + \frac{V_2 - V_M}{2}\end{gathered}$$

**Eliminate $V_M$.** From the node M equation:

$$V_1 - V_M - 4V_1 = \frac{V_M - V_2}{2} \;\Rightarrow\; -3V_1 - V_M = 0.5V_M - 0.5V_2 \;\Rightarrow\; V_M = -2V_1 + \frac{V_2}{3}$$

Put this in the node 1 and node 2 equations:

$$\begin{gathered}I_1 = 1.5V_1 - V_M = 1.5V_1 + 2V_1 - \frac{V_2}{3} = 3.5V_1 - \frac{1}{3}V_2 \\ I_2 = 1.5V_2 - 0.5V_M = 1.5V_2 + V_1 - \frac{V_2}{6} = V_1 + \frac{4}{3}V_2\end{gathered}$$

This is the $Y$ form: $\begin{bmatrix}I_1\\I_2\end{bmatrix} = \begin{bmatrix}3.5 & -1/3\\ 1 & 4/3\end{bmatrix}\begin{bmatrix}V_1\\V_2\end{bmatrix}$. Invert it ($\Delta_Y = 3.5\times\tfrac43 + \tfrac13 = 5$):

$$[Z] = [Y]^{-1} = \frac{1}{5}\begin{bmatrix}4/3 & 1/3\\ -1 & 3.5\end{bmatrix}$$

$$\boxed{\,z_{11} = \frac{4}{15} = 0.267\ \Omega,\quad z_{12} = \frac{1}{15} = 0.067\ \Omega,\quad z_{21} = -\frac{1}{5} = -0.2\ \Omega,\quad z_{22} = \frac{7}{10} = 0.7\ \Omega\,}$$

i.e. $V_1 = 0.267I_1 + 0.067I_2$ and $V_2 = -0.2I_1 + 0.7I_2$.

*Direct check by open-circuit tests.* With $I_2 = 0$: node 2 gives $V_M = 3V_2$; node M then gives $V_2 = -0.75V_1$; node 1 gives $I_1 = 1.5V_1 - 3V_2 = 3.75V_1$, so $z_{11} = 0.267\ \Omega$ and $z_{21} = V_2/I_1 = -0.75/3.75 = -0.2\ \Omega$ ✓.

**Reciprocity.** A network without dependent sources is reciprocal when $z_{12} = z_{21}$ (equivalently $\Delta_T = AD - BC = 1$). Here

$$z_{12} = 0.067\ \Omega \ne z_{21} = -0.2\ \Omega$$

so the network is **not reciprocal** (the dependent source $4V_1$ makes it an active, non-reciprocal two-port).

@s 6
**Cross-section and flux density.**

$$\begin{gathered}A = \frac{\pi d^{2}}{4} = \frac{\pi(0.03)^{2}}{4} = 7.069\times10^{-4}\ \text{m}^2 \\ B = \frac{\Phi}{A} = \frac{0.35\times10^{-3}}{7.069\times10^{-4}} = 0.495\ \text{T}\end{gathered}$$

The magnetising force of the iron comes from its $B$–$H$ curve: $AT = Hl_i + H_gl_g$ and $I = AT/N$ with $N = 800$.

**Reading note on the data.** The printed table lists only $B \ge 1.55$ T (it corresponds to a flux $\Phi \ge 1.10$ mWb in this 3 cm bar), so it does not cover the printed flux of 0.35 mWb ($B = 0.495$ T). For $B = 0.495$ T the iron is far below its knee, where wrought iron is nearly linear with a high relative permeability, so $\mu_r = 4000$ (the value used for iron elsewhere in these papers) is taken. The table method is then shown on a flux that lies in the table range.

**(a) No air gap.** Mean length $l = 40$ cm $= 0.4$ m.

$$H = \frac{B}{\mu_0\mu_r} = \frac{0.4951}{4\pi\times10^{-7}\times4000} = 98.5\ \text{AT/m}$$

$$\begin{gathered}AT = Hl = 98.5\times0.4 = 39.4\ \text{AT} \\ \boxed{\,I = \frac{39.4}{800} = 0.049\ \text{A}\,}\end{gathered}$$

**(b) With a 1 mm air gap.** Iron length $l_i = 0.40 - 0.001 = 0.399$ m. In the air gap (no fringing, same area):

$$\begin{gathered}H_g = \frac{B}{\mu_0} = \frac{0.4951}{4\pi\times10^{-7}} = 3.940\times10^{5}\ \text{AT/m} \\ AT_g = H_gl_g = 3.940\times10^{5}\times10^{-3} = 394.0\ \text{AT}\end{gathered}$$

$$AT_{iron} = 98.5\times0.399 = 39.3\ \text{AT}$$

$$\begin{gathered}AT_{total} = 394.0 + 39.3 = 433.3\ \text{AT} \\ \boxed{\,I = \frac{433.3}{800} = 0.542\ \text{A}\,}\end{gathered}$$

The 1 mm gap needs about 11 times the ampere-turns: 91 % of the m.m.f. is used in the gap.

**Using the printed table (flux inside its range).** The method is the same, with $H$ read (and interpolated) from the table at $B = \Phi/A$. Example: for $B = 1.6$ T ($\Phi = 1.131$ mWb) the table gives $H = 3500$ AT/m, so

$$\begin{gathered}\text{(a)}\quad AT = 3500\times0.4 = 1400,\quad I = 1.75\ \text{A} \\ \text{(b)}\quad AT = 3500\times0.399 + \frac{1.6}{4\pi\times10^{-7}}\times10^{-3} = 1396.5 + 1273.2 = 2669.7,\quad I = 3.34\ \text{A}\end{gathered}$$

For a flux between table points (for example $B = 1.57$ T) interpolate: $H = 2500 + \dfrac{1.57 - 1.55}{1.59 - 1.55}\times500 = 2750$ AT/m.

@s 7
**Which side each test is on.** The OC test is done on the **lv winding** (hv open): 220 V, 1.3 A, 120 W. The SC test is done on the **hv winding** (lv shorted): 22 V, 30 A, 200 W. The turns ratio is $K = \dfrac{400}{200} = 2$. The test voltage of 220 V and current of 30 A are used as printed (the rated hv current is $10000/400 = 25$ A).

**Open-circuit test (lv side) → shunt branch.**

$$\begin{gathered}\cos\phi_0 = \frac{P_0}{V_0I_0} = \frac{120}{220\times1.3} = 0.4196,\quad \sin\phi_0 = 0.9077 \\ I_w = I_0\cos\phi_0 = 0.5455\ \text{A},\quad I_\mu = I_0\sin\phi_0 = 1.180\ \text{A} \\ R_0 = \frac{V_0}{I_w} = \frac{220}{0.5455} = 403.3\ \Omega,\quad X_0 = \frac{V_0}{I_\mu} = \frac{220}{1.180} = 186.4\ \Omega\end{gathered}$$

**Short-circuit test (hv side) → series branch, referred to hv.**

$$\begin{gathered}Z_{01(hv)} = \frac{22}{30} = 0.7333\ \Omega,\quad R_{01(hv)} = \frac{200}{30^{2}} = 0.2222\ \Omega \\ X_{01(hv)} = \sqrt{0.7333^{2} - 0.2222^{2}} = 0.6989\ \Omega\end{gathered}$$

**Refer to the lv winding** (divide by $K^{2} = 4$):

$$\boxed{\,R_{01(lv)} = \frac{0.2222}{4} = 0.0556\ \Omega,\quad X_{01(lv)} = \frac{0.6989}{4} = 0.1747\ \Omega,\quad Z_{01(lv)} = 0.1833\ \Omega\,}$$

$$\boxed{\,R_0 = 403.3\ \Omega,\qquad X_0 = 186.4\ \Omega\ \ (\text{already on the lv side})\,}$$

*For reference, on the hv side:* $R_0' = 4\times403.3 = 1613\ \Omega$, $X_0' = 745.7\ \Omega$, $R_{01} = 0.2222\ \Omega$, $X_{01} = 0.6989\ \Omega$.

```figure caption="Equivalent circuit of the transformer referred to the lv winding: shunt branch R0 || X0 (403.3 Ω, 186.4 Ω) and series R01 = 0.0556 Ω, X01 = 0.1747 Ω."
fig,ax=ckt_canvas(6.4,2.8,xlim=(-2.6,12.0),ylim=(-0.8,4.2))
terminal(ax,(0,3)); terminal(ax,(0,0)); label(ax,(-1.6,1.5),"V$_1$",size=9)
wire(ax,[(0,3),(1.6,3)]); node(ax,(1.6,3)); res(ax,(1.6,3),(1.6,0),"R$_0$ = 403.3 Ω",side=-1,off=1.5)
wire(ax,[(1.6,3),(3.6,3)]); node(ax,(3.6,3)); ind(ax,(3.6,3),(3.6,0),"X$_0$ = 186.4 Ω",side=1,off=1.6)
res(ax,(3.6,3),(6.4,3),"R$_{01}$ = 0.0556 Ω",side=1); ind(ax,(6.4,3),(9.0,3),"X$_{01}$ = 0.1747 Ω",side=1)
wire(ax,[(9.0,3),(10.2,3)]); terminal(ax,(10.2,3)); terminal(ax,(10.2,0)); label(ax,(11.0,1.5),"V$_2'$",size=9)
wire(ax,[(0,0),(10.2,0)]); node(ax,(1.6,0)); node(ax,(3.6,0))
```

@s 8
**Terms.** $\phi$ = flux per pole (Wb); $P$ = number of poles; $Z$ = total number of armature conductors; $A$ = number of parallel paths ($A = P$ for lap, $A = 2$ for wave winding); $N$ = speed (rpm); $I_a$ = armature current.

**(i) Emf equation.** In one revolution each conductor cuts the flux of all poles, $P\phi$ Wb, in a time $60/N$ s. The average emf induced in one conductor (Faraday's law) is

$$e_{cond} = \frac{d\Phi}{dt} = \frac{P\phi}{60/N} = \frac{P\phi N}{60}\ \text{V}$$

There are $Z/A$ conductors in series in each parallel path, and the generated emf equals the emf of one path:

$$\boxed{\,E_g = \frac{\phi ZNP}{60A}\ \text{V}\,}$$

With $\omega = 2\pi N/60$ this is $E = \dfrac{PZ}{2\pi A}\phi\omega = K_a\phi\omega$ with $K_a = \dfrac{PZ}{2\pi A}$. In a generator $E_g = V + I_aR_a$; in a motor the same expression is the back emf, $E_b = V - I_aR_a$.

**(ii) Torque equation.** Let $r$ be the armature radius and $l$ the active length. A conductor carrying $I_c = I_a/A$ in a flux density $B$ experiences a force $F = BI_cl$, giving a torque $F\,r$. The flux per pole is $\phi = B\times\dfrac{2\pi rl}{P}$, hence $Bl = \dfrac{P\phi}{2\pi r}$ and

$$T_{cond} = BlI_c\,r = \frac{P\phi}{2\pi r}\cdot\frac{I_a}{A}\cdot r = \frac{P\phi I_a}{2\pi A}$$

For $Z$ conductors:

$$\boxed{\,T_a = \frac{PZ\phi I_a}{2\pi A} = 0.159\,\frac{PZ}{A}\,\phi I_a\ \text{N·m} = K_a\phi I_a\,}$$

*Consistency with the power balance:* $E_bI_a = T_a\omega$ gives $T_a = \dfrac{E_bI_a}{2\pi N/60} = \dfrac{\phi ZNP}{60A}\cdot\dfrac{60I_a}{2\pi N} = \dfrac{PZ\phi I_a}{2\pi A}$ ✓. Since the shaft torque is $T_{sh} = T_a - $ (rotational loss torque), the shaft output is $P_{out} = T_{sh}\omega$.

@s 9
**Torque–slip expression** (per-phase equivalent circuit, stator voltage $V_1$, $\omega_s = 2\pi n_s$ the synchronous speed in rad/s, $X = X_1 + X_2'$):

$$T = \frac{3}{\omega_s}\cdot\frac{V_1^{2}\,R_2'/s}{\left(R_1 + R_2'/s\right)^{2} + X^{2}}$$

**Characteristic.** The torque against speed curve (speed from standstill, $s = 1$, to synchronous speed, $s = 0$) has three important points:

1. **Starting torque** ($s = 1$, $N = 0$):

$$T_{st} = \frac{3}{\omega_s}\frac{V_1^{2}R_2'}{(R_1 + R_2')^{2} + X^{2}}$$

2. **Maximum (breakdown, pull-out) torque** at the slip $s_m$ obtained from $dT/ds = 0$:

$$\begin{gathered}s_m = \frac{R_2'}{\sqrt{R_1^{2} + X^{2}}} \\ T_{max} = \frac{3}{2\omega_s}\cdot\frac{V_1^{2}}{R_1 + \sqrt{R_1^{2} + X^{2}}}\end{gathered}$$

3. **Synchronous speed** ($s = 0$): torque is zero (no rotor emf, so no rotor current).

**Operating region.** From $s = 0$ to $s = s_m$ the torque rises almost linearly with slip (the curve is nearly straight, $T \propto s$ because $R_2'/s \gg X$). Here the machine is **stable**: if the load rises, the speed falls, the slip and torque rise to balance it. The normal full-load slip is 2–5 % (speed 95–98 % of $n_s$). For $s_m < s < 1$ the torque falls as slip rises ($T \propto 1/s$), so the region is unstable (the motor stalls if the load exceeds $T_{max}$); it is traversed only during starting.

**Effect of rotor resistance.** $T_{max}$ is independent of $R_2'$, but $s_m \propto R_2'$:

- as $R_2'$ rises, the peak moves towards lower speed (larger $s_m$) with the same height;
- $T_{st}$ rises with $R_2'$ and becomes equal to $T_{max}$ when $s_m = 1$, i.e. $R_2' = \sqrt{R_1^{2} + X^{2}}$; beyond that $T_{st}$ falls again;
- for a given load torque the slip increases with $R_2'$, so the speed falls and the copper loss and heating rise (efficiency $\approx 1 - s$ falls).

```figure caption="Torque-speed characteristic of a three-phase induction motor for rotor resistances R2' = 0.4, 1.0, 2.06 and 4.0 Ω (R1 = 0.5 Ω, X = 2 Ω): same T_max, peak moving left, starting torque rising until R2' = sqrt(R1² + X²)."
import numpy as _np
R1=0.5; X=2.0; V=230.0; ws=2*_np.pi*1500/60
s=_np.linspace(1e-4,1,800)
def T(R2): return 3/ws*V**2*(R2/s)/((R1+R2/s)**2+X**2)
fig,ax=plt.subplots(figsize=(5.4,3.1))
cols=[ACCENT,"#2a7a4b","#b46a00","#7a3fb0"]
for R2,c in zip([0.4,1.0,_np.hypot(R1,X),4.0],cols):
    ax.plot(1-s,T(R2),color=c,lw=1.6,label="R$_2'$ = %.2f Ω"%R2)
R2=0.4; sm=R2/_np.hypot(R1,X); Tm=T(R2).max(); Tst=T(R2)[-1]
ax.axvspan(1-sm,1.0,color="#2a7a4b",alpha=0.07); ax.text(0.93,Tm*0.18,"stable\noperating\nregion",ha="center",fontsize=7.5,color="#2a7a4b")
ax.text(0.40,Tm*0.07,"unstable",ha="center",fontsize=7.5,color="#555")
ax.plot([1-sm],[Tm],"o",color=ACCENT,ms=4); ax.annotate("T$_{max}$",xy=(1-sm,Tm),xytext=(0.52,Tm*1.02),fontsize=8,arrowprops=dict(arrowstyle="->",lw=0.7))
ax.plot([0],[Tst],"o",color=ACCENT,ms=4); ax.annotate("T$_{st}$ (R$_2'$ = 0.4)",xy=(0,Tst),xytext=(0.05,Tst+Tm*0.18),fontsize=8,arrowprops=dict(arrowstyle="->",lw=0.7))
ax.set_xlabel("speed N / N$_s$   (1 - s)",fontsize=8); ax.set_ylabel("torque T (N·m)",fontsize=8); ax.set_xlim(0,1.02); ax.set_ylim(0,Tm*1.2)
ax.tick_params(labelsize=8); ax.legend(fontsize=7.5,frameon=False,loc="upper left",bbox_to_anchor=(0.0,0.85))
for sp_ in ("top","right"): ax.spines[sp_].set_visible(False)
fig.tight_layout()
```

**Conclusion.** A low rotor resistance (squirrel-cage motor) gives a small slip and high efficiency but a poor starting torque (and a large starting current). Adding external resistance in the rotor of a slip-ring motor gives a high starting torque with a lower starting current and permits speed control, at the price of efficiency; the maximum torque does not change.

@s 10
**Initial conditions.** In a network containing energy-storage elements, the initial conditions are the values of the currents and voltages and of their derivatives at the instant just after the switching action, $t = 0^+$ (the switch operates at $t = 0$). They fix the arbitrary constants in the complete solution of the differential equation (classical method) and enter the Laplace transform of every $L$ and $C$ (as $Li(0^+)$ and $v(0^+)/s$). The state variables are $i_L(0^+)$ and $v_C(0^+)$, plus $di/dt$, $dv/dt$ and higher derivatives for higher-order circuits.

**Principle of continuity.** The energy stored in an inductor ($\tfrac12Li^{2}$) and in a capacitor ($\tfrac12Cv^{2}$) cannot change in zero time (that would need infinite power). Hence

$$\begin{gathered}i_L(0^+) = i_L(0^-) \\ v_C(0^+) = v_C(0^-)\end{gathered}$$

Other currents and voltages (resistor, inductor voltage, capacitor current) may jump at $t = 0$.

**Procedure to evaluate them.**

1. **Find the state at $t = 0^-$.** Using the circuit before switching in DC steady state: replace each $L$ by a short circuit and each $C$ by an open circuit, then find $i_L(0^-)$ and $v_C(0^-)$ (if the network was unenergised both are zero).
2. **Apply continuity:** $i_L(0^+) = i_L(0^-)$, $v_C(0^+) = v_C(0^-)$.
3. **Draw the equivalent circuit at $t = 0^+$** with the new switch position:

| Element | Zero initial energy | Non-zero initial energy |
|---|---|---|
| Inductor $L$ | open circuit ($i = 0$) | current source $I_0 = i_L(0^+)$ |
| Capacitor $C$ | short circuit ($v = 0$) | voltage source $V_0 = v_C(0^+)$ |
| Resistor $R$ | $R$ | $R$ |

4. **Solve the resistive network** (KVL, KCL, mesh or node) to get every other current and voltage at $0^+$, such as $v_L(0^+)$, $i_C(0^+)$ and the resistor values.
5. **Initial derivatives:**

$$\begin{gathered}\frac{di_L}{dt}\bigg|_{0^+} = \frac{v_L(0^+)}{L} \\ \frac{dv_C}{dt}\bigg|_{0^+} = \frac{i_C(0^+)}{C}\end{gathered}$$

   and for the second derivatives differentiate the loop/node equation once and substitute the $0^+$ values.
6. Use the values to determine the constants of the solution.

*Example.* A series $R$–$L$ circuit ($R = 10\ \Omega$, $L = 2$ H) with a 20 V source switched on at $t = 0$: $i_L(0^-) = 0$, so the inductor is open at $0^+$: $i(0^+) = 0$, $v_R(0^+) = 0$, $v_L(0^+) = 20$ V and $\dfrac{di}{dt}\Big|_{0^+} = \dfrac{20}{2} = 10$ A/s. Question 2 above is a worked case with both an inductor and a capacitor.
