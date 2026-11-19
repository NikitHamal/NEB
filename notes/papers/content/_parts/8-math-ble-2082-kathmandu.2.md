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
