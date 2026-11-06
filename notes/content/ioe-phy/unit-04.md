---
subject: Physics
grade: IOE
unit: 4
title: Waves and Sound
hours: 2
area: Physics
---

Waves and sound carry about **2 questions** (our estimate), from a short list: $v=f\lambda$, the speed of sound and what changes it, resonance in a closed or open pipe, the fundamental of a stretched string, beats, decibels, and the Doppler effect. Each has a one-line formula; the skill is choosing the right one and keeping track of which end of a pipe is closed.

::: key What the paper asks from this chapter
- $v=f\lambda$; wave equation $y=A\sin(\omega t-kx)$, $k=\frac{2\pi}{\lambda}$; nodes and antinodes.
- Speed of sound: $v=\sqrt{\gamma P/\rho}$, $\propto\sqrt{T}$, independent of pressure at fixed $T$, increases with humidity.
- Pipes: closed $f=\frac{(2n-1)v}{4L}$ (odd harmonics), open $f=\frac{nv}{2L}$ (all harmonics); end correction $0.6r$.
- String: $v=\sqrt{T/\mu}$, $f_1=\frac{1}{2L}\sqrt{T/\mu}$ and the laws of vibration.
- Intensity level $\beta=10\log\frac{I}{I_0}$ dB; beats $|f_1-f_2|$; Doppler $f'=f\frac{v\pm v_o}{v\mp v_s}$.
:::

## 4.1 Wave motion: travelling and stationary waves

A wave transfers energy without transferring matter. **Transverse** (displacement perpendicular to propagation: string, light) and **longitudinal** (compressions and rarefactions: sound). $v=f\lambda$. A progressive wave $y=A\sin(\omega t-kx)$ with $\omega=2\pi f$, $k=\frac{2\pi}{\lambda}$, $v=\frac{\omega}{k}$; phase difference $=\frac{2\pi}{\lambda}\times$ path difference. Intensity $\propto A^2f^2$.

**Stationary waves** form by superposing two identical waves moving oppositely: $y=2A\cos kx\sin\omega t$. Nodes (no motion) are $\frac{\lambda}{2}$ apart, as are the antinodes; every point between two nodes is in phase; no energy is transmitted; amplitude varies with position. A fixed end is a node (phase change $\pi$ on reflection); a free end is an antinode.

## 4.2 Mechanical waves: speed of sound

**Newton–Laplace:** $v=\sqrt{\dfrac{E}{\rho}}$: solid $\sqrt{Y/\rho}$, liquid $\sqrt{B/\rho}$, gas $\sqrt{\gamma P/\rho}=\sqrt{\gamma RT/M}$ (Laplace, adiabatic; Newton's isothermal assumption gave 280 m s⁻¹). Typical values: air 332 m s⁻¹ at 0 °C ($\approx331+0.61t$), water about 1480, steel about 5000 m s⁻¹.
- **Temperature:** $v\propto\sqrt{T}$ (kelvin).
- **Pressure:** no effect at constant temperature ($P/\rho$ is constant).
- **Humidity:** moist air is less dense, so $v$ rises.
- **Gas type:** lighter gas, faster sound ($v_{H_2}\approx4v_{O_2}$ at the same $T$).
- Wind adds its component along the direction.

## 4.3 Waves in pipes and strings

**Closed pipe** (one end closed): node at the closed end, antinode at the open end; $f_n=\dfrac{(2n-1)v}{4L}$ — **only odd harmonics** ($f_1:f_2:f_3=1:3:5$). **Open pipe:** antinodes at both ends; $f_n=\dfrac{nv}{2L}$ — all harmonics ($1:2:3$). A closed pipe's fundamental is half that of an open pipe of the same length. **End correction** $e=0.6r$, so $L+0.6r$ is used.

**Resonance tube:** first resonance at $l_1+e=\frac{\lambda}{4}$, second at $l_2+e=\frac{3\lambda}{4}$; hence $\lambda=2(l_2-l_1)$ and $v=2f(l_2-l_1)$ (end correction cancels).

**Stretched string** (length $L$, tension $T$, mass per length $\mu$): $v=\sqrt{\dfrac{T}{\mu}}$; $f_n=\dfrac{n}{2L}\sqrt{\dfrac{T}{\mu}}$. **Laws of vibration:** $f\propto\frac{1}{L}$, $f\propto\sqrt{T}$, $f\propto\frac{1}{\sqrt{\mu}}$ (or $\frac{1}{r}$ for a given material). The sonometer verifies them; a tuning fork of known frequency resonates with the wire.

## 4.4 Acoustic phenomena

- **Intensity** $I=\frac{P}{A}$ (W m⁻²); threshold of hearing $I_0=10^{-12}$ W m⁻²; **level** $\beta=10\log_{10}\frac{I}{I_0}$ dB (a hundred-fold intensity is $+20$ dB; doubling adds 3 dB). Pressure amplitude $p_0=\sqrt{2\rho vI}$. Loudness is subjective (phon, sone).
- **Pitch** is set by frequency, **loudness** by amplitude (intensity), **quality (timbre)** by the number and strength of overtones.
- **Beats:** two close frequencies give $|f_1-f_2|$ beats per second; adding wax to a fork lowers its frequency; filing raises it.
- **Ultrasonic** $>20$ kHz (sonar, imaging, cleaning, bats); **infrasonic** $<20$ Hz (earthquakes, elephants). Audible range 20 Hz – 20 kHz.
- **Doppler effect:** $f'=f\dfrac{v+v_o}{v-v_s}$ ($v_o$ positive toward the source, $v_s$ positive toward the observer). Approach raises the pitch; recession lowers it. For a 500 Hz source approaching at 34 m s⁻¹: $500\times\frac{340}{306}\approx556$ Hz. If the medium moves, include its speed.

::: caution Wave traps
The wavelength of the closed-pipe fundamental is $4L$ (not $2L$). A change in pressure at constant temperature does not change the speed of sound. Light has no Doppler dependence on a medium but sound does.
:::

```photogrid label="4.1" cols="2" ratio="1.2" caption="Open and closed pipes. (a) Organ pipes: each pipe sounds one note and the pipe length fixes the pitch. An open pipe has an antinode at both ends and supports every harmonic, $f = nv/2L$; a closed pipe has a node at the shut end and supports only odd harmonics, $f = (2n - 1)v/4L$. (b) Frequencies computed for a 0.85 m pipe with the speed of sound 340 m per s: the closed pipe sounds an octave lower and misses the even harmonics."
@ photo id="ioephy/organ" cap="Organ pipes of different lengths"
fit 1.2
focus 0.5 0.5
@ svg cap="0.85 m pipe, v = 340 m/s: allowed frequencies"
v, L = 340.0, 0.85
op = [n * v / (2 * L) for n in range(1, 5)]; cl = [(2 * n - 1) * v / (4 * L) for n in range(1, 5)]
assert op == [200, 400, 600, 800] and cl == [100, 300, 500, 700]
f = Fig(300, 236)
f.text(80, 14, "open pipe", size=10.5, color=TEAL, bold=True); f.text(220, 14, "closed pipe", size=10.5, color=AMBER, bold=True)
Y = lambda hz: 206 - hz * 0.2
f.line(150, 24, 150, 206, color=SLATE, sw=1)
for k in range(0, 900, 100):
    f.text(150, Y(k) + 3, str(k), size=9.5, color=SLATE, bg=None) if False else None
for i, hz in enumerate(op):
    f.box(20, Y(hz) - 9, 100, 18, "f%d = %d Hz" % (i + 1, hz), fill=MINT, stroke=TEAL, size=10.5, bold=True, r=3)
for i, hz in enumerate(cl):
    f.box(180, Y(hz) - 9, 110, 18, "f%d = %d Hz" % (2 * i + 1, hz), fill=SAND, stroke=AMBER, size=10.5, bold=True, r=3)
f.text(150, 230, "ratios 1:2:3:4 and 1:3:5:7", size=10.5, color=NAVY, bold=True)
```

## Formula and fact sheet

| Topic | Result |
|---|---|
| wave speed | $v=f\lambda=\omega/k$ |
| gas | $v=\sqrt{\gamma P/\rho}\propto\sqrt{T}$ |
| closed / open pipe | $\frac{(2n-1)v}{4L}$ / $\frac{nv}{2L}$ |
| string | $\frac{1}{2L}\sqrt{T/\mu}$ |
| level | $10\log(I/I_0)$ dB |
| beats | $|f_1-f_2|$ |
| Doppler | $f\frac{v+v_o}{v-v_s}$ |

## Chapter summary

- $v=f\lambda$; stationary-wave nodes are $\frac{\lambda}{2}$ apart.
- Sound speed depends on temperature, medium and humidity; not on pressure alone.
- Closed pipes give odd harmonics; the resonance-tube method gives $v=2f(l_2-l_1)$.
- A string's frequency rises with tension and falls with length and mass density.
- Beats count the frequency difference; a ten-fold intensity change is 10 dB.

## Practice questions

**Set A — Recall (10 questions)**

1. A source of 500 Hz produces waves of wavelength 0.68 m. The speed of the wave is
   (a) 170 m s⁻¹ (b) 680 m s⁻¹ (c) 340 m s⁻¹ (d) 1000 m s⁻¹
2. If the absolute temperature of a gas is quadrupled, the speed of sound in it
   (a) halves (b) doubles (c) quadruples (d) is unchanged
3. The fundamental frequency of an open pipe 0.5 m long is ($v=340$ m s⁻¹)
   (a) 340 Hz (b) 170 Hz (c) 680 Hz (d) 85 Hz
4. A pipe closed at one end can produce
   (a) no resonance (b) all harmonics (c) only even harmonics (d) only odd harmonics
5. A sound of intensity $10^{-6}$ W m⁻² has an intensity level of
   (a) 6 dB (b) 120 dB (c) 60 dB (d) 600 dB
6. When a source of sound approaches a stationary observer, the observed frequency
   (a) increases (b) decreases (c) is unchanged (d) is zero
7. Ultrasonic waves have frequencies
   (a) below 20 Hz (b) above 20 kHz (c) from 20 Hz to 20 kHz (d) of exactly zero
8. In a stationary wave of wavelength 1 m, the distance between consecutive nodes is
   (a) 1 m (b) 0.25 m (c) 2 m (d) 0.5 m
9. If the tension in a stretched string is made four times, its fundamental frequency
   (a) becomes four times (b) halves (c) doubles (d) is unchanged
10. Two forks of 256 Hz and 260 Hz sounded together produce beats per second equal to
    (a) 4 (b) 258 (c) 516 (d) 2

::: note Answers and explanations — Set A
**1.** (c) — $500\times0.68=340$.
**2.** (b) — $v\propto\sqrt{T}$, $\sqrt{4}=2$.
**3.** (a) — $\frac{v}{2L}=\frac{340}{1}$.
**4.** (d) — closed pipe: $f=\frac{(2n-1)v}{4L}$.
**5.** (c) — $10\log\frac{10^{-6}}{10^{-12}}=60$.
**6.** (a) — approach compresses the waves.
**7.** (b) — above the audible limit.
**8.** (d) — $\frac{\lambda}{2}$.
**9.** (c) — $f\propto\sqrt{T}$.
**10.** (a) — $260-256$.
:::

**Set B — Understanding (6 questions)**

1. The speed of sound in air at 27 °C, taking $v_0=331$ m s⁻¹ at 0 °C and the rule $v=331+0.61\,t$, is
   (a) 347 m s⁻¹ (b) 331 m s⁻¹ (c) 360 m s⁻¹ (d) 300 m s⁻¹
2. A pipe closed at one end is 0.85 m long ($v=340$ m s⁻¹). Its first overtone is
   (a) 100 Hz (b) 200 Hz (c) 300 Hz (d) 400 Hz
3. In a resonance-tube experiment with a 500 Hz fork, resonance occurs at air-column lengths 17 cm and 51 cm. The speed of sound is
   (a) 340 m s⁻¹ (b) 170 m s⁻¹ (c) 680 m s⁻¹ (d) 510 m s⁻¹
4. A 1 m string under 100 N tension has linear density 0.01 kg m⁻¹. Its fundamental frequency is
   (a) 25 Hz (b) 50 Hz (c) 100 Hz (d) 200 Hz
5. A 500 Hz source approaches a stationary observer at 34 m s⁻¹ ($v=340$). The observed frequency is nearly
   (a) 450 Hz (b) 500 Hz (c) 556 Hz (d) 600 Hz
6. If the intensity of a sound is increased 100-fold, the level rises by
   (a) 2 dB (b) 10 dB (c) 100 dB (d) 20 dB

::: note Answers and explanations — Set B
**1.** (a) — $331+0.61\times27=347.5$.
**2.** (c) — $f_1=\frac{340}{4\times0.85}=100$ Hz; the first overtone is the third harmonic, 300 Hz.
**3.** (a) — $v=2f(l_2-l_1)=2\times500\times0.34$.
**4.** (b) — $v=\sqrt{100/0.01}=100$; $f_1=\frac{100}{2\times1}$.
**5.** (c) — $500\times\frac{340}{340-34}=555.6$.
**6.** (d) — $10\log100=20$.
:::

**Set C — Application (4 questions)**

1. A fork of 256 Hz and an unknown fork give 4 beats per second. Loading the unknown fork with wax reduces the beats to 2 per second. The unknown frequency is
   (a) 252 Hz (b) 260 Hz (c) 258 Hz (d) 264 Hz
2. An open pipe has fundamental frequency 300 Hz. If one end is closed, its fundamental becomes
   (a) 150 Hz (b) 300 Hz (c) 600 Hz (d) 75 Hz
3. A whistle of 400 Hz on a train moving at 40 m s⁻¹ ($v=340$) is heard by a stationary person ahead of the train at nearly
   (a) 400 Hz (b) 360 Hz (c) 467 Hz (d) 453 Hz
4. At a point each of 10 identical sources produces a 50 dB level. The combined level is
   (a) 500 dB (b) 51 dB (c) 60 dB (d) 55 dB

::: note Answers and explanations — Set C
**1.** (b) — loading lowers the unknown frequency, and the beats fell from 4 to 2, so the unknown was above 256: it was 260 Hz, loaded down to 258 Hz.
**2.** (a) — open: $\frac{v}{2L}$; closed: $\frac{v}{4L}$, half.
**3.** (d) — $400\times\frac{340}{300}=453$ Hz.
**4.** (c) — intensities add: 10 times, $+10$ dB.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Explain stationary waves in a stretched string, an open pipe and a closed pipe, with the harmonics and numericals. <span class="marks">[10]</span>
2. Derive the speed of sound in a gas, and explain beats, the Doppler effect and the intensity level of sound. <span class="marks">[10]</span>

```photogrid label="4.H" cols="4" ratio="1.25" caption="Waves and sound. (a) An organ pipe sounds because of a stationary wave in an air column. (b) Chladni figures show nodal lines of a vibrating plate. (c) A guitar string vibrates in harmonics. (d) An oscilloscope displays a sound wave as a trace."
@ photo id="ioephy/organ" cap="(a) Organ pipe"
fit 1.25
focus 0.5 0.5
@ photo id="phy12b/chladni" cap="(b) Chladni figure"
fit 1.25
focus 0.5 0.5
@ photo id="phy12b/guitar" cap="(c) Guitar"
fit 1.25
focus 0.5 0.5
@ photo id="phy12b/scope" cap="(d) Oscilloscope"
fit 1.25
focus 0.5 0.5
```

### Model answer D1: Stationary waves in strings and pipes (10 marks)

**Introduction.** A **stationary (standing) wave** forms when two identical waves travel in opposite directions. It has fixed **nodes** (zero displacement) and **antinodes** (maximum displacement) a half wavelength $\frac{\lambda}{2}$ apart, and it carries no net energy.

**Stretched string (fixed at both ends).** The speed is $v = \sqrt{T/\mu}$ and the allowed wavelengths are $\lambda_n = \frac{2L}{n}$, so
$$f_n = \frac{n}{2L}\sqrt{\frac{T}{\mu}},\quad n = 1, 2, 3, \dots$$
All harmonics are present. **Numerical:** $L = 0.6\ \text{m}$, $T = 100\ \text{N}$, $\mu = 0.01\ \text{kg m}^{-1}$: $v = 100\ \text{m s}^{-1}$, $f_1 = 100/1.2 = 83.3\ \text{Hz}$, $f_2 = 166.7\ \text{Hz}$, $f_3 = 250\ \text{Hz}$. **Laws:** $f \propto 1/L$, $f \propto \sqrt{T}$, $f \propto 1/\sqrt{\mu}$.

**Open pipe (both ends open, antinodes at both ends).** $f_n = \frac{nv}{2L}$. All harmonics are present. For $L = 0.5\ \text{m}$ and $v = 340\ \text{m s}^{-1}$: $f_1 = 340\ \text{Hz}$, then $680$ and $1020\ \text{Hz}$.

**Closed pipe (one end closed: node at the closed end, antinode at the open end).** $f_n = \frac{(2n-1)v}{4L}$. Only **odd harmonics** are present. For $L = 0.5\ \text{m}$: $f_1 = 170\ \text{Hz}$, and the next are $510\ \text{Hz}$ and $850\ \text{Hz}$ (ratio 1:3:5).

**End correction.** The antinode is slightly outside the open end, so the effective length is $L + e$, with $e \approx 0.6r$. In the resonance-tube experiment, $v = 2(l_2 - l_1)f$ eliminates $e$.

| Source | Harmonics | Fundamental |
|---|---|---|
| String, both ends fixed | All | $v/2L$ |
| Open pipe | All | $v/2L$ |
| Closed pipe | Odd only | $v/4L$ |

**Conclusion.** The boundary conditions fix the wavelengths, so the tone of an instrument depends on its length and on which harmonics are present.

### Model answer D2: Speed of sound, beats, Doppler effect and intensity (10 marks)

**Introduction.** Sound is a longitudinal mechanical wave that needs a medium.

**Speed of sound.** Newton assumed isothermal changes and got $v = \sqrt{P/\rho}$ (about $280\ \text{m s}^{-1}$), which is wrong. **Laplace** said that compressions are so fast that they are **adiabatic**, so
$$v = \sqrt{\frac{\gamma P}{\rho}}.$$
For air, $\gamma = 1.4$, $P = 1.013\times10^5\ \text{Pa}$, $\rho = 1.29\ \text{kg m}^{-3}$: $v = 331.6\ \text{m s}^{-1}$ at $0^\circ\text{C}$. The speed increases about $0.61\ \text{m s}^{-1}$ per $^\circ\text{C}$, so it is about $343\ \text{m s}^{-1}$ at $20^\circ\text{C}$. It does not depend on pressure at constant temperature, and it increases with humidity.

**Beats.** Two sounds of nearby frequencies $f_1$ and $f_2$ give periodic loud-soft variations. The **beat frequency** is $|f_1 - f_2|$; for $256\ \text{Hz}$ and $260\ \text{Hz}$ it is **4 beats per second**. Musicians use beats to tune instruments.

**Doppler effect.** The apparent frequency changes when the source or observer moves: $f' = f\,\frac{v \pm v_o}{v \mp v_s}$. **Numerical:** a $340\ \text{Hz}$ siren moving at $20\ \text{m s}^{-1}$ towards a still observer ($v = 340$): $f' = 340\times\frac{340}{320} = 361\ \text{Hz}$, and when moving away $f' = 340\times\frac{340}{360} = 321\ \text{Hz}$. It is used in radar, ultrasound blood-flow scans and speed guns.

**Intensity level.** The loudness is measured by $\beta = 10\log_{10}\frac{I}{I_0}$ decibels, with $I_0 = 10^{-12}\ \text{W m}^{-2}$. For $I = 10^{-6}$ the level is $60\ \text{dB}$, and two such sources together ($2\times10^{-6}$) give $63\ \text{dB}$, not $120\ \text{dB}$.

| Effect | Cause | Formula |
|---|---|---|
| Beats | Two close frequencies | $\lvert f_1 - f_2\rvert$ |
| Doppler | Relative motion | $f' = f\,\frac{v \pm v_o}{v \mp v_s}$ |
| Sound level | Logarithmic scale | $10\log(I/I_0)$ |

**Conclusion.** The adiabatic correction of Laplace gives the correct speed, and beats, the Doppler effect and the decibel scale describe how we hear sound.
