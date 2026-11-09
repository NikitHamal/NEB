---
file: NEBians-IOE-Past-Paper-Fluid-Mechanics-ENCE201-2082-Kartik.pdf
subject: Fluid Mechanics
level: BE · Year II / Part I
code: ENCE 201
year_bs: 2082 Kartik
cal: BS
year_ad: 2025
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE Civil, Year II / Part I. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) A concrete block (sp. gr. = 2.5) having weight $W$ is tied to the bottom of a slanted rectangular gate (OA) having unit width with the help of a cable (ABC) mounted on a pulley system as shown in the figure below. The slanted gate has a weight of 2 kN and is hinged at point O to allow opening and closing of the gate. Determine the volume of the concrete block ($V$) if the block is just about to open the gate in the condition shown by the figure. [[6]]

```figure caption="Question 1(a): water depth 6 m; hinge O is 4 m above the floor; the gate OA is inclined at 60° to the floor (A on the floor); the cable from A passes over the pulley B to the submerged concrete block W (C). The cable AB is read from the scale of the original figure as rising about 2 m over a horizontal distance of 5 m (about 21.8° to the horizontal)."
import matplotlib.patches as mp, numpy as _np
fig,ax=plt.subplots(figsize=(5.6,3.7)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((-1,0),9.3,6,fc="#d6e6f5",ec="none"))
ax.plot([-1,8.31+0.4],[0,0],color=INK,lw=1.6); ax.plot([-1,8.3],[6,6],color=INK,lw=1.0,ls="--")
ax.add_patch(mp.Rectangle((8.31,4),0.5,3.4,fc="#c3c9d1",ec=INK,lw=1.0,hatch="////"))
ax.plot([6,8.31],[0,4],color=INK,lw=3.2); ax.plot([8.31],[4],"o",color=INK,ms=5)
ax.text(8.5,3.6,"O",fontsize=9); ax.text(5.9,-0.7,"A",fontsize=9)
ax.text(6.35,0.35,"60°",fontsize=8)
ax.plot([6,1.2],[0,2.0],color=INK,lw=1.2); ax.add_patch(mp.Circle((1.0,2.0),0.3,fc="white",ec=INK,lw=1.2)); ax.text(1.0,2.5,"B",fontsize=9,ha="center")
ax.plot([0.7,0.7],[2.0,0.8],color=INK,lw=1.2)
ax.add_patch(mp.Rectangle((0.2,0.0),1.0,0.8,fc="#8b929c",ec=INK,lw=1.0)); ax.text(0.7,0.4,"W",fontsize=8.5,ha="center",va="center",color="white"); ax.text(0.7,1.1,"C",fontsize=8,ha="center")
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
ax.annotate("",xy=(-1.5,0),xytext=(-1.5,6),arrowprops=ar); ax.text(-1.7,3,"6 m",ha="right",va="center",fontsize=8)
ax.annotate("",xy=(9.4,0),xytext=(9.4,4),arrowprops=ar); ax.text(9.55,2,"4 m",va="center",fontsize=8)
ax.set_xlim(-3.2,10.6); ax.set_ylim(-1.2,7.6)
```

b) A jet of water from a nozzle is deflected through 60° from its original direction by a curved plate which it enters tangentially without shock with a velocity of 30 m/s and leaves with a mean velocity of 25 m/s. If the discharge from the nozzle is 0.8 kg/s, calculate the magnitude and direction of the resultant force on the vane, if the vane is stationary. [[6]]

@q 2
a) The performance of a spillway of a power project is to be studied utilizing a model constructed to a scale of 1:9. Neglecting the viscous and surface tension effect, determine: [[3+3]]

(i) The rate of flow in the model for a prototype discharge of 1000 m³/s and

(ii) The dissipation of energy in the prototype hydraulic jump, if the jump in the model studies dissipates 0.4 horsepower.

b) The figure shows a pressure gauge with the following particulars: the cross-sectional area of each of the bulbs L and M = 1200 mm²; the cross-sectional area of each vertical limb = 30 mm²; the specific gravity of the liquid filled in bulb M = 0.9. If the surface of separation is in the limb attached to M, find the displacement of the surface of separation when the pressure on the surface in M is greater than that in L by an amount equal to 20 mm of head of water. [[6]]

```figure caption="Question 2(b): two-liquid differential gauge. Bulb L holds water (S = 1.0), bulb M holds a liquid of S = 0.9; X–X is the initial and Z–Z the final level of the surface of separation. The extra pressure of 20 mm of water acts on the surface in M."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.8,3.3)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((0,8),3,3,fc="#cfe3f5",ec=INK,lw=1.2)); ax.text(1.5,9.5,"water\nS = 1.0",ha="center",va="center",fontsize=7.5); ax.text(-0.4,9.5,"L",ha="right",fontsize=9)
ax.add_patch(mp.Rectangle((6,8),3,3,fc="#f0d9a8",ec=INK,lw=1.2)); ax.text(7.5,9.5,"liquid\nS = 0.9",ha="center",va="center",fontsize=7.5); ax.text(9.4,9.5,"M",fontsize=9)
ax.plot([1.2,1.2,7.8,7.8],[8,1,1,8],color=INK,lw=1.2); ax.plot([1.8,1.8,7.2,7.2],[8,1.6,1.6,8],color=INK,lw=1.2)
ax.add_patch(mp.Rectangle((1.2,1),0.6,7,fc="#cfe3f5",ec="none")); ax.add_patch(mp.Rectangle((1.2,1),6.6,0.6,fc="#cfe3f5",ec="none")); ax.add_patch(mp.Rectangle((7.2,1),0.6,3.3,fc="#cfe3f5",ec="none"))
ax.add_patch(mp.Rectangle((7.2,4.3),0.6,3.7,fc="#f0d9a8",ec="none"))
ax.plot([-0.5,9],[4.3,4.3],color=MUTED,lw=0.8,ls="--"); ax.text(-0.6,4.3,"X",ha="right",va="center",fontsize=8)
ax.plot([-0.5,9],[3.0,3.0],color=MUTED,lw=0.8,ls="--"); ax.text(-0.6,3.0,"Z",ha="right",va="center",fontsize=8)
ax.annotate("",xy=(9.6,4.3),xytext=(9.6,3.0),arrowprops=dict(arrowstyle="<->",color=INK,lw=0.8)); ax.text(9.8,3.5,"z",fontsize=8.5)
ax.annotate("",xy=(7.5,12.4),xytext=(7.5,11.1),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.3)); ax.text(5.0,12.0,"+20 mm water",fontsize=7.5,color="#d9534f")
ax.set_xlim(-2,11); ax.set_ylim(0,13)
```

@q 3
a) Derive Euler's equation of motion and hence deduce Bernoulli's equation from the derived equation. Mention the basic assumptions and explain each term of Bernoulli's with neat diagram. [[6]]

b) A smooth flat plate 2.0 m wide and 2.5 m long is towed in oil (S = 0.8) at a velocity of 1.5 m/s along its length. Find the thickness of the boundary layer and shear stress at the trailing edge of the plate. Also, find the power required for towing the plate. [$\nu=10^{-4}$ m²/s] [[6]]

@q 4
a) Define metacentre and derive an expression for metacentric height determination by analytical method. [[1+5]]

b) Differentiate between the rotational and irrotational flows. If $\phi = 3xy$, find $x$ and $y$ components of velocity at (1, 3) and (3, 3). Determine the discharge between stream lines passing through these points. [[2+4]]

@q 5
a) The depth of water in a 300 m wide rectangular river is 2 m and the velocity of flow is 0.6 m/s. What should be the height of weir to be built across the river if the depth of water in the river upstream side of the weir is not to exceed 3.5 m. Consider velocity of approach and take coefficient of discharge for the weir as 0.62. [[6]]

b) A solid cone of radius $r_0$ and vertex angle $2\theta$ is to rotate at an angular velocity $\omega$. An oil of viscosity $\mu$ and thickness $h$ fills the gap between the cone and the housing. Determine torque $T$ required to rotate the cone. [[6]]

```figure caption="Question 5(b): solid cone of base radius r₀ and vertex (semi-)angle θ rotating at ω inside a conical housing; oil film of thickness h."
import matplotlib.patches as mp, numpy as _np
fig,ax=plt.subplots(figsize=(3.6,3.2)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Polygon([(-2.2,3),(2.2,3),(0,-1.2)],closed=True,fc="#e8d9a8",ec="none"))
ax.add_patch(mp.Polygon([(-2.0,3),(2.0,3),(0,-0.9)],closed=True,fc="white",ec=INK,lw=1.2))
ax.plot([-0.12,-0.12,0.12,0.12],[3,4.1,4.1,3],color=INK,lw=1.2)
ax.annotate("",xy=(0,4.5),xytext=(0,3.2),arrowprops=dict(arrowstyle="-",color="none"))
ax.annotate("",xy=(0.0,0.0),xytext=(2.0,3.0),arrowprops=dict(arrowstyle="-",color="none"))
ax.annotate("",xy=(2.0,3.35),xytext=(0,3.35),arrowprops=dict(arrowstyle="<->",color=INK,lw=0.8)); ax.text(1.0,3.5,"r₀",ha="center",fontsize=9)
ax.text(0,1.0,"2θ",ha="center",fontsize=9); ax.text(2.0,0.6,"oil, h",fontsize=8)
ax.text(0.45,4.3,"ω",fontsize=10)
ax.set_xlim(-2.8,3.4); ax.set_ylim(-1.5,4.8)
```

<!-- SOLUTIONS -->

@s 1
**(a) Gate OA.** Take unit width. Geometry: the floor is 6 m below the water surface and O is 4 m above the floor, so O is **2 m below the surface**. The gate is inclined at $60^\circ$:

$$\begin{gathered}L=\frac{4}{\sin60^\circ}=4.619\ \text{m} \\ \text{A is at depth }6\ \text{m}\end{gathered}$$

*Water force on the gate* (water on the upper face): depth of the centroid $\bar h=\dfrac{2+6}{2}=4$ m.

$$F=\gamma\bar hA=9.81(4)(4.619\times1)=181.24\ \text{kN}$$

*Centre of pressure.* Distance of the centroid from the free surface along the slope is $\bar y=\bar h/\sin60^\circ=4.619$ m, so

$$\bar y_{cp}=\bar y+\frac{I_G}{A\bar y}=4.619+\frac{L^2}{12\,\bar y}=4.619+\frac{21.33}{12(4.619)}=5.004\ \text{m}$$

Distance of the centre of pressure from the hinge O along the gate: $s=5.004-\dfrac{2}{\sin60^\circ}=5.004-2.309=2.694$ m. The moment of the water force about O (it tends to *close* the gate):

$$M_w=181.24(2.694)=488.3\ \text{kN·m}$$

*Gate weight.* $W_g=2$ kN acts at the middle of OA, whose horizontal distance from O is $(L/2)\cos60^\circ=1.155$ m, and it also resists opening:

$$M_g=2(1.155)=2.31\ \text{kN·m}$$

*Cable pull.* The block is submerged, so the tension in the cable is its weight less its buoyancy:

$$T=W-F_B=(\gamma_c-\gamma_w)V=(2.5-1)(9.81)V=14.715\,V\ \text{kN}$$

The cable acts at A and pulls it towards the pulley B, i.e. at an angle $\alpha$ above the horizontal ($\tan\alpha=2/5$ from the figure, $\alpha=21.8^\circ$). The position of A relative to O is $(-2.309,\,-4.0)$ m, so the moment arm of $T$ about O is

$$r_T=2.309\sin\alpha+4.0\cos\alpha=2.309(0.3714)+4.0(0.9285)=4.572\ \text{m}$$

*Gate just about to open:* the opening moment equals the closing moments:

$$T\,(4.572)=488.3+2.31\ \Rightarrow\ T=107.3\ \text{kN}$$

$$\begin{gathered}\boxed{V=\frac{107.3}{14.715}=7.29\ \text{m}^3} \\ (W=\gamma_cV=178.8\ \text{kN})\end{gathered}$$

(If the cable AB were taken horizontal the arm would be 4.0 m, giving $T=122.7$ kN and $V=8.34$ m³; the angle must be taken from the figure.)

**(b) Jet on a stationary curved vane.** The jet enters at 30 m/s along the $x$ axis and leaves at 25 m/s after being turned through $60^\circ$ (upward). Mass flow rate $\dot m=0.8$ kg/s. For a stationary vane the force on the fluid equals the rate of change of momentum:

$$\begin{gathered}F_x=\dot m\,(V_1-V_2\cos60^\circ)=0.8(30-25\cos60^\circ)=14.0\ \text{N}\\ F_y=\dot m\,(0-V_2\sin60^\circ)\ \Rightarrow\ |F_y|=0.8(25)(0.8660)=17.32\ \text{N}\end{gathered}$$

(these are the forces exerted *by the vane on the water* in the $x$ direction and ($-$) $y$ direction; the water exerts the same forces in the opposite sense on the vane). The force of the jet on the vane is therefore 14.0 N along the original direction of the jet and 17.32 N downward (the jet is deflected upward, so the vane is pushed down):

$$\boxed{R=\sqrt{14.0^2+17.32^2}=22.27\ \text{N}}$$

$$\theta=\tan^{-1}\frac{17.32}{14.0}=\boxed{51.05^\circ\ \text{to the original direction of the jet, on the side opposite to the deflection}}$$

@s 2
**(a) Spillway model (Froude law).** Gravity governs, so $Fr_m=Fr_p$. With scale $L_r=L_p/L_m=9$ and the same fluid ($\rho_r=g_r=1$): $V_r=L_r^{1/2}$.

**(i) Discharge:** $Q_r=V_rL_r^2=L_r^{5/2}=9^{2.5}=243$.

$$\boxed{Q_m=\frac{Q_p}{243}=\frac{1000}{243}=4.115\ \text{m}^3/\text{s}}$$

**(ii) Power dissipated.** $P=\gamma QH$ so $P_r=Q_rH_r=L_r^{5/2}L_r=L_r^{7/2}=9^{3.5}=2187$.

$$\begin{gathered}P_p=0.4(2187)=874.8\ \text{hp} \\ \boxed{P_p=874.8(0.7457)=652\ \text{kW}}\end{gathered}$$

**(b) Two-liquid pressure gauge.** Let $A=1200$ mm² (bulb), $a=30$ mm² (limb), $S_M=0.9$. When the pressures are equal, the interface stands at X–X and the two liquid levels are such that $\gamma_wh_L=\gamma_Mh_M$, i.e. $h_L=0.9\,h_M$.

The pressure on M is raised by $\Delta p=\gamma_w(20\ \text{mm})$; the interface moves **down** a distance $z$ in the M limb. By volume conservation the surface in bulb M falls by $\delta$ and the water surface in bulb L rises by $\delta$, where

$$\delta A=z\,a\ \Rightarrow\ \delta=z\frac{a}{A}=\frac{z}{40}$$

Equate the pressures at the new level Z–Z (in the M limb) calculated from the M side and from the L side:

$$\begin{gathered}p_M+\gamma_M\big[(h_M-\delta)+z\big]=p_L+\gamma_w\big[(h_L+\delta)+z\big]\\ p_M-p_L=\gamma_w\big(h_L-S_Mh_M\big)+\gamma_w\big[\delta(1+S_M)+z(1-S_M)\big]\end{gathered}$$

The first bracket vanishes ($\gamma_wh_L=\gamma_Mh_M$). Thus

$$p_M-p_L=\gamma_w\,z\left[(1-S_M)+(1+S_M)\frac{a}{A}\right]=\gamma_w\,z\,[0.1+1.9(0.025)]=0.1475\,\gamma_w z$$

Setting $p_M-p_L=\gamma_w(20\ \text{mm})$:

$$\boxed{z=\frac{20}{0.1475}=135.6\ \text{mm}}$$

(the surface of separation moves down by about 136 mm in the limb attached to M; the surface in M falls 3.4 mm and that in L rises 3.4 mm).

@s 3
**(a) Euler's equation.** *Assumptions:* the fluid is ideal (inviscid, so no shear), the flow is steady, along a single streamline, and the fluid is incompressible (for Bernoulli); the only forces are pressure and gravity.

Consider a small cylindrical element of length $ds$ and cross-section $dA$ along a streamline inclined at $\theta$ to the horizontal, with velocity $v$ at $s$. Forces along the streamline:

- pressure force on the upstream face $p\,dA$ and downstream face $-(p+\frac{\partial p}{\partial s}ds)dA$;
- weight component $-\rho g\,dA\,ds\cos\theta$, with $\cos\theta=\dfrac{dz}{ds}$.

Newton's second law ($F=ma_s$, $a_s=v\dfrac{\partial v}{\partial s}+\dfrac{\partial v}{\partial t}$; the mass is $\rho\,dA\,ds$):

$$-\frac{\partial p}{\partial s}ds\,dA-\rho g\,dA\,ds\frac{dz}{ds}=\rho\,dA\,ds\,a_s$$

Dividing by $\rho\,dA\,ds$ gives the **Euler equation** along a streamline:

$$\boxed{\frac{1}{\rho}\frac{\partial p}{\partial s}+g\frac{dz}{ds}+v\frac{\partial v}{\partial s}+\frac{\partial v}{\partial t}=0}\quad\text{or, for steady flow, }\ \frac{dp}{\rho}+g\,dz+v\,dv=0$$

*Bernoulli's equation.* For incompressible flow ($\rho$ constant), integrating the steady form:

$$\frac{p}{\rho}+gz+\frac{v^2}{2}=\text{constant}\ \Rightarrow\ \boxed{\frac{p}{\gamma}+\frac{v^2}{2g}+z=H=\text{constant}}$$

*Terms (each is an energy per unit weight, i.e. a length):* $\dfrac{p}{\gamma}$ is the **pressure head** (flow work), $\dfrac{v^2}{2g}$ the **velocity (kinetic) head**, $z$ the **datum (potential) head** above an arbitrary datum; $H$ is the **total head**, the same at all sections along the streamline. The hydraulic grade line (HGL) plots $p/\gamma+z$ and the energy grade line (EGL) plots $H$; the EGL lies a distance $v^2/2g$ above the HGL (see the figure).

```figure caption="Question 3(a): Bernoulli's equation for a streamline in a pipe. The energy line is horizontal for an ideal fluid; the hydraulic grade line lies v²/2g below it, and the pipe centre-line is z above the datum."
fig,ax=plt.subplots(figsize=(5.2,2.7)); ax.axis("off")
ax.plot([0,10],[3.2,3.2],color="#d9534f",lw=1.6); ax.text(10.1,3.2,"EGL",fontsize=8,va="center",color="#d9534f")
ax.plot([0,3,4.5,7,10],[2.7,2.7,2.0,2.0,2.2],color=ACCENT,lw=1.6)
ax.text(10.1,2.2,"HGL",fontsize=8,va="center",color=ACCENT)
ax.plot([0,3,4.5,7,10],[0.9,0.9,0.6,0.6,0.8],color=INK,lw=3); ax.plot([0,10],[0,0],color=MUTED,lw=0.9,ls="--"); ax.text(10.1,0,"datum",fontsize=8,va="center")
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
ax.annotate("",xy=(1.5,3.2),xytext=(1.5,2.7),arrowprops=ar); ax.text(1.65,2.95,"v²/2g",fontsize=8)
ax.annotate("",xy=(1.5,2.7),xytext=(1.5,0.9),arrowprops=ar); ax.text(1.65,1.75,"p/γ",fontsize=8)
ax.annotate("",xy=(1.5,0.9),xytext=(1.5,0),arrowprops=ar); ax.text(1.65,0.35,"z",fontsize=8)
ax.text(5.6,3.35,"total head H = p/γ + v²/2g + z",fontsize=8,ha="center")
ax.set_xlim(-0.5,11.5); ax.set_ylim(-0.3,3.8)
```

**(b) Flat plate towed in oil.** $L=2.5$ m, $b=2.0$ m, $U=1.5$ m/s, $\nu=10^{-4}$ m²/s, $\rho=0.8(1000)=800$ kg/m³.

$$Re_L=\frac{UL}{\nu}=\frac{1.5(2.5)}{10^{-4}}=37\,500<5\times10^5\ \Rightarrow\ \text{laminar boundary layer}$$

*Thickness at the trailing edge* (Blasius):

$$\delta=\frac{5L}{\sqrt{Re_L}}=\frac{5(2.5)}{\sqrt{37500}}=\frac{12.5}{193.65}=\boxed{0.0645\ \text{m}\approx64.5\ \text{mm}}$$

*Local shear stress at the trailing edge:*

$$\tau_0=\frac{0.332\,\rho U^2}{\sqrt{Re_L}}=\frac{0.332(800)(1.5)^2}{193.65}=\boxed{3.09\ \text{N/m}^2}$$

*Drag and power.* Average drag coefficient $C_D=\dfrac{1.328}{\sqrt{Re_L}}=0.006858$. Wetted area of one face $A=2.0\times2.5=5$ m²:

$$F_D=C_D\tfrac12\rho U^2A=0.006858(0.5)(800)(1.5)^2(5)=30.86\ \text{N}\ (\text{one side})$$

$$P=F_DU=30.86(1.5)=46.3\ \text{W (one side)}$$

For a plate towed with **both faces** wetted the drag doubles: $F_D=61.7$ N and

$$\boxed{P=2(46.3)=92.6\ \text{W}\approx0.093\ \text{kW}}$$

@s 4
**(a) Metacentre.** The *metacentre* M is the point about which a floating (or submerged) body starts to oscillate when it is tilted through a small angle; it is the point of intersection of the line of buoyancy in the displaced position with the original vertical axis through the centre of buoyancy B. The *metacentric height* $GM$ is the distance between the centre of gravity G and M; the body is stable if M lies above G ($GM>0$).

**Analytical derivation.** Let the body (displaced volume $V$) heel through a small angle $\theta$ about the axis through the centroid O of the water-line plane. A wedge of volume on one side goes into the water and an equal wedge comes out of the other. At a distance $x$ from the axis the wedge has depth $x\theta$, so an element of the water-line area $dA$ has the volume $x\theta\,dA$ and a buoyancy moment $\gamma\,x\theta\,dA\cdot x$ about the axis. The total moment of the transferred buoyancy is

$$M_w=\gamma\theta\int x^2dA=\gamma\,\theta\,I$$

where $I$ is the second moment of the water-line area about the tilting axis. The same moment equals the total buoyancy $\gamma V$ times the horizontal shift $BB_1$ of the centre of buoyancy:

$$\gamma V\cdot BB_1=\gamma\theta I\ \Rightarrow\ BB_1=\frac{I\theta}{V}$$

From the geometry (small angle) $BB_1=BM\,\theta$, so

$$\begin{gathered}\boxed{BM=\frac{I}{V}} \\ \boxed{GM=BM-BG=\frac{I}{V}-BG}\end{gathered}$$

($BG$ is positive when G is above B, negative when G is below B.) The restoring couple is $W\,GM\sin\theta$; $GM>0$ stable, $GM=0$ neutral, $GM<0$ unstable. For a rectangular barge of width $B$ and length $L$: $I=LB^3/12$.

**(b) Rotational and irrotational flow.** In *rotational* flow the fluid particles rotate about their own axes while moving, the vorticity $\omega_z=\tfrac12\left(\frac{\partial v}{\partial x}-\frac{\partial u}{\partial y}\right)\neq0$ (for example flow in a boundary layer or a free vortex with forced rotation); no velocity potential exists. In *irrotational* flow the particles have no net rotation, $\omega_z=0$, so a velocity potential exists and $\nabla^2\phi=0$ (for example a free vortex outside the core, flow towards a sink).

*Velocity components* from $\phi=3xy$ (convention $u=-\partial\phi/\partial x$, $v=-\partial\phi/\partial y$):

$$\begin{gathered}u=-3y \\ v=-3x\end{gathered}$$

| Point | $u$ (m/s) | $v$ (m/s) | resultant (m/s) |
|---|---|---|---|
| (1, 3) | $-9$ | $-3$ | 9.49 |
| (3, 3) | $-9$ | $-9$ | 12.73 |

*Stream function* ($u=\partial\psi/\partial y$, $v=-\partial\psi/\partial x$): $\partial\psi/\partial y=-3y\Rightarrow\psi=-\tfrac32y^2+g(x)$, and $-\partial\psi/\partial x=-3x\Rightarrow g=\tfrac32x^2$, so

$$\psi=\tfrac32\,(x^2-y^2)$$

$$\begin{gathered}\psi_{(1,3)}=\tfrac32(1-9)=-12 \\ \psi_{(3,3)}=\tfrac32(9-9)=0\end{gathered}$$

$$\boxed{q=\psi_2-\psi_1=0-(-12)=12\ \text{m}^2/\text{s per unit width (i.e. 12 m}^3/\text{s per metre depth)}}$$

(With the opposite sign convention the velocities change sign and $\psi=-\tfrac32(x^2-y^2)$, but the discharge between the streamlines is still 12 m³/s per metre.)

@s 5
**(a) Weir across the river.** Discharge in the river:

$$Q=B\,y\,V=300(2)(0.6)=360\ \text{m}^3/\text{s}$$

The upstream depth must not exceed 3.5 m, so the velocity of approach (to the weir) is $V_a=\dfrac{Q}{300(3.5)}=0.3429$ m/s and $h_a=\dfrac{V_a^2}{2g}=\dfrac{(0.3429)^2}{19.62}=0.00599$ m. Let $H$ be the head over the crest and $P$ the weir height; $H+P=3.5$ m. Rectangular weir with velocity of approach:

$$Q=\tfrac23C_dL\sqrt{2g}\left[(H+h_a)^{3/2}-h_a^{3/2}\right]$$

$$360=\tfrac23(0.62)(300)(4.429)\left[(H+0.00599)^{3/2}-0.00599^{3/2}\right]=549.2\left[(H+0.00599)^{3/2}-0.000464\right]$$

$$(H+0.00599)^{3/2}=0.6555+0.00046=0.6560\ \Rightarrow\ H+0.00599=0.7551\ \Rightarrow\ H=0.749\ \text{m}$$

$$\boxed{P=3.5-0.749=2.75\ \text{m}}$$

(Neglecting the approach velocity, $H=0.7545$ m and $P=2.745$ m; the weir should be about 2.75 m high.)

**(b) Torque to rotate the cone.** Let the cone surface be inclined so that the semi-vertex angle is $\theta$; a point at slant distance $s$ from the vertex is at radius $r=s\sin\theta$. The oil film of thickness $h$ is thin, so the velocity gradient is linear: the surface of the cone moves at $\omega r$ and the housing is at rest.

$$\tau=\mu\frac{du}{dy}=\mu\frac{\omega r}{h}$$

Consider a conical ring of slant width $ds=\dfrac{dr}{\sin\theta}$ at radius $r$. Its area is $dA=2\pi r\,ds=\dfrac{2\pi r\,dr}{\sin\theta}$ and the shear force is $dF=\tau\,dA$, so the torque of the element is

$$dT=r\,dF=r\left(\mu\frac{\omega r}{h}\right)\frac{2\pi r\,dr}{\sin\theta}=\frac{2\pi\mu\omega}{h\sin\theta}\,r^3dr$$

$$T=\frac{2\pi\mu\omega}{h\sin\theta}\int_0^{r_0}r^3dr=\frac{2\pi\mu\omega}{h\sin\theta}\frac{r_0^4}{4}$$

$$\boxed{T=\frac{\pi\,\mu\,\omega\,r_0^{4}}{2\,h\,\sin\theta}}$$

(The flat top of the cone is open to the air, so only the conical surface contributes. For $\theta=90^\circ$ the cone becomes a disc and $T=\pi\mu\omega r_0^4/2h$, the standard result for a disc.)
