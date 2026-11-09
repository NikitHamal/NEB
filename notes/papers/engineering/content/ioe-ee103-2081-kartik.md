---
file: NEBians-IOE-Past-Paper-Basic-Electrical-and-Electronics-Engineering-EE103-2081-Kartik.pdf
subject: Basic Electrical and Electronics Engineering
level: BE · Year I / Part I
code: EE 103
year_bs: 2081 Kartik
cal: BS
year_ad: 2024
stream: BCE, BCH
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course, 2080 batch). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Calculate the current flowing through $6\ \Omega$ resistor using Nodal analysis. [[6]]

```figure caption="Network of Question 1: a 2 A current source with 12 Ω in parallel feeds the bridge A–B–C–D."
fig,ax=ckt_canvas(5.6,3.2,xlim=(-1.3,9.3),ylim=(-0.5,3.8))
isrc(ax,(0,0),(0,3.2),"2 A",side=1)
wire(ax,[(0,3.2),(6,3.2)]); wire(ax,[(0,0),(6,0)])
res(ax,(2.2,3.2),(2.2,0),"12 Ω",side=-1)
A=(6,3.2); B=(8,1.6); C=(6,0); D=(4,1.6)
res(ax,A,D,"8 Ω",side=-1,off=0.5); res(ax,A,B,"4 Ω",side=1,off=0.5)
res(ax,D,B,"6 Ω",side=1,off=0.4)
res(ax,D,C,"20 Ω",side=-1,off=0.55); res(ax,B,C,"10 Ω",side=1,off=0.55)
for p in (A,B,C,D,(2.2,3.2),(2.2,0)): node(ax,p)
label(ax,(6,3.55),"A"); label(ax,(8.35,1.6),"B"); label(ax,(6,-0.35),"C"); label(ax,(3.65,1.6),"D")
```

@q 2
Explain the generation of AC voltage. A coil having a resistance of $5\ \Omega$ and inductance of $30$ mH in series are connected across a $230$ V, $50$ Hz supply. Calculate current, power factor, and power consumed. [[3+3]]

@q 3
What are the advantages of three phase supply system over single-phase system. Three identical coils, each having resistance of $20\ \Omega$ and inductance of $0.08$ H are connected in delta across a three-phase, $415$ V, $50$ Hz supply. Calculate: i) The phase current, ii) The line current, iii) The total power consumed, and iv) power factor. [[2+4]]

@q 4
A $300$ kVA single phase transformer has iron losses of $1.8$ kW. The full load copper losses is $2500$ watts. Calculate, [[6]]
(i) Efficiency at full load, $0.8$ lagging pf
(ii) kVA supplied at maximum Efficiency
(iii) Maximum Efficiency at $0.8$ lagging pf

@q 5
Derive the condition for maximum torque in an induction motor. Describe the torque slip characteristics of a three-phase induction motor. [[3+3]]

@q 6
Explain working principle of a synchronous generator. A 4 pole $230$ V dc shunt motor, lap wound has $980$ conductors. The flux per pole is $20$ mWb. Determine the torque developed by the armature in Nm when the current drawn by the motor is $26$ A. The armature resistance is $0.12\ \Omega$ and the field resistance is $130\ \Omega$. [[2+4]]

@q 7
Define and explain reverse breakdown effect. Describe how Zener diode works as a voltage regulator. [[3+3]]

@q 8
Define biasing. Find $R_C$ and $R_B$ in the given circuit. Given data are: $I_C = 1.2$ mA, $V_{CE} = 6$ V, and $\beta = 100$ [[6]]

```figure caption="Question 8: the base resistor R$_B$ is connected from the collector to the base (V$_{CC}$ = +12 V, β = 100)."
fig,ax=ckt_canvas(5.0,3.4,xlim=(-1.6,6.6),ylim=(-1.6,4.2))
bj=bjt(ax,2.4,1.0)
B,C,E=bj["B"],bj["C"],bj["E"]
wire(ax,[C,(C[0],2.9)]); res(ax,(C[0],3.9),(C[0],2.9),"R$_C$",side=1,body=0.9)
label(ax,(C[0],4.15),"+V$_{CC}$ = 12 V",size=8.4)
wire(ax,[E,(E[0],-0.6)]); gnd(ax,(E[0],-0.6))
wire(ax,[(C[0],2.2),(0.6,2.2)]); res(ax,(0.6,2.2),(0.6,1.0),"R$_B$",side=1,body=0.8)
wire(ax,[(0.6,1.0),B]); node(ax,(0.6,1.0)); node(ax,(C[0],2.2))
cap(ax,(-1.4,1.0),(0.6,1.0),"10 μF",side=1,off=0.5)
terminal(ax,(-1.4,1.0)); label(ax,(-1.4,0.55),"v$_i$",size=8.4)
cap(ax,(C[0],2.2),(5.8,2.2),"10 μF",side=1,off=0.5); terminal(ax,(5.8,2.2)); label(ax,(5.8,1.8),"v$_o$",size=8.4)
```

@q 9
Explain different types of wiring used in households and explain the process to determine the size of the wire. [[3+3]]

@q 10
Write short notes on (Any Two): [[3×2]]
a) Electrical Safety Rules
b) Boolean Algebra
c) Protective Device and their sizing
<!-- SOLUTIONS -->

@s 1
**Observation.** The 12 Ω resistor is in parallel with the source and the bridge; the current source and the 12 Ω together only set the voltage across terminals A–C. Nodes: A, B, D; take C as the reference node ($V_C = 0$). Write KCL at A, D and B (currents leaving a node through the resistors = current entering).

*Node A* (2 A is injected, the 12 Ω goes to C):

$$2 = \frac{V_A}{12} + \frac{V_A - V_D}{8} + \frac{V_A - V_B}{4}$$

*Node D*:

$$\frac{V_A - V_D}{8} = \frac{V_D}{20} + \frac{V_D - V_B}{6}$$

*Node B*:

$$\frac{V_A - V_B}{4} + \frac{V_D - V_B}{6} = \frac{V_B}{10}$$

Clear the denominators (multiply by 120, 120 and 60 respectively):

$$\begin{gathered} 55V_A - 15V_D - 30V_B = 240 \\ 15V_A - 41V_D + 20V_B = 0 \\ 15V_A + 10V_D - 31V_B = 0 \end{gathered}$$

Solving (for example by Cramer's rule or elimination):

$$\boxed{V_A = 10.5\ \text{V},\qquad V_D = 7.5\ \text{V},\qquad V_B = 7.5\ \text{V}}$$

**Current in the 6 Ω resistor** (between D and B):

$$I_{6\Omega} = \frac{V_D - V_B}{6} = \frac{7.5 - 7.5}{6} = \mathbf{0\ A}$$

**Why zero?** The bridge is *balanced*: $\dfrac{R_{AD}}{R_{DC}} = \dfrac{8}{20} = 0.4 = \dfrac{4}{10} = \dfrac{R_{AB}}{R_{BC}}$. Points D and B are therefore at the same potential, so no current flows in the 6 Ω arm, whatever its value, and it can be removed.

*Check by equivalent resistance.* $(8 + 20)\parallel(4 + 10) = 28\parallel14 = 9.33\ \Omega$, then $12\parallel9.33 = 5.25\ \Omega$, so $V_A = 2 \times 5.25 = 10.5$ V ✓. The bridge currents are $10.5/28 = 0.375$ A through 8 Ω and 20 Ω, and $10.5/14 = 0.75$ A through 4 Ω and 10 Ω; check: $V_D = 0.375 \times 20 = 7.5$ V ✓.

@s 2
**Generation of AC voltage.** Faraday's law: an emf is induced in a conductor when it cuts magnetic flux. Take a rectangular coil of $N$ turns, area $A$, rotating at constant angular speed $\omega$ in a uniform magnetic field $B$. When its plane makes angle $\theta = \omega t$ with the neutral position, the flux linked is $\phi = BA\cos\omega t$, so

$$\begin{gathered}e = -N\frac{d\phi}{dt} = NBA\omega\sin\omega t = E_m\sin\omega t \\ E_m = NBA\omega\end{gathered}$$

The emf is zero when the coil sides move parallel to the field (neutral position), maximum when they cut the field at right angles, and reverses each half revolution. The ends of the coil are taken out through two slip rings and brushes, so the output is a sinusoidal AC voltage with frequency $f = \omega/2\pi$. In power stations the field magnet rotates inside a stationary armature (alternator), and $f = PN/120$.

```figure caption="One revolution of the coil gives one cycle of the sinusoidal emf e = E$_m$ sin ωt."
import numpy as np, matplotlib.pyplot as plt
t=np.linspace(0,2*np.pi,400)
fig,ax=plt.subplots(figsize=(5.2,2.3))
ax.plot(t,np.sin(t),color=ACCENT); ax.axhline(0,color=INK,lw=0.7)
ax.set_xticks([0,np.pi/2,np.pi,3*np.pi/2,2*np.pi]); ax.set_xticklabels(["0","π/2","π","3π/2","2π"])
ax.set_xlabel("coil angle ωt"); ax.set_ylabel("e / E$_m$")
for x,txt in ((0,"neutral"),(np.pi/2,"max"),(np.pi,"neutral"),(3*np.pi/2,"max (reversed)")): ax.annotate(txt,(x,np.sin(x)),xytext=(x,np.sin(x)+(0.25 if np.sin(x)>=0 else -0.35)),ha='center',fontsize=7.2,color=MUTED)
ax.set_ylim(-1.5,1.5)
```

**Coil on 230 V, 50 Hz** ($R = 5\ \Omega$, $L = 30$ mH):

$$X_L = 2\pi fL = 2\pi \times 50 \times 0.03 = 9.425\ \Omega$$

$$Z = \sqrt{R^2 + X_L^2} = \sqrt{25 + 88.83} = 10.67\ \Omega$$

$$\boxed{I = \frac{V}{Z} = \frac{230}{10.67} = 21.56\ \text{A}}$$

$$\boxed{\cos\varphi = \frac{R}{Z} = \frac{5}{10.67} = 0.469\ \text{lagging}}\quad(\varphi = 62.05^\circ)$$

$$\boxed{P = I^2R = 21.56^2 \times 5 = 2324\ \text{W}}\quad(= VI\cos\varphi = 230 \times 21.56 \times 0.4686)$$

(The reactive power is $Q = I^2X_L = 4380$ var and the apparent power $S = 4958$ VA.)

@s 3
**Advantages of a three-phase system over single phase.**

1. For the same size, a three-phase generator and motor give about 1.5 times the output (power rating) of a single-phase machine.
2. The conductor material needed for a transmission line is only about 75% of that of an equivalent single-phase line (3-wire against 2-wire, for the same power and loss), so it is cheaper.
3. The instantaneous power of a balanced load is **constant**, not pulsating, so three-phase motors run smoothly with a constant torque.
4. A three-phase induction motor is self-starting, with a rotating magnetic field, and needs no starting device. A single-phase motor does not.
5. Two voltage levels are available (line and phase, 400/230 V), so both single-phase and three-phase loads can be supplied.
6. Better voltage regulation and higher efficiency; the power factor of a three-phase motor is higher, and the power can be transmitted over long distances economically.

**Delta-connected coils** ($R = 20\ \Omega$, $L = 0.08$ H, $V_L = 415$ V, 50 Hz). In a delta, $V_{ph} = V_L = 415$ V.

$$\begin{gathered}X_L = 2\pi \times 50 \times 0.08 = 25.13\ \Omega \\ Z_{ph} = \sqrt{20^2 + 25.13^2} = 32.12\ \Omega \\ \varphi = \tan^{-1}\frac{25.13}{20} = 51.49^\circ\end{gathered}$$

**(i) Phase current:**

$$I_{ph} = \frac{V_{ph}}{Z_{ph}} = \frac{415}{32.12} = \mathbf{12.92\ A}$$

**(ii) Line current:**

$$I_L = \sqrt3\,I_{ph} = \sqrt3 \times 12.92 = \mathbf{22.38\ A}$$

**(iii) Total power consumed:**

$$P = 3I_{ph}^2R = 3 \times 12.92^2 \times 20 = \mathbf{10\,016\ W} \approx 10.0\ \text{kW}$$

(Check: $\sqrt3 V_LI_L\cos\varphi = \sqrt3 \times 415 \times 22.38 \times 0.6227 = 10.02$ kW ✓.)

**(iv) Power factor:**

$$\cos\varphi = \frac{R}{Z_{ph}} = \frac{20}{32.12} = \mathbf{0.623\ lagging}$$

The reactive power is $Q = 3I_{ph}^2X_L = 12.59$ kvar and the apparent power is $S = 16.09$ kVA.

@s 4
Given: $S = 300$ kVA, $P_i = 1.8$ kW, full-load copper loss $P_{cu} = 2.5$ kW, $\cos\varphi = 0.8$ lagging.

**(i) Efficiency at full load, 0.8 lagging.**

$$\begin{gathered}\text{output} = 300 \times 0.8 = 240\ \text{kW} \\ \text{total loss} = 1.8 + 2.5 = 4.3\ \text{kW}\end{gathered}$$

$$\eta = \frac{240}{240 + 4.3} \times 100 = \mathbf{98.24\%}$$

**(ii) kVA supplied at maximum efficiency.** Maximum efficiency occurs when the copper loss equals the iron loss, $x^2P_{cu} = P_i$:

$$x = \sqrt{\frac{P_i}{P_{cu}}} = \sqrt{\frac{1.8}{2.5}} = 0.8485$$

$$\text{kVA at } \eta_{max} = x \times 300 = 0.8485 \times 300 = \mathbf{254.6\ kVA}$$

**(iii) Maximum efficiency at 0.8 lagging.**

$$\begin{gathered}\text{output} = 254.56 \times 0.8 = 203.65\ \text{kW} \\ \text{losses} = 2P_i = 3.6\ \text{kW}\end{gathered}$$

$$\eta_{max} = \frac{203.65}{203.65 + 3.6} \times 100 = \mathbf{98.26\%}$$

The maximum efficiency (98.26%) is only slightly larger than the full-load value (98.24%).

@s 5
**Torque equation.** In a three-phase induction motor, with $E_2$ the rotor emf per phase at standstill, $R_2$ and $X_2$ the rotor resistance and standstill leakage reactance per phase, and $s$ the slip, the rotor at slip $s$ has emf $sE_2$ and reactance $sX_2$:

$$\begin{gathered}I_2 = \frac{sE_2}{\sqrt{R_2^2 + (sX_2)^2}} \\ \cos\varphi_2 = \frac{R_2}{\sqrt{R_2^2 + (sX_2)^2}}\end{gathered}$$

The torque is proportional to $\Phi I_2\cos\varphi_2$, and $\Phi \propto E_2$, so (from the rotor power input $P_2 = 3I_2^2R_2/s$ and $T = P_2/\omega_s$):

$$T = \frac{3}{\omega_s}\cdot\frac{sE_2^2R_2}{R_2^2 + s^2X_2^2}$$

**Condition for maximum torque.** Differentiate with respect to $s$ and set to zero:

$$\frac{dT}{ds} \propto \frac{(R_2^2 + s^2X_2^2) - s(2sX_2^2)}{(R_2^2 + s^2X_2^2)^2} = 0 \ \Rightarrow\ R_2^2 - s^2X_2^2 = 0$$

$$\boxed{s_m = \frac{R_2}{X_2}}\quad\text{i.e. } R_2 = s_mX_2\ (\text{rotor resistance} = \text{rotor reactance at that slip})$$

$$T_{max} = \frac{3}{\omega_s}\cdot\frac{E_2^2}{2X_2}$$

$T_{max}$ is **independent of the rotor resistance**; $R_2$ only decides at what slip (speed) it occurs. Dividing the torque by $T_{max}$:

$$\frac{T}{T_{max}} = \frac{2s\,s_m}{s^2 + s_m^2}$$

Starting torque ($s = 1$): $T_{st} = \dfrac{3}{\omega_s}\dfrac{E_2^2R_2}{R_2^2 + X_2^2}$, and it equals $T_{max}$ when $R_2 = X_2$.

**Torque-slip characteristic.**

```figure caption="Torque-slip characteristic of a three-phase induction motor for three values of rotor resistance (s$_m$ = R$_2$/X$_2$). Raising R$_2$ moves the peak towards s = 1 but does not change T$_{max}$."
import numpy as np, matplotlib.pyplot as plt
s=np.linspace(0.001,1,500)
fig,ax=plt.subplots(figsize=(5.3,2.8))
for sm,c,l in ((0.15,ACCENT,"R$_2$ small (s$_m$ = 0.15)"),(0.5,SERIES[1],"R$_2$ medium (s$_m$ = 0.5)"),(1.0,SERIES[2],"R$_2$ = X$_2$ (s$_m$ = 1)")):
    ax.plot(s,2*s*sm/(s**2+sm**2),color=c,label=l)
ax.axvspan(0,0.15,color="#eaf1ff",alpha=0.7); ax.text(0.015,0.08,"normal\nrunning",fontsize=7,color=MUTED)
ax.set_xlabel("slip s  (s = 1 standstill  →  s = 0 synchronous speed)"); ax.set_ylabel("T / T$_{max}$"); ax.legend(loc="center right",fontsize=7.2)
ax.set_ylim(0,1.12)
```

*Description.*

- At synchronous speed ($s = 0$) the torque is zero: there is no relative motion, so no rotor emf or current.
- For small slip ($0 < s < s_m$, the **stable** region, normal operating range with $s \approx 2$–$5\%$ at full load), $sX_2 \ll R_2$ and $T \propto s$: the characteristic is nearly a straight line. A rise in load slows the motor (larger $s$), and the torque grows, so a new equilibrium is reached.
- At $s = s_m$ the torque is maximum, the **breakdown (pull-out) torque** (typically 2–3 times the full-load torque). Loading beyond this stalls the motor.
- For $s_m < s < 1$ (**unstable** region) $sX_2 \gg R_2$ and $T \propto 1/s$: the torque falls as slip rises, so the motor cannot run steadily here and will decelerate to a stop if the load torque exceeds the available torque.
- At $s = 1$ (standstill) the motor develops the **starting torque** $T_{st}$. In a slip-ring motor, adding external rotor resistance at start moves the peak towards $s = 1$ and raises $T_{st}$ (up to $T_{max}$ when $R_2 = X_2$).

@s 6
**Working principle of a synchronous generator (alternator).** It works on Faraday's law of electromagnetic induction. The rotor carries a field winding fed with DC (through slip rings), so it forms alternate N and S poles. A prime mover (turbine) rotates the rotor at the constant synchronous speed $N_s$. The rotating field flux cuts the stationary three-phase armature conductors placed in the stator slots, and an emf is induced in each phase. The three phase windings are displaced by $120^\circ$ in space, so the three emfs are displaced by $120^\circ$ in time.

$$\begin{gathered}f = \frac{PN_s}{120} \\ E_{ph} = 4.44\,K_pK_d\,f\,\Phi\,T_{ph}\ \text{volt}\end{gathered}$$

It is called *synchronous* because the speed is rigidly tied to the frequency: a 4-pole machine at 1500 rpm gives 50 Hz, a 2-pole at 3000 rpm, a 20-pole hydro machine at 300 rpm. The field excitation controls the terminal voltage and reactive power; the mechanical input controls the active power.

```figure caption="Three-phase emfs of an alternator: equal in magnitude and displaced by 120° (phase sequence R, Y, B)."
import numpy as np, matplotlib.pyplot as plt
t=np.linspace(0,2*np.pi,400)
fig,ax=plt.subplots(figsize=(5.2,2.3))
for k,(c,n) in enumerate(((ACCENT,"e$_R$"),(SERIES[3],"e$_Y$"),(SERIES[1],"e$_B$"))):
    ax.plot(t,np.sin(t-k*2*np.pi/3),color=c,label=n)
ax.axhline(0,color=INK,lw=0.6); ax.set_xticks([0,np.pi,2*np.pi]); ax.set_xticklabels(["0","π","2π"]); ax.set_xlabel("ωt"); ax.set_ylabel("e / E$_m$"); ax.legend(ncol=3,loc="upper right",fontsize=7.2)
ax.set_ylim(-1.2,1.5)
```

**DC shunt motor.** Given $V = 230$ V, $P = 4$ poles, lap winding ($A = P = 4$), $Z = 980$, $\Phi = 20$ mWb, $I_L = 26$ A, $R_a = 0.12\ \Omega$, $R_{sh} = 130\ \Omega$.

*Field (shunt) current:*

$$I_{sh} = \frac{V}{R_{sh}} = \frac{230}{130} = 1.769\ \text{A}$$

*Armature current:*

$$I_a = I_L - I_{sh} = 26 - 1.769 = 24.23\ \text{A}$$

*Back emf:*

$$E_b = V - I_aR_a = 230 - 24.23 \times 0.12 = 227.09\ \text{V}$$

*Torque developed by the armature:*

$$T_a = \frac{P\Phi Z I_a}{2\pi A} = \frac{4 \times 0.02 \times 980 \times 24.23}{2\pi \times 4} = \frac{1899.6}{25.13}$$

$$\boxed{T_a = 75.6\ \text{N\,m}}$$

*Check.* The speed is $N = \dfrac{60AE_b}{P\Phi Z} = \dfrac{60 \times 4 \times 227.09}{4 \times 0.02 \times 980} = 695\ \text{rpm}$ ($\omega = 72.8$ rad/s). The developed power is $E_bI_a = 227.09 \times 24.23 = 5502$ W, and $T_a\omega = 75.59 \times 72.8 = 5502$ W ✓.

@s 7
**Reverse breakdown.** A p–n junction diode under reverse bias passes only a very small reverse saturation current (leakage). If the reverse voltage is increased beyond a critical value, the **breakdown voltage** $V_{BR}$, the reverse current suddenly rises sharply while the voltage across the diode stays almost constant. This is the *reverse breakdown effect*. It is not destructive in itself; damage occurs only if the power $V_{BR}I_R$ exceeds the rating, so the current must be limited by an external resistor. Two mechanisms are responsible:

1. *Avalanche breakdown* (usually $V_{BR} > 6$ V; lightly doped, wide depletion layer). Minority carriers accelerated by the strong field gain enough energy to knock out more electron-hole pairs on collision. The new carriers do the same, so there is a multiplication ("avalanche") of carriers.
2. *Zener breakdown* ($V_{BR} < 5$ V; heavily doped, very thin depletion layer, $<10$ nm). The electric field in the thin layer is so intense ($\sim 10^7$ V/m) that it pulls electrons directly out of covalent bonds (field ionisation). The Zener diode is designed to operate in this region.

```figure caption="V–I characteristic of a Zener diode. In reverse breakdown the voltage stays near V$_Z$ over a wide range of current (I$_{Zmin}$ to I$_{Zmax}$)."
import numpy as np, matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(5.0,2.9))
v=np.linspace(-6.0,0.8,900)
fwd=0.0015*(np.exp(np.clip(v,0,None)/0.085)-1)
rev=-0.04-0.05*(np.exp(np.clip(-v-5.0,0,None)/0.17)-1)*(v<-5.0)*1.0
i=np.where(v>=0,fwd,np.where(v>-5.0,-0.04*(1-np.exp(v/0.0001))*0+(-0.04),rev))
i=np.clip(i,-1.0,1.0); m=(v>-6.0)
ax.plot(v[m],i[m],color=ACCENT)
ax.axhline(0,color=INK,lw=0.7); ax.axvline(0,color=INK,lw=0.7)
ax.set_xlim(-6.4,1.3); ax.set_ylim(-1.1,1.05); ax.set_xticks([-5,0]); ax.set_xticklabels(["−V$_Z$","0"]); ax.set_yticks([])
ax.text(-4.9,-0.62,"breakdown: V ≈ V$_Z$,\nI rises sharply",fontsize=7.4,color=SERIES[1]); ax.text(0.15,0.55,"forward",fontsize=7.4,color=MUTED)
ax.text(-3.4,0.1,"reverse leakage (tiny)",fontsize=7.2,color=MUTED); ax.set_xlabel("diode voltage V$_D$"); ax.set_ylabel("current I$_D$")
```

**Zener diode as a voltage regulator.** The Zener diode is connected in **reverse** across the load, in parallel with it, with a series resistor $R_s$ between the unregulated supply $V_{in}$ and the combination.

```figure caption="Zener shunt voltage regulator: the Zener holds the load voltage at V$_Z$ when V$_{in}$ or the load current changes."
fig,ax=ckt_canvas(5.0,2.7,xlim=(-1.8,7.4),ylim=(-0.6,3.1))
batt(ax,(0,0.5),(0,1.7),"V$_{in}$",side=1)
wire(ax,[(0,1.7),(0,2.4)]); wire(ax,[(0,0.5),(0,0),(6,0)])
res(ax,(0,2.4),(2.8,2.4),"R$_s$"); wire(ax,[(2.8,2.4),(6,2.4)])
diode(ax,(2.8,0),(2.8,2.4),"Zener",side=-1,zener=True,off=0.7)
res(ax,(6,2.4),(6,0),"R$_L$",side=1); node(ax,(2.8,2.4)); node(ax,(2.8,0))
arrow(ax,(1.5,2.75),(2.3,2.75),"I$_s$",off=0.2); arrow(ax,(3.15,1.7),(3.15,1.0),"I$_Z$",off=-0.28); arrow(ax,(5.5,2.75),(6.1,2.75),"I$_L$",off=0.2)
label(ax,(5.2,1.2),"V$_o$ = V$_Z$",ha="right")
```

*Action.* While $V_{in}$ is above $V_Z$, the Zener is in breakdown and $V_o = V_Z$, constant:

$$\begin{gathered}I_s = \frac{V_{in} - V_Z}{R_s} = I_Z + I_L \\ V_o = V_Z\end{gathered}$$

- *Line regulation:* if $V_{in}$ rises, $I_s$ rises, the extra current flows through the Zener (its voltage hardly changes, only $I_Z$ rises) and the extra drop appears across $R_s$. The output stays at $V_Z$. If $V_{in}$ falls, $I_Z$ falls, with the same result.
- *Load regulation:* if $I_L$ rises, $I_Z$ falls by the same amount, since $I_s = I_Z + I_L$ is nearly constant. If $I_L$ falls, $I_Z$ rises.
- *Design limits:* $I_Z$ must stay between $I_{Zmin}$ (knee current) and $I_{Zmax} = P_{ZM}/V_Z$, so $\dfrac{V_{in,max} - V_Z}{I_{Zmax} + I_{L,min}} \le R_s \le \dfrac{V_{in,min} - V_Z}{I_{Zmin} + I_{L,max}}$.

@s 8
**Biasing.** Biasing is the application of suitable DC voltages and currents to a transistor so that it is set to a fixed *quiescent (operating) point Q* $(I_{CQ}, V_{CEQ})$ in the active region. Then, when the small AC signal is applied, the transistor amplifies it faithfully, without cut-off or saturation distortion, and the operating point is kept stable against temperature and $\beta$ variation.

**Circuit.** $R_B$ joins the **collector to the base** (collector-feedback bias). Given $I_C = 1.2$ mA, $V_{CE} = 6$ V, $\beta = 100$, $V_{CC} = 12$ V (take $V_{BE} = 0.7$ V for silicon).

$$\begin{gathered}I_B = \frac{I_C}{\beta} = \frac{1.2\ \text{mA}}{100} = 12\ \mu\text{A} \\ I_E = I_C + I_B = 1.212\ \text{mA}\end{gathered}$$

*Collector loop.* Both $I_C$ and $I_B$ flow through $R_C$:

$$V_{CC} = (I_C + I_B)R_C + V_{CE}$$

$$R_C = \frac{12 - 6}{1.212\times10^{-3}} = 4950\ \Omega \approx \mathbf{4.95\ k\Omega}\ (\approx 5\ \text{k}\Omega\text{ if } I_B \text{ is neglected})$$

*Base loop.* $V_{CE} = I_BR_B + V_{BE}$:

$$R_B = \frac{V_{CE} - V_{BE}}{I_B} = \frac{6 - 0.7}{12\times10^{-6}} = 441.7\ \text{k}\Omega \approx \mathbf{442\ k\Omega}$$

$$\boxed{R_C \approx 4.95\ \text{k}\Omega\ (5\ \text{k}\Omega),\qquad R_B \approx 442\ \text{k}\Omega}$$

*Remark.* The feedback gives self-stabilisation: if $I_C$ increases, $V_C$ falls, so $I_B$ falls and brings $I_C$ back. Capacitors (10 μF) couple the AC input and output while blocking DC. If a *fixed-bias* reading were intended ($R_B$ from $V_{CC}$ to base), $R_B = (12 - 0.7)/12\ \mu\text{A} = 942\ \text{k}\Omega$ and $R_C = (12 - 6)/1.2\ \text{mA} = 5\ \text{k}\Omega$.

@s 9
**Types of wiring in households.**

| Type | Description | Merits / demerits |
|---|---|---|
| **Cleat wiring** | PVC/VIR cables held by porcelain or plastic cleats on walls and ceilings | Cheapest and easiest to inspect; temporary use only; exposed and unsafe, poor appearance |
| **Casing-capping** | Cables laid in grooves of a wooden/PVC casing, covered by a capping | Cheaper than conduit, neat; risk of fire, damp and termites for wood; used in old houses |
| **Batten wiring** | Cables clipped on wooden battens fixed to the wall | Cheap and simple; poor appearance and life; not for damp places |
| **Conduit wiring (surface or concealed)** | Cables drawn through PVC or GI pipes fixed on the surface or buried in the wall plaster | Safest and the standard modern wiring: protection against mechanical damage, moisture and fire, long life, neat; costly, and costly to modify after plastering |
| **Lead-sheathed / TRS (CTS)** | Cables with a metal or tough-rubber sheath clipped to the wall | Moisture- and damage-proof; costly, so seldom used now |

In a house the *distribution* may be of the **loop-in (looping)** or the **joint-box (tree)** system, with separate final sub-circuits for light/fan (5 A, 1.5 mm²), power sockets (15/16 A, 2.5 mm²) and heavy loads (geyser, AC), each protected by an MCB, with a common main distribution board with a double-pole main switch/RCCB.

**Process to determine the size of the wire (cable).**

1. *List the connected load* on the circuit and find the maximum demand (apply a diversity factor): $P = \sum P_i \times$ diversity factor.
2. *Calculate the full-load current:* single-phase $I_B = \dfrac{P}{V\cos\varphi}$; three-phase $I_B = \dfrac{P}{\sqrt3 V_L\cos\varphi}$.
3. *Choose the protective device rating* $I_n \ge I_B$ and select the wire so that its **current-carrying capacity** (ampacity) $I_z \ge I_n$, after applying the de-rating factors for ambient temperature, grouping of cables and the installation method (conduit, buried, etc.). Allow 20–25% spare capacity for future loads.
4. *Check the voltage drop:* $V_d = \dfrac{2IL\rho}{A}$ (single-phase, $L$ is the length one way, $\rho_{Cu} = 0.0175\ \Omega\,\text{mm}^2/\text{m}$); it must be within about 3% for lighting and 5% overall of the supply voltage. If it is exceeded, take the next larger size.
5. *Check short-circuit withstand:* $I_{sc}^2t \le k^2A^2$ ($k = 115$ for PVC copper).
6. *Select the standard size* ($1.5, 2.5, 4, 6, 10, 16\ \text{mm}^2$...) and the insulation type.

*Typical copper PVC-insulated capacities in conduit:* $1.5\ \text{mm}^2$: 13–17 A; $2.5\ \text{mm}^2$: 18–24 A; $4\ \text{mm}^2$: 24–32 A; $6\ \text{mm}^2$: 31–41 A; $10\ \text{mm}^2$: 42–57 A (depends on the standard and installation).

*Worked example.* A 2.5 kW water heater on 230 V, $\cos\varphi = 1$, 20 m from the board: $I_B = 2500/230 = 10.9$ A, so the MCB is 16 A and $2.5\ \text{mm}^2$ copper is chosen (capacity about 18–24 A $\ge$ 16 A). Voltage drop $= 2 \times 10.9 \times 20 \times 0.0175/2.5 = 3.05$ V, i.e. $1.3\% < 3\%$ ✓.

@s 10
Any two are required; all three are answered.

**(a) Electrical safety rules.**

1. Switch **off** the main supply and verify with a tester before working on any circuit; put a "man at work" tag and lock the switch.
2. Use properly rated, ISI/IEC-approved wires, switches, plugs and **MCB/RCCB**; never replace a fuse with a thicker wire.
3. Every metal body (fridge, washing machine, geyser, switchboard) must be **earthed**; use 3-pin plugs with the earth pin.
4. Switches and fuses are fitted in the **phase (live)** wire only; the neutral and the earth must not be switched/fused separately.
5. Do not overload sockets with multi-plug adaptors; avoid joints in wires, and insulate all joints with proper connectors.
6. Keep electrical equipment away from water; do not touch switches with wet hands; use waterproof fittings in the bathroom/kitchen.
7. Use rubber-soled shoes, insulated tools, rubber gloves and a ladder made of insulating material when working.
8. Never touch a person in contact with a live conductor: switch off, or push the person away with a dry wooden/plastic object. Give artificial respiration and call for medical help.
9. Fire from electrical causes must be put out with a CO₂ or dry powder extinguisher, **never water**, after switching off the supply.
10. Inspect and test the wiring and the earth resistance periodically and keep overhead lines clear of buildings and trees.

**(b) Boolean algebra.** Boolean algebra (George Boole) deals with variables that take only the values 0 and 1, and the operations AND ($\cdot$), OR ($+$) and NOT ($\bar{\ }$). It is the mathematical basis of digital logic design: any logic circuit can be written as a Boolean expression and simplified to reduce the number of gates.

| Law | AND form | OR form |
|---|---|---|
| Identity | $A\cdot1 = A$ | $A + 0 = A$ |
| Null (domination) | $A\cdot0 = 0$ | $A + 1 = 1$ |
| Idempotent | $A\cdot A = A$ | $A + A = A$ |
| Complement | $A\cdot\bar A = 0$ | $A + \bar A = 1$ |
| Involution | $\bar{\bar A} = A$ | |
| Commutative | $AB = BA$ | $A + B = B + A$ |
| Associative | $(AB)C = A(BC)$ | $(A+B)+C = A+(B+C)$ |
| Distributive | $A(B + C) = AB + AC$ | $A + BC = (A+B)(A+C)$ |
| Absorption | $A(A + B) = A$ | $A + AB = A$ |
| De Morgan's | $\overline{A\cdot B} = \bar A + \bar B$ | $\overline{A + B} = \bar A\cdot\bar B$ |

*Example.* Simplify $Y = AB + A\bar B + \bar AB$:

$$Y = A(B + \bar B) + \bar AB = A + \bar AB = (A + \bar A)(A + B) = A + B$$

so one OR gate replaces three AND gates, one OR gate and two NOT gates. (By *duality*, interchanging AND with OR and 0 with 1 in a valid identity gives another valid identity.)

**(c) Protective devices and their sizing.** Protective devices disconnect a circuit automatically when an abnormal condition (overload, short circuit, earth leakage, over/under voltage, surge) arises, protecting the wiring, the appliances and people.

| Device | Protects against | Operating principle |
|---|---|---|
| Fuse (rewirable, HRC cartridge) | overload and short circuit | fusible element melts |
| MCB | overload and short circuit | bimetal (thermal) + solenoid (magnetic); characteristics B, C, D |
| MCCB | larger overload and short-circuit currents (up to 1600 A) | adjustable thermal-magnetic trips |
| RCCB / ELCB / RCD | earth leakage (shock), 30 mA for people | difference of phase and neutral currents $\ne$ 0 trips the relay |
| Surge protective device (SPD), lightning arrester | transient overvoltages | metal-oxide varistor |
| Overload relay, voltage relays | motor overload, under/over voltage | thermal element / electronic |

*Sizing rules (IEC 60364):* the device rating $I_n$ and the cable capacity $I_z$ must satisfy

$$\begin{gathered}I_B \le I_n \le I_z \\ I_2 \le 1.45\,I_z\end{gathered}$$

where $I_B$ is the design current and $I_2$ the current that makes the device operate (conventional tripping current). The *breaking capacity* must exceed the prospective short-circuit current at that point (6 kA/10 kA for household MCBs). The *curve* is chosen by the load: B (3–5 $I_n$) for lighting and resistive loads; C (5–10 $I_n$) for general loads and small motors; D (10–20 $I_n$) for transformers and heavy motors. The RCCB is rated 25/40 A (equal to or above the circuit MCB) with sensitivity 30 mA.

*Examples.* A 1.5 kW heater on 230 V: $I_B = 6.5$ A, so a 10 A MCB with 1.5 mm² wire. A 2 kW geyser: $I_B = 8.7$ A, so a 10 A MCB (B curve), 2.5 mm² wire. A 1.5-ton air conditioner (1.8 kW, $\cos\varphi = 0.85$): $I_B = 9.2$ A, so a 16 A, C-curve MCB, which tolerates the compressor starting surge.

