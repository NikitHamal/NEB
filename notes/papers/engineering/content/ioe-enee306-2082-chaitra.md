---
file: NEBians-IOE-Past-Paper-Electric-Machine-Design-ENEE306-2082-Chaitra.pdf
subject: Electric Machine Design
level: BE · Year III / Part I
code: ENEE 306
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular paper (new course), BE Electrical Engineering (BEL), Year III / Part I. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt All questions · The figures in the margin indicate Full Marks · Assume suitable data if necessary</small>

@q 1
(a) Differentiate between soft magnetic materials and hard magnetic materials in brief with necessary diagrams. [[4]]

(b) What is ageing of core of electrical machine? What are the advantages and disadvantages of adding silicon with iron? [[4]]

@q 2
(a) Define hot spot in relation to electrical machine. Taking the example of a plate of thickness $t$ derive the necessary expression of temperature of the hottest spot. [[5]]

(b) A 40 kVA, 11000/400 V, 3-phase transformer is working in an ambient temperature of 35 °C on full load. Its oil temperature is recorded as follows:

- 59 °C after 1.5 hours
- 71 °C after 3 hours

Its full-load copper losses are 2 times the iron losses. Calculate: (i) heating time constant, (ii) final steady temperature rise, (iii) 1-hour rating. [[4]]

@q 3
(a) For a 500 kVA, 50 Hz, 6600/400 V, single phase core type, oil immersed, natural cooled power transformer, the design parameters are:

| Parameter | Value |
|---|---|
| Constant for output voltage per turn ($K$) | 0.8 |
| Resistivity of copper | 0.021 Ω-mm²/m |
| Maximum flux density in core ($B_m$) | 1.5 Wb/m² |
| Current density | 2.75 A/mm² |
| Core type | Cruciform |
| Window space factor ($k_w$) | 0.27 |
| Stacking factor ($K_i$) | 0.9 |
| Ratio of height to width of windows ($H_w/W_w$) | 2.5 |
| Ratio of yoke height to width ($H_y/D_y$) | 1 |
| Axial depth of LV winding | 402 mm |
| Axial depth of HV winding | 377.5 mm |
| Inside diameter of LV winding | 310 mm |
| Outside diameter of LV winding | 348 mm |
| Inside diameter of HV winding | 360 mm |
| Outside diameter of HV winding | 418 mm |
| Iron loss | 1460 W |
| Copper loss | 3865 W at full load |
| Height of tank | 1.6 m |
| Length of tank | 1.05 m |
| Width of tank | 0.62 m |

Find the temperature rise. If the mean rise of oil is not to rise 35 °C, find the necessary number of tubes and show its arrangement. [[16]]

(b) Compare power transformer with distribution transformer. [[3]]

@q 4
(a) What are the factors that must be considered while selecting the length of air gap in induction motor? [[6]]

(b) For a 2.2 kW, 440 V, 3-phase, 50 Hz, 1430 rpm squirrel cage induction motor having efficiency of 0.8 and p.f. 0.85 designed for its best power factor. Given $B_{av} = 0.44$ Wb/m², $A_c = 21{,}000$ A/m, slot space factor $= 0.4$, ratio of slot depth to width $= 4$, stator slot pitch $= 12$ to $15$ mm, $\delta_s = 4$ A/mm². Calculate: (i) main dimensions, (ii) $T_s$ (turns per phase of stator conductor), (iii) $A_s$ (area of stator conductor), (iv) number of stator slots, (v) area and dimension of each stator slot, (vi) minimum width of stator teeth, (vii) find stator slot loading. Note: for best power factor, $\tau = \sqrt{0.18L}$. [[8]]

@q 5
(a) Explain the factors to be considered for the choice of ampere conductors per meter ($A_c$) in DC machine. [[5]]

(b) A design is required for a 30 kW, 4 pole, 900 rpm DC shunt generator, the full load terminal voltage being 240 V. Assume that the full load armature voltage is 3% of the terminal voltage. Calculate the main dimensions of the machine if the maximum gap density is 0.85 Wb/m², specific electrical loading of 20,000 ampere conductor/meter and field resistance is 120 Ω. The ratio of pole arc to pole pitch is 0.7. The pole face is square. [[5]]
<!-- SOLUTIONS -->

@s 1
**(a) Soft and hard magnetic materials**

| Property | Soft magnetic material | Hard magnetic material |
|---|---|---|
| Coercivity $H_c$ | Very small ($< 100$ A/m) | Large ($10^4$ to $10^6$ A/m) |
| Hysteresis loop | Narrow, tall, small area | Wide, large area |
| Hysteresis loss per cycle | Small | Large |
| Permeability | High ($\mu_r$ of $10^3$ to $10^5$) | Low |
| Retentivity | Low in practice (loses field when $H \to 0$) | High (keeps its magnetism) |
| Magnetising / demagnetising | Easy | Difficult |
| Examples | Silicon steel, soft iron, permalloy, ferrites | Alnico, steel, ferrite magnets, NdFeB, SmCo |
| Used for | Cores of transformers, rotors, stators, relays, chokes | Permanent magnets (PM motors, loudspeakers, meters, generators) |

```figure caption="Hysteresis loops: the soft material loop (left) is narrow, so little energy is lost per cycle; the hard material loop (right) is wide, with large coercivity and retentivity."
import numpy as np, matplotlib.pyplot as plt
fig,axs=plt.subplots(1,2,figsize=(6.2,2.6))
def loop(ax,Hc,Br,Bs,hs,title):
    H=np.linspace(-hs,hs,400)
    up=Bs*np.tanh((H+Hc)/(hs/3)); dn=Bs*np.tanh((H-Hc)/(hs/3))
    ax.plot(H,up,color=ACCENT); ax.plot(H,dn,color=ACCENT)
    ax.axhline(0,color=INK,lw=0.6); ax.axvline(0,color=INK,lw=0.6)
    ax.set_title(title,fontsize=8); ax.set_xlabel("H"); ax.set_ylabel("B"); ax.set_xticks([]); ax.set_yticks([])
    ax.annotate("Hc",(Hc,0),textcoords="offset points",xytext=(2,-10),fontsize=7)
    ax.annotate("Br",(0,Bs*np.tanh(Hc/(hs/3))),textcoords="offset points",xytext=(3,2),fontsize=7)
loop(axs[0],0.12,0.8,1.0,1.0,"Soft: narrow loop")
loop(axs[1],0.7,0.8,1.0,1.0,"Hard: wide loop")
fig.tight_layout()
```

**(b) Ageing of core and the effect of silicon**

*Ageing.* In a machine core made of ordinary (low-carbon) iron, the iron losses slowly **increase with time** when the core operates at an elevated temperature (about $80$ to $100$ °C for months or years). Dissolved carbon, nitrogen and oxygen precipitate as carbides and nitrides at the grain boundaries, which obstruct domain-wall motion and raise the hysteresis loss. The increase can reach $10$ to $20$ percent or more, so the efficiency and temperature rise of the machine deteriorate over its life.

*Advantages of adding silicon (up to about $4$ to $4.5$ percent) to iron:*

1. Raises the electrical resistivity (roughly from $0.1$ to $0.5\ \mu\Omega\,$m), so **eddy-current loss falls**.
2. Reduces the hysteresis loss (lower coercivity, higher initial permeability, lower magnetostriction).
3. **Eliminates ageing**: silicon locks the carbon and reduces the iron's tendency to form precipitates, so the core loss stays constant over the years.
4. Better permeability at low and medium flux densities, and a lower core loss means lower temperature rise, hence a smaller machine for the same rating.

*Disadvantages:*

1. The steel becomes **hard and brittle**: punching, shearing and handling of laminations are difficult, with more tool wear and burrs.
2. Saturation flux density and **permeability at high flux density fall**, so the magnetising MMF for a given flux is a little larger.
3. Thermal conductivity falls (heat is removed less readily from the core).
4. Higher cost, and the density and mechanical strength change; above about $5$ percent the steel cannot be rolled economically.

@s 2
**(a) Hot spot**

The **hot spot** is the point inside the machine (core, winding or insulation) where the temperature is highest. Heat generated inside a body must flow through the material to its cooled surface, so the temperature rises towards the interior and the centre is hotter than the surface. The temperature rating of the insulation is decided by the hot spot, not by the surface or average temperature.

*Derivation for a plate of thickness $t$.* Consider a plate (e.g. a stack of laminations or a flat winding layer) of thickness $t$ and thermal conductivity $\lambda$ (W/m·°C), generating heat uniformly at $q$ W/m³ (for example iron loss or $\rho J^2$). It is cooled equally on both faces, so by symmetry the centre plane carries no heat flow. Take $x$ from the centre plane, $x = \pm t/2$ at the faces.

Heat generated in the slab between the centre and a plane $x$ (per unit area) is $q\,x$; it flows out across that plane:

$$-\lambda\frac{d\theta}{dx} = q\,x$$

Integrating, with $\theta = \theta_0$ at the centre ($x = 0$):

$$\theta = \theta_0 - \frac{q\,x^2}{2\lambda}$$

At the surface $x = t/2$ the temperature is $\theta_s$:

$$\theta_s = \theta_0 - \frac{q\,t^2}{8\lambda}$$

The **hot-spot temperature rise above the surface** is therefore

$$\boxed{\theta_0 - \theta_s = \frac{q\,t^2}{8\lambda}}$$

The mean rise of the plate above its surface is $\dfrac{2}{3}$ of this: $\theta_{mean} - \theta_s = \dfrac{q\,t^2}{12\lambda}$. If only one face is cooled (the other being thermally insulated) the whole thickness acts as the half-plate and the hot spot is on the insulated face with rise $\dfrac{q\,t^2}{2\lambda}$.

```figure caption="Parabolic temperature distribution in a plate of thickness t with uniform heat generation: the hot spot is at the centre, $\theta_0 - \theta_s = qt^2/(8\lambda)$."
import numpy as np, matplotlib.pyplot as plt
x=np.linspace(-1,1,200); th=1-x**2*0.5
fig,ax=plt.subplots(figsize=(5.0,2.4))
ax.plot(x,th,color=ACCENT); ax.axvline(-1,color=INK,lw=1); ax.axvline(1,color=INK,lw=1)
ax.axhline(0.5,color=SERIES[1],ls='--',lw=0.8); ax.axhline(1,color=SERIES[1],ls='--',lw=0.8)
ax.annotate(r"$\theta_0$ (hot spot)",(0,1),textcoords="offset points",xytext=(0,4),ha='center',fontsize=8)
ax.annotate(r"$\theta_s$",(1,0.5),textcoords="offset points",xytext=(5,-3),fontsize=8)
ax.annotate("x = -t/2",(-1,0.42),textcoords="offset points",xytext=(-5,-12),ha='center',fontsize=7.5)
ax.annotate("x = +t/2",(1,0.42),textcoords="offset points",xytext=(5,-12),ha='center',fontsize=7.5)
ax.set_ylim(0.3,1.15); ax.set_yticks([]); ax.set_xticks([0]); ax.set_xticklabels(["centre"]); ax.set_ylabel("temperature")
```

**(b) Transformer heating test**

Take the temperature rise above the ambient $35$ °C, starting from cold ($\theta = 0$ at $t = 0$). The heating curve is $\theta = \theta_f\,(1 - e^{-t/\tau})$.

$$\begin{gathered}\theta_1 = 59 - 35 = 24\ ^\circ\text{C at } t = 1.5\ \text{h} \\ \theta_2 = 71 - 35 = 36\ ^\circ\text{C at } t = 3\ \text{h}\end{gathered}$$

Divide the two equations and let $x = e^{-1.5/\tau}$ (so $e^{-3/\tau} = x^2$):

$$\begin{gathered}\frac{36}{24} = \frac{1 - x^2}{1 - x} = 1 + x \ \Rightarrow\ x = 0.5\end{gathered}$$

**(i) Heating time constant**

$$e^{-1.5/\tau} = 0.5 \ \Rightarrow\ \tau = \frac{1.5}{\ln 2} = \boxed{2.164\ \text{h}\ (\approx 130\ \text{min})}$$

**(ii) Final steady temperature rise**

$$\theta_f = \frac{24}{1 - 0.5} = \boxed{48\ ^\circ\text{C}}\quad(\text{final oil temperature } 35 + 48 = 83\ ^\circ\text{C})$$

**(iii) One-hour rating**

The final rise is proportional to the total loss. At full load let iron loss $= P_i$, copper loss $= 2P_i$, total $3P_i$. At a load of $k$ times full load the loss is $P_i + 2k^2P_i = P_i(1 + 2k^2)$, so the final rise is

$$\theta_f(k) = 48\,\frac{1 + 2k^2}{3}.$$

The 1-hour rating is the load which makes the temperature rise reach the permitted maximum ($48$ °C, the full-load steady rise) at the end of one hour:

$$\begin{gathered}48 = \theta_f(k)\left(1 - e^{-1/\tau}\right) \\ e^{-1/2.164} = e^{-0.4621} = 0.630,\quad 1 - 0.630 = 0.370\end{gathered}$$

$$\begin{gathered}\frac{1 + 2k^2}{3}(0.370) = 1 \ \Rightarrow\ 1 + 2k^2 = 8.108 \ \Rightarrow\ k^2 = 3.554,\ \ k = 1.885\end{gathered}$$

$$\boxed{\text{1-hour rating} = 1.885 \times 40 = 75.4\ \text{kVA}}$$

(The load can be almost twice the rating for one hour because the oil and windings need time, $\tau = 2.16$ h, to heat up; for continuous duty only $40$ kVA is permitted.)

```figure caption="Heating curve of the transformer, $\theta = 48(1 - e^{-t/2.164})$ °C above ambient; the test points 24 °C at 1.5 h and 36 °C at 3 h are marked."
import numpy as np, matplotlib.pyplot as plt
t=np.linspace(0,10,200); th=48*(1-np.exp(-t/2.164))
fig,ax=plt.subplots(figsize=(5.2,2.6))
ax.plot(t,th,color=ACCENT); ax.axhline(48,color=SERIES[1],ls='--',lw=0.8)
ax.plot([1.5,3],[24,36],'o',color=INK,ms=4)
ax.annotate("(1.5 h, 24 C)",(1.5,24),textcoords="offset points",xytext=(6,-10),fontsize=7.5)
ax.annotate("(3 h, 36 C)",(3,36),textcoords="offset points",xytext=(6,-10),fontsize=7.5)
ax.annotate("final rise 48 C",(7,48),textcoords="offset points",xytext=(0,4),fontsize=7.5)
ax.set_xlabel("time (h)"); ax.set_ylabel("rise above ambient (C)"); ax.grid(True)
```

@s 3
**(a) Temperature rise and cooling tubes**

*Which data are needed.* The core and winding dimensions in the table fix the active part of the transformer (flux, turns, window); for the **thermal** part only the losses and the tank size are required: iron loss $P_i = 1460$ W, full-load copper loss $P_c = 3865$ W, so the total loss to be dissipated is

$$\begin{gathered}P_T = 1460 + 3865 = 5325\ \text{W}.\end{gathered}$$

*Assumptions (standard for natural-cooled oil transformers).*

- The tank walls dissipate by radiation plus convection at $12.5$ W/m²·°C (about $6$ by radiation and $6.5$ by convection) per °C of oil temperature rise.
- The top cover and bottom are neglected (their contribution is small and this keeps the estimate safe).
- Cooling tubes dissipate by convection only (they shield each other from radiation), at $8.8$ W/m²·°C of their own surface. The tubes are 50 mm in outside diameter, with length $0.8$ of the tank height.

**Tank surface** (four vertical sides):

$$\begin{gathered}S_t = 2(L_t + W_t)H_t = 2(1.05 + 0.62)(1.6) = 5.344\ \text{m}^2\end{gathered}$$

**Temperature rise of the plain tank**

$$\theta = \frac{P_T}{12.5\,S_t} = \frac{5325}{12.5 \times 5.344} = \frac{5325}{66.8} = \boxed{79.7\ ^\circ\text{C}}$$

This is far above the permitted $35$ °C, so cooling tubes are needed. (The loss per square metre of tank surface is $5325/5.344 = 996$ W/m², far above the $\approx 300$ W/m² a plain natural-cooled tank can dissipate.)

**Tube surface needed for $\theta = 35$ °C.** The heat dissipated per °C of rise must be $\dfrac{5325}{35} = 152.1$ W/°C:

$$\begin{gathered}12.5\,S_t + 8.8\,S_{tubes} = 152.1 \ \Rightarrow\ 66.8 + 8.8\,S_{tubes} = 152.1 \ \Rightarrow\ S_{tubes} = \frac{152.1 - 66.8}{8.8} = 9.70\ \text{m}^2\end{gathered}$$

**Number of tubes.** Tube length $= 0.8 \times 1.6 = 1.28$ m, diameter $0.05$ m:

$$\begin{gathered}\text{area of one tube} = \pi d\,l = \pi(0.05)(1.28) = 0.2011\ \text{m}^2\end{gathered}$$

$$n = \frac{9.70}{0.2011} = 48.2 \ \Rightarrow\ \boxed{n = 49\ \text{tubes (about 50)}}$$

**Check:** heat dissipated $= (66.8 + 49 \times 0.2011 \times 8.8)\times 35 = (66.8 + 86.7)(35) = 5373$ W $> 5325$ W ✓, mean oil rise $\approx 34.7$ °C.

**Arrangement.** Tubes at a pitch of at least $75$ mm (one and a half tube diameters) between centres. The tank perimeter is $2(1.05 + 0.62) = 3.34$ m, which would take about $44$ tubes at $75$ mm in a single row, so the tubes are fitted in **two staggered rows** on all four faces: $25$ tubes in the inner row and $24$ in the outer row (pitch about $134$ mm in each row, the outer row offset by half a pitch and set $\approx 75$ mm further out). The ends of every tube are welded into the tank wall, the upper end near the top of the oil level and the lower end near the bottom, so the hot oil rises through the tank, cools in the tubes and sinks back (thermosiphon circulation).

```figure caption="Plan view of the tank (1.05 m x 0.62 m) with 49 cooling tubes arranged in two staggered rows around the perimeter: 25 in the inner row and 24 in the outer row."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
L,W=1.05,0.62
def row(n,off):
    per=2*(L+W+2*off); pts=[]
    for i in range(n):
        s=(i+0.5)*per/n
        a,b=L+2*off,W+2*off
        if s<a: pts.append((-off+s,-off))
        elif s<a+b: pts.append((L+off,-off+(s-a)))
        elif s<2*a+b: pts.append((L+off-(s-a-b),W+off))
        else: pts.append((-off,W+off-(s-2*a-b)))
    return pts
fig,ax=plt.subplots(figsize=(5.4,3.3))
ax.add_patch(Rectangle((0,0),L,W,fill=False,ec=INK,lw=1.6))
for (x,y) in row(25,0.035): ax.add_patch(Circle((x,y),0.025,fc='none',ec=ACCENT,lw=1))
for (x,y) in row(24,0.11): ax.add_patch(Circle((x,y),0.025,fc='none',ec=SERIES[1],lw=1))
ax.annotate("tank wall",(L/2,W/2),ha='center',fontsize=8)
ax.annotate("inner row: 25 tubes",(L/2,-0.1),ha='center',fontsize=7.5,color=ACCENT)
ax.annotate("outer row: 24 tubes",(L/2,W+0.17),ha='center',fontsize=7.5,color=SERIES[1])
ax.set_xlim(-0.25,L+0.25); ax.set_ylim(-0.25,W+0.3); ax.set_aspect('equal'); ax.axis('off')
```

**(b) Power transformer and distribution transformer**

| Point | Power transformer | Distribution transformer |
|---|---|---|
| Position in system | Generating stations and transmission substations | Near the consumer, end of distribution |
| Rating | Large (above about 200 kVA up to hundreds of MVA) | Small (up to about 200 to 500 kVA) |
| Voltage | High: 33, 66, 132, 220 kV and above | Medium to low: 11 kV or 33 kV to 400/230 V |
| Loading | Operates near full load almost all the time | Load varies widely during the day, often light load |
| Design aim | **High full-load efficiency** (iron loss $\approx$ copper loss at full load) | **High all-day efficiency** (small iron loss, since it is energised 24 h) |
| Core flux density | Higher, about $1.5$ to $1.7$ T | Lower, about $1.2$ to $1.4$ T to cut no-load loss |
| Losses | Copper loss designed lower | Iron loss kept small, copper loss relatively larger |
| Voltage regulation | Smaller leakage reactance is often not a priority (impedance high to limit short circuit) | Low impedance (about $4$ to $5$ percent) for good regulation |
| Cooling | Oil with fans, pumps, radiators (ONAN, ONAF, OFAF) | Oil natural (ONAN), with plain or tubular tank |
| Fittings | Conservator, Buchholz relay, OLTC, bushings, many protections | Few accessories: breather, bushings, simple tap changer (off-load) |
| Cost and weight | High | Low |

@s 4
**(a) Factors in selecting the length of air gap of an induction motor**

The air gap is much smaller than in other machines, because the whole magnetising current comes from the stator supply. The gap length $l_g$ is a compromise between several factors:

1. **Power factor.** The magnetising MMF is mostly spent in the gap, so $I_m \propto B\,l_g\,k_g$. A **small gap** gives a small magnetising current and therefore a high power factor. This is the main reason the gap is made as short as possible.
2. **Overload capacity.** The leakage reactance (differential/zig-zag leakage) falls with a smaller gap, so the maximum torque (pull-out) and overload capacity increase.
3. **Cooling.** A larger gap gives better ventilation and a better path for heat; a very small gap hampers cooling.
4. **Noise.** A very small gap increases tooth-ripple and slot-harmonic effects (high-frequency noise and hum) and produces mechanical noise; a larger gap reduces noise.
5. **Unbalanced magnetic pull and mechanical clearance.** A small gap magnifies the effect of rotor eccentricity, shaft deflection and bearing wear; the pull is greater and rubbing may occur. The gap must be large enough for the manufacturing tolerance of the rotor and stator bores.
6. **Surface (pole-face) and pulsation losses.** A small gap raises the high-frequency tooth-pulsation and surface losses in the rotor and stator teeth and lowers the efficiency.
7. **Cross-magnetisation and stray load loss.** Smaller gap gives larger harmonic fluxes and higher stray-load loss, a larger gap reduces them.
8. **Machine size.** A gap that is too large raises the MMF per pole and requires more copper and iron for the same rating.

A usual empirical choice for 3-phase motors is $l_g = 0.2 + 2\sqrt{DL}$ mm ($D$ and $L$ in m), for example about $0.35$ mm for the motor of part (b).

**(b) Design of the 2.2 kW motor**

*Data:* $P = 2.2$ kW, $V = 440$ V (taken as the line voltage, star connected), $f = 50$ Hz, $N = 1430$ rpm so the synchronous speed is $1500$ rpm and $p = 4$ poles; $\eta = 0.8$, $\cos\phi = 0.85$, $B_{av} = 0.44$ T, $A_c = 21000$ A/m, slot space factor $0.4$, $d_s/w_s = 4$, $\delta_s = 4$ A/mm². Assume winding factor $K_w = 0.955$.

**(i) Main dimensions**

Input kVA: $\ Q = \dfrac{P}{\eta\cos\phi} = \dfrac{2.2}{0.8 \times 0.85} = 3.235\ \text{kVA}$.

Output coefficient: $\ C_0 = 11\,K_w B_{av} A_c \times 10^{-3} = 11(0.955)(0.44)(21000)\times 10^{-3} = 97.07$.

Synchronous speed $n_s = 1500/60 = 25$ rps:

$$\begin{gathered}D^2L = \frac{Q}{C_0\,n_s} = \frac{3.235}{97.07 \times 25} = 1.333 \times 10^{-3}\ \text{m}^3\end{gathered}$$

Best power factor: $\tau = \sqrt{0.18L}$ with $\tau = \dfrac{\pi D}{p} = \dfrac{\pi D}{4}$:

$$\begin{gathered}D = \frac4\pi\sqrt{0.18L} \ \Rightarrow\ D^2 = \frac{16}{\pi^2}(0.18L) = 0.2918\,L\end{gathered}$$

$$\begin{gathered}D^2L = 0.2918\,L^2 = 1.333\times10^{-3} \ \Rightarrow\ L = 0.0676\ \text{m} \\ D = \sqrt{0.2918(0.0676)} = 0.1404\ \text{m}\end{gathered}$$

Adopt $D = 0.140$ m and $L = 0.068$ m. Pole pitch $\tau = \pi(0.140)/4 = 0.110$ m, $L/\tau = 0.62$.

$$\boxed{D = 140\ \text{mm},\qquad L = 68\ \text{mm},\qquad \tau = 110\ \text{mm}}$$

**(ii) Turns per phase.** Flux per pole $\Phi = B_{av}\tau L = 0.44(0.110)(0.068) = 3.29 \times 10^{-3}$ Wb. Star connection: $V_{ph} = 440/\sqrt3 = 254$ V; taking $E_{ph} \approx V_{ph}$:

$$\begin{gathered}T_s = \frac{E_{ph}}{4.44\,f\,\Phi\,K_w} = \frac{254}{4.44(50)(3.29\times10^{-3})(0.955)} = 364\ \text{(final value fixed after the slot count)}\end{gathered}$$

**(iv) Number of stator slots** (done before the final $T_s$). Slot pitch $12$ to $15$ mm, so $S_s = \dfrac{\pi D}{y_{ss}} = \dfrac{\pi(140)}{12\ \text{to}\ 15} = 29$ to $37$. For a balanced three-phase, 4-pole winding take a multiple of $12$: $S_s = 36$ ($q = 3$ slots per pole per phase). The slot pitch is $\pi(140)/36 = 12.2$ mm, within the range.

Conductors per slot $Z_s = \dfrac{6\,T_s}{S_s} = \dfrac{6 \times 364}{36} = 60.7 \approx 60$ (even, for a double-layer winding). Then

$$\boxed{T_s = \frac{Z_s S_s}{6} = \frac{60 \times 36}{6} = 360\ \text{turns per phase}}$$

**(iii) Stator conductor area.** Full-load current $I_{ph} = \dfrac{P}{3V_{ph}\,\eta\cos\phi} = \dfrac{2200}{3(254)(0.8)(0.85)} = 4.245$ A.

$$\boxed{A_s = \frac{I_{ph}}{\delta_s} = \frac{4.245}{4} = 1.06\ \text{mm}^2}\quad(\text{about 1.16 mm bare diameter, SWG 18})$$

**(v) Slot area and dimensions.** Copper in each slot $= Z_sA_s = 60 \times 1.06 = 63.7$ mm². With slot space factor $0.4$:

$$\begin{gathered}\text{slot area} = \frac{63.7}{0.4} = 159\ \text{mm}^2\end{gathered}$$

With $d_s = 4w_s$: $\ 4w_s^2 = 159 \Rightarrow w_s = 6.3$ mm, $d_s = 25.2$ mm.

$$\boxed{\text{slot area} \approx 159\ \text{mm}^2,\qquad \text{slot } 6.3\ \text{mm wide} \times 25.2\ \text{mm deep}}$$

**(vi) Minimum width of stator teeth.** For parallel-sided slots the tooth is narrowest at the air-gap surface:

$$\begin{gathered}w_t = y_{ss} - w_s = 12.2 - 6.3 = 5.9\ \text{mm}\end{gathered}$$

Check of the tooth flux density (maximum gap density $B_{max} = 1.36B_{av} = 0.598$ T, stacking factor $0.9$): $B_t = \dfrac{B_{max}\,y_{ss}}{w_t K_i} = \dfrac{0.598 \times 12.2}{5.9 \times 0.9} = 1.37$ T, below the usual limit of about $1.7$ T ✓.

$$\boxed{w_{t,min} \approx 5.9\ \text{mm}}$$

**(vii) Stator slot loading** (ampere-conductors per slot):

$$I_{ph} \times Z_s = 4.245 \times 60 = \boxed{255\ \text{A}}$$

This is far below the usual limit of about $1500$ A per slot, so the loading is acceptable.

@s 5
**(a) Factors for the choice of specific electric loading $A_c$ of a DC machine**

Typical values are $15{,}000$ to $50{,}000$ A/m for DC machines. A larger $A_c$ gives a smaller, cheaper machine for a given output ($P \propto B_{av}A_c D^2Ln$) but is limited by:

1. **Temperature rise (heating).** Armature copper loss per unit surface $\propto A_c\delta$. A higher $A_c$ heats the winding; the permitted insulation class and the cooling arrangement set the limit.
2. **Commutation.** The reactance voltage $e_r \propto A_c$. A high loading makes commutation difficult (sparking), so interpoles and compensating windings are required.
3. **Armature reaction.** The armature MMF per pole is proportional to $A_c\tau$; high loading distorts and weakens the main field, worsens regulation and may cause flashover at the brushes.
4. **Voltage.** At high voltage more insulation is needed in each slot, so the copper fraction falls and a lower $A_c$ must be used. Low-voltage machines can take higher loading.
5. **Efficiency.** Higher $A_c$ means more copper loss, so efficiency is lower for the same size. It also affects the speed regulation.
6. **Size, speed and cooling.** Machines with good ventilation (open, forced air) and a larger diameter can use higher $A_c$; small and totally-enclosed machines use less. Low-speed machines can take a high loading because heat dissipation is relatively good.
7. **Type of duty and cost.** Intermittent duty machines (cranes, traction) can be loaded more heavily than continuous-duty machines.

**(b) 30 kW, 4-pole, 900 rpm DC shunt generator**

$$\begin{gathered}\text{Load current } I = \frac{30000}{240} = 125\ \text{A} \\ \text{field current } I_f = \frac{240}{120} = 2\ \text{A}\end{gathered}$$

$$\begin{gathered}I_a = I + I_f = 127\ \text{A} \\ E_a = V + 0.03V = 1.03(240) = 247.2\ \text{V}\end{gathered}$$

Electromagnetic (armature) power $P_a = E_aI_a = 247.2 \times 127 = 31{,}394$ W.

Average flux density $B_{av} = \psi B_g = 0.7 \times 0.85 = 0.595$ T. Speed $n = 900/60 = 15$ rps. The output equation is

$$P_a = \pi^2 B_{av}A_c\,D^2L\,n$$

$$\begin{gathered}D^2L = \frac{31394}{\pi^2(0.595)(20000)(15)} = \frac{31394}{1.7617\times10^{6}} = 0.01782\ \text{m}^3\end{gathered}$$

Pole pitch $\tau = \pi D/4$. The pole face is square: pole arc $=$ axial length, i.e. $L = \psi\tau = 0.7\,\dfrac{\pi D}{4} = 0.5498\,D$.

$$\begin{gathered}D^2(0.5498D) = 0.01782 \ \Rightarrow\ D^3 = 0.03241 \ \Rightarrow\ D = 0.319\ \text{m}\end{gathered}$$

$$\begin{gathered}L = 0.5498(0.3188) = 0.175\ \text{m} \\ \tau = \frac{\pi(0.3188)}{4} = 0.250\ \text{m} \\ \text{pole arc} = 0.7\tau = 0.175\ \text{m}\end{gathered}$$

$$\boxed{D \approx 0.319\ \text{m (armature diameter)},\qquad L \approx 0.175\ \text{m},\qquad \tau \approx 0.250\ \text{m}}$$

Check: $\psi\tau = 0.175 = L$ ✓ (square pole face). Useful follow-on values: flux per pole $\Phi = B_g\psi\tau L = 0.85(0.175)(0.175) = 0.0261$ Wb, and the total number of armature conductors $Z = \dfrac{A_c\pi D}{I_c}$ where $I_c$ is the current per conductor: $Z \approx \dfrac{20000\pi(0.3188)}{31.75} = 631$ for a lap winding ($I_c = 127/4$) or $\approx 315$ for a wave winding ($I_c = 127/2$).
