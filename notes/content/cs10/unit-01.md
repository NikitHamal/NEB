---
subject: Computer Science
grade: 10
unit: 1
title: Computer Network and Communication
hours: 14
---

When you send a video to a friend in Dharan, pay a bill with eSewa or join an
online class, your data crosses several networks in less than a second. This
unit explains how that happens: how signals travel through cables and through
the air, which devices pass them along, how computers are arranged and given
addresses, and how the Internet differs from the private networks inside
schools and companies. Almost everything here is asked as a definition, a
difference or a diagram, so learn the tables as carefully as the text.

::: key What the SEE asks from this unit (11 marks)
In the CDC specification grid this unit carries **11 of the 50 marks**: **three
MCQs** (3 marks), **two short questions** (2 × 2 = 4 marks) and **one long
question** (4 marks). The MCQs test single facts: a full form, which device or
command does what, the length of an IPv4 address. Short questions want a
definition with an example, or two clear differences (bandwidth and throughput,
guided and unguided media, Internet and intranet). The long question is either
"types of broadband / topologies / networks, with features", or a scenario:
plan the network for a school, a home or an office and justify each device.
The marker gives **one mark for each correct key point**, so write points, not
paragraphs.
:::

## 1.1 Concept of telecommunication

::: definition Telecommunication
**Telecommunication** is the sending and receiving of information — voice,
text, pictures, video or computer data — over a distance by electronic means:
electrical signals in wires, radio waves through the air, or light in optical
fibre. The word joins the Greek *tele* (far) and the Latin *communicare* (to
share), so it means "sharing from far away".
:::

Every telecommunication link, from a landline call to a 4G video stream, has the
same five parts.

| Component | Meaning | Example: sending a photo on Viber |
|---|---|---|
| Sender (source) | the device that creates and sends the message | your phone |
| Message | the information being sent | the photo |
| Medium (channel) | the path the signal travels along | Wi-Fi, then optical fibre, then the mobile network |
| Receiver | the device that accepts the message | your friend's phone |
| Protocol | the rules both sides follow | TCP/IP and the app's own rules |

When devices are joined so that they can exchange data in this way, they form a
**network**. The rest of this section defines the words used to describe how
fast and how well such a link works.

### Bandwidth

::: definition Bandwidth
**Bandwidth** is the maximum amount of data a communication link can carry in
one second. It is a property of the link — the cable, the radio channel or the
plan you buy from an Internet Service Provider (ISP) — in the same way that the
number of lanes is a property of a highway.
:::

Bandwidth is measured in **bits per second**. In networking the prefixes are
decimal, the small letter **b** means *bit*, and the capital **B** means
*byte* (1 byte = 8 bits).

| Unit | Full form | Value |
|---|---|---|
| bps | bits per second | 1 bit each second |
| kbps | kilobits per second | 1,000 bps |
| Mbps | megabits per second | 1,000,000 bps |
| Gbps | gigabits per second | 1,000,000,000 bps |

Radio engineers also use "bandwidth" for the *width of a frequency band* in
hertz: a Wi-Fi channel, for example, is 20 MHz wide. A wider band can carry
more bits per second, which is why the two meanings share one word.

### Throughput

::: definition Throughput
**Throughput** is the amount of data actually delivered successfully in one
second. It is what an Internet speed test measures, in the same units as
bandwidth.
:::

Throughput can never be more than the bandwidth, and it is usually less,
because of

- many users sharing the same link at the same time (congestion);
- distance, walls and interference that weaken a wireless signal;
- damaged data that has to be sent again;
- the extra address information that travels with every packet of data.

A third measure, **latency** (delay), is the time a piece of data takes to
reach the other end, in milliseconds (ms). For video calls and online games a
low latency matters as much as a high throughput.

| Bandwidth | Throughput |
|---|---|
| maximum possible data rate of a link | data rate actually achieved |
| fixed by the cable, channel or plan | changes from moment to moment |
| does not depend on how busy the link is | falls when the link is busy or the signal is weak |
| like the number of lanes on a highway | like the number of vehicles that actually pass in a minute |
| example: a 50 Mbps fibre plan | example: a speed test that reads 42 Mbps |

::: caution Mbps is not MBps
A "100 Mbps" plan is 100 mega**bits** per second, but a download window shows
mega**bytes** per second. Divide by 8: a perfect 100 Mbps link delivers at most
12.5 MB per second. Forgetting the factor of 8 is the commonest mistake in
transfer-time questions.
:::

::: example Worked example 1.1 — how long will the download take?
**Problem.** A school buys a 40 Mbps fibre connection. (a) What is the shortest
possible time to download a 750 MB video? (b) A speed test shows that the real
throughput is 32 Mbps. How long does the download actually take, and what
percentage of the bandwidth is being achieved? (Take 1 MB = 1,000,000 bytes, as
network calculations do.)

**Solution.** First change the file size into bits:
750 MB × 8 = 6,000 Mb (megabits).

(a) Time = data ÷ rate = 6,000 Mb ÷ 40 Mbps = **150 s**, that is 2 minutes 30
seconds.

(b) Time = 6,000 ÷ 32 = **187.5 s**, that is 3 minutes 7.5 seconds.
Percentage achieved = 32 ÷ 40 × 100% = **80%**.
:::

::: example Worked example 1.2 — measuring throughput
**Problem.** A student copies a 180 MB file from the school server in exactly
one minute. Find the throughput.

**Solution.** 180 MB × 8 = 1,440 Mb. Throughput = 1,440 Mb ÷ 60 s =
**24 Mbps**.
:::

### Broadband

::: definition Broadband
**Broadband** is a high-speed Internet connection that is always on and carries
a large amount of data at once.
:::

Before broadband, homes used **dial-up**: a modem dialled a telephone number
before every session, reached at most 56 kbps and kept the telephone line busy.
Broadband is hundreds of times faster, stays connected, and leaves the
telephone free.

| Type | Medium | Main features | Typical use |
|---|---|---|---|
| DSL (Digital Subscriber Line) | ordinary copper telephone line | moderate speed that falls with distance from the telephone exchange; phone and Internet work together | older home connections |
| Cable | coaxial cable of a cable-TV network | faster than DSL; neighbours on one line share the speed | homes already wired for cable TV |
| Fibre (FTTH: fibre to the home) | optical fibre right into the building | the fastest and most stable; hundreds of Mbps or more; immune to electrical noise | the usual home and office connection in Nepal's towns today |
| Satellite | radio link through a satellite | works anywhere with a clear view of the sky; long delay; heavy rain can interrupt it | remote villages, ships, aircraft |
| Wireless (mobile) | radio: 4G, 5G, fixed wireless | no cable needed; speed depends on signal strength and the number of users | phones, MiFi devices, places without cables |

### Mobile generations: 3G, 4G and 5G

A **generation** ("G") is a major new version of mobile-phone technology,
arriving roughly once every ten years. 1G (1980s) carried analogue voice and 2G
(1990s) added digital voice and SMS. The three that matter now are:

| | 3G | 4G (LTE) | 5G |
|---|---|---|---|
| First commercial service | Japan, 2001 | Sweden and Norway, 2009 | South Korea and USA, 2019 |
| ITU target peak speed | at least 2 Mbps (stationary) | 1 Gbps stationary, 100 Mbps moving | 20 Gbps download |
| Delay (latency) | high | low | very low (designed for about 1 ms) |
| What it made possible | mobile web browsing, picture messages, video calls | HD video streaming, online classes, cloud apps, calls over data (VoLTE) | augmented and virtual reality, self-driving cars, millions of IoT sensors |
| In Nepal | widely available | Nepal Telecom from 1 January 2017, Ncell from 1 June 2017 | tested by Nepal Telecom; commercial launch still awaited in 2026 |

4G gave Nepal fast mobile Internet in every province. 5G is faster still, has
almost no delay and can serve a very large number of devices in a small area,
which is what smart cities and the Internet of Things (Unit 5) need.

### Data packets

::: definition Data packet
A **data packet** is a small unit of data into which a large message is broken
before it is sent across a network. Each packet travels separately and the
packets are put back together at the destination.
:::

Every packet has three parts:

| Part | Contains |
|---|---|
| Header | source (sender's) address, destination (receiver's) address, packet number, protocol information |
| Payload | one piece of the actual message — on an Ethernet LAN at most about 1,500 bytes |
| Trailer | an error-checking code so the receiver can detect a damaged packet |

Sending data this way is called **packet switching**. The packets may take
different routes and arrive out of order; the receiver uses the packet numbers
to rebuild the message and asks again for any packet that is missing or
damaged. Because the link is shared packet by packet, many users can use it at
once, a broken route affects only a few packets, and long-distance transfer
becomes fast and reliable.

::: example Worked example 1.3 — how many packets?
**Problem.** A 3 MB photo (3,000,000 bytes) is sent in packets that each carry
1,460 bytes of data. How many packets are needed, and how much data is in the
last one?

**Solution.** 3,000,000 ÷ 1,460 = 2,054.79…, so 2,054 full packets are not
enough and **2,055 packets** are needed. The first 2,054 carry
2,054 × 1,460 = 2,998,840 bytes, so the last packet carries
3,000,000 − 2,998,840 = **1,160 bytes**.
:::

### Frequency

::: definition Frequency
The **frequency** of a signal is the number of complete waves (cycles) it makes
in one second. It is measured in **hertz (Hz)**: 1 kHz = 1,000 Hz,
1 MHz = 1,000,000 Hz and 1 GHz = 1,000,000,000 Hz.
:::

::: caution Frequency is not "how often data is sent"
The textbook describes frequency as "how often data signals are sent over a
channel in one second". That is not quite right. Frequency belongs to the
**wave** that carries the data (a 2.4 GHz Wi-Fi wave vibrates 2.4 billion times
a second). How many *bits* are sent each second is the **data rate**, measured
in bps.
:::

Frequency decides how a signal behaves. A higher frequency has a shorter
wavelength, can carry more data, but has a shorter range and is stopped more
easily by walls and rain. A lower frequency travels farther and passes through
walls better but carries less data. This is why 5 GHz Wi-Fi is faster than
2.4 GHz Wi-Fi in the same room but weaker one floor up.

| Technology | Frequency | Use |
|---|---|---|
| AM (medium-wave) radio | 531–1602 kHz in Asia | long-distance radio |
| FM radio | 88–108 MHz | every FM station in Nepal |
| RFID cards and NFC | 13.56 MHz | ID cards, tap-to-pay cards |
| RFID stock tags | 860–960 MHz | tracking goods in shops and warehouses |
| 4G mobile in Nepal | 900 and 1800 MHz bands | Nepal Telecom's first 4G (2017) used 1800 MHz |
| Wi-Fi | 2.4 GHz and 5 GHz (6 GHz in Wi-Fi 6E and 7) | wireless LAN at home and school |
| Bluetooth | 2.4–2.4835 GHz | earbuds, speakers, smartwatches |
| Microwave oven | 2.45 GHz | heating food (not communication) |
| 5G millimetre wave | about 24–71 GHz | very fast 5G over very short distances |

::: example Worked example 1.4 — frequency and wavelength
**Problem.** Radio waves travel at $c = 3\times10^8$ m/s. Find the wavelength
of (a) 2.4 GHz Wi-Fi, (b) 5 GHz Wi-Fi and (c) an FM station at 100 MHz. Which
Wi-Fi band reaches better through walls?

**Solution.** Wavelength $\lambda = \frac{c}{f}$.

(a) $\lambda = \frac{3\times10^8}{2.4\times10^9} = 0.125$ m = **12.5 cm**.

(b) $\lambda = \frac{3\times10^8}{5\times10^9} = 0.06$ m = **6 cm**.

(c) $\lambda = \frac{3\times10^8}{1\times10^8} = $ **3 m**.

The 2.4 GHz band, with the longer wave, passes through walls and floors better
and reaches farther; the 5 GHz band carries more data over a shorter range.
:::

### Communication modes

**Data communication** is the exchange of data between two devices over a
medium. According to the direction in which data can flow, there are three
**modes of communication**.

```figure caption="The three modes of communication. In half duplex the second arrow is dashed because it can be used only when the first is idle; in full duplex both arrows carry data at the same moment."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.9, 2.9))
def dev(x, y, t):
    ax.add_patch(FancyBboxPatch((x - 0.5, y - 0.3), 1.0, 0.6,
                 boxstyle="round,pad=0.02,rounding_size=0.08",
                 fc="#eef4fa", ec=ACCENT, lw=1.1))
    ax.text(x, y, t, ha="center", va="center", fontsize=8.4, color=INK)
rows = [("Simplex", "radio and TV broadcast;\nkeyboard to computer", "one direction only"),
        ("Half duplex", "walkie-talkie", "both ways, but one at a time"),
        ("Full duplex", "phone call, video call", "both ways at the same time")]
ys = [2.6, 1.45, 0.3]
for (name, ex, rule), y in zip(rows, ys):
    ax.text(0.0, y + 0.14, name, ha="left", va="center", fontsize=9,
            fontweight="bold", color=INK)
    ax.text(0.0, y - 0.16, ex, ha="left", va="top", fontsize=7.2,
            color=MUTED, linespacing=1.2)
    dev(3.55, y, "A")
    dev(7.45, y, "B")
    ax.text(5.5, y + 0.36, rule, ha="center", va="bottom", fontsize=7.4, color=INK)
ax.annotate("", xy=(6.9, 2.6), xytext=(4.1, 2.6),
            arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.6, mutation_scale=12))
ax.annotate("", xy=(6.9, 1.55), xytext=(4.1, 1.55),
            arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.6, mutation_scale=12))
ax.annotate("", xy=(4.1, 1.33), xytext=(6.9, 1.33),
            arrowprops=dict(arrowstyle="-|>", color="#9aa3af", lw=1.4, ls="--",
                            mutation_scale=12))
ax.text(5.5, 1.13, "(waits for its turn)", ha="center", va="top", fontsize=6.8, color=MUTED)
ax.annotate("", xy=(6.9, 0.4), xytext=(4.1, 0.4),
            arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.6, mutation_scale=12))
ax.annotate("", xy=(4.1, 0.2), xytext=(6.9, 0.2),
            arrowprops=dict(arrowstyle="-|>", color=SERIES[1], lw=1.6, mutation_scale=12))
ax.set_xlim(-0.05, 8.05); ax.set_ylim(-0.3, 3.25); ax.axis("off")
```

| Mode | Direction of data | Can both sides send? | Examples |
|---|---|---|---|
| Simplex | one way only (unidirectional) | no — the receiver can never reply | radio and TV broadcasting, keyboard to computer, a loudspeaker announcement |
| Half duplex | both ways, one way at a time | yes, but they take turns | walkie-talkie, police wireless handset |
| Full duplex | both ways at the same time (bidirectional) | yes, together | mobile or landline phone call, video call, a switch port |

::: tip Write the example with the mode
"Half duplex — both directions but one at a time, e.g. walkie-talkie" earns
both marks of a 2-mark answer. A definition without an example usually earns
only one.
:::

## 1.2 Communication media: guided and unguided

::: definition Communication media
**Communication media** (also called **transmission media**) are the paths
through which signals travel from the sender to the receiver. They are of two
types: **guided (wired or bounded)** media, which carry the signal along a
cable, and **unguided (wireless or unbounded)** media, which carry it through
air or space without a cable.
:::

### Guided media

**1. Twisted-pair cable.** Pairs of insulated copper wires are twisted around
each other. The twisting cancels much of the electrical interference that one
pair picks up from its neighbours and from outside. **UTP** (unshielded twisted
pair) is used in almost every LAN; **STP** (shielded twisted pair) adds a foil
screen for electrically noisy places such as factories. Telephone lines also
use twisted pairs. Twisted-pair cables are sold in **categories**:

| Category | Speed | Frequency rating | Note |
|---|---|---|---|
| CAT5e | 1 Gbps up to 100 m | 100 MHz | older LANs |
| **CAT6** | 1 Gbps up to 100 m; 10 Gbps up to about 55 m | 250 MHz | tighter twists, better insulation and often a plastic spline between the pairs, so less interference |
| CAT6A | 10 Gbps up to 100 m | 500 MHz | data centres and new buildings |

A single run of twisted-pair Ethernet cable may be at most **100 m** long.

**2. Coaxial cable.** A single copper core is surrounded by an insulating
layer, a braided copper **shield** and an outer plastic jacket. Because the
shield surrounds the core on every side, coaxial cable resists interference
well. It is used for cable TV, for CCTV cameras, to connect dish antennas, and
in older Ethernet networks.

**3. Optical fibre cable.** A hair-thin **core** of very pure glass (or
plastic) is surrounded by glass **cladding** that bends light less strongly.
Light pulses sent into the core strike the boundary at a shallow angle and are
reflected back every time (*total internal reflection*), so the light stays in
the core even when the cable curves. A **buffer coating**, **strength fibres**
and a **jacket** protect the glass. Light travels in glass at about
200,000 km/s, two-thirds of its speed in a vacuum.

**Single-mode** fibre has a very thin core (about 9 µm) and a laser source and
carries data for tens of kilometres; ISPs use it for their main lines.
**Multimode** fibre has a thicker core (50 or 62.5 µm), uses cheaper light
sources and serves shorter links inside buildings and campuses. Most of
Nepal's Internet traffic enters the country through fibre links from India,
and since 12 January 2018 also from China through the Rasuwagadhi–Kerung
border.

```figure caption="Inside the three guided media, drawn with each layer cut back to show the one beneath. The twisted pair and the coaxial cable carry electrical signals in copper; the optical fibre carries light in its glass core."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0, 3.4))
def layer(x0, x1, yc, h, fc, hatch=None):
    ax.add_patch(Rectangle((x0, yc - h / 2), x1 - x0, h, fc=fc, ec=INK, lw=0.8,
                           hatch=hatch, zorder=2))
def up(x, yc, h, t, dx=0.0):
    ax.annotate(t, xy=(x, yc + h / 2), xytext=(x + dx, yc + 0.48), fontsize=7.0,
                color=INK, ha="center", va="bottom",
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
def down(x, yc, h, t, dx=0.0):
    ax.annotate(t, xy=(x, yc - h / 2), xytext=(x + dx, yc - 0.48), fontsize=7.0,
                color=INK, ha="center", va="top",
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
y = 3.12
layer(1.0, 4.4, y, 0.56, "#c9d7e8")
t = np.linspace(4.4, 9.6, 500)
for off, c1, c2 in [(0.13, "#d9771e", "#f3c99a"), (-0.13, "#2e8b57", "#a9dcbf")]:
    w = 0.075 * np.sin(2 * np.pi * (t - 4.4) / 0.8)
    ax.plot(t, y + off + w, color=c1, lw=2.4, zorder=3, solid_capstyle="round")
    ax.plot(t, y + off - w, color=c2, lw=2.4, zorder=3, solid_capstyle="round")
up(2.7, y, 0.56, "outer jacket")
up(7.0, y, 0.40, "copper wires twisted in pairs\n(4 pairs in a CAT6 cable)")
ax.text(0.85, y, "Twisted\npair", ha="right", va="center", fontsize=8.2,
        fontweight="bold", color=INK, linespacing=1.15)
y = 1.88
layer(1.0, 3.8, y, 0.56, "#4a5059")
layer(3.8, 5.6, y, 0.46, "#b8bec7", hatch="xxxx")
layer(5.6, 7.6, y, 0.34, "white")
layer(7.6, 9.6, y, 0.10, "#c87533")
up(2.4, y, 0.56, "plastic jacket")
down(4.6, y, 0.46, "braided copper shield")
up(6.6, y, 0.34, "insulator (dielectric)", dx=-0.45)
up(8.6, y, 0.10, "copper core", dx=0.4)
ax.text(0.85, y, "Coaxial", ha="right", va="center", fontsize=8.2,
        fontweight="bold", color=INK)
y = 0.32
layer(1.0, 3.1, y, 0.50, "#f2cf3d")
layer(3.1, 4.9, y, 0.40, "#fbf0c2")
tt = np.linspace(3.1, 4.9, 200)
for k in (-0.1, 0.0, 0.1):
    ax.plot(tt, y + k + 0.025 * np.sin(2 * np.pi * (tt - 3.1) / 0.35),
            color="#c9a227", lw=0.8, zorder=3)
layer(4.9, 6.5, y, 0.26, "#e6e8ec")
layer(6.5, 8.1, y, 0.15, "#cfe3f6")
layer(8.1, 9.6, y, 0.05, ACCENT)
up(2.05, y, 0.50, "outer jacket")
down(4.0, y, 0.40, "strength fibres")
up(5.7, y, 0.26, "buffer coating")
down(7.3, y, 0.15, "cladding (glass)")
up(8.95, y, 0.05, "core (glass)\ncarries the light", dx=0.15)
ax.text(0.85, y, "Optical\nfibre", ha="right", va="center", fontsize=8.2,
        fontweight="bold", color=INK, linespacing=1.15)
ax.set_xlim(-0.55, 9.75); ax.set_ylim(-0.42, 3.95); ax.axis("off")
```

| Feature | Twisted pair (CAT6) | Coaxial | Optical fibre |
|---|---|---|---|
| Signal carried | electrical | electrical | light |
| Conductor | 4 pairs of copper wires | one copper core | glass or plastic core |
| Typical speed | up to 1 Gbps (10 Gbps on short runs) | hundreds of Mbps | 10 Gbps and far beyond |
| Distance without a repeater | 100 m | a few hundred metres | tens of kilometres |
| Interference | some, reduced by twisting | low, blocked by the shield | none — light ignores electrical noise and lightning |
| Cost and handling | cheapest, easy to fit | moderate | most expensive; needs special tools to join |
| Connector | RJ-45 | BNC, F-type | ST, SC, LC, SMA |
| Typical use | LAN cabling, telephone lines | cable TV, CCTV | ISP backbones, FTTH, links between buildings |

### Unguided media

Unguided media send **electromagnetic waves** through air or space, so no cable
is needed. They are what make mobile phones, Wi-Fi and satellite TV possible.
Because every wireless user shares the same airwaves, the government regulates
who may use which frequency; Nepal's mobile operators, for example, use
frequencies licensed through the **Nepal Telecommunications Authority (NTA)**.

**1. Radio waves** (roughly 3 kHz to 1 GHz) spread out in all directions, pass
through walls and travel long distances. AM and FM radio, mobile phones and
walkie-talkies use them.

**2. Microwaves** (roughly 1 to 300 GHz) travel in straight lines, so the
sending and receiving dish antennas must be in **line of sight**. Towers on
hilltops relay microwave signals over hops of a few tens of kilometres, which
made them useful in Nepal's hills where laying cable is hard. Heavy rain can
weaken them.

**3. Infrared** waves carry data only a few metres, need a clear line of sight
and cannot pass through walls. A TV remote control is the everyday example;
because infrared stays inside one room, it is also hard to eavesdrop on.

**4. Satellite communication** uses an artificial satellite as a microwave
relay station in space. A ground station sends the signal up — the
**uplink** — and the satellite sends it back down to a wide area — the
**downlink** — on a different frequency. A **geostationary** satellite,
35,786 km above the equator, turns with the Earth and appears fixed in the sky,
so dish antennas never need to move. The first commercial communications
satellite, *Early Bird* (Intelsat I), went into service in 1965. Satellites
carry direct-to-home (DTH) television, weather images, GPS navigation and
Internet to remote areas, but because the signal travels about 72,000 km up and
down, each one-way trip takes about a quarter of a second. Nepal's own first
satellite, the small research satellite NepaliSat-1, was launched in 2019.

**5. Wi-Fi** (Wireless Fidelity, the IEEE 802.11 standards) connects devices to
a LAN by radio in the 2.4 GHz and 5 GHz bands, usually over 30–50 m indoors.
A **router** or **access point** sends and receives the signals. Modern Wi-Fi
uses **channel bonding** (joining two neighbouring channels into one wider,
faster channel) and **beamforming** (aiming the signal towards each device
instead of spreading it equally everywhere). A WPA2 or WPA3 password encrypts
the data in the air.

**6. Bluetooth** connects devices over about 10 m using very little power, in
the 2.4 GHz band. It uses **frequency hopping spread spectrum (FHSS)**: the
connection jumps between 79 narrow channels about 1,600 times a second, so
interference on one channel spoils only a tiny part of the data. Earbuds,
keyboards, smartwatches and car audio systems use it.

**7. RFID (Radio Frequency Identification)** uses radio waves to read data
stored in a small **tag** fixed to an object. A **passive** tag has no battery
and is powered by the reader's own signal, so it works only close to the
reader; an **active** tag has a battery and can be read from much farther away.
Library books, ID cards, contactless payment cards, toll gates and warehouse
stock all use RFID.

| Guided media | Unguided media |
|---|---|
| signals travel along a physical cable | signals travel through air or space as electromagnetic waves |
| also called wired or bounded media | also called wireless or unbounded media |
| the cable gives a fixed path | no fixed path; the signal spreads out |
| little affected by weather | rain, walls and distance weaken the signal |
| more secure: a person must reach the cable to tap it | easier to intercept, so encryption is needed |
| devices cannot move freely | devices can move (mobility) |
| examples: twisted pair, coaxial, optical fibre | examples: radio, microwave, infrared, satellite, Wi-Fi, Bluetooth |

::: caution Distance is not the difference
The textbook's table says guided media connect "close devices" and unguided
media connect "devices far away". Both claims break easily: an optical fibre
crosses whole countries, while infrared and Bluetooth reach only a few metres.
In a "differences" answer use the points in the table above instead.
:::

## 1.3 Connectors: RJ-45, RJ-11, BNC, fibre connectors and the media converter

::: definition Connector
A **connector** is the plug or socket at the end of a cable that joins the
communication medium to the port of a device such as a computer, switch or
router, keeping each wire (or the glass fibre) exactly in place.
:::

**RJ-45 (Registered Jack 45).** The clear plastic plug on every Ethernet cable.
It has **eight positions and eight contacts** (8P8C), one for each of the eight
wires of a twisted-pair cable, and a springy clip that locks it into the port.
The order of the coloured wires follows the standard **T568A** or **T568B**.

```photo id="cs10/rj45-pins" caption="An RJ-45 (8P8C) plug. Each of the eight gold contacts, numbered 1 to 8 in the photograph, presses on one of the eight wires of the twisted-pair cable when the plug is crimped." width="58"
```

**RJ-11.** The smaller plug of a **telephone** cable. It has six positions but
usually only two or four contacts. It connects telephones and DSL modems to the
phone line. An RJ-11 plug fits loosely into an RJ-45 port, but it is the wrong
connector for Ethernet.

**BNC (Bayonet Neill–Concelman).** A round metal connector for **coaxial**
cable that is pushed on and turned a quarter turn to lock (a bayonet joint).
It is used on CCTV cameras, laboratory instruments and old coaxial Ethernet.

**Fibre-optic connectors** hold the glass fibre in a precise ceramic tube
(the *ferrule*) so that the two fibre ends meet exactly:

- **ST (Straight Tip)** — round metal body with a bayonet twist-lock;
- **SC (Subscriber Connector, also called Square or Standard Connector)** —
  square plastic body that clicks in with a push and comes out with a pull;
  it is the usual plug on home fibre (FTTH) equipment;
- **LC (Lucent Connector)** — a small push-pull connector about half the size
  of SC, used on the fibre modules of switches;
- **SMA (SubMiniature version A)** — a connector with a threaded nut that is
  screwed on; mainly older and industrial equipment.

```photo id="cs10/fibre-st-sc" caption="Two common fibre-optic connectors on patch cables: ST connectors with round metal bodies and a twist-lock (left) and SC connectors with square push-pull bodies (right). The white tip at the front of each is the ferrule that holds the glass fibre." width="100"
label 0.50 0.16 "ST: round, twist-lock"
label 0.80 0.16 "SC: square, push-pull"
```

::: caution SMA is "SubMiniature version A"
The textbook expands SMA as "Screw-Mounted Adaptor". That phrase is a handy way
to remember that SMA screws on, but it is not the name. SMA stands for
**SubMiniature version A**, a connector design first made for radio equipment
and later adapted for fibre.
:::

**Media converter.** A media converter joins two different kinds of cable,
usually copper twisted pair and optical fibre. It turns the **electrical
signals** arriving through its RJ-45 port into **light pulses** for the fibre
port, and turns incoming light back into electrical signals. It is needed when

- a link is longer than the 100 m allowed for copper Ethernet, for example
  between two school buildings;
- a fibre line from an ISP or another building must join an ordinary copper
  switch;
- a cable must pass through a place full of electrical noise, such as near
  motors or high-voltage lines.

```photo id="cs10/media-converter" caption="A copper-to-fibre media converter with its cover removed. Electrical signals enter through the RJ-45 port, the circuit board converts them, and the fibre port sends them on as light; a small power supply feeds the board." width="74"
call 0.17 0.15 0.19 0.47 "power supply"
call 0.42 0.07 0.60 0.30 "fibre port"
call 0.86 0.12 0.72 0.33 "RJ-45 port"
call 0.80 0.95 0.66 0.62 "converter board"
```

| Connector | Cable | Shape and locking | Typical use |
|---|---|---|---|
| RJ-45 | twisted pair (CAT5e, CAT6) | clear plastic, 8 contacts, clip | Ethernet: PCs, switches, routers |
| RJ-11 | telephone twisted pair | smaller plastic, 2 or 4 contacts, clip | telephones, DSL modems |
| BNC | coaxial | round metal, push and twist | CCTV, instruments, old Ethernet |
| ST | optical fibre | round metal, bayonet twist | older fibre equipment |
| SC | optical fibre | square plastic, push-pull | FTTH, patch panels |
| LC | optical fibre | small square, push-pull | switch fibre modules |
| SMA | optical fibre | threaded nut, screwed on | industrial and older equipment |

::: note Activity 1.4 — RJ-45 and fibre connectors in the lab
1. Hold an RJ-45 plug and an SC or LC fibre connector side by side. Note that
   the RJ-45 has metal contacts for electricity, while the fibre connector has
   only a glass tip for light.
2. **Crimp a cable.** Strip about 2–3 cm of the jacket. Untwist the pairs and
   arrange the wires in the T568B order: white-orange, orange, white-green,
   blue, white-blue, green, white-brown, brown. Trim them straight to about
   1.3 cm, push them fully into the plug with the clip underneath, and squeeze
   the crimping tool. Do the same at the other end and check the cable with a
   cable tester: all eight lights should flash in order.
3. Plug the cable into a PC and a switch and watch the link light come on.
4. Discuss why the school's link to the ISP is fibre while the cables in the
   lab are copper.
:::

## 1.4 Networking devices

A network is built from three kinds of component: **hardware** (computers,
cables and the devices below), **software** (a network operating system such as
Windows Server or Linux, and application software), and the **communication
medium**. The devices decide where each piece of data goes.

**NIC (Network Interface Card).** The circuit, built into every computer and
phone or added as a card, that connects the device to the network medium — an
RJ-45 port for a cable or a radio for Wi-Fi. Every NIC carries a permanent
48-bit **MAC (Media Access Control) address**, written in hexadecimal such as
`3C-52-82-9A-7F-10`, which identifies that card on the local network.

**Repeater.** A signal grows weaker the farther it travels. A repeater receives
the weak signal, **regenerates** it to full strength and sends it on, so the
network can reach farther. It does not look at addresses.

**Hub.** A box with many ports into which computers are plugged in a star. A
hub is a "multi-port repeater": whatever arrives at one port is **copied to
every other port**. All the computers share one bandwidth and their signals can
collide. Hubs are cheap and simple but have been replaced by switches.

**Switch.** Also a multi-port box at the centre of a star, but intelligent. It
reads the **MAC address** in each frame, learns which computer is on which port
(its MAC address table), and sends the frame **only to the port of the
destination**. Each port gets the full speed and can send and receive at the
same time, so a switched LAN is faster and more private than one built on a
hub.

**Bridge.** Joins two LAN segments that use the same protocol, inspects each
frame and forwards it to the other segment only if the destination is there.
In effect it is a two-port switch.

**Router.** Joins **different networks** — for example a school LAN and the
ISP's network — and forwards packets between them using **IP addresses**. It
keeps a **routing table** and chooses the best path for each packet. The
"Wi-Fi router" in a home is really several devices in one box: a router, a
small switch, a wireless access point, a DHCP server that hands out IP
addresses, and a firewall.

**Modem (modulator–demodulator).** Converts the computer's digital signals into
the form the line carries (modulation) and back again (demodulation). DSL
modems work on telephone lines, cable modems on coaxial cable and 4G dongles or
MiFi devices on the mobile network. On a fibre line the same job is done by an
**ONT (Optical Network Terminal)**, which converts light to electrical signals.

**Wireless access point (WAP).** Lets Wi-Fi devices join a wired LAN. It is
connected to a switch by cable and broadcasts a network name (SSID); schools,
hotels and offices mount several on ceilings so that the signal reaches every
room.

**Gateway.** A device or program that connects two networks that use
**different protocols**, translating between them — for example a VoIP gateway
between telephone lines and the Internet, or an IoT gateway between sensors and
a cloud server. In everyday use, the **default gateway** of a computer is the
router address to which it sends every packet meant for another network.

```photo id="cs10/switch-rack" caption="Network equipment in a rack. The grey CAT6 patch cables run from the patch panels at the top, where the wall cables of each room end, to the Ethernet switches below; the switches join every room into one LAN." width="70"
call 0.21 0.95 0.30 0.80 "patch panels"
call 0.22 0.06 0.30 0.30 "Ethernet switches"
```

```photo id="cs10/access-point" caption="A wireless access point. Its two antennas send and receive the Wi-Fi radio signals; a cable at the back joins it to the switch of the wired LAN." width="56"
```

| Point | Hub | Switch | Router |
|---|---|---|---|
| Job | joins computers of one LAN | joins computers of one LAN | joins different networks, e.g. a LAN and the Internet |
| How it forwards data | copies every signal to all ports | sends each frame only to the destination's port | chooses the best path to the destination network |
| Address it uses | none | MAC address | IP address |
| Speed and traffic | all ports share one bandwidth; collisions | full bandwidth on every port; no collisions | depends on its links |
| Intelligence | none | learns MAC addresses | routing table, NAT, DHCP, firewall |
| Today | obsolete | in every LAN | at the edge of every network |

::: note Field Visit Activity 1.1 — identify network devices and cables
Visit your school's computer lab, an ISP office, a telecom office or a bank
branch. (1) Find the router, the switches, any modem or ONT and the wireless
access points, and write one line on what each does. (2) Identify the cables:
CAT6 patch cords with RJ-45 plugs, coaxial cable, and fibre patch cords with SC
or LC plugs. (3) Make a two-column list of the wired and the wireless parts of
the network, and draw how they are joined.
:::

## 1.5 Network topology

::: definition Network topology
**Network topology** is the pattern in which the computers and devices of a
network are connected. The **physical topology** is the layout of the cables
and devices; the **logical topology** is the path that data actually follows.
:::

```figure caption="The six topologies. Squares are computers (nodes) and the orange boxes are switches. In a full mesh every pair of nodes has its own link, so five nodes need 10 links."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
fig, axs = plt.subplots(2, 3, figsize=(5.0, 3.6))
def pc(ax, x, y, w=0.15):
    ax.add_patch(Rectangle((x - w / 2, y - 0.055), w, 0.11, fc="white",
                           ec=ACCENT, lw=1.1, zorder=3))
def sw(ax, x, y):
    ax.add_patch(FancyBboxPatch((x - 0.12, y - 0.05), 0.24, 0.10,
                 boxstyle="round,pad=0.008", fc="#fbe3bd", ec="#b8860b", lw=1.0, zorder=3))
def ln(ax, p, q):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=MUTED, lw=1.0, zorder=1)
def title(ax, t):
    ax.text(0.5, -0.04, t, ha="center", va="top", fontsize=8.4, fontweight="bold",
            color=INK, transform=ax.transAxes)
ax = axs[0, 0]
ax.plot([0.04, 0.96], [0.5, 0.5], color=INK, lw=2.0, zorder=1)
for xt in (0.04, 0.96):
    ax.add_patch(Rectangle((xt - 0.022, 0.46), 0.044, 0.08, fc=INK, ec=INK, zorder=2))
for i, x in enumerate([0.18, 0.34, 0.5, 0.66, 0.82]):
    yy = 0.78 if i % 2 == 0 else 0.22
    ln(ax, (x, 0.5), (x, yy)); pc(ax, x, yy)
ax.text(0.03, 0.37, "terminator", ha="left", va="top", fontsize=6.8, color=MUTED)
title(ax, "Bus")
ax = axs[0, 1]
ang = np.pi / 2 + np.arange(6) * 2 * np.pi / 6
pts = [(0.5 + 0.34 * np.cos(a), 0.5 + 0.34 * np.sin(a)) for a in ang]
for i in range(6):
    ln(ax, pts[i], pts[(i + 1) % 6])
for p in pts:
    pc(ax, *p)
ax.annotate("", xy=(0.37, 0.44), xytext=(0.63, 0.44),
            arrowprops=dict(arrowstyle="-|>", color=SERIES[1], lw=1.2,
                            connectionstyle="arc3,rad=1.2", mutation_scale=9))
title(ax, "Ring")
ax = axs[0, 2]
for a in np.pi / 2 + np.arange(6) * 2 * np.pi / 6:
    p = (0.5 + 0.38 * np.cos(a), 0.5 + 0.38 * np.sin(a))
    ln(ax, (0.5, 0.5), p); pc(ax, *p)
sw(ax, 0.5, 0.5)
title(ax, "Star")
ax = axs[1, 0]
ang = np.pi / 2 + np.arange(5) * 2 * np.pi / 5
pts = [(0.5 + 0.38 * np.cos(a), 0.47 + 0.38 * np.sin(a)) for a in ang]
for i in range(5):
    for j in range(i + 1, 5):
        ln(ax, pts[i], pts[j])
for p in pts:
    pc(ax, *p)
title(ax, "Mesh (full)")
ax = axs[1, 1]
root = (0.5, 0.86); kids = [(0.24, 0.52), (0.76, 0.52)]
for k in kids:
    ln(ax, root, k)
    for dx in (-0.155, 0.0, 0.155):
        p = (k[0] + dx, 0.14); ln(ax, k, p); pc(ax, *p, w=0.12)
sw(ax, *root)
for k in kids:
    sw(ax, *k)
title(ax, "Tree")
ax = axs[1, 2]
ax.plot([0.04, 0.96], [0.86, 0.86], color=INK, lw=2.0, zorder=1)
for xt in (0.04, 0.96):
    ax.add_patch(Rectangle((xt - 0.022, 0.82), 0.044, 0.08, fc=INK, ec=INK, zorder=2))
for cx in (0.27, 0.73):
    ln(ax, (cx, 0.86), (cx, 0.5))
    for dx in (-0.16, 0.0, 0.16):
        p = (cx + dx, 0.14); ln(ax, (cx, 0.5), p); pc(ax, *p, w=0.12)
    sw(ax, cx, 0.5)
title(ax, "Hybrid (stars on a bus)")
for ax in axs.flat:
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal"); ax.axis("off")
fig.subplots_adjust(wspace=0.12, hspace=0.32)
```

**Bus topology.** All nodes are attached to one main cable, the **bus** or
backbone. A **terminator** at each end absorbs the signal so that it does not
bounce back. A signal sent by one node travels along the whole bus and every
node checks whether it is the addressee. A bus needs the least cable and is
cheap for a few computers, but a single break in the backbone stops the whole
network, faults are hard to find, and more nodes mean more collisions.

**Ring topology.** Each node is connected to the next and the last to the
first, forming a closed loop. Data travels round the ring in **one direction**,
from node to node; each node checks the address, regenerates the signal like a
repeater and passes it on. In a *token ring* only the node holding a special
message, the token, may send, so there are no collisions. But one broken cable
or switched-off node can stop the whole ring (unless a second ring is laid in
the opposite direction), and adding a node means breaking the ring.

**Star topology.** Every node has its own cable to a central **switch** (or,
in old networks, a hub). It is the topology of almost every LAN today. A faulty
cable affects only its own computer, nodes can be added or removed without
disturbing the others, and faults are easy to trace. It needs more cable than a
bus, and if the central switch fails, the whole star stops.

**Mesh topology.** Nodes are joined by many links, so there are several paths
between any two of them. In a **full mesh** every node is linked to every
other: $n$ nodes need $\frac{n(n-1)}{2}$ links and each node needs $n-1$ ports.
A mesh keeps working when a link fails and carries heavy traffic, but it is the
most expensive. The routers of the Internet's backbone form a (partial) mesh,
and "mesh Wi-Fi" systems use the same idea at home.

**Tree topology.** Star networks arranged in levels under a root: a main
switch feeds the switches of each floor or building, which feed the computers.
A school with several buildings is usually wired this way. It is easy to extend
branch by branch, but if the root fails, the branches below it are cut off.

**Hybrid topology.** A combination of two or more topologies — stars joined by
a bus or ring backbone, or a tree with a mesh core. Most real networks are
hybrid: each department keeps its own star while the backbone uses whatever
suits the distance and the budget. A hybrid network grows easily and one
failure rarely stops everything, but it is more complex to design and manage.

| Topology | Cable needed | Effect of one failure | Troubleshooting | Cost | Typical use |
|---|---|---|---|---|---|
| Bus | least | backbone break stops all | hard | lowest | very small, old networks |
| Ring | low | one break can stop all | hard | low | older networks; dual-ring city fibre |
| Star | more | only that node is cut off (switch failure stops all) | easy | moderate | almost every LAN |
| Mesh | most | traffic takes another path | moderate | highest | Internet backbone, mesh Wi-Fi |
| Tree | more | that branch is cut off | moderate | moderate | schools, offices on several floors |
| Hybrid | depends | usually local | depends | depends | large organisations |

::: caution Three textbook statements about the ring that are not right
The textbook says a ring "uses fibre optic cable", "is not affected by high
traffic or by adding more nodes" and "is cheap to set up and expand". A ring can
use any cable (the classic Token Ring used twisted pair); every extra node adds
delay to every message; and adding a node means opening the ring, which stops
the network while it is done. Do not copy those three points into an answer.
:::

::: example Worked example 1.5 — mesh or star?
**Problem.** Six computers are to be connected. (a) How many cables and ports
does a full mesh need? (b) How many does a star need?

**Solution.** (a) Links $= \frac{n(n-1)}{2} = \frac{6\times5}{2} =$ **15
cables**, and each computer needs $n-1 =$ **5 network ports**.
(b) A star needs one cable per computer, **6 cables**, and one switch with at
least 6 ports; each computer needs only **1 port**. This is why LANs are built
as stars: the mesh's reliability costs far more cable and hardware.
:::

## 1.6 Networks by coverage: PAN, LAN, MAN and WAN

::: definition Computer network
A **computer network** is a group of two or more computers and devices
connected by wired or wireless media to exchange data and to share hardware,
software and other resources.
:::

A network lets users **share hardware** (one printer or scanner for a whole
office), **share data and software**, **communicate** (email, chat, video
calls, the Internet), keep **centralised control** of users and security, and
make **central backups**. It offers services such as file, print, message,
application and database services. Networks are classified by the area they
cover.

**PAN (Personal Area Network).** Connects the devices of one person within
about 10 m: a phone with earbuds and a smartwatch over Bluetooth, or a laptop
using a phone's hotspot. It is easy to set up and needs little configuration.

**LAN (Local Area Network).** Connects computers in one room, building or
campus, up to about a kilometre across. It is privately owned (by the school
or office), fast (100 Mbps to 10 Gbps), has very few errors, and today is
almost always a **star** of switches. A LAN whose devices join by Wi-Fi is a
**WLAN** (wireless LAN). A school's computer lab is a LAN; a LAN spread over a
university's buildings is sometimes called a **CAN** (campus area network).

**MAN (Metropolitan Area Network).** Covers a city or a valley, from a few to
about 50 km. It usually joins many LANs, is owned by one large organisation or
a service provider, and links the LANs to the wider Internet. A cable-TV
network across Kathmandu Valley, an ISP's fibre ring around a city, or a bank
joining its branches within one city are MANs.

**WAN (Wide Area Network).** Covers a country, a continent or the whole world.
It joins LANs and MANs through links owned by many organisations — telephone
companies, ISPs and satellite operators — mainly **optical fibre** on land and
under the sea, with satellite and microwave links where cables cannot go.
Compared with a LAN its data rate per user is lower and its delay higher. The
**Internet** is the largest WAN; a bank linking branches in every province, or
Nepal Telecom's national network, are others.

```figure caption="Typical reach of the four kinds of network, on a logarithmic scale where each grid line is ten times the one before. The boundaries are typical figures, not fixed rules."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 2.6))
nets = [("PAN", 0.1, 10, "phone, earbuds, smartwatch (Bluetooth)"),
        ("LAN", 10, 1_000, "computer lab, one building or campus"),
        ("MAN", 1_000, 50_000, "a city or a valley, e.g. Kathmandu Valley"),
        ("WAN", 50_000, 2.0e7, "a country or the whole world (the Internet)")]
for i, (n, lo, hi, ex) in enumerate(nets):
    y = 3 - i
    ax.barh(y, hi - lo, left=lo, height=0.42, color=SERIES[i], alpha=0.9)
    ax.text(lo * 1.25, y + 0.29, ex, ha="left", va="bottom", fontsize=7.0, color=INK)
ax.set_xscale("log")
ax.set_xlim(0.05, 4e7)
ticks = [1, 10, 100, 1e3, 1e4, 1e5, 1e7]
ax.set_xticks(ticks)
ax.set_xticklabels(["1 m", "10 m", "100 m", "1 km", "10 km", "100 km", "10 000 km"],
                   fontsize=7)
ax.minorticks_off()
ax.set_yticks([3, 2, 1, 0]); ax.set_yticklabels([n[0] for n in nets], fontsize=8.5,
                                               fontweight="bold")
ax.set_ylim(-0.5, 3.75)
ax.set_xlabel("typical distance covered (log scale)", fontsize=8)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.grid(axis="x", color=GRID, lw=0.6); ax.set_axisbelow(True)
```

| Feature | PAN | LAN | MAN | WAN |
|---|---|---|---|---|
| Coverage | about 10 m around one person | room, building, campus (up to about 1 km) | city or valley (up to about 50 km) | country, continent, world |
| Ownership | one person | one organisation | one big organisation or a provider | many organisations |
| Speed | low to moderate | highest | high | lower per user |
| Delay and errors | low | lowest | moderate | highest |
| Media | Bluetooth, USB, infrared | twisted pair, Wi-Fi, fibre | fibre, microwave | fibre, satellite, microwave |
| Example | phone + earbuds | school computer lab | cable-TV network in a city | the Internet |

::: caution Two outdated LAN and WAN claims
The textbook says that "LANs commonly use topologies such as bus and ring" and
that WAN computers are connected "through wireless technology or media as
satellite communication". Both were true decades ago. Today LANs are switched
**stars**, and WANs run mainly over **optical fibre**, with satellites serving
the places fibre cannot reach.
:::

## 1.7 Network architecture: client–server and peer-to-peer

**Network architecture** describes how the computers of a network share the
work: whether some of them provide services for the rest, or all of them are
equal.

::: definition Client–server and peer-to-peer
In a **client–server network** one or more powerful computers called
**servers** provide services (files, printing, email, websites, databases),
and the other computers, called **clients**, request and use those services.
In a **peer-to-peer (P2P) network** every computer is equal: each one can share
its own files and printer with the others and use theirs, without a dedicated
server. A small P2P network is also called a **workgroup**.
:::

```figure caption="Client–server: every client sends its requests to the server, which answers them and controls the shared resources. Peer-to-peer: each computer talks directly to the others and acts as both client and server."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.0, 2.6))
def pc(ax, x, y, t="client"):
    ax.add_patch(Rectangle((x - 0.12, y - 0.07), 0.24, 0.14, fc="white", ec=ACCENT, lw=1.1, zorder=3))
    ax.text(x, y, t, ha="center", va="center", fontsize=6.9, color=INK, zorder=4)
a1.add_patch(FancyBboxPatch((0.4, 0.66), 0.2, 0.24, boxstyle="round,pad=0.01",
             fc="#fdecd2", ec="#b8860b", lw=1.1, zorder=3))
a1.text(0.5, 0.94, "server", ha="center", va="bottom", fontsize=7.4, color="#8a6408")
cl = [(0.08, 0.24), (0.36, 0.12), (0.64, 0.12), (0.92, 0.24)]
for p in cl:
    a1.plot([0.5, p[0]], [0.66, p[1] + 0.07], color=MUTED, lw=1.0, zorder=1)
    pc(a1, *p)
a1.annotate("", xy=(0.47, 0.62), xytext=(0.18, 0.33),
            arrowprops=dict(arrowstyle="-|>", color=SERIES[2], lw=1.1, mutation_scale=8))
a1.text(0.13, 0.52, "request", ha="center", va="center", fontsize=6.9, color=SERIES[2])
a1.annotate("", xy=(0.84, 0.33), xytext=(0.55, 0.62),
            arrowprops=dict(arrowstyle="-|>", color=SERIES[1], lw=1.1, mutation_scale=8))
a1.text(0.88, 0.52, "response", ha="center", va="center", fontsize=6.9, color=SERIES[1])
a1.text(0.5, -0.08, "Client–server", ha="center", va="top", fontsize=8.4,
        fontweight="bold", color=INK, transform=a1.transAxes)
ang = np.pi / 2 + np.arange(5) * 2 * np.pi / 5
pts = [(0.5 + 0.36 * np.cos(a), 0.5 + 0.36 * np.sin(a)) for a in ang]
for i in range(5):
    for j in range(i + 1, 5):
        a2.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]], color=MUTED, lw=0.9, zorder=1)
for p in pts:
    pc(a2, *p, t="peer")
a2.text(0.5, -0.08, "Peer-to-peer", ha="center", va="top", fontsize=8.4,
        fontweight="bold", color=INK, transform=a2.transAxes)
for a in (a1, a2):
    a.set_xlim(-0.06, 1.06); a.set_ylim(0, 1); a.set_aspect("equal"); a.axis("off")
fig.subplots_adjust(wspace=0.15)
```

| Point | Client–server | Peer-to-peer |
|---|---|---|
| Control | central: the server and an administrator control access | none: each user controls their own shared resources |
| Server | one or more dedicated servers | no dedicated server |
| Security | strong, managed in one place | weak; depends on every user |
| Backup | central backup of the server | each computer must be backed up separately |
| Cost | high (server hardware, software, administrator) | low |
| Failure | if the server fails, its services stop for everyone | one computer failing affects only its own shared resources |
| Size | scales to thousands of users | best for about 10 computers or fewer |
| Operating system | server OS: Windows Server, Ubuntu Server, UNIX | ordinary OS: Windows 11, macOS, Ubuntu |
| Example | school result system, online banking, websites | small office workgroup, Bluetooth file sharing |

### Network protocols

::: definition Protocol
A **protocol** is a set of rules that computers follow to communicate over a
network: how data is formatted, addressed, sent, checked and received. Two
devices can talk only if they follow the same protocol.
:::

The first host-to-host protocol of ARPANET, the network that grew into the
Internet, was **NCP (Network Control Program)**. ARPANET carried its first
message on 29 October 1969 — "LO", because the system crashed before "LOGIN"
was complete — and replaced NCP with TCP/IP on 1 January 1983.

| Protocol | Full form | What it does |
|---|---|---|
| TCP/IP | Transmission Control Protocol / Internet Protocol | the basic protocols of the Internet: IP addresses and routes packets, TCP checks that every packet arrives and in order |
| HTTP | HyperText Transfer Protocol | transfers web pages (HTML documents) from a web server to a browser |
| HTTPS | HyperText Transfer Protocol Secure | HTTP with encryption, so passwords and payments cannot be read in transit |
| DHCP | Dynamic Host Configuration Protocol | gives each device an IP address, subnet mask and default gateway automatically |
| DNS | Domain Name System | turns a name such as `www.google.com` into the IP address of the server |
| SMTP | Simple Mail Transfer Protocol | sends email from your mail program to the mail server and between servers |
| POP3 / IMAP | Post Office Protocol 3 / Internet Message Access Protocol | collect email from the mail server |
| FTP | File Transfer Protocol | transfers files between computers |
| Telnet | Teletype Network | remote login to another computer's command line (unencrypted; SSH is its secure replacement) |

## 1.8 IP addressing

::: definition IP address
An **IP (Internet Protocol) address** is a logical number given to every device
on a network that identifies the device and lets data be routed to it. The MAC
address is fixed in the network card and is used only inside the local
network; the IP address is assigned by the network and is used to deliver
packets across networks.
:::

### IPv4

An **IPv4** address is **32 bits** long, written as four decimal numbers called
**octets**, each from 0 to 255, separated by dots — **dotted-decimal
notation**, for example `192.168.1.10`. Each octet is 8 bits, so
$2^{32} = 4,294,967,296$ (about 4.3 billion) addresses are possible. That is
fewer than the number of devices now online; the central pool of free IPv4
addresses ran out in 2011, and networks survive by giving private addresses
inside and sharing one public address through **NAT** (Network Address
Translation) on the router.

::: example Worked example 1.6 — reading IPv4 addresses
**Problem.** (a) Write `192.168.1.10` in binary. (b) Which of these are not
valid IPv4 addresses: `10.0.0.300`, `172.20.5.1`, `256.1.1.1`?

**Solution.** (a) Convert each octet to 8 bits:
192 = 11000000, 168 = 10101000, 1 = 00000001, 10 = 00001010, so the address is
**11000000.10101000.00000001.00001010** — 32 bits.
(b) An octet can only be 0 to 255, so **`10.0.0.300` and `256.1.1.1` are
invalid**; `172.20.5.1` is valid.
:::

### IPv6

**IPv6** was designed to replace IPv4. Its addresses are **128 bits** long,
written as **eight groups of four hexadecimal digits** separated by colons, for
example `2001:0db8:85a3:0000:0000:8a2e:0370:7334`. That gives
$2^{128} \approx 3.4\times10^{38}$ addresses — enough for every device that
will ever be built. Two rules shorten an address: leading zeros in a group may
be dropped, and **one** run of consecutive all-zero groups may be replaced by
`::`. So the address above is written `2001:db8:85a3::8a2e:370:7334`.

| Point | IPv4 | IPv6 |
|---|---|---|
| Length | 32 bits | 128 bits |
| Written as | 4 decimal octets with dots | 8 hexadecimal groups with colons |
| Number of addresses | $2^{32}\approx4.29\times10^{9}$ | $2^{128}\approx3.4\times10^{38}$ |
| Configuration | manual or by DHCP | automatic (stateless auto-configuration), DHCPv6 or manual |
| Header | 20–60 bytes, variable | 40 bytes, fixed and simpler |
| Security (IPsec) | can be added | designed into the standard |
| Broadcast | used | not used; multicast instead |
| NAT | widely needed | not needed |
| Example | `192.168.1.1` | `2001:db8::1` |

::: caution IPv4 is not "without security"
The textbook says IPv4 provides no encryption or authentication. The security
system for IP, **IPsec**, works with IPv4 as well; the difference is that it was
built into the IPv6 design from the start. Most encryption you actually use
(HTTPS) works the same way on both.
:::

::: example Worked example 1.7 — shortening an IPv6 address
**Problem.** Write `2001:0db8:0000:0000:0000:ff00:0042:8329` in its shortest
form. How many times more addresses does IPv6 have than IPv4?

**Solution.** Drop leading zeros: `2001:db8:0:0:0:ff00:42:8329`. Replace the
run of three zero groups by `::`: **`2001:db8::ff00:42:8329`**.
Ratio $= \frac{2^{128}}{2^{32}} = 2^{96} \approx$ **7.9 × 10²⁸** times.
:::

### Private and public, static and dynamic addresses

**Private addresses** are reserved for use inside LANs. They can be repeated
in every home and school, and routers on the Internet do not forward them.
**Public addresses** are globally unique and are assigned by ISPs (in our
region, from the pool managed by APNIC); every device visible on the Internet
needs one.

| Private IPv4 range | Number of addresses |
|---|---|
| 10.0.0.0 to 10.255.255.255 | about 16.8 million |
| 172.16.0.0 to 172.31.255.255 | about 1 million |
| 192.168.0.0 to 192.168.255.255 | 65,536 |

Two other special addresses: `127.0.0.1` (*loopback*) always means "this
computer", and an address beginning `169.254` means a computer asked for an
address by DHCP and got no reply.

| Static IP address | Dynamic IP address |
|---|---|
| typed in manually and never changes | given automatically by a DHCP server for a lease period |
| needs planning to avoid two devices getting the same address | no planning; the server never repeats an address |
| used for servers, network printers, CCTV recorders, routers | used for phones, laptops and most PCs |
| example: a printer fixed at 192.168.1.20 | example: a phone that gets 192.168.1.101 when it joins Wi-Fi |

```figure caption="A typical school LAN. The router is the default gateway (192.168.1.1) between the private LAN and the ISP; wired computers reach it through the switch, and Wi-Fi devices through the access point. The printer has a static address, the laptop and phone get dynamic ones from the router's DHCP server."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse
fig, ax = plt.subplots(figsize=(5.1, 3.6))
def box(x, y, t, w=1.5, h=0.62, fc="#eef4fa", ec=ACCENT, fs=7.4):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                 boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=1.1, zorder=3))
    ax.text(x, y, t, ha="center", va="center", fontsize=fs, color=INK, zorder=4,
            linespacing=1.15)
def ln(p, q, ls="-", c=MUTED, lw=1.2):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=c, lw=lw, ls=ls, zorder=1)
ax.add_patch(FancyBboxPatch((0.15, 0.05), 9.7, 3.75, boxstyle="round,pad=0.02,rounding_size=0.2",
             fc="none", ec="#9aa3af", lw=1.0, ls="--", zorder=0))
ax.text(0.35, 3.62, "School LAN: private addresses 192.168.1.x", ha="left", va="center",
        fontsize=7.2, color=MUTED)
for (x, y) in [(0.85, 5.15), (1.2, 5.4), (1.6, 5.2), (1.25, 4.95)]:
    ax.add_patch(Ellipse((x, y), 1.0, 0.62, fc="#e8edf4", ec="none", zorder=2))
ax.text(1.23, 5.17, "Internet", ha="center", va="center", fontsize=8, color=INK, zorder=4)
box(4.55, 5.15, "Modem / ONT", w=1.9)
box(8.0, 5.15, "Router\n192.168.1.1", w=1.7, h=0.78, fc="#fdecd2", ec="#b8860b")
ln((2.15, 5.15), (3.55, 5.15), c=SERIES[2], lw=2.0)
ax.text(2.85, 5.0, "fibre\nfrom ISP", ha="center", va="top", fontsize=6.8, color=SERIES[2],
        linespacing=1.1)
ln((5.55, 5.15), (7.15, 5.15))
ax.text(8.0, 4.68, "default gateway", ha="center", va="top", fontsize=6.8, color="#8a6408")
box(4.3, 2.75, "Switch (24 ports)", w=2.0, fc="#fdecd2", ec="#b8860b")
box(8.3, 2.75, "Wireless\naccess point", w=1.6, h=0.72)
ln((8.0, 4.76), (4.9, 3.06))
ln((5.3, 2.75), (7.5, 2.75))
wired = [(1.0, "PC\n.11"), (2.35, "PC\n.12"), (3.7, "PC\n.13"), (5.05, "Printer\n.20")]
for x, t in wired:
    box(x, 0.85, t, w=1.05, h=0.7, fs=7.0)
    ln((4.3, 2.44), (x, 1.2))
for x, t in [(7.55, "Laptop\n.101"), (9.05, "Phone\n.102")]:
    box(x, 0.85, t, w=1.15, h=0.7, fs=7.0)
    ln((8.3, 2.39), (x, 1.2), ls=(0, (2, 2)), c=ACCENT)
ax.text(8.3, 1.75, "Wi-Fi", ha="center", va="center", fontsize=7, color=ACCENT,
        bbox=dict(fc="white", ec="none", pad=1.2), zorder=4)
ax.annotate("CAT6 cables", xy=(2.46, 1.75), xytext=(1.2, 2.45), fontsize=6.8,
            color=MUTED, ha="center", va="bottom",
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
ax.set_xlim(0, 10); ax.set_ylim(-0.05, 5.75); ax.axis("off")
```

### Checking an IP address and the default gateway

A device's **subnet mask** (usually `255.255.255.0` in a small LAN) tells it
which addresses are on its own network. For any other address it sends the
packet to the **default gateway**, the address of the router — the door out of
the LAN.

::: note Activity 1.2 — check your IP address and default gateway
On a Windows computer open **Command Prompt** and type `ipconfig`. A laptop on
Wi-Fi shows something like this (your numbers will differ):

```text
Wireless LAN adapter Wi-Fi:

   Connection-specific DNS Suffix  . :
   Link-local IPv6 Address . . . . . : fe80::1c2b:7d4e:9a10:3f21%12
   IPv4 Address. . . . . . . . . . . : 192.168.1.105
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.1.1
```

Read it: the IPv4 address `192.168.1.105` is **private**; the router is at
`192.168.1.1`; the computer also has an IPv6 address beginning `fe80`, which is
used only on the local link. `ipconfig /all` adds the MAC address ("Physical
Address") and the line "DHCP Enabled: Yes", which means the address is
**dynamic**. To see your **public** address, search "what is my IP" in a
browser: you will see the single address that your router shares with every
device in the house. On Android open Settings → Wi-Fi → the connected network
→ details.
:::

::: note Activity 1.3 — four troubleshooting commands
| Command | What it does | What to look for |
|---|---|---|
| `ping google.com` | sends four small test packets and times the replies | "Reply from …" lines and "Lost = 0 (0% loss)" mean the host is reachable |
| `ipconfig` | shows this computer's IP address, subnet mask and gateway | an address starting 169.254 means DHCP failed |
| `tracert google.com` | lists every router (hop) on the path to the destination | the number of hops, and where the delay suddenly grows |
| `nslookup google.com` | asks the DNS server for the IP address of a name | the "Addresses" lines are the server's IP addresses |

A sample `ping` (the address and times will differ on your computer):

```text
Pinging google.com [142.250.193.78] with 32 bytes of data:
Reply from 142.250.193.78: bytes=32 time=38ms TTL=117
Reply from 142.250.193.78: bytes=32 time=37ms TTL=117
Reply from 142.250.193.78: bytes=32 time=41ms TTL=117
Reply from 142.250.193.78: bytes=32 time=38ms TTL=117

Ping statistics for 142.250.193.78:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
```

The name `google.com` was first turned into an IP address by DNS; the "time"
of about 38 ms is the round-trip latency.
:::

::: example Worked example 1.8 — classify the addresses
**Problem.** For each address say whether it is private or public:
`10.12.0.7`, `172.20.5.1`, `172.32.1.1`, `192.168.10.25`, `8.8.8.8`.

**Solution.** `10.12.0.7` — **private** (10.x.x.x). `172.20.5.1` — **private**
(172.16 to 172.31). `172.32.1.1` — **public**, because 32 is outside 16–31.
`192.168.10.25` — **private**. `8.8.8.8` — **public** (it is Google's public
DNS server).
:::

## 1.9 Internet, intranet and extranet

::: definition Internet, intranet and extranet
The **Internet** is the worldwide network of networks, joined by the TCP/IP
protocols and open to anyone. An **intranet** is a private network inside one
organisation that uses Internet technologies (TCP/IP, web pages, email) but is
open only to the organisation's own staff. An **extranet** is the part of an
organisation's private network that is opened, with passwords and controls, to
selected outsiders such as customers, suppliers or partners.
:::

The Internet offers the **World Wide Web**, **email**, file transfer (FTP),
chat (IRC and messaging apps), remote login (Telnet, SSH), video calls, online
shopping, banking and cloud storage. A bank's internal portal where staff check
circulars and apply for leave is an **intranet**; the same bank's portal where
its merchants check their QR-payment settlements is an **extranet**. A school
whose results and attendance pages can be seen only from inside the school is
running an intranet; if parents may log in from home to see their own child's
records, that part becomes an extranet.

| Point | Internet | Intranet | Extranet |
|---|---|---|---|
| What it is | global network of public, private, academic, business and government networks | private network of one organisation | private network opened in a controlled way to outsiders |
| Who can use it | anyone | the organisation's staff only | staff plus selected partners, suppliers or customers |
| Purpose | share information and connect people worldwide | share information and resources inside the organisation | share specific information with partners |
| Security | least secure; users need firewalls and antivirus | most secure, behind the firewall | secure, but must balance access for outsiders |
| Example | websites, Google, Facebook, YouTube | company portal, school staff portal | supplier ordering portal, parents' result portal |

## Textbook exercises: model answers

**1. Full forms.** (a) DSL — Digital Subscriber Line. (b) bps — bits per second.
(c) LAN — Local Area Network. (d) TCP/IP — Transmission Control Protocol /
Internet Protocol. (e) IPv6 — Internet Protocol version 6. (f) ISP — Internet
Service Provider. (g) RFID — Radio Frequency Identification. (h) CAT6 —
Category 6 (twisted-pair cable). (i) NCP — Network Control Program (also called
Network Control Protocol). (j) DNS — Domain Name System.

::: note 2. Multiple choice — answers

**i.** (d) — DSL, fibre and cable are all broadband connections.

**ii.** (b) — throughput is the data actually transferred per second.

**iii.** (b) — a packet is a small unit of data sent over a network.

**iv.** (a) — fibre is a cable; infrared, microwave and laser beams are wireless.

**v.** (c) — Earth to satellite is the uplink; satellite to Earth is the downlink.

**vi.** (c) — RJ-45 ends twisted-pair Ethernet cables.

**vii.** (b) — the connection pattern is the topology.

**viii.** (c) — in a star every device is cabled to a central hub or switch.

**ix.** (c) — a WAN joins LANs over large areas.

**x.** (d) — IRC (chat), Telnet (remote login) and email are all Internet services.

**xi.** (c) — FTP is the File Transfer Protocol.

**xii.** (b) — IPv4 addresses are 32 bits (IPv6 are 128).

**xiii.** (c) — an IP address identifies one device on a network.

**xiv.** (c) — SMTP sends email; HTTP carries web pages.

**xv.** (c) — a repeater regenerates weak signals.
:::

::: note 3. Short questions — model answers
**a.** Broadband is an always-on, high-speed Internet connection that carries a
large amount of data at once. Dial-up had to dial a number before each session,
was limited to 56 kbps and kept the telephone line busy; broadband is hundreds of
times faster, always connected, and leaves the phone free.

**b.** Bandwidth is the maximum amount of data a link can carry per second. It is
measured in bits per second: bps, kbps, Mbps and Gbps.

**c.** A data packet is a small unit into which a message is broken for sending.
Its header holds the source and destination addresses and a sequence number, its
payload holds part of the message, and its trailer holds an error check; the
receiver reassembles the packets in order.

**d.** Frequency is the number of complete cycles a signal's wave makes in one
second, measured in hertz (kHz, MHz, GHz). Each service uses its own frequency
band, for example 88–108 MHz for FM radio and 2.4 GHz for Wi-Fi.

**e.** A repeater receives a weakened signal, regenerates it to full strength and
retransmits it, so data can travel farther than one cable or radio link allows.

**f.** A computer network is two or more computers and devices connected by wired
or wireless media to share data and resources. It lets users share printers,
files and an Internet connection, communicate by email and video call, and keep
data backed up and secured centrally.

**g.** Because it gives mobility (phones and laptops move freely), needs no
cabling so it is quick and cheap to install, reaches places where cables are
hard to lay, and modern Wi-Fi, 4G and 5G are now fast enough for video and
online classes.

**h.** RJ-45 is a clear plastic 8P8C plug with eight gold contacts and a locking
clip, crimped onto twisted-pair cable. It connects computers, switches, routers
and access points in Ethernet LANs.

**i.** A media converter joins copper twisted-pair cable to optical fibre by
converting electrical signals into light and back. It is used when a link must
run farther than 100 m or a fibre line must join a copper switch.

**j.** Bandwidth is the maximum data rate a link can carry; throughput is the
rate actually achieved. Bandwidth is fixed by the link or plan, while throughput
changes with traffic, distance and interference and is always less than or
equal to bandwidth.

**k.** The Wi-Fi adapter of the laptop or phone turns data into radio waves in
the 2.4 GHz or 5 GHz band. The router or access point receives them and passes
the data on through its wired connection; replies come back as radio waves the
same way. A WPA2/WPA3 password encrypts the data in the air.

**l.** The sending computer breaks the data into packets carrying the source and
destination addresses. Its NIC sends them as signals over the medium; a switch
forwards them inside the LAN using MAC addresses, and routers forward them from
network to network using IP addresses. The receiver puts the packets back in
order and asks again for any that are missing.

**m.** In a ring, data travels in one direction from one node to the next. Each
node reads the destination address, keeps the data if it is the addressee, and
otherwise regenerates the signal and passes it on until it reaches the
destination.

**n.** Direct-to-home (DTH) television, which brings TV channels straight to a
small dish on the house. (GPS navigation and weather forecasting are other
uses.)

**o.** Guided media — for example optical fibre (also twisted pair, coaxial).
Unguided media — for example Wi-Fi (also radio, microwave, satellite).
:::

::: note 4. Long questions — model answers
**i. Communication media.** Communication (transmission) media are the paths
through which signals travel from sender to receiver. **Guided** media carry
signals along a cable: *twisted pair* (cheap, used in LANs, up to 100 m),
*coaxial* (shielded, used for cable TV and CCTV) and *optical fibre* (light in a
glass core, very fast, tens of kilometres, immune to interference). **Unguided**
media carry electromagnetic waves through air or space: *radio waves*
(all directions, long range), *microwave* (line of sight between dishes),
*infrared* (a few metres, e.g. TV remote), *satellite* (relay in space for TV,
GPS and remote Internet), *Wi-Fi* and *Bluetooth*. Guided media are more secure
and less affected by weather; unguided media allow mobility and need no cables.

**ii. LAN and MAN.**

| LAN | MAN |
|---|---|
| covers a room, building or campus (up to about 1 km) | covers a city or valley (up to about 50 km) |
| owned by one organisation such as a school | owned by a large organisation or a service provider |
| highest speed, fewest errors | lower speed and more delay than a LAN |
| twisted pair, Wi-Fi and some fibre | mostly optical fibre and microwave |
| cheap to set up and maintain | costly to set up |
| example: school computer lab | example: cable-TV network across Kathmandu |

**iii. Client–server and peer-to-peer.** In client–server, dedicated servers
provide services and clients request them; in peer-to-peer every computer is
equal and shares its own resources. Client–server has central control and
security, central backup, high cost, a single point of failure at the server
and room for thousands of users. Peer-to-peer has no central control, weak
security, separate backups, low cost, no single point of failure, and suits
about ten computers or fewer. (See the full table in §1.7.)

**iv. A school with three buildings.** The school needs a **campus LAN built as
a tree (hybrid) topology**. Each building gets its own star: a switch with CAT6
cables to its computers and an access point for Wi-Fi. The three building
switches are joined to a core switch in the server room by **optical fibre**
(through media converters or fibre ports), because the buildings are more than
100 m apart and fibre is immune to lightning and electrical noise between
buildings. *Communication:* every device is on one LAN, so email, chat and the
school's intranet work at LAN speed. *File sharing:* a file server in the server
room (client–server) holds shared folders and is backed up centrally.
*Internet access:* one router with a firewall connects the core switch to the
ISP's fibre line and shares the connection with all three buildings through NAT,
with DHCP giving every device an address.

**v. A home network.** The ISP's fibre ends at an **ONT**, which connects to a
**Wi-Fi router** (router, 4-port switch, access point, DHCP and firewall in one).
Two desktop PCs are connected to the router's LAN ports with **CAT6 cables**
(wired, for a fast and stable link); the third PC, if it is a laptop, and the
**mobile phone** connect by **Wi-Fi**; the **printer** joins by Wi-Fi or a cable
and is given a **static IP** such as 192.168.1.20 so that every computer can
always find it. The router hands dynamic IP addresses to the other devices and
shares one public IP address through NAT. A strong WPA2/WPA3 password protects
the Wi-Fi. If more wired ports are needed, a small switch is added. The layout
is the same as the school LAN in the figure of §1.8, on a smaller scale.

**vi. Small office: client–server or peer-to-peer?** For a small office of
five or six computers, **peer-to-peer** is usually more suitable.
*Cost:* no server or server software to buy and no administrator to pay.
*Management:* each user shares a folder or the printer in a few clicks.
*Security:* weaker than client–server, but acceptable if the office holds
little confidential data and uses good passwords.
*Scalability:* poor beyond about ten computers. So if the office expects to grow
quickly or stores sensitive customer records, client–server is the better
choice, because it gives central security, central backup and room to grow.

**vii. A school lab of 10 computers.** Use a **star topology** with a 16-port
**switch** at the centre: ten CAT6 cables (each under 100 m) from the
computers, one cable to a printer, and one uplink cable to the **router**, which
connects to the ISP and acts as the **default gateway** and DHCP server. Each PC
gets an address such as 192.168.1.11 to 192.168.1.20. When PC 1 sends a file
to PC 2, the switch forwards the frames only to PC 2's port using its MAC
address; when PC 1 opens a website, the packets go through the switch to the
router and out to the Internet. A star is chosen because one faulty cable
affects only one computer, computers are easy to add, and faults are easy to
find.
:::

::: note Case studies — suggested answers
**1. A lab of 36 computers.** A **star** topology with a 48-port gigabit switch
(or two 24-port switches joined in a tree), CAT6 cables, and one uplink to the
router for Internet access, forming one LAN. A switch delivers files instantly
between any two computers at full speed, one damaged cable affects only one
computer, and a faulty computer is found by checking one cable and one port.

**2. Wi-Fi slow on the first floor.** Likely reasons: the signal weakens with
distance and through concrete floors and walls, especially in the 5 GHz band;
the router is in a corner, low down or inside a cabinet; neighbouring Wi-Fi
networks, microwave ovens and Bluetooth devices interfere in the 2.4 GHz band;
many devices share the bandwidth. Solutions: place the router high in a central
spot; use the 2.4 GHz band upstairs; change to a less crowded channel; add a
Wi-Fi repeater, a mesh node or, best of all, a second access point connected to
the router by a CAT6 cable.

**3. Upgrading an office in Birgunj.** Replace the old devices with a modern
router, a gigabit switch, Wi-Fi 6 access points and CAT6 cabling; take a fibre
(FTTH) connection now. 5G would bring far higher throughput, very low latency
for video meetings and cloud software, and room for many devices at once,
including IoT sensors. Since commercial 5G had not yet been launched in Nepal in
2026, the office should use fibre or 4G LTE today and choose a router that can
later take a 5G connection.
:::

## Chapter summary

- **Telecommunication** is exchanging information over a distance electronically;
  every link has a sender, message, medium, receiver and protocol.
- **Bandwidth** is the maximum data rate of a link; **throughput** is the rate
  actually achieved; time = data in bits ÷ rate, and 1 byte = 8 bits.
- **Broadband** (DSL, cable, fibre, satellite, wireless) is always-on and fast;
  **3G → 4G → 5G** brought mobile Internet, then HD streaming, then very low
  latency for IoT. 4G reached Nepal in 2017.
- Data travels in **packets** (header, payload, trailer). **Frequency** is
  cycles per second in hertz; $\lambda = \frac{c}{f}$.
- Modes: **simplex** (one way), **half duplex** (both ways, one at a time),
  **full duplex** (both ways together).
- **Guided media**: twisted pair (CAT6, 100 m), coaxial, optical fibre (light,
  tens of km). **Unguided**: radio, microwave, infrared, satellite (uplink and
  downlink), Wi-Fi, Bluetooth, RFID.
- **Connectors**: RJ-45 (Ethernet, 8 pins), RJ-11 (telephone), BNC (coaxial),
  ST, SC, LC and SMA (fibre); a **media converter** joins copper and fibre.
- **Devices**: NIC (MAC address), repeater, hub (copies to all), switch (MAC,
  one port), bridge, router (IP, best path), modem/ONT, access point, gateway
  (different protocols).
- **Topologies**: bus, ring, star, mesh ($\frac{n(n-1)}{2}$ links), tree,
  hybrid. **Coverage**: PAN, LAN, MAN, WAN. **Architecture**: client–server or
  peer-to-peer.
- **IPv4**: 32 bits, dotted decimal; **IPv6**: 128 bits, hexadecimal with
  colons. Private ranges 10.x, 172.16–31.x, 192.168.x; static or dynamic (DHCP);
  check with `ipconfig`. Internet (public), intranet (staff only), extranet
  (selected outsiders).

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. A student's plan is 50 Mbps but a speed test reads 38 Mbps. The 38 Mbps is the <span class="marks">[1]</span>
   (a) bandwidth (b) throughput (c) frequency (d) latency
2. A walkie-talkie works in <span class="marks">[1]</span>
   (a) simplex mode (b) half-duplex mode (c) full-duplex mode (d) broadcast mode
3. Which medium carries data as pulses of light? <span class="marks">[1]</span>
   (a) CAT6 (b) coaxial cable (c) optical fibre (d) STP cable
4. The connector on a telephone-line cable is <span class="marks">[1]</span>
   (a) RJ-45 (b) RJ-11 (c) BNC (d) SC
5. Which device sends a frame only to the port of the destination computer? <span class="marks">[1]</span>
   (a) hub (b) repeater (c) switch (d) modem
6. In which topology does the failure of the central device stop the whole network? <span class="marks">[1]</span>
   (a) bus (b) ring (c) star (d) mesh
7. How many cables are needed to join 8 computers in a full mesh? <span class="marks">[1]</span>
   (a) 8 (b) 16 (c) 28 (d) 56
8. Which is a private IPv4 address? <span class="marks">[1]</span>
   (a) 8.8.8.8 (b) 172.32.0.5 (c) 192.168.10.25 (d) 1.1.1.1
9. Which command shows a Windows computer's IP address, subnet mask and default gateway? <span class="marks">[1]</span>
   (a) ping (b) ipconfig (c) tracert (d) nslookup
10. An IPv6 address is written as <span class="marks">[1]</span>
    (a) four decimal numbers with dots (b) eight hexadecimal groups with colons (c) 32 binary digits (d) six hexadecimal pairs with hyphens
11. A company lets its suppliers log in to check orders and stock. This network is an <span class="marks">[1]</span>
    (a) Internet (b) intranet (c) extranet (d) PAN
12. Which protocol gives devices their IP addresses automatically? <span class="marks">[1]</span>
    (a) DNS (b) DHCP (c) FTP (d) SMTP

::: note Answers to Group A
**1.** (b) — the measured rate is throughput; 50 Mbps is the bandwidth.
**2.** (b) — both sides talk, but only one at a time.
**3.** (c) — fibre carries light; the others carry electrical signals.
**4.** (b) — RJ-11 is the telephone plug; RJ-45 is for Ethernet.
**5.** (c) — a switch reads the MAC address; a hub copies to every port.
**6.** (c) — every node depends on the central switch.
**7.** (c) — $\frac{8\times7}{2}=28$.
**8.** (c) — 192.168.x.x is private; 172.32 is outside 172.16–172.31.
**9.** (b) — `ipconfig` shows the address details; `ping` tests reachability.
**10.** (b) — 128 bits in eight groups of four hexadecimal digits.
**11.** (c) — controlled access for selected outsiders is an extranet.
**12.** (b) — DHCP is the Dynamic Host Configuration Protocol.
:::

**Group B — Short answer (2 marks each)**

1. Differentiate between bandwidth and throughput with two points. <span class="marks">[2]</span>
2. A 600 MB file is downloaded on a 20 Mbps connection. Find the shortest possible download time. <span class="marks">[2]</span>
3. Give two reasons why optical fibre, not CAT6, should join two school buildings 400 m apart. <span class="marks">[2]</span>
4. What is a gateway? How is it different from a router? <span class="marks">[2]</span>
5. Write two differences between a hub and a switch. <span class="marks">[2]</span>
6. Write the IPv6 address `2001:0db8:0000:0000:0000:0000:0000:0001` in its shortest form and state the length of an IPv6 address in bits. <span class="marks">[2]</span>
7. Differentiate between a static and a dynamic IP address, with one use of each. <span class="marks">[2]</span>
8. What is a data packet? Name two items carried in its header. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Bandwidth is the maximum data rate of a link; throughput is the rate
actually achieved. Bandwidth is fixed by the link or plan; throughput varies
with traffic and signal quality and is never more than the bandwidth.

**2.** 600 MB × 8 = 4,800 Mb; time = 4,800 ÷ 20 = **240 s = 4 minutes**.

**3.** CAT6 is limited to 100 m per run, while fibre carries data for
kilometres; and fibre carries light, so it is immune to electrical interference
and lightning between buildings (it is also faster).

**4.** A gateway connects two networks that use different protocols and
translates between them. A router connects networks that use the same protocol
(IP) and only chooses the path; a home router is the "default gateway" of its
LAN because it is the way out to other networks.

**5.** A hub copies every signal to all ports, while a switch sends each frame
only to the destination's port. On a hub all ports share one bandwidth and
collide; on a switch every port gets the full bandwidth.

**6.** `2001:db8::1`; an IPv6 address is **128 bits** long.

**7.** A static address is set manually and never changes — used for a network
printer or a server. A dynamic address is given automatically by a DHCP server
for a period — used for phones and laptops joining Wi-Fi.

**8.** A data packet is a small unit of data into which a message is broken for
transmission across a network. Its header carries the source address, the
destination address and the packet's sequence number (any two).
:::

**Group C — Long answer (4 marks each)**

1. What is network topology? Explain star and mesh topologies with diagrams, giving one advantage and one disadvantage of each. <span class="marks">[1+3]</span>
2. A school has two buildings 300 m apart. Building A has a lab of 30 computers; Building B has an office with 5 computers and a printer; teachers want Wi-Fi in both. Suggest the media, devices and topology, giving a reason for each choice. <span class="marks">[4]</span>
3. Define IP address. Differentiate between IPv4 and IPv6 in any three points. <span class="marks">[1+3]</span>
4. Explain PAN, LAN, MAN and WAN with one example of each. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Topology is the pattern in which the computers and devices of a network
are connected (1 mark). *Star*: every node has its own cable to a central
switch (draw a switch with six computers around it). Advantage: a faulty cable
affects only one computer and faults are easy to find. Disadvantage: if the
central switch fails, the whole network stops. *Mesh*: nodes are joined by
many links, in a full mesh every node to every other (draw five nodes with all
ten links). Advantage: data takes another path if a link fails. Disadvantage:
very expensive — $n$ nodes need $\frac{n(n-1)}{2}$ cables and $n-1$ ports each.

**2.** *Building A:* a star — a 48-port switch with CAT6 cables to the 30 PCs
(each run under 100 m), because a switch is fast and one bad cable affects one
PC only. *Building B:* a small switch for the 5 PCs and the printer, the printer
given a static IP so everyone can find it. *Between buildings:* optical fibre
with a media converter (or fibre ports) at each end, because 300 m is beyond
copper's 100 m limit and fibre is immune to lightning and interference.
*Internet and Wi-Fi:* one router with a firewall connected to the ISP, acting as
default gateway and DHCP server, and a wireless access point in each building
connected to its switch. The result is a tree (hybrid) topology forming one
campus LAN.

**3.** An IP address is a logical number given to every device on a network
that identifies it and lets packets be routed to it (1 mark). Any three: IPv4 is
32 bits, IPv6 is 128 bits; IPv4 is written in dotted decimal (`192.168.1.1`),
IPv6 in hexadecimal groups with colons (`2001:db8::1`); IPv4 gives about
4.3 × 10⁹ addresses, IPv6 about 3.4 × 10³⁸; IPv4's header is 20–60 bytes,
IPv6's is a fixed 40 bytes; IPv6 configures itself automatically and does not
need NAT.

**4.** *PAN:* devices of one person within about 10 m, e.g. a phone and its
Bluetooth earbuds. *LAN:* computers in one room, building or campus, owned by
one organisation, very fast, e.g. a school computer lab. *MAN:* a network
across a city or valley joining many LANs, e.g. a cable-TV or ISP network in
Kathmandu Valley. *WAN:* a network across a country or the world, using links
of many organisations, e.g. the Internet.
:::
