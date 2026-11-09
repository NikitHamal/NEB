---
file: NEBians-IOE-Past-Paper-Basic-Electrical-and-Electronics-Engineering-ENEE103-2081-Chaitra.pdf
subject: Basic Electrical and Electronics Engineering
level: BE · Year I / Part I
code: ENEE 103
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BCE, BCH
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
State KCL and KVL. Explain different types of voltage and current sources. [[2+4]]

@q 2
Determine the current through branch a-b of the circuit given below using Nodal Analysis. [[6]]

```figure caption="Circuit of Question 2 (the left resistor, printed '2V' on the scan, is read as 2 Ω; both sources have + at the top)."
fig,ax=ckt_canvas(5.6,3.1,xlim=(-1.2,10.2),ylim=(-0.7,3.7))
res(ax,(0,3),(0,0),"2 Ω",side=-1)
wire(ax,[(0,3),(3,3)]); wire(ax,[(0,0),(9,0)])
res(ax,(3,3),(6.5,3),"10 Ω",side=1); res(ax,(6.5,3),(9,3),"2 Ω",side=1,body=0.9); 
res(ax,(3,3),(3,1.8),"5 Ω",side=-1,body=0.9); vsrc(ax,(3,0),(3,1.8),"25 V",side=-1)
res(ax,(6.5,3),(6.5,0),"4 Ω",side=1)
vsrc(ax,(9,0),(9,3),"50 V",side=-1)
for p in ((3,3),(6.5,3),(6.5,0)): node(ax,p)
label(ax,(3,3.35),"a"); label(ax,(6.5,3.35),"b"); label(ax,(6.5,-0.35),"c")
```

@q 3
From the given circuit, find total current (I), branch currents I$_1$ and I$_2$, and real power. [[6]]

```figure caption="Circuit of Question 3: two parallel branches supplied by 200∠53.8° V."
fig,ax=ckt_canvas(5.4,3.2,xlim=(-0.8,8.0),ylim=(-1.0,4.2))
res(ax,(1,3.6),(3.8,3.6),"18 Ω"); ind(ax,(3.8,3.6),(7,3.6),"j24 Ω")
res(ax,(1,1.8),(3.8,1.8),"15 Ω"); cap(ax,(3.8,1.8),(7,1.8),"−j30 Ω")
wire(ax,[(1,1.8),(1,3.6)]); wire(ax,[(7,1.8),(7,3.6)])
wire(ax,[(0,0),(0,2.7),(1,2.7)]); wire(ax,[(7,2.7),(8,2.7),(8,0)]); node(ax,(1,2.7)); node(ax,(7,2.7))
acsrc(ax,(0,0),(8,0),"200∠53.8° V",side=-1,off=0.75)
arrow(ax,(1.2,4.0),(2.0,4.0),"I$_1$",off=0.2); arrow(ax,(1.2,2.2),(2.0,2.2),"I$_2$",off=0.2)
arrow(ax,(-0.35,0.8),(-0.35,1.8),"I",off=-0.25); 
```

@q 4
Define transformer, describe operating principle of transformer and write emf equation for it. [[6]]

@q 5
An ideal 25 kVA transformer has 500 turns on the primary winding and 40 turns on the secondary winding. The primary is connected to 3,000 V, 50 Hz supply. Calculate [[6]]
i) Primary and secondary currents on full load.
ii) Secondary emf
iii) The maximum core flux

@q 6
Define DC machine and describe the different parts related to construction of DC Machine. [[6]]

@q 7
For the circuit shown below, find: [[6]]
i) the output voltage
ii) the voltage drop across series resistance
iii) the current through Zener diode

```figure caption="Circuit of Question 7: 120 V supply, R = 5 kΩ, Zener 50 V, load 10 kΩ."
fig,ax=ckt_canvas(4.6,2.6,xlim=(-1.9,7.9),ylim=(-0.6,3.2))
batt(ax,(0,0.5),(0,1.7),"120 V",side=1)
wire(ax,[(0,1.7),(0,2.4)]); wire(ax,[(0,0.5),(0,0),(6.5,0)])
res(ax,(0,2.4),(3.5,2.4),"R = 5 kΩ"); wire(ax,[(3.5,2.4),(6.5,2.4)])
diode(ax,(3.5,0),(3.5,2.4),"50 V",side=-1,zener=True,off=0.7)
res(ax,(6.5,2.4),(6.5,0),"10 kΩ",side=1); node(ax,(3.5,2.4)); node(ax,(3.5,0))
arrow(ax,(1.4,2.75),(2.2,2.75),"I",off=0.2); arrow(ax,(3.15,1.7),(3.15,1.0),"I$_Z$",off=-0.28); arrow(ax,(4.5,2.75),(5.3,2.75),"I$_L$",off=0.2)
```

@q 8
Why is transistor called Bipolar Junction Transistor? Explain the operation of the npn transistor in active mode. [[2+4]]

@q 9
Why are protective devices important in residential installation? Explain in brief different types of protective devices used nowadays. [[3+3]]

@q 10
Write short notes on: (Any Two) [[2×3]]
a) Types of Electrical wiring system
b) Electrical safety rules
c) Ex-OR and Ex-nor gate
<!-- SOLUTIONS -->

@s 1
**Kirchhoff's current law (KCL).** The algebraic sum of the currents meeting at a node (junction) is zero; equivalently, the total current entering a node equals the total current leaving it:

$$\sum I = 0\quad(\text{charge is conserved at a node})$$

**Kirchhoff's voltage law (KVL).** The algebraic sum of all the voltages (rises and drops) around any closed loop of a circuit is zero; the sum of the emfs equals the sum of the potential drops:

$$\sum V = 0\quad(\text{energy is conserved around a loop})$$

*Example.* In a loop with a 12 V battery and resistors 2 Ω and 4 Ω in series: $12 - 2I - 4I = 0$, so $I = 2$ A. At a junction where 5 A and 3 A enter, $I_{out} = 8$ A.

**Types of sources.** A source supplies electrical energy to a circuit.

*Voltage sources.*

- **Ideal independent voltage source:** keeps a fixed terminal voltage whatever the current drawn (internal resistance $= 0$). It is a battery or DC supply (symbol: circle with +/−, or long and short plates).
- **Practical voltage source:** an ideal source $E$ in *series* with an internal resistance $r$; terminal voltage $V = E - Ir$ falls with load.
- **Dependent (controlled) voltage source:** its voltage depends on a voltage or current elsewhere in the circuit (VCVS, CCVS); used to model transistors and amplifiers (drawn as a diamond).

*Current sources.*

- **Ideal independent current source:** supplies a fixed current whatever the voltage across it (internal resistance $= \infty$).
- **Practical current source:** an ideal source $I_s$ in *parallel* with a resistance $r$; the output current is $I = I_s - V/r$.
- **Dependent current source:** the current is proportional to some other voltage or current (VCCS, CCCS), e.g. $i_c = \beta i_b$.

*By waveform:* **DC sources** (batteries, solar cells, rectifier supplies: constant polarity) and **AC sources** (alternators, mains: sinusoidal, alternating polarity). A practical voltage source and a practical current source can be converted into one another (source transformation): $I_s = E/r$ with the same $r$.

@s 2
Take c as the reference node, $V_c = 0$. The unknown node voltages are $V_a$ and $V_b$. Reading the circuit: node a has the 2 Ω resistor to c, the 5 Ω resistor in series with the 25 V source (its + terminal at the top, so the branch ends on the 25 V side at c), and the 10 Ω resistor to b. Node b has the 10 Ω to a, the 4 Ω to c, and the 2 Ω in series with the 50 V source.

**KCL at node a** (sum of currents leaving a $= 0$):

$$\frac{V_a}{2} + \frac{V_a - 25}{5} + \frac{V_a - V_b}{10} = 0\ \Rightarrow\ 5V_a + 2V_a - 50 + V_a - V_b = 0\ \Rightarrow\ 8V_a - V_b = 50$$

**KCL at node b:**

$$\frac{V_b - V_a}{10} + \frac{V_b}{4} + \frac{V_b - 50}{2} = 0\ \Rightarrow\ 2V_b - 2V_a + 5V_b + 10V_b - 500 = 0\ \Rightarrow\ -2V_a + 17V_b = 500$$

Solve: from the first, $V_b = 8V_a - 50$. Substitute in the second:

$$-2V_a + 17(8V_a - 50) = 500 \Rightarrow 134V_a = 1350$$

$$\begin{gathered}V_a = 10.075\ \text{V} \\ V_b = 8(10.075) - 50 = 30.597\ \text{V}\end{gathered}$$

**Current in branch a-b:**

$$I_{ab} = \frac{V_a - V_b}{10} = \frac{10.075 - 30.597}{10} = -2.052\ \text{A}$$

$$\boxed{I_{ab} = 2.05\ \text{A flowing from b to a}}$$

*Check by KCL.* At b: $2.052$ A leaves towards a, $30.597/4 = 7.649$ A leaves through the 4 Ω, and $(30.597 - 50)/2 = -9.701$ A leaves through the 50 V branch (so 9.701 A enters): $2.052 + 7.649 - 9.701 = 0$ ✓. At a: $5.037 + (-2.985) + (-2.052) = 0$ ✓ (through 2 Ω, the 25 V branch, and a-b).

@s 3
Use phasors. $Z_1 = 18 + j24 = 30\angle 53.13^\circ\ \Omega$, $Z_2 = 15 - j30 = 33.54\angle{-63.43}^\circ\ \Omega$, $\bar V = 200\angle 53.8^\circ$ V.

**Branch currents.**

$$\bar I_1 = \frac{\bar V}{Z_1} = \frac{200\angle 53.8^\circ}{30\angle 53.13^\circ} = \mathbf{6.667\angle 0.67^\circ\ A} = 6.667 + j0.078\ \text{A}$$

$$\bar I_2 = \frac{\bar V}{Z_2} = \frac{200\angle 53.8^\circ}{33.54\angle{-63.43^\circ}} = \mathbf{5.963\angle 117.23^\circ\ A} = -2.723 + j5.304\ \text{A}$$

**Total current.**

$$\bar I = \bar I_1 + \bar I_2 = 3.944 + j5.382 = \mathbf{6.667\angle 53.8^\circ\ A}$$

The current is **in phase with the voltage** (both at 53.8°), so the circuit is purely resistive as a whole: $Z_{eq} = 200/6.667 = 30\ \Omega$ (check: $Z_1Z_2/(Z_1 + Z_2) = (30\angle 53.13^\circ)(33.54\angle{-63.43^\circ})/(33 - j6) = 1006.2\angle{-10.3^\circ}/33.54\angle{-10.3^\circ} = 30\angle 0^\circ$ ✓).

**Real power.**

$$P = VI\cos\varphi = 200 \times 6.667 \times \cos 0^\circ = \mathbf{1333\ W}$$

Check, branch by branch: $P_1 = I_1^2R_1 = 6.667^2 \times 18 = 800$ W, $P_2 = I_2^2R_2 = 5.963^2 \times 15 = 533$ W, total $1333$ W ✓. The reactive power cancels, $Q = 6.667^2 \times 24 - 5.963^2 \times 30 = 1067 - 1067 = 0$ var, and the power factor is **unity**.

@s 4
**Definition.** A transformer is a static (stationary) electrical device that transfers electrical energy from one circuit to another by **electromagnetic (mutual) induction**, at the same frequency, usually with a change in voltage (and current) level, without any moving part.

**Operating principle.** It has two windings, the primary (turns $N_1$) and the secondary (turns $N_2$), wound on a common laminated silicon-steel core. When the primary is connected to an AC supply $V_1$, a small magnetising current produces an alternating flux $\Phi$ in the core. The core links both windings, so by Faraday's law the changing flux induces emfs $E_1$ in the primary (it opposes $V_1$: self-induction) and $E_2$ in the secondary (mutual induction). If a load is connected to the secondary, a current $I_2$ flows and the primary draws a corresponding extra current, so power passes from the primary to the secondary ($V_1I_1 \approx V_2I_2$ for an ideal transformer).

```figure caption="Transformer: the alternating flux Φ set up by the primary links the secondary and induces E$_2$."
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

**EMF equation.** Let the flux be $\Phi = \Phi_m\sin\omega t$, $\omega = 2\pi f$. The instantaneous emf induced in a winding of $N$ turns is

$$e = -N\frac{d\Phi}{dt} = -N\omega\Phi_m\cos\omega t = N\omega\Phi_m\sin\left(\omega t - 90^\circ\right)$$

so the peak emf is $E_m = N\omega\Phi_m = 2\pi fN\Phi_m$, and the RMS value is

$$E = \frac{E_m}{\sqrt2} = \frac{2\pi}{\sqrt2}fN\Phi_m \ \Rightarrow\ \boxed{E = 4.44\,f\,N\,\Phi_m}$$

$$\begin{gathered}E_1 = 4.44fN_1\Phi_m \\ E_2 = 4.44fN_2\Phi_m \\ \frac{E_2}{E_1} = \frac{N_2}{N_1} = K\ (\text{transformation ratio})\end{gathered}$$

(For a transformer with a rectangular-wave or other waveform the constant differs, $4.44 = 4 \times$ form factor $1.11$.)

@s 5
Given an ideal transformer: $S = 25$ kVA, $N_1 = 500$, $N_2 = 40$, $V_1 = 3000$ V, $f = 50$ Hz. Transformation ratio $K = N_2/N_1 = 40/500 = 0.08$.

**(i) Full-load currents.** For an ideal transformer $S = V_1I_1 = V_2I_2$ and $V_2 = KV_1 = 0.08 \times 3000 = 240$ V.

$$\begin{gathered}I_1 = \frac{S}{V_1} = \frac{25\,000}{3000} = \mathbf{8.33\ A} \\ I_2 = \frac{S}{V_2} = \frac{25\,000}{240} = \mathbf{104.2\ A}\end{gathered}$$

(Check: $I_2/I_1 = N_1/N_2 = 12.5$ ✓.)

**(ii) Secondary emf.** In an ideal transformer there are no voltage drops, so

$$E_2 = V_2 = \frac{N_2}{N_1}V_1 = \mathbf{240\ V}\quad(E_1 = V_1 = 3000\ \text{V})$$

**(iii) Maximum core flux.** From $E_1 = 4.44fN_1\Phi_m$:

$$\Phi_m = \frac{E_1}{4.44fN_1} = \frac{3000}{4.44 \times 50 \times 500} = 0.02703\ \text{Wb} = \mathbf{27.0\ mWb}$$

(Check from the secondary: $240/(4.44 \times 50 \times 40) = 0.02703$ Wb ✓.)

@s 6
**Definition.** A DC machine is an electromechanical energy converter that converts mechanical energy into direct-current electrical energy (**DC generator**) or direct-current electrical energy into mechanical energy (**DC motor**). The same construction serves for both.

```figure caption="Cross-section of a two-pole DC machine, and the commutator with its brushes (side view)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Rectangle
fig,ax=plt.subplots(figsize=(6.0,3.3)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-3.3,10.6); ax.set_ylim(-3.1,3.1)
ax.add_patch(Wedge((0,0),2.85,0,360,width=0.4,fc="#9aa3b2",ec=INK,lw=1.1))
for sgn in (1,-1):
    ax.add_patch(Rectangle((-0.55,sgn*1.55 if sgn>0 else -2.45),1.1,0.9,fc="#d5dae3",ec=INK,lw=1))
    ax.add_patch(Wedge((0,0),1.62,90*sgn-50 if sgn>0 else 270-50,90*sgn+50 if sgn>0 else 270+50,width=0.3,fc="#1d6fb8" if sgn>0 else "#2e8b57",ec=INK,lw=1,alpha=0.85))
    for dx in (-0.85,0.85):
        ax.add_patch(Rectangle((dx-0.2,sgn*1.6-0.4 if sgn>0 else -2.0),0.4,0.8,fc="#b8860b",ec=INK,lw=0.7))
ax.add_patch(Circle((0,0),1.1,fc="#f6f8fc",ec=INK,lw=1.2))
for a in np.linspace(0,2*np.pi,16,endpoint=False): ax.add_patch(Circle((0.95*np.cos(a),0.95*np.sin(a)),0.07,fc=SERIES[1],ec="none"))
ax.add_patch(Circle((0,0),0.2,fc=INK))
ax.text(0,1.95,"N",color=INK,ha='center',va='center',fontsize=9,fontweight="bold"); ax.text(0,-1.95,"S",color=INK,ha='center',va='center',fontsize=9,fontweight="bold")
# commutator
cx=8.6
ax.add_patch(Circle((cx,0),1.0,fc="#e2b25e",ec=INK,lw=1.2))
for a in np.linspace(0,2*np.pi,12,endpoint=False): ax.plot([cx+0.45*np.cos(a),cx+1.0*np.cos(a)],[0.45*np.sin(a),np.sin(a)],color=INK,lw=0.9)
ax.add_patch(Circle((cx,0),0.45,fc="#f6f8fc",ec=INK,lw=1)); ax.add_patch(Rectangle((cx-0.4,1.0),0.8,0.55,fc="#2a2f3a",ec=INK)); ax.add_patch(Rectangle((cx-0.4,-1.55),0.8,0.55,fc="#2a2f3a",ec=INK))
def lab(txt,xy,xt):
    ax.annotate(txt,xy=xy,xytext=xt,fontsize=7.6,color=INK,arrowprops=dict(arrowstyle="-",color=MUTED,lw=0.8),va="center",ha="left")
lab("yoke (frame)",(2.3,1.6),(3.3,2.8)); lab("pole core + pole shoe",(0.6,1.7),(1.9,2.4))
lab("field winding",(0.85,1.6),(3.3,1.9)); lab("armature core with slots",(1.0,-0.45),(3.0,-1.1)); lab("armature conductors",(0.95,0.1),(3.0,-2.0))
ax.text(cx,-2.15,"commutator segments, mica-insulated",ha='center',fontsize=7.4,color=INK); ax.text(cx,2.0,"carbon brushes",ha='center',fontsize=7.6,color=INK)
```

**Main parts.**

1. **Yoke (frame):** the outer cylindrical casing of cast iron (small machines) or rolled steel (large). It carries the magnetic flux produced by the poles, and gives mechanical support and protection.
2. **Poles and pole shoes:** laminated steel poles bolted to the yoke carry the field winding. The widened **pole shoe** spreads the flux uniformly over the air gap and supports the field coil.
3. **Field winding:** coils of insulated copper wire around the pole cores, that carry the exciting current and set up the main flux. (Connected in shunt, series or compound.)
4. **Armature core:** a cylindrical drum of thin, insulated *silicon-steel laminations* keyed on the shaft, with slots on the outside. The laminations reduce the eddy-current loss.
5. **Armature winding:** copper conductors placed in the slots, joined as lap or wave winding, in which the emf is induced (generator) or the torque is developed (motor).
6. **Commutator:** a cylinder of hard-drawn copper segments, insulated from one another by mica, fixed on the shaft. It converts the alternating emf induced in the armature conductors into unidirectional (DC) voltage in a generator, and reverses the current in the conductors in a motor to keep the torque one-directional.
7. **Brushes and brush gear:** carbon (graphite) blocks held by holders and springs which press on the commutator and conduct current between the rotating armature and the external circuit.
8. **Other parts:** shaft, bearings (ball or roller), end covers/shields, cooling fan, interpoles (commutating poles) and terminal box.

@s 7
**Check the state of the Zener.** Remove the Zener and find the voltage across the 10 kΩ load by voltage division:

$$V_L' = \frac{R_L}{R + R_L}V_{in} = \frac{10}{5 + 10} \times 120 = 80\ \text{V}$$

Since $80\ \text{V} > V_Z = 50$ V, the Zener is in breakdown (**ON**) and clamps the load voltage at $V_Z$.

**(i) Output voltage:**

$$V_o = V_Z = \mathbf{50\ V}$$

**(ii) Voltage drop across the series resistance:**

$$V_R = V_{in} - V_Z = 120 - 50 = \mathbf{70\ V}$$

**(iii) Current through the Zener diode.**

$$\begin{gathered}I = \frac{V_R}{R} = \frac{70}{5\ \text{k}\Omega} = 14\ \text{mA} \\ I_L = \frac{V_o}{R_L} = \frac{50}{10\ \text{k}\Omega} = 5\ \text{mA}\end{gathered}$$

$$\boxed{I_Z = I - I_L = 14 - 5 = 9\ \text{mA}}$$

The power in the Zener is $P_Z = V_ZI_Z = 50 \times 9\ \text{mA} = 450$ mW, so a Zener rated 0.5 W or more is needed (a 1 W diode in practice).

@s 8
**Why "bipolar"?** In a bipolar junction transistor (BJT) the current is carried by **both types of charge carriers**, free electrons (majority in n-type) and holes (majority in p-type), and the device has **two p-n junctions** (emitter-base and collector-base). "Bipolar" refers to this two-carrier conduction, in contrast to the unipolar FET where only one type of carrier (majority) carries the current. It is a three-layer device (npn or pnp): the **emitter** (heavily doped, emits carriers), the **base** (very thin, lightly doped) and the **collector** (moderately doped, largest area, collects carriers).

**Operation of an npn transistor in active mode.** For the active region, the **emitter-base junction is forward biased** and the **collector-base junction is reverse biased** ($V_{BE} \approx 0.7$ V, $V_{CB} > 0$).

```figure caption="npn transistor in the active mode: the forward-biased emitter junction injects electrons into the thin base, and almost all of them are swept into the collector by the reverse-biased collector junction."
fig,ax=ckt_canvas(5.6,3.1,xlim=(-0.6,6.4),ylim=(-2.2,3.0))
from matplotlib.patches import Rectangle
for x,w,c,t in ((0.3,2.0,"#cfe1f5","n  (emitter)"),(2.3,0.6,"#f6d6d4","p (base)"),(2.9,2.4,"#cfe1f5","n  (collector)")):
    ax.add_patch(Rectangle((x,0.6),w,1.5,fc=c,ec=INK,lw=1.2)); label(ax,(x+w/2,2.4),t,size=7.8)
arrow(ax,(1.0,1.45),(4.4,1.45),None,color=SERIES[0],lw=2.0); label(ax,(2.6,1.05),"electrons (≈ 98–99 % reach the collector)",size=7,color=SERIES[0])
arrow(ax,(2.6,0.95),(2.6,0.3),None,color=SERIES[1],lw=1.4); label(ax,(3.45,0.45),"few recombine → I$_B$",size=7,color=SERIES[1])
wire(ax,[(1.3,0.6),(1.3,-0.4)]); wire(ax,[(2.6,0.6),(2.6,-1.5)]); wire(ax,[(4.1,0.6),(4.1,-1.5)])
batt(ax,(1.3,-0.4),(2.6,-0.4),"V$_{BE}$ (forward)",side=-1,off=0.8); node(ax,(2.6,-0.4))
batt(ax,(2.6,-1.5),(4.1,-1.5),"V$_{CB}$ (reverse)",side=-1,off=0.8)
label(ax,(0.1,-0.4),"E",size=8); label(ax,(2.6,-1.95),"B",size=8); label(ax,(4.3,-1.0),"C",size=8)
```

1. **Emitter injection.** The forward bias lowers the barrier at the emitter junction. Because the emitter is heavily doped, a large number of electrons (majority carriers) are injected into the base. A small flow of holes passes from base to emitter, which is negligible. This gives the emitter current $I_E$.
2. **Diffusion through the base.** The base is very thin ($\sim 1\ \mu$m) and lightly doped, so only 1–2% of the electrons recombine with holes there. The recombined holes are replaced from the base supply, giving the small base current $I_B$.
3. **Collection.** The remaining 98–99% of the electrons reach the edge of the collector junction. The reverse-biased junction has a strong field that sweeps them into the collector, so the collector current is $I_C = \alpha I_E$ with $\alpha = 0.98$–$0.99$.

$$\begin{gathered}I_E = I_B + I_C \\ I_C = \alpha I_E = \beta I_B \\ \alpha = \frac{\beta}{1 + \beta} \\ \beta = \frac{\alpha}{1 - \alpha}\end{gathered}$$

For example, $\alpha = 0.99$ gives $\beta = 99$. A small change in the base current therefore controls a large change in the collector current: the transistor amplifies. (For a pnp transistor, holes play the role of electrons and all polarities are reversed.)

@s 9
**Importance of protective devices in residential installation.**

- A fault current (short circuit) can be hundreds of times the rated current, and an overload heats the cable insulation. Either can start a **fire**; a protective device cuts the supply within milliseconds to seconds.
- They protect **people** from electric shock when insulation fails or a live wire is touched (earth-leakage protection); even a current of 30 mA through the body can be fatal.
- They protect **appliances and wiring** (TV, refrigerator, computers) from overload, overvoltage, lightning and switching surges, saving the cost of replacement.
- They **isolate only the faulty circuit**, so the rest of the house stays supplied; they also satisfy the electrical code and insurance requirements.

**Types of protective devices.**

| Device | Function and working |
|---|---|
| **Fuse** | A low-melting wire (tin-lead, copper) in series with the circuit melts when $I > I_{rated}$. Types: rewirable (kit-kat), cartridge, HRC. Cheap; the element must be replaced after operating. |
| **MCB** | Miniature circuit breaker: bimetallic strip trips on overload, solenoid trips instantly on short circuit; resettable; ratings 6–63 A, with B, C and D curves. |
| **MCCB** | Moulded-case circuit breaker, same principle but for larger currents (up to 1600 A) with adjustable settings; used at the main board. |
| **ELCB / RCCB (RCD)** | Residual-current device: compares the phase and neutral currents; if the difference (leakage to earth) exceeds 30 mA it trips in about 30 ms. Prevents electric shock and earth-fault fires. |
| **Surge protector / lightning arrester** | A metal-oxide varistor (or spark gap) clamps high-voltage transients and diverts them to earth. |
| **Earthing (grounding)** | Gives a low-resistance path for the fault current so that the above devices operate, and keeps metal bodies at earth potential. |
| **Relays / voltage protectors** | Disconnect appliances (refrigerator, air conditioner) on over/under voltage or phase failure. |

@s 10
Any two are required; all three are answered.

**(a) Types of electrical wiring systems.**

1. *Cleat wiring:* PVC or VIR cables are supported on porcelain cleats; temporary, cheap, easy to inspect; unsafe and unsightly.
2. *Casing-capping wiring:* cables run in parallel grooves of a wooden or PVC casing and covered by a capping; neat and cheap but a fire risk (wood), and not for damp places.
3. *Batten wiring:* insulated cables clipped to wooden battens on the walls or ceiling; low cost, but poor appearance, limited life.
4. *Conduit wiring:* cables drawn through PVC or GI conduit fixed on the surface (**surface conduit**) or buried in the wall or slab (**concealed conduit**); gives mechanical protection and safety against moisture and fire, long life and a good appearance. It is the standard system in modern buildings but is costly.
5. *Lead-sheathed (CTS/TRS) wiring:* cables with a tough rubber or lead sheath clipped to walls; suitable for damp places, rarely used now.

*By circuit arrangement:* the **radial** (each final sub-circuit fed from the distribution board), the **ring** (sockets in a loop) and the **loop-in/joint-box (tree)** systems.

**(b) Electrical safety rules.**

- Switch off and isolate the supply, and test with a tester, before any work; lock and tag the switch.
- Use approved cables, plugs and sockets; wire the switch and fuse/MCB in the phase conductor; use a proper rated MCB/RCCB, never a copper-wire fuse substitute.
- Earth all metal enclosures and use three-pin plugs; check the earth resistance periodically.
- Do not touch electrical devices with wet hands or work in a wet place; keep water away from sockets.
- Avoid overloading sockets; do not use damaged or poorly joined wires and keep joints insulated.
- Use insulated tools, rubber gloves and boots; keep the ladder, rods and kites away from overhead lines.
- Never touch a victim of electric shock directly: switch off the supply or push the person off with an insulator, then give first aid (CPR) and call a doctor. Use CO₂/dry-powder extinguishers on electrical fires, not water.

**(c) Ex-OR and Ex-NOR gates.**

*Exclusive-OR (XOR)*: the output is 1 when the inputs are **different** (an odd number of 1s): $Y = A\oplus B = A\bar B + \bar AB$.

*Exclusive-NOR (XNOR)*: the output is 1 when the inputs are the **same**: $Y = \overline{A\oplus B} = A\odot B = AB + \bar A\bar B$.

```figure caption="Symbols of the XOR and XNOR gates."
fig,ax=plt.subplots(figsize=(4.8,1.6)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1,10.6); ax.set_ylim(-1.0,1.0)
gate(ax,"XOR",0.2,0.0,w=1.8,h=1.2,lead=0.8,labels=["A","B","Y"])
gate(ax,"XNOR",6.0,0.0,w=1.8,h=1.2,lead=0.8,labels=["A","B","Y"])
ax.text(1.5,-0.95,"XOR  Y = A ⊕ B",ha='center',fontsize=8,color=MUTED); ax.text(7.4,-0.95,"XNOR  Y = (A ⊕ B)′",ha='center',fontsize=8,color=MUTED)
```

| $A$ | $B$ | XOR $A\oplus B$ | XNOR $\overline{A\oplus B}$ |
|---|---|---|---|
| 0 | 0 | 0 | 1 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |

*Applications:* the XOR gate is the sum bit of a half adder ($S = A\oplus B$, carry $= AB$), and is used in parity generators and checkers, binary comparators, controlled inverters and encryption; the XNOR gate is used as an *equality detector* (a one-bit comparator).

