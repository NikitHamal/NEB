---
file: NEBians-IOE-Past-Paper-Design-of-Steel-Structures-ENCE303-2082-Chaitra.pdf
subject: Design of Steel Structures
level: BE · Year III / Part I
code: ENCE 303
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular examination (new course), BE Civil (BCE), Year III / Part I. Full marks 60, pass marks 24. IS 800:2007, IS 883:2016, IS 875 (Part 3) and IS 808 are allowed.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · IS 800:2007, IS 883:2016, IS 875 (Part 3) and IS 808 are allowed · Assume suitable data if necessary</small>

@q 1
(a) Explain the different failure mechanisms of bolted connections in steel structures. [[3]]

(b) Calculate the tensile force developed in each bolt of the given bracket connection subjected to an eccentric load. The connection consists of M20 grade 4.6 bolts arranged as shown with an edge distance of 30 mm and a pitch of 50 mm. The connection carries a load of 300 kN acting at an eccentricity of 250 mm, as shown in the figure. (Bolt layout read from the scan: 8 rows at 50 mm pitch with 30 mm end distances, 4 bolts per row, two on each side of the bracket web.) [[9]]

@q 2
(a) Design a lap connection to join two plates of 200 mm $\times$ 10 mm of grade E250 to mobilize full plate tensile strength using shop fillet welds. [[4]]

(b) A diagonal member of a roof truss carries a maximum pull of 300 kN. Design the section and its connection with a 16 mm thick gusset plate. The length of the connection is limited to 340 mm. Design the lug angles also if required. The steel of grade Fe 410 and bolts of grade 4.6 are to be used. [[8]]

@q 3
A built-up steel column is subjected to the design axial load of 1500 kN. If the unsupported length of the column is 8 m, the ends of the column are fixed, design the column, when the column is made up of two channel sections placed toe-to-toe with a single lacing system. [[12]]

@q 4
(a) Design a simple beam having clear span 3.2 m, supported over wall having thickness 150 mm, beam has to carry imposed load of 20 kN/m (excluding self-weight) and point load from secondary beam 10 kN at mid-span. Consider laterally unrestrained beam. Check for lateral stability of web. [[9]]

(b) Discuss procedure to estimate size of web and flange plates of a welded plate girder. [[3]]

@q 5
(a) Determine wind pressure on roof of a building having height 15 m, length 40 m and width 25 m. Building is located in dense forest of a hill having average slope 1:1.5, height of hill is 800 m and building is located at mid height of hill. Consider normal opening of building. [[6]]

(b) Design a slab base for column SC 150, subjected to axial compressive load of 300 kN. Slab base is supported over concrete footing of grade M15. [[6]]

<!-- SOLUTIONS -->

**Common data (IS 800:2007).** E250 (Fe 410): $f_y=250$ N/mm$^2$, $f_u=410$ N/mm$^2$, $E=2\times10^5$ N/mm$^2$. Partial safety factors: $\gamma_{m0}=1.10$ (yield), $\gamma_{m1}=1.25$ (rupture), $\gamma_{mb}=1.25$ (bolts), $\gamma_{mw}=1.25$ (shop welds). Bolts grade 4.6: $f_{ub}=400$, $f_{yb}=240$ N/mm$^2$. All loads below are taken as factored (design) loads unless stated.

@s 1
**(a) Failure mechanisms of bolted connections.**

1. **Shear failure of the bolt:** the shank is sheared on one (single shear) or two planes (double shear); with threads in the shear plane the area is the net tensile area.
2. **Bearing failure of the plate (or bolt):** the plate material in front of the bolt crushes and the hole elongates, when the end or pitch distance is small, or the plate is thin.
3. **Tension (net section) failure of the plate:** rupture of the plate through the line of bolt holes where the area is reduced by holes; also yielding of the gross section.
4. **Block shear failure:** a block of plate tears out along a path of shear on one face and tension on the other (common in gusset plates and angles).
5. **Tearing (end) failure:** the plate shears out between the bolt and the free end, when the end distance is smaller than $1.5d_0$.
6. **Tension failure of the bolt:** the bolt breaks at the threaded section under a direct pull (for example the bracket here), often with **prying action** from the flexible connection plate, which increases the bolt tension.
7. **Combined shear and tension** in the bolt (interaction check).
8. **Slip** in friction-grip (HSFG) connections: the friction between the plates is overcome, so the bolts then act in bearing.
9. Bending of the bolt (a long grip, or thick packing) and buckling of the plate in compression between the bolts (pitch limits).

**(b) Eccentric bracket (bolts in tension and shear).**

*Loads.* Direct shear $V=300$ kN, moment

$$M=300\times0.25=75$$

kN m. The moment produces tension in the bolts above the neutral axis and compression on the bearing zone below. The bolts: 8 rows $\times$ 4 bolts $=32$ bolts of M20 4.6 ($A_{sb}=314$ mm$^2$, $A_{nb}=245$ mm$^2$).

*Neutral axis.* Take the neutral axis at the bottom bolt row (a conservative assumption; the compression is taken by the bracket bearing at the bottom). Let $y$ be the distance of a bolt row above this axis: $y=0,50,100,\ldots,350$ mm. The tension in a bolt is proportional to $y$: $T_i=ky_i$. With 4 bolts in each row,

$$\sum y^2=50^2(0^2+1^2+\cdots+7^2)=50^2\times140=350\,000\ \text{mm}^2$$

$$M=4\sum T_iy_i=4k\sum y_i^2\ \Rightarrow\ k=\frac{M}{4\sum y^2}=\frac{75\times10^6}{4\times350\,000}=53.57\ \text{N/mm}$$

| Row (from the bottom) | $y$ (mm) | Tension per bolt $T=53.57y$ (kN) |
|---|---|---|
| 8 (top) | 350 | **18.75** |
| 7 | 300 | 16.07 |
| 6 | 250 | 13.39 |
| 5 | 200 | 10.71 |
| 4 | 150 | 8.04 |
| 3 | 100 | 5.36 |
| 2 | 50 | 2.68 |
| 1 (bottom) | 0 | 0 |

$$\boxed{T_{b,max}=\frac{My_{max}}{4\sum y^2}=\frac{75\times10^6\times350}{4\times350\,000}=18.75\ \text{kN (top row bolts)}}$$

*Shear per bolt* (equal sharing):

$$V_{sb}=\dfrac{300}{32}=9.375\ \text{kN.}$$

*Capacities (IS 800 cl. 10.3):*

$$\begin{gathered}V_{dsb}=\frac{f_{ub}}{\sqrt3}\frac{n_nA_{nb}}{\gamma_{mb}}=\frac{400}{\sqrt3}\times\frac{245}{1.25}=45.3\ \text{kN} \\ T_{db}=\frac{0.9f_{ub}A_{nb}}{\gamma_{mb}}=\frac{0.9\times400\times245}{1.25}=70.6\ \text{kN}\end{gathered}$$

(the upper limit

$$f_{yb}A_{sb}\gamma_{mb}/\gamma_{m0}=240\times314\times1.25/1.1=85.6$$

kN is larger, so $70.6$ kN governs.)

*Interaction (cl. 10.3.6):*

$$\left(\frac{V_{sb}}{V_{db}}\right)^2+\left(\frac{T_b}{T_{db}}\right)^2=\left(\frac{9.375}{45.3}\right)^2+\left(\frac{18.75}{70.6}\right)^2=0.043+0.071=0.11\le1.0\ \checkmark$$

The bolts are safe; the maximum tensile force is 18.75 kN per bolt. (The plate bending and prying action must be checked separately, with a bracket plate thick enough that the prying force $Q$ is small.)

```figure caption="Question 1(b): bracket with 8 rows of bolts at 50 mm pitch; 300 kN at 250 mm gives M = 75 kN m. Bolt tension varies linearly from zero at the bottom row (neutral axis) to 18.75 kN at the top row."
fig,(a,b)=plt.subplots(1,2,figsize=(6.2,3.1),gridspec_kw={"width_ratios":[1.1,1]})
a.set_xlim(0,12); a.set_ylim(0,10); a.axis("off")
a.add_patch(plt.Rectangle((0.5,0.5),0.8,8.5,fc="#c9ccd1",ec=INK)); a.text(0.9,9.3,"column",ha="center",fontsize=7)
a.add_patch(plt.Polygon([[1.3,8.5],[9.5,8.5],[9.5,5.5],[1.3,1.5]],fc="#dfe6f0",ec=INK))
for i in range(8): a.add_patch(plt.Rectangle((1.0,1.8+i*0.9),0.6,0.35,fc=INK))
a.annotate("",xy=(9.5,8.5),xytext=(9.5,10.0),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=2)); a.text(9.0,9.7,"300 kN",fontsize=8,color="#d9534f")
a.annotate("",xy=(1.3,9.0),xytext=(9.5,9.0),arrowprops=dict(arrowstyle="<->",color=INK)); a.text(5,9.3,"e = 250 mm",ha="center",fontsize=8)
b.set_xlim(-1,10); b.set_ylim(0,10); b.axis("off"); b.set_title("bolt tension (kN)",fontsize=8.5)
ys=np.arange(8)*50; T=53.57*ys/1000
for i,(y,t) in enumerate(zip(ys,T)):
    b.plot([1,1+t*0.35],[1.2+i*1.0]*2,color=ACCENT,lw=5,solid_capstyle="butt"); b.text(1+t*0.35+0.15,1.2+i*1.0,f"{t:.2f}",va="center",fontsize=7)
b.plot([1,1],[0.8,8.6],color=INK,lw=1.2); b.text(1,0.2,"N.A. at bottom row",fontsize=7,color=MUTED)
fig.tight_layout()
```

@s 2
**(a) Lap joint, full plate strength, shop fillet welds.**

*Plate strength (IS 800 cl. 6).*

$$A_g=200\times10=2000$$

mm$^2$ (no holes, so $A_n=A_g$).

$$\begin{gathered}T_{dg}=\frac{f_yA_g}{\gamma_{m0}}=\frac{250\times2000}{1.1}=454.5\ \text{kN} \\ T_{dn}=\frac{0.9f_uA_n}{\gamma_{m1}}=\frac{0.9\times410\times2000}{1.25}=590.4\ \text{kN}\end{gathered}$$

The design tensile strength of the plate is $T_d=454.5$ kN (yielding governs). The weld is to develop this full force.

*Weld size* (IS 800 cl. 10.5.2): the minimum size for the thicker part 10 mm is 3 mm (5 mm for parts above 10 mm); the maximum size for a plate edge $=t-1.5=8.5$ mm. Adopt **$s=8$ mm** (throat

$$t_t=0.7\times8=5.6\ \text{mm).}$$

*Strength of the weld per mm length* (shop weld, $\gamma_{mw}=1.25$):

$$\begin{gathered}f_{wd}=\frac{f_u}{\sqrt3\,\gamma_{mw}}=\frac{410}{\sqrt3\times1.25}=189.4\ \text{N/mm}^2 \\ P_w=f_{wd}t_t=189.4\times5.6=1060\ \text{N/mm}=1.06\ \text{kN/mm}\end{gathered}$$

*Length required:*

$$L_w=\dfrac{454.5}{1.06}=428.6$$

mm in total. Provide **two longitudinal (side) fillet welds**, each $214.3$ mm, so use **2 × 220 mm** (total 440 mm $\ge428.6$ mm). Check of the arrangement:

- Each longitudinal weld $\ge$ the distance between the welds: $220\ge b=200$ mm ✓ (limits shear lag).
- Overlap $\ge5t=50$ mm and $\ge$ 25 mm: provided overlap $=220+$ end return, so about 230 mm ✓. Weld ends are returned round the corner for $2s=16$ mm.
- Minimum length of a weld $\ge4s=32$ mm ✓, maximum effective length $70s=560$ mm ✓.

$$\boxed{\text{Lap joint: overlap }\approx230\text{ mm; 8 mm fillet weld; 2 side welds each 220 mm (total 440 mm}\ge428.6\text{ mm)}}$$

*Alternative with a transverse weld:* a weld across the 200 mm width carries $1.06\times200=212$ kN; the remaining $242.5$ kN need $2\times114.4$ mm, so 2 × 120 mm side welds + 200 mm end weld also works (overlap about 130 mm).

```figure caption="Question 2(a): lap joint of two 200 x 10 plates with 8 mm shop fillet welds: two longitudinal welds of 220 mm and returns at the ends."
fig,a=plt.subplots(figsize=(5.4,2.0))
a.set_xlim(0,14); a.set_ylim(0,5); a.axis("off")
a.add_patch(plt.Rectangle((0.3,1.2),8.0,2.4,fc="#dfe6f0",ec=INK)); a.add_patch(plt.Rectangle((5.0,1.2),8.7,2.4,fc="#c9d6e8",ec=INK,alpha=0.85))
a.plot([5.0,8.3],[1.2,1.2],color="#d9534f",lw=3); a.plot([5.0,8.3],[3.6,3.6],color="#d9534f",lw=3)
a.annotate("",xy=(0.3,2.4),xytext=(-0.2,2.4),arrowprops=dict(arrowstyle="-|>",color=INK,lw=2)); a.annotate("",xy=(14.3,2.4),xytext=(13.7,2.4),arrowprops=dict(arrowstyle="-|>",color=INK,lw=2))
a.text(6.6,4.1,"2 x 220 mm, 8 mm fillet",ha="center",fontsize=7.5,color="#d9534f"); a.text(6.6,0.5,"overlap about 230 mm",ha="center",fontsize=7.5)
a.text(2.5,2.4,"PL 200x10",ha="center",fontsize=8); a.text(11,2.4,"PL 200x10",ha="center",fontsize=8)
```

**(b) Roof-truss diagonal, 300 kN pull, gusset 16 mm, bolted (M20, 4.6).**

*Gross area required for yielding:*

$$A_g\ge\dfrac{T\gamma_{m0}}{f_y}=\dfrac{300\times10^3\times1.1}{250}=1320$$

mm$^2$ (and more, to allow for the holes and shear lag). Adopt **two equal angles 2 ISA 75×75×8** (area $2\times1138=2276$ mm$^2$), placed on both sides of the 16 mm gusset and connected through one leg each.

*Bolts.* M20, 4.6, hole $d_0=22$ mm. The bolts are in double shear (each bolt joins the two angles to the gusset), threads in the shear plane:

$$V_{dsb}=2\times\frac{400}{\sqrt3}\times\frac{245}{1.25}=90.5\ \text{kN}$$

Bearing (pitch $p=50$ mm, end distance $e=40$ mm, thickness 16 mm of the gusset, equal to $2\times8$ of the angles):

$$k_b=\min\left(\dfrac{e}{3d_0},\dfrac{p}{3d_0}-0.25,\dfrac{f_{ub}}{f_u},1\right)=\min(0.606,0.508,0.976,1)=0.508\ \text{,}$$

$$V_{dpb}=\frac{2.5k_bdtf_u}{\gamma_{mb}}=\frac{2.5\times0.508\times20\times16\times410}{1.25}=133.2\ \text{kN}$$

Bolt value $=\min(90.5,133.2)=90.5$ kN. Number of bolts $=\dfrac{300}{90.5}=3.3$; **provide 4 bolts in one line**: $4\times90.5=362\ge300$ ✓.

*Length of the connection.* $e=40$, three pitches of 50, $e=40$: total $=40+150+40=230$ mm $\le340$ mm ✓. The joint length between the end bolts $=150$ mm $<15d=300$ mm, so there is no long-joint reduction. The bolt line is at 40 mm from the heel (the standard gauge of ISA 75 is 40 mm), so the other edge distance is 35 mm $\ge1.5d_0=33$ mm ✓.

*Tension capacity of the angles (per angle).*

(i) Gross-section yielding:

$$T_{dg}=\dfrac{A_gf_y}{\gamma_{m0}}=\dfrac{2276\times250}{1.1}=517$$

kN (for the pair).

(ii) Net-section rupture with shear lag (cl. 6.3.3): $T_{dn}=\dfrac{0.9A_{nc}f_u}{\gamma_{m1}}+\dfrac{\beta A_{go}f_y}{\gamma_{m0}}$.

$$A_{nc}=\left(75-\dfrac82-22\right)\times8=392$$

mm$^2$ (connected leg net area),

$$A_{go}=\left(75-\dfrac82\right)\times8=568$$

mm$^2$ (outstanding leg). $\beta=1.4-0.076\dfrac{w}{t}\dfrac{f_y}{f_u}\dfrac{b_s}{L_c}$ with $w=75$,

$$b_s=75+75-8=142$$

mm, $L_c=150$ mm:

$$\beta=1.4-0.076\times\frac{75}{8}\times\frac{250}{410}\times\frac{142}{150}=0.989\quad(0.7\le\beta\le1.44\ \checkmark)$$

$$T_{dn}=\frac{0.9\times392\times410}{1.25}+\frac{0.989\times568\times250}{1.1}=115.7+127.7=243.4\ \text{kN per angle}\ \Rightarrow\ 486.7\ \text{kN for two}$$

(iii) Block shear (cl. 6.4), per angle:

$$A_{vg}=(40+150)\times8=1520$$

$$A_{vn}=(190-3.5\times22)\times8=904$$

$$A_{tg}=35\times8=280$$

$$A_{tn}=(35-11)\times8=192$$

mm$^2$:

$$T_{db1}=\frac{A_{vg}f_y}{\sqrt3\gamma_{m0}}+\frac{0.9A_{tn}f_u}{\gamma_{m1}}=199.5+56.7=256.1\ \text{kN}$$

$$T_{db2}=\frac{0.9A_{vn}f_u}{\sqrt3\gamma_{m1}}+\frac{A_{tg}f_y}{\gamma_{m0}}=154.1+63.6=217.7\ \text{kN}\ \Rightarrow\ T_{db}=217.7\ \text{kN per angle}=435\ \text{kN for two}$$

*Design tensile strength* $=\min(517,\ 486.7,\ 435)=435\text{ kN}>300\text{ kN}$ ✓.

*Slenderness:* ISA 75×75×8 has

$$r_{min}=r_{vv}=14.7$$

mm, so a member length up to $350\times14.7=5.1$ m is permitted for a tension member subject to possible reversal (IS 800 Table 3). Tack bolts or battens may be used between the two angles at about 1 m.

*Lug angles.* A lug angle is provided when the outstanding leg is to be connected (to reduce shear lag and the length of connection). Here the single-leg connection with the $\beta$ reduction already carries the load with a connection of only 230 mm ($\le340$ mm), and the design strength exceeds the pull by 45 %. **Lug angles are therefore not required.** (If the 340 mm limit were exceeded, a lug angle ISA 50×50×6 with 2 bolts, designed for 20 % of the force, would be added.)

$$\boxed{\text{2 ISA 75}\times75\times8\text{ with 4 M20 (4.6) bolts at 50 mm pitch, 40 mm end distance, in double shear on a 16 mm gusset (connection length 230 mm)}}$$

```figure caption="Question 2(b): two angles ISA 75x75x8 connected to the 16 mm gusset plate with four M20 bolts (pitch 50 mm, edge distance 40 mm, connection length 230 mm)."
fig,a=plt.subplots(figsize=(5.6,2.4))
a.set_xlim(0,16); a.set_ylim(0,6); a.axis("off")
a.add_patch(plt.Polygon([[3,0.5],[15,0.5],[15,5.5],[3,5.5]],fc="#dfe6f0",ec=INK)); a.text(13.5,4.9,"gusset 16 mm",ha="right",fontsize=7)
a.add_patch(plt.Rectangle((0.5,2.4),11.5,1.2,fc="#c9d6e8",ec=INK)); a.text(1.6,3.0,"2 ISA 75x75x8",fontsize=7.5)
for i in range(4): a.add_patch(plt.Circle((4.0+i*1.25,3.0),0.28,fc="white",ec=INK)); 
a.annotate("",xy=(4.0,2.0),xytext=(9.75,2.0),arrowprops=dict(arrowstyle="<->",color=INK)); a.text(6.9,1.5,"3 x 50 = 150",ha="center",fontsize=7)
a.annotate("",xy=(3.2,4.1),xytext=(10.4,4.1),arrowprops=dict(arrowstyle="<->",color=INK)); a.text(6.8,4.4,"connection length 230 mm",ha="center",fontsize=7)
a.annotate("",xy=(0.0,3.0),xytext=(0.5,3.0),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=2)); a.text(0.2,3.8,"T = 300 kN",fontsize=7.5,color="#d9534f")
```

@s 3
**Laced column of two channels toe-to-toe.** Design load $P=1500$ kN, $L=8$ m, both ends fixed: effective length

$$L_e=0.65L=5.2$$

m (IS 800 Table 11, for both ends fixed, the recommended value $0.65L$). E250. Buckling class **c** about both axes for built-up sections (Table 10).

**Trial section.** Try **2 ISMC 300** ($A=4564$ mm$^2$ each, $I_{xx}=6362.6$ cm$^4$, $I_{yy}=310.8$ cm$^4$, $C_{yy}=23.6$ mm, $b_f=90$ mm, $r_{yy}=26$ mm). For the pair: $A=9128$ mm$^2$,

$$I_{xx}=2\times6362.6=12\,725$$

cm$^4$,

$$r_{xx}=\sqrt{I_{xx}/A}=118.1\ \text{mm.}$$

*Spacing.* Choose the gap so that $I_{yy}\ge I_{xx}$ (equal strength in both directions). With the toes facing each other and a clear gap $S$ between the toes, the centroid of each channel is $S/2+b_f-C_{yy}$ from the y–y axis:

$$\begin{gathered}S=100\ \text{mm}:\ d=50+90-23.6=116.4\ \text{mm} \\ I_{yy}=2\left[310.8\times10^4+4564\times116.4^2\right]=1.299\times10^8\ \text{mm}^4\ (12\,990\text{ cm}^4)\ge12\,725\text{ cm}^4\ \checkmark\end{gathered}$$

$$r_{yy}=\sqrt{1.299\times10^8/9128}=119.3\ \text{mm.}$$

*Slenderness.*

$$\begin{gathered}\lambda_{xx}=\frac{5200}{118.1}=44.0 \\ \lambda_{yy}=\frac{5200}{119.3}=43.6\end{gathered}$$

For a laced column the effective slenderness about the axis perpendicular to the lacing plane is taken 5 % larger (IS 800 cl. 10.7.5.1):

$$\lambda_e=1.05\times43.6=45.8$$

Governing $\lambda=45.8$ (about y–y, within the limit of 180 for the main members of the column).

*Compressive strength.* Non-dimensional slenderness

$$\lambda_n=\dfrac{\lambda}{\pi\sqrt{E/f_y}}=\dfrac{45.8}{88.9}=0.515$$

For class c, $\alpha=0.49$:

$$\phi=0.5\left[1+0.49(0.515-0.2)+0.515^2\right]=0.710$$

$$\chi=\dfrac{1}{\phi+\sqrt{\phi^2-\lambda_n^2}}=\dfrac{1}{0.710+0.488}=0.835$$

so

$$f_{cd}=\dfrac{\chi f_y}{\gamma_{m0}}=189.7$$

N/mm$^2$.

$$P_d=f_{cd}A=189.7\times9128=1731\ \text{kN}>1500\ \text{kN}\ \checkmark\ (\text{utilisation }87\%)$$

(2 ISMC 250 gives only about 1390 kN, which is not enough.)

**Design of the single lacing (cl. 10.7.3 to 10.7.5).**

*Transverse shear:* $V=2.5\%$ of the axial load $=0.025\times1500=37.5$ kN. Two lacing planes (one on each open face):

$$V_1=37.5/2=18.75\ \text{kN per plane.}$$

*Layout.* Take the bolt line $e=30$ mm from the toe of each flange, so the distance between the connecting bolt lines is

$$a=S+2e=100+60=160$$

mm. Lacing at **$\theta=45^\circ$** to the column axis (limits $40^\circ$ to $70^\circ$ for single lacing). Length of one bar between bolt centres:

$$l=\dfrac{160}{\sin45^\circ}=226$$

mm (measured along the bar). Each bar spans 160 mm along the column axis, so the connections on the same flange line are $2\times160=320$ mm apart.

*Force in one lacing bar:*

$$F=\frac{V_1}{\sin\theta}=\frac{18.75}{\sin45^\circ}=26.5\ \text{kN}$$

*Section of the flat:* thickness

$$t\ge\dfrac{l}{40}=\dfrac{226}{40}=5.7$$

mm (single lacing). Adopt **flat 50 mm × 8 mm** with one M16 bolt (4.6) at each end ($d_0=18$ mm, end distance $\ge1.5d_0=27$ mm ✓, flat width $\ge$ 3 × bolt diameter = 48 mm).

- Slenderness: $r=t/\sqrt{12}=2.31$ mm, $\lambda=\dfrac{l}{r}=\dfrac{226}{2.31}=98<145$ ✓ (limit 145).
- Compression: for $\lambda=98$ (class c) $f_{cd}=110$ N/mm$^2$, $P_d=110\times50\times8=44$ kN $>26.5$ ✓.
- Tension (net section): $T_{dn}=\dfrac{0.9\times(50-18)\times8\times410}{1.25}=75.6$ kN $>26.5$ ✓.
- Bolt M16 in single shear: $V_{dsb}=\dfrac{400}{\sqrt3}\times\dfrac{157}{1.25}=29.0$ kN $>26.5$ ✓; bearing on the 8 mm flat: $\dfrac{2.5\times0.55\times16\times8\times410}{1.25}=57.7$ kN ✓. One bolt at each end is enough.

*Check of the main channels between lacing points.* Slenderness of one channel between the connections $=\dfrac{320}{26}=12.3\le\min(50,\ 0.7\lambda_{max})=\min(50,\ 32)$ ✓ (IS 800 cl. 10.7.6).

*Tie plates (end and intermediate), cl. 10.7.7.* The lacing is terminated by a **tie plate** at the ends and at the points where the lacing is interrupted. Effective depth of the end tie plate $\ge$ the distance between the bolt lines $=160$ mm; the intermediate tie plate $\ge\tfrac34\times160=120$ mm; thickness $\ge\dfrac{1}{50}\times160=3.2$ mm $\to$ **8 mm**. Provide end tie plates 160 × 8 mm with 2 M16 bolts each side, as the length along the column of 200 mm.

$$\boxed{\text{2 ISMC 300 toe-to-toe, clear gap 100 mm; single lacing 50}\times8\text{ flats at }45^\circ\text{ with M16 bolts; tie plates 160}\times8}$$

```figure caption="Question 3: column of two ISMC 300 channels toe-to-toe (clear gap 100 mm), single lacing of 50x8 flats at 45 degrees, end tie plates 160 x 8; cross-section on the right."
fig,(a,b)=plt.subplots(1,2,figsize=(5.8,3.4),gridspec_kw={"width_ratios":[1,1]})
a.set_xlim(0,10); a.set_ylim(0,12); a.axis("off")
a.add_patch(plt.Rectangle((2,0.5),0.8,11,fc="#c9d6e8",ec=INK)); a.add_patch(plt.Rectangle((7.2,0.5),0.8,11,fc="#c9d6e8",ec=INK))
a.add_patch(plt.Rectangle((2,0.5),6,0.9,fc="#9aa5b5",ec=INK)); a.add_patch(plt.Rectangle((2,10.6),6,0.9,fc="#9aa5b5",ec=INK))
ys=np.linspace(1.4,10.6,7)
for i in range(6):
    p=((2.8,ys[i]),(7.2,ys[i+1])) if i%2==0 else ((7.2,ys[i]),(2.8,ys[i+1]))
    a.plot([p[0][0],p[1][0]],[p[0][1],p[1][1]],color="#d9534f",lw=2)
a.text(5,0.0,"single lacing at 45 deg",ha="center",fontsize=7.5); a.text(5,11.7,"tie plates",ha="center",fontsize=7,color=MUTED)
b.set_xlim(-6,6); b.set_ylim(-5,5); b.set_aspect("equal"); b.axis("off"); b.set_title("section (toe-to-toe)",fontsize=8)
for s in (-1,1):
    x0=s*0.5*1.0
    # channel: web outside, flanges pointing inward
    xw=s*3.8; b.add_patch(plt.Rectangle((xw-0.35,-3.0),0.7,6.0,fc="#c9d6e8",ec=INK))
    for yy in (-3.0,2.6): b.add_patch(plt.Rectangle((min(xw,s*1.0),yy),abs(xw-s*1.0),0.4,fc="#c9d6e8",ec=INK))
b.annotate("",xy=(-1.0,0),xytext=(1.0,0),arrowprops=dict(arrowstyle="<->",color=INK)); b.text(0,0.4,"100",ha="center",fontsize=7)
b.text(0,-4.4,"ISMC 300 x 2, flange tips face each other",ha="center",fontsize=7)
fig.tight_layout()
```

@s 4
**(a) Simply supported beam, clear span 3.2 m on 150 mm walls.**

*Effective span* (IS 800 cl. 8.2.1.3): clear span + 150 mm bearing (the distance between the centres of bearings)

$$L=3.2+0.15=3.35\ \text{m.}$$

*Loads.* Imposed udl $=20$ kN/m, self-weight assumed $0.37$ kN/m (ISMB 250, 37.3 kg/m); point load $10$ kN at mid-span. Partial safety factor for loads 1.5:

$$\begin{gathered}w_u=1.5(20+0.37)=30.55\ \text{kN/m} \\ W_u=1.5\times10=15\ \text{kN}\end{gathered}$$

$$M_u=\frac{w_uL^2}{8}+\frac{W_uL}{4}=\frac{30.55\times3.35^2}{8}+\frac{15\times3.35}{4}=42.9+12.6=55.4\ \text{kN m}$$

$$V_u=\frac{w_uL}{2}+\frac{W_u}{2}=51.2+7.5=58.7\ \text{kN}$$

*Trial section* **ISMB 250**: $h=250$, $b_f=125$, $t_f=12.5$, $t_w=6.9$, $R_1=13$ mm, $A=4755$ mm$^2$, $I_{xx}=5131.6$ cm$^4$, $I_{yy}=334.5$ cm$^4$, $Z_p=465.7$ cm$^3$. Section classification: $\varepsilon=1$;

$$b/t_f=\dfrac{62.5}{12.5}=5<9.4$$

and

$$d/t_w=\dfrac{199}{6.9}=28.8<84$$

**plastic** ($\beta_b=1$).

*Lateral-torsional buckling* (the beam is laterally unrestrained, $L_{LT}=3350$ mm, simply supported with torsional restraint at the ends).

$$I_t=\sum bt^3/3=1.87\times10^5$$

mm$^4$,

$$I_w=I_y\,h_f^2/4=4.72\times10^{10}$$

mm$^6$ with $h_f=237.5$ mm, $G=0.769\times10^5$ N/mm$^2$:

$$M_{cr}=\sqrt{\frac{\pi^2EI_y}{L_{LT}^2}\left(GI_t+\frac{\pi^2EI_w}{L_{LT}^2}\right)}=115.6\ \text{kN m}$$

$$\lambda_{LT}=\sqrt{\frac{\beta_bZ_pf_y}{M_{cr}}}=\sqrt{\frac{465.7\times10^3\times250}{115.6\times10^6}}=1.00$$

For a rolled section $\alpha_{LT}=0.21$:

$$\phi_{LT}=0.5\left[1+0.21(1.00-0.2)+1.00^2\right]=1.08$$

$$\chi_{LT}=\dfrac{1}{\phi_{LT}+\sqrt{\phi_{LT}^2-\lambda_{LT}^2}}=0.663$$

so

$$f_{bd}=\dfrac{\chi_{LT}f_y}{\gamma_{m0}}=150.7$$

N/mm$^2$.

$$M_d=\beta_bZ_pf_{bd}=465.7\times10^3\times150.7=70.2\ \text{kN m}>M_u=55.4\ \text{kN m}\ \checkmark$$

*Shear:*

$$V_d=\dfrac{f_yh\,t_w}{\sqrt3\gamma_{m0}}=\dfrac{250\times250\times6.9}{\sqrt3\times1.1}=226$$

kN $>58.7$ kN ✓ (also $V<0.6V_d$, so low shear: the moment capacity is not reduced).

*Deflection* under the unfactored imposed load (limit $L/300$ for a beam supporting brittle finishes, $=11.2$ mm):

$$\delta=\frac{5wL^4}{384EI}+\frac{WL^3}{48EI}=\frac{5\times20\times3350^4}{384\times2\times10^5\times5.1316\times10^7}+\frac{10\times10^3\times3350^3}{48\times2\times10^5\times5.1316\times10^7}=3.2+0.76=3.96\ \text{mm}\ll11.2\ \checkmark$$

**Check of the web (stiffened/unstiffened bearing, cl. 8.7.1.5 to 8.7.4).**

*Web buckling at the support* (stiff bearing length $b_1=150$ mm, the wall thickness). Dispersion at 45° to the mid-depth:

$$n_1=h/2=125$$

mm. Clear web depth

$$d=250-2(12.5+13)=199$$

mm. Slenderness

$$\lambda=2.5d/t_w=\dfrac{2.5\times199}{6.9}=72.1$$

class c curve: $f_{cd}=148.9$ N/mm$^2$.

$$F_w=(b_1+n_1)t_wf_{cd}=(150+125)\times6.9\times148.9=282.5\ \text{kN}>V_u=58.7\ \text{kN}\ \checkmark$$

*Web crushing (bearing / yielding)*:

$$n_2=2.5(t_f+R_1)=2.5(12.5+13)=63.75\ \text{mm,}$$

$$F_{psd}=\frac{(b_1+n_2)t_wf_{yw}}{\gamma_{m0}}=\frac{(150+63.75)\times6.9\times250}{1.1}=335\ \text{kN}>58.7\ \text{kN}\ \checkmark$$

The web is safe against buckling and crushing, and no bearing stiffener is needed at the supports. The 15 kN point load from the secondary beam is far below $F_w$ and $F_{psd}$, so no load-bearing stiffener is needed at mid-span either; connect the secondary beam to the web by a cleat. Bearing stress of the beam on the wall: $\dfrac{58.7\times10^3}{125\times150}=3.1$ N/mm$^2$, acceptable for masonry in cement mortar (use a bearing plate or a concrete pad if the wall is weak).

$$\boxed{\text{Use ISMB 250 (utilisation 79\% in bending); LTB, shear, deflection and web checks are satisfied}}$$

```figure caption="Question 4(a): ISMB 250 simply supported over 3.35 m: factored loading (30.55 kN/m and a 15 kN point load), shear force and bending moment diagrams (Mu = 55.4 kN m at mid-span, Vu = 58.7 kN at the supports)."
fig,ax=plt.subplots(3,1,figsize=(5.0,4.6),sharex=True,gridspec_kw={"height_ratios":[1,1,1]})
L=3.35;x=np.linspace(0,L,400);w=30.55;W=15
V=w*(L/2-x)+np.where(x<L/2,W/2,-W/2)
Mx=w*x*(L-x)/2+np.where(x<L/2,W*x/2,W*(L-x)/2)
a=ax[0]; a.plot([0,L],[0,0],color=INK,lw=3); a.annotate("",xy=(L/2,0),xytext=(L/2,0.9),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=2)); a.text(L/2+0.1,0.75,"15 kN",fontsize=8,color="#d9534f")
for xx in np.linspace(0.1,L-0.1,15): a.annotate("",xy=(xx,0.05),xytext=(xx,0.4),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=0.8))
a.text(0.05,0.55,"30.55 kN/m",fontsize=8,color=ACCENT); a.set_ylim(-0.3,1.1); a.axis("off")
ax[1].fill_between(x,0,V,color="#cfe3f7"); ax[1].plot(x,V,color=ACCENT); ax[1].axhline(0,color=INK,lw=0.8); ax[1].text(0.05,V[0]-8,"58.7 kN",fontsize=8); ax[1].set_ylabel("SF (kN)",fontsize=8)
ax[2].fill_between(x,0,Mx,color="#f7d9d7"); ax[2].plot(x,Mx,color="#d9534f"); ax[2].text(L/2,Mx.max()+1,"55.4 kN m",ha="center",fontsize=8); ax[2].set_ylabel("BM (kN m)",fontsize=8); ax[2].set_ylim(0,66)
fig.tight_layout()
```

**(b) Sizing the web and flange plates of a welded plate girder (procedure).**

1. **Design forces.** Compute the factored maximum bending moment $M_u$ and shear force $V_u$ from the loads on the girder (including the estimated self-weight, 1 to 2 % of the load).
2. **Depth of the web.** Economic depth $d=\left(\dfrac{M_uk}{f_y/\gamma_{m0}}\right)^{1/3}$ with $k=\dfrac{d}{t_w}$ (range 150 to 200 for unstiffened or 200 to 345 for stiffened webs); in practice $d\approx L/10$ to $L/12$ and the clear depth is chosen in multiples of 50 mm, with an overall depth consistent with headroom.
3. **Thickness of the web.** $t_w=d/k$ must satisfy the serviceability limits $d/t_w\le200\varepsilon$ (no transverse stiffener) or $\le250\varepsilon$ (transverse stiffeners with $c\ge1.5d$) or $\le345\varepsilon^2$ (to prevent flange buckling into the web) and the shear check $V_u\le V_d=\dfrac{f_yd\,t_w}{\sqrt3\gamma_{m0}}$ (or the post-buckling shear strength by the simple post-critical method with intermediate stiffeners). The minimum thickness is 8 mm for normal environments.
4. **Area of the flanges.** Assuming that the flanges carry the entire moment: $A_f=\dfrac{M_u\gamma_{m0}}{f_yd}-\dfrac{A_w}{6}$ for the web ($A_w=dt_w$) taking part of the moment (when $d/t_w$ is small). Each flange is $A_f=b_ft_f$.
5. **Flange plate dimensions.** Choose $b_f\approx\dfrac{d}{5}$ to $\dfrac{d}{3}$ and $t_f=A_f/b_f$ so that the outstand satisfies the local buckling limit $\dfrac{b}{t_f}\le13.6\varepsilon$ (welded section, semi-compact) or $8.4\varepsilon$ (plastic/compact), with $t_f\ge$ 12 mm (for $b_f/t_f\le20$).
6. **Check** the girder: moment capacity (and the reduction for lateral-torsional buckling if the compression flange is not restrained), shear with the high-shear interaction when $V>0.6V_d$, deflection (limit $L/300$), web buckling and crushing at the supports and under the concentrated loads (design of the bearing and the intermediate stiffeners), and the **flange-to-web welds** (fillet welds) designed for the horizontal shear flow $q=\dfrac{VA_f\bar y}{I}$.
7. **Curtail the flange plates** where the moment reduces (extra plates theoretical cut-off + the extension needed for the weld length), and provide the splices.

@s 5
**(a) Design wind pressure on the roof (IS 875 Part 3:2015).**

*Data adopted:* basic wind speed $V_b=47$ m/s (Nepal and the Himalayan belt, NBC 104; the question gives none). Life 50 years, height 15 m, plan 40 m × 25 m.

*Design wind speed* $V_z=V_b\,k_1\,k_2\,k_3\,k_4$:

- $k_1$ (risk coefficient) $=1.0$ (general buildings, 50 years).
- $k_2$ (terrain, height and size): dense forest means **terrain category 4** (numerous closely spaced obstructions); the largest dimension (the diagonal or the 40 m length) falls in **class B** (20 to 50 m); at the height of 15 m, $k_2\approx0.80$ (Table 2; check the table which is permitted).
- $k_3$ (topography). The site is on a hill, slope $1{:}1.5$ ($\theta=33.7^\circ>17^\circ$): $k_3=1+Cs$ with $C=0.36$ for $\theta>17^\circ$ and the factor $s$ from the figure of Appendix C for the position at mid-height on the upwind slope of the hill (effective length $L_e=Z/0.3$ where $Z=800$ m is the height of the hill; the building is at $x=600$ m from the crest on the upwind side, $x/L_e\approx-0.23$): $s\approx0.5$, so

$$k_3=1+0.36\times0.5=1.18$$

- $k_4$ (importance for cyclonic region) $=1.0$.

$$V_z=47\times1.0\times0.80\times1.18\times1.0=44.4\ \text{m/s}$$

*Wind pressure:*

$$p_z=0.6V_z^2=0.6\times44.4^2=1182\ \text{N/m}^2=1.18\ \text{kN/m}^2$$

*Design pressure* $p_d=K_dK_aK_cp_z$ with the wind directionality factor $K_d=0.9$ (rectangular building), area averaging factor $K_a=0.8$ (for a tributary area greater than 100 m$^2$ on the roof) and the combination factor $K_c=0.9$ (for a wind pressure acting with both external and internal pressures):

$$p_d=0.9\times0.8\times0.9\times1.18=0.77\ \text{kN/m}^2$$

*Pressure coefficients on the roof.* The roof is flat (slope $<5^\circ$),

$$h/w=15/25=0.6$$

and

$$l/w=40/25=1.6$$

External coefficient for the roof (Table 5): suction over the whole roof, taking the worst value on the windward edge zones $C_{pe}=-0.8$ (average of $-0.7$ over the rest). **Normal opening (permeability 5 to 20 %):** $C_{pi}=\pm0.2$. The worst net uplift occurs with internal pressure $+0.2$:

$$C_p=C_{pe}-C_{pi}=-0.8-0.2=-1.0\ \text{(suction)}$$

$$\boxed{p_{roof}=C_p\,p_d=-1.0\times0.77=-0.77\ \text{kN/m}^2\ (\text{uplift/suction})}$$

For the central part of the roof ($C_{pe}=-0.7$): $-0.9\times0.77=-0.69$ kN/m$^2$. With $C_{pi}=-0.2$ the net pressure is only $-0.6\times0.77=-0.46$ kN/m$^2$. Total uplift on the roof: $0.77\times(40\times25)=770$ kN, which must be resisted by the dead load of the roof, the holding-down anchors and the connections.

**(b) Slab base for ISSC 150 (SC 150), 300 kN, M15 footing.**

*Section:* ISSC 150 (SC 150): depth $d=150$ mm, flange width $b_f=150$ mm, $t_f=9$ mm, $t_w=8.4$ mm. Load $P=300$ kN (taken as factored). Steel E250 ($f_y=250$).

*Bearing strength of concrete* (IS 800 cl. 7.4.1):

$$0.45f_{ck}=0.45\times15=6.75$$

N/mm$^2$.

$$A_{req}=\frac{P}{0.45f_{ck}}=\frac{300\times10^3}{6.75}=44\,444\ \text{mm}^2\ (\ge211\times211\text{ mm})$$

*Plate size.* Provide **B × L = 250 × 250 mm** ($62\,500$ mm$^2$). Actual bearing pressure

$$w=\frac{300\times10^3}{250\times250}=4.8\ \text{N/mm}^2<6.75\ \checkmark$$

*Projections* beyond the column:

$$a=\dfrac{L-0.95d}{2}=\dfrac{250-0.95\times150}{2}=53.75$$

mm (along the depth) and

$$b=\dfrac{B-b_f}{2}=\dfrac{250-150}{2}=50$$

mm (along the flange width).

*Thickness of the plate* (cl. 7.4.3.1; $a$ is the larger projection, $b$ the smaller):

$$t_s=\sqrt{\frac{2.5w\left(a^2-0.3b^2\right)\gamma_{m0}}{f_y}}=\sqrt{\frac{2.5\times4.8\times(53.75^2-0.3\times50^2)\times1.1}{250}}=\sqrt{\frac{12\times2139\times1.1}{250}}=10.6\ \text{mm}$$

and $t_s\ge t_f=9$ mm (the flange thickness of the column). **Adopt $t_s=12$ mm.**

*Connection of the column to the base plate:* the load is transferred by direct contact (the column end is machined, i.e. faced for bearing), so the weld is nominal: **6 mm fillet weld all round**, plus 4 anchor bolts M16 (nominal) at 25 mm from the plate edge to hold the column in position, and a **grout** of 25 mm cement (1:2) under the plate. Since the load is small, a gusset is not necessary.

$$\boxed{\text{Slab base plate }250\times250\times12\text{ mm with 4 anchor bolts M16, 6 mm fillet weld all round, on M15 concrete (bearing stress 4.8 N/mm}^2\text{)}}$$

```figure caption="Question 5(b): slab base 250 x 250 x 12 for ISSC 150: plan with projections a = 53.75 mm, b = 50 mm and four M16 anchor bolts; elevation with 300 kN axial load on the M15 footing."
fig,(a,b)=plt.subplots(1,2,figsize=(5.8,2.8),gridspec_kw={"width_ratios":[1,1]})
a.set_xlim(-0.5,10.5); a.set_ylim(-0.5,10.5); a.set_aspect("equal"); a.axis("off"); a.set_title("plan",fontsize=8.5)
a.add_patch(plt.Rectangle((0,0),10,10,fc="#dfe6f0",ec=INK))
s=10/250
a.add_patch(plt.Rectangle((50*s,(250-150)/2*s),150*s,150*s,fill=False,ec=INK,lw=1.2)); a.add_patch(plt.Rectangle((50*s,(125-75)*s+ (150*s-9*s*0)/2-75*s+75*s-4.2*s),150*s,8.4*s,fc=INK)) if False else None
a.plot([50*s,200*s],[125*s-0.0,125*s],color=INK,lw=2.0)
a.plot([50*s,200*s],[50*s,50*s],color=INK,lw=1.2); a.plot([50*s,200*s],[200*s,200*s],color=INK,lw=1.2)
for x,y in ((25,25),(225,25),(25,225),(225,225)): a.add_patch(plt.Circle((x*s,y*s),0.35,fc="white",ec=INK))
a.annotate("",xy=(0,-0.3),xytext=(50*s,-0.3),arrowprops=dict(arrowstyle="<->",color=ACCENT)); a.text(1.0,-0.45,"b=50",fontsize=7,color=ACCENT,va="top")
b.set_xlim(0,10); b.set_ylim(0,10); b.axis("off"); b.set_title("elevation",fontsize=8.5)
b.add_patch(plt.Rectangle((0.5,0.5),9,2.2,fc="#c9ccd1",ec=INK)); b.text(5,1.6,"M15 footing",ha="center",fontsize=8)
b.add_patch(plt.Rectangle((1.5,2.7),7,0.4,fc="#9aa5b5",ec=INK)); b.text(9.6,2.9,"PL 12",fontsize=7,va="center")
b.add_patch(plt.Rectangle((3.5,3.1),3,5.0,fc="#dfe6f0",ec=INK)); b.text(5,5.6,"ISSC 150",ha="center",fontsize=8)
b.annotate("",xy=(5,8.1),xytext=(5,9.7),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=2)); b.text(5.4,9.3,"300 kN",fontsize=8,color="#d9534f")
fig.tight_layout()
```
