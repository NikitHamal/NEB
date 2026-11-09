---
file: NEBians-IOE-Past-Paper-Signals-and-Systems-ENEX255-2082-Bhadra.pdf
subject: Signals and Systems
level: BE · Year II / Part II
code: ENEX 255
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Briefly explain discrete time unit impulse, unit step and unit ramp signal. What is the relationship between unit impulse, unit step and unit ramp signal? [[3+2]]

b) Calculate the energy and power of the signal $x(t) = 2e^{-5t}u(t-1)$. [[4]]

@q 2
a) Derive the Fourier series expansion of a continuous time periodic signal $x(t)$. [[4]]

b) Consider a signal $x[n] = \sin(\omega_0 n)$ with period $N = 6$. Find the Fourier series coefficient of the given signal $x[n]$. Plot spectra and find the average power. [[4+4]]

@q 3
a) Derive the Fourier transform for discrete-time aperiodic signal. Also show that DTFT periodic with period $2\pi$. [[5+3]]

b) State and prove: Parseval's theorem for a DT aperiodic signal. [[3]]

@q 4
a) Explain the properties of discrete time Fourier transform. State and prove the convolution property of discrete time Fourier transform. [[3+3]]

b) Find the convolution between the signal $x(n) = \delta(n-2) - \delta(n-1) + 2\times\delta(n) + \delta(n+1) + \delta(n+2)$ and $h(n) = u[n] - u[n-1]$. [[4]]

@q 5
a) Derive the convolution integral formula for the continuous time signal. [[4]]

b) A discrete time LTI system is defined by the impulse response $h[n] = \{-2, -1, 0, 1, 2\}$. If the input to the given system is $x[n] = \{1, -0.25, 0, -1, 0.5, -0.5\}$, find and plot the output of the system. [[5]]

@q 6
a) State and prove the sampling theorem. What is aliasing effect? Explain. [[3+2+3]]

b) Determine the Nyquist rate for the signal $x(t) = 5\cos(3{,}000\pi t)\sin(1{,}000\pi t)$. [[3]]

@q 7
Define frequency response of a LTI system. Derive the impulse response of an ideal low pass and high pass filter. [[2+6]]

<!-- SOLUTIONS -->

@s 1
**(a) Basic DT signals.**

{{FIG_basic}}

- **Unit impulse (unit sample)** $\delta[n] = 1$ for $n = 0$ and $0$ for $n \ne 0$. It is the DT identity of convolution, and the sifting property is $x[n]\delta[n - n_0] = x[n_0]\delta[n - n_0]$ and $\sum x[n]\delta[n - n_0] = x[n_0]$.
- **Unit step** $u[n] = 1$ for $n \ge 0$ and $0$ for $n < 0$. It switches a signal on at $n = 0$.
- **Unit ramp** $r[n] = n\,u[n] = n$ for $n \ge 0$ and $0$ for $n < 0$: a line of unit slope that starts at 0.

**Relationship.** The step is the running sum of the impulse, and the ramp is the running sum of the step (one sample delayed); conversely, the first difference undoes each sum:

$$u[n] = \sum_{k=-\infty}^{n}\delta[k],\qquad \delta[n] = u[n] - u[n-1],$$

$$r[n] = \sum_{k=-\infty}^{n-1}u[k] = \sum_{k=-\infty}^{n}u[k-1],\qquad u[n] = r[n+1] - r[n],$$

and hence $\delta[n] = r[n+1] - 2r[n] + r[n-1]$ (the second difference of the ramp). *Check:* $r[0] = 0$, $r[1] = 1$, $r[-1] = 0$ give $\delta[0] = 1 - 0 + 0 = 1$ and $\delta[1] = r[2] - 2r[1] + r[0] = 2 - 2 + 0 = 0$. (In continuous time the same relations hold with the integral and the derivative: $u(t) = \int\delta$, $r(t) = \int u$.)

**(b) Energy and power of $x(t) = 2e^{-5t}u(t-1)$.** The signal is zero for $t < 1$ and $2e^{-5t}$ for $t \ge 1$:

$$E = \int_{-\infty}^{\infty}\lvert x(t)\rvert^2dt = \int_1^\infty 4e^{-10t}dt = 4\left[\frac{e^{-10t}}{-10}\right]_1^\infty = \frac{4}{10}e^{-10} = 0.4\,e^{-10} = {{EB}}\ \text{J}.$$

The energy is finite and non-zero, so $x(t)$ is an **energy signal**, and its average power is

$$P = \lim_{T\to\infty}\frac{1}{2T}\int_{-T}^{T}\lvert x(t)\rvert^2dt = \lim_{T\to\infty}\frac{E_T}{2T} = 0.$$

(Result: $E = 0.4e^{-10} \approx 1.82\times10^{-5}$, $P = 0$.)

@s 2
**(a) Fourier series of a CT periodic signal.** A periodic signal $x(t)$ with period $T_0$ satisfying the Dirichlet conditions (absolutely integrable over a period, finite number of maxima, minima and discontinuities) can be written as a sum of harmonically related sinusoids, $\omega_0 = 2\pi/T_0$.

*Exponential form.* Assume $x(t) = \displaystyle\sum_{k=-\infty}^{\infty}c_k\,e^{jk\omega_0 t}$. Multiply both sides by $e^{-jm\omega_0 t}$ and integrate over one period:

$$\int_{T_0}x(t)e^{-jm\omega_0 t}dt = \sum_k c_k\int_{T_0}e^{j(k-m)\omega_0 t}dt .$$

The integral is $T_0$ for $k = m$ and $0$ for $k \ne m$ (orthogonality: $\int_{T_0}e^{jn\omega_0 t}dt = \left[\tfrac{e^{jn\omega_0 t}}{jn\omega_0}\right] = 0$ for $n \ne 0$). So

$$c_k = \frac{1}{T_0}\int_{T_0}x(t)\,e^{-jk\omega_0 t}\,dt,\qquad c_0 = \frac{1}{T_0}\int_{T_0}x(t)dt\ (\text{the average value}).$$

*Trigonometric form.* Combining $c_k$ and $c_{-k}$ ($= c_k^*$ for real $x$):

$$x(t) = a_0 + \sum_{k=1}^{\infty}\bigl[a_k\cos k\omega_0 t + b_k\sin k\omega_0 t\bigr],$$

$$a_0 = \frac{1}{T_0}\int_{T_0}x\,dt,\quad a_k = \frac{2}{T_0}\int_{T_0}x(t)\cos k\omega_0 t\,dt,\quad b_k = \frac{2}{T_0}\int_{T_0}x(t)\sin k\omega_0 t\,dt,$$

with $a_k = 2\,\mathrm{Re}\,c_k$, $b_k = -2\,\mathrm{Im}\,c_k$, and in compact form $x(t) = a_0 + \sum A_k\cos(k\omega_0 t + \theta_k)$, $A_k = 2\lvert c_k\rvert = \sqrt{a_k^2 + b_k^2}$. Parseval: the average power is $\dfrac{1}{T_0}\int\lvert x\rvert^2dt = \sum\lvert c_k\rvert^2$.

**(b) $x[n] = \sin(\omega_0 n)$ with $N = 6$.** The period is $N = 6$, so the fundamental frequency is $\omega_0 = 2\pi/N = \pi/3$ and $x[n] = \sin(\pi n/3)$, the first harmonic. Expand with Euler's formula,

$$x[n] = \frac{1}{2j}e^{j(2\pi/6)n} - \frac{1}{2j}e^{-j(2\pi/6)n},$$

and compare with $x[n] = \sum_{k=0}^{5}c_k e^{jk(2\pi/6)n}$. Therefore (using $c_{-1} = c_5$):

$$\begin{gathered} c_1 = \frac{1}{2j} = -\frac{j}{2} \\ c_{-1} = c_5 = -\frac{1}{2j} = +\frac{j}{2} \\ c_0 = c_2 = c_3 = c_4 = 0 \end{gathered}$$

Magnitude $\lvert c_{\pm1}\rvert = 0.5$ and phase $\angle c_1 = -90^\circ$, $\angle c_{-1} = +90^\circ$. (Check with the formula $c_k = \tfrac16\sum_{n=0}^{5}x[n]e^{-jk\pi n/3}$ with $x = \{0, 0.866, 0.866, 0, -0.866, -0.866\}$: $c_1 = -0.5j$, verified numerically.)

{{FIG_sinB}}

*Average power.* From the coefficients $P = \sum_{k=0}^{5}\lvert c_k\rvert^2 = 0.25 + 0.25 = \mathbf{0.5}$. In the time domain, $P = \tfrac16\sum\sin^2(\pi n/3) = \tfrac16(0 + 0.75 + 0.75 + 0 + 0.75 + 0.75) = 0.5$, the same.

@s 3
**(a) DTFT of an aperiodic signal.** Let $x[n]$ be zero outside $-N_1 \le n \le N_2$ and let $\tilde x[n]$ be its periodic extension of period $N > N_1 + N_2$. The DT Fourier series of $\tilde x$ is

$$\tilde x[n] = \sum_{k=\langle N\rangle}c_k\,e^{jk\Omega_0 n},\qquad c_k = \frac{1}{N}\sum_{n=\langle N\rangle}\tilde x[n]e^{-jk\Omega_0 n},\qquad \Omega_0 = \frac{2\pi}{N}.$$

In the summation interval $\tilde x[n] = x[n]$, and $x[n] = 0$ outside it, so $Nc_k = \displaystyle\sum_{n=-\infty}^{\infty}x[n]e^{-jk\Omega_0 n}$. Define

$$\boxed{X(\Omega) = \sum_{n=-\infty}^{\infty}x[n]\,e^{-j\Omega n}}\qquad\text{so that } c_k = \frac{1}{N}X(k\Omega_0).$$

Then $\tilde x[n] = \dfrac{1}{2\pi}\sum_{k=\langle N\rangle}X(k\Omega_0)e^{jk\Omega_0 n}\Omega_0$. When $N \to \infty$, $\Omega_0 \to d\Omega$, $k\Omega_0 \to \Omega$, and the sum over the $N$ terms (covering a $2\pi$ range) becomes an integral over $2\pi$:

$$\boxed{x[n] = \frac{1}{2\pi}\int_{2\pi}X(\Omega)\,e^{j\Omega n}\,d\Omega}\qquad\text{(inverse DTFT).}$$

$X(\Omega)$ exists if $\sum\lvert x[n]\rvert < \infty$.

*Periodicity of the DTFT.* Replace $\Omega$ by $\Omega + 2\pi$:

$$X(\Omega + 2\pi) = \sum x[n]e^{-j(\Omega + 2\pi)n} = \sum x[n]e^{-j\Omega n}\underbrace{e^{-j2\pi n}}_{=1\ (n\ \text{integer})} = X(\Omega).$$

So $X(\Omega)$ is periodic with period $2\pi$ (it is therefore specified by one period, $-\pi \le \Omega \le \pi$). This is because DT frequencies $\Omega$ and $\Omega + 2\pi$ give the same sequence $e^{j\Omega n}$. $\blacksquare$

**(b) Parseval's theorem for a DT aperiodic signal.** *Statement:* $E = \displaystyle\sum_{n=-\infty}^{\infty}\lvert x[n]\rvert^2 = \frac{1}{2\pi}\int_{2\pi}\lvert X(\Omega)\rvert^2d\Omega$.

*Proof.* $\sum x[n]x^*[n]$ with $x^*[n] = \dfrac{1}{2\pi}\displaystyle\int_{2\pi}X^*(\Omega)e^{-j\Omega n}d\Omega$:

$$E = \sum_n x[n]\frac{1}{2\pi}\int_{2\pi}X^*(\Omega)e^{-j\Omega n}d\Omega = \frac{1}{2\pi}\int_{2\pi}X^*(\Omega)\Bigl[\sum_n x[n]e^{-j\Omega n}\Bigr]d\Omega = \frac{1}{2\pi}\int_{2\pi}X^*(\Omega)X(\Omega)\,d\Omega,$$

which is $\dfrac{1}{2\pi}\displaystyle\int_{2\pi}\lvert X(\Omega)\rvert^2d\Omega$. $\blacksquare$ ($\lvert X(\Omega)\rvert^2$ is the energy spectral density.)

@s 4
**(a) Properties of the DTFT** ($x[n] \leftrightarrow X(\Omega)$, $y[n] \leftrightarrow Y(\Omega)$):

| Property | Time domain | Frequency domain |
|---|---|---|
| Periodicity | | $X(\Omega + 2\pi) = X(\Omega)$ |
| Linearity | $a x[n] + b y[n]$ | $aX(\Omega) + bY(\Omega)$ |
| Time shift | $x[n - n_0]$ | $e^{-j\Omega n_0}X(\Omega)$ |
| Frequency shift | $e^{j\Omega_0 n}x[n]$ | $X(\Omega - \Omega_0)$ |
| Time reversal | $x[-n]$ | $X(-\Omega)$ |
| Conjugation | $x^*[n]$ | $X^*(-\Omega)$ |
| Conjugate symmetry (real $x$) | | $X(-\Omega) = X^*(\Omega)$ |
| Differencing | $x[n] - x[n-1]$ | $(1 - e^{-j\Omega})X(\Omega)$ |
| Accumulation | $\sum_{k\le n}x[k]$ | $\dfrac{X(\Omega)}{1 - e^{-j\Omega}} + \pi X(0)\sum_k\delta(\Omega - 2\pi k)$ |
| Differentiation in frequency | $n\,x[n]$ | $j\dfrac{dX}{d\Omega}$ |
| Convolution | $x[n] * y[n]$ | $X(\Omega)\,Y(\Omega)$ |
| Multiplication | $x[n]\,y[n]$ | $\dfrac{1}{2\pi}\displaystyle\int_{2\pi}X(\theta)Y(\Omega - \theta)d\theta$ |
| Parseval | $\sum\lvert x[n]\rvert^2$ | $\dfrac{1}{2\pi}\displaystyle\int_{2\pi}\lvert X\rvert^2d\Omega$ |

**Convolution property.** *Statement:* if $y[n] = x[n] * h[n]$ then $Y(\Omega) = X(\Omega)H(\Omega)$.

*Proof.* $Y(\Omega) = \displaystyle\sum_n\Bigl[\sum_k x[k]h[n-k]\Bigr]e^{-j\Omega n}$. Interchange the sums: $= \displaystyle\sum_k x[k]\sum_n h[n-k]e^{-j\Omega n}$. Put $m = n - k$ in the inner sum, so $e^{-j\Omega n} = e^{-j\Omega m}e^{-j\Omega k}$:

$$Y(\Omega) = \sum_k x[k]e^{-j\Omega k}\sum_m h[m]e^{-j\Omega m} = X(\Omega)\,H(\Omega). \qquad\blacksquare$$

So convolution in time is multiplication in frequency, and $H(\Omega) = Y/X$ is the frequency response.

**(b) $x(n) * h(n)$.** Since $u[n] - u[n-1] = \delta[n]$ (the step minus its delayed copy is 1 only at $n = 0$), $h(n) = \delta(n)$, the identity of convolution, so

$$y(n) = x(n) * \delta(n) = x(n) = \delta(n-2) - \delta(n-1) + 2\delta(n) + \delta(n+1) + \delta(n+2).$$

*Direct check:* $y[n] = \sum_k x[k]h[n-k] = \sum_k x[k]\delta[n - k] = x[n]$. As a sequence (values for $n = -2, -1, 0, 1, 2$):

| $n$ | $-2$ | $-1$ | 0 | 1 | 2 |
|---|---|---|---|---|---|
| $y[n]$ | 1 | 1 | **2** | −1 | 1 |

(the term $\delta(n+2)$ has the coefficient 1 at $n = -2$; $\delta(n+1)$ gives 1 at $n = -1$; $2\delta(n)$ gives 2 at $n = 0$; $-\delta(n-1)$ gives $-1$ at $n = 1$; $\delta(n-2)$ gives 1 at $n = 2$). Sum check: $\sum y = 4 = (\sum x)(\sum h) = 4 \times 1$.

@s 5
**(a) Convolution integral.** Any CT signal is a continuum of weighted impulses (the sifting property):

$$x(t) = \int_{-\infty}^{\infty}x(\tau)\,\delta(t - \tau)\,d\tau.$$

Let $h(t)$ be the response of the LTI system to $\delta(t)$. By **time invariance** the response to $\delta(t - \tau)$ is $h(t - \tau)$; by **linearity** (scaling by $x(\tau)$ and superposition, an integral being a limit of a sum):

$$y(t) = \int_{-\infty}^{\infty}x(\tau)\,h(t - \tau)\,d\tau = x(t) * h(t).$$

*Steps in evaluating:* (1) change $t$ to $\tau$; (2) fold $h(\tau) \to h(-\tau)$; (3) shift by $t$, $h(t - \tau)$; (4) multiply by $x(\tau)$ and integrate (the limits change with the overlap); repeat for each range of $t$. *Properties:* commutative, associative, distributive; $x * \delta(t - t_0) = x(t - t_0)$; the $\mathcal{F}$ transform turns it into $Y(\omega) = X(\omega)H(\omega)$. For a causal system with a causal input the limits are $0$ to $t$. *Example:* $x = u(t)$ and $h = e^{-t}u(t)$ give $y(t) = \int_0^te^{-(t-\tau)}d\tau = 1 - e^{-t}$ for $t \ge 0$.

**(b) Output of the DT LTI system.** Take the first sample of each sequence at $n = 0$: $x[n] = \{1, -0.25, 0, -1, 0.5, -0.5\}$ (6 samples) and $h[n] = \{-2, -1, 0, 1, 2\}$ (5 samples), so $y[n] = \sum_k x[k]h[n-k]$ has $6 + 5 - 1 = 10$ samples ($n = 0, \dots, 9$). Each $x[k]$ multiplies $h$ and the row is shifted by $k$:

{{TAB_B}}

$$y[n] = \{{{Y_B}}\},\qquad n = 0, 1, \dots, 9.$$

For example $y[0] = 1(-2) = -2$; $y[1] = 1(-1) + (-0.25)(-2) = -0.5$; $y[4] = 1(2) + (-0.25)(1) + 0 + (-1)(-1) + 0.5(-2) = 1.75$; $y[9] = (-0.5)(2) = -1$. Check: $\sum y = (\sum x)(\sum h) = (-0.25)(0) = 0$ ✓. (The answer was computed with a program; the result also satisfies $y[0] = x[0]h[0]$ and $y[9] = x[5]h[4]$.)

{{FIG_convB}}

@s 6
**(a) Sampling theorem.** *Statement:* a signal $x(t)$ band-limited to $f_m$ (its spectrum $X(f) = 0$ for $\lvert f\rvert > f_m$) is **uniquely determined by its samples** $x(nT_s)$ taken at a rate $f_s = 1/T_s \ge 2f_m$. The minimum rate $f_N = 2f_m$ is the *Nyquist rate*.

*Proof.* Sampling is multiplication by an impulse train, $x_s(t) = x(t)\,p(t)$, $p(t) = \sum_n\delta(t - nT_s)$, $x_s(t) = \sum_n x(nT_s)\delta(t - nT_s)$. The impulse train has the Fourier series $p(t) = \dfrac{1}{T_s}\sum_m e^{jm\omega_st}$, $\omega_s = 2\pi f_s$, so by the frequency shift property

$$X_s(\omega) = \frac{1}{T_s}\sum_{m=-\infty}^{\infty}X(\omega - m\omega_s):$$

the spectrum of $x$ is repeated at every multiple of $\omega_s$ and scaled by $1/T_s$. The copies are $\omega_s$ apart and each is $2\omega_m$ wide, so they **do not overlap** if $\omega_s - \omega_m \ge \omega_m$, that is $\omega_s \ge 2\omega_m$, $f_s \ge 2f_m$. Then passing $x_s(t)$ through an ideal low-pass filter of gain $T_s$ and cut-off $\omega_c$ with $\omega_m \le \omega_c \le \omega_s - \omega_m$ selects the $m = 0$ copy and returns $X(\omega)$, hence $x(t)$:

$$x(t) = \sum_n x(nT_s)\,\mathrm{sinc}\!\left(\frac{t - nT_s}{T_s}\right)\ \text{for } f_s = 2f_m .\qquad\blacksquare$$

**Aliasing.** If $f_s < 2f_m$ the shifted copies **overlap**; the high-frequency part of one copy falls on the low-frequency part of the next, a frequency $f$ then appears as $\lvert f - mf_s\rvert$ (an *alias*), and the original cannot be recovered by filtering (the distortion is permanent). It is caused by under-sampling ($f_s < 2f_m$) or by a signal that is not band-limited. Example: a 700 Hz tone sampled at 1000 Hz appears as 300 Hz. It is prevented with an anti-aliasing low-pass filter before sampling and a sampling rate of at least $2f_m$.

**(b) Nyquist rate for $x(t) = 5\cos(3000\pi t)\sin(1000\pi t)$.** Use $\cos A\sin B = \tfrac12[\sin(A + B) - \sin(A - B)]$ with $A = 3000\pi t$, $B = 1000\pi t$:

$$x(t) = \frac52\bigl[\sin(4000\pi t) - \sin(2000\pi t)\bigr].$$

The frequencies are $f_1 = 4000\pi/2\pi = 2000$ Hz and $f_2 = 2000\pi/2\pi = 1000$ Hz, so $f_{max} = 2000$ Hz (2 kHz) and

$$\text{Nyquist rate} = 2f_{max} = \mathbf{4000\ Hz\ (4\ kHz)},\qquad T_s = \frac{1}{4000} = 0.25\ \text{ms}.$$

(The product contains the sum frequency, 2 kHz, so $f_{max}$ is 2 kHz and not the 1.5 kHz of the cosine alone; the identity was verified numerically.)

@s 7
**Frequency response.** The response of a LTI system to $e^{j\omega t}$ is $H(\omega)e^{j\omega t}$ with

$$H(\omega) = \int_{-\infty}^{\infty}h(t)\,e^{-j\omega t}dt = \frac{Y(\omega)}{X(\omega)} = \lvert H(\omega)\rvert\,e^{j\angle H(\omega)},$$

the Fourier transform of the impulse response: $\lvert H\rvert$ is the gain and $\angle H$ the phase shift each frequency receives ($Y = XH$); for DT systems $H(\Omega) = \sum h[n]e^{-j\Omega n}$.

**Ideal low-pass filter (LPF)** with cut-off $\omega_c$: it passes all frequencies below $\omega_c$ with unit gain and zero phase (linear phase $e^{-j\omega t_0}$ would only delay the output) and stops all others:

$$H_{LP}(\omega) = \begin{cases}1 & \lvert\omega\rvert \le \omega_c\\ 0 & \lvert\omega\rvert > \omega_c\end{cases}$$

The impulse response is the inverse Fourier transform:

$$h_{LP}(t) = \frac{1}{2\pi}\int_{-\omega_c}^{\omega_c}e^{j\omega t}d\omega = \frac{1}{2\pi}\left[\frac{e^{j\omega t}}{jt}\right]_{-\omega_c}^{\omega_c} = \frac{1}{2\pi}\cdot\frac{e^{j\omega_ct} - e^{-j\omega_ct}}{jt} = \frac{\sin\omega_ct}{\pi t} = \frac{\omega_c}{\pi}\,\mathrm{sinc}\!\left(\frac{\omega_ct}{\pi}\right),$$

with $\mathrm{sinc}(x) = \sin(\pi x)/(\pi x)$ and $h_{LP}(0) = \omega_c/\pi$. It extends from $-\infty$ to $\infty$, so it is **non-causal** (nonzero for $t < 0$) and cannot be built exactly (it is approximated with a delay and a window, or with Butterworth, Chebyshev filters).

**Ideal high-pass filter (HPF):** it stops $\lvert\omega\rvert < \omega_c$ and passes all higher frequencies,

$$H_{HP}(\omega) = \begin{cases}0 & \lvert\omega\rvert < \omega_c\\ 1 & \lvert\omega\rvert \ge \omega_c\end{cases} = 1 - H_{LP}(\omega).$$

By linearity, with $1 \leftrightarrow \delta(t)$,

$$h_{HP}(t) = \delta(t) - h_{LP}(t) = \delta(t) - \frac{\sin\omega_ct}{\pi t}.$$

{{FIG_ideal}}

The HPF is also non-causal and not realisable exactly. Equivalent results in DT (cut-off $\Omega_c$): $h_{LP}[n] = \dfrac{\sin\Omega_cn}{\pi n}$ ($\Omega_c/\pi$ at $n = 0$) and $h_{HP}[n] = \delta[n] - \dfrac{\sin\Omega_cn}{\pi n}$.
