---
subject: Physics
grade: 11
unit: 3
title: Kinematics
hours: 5
area: Mechanics
---

Kinematics is the description of motion — where a body is, how fast it moves and
how that speed changes — without asking *why* it moves. The "why" is dynamics,
the next unit. Everything here rests on three quantities: displacement, velocity
and acceleration, and on the two operations that connect them, differentiation
and integration.

::: key Why the graphs matter
Almost every Group A and Group B kinematics question in recent NEB papers is
either a graph-reading question or a projectile question. Learn to *read* a
motion graph and half the unit is already done.
:::

## 3.1 Instantaneous velocity and acceleration

If a particle moves along the $x$-axis and is at $x_1$ at time $t_1$ and at $x_2$
at $t_2$, its **average velocity** over that interval is

$$ v_{av} = \frac{x_2 - x_1}{t_2 - t_1} = \frac{\Delta x}{\Delta t} $$

Average velocity tells you nothing about what happened *inside* the interval. To
get the velocity at one instant we shrink the interval to zero. The limit is the
**instantaneous velocity**:

$$ v = \lim_{\Delta t \to 0}\frac{\Delta x}{\Delta t} = \frac{dx}{dt} $$

::: definition Instantaneous velocity
The instantaneous velocity of a particle is the first derivative of its position
with respect to time. Its magnitude is the instantaneous speed, and its direction
is the direction of motion at that instant — i.e. along the tangent to the path.
:::

Geometrically, on a displacement–time graph the average velocity is the slope of
the **chord** joining two points, and the instantaneous velocity is the slope of
the **tangent** at a point. As the second point slides back towards the first,
the chord rotates into the tangent.

```figure caption="As $\Delta t$ shrinks, the chord PQ rotates into the tangent at P. The slope of the tangent is the instantaneous velocity."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
t = np.linspace(0, 4, 400); x = 0.55*t**2 + 1.0
ax.plot(t, x, color=ACCENT, lw=1.9, zorder=3)
t0 = 1.4; x0 = 0.55*t0**2 + 1.0
for dt, a, lab in [(2.2,0.30,None), (1.3,0.50,None), (0.55,0.80,'chords')]:
    t1 = t0+dt; x1 = 0.55*t1**2+1.0
    ax.plot([t0,t1],[x0,x1], color=MUTED, lw=1.0, alpha=a, ls='--', zorder=2, label=lab)
m = 2*0.55*t0
tt = np.array([t0-1.25, t0+1.9])
ax.plot(tt, x0 + m*(tt-t0), color='#A8271F', lw=1.6, zorder=4, label='tangent at P')
ax.plot([t0],[x0],'o',color=ACCENT, ms=5.5, zorder=5)
tq = t0+2.2; xq = 0.55*tq**2+1.0
ax.plot([tq],[xq],'o',color=MUTED, ms=4.5, zorder=5)
ax.annotate('P', (t0,x0), textcoords='offset points', xytext=(-11,-3), color=INK, fontsize=9.5)
ax.annotate('Q', (tq, xq), textcoords='offset points',
            xytext=(-16,8), ha='center', va='bottom', color=MUTED, fontsize=9.5)
ax.set_xlabel('time  $t$  (s)'); ax.set_ylabel('displacement  $x$  (m)')
ax.set_xlim(0,4); ax.set_ylim(0,10)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.55); ax.legend(loc='upper left')
```
In the same way, **acceleration** is the rate of change of velocity:

$$ a_{av} = \frac{\Delta v}{\Delta t}, \qquad a = \lim_{\Delta t \to 0}\frac{\Delta v}{\Delta t} = \frac{dv}{dt} = \frac{d^{2}x}{dt^{2}} $$

::: derivation The third form of acceleration, $a = v\,\dfrac{dv}{dx}$
We start from the definition $a = dv/dt$ and reach a form of acceleration with no
time in it at all — useful whenever a question gives you velocity as a function of
position.

**Step 1 — the definition.** Acceleration is the rate of change of velocity with
time:

$$ a = \frac{dv}{dt} $$

**Step 2 — bring in $x$.** The velocity $v$ changes with time only because the
particle has moved to a new position $x$, and $x$ itself changes with time. So $v$
depends on $t$ *through* $x$. The chain rule of differentiation lets us insert
$dx$ on the top and bottom:

$$ a = \frac{dv}{dx}\cdot\frac{dx}{dt} $$

(Think of it as $\dfrac{dv}{dt} = \dfrac{dv}{dx}\times\dfrac{dx}{dt}$ — the two
$dx$ factors formally cancel.)

**Step 3 — recognise the second factor.** By definition $dx/dt$ is the velocity:

$$ \frac{dx}{dt} = v $$

**Step 4 — substitute.** Replacing $dx/dt$ by $v$:

$$ a = v\,\frac{dv}{dx} $$

**Result.**

$$ a = \frac{dv}{dt} = v\,\frac{dv}{dx} $$

**What it means.** Both forms describe the same acceleration. The first is "how
fast does the speed change each second", the second is "how fast does the speed
change each metre, multiplied by how many metres you cover per second".

**Condition used.** The particle must move along a single line (one dimension) and
$v$ must be a well-defined function of $x$. If the particle turns back and passes
the same $x$ at two different speeds, you must treat each part of the journey
separately.
:::

::: tip The examiner is looking for
For "show that $a = v\,dv/dx$": start from $a = dv/dt$, write the chain rule
step explicitly, state that $dx/dt = v$, then substitute. Three lines, three
marks — do not skip the chain-rule line.
:::

::: tip When to use each form
Use $a = dv/dt$ when the data is velocity against **time**; use $a = v\,dv/dx$
when it is velocity against **position**. Choosing the wrong one turns a two-line
problem into a page of algebra.
:::

| Quantity | Defining relation | SI unit | Dimensional formula |
|---|---|---|---|
| Displacement | $\vec{s} = \vec{r}_2 - \vec{r}_1$ | m | $[L]$ |
| Velocity | $\vec{v} = d\vec{r}/dt$ | m s⁻¹ | $[LT^{-1}]$ |
| Acceleration | $\vec{a} = d\vec{v}/dt$ | m s⁻² | $[LT^{-2}]$ |

::: example Worked example 3.1
**Problem.** A particle moves so that $x = 3t^{3} - 4t^{2} + 2t$ (metres, seconds).
Find (a) its velocity and acceleration at $t = 2\ \text{s}$, and (b) the time at
which the acceleration is zero.

**Solution.**

(a) Differentiating once and twice,

$$ v = \frac{dx}{dt} = 9t^{2} - 8t + 2, \qquad a = \frac{dv}{dt} = 18t - 8 $$

At $t = 2\ \text{s}$: $v = 9(4) - 8(2) + 2 = 22\ \text{m s}^{-1}$ and
$a = 18(2) - 8 = 28\ \text{m s}^{-2}$.

(b) Setting $a = 0$ gives $18t - 8 = 0$, so $t = 4/9 \approx 0.44\ \text{s}$.
:::

## 3.2 Relative velocity

All velocity is measured with respect to some frame. If two bodies A and B have
velocities $\vec{v}_A$ and $\vec{v}_B$ measured in the same frame, the velocity
of A **relative to** B is

$$ \vec{v}_{AB} = \vec{v}_A - \vec{v}_B $$

Read the subscripts as "A with respect to B". Reversing them reverses the vector:
$\vec{v}_{BA} = -\vec{v}_{AB}$.

For motion along one line the vector subtraction is just a signed subtraction. In
two dimensions, subtract the components, or use the parallelogram rule with
$-\vec{v}_B$. If $\theta$ is the angle between $\vec{v}_A$ and $\vec{v}_B$, the
magnitude is

$$ v_{AB} = \sqrt{v_A^{2} + v_B^{2} - 2v_Av_B\cos\theta} $$

```figure caption="Relative velocity of A with respect to B is the vector $\vec{v}_A + (-\vec{v}_B)$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2,2.9))
O=np.array([0,0]); vA=np.array([2.6,1.5]); vB=np.array([2.1,-0.9])
def arr(a,b,c,lab,lpos,ls='-'):
    ax.annotate('', xy=b, xytext=a,
        arrowprops=dict(arrowstyle='-|>', color=c, lw=1.7, linestyle=ls,
                        shrinkA=0, shrinkB=0, mutation_scale=13))
    ax.annotate(lab, lpos, ha='center', va='center', color=c, fontsize=9.5)
# labels sit on the free side of each arrow, well clear of every stroke
arr(O, vA, ACCENT, r'$\vec{v}_A$', (1.02, 1.24))
arr(O, vB, '#0B6A62', r'$\vec{v}_B$', (1.40, -1.14))
arr(O, -vB, MUTED, r'$-\vec{v}_B$', (-1.32, -0.20), ls=(0,(3,2)))
arr(vA, vA-vB, '#A8271F', r'$\vec{v}_{AB}$', (1.76, 2.42))
ax.plot([(vA-vB)[0]],[(vA-vB)[1]],'o',color='#A8271F',ms=4)
ax.set_xlim(-2.45,3.0); ax.set_ylim(-1.45,2.8); ax.set_aspect('equal')
ax.axis('off')
```
::: example Worked example 3.2
**Problem.** Rain falls vertically at $4\ \text{m s}^{-1}$. A cyclist rides due
east at $3\ \text{m s}^{-1}$. At what angle to the vertical must the cyclist tilt
an umbrella?

**Solution.** The rain's velocity relative to the cyclist is
$\vec{v}_{rc} = \vec{v}_r - \vec{v}_c$. Taking east as $+x$ and up as $+y$,
$\vec{v}_r = (0,-4)$ and $\vec{v}_c = (3,0)$, so $\vec{v}_{rc} = (-3,-4)$.

Its magnitude is $\sqrt{3^2+4^2} = 5\ \text{m s}^{-1}$ and it makes an angle
$\theta$ with the vertical given by $\tan\theta = 3/4$, so
$\theta = 36.87^{\circ}$. The umbrella must be tilted about $37^{\circ}$ **forward**,
towards the east.
:::

::: caution The commonest relative-velocity error
Students subtract the *speeds* instead of the *vectors*. Velocity is a vector:
always resolve into components, subtract componentwise, then recombine.
:::

## 3.3 Equations of motion — graphical treatment

For **uniform acceleration** $a$, with initial velocity $u$ and velocity $v$
after time $t$, the velocity–time graph is a straight line of slope $a$ and
intercept $u$.

```figure caption="Velocity–time graph for uniform acceleration. The slope gives $a$; the shaded area gives the displacement $s$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.5,2.8))
t=np.linspace(0,5,200); u=4.0; a=2.0; v=u+a*t
ax.plot(t,v,color=ACCENT,lw=2)
ax.fill_between(t,0,v,color=ACCENT,alpha=0.10)
ax.hlines(u,0,5,color=MUTED,lw=.9,ls=':')
ax.vlines(5,0,u+a*5,color=MUTED,lw=.9,ls=':')
ax.annotate('$u$',(0,u),textcoords='offset points',xytext=(-16,-4),color=INK,fontsize=10)
ax.annotate('$v$',(5,u+a*5),textcoords='offset points',xytext=(4,-3),color=INK,fontsize=10)
ax.annotate('slope $=a$',(2.6,u+a*2.6),textcoords='offset points',xytext=(-48,16),
            color='#A8271F',fontsize=9.5,
            arrowprops=dict(arrowstyle='-|>',color='#A8271F',lw=1.1,mutation_scale=10))
ax.annotate('area $=s$',(2.4,4.6),color=INK,fontsize=9.5,ha='center')
ax.set_xlabel('time  $t$'); ax.set_ylabel('velocity  $v$')
ax.set_xlim(0,5.6); ax.set_ylim(0,16)
ax.set_xticks([0,5]); ax.set_xticklabels(['$0$','$t$'])
ax.set_yticks([])
ax.spines[['top','right']].set_visible(False)
```

::: derivation The three equations of motion from a velocity–time graph
We start from just two facts about a velocity–time graph — its **slope** is the
acceleration and the **area** under it is the displacement — and we reach all
three equations of uniformly accelerated motion.

Read the graph above: at $t = 0$ the velocity is $u$ (the intercept), at time $t$
it is $v$, and because the acceleration is constant the line is straight.

---

**First equation: $v = u + at$**

**Step 1.** The acceleration is the slope of the straight line. Slope means
"rise divided by run". The rise is the velocity gained, $v - u$; the run is the
time taken, $t - 0 = t$:

$$ a = \frac{v - u}{t} $$

**Step 2.** Multiply both sides by $t$ to clear the fraction:

$$ at = v - u $$

**Step 3.** Add $u$ to both sides to make $v$ the subject:

$$ v = u + at $$

---

**Second equation: $s = ut + \frac{1}{2}at^{2}$**

**Step 1.** The displacement is the area between the line and the time axis. That
shape is a **trapezium**. Cut it with a horizontal line at height $u$: below the
cut is a rectangle, above it a triangle.

$$ s = \text{area of rectangle} + \text{area of triangle} $$

**Step 2.** The rectangle has height $u$ and width $t$, so its area is length
$\times$ breadth:

$$ \text{area of rectangle} = u \times t = ut $$

**Step 3.** The triangle has base $t$ and height $(v - u)$, and the area of a
triangle is $\frac{1}{2}\times$ base $\times$ height:

$$ \text{area of triangle} = \tfrac{1}{2}\,t\,(v - u) $$

**Step 4.** From the first equation, $v - u = at$. Substitute it:

$$ \text{area of triangle} = \tfrac{1}{2}\,t\,(at) = \tfrac{1}{2}at^{2} $$

**Step 5.** Add the two areas:

$$ s = ut + \tfrac{1}{2}at^{2} $$

---

**Third equation: $v^{2} = u^{2} + 2as$**

**Step 1.** Take the trapezium area in one go. The area of a trapezium is
$\frac{1}{2}\times$(sum of the two parallel sides)$\times$(distance between them).
The parallel sides are $u$ and $v$, and the distance between them is $t$:

$$ s = \tfrac{1}{2}(u + v)\,t $$

**Step 2.** We want no $t$ in the answer, so get $t$ from the first equation.
Starting from $v = u + at$, subtract $u$ and divide by $a$:

$$ t = \frac{v - u}{a} $$

**Step 3.** Substitute this $t$ into the expression for $s$:

$$ s = \tfrac{1}{2}(u + v)\cdot\frac{v - u}{a} $$

**Step 4.** Multiply the two brackets. $(u+v)(v-u) = v^{2} - u^{2}$, the
difference-of-squares identity:

$$ s = \frac{v^{2} - u^{2}}{2a} $$

**Step 5.** Multiply both sides by $2a$:

$$ 2as = v^{2} - u^{2} $$

**Step 6.** Add $u^{2}$ to both sides:

$$ v^{2} = u^{2} + 2as $$

---

**Result.**

$$ v = u + at, \qquad s = ut + \tfrac{1}{2}at^{2}, \qquad v^{2} = u^{2} + 2as $$

**What it means.** The first links velocity to time, the second links position to
time, and the third links velocity to position with no time involved — so you pick
the one that avoids the quantity you were not given.

**Condition used.** All three need the acceleration $a$ to be **constant**; that is
what makes the graph a straight line. They also need motion in a **straight line**,
with one fixed positive direction chosen before you start. They do not apply to
circular motion, or to a car whose acceleration is changing.
:::

::: tip The examiner is looking for
A 5-mark "derive the three equations graphically" answer must contain: (i) a
labelled $v$–$t$ graph with $u$, $v$, $t$ marked; (ii) the sentence "slope =
acceleration" and the sentence "area = displacement"; (iii) the algebra for each
of the three, with the trapezium split into rectangle + triangle shown; (iv) the
substitution $v - u = at$ in the second, and $t = (v-u)/a$ in the third. No graph
means you cannot score the "graphical treatment" marks even if the algebra is
perfect.
:::

A fourth relation gives the distance travelled in the $n^{th}$ second:

$$ s_{n} = u + \frac{a}{2}(2n-1) $$

::: caution $s_n$ is not a distance per unit time
$s_n$ is the distance covered **during** the $n^{\text{th}}$ second, i.e. between
$t=n-1$ and $t=n$. Its unit is the metre, not m s⁻¹, even though the formula looks
like a velocity.
:::

| Graph | Slope represents | Area under it represents |
|---|---|---|
| Displacement–time | velocity | — (no physical meaning) |
| Velocity–time | acceleration | displacement |
| Acceleration–time | jerk (not in syllabus) | change in velocity |

## 3.4 Motion of a freely falling body

A body falling freely near the Earth's surface, with air resistance neglected,
has constant acceleration $g \approx 9.8\ \text{m s}^{-2}$ directed downwards.
The three equations apply unchanged with $a$ replaced by $g$ — you only have to
be consistent about signs.

::: tip A sign convention that never fails
Fix **upward as positive** before you write anything. Then $a = -g$ always,
an upward throw has $u > 0$, and a downward throw has $u < 0$. Never change the
convention halfway through a problem.
:::

For a body projected vertically upwards with speed $u$:

$$ t_{\text{up}} = \frac{u}{g}, \qquad H_{\max} = \frac{u^{2}}{2g},
\qquad t_{\text{total}} = \frac{2u}{g} $$

and it returns to the point of projection with speed $u$ — equal in magnitude,
opposite in direction. Time of ascent equals time of descent.

::: example Worked example 3.3
**Problem.** A stone is dropped from a balloon rising at $5\ \text{m s}^{-1}$ when
the balloon is at $60\ \text{m}$. How long does the stone take to reach the ground?
Take $g = 10\ \text{m s}^{-2}$.

**Solution.** The stone starts with the balloon's velocity: $u = +5\ \text{m s}^{-1}$
(upward positive). Displacement to the ground is $s = -60\ \text{m}$, and $a = -10\ \text{m s}^{-2}$.

$$ s = ut + \tfrac{1}{2}at^{2} \;\Rightarrow\; -60 = 5t - 5t^{2} $$

So $5t^{2} - 5t - 60 = 0$, i.e. $t^{2} - t - 12 = 0$, giving $(t-4)(t+3)=0$.
Taking the positive root, $t = 4\ \text{s}$.

Note the stone first rises for $0.5\ \text{s}$ — forgetting its initial upward
velocity is the standard trap in this question.
:::

## 3.5 Projectile motion and its applications

A projectile is a body given an initial velocity and then left to move under
gravity alone. The whole subject reduces to one idea:

::: key The independence of horizontal and vertical motion
The horizontal and vertical motions are completely independent. Horizontally
there is no acceleration, so $x$-motion is uniform; vertically the acceleration
is $-g$, so $y$-motion is uniformly accelerated. Solve them separately and link
them only through the common time $t$.
:::

::: derivation The path of a projectile is a parabola
We start from the two separate equations of motion, one for the horizontal
direction and one for the vertical, and we reach a single equation linking $y$ to
$x$ with no time in it. Its shape is what we want to identify.

**Step 1 — split the initial velocity.** A speed $u$ at angle $\theta$ to the
horizontal has a horizontal part and a vertical part, found by resolving:

$$ u_x = u\cos\theta, \qquad u_y = u\sin\theta $$

**Step 2 — horizontal motion.** There is no horizontal force (we ignore air
resistance), so there is no horizontal acceleration and the horizontal velocity
stays $u\cos\theta$ for ever. Distance = speed $\times$ time:

$$ x = (u\cos\theta)\,t $$

**Step 3 — vertical motion.** Vertically the acceleration is $g$ downwards. Using
$s = ut + \frac{1}{2}at^{2}$ with $u \to u\sin\theta$ and $a \to -g$ (taking up as
positive):

$$ y = (u\sin\theta)\,t - \tfrac{1}{2}gt^{2} $$

**Step 4 — make $t$ the subject of the horizontal equation.** Divide both sides of
Step 2 by $u\cos\theta$:

$$ t = \frac{x}{u\cos\theta} $$

**Step 5 — substitute this $t$ into the vertical equation.** This is legal because
it is the *same* $t$ in both — the two motions share one clock:

$$ y = (u\sin\theta)\left(\frac{x}{u\cos\theta}\right)
- \tfrac{1}{2}g\left(\frac{x}{u\cos\theta}\right)^{2} $$

**Step 6 — tidy the first term.** The $u$ cancels, and
$\sin\theta/\cos\theta = \tan\theta$:

$$ y = x\tan\theta - \tfrac{1}{2}g\left(\frac{x}{u\cos\theta}\right)^{2} $$

**Step 7 — square the bracket in the second term.** Squaring top and bottom:

$$ y = x\tan\theta - \frac{g\,x^{2}}{2u^{2}\cos^{2}\theta} $$

**Step 8 — read off the shape.** For a given launch, $u$ and $\theta$ are fixed
numbers, so we may write $A = \tan\theta$ and $B = g/(2u^{2}\cos^{2}\theta)$, both
constants:

$$ y = Ax - Bx^{2} $$

**Result.** The trajectory equation is

$$ y = x\tan\theta - \frac{g\,x^{2}}{2u^{2}\cos^{2}\theta} $$

and since $y$ is a quadratic in $x$ with a negative $x^{2}$ coefficient, the path
is a **parabola opening downwards**.

**What it means.** Gravity pulls the projectile below the straight line it would
have followed, and the amount it falls behind grows as $t^{2}$ — that $x^{2}$ term
is exactly the free fall the body would have had.

**Assumptions used.** Air resistance is neglected, $g$ is constant in size and
direction over the flight, and the Earth's curvature and rotation are ignored.
:::

```figure caption="Trajectories for a fixed speed at several angles. Complementary angles ($30^\circ$ and $60^\circ$) give the same range; $45^\circ$ gives the maximum."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.7))
u=20.0; g=9.8
for th,c,ls in [(30,'#0B6A62','-'),(45,'#4A42D6','-'),(60,'#A8271F','-'),(75,'#8a8f99','--')]:
    r=np.radians(th); T=2*u*np.sin(r)/g; t=np.linspace(0,T,220)
    ax.plot(u*np.cos(r)*t, u*np.sin(r)*t-0.5*g*t**2, color=c, ls=ls, lw=1.7,
            label=f'${th}^\\circ$')
ax.set_xlabel('horizontal distance (m)'); ax.set_ylabel('height (m)')
ax.set_ylim(0,20.5); ax.set_xlim(0,44)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.5)
# legend lifted clear of the axes so it cannot sit on the 75 deg trajectory
ax.legend(title='angle of projection', ncol=4, loc='lower center',
          bbox_to_anchor=(0.5, 1.02), fontsize=8.2,
          title_fontsize=8.2, columnspacing=1.4, handlelength=1.6)
```
::: derivation Time of flight, maximum height and horizontal range
We start from the same two motion equations, $x = (u\cos\theta)t$ and
$y = (u\sin\theta)t - \frac{1}{2}gt^{2}$, and reach the three numbers a question
always asks for: how long the flight lasts, how high it goes, and how far it lands.

---

**Time of flight $T$**

**Step 1.** The projectile is back on the ground when its height is zero again, so
put $y = 0$ and $t = T$:

$$ 0 = (u\sin\theta)T - \tfrac{1}{2}gT^{2} $$

**Step 2.** Take out the common factor $T$:

$$ 0 = T\left(u\sin\theta - \tfrac{1}{2}gT\right) $$

**Step 3.** A product is zero when one factor is zero. So either $T = 0$ (that is
the launch instant, which we do not want) or the bracket is zero:

$$ u\sin\theta - \tfrac{1}{2}gT = 0 $$

**Step 4.** Move the second term across:

$$ \tfrac{1}{2}gT = u\sin\theta $$

**Step 5.** Multiply both sides by $2$ and divide by $g$:

$$ T = \frac{2u\sin\theta}{g} $$

---

**Maximum height $H$**

**Step 1.** At the highest point the projectile has stopped rising and has not yet
started falling, so its **vertical** velocity is zero there. Apply
$v^{2} = u^{2} + 2as$ to the vertical direction only, with initial vertical
velocity $u\sin\theta$, final vertical velocity $0$, acceleration $-g$ and
displacement $H$:

$$ 0^{2} = (u\sin\theta)^{2} + 2(-g)H $$

**Step 2.** Write out the squares and the product:

$$ 0 = u^{2}\sin^{2}\theta - 2gH $$

**Step 3.** Move $2gH$ to the left:

$$ 2gH = u^{2}\sin^{2}\theta $$

**Step 4.** Divide both sides by $2g$:

$$ H = \frac{u^{2}\sin^{2}\theta}{2g} $$

---

**Horizontal range $R$**

**Step 1.** Horizontally there is no acceleration, so the range is just the
constant horizontal speed multiplied by the whole time of flight:

$$ R = (u\cos\theta)\,T $$

**Step 2.** Put in $T = 2u\sin\theta/g$ from above:

$$ R = (u\cos\theta)\cdot\frac{2u\sin\theta}{g} $$

**Step 3.** Multiply the two $u$ factors together:

$$ R = \frac{2u^{2}\sin\theta\cos\theta}{g} $$

**Step 4.** Use the double-angle identity $2\sin\theta\cos\theta = \sin 2\theta$:

$$ R = \frac{u^{2}\sin 2\theta}{g} $$

---

**Maximum range**

**Step 1.** In $R = u^{2}\sin 2\theta/g$, only $\sin 2\theta$ can change if $u$ is
fixed. The largest value of a sine is $1$:

$$ R_{\max} = \frac{u^{2}\times 1}{g} = \frac{u^{2}}{g} $$

**Step 2.** This happens when $\sin 2\theta = 1$, i.e. when $2\theta = 90^{\circ}$:

$$ \theta = 45^{\circ} $$

---

**Result.**

$$ T = \frac{2u\sin\theta}{g}, \qquad H = \frac{u^{2}\sin^{2}\theta}{2g},
\qquad R = \frac{u^{2}\sin 2\theta}{g}, \qquad R_{\max} = \frac{u^{2}}{g}
\ \text{at}\ 45^{\circ} $$

**What it means.** Time of flight and height depend only on the **vertical**
component $u\sin\theta$; the range needs both components, which is why there is a
best compromise angle of $45^{\circ}$. Note also $T = 2\times$(time to reach the
top), so rise time equals fall time.

**Assumptions used.** No air resistance, constant $g$, and — important — the
landing point is at the **same height** as the launch point. If the ground is lower
(a ball thrown off a cliff), $T$ and $R$ must be recalculated from
$y = -h$ instead of $y = 0$.
:::

::: tip The examiner is looking for
(i) Resolve $u$ into $u\cos\theta$ and $u\sin\theta$ and say the two motions are
independent; (ii) for $T$, set $y = 0$ and *reject the root $t = 0$ with a reason*;
(iii) for $H$, state that the vertical velocity is zero at the top; (iv) for $R$,
use $R = u\cos\theta\times T$ and show the $2\sin\theta\cos\theta = \sin2\theta$
step; (v) state the same-level assumption. The rejected root and the double-angle
step are the two places marks are usually dropped.
:::

Three consequences follow at once and are examined constantly:

- $R$ is maximum when $\sin 2\theta = 1$, i.e. $\theta = 45^{\circ}$, giving $R_{\max} = u^{2}/g$.
- Angles $\theta$ and $(90^{\circ}-\theta)$ give the **same range**, because
  $\sin 2\theta = \sin(180^{\circ} - 2\theta)$. This is why $30^{\circ}$ and $60^{\circ}$ land together.
- At the highest point the velocity is **not zero** — it is horizontal, of magnitude $u\cos\theta$.

::: caution Velocity at the top
"The velocity at the maximum height is zero" is wrong for a projectile. Only the
*vertical component* vanishes. The speed there is $u\cos\theta$.
:::

**Horizontal projection.** If a body is projected horizontally with speed $u$
from height $h$, then $\theta = 0$ and

$$ t = \sqrt{\frac{2h}{g}}, \qquad R = u\sqrt{\frac{2h}{g}},
\qquad v = \sqrt{u^{2} + 2gh} $$

The time of fall does not depend on $u$: a bullet fired horizontally and one
dropped from the same height hit the ground together.

::: example Worked example 3.4
**Problem.** A ball is thrown at $25\ \text{m s}^{-1}$ at $53^{\circ}$ to the
horizontal. Taking $g = 10\ \text{m s}^{-2}$, $\sin 53^{\circ} = 0.8$ and
$\cos 53^{\circ} = 0.6$, find the time of flight, maximum height, range, and the
speed at the highest point.

**Solution.** Components: $u_x = 25(0.6) = 15\ \text{m s}^{-1}$,
$u_y = 25(0.8) = 20\ \text{m s}^{-1}$.

$$ T = \frac{2u_y}{g} = \frac{40}{10} = 4\ \text{s} $$
$$ H = \frac{u_y^{2}}{2g} = \frac{400}{20} = 20\ \text{m} $$
$$ R = u_x T = 15 \times 4 = 60\ \text{m} $$

At the highest point the velocity is purely horizontal, so the speed is
$u_x = 15\ \text{m s}^{-1}$.
:::

## Chapter summary

- Instantaneous velocity is $v = dx/dt$ (slope of the tangent to the $x$–$t$
  graph); acceleration is $a = dv/dt = v\,dv/dx$.
- On a $v$–$t$ graph, slope is acceleration and area is displacement.
- For uniform acceleration: $v = u+at$, $s = ut + \frac{1}{2}at^{2}$,
  $v^{2} = u^{2}+2as$, $s_n = u + \frac{a}{2}(2n-1)$.
- Free fall is uniform acceleration with $a = -g$ (upward positive). Time up
  equals time down; the landing speed equals the launch speed.
- Projectile motion = uniform horizontal motion + free vertical fall. The path is
  a parabola, $T = 2u\sin\theta/g$, $H = u^2\sin^2\theta/2g$, $R = u^2\sin 2\theta/g$.
- Range is maximum at $45^\circ$; complementary angles give equal ranges; the
  speed at the top is $u\cos\theta$, not zero.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The slope of a displacement–time graph gives <span class="marks">[1]</span>
   (a) acceleration (b) velocity (c) distance (d) jerk
2. A projectile has maximum range when the angle of projection is <span class="marks">[1]</span>
   (a) $30^{\circ}$ (b) $45^{\circ}$ (c) $60^{\circ}$ (d) $90^{\circ}$
3. At the highest point of its path a projectile's velocity is <span class="marks">[1]</span>
   (a) zero (b) vertical (c) horizontal (d) along the tangent to the vertical

::: note Answers to Group A
**1.** (b) — slope of $x$–$t$ is $dx/dt = v$.
**2.** (b) — $R = u^2\sin2\theta/g$ is maximum when $2\theta = 90^{\circ}$.
**3.** (c) — only the vertical component vanishes; the horizontal component $u\cos\theta$ survives.
:::

**Group B — Short answer (5 marks each)**

1. Define instantaneous velocity and acceleration. Show that $a = v\,\dfrac{dv}{dx}$. <span class="marks">[5]</span>
2. Derive the three equations of uniformly accelerated motion from a velocity–time graph. <span class="marks">[5]</span>
3. A car accelerates uniformly from rest and covers $100\ \text{m}$ in $5\ \text{s}$.
   Find its acceleration and the distance covered in the $5^{\text{th}}$ second. <span class="marks">[5]</span>
4. Rain falls vertically at $6\ \text{m s}^{-1}$ while a man walks east at
   $8\ \text{m s}^{-1}$. Find the magnitude and direction of the rain relative to the man. <span class="marks">[5]</span>

::: note Answers to Group B
**3.** From $s = ut+\frac12at^2$ with $u=0$: $100 = \frac12a(25)$, so
$a = 8\ \text{m s}^{-2}$. Then $s_5 = u + \frac{a}{2}(2\times5-1) = 0 + 4(9) = 36\ \text{m}$.

**4.** $\vec{v}_{rm} = (0,-6)-(8,0) = (-8,-6)$; magnitude $\sqrt{64+36} = 10\ \text{m s}^{-1}$,
at $\tan^{-1}(8/6) = 53.1^{\circ}$ to the vertical, tilted towards the west
(i.e. the man must tilt his umbrella $53^{\circ}$ forward, to the east).
:::

**Group C — Long answer (8 marks each)**

1. (a) Show that the trajectory of a projectile is a parabola. <span class="marks">[4]</span>
   (b) Derive expressions for its time of flight, maximum height and horizontal
   range, and hence show that the range is maximum at $45^{\circ}$. <span class="marks">[4]</span>
2. A body is projected at $u = 40\ \text{m s}^{-1}$ at $30^{\circ}$ from the top of
   a tower $50\ \text{m}$ high. Taking $g = 10\ \text{m s}^{-2}$, find (a) the time
   to reach the ground, (b) the horizontal distance from the foot of the tower,
   and (c) the speed on landing. <span class="marks">[8]</span>

::: note Answer to Group C question 2
$u_x = 40\cos30^{\circ} = 34.64\ \text{m s}^{-1}$, $u_y = 40\sin30^{\circ} = 20\ \text{m s}^{-1}$.

(a) Taking upward positive, $-50 = 20t - 5t^{2}$, so $5t^{2}-20t-50 = 0$,
i.e. $t^{2}-4t-10=0$, giving $t = 2+\sqrt{14} = 5.74\ \text{s}$.

(b) $x = u_xt = 34.64 \times 5.74 = 198.8\ \text{m}$.

(c) $v_y = u_y - gt = 20 - 57.4 = -37.4\ \text{m s}^{-1}$, so
$v = \sqrt{34.64^{2}+37.4^{2}} = 51.0\ \text{m s}^{-1}$.
:::
