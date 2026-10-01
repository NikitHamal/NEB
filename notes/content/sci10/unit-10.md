---
subject: Science and Technology
grade: 10
unit: 10
title: Wave
hours: 0
area: Science and Technology
---

We hear a temple bell, see a rainbow, watch a cricket match on television and send a message over a mobile phone. All of these depend on **waves**. A wave carries energy from one place to another without carrying matter along with it. In this unit you will study wave motion in general, then two very important kinds of wave: sound and light. You will learn how light is reflected by mirrors and refracted by lenses, and how the eye, the camera, the microscope and the telescope use these ideas.

::: key What SEE asks from this unit
Definitions of wave terms and $v = f\lambda$; echo numericals; laws of reflection and refraction; the mirror formula and lens formula with magnification; critical angle and total internal reflection; power of a lens; defects of the eye and their correction; and ray diagrams. Learn to draw the ray diagrams neatly with a ruler.
:::

## 10.1 Wave motion

When you drop a stone in a still pond, circles spread out from the spot. A leaf floating on the water just moves up and down. The disturbance travels outward, but the water (and the leaf) do not travel with it. This is a **wave**.

::: definition Wave
A wave is a disturbance that travels through a medium (or space) and carries energy from one place to another without the transfer of matter.
:::

### Types of waves

| Basis | Type | Meaning | Example |
|---|---|---|---|
| Medium needed | **Mechanical** waves | Need a material medium | Sound, water waves, waves on a string |
| | **Electromagnetic** waves | Need no medium; can travel in vacuum | Light, radio waves, X-rays |
| Direction of vibration | **Transverse** waves | Particles vibrate at right angles to the direction of the wave | Waves on a rope, water ripples, light |
| | **Longitudinal** waves | Particles vibrate along the direction of the wave | Sound in air, waves in a spring |

A transverse wave has **crests** (highest points) and **troughs** (lowest points). A longitudinal wave has **compressions** (particles crowded together, high pressure) and **rarefactions** (particles spread apart, low pressure).

```figure caption="Top: a transverse wave with its crest, trough, amplitude and wavelength. Bottom: a longitudinal wave, where the particles bunch up in compressions (C) and spread out in rarefactions (R)."
import numpy as np, matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(2, 1, figsize=(4.8, 3.6))
x = np.linspace(0, 4*np.pi, 300)
a1.plot(x, np.sin(x), color=ACCENT, lw=2)
a1.axhline(0, color=MUTED, lw=0.8)
a1.annotate('', xy=(np.pi/2, 0), xytext=(np.pi/2, 1), arrowprops=dict(arrowstyle='<->', color=INK))
a1.text(2.65, 0.85, 'amplitude', fontsize=8, color=INK)
a1.annotate('', xy=(2*np.pi + np.pi/2, -1.55), xytext=(np.pi/2, -1.55), arrowprops=dict(arrowstyle='<->', color=INK))
a1.text(np.pi + 0.5, -1.95, 'wavelength', fontsize=8, color=INK)
a1.text(np.pi/2-0.3, 1.2, 'crest', fontsize=8, color=INK)
a1.text(1.5*np.pi-0.3, -1.3, 'trough', fontsize=8, color=INK)
a1.set_ylim(-2.3, 1.7); a1.axis('off')
n = 40
pos = np.arange(n)*1.0
disp = 0.45*np.sin(2*np.pi*pos/10.0)
xs = pos + disp
for i in range(n):
    a2.plot([xs[i], xs[i]], [0, 1], color=ACCENT, lw=1.3)
for k in (5, 15, 25, 35):
    a2.text(xs[k]-0.5, 1.25, 'C', fontsize=9, color=INK)
for k in (0, 10, 20, 30):
    a2.text(xs[k]-0.5, 1.25, 'R', fontsize=9, color=INK)
a2.set_ylim(-0.2, 1.7); a2.axis('off')
fig.tight_layout()
```

### Wave terms

| Term | Meaning | Unit |
|---|---|---|
| Amplitude ($a$) | Maximum displacement of a particle from its mean position | m |
| Wavelength ($\lambda$) | Distance between two successive crests (or troughs, or compressions) | m |
| Frequency ($f$) | Number of complete waves passing a point (or vibrations per second) | hertz (Hz) |
| Time period ($T$) | Time for one complete wave, $T = 1/f$ | s |
| Speed ($v$) | Distance the wave travels per second | m s⁻¹ |

In one time period $T$, the wave moves forward by one wavelength $\lambda$. Therefore speed $= \lambda/T$. Since $1/T = f$,

$$ v = f\lambda $$

This is the **wave equation**. It applies to every kind of wave. The speed of a wave depends on the medium; the frequency depends on the source.

::: example Using the wave equation
**Problem.** A wave on a rope has frequency 50 Hz and wavelength 4 m. Find (a) its speed and (b) its time period.

**Solution.** (a) $v = f\lambda = 50 \times 4 = 200$ m s⁻¹.

(b) $T = \dfrac{1}{f} = \dfrac{1}{50} = 0.02$ s.
:::

## 10.2 Sound

### Production and transmission

Sound is produced by **vibrating** bodies: a plucked guitar string, a struck drum skin, the vocal cords in your throat. Sound is a mechanical, longitudinal wave. It needs a material medium (solid, liquid or gas) and **cannot travel through a vacuum**. This can be shown with an electric bell in a bell jar: as the air is pumped out, the sound fades away though the hammer is seen striking.

### Speed of sound

| Medium | Speed (m s⁻¹) |
|---|---|
| Air at 0 °C | 332 |
| Air at 20 °C | 343 (often taken as 340) |
| Water | about 1500 |
| Iron / steel | about 5000 |

Sound travels fastest in solids and slowest in gases. Its speed in air increases as the temperature rises, and it is not affected by changes in loudness or pitch. Light travels at $3\times10^{8}$ m s⁻¹, far faster than sound, so we see lightning before we hear thunder.

### Characteristics of sound

| Characteristic | Depends on | Meaning |
|---|---|---|
| **Loudness** | Amplitude (and intensity) | How strong the sound seems; measured in decibel (dB) |
| **Pitch** | Frequency | How high or low (shrill or flat) the note is; women's voices have higher pitch than men's |
| **Quality (timbre)** | Waveform (the overtones present) | Lets us tell a flute from a sitar when both play the same note at the same loudness |

The human ear can hear frequencies from **20 Hz to 20,000 Hz** (the audible range). Below 20 Hz is **infrasound** (elephants and earthquakes), and above 20,000 Hz is **ultrasound** (bats and dolphins use it).

Uses of ultrasound: SONAR (finding the depth of the sea or a submarine), ultrasonography scans of the body (the unborn baby), cleaning delicate machinery, and detecting cracks in metal.

### Reflection of sound and echo

Sound is reflected from hard surfaces like cliffs, walls and mountains, just like a ball bouncing off a wall. The reflected sound heard after the original sound is an **echo**.

The human ear keeps a sound in memory for about 0.1 s. To hear a clear echo, the reflected sound must arrive at least 0.1 s after the original. So the minimum distance to the reflecting wall is

$$ d = \frac{v \times t}{2} = \frac{340 \times 0.1}{2} = 17\ \text{m} $$

(We divide by 2 because the sound goes to the wall and comes back.)

If the reflection returns within 0.1 s, it blends with the original sound and we get **reverberation**, a prolonged sound. Concert halls reduce it with curtains and soft panels.

::: example Echo
**Problem.** A man standing in front of a cliff claps his hands and hears the echo after 2 s. If the speed of sound is 340 m s⁻¹, how far is the cliff?

**Solution.** Total distance travelled by the sound $= v t = 340 \times 2 = 680$ m.

Distance of the cliff $= \dfrac{680}{2} = 340$ m.
:::

::: example Depth of the sea
**Problem.** A ship sends an ultrasonic pulse to the sea bed and receives the echo after 0.8 s. If the speed of sound in sea water is 1500 m s⁻¹, find the depth of the sea.

**Solution.** $d = \dfrac{vt}{2} = \dfrac{1500 \times 0.8}{2} = 600$ m.
:::

Uses of echo: bats and dolphins find their way and food by echo (echolocation); SONAR; and the medical technique of ultrasound scanning.

## 10.3 Reflection and refraction of light

Light is an electromagnetic transverse wave. It travels in straight lines in a uniform medium (rectilinear propagation) at $3\times10^{8}$ m s⁻¹ in vacuum.

### Reflection of light

When light falls on a smooth surface and bounces back into the same medium, it is **reflected**.

::: definition Laws of reflection
1. The incident ray, the reflected ray and the normal at the point of incidence all lie in the same plane.
2. The angle of incidence is equal to the angle of reflection: $\angle i = \angle r$.
:::

Both angles are measured from the **normal** (the line perpendicular to the surface), not from the surface.

**Image in a plane mirror:** virtual, erect, the same size as the object, as far behind the mirror as the object is in front, and laterally inverted (left and right are interchanged).

### Spherical mirrors

A spherical mirror is part of a hollow sphere. A **concave** mirror reflects from the inside (it converges light); a **convex** mirror reflects from the outside (it diverges light).

| Term | Meaning |
|---|---|
| Pole (P) | Centre of the mirror surface |
| Centre of curvature (C) | Centre of the sphere of which the mirror is a part |
| Radius of curvature (R) | Distance PC |
| Principal axis | Line through P and C |
| Principal focus (F) | Point where rays parallel to the axis meet (concave) or appear to come from (convex) after reflection |
| Focal length (f) | Distance PF, and $f = R/2$ |

Rules for ray diagrams (concave mirror):

1. A ray parallel to the principal axis reflects through the focus F.
2. A ray passing through F reflects parallel to the principal axis.
3. A ray through C returns along the same path.

```figure caption="Concave mirror: object beyond C. The image forms between F and C and is real, inverted and diminished. (P is the pole, F the focus and C the centre of curvature.)"
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 3.0))
ax.set_xlim(-38, 6); ax.set_ylim(-6, 10); ax.axis('off')
ax.plot([-38, 6], [0, 0], color=MUTED, lw=1)
ax.plot([0, 0], [-8, 8], color=INK, lw=2.5)
for yy in np.arange(-8, 8, 1.6):
    ax.plot([0, 1.2], [yy, yy-0.9], color=INK, lw=0.8)
ax.annotate('', xy=(-30, 6), xytext=(-30, 0), arrowprops=dict(arrowstyle='-|>', color=INK, lw=2))
ax.annotate('', xy=(-15, -3), xytext=(-15, 0), arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=2))
ax.plot([-30, 0], [6, 6], color=ACCENT, lw=1.3)
ax.plot([0, -20], [6, -6], color=ACCENT, lw=1.3)
ax.plot([-30, 0], [6, -3], color='#1B6E3A', lw=1.3)
ax.plot([0, -30], [-3, -3], color='#1B6E3A', lw=1.3)
for xx, lab in [(0, 'P'), (-10, 'F'), (-20, 'C')]:
    ax.plot([xx], [0], 'o', color=INK, ms=3)
    ax.text(xx-(1.6 if lab=='P' else 0), 0.8 if lab!='P' else -2.2, lab, ha='center', fontsize=9, color=INK)
ax.text(-30, 6.8, 'object', ha='center', fontsize=8.5, color=INK)
ax.text(-15, -4.8, 'image', ha='center', fontsize=8.5, color='#A8271F')
```

### Images formed by a concave mirror

| Object position | Image position | Nature and size |
|---|---|---|
| At infinity | At F | Real, inverted, point-sized |
| Beyond C | Between F and C | Real, inverted, diminished |
| At C | At C | Real, inverted, same size |
| Between C and F | Beyond C | Real, inverted, magnified |
| At F | At infinity | Real, inverted, highly magnified |
| Between F and P | Behind the mirror | Virtual, erect, magnified |

A **convex mirror** always forms a virtual, erect, diminished image behind the mirror, whatever the position of the object. It gives a wide field of view, so it is used as a rear-view mirror in vehicles and as a security mirror in shops. A concave mirror is used as a shaving mirror (large erect image when the face is close), in a dentist's mirror, a torch or headlight reflector (lamp at F gives a parallel beam), and in solar cookers.

### Mirror formula and magnification

In this book we use the "real is positive" convention: distances of real objects and real images are positive; distances to virtual images and virtual objects are negative. A concave mirror has a positive $f$ and a convex mirror a negative $f$.

$$ \frac{1}{f} = \frac{1}{u} + \frac{1}{v} \qquad f = \frac{R}{2} $$

where $u$ is the object distance and $v$ is the image distance. Linear magnification:

$$ m = \frac{\text{height of image}}{\text{height of object}} = \frac{v}{u} \quad(\text{size only}) $$

::: example Real image in a concave mirror
**Problem.** An object is placed 30 cm in front of a concave mirror of focal length 10 cm. Find the position and magnification of the image.

**Solution.** $u = 30$ cm, $f = 10$ cm.

$\dfrac{1}{v} = \dfrac{1}{f} - \dfrac{1}{u} = \dfrac{1}{10} - \dfrac{1}{30} = \dfrac{3-1}{30} = \dfrac{2}{30}$, so $v = 15$ cm.

$v$ is positive, so the image is real and in front of the mirror. $m = \dfrac{v}{u} = \dfrac{15}{30} = 0.5$: the image is inverted and half the size of the object.
:::

::: example Virtual image in a concave mirror
**Problem.** An object is 5 cm from a concave mirror of focal length 10 cm. Find where the image forms and how large it is.

**Solution.** $\dfrac{1}{v} = \dfrac{1}{10} - \dfrac{1}{5} = \dfrac{1-2}{10} = -\dfrac{1}{10}$, so $v = -10$ cm.

The negative sign means the image is virtual, 10 cm behind the mirror. Magnification (size) $= \dfrac{|v|}{u} = \dfrac{10}{5} = 2$. The image is erect and twice as large (the shaving-mirror case).
:::

### Refraction of light

When light passes from one transparent medium to another, it changes direction at the boundary. This bending is called **refraction**. It happens because the speed of light is different in different media. Light going from a rarer to a denser medium (air to glass) **bends toward the normal**; from denser to rarer, it **bends away from the normal**.

Everyday examples: a pencil in a glass of water looks bent; a pond looks shallower than it is; a coin in a bowl comes into view when water is poured in; stars twinkle.

::: definition Laws of refraction
1. The incident ray, the refracted ray and the normal lie in the same plane.
2. **Snell's law:** the ratio $\dfrac{\sin i}{\sin r}$ is constant for a given pair of media and given colour of light.
:::

$$ \frac{\sin i}{\sin r} = n $$

The constant $n$ is the **refractive index** of the second medium relative to the first. For a medium compared with vacuum (or air):

$$ n = \frac{\text{speed of light in vacuum}}{\text{speed of light in the medium}} = \frac{c}{v} $$

Refractive index has no unit. A higher $n$ means light is slowed more, and bends more.

| Medium | Refractive index |
|---|---|
| Air | 1.0003 |
| Water | 1.33 |
| Glass | 1.5 |
| Diamond | 2.42 |

::: example Refraction at a glass surface
**Problem.** Light enters glass of refractive index 1.5 from air at an angle of incidence of 30°. Find (a) the angle of refraction and (b) the speed of light in glass.

**Solution.** (a) $\sin r = \dfrac{\sin i}{n} = \dfrac{\sin 30°}{1.5} = \dfrac{0.5}{1.5} = 0.333$, so $r \approx 19.5°$. The ray bends toward the normal.

(b) $v = \dfrac{c}{n} = \dfrac{3\times10^{8}}{1.5} = 2\times10^{8}$ m s⁻¹.
:::

### Total internal reflection

When light goes from a denser to a rarer medium, it bends away from the normal. As the angle of incidence increases, the angle of refraction increases until it reaches 90° (the refracted ray skims the surface). The angle of incidence in the denser medium for which the angle of refraction in the rarer medium is 90° is the **critical angle** $C$.

::: definition Total internal reflection
When a ray of light travels from a denser to a rarer medium and the angle of incidence is greater than the critical angle, the ray is completely reflected back into the denser medium. This is total internal reflection.
:::

Conditions: (1) light travels from a denser to a rarer medium, (2) the angle of incidence is greater than the critical angle.

For a medium of refractive index $n$ in air, light going from the medium into air at the critical angle has $r = 90°$. Snell's law (air to medium, with the path reversed) gives $n = \dfrac{\sin 90°}{\sin C}$, so

$$ \sin C = \frac{1}{n} $$

```figure caption="Light going from glass (n = 1.5) to air. In the first diagram the ray is refracted; at the critical angle (about 42 degrees) the refracted ray grazes the surface; at larger angles the ray is totally internally reflected."
import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 3, figsize=(5.2, 2.5))
n = 1.5
C = np.degrees(np.arcsin(1/n))
cases = [(30, 'i < C'), (C, 'i = C'), (60, 'i > C')]
L = 1.0
for ax, (ang, t) in zip(axs, cases):
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.2, 1.2); ax.set_aspect('equal'); ax.axis('off')
    ax.fill_between([-1.3, 1.3], [-1.2, -1.2], [0, 0], color='#D6E6FF')
    ax.plot([-1.3, 1.3], [0, 0], color=INK, lw=1.2)
    ax.plot([0, 0], [-1.1, 1.1], color=MUTED, lw=0.8, ls='--')
    a = np.radians(ang)
    ax.plot([-L*np.sin(a), 0], [-L*np.cos(a), 0], color=ACCENT, lw=1.8)
    sr = n*np.sin(a)
    if sr < 1.0 - 1e-9:
        r = np.arcsin(sr)
        ax.plot([0, L*np.sin(r)], [0, L*np.cos(r)], color='#A8271F', lw=1.8)
    elif abs(sr - 1.0) < 1e-6:
        ax.plot([0, 1.2], [0, 0.0], color='#A8271F', lw=1.8)
    else:
        ax.plot([0, L*np.sin(a)], [0, -L*np.cos(a)], color='#A8271F', lw=1.8)
    ax.set_title(t, fontsize=9, color=INK)
    ax.text(-1.25, -1.1, 'glass', fontsize=8, color=INK)
    ax.text(-1.25, 0.9, 'air', fontsize=8, color=INK)
fig.tight_layout()
```

::: example Critical angle
**Problem.** Find the critical angle for (a) water ($n = 1.33$) and (b) diamond ($n = 2.42$).

**Solution.** (a) $\sin C = \dfrac{1}{1.33} = 0.752$, so $C \approx 48.8°$.

(b) $\sin C = \dfrac{1}{2.42} = 0.413$, so $C \approx 24.4°$.

Diamond has a very small critical angle, so light entering it undergoes total internal reflection many times inside, and the stone sparkles.
:::

Applications of total internal reflection: **optical fibres** (light signals travel long distances by repeated total internal reflection; used for internet, telephone, and the endoscope in medicine), totally reflecting prisms in binoculars and periscopes, the sparkle of diamonds, and **mirage** in the desert (hot air near the ground is rarer than the cooler air above, so light from the sky is totally reflected upward and appears as water).

## 10.4 Lenses

A **lens** is a transparent material (glass or plastic) bounded by two curved surfaces. A **convex (converging) lens** is thicker in the middle; a **concave (diverging) lens** is thinner in the middle.

| Term | Meaning |
|---|---|
| Optical centre (O) | Centre of the lens; a ray through it goes straight |
| Principal axis | Line through O joining the centres of curvature |
| Principal focus (F) | Point where rays parallel to the axis meet (convex) or seem to come from (concave) after refraction. A lens has two foci, one on each side |
| Focal length (f) | Distance OF |

Rules for ray diagrams:

1. A ray parallel to the principal axis passes through the focus (convex) or appears to come from the focus (concave).
2. A ray through the optical centre goes straight, undeviated.
3. A ray through the first focus emerges parallel to the axis.

```figure caption="Convex lens with the object at 20 cm and f = 15 cm. The image is formed 60 cm on the other side: real, inverted and magnified three times."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2, 2.8))
ax.set_xlim(-30, 72); ax.set_ylim(-14, 8); ax.axis('off')
ax.plot([-30, 72], [0, 0], color=MUTED, lw=1)
ax.annotate('', xy=(0, 8), xytext=(0, -8), arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=2))
ax.annotate('', xy=(-20, 4), xytext=(-20, 0), arrowprops=dict(arrowstyle='-|>', color=INK, lw=2))
ax.annotate('', xy=(60, -12), xytext=(60, 0), arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=2))
ax.plot([-20, 0], [4, 4], color=ACCENT, lw=1.3)
ax.plot([0, 60], [4, -12], color=ACCENT, lw=1.3)
ax.plot([-20, 60], [4, -12], color='#1B6E3A', lw=1.3)
for xx, lab in [(-15, 'F'), (15, 'F'), (0, 'O')]:
    ax.plot([xx], [0], 'o', color=INK, ms=3)
    ax.text(xx+(2.0 if lab=='O' else 0), 0.9 if lab!='O' else -2.4, lab, ha='center', fontsize=9, color=INK)
ax.text(-20, 4.9, 'object', ha='center', fontsize=8.5, color=INK)
ax.text(60, -13.6, 'image', ha='center', fontsize=8.5, color='#A8271F')
```

### Images formed by a convex lens

| Object position | Image position | Nature and size |
|---|---|---|
| At infinity | At F | Real, inverted, point-sized |
| Beyond 2F | Between F and 2F | Real, inverted, diminished |
| At 2F | At 2F | Real, inverted, same size |
| Between 2F and F | Beyond 2F | Real, inverted, magnified |
| At F | At infinity | Real, inverted, highly magnified |
| Between F and O | Same side as object | Virtual, erect, magnified (magnifying glass) |

A concave lens always forms a virtual, erect, diminished image on the same side as the object.

### Lens formula, magnification and power

Using the same "real is positive" convention (convex lens $f$ positive; concave lens $f$ negative):

$$ \frac{1}{f} = \frac{1}{u} + \frac{1}{v} \qquad m = \frac{v}{u} $$

The **power** of a lens measures how strongly it bends light:

$$ P = \frac{1}{f\ (\text{in metres})} $$

The unit of power is the **dioptre (D)**. A convex lens has positive power, a concave lens has negative power. For lenses in contact, powers add: $P = P_1 + P_2$.

::: example Convex lens image
**Problem.** An object is placed 20 cm from a convex lens of focal length 15 cm. Find the image distance and magnification.

**Solution.** $\dfrac{1}{v} = \dfrac{1}{15} - \dfrac{1}{20} = \dfrac{4-3}{60} = \dfrac{1}{60}$, so $v = 60$ cm.

The image is real (positive $v$), inverted, and $m = \dfrac{60}{20} = 3$, three times the object size.
:::

::: example Power of lenses
**Problem.** Find the power of (a) a convex lens of focal length 25 cm and (b) a concave lens of focal length 50 cm.

**Solution.** (a) $f = 0.25$ m, $P = \dfrac{1}{0.25} = +4$ D.

(b) $f = -0.5$ m (concave), $P = \dfrac{1}{-0.5} = -2$ D.
:::

## 10.5 Optical instruments

### The human eye

The eye is a natural optical instrument. Light enters through the transparent **cornea**, passes the **pupil** (the opening whose size is controlled by the coloured **iris**), and is focused by the **convex eye lens** onto the **retina** at the back. The retina has light-sensitive cells (rods for dim light, cones for colour) and the **optic nerve** carries the signal to the brain, which sees the image upright. The lens is made thicker or thinner by the **ciliary muscles** to focus on near or far objects. This is called **accommodation**.

Normal vision: the **near point** (least distance of distinct vision) is 25 cm and the **far point** is infinity.

### Defects of vision and their correction

| Defect | Problem | Cause | Correction |
|---|---|---|---|
| **Myopia** (short sight) | Can see near things clearly but not distant ones | Eyeball too long, or lens too curved; image forms in front of the retina | Concave (diverging) lens |
| **Hypermetropia** (long sight) | Can see distant things clearly but not near ones | Eyeball too short, or lens too flat; image forms behind the retina | Convex (converging) lens |
| **Presbyopia** | Difficulty in seeing near objects after the age of 40–45 | Ciliary muscles weaken and the lens loses flexibility | Bifocal lenses (or reading glasses) |
| **Astigmatism** | Blurred or distorted vision in one direction | Cornea not perfectly spherical | Cylindrical lens |
| **Cataract** | Cloudy vision | The eye lens becomes cloudy | Surgery to replace the lens |

::: example Correcting short sight
**Problem.** A short-sighted person cannot see clearly beyond 50 cm. Which lens, and of what power, must be used to see distant objects clearly?

**Solution.** The lens must form a virtual image at the far point (50 cm) of an object at infinity: $u = \infty$, $v = -50$ cm.

$\dfrac{1}{f} = \dfrac{1}{u} + \dfrac{1}{v} = 0 - \dfrac{1}{50}$, so $f = -50$ cm $= -0.5$ m.

Power $P = \dfrac{1}{-0.5} = -2$ D. A concave lens of power $-2$ D is needed.
:::

### Simple microscope (magnifying glass)

A convex lens of short focal length held close to a small object (between F and O) gives a virtual, erect, magnified image. It is used by watchmakers, jewellers and to read small print. Its magnifying power for the image at the near point is $M = 1 + \dfrac{D}{f}$ with $D = 25$ cm.

### Compound microscope

It uses two convex lenses: the **objective** (very short focal length, near the object) forms a real, inverted, magnified image; the **eyepiece** (longer focal length) acts as a magnifying glass on that image and gives a final virtual, inverted, highly magnified image. It is used to see cells, bacteria and tiny parts of insects.

### Astronomical telescope

It also uses two convex lenses, but the **objective** has a **long** focal length and a large aperture to gather light from a distant object. It forms a real image at its focus, which the eyepiece magnifies. The final image is virtual, inverted and magnified. It is used to look at the Moon, planets and stars. Magnification (in normal adjustment) $= \dfrac{f_o}{f_e}$.

### Camera, projector and others

| Instrument | Lens / mirror | Image |
|---|---|---|
| Camera | Convex lens | Real, inverted, diminished image on film or sensor |
| Projector | Convex lens | Real, inverted, magnified image on a screen (slide is placed upside down) |
| Periscope | Plane mirrors (or prisms) | Lets us see over obstacles |
| Binoculars | Lenses and prisms | Magnified, erect view with both eyes |

::: caution Eye lens and camera
Do not confuse the pupil with the retina. The pupil is the hole; the retina is the screen. In a camera, the diaphragm (aperture) is like the iris, and the film or sensor is like the retina.
:::

## Chapter summary

- A wave transfers energy without transferring matter. Transverse: vibration ⟂ wave direction; longitudinal: vibration ∥ wave direction. $v = f\lambda$, $T = 1/f$.
- Sound is a longitudinal mechanical wave; cannot travel in a vacuum; fastest in solids. Audible range 20 Hz–20 kHz. Echo needs at least 17 m: $d = vt/2$.
- Loudness depends on amplitude, pitch on frequency, quality on waveform.
- Reflection: $\angle i = \angle r$. Mirror formula $\dfrac{1}{f} = \dfrac{1}{u} + \dfrac{1}{v}$, $f = R/2$, $m = v/u$.
- Refraction: $\dfrac{\sin i}{\sin r} = n = \dfrac{c}{v}$; total internal reflection when light goes dense → rare with $i > C$, where $\sin C = 1/n$.
- Lens formula $\dfrac{1}{f} = \dfrac{1}{u} + \dfrac{1}{v}$; power $P = 1/f$ (m) in dioptre; convex is positive, concave is negative.
- Myopia is corrected by a concave lens, hypermetropia by a convex lens. Compound microscope and telescope use two convex lenses.

## Practice questions

**Group A — Objective (1 mark each)**

1. Sound waves in air are <span class="marks">[1]</span>
   (a) transverse (b) longitudinal (c) electromagnetic (d) none of these
2. The speed of light in a medium of refractive index 2 is <span class="marks">[1]</span>
   (a) $3\times10^8$ m s⁻¹ (b) $6\times10^8$ m s⁻¹ (c) $1.5\times10^8$ m s⁻¹ (d) $2\times10^8$ m s⁻¹
3. The image formed by a convex mirror is always <span class="marks">[1]</span>
   (a) real and inverted (b) virtual and diminished (c) real and magnified (d) virtual and magnified
4. The unit of power of a lens is <span class="marks">[1]</span>
   (a) watt (b) metre (c) dioptre (d) hertz
5. A short-sighted person should use <span class="marks">[1]</span>
   (a) a convex lens (b) a concave lens (c) a plane mirror (d) a cylindrical lens

::: note Answers to Group A
**1.** (b) — air particles vibrate along the direction of the wave.
**2.** (c) — $v = c/n = 3\times10^8/2 = 1.5\times10^8$ m s⁻¹.
**3.** (b) — always virtual, erect and diminished.
**4.** (c) — $P = 1/f$ in metres gives dioptre.
**5.** (b) — a concave lens moves the image back onto the retina.
:::

**Group B — Short answer (2 marks each)**

1. Differentiate between transverse and longitudinal waves. <span class="marks">[2]</span>
2. Why can sound not travel in a vacuum? <span class="marks">[2]</span>
3. State the laws of reflection of light. <span class="marks">[2]</span>
4. What is total internal reflection? Write its two conditions. <span class="marks">[2]</span>
5. Why does a diamond sparkle? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** In a transverse wave the particles vibrate perpendicular to the direction of the wave (crests and troughs, e.g. light); in a longitudinal wave they vibrate along the direction of the wave (compressions and rarefactions, e.g. sound).
**2.** Sound is a mechanical wave and needs particles to pass the vibration on. A vacuum has no particles.
**3.** The incident ray, reflected ray and normal lie in one plane; and the angle of incidence equals the angle of reflection.
**4.** Complete reflection of light back into a denser medium at its boundary with a rarer one. Conditions: light goes from denser to rarer medium, and the angle of incidence is greater than the critical angle.
**5.** Diamond's refractive index (2.42) is very high, so its critical angle (24.4°) is very small. Light entering it is totally internally reflected many times inside before coming out, making it sparkle.
:::

**Group C — Long answer (4 marks each)**

1. A wave has a frequency of 256 Hz and wavelength of 1.33 m. Find the speed of the wave. <span class="marks">[4]</span>
2. A man fires a gun and hears the echo from a hill after 3 s. If the speed of sound is 340 m s⁻¹, find the distance of the hill. <span class="marks">[4]</span>
3. An object 4 cm high is placed 24 cm from a concave mirror of focal length 8 cm. Find the position and height of the image. <span class="marks">[4]</span>
4. Light enters water ($n = 1.33$) from air at 40°. Find the angle of refraction. <span class="marks">[4]</span>
5. An object is kept 10 cm from a convex lens of focal length 15 cm. Find the image distance, magnification and the nature of the image. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** $v = f\lambda = 256 \times 1.33 \approx 340$ m s⁻¹.
**2.** Distance travelled $= 340 \times 3 = 1020$ m; hill distance $= 1020/2 = 510$ m.
**3.** $\dfrac{1}{v} = \dfrac{1}{8} - \dfrac{1}{24} = \dfrac{3-1}{24} = \dfrac{1}{12}$, so $v = 12$ cm (real). $m = 12/24 = 0.5$, so image height $= 0.5 \times 4 = 2$ cm, inverted.
**4.** $\sin r = \dfrac{\sin 40°}{1.33} = \dfrac{0.643}{1.33} = 0.483$, so $r \approx 28.9°$.
**5.** $\dfrac{1}{v} = \dfrac{1}{15} - \dfrac{1}{10} = \dfrac{2-3}{30} = -\dfrac{1}{30}$, so $v = -30$ cm. The image is virtual and on the same side as the object. $m = 30/10 = 3$; virtual, erect and three times larger (a magnifying glass).
:::
