---
file: NEBians-IOE-Past-Paper-Instrumentation-ENEX252-2082-Bhadra.pdf
subject: Instrumentation
level: BE · Year II / Part II
code: ENEX 252
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular paper (new course), BE Electronics and Communication / Computer (BEI, BCT), Year II / Part II. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt All questions · The figures in the margin indicate Full Marks · Assume suitable data if necessary</small>

@q 1
Explain closed loop microprocessor based instrumentation system with useful example. [[3]]

@q 2
a) Define errors and list out its types. [[2]]

b) Analyze the significance of accuracy vs. precision in different measurement scenarios. Can you have high precision but poor accuracy? Illustrate with an example. [[4]]

@q 3
a) A linear resistance potentiometer is 50 mm long and is uniformly wound with a wire of total resistance 5,000 Ω under normal condition, the slider is at the center of the potentiometer. Determine the linear displacement when the resistance of the POT as measured by a Wheatstone bridge is 1850 Ω. If it is possible to measure a minimum value of 5 Ω resistance with the above arrangement determine the resolution of the POT in mm. [[4]]

b) Define an optical sensor and describe its simple working principle with an example. [[4]]

@q 4
a) Explain the block diagram of mode 1 input configuration and also write its control word and status word. [[5]]

b) Draw the general block diagram of Atmega328 (AVR) CPU microcontroller. Briefly explain its features. [[5]]

c) How can interface temperature sensor using I2C protocol with Atmega328 microcontroller? Explain with circuit diagram and program. [[5]]

@q 5
What do you mean by WSN and how it is different from traditional sensors? Explain protocol stack diagram of ZIGBEE. [[3+3]]

@q 6
Write an importance of decoupling, ground bounce, cross talk and impedance matching in designing circuit. [[4]]

@q 7
List out the steps for Software development life cycle. Explain how prototype software development model is different from waterfall model. [[2+4]]

@q 8
Explain the working principle of Electrodynamometer type wattmeter with its mathematical expression of deflection for both AC and DC operations. [[6]]

@q 9
Explain the structural block diagram of smart sensor. [[3]]

@q 10
Define Industrial 4.0. What might be the challenges to implement automation system in industrial instrumentation system? [[1+2]]

<!-- SOLUTIONS -->

@s 1
**Closed-loop microprocessor-based instrumentation system.** In a closed-loop system the measured output is **fed back** and compared with the desired value (set-point); the microprocessor computes the control action from the error and drives an actuator so that the process variable is held at the set-point despite disturbances. The blocks are:

1. **Sensor / transducer** converts the process variable (temperature, pressure, speed) into an electrical signal.
2. **Signal conditioning:** amplifier, filter, linearisation, level shifter.
3. **ADC** (with a sample-and-hold, multiplexer) converts it into a digital word.
4. **Microprocessor / microcontroller:** reads the digital value, computes the error $e = r - y$ against the set-point $r$, applies the control law (on/off, **PID**: $u = K_pe + K_i\int e\,dt + K_d\,de/dt$), displays the value and handles alarms.
5. **DAC / PWM output and driver:** converts the control word to an analogue signal and power-amplifies it.
6. **Actuator / final control element** (heater, valve, motor) acts on the process, closing the loop.

```figure caption="Question 1: closed-loop microprocessor-based temperature control (electric furnace)."
fig,ax=plt.subplots(figsize=(6.8,2.7)); ax.axis('off'); ax.set_xlim(0,15); ax.set_ylim(0,5.2)
def bx(x,y,w,h,t,fc='#e0f2fe'):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=INK,lw=1)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=6.8)
bx(0.2,2.9,2.0,1.3,'Set-point\n(keypad)','#fef9c3'); bx(3.2,2.9,3.0,1.3,'Microcontroller\nPID algorithm\ndisplay, alarm','#dbeafe')
bx(7.2,2.9,2.0,1.3,'PWM / DAC\n+ TRIAC driver'); bx(10.2,2.9,2.0,1.3,'Heater\n(actuator)','#fde68a'); bx(12.8,2.9,2.0,1.3,'Furnace\n(process)','#dcfce7')
bx(10.2,0.5,2.0,1.3,'Sensor\nLM35 / PT100'); bx(7.2,0.5,2.0,1.3,'Signal\nconditioning'); bx(4.2,0.5,2.0,1.3,'ADC\n(10-bit)')
for a,b in (((2.2,3.55),(3.2,3.55)),((6.2,3.55),(7.2,3.55)),((9.2,3.55),(10.2,3.55)),((12.2,3.55),(12.8,3.55)),((13.8,2.9),(12.2,1.15)),((10.2,1.15),(9.2,1.15)),((7.2,1.15),(6.2,1.15)),((5.2,1.8),(5.2,2.9))): arrow(ax,a,b,None,color=INK)
ax.text(8.7,0.15,'feedback',fontsize=7,ha='center',color=ACCENT)
```

*Example:* in an **oven / furnace temperature controller** an LM35 or PT100 gives a voltage, which is amplified and digitised (ADC); if the oven is at 180 °C against a set-point of 200 °C, the microcontroller computes the error and a PID output, which sets the PWM duty cycle of a TRIAC / solid-state relay controlling the heater, so the temperature settles at 200 °C. The same structure serves motor-speed regulation, level control and battery chargers.

@s 2
**(a) Error.** The **error** is the difference between the measured value and the true value of the quantity: $e = x_m - x_t$ (absolute error), or $\varepsilon = e/x_t\times100\ \%$ (relative error).

**Types of errors**

1. **Gross errors:** human mistakes in reading, recording or using the instrument, or a faulty instrument (wrong range, misplaced decimal).
2. **Systematic errors:** repeatable, with a definite sign: *instrumental* (zero error, calibration drift, friction, loading error), *environmental* (temperature, humidity, vibration, magnetic field), and *observational* (parallax, wrong estimation). They can be reduced by calibration and correction.
3. **Random (accidental) errors:** small unpredictable variations from noise, fluctuations, resolution; they follow a Gaussian distribution and are reduced by averaging many readings.
4. By behaviour: **static errors** (steady, e.g. offset, gain error, non-linearity, hysteresis) and **dynamic errors** (the lag of the instrument when the input changes, with time constant and response time).

**(b) Accuracy against precision.**

- **Accuracy** is how close a measurement is to the **true** value (the systematic error, or bias).
- **Precision** is how close **repeated** measurements are to **one another** (the spread, repeatability; random error), whatever the true value.

| Scenario | Which is critical |
|---|---|
| Calibration labs, billing (energy meters), pharmaceutical dosing | **Accuracy** first, then precision; traceable to a standard |
| Process control on a repeating batch, closed-loop control of a drive | **Precision** (repeatability) matters most, a constant offset can be trimmed out |
| Monitoring a trend or a change (leak detection, vibration trending) | Precision / resolution; absolute accuracy is secondary |
| Safety limits (boiler pressure trip) | Both: accuracy to protect, precision to avoid nuisance trips |

**Yes: high precision with poor accuracy is possible.** It happens when the instrument has a **large systematic error** but a small random error: a miscalibrated or zero-shifted instrument.

*Illustration:* the true voltage of a reference is 5.00 V. A voltmeter with a +0.12 V offset gives 5.12, 5.13, 5.12, 5.11, 5.12 V. The spread is only ±0.01 V (standard deviation $\approx$ 0.007 V, very precise) but the mean 5.12 V is in error by $+0.12$ V, i.e. $+2.4\ \%$ (poor accuracy). Calibration (subtracting 0.12 V) would make it both precise and accurate. The target analogy below shows the four cases.

```figure caption="Question 2(b): accuracy and precision shown as shots on a target."
fig,axs=plt.subplots(1,4,figsize=(6.8,2.0))
rng=np.random.RandomState(3)
cases=(('accurate, precise',0,0,0.08),('accurate, imprecise',0,0,0.45),('precise, inaccurate',0.55,0.4,0.08),('neither',-0.4,0.5,0.45))
for ax,(t,cx,cy,sd) in zip(axs,cases):
    ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.1,1.1); ax.set_ylim(-1.1,1.1); ax.set_title(t,fontsize=7)
    for r,f in ((1.0,'#e2e8f0'),(0.66,'#cbd5e1'),(0.33,'#94a3b8')): ax.add_patch(Circle((0,0),r,fc=f,ec=INK,lw=0.6))
    ax.plot(0,0,'+',color=INK)
    px=cx+rng.randn(6)*sd; py=cy+rng.randn(6)*sd
    ax.plot(px,py,'o',color='#dc2626',ms=3)
```

@s 3
**(a) Linear potentiometer.** Length $L = 50$ mm, total resistance $R_T = 5000\ \Omega$, so the resistance per unit length is $5000/50 = 100\ \Omega/\text{mm}$. At the normal position the slider is at the centre: $x_0 = 25$ mm, $R_0 = 2500\ \Omega$.

The bridge measures the resistance of the potentiometer (between the slider and the reference end) as $R_x = 1850\ \Omega$:

$$x = \frac{R_x}{R_T}L = \frac{1850}{5000}\times50 = 18.5\ \text{mm from the reference end}$$

$$\boxed{\Delta x = x - x_0 = 18.5 - 25 = -6.5\ \text{mm}}$$

The slider has moved **6.5 mm towards the reference end** (equivalently $\Delta R = 1850 - 2500 = -650\ \Omega$, so $\Delta x = 650/100 = 6.5$ mm).

**Resolution.** The smallest measurable resistance change is 5 Ω, so

$$\text{resolution} = \frac{5\ \Omega}{100\ \Omega/\text{mm}} = \mathbf{0.05\ mm}$$

(or $0.1\ \%$ of the full span: $0.05/50 = 0.1\ \%$).

**(b) Optical sensor.** An optical (photo) sensor converts **light** (intensity, presence or wavelength, from the UV to the IR) into an **electrical signal**. The working principle is based on the **photoelectric effect**: photons of energy $h\nu \ge E_g$ create electron-hole pairs in a semiconductor (internal photoelectric / photoconductive effect) or release electrons from a metal (external effect), which changes a resistance, a current or a voltage in proportion to the illumination.

*Types:* LDR (photoresistor), photodiode, phototransistor, photovoltaic cell, photomultiplier tube, CCD/CMOS image sensor, and optical encoders and optocouplers.

*Example: LDR (CdS cell).* Its resistance falls from about 1 MΩ in the dark to a few hundred ohms in bright light. In a voltage divider with a fixed resistor $R$:

$$V_o = V_{cc}\frac{R}{R + R_{LDR}}$$

$V_o$ rises with the illumination, and an ADC or a comparator gives a light-controlled switch (automatic street light). A **photodiode** operated in reverse bias gives $I_{ph} = S\,P$ (S = responsivity, A/W), which is fast and linear, and is used in a transimpedance amplifier ($V_o = -I_{ph}R_f$), in the barcode reader and in the optical fibre receiver.

```figure caption="Question 3(b): LDR in a voltage divider giving an output that rises with the light."
fig,ax=plt.subplots(figsize=(3.6,3.0)); ax.axis('off'); ax.set_xlim(-0.8,3.8); ax.set_ylim(-0.4,4.4)
wire(ax,[(0,0),(2,0)]); wire(ax,[(1,0),(1,0)])
wire(ax,[(1,4),(1,3.4)]); res(ax,(1,3.4),(1,2.1),'R',side=1,body=0.8); wire(ax,[(1,2.1),(1,1.9)]); node(ax,(1,1.95))
res(ax,(1,1.9),(1,0.5),'LDR',side=1,body=0.8); wire(ax,[(1,0.5),(1,0)])
wire(ax,[(1,1.95),(2.6,1.95)]); arrow(ax,(2.6,1.95),(3.4,1.95),'$V_o$ to ADC',off=0.25)
ax.text(1,4.15,'+$V_{cc}$',ha='center',fontsize=8); ax.text(1,-0.3,'GND',ha='center',fontsize=8)
arrow(ax,(-0.5,3.0),(0.3,1.3),'light',color=ACCENT,off=0.35)
```

@s 4
**(a) Mode 1 (strobed input) of the 8255.** In mode 1 input, port A (group A) and port B (group B) are used as **8-bit input ports with handshaking**; the handshake signals are taken from port C:

| Signal | Port A | Port B | Direction | Function |
|---|---|---|---|---|
| STB (strobe, active low) | PC4 | PC2 | input | the peripheral loads the data into the input latch |
| IBF (input buffer full) | PC5 | PC1 | output | high: the data are latched and not yet read; set by $\overline{STB}$ low, reset by the rising edge of $\overline{RD}$ |
| INTR (interrupt request) | PC3 | PC0 | output | set when $\overline{STB} = 1$, IBF = 1 and INTE = 1; reset by the falling edge of $\overline{RD}$ |
| INTE (interrupt enable flip-flop) | via PC4 (BSR) | via PC2 (BSR) | internal | enables the interrupt |
| PC6, PC7 | free (I/O), when A is in mode 1 input | | | general I/O (set by D3) |

**Operation:** (1) the input device places data on the port lines and drives $\overline{STB}$ low; (2) the 8255 latches the data and IBF goes high, telling the peripheral not to send more; (3) when $\overline{STB}$ returns high, INTR goes high (if INTE is set) and interrupts the CPU; (4) the CPU reads the port with $\overline{RD}$; the falling edge of $\overline{RD}$ clears INTR and the rising edge clears IBF, ready for the next byte.

```figure caption="Question 4(a): mode 1 strobed-input timing: STB loads the data, IBF goes high, INTR requests service, RD clears them."
fig,ax=plt.subplots(figsize=(6.4,2.8))
t=np.arange(0,12.01,0.01)
def sig(pts,off,col,name):
    xs=[0];ys=[pts[0][1]]
    for x,y in pts:
        xs+= [x,x]; ys+=[ys[-1],y]
    xs.append(12); ys.append(ys[-1])
    ax.plot(xs,np.array(ys)*0.7+off,color=col,lw=1.6); ax.text(-0.2,off+0.35,name,ha='right',va='center',fontsize=7.5)
sig([(0,1),(2,0),(4,1)],6.0,INK,'STB'); sig([(0,0),(2,1),(8,0)],4.5,ACCENT,'IBF'); sig([(0,0),(4,1),(7,0)],3.0,SERIES[2],'INTR'); sig([(0,1),(7,0),(8,1)],1.5,SERIES[3],'RD'); sig([(0,0),(2,1),(8,0)],0.0,MUTED,'Data latched')
for x,l in ((2,'data in,\nIBF=1'),(4,'INTR=1'),(7,'RD low\nclears INTR'),(8,'RD high\nclears IBF')): ax.axvline(x,color=GRID,ls=':',lw=0.8); ax.text(x,7.1,l,ha='center',fontsize=6.3)
ax.set_xlim(-0.2,12); ax.set_ylim(-0.3,7.9); ax.axis('off')
```

**Control word (I/O mode, group A and B in mode 1, both ports input):**

| D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 1 | x | 1 | 1 | x |
| I/O mode | group A mode 1 | | port A input | PC7-PC6 in (1) or out (0) | group B mode 1 | port B input | PC2-PC0 not used (handshake) |

With PC7, PC6 as outputs: $1011\,0110 = $ **B6H** (with them as inputs: BEH). To enable the interrupts use BSR: PC4 = 1 (INTE A) with 09H, PC2 = 1 (INTE B) with 05H.

**Status word** (read from port C in mode 1 input):

| D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 |
|---|---|---|---|---|---|---|---|
| I/O | I/O | IBF A | INTE A | INTR A | INTE B | IBF B | INTR B |

**(b) ATmega328 (AVR) microcontroller.** An 8-bit AVR RISC microcontroller with a **Harvard** architecture (separate program and data memories), a 2-stage pipeline (fetch and execute in parallel), and most instructions executed in a single clock (1 MIPS/MHz, up to 20 MHz).

**Features**

- **CPU:** 131 instructions, **32 × 8 general-purpose registers** directly connected to the ALU (two registers accessed in one cycle), status register SREG, 16-bit program counter, stack pointer, instruction decoder.
- **Memory:** 32 KB in-system programmable **Flash** (10 000 write cycles), 2 KB **SRAM**, 1 KB **EEPROM** (100 000 cycles); bootloader section with lock bits.
- **I/O:** 23 programmable I/O lines in three ports (B, C, D); the port pins are multiplexed with the alternate peripheral functions.
- **Timers/Counters:** Timer0 (8-bit), Timer1 (16-bit), Timer2 (8-bit, with an RTC oscillator), 6 PWM channels, input capture, compare match.
- **ADC:** 10-bit, 6 channels (8 in the SMD package) with an internal temperature sensor and 1.1 V reference; analogue comparator.
- **Serial interfaces:** USART, SPI master/slave, 2-wire serial interface TWI (I²C).
- **Interrupt controller:** 26 interrupt vectors (external INT0 and INT1, pin change, timers, ADC, serial); watchdog timer with its own oscillator; brown-out detector, power-on reset.
- **Clock and power:** internal 8 MHz RC oscillator or an external crystal/resonator (up to 20 MHz); six sleep modes (idle, ADC noise reduction, power-save, power-down, standby, extended standby); 1.8 to 5.5 V operation.

```figure caption="Question 4(b): block diagram of the ATmega328 microcontroller."
fig,ax=plt.subplots(figsize=(6.8,4.0)); ax.axis('off'); ax.set_xlim(0,14); ax.set_ylim(0,8.2)
def bx(x,y,w,h,t,fc='#e0f2fe'):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=INK,lw=1)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=6.6)
bx(0.2,6.0,2.8,1.4,'Flash 32 KB\n+ program counter','#dcfce7'); bx(3.4,6.0,2.4,1.4,'Instruction\nregister /\ndecoder','#dbeafe'); bx(6.2,6.0,2.8,1.4,'Control lines,\nSREG, stack ptr','#dbeafe')
bx(0.2,3.8,2.8,1.4,'SRAM 2 KB','#dcfce7'); bx(3.4,3.8,2.4,1.4,'32 x 8\ngeneral registers','#dbeafe'); bx(6.2,3.8,2.8,1.4,'ALU','#dbeafe'); bx(0.2,1.8,2.8,1.4,'EEPROM 1 KB','#dcfce7')
bx(9.8,6.0,4.0,1.4,'Timers 0/1/2, PWM,\nwatchdog, interrupts','#fde68a'); bx(9.8,4.0,4.0,1.4,'10-bit ADC (6 ch),\nanalogue comparator','#fde68a'); bx(9.8,2.0,4.0,1.4,'USART, SPI, TWI (I2C)','#fde68a'); bx(9.8,0.2,4.0,1.2,'I/O ports B, C, D\n(23 lines)','#fef9c3')
bx(3.4,1.8,5.6,1.4,'8-bit internal data bus','#e2e8f0')
bx(0.2,0.2,5.6,1.1,'Clock, reset, power supervision (POR, BOD), 8 MHz RC / crystal','#f1f5f9')
for a,b in (((1.6,6.0),(1.6,5.2)),((4.6,6.0),(4.6,5.2)),((7.6,6.0),(7.6,5.2)),((9.0,6.7),(9.8,6.7)),((9.0,4.5),(9.8,4.7)),((9.0,2.5),(9.8,2.7))): arrow(ax,a,b,None,color=MUTED,lw=1.0)
```

**(c) Interfacing an I²C temperature sensor (TMP102 or LM75) with the ATmega328.** The ATmega's **TWI** (hardware I²C) uses **SDA = PC4** and **SCL = PC5**. The two lines are open-drain, so each needs a **4.7 kΩ pull-up** to +5 V (use a 3.3 V sensor with a level shifter, or a 5 V LM75). The sensor has the 7-bit address **0x48** (ADD0 to GND) and a 12-bit temperature register at pointer 0x00.

**Circuit:** ATmega328 PC4 (SDA) to sensor SDA; PC5 (SCL) to sensor SCL; 4.7 kΩ resistors from SDA and SCL to $V_{cc}$; sensor $V_{cc}$ and GND to the supply (0.1 µF decoupling); ADD0 to GND; (an LCD or the UART shows the reading).

```figure caption="Question 4(c): TMP102 I2C temperature sensor connected to the ATmega328 TWI pins with pull-up resistors."
fig,ax=plt.subplots(figsize=(6.4,3.0)); ax.axis('off'); ax.set_xlim(0,13); ax.set_ylim(0,6)
ax.add_patch(Rectangle((0.3,1.2),3.2,3.8,fc='#dbeafe',ec=INK,lw=1.2)); ax.text(1.9,4.5,'ATmega328',ha='center',fontsize=8,weight='bold')
ax.add_patch(Rectangle((9.0,1.2),3.0,3.8,fc='#dcfce7',ec=INK,lw=1.2)); ax.text(10.5,4.5,'TMP102',ha='center',fontsize=8,weight='bold'); ax.text(10.5,1.6,'addr 0x48\nADD0 = GND',ha='center',fontsize=6.5)
for y,n1,n2 in ((3.4,'PC4 / SDA','SDA'),(2.4,'PC5 / SCL','SCL')):
    ax.plot([3.5,9.0],[y,y],color=INK,lw=1.3); ax.text(3.45,y+0.1,n1,fontsize=6.8,ha='right'); ax.text(8.9,y+0.1,n2,fontsize=6.8,ha='right')
ax.plot([5.2,5.2],[5.6,3.4],color=INK,lw=1.0); ax.plot([7.4,7.4],[5.6,2.4],color=INK,lw=1.0); ax.plot([5.0,7.6],[5.6,5.6],color=INK,lw=1.3); ax.text(6.3,5.75,'+Vcc',fontsize=7,ha='center')
for x in (5.2,7.4): ax.add_patch(Rectangle((x-0.12,4.1),0.24,0.9,fc='white',ec=INK,lw=1.0)); ax.text(x+0.25,4.5,'4.7k',fontsize=6.5)
ax.plot([5.2],[3.4],'o',color=INK,ms=3); ax.plot([7.4],[2.4],'o',color=INK,ms=3)
```

**Program (avr-gcc, C), polling the TWI hardware:**

```c
#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>
#define TMP102_W 0x90          /* 0x48 << 1 | write */
#define TMP102_R 0x91          /* 0x48 << 1 | read  */

static void twi_init(void) { TWSR = 0; TWBR = 72; }          /* SCL = 16 MHz / (16 + 2*72) = 100 kHz */
static void twi_start(void) { TWCR = (1<<TWINT)|(1<<TWSTA)|(1<<TWEN); while (!(TWCR & (1<<TWINT))); }
static void twi_stop(void)  { TWCR = (1<<TWINT)|(1<<TWSTO)|(1<<TWEN); }
static void twi_write(uint8_t d) { TWDR = d; TWCR = (1<<TWINT)|(1<<TWEN); while (!(TWCR & (1<<TWINT))); }
static uint8_t twi_read_ack(void)  { TWCR = (1<<TWINT)|(1<<TWEN)|(1<<TWEA); while (!(TWCR & (1<<TWINT))); return TWDR; }
static uint8_t twi_read_nack(void) { TWCR = (1<<TWINT)|(1<<TWEN);           while (!(TWCR & (1<<TWINT))); return TWDR; }

float read_temperature(void)
{
    twi_start();  twi_write(TMP102_W);  twi_write(0x00);     /* pointer = temperature register */
    twi_start();  twi_write(TMP102_R);                       /* repeated start, read mode      */
    uint8_t msb = twi_read_ack();
    uint8_t lsb = twi_read_nack();
    twi_stop();
    int16_t raw = ((int16_t)msb << 8 | lsb) >> 4;            /* 12-bit two's complement        */
    return raw * 0.0625f;                                    /* 0.0625 degC per LSB            */
}

int main(void)
{
    twi_init();
    while (1) {
        float t = read_temperature();                        /* e.g. 0x1900 -> 25.0 degC       */
        /* send t to LCD / UART here */
        _delay_ms(500);
    }
}
```

Check: the register bytes `0x19 0x00` give $\text{raw} = 0x190 = 400$ and $T = 400\times0.0625 = 25.0\ ^\circ\text{C}$.

@s 5
**WSN (wireless sensor network).** A WSN is a network of spatially distributed, small, low-power, battery-operated **sensor nodes** (each with a sensor, a microcontroller, a radio transceiver and a power source) that **cooperatively monitor** physical or environmental conditions (temperature, humidity, vibration, pollution), process the data locally and **forward it wirelessly, hop by hop, to a sink / base station (gateway)**, from where it goes to a user or the Internet. Topologies: star, tree, mesh.

**Difference from traditional sensors**

| | **Traditional (wired) sensor** | **Wireless sensor network node** |
|---|---|---|
| Connection | Point-to-point cable to the controller / DAQ | Wireless, multi-hop network, no cable |
| Deployment | Fixed, costly wiring, hard in remote or moving places | Easy, ad hoc, remote and hazardous sites, scalable to hundreds or thousands of nodes |
| Power | Mains or loop powered | Battery or energy harvesting: energy is the critical resource |
| Processing | Raw analogue signal to a central unit | **In-node (in-network) processing**, data aggregation, compression |
| Network | None, each sensor is separate | **Self-organising, self-healing** routing around failed nodes |
| Cost / maintenance | High installation cost, easy to maintain | Low installation cost, battery replacement needed |
| Data rate / reliability | High and steady | Low rate, shared channel, packet loss and interference |

**ZigBee protocol stack.** ZigBee (based on IEEE 802.15.4) is a low-rate (250 kbps at 2.4 GHz), low-power, low-cost standard for WSN. Layers from the bottom:

1. **PHY layer (IEEE 802.15.4):** radio operation in the 868 MHz (20 kbps), 915 MHz (40 kbps) and 2.4 GHz (250 kbps, 16 channels) bands, O-QPSK / BPSK modulation with DSSS, energy detection, link-quality indication, channel selection.
2. **MAC layer (IEEE 802.15.4):** channel access by CSMA/CA (with an optional beacon-enabled superframe and guaranteed time slots), frame validation, acknowledgements, association and disassociation.
3. **Network (NWK) layer (ZigBee):** network formation and joining, address assignment, **routing** (AODV mesh, cluster-tree), multi-hop forwarding, security.
4. **Application support sub-layer (APS):** binding, address mapping between the devices and the endpoints, fragmentation, reliable data transfer.
5. **ZigBee device object (ZDO):** the device roles and discovery (coordinator, router, end device); security manager; **Application framework** with up to 240 application objects (profiles such as Home Automation and Smart Energy).
6. **Security service provider** (across the layers): AES-128 encryption, authentication, key management.

**Devices:** *coordinator* (one per network; starts it, holds the trust centre), *router* (relays data, extends the range), *end device* (low-power, sleeps most of the time).

```figure caption="Question 5: ZigBee protocol stack on top of IEEE 802.15.4."
fig,ax=plt.subplots(figsize=(5.8,3.3)); ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,7)
def bx(x,y,w,h,t,fc):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=INK,lw=1)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=7.2)
bx(1.0,5.6,7.0,1.0,'Application (profiles, application objects, endpoints 1-240)','#fde68a')
bx(1.0,4.4,3.4,1.0,'Application support (APS)','#fde68a'); bx(4.6,4.4,3.4,1.0,'ZigBee device object (ZDO)','#fde68a')
bx(1.0,3.2,7.0,1.0,'Network layer (NWK): formation, addressing, routing','#dbeafe')
bx(1.0,2.0,7.0,1.0,'MAC layer (IEEE 802.15.4): CSMA/CA, ACK, beacons','#dcfce7')
bx(1.0,0.8,7.0,1.0,'PHY layer (IEEE 802.15.4): 868 / 915 MHz, 2.4 GHz','#dcfce7')
bx(8.4,0.8,2.6,5.8,'Security\nservice\nprovider\n(AES-128)','#f1f5f9')
ax.text(0.9,0.2,'ZigBee Alliance (layers 3-7)  over  IEEE 802.15.4 (layers 1-2)',fontsize=6.5,color=MUTED)
```

@s 6
**Importance of decoupling, ground bounce, cross-talk and impedance matching in circuit design**

**1. Decoupling (bypass) capacitors.** When the gates of a digital IC switch, they draw sharp current pulses $di/dt$. The inductance of the supply track $L$ makes the supply drop $\Delta V = L\,\dfrac{di}{dt}$. A **0.1 µF ceramic capacitor placed right at the IC's V$_{cc}$ pin** acts as a local charge reservoir and a low-impedance path for the high-frequency current, so (a) the supply rail stays steady, (b) switching noise is not conducted onto the common supply and to the other circuits, (c) there is less EMI. Use a 0.1 µF with a 10 µF bulk capacitor per board section, and a ferrite bead between analogue and digital supplies. Without decoupling an ADC reads erratically and the logic can mis-trigger.

**2. Ground bounce.** When several outputs switch at the same time, their return current $di/dt$ flows through the **inductance of the ground lead / package pin** $L_g$, which lifts the local IC ground relative to the board ground by

$$V_{gb} = L_g\frac{di}{dt}$$

For example, 8 outputs each switching 20 mA in 2 ns through a 5 nH ground lead give

$$V_{gb} = 5\ \text{nH}\times\frac{8\times20\ \text{mA}}{2\ \text{ns}} = 0.4\ \text{V}$$ This shifts the logic thresholds and gives false switching on a quiet output, latch-up, and data errors. **Remedy:** a continuous low-inductance **ground plane**, several ground pins and short, wide return paths, decoupling capacitors, limiting the simultaneous switching, slower edge rates and series damping resistors, and separating the analogue and digital grounds.

**3. Cross-talk.** Unwanted coupling of signals between **neighbouring tracks or wires** by mutual capacitance $C_m$ (electric, current $i = C_m\,dv/dt$) and mutual inductance $M$ (magnetic, voltage $v = M\,di/dt$). A fast edge on an aggressor line induces a pulse on the victim line, which gives false data, jitter and noise on sensitive analogue lines. **Remedy:** increase the spacing (the **3W rule**: centre spacing at least 3 trace widths), keep the parallel run short, place the tracks close above a ground plane, route adjacent layers at right angles, use **guard traces** with grounded vias, differential signalling and twisted pair or shielded cable, and slower edges.

**4. Impedance matching.** When the track length exceeds about $t_r/(6\,t_{pd})$ (the rise time $t_r$ shorter than six propagation delays), the track behaves as a **transmission line** with characteristic impedance $Z_0$. A mismatch between the load $Z_L$ and $Z_0$ makes a reflection with the coefficient

$$\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$$

which causes overshoot, undershoot, ringing, and data errors. Matching the source and load to $Z_0$ (50 Ω for RF, 100 Ω differential for USB / Ethernet; controlled-impedance PCB layers with a defined width and dielectric) by **series termination** (a resistor at the source, $R_s = Z_0 - R_{out}$) or **parallel (shunt) termination** (a resistor $Z_0$ at the load) removes the reflection ($\Gamma = 0$) and also gives maximum power transfer in RF and antenna systems.

@s 7
**Steps of the software development life cycle (SDLC)**

1. **Planning and feasibility study** (scope, cost, schedule, risk).
2. **Requirement analysis and specification** (SRS).
3. **System and software design** (architecture, modules, data, user interface).
4. **Implementation (coding)**.
5. **Testing** (unit, integration, system, acceptance).
6. **Deployment (installation / release)**.
7. **Operation and maintenance** (corrective, adaptive, perfective, preventive).

**Prototype model against waterfall model**

| | **Waterfall model** | **Prototype model** |
|---|---|---|
| Process | Linear and sequential: requirements, design, code, test, deploy; each phase completes before the next, no going back | **Iterative:** a quick working prototype is built, evaluated by the user, refined and repeated until accepted, then the final system is built |
| Requirements | Must be **fully known and frozen** at the start | Unclear or changing requirements are accepted; they are discovered through the prototype |
| User involvement | Mainly at the start (requirements) and at the end (acceptance) | **Continuous**, at each evaluation |
| Working software | Only at the end of the project | Early (the prototype) |
| Risk | High: errors in the requirements are found late and are costly | Low: misunderstandings are found early |
| Change handling | Difficult and expensive | Easy |
| Documentation | Heavy, formal at every phase | Lighter; may be incomplete |
| Cost and time | Predictable for stable projects | May increase through repeated iterations, and the prototype may be thrown away |
| Suitable for | Small, well-understood projects (embedded firmware with fixed specifications) | Projects with unclear needs, user-interface intensive systems |

@s 8
**Electrodynamometer-type wattmeter.**

**Construction.** Two coils: a pair of **fixed coils** (the current coil, CC, of few turns of thick wire, in series with the load, carrying the load current $i_1 = i$) and a **moving coil** (the pressure or potential coil, PC, many turns of fine wire in series with a high non-inductive resistor $R_p$ across the supply, carrying $i_2 = v/R_p$). The pointer is attached to the moving coil, controlled by spiral springs (controlling torque $T_c = K\theta$), with air-friction damping and no iron (no hysteresis loss, so it is accurate to 0.1 to 0.25 %).

**Principle.** The torque is produced by the interaction of the magnetic field of the fixed coils with the current in the moving coil. The instantaneous deflecting torque is

$$T_i = i_1i_2\frac{dM}{d\theta}$$

where $M$ is the mutual inductance between the coils.

**DC operation.** $i_1 = I$ (load current) and $i_2 = V/R_p$ (constant). The torque is constant:

$$T_d = I\,\frac{V}{R_p}\,\frac{dM}{d\theta}$$

At equilibrium $T_d = T_c = K\theta$:

$$\boxed{\theta = \frac{1}{K}\,\frac{VI}{R_p}\,\frac{dM}{d\theta} \ \propto\ VI = P}$$

**AC operation.** Let $v = V_m\sin\omega t$ and $i = I_m\sin(\omega t - \varphi)$ with $\varphi$ the load phase angle. As $R_p$ is much larger than the pressure-coil reactance, $i_2 = (V_m/R_p)\sin\omega t$ in phase with $v$:

$$T_i = \frac{V_mI_m}{R_p}\sin\omega t\,\sin(\omega t - \varphi)\,\frac{dM}{d\theta} = \frac{V_mI_m}{2R_p}\left[\cos\varphi - \cos(2\omega t - \varphi)\right]\frac{dM}{d\theta}$$

The pointer cannot follow the $2\omega$ term; it responds to the **average torque** over one cycle:

$$T_{avg} = \frac{V_mI_m}{2R_p}\cos\varphi\,\frac{dM}{d\theta} = \frac{VI\cos\varphi}{R_p}\,\frac{dM}{d\theta}$$

with $V$ and $I$ the r.m.s. values. Equating to $K\theta$:

$$\boxed{\theta = \frac{1}{KR_p}\,VI\cos\varphi\,\frac{dM}{d\theta} \ \propto\ P = VI\cos\varphi}$$

So the wattmeter reads the **true (active) power** in both d.c. and a.c. circuits. The deflection is proportional to the power if $dM/d\theta$ is constant over the working range, which is why the scale is uniform (nearly linear), with the cramped ends because $dM/d\theta$ varies at the ends of the travel (the instrument is designed so that $dM/d\theta$ is nearly constant for $\pm 45^\circ$).

*Error due to the inductance of the pressure coil.* If the PC has the reactance giving the phase angle $\beta = \tan^{-1}(\omega L_p/R_p)$, the reading $\propto VI\cos\beta\,\cos(\varphi - \beta)$, and the true power is the reading multiplied by the correction factor

$$\frac{\cos\varphi\,\cos\beta}{\cos(\varphi - \beta)}$$

(1 at unity pf; the error is large at low pf, which is compensated by a capacitor across a part of $R_p$ and by low-power-factor wattmeters). **Uses:** the measurement of power from d.c. up to the audio frequencies, the standard of the transfer instrument and the calibration of other wattmeters.

@s 9
**Smart sensor: structural block diagram.** A **smart sensor** is a sensor with an embedded **microprocessor and communication interface** so that it performs signal conditioning, conversion, compensation, diagnostics and communication in one package (IEEE 1451). The blocks, in the order of the signal:

1. **Sensing element (primary transducer):** converts the measurand to an electrical quantity.
2. **Signal conditioning:** amplifier, filter, excitation, offset and bridge circuits.
3. **Multiplexer, sample-and-hold and ADC:** convert to a digital word (an auxiliary sensor measures temperature or supply for compensation).
4. **Microcontroller / DSP (the "smartness"):** calibration, **linearisation**, **temperature and cross-sensitivity compensation**, digital filtering and averaging, scaling to engineering units, range switching, **self-diagnosis, self-calibration and self-validation**, alarm limits, and data storage.
5. **Memory (EEPROM / Flash):** calibration coefficients, the identification data (the transducer electronic data sheet, TEDS), configuration.
6. **Communication interface:** a digital bus to the host: I²C, SPI, RS-485, HART, Foundation Fieldbus, CAN, Profibus or wireless (ZigBee, BLE).
7. **Power supply unit** (regulator, a battery or loop power); an **actuator output** may be included.

```figure caption="Question 9: structural block diagram of a smart sensor."
fig,ax=plt.subplots(figsize=(6.8,2.9)); ax.axis('off'); ax.set_xlim(0,15); ax.set_ylim(0,6)
def bx(x,y,w,h,t,fc='#e0f2fe'):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=INK,lw=1)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=6.8)
bx(0.2,3.2,2.0,1.4,'Measurand\n->  Sensing\nelement','#fde68a'); bx(3.0,3.2,2.0,1.4,'Signal\nconditioning'); bx(5.8,3.2,1.8,1.4,'MUX, S/H,\nADC'); bx(8.4,3.2,3.0,1.4,'Microcontroller / DSP\ncalibration, linearise,\ncompensate, diagnose','#dbeafe'); bx(12.2,3.2,2.6,1.4,'Digital interface\nI2C, SPI, HART,\nwireless','#dcfce7')
bx(5.8,0.8,1.8,1.4,'Temperature\nsensor','#fde68a'); bx(8.4,0.8,3.0,1.4,'EEPROM: calibration,\nTEDS, configuration','#f1f5f9'); bx(12.2,0.8,2.6,1.4,'Power supply /\nregulator','#f1f5f9')
for a,b in (((2.2,3.9),(3.0,3.9)),((5.0,3.9),(5.8,3.9)),((7.6,3.9),(8.4,3.9)),((11.4,3.9),(12.2,3.9)),((6.7,2.2),(6.7,3.2)),((9.9,2.2),(9.9,3.2))): arrow(ax,a,b,None,color=INK)
arrow(ax,(14.8,3.9),(14.99,3.9),None,color=INK); ax.text(13.5,5.0,'to host / network',fontsize=7,ha='center',color=MUTED)
```

@s 10
**Industry 4.0.** Industry 4.0 (the Fourth Industrial Revolution) is the integration of **cyber-physical systems, the Internet of Things (IIoT), cloud and edge computing, big data and AI, robotics and additive manufacturing** into manufacturing and process industries, so that machines, products and people are connected and the factory becomes a **smart, self-optimising and flexible** system with real-time data exchange (after mechanisation, electrification and computer automation).

**Challenges in implementing automation in industrial instrumentation**

1. **High initial investment** (sensors, PLC/DCS, network, software, training) and an uncertain return, especially for small industries.
2. **Cybersecurity and data privacy:** networked controllers (OT) exposed to attack; a need for firewalls, segmentation, authentication and IEC 62443 practices.
3. **Interoperability and legacy equipment:** old analogue (4 to 20 mA) instruments and proprietary protocols (Modbus, Profibus, HART) have to be integrated with the new IIoT/OPC-UA systems; lack of standards.
4. **Shortage of skilled manpower** (instrumentation, networking, data science) and the resistance to change and job-loss fears.
5. **Reliability and real-time requirements:** the latency and the availability of the network, the noise (EMI) and the harsh environment (temperature, dust, vibration), and the need for redundancy and fail-safe design.
6. **Data management:** huge volumes of sensor data to store, clean and analyse; data quality and the calibration drift of the sensors.
7. **Infrastructure:** unstable power supply and weak Internet connectivity, spare-part and maintenance support (especially in Nepal).
8. **Safety, regulatory and standards compliance** and the integration with the existing processes with minimal downtime.
