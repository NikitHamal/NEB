---
subject: Physics
grade: 11
unit: 6
title: Circular Motion
hours: 6
area: Mechanics
---

A bus rounding a bend on the Prithvi Highway, a stone whirled on a string, the
Moon going round the Earth and an electron in a magnetic field are all doing the
same thing: moving on a curved path at a speed that may not change at all, yet
accelerating every instant. This unit explains that apparent contradiction,
builds the language of angular quantities, and applies it to three standard
systems — the conical pendulum, the vertical circle and the banked road.

::: key The one idea behind the whole unit
Velocity is a **vector**. A body going round a circle at constant speed is
changing the *direction* of its velocity all the time, so it is accelerating.
That acceleration points to the centre, and something real must supply the force
that causes it.
:::

## 6.1 Angular displacement, velocity and acceleration

For a particle moving on a circle of radius $r$, it is easier to describe the
position by the angle $\theta$ swept out at the centre than by the arc length.

::: definition Angular displacement
The **angular displacement** $\theta$ is the angle turned through by the radius
joining the particle to the centre. It is measured in **radians**:

$$ \theta = \frac{\text{arc length}}{\text{radius}} = \frac{s}{r} $$

One complete revolution is $2\pi\ \text{rad} = 360^{\circ}$, so
$1\ \text{rad} = 57.3^{\circ}$. The radian is dimensionless.
:::

```figure caption="Angular displacement $\theta = s/r$. The direction of $\vec{\omega}$ is given by the right-hand rule, along the axis of rotation."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,2.9))
th = np.linspace(0,2*np.pi,400)
ax.plot(np.cos(th), np.sin(th), color=GRID, lw=1.4)
a0, a1 = np.radians(12), np.radians(72)
arc = np.linspace(a0,a1,120)
ax.plot(np.cos(arc), np.sin(arc), color=ACCENT, lw=2.6)
for a,lab,off in [(a0,'A',(6,-6)),(a1,'B',(4,6))]:
    ax.plot([0,np.cos(a)],[0,np.sin(a)], color=INK, lw=1.1)
    ax.plot([np.cos(a)],[np.sin(a)],'o',color=INK,ms=4.5)
    ax.annotate(lab,(np.cos(a),np.sin(a)),textcoords='offset points',
                xytext=off,color=INK,fontsize=10)
sm = np.linspace(a0,a1,60)*0.0 + 0
ax.plot(0.3*np.cos(np.linspace(a0,a1,60)), 0.3*np.sin(np.linspace(a0,a1,60)),
        color='#d9534f', lw=1.3)
ax.annotate(r'$\theta$',(0.40*np.cos((a0+a1)/2),0.40*np.sin((a0+a1)/2)),
            color='#d9534f',fontsize=11,ha='center',va='center')
ax.annotate('$r$',(0.55*np.cos(a0),0.55*np.sin(a0)),textcoords='offset points',
            xytext=(0,-13),color=INK,fontsize=10)
ax.annotate('arc $s$',(np.cos((a0+a1)/2),np.sin((a0+a1)/2)),
            textcoords='offset points',xytext=(10,6),color=ACCENT,fontsize=9.5)
ax.plot([0],[0],'o',color=INK,ms=4)
ax.annotate('O',(0,0),textcoords='offset points',xytext=(-11,-5),color=INK,fontsize=9.5)
tangent = np.array([-np.sin(a1), np.cos(a1)])*0.62
ax.annotate('', xy=(np.cos(a1)+tangent[0], np.sin(a1)+tangent[1]),
            xytext=(np.cos(a1),np.sin(a1)),
            arrowprops=dict(arrowstyle='-|>',color='#2e8b57',lw=1.6,mutation_scale=12))
ax.annotate(r'$\vec{v}$',(np.cos(a1)+tangent[0],np.sin(a1)+tangent[1]),
            textcoords='offset points',xytext=(-2,6),color='#2e8b57',fontsize=10)
ax.set_xlim(-1.25,1.55); ax.set_ylim(-1.25,1.35)
ax.set_aspect('equal'); ax.axis('off')
```

**Angular velocity** $\omega$ is the rate of change of angular displacement, and
**angular acceleration** $\alpha$ the rate of change of $\omega$:

$$ \omega_{av} = \frac{\Delta\theta}{\Delta t}, \quad \omega = \frac{d\theta}{dt};
\qquad \alpha_{av} = \frac{\Delta\omega}{\Delta t}, \quad \alpha = \frac{d\omega}{dt} = \frac{d^{2}\theta}{dt^{2}} $$

Both are vectors directed along the axis of rotation, their sense given by the
right-hand rule. For one revolution in a time $T$ (the **period**), with
frequency $f = 1/T$,

$$ \omega = \frac{2\pi}{T} = 2\pi f $$

Because the equations $\theta = \omega t$ and so on have exactly the same form as
the linear ones, the kinematic equations carry over term by term:

| Linear motion | Angular motion |
|---|---|
| $v = u + at$ | $\omega = \omega_0 + \alpha t$ |
| $s = ut + \frac{1}{2}at^{2}$ | $\theta = \omega_0 t + \frac{1}{2}\alpha t^{2}$ |
| $v^{2} = u^{2} + 2as$ | $\omega^{2} = \omega_0^{2} + 2\alpha\theta$ |
| units m, m s⁻¹, m s⁻² | units rad, rad s⁻¹, rad s⁻² |

::: caution Always convert rpm to rad s⁻¹
A speed quoted in revolutions per minute must be multiplied by $2\pi/60$ before
it goes into any formula. $300\ \text{rpm} = 300 \times 2\pi/60 = 10\pi
\approx 31.4\ \text{rad s}^{-1}$, not $300\ \text{rad s}^{-1}$.
:::

## 6.2 Relation between angular and linear velocity and acceleration

::: derivation The relations $v = r\omega$ and $a_t = r\alpha$
We start from the definition of angle in radians and reach the two formulas that
connect the *linear* quantities of a point on a wheel to the *angular* quantities of
the wheel itself.

**Step 1 — the definition of the radian.** If a point moves a distance $s$ along a
circle of radius $r$, the angle turned in radians is $\theta = s/r$. Multiply both
sides by $r$:

$$ s = r\theta $$

**Step 2 — differentiate both sides with respect to time.** The radius $r$ is a fixed
number for a given circle, so it is a constant multiplier and stays outside the
derivative:

$$ \frac{ds}{dt} = r\,\frac{d\theta}{dt} $$

**Step 3 — name the two derivatives.** $ds/dt$ is the linear speed $v$ along the
circle, and $d\theta/dt$ is the angular velocity $\omega$:

$$ v = r\omega $$

**Step 4 — differentiate once more with respect to time.** Same reasoning: $r$ stays
outside:

$$ \frac{dv}{dt} = r\,\frac{d\omega}{dt} $$

**Step 5 — name these derivatives.** $dv/dt$ is the rate at which the *speed* changes
— the **tangential** acceleration $a_t$ — and $d\omega/dt$ is the angular
acceleration $\alpha$:

$$ a_t = r\alpha $$

**Result.**

$$ v = r\omega, \qquad a_t = r\alpha $$

In vector form $\vec{v} = \vec{\omega}\times\vec{r}$ and
$\vec{a}_t = \vec{\alpha}\times\vec{r}$.

**What it means.** Every point on a rigid rotating body shares the same $\omega$ and
$\alpha$, but a point twice as far from the axis moves twice as fast and gains speed
twice as quickly.

**Conditions used.** $\theta$ must be in **radians** — in degrees, $s = r\theta$ is
simply false. The radius $r$ must be constant (the body is rigid, the point does not
spiral in or out). Also, $a_t$ is only the part of the acceleration along the
tangent; there is always a second, radial part as well, which the next section
works out.
:::

::: tip All points of a rigid body share $\omega$, not $v$
On a rotating wheel every point has the same $\omega$ and $\alpha$, but $v = r\omega$
means the rim moves faster than a point near the hub. This is why the outer
gear-teeth of a bicycle wheel travel further per turn than the inner ones.
:::

::: example Worked example 6.1
**Problem.** A flywheel of radius $0.40\ \text{m}$ rotates at $300\ \text{rpm}$.
It is then brought uniformly to rest in $10\ \text{s}$. Find (a) the initial
angular velocity, (b) the linear speed of a point on the rim, (c) the angular
retardation, and (d) the number of revolutions made before stopping.

**Solution.**

(a) $\omega_0 = \dfrac{2\pi N}{60} = \dfrac{2\pi \times 300}{60} = 10\pi = 31.4\ \text{rad s}^{-1}$

(b) $v = r\omega_0 = 0.40 \times 31.4 = 12.6\ \text{m s}^{-1}$

(c) $\alpha = \dfrac{\omega - \omega_0}{t} = \dfrac{0 - 31.4}{10} = -3.14\ \text{rad s}^{-2}$

(d) $\theta = \dfrac{\omega_0 + \omega}{2}t = \dfrac{31.4}{2}\times 10 = 157\ \text{rad}$,
so the number of revolutions is $\dfrac{157}{2\pi} = 25$.
:::

## 6.3 Centripetal acceleration

::: derivation Centripetal acceleration $a = v^{2}/r$
We start from the fact that a body going round a circle at constant speed keeps
changing the *direction* of its velocity, and we reach a formula for how big the
resulting acceleration is and where it points.

**Setting up.** A particle moves on a circle of radius $r$ at constant speed $v$. In a
short time $\Delta t$ it travels from point A to point B, and the radius to it turns
through a small angle $\Delta\theta$.

**Step 1 — the angle turned.** By the definition of angular velocity,
$\omega = \Delta\theta/\Delta t$, so

$$ \Delta\theta = \omega\,\Delta t $$

**Step 2 — the velocity turns through the same angle.** The velocity is always along
the tangent, and the tangent turns exactly as fast as the radius does. So
$\vec{v}_A$ and $\vec{v}_B$ have the **same length** $v$ but differ in direction by
$\Delta\theta$.

**Step 3 — find the change in velocity.** Redraw $\vec{v}_A$ and $\vec{v}_B$ from one
common point (right-hand figure). The change is the vector from the tip of
$\vec{v}_A$ to the tip of $\vec{v}_B$:

$$ \Delta\vec{v} = \vec{v}_B - \vec{v}_A $$

**Step 4 — measure its length.** The two vectors and $\Delta\vec{v}$ form an isosceles
triangle: two equal sides of length $v$ with $\Delta\theta$ between them. Splitting
that triangle down the middle gives two right-angled triangles, each with angle
$\Delta\theta/2$ and hypotenuse $v$, so half the base is $v\sin(\Delta\theta/2)$ and
the whole base is twice that:

$$ |\Delta\vec{v}| = 2v\sin\frac{\Delta\theta}{2} $$

**Step 5 — use the small-angle approximation.** When an angle in radians is very
small, $\sin x \approx x$ (try $x = 0.01$: $\sin x = 0.0099998$). Since we are about to
let $\Delta t \to 0$, the angle is as small as we like:

$$ |\Delta\vec{v}| \approx 2v\cdot\frac{\Delta\theta}{2} = v\,\Delta\theta $$

**Step 6 — divide by the time taken.** Acceleration is change of velocity divided by
time:

$$ a = \frac{|\Delta\vec{v}|}{\Delta t} = \frac{v\,\Delta\theta}{\Delta t} $$

**Step 7 — take the limit as $\Delta t \to 0$** so that the answer is the
instantaneous acceleration. The constant $v$ comes outside the limit:

$$ a = v\lim_{\Delta t \to 0}\frac{\Delta\theta}{\Delta t} $$

**Step 8 — recognise the limit as $\omega$:**

$$ a = v\omega $$

**Step 9 — get the first standard form.** Substitute $\omega = v/r$ (from
$v = r\omega$):

$$ a = v\cdot\frac{v}{r} = \frac{v^{2}}{r} $$

**Step 10 — get the second standard form.** Instead substitute $v = r\omega$ into
$a = v\omega$:

$$ a = (r\omega)\omega = r\omega^{2} $$

**Step 11 — get the third form in terms of the period.** Since $\omega = 2\pi/T$:

$$ a = r\left(\frac{2\pi}{T}\right)^{2} = \frac{4\pi^{2}r}{T^{2}} $$

**Step 12 — the direction.** In Step 4's isosceles triangle, the two base angles are
each $(180^{\circ} - \Delta\theta)/2$. As $\Delta\theta \to 0$ each base angle
approaches $90^{\circ}$ — so $\Delta\vec{v}$ becomes **perpendicular** to the velocity,
pointing inwards along the radius, i.e. **towards the centre**.

**Result.**

$$ a = \frac{v^{2}}{r} = r\omega^{2} = \frac{4\pi^{2}r}{T^{2}},
\quad \text{directed towards the centre} $$

That inward direction is why it is called the **centripetal** ("centre-seeking")
acceleration.

**What it means.** A body can accelerate without speeding up. Here the *size* of the
velocity never changes, only its direction — and changing direction is itself an
acceleration, which needs a force pointing at the centre.

**Conditions used.** The speed $v$ is constant (uniform circular motion) and the
radius $r$ is constant. Step 5 needs the angle in **radians**. If the speed also
changes there is an extra tangential part $a_t = r\alpha$, and the total acceleration
is $\sqrt{a_c^{2} + a_t^{2}}$.
:::

::: tip The examiner is looking for
(i) Two diagrams — the circle with $\vec{v}_A$, $\vec{v}_B$ and $\Delta\theta$, and the
vector triangle; (ii) the statement that the *magnitudes* are equal but the
directions differ by $\Delta\theta$; (iii) $|\Delta v| = 2v\sin(\Delta\theta/2)$;
(iv) the small-angle step, said out loud; (v) the limit, giving $a = v\omega$;
(vi) all three final forms and, crucially, the sentence "directed towards the
centre".
:::

```figure caption="Left: velocities at A and B, each of magnitude $v$, turned through $\Delta\theta$. Right: the vector triangle gives $|\Delta\vec{v}| = 2v\sin(\Delta\theta/2)$, directed towards the centre as $\Delta\theta \to 0$."
import numpy as np, matplotlib.pyplot as plt
fig, (a1,a2) = plt.subplots(1,2, figsize=(5.2,2.6))
th = np.linspace(0,2*np.pi,400)
a1.plot(np.cos(th),np.sin(th),color=GRID,lw=1.3)
A,B = np.radians(55), np.radians(115)
for a,lab,off in [(A,'A',(8,-2)),(B,'B',(-14,2))]:
    a1.plot([0,np.cos(a)],[0,np.sin(a)],color=INK,lw=1.0)
    a1.plot([np.cos(a)],[np.sin(a)],'o',color=INK,ms=4)
    a1.annotate(lab,(np.cos(a),np.sin(a)),textcoords='offset points',xytext=off,
                color=INK,fontsize=10)
    t = np.array([-np.sin(a),np.cos(a)])*0.75
    a1.annotate('',xy=(np.cos(a)+t[0],np.sin(a)+t[1]),xytext=(np.cos(a),np.sin(a)),
                arrowprops=dict(arrowstyle='-|>',color=ACCENT,lw=1.6,mutation_scale=12))
a1.plot(0.42*np.cos(np.linspace(A,B,50)),0.42*np.sin(np.linspace(A,B,50)),
        color='#d9534f',lw=1.2)
# angle label on the bisector, well outside the arc and clear of both radii
a1.annotate(r'$\Delta\theta$',(0.72*np.cos(np.radians(85)),0.72*np.sin(np.radians(85))),
            ha='center',va='center',color='#d9534f',fontsize=10)
a1.annotate(r'$\vec{v}_A$',(np.cos(A)-0.55,np.sin(A)+0.70),color=ACCENT,fontsize=10)
a1.annotate(r'$\vec{v}_B$',(-1.42,0.98),ha='center',va='center',color=ACCENT,fontsize=10)
a1.set_xlim(-2.0,1.6); a1.set_ylim(-1.2,2.0); a1.set_aspect('equal'); a1.axis('off')
vA = np.array([np.cos(np.radians(55+90)),np.sin(np.radians(55+90))])
vB = np.array([np.cos(np.radians(115+90)),np.sin(np.radians(115+90))])
O = np.array([0,0])
for vec,lab,c,off in [(vA,r'$\vec{v}_A$',ACCENT,(8,4)),(vB,r'$\vec{v}_B$',ACCENT,(-6,-16))]:
    a2.annotate('',xy=vec,xytext=O,
                arrowprops=dict(arrowstyle='-|>',color=c,lw=1.7,mutation_scale=12))
    a2.annotate(lab,vec/2,textcoords='offset points',xytext=off,color=c,fontsize=10)
a2.annotate('',xy=vB,xytext=vA,
            arrowprops=dict(arrowstyle='-|>',color='#d9534f',lw=1.8,mutation_scale=12))
a2.annotate(r'$\Delta\vec{v}$',(vA+vB)/2,textcoords='offset points',xytext=(-36,0),
            color='#d9534f',fontsize=10)
a2.plot(0.34*np.cos(np.linspace(np.radians(145),np.radians(205),40)),
        0.34*np.sin(np.linspace(np.radians(145),np.radians(205),40)),color=MUTED,lw=1.1)
a2.annotate(r'$\Delta\theta$',(0.60*np.cos(np.radians(175)),0.60*np.sin(np.radians(175))),
            ha='center',va='center',color=MUTED,fontsize=10)
a2.set_xlim(-1.75,1.05); a2.set_ylim(-1.35,0.95); a2.set_aspect('equal'); a2.axis('off')
fig.tight_layout()
```
If the speed also changes, the total acceleration has two perpendicular parts:

$$ a = \sqrt{a_c^{2} + a_t^{2}} = \sqrt{\left(\frac{v^{2}}{r}\right)^{2} + (r\alpha)^{2}} $$

In **uniform** circular motion $a_t = 0$, so the acceleration is purely radial.

## 6.4 Centripetal force

By Newton's second law an acceleration needs a force. The force required to keep
a body of mass $m$ moving on a circle of radius $r$ at speed $v$ is

$$ F_c = ma_c = \frac{mv^{2}}{r} = mr\omega^{2} = \frac{4\pi^{2}mr}{T^{2}} $$

::: key Centripetal force is a role, not a new force
No new force of nature is involved. Some *existing* force plays the part of the
centripetal force in each situation, and it always points to the centre.
:::

| Motion | Force acting as the centripetal force |
|---|---|
| Stone whirled on a string | tension in the string |
| Car on a level curve | friction between tyres and road |
| Car on a banked curve | horizontal component of the normal reaction |
| Moon round the Earth | gravitational attraction |
| Electron round a nucleus (Bohr model) | electrostatic attraction |

::: caution Centrifugal force is not real
The outward "centrifugal force" a passenger feels on a bend is not a force at
all; it is the passenger's inertia trying to continue in a straight line. It
appears only in the rotating (non-inertial) frame. In an NEB answer, always
resolve forces in the ground frame and put $mv^2/r$ on the *acceleration* side.
:::

::: example Worked example 6.2
**Problem.** A car of mass $1000\ \text{kg}$ takes an unbanked curve of radius
$50\ \text{m}$ at $10\ \text{m s}^{-1}$. Find the centripetal force needed and the
minimum coefficient of friction required. Take $g = 10\ \text{m s}^{-2}$.

**Solution.**

$$ F_c = \frac{mv^{2}}{r} = \frac{1000 \times 100}{50} = 2000\ \text{N} $$

Friction must supply this: $\mu mg \geq \dfrac{mv^{2}}{r}$, so

$$ \mu \geq \frac{v^{2}}{rg} = \frac{100}{50 \times 10} = 0.20 $$

A wet road can drop below $\mu = 0.2$, which is why vehicles skid outwards on
monsoon bends.
:::

## 6.5 Conical pendulum

A conical pendulum is a bob on a string that moves in a **horizontal** circle
while the string sweeps out a cone of semi-vertical angle $\theta$.

```figure caption="Conical pendulum. The vertical component $T\cos\theta$ balances the weight; the horizontal component $T\sin\theta$ provides the centripetal force $mv^2/r$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.4,3.3))
S = np.array([0,3.0]); B = np.array([1.55,0.55])
ax.plot([-1.1,1.1],[3.0,3.0],color=INK,lw=1.8)
for x in np.arange(-1.0,1.05,0.28):
    ax.plot([x,x-0.16],[3.0,3.22],color=MUTED,lw=0.8)
ax.plot([S[0],B[0]],[S[1],B[1]],color=INK,lw=1.3)
ax.plot([S[0],-B[0]],[S[1],B[1]],color=MUTED,lw=0.9,ls=':')
ax.plot([S[0],S[0]],[S[1],B[1]],color=MUTED,lw=0.9,ls='--')
# radius drawn on the far side of the axis so it cannot lie under the T sin(theta) arrow
ax.plot([-B[0],0.0],[B[1],B[1]],color=MUTED,lw=0.9,ls='--')
t = np.linspace(0,2*np.pi,200)
ax.plot(B[0]*np.cos(t), B[1]+0.26*np.sin(t), color=GRID, lw=1.2)
ax.add_patch(Circle(B,0.15,fc=ACCENT,ec=INK,lw=1.0))
phi = np.arctan2(B[0], S[1]-B[1])
ang = np.linspace(-np.pi/2, -np.pi/2+phi, 40)
ax.plot(S[0]+0.55*np.cos(ang), S[1]+0.55*np.sin(ang), color='#d9534f', lw=1.2)
am = -np.pi/2 + phi/2
ax.annotate(r'$\theta$',(S[0]+0.85*np.cos(am), S[1]+0.85*np.sin(am)),
            ha='center',va='center',color='#d9534f',fontsize=11)
ax.annotate('$L$',(0.80,1.95),color=INK,fontsize=10)
ax.annotate('$r$',(-0.78,B[1]),ha='center',va='center',color=MUTED,fontsize=10,
            bbox=dict(fc='white', ec='none', pad=1.5))
ax.annotate('$h$',(0.0,1.8),textcoords='offset points',xytext=(-19,0),color=MUTED,fontsize=10)
ax.annotate('',xy=(B[0]-0.50,B[1]+0.79),xytext=B,
            arrowprops=dict(arrowstyle='-|>',color='#2e8b57',lw=1.8,mutation_scale=13))
ax.annotate('$T$',(0.92,1.00),ha='center',va='center',color='#2e8b57',fontsize=10)
ax.annotate('',xy=(B[0],B[1]-0.75),xytext=B,
            arrowprops=dict(arrowstyle='-|>',color='#d9534f',lw=1.8,mutation_scale=13))
ax.annotate('$mg$',(B[0]+0.16,B[1]-0.55),color='#d9534f',fontsize=10)
ax.annotate('',xy=(B[0],B[1]+0.79),xytext=B,
            arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.1,mutation_scale=10,linestyle=(0,(3,2))))
ax.annotate(r'$T\cos\theta$',(B[0]+0.16,B[1]+0.63),ha='left',va='center',color=MUTED,fontsize=9)
ax.annotate('',xy=(B[0]-0.50,B[1]),xytext=B,
            arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.1,mutation_scale=10,linestyle=(0,(3,2))))
ax.annotate(r'$T\sin\theta$',(0.93,B[1]),ha='right',va='center',color=MUTED,fontsize=9)
ax.set_xlim(-1.9,2.7); ax.set_ylim(-0.6,3.5); ax.set_aspect('equal'); ax.axis('off')
```
::: derivation Period of a conical pendulum
We start from the two force equations for the bob — one vertical, one horizontal —
and reach an expression for the time of one revolution.

**Setting up.** A bob of mass $m$ hangs from a string of length $L$ fixed at a point,
and it moves in a horizontal circle so that the string sweeps out a cone at a
constant angle $\theta$ to the vertical. From the geometry of that cone,

$$ r = L\sin\theta \quad (\text{radius of the circle}), \qquad
h = L\cos\theta \quad (\text{depth of the circle below the support}) $$

Only two forces act on the bob: its weight $mg$ straight down, and the tension $T$
along the string towards the support.

**Step 1 — resolve the tension.** The string makes angle $\theta$ with the vertical, so
the tension has a vertical part $T\cos\theta$ (upwards) and a horizontal part
$T\sin\theta$ (pointing at the centre of the circle).

**Step 2 — vertical equation.** The bob stays at the same height, so it has no vertical
acceleration and the vertical forces balance:

$$ T\cos\theta = mg $$

**Step 3 — horizontal equation.** Horizontally the bob *is* accelerating — it is going
round a circle — and the only horizontal force is $T\sin\theta$. So this component
must supply the whole centripetal force:

$$ T\sin\theta = \frac{mv^{2}}{r} = mr\omega^{2} $$

**Step 4 — divide Step 3 by Step 2.** We divide because both $T$ and $m$ then cancel,
which is exactly what we want:

$$ \frac{T\sin\theta}{T\cos\theta} = \frac{mr\omega^{2}}{mg} $$

**Step 5 — cancel and use $\sin/\cos = \tan$:**

$$ \tan\theta = \frac{r\omega^{2}}{g} $$

(The same division with $mv^{2}/r$ instead gives the equally useful
$\tan\theta = v^{2}/rg$.)

**Step 6 — replace $r$ by $L\sin\theta$:**

$$ \tan\theta = \frac{L\sin\theta\;\omega^{2}}{g} $$

**Step 7 — write $\tan\theta$ as $\sin\theta/\cos\theta$:**

$$ \frac{\sin\theta}{\cos\theta} = \frac{L\sin\theta\;\omega^{2}}{g} $$

**Step 8 — cancel $\sin\theta$ from both sides.** This is allowed because the bob is
actually circling, so $\theta \ne 0$ and $\sin\theta \ne 0$:

$$ \frac{1}{\cos\theta} = \frac{L\omega^{2}}{g} $$

**Step 9 — make $\omega^{2}$ the subject.** Multiply both sides by $g$ and divide by
$L$:

$$ \omega^{2} = \frac{g}{L\cos\theta} $$

**Step 10 — take the square root:**

$$ \omega = \sqrt{\frac{g}{L\cos\theta}} $$

**Step 11 — convert to a period.** One revolution takes $T_p = 2\pi/\omega$:

$$ T_p = \frac{2\pi}{\sqrt{\dfrac{g}{L\cos\theta}}} $$

**Step 12 — turn the divided root upside down.** Dividing by $\sqrt{g/x}$ is the same
as multiplying by $\sqrt{x/g}$:

$$ T_p = 2\pi\sqrt{\frac{L\cos\theta}{g}} $$

**Step 13 — recognise $L\cos\theta$ as the depth $h$:**

$$ T_p = 2\pi\sqrt{\frac{h}{g}} $$

**Step 14 — the tension.** Go back to Step 2 and divide both sides by $\cos\theta$:

$$ T = \frac{mg}{\cos\theta} $$

**Result.**

$$ T_p = 2\pi\sqrt{\frac{L\cos\theta}{g}} = 2\pi\sqrt{\frac{h}{g}},
\qquad \tan\theta = \frac{v^{2}}{rg}, \qquad T = \frac{mg}{\cos\theta} $$

**What it means.** The mass cancelled, so a heavy bob and a light bob on the same
string at the same angle take the same time to go round. The period depends only on
the **depth** $h$ of the circle below the support — so as the bob spins faster, $\theta$
grows, $h$ shrinks and the period gets shorter. Because $\cos\theta < 1$, the tension
$mg/\cos\theta$ is always **bigger** than the weight, and it would become infinite at
$\theta = 90^{\circ}$ — which is why the string can never be truly horizontal.

**Conditions used.** The string is light and inextensible, the angle $\theta$ stays
constant (steady motion, not a wobble), air resistance is neglected, and the circle
is horizontal so there is no vertical acceleration.
:::

::: tip The examiner is looking for
(i) A labelled diagram showing $L$, $\theta$, $r$, $h$, $mg$ and $T$ resolved into
$T\cos\theta$ and $T\sin\theta$; (ii) the vertical **balance** equation with the reason
"no vertical acceleration"; (iii) the horizontal equation identified as the
centripetal force; (iv) the division step; (v) $r = L\sin\theta$ substituted and
$\sin\theta$ cancelled; (vi) the final period, plus the remark that it is independent
of the mass.
:::

The period depends on $h$, not on the mass of the bob — the same result as the
simple pendulum, with $h$ in place of $L$.

::: example Worked example 6.3
**Problem.** A bob of mass $0.50\ \text{kg}$ hangs from a string of length
$1.0\ \text{m}$ and moves in a horizontal circle with the string making
$60^{\circ}$ with the vertical. Taking $g = 10\ \text{m s}^{-2}$, find the
tension, the speed of the bob and the period.

**Solution.** $\cos 60^{\circ} = 0.5$, $\sin 60^{\circ} = 0.866$, $\tan 60^{\circ} = 1.732$.

$$ T = \frac{mg}{\cos\theta} = \frac{0.50 \times 10}{0.5} = 10\ \text{N} $$

Radius: $r = L\sin\theta = 1.0 \times 0.866 = 0.866\ \text{m}$. From
$\tan\theta = v^{2}/rg$:

$$ v = \sqrt{rg\tan\theta} = \sqrt{0.866 \times 10 \times 1.732} = \sqrt{15.0} = 3.87\ \text{m s}^{-1} $$

$$ T_p = 2\pi\sqrt{\frac{L\cos\theta}{g}} = 2\pi\sqrt{\frac{0.5}{10}} = 2\pi(0.2236) = 1.40\ \text{s} $$
:::

## 6.6 Motion in a vertical circle

Whirl a bucket of water in a vertical circle and the water does not fall out at
the top. Here gravity acts along the radius at the top and bottom, so the speed
is **not** constant — the motion is non-uniform circular motion.

```figure caption="Motion in a vertical circle. At the top $T_1 + mg = mv_1^2/r$; at the bottom $T_2 - mg = mv_2^2/r$. Hence $T_2 - T_1 = 6mg$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.2,3.4))
t = np.linspace(0,2*np.pi,300)
ax.plot(np.cos(t),np.sin(t),color=GRID,lw=1.4)
ax.plot([0],[0],'o',color=INK,ms=4)
ax.annotate('O',(0,0),textcoords='offset points',xytext=(-12,-4),color=INK,fontsize=9.5)
ax.plot([0,0],[0,1],color=INK,lw=1.0,ls=':')
ax.annotate('$r$',(0.11,0.28),ha='left',va='center',color=MUTED,fontsize=10)
def farrow(x, y0, y1, c):
    ax.annotate('', xy=(x,y1), xytext=(x,y0),
                arrowprops=dict(arrowstyle='-|>',color=c,lw=1.7,mutation_scale=12))
# at the top both T and mg point down, so they are drawn side by side
ax.add_patch(Circle((0,1),0.11,fc=ACCENT,ec=INK,lw=1.0))
farrow(-0.15, 1.0, 0.54, '#2e8b57')
ax.annotate('$T_1$',(-0.27,0.75),ha='right',va='center',color='#2e8b57',fontsize=10)
farrow(0.15, 1.0, 0.54, '#d9534f')
ax.annotate('$mg$',(0.27,0.75),ha='left',va='center',color='#d9534f',fontsize=10)
ax.annotate('',xy=(-0.75,1),xytext=(0,1),
            arrowprops=dict(arrowstyle='-|>',color=INK,lw=1.5,mutation_scale=12))
ax.annotate('$v_1$',(-0.45,1.10),ha='center',va='bottom',color=INK,fontsize=10)
ax.annotate('top',(0.42,1.32),ha='left',va='center',color=MUTED,fontsize=9)
# at the lowest point T is up and mg is down
ax.add_patch(Circle((0,-1),0.11,fc=ACCENT,ec=INK,lw=1.0))
farrow(0.0, -1.0, -0.52, '#2e8b57')
ax.annotate('$T_2$',(0.11,-0.72),ha='left',va='center',color='#2e8b57',fontsize=10)
farrow(0.0, -1.0, -1.48, '#d9534f')
ax.annotate('$mg$',(0.11,-1.28),ha='left',va='center',color='#d9534f',fontsize=10)
ax.annotate('',xy=(0.75,-1),xytext=(0,-1),
            arrowprops=dict(arrowstyle='-|>',color=INK,lw=1.5,mutation_scale=12))
ax.annotate('$v_2$',(0.60,-0.92),ha='center',va='bottom',color=INK,fontsize=10)
ax.annotate('lowest point',(0.42,-1.74),ha='left',va='center',color=MUTED,fontsize=9)
ax.set_xlim(-1.6,1.9); ax.set_ylim(-2.1,1.9); ax.set_aspect('equal'); ax.axis('off')
```
::: derivation Vertical circle: minimum speeds and the $6mg$ tension difference
We start from $F = mv^{2}/r$ applied at the top and at the bottom of the circle, add
conservation of energy between those two points, and reach three results: the least
speed at the top, the least speed at the bottom, and the fact that the tension
difference is always $6mg$.

**Setting up.** A mass $m$ on a string of length $r$ is whirled in a vertical circle.
Let $v_1$ be its speed at the highest point and $v_2$ at the lowest point. At both of
those two points the string is vertical, so the tension lies exactly along the radius
— which is why these two points are the easy ones to analyse.

---

**At the highest point**

**Step 1 — which way does each force point?** At the top, the centre of the circle is
**below** the mass. Both the weight $mg$ and the tension $T_1$ (pulling towards the
support, which is below) therefore point downwards, i.e. both point towards the
centre.

**Step 2 — write the centripetal equation.** The sum of the inward forces equals
$mv^{2}/r$:

$$ T_1 + mg = \frac{mv_1^{2}}{r} $$

**Step 3 — make $T_1$ the subject** by subtracting $mg$ from both sides:

$$ T_1 = \frac{mv_1^{2}}{r} - mg $$

**Step 4 — apply the physical limit.** A string can pull but cannot push, so the
tension can never be negative:

$$ T_1 \ge 0 $$

**Step 5 — substitute Step 3 into that inequality:**

$$ \frac{mv_1^{2}}{r} - mg \ge 0 $$

**Step 6 — add $mg$ to both sides:**

$$ \frac{mv_1^{2}}{r} \ge mg $$

**Step 7 — cancel $m$ and multiply both sides by $r$:**

$$ v_1^{2} \ge gr $$

**Step 8 — take the square root.** The smallest allowed speed is the boundary case:

$$ v_1(\min) = \sqrt{gr} $$

At exactly this speed $T_1 = 0$: the string goes slack and **gravity alone** supplies
the whole centripetal force.

---

**At the lowest point**

**Step 9 — which way does each force point?** At the bottom the centre is **above** the
mass. The tension $T_2$ points up (towards the centre) and the weight points down
(away from the centre), so the net inward force is $T_2 - mg$:

$$ T_2 - mg = \frac{mv_2^{2}}{r} $$

**Step 10 — make $T_2$ the subject:**

$$ T_2 = \frac{mv_2^{2}}{r} + mg $$

---

**Linking top and bottom by energy**

**Step 11 — apply conservation of mechanical energy.** The tension does no work
(it is always perpendicular to the motion), so only gravity matters. Take the lowest
point as the zero of potential energy; the highest point is a height $2r$ above it:

$$ \tfrac{1}{2}mv_2^{2} = \tfrac{1}{2}mv_1^{2} + mg(2r) $$

**Step 12 — multiply every term by 2:**

$$ mv_2^{2} = mv_1^{2} + 4mgr $$

**Step 13 — cancel $m$ throughout:**

$$ v_2^{2} = v_1^{2} + 4gr $$

**Step 14 — put in the minimum top speed $v_1^{2} = gr$:**

$$ v_2^{2} = gr + 4gr = 5gr $$

**Step 15 — take the square root:**

$$ v_2(\min) = \sqrt{5gr} $$

---

**The tension difference**

**Step 16 — subtract the top equation (Step 3) from the bottom one (Step 10):**

$$ T_2 - T_1 = \left(\frac{mv_2^{2}}{r} + mg\right) - \left(\frac{mv_1^{2}}{r} - mg\right) $$

**Step 17 — remove the brackets carefully; the two $mg$ terms now add:**

$$ T_2 - T_1 = \frac{mv_2^{2}}{r} - \frac{mv_1^{2}}{r} + 2mg $$

**Step 18 — combine the first two terms over the common denominator $r$:**

$$ T_2 - T_1 = \frac{m(v_2^{2} - v_1^{2})}{r} + 2mg $$

**Step 19 — use Step 13, which says $v_2^{2} - v_1^{2} = 4gr$:**

$$ T_2 - T_1 = \frac{m(4gr)}{r} + 2mg $$

**Step 20 — cancel $r$:**

$$ T_2 - T_1 = 4mg + 2mg = 6mg $$

---

**Result.**

$$ v_1(\min) = \sqrt{gr}, \qquad v_2(\min) = \sqrt{5gr},
\qquad T_2 - T_1 = 6mg $$

**What it means.** To keep the string taut all the way round you need a speed at the
bottom of at least $\sqrt{5gr}$ — that is why you must swing a bucket of water
briskly. The $6mg$ result is remarkable: the speed cancelled out, so the tension
difference between bottom and top is the same no matter how fast you whirl it (as
long as it does get round).

**Conditions used.** The string is light and inextensible, air resistance is
neglected, and Step 11 assumed no energy is lost to friction. The $6mg$ result and
$v_2^{2} = v_1^{2} + 4gr$ hold for **any** speed; only $v_1 = \sqrt{gr}$ and
$v_2 = \sqrt{5gr}$ are the special minimum case. For a **rod** instead of a string
the rod can push, so $T_1$ may be negative and the minimum top speed is zero.
:::

::: tip The examiner is looking for
(i) A diagram with the forces drawn at the top and at the bottom; (ii) the correct
*signs* — both forces inward at the top, opposing at the bottom; (iii) the argument
"a string cannot push, so $T \ge 0$" leading to $v_1 = \sqrt{gr}$; (iv) energy
conservation over the height $2r$, with the remark that the tension does no work;
(v) the subtraction giving $6mg$. Marks are most often lost on (ii) and on forgetting
that the height difference is $2r$, not $r$.
:::

::: example Worked example 6.4
**Problem.** A body of mass $1\ \text{kg}$ tied to a string of length $1\ \text{m}$
is rotated in a vertical circle. Its speed at the highest point is
$5\ \text{m s}^{-1}$. Taking $g = 10\ \text{m s}^{-2}$, find the tension at the
highest and lowest points, and the minimum speed needed at the top.

**Solution.** At the top:

$$ T_1 = \frac{mv_1^{2}}{r} - mg = \frac{1 \times 25}{1} - 10 = 15\ \text{N} $$

Speed at the bottom: $v_2^{2} = v_1^{2} + 4gr = 25 + 40 = 65\ \text{m}^{2}\text{s}^{-2}$,
so $v_2 = 8.06\ \text{m s}^{-1}$. Then

$$ T_2 = \frac{mv_2^{2}}{r} + mg = 65 + 10 = 75\ \text{N} $$

*Check:* $T_2 - T_1 = 60\ \text{N} = 6mg$ ✓. The minimum speed at the top is
$v_1(\min) = \sqrt{gr} = \sqrt{10} = 3.16\ \text{m s}^{-1}$; the actual
$5\ \text{m s}^{-1}$ is comfortably above it.
:::

## 6.7 Applications of banking

On a level road the centripetal force for a turn can only come from friction,
which is unreliable when the surface is wet or dusty. So the outer edge of a
curve is raised above the inner edge — the road is **banked** — and a component
of the normal reaction does the job instead.

```figure caption="Cross-section of a banked road. The normal reaction $N$ resolves into $N\cos\theta$ balancing $mg$ and $N\sin\theta$ providing the centripetal force."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.8,2.9))
th = np.radians(22)
x0, x1 = 0.0, 5.0
ax.add_patch(Polygon([[x0,0],[x1,0],[x1,x1*np.tan(th)]], closed=True,
                     fc='#e7ebf1', ec=INK, lw=1.3))
P = np.array([3.0, 3.0*np.tan(th)])
ax.plot([P[0]],[P[1]],'s',color=ACCENT,ms=9, mec=INK)
n = np.array([-np.sin(th), np.cos(th)])*2.1
nu = n/np.linalg.norm(n); pu = np.array([nu[1], -nu[0]])
ax.annotate('',xy=P+n,xytext=P,
            arrowprops=dict(arrowstyle='-|>',color='#2e8b57',lw=1.9,mutation_scale=13))
ax.annotate('$N$',P+0.85*n+0.34*pu,ha='center',va='center',color='#2e8b57',fontsize=10)
ax.annotate('',xy=(P[0],P[1]+n[1]),xytext=P,
            arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.0,mutation_scale=10,linestyle=(0,(3,2))))
ax.annotate(r'$N\cos\theta$',(P[0]+0.24,P[1]+n[1]*0.55),ha='left',va='center',
            color=MUTED,fontsize=9)
ax.annotate('',xy=(P[0]+n[0],P[1]),xytext=P,
            arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.0,mutation_scale=10,linestyle=(0,(3,2))))
# label placed beyond the arrow tip, off the block and off the N arrow
ax.annotate(r'$N\sin\theta$',(P[0]+n[0]-0.20,P[1]),ha='right',va='center',
            color=MUTED,fontsize=9)
ax.annotate('',xy=(P[0],P[1]-1.05),xytext=P,
            arrowprops=dict(arrowstyle='-|>',color='#d9534f',lw=1.9,mutation_scale=13))
ax.annotate('$mg$',(P[0]+0.22,P[1]-0.78),ha='left',va='center',color='#d9534f',fontsize=10)
arc = np.linspace(0,th,40)
ax.plot(x0+1.5*np.cos(arc), 1.5*np.sin(arc), color='#d9534f', lw=1.2)
ax.annotate(r'$\theta$',(1.70,0.28),ha='center',va='center',color='#d9534f',fontsize=11)
ax.annotate('',xy=(-1.85,-0.55),xytext=(0.0,-0.55),
            arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.0,mutation_scale=10))
ax.annotate('to centre of curve', xy=(-1.85,-0.55), textcoords='offset points',
            xytext=(0,-13), ha='left', color=MUTED, fontsize=8.6)
ax.set_xlim(-2.3,5.9); ax.set_ylim(-1.5,4.4); ax.set_aspect('equal'); ax.axis('off')
```
::: derivation Angle of banking of a road
We start from the two force equations for a car on a frictionless banked road and
reach a formula for the correct banking angle.

**Setting up.** The road surface is tilted at an angle $\theta$ to the horizontal, with
the outer edge raised. Take friction as negligible, so only two forces act on a car of
mass $m$: its weight $mg$ straight down, and the normal reaction $N$ at right angles
to the road surface. Because the surface is tilted by $\theta$, the normal $N$ is
tilted by $\theta$ from the vertical.

**Step 1 — resolve $N$ into vertical and horizontal parts.** Since $N$ makes angle
$\theta$ with the vertical:

$$ \text{vertical part} = N\cos\theta, \qquad
\text{horizontal part} = N\sin\theta \ (\text{pointing towards the centre}) $$

**Step 2 — the vertical equation.** The car stays on the road and does not rise or
sink, so it has no vertical acceleration; the vertical forces must balance:

$$ N\cos\theta = mg $$

**Step 3 — the horizontal equation.** Horizontally the car *is* accelerating, because
it is turning. The only horizontal force is $N\sin\theta$, so that component must be
the whole centripetal force:

$$ N\sin\theta = \frac{mv^{2}}{r} $$

**Step 4 — divide Step 3 by Step 2.** We divide because both $N$ and $m$ then cancel:

$$ \frac{N\sin\theta}{N\cos\theta} = \frac{mv^{2}/r}{mg} $$

**Step 5 — cancel $N$ on the left and $m$ on the right:**

$$ \frac{\sin\theta}{\cos\theta} = \frac{v^{2}}{rg} $$

**Step 6 — use $\sin\theta/\cos\theta = \tan\theta$:**

$$ \tan\theta = \frac{v^{2}}{rg} $$

**Step 7 — take the inverse tangent to get the angle:**

$$ \theta = \tan^{-1}\left(\frac{v^{2}}{rg}\right) $$

**Step 8 — or make $v$ the subject instead.** Multiply Step 6 by $rg$ and take the
square root:

$$ v = \sqrt{rg\tan\theta} $$

**Step 9 — the height of the outer edge.** If the road is $b$ wide, the raised edge is
the "opposite" side of a right triangle whose hypotenuse is $b$:

$$ h = b\sin\theta $$

**Result.**

$$ \tan\theta = \frac{v^{2}}{rg}, \qquad v = \sqrt{rg\tan\theta},
\qquad h = b\sin\theta $$

**What it means.** The mass cancelled in Step 5, so one banking angle serves a
motorcycle and a loaded truck equally — the engineer only has to choose the design
speed $v$ and the radius $r$. Sharper bends (small $r$) and faster roads (large $v$)
need steeper banking. A cyclist leaning into a turn uses the identical relation.

**Conditions used.** Friction is neglected, so this gives the **one** speed at which no
sideways friction is needed at all. The car is treated as a point mass (no toppling),
the road is a circular arc of fixed radius, and $\theta$ is the same across the whole
width. At speeds away from the design speed, friction must make up the difference —
which is where the $v_{\max}$ formula below comes from.
:::

::: tip The examiner is looking for
(i) A diagram of the tilted surface with $mg$, $N$, and $N$ resolved into
$N\cos\theta$ and $N\sin\theta$; (ii) the words "no vertical acceleration" beside the
vertical equation; (iii) the horizontal component named as the centripetal force;
(iv) the division step; (v) the final relation plus the statement "independent of the
mass of the vehicle". A very common error is resolving $mg$ along the slope instead of
resolving $N$ vertically — for banking, resolve $N$.
:::

Including friction, the **maximum safe speed** on a banked road is

$$ v_{\max} = \sqrt{\frac{rg(\mu + \tan\theta)}{1 - \mu\tan\theta}} $$

which reduces to $v_{\max} = \sqrt{\mu rg}$ for a level road ($\theta = 0$).

- **Roads.** Highway bends such as those on the Mugling–Naubise section are
  banked for a chosen design speed.
- **Railways.** The outer rail on a curve is laid higher than the inner rail
  ("superelevation") so that the flanges do not grind against the rails.
- **Aircraft.** A turning aeroplane banks its wings so that the horizontal
  component of the lift becomes the centripetal force.
- **Cyclists and bikers** lean inwards at an angle $\theta$ with
  $\tan\theta = v^{2}/rg$ — exactly the same relation.

::: example Worked example 6.5
**Problem.** A curve of radius $100\ \text{m}$ on a highway is to be banked for a
speed of $72\ \text{km h}^{-1}$. Find the angle of banking and, if the road is
$10\ \text{m}$ wide, the height of the outer edge above the inner edge. Take
$g = 10\ \text{m s}^{-2}$.

**Solution.** First convert the speed:
$72\ \text{km h}^{-1} = 72 \times \frac{5}{18} = 20\ \text{m s}^{-1}$.

$$ \tan\theta = \frac{v^{2}}{rg} = \frac{400}{100 \times 10} = 0.40
\qquad \Longrightarrow \qquad \theta = 21.8^{\circ} $$

The outer edge must be raised by

$$ h = b\sin\theta = 10 \times \sin 21.8^{\circ} = 10 \times 0.371 = 3.71\ \text{m} $$
:::

## Chapter summary

- $\theta = s/r$ in radians; $\omega = d\theta/dt = 2\pi/T = 2\pi f$;
  $\alpha = d\omega/dt$. Angular kinematic equations mirror the linear ones.
- $v = r\omega$ and $a_t = r\alpha$; all points of a rigid rotating body share
  $\omega$ but not $v$.
- Centripetal acceleration $a_c = v^{2}/r = r\omega^{2} = 4\pi^{2}r/T^{2}$,
  directed towards the centre. Total acceleration $= \sqrt{a_c^2 + a_t^2}$.
- Centripetal force $F_c = mv^{2}/r$ is supplied by tension, friction, gravity or
  a component of the normal reaction. Centrifugal force is a fictitious force.
- Conical pendulum: $\tan\theta = v^{2}/rg$, $T = mg/\cos\theta$, period
  $T_p = 2\pi\sqrt{L\cos\theta/g} = 2\pi\sqrt{h/g}$.
- Vertical circle: $v_{\text{top}}(\min) = \sqrt{gr}$,
  $v_{\text{bottom}}(\min) = \sqrt{5gr}$, $v_2^2 = v_1^2 + 4gr$, and
  $T_2 - T_1 = 6mg$ always.
- Banking: $\tan\theta = v^{2}/rg$, independent of mass;
  $v_{\max} = \sqrt{rg(\mu+\tan\theta)/(1-\mu\tan\theta)}$; on a level road
  $v_{\max} = \sqrt{\mu rg}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. A body moves in a circle at constant speed. Which quantity remains
   constant? <span class="marks">[1]</span>
   (a) velocity (b) acceleration (c) kinetic energy (d) momentum
2. The angular velocity of a body making $300$ revolutions per minute
   is <span class="marks">[1]</span>
   (a) $5\ \text{rad s}^{-1}$ (b) $10\pi\ \text{rad s}^{-1}$ (c) $300\ \text{rad s}^{-1}$ (d) $60\pi\ \text{rad s}^{-1}$
3. The angle of banking of a road is independent of <span class="marks">[1]</span>
   (a) speed of the vehicle (b) radius of the curve (c) mass of the vehicle (d) acceleration due to gravity
4. The minimum speed at the highest point of a vertical circle of radius $r$
   is <span class="marks">[1]</span>
   (a) $\sqrt{5gr}$ (b) $\sqrt{2gr}$ (c) $\sqrt{gr}$ (d) zero
5. The work done by the centripetal force in one complete revolution
   is <span class="marks">[1]</span>
   (a) $mv^{2}/r$ (b) $2\pi r \cdot mv^{2}/r$ (c) zero (d) $\frac{1}{2}mv^{2}$

::: note Answers to Group A
**1.** (c) — the speed is constant, so $\frac{1}{2}mv^2$ is constant; velocity, acceleration and momentum all change direction.
**2.** (b) — $\omega = 2\pi N/60 = 2\pi(300)/60 = 10\pi\ \text{rad s}^{-1}$.
**3.** (c) — $\tan\theta = v^2/rg$ contains no mass term.
**4.** (c) — at the limit the tension is zero and gravity alone gives $mg = mv^2/r$.
**5.** (c) — the force is always perpendicular to the displacement, so $W = 0$.
:::

**Group B — Short answer (5 marks each)**

1. Define angular velocity and angular acceleration. Derive the relations
   $v = r\omega$ and $a_t = r\alpha$. <span class="marks">[5]</span>
2. Derive an expression for the centripetal acceleration of a body moving
   uniformly in a circle of radius $r$ with speed $v$. <span class="marks">[5]</span>
3. What is a conical pendulum? Derive an expression for its period. <span class="marks">[5]</span>
4. Show that for a body moving in a vertical circle the difference between the
   tensions at the lowest and the highest points is $6mg$. <span class="marks">[5]</span>
5. A stone of mass $0.20\ \text{kg}$ is whirled in a horizontal circle of radius
   $0.50\ \text{m}$ at $4\ \text{rev s}^{-1}$. Calculate its linear speed and the
   tension in the string. <span class="marks">[5]</span>

::: note Answers to Group B
**5.** $\omega = 2\pi f = 2\pi(4) = 8\pi = 25.13\ \text{rad s}^{-1}$.
Linear speed $v = r\omega = 0.50 \times 25.13 = 12.6\ \text{m s}^{-1}$.
Tension $= mr\omega^{2} = 0.20 \times 0.50 \times (25.13)^{2} = 0.10 \times 631.7
= 63.2\ \text{N}$.

**1., 2., 3., 4.** See §6.2, the derivation box in §6.3, §6.5 and §6.6
respectively.
:::

**Group C — Long answer (8 marks each)**

1. (a) What is meant by banking of a road? Derive an expression for the angle of
   banking of a curved road for a vehicle moving with speed $v$ on a curve of
   radius $r$. <span class="marks">[5]</span>
   (b) A cyclist rides round a circular track of radius $20\ \text{m}$ at
   $10\ \text{m s}^{-1}$. Find the angle through which he must lean from the
   vertical. Take $g = 10\ \text{m s}^{-2}$. <span class="marks">[3]</span>
2. (a) Derive expressions for the minimum speeds at the highest and lowest points
   for a body to just complete a vertical circle of radius $r$. <span class="marks">[5]</span>
   (b) A bucket of water of mass $2\ \text{kg}$ is whirled in a vertical circle of
   radius $1\ \text{m}$. Find the minimum speed at the top for the water not to
   spill, and the tension in the rope at the lowest point in that case
   ($g = 10\ \text{m s}^{-2}$). <span class="marks">[3]</span>

::: note Answers to Group C
**1.** (b) A leaning cyclist obeys the same relation, $\tan\theta = v^{2}/rg
= 100/(20 \times 10) = 0.50$, so $\theta = 26.6^{\circ}$ from the vertical.

**2.** (b) Minimum speed at the top: $v_1 = \sqrt{gr} = \sqrt{10 \times 1}
= 3.16\ \text{m s}^{-1}$. Then $v_2^{2} = v_1^{2} + 4gr = 10 + 40 = 50$, so
$T_2 = \dfrac{mv_2^{2}}{r} + mg = \dfrac{2 \times 50}{1} + 20 = 120\ \text{N}$
(which is $6mg$, as expected when $T_1 = 0$).
:::
