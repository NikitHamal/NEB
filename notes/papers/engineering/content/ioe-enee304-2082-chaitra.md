---
file: NEBians-IOE-Past-Paper-Digital-Control-Systems-ENEE304-2082-Chaitra.pdf
subject: Digital Control Systems
level: BE · Year III / Part I
code: ENEE 304
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
a) With the help of block diagram, explain digital control system in detail. Also mention the advantages of digital control system over analog. [[5]]

b) What do you mean by sample and hold circuit? How is tracking and hold mode employed in digital control system? [[3]]

@q 2
a) Obtain the Z-transform of $X(k) = k^2a^{k-1}$. [[4]]

b) Find the inverse z-transform of $X(z) = \dfrac{z^2}{(z-1)^2(z-e^{-aT})}$ by using inversion integral method. [[4]]

c) Solve the following difference equation by use of Z-transform method: $X(k+2) + 3X(k+1) + 2X(k) = 0$, given that $X(0) = 0$, $X(1) = 1$. [[4]]

@q 3
a) What do you mean by data hold circuit? Derive the transfer function of Zero Order Hold (ZOH). [[3]]

b) Consider the digital filter defined by

$$G(z) = \frac{2 + 2.2z^{-1} + 0.2z^{-2}}{1 + 0.4z^{-1} - 0.12z^{-2}}$$

Realize this filter in the ladder scheme. [[5]]

c) Obtain the closed loop transfer function of the system shown in figure below (unity feedback loop: digital PID controller, ZOH and plant $G(s) = \dfrac{1}{s(s+1)}$). Assume proportional gain ($k_p$) = 1, integral gain ($k_i$) = 0.2, derivative gain ($k_d$) = 0.2. [Take $T$ = 1 sec] [[4]]

@q 4
a) Examine the stability of the given characteristic equation using Jury stability test. $P(z) = z^3 + 2.1z^2 + 1.44z + 0.32 = 0$ [[4]]

b) Map the following system in Z-plane. (The S-plane figure shows the shaded rectangle $-2 \le \sigma \le -1$, $-\omega_s/4 \le \omega \le \omega_s/4$, with corners a, b, c, d, e, f: a $(\sigma=-1,\,-\omega_s/4)$, b $(\sigma=-1,\,0)$, c $(\sigma=-1,\,\omega_s/4)$, d $(\sigma=-2,\,\omega_s/4)$, e $(\sigma=-2,\,0)$, f $(\sigma=-2,\,-\omega_s/4)$.) [[3]]

c) Consider a digital control system shown in figure below. The plant is a second order system described as $G(s) = \dfrac{1}{s(s+1)}$. The sampling period of the system is taken to be $T = 1$ s. Design a digital controller such that the dominant closed loop poles of the system will have damping ratio $\zeta = 0.5$ and number of samples per cycle of damped sinusoidal oscillation to be 8. Following the design, obtain the unit step response of the designed system and static velocity error constant $K_v$. [[9]]

@q 5
a) Obtain a state-space representation of the following pulse-transfer-function system in the controllable canonical form.

$$\frac{Y(z)}{U(z)} = \frac{z^{-1} + 2z^{-2}}{1 + 4z^{-1} + 3z^{-2}}$$

[[4]]

b) Obtain the state space representation of the system shown below in Jordan canonical form:

$$\frac{Y(z)}{U(z)} = \frac{5}{(z+1)^2(z+2)}$$

[[4]]

c) Describe Discretization of continuous time state space representation. Obtain the state transition matrix for the discrete time system given below.

$x(k+1) = Gx(k) + Hu(k)$, $y(k) = Cx(k)$, where

$$G = \begin{bmatrix} 0 & 2 \\ -0.2 & -1.5 \end{bmatrix},\quad H = \begin{bmatrix} 1 \\ 1 \end{bmatrix},\quad C = \begin{bmatrix} 1 & 0 \end{bmatrix}$$

[[4]]
<!-- SOLUTIONS -->

@s 1
**(a) Digital control system.** A digital control system is one in which a digital computer (microcontroller, DSP or PLC) works as the controller. The signals in the computer are discrete in time and quantised in amplitude, while the plant is continuous in time, so the loop contains converters.

```figure caption="Block diagram of a digital control system: the continuous error is sampled and quantised by the A/D converter, the digital controller computes the control sequence, and the D/A converter with a hold circuit drives the continuous plant. The sensor closes the loop."
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(6.8,2.7)); ax.axis('off'); ax.set_xlim(0,14); ax.set_ylim(0,5)
def box(x,y,w,h,t,fc='#eaf1ff'):
    ax.add_patch(plt.Rectangle((x,y),w,h,fc=fc,ec=INK,lw=1)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=7)
def arr(p,q): ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="->",color=INK,lw=1))
ax.add_patch(plt.Circle((1.5,3.5),0.3,fc='white',ec=INK)); ax.text(1.5,3.5,"$\\Sigma$",ha='center',va='center',fontsize=8)
ax.text(0.9,3.85,"+",fontsize=8); ax.text(1.7,2.85,"$-$",fontsize=8)
arr((0.2,3.5),(1.2,3.5)); ax.text(0.1,3.8,"$r(t)$",fontsize=8)
box(2.5,3.0,1.8,1.0,"Sampler\nA/D converter"); box(5.1,3.0,2.2,1.0,"Digital controller\n(computer) $D(z)$",fc='#fff4e0')
box(8.1,3.0,1.8,1.0,"D/A converter\n+ hold (ZOH)"); box(10.6,3.0,1.7,1.0,"Plant\n$G(s)$")
arr((1.8,3.5),(2.5,3.5)); ax.text(2.0,3.7,"$e(t)$",fontsize=7); arr((4.3,3.5),(5.1,3.5)); ax.text(4.35,3.7,"$e(k)$",fontsize=7)
arr((7.3,3.5),(8.1,3.5)); ax.text(7.35,3.7,"$u(k)$",fontsize=7); arr((9.9,3.5),(10.6,3.5)); ax.text(9.95,3.7,"$u(t)$",fontsize=7)
arr((12.3,3.5),(13.5,3.5)); ax.text(12.7,3.7,"$y(t)$",fontsize=8)
box(5.9,0.8,2.2,0.9,"Sensor / transducer")
ax.plot([13.0,13.0,8.1],[3.5,1.25,1.25],color=INK,lw=1); ax.plot([13.0],[3.5],'o',color=INK,ms=3)
ax.plot([5.9,1.5,1.5],[1.25,1.25,3.2],color=INK,lw=1); arr((1.5,1.25),(1.5,3.2))
```

*Working.* The reference and the measured output are compared, the error is sampled at period $T$ by the sampler and converted to a binary number by the A/D converter. The control algorithm (for example PID, lead-lag or state feedback) is executed by the computer once per sampling period and produces the control sequence $u(k)$. The D/A converter and the hold circuit turn it into a piecewise-constant signal $u(t)$ that drives the actuator and plant. The sensor feeds the output back.

**Advantages over analog control**

1. **Flexibility:** changing the controller needs only a change of software, not of hardware components.
2. **Complex algorithms:** adaptive, optimal, nonlinear and multivariable control are possible.
3. **High accuracy and no drift:** the digital arithmetic is not affected by ageing, temperature or component tolerance.
4. **Noise immunity:** digital signals are less sensitive to noise during processing and transmission.
5. **Cost and size:** one computer can control several loops by time sharing; it is compact and cheap with the microprocessor.
6. **Easy supervision:** data logging, display, networking, self-diagnosis and communication with other systems.
7. **Reliability and repeatability** of the controller (no component variation from unit to unit).

(Disadvantages: sampling reduces the stability margin, quantisation error and time delay, and the A/D, D/A converters are required.)

**(b) Sample and hold circuit.** A sample-and-hold (S/H) circuit samples the continuous signal at the sampling instant $kT$ and holds that value constant for the sampling period (the conversion time of the A/D converter). It consists of an electronic switch (a FET or an analog switch), a hold capacitor and a buffer op-amp.

*Tracking (sample) mode:* the switch is closed, the capacitor charges and the output **follows (tracks)** the input signal. *Hold mode:* on the sampling command the switch opens, and the capacitor holds the voltage that existed at that instant, so the output is a constant while the A/D converter converts it to a binary number. The cycle repeats every $T$.

In a digital control system the S/H circuit makes the input of the A/D converter constant during conversion (otherwise the code would be wrong for a changing signal), and at the output of the D/A it holds the controller value until the next sample (the zero-order hold).

```figure caption="Operation of a sample-and-hold circuit: the output tracks the input during the sampling (tracking) interval and then holds the last value until the next sample."
import numpy as np, matplotlib.pyplot as plt
t=np.linspace(0,10,1000); x=2+1.6*np.sin(0.8*t)+0.6*np.sin(2.1*t)
T=1.25; out=np.zeros_like(t)
for i,tt in enumerate(t):
    ph=tt%T
    out[i]=x[i] if ph<0.25 else np.interp(tt-(ph-0.25),t,x)
fig,ax=plt.subplots(figsize=(5.8,2.5)); ax.plot(t,x,color='#aaa',lw=1,label="input $x(t)$"); ax.plot(t,out,color=ACCENT,lw=1.5,label="S/H output")
for k in range(0,8): ax.axvspan(k*T,k*T+0.25,color=SERIES[1],alpha=.12)
ax.text(0.02,0.1,"shaded = tracking, unshaded = hold",fontsize=7,transform=ax.transAxes); ax.set_xlabel("t"); ax.legend(fontsize=7,loc="upper right"); ax.grid(True)
```

@s 2
**(a)** Start from the geometric sequence and use the rule $\mathcal Z[k\,x(k)] = -z\dfrac{d}{dz}X(z)$.

$$\mathcal Z[a^k] = \frac{z}{z-a}$$

$$\mathcal Z[k\,a^k] = -z\frac{d}{dz}\left(\frac{z}{z-a}\right) = -z\cdot\frac{(z-a)-z}{(z-a)^2} = \frac{az}{(z-a)^2}$$

$$\mathcal Z[k^2a^k] = -z\frac{d}{dz}\left[\frac{az}{(z-a)^2}\right] = -z\cdot a\frac{(z-a)^2 - 2z(z-a)}{(z-a)^4} = \frac{az(z+a)}{(z-a)^3}$$

Since $X(k) = k^2a^{k-1} = \dfrac1a\,k^2a^k$,

$$\boxed{X(z) = \frac{z(z+a)}{(z-a)^3}}$$

(Check by series: $X(k)$ is $0, 1, 4a, 9a^2,\dots$ and $z(z+a)/(z-a)^3 = z^{-1} + 4az^{-2} + 9a^2z^{-3}+\dots$ ✓.)

**(b) Inversion integral method.** $x(k) = \sum\text{residues of }X(z)z^{k-1}$ at the poles of $X(z)z^{k-1}$. Let $b = e^{-aT}$.

$$X(z)z^{k-1} = \frac{z^{k+1}}{(z-1)^2(z-b)}$$

*Simple pole at $z = b$:*

$$K_1 = \left.\frac{z^{k+1}}{(z-1)^2}\right|_{z=b} = \frac{b^{k+1}}{(1-b)^2}$$

*Double pole at $z = 1$:* $K_2 = \dfrac{d}{dz}\left[\dfrac{z^{k+1}}{z-b}\right]_{z=1} = \left[\dfrac{(k+1)z^k(z-b) - z^{k+1}}{(z-b)^2}\right]_{z=1} = \dfrac{(k+1)(1-b) - 1}{(1-b)^2}$

$$K_2 = \frac{k+1}{1-b} - \frac{1}{(1-b)^2}$$

Sum:

$$x(k) = K_1 + K_2 = \frac{k+1}{1-b} - \frac{1-b^{k+1}}{(1-b)^2}$$

$$\boxed{x(k) = \frac{k+1}{1-e^{-aT}} - \frac{1 - e^{-a(k+1)T}}{(1-e^{-aT})^2},\quad k = 0,1,2,\dots}$$

Check: $x(0) = \frac{1}{1-b} - \frac{1-b}{(1-b)^2} = 0$ ✓ and $x(1) = \frac{2}{1-b} - \frac{1-b^2}{(1-b)^2} = \frac{2-(1+b)}{1-b} = 1$ ✓.

**(c)** Take the $z$-transform with $\mathcal Z[x(k+2)] = z^2X(z) - z^2x(0) - zx(1)$ and $\mathcal Z[x(k+1)] = zX(z) - zx(0)$:

$$z^2X(z) - z\cdot1 + 3zX(z) + 2X(z) = 0\ \ (x(0)=0,\ x(1)=1)$$

$$X(z) = \frac{z}{z^2+3z+2} = \frac{z}{(z+1)(z+2)}$$

Partial fractions of $X(z)/z = \dfrac{1}{(z+1)(z+2)} = \dfrac{1}{z+1} - \dfrac{1}{z+2}$:

$$X(z) = \frac{z}{z+1} - \frac{z}{z+2}$$

$$\boxed{x(k) = (-1)^k - (-2)^k}$$

Check: $x(0) = 0$, $x(1) = -1+2 = 1$, and from the equation $x(2) = -3x(1)-2x(0) = -3$, while the formula gives $1-4 = -3$ ✓. The sequence is $0, 1, -3, 7, -15,\dots$ and it diverges, since the pole at $z = -2$ is outside the unit circle.

@s 3
**(a) Data hold.** A data hold (reconstruction) circuit converts the discrete-time sampled sequence $x(kT)$ into a continuous-time signal $x_h(t)$, by extrapolating between samples using the previous sample values. The **zero-order hold (ZOH)** holds the last sample value constant over the whole sampling period: $x_h(kT + \tau) = x(kT)$ for $0\le\tau<T$.

*Derivation.* The impulse response of the ZOH is a unit-height rectangular pulse of width $T$:

$$g_h(t) = u_s(t) - u_s(t-T)$$

where $u_s$ is the unit step. Taking the Laplace transform,

$$G_h(s) = \frac1s - \frac{e^{-Ts}}{s}$$

$$\boxed{G_h(s) = \frac{1-e^{-Ts}}{s}}$$

*Frequency response.* With $s = j\omega$,

$$G_h(j\omega) = \frac{1-e^{-j\omega T}}{j\omega} = T\,\frac{\sin(\omega T/2)}{\omega T/2}\,e^{-j\omega T/2}$$

so the ZOH is a low-pass filter of gain $T$ at $\omega = 0$, with zeros at multiples of the sampling frequency $\omega_s = 2\pi/T$ and a **delay of $T/2$**, which reduces the phase margin of the loop.

**(b) Ladder realization.** Multiply numerator and denominator by $z^2$:

$$G(z) = \frac{2z^2 + 2.2z + 0.2}{z^2 + 0.4z - 0.12} = \frac{2(z+1)(z+0.1)}{(z+0.6)(z-0.2)}$$

Ladder (continued-fraction) realization: expand $G(z)$ by repeated division, taking out the highest power of $z$ each time.

*Step 1:* $G(z) = 2 + \dfrac{1.4z + 0.44}{z^2+0.4z-0.12} = 2 + \dfrac{1}{P_1(z) + \cdots}$. Divide $z^2 + 0.4z - 0.12$ by $1.4z + 0.44$:

$$\frac{z^2+0.4z-0.12}{1.4z+0.44} = 0.7143z + \frac{0.0857z - 0.12}{1.4z+0.44}$$

*Step 2:* $\dfrac{1.4z+0.44}{0.0857z-0.12} = 16.333 + \dfrac{2.4}{0.0857z-0.12}$ and $\dfrac{0.0857z-0.12}{2.4} = 0.035714z - 0.05$.

Therefore

$$\boxed{G(z) = 2 + \cfrac{1}{0.7143z + \cfrac{1}{16.333 + \cfrac{1}{0.035714z - 0.05}}}}$$

Write $P_1 = 0.7143z$, $P_2 = 16.333$, $P_3 = 0.035714z - 0.05$. The ladder equations (series and shunt branches alternate) are

$$\begin{gathered}Y = 2U + X_1 \\ P_1X_1 = U - X_2 \\ P_2X_2 = X_1 - X_3 \\ P_3X_3 = X_2\end{gathered}$$

Dividing by the $z$-terms (each $z$ on the left means one delay $z^{-1}$ on the right) gives the difference equations for the two delay elements $x_1$ and $x_3$:

$$\begin{aligned}x_2(k) &= \frac{x_1(k) - x_3(k)}{16.333} = 0.06122\,[x_1(k) - x_3(k)]\\ x_1(k+1) &= 1.4\,[u(k) - x_2(k)]\\ x_3(k+1) &= 28\,x_2(k) + 1.4\,x_3(k)\\ y(k) &= 2u(k) + x_1(k)\end{aligned}$$

*Check:* simulating these equations with a unit impulse gives $y = 2,\ 1.4,\ -0.12,\ 0.216,\ -0.1008,\ 0.0662,\dots$, identical to the impulse response of $G(z)$ obtained from the difference equation $y(k) = -0.4y(k-1) + 0.12y(k-2) + 2u(k) + 2.2u(k-1) + 0.2u(k-2)$. The realization uses only **two delays** (the minimum for second order).

```figure caption="Ladder realization of G(z): two delay elements (outputs x1 and x3), gains 1.4, 0.06122 and 28, and a gain 1.4 around the second delay. Signs at the summing junctions are marked."
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(6.8,3.6)); ax.axis('off'); ax.set_xlim(0,14.2); ax.set_ylim(-1.7,6.6)
def arr(p,q): ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="->",color=INK,lw=1))
def ln(xs,ys): ax.plot(xs,ys,color=INK,lw=1)
def dot(x,y): ax.plot([x],[y],'o',color=INK,ms=3)
def box(x,y,w,h,t,fc='#eaf1ff'):
    ax.add_patch(plt.Rectangle((x,y),w,h,fc=fc,ec=INK,lw=1)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=7.5)
def summ(x,y):
    ax.add_patch(plt.Circle((x,y),0.28,fc='white',ec=INK)); ax.text(x,y,"$\\Sigma$",ha='center',va='center',fontsize=7)
ax.text(0.0,4.85,"$u(k)$",fontsize=8); arr((0.1,4.5),(1.3,4.5)); dot(0.8,4.5)
summ(1.6,4.5); ax.text(1.1,4.8,"+",fontsize=8); ax.text(1.75,3.85,"$-$",fontsize=9)
arr((1.9,4.5),(2.6,4.5)); box(2.6,4.1,1.1,0.8,"1.4"); arr((3.7,4.5),(4.4,4.5)); box(4.4,4.1,1.0,0.8,"$z^{-1}$",fc='#fff4e0')
ln([5.4,6.0],[4.5,4.5]); dot(6.0,4.5); ax.text(5.55,4.8,"$x_1$",fontsize=8)
arr((6.0,4.5),(10.7,4.5)); summ(11.0,4.5); ax.text(10.5,4.8,"+",fontsize=8); ax.text(11.15,5.2,"+",fontsize=8)
arr((11.3,4.5),(13.0,4.5)); ax.text(12.0,4.8,"$y(k)$",fontsize=8)
ln([0.8,0.8,6.5],[4.5,6.0,6.0]); box(6.5,5.65,1.0,0.7,"2"); ln([7.5,11.0],[6.0,6.0]); arr((11.0,6.0),(11.0,4.8))
ln([6.0,6.0],[4.5,2.8]); arr((6.0,2.9),(6.0,2.8)); summ(6.0,2.5); ax.text(5.35,2.75,"+",fontsize=8); ax.text(6.15,1.85,"$-$",fontsize=9)
arr((6.3,2.5),(7.2,2.5)); box(7.2,2.1,1.5,0.8,"0.06122"); ln([8.7,9.6],[2.5,2.5]); dot(9.6,2.5); ax.text(9.0,2.8,"$x_2$",fontsize=8)
ln([9.6,9.6,1.6],[2.5,3.4,3.4]); arr((1.6,3.4),(1.6,4.2))
ln([9.6,9.6],[2.5,0.8]); arr((9.6,0.8),(10.2,0.8)); box(10.2,0.4,0.9,0.8,"28"); arr((11.1,0.8),(11.9,0.8)); summ(12.2,0.8)
ax.text(11.75,1.15,"+",fontsize=8); ax.text(12.35,0.2,"+",fontsize=8)
arr((12.5,0.8),(12.9,0.8)); box(12.9,0.4,0.9,0.8,"$z^{-1}$",fc='#fff4e0'); ln([13.8,14.1],[0.8,0.8]); dot(14.1,0.8); ax.text(13.5,1.3,"$x_3$",fontsize=8)
ln([14.1,14.1],[0.8,-0.3]); ln([14.1,12.2],[-0.3,-0.3]); box(12.6,-0.65,1.0,0.7,"1.4") if False else None
ax.add_patch(plt.Rectangle((12.9,-0.65),0.9,0.7,fc='#eaf1ff',ec=INK,lw=1)); ax.text(13.35,-0.3,"1.4",ha='center',va='center',fontsize=7.5)
arr((12.2,-0.3),(12.2,0.52))
ln([14.1,14.1],[-0.3,-1.2]); ln([14.1,6.0],[-1.2,-1.2]); arr((6.0,-1.2),(6.0,2.2))
```

**(c) Closed-loop transfer function.** $T = 1$ s, $k_p = 1$, $k_i = 0.2$, $k_d = 0.2$.

*Plant with ZOH.*

$$\begin{gathered}G(z) = (1-z^{-1})\mathcal Z\left[\frac{1}{s^2(s+1)}\right] \\ \frac{1}{s^2(s+1)} = \frac{1}{s^2} - \frac1s + \frac{1}{s+1}\end{gathered}$$

$$G(z) = \frac{(T - 1 + e^{-T})z + (1 - e^{-T} - Te^{-T})}{(z-1)(z-e^{-T})} = \frac{0.3679z + 0.2642}{(z-1)(z-0.3679)} = \frac{0.3679(z+0.7183)}{(z-1)(z-0.3679)}$$

*Digital PID controller* (rectangular integration, backward difference):

$$D(z) = k_p + k_i\frac{Tz}{z-1} + k_d\frac{z-1}{Tz} = \frac{k_pz(z-1) + k_iTz^2 + k_d(z-1)^2}{z(z-1)}$$

$$D(z) = \frac{(1)z(z-1) + (0.2)(1)z^2 + (0.2)(z-1)^2}{z(z-1)}$$

Collecting terms ($z^2$: $1 + 0.2 + 0.2 = 1.4$; $z$: $-1 - 0.4 = -1.4$; constant: $0.2$):

$$D(z) = \frac{1.4z^2 - 1.4z + 0.2}{z(z-1)}$$

*Open loop:*

$$D(z)G(z) = \frac{(1.4z^2 - 1.4z + 0.2)(0.3679z + 0.2642)}{z(z-1)^2(z-0.3679)} = \frac{0.5150z^3 - 0.1451z^2 - 0.2964z + 0.0529}{z^4 - 2.3679z^3 + 1.7358z^2 - 0.3679z}$$

*Closed loop* $\dfrac{Y(z)}{R(z)} = \dfrac{DG}{1+DG}$:

$$\boxed{\frac{Y(z)}{R(z)} = \frac{0.5150z^3 - 0.1451z^2 - 0.2964z + 0.0529}{z^4 - 1.8529z^3 + 1.5907z^2 - 0.6642z + 0.0529}}$$

The closed-loop poles are $0.476\pm j0.652$ ($|z| = 0.807$), $0.799$ and $0.101$, all inside the unit circle, so the loop is stable. The DC gain is $1$ (the integrator gives zero steady-state error to a step).

@s 4
**(a) Jury test.** $P(z) = a_3z^3 + a_2z^2 + a_1z + a_0$ with $a_3 = 1$, $a_2 = 2.1$, $a_1 = 1.44$, $a_0 = 0.32$, $n = 3$.

*Necessary conditions*

1. $P(1) = 1 + 2.1 + 1.44 + 0.32 = 4.86 > 0$ ✓
2. $(-1)^3P(-1) = -(-1 + 2.1 - 1.44 + 0.32) = -(-0.02) = 0.02 > 0$ ✓
3. $|a_0| < a_3$: $0.32 < 1$ ✓

*Jury table* (with $b_k = a_0a_k - a_na_{n-k}$):

| Row | $z^0$ | $z^1$ | $z^2$ | $z^3$ |
|---|---|---|---|---|
| 1 | $0.32$ | $1.44$ | $2.1$ | $1$ |
| 2 | $1$ | $2.1$ | $1.44$ | $0.32$ |
| 3 | $b_0 = -0.8976$ | $b_1 = -1.6392$ | $b_2 = -0.7680$ | |

$$b_0 = a_0^2 - a_3^2 = 0.1024 - 1 = -0.8976,\quad b_1 = a_0a_1 - a_3a_2 = 0.4608 - 2.1 = -1.6392,\quad b_2 = a_0a_2 - a_3a_1 = 0.672 - 1.44 = -0.768$$

*Fourth condition:* $|b_0| > |b_{n-1}| = |b_2|$: $0.8976 > 0.768$ ✓

All the Jury conditions hold, so **all the roots lie inside the unit circle and the system is stable**.

Check: $P(z) = (z+0.5)(z+0.8)^2$, so the roots are $-0.5$, $-0.8$, $-0.8$, with $|z|<1$ ✓.

**(b) Mapping the S-plane strip into the Z-plane.** Use $z = e^{sT}$ with $s = \sigma + j\omega$ and $T = 2\pi/\omega_s$, so $|z| = e^{\sigma T}$ and $\angle z = \omega T$.

- Vertical lines $\sigma = -1$ and $\sigma = -2$ map to circles of radius $e^{-T}$ and $e^{-2T}$ with the centre at the origin (inside the unit circle, because $\sigma<0$).
- The limits $\omega = \pm\omega_s/4$ map to angles $\omega T = \pm\dfrac{\omega_s}{4}\cdot\dfrac{2\pi}{\omega_s} = \pm\dfrac{\pi}{2} = \pm90^\circ$.
- $\omega = 0$ maps to the positive real axis.

| Point | $s$ | $z = e^{sT}$ |
|---|---|---|
| a | $-1 - j\omega_s/4$ | $e^{-T}\angle{-90^\circ}$ |
| b | $-1$ | $e^{-T}\angle0^\circ$ |
| c | $-1 + j\omega_s/4$ | $e^{-T}\angle{+90^\circ}$ |
| d | $-2 + j\omega_s/4$ | $e^{-2T}\angle{+90^\circ}$ |
| e | $-2$ | $e^{-2T}\angle0^\circ$ |
| f | $-2 - j\omega_s/4$ | $e^{-2T}\angle{-90^\circ}$ |

The shaded rectangle becomes the **annular sector** between the circles $|z| = e^{-2T}$ and $|z| = e^{-T}$, bounded by the rays at $\pm90^\circ$ (the right half of the annulus, in the first and fourth quadrants). For example, for $T = 1$ s the radii are $0.368$ and $0.135$.

```figure caption="Mapping of the shaded S-plane strip (-2 <= sigma <= -1, |omega| <= omega_s/4) into the z-plane by z = exp(sT): the annular sector between radii e^-2T and e^-T within +/- 90 degrees. Corner points a to f are marked in both planes."
import numpy as np, matplotlib.pyplot as plt
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.8,3.0))
a1.fill([-2,-1,-1,-2],[-1,-1,1,1],color=ACCENT,alpha=.3); a1.axhline(0,color='#888',lw=.7); a1.axvline(0,color='#888',lw=.7)
for n,(x,y) in dict(a=(-1,-1),b=(-1,0),c=(-1,1),d=(-2,1),e=(-2,0),f=(-2,-1)).items(): a1.plot([x],[y],'o',color=INK,ms=3); a1.text(x+(0.07 if x==-1 else -0.2),y+0.05,n,fontsize=8)
a1.set_xlim(-2.8,0.8); a1.set_ylim(-1.5,1.5); a1.set_xticks([-2,-1,0]); a1.set_xticklabels(["-2","-1","0"]); a1.set_yticks([-1,0,1]); a1.set_yticklabels(["$-\\omega_s/4$","0","$\\omega_s/4$"])
a1.set_title("s-plane",fontsize=8); a1.set_xlabel("$\\sigma$",fontsize=8)
T=1; r1,r2=np.exp(-1*T),np.exp(-2*T)
t=np.linspace(0,2*np.pi,200); a2.plot(np.cos(t),np.sin(t),color='#999',lw=.8)
th=np.linspace(-np.pi/2,np.pi/2,100)
xs=np.r_[r1*np.cos(th),r2*np.cos(th[::-1])]; ys=np.r_[r1*np.sin(th),r2*np.sin(th[::-1])]
a2.fill(xs,ys,color=ACCENT,alpha=.3,ec=INK)
pts=dict(a=(0,-r1),b=(r1,0),c=(0,r1),d=(0,r2),e=(r2,0),f=(0,-r2))
for n,(x,y) in pts.items(): a2.plot([x],[y],'o',color=INK,ms=3)
a2.text(0.03,-r1-0.12,"a",fontsize=8); a2.text(r1+0.03,0.03,"b",fontsize=8); a2.text(0.03,r1+0.05,"c",fontsize=8); a2.text(-0.12,r2+0.0,"d",fontsize=8); a2.text(r2-0.1,0.05,"e",fontsize=8); a2.text(-0.12,-r2-0.1,"f",fontsize=8)
a2.axhline(0,color='#888',lw=.7); a2.axvline(0,color='#888',lw=.7); a2.set_aspect('equal'); a2.set_xlim(-1.2,1.2); a2.set_ylim(-1.2,1.2); a2.set_title("z-plane  (radii $e^{-T}$, $e^{-2T}$)",fontsize=8)
```

**(c) Design of the digital controller (pole placement by the root-locus angle condition).** Plant with ZOH, $T = 1$ s (from Q3):

$$G(z) = \frac{0.3679(z+0.7183)}{(z-1)(z-0.3679)}$$

*Step 1: desired dominant closed-loop poles.* Eight samples per damped cycle means $\omega_dT = \dfrac{2\pi}{8} = 45^\circ$, so $\omega_d = 0.7854$ rad/s. With $\zeta = 0.5$:

$$\begin{gathered}\omega_n = \frac{\omega_d}{\sqrt{1-\zeta^2}} = \frac{0.7854}{0.8660} = 0.9069\ \text{rad/s} \\ \sigma = \zeta\omega_n = 0.4534\end{gathered}$$

$$z_{1,2} = e^{-\sigma T}\angle\pm\omega_dT = e^{-0.4534}\angle\pm45^\circ = 0.6354\angle\pm45^\circ = 0.4493\pm j0.4493$$

*Step 2: angle deficiency.* At $z_1 = 0.4493 + j0.4493$:

| Factor | Angle contribution |
|---|---|
| zero at $-0.7183$ | $+21.05^\circ$ |
| pole at $1$ | $-140.80^\circ$ |
| pole at $0.3679$ | $-79.67^\circ$ |
| **Sum** | $-199.47^\circ$ |

The condition requires $-180^\circ$, so the controller must give $+19.47^\circ$ (a phase **lead**). Choose a lead controller whose zero **cancels the plant pole at $0.3679$** (which keeps the system order low):

$$D(z) = K\,\frac{z - 0.3679}{z - \beta}$$

Without the pole at 0.3679 the angle of the loop is $21.05^\circ - 140.80^\circ = -119.75^\circ$, so the pole at $\beta$ must give $-60.25^\circ$, that is, $\angle(z_1 - \beta) = 60.25^\circ$:

$$0.4493 - \beta = \frac{0.4493}{\tan60.25^\circ} = 0.2567\ \Rightarrow\ \beta = 0.1926$$

*Step 3: gain from the magnitude condition* $|D(z_1)G(z_1)| = 1$:

$$K = \frac{|z_1 - 1|\,|z_1 - \beta|}{0.3679\,|z_1 + 0.7183|} = \frac{(0.7107)(0.5175)}{(0.3679)(1.2511)} = 0.7991$$

with $|z_1-1| = 0.7107$, $|z_1-0.1926| = 0.5175$ and $|z_1+0.7183| = 1.2511$.

$$\boxed{D(z) = 0.7991\,\frac{z - 0.3679}{z - 0.1926}}$$

*Check.* The open loop is

$$D(z)G(z) = \frac{0.2940(z+0.7183)}{(z-1)(z-0.1926)} = \frac{0.2940z + 0.2112}{z^2 - 1.1926z + 0.1926}$$

and the closed-loop characteristic equation is

$$z^2 - 1.1926z + 0.1926 + 0.2940z + 0.2112 = z^2 - 0.8986z + 0.4038 = 0$$

whose roots are $0.4493\pm j0.4493$ ✓. They are exactly the desired poles.

*Closed-loop transfer function.*

$$\frac{Y(z)}{R(z)} = \frac{0.2940z + 0.2112}{z^2 - 0.8986z + 0.4038}$$

*Unit step response.* For $R(z) = \dfrac{z}{z-1}$, solve the difference equation $y(k) = 0.8986y(k-1) - 0.4038y(k-2) + 0.2940r(k-1) + 0.2112r(k-2)$ with $r(k) = 1$:

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $y(k)$ | 0 | 0.2940 | 0.7693 | 1.0778 | **1.1630** | 1.1151 | 1.0376 | 0.9873 | 0.9734 | 0.9812 | 0.9939 |

The response peaks at $k = 4$ ($t = 4$ s) with $y_{max} = 1.163$, a **maximum overshoot of about 16.3%**, as expected for $\zeta = 0.5$ ($e^{-\pi\zeta/\sqrt{1-\zeta^2}} = 16.3\%$). The output settles to $1$ (the final value is $\dfrac{0.2940+0.2112}{1 - 0.8986 + 0.4038} = 1.000$, zero steady-state error to a step because of the pole at $z=1$), with a period of 8 samples.

*Static velocity error constant.*

$$K_v = \frac1T\lim_{z\to1}(z-1)D(z)G(z) = \frac{0.2940(1+0.7183)}{1-0.1926} = \frac{0.5051}{0.8074}$$

$$\boxed{K_v = 0.626\ \text{s}^{-1}}$$

The steady-state error to a unit ramp is $e_{ss} = 1/K_v = 1.60$.

```figure caption="Unit-step response of the designed system (8 samples per cycle, 16.3% overshoot) and the closed-loop poles 0.449 +/- j0.449 in the z-plane."
import numpy as np, matplotlib.pyplot as plt
y=[0,0.2940,0.7693,1.0778,1.1630,1.1151,1.0376,0.9873,0.9734,0.9812,0.9939,1.0021,1.0043,1.0031,1.0010,0.9997]
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.6,2.6),gridspec_kw={'width_ratios':[1.6,1]})
k=np.arange(len(y)); a1.stem(k,y,linefmt=ACCENT,markerfmt='o',basefmt=INK); a1.axhline(1,color='#999',ls=':',lw=.8); a1.plot([4],[1.163],'o',color=SERIES[1],ms=6,mfc='none')
a1.text(4.5,1.17,"peak 1.163",fontsize=7); a1.set_xlabel("sample $k$ (T = 1 s)",fontsize=8); a1.set_ylabel("$y(k)$",fontsize=8); a1.grid(True)
t=np.linspace(0,2*np.pi,200); a2.plot(np.cos(t),np.sin(t),color='#999',lw=.8); a2.plot([0.4493,0.4493],[0.4493,-0.4493],'x',color=SERIES[1],ms=8,mew=1.8)
a2.plot([0.3679,0.1926,-0.7183],[0,0,0],'o',mfc='none',mec=ACCENT,ms=5)
a2.axhline(0,color='#888',lw=.6); a2.axvline(0,color='#888',lw=.6); a2.set_aspect('equal'); a2.set_xlim(-1.2,1.2); a2.set_ylim(-1.2,1.2); a2.set_title("z-plane",fontsize=8)
```

@s 5
**(a) Controllable canonical form.** Multiply numerator and denominator by $z^2$:

$$\frac{Y(z)}{U(z)} = \frac{z+2}{z^2 + 4z + 3}$$

With $n = 2$, $a_1 = 4$, $a_2 = 3$ and numerator $b_0 = 0$, $b_1 = 1$, $b_2 = 2$ (of the form $b_0z^2 + b_1z + b_2$). Choose the states $x_1(k)$ and $x_2(k) = x_1(k+1)$:

$$\begin{gathered}x_1(k+1) = x_2(k) \\ x_2(k+1) = -3x_1(k) - 4x_2(k) + u(k)\end{gathered}$$

$$\boxed{\begin{bmatrix}x_1(k+1)\\x_2(k+1)\end{bmatrix} = \begin{bmatrix}0&1\\-3&-4\end{bmatrix}\begin{bmatrix}x_1(k)\\x_2(k)\end{bmatrix} + \begin{bmatrix}0\\1\end{bmatrix}u(k)}$$

$$\boxed{y(k) = \begin{bmatrix}2&1\end{bmatrix}\begin{bmatrix}x_1(k)\\x_2(k)\end{bmatrix}}$$

The output matrix is $[\,b_2 - a_2b_0\ \ b_1 - a_1b_0\,] = [2\ \ 1]$ (here $b_0 = 0$, so no direct feed-through, $D = 0$). Check: $C(zI-A)^{-1}B = [2\ 1]\dfrac{1}{z^2+4z+3}\begin{bmatrix}z+4&1\\-3&z\end{bmatrix}\begin{bmatrix}0\\1\end{bmatrix} = \dfrac{2 + z}{z^2+4z+3}$ ✓.

**(b) Jordan canonical form.** The pulse transfer function has a double pole at $z = -1$ and a simple pole at $z = -2$. Partial fractions:

$$\frac{Y(z)}{U(z)} = \frac{5}{(z+1)^2(z+2)} = \frac{5}{(z+1)^2} - \frac{5}{z+1} + \frac{5}{z+2}$$

(the constants: $A = 5/(−1+2) = 5$, $C = 5/(−2+1)^2 = 5$, $B = \dfrac{d}{dz}\left[\dfrac{5}{z+2}\right]_{z=-1} = -5$).

Choose the states $X_2(z) = \dfrac{U(z)}{z+1}$, $X_1(z) = \dfrac{X_2(z)}{z+1} = \dfrac{U(z)}{(z+1)^2}$ and $X_3(z) = \dfrac{U(z)}{z+2}$. Then

$$x_1(k+1) = -x_1(k) + x_2(k),\quad x_2(k+1) = -x_2(k) + u(k),\quad x_3(k+1) = -2x_3(k) + u(k)$$

$$y(k) = 5x_1(k) - 5x_2(k) + 5x_3(k)$$

$$\boxed{\begin{bmatrix}x_1\\x_2\\x_3\end{bmatrix}(k+1) = \begin{bmatrix}-1&1&0\\0&-1&0\\0&0&-2\end{bmatrix}\begin{bmatrix}x_1\\x_2\\x_3\end{bmatrix}(k) + \begin{bmatrix}0\\1\\1\end{bmatrix}u(k),\qquad y(k) = \begin{bmatrix}5&-5&5\end{bmatrix}\begin{bmatrix}x_1\\x_2\\x_3\end{bmatrix}(k)}$$

The matrix is in **Jordan form** (a $2\times2$ Jordan block for the repeated eigenvalue $-1$ and a $1\times1$ block for $-2$). Check: $C(zI-A)^{-1}B$ evaluated numerically gives the numerator $5$ and the denominator $z^3 + 4z^2 + 5z + 2 = (z+1)^2(z+2)$ ✓.

**(c) Discretization of the continuous-time state equations.** A continuous plant $\dot x(t) = Ax(t) + Bu(t)$, $y = Cx$, driven by a computer through a D/A converter with a zero-order hold, has an input that is constant over each period, $u(t) = u(kT)$ for $kT\le t<(k+1)T$. The solution of the state equation over one period is

$$x((k+1)T) = e^{AT}x(kT) + \int_0^Te^{A\tau}B\,d\tau\;u(kT)$$

so the equivalent discrete-time system is

$$\begin{gathered}x(k+1) = Gx(k) + Hu(k) \\ y(k) = Cx(k)\end{gathered}$$

$$\begin{gathered}G = e^{AT} = \mathcal L^{-1}\left[(sI-A)^{-1}\right]_{t=T} \\ H = \left(\int_0^Te^{A\tau}d\tau\right)B \\ C\ \text{unchanged}.\end{gathered}$$

The matrix $G$ is the state transition matrix over one sampling period (Cayley-Hamilton, the Laplace transform or the diagonalisation can be used to compute it).

**State transition matrix of the given system.** For $x(k+1) = Gx(k) + Hu(k)$ the state transition matrix is $\Phi(k) = G^k$, computed by $\Phi(k) = \mathcal Z^{-1}\left[(zI - G)^{-1}z\right]$.

$$zI - G = \begin{bmatrix}z & -2\\0.2 & z+1.5\end{bmatrix},\qquad |zI-G| = z(z+1.5) + 0.4 = z^2 + 1.5z + 0.4$$

The characteristic roots are

$$\lambda_{1,2} = \frac{-1.5\pm\sqrt{2.25 - 1.6}}{2} = \frac{-1.5\pm0.8062}{2}\ \Rightarrow\ \lambda_1 = -0.3469,\quad \lambda_2 = -1.1531$$

$$(zI-G)^{-1} = \frac{1}{z^2+1.5z+0.4}\begin{bmatrix}z+1.5 & 2\\-0.2 & z\end{bmatrix}$$

Using partial fractions with $z^2+1.5z+0.4 = (z-\lambda_1)(z-\lambda_2)$ and $\lambda_1-\lambda_2 = 0.8062$:

$$\Phi(k) = \frac{\lambda_1^k\,(G - \lambda_2I) - \lambda_2^k\,(G - \lambda_1I)}{\lambda_1 - \lambda_2}$$

$$\boxed{\Phi(k) = (-0.3469)^k\begin{bmatrix}1.4303 & 2.4807\\-0.2481 & -0.4303\end{bmatrix} + (-1.1531)^k\begin{bmatrix}-0.4303 & -2.4807\\0.2481 & 1.4303\end{bmatrix}}$$

*Check:* $\Phi(0) = I$ (the two matrices add to the identity) and

$$\Phi(1) = \begin{bmatrix}0&2\\-0.2&-1.5\end{bmatrix} = G,\qquad \Phi(2) = G^2 = \begin{bmatrix}-0.4&-3\\0.3&1.85\end{bmatrix},\qquad \Phi(3) = \begin{bmatrix}0.6&3.7\\-0.37&-2.175\end{bmatrix}$$

✓. Since $|\lambda_2| = 1.153 > 1$, the system as printed is unstable (the term $(-1.1531)^k$ grows without bound); the output sequence follows $y(k) = C\Phi(k)x(0) + \sum_{j=0}^{k-1}C\Phi(k-j-1)Hu(j)$.
