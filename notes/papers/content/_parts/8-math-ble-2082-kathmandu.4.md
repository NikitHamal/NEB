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
