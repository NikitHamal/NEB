---
subject: Physics
grade: CEE
unit: 18
title: Electrons and Photons
hours: 3
area: Modern Physics
---

Modern Physics carries **12 of the 50 Physics questions** (official MEC weightage),
and we estimate about **3** come from this chapter. They divide into two halves.
The first half is the electron as a particle: how a beam of electrons bends in an
electric or a magnetic field, how Thomson weighed its charge against its mass, and
how Millikan caught the charge itself. The second half is the photon: $E = hf$,
$p = h/\lambda$, and the photoelectric effect, where the particle picture of light
was forced on physics. Both halves are formula-light and idea-heavy, so the marks
go to the student who can say *why*, not only *what*.

::: key What the paper asks from this chapter
- Electron in a field **along** its motion: accelerated, $v=\sqrt{2eV/m}$.
- Electron in a **transverse** electric field: a parabolic path, $y=\frac{1}{2}at^2=\frac{eEx^2}{2mv^2}$ — the oscilloscope.
- Electron in a magnetic field: a circle of radius $r=\frac{mv}{eB}$; the period $T=\frac{2\pi m}{eB}$ does not depend on speed.
- Thomson's crossed fields: undeflected when $eE=evB$, so $v=E/B$ and then $e/m=\frac{E}{B^2r}$.
- Millikan: a charged drop held stationary has $qE=mg$; every charge found is a whole multiple of $e$.
- Photon energy $E=hf=hc/\lambda$ and momentum $p=h/\lambda$; $hc\approx1240$ eV nm.
- The four experimental laws of the photoelectric effect, and exactly why the wave theory fails each.
- Einstein's equation $hf=\phi+K_{max}$; threshold $f_0=\phi/h$; stopping potential $eV_0=K_{max}$; the $V_0$–$f$ line with slope $h/e$ and intercept $-\phi/e$.
- Intensity sets the **number** of photons, hence the saturation current; frequency sets the **energy** of each photon, hence the stopping potential.
:::

## 18.1 Motion of an electron in electric and magnetic fields

An electron carries charge $-e=-1.6\times10^{-19}$ C and mass
$m=9.11\times10^{-31}$ kg. In a field it obeys Newton's second law with the
**Lorentz force**

$$ \vec F = -e\vec E - e\,\vec v\times\vec B $$

The electric part acts along the field line (backwards, because the charge is
negative); the magnetic part acts at right angles to both $\vec v$ and $\vec B$.
That single difference in direction produces two completely different paths.

### 18.1.1 Field along the motion: acceleration

If the electron starts from rest and falls through a potential difference $V$, the
work done on it is $eV$ and this becomes kinetic energy:

$$ eV = \frac{1}{2}mv^2 \qquad\Longrightarrow\qquad v=\sqrt{\frac{2eV}{m}} $$

For $V=1000$ V this gives $v=1.87\times10^{7}$ m s⁻¹ — about 6 % of the speed of
light, so the classical formula is still acceptable here. Notice the two
proportionalities that the paper likes: **$v\propto\sqrt{V}$** and
**$K\propto V$**. Doubling the voltage multiplies the speed by $\sqrt{2}$, not by 2.

The same formula is used in reverse in an X-ray tube or a cathode-ray tube: the
accelerating voltage fixes the energy of every electron in the beam, and therefore
the shortest X-ray wavelength the tube can produce.

### 18.1.2 Transverse electric field: the parabolic path

Now let the electron enter with velocity $v$ **perpendicular** to a uniform field
between two parallel plates. This is the deflector of a cathode-ray oscilloscope.

Inside the plates the electron feels a constant force $eE$ at right angles to its
velocity. The motion is exactly the projectile problem of Chapter 1, with $g$
replaced by $a=eE/m$:

- along the plates: **uniform velocity** $v$ (no force in that direction), so
  $x=vt$ and $t=x/v$;
- across the plates: **uniform acceleration** $a=eE/m$ starting from zero
  perpendicular velocity.

Therefore

$$ y=\frac{1}{2}at^2=\frac{eE}{2m}\left(\frac{x}{v}\right)^2=\frac{eEx^2}{2mv^2} $$

which is a **parabola**. At the exit from plates of length $L$ the deflection is

$$ y_1=\frac{eEL^2}{2mv^2}, \qquad \tan\theta=\frac{v_y}{v}=\frac{eEL}{mv^2} $$

and the beam then travels in a straight line, so on a screen a distance $D$ beyond
the plates the total deflection is $y=y_1+D\tan\theta$.

```figure caption="An electron beam crossing a transverse field. Between the plates the path is a parabola; after leaving them it is a straight line. The deflecting voltage is what moves the spot on the screen, which is the whole principle of the cathode-ray oscilloscope."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.9))
ax.add_patch(plt.Rectangle((2.0,1.0),4.0,0.09, fc=MUTED, ec='none'))
ax.add_patch(plt.Rectangle((2.0,-1.09),4.0,0.09, fc=MUTED, ec='none'))
for xx in (2.7,3.7,4.7,5.7):
    ax.text(xx,1.22,'+',ha='center',va='bottom',fontsize=10,color=INK)
    ax.text(xx,-1.22,'−',ha='center',va='top',fontsize=10,color=INK)
x1 = np.linspace(2.0,6.0,120); y1 = 0.05*(x1-2.0)**2
ax.plot([0.4,2.0],[0,0],color=ACCENT,lw=1.9)
ax.plot(x1,y1,color=ACCENT,lw=1.9)
ax.plot([6.0,10.0],[0.8,2.4],color=ACCENT,lw=1.9)
ax.annotate('', xy=(1.55,0.0), xytext=(0.75,0.0),
            arrowprops=dict(arrowstyle='-|>',color=INK,lw=0.9,mutation_scale=9))
ax.text(0.80,0.14,'$v_0$',fontsize=9,color=INK)
ax.annotate('', xy=(2.62,0.26), xytext=(2.62,0.84),
            arrowprops=dict(arrowstyle='-|>',color='#A8271F',lw=1.0,mutation_scale=9))
ax.text(2.72,0.50,'$E$',fontsize=9,color='#A8271F')
ax.plot([6.0,6.0],[0,0.8],ls=':',lw=0.9,color=MUTED)
ax.text(6.10,0.36,'$y_1$',fontsize=9,color=INK)
ax.plot([10.0,10.0],[-2.2,3.05],color=INK,lw=1.6)
ax.text(10.14,-1.80,'screen',fontsize=8.5,color=INK,rotation=90,va='bottom')
ax.plot([9.72,9.72],[0,2.29],ls=':',lw=0.9,color=MUTED)
ax.text(9.58,1.05,'$y$',fontsize=9,color=INK,ha='right')
ax.text(4.0,-1.95,'plates:  separation $d$,  length $L$',fontsize=8.5,color=MUTED,ha='center')
ax.set_xlim(0.2,11.0); ax.set_ylim(-2.3,3.2)
ax.axis('off')
```

::: derivation Deflection in a transverse field, and why a CRO reads volts
**Setting up.** Plates of length $L$ and separation $d$ carry a deflecting voltage
$V_d$, so $E=V_d/d$. The beam was accelerated through $V_a$, so $\frac{1}{2}mv^2=eV_a$.

**Step 1 — time in the field.** The horizontal velocity does not change, so
$t=L/v$.

**Step 2 — sideways acceleration.** $a=eE/m=eV_d/(md)$.

**Step 3 — deflection at the exit.** $y_1=\frac{1}{2}at^2
=\frac{eV_d}{2md}\cdot\frac{L^2}{v^2}$.

**Step 4 — put in the speed.** From $\frac{1}{2}mv^2=eV_a$, $mv^2=2eV_a$. Substituting,

$$ y_1=\frac{eV_dL^2}{2md}\cdot\frac{m}{2eV_a}=\frac{V_dL^2}{4dV_a} $$

**Result.** $y_1=\dfrac{V_dL^2}{4dV_a}$, and the spot deflection is proportional to it.

**What it means.** The charge and mass of the electron have cancelled. A cathode-ray
tube therefore deflects by an amount fixed by its **geometry and its voltages alone**,
which is why an oscilloscope can be calibrated in volts per centimetre. The same
cancellation is why the tube works the same with any charged particle of the same
energy per charge.
:::

::: example Worked example 18.1 — the oscilloscope spot
**Problem.** In a cathode-ray tube the deflecting plates are 2.0 cm long and 1.0 cm
apart, and the beam is accelerated through 1000 V. Find the deflection at the exit
when the deflecting voltage is 100 V.

**Solution.** $y_1=\dfrac{V_dL^2}{4dV_a}
=\dfrac{100\times(0.020)^2}{4\times0.010\times1000}
=\dfrac{100\times4.0\times10^{-4}}{40}=1.0\times10^{-3}$ m $=1.0$ mm.

**Check.** At 200 V the spot moves to 2.0 mm: the deflection is linear in $V_d$,
which is the property the instrument is sold on.
:::

::: caution Two things the deflection does not depend on
$y_1$ does **not** depend on $e/m$, and it does **not** depend on the speed
separately — the speed is already fixed by $V_a$. What it does depend on is
$1/V_a$: increasing the accelerating voltage makes the beam stiffer and the spot
deflection smaller. Students often say "a faster electron is deflected more"; the
opposite is true.
:::

### 18.1.3 Magnetic field: the circular path

A charge moving in a magnetic field feels $F=evB\sin\theta$, always perpendicular
to $\vec v$. A force perpendicular to the velocity does **no work**: it changes the
direction of motion but never the speed or the kinetic energy. The path is therefore
a **circle** at constant speed, and the magnetic force supplies the centripetal
force:

$$ evB=\frac{mv^2}{r} \qquad\Longrightarrow\qquad r=\frac{mv}{eB}=\frac{p}{eB} $$

The period follows at once:

$$ T=\frac{2\pi r}{v}=\frac{2\pi m}{eB} $$

which contains no $v$: **all electrons of the same charge and mass take the same time
for one turn, however fast they are moving.** Faster electrons simply travel a bigger
circle. This is the principle of the cyclotron.

If the velocity has a component along $\vec B$ as well as across it, the across part
makes a circle and the along part carries the particle forward at constant speed; the
two together trace a **helix**.

| Field | Force on the electron | Path | Speed |
|---|---|---|---|
| $\vec E$ parallel to $\vec v$ | $eE$, along the line | straight line, accelerated | changes |
| $\vec E$ perpendicular to $\vec v$ | $eE$, constant | parabola | constant along the plates, $v_y$ grows |
| $\vec B$ perpendicular to $\vec v$ | $evB$, always perpendicular to $\vec v$ | circle | constant |
| $\vec B$ at an angle to $\vec v$ | $evB\sin\theta$ | helix | constant |

::: example Worked example 18.2 — radius and period
**Problem.** An electron moves at $1.0\times10^{7}$ m s⁻¹ perpendicular to a field of
$1.0\times10^{-2}$ T. Find the radius of its path and the time for one revolution.

**Solution.** $r=\dfrac{mv}{eB}
=\dfrac{9.11\times10^{-31}\times1.0\times10^{7}}{1.6\times10^{-19}\times1.0\times10^{-2}}
=\dfrac{9.11\times10^{-24}}{1.6\times10^{-21}}=5.7\times10^{-3}$ m $=5.7$ mm.

$T=\dfrac{2\pi r}{v}=\dfrac{2\pi\times5.69\times10^{-3}}{1.0\times10^{7}}
=3.6\times10^{-9}$ s.

**Check.** The same $T$ comes from $2\pi m/eB$ alone, so an electron at twice the speed
would circle a radius of 11 mm in the same 3.6 ns.
:::

::: tip Comparing two particles in the same field
In the same field, $r=mv/qB$. At the **same speed**, $r\propto m/q$; at the
**same accelerating voltage**, $r\propto\sqrt{m/q}$; at the **same kinetic energy**,
$r\propto\sqrt{m/q}$ as well, because $p=\sqrt{2mK}$. An alpha particle and a proton
with equal speeds have radii in the ratio $2:1$ (charge-to-mass ratio halved), and
the ratio of their periods is also $2:1$.
:::

## 18.2 J. J. Thomson's experiment and Millikan's oil-drop experiment

### 18.2.1 Cathode rays and thermionic emission

When a high voltage is applied across a gas at low pressure in a discharge tube, a
stream of particles leaves the cathode and travels in straight lines. These **cathode
rays** were shown to be deflected towards the positive plate, to blacken a
photographic plate, to make certain minerals fluoresce and to ionise the gas they
passed through — so they are streams of **negative** particles.

```photo id="phy12/thomson" caption="J. J. Thomson at work with a cathode-ray tube (colourised photograph)." width="60"
```


In 1897 J. J. Thomson measured the ratio of their charge to their mass. The ratio
came out at about $1.76\times10^{11}$ C kg⁻¹, more than a thousand times the value for
a hydrogen ion ($9.58\times10^{7}$ C kg⁻¹). Since the value did not change when the
gas in the tube or the metal of the cathode was changed, these particles must be a
**common constituent of all matter**. They were named **electrons**.

Electrons are also freed by heating: a metal filament heated to about 2000 °C or more emits
electrons from its surface. This is **thermionic emission**, the source of electrons
in a cathode-ray tube, an X-ray tube and the old valve radios. It works because the
electrons in a hot metal have a distribution of energies, and the fastest of them
have enough energy to escape the attraction of the positive ions they leave behind.

```photo id="phy12/millikan" caption="The viewing microscope of a Millikan oil-drop apparatus (teaching model). The drop is watched between the charged plates through this eyepiece." width="55"
```


### 18.2.2 The crossed-field measurement of e/m

Thomson's tube had two sets of deflectors at right angles: an electric field $E$
between plates, and a magnetic field $B$ from a coil, arranged so that the two forces
on the electron were opposite.

1. **Both fields on.** The electric force $eE$ and the magnetic force $evB$ pull in
   opposite directions. Adjust the fields until the spot returns to zero. Then the
   forces balance and the electron travels in a straight line:

   $$ eE=evB \qquad\Longrightarrow\qquad v=\frac{E}{B} $$

2. **Electric field off.** Only the magnetic force acts, so the electron moves in a
   circle of radius $r$, which is measured from the position of the spot on the
   fluorescent screen. Then

   $$ \frac{e}{m}=\frac{v}{Br}=\frac{E}{B^2r} $$

Every quantity on the right is measured, so $e/m$ is found without knowing $e$ or $m$
separately. Thomson's number was about $1.76\times10^{11}$ C kg⁻¹ (modern value
$1.759\times10^{11}$).

::: caution What Thomson did and did not measure
Thomson measured the **ratio** $e/m$, not $e$ and not $m$. From $e/m$ alone the
electron could be a particle of small charge and tiny mass or of large charge and
larger mass. The mass was only pinned down once Millikan measured $e$ (from 1909
onwards); then $m=e/(e/m)=1.6\times10^{-19}/1.76\times10^{11}=9.1\times10^{-31}$ kg.
:::

### 18.2.3 Millikan's oil-drop experiment

Millikan's apparatus sprays a fine mist of oil into a chamber between two horizontal
plates. The droplets are charged by friction in the nozzle and by X-rays that ionise
the air. A microscope with a graduated eyepiece watches one drop.

- **Field off.** The drop falls, and air resistance quickly makes it fall at a
  steady **terminal velocity**. Stokes' law, $6\pi\eta rv_t=mg$, then gives the
  radius $r$ of the drop, and hence its mass from the density of the oil.
- **Field on.** The plates are charged so that the electric force on the drop acts
  **upwards**. The voltage is adjusted until the drop hangs **stationary**.

Why stationary? Because a stationary drop has **zero velocity, so the viscous drag is
zero** (drag depends on speed). The only vertical forces left are the electric force
and the weight, and they must balance exactly:

$$ qE=mg \qquad\Longrightarrow\qquad q=\frac{mg}{E}=\frac{mgd}{V} $$

There is no drag term and no correction for speed to worry about — that is the whole
elegance of holding the drop still.

```figure caption="The forces on a charged oil drop held stationary between the plates. With the drop at rest the viscous drag is zero, so the upward electric force balances the weight exactly: $qE = mg$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.4,3.0))
ax.add_patch(plt.Rectangle((1.0,3.0),5.2,0.10, fc=MUTED, ec='none'))
ax.add_patch(plt.Rectangle((1.0,0.0),5.2,0.10, fc=MUTED, ec='none'))
ax.text(3.6,3.22,'+   +   +   +   +',ha='center',va='bottom',fontsize=10,color=INK)
ax.text(3.6,-0.22,'−   −   −   −   −',ha='center',va='top',fontsize=10,color=INK)
ax.add_patch(Circle((3.0,1.55),0.16, fc='#D9E4F2', ec=ACCENT, lw=1.2, zorder=5))
ax.annotate('', xy=(3.0,2.72), xytext=(3.0,1.75),
            arrowprops=dict(arrowstyle='-|>',color=ACCENT,lw=1.3,mutation_scale=10))
ax.text(2.86,2.28,'$qE$',fontsize=10,color=ACCENT,ha='right')
ax.annotate('', xy=(3.0,0.38), xytext=(3.0,1.35),
            arrowprops=dict(arrowstyle='-|>',color='#A8271F',lw=1.3,mutation_scale=10))
ax.text(2.86,0.82,'$mg$',fontsize=10,color='#A8271F',ha='right')
ax.annotate('', xy=(4.9,1.95), xytext=(4.9,2.65),
            arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.0,mutation_scale=9))
ax.text(5.02,2.28,'$E$',fontsize=9,color=MUTED)
ax.text(3.28,1.55,'oil drop',fontsize=8.5,color=INK,ha='left',va='center')
ax.text(1.0,3.55,'stationary drop:  $qE = mg$',fontsize=9.5,color=INK,ha='left')
ax.set_xlim(0.7,6.5); ax.set_ylim(-0.6,3.8)
ax.axis('off')
```

The result was not a number but a **pattern**. However the drop was charged, and
however many times it was recharged with X-rays, the charge always came out as

$$ q=ne, \qquad n=1,2,3,\dots, \qquad e=1.60\times10^{-19}\ \text{C} $$

Millikan never found a fraction of the smallest charge. That is the experimental
basis of **quantisation of charge**: electric charge exists only in whole multiples of
the elementary charge $e$.

::: note A subtlety worth one mark
The upward force must balance the **apparent** weight, $mg$ minus the buoyancy of the
air, because the drop is in air and not in vacuum. For an oil drop of density
900 kg m⁻³ the buoyancy correction is about 0.1 %, which is why most textbook
treatments simply write $qE=mg$. If a question gives the density of air, subtract the
buoyancy.
:::

| | Thomson | Millikan |
|---|---|---|
| Measured | $e/m$ | $e$ |
| Method | deflection of an electron beam in crossed $E$ and $B$ | a charged oil drop held stationary in an electric field |
| Key relation | $e/m=E/(B^2r)$ | $q=mg/E$ |
| What it proved | electrons are a universal constituent of matter | charge is quantised in units of $e$ |
| Gave, with the other | $m=e/(e/m)=9.1\times10^{-31}$ kg | the size of the elementary charge |

::: example Worked example 18.3 — e/m from crossed fields
**Problem.** In a Thomson tube the beam is undeflected when $E=3.4\times10^{4}$ V m⁻¹
and $B=2.0\times10^{-3}$ T. With the electric field off, the beam moves in a circle of
radius 4.8 cm in the same field. Find $e/m$.

**Solution.** $v=E/B=3.4\times10^{4}/2.0\times10^{-3}=1.7\times10^{7}$ m s⁻¹.

$\dfrac{e}{m}=\dfrac{v}{Br}=\dfrac{1.7\times10^{7}}{2.0\times10^{-3}\times0.048}
=\dfrac{1.7\times10^{7}}{9.6\times10^{-5}}=1.8\times10^{11}$ C kg⁻¹.

**Check.** This is within 2 % of the accepted $1.76\times10^{11}$ C kg⁻¹ — the small
difference is the precision of the data, not a different particle.
:::

::: example Worked example 18.4 — the charge on a held drop
**Problem.** An oil drop of mass $3.2\times10^{-15}$ kg is held stationary between
plates 1.0 cm apart with a potential difference of 200 V. Find the charge on the drop
and the number of electrons it carries ($g=10$ m s⁻²).

**Solution.** $E=V/d=200/0.010=2.0\times10^{4}$ V m⁻¹.

$q=\dfrac{mg}{E}=\dfrac{3.2\times10^{-15}\times10}{2.0\times10^{4}}
=1.6\times10^{-18}$ C.

$n=q/e=1.6\times10^{-18}/1.6\times10^{-19}=10$ electrons.
:::

## 18.3 Photons and the photoelectric effect: laws and Einstein's equation

### 18.3.1 The photon

Planck had supposed that the atoms in a hot body emit energy in packets of size $hf$.
Einstein went further in 1905: **light itself is made of packets**. A **photon** is a
quantum of electromagnetic radiation, with energy and momentum

$$ E=hf=\frac{hc}{\lambda}, \qquad p=\frac{h}{\lambda}=\frac{E}{c} $$

with $h=6.63\times10^{-34}$ J s and $c=3.0\times10^{8}$ m s⁻¹. A useful working form
is $E(\text{eV})=1240/\lambda(\text{nm})$, because $hc=1.99\times10^{-25}$ J m
$\approx1240$ eV nm.

Three properties that questions turn on:

- A photon has **zero rest mass**, but it does have momentum $h/\lambda$; when it is
  absorbed or emitted, momentum is conserved.
- A photon is **uncharged**, so it is not deflected by electric or magnetic fields.
  (Gravity bends light, but not through the Lorentz force.)
- The **intensity** of a beam is the number of photons crossing unit area per second
  times the energy of each: $I=Nhf/At$. Bright red light and dim red light differ in
  $N$, not in $hf$. Red light and blue light differ in $hf$, not necessarily in $N$.

### 18.3.2 Thermionic emission and the work function

Electrons in a metal are bound by the attraction of the positive ions. To pull one
out of the surface, even from the least tightly bound states, takes a definite
minimum energy. That minimum is the **work function** $\phi$ of the metal:

::: definition Work function
The **work function** $\phi$ of a metal is the minimum energy needed to remove an
electron from its surface to a point just outside, at rest. It is a property of the
metal, quoted in electron volts (1 eV $=1.6\times10^{-19}$ J).
:::

| Metal | $\phi$ (eV) | Threshold $\lambda_0=1240/\phi$ (nm) | Which light ejects electrons |
|---|---|---|---|
| Caesium | 2.14 | 579 | visible (green and shorter) |
| Sodium | 2.28 | 544 | visible |
| Zinc | 4.3 | 288 | ultraviolet only |
| Copper | 4.7 | 264 | ultraviolet only |

The work function is not the same as the ionisation energy of a free atom, and it is
not the same for every crystal face of the same metal. For the paper, remember the
order of magnitude: **a few electron volts**, which corresponds to visible or near
ultraviolet light.

### 18.3.3 The photoelectric effect and its four laws

When light of sufficiently high frequency falls on a clean metal surface, electrons
are emitted from it. This is the **photoelectric effect**, and the emitted electrons
are **photoelectrons**. The effect is used in light meters, in photomultiplier tubes
and in the automatic doors of a supermarket.

The experiments give four laws.

| Law | Statement |
|---|---|
| 1. Threshold frequency | For each metal there is a minimum frequency $f_0$ below which **no electrons are emitted at all**, however intense the light and however long it shines. |
| 2. Maximum kinetic energy | $K_{max}$ of the photoelectrons increases with the frequency of the light and depends on the metal; it does **not** depend on the intensity. |
| 3. Current and intensity | For $f>f_0$, the number of photoelectrons emitted per second — the **saturation current** — is directly proportional to the intensity of the light. |
| 4. Instantaneity | Emission begins within about $10^{-9}$ s of the light arriving, even when the intensity is so low that only one photon arrives at a time. |

### 18.3.4 Why the wave theory fails

In the wave picture, light delivers energy continuously to the electrons in the
metal. A weak wave simply takes longer to deliver the same energy. That picture makes
three predictions, and all three are wrong.

| Wave theory predicts | What is observed | Which law is broken |
|---|---|---|
| Any frequency will do, given enough intensity or enough time: the electron can accumulate the work function from many small instalments. | Below $f_0$ there is no emission at all, even with a very intense beam. | Law 1 |
| A brighter beam delivers more energy per second, so electrons should leave faster. | $K_{max}$ is unchanged when the intensity is increased; only the number of electrons grows. | Law 2 |
| A very faint beam should need a measurable time to build up 2 eV or so on one electron. | Emission starts at once, within $10^{-9}$ s. | Law 4 |

The third row is worth a number. At an intensity of $10^{-6}$ W m⁻², the power falling
on one atom (area about $10^{-20}$ m²) is $10^{-26}$ W. To collect a work function of
2 eV $=3.2\times10^{-19}$ J at that rate would take $3.2\times10^{7}$ s, about a year.
No such delay is ever seen.

Only law 3 is *consistent* with the wave theory as well, so it cannot be used to
choose between the two pictures. The other three decide the argument, and they decide
it for the particle picture.

### 18.3.5 Einstein's equation

Einstein's postulate is that **one photon is absorbed by one electron, whole**. The
photon's energy pays the work function first, and whatever is left becomes the
electron's kinetic energy:

$$ hf=\phi+K_{max} \qquad\Longrightarrow\qquad K_{max}=hf-\phi $$

This single equation contains all four laws:

- If $hf<\phi$ there is no energy left over, so no electron can escape: **threshold**.
- $K_{max}$ rises linearly with $f$ and is fixed by $\phi$ for that metal: **law 2**.
- A brighter beam has more photons, so more electrons per second: **law 3**.
- Absorption is a single event, so there is no build-up time: **law 4**.

The **threshold frequency** and **threshold wavelength** follow by putting $K_{max}=0$:

$$ f_0=\frac{\phi}{h}, \qquad \lambda_0=\frac{hc}{\phi}=\frac{1240}{\phi(\text{eV})}\ \text{nm} $$

### 18.3.6 Stopping potential and the V₀–f graph

The fastest photoelectrons can be stopped by making the collector electrode negative.
The smallest retarding potential that just stops the current is the **stopping
potential** $V_0$, and it measures the maximum kinetic energy directly:

$$ eV_0=K_{max}=hf-\phi \qquad\Longrightarrow\qquad V_0=\frac{h}{e}f-\frac{\phi}{e} $$

So a graph of $V_0$ against $f$ is a **straight line**:

- **slope** $=h/e$, the same for every metal — this is how Millikan measured $h$;
- **intercept on the $V_0$ axis** $=-\phi/e$;
- **intercept on the $f$ axis** $=f_0=\phi/h$.

```figure caption="Stopping potential against frequency for two metals. The lines are parallel because the slope $h/e$ is a constant of nature; the intercept on the vertical axis is $-\phi/e$ and the intercept on the horizontal axis is the threshold frequency."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,3.0))
he = 4.14e-15
f = np.linspace(0,15e14,200)
for phi, c, lab in [(2.0,'#A8271F','$\phi=2.0$ eV'), (3.0,ACCENT,'$\phi=3.0$ eV')]:
    v = he*f - phi
    ax.plot(f/1e14, v, color=c, lw=1.9, label=lab)
    ax.plot([0],[-phi],'o',color=c,ms=4.5)
    ax.plot([phi/he/1e14],[0],'o',color=c,ms=4.5)
ax.axhline(0, color=INK, lw=0.8)
ax.annotate('slope $=h/e$', xy=(10.6,1.39), xytext=(8.3,-2.15), fontsize=9, color=INK,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8, mutation_scale=8))
ax.set_xlabel('frequency  $f$  ($10^{14}$ Hz)')
ax.set_ylabel('stopping potential  $V_0$  (V)')
ax.set_xlim(-0.6,15.6); ax.set_ylim(-3.6,5.2)
ax.legend(loc='upper left', fontsize=8.5, frameon=False)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

### 18.3.7 Intensity, saturation current and stopping potential

Two knobs, two different effects. This is the most examined idea in the chapter.

```figure caption="Photocurrent against applied voltage for two intensities of the same frequency. Both curves reach zero at the same stopping potential $-V_0$, because the photon energy is the same; only the saturation current changes, because a brighter beam has more photons."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
V0 = 1.5
V = np.linspace(-3.0,3.0,400)
for Is, c, lab in [(1.0,MUTED,'intensity $I$'), (2.0,ACCENT,'intensity $2I$')]:
    cur = np.where(V > -V0, Is*(1-np.exp(-(V+V0)/0.45)), 0.0)
    ax.plot(V, cur, color=c, lw=1.9, label=lab)
ax.axvline(-V0, color=INK, ls=':', lw=0.9)
ax.axhline(0, color=INK, lw=0.8)
ax.annotate('$-V_0$', xy=(-V0,0.0), xytext=(-2.92,0.62), fontsize=9, color=INK,
            ha='left', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.text(2.15,0.84,'$I$',fontsize=9,color=MUTED)
ax.text(2.15,1.84,'$2I$',fontsize=9,color=ACCENT)
ax.set_xlabel('applied voltage  $V$  (V)')
ax.set_ylabel('photocurrent  ($\\mu$A)')
ax.set_xlim(-3.1,3.1); ax.set_ylim(-0.45,2.35)
ax.set_yticks([0,1,2])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

| Change made | Saturation current | Stopping potential | $K_{max}$ |
|---|---|---|---|
| Intensity doubled, $f$ fixed | doubles | unchanged | unchanged |
| Frequency increased, intensity fixed | may fall slightly (fewer photons per second if the source power is fixed) | rises | rises |
| Metal changed to one with larger $\phi$, same light | about the same, if $f$ is still above the new threshold; zero if it is not | falls | falls |
| Distance from the lamp increased | falls (inverse square) | unchanged | unchanged |

::: caution Three traps in the photoelectric effect
1. **Work function in eV against joules.** $\phi=2.0$ eV is $3.2\times10^{-19}$ J. If
   you put 2.0 into $hf-\phi$ with $hf$ in joules, you get nonsense. Convert first:
   $E(\text{eV})=1240/\lambda(\text{nm})$ is the safe route.
2. **"No emission below threshold, however intense."** Intensity adds photons, not
   energy per photon. A thousand dim red photons cannot do what one ultraviolet photon
   does.
3. **Stopping potential is a magnitude.** $K_{max}=eV_0$ uses the size of the
   retarding voltage. The applied voltage that stops the current is $-V_0$; the
   *stopping potential* is quoted as a positive number, and on the graph the current
   reaches zero at $-V_0$.
:::

::: example Worked example 18.5 — the full photoelectric chain
**Problem.** Light of wavelength 400 nm falls on a metal of work function 2.5 eV.
Find the photon energy, the maximum kinetic energy of the photoelectrons, the
stopping potential and the threshold wavelength.

**Solution.** $E=\dfrac{1240}{400}=3.1$ eV.

$K_{max}=3.1-2.5=0.6$ eV $=0.6\times1.6\times10^{-19}=9.6\times10^{-20}$ J.

$V_0=K_{max}/e=0.6$ V.

$\lambda_0=\dfrac{1240}{2.5}=496$ nm $\approx 500$ nm, so this light (400 nm) is just
beyond the threshold and the electrons come off slowly.
:::

::: example Worked example 18.6 — counting photons
**Problem.** A sodium lamp emits 100 W of light of wavelength 589 nm. How many photons
does it emit per second?

**Solution.** $E=\dfrac{hc}{\lambda}=\dfrac{6.63\times10^{-34}\times3.0\times10^{8}}{589\times10^{-9}}
=3.38\times10^{-19}$ J.

$N=\dfrac{P}{E}=\dfrac{100}{3.38\times10^{-19}}=3.0\times10^{20}$ photons per second.

**Check.** $3\times10^{20}$ photons per second from a 100 W lamp sounds enormous, and
it is — which is why a beam of ordinary brightness still delivers its energy in
countless separate packets.
:::

::: tip Reading a photoelectric question in ten seconds
1. Convert $\lambda$ to energy in eV with $1240/\lambda$ (nm).
2. Subtract $\phi$ in eV. A negative answer means **no emission** — that is the
   answer, and no further work is needed.
3. The remainder is $K_{max}$ in eV, and numerically the same number is $V_0$ in
   volts.
4. If the question gives $V_0$ and $f$, the slope of the line is $h/e$ and the
   intercept is $-\phi/e$; if it gives two metals, the lines are parallel.
:::

```photogrid label="18.1" cols="2" ratio="1.2" caption="Einstein's photoelectric equation. (a) Light of high enough frequency ejects electrons from the cathode of a vacuum photocell. (b) For a caesium-type cathode of work function 2.1 eV (assumed) the stopping potential is V0 = (h / e) f - phi / e, a straight line of slope h / e = 4.14 x 10^-15 V s. Emission starts at the threshold frequency 5.08 x 10^14 Hz, wavelength 590 nm. Light of 400 nm gives a maximum kinetic energy of 1.00 eV, 500 nm gives 0.38 eV and 600 nm gives none, however bright it is."
@ photo id="ceephy/photocell" cap="A vacuum photocell: light on the cathode releases photoelectrons collected by the anode"
fit 1.2
focus 0.5 0.5
@ svg cap="Stopping potential against frequency (caesium, 2.1 eV)"
h = 6.626e-34; e = 1.602e-19; phi = 2.1; hc = 1239.84
f0 = phi * e / h; V0 = lambda fr: h * fr / e - phi
k = lambda nm: max(0.0, hc / nm - phi)
slope = (V0(8e14) - V0(6e14)) / 2e14
assert abs(slope * e - h) < 1e-36 and abs(f0 / 1e14 - 5.08) < 0.01 and abs(k(400) - 1.0) < 0.01 and k(600) == 0
facts = dict(slope="%.2f" % (slope * 1e15), f0="%.2f" % (f0 / 1e14), l0="%.0f" % (hc / phi), k4="%.2f" % k(400), k5="%.2f" % k(500))
f = Fig(300, 244)
f.text(150, 14, "V0 = (h / e) f - phi / e", size=10.5, color=NAVY, bold=True)
X = lambda fr: 40 + (fr - 3e14) / 1e14 * 48; Y = lambda v: 110 - v * 42
f.line(X(3e14), Y(0), 285, Y(0), color=SLATE, sw=1.4); f.line(X(3e14), Y(-1), X(3e14), 34, color=SOFT, sw=1.2)
f.line(X(3e14), Y(V0(3e14)), X(8e14), Y(V0(8e14)), color=NAVY, sw=2.6)
f.line(X(3e14), Y(V0(3e14)), X(f0), Y(0), color=SOFT, sw=0.1)
f.line(X(f0), Y(0), X(f0), Y(V0(3e14)) , color=AMBER, sw=1.2, dash=True)
f.circle(X(f0), Y(0), 4, fill=AMBER, stroke=AMBER)
f.text(X(f0) + 6, Y(0) + 15, "f0 = %.2f" % (f0 / 1e14), size=10.5, color=AMBER, bold=True, anchor="start")
f.text(X(8e14) - 4, Y(V0(8e14)) - 10, "%.2f V" % V0(8e14), size=10.5, color=NAVY, bold=True, anchor="end")
for q in (3, 4, 5, 6, 7, 8): f.text(X(q * 1e14), Y(0) - 7 if q > 5 else Y(0) - 7, "%d" % q, size=10.5, color=SLATE)
f.text(150, 164, "f in units of 10^14 Hz; V0 in volts", size=10.5, color=SLATE)
f.text(150, 184, "slope h/e = %.2f x 10^-15 V s" % (slope * 1e15), size=10.5, color=NAVY, bold=True)
f.text(150, 202, "threshold %.2f x 10^14 Hz = %.0f nm" % (f0 / 1e14, hc / phi), size=10.5, color=NAVY, bold=True)
f.text(150, 220, "400 nm: %.2f eV; 500 nm: %.2f eV; 600 nm: 0" % (k(400), k(500)), size=10.5, color=NAVY, bold=True)
```

## Formula and fact sheet

| Quantity | Formula or value |
|---|---|
| Charge and mass of electron | $e=1.6\times10^{-19}$ C, $m=9.11\times10^{-31}$ kg, $e/m=1.76\times10^{11}$ C kg⁻¹ |
| Speed after acceleration | $v=\sqrt{2eV/m}$, $v\propto\sqrt{V}$ |
| Transverse electric field | $y=\frac{1}{2}at^2=\frac{eEx^2}{2mv^2}$; $y_1=\frac{eEL^2}{2mv^2}$; $\tan\theta=\frac{eEL}{mv^2}$ |
| Oscilloscope deflection | $y_1=\frac{V_dL^2}{4dV_a}$ — independent of $e/m$ |
| Magnetic force | $F=evB\sin\theta$, perpendicular to $\vec v$, does no work |
| Radius in a magnetic field | $r=\frac{mv}{eB}=\frac{p}{eB}=\frac{\sqrt{2mK}}{eB}$ |
| Period in a magnetic field | $T=\frac{2\pi m}{eB}$, independent of speed |
| Thomson | undeflected: $eE=evB$, $v=E/B$; then $e/m=\frac{E}{B^2r}$ |
| Millikan | stationary drop: $qE=mg$, $q=\frac{mgd}{V}$; $q=ne$ |
| Planck's constant | $h=6.63\times10^{-34}$ J s; $hc=1.99\times10^{-25}$ J m $\approx1240$ eV nm |
| Photon energy | $E=hf=\frac{hc}{\lambda}$; $E(\text{eV})=\frac{1240}{\lambda(\text{nm})}$ |
| Photon momentum | $p=\frac{h}{\lambda}=\frac{E}{c}$; rest mass zero |
| Einstein's equation | $hf=\phi+K_{max}$; $K_{max}=eV_0$ |
| Threshold | $f_0=\frac{\phi}{h}$, $\lambda_0=\frac{hc}{\phi}=\frac{1240}{\phi(\text{eV})}$ nm |
| $V_0$–$f$ line | $V_0=\frac{h}{e}f-\frac{\phi}{e}$; slope $h/e=4.14\times10^{-15}$ V s; intercept $-\phi/e$ |
| Work functions | Cs 2.14, Na 2.28, Zn 4.3, Cu 4.7 eV (approximate) |
| Intensity against current | saturation current $\propto$ intensity; $V_0$ independent of intensity |
| Wave-theory failures | no threshold, energy should grow with intensity, and a measurable time lag should exist |

## Chapter summary

- An electron in a field **along** its velocity is accelerated: $eV=\frac{1}{2}mv^2$,
  so $v\propto\sqrt{V}$.
- In a **transverse** electric field the path is a parabola,
  $y=eEx^2/(2mv^2)$; the oscilloscope deflection $V_dL^2/(4dV_a)$ does not contain
  $e/m$, and it falls when the accelerating voltage rises.
- In a magnetic field the path is a circle of radius $r=mv/eB$, traced at constant
  speed; the period $2\pi m/eB$ is the same for every speed. A velocity component
  along $\vec B$ turns the circle into a helix.
- Thomson used crossed fields: balance gives $v=E/B$, and the radius in the magnetic
  field alone gives $e/m=E/(B^2r)=1.76\times10^{11}$ C kg⁻¹. He measured a **ratio**,
  and its constancy proved electrons are in all matter.
- Millikan held a charged drop **stationary**, so the drag vanished and $qE=mg$. Every
  charge was a whole multiple of $e=1.60\times10^{-19}$ C: charge is quantised.
- A photon has energy $hf=hc/\lambda$ and momentum $h/\lambda$, zero rest mass and no
  charge. $1240/\lambda(\text{nm})$ gives the energy in eV.
- The photoelectric laws: a threshold frequency; $K_{max}$ set by frequency and metal
  only; current proportional to intensity; emission instantaneous. The wave theory
  fails the first, second and fourth.
- Einstein: $hf=\phi+K_{max}$. Hence $f_0=\phi/h$, $\lambda_0=hc/\phi$, and
  $eV_0=hf-\phi$.
- The $V_0$–$f$ graph is a straight line of slope $h/e$ and intercept $-\phi/e$;
  different metals give parallel lines.
- Intensity changes the **number** of photons and so the saturation current; it never
  changes the energy per photon, so it never changes $V_0$.

## Practice questions

**Set A — Recall (28 questions)**

1. Cathode rays are deflected towards the positive plate of an electric field, which shows that they are
   (a) uncharged (b) positively charged (c) negatively charged (d) electromagnetic waves
2. An electron moving parallel to a uniform electric field is
   (a) deflected sideways (b) accelerated along the field (c) made to move in a circle (d) unaffected by the field
3. An electron moving perpendicular to a uniform magnetic field follows a path that is a
   (a) parabola (b) straight line (c) helix (d) circle
4. If the speed of an electron moving perpendicular to a magnetic field is doubled, the radius of its path becomes
   (a) half (b) the same (c) twice (d) four times
5. The time period of an electron moving in a uniform magnetic field is independent of its
   (a) speed (b) mass (c) charge (d) magnetic field
6. In Thomson's experiment the electron beam is undeflected when the electric and magnetic forces balance. The speed of the electrons is then
   (a) $E/B$ (b) $B/E$ (c) $EB$ (d) $E/B^2$
7. The specific charge $e/m$ of cathode rays measured by Thomson is about
   (a) $1.76\times10^{8}$ C kg⁻¹ (b) $9.1\times10^{-31}$ C kg⁻¹ (c) $1.6\times10^{-19}$ C kg⁻¹ (d) $1.76\times10^{11}$ C kg⁻¹
8. Millikan's oil-drop experiment was designed to measure the
   (a) charge-to-mass ratio of the electron (b) charge of the electron (c) mass of the electron (d) speed of light
9. In Millikan's experiment the drop is held stationary so that
   (a) the viscous drag is zero and $qE=mg$ (b) the drop evaporates slowly (c) the buoyancy becomes zero (d) the drop becomes uncharged
10. The charge on an oil drop in Millikan's experiment is always
   (a) exactly $e$ (b) any continuous value (c) an integral multiple of $e$ (d) negative
11. The work function of a metal is
   (a) the maximum kinetic energy of a photoelectron (b) the energy of an incident photon (c) the energy needed to ionise a free atom (d) the minimum energy needed to remove an electron from the surface
12. The energy of a photon of frequency $f$ is
   (a) $hf$ (b) $h/f$ (c) $f/h$ (d) $hf^2$
13. The momentum of a photon of wavelength $\lambda$ is
   (a) $h\lambda$ (b) $h/\lambda$ (c) $hf$ (d) $hc/\lambda$
14. The rest mass of a photon is
   (a) $9.1\times10^{-31}$ kg (b) $h/c^2$ (c) zero (d) infinite
15. Photoelectric emission from a given metal takes place only when the incident light has
   (a) large intensity (b) long duration (c) large wavelength (d) frequency at least equal to the threshold frequency
16. The stopping potential in a photoelectric experiment measures the
   (a) maximum kinetic energy of the photoelectrons (b) work function of the metal (c) threshold frequency (d) saturation current
17. The slope of the graph of stopping potential against frequency is
   (a) $h$ (b) $h/e$ (c) $e/h$ (d) $\phi/e$
18. The intercept made by the $V_0$–$f$ line on the $V_0$ axis is
   (a) $\phi/e$ (b) $f_0$ (c) $h/e$ (d) $-\phi/e$
19. For light of frequency above threshold, the saturation photocurrent depends on the
   (a) frequency (b) work function (c) intensity (d) stopping potential
20. The threshold wavelength for a metal of work function $\phi$ is
   (a) $hc/\phi$ (b) $\phi/hc$ (c) $h/\phi$ (d) $c/f$
21. When the intensity of light is increased at a fixed frequency above threshold, the quantity that does NOT change is the
   (a) number of photons per second (b) saturation current (c) number of photoelectrons per second (d) maximum kinetic energy of the photoelectrons
22. Photoelectric emission starts almost instantaneously because
   (a) light travels very fast (b) the energy of a photon is absorbed as a whole (c) electrons are free inside the metal (d) the metal is hot
23. Thermionic emission is the emission of electrons from a metal by
   (a) heating it (b) shining light on it (c) applying a magnetic field (d) cooling it
24. The deflection of the beam in a cathode-ray oscilloscope is directly proportional to the
   (a) deflecting voltage (b) square of the deflecting voltage (c) plate separation (d) accelerating voltage
25. An electron at rest in a uniform electric field begins to move
   (a) along the field (b) perpendicular to the field (c) in a circle (d) opposite to the field
26. The number of photons emitted per second by a source of power $P$ and frequency $f$ is
   (a) $P/hf$ (b) $Phf$ (c) $P/f$ (d) $hf/P$
27. The photoelectric current becomes zero when the applied potential equals
   (a) $+V_0$ (b) zero (c) $-V_0$ (d) the threshold potential
28. Which of the following is NOT a property of photons?
   (a) they travel at the speed of light in vacuum (b) they carry momentum (c) they are deflected by a magnetic field (d) their energy is $hf$

::: note Answers and explanations — Set A
**1.** (c) — cathode rays bend towards the positive plate, so they carry negative charge. That is the observation Thomson built on.
**2.** (b) — the force $-e\vec E$ is along the field line for an electron, so the electron accelerates along the field (opposite to $\vec E$); there is no sideways force.
**3.** (d) — the magnetic force is always perpendicular to $\vec v$, so it acts as a centripetal force and the path is a circle. A helix needs a velocity component along $\vec B$.
**4.** (c) — $r=mv/eB$, so $r\propto v$; twice the speed gives twice the radius, in the same time period.
**5.** (a) — $T=2\pi m/eB$ contains no $v$: fast electrons circle in bigger circles but take the same time.
**6.** (a) — balance means $eE=evB$, so $v=E/B$. Option (b) is the reciprocal, which has the wrong units.
**7.** (d) — $1.76\times10^{11}$ C kg⁻¹, about 1836 times the value for a hydrogen ion. (b) is the electron's mass, not its specific charge.
**8.** (b) — Millikan measured $e$; $e/m$ was Thomson's measurement.
**9.** (a) — at rest the drop has no viscous drag, so the only forces are $qE$ up and $mg$ down; they balance.
**10.** (c) — every drop carried a whole number of elementary charges; that is the quantisation result.
**11.** (d) — the work function is a minimum escape energy from the surface, a few eV for metals.
**12.** (a) — Planck's relation $E=hf$; $h/f$ would have units of J s².
**13.** (b) — $p=h/\lambda$, the de Broglie relation applied to a photon; $hc/\lambda$ is the energy.
**14.** (c) — a photon has no rest mass, yet it carries momentum $h/\lambda$ and energy $hf$.
**15.** (d) — a single photon must supply at least $\phi$, so $hf\ge\phi$; intensity cannot help.
**16.** (a) — $eV_0=K_{max}$, so the stopping potential is a direct measure of the fastest electrons' energy.
**17.** (b) — $V_0=(h/e)f-\phi/e$, so the slope is $h/e=4.14\times10^{-15}$ V s.
**18.** (d) — putting $f=0$ gives $V_0=-\phi/e$; the intercept is negative because energy must be supplied.
**19.** (c) — current counts electrons, and the number of electrons follows the number of photons, i.e. the intensity.
**20.** (a) — setting $hc/\lambda_0=\phi$ gives $\lambda_0=hc/\phi$.
**21.** (d) — $K_{max}=hf-\phi$ depends only on frequency and metal; the other three all grow with intensity.
**22.** (b) — absorption is a single photon-electron event, so no build-up time is needed; that is what the wave picture cannot explain.
**23.** (a) — heating gives the fastest electrons enough energy to escape the surface; light gives photoelectric emission instead.
**24.** (a) — $y_1=V_dL^2/(4dV_a)$ is linear in $V_d$ and in $1/V_a$, which is why the tube can be calibrated.
**25.** (d) — the force on a negative charge is opposite to $\vec E$, so a stationary electron accelerates against the field.
**26.** (a) — each photon carries $hf$, so $N=P/hf$.
**27.** (c) — the retarding potential must be $-V_0$; at $+V_0$ the electrons are accelerated, not stopped.
**28.** (c) — a photon is uncharged, so the Lorentz force on it is zero; the other three statements are true.
:::

**Set B — Understanding (17 questions)**

1. An electron enters a uniform electric field at right angles to it. Its path inside the field is a parabola because
   (a) its speed stays constant (b) the force is constant and perpendicular to its initial velocity (c) the force increases with distance (d) the field does work at a constant rate
2. An electron and a proton enter the same magnetic field with the same speed, perpendicular to the field. The ratio of the radii of their paths, $r_e:r_p$, is
   (a) $1:1$ (b) $1836:1$ (c) $1:1836$ (d) $1:43$
3. The magnetic force on a moving electron can never change its
   (a) direction of motion (b) momentum (c) kinetic energy (d) velocity
4. In Thomson's tube, the electric and magnetic deflections are arranged to be opposite. This arrangement is used because it
   (a) allows the speed to be found from the balanced fields (b) doubles the deflection (c) measures the charge directly (d) removes the need for a vacuum
5. The value of $e/m$ for cathode rays is the same whatever gas is in the tube and whatever metal is the cathode. This shows that
   (a) all gases contain hydrogen (b) the particles are photons (c) the tube is always at the same pressure (d) the particles are a common constituent of all matter
6. X-rays are passed through the chamber in Millikan's experiment in order to
   (a) make the oil glow (b) ionise the air so that drops become charged (c) heat the oil (d) increase the viscosity of the air
7. In Millikan's experiment the terminal velocity of a drop is measured with the field off in order to find the
   (a) charge on the drop (b) viscosity of the oil (c) electric field (d) radius and hence mass of the drop
8. The intensity of light falling on a photocell is doubled while its frequency is kept the same. Then
   (a) the stopping potential doubles (b) the saturation current doubles and the stopping potential is unchanged (c) both double (d) neither changes
9. For a metal of work function 2.0 eV, light of wavelength 700 nm produces no photoelectrons because
   (a) the intensity is too low (b) the photons are too few (c) each photon has less energy than the work function (d) the metal is not clean
10. Two metals have work functions 2.0 eV and 3.0 eV. Their $V_0$–$f$ graphs are
   (a) the same line (b) curves (c) lines of different slopes (d) parallel lines with different intercepts
11. A photon of energy 3 eV strikes a metal whose work function is 4 eV. The result is
   (a) an electron leaves with 1 eV (b) an electron leaves with 7 eV (c) no electron leaves, and the photon is not absorbed by a bound electron (d) two electrons leave
12. The stopping potential does not depend on the intensity of the light because
   (a) intensity does not change the number of photons (b) the current is always saturated (c) the work function changes with intensity (d) intensity changes only the number of photons, not the energy of each
13. Light of frequency just above the threshold falls on a metal. If the frequency is now doubled, the maximum kinetic energy of the photoelectrons
   (a) doubles (b) is unchanged (c) more than doubles (d) becomes four times
14. In a cathode-ray tube, increasing the accelerating voltage while the deflecting voltage is fixed makes the spot deflection
   (a) larger (b) zero (c) unchanged (d) smaller
15. A beam of electrons and a beam of protons are accelerated through the same potential difference and then enter the same magnetic field. The radius of the proton path is larger because
   (a) the proton has more charge (b) the proton has larger momentum for the same energy (c) the proton moves faster (d) the field is weaker on the proton
16. The wave theory of light cannot explain the threshold frequency because, in that theory,
   (a) energy is carried in packets (b) electrons are waves (c) light has no momentum (d) energy arrives continuously, so any frequency should work
17. In the graph of stopping potential against frequency, the intercept on the frequency axis gives
   (a) the work function in joules (b) Planck's constant (c) the threshold frequency (d) the charge on the electron

::: note Answers and explanations — Set B
**1.** (b) — a constant force at right angles to the velocity is exactly the projectile condition: uniform motion along the field-free direction and uniform acceleration across it give $y\propto x^2$.
**2.** (c) — $r=mv/eB$ at the same speed gives $r\propto m$, so the electron's radius is $1/1836$ of the proton's. (d) is the ratio of the square roots, which would apply at the same energy with equal charges — not here.
**3.** (c) — the force is perpendicular to $\vec v$, so it does no work; speed and kinetic energy stay constant while the direction changes.
**4.** (a) — with both fields on and no deflection, $eE=evB$ gives $v=E/B$; the magnetic field alone then gives $e/m$. Neither field alone can give both.
**5.** (d) — the same $e/m$ from every gas and every cathode means the particles are not fragments of a particular element; they are present in all matter.
**6.** (b) — X-rays ionise the air molecules, and the ions attach to the oil drops and charge them, so the charge can be varied at will.
**7.** (d) — at terminal velocity Stokes' law balances the weight, which gives the radius, and the density gives the mass — needed before $q=mg/E$ can be used.
**8.** (b) — doubling the intensity doubles the photon arrival rate, hence the saturation current; the energy of each photon, and so $V_0$, is set by the frequency alone.
**9.** (c) — $1240/700=1.8$ eV, less than the 2.0 eV work function, so no single photon can free an electron. More of them cannot help.
**10.** (d) — the slope is $h/e$ for every metal, so the lines are parallel; the intercept $-\phi/e$ differs.
**11.** (c) — a photon is absorbed whole and cannot pay the 4 eV work function; a bound electron does not absorb part of a photon.
**12.** (d) — $K_{max}=hf-\phi$ contains no intensity term; intensity only multiplies the number of photons.
**13.** (c) — $K=hf-\phi$; doubling $f$ gives $2hf-\phi=2(hf-\phi)+\phi$, which is more than twice the original.
**14.** (d) — $y_1=V_dL^2/(4dV_a)$, so a larger $V_a$ means a smaller deflection; the beam is stiffer.
**15.** (b) — at the same energy $p=\sqrt{2mK}$ is larger for the proton (1836 times the mass, so about 43 times the momentum), and $r=p/eB$.
**16.** (d) — continuous absorption means the required energy can always be accumulated, so a threshold should not exist; the observed threshold needs the photon picture.
**17.** (c) — $V_0=0$ at $f=f_0=\phi/h$; the work function is the intercept on the $V_0$ axis divided by $e$.
:::

**Set C — Application (11 questions)**

1. The energy of a photon of wavelength 500 nm is about
   (a) 1.2 eV (b) 3.1 eV (c) 4.1 eV (d) 2.5 eV
2. The momentum of a photon of wavelength 500 nm is about
   (a) $6.6\times10^{-34}$ kg m s⁻¹ (b) $1.3\times10^{-27}$ kg m s⁻¹ (c) $2.5\times10^{-27}$ kg m s⁻¹ (d) $1.5\times10^{-36}$ kg m s⁻¹
3. The threshold wavelength for a metal of work function 2.5 eV is about
   (a) 248 nm (b) 310 nm (c) 496 nm (d) 620 nm
4. Light of wavelength 300 nm falls on a metal of work function 2.0 eV. The maximum kinetic energy of the photoelectrons is about
   (a) 1.1 eV (b) 4.1 eV (c) 6.2 eV (d) 2.1 eV
5. Light of wavelength 400 nm falls on a metal of work function 2.5 eV. The stopping potential is
   (a) 0.6 V (b) 0.3 V (c) 2.5 V (d) 3.1 V
6. A source emits 100 W of light of wavelength 589 nm. The number of photons emitted per second is about
   (a) $3.0\times10^{20}$ (b) $3.0\times10^{18}$ (c) $5.9\times10^{20}$ (d) $1.7\times10^{26}$
7. An electron is accelerated from rest through 1000 V. Its speed is about
   (a) $1.9\times10^{6}$ m s⁻¹ (b) $3.5\times10^{7}$ m s⁻¹ (c) $6.0\times10^{7}$ m s⁻¹ (d) $1.9\times10^{7}$ m s⁻¹
8. An electron moves at $1.0\times10^{7}$ m s⁻¹ perpendicular to a field of $1.0\times10^{-2}$ T. The radius of its path is about
   (a) 0.57 mm (b) 57 mm (c) 5.7 mm (d) 570 mm
9. In a Thomson tube the beam is undeflected with $E=3.4\times10^{4}$ V m⁻¹ and $B=2.0\times10^{-3}$ T. With the electric field off the beam circles with radius 4.8 cm. The value of $e/m$ is about
   (a) $1.8\times10^{9}$ C kg⁻¹ (b) $1.8\times10^{11}$ C kg⁻¹ (c) $1.8\times10^{10}$ C kg⁻¹ (d) $3.5\times10^{11}$ C kg⁻¹
10. An oil drop of mass $3.2\times10^{-15}$ kg is held stationary between plates 1.0 cm apart at 200 V. The charge on the drop is ($g=10$ m s⁻²)
   (a) $1.6\times10^{-19}$ C (b) $3.2\times10^{-18}$ C (c) $6.4\times10^{-19}$ C (d) $1.6\times10^{-18}$ C
11. In a cathode-ray tube the plates are 2.0 cm long and 1.0 cm apart, and the beam is accelerated through 1000 V. With 100 V across the plates the deflection at the exit is
   (a) 0.5 mm (b) 2.0 mm (c) 1.0 mm (d) 4.0 mm

::: note Answers and explanations — Set C
**1.** (d) — $E=1240/500=2.48$ eV $\approx2.5$ eV. (b) is the value for 400 nm.
**2.** (b) — $p=h/\lambda=6.63\times10^{-34}/5.0\times10^{-7}=1.3\times10^{-27}$ kg m s⁻¹. (a) is $h$ itself, and (d) divides by $\lambda$ twice.
**3.** (c) — $\lambda_0=1240/2.5=496$ nm. 620 nm is the threshold for a 2.0 eV metal.
**4.** (d) — $1240/300=4.13$ eV, so $K_{max}=4.13-2.0=2.1$ eV. (b) forgets to subtract the work function.
**5.** (a) — $1240/400=3.1$ eV; $K_{max}=3.1-2.5=0.6$ eV, so $V_0=0.6$ V. (d) is the photon energy, not the stopping potential.
**6.** (a) — $E=3.38\times10^{-19}$ J, so $N=100/3.38\times10^{-19}=3.0\times10^{20}$ s⁻¹.
**7.** (d) — $v=\sqrt{2eV/m}=\sqrt{2(1.6\times10^{-19})(1000)/9.11\times10^{-31}}=1.87\times10^{7}$ m s⁻¹.
**8.** (c) — $r=mv/eB=(9.11\times10^{-31})(10^{7})/(1.6\times10^{-19})(10^{-2})=5.7\times10^{-3}$ m $=5.7$ mm.
**9.** (b) — $v=E/B=1.7\times10^{7}$ m s⁻¹, then $e/m=v/(Br)=1.7\times10^{7}/(2.0\times10^{-3}\times0.048)=1.8\times10^{11}$ C kg⁻¹, the electron value.
**10.** (d) — $E=V/d=2.0\times10^{4}$ V m⁻¹; $q=mg/E=(3.2\times10^{-15})(10)/(2.0\times10^{4})=1.6\times10^{-18}$ C, which is 10 electrons.
**11.** (c) — $y_1=V_dL^2/(4dV_a)=100(0.020)^2/(4\times0.010\times1000)=1.0\times10^{-3}$ m $=1.0$ mm.
:::
