---
file: NEBians-IOE-Past-Paper-Propagation-and-Antenna-ENEX303-2082-Chaitra.pdf
subject: Propagation and Antenna
level: BE · Year III / Part I
code: ENEX 303
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
List the main properties of antenna. Explain the major required conditions for a simple conductor to be a good antenna. [[2+3]]

@q 2
State the following antenna theorems:

a) Compensation theorem

b) Reciprocity theorem [[2+2]]

@q 3
Derive an expression for the total field in case of two isotropic point sources with equal amplitude and quadrature phase. [[5]]

@q 4
Define the following antenna parameters:

a) Fractional Bandwidth (FBW)

b) Power flux density (PFD) [[2+2]]

@q 5
What is a travelling wave antenna? Explain the working principle and main features of V-antenna with necessary diagrams. [[1+4]]

@q 6
Design a 5 element Yagi-Uda antenna for receiving UHF band of frequency range from 540 MHz to 548 MHz. Assume the driven element is a half-wave folded dipole and take spacing between elements $0.15\lambda_c$. [[5]]

@q 7
What are the major features of corrugated horn antenna? How does a helical antenna radiate in axial mode? Explain with necessary diagrams. [[2+3]]

@q 8
What is a direct wave propagation? Explain the different factors that affect the space wave propagation. [[1+3]]

@q 9
Derive the Friis transmission equation and find out the free space path loss from the equation that is equal to $22 + 20\log(R/\lambda_c)$ in dB where $R$ is distance between transmitting and receiving antennas and $\lambda_c$ is wavelength of the frequency being used. [[3+2]]

@q 10
Define the virtual height of the ionosphere and derive the expression for relation between the skip distance ($D$) and critical frequency ($f_{crt}$) assuming Earth is not curve. [[1+5]]

@q 11
A ground station located at 42.7° N latitude and 108.3° E longitude need to establish a Ku-band uplink to a GEO satellite positioned at 128° E longitude. The satellite's receiver has a G/T of 4.8 dB/K and the desired $C/N_0$ is 107 dBHz. The ground station employs a parabolic antenna with a diameter of 7.8 m, an antenna efficiency of 75% and waveguide loss of 1.6 dB. Determine the minimum transmit power that the ground station must provide to achieve the required $C/N_0$, accounting for the actual Earth-satellite slant distance. [[8]]

@q 12
Write short notes on (Any Two):

a) Smart Antennas

b) Duct propagation

c) Knife edge diffraction [[2×2]]
<!-- SOLUTIONS -->

@s 1
**Main properties (parameters) of an antenna**

1. **Radiation pattern:** the angular variation of the radiated field or power (main lobe, side lobes, back lobe, nulls).
2. **Directivity and gain:** $D = U_{max}/U_{av}$ and $G = \eta D$.
3. **Beamwidth:** half-power beamwidth (HPBW) and first-null beamwidth.
4. **Input impedance and radiation resistance:** $Z_{in} = R_r + R_L + jX$; decides matching and VSWR.
5. **Bandwidth:** the frequency range over which the pattern, gain and impedance stay within specification.
6. **Efficiency:** $\eta = R_r/(R_r + R_L)$ (ratio of radiated to input power).
7. **Polarization:** the direction of the electric field of the radiated wave (linear, circular, elliptical).
8. **Effective aperture** $A_e = G\lambda^2/4\pi$ and **effective length**.
9. **Front-to-back ratio** and side-lobe level; **reciprocity** of transmit and receive behaviour.

**Conditions for a simple conductor to be a good antenna**

A piece of wire carrying a steady current radiates nothing. A conductor radiates efficiently only when the following conditions are satisfied.

1. **Time-varying current.** Radiation comes from accelerated charges, so the current must vary with time (alternating current at radio frequency).
2. **Dimensions comparable to the wavelength.** The length must be of the order of $\lambda/2$ or $\lambda/4$ (at least about $\lambda/10$). A much shorter wire has a tiny radiation resistance (for a short dipole $R_r = 80\pi^2(l/\lambda)^2$) and radiates poorly, with most input power lost as heat.
3. **Open, spread-out geometry.** The two conductors of a transmission line carry currents in opposite directions at spacing $\ll\lambda$, so their fields cancel and almost nothing is radiated. If the ends are bent apart (flared) to form a dipole, the currents become in phase in space, the fields add, and the structure radiates.
4. **A suitable current distribution.** A standing wave (resonant antenna) or a travelling wave must exist on the conductor. For a half-wave dipole the current is sinusoidal with a maximum at the centre and nodes at the ends, which gives a real, low radiation resistance of about $73\,\Omega$.
5. **Good impedance match to the feed line.** The input impedance should match the characteristic impedance of the line so that the power is not reflected (VSWR close to 1).
6. **Low loss.** A highly conducting, adequately thick conductor so that $R_L\ll R_r$ and the efficiency is high.
7. **Required pattern and polarization** for the application (directive, omnidirectional, and so on).

@s 2
**(a) Compensation theorem.** If the impedance $Z$ of a branch of a linear network, carrying a current $I$, is changed by an amount $\Delta Z$, the resulting change in the currents of all branches is the same as the current that would be produced by a *compensating* voltage source $\Delta V = -I\,\Delta Z$ placed in series in that branch, with all the other independent sources of the network replaced by their internal impedances (set to zero).

$$\Delta I_k = \text{current in branch } k \text{ due to the single source } (-I\Delta Z)\text{ acting in the original network.}$$

In antennas it is used to find how the input impedance and the current distribution of an antenna change when a load, a parasitic element or an obstacle is added near it (the change in impedance is treated as a source at the changed point).

**(b) Reciprocity theorem.** In a linear, passive, isotropic medium, if a voltage $V_1$ applied at the terminals of antenna 1 produces a current $I_2$ at the terminals of antenna 2 (short-circuited), then the same voltage applied at antenna 2 produces the same current at antenna 1:

$$\frac{V_1}{I_2} = \frac{V_2}{I_1}\quad\text{i.e.}\quad Z_{12} = Z_{21}.$$

Consequently the radiation pattern, directivity, gain, effective aperture and impedance of an antenna are the same whether it is used for transmitting or receiving. This lets one measure or analyse the receiving pattern by treating the antenna as a transmitter.

@s 3
Two isotropic point sources 1 and 2 of equal amplitude $E_0$ are separated by a distance $d$ along the $x$ axis. Source 2 leads source 1 by $\delta = 90^\circ$ (quadrature). Consider a far-field point $P$ at an angle $\phi$ from the line joining the sources. The distances to $P$ are $r_1$ and $r_2\approx r_1 - d\cos\phi$ (parallel rays; the amplitude difference is neglected).

Field of source 1 (taken as reference, centred at the origin):

$$E_1 = E_0\,e^{-j\beta r_1}$$

Field of source 2, which leads in phase by $\delta$ and is closer to $P$ by $d\cos\phi$:

$$E_2 = E_0\,e^{-j\beta r_2}\,e^{j\delta} = E_0\,e^{-j\beta r_1}\,e^{\,j(\beta d\cos\phi + \delta)}$$

Define the total phase difference $\psi = \beta d\cos\phi + \delta$, where $\beta = 2\pi/\lambda$. The total field is

$$E = E_1 + E_2 = E_0e^{-j\beta r_1}\left(1 + e^{j\psi}\right) = E_0e^{-j\beta r_1}\,e^{j\psi/2}\left(e^{-j\psi/2} + e^{j\psi/2}\right)$$

$$E = 2E_0\cos\left(\frac{\psi}{2}\right)e^{\,j\psi/2}\,e^{-j\beta r_1}$$

The magnitude of the field is

$$|E| = 2E_0\left|\cos\frac{\psi}{2}\right|$$

Put $\delta = \pi/2$ (quadrature):

$$\boxed{|E| = 2E_0\left|\cos\left[\frac{1}{2}\left(\beta d\cos\phi + \frac{\pi}{2}\right)\right]\right| = 2E_0\left|\cos\left(\frac{\pi d}{\lambda}\cos\phi + \frac{\pi}{4}\right)\right|}$$

The normalised pattern is $E_n = \cos\left(\frac{\pi d}{\lambda}\cos\phi + \frac\pi4\right)$.

**Maxima and nulls.** Maximum when $\psi = 0$: $\cos\phi_{max} = -\dfrac{\delta}{\beta d} = -\dfrac{\lambda}{4d}$. Nulls when $\psi = \pm\pi$: $\cos\phi_{null} = \dfrac{\pi - \pi/2}{\beta d} = \dfrac{\lambda}{4d}$ (and the corresponding $-3\lambda/4d$ if it exists).

**Example: $d = \lambda/4$.** Then $\psi = \frac\pi2(\cos\phi + 1)$ and

$$E_n = \cos\left[\frac{\pi}{4}(1+\cos\phi)\right]$$

This is zero at $\phi = 0^\circ$ ($\psi=\pi$) and maximum at $\phi = 180^\circ$ ($\psi = 0$): a **unidirectional (end-fire) cardioid-like pattern**, radiating away from the leading source's side and with a null in the direction $\phi=0$. For $d = \lambda/2$ the nulls occur at $\cos\phi = 1/2$, that is $\phi = 60^\circ$, and the pattern has maxima at $\phi = 120^\circ$ and $240^\circ$ ($\cos\phi=-1/2$).

```figure caption="Normalised field pattern of two isotropic sources of equal amplitude in phase quadrature for d = lambda/4: En = cos[(pi/4)(1 + cos phi)]. The null is at phi = 0 and the maximum at phi = 180 degrees (end-fire)."
import numpy as np, matplotlib.pyplot as plt
phi=np.linspace(0,2*np.pi,500); r=abs(np.cos(np.pi/4*(1+np.cos(phi))))
fig=plt.figure(figsize=(3.6,3.3)); ax=fig.add_subplot(111,projection='polar')
ax.plot(phi,r,color=ACCENT,lw=1.6); ax.fill(phi,r,color=ACCENT,alpha=.15)
ax.set_rticks([0.5,1.0]); ax.tick_params(labelsize=7); ax.set_title("$d=\\lambda/4,\\ \\delta=90^\\circ$",fontsize=8)
```

@s 4
**(a) Fractional bandwidth (FBW).** The ratio of the usable bandwidth of the antenna to its centre frequency:

$$\begin{gathered}\text{FBW} = \frac{f_H - f_L}{f_c} \\ f_c = \frac{f_H + f_L}{2} \\ (\times100\ \text{for percentage}).\end{gathered}$$

$f_H$ and $f_L$ are the upper and lower frequencies at which the antenna still meets its specification (for example $\text{VSWR}\le2$ or $S_{11}\le-10$ dB). It is a dimensionless number: narrow-band antennas have FBW below about 1%, wide-band ones above 20% (ultra-wideband antennas have FBW above 20% by the FCC definition). Example: an antenna working from 540 to 548 MHz has $\text{FBW} = 8/544 = 1.47\%$.

**(b) Power flux density (PFD).** The power per unit area crossing a surface held perpendicular to the direction of propagation at a distance $R$ from the antenna. For a transmitter with power $P_t$ and gain $G_t$ (EIRP $= P_tG_t$):

$$\begin{gathered}\text{PFD} = \frac{P_tG_t}{4\pi R^2} = \frac{\text{EIRP}}{4\pi R^2}\ \ \text{W/m}^2 = \frac{|E|^2}{\eta_0} \\ \eta_0 = 120\pi\,\Omega.\end{gathered}$$

It is the magnitude of the time-averaged Poynting vector, and is quoted in W/m$^2$ or dB(W/m$^2$). The power received is $P_r = \text{PFD}\times A_e$ with $A_e = G_r\lambda^2/4\pi$ (it is the basis of the Friis equation).

@s 5
**Travelling wave antenna.** An antenna in which the current is a pure *travelling wave* moving along the conductor in one direction only (there is no reflected wave and hence no standing wave). It is obtained by making the wire long (several wavelengths) and **terminating it in its characteristic impedance** (a matched resistor of $200$ to $800\,\Omega$), so that the wave is absorbed at the end instead of being reflected. Because it does not rely on resonance, it is a **non-resonant, aperiodic and wide-band antenna**. Examples: long wire, V, rhombic, beverage antenna.

**V-antenna.**

*Construction.* Two long wires, each of length $L$ (several $\lambda$), are fed at the apex and spread apart in the shape of a V with an included angle $2\theta$ (half angle $\theta$ from the bisector). The ends are terminated in resistors (or left open for a resonant V).

*Working principle.* A single long wire carrying a travelling current of length $L$ radiates a pattern in the form of a **cone** around the wire. The main lobe makes an angle $\theta_m$ with the wire:

$$\cos\theta_m \approx 1 - 0.371\frac{\lambda}{L}$$

so the lobe moves closer to the wire as $L$ increases. In a V antenna the two legs carry currents flowing in opposite directions (fed in antiphase, $180^\circ$ out of phase) from the apex. If the half angle $\theta$ of the V is made equal to $\theta_m$, the main lobes of both legs, which are tilted by $\theta_m$ from each wire, coincide along the bisector of the V and the fields **add in phase** there. The other lobes partly cancel. The result is a single strong lobe along the bisector, a sharp unidirectional beam with the main radiation off the open end of the V (end-fire).

*Example.* For $L = 3\lambda$, $\cos\theta_m = 1 - 0.371/3 = 0.876$, giving $\theta_m = 28.8^\circ$, so the V is built with an included angle of about $58^\circ$.

*Main features*

1. Wide bandwidth (a frequency range of about $2:1$ or more) because no resonance is used.
2. A resonant (open ended) V is bidirectional; terminating the legs removes the reflected wave and gives a **unidirectional** pattern with front-to-back ratio of about 10 to 20 dB.
3. Gain increases with the leg length $L$ (typically 8 to 12 dB for $L$ of 3 to 6 wavelengths) and with the correct apex angle.
4. Linear polarization (horizontal if the V is mounted horizontally).
5. The terminating resistors absorb about half of the power, so the efficiency is lower (about 50 to 70%).
6. Requires a large open space, and is used for HF communication and as an element in rhombic arrays.

```figure caption="V-antenna: two legs of length L at half-angle theta from the bisector, each leg radiating a conical lobe at angle theta_m to the wire (theta = theta_m). The two lobes reinforce along the bisector. The far ends are terminated in resistors R."
import numpy as np, matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(5.4,2.9)); ax.axis('off'); ax.set_aspect('equal'); ax.set_xlim(-1,10.5); ax.set_ylim(-3,3)
th=np.radians(28.8); L=6.5
for s in (1,-1):
    ex,ey=L*np.cos(th),s*L*np.sin(th); ax.plot([0,ex],[0,ey],color=INK,lw=2)
    ax.plot([ex],[ey-0.15*s],'s',color=SERIES[1],ms=5)
    # lobe around leg
    t=np.linspace(-0.55,0.55,60)
    ang=s*th+t; r=3.4*np.cos(t*2.6)**2*(abs(np.cos(t*2.6))>0)
    ax.plot(r*np.cos(ang)+1.0,r*np.sin(ang),color=ACCENT,lw=1,ls='--')
a=np.linspace(-0.6,0.6,80); r=5.5*np.cos(a*2.4)**3
ax.plot(r*np.cos(a)+1.0,r*np.sin(a),color=SERIES[1],lw=1.6)
ax.annotate("",xy=(9.2,0),xytext=(1.0,0),arrowprops=dict(arrowstyle="->",color=SERIES[1]))
ax.text(9.3,0.15,"main beam",fontsize=7); ax.text(-0.9,0.0,"feed",fontsize=7,va='center')
ax.text(3.4,1.9,"leg 1 ($L$)",fontsize=7,rotation=28); ax.text(3.4,-2.3,"leg 2 ($L$)",fontsize=7,rotation=-28)
ax.text(1.6,0.55,"$\\theta$",fontsize=8)
```

@s 6
**Design of the 5-element Yagi-Uda array (reflector + driven element + 3 directors).**

*Centre frequency and wavelength.* The band is 540 to 548 MHz, so

$$\begin{gathered}f_c = \frac{540 + 548}{2} = 544\ \text{MHz} \\ \lambda_c = \frac{c}{f_c} = \frac{3\times10^8}{544\times10^6} = 0.5515\ \text{m} = 551.5\ \text{mm}.\end{gathered}$$

The fractional bandwidth is only $8/544 = 1.47\%$, so a single design at $f_c$ is sufficient for the whole band.

*Element lengths.* The parasitic elements are tuned for the required current phase: the **reflector** is slightly longer than $\lambda/2$ (inductive, current lags), the **driven element** is a half-wave resonant folded dipole shortened by the end effect, and the **directors** are shorter than $\lambda/2$ (capacitive, current leads). The directors are tapered slightly. Standard design factors (end-effect corrected, thin elements) give:

| Element | Length factor | Length $= $ factor $\times\lambda_c$ | Position from the reflector |
|---|---|---|---|
| Reflector | $0.500\lambda_c$ | $275.7$ mm | $0$ |
| Driven element (folded dipole) | $0.473\lambda_c$ | $260.8$ mm | $0.15\lambda_c = 82.7$ mm |
| Director 1 | $0.440\lambda_c$ | $242.6$ mm | $0.30\lambda_c = 165.4$ mm |
| Director 2 | $0.436\lambda_c$ | $240.4$ mm | $0.45\lambda_c = 248.1$ mm |
| Director 3 | $0.430\lambda_c$ | $237.1$ mm | $0.60\lambda_c = 330.9$ mm |

*Spacing.* All adjacent elements are $0.15\lambda_c = 82.7$ mm apart, so the boom length is $4\times0.15\lambda_c = 0.6\lambda_c \approx 331$ mm (plus a little at each end).

*Driven element.* A half-wave **folded dipole** is two parallel conductors joined at both ends, of length $\approx0.473\lambda_c$ (260.8 mm) and a spacing of a few element diameters. An isolated folded dipole has $Z_{in}\approx4\times73 = 292\,\Omega$. The parasitic elements, which are close, lower it to roughly $50$ to $75\,\Omega$, so the antenna matches a $50$ or $75\,\Omega$ line (for television coax, a balun is added for the balanced-to-unbalanced transition).

*Expected performance.* Gain about $9$ to $11$ dBi (7 to 9 dBd) for 5 elements, half-power beamwidth about $50^\circ$ to $60^\circ$, front-to-back ratio about 15 to 20 dB, horizontally polarized when the elements are horizontal. The elements may be made of aluminium rod of 4 to 6 mm diameter and the boom is non-conducting or conducting (with element-length corrections).

```figure caption="Layout of the 5-element Yagi-Uda antenna for 544 MHz (lambda_c = 551.5 mm): reflector, folded-dipole driven element and three directors on a boom, spaced 0.15 lambda_c. Element lengths in multiples of lambda_c."
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(5.6,2.9)); ax.axis('off'); ax.set_xlim(-1.2,10.6); ax.set_ylim(-3.2,3.2)
xs=[0,1.9,3.8,5.7,7.6]; Ls=[0.500,0.473,0.440,0.436,0.430]; nm=["reflector\n0.500$\\lambda$","driven (folded)\n0.473$\\lambda$","D1\n0.440$\\lambda$","D2\n0.436$\\lambda$","D3\n0.430$\\lambda$"]
ax.plot([-0.5,8.4],[0,0],color='#666',lw=2.5)
for x,L,n in zip(xs,Ls,nm):
    h=L*5.4; ax.plot([x,x],[-h/2,h/2],color=ACCENT if x!=1.9 else SERIES[1],lw=3)
    ax.text(x,-h/2-0.2,n,ha='center',va='top',fontsize=6.8)
ax.plot([1.9+0.18]*2,[-1.27,1.27],color=SERIES[1],lw=1.5)
for i in range(4):
    ax.annotate("",xy=(xs[i+1],2.2),xytext=(xs[i],2.2),arrowprops=dict(arrowstyle="<->",color=INK,lw=.8)); ax.text((xs[i]+xs[i+1])/2,2.35,"0.15$\\lambda$",ha='center',fontsize=6.8)
ax.annotate("",xy=(10.3,0),xytext=(8.5,0),arrowprops=dict(arrowstyle="->",color=SERIES[1],lw=1.6)); ax.text(9.0,0.3,"beam",fontsize=7)
ax.text(1.9,1.5,"to receiver",fontsize=6.8,ha='center')
```

@s 7
**Corrugated horn antenna: major features**

A corrugated horn is a (usually conical) horn whose inner wall carries circumferential grooves about $\lambda/4$ deep, which make the wall surface reactive in both polarizations (balanced hybrid mode $HE_{11}$).

1. **Equal E-plane and H-plane patterns:** the beam is axially symmetric, with equal beamwidths and phase centres in both planes.
2. **Very low cross-polarization** (below about $-30$ dB) and low side lobes and back lobes, because the field at the wall edge falls to zero.
3. **Low spill-over and high aperture efficiency** (about 70 to 80% when used as a feed).
4. **Wide bandwidth** (about $1.5:1$ and beyond), a stable phase centre and a low VSWR.
5. Used as the **primary feed** of parabolic and Cassegrain reflectors in satellite earth stations, radio-astronomy and microwave links, and as a standard gain horn.
6. **Disadvantages:** heavy, costly to machine, bulkier than a smooth-wall horn, and the grooves must be accurate.

**Helical antenna in axial mode**

A helical antenna is a wire wound in the shape of a helix over a ground plane (a flat metal sheet or mesh), fed at the base by a coaxial line. Dimensions: helix diameter $D$ and circumference $C = \pi D$, spacing between turns $S$, pitch angle $\alpha = \tan^{-1}(S/\pi D)$, number of turns $N$, axial length $A = NS$.

*Axial (end-fire) mode.* For $0.75\lambda < C < 1.33\lambda$ (that is $C\approx\lambda$), $S\approx\lambda/4$ and $\alpha = 12^\circ$ to $14^\circ$, the helix behaves as a **travelling-wave antenna**. A current wave travels along the wire; the phase velocity along the helix axis is slowed down so that the radiation from every turn adds in phase along the axis (the Hansen-Woodyard condition for maximum directivity: the progressive phase between successive turns is $\psi = -(\beta S + \pi/N)$ instead of the ordinary end-fire value $-\beta S$). Each turn of circumference about $\lambda$ carries currents of equal amplitude whose horizontal and vertical components are $90^\circ$ out of phase in space, so the radiated wave in the direction of the axis is **circularly polarized** (the sense of the polarization is set by the sense of winding, right or left-handed). The maximum radiation is in the direction of the axis, away from the ground plane, giving a single beam with:

$$\begin{gathered}D\approx15\left(\frac{C}{\lambda}\right)^2\frac{NS}{\lambda} \\ \text{HPBW}\approx\frac{52\lambda^{3/2}}{C\sqrt{NS}} \\ R_{in}\approx140\frac{C}{\lambda}\ \Omega\end{gathered}$$

The bandwidth is wide (about $1.7:1$), and the antenna is widely used for satellite and space telemetry because circular polarization removes the need to align the transmit and receive antennas.

*Normal mode (for contrast).* When the helix is very small ($D, S\ll\lambda$), the radiation is broadside, like a short dipole or loop, with linear or elliptical polarization.

```figure caption="Helical antenna in axial mode: helix of N turns (circumference about lambda, spacing about lambda/4) above a ground plane; the main beam is along the helix axis and is circularly polarized."
import numpy as np, matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(4.4,3.2)); ax.axis('off'); ax.set_xlim(-3,3.2); ax.set_ylim(-1.2,5.6)
t=np.linspace(0,6*2*np.pi,600); x=0.9*np.cos(t); y=0.35*np.sin(t)+t/(2*np.pi)*0.7+0.4
ax.plot(x,y,color=ACCENT,lw=1.6)
ax.add_patch(plt.Polygon([[-2.4,0.1],[2.4,0.1],[2.9,-0.5],[-1.9,-0.5]],fc='#e6e6e6',ec=INK,lw=1)); ax.text(0,-0.85,"ground plane",ha='center',fontsize=7)
ax.plot([0,0],[-0.3,0.4],color=INK,lw=2); ax.text(0.2,-0.2,"feed",fontsize=7)
ax.annotate("",xy=(0,5.5),xytext=(0,4.7),arrowprops=dict(arrowstyle="->",color=SERIES[1],lw=1.6)); ax.text(0.15,5.15,"axial beam (circular polarization)",fontsize=7)
ax.annotate("",xy=(1.8,0.5),xytext=(1.8,2.5),arrowprops=dict(arrowstyle="<->",lw=.8)); ax.text(1.9,1.5,"$S$",fontsize=8)
```

@s 8
**Direct wave (line-of-sight) propagation.** The direct wave is the part of the space wave that travels in a straight line from the transmitting antenna to the receiving antenna when they are in sight of each other, without touching the ground. It is the main mode of propagation for VHF, UHF and microwave frequencies (above about 30 MHz), such as FM, TV broadcasting, microwave links and mobile communication. The range is limited by the **radio horizon**, $d = 4.12\left(\sqrt{h_t} + \sqrt{h_r}\right)$ km ($h$ in metres, with the effective earth radius $\tfrac43R$).

**Factors affecting space wave propagation**

1. **Curvature of the Earth and antenna heights.** The line of sight is blocked beyond the horizon. The range increases with the heights of the antennas: $d = 4.12(\sqrt{h_t}+\sqrt{h_r})$ km. Larger heights also give clearance from obstacles.
2. **Ground-reflected wave.** The wave reflected from the ground interferes with the direct wave. The received field is $E = 2E_0\sin\left(\dfrac{2\pi h_th_r}{\lambda d}\right)$ for perfect reflection ($180^\circ$ phase shift), so the field changes with the distance, the heights and the wavelength (height-gain and lobing effects); the reflection coefficient depends on polarization, ground conductivity and grazing angle.
3. **Atmospheric refraction.** The refractive index of the troposphere decreases with height, which bends the ray towards the Earth. This is described by the effective Earth radius factor $k = 4/3$ for the standard atmosphere; sub-refraction shortens the range, and super-refraction or ducting extends it.
4. **Diffraction and obstacles.** Hills, buildings and trees obstruct the path; the Fresnel zone clearance (60% of the first Fresnel zone) is required, otherwise there is diffraction loss.
5. **Atmospheric absorption and rain attenuation.** Oxygen (60 GHz) and water-vapour (22 GHz) resonances and rain, fog and snow attenuate the signal strongly above about 10 GHz.
6. **Multipath, scattering and fading.** Reflections from buildings and hills and scattering from rough terrain, together with variations of the refractive index (tropospheric scatter, layers), cause fading.
7. **Frequency and polarization.** Higher frequency gives sharper beams but larger losses; vertical and horizontal polarizations are reflected and attenuated differently.

@s 9
**Friis transmission equation.** Consider a transmitting antenna with input power $P_t$ and gain $G_t$ at a distance $R$ from a receiving antenna with gain $G_r$ and effective aperture $A_{er}$, both in free space, matched, polarization-aligned and pointing at each other.

*Step 1: power density at the receiver.* An isotropic radiator spreads its power uniformly over a sphere of area $4\pi R^2$. The transmitting antenna adds its gain $G_t$:

$$S = \frac{P_tG_t}{4\pi R^2}\ \ \text{W/m}^2$$

*Step 2: power collected.* The receiving antenna captures the power in the area of its effective aperture, $P_r = S\,A_{er}$, with

$$A_{er} = \frac{\lambda^2}{4\pi}G_r$$

*Step 3: combine.*

$$P_r = \frac{P_tG_t}{4\pi R^2}\cdot\frac{G_r\lambda^2}{4\pi}$$

$$\boxed{P_r = P_tG_tG_r\left(\frac{\lambda}{4\pi R}\right)^2}$$

which is the **Friis transmission equation**. With $\text{EIRP} = P_tG_t$, $P_r = \text{EIRP}\cdot G_r/L_{fs}$.

**Free space path loss.** The factor $(\lambda/4\pi R)^2$ is the reciprocal of the free-space path loss, which is the ratio of the transmitted power to the received power for unity-gain antennas ($G_t = G_r = 1$):

$$L_{fs} = \frac{P_t}{P_r} = \left(\frac{4\pi R}{\lambda}\right)^2$$

In decibels:

$$L_{fs}(\text{dB}) = 10\log\left(\frac{4\pi R}{\lambda}\right)^2 = 20\log(4\pi) + 20\log\left(\frac{R}{\lambda}\right)$$

Since $20\log(4\pi) = 20\log(12.566) = 21.98\approx22$:

$$\boxed{L_{fs}(\text{dB}) = 22 + 20\log\left(\frac{R}{\lambda_c}\right)}$$

where $R$ and $\lambda_c$ are in the same units. (In terms of frequency, with $R$ in km and $f$ in MHz, it is $L_{fs} = 32.44 + 20\log R_{km} + 20\log f_{MHz}$.)

@s 10
**Virtual height.** When a radio wave is sent obliquely into the ionosphere, the electron density increases with height, the refractive index decreases, and the wave bends gradually and returns to Earth. The **virtual height $h'$** is the height of an imaginary *sharp* reflecting surface from which the wave would be reflected, if it were to travel along the straight incident and reflected paths (the straight-line extensions) without bending. It is greater than the true (actual) height of the reflecting point, because the wave slows down (group velocity $<c$) in the ionized layer. It is measured with an ionosonde as $h' = c\,t/2$, where $t$ is the pulse round-trip time.

**Critical frequency and skip distance.** The **critical frequency** $f_{crt}$ is the highest frequency that is reflected back to Earth when sent vertically upward ($f_{crt} = 9\sqrt{N_{max}}$, with $N_{max}$ in electrons/m$^3$ and $f_{crt}$ in Hz). The **skip distance $D$** is the shortest ground distance from the transmitter at which the sky wave of a given frequency $f$ ($>f_{crt}$) returns to Earth, with the **skip zone** inside it receiving no signal.

*Derivation (flat Earth, plane ionosphere).*

Take the equivalent sharp reflection at the virtual height $h'$. The wave leaves at an angle of incidence $\theta_i$ (measured from the vertical) and returns at the same angle. The ground range is

$$\begin{gathered}D = 2h'\tan\theta_i \\ (1)\end{gathered}$$

At the layer the refractive index is $n = \sqrt{1 - 81N/f^2}$ and by Snell's law for the stratified medium $\sin\theta_i = n\sin 90^\circ$ at the reflection level, where the ray becomes horizontal, so

$$\begin{gathered}\sin\theta_i = \sqrt{1 - \frac{81N_{max}}{f^2}} = \sqrt{1 - \frac{f_{crt}^2}{f^2}} \\ (2)\end{gathered}$$

using $f_{crt}^2 = 81N_{max}$. Then

$$\begin{gathered}\cos\theta_i = \frac{f_{crt}}{f}\quad\Rightarrow\quad \sec\theta_i = \frac{f}{f_{crt}} \\ (3)\end{gathered}$$

(this is the **secant law**: $f_{MUF} = f_{crt}\sec\theta_i$). From (3),

$$\begin{gathered}\tan\theta_i = \sqrt{\sec^2\theta_i - 1} = \sqrt{\left(\frac{f}{f_{crt}}\right)^2 - 1} \\ (4)\end{gathered}$$

Substituting (4) in (1):

$$\boxed{D = 2h'\sqrt{\left(\frac{f}{f_{crt}}\right)^2 - 1}}$$

Equivalently, for a given distance $D$ the maximum usable frequency is $f_{MUF} = f_{crt}\sqrt{1 + (D/2h')^2}$. When $f = f_{crt}$, $D = 0$ (the wave is reflected vertically). The skip distance increases with the operating frequency $f$ and the virtual height $h'$, and decreases as $f_{crt}$ increases (the ionosphere is denser by day).

```figure caption="Skip-distance geometry for a flat Earth: the sky wave is reflected as if from a mirror at the virtual height h'. The skip distance D = 2 h' tan(theta)."
import numpy as np, matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(5.2,2.7)); ax.axis('off'); ax.set_xlim(-0.5,10.5); ax.set_ylim(-0.7,4.2)
ax.plot([0,10],[0,0],color=INK,lw=2); ax.text(-0.45,-0.35,"Earth (flat)",fontsize=7)
ax.fill_between([0,10],[3.0,3.0],[3.7,3.7],color=ACCENT,alpha=.15); ax.text(8.3,3.9,"ionosphere layer",fontsize=7)
ax.plot([0,5,10],[0,3.4,0],color=SERIES[1],lw=1.2,ls='--'); ax.plot([0,5],[0,2.5],color=SERIES[1],lw=0); 
ax.plot([0,4.1,5],[0,2.7,3.0],color=SERIES[1],lw=1.4); ax.plot([5,5.9,10],[3.0,2.7,0],color=SERIES[1],lw=1.4)
ax.plot([5,5],[0,3.4],color='#888',lw=.8,ls=':'); ax.text(5.1,1.7,"$h'$",fontsize=9)
ax.annotate("",xy=(0,-0.5),xytext=(10,-0.5),arrowprops=dict(arrowstyle="<->",lw=.9)); ax.text(5,-0.68,"skip distance $D$",ha='center',fontsize=7.5)
ax.text(0.4,0.55,"$\\theta_i$",fontsize=8); ax.text(4.35,3.55,"virtual reflection point",fontsize=6.5,ha='center')
ax.plot([0],[0],'^',color=INK); ax.plot([10],[0],'v',color=INK); ax.text(0.15,0.2,"Tx",fontsize=7); ax.text(9.5,0.25,"Rx",fontsize=7)
```

@s 11
**Given:** ground station at $42.7^\circ$ N, $108.3^\circ$ E; GEO satellite at $128^\circ$ E (sub-satellite point on the equator); $G/T = 4.8$ dB/K; required $C/N_0 = 107$ dBHz; dish $D = 7.8$ m, $\eta = 0.75$; waveguide (feeder) loss $L_{wg} = 1.6$ dB. The Ku-band uplink is taken as $f = 14$ GHz (the uplink band is 14.0 to 14.5 GHz; the final transmit power turns out to be independent of the exact value of $f$). Other losses (rain, atmosphere, pointing) are not given, so they are not included.

**Step 1: slant range.** Earth radius $R_e = 6378$ km, GEO radius $a = R_e + h = 42164$ km. The longitude difference is $\Delta\lambda = 128 - 108.3 = 19.7^\circ$, and the central angle $\gamma$ between the station and the sub-satellite point satisfies

$$\cos\gamma = \cos(\text{lat})\cos(\Delta\lambda) = \cos42.7^\circ\cos19.7^\circ = 0.7349\times0.9414 = 0.6918\ \Rightarrow\ \gamma = 46.22^\circ$$

$$d = \sqrt{R_e^2 + a^2 - 2R_ea\cos\gamma} = \sqrt{6378^2 + 42164^2 - 2(6378)(42164)(0.6918)}$$

$$\boxed{d = 38\,031\ \text{km}}$$

(The elevation angle of the antenna is $El = \tan^{-1}\left[\dfrac{\cos\gamma - R_e/a}{\sin\gamma}\right] = 36.8^\circ$.)

**Step 2: free-space path loss** at $14$ GHz, $\lambda = c/f = 0.02143$ m:

$$L_{fs} = 20\log\left(\frac{4\pi d}{\lambda}\right) = 20\log\left(\frac{4\pi\times38.031\times10^6}{0.02143}\right) = 20\log(2.230\times10^{10})$$

$$\boxed{L_{fs} = 206.97\ \text{dB}}$$

**Step 3: ground antenna gain.**

$$G_t = \eta\left(\frac{\pi D}{\lambda}\right)^2 = 0.75\left(\frac{\pi\times7.8}{0.02143}\right)^2 = 0.75\,(1143.5)^2 = 9.81\times10^5$$

$$\boxed{G_t = 59.92\ \text{dBi}}$$

**Step 4: required EIRP.** The uplink carrier-to-noise-density ratio is

$$\begin{gathered}\frac{C}{N_0} = \text{EIRP} + \frac{G}{T} - L_{fs} - k\ (\text{dB}) \\ k = -228.6\ \text{dBW/K/Hz}\end{gathered}$$

$$\text{EIRP} = \frac{C}{N_0} - \frac GT + L_{fs} - 228.6 = 107 - 4.8 + 206.97 - 228.6$$

$$\boxed{\text{EIRP} = 80.57\ \text{dBW}}$$

**Step 5: transmit power.** $\text{EIRP} = P_t - L_{wg} + G_t$, so

$$P_t = \text{EIRP} - G_t + L_{wg} = 80.57 - 59.92 + 1.6$$

$$\boxed{P_t = 22.25\ \text{dBW} \approx 168\ \text{W}\ (52.3\ \text{dBm})}$$

The ground station must supply a minimum of about **168 W (22.3 dBW)** to the feeder (so that about 116 W reaches the antenna after the 1.6 dB waveguide loss). Because the path loss increases with $f^2$ and the dish gain also increases with $f^2$, the two cancel and the required power does not depend on the frequency chosen inside the Ku band. A real link budget adds a margin for rain fade (several dB at Ku-band), pointing error and atmospheric loss, which would increase the power accordingly.

@s 12
**(a) Smart antennas**

A smart (adaptive) antenna is an **array of antenna elements** combined with a **digital signal-processing unit** that adjusts the array weights (amplitude and phase of each element) in real time, so the radiation pattern is steered towards the desired user and nulls are placed in the direction of interferers.

*Block diagram:* array elements $\to$ RF front ends / down-converters $\to$ A/D converters $\to$ beamforming network (weights $w_1\dots w_N$, summed) $\to$ output; the weights are computed by an adaptive algorithm (LMS, RLS, CMA) or from direction-of-arrival estimation (MUSIC, ESPRIT).

*Types:* (i) **switched-beam** antennas select one of several fixed beams; (ii) **adaptive-array** antennas continuously steer the main beam to the user and nulls to interferers.

*Advantages:* increased range and coverage (array gain), higher system capacity through frequency reuse and SDMA (space-division multiple access), reduction of co-channel interference, multipath mitigation, higher data rates (MIMO), lower transmit power and better security. *Disadvantages:* more complex and expensive hardware and software, calibration of channels, and a larger power requirement for processing. *Applications:* cellular base stations (3G, 4G, 5G massive MIMO), radar, satellite and Wi-Fi.

**(b) Duct propagation**

Normally the refractive index of the troposphere decreases with height, and the radio wave bends slightly downward (standard atmosphere $dN/dh\approx-40$ N-units/km). Under certain conditions the refractive index decreases so rapidly with height that the radius of curvature of the ray becomes smaller than the Earth's radius: this happens when the **modified refractivity** $M = N + 0.157h$ decreases with height ($dM/dh<0$), or $dN/dh<-157$ N-units/km. The condition occurs in a **temperature inversion** (warm dry air over cool moist air, as over a sea surface or on calm clear nights, or on the passage of a warm front) and a rapid decrease of humidity with height.

Then a layer is formed in which rays that leave at small angles of elevation are repeatedly bent back towards the Earth and reflected by the ground (or by the sea). The wave is **trapped** in the duct, like in a waveguide, and travels a long way, beyond the normal horizon, with very little attenuation (a loss proportional to the first power of the distance and not to $d^2$). The duct may be a *surface duct* (from the ground to the top of the inversion) or an *elevated duct* (between two layers above the ground).

Features: occurs mostly for VHF, UHF and microwaves, since a duct of limited thickness can trap only the shorter wavelengths (a thin duct cannot trap long waves, which is why it does not affect HF); gives unexpected long-range reception of TV and FM signals (hundreds of kilometres), interference between distant stations on the same channel, radar anomalous propagation, and deep fading for receivers in the skip region of the duct. The attenuation along a duct is much smaller than the free-space loss, because the energy is confined between the layers (it spreads in two dimensions instead of three).

**(c) Knife-edge diffraction**

When an obstacle such as a hill or a building lies in the path between the transmitter and the receiver, the wave still reaches the shadow region by diffraction (the Huygens-Fresnel principle: each point on the wavefront above the obstacle acts as a secondary source). For a quick estimate the obstacle is modelled as a perfectly absorbing, infinitely thin **knife edge** of height $h$ above the line joining the antennas, at distances $d_1$ and $d_2$ from them.

The geometry is described by the dimensionless **Fresnel-Kirchhoff diffraction parameter**

$$\nu = h\sqrt{\frac{2(d_1+d_2)}{\lambda\,d_1d_2}}$$

($h>0$ when the edge blocks the line of sight, $h<0$ when there is clearance). The diffraction loss relative to free space is

$$J(\nu) = -20\log\left|\frac{1+j}{2}\int_\nu^\infty e^{-j\pi t^2/2}dt\right|\ \approx\ 6.9 + 20\log\left(\sqrt{(\nu-0.1)^2+1} + \nu - 0.1\right)\ \text{dB}\quad(\nu>-0.78)$$

Typical values: $\nu = -1$ (path clear by the first Fresnel zone radius) $\Rightarrow$ about $0$ dB; $\nu = 0$ (the edge just touching the line of sight) $\Rightarrow$ $6$ dB; $\nu = 1$ $\Rightarrow$ about $14$ dB; $\nu = 2.4\Rightarrow$ about $20$ dB. In link design, 60% of the first Fresnel zone radius $r_1 = \sqrt{\lambda d_1d_2/(d_1+d_2)}$ must be kept clear. Multiple edges are handled by the Bullington, Epstein-Peterson or Deygout constructions.

```figure caption="(b) Duct propagation: a ray trapped between the ground and the top of a surface duct (dM/dh < 0). (c) Knife-edge diffraction: obstacle of height h above the line of sight at distances d1 and d2 from Tx and Rx."
import numpy as np, matplotlib.pyplot as plt
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.8,2.5))
a1.axis('off'); a1.set_xlim(0,10); a1.set_ylim(-0.3,3.3)
a1.plot([0,10],[0,0],color=INK,lw=2); a1.fill_between([0,10],[1.6,1.6],[1.9,1.9],color=ACCENT,alpha=.2); a1.text(0.2,2.05,"inversion layer (duct top)",fontsize=6.8)
x=np.linspace(0.3,9.7,300); y=0.75+0.7*abs(np.sin(x*1.1))
a1.plot(x,0.1+1.35*abs(np.sin(x*0.95))**0.9,color=SERIES[1],lw=1.3)
a1.plot([0.3],[0.1],'^',color=INK); a1.plot([9.7],[0.1],'v',color=INK); a1.text(4.3,-0.28,"surface duct",fontsize=7); a1.set_title("(b) duct propagation",fontsize=8)
a2.axis('off'); a2.set_xlim(0,10); a2.set_ylim(-0.3,4.5)
a2.plot([0,10],[0,0],color='#999',lw=1); a2.fill([4.2,4.2,4.8,4.8],[0,2.0,2.0,0],color='#888',alpha=.7)
a2.plot([1,10-1],[1.0,1.0],color=INK,lw=.9,ls='--'); a2.plot([1,4.5,9],[1.0,2.0,1.0],color=SERIES[1],lw=1.4)
a2.plot([1],[1.0],'^',color=INK); a2.plot([9],[1.0],'v',color=INK); a2.text(0.2,0.45,"Tx",fontsize=7); a2.text(9.2,0.45,"Rx",fontsize=7)
a2.annotate("",xy=(4.5,1.0),xytext=(4.5,2.0),arrowprops=dict(arrowstyle="<->",lw=.8)); a2.text(4.65,1.45,"$h$",fontsize=8)
a2.annotate("",xy=(1,3.2),xytext=(4.5,3.2),arrowprops=dict(arrowstyle="<->",lw=.8)); a2.text(2.75,3.35,"$d_1$",fontsize=8,ha='center')
a2.annotate("",xy=(4.5,3.2),xytext=(9,3.2),arrowprops=dict(arrowstyle="<->",lw=.8)); a2.text(6.75,3.35,"$d_2$",fontsize=8,ha='center'); a2.set_title("(c) knife-edge diffraction",fontsize=8)
```
