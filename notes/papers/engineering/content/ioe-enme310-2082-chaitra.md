---
file: NEBians-IOE-Past-Paper-Engineering-Thermodynamics-and-Heat-Transfer-ENME310-2082-Chaitra.pdf
subject: Engineering Thermodynamics and Heat Transfer
level: BE · Year III / Part I
code: ENME 310
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular exam (new course), BE Electrical (BEL), Year III / Part I. Full marks 60, pass marks 24. Necessary charts are attached herewith (steam tables, printed with the questions).
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Necessary charts are attached herewith · Assume suitable data if necessary</small>

@q 1
a) Differentiate between state and path function with examples. [[3]]

b) Write down salient characteristics of stored energy. Also, define total energy of a system. [[3]]

@q 2
a) Define the term quality and write its relationship with moisture content. Derive the expression for specific volume of a two-phase mixture in terms of quality. [[3]]

b) Write the functions and governing equation for an adiabatic nozzle and an evaporator. [[3]]

@q 3
a) State Clausius and Kelvin-Planck statement of second law of thermodynamics and show their equivalence. [[3]]

b) Derive the efficiency of an ideal gas power cycle in terms of pressure ratio with corresponding processes on P-V and T-S diagrams. Explain the effects of regeneration on the cycle. [[5]]

@q 4
a) List the four fundamental thermodynamic processes of an ideal vapour compression refrigeration cycle and show them in a P-h diagram. Also draw a layout of steam power plant with its essential components. [[5]]

b) Define the terms fin performance and fin effectiveness. Also derive an expression for critical radius of insulation for cylinders. [[5]]

@q 5
At the inlet and outlet of turbine the absolute steam pressures are 6,000 kPa and 4.0 cm of Hg respectively. Barometric pressure is 75 cm of Hg. Calculate the gauge pressure for the entering steam and vacuum gauge pressure for the exiting steam. [Take ρHg = 13600 kg/m³ and g = 9.81 m/s².] [[5]]

@q 6
A rigid vessel having a volume of 0.02 m³, initially contains water at its critical state. The vessel is cooled until its pressure drops to 2000 kPa. Determine: [[5]]

a) The mass of water present in the vessel,

b) The quality at final state, and

c) The mass of saturated liquid water and saturated water vapour at the final state.

@q 7
Air at 100 kPa and 127 °C enters an adiabatic diffuser at a rate of 1.5 kg/s and leaves at a pressure of 150 kPa. The velocity of the air is decreased from 250 m/s to 50 m/s as it passes through the diffuser. Determine the exit temperature of the air and the exit area of the diffuser. [For air, take R = 287 J/kgK, c<sub>p</sub> = 1005 J/kgK]. [[5]]

@q 8
Steam enters into a turbine at 2 MPa, 400 °C and with a velocity of 200 m/s and saturated vapour exits from the turbine at 100 kPa with a velocity of 80 m/s. The power output of the turbine is 800 kW when the mass flow rate of steam is 1.5 kg/s. Turbine rejects heat to the surroundings at 300 K. Determine the rate at which the entropy is generated within the turbine. [[5]]

@q 9
An air-standard Diesel cycle has a compression ratio of 18, and the heat transferred to the working fluid per cycle is 1800 kJ/kg. At the beginning of the compression process the pressure is 0.1 MPa and the temperature is 15 °C. Determine: (a) the thermal efficiency, and (b) the mean effective pressure. [Take γ = 1.4, and c<sub>p</sub> = 1005 kJ/kgK] [[5]]

@q 10
A hot room wall has made of 40 cm of brick on the outside, 12 cm of plastic foam and finally 2 cm of fire clay on the inside. The inside and outside temperatures are 570 °C and 210 °C respectively. If inside and outside heat transfer coefficients are 56 W/m²K and 6 W/m²K and thermal conductivities of brick, foam and fire clay are 0.98 W/mK, 0.02 W/mK and 0.09 W/mK respectively, Determine: [[5]]

a) Rate of heat loss from the hot room if the total wall area is 100 m² and

b) The temperature of outer surface of the brick.

**Steam table data printed with the paper (used in Q6 and Q8).**

| P (kPa) | T<sub>sat</sub> (°C) | v<sub>f</sub> (m³/kg) | v<sub>g</sub> (m³/kg) | h<sub>f</sub> | h<sub>g</sub> | s<sub>f</sub> | s<sub>g</sub> |
|---|---|---|---|---|---|---|---|
| 10 | 45.817 | 0.001010 | 14.674 | 191.83 | 2583.8 | 0.6493 | 8.1482 |
| 100 | 99.632 | 0.001043 | 1.6943 | 417.51 | 2675.1 | 1.3027 | 7.3589 |
| 500 | 151.87 | 0.001093 | 0.3749 | 640.38 | 2748.6 | 1.8610 | 6.8214 |
| 2000 | 212.42 | 0.001177 | 0.09959 | 908.69 | 2798.7 | 2.4471 | 6.3396 |
| 4000 | 250.39 | 0.001252 | 0.04977 | 1087.2 | 2800.6 | 2.7962 | 6.0689 |
| 22055 (critical) | 373.98 | 0.00311 | 0.00311 | 2086 | 2086 | 4.409 | 4.409 |

Superheated steam, 2000 kPa: 400 °C gives v = 0.1512 m³/kg, u = 2945.1, h = 3247.5 kJ/kg, s = 7.1269 kJ/kgK.

<!-- SOLUTIONS -->

@s 1
**(a) State function and path function.**

| | State (point) function | Path function |
|---|---|---|
| Depends on | only the **end state** of the system | the **path** followed between the states |
| Differential | **exact** differential ($dP$, $dT$, $dU$) | **inexact** differential ($\delta Q$, $\delta W$) |
| Cyclic integral | $\oint dX = 0$ | $\oint \delta X \ne 0$ in general |
| Change | $\int_1^2 dX = X_2 - X_1$ | $\int_1^2 \delta X$ = the quantity transferred (not $X_2-X_1$) |
| Examples | pressure, temperature, volume, internal energy $U$, enthalpy $H$, entropy $S$ | heat $Q$, work $W$ |

Example: when 1 kg of gas goes from $(P_1, V_1)$ to $(P_2, V_2)$, the change $U_2 - U_1$ is the same by an isothermal or an adiabatic path, but the work $\int P\,dV$ (the area under the curve) is different for each path, so $W$ is a path function.

**(b) Stored energy.** Energy that is **possessed by the system** (as against heat and work, which are energy in transit across the boundary).

- It is a **property** of the system (a **state function**, with an exact differential); its change depends on the end states only.
- It is **extensive** (the energy per unit mass $e = E/m$ is intensive), and it is conserved: only its form can change.
- It exists in **macroscopic forms** (the kinetic energy of the bulk motion and the potential energy in the gravity or other fields, which depend on the frame of reference) and **microscopic forms** (the molecular KE and PE, chemical and nuclear energy, together the internal energy $U$, independent of the outside reference).
- It can be **stored, converted and transferred** by heat, work and mass flow.

**Total energy** of a system is the sum of all forms of its energy:

$$\begin{gathered}E = U + KE + PE = U + \tfrac12 mV^2 + mgz\quad(\text{J}) \\ e = u + \tfrac12 V^2 + gz\ (\text{J/kg})\end{gathered}$$

for a stationary closed system without other effects, $E = U$.

@s 2
**(a) Quality.** For a saturated liquid–vapour mixture, the **quality (dryness fraction)** $x$ is the mass fraction of the vapour in the mixture:

$$\begin{gathered}x = \frac{m_g}{m_f + m_g} = \frac{m_g}{m_t} \\ 0 \le x \le 1\end{gathered}$$

($x = 0$ saturated liquid, $x = 1$ saturated vapour). The **moisture content (wetness fraction)** is the mass fraction of the liquid, $y = m_f/m_t$, so

$$ \boxed{y = 1 - x} $$

**Specific volume of the mixture.** The total volume is $V = V_f + V_g$, that is $m_t v = m_f v_f + m_g v_g$. Dividing by $m_t$ and using $m_f/m_t = 1-x$, $m_g/m_t = x$:

$$ v = (1-x)\,v_f + x\,v_g = v_f + x\,(v_g - v_f) $$

$$\begin{gathered}\boxed{v = v_f + x\,v_{fg}} \\ x = \frac{v - v_f}{v_{fg}}\end{gathered}$$

and likewise $h = h_f + x h_{fg}$, $u = u_f + xu_{fg}$, $s = s_f + xs_{fg}$.

**(b) Adiabatic nozzle.** *Function:* a duct of varying area that **increases the velocity (kinetic energy) of the fluid at the expense of its pressure** (and enthalpy). *Governing equation:* the steady-flow energy equation with $Q = 0$, $W = 0$ and a negligible change of PE:

$$ h_1 + \frac{V_1^2}{2} = h_2 + \frac{V_2^2}{2}\ \ \Rightarrow\ \ V_2 = \sqrt{V_1^2 + 2(h_1 - h_2)} $$

with the continuity $\dot m = \rho_1A_1V_1 = \rho_2A_2V_2$.

**Evaporator.** *Function:* a heat exchanger (in a refrigerator or a boiler) in which the **working fluid absorbs heat at nearly constant pressure and changes from the liquid (or the liquid–vapour mixture) to the vapour**, producing the cooling effect in a refrigeration cycle. *Governing equation:* steady flow, $W = 0$, negligible $\Delta KE$, $\Delta PE$:

$$\begin{gathered}\dot Q_{in} = \dot m\,(h_{out} - h_{in}) \\ P_{out} \approx P_{in}\end{gathered}$$

(for the refrigerator, $\dot Q_{in}$ is the refrigeration capacity $\dot Q_L$).

@s 3
**(a) The statements.**

- **Kelvin–Planck:** it is impossible to construct a device that works in a cycle and produces no effect other than the **net work output from the heat taken from a single thermal reservoir** (no heat engine has $\eta = 100\,\%$).
- **Clausius:** it is impossible to construct a device that works in a cycle and produces no effect other than the **transfer of heat from a colder to a hotter body** (no refrigerator works without work input).

**Equivalence.** The two statements are equivalent: a violation of one means a violation of the other.

1. *Violation of Clausius ⇒ violation of Kelvin–Planck.* Let a Clausius-violating device $C$ move $Q_L$ from the cold reservoir $T_L$ to the hot reservoir $T_H$ without work. A normal engine $E$ takes $Q_H$ from $T_H$, rejects $Q_L$ to $T_L$ and does $W = Q_H - Q_L$. The cold reservoir gives and gets $Q_L$, so it is unchanged. The combination takes the net heat $Q_H - Q_L$ from the **single** reservoir $T_H$ and converts it all into work, which violates Kelvin–Planck.
2. *Violation of Kelvin–Planck ⇒ violation of Clausius.* Let a K–P violating engine $K$ take $Q_H$ from $T_H$ and produce $W = Q_H$. Use that work to drive a refrigerator $R$ that takes $Q_L$ from $T_L$ and rejects $Q_L + W$ to $T_H$. Net: the hot reservoir receives $Q_L + W - Q_H = Q_L$, the cold loses $Q_L$, and no net work is used: heat flows from cold to hot unaided, which violates Clausius.

So the two statements are two forms of the same law.

```figure caption="Question 3(a): equivalence of the Clausius and Kelvin–Planck statements. (Left) a Clausius violator C plus an ordinary engine E gives a Kelvin–Planck violator. (Right) a K–P violator K driving a refrigerator R gives a Clausius violator."
import matplotlib.patches as mp
fig,axs=plt.subplots(1,2,figsize=(6.2,3.0))
def res(ax,x,y,t): ax.add_patch(mp.Rectangle((x,y),3.2,0.6,fc="#eef2fb",ec=INK)); ax.text(x+1.6,y+0.3,t,ha="center",va="center",fontsize=7.5)
def dev(ax,x,y,t): ax.add_patch(mp.Circle((x,y),0.45,fc="#fdf1dd",ec=INK)); ax.text(x,y,t,ha="center",va="center",fontsize=8)
ar=dict(arrowstyle="-|>",color=ACCENT,lw=1.2)
a=axs[0]; a.axis("off"); res(a,0,4.2,"hot $T_H$"); res(a,0,0,"cold $T_L$")
dev(a,0.8,2.1,"C"); dev(a,2.4,2.1,"E")
a.annotate("",xy=(0.8,4.2),xytext=(0.8,2.6),arrowprops=ar); a.annotate("",xy=(0.8,1.6),xytext=(0.8,0.6),arrowprops=dict(arrowstyle="<|-",color=ACCENT,lw=1.2))
a.annotate("",xy=(2.4,2.6),xytext=(2.4,4.2),arrowprops=ar); a.annotate("",xy=(2.4,0.6),xytext=(2.4,1.6),arrowprops=ar)
a.text(0.65,3.3,"$Q_L$",ha="right",fontsize=8); a.text(2.55,3.3,"$Q_H$",fontsize=8); a.text(2.55,1.0,"$Q_L$",fontsize=8); a.text(3.45,2.1,"$W=Q_H-Q_L$",fontsize=7.5,va="center")
a.set_title("Clausius violator ⇒ K–P violator",fontsize=8); a.set_xlim(-0.3,5.2); a.set_ylim(-0.2,5.1)
b=axs[1]; b.axis("off"); res(b,0,4.2,"hot $T_H$"); res(b,0,0,"cold $T_L$")
dev(b,0.8,2.1,"K"); dev(b,2.4,2.1,"R")
b.annotate("",xy=(0.8,2.6),xytext=(0.8,4.2),arrowprops=ar); b.annotate("",xy=(2.4,4.2),xytext=(2.4,2.6),arrowprops=ar); b.annotate("",xy=(2.4,1.6),xytext=(2.4,0.6),arrowprops=dict(arrowstyle="<|-",color=ACCENT,lw=1.2))
b.annotate("",xy=(1.95,2.1),xytext=(1.25,2.1),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2)); b.text(1.6,2.35,"W",ha="center",fontsize=8)
b.text(0.65,3.3,"$Q_H$",ha="right",fontsize=8); b.text(2.55,3.3,"$Q_L+W$",fontsize=7.5); b.text(2.55,1.0,"$Q_L$",fontsize=8)
b.set_title("K–P violator ⇒ Clausius violator",fontsize=8); b.set_xlim(-0.3,5.2); b.set_ylim(-0.2,5.1)
fig.tight_layout()
```

**(b) Ideal gas power cycle in terms of pressure ratio: the Brayton (gas-turbine) cycle.** Air-standard assumptions: the working fluid is an ideal gas with constant $c_p$, all processes are internally reversible and the heat addition/rejection are at constant pressure.

- **1–2** reversible adiabatic (isentropic) **compression** in the compressor, $P_1 \to P_2$;
- **2–3** **heat addition** at constant pressure $P_2$ (the combustor / heat exchanger), $Q_{in} = c_p(T_3 - T_2)$;
- **3–4** isentropic **expansion** in the turbine, $P_3 = P_2 \to P_4 = P_1$;
- **4–1** **heat rejection** at constant pressure $P_1$, $Q_{out} = c_p(T_4 - T_1)$.

$$ \eta = 1 - \frac{Q_{out}}{Q_{in}} = 1 - \frac{T_4 - T_1}{T_3 - T_2} = 1 - \frac{T_1\,(T_4/T_1 - 1)}{T_2\,(T_3/T_2 - 1)} $$

For the isentropic processes, with the pressure ratio $r_p = P_2/P_1 = P_3/P_4$:

$$ \frac{T_2}{T_1} = r_p^{(\gamma-1)/\gamma} = \frac{T_3}{T_4}\ \Rightarrow\ \frac{T_3}{T_2} = \frac{T_4}{T_1} $$

so the bracket terms cancel and

$$ \boxed{\eta_{\text{Brayton}} = 1 - \frac{T_1}{T_2} = 1 - \frac{1}{r_p^{(\gamma-1)/\gamma}}} $$

The efficiency rises with the pressure ratio and does not depend on the maximum temperature $T_3$ (which, however, limits the net work and $r_p$ for a given turbine blade temperature). For air ($\gamma = 1.4$), $r_p = 10$ gives $\eta = 1 - 10^{-0.2857} = 48.2\,\%$.

**Effect of regeneration.** A **regenerator** (a counter-flow heat exchanger) uses the hot turbine exhaust (state 4, $T_4 > T_2$) to pre-heat the compressed air from $T_2$ to $T_5$ before it enters the combustor. With the **regenerator effectiveness**

$$ \varepsilon = \frac{h_5 - h_2}{h_4 - h_2} \approx \frac{T_5 - T_2}{T_4 - T_2} $$

the heat supplied and rejected are:

$$\begin{gathered}Q_{in} = c_p(T_3 - T_5) \\ Q_{out} = c_p(T_6 - T_1)\end{gathered}$$

and for the ideal regenerator ($\varepsilon = 1$, $T_5 = T_4$, $T_6 = T_2$)

$$ \eta_{\text{regen}} = 1 - \frac{T_1}{T_3}\,r_p^{(\gamma-1)/\gamma} $$

So the **heat supplied (fuel) and the heat rejected both fall by the same amount** $c_p(T_5 - T_2)$ while the net work is unchanged, so the **thermal efficiency increases**. Unlike the simple cycle, $\eta_{\text{regen}}$ **decreases** as $r_p$ increases, and regeneration helps only at low pressure ratio, while $T_4 > T_2$, i.e. $r_p^{(\gamma-1)/\gamma} < \sqrt{T_3/T_1}$ (beyond it the exhaust is colder than the delivery air and the regenerator would cool the air). The cost: a larger, heavier heat exchanger and some pressure loss.

```figure caption="Question 3(b): the ideal Brayton cycle 1-2-3-4 on P–V and T–S diagrams, and the regenerative cycle on T–S (the hatched/dashed path: compressed air is heated from 2 to 5 by the exhaust that cools from 4 to 6)."
v=np.linspace(0.5,1,50)
g=1.4
fig,axs=plt.subplots(1,3,figsize=(6.4,2.5))
# PV
a=axs[0]; P1,P2=1.0,6.0; V1=1.0; V2=V1*(P1/P2)**(1/g); V3=1.6*V2; V4=V3*(P2/P1)**(1/g)
vv=np.linspace(V2,V1,50); a.plot(vv,P1*(V1/vv)**g,color=ACCENT,lw=1.6)
a.plot([V2,V3],[P2,P2],color=ACCENT,lw=1.6)
vv=np.linspace(V3,V4,50); a.plot(vv,P2*(V3/vv)**g,color=ACCENT,lw=1.6)
a.plot([V4,V1],[P1,P1],color=ACCENT,lw=1.6)
for n,(x,y) in zip("1234",[(V1,P1),(V2,P2),(V3,P2),(V4,P1)]): a.plot(x,y,"o",color=INK,ms=3); a.text(x+0.02,y+0.18,n,fontsize=8)
a.set_xlabel("V",fontsize=8); a.set_ylabel("P",fontsize=8); a.set_title("P–V",fontsize=8); a.tick_params(labelsize=6); a.set_xticks([]); a.set_yticks([])
# TS
def ts(a,reg=False):
    s=np.linspace(0,1,40); cp=1.0
    T1=1.0; r=1.5; T2=T1*r; T3=3.0*T1; T4=T3/r
    s1,s2=0.0,0.0; s3=cp*np.log(T3/T2); s4=s3
    t=np.linspace(T2,T3,50); a.plot(cp*np.log(t/T2),t,color=ACCENT,lw=1.6)
    t=np.linspace(T1,T4,50); a.plot(s3+0*t+cp*np.log(t/T4)+0*t,t,color=ACCENT,lw=1.6,alpha=0)
    # isobar 4-1 : s = s4 + cp ln(T/T4)
    a.plot(s4+np.log(t/T4),t,color=ACCENT,lw=1.6)
    a.plot([0,0],[T1,T2],color=ACCENT,lw=1.6); a.plot([s3,s4],[T3,T4],color=ACCENT,lw=1.6)
    pts=[("1",0,T1),("2",0,T2),("3",s3,T3),("4",s4,T4)]
    if reg:
        T5=T4; T6=T2
        a.plot([0],[T5],"o",color=INK,ms=3); a.text(0.03,T5+0.08,"5",fontsize=8)
        a.plot([s4+np.log(T6/T4)],[T6],"o",color=INK,ms=3); a.text(s4+np.log(T6/T4)+0.03,T6-0.2,"6",fontsize=8)
        a.plot([0,0],[T2,T5],color=ACCENT,lw=2.4,ls="--")
    for n,x,y in pts: a.plot(x,y,"o",color=INK,ms=3); a.text(x+0.03,y+0.08,n,fontsize=8)
    a.set_xlabel("s",fontsize=8); a.set_ylabel("T",fontsize=8); a.tick_params(labelsize=6); a.set_xticks([]); a.set_yticks([])
ts(axs[1]); axs[1].set_title("T–S (simple)",fontsize=8)
ts(axs[2],True); axs[2].set_title("T–S (regenerative)",fontsize=8)
fig.tight_layout()
```

@s 4
**(a) Ideal vapour-compression refrigeration cycle (the four processes).**

| Process | Description | Device | Property |
|---|---|---|---|
| 1–2 | **Isentropic compression** of saturated vapour | compressor | $s_2 = s_1$, $P$ rises, superheated |
| 2–3 | **Constant-pressure heat rejection** (de-superheating and condensation) to saturated liquid | condenser | $P = $ const |
| 3–4 | **Isenthalpic throttling** (irreversible expansion) to the evaporator pressure | expansion valve | $h_4 = h_3$ |
| 4–1 | **Constant-pressure heat absorption** (evaporation) from the cold space | evaporator | $P = $ const |

$\text{COP} = \dfrac{h_1 - h_4}{h_2 - h_1}$.

```figure caption="Question 4(a): (left) the ideal vapour-compression refrigeration cycle 1-2-3-4 on a P–h diagram (saturation dome, the isentropic compression 1-2, condensation 2-3, throttling 3-4 at constant h and evaporation 4-1); (right) layout of a simple steam power plant (Rankine cycle) with its essential components."
import matplotlib.patches as mp
fig,axs=plt.subplots(1,2,figsize=(6.6,3.0),gridspec_kw={"width_ratios":[1,1.25]})
a=axs[0]
Pdome=lambda x: 0.6+ (3.2-0.5)**1.5*0.9 - ((x-3.2)/6.3)**1.2*2.6
xs=np.linspace(0.5,3.2,60); ys=0.6+(xs-0.5)**1.5*0.9
a.plot(xs,ys,color=MUTED,lw=1.2); xg=np.linspace(3.2,9.5,60); a.plot(xg,Pdome(xg),color=MUTED,lw=1.2)
Ph,Pl=3.0,1.0
h1=7.6; h2=9.6; h3=2.0; h4=h3
a.plot([h4,h1],[Pl,Pl],color=ACCENT,lw=1.8); a.plot([h1,h2],[Pl,Ph],color=ACCENT,lw=1.8); a.plot([h2,h3],[Ph,Ph],color=ACCENT,lw=1.8); a.plot([h3,h4],[Ph,Pl],color=ACCENT,lw=1.8)
for n,x,y,dx,dy in [("1",h1,Pl,0.1,-0.28),("2",h2,Ph,0.1,0.1),("3",h3,Ph,-0.35,0.1),("4",h4,Pl,-0.35,-0.28)]: a.plot(x,y,"o",color=INK,ms=3.5); a.text(x+dx,y+dy,n,fontsize=8.5)
a.text(5.5,0.75,"evaporator",fontsize=6.5,ha="center"); a.text(5.9,3.2,"condenser",fontsize=6.5,ha="center"); a.text(9.0,2.0,"compressor",fontsize=6.5,rotation=75,ha="center"); a.text(0.7,2.0,"valve",fontsize=6.5,rotation=90)
a.set_xlabel("enthalpy h",fontsize=8); a.set_ylabel("pressure P (log)",fontsize=8); a.set_xticks([]); a.set_yticks([]); a.set_title("P–h diagram",fontsize=8); a.set_xlim(0,10.4); a.set_ylim(0.3,3.7)
b=axs[1]; b.axis("off")
def box(x,y,w,hh,t,fc="#eef2fb"):
    b.add_patch(mp.FancyBboxPatch((x,y),w,hh,boxstyle="round,pad=0.03",fc=fc,ec=INK,lw=0.9)); b.text(x+w/2,y+hh/2,t,ha="center",va="center",fontsize=6.5)
box(0,2.4,2.0,1.3,"BOILER\n(+ superheater)\nfuel / heat in",fc="#fdf1dd"); box(3.6,2.4,1.6,1.3,"TURBINE"); box(6.0,2.4,1.4,1.3,"GENERATOR",fc="#e8f4ea")
box(3.6,0.0,1.6,1.0,"CONDENSER\ncooling water"); box(0.3,0.0,1.4,1.0,"FEED PUMP")
ar=dict(arrowstyle="-|>",color=ACCENT,lw=1.2)
b.annotate("",xy=(3.6,3.05),xytext=(2.0,3.05),arrowprops=ar); b.text(2.8,3.25,"steam",fontsize=6.5,ha="center")
b.annotate("",xy=(6.0,3.05),xytext=(5.2,3.05),arrowprops=dict(arrowstyle="-",color=INK,lw=2)); 
b.annotate("",xy=(4.4,1.0),xytext=(4.4,2.4),arrowprops=ar); b.text(4.55,1.7,"exhaust steam",fontsize=6.5)
b.annotate("",xy=(1.7,0.5),xytext=(3.6,0.5),arrowprops=ar); b.text(2.65,0.62,"water",fontsize=6.5,ha="center")
b.annotate("",xy=(1.0,2.4),xytext=(1.0,1.0),arrowprops=ar); b.text(1.15,1.7,"feed water",fontsize=6.5)
b.text(6.7,2.0,"electric\npower out",fontsize=6.5,ha="center"); b.text(2.8,-0.35,"1 boiler → 2 turbine → 3 condenser → 4 pump",fontsize=6.5,ha="center",color=MUTED)
b.set_xlim(-0.3,7.6); b.set_ylim(-0.7,4.0); b.set_title("steam power plant layout",fontsize=8)
fig.tight_layout()
```

**Essential components of the steam power plant** (Rankine cycle): the **boiler (steam generator with the superheater)**, where the feed water is turned into high-pressure steam (the fuel, the nuclear or the solar heat); the **turbine** that expands the steam and drives the **generator**; the **condenser** that condenses the exhaust steam using the cooling water; and the **feed pump** that raises the condensate to the boiler pressure. (Real plants add the economiser, the air pre-heater, the reheater and the feed-water heaters.)

**(b) Fin performance.** A **fin** is an extended surface that increases the heat transfer from a surface by increasing the area. Its performance is measured by

- **Fin efficiency** $\eta_f$: the ratio of the **actual heat transfer from the fin** to the **ideal heat transfer if the whole fin were at the base temperature** $T_b$:

$$ \eta_f = \frac{\dot Q_{fin}}{h A_{fin}(T_b - T_\infty)} $$

(it is 1 for a fin of infinite conductivity and falls as the fin gets longer or thinner, $\eta_f = \tanh(mL)/(mL)$ for an insulated-tip straight fin, with $m = \sqrt{hP/kA_c}$);

- **Fin effectiveness** $\varepsilon_f$: the ratio of the heat transfer **with the fin** to that **without the fin** (from the same base area $A_b$):

$$ \varepsilon_f = \frac{\dot Q_{fin}}{h A_b (T_b - T_\infty)} $$

A fin is worthwhile only if $\varepsilon_f > 1$ (and normally $\ge 2$); it is large for high-$k$ material, a thin, closely spaced fin with a large $P/A_c$, and a low $h$ (gases, natural convection). The two are related by $\varepsilon_f = \eta_f\,A_{fin}/A_b$.

**Critical radius of insulation for a cylinder.** A pipe of the outer radius $r_i$ at the temperature $T_i$ is covered by insulation of conductivity $k$ up to the radius $r$; the outside is at $T_\infty$ with the convection coefficient $h$. The heat loss for the length $L$:

$$ \dot Q = \frac{T_i - T_\infty}{R_{ins} + R_{conv}} = \frac{2\pi L\,(T_i - T_\infty)}{\dfrac{\ln(r/r_i)}{k} + \dfrac{1}{h\,r}} $$

$\dot Q$ is a maximum when the total resistance $R_t = \dfrac{\ln(r/r_i)}{2\pi kL} + \dfrac{1}{2\pi r L h}$ is a minimum:

$$ \frac{dR_t}{dr} = \frac{1}{2\pi kL\,r} - \frac{1}{2\pi h L\,r^2} = 0\ \ \Rightarrow\ \ \boxed{r_{cr} = \frac{k}{h}} $$

$\dfrac{d^2R_t}{dr^2}\Big|_{r_{cr}} = \dfrac{1}{2\pi L}\left(-\dfrac{1}{kr^2} + \dfrac{2}{hr^3}\right) = \dfrac{1}{2\pi L\,k\,r_{cr}^2} > 0$, so the resistance is a **minimum** (the heat loss a maximum) at $r = k/h$.

- If $r_i < r_{cr}$ (a thin wire or small tube), adding the insulation **increases the heat loss** until $r = r_{cr}$, and only the insulation thicker than the radius $r$ for which the loss equals the bare value reduces it.
- If $r_i \ge r_{cr}$ (large pipes), any insulation reduces the loss.

(For a sphere, $r_{cr} = 2k/h$.) For example, $k = 0.05$ W/mK and $h = 10$ W/m²K gives $r_{cr} = 5$ mm.

```figure caption="Question 4(b): heat loss from an insulated cylinder against the outer radius of insulation. For r_i < r_cr = k/h the loss first rises to a maximum at r_cr and only then falls."
ri=0.5; k=1.0; h=1.0; rc=k/h
r=np.linspace(ri,6,300); R=np.log(r/ri)/k+1/(h*r); Q=1/R
fig,ax=plt.subplots(figsize=(4.8,2.5))
ax.plot(r,Q,color=ACCENT,lw=1.8); ax.axvline(rc,color=MUTED,lw=0.8,ls="--"); ax.axvline(ri,color=INK,lw=0.8,ls=":")
ax.plot(rc,1/(np.log(rc/ri)/k+1/(h*rc)),"o",color=INK,ms=4)
ax.text(rc+0.1,0.62,"$r_{cr}=k/h$ (max loss)",fontsize=8); ax.text(ri+0.05,0.3,"$r_i$",fontsize=8)
ax.set_xlabel("outer radius r of insulation",fontsize=8); ax.set_ylabel("heat loss Q (relative)",fontsize=8); ax.tick_params(labelsize=7); ax.grid(True,color=GRID,lw=0.5); ax.set_ylim(0.2,1.0)
fig.tight_layout()
```

@s 5
Pressure = $\rho g h$. The barometric (atmospheric) pressure:

$$ P_{atm} = \rho_{Hg}\,g\,h = 13600 \times 9.81 \times 0.75 = 100\,062\ \text{Pa} = 100.06\ \text{kPa} $$

**Entering steam (gauge pressure)** $= P_{abs} - P_{atm}$:

$$ P_{gauge,1} = 6000 - 100.06 = \boxed{5899.9\ \text{kPa}\ (\approx 5.90\ \text{MPa gauge})} $$

**Exiting steam.** The absolute pressure is 4.0 cm of Hg:

$$ P_{abs,2} = 13600 \times 9.81 \times 0.04 = 5337\ \text{Pa} = 5.34\ \text{kPa} $$

It is below the atmospheric pressure, so the gauge reads vacuum:

$$ P_{vac} = P_{atm} - P_{abs,2} = 100.06 - 5.34 = \boxed{94.73\ \text{kPa (vacuum)}} $$

(equivalently 71 cm of Hg vacuum, i.e. $75 - 4$ cm Hg $= 71$ cm Hg, or the gauge pressure $-94.73$ kPa.)

@s 6
**(a) Mass of water.** At the critical state (22 055 kPa, 373.98 °C; table) the liquid and the vapour are identical, $v_c = 0.00311\ \text{m}^3/\text{kg}$. The vessel is rigid, so the mass is constant and the volume is constant:

$$ m = \frac{V}{v_c} = \frac{0.02}{0.00311} = \boxed{6.43\ \text{kg}} $$

**(b) Final quality.** At the final state $P = 2000$ kPa, $v_2 = v_c = 0.00311$ m³/kg (rigid, closed). From the table: $v_f = 0.001177$, $v_g = 0.09959$ m³/kg, $T_{sat} = 212.42\,°$C. Since $v_f < v_2 < v_g$ the state is a wet mixture:

$$ x_2 = \frac{v_2 - v_f}{v_g - v_f} = \frac{0.00311 - 0.001177}{0.09959 - 0.001177} = \frac{0.001933}{0.098413} = \boxed{0.0196\ (1.96\,\%)} $$

**(c) Masses of saturated liquid and vapour.**

$$ m_g = x_2\,m = 0.01964(6.431) = \boxed{0.126\ \text{kg (vapour)}} $$

$$ m_f = (1 - x_2)\,m = 6.431 - 0.126 = \boxed{6.30\ \text{kg (liquid)}} $$

Check of the volume:

$$ V = m_f v_f + m_g v_g = 6.3046(0.001177) + 0.1263(0.09959) = 0.0200\ \text{m}^3 \quad\checkmark $$

@s 7
For the adiabatic diffuser, steady flow, $\dot W = 0$, $\dot Q = 0$, $\Delta PE = 0$, ideal gas with constant $c_p$:

$$ c_pT_1 + \frac{V_1^2}{2} = c_pT_2 + \frac{V_2^2}{2} $$

$$ T_2 = T_1 + \frac{V_1^2 - V_2^2}{2c_p} = 400 + \frac{250^2 - 50^2}{2(1005)} = 400 + \frac{60\,000}{2010} $$

$$ \boxed{T_2 = 429.85\ \text{K} \approx 156.9\,°\text{C}} $$

($T_1 = 127 + 273 = 400$ K.) **Exit area.** Exit specific volume:

$$ v_2 = \frac{RT_2}{P_2} = \frac{287(429.85)}{150\,000} = 0.8224\ \text{m}^3/\text{kg} $$

Continuity: $\dot m = \dfrac{A_2V_2}{v_2}$:

$$ A_2 = \frac{\dot m\,v_2}{V_2} = \frac{1.5(0.8224)}{50} = 0.02467\ \text{m}^2 \Rightarrow \boxed{A_2 \approx 246.7\ \text{cm}^2} $$

For comparison the inlet has $v_1 = RT_1/P_1 = 1.148$ m³/kg and $A_1 = \dot m v_1/V_1 = 68.9$ cm², so the area grows about 3.6 times as the flow decelerates and is compressed.

@s 8
Steam properties from the table: inlet 2 MPa, 400 °C: $h_1 = 3247.5$ kJ/kg, $s_1 = 7.1269$ kJ/kgK. Exit saturated vapour at 100 kPa: $h_2 = h_g = 2675.1$ kJ/kg, $s_2 = s_g = 7.3589$ kJ/kgK.

**Energy balance** (steady flow, $\Delta PE = 0$; $\dot W = 800$ kW out, $\dot Q$ is heat **to** the steam):

$$ \dot Q - \dot W = \dot m\left[(h_2 - h_1) + \frac{V_2^2 - V_1^2}{2}\right] $$

$$ \dot Q = 800 + 1.5\left[(2675.1 - 3247.5) + \frac{80^2 - 200^2}{2000}\right] = 800 + 1.5\,[-572.4 - 16.8] $$

$$ \dot Q = 800 - 883.8 = -83.8\ \text{kW} $$

The negative sign means the turbine **loses 83.8 kW** of heat to the surroundings at $T_0 = 300$ K.

**Entropy generation** of the turbine plus its surroundings (the heat is rejected at $T_0$):

$$ \dot S_{gen} = \dot m(s_2 - s_1) + \frac{\dot Q_{out}}{T_0} = 1.5(7.3589 - 7.1269) + \frac{83.8}{300} $$

$$ \dot S_{gen} = 0.3480 + 0.2793 = \boxed{0.627\ \text{kW/K}} $$

($> 0$, so the process is possible and irreversible. The first term is the entropy gain of the steam, 0.348 kW/K, the second is the entropy gained by the surroundings, 0.279 kW/K.)

@s 9
**Data:** $r = 18$, $q_{in} = 1800$ kJ/kg, $P_1 = 100$ kPa, $T_1 = 288$ K, $\gamma = 1.4$, $c_p = 1.005$ kJ/kgK. Then $R = c_p(\gamma-1)/\gamma = 0.2871$ kJ/kgK and $c_v = c_p - R = 0.7179$ kJ/kgK.

**State 2** (isentropic compression):

$$\begin{gathered}T_2 = T_1\,r^{\gamma-1} = 288(18)^{0.4} = 915.2\ \text{K} \\ P_2 = P_1 r^{\gamma} = 100(18)^{1.4} = 5720\ \text{kPa}\end{gathered}$$

**State 3** (constant-pressure heat addition $q_{in} = c_p(T_3 - T_2)$):

$$ T_3 = T_2 + \frac{q_{in}}{c_p} = 915.2 + \frac{1800}{1.005} = 2706.2\ \text{K} $$

Cut-off ratio $r_c = \dfrac{V_3}{V_2} = \dfrac{T_3}{T_2} = \dfrac{2706.2}{915.2} = 2.957$.

**(a) Thermal efficiency of the Diesel cycle:**

$$ \eta = 1 - \frac{1}{r^{\gamma-1}}\cdot\frac{r_c^{\gamma} - 1}{\gamma\,(r_c - 1)} $$

With $r^{\gamma-1} = 18^{0.4} = 3.1778$ and $r_c^{\gamma} = 2.957^{1.4} = 4.5627$:

$$ \eta = 1 - 0.3147\times\frac{4.5627 - 1}{1.4(1.957)} = 1 - 0.3147\times 1.3004 = 0.5908 $$

$$ \boxed{\eta \approx 59.1\,\%} $$

*Check by the temperatures:* $T_4 = T_1 r_c^{\gamma} = 1314$ K, so the heat rejected is

$$ q_{out} = c_v(T_4 - T_1) = 0.7179\,(1026) = 736.5\ \text{kJ/kg} $$

and

$$ \eta = 1 - \frac{736.5}{1800} = 0.591 \quad\checkmark $$

**(b) Mean effective pressure.** The net work is

$$ w_{net} = \eta\,q_{in} = 0.5908(1800) = 1063.5\ \text{kJ/kg} $$

$$\begin{gathered}v_1 = \frac{RT_1}{P_1} = \frac{0.2871(288)}{100} = 0.8270\ \text{m}^3/\text{kg} \\ v_2 = \frac{v_1}{r} = 0.04594\ \text{m}^3/\text{kg}\end{gathered}$$

$$ \text{mep} = \frac{w_{net}}{v_1 - v_2} = \frac{1063.5}{0.8270 - 0.0459} = \frac{1063.5}{0.7811} $$

$$ \boxed{\text{mep} \approx 1362\ \text{kPa} \approx 1.36\ \text{MPa}} $$

```figure caption="Question 9: the air-standard Diesel cycle (r = 18, r_c = 2.957): 1-2 isentropic compression to 5720 kPa, 2-3 constant-pressure heat addition (1800 kJ/kg), 3-4 isentropic expansion to 456 kPa, 4-1 constant-volume heat rejection."
g=1.4; v1=0.8270; v2=v1/18; v3=v2*2.957; v4=v1; P1=100; P2=P1*18**g; P4=P1*2.957**g
fig,ax=plt.subplots(figsize=(5.0,2.7))
v=np.linspace(v2,v1,100); ax.plot(v,P1*(v1/v)**g,color=ACCENT,lw=1.8)
ax.plot([v2,v3],[P2,P2],color=ACCENT,lw=1.8)
v=np.linspace(v3,v4,100); ax.plot(v,P2*(v3/v)**g,color=ACCENT,lw=1.8)
ax.plot([v4,v1],[P4,P1],color=ACCENT,lw=1.8)
for n,x,y,dx,dy in [("1",v1,P1,0.01,-250),("2",v2,P2,-0.045,60),("3",v3,P2,0.01,80),("4",v4,P4,0.015,0)]: ax.plot(x,y,"o",color=INK,ms=3.5); ax.text(x+dx,y+dy,n,fontsize=8.5)
ax.text(0.5,5300,"5720 kPa",fontsize=7); ax.text(0.7,520,"456 kPa",fontsize=7); ax.text(0.1,100,"100 kPa",fontsize=7)
ax.set_xlabel("v (m³/kg)",fontsize=8); ax.set_ylabel("P (kPa)",fontsize=8); ax.tick_params(labelsize=7); ax.grid(True,color=GRID,lw=0.5)
fig.tight_layout()
```

@s 10
**Thermal resistances** (per m² of wall; the inside and outside temperatures are the fluid (gas/air) temperatures, since the film coefficients are given). The series circuit from the room to the outside air is: inside film → fire clay → plastic foam → brick → outside film.

| Layer | Expression | $R$ (m²K/W) |
|---|---|---|
| Inside film | $1/h_i = 1/56$ | 0.01786 |
| Fire clay (2 cm) | $0.02/0.09$ | 0.22222 |
| Plastic foam (12 cm) | $0.12/0.02$ | 6.00000 |
| Brick (40 cm) | $0.40/0.98$ | 0.40816 |
| Outside film | $1/h_o = 1/6$ | 0.16667 |
| **Total** | | **6.8149** |

**(a)** Heat flux and heat loss for $A = 100$ m²:

$$ q = \frac{T_i - T_o}{\sum R} = \frac{570 - 210}{6.8149} = 52.83\ \text{W/m}^2 $$

$$ \dot Q = qA = 52.83 \times 100 = 5283\ \text{W} \Rightarrow \boxed{\dot Q \approx 5.28\ \text{kW}} $$

**(b)** The outer surface of the brick is cooled by the outside film, so

$$ T_{s,out} = T_o + q\,R_{o} = 210 + \frac{52.83}{6} = 210 + 8.80 $$

$$ \boxed{T_{s,out} \approx 218.8\,°\text{C}} $$

*Check of the other interfaces:* inside surface of the fire clay $570 - 52.83/56 = 569.06$ °C; fire clay / foam $569.06 - 52.83(0.2222) = 557.3$ °C; foam / brick $557.3 - 52.83(6.0) = 240.3$ °C; brick outer surface $240.3 - 52.83(0.4082) = 218.8$ °C ✓. The plastic foam takes $317/360 = 88\,\%$ of the whole temperature drop since it is by far the largest resistance.
