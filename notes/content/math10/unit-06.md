---
subject: Mathematics
grade: 10
unit: 6
title: Cylinder and Sphere
hours: 0
area: Compulsory Mathematics
---

Water tanks, gas cylinders, rolling pins, road rollers, footballs, domes and ball bearings are all cylinders and spheres. The surface area tells us how much paint or sheet metal is needed; the volume tells us how much water, gas or metal is inside. This chapter builds the formulas for the **cylinder**, the **hollow cylinder (pipe)**, the **sphere**, the **hemisphere** and the **hollow sphere**, converts volume to litres, and then solves the problems the SEE likes: rollers, melting and recasting, water displaced by a ball, and solids built from more than one piece.

::: key What the SEE asks from this chapter
Expect a 3- or 4-mark question such as: (i) curved surface area, total surface area and volume of a cylinder; (ii) capacity of a tank **in litres**; (iii) volume of metal in a **pipe**; (iv) a **sphere melted** and recast into smaller spheres; (v) a **combined solid** (cylinder with hemispherical ends). Use $\pi=\dfrac{22}{7}$ unless told otherwise, and always write the unit: cm², cm³, m², m³, litres.
:::

## 6.1 Cylinder and Sphere: concepts, formulas and worked problems

### Units of volume and capacity

| Quantity | Relation |
|---|---|
| Length | 1 m $=100$ cm |
| Area | 1 m² $=10{,}000$ cm² |
| Volume | 1 m³ $=10{,}00{,}000$ cm³ |
| Capacity | 1 litre $=1000$ cm³ |
| Capacity | 1 m³ $=1000$ litres |

### The solid cylinder

A **right circular cylinder** has two parallel circular faces of radius $r$ and a curved surface; $h$ is the distance between the circles (the height).

::: derivation Curved surface area of a cylinder
We unroll the curved surface of a cylinder to see its shape, and find its area from the area of that shape.

**Setting up.** A cylinder has radius $r$ and height $h$. Cut the curved surface along a straight line from top to bottom and flatten it.

**Step 1 — the flat shape is a rectangle.** Its height is $h$, the same as the cylinder's.

**Step 2 — its length is the circumference of the base.** The bottom edge of the curved surface was a circle of radius $r$, so after unrolling its length is

$$ 2\pi r $$

**Step 3 — area of the rectangle.**

$$ \text{CSA} = \text{length}\times\text{breadth} = 2\pi r\times h $$

**Result.** $\text{CSA}=2\pi rh$.

**Step 4 — total surface area.** Add the two circular ends, each of area $\pi r^2$:

$$ \text{TSA} = 2\pi rh + 2\pi r^2 = 2\pi r(h+r) $$

**What it means.** The curved surface of a tin is a rectangle wrapped round: its length is the distance round the lid. A label for a tin of radius 7 cm and height 10 cm is a rectangle $44\text{ cm}\times 10\text{ cm}$.
:::

```figure caption="A cylinder opened out. The curved surface unrolls into a rectangle of length 2πr and height h; the two circles are the top and the base."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, Circle
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.6), gridspec_kw={'width_ratios':[1, 1.9]})
r, h = 1.0, 2.2
ax1.add_patch(Rectangle((-r, 0), 2*r, h, fc='#dbeafe', ec='none'))
ax1.add_patch(Ellipse((0, h), 2*r, 0.5, fc='#bfdbfe', ec=INK, lw=1.1))
t = np.linspace(np.pi, 2*np.pi, 60)
ax1.plot(r*np.cos(t), 0.25*np.sin(t), color=INK, lw=1.1)
ax1.plot(r*np.cos(t[::-1]), 0.25*np.sin(t[::-1]), alpha=0)
ax1.plot([-r, -r], [0, h], color=INK, lw=1.1); ax1.plot([r, r], [0, h], color=INK, lw=1.1)
t2 = np.linspace(0, np.pi, 40)
ax1.plot(r*np.cos(t2), 0.25*np.sin(t2), color=MUTED, lw=0.8, ls='--')
ax1.plot([0, r], [h, h], color=ACCENT, lw=1)
ax1.text(0.5, h - 0.08, 'r', color=ACCENT, fontsize=8.5, ha='center', va='top')
ax1.text(r + 0.12, h/2, 'h', fontsize=8.5, va='center')
ax1.set_xlim(-1.5, 1.6); ax1.set_ylim(-0.6, 3.2); ax1.set_aspect('equal'); ax1.axis('off')
ax1.set_title('Cylinder', fontsize=8.5, pad=1)
L = 2*np.pi*r
ax2.add_patch(Rectangle((0, 0), L, h, fc='#dcfce7', ec=INK, lw=1.1))
ax2.text(L/2, h/2, 'curved surface\narea = 2πr × h', ha='center', va='center', fontsize=8.5)
ax2.text(L/2, -0.3, 'length = circumference = 2πr', ha='center', va='top', fontsize=8)
ax2.text(-0.12, h/2, 'h', ha='right', va='center', fontsize=8.5)
ax2.add_patch(Circle((L/2 - 1.3, h + 0.9), 0.55, fc='#bfdbfe', ec=INK, lw=1.0))
ax2.add_patch(Circle((L/2 + 1.3, h + 0.9), 0.55, fc='#bfdbfe', ec=INK, lw=1.0))
ax2.text(L/2, h + 0.9, 'two ends,\neach πr²', ha='center', va='center', fontsize=8)
ax2.set_xlim(-0.6, L + 0.3); ax2.set_ylim(-1.2, h + 1.7); ax2.set_aspect('equal'); ax2.axis('off')
ax2.set_title('Net', fontsize=8.5, pad=1)
fig.tight_layout(pad=0.3)
```

::: key Cylinder formulas
Radius $r$, height $h$:
$$ \text{CSA}=2\pi rh \qquad \text{TSA}=2\pi r(r+h) \qquad V=\pi r^2h $$

- The volume of a cylinder is the base area $\pi r^2$ times the height.
- An **open** cylinder (a bucket, a tank with no lid) has only one circular end: area $=2\pi rh+\pi r^2$.
- Radius $=\dfrac{\text{diameter}}{2}$ — always halve a given diameter.
:::

::: example Surface areas and volume of a cylinder
**Problem.** A solid cylinder has radius 7 cm and height 20 cm. Find its curved surface area, total surface area and volume.

**Solution.** $\text{CSA}=2\pi rh=2\times\dfrac{22}{7}\times 7\times 20=880\text{ cm}^2$.

$\text{TSA}=2\pi r(r+h)=2\times\dfrac{22}{7}\times 7\times(7+20)=44\times 27=1188\text{ cm}^2$.

$V=\pi r^2h=\dfrac{22}{7}\times 7^2\times 20=\dfrac{22}{7}\times 49\times 20=3080\text{ cm}^3$.
:::

::: example Capacity of a tank in litres
**Problem.** A cylindrical water tank has radius 1.4 m and height 5 m. How many litres of water does it hold when full?

**Solution.** $V=\pi r^2h=\dfrac{22}{7}\times 1.4^2\times 5=\dfrac{22}{7}\times 1.96\times 5=30.8\text{ m}^3$.

Since 1 m³ $=1000$ litres, the tank holds $30.8\times 1000=30{,}800$ litres.
:::

::: example Finding the height from the volume
**Problem.** A cylindrical can of radius 7 cm holds 1,540 cm³ of oil. Find the height of the oil.

**Solution.** $V=\pi r^2h$:

$$ 1540=\frac{22}{7}\times 49\times h = 154\,h \;\Rightarrow\; h=\frac{1540}{154}=10\text{ cm} $$
:::

::: example Road roller
**Problem.** A garden roller is a cylinder of radius 0.7 m and length 1.5 m. How much area does it level in 100 revolutions?

**Solution.** In one revolution the roller covers its **curved surface**:

$$ \text{CSA}=2\pi rh=2\times\frac{22}{7}\times 0.7\times 1.5=6.6\text{ m}^2 $$

In 100 revolutions: $100\times 6.6=660\text{ m}^2$.
:::

::: example Capacity of a bucket
**Problem.** A cylindrical bucket has radius 21 cm and height 30 cm. How many litres of water can it hold?

**Solution.** $V=\dfrac{22}{7}\times 21^2\times 30=\dfrac{22}{7}\times 441\times 30=41{,}580\text{ cm}^3$.

Litres $=\dfrac{41580}{1000}=41.58$ litres.
:::

::: caution Common mistakes
- Using the diameter as the radius. A tank "28 cm across" has $r=14$ cm.
- Writing CSA when the question asks for TSA, or adding both circular ends to an open vessel.
- Mixing units: if $r$ is in metres and $h$ in cm, convert first.
- Forgetting to convert m³ or cm³ into litres when the question asks for litres.
:::

### The hollow cylinder (pipe)

A pipe has an outer radius $R$, an inner radius $r$ and length $h$. The **volume of the material** is the volume of the outer solid cylinder minus the volume of the hollow space.

::: key Hollow cylinder
$$ V_{\text{material}}=\pi R^2h-\pi r^2h=\pi h\,(R^2-r^2)=\pi h(R+r)(R-r) $$

- Outer curved surface $=2\pi Rh$; inner curved surface $=2\pi rh$.
- Total surface area (open ends included) $=2\pi h(R+r)+2\pi(R^2-r^2)$.
- Thickness of the pipe $=R-r$.
:::

```figure caption="End view and side view of a pipe. The metal is the ring between the inner radius r and outer radius R, with length h."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Ellipse
fig, (a1, a2) = plt.subplots(1, 2, figsize=(4.6, 2.5), gridspec_kw={'width_ratios':[1, 1.3]})
a1.add_patch(Circle((0, 0), 8, fc='#fde68a', ec=INK, lw=1.2))
a1.add_patch(Circle((0, 0), 6, fc='white', ec=INK, lw=1.2))
a1.annotate('', xy=(8*np.cos(0.8), 8*np.sin(0.8)), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color=INK, lw=0.9))
a1.annotate('', xy=(-6, 0), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color=INK, lw=0.9))
a1.text(5.6, 7.4, 'R = 8', fontsize=8, ha='left', va='center')
a1.text(-3, -0.9, 'r = 6', fontsize=8, ha='center', va='top')
a1.text(0, -10.2, 'end view', fontsize=8, ha='center', va='top')
a1.set_xlim(-9, 13.5); a1.set_ylim(-11.5, 9); a1.set_aspect('equal'); a1.axis('off')
L, R = 4.2, 1.5
a2.add_patch(Rectangle((0, -R), L, 2*R, fc='#fde68a', ec='none'))
a2.add_patch(Rectangle((0, -0.5*R*0.75), L, 1.5*R*0.5, fc='white', ec='none', alpha=0))
a2.plot([0, L], [R, R], color=INK, lw=1.2); a2.plot([0, L], [-R, -R], color=INK, lw=1.2)
a2.add_patch(Ellipse((0, 0), 0.7, 2*R, fc='#fcd34d', ec=INK, lw=1.2))
a2.add_patch(Ellipse((0, 0), 0.5, 1.5, fc='white', ec=INK, lw=1.0))
a2.add_patch(Ellipse((L, 0), 0.7, 2*R, fc='none', ec=INK, lw=1.2))
a2.annotate('', xy=(0, -R - 0.55), xytext=(L, -R - 0.55), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.9))
a2.text(L/2, -R - 0.75, 'h = 21 cm', fontsize=8, ha='center', va='top')
a2.set_xlim(-0.8, L + 0.8); a2.set_ylim(-3.2, 2.2); a2.set_aspect('equal'); a2.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Volume of metal in a pipe
**Problem.** A hollow iron pipe is 21 cm long. Its outer radius is 8 cm and its inner radius is 6 cm. Find the volume of the iron and the outer curved surface area.

**Solution.** $V=\pi h(R^2-r^2)=\dfrac{22}{7}\times 21\times(64-36)=\dfrac{22}{7}\times 21\times 28=1848\text{ cm}^3$.

Outer CSA $=2\pi Rh=2\times\dfrac{22}{7}\times 8\times 21=1056\text{ cm}^2$.
:::

### The sphere and the hemisphere

A **sphere** is the solid round shape of a ball; every point of its surface is the same distance $r$ from the centre. A **hemisphere** is half a sphere, cut by a plane through the centre.

::: key Sphere and hemisphere formulas
Radius $r$:

| Solid | Curved surface area | Total surface area | Volume |
|---|---|---|---|
| Sphere | $4\pi r^2$ | $4\pi r^2$ | $\dfrac43\pi r^3$ |
| Hemisphere | $2\pi r^2$ | $3\pi r^2$ (curved $+$ flat circle $\pi r^2$) | $\dfrac23\pi r^3$ |

A sphere has only a curved surface, so its CSA and TSA are equal. The TSA of a hemisphere includes the flat circular face.
:::

::: example Sphere
**Problem.** Find the surface area and volume of a sphere of radius 21 cm.

**Solution.** $\text{Surface area}=4\pi r^2=4\times\dfrac{22}{7}\times 21^2=4\times\dfrac{22}{7}\times 441=5544\text{ cm}^2$.

$V=\dfrac43\pi r^3=\dfrac43\times\dfrac{22}{7}\times 9261=38{,}808\text{ cm}^3$.
:::

::: example Hemisphere
**Problem.** Find the curved surface area, total surface area and volume of a solid hemisphere of radius 21 cm.

**Solution.** $\text{CSA}=2\pi r^2=2\times\dfrac{22}{7}\times 441=2772\text{ cm}^2$.

$\text{TSA}=3\pi r^2=3\times\dfrac{22}{7}\times 441=4158\text{ cm}^2$.

$V=\dfrac23\pi r^3=\dfrac23\times\dfrac{22}{7}\times 9261=19{,}404\text{ cm}^3$.

Check: this is exactly half the volume of the sphere of the same radius (38,808 ÷ 2) ✓.
:::

::: example Finding the radius from the surface area
**Problem.** The surface area of a sphere is 616 cm². Find its radius and diameter.

**Solution.** $4\pi r^2=616$, so $4\times\dfrac{22}{7}\times r^2=616$.

$$ r^2=\frac{616\times 7}{4\times 22}=49 \;\Rightarrow\; r=7\text{ cm} $$

Diameter $=14$ cm.
:::

::: example Finding the radius from the volume
**Problem.** The volume of a sphere is 4,851 cm³. Find its radius.

**Solution.** $\dfrac43\times\dfrac{22}{7}\,r^3=4851$, so

$$ r^3=\frac{4851\times 21}{88}=1157.625 \;\Rightarrow\; r=10.5\text{ cm} $$

since $10.5\times 10.5\times 10.5=1157.625$.
:::

::: example Painting a dome
**Problem.** A hemispherical dome of a temple has radius 14 m. Find the cost of painting its outer surface at Rs 25 per m².

**Solution.** The outer surface of the dome is the curved surface of a hemisphere:

$$ \text{CSA}=2\pi r^2=2\times\frac{22}{7}\times 196=1232\text{ m}^2 $$

Cost $=1232\times 25=\text{Rs } 30{,}800$.
:::

### The hollow sphere

::: key Hollow sphere (spherical shell)
With outer radius $R$ and inner radius $r$:

$$ V_{\text{material}}=\frac43\pi\left(R^3-r^3\right) $$
:::

::: example Hollow sphere
**Problem.** A metal ball is hollow with outer radius 6 cm and inner radius 3 cm. Find the volume of the metal.

**Solution.** $V=\dfrac43\times\dfrac{22}{7}\times(6^3-3^3)=\dfrac43\times\dfrac{22}{7}\times(216-27)=\dfrac43\times\dfrac{22}{7}\times 189=792\text{ cm}^3$.
:::

### Recasting and displacement

When a solid is **melted** and recast into other solids, no metal is lost, so the **total volume stays the same**. When a solid is **fully immersed** in water, it pushes aside a volume of water equal to its own volume.

::: example Melting a sphere into small spheres
**Problem.** A metal sphere of radius 6 cm is melted and recast into small spheres of radius 1.5 cm. How many small spheres are made?

**Solution.** Number $=\dfrac{\text{volume of big sphere}}{\text{volume of one small sphere}}=\dfrac{\frac43\pi(6)^3}{\frac43\pi(1.5)^3}=\left(\dfrac{6}{1.5}\right)^3=4^3=64$.

**64 small spheres** are made.
:::

::: example Cylinder recast into spheres
**Problem.** A solid metal cylinder of radius 4 cm and height 18 cm is melted and made into spheres of radius 3 cm. How many spheres are made?

**Solution.** Volume of cylinder $=\pi\times 4^2\times 18=288\pi$ cm³.

Volume of one sphere $=\dfrac43\pi\times 3^3=36\pi$ cm³.

Number of spheres $=\dfrac{288\pi}{36\pi}=8$.
:::

```figure caption="A steel ball of radius 3 cm is dropped into a cylindrical jar of radius 6 cm. The water rises until the extra volume equals the volume of the ball."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, (a1, a2) = plt.subplots(1, 2, figsize=(4.6, 2.9))
def jar(ax, level, ball, title):
    ax.add_patch(Rectangle((-6, 0), 12, level, fc='#bfdbfe', ec='none'))
    ax.plot([-6, -6, 6, 6], [14, 0, 0, 14], color=INK, lw=1.3)
    ax.plot([-6, 6], [level, level], color=ACCENT, lw=1.2)
    if ball:
        ax.add_patch(Circle((0, 3), 3, fc='#9ca3af', ec=INK, lw=1.1))
    ax.set_title(title, fontsize=8.5, pad=2)
    ax.set_xlim(-9, 11); ax.set_ylim(-1, 15); ax.set_aspect('equal'); ax.axis('off')
jar(a1, 8, False, 'before')
jar(a2, 9, True, 'after')
a2.annotate('', xy=(8, 9), xytext=(8, 8), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.9))
a2.plot([6, 8.2], [8, 8], color=MUTED, lw=0.7, ls=':')
a2.text(8.5, 8.5, 'rise\n1 cm', fontsize=8, va='center', ha='left')
fig.tight_layout(pad=0.3)
```

::: example Water displaced by a ball
**Problem.** A cylindrical jar of radius 6 cm contains water. A steel ball of radius 3 cm is dropped in and sinks completely. By how much does the water level rise?

**Solution.** Volume of ball $=\dfrac43\pi\times 3^3=36\pi$ cm³. This equals the volume of the extra water layer of height $x$ in the jar:

$$ \pi\times 6^2\times x=36\pi \;\Rightarrow\; 36x=36 \;\Rightarrow\; x=1\text{ cm} $$

The level rises by **1 cm**.
:::

### Combined solids

Split the solid into cylinders, hemispheres and so on. Remember: for the **surface area** of a combined solid, do not count the faces where the parts join, because they are inside.

```figure caption="A gas tank: a cylinder of length 4 m with a hemisphere on each end, radius 2.1 m. The two joining circles are inside the solid."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Wedge
fig, ax = plt.subplots(figsize=(4.8, 2.3))
r, L = 2.1, 4.0
ax.add_patch(Rectangle((0, -r), L, 2*r, fc='#dbeafe', ec='none'))
ax.add_patch(Wedge((0, 0), r, 90, 270, fc='#fde68a', ec='none'))
ax.add_patch(Wedge((L, 0), r, -90, 90, fc='#fde68a', ec='none'))
ax.plot([0, L], [r, r], color=INK, lw=1.2); ax.plot([0, L], [-r, -r], color=INK, lw=1.2)
t = np.linspace(np.pi/2, 3*np.pi/2, 60); ax.plot(r*np.cos(t), r*np.sin(t), color=INK, lw=1.2)
t = np.linspace(-np.pi/2, np.pi/2, 60); ax.plot(L + r*np.cos(t), r*np.sin(t), color=INK, lw=1.2)
ax.plot([0, 0], [-r, r], color=MUTED, lw=0.8, ls='--'); ax.plot([L, L], [-r, r], color=MUTED, lw=0.8, ls='--')
ax.annotate('', xy=(0, -r - 0.5), xytext=(L, -r - 0.5), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.9))
ax.text(L/2, -r - 0.7, 'cylindrical part 4 m', fontsize=8, ha='center', va='top')
ax.text(L/2, 0, 'cylinder', fontsize=8.5, ha='center', va='center')
ax.text(-0.9, 0, 'hemi-\nsphere', fontsize=7.5, ha='center', va='center')
ax.text(L + 0.9, 0, 'hemi-\nsphere', fontsize=7.5, ha='center', va='center')
ax.annotate('', xy=(L + r, 0.0), xytext=(L, 0.0), arrowprops=dict(arrowstyle='-', color=ACCENT, lw=0))
ax.set_xlim(-3, L + 3); ax.set_ylim(-3.7, 2.8); ax.set_aspect('equal'); ax.axis('off')
```

::: example Cylinder with hemispherical ends
**Problem.** A gas tank is a cylinder of length 4 m with a hemisphere of radius 2.1 m fixed on each end. Find its total volume and its total surface area.

**Solution.** Radius $r=2.1$ m, cylindrical length $h=4$ m. The two hemispheres together make one full sphere of radius 2.1 m.

Volume of cylinder $=\pi r^2h=\dfrac{22}{7}\times 2.1^2\times 4=55.44\text{ m}^3$.

Volume of the two hemispheres $=\dfrac43\pi r^3=\dfrac43\times\dfrac{22}{7}\times 2.1^3=38.808\text{ m}^3$.

Total volume $=55.44+38.808=94.248\text{ m}^3$ (that is 94,248 litres).

Surface area $=$ CSA of cylinder $+$ surface of the sphere:

$$ 2\pi rh+4\pi r^2=2\times\frac{22}{7}\times 2.1\times 4+4\times\frac{22}{7}\times 2.1^2=52.8+55.44=108.24\text{ m}^2 $$
:::

::: tip The shape of every solid problem
1. Draw the solid; label $r$, $h$ and which units are used.
2. Decide: **surface** (paint, cloth, sheet, label) or **volume** (water, metal, gas).
3. If melted/recast: volume before $=$ volume after.
4. If fully submerged: rise in water $=\dfrac{\text{volume of solid}}{\text{base area of vessel}}$.
5. Convert to litres only at the end.
:::

## 6.2 Exercises of the SEE type

### Method for any question

1. Halve a diameter to get the radius; put all lengths in one unit.
2. Write the formula, then substitute with $\pi=\frac{22}{7}$ (cancel the 7 with the radius where you can).
3. For "how many" (melting, filling): divide the volume of the big solid by the volume of one small one.
4. For a combined solid: add volumes; for the surface, drop the joining faces.
5. Answer in a sentence with units; litres only if asked.

## Chapter summary

- Cylinder: CSA $=2\pi rh$, TSA $=2\pi r(r+h)$, $V=\pi r^2h$.
- Hollow cylinder: $V=\pi h(R^2-r^2)$; outer CSA $=2\pi Rh$.
- Sphere: surface $=4\pi r^2$, $V=\frac43\pi r^3$.
- Hemisphere: CSA $=2\pi r^2$, TSA $=3\pi r^2$, $V=\frac23\pi r^3$.
- Hollow sphere: $V=\frac43\pi(R^3-r^3)$.
- 1 litre $=1000$ cm³; 1 m³ $=1000$ litres.
- Melting and recasting: total volume is unchanged; number of small solids $=\frac{V_{\text{big}}}{V_{\text{small}}}$.
- A submerged solid raises the water level by $\frac{V_{\text{solid}}}{\text{base area}}$.
- Combined solids: add volumes; omit the joining faces from the surface area.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The curved surface area of a cylinder of radius $r$ and height $h$ is <span class="marks">[1]</span>
   (a) $\pi r^2h$ (b) $2\pi rh$ (c) $2\pi r(r+h)$ (d) $4\pi r^2$
2. The volume of a sphere of radius $r$ is <span class="marks">[1]</span>
   (a) $\frac43\pi r^2$ (b) $4\pi r^2$ (c) $\frac43\pi r^3$ (d) $\frac23\pi r^3$
3. The total surface area of a solid hemisphere of radius $r$ is <span class="marks">[1]</span>
   (a) $2\pi r^2$ (b) $3\pi r^2$ (c) $4\pi r^2$ (d) $\pi r^2$
4. How many litres are in 1 m³? <span class="marks">[1]</span>
   (a) 10 (b) 100 (c) 1,000 (d) 10,000
5. If the radius of a sphere is doubled, its surface area becomes <span class="marks">[1]</span>
   (a) 2 times (b) 4 times (c) 6 times (d) 8 times

::: note Answers to Group A
**1.** (b) — the unrolled rectangle is $2\pi r\times h$.
**2.** (c) — $\frac43\pi r^3$.
**3.** (b) — curved $2\pi r^2$ plus the flat circle $\pi r^2$.
**4.** (c) — 1 m³ $=1000$ litres.
**5.** (b) — surface area $\propto r^2$, so $2^2=4$ times.
:::

**Group B — Short answer (2 marks each)**

1. Find the curved surface area of a cylinder of radius 7 cm and height 10 cm. <span class="marks">[2]</span>
2. Find the volume of a cylinder of radius 7 cm and height 15 cm. <span class="marks">[2]</span>
3. Find the surface area of a sphere of radius 14 cm. <span class="marks">[2]</span>
4. Find the volume of a hemisphere of radius 10.5 cm. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $2\times\frac{22}{7}\times 7\times 10=440\text{ cm}^2$.
**2.** $\frac{22}{7}\times 49\times 15=2310\text{ cm}^3$.
**3.** $4\times\frac{22}{7}\times 196=2464\text{ cm}^2$.
**4.** $\frac23\times\frac{22}{7}\times 10.5^3=\frac23\times\frac{22}{7}\times 1157.625=2425.5\text{ cm}^3$.
:::

**Group C — Short answer (3 marks each)**

1. A cylinder has volume 3,465 cm³ and radius 10.5 cm. Find its height and its curved surface area. <span class="marks">[3]</span>
2. A roller of radius 0.35 m and length 1.4 m makes 500 revolutions. Find the area it levels. <span class="marks">[3]</span>
3. The surface area of a sphere is 1,386 cm². Find its radius and volume. <span class="marks">[3]</span>
4. A metal sphere of radius 6 cm is melted and recast into small spheres of radius 2 cm. How many small spheres are formed? <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $\frac{22}{7}\times 10.5^2\times h=3465$, so $346.5h=3465$ and $h=10$ cm. CSA $=2\times\frac{22}{7}\times 10.5\times 10=660\text{ cm}^2$.
**2.** CSA per revolution $=2\times\frac{22}{7}\times 0.35\times 1.4=3.08\text{ m}^2$. For 500 revolutions $=3.08\times 500=1540\text{ m}^2$.
**3.** $4\times\frac{22}{7}r^2=1386\Rightarrow r^2=\frac{1386\times 7}{88}=110.25\Rightarrow r=10.5$ cm. $V=\frac43\times\frac{22}{7}\times 10.5^3=4851\text{ cm}^3$.
**4.** Number $=\left(\frac{6}{2}\right)^3=27$.
:::

**Group D — Long answer (4 marks each)**

1. A hollow metal pipe is 14 cm long, with outer radius 7 cm and inner radius 5 cm. Find the volume of the metal, and its mass if 1 cm³ of the metal has mass 8 g. <span class="marks">[4]</span>
2. A cylindrical jar of radius 6 cm contains water. A steel ball of radius 3 cm is dropped in and sinks completely. Find the rise in water level. <span class="marks">[4]</span>
3. A hemispherical dome has radius 14 m. Find the cost of painting its outside at Rs 25 per m². Also find the total surface area of a solid hemisphere of the same radius. <span class="marks">[4]</span>
4. A gas tank is a cylinder 4 m long with a hemisphere of radius 2.1 m on each end. Find its volume (in litres) and its surface area. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** $V=\frac{22}{7}\times 14\times(7^2-5^2)=\frac{22}{7}\times 14\times 24=1056\text{ cm}^3$. Mass $=1056\times 8=8448\text{ g}=8.448\text{ kg}$.
**2.** Volume of ball $=\frac43\pi\times 27=36\pi\text{ cm}^3$. Let the rise be $x$: $\pi\times 36\times x=36\pi$, so $x=1$ cm.
**3.** CSA $=2\times\frac{22}{7}\times 196=1232\text{ m}^2$; cost $=1232\times 25=\text{Rs } 30{,}800$. TSA of solid hemisphere $=3\pi r^2=3\times\frac{22}{7}\times 196=1848\text{ m}^2$.
**4.** Volume $=\frac{22}{7}\times 2.1^2\times 4+\frac43\times\frac{22}{7}\times 2.1^3=55.44+38.808=94.248\text{ m}^3=94{,}248$ litres. Surface area $=2\pi rh+4\pi r^2=52.8+55.44=108.24\text{ m}^2$.
:::
