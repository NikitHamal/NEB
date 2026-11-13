---
subject: Internet of Things
grade: BCA Semester 8 (Elective IV)
unit: 2
title: Sensors, Actuators and Interfacing
hours: 18
area: BCA 454 · Internet of Things · Unit 2
---

Every IoT system is built on two kinds of parts that touch the physical world: **sensors** that turn a physical quantity (heat, light, motion) into an electrical signal, and **actuators** that turn an electrical signal into a physical action (a lamp, a motor, a valve). Between them sits a board that reads, decides and writes. This is the longest unit of the course (18 hours, with the laboratory) because every later topic depends on knowing what a sensor really delivers and how to read it correctly.

::: key What this unit gives you
- The role of sensors and actuators and four ways of classifying sensors, with the quantities that describe a sensor's quality.
- How the sensors of the outline work: position, occupancy and motion, velocity and acceleration, force, pressure, flow, acoustic, humidity, light, radiation, temperature, chemical, biosensor and camera.
- The common actuators and how to drive them, including PWM.
- Arduino and Raspberry Pi: installation, interfacing and Python programming, with worked numerical examples and a laboratory list.
:::

## 2.1 Roles of sensors and actuators

A **sensor** detects a physical quantity (the **measurand**) and produces an output, usually an electrical voltage, current, resistance or digital value, that a processor can read. An **actuator** accepts a command signal and produces motion, heat, light or sound. Together they close the **sense, decide, act** loop:

1. the sensor measures (soil moisture is 18 percent);
2. the controller compares it with a rule (below 25 percent means dry);
3. the actuator acts (open the valve);
4. the sensor measures again (the loop is a feedback loop).

A **transducer** is any device that converts one form of energy into another; sensors and actuators are both transducers, in opposite directions. Between the real world and the processor stand the **signal chain** parts: the sensing element, **signal conditioning** (amplify, filter, convert resistance to voltage), the **analog-to-digital converter (ADC)** and finally the digital value in code.

```svgfig label="2.1" caption="The sense, decide, act loop. The sensor chain converts a physical quantity into a number, the controller applies a rule, and the actuator changes the physical world that the sensor then measures again."
f = Fig(640, 200)
f.box(10, 70, 100, 56, "Physical\nworld", fill=SOFT, stroke=SLATE, size=11)
f.box(150, 20, 110, 46, "Sensing element\n(transducer)", fill=BLUE, stroke=NAVY, size=10)
f.box(290, 20, 100, 46, "Signal\nconditioning", fill=BLUE, stroke=NAVY, size=10)
f.box(420, 20, 80, 46, "ADC", fill=BLUE, stroke=NAVY, size=11)
f.box(520, 70, 110, 56, "Controller\n(board + code)", fill=SAND, stroke=AMBER, size=10.5)
f.box(290, 140, 110, 46, "Driver\n(relay, MOSFET)", fill=MINT, stroke=TEAL, size=10)
f.box(150, 140, 110, 46, "Actuator", fill=MINT, stroke=TEAL, size=11)
f.arrow([(110, 90), (150, 50)], color=NAVY)
f.arrow([(260, 43), (290, 43)], color=NAVY)
f.arrow([(390, 43), (420, 43)], color=NAVY)
f.arrow([(500, 43), (575, 70)], color=NAVY)
f.arrow([(575, 126), (400, 160)], color=TEAL)
f.arrow([(290, 163), (260, 163)], color=TEAL)
f.arrow([(150, 163), (60, 126)], color=TEAL, label="acts on")
```

## 2.2 Types of sensors

The outline lists four pairs of classes. A given sensor falls into one class of each pair.

| Classification | Meaning | Examples |
|---|---|---|
| **Active** | Needs an **external power supply** to produce an output signal; it modulates that supply. | Thermistor (needs a current to read its resistance), strain gauge, LDR, ultrasonic ranger |
| **Passive** | **Generates its own** signal from the measured energy, with no external excitation. | Thermocouple, photovoltaic cell, piezoelectric microphone, PIR (senses incoming infrared) |
| **Analog** | Output varies **continuously** with the measurand (a voltage or resistance). Needs an ADC. | LM35 temperature sensor, LDR, potentiometer |
| **Digital** | Output is **discrete**: a logic level, a pulse train or a bus message. | DHT22, DS18B20, BMP280 (I2C), PIR (high or low) |
| **Contact** | Must **touch** the object or medium it measures. | Thermocouple on a pipe, strain gauge on a beam, pH probe |
| **No-contact** | Measures **remotely**, with no touching. | Infrared thermometer, ultrasonic ranger, camera, PIR |
| **Absolute** | Output refers to a **fixed zero**; its reading always means the same thing, even after power-off. | Absolute rotary encoder (a unique code per angle), potentiometer position sensor |
| **Relative** | Output is a **change from a starting point**; you must count or zero it. | Incremental rotary encoder, accelerometer-integrated velocity |

::: caution The classes are about behaviour, not the part number
The same physical quantity can be measured by sensors of different classes. The LM35 is analog and active; the DS18B20 is digital and active; a thermocouple is analog and passive. Say which class **and why** (for instance "active because the thermistor needs a bias current").
:::

## 2.3 Sensor characteristics and the ADC

Sensors are compared by **specifications**. The ones that examiners and engineers use:

| Quantity | Meaning |
|---|---|
| **Range** | Smallest to largest value the sensor can measure (LM35: -55 to 150 degrees C in the full-range circuit). |
| **Sensitivity** | Change of output per unit change of input (LM35: 10 mV per degree C). |
| **Resolution** | Smallest change that can be detected (DS18B20 at 12 bits: 0.0625 degrees C). |
| **Accuracy** | How close the reading is to the true value (DHT22: about 0.5 degrees C). |
| **Precision (repeatability)** | How close repeated readings are to each other. A sensor can be precise but not accurate (a constant offset). |
| **Linearity** | How well the output follows a straight line with the input. |
| **Response time** | Time to reach, usually, 63 percent (one time constant) or 90 percent of a step change. |
| **Hysteresis** | Different output for the same input depending on whether the input is rising or falling. |
| **Drift** | Slow change of output with time or temperature, needing recalibration. |

**Reading an analog sensor.** An ADC with $n$ bits divides the reference voltage $V_{ref}$ into $2^n$ steps. The smallest voltage step (the **LSB**) is $V_{ref}/2^n$, and a count $N$ corresponds to $V = N\cdot V_{ref}/2^n$. The Arduino Uno has a 10-bit ADC with $V_{ref}=5$ V, so the step is $5/1024=4.88$ mV and $N$ runs from 0 to 1023.

::: example Reading an LM35 on an Arduino
The LM35 gives 10 mV per degree C. The ADC returns $N=75$. Voltage $=75\times5/1024=0.366$ V, so temperature $=0.366/0.010=36.6$ degrees C. One ADC step is $4.88\text{ mV}/10\text{ mV per }^\circ\text{C}=0.49\,^\circ\text{C}$, so the **resolution of the whole chain is about half a degree**, much coarser than the sensor itself. Using a lower reference voltage (1.1 V internal reference, step 1.07 mV, resolution 0.107 degrees C) improves it, which is why the Uno's `analogReference(INTERNAL)` is common with LM35.
:::

```python
def adc_to_volts(count, bits=10, vref=5.0):
    return count * vref / (2 ** bits)

step_5v = 5.0 / 2 ** 10
step_11 = 1.1 / 2 ** 10
print("LSB at 5 V reference   : %.2f mV -> %.3f degC per step" % (step_5v * 1000, step_5v / 0.010))
print("LSB at 1.1 V reference : %.2f mV -> %.3f degC per step" % (step_11 * 1000, step_11 / 0.010))
for n in (75, 76, 300):
    v = adc_to_volts(n)
    print("count %4d -> %.3f V -> %.1f degC" % (n, v, v / 0.010))
# a 12-bit ADC at 3.3 V (as on many 3.3 V boards)
print("12-bit, 3.3 V: LSB = %.3f mV" % (3.3 / 2 ** 12 * 1000))
```
```output
LSB at 5 V reference   : 4.88 mV -> 0.488 degC per step
LSB at 1.1 V reference : 1.07 mV -> 0.107 degC per step
count   75 -> 0.366 V -> 36.6 degC
count   76 -> 0.371 V -> 37.1 degC
count  300 -> 1.465 V -> 146.5 degC
12-bit, 3.3 V: LSB = 0.806 mV
```
**Voltage divider.** Many analog sensors are resistive (LDR, thermistor), so their resistance is turned into a voltage by a divider with a fixed resistor $R_1$ from the supply to the ADC pin and the sensor $R_s$ from the pin to ground:
$$V_{out}=V_{cc}\cdot\frac{R_s}{R_1+R_s}.$$
The reading is most sensitive when $R_1$ is close to the sensor's resistance in the middle of its range, which is the rule for choosing $R_1$.

**Digital inputs.** A digital input needs a defined level when nothing drives it. A **pull-up** (or pull-down) resistor, about 10 kilohms, ties the pin to the supply (or ground) so that a switch pulls it the other way. Mechanical switches **bounce**: for a few milliseconds the contact opens and closes repeatedly, so software ignores changes that last less than about 20 ms (**debouncing**).

## 2.4 Working of sensors: position, occupancy, motion, velocity, force, pressure and flow

**Position.** Position can be linear or angular.

- **Potentiometer.** A resistive track with a sliding contact; the wiper voltage is proportional to position. Cheap, analog, absolute, but it wears.
- **Rotary encoder.** A disc with slots or a code pattern interrupts a light beam (optical) or changes a magnetic field (magnetic). An **incremental** encoder gives pulses (two channels A and B, 90 degrees out of phase, so the order of edges shows the direction) and the controller counts them. An **absolute** encoder gives a unique binary code (often Gray code) for each angle.
- **Hall-effect sensor.** A current-carrying semiconductor produces a transverse voltage in a magnetic field. A magnet on the moving part makes the sensor switch or vary; used for door contacts, wheel counters and brushless motors.
- **Limit switch** and **reed switch** give a simple digital "at position" signal.

**Occupancy and motion.**

- **PIR (passive infrared) sensor**, for example the HC-SR501. A pyroelectric element senses changes in infrared radiation. A warm body moving across the sensor's two segments produces a differential signal; the digital output goes high, typically for a few seconds, adjustable by a potentiometer. It detects **movement of warm bodies**, not a person standing still, which is why a room light may switch off on a still reader.
- **Ultrasonic ranger**, for example the HC-SR04. It sends a 40 kHz burst and measures the echo time. The distance is $d=v_s t/2$ where $v_s\approx343$ m/s at 20 degrees C; in the usual form $d(\text{cm})=t(\mu s)/58$. Range about 2 cm to 4 m. It also detects occupancy (a car in a parking bay).
- **Microwave (radar) sensor**, for example RCWL-0516, detects motion through thin walls using the Doppler shift; **magnetic contacts** report doors; **cameras** with people counting report occupancy.

::: example Ultrasonic ranging
The echo pin of an HC-SR04 stays high for 1,166 microseconds. Distance $=343\ \text{m/s}\times1166\times10^{-6}\ \text{s}/2=0.20$ m, that is 20 cm. Check with the rule of thumb: $1166/58=20.1$ cm. At 35 degrees C the speed of sound is about 352 m/s, so ignoring temperature gives a 2.6 percent error (0.5 cm at 20 cm); a good design reads the temperature too and corrects $v_s\approx331.3+0.606\,T$ m/s.
:::

**Velocity and acceleration.**

- **Tachometer** and **encoder-based speed**: count pulses in a fixed time. A wheel with 20 slots giving 50 pulses in 0.5 s turns at $50/20=2.5$ rev in 0.5 s, that is 5 rev/s or 300 rpm. A Hall sensor counting a magnet on a bicycle wheel gives speed as $v=2\pi r\cdot f$.
- **Accelerometer (MEMS).** A tiny proof mass on springs inside the chip moves under acceleration; the change of capacitance between fixed and moving plates is measured. Three axes give tilt (from gravity, 1 g) and shock. Example: MPU-6050 (3-axis accelerometer plus 3-axis gyroscope, I2C address 0x68). Velocity from acceleration is an integral, so errors accumulate (drift); this is why dead reckoning needs correction from GPS.
- **Gyroscope** measures angular velocity; fused with the accelerometer (a complementary or Kalman filter) it gives orientation.
- **GPS** gives position and, from successive fixes or Doppler, velocity.

**Force and load.**

- **Strain gauge.** A thin metallic foil whose resistance changes by a small fraction when stretched, $\Delta R/R=GF\cdot\varepsilon$ where the gauge factor $GF\approx2$. Because the change is tiny (for 1000 microstrain, 0.2 percent), strain gauges sit in a **Wheatstone bridge** and the output is amplified (an HX711 24-bit amplifier is the common module).
- **Load cell.** A metal block with strain gauges, calibrated to give a signal proportional to weight; used in smart scales, silo level and bin-weight measurements.
- **Force-sensitive resistor (FSR).** Resistance falls as pressing force increases; for touch and presence, not for accurate weight.

**Pressure.**

- **Piezoresistive MEMS** (most common) measures the deformation of a silicon diaphragm. The BMP280 gives pressure from about 300 to 1100 hPa (and altitude from it) over I2C or SPI; sea-level pressure is 1013 hPa and falls about 12 hPa per 100 m near sea level.
- **Capacitive** and **piezoelectric** types are used for tyres, hydraulics and dynamic pressure.

::: example Altitude from pressure
A BMP280 reads 840 hPa where the sea-level reference is 1013.25 hPa. With the barometric formula $h=44330\left[1-(P/P_0)^{1/5.255}\right]$ metres, $h=44330\,[1-(0.829)^{0.1903}]\approx1{,}550$ m. For comparison, Kathmandu at about 1,400 m reads roughly 855 hPa. Weather changes the reading by about 10 to 30 hPa, which is 100 to 300 m of error, so absolute altitude from pressure needs a fresh reference.
:::

**Flow.**

- **Turbine (paddle-wheel) flow sensor**, for example YF-S201: water spins a rotor with a magnet; a Hall sensor outputs pulses whose **frequency is proportional to flow**. For the YF-S201 the commonly quoted relation is $f=7.5\,Q$ with $f$ in Hz and $Q$ in L/min.
- **Ultrasonic flow meters** (transit-time) measure the difference in travel time of sound along and against the flow, with no moving parts and no contact with the liquid.
- **Electromagnetic flow meters** measure the voltage induced by a conducting liquid moving through a magnetic field. **Differential-pressure** meters (orifice plate) measure the pressure drop.

```python
# Pulse-based sensors: speed from a wheel encoder, flow from a YF-S201 type sensor, ultrasonic distance
slots, pulses, window = 20, 50, 0.5
rev_per_s = pulses / slots / window
print("wheel: %.1f rev/s = %.0f rpm" % (rev_per_s, rev_per_s * 60))

radius = 0.33                     # bicycle wheel radius in metres
pulses_per_rev, f = 1, 3.0        # one magnet, 3 pulses per second
speed = 2 * 3.14159 * radius * f / pulses_per_rev
print("bicycle: %.1f m/s = %.1f km/h" % (speed, speed * 3.6))

freq = 45.0                       # Hz from the flow sensor
Q = freq / 7.5                    # L/min, f = 7.5 Q
print("flow: %.1f L/min, %.2f L in 10 s" % (Q, Q * 10 / 60))

t_us = 1166                       # echo width in microseconds
print("distance: %.1f cm (t/58) and %.1f cm (343 m/s)" % (t_us / 58, 343 * t_us * 1e-6 / 2 * 100))
for T in (20, 35):
    print("speed of sound at %d degC: %.1f m/s" % (T, 331.3 + 0.606 * T))
```
```output
wheel: 5.0 rev/s = 300 rpm
bicycle: 6.2 m/s = 22.4 km/h
flow: 6.0 L/min, 1.00 L in 10 s
distance: 20.1 cm (t/58) and 20.0 cm (343 m/s)
speed of sound at 20 degC: 343.4 m/s
speed of sound at 35 degC: 352.5 m/s
```
```svgfig label="2.2" caption="Echo-time ranging with an ultrasonic sensor. A 10-microsecond trigger starts a burst of eight 40 kHz pulses; the echo pin stays high for the round-trip time t, and the distance is half of speed times t."
f = Fig(640, 220)
f.box(20, 80, 90, 60, "HC-SR04\nsensor", fill=BLUE, stroke=NAVY, size=11)
f.box(540, 60, 80, 100, "Object", fill=SAND, stroke=AMBER, size=11)
f.arrow([(110, 100), (540, 100)], color=NAVY, label="burst out", lpos=(325, 90))
f.arrow([(540, 125), (110, 125)], color=TEAL, label="echo back", lpos=(325, 142))
f.text(325, 185, "distance d = (speed x t) / 2    (speed 343 m/s at 20 degC)", size=11, color=NAVY, bold=True)
f.text(325, 28, "TRIG: 10 us pulse   ->   ECHO high for t", size=10.5, color=SLATE)
```

## 2.5 Working of sensors: acoustic, humidity, light, radiation and temperature

**Acoustic (sound).**

- **Electret condenser microphone.** A charged diaphragm and a back plate form a capacitor; sound pressure changes the capacitance and so a tiny voltage, which a built-in FET buffers. A module (for example the KY-038 or MAX4466) adds an amplifier and gives an analog level plus a digital threshold output.
- **MEMS microphone** (in phones) integrates the same idea on silicon with a digital I2S or PDM output.
- **Piezoelectric** sensors give a voltage when flexed; used as knock and vibration sensors and as ultrasonic transducers (the HC-SR04 contains two).
- Sound level is measured in decibels, $L=20\log_{10}(p/p_0)$ with $p_0=20\ \mu$Pa. Each doubling of pressure is 6 dB. A sound-level IoT node samples the microphone for a short window, takes the **RMS** value and reports it (noise monitoring in cities).

**Humidity.** Relative humidity (RH) is the water vapour present as a percentage of the maximum the air can hold at that temperature. A **capacitive humidity sensor** has a polymer film between electrodes whose dielectric constant rises as it absorbs water, so capacitance rises with RH. The **DHT11** (RH 20 to 80 percent, accuracy about 5 percent, 1 reading per second) and **DHT22** (RH 0 to 100 percent, about 2 to 5 percent, temperature -40 to 80 degrees C with 0.5 degree accuracy, one reading every 2 seconds) include an ADC and send a 40-bit packet (16 bits humidity, 16 bits temperature, 8-bit checksum) on a single data wire. Never poll them faster than the data sheet allows. **Soil moisture** probes measure resistance (cheap, corrode) or capacitance (better) between two electrodes.

**Light.**

- **LDR (light-dependent resistor, photoresistor).** Cadmium-sulphide film whose resistance falls from megohms in the dark to a few kilohms in bright light. Analog, slow (tens of milliseconds), not calibrated: good for "is it dark".
- **Photodiode and phototransistor.** A reverse-biased junction passes a current proportional to light; fast (used in remote-control receivers and optical encoders).
- **Digital light sensors** (BH1750, TSL2561) output illuminance in **lux** over I2C: office about 300 to 500 lux, overcast day about 1,000, direct sun about 100,000.
- **Colour (TCS3200) and UV sensors** exist for sorting and sun-exposure alarms. A **photovoltaic cell** is a passive light sensor, and also the source in solar IoT nodes.

**Radiation.** "Radiation" in sensors means two things. **Ionising radiation** (alpha, beta, gamma) is detected by a **Geiger-Mueller tube**: a gas-filled tube in which one ionising particle triggers a discharge pulse; the board counts **counts per minute (CPM)** and converts to dose rate (for a typical tube, about 150 to 175 CPM per microsievert per hour; the factor is printed for each tube). Natural background in many places is around 0.1 microsievert per hour. **Infrared and UV** are detected by photodiodes, thermopiles (non-contact infrared thermometers such as the MLX90614) and pyroelectric sensors (PIR).

**Temperature.** This is the most-used IoT sensor. Four families:

| Sensor | Principle | Output | Range and accuracy (typical) |
|---|---|---|---|
| **Thermistor (NTC)** | Resistance of a ceramic semiconductor **falls** as temperature rises, strongly non-linear | Resistance (analog, via divider) | -50 to 150 degrees C; about 1 degree C after calibration |
| **RTD (Pt100, Pt1000)** | Resistance of platinum rises almost linearly: $R=R_0(1+\alpha T)$, $\alpha=0.00385\ /^\circ$C | Resistance | -200 to 850 degrees C; very accurate and stable |
| **Thermocouple** | Two different metals joined produce a small voltage (Seebeck effect), about 41 microvolts per degree C for type K | Millivolts, needs amplifier (MAX6675 or MAX31855) | -200 to 1,300 degrees C and more; passive; used for flames and furnaces |
| **Integrated sensors** | LM35 (analog, 10 mV per degree C), TMP36 (500 mV offset, 10 mV per degree C), DS18B20 (digital 1-Wire, 9 to 12 bits, -55 to 125 degrees C, 0.5 degree accuracy, 750 ms conversion at 12 bits, a 64-bit unique ID so many sit on one wire) | Voltage or digital | Easiest for IoT |

The **beta equation** converts an NTC resistance to temperature: $\dfrac1T=\dfrac1{T_0}+\dfrac1B\ln\dfrac R{R_0}$, with $T$ in kelvin, $R_0$ the resistance at $T_0=298.15$ K (25 degrees C) and $B$ (about 3950 K for the common 10-kilohm module).

::: example NTC thermistor reading
A 10 kilohm NTC ($B=3950$) is the lower leg of a divider with a fixed 10 kilohm resistor, powered at 5 V and read by a 10-bit ADC. The ADC reads 512 (half of full scale). Then $R_s=R_1\cdot N/(1023-N)=10\ \text{k}\Omega\times512/511\approx10.02$ k$\Omega$, so $T\approx25$ degrees C. If the count rises to 683, $R_s=10\times683/340=20.09$ k$\Omega$, and $1/T=0.003354+\ln(2.009)/3950=0.003354+0.000177=0.003531$, so $T=283.2$ K $=10.1$ degrees C: as the thermistor is the **lower** leg of the divider here, more resistance means a colder thermistor.
:::

```python
import math
def ntc_celsius(count, r_fixed=10_000.0, r0=10_000.0, beta=3950.0, bits=10):
    top = 2 ** bits - 1
    r = r_fixed * count / (top - count)          # thermistor is the lower leg of the divider
    inv_t = 1 / 298.15 + math.log(r / r0) / beta
    return r, 1 / inv_t - 273.15

for n in (512, 683, 300):
    r, t = ntc_celsius(n)
    print("count %3d  R = %7.0f ohm  T = %5.1f degC" % (n, r, t))

# RTD Pt100: R = 100 (1 + 0.00385 T)   ->   T from a measured resistance
for r in (100.0, 119.4, 138.5):
    print("Pt100 %.1f ohm -> %.1f degC" % (r, (r / 100 - 1) / 0.00385))

# LDR divider: 10 kohm fixed on top, LDR below, 5 V supply
for name, r_ldr in (("dark", 1_000_000), ("room", 10_000), ("sun", 500)):
    v = 5 * r_ldr / (10_000 + r_ldr)
    print("%-5s LDR %8d ohm -> %.2f V -> ADC %d" % (name, r_ldr, v, round(v / 5 * 1023)))
# sound level: pressure doubling
print("pressure x2 = +%.1f dB; pressure x10 = +%.0f dB" % (20 * math.log10(2), 20))
```
```output
count 512  R =   10020 ohm  T =  25.0 degC
count 683  R =   20088 ohm  T =  10.1 degC
count 300  R =    4149 ohm  T =  46.2 degC
Pt100 100.0 ohm -> 0.0 degC
Pt100 119.4 ohm -> 50.4 degC
Pt100 138.5 ohm -> 100.0 degC
dark  LDR  1000000 ohm -> 4.95 V -> ADC 1013
room  LDR    10000 ohm -> 2.50 V -> ADC 512
sun   LDR      500 ohm -> 0.24 V -> ADC 49
pressure x2 = +6.0 dB; pressure x10 = +20 dB
```
```svgfig label="2.3" caption="Voltage-divider reading of a resistive sensor (an NTC thermistor or LDR). The ADC pin sits between the fixed resistor and the sensor; as the sensor resistance changes, the voltage on the pin changes."
f = Fig(640, 230)
f.line(120, 30, 520, 30, color=SLATE, sw=1.4)
f.text(80, 30, "+5 V", size=11, color=RED, bold=True)
f.box(280, 40, 40, 60, "", fill=SAND, stroke=AMBER)
f.text(340, 70, "R1 = 10 k", size=11, color=AMBER, bold=True, anchor="start")
f.line(300, 30, 300, 40, color=SLATE)
f.line(300, 100, 300, 130, color=SLATE)
f.circle(300, 130, 4, fill=NAVY, stroke=NAVY)
f.line(300, 130, 420, 130, color=NAVY, sw=1.6)
f.box(420, 105, 100, 50, "ADC pin A0\n(10 bit)", fill=BLUE, stroke=NAVY, size=10.5)
f.box(280, 140, 40, 60, "", fill=MINT, stroke=TEAL)
f.text(340, 170, "Rs: NTC or LDR", size=11, color=TEAL, bold=True, anchor="start")
f.line(300, 130, 300, 140, color=SLATE)
f.line(300, 200, 300, 218, color=SLATE)
f.line(280, 218, 320, 218, color=SLATE, sw=2)
f.text(80, 218, "GND", size=11, color=SLATE, bold=True)
f.text(110, 130, "Vout = 5 x Rs / (R1 + Rs)", size=10.5, color=NAVY, bold=True, anchor="start")
```

## 2.6 Working of sensors: chemical, biosensor and camera

**Chemical sensors.** They respond to the presence or concentration of a substance.

- **Metal-oxide semiconductor gas sensors (MQ series).** A heated tin-dioxide layer changes resistance when gas molecules react on its surface. The MQ-2 responds to LPG, smoke and propane, the MQ-3 to alcohol, the MQ-7 to carbon monoxide, the MQ-135 to air-quality gases. Each needs a **warm-up** of minutes to days for stable readings, a heater drawing about 150 mA at 5 V, and **calibration**: the ratio $R_s/R_0$ (resistance in gas over resistance in clean air) is mapped to ppm on a log-log curve from the data sheet. They are **cross-sensitive** (several gases look alike) so they suit alarms, not measurement.
- **Electrochemical sensors** (CO, O2, toxic gases) give a current proportional to concentration; more accurate, with a life of a few years.
- **NDIR sensors** (MH-Z19 for CO2) measure the infrared absorbed by CO2 in a small chamber; the right choice for indoor CO2 (outdoor air is about 420 ppm; above 1,000 ppm indoors signals poor ventilation).
- **pH and conductivity (TDS) probes** for water: a glass electrode produces a voltage of about 59 mV per pH unit at 25 degrees C, needing a high-impedance amplifier and calibration with buffer solutions of pH 4, 7 and 10.

**Biosensors.** A biosensor combines a **biological recognition element** (enzyme, antibody, DNA, cell) with a **transducer** (electrochemical, optical, piezoelectric) that turns the recognition into a signal.

- **Glucose meter.** The enzyme glucose oxidase on a test strip reacts with blood glucose and produces a current proportional to concentration; the meter converts it to mg/dL. Continuous glucose monitors do the same in tissue fluid and report over BLE.
- **Pulse oximeter (MAX30100, MAX30102).** Red (about 660 nm) and infrared (about 880 to 940 nm) LEDs shine through a fingertip; a photodiode measures the light that passes. The pulsing component (blood volume change at each beat) gives **heart rate**, and the ratio of the red and infrared pulsations gives **SpO2**, the oxygen saturation (normal 95 to 100 percent). This method is **photoplethysmography (PPG)** and is what smartwatches use.
- **ECG electrodes (AD8232)** measure the heart's electrical signal; **GSR** and **body-temperature** sensors serve wearables and stress monitors.
- Others: DNA and antibody biosensors for pathogens, enzyme sensors in food quality.

**Camera.** An image sensor (CMOS) is an array of photodiodes with a colour filter; a lens focuses the scene and the sensor outputs a grid of pixels. In IoT, cameras are **no-contact, digital** sensors and are the heaviest in data: a 640 by 480 colour image is $640\times480\times3=921{,}600$ bytes raw, and a few kilobytes to tens of kilobytes after JPEG compression. Interfaces: **CSI** ribbon for the Raspberry Pi Camera Module, **USB** webcams, and the **ESP32-CAM** module (OV2640, 2 MP) with Wi-Fi. Uses: security and doorbells, **people and vehicle counting**, plant-health imaging, reading meters, quality inspection on conveyors. Because a camera can identify people, it brings the greatest **privacy** obligations (process on the device when possible and send only the result, such as "3 people").

::: note Choosing a sensor in practice
Ask in order: what must be measured and over what range; what accuracy and response time are needed; contact or no-contact; analog or digital interface (the board's available pins and voltage level); power draw (battery nodes need microamps in sleep); cost and availability; and how it will be calibrated and protected from dust, water and sun.
:::

## 2.7 Actuators and how to drive them

An actuator needs more power than a microcontroller pin can supply (an Arduino pin gives at most 20 mA recommended, 40 mA absolute; a Raspberry Pi pin only a few mA). A **driver** stage sits between them.

| Actuator | What it does | How to drive it |
|---|---|---|
| **LED** | Light, status | Series resistor: $R=(V_{supply}-V_f)/I$ |
| **Buzzer** | Sound | Active type: on/off; passive type: a square wave (`tone()`) |
| **Relay** | Switches a high-power or mains load with an electrically isolated coil | Transistor driver plus **flyback diode**; relay modules include these |
| **DC motor** | Rotation | **MOSFET or H-bridge** (L298N, L293D, TB6612); speed by PWM, direction by the bridge |
| **Servo motor** | Rotates to a commanded angle (0 to 180 degrees) | A pulse of 1 to 2 ms every 20 ms (1.5 ms is the centre) |
| **Stepper motor** | Rotates in fixed steps (for example 200 steps per turn, 1.8 degrees each) | Driver (ULN2003, A4988) with step and direction pulses |
| **Solenoid valve or lock** | Opens or locks by magnetic pull | MOSFET or relay with a flyback diode |
| **Pump** | Moves liquid | Relay or MOSFET with PWM |

**PWM (pulse-width modulation).** A digital pin cannot output an intermediate voltage, so it switches fast between 0 and $V$; the fraction of time it is high is the **duty cycle** $D$ and the **average voltage** is $D\cdot V$. A motor or an LED (the eye) responds to the average. On the Arduino Uno, `analogWrite(pin, value)` takes $0$ to $255$, so $D=\text{value}/255$; the PWM frequency is about 490 Hz (980 Hz on pins 5 and 6).

::: example LED resistor and PWM
A red LED has $V_f=2.0$ V and should carry 10 mA from a 5 V pin: $R=(5-2.0)/0.010=300\ \Omega$; use the next standard value, 330 ohms, giving $I=3.0/330=9.1$ mA. To run a 6 V motor from a 12 V supply at half speed, set $D=0.5$ (`analogWrite` value 128, giving 128/255 = 50.2 percent). For a servo, an angle $\theta$ corresponds to a pulse width of about $1\text{ ms}+\theta/180\times1\text{ ms}$, so 90 degrees is 1.5 ms and 45 degrees is 1.25 ms.
:::

```python
def led_resistor(v_supply, v_forward, current_a):
    return (v_supply - v_forward) / current_a

print("LED resistor: %.0f ohm" % led_resistor(5, 2.0, 0.010))
print("current with 330 ohm: %.1f mA" % (1000 * (5 - 2.0) / 330))
for value in (0, 64, 128, 255):
    d = value / 255
    print("analogWrite(%3d): duty %5.1f %%  average %.2f V from 5 V" % (value, 100 * d, 5 * d))
for angle in (0, 45, 90, 180):
    print("servo %3d deg -> pulse %.2f ms" % (angle, 1 + angle / 180))
steps_per_rev = 200
print("stepper: %d steps for %.1f degrees; one turn = %d steps" % (int(90 / (360 / steps_per_rev)), 90, steps_per_rev))
```
```output
LED resistor: 300 ohm
current with 330 ohm: 9.1 mA
analogWrite(  0): duty   0.0 %  average 0.00 V from 5 V
analogWrite( 64): duty  25.1 %  average 1.25 V from 5 V
analogWrite(128): duty  50.2 %  average 2.51 V from 5 V
analogWrite(255): duty 100.0 %  average 5.00 V from 5 V
servo   0 deg -> pulse 1.00 ms
servo  45 deg -> pulse 1.25 ms
servo  90 deg -> pulse 1.50 ms
servo 180 deg -> pulse 2.00 ms
stepper: 50 steps for 90.0 degrees; one turn = 200 steps
```
## 2.8 Development boards: Arduino

**Arduino** is an open-source family of microcontroller boards with a simple programming environment. The **Arduino Uno R3** is the reference board.

| Feature | Arduino Uno R3 |
|---|---|
| Microcontroller | ATmega328P, 8-bit AVR |
| Clock | 16 MHz |
| Memory | 32 KB flash (program, 0.5 KB used by the bootloader), 2 KB SRAM, 1 KB EEPROM |
| Digital I/O | 14 pins (D0 to D13), 6 of which give PWM (D3, D5, D6, D9, D10, D11) |
| Analog inputs | 6 (A0 to A5) with a 10-bit ADC |
| Logic level and supply | 5 V logic; 7 to 12 V recommended on the barrel jack; 3.3 V and 5 V output pins |
| Buses | UART (D0 RX, D1 TX), I2C (A4 SDA, A5 SCL), SPI (D10 SS, D11 MOSI, D12 MISO, D13 SCK) |
| Wireless | None; add an ESP8266 or ESP32 module, a Bluetooth module or a shield |

For IoT the **ESP32** or **ESP8266** boards (programmable from the Arduino IDE) are usually a better choice than the Uno because they include Wi-Fi (and Bluetooth on the ESP32), run at 3.3 V and have more memory.

**Installation and first program.**

1. Install the **Arduino IDE** (version 2 is current) from arduino.cc.
2. Connect the board by USB; in **Tools > Board** pick *Arduino Uno* and in **Tools > Port** the new serial port (COMx on Windows, /dev/ttyACM0 on Linux).
3. Open **File > Examples > 01.Basics > Blink**, press **Upload**. The IDE compiles the sketch with avr-gcc, and the bootloader writes it to flash over the serial link.

A sketch has two required functions: `setup()` runs once, `loop()` runs forever. The main functions are `pinMode`, `digitalWrite`, `digitalRead`, `analogRead`, `analogWrite`, `delay`, `millis` and the `Serial` object.

```cpp
// (Arduino C++; compile in the Arduino IDE)
// Read an LM35 on A0, switch a fan relay on D7 above 30 degC, report over serial
const int SENSOR = A0, RELAY = 7;

void setup() {
  pinMode(RELAY, OUTPUT);
  analogReference(INTERNAL);          // 1.1 V reference: 1.07 mV per step
  Serial.begin(9600);
}

void loop() {
  int count = analogRead(SENSOR);
  float celsius = count * 1.1 / 1024.0 / 0.010;      // 10 mV per degC
  digitalWrite(RELAY, celsius > 30.0 ? HIGH : LOW);
  Serial.print("temp: "); Serial.println(celsius);
  delay(1000);                                       // blocking delay; use millis() for multitasking
}
```

```cpp
// (HC-SR04 on D9 trigger, D10 echo; prints distance in cm)
const int TRIG = 9, ECHO = 10;
void setup() { pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT); Serial.begin(9600); }
void loop() {
  digitalWrite(TRIG, LOW);  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10);  digitalWrite(TRIG, LOW);
  long t = pulseIn(ECHO, HIGH, 30000UL);             // echo width in microseconds (30 ms time-out)
  if (t > 0) { Serial.print(t / 58.0); Serial.println(" cm"); }
  delay(100);
}
```

**Serial buses used to connect sensors.** **UART** is asynchronous, two wires (TX, RX) with an agreed baud rate (GPS modules, Bluetooth modules). **I2C** uses two wires (SDA data, SCL clock) shared by many devices, each with a 7-bit address (BMP280 at 0x76 or 0x77, MPU-6050 at 0x68, BH1750 at 0x23); it needs pull-up resistors, which most modules include. **SPI** uses four wires (MOSI, MISO, SCK and a chip-select per device); faster than I2C (SD cards, displays). **1-Wire** (DS18B20) uses a single data line with a pull-up. Match the bus to the sensor and check the **voltage level**: connecting a 5 V output to a 3.3 V input pin can damage the 3.3 V board, so use a level shifter or a resistor divider.

## 2.9 Development boards: Raspberry Pi

The **Raspberry Pi** is a credit-card-size **single-board computer** (SBC) running a full operating system, Raspberry Pi OS (Debian-based) or Ubuntu. Unlike the Arduino, it is not real-time, it has Linux services, USB, Ethernet, Wi-Fi, HDMI and a camera port, and so it commonly acts as a **gateway** or local server.

| Feature | Arduino Uno | Raspberry Pi 4 Model B |
|---|---|---|
| Type | Microcontroller board | Single-board computer |
| CPU | 8-bit, 16 MHz | 64-bit quad-core Cortex-A72, 1.5 GHz |
| Memory | 2 KB RAM | 1, 2, 4 or 8 GB RAM |
| Storage | 32 KB flash | microSD card (and USB storage) |
| OS | None (one sketch) | Linux |
| Analog input | Yes, 10-bit ADC | **No**: add an ADC chip (MCP3008 on SPI, ADS1115 on I2C) |
| GPIO voltage | 5 V | **3.3 V only** (5 V on an input can destroy the Pi) |
| Power | About 0.2 to 0.5 W | About 3 to 7 W |
| Real-time behaviour | Good, deterministic | Not guaranteed |
| Best for | Simple, low-power sensing and control | Gateways, camera and ML tasks, local web servers |

The Pi 5 (released in October 2023) is faster still; the **Raspberry Pi Pico** (RP2040) is a microcontroller in the Arduino class, programmable in MicroPython.

**Installation.** (1) On a PC, run **Raspberry Pi Imager**, choose the OS, pick the microSD card and, in the advanced settings, set the hostname, user, Wi-Fi and enable SSH. (2) Insert the card and power the Pi. (3) Connect by monitor or `ssh pi@raspberrypi.local`. (4) Update with `sudo apt update && sudo apt full-upgrade`, and enable interfaces (I2C, SPI, camera) in `sudo raspi-config`.

**The 40-pin header.** Pins 1 and 17 give 3.3 V, pins 2 and 4 give 5 V, eight pins are ground; GPIO2 and GPIO3 are I2C (SDA, SCL), GPIO14 and GPIO15 are UART, GPIO10, 9, 11, 8 are SPI (MOSI, MISO, SCLK, CE0), GPIO4 is the default 1-Wire pin, and GPIO12, 13, 18, 19 support hardware PWM. Programs refer to **BCM numbers** (GPIO18) rather than physical pin numbers (pin 12).

**Programming with Python.** Two libraries: **gpiozero** (high-level objects `LED`, `Button`, `DistanceSensor`, `MotionSensor`, `Servo`) and **RPi.GPIO** (low-level). The following program blinks an LED and reads a button; it runs only on a Pi, so it is shown unexecuted.

```python
# noexec
# (runs on a Raspberry Pi with an LED on GPIO17 and a button on GPIO27)
from gpiozero import LED, Button, MotionSensor
from signal import pause

led = LED(17)                      # BCM number 17 = physical pin 11
button = Button(27)                # internal pull-up; pressed = connects to ground
pir = MotionSensor(4)

button.when_pressed = led.toggle
pir.when_motion = lambda: print("motion detected")
pir.when_no_motion = lambda: print("quiet")
pause()                            # wait for events forever
```
```python
# noexec
# (DHT22 on GPIO4 using the Adafruit_DHT-compatible library adafruit-circuitpython-dht)
import time, board, adafruit_dht
dht = adafruit_dht.DHT22(board.D4)
while True:
    try:
        print("temp %.1f C  humidity %.1f %%" % (dht.temperature, dht.humidity))
    except RuntimeError as e:        # DHT sensors often miss a read; just try again
        print("read error:", e.args[0])
    time.sleep(2.0)                  # DHT22 allows one reading per 2 s
```
Because the Pi has no ADC, an analog sensor needs a converter. The MCP3008 is a 10-bit, 8-channel SPI ADC; a reading is converted exactly as in Section 2.3, but with $V_{ref}=3.3$ V, so the step is $3.3/1024=3.22$ mV.

## 2.10 Interfacing in practice: executable models

The laboratory needs hardware, but the **logic** of reading a sensor can be tested on any computer. The programs below simulate the data a board receives and run the same algorithms that go into the sketch or the Python script on the Pi.

**Decoding a DHT22 packet.** The sensor sends 40 bits: 16 for humidity (tenths of a percent), 16 for temperature (tenths of a degree, the top bit is the sign) and 8 for a checksum equal to the low byte of the sum of the other four bytes.

```python
def decode_dht22(b):                      # b = 5 bytes
    if (b[0] + b[1] + b[2] + b[3]) & 0xFF != b[4]:
        raise ValueError("checksum mismatch")
    hum = ((b[0] << 8) | b[1]) / 10.0
    raw = ((b[2] & 0x7F) << 8) | b[3]
    temp = raw / 10.0 * (-1 if b[2] & 0x80 else 1)
    return hum, temp

good = bytes([0x02, 0x8C, 0x01, 0x5F, 0xEE])         # 65.2 % RH, 35.1 degC
print("decoded:", decode_dht22(good))
cold = bytes([0x01, 0xF4, 0x80, 0x65, 0xDA])         # 50.0 % RH, -10.1 degC
print("decoded:", decode_dht22(cold))
bad = bytes([0x02, 0x8C, 0x01, 0x5F, 0xEF])
try:
    decode_dht22(bad)
except ValueError as e:
    print("bad packet ->", e)
```
```output
decoded: (65.2, 35.1)
decoded: (50.0, -10.1)
bad packet -> checksum mismatch
```
**A thermostat with hysteresis, smoothing and debouncing.** A controller that switches a fan on at exactly 30 degrees and off at exactly 30 degrees would chatter when the reading hovers near 30. **Hysteresis** uses two thresholds (on at 30, off at 28). A **moving average** reduces noise, and a **debounce** counter accepts a button change only if it is stable for several samples.

```python
import random
random.seed(8)

def moving_average(values, k=3):
    return [sum(values[max(0, i - k + 1):i + 1]) / len(values[max(0, i - k + 1):i + 1]) for i in range(len(values))]

true_temp = [28, 29.5, 30.6, 31.0, 30.8, 30.4, 30.9, 30.6, 30.3, 29.5, 28.3, 27.2, 26.8]
noisy = [t + random.uniform(-1.5, 1.5) for t in true_temp]
smooth = moving_average(noisy)
fan, log, plain, switches_plain = False, [], False, 0
for raw, s in zip(noisy, smooth):
    new_plain = raw > 30                         # single threshold on the raw reading
    switches_plain += new_plain != plain; plain = new_plain
    if not fan and s > 30: fan = True            # hysteresis: on above 30, off below 28
    elif fan and s < 28: fan = False
    log.append("%.1f->%s" % (s, "ON " if fan else "off"))
print(" ".join(log[:7]))
print(" ".join(log[7:]))
print("raw readings:", " ".join("%.1f" % r for r in noisy))
print("switch changes with one raw threshold:", switches_plain, "  with smoothing + hysteresis:",
      sum(1 for a, b in zip(log, log[1:]) if a[-3:] != b[-3:]))

def debounce(samples, need=3):
    state, count, events = 0, 0, []
    for s in samples:
        count = count + 1 if s != state else 0
        if count >= need:
            state, count = s, 0; events.append(state)
    return events

bounce = [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0]
print("raw edges:", sum(1 for a, b in zip(bounce, bounce[1:]) if a != b), " debounced events:", debounce(bounce))
```
```output
27.2->off 29.0->off 29.2->off 30.7->ON  30.2->ON  30.3->ON  30.5->ON 
30.6->ON  31.0->ON  29.9->ON  29.4->ON  28.2->ON  27.1->off
raw readings: 27.2 30.9 29.5 31.6 29.6 29.6 32.4 29.7 30.7 29.4 28.2 27.2 25.9
switch changes with one raw threshold: 8   with smoothing + hysteresis: 2
raw edges: 8  debounced events: [1, 0]
```
**A mock of the Raspberry Pi GPIO.** The class below mimics the calls of the `RPi.GPIO` library so that a control program can be tested without a Pi (this is how unit tests for IoT code are written).

```python
class FakeGPIO:
    BCM, OUT, IN, HIGH, LOW = "BCM", "OUT", "IN", 1, 0
    def __init__(self): self.pins = {}; self.history = []
    def setmode(self, m): pass
    def setup(self, pin, mode): self.pins[pin] = 0
    def output(self, pin, v): self.pins[pin] = v; self.history.append((pin, v))
    def input(self, pin): return self.pins.get(pin, 0)

GPIO = FakeGPIO()
GPIO.setmode(GPIO.BCM); GPIO.setup(17, GPIO.OUT); GPIO.setup(22, GPIO.OUT)

def irrigate(moisture_percent):                    # LED on 17 = pump, LED on 22 = tank-low alarm
    GPIO.output(17, GPIO.HIGH if moisture_percent < 25 else GPIO.LOW)

for m in (40, 31, 24, 18, 27):
    irrigate(m)
    print("moisture %2d %% -> pump pin 17 = %d" % (m, GPIO.input(17)))
print("pin changes recorded:", GPIO.history)

# MCP3008-style 10-bit reading at 3.3 V
raw = 512
print("MCP3008 count %d -> %.3f V" % (raw, raw * 3.3 / 1024))
```
```output
moisture 40 % -> pump pin 17 = 0
moisture 31 % -> pump pin 17 = 0
moisture 24 % -> pump pin 17 = 1
moisture 18 % -> pump pin 17 = 1
moisture 27 % -> pump pin 17 = 0
pin changes recorded: [(17, 0), (17, 0), (17, 1), (17, 1), (17, 0)]
MCP3008 count 512 -> 1.650 V
```
```svgfig label="2.4" caption="PWM waveforms at 25, 50 and 75 percent duty cycle. The period is the same; only the fraction of time at the high level changes, and so does the average voltage seen by an LED or a motor."
f = Fig(640, 250)
duty = [0.25, 0.5, 0.75]
for k, d in enumerate(duty):
    y0 = 40 + k * 72
    f.text(60, y0 - 4, "%d %%" % int(d * 100), size=11, color=NAVY, bold=True)
    x = 120
    for _ in range(4):
        w = 100 * d
        pts = [(x, y0), (x, y0 - 30), (x + w, y0 - 30), (x + w, y0), (x + 100, y0)]
        for a, b in zip(pts, pts[1:]):
            f.line(a[0], a[1], b[0], b[1], color=NAVY, sw=2.2)
        x += 100
    f.text(560, y0 - 12, "avg %.2f V" % (5 * d), size=10, color=TEAL, bold=True, anchor="start")
f.text(320, 238, "one period = 2 ms (about 490 Hz on an Arduino Uno)", size=10.5, color=SLATE)
```

## 2.11 Laboratory work

The outline asks for the course concepts to be implemented in Python with an Arduino or Raspberry Pi, with every sensor of the unit built either in one project or separately. A workable plan for a college lab of about 15 sessions:

| Lab | Task | Boards and parts | What to submit |
|---|---|---|---|
| 1 | Install the IDE or OS, blink an LED, change the rate | Arduino or Pi, LED, 330 ohm resistor | Circuit sketch, code, photo |
| 2 | Push-button with debouncing, toggle an LED | Button, 10 kilohm pull-down | Code, explanation of bouncing |
| 3 | Temperature: LM35 or thermistor, serial plot, ADC arithmetic | Uno, LM35 or NTC | Calibration table against a reference thermometer |
| 4 | DHT22 temperature and humidity, display on LCD or serial | DHT22, 16 by 2 I2C LCD | Code, 10 minutes of readings |
| 5 | Light: LDR divider and BH1750; automatic lamp | LDR, 10 kilohm, relay | Divider calculation, threshold with hysteresis |
| 6 | Ultrasonic distance and parking alarm | HC-SR04, buzzer | Accuracy test at 10, 20, 50, 100 cm |
| 7 | Motion: PIR alarm; occupancy counter with two sensors | HC-SR501, LED | Timing diagram |
| 8 | Soil moisture, pump relay, irrigation rule | Moisture probe, relay, small pump | Rule and test log |
| 9 | Motors: servo angle with a potentiometer; DC motor PWM | Servo, L298N | PWM table |
| 10 | Accelerometer, gyroscope: tilt angle | MPU-6050 | Angle against a protractor |
| 11 | Pressure and altitude, sound level | BMP280, microphone module | Barometric formula, noise log |
| 12 | Gas, flow, pulse sensors as an alarm or meter | MQ-2 or MQ-135, YF-S201, MAX30102 | Warm-up and calibration notes |
| 13 | Raspberry Pi: GPIO with gpiozero, camera capture | Pi, camera | Scripts and images |
| 14 | Single integrated project: every sensor reports to one Python script and a log file | Board of choice | Block diagram, code, demo |

Document each lab with a **circuit diagram**, the **pin table**, the code, the **observed output** and a short note on errors.

## 2.12 Summary and exercises

Sensors convert physical quantities into signals and actuators convert signals into actions, joined by conditioning, ADC and a controller in a feedback loop. Sensors are classified as active or passive, analog or digital, contact or no-contact, absolute or relative, and are compared by range, sensitivity, resolution, accuracy, precision, linearity, response time, hysteresis and drift. Each physical quantity has typical sensors (encoders and Hall sensors for position, PIR and ultrasonic for motion and occupancy, MEMS for acceleration, strain gauges for force, piezoresistive for pressure, turbines for flow, thermistors, RTDs, thermocouples and ICs for temperature, MQ and electrochemical for gases, PPG for pulse and SpO2). The Arduino is a microcontroller board for simple real-time control; the Raspberry Pi is a Linux computer with 3.3 V GPIO and no ADC.

1. Distinguish active and passive, analog and digital, contact and no-contact, absolute and relative sensors, with two examples each.
2. Define range, sensitivity, resolution, accuracy and precision. Can a sensor be precise but inaccurate? Explain.
3. A 10-bit ADC with a 5 V reference reads 410. Find the voltage and, for an LM35, the temperature. What is the resolution of the chain?
4. Explain the working of a PIR sensor. Why does it fail to detect a person who is sitting still?
5. An ultrasonic sensor's echo lasts 2,330 microseconds. Find the distance at 343 m/s.
6. Explain the working of an accelerometer and a strain gauge.
7. A thermistor circuit gives ADC 400 (10 bit) with a 10 kilohm fixed resistor on top and the NTC below; $B=3950$, $R_0=10$ kilohm at 25 degrees C. Find the temperature.
8. Compare thermistor, RTD, thermocouple and the DS18B20.
9. Explain how a pulse oximeter works.
10. Why does a motor need a driver? Explain PWM and find the average voltage for a duty cycle of 40 percent on a 12 V supply.
11. Compare Arduino Uno and Raspberry Pi 4 in six points.
12. Write the steps to read a DHT22 and an LDR and use them to switch a lamp. Draw the block diagram.
13. A flow sensor with $f=7.5Q$ gives 90 pulses in 4 seconds. Find the flow and the volume in 1 minute.
14. A wheel has 12 slots and the encoder gives 90 pulses in 3 seconds. Find the rpm.

**Answers to the numerical items.** (3) $410\times5/1024=2.002$ V, $T=200$ degrees C, which is outside the useful LM35 range for this example (use 1.1 V reference); resolution 0.49 degrees C. (5) $343\times2330\times10^{-6}/2=0.400$ m = 40 cm. (7) $R_s=10\times400/623=6.42$ k$\Omega$; $1/T=0.0033540+\ln(0.642)/3950=0.0033540-0.0001124=0.0032416$, $T=308.5$ K $=35.3$ degrees C. (10) $0.4\times12=4.8$ V. (13) $f=90/4=22.5$ Hz, $Q=3$ L/min, 3 L per minute. (14) $90/3=30$ pulses per second, $30/12=2.5$ rev/s, 150 rpm.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Classify sensors with examples.**

Active sensors need an external supply (thermistor, strain gauge, ultrasonic ranger); passive sensors produce their own signal (thermocouple, photovoltaic cell, piezoelectric microphone). Analog sensors give a continuous output that needs an ADC (LM35, LDR); digital sensors give discrete values or messages (DHT22, DS18B20, PIR). Contact sensors touch the medium (thermocouple, pH probe); no-contact sensors measure remotely (infrared thermometer, ultrasonic, camera). Absolute sensors have a fixed zero (absolute encoder); relative sensors report changes (incremental encoder).

**Q2 (5 marks). Read an LM35 with ADC value 410 using a 1.1 V reference.**

Voltage $=410\times1.1/1024=0.4404$ V. Temperature $=0.4404/0.010=44.0$ degrees C. The step is $1.1/1024=1.07$ mV so the resolution is 0.107 degrees C. With a 5 V reference the same count would mean 200 degrees C, which shows that the reference must match the formula in the code.

**Q3 (10 marks). Explain the working of temperature sensors and choose one for a cold-storage room.**

*Introduction.* Temperature sensors turn heat into resistance, voltage or a digital value.

*Body.* Thermistor: NTC resistance falls with temperature, strongly non-linear, converted with the beta equation after a divider. RTD: platinum resistance rises almost linearly, $R=R_0(1+\alpha T)$, most accurate and stable. Thermocouple: Seebeck voltage between two metals, about 41 microvolts per degree C for type K, passive, for high temperatures, needs cold-junction compensation. Integrated sensors: LM35 gives 10 mV per degree C; DS18B20 gives a digital reading over 1-Wire with a unique ID.

*Choice.* For a cold room between -20 and +10 degrees C with several points of measurement: the DS18B20 (range -55 to 125, 0.5 degree accuracy, many on one wire, waterproof probe versions).

*Conclusion.* Match range, accuracy, interface and cost; calibrate against a reference.

**Q4 (10 marks). Compare Arduino and Raspberry Pi and describe how you would connect a sensor to each.**

*Introduction.* Both are used as IoT nodes but they sit at different points on the scale.

*Comparison.* Arduino: microcontroller, 16 MHz, 2 KB RAM, no OS, 10-bit ADC, 5 V logic, low power, real-time. Raspberry Pi: single-board computer, quad-core 1.5 GHz, GB of RAM, Linux, no ADC, 3.3 V logic, more power, not real-time, good as a gateway.

*Connection.* Arduino: wire the LM35 to 5 V, A0 and ground; read with `analogRead(A0)` and convert as in Section 2.3. Pi: wire a DHT22 to 3.3 V, GPIO4 and ground and read it with a library; for an analog sensor add an MCP3008 on the SPI bus and read counts with `spidev`.

*Conclusion.* Use the Arduino for the node that senses and acts; use the Pi where networking, storage, cameras or Python services are needed.

**Q5 (10 marks). Describe actuators and explain PWM with a motor example.**

*Introduction.* Actuators convert electrical commands into physical action, and need drivers because a microcontroller pin cannot supply their current.

*Body.* LED with series resistor, relay with transistor and flyback diode, DC motor with H-bridge, servo with 1 to 2 ms pulses every 20 ms, stepper with step and direction pulses, solenoid and pump through a MOSFET. PWM switches a pin between 0 and $V$ and the average is $D\cdot V$. Figure 2.4 shows 25, 50 and 75 percent.

*Example.* A 12 V motor at $D=0.4$ sees an average of 4.8 V and runs slower. On the Uno, `analogWrite(9, 102)` gives $102/255=40$ percent.

*Conclusion.* Always drive loads through a suitable driver with protection and control power with PWM rather than by series resistance, which wastes energy as heat.
