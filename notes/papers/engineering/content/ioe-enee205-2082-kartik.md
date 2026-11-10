---
file: NEBians-IOE-Past-Paper-Power-System-Analysis-I-ENEE205-2082-Kartik.pdf
subject: Power System Analysis I
level: BE · Year II / Part I
code: ENEE 205
year_bs: 2082 Kartik
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE Electrical Engineering (BEL), Year II / Part I. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
(a) What are differences between conventional and non-conventional sources of energy? Draw a schematic diagram of one of the power generating stations with non-conventional sources. [[2+4]]

(b) An insulator string for 66 kV line has 4 discs. The shunt capacitance between each joint and metal work is 10% of the capacitance of each disc. Find the voltage across the different discs and string efficiency. [[6]]

@q 2
(a) A voltage source $E_{an} = -120\angle 210^\circ$ V and the current through the source $I_{na} = 10\angle 60^\circ$ A. Find the values of real power (P) and reactive power (Q) and state whether the source is delivering or receiving each. [[4]]

(b) Figure below shows a single line diagram power system. Draw its impedance diagram without showing their values. Also, redraw the circuit with per unit values in the reactance diagram. Take 5,000 VA base and common system base voltage of 250 V. [[2+6]]

Single-line diagram: generator G1 (2000 VA, 250 V, Z = j0.2 p.u.) and generator G2 (2000 VA, 250 V, Z = j0.3 p.u.) are connected to a common bus. The bus feeds transformer T1 (4000 VA, 250/800 V, Z = j0.2 p.u.), then the line (Z = 40 + j150 Ω), then transformer T2 (8000 VA, 1000/500 V, Z = j0.06 p.u.), which supplies the load.

@q 3
(a) What do you mean by skin effect? Clarify it on the basis of AC current and DC current. [[4]]

(b) A 3-phase single circuit bundled conductor line with three sub conductors per phase has a horizontal configuration with spacing of 6.1 m between the center lines of adjacent phases as shown in figure. The distance between the sub conductors of each phase is 30.5 cm and each sub conductors has a diameter of 2.54 cm. Find the inductance per phase per km. [[8]]

Figure: each phase has three sub-conductors at the corners of a triangle of side 30.5 cm; the three phase centres are in a horizontal row, 6.1 m apart (12.2 m between the outer phases).

@q 4
(a) Classify transmission line model. Find A, B, C, D parameters of short transmission line and also draw its phasor diagram with lagging and leading power factor of the load. [[2+4]]

(b) A 3-phase 132 kV, 50 Hz overhead line delivers 50 MVA and pf 0.8 lagging at its receiving end. The constant of the line are $A = 0.98\angle 3^\circ$ and $B = 110\angle 75^\circ\ \Omega$ phase. Find (i) sending end voltage and power angle (ii) sending end active and reactive power (iii) line losses. [[6]]

@q 5
(a) Why do transmission line perform as source and sink of reactive power? What are their effects on power system? [[3+3]]

(b) A 3-phase, 50 Hz 100 km long overhead line has the following line constants: resistance per phase per km = 0.153 Ω, inductance per phase per km = 1.21 mH, Capacitance per phase per km = 0.00958 μF. The line supplies a load of 20 MW at 0.9 power factor lagging at a line voltage of 110 kV at the receiving end. Calculate the regulation and efficiency. [[6]]

<!-- SOLUTIONS -->

@s 1
**(a) Conventional and non-conventional sources of energy.**

| Point | Conventional sources | Non-conventional (renewable) sources |
|---|---|---|
| Nature | Finite, exhaustible: coal, oil, natural gas, uranium, large hydro | Naturally replenished: sun, wind, small hydro, biomass, geothermal, tides |
| Environment | CO$_2$, SO$_x$, NO$_x$, ash, reservoir and fuel-cycle damage | Little or no emission during operation |
| Energy density, output | High, steady, controllable, base-load | Low density, intermittent (weather, day-night), needs storage or back-up |
| Capital / running cost | Moderate capital, fuel cost recurring | High capital (per kW), almost zero fuel cost |
| Size | Large central stations (hundreds of MW) | Small, modular, distributed (kW to tens of MW) |
| Technology | Mature | Newer, fast developing |

**Schematic of a non-conventional plant (grid-connected solar photovoltaic plant).** Sunlight falls on the PV array; the DC output is collected by the combiner box, converted to AC by the inverter, stepped up by the transformer, and fed to the grid through the switchyard.

```figure caption="Question 1(a): block schematic of a grid-connected solar photovoltaic power plant."
fig,ax=flow([("PV array","sunlight to DC"),("Combiner","DC cables, fuses"),("Inverter","DC to AC, MPPT"),("Step-up Tx","0.4 / 11 / 33 kV"),("Grid","switchyard, meter")],figsize=(6.4,1.9))
```

**(b) String efficiency of a 4-disc string.** Number the discs 1 to 4 from the cross-arm (earthed) end; let $C$ be the capacitance of each disc and $kC$ ($k = 0.1$) the shunt capacitance of each joint to the metal work (earth). $V_1, \dots, V_4$ are the voltages across the discs and $V$ is the phase voltage.

$$V = \frac{66}{\sqrt{3}} = 38.105\ \text{kV}$$

Joint A (between discs 1 and 2): the current in disc 2 equals the current in disc 1 plus the leakage current to earth through $kC$:

$$V_2 = V_1 + kV_1 = V_1(1+k) = 1.1\,V_1$$

Joint B (between discs 2 and 3): $I_3 = I_2 + i_B$, with $i_B = k\,\omega C\,(V_1 + V_2)$:

$$V_3 = V_2 + k(V_1+V_2) = V_1(1 + 3k + k^2) = 1.31\,V_1$$

Joint C (between discs 3 and 4): $V_4 = V_3 + k(V_1+V_2+V_3) = V_1(1 + 6k + 5k^2 + k^3) = 1.651\,V_1$.

The sum of the four disc voltages is the phase voltage:

$$V_1(1 + 1.1 + 1.31 + 1.651) = 5.061\,V_1 = 38.105\ \text{kV} \quad\Rightarrow\quad V_1 = 7.529\ \text{kV}$$

| Disc (from earth end) | Multiple of $V_1$ | Voltage (kV) |
|---|---|---|
| 1 | 1.000 | **7.53** |
| 2 | 1.100 | **8.28** |
| 3 | 1.310 | **9.86** |
| 4 (next to the line) | 1.651 | **12.43** |

$$\text{String efficiency} = \frac{V}{n\,V_4} = \frac{38.105}{4 \times 12.431} = 0.766 = \mathbf{76.6\,\%}$$

```figure caption="Question 1(b): voltage across each disc of the 4-disc, 66 kV string (the disc nearest the line carries 12.43 kV, the one nearest the cross-arm only 7.53 kV)."
fig,ax=plt.subplots(figsize=(5.2,2.4))
v=[7.529,8.282,9.863,12.431]
b=ax.bar(["Disc 1\n(earth end)","Disc 2","Disc 3","Disc 4\n(line end)"],v,color=[SERIES[0]]*3+[SERIES[1]],width=0.55)
ax.axhline(38.105/4,color=MUTED,ls="--",lw=1); ax.text(3.45,38.105/4+0.3,"ideal 9.53 kV",ha="right",fontsize=8,color=MUTED)
for r,x in zip(b,v): ax.text(r.get_x()+r.get_width()/2,x+0.25,f"{x:.2f} kV",ha="center",fontsize=8)
ax.set_ylim(0,15); ax.set_ylabel("voltage (kV)",fontsize=8.5); ax.tick_params(labelsize=8)
for s in ("top","right"): ax.spines[s].set_visible(False)
```

@s 2
**(a) Real and reactive power of the source.** The current $I_{na}$ flows from $n$ to $a$ through the source, that is it leaves the source at its positive terminal $a$ (voltage $E_{an}$ of $a$ with respect to $n$). With this (generator) convention the complex power delivered by the source is $S = E_{an}\,I_{na}^{*}$.

$$\begin{gathered}E_{an} = -120\angle 210^\circ = 120\angle 30^\circ\ \text{V} \\ I_{na} = 10\angle 60^\circ\ \text{A}\end{gathered}$$

$$S = E_{an}I_{na}^{*} = (120\angle 30^\circ)(10\angle -60^\circ) = 1200\angle -30^\circ = 1039.2 - j600\ \text{VA}$$

$$\begin{gathered}P = 1200\cos 30^\circ = \mathbf{1039.2\ W} \\ Q = 1200\sin(-30^\circ) = \mathbf{-600\ var}\end{gathered}$$

$P > 0$: the source **delivers** 1039.2 W of real power. $Q < 0$: the source **receives (absorbs)** 600 var of reactive power, because its current leads its voltage by $30^\circ$ (a capacitive-type load on the source).

**(b) Impedance diagram and per-unit reactance diagram.**

*Impedance diagram (no values):* each machine becomes its emf behind its impedance, each transformer its series impedance (magnetising branch neglected), the line its series $R + jX$, and the load an impedance to the neutral.

```figure caption="Question 2(b): impedance diagram (symbols only). G1 and G2 are in parallel on the bus; T1, the line and T2 are in series; the load is shown as Z_L."
fig,ax=ckt_canvas(6.4,2.9)
wire(ax,[(0.2,0),(11.6,0)])
for x,n in ((1.0,"G1"),(2.8,"G2")):
    vsrc(ax,(x,0),(x,1.0),"E$_{%s}$"%n,side=-1,off=0.85); res(ax,(x,1.0),(x,2.6),"Z$_{%s}$"%n,side=1,body=1.0)
wire(ax,[(1.0,2.6),(3.4,2.6)]); node(ax,(2.8,2.6)); node(ax,(3.4,2.6))
res(ax,(3.4,2.6),(5.1,2.6),"Z$_{T1}$",side=1,body=1.0); res(ax,(5.1,2.6),(7.2,2.6),"Z$_{line}$",side=1,body=1.0); res(ax,(7.2,2.6),(8.9,2.6),"Z$_{T2}$",side=1,body=1.0)
wire(ax,[(8.9,2.6),(11.0,2.6)]); res(ax,(11.0,2.6),(11.0,0),"Z$_L$",side=1,body=1.2); node(ax,(11.0,2.6))
label(ax,(3.4,3.35),"bus",size=8)
```

*Per-unit values.* $S_{base} = 5000$ VA. Common base voltage 250 V in the generator zone. The base voltage of the other zones follows the transformer ratios:

$$\begin{gathered}V_{base,line} = 250 \times \frac{800}{250} = 800\ \text{V} \\ V_{base,load} = 800 \times \frac{500}{1000} = 400\ \text{V}\end{gathered}$$

(The line side of T2 is rated 1000 V, not 800 V, so T2 needs a voltage correction.) The line base impedance is

$$Z_{base,line} = \frac{800^2}{5000} = 128\ \Omega$$

New per-unit values, $Z_{new} = Z_{old}\,\dfrac{S_{base,new}}{S_{base,old}}\left(\dfrac{V_{rated}}{V_{base}}\right)^2$:

| Element | Calculation | p.u. |
|---|---|---|
| G1 | $0.2 \times 5000/2000 \times (250/250)^2$ | **j0.500** |
| G2 | $0.3 \times 5000/2000 \times (250/250)^2$ | **j0.750** |
| T1 | $0.2 \times 5000/4000 \times (250/250)^2$ | **j0.250** |
| Line | $(40 + j150)/128$ | **0.3125 + j1.1719** (reactance j1.1719) |
| T2 | $0.06 \times 5000/8000 \times (1000/800)^2 = 0.06 \times 0.625 \times 1.5625$ | **j0.0586** |

The load is shown without a value in the question, so it is left as $Z_L$ (its per-unit value would be found with base 400 V: $Z_{base,load} = 400^2/5000 = 32\ \Omega$).

```figure caption="Question 2(b): per-unit reactance diagram on 5000 VA. The line resistance (0.3125 p.u.) is neglected in the reactance diagram; E_G1 and E_G2 are the generator emfs."
fig,ax=ckt_canvas(6.4,2.9)
wire(ax,[(0.2,0),(11.6,0)])
for x,n,v in ((1.0,"G1","j0.5"),(2.8,"G2","j0.75")):
    vsrc(ax,(x,0),(x,1.0),"E$_{%s}$"%n,side=-1,off=0.85); ind(ax,(x,1.0),(x,2.6),v,side=1,body=1.0)
wire(ax,[(1.0,2.6),(3.4,2.6)]); node(ax,(2.8,2.6)); node(ax,(3.4,2.6))
ind(ax,(3.4,2.6),(5.1,2.6),"j0.25",side=1,body=1.0); ind(ax,(5.1,2.6),(7.2,2.6),"j1.172",side=1,body=1.0); ind(ax,(7.2,2.6),(8.9,2.6),"j0.0586",side=1,body=1.0)
wire(ax,[(8.9,2.6),(11.0,2.6)]); label(ax,(10.3,3.2),"to load",size=8)
label(ax,(2.2,-0.7),"zone 250 V",size=7.5); label(ax,(6.1,-0.7),"zone 800 V",size=7.5); label(ax,(10.2,-0.7),"zone 400 V",size=7.5)
```

@s 3
**(a) Skin effect.** When a conductor carries alternating current, the current is not distributed uniformly over the cross-section: it crowds towards the outer surface (the "skin") and the centre carries much less current.

*Reason.* The alternating current produces an alternating flux, linking the conductor both inside and outside. Filaments near the centre are linked by more flux than filaments near the surface, so they have a larger inductance and reactance. The central filaments therefore carry less current, and the current density is highest at the surface (eddy currents induced in the conductor oppose the current at the centre and aid it at the surface).

*AC versus DC.* For DC the flux is constant, no emf is induced, and the current density is uniform, so $R_{dc} = \rho l/A$ with the whole area used. For AC the effective area is smaller, so $R_{ac} > R_{dc}$ (the ratio $R_{ac}/R_{dc}$ is the skin-effect factor).

The skin effect increases with: conductor diameter, frequency, permeability and conductivity of the material. The skin depth is $\delta = \sqrt{2/(\omega\mu\sigma)}$ (about 9.3 mm in copper at 50 Hz). It is why large conductors are stranded or made hollow and why ACSR (steel core carrying no useful current) is used.

**(b) Inductance of the bundled line.** Sub-conductor radius $r = 2.54/2 = 1.27$ cm, so

$$r' = 0.7788\,r = 0.7788 \times 0.0127 = 0.009891\ \text{m}$$

*GMR of one bundle* (three sub-conductors at the corners of an equilateral triangle of side $d = 0.305$ m):

$$D_s^{b} = \left(r'\,d\,d\right)^{1/3} = \left(0.009891 \times 0.305^2\right)^{1/3} = \left(9.2009\times10^{-4}\right)^{1/3} = 0.09726\ \text{m}$$

*GMD between phases* (horizontal, 6.1 m, 6.1 m, 12.2 m; the bundle dimension is small and the centre-to-centre distance is used):

$$D_{eq} = \left(6.1 \times 6.1 \times 12.2\right)^{1/3} = 7.686\ \text{m}$$

*Inductance per phase:*

$$L = 2\times10^{-7}\ln\frac{D_{eq}}{D_s^{b}}\ \text{H/m} = 2\times10^{-7}\ln\frac{7.686}{0.09726}= 2\times10^{-7}\times 4.370$$

$$L = 8.74\times10^{-7}\ \text{H/m} = \mathbf{0.874\ mH/km\ per\ phase}$$

(reactance $X_L = 2\pi \times 50 \times 0.874\times10^{-3} = 0.275\ \Omega$/km). A single conductor of the same radius would give about 1.3 mH/km, so bundling cuts the inductance by about one third.

```figure caption="Question 3(b): geometry of the bundled line (three sub-conductors per phase at the corners of a 30.5 cm triangle, phases 6.1 m apart; not to scale)."
fig,ax=plt.subplots(figsize=(6.2,2.2))
for i,(x0,n) in enumerate(((0,"a"),(6.1,"b"),(12.2,"c"))):
    ps=[(x0-0.15,0),(x0+0.15,0),(x0,0.26)]
    for p in ps: ax.add_patch(Circle(p,0.07,fc="white",ec=ACCENT,lw=1.4))
    ax.text(x0,0.55,"phase "+n,ha="center",fontsize=9)
ax.annotate("",xy=(0,-0.35),xytext=(6.1,-0.35),arrowprops=dict(arrowstyle="<->",color=MUTED)); ax.text(3.05,-0.6,"6.1 m",ha="center",fontsize=8.5)
ax.annotate("",xy=(6.1,-0.35),xytext=(12.2,-0.35),arrowprops=dict(arrowstyle="<->",color=MUTED)); ax.text(9.15,-0.6,"6.1 m",ha="center",fontsize=8.5)
ax.text(0,-0.18,"d = 30.5 cm",ha="center",fontsize=7.5,color=MUTED)
ax.set_xlim(-1,13.2); ax.set_ylim(-0.9,0.9); ax.set_aspect("auto"); ax.axis("off")
```

@s 4
**(a) Classification of transmission line models.**

| Class | Length | Model | Capacitance |
|---|---|---|---|
| Short | up to about 80 km (below 69 kV or so) | series $R + jX$ only | neglected |
| Medium | 80 to 250 km | nominal $\pi$ or nominal T (lumped $Y$) | lumped |
| Long | above 250 km | distributed parameters (hyperbolic equations) | uniformly distributed |

**ABCD constants of a short line.** With $Z = R + jX$ the whole series impedance, the sending and receiving currents are equal ($I_S = I_R$):

$$\begin{gathered}V_S = V_R + Z\,I_R \\ I_S = I_R\end{gathered}$$

Comparing with $V_S = AV_R + BI_R$, $I_S = CV_R + DI_R$:

$$\boxed{A = 1,\quad B = Z,\quad C = 0,\quad D = 1}$$

(and $AD - BC = 1$, as required for a passive reciprocal network).

*Phasor diagrams.* Take $V_R$ as reference. For a lagging load the current $I_R$ lags $V_R$ by $\varphi_R$; $I_RR$ is in phase with $I_R$ and $I_RX$ leads it by $90^\circ$; $V_S = V_R + I_RR + jI_RX$ is larger than $V_R$ (positive regulation). For a strongly leading load, $I_R$ leads $V_R$ and $V_S < V_R$ (negative regulation, the Ferranti-type rise at the receiving end).

```figure caption="Question 4(a): phasor diagrams of the short line. Left: lagging power factor, V_S larger than V_R. Right: strongly leading power factor, V_S smaller than V_R."
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.4,2.8))
def ph(ax,deg,title):
    a=np.radians(deg); u=np.array([np.cos(a),np.sin(a)])
    VR=np.array([3.0,0.0]); IRd=u*0.55; jIX=np.array([-u[1],u[0]])*1.1
    P1=VR+IRd; P2=P1+jIX; Iv=u*2.0
    def arr(p,q,c): ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="-|>",color=c,lw=1.6))
    arr((0,0),VR,INK); arr(VR,P1,SERIES[2]); arr(P1,P2,SERIES[3]); arr((0,0),P2,SERIES[1]); arr((0,0),Iv,ACCENT)
    ax.text(VR[0]-0.3,-0.3,"V$_R$",fontsize=9,color=INK)
    ax.text(P2[0]+0.05,P2[1]+0.08,"V$_S$",fontsize=9,color=SERIES[1])
    ax.text(Iv[0]-0.15,Iv[1]+0.15,"I$_R$",fontsize=9,color=ACCENT)
    ax.text(VR[0]+0.3,VR[1]+IRd[1]/2-0.35,"I$_R$R",fontsize=8,color=SERIES[2])
    ax.text(P1[0]+jIX[0]/2+0.1,P1[1]+jIX[1]/2-0.3,"jI$_R$X",fontsize=8,color=SERIES[3])
    ax.set_title(title,fontsize=9); ax.set_xlim(-0.2,4.8); ax.set_ylim(-1.3,2.3); ax.set_aspect("equal"); ax.axis("off")
ph(a1,-30,"lagging pf"); ph(a2,60,"leading pf")
```

**(b) Sending-end quantities.** Per phase receiving-end values:

$$\begin{gathered}V_R = \frac{132\times10^3}{\sqrt3} = 76.21\ \text{kV}\angle 0^\circ \\ I_R = \frac{50\times10^6}{\sqrt3\times132\times10^3} = 218.7\ \text{A},\ \ \varphi_R = \cos^{-1}0.8 = 36.87^\circ\end{gathered}$$

$$I_R = 218.7\angle -36.87^\circ\ \text{A}$$

**(i) Sending-end voltage and power angle.**

$$V_S = AV_R + BI_R = (0.98\angle3^\circ)(76210) + (110\angle75^\circ)(218.7\angle-36.87^\circ)$$

$$= 74.69\angle3^\circ + 24.06\angle38.13^\circ\ \text{kV} = (74.59 + j3.91) + (18.93 + j14.85)\ \text{kV}$$

$$V_S = 93.52 + j18.76 = 95.37\angle 11.35^\circ\ \text{kV (per phase)}$$

$$\boxed{V_{S(line)} = \sqrt3 \times 95.37 = 165.2\ \text{kV},\qquad \delta = 11.35^\circ}$$

**(ii) Sending-end power.** A passive line has $AD - BC = 1$. The paper gives only A and B, so the line is taken as symmetrical, $D = A = 0.98\angle3^\circ$; then

$$C = \frac{AD - 1}{B} = \frac{0.9604\angle6^\circ - 1}{110\angle75^\circ} = 0.9996\times10^{-3}\angle 39.08^\circ\ \text{S}$$

$$I_S = CV_R + DI_R = 76.2\angle39.08^\circ + 214.3\angle(3^\circ-36.87^\circ) = 247.6\angle-16.76^\circ\ \text{A}$$

The angle between $V_S$ and $I_S$ is $11.35^\circ + 16.76^\circ = 28.11^\circ$ (sending-end power factor $\cos28.11^\circ = 0.882$ lagging):

$$S_S = 3\,V_SI_S^{*} = 3(95.37\times10^3)(247.6)\angle 28.11^\circ = 62.49 + j33.38\ \text{MVA}$$

$$\boxed{P_S = 62.5\ \text{MW}, \qquad Q_S = 33.4\ \text{MVAr}}$$

**(iii) Line losses.** The receiving-end power is $S_R = 50(0.8 + j0.6) = 40 + j30$ MVA, so

$$\begin{gathered}P_{loss} = 62.49 - 40 = \mathbf{22.5\ MW} \\ Q_{loss} = 33.38 - 30 = \mathbf{3.38\ MVAr}\end{gathered}$$

Efficiency $= 40/62.49 = 64.0\,\%$. (The loss is very large because the data $|A| = 0.98$, $B = 110\angle75^\circ\ \Omega$ imply a large charging current in a symmetrical line; it is the result implied by the given constants.) The power-circle equation $P_S = \dfrac{|D||V_S|^2}{|B|}\cos(\beta-\alpha) - \dfrac{|V_S||V_R|}{|B|}\cos(\beta+\delta)$ per phase gives the same result.

@s 5
**(a) A transmission line as a source and as a sink of reactive power.** A line has a series inductance $L$ and a shunt capacitance $C$ per unit length.

- The shunt capacitance is charged by the line voltage and **generates** reactive power $Q_C = V^2\omega C = V^2/X_C$ (independent of the load, proportional to $V^2$).
- The series inductance **absorbs** reactive power $Q_L = I^2\omega L = I^2X_L$ (proportional to $I^2$, that is, to the load).

The net reactive power of the line is $Q_C - Q_L$:

- **Light load (current below the surge-impedance-loading current):** $Q_C > Q_L$, the line behaves as a **source** (a capacitor) of reactive power and its receiving-end voltage rises (Ferranti effect).
- **Heavy load (above SIL):** $Q_L > Q_C$, the line is a **sink** (an inductor) and the voltage falls.
- **At SIL**, $P = V^2/Z_c$ with $Z_c = \sqrt{L/C}$, the two are equal, the voltage profile is flat and no reactive power flows in the line.

*Effects on the power system:*

1. Overvoltage at light load (long EHV lines): insulation stress, transformer saturation, harmonics.
2. Voltage drop at heavy load, possibly voltage collapse.
3. Reactive power must flow from the generators through the line, giving extra $I^2R$ loss and reducing the real power the line can carry (thermal and voltage limits).
4. Generators and transformers must be over-sized, and the stability margin falls.
5. Voltage control needs compensation: shunt reactors (light load), shunt capacitors (heavy load), SVC/STATCOM, synchronous condensers, tap-changing transformers, series capacitors.

```figure caption="Question 5(a): voltage along a 300 km lossless line (sending end held at 1.0 p.u., unity-power-factor load of 0, 1 and 1.5 times SIL): the voltage swells at light load and sags at heavy load."
fig,ax=plt.subplots(figsize=(5.4,2.7))
beta=2*np.pi/6000.0; d=300.0; x=np.linspace(0,d,200)
for k,c,l in ((0,SERIES[1],"no load (line is a source of vars)"),(1,SERIES[2],"SIL (flat)"),(1.5,SERIES[0],"1.5 SIL (line is a sink of vars)")):
    VR=1/np.sqrt(np.cos(beta*d)**2+k**2*np.sin(beta*d)**2); s=d-x
    ax.plot(x,VR*np.sqrt(np.cos(beta*s)**2+k**2*np.sin(beta*s)**2),color=c,lw=1.8,label=l)
ax.set_xlabel("distance from sending end (km)",fontsize=8.5); ax.set_ylabel("|V| (p.u.)",fontsize=8.5); ax.legend(fontsize=7.5,loc="center left"); ax.tick_params(labelsize=8); ax.grid(color=GRID,lw=0.6)
```

**(b) Regulation and efficiency of the 100 km line** (nominal $\pi$ model, the usual choice for 80 to 250 km; the capacitance cannot be ignored at 110 kV). Total values for 100 km:

$$\begin{gathered}R = 0.153\times100 = 15.3\ \Omega \\ X_L = 2\pi(50)(1.21\times10^{-3})(100) = 38.01\ \Omega\end{gathered}$$

$$\begin{gathered}Z = 15.3 + j38.01 = 40.98\angle68.08^\circ\ \Omega \\ Y = j\omega C = j2\pi(50)(0.00958\times10^{-6})(100) = j3.010\times10^{-4}\ \text{S}\end{gathered}$$

$$\frac{YZ}{2} = \frac{(3.010\times10^{-4}\angle90^\circ)(40.98\angle68.08^\circ)}{2} = 0.006167\angle158.08^\circ = -0.005717 + j0.002312$$

$$A = D = 1 + \frac{YZ}{2} = 0.99428 + j0.00231 = 0.9943\angle0.133^\circ$$

$$\begin{gathered}B = Z = 40.98\angle68.08^\circ\ \Omega \\ C = Y\left(1 + \frac{YZ}{4}\right) = 3.001\times10^{-4}\angle90.07^\circ\ \text{S}\end{gathered}$$

*Receiving end (per phase):*

$$\begin{gathered}V_R = \frac{110}{\sqrt3} = 63.51\ \text{kV} \\ I_R = \frac{20\times10^6}{\sqrt3\,(110\times10^3)(0.9)} = 116.6\ \text{A}\ \ \Rightarrow\ \ I_R = 116.6\angle-25.84^\circ\ \text{A}\end{gathered}$$

*Sending end:*

$$V_S = AV_R + BI_R = 63.15\angle0.133^\circ\ \text{kV} + 4.778\angle42.24^\circ\ \text{kV} = 66.77\angle2.88^\circ\ \text{kV (phase)} \ \ \Rightarrow\ \ V_{S(line)} = 115.6\ \text{kV}$$

$$I_S = CV_R + DI_R = 109.0\angle-16.65^\circ\ \text{A}$$

*Regulation.* At no load ($I_R = 0$), the receiving-end voltage is $V_{R,NL} = V_S/A = 66.77/0.9943 = 67.15$ kV (phase):

$$\text{Regulation} = \frac{|V_{R,NL}| - |V_{R,FL}|}{|V_{R,FL}|} \times 100 = \frac{67.15 - 63.51}{63.51}\times100 = \mathbf{5.74\,\%}$$

*Efficiency.* The sending-end power is

$$P_S = 3|V_S||I_S|\cos(2.88^\circ + 16.65^\circ) = 3(66.77\times10^3)(109.0)(0.9424) = 20.58\ \text{MW}$$

$$\eta = \frac{P_R}{P_S}\times100 = \frac{20}{20.58}\times100 = \mathbf{97.2\,\%}$$

(line loss $0.58$ MW; with the nominal T model the results are 5.72 % and 97.16 %, essentially the same, which confirms the accuracy of the approximation.) All numbers were evaluated with complex arithmetic in Python.
