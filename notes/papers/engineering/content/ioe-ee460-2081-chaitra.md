---
file: NEBians-IOE-Past-Paper-Electric-Circuits-and-Machines-EE460-2081-Chaitra.pdf
subject: Electric Circuits and Machines
level: BE · Year I / Part II
code: EE 460
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BEI
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper. Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · All questions carry equal marks · Assume suitable data if necessary</small>

@q 1
(a) Explain the phenomenon of resonance of a practical coil connected with capacitor in parallel. Why parallel resonance is also known as current resonance? [[8]]
(b) The switch has been in position 'a' for a long long time. At t = 0, it is suddenly thrown to position 'b'. At t = 0+, find q$_c$, V$_c$, V$_L$, i$_{4Ω}$, i$_{2Ω}$, i$_{6Ω}$, i$_c$, V$_{ab}$, dV$_c$/dt and di/dt of the inductor. [[8]]

```figure caption="Circuit of Question 1(b): 12 V source, switch a/b, 2 Ω, 6 Ω, 4 Ω, 2 F and 3 H."
fig,ax=ckt_canvas(5.6,3.0,xlim=(-1.2,9.2),ylim=(-0.6,3.9))
batt(ax,(0,0.7),(0,2.0),"12 V",side=-1)
wire(ax,[(0,2.0),(0,3),(2.1,3)]); wire(ax,[(0,0.7),(0,0),(8,0)])
node(ax,(2.1,3)); label(ax,(2.1,3.35),"a")
node(ax,(3,3)); node(ax,(3,2.05)); label(ax,(3.35,2.05),"b")
ax.plot([3,3.0],[3,2.15],color=INK,lw=1.6)
label(ax,(3.45,2.75),"t = 0",size=8)
res(ax,(3,3),(5.4,3),"2 Ω",side=1)
res(ax,(3,2.05),(3,0),"6 Ω",side=-1)
node(ax,(5.4,3)); wire(ax,[(5.4,3),(5.4,2.0)]); cap(ax,(5.4,2.0),(5.4,0),"2 F",side=1)
res(ax,(5.4,3),(8,3),"4 Ω",side=1); ind(ax,(8,3),(8,0),"3 H",side=1)
node(ax,(5.4,0)); node(ax,(3,0))
```

@q 2
(a) Initially, the switch S was opened. Find the expression of current supplied by source at t > 0, if switch S is closed at t = 0 using classical method. [[8]]

```figure caption="Circuit of Question 2(a): 40 V source, switch S, 4 Ω, 0.5 F and the 4 Ω + 0.1 H branch."
fig,ax=ckt_canvas(5.4,3.0,xlim=(-1.4,9.4),ylim=(-0.6,3.9))
vsrc(ax,(0,0),(0,3),"40 V",side=-1)
switch(ax,(0,3),(2.4,3),"S",side=1)
res(ax,(2.4,3),(5,3),"4 Ω",side=1)
node(ax,(5,3)); wire(ax,[(5,3),(8,3)])
cap(ax,(5,3),(5,0),"0.5 F",side=1)
res(ax,(8,3),(8,1.6),"4 Ω",side=1,body=0.9); ind(ax,(8,1.6),(8,0),"0.1 H",side=1,body=1.0)
wire(ax,[(0,0),(8,0)]); node(ax,(5,0))
```

(b) A sinusoidal voltage V(t) = 250 sin 10t is applied at time t = 0 to a series R-L circuit comprising R = 5 Ω and L = 1 H. Obtain the particular solution for the current i(t) in the circuit. Also determine voltage across each element. Use Laplace transform method. [[8]]

@q 3
(a) Obtain the open circuit parameter of the network shown below. Convert the obtained parameter into T-parameter. [[8]]

```figure caption="Network of Question 3(a): 3 Ω and 6 Ω series arms, 15 Ω shunt arm and a 9 Ω bridge between the two top terminals."
fig,ax=ckt_canvas(5.4,3.0,xlim=(-0.9,8.9),ylim=(-0.8,4.2))
terminal(ax,(0,2)); terminal(ax,(8,2)); terminal(ax,(0,0)); terminal(ax,(8,0))
wire(ax,[(0,2),(1,2)]); res(ax,(1,2),(3.5,2),"3 Ω",side=-1); res(ax,(3.5,2),(6,2),"6 Ω",side=-1); wire(ax,[(6,2),(8,2)])
wire(ax,[(1,2),(1,3.4)]); res(ax,(1,3.4),(6,3.4),"9 Ω",side=1); wire(ax,[(6,3.4),(6,2)])
node(ax,(1,2)); node(ax,(6,2)); node(ax,(3.5,2))
res(ax,(3.5,2),(3.5,0),"15 Ω",side=1)
wire(ax,[(0,0),(8,0)]); node(ax,(3.5,0))
label(ax,(-0.5,1.0),"1",size=9); label(ax,(8.5,1.0),"2",size=9)
```

(b) A cast steel magnetic structure made of a bar of section 2 cm × 2 cm is shown in figure below. Determine the current that the 500 turn magnetizing coil on the left limb should carry so that a flux of 2 mWb is produced in the right limb. Take μ$_r$ = 600 and neglect leakage. [[8]]

```figure caption="Magnetic structure of Question 3(b): three limbs E (coil), C (centre) and D, each window 25 cm wide and 15 cm high, section 2 cm × 2 cm."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.2,2.7)); ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-12,56); ax.set_ylim(-5,21)
ax.add_patch(mp.Rectangle((0,0),50,15,fill=False,lw=2.4,ec=INK))
ax.plot([25,25],[0,15],color=INK,lw=2.4)
for yy in _np.linspace(3.5,11.5,8):
    ax.add_patch(mp.Ellipse((0,yy),3.4,1.4,fill=False,ec=ACCENT,lw=1.3))
ax.plot([-7,-1.5],[11.5,11.5],color=INK,lw=1); ax.plot([-7,-1.5],[3.5,3.5],color=INK,lw=1)
ax.text(-9.8,7.5,"500\nturns",fontsize=8,ha="center",va="center")
ax.text(0,16.8,"E",fontsize=9,ha="center"); ax.text(25,16.8,"C",fontsize=9,ha="center"); ax.text(50,16.8,"D",fontsize=9,ha="center")
ax.annotate("",xy=(12.5,15.9),xytext=(0,15.9),arrowprops=dict(arrowstyle="<->",color=INK,lw=0.9)); 
ax.text(12.5,18.3,"25 cm",fontsize=8,ha="center")
ax.annotate("",xy=(50,15.9),xytext=(25,15.9),arrowprops=dict(arrowstyle="<->",color=INK,lw=0.9)); ax.text(37.5,18.3,"25 cm",fontsize=8,ha="center")
ax.annotate("",xy=(27.8,0),xytext=(27.8,15),arrowprops=dict(arrowstyle="<->",color=INK,lw=0.9)); ax.text(31.6,7.5,"15 cm",fontsize=8,ha="center",va="center")
ax.annotate("",xy=(4,5),xytext=(4,10),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.2)); ax.text(7,7.5,"$\\phi$",fontsize=10,color="#d9534f")
ax.annotate("",xy=(22,10),xytext=(22,5),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.2)); ax.text(19,7.5,"$\\phi_1$",fontsize=10,color="#d9534f")
ax.annotate("",xy=(46,5),xytext=(46,10),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.2)); ax.text(42.8,7.5,"$\\phi_2$",fontsize=10,color="#d9534f")
```

@q 4
(a) Why testing of transformer is essential? Explain open circuit and short circuit test in detail. [[8]]
(b) A single phase transformer takes 10 A on no-load at 0.2 p.f. lagging. The turn ratio is 4:1 (step down). If the load on the secondary is 200 A at a pf of 0.85 lagging, find the primary current and power factor. Neglect the voltage drop in the winding. Also draw the phasor diagram. [[8]]

@q 5
(a) A 250 V DC shunt motor has an armature resistance of 0.5 Ω and field winding resistance of 125 Ω, motor drives a load at 600 rpm and draw the current of 22 A from the supply. A resistance of 50 Ω is connected in series with the field winding keeping the load torque constant. Calculate the speed of motor. [[8]]
(b) "Three phase induction motors are self-starting." Justify the statement showing how three phase supply produces rotating magnetic field. [[8]]
<!-- SOLUTIONS -->

@s 1
**(a) Parallel resonance of a practical coil with a capacitor.**

A practical coil has inductance $L$ and unavoidable winding resistance $R$ (a series $R$–$L$ branch). It is connected in parallel with an ideal capacitor $C$ across a supply $V$ of variable frequency.

```figure caption="Practical coil (R + jωL) in parallel with C; phasor diagram at resonance and the line-current curve."
import numpy as _np
fig=plt.figure(figsize=(6.2,2.7))
a1=fig.add_axes([0.0,0.0,0.46,1.0]); a1.set_aspect("equal"); a1.axis("off"); a1.set_xlim(-0.6,6.4); a1.set_ylim(-1.7,4.4)
a1.annotate("",xy=(5.6,0),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.8)); a1.text(5.7,-0.35,"V",fontsize=10)
phi=_np.radians(70)
IL=3.4; a1.annotate("",xy=(IL*_np.cos(phi),-IL*_np.sin(phi)),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.6)); a1.text(1.4,-1.5,"I$_{coil}$ (lags V by $\\phi$)",fontsize=7.5,color="#d9534f")
a1.annotate("",xy=(IL*_np.cos(phi),IL*_np.sin(phi)),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.6)); a1.text(1.4,3.8,"I$_C$ (leads V by 90°)",fontsize=7.5,color=ACCENT)
a1.annotate("",xy=(IL*_np.cos(phi),0),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color="#2a9d4a",lw=2.2)); a1.text(0.15,0.25,"I = I$_{min}$",fontsize=7.5,color="#2a9d4a")
a1.plot([IL*_np.cos(phi)]*2,[-IL*_np.sin(phi),IL*_np.sin(phi)],ls=":",color="#888",lw=0.9)
a1.add_patch(__import__("matplotlib.patches",fromlist=["Arc"]).Arc((0,0),1.6,1.6,theta1=-70,theta2=0,color=INK,lw=0.9)); a1.text(0.95,-0.45,"$\\phi$",fontsize=8)
a2=fig.add_axes([0.58,0.2,0.4,0.72])
w=_np.linspace(0.3,1.9,400); Rr,Ll,Cc=0.15,1.0,1.0
Y=1j*w*Cc+1/(Rr+1j*w*Ll); a2.plot(w,abs(Y),color=ACCENT,lw=1.8)
w0=_np.sqrt(1/(Ll*Cc)-(Rr/Ll)**2); a2.axvline(w0,color="#888",ls=":",lw=0.9); a2.text(w0+0.04,abs(Y).max()*0.92,"$\\omega_0$",fontsize=9)
a2.set_xlabel("frequency  $\\omega$",fontsize=8); a2.set_ylabel("line current  |I| / V",fontsize=8); a2.tick_params(labelsize=7); a2.set_yticks([]); a2.set_xticks([])
for sp_ in ("top","right"): a2.spines[sp_].set_visible(False)
```

*Admittance of the circuit.*

$$Y = j\omega C + \frac{1}{R + j\omega L} = \frac{R}{R^{2}+\omega^{2}L^{2}} + j\left[\omega C - \frac{\omega L}{R^{2}+\omega^{2}L^{2}}\right]$$

*Resonance condition.* The circuit is in resonance when the supply voltage and the line current are in phase, that is the imaginary part of $Y$ is zero:

$$\omega_0 C = \frac{\omega_0 L}{R^{2}+\omega_0^{2}L^{2}} \;\Rightarrow\; R^{2}+\omega_0^{2}L^{2} = \frac{L}{C}$$

$$\begin{gathered}\omega_0 = \sqrt{\frac{1}{LC}-\frac{R^{2}}{L^{2}}} \\ f_0 = \frac{1}{2\pi}\sqrt{\frac{1}{LC}-\frac{R^{2}}{L^{2}}}\end{gathered}$$

If $R \ll \omega L$ then $f_0 \approx 1/(2\pi\sqrt{LC})$. Resonance is possible only if $R < \sqrt{L/C}$.

*Properties at resonance.*

- The admittance is a pure conductance $Y_0 = \dfrac{R}{R^{2}+\omega_0^{2}L^{2}} = \dfrac{CR}{L}$, the **minimum** value of $|Y|$, so the line current is **minimum**: $I_{min} = V\dfrac{CR}{L}$.
- The impedance is maximum and purely resistive (dynamic impedance) $Z_d = \dfrac{L}{CR}$.
- The power factor is unity. The reactive component of the coil current, $I_L\sin\phi$, exactly equals the capacitor current $I_C$ (phasor diagram), so the line carries only the in-phase component $I_L\cos\phi$.
- Quality factor $Q_0 = \dfrac{\omega_0 L}{R}$; bandwidth $BW = \dfrac{f_0}{Q_0}$.
- Below $f_0$ the circuit is inductive (lagging), above $f_0$ it is capacitive (leading).

**Why it is called current resonance.** The coil current $I_L$ and the capacitor current $I_C$ are equal in their reactive parts, and each is about $Q_0$ times the line current:

$$\begin{gathered}I_C = \omega_0 C V \\ \frac{I_C}{I} = \frac{\omega_0 C V}{V CR/L} = \frac{\omega_0 L}{R} = Q_0\end{gathered}$$

So a small line current sustains a large circulating current $Q_0 I$ between the coil and the capacitor: the currents in the branches are *magnified* while the supply current is at its minimum. This current magnification is the counterpart of voltage magnification in series resonance, hence parallel resonance is called **current resonance** (also an *anti-resonance* or rejector circuit because it rejects the resonant frequency by offering a maximum impedance).

**(b) Initial conditions at t = 0+ after the switch moves from a to b.**

*State at t = 0− (switch in a for a long time, DC steady state).* The capacitor is open and the inductor is a short, so the 12 V source drives 2 Ω + 4 Ω:

$$\begin{gathered}i_L(0^-) = \frac{12}{2+4} = 2\ \text{A} \\ v_C(0^-) = 4\times 2 = 8\ \text{V}\end{gathered}$$

*Continuity.* A capacitor voltage and an inductor current cannot jump, so $v_C(0^+) = 8$ V and $i_L(0^+) = 2$ A.

*After switching.* The source is disconnected. The 2 Ω and 6 Ω resistors are now in series (8 Ω) from the common node N to the bottom rail, in parallel with the capacitor and with the 4 Ω + 3 H branch. The node voltage at $0^+$ is $v_C = 8$ V.

1. Charge on the capacitor: $q_c = C\,v_C = 2\times 8 = 16$ C.
2. Capacitor voltage: $V_c(0^+) = 8$ V.
3. Current in 2 Ω and 6 Ω (series): $i_{2Ω} = i_{6Ω} = \dfrac{8}{2+6} = 1$ A (from N to ground).
4. Current in 4 Ω (the inductor current): $i_{4Ω} = i_L = 2$ A.
5. KCL at N: capacitor current (taken downwards through the capacitor, N to ground) $i_c = -(1+2) = -3$ A. The capacitor is discharging; 3 A flows out of its positive plate.
6. Inductor voltage: $V_L = v_N - 4 i_L = 8 - 4(2) = 0$ V.
7. $\dfrac{dV_c}{dt} = \dfrac{i_c}{C} = \dfrac{-3}{2} = -1.5$ V/s.
8. $\dfrac{di_L}{dt} = \dfrac{V_L}{L} = \dfrac{0}{3} = 0$ A/s.
9. Voltage across the switch contacts: contact 'a' is still at the source voltage $+12$ V while contact 'b' sits at the top of the 6 Ω resistor, $6 i_{6Ω} = 6$ V, so $V_{ab} = 12 - 6 = 6$ V (taking the battery positive at the top).

| Quantity at 0+ | $q_c$ | $V_c$ | $V_L$ | $i_{4Ω}$ | $i_{2Ω}$ | $i_{6Ω}$ | $i_c$ | $V_{ab}$ | $dV_c/dt$ | $di/dt$ |
|---|---|---|---|---|---|---|---|---|---|---|
| Value | 16 C | 8 V | 0 V | 2 A | 1 A | 1 A | −3 A | 6 V | −1.5 V/s | 0 A/s |

@s 2
**(a) Current supplied by the source (classical method).**

Before closing, the capacitor is uncharged and the inductor carries no current: $v_C(0^-) = 0$, $i_L(0^-) = 0$. Let $v$ be the voltage across the capacitor (and across the 4 Ω + 0.1 H branch), $i$ the source current and $i_L$ the inductor current for $t > 0$.

$$\begin{gathered}40 = 4i + v \\ i = 0.5\frac{dv}{dt} + i_L \\ v = 4 i_L + 0.1\frac{di_L}{dt}\end{gathered}$$

Eliminating $v$ and $i$ in favour of $i_L$:

$$\begin{gathered}v = 4i_L + 0.1 i_L' \\ i = 0.5v' + i_L = 0.05\,i_L'' + 2 i_L' + i_L\end{gathered}$$

$$40 = 4(0.05 i_L'' + 2 i_L' + i_L) + 4 i_L + 0.1 i_L' \;\Rightarrow\; i_L'' + 40.5\, i_L' + 40\, i_L = 200$$

*Roots of the characteristic equation* $s^{2} + 40.5 s + 40 = 0$:

$$\begin{gathered}s_{1,2} = \frac{-81 \pm \sqrt{5921}}{4} \\ s_1 = -1.013,\quad s_2 = -39.487\ \text{s}^{-1}\end{gathered}$$

Two distinct real roots: over-damped response.

*Forced (steady-state) part.* In DC steady state the capacitor is open and the inductor a short: $i_L(\infty) = \dfrac{40}{4+4} = 5$ A.

$$i_L(t) = 5 + K_1 e^{s_1 t} + K_2 e^{s_2 t}$$

*Initial conditions:* $i_L(0) = 0$ and $i_L'(0) = \dfrac{v(0) - 4i_L(0)}{0.1} = 0$.

$$\begin{gathered}K_1 + K_2 = -5 \\ s_1 K_1 + s_2 K_2 = 0 \;\Rightarrow\; K_1 = -5.1316,\quad K_2 = 0.1316\end{gathered}$$

$$i_L(t) = 5 - 5.1316\,e^{-1.013t} + 0.1316\,e^{-39.487t}\ \text{A}$$

*Source current.* Using $i = 0.05 i_L'' + 2 i_L' + i_L$ and $0.05 s^{2} + 2 s + 1 = -0.025 s - 1$ for each root:

$$i(t) = 5 + K_1(-0.025 s_1 - 1)e^{s_1 t} + K_2(-0.025 s_2 - 1)e^{s_2 t}$$

$$\boxed{\,i(t) = 5 + 5.0017\,e^{-1.013t} - 0.0017\,e^{-39.49t}\ \text{A}\,}$$

*Checks:* $i(0^+) = 5 + 5.0017 - 0.0017 = 10$ A $= 40/4$ (the uncharged capacitor is a short and the inductor an open circuit at $t = 0^+$), and $i(\infty) = 5$ A. The fast term is negligible after about 0.1 s, so practically $i(t) \approx 5 + 5e^{-t}$ A.

**(b) Series R–L with sinusoidal voltage (Laplace transform method).**

$v(t) = 250\sin 10t$, $R = 5\ \Omega$, $L = 1$ H, $i(0^-) = 0$.

$$\begin{gathered}V(s) = \frac{250\times 10}{s^{2}+100} = \frac{2500}{s^{2}+100} \\ I(s) = \frac{V(s)}{R + sL} = \frac{2500}{(s+5)(s^{2}+100)}\end{gathered}$$

Partial fractions: $I(s) = \dfrac{A}{s+5} + \dfrac{Bs + D}{s^{2}+100}$.

$$\begin{gathered}A = \frac{2500}{25+100} = 20 \\ B = -20 \\ D = 100\end{gathered}$$

$$I(s) = \frac{20}{s+5} + \frac{-20 s + 100}{s^{2}+100} = \frac{20}{s+5} - 20\frac{s}{s^{2}+100} + 10\frac{10}{s^{2}+100}$$

$$i(t) = 20 e^{-5t} - 20\cos 10t + 10\sin 10t$$

Writing the sinusoidal part as one wave: $-20\cos 10t + 10\sin 10t = 22.36\sin(10t - 63.43^\circ)$, since $|Z| = \sqrt{5^{2}+10^{2}} = 11.18\ \Omega$, $\theta = \tan^{-1}(10/5) = 63.43^\circ$ and $250/11.18 = 22.36$ A.

*Particular solution (steady state):*

$$\boxed{\,i_p(t) = 22.36\sin(10t - 63.43^\circ)\ \text{A}\,}$$

The complete response is $i(t) = 20e^{-5t} + 22.36\sin(10t - 63.43^\circ)$ A, with $i(0) = 20 - 20 = 0$.

*Voltage across each element:*

$$v_R = 5\,i = 100 e^{-5t} + 111.8\sin(10t - 63.43^\circ)\ \text{V}$$

$$v_L = L\frac{di}{dt} = -100 e^{-5t} + 223.6\cos(10t - 63.43^\circ)\ \text{V}$$

*Check:* $v_R + v_L$ at $t = 0$: $100 + 111.8(-0.894) - 100 + 223.6(0.447) = 0 = 250\sin 0$. Steady-state amplitudes: $V_R = 111.8$ V, $V_L = 223.6$ V, and $\sqrt{111.8^{2} + 223.6^{2}} = 250$ V.

@s 3
**(a) Open-circuit (impedance, z) parameters.**

$$\begin{gathered}V_1 = z_{11}I_1 + z_{12}I_2 \\ V_2 = z_{21}I_1 + z_{22}I_2\end{gathered}$$

$z_{11} = V_1/I_1$ and $z_{21} = V_2/I_1$ with port 2 open; $z_{22} = V_2/I_2$ and $z_{12} = V_1/I_2$ with port 1 open.

*$z_{11}$ (port 2 open).* From port 1 there are two routes to the junction N: the 3 Ω arm, and the 9 Ω bridge followed by the 6 Ω arm (9 + 6 = 15 Ω). They are in parallel, then in series with the 15 Ω shunt:

$$z_{11} = (3\parallel 15) + 15 = 2.5 + 15 = 17.5\ \Omega$$

*$z_{21}$ (port 2 open).* With $I_1$ entering port 1, $V_N = V_1\dfrac{15}{17.5} = 0.857V_1$. The 15 Ω route carries $(V_1 - V_N)/15 = 0.00952V_1$, so the open port-2 voltage is the drop of $V_N$ plus the 6 Ω drop:

$$V_2 = V_N + 6\left(\frac{V_1 - V_N}{15}\right) = 0.857V_1(0.6) + 0.4V_1 = 0.9143V_1 \;\Rightarrow\; z_{21} = 0.9143\times 17.5 = 16\ \Omega$$

*$z_{22}$ (port 1 open).* From port 2, the 6 Ω arm and the (9 + 3) = 12 Ω route are in parallel, in series with the 15 Ω:

$$z_{22} = (6\parallel 12) + 15 = 4 + 15 = 19\ \Omega$$

The network is reciprocal (passive, no dependent sources) so $z_{12} = z_{21} = 16\ \Omega$.

$$[z] = \begin{bmatrix} 17.5 & 16 \\ 16 & 19 \end{bmatrix}\ \Omega$$

*Check by admittance addition.* $[y]_{T} = \dfrac{1}{153}\begin{bmatrix}21 & -15\\ -15 & 18\end{bmatrix}$ for the (3, 6, 15) T and the 9 Ω bridge adds $\tfrac19\begin{bmatrix}1&-1\\-1&1\end{bmatrix}$; the sum, inverted, gives exactly the matrix above.

*Conversion to T (ABCD) parameters:* $V_1 = AV_2 - BI_2$, $I_1 = CV_2 - DI_2$.

$$\begin{gathered}A = \frac{z_{11}}{z_{21}} = \frac{17.5}{16} = 1.094 \\ B = \frac{\Delta z}{z_{21}} = \frac{17.5(19) - 16^{2}}{16} = \frac{76.5}{16} = 4.781\ \Omega\end{gathered}$$

$$\begin{gathered}C = \frac{1}{z_{21}} = 0.0625\ \text{S} \\ D = \frac{z_{22}}{z_{21}} = \frac{19}{16} = 1.1875\end{gathered}$$

$$\boxed{\begin{bmatrix}A&B\\C&D\end{bmatrix} = \begin{bmatrix}1.094 & 4.781\ \Omega\\ 0.0625\ \text{S} & 1.1875\end{bmatrix}}$$

Check of reciprocity: $AD - BC = 1.2988 - 0.2988 = 1$.

**(b) Magnetic circuit with a coil on the left limb.**

The flux of the left limb divides at the top and bottom junctions between the centre limb C and the right-hand path (top 25 cm + limb D 15 cm + bottom 25 cm = 65 cm). The coil limb path (E with its two 25 cm horizontal members) is 65 cm long. The magnetic circuit is therefore a series reluctance $S_E$ feeding two parallel paths, $S_C$ and $S_D$.

```figure caption="Equivalent magnetic circuit of Question 3(b): mmf NI drives S_E in series with S_C parallel to S_D."
fig,ax=ckt_canvas(4.6,2.5,xlim=(-1.8,8.2),ylim=(-0.7,3.9))
vsrc(ax,(0,0),(0,3),"NI",side=-1)
res(ax,(0,3),(2.4,3),"S$_E$",side=1)
wire(ax,[(2.4,3),(6,3)]); node(ax,(2.4,3)); node(ax,(6,3))
wire(ax,[(2.4,3),(2.4,2.2)]); res(ax,(2.4,2.2),(2.4,0),"S$_C$",side=-1,body=0.9)
wire(ax,[(6,3),(6,2.2)]); res(ax,(6,2.2),(6,0),"S$_D$",side=1,body=0.9)
wire(ax,[(0,0),(6,0)]); node(ax,(2.4,0))
arrow(ax,(3.1,3.45),(3.9,3.45),"$\\phi$",off=0.2); arrow(ax,(1.65,1.0),(1.65,1.8),"$\\phi_1$",off=-0.28); arrow(ax,(6.55,1.8),(6.55,1.0),"$\\phi_2$",off=0.3)
```

*Data.* $A = 2\times2 = 4\ \text{cm}^2 = 4\times10^{-4}$ m², $\mu = \mu_0\mu_r = 4\pi\times10^{-7}\times600 = 7.54\times10^{-4}$ H/m. Reluctance $S = \dfrac{l}{\mu A}$ with $\dfrac{1}{\mu A} = 3.316\times10^{6}$ per metre.

$$\begin{gathered}S_D = S_E = 0.65\times3.316\times10^{6} = 2.155\times10^{6}\ \text{AT/Wb} \\ S_C = 0.15\times3.316\times10^{6} = 4.974\times10^{5}\ \text{AT/Wb}\end{gathered}$$

*Fluxes.* The two parallel paths have the same mmf drop, $\phi_1S_C = \phi_2S_D$:

$$\begin{gathered}\phi_1 = \phi_2\frac{S_D}{S_C} = 2\times10^{-3}\times\frac{0.65}{0.15} = 8.667\ \text{mWb} \\ \phi = \phi_1 + \phi_2 = 10.667\ \text{mWb}\end{gathered}$$

*Ampere-turns.*

$$NI = \phi S_E + \phi_1S_C = (10.667\times10^{-3})(2.155\times10^{6}) + (8.667\times10^{-3})(4.974\times10^{5}) = 22\,987 + 4\,311 = 27\,299\ \text{AT}$$

$$\boxed{I = \frac{27\,299}{500} = 54.6\ \text{A}}$$

*Note.* The scan gives no B–H curve, only a constant $\mu_r = 600$, so the linear result above is what the question asks for. With a 2 cm × 2 cm section the flux densities ($B_C = 21.7$ T, $B_E = 26.7$ T) are far beyond real cast steel saturation, so a real core would need far more current; the answer is a textbook idealisation. The dimensions were read as: three limbs each 15 cm high, horizontal members 25 cm each.

@s 4
**(a) Why transformer testing is essential, and the O.C. and S.C. tests.**

*Why test.* The losses (iron loss and copper loss), efficiency, voltage regulation and the equivalent-circuit constants ($R_0, X_0, R_{e}, X_{e}$) of a transformer must be known to rate it and to predict its behaviour under load. A direct load test needs a load of the full rating, wastes the full power in the load, and cannot separate core and copper losses. The **open-circuit** and **short-circuit** tests give all of these data accurately from a tiny power input, and also verify the design before it is put in service.

**Open-circuit (no-load) test.** The high-voltage winding is left open; the instruments are put on the **low-voltage** side (small voltage, easier to supply) and rated voltage and frequency are applied.

```figure caption="Equivalent circuits seen in the two tests: the exciting branch (R0 ∥ X0) and the series branch (Re + jXe)."
fig,ax=ckt_canvas(6.0,2.5,xlim=(-1.4,13.4),ylim=(-0.7,3.6))
label(ax,(2.6,3.4),"O.C. test (rated V, I$_0$ small)",size=8)
terminal(ax,(0,3)); terminal(ax,(0,0)); wire(ax,[(0,3),(2,3)]); wire(ax,[(0,0),(5,0)])
res(ax,(2,3),(2,0),"R$_0$",side=1); wire(ax,[(2,3),(4.5,3)]); wire(ax,[(4.5,3),(4.5,2.2)]); ind(ax,(4.5,2.2),(4.5,0),"X$_0$",side=1,body=1.0)
node(ax,(2,3)); node(ax,(2,0)); node(ax,(4.5,3)); 
label(ax,(10.0,3.4),"S.C. test (reduced V, rated I)",size=8)
terminal(ax,(7.5,3)); terminal(ax,(7.5,0)); res(ax,(7.5,3),(9.8,3),"R$_e$",side=1); ind(ax,(9.8,3),(12.3,3),"X$_e$",side=1); wire(ax,[(12.3,3),(12.3,0)]); wire(ax,[(7.5,0),(12.3,0)])
```

*Procedure.* A wattmeter, voltmeter and ammeter are connected in the primary; rated voltage $V_0$ is applied and the readings $W_0$, $I_0$ are recorded. Because $I_0$ is only 2 to 5 percent of full-load current, the copper loss ($I_0^{2}R_1$) is negligible, so

$$W_0 = \text{iron (core) loss } P_i$$

$$\begin{gathered}\cos\phi_0 = \frac{W_0}{V_0I_0},\quad I_w = I_0\cos\phi_0,\quad I_\mu = I_0\sin\phi_0\\ R_0 = \frac{V_0}{I_w},\quad X_0 = \frac{V_0}{I_\mu}\end{gathered}$$

The test gives the **iron loss**, no-load current and power factor and the exciting-branch parameters.

**Short-circuit test.** The low-voltage winding is short-circuited, and the instruments are on the **high-voltage** side (rated current is small there). The applied voltage is raised slowly from zero until the **rated current** $I_{sc}$ flows (this needs only 5 to 10 percent of rated voltage, $V_{sc}$). The flux is then very small, so the iron loss is negligible and

$$\begin{gathered}W_{sc} = I_{sc}^{2}R_{e} = P_{cu}\ (\text{full-load copper loss})\end{gathered}$$

$$\begin{gathered}R_{e} = \frac{W_{sc}}{I_{sc}^{2}} \\ Z_{e} = \frac{V_{sc}}{I_{sc}} \\ X_{e} = \sqrt{Z_{e}^{2} - R_{e}^{2}}\end{gathered}$$

These are referred to the winding on which the instruments are connected. The test gives the **full-load copper loss** and the equivalent resistance and leakage reactance, from which regulation $\dfrac{I R_e\cos\phi \pm I X_e\sin\phi}{V}$ is found.

*Efficiency without loading:* $\eta = \dfrac{x\,S\cos\phi}{x\,S\cos\phi + P_i + x^{2}P_{cu}}$, maximum when $x = \sqrt{P_i/P_{cu}}$.

**(b) Primary current and power factor.**

Voltage drops are neglected, so the load current referred to the primary is

$$I_2' = \frac{N_2}{N_1}I_2 = \frac{1}{4}\times200 = 50\ \text{A at pf } 0.85\ \text{lag}\ (\phi_2 = 31.79^\circ)$$

The no-load current is $I_0 = 10$ A at pf 0.2 lag ($\phi_0 = 78.46^\circ$). The primary current is the phasor sum $\bar I_1 = \bar I_0 + \bar I_2'$ (taking $V_1$ as reference):

$$\begin{gathered}\bar I_2' = 50(0.85 - j0.5268) = 42.5 - j26.34\ \text{A} \\ \bar I_0 = 10(0.2 - j0.9798) = 2 - j9.80\ \text{A}\end{gathered}$$

$$\bar I_1 = 44.5 - j36.14\ \text{A}$$

$$\boxed{I_1 = \sqrt{44.5^{2} + 36.14^{2}} = 57.3\ \text{A},\qquad \phi_1 = \tan^{-1}\frac{36.14}{44.5} = 39.08^\circ,\qquad \cos\phi_1 = 0.776\ \text{lagging}}$$

```figure caption="Phasor diagram of the loaded transformer (referred to the primary): I1 = I0 + I2'."
import numpy as _np
fig,ax=plt.subplots(figsize=(4.8,3.0)); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-6,66); ax.set_ylim(-46,14)
def ar(p,q,c,lw=1.8): ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="-|>",color=c,lw=lw))
ar((0,0),(62,0),INK); ax.text(60,3,"V$_1$",fontsize=10)
I0=(2,-9.8); I2=(42.5,-26.34); I1=(44.5,-36.14)
ar((0,0),I0,"#8a6d3b"); ar(I0,I1,ACCENT); ar((0,0),I2,ACCENT,1.4); ar((0,0),I1,"#d9534f",2.2)
ax.plot([I2[0],I1[0]],[I2[1],I1[1]],ls=":",color="#aaa"); ax.plot([I0[0],I1[0]],[I0[1],I1[1]],ls=":",color="#aaa",lw=0.8)
ax.text(-1,-14,"I$_0$ = 10 A",fontsize=8,ha="right",color="#8a6d3b"); ax.text(46,-24,"I$_2'$ = 50 A (0.85 lag)",fontsize=8,color=ACCENT)
ax.text(46,-43,"I$_1$ = 57.3 A",fontsize=9,color="#d9534f")
from matplotlib.patches import Arc
ax.add_patch(Arc((0,0),26,26,theta1=-39.08,theta2=0,color=INK,lw=0.9)); ax.text(14,-6,"$\\phi_1$",fontsize=8)
ax.add_patch(Arc((0,0),40,40,theta1=-78.46,theta2=0,color="#8a6d3b",lw=0.8)); ax.text(5,-24,"$\\phi_0$",fontsize=8,color="#8a6d3b")
```

@s 5
**(a) Speed of the shunt motor with a series resistance in the field.**

*Initial condition.*

$$\begin{gathered}I_{sh1} = \frac{250}{125} = 2\ \text{A} \\ I_{a1} = 22 - 2 = 20\ \text{A} \\ E_{b1} = 250 - 20(0.5) = 240\ \text{V}\end{gathered}$$

*With 50 Ω added in the field circuit.*

$$\begin{gathered}I_{sh2} = \frac{250}{125 + 50} = 1.4286\ \text{A} \\ \frac{\phi_2}{\phi_1} = \frac{I_{sh2}}{I_{sh1}} = 0.7143\end{gathered}$$

(flux taken proportional to field current, i.e. magnetic circuit unsaturated.)

*Constant load torque.* $T \propto \phi I_a$, so $\phi_1I_{a1} = \phi_2I_{a2}$:

$$\begin{gathered}I_{a2} = I_{a1}\frac{\phi_1}{\phi_2} = 20\times1.4 = 28\ \text{A} \\ E_{b2} = 250 - 28(0.5) = 236\ \text{V}\end{gathered}$$

*Speed.* $E_b \propto \phi N$:

$$\frac{N_2}{N_1} = \frac{E_{b2}}{E_{b1}}\cdot\frac{\phi_1}{\phi_2} = \frac{236}{240}\times1.4 = 1.3767$$

$$\boxed{N_2 = 600\times1.3767 \approx 826\ \text{rpm}}$$

The speed rises because weakening the field reduces $E_b$ per rpm; the armature current rises to 28 A to keep the torque constant (field control of speed above base speed).

**(b) Why a three-phase induction motor is self-starting.**

*Production of a rotating magnetic field.* The stator has three identical windings displaced $120^\circ$ in space, carrying currents $120^\circ$ apart in time, so each winding produces a pulsating (alternating) flux along its own axis:

$$\begin{gathered}\phi_a = \phi_m\sin\omega t \\ \phi_b = \phi_m\sin(\omega t - 120^\circ) \\ \phi_c = \phi_m\sin(\omega t - 240^\circ)\end{gathered}$$

Resolve the three fluxes into the horizontal (x) and vertical (y) directions. Their axes lie at $0^\circ$, $120^\circ$ and $240^\circ$ (phase a along the positive x axis; b and c are $120^\circ$ and $240^\circ$ from it):

$$\begin{gathered}\phi_x = \phi_a + \phi_b\cos120^\circ + \phi_c\cos240^\circ \\ \phi_y = \phi_b\sin120^\circ + \phi_c\sin240^\circ\end{gathered}$$

$$\phi_x = \phi_m\left[\sin\omega t - \tfrac12\sin(\omega t - 120^\circ) - \tfrac12\sin(\omega t - 240^\circ)\right] = 1.5\,\phi_m\sin\omega t$$

$$\phi_y = \frac{\sqrt3}{2}\phi_m\left[\sin(\omega t - 120^\circ) - \sin(\omega t - 240^\circ)\right] = -1.5\,\phi_m\cos\omega t$$

$$\begin{gathered}\phi_r = \sqrt{\phi_x^{2} + \phi_y^{2}} = 1.5\,\phi_m \\ \tan\theta = \frac{\phi_y}{\phi_x} = -\cot\omega t \;\Rightarrow\; \theta = \omega t - 90^\circ\end{gathered}$$

The resultant flux has **constant magnitude** $1.5\phi_m$ and its direction advances by $\omega t$: it rotates at the synchronous speed

$$N_s = \frac{120 f}{P}\ \text{rpm}$$

```figure caption="Three phase currents and the resultant flux at ωt = 0°, 60°, 120° and 180°: constant length 1.5 φm, rotating through the same angle."
import numpy as _np
fig=plt.figure(figsize=(6.2,2.5))
a=fig.add_axes([0.05,0.2,0.42,0.7]); th=_np.linspace(0,2*_np.pi,400)
for k,(c,l) in enumerate(zip(("#d9534f",ACCENT,"#2a9d4a"),("a","b","c"))): a.plot(_np.degrees(th),_np.sin(th-k*2*_np.pi/3),color=c,lw=1.5,label=l)
for d in (0,60,120,180): a.axvline(d,color="#aaa",ls=":",lw=0.8)
a.axhline(0,color=INK,lw=0.6); a.set_xticks([0,60,120,180,240,300,360]); a.tick_params(labelsize=6.5); a.set_yticks([]); a.set_xlabel("$\\omega t$ (degrees)",fontsize=8); a.legend(fontsize=7,ncol=3,loc="upper right",frameon=False)
for sp_ in ("top","right"): a.spines[sp_].set_visible(False)
for i,d in enumerate((0,60,120,180)):
    b=fig.add_axes([0.5+i*0.125,0.25,0.12,0.6]); b.set_aspect("equal"); b.axis("off"); b.set_xlim(-1.8,1.8); b.set_ylim(-1.8,1.8)
    for k in range(3):
        ang=_np.radians(90+k*0 -k*120); 
    w=_np.radians(d); fx=_np.sin(w); fy=-_np.cos(w)
    b.add_patch(__import__("matplotlib.patches",fromlist=["Circle"]).Circle((0,0),1.5,fill=False,ec="#bbb",lw=0.7))
    b.annotate("",xy=(1.5*fx,1.5*fy),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8))
    b.set_title("%d°"%d,fontsize=7.5)
```

*Why it is self-starting.* At standstill the rotor conductors (short-circuited bars or windings) are stationary, while the stator field rotates at $N_s$, so the field cuts them at speed $N_s$. By Faraday's law an emf is induced in the rotor, and since the rotor circuit is closed a rotor current flows. By Lenz's law this current opposes the cause, the relative motion between field and rotor, and the interaction of the rotor current with the stator flux produces a torque (force $F = BIl$ on every conductor) in the **direction of the rotating field**. If this starting torque exceeds the load torque the rotor accelerates. The torque exists at zero speed because the field is already rotating at synchronous speed, in contrast to a single-phase supply that produces only a pulsating field (no net starting torque, so a single-phase induction motor needs a starting winding). The rotor can never reach $N_s$ (slip $s = \dfrac{N_s - N}{N_s}$ would be zero, no emf, no torque), so the motor runs at a slightly smaller speed. Hence a three-phase induction motor is **self-starting**.
