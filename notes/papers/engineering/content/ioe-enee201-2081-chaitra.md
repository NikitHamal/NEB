---
file: NEBians-IOE-Past-Paper-Instrumentation-and-Measurement-ENEE201-2081-Chaitra.pdf
subject: Instrumentation and Measurement
level: BE · Year II / Part I
code: ENEE 201
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular paper (new course), BE Electrical Engineering (BEL), Year II / Part I. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt All questions · The figures in the margin indicate Full Marks · Assume suitable data if necessary</small>

@q 1
What do you understand by an instrumentation system? Explain the function of each of its components with an example. [[4]]

@q 2
A voltmeter whose accuracy is 2% of the full scale reading is used on its 0-100V scale. It is used to measure a voltage of 30V and 63V. Calculate the possible error of both readings. Comment on your answer. [[4]]

@q 3
An AC bridge circuit is working at 1000Hz. Arm AB has 0.2 µF pure capacitance, arm BC has 500 Ω resistance, arm CD contains an unknown impedance and arm DA has 300 Ω resistance in parallel with 0.1 µF capacitor. Find the constant of arm CD considering it as a series circuit. [[6]]

@q 4
Prove that linearity and sensitivity are two conflicting requirements of a potentiometer. [[4]]

@q 5
Explain the working of a capacitive transducer for liquid level measurement. [[4]]

@q 6
What is piezoelectric transducer? Define the voltage sensitivity and charge sensitivity. Give the equivalent circuit for piezoelectric transducer. Derive the expression for the output voltage by making suitable assumptions. [[6]]

@q 7
Explain the features of an instrumentation amplifier and derive the expression for its gain. [[6]]

@q 8
Explain the working and application of op-amp as:

i) An integrator

ii) Subtractor [[6]]

@q 9
Describe how digital to analog conversion is achieved by using the R-2R Ladder network. [[4]]

@q 10
What do you understand by sample and Hold circuit? Explain the role of multiplexer in a data acquisition system with a neat sketch. [[6]]

@q 11
State and explain sampling theorem. [[4]]

@q 12
Explain the working principle of dynamometer type wattmeter and also prove that the deflection torque is directly proportional to power consumed by the load in both AC and DC circuit. [[6]]

<!-- SOLUTIONS -->

@s 1
**Instrumentation system.** An instrumentation system is a set of devices that **measures a physical quantity, converts it into a usable form and presents, records or uses it** (display, storage, control). Its components, with their functions:

1. **Sensor / transducer (primary element):** senses the measurand and converts it to an electrical signal (thermocouple: temperature to mV).
2. **Signal conditioning:** amplifies, filters, linearises, excites (bridge), converts (current to voltage), isolates and brings the signal to a level suitable for the next stage.
3. **Signal processing and data conversion:** a sample-and-hold, **ADC** and a microcontroller / processor that compute, calibrate, scale to engineering units, apply control laws.
4. **Output / presentation:** display (LCD, meter), recorder / data logger, alarm, communication (to PLC, SCADA, the cloud) and, in a control system, an actuator.
5. **Power supply and calibration source** (reference).

*Example: digital thermometer for a furnace.* A K-type thermocouple (sensor) gives 41 µV/°C; an instrumentation amplifier with cold-junction compensation and a filter (conditioning) brings it to 0 to 5 V; a 10-bit ADC and a microcontroller (processing) linearise it and convert it to °C; an LCD shows the temperature (presentation) and a relay trips an alarm above the limit.

```figure caption="Question 1: general instrumentation system."
fig,ax=plt.subplots(figsize=(6.8,1.9)); ax.axis('off'); ax.set_xlim(0,15); ax.set_ylim(0,3.4)
def bx(x,y,w,h,t,fc='#e0f2fe'):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=INK,lw=1)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=7)
bx(0.1,1.0,2.2,1.3,'Measurand\n(temperature, flow, ...)','#fef9c3'); bx(2.9,1.0,2.2,1.3,'Sensor /\ntransducer'); bx(5.7,1.0,2.2,1.3,'Signal\nconditioning'); bx(8.5,1.0,2.0,1.3,'S/H + ADC +\nprocessor','#dbeafe'); bx(11.1,1.0,2.0,1.3,'Display /\nrecorder','#dcfce7'); bx(13.6,1.0,1.3,1.3,'Control\nactuator','#dcfce7')
for a,b in (((2.3,1.65),(2.9,1.65)),((5.1,1.65),(5.7,1.65)),((7.9,1.65),(8.5,1.65)),((10.5,1.65),(11.1,1.65)),((13.1,1.65),(13.6,1.65))): arrow(ax,a,b,None,color=INK)
```

@s 2
The accuracy of the instrument is $\pm2\ \%$ of the **full-scale** reading, so the limiting (guarantee) error is the same for every reading on the 0-100 V range:

$$\Delta V = \pm\frac{2}{100}\times100 = \pm2\ \text{V}$$

| Reading | Possible error | Relative error |
|---|---|---|
| 30 V | $\pm2$ V (true value between 28 V and 32 V) | $\dfrac{2}{30}\times100 = \mathbf{\pm6.67\ \%}$ |
| 63 V | $\pm2$ V (true value between 61 V and 65 V) | $\dfrac{2}{63}\times100 = \mathbf{\pm3.17\ \%}$ |

**Comment.** The absolute error is constant ($\pm2$ V), but the **relative (percentage) error is larger for the smaller reading**: 6.67 % at 30 V against 3.17 % at 63 V, and it would be 2 % only at the full scale. Therefore the instrument should be used so that the pointer deflects in the **upper part (more than two thirds) of the scale**; a lower range (e.g. 0 to 50 V for the 30 V reading, giving $\pm1$ V, 3.3 %) gives a more accurate result.

@s 3
**Arms:** $Z_{AB} = \dfrac{1}{j\omega C_1}$ with $C_1 = 0.2\ \mu\text{F}$; $Z_{BC} = 500\ \Omega$; $Z_{CD} = Z_x$ (unknown); $Z_{DA} = 300\ \Omega \parallel 0.1\ \mu\text{F}$. $\omega = 2\pi\times1000 = 6283.2$ rad/s.

**Balance condition** (product of opposite arms): $Z_{AB}Z_{CD} = Z_{BC}Z_{DA}$, so $Z_x = \dfrac{Z_{BC}Z_{DA}}{Z_{AB}}$.

$$Z_{AB} = \frac{1}{j(6283.2)(0.2\times10^{-6})} = -j795.77\ \Omega$$

$$Z_{DA} = \frac{1}{\dfrac{1}{300} + j(6283.2)(0.1\times10^{-6})} = \frac{1}{0.003333 + j0.0006283} = 289.71 - j54.61\ \Omega$$

$$Z_x = \frac{500\,(289.71 - j54.61)}{-j795.77} = j0.62832\,(289.71 - j54.61) = 34.31 + j182.03\ \Omega$$

**Series equivalent of arm CD:**

$$\boxed{R_x = 34.3\ \Omega,\qquad L_x = \frac{182.03}{\omega} = \frac{182.03}{6283.2} = 28.97\ \text{mH}}$$

so the unknown arm is an **inductor of 28.97 mH with a series resistance of 34.3 Ω** (an inductive coil with $Q = \omega L/R = 5.3$).

*Check with the parallel equivalent:* $Y_x = 1/Z_x = 0.001 - j0.005305$ S, i.e. $R_p = 1000\ \Omega$ in parallel with $L_p = 1/(\omega\times0.005305) = 30.0$ mH, which gives the same impedance.

@s 4
**Potentiometer (resistive displacement transducer).** A wire-wound or conductive-plastic resistance $R_p$ of length $L$, excited by $E$, with the slider at a distance $x$; $x_t = x/L$ is the fraction of the travel. With **no load**:

$$e_o = E\,\frac{x}{L}\quad\text{(perfectly linear), sensitivity } S = \frac{e_o}{x} = \frac{E}{L}$$

**With a load $R_L$** across the slider (e.g. the meter or the next stage), the lower part $x_tR_p$ is in parallel with $R_L$:

$$e_o = \frac{E\,\dfrac{R_Lx_tR_p}{R_L + x_tR_p}}{(1 - x_t)R_p + \dfrac{R_Lx_tR_p}{R_L + x_tR_p}}\quad\Rightarrow\quad \frac{e_o}{E} = \frac{x_t}{1 + \dfrac{R_p}{R_L}\,x_t(1 - x_t)}$$

The deviation from the linear law $x_t$ (the non-linearity error) is

$$\varepsilon = \frac{e_o}{E} - x_t = -\frac{\dfrac{R_p}{R_L}x_t^2(1 - x_t)}{1 + \dfrac{R_p}{R_L}x_t(1 - x_t)}\approx -\frac{R_p}{R_L}\,x_t^2(1 - x_t)\quad(R_p \ll R_L)$$

Its magnitude is maximum at $x_t = 2/3$ (put $d[x_t^2(1 - x_t)]/dx_t = 0$): $|\varepsilon|_{max} = \dfrac{4}{27}\dfrac{R_p}{R_L} = 0.148\dfrac{R_p}{R_L}$. For good **linearity** we need the ratio $R_p/R_L$ small, i.e. a low $R_p$.

**Sensitivity.** The sensitivity $S = E/L$ is increased by raising the excitation $E$. But the potentiometer dissipates the power $P = E^2/R_p$, which is limited by its rating (heating): $E_{max} = \sqrt{PR_p}$. So

$$S_{max} = \frac{\sqrt{PR_p}}{L}$$

and **a high sensitivity needs a high $R_p$** (a high permissible voltage, with the same power), whereas **high linearity needs a low $R_p$** (a small $R_p/R_L$). The two requirements need opposite changes of $R_p$ (for a given load and power rating), so **linearity and sensitivity conflict**: raising $R_p$ increases $S$ as $\sqrt{R_p}$, but the loading non-linearity grows in proportion to $R_p$. The compromise is the design with a load resistance as high as possible (an electronic buffer or an op-amp), with $R_p/R_L \le 0.01$ giving an error below $0.15\ \%$.

@s 5
**Capacitive transducer for liquid-level measurement.** The probe is a **cylindrical capacitor** formed by two concentric metal tubes (or a rod inside a tube, inner radius $a$, outer radius $b$) of the total height $H$, placed vertically in the tank. The liquid enters the gap and rises to the level $h$; the part $h$ of the capacitor has the **liquid** as the dielectric (relative permittivity $\varepsilon_r$) and the remaining part $H - h$ has **air** ($\varepsilon_r \approx 1$). The two parts are in parallel:

$$C = \frac{2\pi\varepsilon_0\varepsilon_rh}{\ln(b/a)} + \frac{2\pi\varepsilon_0(H - h)}{\ln(b/a)} = \frac{2\pi\varepsilon_0}{\ln(b/a)}\left[H + (\varepsilon_r - 1)h\right]$$

$$\boxed{C = C_0 + kh,\qquad C_0 = \frac{2\pi\varepsilon_0H}{\ln(b/a)},\quad k = \frac{2\pi\varepsilon_0(\varepsilon_r - 1)}{\ln(b/a)}}$$

so the capacitance varies **linearly with the level $h$** (for a liquid with a constant $\varepsilon_r$; for water $\varepsilon_r \approx 80$, for oil about 2 to 3). The capacitance is measured by an a.c. bridge, by an oscillator whose frequency $f = 1/(2\pi\sqrt{LC})$ depends on $C$, or by a capacitance-to-voltage converter, and gives a signal proportional to the level.

*Practical points:* for a **conducting liquid** (water) the electrode is coated with an insulating layer (PTFE), the liquid becoming the second plate; the sensor works with no moving parts and no contact for solids and powders too; the changes of temperature, composition and permittivity of the liquid have to be compensated (a reference capacitor); it is used for fuel gauges, chemical tanks and silos. *Sensitivity* $k = 2\pi\varepsilon_0(\varepsilon_r - 1)/\ln(b/a)$: for $\varepsilon_r = 2.5$, $b/a = 2$: $k = 120\ \text{pF/m}$.

@s 6
**Piezoelectric transducer.** A transducer that depends on the **piezoelectric effect**: when a mechanical force (stress) is applied to certain crystals (quartz, Rochelle salt, barium titanate, PZT), **an electric charge appears on the opposite faces**, proportional to the force: $Q = dF$. It is a self-generating (active) transducer for force, pressure, acceleration and vibration (dynamic measurements only, because the charge leaks away).

**Charge sensitivity** $d$ (or $S_q$): the charge produced per unit applied force,

$$d = \frac{Q}{F}\ \ \text{(C/N, e.g. quartz } 2.3\ \text{pC/N)}$$

**Voltage sensitivity** $g$ (or $S_v$): the electric field (open-circuit voltage gradient) per unit applied stress, $g = \dfrac{E_p}{\sigma} = \dfrac{V/t}{F/A}$ (V m/N), related to $d$ by $g = \dfrac{d}{\varepsilon}$ (with $\varepsilon = \varepsilon_r\varepsilon_0$ the permittivity). For a crystal of thickness $t$ and area $A$: $V = g\,t\,\sigma = \dfrac{dF}{C_p}$ with $C_p = \varepsilon A/t$.

**Equivalent circuit.** The crystal behaves as a **charge generator $q = dF$ in parallel with its capacitance $C_p$ and its leakage (insulation) resistance $R_p$**; the cable capacitance $C_c$ and the amplifier input capacitance $C_a$ and resistance $R_a$ are connected in parallel. (An equivalent form is a voltage source $e = q/C_p$ in series with $C_p$.)

```figure caption="Question 6: equivalent circuit of a piezoelectric transducer with its cable and amplifier."
fig,ax=plt.subplots(figsize=(5.6,2.9)); ax.axis('off'); ax.set_xlim(-0.5,10.5); ax.set_ylim(-0.4,4.6)
isrc(ax,(0,0.2),(0,3.8),'$q=dF$',side=-1,off=0.9)
wire(ax,[(0,3.8),(8.6,3.8)]); wire(ax,[(0,0.2),(8.6,0.2)])
for x,l in ((2.2,'$C_p$'),(4.2,'$R_p$'),(6.0,'$C_c + C_a$'),(8.2,'$R_a$')): 
    if l in ('$C_p$','$C_c + C_a$'): cap(ax,(x,3.8),(x,0.2),l,side=1,gap=0.18,off=0.8)
    else: res(ax,(x,3.8),(x,0.2),l,side=1,body=1.2)
arrow(ax,(9.2,3.2),(9.2,0.8),None,color=ACCENT); ax.text(9.35,2.0,'$e_o$',fontsize=10,color=ACCENT)
```

**Output voltage.** Let $C = C_p + C_c + C_a$ and $R = \dfrac{R_pR_a}{R_p + R_a}$. For a sinusoidal force $F = F_m\sin\omega t$ the charge generator drives the current $i = dq/dt = j\omega dF$ into the parallel combination $R \parallel C$:

$$e_o = i\,\frac{R}{1 + j\omega RC} = \frac{j\omega d\,R\,F}{1 + j\omega RC}$$

$$\boxed{\left|\frac{e_o}{F}\right| = \frac{d}{C}\cdot\frac{\omega RC}{\sqrt{1 + (\omega RC)^2}}}$$

**Assumption of a good (high-frequency) response**, $\omega RC \gg 1$ ($\omega \gg 1/RC$, i.e. $f \gg f_c = \dfrac{1}{2\pi RC}$):

$$e_o \approx \frac{dF}{C} = \frac{dF}{C_p + C_c + C_a}$$

so the output is proportional to the force and independent of the frequency; **the lower cut-off frequency** is $f_c = 1/(2\pi RC)$ (so a high $R_a$ is needed to measure low frequencies; a true static force cannot be measured). The output depends on the cable capacitance, so a **charge amplifier** (with feedback capacitor $C_f$, $e_o = -q/C_f$) is used to make the sensitivity independent of the cable length.

@s 7
**Features of an instrumentation amplifier**

1. A very **high input impedance** at both inputs (balanced), so no loading of the sensor or bridge.
2. A very **high common-mode rejection ratio** (80 to 120 dB), amplifying only the difference of the two inputs.
3. A **low drift, low offset voltage and low noise**, a good linearity and a low output impedance.
4. The **gain is set by one resistor $R_G$**, adjustable from 1 to 1000, stable and accurate (matched resistors in the same package).
5. A differential-input, single-ended-output stage; it is used for strain-gauge bridges, thermocouples, ECG and so on.

**Gain (three op-amp circuit: A1, A2 input buffers with $R_1$, $R_G$; A3 difference amplifier with $R_2$, $R_3$).** By the virtual short the ends of $R_G$ are at $v_1$ and $v_2$:

$$\begin{gathered}I_G = \frac{v_1 - v_2}{R_G} \\ v_{o1} = v_1 + I_GR_1 \\ v_{o2} = v_2 - I_GR_1\end{gathered}$$

$$v_{o1} - v_{o2} = (v_1 - v_2)\left(1 + \frac{2R_1}{R_G}\right)$$

The output stage with the equal ratios $R_3/R_2$ gives $v_o = \dfrac{R_3}{R_2}(v_{o2} - v_{o1})$ (the inputs are labelled so that the gain is positive for $v_2 > v_1$), so

$$\boxed{A_v = \frac{v_o}{v_2 - v_1} = \left(1 + \frac{2R_1}{R_G}\right)\frac{R_3}{R_2}}$$

For a common-mode input $v_1 = v_2$ we get $I_G = 0$, so the first stage has a unity common-mode gain and the differential gain is $1 + 2R_1/R_G$ (so the overall CMRR is improved by this factor). *Example:* $R_1 = 25$ kΩ, $R_2 = R_3 = 10$ kΩ, $R_G = 1$ kΩ: $A_v = 51$.

@s 8
**(i) Integrator.** An inverting op-amp with a resistor $R$ in the input and a capacitor $C$ in the feedback. The virtual earth at the inverting terminal gives $i_R = v_{in}/R$ and $i_C = -C\,dv_o/dt$, with $i_R = i_C$:

$$\boxed{v_o(t) = -\frac{1}{RC}\int_0^tv_{in}(\tau)\,d\tau + v_o(0)}$$

The output is the **time integral of the input**, inverted and scaled by $1/RC$. For a constant input $V$ the output is a ramp, $v_o = -Vt/RC$; for a square-wave input it is a triangular wave; for a sine wave, a cosine ($90^\circ$ shift). In the frequency domain $A(j\omega) = -\dfrac{1}{j\omega RC}$ (a low-pass filter with the unity-gain frequency $1/2\pi RC$). A **resistor $R_f$ in parallel with $C$** (about $10R$) limits the d.c. gain to $R_f/R$ and stops the drift to saturation (offset and bias currents).

*Applications:* ramp and triangular-wave generators, the dual-slope ADC, the analogue computer (solving differential equations), active low-pass filters, charge amplifiers, the integration of the signals from the accelerometers (velocity from acceleration), the PID controller (integral term).

**(ii) Subtractor (difference amplifier).** The input $v_1$ goes to the inverting input through $R_1$ with the feedback $R_f$, and $v_2$ to the non-inverting input through $R_1$ with the divider resistor $R_f$ to ground. By superposition:

$$v_o = -\frac{R_f}{R_1}v_1 + \left(1 + \frac{R_f}{R_1}\right)\frac{R_f}{R_1 + R_f}\,v_2$$

$$\boxed{v_o = \frac{R_f}{R_1}\,(v_2 - v_1)}$$

The output is **proportional to the difference** of the inputs, with the gain $R_f/R_1$ (the common-mode signal is rejected if the resistor pairs are well matched). The input resistances are modest ($R_1$ and $R_1 + R_f$), so buffers are often added.

*Applications:* amplifying the output of a bridge (strain gauge, thermocouple), the error amplifier of the control system ($e = r - y$), the differential receiver of the balanced line, the current sensing, the audio mixers and the first stage of the instrumentation amplifier.

@s 9
**R-2R ladder DAC.** A network with only two resistor values: $R$ in series along the ladder and $2R$ in each shunt leg; the $2R$ leg of the bit $b_i$ is switched to $V_{ref}$ (bit = 1) or to ground (bit = 0); the last leg (the LSB end) is terminated with an extra $2R$.

**Principle.** Looking from any node towards the LSB end the resistance is always $2R$ ($2R \parallel 2R = R$, then $R + R = 2R$, repeated), so at every node the current splits equally and the voltage contribution of each source is **halved at each successive node**. By superposition, the voltage at the output node (the MSB end) with a buffer is

$$V_o = V_{ref}\left(\frac{b_{n-1}}{2} + \frac{b_{n-2}}{4} + \dots + \frac{b_0}{2^n}\right) = \frac{V_{ref}}{2^n}\sum_{i=0}^{n-1}b_i2^i = \frac{V_{ref}}{2^n}D$$

A non-inverting op-amp buffer (gain 1) isolates the ladder from the load. *Example:* 4 bits, 1011 (D = 11), $V_{ref} = 5$ V: $V_o = 5\times\dfrac{11}{16} = 3.4375$ V; the resolution (the LSB) is $5/16 = 0.3125$ V and the full scale $V_{ref}(1 - 2^{-4}) = 4.6875$ V.

*Advantages:* only two resistor values, matched easily in an IC (thin film); good accuracy for more bits; the switches see a constant impedance, with a fast, simple design (the inverted R-2R form works with the nodes at a virtual ground). It overcomes the wide-range resistors of the weighted-resistor DAC.

@s 10
**Sample-and-hold circuit.** A circuit which **samples** the analogue input at a command instant and **holds** the sampled value constant for the required time. A MOSFET switch, a hold capacitor $C_H$ and input and output buffer amplifiers form it: in the *sample* mode the switch is closed and $C_H$ charges, so the output follows the input; in the *hold* mode the switch is open, $C_H$ keeps the voltage and the output buffer holds it (the droop rate is $I_{leak}/C_H$). It is needed because an ADC needs a steady input during its conversion time, otherwise the error is more than 1 LSB for any changing signal; the **aperture time** and the **acquisition time** of the switch limit its speed.

**Role of the multiplexer in a data acquisition system (DAS).** A multi-channel DAS measures many sensors with **one** set of signal conditioning, S/H and ADC. The **analogue multiplexer** (a set of electronically controlled analogue switches, e.g. the CD4051 8:1 or ADG, controlled by the address lines from the controller) **connects one input channel at a time to the common output** in sequence (or a chosen order), so:

1. the **single ADC (and S/H, amplifier) is shared** by $N$ channels: cost, size and power are reduced;
2. the channel selection is by the digital address, so scanning, a random access and a programmable sequence are easy;
3. the conversion rate per channel is the ADC rate divided by $N$; the S/H holds the sample of the selected channel while the ADC converts, then the MUX moves to the next channel (the settling time of the MUX must be allowed for);
4. the off-channel leakage, the on-resistance (which with the input impedance causes an error) and the cross-talk limit the accuracy, so a buffer or a programmable-gain amplifier follows the MUX.

```figure caption="Question 10: multi-channel data acquisition system with an analogue multiplexer, sample-and-hold and ADC."
fig,ax=plt.subplots(figsize=(6.8,3.0)); ax.axis('off'); ax.set_xlim(0,15); ax.set_ylim(0,6.4)
def bx(x,y,w,h,t,fc='#e0f2fe'):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=INK,lw=1)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=7)
for k,y in enumerate((5.0,3.8,2.6,1.4)):
    bx(0.1,y-0.3,1.6,0.6,'Sensor %d'%(k+1),'#fef9c3'); bx(2.1,y-0.3,1.7,0.6,'conditioning'); arrow(ax,(1.7,y),(2.1,y),None,color=INK)
    ax.plot([3.8,5.2],[y,y],color=INK,lw=1.0)
ax.add_patch(Polygon([(5.2,0.8),(5.2,5.6),(6.8,4.4),(6.8,2.0)],fc='#dbeafe',ec=INK,lw=1.2)); ax.text(6.0,3.2,'MUX',fontsize=8,ha='center',weight='bold')
bx(7.6,2.7,1.8,1.0,'Sample &\nhold','#fde68a'); bx(10.0,2.7,1.6,1.0,'ADC','#dbeafe'); bx(12.2,2.7,2.5,1.0,'Computer /\nprocessor','#dcfce7')
for a,b in (((6.8,3.2),(7.6,3.2)),((9.4,3.2),(10.0,3.2)),((11.6,3.2),(12.2,3.2))): arrow(ax,a,b,None,color=INK)
bx(7.6,0.6,7.1,1.0,'Control logic: channel address, S/H command, start of conversion, end of conversion','#f1f5f9')
ax.plot([6.0,6.0],[1.6,1.1],color=ACCENT); ax.plot([6.0,7.6],[1.1,1.1],color=ACCENT); ax.plot([8.5,8.5],[1.6,2.7],color=ACCENT); ax.plot([10.8,10.8],[1.6,2.7],color=ACCENT)
```

@s 11
**Sampling theorem (Nyquist-Shannon).** *A band-limited continuous-time signal $x(t)$ with the highest frequency component $f_m$ (no spectrum above $f_m$) can be completely recovered from its samples taken at a uniform rate*

$$\boxed{f_s \ge 2f_m}$$

*i.e. the sampling interval $T_s \le \dfrac{1}{2f_m}$. The minimum rate $2f_m$ is called the **Nyquist rate**; $f_s/2$ is the Nyquist (folding) frequency.*

**Explanation.** Sampling is the multiplication of $x(t)$ by a train of impulses of period $T_s$. In the frequency domain this **repeats the spectrum $X(f)$ around every multiple of $f_s$**:

$$X_s(f) = \frac{1}{T_s}\sum_{k=-\infty}^{\infty}X(f - kf_s)$$

- If $f_s \ge 2f_m$ the copies **do not overlap**; the original spectrum can be recovered by an **ideal low-pass filter** of cut-off between $f_m$ and $f_s - f_m$ (reconstruction filter), which gives back $x(t)$ exactly (the interpolation $x(t) = \sum x(nT_s)\,\text{sinc}\left[(t - nT_s)/T_s\right]$).
- If $f_s < 2f_m$ the neighbouring spectra **overlap (aliasing)**: the higher frequencies appear as lower ones (a frequency $f$ appears as $|f - kf_s|$) and cannot be separated, so the signal is distorted and cannot be recovered.

**Practical points:** an **anti-aliasing low-pass filter** (cut-off $f_s/2$) is placed before the sampler, and the sampling rate is chosen as 2.5 to 10 times $f_m$ (a real filter has a finite roll-off). *Examples:* telephone speech (3.4 kHz) is sampled at 8 kHz; CD audio (20 kHz) at 44.1 kHz; a 50 Hz signal with up to the 25th harmonic ($f_m = 1250$ Hz) needs at least $2.5$ kHz.

```figure caption="Question 11: spectrum of a band-limited signal and of its samples: no overlap for f_s > 2 f_m (top), aliasing for f_s < 2 f_m (bottom)."
fig,axs=plt.subplots(2,1,figsize=(6.2,3.4),sharex=False)
f=np.linspace(-4,4,800)
tri=lambda x,c,w:np.clip(1-abs(x-c)/w,0,None)
for ax,(fs,t) in zip(axs,((3.0,'$f_s = 3 f_m$: copies separate (recoverable)'),(1.4,'$f_s = 1.4 f_m$: copies overlap (aliasing)'))):
    s=sum(tri(f,k*fs,1.0) for k in range(-3,4)); ax.plot(f,tri(f,0,1.0),color=INK,lw=1.2,ls='--'); ax.plot(f,s,color=ACCENT,lw=1.6)
    ax.set_title(t,fontsize=8); ax.set_yticks([]); ax.set_xlim(-4,4); ax.set_xticks([-fs,0,fs]); ax.set_xticklabels(['$-f_s$','0','$f_s$'])
```

@s 12
**Dynamometer (electrodynamometer) wattmeter.**

**Construction.** Two **fixed coils** (current coil, CC, few turns of thick wire, in **series** with the load, carrying the load current $i_1 = i$) produce a nearly uniform field. The **moving coil** (pressure or potential coil, PC, many turns of fine wire in series with a high non-inductive resistance $R_p$, connected **across** the load) is mounted on a spindle inside it, with the pointer, spiral springs (the controlling torque $T_c = K\theta$, which also lead the current) and air-friction damping. There is no iron, so no hysteresis error.

**Principle.** The torque comes from the interaction of the moving-coil current $i_2 = v/R_p$ with the field of the fixed coils (proportional to $i_1$). The instantaneous deflecting torque is

$$T_i = i_1i_2\frac{dM}{d\theta}$$

where $M$ is the mutual inductance between the coils and $\theta$ the deflection.

**D.C. circuit.** $i_1 = I$ (load current) and $i_2 = V/R_p$ (with $V$ the load voltage):

$$T_d = \frac{VI}{R_p}\frac{dM}{d\theta}\ \propto\ VI = P$$

At balance $T_d = T_c = K\theta$, so $\theta = \dfrac{1}{KR_p}\dfrac{dM}{d\theta}\,P$: **the deflection is proportional to the power.**

**A.C. circuit.** Let $v = V_m\sin\omega t$ and $i = I_m\sin(\omega t - \varphi)$. The pressure-coil current is practically in phase with $v$ (as $R_p$ is much larger than its reactance): $i_2 = (V_m/R_p)\sin\omega t$.

$$T_i = \frac{V_mI_m}{R_p}\sin\omega t\sin(\omega t - \varphi)\frac{dM}{d\theta} = \frac{V_mI_m}{2R_p}\left[\cos\varphi - \cos(2\omega t - \varphi)\right]\frac{dM}{d\theta}$$

The moving system cannot follow the $2\omega$ term, so the pointer takes the **average torque**:

$$T_{avg} = \frac{V_mI_m}{2R_p}\cos\varphi\,\frac{dM}{d\theta} = \frac{VI\cos\varphi}{R_p}\,\frac{dM}{d\theta}$$

where $V$ and $I$ are the r.m.s. values. Equating with $K\theta$:

$$\boxed{\theta = \frac{1}{KR_p}\frac{dM}{d\theta}\,VI\cos\varphi\ \propto\ P}$$

(if $dM/d\theta$ is constant over the working range). **Hence the deflecting torque, and the deflection, are directly proportional to the true (active) power $P = VI\cos\varphi$ in both a.c. and d.c. circuits;** the scale is uniform, calibrated directly in watts. *Errors:* the inductance of the pressure coil (the correction factor $\dfrac{\cos\varphi\cos\beta}{\cos(\varphi - \beta)}$, important at low power factor), the capacitance between the coils, the eddy currents and the stray fields (astatic construction, shielding), the power loss in the instrument itself (the connection of the pressure coil before or after the current coil).
