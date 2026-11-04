---
subject: Mathematics
grade: BCA
unit: 8
title: Trigonometry
hours: 4
area: Trigonometry
---

Trigonometry carries 2–5 questions, and the Dean's Office model asks only the most basic ($\cos0^\circ$). The usual mix is one value from the standard-angle table, one identity or compound-angle question, one height-and-distance problem and sometimes an equation or inverse function. All of it comes from a one-page table and about ten identities, so learn them by heart.

::: key What the paper asks from this chapter
- **Standard angles** (0°, 30°, 45°, 60°, 90°), radians and degrees, signs by quadrant.
- **Identities**: $\sin^2\theta+\cos^2\theta=1$, $1+\tan^2\theta=\sec^2\theta$, complementary angles.
- **Compound and multiple angles**: $\sin(A\pm B)$, $\cos2A$, $\tan(A+B)$.
- **Equations** and **inverse functions**: general solutions, principal values.
- **Heights and distances**, sine and cosine rules, area of a triangle.
:::

## 8.1 Trigonometric ratios, standard angles and identities

| $\theta$ | 0° | 30° | 45° | 60° | 90° |
|---|---|---|---|---|---|
| $\sin\theta$ | 0 | $\frac{1}{2}$ | $\frac{1}{\sqrt{2}}$ | $\frac{\sqrt{3}}{2}$ | 1 |
| $\cos\theta$ | 1 | $\frac{\sqrt{3}}{2}$ | $\frac{1}{\sqrt{2}}$ | $\frac{1}{2}$ | 0 |
| $\tan\theta$ | 0 | $\frac{1}{\sqrt{3}}$ | 1 | $\sqrt{3}$ | not defined |

- $\csc\theta=\frac{1}{\sin\theta}$, $\sec\theta=\frac{1}{\cos\theta}$, $\cot\theta=\frac{\cos\theta}{\sin\theta}$, $\tan\theta=\frac{\sin\theta}{\cos\theta}$.
- $\sin^2\theta+\cos^2\theta=1$; $1+\tan^2\theta=\sec^2\theta$; $1+\cot^2\theta=\csc^2\theta$.
- $\sin(90^\circ-\theta)=\cos\theta$, $\tan(90^\circ-\theta)=\cot\theta$. $\pi$ rad $=180^\circ$.
- **Signs (ASTC)**: all positive in I; only sin in II; only tan in III; only cos in IV. Range of $\sin,\cos$ is $[-1,1]$; period $2\pi$.

```svgfig label="8.1" caption="The unit circle with the standard angles. A point at angle t is (cos t, sin t): at 30 degrees it is (0.866, 0.5), at 45 degrees (0.707, 0.707), at 60 degrees (0.5, 0.866). The cell asserts sin^2 + cos^2 = 1 at each. The table uses the memory rule: sin of 0, 30, 45, 60, 90 degrees is sqrt(0)/2, sqrt(1)/2, sqrt(2)/2, sqrt(3)/2, sqrt(4)/2, and cos runs in reverse."
import math
angs = [0, 30, 45, 60, 90]
sv = [math.sqrt(k) / 2 for k in range(5)]; cv = sv[::-1]
for a, s, c in zip(angs, sv, cv):
    assert abs(math.sin(math.radians(a)) - s) < 1e-9 and abs(math.cos(math.radians(a)) - c) < 1e-9 and abs(s * s + c * c - 1) < 1e-9
assert round(math.tan(math.radians(60)), 4) == round(math.sqrt(3), 4)
f = Fig(780, 320)
cx, cy, R = 170, 160, 130
f.raw('<circle cx="%d" cy="%d" r="%d" fill="#f8fafc" stroke="%s" stroke-width="2"/>' % (cx, cy, R, NAVY))
f.line(cx - R - 14, cy, cx + R + 14, cy, color=SLATE, sw=1.3); f.line(cx, cy - R - 14, cx, cy + R + 14, color=SLATE, sw=1.3)
for a, s, c in zip(angs, sv, cv):
    x, y = cx + R * c, cy - R * s
    f.line(cx, cy, x, y, color=TEAL, sw=1.6); f.circle(x, y, 4.5, fill=RED, stroke=RED)
    if a in (30, 45, 60):
        f.line(x, y, x, cy, color=AMBER, sw=1.2, dash=True)
        f.text(x + 8, y - 12, "%d: (%.3f, %.3f)" % (a, c, s), size=10, color=NAVY, bold=True, anchor="start")
f.text(cx + R + 4, cy + 18, "0: (1, 0)", size=10, color=NAVY, bold=True, anchor="end"); f.text(cx + 8, cy - R - 6, "90: (0, 1)", size=10, color=NAVY, bold=True, anchor="start")
f.text(570, 24, "Standard values", size=11.5, color=NAVY, bold=True)
hd = ["angle", "sin", "cos", "tan"]; xs = [400, 480, 570, 660]
for h, x in zip(hd, xs): f.text(x, 52, h, size=11, color=NAVY, bold=True, anchor="start")
rows = [("0", "0", "1", "0"), ("30", "1/2", "sqrt3/2", "1/sqrt3"), ("45", "1/sqrt2", "1/sqrt2", "1"), ("60", "sqrt3/2", "1/2", "sqrt3"), ("90", "1", "0", "not defined")]
for j, r in enumerate(rows):
    y = 62 + j * 32
    f.box(392, y, 370, 28, "", fill=(SOFT if j % 2 == 0 else BLUE), stroke="#cbd5e1", r=3)
    for v, x in zip(r, xs): f.text(x, y + 14, v, size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
f.text(580, 252, "ASTC: All, Sin, Tan, Cos are positive in", size=10.5, color=SLATE); f.text(580, 272, "quadrants I, II, III, IV respectively", size=10.5, color=SLATE)
f.text(580, 296, "sin(180 - t) = sin t,  cos(180 - t) = -cos t", size=10.5, color=RED, bold=True)
```

## 8.2 Compound, multiple and half angles

- $\sin(A\pm B)=\sin A\cos B\pm\cos A\sin B$; $\cos(A\pm B)=\cos A\cos B\mp\sin A\sin B$; $\tan(A+B)=\frac{\tan A+\tan B}{1-\tan A\tan B}$.
- $\sin2A=2\sin A\cos A$; $\cos2A=\cos^2A-\sin^2A=2\cos^2A-1=1-2\sin^2A$; $\tan2A=\frac{2\tan A}{1-\tan^2A}$.
- $\sin3A=3\sin A-4\sin^3A$; $\cos3A=4\cos^3A-3\cos A$.
- Maximum of $a\sin\theta+b\cos\theta$ is $\sqrt{a^2+b^2}$; $\sin\theta\cos\theta\le\frac{1}{2}$.

```svgfig label="8.2" caption="The three basic graphs over one period 0 to 360 degrees, and a worked compound angle. sin x and cos x oscillate between -1 and 1 with period 360 degrees; tan x has period 180 degrees and breaks at 90 and 270. On the right, sin 75 degrees = sin(45 + 30) = (sqrt6 + sqrt2)/4 = 0.9659, and from a 3-4-5 triangle sin 2A = 2 x 3/5 x 4/5 = 24/25."
import math
s75 = math.sin(math.radians(75)); assert round(s75, 4) == round((math.sqrt(6) + math.sqrt(2)) / 4, 4) == 0.9659
assert abs(math.sin(math.radians(45 + 30)) - (math.sin(math.radians(45)) * math.cos(math.radians(30)) + math.cos(math.radians(45)) * math.sin(math.radians(30)))) < 1e-12
A = math.asin(3 / 5); assert abs(math.sin(2 * A) - 24 / 25) < 1e-12 and abs(math.cos(2 * A) - 7 / 25) < 1e-12
f = Fig(780, 320)
ax = Axes(f, 40, 24, 400, 230, (0, 360), (-2, 2))
ax.grid(90, 1, labels=False); ax.axes("", "")
for d in (0, 90, 180, 270, 360): f.text(ax.X(d), 272, str(d), size=10, color=SLATE, bold=True)
for v in (-1, 0, 1): f.text(30, ax.Y(v) + 4, str(v), size=10, color=SLATE, anchor="end", bold=True)
ax.curve(lambda d: math.sin(math.radians(d)), 0, 360, color=NAVY, sw=2.5)
ax.curve(lambda d: math.cos(math.radians(d)), 0, 360, color=TEAL, sw=2.5)
ax.curve(lambda d: math.tan(math.radians(d)), 0, 360, color=AMBER, sw=1.8, dash=True)
f.text(ax.X(100), ax.Y(1) - 8, "sin", size=11, color=NAVY, bold=True); f.text(ax.X(20), ax.Y(1) - 8, "cos", size=11, color=TEAL, bold=True); f.text(ax.X(222), ax.Y(1.5), "tan", size=11, color=AMBER, bold=True)
f.text(240, 296, "x in degrees", size=10, color=SLATE)
f.text(600, 30, "Compound and multiple angles", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("sin(A + B) = sinA cosB + cosA sinB", NAVY), ("cos(A + B) = cosA cosB - sinA sinB", NAVY), ("sin 75 = sin(45 + 30)", SLATE), ("= (1/sqrt2)(sqrt3/2) + (1/sqrt2)(1/2)", SLATE), ("= (sqrt6 + sqrt2)/4 = 0.9659", RED), ("sin 2A = 2 sinA cosA", NAVY), ("cos 2A = cos^2A - sin^2A = 1 - 2sin^2A", NAVY), ("3-4-5: sinA = 3/5, cosA = 4/5", SLATE), ("sin 2A = 24/25,  cos 2A = 7/25", RED)]):
    f.text(470, 62 + j * 27, t, size=10.5, color=c, anchor="start", bold=(c in (NAVY, RED)))
```

## 8.3 Trigonometric equations and inverse functions

- General solutions: $\sin\theta=\sin\alpha\Rightarrow\theta=n\pi+(-1)^n\alpha$; $\cos\theta=\cos\alpha\Rightarrow\theta=2n\pi\pm\alpha$; $\tan\theta=\tan\alpha\Rightarrow\theta=n\pi+\alpha$. $\sin\theta=0\Rightarrow\theta=n\pi$.
- Principal values: $\sin^{-1}x\in[-\frac{\pi}{2},\frac{\pi}{2}]$; $\cos^{-1}x\in[0,\pi]$; $\tan^{-1}x\in(-\frac{\pi}{2},\frac{\pi}{2})$. $\sin^{-1}x+\cos^{-1}x=\frac{\pi}{2}$.

```svgfig label="8.3" caption="Solving sin x = 1/2 for 0 to 360 degrees: the line y = 1/2 cuts the sine curve twice, at x = 30 and x = 150 degrees (sin(180 - x) = sin x). The general solution is x = n x 180 + (-1)^n x 30 degrees. Also 2 sin^2 x - sin x - 1 = 0 factorises as (2 sin x + 1)(sin x - 1) = 0, giving sin x = 1 or -1/2 and x = 90, 210, 330 degrees. Right: principal ranges of the inverse functions."
import math
sol = [x for x in range(0, 360) if abs(math.sin(math.radians(x)) - 0.5) < 1e-9]; assert sol == [30, 150]
roots = [x for x in range(0, 360) if abs(2 * math.sin(math.radians(x)) ** 2 - math.sin(math.radians(x)) - 1) < 1e-9]; assert roots == [90, 210, 330]
assert round(math.degrees(math.asin(0.5))) == 30 and round(math.degrees(math.acos(0.5))) == 60 and round(math.degrees(math.atan(1))) == 45
assert abs(math.asin(0.3) + math.acos(0.3) - math.pi / 2) < 1e-12
f = Fig(780, 320)
ax = Axes(f, 40, 24, 400, 230, (0, 360), (-1.3, 1.3))
ax.grid(90, 0.5, labels=False); ax.axes("", "")
for d in (0, 90, 180, 270, 360): f.text(ax.X(d), 272, str(d), size=10, color=SLATE, bold=True)
for v in (-1, 0, 0.5, 1): f.text(30, ax.Y(v) + 4, "%g" % v, size=10, color=SLATE, anchor="end", bold=True)
ax.curve(lambda d: math.sin(math.radians(d)), 0, 360, color=NAVY, sw=2.5); ax.hline(0.5, color=RED, dash=False, sw=1.6)
ax.pt(30, 0.5, "30", r=5, color=RED, dx=-8, dy=-12, size=11, anchor="end"); ax.pt(150, 0.5, "150", r=5, color=RED, dx=8, dy=-12, size=11)
ax.pt(210, -0.5, "210", r=4, color=AMBER, dx=8, dy=14, size=10.5); ax.pt(330, -0.5, "330", r=4, color=AMBER, dx=-4, dy=14, size=10.5, anchor="end")
f.text(240, 296, "x in degrees;  y = 1/2 (red) meets sin x at 30 and 150", size=10.5, color=SLATE)
f.text(600, 30, "Principal values of inverse functions", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("sin^-1 x : range -90 to 90 degrees", NAVY), ("cos^-1 x : range 0 to 180 degrees", TEAL), ("tan^-1 x : range -90 to 90 (open)", AMBER), ("sin^-1(1/2) = 30,  cos^-1(1/2) = 60", SLATE), ("tan^-1(1) = 45", SLATE), ("sin^-1 x + cos^-1 x = 90 degrees", RED), ("sin^-1 x is NOT 1/sin x", RED), ("sinx = sin a:  x = n(180) + (-1)^n a", NAVY), ("cosx = cos a:  x = 360n +/- a;  tan: 180n + a", NAVY)]):
    f.text(470, 62 + j * 27, t, size=10.5, color=c, anchor="start", bold=(c in (RED, NAVY)))
```

## 8.4 Heights and distances, triangle properties

- Angle of elevation is measured **up** from the horizontal; depression **down**. $\tan\theta=\frac{\text{height}}{\text{distance}}$.
- Sine rule: $\frac{a}{\sin A}=\frac{b}{\sin B}=\frac{c}{\sin C}=2R$. Cosine rule: $a^2=b^2+c^2-2bc\cos A$. Area $=\frac{1}{2}ab\sin C$.

```photogrid label="8.1" cols="4" ratio="0.9" caption="Measuring heights by angles. (a) Radhanath Sikdar (1813-1870), the Bengali mathematician of the Great Trigonometrical Survey who computed that Peak XV, later Everest, was about 29,000 feet, using exactly the angle-of-elevation method of this section. (b) A plaque at Pune showing the two-angle formula h = x sin(a) sin(b) / sin(a - b). (c) A surveyor sighting through a theodolite. (d) A 19th-century transit theodolite of the kind used in the survey."
@ photo id="bcamath/sikdar" cap="Radhanath Sikdar, Everest computer"
focus 0.5 0.3
@ photo id="bcamath/zeropt" cap="Pune plaque: height formula"
focus 0.5 0.55
@ photo id="bcamath/theod" cap="Surveyor with a theodolite"
focus 0.5 0.5
@ photo id="bcamath/transit" cap="Transit theodolite"
focus 0.5 0.5
```

```svgfig label="8.4" caption="Angle of elevation problems, computed. (a) From 50 m away the top of a tower is seen at 30 degrees: height = 50 tan 30 = 28.87 m. (b) Two sightings along a line toward the tower, at 30 degrees and then, after walking 100 m closer, at 45 degrees: h = 100 / (cot 30 - cot 45) = 100 / (sqrt3 - 1) = 136.60 m. The angle of elevation is always measured from the HORIZONTAL."
import math
t = lambda d: math.tan(math.radians(d))
h1 = 50 * t(30); assert round(h1, 2) == 28.87
h2 = 100 / (1 / t(30) - 1 / t(45)); assert round(h2, 2) == 136.60 and abs(h2 - 100 / (math.sqrt(3) - 1)) < 1e-9
assert abs(h2 / t(45) - (h2 / t(30) - 100)) < 1e-9 and round(h2 / t(45), 2) == 136.60 and round(h2 / t(30) - h2 / t(45), 2) == 100.0
f = Fig(780, 320)
f.text(180, 22, "(a) One angle", size=11.5, color=NAVY, bold=True)
f.line(30, 260, 330, 260, color=SLATE, sw=2); f.line(300, 260, 300, 90, color=NAVY, sw=3)
f.line(60, 260, 300, 90, color=TEAL, sw=1.6, dash=True)
f.text(180, 284, "50 m", size=11, color=SLATE, bold=True); f.text(318, 175, "h", size=13, color=NAVY, bold=True)
f.text(110, 245, "30 deg", size=10.5, color=RED, bold=True)
f.text(180, 120, "h = 50 tan 30 = 50 x 0.5774", size=11, color=NAVY, bold=True); f.text(180, 142, "= 28.87 m", size=11.5, color=RED, bold=True)
f.text(580, 22, "(b) Two angles, baseline 100 m", size=11.5, color=NAVY, bold=True)
f.line(400, 260, 760, 260, color=SLATE, sw=2); f.line(730, 260, 730, 70, color=NAVY, sw=3)
f.line(430, 260, 730, 70, color=TEAL, sw=1.4, dash=True); f.line(600, 260, 730, 70, color=AMBER, sw=1.4, dash=True)
f.text(515, 284, "100 m", size=11, color=SLATE, bold=True); f.text(665, 284, "d", size=11, color=SLATE, bold=True)
f.text(470, 245, "30", size=10.5, color=TEAL, bold=True); f.text(618, 245, "45", size=10.5, color=AMBER, bold=True)
f.text(396, 48, "tan 45: h = d", size=10.5, color=SLATE, anchor="start"); f.text(396, 68, "tan 30: h = (d + 100)/sqrt3", size=10.5, color=SLATE, anchor="start")
f.text(396, 92, "h = 100 / (sqrt3 - 1) = 136.60 m", size=11, color=RED, bold=True, anchor="start")
f.text(396, 112, "d = 136.60 m from the base", size=10.5, color=SLATE, anchor="start")
```

```svgfig label="8.5" caption="Triangle rules on the triangle with sides 5, 7, 8. The cosine rule gives cos A = (5^2 + 8^2 - 7^2)/(2 x 5 x 8) = 0.5, so the angle opposite the side 7 is 60 degrees. Area = (1/2) x 5 x 8 x sin 60 = 17.32, which Heron's formula confirms (s = 10, area = sqrt(10 x 5 x 3 x 2)). The sine rule 7 / sin 60 = 2R gives circumradius R = 4.04."
import math
a, b, c = 7, 5, 8
cosA = (b * b + c * c - a * a) / (2 * b * c); A = math.degrees(math.acos(cosA)); assert round(cosA, 6) == 0.5 and round(A, 6) == 60
area = 0.5 * b * c * math.sin(math.radians(A)); s = (a + b + c) / 2; heron = math.sqrt(s * (s - a) * (s - b) * (s - c))
assert round(area, 2) == round(heron, 2) == 17.32 and round(a / math.sin(math.radians(A)) / 2, 2) == 4.04
f = Fig(780, 320)
sc = 34; B = (60, 270); C = (60 + 8 * sc, 270)
x = (b * b + c * c - a * a) / (2 * c); y = math.sqrt(b * b - x * x); Pt = (B[0] + x * sc, B[1] - y * sc)
f.poly([B, C, Pt], fill="#dbeafe", stroke=NAVY, sw=2)
f.text((B[0] + C[0]) / 2, 292, "c = 8", size=11.5, color=NAVY, bold=True); f.text(B[0] + 40, 190, "b = 5", size=11.5, color=NAVY, bold=True, anchor="end")
f.text((Pt[0] + C[0]) / 2 + 30, 180, "a = 7", size=11.5, color=NAVY, bold=True); f.text(Pt[0] + 6, Pt[1] - 10, "A = 60 deg", size=11, color=RED, bold=True)
f.text(560, 30, "Rules", size=11.5, color=NAVY, bold=True)
for j, (t, col) in enumerate([("sine rule: a / sinA = b / sinB = c / sinC = 2R", NAVY), ("cosine rule: a^2 = b^2 + c^2 - 2bc cosA", NAVY), ("cos A = (25 + 64 - 49) / 80 = 0.5", SLATE), ("A = 60 degrees", RED), ("area = (1/2) bc sinA = 20 x 0.866 = 17.32", SLATE), ("Heron: s = 10, sqrt(10 x 5 x 3 x 2) = 17.32", TEAL), ("2R = 7 / sin 60 = 8.083, R = 4.04", SLATE), ("angles add to 180; longest side faces", SLATE), ("the largest angle", SLATE)]):
    f.text(380, 62 + j * 27, t, size=10.5, color=col, anchor="start", bold=(col in (NAVY, RED)))
```

## 8.5 Eight traps in trigonometry

Trigonometry has fewer ideas than algebra but more places to slip on a sign. These eight traps cover the identity, equation and height-and-distance questions of the model paper.

1. **Learn the standard values with the 0-1-2-3-4 rule.** The sines of 0, 30, 45, 60, 90 degrees are $\frac{\sqrt0}{2},\frac{\sqrt1}{2},\frac{\sqrt2}{2},\frac{\sqrt3}{2},\frac{\sqrt4}{2}$, and the cosines run in the opposite order (Fig 8.1). So $\sin30^\circ=\frac12$ but $\cos30^\circ=\frac{\sqrt3}{2}$. A common error is to swap them, and $\tan45^\circ=1$ is the value that is never mixed up.
2. **Fix the sign by the quadrant (ASTC).** $\sin150^\circ=+\frac12$, $\cos120^\circ=-\frac12$ and $\tan135^\circ=-1$. Reduce the angle to an acute one first, then attach the sign of the quadrant. Remember $\sin(180^\circ-\theta)=\sin\theta$ and $\cos(180^\circ-\theta)=-\cos\theta$.
3. **The three Pythagorean identities.** $\sin^2\theta+\cos^2\theta=1$, $1+\tan^2\theta=\sec^2\theta$ and $1+\cot^2\theta=\operatorname{cosec}^2\theta$. Expressions such as $(\sin\theta+\cos\theta)^2$ expand to $1+\sin2\theta$. Do not cancel $\sin$ from $\sin(A+B)$ as if it were a factor.
4. **Compound angles do not distribute.** $\sin(A+B)\neq\sin A+\sin B$; the true rule is $\sin A\cos B+\cos A\sin B$ (Fig 8.2). For cosine the sign flips: $\cos(A+B)=\cos A\cos B-\sin A\sin B$. Use $75^\circ=45^\circ+30^\circ$ to get $\sin75^\circ=\frac{\sqrt6+\sqrt2}{4}$.
5. **Pick the right form of $\cos2A$.** $\cos2A=\cos^2A-\sin^2A=2\cos^2A-1=1-2\sin^2A$, and the choice depends on what is given. Also $\sin2A=2\sin A\cos A$ and $\sin3A=3\sin A-4\sin^3A$. For half angles the sign of the root comes from the quadrant of $\frac A2$, not of $A$.
6. **For equations, list all solutions in the interval.** $\sin x=\frac12$ has two solutions in $[0^\circ,360^\circ)$, namely 30 and 150 (Fig 8.3). The general solutions are $x=n\pi+(-1)^n\alpha$ for sine, $2n\pi\pm\alpha$ for cosine and $n\pi+\alpha$ for tangent. Never divide by $\sin x$ in $\sin x\cos x=\sin x$, because you lose the roots with $\sin x=0$.
7. **Inverse functions give principal values only.** $\sin^{-1}x\in[-\frac\pi2,\frac\pi2]$, $\cos^{-1}x\in[0,\pi]$ and $\tan^{-1}x\in(-\frac\pi2,\frac\pi2)$. So $\sin^{-1}(\sin150^\circ)=30^\circ$, not 150. Also $\sin^{-1}x+\cos^{-1}x=\frac\pi2$, and $\sin^{-1}x$ does not mean $\frac1{\sin x}$.
8. **Draw the triangle and measure elevation from the horizontal.** The angle of elevation is between the line of sight and the horizontal, so for a tower of height $h$ at distance $d$ we have $\tan\theta=\frac hd$ (Fig 8.4). With two sightings use $h=\frac{x}{\cot\alpha-\cot\beta}$. For a general triangle use the sine rule $\frac{a}{\sin A}=2R$ and the cosine rule, and check that the longest side faces the largest angle (Fig 8.5).

### 8.5.1 Worked checks

**Q. Find the exact value of $\sin75^\circ$ and of $\cos15^\circ$.**

**Answer.** $\sin75^\circ=\sin(45^\circ+30^\circ)=\frac{1}{\sqrt2}\cdot\frac{\sqrt3}{2}+\frac1{\sqrt2}\cdot\frac12=\frac{\sqrt3+1}{2\sqrt2}=\frac{\sqrt6+\sqrt2}{4}\approx0.9659$. Since $\cos15^\circ=\sin75^\circ$, the second value is the same. Check numerically with a calculator in degree mode.

**Q. Solve $2\sin^2x-\sin x-1=0$ for $0^\circ\le x<360^\circ$.**

**Answer.** Factorise: $(2\sin x+1)(\sin x-1)=0$, so $\sin x=1$ or $\sin x=-\frac12$. The first gives $x=90^\circ$. The second needs the third and fourth quadrants: $x=210^\circ$ and $330^\circ$. So $x=90^\circ,210^\circ,330^\circ$, as marked in Fig 8.3.

**Q. The angle of elevation of the top of a tower is $30^\circ$ from a point 50 m from its foot. Find its height. What if a second point 100 m nearer gives $45^\circ$ and the distance is unknown?**

**Answer.** First case: $h=50\tan30^\circ=\frac{50}{\sqrt3}=28.87$ m. Second case: $h=\frac{100}{\cot30^\circ-\cot45^\circ}=\frac{100}{\sqrt3-1}=136.6$ m, as in Fig 8.4.

## Formula and fact sheet

| Item | Result |
|---|---|
| Pythagorean | $\sin^2\theta+\cos^2\theta=1$ |
| Double angle | $\sin2A=2\sin A\cos A$, $\cos2A=1-2\sin^2A$ |
| Sum | $\tan(A+B)=\frac{\tan A+\tan B}{1-\tan A\tan B}$ |
| $\sin\theta=0$ | $\theta=n\pi$ |
| Sine rule | $\frac{a}{\sin A}=2R$ |

## Chapter summary

- Memorise the 0°–90° table; every other value reduces to it.
- Complementary angles swap sin with cos, tan with cot.
- Three forms of $\cos2A$; pick the one that fits the data.
- General solution needs $n\pi$ for tan and sine, $2n\pi$ for cosine.
- In height problems, draw a right triangle and use tan.

## Practice questions

**Set A — Recall (20 questions)**

1. The value of $\cos0^\circ$ is
   (a) 0 (b) 1 (c) $\frac{1}{2}$ (d) $-1$
2. The value of $\sin30^\circ$ is
   (a) $\frac{\sqrt{3}}{2}$ (b) 1 (c) $\frac{1}{\sqrt{2}}$ (d) $\frac{1}{2}$
3. $\sin^2\theta+\cos^2\theta$ equals
   (a) 1 (b) 0 (c) 2 (d) $\sin2\theta$
4. The value of $\tan45^\circ$ is
   (a) 0 (b) $\sqrt{3}$ (c) 1 (d) $\frac{1}{\sqrt{3}}$
5. $180^\circ$ in radians is
   (a) $\frac{\pi}{2}$ (b) $\pi$ (c) $2\pi$ (d) $\frac{3\pi}{2}$
6. $\sec\theta$ equals
   (a) $\frac{1}{\sin\theta}$ (b) $\frac{1}{\tan\theta}$ (c) $\cos\theta$ (d) $\frac{1}{\cos\theta}$
7. $\sin(90^\circ-\theta)$ equals
   (a) $\sin\theta$ (b) $-\cos\theta$ (c) $\cos\theta$ (d) $\tan\theta$
8. $1+\tan^2\theta$ equals
   (a) $\sec^2\theta$ (b) $\csc^2\theta$ (c) $\cot^2\theta$ (d) 1
9. The value of $\tan60^\circ$ is
   (a) $\frac{1}{\sqrt{3}}$ (b) 1 (c) $\frac{1}{2}$ (d) $\sqrt{3}$
10. $\sin2A$ equals
    (a) $2\sin A$ (b) $2\sin A\cos A$ (c) $\sin^2A$ (d) $\cos^2A-\sin^2A$
11. $\sin(A+B)$ equals
    (a) $\sin A\cos B+\cos A\sin B$ (b) $\sin A\sin B+\cos A\cos B$ (c) $\sin A\cos B-\cos A\sin B$ (d) $\cos A\cos B-\sin A\sin B$
12. $\cos2A$ equals
    (a) $2\cos^2A+1$ (b) $2\sin^2A-1$ (c) $1-2\sin^2A$ (d) $1+2\sin^2A$
13. The value of $\cos90^\circ$ is
    (a) 1 (b) $-1$ (c) $\frac{1}{2}$ (d) 0
14. $30^\circ$ in radians is
    (a) $\frac{\pi}{6}$ (b) $\frac{\pi}{3}$ (c) $\frac{\pi}{4}$ (d) $\frac{\pi}{2}$
15. The range of $\sin x$ is
    (a) $[0,1]$ (b) $[-1,1]$ (c) all real numbers (d) $[-\pi,\pi]$
16. In which quadrant is $\sin\theta$ positive and $\cos\theta$ negative?
    (a) first (b) third (c) second (d) fourth
17. The period of $\sin x$ is
    (a) $\pi$ (b) $\frac{\pi}{2}$ (c) $4\pi$ (d) $2\pi$
18. The value of $\sin^{-1}\frac{1}{2}$ is
    (a) $\frac{\pi}{3}$ (b) $\frac{\pi}{6}$ (c) $\frac{\pi}{4}$ (d) $\frac{\pi}{2}$
19. $\cot\theta$ equals
    (a) $\frac{\cos\theta}{\sin\theta}$ (b) $\frac{\sin\theta}{\cos\theta}$ (c) $\frac{1}{\cos\theta}$ (d) $\frac{1}{\sin\theta}$
20. The value of $\csc30^\circ$ is
    (a) $\frac{1}{2}$ (b) $\sqrt{2}$ (c) 2 (d) $\sqrt{3}$

::: note Answers and explanations — Set A
**1.** (b) — cos 0° = 1.
**2.** (d) — sin 30° = 1/2; (a) is sin 60°.
**3.** (a) — the Pythagorean identity.
**4.** (c) — equal legs in a 45° triangle.
**5.** (b) — π rad = 180°.
**6.** (d) — sec is the reciprocal of cos, not sin.
**7.** (c) — complementary angle.
**8.** (a) — divide sin² + cos² = 1 by cos².
**9.** (d) — tan 60° = √3; (a) is tan 30°.
**10.** (b) — double-angle formula; (d) is cos 2A.
**11.** (a) — signs are + for sin of a sum.
**12.** (c) — cos 2A = 1 − 2 sin²A.
**13.** (d) — cos 90° = 0.
**14.** (a) — 30 × π/180 = π/6.
**15.** (b) — sin lies between −1 and 1.
**16.** (c) — second quadrant: sin +, cos −.
**17.** (d) — sin repeats every 2π (tan every π).
**18.** (b) — sin 30° = 1/2.
**19.** (a) — cot = cos/sin.
**20.** (c) — 1 / sin 30° = 2.
:::

**Set B — Understanding (12 questions)**

1. If $\sin\theta=\frac{3}{5}$ with $\theta$ acute, then $\tan\theta$ is
   (a) $\frac{4}{3}$ (b) $\frac{3}{5}$ (c) $\frac{3}{4}$ (d) $\frac{5}{4}$
2. The value of $\sin60^\circ\cos30^\circ+\cos60^\circ\sin30^\circ$ is
   (a) 1 (b) 0 (c) $\frac{1}{2}$ (d) $\frac{\sqrt{3}}{2}$
3. If $\cos\theta=\frac{3}{5}$, then $\cos2\theta$ is
   (a) $\frac{7}{25}$ (b) $\frac{6}{5}$ (c) $\frac{18}{25}$ (d) $-\frac{7}{25}$
4. The shadow of a tower is $\sqrt{3}$ times its height. The angle of elevation of the sun is
   (a) 60° (b) 30° (c) 45° (d) 15°
5. If $\tan\theta=1$ with $0^\circ<\theta<90^\circ$, then $\sin\theta+\cos\theta$ is
   (a) $\sqrt{2}$ (b) 1 (c) 2 (d) $\frac{1}{\sqrt{2}}$
6. The value of $\tan30^\circ\tan60^\circ$ is
   (a) 0 (b) 2 (c) 1 (d) $\sqrt{3}$
7. The general solution of $\sin\theta=0$ is
   (a) $2n\pi$ (b) $(2n+1)\frac{\pi}{2}$ (c) $\frac{n\pi}{2}$ (d) $n\pi$
8. $\sin^{-1}x+\cos^{-1}x$ equals
   (a) $\pi$ (b) $\frac{\pi}{2}$ (c) 0 (d) $\frac{\pi}{4}$
9. In a triangle $a=5$ and $A=30^\circ$. The circumradius $R$ is
   (a) 10 (b) 2.5 (c) 5 (d) 7.5
10. From a point 20 m away the angle of elevation of the top of a pole is 45°. The height of the pole is
    (a) 10 m (b) $20\sqrt{3}$ m (c) 40 m (d) 20 m
11. $(1+\tan^2\theta)\cos^2\theta$ equals
    (a) 1 (b) $\sin^2\theta$ (c) $\tan^2\theta$ (d) 0
12. If $\tan\theta=\frac{1}{2}$, then $\sin2\theta$ is
    (a) $\frac{3}{5}$ (b) $\frac{4}{5}$ (c) $\frac{1}{2}$ (d) $\frac{2}{5}$

::: note Answers and explanations — Set B
**1.** (c) — 3-4-5 triangle: tan = 3/4.
**2.** (a) — it is sin(60° + 30°) = sin 90° = 1.
**3.** (d) — 2(9/25) − 1 = −7/25.
**4.** (b) — tan θ = h/shadow = 1/√3.
**5.** (a) — θ = 45°: 2 × (1/√2) = √2.
**6.** (c) — (1/√3)(√3) = 1.
**7.** (d) — sine vanishes at every multiple of π.
**8.** (b) — complementary inverse functions.
**9.** (c) — 2R = 5 / (1/2) = 10.
**10.** (d) — tan 45° = 1, so height = distance.
**11.** (a) — sec² × cos² = 1.
**12.** (b) — 2t/(1 + t²) = 1/1.25 = 4/5.
:::

**Set C — Application (8 questions)**

1. If $\sec\theta=\frac{5}{4}$ and $\theta$ is acute, then $\tan\theta$ is
   (a) $\frac{4}{3}$ (b) $\frac{5}{3}$ (c) $\frac{4}{5}$ (d) $\frac{3}{4}$
2. A 10 m ladder makes 60° with the ground. The height it reaches is
   (a) $5\sqrt{3}$ m (b) 5 m (c) $10\sqrt{3}$ m (d) $\frac{10}{\sqrt{3}}$ m
3. The sum of the solutions of $\cos\theta=\frac{1}{2}$ in $[0,2\pi]$ is
   (a) $\pi$ (b) $\frac{5\pi}{3}$ (c) $2\pi$ (d) $\frac{\pi}{3}$
4. The value of $2\sin15^\circ\cos15^\circ$ is
   (a) 1 (b) $\frac{1}{2}$ (c) $\frac{\sqrt{3}}{2}$ (d) $\frac{1}{4}$
5. If $\tan A=\frac{1}{2}$ and $\tan B=\frac{1}{3}$, then $\tan(A+B)$ is
   (a) $\frac{5}{6}$ (b) $\frac{1}{6}$ (c) $\frac{5}{7}$ (d) 1
6. The area of a triangle with sides 6 and 8 and included angle 30° is
   (a) 12 (b) 24 (c) $12\sqrt{3}$ (d) 48
7. The maximum value of $3\sin\theta+4\cos\theta$ is
   (a) 7 (b) 12 (c) 5 (d) 1
8. The maximum value of $\sin\theta\cos\theta$ is
   (a) 1 (b) $\frac{1}{2}$ (c) 2 (d) $\frac{1}{4}$

::: note Answers and explanations — Set C
**1.** (d) — cos = 4/5, sin = 3/5, tan = 3/4.
**2.** (a) — 10 sin 60° = 5√3.
**3.** (c) — solutions π/3 and 5π/3, sum 2π.
**4.** (b) — it is sin 30° = 1/2.
**5.** (d) — (5/6)/(1 − 1/6) = 1, so A + B = 45°.
**6.** (a) — ½ · 6 · 8 · ½ = 12.
**7.** (c) — √(9 + 16) = 5.
**8.** (b) — ½ sin 2θ ≤ ½.
:::
