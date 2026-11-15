---
file: NEBians-IOE-Past-Paper-Data-Communication-ENCT253-2082-Bhadra.pdf
subject: Data Communication
level: BE · Year II / Part II
code: ENCT 253
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Using suitable generic real-world examples of digital communication systems, compare the functioning of half- and full-duplex modes. [[5]]

@q 2
a) With suitable examples, explain how time invariance of a system is checked. [[5]]

b) Plot the magnitude and phase spectrums of: $x(t) = 6 - 8\sin(2\pi 160t + 30^\circ) - 6\cos(\pi 160t - 50^\circ) + 2\sin(300\pi t + 120^\circ)$. [[4]]

@q 3
a) Compare coaxial cable, twisted pair, and optical fiber based on bandwidth, cost, and use case. [[2]]

b) Encode "I'm 100% OK." using weighted Huffman Encoder, and find the transmission efficiency. [[5+1]]

c) Determine and correct the error bit in the even parity received Hamming codeword of 1110011. [[5]]

@q 4
a) Draw the waveform for the bit sequence 1000000000101 using each one suitable unipolar, polar and bipolar encoders. [[6]]

b) Compare AM and FM with basic mathematical formulations and signal diagrams. [[7]]

c) Describe PCM with a block diagram. [[3]]

@q 5
a) Compare digital and analog hierarchies with detailed block diagram showing number of channels and data-rate. [[4]]

b) Demonstrate the operation of CDMA for 8 users among whom four users are sending bit 1, two users are sending bit 0 and remaining two are silent. [[5]]

@q 6
Write short notes on (Any Two): [[2×4]]

a) Evolution of mobile communication technologies from 1G to 5G

b) CRC-4

c) LAN vs WAN

d) FHSS and DSSS

<!-- SOLUTIONS -->

@s 1
**Half duplex and full duplex.** In **half-duplex** communication both stations can transmit and receive, but only **one at a time** over a single shared channel; the stations take turns (push-to-talk). In **full-duplex** communication both stations transmit and receive **simultaneously**, which needs two channels (two frequencies, two wire pairs, two time slots, or echo cancellation).

{{FIG_both}}

| Basis | Half duplex | Full duplex |
|---|---|---|
| Direction of flow | both directions, but alternately | both directions at the same time |
| Channels | one channel shared by the two directions | two channels (or one split by frequency / time) |
| Transmit and receive | one active at a time; a switch (turn-around) is needed | both active together |
| Efficiency | lower, turn-around time is lost | higher, almost twice the throughput of half duplex |
| Cost and complexity | simple, cheap | more complex (extra channel or filters, echo cancellers) |
| Real-world example | walkie-talkie / two-way radio (push to talk), CB radio, old Ethernet hubs (CSMA/CD) | telephone and mobile call, VoIP, video conference, switched full-duplex Ethernet |
| Collision | possible if both talk together | none (separate paths) |

*Examples in more detail.* A **walkie-talkie** (digital two-way radio) has a push-to-talk button: while it is pressed the microphone, ADC, codec and modulator send the voice on the shared channel and the receiver is muted; when it is released the set listens; only one person talks at a time. A **mobile (digital) call** runs a transmit chain (microphone → ADC and codec → channel encoder → modulator) on the uplink frequency and a receive chain (demodulator → channel decoder → DAC → speaker) on the downlink frequency, both working together, so the two persons can talk and hear at the same time.

@s 2
**(a) Checking time invariance.** A system $y(t) = T[x(t)]$ is **time-invariant** if a time shift of the input only shifts the output by the same amount: if $x(t) \to y(t)$ then $x(t - t_0) \to y(t - t_0)$ for every $t_0$.

*Procedure:* (1) delay the **input** by $t_0$ and find the output $y_1(t) = T[x(t - t_0)]$; (2) delay the **output** by $t_0$: $y_2(t) = y(t - t_0)$ (replace $t$ by $t - t_0$ in the whole output expression, including the explicit $t$); (3) if $y_1(t) = y_2(t)$ for all $t$ the system is time-invariant, otherwise time-variant.

| System | $T[x(t - t_0)]$ | $y(t - t_0)$ | Result |
|---|---|---|---|
| $y = 3x(t)$ | $3x(t - t_0)$ | $3x(t - t_0)$ | equal: **time-invariant** |
| $y = x(t) + x(t-1)$ | $x(t - t_0) + x(t - t_0 - 1)$ | $x(t - t_0) + x(t - t_0 - 1)$ | equal: **time-invariant** |
| $y = \dfrac{dx}{dt}$ | $x'(t - t_0)$ | $x'(t - t_0)$ | equal: **time-invariant** |
| $y = t\,x(t)$ | $t\,x(t - t_0)$ | $(t - t_0)\,x(t - t_0)$ | different: **time-variant** |
| $y = x(2t)$ | $x(2t - t_0)$ | $x(2(t - t_0)) = x(2t - 2t_0)$ | different: **time-variant** (compression) |
| $y = x(-t)$ | $x(-t - t_0)$ | $x(-(t - t_0)) = x(-t + t_0)$ | different: **time-variant** |
| $y = \sin\bigl(x(t)\bigr)$ | $\sin x(t - t_0)$ | $\sin x(t - t_0)$ | equal: **time-invariant** (non-linear but TI) |

*Numerical check for $y = t\,x(t)$:* let $x(t) = u(t)$ (unit step) and $t_0 = 2$. Delaying the input gives $t\,u(t - 2)$, which at $t = 3$ is $3$; delaying the output gives $(t - 2)\,u(t - 2)$, which at $t = 3$ is $1$. They differ, so the system is time-variant. In communication terms, a time-invariant channel (a fixed cable) has the same response at any time, but a fading mobile channel is time-variant.

**(b) Spectra of $x(t)$.** First convert every term to a **cosine with positive amplitude**, using $-\sin\theta = \cos(\theta + 90^\circ)$, $\sin\theta = \cos(\theta - 90^\circ)$ and $-\cos\theta = \cos(\theta + 180^\circ)$; and read the frequencies from the angular frequencies ($\omega = 2\pi f$):

| Term | Angular frequency | $f$ | Cosine form | Amplitude $A$ | Phase $\phi$ |
|---|---|---|---|---|---|
| 6 | 0 | 0 (DC) | $6$ | 6 | $0^\circ$ |
| $-6\cos(160\pi t - 50^\circ)$ | $160\pi$ | 80 Hz | $6\cos(160\pi t + 130^\circ)$ | 6 | $+130^\circ$ |
| $2\sin(300\pi t + 120^\circ)$ | $300\pi$ | 150 Hz | $2\cos(300\pi t + 30^\circ)$ | 2 | $+30^\circ$ |
| $-8\sin(2\pi\,160\,t + 30^\circ)$ | $320\pi$ | 160 Hz | $8\cos(320\pi t + 120^\circ)$ | 8 | $+120^\circ$ |

(The first sinusoid has the argument $2\pi\,160\,t$, so it is at 160 Hz, whereas the cosine term has $\pi\,160\,t$, which is only 80 Hz.) So

$$x(t) = 6 + 6\cos(2\pi\,80\,t + 130^\circ) + 2\cos(2\pi\,150\,t + 30^\circ) + 8\cos(2\pi\,160\,t + 120^\circ).$$

The **single-sided** spectrum is the amplitude $A_k$ and phase $\phi_k$ at $f_k \ge 0$. In the **two-sided** (exponential) form each cosine gives two lines, $\tfrac{A}{2}e^{\pm j\phi}$ at $\pm f$, and the DC term stays 6:

| $f$ (Hz) | $-160$ | $-150$ | $-80$ | 0 | 80 | 150 | 160 |
|---|---|---|---|---|---|---|---|
| $\lvert X \rvert$ (two-sided) | 4 | 1 | 3 | 6 | 3 | 1 | 4 |
| $\angle X$ | $-120^\circ$ | $-30^\circ$ | $-130^\circ$ | $0^\circ$ | $130^\circ$ | $30^\circ$ | $120^\circ$ |

{{FIG_spec}}

The magnitude spectrum is even and the phase spectrum is odd (as for any real signal); the plot on the left shows the single-sided amplitudes 6, 6, 2, 8 at 0, 80, 150, 160 Hz. The line positions, amplitudes and phases were confirmed with an FFT of the sampled signal.

@s 3
**(a) Transmission media.**

| Basis | Twisted pair (UTP, Cat 5e/6) | Coaxial cable | Optical fiber |
|---|---|---|---|
| Bandwidth / data rate | low: about 100 Mbit/s to 10 Gbit/s over 100 m | medium: up to about 1 GHz | very high: tens of THz, 10 Gbit/s to Tbit/s |
| Cost | cheapest | medium | highest, falling |
| Quality | sensitive to noise and crosstalk | shielded, better immunity | immune to EMI, 0.2 dB/km loss |
| Use case | telephone, Ethernet LAN to the desk | cable TV, broadband, antenna feeders | backbone, long haul, FTTH, undersea |

**(b) Weighted Huffman coding of "I'm 100% OK."** The message has $N = {{H_N}}$ symbols (letters, apostrophe, spaces, digits, percent sign and full stop). *Algorithm:* list the symbols with their weights (counts); repeatedly **merge the two smallest weights** into a node whose weight is their sum (label the branches 0 and 1) until one node (the root, weight {{H_N}}) remains; read each code from the root down to its symbol.

| Step | Smaller weight | Next smaller weight | New node |
|---|---|---|---|
{{HUFF_STEPS}}

(`␣` is the space; ties are broken in order of appearance, and a different tie order gives other codes with the same lengths in total.)

{{HUFF_TABLE}}

*Encoded message:*

`{{HUFF_ENC}}`

Total = {{H_BITS}} bits against {{H_ASCII}} bits in 8-bit ASCII.

*Entropy* $H = -\sum p_i\log_2 p_i$ is {{H_H}} bit/symbol; *average length* $\bar L = \sum p_i l_i$ is {{H_L}} bit/symbol ({{H_BITS}}/{{H_N}}).

$$\eta = \frac{H}{\bar L}\times 100\% = \frac{{{H_H}}}{{{H_L}}}\times 100\% = {{H_EFF}}\%$$

**(c) Hamming code error correction (even parity).** A 7-bit Hamming code has the parity bits at positions 1, 2, 4 (powers of 2) and data bits at 3, 5, 6, 7. The received word is $1110011$:

| Position | 1 ($p_1$) | 2 ($p_2$) | 3 ($d_3$) | 4 ($p_4$) | 5 ($d_5$) | 6 ($d_6$) | 7 ($d_7$) |
|---|---|---|---|---|---|---|---|
| Bit | 1 | 1 | 1 | 0 | 0 | 1 | 1 |

Each parity bit covers the positions whose binary index contains its weight; the check must give an **even** number of 1s:

| Check | Positions covered | Bits | Number of 1s | Check bit |
|---|---|---|---|---|
| $c_1$ | 1, 3, 5, 7 | 1, 1, 0, 1 | 3 (odd) | **1** (error) |
| $c_2$ | 2, 3, 6, 7 | 1, 1, 1, 1 | 4 (even) | 0 |
| $c_4$ | 4, 5, 6, 7 | 0, 0, 1, 1 | 2 (even) | 0 |

The syndrome (error position) is $c_4c_2c_1 = 001_2 = 1$, so **bit 1 ($p_1$) is in error**. Correct it by inverting bit 1: $1 \to 0$, giving the corrected codeword

$$0110011$$

(re-check: $p_1$ covers 0, 1, 0, 1 = even, $p_2$ covers 1, 1, 1, 1 = even, $p_4$ covers 0, 0, 1, 1 = even; all checks pass). The data bits $d_3 d_5 d_6 d_7 = 1011$ are unaffected, because the error was in a parity bit.

@s 4
**(a) Line codes for 1000000000101.** The sequence has a long run of **nine 0s**. Suitable encoders: **unipolar NRZ** (1 = +V, 0 = 0 V), **polar NRZ-L** (1 = +V, 0 = −V) and **Manchester** (a mid-bit transition: 1 = high-to-low, 0 = low-to-high), and **bipolar AMI** (0 = 0 V, 1s alternately +V and −V). Because AMI loses synchronisation in a long run of zeros, **B8ZS** (used with T1) is also shown: eight zeros are replaced by $000VB0VB$, where V is a *violation* (same polarity as the previous pulse) and B a normal bipolar pulse.

{{FIG_lineB}}

| Bit | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Unipolar NRZ | + | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | + | 0 | + |
| Polar NRZ-L | + | − | − | − | − | − | − | − | − | − | + | − | + |
| Bipolar AMI | + | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | − | 0 | + |
| Bipolar B8ZS | + | 0 | 0 | 0 | + | − | 0 | − | + | 0 | − | 0 | + |

*B8ZS:* the last pulse before the zeros is +, so the substitution is $000\,{+}{-}\,0\,{-}{+}$ (V = + has the same polarity as the previous pulse, B = −, then V = −, B = +); the ninth zero stays 0, and the next 1 must follow the alternation from the last B (+), so it is −. The receiver recognises the two violations and restores the zeros.

**(b) AM and FM.** Let the message be $m(t) = A_m\cos 2\pi f_m t$ and the carrier $c(t) = A_c\cos 2\pi f_c t$.

| Basis | Amplitude modulation (AM) | Frequency modulation (FM) |
|---|---|---|
| What varies | the carrier **amplitude** | the carrier **instantaneous frequency** |
| Equation | $s(t) = A_c[1 + \mu\cos 2\pi f_m t]\cos 2\pi f_c t$ | $s(t) = A_c\cos\bigl[2\pi f_c t + \beta\sin 2\pi f_m t\bigr]$, $f_i = f_c + k_f A_m\cos 2\pi f_m t$ |
| Modulation index | $\mu = A_m/A_c \le 1$ | $\beta = \Delta f/f_m = k_f A_m/f_m$ ($\Delta f$ = peak frequency deviation) |
| Spectrum | carrier + two sidebands $f_c \pm f_m$ | carrier + infinite sidebands at $f_c \pm n f_m$ with amplitudes $A_c J_n(\beta)$ |
| Bandwidth | $2f_m$ | Carson's rule: $B \approx 2(\Delta f + f_m) = 2f_m(\beta + 1)$ |
| Power | $P_t = P_c(1 + \mu^2/2)$, varies with the message | $P_t = A_c^2/2$, **constant** (independent of $\beta$) |
| Noise immunity | poor (noise changes the amplitude) | good (a limiter removes amplitude noise; FM improvement $\propto \beta^2$) |
| Efficiency | at most 33 % useful (sideband) power | all the power is useful |
| Circuit | simple (a diode detector) | more complex (VCO, discriminator, PLL) |
| Use | medium-wave radio, aircraft band | FM broadcast (88 to 108 MHz, $\Delta f$ = 75 kHz), TV sound, two-way radio |

{{FIG_amfm}}

*Numerical example (FM broadcast):* $\Delta f = 75$ kHz, $f_m = 15$ kHz: $\beta = 5$ and $B = 2(75 + 15) = 180$ kHz (the 200 kHz channel), compared with 30 kHz for AM with the same audio.

**(c) PCM (pulse code modulation).** PCM converts an analog signal into a digital bit stream in three steps: **sampling, quantizing and encoding**.

{{FIG_pcm}}

1. **Low-pass filter:** limits the signal to $f_m$ to prevent aliasing (for voice 3.4 kHz).
2. **Sampling:** at $f_s \ge 2f_m$ (Nyquist; 8 kHz for voice) gives a pulse-amplitude-modulated (PAM) signal.
3. **Quantizing:** each sample is rounded to the nearest of $L = 2^n$ levels (step $\Delta = V_{pp}/L$); the error ($\le \Delta/2$) is the quantization noise, with $\mathrm{SNR} \approx 6.02\,n + 1.76$ dB. (Non-uniform companding, A-law or μ-law, is used for speech.)
4. **Encoding:** each level is given an $n$-bit binary code word; the series of code words is the PCM output, with bit rate $R_b = n f_s$ (for voice $8 \times 8000 = 64$ kbit/s).

*Receiver:* regenerative repeaters clean the pulses, a decoder (DAC) rebuilds the samples and a low-pass filter restores the analog signal. In the example of the figure $n = 3$, $L = 8$ and the eight samples are coded $100,\ 110,\ 111,\ 110,\ 100,\ 001,\ 000,\ 001$ (the sine centred at 3.5).

@s 5
**(a) Digital and analog hierarchies.**

{{FIG_hier}}

*Digital hierarchy (TDM).* A voice channel (8 kHz × 8 bit) is 64 kbit/s (DS0). The higher levels time-multiplex the lower ones and add framing and stuffing bits:

| Level | Made of | Channels | Data rate | Calculation |
|---|---|---|---|---|
| DS1 (T1) | 24 DS0 | 24 | 1.544 Mbit/s | $24 \times 64 = 1.536$ + 8 kbit/s framing |
| DS2 (T2) | 4 DS1 | 96 | 6.312 Mbit/s | $4 \times 1.544 = 6.176$ + stuffing and framing |
| DS3 (T3) | 7 DS2 | 672 | 44.736 Mbit/s | $7 \times 6.312 = 44.184$ + overhead |
| DS4 (T4) | 6 DS3 | 4032 | 274.176 Mbit/s | $6 \times 44.736 = 268.416$ + overhead |

European E-carrier: E1 30 channels (2.048 Mbit/s), E2 120 (8.448 Mbit/s), E3 480 (34.368 Mbit/s), E4 1920 (139.264 Mbit/s), E5 7680 (565.148 Mbit/s).

*Analog hierarchy (FDM)* of 4 kHz voice channels:

| Level | Made of | Channels | Bandwidth | Band |
|---|---|---|---|---|
| Group | 12 voice channels | 12 | 48 kHz | 60 to 108 kHz |
| Supergroup | 5 groups | 60 | 240 kHz | 312 to 552 kHz |
| Mastergroup | 10 supergroups | 600 | 2.52 MHz | 564 to 3084 kHz |
| Jumbogroup | 6 mastergroups | 3600 | 16.984 MHz | |

| Digital (TDM) | Analog (FDM) |
|---|---|
| channels share the link in **time** slots | channels share the link in **frequency** bands |
| regenerated at repeaters, noise does not accumulate | noise accumulates in the amplifiers |
| rate in bit/s | bandwidth in Hz |
| needs synchronisation and framing | needs guard bands and many carriers |

**(b) CDMA for 8 users.** Every user has a unique orthogonal **Walsh code** of 8 chips and all users transmit together in the same band. Bit 1 is sent as $+1$ times the code, bit 0 as $-1$ times the code, a silent user sends 0. Users 1 to 4 send bit 1, users 5 and 6 send bit 0, users 7 and 8 are silent.

{{CDMA_B.0}}

*Transmission* (each user's data times its code, then the channel adds them chip by chip):

{{CDMA_B.1}}

*Reception* (inner product of the channel chips with the user's code, divided by 8; the codes are orthogonal, $c_i\cdot c_j = 0$ for $i \ne j$, so the other users cancel):

{{CDMA_B.2}}

Users 1 to 4 decode 1, users 5 and 6 decode 0 and users 7, 8 get 0 (silent): every user's data are recovered exactly although all signals were sent at the same time in the same band.

@s 6
**(a) Evolution of mobile communication, 1G to 5G.**

| Generation | Period | Technology | Data rate | Features |
|---|---|---|---|---|
| 1G | 1980s | analog, FDMA (AMPS, NMT) | 2.4 kbit/s | voice only, poor security and capacity |
| 2G | 1990s | digital, TDMA / CDMA (GSM, IS-95) | 9.6 to 64 kbit/s (GPRS 114, EDGE 384) | digital voice, SMS, encryption, roaming |
| 3G | 2000s | WCDMA, CDMA2000 (UMTS, HSPA) | 384 kbit/s to 42 Mbit/s | mobile internet, video calls, packet data |
| 4G | 2010s | OFDMA / SC-FDMA, MIMO, all-IP (LTE, LTE-A) | 100 Mbit/s to 1 Gbit/s | HD video, VoLTE, latency about 50 ms |
| 5G | 2020s | OFDM, massive MIMO, mmWave (NR) | up to 10 to 20 Gbit/s | latency about 1 ms, 1 million devices per km², eMBB, URLLC, mMTC, network slicing, IoT |

**(b) CRC-4.** The cyclic redundancy check appends $r = 4$ check bits to the data. The data bits are treated as a polynomial; $r$ zeros are appended; the result is divided (modulo-2, with XOR) by the **generator polynomial** $G(x) = x^4 + x + 1$ (CRC-4, bits $10011$); the 4-bit remainder is the CRC and replaces the appended zeros. The receiver divides the whole received word by $G$: a remainder 0 means no error is detected.

*Example.* Data $1101011011$; generator $10011$. Dividend $1101011011\,0000$:

| XOR step | Current 5 bits | After XOR with 10011 |
|---|---|---|
{{CRC_STEPS}}

The remainder is **{{CRC}}**, so the transmitted word is $1101011011\,{{CRC}}$ = `{{CRC_TX}}`. Receiver check: dividing `{{CRC_TX}}` by $10011$ gives remainder 0000 (accepted). If bit 5 is flipped in the channel the word is `{{CRC_BAD}}` and the remainder is {{CRC_BAD_REM}}, which is not zero, so the error is detected. (The division was done by program and the remainder 0000 at the receiver was asserted.)

CRC-4 detects all single-bit errors, all double-bit errors within a block of up to 15 bits (the polynomial is primitive with period 15) and all burst errors of length $\le 4$; it is used in ITU-T G.704 (T1/E1 framing) and in short packet headers. Longer polynomials (CRC-16, CRC-32) are used in HDLC and Ethernet.

**(c) LAN vs WAN.**

| Basis | LAN (local area network) | WAN (wide area network) |
|---|---|---|
| Coverage | a room, building or campus (up to a few km) | a country, a continent or the world |
| Data rate | 100 Mbit/s to 10 Gbit/s | lower on leased lines, 64 kbit/s to a few Gbit/s |
| Ownership | one organisation, private | many organisations; carriers lease the links (public) |
| Technology | Ethernet (802.3), Wi-Fi (802.11); switches | leased lines, MPLS, frame relay, ATM, satellite, fibre backbone, routers |
| Delay and errors | very low delay, very low error rate | high delay (tens of ms and more), more errors |
| Cost | low | high (lease and equipment) |
| Example | a college lab | the Internet, a bank's ATM network between cities |

**(d) FHSS and DSSS (spread spectrum).** Both spread a narrow-band signal over a much wider band, which gives resistance to jamming and interference, low probability of intercept and multiple access (CDMA).

| Basis | FHSS (frequency hopping) | DSSS (direct sequence) |
|---|---|---|
| Method | the carrier **hops** over $N$ channels in a pseudo-random order (PN sequence), staying on each for a short dwell time | each data bit is multiplied (XOR) by a fast **PN chip sequence** (spreading code) |
| Bandwidth | $N \times$ channel width | chip rate / data rate times the data bandwidth (processing gain $G_p = R_c/R_b$) |
| Interference | a narrow-band jammer hits only some hops, with only a small loss of bits | a jammer is spread by the despreading process and the signal is recovered by correlation |
| Synchronisation | the hop timing of transmitter and receiver must match | the chip sequence phase must be acquired |
| Examples | Bluetooth (79 channels of 1 MHz, 1600 hops/s), early Wi-Fi 802.11 FHSS | 802.11b Wi-Fi (11-chip Barker code), GPS, CDMA, IS-95 |

*DSSS example.* With the 11-chip Barker code `10110111000` a data bit 1 is sent as the code itself and a bit 0 as its complement:

| Data bit | PN (Barker) code | Transmitted chips |
|---|---|---|
{{DSSS}}

The processing gain is $G_p = 11$ (10.4 dB). *FHSS example:* with 8 channels (2.400 to 2.407 GHz) and the PN hop pattern 3, 7, 1, 5, 2, 6, 0, 4 the carrier is at 2.403, 2.407, 2.401, 2.405, 2.402, 2.406, 2.400, 2.404 GHz in successive dwell times, and the receiver hops with the same pattern.
