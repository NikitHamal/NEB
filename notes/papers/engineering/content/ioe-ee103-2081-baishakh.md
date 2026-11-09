---
file: NEBians-IOE-Past-Paper-Basic-Electrical-and-Electronics-Engineering-EE103-2081-Baishakh.pdf
subject: Basic Electrical and Electronics Engineering
level: BE · Year I / Part I
code: EE 103
year_bs: 2081 Baishakh
cal: BS
year_ad: 2024
stream: BCE, BCH
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course, 2080 batch). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Define RMS and Average value of AC quantities. Determine the mesh current using Mesh Analysis for the network shown in figure below. [[2+4]]

```figure caption="Network of Question 1 (the 12 V and 6 V batteries have their + terminal at the top)."
fig,ax=ckt_canvas(5.4,3.3,xlim=(-1.6,7.6),ylim=(-0.5,3.9))
isrc(ax,(6,3.2),(0,3.2),"3 A",side=-1)
wire(ax,[(0,3.2),(0,2.2)]); wire(ax,[(6,3.2),(6,2.2)])
res(ax,(0,2.2),(3,2.2),"5 Ω"); res(ax,(3,2.2),(6,2.2),"6 Ω")
batt(ax,(0,0.4),(0,1.6),"12 V",side=1)
res(ax,(3,2.2),(3,0),"2 Ω",side=1)
batt(ax,(6,1.5),(6,2.2),"6 V",side=-1)
res(ax,(6,1.5),(6,0),"1 Ω",side=1,body=0.9)
wire(ax,[(0,0.4),(0,0),(6,0)])
node(ax,(0,2.2)); node(ax,(3,2.2)); node(ax,(6,2.2)); node(ax,(3,0))
```

@q 2
A two-element series circuit is connected across an A.C. source $e = 400\sqrt{2}\sin(\omega t + 40^\circ)$ V. The current in the circuit is then found to be $i = 20\sqrt{2}\cos(314t - 45^\circ)$ A. Determine parameters of the circuit, voltage drop across each element and power factor, power consumed by the circuit. [[6]]

@q 3
The two-wattmeter method produces wattmeter readings $W_1 = 2100$ W and $W_2 = 1550$ W when connected to a star-connected load. If the line voltage is 400 V, calculate: (i) the per-phase average power, (ii) the per phase reactive power, (iii) the power factor, and (iv) the phase impedance. [[6]]

@q 4
Describe the operating principle of a single-phase transformer. Derive the condition for which the efficiency of the transformer is maximum. [[2+4]]

@q 5
A 3-phase, 400 V, 80 kW, 50 Hz, 4-pole induction machine delivers rated output power at a slip of 0.05. Determine the: [[6]]
(a) Synchronous speed,
(b) Motor speed,
(c) Frequency of the rotor current,
(d) Rotor induced voltage at the operating speed, if the stator-to-rotor turns ratio is 1.5 and
(e) Rated torque

@q 6
Describe back emf in a dc motor. Explain the significance of back emf in a dc motor. Draw a constructional diagram of synchronous generator mentioning its components. [[1+2+3]]

@q 7
Draw the full bridge rectifier circuit and explain its operation. Express its equivalent average dc output voltage. [[6]]

@q 8
For the Zener diode network shown below, determine $V_L$, $V_R$, $I_Z$ and $P_Z$ for $R_L = 1.2$ k$\Omega$ and $R_L = 3$ k$\Omega$. [[6]]

```figure caption="Zener network of Question 8: V$_i$ = 16 V, R = 1 kΩ, V$_Z$ = 10 V, P$_{ZM}$ = 30 mW."
fig,ax=ckt_canvas(4.6,2.7,xlim=(-1.9,7.9),ylim=(-0.6,3.2))
batt(ax,(0,0.5),(0,1.7),"V$_i$ = 16 V",side=1)
wire(ax,[(0,1.7),(0,2.4)]); wire(ax,[(0,0.5),(0,0),(6.5,0)])
res(ax,(0,2.4),(3.5,2.4),"R = 1 kΩ")
wire(ax,[(3.5,2.4),(6.5,2.4)])
diode(ax,(3.5,0),(3.5,2.4),"V$_Z$ = 10 V\nP$_{ZM}$ = 30 mW",side=-1,zener=True,off=1.15)
res(ax,(6.5,2.4),(6.5,0),"R$_L$",side=1)
node(ax,(3.5,2.4)); node(ax,(3.5,0))
arrow(ax,(3.15,1.5),(3.15,0.9),"I$_Z$",off=-0.28)
```

@q 9
What are the differences between fuse and MCB? Describe the operating principle of MCB. [[3+3]]

@q 10
Write short notes on: (Any Two) [[2×3]]
(a) Earthing System
(b) Logic Gates
(c) Power Supply System
<!-- SOLUTIONS -->

@s 1
**Definitions.**

*RMS (effective) value.* The RMS value of an alternating quantity is the square root of the mean of the squares of its instantaneous values over one complete cycle. It equals the steady DC value that produces the same heating effect in a resistor:

$$\begin{gathered}I_{rms} = \sqrt{\frac{1}{T}\int_0^T i^2\,dt}\ \\ I_{rms} = \frac{I_m}{\sqrt2} = 0.707\,I_m\ \text{(sine wave)}\end{gathered}$$

*Average value.* The average value is the mean of the instantaneous values over a cycle. For a symmetrical wave it is zero, so it is taken over one half cycle:

$$\begin{gathered}I_{av} = \frac{1}{T/2}\int_0^{T/2} i\,dt\ \\ I_{av} = \frac{2I_m}{\pi} = 0.637\,I_m\ \text{(sine wave)}\end{gathered}$$

The form factor is $I_{rms}/I_{av} = 1.11$ and the peak factor is $I_m/I_{rms} = 1.414$.

**Mesh analysis.** Take three clockwise meshes: $I_1$ (left window: 12 V, 5 Ω, 2 Ω), $I_2$ (right window: 2 Ω, 6 Ω, 6 V, 1 Ω) and $I_3$ (the outer top loop which holds the current source, the 6 Ω and the 5 Ω). The 3 A source sits in a branch that belongs to the top mesh alone, so that mesh current is fixed by the source. The arrow points from right to left, which is **anticlockwise**, hence

$$I_3 = -3\ \text{A (clockwise reference)}.$$

```figure caption="Mesh currents (all clockwise). I$_3$ is forced by the current source, so only I$_1$ and I$_2$ are unknown."
fig,ax=ckt_canvas(5.4,3.3,xlim=(-1.6,7.6),ylim=(-0.5,3.9))
isrc(ax,(6,3.2),(0,3.2),"3 A",side=-1)
wire(ax,[(0,3.2),(0,2.2)]); wire(ax,[(6,3.2),(6,2.2)])
res(ax,(0,2.2),(3,2.2),"5 Ω",off=-0.4); res(ax,(3,2.2),(6,2.2),"6 Ω",off=-0.4)
batt(ax,(0,0.4),(0,1.6),"12 V",side=1)
res(ax,(3,2.2),(3,0),"2 Ω",side=-1)
batt(ax,(6,1.5),(6,2.2),"6 V",side=-1)
res(ax,(6,1.5),(6,0),"1 Ω",side=1,body=0.9)
wire(ax,[(0,0.4),(0,0),(6,0)])
mesh(ax,(1.5,1.1),0.5,"I$_1$"); mesh(ax,(4.5,1.1),0.5,"I$_2$"); mesh(ax,(3,2.72),0.3,"I$_3$",size=7.5)
```

Going round each mesh clockwise, a branch element shared by two meshes carries the **difference** of the two mesh currents.

*Mesh 1* (the 12 V battery is a rise, the 5 Ω carries $I_1 - I_3$, the 2 Ω carries $I_1 - I_2$):

$$12 - 5(I_1 - I_3) - 2(I_1 - I_2) = 0 \ \Rightarrow\ 7I_1 - 2I_2 - 5I_3 = 12$$

*Mesh 2* (the 6 V battery is a drop, the 6 Ω carries $I_2 - I_3$, the 1 Ω carries $I_2$, the 2 Ω carries $I_2 - I_1$):

$$-6(I_2 - I_3) - 6 - 1\cdot I_2 - 2(I_2 - I_1) = 0 \ \Rightarrow\ 2I_1 - 9I_2 + 6I_3 = 6$$

Put $I_3 = -3$:

$$\begin{gathered} 7I_1 - 2I_2 = 12 - 15 = -3 \\ 2I_1 - 9I_2 = 6 + 18 = 24 \end{gathered}$$

Determinant $\Delta = 7(-9) - (-2)(2) = -59$.

$$\begin{gathered}I_1 = \frac{(-3)(-9) - (-2)(24)}{-59} = \frac{75}{-59} \\ I_2 = \frac{7(24) - 2(-3)}{-59} = \frac{174}{-59}\end{gathered}$$

$$\boxed{I_1 = -1.271\ \text{A},\qquad I_2 = -2.949\ \text{A},\qquad I_3 = -3\ \text{A}}$$

The minus signs mean that the actual currents flow **anticlockwise** (for $I_1$ and $I_2$ with the polarities shown).

*Branch currents.* 5 Ω: $I_1 - I_3 = 1.729$ A to the right; 2 Ω: $I_1 - I_2 = 1.678$ A downwards; 6 Ω: $I_2 - I_3 = 0.051$ A to the right; 1 Ω: $2.949$ A upwards.

*Check.* Mesh 1: $12 - 5(1.729) - 2(1.678) = 12 - 8.644 - 3.356 = 0$. Mesh 2: $-6(0.0508) - 6 - 1(-2.949) - 2(-2.949 + 1.271) = -0.305 - 6 + 2.949 + 3.356 = 0$. ✓

@s 2
**Step 1: bring both to the sine form.** Since $\cos\theta = \sin(\theta + 90^\circ)$,

$$i = 20\sqrt2\cos(314t - 45^\circ) = 20\sqrt2\sin(314t + 45^\circ)\ \text{A}$$

So the RMS phasors are

$$\begin{gathered}\bar V = 400\angle 40^\circ\ \text{V} \\ \bar I = 20\angle 45^\circ\ \text{A} \\ \omega = 314\ \text{rad/s}\ (f = 50\ \text{Hz}).\end{gathered}$$

**Step 2: impedance.** The current **leads** the voltage by $\varphi = 45^\circ - 40^\circ = 5^\circ$, so the circuit is **R–C** in series.

$$Z = \frac{\bar V}{\bar I} = \frac{400\angle 40^\circ}{20\angle 45^\circ} = 20\angle{-5^\circ}\ \Omega = 19.92 - j1.743\ \Omega$$

$$\boxed{R = 20\cos 5^\circ = 19.92\ \Omega,\qquad X_C = 20\sin 5^\circ = 1.743\ \Omega}$$

$$C = \frac{1}{\omega X_C} = \frac{1}{314 \times 1.743} = 1.827\times10^{-3}\ \text{F} \approx 1827\ \mu\text{F}$$

**Step 3: voltage drops.**

$$\begin{gathered}V_R = IR = 20 \times 19.92 = 398.5\ \text{V} \\ V_C = IX_C = 20 \times 1.743 = 34.9\ \text{V}\end{gathered}$$

Check: $\sqrt{398.5^2 + 34.9^2} = 400$ V ✓.

**Step 4: power factor and power.**

$$\text{p.f.} = \cos 5^\circ = 0.996\ \text{(leading)}$$

$$P = VI\cos\varphi = 400 \times 20 \times 0.9962 = 7970\ \text{W} \ (= I^2R = 400 \times 19.92)$$

$$\boxed{\text{p.f.} = 0.996\ \text{leading},\qquad P = 7.97\ \text{kW}}$$

The reactive power is $Q = VI\sin\varphi = 697$ var (capacitive) and the apparent power is $S = 8000$ VA.

@s 3
For a balanced load, the two-wattmeter readings give

$$\begin{gathered}P = W_1 + W_2 \\ Q = \sqrt3\,(W_1 - W_2) \\ \tan\varphi = \frac{\sqrt3\,(W_1 - W_2)}{W_1 + W_2}\end{gathered}$$

(the load is inductive, since $W_1 > W_2$ with both positive).

**(i) Per-phase average power.**

$$\begin{gathered}P_{total} = 2100 + 1550 = 3650\ \text{W} \\ P_{ph} = \frac{3650}{3} = \mathbf{1216.7\ W}\end{gathered}$$

**(ii) Per-phase reactive power.**

$$\begin{gathered}Q_{total} = \sqrt3\,(2100 - 1550) = 952.6\ \text{var} \\ Q_{ph} = \frac{952.6}{3} = \mathbf{317.5\ var}\ \text{(lagging)}\end{gathered}$$

**(iii) Power factor.**

$$\begin{gathered}\tan\varphi = \frac{952.6}{3650} = 0.2610 \Rightarrow \varphi = 14.63^\circ \\ \cos\varphi = \mathbf{0.968\ lagging}\end{gathered}$$

**(iv) Phase impedance** (star connection: $V_{ph} = 400/\sqrt3 = 230.9$ V).

$$P = \sqrt3\,V_L I_L\cos\varphi \Rightarrow I_L = I_{ph} = \frac{3650}{\sqrt3 \times 400 \times 0.9676} = 5.445\ \text{A}$$

$$\begin{gathered}Z_{ph} = \frac{V_{ph}}{I_{ph}} = \frac{230.9}{5.445} = \mathbf{42.4\ \Omega} \\ Z = 42.4\angle 14.63^\circ = 41.04 + j10.71\ \Omega\end{gathered}$$

So $R_{ph} = 41.0\ \Omega$ and $X_{ph} = 10.7\ \Omega$ (inductive).

@s 4
**Principle.** A transformer works on **mutual induction** (Faraday's law). An alternating voltage $V_1$ applied to the primary drives an alternating magnetising current, which sets up an alternating flux $\Phi = \Phi_m\sin\omega t$ in the laminated iron core. The flux links the secondary winding as well. By Faraday's law it induces an emf in every turn, so

$$\begin{gathered}E_1 = 4.44 f N_1 \Phi_m \\ E_2 = 4.44 f N_2 \Phi_m \\ \frac{E_2}{E_1} = \frac{N_2}{N_1} = \frac{V_2}{V_1} = \frac{I_1}{I_2} = K\end{gathered}$$

There is no electrical connection between the windings: energy is transferred by the common flux at constant frequency. If $K > 1$ it is a step-up transformer, and if $K < 1$ it is step-down.

```figure caption="Single-phase core-type transformer: the flux in the core links both windings."
fig,ax=ckt_canvas(5.0,3.0,xlim=(-2.9,6.9),ylim=(-0.5,3.2))
t=transformer(ax,0,0,3.0,2.6)
acsrc(ax,(-1.6,0.45),(-1.6,2.15),"V$_1$",side=1,off=0.62)
wire(ax,[t["p_top"],(-1.6,t["p_top"][1]),(-1.6,2.15)]); wire(ax,[t["p_bot"],(-1.6,t["p_bot"][1]),(-1.6,0.45)])
res(ax,(4.7,2.2),(4.7,0.5),"Load",side=-1)
wire(ax,[t["s_top"],(4.7,t["s_top"][1]),(4.7,2.2)]); wire(ax,[t["s_bot"],(4.7,t["s_bot"][1]),(4.7,0.5)])
label(ax,(-0.35,3.05),"primary N$_1$",color="#1d6fb8"); label(ax,(3.4,3.05),"secondary N$_2$",color="#d9534f")
label(ax,(1.5,1.3),"Φ",size=12)
ax.annotate("",xy=(1.9,1.8),xytext=(1.1,1.8),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2))
```

**Condition for maximum efficiency.** Let $x$ be the fraction of full load, $S$ the rated kVA, $P_i$ the iron (core) loss, which depends on voltage and frequency and is **constant**, and $P_{cu}$ the full-load copper loss, so that the copper loss at load $x$ is $x^2P_{cu}$.

$$\eta = \frac{\text{output}}{\text{input}} = \frac{xS\cos\varphi}{xS\cos\varphi + P_i + x^2P_{cu}}$$

Dividing by $x$ and writing the denominator as $D = S\cos\varphi + P_i/x + xP_{cu}$, $\eta$ is maximum when $D$ is minimum:

$$\frac{dD}{dx} = -\frac{P_i}{x^2} + P_{cu} = 0\ \Rightarrow\ x^2P_{cu} = P_i$$

$$\begin{gathered}\boxed{\text{Copper loss at that load} = \text{Iron loss}} \\ x_{\eta max} = \sqrt{\frac{P_i}{P_{cu}}}\end{gathered}$$

(The second derivative $2P_i/x^3 > 0$, so this is indeed a minimum of $D$.) The maximum efficiency is

$$\eta_{max} = \frac{x S\cos\varphi}{xS\cos\varphi + 2P_i}$$

```figure caption="Efficiency against load fraction x for P$_i$ = 0.5 P$_{cu}$ (illustrative): the peak occurs where the copper loss x²P$_{cu}$ equals the constant iron loss P$_i$."
import numpy as np, matplotlib.pyplot as plt
x=np.linspace(0.02,1.4,300); Pi=0.5; Pc=1.0; S=100; pf=0.8
eta=100*x*S*pf/(x*S*pf+Pi+x**2*Pc)
xm=np.sqrt(Pi/Pc)
fig,ax=plt.subplots(figsize=(5.2,2.5))
ax.plot(x,eta,color=ACCENT); ax.axvline(xm,ls=':',color=SERIES[1]); ax.plot([xm],[100*xm*S*pf/(xm*S*pf+2*Pi)],'o',color=SERIES[1])
ax.text(xm+0.04,97.9,"x = √(P$_i$/P$_{cu}$)",fontsize=7.8,color=SERIES[1])
ax.set_xlabel("load fraction x"); ax.set_ylabel("efficiency η (%)"); ax.set_ylim(96.5,100)
```

@s 5
Given: $V_L = 400$ V, $P_{out} = 80$ kW, $f = 50$ Hz, $P = 4$ poles, $s = 0.05$.

**(a) Synchronous speed.**

$$N_s = \frac{120f}{P} = \frac{120 \times 50}{4} = \mathbf{1500\ rpm}\quad(\omega_s = 157.1\ \text{rad/s})$$

**(b) Motor speed.**

$$N = N_s(1 - s) = 1500\,(1 - 0.05) = \mathbf{1425\ rpm}$$

**(c) Frequency of the rotor current.**

$$f_r = sf = 0.05 \times 50 = \mathbf{2.5\ Hz}$$

**(d) Rotor induced voltage at the operating speed.** The stator phase voltage (star-connected stator) is $400/\sqrt3 = 230.9$ V. With a stator-to-rotor turns ratio $N_1/N_2 = 1.5$, the rotor emf **at standstill** (per phase) is

$$E_{2} = \frac{230.9}{1.5} = 153.96\ \text{V}.$$

The rotor emf is proportional to the slip, so at the operating speed

$$E_{2r} = sE_2 = 0.05 \times 153.96 = \mathbf{7.70\ V\ per\ phase}\quad(\approx 13.3\ \text{V between rotor lines if the rotor is star-connected})$$

**(e) Rated torque.**

$$\begin{gathered}\omega = \frac{2\pi N}{60} = \frac{2\pi \times 1425}{60} = 149.2\ \text{rad/s}\ \\ T = \frac{P_{out}}{\omega} = \frac{80\,000}{149.2} = \mathbf{536\ N\,m}\end{gathered}$$

@s 6
**Back emf.** When the armature of a DC motor rotates, its conductors cut the main-pole flux, so an emf is induced in them according to the generator action. By Lenz's law this emf **opposes the applied voltage** (the cause producing the rotation), hence it is called the back (counter) emf:

$$\begin{gathered}E_b = \frac{P\Phi Z N}{60A}\ \text{volt} \\ V = E_b + I_aR_a \ \Rightarrow\ I_a = \frac{V - E_b}{R_a}\end{gathered}$$

**Significance of back emf.**

1. *It makes the motor self-regulating.* If the load rises, the motor slows, $E_b$ falls, $I_a = (V - E_b)/R_a$ increases and so does the torque until it balances the load. If the load falls, the opposite happens. Speed settles automatically.
2. *It limits the armature current.* At standstill $E_b = 0$ and $I_a = V/R_a$ is 20–30 times the rated value, because $R_a$ is tiny. So a starter (series resistance) is needed at starting, and it is cut out as $E_b$ builds up.
3. *It is the measure of energy conversion.* Multiplying $V = E_b + I_aR_a$ by $I_a$ gives $VI_a = E_bI_a + I_a^2R_a$, so $E_bI_a$ is the electrical power converted into mechanical power, and $I_a^2R_a$ is the copper loss. The motor torque is $T = E_bI_a/\omega$.
4. *It determines speed:* $N \propto E_b/\Phi$.

**Constructional diagram of a synchronous generator (alternator).**

```figure caption="Cross-section of a salient-pole synchronous generator: the DC-excited rotor poles rotate inside the stationary armature winding."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Rectangle, Polygon
fig,ax=plt.subplots(figsize=(5.6,3.7)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-3.5,7.3); ax.set_ylim(-3.1,3.1)
ax.add_patch(Wedge((0,0),2.9,0,360,width=0.38,fc="#9aa3b2",ec=INK,lw=1.1))      # frame
ax.add_patch(Wedge((0,0),2.52,0,360,width=0.52,fc="#d5dae3",ec=INK,lw=1.1))     # stator core
for a in np.linspace(0,2*np.pi,24,endpoint=False):
    ax.add_patch(Circle((2.15*np.cos(a),2.15*np.sin(a)),0.1,fc=SERIES[1],ec=INK,lw=0.5))   # armature conductors in slots
ax.add_patch(Circle((0,0),1.0,fc="#f6f8fc",ec=INK,lw=1.2))                       # rotor spider
for ang,col in ((0,"#1d6fb8"),(180,"#2e8b57")):
    ax.add_patch(Wedge((0,0),1.82,ang-32,ang+32,width=0.62,fc=col,ec=INK,lw=1.0,alpha=0.85))   # pole shoe
    for s in (-1,1):
        a=np.radians(ang+s*40); ax.add_patch(Circle((1.3*np.cos(a),1.3*np.sin(a)),0.17,fc="#b8860b",ec=INK,lw=0.5))
ax.text(1.38,0,"N",color="white",fontsize=9,fontweight="bold",ha="center",va="center"); ax.text(-1.38,0,"S",color="white",fontsize=9,fontweight="bold",ha="center",va="center")
ax.add_patch(Circle((0,0),0.22,fc=INK))
def lab(txt,xy,xt):
    ax.annotate(txt,xy=xy,xytext=xt,fontsize=7.8,color=INK,arrowprops=dict(arrowstyle="-",color=MUTED,lw=0.8),va="center")
lab("stator frame (cast iron / steel)",(2.1,2.0),(3.3,2.6))
lab("stator core: laminated silicon steel",(2.55,0.5),(3.3,1.6))
lab("armature winding (3-phase) in slots",(2.08,-0.56),(3.3,-0.3))
lab("air gap",(1.84,0.15),(3.3,0.65))
lab("salient pole + pole shoe",(1.5,-0.55),(3.3,-1.1))
lab("field (exciter) winding on pole",(0.99,-0.84),(3.3,-1.85))
lab("shaft, rotated by prime mover",(0.0,-0.2),(3.3,-2.6))
```

*Main parts.* (1) **Stator** (armature): a frame holding a laminated slotted core that carries the 3-phase armature winding; the load current and the output voltage are taken from here. (2) **Rotor**: a salient-pole (low-speed, hydro) or cylindrical (high-speed, turbo) structure carrying the field winding, driven by a prime mover. (3) **Slip rings and brushes** carry DC from the exciter to the rotating field winding. (4) **Exciter**: a small DC source (or a rectifier) for the field. (5) **Air gap**, **shaft**, **bearings** and the cooling arrangement.

*Frequency.* The emf frequency is $f = PN_s/120$, so a 4-pole rotor at 1500 rpm gives 50 Hz.

@s 7
**Circuit.** Four diodes $D_1$–$D_4$ are connected as a bridge. The AC source (through a transformer, if needed) is connected to one diagonal, and the load $R_L$ to the other. No centre-tapped transformer is needed.

```figure caption="Full-wave bridge rectifier. Positive half-cycle: D$_1$ and D$_4$ conduct; negative half-cycle: D$_2$ and D$_3$ conduct. The current through R$_L$ always flows in the same direction."
fig,ax=ckt_canvas(5.4,3.6,xlim=(-2.2,8.6),ylim=(-2.3,3.2))
L=(1.6,1.0); T=(3.2,2.6); R=(4.8,1.0); B=(3.2,-0.6)
diode(ax,L,T,"D$_1$",side=-1,off=0.45); diode(ax,R,T,"D$_2$",side=1,off=0.45)
diode(ax,B,L,"D$_3$",side=-1,off=0.45); diode(ax,B,R,"D$_4$",side=1,off=0.45)
acsrc(ax,(-0.6,-1.7),(-0.6,0.4+0.6),"v$_s$",side=1,off=0.7)
wire(ax,[(-0.6,1.0),(1.6,1.0)]); wire(ax,[(-0.6,-1.7),(4.8,-1.7),(4.8,1.0)])
wire(ax,[T,(7.4,2.6)]); res(ax,(7.4,2.6),(7.4,-1.0),"R$_L$",side=-1)
wire(ax,[B,(3.2,-1.0),(7.4,-1.0)])
node(ax,L); node(ax,R); node(ax,T); node(ax,B)
label(ax,(3.2,3.0),"+",size=11); label(ax,(3.2,-1.35),"−",size=11)
arrow(ax,(5.4,2.9),(6.5,2.9),"i$_L$",off=0.22)
```

**Operation.**

- *Positive half-cycle* (upper terminal of the source positive): $D_1$ and $D_4$ are forward biased, $D_2$ and $D_3$ are reverse biased. Current flows: source → $D_1$ → $R_L$ (top to bottom) → $D_4$ → back to the source.
- *Negative half-cycle*: the polarity reverses, $D_2$ and $D_3$ conduct, $D_1$ and $D_4$ block. Current flows: source (lower terminal positive) → $D_2$ → $R_L$ (again top to bottom) → $D_3$ → back to the source.

In both half-cycles the current passes through $R_L$ in the same direction, so the load voltage is a pulsating DC made of positive half-sine loops, $v_L = |V_m\sin\omega t|$ (ripple frequency $2f$).

```figure caption="Input voltage and the full-wave rectified output. The dashed line is the average (dc) value 2V$_m$/π = 0.637 V$_m$."
import numpy as np, matplotlib.pyplot as plt
t=np.linspace(0,4*np.pi,600)
fig,(a,b)=plt.subplots(2,1,figsize=(5.2,3.2),sharex=True)
a.plot(t,np.sin(t),color=ACCENT); a.axhline(0,color=INK,lw=0.6); a.set_ylabel("v$_s$ / V$_m$")
b.plot(t,abs(np.sin(t)),color=SERIES[1]); b.axhline(2/np.pi,ls='--',color=INK,lw=0.9)
b.text(4*np.pi*0.985,2/np.pi+0.05,"V$_{dc}$ = 0.637 V$_m$",ha='right',fontsize=7.5)
b.set_ylabel("v$_L$ / V$_m$"); b.set_xticks([0,np.pi,2*np.pi,3*np.pi,4*np.pi]); b.set_xticklabels(["0","π","2π","3π","4π"]); b.set_xlabel("ωt")
```

**Average (dc) output voltage.** With $v_s = V_m\sin\omega t$ and ideal diodes,

$$V_{dc} = \frac{1}{\pi}\int_0^{\pi} V_m\sin\theta\,d\theta = \frac{V_m}{\pi}\big[-\cos\theta\big]_0^{\pi} = \frac{2V_m}{\pi}$$

$$\boxed{V_{dc} = \frac{2V_m}{\pi} = 0.637\,V_m = 0.9\,V_{rms}}$$

In a practical bridge two diodes are in series in the conduction path, so $V_{dc} = \dfrac{2(V_m - 2V_D)}{\pi}$ ($V_D \approx 0.7$ V for silicon). Other figures of merit: $I_{dc} = 2I_m/\pi$, $V_{rms} = V_m/\sqrt2$, ripple factor $r = 0.482$, rectification efficiency $\eta = 81.2\%$, and the peak inverse voltage of each diode is $V_m$.

@s 8
Given $V_i = 16$ V, $R = 1\ \text{k}\Omega$, $V_Z = 10$ V, $P_{ZM} = 30$ mW, so the maximum Zener current is $I_{ZM} = P_{ZM}/V_Z = 30/10 = 3$ mA.

**Method.** First remove the Zener and find the open-circuit voltage across $R_L$ (voltage-divider):

$$V_{L}' = \frac{R_L}{R + R_L}V_i$$

If $V_L' \ge V_Z = 10$ V the Zener is ON (it clamps $V_L = V_Z$). If $V_L' < V_Z$ it is OFF (an open circuit).

**Case 1: $R_L = 1.2\ \text{k}\Omega$.**

$$V_L' = \frac{1.2}{1 + 1.2}\times16 = 8.73\ \text{V} < 10\ \text{V}$$

The Zener is **OFF**.

$$\begin{gathered}V_L = 8.73\ \text{V} \\ V_R = 16 - 8.73 = 7.27\ \text{V} \\ I_Z = 0 \\ P_Z = 0\end{gathered}$$

(The series current is $7.27\ \text{V}/1\ \text{k}\Omega = 7.27$ mA, all going to the load.)

**Case 2: $R_L = 3\ \text{k}\Omega$.**

$$V_L' = \frac{3}{1 + 3}\times16 = 12\ \text{V} > 10\ \text{V}$$

The Zener is **ON**, so $V_L = V_Z = 10$ V.

$$\begin{gathered}V_R = 16 - 10 = 6\ \text{V} \\ I_R = \frac{6}{1\ \text{k}\Omega} = 6\ \text{mA} \\ I_L = \frac{10}{3\ \text{k}\Omega} = 3.33\ \text{mA}\end{gathered}$$

$$\begin{gathered}I_Z = I_R - I_L = 6 - 3.33 = 2.67\ \text{mA} \\ P_Z = V_ZI_Z = 10 \times 2.67 = 26.7\ \text{mW}\end{gathered}$$

Since $26.7\ \text{mW} < P_{ZM} = 30$ mW (equivalently $I_Z < 3$ mA), the diode is within its rating.

| $R_L$ | Zener | $V_L$ | $V_R$ | $I_Z$ | $P_Z$ |
|---|---|---|---|---|---|
| 1.2 kΩ | OFF | 8.73 V | 7.27 V | 0 | 0 |
| 3 kΩ | ON | 10 V | 6 V | 2.67 mA | 26.7 mW |

@s 9
**Differences between a fuse and an MCB.**

| Basis | Fuse | MCB (miniature circuit breaker) |
|---|---|---|
| Operating principle | A thin fusible element melts (heating effect, $I^2R$) | Bimetallic strip (overload) and electromagnet (short circuit) trip a spring-loaded latch |
| After operation | Element is destroyed and must be **replaced** | Switched back **on by hand** after the fault is cleared; reusable |
| Operating time | Slower, and varies with ageing and ambient temperature | Fast and repeatable; a defined tripping curve |
| Protection against | Overload and short circuit (single-pole behaviour) | Overload and short circuit; many types can also be operated as a switch |
| Fault indication | Must open the holder and inspect the element | Handle drops to OFF, so the faulty circuit is evident at a glance |
| Breaking capacity and cost | Cheap, lower breaking capacity | Dearer, higher breaking capacity (up to 10 kA) |
| Multi-pole use | A fuse in each phase may blow separately, giving single-phasing of 3-phase loads | Common trip bar opens all poles together |

**Operating principle of the MCB.** The MCB has two tripping mechanisms acting on the same contacts:

1. *Thermal (overload) trip.* The load current passes through a **bimetallic strip**. A moderate overload heats the strip; the two metals expand differently, so it bends. After a delay that falls as the overload grows (inverse-time characteristic) the strip releases the latch, and the spring pulls the contacts apart.
2. *Magnetic (short-circuit) trip.* The load current also flows through a **solenoid** coil. A short circuit gives a very large current, and the coil pulls in a plunger that strikes the trip lever instantly (within a few milliseconds), opening the contacts.
3. *Arc extinction.* When the contacts open on load, an arc forms. It is drawn into the **arc chute** (a stack of steel splitter plates) where it is split into short arcs, cooled and extinguished.

```figure caption="Internal arrangement of a miniature circuit breaker (schematic)."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
fig,ax=plt.subplots(figsize=(5.4,2.9)); ax.axis('off'); ax.set_xlim(0,11); ax.set_ylim(0,5.4)
ax.add_patch(FancyBboxPatch((0.6,0.7),7.4,3.6,boxstyle="round,pad=0.05,rounding_size=0.2",fc="#f6f8fc",ec=INK,lw=1.4))
ax.plot([0.6,1.8],[2.5,2.5],color=INK,lw=2.2); ax.text(0.45,2.5,"in",ha='right',va='center',fontsize=8)
ax.plot([1.8,2.9],[2.5,2.5],color=INK,lw=2)
ax.add_patch(Rectangle((2.9,2.25),1.7,0.5,fc="#e2b25e",ec=INK,lw=1)); ax.text(3.45,3.35,"bimetallic strip\n(thermal trip)",ha='center',fontsize=7.2)
ax.plot([4.6,4.6],[2.5,2.5],color=INK)
for i in range(6): ax.plot([4.6+i*0.22,4.7+i*0.22],[2.5,2.95 if i%2==0 else 2.05],color=SERIES[1],lw=1.4)
ax.text(5.9,3.45,"solenoid\n(magnetic trip)",ha='center',fontsize=7.2)
ax.plot([5.95,6.55],[2.5,2.5],color=INK,lw=2)
ax.plot([6.55,7.25],[2.5,3.1],color=INK,lw=2.4); ax.plot([7.25,7.25],[2.0,2.4],color=INK,lw=0)
ax.plot([7.3,7.3],[1.9,2.35],color=INK,lw=2.4)
ax.text(6.1,1.25,"moving contact\n+ fixed contact",ha='center',fontsize=7.2)
for k in range(5): ax.plot([7.55,7.95],[1.0+0.55*k,1.0+0.55*k],color=MUTED,lw=2.2)
ax.text(9.5,2.5,"arc chute\n(splitter\nplates)",ha='center',va='center',fontsize=7.6)
ax.plot([7.3,8.0,8.0],[1.9,1.9,2.1],color=INK,lw=0); ax.plot([8.0,8.9],[0.55,0.55],color=INK,lw=2.2); ax.text(9.0,0.55,"out",ha='left',va='center',fontsize=8)
ax.plot([4.3,4.9],[4.3,5.0],color=INK,lw=2.4); ax.text(5.3,5.0,"operating handle (ON/OFF)",fontsize=7.6,va='center')
```

@s 10
Any two are required; all three are answered here.

**(a) Earthing system.** *Earthing* means connecting the non-current-carrying metal parts of an installation (or the neutral of the supply) to the general mass of earth through a low-resistance conductor.

*Purposes.* (1) To protect people from electric shock: if insulation fails, the metal body stays at earth potential and the leakage current is carried to earth. (2) To let the fault current flow so that the fuse or MCB operates quickly. (3) To protect equipment and lines from lightning and surges. (4) To hold the system voltage steady with respect to earth.

*Methods.* Plate earthing (a copper $60 \times 60 \times 0.3$ cm or GI $60 \times 60 \times 0.6$ cm plate buried at 3 m), **pipe earthing** (a GI pipe of 38–50 mm diameter and 2–3 m long, the most common), rod earthing and strip or mat earthing.

*Pipe earthing.* The pipe is driven vertically into moist ground. The earth wire is bolted near the top, the surrounding pit is filled with alternate layers of **charcoal and common salt** (or bentonite) which keep the soil moist and conductive, and a funnel at the top lets water be poured in during dry weather. The earth electrode resistance should be low: about 5 Ω or less for a house (1 Ω or less for substations).

```figure caption="Pipe earthing: the equipment body is bonded to a GI pipe buried in salt-and-charcoal filling."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
fig,ax=plt.subplots(figsize=(5.0,3.0)); ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,6.2)
ax.add_patch(Rectangle((0,0),10,3.4,fc="#e9e4d8",ec="none")); ax.plot([0,10],[3.4,3.4],color=INK,lw=1.4); ax.text(9.9,3.55,"ground level",ha='right',fontsize=7.6)
ax.add_patch(Rectangle((3.4,0.2),1.7,2.7,fc="#cfd5de",ec=MUTED,lw=0.8,hatch="..")); ax.add_patch(Rectangle((4.0,0.1),0.5,3.4,fc="#9aa3b2",ec=INK,lw=1.2))
ax.add_patch(Polygon([[3.8,4.1],[4.7,4.1],[4.5,3.5],[4.0,3.5]],fc="#d5dae3",ec=INK)); ax.text(5.3,4.3,"funnel with\nwire mesh",fontsize=7.6,va='center')
ax.add_patch(Rectangle((0.6,3.6),1.8,1.4,fc="#2e8b57",ec=INK,alpha=0.85)); ax.text(1.5,4.3,"equipment\nbody",ha='center',va='center',fontsize=7.6,color="white")
ax.plot([2.4,3.0,3.0,4.25,4.25],[4.3,4.3,3.3,3.3,2.9],color=SERIES[1],lw=1.8); ax.text(2.6,3.75,"earth wire",fontsize=7.6,color=SERIES[1],ha='right')
ax.text(6.2,2.45,"charcoal + salt layers",fontsize=7.6,va='center'); ax.plot([5.1,6.1],[2.1,2.4],color=MUTED,lw=0.8)
ax.text(6.2,1.2,"GI pipe, 38–50 mm, 2.5–3 m long\n(holes in the lower part)",fontsize=7.6,va='center'); ax.plot([4.5,6.1],[1.0,1.2],color=MUTED,lw=0.8)
```

**(b) Logic gates.** A logic gate is a digital circuit with one or more inputs and one output that implements a Boolean function. Inputs and outputs have only two levels, 0 (low) and 1 (high). The **AND, OR and NOT** gates are the basic gates, and **NAND and NOR** are *universal* gates, since any logic function can be built from either alone. XOR and XNOR are the exclusive gates.

```figure caption="Symbols of the basic logic gates."
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(5.6,2.6)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-0.6,13.9); ax.set_ylim(-0.7,3.7)
spec=[("AND",0,2.6),("OR",4.7,2.6),("NOT",9.4,2.6),("NAND",0,0.7),("NOR",4.7,0.7),("XOR",9.4,0.7)]
for k,x,y in spec:
    gate(ax,k,x+0.4,y,w=1.5,h=1.0,lead=0.55)
    ax.text(x+1.4,y-0.95,k,ha='center',fontsize=8,color=MUTED)
```

| Gate | Expression | $A,B = 00$ | $01$ | $10$ | $11$ |
|---|---|---|---|---|---|
| AND | $Y = A\cdot B$ | 0 | 0 | 0 | 1 |
| OR | $Y = A + B$ | 0 | 1 | 1 | 1 |
| NOT | $Y = \bar A$ | 1 (for $A=0$) | 0 (for $A=1$) | – | – |
| NAND | $Y = \overline{A\cdot B}$ | 1 | 1 | 1 | 0 |
| NOR | $Y = \overline{A + B}$ | 1 | 0 | 0 | 0 |
| XOR | $Y = A\oplus B$ | 0 | 1 | 1 | 0 |
| XNOR | $Y = \overline{A\oplus B}$ | 1 | 0 | 0 | 1 |

**(c) Power supply system.** Electric power in Nepal reaches the consumer in four stages:

1. *Generation* in hydro-power stations at 6.6–11 kV (three-phase, 50 Hz).
2. *Transmission.* Step-up transformers raise the voltage to 132, 220 or 400 kV so that the line current, and so the $I^2R$ loss, is small; the national grid interconnects the stations.
3. *Sub-transmission and distribution.* Grid substations step down to 66/33 kV, then to 11 kV (primary distribution).
4. *Utilisation.* Distribution transformers step 11 kV down to **400 V three-phase / 230 V single-phase** (secondary distribution) for homes and industry.

```figure caption="Layout of an electric power supply system."
fig=blockchain([("Generating station","6.6–11 kV"),("Step-up substation","132–400 kV"),("Transmission grid","220 / 132 kV"),("Step-down substation","33 / 11 kV"),("Distribution transformer","400 / 230 V"),("Consumer","homes, industry")],cols=3)
```

In a *regulated DC power supply* (for electronic circuits) the 230 V AC is passed through a step-down transformer, a rectifier, a filter capacitor and a voltage regulator (Zener or IC 78xx) to give a steady DC output.

