---
subject: Physics
grade: IOE
unit: 3
title: Geometric and Physical Optics
hours: 4
area: Physics
---

Optics carries about **4 questions**. The two halves are ray optics (mirror and lens formulae, refraction, prism, total internal reflection) and wave optics (Young's fringe width, grating, Brewster's law, Malus' law). Almost every numerical question uses one of five formulae.

::: key What the paper asks from this chapter
- Mirror $\frac{1}{v}+\frac{1}{u}=\frac{1}{f}$, $f=\frac{R}{2}$; lens $\frac{1}{v}-\frac{1}{u}=\frac{1}{f}$; magnification; sign convention.
- Refraction: Snell, critical angle $\sin C=\frac{1}{n}$, apparent depth, lateral shift.
- Prism: $n=\frac{\sin\frac{A+\delta_m}{2}}{\sin\frac{A}{2}}$; lens maker's formula; lenses in contact $P=P_1+P_2$.
- Dispersion, dispersive power, chromatic aberration, rainbow, scattering ($\propto\lambda^{-4}$).
- Young's fringe width $\beta=\frac{\lambda D}{d}$; diffraction grating $d\sin\theta=n\lambda$; resolving power.
- Polarisation: Brewster's $\tan\theta_p=n$, Malus' law $I=I_0\cos^2\theta$.
:::

## 3.1 Reflection

Laws: the incident ray, reflected ray and normal are coplanar; $\angle i=\angle r$. A plane mirror forms a virtual image as far behind as the object is in front; rotating the mirror by $\theta$ rotates the reflected ray by $2\theta$; two mirrors at angle $\theta$ form $\frac{360^\circ}{\theta}-1$ images. Minimum mirror length to see oneself fully is half one's height.

**Spherical mirrors** (Cartesian sign convention: distances measured from the pole, positive in the direction of the incident light; concave mirror has negative $f$, $R$): $\dfrac{1}{v}+\dfrac{1}{u}=\dfrac{1}{f}=\dfrac{2}{R}$, $m=-\dfrac{v}{u}=\dfrac{h_i}{h_o}$. With the "real-is-positive" shortcut for a concave mirror: object at $u=30$ cm with $f=20$ cm gives $\frac{1}{v}=\frac{1}{20}-\frac{1}{30}$, $v=60$ cm real, inverted, $m=-2$. Convex mirror always gives a virtual, erect, diminished image (rear-view mirrors, wide field).

## 3.2 Refraction

Snell's law $\dfrac{\sin i}{\sin r}={}_1n_2=\dfrac{n_2}{n_1}=\dfrac{v_1}{v_2}$; $n=\frac{c}{v}$; the frequency is unchanged, so $\lambda_{medium}=\frac{\lambda}{n}$. **Apparent depth** $=\frac{\text{real}}{n}$ (a 12 cm column of water, $n=\frac{4}{3}$, looks 9 cm). **Lateral shift** through a slab of thickness $t$: $d=t\sin(i-r)/\cos r$.

**Critical angle:** $\sin C=\dfrac{1}{n}$ (glass 1.5: $41.8^\circ$; $n=\sqrt{2}$: $45^\circ$; diamond 2.42: $24^\circ$). **Total internal reflection** needs light going from the denser to the rarer medium at $i>C$. Applications: prisms in binoculars, mirages, sparkle of diamonds, endoscope, and the **optical fibre** (core $n_1>$ cladding $n_2$): numerical aperture $\text{NA}=\sqrt{n_1^2-n_2^2}$ (core 1.5, cladding 1.4: 0.54); used in telecommunication with very low loss.

**Prism:** $\delta=i+e-A$; minimum deviation when the ray passes symmetrically, $n=\dfrac{\sin\frac{A+\delta_m}{2}}{\sin\frac{A}{2}}$; for a thin prism $\delta=(n-1)A$. For $A=60^\circ$, $n=\sqrt{3}$: $\delta_m=60^\circ$.

**Thin lens:** $\dfrac{1}{v}-\dfrac{1}{u}=\dfrac{1}{f}$ (Cartesian), $m=\dfrac{v}{u}$; **lens maker's formula** $\dfrac{1}{f}=(n-1)\Big(\dfrac{1}{R_1}-\dfrac{1}{R_2}\Big)$ (for $n$ relative to the surrounding medium: a glass lens in water has longer focal length, $f_w=f_a\frac{(n_g-1)}{(n_g/n_w-1)}$; $f_{water}\approx4f_{air}$). **Power** $P=\frac{1}{f}$ (metres) in dioptres; lenses in contact $P=P_1+P_2$, $\frac{1}{f}=\frac{1}{f_1}+\frac{1}{f_2}$; separated by $d$: $\frac{1}{f}=\frac{1}{f_1}+\frac{1}{f_2}-\frac{d}{f_1f_2}$. A convex lens gives a real image with $m=-1$ at $u=2f$. Eye defects: myopia (concave lens), hypermetropia (convex lens). Microscope $M\approx\frac{v_o}{u_o}\cdot\frac{D}{f_e}$, telescope $M=\frac{f_o}{f_e}$.

## 3.3 Dispersion

White light splits into a spectrum because $n$ depends on wavelength ($n_{violet}>n_{red}$; violet bends most). **Dispersive power** $\omega=\dfrac{n_v-n_r}{n_y-1}$. **Angular dispersion** $\delta_v-\delta_r=(n_v-n_r)A$. **Chromatic aberration** (different foci for different colours) is removed by an **achromatic doublet**: convex crown with concave flint, $\frac{\omega_1}{f_1}+\frac{\omega_2}{f_2}=0$. **Spherical aberration** (marginal rays focus nearer) is reduced by a stop or a parabolic mirror. **Rainbow:** dispersion plus internal reflection in raindrops (primary bow: one internal reflection, red outside at $42^\circ$). **Scattering** (Rayleigh) $\propto\lambda^{-4}$: the sky is blue, the Sun red at sunrise and sunset; red is used for danger signals.

## 3.4 Nature and propagation of light

**Huygens' principle:** every point of a wavefront is a source of secondary wavelets, and the envelope forms the new wavefront; it derives the laws of reflection and refraction and shows that light slows down in a denser medium. The speed of light in vacuum $c=3\times10^8$ m s⁻¹ (Römer, Fizeau's toothed wheel, Foucault's rotating mirror, Michelson). In a medium $v=\frac{c}{n}$ ($n=1.5$: $2\times10^8$ m s⁻¹). Wavefronts are plane (distant source), spherical (point source) or cylindrical (slit).

## 3.5 Interference

**Coherent sources** have a constant phase difference (produced by splitting one wavefront). **Young's double slit:** path difference $\Delta=\frac{yd}{D}$; bright fringe $\Delta=n\lambda$, dark $(n+\frac{1}{2})\lambda$; **fringe width** $\beta=\dfrac{\lambda D}{d}$ (for $\lambda=600$ nm, $D=1$ m, $d=1$ mm: 0.6 mm). Immersing the apparatus in a medium of index $n$ reduces $\beta$ to $\frac{\beta}{n}$; a thin sheet of thickness $t$ over one slit shifts the pattern by $\frac{(n-1)tD}{d}$. Intensity $I=4I_0\cos^2\frac{\phi}{2}$; for two sources of intensities $I_1,I_2$: $I_{max}/I_{min}=\Big(\frac{\sqrt{I_1}+\sqrt{I_2}}{\sqrt{I_1}-\sqrt{I_2}}\Big)^2$. Thin films (colours of soap bubbles) and Newton's rings are the same effect. Interference is energy redistribution, not creation.

## 3.6 Diffraction

Bending of waves around obstacles; significant when the aperture is comparable with $\lambda$. **Fraunhofer single slit:** minima at $a\sin\theta=n\lambda$; central maximum width $\frac{2\lambda D}{a}$. **Diffraction grating:** $d\sin\theta=n\lambda$ with $d=\frac{1}{N}$ (5000 lines cm⁻¹: $d=2\,\mu$m; $\lambda=500$ nm gives $\sin\theta_1=0.25$); the maximum order is $n<\frac{d}{\lambda}$. **Resolving power** of a telescope: minimum angle $\theta=\dfrac{1.22\lambda}{D}$ (Rayleigh); a larger aperture resolves better; microscope $\frac{2n\sin\theta}{1.22\lambda}$; grating $\frac{\lambda}{\Delta\lambda}=nN$.

## 3.7 Polarization

Polarisation proves light is a **transverse** wave (sound cannot be polarised). **Malus' law:** $I=I_0\cos^2\theta$; unpolarised light through a polariser loses half. **Brewster's law:** reflected light is completely polarised when $\tan\theta_p=n$, and the reflected and refracted rays are at $90^\circ$ ($n=\sqrt{3}$: $60^\circ$). **Polaroid** (aligned molecules) is used in sunglasses (to cut glare) and 3-D cinema. Optical activity (sugar solution) and double refraction (calcite).

::: caution Optics traps
Sign convention first: write it down. Frequency never changes on refraction. TIR needs *denser to rarer*. A larger refractive index means a *shorter* wavelength and a *smaller* fringe width. Brewster's angle depends on $n$.
:::

```photogrid label="3.1" cols="2" ratio="1.2" caption="Total internal reflection in practice. (a) A green laser beam guided inside an acrylic rod: light that meets the wall beyond the critical angle is reflected completely and stays inside, even round a bend. An optical fibre does the same with a glass core of index 1.48 in a cladding of index 1.46. (b) The values that follow from those two numbers, computed here: critical angle $\\sin C = n_2/n_1$, numerical aperture $NA = \\sqrt{n_1^2 - n_2^2}$ and the acceptance half-angle in air."
@ photo id="ioephy/fibre" cap="Light guided inside a transparent rod by total internal reflection"
fit 1.2
focus 0.5 0.5
@ svg cap="Core 1.48, cladding 1.46: what light survives"
import math
n1, n2 = 1.48, 1.46
C = math.degrees(math.asin(n2 / n1)); NA = math.sqrt(n1 ** 2 - n2 ** 2); acc = math.degrees(math.asin(NA))
assert abs(C - 80.6) < 0.1 and abs(acc - 14.0) < 0.1
loss_db = 0.2 * 100; frac = 10 ** (-loss_db / 10)
f = Fig(300, 236)
f.box(10, 20, 280, 12, "", fill=SAND, stroke=AMBER, r=1, sw=1); f.box(10, 32, 280, 36, "", fill=MINT, stroke=TEAL, r=1, sw=1); f.box(10, 68, 280, 12, "", fill=SAND, stroke=AMBER, r=1, sw=1)
f.text(150, 95, "core n1 = 1.48", size=10.5, color=TEAL, bold=True)
f.text(150, 14, "cladding n2 = 1.46", size=10.5, color=AMBER, bold=True)
pts = [(14, 50), (62, 32), (110, 68), (158, 32), (206, 68), (254, 32), (286, 50)]
f.arrow(pts, color=RED, sw=1.6)
f.text(150, 108, "critical angle C = %.1f°" % C, size=10.5, color=NAVY, bold=True)
f.text(150, 128, "NA = √(n1² - n2²) = %.3f" % NA, size=10.5, color=NAVY, bold=True)
f.text(150, 148, "acceptance half-angle = %.1f° (air)" % acc, size=10.5, color=TEAL, bold=True)
f.text(150, 176, "loss 0.2 dB/km over 100 km = %d dB" % loss_db, size=10.5, color=SLATE)
f.text(150, 196, "power left = %.0f%% of the input" % (frac * 100), size=10.5, color=RED, bold=True)
f.text(150, 218, "rays steeper than 14° leak out", size=10.5, color=SLATE)
```

## Formula and fact sheet

| Topic | Result |
|---|---|
| mirror | $\frac{1}{v}+\frac{1}{u}=\frac{2}{R}$ |
| lens | $\frac{1}{v}-\frac{1}{u}=\frac{1}{f}$; $\frac{1}{f}=(n-1)(\frac{1}{R_1}-\frac{1}{R_2})$ |
| critical angle | $\sin C=\frac{1}{n}$ |
| apparent depth | real depth$/n$ |
| prism | $n=\frac{\sin(A+\delta_m)/2}{\sin A/2}$ |
| dispersive power | $\frac{n_v-n_r}{n_y-1}$ |
| fringe width | $\frac{\lambda D}{d}$ |
| grating | $d\sin\theta=n\lambda$ |
| Brewster / Malus | $\tan\theta_p=n$ / $I_0\cos^2\theta$ |
| resolving angle | $\frac{1.22\lambda}{D}$ |

## Chapter summary

- Mirror and lens formulas are used with a consistent sign convention.
- $\sin C=1/n$; TIR only from dense to rare; fibres use it with NA $=\sqrt{n_1^2-n_2^2}$.
- Prisms: minimum deviation relation; thin prism $\delta=(n-1)A$.
- Violet bends most; achromatism needs two glasses.
- $\beta=\frac{\lambda D}{d}$ shrinks in a medium.
- Polarisation shows light is transverse; Brewster and Malus give the numbers.

## Practice questions

**Set A — Recall (10 questions)**

1. The focal length of a concave mirror of radius 40 cm is
   (a) 10 cm (b) 20 cm (c) 40 cm (d) 80 cm
2. The critical angle for a medium of refractive index $\sqrt{2}$ is
   (a) $30^\circ$ (b) $60^\circ$ (c) $45^\circ$ (d) $90^\circ$
3. The power of a lens of focal length 50 cm is
   (a) 2 D (b) 0.5 D (c) 5 D (d) 50 D
4. Total internal reflection can occur when light travels from
   (a) air to water (b) a rarer to a denser medium (c) a denser to a rarer medium (d) air to glass
5. A rainbow is formed by
   (a) interference (b) diffraction (c) polarisation (d) dispersion with total internal reflection
6. Light is completely polarised on reflection from a medium of index $\sqrt{3}$ at the angle
   (a) $60^\circ$ (b) $30^\circ$ (c) $45^\circ$ (d) $90^\circ$
7. In Young's experiment $\lambda=600$ nm, $D=1$ m and $d=1$ mm. The fringe width is
   (a) 0.06 mm (b) 0.6 mm (c) 6 mm (d) 0.3 mm
8. The transverse nature of light is shown by
   (a) interference (b) diffraction (c) reflection (d) polarisation
9. The speed of light in a medium of refractive index 1.5 is
   (a) $3\times10^8$ m s⁻¹ (b) $2\times10^8$ m s⁻¹ (c) $4.5\times10^8$ m s⁻¹ (d) $1.5\times10^8$ m s⁻¹
10. A biconvex glass lens ($n=1.5$) has both radii 20 cm. Its focal length is
    (a) 10 cm (b) 40 cm (c) 20 cm (d) 30 cm

::: note Answers and explanations — Set A
**1.** (b) — $f=\frac{R}{2}$.
**2.** (c) — $\sin C=\frac{1}{\sqrt{2}}$.
**3.** (a) — $P=\frac{1}{0.5}=2$ D.
**4.** (c) — only from denser to rarer, with $i>C$.
**5.** (d) — refraction and dispersion in the drop, with internal reflection.
**6.** (a) — $\tan\theta_p=\sqrt{3}$.
**7.** (b) — $\frac{\lambda D}{d}=\frac{600\times10^{-9}\times1}{10^{-3}}$.
**8.** (d) — only transverse waves can be polarised.
**9.** (b) — $\frac{3\times10^8}{1.5}$.
**10.** (c) — $\frac{1}{f}=0.5\big(\frac{1}{20}+\frac{1}{20}\big)=\frac{1}{20}$.
:::

**Set B — Understanding (7 questions)**

1. An object is 30 cm from a concave mirror of focal length 20 cm. The image distance is
   (a) 60 cm (b) 12 cm (c) 30 cm (d) 15 cm
2. A convex lens of $f=10$ cm forms the image of an object placed 15 cm away at
   (a) 6 cm (b) 25 cm (c) 30 cm (d) 150 cm
3. A prism of angle $60^\circ$ and index $\sqrt{3}$ has minimum deviation
   (a) $60^\circ$ (b) $30^\circ$ (c) $45^\circ$ (d) $75^\circ$
4. Two thin lenses of powers $+10$ D and $-2.5$ D are in contact. The combination has power
   (a) 12.5 D (b) 7.5 D (c) 25 D (d) 4 D
5. A fish is 12 cm below the surface of water ($n=\frac{4}{3}$). Its apparent depth is
   (a) 16 cm (b) 12 cm (c) 8 cm (d) 9 cm
6. A grating has 5000 lines per cm. For $\lambda=500$ nm the first-order $\sin\theta$ is
   (a) 0.5 (b) 0.1 (c) 0.25 (d) 0.75
7. When the whole Young's apparatus is immersed in water ($n=\frac{4}{3}$), the fringe width
   (a) increases by $\frac{4}{3}$ (b) is unchanged (c) vanishes (d) decreases to $\frac{3}{4}$ of its value

::: note Answers and explanations — Set B
**1.** (a) — $\frac{1}{v}=\frac{1}{20}-\frac{1}{30}=\frac{1}{60}$: real image, $m=-2$.
**2.** (c) — $\frac{1}{v}=\frac{1}{10}-\frac{1}{15}=\frac{1}{30}$.
**3.** (a) — $\sin\frac{A+\delta_m}{2}=\sqrt{3}\sin30^\circ=\frac{\sqrt{3}}{2}$, so $\frac{60+\delta_m}{2}=60^\circ$.
**4.** (b) — powers add: $10-2.5$.
**5.** (d) — $12\times\frac{3}{4}=9$ cm.
**6.** (c) — $d=\frac{1}{5000\,\text{cm}^{-1}}=2\,\mu$m; $\sin\theta=\frac{0.5}{2}$.
**7.** (d) — $\lambda_{water}=\frac{\lambda}{n}$, so $\beta\to\frac{\beta}{n}$.
:::

**Set C — Application (5 questions)**

1. A convex lens forms a real image twice the size of the object on a screen 60 cm from the lens. Its focal length is
   (a) 15 cm (b) 20 cm (c) 40 cm (d) 30 cm
2. An optical fibre has a core of index 1.5 and cladding of 1.4. Its numerical aperture is
   (a) 0.54 (b) 0.1 (c) 0.29 (d) 1.0
3. A telescope objective has aperture 0.1 m. For $\lambda=500$ nm the minimum angular separation resolved is
   (a) $5\times10^{-6}$ rad (b) $6.1\times10^{-7}$ rad (c) $6.1\times10^{-6}$ rad (d) $1.2\times10^{-5}$ rad
4. Unpolarised light of intensity $I_0$ passes through two polaroids whose axes are at $60^\circ$. The emerging intensity is
   (a) $I_0/2$ (b) $I_0/4$ (c) 0 (d) $I_0/8$
5. A glass lens ($n=1.5$) has focal length 20 cm in air. In water ($n=\frac{4}{3}$) its focal length is
   (a) 80 cm (b) 40 cm (c) 20 cm (d) 60 cm

::: note Answers and explanations — Set C
**1.** (b) — $v=2u=60\Rightarrow u=30$; $\frac{1}{f}=\frac{1}{30}+\frac{1}{60}=\frac{1}{20}$.
**2.** (a) — $\sqrt{1.5^2-1.4^2}=\sqrt{0.29}$.
**3.** (c) — $\frac{1.22\times5\times10^{-7}}{0.1}$.
**4.** (d) — $\frac{I_0}{2}\cos^260^\circ=\frac{I_0}{8}$.
**5.** (a) — $\frac{1/f_w}{1/f_a}=\frac{1.5/(4/3)-1}{0.5}=\frac{0.125}{0.5}=\frac{1}{4}$, so $f_w=4f_a$.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Derive the lens maker's formula and the prism formula, and explain total internal reflection and its applications. <span class="marks">[10]</span>
2. Describe Young's double-slit experiment, diffraction by a grating and polarisation, with numericals. <span class="marks">[10]</span>

```photogrid label="3.H" cols="4" ratio="1.25" caption="Light in practice. (a) A glass prism disperses white light into a spectrum. (b) A rainbow forms by refraction, internal reflection and dispersion in raindrops. (c) Newton's rings are fringes from a thin air film. (d) An optical fibre guides light by total internal reflection."
@ photo id="phy11/prism" cap="(a) Prism"
fit 1.25
focus 0.5 0.5
@ photo id="ceephy/rainbow" cap="(b) Rainbow"
fit 1.25
focus 0.5 0.5
@ photo id="cee-phy/newtons-rings" cap="(c) Newton's rings"
fit 1.25
focus 0.5 0.5
@ photo id="ioephy/fibre" cap="(d) Optical fibre"
fit 1.25
focus 0.5 0.5
```

### Model answer D1: Refraction, lenses, prisms and total internal reflection (10 marks)

**Introduction.** Refraction is the bending of light when it passes from one medium to another, because its speed changes. **Snell's law:** $n_1\sin i = n_2\sin r$, where $n = c/v$.

**Lens maker's formula.** For a thin lens of refractive index $n$ with surfaces of radii $R_1$ and $R_2$ in air:
$$\frac{1}{f} = (n-1)\left(\frac{1}{R_1} - \frac{1}{R_2}\right).$$
It is found by applying the refraction formula $\frac{n_2}{v} - \frac{n_1}{u} = \frac{n_2 - n_1}{R}$ at each surface and adding the two results. For a double-convex lens with $n = 1.5$ and $R = 20\ \text{cm}$ on both sides: $\frac{1}{f} = 0.5\times\frac{2}{20} = 0.05$, so $f = 20\ \text{cm}$. For an object $30\ \text{cm}$ away, $\frac{1}{v} = \frac{1}{20} - \frac{1}{30} = \frac{1}{60}$, so $v = 60\ \text{cm}$ (real, inverted) and $m = -2$.

**Prism formula.** For a prism of angle $A$ at minimum deviation $D_m$:
$$n = \frac{\sin\frac{A + D_m}{2}}{\sin\frac{A}{2}}.$$
For $A = 60^\circ$ and $n = 1.5$: $\sin\frac{60 + D_m}{2} = 0.75$, so $D_m = 37.2^\circ$. Because $n$ is greater for violet than for red, **dispersion** occurs.

**Total internal reflection (TIR).** It occurs when light goes from a denser to a rarer medium at an angle of incidence **greater than the critical angle** $C$, where $\sin C = \frac{1}{n}$. For glass ($n = 1.5$), $C = 41.8^\circ$; for water ($n = 1.33$), $C = 48.8^\circ$.

**Applications of TIR.**

1. **Optical fibres** carry telephone and internet signals (as in Nepal's fibre-to-home service) with little loss.
2. **Totally reflecting prisms** in binoculars and periscopes.
3. **Mirage** and the sparkle of **diamond** ($n = 2.42$, $C = 24.4^\circ$).
4. **Endoscopes** that let doctors see inside the body.

| Quantity | Formula | Value in example |
|---|---|---|
| Lens focal length | Lens maker's | $20\ \text{cm}$ |
| Minimum deviation | Prism | $37.2^\circ$ |
| Critical angle | $\sin C = 1/n$ | $41.8^\circ$ (glass) |

**Conclusion.** The same law of refraction explains lenses, prisms, dispersion and the guiding of light in fibres.

### Model answer D2: Interference, diffraction and polarisation (10 marks)

**Introduction.** These three effects prove that light is a **wave**, and polarisation shows that it is a **transverse** wave.

**Young's double-slit experiment.** Light from a single slit falls on two narrow slits $S_1$ and $S_2$ (distance $d$) and forms bright and dark **fringes** on a screen at distance $D$.

1. **Bright fringes (path difference = $n\lambda$):** $y_n = \frac{n\lambda D}{d}$.
2. **Dark fringes:** path difference $(2n+1)\frac{\lambda}{2}$.
3. **Fringe width:** $\beta = \frac{\lambda D}{d}$, equal for all fringes.
4. Conditions: the sources must be **coherent** and narrow, and close together.

Numerical: $\lambda = 600\ \text{nm}$, $D = 1.5\ \text{m}$, $d = 0.3\ \text{mm}$: $\beta = \frac{600\times10^{-9}\times1.5}{0.3\times10^{-3}} = 3\ \text{mm}$.

**Diffraction.** The bending of light around an edge or slit. For a single slit of width $a$, the minima are at $a\sin\theta = n\lambda$ and the central maximum is twice as wide as the others. A **diffraction grating** with $d$ distance between lines gives maxima at $d\sin\theta = n\lambda$. For a grating of $5000$ lines per cm, $d = 2\ \mu\text{m}$, so for sodium light ($589\ \text{nm}$) the first order is at $\theta = \sin^{-1}(0.2945) = 17.1^\circ$.

**Polarisation.** Light vibrates in one plane after passing through a polaroid. **Malus' law:** $I = I_0\cos^2\theta$; at $\theta = 30^\circ$ the intensity is $0.75\,I_0$. **Brewster's law:** reflected light is fully polarised when $\tan i_p = n$; for $n = \sqrt{3}$, $i_p = 60^\circ$. Uses: polaroid sun glasses and 3-D cinema.

| Effect | Condition | Formula |
|---|---|---|
| Interference | Two coherent sources | $\beta = \lambda D/d$ |
| Diffraction | Slit width near $\lambda$ | $d\sin\theta = n\lambda$ |
| Polarisation | Transverse waves | $I = I_0\cos^2\theta$ |

**Conclusion.** Interference and diffraction confirm the wave nature of light, and polarisation shows that the waves are transverse.
