---
subject: Mathematics
grade: 11
unit: 21
title: Mechanics (alternative to Unit 20)
hours: 12
area: Computational Methods OR Mechanics
---

Mechanics is the part of mathematics that describes how bodies push, pull and move.
It is the oldest application of the algebra and calculus you have already learned,
and it is the reason those subjects were invented. In this unit a force is a vector,
so every rule from Unit 7 (Vectors) applies unchanged: forces add by the
parallelogram law, they resolve into components, and a body stays still only when
the vector sum of the forces on it is zero. Motion is described by three quantities
— displacement, velocity, acceleration — and velocity is the derivative of
displacement, acceleration the derivative of velocity, exactly as in Unit 18.

Mechanics splits into two halves, and this unit follows that split.

- **Statics** studies bodies at rest. The question is always: what combination of
  forces leaves the body in equilibrium?
- **Dynamics** studies bodies in motion. The question is always: given the forces
  (or the acceleration they produce), where is the body and how fast is it going?

Throughout, forces are measured in **newtons (N)**, lengths in metres (m), time in
seconds (s), and the acceleration due to gravity is taken as
$g = 9.8\ \text{m/s}^2$ unless a question says otherwise. Some board questions use
$g = 10\ \text{m/s}^2$ to keep the arithmetic short; always use the value printed in
the question.

::: caution Unit 20 or Unit 21 — you choose one
The syllabus offers Computational Methods (Unit 20) **or** Mechanics (Unit 21) as
alternatives worth 12 teaching hours. In the examination the two appear as
alternative questions: you attempt the set for the option your school taught. Do
not split your revision across both.
:::

## 21.1 Statics: forces and resultant forces; parallelogram law of forces

### What a force is

A **force** is a push or a pull. To describe it completely you need three things:
its **magnitude** (how hard, in newtons), its **direction**, and its **point of
application**. Magnitude and direction together make a force a **vector**, so we
write it as $\vec{F}$ and draw it as an arrow whose length is proportional to the
magnitude.

Because forces are vectors, two forces acting at the same point can be replaced by
a single force with the same effect. That single force is the **resultant**.
Conversely, any force can be replaced by two or more forces whose resultant is the
original; those are its **components**. Replacing several forces by one is
**composition**; replacing one by several is **resolution**. Both are used
constantly, and §21.2 treats them in detail.

::: definition Resultant and equilibrium
The **resultant** of a set of forces acting at a point is the single force that has
the same effect as the whole set. If the resultant is the zero vector, the forces
are in **equilibrium** and a body at rest under them stays at rest.
:::

Forces acting at a single point are called **concurrent**; forces all lying in one
plane are **coplanar**. Everything in this unit deals with coplanar concurrent
forces, which is what the syllabus requires.

### The parallelogram law of forces

Two forces acting at a point are combined by the same construction used for vectors.

::: key Parallelogram law of forces
If two forces acting at a point are represented in magnitude and direction by the
two adjacent sides of a parallelogram drawn from that point, their resultant is
represented in magnitude and direction by the diagonal of the parallelogram through
that point.
:::

Put the law into symbols. Let two forces of magnitudes $P$ and $Q$ act at the point
$O$ with angle $\theta$ between them, and let the resultant $R$ make angle $\alpha$
with $P$.

```figure caption="The parallelogram law. Forces $P$ and $Q$ at angle $\theta$ have resultant $R$ along the diagonal, making angle $\alpha$ with $P$."
import numpy as np
fig, ax = plt.subplots(figsize=(4.8, 3.0))
P = np.array([4.0, 0.0])
th = np.radians(62.0)
Q = 3.0*np.array([np.cos(th), np.sin(th)])
R = P + Q
O = np.array([0.0, 0.0])
def arrow(a, b, color, lw=1.7):
    ax.annotate("", xy=b, xytext=a,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0))
# parallelogram sides (dashed completions)
ax.plot([P[0], R[0]], [P[1], R[1]], ls="--", color=MUTED, lw=1.0)
ax.plot([Q[0], R[0]], [Q[1], R[1]], ls="--", color=MUTED, lw=1.0)
arrow(O, P, SERIES[2])
arrow(O, Q, SERIES[1])
arrow(O, R, ACCENT, lw=2.1)
ax.text(P[0]*0.55, -0.28, "$P$", color=SERIES[2], fontsize=11)
ax.text(Q[0]*0.45-0.30, Q[1]*0.52+0.06, "$Q$", color=SERIES[1], fontsize=11)
ax.text(R[0]*0.52+0.06, R[1]*0.52+0.16, "$R$", color=ACCENT, fontsize=11)
# angle theta at O between P and Q
t = np.linspace(0, th, 60)
ax.plot(0.95*np.cos(t), 0.95*np.sin(t), color=MUTED, lw=0.9)
ax.text(1.12*np.cos(th/2), 1.12*np.sin(th/2)-0.02, r"$\theta$", color=INK, fontsize=10)
al = np.arctan2(R[1], R[0])
t2 = np.linspace(0, al, 60)
ax.plot(1.75*np.cos(t2), 1.75*np.sin(t2), color=ACCENT, lw=0.9)
ax.text(1.95*np.cos(al/2), 1.95*np.sin(al/2)-0.12, r"$\alpha$", color=ACCENT, fontsize=10)
ax.plot([0], [0], "o", color=INK, ms=4)
ax.text(-0.30, -0.28, "$O$", color=INK, fontsize=10)
ax.set_xlim(-0.8, 7.0); ax.set_ylim(-0.8, 3.4)
ax.set_aspect("equal"); ax.axis("off")
```

Drop a perpendicular from the tip of the resultant to the line of $P$ extended. The
horizontal side of the right triangle so formed is $P + Q\cos\theta$ and the
vertical side is $Q\sin\theta$. Pythagoras and the tangent ratio give the two
working formulas.

::: key Magnitude and direction of the resultant of two forces
For forces $P$ and $Q$ with angle $\theta$ between them,
$$ R = \sqrt{P^2 + Q^2 + 2PQ\cos\theta}, \qquad \tan\alpha = \frac{Q\sin\theta}{P + Q\cos\theta} $$
where $\alpha$ is the angle the resultant makes with the force $P$.
:::

::: derivation Where the formula comes from
Place $O$ at the origin with $P$ along the $x$-axis. Then
$\vec{P} = (P,\,0)$ and $\vec{Q} = (Q\cos\theta,\ Q\sin\theta)$.

Adding the vectors, the resultant is
$$ \vec{R} = (P + Q\cos\theta,\ Q\sin\theta) $$

Its magnitude is the square root of the sum of the squares of the components:
$$ R^2 = (P + Q\cos\theta)^2 + (Q\sin\theta)^2 $$

Expanding the first bracket,
$$ R^2 = P^2 + 2PQ\cos\theta + Q^2\cos^2\theta + Q^2\sin^2\theta $$

Now use $\cos^2\theta + \sin^2\theta = 1$ on the last two terms:
$$ R^2 = P^2 + Q^2 + 2PQ\cos\theta $$

The direction follows from the right triangle, since $\tan\alpha$ is the vertical
component over the horizontal component:
$$ \tan\alpha = \frac{Q\sin\theta}{P + Q\cos\theta} $$
:::

Three special cases are worth memorising because they appear in multiple-choice
questions.

| Angle between the forces | Resultant $R$ | Direction |
|---|---|---|
| $\theta = 0^\circ$ (same direction) | $P + Q$ — the maximum possible | along both forces |
| $\theta = 90^\circ$ (perpendicular) | $\sqrt{P^2+Q^2}$ | $\tan\alpha = Q/P$ |
| $\theta = 180^\circ$ (opposite) | $|P - Q|$ — the minimum possible | along the larger force |

So the resultant of two forces always lies between $|P-Q|$ and $P+Q$. If a question
claims two forces of 3 N and 4 N have a resultant of 9 N, it is wrong: the largest
possible resultant is 7 N.

::: example Worked example 21.1 — perpendicular forces
Two forces of 5 N and 12 N act at a point at right angles to each other. Find the
magnitude of the resultant and the angle it makes with the 12 N force.

**Solution.** Here $P = 12$, $Q = 5$, $\theta = 90^\circ$, so $\cos\theta = 0$.

Substituting into the magnitude formula:
$$ R = \sqrt{12^2 + 5^2 + 0} = \sqrt{144 + 25} = \sqrt{169} = 13\ \text{N} $$

For the direction, with $\cos 90^\circ = 0$ and $\sin 90^\circ = 1$:
$$ \tan\alpha = \frac{5 \times 1}{12 + 0} = \frac{5}{12} = 0.4167 $$

Taking the inverse tangent:
$$ \alpha = \tan^{-1}(0.4167) = 22.62^\circ = 22^\circ 37' $$

The resultant is **13 N at $22^\circ 37'$ to the 12 N force**.
:::

::: example Worked example 21.2 — a general angle
Forces of 3 N and 5 N act at a point with $60^\circ$ between them. Find the
resultant completely.

**Solution.** Take $P = 3$, $Q = 5$, $\theta = 60^\circ$, so
$\cos 60^\circ = \tfrac{1}{2}$ and $\sin 60^\circ = \tfrac{\sqrt{3}}{2}$.

Magnitude first:
$$ R = \sqrt{3^2 + 5^2 + 2(3)(5)\left(\tfrac{1}{2}\right)} = \sqrt{9 + 25 + 15} = \sqrt{49} = 7\ \text{N} $$

Now the direction, measured from the 3 N force:
$$ \tan\alpha = \frac{5\left(\tfrac{\sqrt{3}}{2}\right)}{3 + 5\left(\tfrac{1}{2}\right)} = \frac{4.330}{5.5} = 0.7873 $$

Hence
$$ \alpha = \tan^{-1}(0.7873) = 38.21^\circ = 38^\circ 13' $$

The resultant is **7 N at $38^\circ 13'$ to the 3 N force**, and therefore at
$60^\circ - 38^\circ 13' = 21^\circ 47'$ to the 5 N force.
:::

::: example Worked example 21.3 — working backwards to the angle
The resultant of two forces of 7 N and 8 N is 13 N. Find the angle between the
forces.

**Solution.** Substitute the three magnitudes into $R^2 = P^2+Q^2+2PQ\cos\theta$:
$$ 13^2 = 7^2 + 8^2 + 2(7)(8)\cos\theta $$

Evaluating the squares:
$$ 169 = 49 + 64 + 112\cos\theta = 113 + 112\cos\theta $$

Rearranging for the cosine:
$$ \cos\theta = \frac{169 - 113}{112} = \frac{56}{112} = \frac{1}{2} $$

Therefore $\theta = 60^\circ$.

Check the answer for plausibility: 13 N lies between $|8-7| = 1$ N and
$8+7 = 15$ N, so a solution must exist — and it does.
:::

::: example Worked example 21.4 — two equal forces
Two equal forces of magnitude $P$ act at a point and their resultant is also $P$.
Find the angle between them.

**Solution.** Put $Q = P$ and $R = P$ in the magnitude formula:
$$ P^2 = P^2 + P^2 + 2P^2\cos\theta $$

Cancel $P^2$ throughout (it is non-zero):
$$ 1 = 2 + 2\cos\theta $$

Solving for the cosine:
$$ \cos\theta = -\frac{1}{2} \quad\Longrightarrow\quad \theta = 120^\circ $$

The two forces are inclined at $120^\circ$. By symmetry the resultant bisects the
angle, so it makes $60^\circ$ with each force.
:::

### Triangle law and Lami's theorem

The parallelogram law has an equivalent form that is often quicker to use.

::: key Triangle law of forces
If two forces acting at a point are represented in magnitude and direction by two
sides of a triangle taken in order, their resultant is represented by the third
side taken in the reverse order.
:::

Turning that around gives the condition for three forces to be in equilibrium: if
three concurrent forces are in equilibrium, they can be represented by the three
sides of a triangle taken in order. Applying the sine rule to that triangle gives a
result that solves most statics problems in one line.

::: key Lami's theorem
If three coplanar concurrent forces $P$, $Q$, $S$ are in equilibrium, then
$$ \frac{P}{\sin\alpha} = \frac{Q}{\sin\beta} = \frac{S}{\sin\gamma} $$
where $\alpha$ is the angle **between the other two forces** $Q$ and $S$, and
similarly for $\beta$ and $\gamma$. Note $\alpha + \beta + \gamma = 360^\circ$.
:::

::: example Worked example 21.5 — Lami's theorem
A body of weight 20 N hangs at rest from two light strings. One string makes
$30^\circ$ with the vertical and the other $60^\circ$ with the vertical, on opposite
sides. Find the tension in each string.

**Solution.** Three forces act at the knot: the tensions $T_1$ and $T_2$ along the
strings, and the weight 20 N vertically downwards. They are in equilibrium, so
Lami's theorem applies. First find the angle opposite each force.

The two strings make $30^\circ + 60^\circ = 90^\circ$ with each other, so the angle
between $T_1$ and $T_2$ is $90^\circ$; this is the angle opposite the weight.
The angle between $T_2$ and the downward weight is $180^\circ - 60^\circ = 120^\circ$,
which is opposite $T_1$. Likewise the angle opposite $T_2$ is
$180^\circ - 30^\circ = 150^\circ$.

By Lami's theorem,
$$ \frac{T_1}{\sin 120^\circ} = \frac{T_2}{\sin 150^\circ} = \frac{20}{\sin 90^\circ} $$

The last ratio equals 20, since $\sin 90^\circ = 1$. Hence
$$ T_1 = 20\sin 120^\circ = 20(0.8660) = 17.32\ \text{N} $$

and
$$ T_2 = 20\sin 150^\circ = 20(0.5) = 10\ \text{N} $$

The tensions are **17.32 N** (in the string nearer the vertical) and **10 N**. As a
check, the vertical components must carry the weight:
$17.32\cos 30^\circ + 10\cos 60^\circ = 15 + 5 = 20$ N. Correct.
:::

## 21.2 Composition and resolution of forces; resultant of coplanar forces acting on a point

### Resolving a force into components

Composition replaces many forces by one. **Resolution** is the reverse operation and
is the more useful of the two, because once every force is written in components the
whole problem becomes arithmetic with no geometry at all.

::: key Rectangular components
A force $F$ making an angle $\theta$ with the $x$-axis has components
$$ F_x = F\cos\theta, \qquad F_y = F\sin\theta $$
and conversely $F = \sqrt{F_x^2 + F_y^2}$ with $\tan\theta = F_y/F_x$.
:::

```figure caption="Resolving a force $F$ at angle $\theta$ into the rectangular components $F\cos\theta$ and $F\sin\theta$."
import numpy as np
fig, ax = plt.subplots(figsize=(4.6, 2.9))
F = 4.2
th = np.radians(38.0)
tip = np.array([F*np.cos(th), F*np.sin(th)])
def arrow(a, b, color, lw=1.7, ls="-"):
    ax.annotate("", xy=b, xytext=a,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls,
                                shrinkA=0, shrinkB=0))
ax.axhline(0, color=GRID, lw=0.9)
ax.axvline(0, color=GRID, lw=0.9)
arrow((0, 0), tip, ACCENT, lw=2.1)
arrow((0, 0), (tip[0], 0), SERIES[2])
arrow((0, 0), (0, tip[1]), SERIES[1])
ax.plot([tip[0], tip[0]], [0, tip[1]], ls=":", color=MUTED, lw=1.0)
ax.plot([0, tip[0]], [tip[1], tip[1]], ls=":", color=MUTED, lw=1.0)
ax.text(tip[0]*0.52+0.10, tip[1]*0.52+0.22, "$F$", color=ACCENT, fontsize=11)
ax.text(tip[0]*0.45, -0.40, r"$F\cos\theta$", color=SERIES[2], fontsize=10)
ax.text(-1.16, tip[1]*0.46, r"$F\sin\theta$", color=SERIES[1], fontsize=10)
t = np.linspace(0, th, 60)
ax.plot(1.05*np.cos(t), 1.05*np.sin(t), color=MUTED, lw=0.9)
ax.text(1.22*np.cos(th/2), 1.22*np.sin(th/2)-0.10, r"$\theta$", color=INK, fontsize=10)
# right angle square at the foot
s = 0.17
ax.plot([tip[0]-s, tip[0]-s, tip[0]], [0, s, s], color=MUTED, lw=0.9)
ax.set_xlim(-1.35, 4.3); ax.set_ylim(-0.75, 3.1)
ax.set_aspect("equal"); ax.axis("off")
```

Two remarks make resolution safe in the examination.

- The **direction matters for the sign**. A force pointing left has a negative
  $x$-component; one pointing down has a negative $y$-component. Choose east and
  north as positive once, at the start, and keep that choice.
- You may resolve along **any** two perpendicular directions, not only horizontal
  and vertical. On an inclined plane it is almost always better to resolve along and
  perpendicular to the plane, as §21.4 does.

### Resultant of any number of coplanar concurrent forces

Because components simply add, the method extends to as many forces as you like.

::: key Resultant by components
For forces $F_1, F_2, \dots, F_n$ acting at a point at angles
$\theta_1, \theta_2, \dots, \theta_n$ to the $x$-axis, let
$$ X = \sum F_i\cos\theta_i, \qquad Y = \sum F_i\sin\theta_i $$
Then the resultant has magnitude and direction
$$ R = \sqrt{X^2 + Y^2}, \qquad \tan\theta = \frac{Y}{X} $$
and the forces are in **equilibrium** if and only if $X = 0$ **and** $Y = 0$.
:::

::: caution Which quadrant is the resultant in?
A calculator returns $\tan^{-1}(Y/X)$ between $-90^\circ$ and $90^\circ$, so it
cannot tell you the quadrant. Read the **signs of $X$ and $Y$** and place the
resultant yourself: $X>0, Y>0$ first quadrant; $X<0, Y>0$ second; $X<0, Y<0$ third;
$X>0, Y<0$ fourth. Always sketch.
:::

::: example Worked example 21.6 — four forces at a point
Forces of 5 N, 10 N, 15 N and 20 N act at a point in the directions east, north,
west and south respectively. Find their resultant.

**Solution.** Take east as the positive $x$-direction and north as positive $y$.
The four forces are along $0^\circ$, $90^\circ$, $180^\circ$, $270^\circ$.

Sum the $x$-components. Only the east and west forces contribute:
$$ X = 5 - 15 = -10\ \text{N} $$

Sum the $y$-components. Only the north and south forces contribute:
$$ Y = 10 - 20 = -10\ \text{N} $$

The magnitude of the resultant is
$$ R = \sqrt{(-10)^2 + (-10)^2} = \sqrt{200} = 10\sqrt{2} = 14.14\ \text{N} $$

For the direction, $\tan\theta = (-10)/(-10) = 1$, and since both $X$ and $Y$ are
negative the resultant lies in the **third quadrant**, i.e. it points south-west:
$$ \theta = 180^\circ + 45^\circ = 225^\circ $$

The resultant is **$10\sqrt{2} \approx 14.14$ N towards the south-west**, making
$45^\circ$ with both the south and the west directions.
:::

```figure caption="Worked example 21.6: four coplanar forces at a point and their resultant $10\sqrt{2}$ N to the south-west."
import numpy as np
fig, ax = plt.subplots(figsize=(4.4, 3.2))
def arrow(b, color, lw=1.7):
    ax.annotate("", xy=b, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0))
k = 0.22
forces = [(5, 0, "5 N"), (10, 90, "10 N"), (15, 180, "15 N"), (20, 270, "20 N")]
for F, a, lab in forces:
    t = np.radians(a)
    tip = (k*F*np.cos(t), k*F*np.sin(t))
    arrow(tip, MUTED)
    ax.text(tip[0]*1.13 - 0.22*(a == 180), tip[1]*1.10 + 0.10*(a == 0),
            lab, color=INK, fontsize=9)
X, Y = 5 - 15, 10 - 20
tip = (k*X, k*Y)
arrow(tip, ACCENT, lw=2.3)
ax.plot([0], [0], "o", color=INK, ms=4)
ax.text(tip[0] - 0.30, tip[1] - 0.62, "$R = 10\\sqrt{2}$ N",
        color=ACCENT, fontsize=10, ha="center")
ax.text(0.22, 0.28, "$O$", color=INK, fontsize=10)
ax.set_xlim(-4.2, 2.1); ax.set_ylim(-4.9, 2.7)
ax.set_aspect("equal"); ax.axis("off")
```

::: example Worked example 21.7 — three forces at awkward angles
Three forces of 4 N, 3 N and 2 N act at a point, in directions making $0^\circ$,
$60^\circ$ and $150^\circ$ with the positive $x$-axis. Find the resultant.

**Solution.** Work out each component separately, to four decimal places, and only
round at the end.

For the $x$-components:
$$ X = 4\cos 0^\circ + 3\cos 60^\circ + 2\cos 150^\circ = 4 + 1.5 - 1.7321 = 3.7679 $$

For the $y$-components:
$$ Y = 4\sin 0^\circ + 3\sin 60^\circ + 2\sin 150^\circ = 0 + 2.5981 + 1 = 3.5981 $$

The magnitude of the resultant is
$$ R = \sqrt{(3.7679)^2 + (3.5981)^2} = \sqrt{14.197 + 12.946} = \sqrt{27.143} = 5.21\ \text{N} $$

Since both components are positive the resultant is in the first quadrant:
$$ \theta = \tan^{-1}\!\left(\frac{3.5981}{3.7679}\right) = \tan^{-1}(0.9549) = 43.68^\circ $$

The resultant is **5.21 N at $43^\circ 41'$ to the $x$-axis**.
:::

::: example Worked example 21.8 — three equal forces in equilibrium
Three forces, each of magnitude 10 N, act at a point in directions making $0^\circ$,
$120^\circ$ and $240^\circ$ with the $x$-axis. Show that they are in equilibrium.

**Solution.** Compute the two component sums.

Horizontally, using $\cos 120^\circ = \cos 240^\circ = -\tfrac{1}{2}$:
$$ X = 10(1) + 10\left(-\tfrac{1}{2}\right) + 10\left(-\tfrac{1}{2}\right) = 10 - 5 - 5 = 0 $$

Vertically, using $\sin 120^\circ = \tfrac{\sqrt{3}}{2}$ and
$\sin 240^\circ = -\tfrac{\sqrt{3}}{2}$:
$$ Y = 0 + 10\left(\tfrac{\sqrt{3}}{2}\right) + 10\left(-\tfrac{\sqrt{3}}{2}\right) = 0 $$

Both sums vanish, so $R = 0$ and the three forces are in equilibrium. Geometrically
they form a closed equilateral triangle when drawn head to tail, which is the
triangle law in action.
:::

::: example Worked example 21.9 — finding an unknown force for equilibrium
A particle is in equilibrium under three forces. Two of them are 6 N due east and
8 N due north. Find the third force.

**Solution.** For equilibrium the sum of all three forces is zero, so the third
force is the **equal and opposite** of the resultant of the first two.

The resultant of the given pair, which are perpendicular, is
$$ R = \sqrt{6^2 + 8^2} = \sqrt{100} = 10\ \text{N} $$

Its direction from east is
$$ \tan\theta = \frac{8}{6} = 1.3333 \quad\Longrightarrow\quad \theta = 53^\circ 8' $$

so this resultant is 10 N at $53^\circ 8'$ north of east. The third force must
therefore be **10 N at $53^\circ 8'$ south of west**, i.e. along the bearing
$233^\circ 8'$ measured from the positive $x$-axis. Such a balancing force is called
the **equilibrant** of the other two.
:::

::: tip The equilibrant
The equilibrant of a set of forces is equal in magnitude to their resultant but
opposite in direction. Every equilibrium question is a resultant question with a
minus sign, so learn one method and you have both.
:::

## 21.3 Dynamics: motion of a particle in a straight line; motion with uniform acceleration

### The three quantities, and how calculus links them

A **particle** is a body small enough that its size can be ignored. Restrict it to a
straight line and take a fixed point $O$ on that line as origin. Then a single
number describes where the particle is.

::: definition Displacement, velocity, acceleration
**Displacement** $s$ is the directed distance from $O$, positive one way and
negative the other. **Velocity** is the rate of change of displacement and
**acceleration** is the rate of change of velocity:
$$ v = \frac{ds}{dt}, \qquad a = \frac{dv}{dt} = \frac{d^2s}{dt^2} $$
:::

Distance and displacement are not the same. A particle that goes 5 m forward and 5 m
back has travelled a distance of 10 m but has displacement 0. Likewise speed is the
magnitude of velocity: velocity can be negative, speed never is.

Because $v = ds/dt$, everything from Unit 18 transfers directly. The particle is
**momentarily at rest** when $v = 0$; it **reverses direction** where $v$ changes
sign; its velocity is greatest where $a = 0$ and changes from positive to negative.

::: example Worked example 21.10 — motion given by a formula
A particle moves along a straight line so that its displacement after $t$ seconds is
$s = t^3 - 6t^2 + 9t$ metres. Find its velocity and acceleration, the times at which
it is momentarily at rest, and the total distance travelled in the first 4 seconds.

**Solution.** Differentiate once for the velocity:
$$ v = \frac{ds}{dt} = 3t^2 - 12t + 9 $$

Differentiate again for the acceleration:
$$ a = \frac{dv}{dt} = 6t - 12 $$

The particle is at rest when $v = 0$:
$$ 3t^2 - 12t + 9 = 0 \;\Longrightarrow\; 3(t^2 - 4t + 3) = 0 \;\Longrightarrow\; 3(t-1)(t-3) = 0 $$

so $t = 1\ \text{s}$ and $t = 3\ \text{s}$. At those instants
$a = 6(1) - 12 = -6\ \text{m/s}^2$ and $a = 6(3) - 12 = +6\ \text{m/s}^2$.

For the distance, the particle turns round at $t = 1$ and $t = 3$, so compute the
displacement at each of $t = 0, 1, 3, 4$:
$$ s(0) = 0, \quad s(1) = 1 - 6 + 9 = 4, \quad s(3) = 27 - 54 + 27 = 0, \quad s(4) = 64 - 96 + 36 = 4 $$

Add the magnitudes of the three legs:
$$ |4 - 0| + |0 - 4| + |4 - 0| = 4 + 4 + 4 = 12\ \text{m} $$

The total distance travelled is **12 m**, although the displacement after 4 s is
only 4 m.
:::

### The equations of uniformly accelerated motion

If the acceleration is **constant**, the calculus can be done once and for all. Let
$u$ be the velocity at $t = 0$, $v$ the velocity at time $t$, $a$ the constant
acceleration, and $s$ the displacement in that time.

::: key The four equations of motion (constant acceleration only)
$$ v = u + at $$
$$ s = ut + \tfrac{1}{2}at^2 $$
$$ v^2 = u^2 + 2as $$
$$ s = \left(\frac{u+v}{2}\right)t $$
Distance travelled in the $n$-th second:
$\ s_n = u + \dfrac{a(2n-1)}{2}$.
:::

::: derivation The first three equations from calculus
Start from $a = dv/dt$ with $a$ constant and integrate with respect to $t$:
$$ v = \int a\,dt = at + C $$

At $t = 0$ the velocity is $u$, so $C = u$ and
$$ v = u + at $$

which is the first equation. Now write $v = ds/dt$ and integrate again:
$$ s = \int (u + at)\,dt = ut + \tfrac{1}{2}at^2 + C_1 $$

Measuring $s$ from the starting point makes $s = 0$ at $t = 0$, so $C_1 = 0$ and
$$ s = ut + \tfrac{1}{2}at^2 $$

For the third equation, eliminate $t$. From the first equation $t = (v-u)/a$.
Substituting into the second,
$$ s = u\left(\frac{v-u}{a}\right) + \frac{1}{2}a\left(\frac{v-u}{a}\right)^2 = \frac{uv - u^2}{a} + \frac{(v-u)^2}{2a} $$

Multiply through by $2a$ and expand the square:
$$ 2as = 2uv - 2u^2 + v^2 - 2uv + u^2 = v^2 - u^2 $$

Hence $v^2 = u^2 + 2as$.
:::

::: caution Use them only when $a$ is constant
These four equations are valid **only** for uniform acceleration. If the
acceleration varies with time, go back to $v = ds/dt$ and $a = dv/dt$ and use
calculus, as in Worked example 21.10. Also keep the signs consistent: if you take
the direction of motion as positive, a retardation of $2\ \text{m/s}^2$ enters the
equations as $a = -2\ \text{m/s}^2$.
:::

The **velocity-time graph** makes the equations visible. For constant acceleration
it is a straight line of gradient $a$ and intercept $u$; the area under it between
two times is the displacement, and for a trapezium that area is
$\tfrac{1}{2}(u+v)t$ — the fourth equation.

```figure caption="Velocity-time graph for uniform acceleration. The gradient is $a$; the shaded trapezium has area $\frac{1}{2}(u+v)t$, which is the displacement."
import numpy as np
fig, ax = plt.subplots(figsize=(4.8, 2.9))
u, a, T = 4.0, 1.6, 5.0
t = np.linspace(0, T, 200)
v = u + a*t
ax.plot(t, v, color=ACCENT, lw=2.0)
ax.fill_between(t, 0, v, color=ACCENT, alpha=0.14)
ax.plot([0, T], [u, u], ls=":", color=MUTED, lw=1.0)
ax.plot([T, T], [u, u + a*T], ls=":", color=MUTED, lw=1.0)
ax.text(T + 0.12, u + a*T*0.5, "$at$", color=MUTED, fontsize=10)
ax.text(T*0.42, u*0.42, "area $= s$", color=INK, fontsize=10)
ax.text(T*0.20, u + a*T*0.20 + 0.60, "gradient $= a$",
        color=ACCENT, fontsize=10)
ax.set_xlim(0, T + 0.9); ax.set_ylim(0, u + a*T + 1.6)
ax.set_xticks([0, T]); ax.set_xticklabels(["$0$", "$t$"])
ax.set_yticks([u, u + a*T]); ax.set_yticklabels(["$u$", "$v$"])
ax.set_xlabel("time")
ax.set_ylabel("velocity")
ax.grid(True, color=GRID, lw=0.6, alpha=0.7)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
```

::: example Worked example 21.11 — a car accelerating from rest
A car starts from rest and accelerates uniformly at $2\ \text{m/s}^2$. Find its
velocity after 10 s and the distance covered in that time.

**Solution.** Here $u = 0$, $a = 2\ \text{m/s}^2$, $t = 10\ \text{s}$.

From $v = u + at$:
$$ v = 0 + 2(10) = 20\ \text{m/s} $$

From $s = ut + \tfrac{1}{2}at^2$:
$$ s = 0 + \tfrac{1}{2}(2)(10)^2 = 100\ \text{m} $$

The car reaches **20 m/s** and covers **100 m**. Check with the third equation:
$v^2 = 0 + 2(2)(100) = 400$, so $v = 20$ m/s. Consistent.
:::

::: example Worked example 21.12 — a train being braked
A train moving at $72\ \text{km/h}$ is brought to rest in 200 m by a uniform
retardation. Find the retardation and the time taken.

**Solution.** Convert the speed to SI units first, multiplying by $\tfrac{5}{18}$:
$$ u = 72 \times \frac{5}{18} = 20\ \text{m/s} $$

The train stops, so $v = 0$ and $s = 200$ m. Use $v^2 = u^2 + 2as$:
$$ 0 = 20^2 + 2a(200) = 400 + 400a $$

Solving for $a$:
$$ a = -\frac{400}{400} = -1\ \text{m/s}^2 $$

The negative sign means deceleration, so the retardation is $1\ \text{m/s}^2$. For
the time use $v = u + at$:
$$ 0 = 20 + (-1)t \quad\Longrightarrow\quad t = 20\ \text{s} $$

The retardation is **$1\ \text{m/s}^2$** and the train takes **20 s** to stop.
:::

::: example Worked example 21.13 — distance in a particular second
A particle starts with velocity $5\ \text{m/s}$ and moves with uniform acceleration
$2\ \text{m/s}^2$. Find the distance it covers during the 4th second.

**Solution.** Use the $n$-th second formula with $u = 5$, $a = 2$, $n = 4$:
$$ s_4 = u + \frac{a(2n-1)}{2} = 5 + \frac{2(2 \times 4 - 1)}{2} = 5 + \frac{2 \times 7}{2} = 5 + 7 = 12\ \text{m} $$

The particle covers **12 m** during the 4th second.

The formula is just a difference of two displacements. Checking directly,
$s(4) = 5(4) + \tfrac{1}{2}(2)(16) = 36$ m and
$s(3) = 5(3) + \tfrac{1}{2}(2)(9) = 24$ m, and $36 - 24 = 12$ m. Same answer.
:::

## 21.4 Motion under gravity; motion down a smooth inclined plane

### Free vertical motion

Near the surface of the earth every body, whatever its mass, falls with the same
constant acceleration $g = 9.8\ \text{m/s}^2$ directed downwards, provided air
resistance is ignored. Constant acceleration means the four equations of §21.3 apply
with $a = \pm g$; only the sign needs care.

::: key Sign convention for vertical motion
Choose **one** positive direction and keep it.

- Taking **upwards positive**: $a = -g$ for the whole flight, up and down.
- Taking **downwards positive** (convenient for a body simply dropped): $a = +g$.

A body **dropped** has $u = 0$; a body **thrown** has $u \neq 0$. At the highest
point the velocity is zero but the acceleration is still $g$ downwards.
:::

Two standard results follow from taking upwards as positive with $a = -g$. At the
greatest height $v = 0$, so $0 = u^2 - 2gH$ gives the **maximum height**
$H = u^2/(2g)$; and putting $s = 0$ in $s = ut - \tfrac{1}{2}gt^2$ gives
$t(u - \tfrac{1}{2}gt) = 0$, so the **total time of flight** back to the starting
level is $t = 2u/g$, exactly twice the time to rise.

```figure caption="A stone thrown up at $19.6$ m/s: height against time is a parabola, peaking at $19.6$ m after $2$ s and returning after $4$ s."
import numpy as np
fig, ax = plt.subplots(figsize=(4.8, 3.0))
g, u = 9.8, 19.6
t = np.linspace(0, 2*u/g, 300)
h = u*t - 0.5*g*t**2
ax.plot(t, h, color=ACCENT, lw=2.0)
tp, hp = u/g, u**2/(2*g)
ax.plot([tp], [hp], "o", color=ACCENT, ms=6)
ax.plot([tp, tp], [0, hp], ls=":", color=MUTED, lw=1.0)
ax.plot([0, tp], [hp, hp], ls=":", color=MUTED, lw=1.0)
ax.annotate("highest point, $v = 0$", xy=(tp, hp), xytext=(-30, -34),
            textcoords="offset points", color=INK, fontsize=9,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
ax.plot([2*u/g], [0], "o", color=SERIES[1], ms=5)
ax.annotate("back at start, $v = -19.6$ m/s", xy=(2*u/g, 0), xytext=(-116, 16),
            textcoords="offset points", color=SERIES[1], fontsize=9,
            arrowprops=dict(arrowstyle="->", color=SERIES[1], lw=0.9))
ax.set_xlim(0, 4.75); ax.set_ylim(0, 25.5)
ax.set_xticks([0, 1, 2, 3, 4])
ax.set_yticks([0, 9.8, 19.6])
ax.set_yticklabels(["$0$", "$9.8$", "$19.6$"])
ax.set_xlabel("time $t$ (s)")
ax.set_ylabel("height $h$ (m)")
ax.grid(True, color=GRID, lw=0.6, alpha=0.7)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
```

::: example Worked example 21.14 — a stone thrown vertically up
A stone is thrown vertically upwards with a velocity of $19.6\ \text{m/s}$. Find the
time to reach the greatest height, the greatest height, and the total time before it
returns to the thrower's hand. Take $g = 9.8\ \text{m/s}^2$.

**Solution.** Take upwards as positive, so $u = 19.6\ \text{m/s}$ and
$a = -9.8\ \text{m/s}^2$.

At the greatest height $v = 0$, so from $v = u + at$:
$$ 0 = 19.6 - 9.8t \quad\Longrightarrow\quad t = \frac{19.6}{9.8} = 2\ \text{s} $$

For the greatest height use $v^2 = u^2 + 2as$ with $v = 0$:
$$ 0 = (19.6)^2 - 2(9.8)H \quad\Longrightarrow\quad H = \frac{384.16}{19.6} = 19.6\ \text{m} $$

The upward and downward journeys take equal times, so the total time of flight is
$$ T = 2 \times 2 = 4\ \text{s} $$

The stone rises **19.6 m in 2 s** and is back after **4 s**, arriving with speed
19.6 m/s downwards.
:::

::: example Worked example 21.15 — a body dropped from a height
A ball is dropped from the top of a tower 78.4 m high. Find the time it takes to
reach the ground and its velocity on striking the ground.

**Solution.** The ball is dropped, so $u = 0$. Take downwards as positive, giving
$a = +9.8\ \text{m/s}^2$ and $s = 78.4$ m.

From $s = ut + \tfrac{1}{2}at^2$:
$$ 78.4 = 0 + \tfrac{1}{2}(9.8)t^2 = 4.9t^2 $$

Solving for $t$:
$$ t^2 = \frac{78.4}{4.9} = 16 \quad\Longrightarrow\quad t = 4\ \text{s} $$

From $v = u + at$:
$$ v = 0 + 9.8(4) = 39.2\ \text{m/s} $$

The ball lands after **4 s** at **39.2 m/s**. (Check with $v^2 = 2gs$:
$v = \sqrt{2(9.8)(78.4)} = \sqrt{1536.6} = 39.2$ m/s.)
:::

### Motion down a smooth inclined plane

Let a particle of mass $m$ rest on a plane inclined at angle $\theta$ to the
horizontal. Two forces act on it: its weight $mg$ vertically downwards, and the
**normal reaction** $N$ perpendicular to the plane. **Smooth** means there is no
friction, so no force acts along the plane except the component of the weight.

Resolve the weight along and perpendicular to the plane — not horizontally and
vertically. The component along the plane, pointing down the slope, is
$mg\sin\theta$; the component pressing into the plane is $mg\cos\theta$.

```figure caption="A particle on a smooth plane of inclination $\theta$. The weight resolves into $mg\sin\theta$ down the slope and $mg\cos\theta$ into the plane, balanced by $N$."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0, 3.0))
th = np.radians(30.0)
L = 6.0
ax.plot([0, L], [0, 0], color=INK, lw=1.4)
ax.plot([0, L*np.cos(th)], [0, L*np.cos(th)*np.tan(th)], color=INK, lw=1.8)
ax.plot([L*np.cos(th), L*np.cos(th)], [0, L*np.cos(th)*np.tan(th)],
        color=MUTED, lw=1.0, ls="--")
# particle at 70% up the slope
f = 0.62
P = np.array([L*f*np.cos(th), L*f*np.sin(th)])
# offset the block slightly above the surface
n = np.array([-np.sin(th), np.cos(th)])
C = P + 0.14*n
ax.plot([C[0]], [C[1]], "s", color=ACCENT, ms=9)
def arrow(a, b, color, lw=1.6):
    ax.annotate("", xy=b, xytext=a,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0))
W = 1.55
down = C + np.array([0.0, -W])
arrow(C, down, SERIES[3])
ax.text(down[0] + 0.14, down[1] - 0.36, "$mg$", color=SERIES[3], fontsize=10)
# component along the plane (down the slope)
d = np.array([-np.cos(th), -np.sin(th)])
arrow(C, C + W*np.sin(th)*d*1.0, SERIES[1])
ax.text((C + W*np.sin(th)*d)[0] - 0.95, (C + W*np.sin(th)*d)[1] + 0.16,
        r"$mg\sin\theta$", color=SERIES[1], fontsize=10)
# component into the plane
arrow(C, C - W*np.cos(th)*n, SERIES[2])
ax.text((C - W*np.cos(th)*n)[0] + 0.12, (C - W*np.cos(th)*n)[1] - 0.30,
        r"$mg\cos\theta$", color=SERIES[2], fontsize=10)
# normal reaction
arrow(C, C + W*np.cos(th)*n, ACCENT)
ax.text((C + W*np.cos(th)*n)[0] - 0.62, (C + W*np.cos(th)*n)[1] + 0.12,
        "$N$", color=ACCENT, fontsize=11)
t = np.linspace(0, th, 60)
ax.plot(1.25*np.cos(t), 1.25*np.sin(t), color=MUTED, lw=0.9)
ax.text(1.45*np.cos(th/2), 1.45*np.sin(th/2) - 0.16, r"$\theta$", color=INK, fontsize=10)
ax.set_xlim(-0.5, 6.5); ax.set_ylim(-1.05, 4.25)
ax.set_aspect("equal"); ax.axis("off")
```

Perpendicular to the plane the particle does not move, so $N = mg\cos\theta$. Along
the plane the only force is $mg\sin\theta$, so by Newton's second law
$ma = mg\sin\theta$, and the mass cancels.

::: key Motion on a smooth inclined plane
A particle sliding freely on a smooth plane of inclination $\theta$ has acceleration
$$ a = g\sin\theta $$
down the slope, **independent of its mass**. Starting from rest and sliding a
distance $l$ along the plane,
$$ v = \sqrt{2gl\sin\theta}, \qquad t = \sqrt{\frac{2l}{g\sin\theta}} $$
Since $l\sin\theta = h$, the vertical drop, this gives $v = \sqrt{2gh}$ — the same
speed as a free fall through the same height.
:::

::: tip Two useful checks
When $\theta = 90^\circ$ the plane is vertical and $a = g\sin 90^\circ = g$, free
fall. When $\theta = 0^\circ$ the plane is horizontal and $a = 0$, no motion. Any
formula for an inclined plane that fails these two checks is wrong.
:::

::: example Worked example 21.16 — sliding down a smooth slope
A body slides from rest down a smooth plane inclined at $30^\circ$ to the horizontal.
Find its acceleration, and its speed and the time taken after sliding 20 m along the
plane. Take $g = 9.8\ \text{m/s}^2$.

**Solution.** The acceleration down the slope is
$$ a = g\sin\theta = 9.8 \times \sin 30^\circ = 9.8 \times 0.5 = 4.9\ \text{m/s}^2 $$

With $u = 0$ and $s = 20$ m, use $v^2 = u^2 + 2as$:
$$ v^2 = 0 + 2(4.9)(20) = 196 \quad\Longrightarrow\quad v = 14\ \text{m/s} $$

For the time use $v = u + at$:
$$ 14 = 0 + 4.9t \quad\Longrightarrow\quad t = \frac{14}{4.9} = 2.86\ \text{s} $$

The acceleration is **$4.9\ \text{m/s}^2$**, the speed after 20 m is **14 m/s**, and
it takes **2.86 s**. Notice the mass was never needed.
:::

::: example Worked example 21.17 — given the vertical height
A smooth plane of inclination $30^\circ$ has vertical height 4.9 m. A particle slides
from rest at the top. Find the length of the slope, the time of descent and the speed
at the bottom.

**Solution.** The length $l$ of the slope satisfies $h = l\sin\theta$, so
$$ l = \frac{h}{\sin 30^\circ} = \frac{4.9}{0.5} = 9.8\ \text{m} $$

The acceleration is $a = g\sin 30^\circ = 4.9\ \text{m/s}^2$. With $u = 0$,
from $l = \tfrac{1}{2}at^2$:
$$ 9.8 = \tfrac{1}{2}(4.9)t^2 = 2.45t^2 \quad\Longrightarrow\quad t^2 = 4 \quad\Longrightarrow\quad t = 2\ \text{s} $$

The speed at the bottom follows from $v = u + at$:
$$ v = 0 + 4.9(2) = 9.8\ \text{m/s} $$

The slope is **9.8 m** long, the descent takes **2 s**, and the particle arrives at
**9.8 m/s**. As predicted, $\sqrt{2gh} = \sqrt{2(9.8)(4.9)} = \sqrt{96.04} = 9.8$
m/s — the same speed as falling 4.9 m freely, but reached in 2 s instead of 1 s.
:::

::: example Worked example 21.18 — finding the inclination
A particle slides 9.8 m from rest down a smooth inclined plane in 2 s. Find the
inclination of the plane.

**Solution.** Let the inclination be $\theta$, so $a = g\sin\theta = 9.8\sin\theta$.
With $u = 0$, $s = 9.8$ m and $t = 2$ s, use $s = \tfrac{1}{2}at^2$:
$$ 9.8 = \tfrac{1}{2}(9.8\sin\theta)(2)^2 = 19.6\sin\theta $$

Solving for the sine:
$$ \sin\theta = \frac{9.8}{19.6} = \frac{1}{2} \quad\Longrightarrow\quad \theta = 30^\circ $$

The plane is inclined at **$30^\circ$** to the horizontal.
:::

::: memory Everything in this unit, in six lines
- Two forces: $R^2 = P^2+Q^2+2PQ\cos\theta$, $\ \tan\alpha = \dfrac{Q\sin\theta}{P+Q\cos\theta}$
- Many forces: $R = \sqrt{X^2+Y^2}$; equilibrium means $X = 0$ **and** $Y = 0$
- Lami: each force over the sine of the angle between the other two
- Calculus: $v = \dfrac{ds}{dt}$, $\ a = \dfrac{dv}{dt}$
- Uniform $a$: $v = u+at$, $\ s = ut+\tfrac{1}{2}at^2$, $\ v^2 = u^2+2as$
- Gravity $a = \pm g$; smooth incline $a = g\sin\theta$, $\ N = mg\cos\theta$
:::

## Chapter summary

- A force is a vector: magnitude, direction, point of application. Forces at a point
  are **concurrent**; forces in one plane are **coplanar**.
- **Parallelogram law**: two forces $P$, $Q$ at angle $\theta$ have resultant
  $R = \sqrt{P^2+Q^2+2PQ\cos\theta}$ making angle
  $\alpha = \tan^{-1}\dfrac{Q\sin\theta}{P+Q\cos\theta}$ with $P$.
- The resultant always lies between $|P-Q|$ and $P+Q$; it equals $P+Q$ at
  $\theta = 0^\circ$, $\sqrt{P^2+Q^2}$ at $90^\circ$, $|P-Q|$ at $180^\circ$.
- **Resolution**: $F_x = F\cos\theta$, $F_y = F\sin\theta$. Any number of coplanar
  concurrent forces combine as $X = \sum F\cos\theta$, $Y = \sum F\sin\theta$,
  $R = \sqrt{X^2+Y^2}$, $\tan\theta = Y/X$; read the quadrant from the signs.
- **Equilibrium** $\Leftrightarrow X = 0$ and $Y = 0$. For three forces use
  **Lami's theorem**: each force divided by the sine of the angle between the other
  two is the same. The **equilibrant** is minus the resultant.
- **Kinematics**: $v = ds/dt$, $a = dv/dt = d^2s/dt^2$. Distance is not
  displacement; reverse of direction happens where $v$ changes sign.
- **Uniform acceleration only**: $v = u+at$, $s = ut+\tfrac12 at^2$,
  $v^2 = u^2+2as$, $s = \tfrac12(u+v)t$, and $s_n = u + \tfrac{a(2n-1)}{2}$.
  On a $v$–$t$ graph the gradient is $a$ and the area is $s$.
- **Gravity**: $a = -g$ upwards positive, $a = +g$ downwards positive, with
  $g = 9.8\ \text{m/s}^2$. Maximum height $u^2/2g$, time of flight $2u/g$.
- **Smooth inclined plane**: $a = g\sin\theta$ down the slope (mass cancels) and
  $N = mg\cos\theta$. Speed after a vertical drop $h$ is $\sqrt{2gh}$, the same as
  in free fall.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The greatest possible resultant of two forces of 8 N and 6 N is <span class="marks">[1]</span>
   (a) $2$ N (b) $10$ N (c) $14$ N (d) $48$ N
2. Two forces, each of 5 N, act at a point at $120^\circ$. Their resultant is <span class="marks">[1]</span>
   (a) $0$ (b) $5$ N (c) $5\sqrt{3}$ N (d) $10$ N
3. Coplanar concurrent forces are in equilibrium if and only if <span class="marks">[1]</span>
   (a) $X = 0$ only (b) $Y = 0$ only (c) $X = 0$ and $Y = 0$ (d) $X = Y$
4. In Lami's theorem each force is divided by the sine of the angle <span class="marks">[1]</span>
   (a) it makes with the vertical (b) between the other two forces
   (c) between it and the next force (d) of $90^\circ$
5. A body dropped from rest falls, in the first second, a distance of
   (take $g = 9.8\ \text{m/s}^2$) <span class="marks">[1]</span>
   (a) $4.9$ m (b) $9.8$ m (c) $19.6$ m (d) $2.45$ m
6. If $s = 4t^2$, the velocity at $t = 3$ s is <span class="marks">[1]</span>
   (a) $12$ m/s (b) $24$ m/s (c) $36$ m/s (d) $8$ m/s
7. At the highest point of the path of a stone thrown vertically upwards <span class="marks">[1]</span>
   (a) $v = 0$ and $a = 0$ (b) $v = 0$ and $a = g$ downwards
   (c) $v = g$ and $a = 0$ (d) both $v$ and $a$ are upwards
8. The acceleration of a particle sliding freely down a smooth plane inclined at
   $30^\circ$ is <span class="marks">[1]</span>
   (a) $9.8\ \text{m/s}^2$ (b) $4.9\ \text{m/s}^2$ (c) $8.49\ \text{m/s}^2$
   (d) it depends on the mass

::: note Answers to Group A
**1.** (c) — the resultant is greatest when $\theta = 0^\circ$, giving
$8 + 6 = 14$ N.

**2.** (b) — $R = \sqrt{25+25+2(25)\cos 120^\circ} = \sqrt{50-25} = 5$ N.

**3.** (c) — the resultant $\sqrt{X^2+Y^2}$ vanishes only when **both** component
sums vanish.

**4.** (b) — that is the statement of the theorem; the angles used sum to
$360^\circ$.

**5.** (a) — $s = \tfrac12 gt^2 = \tfrac12(9.8)(1)^2 = 4.9$ m.

**6.** (b) — $v = ds/dt = 8t$, so $v(3) = 24$ m/s.

**7.** (b) — the velocity is momentarily zero but gravity never switches off.

**8.** (b) — $a = g\sin 30^\circ = 9.8 \times 0.5 = 4.9\ \text{m/s}^2$,
independent of mass.
:::

**Group B — Short answer (5 marks each)**

1. Forces of 4 N and 7 N act at a point with $60^\circ$ between them. Find the
   magnitude and direction of the resultant. <span class="marks">[5]</span>
2. The resultant of two forces $P$ and $2P$ acting at a point is perpendicular to
   $P$. Find the angle between the forces and the magnitude of the
   resultant. <span class="marks">[5]</span>
3. Three forces of 5 N, 10 N and 15 N act at a point in directions making $0^\circ$,
   $120^\circ$ and $240^\circ$ with the $x$-axis. Find their
   resultant. <span class="marks">[5]</span>
4. A particle moves so that $s = 2t^3 - 9t^2 + 12t$ metres. Find when it is at rest,
   and the total distance it travels in the first 3 seconds. <span class="marks">[5]</span>
5. A ball is thrown vertically upwards with velocity $24.5\ \text{m/s}$. Find the
   greatest height reached and the total time of flight.
   ($g = 9.8\ \text{m/s}^2$) <span class="marks">[5]</span>
6. A particle slides from rest down a smooth plane of inclination $45^\circ$ and
   length 10 m. Find the acceleration, the speed at the bottom and the time
   taken. <span class="marks">[5]</span>

::: note Solutions to Group B
**1.** With $P = 4$, $Q = 7$, $\theta = 60^\circ$:
$$ R = \sqrt{4^2 + 7^2 + 2(4)(7)(0.5)} = \sqrt{16+49+28} = \sqrt{93} = 9.64\ \text{N} $$
For the direction from the 4 N force,
$$ \tan\alpha = \frac{7\sin 60^\circ}{4 + 7\cos 60^\circ} = \frac{6.062}{7.5} = 0.8083 $$
so $\alpha = 38.95^\circ = 38^\circ 57'$. The resultant is $9.64$ N at
$38^\circ 57'$ to the 4 N force.

**2.** Take $P$ along the $x$-axis. The resultant is perpendicular to $P$ exactly
when its $x$-component is zero:
$$ X = P + 2P\cos\theta = 0 \;\Longrightarrow\; \cos\theta = -\tfrac12 \;\Longrightarrow\; \theta = 120^\circ $$
The resultant is then purely the $y$-component,
$$ R = 2P\sin 120^\circ = 2P\left(\tfrac{\sqrt{3}}{2}\right) = \sqrt{3}\,P $$
So the angle is $120^\circ$ and $R = \sqrt{3}P$.

**3.** Components, using $\cos 120^\circ = \cos 240^\circ = -\tfrac12$,
$\sin 120^\circ = \tfrac{\sqrt{3}}{2}$, $\sin 240^\circ = -\tfrac{\sqrt{3}}{2}$:
$$ X = 5 - 5 - 7.5 = -7.5, \qquad Y = 0 + 8.660 - 12.990 = -4.330 $$
Hence
$$ R = \sqrt{56.25 + 18.75} = \sqrt{75} = 5\sqrt{3} = 8.66\ \text{N} $$
and $\tan\theta = (-4.330)/(-7.5) = 0.5774$ with both components negative, so the
resultant lies in the third quadrant:
$\theta = 180^\circ + 30^\circ = 210^\circ$. The resultant is $5\sqrt{3}$ N at
$210^\circ$ to the $x$-axis.

**4.** Differentiating, $v = 6t^2 - 18t + 12 = 6(t-1)(t-2)$, so the particle is at
rest at $t = 1$ s and $t = 2$ s. The displacements at the turning times and the end
points are
$$ s(0) = 0, \quad s(1) = 5, \quad s(2) = 4, \quad s(3) = 9 $$
Adding the magnitudes of the three legs,
$$ |5-0| + |4-5| + |9-4| = 5 + 1 + 5 = 11\ \text{m} $$
Total distance $= 11$ m (while the displacement is only 9 m).

**5.** Upwards positive: $u = 24.5$, $a = -9.8$. At the top $v = 0$, so from
$v^2 = u^2 + 2as$,
$$ H = \frac{u^2}{2g} = \frac{(24.5)^2}{2(9.8)} = \frac{600.25}{19.6} = 30.63\ \text{m} $$
The time of flight is
$$ T = \frac{2u}{g} = \frac{2(24.5)}{9.8} = 5\ \text{s} $$
Greatest height $30.63$ m, time of flight $5$ s (rising for $2.5$ s).

**6.** The acceleration down the slope is
$$ a = g\sin 45^\circ = 9.8 \times 0.7071 = 6.93\ \text{m/s}^2 $$
With $u = 0$ and $s = 10$ m, from $v^2 = 2as$,
$$ v = \sqrt{2(6.93)(10)} = \sqrt{138.6} = 11.77\ \text{m/s} $$
and from $v = at$,
$$ t = \frac{11.77}{6.93} = 1.70\ \text{s} $$
:::

**Group C — Long answer (8 marks each)**

1. State the parallelogram law of forces and derive expressions for the magnitude
   and the direction of the resultant of two forces $P$ and $Q$ inclined at an angle
   $\theta$. Hence find two forces whose magnitudes are in the ratio $3:5$, act at
   $60^\circ$ to each other and have a resultant of 35 N. <span class="marks">[8]</span>
2. Starting from the definitions $v = ds/dt$ and $a = dv/dt$, derive the equations
   $v = u+at$, $s = ut+\tfrac12 at^2$ and $v^2 = u^2+2as$ for constant acceleration.
   A train starts from rest, accelerates uniformly at $1\ \text{m/s}^2$ for 20 s,
   runs at constant speed for 60 s, and is then brought to rest by a uniform
   retardation of $2\ \text{m/s}^2$. Find the total distance
   travelled. <span class="marks">[8]</span>
3. Show that a particle sliding freely on a smooth plane of inclination $\theta$ has
   acceleration $g\sin\theta$ down the plane and that the normal reaction is
   $mg\cos\theta$. A body slides from rest down a smooth plane of inclination
   $30^\circ$ whose vertical height is 10 m. Find the speed at the bottom and the
   time taken, and compare the speed with that of a body falling freely through
   10 m. <span class="marks">[8]</span>

::: note Solutions to Group C
**1. Statement.** If two forces acting at a point are represented in magnitude and
direction by the two adjacent sides of a parallelogram drawn from that point, their
resultant is represented by the diagonal of the parallelogram through that point.

**Derivation.** Put $O$ at the origin with $P$ along the $x$-axis, so
$\vec P = (P, 0)$ and $\vec Q = (Q\cos\theta,\ Q\sin\theta)$. Adding,
$$ \vec R = (P + Q\cos\theta,\ Q\sin\theta) $$
Squaring and adding the components,
$$ R^2 = (P+Q\cos\theta)^2 + Q^2\sin^2\theta = P^2 + 2PQ\cos\theta + Q^2(\cos^2\theta+\sin^2\theta) $$
so, using $\cos^2\theta+\sin^2\theta = 1$,
$$ R = \sqrt{P^2 + Q^2 + 2PQ\cos\theta} $$
and the angle $\alpha$ the resultant makes with $P$ satisfies
$$ \tan\alpha = \frac{Q\sin\theta}{P+Q\cos\theta} $$

**Application.** Let the forces be $3k$ and $5k$. Then with $\theta = 60^\circ$,
$$ R^2 = 9k^2 + 25k^2 + 2(3k)(5k)\left(\tfrac12\right) = 9k^2+25k^2+15k^2 = 49k^2 $$
so $R = 7k$. Given $R = 35$ N,
$$ 7k = 35 \;\Longrightarrow\; k = 5 $$
The forces are $3(5) = 15$ N and $5(5) = 25$ N.

**2. Derivation.** With $a$ constant, integrating $a = dv/dt$ gives $v = at + C$,
and $v = u$ at $t = 0$ forces $C = u$, so
$$ v = u + at $$
Integrating $v = ds/dt$ next,
$$ s = \int (u+at)\,dt = ut + \tfrac12 at^2 + C_1 $$
and measuring $s$ from the start gives $C_1 = 0$, so $s = ut + \tfrac12 at^2$.
Eliminating $t = (v-u)/a$ from this,
$$ 2as = 2u(v-u) + (v-u)^2 = 2uv - 2u^2 + v^2 - 2uv + u^2 = v^2 - u^2 $$
hence $v^2 = u^2 + 2as$.

**Application.** *Phase 1* ($u = 0$, $a = 1$, $t = 20$):
$$ v = 0 + 1(20) = 20\ \text{m/s}, \qquad s_1 = 0 + \tfrac12(1)(20)^2 = 200\ \text{m} $$
*Phase 2* (constant $20$ m/s for 60 s):
$$ s_2 = 20 \times 60 = 1200\ \text{m} $$
*Phase 3* ($u = 20$, $v = 0$, $a = -2$): from $v^2 = u^2+2as$,
$$ 0 = 400 - 4s_3 \;\Longrightarrow\; s_3 = 100\ \text{m} \quad (\text{taking } t = 20/2 = 10\ \text{s}) $$
Total distance
$$ s = 200 + 1200 + 100 = 1500\ \text{m} $$

**3. Derivation.** The particle of mass $m$ has only two forces on it: the weight
$mg$ vertically down and the normal reaction $N$ perpendicular to the plane (the
plane is smooth, so there is no friction). Resolve the weight along and
perpendicular to the plane: the components are $mg\sin\theta$ down the slope and
$mg\cos\theta$ into the plane.

Perpendicular to the plane there is no motion, so those forces balance:
$$ N = mg\cos\theta $$
Along the plane the only force is $mg\sin\theta$, so Newton's second law gives
$$ ma = mg\sin\theta \;\Longrightarrow\; a = g\sin\theta $$
The mass cancels, so the acceleration is independent of the mass.

**Application.** The length of the slope is
$$ l = \frac{h}{\sin\theta} = \frac{10}{\sin 30^\circ} = 20\ \text{m} $$
and the acceleration is $a = 9.8\sin 30^\circ = 4.9\ \text{m/s}^2$. With $u = 0$,
$$ v = \sqrt{2al} = \sqrt{2(4.9)(20)} = \sqrt{196} = 14\ \text{m/s} $$
$$ t = \frac{v}{a} = \frac{14}{4.9} = 2.86\ \text{s} $$
For free fall through the same height,
$$ v = \sqrt{2gh} = \sqrt{2(9.8)(10)} = \sqrt{196} = 14\ \text{m/s} $$
The two speeds are **equal**: the slope does not change the final speed, only the
time taken to acquire it ($2.86$ s on the plane against
$14/9.8 = 1.43$ s in free fall).
:::
