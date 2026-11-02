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
