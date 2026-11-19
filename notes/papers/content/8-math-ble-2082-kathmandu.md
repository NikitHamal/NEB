---
file: NEBians-BLE-Past-Paper-Grade-8-Mathematics-2082-Kathmandu.pdf
subject: Compulsory Mathematics
grade: 8
year_bs: 2082
year_ad: 2026
stream: Basic Level Examination, Kathmandu Metropolitan City
code:
kind: BLE Past Paper
time: 2 hrs
marks: 50
students: Class 8 Basic Level Examination (BLE) paper set by Kathmandu Metropolitan City for the year 2082. Questions are re-typeset in English from the published paper; the layout and every solution are NEBians.
category: Basic Level Exam
---
## Attempt all the questions
<small>Full marks 50 · time 2 hours · figures in the margin show the marks</small>

@q 1
A school offers three extra-curricular activities: dance, music and painting. They are denoted by the set $A=\{\text{dance, music, painting}\}$.
(a) Construct any two proper subsets that show different combinations of two activities made from set $A$. [[2]]
(b) "Every set is an improper subset of itself." Do you agree? Give a reason. [[1]]

@q 2
According to the National Census 2078, the population density of Nepal was 198 people per square kilometre.
(a) Define a rational number. [[1]]
(b) Convert 198 into the quinary number system. [[1]]
(c) Prove that $1243_5 = 11000110_2$. [[2]]

@q 3
Hari deposited Rs. 4,00,000 in a bank in the ratio $2:3$ in the names of his son and daughter.
(a) How much money did Hari deposit in the bank for his daughter? [[2]]
(b) If the amount deposited in the son's name is doubled while the amount in the daughter's name is kept the same, what will be the new ratio? [[2]]
(c) If Rs. 4,00,000 had been invested at a 10% simple interest rate, how much interest would have been received after 2 years? Find it. [[1]]

@q 4
18 workers spent 12 days to repair a 432-metre-long irrigation canal.
(a) What is the difference between direct and indirect variation? Write it. [[1]]
(b) How many metres of canal can 9 workers repair in 1 day? [[2]]
(c) How many metres of canal can 9 workers repair in 6 days? [[1]]
(d) How many more days will 9 workers need to repair the 432-metre-long canal? [[1]]

<div style="break-before:page"></div>

@q 5
In the figure, $ABCD$ is a trapezium, where $AB=14$ cm, $CD=10$ cm, $BC=h$ cm and the area of triangle $ABC$ is 56 sq. cm.

```figure caption="Trapezium ABCD, with the right angle at B and C."
fig, ax = plt.subplots(figsize=(3.0,1.6))
A,B,C,D=(0,0),(14,0),(14,8),(4,8)
ax.fill([A[0],B[0],C[0],D[0]],[A[1],B[1],C[1],D[1]],fc=ACCENT,alpha=0.07,ec=INK,lw=1.4)
ax.plot([A[0],C[0]],[A[1],C[1]],color=INK,lw=1.2)
ax.plot([13,13,14],[0,1,1],color=INK,lw=0.9); ax.plot([13,13,14],[8,7,7],color=INK,lw=0.9)
for t,p,o in [('A',A,(-0.9,-0.9)),('B',B,(0.5,-0.9)),('C',C,(0.5,0.3)),('D',D,(-0.9,0.3))]:
    ax.text(p[0]+o[0],p[1]+o[1],t,fontsize=9,fontweight='bold')
ax.text(7,-1.5,'14 cm',ha='center',fontsize=8); ax.text(9,8.5,'10 cm',ha='center',fontsize=8); ax.text(14.6,4,'h cm',fontsize=8,va='center')
ax.text(10.6,2.4,'56 cm$^2$',fontsize=8,ha='center')
ax.set_xlim(-1.5,17); ax.set_ylim(-2.4,10); ax.set_aspect('equal'); ax.axis('off')
```

(a) Write the formula for finding the area of a right-angled triangle. [[1]]
(b) Find the value of $BC$ $(h)$. [[1]]
(c) Calculate the area of the trapezium $ABCD$. [[2]]
(d) Are the areas of the two triangles $ADC$ and $ABC$ equal? Give a logical answer. [[1]]

@q 6
(a) Write the value of $(3m+n)^0$. [[1]]
(b) Simplify: $p^{a-b}\times p^{b-c}\times p^{c-a}$. [[2]]

@q 7
(a) How many maximum values of $x$ are there in the quadratic equation $ax^2+bx+c=0,\ a\neq 0$? [[1]]
(b) Simplify: $\dfrac{ax}{ax-ay}+\dfrac{ay}{ay-ax}$. [[2]]

@q 8
Here, the sample of algebraic tiles of $x^2+5x+6$ is illustrated: one $x^2$ tile, five $x$ tiles and six unit tiles.

```figure caption="Algebraic tiles of x² + 5x + 6."
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.0,1.25))
ax.add_patch(Rectangle((0,0),3,3,fc=ACCENT,alpha=0.18,ec=INK,lw=1.2)); ax.text(1.5,1.5,'$x^2$',ha='center',va='center',fontsize=11)
for i in range(5):
    ax.add_patch(Rectangle((3.6+i*0.8,0),0.6,3,fc='white',ec=INK,lw=1.2)); ax.text(3.9+i*0.8,1.5,'$x$',ha='center',va='center',fontsize=9)
for c in range(2):
    for r in range(3):
        ax.add_patch(Rectangle((8.2+c*0.9,r*1.0),0.8,0.8,fc=INK,alpha=0.85,ec=INK,lw=0.8))
ax.set_xlim(-0.3,10.3); ax.set_ylim(-0.3,3.3); ax.set_aspect('equal'); ax.axis('off')
```

(a) Present the given tiles in a rectangular shape by arranging them. [[2]]
(b) Find the length and breadth of the rectangular shape in terms of $x$. [[2]]

<div style="break-before:page"></div>

@q 9
In the given graph, a triangle with vertices $(-3,2)$, $(3,6)$ and $(5,3)$ is shown.

```figure caption="The triangle on the coordinate plane."
fig, ax = plt.subplots(figsize=(2.7,2.5))
ax.set_xticks(range(-10,11,5)); ax.set_yticks(range(-10,11,5)); ax.grid(True,color=GRID,lw=0.6)
ax.axhline(0,color=INK,lw=1); ax.axvline(0,color=INK,lw=1)
P=[(-3,2),(3,6),(5,3)]
ax.fill([p[0] for p in P],[p[1] for p in P],fc=ACCENT,alpha=0.12,ec=INK,lw=1.4)
for (x,y),o in zip(P,[(-1.6,-1.6),(-0.6,0.7),(0.6,-0.9)]): ax.text(x+o[0],y+o[1],f'({x},{y})',fontsize=7)
ax.set_xlim(-10,10); ax.set_ylim(-10,10); ax.set_aspect('equal'); ax.tick_params(labelsize=6)
for s in ax.spines.values(): s.set_visible(False)
```

(a) Write the formula to find the value of each interior angle of a regular polygon. [[1]]
(b) Find the distance between $(-3,2)$ and $(3,6)$. [[2]]
(c) Write the coordinates of the vertices of the image of the triangle after reflecting it in the $X$-axis. [[3]]
(d) Is the image of the triangle after reflecting in the $Y$-axis congruent with the original triangle? Give logic. [[1]]

@q 10
In the figure, four equilateral triangles having sides of 5 cm are shown.

```figure caption="Four equilateral triangles, side 5 cm."
fig, ax = plt.subplots(figsize=(2.0,1.25))
for i in range(4):
    x0=(i%2)*6.0; y0=(i//2)*4.6
    ax.fill([x0,x0+5,x0+2.5],[y0,y0,y0+4.33],fc='white',ec=INK,lw=1.3)
ax.set_xlim(-0.4,11.4); ax.set_ylim(-0.4,9.2); ax.set_aspect('equal'); ax.axis('off')
```

(a) Define regular tessellation. [[1]]
(b) Rama says, "If a square having sides of 5 cm can be added to the given four equilateral triangles, we will form a square pyramid." Do you agree? If yes, present it with measurement. [[2]]

@q 11
In the figure, rectangle $ABCD$ has length $BC=8$ cm and breadth $CD=6$ cm.

```figure caption="Rectangle ABCD with diagonal BD."
fig, ax = plt.subplots(figsize=(2.5,1.5))
ax.plot([0,8,8,0,0],[0,0,6,6,0],color=INK,lw=1.4); ax.plot([0,8],[0,6],color=INK,lw=1.1)
ax.plot([7.2,7.2,8],[0,0.8,0.8],color=INK,lw=0.9)
for t,x,y in [('A',-0.8,6.2),('B',-0.8,-0.9),('C',8.2,-0.9),('D',8.2,6.2)]: ax.text(x,y,t,fontsize=9,fontweight='bold')
ax.text(4,-1.1,'8 cm',ha='center',fontsize=8); ax.text(8.9,3,'6 cm',fontsize=8,va='center')
ax.set_xlim(-1.5,10.8); ax.set_ylim(-1.8,7.4); ax.set_aspect('equal'); ax.axis('off')
```

(a) Find the length of the diagonal $BD$. [[2]]
(b) Construct the rectangle $ABCD$ by using a compass with the given dimensions. [[3]]

@q 12
Here, the run scores of the cricket player Rohit Paudel in 8 matches against America are given: 62, 2, 62, 16, 16, 96, 1, 2.
(a) Write the formula to find the mean of an individual series. [[1]]
(b) What is the average (mean) run score of Rohit Paudel in the 8 matches played against America? Find it. [[1]]
(c) If he wants to make his average (mean) run score 40 including the ninth match, how many runs does he need to score in the ninth match? [[1]]

<!-- SOLUTIONS -->

@s 1
**(a)** The set is $A=\{\text{dance, music, painting}\}$. A proper subset is a subset that is not equal to $A$ itself. Two proper subsets with two activities each are
$$B=\{\text{dance, music}\}$$
$$C=\{\text{music, painting}\}$$
(Also acceptable: $\{\text{dance, painting}\}$.) Both are subsets of $A$ and neither equals $A$. [2]

**(b)** Yes, I agree. Every element of a set $A$ is also an element of $A$, so $A\subseteq A$. A subset that is equal to the set itself is called an improper subset. [1]

@s 2
**(a)** A number that can be written in the form $\dfrac pq$, where $p$ and $q$ are integers and $q\neq0$, is called a rational number. Examples: $\dfrac35$, $-4$, $0.25$. [1]

**(b)** Divide 198 repeatedly by 5 and write the remainders from bottom to top.

| Division | Quotient | Remainder |
|---|---|---|
| $198\div5$ | 39 | 3 |
| $39\div5$ | 7 | 4 |
| $7\div5$ | 1 | 2 |
| $1\div5$ | 0 | 1 |

So $198=1243_5$. [1]

**(c)** Change both numbers to base 10.
$$1243_5=1\times5^3+2\times5^2+4\times5+3=125+50+20+3=198$$
Now convert 198 to binary by repeated division by 2.

| Division | Quotient | Remainder |
|---|---|---|
| $198\div2$ | 99 | 0 |
| $99\div2$ | 49 | 1 |
| $49\div2$ | 24 | 1 |
| $24\div2$ | 12 | 0 |
| $12\div2$ | 6 | 0 |
| $6\div2$ | 3 | 0 |
| $3\div2$ | 1 | 1 |
| $1\div2$ | 0 | 1 |

Reading the remainders from bottom to top gives $198=11000110_2$. Check: $128+64+4+2=198$.

Hence $1243_5=198=11000110_2$. Proved. [2]

@s 3
**(a)** Total deposit $=$ Rs. 4,00,000, ratio son : daughter $=2:3$, sum of ratio $=2+3=5$.
$$\text{Daughter's share}=\frac35\times4{,}00{,}000=\text{Rs. }2{,}40{,}000$$
Hari deposited **Rs. 2,40,000** for his daughter. [2]

**(b)** The son's share is two fifths of Rs. 4,00,000, which is Rs. 1,60,000. Doubled, it becomes Rs. 3,20,000. The daughter's amount stays Rs. 2,40,000.
$$\text{New ratio}=3{,}20{,}000:2{,}40{,}000=32:24=4:3$$
The new ratio of son : daughter is **4 : 3**. [2]

**(c)** $P=$ Rs. 4,00,000, $R=10\%$, $T=2$ years.
$$I=\frac{P\times T\times R}{100}=\frac{4{,}00{,}000\times2\times10}{100}=\text{Rs. }80{,}000$$
The interest after 2 years would be **Rs. 80,000**. [1]

@s 4
**(a)** In direct variation, when one quantity increases the other also increases (or one decreases and the other decreases) in the same ratio, so their ratio stays constant. In indirect variation, when one quantity increases the other decreases in the same ratio, so their product stays constant. [1]

**(b)** 18 workers repair 432 m in 12 days, so the work of one worker in one day is
$$\frac{432}{18\times12}=2\text{ m}.$$
Then 9 workers in 1 day repair $9\times2=$ **18 m**. [2]

**(c)** In 6 days, 9 workers repair $18\times6=$ **108 m**. [1]

**(d)** Time needed by 9 workers for 432 m: $\dfrac{432}{18}=24$ days (fewer workers, more days, so this is indirect variation: $18\times12=9\times d$ gives $d=24$). They need $24-12=$ **12 more days** than the 18 workers. [1]

@s 5
**(a)** The area of a right-angled triangle is half the product of its base and height (the two sides that meet at the right angle):
$$A=\frac12\times\text{base}\times\text{height}$$ [1]

**(b)** In the right-angled triangle $ABC$, the base is $AB=14$ cm and the height is $BC=h$.
$$\frac12\times14\times h=56$$
$$7h=56$$
$$h=8$$
So $BC=h=$ **8 cm**. [1]

**(c)** $AB\parallel CD$, so $ABCD$ is a trapezium with parallel sides 14 cm and 10 cm and height $BC=8$ cm.
$$\text{Area}=\frac12(AB+CD)\times h=\frac12(14+10)\times8=\frac12\times24\times8=96\text{ cm}^2$$
[2]

**(d)** No, they are not equal. Area of $\triangle ABC=56$ cm$^2$. Area of $\triangle ADC=96-56=40$ cm$^2$ (check: $\tfrac12\times CD\times8=\tfrac12\times10\times8=40$). Both triangles lie between the same parallel lines, so they have the same height of 8 cm, but their bases $AB=14$ cm and $CD=10$ cm are different. Equal height with unequal bases gives unequal areas. [1]

@s 6
**(a)** Any non-zero quantity raised to the power 0 is 1, so $(3m+n)^0=$ **1** (for $3m+n\neq0$). [1]

**(b)** Same base, so add the powers.
$$p^{a-b}\times p^{b-c}\times p^{c-a}=p^{(a-b)+(b-c)+(c-a)}=p^{0}=1$$
[2]

@s 7
**(a)** A quadratic equation has degree 2, so it has at most **2** values of $x$ (two roots). [1]

**(b)** Take the common factor out of each denominator. $ay-ax=-(ax-ay)$, so
$$\frac{ax}{ax-ay}+\frac{ay}{ay-ax}=\frac{ax}{ax-ay}-\frac{ay}{ax-ay}=\frac{ax-ay}{ax-ay}=1\qquad(x\neq y).$$
[2]

@s 8
**(a)** Arrange the six unit tiles, five $x$ tiles and the $x^2$ tile without gaps or overlaps: the $x^2$ tile in one corner, three $x$ tiles standing beside it, two $x$ tiles lying above it, and the six unit tiles filling the remaining corner as a $3\times2$ block. [2]

```figure caption="The tiles arranged as a rectangle of length x + 3 and breadth x + 2."
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.2,2.5))
s=3.0
ax.add_patch(Rectangle((0,0),s,s,fc=ACCENT,alpha=0.18,ec=INK,lw=1.2)); ax.text(s/2,s/2,'$x^2$',ha='center',va='center',fontsize=12)
for i in range(3):
    ax.add_patch(Rectangle((s+i,0),1,s,fc='white',ec=INK,lw=1.2)); ax.text(s+i+0.5,s/2,'$x$',ha='center',va='center',fontsize=9)
for j in range(2):
    ax.add_patch(Rectangle((0,s+j),s,1,fc='white',ec=INK,lw=1.2)); ax.text(s/2,s+j+0.5,'$x$',ha='center',va='center',fontsize=9)
for i in range(3):
    for j in range(2):
        ax.add_patch(Rectangle((s+i,s+j),1,1,fc=INK,alpha=0.85,ec='white',lw=0.8))
ax.annotate('',xy=(0,-0.5),xytext=(s+3,-0.5),arrowprops=dict(arrowstyle='<->',color=ACCENT)); ax.text((s+3)/2,-1.2,'length = $x+3$',ha='center',fontsize=9)
ax.annotate('',xy=(s+3.5,0),xytext=(s+3.5,s+2),arrowprops=dict(arrowstyle='<->',color=ACCENT)); ax.text(s+3.8,(s+2)/2,'breadth\n$=x+2$',va='center',fontsize=9)
ax.set_xlim(-0.5,s+6); ax.set_ylim(-1.8,s+2.5); ax.set_aspect('equal'); ax.axis('off')
```

**(b)** Read the sides from the arrangement. Along the bottom there is one $x^2$ tile (width $x$) and three $x$ tiles (width $1$ each), so the length is $x+3$. Up the side there is one $x^2$ tile (height $x$) and two $x$ tiles (height 1 each), so the breadth is $x+2$.

Check by multiplying the length and breadth:
$$(x+3)(x+2)=x^2+2x+3x+6=x^2+5x+6$$
Therefore
$$x^2+5x+6=(x+3)(x+2),$$
length $=\mathbf{x+3}$ and breadth $=\mathbf{x+2}$. [2]

@s 9
**(a)** Each interior angle of a regular polygon of $n$ sides $=\dfrac{(n-2)\times180^\circ}{n}$. [1]

**(b)** Distance between $(x_1,y_1)=(-3,2)$ and $(x_2,y_2)=(3,6)$:
$$d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}=\sqrt{(3+3)^2+(6-2)^2}=\sqrt{36+16}=\sqrt{52}=2\sqrt{13}\approx7.21\text{ units}$$
[2]

**(c)** In reflection in the $X$-axis, $(x,y)\to(x,-y)$.
$$A(-3,2)\to A'(-3,-2),\qquad B(3,6)\to B'(3,-6),\qquad C(5,3)\to C'(5,-3)$$
The vertices of the image are **$(-3,-2)$, $(3,-6)$ and $(5,-3)$**. [3]

**(d)** Yes, congruent. Under reflection in the $Y$-axis, $(x,y)\to(-x,y)$, giving $(3,2)$, $(-3,6)$ and $(-5,3)$. A reflection only flips the figure over the mirror line; it keeps all lengths and angles unchanged (for example the side from $(-3,2)$ to $(3,6)$ becomes the side from $(3,2)$ to $(-3,6)$, still $\sqrt{52}$). So the image and the original triangle have the same shape and size. [1]

```figure caption="The triangle (black) and its images in the X-axis (blue) and the Y-axis (orange)."
fig, ax = plt.subplots(figsize=(3.8,3.5))
ax.set_xticks(range(-10,11,5)); ax.set_yticks(range(-10,11,5)); ax.grid(True,color=GRID,lw=0.6)
ax.axhline(0,color=INK,lw=1); ax.axvline(0,color=INK,lw=1)
P=[(-3,2),(3,6),(5,3)]
def tri(pts,c,lab,fa):
    ax.fill([p[0] for p in pts],[p[1] for p in pts],fc=c,alpha=fa,ec=c,lw=1.4)
tri(P,INK,'',0.10); tri([(x,-y) for x,y in P],ACCENT,'',0.14); tri([(-x,y) for x,y in P],'#c2410c','',0.12)
ax.text(1,1.2,'ABC',fontsize=7); ax.text(1,-1.9,"A'B'C'",fontsize=7,color=ACCENT); ax.text(-3,1.2,"A''B''C''",fontsize=7,color='#c2410c')
ax.set_xlim(-10,10); ax.set_ylim(-10,10); ax.set_aspect('equal'); ax.tick_params(labelsize=6)
for s in ax.spines.values(): s.set_visible(False)
```

@s 10
**(a)** Covering a plane completely with copies of one type of regular polygon, without any gap or overlap, is called a regular tessellation. Only equilateral triangles, squares and regular hexagons can do this. [1]

**(b)** Yes, I agree. A square pyramid has one square base and four triangular faces that meet at the top. If the base is a square of side 5 cm, each side of the base is the base edge of one triangular face, and the four equilateral triangles of side 5 cm fit exactly on the four sides of the square. So the five pieces fold into a square pyramid, with
- base: square of 5 cm $\times$ 5 cm,
- four faces: equilateral triangles with all sides 5 cm (so every slant edge is also 5 cm),
- slant height of a face $=\dfrac{\sqrt3}{2}\times5\approx4.33$ cm.

[2]

```figure caption="Net of the square pyramid: a 5 cm square with four equilateral triangles of side 5 cm."
fig, ax = plt.subplots(figsize=(3.4,3.4))
h=5*3**0.5/2
ax.fill([0,5,5,0],[0,0,5,5],fc=ACCENT,alpha=0.14,ec=INK,lw=1.4)
for pts in ([(0,0),(5,0),(2.5,-h)],[(0,5),(5,5),(2.5,5+h)],[(0,0),(0,5),(-h,2.5)],[(5,0),(5,5),(5+h,2.5)]):
    ax.fill([p[0] for p in pts],[p[1] for p in pts],fc='white',ec=INK,lw=1.4)
ax.text(2.5,2.5,'square\n5 cm',ha='center',va='center',fontsize=8)
ax.text(2.5,-h*0.45,'5 cm',ha='center',fontsize=7,va='center'); ax.text(2.5,5+h*0.45,'5 cm',ha='center',fontsize=7,va='center')
ax.set_xlim(-5.2,10.2); ax.set_ylim(-5,10); ax.set_aspect('equal'); ax.axis('off')
```

@s 11
**(a)** The diagonal $BD$ is the hypotenuse of the right-angled triangle $BCD$ (right angle at $C$), with $BC=8$ cm and $CD=6$ cm. By the Pythagoras theorem,
$$BD^2=BC^2+CD^2=8^2+6^2=64+36=100$$
$$BD=\sqrt{100}=10\text{ cm}$$
[2]

**(b)** Steps of construction (compass, ruler and pencil):
1. Draw a line segment $BC=8$ cm.
2. At $C$, construct a perpendicular to $BC$: with centre $C$ draw arcs cutting $BC$ produced on both sides, then draw bigger arcs from those two points to meet above $C$ and join this point to $C$.
3. With centre $C$ and radius 6 cm draw an arc on this perpendicular. Mark the point $D$.
4. With centre $B$ and radius 6 cm draw an arc above $B$.
5. With centre $D$ and radius 8 cm draw an arc to cut the arc of step 4. Mark the point of intersection as $A$.
6. Join $AB$, $AD$ (and $BD$ to check it is 10 cm). $ABCD$ is the required rectangle.

[3]

```figure caption="Construction of rectangle ABCD (BC = 8 cm, CD = 6 cm)."
import numpy as np
fig, ax = plt.subplots(figsize=(3.8,2.5))
ax.plot([0,8,8,0,0],[0,0,6,6,0],color=INK,lw=1.5); ax.plot([0,8],[0,6],color=INK,lw=0.8,ls='--')
ax.plot([8,8],[0,8.2],color=GRID,lw=1,zorder=0)
def arc(cx,cy,r,a0,a1):
    a=np.radians(np.linspace(a0,a1,30)); ax.plot(cx+r*np.cos(a),cy+r*np.sin(a),color=ACCENT,lw=1)
arc(8,0,6,78,102); arc(0,0,6,78,102); arc(8,6,8,168,192)
for t_,x,y in [('A',-0.8,6.2),('B',-0.8,-0.9),('C',8.2,-0.9),('D',8.2,6.2)]: ax.text(x,y,t_,fontsize=9,fontweight='bold')
ax.text(4,-1.1,'8 cm',ha='center',fontsize=8); ax.text(8.9,3,'6 cm',fontsize=8,va='center')
ax.set_xlim(-1.5,11); ax.set_ylim(-1.8,8.5); ax.set_aspect('equal'); ax.axis('off')
```

@s 12
**(a)** Mean $\bar x=\dfrac{\sum x}{n}$, the sum of all the observations divided by the number of observations. [1]

**(b)** The sum of the scores is 257 and the number of matches is 8.
$$\text{Sum}=62+2+62+16+16+96+1+2=257$$
$$\bar x=\frac{257}{8}=32.125$$
His average score is about **32.1 runs** ($32\tfrac18$). [1]

**(c)** For 9 matches with mean 40, the total must be $9\times40=360$. Runs needed in the ninth match are 360 minus 257, which is **103 runs**. Check: the new mean is 360 divided by 9, which is 40. [1]

**Marks check:** 3 + 4 + 5 + 5 + 5 + 3 + 3 + 4 + 7 + 3 + 5 + 3 = 50.
