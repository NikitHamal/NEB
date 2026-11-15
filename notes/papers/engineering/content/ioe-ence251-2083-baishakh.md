---
file: NEBians-IOE-Past-Paper-Hydraulics-ENCE251-2083-Baishakh.pdf
subject: Hydraulics
level: BE · Year II / Part II
code: ENCE 251
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE Civil, Year II / Part II. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Prove that the shear stress distribution in the case of steady laminar flow for circular pipe is linear. What is Prandtl Mixing Length? [[3+1]]

b) Reservoir 'A' water surface elevation 120 m is connected to reservoir B and C having surface elevation 70 m and 50 m respectively. A pipeline 150 mm diameter and 400 mm long connects reservoir 'A' to junction D. Reservoir B and C are connected to junction D by 75 mm diameter 100 m long and 100 mm diameter and 250 m long pipe line respectively. Assume friction factor f = 0.04 for all pipes, estimate the rate of flow for each pipe, neglecting minor head losses. [[8]]

@q 2
a) Define Conveyance and Section factor (Uniform and critical flow). Derive the condition for hydraulically efficient side slopes for Trapezoidal channel. [[2+4]]

b) A steel pipeline is 30 cm in diameter and has a wall thickness of 3 mm. The pipe is 1000 m long and conveys a flow of 100 Liter/sec (S = 0.82). The static head at the outlet is 160 m of oil. If the working stress of steel is 0.1 kN/mm², calculate the minimum time of closure of the downstream valve. For oil, K = 10⁹ Pa and for steel E = 2.14 × 10¹¹ Pa. [[6]]

@q 3
a) What is Rapidly Varied Flow? Classify the hydraulic jump based on Froude number and tail water depth. [[1+3]]

b) A rectangular channel 8 m wide and 1.5 m deep has a slope of 1 in 1000 lined with smooth concrete plaster. It is desired to have the discharge to be maximum by changing the dimensions of the channel by keeping the same quantity of lining. Workout the new dimensions and the percentage increase in discharge. Assume n = 0.015. [[8]]

@q 4
a) Write down the assumptions in derivation of GVF equation. Prove that the equation for wide rectangular channel is given by $\dfrac{dy}{dx}=\dfrac{1-\left(\frac{y_n}{y}\right)^{10/3}}{1-\left(\frac{y_c}{y}\right)^{3}}$, where $y_n$ is normal depth and $y_c$ is critical depth. [[1+3]]

b) Water flows in a rectangular channel of 4 m width at a depth of 2.50 m and a velocity of 2.25 m/s. If the channel width is reduced to 2.50 m and the bed of the channel is raised by 0.20 m at a section, how will the level of water surface be affected? [[8]]

@q 5
a) A sluice gate across a channel 5 m wide discharges a stream 1 m deep. What is the velocity of the flow releasing through the gate when the depth upstream of the sluice is 4 m? On the downstream side concrete blocks have been placed to create conditions for hydraulic jump to occur. Calculate the force on blocks if the downstream depth is 2 m. [[6]]

```figure caption="Question 5(a): sluice gate with upstream depth 4 m, stream depth 1 m at the gate, a jump held by concrete blocks (force F), and a downstream depth of 2 m."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.8,2.3)); ax.axis("off")
ax.plot([0,14],[0,0],color=INK,lw=2)
ax.add_patch(mp.Polygon([[0,0],[0,4],[2.9,4],[2.9,1.0],[3.0,0.9],[3.0,0],],fc="#cfe3f5",ec="none"))
ax.plot([3.0,3.0],[4.6,1.0],color=INK,lw=3)
x=np.linspace(3,7,30); ax.fill_between(x,0,1.0+0.5*((x-3)/4)**2,color="#cfe3f5")
ax.fill_between(np.linspace(7,13.8,30),0,2.0,color="#cfe3f5")
xx=np.linspace(7,8.2,20); ax.plot(xx,1.4+0.6*(1/(1+np.exp(-(xx-7.6)*5))),color=ACCENT,lw=1.4)
ax.plot([3.1,6.9],[1.0,1.35],color=ACCENT,lw=1.4); ax.plot([8.2,13.8],[2,2],color=ACCENT,lw=1.4); ax.plot([0,2.9],[4,4],color=ACCENT,lw=1.4)
ax.add_patch(mp.Rectangle((6.2,0),0.6,0.5,fc="#bbb",ec=INK,hatch="///")); ax.annotate("",xy=(5.5,0.25),xytext=(6.2,0.25),arrowprops=dict(arrowstyle="->",color="#d9534f",lw=1.5)); ax.text(5.1,0.45,"F",color="#d9534f",fontsize=10)
ar=dict(arrowstyle="<->",lw=0.8); ax.annotate("",xy=(0.6,0),xytext=(0.6,4),arrowprops=ar); ax.text(0.75,2,"4 m",fontsize=9)
ax.annotate("",xy=(3.4,0),xytext=(3.4,1.0),arrowprops=ar); ax.text(3.55,0.35,"1 m",fontsize=9)
ax.annotate("",xy=(12.3,0),xytext=(12.3,2),arrowprops=ar); ax.text(12.45,1.0,"2 m",fontsize=9)
ax.set_xlim(-0.3,14.2); ax.set_ylim(-0.3,4.9)
```

b) A rectangular channel of 4 m width has a manning's roughness coefficient of 0.025. For a discharge of 6 m³/s in this channel, identify the possible GVF profiles produced when bed slope changes from $S_{01}$ = 0.0004 to $S_{02}$ = 0.015. Find the length of GVF curve formed in $S_{01}$ = 0.0004 using direct step method. Take three steps for solution. [[6]]

<!-- SOLUTIONS -->

@s 1
**(a) Linear shear stress distribution in laminar pipe flow.** Consider a coaxial cylinder of fluid of radius $r$ and length $L$ in a horizontal pipe of radius $R$ in steady, uniform flow. The pressure drops from $p_1$ to $p_2$ over $L$ ($\Delta p=p_1-p_2$). There is no acceleration, so the pressure force on the ends balances the shear force on the curved surface:

$$(p_1-p_2)\,\pi r^2=\tau\,(2\pi rL)$$

$$\boxed{\tau=\frac{\Delta p}{2L}\,r}$$

Because $\Delta p/2L$ is the same for all $r$, $\tau$ is **directly proportional to $r$**: it is zero at the pipe axis and maximum at the wall, $\tau_0=\dfrac{\Delta p\,R}{2L}$, and varies linearly across the section. (The same balance holds for turbulent flow; the linear law is a statement of equilibrium and does not depend on the fluid viscosity law.) For laminar flow, $\tau=-\mu\,dv/dr$ then integrates to the parabolic velocity profile $v=\dfrac{\Delta p}{4\mu L}(R^2-r^2)$.

*Prandtl's mixing length.* In turbulent flow it is the average transverse distance $l$ travelled by a fluid lump, before it loses its identity and mixes with the surrounding fluid, while keeping its original momentum. It relates the turbulent shear stress to the velocity gradient:

$$\begin{gathered}\tau=\rho\,l^{2}\left(\frac{du}{dy}\right)^{2} \\ l=\kappa y\ \ (\kappa\approx0.4,\ \text{von Kármán constant, near a wall})\end{gathered}$$

**(b) Three-reservoir problem.** Pipe lengths: AD = 400 m (not "400 mm"), DB = 100 m, DC = 250 m. Friction loss $h_f=\dfrac{8fLQ^2}{\pi^2gd^5}=KQ^2$:

$$K_{AD}=\frac{8(0.04)(400)}{\pi^2(9.81)(0.15)^5}=17\,409,\quad K_{DB}=\frac{8(0.04)(100)}{\pi^2(9.81)(0.075)^5}=139\,276,\quad K_{DC}=\frac{8(0.04)(250)}{\pi^2(9.81)(0.10)^5}=82\,627$$

(units s²/m⁵). Let $H_D$ be the piezometric head at junction D. As $120>H_D$, flow runs from A to D. If $70<H_D$ water flows from D to both B and C ($H_D>70>50$); this is checked below. Continuity at D: $Q_{A}=Q_B+Q_C$:

$$\sqrt{\frac{120-H_D}{17409}}=\sqrt{\frac{H_D-70}{139276}}+\sqrt{\frac{H_D-50}{82627}}$$

Trial and error (or a bisection method) gives $H_D=95.90$ m (> 70 m, so the assumption of flow into both B and C is valid):

| Trial $H_D$ (m) | $Q_A$ (L/s) | $Q_B+Q_C$ (L/s) | Remark |
|---|---|---|---|
| 90 | 41.5 | 12.0 + 22.0 = 34.0 | $Q_A>Q_B+Q_C$: raise $H_D$ |
| 95 | 37.9 | 13.4 + 23.3 = 36.7 | still slightly large |
| 95.90 | 37.2 | 13.6 + 23.6 = 37.2 | balanced |

The discharges, with $Q=\sqrt{h_f/K}$:

$$\boxed{Q_{AD}=37.2\ \text{L/s},\qquad Q_{DB}=13.6\ \text{L/s},\qquad Q_{DC}=23.6\ \text{L/s}}$$

(velocities 2.11, 3.09 and 3.00 m/s). Head losses: AD 24.10 m, DB 25.90 m, DC 45.90 m.

@s 2
**(a) Definitions.**

- **Conveyance** $K$ is the carrying capacity of a channel section per unit slope-root: $K=\dfrac{Q}{\sqrt{S_0}}=\dfrac1nAR^{2/3}$ (Manning), or $CA\sqrt R$ (Chezy). It depends only on the geometry and roughness of the section, and for uniform flow $Q=K\sqrt{S_0}$.
- **Section factor** $Z$: for **uniform flow**, $Z_u=AR^{2/3}=\dfrac{nQ}{\sqrt{S_0}}$ (a function of depth, which gives the normal depth); for **critical flow**, $Z_c=A\sqrt{\dfrac AT}=\dfrac{Q}{\sqrt g}$ (which gives the critical depth, from $Q^2/g=A^3/T$).

*Hydraulically efficient trapezoidal section.* The section that carries the maximum discharge for a given area $A$ has the minimum wetted perimeter $P$. For side slope $m$ H : 1 V and depth $y$:

$$\begin{gathered}A=(B+my)y \\ P=B+2y\sqrt{1+m^2}=\frac Ay-my+2y\sqrt{1+m^2}\end{gathered}$$

*Optimum depth* ($m$ fixed, $A$ fixed): $\dfrac{dP}{dy}=-\dfrac{A}{y^2}-m+2\sqrt{1+m^2}=0$. With $A=(B+my)y$ this becomes

$$B+my=2y\sqrt{1+m^2}-my\ \Rightarrow\ \frac{B+2my}{2}=y\sqrt{1+m^2}$$

that is, **half the top width equals the sloping side**; the hydraulic radius is $R=\dfrac{A}{P}=\dfrac y2$.

*Optimum side slope* ($y$ fixed, $A$ fixed): $\dfrac{\partial P}{\partial m}=-y+\dfrac{2my}{\sqrt{1+m^2}}=0$:

$$\frac{m}{\sqrt{1+m^2}}=\frac12\ \Rightarrow\ \boxed{m=\frac1{\sqrt3}=0.577,\ \ \theta=60^\circ\ \text{with the horizontal}}$$

so the most efficient trapezoidal channel is **half of a regular hexagon**, with $B=\dfrac{2y}{\sqrt3}$, $A=\sqrt3\,y^2$ and $R=y/2$.

**(b) Closure time of the valve.** Data: $D=0.30$ m, $t=3$ mm, $L=1000$ m, $Q=0.1$ m³/s, $\rho=820$ kg/m³, static head 160 m of oil, working stress $\sigma=0.1$ kN/mm² $=100$ MPa.

*Allowable pressure.* For a thin cylinder $\sigma=\dfrac{pD}{2t}$:

$$p_{max}=\frac{2t\sigma}{D}=\frac{2(0.003)(100\times10^6)}{0.30}=2.0\ \text{MPa}$$

Static pressure $p_s=\rho gH=820(9.81)(160)=1.287$ MPa, so the allowable surge pressure is $\Delta p=2.0-1.287=0.713$ MPa, i.e. $\Delta H=\dfrac{0.713\times10^6}{820(9.81)}=88.6$ m of oil.

*Wave speed* (elastic pipe), $K'=\dfrac{K}{1+\dfrac{KD}{Et}}$:

$$K'=\frac{10^9}{1+\dfrac{10^9(0.30)}{2.14\times10^{11}(0.003)}}=\frac{10^9}{1.4673}=6.815\times10^8\ \text{Pa}$$

$$c=\sqrt{\frac{K'}{\rho}}=\sqrt{\frac{6.815\times10^8}{820}}=911.7\ \text{m/s}$$

*Velocity:* $V=\dfrac{Q}{A}=\dfrac{0.1}{\frac\pi4(0.3)^2}=1.415$ m/s. Critical (rapid-closure) time $2L/c=2.19$ s. For sudden closure the surge would be $cV/g=131.5$ m, which exceeds the allowable 88.6 m, so the valve must close slowly, $T>2L/c$. For gradual closure (uniform rate, rigid-column approximation):

$$\Delta H=\frac{2LV}{gT}\ \Rightarrow\ T=\frac{2LV}{g\,\Delta H}=\frac{2(1000)(1.415)}{9.81(88.6)}$$

$$\boxed{T_{min}\approx3.25\ \text{s}}$$

Check: $T=3.25\ \text{s}>2L/c=2.19$ s, so the closure is indeed slow and the formula is applicable.

@s 3
**(a) Rapidly varied flow (RVF).** It is flow in which the depth changes abruptly over a short length of channel, so that the curvature of the streamlines is large, the pressure is not hydrostatic, and the energy losses are local and significant (e.g. hydraulic jump, hydraulic drop, flow over a sharp-crested weir or sluice gate, flow at a sudden transition). 

*Hydraulic jump classification.*

(i) On the basis of the **Froude number** $Fr_1$ of the supercritical approach flow:

| $Fr_1$ | Type of jump | Energy loss |
|---|---|---|
| 1 – 1.7 | Undular jump | very small (< 5 %) |
| 1.7 – 2.5 | Weak jump (rollers form) | 5 – 15 % |
| 2.5 – 4.5 | Oscillating jump (unstable) | 15 – 45 % |
| 4.5 – 9.0 | Steady jump (stable, well-balanced) | 45 – 70 % |
| > 9.0 | Strong (choppy) jump | 70 – 85 % |

(ii) On the basis of the **tail-water depth** $y_t$ compared with the sequent depth $y_2$: a **free (normal) jump** forms at the section where $y_t=y_2$; a **repelled (swept-out) jump** is carried downstream when $y_t<y_2$; a **drowned (submerged) jump** forms against the gate when $y_t>y_2$; and a **forced jump** is held in position by baffle blocks or a sill, when $y_t$ is less than $y_2$.

**(b) Maximum-discharge rectangle with the same lining.** The quantity of lining is the wetted perimeter. Existing section: $B=8$ m, $y=1.5$ m:

$$A=12\ \text{m}^2,\ P=8+2(1.5)=11\ \text{m},\ R=1.0909\ \text{m},\ S_0=0.001$$

$$Q_1=\frac1nAR^{2/3}S_0^{1/2}=\frac1{0.015}(12)(1.0909)^{2/3}(0.001)^{1/2}=26.81\ \text{m}^3/\text{s}$$

For a fixed perimeter $P=B+2y=11$ m the discharge is maximum when the area is maximum, i.e. for the **best rectangular section**, $B=2y$:

$$4y=11\ \Rightarrow\ \boxed{y=2.75\ \text{m},\quad B=5.5\ \text{m}}$$

$$A=5.5(2.75)=15.125\ \text{m}^2,\quad R=\frac y2=1.375\ \text{m}$$

$$Q_2=\frac{1}{0.015}(15.125)(1.375)^{2/3}(0.001)^{1/2}=39.43\ \text{m}^3/\text{s}$$

$$\boxed{\text{increase}=\frac{39.43-26.81}{26.81}\times100\approx47.1\%}$$

@s 4
**(a) Assumptions in the GVF equation.**

1. The flow is steady, $\partial/\partial t=0$.
2. The pressure distribution is hydrostatic (streamline curvature is small and vertical accelerations are negligible).
3. The channel is prismatic, with a constant bed slope $S_0$ (small, so $\cos\theta\approx1$, $\sin\theta\approx\tan\theta$) and a constant shape.
4. The energy (velocity) coefficient $\alpha=1$ and the friction slope $S_f$ at a section is given by the uniform-flow formula (Manning/Chezy) for the local velocity and depth.
5. The channel roughness is constant, and there is no lateral inflow or outflow.

*Proof.* The total head above a datum is $H=z+y+\dfrac{V^2}{2g}$. Differentiating with respect to $x$ (distance along the bed), using $\dfrac{dH}{dx}=-S_f$ and $\dfrac{dz}{dx}=-S_0$:

$$-S_f=-S_0+\frac{dy}{dx}+\frac{d}{dy}\!\left(\frac{Q^2}{2gA^2}\right)\frac{dy}{dx}$$

With $\dfrac{dA}{dy}=T$: $\dfrac{d}{dy}\!\left(\dfrac{Q^2}{2gA^2}\right)=-\dfrac{Q^2T}{gA^3}=-Fr^2$. So $\dfrac{dy}{dx}(1-Fr^2)=S_0-S_f$:

$$\frac{dy}{dx}=\frac{S_0-S_f}{1-Fr^2}$$

*Wide rectangular channel* ($R\approx y$, $A=By$, $q=Q/B$). Manning: $q=\dfrac1ny^{5/3}S_f^{1/2}$ at depth $y$, and $q=\dfrac1ny_n^{5/3}S_0^{1/2}$ at normal depth, hence

$$\frac{S_f}{S_0}=\left(\frac{y_n}{y}\right)^{10/3}$$

The critical depth satisfies $y_c^3=q^2/g$, so $Fr^2=\dfrac{q^2}{gy^3}=\left(\dfrac{y_c}{y}\right)^3$. Substituting,

$$\boxed{\frac{dy}{dx}=S_0\,\frac{1-\left(\dfrac{y_n}{y}\right)^{10/3}}{1-\left(\dfrac{y_c}{y}\right)^{3}}}$$

which is the required equation (the multiplier $S_0$ is the slope; it is omitted in the printed form which gives $dy/dx$ in units of $S_0$).

**(b) Channel contraction with raised bed.** Upstream: $b_1=4$ m, $y_1=2.50$ m, $V_1=2.25$ m/s:

$$\begin{gathered}Q=4(2.5)(2.25)=22.5\ \text{m}^3/\text{s} \\ E_1=2.5+\frac{2.25^2}{2(9.81)}=2.758\ \text{m} \\ Fr_1=0.454\ (\text{subcritical})\end{gathered}$$

At the throat $b_2=2.5$ m, so $q_2=22.5/2.5=9.0$ m²/s, with the bed raised $\Delta z=0.20$ m. Minimum specific energy possible at the throat:

$$\begin{gathered}y_c=\left(\frac{q_2^2}{g}\right)^{1/3}=\left(\frac{81}{9.81}\right)^{1/3}=2.021\ \text{m} \\ E_{min}=1.5y_c=3.032\ \text{m}\end{gathered}$$

Specific energy *available* at the throat (energy conserved): $E_2=E_1-\Delta z=2.758-0.20=2.558$ m, which is **less than $E_{min}=3.032$ m**. The flow cannot pass the contraction at the existing upstream depth: the section **chokes**, critical flow occurs at the throat, and the upstream depth rises (afflux) until the available energy equals the minimum:

$$E_1'=E_{min}+\Delta z=3.032+0.20=3.232\ \text{m}$$

The new upstream depth $y_1'$ (subcritical root) satisfies

$$y_1'+\frac{(22.5/4y_1')^2}{2(9.81)}=3.232\ \Rightarrow\ y_1'+\frac{1.6125}{y_1'^2}=3.232$$

$$\boxed{y_1'\approx3.06\ \text{m}}$$

so the water surface upstream **rises from 2.50 m to about 3.06 m, an afflux of 0.56 m**, and the flow at the throat passes at the critical depth of 2.02 m (the depth in the contraction is 2.02 m above the raised bed). Downstream the flow returns to the normal subcritical condition (or a jump forms if the tail water is low). The discharge remains 22.5 m³/s.

@s 5
**(a) Sluice gate and jump (per unit width, $b=5$ m).** Upstream depth $y_0=4$ m, depth at the vena contracta $y_1=1$ m. Energy equation (no loss through the gate), with $q=V_0y_0=V_1y_1$:

$$y_0+\frac{q^2}{2gy_0^2}=y_1+\frac{q^2}{2gy_1^2}\ \Rightarrow\ 4-1=\frac{q^2}{2g}\left(\frac1{1^2}-\frac1{4^2}\right)$$

$$q^2=\frac{3(2)(9.81)}{0.9375}=62.78\ \Rightarrow\ q=7.92\ \text{m}^2/\text{s}$$

$$\begin{gathered}\boxed{V_1=\frac{q}{y_1}=7.92\ \text{m/s}} \\ Q=qb=39.6\ \text{m}^3/\text{s}\end{gathered}$$

Froude number at the gate $Fr_1=7.92/\sqrt{9.81(1)}=2.53$, and the sequent depth would be $y_2=\tfrac12(\sqrt{1+8Fr_1^2}-1)(1)=3.11$ m. The tail water depth is only $y_3=2$ m $<3.11$ m, so without help the jump would be swept away. The blocks provide the extra force that holds the jump.

*Momentum equation between the section of depth 1 m ($V_1=7.92$ m/s) and the downstream section of depth 2 m ($V_2=q/2=3.96$ m/s), per metre width:*

$$\frac12\gamma y_1^2-\frac12\gamma y_3^2-F=\rho q\,(V_2-V_1)$$

$$\frac12(9.81)(1)^2-\frac12(9.81)(2)^2-F=\frac{1000(7.92)(3.96-7.92)}{1000}$$

$$4.905-19.62-F=-31.39\ \Rightarrow\ F=16.68\ \text{kN per metre width}$$

$$\boxed{F\approx16.7\ \text{kN/m}\ \Rightarrow\ F_{total}=16.68(5)\approx83.4\ \text{kN on the blocks}}$$

The water pushes the blocks downstream with this force (the blocks push back on the water with the same magnitude).

**(b) GVF profiles and the length of the curve.** $b=4$ m, $n=0.025$, $Q=6$ m³/s, $q=1.5$ m²/s.

*Critical depth:* $y_c=\left(\dfrac{q^2}{g}\right)^{1/3}=\left(\dfrac{2.25}{9.81}\right)^{1/3}=0.612$ m.

*Normal depths* from $Q=\dfrac1n\dfrac{(by)^{5/3}}{(b+2y)^{2/3}}S_0^{1/2}$:

$$\begin{gathered}S_{01}=0.0004:\ y_{n1}=1.906\ \text{m}\ (>y_c\ \Rightarrow\text{ mild}) \\ S_{02}=0.015:\ y_{n2}=0.541\ \text{m}\ (<y_c\ \Rightarrow\text{ steep})\end{gathered}$$

*Possible profiles.* The channel changes from a mild to a steep slope. The flow must pass through the critical depth at the break in grade (control section). In the mild reach the water surface falls from $y_{n1}$ towards $y_c$, with $y_c<y<y_{n1}$: an **M2 (drawdown) curve**. In the steep reach the depth continues from $y_c$ down to $y_{n2}$, with $y_{n2}<y<y_c$: an **S2 curve**. No jump occurs.

```figure caption="Mild to steep break in grade: an M2 drawdown curve in the mild reach (yn1 → yc at the break) followed by an S2 curve in the steep reach (yc → yn2)."
fig,ax=plt.subplots(figsize=(5.8,2.6)); ax.axis("off")
x1=np.linspace(0,6,100); x2=np.linspace(6,12,100)
bed1=0-0.0004*60*x1/6*0; 
b1=lambda x:-0.04*x; b2=lambda x:-0.04*6-0.5*(x-6)
ax.plot(x1,b1(x1),color=INK,lw=2.2); ax.plot(x2,b2(x2),color=INK,lw=2.2)
yn1,yc,yn2=1.9,0.61,0.54
M2=yc+(yn1-yc)*np.exp(-((x1)/2.2)**1.3*0+0)  # placeholder
t=(6-x1)/6; M2=yc+(yn1-yc)*(1-np.exp(-3*t))/(1-np.exp(-3))
ax.plot(x1,b1(x1)+M2,color=ACCENT,lw=2); ax.text(2.0,b1(2)+1.55,"M2",fontsize=10,color=ACCENT)
s=(x2-6)/6; S2=yc-(yc-yn2)*(1-np.exp(-4*s)); ax.plot(x2,b2(x2)+S2*1.0,color="#d9534f",lw=2); ax.text(8.5,b2(8.5)+1.0,"S2",fontsize=10,color="#d9534f")
ax.plot(x1,b1(x1)+yn1,color=MUTED,lw=0.9,ls="--"); ax.text(0.1,b1(0)+yn1+0.1,"NDL ($y_{n1}$ = 1.906 m)",fontsize=7.5)
ax.plot(x1,b1(x1)+yc,color=MUTED,lw=0.9,ls=":"); ax.text(0.1,b1(0)+yc-0.35,"CDL ($y_c$ = 0.612 m)",fontsize=7.5)
ax.plot([6],[b1(6)+yc],"o",color=INK,ms=4); ax.text(5.0,b1(6)-0.6,"break in grade",fontsize=8)
ax.text(1.0,-3.0,"mild slope S$_{01}$ = 0.0004",fontsize=8); ax.text(7.0,-4.0,"steep slope S$_{02}$ = 0.015",fontsize=8)
ax.set_xlim(-0.2,12.2); ax.set_ylim(-4.6,2.4)
```

*Length of the M2 curve by the direct step method.* Starting at the upstream end $y=0.99y_{n1}=1.887$ m (the curve is asymptotic to the normal depth, so exactly $y_{n1}$ would need infinite length) and ending at $y_c=0.612$ m, in three steps of equal depth change $\Delta y=0.425$ m. At each depth: $A=4y$, $R=\dfrac{4y}{4+2y}$, $V=Q/A$, $E=y+\dfrac{V^2}{2g}$, $S_f=\dfrac{n^2V^2}{R^{4/3}}$ and

$$\begin{gathered}\Delta x=\frac{E_2-E_1}{S_0-\bar S_f} \\ \bar S_f=\tfrac12(S_{f1}+S_{f2})\end{gathered}$$

| Step | $y_1\to y_2$ (m) | $E_1$ (m) | $E_2$ (m) | $S_{f1}$ | $S_{f2}$ | $S_0-\bar S_f$ | $\Delta x$ (m) |
|---|---|---|---|---|---|---|---|
| 1 | 1.887 → 1.462 | 1.919 | 1.516 | 0.000411 | 0.000824 | −0.000217 | 1854 |
| 2 | 1.462 → 1.037 | 1.516 | 1.144 | 0.000824 | 0.002175 | −0.001100 | 338 |
| 3 | 1.037 → 0.612 | 1.144 | 0.918 | 0.002175 | 0.010309 | −0.005842 | 39 |

$$\boxed{L=1854+338+39\approx2231\ \text{m}\ (\approx2.2\ \text{km})}$$

(The M2 curve is mainly spread over the first step, because the depth is close to the normal depth where the gradient is gentle; a finer step would give a slightly different value, but the answer for the three steps asked is about 2.2 km.)
