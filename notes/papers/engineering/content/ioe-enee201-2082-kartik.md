---
file: NEBians-IOE-Past-Paper-Instrumentation-and-Measurement-ENEE201-2082-Kartik.pdf
subject: Instrumentation and Measurement
level: BE · Year II / Part I
code: ENEE 201
year_bs: 2082 Kartik
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE Electrical Engineering (BEL), Year II / Part I. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt All questions · The figures in the margin indicate Full Marks · Assume suitable data if necessary</small>

@q 1
Differentiate between analog and digital systems. Why digital instruments are becoming more popular nowadays? [[4]]

@q 2
Define errors in a measurement system. Explain different types of errors in measurement system along with their corrective measures. [[6]]

@q 3
Explain how capacitance is measured with the help of Hay's bridge. [[4]]

@q 4
Explain how magnitude and direction of displacement can be measured with the help of an inductive sensor. [[6]]

@q 5
A Barium Titanite Pick-up has the dimensions of 5 mm × 5 mm × 1.25 mm. The force acting upon it is 5 N. The charge sensitivity of it is 150 pC/N and its permittivity is 12.5 × 10$^{-9}$ F/m. If the modulus of elasticity of it is 12 × 10$^6$ N/m$^2$, calculate the strain. Also calculate the charge and the capacitance. [[4]]

@q 6
Explain how the fluid flow can be measured by using Hot Wire Anemometers. [[4]]

@q 7
What are the characteristics of an ideal Op-amp? State the features of an Instrumentation Amplifier and derive the expression for its Gain. [[8]]

@q 8
What are the drawbacks of weighted resistor network DAC? Which DAC is used to overcome these drawbacks? Explain its operation with a suitable diagram. [[8]]

@q 9
Explain the operation of sample and hold circuit. Also explain aperture time and acquisition time of the circuit. [[8]]

@q 10
Show how high current and high voltage can be measured with the help of instrument transformers. [[8]]

<!-- SOLUTIONS -->

@s 1
**Analog and digital systems**

| | **Analog system** | **Digital system** |
|---|---|---|
| Signal | Continuous in amplitude and time; the value is the information | Discrete levels (binary 0 and 1) at discrete instants |
| Display / output | Pointer on a scale (parallax, interpolation) | Numerical display (LED, LCD) |
| Resolution and accuracy | Limited by the scale (about 1 % of the full scale), reading error | Set by the number of bits or digits (0.01 % or better); no reading error |
| Noise | The noise adds directly to the signal and cannot be removed | Noise below the logic threshold is rejected; error correction is possible |
| Processing | Fixed by the hardware (filters, amplifiers) | **Programmable**: filtering, linearisation, calibration, averaging in software |
| Storage and transmission | Hard; degradation with copying | Easy to store, copy and transmit without loss |
| Speed | Continuous, no conversion delay | Sampling and conversion delay (ADC time) |
| Cost and complexity | Simple, cheap for basic needs | More complex, needs ADC / DAC and a processor |

**Why digital instruments are more popular**

1. **Higher accuracy and resolution** and a direct numerical read-out with no parallax or interpolation error; the display is easy to read.
2. **Noise immunity** and no drift of the stored data; signals can be sent over long distances (RS-485, wireless) without loss.
3. **Programmable and smart:** automatic ranging and zero, self-calibration, linearisation, statistics, alarms, unit conversion.
4. **Data logging, storage and communication** with computers, PLCs, SCADA and the cloud (USB, Ethernet, wireless).
5. **Small size, low power and low cost** thanks to ICs and microcontrollers; high reliability with no moving parts; high input impedance (low loading).
6. **Easy integration** with digital control systems, with a wide choice of the sensors with the digital output.

@s 2
**Error.** The error of a measurement is the difference between the measured value $x_m$ and the true value $x_t$ of the quantity:

$$\begin{gathered}e = x_m - x_t\ \text{(absolute error)} \\ \varepsilon = \frac{e}{x_t}\times100\ \%\ \text{(relative error)}\end{gathered}$$

**Types of errors and the corrective measures**

| Type | Cause | Corrective measures |
|---|---|---|
| **Gross (human) errors** | Mistakes in reading, recording, wrong range or connection, misuse of the instrument, calculation mistakes | Careful, attentive reading and recording; take several readings by different observers; use the proper range; check the circuit before switching on |
| **Systematic errors** | A definite, repeatable bias: *instrumental* (calibration error, zero error, friction, ageing, loading error), *environmental* (temperature, humidity, vibration, external fields), *observational* (parallax, wrong estimation) | Calibrate against a standard, apply correction factors and curves; use the null (zero-balance) methods; compensate the temperature; shield the instrument; use a mirror scale; use an instrument with a higher input impedance |
| **Random (accidental) errors** | Small, unpredictable fluctuations (noise, thermal and electrical disturbances, resolution) that follow a Gaussian distribution | Take a large number of readings and use the **mean** (the standard deviation of the mean falls as $\sigma/\sqrt n$); statistical analysis; filter the noise; better design and a stable environment |

*Also:* **static errors** (gain, offset, non-linearity, hysteresis, dead zone) and **dynamic errors** (the response lag). *Limiting (guarantee) error:* an instrument of accuracy $\pm a\ \%$ of the full scale has a possible error $\pm a\,x_{fs}/100$, so the readings should be taken in the upper part of the scale.

@s 3
**Hay's bridge.** A four-arm a.c. bridge in which arm 1 contains a known capacitor $C_1$ in **series** with a resistor $R_1$, arms 2 and 3 are the non-reactive resistors $R_2$ and $R_3$, and arm 4 is the unknown impedance. It is a bridge for measuring the **inductance** of a high-Q coil; with a standard inductor in place of the unknown it also measures the **capacitance** as below. A detector (headphones or an amplifier) is across the other diagonal and the bridge is balanced by $R_1$ and $R_2$ (or $R_3$).

**Balance condition:** $Z_1Z_4 = Z_2Z_3$.

*(a) Standard form (unknown $L_x$, $R_x$ in arm 4):*

$$\left(R_1 - \frac{j}{\omega C_1}\right)(R_x + j\omega L_x) = R_2R_3$$

Equating the real and imaginary parts:

$$\begin{gathered}R_1R_x + \frac{L_x}{C_1} = R_2R_3\\ \omega L_xR_1 - \frac{R_x}{\omega C_1} = 0\ \Rightarrow\ R_x = \omega^2L_xC_1R_1\end{gathered}$$

$$\begin{gathered}L_x = \frac{R_2R_3C_1}{1 + \omega^2C_1^2R_1^2} \\ R_x = \frac{\omega^2C_1^2R_1R_2R_3}{1 + \omega^2C_1^2R_1^2} \\ Q = \frac{\omega L_x}{R_x} = \frac{1}{\omega C_1R_1}\end{gathered}$$

*(b) Measuring a capacitance.* The unknown capacitor $C_x$ (with its series loss resistance included in $R_1$) takes the place of $C_1$ in arm 1 and a **standard inductor** $L_s$ (with the resistance $R_s$) is in arm 4. The same balance equation gives

$$\left(R_1 - \frac{j}{\omega C_x}\right)(R_s + j\omega L_s) = R_2R_3$$

$$\begin{gathered}\text{imaginary part: } \omega L_sR_1 = \frac{R_s}{\omega C_x}\ \Rightarrow\ C_x = \frac{R_s}{\omega^2L_sR_1}; \\ \text{real part: } R_1R_s + \frac{L_s}{C_x} = R_2R_3\end{gathered}$$

Eliminating $R_1$ between the two:

$$\boxed{C_x = \frac{R_s^2 + \omega^2L_s^2}{\omega^2L_s\,R_2R_3}\ \approx\ \frac{L_s}{R_2R_3}\quad(\omega L_s \gg R_s)}$$

and $R_1 = \dfrac{R_2R_3R_s}{R_s^2 + \omega^2L_s^2}$ is the equivalent series loss resistance of the capacitor, so the **dissipation factor** is $D = \omega C_xR_1$. The result depends on the frequency (the bridge is frequency-sensitive) and the standard inductor must have a negligible stray capacitance.

```figure caption="Question 3: Hay's bridge (unknown inductor in arm 4)."
fig,ax=plt.subplots(figsize=(5.4,3.6)); ax.axis('off'); ax.set_xlim(-0.8,7.2); ax.set_ylim(-0.6,6.4)
A=(0,3); B=(3,5.4); C=(6,3); D=(3,0.6)
wire(ax,[A,(0.4,3.7)]); 
res(ax,(0.0,3.0),(1.0,4.3),'',side=1) if False else None
ax.plot([A[0],B[0]],[A[1],B[1]],color=INK,lw=1.3); ax.plot([B[0],C[0]],[B[1],C[1]],color=INK,lw=1.3); ax.plot([C[0],D[0]],[C[1],D[1]],color=INK,lw=1.3); ax.plot([D[0],A[0]],[D[1],A[1]],color=INK,lw=1.3)
ax.plot([B[0],D[0]],[B[1],D[1]],color=INK,lw=1.0,ls='--')
for p,t,dx,dy in ((A,'A',-0.35,0),(B,'B',0,0.3),(C,'C',0.35,0),(D,'D',0,-0.35)): ax.text(p[0]+dx,p[1]+dy,t,fontsize=9,ha='center',va='center',weight='bold'); ax.plot(*p,'o',color=INK,ms=3.5)
ax.text(1.0,4.7,'$R_1$ in series\nwith $C_1$',fontsize=7.5,ha='center'); ax.text(5.0,4.7,'$R_2$',fontsize=8,ha='center'); ax.text(1.0,1.2,'$R_3$',fontsize=8,ha='center'); ax.text(5.0,1.2,'$L_x$, $R_x$',fontsize=8,ha='center')
ax.add_patch(Circle((3,3),0.35,fc='white',ec=INK)); ax.text(3,3,'D',fontsize=7,ha='center',va='center'); ax.text(3.45,3.0,'detector',fontsize=7,va='center')
ax.plot([A[0],A[0]-0.5],[A[1],A[1]-0.9],color=INK,lw=1.2); ax.plot([C[0],C[0]+0.5],[C[1],C[1]-0.9],color=INK,lw=1.2); ax.plot([A[0]-0.5,C[0]+0.5],[A[1]-0.9,C[1]-0.9],color=INK,lw=1.2)
ax.add_patch(Circle((3,1.9-0.3),0.3,fc='white',ec=INK)) if False else None
ax.text(3,2.0,'~',fontsize=0)
ax.text(3,1.95,'',fontsize=1)
ax.add_patch(Circle((3,2.1-1.5+0.0),0.0,fc='none'))
ax.text(3,-0.45,'a.c. source  $e$  across A and C',fontsize=7.5,ha='center',color=MUTED)
```

@s 4
**Inductive sensor for displacement: LVDT (linear variable differential transformer).** The LVDT has one **primary** winding $P$ (excited by an a.c. source, 1 to 10 V, 1 to 10 kHz) wound at the centre, and two identical **secondary** windings $S_1$ and $S_2$ placed symmetrically on both sides and **connected in series opposition** (so $e_o = e_{s1} - e_{s2}$). A movable ferromagnetic **core**, attached to the object whose displacement is to be measured, slides inside the former and changes the magnetic coupling to the two secondaries.

**Principle and operation**

- **Null position** (core at the centre): the flux linked with $S_1$ and $S_2$ is equal, so $e_{s1} = e_{s2}$ and the net output $e_o = 0$.
- **Core moves towards $S_1$:** more flux links $S_1$, so $e_{s1} > e_{s2}$ and $e_o = e_{s1} - e_{s2}$ is **in phase with the primary** voltage.
- **Core moves towards $S_2$:** $e_{s2} > e_{s1}$, so the output is **$180^\circ$ out of phase** with the primary.

Thus:

$$\begin{gathered}|e_o| \propto x\ \text{(magnitude of displacement)} \\ \text{phase of } e_o\ (0^\circ\text{ or }180^\circ)\ \text{ with respect to the primary voltage} \Rightarrow\ \text{direction}\end{gathered}$$

The sensitivity is typically 0.5 to 2 mV per 0.01 mm per volt of excitation, the linear range is about $\pm$ the length of the primary.

**Signal processing.** The a.c. output cannot show the direction by its magnitude alone, so a **phase-sensitive demodulator** (synchronous detector, or a rectifier with the reference taken from the excitation) is used: its d.c. output has a **magnitude proportional to the displacement** and a **polarity (+ or −) that gives the direction** (see the figure). A low-pass filter then gives a smooth d.c. voltage, which is read with a voltmeter or an ADC.

*Merits:* high resolution (about 0.1 µm), no friction (no contact between the core and the coil), infinite resolution theoretically, high sensitivity and robustness, a small residual null voltage, low hysteresis; *demerits:* the need for an a.c. excitation and a demodulator, the sensitivity to stray magnetic fields, limited dynamic response (the carrier frequency must be at least 10 times the signal frequency).

```figure caption="Question 4: LVDT: construction and the output against core displacement; the sign (phase) gives the direction."
fig,axs=plt.subplots(1,2,figsize=(6.8,2.7))
ax=axs[0]; ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,5)
ax.add_patch(Rectangle((1.0,1.5),8.0,2.0,fc='none',ec=INK,lw=1.2))
ax.add_patch(Rectangle((4.0,1.3),2.0,2.4,fc='#fde68a',ec=INK,lw=1.0)); ax.text(5.0,3.9,'primary',fontsize=7,ha='center')
ax.add_patch(Rectangle((1.4,1.4),2.2,2.2,fc='#bfdbfe',ec=INK,lw=1.0)); ax.text(2.5,3.9,'$S_1$',fontsize=7.5,ha='center')
ax.add_patch(Rectangle((6.4,1.4),2.2,2.2,fc='#bbf7d0',ec=INK,lw=1.0)); ax.text(7.5,3.9,'$S_2$',fontsize=7.5,ha='center')
ax.add_patch(Rectangle((3.3,2.25),4.0,0.5,fc='#cbd5e1',ec=INK)); ax.text(5.3,2.5,'core',fontsize=7,ha='center',va='center')
ax.plot([7.3,9.6],[2.5,2.5],color=INK,lw=2.0); arrow(ax,(8.4,1.1),(9.4,1.1),'$x$',off=0.25)
ax.text(5,0.45,'$e_o = e_{s1} - e_{s2}$ (series opposition)',fontsize=7.5,ha='center')
ax=axs[1]; x=np.linspace(-1,1,100); ax.plot(x,x,color=INK,lw=1.8); ax.axhline(0,color=GRID); ax.axvline(0,color=GRID)
ax.text(0.45,0.25,'in phase\n(core towards $S_1$)',fontsize=7); ax.text(-0.95,-0.55,'$180^\\circ$ out of phase\n(core towards $S_2$)',fontsize=7)
ax.set_xlabel('core displacement $x$'); ax.set_ylabel('signed demodulated output'); ax.set_xticks([]); ax.set_yticks([])
```

@s 5
**Data.** The pick-up is a barium titanate crystal, 5 mm × 5 mm × 1.25 mm; the force acts on the 5 mm × 5 mm face. Area $A = 5\times5 = 25\ \text{mm}^2 = 25\times10^{-6}\ \text{m}^2$; thickness $t = 1.25\times10^{-3}$ m; force $F = 5$ N; charge sensitivity $d = 150\ \text{pC/N}$; permittivity $\varepsilon = 12.5\times10^{-9}$ F/m; Young's modulus $E = 12\times10^6\ \text{N/m}^2$ (as printed).

**Strain.**

$$\sigma = \frac{F}{A} = \frac{5}{25\times10^{-6}} = 2\times10^5\ \text{N/m}^2$$

$$\boxed{\text{strain } \varepsilon_s = \frac{\sigma}{E} = \frac{2\times10^5}{12\times10^6} = 0.01667\ (1.67\ \%)}$$

**Charge.**

$$\boxed{Q = dF = 150\times10^{-12}\times5 = 750\ \text{pC} = 7.5\times10^{-10}\ \text{C}}$$

**Capacitance** (parallel-plate: electrodes on the faces of area $A$, spacing $t$):

$$\boxed{C = \frac{\varepsilon A}{t} = \frac{12.5\times10^{-9}\times25\times10^{-6}}{1.25\times10^{-3}} = 2.5\times10^{-10}\ \text{F} = 250\ \text{pF}}$$

**Output voltage** (extra check): $V = \dfrac{Q}{C} = \dfrac{750\ \text{pC}}{250\ \text{pF}} = 3\ \text{V}$, which agrees with the voltage sensitivity $g = d/\varepsilon = \dfrac{150\times10^{-12}}{12.5\times10^{-9}} = 0.012\ \text{V m/N}$ and $V = g\,t\,\sigma = 0.012\times1.25\times10^{-3}\times2\times10^5 = 3$ V ✓.

(The printed modulus $12\times10^6$ N/m² is far smaller than the true value for barium titanate, about $12\times10^{10}$ N/m², which would give a strain of $1.67\times10^{-6}$; the working follows the data as printed.)

@s 6
**Hot-wire anemometer.** A hot-wire anemometer measures the **velocity of a fluid (gas or liquid)** from the cooling effect of the flow on an electrically heated thin wire (platinum or tungsten, 4 to 10 µm in diameter, 1 to 2 mm long) with a high temperature coefficient of resistance.

**Principle.** The wire is heated by the current $I$ to a temperature $T_w$ above the fluid temperature $T_a$. The electrical power input equals the heat lost by forced convection, which increases with the velocity $v$ (**King's law**):

$$I^2R_w = (A + B\sqrt{v})\,(T_w - T_a)$$

where $A$ and $B$ are constants of the wire and the fluid found by calibration. So a higher velocity cools the wire more, so for a fixed current $R_w$ (and so $T_w$) falls, or for a fixed temperature a larger current is needed.

**Two modes of operation**

1. **Constant-current mode:** the current is held constant; the wire resistance (temperature) falls as the velocity rises, and the voltage across it $E = IR_w$ is measured with a Wheatstone bridge or an amplifier. The response is slow (the thermal inertia of the wire), so it needs compensation.
2. **Constant-temperature mode (CTA):** the wire is one arm of a Wheatstone bridge with a feedback amplifier that adjusts the bridge current so that $R_w$ (hence $T_w$) stays constant. The bridge voltage (or the current) is a direct measure of the velocity:

$$E^2 = (A' + B'\sqrt{v})\quad\Rightarrow\ v = \left(\frac{E^2 - A'}{B'}\right)^2$$

The frequency response is high (above 100 kHz), so it is used in the study of **turbulence**.

*Merits:* a very fast response, a small size, the measurement at a point, a high sensitivity at a low velocity; *demerits:* fragile, it needs a clean fluid (dust deposits change the calibration), it needs the temperature compensation of the fluid, and the output is non-linear (it needs linearisation).

@s 7
**Characteristics of an ideal op-amp**

1. **Infinite open-loop voltage gain** ($A_{OL} \to \infty$);
2. **Infinite input impedance** ($Z_{in} \to \infty$, so the input current is zero);
3. **Zero output impedance** ($Z_o = 0$; the output can drive any load);
4. **Infinite bandwidth** (the gain is the same at all frequencies, from d.c. to infinity);
5. **Infinite common-mode rejection ratio** (CMRR $\to \infty$, so no output for common-mode signals);
6. **Zero offset:** $V_o = 0$ when $V_1 = V_2$; zero drift with temperature and supply, no noise; infinite slew rate.

With negative feedback this gives the two golden rules: $V_+ = V_-$ (virtual short) and $I_+ = I_- = 0$.

**Instrumentation amplifier: features**

- A **high, balanced input impedance** (hundreds of MΩ to GΩ) on both inputs, so the source loading is negligible;
- A very **high CMRR** (80 to 120 dB), the amplification of the small differential signal from a bridge or thermocouple in the presence of a large common-mode voltage;
- A **low offset voltage and drift**, a low noise;
- A stable and accurate **gain set by a single external resistor** $R_G$ (gain 1 to 1000);
- A low output impedance, a good linearity.

**Gain derivation (three op-amp instrumentation amplifier).** The first stage has two non-inverting amplifiers A1 and A2, with the equal feedback resistors $R_1$ and the gain resistor $R_G$ connected between the inverting inputs. The second stage A3 is a difference amplifier with resistors $R_2$, $R_2$ (input) and $R_3$, $R_3$ (feedback and ground).

By the virtual short, the voltages at the two ends of $R_G$ are $v_1$ and $v_2$, so the current through $R_G$ is

$$I_G = \frac{v_1 - v_2}{R_G}$$

No current enters the op-amp inputs, so the same current flows through both $R_1$ resistors:

$$\begin{gathered}v_{o1} = v_1 + I_GR_1,\qquad v_{o2} = v_2 - I_GR_1\\ v_{o1} - v_{o2} = (v_1 - v_2) + 2I_GR_1 = (v_1 - v_2)\left(1 + \frac{2R_1}{R_G}\right)\end{gathered}$$

The difference amplifier A3 gives

$$v_o = \frac{R_3}{R_2}\left(v_{o2} - v_{o1}\right)\quad\text{(with the inverting input from } v_{o1}\text{)}\ \Rightarrow\ v_o = \frac{R_3}{R_2}(v_{o2} - v_{o1})$$

Taking the polarity so that the output is positive for $v_2 > v_1$ (or by exchanging the inputs):

$$\boxed{A_v = \frac{v_o}{v_2 - v_1} = \left(1 + \frac{2R_1}{R_G}\right)\frac{R_3}{R_2}}$$

For a common-mode input $v_1 = v_2$ the current $I_G = 0$, so $v_{o1} = v_{o2}$ and the first stage has a **unity common-mode gain**, while the differential gain is $1 + 2R_1/R_G$; all the CMRR is therefore improved by this factor, and the second stage only has to reject a small residual. *Example:* $R_1 = 25$ kΩ, $R_2 = R_3 = 10$ kΩ and $R_G = 1$ kΩ give $A_v = (1 + 50) \times 1 = 51$.

```figure caption="Question 7: three op-amp instrumentation amplifier."
fig,ax=plt.subplots(figsize=(6.4,3.8)); ax.axis('off'); ax.set_xlim(0,13); ax.set_ylim(0,7.6)
def amp(x,y,lbl):
    ax.add_patch(Polygon([(x,y-0.9),(x,y+0.9),(x+1.8,y)],fc='#e0f2fe',ec=INK,lw=1.2)); ax.text(x+0.45,y+0.4,'+',fontsize=8); ax.text(x+0.45,y-0.5,'$-$',fontsize=8); ax.text(x+0.75,y,lbl,fontsize=7.5,va='center')
amp(2.2,5.6,'A1'); amp(2.2,1.8,'A2'); amp(8.4,3.7,'A3')
ax.text(0.3,5.95,'$v_1$',fontsize=9); ax.plot([0.8,2.2],[6.0,6.0],color=INK); ax.text(0.3,1.45,'$v_2$',fontsize=9); ax.plot([0.8,2.2],[1.4,1.4],color=INK)
res(ax,(3.4,6.8),(1.6,6.8),'$R_1$',side=1,body=0.9) if False else None
ax.plot([1.8,1.8],[5.2,4.6],color=INK); ax.plot([1.8,2.2],[5.2,5.2],color=INK)
ax.add_patch(Rectangle((1.55,3.05),0.5,1.55,fc='white',ec=INK)); ax.text(2.25,3.85,'$R_G$',fontsize=8)
ax.plot([1.8,1.8],[3.05,2.2],color=INK); ax.plot([1.8,2.2],[2.2,2.2],color=INK)
for yy,t in ((6.9,'$R_1$'),(0.7,'$R_1$')):
    ax.add_patch(Rectangle((2.9,yy-0.2),1.2,0.4,fc='white',ec=INK)); ax.text(3.5,yy,t,fontsize=8,ha='center',va='center')
ax.plot([4.0,4.0],[5.6,6.9],color=INK); ax.plot([2.9,1.2,1.2,2.2],[6.9,6.9,5.2,5.2],color=INK) if False else None
ax.plot([4.0,4.1,4.1],[5.6,5.6,6.9],color=INK); ax.plot([2.9,2.0,2.0],[6.9,6.9,5.2],color=INK)
ax.plot([4.0,4.1,4.1],[1.8,1.8,0.7],color=INK); ax.plot([2.9,2.0,2.0],[0.7,0.7,2.2],color=INK)
ax.plot([4.0,6.0],[5.6,5.6],color=INK); ax.plot([4.0,6.0],[1.8,1.8],color=INK); ax.text(4.3,5.8,'$v_{o1}$',fontsize=8); ax.text(4.3,2.0,'$v_{o2}$',fontsize=8)
ax.add_patch(Rectangle((6.0,5.4),1.2,0.4,fc='white',ec=INK)); ax.text(6.6,5.6,'$R_2$',fontsize=8,ha='center',va='center'); ax.plot([7.2,8.4],[5.6,5.6],color=INK); ax.plot([8.4,8.4],[5.6,4.1],color=INK); ax.plot([8.1,8.4],[4.1,4.1],color=INK) if False else None
ax.add_patch(Rectangle((6.0,1.6),1.2,0.4,fc='white',ec=INK)); ax.text(6.6,1.8,'$R_2$',fontsize=8,ha='center',va='center'); ax.plot([7.2,8.0,8.0],[1.8,1.8,3.3],color=INK); ax.plot([8.0,8.4],[3.3,3.3],color=INK)
ax.plot([8.0,8.0],[5.6,4.1],color=INK) if False else None
ax.plot([10.2,11.8],[3.7,3.7],color=INK); ax.text(11.9,3.7,'$v_o$',fontsize=9,va='center')
ax.text(5.0,3.7,'difference amplifier',fontsize=7,color=MUTED,ha='center')
ax.text(6.5,0.15,'$A_v=(1+2R_1/R_G)\\,R_3/R_2$',fontsize=8.5,ha='center')
```

@s 8
**Drawbacks of the weighted-resistor DAC**

1. It needs a **wide range of resistor values**: for an $n$-bit DAC the resistors are $R, 2R, 4R, \dots, 2^{n-1}R$; for 8 bits the ratio is 128 : 1, for 12 bits 2048 : 1.
2. **High precision is needed for every resistor**, particularly the MSB resistor (an error of the MSB resistor must be less than $\tfrac12$ LSB, e.g. $0.4\ \%$ for 8 bits). Such a range with matched temperature coefficients is hard to fabricate in an IC and expensive.
3. A large resistor (the LSB branch) is slow with the stray capacitance and the op-amp input current gives errors; the **accuracy and the speed fall as the number of bits rises**.
4. The switch resistances also have to be scaled with the weights.

**The R-2R ladder DAC** is used to overcome these drawbacks: **only two resistor values, $R$ and $2R$**, are needed, which is easy to match and fabricate (thin-film) and the scheme is good for many bits.

**Operation (4-bit, voltage mode with the op-amp buffer / inverting form).** The ladder has $R$ in series along the line and $2R$ in each shunt leg, with each leg switched to $V_{ref}$ (bit = 1) or to ground (bit = 0). Looking into any node towards the end of the ladder (from the right), the resistance is always $2R$ (by repeated parallel/series reduction: $2R\parallel2R = R$, $R + R = 2R$), so at every node the current divides in two equal halves. Therefore the contribution of each bit to the node voltage is **halved at each node**, which gives the binary weights $\tfrac12, \tfrac14, \tfrac18, \tfrac1{16}$ (by superposition):

$$V_A = V_{ref}\left(\frac{b_3}{2} + \frac{b_2}{4} + \frac{b_1}{8} + \frac{b_0}{16}\right) = \frac{V_{ref}}{2^4}\left(8b_3 + 4b_2 + 2b_1 + b_0\right)$$

A non-inverting op-amp buffer (or an amplifier of gain $1 + R_f/R_1$) reads this voltage without loading the ladder, so for an $n$-bit DAC

$$\boxed{V_o = \frac{V_{ref}}{2^n}\sum_{i=0}^{n-1}b_i2^i = \frac{V_{ref}}{2^n}\,D}$$

*Example:* $b_3b_2b_1b_0 = 1011$ (D = 11), $V_{ref} = 5$ V: $V_o = 5\times11/16 = 3.4375$ V. The LSB step is $V_{ref}/2^n = 0.3125$ V and the full-scale output is $V_{ref}(1 - 2^{-n})$. In the current-mode (inverted) R-2R ladder, the node voltages are held at virtual ground, so the switch capacitance does not matter and the speed is higher.

```figure caption="Question 8: 4-bit R-2R ladder DAC with a buffer amplifier."
fig,ax=plt.subplots(figsize=(6.6,3.4)); ax.axis('off'); ax.set_xlim(-0.8,13.4); ax.set_ylim(-0.4,5.8)
xs=[2.0,4.6,7.2,9.8]
wire(ax,[(0,3.6),(1.0,3.6)])
res(ax,(0.0,3.6),(0.0,0.9),'2R',side=-1,body=1.0) if False else None
ax.plot([0,0],[3.6,3.1],color=INK); ax.add_patch(Rectangle((-0.2,1.4),0.4,1.7,fc='white',ec=INK)); ax.text(0.35,2.25,'2R',fontsize=7.5); ax.plot([0,0],[1.4,0.6],color=INK); ax.plot([-0.4,0.4],[0.6,0.6],color=INK)
ax.plot([0,10.4],[3.6,3.6],color=INK,lw=1.2)
for x in xs[:3]: pass
for k,x in enumerate(xs):
    if k>0: pass
    ax.plot([x,x],[3.6,3.2],color=INK); ax.add_patch(Rectangle((x-0.2,1.6),0.4,1.6,fc='white',ec=INK)); ax.text(x+0.3,2.4,'2R',fontsize=7.5); ax.plot([x,x],[1.6,1.1],color=INK)
    ax.add_patch(Rectangle((x-0.55,0.55),1.1,0.55,fc='#fde68a',ec=INK)); ax.text(x,0.82,'$b_%d$'%(3-k),fontsize=8,ha='center',va='center'); ax.plot([x,x],[0.55,0.2],color=INK); ax.text(x,-0.2,'$V_{ref}$ / gnd',fontsize=6.3,ha='center')
    ax.plot([x],[3.6],'o',color=INK,ms=3)
for x in (3.3,5.9,8.5):
    ax.add_patch(Rectangle((x-0.4,3.4),0.8,0.4,fc='white',ec=INK)); ax.text(x,3.6,'R',fontsize=7.5,ha='center',va='center')
ax.add_patch(Polygon([(10.8,3.0),(10.8,4.2),(12.2,3.6)],fc='#e0f2fe',ec=INK,lw=1.2)); ax.text(11.0,3.95,'+',fontsize=8); ax.text(11.0,3.0,'$-$',fontsize=8)
ax.plot([10.4,10.8],[3.6,3.6],color=INK) if False else None
ax.plot([10.4,10.8],[3.85,3.85],color=INK); ax.plot([9.8,9.8],[3.6,3.85],color=INK); ax.plot([9.8,10.4],[3.85,3.85],color=INK)
ax.plot([12.2,13.0],[3.6,3.6],color=INK); ax.text(13.05,3.6,'$V_o$',fontsize=9,va='center'); ax.plot([10.5,10.5,12.6,12.6],[3.15,2.4,2.4,3.6],color=INK,lw=1.0)
ax.text(5.0,5.0,'$V_o=\\dfrac{V_{ref}}{16}(8b_3+4b_2+2b_1+b_0)$',fontsize=9,ha='center')
```

@s 9
**Sample-and-hold (S/H) circuit.** It samples an analogue voltage at a precise instant and **holds it constant** while an ADC converts it, because the conversion (SAR, dual-slope) needs a stable input; without it the input would change by more than 1 LSB during the conversion.

**Circuit.** An analogue switch $S$ (a MOSFET, driven by the sample/hold logic input), a **hold capacitor $C_H$** and two op-amp buffers: A1 at the input (high input impedance, low output impedance, so $C_H$ charges quickly) and A2 at the output (high impedance, so the capacitor does not discharge through the load).

**Operation**

- **Sample mode** (control high): the switch is closed, $C_H$ charges through the on-resistance $R_{on}$ and the output follows the input: $v_o(t) = v_{in}(t)$, with the time constant $\tau = (R_{on} + R_{o1})C_H$.
- **Hold mode** (control low): the switch opens at the instant of sampling; $C_H$ keeps the voltage that it had at that instant, and the output buffer holds it at the output ($v_o = v_{in}(t_s)$) until the next sample command. The ADC converts it during this time. The held voltage falls (droop) slowly through the leakage and the amplifier bias current, $\dfrac{dv}{dt} = \dfrac{I_{leak}}{C_H}$.

```figure caption="Question 9: sample-and-hold circuit (left) and its waveforms (right)."
fig,axs=plt.subplots(1,2,figsize=(6.8,2.7),gridspec_kw={'width_ratios':[1.1,1]})
ax=axs[0]; ax.axis('off'); ax.set_xlim(-0.3,9.5); ax.set_ylim(-0.4,4.4)
ax.text(-0.2,2.7,'$v_{in}$',fontsize=8.5); ax.plot([0.7,1.4],[2.5,2.5],color=INK)
ax.add_patch(Polygon([(1.4,1.9),(1.4,3.1),(2.8,2.5)],fc='#e0f2fe',ec=INK)); ax.text(1.6,2.5,'A1',fontsize=7)
ax.plot([2.8,3.6],[2.5,2.5],color=INK); ax.plot([3.6,4.8],[2.5,2.8],color=INK,lw=1.4); ax.plot([4.8,5.6],[2.8,2.5],color=INK) if False else None
ax.plot([3.6,3.6],[2.5,2.5],'o',color=INK,ms=3); ax.plot([4.8,5.4],[2.5,2.5],color=INK); ax.plot([5.4,5.4],[2.5,0.9],color=INK); ax.plot([5.1,5.7],[1.6,1.6],color=INK,lw=2.0); ax.plot([5.1,5.7],[1.35,1.35],color=INK,lw=2.0); ax.plot([5.4,5.4],[1.35,0.9],color=INK); ax.plot([5.0,5.8],[0.9,0.9],color=INK); ax.text(5.9,1.45,'$C_H$',fontsize=8)
ax.plot([5.4,6.1],[2.5,2.5],color=INK); ax.add_patch(Polygon([(6.1,1.9),(6.1,3.1),(7.5,2.5)],fc='#e0f2fe',ec=INK)); ax.text(6.3,2.5,'A2',fontsize=7); ax.plot([7.5,8.6],[2.5,2.5],color=INK); ax.text(8.65,2.5,'$v_o$',fontsize=8.5,va='center')
ax.plot([3.6,4.8],[2.5,2.5],color=INK,lw=0); ax.text(4.2,3.15,'S',fontsize=8,ha='center'); ax.plot([4.0,4.7],[2.55,3.0],color=INK,lw=1.4); ax.plot([4.8,4.8],[2.5,2.5],'o',color=INK,ms=3)
ax.text(4.2,3.9,'sample / hold control',fontsize=6.8,ha='center',color=ACCENT)
ax=axs[1]; t=np.linspace(0,10,600); vin=1.5+np.sin(t*0.9)*1.0+0.3*np.sin(t*2.3)
ctrl=((t%5)<2).astype(float)
vo=vin.copy(); hold=None
for i in range(len(t)):
    if ctrl[i]==0:
        if hold is None: hold=vo[i-1]
        vo[i]=hold-0.004*(t[i]-t[i-1]) if False else hold
    else: hold=None
ax.plot(t,vin,color=MUTED,lw=1.0,label='$v_{in}$'); ax.plot(t,vo,color=INK,lw=1.7,label='$v_o$'); ax.step(t,ctrl*0.45-0.65,color=ACCENT,lw=1.3,label='S/H control')
ax.legend(fontsize=6.5,loc='upper right',ncol=3); ax.set_xlabel('time'); ax.set_ylim(-0.8,3.4); ax.text(1.0,-0.05,'sample',fontsize=6.5); ax.text(3.0,-0.05,'hold',fontsize=6.5)
```

**Aperture time and acquisition time**

- **Aperture time** $t_{ap}$: the time that the switch takes from the instant the hold command is given to the instant the switch is **completely open** (the signal is finally disconnected from $C_H$). It is the uncertainty in the sampling instant: because the input is still changing during $t_{ap}$, the held value has an **aperture error** $\Delta v = \dfrac{dv_{in}}{dt}\,t_{ap}$. For a sine wave of amplitude $V_m$ and frequency $f$, the maximum rate of change is $2\pi fV_m$, so for an $n$-bit ADC the aperture time must satisfy

$$t_{ap} \le \frac{1}{2^{n}\,\pi f}\quad\text{(error} \le \tfrac12\text{ LSB)}$$

(e.g. for 8 bits and 1 kHz, $t_{ap} \le 1.2\ \mu$s; the **aperture jitter** is the variation in $t_{ap}$ from sample to sample.)

- **Acquisition time** $t_{acq}$: the time required, after the sample command, for the hold capacitor to **charge** to the input voltage within a specified error band (e.g. $\pm0.01\ \%$), starting from the worst case (a full-scale step). It includes the switch delay, the slewing of the buffer and the exponential settling $\tau = (R_{on} + R_o)C_H$:

$$t_{acq} \approx \tau\,\ln\!\left(\frac{V_{FS}}{\text{error}}\right)\approx 9.2\,\tau\ \ (0.01\ \%)$$

The sample period must be at least $t_{acq}$ (the sampling rate is limited by it), a **small $C_H$** gives a short acquisition time but a larger droop and charge-injection error, a **large $C_H$** gives a small droop but a long acquisition time: a compromise.

@s 10
**Instrument transformers.** The ordinary meters cannot be connected directly in high-current or high-voltage circuits because of the insulation and the size. Instrument transformers **step down** the current (CT) or the voltage (PT / VT) to the standard low values (5 A or 1 A; 110 V or 63.5 V), isolate the instruments from the high voltage, and allow standard meters and relays to be used.

**(1) Current transformer (CT): measuring a high current.** The primary has very few turns (often a single bar through the core) in **series** with the line carrying the high current $I_p$; the secondary has many turns and feeds an **ammeter or the current coil of a wattmeter or a relay**, whose impedance (the burden) is very low, so the CT works nearly short-circuited. The ideal ratio:

$$\begin{gathered}\frac{I_p}{I_s} = \frac{N_s}{N_p} = K_n\ \ (\text{nominal ratio, e.g. } 1000/5\text{ A} = 200) \\ I_p = K_nI_s\end{gathered}$$

The line current is read as the ammeter reading times $K_n$ (e.g. an ammeter reading 4.2 A with a 1000/5 CT shows 840 A).

*Precautions and errors:* the **secondary must never be open-circuited** while the primary carries current (the flux rises, the core saturates and a dangerous high voltage $e = N_s\,d\Phi/dt$ appears and the core overheats); the secondary is earthed. The actual ratio differs from the nominal because of the magnetising and loss components of the primary current $I_0$: the **ratio error** $\dfrac{K_n - R}{R}\times100\ \%$ with $R$ the actual ratio, and the **phase-angle error** $\delta$ between $-I_s$ and $I_p$; these are reduced by a high-permeability core (nickel-iron, silicon steel, low flux density), a small burden and the turns compensation. Accuracy classes 0.1 to 1 for metering and 5P / 10P for protection.

**(2) Potential (voltage) transformer (PT / VT): measuring a high voltage.** The primary (many turns) is connected **in parallel** across the high-voltage line, the secondary (fewer turns) feeds a **voltmeter or the pressure coil of a wattmeter or energy meter**, with a high impedance (a small burden), so the transformer works nearly open-circuited. The ratio:

$$\begin{gathered}\frac{V_p}{V_s} = \frac{N_p}{N_s} = K_n\ \ (\text{e.g. } 11\,000/110\text{ V} = 100) \\ V_p = K_nV_s\end{gathered}$$

*Precautions and errors:* the **secondary must never be short-circuited** (a large current would burn it, since the impedance is low); the secondary is earthed and fused; the ratio and phase-angle errors come from the voltage drops in the winding resistance and leakage reactance and from the magnetising current; they are made small by a low winding impedance, a low flux density, a small burden.

**Measurement of power** in a high-voltage, high-current circuit: the wattmeter's current coil is fed from the CT and its pressure coil from the PT, so $P = (\text{wattmeter reading})\times K_{CT}\times K_{PT}$ (corrected for the phase-angle errors). A CT in each phase also feeds the overcurrent relays and the energy meters.

```figure caption="Question 10: measurement of high current with a CT and high voltage with a PT; power measurement using both."
fig,ax=plt.subplots(figsize=(6.8,3.3)); ax.axis('off'); ax.set_xlim(0,14); ax.set_ylim(0,6.6)
ax.plot([0.3,13.6],[5.6,5.6],color=INK,lw=2.0); ax.plot([0.3,13.6],[0.8,0.8],color=INK,lw=2.0); ax.text(0.3,5.85,'High-voltage line',fontsize=7.5); ax.text(13.6,5.95,'load',fontsize=8,ha='right')
ax.add_patch(Circle((3.2,5.6),0.55,fc='white',ec=INK,lw=1.3)); ax.add_patch(Circle((3.2,4.45),0.55,fc='white',ec=INK,lw=1.3)); ax.text(3.2,3.6,'CT\n$I_p$ : $I_s$ = $N_s$ : $N_p$',fontsize=7,ha='center')
ax.plot([3.2,3.2],[3.9,3.2],color=INK) if False else None
ax.add_patch(Circle((5.2,2.4),0.5,fc='#fde68a',ec=INK)); ax.text(5.2,2.4,'A',ha='center',va='center',fontsize=9,weight='bold'); ax.plot([2.9,2.9,4.7,4.7],[4.0,2.4,2.4,2.4],color=INK,lw=1.0); ax.plot([3.5,3.5,5.9,5.9],[4.0,1.6,1.6,2.4],color=INK,lw=1.0) if False else None
ax.plot([3.6,3.6,5.7,5.7],[4.0,1.9,1.9,2.4],color=INK,lw=1.0)
ax.add_patch(Circle((9.2,4.0),0.55,fc='white',ec=INK,lw=1.3)); ax.add_patch(Circle((9.2,2.85),0.55,fc='white',ec=INK,lw=1.3)); ax.text(9.2,1.95,'PT   $V_p$ : $V_s$ = $N_p$ : $N_s$',fontsize=7,ha='center')
ax.plot([8.6,8.6],[5.6,3.0],color=INK,lw=1.0) if False else None
ax.plot([9.2,9.2],[5.6,4.55],color=INK,lw=1.2); ax.plot([9.2,9.2],[2.3,0.8],color=INK,lw=1.2)
ax.add_patch(Circle((12.0,3.4),0.55,fc='#bbf7d0',ec=INK)); ax.text(12.0,3.4,'V',ha='center',va='center',fontsize=9,weight='bold'); ax.plot([9.75,12.0,12.0],[3.4,3.4,3.4],color=INK,lw=1.0) if False else None
ax.plot([9.75,11.45],[3.4,3.4],color=INK,lw=1.0)
ax.text(7.0,0.25,'$I = K_{CT}\\,I_{ammeter}$,   $V = K_{PT}\\,V_{voltmeter}$,   $P = K_{CT}K_{PT}\\,W$',fontsize=8,ha='center')
```
