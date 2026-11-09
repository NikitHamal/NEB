---
file: NEBians-IOE-Past-Paper-Hydraulics-ENCE251-2082-Bhadra.pdf
subject: Hydraulics
level: BE · Year II / Part II
code: ENCE 251
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular examination (new course), BE Civil, Year II / Part II. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Derive an expression for the velocity distribution for steady laminar flow in a circular pipe. [[4]]

b) A pipe network system is used to convey water from tank A to tank G located on the other side of the hill with the help of a siphon. A pump of capacity 5 kW with efficiency $\eta_p$ = 80% is installed to pump the water through the siphon as shown in figure. Determine the discharge flowing through the siphon pipe and the pressure at the summit of the siphon. [[5+3]]

```figure caption="Question 1(b) (schematic of the scanned figure): tank A (water level 3 m above pipe BC) feeds three parallel pipes BC1–BC3, a pump P, pipe DS up to the summit S (10 m above the level of A) and pipe SE down, then three parallel pipes EF1–EF3 into tank G whose water level is 15 m below S."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(6.0,2.8)); ax.axis("off")
ax.add_patch(mp.Rectangle((0,0),1.2,1.6,fc="#cfe3f5",ec=INK)); ax.text(0.6,1.8,"A",fontsize=10,ha="center")
ax.add_patch(mp.Rectangle((10.8,0),1.2,0.9,fc="#cfe3f5",ec=INK)); ax.text(11.4,1.1,"G",fontsize=10,ha="center")
for k,yy in enumerate((0.55,0.35,0.15)): ax.plot([1.2,3.4],[yy,yy],color=INK,lw=2)
ax.text(2.3,0.75,"BC$_1$, BC$_2$, BC$_3$",fontsize=7.5,ha="center"); ax.add_patch(mp.Circle((3.9,0.35),0.25,fc="white",ec=INK)); ax.text(3.9,0.3,"P",fontsize=8,ha="center")
x=np.linspace(4.15,10.0,200); y=0.35+np.where(x<7.0,3.8*np.sin((x-4.15)/(7.0-4.15)*np.pi/2)**1.2*1.0,3.8-(3.8+1.0)*(1-np.cos((x-7.0)/3.0*np.pi/2))*0)
yy=np.where(x<=7.0,0.35+3.65*np.sin((x-4.15)/2.85*np.pi/2),4.0-4.6*np.sin((x-7.0)/3.0*np.pi/2)**1.0)
ax.plot(x,yy,color=INK,lw=2.4); ax.text(4.9,1.9,"D → S\nL = 500, D = 0.5",fontsize=7); ax.text(8.4,3.0,"S → E\nL = 1500, D = 0.5",fontsize=7); ax.text(7.0,4.25,"S",fontsize=10,ha="center")
for yy2 in (-0.45,-0.65,-0.85): ax.plot([10.0,10.8],[-0.25-0.0,-0.25-0.0],lw=0)
for yy2 in (0.5,0.35,0.2): ax.plot([9.4,10.8],[yy2-0.3,yy2-0.3],color=INK,lw=2)
ax.plot([0,10.8],[1.6,1.6],color=MUTED,lw=0.8,ls="--"); ax.annotate("",xy=(7.0,1.6),xytext=(7.0,4.0),arrowprops=dict(arrowstyle="<->",lw=0.8)); ax.text(6.4,2.8,"10 m",fontsize=8)
ax.annotate("",xy=(9.9,0.6),xytext=(9.9,4.0),arrowprops=dict(arrowstyle="<->",lw=0.8)); ax.text(9.95,2.2,"15 m",fontsize=8)
ax.text(5.5,-0.7,"BC: 1000/500/1000 m, D = 0.3 m;  EF: 1000/500/1000 m, D = 0.3 m;  f = 0.02 in all pipes",fontsize=7.5,ha="center")
ax.set_xlim(-0.3,12.4); ax.set_ylim(-1.0,4.7)
```

| Pipe | BC₁ | BC₂ | BC₃ | DS | SE | EF₁ | EF₂ | EF₃ |
|---|---|---|---|---|---|---|---|---|
| L (m) | 1000 | 500 | 1000 | 500 | 1500 | 1000 | 500 | 1000 |
| D (m) | 0.3 | 0.3 | 0.3 | 0.5 | 0.5 | 0.3 | 0.3 | 0.3 |
| f | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |

@q 2
a) Water flowing in an elastic pipeline is brought to rest by instantaneous closure of valve. Explain, with illustration, how positive and negative waves are caused and travel along the pipeline (without considering head loss). Also, draw wave propagation chart at valve end if head losses are considered. [[3+1]]

b) Solve discharges in each pipe of the following pipe network using hardy cross method (Consider two trials only) [[8]]

```figure caption="Question 2(b): pipe network ABCDE. Inflows 80 at A and 20 at B; outflows 50 at C, 20 at D and 30 at E."
fig,ax=plt.subplots(figsize=(5.2,2.7)); ax.axis("off")
P={"A":(0,0),"B":(3.5,0),"C":(8,0),"D":(8,-3.2),"E":(8,-6)}
for a,b in ["AB","BC","CD","DE","BD","AE"]:
    ax.plot([P[a][0],P[b][0]],[P[a][1],P[b][1]],color=INK,lw=3.2)
for k,(x,y) in P.items(): ax.text(x+(-0.3 if k in "AB" else 0.35),y+0.35 if k in "ABC" else y,k,fontsize=10,fontweight="bold")
ar=dict(arrowstyle="-|>",color="#d9534f",lw=1.4)
ax.annotate("",xy=(0,0),xytext=(-1.6,0),arrowprops=ar); ax.text(-1.9,0.05,"80",ha="right",va="center",fontsize=9)
ax.annotate("",xy=(3.5,0),xytext=(3.5,1.4),arrowprops=ar); ax.text(3.5,1.6,"20",ha="center",fontsize=9)
ax.annotate("",xy=(9.6,0),xytext=(8,0),arrowprops=ar); ax.text(9.8,0,"50",va="center",fontsize=9)
ax.annotate("",xy=(9.6,-3.2),xytext=(8,-3.2),arrowprops=ar); ax.text(9.8,-3.2,"20",va="center",fontsize=9)
ax.annotate("",xy=(8,-7.4),xytext=(8,-6),arrowprops=ar); ax.text(8,-7.7,"30",ha="center",fontsize=9)
ax.text(6.0,0.3,"BC",fontsize=7.5); ax.text(1.5,0.3,"AB",fontsize=7.5); ax.text(8.2,-1.6,"CD",fontsize=7.5); ax.text(8.2,-4.6,"DE",fontsize=7.5); ax.text(5.0,-1.9,"BD",fontsize=7.5); ax.text(3.0,-4.1,"AE",fontsize=7.5)
ax.set_xlim(-3,11); ax.set_ylim(-8.2,2.2)
```

| Pipe | AB | BC | CD | BD | DE | AE |
|---|---|---|---|---|---|---|
| L (m) | 1000 | 1000 | 500 | 1500 | 500 | 2000 |
| D (m) | 1.0 | 1.0 | 1.0 | 0.8 | 1.0 | 0.8 |
| f | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |

@q 3
a) Define alternate depths and critical depth with the help of specific energy diagram. Determine the critical depth $y_c$ for a discharge Q passing through an equilateral triangular channel of side length $a$ as shown in figure. [[3+3]]

```figure caption="Question 3(a): equilateral triangular cross-section of side a (60° at the base), water depth y_c above the base."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(3.6,2.7)); ax.axis("off"); a=4; h=a*np.sqrt(3)/2
ax.add_patch(mp.Polygon([[0,0],[a,0],[a/2,h]],fc="white",ec=INK,lw=2))
y=1.5; t=a-2*y/np.sqrt(3); ax.add_patch(mp.Polygon([[0,0],[a,0],[a-y/np.sqrt(3),y],[y/np.sqrt(3),y]],fc="#cfe3f5",ec="none"))
ax.plot([y/np.sqrt(3),a-y/np.sqrt(3)],[y,y],color=ACCENT,lw=1.4); ax.annotate("",xy=(a/2,0),xytext=(a/2,y),arrowprops=dict(arrowstyle="<->",lw=0.8)); ax.text(a/2+0.1,0.7,"y$_c$",fontsize=10)
ax.text(0.55,0.15,"60°",fontsize=8); ax.text(a-1.05,0.15,"60°",fontsize=8); ax.text(a/2,-0.45,"a",ha="center",fontsize=10)
ax.set_xlim(-0.4,a+0.4); ax.set_ylim(-0.8,h+0.3)
```

b) A trapezoidal canal with side slope of 2 horizontal to 1 vertical is to carry a discharge of 50 m³/s. The canal is laid at a slope of 0.005 and the manning's roughness coefficient of the canal is n = 0.018. [[3+3]]

i) What should be the base width $B$ of the canal to carry the given discharge at a uniform depth of 2 m?

ii) If you want to redesign the section to be most economical cross section, what are the revised water depth $y$ and base width $B$?

@q 4
a) Derive an expression for momentum equation and sequent depth ratio for hydraulic jump in a rectangular channel with horizontal bed. [[2+2]]

b) A sluice gate across a wide rectangular channel discharges a stream 0.3 m deep. A jump is created just downstream of the gate with the help of concrete baffle blocks and the flow is passed through a broad crested weir where the flow is critical. Neglecting the losses except the one in the jump, determine the force provided by the blocks to the flow near the hydraulic jump and depth upstream of sluice gate. [[8]]

```figure caption="Question 4(b): sluice gate, stream depth 0.3 m, jump held by baffle blocks (force F), then a broad-crested weir of height Δz = 0.10 m on which the flow is critical with y_c = 1 m."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(6.0,2.3)); ax.axis("off")
ax.plot([0,16],[0,0],color=INK,lw=2); ax.add_patch(mp.Rectangle((9.8,0),3.2,0.3,fc="#bbb",ec=INK,hatch="///"))
ax.add_patch(mp.Polygon([[0,0],[0,4.2],[2.0,4.2],[2.0,0.3],[16,0.3],[16,0]],fc="#cfe3f5",ec="none"))
ax.plot([0,2.0],[4.2,4.2],color=ACCENT,lw=1.4); ax.plot([2.0,2.0],[5.0,0.6],color=INK,lw=3)
ax.plot([2.1,5.0],[0.5,0.55],color=ACCENT,lw=1.4); ax.plot([5.0,7.0,7.4,9.8],[0.55,1.7,1.9,1.9],color=ACCENT,lw=1.4)
ax.add_patch(mp.Rectangle((4.8,0),0.5,0.45,fc="#bbb",ec=INK,hatch="///")); ax.annotate("",xy=(4.1,0.2),xytext=(4.8,0.2),arrowprops=dict(arrowstyle="->",color="#d9534f",lw=1.5)); ax.text(3.7,0.45,"F",color="#d9534f",fontsize=10)
ax.plot([9.8,13.0],[1.9,1.3],color=ACCENT,lw=1.4); ax.plot([13,16],[1.3,0.9],color=ACCENT,lw=1.4)
ax.text(11.1,1.8,"y$_c$ = 1 m",fontsize=8); ax.text(10.5,0.05,"Δz = 0.10 m",fontsize=8); ax.text(3.0,1.0,"0.3 m",fontsize=8)
ax.set_xlim(-0.3,16.2); ax.set_ylim(-0.3,5.2)
```

@q 5
a) Derive an expression for governing equation or dynamic equation of gradually varied flow. Draw possible water surface for the following combinations. [[2+2]]

```figure caption="Question 5(a): a channel whose bed changes from a mild slope (with a sluice gate) through a critical slope to a steep slope; CDL and NDL are the critical and normal depth lines."
fig,ax=plt.subplots(figsize=(5.8,2.4)); ax.axis("off")
x=np.linspace(0,12,200); bed=-0.03*x-np.where(x>8,0.3*(x-8),0)-np.where(x>4,0.05*(x-4),0)
ax.plot(x,bed,color=INK,lw=2.5); ax.plot(x,bed+1.2,color=MUTED,lw=0.9,ls="--"); ax.plot(x,bed+0.7,color=MUTED,lw=0.9,ls=":")
ax.plot([4.3,4.3],[bed[72]+0,bed[72]+2.8],color=INK,lw=3); ax.text(4.1,bed[72]+3.0,"sluice gate",fontsize=8)
ax.text(0.2,0.45,"mild slope",fontsize=8); ax.text(5.0,-0.65,"critical slope",fontsize=8); ax.text(9.3,-2.9,"steep slope",fontsize=8)
ax.text(11.6,bed[-1]+1.3,"NDL",fontsize=7.5); ax.text(11.6,bed[-1]+0.65,"CDL",fontsize=7.5)
ax.set_xlim(-0.5,13); ax.set_ylim(-4.2,3.6)
```

b) A sluice gate discharge 2 m³/s/m into a wide horizontal rectangular channel. The depth at the vena-contracta is 0.15 m. The tail water depth is 1.80 m. Assuming the channel to have a Manning's 'n' of 0.015, determine the location of the hydraulic jump. Use direct step method with three steps. [[8]]

OR

A rectangular channel 10 m wide is laid with a break in its bottom slope from 0.01 to 0.0064. If it carries discharge of 12.5 m³/s per meter width, determine the nature of surface profile and compute its length. Use direct step computation method with n = 0.015. [[8]]

<!-- SOLUTIONS -->

@s 1
**(a) Velocity distribution for steady laminar flow in a circular pipe (Hagen–Poiseuille).** Take a pipe of radius $R$ with horizontal axis and a coaxial cylinder of radius $r$ and length $L$. Steady uniform flow requires the pressure force to balance the viscous shear force on the curved surface ($\Delta p=p_1-p_2$):

$$\Delta p\,\pi r^2=\tau\,(2\pi rL)\ \Rightarrow\ \tau=\frac{\Delta p}{2L}\,r$$

Newton's law of viscosity for laminar flow, with $v$ decreasing as $r$ increases: $\tau=-\mu\dfrac{dv}{dr}$. Hence

$$\frac{dv}{dr}=-\frac{\Delta p}{2\mu L}\,r\ \Rightarrow\ v=-\frac{\Delta p}{4\mu L}r^2+C$$

The no-slip condition $v=0$ at $r=R$ gives $C=\dfrac{\Delta p\,R^2}{4\mu L}$:

$$\boxed{v=\frac{\Delta p}{4\mu L}\left(R^2-r^2\right)=v_{max}\left[1-\left(\frac rR\right)^2\right]}$$

a paraboloid of revolution, with $v_{max}=\dfrac{\Delta pR^2}{4\mu L}$ at the axis. The discharge is $Q=\int_0^R v\,2\pi r\,dr=\dfrac{\pi R^4\Delta p}{8\mu L}$ (Hagen–Poiseuille law), the mean velocity is $\bar V=\dfrac{v_{max}}{2}$, and the head loss is $h_f=\dfrac{\Delta p}{\gamma}=\dfrac{32\mu \bar VL}{\gamma D^2}$.

**(b) Siphon with a pump.** *Head-loss coefficients*, $h_f=KQ^2$ with $K=\dfrac{8fL}{\pi^2gD^5}$. For the parallel sets the head loss across each of the three pipes is equal, so $Q_i=\sqrt{h/K_i}$ and the equivalent coefficient is $\dfrac1{\sqrt{K_{eq}}}=\sum\dfrac1{\sqrt{K_i}}$:

| Pipe(s) | $K$ (s²/m⁵) |
|---|---|
| BC₁ (1000 m, 0.3 m), BC₃ | 680.1 each |
| BC₂ (500 m, 0.3 m) | 340.0 |
| **BC (parallel set)** | $\dfrac{1}{\left(2/\sqrt{680.1}+1/\sqrt{340.0}\right)^2}=58.34$ |
| DS (500 m, 0.5 m) | 26.44 |
| SE (1500 m, 0.5 m) | 79.32 |
| **EF (parallel set, same as BC)** | 58.34 |

Total $K_t=58.34+26.44+79.32+58.34=222.44$ s²/m⁵ (minor losses neglected).

*Levels.* The water surface of A is the datum. The summit S is 10 m above it, and the water level in G is 15 m below S, i.e. **5 m below** that of A. So the static lift is negative: the water falls 5 m from A to G, but the friction losses exceed this, so the pump supplies the difference.

*Pump head.* Power delivered to the water $=\eta P=0.8(5)=4$ kW, so $H_p=\dfrac{4000}{\gamma Q}=\dfrac{4000}{9810\,Q}$.

*Energy equation from the water surface in A to that in G* (both at atmospheric pressure and at rest):

$$0+H_p=-5+K_tQ^2\ \Rightarrow\ \frac{0.4078}{Q}+5=222.44\,Q^2$$

Solving by trial: $Q=0.18$: LHS $=7.27$, RHS $=7.21$; $Q=0.1806$: LHS $=7.258$, RHS $=7.257$. Thus

$$\boxed{Q=0.1806\ \text{m}^3/\text{s}=180.6\ \text{L/s}}$$

with pump head $H_p=2.26$ m and total friction loss $7.26$ m. The three pipes of the BC (and EF) group carry 52.9, 74.8 and 52.9 L/s; the loss in the set is $58.34(0.1806)^2=1.90$ m, in DS 0.86 m and in SE 2.59 m.

*Pressure at the summit S.* Energy equation from A to S (the pump lies on the way, between C and D): the velocity in the 0.5 m pipe is $V_S=\dfrac{0.1806}{\frac\pi4(0.5)^2}=0.92$ m/s, $\dfrac{V_S^2}{2g}=0.043$ m:

$$0+H_p=10+\frac{p_S}{\gamma}+\frac{V_S^2}{2g}+h_{BC}+h_{DS}$$

$$2.257=10+\frac{p_S}{\gamma}+0.043+1.903+0.863\ \Rightarrow\ \frac{p_S}{\gamma}=-10.55\ \text{m of water}$$

$$\boxed{p_S\approx-103.5\ \text{kN/m}^2\ (\text{gauge})}$$

*Remark.* This is below the practical limit for a siphon (about $-10.3$ m of water at sea level, i.e. $-101$ kPa, near the vapour pressure), so with the data as printed the water would vaporise (cavitation / air release) at the summit and the siphon would not run full. In practice the summit should be lowered, or the flow reduced, or the pump placed on the downstream side of the summit.

@s 2
**(a) Water hammer on instantaneous closure (frictionless pipe).** Let a pipe of length $L$, wave speed $c$, initial head $H_0$ and velocity $V_0$ be connected to a reservoir at the upstream end and a valve at the downstream end. The closed valve suddenly stops the flow. Let $\Delta H=\dfrac{cV_0}{g}$.

| Interval | What happens | State of the pipe |
|---|---|---|
| $0<t<L/c$ | The layer next to the valve is stopped, its kinetic energy is changed into strain energy; the fluid is compressed and the pipe wall expanded. A **positive pressure wave ($+\Delta H$)** travels upstream at speed $c$, bringing the fluid it passes to rest. | At $t=L/c$: whole pipe at $H_0+\Delta H$, $V=0$ |
| $L/c<t<2L/c$ | The wave reaches the reservoir, where the head is fixed at $H_0$. The compressed fluid is unbalanced and flows out into the reservoir, so the wave is reflected as a **negative wave ($-\Delta H$)** which travels downstream. Pressure falls back to $H_0$, the velocity is $-V_0$ (towards the reservoir). | At $t=2L/c$: whole pipe at $H_0$, $V=-V_0$ |
| $2L/c<t<3L/c$ | The negative wave reaches the closed valve, where the fluid cannot flow out, so it stops and the pressure drops to $H_0-\Delta H$; a **negative wave** reflects upstream. | At $t=3L/c$: whole pipe at $H_0-\Delta H$, $V=0$ |
| $3L/c<t<4L/c$ | At the reservoir the low pressure draws water in: reflection as a **positive wave** ($+\Delta H$) which restores the pressure to $H_0$ and velocity $+V_0$. | At $t=4L/c$: initial conditions, and the cycle repeats |

The period of the pressure oscillation is $4L/c$. Without friction the oscillation never dies out; the pressure at the valve alternates between $H_0+\Delta H$ and $H_0-\Delta H$ as a square wave. The same sequence of events is shown below, and the valve-end chart with head loss.

```figure caption="Pressure head at the valve end after instantaneous closure: (left) frictionless pipe, a square wave of period 4L/c between H0 + ΔH and H0 − ΔH; (right) with head loss, the steps decay and the head settles to the static value."
fig,axs=plt.subplots(1,2,figsize=(5.9,2.5),sharey=True)
t=np.linspace(0,8,801); L=1.0
sq=np.where((t%4)<2,1,-1)
axs[0].step(t,sq,where="post",color=ACCENT,lw=2); axs[0].axhline(0,color=INK,lw=0.8)
axs[0].set_title("without friction",fontsize=8.5)
ti=np.arange(0,9,2.0); amps=[1,.78,.55,.38,.24]; 
tt=[];hh=[]
for k in range(4):
    tt+= [2*k*1.0,2*(k+1)*1.0]; 
sig=1; xs=[0]; ys=[0]
lvl=[1,-.82,.62,-.45,.31,-.21]
for k,l in enumerate(lvl):
    xs+=[2*k,2*k]; ys+=[ys[-1],l]
xs.append(12); ys.append(lvl[-1])
axs[1].plot(np.array(xs)*0.67,ys,color="#d9534f",lw=2); axs[1].axhline(0,color=INK,lw=0.8); axs[1].set_title("with head loss",fontsize=8.5)
for ax in axs: ax.set_xlabel("time  (units of L/c)",fontsize=8); ax.tick_params(labelsize=0); ax.grid(True,color=GRID,lw=0.5)
axs[0].set_ylabel("H − H$_0$",fontsize=8); axs[0].text(0.1,1.12,"+ΔH",fontsize=8); axs[0].text(2.1,-1.35,"−ΔH",fontsize=8); axs[0].set_ylim(-1.5,1.5)
fig.tight_layout()
```

*Chart with head loss.* When friction is considered, each reflection loses part of the energy: the positive and negative peaks at the valve become progressively smaller (the head rises to $H_0+\Delta H$, falls to about $H_0-0.8\,\Delta H$, then rises to about $H_0+0.6\,\Delta H$, etc.), the pressure is no longer uniform in the pipe (it is a series of sloping steps because of the continuous friction drop), and the oscillation decays to the new steady head, which for a closed valve is the reservoir head $H_0$.

**(b) Hardy Cross analysis** (two trials). Relative resistances $r=K/K_{AB}$ (all pipes have $f=0.02$; $K=8fL/\pi^2gD^5$ and the common factor cancels in the correction):

| Pipe | AB | BC | CD | BD | DE | AE |
|---|---|---|---|---|---|---|
| $L/D^5$ | 1000 | 1000 | 500 | 4577.6 | 500 | 6103.5 |
| relative $r$ | 1 | 1 | 0.5 | 4.578 | 0.5 | 6.104 |

*Initial flows* (units of the data) satisfying continuity at each node: AB = 60, AE = 20, BC = 60, BD = 20, CD = 10 (C→D), DE = 10 (D→E). Check: A $80=60+20$; B $60+20=60+20$; C $60=50+10$; D $20+10=20+10$; E $20+10=30$. ✔

*Loops:* **I** = B→C→D→B (BC, CD, DB), **II** = A→B→D→E→A (AB, BD, DE, EA). The flow in the direction of the loop is $+$. The correction is

$$\Delta Q=-\frac{\sum rQ|Q|}{\sum2r|Q|}$$

applied to every pipe in the loop (the common pipe BD gets both corrections, with opposite sign conventions).

*Trial 1*

| Loop | Pipe | $Q$ | $rQ\lvert Q\rvert$ | $2r\lvert Q\rvert$ |
|---|---|---|---|---|
| I | BC | +60 | +3600.0 | 120.0 |
|  | CD | +10 | +50.0 | 10.0 |
|  | DB | −20 | −1831.0 | 183.1 |
|  | | | Σ = +1819.0 | Σ = 313.1 |
| II | AB | +60 | +3600.0 | 120.0 |
|  | BD | +20 | +1831.0 | 183.1 |
|  | DE | +10 | +50.0 | 10.0 |
|  | EA | −20 | −2441.4 | 244.1 |
|  | | | Σ = +3039.6 | Σ = 557.2 |

$\Delta Q_I=-\dfrac{1819.0}{313.1}=-5.81$, $\Delta Q_{II}=-\dfrac{3039.6}{557.2}=-5.45$. New flows: AB = 54.55, BC = 54.19, CD = 4.19, BD = $20+5.81-5.45=20.35$, DE = 4.55, AE = 25.45.

*Trial 2*

| Loop | Pipe | $Q$ | $rQ\lvert Q\rvert$ | $2r\lvert Q\rvert$ |
|---|---|---|---|---|
| I | BC | +54.19 | +2936.6 | 108.4 |
|  | CD | +4.19 | +8.8 | 4.2 |
|  | DB | −20.35 | −1896.6 | 186.4 |
|  | | | Σ = +1048.8 | Σ = 298.9 |
| II | AB | +54.55 | +2975.2 | 109.1 |
|  | BD | +20.35 | +1896.6 | 186.4 |
|  | DE | +4.55 | +10.3 | 4.6 |
|  | EA | −25.45 | −3954.7 | 310.7 |
|  | | | Σ = +927.4 | Σ = 610.7 |

$\Delta Q_I=-3.51$, $\Delta Q_{II}=-1.52$. Flows after two trials:

$$\boxed{AB=53.0,\ BC=50.7,\ CD=0.7\ (C\to D),\ BD=22.3,\ DE=3.0,\ AE=27.0}$$

The iteration is still converging (the corrections are 3.5 and 1.5, still large); continuing to full convergence gives AB = 51.4, BC = 48.6, CD = 1.4 (flowing D→C), BD = 22.7, DE = 1.4 and AE = 28.6, in the same units as the data (node checks: at C, $48.6+1.4=50$; at D, inflow $22.7$ equals the outflow $20+1.4+1.4$ to the demand, to C and to E).

@s 3
**(a) Alternate depths and critical depth.** The specific energy $E=y+\dfrac{V^2}{2g}=y+\dfrac{Q^2}{2gA^2}$ of a channel carrying a constant discharge is plotted against depth: the **specific energy curve** has two branches (asymptotic to $E=y$ and to $E=0$ axis). For a given $E>E_{min}$ there are two possible depths, called **alternate depths**: the *lower* $y_1$ (supercritical, $Fr>1$, small depth, high velocity) and the *upper* $y_2$ (subcritical, $Fr<1$). The two depths coincide at $E=E_{min}$, the **critical depth** $y_c$, where $dE/dy=0$:

$$\frac{dE}{dy}=1-\frac{Q^2T}{gA^3}=0\ \Rightarrow\ \frac{Q^2}{g}=\frac{A_c^3}{T_c}\quad(Fr=1)$$

```figure caption="Specific-energy diagram: alternate depths y1 (supercritical) and y2 (subcritical) for the same E, merging at the critical depth yc where E is minimum."
fig,ax=plt.subplots(figsize=(4.4,2.9))
y=np.linspace(0.25,3.2,300); q=2.0; E=y+q**2/(2*9.81*y**2)
ax.plot(E,y,color=ACCENT,lw=2); ax.plot([0,3.4],[0,3.4],color=MUTED,lw=0.9,ls="--"); ax.text(3.0,3.15,"E = y",fontsize=8,color=MUTED)
yc=(q**2/9.81)**(1/3); Emin=1.5*yc; ax.axhline(yc,color="#d9534f",lw=0.9,ls=":"); ax.text(0.1,yc+0.07,"y$_c$",fontsize=9,color="#d9534f")
E0=1.6
from scipy.optimize import brentq
y1=brentq(lambda v:v+q**2/(2*9.81*v*v)-E0,0.2,yc); y2=brentq(lambda v:v+q**2/(2*9.81*v*v)-E0,yc,3)
ax.plot([E0,E0],[0,y2],color=INK,lw=0.8,ls="--"); ax.plot([0,E0],[y1,y1],color=INK,lw=0.8,ls=":"); ax.plot([0,E0],[y2,y2],color=INK,lw=0.8,ls=":")
ax.text(0.05,y1+0.05,"y$_1$",fontsize=9); ax.text(0.05,y2+0.05,"y$_2$",fontsize=9); ax.text(Emin+0.05,yc-0.2,"E$_{min}$",fontsize=8)
ax.set_xlim(0,3.4); ax.set_ylim(0,3.4); ax.set_xlabel("specific energy E",fontsize=8.5); ax.set_ylabel("depth y",fontsize=8.5); ax.tick_params(labelsize=0)
```

*Critical depth in the triangular section of the figure.* The section is an equilateral triangle of side $a$ with the base at the bottom; the sloping sides are at $60^\circ$ to the horizontal, each giving a horizontal offset of $y/\tan60^\circ=y/\sqrt3$ over the depth $y$. For water depth $y$:

$$\begin{gathered}T=a-\frac{2y}{\sqrt3} \\ A=\frac{(a+T)}2\,y=y\left(a-\frac{y}{\sqrt3}\right)\end{gathered}$$

The critical-flow condition $\dfrac{Q^2}{g}=\dfrac{A^3}{T}$ gives the equation for $y_c$:

$$\boxed{\frac{Q^2}{g}=\frac{y_c^3\left(a-\dfrac{y_c}{\sqrt3}\right)^3}{a-\dfrac{2y_c}{\sqrt3}}}$$

In dimensionless form with $\eta=y_c/a$: $\dfrac{Q^2}{ga^5}=\dfrac{\eta^3(1-\eta/\sqrt3)^3}{1-2\eta/\sqrt3}$, with $0<\eta<\dfrac{\sqrt3}{2}=0.866$ (the apex). The equation is solved by trial or Newton's method; some values:

| $\eta=y_c/a$ | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 |
|---|---|---|---|---|---|---|---|---|
| $Q^2/(ga^5)$ | 0.00095 | 0.00720 | 0.02335 | 0.05410 | 0.10645 | 0.19633 | 0.37850 | 1.04647 |

*Example:* for $a=2$ m and $Q=5.78$ m³/s, $Q^2/(ga^5)=0.1064$, so $\eta=0.5$ and $y_c=1.00$ m. (Because the section closes at the top, the flow reaches critical conditions at a smaller discharge than for an open section; the critical depth increases rapidly as the water nears the apex, where $T\to0$.)

**(b) Trapezoidal canal, $m=2$, $Q=50$ m³/s, $S_0=0.005$, $n=0.018$.**

*(i) Width for $y=2$ m.* $A=(B+2y)y=2(B+4)$, $P=B+2y\sqrt{1+m^2}=B+4\sqrt5=B+8.944$. Manning:

$$Q=\frac1n\frac{A^{5/3}}{P^{2/3}}S_0^{1/2}\ \Rightarrow\ \frac{A^{5/3}}{P^{2/3}}=\frac{50(0.018)}{\sqrt{0.005}}=12.728$$

Trial: $B=1.5$: $A=11.0$, $P=10.44$, $A^{5/3}/P^{2/3}=54.5/4.78=11.40$; $B=2.0$: $A=12.0$, $P=10.94$, $A^{5/3}/P^{2/3}=62.9/4.93=12.75$ (close); $B=1.99$: $A=11.98$, $P=10.93$: 12.73. ✔

$$\boxed{B\approx1.99\approx2.0\ \text{m}}$$

(With $A=11.98$ m², $V=4.17$ m/s and $Fr=V/\sqrt{gA/T}=4.17/\sqrt{9.81(11.98/9.99)}=1.22$ for $T=B+4y=9.99$ m: the flow is supercritical in this steep channel.)

*(ii) Most economical (best hydraulic) section for $m=2$.* The condition is $R=y/2$ and $B=2y\left(\sqrt{1+m^2}-m\right)=2y(\sqrt5-2)=0.472\,y$:

$$\begin{gathered}A=(B+my)y=(0.472+2)y^2=2.472y^2 \\ P=0.472y+2y\sqrt5=4.944y \\ R=0.5y\end{gathered}$$

$$Q=\frac1nAR^{2/3}S_0^{1/2}=\frac1{0.018}(2.472y^2)(0.5y)^{2/3}(0.005)^{1/2}=50$$

$$y^{8/3}\left[\frac{2.472(0.63)(0.0707)}{0.018}\right]=50\ \Rightarrow\ y^{8/3}=\frac{50}{6.117}=8.17\ \Rightarrow\ y=2.20\ \text{m}$$

$$\boxed{y\approx2.20\ \text{m},\qquad B=0.472(2.20)\approx1.04\ \text{m}}$$

($A=11.95$ m², $R=1.10$ m, $V=4.18$ m/s.)

@s 4
**(a) Momentum equation and sequent depth ratio.** Consider a hydraulic jump in a horizontal rectangular channel of unit width. Section 1 (before the jump): depth $y_1$, velocity $V_1$. Section 2 (after the jump): $y_2$, $V_2$, with $q=V_1y_1=V_2y_2$. The friction on the short length is neglected, so the net force equals the rate of change of momentum:

$$\frac12\gamma y_1^2-\frac12\gamma y_2^2=\rho q\,(V_2-V_1)\quad\Rightarrow\quad\frac12\gamma y_1^2+\rho qV_1=\frac12\gamma y_2^2+\rho qV_2$$

$$\begin{gathered}\boxed{\frac{y_1^2}{2}+\frac{q^2}{gy_1}=\frac{y_2^2}{2}+\frac{q^2}{gy_2}} \\ (\text{equality of specific force})\end{gathered}$$

*Sequent depth ratio.* Substituting $q^2=V_1^2y_1^2$ and writing $\dfrac{q^2}{g}=Fr_1^2\,y_1^3$:

$$\frac{y_2^2-y_1^2}{2}=Fr_1^2y_1^3\left(\frac1{y_1}-\frac1{y_2}\right)=Fr_1^2y_1^3\,\frac{y_2-y_1}{y_1y_2}\ \Rightarrow\ \frac{y_2+y_1}{2}=\frac{Fr_1^2y_1^2}{y_2}$$

With $r=y_2/y_1$: $r^2+r-2Fr_1^2=0$, so

$$\boxed{\frac{y_2}{y_1}=\frac12\left(\sqrt{1+8Fr_1^2}-1\right)}$$

The energy loss in the jump is $h_L=\dfrac{(y_2-y_1)^3}{4y_1y_2}$.

**(b) Sluice, jump and broad-crested weir (per metre width).**

*Discharge from the weir.* The flow is critical on the weir with $y_c=1$ m:

$$q=\sqrt{gy_c^3}=\sqrt{9.81}=3.132\ \text{m}^2/\text{s}$$

*Depth after the jump.* The specific energy over the crest is $E_c=\tfrac32y_c=1.5$ m and the crest is $\Delta z=0.10$ m above the bed, so (no loss between the jump and the weir) the energy after the jump relative to the bed is $E_2=1.5+0.10=1.60$ m. The subcritical depth $y_2$ is given by

$$y_2+\frac{q^2}{2gy_2^2}=1.60\ \Rightarrow\ y_2+\frac{0.5}{y_2^2}=1.60\ \Rightarrow\ y_2=1.308\ \text{m},\quad V_2=\frac{3.132}{1.308}=2.395\ \text{m/s}$$

*Flow at the gate:* $y_1=0.3$ m, $V_1=\dfrac{3.132}{0.3}=10.44$ m/s, $Fr_1=\dfrac{10.44}{\sqrt{9.81(0.3)}}=6.09$. The free (natural) sequent depth of 0.3 m would be $y_2=\tfrac12(0.3)(\sqrt{1+8(6.09)^2}-1)=2.44$ m, which is greater than 1.308 m. The jump is therefore pushed downstream unless it is held by the baffle blocks.

*Force of the blocks* (momentum equation, $F$ acting upstream on the flow, per metre width):

$$\frac12\gamma y_1^2-\frac12\gamma y_2^2-F=\rho q(V_2-V_1)$$

$$\frac12(9.81)(0.09)-\frac12(9.81)(1.7106)-F=3.132(2.395-10.44)$$

$$0.441-8.390-F=-25.20\ \Rightarrow\ \boxed{F\approx17.3\ \text{kN per metre width}}$$

(The water pushes the blocks downstream with this force; for a width $b$ multiply by $b$.)

*Depth upstream of the sluice gate.* Energy is conserved through the gate:

$$y_0+\frac{q^2}{2gy_0^2}=y_1+\frac{V_1^2}{2g}=0.3+\frac{10.44^2}{2(9.81)}=5.856\ \text{m}$$

$$y_0+\frac{0.5}{y_0^2}=5.856\ \Rightarrow\ \boxed{y_0\approx5.84\ \text{m}}$$

(the velocity head upstream is only 0.015 m).

@s 5
**(a) Dynamic equation of gradually varied flow.** Assumptions: steady flow, hydrostatic pressure distribution, small bed slope, prismatic channel, energy coefficient $\alpha=1$, and friction slope given by Manning's/Chezy's equation for the local depth. The total head is $H=z+y+\dfrac{V^2}{2g}$. Differentiating along the channel, with $\dfrac{dH}{dx}=-S_f$ and $\dfrac{dz}{dx}=-S_0$:

$$-S_f=-S_0+\frac{dy}{dx}+\frac{d}{dy}\left(\frac{Q^2}{2gA^2}\right)\frac{dy}{dx},\quad \frac{d}{dy}\left(\frac{Q^2}{2gA^2}\right)=-\frac{Q^2T}{gA^3}=-Fr^2$$

$$\boxed{\frac{dy}{dx}=\frac{S_0-S_f}{1-Fr^2}}$$

Using the section factors, $S_f/S_0=(K_n/K)^2$ and $Fr^2=(Z_c/Z)^2$: $\dfrac{dy}{dx}=S_0\dfrac{1-(K_n/K)^2}{1-(Z_c/Z)^2}$, which becomes $S_0\dfrac{1-(y_n/y)^{10/3}}{1-(y_c/y)^3}$ for a wide rectangular channel.

*Water-surface profiles.* Rule: the numerator is positive when $y>y_n$ and the denominator is positive when $y>y_c$. The profile families are: 

| Slope | Condition | Zone 1 ($y>$ both) | Zone 2 (between $y_n$ and $y_c$) | Zone 3 ($y<$ both) |
|---|---|---|---|---|
| Mild (M) | $y_n>y_c$ | **M1** – backwater, depth increases downstream (e.g. upstream of a sluice gate or weir) | **M2** – drawdown, depth falls towards $y_c$ (e.g. before a drop or free overfall) | **M3** – rises to a jump (e.g. downstream of the sluice gate) |
| Critical (C) | $y_n=y_c$ | **C1** – rises downstream (backwater) | – | **C3** – rises towards $y_c$ |
| Steep (S) | $y_n<y_c$ | **S1** – backwater after a jump (rising, becoming horizontal) | **S2** – falls from $y_c$ to $y_n$ (at a change from mild slope to steep slope) | **S3** – rises from the gate to $y_n$ (downstream of a sluice gate) |

For the combination shown in the figure: upstream of the sluice gate on the *mild* slope the depth is above normal, an **M1** curve; downstream of the gate the stream is below the critical depth, an **M3** curve, ending in a hydraulic jump to the normal depth. On the transition from the *mild to critical slope* the flow tends to $y_c=y_n$ with a **C1 / C2-type** (almost uniform) surface; on the *critical to steep* change the depth passes through $y_c$ and then follows an **S2** curve to the normal depth on the steep slope (an **S3** curve below the next gate).

```figure caption="Gradually varied flow profile families: M1, M2, M3 on a mild slope (yn above yc) and S1, S2, S3 on a steep slope (yc above yn). Flow is from left to right; the dashed line is the normal depth line (NDL) and the dotted line the critical depth line (CDL)."
fig,axs=plt.subplots(2,3,figsize=(5.9,3.7))
x=np.linspace(0,1,100)
def panel(ax,ndl,cdl,y,name,col):
    ax.plot([0,1],[0,0],color=INK,lw=2); ax.axhline(ndl,color=MUTED,lw=0.8,ls="--"); ax.axhline(cdl,color=MUTED,lw=0.8,ls=":")
    ax.plot(x,y,color=col,lw=2); ax.set_title(name,fontsize=8.5); ax.set_xlim(0,1); ax.set_ylim(-0.1,2.0); ax.axis("off"); ax.set_title(name,fontsize=9)
panel(axs[0,0],1.0,0.6,1.0+0.8*x**3,"M1",ACCENT); panel(axs[0,1],1.0,0.6,0.6+0.4*(1-x)**1.6,"M2",ACCENT); panel(axs[0,2],1.0,0.6,0.15+0.45*x**0.7,"M3",ACCENT)
panel(axs[1,0],0.6,1.0,1.0+0.8*x**1.8,"S1","#d9534f"); panel(axs[1,1],0.6,1.0,0.6+0.4*np.exp(-3.5*x),"S2","#d9534f"); panel(axs[1,2],0.6,1.0,0.6-0.45*np.exp(-3*x),"S3","#d9534f")
axs[0,0].text(0.0,-0.1,"mild: NDL above CDL",fontsize=6.5); axs[1,0].text(0.0,-0.1,"steep: CDL above NDL",fontsize=6.5)
fig.tight_layout()
```

**(b) Location of the hydraulic jump below the sluice gate.** Wide horizontal channel ($R\approx y$), $q=2$ m²/s, $n=0.015$, $S_0=0$, $y_1=0.15$ m at the vena contracta, tail-water depth $y_t=1.80$ m.

*Sequent depth of the gate stream:* $V_1=\dfrac{2}{0.15}=13.33$ m/s, $Fr_1=\dfrac{13.33}{\sqrt{9.81(0.15)}}=10.99$:

$$y_2=\frac{0.15}{2}\left(\sqrt{1+8(10.99)^2}-1\right)=2.26\ \text{m}>y_t=1.80\ \text{m}$$

The tail water (1.80 m) is *less* than the sequent depth (2.26 m), so the jump cannot form at the gate: the supercritical stream continues downstream with its depth increasing slowly because of friction (an **H3-type**, i.e. horizontal-bed supercritical profile) until it reaches the depth $y_1'$ whose sequent depth equals the tail water depth 1.80 m:

$$\begin{gathered}Fr_2=\frac{2/1.8}{\sqrt{9.81(1.8)}}=0.2644 \\ y_1'=\frac{1.80}{2}\left(\sqrt{1+8(0.2644)^2}-1\right)=0.224\ \text{m}\end{gathered}$$

*Direct step method* for the profile from $y=0.15$ m to $y=0.224$ m, in three equal steps ($\Delta y=0.0246$ m). For the wide channel $E=y+\dfrac{q^2}{2gy^2}$, $S_f=\dfrac{n^2q^2}{y^{10/3}}$ and, since $S_0=0$, $\Delta x=\dfrac{E_2-E_1}{-\bar S_f}$:

| Step | $y_1\to y_2$ (m) | $E_1$ (m) | $E_2$ (m) | $S_{f1}$ | $S_{f2}$ | $\bar S_f$ | $\Delta x$ (m) |
|---|---|---|---|---|---|---|---|
| 1 | 0.1500 → 0.1746 | 9.211 | 6.861 | 0.5019 | 0.3024 | 0.4022 | 5.84 |
| 2 | 0.1746 → 0.1992 | 6.861 | 5.335 | 0.3024 | 0.1948 | 0.2486 | 6.14 |
| 3 | 0.1992 → 0.2239 | 5.335 | 4.292 | 0.1948 | 0.1321 | 0.1635 | 6.38 |

$$\boxed{L=5.84+6.14+6.38\approx18.4\ \text{m downstream of the gate}}$$

The hydraulic jump forms about **18.4 m from the vena contracta**, where the depth is 0.224 m and it jumps to the 1.80 m tail-water depth.

**OR.** *Rectangular channel, $b=10$ m, $q=12.5$ m²/s per metre (so $Q=125$ m³/s), $n=0.015$, slope break from $S_{01}=0.01$ to $S_{02}=0.0064$.*

*Critical depth:* $y_c=\left(\dfrac{q^2}{g}\right)^{1/3}=\left(\dfrac{156.25}{9.81}\right)^{1/3}=2.516$ m.

*Normal depths* from Manning with $A=10y$, $P=10+2y$:

$$\begin{gathered}S_{01}=0.01:\ y_{n1}=1.633\ \text{m} \\ S_{02}=0.0064:\ y_{n2}=1.896\ \text{m}\end{gathered}$$

Both normal depths are *smaller* than $y_c=2.516$ m, so both reaches are **steep**. The slope becomes flatter at the break, so the normal depth increases from 1.633 m to 1.896 m. The flow arrives at the break at the depth $y_{n1}$ (supercritical, uniform), but the new reach requires $y_{n2}$ (greater), so the depth must rise: $y$ is below both $y_{n2}$ and $y_c$, which is Zone 3 of a steep slope. The surface profile is therefore an **S3 curve**, rising gradually from $y_{n1}=1.633$ m towards $y_{n2}$ asymptotically (no jump, since the flow stays supercritical).

*Length by the direct step method* (three steps from $y_{n1}=1.633$ m to $0.99\,y_{n2}=1.877$ m, because the profile only approaches $y_{n2}$ asymptotically; $\Delta y=0.0814$ m). $A=10y$, $R=\dfrac{10y}{10+2y}$, $E=y+\dfrac{Q^2}{2gA^2}$, $S_f=\dfrac{n^2V^2}{R^{4/3}}$, $\Delta x=\dfrac{E_2-E_1}{S_0-\bar S_f}$ with $S_0=0.0064$:

| Step | $y_1\to y_2$ (m) | $E_1$ (m) | $E_2$ (m) | $S_{f1}$ | $S_{f2}$ | $S_0-\bar S_f$ | $\Delta x$ (m) |
|---|---|---|---|---|---|---|---|
| 1 | 1.6326 → 1.7140 | 4.620 | 4.425 | 0.01000 | 0.00864 | −0.00292 | 67.0 |
| 2 | 1.7140 → 1.7954 | 4.425 | 4.266 | 0.00864 | 0.00752 | −0.00168 | 94.4 |
| 3 | 1.7954 → 1.8768 | 4.266 | 4.138 | 0.00752 | 0.00659 | −0.00066 | 194.7 |

$$\boxed{L=67.0+94.4+194.7\approx356\ \text{m}}$$

The S3 curve extends roughly 360 m in the second reach before the depth reaches 99 % of the new normal depth 1.896 m.
