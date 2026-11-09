---
file: NEBians-IOE-Past-Paper-Filter-Design-ENEX301-2082-Chaitra.pdf
subject: Filter Design
level: BE · Year III / Part I
code: ENEX 301
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Tables are attached herewith · Assume suitable data if necessary</small>

@q 1
What is filter? Explain its application in the field of communication. Differentiate between ideal and practical response for various filters. [[1+1+3]]

@q 2
During filter design process, explain the significance of normalization and denormalization. Derive the expression to calculate the new values of elements that will modify the operating frequency of a low pass filter from $\omega_{old}$ to $\omega_{new}$. [[2+2]]

@q 3
What are the characteristics of Butterworth low pass approximation? [[3]]

@q 4
Derive an expression to calculate the order of Chebyshev low pass filter and use it to find the order of Chebyshev low pass filter having following specifications: $\alpha_{max} = 1$ dB, $\alpha_{min} = 18$ dB, $\omega_p = 1000$ rad/sec, $\omega_s = 1400$ rad/sec. Also determine the pole locations and transfer function. [[3+3+3]]

@q 5
Define frequency transformation and mention its importance in filter design. [[3]]

@q 6
Synthesize 4th order Butterworth HPF in resistively terminated lossless ladder network. [[6]]

@q 7
Which of the following is an LC lossless function and why? Pick one of the valid LC lossless functions and realize it using Foster-I and Cauer-I form.

a) $Z_1(s) = \dfrac{s(s^2+4)(s^2+6)}{(s^2+3)(s^2+9)}$

b) $Z_2(s) = \dfrac{(s^2+3)(s^2+6)}{s(s^2+4)(s^2+9)}$

c) $Z_3(s) = \dfrac{(s^2+4)(s^2+6)}{s(s^2+3)(s^2+9)}$

d) $Z_4(s) = \dfrac{(s^2+3)(s^2+6)}{(s^2+4)(s^2+9)}$ [[2+6]]

@q 8
Draw the circuit diagram of Tow-Thomas biquad circuit and derive its transfer function. For an ECG machine of a hospital, you are asked to design a low pass filter using Tow-Thomas biquad circuit with poles located at $-450\pm j\,893.03$ and DC gain of 1.3. Make sure the elements in the final circuit are of practically realizable values. [[3+5]]

@q 9
How can excess gain be compensated in Sallen-key circuit? Explain with necessary derivations and diagrams. [[7]]

@q 10
Perform the sensitivity analysis of quality factor in Tow Thomas LPF. [[3]]

@q 11
What is the significance of using current mode filters in the electronic circuit? With basic block diagram and characteristic equations explain the concepts of first-generation current conveyor (CCI) and second-generation current conveyor (CCII). [[1+3]]

*Table 1: pole locations of Butterworth responses.* $n=2$: $-0.7071068\pm j0.7071068$. $n=3$: $-0.5000000\pm j0.8660254$ and $-1.0$. $n=4$: $-0.3826834\pm j0.9238795$ and $-0.9238795\pm j0.3826834$. $n=5$: $-0.8090170\pm j0.5877852$, $-0.3090170\pm j0.9510565$ and $-1.0$.

*Table 2: element values of the doubly terminated Butterworth low-pass ladder (1 $\Omega$ terminations, half-power frequency 1 rad/s; $C_1$ is the first shunt capacitor after the source resistor, then $L_2$ in series, $C_3$ shunt, and so on).*

| $n$ | $C_1$ | $L_2$ | $C_3$ | $L_4$ | $C_5$ |
|---|---|---|---|---|---|
| 2 | 1.414 | 1.414 | | | |
| 3 | 1 | 2 | 1 | | |
| 4 | 0.7654 | 1.848 | 1.848 | 0.7654 | |
| 5 | 0.618 | 1.618 | 2 | 1.618 | 0.618 |
<!-- SOLUTIONS -->

@s 1
**Filter.** A filter is a circuit (or system) that passes signals of some frequencies with little loss (the **passband**) and rejects or strongly attenuates signals of other frequencies (the **stopband**). Its behaviour is described by the transfer function $H(s)$ or the magnitude response $|H(j\omega)|$. Filters may be passive (R, L, C), active (op-amps, current conveyors) or digital, and by the passband they are low-pass (LP), high-pass (HP), band-pass (BP) and band-stop (BS or notch).

**Applications in communication**

1. **Channel selection:** band-pass filters in the tuner/IF stages of a receiver select the wanted channel and reject the adjacent ones.
2. **Noise and interference rejection:** removing out-of-band noise, harmonics and spurious signals.
3. **Harmonic suppression:** low-pass filters after the power amplifier of a transmitter limit the radiated harmonics.
4. **Anti-aliasing and reconstruction:** low-pass filters before the A/D converter and after the D/A converter.
5. **Image rejection** in superheterodyne receivers, and duplexers for the transmit and receive bands.
6. **Pulse shaping and equalisation:** raised-cosine filters in digital links, equalisers for channel distortion, FDM multiplexing, demodulation of AM/FM, and DC blocking and power supply decoupling.

**Ideal and practical response.**

| | Ideal filter | Practical filter |
|---|---|---|
| Passband | Constant gain, no ripple | Ripple or droop (gain between $1$ and $1-\delta_p$, i.e. $\alpha_{max}$) |
| Transition | Zero width, abrupt (brick wall) at the cut-off | Finite width between $\omega_p$ and $\omega_s$ |
| Stopband | Zero gain (infinite attenuation) | Limited attenuation $\ge\alpha_{min}$, with possible ripple |
| Phase | Linear phase (constant delay) | Non-linear phase, group delay varies |
| Impulse response | Non-causal, infinite ($\text{sinc}$), not realisable | Causal and realisable, using a finite order $N$ |
| Specification | Only the cut-off frequency | $\omega_p,\ \omega_s,\ \alpha_{max},\ \alpha_{min}$ and the order $N$ |

Practical filters approximate the ideal one using Butterworth (flat), Chebyshev (equiripple), inverse Chebyshev, elliptic (Cauer) or Bessel (linear phase) functions. A higher order gives a response closer to the ideal at a greater cost.

```figure caption="Ideal (brick-wall) low-pass response compared with a practical response: passband ripple (alpha_max), transition band between wp and ws, and finite stopband attenuation (alpha_min)."
import numpy as np, matplotlib.pyplot as plt
w=np.linspace(0,3,600)
fig,ax=plt.subplots(figsize=(5.4,2.6))
ax.plot([0,1,1,3],[1,1,0,0],color='#999',lw=1.5,ls='--',label="ideal")
H=1/np.sqrt(1+(w/1.05)**8)
ax.plot(w,H,color=ACCENT,lw=1.6,label="practical (Butterworth N = 4)")
ax.axvline(1,color='#bbb',lw=.7); ax.axvline(1.5,color='#bbb',lw=.7); ax.axhline(0.891,color='#bbb',lw=.7,ls=':'); ax.axhline(0.126,color='#bbb',lw=.7,ls=':')
ax.text(1.0,1.06,"$\\omega_p$",ha='center',fontsize=8); ax.text(1.5,1.06,"$\\omega_s$",ha='center',fontsize=8)
ax.text(2.0,0.15,"stopband ($\\geq\\alpha_{min}$)",fontsize=7); ax.text(0.05,0.82,"passband ($\\leq\\alpha_{max}$)",fontsize=7); ax.text(1.05,0.5,"transition",fontsize=7)
ax.set_xlabel("$\\omega$ (normalised)"); ax.set_ylabel("$|H(j\\omega)|$"); ax.set_ylim(0,1.15); ax.legend(fontsize=7,loc="upper right"); ax.grid(False)
```

@s 2
**Normalization.** Filters are first designed (or looked up in tables) for a **normalised prototype**, a low-pass filter with a cut-off frequency of $\omega_c = 1$ rad/s and terminating resistance $R = 1\,\Omega$.

*Significance:*

1. One set of tables (for each approximation and order) serves every cut-off frequency and every impedance level; the design is done once.
2. It keeps the numbers near unity (for example $1.414$ F and $1.414$ H) and so avoids numerical difficulties with values such as $10^{-9}$ F or $10^{4}$ rad/s.
3. The responses of different approximations and orders can be compared directly.
4. It makes the frequency transformations LP to HP, BP and BS easy, as they are applied to a single prototype.

**Denormalization** is the reverse process: the normalised elements are scaled to the real frequency and impedance level.

*Frequency scaling (derivation).* The impedance of an inductor is $Z_L = j\omega L$ and of a capacitor $Z_C = 1/j\omega C$. To make the response at the new frequency $\omega_{new}$ identical to the response at $\omega_{old}$, each element must show the same impedance at the new frequency as it had at the old one:

$$\begin{gathered}\omega_{new}L_{new} = \omega_{old}L_{old} \\ \frac{1}{\omega_{new}C_{new}} = \frac{1}{\omega_{old}C_{old}}\end{gathered}$$

$$\boxed{L_{new} = L_{old}\,\frac{\omega_{old}}{\omega_{new}},\qquad C_{new} = C_{old}\,\frac{\omega_{old}}{\omega_{new}},\qquad R_{new} = R_{old}}$$

Resistors are independent of frequency and are not changed. The frequency scale factor is $k_f = \omega_{new}/\omega_{old}$, so $L$ and $C$ are divided by $k_f$.

*Impedance scaling* (for completeness): with the scale factor $k_z$ all impedances are multiplied by $k_z$, so $R' = k_zR$, $L' = k_zL$, $C' = C/k_z$. Combining both, from the normalised values $(R_n = 1,\ L_n,\ C_n,\ \omega_n = 1)$:

$$\begin{gathered}R = k_zR_n \\ L = \frac{k_z}{k_f}L_n \\ C = \frac{C_n}{k_zk_f}.\end{gathered}$$

For example, a normalised 1 H inductor of a filter at $\omega_c = 10^4$ rad/s with $R = 600\,\Omega$ becomes $L = 600\times1/10^4 = 60$ mH.

@s 3
**Characteristics of the Butterworth low-pass approximation**

The magnitude-squared function of an $N$th order Butterworth low-pass filter is

$$|H(j\omega)|^2 = \frac{1}{1 + \left(\dfrac{\omega}{\omega_c}\right)^{2N}}$$

1. **Maximally flat passband:** the first $2N-1$ derivatives of $|H|$ at $\omega = 0$ are zero; the response is monotonic, with no ripple in either the passband or the stopband.
2. **3-dB point:** at $\omega = \omega_c$ the gain is $1/\sqrt2$ ($-3.01$ dB) for every order $N$.
3. **Roll-off:** the attenuation in the stopband increases at $20N$ dB/decade ($6N$ dB/octave). A larger $N$ gives a steeper transition, and the response approaches the ideal brick wall.
4. **Poles:** the $N$ poles lie on a circle of radius $\omega_c$ in the left half plane, equally spaced by $\pi/N$ at the angles $\theta_k = \dfrac{\pi}{2}+\dfrac{(2k-1)\pi}{2N}$, so they are always stable; for example $-0.7071\pm j0.7071$ for $N = 2$ and $-0.3827\pm j0.9239$, $-0.9239\pm j0.3827$ for $N = 4$ (from Table 1). All the zeros are at $s = \infty$ (an all-pole filter).
5. **Transfer function:** $H(s) = \dfrac{1}{B_N(s)}$ with the Butterworth polynomials $s^2 + 1.414s + 1$, $(s+1)(s^2+s+1)$, $(s^2+0.7654s+1)(s^2+1.8478s+1)$ for $N = 2,3,4$.
6. **Order:** $N \ge \dfrac{\log\left[(10^{0.1\alpha_{min}}-1)/(10^{0.1\alpha_{max}}-1)\right]}{2\log(\omega_s/\omega_p)}$.
7. **Phase and delay:** the phase is non-linear but smoother than that of Chebyshev; the step response has a moderate overshoot and the group delay is flatter than for a Chebyshev filter of the same order.
8. The transition is wider than for Chebyshev and elliptic filters of the same order, so a larger order is needed for the same specification.

@s 4
**Derivation of the order.** The Chebyshev (type I) low-pass response is

$$|H(j\omega)|^2 = \frac{1}{1+\varepsilon^2C_N^2(\omega/\omega_p)},\qquad C_N(x) = \begin{cases}\cos(N\cos^{-1}x), & |x|\le1\\ \cosh(N\cosh^{-1}x), & |x|>1\end{cases}$$

In the passband $C_N$ oscillates between $-1$ and $1$, so the gain ripples between $1$ and $1/\sqrt{1+\varepsilon^2}$. The maximum passband attenuation is

$$\alpha_{max} = 10\log(1+\varepsilon^2)\ \Rightarrow\ \varepsilon^2 = 10^{0.1\alpha_{max}} - 1$$

In the stopband ($\omega\ge\omega_s>\omega_p$) the minimum attenuation is

$$\alpha_{min} = 10\log\left[1 + \varepsilon^2\cosh^2\left(N\cosh^{-1}\frac{\omega_s}{\omega_p}\right)\right]$$

Solving for $N$:

$$\cosh^2\left(N\cosh^{-1}\frac{\omega_s}{\omega_p}\right) = \frac{10^{0.1\alpha_{min}}-1}{\varepsilon^2} = \frac{10^{0.1\alpha_{min}}-1}{10^{0.1\alpha_{max}}-1}$$

$$\boxed{N \ge \frac{\cosh^{-1}\sqrt{\dfrac{10^{0.1\alpha_{min}}-1}{10^{0.1\alpha_{max}}-1}}}{\cosh^{-1}(\omega_s/\omega_p)}}$$

**Order for the given specification** ($\alpha_{max} = 1$ dB, $\alpha_{min} = 18$ dB, $\omega_p = 1000$, $\omega_s = 1400$ rad/s):

$$\begin{gathered}\varepsilon^2 = 10^{0.1} - 1 = 0.2589 \\ \varepsilon = 0.5088\end{gathered}$$

$$\begin{gathered}\sqrt{\frac{10^{1.8}-1}{10^{0.1}-1}} = \sqrt{\frac{62.096}{0.2589}} = 15.486 \\ \cosh^{-1}(15.486) = 3.432\end{gathered}$$

$$\cosh^{-1}\left(\frac{1400}{1000}\right) = \cosh^{-1}(1.4) = 0.8670$$

$$N \ge \frac{3.432}{0.8670} = 3.96\quad\Rightarrow\quad\boxed{N = 4}$$

**Pole locations.** The poles of the normalised ($\omega_p = 1$) filter are

$$\begin{gathered}s_k = -\sinh a\,\sin\theta_k + j\cosh a\,\cos\theta_k \\ \theta_k = \frac{(2k-1)\pi}{2N},\quad a = \frac1N\sinh^{-1}\frac1\varepsilon\end{gathered}$$

$$\begin{gathered}a = \frac14\sinh^{-1}(1.9652) = \frac14(1.4280) = 0.3570 \\ \sinh a = 0.3646,\quad\cosh a = 1.0644\end{gathered}$$

The angles are $\theta_k = 22.5^\circ, 67.5^\circ, 112.5^\circ, 157.5^\circ$ for $k = 1,\dots,4$.

| $k$ | $\theta_k$ | Normalised pole | Scaled pole ($\times\,1000$ rad/s) |
|---|---|---|---|
| 1 | $22.5^\circ$ | $-0.1395 + j0.9834$ | $-139.5 + j983.4$ |
| 2 | $67.5^\circ$ | $-0.3369 + j0.4073$ | $-336.9 + j407.3$ |
| 3 | $112.5^\circ$ | $-0.3369 - j0.4073$ | $-336.9 - j407.3$ |
| 4 | $157.5^\circ$ | $-0.1395 - j0.9834$ | $-139.5 - j983.4$ |

The poles lie on an ellipse with semi-axes $\sinh a\cdot\omega_p = 364.6$ (real) and $\cosh a\cdot\omega_p = 1064.4$ (imaginary).

**Transfer function.** Pairing the conjugate poles, with $s^2 + 2|\text{Re}\,p|s + |p|^2$:

$$(s^2 + 279.07s + 9.865\times10^5)\,(s^2 + 673.74s + 2.794\times10^5)$$

For even $N$ the DC gain equals the minimum of the ripple, $1/\sqrt{1+\varepsilon^2} = 0.8913$ ($-1$ dB), so

$$\boxed{H(s) = \frac{2.4565\times10^{11}}{(s^2 + 279.07s + 9.865\times10^5)(s^2 + 673.74s + 2.794\times10^5)}}$$

$$H(s) = \frac{2.4565\times10^{11}}{s^4 + 952.8s^3 + 1.4539\times10^6s^2 + 7.426\times10^8s + 2.7563\times10^{11}}$$

*Check.* $|H(j0)| = 0.8913$ ($-1$ dB), $|H(j1000)| = -1.00$ dB (the passband edge) and $|H(j1400)| = -18.31$ dB, which is greater than $18$ dB, so the specification is met by $N=4$ ($N=3$ would give only about 11 dB at $\omega_s$).

```figure caption="4th-order Chebyshev low-pass (1 dB ripple, wp = 1000 rad/s): poles on an ellipse in the s-plane and the magnitude response in dB, meeting -1 dB at wp and more than 18 dB at ws = 1400 rad/s."
import numpy as np, matplotlib.pyplot as plt
P=np.array([-139.536+983.379j,-336.870+407.329j,-336.870-407.329j,-139.536-983.379j])
den=np.real(np.poly(P)); K=245653341045.0
w=np.linspace(0,2500,800); H=20*np.log10(K/abs(np.polyval(den,1j*w)))
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.6,2.7),gridspec_kw={'width_ratios':[1,1.5]})
t=np.linspace(0,2*np.pi,200); a1.plot(364.6*np.cos(t),1064.4*np.sin(t),color='#bbb',lw=.8,ls='--')
a1.plot(P.real,P.imag,'x',color=SERIES[1],ms=8,mew=1.8); a1.axhline(0,color='#888',lw=.6); a1.axvline(0,color='#888',lw=.6)
a1.set_xlim(-600,300); a1.set_ylim(-1300,1300); a1.set_xlabel("$\\sigma$ (rad/s)",fontsize=8); a1.set_ylabel("$j\\omega$",fontsize=8); a1.set_title("poles",fontsize=8)
a2.plot(w,H,color=ACCENT); a2.axhline(-1,color='#bbb',lw=.7,ls=':'); a2.axhline(-18,color='#bbb',lw=.7,ls=':')
a2.plot([1000,1400],[-1,-18.31],'o',color=SERIES[1],ms=4); a2.text(1010,-5,"-1 dB",fontsize=7); a2.text(1420,-22,"-18.3 dB",fontsize=7)
a2.set_ylim(-45,3); a2.set_xlabel("$\\omega$ (rad/s)",fontsize=8); a2.set_ylabel("dB",fontsize=8); a2.set_title("magnitude response",fontsize=8); a2.grid(True)
```

@s 5
**Frequency transformation.** A frequency transformation is a mathematical substitution $s\to f(s)$ (a rational reactance function of the frequency variable) that converts a **normalised low-pass prototype** $H_{LP}(s)$ (cut-off 1 rad/s) into a low-pass, high-pass, band-pass or band-stop filter with the required cut-off frequencies.

| Required filter | Substitution | Element change |
|---|---|---|
| LP to LP (cut-off $\omega_c$) | $s\to s/\omega_c$ | $L\to L/\omega_c$, $C\to C/\omega_c$ |
| LP to HP (cut-off $\omega_c$) | $s\to\omega_c/s$ | $L\to$ capacitor $1/(\omega_cL)$, $C\to$ inductor $1/(\omega_cC)$ |
| LP to BP ($\omega_0=\sqrt{\omega_1\omega_2}$, $B = \omega_2-\omega_1$) | $s\to\dfrac{s^2+\omega_0^2}{Bs}$ | each $L$ becomes a series LC, each $C$ a parallel LC |
| LP to BS | $s\to\dfrac{Bs}{s^2+\omega_0^2}$ | each $L$ becomes a parallel LC, each $C$ a series LC |

*Importance in filter design:*

1. Only **one** prototype (a normalised LP, for which tables, poles and element values are available) must be designed; all the other types follow by transformation.
2. The specification of any filter is first converted to an equivalent LP specification, so the same order formulae and tables are used for HP, BP and BS.
3. It shifts the cut-off to the desired frequency and impedance level in one step (together with denormalization).
4. It saves design effort and gives consistent, accurate results; it is also used in the digital domain (the Constantinides transformations).

@s 6
**Fourth-order Butterworth HPF (cut-off 1 rad/s, terminations $1\,\Omega$).**

*Step 1: LP prototype.* From Table 2 for $n = 4$ (doubly terminated, $1\,\Omega$, $\omega_c = 1$ rad/s): shunt $C_1 = 0.7654$ F, series $L_2 = 1.848$ H, shunt $C_3 = 1.848$ F, series $L_4 = 0.7654$ H. (The same values follow from the Butterworth poles, $2\sin\frac{(2k-1)\pi}{2n}$ for $k = 1\dots4$: $0.7654,\ 1.848,\ 1.848,\ 0.7654$.)

*Step 2: LP to HP transformation* $s\to1/s$: each inductor $L$ becomes a capacitor $C = 1/L$ and each capacitor $C$ becomes an inductor $L = 1/C$. A series element stays in series and a shunt element stays in shunt, and the terminations stay $1\,\Omega$:

| LP element | HP element |
|---|---|
| shunt $C_1 = 0.7654$ F | shunt $L_1 = 1/0.7654 = 1.3066$ H |
| series $L_2 = 1.848$ H | series $C_2 = 1/1.848 = 0.5412$ F |
| shunt $C_3 = 1.848$ F | shunt $L_3 = 1/1.848 = 0.5412$ H |
| series $L_4 = 0.7654$ H | series $C_4 = 1/0.7654 = 1.3066$ F |

```figure caption="4th-order Butterworth high-pass filter as a doubly terminated lossless ladder (1 ohm terminations, cut-off 1 rad/s): shunt L1 = 1.3066 H, series C2 = 0.5412 F, shunt L3 = 0.5412 H, series C4 = 1.3066 F."
fig,ax=ckt_canvas(6.8,2.7,xlim=(-1.6,10.4),ylim=(-0.7,3.4))
vsrc(ax,(0,0),(0,2),"V$_s$",side=-1)
wire(ax,[(0,2),(0.5,2)]); res(ax,(0.5,2),(2.3,2),"1 Ω",side=1)
wire(ax,[(2.3,2),(3.1,2)]); node(ax,(3.1,2))
ind(ax,(3.1,2),(3.1,0),"L$_1$ = 1.3066 H",side=-1,off=0.5)
cap(ax,(3.1,2),(5.3,2),"C$_2$ = 0.5412 F",side=1); wire(ax,[(5.3,2),(5.9,2)]); node(ax,(5.9,2))
ind(ax,(5.9,2),(5.9,0),"L$_3$ = 0.5412 H",side=-1,off=0.5)
cap(ax,(5.9,2),(7.9,2),"C$_4$ = 1.3066 F",side=1); wire(ax,[(7.9,2),(8.8,2)]); node(ax,(8.8,2))
res(ax,(8.8,2),(8.8,0),"R$_L$ = 1 Ω",side=-1,off=0.9)
wire(ax,[(0,0),(8.8,0)])
```

*Step 3: check.* The voltage ratio of the doubly terminated network is $V_L/V_S = \tfrac12\,\dfrac{s^4}{(s^2+0.7654s+1)(s^2+1.8478s+1)}$, so $2|V_L/V_S| = \dfrac{\omega^4}{\sqrt{1+\omega^8}}$, which is $-3.01$ dB at $\omega = 1$ rad/s, $-24.1$ dB at $\omega = 0.5$ and almost $0$ dB above $\omega = 2$. It is the high-pass response (checked by computing the ABCD matrix of the ladder: $0.0624$, $0.7071$, $0.9980$ at $\omega = 0.5, 1, 2$).

*Step 4: denormalization* to a cut-off $\omega_c$ and load $R$: $L = \dfrac{R}{\omega_c}L_n$ and $C = \dfrac{C_n}{R\,\omega_c}$. For example, for $f_c = 10$ kHz ($\omega_c = 62\,832$ rad/s) and $R = 1\ \text{k}\Omega$: $L_1 = 20.8$ mH, $C_2 = 8.61$ nF, $L_3 = 8.61$ mH, $C_4 = 20.8$ nF, and both terminations $1\,\text{k}\Omega$.

@s 7
**Conditions for an LC (lossless) driving-point function** $Z(s)$:

1. $Z(s)$ is the **ratio of an even polynomial to an odd polynomial** (or odd to even), so $Z(-s) = -Z(s)$ (an odd function).
2. All the poles and zeros are **simple and lie on the $j\omega$ axis** (including the origin and infinity), occurring in conjugate pairs.
3. The poles and zeros **alternate** (interlace) along the $j\omega$ axis, and the residues at the poles are real and positive.
4. The degrees of the numerator and the denominator differ by exactly 1; there is a pole or zero at the origin and a pole or zero at infinity.

*Test of each function* (the critical frequencies in rad/s, $\sqrt3 = 1.732$, $\sqrt6 = 2.449$):

| Function | Poles | Zeros | Verdict |
|---|---|---|---|
| $Z_1$ | $1.732,\ 3$ (and $\infty$) | $0,\ 2,\ 2.449$ | Zeros $2$ and $2.449$ are adjacent: they do not alternate. **Not LC** |
| $Z_2$ | $0,\ 2,\ 3$ | $1.732,\ 2.449$ (and $\infty$) | Order $0_p, 1.732_z, 2_p, 2.449_z, 3_p, \infty_z$ alternates. Odd function, degrees $4/5$. **LC** |
| $Z_3$ | $0,\ 1.732,\ 3$ | $2,\ 2.449$ | Poles $0$ and $1.732$ are adjacent: **Not LC** |
| $Z_4$ | $2,\ 3$ | $1.732,\ 2.449$ | Even over even: not odd, no pole/zero at $0$ or $\infty$ pairing. **Not LC** |

Hence **only (b) $Z_2(s)$ is a valid LC lossless function.**

$$Z_2(s) = \frac{(s^2+3)(s^2+6)}{s(s^2+4)(s^2+9)}$$

**Foster-I form** (series connection of the partial-fraction terms of $Z$). Since the degree of the numerator is less than that of the denominator, there is no $k_\infty s$ term:

$$Z_2(s) = \frac{k_0}{s} + \frac{k_1 s}{s^2+4} + \frac{k_2 s}{s^2+9}$$

$$\begin{aligned}k_0 &= \left.sZ\right|_{s=0} = \frac{3\cdot6}{4\cdot9} = \frac12\\ k_1 &= \left.\frac{(s^2+3)(s^2+6)}{s^2(s^2+9)}\right|_{s^2=-4} = \frac{(-1)(2)}{(-4)(5)} = \frac{1}{10}\\ k_2 &= \left.\frac{(s^2+3)(s^2+6)}{s^2(s^2+4)}\right|_{s^2=-9} = \frac{(-6)(-3)}{(-9)(-5)} = \frac{2}{5}\end{aligned}$$

Check: $k_0 + k_1 + k_2 = 0.5 + 0.1 + 0.4 = 1$ (the coefficient of $1/s$ as $s\to\infty$) ✓.

$$Z_2(s) = \frac{1}{2s} + \frac{0.1\,s}{s^2+4} + \frac{0.4\,s}{s^2+9}$$

- $\dfrac{1}{2s}$ is a capacitor $C_0 = 1/k_0 = 2$ F.
- $\dfrac{k_1s}{s^2+4}$ is a parallel LC: $C_1 = 1/k_1 = 10$ F, $L_1 = \dfrac{k_1}{4} = 0.025$ H (as $\omega_1^2 = 1/L_1C_1 = 4$).
- $\dfrac{k_2s}{s^2+9}$ is a parallel LC: $C_2 = 1/k_2 = 2.5$ F, $L_2 = \dfrac{k_2}{9} = 0.0444$ H.

**Cauer-I form** (continued-fraction expansion that removes the pole at infinity first). $Z_2$ has a zero at infinity, so expand the admittance:

$$Y = \frac{1}{Z_2} = \frac{s^5 + 13s^3 + 36s}{s^4 + 9s^2 + 18}$$

$$\begin{aligned}Y &= s + \frac{4s^3 + 18s}{s^4+9s^2+18}\\ \frac{s^4+9s^2+18}{4s^3+18s} &= \frac{s}{4} + \frac{4.5s^2+18}{4s^3+18s}\\ \frac{4s^3+18s}{4.5s^2+18} &= \frac{8}{9}s + \frac{2s}{4.5s^2+18}\\ \frac{4.5s^2+18}{2s} &= 2.25s + \frac{9}{s}\end{aligned}$$

$$\boxed{Y = s + \cfrac{1}{\dfrac{s}{4} + \cfrac{1}{\dfrac{8}{9}s + \cfrac{1}{2.25s + \dfrac{1}{s/9}}}}}$$

So the ladder has a **shunt capacitor $C_1 = 1$ F**, a **series inductor $L_2 = 0.25$ H**, a **shunt capacitor $C_3 = 0.8889$ F**, and a last shunt branch made of a **series inductor $L_4 = 2.25$ H and capacitor $C_5 = 0.1111$ F**. (Verified by recombining the continued fraction: it equals $Y$ exactly.)

```figure caption="Foster-I realization (top: series C0 with two parallel LC tanks) and Cauer-I realization (bottom: shunt C1, series L2, shunt C3 and a final shunt series L4-C5 branch) of Z2(s)."
fig,ax=ckt_canvas(7.0,4.6,xlim=(-0.8,10.6),ylim=(-1.0,7.4))
# Foster I (top), y=5.2 main line
y=5.4
terminal(ax,(0,y)); wire(ax,[(0,y),(0.3,y)]); cap(ax,(0.3,y),(2.0,y),"2 F",side=1)
wire(ax,[(2.0,y),(2.6,y)])
# tank 1
wire(ax,[(2.6,y),(2.6,y+0.9),(3.0,y+0.9)]); ind(ax,(3.0,y+0.9),(4.4,y+0.9),"0.025 H",side=1,off=0.4); wire(ax,[(4.4,y+0.9),(4.8,y+0.9),(4.8,y)])
wire(ax,[(2.6,y),(2.6,y-0.9),(3.0,y-0.9)]); cap(ax,(3.0,y-0.9),(4.4,y-0.9),"10 F",side=-1,off=0.42); wire(ax,[(4.4,y-0.9),(4.8,y-0.9),(4.8,y)])
wire(ax,[(4.8,y),(5.4,y)]); node(ax,(2.6,y)); node(ax,(4.8,y)); node(ax,(5.4,y))
# tank 2
wire(ax,[(5.4,y),(5.4,y+0.9),(5.8,y+0.9)]); ind(ax,(5.8,y+0.9),(7.2,y+0.9),"0.0444 H",side=1,off=0.4); wire(ax,[(7.2,y+0.9),(7.6,y+0.9),(7.6,y)])
wire(ax,[(5.4,y),(5.4,y-0.9),(5.8,y-0.9)]); cap(ax,(5.8,y-0.9),(7.2,y-0.9),"2.5 F",side=-1,off=0.42); wire(ax,[(7.2,y-0.9),(7.6,y-0.9),(7.6,y)])
wire(ax,[(7.6,y),(8.2,y)]); terminal(ax,(8.2,y)); node(ax,(7.6,y))
label(ax,(4.1,7.1),"Foster-I",size=9)
# Cauer I (bottom)
y2=2.0
terminal(ax,(0,y2)); terminal(ax,(0,0)); wire(ax,[(0,y2),(1.2,y2)]); wire(ax,[(0,0),(8.2,0)])
cap(ax,(1.2,y2),(1.2,0),"C$_1$ = 1 F",side=-1,off=0.9); node(ax,(1.2,y2))
ind(ax,(1.2,y2),(3.6,y2),"L$_2$ = 0.25 H",side=1,off=0.45); wire(ax,[(3.6,y2),(4.3,y2)]); node(ax,(4.3,y2))
cap(ax,(4.3,y2),(4.3,0),"C$_3$ = 0.889 F",side=-1,off=1.1)
wire(ax,[(4.3,y2),(7.2,y2)]); node(ax,(7.2,y2))
ind(ax,(7.2,y2),(7.2,1.05),"L$_4$ = 2.25 H",side=1,off=0.95); cap(ax,(7.2,1.05),(7.2,0),"C$_5$ = 0.111 F",side=1,off=1.2)
label(ax,(4.1,3.4),"Cauer-I",size=9)
```

@s 8
**Tow-Thomas biquad.** It is a three-op-amp active-RC filter: a lossy (damped) integrator A1, an ideal integrator A2 and a unity-gain inverter A3, connected in a loop. The low-pass output is taken at A2.

```figure caption="Tow-Thomas biquad: A1 is the lossy integrator (R1, C1 in parallel with RQ), A2 the integrator (R2, C2), A3 a unity-gain inverter (R3 = R4) whose output is fed back through R to A1. The low-pass output is VLP at the output of A2."
fig,ax=ckt_canvas(7.4,3.5,xlim=(-2.4,17.2),ylim=(-1.4,6.0))
A1=opamp(ax,2.0,3.0,w=2.4,h=1.2,text="A1")
A2=opamp(ax,8.0,3.0,w=2.4,h=1.2,text="A2")
A3=opamp(ax,13.4,3.0,w=2.4,h=1.2,text="A3")
# input
terminal(ax,(-2.0,3.3)); label(ax,(-2.0,3.75),"V$_{in}$",size=8)
wire(ax,[(-2.0,3.3),(-1.4,3.3)]); res(ax,(-1.4,3.3),(0.2,3.3),"R$_1$",side=1,off=0.45); wire(ax,[(0.2,3.3),(2.0,3.3)])
node(ax,(1.5,3.3))
# A1 feedback: RQ and C1
wire(ax,[(1.5,3.3),(1.5,4.3),(2.5,4.3)]); res(ax,(2.5,4.3),(4.0,4.3),"R$_Q$",side=1,off=0.4); wire(ax,[(4.0,4.3),(4.9,4.3),(4.9,3.0),(4.4,3.0)])
wire(ax,[(1.5,4.3),(1.5,5.2),(2.5,5.2)]); cap(ax,(2.5,5.2),(4.0,5.2),"C$_1$",side=1,off=0.5); wire(ax,[(4.0,5.2),(4.9,5.2),(4.9,4.3)])
node(ax,(4.9,3.0)); node(ax,(4.9,4.3))
# A1 non-inverting to ground
wire(ax,[(2.0,2.7),(1.4,2.7),(1.4,2.3)]); gnd(ax,(1.4,2.3))
# R2 to A2
wire(ax,[(4.9,3.0),(5.2,3.0)]); res(ax,(5.2,3.0),(6.8,3.0),"R$_2$",side=-1,off=0.45); wire(ax,[(6.8,3.0),(7.0,3.0),(7.0,3.3),(8.0,3.3)])
node(ax,(7.4,3.3)); wire(ax,[(7.4,3.3),(7.4,5.2),(8.0,5.2)]); cap(ax,(8.0,5.2),(9.8,5.2),"C$_2$",side=1,off=0.5); wire(ax,[(9.8,5.2),(10.9,5.2),(10.9,3.0),(10.4,3.0)])
wire(ax,[(8.0,2.7),(7.4,2.7),(7.4,2.3)]); gnd(ax,(7.4,2.3)); node(ax,(10.9,3.0))
# output V_LP
wire(ax,[(10.9,3.0),(10.9,2.1)]); terminal(ax,(10.9,2.1)); label(ax,(10.9,1.6),"V$_{LP}$",size=8)
# A3 inverter
wire(ax,[(10.9,3.0),(11.5,3.0),(11.5,3.3)]); res(ax,(11.5,3.3),(12.7,3.3),"R$_3$",side=1,off=0.4); wire(ax,[(12.7,3.3),(13.4,3.3)]); node(ax,(13.0,3.3))
wire(ax,[(13.0,3.3),(13.0,4.5),(13.7,4.5)]); res(ax,(13.7,4.5),(15.0,4.5),"R$_4$",side=1,off=0.4); wire(ax,[(15.0,4.5),(16.2,4.5),(16.2,3.0),(15.8,3.0)])
wire(ax,[(13.4,2.7),(12.8,2.7),(12.8,2.3)]); gnd(ax,(12.8,2.3)); node(ax,(16.2,3.0))
# feedback via R to A1
wire(ax,[(16.2,3.0),(16.2,-0.6),(12.6,-0.6)]); res(ax,(12.6,-0.6),(10.6,-0.6),"R",side=1,off=0.45); wire(ax,[(10.6,-0.6),(0.6,-0.6),(0.6,3.3)]); node(ax,(0.6,3.3))
```

**Derivation.** Let the resistors of the inverter be equal ($R_3 = R_4$) so that $V_3 = -V_{LP}$. Let the feedback resistor to A1 be $R$, the integrator resistor $R_2$, and let $Z_f = \dfrac{R_Q}{1+sC_1R_Q}$ be the feedback impedance of A1 (the parallel $R_Q C_1$).

*Stage A1* (summing, lossy integrator, inverting): $V_1 = -Z_f\left(\dfrac{V_{in}}{R_1} + \dfrac{V_3}{R}\right) = -Z_f\left(\dfrac{V_{in}}{R_1} - \dfrac{V_{LP}}{R}\right)$.

*Stage A2* (integrator, inverting): $V_{LP} = -\dfrac{V_1}{sR_2C_2}\ \Rightarrow\ V_1 = -sR_2C_2V_{LP}$.

Equating,

$$sR_2C_2V_{LP} = Z_f\left(\frac{V_{in}}{R_1} - \frac{V_{LP}}{R}\right)\ \Rightarrow\ V_{LP}\left[sR_2C_2(1+sC_1R_Q) + \frac{R_Q}{R}\right] = \frac{R_Q}{R_1}V_{in}$$

Dividing by $R_2C_1C_2R_Q$:

$$\boxed{H_{LP}(s) = \frac{V_{LP}}{V_{in}} = \frac{\dfrac{1}{R_1R_2C_1C_2}}{s^2 + \dfrac{1}{R_QC_1}\,s + \dfrac{1}{RR_2C_1C_2}}}$$

This is the standard biquad $\dfrac{H_0\omega_0^2}{s^2 + (\omega_0/Q)s + \omega_0^2}$ with

$$\begin{gathered}\omega_0 = \frac{1}{\sqrt{RR_2C_1C_2}} \\ Q = \omega_0R_QC_1 = R_Q\sqrt{\frac{C_1}{RR_2C_2}} \\ H_0 = \frac{R}{R_1}\end{gathered}$$

(The output of A3, $-V_{LP}$, is the inverted low-pass, and the output of A1 is a band-pass.)

**Design.** The poles are at $-450\pm j893.03$, so

$$\begin{gathered}\omega_0^2 = 450^2 + 893.03^2 \approx 10^6\ \Rightarrow\ \omega_0 = 1000\ \text{rad/s} \\ \frac{\omega_0}{Q} = 2(450) = 900\ \Rightarrow\ Q = 1.111\end{gathered}$$

The required transfer function is $H(s) = \dfrac{1.3\times10^6}{s^2 + 900s + 10^6}$, with DC gain $H_0 = 1.3$.

Choose equal capacitors and resistors in the loop, $C_1 = C_2 = C$ and $R = R_2$, so $\omega_0 = 1/RC$ and $Q = R_Q/R$:

- Take $C = 0.1\ \mu\text{F}$ (a standard value). Then $R = R_2 = \dfrac{1}{\omega_0C} = \dfrac{1}{1000\times0.1\times10^{-6}} = 10\ \text{k}\Omega$.
- $R_Q = QR = 1.111\times10\ \text{k}\Omega = 11.1\ \text{k}\Omega$ (use $11\ \text{k}\Omega$ with $Q=1.1$, or $11.1\ \text{k}\Omega$ from the E96 series).
- $H_0 = R/R_1 = 1.3\ \Rightarrow\ R_1 = \dfrac{10\ \text{k}\Omega}{1.3} = 7.69\ \text{k}\Omega$ (E96 value $7.68\ \text{k}\Omega$).
- Inverter: $R_3 = R_4 = 10\ \text{k}\Omega$.

$$\boxed{C_1 = C_2 = 0.1\ \mu\text{F},\quad R = R_2 = R_3 = R_4 = 10\ \text{k}\Omega,\quad R_Q = 11.1\ \text{k}\Omega,\quad R_1 = 7.68\ \text{k}\Omega}$$

All the values lie in the range $1\ \text{k}\Omega$ to $100\ \text{k}\Omega$ and $0.1\ \mu$F, which are standard and practically realisable (low enough for the op-amp loading, high enough to avoid large currents; 1% resistors and 5% capacitors, or a trimmer on $R_Q$ to set $Q$ exactly). For an ECG amplifier with $f_0 = \omega_0/2\pi = 159$ Hz, the op-amps need only a modest bandwidth.

@s 9
**Sallen-Key low-pass filter.** The non-inverting amplifier of gain $K = 1 + R_f/R_g$ buffers the second node. With $R_1$, $R_2$ in series from the input, $C_1$ from the junction of $R_1$ and $R_2$ to the output (feedback capacitor) and $C_2$ from the non-inverting input to ground:

```figure caption="Sallen-Key low-pass filter with input-divider gain compensation: Ra and Rb replace R1 so that the divider has a gain of 1/K and a Thevenin resistance R. The overall pass-band gain becomes unity while w0 and Q are unchanged."
fig,ax=ckt_canvas(7.2,3.6,xlim=(-2.4,11.6),ylim=(-0.6,5.8))
terminal(ax,(-2.0,3.0)); label(ax,(-2.0,3.5),"V$_{in}$",size=8)
wire(ax,[(-2.0,3.0),(-1.6,3.0)]); res(ax,(-1.6,3.0),(0.4,3.0),"R$_a$ = KR",side=1,off=0.45)
wire(ax,[(0.4,3.0),(3.2,3.0)]); node(ax,(1.0,3.0))
res(ax,(1.0,3.0),(1.0,0.8),"R$_b$",side=-1,off=0.5); gnd(ax,(1.0,0.8)); node(ax,(3.2,3.0))
res(ax,(3.2,3.0),(5.2,3.0),"R$_2$ = R",side=1,off=0.45); wire(ax,[(5.2,3.0),(5.8,3.0)]); node(ax,(5.8,3.0))
cap(ax,(5.8,3.0),(5.8,0.8),"C$_2$",side=-1,off=0.5); gnd(ax,(5.8,0.8))
wire(ax,[(5.8,3.0),(5.8,2.7),(6.8,2.7)])
wire(ax,[(3.2,3.0),(3.2,5.0),(3.8,5.0)]); cap(ax,(3.8,5.0),(5.6,5.0),"C$_1$",side=1,off=0.5); wire(ax,[(5.6,5.0),(9.8,5.0),(9.8,3.0)])
op=opamp(ax,6.8,3.0,w=2.4,h=1.2,text="K")
wire(ax,[(9.2,3.0),(10.6,3.0)]); node(ax,(9.8,3.0)); terminal(ax,(10.6,3.0)); label(ax,(10.6,3.5),"V$_o$",size=8)
wire(ax,[(6.8,3.3),(6.2,3.3),(6.2,1.8)]); node(ax,(6.2,1.8)); res(ax,(6.2,1.8),(8.4,1.8),"R$_f$",side=1,off=0.4); wire(ax,[(8.4,1.8),(9.8,1.8),(9.8,3.0)])
res(ax,(6.2,1.8),(6.2,0.2),"R$_g$",side=-1,off=0.45); gnd(ax,(6.2,0.2))
```

**Transfer function (derivation).** Let $V_A$ be the voltage at the junction of $R_1$, $R_2$ and $C_1$, and $V_B$ the voltage at the non-inverting input, so $V_o = KV_B$. KCL at node B and at node A (ideal op-amp, no input current):

$$\begin{gathered}\frac{V_A - V_B}{R_2} = sC_2V_B \\ V_B = \frac{V_o}{K}\ \Rightarrow\ V_A = V_B(1+sR_2C_2) = \frac{V_o}{K}(1+sR_2C_2)\end{gathered}$$

$$\frac{V_{in} - V_A}{R_1} = \frac{V_A - V_B}{R_2} + sC_1(V_A - V_o)$$

Substituting $V_A$ and $V_B$ and simplifying gives

$$\boxed{H(s) = \frac{V_o}{V_{in}} = \frac{K}{s^2R_1R_2C_1C_2 + s\left[R_1C_2 + R_2C_2 + R_1C_1(1-K)\right] + 1}}$$

For the equal-component design $R_1 = R_2 = R$ and $C_1 = C_2 = C$:

$$\begin{gathered}H(s) = \frac{K\omega_0^2}{s^2 + (3-K)\omega_0\,s + \omega_0^2} \\ \omega_0 = \frac{1}{RC},\quad Q = \frac{1}{3-K},\quad K = 1 + \frac{R_f}{R_g} = 3 - \frac1Q\end{gathered}$$

**The problem of excess gain.** To obtain a given $Q$ (for example $Q = 1.5$) the equal-component circuit needs $K = 3 - 1/Q = 2.33$. Then the pass-band (DC) gain is $K>1$, which is excess: the amplifier gain is fixed by $Q$, so the pass-band gain cannot be chosen freely, which may overload the following stages and (since $Q = 1/(3-K)$) $Q$ becomes extremely sensitive to $K$: $S_K^Q = \dfrac{K}{3-K} = 3Q-1$, so for a high $Q$ even a small error in $K$ (as the op-amp gain is finite) gives a large change in $Q$, and instability if $K\to3$.

**Compensation of the excess gain.** The gain $K$ is reduced to unity by attenuating the input by exactly $1/K$, without changing the poles ($\omega_0$ and $Q$). Replace the input resistor $R_1 = R$ by a **resistive divider** $R_a$, $R_b$ (see the figure), which is equal to its **Thevenin equivalent** $V_{th} = V_{in}/K$ in series with $R_{th} = R_a\parallel R_b = R$:

$$\begin{gathered}\frac{R_b}{R_a+R_b} = \frac1K \\ \frac{R_aR_b}{R_a+R_b} = R\end{gathered}$$

Solving these two equations:

$$\boxed{R_a = KR,\qquad R_b = \frac{KR}{K-1}}$$

Check: $R_a\parallel R_b = \dfrac{KR\cdot KR/(K-1)}{KR + KR/(K-1)} = \dfrac{KR/(K-1)}{K/(K-1)} = R$ ✓ and $\dfrac{R_b}{R_a+R_b} = \dfrac{1/(K-1)}{1 + 1/(K-1)} = \dfrac1K$ ✓.

The filter now sees a source $V_{in}/K$ through a resistance $R$, exactly like the original circuit, so

$$H_{comp}(s) = \frac{1}{K}\cdot\frac{K\omega_0^2}{s^2 + (3-K)\omega_0s+\omega_0^2} = \frac{\omega_0^2}{s^2 + (\omega_0/Q)s + \omega_0^2}$$

which has **unity DC gain** and the same $\omega_0 = 1/RC$ and $Q = 1/(3-K)$.

*Example:* $Q = 1.5$, $R = 10\ \text{k}\Omega$: $K = 3 - 1/1.5 = 2.333$, $R_a = 23.3\ \text{k}\Omega$, $R_b = \dfrac{23.3}{1.333} = 17.5\ \text{k}\Omega$ (the divider has $R_a\parallel R_b = 10\ \text{k}\Omega$ and ratio $1/2.333$), and $R_f/R_g = 1.333$.

*Other ways:* (i) use unity gain ($K = 1$, a voltage follower) with **unequal** components: for $R_1 = R_2 = R$ the denominator becomes $s^2R^2C_1C_2 + 2sRC_2 + 1$, so $\omega_0 = \dfrac{1}{R\sqrt{C_1C_2}}$ and $Q = \dfrac12\sqrt{\dfrac{C_1}{C_2}}$. The gain is then exactly 1 and $Q$ is set by the capacitor ratio (this needs $C_1 = 4Q^2C_2$); (ii) follow the filter by an attenuator, or by an inverting stage of gain smaller than 1.

@s 10
**Sensitivity.** The sensitivity of a quantity $y$ to a component $x$ is $S_x^y = \dfrac{x}{y}\dfrac{\partial y}{\partial x} = \dfrac{\partial\ln y}{\partial\ln x}$.

For the Tow-Thomas low-pass (derived in the previous question):

$$\begin{gathered}Q = R_Q\sqrt{\frac{C_1}{R\,R_2\,C_2}} = R_Q\,C_1^{1/2}\,C_2^{-1/2}\,R^{-1/2}\,R_2^{-1/2} \\ \omega_0 = (RR_2C_1C_2)^{-1/2}\end{gathered}$$

Because $Q$ is a product of powers of the components, each sensitivity is the exponent of that component:

| Component | $S^Q_x$ | $S^{\omega_0}_x$ |
|---|---|---|
| $R_Q$ | $+1$ | $0$ |
| $C_1$ | $+\tfrac12$ | $-\tfrac12$ |
| $C_2$ | $-\tfrac12$ | $-\tfrac12$ |
| $R$ | $-\tfrac12$ | $-\tfrac12$ |
| $R_2$ | $-\tfrac12$ | $-\tfrac12$ |
| $R_1$ (input) | $0$ | $0$ |

$$\boxed{S^Q_{R_Q} = 1,\quad S^Q_{C_1} = \tfrac12,\quad S^Q_{C_2} = S^Q_{R} = S^Q_{R_2} = -\tfrac12,\quad S^Q_{R_1} = 0}$$

Also, the gain sensitivity is $S^{H_0}_{R} = 1$, $S^{H_0}_{R_1} = -1$.

*Conclusions:* all the sensitivities have magnitudes of at most 1, and they are **independent of $Q$**, so the Tow-Thomas circuit is a low-sensitivity filter that can realise high-$Q$ poles reliably (unlike the single-amplifier Sallen-Key circuit, whose $S_K^Q = 3Q-1$ grows with $Q$). $Q$ can be tuned independently through $R_Q$ alone without disturbing $\omega_0$ and with the gain set by $R_1$. For example, with $\pm1\%$ resistors and capacitors the worst-case change of $Q$ is less than about $\pm3\%$ ($1+0.5\times4$ units of 1%, in the worst case).

@s 11
**Current-mode filters: significance.** In a current-mode filter the information is carried by currents rather than voltages, and the active elements are current conveyors, current mirrors, OTAs and so on, not voltage op-amps. Their significance:

1. **Wide bandwidth** and high-frequency operation (MHz to GHz): there is no constant gain-bandwidth limit, because the nodes have low impedance and small voltage swings.
2. **High slew rate** and wide dynamic range, even with a low supply voltage (suited to low-voltage low-power CMOS and portable systems).
3. **Simple circuits:** summation of currents is done by joining wires (KCL) with no resistors, and the gain is set by current ratios (for example, accurate transistor matching).
4. **Large linearity and small chip area,** and easily integrated with floating or grounded capacitors; convenient for tunable and programmable filters.
5. Better performance for **video, RF and wireless** signal processing, and for multi-input multi-output filters.

**Current conveyor.** A current conveyor is a three-terminal (X, Y, Z) building block. The X terminal is a low-impedance current input/output port, Y is a high-impedance voltage input, and Z is the high-impedance current output.

```figure caption="Block diagram of a current conveyor: terminal Y (voltage input), terminal X (low-impedance input/output) and terminal Z (current output). CCI has current iy = ix at Y, CCII has no current into Y."
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(5.8,2.3)); ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,4.4)
def arr(p,q): ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="->",color=INK,lw=1))
for x0,name,sub in [(0.5,"CCI","$i_y = i_x,\\ v_x = v_y,\\ i_z = \\pm i_x$"),(6.6,"CCII","$i_y = 0,\\ v_x = v_y,\\ i_z = \\pm i_x$")]:
    ax.add_patch(plt.Rectangle((x0+1.3,1.2),2.0,2.0,fc='#eaf1ff',ec=INK,lw=1.2)); ax.text(x0+2.3,2.2,name,ha='center',va='center',fontsize=9,weight='bold')
    ax.plot([x0,x0+1.3],[2.8,2.8],color=INK,lw=1); ax.text(x0+0.1,3.05,"Y",fontsize=8); arr((x0,2.8),(x0+0.55,2.8))
    ax.plot([x0,x0+1.3],[1.6,1.6],color=INK,lw=1); ax.text(x0+0.1,1.15,"X",fontsize=8)
    ax.plot([x0+3.3,x0+4.5],[2.2,2.2],color=INK,lw=1); ax.text(x0+4.2,2.45,"Z",fontsize=8); arr((x0+3.3,2.2),(x0+4.0,2.2))
    ax.text(x0+2.2,0.55,sub,ha='center',fontsize=7.2)
```

*Characteristic (port) equations*

$$\begin{bmatrix}i_y\\v_x\\i_z\end{bmatrix} = \begin{bmatrix}0&1&0\\1&0&0\\0&\pm1&0\end{bmatrix}\begin{bmatrix}v_y\\i_x\\v_z\end{bmatrix}\ \ (\text{CCI}),\qquad\begin{bmatrix}i_y\\v_x\\i_z\end{bmatrix} = \begin{bmatrix}0&0&0\\1&0&0\\0&\pm1&0\end{bmatrix}\begin{bmatrix}v_y\\i_x\\v_z\end{bmatrix}\ \ (\text{CCII})$$

- **First-generation conveyor (CCI, Sedra and Smith, 1968):** $i_y = i_x$, $v_x = v_y$, $i_z = \pm i_x$. The current flowing into X is also forced to flow into Y (the voltage at X follows Y, and Y is also a low-impedance port), and the current is copied to Z with the sign $+$ (CCI+) or $-$ (CCI$-$). So both X and Y are low-impedance, and so Y behaves like a current terminal: the conveyor can measure an unknown impedance.
- **Second-generation conveyor (CCII, 1970):** $i_y = 0$, $v_x = v_y$, $i_z = \pm i_x$. Y has an infinite input impedance (no current flows into it), X follows the voltage of Y ($v_x = v_y$, X acts as a voltage buffer with a low output resistance) and the current in X is conveyed to the high-impedance output Z, in the same direction for CCII+ and in the opposite one for CCII$-$. The CCII is the most useful and popular, being the basis of the current-mode filters, integrators, immittance converters and instrumentation circuits.

In summary: the **CCI** has $i_y = i_x$ (current at Y is the same as at X), while the **CCII** has $i_y = 0$; in both $v_x = v_y$ and $i_z = \pm i_x$.
