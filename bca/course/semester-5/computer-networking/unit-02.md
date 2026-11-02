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
