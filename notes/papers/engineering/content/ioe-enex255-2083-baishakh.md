---
file: NEBians-IOE-Past-Paper-Signals-and-Systems-ENEX255-2083-Baishakh.pdf
subject: Signals and Systems
level: BE · Year II / Part II
code: ENEX 255
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Define signals both in continuous time and discrete time with examples. Give the difference between them. [[4]]

b) Determine whether the following signal is an energy or power signal. (i) $f(t) = 3\cos(4\pi t)$ (ii) $x[n] = \sin\left(\frac{\pi n}{6}\right)$ [[4]]

@q 2
a) Derive the exponential form of the Fourier series of a discrete-time signal. [[4]]

b) Find and plot the Fourier series coefficients for the following signal with period $N$: $x[n] = 1 + \sin\left(\frac{2\pi}{N}\right)n + 3\cos\left(\frac{2\pi}{N}\right)n + \cos\left(\frac{4\pi}{N}n + \frac{\pi}{2}\right)$ [[4]]

@q 3
a) State and prove Parseval's theorem for energy signal. [[4]]

b) Describe the continuous-time Fourier series' time reversal, time scaling and frequency shifting properties. [[4]]

@q 4
a) Derive the Fourier transform pair equations of a discrete-time signal. [[5]]

b) Find the continuous time Fourier transform of the signal $x(t) = e^{j\omega_0 t}$. Discuss the result. [[5]]

@q 5
a) Describe the frequency response of a continuous-time LTI system. [[4]]

b) Derive the transfer function of the RC low-pass filter and plot the magnitude and phase. [[4]]

@q 6
a) Derive the convolution sum of a discrete-time signal. [[4]]

b) Find the convolution sum of $x[n] = \{1, 2, 3, 4\}$ and $h[n] = \{1, 2, -3\}$. Choose your own origin. [[4]]

@q 7
a) Define sampling theorem. Explain the aliasing effect and its cause. Find the Nyquist rate and Nyquist time interval of the following signal. $x(t) = 5\cos(150\pi t) + 10\sin(350\pi t) + \cos(150\pi t)$ [[2+2+2]]

b) Find the frequency response of the following signal $y[n] = 0.5\,x[n] - 0.5\,x[n-1]$; $h[n] = \frac12$ for $n = 0$ and $-\frac12$ for $n = 1$. [[4]]

<!-- SOLUTIONS -->

@s 1
**(a) Signals.** A **signal** is a function that carries information about a physical quantity: it varies with one or more independent variables (usually time), for example voltage, speech or temperature.

- A **continuous-time (CT) signal** $x(t)$ is defined for every value of the continuous independent variable $t$ and its amplitude may take any value (analog). Examples: a speech waveform, $x(t) = 5\cos(2\pi\,50\,t)$, the temperature of a room.
- A **discrete-time (DT) signal** $x[n]$ is defined only at integer values $n$ (a sequence of samples). Examples: the daily closing share price, $x[n] = (0.5)^n u[n]$, the samples of speech taken at 8 kHz. (A DT signal whose amplitude is also quantized is a *digital* signal.)

| Basis | Continuous-time signal | Discrete-time signal |
|---|---|---|
| Independent variable | continuous, $t \in \mathbb{R}$ | integers, $n \in \mathbb{Z}$ |
| Notation | $x(t)$, round brackets | $x[n]$, square brackets |
| Defined | at every instant | only at sampling instants |
| Graph | a continuous curve | a stem (lollipop) plot |
| Mathematics | differential equations, integrals, Laplace and Fourier transforms | difference equations, sums, Z-transform and DTFT |
| Periodicity | periodic if $x(t + T) = x(t)$ for any real $T$ | periodic only if $x[n + N] = x[n]$ with integer $N$ (i.e. $\Omega_0/2\pi$ rational) |
| Frequency range | $-\infty < \omega < \infty$, all different | $\Omega$ and $\Omega + 2\pi$ identical |
| Obtained by | natural phenomena, sensors | sampling a CT signal: $x[n] = x(nT_s)$ |

**(b) Energy or power signal.** Energy $E = \sum\lvert x\rvert^2$ (or $\int\lvert x\rvert^2dt$) and power $P = \lim \dfrac{1}{T}\int\lvert x\rvert^2dt$ (average over time). An energy signal has $0 < E < \infty$ (so $P = 0$); a power signal has $0 < P < \infty$ (so $E = \infty$).

(i) $f(t) = 3\cos 4\pi t$ is periodic with $T = 2\pi/4\pi = 0.5$ s. Over a period

$$P = \frac{1}{T}\int_0^{T} 9\cos^2(4\pi t)\,dt = \frac{9}{2} = 4.5\ \text{W}.$$

The energy over all time is infinite ($E = \infty$). Hence $f(t)$ is a **power signal** ($P = A^2/2 = 4.5$).

(ii) $x[n] = \sin(\pi n/6)$: the digital frequency is $\Omega_0 = \pi/6$ and $\Omega_0/2\pi = 1/12$ is rational, so the signal is periodic with $N = 12$. Its power is

$$P = \frac{1}{12}\sum_{n=0}^{11}\sin^2\left(\frac{\pi n}{6}\right) = \frac{1}{12}\cdot 6 = \frac12.$$

The energy is infinite (the sum of a never-decaying periodic sequence). Hence $x[n]$ is a **power signal** with $P = 1/2$.

@s 2
**(a) Exponential Fourier series of a DT periodic signal.** Let $x[n]$ have period $N$, $x[n + N] = x[n]$, and fundamental frequency $\Omega_0 = 2\pi/N$. The complex exponentials $\phi_k[n] = e^{jk\Omega_0 n}$ are periodic with the same period and only $N$ of them are different, because $\phi_{k+N}[n] = e^{jk\Omega_0 n}e^{j2\pi n} = \phi_k[n]$. So we write

$$\begin{gathered}x[n] = \sum_{k=0}^{N-1} c_k\,e^{jk\Omega_0 n} \\ (1)\end{gathered}$$

To find $c_k$ multiply both sides of (1) by $e^{-jr\Omega_0 n}$ and sum over one period ($n = 0$ to $N-1$):

$$\sum_{n=0}^{N-1} x[n]e^{-jr\Omega_0 n} = \sum_{k=0}^{N-1} c_k \sum_{n=0}^{N-1} e^{j(k-r)\Omega_0 n}.$$

The inner sum is a geometric series: for $k - r$ a multiple of $N$ it equals $N$ (every term is 1), otherwise $\dfrac{1 - e^{j(k-r)2\pi}}{1 - e^{j(k-r)2\pi/N}} = 0$. (orthogonality). So only $k = r$ survives and

$$c_k = \frac{1}{N}\sum_{n=0}^{N-1} x[n]\,e^{-jk\Omega_0 n}. \tag{2}$$

Equations (1) (synthesis) and (2) (analysis) are the **DT Fourier series pair**; the coefficients are periodic, $c_{k+N} = c_k$, so the spectrum is periodic with $N$ lines. Parseval: average power $\dfrac{1}{N}\sum\lvert x[n]\rvert^2 = \sum_{k=0}^{N-1}\lvert c_k\rvert^2$.

**(b) Coefficients of $x[n] = 1 + \sin\Omega_0 n + 3\cos\Omega_0 n + \cos(2\Omega_0 n + \pi/2)$**, $\Omega_0 = 2\pi/N$. Write every term with Euler's formula and match with $x[n] = \sum c_k e^{jk\Omega_0 n}$:

- $1 \Rightarrow c_0 = 1$;
- $\sin\Omega_0 n = \dfrac{e^{j\Omega_0 n} - e^{-j\Omega_0 n}}{2j}$ → contributes $\dfrac{1}{2j} = -\dfrac{j}{2}$ to $c_1$ and $+\dfrac{j}{2}$ to $c_{-1}$;
- $3\cos\Omega_0 n = \dfrac32 e^{j\Omega_0 n} + \dfrac32 e^{-j\Omega_0 n}$ → contributes $\dfrac32$ to $c_1$ and $c_{-1}$;
- $\cos(2\Omega_0 n + \pi/2) = \dfrac12 e^{j\pi/2}e^{j2\Omega_0 n} + \dfrac12 e^{-j\pi/2}e^{-j2\Omega_0 n}$ → $c_2 = \dfrac{j}{2}$, $c_{-2} = -\dfrac{j}{2}$.

$$\begin{gathered} c_0 = 1,\quad c_1 = \frac32 - \frac{j}{2},\quad c_{-1} = \frac32 + \frac{j}{2} \\ c_2 = \frac{j}{2},\quad c_{-2} = -\frac{j}{2} \end{gathered}$$

and all other $c_k = 0$ in $-N/2 < k \le N/2$ (this needs $N \ge 5$ so that the lines do not overlap; the pattern repeats with period $N$: $c_{k+N} = c_k$; for example $c_{N-1} = c_{-1}$).

| $k$ | $c_k$ | $\lvert c_k\rvert$ | $\angle c_k$ |
|---|---|---|---|
| 0 | 1 | 1 | $0^\circ$ |
| $\pm1$ | $\tfrac32 \mp \tfrac{j}{2}$ | $\dfrac{\sqrt{10}}{2} = 1.581$ | $\mp 18.43^\circ$ |
| $\pm2$ | $\pm\tfrac{j}{2}$ | $0.5$ | $\pm 90^\circ$ |

```figure caption="Spectra of x[n] = 1 + sin(2 pi n/N) + 3 cos(2 pi n/N) + cos(4 pi n/N + pi/2) (N >= 5): magnitude |c_k| (left) and phase of c_k (right); both repeat with period N."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
import numpy as np
k=np.arange(-4,5); c={0:1,1:1.5-0.5j,-1:1.5+0.5j,2:0.5j,-2:-0.5j}
mag=[abs(c.get(i,0)) for i in k]; ph=[np.degrees(np.angle(c[i])) if i in c else 0 for i in k]
fig,(a,b)=plt.subplots(1,2,figsize=(7.4,2.9))
a.stem(k,mag,linefmt=ACCENT,markerfmt="o",basefmt="k-"); a.set_xlabel("k",fontsize=7); a.set_title("|c_k|",fontsize=8); a.set_ylim(0,1.9); a.tick_params(labelsize=6)
for i,m in zip(k,mag):
    if m>0: a.text(i,m+0.08,"%.3g"%m,ha="center",fontsize=6.5)
b.stem(k,ph,linefmt="#b00020",markerfmt="o",basefmt="k-"); b.set_xlabel("k",fontsize=7); b.set_title("angle of c_k (degrees)",fontsize=8); b.set_ylim(-130,130); b.tick_params(labelsize=6)
for i,p in zip(k,ph):
    if i in c: b.text(i,p+(12 if p>=0 else -22),"%.1f"%p,ha="center",fontsize=6.5)
fig.tight_layout()
```


*Check:* the average power from the time domain, $1 + \tfrac12(1^2 + 3^2) + \tfrac12 = 6.5$, equals $\sum\lvert c_k\rvert^2 = 1 + 2(2.5) + 2(0.25) = 6.5$ (Parseval). The coefficients were also confirmed with an FFT for $N = 8$.

@s 3
**(a) Parseval's theorem for an energy signal.** *Statement:* the energy of an aperiodic signal can be found either in the time domain or in the frequency domain:

$$E = \int_{-\infty}^{\infty}\lvert x(t)\rvert^2dt = \frac{1}{2\pi}\int_{-\infty}^{\infty}\lvert X(\omega)\rvert^2d\omega = \int_{-\infty}^{\infty}\lvert X(f)\rvert^2df.$$

*Proof.* Write $\lvert x(t)\rvert^2 = x(t)\,x^*(t)$ and substitute the inverse Fourier transform for $x^*(t)$, $x^*(t) = \dfrac{1}{2\pi}\displaystyle\int X^*(\omega)e^{-j\omega t}d\omega$:

$$E = \int x(t)\left[\frac{1}{2\pi}\int X^*(\omega)e^{-j\omega t}d\omega\right]dt = \frac{1}{2\pi}\int X^*(\omega)\left[\int x(t)e^{-j\omega t}dt\right]d\omega.$$

The inner integral is $X(\omega)$, so

$$\begin{gathered}E = \frac{1}{2\pi}\int X^*(\omega)X(\omega)\,d\omega = \frac{1}{2\pi}\int\lvert X(\omega)\rvert^2d\omega. \\ \blacksquare\end{gathered}$$

$\lvert X(\omega)\rvert^2$ is the *energy spectral density* (J per rad/s). *Example:* $x(t) = e^{-at}u(t)$ gives $E = \int_0^\infty e^{-2at}dt = \dfrac{1}{2a}$ and $\lvert X\rvert^2 = \dfrac{1}{a^2 + \omega^2}$, $\dfrac{1}{2\pi}\int\dfrac{d\omega}{a^2 + \omega^2} = \dfrac{1}{2\pi}\cdot\dfrac{\pi}{a} = \dfrac{1}{2a}$ as well.

**(b) Properties of the CT Fourier series.** Let $x(t) \leftrightarrow c_k$ with period $T$ and $\omega_0 = 2\pi/T$, $x(t) = \sum c_k e^{jk\omega_0 t}$.

1. **Time reversal:** $x(-t) \leftrightarrow c_{-k}$. *Proof:* $x(-t) = \sum c_k e^{-jk\omega_0 t}$; replace $k$ by $-m$: $= \sum c_{-m}e^{jm\omega_0 t}$, so the coefficients are $c_{-m}$. Meaning: reversing the signal reverses the spectrum (an even $x$ has even $c_k$, and an odd $x$ has odd $c_k$).
2. **Time scaling:** $x(\alpha t)$ ($\alpha > 0$) is periodic with $T/\alpha$ and $\omega_0' = \alpha\omega_0$: $x(\alpha t) = \sum c_k e^{jk(\alpha\omega_0)t}$. The **coefficients are unchanged** $(c_k)$ but the harmonics move to $k\alpha\omega_0$: compression in time ($\alpha > 1$) spreads the spectral lines apart; expansion packs them together.
3. **Frequency shifting (modulation):** $x(t)\,e^{jM\omega_0 t} \leftrightarrow c_{k-M}$. *Proof:* $x(t)e^{jM\omega_0 t} = \sum c_k e^{j(k+M)\omega_0 t} = \sum c_{m-M}e^{jm\omega_0 t}$ with $m = k + M$. So multiplying by a complex exponential shifts the whole line spectrum by $M$ harmonics (e.g. $x(t)\cos(M\omega_0 t) \leftrightarrow \tfrac12(c_{k-M} + c_{k+M})$).

@s 4
**(a) The DT Fourier transform (DTFT) pair.** Take an aperiodic $x[n]$ that is zero outside $-N_1 \le n \le N_2$ and build a periodic signal $\tilde x[n]$ of period $N > N_1 + N_2$ by repeating it. By the DT Fourier series,

$$\begin{gathered}\tilde x[n] = \sum_{k=\langle N\rangle}c_k e^{jk\Omega_0 n} \\ c_k = \frac{1}{N}\sum_{n=\langle N\rangle}\tilde x[n]e^{-jk\Omega_0 n},\quad \Omega_0 = \frac{2\pi}{N}.\end{gathered}$$

Over $-N/2 \le n \le N/2$ the periodic and the aperiodic signals coincide, so the limits of the sum can be taken as $\pm\infty$ for $x[n]$: $N c_k = \displaystyle\sum_{n=-\infty}^{\infty}x[n]e^{-jk\Omega_0 n}$. Define the function

$$\begin{gathered}X(\Omega) = \sum_{n=-\infty}^{\infty}x[n]\,e^{-j\Omega n} \\ \text{(analysis equation, DTFT)}\end{gathered}$$

so that $c_k = \dfrac{1}{N}X(k\Omega_0)$. Substituting in the series,

$$\tilde x[n] = \sum_{k=\langle N\rangle}\frac{1}{N}X(k\Omega_0)e^{jk\Omega_0 n} = \frac{1}{2\pi}\sum_{k=\langle N\rangle}X(k\Omega_0)e^{jk\Omega_0 n}\,\Omega_0 .$$

As $N \to \infty$: $\Omega_0 \to d\Omega$, $k\Omega_0 \to \Omega$, $\tilde x[n] \to x[n]$ and the sum over one period of $N$ terms (a width of $N\Omega_0 = 2\pi$) becomes an integral over any interval of length $2\pi$:

$$\begin{gathered}x[n] = \frac{1}{2\pi}\int_{2\pi}X(\Omega)\,e^{j\Omega n}\,d\Omega \\ \text{(synthesis equation, inverse DTFT)}.\end{gathered}$$

The pair is $x[n] \leftrightarrow X(\Omega)$. Properties: $X(\Omega)$ is continuous and **periodic with $2\pi$**, since $e^{-j(\Omega+2\pi)n} = e^{-j\Omega n}$; the condition for convergence is $\sum\lvert x[n]\rvert < \infty$. *Example:* $x[n] = a^nu[n]$, $\lvert a\rvert < 1$: $X(\Omega) = \dfrac{1}{1 - ae^{-j\Omega}}$.

**(b) CTFT of $x(t) = e^{j\omega_0 t}$.** The direct integral $\int e^{j\omega_0 t}e^{-j\omega t}dt$ does not converge in the ordinary sense (the signal is not absolutely integrable), so it is found through the inverse transform. Try $X(\omega) = 2\pi\,\delta(\omega - \omega_0)$:

$$x(t) = \frac{1}{2\pi}\int_{-\infty}^{\infty}2\pi\,\delta(\omega - \omega_0)e^{j\omega t}d\omega = e^{j\omega_0 t}$$

by the sifting property. Hence

$$e^{j\omega_0 t}\ \longleftrightarrow\ X(\omega) = 2\pi\,\delta(\omega - \omega_0).$$

*Discussion.* (1) The spectrum is a **single impulse at $\omega = \omega_0$**: a complex exponential contains exactly one frequency, with an infinite density at that frequency and zero elsewhere (an impulse has finite area $2\pi$, which stands for a finite power). (2) It is a one-sided spectrum: only the positive frequency $\omega_0$ appears, which is why a real signal needs the pair $e^{\pm j\omega_0 t}$. Thus $\cos\omega_0 t \leftrightarrow \pi[\delta(\omega - \omega_0) + \delta(\omega + \omega_0)]$ and $\sin\omega_0 t \leftrightarrow \dfrac{\pi}{j}[\delta(\omega - \omega_0) - \delta(\omega + \omega_0)]$. (3) For $\omega_0 = 0$ it gives $1 \leftrightarrow 2\pi\delta(\omega)$: a DC signal sits at zero frequency. (4) It also shows the frequency-shift property: multiplying by $e^{j\omega_0 t}$ shifts the spectrum of $1$ to $\omega_0$; this is the basis of modulation. (5) The Fourier transform exists here only as a generalized function; the signal has infinite energy but finite power.

@s 5
**(a) Frequency response of a CT LTI system.** Complex exponentials are the **eigenfunctions** of an LTI system. For the input $x(t) = e^{j\omega t}$ and impulse response $h(t)$,

$$y(t) = \int h(\tau)\,e^{j\omega(t - \tau)}d\tau = e^{j\omega t}\int h(\tau)e^{-j\omega\tau}d\tau = H(\omega)\,e^{j\omega t},$$

where

$$H(\omega) = \int_{-\infty}^{\infty}h(t)\,e^{-j\omega t}dt = \frac{Y(\omega)}{X(\omega)}$$

is the **frequency response** (the Fourier transform of $h(t)$; for a stable system $H(\omega) = H(s)|_{s = j\omega}$). It is a complex function: $H(\omega) = \lvert H(\omega)\rvert e^{j\angle H(\omega)}$, with the **magnitude response** $\lvert H\rvert$ (gain at each frequency) and the **phase response** $\angle H$ (phase shift). A sinusoid $A\cos(\omega_0 t + \theta)$ at the input gives $A\lvert H(\omega_0)\rvert\cos(\omega_0 t + \theta + \angle H(\omega_0))$ at the output, so the system changes the amplitude and the phase of every frequency component; in the frequency domain convolution becomes multiplication, $Y(\omega) = X(\omega)H(\omega)$. For real $h(t)$, $\lvert H\rvert$ is even and $\angle H$ is odd. The frequency response classifies filters: low-pass, high-pass, band-pass, band-stop; distortionless transmission needs a constant $\lvert H\rvert$ and a phase linear in $\omega$.

**(b) RC low-pass filter.** The series resistor $R$ and the capacitor $C$ across the output; $x(t)$ is the input voltage, $y(t)$ the capacitor voltage. In the s-domain the capacitor impedance is $1/sC$, so by the voltage divider

$$\begin{gathered}H(s) = \frac{Y(s)}{X(s)} = \frac{1/sC}{R + 1/sC} = \frac{1}{1 + sRC} \\ H(\omega) = \frac{1}{1 + j\omega RC}.\end{gathered}$$

(In the time domain $RC\,\dot y + y = x$, and $h(t) = \tfrac{1}{RC}e^{-t/RC}u(t)$.) With the cut-off frequency $\omega_c = 1/RC$:

$$\begin{gathered}\lvert H(\omega)\rvert = \frac{1}{\sqrt{1 + (\omega RC)^2}} = \frac{1}{\sqrt{1 + (\omega/\omega_c)^2}} \\ \angle H(\omega) = -\tan^{-1}(\omega RC).\end{gathered}$$

| $\omega/\omega_c$ | 0 | 0.1 | 1 | 10 | $\infty$ |
|---|---|---|---|---|---|
| $\lvert H\rvert$ | 1 | 0.995 | 0.707 (−3 dB) | 0.0995 (−20 dB) | 0 |
| $\angle H$ | $0^\circ$ | $-5.7^\circ$ | $-45^\circ$ | $-84.3^\circ$ | $-90^\circ$ |

```figure caption="RC low-pass filter: circuit, magnitude response |H| (dB) and phase response against w/wc (log scale); wc = 1/RC, |H| = -3 dB and phase = -45 degrees at wc."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
import numpy as np
fig=plt.figure(figsize=(7.4,3.4))
c=fig.add_axes([0.0,0.05,0.34,0.9]); c.axis("off"); c.set_xlim(0,6); c.set_ylim(0,6)
L=dict(color=INK,lw=1.4)
c.plot([0.8,1.5],[4.5,4.5],**L)
zx=[1.5,1.7,1.9,2.1,2.3,2.5,2.7,2.9,3.1]; zy=[4.5,4.9,4.1,4.9,4.1,4.9,4.1,4.9,4.5]
c.plot(zx,zy,**L); c.plot([3.1,4.4],[4.5,4.5],**L)
c.plot([4.4,4.4],[4.5,3.5],**L); c.plot([3.9,4.9],[3.5,3.5],color=INK,lw=2.4); c.plot([3.9,4.9],[3.0,3.0],color=INK,lw=2.4); c.plot([4.4,4.4],[3.0,1.5],**L)
c.plot([0.8,4.4],[1.5,1.5],**L); c.plot([0.8,0.8],[1.5,4.5],**L,alpha=0); c.plot([4.4,5.2],[4.5,4.5],**L); c.plot([4.4,5.2],[1.5,1.5],**L)
c.plot([0.8,0.8],[1.5,2.4],**L); c.plot([0.8,0.8],[3.6,4.5],**L); c.add_patch(mp.Circle((0.8,3.0),0.6,fc="white",ec=INK,lw=1.4)); c.text(0.8,3.0,"~",ha="center",va="center",fontsize=11)
c.plot([5.2,5.2],[1.5,4.5],color=ACCENT,lw=1.2,ls="--"); c.plot([5.2],[4.5],"o",color=ACCENT,ms=4); c.plot([5.2],[1.5],"o",color=ACCENT,ms=4)
c.text(2.3,5.35,"R",fontsize=9,ha="center"); c.text(5.15,3.25,"C",fontsize=9); c.text(0.15,3.0,"x(t)",fontsize=8,ha="right"); c.text(5.4,3.0,"y(t)",fontsize=8,va="center")
w=np.logspace(-2,2,400); H=1/(1+1j*w)
a=fig.add_axes([0.46,0.57,0.52,0.38]); a.semilogx(w,20*np.log10(abs(H)),color=ACCENT,lw=1.6); a.axhline(-3,color="#999",lw=0.6,ls=":"); a.axvline(1,color="#999",lw=0.6,ls=":")
a.set_ylabel("|H| (dB)",fontsize=7); a.tick_params(labelsize=6); a.set_xticklabels([]); a.set_ylim(-42,3); a.plot([1],[-3.01],"o",color="#b00020",ms=3)
b=fig.add_axes([0.46,0.14,0.52,0.38]); b.semilogx(w,np.degrees(np.angle(H)),color="#b00020",lw=1.6); b.axhline(-45,color="#999",lw=0.6,ls=":"); b.axvline(1,color="#999",lw=0.6,ls=":")
b.set_ylabel("phase (deg)",fontsize=7); b.set_xlabel("w / wc",fontsize=7); b.tick_params(labelsize=6); b.set_ylim(-95,5); b.plot([1],[-45],"o",color="#b00020",ms=3)
```


Low frequencies pass with unit gain and no phase shift; above $\omega_c$ the gain falls at 20 dB per decade (−6 dB/octave); the phase tends to −90°. The $-3$ dB bandwidth is $\omega_c = 1/RC$ (for example $R = 1\,\text{k}\Omega$, $C = 1\,\mu\text{F}$ gives $\omega_c = 1000$ rad/s, $f_c = 159$ Hz).

@s 6
**(a) Convolution sum.** Any DT signal is a weighted sum of shifted impulses (sifting): $x[n] = \displaystyle\sum_{k=-\infty}^{\infty}x[k]\,\delta[n - k]$. For a **linear** system the response to a sum is the sum of the responses, and for a **time-invariant** system the response to $\delta[n - k]$ is $h[n - k]$, where $h[n]$ is the response to $\delta[n]$. Therefore

$$y[n] = T\left[\sum_k x[k]\delta[n - k]\right] = \sum_k x[k]\,T\{\delta[n-k]\} = \sum_{k=-\infty}^{\infty}x[k]\,h[n - k] = x[n] * h[n].$$

*Properties:* commutative $x * h = h * x$, associative, distributive over addition, $x[n] * \delta[n - n_0] = x[n - n_0]$; the length of the output is $L_x + L_h - 1$. *Steps to evaluate:* fold $h[k] \to h[-k]$, shift by $n$, multiply with $x[k]$ and sum.

**(b) Convolution of $x[n] = \{1, 2, 3, 4\}$ and $h[n] = \{1, 2, -3\}$.** Choose the origin at the first sample of each, $x[0] = 1,\ x[1] = 2,\ x[2] = 3,\ x[3] = 4$ and $h[0] = 1,\ h[1] = 2,\ h[2] = -3$. The output has $4 + 3 - 1 = 6$ samples ($n = 0$ to 5).

*Tabular (shift and add) method:* each $x[k]$ multiplies the whole $h$ and the row is shifted by $k$; the column sums give $y[n]$.

| $x[k]$ | n=0 | n=1 | n=2 | n=3 | n=4 | n=5 |
|---|---|---|---|---|---|---|
| 1 ($k = 0$) | 1 | 2 | -3 |  |  |  |
| 2 ($k = 1$) |  | 2 | 4 | -6 |  |  |
| 3 ($k = 2$) |  |  | 3 | 6 | -9 |  |
| 4 ($k = 3$) |  |  |  | 4 | 8 | -12 |
| **y[n]** | **1** | **4** | **4** | **4** | **-1** | **-12** |

$$\begin{gathered}y[n] = \{1, 4, 4, 4, -1, -12\} \\ n = 0,\dots,5.\end{gathered}$$

*Direct check:* $y[0] = x[0]h[0] = 1$; $y[1] = x[0]h[1] + x[1]h[0] = 2 + 2 = 4$; $y[2] = x[0]h[2] + x[1]h[1] + x[2]h[0] = -3 + 4 + 3 = 4$; $y[3] = x[1]h[2] + x[2]h[1] + x[3]h[0] = -6 + 6 + 4 = 4$; $y[4] = x[2]h[2] + x[3]h[1] = -9 + 8 = -1$; $y[5] = x[3]h[2] = -12$. The sum $\sum y = 1 + 4 + 4 + 4 - 1 - 12 = 0 = (\sum x)(\sum h) = 10 \times 0$. (With a different origin the whole sequence is just shifted.)

```figure caption="Convolution of x[n] = {1, 2, 3, 4} and h[n] = {1, 2, -3} with the first sample of each at n = 0: y[n] has 4 + 3 - 1 = 6 samples."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
import numpy as np
x=[1.0, 2.0, 3.0, 4.0]; h=[1.0, 2.0, -3.0]; y=[1.0, 4.0, 4.0, 4.0, -1.0, -12.0]
fig,axs=plt.subplots(1,3,figsize=(7.4,2.5))
for ax,v,t in zip(axs,(x,h,y),("x[n]","h[n]","y[n] = x[n] * h[n]")):
    n=np.arange(len(v)); ax.stem(n,v,linefmt=ACCENT,markerfmt="o",basefmt="k-"); ax.set_title(t,fontsize=8); ax.set_xlabel("n",fontsize=7); ax.tick_params(labelsize=6)
    ax.set_ylim(min(0,min(v))-0.15*(max(v)-min(v)+1),max(0,max(v))+0.2*(max(v)-min(v)+1)); ax.set_xticks(n)
    for i,vv in zip(n,v): ax.text(i,vv+(0.04*(max(v)-min(v)+1) if vv>=0 else -0.1*(max(v)-min(v)+1)),("%.4g"%vv),ha="center",fontsize=5.5)
fig.tight_layout()
```


@s 7
**(a) Sampling theorem.** *Statement:* a band-limited signal with highest frequency $f_{max}$ (no components above $f_{max}$) can be **completely recovered** from its samples if it is sampled at a rate

$$f_s \ge 2f_{max},$$

and the minimum rate $2f_{max}$ is the **Nyquist rate**; the **Nyquist interval** is $T_s = 1/(2f_{max})$. Recovery is done by an ideal low-pass filter with cut-off between $f_{max}$ and $f_s - f_{max}$ (interpolation by sinc functions).

**Aliasing.** Sampling in the time domain makes the spectrum repeat at all multiples of $f_s$: $X_s(f) = f_s\sum_m X(f - mf_s)$. If $f_s < 2f_{max}$ the neighbouring replicas **overlap**, so the high frequency components of the signal appear as (are "aliases" of) lower frequencies and cannot be separated; the original cannot be recovered. *Cause:* sampling below the Nyquist rate (or a signal that is not band-limited). A component of frequency $f$ appears at $\lvert f - mf_s\rvert$ (e.g. 175 Hz sampled at 200 Hz appears as 25 Hz). *Prevention:* an anti-aliasing low-pass filter before the sampler, and $f_s \ge 2f_{max}$ (in practice 2.2 to 2.5 times).

```figure caption="Sampling in the frequency domain: for fs > 2B the replicas of the spectrum at multiples of fs do not overlap (left); for fs < 2B they overlap, which is aliasing (right)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
import numpy as np
fig,(a,b)=plt.subplots(1,2,figsize=(7.4,2.6))
def tri(f,B): return np.clip(1-abs(f)/B,0,None)
f=np.linspace(-16,16,2000); B=3
for ax,fs,t in ((a,8,"fs = 8 B/3 > 2B: no overlap"),(b,4,"fs = 4 B/3 < 2B: overlap (aliasing)")):
    tot=0
    for m in range(-3,4):
        y=tri(f-m*fs,B); ax.plot(f,y,color=ACCENT if m==0 else "#b00020",lw=1.3 if m==0 else 0.9,ls="-" if m==0 else "--"); tot=tot+y
    if fs<2*B: ax.fill_between(f,0,tot,where=tot>1.0001*np.maximum(tri(f,B),0),color="#b00020",alpha=0.15)
    ax.set_title(t,fontsize=7.5); ax.set_xlim(-14,14); ax.set_ylim(0,1.5); ax.set_xlabel("f",fontsize=7); ax.tick_params(labelsize=6)
    ax.set_xticks([-fs,0,fs]); ax.set_xticklabels(["-fs","0","fs"])
fig.tight_layout()
```


**Nyquist rate of $x(t) = 5\cos150\pi t + 10\sin350\pi t + \cos150\pi t$.** The two cosines add: $6\cos 150\pi t$. The frequencies are

$$\begin{gathered}f_1 = \frac{150\pi}{2\pi} = 75\ \text{Hz} \\ f_2 = \frac{350\pi}{2\pi} = 175\ \text{Hz}\end{gathered}$$

so $f_{max} = 175$ Hz. Nyquist rate $= 2f_{max} = \mathbf{350\ Hz}$ (samples/s), and Nyquist time interval $T_s = 1/350 = 2.857\ \text{ms}$.

**(b) Frequency response of $y[n] = 0.5x[n] - 0.5x[n-1]$.** Applying $x[n] = \delta[n]$ gives the impulse response $h[n] = 0.5\,\delta[n] - 0.5\,\delta[n-1]$, i.e. $h[0] = \tfrac12,\ h[1] = -\tfrac12$ (as given). The frequency response is the DTFT of $h[n]$:

$$H(\Omega) = \sum_n h[n]e^{-j\Omega n} = 0.5 - 0.5\,e^{-j\Omega} = 0.5\,e^{-j\Omega/2}\left(e^{j\Omega/2} - e^{-j\Omega/2}\right) = j\,\sin\frac{\Omega}{2}\;e^{-j\Omega/2}.$$

Therefore

$$\begin{gathered}\lvert H(\Omega)\rvert = \left\lvert\sin\frac{\Omega}{2}\right\rvert \\ \angle H(\Omega) = \frac{\pi}{2} - \frac{\Omega}{2}\quad (0 < \Omega < \pi),\quad -\frac{\pi}{2} - \frac{\Omega}{2}\quad(-\pi < \Omega < 0).\end{gathered}$$

```figure caption="Frequency response of y[n] = 0.5 x[n] - 0.5 x[n-1]: |H(W)| = |sin(W/2)| (a high-pass / differencing filter) and its phase."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
import numpy as np
W=np.linspace(-np.pi,np.pi,801); H=0.5*(1-np.exp(-1j*W))
fig,(a,b)=plt.subplots(1,2,figsize=(7.4,2.7))
a.plot(W,abs(H),color=ACCENT,lw=1.6); a.set_title("|H(W)| = |sin(W/2)|",fontsize=8); a.set_xlabel("W (rad)",fontsize=7); a.tick_params(labelsize=6); a.set_xticks([-np.pi,0,np.pi]); a.set_xticklabels(["-pi","0","pi"])
b.plot(W,np.degrees(np.angle(H)),color="#b00020",lw=1.6); b.set_title("angle H(W) (degrees)",fontsize=8); b.set_xlabel("W (rad)",fontsize=7); b.tick_params(labelsize=6); b.set_xticks([-np.pi,0,np.pi]); b.set_xticklabels(["-pi","0","pi"]); b.set_ylim(-100,100)
fig.tight_layout()
```


The gain is 0 at $\Omega = 0$ (DC is blocked) and rises to 1 at $\Omega = \pi$ (the highest frequency passes): the system is a **high-pass** filter (a first difference, an approximate differentiator). The phase is linear apart from the jump of $\pi$ at $\Omega = 0$ (a constant group delay of 0.5 samples). Check: $\Omega = \pi/2$: $\lvert H\rvert = \sin 45^\circ = 0.707$; directly $0.5\lvert 1 - e^{-j\pi/2}\rvert = 0.5\lvert 1 + j\rvert = 0.707$.
