---
subject: Computer Networking
grade: BCA Semester 5
unit: 2
title: The Physical Layer
hours: 7
area: BCA 301 · Computer Networking · Unit 2
---

Everything above the physical layer pretends that bits exist. The physical layer is where they stop being a pretence: voltages on copper, pulses of light in glass, and radio waves in the air. How many bits per second you can push through a channel is not a matter of opinion; it is bounded by two famous formulas, Nyquist's and Shannon's, which you will compute in this unit. You will also see how signals are encoded, how many conversations share one wire (multiplexing), and how a network decides to switch traffic (circuits versus packets).

::: key What this unit gives you
- Analog and digital signals, bandwidth, impairments (attenuation, distortion, noise) and data-rate limits.
- Line coding: NRZ, NRZI, Manchester, AMI.
- Transmission media: twisted pair, coaxial, fibre, radio, satellite.
- Multiplexing (FDM, TDM, statistical TDM, WDM) and spread spectrum.
- Circuit, message and packet switching; telephone, cable and mobile data networks.
:::

## 2.1 Functions of the physical layer

The physical layer defines the **mechanical** characteristics (connectors, pin layout), **electrical** characteristics (voltage levels, bit duration), **functional** characteristics (what each wire does) and **procedural** characteristics (the order of events) of the interface to the medium. It decides the data rate (bits per second), whether the transmission is **simplex** (one way, radio broadcast), **half duplex** (both ways, one at a time, walkie-talkie) or **full duplex** (both ways at once, telephone), and how bits are synchronised.

## 2.2 Data and signals

**Data** is information; **signals** are the electromagnetic representation. **Analog** signals vary continuously; **digital** signals take a few discrete levels. A periodic signal is described by amplitude, frequency (cycles per second, hertz) and phase. A signal that is not a pure sine wave is a sum of sine waves of different frequencies (Fourier); the width of the frequency range it occupies is its **bandwidth** in hertz. *Bandwidth in hertz* (analog range of frequencies) and *bandwidth in bits per second* (data rate) are different quantities, though related.

### Baud rate and bit rate

The **signal rate** (baud) is the number of signal elements per second. If each element can carry b bits, then bit rate = baud × b. With 16 distinct levels (4 bits per element), a 56 kbps modem needs 56,000 / 4 = 14,000 baud.

### Transmission impairments

- **Attenuation**: loss of strength along the medium, measured in decibels (dB). dB = 10 log₁₀(P₂/P₁). A loss of 3 dB is half the power; −30 dB is a thousandth.
- **Distortion**: different frequencies travel at different speeds, so the shape of a composite signal changes.
- **Noise**: unwanted signals: thermal noise (always present), crosstalk (from a neighbouring wire), impulse noise (spikes) and interference.

The **signal-to-noise ratio** SNR = (average signal power)/(average noise power), usually quoted as SNR_dB = 10 log₁₀ SNR. An SNR of 1000 is 30 dB; 100 is 20 dB.

## 2.3 Data rate limits

### Nyquist: a noiseless channel

For a channel of bandwidth B Hz with L signal levels, the maximum bit rate is **C = 2 B log₂ L**. Nyquist's theorem says you cannot send more than 2B signal elements per second without intersymbol interference, so the only way to get a higher bit rate is to use more levels.

| Bandwidth B | Levels L | Bits per element | Maximum bit rate |
|---|---|---|---|
| 3000 Hz | 2 | 1 | 6,000 bps |
| 3000 Hz | 4 | 2 | 12,000 bps |
| 3000 Hz | 16 | 4 | 24,000 bps |

### Shannon: a noisy channel

Real channels have noise, which makes many levels indistinguishable. Shannon's capacity theorem gives the absolute maximum for any coding scheme: **C = B log₂(1 + SNR)**.

::: example A telephone channel
A voice channel has B = 3000 Hz and SNR = 30 dB. First convert: SNR = 10^(30/10) = 1000. Then C = 3000 × log₂(1001) = 3000 × 9.967 ≈ 29,902 bps. No technique can exceed about 29.9 kbps on this channel, which is why 56 kbps modems relied on an almost entirely digital telephone network, where the only analog part is the short local loop. For a 1 MHz channel with SNR = 20 dB (100), C = 10⁶ × log₂(101) ≈ 6,658,211 bps.
:::

::: example What SNR does a 56 kbps modem need?
For B = 3100 Hz, 56,000 = 3100 × log₂(1 + SNR) gives 1 + SNR = 2^(18.06), so SNR_dB = 10 log₁₀(2^(56000/3100) − 1) ≈ 54.38 dB. Real voice lines rarely reach that, which is why 56k modems usually connected at less.
:::

In practice use *both*: Shannon gives the ceiling (bandwidth and SNR), Nyquist tells how many signal levels are needed to reach a target rate below the ceiling. For a 6 Mbps target on a 1 MHz channel: Shannon bound is fine (6.66 Mbps), Nyquist demands 2 × 10⁶ × log₂ L ≥ 6 × 10⁶, so L ≥ 2³ = 8 levels.

::: caution Common error
Do not use B in kilohertz with the formula expecting bits per second *per kilohertz*: keep B in hertz so the answer is in bits per second. And Shannon needs SNR as a *ratio* (1000), not in dB (30).
:::

## 2.4 Line coding and digital signalling

To send digital data over a wire the bits become voltage levels. A good code carries the **clock** (so the receiver stays synchronised), has no DC component and detects some errors.

| Code | Rule | Remark |
|---|---|---|
| NRZ-L | 1 = high, 0 = low | simple; long runs of equal bits lose synchronisation |
| NRZI | a 1 flips the level, a 0 keeps it | solves runs of 1s only |
| Manchester | each bit has a mid-bit transition: 1 = low-to-high, 0 = high-to-low (IEEE 802.3 convention) | self-clocking, needs twice the bandwidth; used in 10 Mbps Ethernet |
| AMI (bipolar) | 0 = zero level, 1 alternately +V and −V | no DC, detects single errors; long zero runs are a problem |

For the bit string 10110010: Manchester (as pairs of half-bit levels, 0 = low, 1 = high) is 01 10 01 01 10 10 01 10, which reads 0110010110100110; NRZI (starting at −) is + + − + + + − −; AMI is + 0 − + 0 0 − 0.

Faster Ethernet standards avoid Manchester's halving of efficiency with block codes: **4B/5B** maps every 4 data bits to a 5-bit code with enough transitions (efficiency 80 %), and **8B/10B** and **64B/66B** do the same for gigabit and 10-gigabit links.

### Analog transmission of digital data

Over a band-limited line a **carrier** sine wave is modified by the data: **ASK** (amplitude), **FSK** (frequency), **PSK** (phase) or **QAM**, which varies both amplitude and phase. QAM-16 sends 4 bits per symbol. Wi-Fi and DSL use QAM constellations as dense as 1024 or 4096 points when SNR is high.

### Sampling voice: PCM

A telephone voice channel is limited to about 4 kHz. The Nyquist sampling theorem requires sampling at twice the highest frequency: 8000 samples per second, 8 bits each: 64 kbps per voice channel (the "DS0" rate).

## 2.5 Transmission media

### Guided media

| Medium | Construction | Typical use | Notes |
|---|---|---|---|
| UTP (Cat5e, Cat6) | four twisted pairs, no shield | office LAN, up to 100 m | twisting cancels interference; Cat5e to 1 Gbps, Cat6 to 10 Gbps over short runs |
| STP | pairs with foil/braid shield | noisy places | more costly |
| Coaxial | copper core, insulator, braid | cable TV, old 10BASE2 Ethernet | better shielding, higher bandwidth than twisted pair |
| Optical fibre | glass core and cladding, light pulses | backbones, FTTH | immune to electromagnetic noise, kilometres without repeaters |

**Optical fibre.** Light stays in the core by **total internal reflection**. **Multimode** fibre (50 or 62.5 µm core) carries many light paths and suits up to a few hundred metres with LEDs or VCSEL lasers; **single-mode** fibre (about 9 µm core) carries one path, suffers little dispersion and reaches tens of kilometres with a laser. Fibre has low attenuation (about 0.2 dB/km at 1550 nm), very high bandwidth and no electromagnetic interference, but is harder to splice and connectors must be kept clean. Fibre-to-the-home (**GPON**) shares one fibre among up to 32 or 64 homes using passive splitters and time-division multiplexing.

**UTP cabling.** Ethernet cable is wired to **T568A** or **T568B**. A *straight-through* cable has the same standard at both ends (PC to switch); a *crossover* cable has A at one end and B at the other (PC to PC, switch to switch) although modern ports use auto-MDI-X and make the distinction unnecessary. Maximum segment length for 10/100/1000BASE-T is 100 m.

### Unguided media

Radio waves (3 kHz to 300 GHz) propagate through the air. Low frequencies travel farther and through walls; high frequencies carry more data but need line of sight. Wi-Fi uses the 2.4, 5 and 6 GHz unlicensed bands. Microwave links join towers over a few tens of kilometres, which is how remote hills of Nepal are connected where fibre is too costly. **Infrared** works only within a room. **Satellites** relay signals: geostationary satellites orbit 35,786 km above the equator, giving a one-way trip (ground to satellite to ground) of about 239 ms, so a request and its reply take about 480 ms; low-earth orbit constellations such as Starlink fly at 550 km and have latencies near 30–50 ms.

## 2.6 Multiplexing

**Multiplexing** lets several signals share one link.

- **FDM** (frequency-division): each channel gets its own band. Three 4 kHz voice channels with two 1 kHz guard bands need 3 × 4 + 2 × 1 = 14 kHz. Radio and cable TV use FDM.
- **TDM** (time-division): channels take turns in fixed time slots. Four channels each sending 8 bits per slot, 8000 frames per second, need 4 × 8 × 8000 = 256,000 bps. The North-American T1 carries 24 voice channels plus 1 framing bit per frame: (24 × 8 + 1) × 8000 = 1,544,000 bps; the European E1 carries 30 voice channels plus two control channels: 32 × 8 × 8000 = 2.048 Mbps.
- **Statistical TDM**: slots are given only to channels with data, so the link can be shared by more sources than its capacity if they are rarely all active; each slot carries an address.
- **WDM** (wavelength-division): the optical equivalent of FDM, many colours of laser light on one fibre; dense WDM carries 80 or more wavelengths each at 100 Gbps.

**Spread spectrum** spreads a narrow-band signal over a wide band to resist jamming and interference: **FHSS** hops among frequencies in a pseudo-random pattern (Bluetooth), **DSSS** multiplies each bit by a fast chip sequence (original 802.11, GPS, CDMA). **OFDM** divides the channel into many narrow sub-carriers (Wi-Fi 802.11a/g/n/ac/ax, 4G, 5G, DSL).

## 2.7 Switching

A network of many nodes cannot connect everybody directly, so intermediate nodes **switch** data.

| Method | How | Delay | Resource use | Example |
|---|---|---|---|---|
| Circuit switching | a dedicated path is set up for the call, then used exclusively | set-up time, then constant | capacity reserved even if idle | old telephone network |
| Message switching | the whole message is stored at each node and forwarded | high, grows with message size | no reservation | telegraph, e-mail relays |
| Packet switching: datagram | message cut into packets, each routed independently | variable, queuing | statistical sharing | IP networks |
| Packet switching: virtual circuit | a path is set up once, packets follow it with a short circuit ID | fixed route, queuing | statistical sharing | MPLS, ATM, Frame Relay |

Circuit switching suits constant-rate traffic such as voice. Packet switching suits **bursty** data: if each of 35 users needs 100 kbps but only 10 % of the time on a 1 Mbps link, circuit switching can give only 10 users a circuit, while packet switching serves all 35 and the probability of more than 10 being active at once is small (about 0.0004). That statistical gain is why the Internet uses packet switching.

## 2.8 Telephone, cable and mobile data networks

- **Dial-up and DSL**: the telephone local loop (copper pair) carries voice below 4 kHz; **ADSL** uses frequencies above 25 kHz with DMT (OFDM), giving asymmetric rates (more downstream), a splitter separates voice from data.
- **Cable networks**: **HFC** (hybrid fibre-coax) shares a coaxial segment among homes; the DOCSIS standard assigns upstream and downstream channels and a scheduler arbitrates access.
- **Mobile networks**: cells with a base station each; frequency reuse in non-adjacent cells. 2G (GSM, voice, SMS), 3G (UMTS, data), 4G (LTE, all-IP, OFDMA), 5G (higher bands, massive MIMO, low latency). A handoff moves a call from one cell to the next as the user travels.

## Practising the commands

The code below checks the Nyquist and Shannon figures and regenerates the line-coding example from this unit.

```python
import math
def nyquist(B, L): return 2 * B * math.log2(L)
def shannon(B, snr_db): return B * math.log2(1 + 10 ** (snr_db / 10))
for L in (2, 4, 16): print("Nyquist B=3000 L=%d:" % L, nyquist(3000, L))
print("Shannon 3 kHz, 30 dB: %.0f bps" % shannon(3000, 30))
print("Shannon 1 MHz, 20 dB: %.0f bps" % shannon(1e6, 20))
bits = "10110010"
manch = "".join("01" if b == "1" else "10" for b in bits)
lvl, nrzi = "-", ""
for b in bits:
    if b == "1": lvl = "+" if lvl == "-" else "-"
    nrzi += lvl
print("Manchester", manch); print("NRZI", nrzi)
print("T1 rate", (24 * 8 + 1) * 8000, "bps; E1 rate", 32 * 8 * 8000, "bps")
```
```output
Nyquist B=3000 L=2: 6000.0
Nyquist B=3000 L=4: 12000.0
Nyquist B=3000 L=16: 24000.0
Shannon 3 kHz, 30 dB: 29902 bps
Shannon 1 MHz, 20 dB: 6658211 bps
Manchester 0110010110100110
NRZI ++-+++--
T1 rate 1544000 bps; E1 rate 2048000 bps
```
## 2.9 Seeing the ideas: signals, media, multiplexing and switching

The physical layer is made of real things: copper pairs, glass fibre, radio towers and the boxes that join them. Plate 2.1 puts faces and cables side by side: the two engineers behind the two capacity formulas, a Cat5e cable with its four twisted pairs, and the LC and SC connectors of optical fibre. Plate 2.2 shows the boxes that turn bits into light and radio waves: an SFP optical transceiver, a tower of microwave dishes and a mobile base station. Plate 2.3 shows the telephone line at work: an ADSL splitter socket, an outdoor DSLAM cabinet and an old crossbar exchange. The figures that follow are computed, not sketched: every capacity, waveform, delay and probability in them comes from the formulas of this unit.

```photogrid label="2.1" cols="4" ratio="1.0" caption="Two theorists and two media. (a) The memorial stone of Harry Nyquist (1889-1976), who showed that a channel of bandwidth B carries at most 2B signal elements per second (CC BY-SA 4.0). (b) Claude Shannon at his desk (public domain, MIT, 1958), who proved the capacity of a noisy channel, C = B log2(1 + SNR). (c) A Cat5e cable with the jacket stripped, showing the four twisted pairs (CC BY-SA 3.0): the twist makes noise from outside hit both wires of a pair equally, so the receiver cancels it. (d) LC (left pair) and SC (right pair) fibre connectors (CC BY-SA 3.0): each end holds one glass fibre in a precise ceramic ferrule."
@ photo id="bca301/nyquist" cap="Harry Nyquist memorial"
fit 1.0
focus 0.5 0.3
@ photo id="bca301/shannon" cap="Claude Shannon (1958)"
fit 1.0
focus 0.4 0.3
@ photo id="bca301/cat5e" cap="Cat5e: four twisted pairs"
fit 1.0
focus 0.4 0.45
call 0.52 0.88 0.4 0.55 "twisted pairs"
@ photo id="bca301/lcsc" cap="LC and SC fibre connectors"
fit 1.0
focus 0.5 0.5
```

```photogrid label="2.2" cols="3" ratio="1.25" caption="Where bits become light and radio. (a) An optical transceiver module (SFP, right, with an older GBIC beside it): a laser and a photodiode in a pluggable body, the part that turns the switch's electrical bits into pulses of light for the fibre (CC BY-SA 2.0 de). (b) Parabolic dishes on a tower (CC BY-SA 2.5 au): each dish is one point-to-point microwave link to a distant tower, the way hill districts are joined to the network where fibre is too costly. (c) A mobile base station with its mast and equipment cabin (CC BY-SA 4.0): one cell of a cellular network."
@ photo id="bca301/sfp" cap="SFP transceiver (light)"
fit 1.25
focus 0.5 0.5
@ photo id="bca301/microwave" cap="Microwave dishes on a tower"
fit 1.25
focus 0.5 0.5
@ photo id="bca301/mast" cap="Base station: one cell"
fit 1.25
focus 0.5 0.55
```

```photogrid label="2.3" cols="3" ratio="1.25" caption="The telephone line as a data line. (a) A DSL splitter socket opened up (CC BY 3.0 de): a filter that sends the voice band below 4 kHz to the phone and the higher ADSL band to the modem. (b) An outdoor DSLAM cabinet being serviced (CC BY-SA 4.0): the many copper pairs of a street end here, and the DSLAM multiplexes them onto one fibre. (c) The crossbar switch of a telephone exchange (public domain, bca152): circuit switching in iron, a metal path reserved for the whole call."
@ photo id="bca301/dslsplit" cap="ADSL splitter socket"
fit 1.25
focus 0.5 0.5
@ photo id="bca301/dslam" cap="Outdoor DSLAM cabinet"
fit 1.25
focus 0.5 0.5
@ photo id="bca152/crossbar" cap="Crossbar telephone exchange"
fit 1.25
focus 0.5 0.5
```

```svgfig label="2.1" caption="Nyquist against Shannon for a 3000 Hz telephone channel, computed. The curve is the Shannon limit C = 3000 x log2(1 + SNR) against the signal-to-noise ratio in dB; it climbs about 1000 bps for every 1 dB at high SNR. The dashed lines are Nyquist limits 2 x 3000 x log2 L for 2, 4 and 16 levels (6, 12 and 24 kbps). A scheme with L levels is feasible only where the curve lies above its line: 2 levels need SNR 3 (4.77 dB), 4 levels need 15 (11.76 dB) and 16 levels need 255 (24.07 dB). At 30 dB the ceiling is 29 902 bps, so no cleverness can give 56 kbps on such a line."
f = Fig(580, 270)
cm = __import__("math")
L, T, W, H = 56, 14, 330, 210
X = lambda s: L + W * s / 40.0
Y = lambda c: T + H - H * c / 40000.0
f.box(L, T, W, H, "", fill="#ffffff", stroke="#94a3b8", r=2, sw=1.2)
for k in range(1, 5):
    f.line(L, T + H * k / 5.0, L + W, T + H * k / 5.0, color="#e2e8f0", sw=1)
for k in range(6):
    f.text(L - 6, T + H - H * k / 5.0, "%d" % (k * 8), size=9.5, color=SLATE, anchor="end", vmid=True)
for s in range(0, 41, 10):
    f.text(X(s), T + H + 14, str(s), size=9.5, color=SLATE)
f.text(L + W / 2, T + H + 32, "signal-to-noise ratio (dB)", size=10, color=SLATE, bold=True)
f.text(14, T + H / 2, "kbps", size=10, color=SLATE, bold=True)
for lv, col in ((2, TEAL), (4, AMBER), (16, RED)):
    c = 2 * 3000 * cm.log2(lv)
    f.line(L, Y(c), L + W, Y(c), color=col, sw=1.4, dash=True)
    f.text(L + 6, Y(c) - 7, "Nyquist L = %d (%d kbps)" % (lv, c / 1000), size=9.5, color=col, bold=True, anchor="start")
    snr = lv * lv - 1
    f.circle(X(10 * cm.log10(snr)), Y(c), 4, fill=col, stroke=col)
pm = " ".join("%.1f,%.1f" % (X(s / 4.0), Y(3000 * cm.log2(1 + 10 ** (s / 40.0)))) for s in range(0, 161))
f.raw('<polyline points="%s" fill="none" stroke="#1e3a8a" stroke-width="2.6"/>' % pm)
f.circle(X(30), Y(3000 * cm.log2(1001)), 4.5, fill=NAVY, stroke=NAVY)
f.text(X(30) - 8, Y(3000 * cm.log2(1001)) + 16, "30 dB: 29 902 bps", size=10, color=NAVY, bold=True, anchor="end")
rows = [("L", "needs SNR", "in dB"), ("2", "3", "4.77"), ("4", "15", "11.76"), ("16", "255", "24.07")]
for i, r in enumerate(rows):
    for j, v in enumerate(r):
        f.text([420, 458, 520][j], 46 + i * 26, v, size=10, color=NAVY if i == 0 else SLATE, bold=(i == 0), anchor="start")
f.text(420, 168, "Shannon curve (blue):", size=10, color=NAVY, bold=True, anchor="start")
f.text(420, 184, "the ceiling for any scheme", size=10, color=SLATE, anchor="start")
f.text(420, 204, "More levels need a cleaner line", size=10, color=RED, bold=True, anchor="start")
```

```svgfig label="2.2" caption="Why bandwidth matters: a 1 kHz square wave rebuilt from its sine-wave harmonics (Fourier). With only the 1 kHz sine (bandwidth 1 kHz) the pulse is a smooth hump; adding the 3rd harmonic (bandwidth 3 kHz) makes the shoulders flat; adding the 5th, 7th and 9th (bandwidth 9 kHz) gives sharp edges. Each harmonic of order n has amplitude 4/(n x pi) of the full swing. A channel that passes only the first few harmonics rounds the pulses, and when the rounding of one bit spills into the next, this is intersymbol interference, the effect Nyquist's 2B limit describes."
f = Fig(580, 230)
cm = __import__("math")
panels = [(1, "1 kHz only", "bandwidth 1 kHz"), (3, "harmonics 1 and 3", "bandwidth 3 kHz"), (9, "harmonics 1, 3, 5, 7, 9", "bandwidth 9 kHz")]
for i, (nmax, ttl, bw) in enumerate(panels):
    x0 = 14 + i * 192
    f.box(x0, 8, 180, 170, "", fill="#ffffff", stroke="#cbd5e1", r=4, sw=1)
    f.text(x0 + 90, 24, ttl, size=10.5, color=NAVY, bold=True)
    cy, A = 100, 46
    f.line(x0 + 8, cy, x0 + 172, cy, color="#e2e8f0", sw=1)
    f.line(x0 + 8, cy - A, x0 + 172, cy - A, color="#e2e8f0", sw=1, dash=True)
    f.line(x0 + 8, cy + A, x0 + 172, cy + A, color="#e2e8f0", sw=1, dash=True)
    def sq(t):
        return sum(4 / (cm.pi * n) * cm.sin(2 * cm.pi * n * t) for n in range(1, nmax + 1, 2))
    pts = " ".join("%.1f,%.1f" % (x0 + 10 + 160 * t / 2.0, cy - A * 0.78 * sq(t)) for t in [k / 160.0 * 2 for k in range(161)])
    f.raw('<polyline points="%s" fill="none" stroke="#1e3a8a" stroke-width="2.2"/>' % pts)
    f.text(x0 + 90, 152, bw, size=10.5, color=RED, bold=True)
    f.text(x0 + 90, 168, "sum of %d sine%s" % ((nmax + 1) // 2, "s" if nmax > 1 else ""), size=9.5, color=SLATE)
f.text(290, 200, "amplitude of the n-th harmonic = 4 / (n x pi): 1.27, 0.42, 0.25, 0.18, 0.14 for n = 1, 3, 5, 7, 9", size=10, color=SLATE)
f.text(290, 218, "a perfect square wave needs every odd harmonic, that is infinite bandwidth", size=10, color=NAVY, bold=True)
```

```svgfig label="2.3" caption="Four line codes for the bit string 10110010, drawn to a common bit grid. NRZ-L: high for 1, low for 0. NRZI: a 1 flips the level, a 0 keeps it (starting low). Manchester (IEEE 802.3 convention used in this book): every bit has a transition in the middle, 1 = low then high, 0 = high then low. AMI: 0 is zero volts and the 1s alternate +V and -V. Count the transitions: Manchester always has one or two per bit, so the receiver can recover the clock even from 00000000, while NRZ-L has none for a long run of equal bits."
f = Fig(580, 300)
bits = "10110010"
x0, bw = 112, 56
for i, b in enumerate(bits):
    f.text(x0 + i * bw + bw / 2, 14, b, size=12, color=NAVY, bold=True)
    f.line(x0 + i * bw, 24, x0 + i * bw, 286, color="#e2e8f0", sw=1, dash=True)
f.line(x0 + 8 * bw, 24, x0 + 8 * bw, 286, color="#e2e8f0", sw=1, dash=True)
def draw(cy, levels, col):
    # levels: list of (start, end, level) in bit units; level in -1,0,1
    pts = []
    A = 20
    for (a, b, lv) in levels:
        y = cy - A * lv
        pts.append((x0 + a * bw, y)); pts.append((x0 + b * bw, y))
    d = []
    for p in pts:
        d.append("%.1f,%.1f" % p)
    f.raw('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.4"/>' % (" ".join(d), col))
def rowlab(cy, name, sub):
    f.text(8, cy - 6, name, size=11, color=NAVY, bold=True, anchor="start")
    f.text(8, cy + 9, sub, size=9.5, color=SLATE, anchor="start")
cys = [58, 128, 198, 268]
rowlab(cys[0], "NRZ-L", "1 high, 0 low")
draw(cys[0], [(i, i + 1, 1 if b == "1" else -1) for i, b in enumerate(bits)], "#1e3a8a")
rowlab(cys[1], "NRZI", "1 flips level")
lv = -1; L2 = []
for i, b in enumerate(bits):
    if b == "1": lv = -lv
    L2.append((i, i + 1, lv))
draw(cys[1], L2, "#0f766e")
rowlab(cys[2], "Manchester", "1 low-high")
L3 = []
for i, b in enumerate(bits):
    a, c = (-1, 1) if b == "1" else (1, -1)
    L3.append((i, i + 0.5, a)); L3.append((i + 0.5, i + 1, c))
draw(cys[2], L3, "#b91c1c")
rowlab(cys[3], "AMI", "1 = +V, -V")
pol = 1; L4 = []
for i, b in enumerate(bits):
    if b == "1":
        L4.append((i, i + 1, pol)); pol = -pol
    else:
        L4.append((i, i + 1, 0))
draw(cys[3], L4, "#b45309")
for cy in cys:
    f.line(x0, cy, x0 + 8 * bw, cy, color="#cbd5e1", sw=1)
```

```svgfig label="2.4" caption="Sending bits over a carrier. Left: the bits 1 0 1 1 as ASK (amplitude: the carrier is strong for 1 and weak for 0), FSK (frequency: 4 cycles per bit for 1, 2 cycles for 0) and PSK (phase: the wave is inverted for 0). Right: constellation diagrams, where each dot is one symbol that the receiver must tell apart: BPSK has 2 dots (1 bit per symbol), QPSK 4 (2 bits), 16-QAM 16 (4 bits) and 64-QAM 64 (6 bits). At 1 million symbols per second these carry 1, 2, 4 and 6 Mbps, but the dots of 64-QAM are so close that they need about 18 dB of SNR, which is why a Wi-Fi router drops to a slower scheme when you walk away."
f = Fig(580, 300)
cm = __import__("math")
bits = [1, 0, 1, 1]
names = [("ASK", 58), ("FSK", 140), ("PSK", 222)]
f.text(24, 14, "bits", size=10, color=SLATE, bold=True, anchor="start")
for i, b in enumerate(bits):
    f.text(24 + i * 75 + 37, 14, str(b), size=12, color=NAVY, bold=True)
    f.line(24 + i * 75, 22, 24 + i * 75, 270, color="#e2e8f0", sw=1, dash=True)
f.line(24 + 300, 22, 24 + 300, 270, color="#e2e8f0", sw=1, dash=True)
for nm, cy in names:
    f.text(6, cy, nm, size=10.5, color=NAVY, bold=True, anchor="start")
    pts = []
    for k in range(0, 301):
        t = k / 75.0
        bi = min(int(t), 3); fr = t - bi
        b = bits[bi]
        if nm == "ASK": y = (1.0 if b else 0.3) * cm.sin(2 * cm.pi * 3 * t)
        elif nm == "FSK": y = cm.sin(2 * cm.pi * (4 if b else 2) * fr + 0) if True else 0
        else: y = (1 if b else -1) * cm.sin(2 * cm.pi * 3 * t)
        pts.append("%.1f,%.1f" % (24 + k, cy - 30 * y))
    col = {"ASK": "#1e3a8a", "FSK": "#0f766e", "PSK": "#b91c1c"}[nm]
    f.raw('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.8"/>' % (" ".join(pts), col))
def const(cx, cy, m, title, sub):
    f.box(cx - 52, cy - 52, 104, 104, "", fill="#ffffff", stroke="#cbd5e1", r=4, sw=1)
    f.line(cx - 48, cy, cx + 48, cy, color="#e2e8f0", sw=1)
    f.line(cx, cy - 48, cx, cy + 48, color="#e2e8f0", sw=1)
    if m == 2: P = [(-1, 0), (1, 0)]
    elif m == 4: P = [(a, b) for a in (-1, 1) for b in (-1, 1)]
    else:
        k = int(cm.sqrt(m)); v = [(2 * i - (k - 1)) for i in range(k)]
        P = [(a, b) for a in v for b in v]
    mx = max(max(abs(a), abs(b)) for a, b in P)
    for a, b in P:
        f.circle(cx + a / mx * 38, cy - b / mx * 38, 2.6 if m < 64 else 2.0, fill=NAVY, stroke=NAVY)
    f.text(cx, cy + 66, title, size=10.5, color=NAVY, bold=True)
    f.text(cx, cy + 80, sub, size=9.5, color=SLATE)
const(374, 70, 2, "BPSK", "1 bit, 1 Mbps")
const(504, 70, 4, "QPSK", "2 bits, 2 Mbps")
const(374, 210, 16, "16-QAM", "4 bits, 4 Mbps")
const(504, 210, 64, "64-QAM", "6 bits, 6 Mbps")
```

```svgfig label="2.5" caption="Pulse code modulation of a 1 kHz tone, computed. The wave is sampled every 125 microseconds (8000 samples per second, twice the 4 kHz voice limit), each sample is rounded to one of 8 levels (3 bits, so the figure stays readable) and sent as a code word: 100 110 111 110 100 001 000 001, which is 24 bits in 1 ms. The rounding error is the quantisation noise; every extra bit adds about 6 dB of signal-to-noise ratio (3 bits about 19.8 dB, 8 bits about 49.9 dB). Real telephony uses 8 bits per sample: 8000 x 8 = 64 000 bps, the DS0 channel."
f = Fig(580, 290)
cm = __import__("math")
L, T, W, H = 40, 14, 340, 230
f.box(L, T, W, H, "", fill="#ffffff", stroke="#94a3b8", r=2, sw=1.2)
Yv = lambda v: T + H / 2 - v * (H / 2 - 6)
for k in range(9):
    v = -1 + k * 0.25
    f.line(L, Yv(v), L + W, Yv(v), color="#e2e8f0", sw=1)
codes = []
for k in range(8):
    v = cm.sin(2 * cm.pi * k / 8.0)
    idx = min(int((v + 1) / 0.25), 7)
    codes.append(format(idx, "03b"))
for q in range(8):
    f.text(L - 6, Yv(-1 + q * 0.25 + 0.125), format(q, "03b"), size=9, color=SLATE, anchor="end", vmid=True)
pts = " ".join("%.1f,%.1f" % (L + W * t / 1.0, Yv(cm.sin(2 * cm.pi * t))) for t in [k / 200.0 for k in range(201)])
f.raw('<polyline points="%s" fill="none" stroke="#1e3a8a" stroke-width="2"/>' % pts)
for k in range(9):
    x = L + W * k / 8.0
    f.line(x, T, x, T + H, color="#fecaca", sw=1, dash=True)
    v = cm.sin(2 * cm.pi * k / 8.0)
    if k < 8:
        idx = min(int((v + 1) / 0.25), 7)
        f.circle(x, Yv(v), 3.6, fill=RED, stroke=RED)
        f.circle(x, Yv(-1 + idx * 0.25 + 0.125), 4.0, fill="#ffffff", stroke=TEAL, sw=2)
        f.text(x + W / 16.0, T + H + 14, codes[k], size=9.5, color=NAVY, bold=True)
f.text(L + W / 2, T + H + 32, "one cycle of 1 kHz = 1000 microseconds, one sample every 125 microseconds, 3-bit code words", size=10, color=SLATE)
f.text(396, 40, "red dot: the sample", size=10, color=RED, bold=True, anchor="start")
f.text(396, 58, "ring: the nearest level sent", size=10, color=TEAL, bold=True, anchor="start")
f.text(396, 92, "rate = samples/s x bits", size=10, color=NAVY, bold=True, anchor="start")
f.text(396, 112, "3-bit: 8000 x 3 = 24 kbps", size=10, color=SLATE, anchor="start")
f.text(396, 130, "8-bit: 8000 x 8 = 64 kbps", size=10, color=SLATE, anchor="start")
f.text(396, 164, "SNR = 6.02 n + 1.76 dB", size=10, color=NAVY, bold=True, anchor="start")
f.text(396, 184, "n = 3: 19.8 dB", size=10, color=SLATE, anchor="start")
f.text(396, 202, "n = 8: 49.9 dB", size=10, color=SLATE, anchor="start")
```

```svgfig label="2.6" caption="How a fibre guides light, with the numbers worked out. Left: a ray inside a core of refractive index 1.48 meets the cladding of index 1.46 at an angle larger than the critical angle asin(1.46 / 1.48) = 80.6 degrees (measured from the normal), so it is totally reflected again and again; a ray that enters within a cone of half-angle asin(sqrt(1.48^2 - 1.46^2)) = 14.0 degrees is accepted. Right: cross-sections drawn to the same scale (0.9 px per micrometre): both fibres have a 125 micrometre cladding, but a multimode core is 50 micrometres and a single-mode core only 9. Below: at 0.2 dB per km a signal keeps 63 percent of its power after 10 km, 10 percent after 50 km and 1 percent after 100 km."
f = Fig(580, 290)
cm = __import__("math")
f.box(16, 56, 270, 30, "cladding n = 1.46", fill="#dbeafe", stroke="#93c5fd", size=10, r=2, color=NAVY)
f.box(16, 86, 270, 40, "", fill="#fef9c3", stroke="#fcd34d", r=0, sw=1.2)
f.box(16, 126, 270, 30, "cladding n = 1.46", fill="#dbeafe", stroke="#93c5fd", size=10, r=2, color=NAVY)
f.text(60, 118, "core n = 1.48", size=9.5, color=AMBER, bold=True)
pts = [(16, 126)]
x, up = 16, False
ys = [(16, 100)]
rx = [16, 66, 126, 186, 246, 286]
ry = [106, 88, 124, 88, 124, 100]
f.raw('<polyline points="%s" fill="none" stroke="#b91c1c" stroke-width="2.4"/>' % " ".join("%d,%d" % p for p in zip(rx, ry)))
f.arrow([(0, 106), (16, 106)], color=RED, sw=2)
f.text(150, 176, "critical angle 80.6 deg; total internal reflection", size=10, color=RED, bold=True)
f.text(150, 192, "acceptance half-angle 14.0 deg", size=10, color=SLATE)
f.text(150, 208, "light never leaves the core, so loss is small", size=10, color=SLATE)
for cx, core, ttl, sub in ((380, 50, "multimode", "50 um core, LED"), (500, 9, "single-mode", "9 um core, laser")):
    f.circle(cx, 100, 125 * 0.9 / 2, fill="#dbeafe", stroke="#93c5fd", sw=1.5, label="")
    f.circle(cx, 100, core * 0.9 / 2, fill="#fde68a", stroke=AMBER, sw=1.5, label="")
    f.text(cx, 176, ttl, size=11, color=NAVY, bold=True)
    f.text(cx, 192, sub, size=9.5, color=SLATE)
f.text(440, 20, "125 um cladding, drawn to scale", size=10, color=NAVY, bold=True)
rows = [("distance", "loss at 0.2 dB/km", "power left"), ("10 km", "2 dB", "63 %"), ("50 km", "10 dB", "10 %"), ("100 km", "20 dB", "1 %")]
for i, r in enumerate(rows):
    for j, v in enumerate(r):
        f.text([70, 190, 350][j], 232 + i * 17, v, size=10, color=NAVY if i == 0 else SLATE, bold=(i == 0), anchor="start")
```

```svgfig label="2.7" caption="The crossover cable explained. Each wire keeps its colour from one plug to the other. The top plug is wired to T568B (pin 1 white-orange, 2 orange, 3 white-green, 4 blue, 5 white-blue, 6 green, 7 white-brown, 8 brown), the bottom plug to T568A (pins 1 and 3 and pins 2 and 6 swapped). Following the colours, the orange pair that leaves pins 1 and 2 (transmit) arrives at pins 3 and 6 (receive) of the other end, and the green pair does the opposite, so two computers can talk directly. Wire both plugs to the same standard (usually T568B) and the cable is straight-through, used between a computer and a switch. The 4-5 and 7-8 pairs go straight across; they carry data only in gigabit Ethernet."
f = Fig(580, 290)
B = ["wo", "o", "wg", "bl", "wbl", "g", "wbr", "br"]
A = ["wg", "g", "wo", "bl", "wbl", "o", "wbr", "br"]
col = {"o": "#f97316", "g": "#16a34a", "bl": "#2563eb", "br": "#92400e"}
def patch(x, y, c):
    base = col[c[1:] if c.startswith("w") else c]
    f.box(x, y, 34, 24, "", fill=base, stroke="#334155", r=3, sw=1)
    if c.startswith("w"):
        f.line(x + 6, y + 12, x + 28, y + 12, color="#ffffff", sw=6)
        f.box(x, y, 34, 24, "", fill="none", stroke="#334155", r=3, sw=1)
xs = [86 + i * 60 for i in range(8)]
f.text(6, 52, "T568B end", size=11, color=NAVY, bold=True, anchor="start")
f.text(6, 66, "(computer 1)", size=9.5, color=SLATE, anchor="start")
f.text(6, 218, "T568A end", size=11, color=NAVY, bold=True, anchor="start")
f.text(6, 232, "(computer 2)", size=9.5, color=SLATE, anchor="start")
fn = ["TX+", "TX-", "RX+", "", "", "RX-", "", ""]
for i in range(8):
    f.text(xs[i] + 17, 24, str(i + 1), size=10.5, color=NAVY, bold=True)
    f.text(xs[i] + 17, 92 - 20 + 3, fn[i], size=9.5, color=SLATE)
    patch(xs[i], 40, B[i])
    patch(xs[i], 190, A[i])
    f.line(xs[i] + 17, 64, xs[A.index(B[i])] + 17, 190, color="#475569" if A.index(B[i]) == i else "#dc2626", sw=1.4 if A.index(B[i]) == i else 2.2)
    f.text(xs[i] + 17, 232, str(i + 1), size=10.5, color=NAVY, bold=True)
f.text(290, 262, "red lines: the wires that cross (1 to 3, 2 to 6, 3 to 1, 6 to 2); grey lines go straight across", size=10, color=RED, bold=True)
f.text(290, 280, "TX = transmit pair (pins 1, 2) and RX = receive pair (pins 3, 6) at the computer end of 10/100BASE-T", size=10, color=SLATE)
```

```svgfig label="2.8" caption="Multiplexing to scale. Top: FDM of three 4 kHz voice channels with 1 kHz guard bands needs 3 x 4 + 2 x 1 = 14 kHz (20 px per kHz). Below: one TDM frame lasts 125 microseconds (8000 frames per second). A T1 frame holds 24 slots of 8 bits plus 1 framing bit = 193 bits, giving 193 x 8000 = 1 544 000 bps; an E1 frame holds 32 slots of 8 bits = 256 bits, giving 2 048 000 bps, with slot 0 for frame synchronisation and slot 16 for signalling, so 30 slots carry voice. A phone call fills exactly one slot per frame: 8 x 8000 = 64 kbps. Drawn at 2 px per bit."
f = Fig(580, 300)
f.text(14, 16, "FDM: 14 kHz total", size=10.5, color=NAVY, bold=True, anchor="start")
x = 14
for i in range(3):
    f.box(x, 26, 80, 34, "channel %d, 4 kHz" % (i + 1), fill=[MINT, BLUE, SAND][i], stroke=[TEAL, NAVY, AMBER][i], size=9.5, r=2)
    x += 80
    if i < 2:
        f.box(x, 26, 20, 34, "", fill="#f1f5f9", stroke="#94a3b8", r=0, sw=1, dash=True)
        f.text(x + 10, 72, "guard", size=9, color=SLATE)
        x += 20
f.text(14, 98, "frequency", size=9.5, color=SLATE, anchor="start")
f.arrow([(60, 98), (320, 98)], color=SLATE, sw=1)
f.text(14, 124, "TDM: T1 frame = 193 bits = 125 us", size=10.5, color=NAVY, bold=True, anchor="start")
x = 14
f.box(x, 134, 2, 26, "", fill=RED, stroke=RED, r=0, sw=1)
x += 2
for i in range(24):
    f.box(x, 134, 16, 26, "", fill=[BLUE, MINT][i % 2], stroke="#64748b", r=0, sw=0.8)
    x += 16
f.text(14 + 2 + 8, 174, "1", size=9, color=NAVY)
f.text(14 + 2 + 16 * 23 + 8, 174, "24", size=9, color=NAVY)
f.text(14, 174, "F", size=9, color=RED, bold=True, anchor="start")
f.text(14 + 2 + 192, 190, "24 slots x 8 bits + 1 framing bit (F)", size=10, color=SLATE)
f.text(14, 216, "E1 frame = 256 bits = 125 us", size=10.5, color=NAVY, bold=True, anchor="start")
x = 14
for i in range(32):
    sync = i in (0, 16)
    f.box(x, 226, 16, 26, "", fill=SAND if sync else [BLUE, MINT][i % 2], stroke=AMBER if sync else "#64748b", r=0, sw=0.8)
    x += 16
f.text(14 + 8, 266, "0", size=9, color=AMBER, bold=True)
f.text(14 + 16 * 16 + 8, 266, "16", size=9, color=AMBER, bold=True)
f.text(14 + 16 * 31 + 8, 266, "31", size=9, color=NAVY)
f.text(300, 284, "slot 0 sync, slot 16 signalling (amber), 30 voice slots: 2 048 000 bps", size=10, color=SLATE)
f.text(340, 46, "T1: 1 544 000 bps", size=11, color=TEAL, bold=True, anchor="start")
f.text(340, 64, "E1: 2 048 000 bps", size=11, color=RED, bold=True, anchor="start")
f.text(340, 82, "one call: 64 000 bps", size=11, color=NAVY, bold=True, anchor="start")
```

```svgfig label="2.9" caption="Why packet switching wins for bursty traffic, computed with the binomial distribution. A 1 Mbps link and users who each need 100 kbps but are active only 10 percent of the time: circuit switching reserves 100 kbps per user and so serves only 10. With 35 users on a shared packet link the number active at once has mean 35 x 0.1 = 3.5 and standard deviation 1.77; the bars show the probability of exactly k users active, and the red bars (11 or more) add up to 0.00042 = 0.04 percent. So 3.5 times as many users share the link and the link is overloaded for only about 4 minutes in a week of use."
f = Fig(580, 270)
cm = __import__("math")
L, T, W, H = 50, 14, 340, 200
f.box(L, T, W, H, "", fill="#ffffff", stroke="#94a3b8", r=2, sw=1.2)
P = lambda k: cm.comb(35, k) * 0.1 ** k * 0.9 ** (35 - k)
ymax = 0.25
for k in range(0, 6):
    y = T + H - H * k * 0.05 / ymax
    f.line(L, y, L + W, y, color="#e2e8f0", sw=1)
    f.text(L - 6, y, "%.2f" % (k * 0.05), size=9.5, color=SLATE, anchor="end", vmid=True)
bw = W / 16.0
for k in range(16):
    p = P(k)
    h = H * p / ymax
    f.box(L + k * bw + 2, T + H - h, bw - 4, max(h, 0.6), "", fill="#fecaca" if k > 10 else "#bfdbfe", stroke=RED if k > 10 else NAVY, r=0, sw=1)
    f.text(L + k * bw + bw / 2, T + H + 14, str(k), size=9.5, color=SLATE)
f.text(L + W / 2, T + H + 32, "k = users active at the same time (35 users, each active 10 percent of the time)", size=10, color=SLATE, bold=True)
f.line(L + 11 * bw, T, L + 11 * bw, T + H, color=RED, sw=1.6, dash=True)
f.text(L + 11 * bw + 6, T + 22, "11 or more:", size=10, color=RED, bold=True, anchor="start")
f.text(L + 11 * bw + 6, T + 38, "0.00042", size=10, color=RED, bold=True, anchor="start")
f.text(L + 11 * bw + 6, T + 54, "link overloaded", size=9.5, color=RED, anchor="start")
f.text(410, 60, "Circuit switching:", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(410, 78, "1000 / 100 = 10 users", size=10, color=SLATE, anchor="start")
f.text(410, 108, "Packet switching:", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(410, 126, "35 users, P(overload)", size=10, color=SLATE, anchor="start")
f.text(410, 142, "= 0.04 percent", size=10, color=SLATE, anchor="start")
f.text(410, 172, "gain = 35 / 10 = 3.5 x", size=11, color=RED, bold=True, anchor="start")
```

```svgfig label="2.10" caption="Three ways to send a 9000 bit message over three 1 Mbps links, as a timeline (propagation delay ignored). Circuit switching: a 6 ms set-up phase reserves the path, then the message flows through all three links at once for 9 ms: 15 ms, and the circuit stays reserved even in the gaps. Message switching: each node must receive the whole message before forwarding, so the links work one after another: 3 x 9 = 27 ms. Packet switching with three packets of 3000 bits: the links work in a pipeline, (3 links + 3 packets - 1) x 3 ms = 15 ms, with no set-up and no reservation. General rule: packets of L bits over N links of rate R, M packets: (N + M - 1) x L / R."
f = Fig(580, 312)
sx = lambda t: 118 + t * 15.0
for t in range(0, 28, 3):
    f.line(sx(t), 18, sx(t), 290, color="#e2e8f0", sw=1)
    f.text(sx(t), 302, str(t), size=9.5, color=SLATE)
f.text(sx(27) + 4, 302, "ms", size=9.5, color=SLATE, bold=True, anchor="start")
def bar(row, a, b, fl, st, lab=""):
    f.box(sx(a), 26 + row * 24, sx(b) - sx(a), 18, lab, fill=fl, stroke=st, size=9, r=2, sw=1)
def lab(row, s, c=NAVY, bold=False):
    f.text(6, 35 + row * 24, s, size=9.5 if not bold else 10.5, color=c, bold=bold, anchor="start", vmid=True)
lab(0, "Circuit switching", NAVY, True)
lab(1, "set-up"); bar(1, 0, 6, "#f1f5f9", "#64748b", "set-up 6")
lab(2, "links 1,2,3"); bar(2, 6, 15, BLUE, NAVY, "message 9 ms on all")
f.text(sx(15) + 6, 35 + 2 * 24, "15 ms", size=10.5, color=RED, bold=True, anchor="start", vmid=True)
lab(3, "Message switching", NAVY, True)
for i in range(3):
    lab(4 + i, "link %d" % (i + 1)); bar(4 + i, 9 * i, 9 * i + 9, SAND, AMBER, "whole message")
f.text(sx(27) - 40, 35 + 6 * 24 - 0, "", size=9)
f.text(sx(27) + 0, 35 + 6 * 24 + 0, "", size=9)
lab(7, "Packet switching", NAVY, True)
for i in range(3):
    lab(8 + i, "link %d" % (i + 1))
    for p in range(3):
        bar(8 + i, 3 * (i + p), 3 * (i + p) + 3, [MINT, BLUE, SAND][p], [TEAL, NAVY, AMBER][p], "P%d" % (p + 1))
f.text(sx(15) + 6, 35 + 10 * 24, "15 ms", size=10.5, color=RED, bold=True, anchor="start", vmid=True)
f.text(sx(27) + 0, 35 + 4 * 24, "", size=9)
```

```svgfig label="2.11" caption="Satellite orbits to scale (0.0032 px per km) and the delay each causes, computed with signals travelling at 299 792 km/s. A low-earth orbit at 550 km (Starlink class) gives a round trip (up, down, up, down) of 4 x 550 / 299 792 = 7.3 ms; a medium-earth orbit at 8000 km gives 107 ms; a geostationary orbit at 35 786 km gives 477 ms, because the satellite must keep pace with the turning Earth and so sits high above the equator. Real services add processing time: LEO links measure 30-50 ms, GEO links 600 ms or more. Interactive voice wants under about 150 ms one way, which GEO cannot offer."
f = Fig(580, 296)
cx, cy, s = 140, 146, 0.0032
R = 6371
f.circle(cx, cy, 6371 * s, fill="#bfdbfe", stroke=NAVY, sw=1.5)
for alt, nm, col, ang in ((550, "LEO 550 km", TEAL, 215), (8000, "MEO 8000 km", AMBER, 320), (35786, "GEO 35 786 km", RED, 40)):
    r = (R + alt) * s
    f.raw('<circle cx="%d" cy="%d" r="%.1f" fill="none" stroke="%s" stroke-width="1.3" stroke-dasharray="5 3"/>' % (cx, cy, r, col))
    sxp = cx + r * __import__("math").cos(__import__("math").radians(ang)); syp = cy - r * __import__("math").sin(__import__("math").radians(ang))
    f.circle(sxp, syp, 5, fill=col, stroke=col)
    f.text(14, 14 + [550, 8000, 35786].index(alt) * 15, "o  " + nm, size=9.5, color=col, bold=True, anchor="start")
f.text(140, 290, "orbits to scale; Earth radius 6371 km", size=9.5, color=SLATE)
ms = lambda a: 4 * a / 299792.458 * 1000
rows = [("LAN, 100 m", 0.001, SLATE), ("LEO 550 km", ms(550), TEAL), ("MEO 8000 km", ms(8000), AMBER), ("GEO 35 786 km", ms(35786), RED)]
f.text(330, 30, "round-trip propagation delay (ms)", size=10.5, color=NAVY, bold=True, anchor="start")
for i, (nm, v, c) in enumerate(rows):
    y = 52 + i * 38
    f.text(330, y + 10, nm, size=10, color=SLATE, anchor="start", vmid=True)
    w = max(v * 0.36, 1.5)
    f.box(430, y, w, 20, "", fill=c, stroke=c, r=2, sw=1)
    f.text(430 + w + 6, y + 10, "%.1f" % v if v >= 1 else "0.001", size=10, color=c, bold=True, anchor="start", vmid=True)
f.line(430 + 150 * 0.36, 44, 430 + 150 * 0.36, 200, color=NAVY, sw=1.4, dash=True)
f.text(430 + 150 * 0.36, 214, "150 ms", size=9.5, color=NAVY, bold=True)
f.text(330, 240, "voice limit shown at 150 ms", size=9.5, color=NAVY, anchor="start")
```

```svgfig label="2.12" caption="Frequency reuse in a cellular network. The service area is divided into hexagonal cells of radius R. The channels are split into 7 groups, numbered 1 to 7, and no two neighbouring cells use the same group (colouring rule: group = (q + 3r) mod 7 + 1 for the cell at hex coordinates q, r). The nearest cell with the same group lies at distance D = R x sqrt(3 N) = R x sqrt(21) = 4.58 R for cluster size N = 7. With 70 channels in total, each cell gets 10; a city of 49 cells then carries 49 x 10 = 490 calls at once instead of 70, a gain of 7. A smaller cluster (N = 3, D = 3 R) gives more channels per cell but more interference."
f = Fig(580, 290)
cm = __import__("math")
Rr = 21.0
fills = ["#fecaca", "#fde68a", "#bbf7d0", "#bfdbfe", "#e9d5ff", "#fbcfe8", "#a7f3d0"]
cells = {}
for q in range(-6, 7):
    for r in range(-6, 7):
        x = 160 + 1.5 * Rr * q
        y = 140 + cm.sqrt(3) * Rr * (r + q / 2.0)
        if 30 <= x <= 292 and 28 <= y <= 258:
            cells[(q, r)] = (x, y)
for (q, r), (x, y) in cells.items():
    g = (q + 3 * r) % 7
    pts = [(x + Rr * cm.cos(cm.radians(60 * k)), y + Rr * cm.sin(cm.radians(60 * k))) for k in range(6)]
    f.poly(pts, fill=fills[g], stroke="#64748b", sw=1, label=str(g + 1), lx=x, ly=y, size=10, color=NAVY)
(a, b) = cells[(0, 0)], cells[(1, 2)] if (1, 2) in cells else None
if b:
    f.arrow([(a[0], a[1]), (b[0], b[1])], color=RED, sw=2.2, both=True)
    f.text((a[0] + b[0]) / 2 + 36, (a[1] + b[1]) / 2, "D = 4.58 R", size=10.5, color=RED, bold=True, anchor="start")
rows = [("cluster N", "D / R = sqrt(3N)"), ("3", "3.00"), ("4", "3.46"), ("7", "4.58"), ("12", "6.00")]
f.text(340, 40, "cluster size and reuse distance", size=10.5, color=NAVY, bold=True, anchor="start")
for i, (u, v) in enumerate(rows):
    f.text(340, 66 + i * 20, u, size=10, color=NAVY if i == 0 else SLATE, bold=(i == 0), anchor="start")
    f.text(420, 66 + i * 20, v, size=10, color=NAVY if i == 0 else SLATE, bold=(i == 0), anchor="start")
f.text(340, 182, "70 channels, N = 7: 10 per cell", size=10, color=SLATE, anchor="start")
f.text(340, 200, "49 cells x 10 = 490 calls at once", size=10, color=SLATE, anchor="start")
f.text(340, 218, "without reuse: 70 calls in all", size=10, color=SLATE, anchor="start")
f.text(340, 242, "capacity gain = 7 times", size=11, color=RED, bold=True, anchor="start")
```

### 2.9.1 Eight uses of physical-layer technology in Nepal

1. **Optical fibre backbones and fibre to the home.** Internet providers such as WorldLink, Vianet and Subisu bring fibre to homes and offices in the valley and in big towns, and Nepal Telecom runs fibre between cities. Light in glass loses only 0.2 dB per kilometre, so a signal can travel tens of kilometres before it needs a repeater (Fig. 2.6). One fibre can be shared by 32 or 64 homes with a passive splitter, which keeps the cost per family low.
2. **Campus and office LANs on twisted pair.** A college lab connects every computer to a switch with a Cat5e or Cat6 cable of at most 100 metres, wired to the T568B standard (Fig. 2.7). The twist of each pair cancels outside noise, so the cable is cheap and reliable (Plate 2.1c). When the cable run is longer than 100 metres, the right choice is to add a switch or use fibre.
3. **Microwave links to remote places.** Where a road or a fibre trench is too costly, a pair of dishes on two hilltops can carry hundreds of megabits across tens of kilometres (Plate 2.2b). Hill-district health posts, schools and police posts are joined to the network this way. The two dishes must see each other, so the towers are built on ridges.
4. **Mobile data in every district.** Nepal Telecom and Ncell cover towns and many villages with 4G cells, and each base station serves the phones in its cell (Plate 2.2c). The same set of radio channels is reused in cells that are far enough apart (Fig. 2.12), which lets millions of people use ConnectIPS, Fonepay and the Nagarik App at the same time. A phone that moves from one cell to the next is handed over without dropping the call.
5. **ADSL and VDSL on old telephone lines.** In towns, a telephone pair can carry an Internet connection because ADSL uses frequencies above 25 kHz while voice stays below 4 kHz (Plate 2.3a). A DSLAM in the street cabinet puts many such lines on one fibre (Plate 2.3b). The speed falls as the copper gets longer, because the signal loses power and the SNR drops (Fig. 2.1).
6. **Satellite links for the hardest places.** A VSAT dish can give a bank branch, an ATM or a remote school a connection where no cable and no mobile signal reaches. A geostationary link has a round trip of about 477 ms before any processing (Fig. 2.11), so it suits e-mail and payments better than voice calls or games. Low-orbit services reduce that delay to a few tens of milliseconds.
7. **Digital voice and E1 links.** A telephone call is sampled 8000 times a second at 8 bits, giving 64 kbps (Fig. 2.5), and 30 such calls share one E1 line of 2.048 Mbps (Fig. 2.8). Mobile operators use E1 and larger multiplexed links to connect base stations to their exchanges. Knowing the frame structure explains why capacity is bought in units of 2 Mbps.
8. **Wi-Fi that adapts to the signal.** A home router chooses a modulation to match the signal quality: 64-QAM or higher near the router, QPSK farther away (Fig. 2.4). This is Shannon's law at work, since a lower SNR means a lower capacity (Fig. 2.1). It is why the speed test next to the router is much better than the same test in the far bedroom.

## Formula and fact sheet

- Nyquist: C = 2 B log₂ L. Shannon: C = B log₂(1 + SNR); SNR_dB = 10 log₁₀ SNR.
- Bit rate = baud × bits per signal element. PCM voice: 8000 × 8 = 64 kbps.
- T1 = 1.544 Mbps (24 channels), E1 = 2.048 Mbps (30 channels).
- Attenuation (dB) = 10 log₁₀(P₂/P₁); 3 dB ≈ factor 2 in power.
- Switching: circuit (reserve), message (store whole), packet (datagram or virtual circuit).

## Chapter summary

- The physical layer moves raw bits as signals. Impairments are attenuation, distortion and noise.
- Nyquist limits a noiseless channel by bandwidth and levels; Shannon limits a noisy one by bandwidth and SNR.
- Line codes trade bandwidth against clock recovery: Manchester is self-clocking, NRZI and AMI are simpler.
- Fibre outperforms copper in bandwidth, distance and noise immunity; UTP dominates the last 100 m.
- Multiplexing shares a link by frequency, time or wavelength; switching shares a network by circuits or packets, and bursty data favours packets.

## Practice

1. Differentiate between baud rate and bit rate. A signal uses 8 levels at 2400 baud; find the bit rate.
2. Find the Nyquist maximum bit rate of a 3000 Hz noiseless channel with 4 levels.
3. Find the Shannon capacity of a 3000 Hz channel with SNR 30 dB.
4. What is the minimum number of levels to carry 6 Mbps in a noiseless 1 MHz channel?
5. Draw the Manchester and NRZI encodings of 10110010 (state your convention).
6. Why is Manchester coding unsuitable for gigabit Ethernet? What replaces it?
7. Compare UTP, coaxial and fibre for a campus backbone.
8. Four channels of 8 bits per slot at 8000 frames/s are TDM-multiplexed. Find the link rate. What is T1's rate and why does it include one extra bit per frame?
9. Compare circuit switching and packet switching with examples.
10. Why is geostationary satellite delay too high for interactive games?

::: note Answers and worked solutions
**1.** Baud = signal elements per second; bit rate = baud × bits per element. 8 levels = 3 bits, so 2400 × 3 = 7200 bps.
**2.** 2 × 3000 × log₂ 4 = 12,000 bps.
**3.** SNR = 1000, C = 3000 × log₂ 1001 ≈ 29,902 bps.
**4.** 2 × 10⁶ × log₂ L ≥ 6 × 10⁶, so log₂ L ≥ 3 and L = 8 (Shannon at 20 dB allows 6.66 Mbps, so it is feasible).
**5.** Manchester with 1 = low-to-high: 01 10 01 01 10 10 01 10. NRZI starting low with a flip on every 1: + + − + + + − −.
**6.** It needs twice the signal bandwidth of the bit rate (50 % efficiency), which is hard on copper at 1 Gbps; gigabit and faster Ethernet use 8B/10B, PAM-5 or 64B/66B block codes.
**7.** UTP: cheapest, 100 m limit, fine inside buildings. Coax: better shielded, older. Fibre: kilometres, huge bandwidth, no EMI; the right choice between buildings.
**8.** 4 × 8 × 8000 = 256,000 bps. T1: (24 × 8 + 1) × 8000 = 1,544,000 bps; the extra bit per frame is the framing bit used for frame synchronisation.
**9.** Circuit: reserved path, constant delay, wasted when idle (telephone). Packet: shared capacity, queuing delay, efficient for bursts (Internet).
**10.** The orbit is 35,786 km high; a one-way trip ground–satellite–ground takes about 240 ms, so a request and reply take about 480 ms plus processing, far above the 50 ms or so that games tolerate.
:::

## Model answers for Unit 2

**Q1. State the Nyquist and Shannon limits on the data rate of a channel. Compute both for a telephone line and explain how they are used together. (10 marks)**

**Introduction.** The data rate of a channel is not limited by the cleverness of the equipment but by physics. Two results set the limits: Nyquist's theorem for a channel without noise and Shannon's theorem for a channel with noise. Fig. 2.1 draws both for a 3000 Hz line.

**Nyquist (noiseless channel).** A channel of bandwidth B hertz can carry at most 2B signal elements per second without intersymbol interference (Fig. 2.2). If each element can take L levels, it carries log2 L bits, so the maximum bit rate is C = 2 B log2 L.

**Shannon (noisy channel).** Noise makes close levels impossible to tell apart (Fig. 2.4). Shannon proved that the highest rate at which data can be sent with an arbitrarily small error is C = B log2(1 + SNR), where SNR is a power ratio, not decibels. A value in dB must first be converted: SNR = 10^(dB / 10).

**Worked example for B = 3000 Hz.**

| Quantity | Calculation | Result |
|---|---|---|
| Nyquist, 2 levels | 2 x 3000 x log2 2 | 6000 bps |
| Nyquist, 4 levels | 2 x 3000 x log2 4 | 12 000 bps |
| Nyquist, 16 levels | 2 x 3000 x log2 16 | 24 000 bps |
| Shannon, SNR 30 dB (ratio 1000) | 3000 x log2 1001 | 29 902 bps |

**How they are used together.**

1. Shannon gives the ceiling for the channel: 29.9 kbps for this line, whatever coding is used.
2. Nyquist tells how many levels are needed for a target rate below the ceiling. For 24 kbps we need L = 16.
3. The level count must be feasible at the SNR available. L levels need SNR of at least L squared minus 1: 3 for L = 2, 15 for L = 4 and 255 (24.07 dB) for L = 16.
4. To increase the rate, increase B (a wider channel) or SNR (a cleaner line); doubling B doubles C, while doubling SNR adds only about B bits per second.
5. A 56 kbps modem on a 3100 Hz line would need SNR of about 54 dB, which is why real lines gave less.

**Conclusion.** Nyquist limits a channel by its bandwidth and the number of levels, Shannon by its bandwidth and noise. Designers use Shannon to see whether a rate is possible at all, and Nyquist to choose the signalling scheme that reaches it.

**Q2. What is line coding? Explain NRZ-L, NRZI, Manchester and AMI with the waveform of 10110010. (10 marks)**

**Introduction.** **Line coding** converts digital data into a digital signal, a sequence of voltage levels, for transmission over a wire. A good code helps the receiver keep its clock, avoids a DC component, uses little bandwidth and, if possible, detects some errors.

**Requirements of a good code.**

1. **Synchronisation:** the receiver has no separate clock wire, so it needs level changes in the data to stay in step.
2. **No DC component:** a long-term average of zero lets transformers and capacitors in the link pass the signal.
3. **Low bandwidth:** fewer changes per bit use less of the channel.
4. **Error detection:** a rule that is broken by a single error, such as the alternation in AMI.

**The four codes (Fig. 2.3).**

| Code | Rule | Waveform for 10110010 | Strength | Weakness |
|---|---|---|---|---|
| NRZ-L | 1 is high, 0 is low | high, low, high, high, low, low, high, low | simple, uses least bandwidth | long runs of equal bits lose the clock |
| NRZI | a 1 flips the level, a 0 keeps it | + + - + + + - - (start low) | runs of 1s are safe | runs of 0s still lose the clock |
| Manchester | 1 is low then high, 0 is high then low | 01 10 01 01 10 10 01 10 | transition in every bit, self-clocking, no DC | needs twice the bandwidth |
| AMI | 0 is zero volts, 1s alternate +V and -V | + 0 - + 0 0 - 0 | no DC, single errors detected | long runs of 0s lose the clock |

**Where they are used.** Manchester coding was used by 10 Mbps Ethernet. Faster Ethernet avoids its 50 percent efficiency with block codes: 4B/5B (80 percent), 8B/10B and 64B/66B. AMI, with a scrambling rule, was used on T1 lines.

**Checking the Manchester row.** Take the bits 1, 0, 1, 1. Bit 1 becomes low-high (01), bit 0 becomes high-low (10), and the next two 1s become 01 and 01, so the line reads 01 10 01 01. The signal changes level at least once in every bit period, even for the string 00000000, which is exactly what a receiver needs to stay locked. The price is that the signal changes up to twice per bit, so a 10 Mbps stream needs about 20 MHz of bandwidth.

**Conclusion.** Line codes trade bandwidth against clock recovery. Manchester is the most robust but the most costly, NRZ-L the cheapest but the weakest in synchronisation, and the others sit between.

**Q3. Compare the guided and unguided transmission media. Which medium would you choose for a college campus, and why? (10 marks)**

**Introduction.** A **transmission medium** is the path that carries the signal. **Guided** media (twisted pair, coaxial cable, optical fibre) keep the signal in a physical conductor; **unguided** media (radio, microwave, infrared, satellite) send it through the air. The choice depends on distance, speed, cost and noise.

**Guided media.**

1. **Twisted pair (UTP, STP).** Pairs are twisted so that noise cancels (Plate 2.1c). Cat5e and Cat6 carry 1 Gbps up to 100 m and cost little.
2. **Coaxial cable.** A copper core inside a braid shield resists noise better and was the bus of early Ethernet.
3. **Optical fibre.** Light stays in the core by total internal reflection (Fig. 2.6). Fibre has very high bandwidth, loses 0.2 dB per km, is immune to electrical noise and cannot be tapped easily, but splicing needs skill (Plate 2.1d).

**Unguided media.** Radio waves cover people on the move (Wi-Fi, mobile networks); microwave dishes join towers on a straight line of sight (Plate 2.2b); satellites reach anywhere but with a long delay (Fig. 2.11).

| Medium | Typical reach | Speed | Cost | Noise immunity | Use |
|---|---|---|---|---|---|
| UTP Cat6 | 100 m | up to 10 Gbps (short runs) | low | fair | rooms, floors |
| Coaxial | 500 m | up to 1 Gbps (cable TV) | medium | good | cable broadband |
| Single-mode fibre | tens of km | 100 Gbps and more | high | excellent | backbone |
| Microwave | 30-50 km | 100 Mbps - 1 Gbps | medium | fair (weather) | hills, no fibre |
| Satellite | global | 10-300 Mbps | high | fair | remote areas |

**Recommendation for a campus.** Use **fibre between buildings** because the distance exceeds 100 m and lightning or earth-potential differences cannot travel along glass. Use **Cat6 UTP** inside each building from a floor switch to the rooms, and **Wi-Fi** for mobile devices. A microwave link is only a backup.

**Conclusion.** There is no best medium, only the best medium for a distance and a budget. A campus uses a mixture: fibre for the backbone, copper for the last 100 metres and radio for convenience.

**Q4. Explain frequency-division, time-division and wavelength-division multiplexing with examples. (5 marks)**

**Multiplexing** lets many signals share one link. The link is divided in one of three ways.

1. **FDM** gives each channel its own band of frequencies. Three 4 kHz voice channels with two 1 kHz guard bands need 3 x 4 + 2 x 1 = 14 kHz (Fig. 2.8). Radio, TV and the cable-TV network use FDM.
2. **TDM** gives each channel the whole link for a short, fixed time slot in turn. One frame lasts 125 microseconds. A T1 frame has 24 slots of 8 bits plus 1 framing bit: 193 x 8000 = 1 544 000 bps. An E1 frame has 32 slots: 2 048 000 bps, of which 30 slots carry voice.
3. **WDM** is FDM for light: each channel is a different colour of laser on the same fibre. Dense WDM carries 80 or more wavelengths, each at 100 Gbps.
4. **Statistical TDM** gives a slot only to a channel that has data, which suits bursty traffic (Fig. 2.9).

For example, a voice call is exactly one slot of an E1 line (64 kbps), and the E1 line is one channel on a fibre that carries many colours.

**Q5. Compare circuit switching and packet switching. Show with a calculation which is faster for a 9000 bit message over three links. (10 marks)**

**Introduction.** A large network cannot join every pair of nodes directly, so intermediate nodes **switch** the data. The main methods are circuit switching, message switching and packet switching (datagram or virtual circuit).

**Circuit switching.** A dedicated path is set up for the call, used by it alone, and released at the end. The old telephone network works like this (Plate 2.3c).

**Packet switching.** The message is cut into packets, each with an address, and every node stores a packet and forwards it. Capacity is shared on demand. The Internet works like this.

**Calculation (Fig. 2.10).** Take a 9000 bit message, three links of 1 Mbps and no propagation delay.

1. **Message switching:** each link must send all 9000 bits before the next starts: 3 x 9 = 27 ms.
2. **Packet switching:** three packets of 3000 bits (3 ms each) pipeline through the links: (3 + 3 - 1) x 3 = 15 ms.
3. **Circuit switching:** a 6 ms set-up, then 9 ms on all links at once = 15 ms, but the circuit is reserved for the whole time.

**Comparison.**

| Point | Circuit switching | Packet switching |
|---|---|---|
| Set-up | needed before data | none (datagram) |
| Path | fixed for the call | may change per packet |
| Capacity | reserved, wasted when idle | shared, used on demand |
| Delay | constant after set-up | varies with queues |
| Failure | call is lost if a node fails | packets take another route |
| Best for | steady voice | bursty data |

**Statistical gain.** If 35 users each need 100 kbps for 10 percent of the time on a 1 Mbps link, circuit switching serves 10 users but packet switching serves all 35 and overloads the link only 0.04 percent of the time (Fig. 2.9).

**Virtual circuits.** A third style sits between the two: a virtual circuit sets up a route once, then sends packets along it with a short circuit number instead of a full address, as MPLS does in an ISP core. It keeps packet order and gives a predictable route without reserving the capacity of the links.

**Conclusion.** Circuit switching guarantees quality but wastes capacity. Packet switching uses capacity well and survives faults, at the price of variable delay. This is why the Internet is packet switched.

**Q6. Explain pulse code modulation. How is the 64 kbps rate of a voice channel obtained? (5 marks)**

**PCM** converts an analog voice signal into a digital one in three steps (Fig. 2.5).

1. **Sampling.** Voice is limited to about 4 kHz. By Nyquist's sampling theorem it must be sampled at twice the highest frequency: 2 x 4000 = 8000 samples per second, one every 125 microseconds.
2. **Quantisation.** Each sample is rounded to the nearest of 2^n levels. The rounding error is quantisation noise, and each extra bit adds about 6 dB to the SNR (8 bits give about 49.9 dB).
3. **Encoding.** Each level is sent as an n-bit code word.

With 8 bits per sample the bit rate is 8000 x 8 = **64 000 bps**, the DS0 channel. Thirty-two such channels fill the 2.048 Mbps E1 frame (Fig. 2.8). The quality of the received voice depends on the number of bits: 3 bits would sound harsh, 8 bits sound natural. In practice the levels are spaced non-uniformly (A-law in Europe and Nepal, mu-law in North America) so that quiet sounds are described more finely than loud ones.

**Q7. Explain the cellular concept and frequency reuse. (5 marks)**

A mobile network divides its area into **cells**, each served by a base station with a low-power transmitter (Plate 2.2c). Because power is low, a frequency used in one cell can be used again in another cell far enough away.

1. **Cluster.** The available channels are split into N groups (commonly 7) and a cluster of N neighbouring cells uses each group once, with no two adjacent cells sharing a group (Fig. 2.12).
2. **Reuse distance.** The nearest cell with the same group is at D = R x sqrt(3N); for N = 7 this is 4.58 R, which keeps co-channel interference low.
3. **Capacity gain.** With 70 channels and N = 7, each cell has 10, but a city of 49 cells carries 490 calls at once, seven times the 70 calls possible without reuse.
4. **Handoff.** When a phone moves toward the cell edge and the signal falls, the network switches the call to the next base station without a break.
5. **Trade-off.** A smaller N gives more channels per cell but a smaller D and more interference; a smaller cell radius gives more capacity per area but needs more towers.

This is how Nepal Telecom and Ncell serve millions of subscribers with a limited share of the radio spectrum.
