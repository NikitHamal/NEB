---
file: NEBians-IOE-Past-Paper-Instrumentation-ENEE252-2083-Baishakh.pdf
subject: Instrumentation
level: BE · Year II / Part II
code: ENEE 252
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE Electronics and Communication / Computer (BEI, BCT), Year II / Part II. Full marks 60, pass marks 24. The code is printed as ENEE 252 on the scan.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt All questions · The figures in the margin indicate Full Marks · Assume suitable data if necessary</small>

@q 1
What are the factor consideration while selecting a processor? [[3]]

@q 2
a) Define sensitivity with example. [[2]]

b) Derive the expression for resistance using the ammeter-voltmeter method. Interpret the results of the ammeter-voltmeter method for measuring medium resistance. Discuss the impact of the internal resistance of the ammeter and voltmeter on the measured value of resistance. [[4]]

@q 3
a) A rotary potentiometer has a total resistance of 5 kΩ, a total angular displacement of 300°. If the wiper is at 120° and applied voltage is 10 V, what is the resistance between the wiper and the starting end? Also find output voltage. [[4]]

b) Define a chemical sensor and describe its simple working principle with an example. [[4]]

@q 4
a) What are the operation modes of 8255? Explain their format with suitable example. [[1+4]]

b) Explain the internal architecture of STM32 Cortex M4 single core processor. [[5]]

c) Explain interfacing of DC motor with AT Mega 328P microcontroller along with its circuit diagram and program. [[5]]

@q 5
What are the major considerations while choosing right connectivity in instrumentation system? Explain SPI protocol with communication design of master slave configuration. [[2+4]]

@q 6
Write about the factors we should consider while doing component placement. Explain with relevant diagram how inductive noise coupling mechanism can be minimized. [[1+3]]

@q 7
a) Draw and list out the steps for prototype SDLC. [[3]]

b) Define coupling and cohesion concepts in software engineering. [[3]]

@q 8
Explain the working principle of induction type motor with derivation. [[6]]

@q 9
Explain the importance of cloud in instrumentation system. [[3]]

@q 10
Why are autonomous systems considered more efficient than traditional manual systems in industrial operations? Explain its technical view. [[3]]

<!-- SOLUTIONS -->

@s 1
**Factors in selecting a processor (microprocessor / microcontroller) for an instrumentation system**

1. **Application and processing load:** the required computation (filtering, FFT, PID, floating point) decides between an 8-bit MCU, a 32-bit ARM Cortex-M or a DSP / FPGA.
2. **Word length and data width:** 8, 16 or 32 bit, matched to the ADC resolution and the arithmetic precision.
3. **Speed:** clock frequency, instructions per cycle (MIPS), interrupt latency; must meet the real-time deadline of the control loop.
4. **Memory:** on-chip Flash (program), SRAM (data), EEPROM (calibration constants); the possibility of external memory expansion.
5. **On-chip peripherals:** ADC / DAC resolution and channels, timers, PWM, UART, SPI, I²C, CAN, USB, DMA, comparators, RTC, watchdog. These reduce the external parts.
6. **Power consumption and low-power modes:** crucial for battery-operated and remote sensors.
7. **Cost, size and package;** availability and supply chain, **operating temperature range**, reliability and noise immunity (industrial grade).
8. **Architecture and instruction set** (RISC or CISC, Harvard or von Neumann), **software support:** compilers, IDE, libraries, RTOS support, debugging interface (JTAG / SWD), documentation and community.
9. **I/O voltage levels** (3.3 V or 5 V) compatible with the sensors and actuators, and the number of I/O pins.
10. **Scalability and upgrade path** within the same family; security features (secure boot, crypto).

@s 2
**(a) Sensitivity.** The sensitivity of an instrument or sensor is the ratio of the change in the output signal to the change in the input (measurand) that causes it:

$$S = \frac{\Delta q_o}{\Delta q_i}\quad(\text{slope of the calibration curve})$$

It has the unit of output per unit of input. A larger $S$ means that a small input change gives a large, easily measured output.

*Example:* a type-K thermocouple gives 41 µV for each °C, so $S = 41\ \mu\text{V/}^\circ\text{C}$. An LVDT with 2 V output for 10 mm core movement has $S = 0.2$ V/mm; a strain gauge with gauge factor 2 has $S = \dfrac{\Delta R/R}{\varepsilon} = 2$. The reciprocal $1/S$ is the *inverse sensitivity* (deflection factor).

**(b) Ammeter-voltmeter method for resistance.** The unknown resistance $R$ is found from Ohm's law, $R = V/I$, with a voltmeter and an ammeter. Because both instruments have internal resistance ($R_a$ of the ammeter, $R_v$ of the voltmeter), there are two possible connections.

*Connection 1: voltmeter connected across the resistance only (ammeter measures the sum of the currents).* The ammeter carries $I = I_R + I_v$:

$$\begin{gathered}R_m = \frac{V}{I} = \frac{V}{V/R + V/R_v} = \frac{RR_v}{R + R_v} \\ \text{true } R = \frac{R_m}{1 - R_m/R_v} = \frac{R_m}{1 - R_m/R_v}\end{gathered}$$

The measured value is **less than the true value** ($R_m < R$) because the voltmeter shunts $R$. The relative error is

$$\varepsilon_1 = \frac{R_m - R}{R} = -\frac{R}{R + R_v}\approx -\frac{R}{R_v}$$

It is small when $R \ll R_v$: this connection is suitable for **low resistances**.

*Connection 2: ammeter in series with R, voltmeter across both.* The voltmeter reads the drop across $R$ plus the ammeter:

$$R_m = \frac{V}{I} = R + R_a\ \Rightarrow\ R = R_m - R_a$$

The measured value is **greater than the true value** and the relative error is

$$\varepsilon_2 = \frac{R_m - R}{R} = \frac{R_a}{R}$$

It is small when $R \gg R_a$: this connection is suitable for **high resistances**.

**Medium resistances.** For a medium-value resistance neither approximation is good, so the connection is chosen so that the error is the smaller one. The two errors have equal magnitude when $\dfrac{R_a}{R} = \dfrac{R}{R_v}$, i.e. at the **critical resistance**

$$R_c = \sqrt{R_aR_v}$$

- If $R < R_c$: use connection 1 (voltmeter across the resistor only).
- If $R > R_c$: use connection 2 (ammeter next to the source side, voltmeter across both).
- At $R = R_c$ the error of both is $\approx \sqrt{R_a/R_v}$, the minimum possible with this method.

For the best result the measured values are corrected by the formulas above, which needs the knowledge of $R_a$ and $R_v$.

*Example:* $R_a = 0.5\ \Omega$, $R_v = 10\ \text{k}\Omega$: $R_c = \sqrt{0.5\times10^4} = 70.7\ \Omega$. A resistor of 50 Ω gives $\varepsilon_1 = -0.50\ \%$ and $\varepsilon_2 = +1.0\ \%$, so connection 1 is chosen; a 500 Ω resistor gives $\varepsilon_1 = -4.8\ \%$ and $\varepsilon_2 = +0.1\ \%$, so connection 2.

**Impact of the internal resistances:** a high $R_v$ (ideal $\infty$) and a low $R_a$ (ideal 0) reduce the loading error; any finite value gives a systematic error that is the larger the closer the unknown resistance is to $R_v$ (connection 1) or to $R_a$ (connection 2).

@s 3
**(a) Rotary potentiometer.** The resistance of a linear potentiometer is proportional to the angle of the wiper:

$$R_{w} = R_T\frac{\theta}{\theta_T} = 5000\times\frac{120^\circ}{300^\circ} = \mathbf{2000\ \Omega}\quad(\text{between wiper and the starting end})$$

The remaining resistance, between the wiper and the other end, is $5000 - 2000 = 3000\ \Omega$.

The output voltage of the unloaded potentiometer (divider) is

$$V_o = V_s\frac{R_w}{R_T} = 10\times\frac{2000}{5000} = \mathbf{4\ V}$$

(With a load of resistance $R_L$ the output would drop below 4 V, by the loading error; the result above assumes $R_L \gg R_T$.)

**(b) Chemical sensor.** A chemical sensor is a device that converts **chemical information** (the concentration or presence of an analyte such as a gas, ion, or molecule in a gas or liquid) into a measurable **electrical signal**. It consists of (1) a **receptor** layer that interacts selectively with the analyte and (2) a **transducer** that converts the interaction (a change of mass, charge, potential, conductivity or optical property) into an electrical signal, followed by signal conditioning.

*Working principle with an example, metal-oxide semiconductor (MOS) gas sensor (MQ type):* the sensing element is a tin-dioxide ($\text{SnO}_2$) film, heated to 200 to 400 °C. In clean air, oxygen is adsorbed on the grains and captures conduction electrons, forming $\text{O}^-$ and $\text{O}^{2-}$ and a potential barrier; the film resistance is high. When a reducing gas (CO, LPG, alcohol, methane) is present, it reacts with the adsorbed oxygen and releases electrons back to the film:

$$\text{CO} + \text{O}^- \rightarrow \text{CO}_2 + e^-$$

so the conductivity rises and the resistance $R_s$ falls with the gas concentration $C$: $R_s/R_0 = A\,C^{-\alpha}$. A series load resistor forms a voltage divider, $V_o = V_{cc}R_L/(R_L + R_s)$, which rises with gas concentration and is read by an ADC.

Other examples: the glass **pH electrode** (the potential depends on the H$^+$ activity, Nernst: 59.2 mV/pH at 25 °C); the **electrochemical oxygen cell**; the blood-glucose enzyme (amperometric) sensor.

@s 4
**(a) Operating modes of the 8255 PPI (programmable peripheral interface).** The 8255 has three 8-bit ports (A, B, C) and two groups (Group A: port A and PC7-PC4; Group B: port B and PC3-PC0). It works in two main modes selected by bit D7 of the control word:

1. **I/O mode (D7 = 1)** with three sub-modes:
   - **Mode 0, basic (simple) input/output:** every port is a simple latched output or buffered input, no handshaking; PC upper and lower nibbles are separately programmable.
   - **Mode 1, strobed (handshake) input/output:** ports A and B transfer data with handshaking signals from port C (STB, IBF, OBF, ACK, INTR).
   - **Mode 2, bidirectional bus:** only port A, 8-bit bidirectional with 5 handshake lines from port C (PC3 to PC7); port B in mode 0 or 1.
2. **Bit Set/Reset (BSR) mode (D7 = 0):** individual bits of port C can be set or cleared.

**Control-word format**

| D7 | D6 D5 | D4 | D3 | D2 | D1 | D0 |
|---|---|---|---|---|---|---|
| Mode set flag: 1 = I/O mode | Group A mode: 00 = mode 0, 01 = mode 1, 1x = mode 2 | Port A: 1 = input, 0 = output | Port C upper (PC7-PC4): 1 = input, 0 = output | Group B mode: 0 = mode 0, 1 = mode 1 | Port B: 1 = input, 0 = output | Port C lower (PC3-PC0): 1 = input, 0 = output |

BSR format: D7 = 0, D6-D4 don't care, **D3 D2 D1** = bit number (000 to 111 for PC0 to PC7), **D0** = 1 set, 0 reset.

**Example 1 (I/O mode 0):** port A output, port B input, PC upper output, PC lower input:

$$D_7 \ldots D_0 = 1\ 00\ 0\ 0\ 0\ 1\ 1 = 10000011_2 = \textbf{83H}$$

Program: `MOV AL, 83H` then `OUT CWR, AL`; then `IN AL, PORTB` reads switches and `OUT PORTA, AL` drives LEDs.

**Example 2 (BSR):** set PC3: $0\ xxx\ 011\ 1$ = 07H (reset PC3 = 06H).

**(b) STM32 Cortex-M4 architecture (single core).** The **ARM Cortex-M4** is a 32-bit RISC core (ARMv7E-M, Thumb-2 instruction set) with a **Harvard** bus architecture, a 3-stage pipeline (fetch, decode, execute), and DSP extensions:

- **Core:** 32-bit ALU, 16 registers (R0-R12 general, R13 SP with MSP/PSP, R14 LR, R15 PC), hardware single-cycle 32 × 32 multiplier and a MAC, hardware divider, **SIMD DSP instructions**, and a single-precision **FPU** (in STM32F4 and similar).
- **Memory Protection Unit (MPU)** with 8 regions; **NVIC** (nested vectored interrupt controller) with up to 240 interrupts and 16 priority levels, low-latency (12 cycles); **SysTick** timer; wake-up interrupt controller (WIC).
- **Buses:** I-Code (instruction fetch from Flash), D-Code (data/literals from Flash), and System bus (SRAM and peripherals), joined by a **multilayer AHB bus matrix**; **ART accelerator** with prefetch and cache gives zero-wait-state Flash access up to 168 MHz or more.
- **Memory:** on-chip Flash (up to 1 to 2 MB), SRAM (up to 192 KB, with CCM), backup SRAM, option bytes.
- **DMA controllers** (DMA1/2) offload data transfer between memory and peripherals.
- **Peripherals on APB1/APB2:** GPIO, general-purpose and advanced timers (PWM), 12-bit ADCs (up to 2.4 MSPS), DAC, USART/UART, SPI/I²S, I²C, CAN, USB OTG, SDIO, Ethernet, RTC, watchdogs, CRC and random-number generator.
- **Clock and power:** HSI/HSE oscillators and a PLL (up to 168 MHz or higher), clock-security system, sleep, stop and standby low-power modes.
- **Debug:** SWD/JTAG, ETM trace, breakpoints (FPB) and DWT.

```figure caption="Question 4(b): block diagram of an STM32 (Cortex-M4) microcontroller."
fig,ax=plt.subplots(figsize=(6.8,3.9)); ax.axis('off'); ax.set_xlim(0,14); ax.set_ylim(0,8)
def bx(x,y,w,h,t,fc='#e0f2fe'):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=INK,lw=1)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=6.8)
bx(0.2,5.2,3.6,2.3,'ARM Cortex-M4 core\n3-stage pipeline, ALU, MAC\nDSP/SIMD, FPU\nNVIC, SysTick, MPU','#dbeafe')
bx(0.2,3.4,3.6,1.2,'ETM / SWD / JTAG debug','#f1f5f9')
bx(4.8,6.3,3.0,1.2,'Flash + ART accelerator\n(I-Code, D-Code)','#dcfce7'); bx(4.8,4.6,3.0,1.2,'SRAM / CCM RAM\n(System bus)','#dcfce7')
bx(4.8,2.9,3.0,1.2,'DMA 1 / DMA 2','#fef9c3')
bx(4.4,0.3,3.8,1.6,'AHB bus matrix  (multilayer)','#e2e8f0')
bx(9.4,6.0,4.2,1.6,'APB1 (42 MHz): timers, USART,\nI2C, SPI/I2S, CAN, DAC, RTC','#fde68a'); bx(9.4,3.9,4.2,1.6,'APB2 (84 MHz): ADC1-3, SPI1,\nUSART1/6, TIM1/8, GPIO A-I','#fde68a')
bx(9.4,1.8,4.2,1.5,'Clock tree: HSI/HSE, PLL, RTC osc.\nPower: sleep, stop, standby','#f1f5f9')
for a,b in (((3.8,6.3),(4.8,6.9)),((3.8,5.6),(4.8,5.2)),((3.8,5.4),(4.4,1.4)),((6.3,2.9),(6.3,1.9)),((8.2,1.1),(9.4,2.6)),((7.8,3.2),(9.4,4.5)),((7.8,2.9),(9.4,6.4))):
    arrow(ax,a,b,None,color=MUTED,lw=1.0)
```

**(c) Interfacing a DC motor with ATmega328P.** The microcontroller pins can source only about 20 to 40 mA, but a small DC motor needs 100 mA to several amperes and produces inductive back-emf spikes. The motor is therefore driven through a **power driver**: an **L293D / L298N H-bridge** (or an NPN power transistor / MOSFET with a flyback diode). The speed is controlled by **PWM** on an OC pin (Timer0 on OC0A = PD6), and the direction by the logic levels on two input pins.

**Circuit connections (L293D dual H-bridge):**

- PD6 (OC0A, PWM) to the L293D enable pin EN1,2 (pin 1).
- PD2 to IN1 (pin 2), PD3 to IN2 (pin 7).
- Motor between OUT1 (pin 3) and OUT2 (pin 6). The L293D has built-in clamp diodes (for a discrete transistor use a 1N4007 flyback diode across the motor).
- $V_{CC1}$ (pin 16) = 5 V logic, $V_{CC2}$ (pin 8) = motor supply (e.g. 9 to 12 V); all GND pins to common ground with the ATmega328P GND. A 100 nF capacitor near each supply and a 100 µF capacitor across the motor supply.

```figure caption="Question 4(c): ATmega328P driving a DC motor through an L293D H-bridge with PWM speed control."
fig,ax=plt.subplots(figsize=(6.6,3.3)); ax.axis('off'); ax.set_xlim(0,13); ax.set_ylim(0,6.4)
ax.add_patch(Rectangle((0.3,1.2),3.2,4.2,fc='#dbeafe',ec=INK,lw=1.2)); ax.text(1.9,5.0,'ATmega328P',ha='center',fontsize=8,weight='bold')
ax.add_patch(Rectangle((6.0,1.2),2.8,4.2,fc='#dcfce7',ec=INK,lw=1.2)); ax.text(7.4,5.0,'L293D',ha='center',fontsize=8,weight='bold')
for y,t1,t2 in ((4.0,'PD6 (OC0A, PWM)','EN1,2'),(3.1,'PD2','IN1'),(2.2,'PD3','IN2')):
    ax.plot([3.5,6.0],[y,y],color=INK,lw=1.2); ax.text(3.45,y+0.1,t1,fontsize=6.5,ha='right'); ax.text(6.1,y+0.1,t2,fontsize=6.5)
ax.plot([8.8,10.2],[4.0,4.0],color=INK,lw=1.2); ax.plot([8.8,10.2],[2.2,2.2],color=INK,lw=1.2); ax.plot([10.2,10.2],[4.0,3.7],color=INK); ax.plot([10.2,10.2],[2.2,2.5],color=INK)
ax.add_patch(Circle((10.2,3.1),0.6,fc='white',ec=INK,lw=1.4)); ax.text(10.2,3.1,'M',ha='center',va='center',fontsize=10,weight='bold')
ax.text(8.9,4.1,'OUT1',fontsize=6.5); ax.text(8.9,2.3,'OUT2',fontsize=6.5)
ax.text(7.4,0.9,'+Vm to pin 8,  +5 V to pin 16,  GND common',fontsize=6.5,ha='center',color=MUTED)
ax.text(10.2,1.5,'1N4007 clamp diodes\n(inside L293D)',fontsize=6.5,ha='center',color=MUTED)
```

**Program (avr-gcc, C)** which ramps the speed up, then reverses the direction:

```c
#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>

int main(void)
{
    DDRD |= (1 << PD6) | (1 << PD2) | (1 << PD3);       /* PWM pin and two direction pins as output */
    TCCR0A = (1 << COM0A1) | (1 << WGM01) | (1 << WGM00); /* fast PWM, non-inverting on OC0A (PD6) */
    TCCR0B = (1 << CS01) | (1 << CS00);                  /* prescaler 64: f_pwm = 16 MHz/(64*256) = 976 Hz */

    while (1) {
        PORTD |=  (1 << PD2);  PORTD &= ~(1 << PD3);     /* forward: IN1 = 1, IN2 = 0 */
        for (uint8_t d = 0; d < 255; d++) { OCR0A = d; _delay_ms(10); }  /* duty = OCR0A/256 */
        _delay_ms(1000);
        OCR0A = 0; _delay_ms(500);                        /* stop */
        PORTD &= ~(1 << PD2);  PORTD |=  (1 << PD3);     /* reverse: IN1 = 0, IN2 = 1 */
        OCR0A = 128; _delay_ms(2000);                     /* half speed */
        OCR0A = 0; _delay_ms(500);
    }
}
```

The average motor voltage is $V_{avg} = D\,V_m$ with $D = \text{OCR0A}/256$; $\text{IN1} = \text{IN2}$ brakes the motor.

@s 5
**Considerations in choosing connectivity for an instrumentation system**

1. **Distance and range** (cm for on-board buses, metres for RS-485, kilometres for fieldbus or LoRa).
2. **Data rate and bandwidth** needed by the sensor and the sample rate (kbps for sensors, Mbps for cameras).
3. **Number of nodes, topology** (point-to-point, bus, star, mesh) and the scalability.
4. **Power consumption** (battery life for wireless nodes; BLE, ZigBee, LoRa against Wi-Fi).
5. **Noise immunity and reliability:** differential signalling (RS-485, CAN), shielding, error detection (CRC), robustness in an industrial environment.
6. **Latency and determinism** for real-time control (EtherCAT, CAN, PROFIBUS).
7. **Cost and complexity:** wiring, connectors, protocol stack, licences, the availability of drivers.
8. **Standards and interoperability** (Modbus, HART, OPC-UA, MQTT), compatibility with legacy devices, and **security** (encryption, authentication).
9. **Wired against wireless:** installation cost, mobility, interference, regulatory (ISM band) limits.

**SPI (Serial Peripheral Interface).** A synchronous, full-duplex, serial bus with one **master** and one or more **slaves**, using four lines:

| Line | Direction | Function |
|---|---|---|
| SCLK (SCK) | master to slave | clock generated by the master |
| MOSI | master to slave | master out, slave in: data |
| MISO | slave to master | master in, slave out: data |
| SS / CS (active low) | master to slave | slave select; one line per slave |

**Operation.** Master and slave each contain an 8-bit **shift register**. The master pulls $\overline{SS}$ low, then each SCLK pulse shifts one bit out of the master's register on MOSI into the slave and at the same time one bit out of the slave's register on MISO into the master: after 8 clocks the two registers have **exchanged** their contents (full duplex). The master raises $\overline{SS}$ to end the transfer. Four modes (0 to 3) are defined by clock polarity CPOL and clock phase CPHA (data sampled on the leading or the trailing edge). The rate can be several MHz to tens of MHz, no addressing is needed, and the design is simple, fast and with no start/stop bits; its drawbacks are the number of lines (one extra SS per slave), the lack of acknowledgement and the short distance.

**Master-slave design:** with several slaves, SCLK, MOSI and MISO are shared and each slave has its own $\overline{SS}_n$ from the master; or the slaves can be **daisy chained** (MISO of one to MOSI of the next) with a common SS.

```figure caption="Question 5: SPI master with three slaves; SCLK, MOSI and MISO are shared, each slave has its own select line."
fig,ax=plt.subplots(figsize=(6.6,3.5)); ax.axis('off'); ax.set_xlim(0,13); ax.set_ylim(0,7.4)
ax.add_patch(Rectangle((0.3,1.0),3.0,6.0,fc='#dbeafe',ec=INK,lw=1.2)); ax.text(1.8,6.0,'SPI MASTER\n(microcontroller)',ha='center',va='center',fontsize=7.5,weight='bold')
ax.add_patch(Rectangle((0.7,3.0),2.2,0.6,fc='white',ec=INK)); ax.text(1.8,3.3,'8-bit shift reg.',ha='center',va='center',fontsize=6.5)
ys=(5.4,3.6,1.8)
for k,y in enumerate(ys):
    ax.add_patch(Rectangle((9.0,y-0.55),3.4,1.6,fc='#dcfce7',ec=INK,lw=1.2)); ax.text(10.7,y+0.8,'Slave %d'%(k+1),ha='center',fontsize=7.5,weight='bold')
    ax.add_patch(Rectangle((9.5,y-0.3),2.4,0.5,fc='white',ec=INK)); ax.text(10.7,y-0.05,'shift register',ha='center',va='center',fontsize=6.3)
ax.plot([3.3,7.2],[6.6,6.6],color=INK,lw=1.3); ax.text(3.5,6.7,'SCLK',fontsize=7)
ax.plot([3.3,7.0],[6.2,6.2],color=ACCENT,lw=1.3); ax.text(3.5,6.3,'MOSI',fontsize=7,color=ACCENT)
ax.plot([3.3,6.8],[0.6,0.6],color=SERIES[2],lw=1.3); ax.text(3.5,0.7,'MISO',fontsize=7,color=SERIES[2])
ax.plot([7.2,7.2],[6.6,2.3],color=INK,lw=1.3); ax.plot([7.0,7.0],[6.2,2.05],color=ACCENT,lw=1.3); ax.plot([6.8,6.8],[0.6,5.4],color=SERIES[2],lw=1.3)
for y in ys:
    ax.plot([7.2,9.0],[y+0.5,y+0.5],color=INK,lw=1.0); ax.plot([7.0,9.0],[y+0.25,y+0.25],color=ACCENT,lw=1.0); ax.plot([6.8,9.0],[y,y],color=SERIES[2],lw=1.0)
    for xx,yy in ((7.2,y+0.5),(7.0,y+0.25),(6.8,y)): ax.plot([xx],[yy],'o',color=INK,ms=2.5)
for k,y in enumerate(ys):
    yy=y-0.4
    ax.plot([3.3,9.0],[yy,yy],color=SERIES[3],lw=1.0,ls='--'); ax.text(3.5,yy+0.07,'SS%d (active low)'%(k+1),fontsize=6.3,color=SERIES[3])
```

@s 6
**Factors to consider while placing components (PCB layout)**

1. **Signal flow:** place components in the order of the circuit signal path (input, analogue front end, ADC, processor, output) with short, direct tracks.
2. **Partitioning:** keep **analogue, digital, power and RF** sections separate, each with its own ground area joined at one point (star or a single bridge) so digital return current does not flow through the analogue ground.
3. **Decoupling capacitors** (0.1 µF) as close as possible to the supply pins of each IC; the oscillator/crystal very near the MCU with short tracks and a ground guard.
4. **Sensitive and noisy parts:** keep sensitive inputs (op-amp inputs, sensor traces, references) away from noisy parts (switching regulators, relays, motor drivers, clocks, inductors).
5. **Connectors** on the board edge, and with the related I/O circuits close to them; **thermal** considerations (hot parts spaced out, away from electrolytic capacitors and sensors, with copper for heat sinks).
6. **Orientation** (inductors perpendicular to each other to reduce mutual coupling; ICs in the same direction for assembly), accessible test points, mechanical (mounting holes, height) and manufacturing (DFM, clearance, assembly side) constraints.

**Inductive noise coupling.** A changing current $I_1$ in a noise-source loop produces a magnetic flux that links the loop of the victim circuit and induces a noise voltage

$$\begin{gathered}V_n = M\frac{dI_1}{dt} = \omega MI_1\ (\text{sinusoidal}) \\ M \propto \frac{A_1A_2}{d^3}\cos\theta\end{gathered}$$

so the coupling depends on the mutual inductance $M$ (which depends on the **loop areas $A_1$, $A_2$, the separation $d$ and the orientation**) and on $dI/dt$.

**Minimisation**

1. **Reduce the loop areas**: route the signal and its return path close together (tracks over a solid ground plane, **twisted pair** cable): $A \to 0$ gives $M \to 0$.
2. **Increase the separation** $d$ between the noise source and the victim circuit (M falls as $1/d^3$).
3. **Orient the loops at right angles** ($\cos\theta = 0$) or use a **twisted pair**, in which the induced emfs in adjacent half-turns cancel.
4. **Reduce $dI/dt$**: slow down switching edges (series resistor, snubber), filter the noisy lines, use low-di/dt drivers.
5. **Magnetic shielding** with high-permeability material (mu-metal) and ground planes; **balanced differential** transmission with common-mode rejection.

```figure caption="Question 6: inductive coupling between a noise loop and a victim loop. A small, closely spaced loop pair with a ground plane (right) reduces the coupled flux."
fig,axs=plt.subplots(1,2,figsize=(6.8,2.6))
for ax,(t,A,d) in zip(axs,(('large loops, close: strong coupling',(2.2,1.6),0.6),('small loops, spaced, orthogonal: weak',(1.0,0.7),2.2))):
    ax.axis('off'); ax.set_xlim(-0.2,6.4); ax.set_ylim(-0.3,3.2); ax.set_title(t,fontsize=7.5)
    w,h=A
    ax.add_patch(Rectangle((0.2,1.5-h/2),w,h,fc='none',ec=ACCENT,lw=1.6)); ax.text(0.2+w/2,1.5,'$I_1$ noise',ha='center',fontsize=7,color=ACCENT)
    x2=0.2+w+d
    ax.add_patch(Rectangle((x2,1.5-h/2),w,h,fc='none',ec=INK,lw=1.6)); ax.text(x2+w/2,1.5,'$V_n$ victim',ha='center',fontsize=7)
    for k in range(3): ax.add_patch(Arc((0.2+w+d/2,1.5),d*0.8+0.2*k,0.6+0.5*k,theta1=0,theta2=360,color=MUTED,lw=0.6,ls=':'))
    ax.text(0.2+w+d/2,0.3,'$M = k\\sqrt{L_1L_2}$',ha='center',fontsize=7.5)
```

@s 7
**(a) Prototype SDLC model.** The prototyping model builds a working model (prototype) of the system quickly, lets the user evaluate it and refines the requirements through repeated iterations until the user is satisfied, then the final system is engineered.

**Steps**

1. **Requirement gathering (initial, rough requirements)** with the user.
2. **Quick design:** a simple design of the visible parts (screens, I/O, user interface), not the details.
3. **Build the prototype:** a small working model using quick tools (throw-away or evolutionary).
4. **User evaluation:** the customer uses the prototype and gives feedback.
5. **Refinement:** requirements and the prototype are revised; steps 2 to 4 repeat until the prototype is accepted.
6. **Engineer the final product:** full design, implementation (coding) and **testing**.
7. **Deployment and maintenance.**

```figure caption="Question 7(a): the prototype software development life cycle."
fig,ax=plt.subplots(figsize=(6.8,2.6)); ax.axis('off'); ax.set_xlim(0,14); ax.set_ylim(0,5)
def bx(x,y,w,h,t,fc='#e0f2fe'):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=INK,lw=1)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=7)
bx(0.2,2.0,2.1,1.2,'Requirements\ngathering'); bx(3.0,2.0,2.1,1.2,'Quick design'); bx(5.8,2.0,2.1,1.2,'Build\nprototype'); bx(8.6,2.0,2.1,1.2,'User\nevaluation','#fde68a')
bx(11.4,2.0,2.4,1.2,'Final design,\ncoding, test,\nmaintenance','#dcfce7')
for a,b in (((2.3,2.6),(3.0,2.6)),((5.1,2.6),(5.8,2.6)),((7.9,2.6),(8.6,2.6)),((10.7,2.6),(11.4,2.6))): arrow(ax,a,b,None,color=INK)
ax.plot([9.65,9.65,4.05,4.05],[2.0,0.9,0.9,2.0],color=ACCENT,lw=1.3); arrow(ax,(4.05,1.5),(4.05,2.0),None,color=ACCENT)
ax.text(6.9,0.55,'not accepted: refine requirements and prototype (loop)',fontsize=7,ha='center',color=ACCENT); ax.text(11.0,3.35,'accepted',fontsize=7,ha='center')
```

**(b) Coupling and cohesion**

- **Coupling** is the degree of **interdependence between modules**: how much one module relies on the internals of another. *Low (loose) coupling* is desirable: a change in one module does not ripple into others, so the modules are easy to test, reuse and maintain.
- **Cohesion** is the degree to which the **elements inside one module belong together** and perform a single, well-defined task. *High cohesion* is desirable: the module is understandable, reliable and reusable.

| | Types (from worst to best) |
|---|---|
| **Coupling** | Content (one module modifies another's data or code), common (shared global data), external, control (passes a flag that controls the other's logic), stamp (shares a whole data structure), **data** (only the needed parameters; best) |
| **Cohesion** | Coincidental (unrelated tasks), logical, temporal, procedural, communicational, sequential, **functional** (one task only; best) |

*Good design = low coupling and high cohesion.* For instrumentation firmware, a module `read_adc()` that only samples the ADC (functionally cohesive) and passes a plain integer to `filter()` (data coupling) is better than one routine that reads the ADC, filters it, prints it and drives the relay using global variables.

@s 8
**Induction motor: working principle.**

1. A balanced three-phase supply in the stator winding produces a **rotating magnetic field** of constant magnitude $\Phi_m$ rotating at the synchronous speed $N_s = \dfrac{120f}{P}$ rpm ($\omega_s = 2\pi N_s/60$).
2. This field cuts the stationary rotor conductors, inducing an emf in them (Faraday's law). The rotor is short-circuited (squirrel cage), so rotor currents flow.
3. By **Lenz's law** the rotor currents oppose the cause (the relative motion of the field and rotor), so a torque (Lorentz force $F = BIl$ on the rotor conductors) drags the rotor in the **direction of the field**.
4. The rotor can never reach $N_s$: at $N = N_s$ there would be no relative motion, no emf, no current and no torque. The speed $N < N_s$, and the relative speed is expressed by the slip

$$s = \frac{N_s - N}{N_s}$$

**Derivation of the torque equation.**

At standstill the rotor emf per phase is $E_2$ at frequency $f$ and the rotor reactance is $X_2$. At slip $s$:

$$\begin{gathered}f_2 = sf \\ E_{2s} = sE_2 \\ X_{2s} = sX_2\end{gathered}$$

Rotor current per phase and its power factor:

$$\begin{gathered}I_2 = \frac{sE_2}{\sqrt{R_2^2 + (sX_2)^2}} \\ \cos\varphi_2 = \frac{R_2}{\sqrt{R_2^2 + (sX_2)^2}}\end{gathered}$$

The torque is proportional to the flux and to the active component of the rotor current: $T \propto \Phi I_2\cos\varphi_2$. Using powers instead (exact): the **air-gap power** transferred from the stator to the rotor is $P_g = 3I_2^2R_2/s$ of which the fraction $s$ is lost as rotor copper loss ($3I_2^2R_2$) and the fraction $(1-s)$ becomes mechanical power. Since $P_g = T\omega_s$:

$$T = \frac{P_g}{\omega_s} = \frac{3}{\omega_s}\cdot\frac{I_2^2R_2}{s}$$

Substituting $I_2$:

$$\boxed{T = \frac{3}{\omega_s}\cdot\frac{sE_2^2R_2}{R_2^2 + (sX_2)^2}}$$

**Results**

- *Starting torque* ($s = 1$): $T_{st} = \dfrac{3}{\omega_s}\dfrac{E_2^2R_2}{R_2^2 + X_2^2}$; it rises with $R_2$ (rotor-resistance starter for the slip-ring motor).
- *Maximum (breakdown) torque:* $dT/ds = 0 \Rightarrow s_m = \dfrac{R_2}{X_2}$,

$$T_{max} = \frac{3E_2^2}{2\omega_sX_2}$$

independent of $R_2$, but the slip at which it occurs, $s_m$, is proportional to $R_2$.
- For small slip ($sX_2 \ll R_2$), $T \approx \dfrac{3E_2^2}{\omega_sR_2}\,s \propto s$, a straight line (the stable operating region, near-constant speed); $T \propto V^2$ since $E_2 \propto V$.

```figure caption="Question 8: torque-slip characteristic of a three-phase induction motor for rotor resistance R_2 and 3R_2; the motoring region is 0 < s < 1."
fig,ax=plt.subplots(figsize=(5.8,3.3))
s=np.linspace(0.001,1.2,500); X2=1.0
for R,c,l in ((0.2,INK,'$R_2$ (cage)'),(0.6,ACCENT,'$3R_2$ (added to slip ring)')):
    ax.plot(s,2*s*R/(R**2+(s*X2)**2),color=c,lw=1.8,label=l)
ax.axvline(0.2,color=GRID,ls=':'); ax.text(0.205,0.02,'$s_m=R_2/X_2$',fontsize=7)
ax.set_xlim(0,1.2); ax.set_ylim(0,1.3); ax.set_xlabel('slip $s$   (1 = standstill, 0 = synchronous speed)'); ax.set_ylabel('torque (pu)'); ax.legend(fontsize=7,loc='upper right')
ax.text(0.5,0.12,'motoring region (stable: 0 < s < s$_m$)',fontsize=7,color=MUTED)
```

@s 9
**Importance of the cloud in instrumentation systems.** In a modern (IIoT) instrumentation system the field instruments (sensors, transmitters, PLCs, smart meters) send their measurements through a gateway (MQTT / HTTP / OPC-UA) to a **cloud platform** (AWS IoT, Azure IoT, Google Cloud, ThingsBoard), which gives the following benefits:

1. **Remote monitoring and control:** real-time dashboards and mobile apps for plants that are geographically distributed (hydropower stations, substations, water-supply schemes); remote set-points and commands.
2. **Scalable storage:** large volumes of time-series data are logged cheaply and for a long time (historian) with no local storage limit.
3. **Analytics, AI and machine learning:** trend analysis, anomaly detection and **predictive maintenance** (vibration, temperature) reduce unplanned downtime.
4. **Lower cost:** pay-as-you-go, no on-site servers, central updates.
5. **Remote configuration and OTA firmware update** and calibration management of thousands of devices.
6. **Alarms and notification** (SMS, e-mail), reporting, integration with ERP/SCADA, multi-user access, data sharing.
7. **Availability and backup**, redundancy and security (encryption, authentication, access control).

Limitations to be managed: latency (so fast control loops stay at the edge), connectivity dependence, data security and privacy.

```figure caption="Question 9: cloud-connected instrumentation: field devices, edge gateway, cloud and users."
fig,ax=plt.subplots(figsize=(6.8,2.4)); ax.axis('off'); ax.set_xlim(0,14); ax.set_ylim(0,4.4)
def bx(x,y,w,h,t,fc='#e0f2fe'):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=INK,lw=1)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=7)
bx(0.2,1.4,2.4,1.6,'Sensors /\ntransmitters\nactuators'); bx(3.4,1.4,2.4,1.6,'Edge gateway\n(MCU, PLC)\nlocal control','#fef9c3')
ax.add_patch(Ellipse((8.6,2.2),3.6,2.4,fc='#dbeafe',ec=INK,lw=1.2)); ax.text(8.6,2.2,'CLOUD\nstorage, analytics,\nAI, alarms',ha='center',va='center',fontsize=7.2)
bx(11.2,2.7,2.6,1.2,'Dashboard / mobile app','#dcfce7'); bx(11.2,0.5,2.6,1.2,'ERP / SCADA / OTA\nupdates','#dcfce7')
for a,b in (((2.6,2.2),(3.4,2.2)),((5.8,2.2),(6.8,2.2)),((10.4,2.6),(11.2,3.3)),((10.4,1.8),(11.2,1.1))): arrow(ax,a,b,None,color=INK)
ax.text(6.3,2.45,'MQTT /\nHTTP',fontsize=6.2,ha='center')
```

@s 10
**Why autonomous systems are more efficient than manual operation.** An autonomous system senses its environment, makes decisions with embedded control or AI and acts on the process **without continuous human intervention**. Compared with manual operation they:

1. **Operate continuously (24 × 7)** with no fatigue, breaks or shift changes, which raises the throughput and the equipment utilisation.
2. Give **consistent quality and precision:** a closed loop repeats the same set-point to within the sensor accuracy (human error and variability are removed).
3. **React faster:** millisecond sensing and control instead of a human response time of seconds, so disturbances are rejected before they affect the product; faster fault detection.
4. **Optimise the process** with data: the controllers (PID, MPC, ML) minimise energy, material and waste (typically 10 to 30 % energy saving in HVAC, pumping and kilns).
5. **Improve safety** by taking people out of hazardous environments (high voltage, chemicals, heat) and by built-in interlocks.
6. **Lower operating cost** in the long run (labour, scrap, downtime) and allow **predictive maintenance** from the continuous condition data.
7. Give complete **traceability and logging** of the data for audit and improvement.

**Technical view:** the system is a closed **sense, decide, act** loop:

- **Sensing layer:** smart sensors and vision, LiDAR, encoders measure the process variables.
- **Processing / decision layer:** a PLC, microcontroller, industrial PC or edge-AI unit runs the control algorithms (PID, state machine, path planning, ML inference) in real time.
- **Actuation layer:** drives, valves, motors, robots and AGVs carry out the commands; **feedback** continuously corrects the error $e = r - y$.
- **Communication layer:** industrial networks (Modbus, CAN, EtherCAT, OPC-UA, 5G) link the units to SCADA and the cloud.
- **Supervisory layer:** the exceptions, safety (SIL-rated interlocks) and human override.

*Example:* an automated bottling line with vision inspection and AGVs can run at constant speed with a rejection rate below 0.1 %, while a manual line varies with the operator.
