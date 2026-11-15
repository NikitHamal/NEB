---
file: NEBians-IOE-Past-Paper-Digital-Signal-Processing-and-Application-ENEX304-2082-Chaitra.pdf
subject: Digital Signal Processing and Application
level: BE · Year III / Part I
code: ENEX 304
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Define energy signal and power signal. Is the signal $x[n] = \cos\left(\frac{\pi}{5}n\right)\sin\left(\frac{\pi}{3}n\right)$ periodic? If it is periodic, determine the fundamental period. [[2+2]]

@q 2
Find the output of an LTI system having impulse response $h[n] = \{1, 3, 2, -1, 1\}$ to the input $x[n] = 2\delta[n] - \delta[n-1]$. [[4]]

@q 3
Determine the causal signal $x(n)$ having the z-transform

$$X(z) = \frac{1}{(1+z^{-1})(1-z^{-1})^2}.$$

[[4]]

@q 4
Plot the pole-zero in Z-plane and draw magnitude response (not to the scale) of the system described by difference equation

$$y[n] - 0.4y[n-1] + 0.25y[n-2] = x[n] - 0.4x[n-1].$$

[[2+4]]

@q 5
Compute the lattice-ladder coefficients for the given IIR system:

$$H(z) = \frac{1 + 2z^{-1} + 2z^{-2} + z^{-3}}{1 + \frac{13}{24}z^{-1} + \frac{5}{8}z^{-2} + \frac{1}{3}z^{-3}}.$$

Also, comment on the stability and draw the lattice-ladder structure for the system. [[5+1+2]]

@q 6
Define Gibb's phenomenon. The desired frequency response of a HPF is given by

$$H_d(e^{j\omega}) = \begin{cases} e^{-j3\omega}, & \omega_c \le |\omega| \le \pi \\ 0, & |\omega| < \omega_c \end{cases}$$

Design a linear phase FIR filter using hamming window for $M = 7$ and $\omega_c = 2$ rad/sample. [[2+6]]

@q 7
What do you understand by optimum filter? Describe Remez exchange algorithm for FIR filter design using a flowchart. [[1+3]]

@q 8
Compare and contrast between impulse invariance method and bilinear transformation method. Design a digital IIR low pass filter using bilinear transformation based on Butterworth approximation to meet the following specifications: passband magnitude characteristics that is constant to within 1 dB for frequencies below $\omega = 0.2\pi$ and stopband attenuation of at least 15 dB for frequencies between $\omega = 0.3\pi$ and $\pi$. Use bilinear transformation. [[2+10]]

@q 9
Find 8-point DFT using DIF-FFT of the sequence $x[n] = \{1, 2, 3, 2, 1\}$. [[5]]

@q 10
Discuss the application of DSP in Power System Monitoring and Diagnostics. Perform the circular convolution of the following two sequences $x_1[n] = \{1, 2, 3\}$ and $x_2 = \{1, 2, 3, 4\}$. [[2+3]]
<!-- SOLUTIONS -->

@s 1
**Energy signal.** A signal with finite energy and zero average power:

$$\begin{gathered}E = \sum_{n=-\infty}^{\infty}|x[n]|^2 < \infty \\ P = \lim_{N\to\infty}\frac{1}{2N+1}\sum_{n=-N}^{N}|x[n]|^2 = 0.\end{gathered}$$

Examples: $a^n u[n]$ with $|a|<1$, a finite pulse.

**Power signal.** A signal with finite, non-zero average power ($0<P<\infty$, so $E = \infty$). Periodic signals (for example $\cos\omega_0 n$) are power signals; $P = \frac1N\sum_{n=0}^{N-1}|x[n]|^2$ over one period $N$.

**Periodicity of $x[n]$.** Use $\cos A\sin B = \frac12[\sin(A+B) - \sin(A-B)]$ with $A = \pi n/5$, $B = \pi n/3$:

$$x[n] = \frac12\left[\sin\left(\frac{8\pi}{15}n\right) + \sin\left(\frac{2\pi}{15}n\right)\right]$$

A discrete sinusoid $\sin(2\pi f_0 n)$ is periodic if $f_0$ is a ratio of integers.

- First term: $2\pi f_1 = \frac{8\pi}{15}\Rightarrow f_1 = \frac{4}{15}$, period $N_1 = 15$.
- Second term: $2\pi f_2 = \frac{2\pi}{15}\Rightarrow f_2 = \frac{1}{15}$, period $N_2 = 15$.

Both $f_1$ and $f_2$ are rational, so $x[n]$ **is periodic**, with period equal to the LCM of the two periods:

$$\boxed{N = \text{LCM}(15, 15) = 15\ \text{samples}}$$

Being periodic, it is a power signal with $P = \frac12\cdot\frac14 + \frac12\cdot\frac14 = \frac14$.

@s 2
$x[n] = 2\delta[n] - \delta[n-1] = \{2, -1\}$ (starting at $n=0$) and $h[n] = \{1, 3, 2, -1, 1\}$ (starting at $n = 0$).

Using linearity and time invariance,

$$y[n] = x[n]*h[n] = 2h[n] - h[n-1].$$

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $2h[n]$ | 2 | 6 | 4 | $-2$ | 2 | 0 |
| $-h[n-1]$ | 0 | $-1$ | $-3$ | $-2$ | $1$ | $-1$ |
| $y[n]$ | 2 | 5 | 1 | $-4$ | 3 | $-1$ |

$$\boxed{y[n] = \{2,\ 5,\ 1,\ -4,\ 3,\ -1\}}$$

The output has length $2 + 5 - 1 = 6$, as it must. (Checked by direct polynomial multiplication $(2 - x)(1 + 3x + 2x^2 - x^3 + x^4)$.)

@s 3
Write $w = z^{-1}$ and expand in partial fractions:

$$X = \frac{1}{(1+w)(1-w)^2} = \frac{A}{1+w} + \frac{B}{1-w} + \frac{C}{(1-w)^2}.$$

$$\begin{aligned}A &= \left.\frac{1}{(1-w)^2}\right|_{w=-1} = \frac14\\ C &= \left.\frac{1}{1+w}\right|_{w=1} = \frac12\end{aligned}$$

To find $B$, put $w=0$: $1 = A + B + C \Rightarrow B = 1 - \frac14 - \frac12 = \frac14$.

$$X(z) = \frac{1/4}{1+z^{-1}} + \frac{1/4}{1-z^{-1}} + \frac{1/2}{(1-z^{-1})^2}$$

For a **causal** signal (ROC $|z|>1$) use $\frac{1}{1-az^{-1}}\leftrightarrow a^nu[n]$ and $\frac{1}{(1-z^{-1})^2}\leftrightarrow(n+1)u[n]$:

$$\boxed{x[n] = \left[\frac14(-1)^n + \frac14 + \frac12(n+1)\right]u[n]}$$

Check by long division: $X = 1 + z^{-1} + 2z^{-2} + 2z^{-3} + 3z^{-4} + \dots$. The formula gives $x[0] = \frac14+\frac14+\frac12 = 1$, $x[1] = -\frac14+\frac14+1 = 1$, $x[2] = \frac14+\frac14+\frac32 = 2$, $x[3] = -\frac14+\frac14+2 = 2$. ✓

@s 4
$$H(z) = \frac{1 - 0.4z^{-1}}{1 - 0.4z^{-1} + 0.25z^{-2}} = \frac{z(z - 0.4)}{z^2 - 0.4z + 0.25}$$

**Zeros:** $z = 0.4$ and $z = 0$ (the second one is at the origin, from the factor $z$).

**Poles:** $z^2 - 0.4z + 0.25 = 0$

$$z = \frac{0.4 \pm\sqrt{0.16 - 1}}{2} = 0.2 \pm j\,0.4583 = 0.5\,e^{\pm j66.4^\circ}$$

Both poles have $|z| = 0.5 < 1$, so the system is stable. The poles are close to the unit circle at angle $\pm66.4^\circ$ ($\approx 1.16$ rad), which gives a resonance in the magnitude response, while the zero at $0.4$ gives a dip near $\omega = 0$.

**Magnitude response** $|H(e^{j\omega})| = \dfrac{|e^{j\omega} - 0.4|}{|e^{j\omega} - p_1||e^{j\omega} - p_2|}$ ($|e^{j\omega}| = 1$ for the zero at origin).

| $\omega$ | $0$ | $\pi/3$ | $\pi/2$ | $\pi$ |
|---|---|---|---|---|
| $\lvert H\rvert$ | 0.706 | 1.268 | 1.267 | 0.849 |

The peak is $|H|_{max} = 1.34$ at $\omega \approx 1.29$ rad ($0.41\pi$). So the filter is a weak **band-pass / resonator** with peak near $0.41\pi$.

```figure caption="Pole-zero plot in the z-plane (zero at 0.4 and at the origin, poles at 0.2 ± j0.458) and the magnitude response over 0 to pi (peak 1.34 near 0.41 pi)."
import numpy as np, matplotlib.pyplot as plt
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.6,2.7),gridspec_kw={'width_ratios':[1,1.5]})
t=np.linspace(0,2*np.pi,200); a1.plot(np.cos(t),np.sin(t),color=INK,lw=.8)
a1.plot([0.4,0],[0,0],'o',mfc='none',mec=ACCENT,ms=7); a1.plot([0.2,0.2],[0.4583,-0.4583],'x',color=SERIES[1],ms=8,mew=1.8)
a1.axhline(0,color='#999',lw=.5); a1.axvline(0,color='#999',lw=.5); a1.set_aspect('equal'); a1.set_xlim(-1.3,1.3); a1.set_ylim(-1.3,1.3)
a1.set_xlabel("Re z",fontsize=8); a1.set_ylabel("Im z",fontsize=8); a1.set_title("pole-zero plot",fontsize=8)
w=np.linspace(0,np.pi,500); z=np.exp(1j*w); H=(1-0.4/z)/(1-0.4/z+0.25/z**2)
a2.plot(w/np.pi,abs(H),color=ACCENT); a2.set_xlabel("$\\omega/\\pi$",fontsize=8); a2.set_ylabel("$|H(e^{j\\omega})|$",fontsize=8); a2.set_title("magnitude response",fontsize=8); a2.grid(True)
a2.plot([1.29/np.pi],[1.34],'o',color=SERIES[1],ms=4); a2.text(0.45,1.36,"peak 1.34",fontsize=7)
a2.set_ylim(0,1.6)
```

@s 5
$H(z) = \dfrac{B_3(z)}{A_3(z)}$ with $b = \{1,2,2,1\}$ and $A_3(z) = 1 + \alpha_{3}(1)z^{-1} + \alpha_3(2)z^{-2} + \alpha_3(3)z^{-3}$, $\alpha_3(1) = \frac{13}{24}$, $\alpha_3(2) = \frac58$, $\alpha_3(3) = \frac13$.

**Lattice (reflection) coefficients** by the step-down recursion. $K_m = \alpha_m(m)$ and

$$\alpha_{m-1}(i) = \frac{\alpha_m(i) - K_m\,\alpha_m(m-i)}{1 - K_m^2}.$$

*Order 3:* $K_3 = \alpha_3(3) = \dfrac13$, $1 - K_3^2 = \dfrac89$.

$$\begin{gathered}\alpha_2(1) = \frac{\frac{13}{24} - \frac13\cdot\frac58}{\frac89} = \frac{\frac{8}{24}}{\frac89} = \frac38 \\ \alpha_2(2) = \frac{\frac58 - \frac13\cdot\frac{13}{24}}{\frac89} = \frac{\frac{32}{72}}{\frac89} = \frac12\end{gathered}$$

*Order 2:* $K_2 = \alpha_2(2) = \dfrac12$, $1 - K_2^2 = \dfrac34$.

$$\alpha_1(1) = \frac{\frac38 - \frac12\cdot\frac38}{\frac34} = \frac{\frac{3}{16}}{\frac34} = \frac14$$

*Order 1:* $K_1 = \alpha_1(1) = \dfrac14$.

$$\boxed{K_1 = \tfrac14,\quad K_2 = \tfrac12,\quad K_3 = \tfrac13}$$

**Ladder (feed-forward) coefficients.** $v_m = b_m - \sum_{i=m+1}^{3}v_i\,\alpha_i(i-m)$, starting from $v_3 = b_3$.

$$\begin{aligned}v_3 &= b_3 = 1\\ v_2 &= b_2 - v_3\alpha_3(1) = 2 - \tfrac{13}{24} = \tfrac{35}{24} = 1.4583\\ v_1 &= b_1 - v_2\alpha_2(1) - v_3\alpha_3(2) = 2 - \tfrac{35}{24}\cdot\tfrac38 - \tfrac58 = \tfrac{53}{64} = 0.8281\\ v_0 &= b_0 - v_1\alpha_1(1) - v_2\alpha_2(2) - v_3\alpha_3(3) = 1 - \tfrac{53}{256} - \tfrac{35}{48} - \tfrac13 = -\tfrac{69}{256} = -0.2695\end{aligned}$$

$$\boxed{v_0 = -0.2695,\quad v_1 = 0.8281,\quad v_2 = 1.4583,\quad v_3 = 1}$$

(Verified: simulating the lattice-ladder with an impulse gives $1,\ 1.4583,\ 0.5851,\ -0.5617,\ \dots$, identical to the direct-form impulse response of $H(z)$.)

**Stability.** An all-pole lattice section is stable if and only if every reflection coefficient has magnitude less than 1. Here $|K_1| = 0.25$, $|K_2| = 0.5$, $|K_3| = 0.333$, all less than 1, so **the system is stable** (the poles of $A_3(z)$ have magnitudes $0.789, 0.789, 0.536$, all inside the unit circle).

**Structure.** The IIR lattice (all-pole part, $f_3 = x[n]$) has $f_{m-1}[n] = f_m[n] - K_m g_{m-1}[n-1]$, $g_m[n] = K_m f_{m-1}[n] + g_{m-1}[n-1]$, $g_0 = f_0$, and the ladder output is $y[n] = \sum_{m=0}^{3}v_m g_m[n]$.

```figure caption="Third-order lattice-ladder IIR structure. Upper rail f3 -> f0 (input x[n] at the right), lower rail g0 -> g3 with z^-1 delays, reflection coefficients K1 = 1/4, K2 = 1/2, K3 = 1/3 and ladder taps v0 ... v3 summed into y[n]."
import numpy as np, matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(6.8,3.6)); ax.axis('off'); ax.set_xlim(-1.5,11); ax.set_ylim(-3.2,2)
def arr(p,q,c=INK,lw=1.0): ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="->",color=c,lw=lw))
def ln(p,q): ax.plot([p[0],q[0]],[p[1],q[1]],color=INK,lw=1.0)
def summer(x,y): ax.add_patch(plt.Circle((x,y),0.16,fc='white',ec=INK,lw=1)); ax.text(x,y,"+",ha='center',va='center',fontsize=8)
yt,yb=1.0,-0.6
X=[0,3.2,6.4,9.6]
# vertical joint f0=g0
ln((X[0],yt),(X[0],yb)); ax.plot([X[0]],[yt],'o',color=INK,ms=3); ax.plot([X[0]],[yb],'o',color=INK,ms=3)
ax.text(X[0]-0.1,yt+0.3,"$f_0$",fontsize=8,ha='center'); ax.text(X[0]-0.1,yb-0.4,"$g_0$",fontsize=8,ha='center')
ks=["$K_1$","$K_2$","$K_3$"]; kv=["1/4","1/2","1/3"]
for m in (1,2,3):
    a=X[m-1]; b=X[m]
    # top rail: from f_m (x=b) leftwards through summer at a+1.4 to f_{m-1} at a
    sx=a+1.0
    arr((b,yt),(sx+0.16,yt)); arr((sx-0.16,yt),(a+0.05,yt)); summer(sx,yt)
    # bottom rail: g_{m-1} -> delay -> node D -> summer -> g_m
    ax.add_patch(plt.Rectangle((a+0.35,yb-0.2),0.6,0.4,fc='#eaf1ff',ec=INK,lw=1)); ax.text(a+0.65,yb,"$z^{-1}$",fontsize=7.5,ha='center',va='center')
    ln((a,yb),(a+0.35,yb)); dx=a+1.25; ln((a+0.95,yb),(dx,yb)); ax.plot([dx],[yb],'o',color=INK,ms=3)
    bx=b-1.0; arr((dx,yb),(bx-0.16,yb)); summer(bx,yb); arr((bx+0.16,yb),(b-0.05,yb))
    # up branch from D to top summer with -K
    arr((dx,yb),(sx+0.0,yt-0.16)) if abs(dx-sx)<1e-9 else arr((dx,yb),(sx+0.1,yt-0.15))
    ax.text(sx+0.55,(yt+yb)/2+0.35,"$-K_%d$"%m,fontsize=7.5,ha='center')
    # down branch from top rail point T to bottom summer with +K
    tx=a+0.45; ax.plot([tx],[yt],'o',color=INK,ms=3); arr((tx,yt),(bx-0.1,yb+0.15))
    ax.text(bx-0.9,(yt+yb)/2-0.35,"$K_%d$"%m,fontsize=7.5,ha='center')
    ax.text(b+0.05,yt+0.3,"$f_%d$"%m,fontsize=8,ha='center'); ax.text(b+0.05,yb-0.4,"$g_%d$"%m,fontsize=8,ha='center')
ax.text(X[3]+0.75,yt,"$x[n]$",fontsize=8,va='center'); arr((X[3]+0.7,yt),(X[3]+0.05,yt))
# ladder
yo=-2.5
ln((-1.0,yo),(X[3],yo))
for m in range(4):
    x=X[m]; ln((x,yb),(x,yo+0.45)); ax.add_patch(plt.Rectangle((x-0.3,yo+0.45),0.6,0.36,fc='#fff4e0',ec=INK,lw=1)); ax.text(x,yo+0.63,"$v_%d$"%m,fontsize=7.5,ha='center',va='center')
    arr((x,yo+0.45),(x,yo+0.02))
    if m>0: summer(x,yo) if False else None
    ax.plot([x],[yo],'o',color=INK,ms=3)
arr((X[0]-0.3,yo),(-1.0,yo)); ax.text(-1.45,yo,"$y[n]$",fontsize=8,va='center')
```

@s 6
**Gibbs phenomenon.** When an ideal (infinitely long) impulse response is truncated by a rectangular window to obtain a finite-length FIR filter, the frequency response shows ripples in the passband and stopband. Near the discontinuity (band edge) there is an overshoot of about $9\%$ of the jump (so about $0.09$ for a unit step in $H_d$). Increasing the length $M$ makes the ripples narrower and closer to the edge but does **not** reduce the peak overshoot. It is reduced only by using a smooth window (Hamming, Hanning, Blackman) in place of the rectangular one, at the cost of a wider transition band.

**Design.** $M = 7$, so the delay is $\alpha = \frac{M-1}{2} = 3$ and $H_d(e^{j\omega}) = e^{-j3\omega}$ outside $|\omega| < \omega_c = 2$ rad.

*Ideal impulse response:*

$$h_d[n] = \frac{1}{2\pi}\left[\int_{-\pi}^{-\omega_c}e^{-j3\omega}e^{j\omega n}d\omega + \int_{\omega_c}^{\pi}e^{-j3\omega}e^{j\omega n}d\omega\right] = \frac{\sin\pi(n-3) - \sin\omega_c(n-3)}{\pi(n-3)}$$

$$\begin{gathered}h_d[n] = \delta[n-3] - \frac{\sin 2(n-3)}{\pi(n-3)} \\ h_d[3] = 1 - \frac{\omega_c}{\pi} = 1 - \frac{2}{\pi} = 0.3634\end{gathered}$$

*Hamming window* of length 7:

$$w[n] = 0.54 - 0.46\cos\left(\frac{2\pi n}{6}\right),\quad n = 0,1,\dots,6$$

*Product* $h[n] = h_d[n]\,w[n]$:

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $h_d[n]$ | 0.0296 | 0.1204 | $-0.2894$ | 0.3634 | $-0.2894$ | 0.1204 | 0.0296 |
| $w[n]$ | 0.08 | 0.31 | 0.77 | 1.00 | 0.77 | 0.31 | 0.08 |
| $h[n]$ | 0.0024 | 0.0373 | $-0.2229$ | 0.3634 | $-0.2229$ | 0.0373 | 0.0024 |

$$\boxed{h[n] = \{0.0024,\ 0.0373,\ -0.2229,\ 0.3634,\ -0.2229,\ 0.0373,\ 0.0024\}}$$

The response is symmetric, $h[n] = h[6-n]$, so the filter has exactly linear phase with a delay of 3 samples. Its frequency response is

$$H(e^{j\omega}) = e^{-j3\omega}\left[0.3634 - 0.4458\cos\omega + 0.0746\cos2\omega + 0.0048\cos3\omega\right].$$

```figure caption="Hamming-window HPF design (M = 7, wc = 2 rad/sample): the symmetric impulse response and the amplitude A(w); the response is small below w = 2 and rises to about 1 near w = pi."
import numpy as np, matplotlib.pyplot as plt
h=np.array([0.0024,0.0373,-0.2229,0.3634,-0.2229,0.0373,0.0024]); n=np.arange(7)
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.6,2.5))
a1.stem(n,h,linefmt=ACCENT,markerfmt='o',basefmt=INK); a1.set_xlabel("n",fontsize=8); a1.set_title("h[n]",fontsize=8)
w=np.linspace(0,np.pi,400); A=0.3634-0.4458*np.cos(w)+0.0746*np.cos(2*w)+0.0048*np.cos(3*w)
a2.plot(w,abs(A),color=ACCENT); a2.axvline(2,color=SERIES[1],ls='--',lw=1); a2.text(2.03,0.05,"$\\omega_c=2$",fontsize=7)
a2.set_xlabel("$\\omega$ (rad/sample)",fontsize=8); a2.set_title("$|H(e^{j\\omega})|$",fontsize=8); a2.grid(True)
```

@s 7
**Optimum filter.** A filter whose coefficients are chosen to minimise some error measure between the desired and the actual response. For FIR filters the *optimum (equiripple) filter* minimises the **maximum weighted error** over the passband and stopband (Chebyshev / minimax criterion). The error is spread evenly as ripples of equal height, so for the same order (length) it gives the smallest peak ripple, or for the same ripple the smallest order, compared with window methods. It is designed by the **Parks-McClellan (Remez exchange) algorithm**.

**Remez exchange algorithm.** The amplitude response of a linear-phase FIR filter is a trigonometric polynomial $A(\omega) = \sum_{k=0}^{r}a_k\cos k\omega$. The weighted error is $E(\omega) = W(\omega)\,[H_d(\omega) - A(\omega)]$, with $W = \delta_s/\delta_p$ in the passband to balance the ripples. By the **alternation theorem**, the best $A(\omega)$ has at least $r+2$ alternating extrema of $E(\omega)$ of equal magnitude $\delta$.

Steps (see the flowchart):

1. Specify $\omega_p$, $\omega_s$, $\delta_p$, $\delta_s$, the length $M$ and the weight $W(\omega)$.
2. Guess $r+2$ extremal frequencies $\omega_0 < \omega_1 < \dots < \omega_{r+1}$ (equally spaced in the bands, including the band edges).
3. Solve for the ripple $\delta$ with the closed-form expression, then interpolate $A(\omega)$ (barycentric Lagrange form) through $r+1$ of the points so that $E(\omega_i) = (-1)^i\delta$.
4. Evaluate $E(\omega)$ on a dense frequency grid.
5. If $\max|E(\omega)| > |\delta|$ somewhere, take the $r+2$ largest alternating local extrema of $|E|$ as the new extremal set (the *exchange*) and go back to step 3.
6. If $|E(\omega)| \le |\delta|$ everywhere (the extremal set no longer changes), stop. The ripple $\delta$ is the optimum. Compute $h[n]$ from $A(\omega)$ by an inverse DFT.

```figure caption="Flowchart of the Remez exchange algorithm for equiripple FIR design."
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(6.2,5.0)); ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,12.4)
def box(y,t,w=5.4,h=0.95,fc='#eaf1ff'):
    ax.add_patch(plt.Rectangle((5-w/2,y-h/2),w,h,fc=fc,ec=INK,lw=1)); ax.text(5,y,t,ha='center',va='center',fontsize=7.3)
def arr(p,q): ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="->",color=INK,lw=1))
box(11.7,"Start: specify $\\omega_p,\\omega_s,\\delta_p,\\delta_s$, length $M$, weight $W(\\omega)$",fc='#e8f6ee')
box(10.1,"Choose $r+2$ initial extremal frequencies $\\omega_i$\n(equally spaced in the bands, incl. band edges)")
box(8.5,"Compute ripple $\\delta$ and interpolate $A(\\omega)$\nso that $E(\\omega_i)=(-1)^i\\delta$")
box(6.9,"Evaluate error $E(\\omega)=W(\\omega)[H_d(\\omega)-A(\\omega)]$\non a dense frequency grid")
ax.add_patch(plt.Polygon([[5,5.9],[7.7,4.9],[5,3.9],[2.3,4.9]],fc='#fff4e0',ec=INK,lw=1)); ax.text(5,4.9,"$|E(\\omega)|\\leq|\\delta|$\nfor all $\\omega$ ?",ha='center',va='center',fontsize=7.3)
box(2.6,"Yes: converged. Compute $h[n]$ from $A(\\omega)$\n(inverse DFT) and stop",fc='#e8f6ee')
for a,b in [((5,11.2),(5,10.6)),((5,9.6),(5,9.0)),((5,8.0),(5,7.4)),((5,6.4),(5,5.9)),((5,3.9),(5,3.1))]: arr(a,b)
ax.text(5.2,3.5,"yes",fontsize=7)
ax.add_patch(plt.Rectangle((8.0,4.35),3.6,1.1,fc='#fde8e8',ec=INK,lw=1)); ax.text(9.8,4.9,"No: new extremal set =\n$r+2$ largest peaks of $|E|$",ha='center',va='center',fontsize=7.3)
arr((7.7,4.9),(8.0,4.9)); ax.plot([9.8,9.8],[5.45,8.5],color=INK,lw=1); arr((9.8,8.5),(7.75,8.5)); ax.text(7.75,5.2,"no",fontsize=7)
```

@s 8
**Impulse invariance vs bilinear transformation**

| Feature | Impulse invariance | Bilinear transformation |
|---|---|---|
| Principle | $h[n] = T_s\,h_a(nT_s)$: sample the analog impulse response | Replace $s$ by $\dfrac{2}{T}\dfrac{1-z^{-1}}{1+z^{-1}}$ |
| Mapping | Many-to-one: $z = e^{sT}$, strips of width $2\pi/T$ map onto the whole $z$-plane | One-to-one, the entire $j\Omega$ axis maps to the unit circle once |
| Aliasing | **Present**, because the analog response is not strictly band-limited | **None** |
| Frequency relation | Linear, $\omega = \Omega T$ | Non-linear (warped), $\Omega = \frac{2}{T}\tan\frac\omega2$, needs pre-warping |
| Suitable filters | Only band-limited: low-pass and band-pass. Not high-pass or band-stop | All types (LP, HP, BP, BS) |
| Stability | Preserved | Preserved |
| Phase / shape | Impulse response shape preserved | Magnitude shape preserved only in the piecewise-constant sense |
| Complexity | Partial fractions required | Direct algebraic substitution |

**Design.** Specifications: $\omega_p = 0.2\pi$, $\alpha_p = 1$ dB; $\omega_s = 0.3\pi$, $\alpha_s = 15$ dB. Take $T = 1$ (the digital filter does not depend on $T$).

*Step 1: pre-warp the edges.*

$$\begin{gathered}\Omega_p = \frac{2}{T}\tan\frac{\omega_p}{2} = 2\tan(0.1\pi) = 0.6498\ \text{rad/s} \\ \Omega_s = 2\tan(0.15\pi) = 1.0191\ \text{rad/s}\end{gathered}$$

*Step 2: order.*

$$N \ge \frac{\log\dfrac{10^{0.1\alpha_s}-1}{10^{0.1\alpha_p}-1}}{2\log(\Omega_s/\Omega_p)} = \frac{\log\dfrac{30.623}{0.2589}}{2\log(1.5682)} = \frac{2.0729}{0.3908} = 5.30$$

$$\boxed{N = 6}$$

*Step 3: cut-off.* Meeting the pass-band edge exactly ($\alpha_p = 1$ dB at $\Omega_p$):

$$\Omega_c = \frac{\Omega_p}{(10^{0.1\alpha_p}-1)^{1/2N}} = \frac{0.6498}{(0.2589)^{1/12}} = 0.7273\ \text{rad/s}$$

(the stop-band is then met with margin, because $N$ was rounded up).

*Step 4: analog Butterworth transfer function.* The poles lie on a circle of radius $\Omega_c$ at angles $105^\circ, 135^\circ, 165^\circ$ and their conjugates ($s_k = \Omega_c e^{j\pi(N+2k-1)/2N}$). Pairing conjugates,

$$\begin{gathered}H_a(s) = \prod_{k=1}^{3}\frac{\Omega_c^2}{s^2 + b_ks + \Omega_c^2} \\ b_k = 2\Omega_c\cos\theta_k\end{gathered}$$

with $\Omega_c^2 = 0.5290$ and $b_1 = 2\Omega_c\cos75^\circ = 0.3765$, $b_2 = 2\Omega_c\cos45^\circ = 1.0285$, $b_3 = 2\Omega_c\cos15^\circ = 1.4050$.

*Step 5: bilinear transformation.* Put $s = 2\dfrac{1-z^{-1}}{1+z^{-1}}$ in each section. For a section with $b$:

$$H_k(z) = \frac{\Omega_c^2(1+z^{-1})^2}{(4+2b+\Omega_c^2) + (2\Omega_c^2-8)z^{-1} + (4-2b+\Omega_c^2)z^{-2}}$$

| Section | $b$ | Gain | $a_1$ | $a_2$ |
|---|---|---|---|---|
| 1 | 0.3765 | 0.10014 | $-1.3143$ | 0.7149 |
| 2 | 1.0285 | 0.08031 | $-1.0541$ | 0.3753 |
| 3 | 1.4050 | 0.07207 | $-0.9459$ | 0.2342 |

$$\boxed{H(z) = \frac{0.00058\,(1+z^{-1})^6}{(1 - 1.3143z^{-1} + 0.7149z^{-2})(1 - 1.0541z^{-1} + 0.3753z^{-2})(1 - 0.9459z^{-1} + 0.2342z^{-2})}}$$

*Check.* $|H(e^{j0})| = 0$ dB; at $\omega = 0.2\pi$ the gain is $-1.00$ dB; at $\omega = 0.3\pi$ it is $-17.65$ dB ($\ge 15$ dB required); and it falls to zero at $\omega = \pi$ because of the six zeros at $z = -1$. The specifications are met.

```figure caption="Magnitude response in dB of the 6th-order Butterworth low-pass obtained by the bilinear transformation: -1 dB at 0.2 pi and -17.65 dB at 0.3 pi, meeting the specification."
import numpy as np, matplotlib.pyplot as plt
w=np.linspace(0.001,np.pi,800); z=np.exp(1j*w)
H=0.0005797*(1+1/z)**6
for a1,a2 in [(-1.3143,0.7149),(-1.0541,0.3753),(-0.9459,0.2342)]: H=H/(1+a1/z+a2/z**2)
d=20*np.log10(abs(H)+1e-12)
fig,ax=plt.subplots(figsize=(5.2,2.7)); ax.plot(w/np.pi,d,color=ACCENT)
ax.axhline(-1,color='#999',ls=':',lw=.8); ax.axhline(-15,color='#999',ls=':',lw=.8)
ax.plot([0.2,0.3],[-1,-17.65],'o',color=SERIES[1],ms=4); ax.text(0.21,-3.5,"-1 dB",fontsize=7); ax.text(0.31,-20,"-17.65 dB",fontsize=7)
ax.set_ylim(-60,3); ax.set_xlabel("$\\omega/\\pi$"); ax.set_ylabel("$20\\log|H|$ (dB)"); ax.grid(True)
```

@s 9
$x[n] = \{1,2,3,2,1\}$ is padded with zeros to $N = 8$: $x = \{1,2,3,2,1,0,0,0\}$. $W_8 = e^{-j\pi/4}$, so $W_8^0 = 1$, $W_8^1 = \frac{1-j}{\sqrt2}$, $W_8^2 = -j$, $W_8^3 = \frac{-1-j}{\sqrt2}$.

In decimation in frequency each butterfly takes $a = x[n]$, $b = x[n+N/2]$ and gives $a+b$ and $(a-b)W_N^{n}$.

**Stage 1** ($N/2 = 4$): $g[n] = x[n] + x[n+4]$ and $h[n] = (x[n] - x[n+4])W_8^n$.

| $n$ | $x[n]$ | $x[n+4]$ | $g[n]$ | $x[n]-x[n+4]$ | $h[n]$ |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 2 | 0 | $0$ |
| 1 | 2 | 0 | 2 | 2 | $2W_8 = 1.414 - j1.414$ |
| 2 | 3 | 0 | 3 | 3 | $3W_8^2 = -j3$ |
| 3 | 2 | 0 | 2 | 2 | $2W_8^3 = -1.414 - j1.414$ |

**Stage 2** (two 4-point groups, twiddle $W_8^{2n} = W_4^n$):

| Group | Outputs |
|---|---|
| $g$: $g[0]+g[2]$, $g[1]+g[3]$ | $5,\ 4$ |
| $g$: $(g[0]-g[2])$, $(g[1]-g[3])W_8^2$ | $-1,\ 0$ |
| $h$: $h[0]+h[2]$, $h[1]+h[3]$ | $-j3,\ -j2.828$ |
| $h$: $(h[0]-h[2])$, $(h[1]-h[3])W_8^2$ | $j3,\ -j2.828$ |

**Stage 3** (2-point butterflies, no twiddle): sums and differences of each pair.

| Pair | Sum | Difference | Output index |
|---|---|---|---|
| $5, 4$ | $9$ | $1$ | $X[0]$, $X[4]$ |
| $-1, 0$ | $-1$ | $-1$ | $X[2]$, $X[6]$ |
| $-j3, -j2.828$ | $-j5.828$ | $-j0.172$ | $X[1]$, $X[5]$ |
| $j3, -j2.828$ | $j0.172$ | $j5.828$ | $X[3]$, $X[7]$ |

The outputs come in bit-reversed order ($0,4,2,6,1,5,3,7$), so after re-ordering:

$$\boxed{X[k] = \{9,\ -j5.828,\ -1,\ j0.172,\ 1,\ -j0.172,\ -1,\ j5.828\}}$$

Check: $X[0] = \sum x = 9$ ✓ and $X[4] = \sum(-1)^nx[n] = 1-2+3-2+1 = 1$ ✓. The full 8-point DFT computed independently agrees (conjugate symmetry $X[8-k] = X^*[k]$ holds).

```figure caption="8-point radix-2 DIF-FFT signal-flow graph. Dashed cross branches are subtracted; W^t is the twiddle applied to the difference output. Outputs appear in bit-reversed order."
import numpy as np, matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(6.6,3.8)); ax.axis('off'); ax.set_xlim(-1.3,10.4); ax.set_ylim(-8,0.8)
xs=[0,2.8,5.6,8.4]; N=8
xin=[1,2,3,2,1,0,0,0]
for i in range(N):
    ax.text(xs[0]-0.15,-i,"$x[%d]$=%d"%(i,xin[i]),ha='right',va='center',fontsize=6.5)
for s in range(3):
    span=4>>s
    for i in range(N):
        if (i//span)%2==0:
            j=i+span; t=(i%span)*(N//(2*span))
            ax.plot([xs[s],xs[s+1]],[-i,-i],color=INK,lw=.8); ax.plot([xs[s],xs[s+1]],[-j,-j],color=INK,lw=.8)
            ax.plot([xs[s],xs[s+1]],[-j,-i],color=INK,lw=.8)
            ax.plot([xs[s],xs[s+1]],[-i,-j],color=SERIES[1],lw=.8,ls='--')
            if t>0: ax.text(xs[s+1]-0.35,-j+0.22,"$W^{%d}$"%t,fontsize=6,color=ACCENT,ha='center')
for s in range(4):
    for i in range(N): ax.plot([xs[s]],[-i],'o',color=INK,ms=2.5)
outs=[0,4,2,6,1,5,3,7]; vals=["9","1","-1","-1","-5.83j","-0.17j","0.17j","5.83j"]
for i in range(N): ax.text(xs[3]+0.2,-i,"$X[%d]$=%s"%(outs[i],vals[i]),va='center',fontsize=6.5)
for s,t in enumerate(["stage 1","stage 2","stage 3"]): ax.text((xs[s]+xs[s+1])/2,0.5,t,ha='center',fontsize=7)
```

@s 10
**Application of DSP in power system monitoring and diagnostics**

Modern power systems carry large amounts of voltage and current data from instrument transformers, protection relays, PMUs and smart meters. DSP converts these sampled waveforms into information on the health of the network:

1. **Harmonic and power-quality analysis.** The DFT/FFT of sampled voltage and current gives the harmonic spectrum, THD, inter-harmonics and flicker caused by rectifiers, drives and arc furnaces. This is the basis of power-quality standards (IEEE 519, IEC 61000-4-7) and of the design of passive and active harmonic filters.
2. **Digital protection.** Protective relays sample currents at 1 to 4 kHz. Digital filters (low-pass anti-alias filters, the DFT or cosine filters) extract the fundamental phasor, reject the decaying DC offset and harmonics, and decide on a trip for overcurrent, distance and differential protection.
3. **Fault detection, classification and location.** Wavelet transforms and travelling-wave analysis detect the sharp transient at the start of a fault, classify its type, and locate it from the arrival times of the waves.
4. **Synchrophasor measurement (PMU).** DFT-based estimation of amplitude, phase, frequency and rate of change of frequency, time-stamped by GPS, supports wide-area monitoring and oscillation detection.
5. **Condition monitoring of equipment.** Spectral analysis of vibration, current (motor current signature analysis) and partial-discharge signals diagnoses broken rotor bars, bearing faults, winding insulation ageing and transformer faults (dissolved-gas and frequency-response analysis).
6. **Disturbance detection.** Sags, swells, interruptions and transients are detected by RMS tracking, the Kalman filter or the short-time Fourier transform. Adaptive filters (PLL) track the grid frequency.
7. **Smart grid and forecasting.** Filtering and de-noising of smart-meter data, load forecasting, state estimation and non-intrusive load monitoring.

**Circular convolution.** $x_1[n] = \{1,2,3\}$ has length 3 and $x_2[n] = \{1,2,3,4\}$ has length 4, so the circular convolution is taken with $N = \max(3,4) = 4$ after padding $x_1 = \{1,2,3,0\}$.

$$y[n] = \sum_{m=0}^{3}x_1[m]\,x_2[(n-m)_4]$$

*Matrix (circulant) form:* the columns are cyclic shifts of $x_2$.

$$\begin{bmatrix}y[0]\\y[1]\\y[2]\\y[3]\end{bmatrix} = \begin{bmatrix}1&4&3&2\\2&1&4&3\\3&2&1&4\\4&3&2&1\end{bmatrix}\begin{bmatrix}1\\2\\3\\0\end{bmatrix} = \begin{bmatrix}1+8+9+0\\2+2+12+0\\3+4+3+0\\4+6+6+0\end{bmatrix} = \begin{bmatrix}18\\16\\10\\16\end{bmatrix}$$

$$\boxed{y[n] = \{18,\ 16,\ 10,\ 16\}}$$

*Check:* the linear convolution is $\{1,4,10,16,17,12\}$; wrapping the last two samples onto the first two gives $1+17 = 18$, $4+12 = 16$, then $10$, $16$ ✓. The DFT route ($y = \text{IDFT}[X_1X_2]$) gives the same result.
