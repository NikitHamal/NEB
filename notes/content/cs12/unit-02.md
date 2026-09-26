---
subject: Computer Science
grade: 12
unit: 2
title: Data Communication and Networking
hours: 15
---

A computer on its own is a calculator; connected to others it becomes a
communication system. This unit explains how a message gets from one machine to
another — what the pieces of a communication system are, what carries the
signal, what damages it on the way, how machines are addressed, and how the
whole job is divided into layers. At 15 teaching hours this is the largest unit
in the course and it supplies the largest share of the written marks.

::: key What the examiner asks from this unit
Expect the block diagram of a communication system, topologies with their
advantages and disadvantages, guided versus unguided media, the OSI model
(layer names, functions and one protocol each), and IP address classes with a
small calculation. Diagrams earn marks: draw them, label them, and name the
parts.
:::

## 2.1 Basic elements of a communication system

**Data communication** is the exchange of data between two devices through a
transmission medium. For it to happen at all, five elements must be present.

::: definition The five elements of data communication
1. **Message** — the information (data) to be communicated: text, number,
   picture, audio or video.
2. **Sender** — the device that sends the message: a computer, phone, camera.
3. **Receiver** — the device that receives it.
4. **Transmission medium** — the physical path the message travels along:
   cable, fibre or free space.
5. **Protocol** — the agreed set of rules governing the exchange. Without a
   shared protocol two connected devices still cannot understand each other,
   exactly as two people who share no language cannot talk through a working
   telephone.
:::

Four characteristics decide whether a communication system is any good:
**delivery** (to the correct destination), **accuracy** (no altered bits),
**timeliness** (in time to be useful — critical for voice and video), and
**jitter** (even spacing between arriving packets).

## 2.2 Concept of a communication system and its block diagram

A general communication system is described by five functional blocks. This is
the diagram examiners ask for.

```figure caption="Block diagram of a general communication system. The transmitter converts the message into a signal the medium can carry; noise is added on the way; the receiver converts it back."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.15, 2.6))

names = ["Source", "Transmitter", "Transmission\nsystem\n(medium)", "Receiver", "Destination"]
cols  = ["#eef4fa", "#f3eefa", "#eaf3ee", "#f3eefa", "#eef4fa"]
edges = [ACCENT, "#6a5acd", "#2e8b57", "#6a5acd", ACCENT]
x = 0.1
xs = []
for n, fc, ec in zip(names, cols, edges):
    w = 1.45
    ax.add_patch(FancyBboxPatch((x, 1.55), w, 0.85, boxstyle="round,pad=0.05",
                                facecolor=fc, edgecolor=ec, lw=1.2))
    ax.text(x + w/2, 1.97, n, ha="center", va="center", fontsize=6.4, color=INK)
    xs.append((x, x + w))
    x += w + 0.42

for i in range(4):
    ax.annotate("", xy=(xs[i+1][0] - 0.03, 1.97), xytext=(xs[i][1] + 0.03, 1.97),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2, mutation_scale=10))

labels = ["message\n(text, voice)", "signal", "transmitted\nsignal", "received\nsignal",
          "message"]
mids = [xs[0][1] + 0.21, xs[1][1] + 0.21, xs[2][1] + 0.21, xs[3][1] + 0.21]
for m, t in zip(mids, ["signal", "transmitted\nsignal", "received\nsignal", "message"]):
    ax.text(m, 2.62, t, ha="center", va="center", fontsize=6.3, color=MUTED)

# noise
ax.annotate("", xy=(xs[2][0] + 0.72, 1.50), xytext=(xs[2][0] + 0.72, 0.72),
            arrowprops=dict(arrowstyle="-|>", color="#d9534f", lw=1.2, mutation_scale=10))
ax.text(xs[2][0] + 0.72, 0.50, "NOISE\n(thermal, crosstalk, impulse)", ha="center",
        va="center", fontsize=7.0, color="#b02a37")
for i, t in [(0, "e.g. computer"), (1, "e.g. modem"),
             (3, "e.g. modem"), (4, "e.g. computer")]:
    ax.text((xs[i][0] + xs[i][1]) / 2, 1.28, t, ha="center", va="center",
            fontsize=6.2, color=MUTED)

ax.set_xlim(0.0, 9.5); ax.set_ylim(0.25, 2.95)
ax.axis("off")
```

- The **source** produces the data.
- The **transmitter** converts it into a signal the medium can carry — a modem
  modulating digital bits onto an analogue carrier, for example.
- The **transmission system** carries the signal, and unavoidably adds noise.
- The **receiver** converts the received signal back into data — the modem at
  the far end demodulating.
- The **destination** consumes the data.

## 2.3 Elements of data transmission

A **signal** is the electrical, optical or electromagnetic representation of
data. Signals are of two kinds:

| | Analogue signal | Digital signal |
|---|---|---|
| Shape | Continuous wave | Discrete levels (0 and 1) |
| Described by | Amplitude, frequency, phase | Bit rate, bit interval |
| Example | Human voice, radio broadcast | Data inside a computer |
| Noise | Accumulates and cannot be removed | Can be regenerated exactly |

Three more terms are examined constantly:

- **Bandwidth** — for an analogue channel, the range of frequencies it passes,
  in hertz; for a digital channel, the maximum bit rate, in bits per second.
  Larger bandwidth means more data per second.
- **Bit rate** — bits transmitted per second (bps, kbps, Mbps, Gbps).
- **Baud rate** — signal changes per second. If each signal change carries $n$
  bits then $\text{bit rate} = \text{baud rate}\times n$; they are equal only
  when one change carries one bit.
- **Transmission mode** — data may be sent **serially** (one bit after another
  on one wire; cheap, used over any distance) or in **parallel** (n bits at once
  on n wires; fast but only over short distances). Serial transmission is further
  divided into **synchronous** (a continuous stream timed by a shared clock) and
  **asynchronous** (one character at a time framed by start and stop bits).

## 2.4 Simplex, half duplex and full duplex

```figure caption="The three communication modes. Half duplex shares one channel and must take turns; full duplex has capacity in both directions at once."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axes = plt.subplots(3, 1, figsize=(4.8, 3.2))

def dev(ax, x, t):
    ax.add_patch(Rectangle((x - 0.42, 0.28), 0.84, 0.46, facecolor="#eef4fa",
                           edgecolor=ACCENT, lw=1.1))
    ax.text(x, 0.51, t, ha="center", va="center", fontsize=7.4, color=INK)

titles = ["Simplex — one direction only",
          "Half duplex — both directions, one at a time",
          "Full duplex — both directions at once"]
for k, (ax, t) in enumerate(zip(axes, titles)):
    dev(ax, 0.6, "A"); dev(ax, 4.4, "B")
    if k == 0:
        ax.annotate("", xy=(3.92, 0.51), xytext=(1.08, 0.51),
                    arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.5, mutation_scale=12))
        ax.text(2.5, 0.72, "data", ha="center", fontsize=6.8, color=MUTED)
        ax.text(2.5, 0.10, "keyboard → computer, TV broadcast", ha="center",
                fontsize=6.4, color=MUTED)
    elif k == 1:
        ax.annotate("", xy=(3.92, 0.61), xytext=(1.08, 0.61),
                    arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.5, mutation_scale=12))
        ax.annotate("", xy=(1.08, 0.41), xytext=(3.92, 0.41),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2, ls=(0, (3, 2)),
                                    mutation_scale=11))
        ax.text(2.5, 0.10, "walkie-talkie: one talks while the other listens",
                ha="center", fontsize=6.4, color=MUTED)
    else:
        ax.annotate("", xy=(3.92, 0.63), xytext=(1.08, 0.63),
                    arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.5, mutation_scale=12))
        ax.annotate("", xy=(1.08, 0.39), xytext=(3.92, 0.39),
                    arrowprops=dict(arrowstyle="-|>", color="#2e8b57", lw=1.5, mutation_scale=12))
        ax.text(2.5, 0.10, "telephone call, modern Ethernet link", ha="center",
                fontsize=6.4, color=MUTED)
    ax.set_title(t, fontsize=8.0, loc="left", color=INK)
    ax.set_xlim(0.0, 5.0); ax.set_ylim(0.0, 0.92); ax.axis("off")
fig.subplots_adjust(hspace=0.75)
```

| Mode | Direction | Channel capacity used | Example |
|---|---|---|---|
| Simplex | One way only | Full capacity one way | Keyboard to CPU, radio and TV broadcast |
| Half duplex | Both ways, alternately | Full capacity, one direction at a time | Walkie-talkie, old coaxial Ethernet with a hub |
| Full duplex | Both ways simultaneously | Capacity shared, or two separate channels | Telephone, switched Ethernet, mobile call |

## 2.5 Concept of LAN and WAN

A **computer network** is two or more devices connected so that they can share
data and resources. Networks are classified by the area they cover.

```figure caption="Networks classified by geographical coverage. A campus is a LAN, a city is a MAN, and links between cities or countries make a WAN — the Internet being the largest WAN of all."
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, ax = plt.subplots(figsize=(4.8, 3.0))

rings = [(1.05, "LAN", "one room, building or campus\n10 m – 2 km, 100 Mbps – 10 Gbps",
          "#eef4fa", ACCENT),
         (1.95, "MAN", "a city — e.g. all branches in Pokhara\n5 – 50 km", "#f3eefa", "#6a5acd"),
         (2.85, "WAN", "country, continent or the world\nthe Internet", "#eaf3ee", "#2e8b57")]
for r, name, sub, fc, ec in reversed(rings):
    ax.add_patch(Circle((0, 0), r, facecolor=fc, edgecolor=ec, lw=1.3, alpha=0.95))
for (r, name, sub, fc, ec), y in zip(rings, [0.0, 1.50, 2.42]):
    ax.text(0, y, name, ha="center", va="center", fontsize=9.0, color=ec, weight="bold")
    ax.annotate(sub, xy=(0.0, y - 0.22), xytext=(3.25, y - 0.22), fontsize=6.8,
                color=ec, va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=ec, lw=0.7))
ax.set_xlim(-3.1, 9.3); ax.set_ylim(-3.1, 3.1)
ax.set_aspect("equal"); ax.axis("off")
```

| Point | LAN | MAN | WAN |
|---|---|---|---|
| Area | A room, building or campus (up to ~2 km) | A city (5–50 km) | Country to worldwide |
| Ownership | Private — one organisation | One organisation or an ISP | Usually leased from telecom operators |
| Speed | Highest: 100 Mbps to 10 Gbps | High | Lowest per user; long-haul links are shared |
| Error rate | Very low | Low | Higher |
| Media | Twisted pair, fibre, Wi-Fi | Fibre, microwave | Fibre, satellite, leased lines |
| Cost of setup | Low | Medium | High |
| Example | A school computer lab | Cable TV or ISP network inside Kathmandu | The Internet, a bank's branch network |

A **PAN** (personal area network, a few metres — Bluetooth earphones) and a
**CAN** (campus area network) are sometimes added at the small end.

## 2.6 Transmission medium: guided and unguided

::: definition Guided and unguided media
A **guided (bounded/wired)** medium carries the signal along a solid physical
conductor — twisted pair, coaxial cable, optical fibre.
An **unguided (unbounded/wireless)** medium carries the signal through free
space as an electromagnetic wave — radio, microwave, infrared, satellite.
:::

```figure caption="Classification of transmission media."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.15, 2.9))

def nb(x, y, w, t, fc, ec, fs=7.2, h=0.46):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.04",
                                facecolor=fc, edgecolor=ec, lw=1.1))
    ax.text(x, y, t, ha="center", va="center", fontsize=fs, color=INK)

def elbow(x1, y1, x2, y2):
    ym = (y1 + y2) / 2
    ax.plot([x1, x1, x2, x2], [y1, ym, ym, y2], color=MUTED, lw=0.9, zorder=0)

nb(4.25, 3.25, 2.3, "Transmission media", "#f4f6f9", INK, fs=8.0)
nb(2.1, 2.35, 2.0, "Guided (wired)", "#eef4fa", ACCENT, fs=7.6)
nb(6.4, 2.35, 2.2, "Unguided (wireless)", "#eaf3ee", "#2e8b57", fs=7.6)
elbow(4.25, 3.02, 2.1, 2.58); elbow(4.25, 3.02, 6.4, 2.58)

for x, t in [(0.72, "Twisted pair\n(UTP / STP)"), (2.1, "Coaxial\ncable"),
             (3.5, "Optical\nfibre")]:
    nb(x, 1.25, 1.22, t, "white", ACCENT, fs=6.6, h=0.62)
    elbow(2.1, 2.12, x, 1.56)
for x, t in [(5.1, "Radio\nwave"), (6.4, "Micro-\nwave"), (7.7, "Infrared /\nsatellite")]:
    nb(x, 1.25, 1.14, t, "white", "#2e8b57", fs=6.6, h=0.62)
    elbow(6.4, 2.12, x, 1.56)

ax.text(2.1, 0.55, "signal confined in a conductor", ha="center", fontsize=6.6, color=ACCENT)
ax.text(6.4, 0.55, "signal radiated into free space", ha="center", fontsize=6.6, color="#2e8b57")
ax.set_xlim(0.0, 8.5); ax.set_ylim(0.3, 3.6)
ax.axis("off")
```

| Medium | Structure | Typical speed / bandwidth | Range before repeater | Notes |
|---|---|---|---|---|
| **Twisted pair (UTP)** | 4 pairs of insulated copper twisted together; RJ-45 plug | Cat 5e 1 Gbps (100 MHz); Cat 6 up to 10 Gbps over 55 m (250 MHz); Cat 6a 10 Gbps over 100 m (500 MHz) | 100 m | Cheapest, easiest to install; twisting cancels crosstalk; most LAN cabling |
| **STP** | UTP plus a metal shield | Same as UTP | 100 m | Better noise immunity, costlier, must be earthed |
| **Coaxial** | Copper core, insulator, braided shield, jacket | Up to ~1 Gbps; hundreds of MHz | ~500 m | Used by cable TV and cable internet; obsolete for LANs |
| **Optical fibre** | Glass core + cladding; light is carried by total internal reflection | Tbps possible; 10–100 Gbps routine | Many km (single-mode > 40 km) | Immune to EMI, very secure, very high bandwidth; costly, needs skilled splicing |
| **Radio wave** | Omnidirectional, 3 kHz–1 GHz | Up to a few hundred Mbps | Tens of km | Penetrates walls; FM radio, older wireless |
| **Microwave** | Line-of-sight dish, 1–300 GHz | Hundreds of Mbps to Gbps | ~50 km per hop | Needs clear line of sight; Wi-Fi uses 2.4, 5 and 6 GHz |
| **Infrared** | Line-of-sight light, < 1 mm wavelength | Low to moderate | A few metres | Cannot pass through walls, so it is secure inside a room; TV remotes |
| **Satellite** | Microwave relayed by a satellite | High | Global | Large propagation delay for geostationary satellites (~250 ms one way) |

| Point | Guided | Unguided |
|---|---|---|
| Path | Along a physical conductor | Through free space |
| Direction | Point-to-point | Usually broadcast |
| Interference | Low (shielded) | High (weather, obstacles, other transmitters) |
| Security | Higher — tapping needs physical access | Lower — anyone in range can receive |
| Installation | Cabling work, hard in difficult terrain | Quick, reaches remote hills and islands |
| Mobility | None | Full |

> **Current practice (2026).** Wi-Fi 6/6E (IEEE 802.11ax) is the mainstream
> wireless LAN standard; **Wi-Fi 7 (802.11be)** was published in July 2025 and
> adds 320 MHz channels and 4096-QAM, and **Wi-Fi 8 (802.11bn)** is still under
> development with an expected release around 2028. Nepal's fixed broadband is
> now mostly **FTTH** (fibre to the home); mobile data runs on 4G LTE, which
> Nepal Telecom launched on 1 January 2017 — 5G in Nepal has so far only
> reached the trial stage.

## 2.7 Transmission impairments

A signal that arrives is never exactly the signal that was sent. The differences
are **impairments**.

| Impairment | What it is | Cause | Cure |
|---|---|---|---|
| **Attenuation** | Loss of signal strength with distance | Resistance of the medium | Amplifier (analogue), repeater (digital) |
| **Distortion** | Change in the *shape* of the signal | Different frequency components travel at different speeds | Equalisers; limit the bandwidth used |
| **Noise** | Unwanted energy added to the signal | See the four types below | Shielding, twisting, error detection |
| **Crosstalk** | Signal from one wire leaks into a neighbouring wire — you faintly hear another conversation | Electromagnetic coupling between adjacent conductors | Twisting the pairs, shielding (STP), fibre |
| **Echo** | The signal is reflected back to the sender, who hears a delayed copy of themselves | Impedance mismatch at a junction or hybrid | Echo suppressors and echo cancellers |
| **Singing** | A continuous howling or whistling tone — an echo that has become self-sustaining feedback | Echo plus excessive amplifier gain going round a loop | Reduce gain, use echo cancellers |
| **Jitter** | Variation in the arrival time (delay) of successive packets | Varying queueing delay in routers | Jitter buffer at the receiver, QoS |
| **Bandwidth** | A *limit*, not a fault: the channel simply cannot carry frequencies (or bit rates) above its bandwidth, so fast signals are rounded off | Physical properties of the medium | Use a wider medium — fibre instead of copper |
| **Number of receivers** | Each extra receiver tapped onto a line draws power and adds a reflection, so the signal weakens and distorts | Loading of the line | Use point-to-point links and switches instead of a shared bus |

The four standard kinds of **noise**: **thermal** (random electron motion,
present in every conductor, also called white noise), **intermodulation**
(two frequencies mixing to produce a third), **crosstalk**, and **impulse**
(sudden spikes from lightning or switching — the worst for digital data).

## 2.8 Network architecture: client–server and peer-to-peer

```figure caption="Client–server: all shared resources sit on a dedicated server. Peer-to-peer: every computer is both client and server to the others."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
fig, axes = plt.subplots(1, 2, figsize=(5.15, 2.7))

def pc(ax, x, y, t, fc="white", ec=MUTED):
    ax.add_patch(Rectangle((x - 0.34, y - 0.22), 0.68, 0.44, facecolor=fc,
                           edgecolor=ec, lw=1.0))
    ax.text(x, y - 0.42, t, ha="center", va="center", fontsize=6.4, color=MUTED)

ax = axes[0]
ax.add_patch(FancyBboxPatch((1.25, 2.15), 1.5, 0.66, boxstyle="round,pad=0.04",
                            facecolor="#eef4fa", edgecolor=ACCENT, lw=1.3))
ax.text(2.0, 2.48, "SERVER", ha="center", va="center", fontsize=7.8, color=INK,
        weight="bold")
ax.text(2.0, 1.94, "files, database, printer", ha="center", fontsize=6.3, color=MUTED,
        zorder=5, bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
for i, t in enumerate(["Client 1", "Client 2", "Client 3"]):
    x = 0.65 + i*1.35
    pc(ax, x, 0.95, t)
    ax.plot([x, 2.0], [1.19, 2.12], color="#8a8f99", lw=0.9, zorder=0)
ax.set_title("Client–server", fontsize=9.0)
ax.set_xlim(0.0, 4.0); ax.set_ylim(0.3, 3.0); ax.axis("off")

ax = axes[1]
pts = [(0.75, 2.35, "PC A"), (3.25, 2.35, "PC B"), (0.75, 0.95, "PC C"), (3.25, 0.95, "PC D")]
for x, y, t in pts:
    pc(ax, x, y, t, fc="#eaf3ee", ec="#2e8b57")
import itertools
for (x1, y1, _), (x2, y2, _) in itertools.combinations(pts, 2):
    ax.plot([x1, x2], [y1, y2], color="#2e8b57", lw=0.8, alpha=0.75, zorder=0)
ax.set_title("Peer-to-peer", fontsize=9.0)
ax.set_xlim(0.0, 4.0); ax.set_ylim(0.3, 3.0); ax.axis("off")
fig.subplots_adjust(wspace=0.05)
```

| Point | Client–server | Peer-to-peer |
|---|---|---|
| Roles | Dedicated server provides, clients request | Every node is both client and server |
| Best size | Medium to very large networks | Up to about 10 computers |
| Cost | High — server hardware, server OS, admin | Low — ordinary PCs, no extra software |
| Administration | Centralised: one place for accounts, backup, security | Each user administers their own machine |
| Security | Strong, centrally enforced | Weak, depends on every user |
| Performance | Scales well; server may become a bottleneck | Degrades as the number of peers grows |
| Failure | Server down = network unusable | One peer down affects only its own shares |
| Example | A school's ERP, any website | File and printer sharing in a small office; BitTorrent |

## 2.9 Basic terms

| Term | Meaning |
|---|---|
| **IP address** | A logical address identifying a host on a network. IPv4 is 32 bits written as four decimal octets (`202.79.32.33`); IPv6 is 128 bits written in hexadecimal. Assigned by software; changes when the host moves network. |
| **Subnet mask** | A 32-bit number of consecutive 1s then 0s (`255.255.255.0`) that tells a host which part of an IP address is the **network** and which is the **host**. |
| **Default gateway** | The IP address of the router interface on your own network. Any packet whose destination is outside the local network is handed to the gateway. |
| **MAC address** | The 48-bit physical address burned into a NIC by its manufacturer, written as 12 hexadecimal digits (`00:1A:2B:3C:4D:5E`). The first 24 bits are the manufacturer's OUI. Permanent and globally unique; works only within one LAN. |
| **Internet** | The global public network of networks, using TCP/IP; open to everyone. |
| **Intranet** | A private network inside one organisation using the same Internet technologies (web, email), accessible only to its employees. |
| **Extranet** | A controlled extension of an intranet to selected outsiders — suppliers, dealers, partners — usually over a VPN with a login. |

::: caution IP address vs MAC address
The MAC address is **physical, permanent and local** — it identifies a NIC and is
used by switches inside one LAN (OSI layer 2). The IP address is **logical,
changeable and global** — it identifies a host on the Internet and is used by
routers (layer 3). Moving a laptop from your school to a cybercafé changes its IP
address but never its MAC address.
:::

## 2.10 Network tools

- **Cisco Packet Tracer** — a free network *simulator*. You drag routers,
  switches, PCs and cables onto a canvas, configure them, and watch animated
  packets travel hop by hop. It lets a student build and debug a whole network
  without owning any hardware, so it is the standard lab tool for this course.
- **Remote login** — working on a distant computer as though you were sitting at
  it. **Telnet** (port 23) was the original tool but sends everything, including
  the password, as plain text; it has been replaced by **SSH** (Secure Shell,
  port 22), which encrypts the whole session. For a graphical desktop, Windows
  uses **RDP** (port 3389), and VNC and AnyDesk are common alternatives.
- Small diagnostic commands worth knowing: `ping` (is the host reachable, and
  how long does a round trip take), `tracert`/`traceroute` (list the routers
  along the path), `ipconfig`/`ifconfig` (show my IP address, mask and gateway),
  and `nslookup` (find the IP address behind a domain name).

## 2.11 Network connecting devices

```figure caption="A small campus network. The NIC attaches each host, a switch forms the LAN, the router joins two networks, and the modem converts the LAN's digital data for the ISP's line."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.15, 3.0))

def pc(x, y, t):
    ax.add_patch(Rectangle((x - 0.33, y - 0.22), 0.66, 0.44, facecolor="white",
                           edgecolor=MUTED, lw=1.0))
    ax.text(x, y, "PC", ha="center", va="center", fontsize=6.4, color=INK)
    ax.text(x, y - 0.40, t, ha="center", va="center", fontsize=6.0, color=MUTED)

def dev(x, y, w, t, fc, ec):
    ax.add_patch(FancyBboxPatch((x - w/2, y - 0.25), w, 0.50, boxstyle="round,pad=0.04",
                                facecolor=fc, edgecolor=ec, lw=1.2))
    ax.text(x, y, t, ha="center", va="center", fontsize=7.0, color=INK)

for i in range(3):
    pc(0.7 + i*1.15, 2.60, "")
    ax.plot([0.7 + i*1.15, 1.85], [2.38, 1.75], color="#8a8f99", lw=0.9, zorder=0)
ax.annotate("each PC has a NIC", xy=(3.37, 2.60), xytext=(3.62, 2.74),
            fontsize=6.4, color=MUTED, va="center", ha="left",
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
dev(1.85, 1.50, 1.7, "SWITCH  (layer 2)", "#eef4fa", ACCENT)
ax.plot([1.85, 1.85], [1.25, 0.95], color="#8a8f99", lw=0.9, zorder=0)
dev(1.85, 0.70, 1.7, "ROUTER  (layer 3)", "#f3eefa", "#6a5acd")
ax.annotate("", xy=(3.55, 0.70), xytext=(2.72, 0.70),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1, mutation_scale=10))
dev(4.4, 0.70, 1.6, "MODEM", "#eaf3ee", "#2e8b57")
ax.annotate("", xy=(6.1, 0.70), xytext=(5.22, 0.70),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1, mutation_scale=10))
ax.text(6.25, 0.70, "ISP / Internet", fontsize=7.4, color=INK, va="center")
ax.text(3.13, 0.90, "digital", fontsize=6.0, color=MUTED, ha="center")
ax.text(5.66, 0.28, "analogue / optical", fontsize=6.0, color=MUTED, ha="center")
ax.annotate("one LAN\n(one broadcast domain)", xy=(2.75, 1.60), xytext=(3.15, 1.95),
            fontsize=6.4, color=ACCENT, va="center",
            arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.7))
ax.set_xlim(0.0, 8.3); ax.set_ylim(0.14, 3.15)
ax.axis("off")
```

| Device | OSI layer | Function |
|---|---|---|
| **NIC** (network interface card) | 1 and 2 | Connects a computer to the medium; holds the MAC address; converts parallel data to serial signals |
| **Modem** (modulator–demodulator) | 1 | Modulates digital data onto an analogue carrier to send, demodulates on receipt — needed on telephone, cable and DSL lines |
| **Repeater** | 1 | Regenerates a weakened signal to extend distance |
| **Hub** | 1 | Multiport repeater: copies an incoming frame to *every* other port. Obsolete — wastes bandwidth and causes collisions |
| **Bridge** | 2 | Joins two LAN segments and filters traffic by MAC address |
| **Switch** | 2 | Multiport bridge: learns which MAC address is on which port and forwards each frame only to that port. Full duplex, no collisions |
| **Router** | 3 | Joins *different* networks, reads the destination IP address and chooses the best path from its routing table |
| **Gateway** | All 7 | Joins networks that use different protocols, translating between them |

## 2.12 Network topologies

::: definition Topology
A **topology** is the arrangement of the nodes and links of a network. The
**physical** topology is how the cables actually run; the **logical** topology is
how data flows. A modern Ethernet network is usually a physical star that behaves
logically like a bus.
:::

```figure caption="The three basic topologies. Bus: one shared backbone with terminators. Star: every node to a central switch. Ring: each node to the next, closing a loop."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, axes = plt.subplots(1, 3, figsize=(5.15, 2.3))

def node(ax, x, y, t="", r=0.16, fc="#eef4fa", ec=ACCENT):
    ax.add_patch(Circle((x, y), r, facecolor=fc, edgecolor=ec, lw=1.1, zorder=3))
    if t:
        ax.text(x, y, t, ha="center", va="center", fontsize=5.6, color=INK, zorder=4)

# ---- BUS
ax = axes[0]
ax.plot([0.25, 2.75], [1.15, 1.15], color=INK, lw=2.0, zorder=1)
for xx in (0.25, 2.75):
    ax.plot([xx, xx], [1.0, 1.3], color="#d9534f", lw=2.2)
ax.text(0.25, 0.80, "terminator", fontsize=5.4, color="#d9534f", ha="center")
ax.text(2.75, 0.80, "terminator", fontsize=5.4, color="#d9534f", ha="center")
for i, xx in enumerate([0.75, 1.5, 2.25]):
    ax.plot([xx, xx], [1.15, 1.72], color=MUTED, lw=0.9, zorder=1)
    node(ax, xx, 1.9)
for i, xx in enumerate([1.1, 1.9]):
    ax.plot([xx, xx], [1.15, 0.58], color=MUTED, lw=0.9, zorder=1)
    node(ax, xx, 0.40)
ax.set_title("Bus", fontsize=9.0)
ax.set_xlim(0.0, 3.0); ax.set_ylim(0.1, 2.25)

# ---- STAR
ax = axes[1]
cx, cy = 1.5, 1.2
ax.add_patch(Rectangle((cx-0.34, cy-0.18), 0.68, 0.36, facecolor="#f3eefa",
                       edgecolor="#6a5acd", lw=1.2, zorder=3))
ax.text(cx, cy, "switch", ha="center", va="center", fontsize=5.6, color=INK, zorder=4)
for a in np.linspace(0, 2*np.pi, 7)[:-1]:
    x, y = cx + 0.95*np.cos(a), cy + 0.88*np.sin(a)
    ax.plot([cx, x], [cy, y], color=MUTED, lw=0.9, zorder=1)
    node(ax, x, y)
ax.set_title("Star", fontsize=9.0)
ax.set_xlim(0.0, 3.0); ax.set_ylim(0.1, 2.25)

# ---- RING
ax = axes[2]
cx, cy, R = 1.5, 1.2, 0.85
angs = np.linspace(0, 2*np.pi, 7)[:-1]
pts = [(cx + R*np.cos(a), cy + R*np.sin(a)) for a in angs]
for i in range(len(pts)):
    x1, y1 = pts[i]; x2, y2 = pts[(i+1) % len(pts)]
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.9,
                                shrinkA=9, shrinkB=9, mutation_scale=7), zorder=1)
for x, y in pts:
    node(ax, x, y)
ax.text(cx, cy, "token\npasses\none way", ha="center", va="center",
        fontsize=5.0, color=MUTED)
ax.set_title("Ring", fontsize=9.0)
ax.set_xlim(0.0, 3.0); ax.set_ylim(0.1, 2.25)
for ax in axes:
    ax.set_aspect("equal"); ax.axis("off")
fig.subplots_adjust(wspace=0.05)
```

```figure caption="Three further topologies. Mesh: every node linked to every other. Tree: stars joined into a hierarchy. Hybrid: a mixture — here a star of a bus, a ring and a star."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, axes = plt.subplots(1, 3, figsize=(5.15, 2.3))

def node(ax, x, y, r=0.15, fc="#eef4fa", ec=ACCENT):
    ax.add_patch(Circle((x, y), r, facecolor=fc, edgecolor=ec, lw=1.1, zorder=3))

def hub(ax, x, y, w=0.56, h=0.30, fc="#f3eefa", ec="#6a5acd"):
    ax.add_patch(Rectangle((x-w/2, y-h/2), w, h, facecolor=fc, edgecolor=ec,
                           lw=1.1, zorder=3))

# ---- MESH
ax = axes[0]
angs = np.linspace(np.pi/2, 2.5*np.pi, 6)[:-1]
pts = [(1.5 + 0.88*np.cos(a), 1.2 + 0.88*np.sin(a)) for a in angs]
import itertools
for (x1, y1), (x2, y2) in itertools.combinations(pts, 2):
    ax.plot([x1, x2], [y1, y2], color="#8a8f99", lw=0.7, zorder=1)
for x, y in pts:
    node(ax, x, y)
ax.text(1.5, 0.12, "n(n−1)/2 links", ha="center", fontsize=6.0, color=MUTED)
ax.set_title("Mesh", fontsize=9.0)

# ---- TREE
ax = axes[1]
hub(ax, 1.5, 2.05, w=0.70)
for i, hx in enumerate([0.75, 2.25]):
    hub(ax, hx, 1.25)
    ax.plot([1.5, hx], [1.90, 1.40], color=MUTED, lw=0.9, zorder=1)
    for dx in (-0.36, 0.0, 0.36):
        ax.plot([hx, hx+dx], [1.10, 0.55], color=MUTED, lw=0.8, zorder=1)
        node(ax, hx+dx, 0.40, r=0.13)
ax.text(1.5, 2.05, "root", ha="center", va="center", fontsize=5.4, color=INK, zorder=4)
ax.set_title("Tree", fontsize=9.0)

# ---- HYBRID
ax = axes[2]
hub(ax, 1.5, 1.95, w=0.62)
ax.text(1.5, 1.95, "core", ha="center", va="center", fontsize=5.4, color=INK, zorder=4)
# bus branch (left)
ax.plot([1.5, 0.55], [1.80, 1.35], color=MUTED, lw=0.9, zorder=1)
ax.plot([0.15, 0.95], [1.25, 1.25], color=INK, lw=1.6, zorder=1)
for xx in (0.32, 0.78):
    ax.plot([xx, xx], [1.25, 1.02], color=MUTED, lw=0.8, zorder=1)
    node(ax, xx, 0.88, r=0.12)
ax.text(0.55, 1.45, "bus", fontsize=5.6, color=MUTED, ha="center")
# ring branch (right)
ax.plot([1.5, 2.45], [1.80, 1.45], color=MUTED, lw=0.9, zorder=1)
rp = [(2.45 + 0.38*np.cos(a), 1.05 + 0.38*np.sin(a)) for a in np.linspace(0, 2*np.pi, 5)[:-1]]
for i in range(4):
    x1, y1 = rp[i]; x2, y2 = rp[(i+1) % 4]
    ax.plot([x1, x2], [y1, y2], color="#8a8f99", lw=0.8, zorder=1)
for x, y in rp:
    node(ax, x, y, r=0.11)
ax.text(2.45, 1.58, "ring", fontsize=5.6, color=MUTED, ha="center")
# star branch (bottom)
ax.plot([1.5, 1.5], [1.80, 0.92], color=MUTED, lw=0.9, zorder=1)
hub(ax, 1.5, 0.78, w=0.42, h=0.24, fc="#eaf3ee", ec="#2e8b57")
for dx in (-0.34, 0.0, 0.34):
    ax.plot([1.5, 1.5+dx], [0.66, 0.34], color=MUTED, lw=0.8, zorder=1)
    node(ax, 1.5+dx, 0.22, r=0.11)
ax.text(1.76, 0.80, "star", fontsize=5.6, color=MUTED, ha="left")
ax.set_title("Hybrid", fontsize=9.0)

for ax in axes:
    ax.set_xlim(0.0, 3.0); ax.set_ylim(0.0, 2.35)
    ax.set_aspect("equal"); ax.axis("off")
fig.subplots_adjust(wspace=0.05)
```

| Topology | Advantages | Disadvantages |
|---|---|---|
| **Bus** | Least cable, cheapest, easy to extend for a few nodes | One break in the backbone kills the whole network; collisions rise with traffic; hard to fault-find; needs terminators |
| **Star** | One cable fault affects one node only; easy to add or remove nodes; easy to manage; no collisions with a switch | Needs the most cable; the central switch is a single point of failure |
| **Ring** | Equal access for every node; no collisions (token passing); signal is regenerated at each node so it travels far | A single node or link failure breaks the ring (unless it is a dual ring); adding a node interrupts service; slow with many nodes |
| **Mesh** | Most reliable — many alternative paths; no traffic sharing; privacy | Very expensive: $n(n-1)/2$ links and $n-1$ ports per node; hard to install |
| **Tree** | Scales well; hierarchical, so easy to manage and to isolate groups | Failure of the root or a branch hub disconnects everything below it; much cabling |
| **Hybrid** | Combines the strengths of its parts; very flexible; scales to any size | Complex to design and manage; costly |

::: example Worked example 2.1 — cost of a mesh
**Problem.** A mesh network connects 8 computers. How many cables are needed, how
many ports must each computer have, and how many cables would a star with the
same 8 computers need?

**Solution.** In a full mesh every pair of nodes has its own link, so the number
of cables is

$$ \frac{n(n-1)}{2} = \frac{8\times 7}{2} = 28\ \text{cables} $$

and each computer needs $n-1 = 7$ ports. A star needs one cable per node, i.e.
**8 cables**, plus a switch with 8 ports. The mesh costs 3.5 times as much
cable here, and the ratio grows with $n$ — which is why mesh is used only for
backbone links where reliability is worth the price.
:::

## 2.13 Basic concept of the OSI reference model

The **OSI (Open Systems Interconnection)** model was published by **ISO in 1984**.
It is a *reference* model: it divides the work of communication into seven
independent layers, so that any layer may be changed without disturbing the rest.
Data travels **down** the seven layers at the sender, across the medium, and
**up** the seven layers at the receiver. Each layer adds its own header to the
data it receives from above — this is called **encapsulation**.

```figure caption="The seven-layer OSI model beside the four-layer TCP/IP model, with the unit of data (PDU) and an example protocol at each level."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.15, 4.0))

osi = [("7  Application", "HTTP, FTP, SMTP, DNS", "#eef4fa"),
       ("6  Presentation", "TLS, JPEG, ASCII", "#eef4fa"),
       ("5  Session", "NetBIOS, RPC", "#eef4fa"),
       ("4  Transport", "TCP, UDP   —  segment", "#f3eefa"),
       ("3  Network", "IP, ICMP   —  packet", "#eaf3ee"),
       ("2  Data link", "Ethernet, PPP   —  frame", "#fdf3e6"),
       ("1  Physical", "cables, RJ-45   —  bit", "#fdecec")]
tcp = [("Application", 3, "#eef4fa"), ("Transport", 1, "#f3eefa"),
       ("Internet", 1, "#eaf3ee"), ("Network access", 2, "#fdf3e6")]

h = 0.52
for i, (name, proto, fc) in enumerate(osi):
    y = (6 - i) * h + 0.55
    ax.add_patch(Rectangle((0.55, y), 2.35, h, facecolor=fc, edgecolor=INK, lw=0.9))
    ax.text(0.67, y + h/2, name, ha="left", va="center", fontsize=7.4, color=INK)
    ax.text(3.02, y + h/2, proto, ha="left", va="center", fontsize=6.6, color=MUTED)

y = 0.55
for name, span, fc in reversed(tcp):
    ax.add_patch(Rectangle((5.45, y), 1.75, h*span, facecolor=fc, edgecolor=INK, lw=0.9))
    ax.text(6.32, y + h*span/2, name, ha="center", va="center", fontsize=7.4, color=INK)
    y += h*span

ax.text(1.72, 4.35, "OSI  (ISO, 1984)", ha="center", fontsize=8.6, color=INK, weight="bold")
ax.text(6.32, 4.35, "TCP/IP", ha="center", fontsize=8.6, color=INK, weight="bold")
ax.annotate("", xy=(0.30, 0.40), xytext=(0.30, 4.12),
            arrowprops=dict(arrowstyle="-|>", color="#d9534f", lw=1.1, mutation_scale=10))
ax.text(0.42, 0.22, "sender: data travels down, each layer adds a header",
        fontsize=6.3, color="#b02a37")
ax.set_xlim(0.0, 7.6); ax.set_ylim(0.1, 4.55)
ax.axis("off")
```

| # | Layer | Main function | PDU | Protocol / device |
|---|---|---|---|---|
| 7 | Application | Provides network services to the user's program | Data | HTTP, FTP, SMTP, DNS, Telnet |
| 6 | Presentation | Translation of formats, encryption/decryption, compression | Data | TLS/SSL, JPEG, MPEG, ASCII |
| 5 | Session | Establishes, manages, synchronises and terminates sessions | Data | NetBIOS, RPC, PPTP |
| 4 | Transport | End-to-end delivery, segmentation and reassembly, flow control, error control; port numbers | Segment | TCP (reliable), UDP (fast) |
| 3 | Network | Logical (IP) addressing and routing between networks | Packet | IP, ICMP — **router** |
| 2 | Data link | Framing, physical (MAC) addressing, error detection by CRC, access control | Frame | Ethernet, PPP — **switch, bridge** |
| 1 | Physical | Transmits raw bits: voltages, connectors, cables, data rate | Bit | RJ-45, fibre — **hub, repeater** |

::: memory Remembering the seven layers
Top-down (7→1): **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing.
Bottom-up (1→7): **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way.
:::

| Point | OSI | TCP/IP |
|---|---|---|
| Layers | 7 | 4 (Application, Transport, Internet, Network access) |
| Developed by | ISO, 1984 | US DoD/ARPANET, 1970s |
| Status | A theoretical reference model | The model actually used on the Internet |
| Layer independence | Strictly separated | Application layer merges OSI 5, 6 and 7 |
| Approach | Protocol-independent standard | Built around existing protocols (TCP, IP) |

## 2.14 Internet protocol addressing

An **IPv4** address is 32 bits, written as four decimal **octets** separated by
dots — *dotted decimal notation*. Each octet is 0–255, so the whole space holds
$2^{32} \approx 4.3$ billion addresses. Every address has a **network part**
(which network) and a **host part** (which machine on it); the subnet mask marks
the boundary.

```figure caption="IPv4 address classes. The leading bits fix the class, which fixes how many octets are network and how many are host."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.15, 3.0))

rows = [("A", 1, "0", "1 – 126", "255.0.0.0", "#eef4fa"),
        ("B", 2, "10", "128 – 191", "255.255.0.0", "#f3eefa"),
        ("C", 3, "110", "192 – 223", "255.255.255.0", "#eaf3ee"),
        ("D", 0, "1110", "224 – 239", "multicast", "#fdf3e6"),
        ("E", 0, "1111", "240 – 255", "reserved", "#fdecec")]
ow, h = 0.82, 0.44
X0 = 0.95
for i, (cls, nnet, bits, rng, mask, fc) in enumerate(rows):
    y = (4 - i) * (h + 0.11) + 0.42
    ax.text(0.05, y + h/2, "Class " + cls, fontsize=7.2, color=INK, va="center")
    if nnet == 0:
        ax.add_patch(Rectangle((X0, y), 4*ow, h, facecolor="white",
                               edgecolor=INK, lw=0.9))
        ax.text(X0 + 2*ow, y + h/2, "not assigned to hosts", ha="center",
                va="center", fontsize=6.4, color=MUTED)
    else:
        for j in range(4):
            isnet = j < nnet
            ax.add_patch(Rectangle((X0 + j*ow, y), ow, h,
                                   facecolor=fc if isnet else "white",
                                   edgecolor=INK, lw=0.9))
            ax.text(X0 + j*ow + ow/2, y + h/2, "net" if isnet else "host",
                    ha="center", va="center", fontsize=6.4,
                    color=INK if isnet else MUTED)
    ax.text(5.05, y + h/2, bits, ha="center", va="center", fontsize=6.4, color=MUTED)
    ax.text(6.35, y + h/2, rng, ha="center", va="center", fontsize=6.4, color=MUTED)
    ax.text(8.05, y + h/2, mask, ha="center", va="center", fontsize=6.4, color=MUTED)

for j, t in enumerate(["octet 1", "octet 2", "octet 3", "octet 4"]):
    ax.text(X0 + j*ow + ow/2, 3.32, t, ha="center", fontsize=6.4, color=MUTED)
for x, t in [(5.05, "first bits"), (6.35, "1st octet"), (8.05, "default mask")]:
    ax.text(x, 3.32, t, ha="center", fontsize=6.6, color=INK)
ax.plot([0.95, 8.85], [3.20, 3.20], color=MUTED, lw=0.7)
ax.text(0.95, 0.15, "network part is coloured;  host part is white;  "
                    "8 bits per octet, 32 bits in all",
        fontsize=6.4, color=MUTED)
ax.set_xlim(0.0, 9.2); ax.set_ylim(0.02, 3.55)
ax.axis("off")
```

| Class | First bits | First octet | Default mask | Networks | Hosts per network | Use |
|---|---|---|---|---|---|---|
| A | 0 | 1 – 126 | 255.0.0.0 (/8) | 126 | 16,777,214 | Very large organisations |
| B | 10 | 128 – 191 | 255.255.0.0 (/16) | 16,384 | 65,534 | Medium organisations |
| C | 110 | 192 – 223 | 255.255.255.0 (/24) | 2,097,152 | 254 | Small networks |
| D | 1110 | 224 – 239 | — | — | — | Multicast |
| E | 1111 | 240 – 255 | — | — | — | Reserved / experimental |

Two subtractions to remember: the host part of all 0s is the **network address**
and all 1s is the **broadcast address**, so a network with $n$ host bits has
$2^{n}-2$ usable hosts. `127.0.0.0/8` is reserved for **loopback**
(`127.0.0.1` is always "this computer"), which is why class A stops at 126.

**Private addresses** are never routed on the Internet and may be reused inside
any organisation: `10.0.0.0/8`, `172.16.0.0/12` and `192.168.0.0/16`. A router
performing **NAT** (Network Address Translation) lets a whole school share one
public address.

::: example Worked example 2.2 — reading an address and its mask
**Problem.** A computer is configured with IP address `192.168.10.37` and subnet
mask `255.255.255.0`. Find (a) its class, (b) the network address, (c) the
broadcast address, (d) the number of usable host addresses, and (e) write the IP
address in binary.

**Solution.**

(a) The first octet is 192, which lies in 192–223, so it is **class C** (and it
is a private address).

(b) The mask `255.255.255.0` means the first 24 bits are network. Set the host
octet to 0: **network address = 192.168.10.0**.

(c) Set the host octet to all 1s (255): **broadcast address = 192.168.10.255**.

(d) 8 host bits remain, so $2^{8}-2 = 256-2 = \textbf{254}$ usable addresses,
namely 192.168.10.1 to 192.168.10.254.

(e) Each octet in 8 bits: $192 = 11000000$, $168 = 10101000$, $10 = 00001010$,
$37 = 00100101$, so the address is

`11000000.10101000.00001010.00100101`
:::

::: example Worked example 2.3 — simple subnetting
**Problem.** The network `192.168.1.0/24` must be divided into 4 subnets. Give
the new subnet mask, and for each subnet the network address, the usable host
range and the broadcast address.

**Solution.** To make 4 subnets we must borrow $b$ host bits with $2^{b} \ge 4$,
so $b = 2$. The prefix becomes $24 + 2 = 26$, and the mask is

$$ /26 = 255.255.255.192 $$

because the last octet 11000000 is 192. Host bits left $= 32-26 = 6$, so each
subnet holds $2^{6} = 64$ addresses of which $64-2 = 62$ are usable. The block
size is 64, so the subnets start at 0, 64, 128 and 192:

| Subnet | Network address | Usable host range | Broadcast |
|---|---|---|---|
| 1 | 192.168.1.0 | 192.168.1.1 – 192.168.1.62 | 192.168.1.63 |
| 2 | 192.168.1.64 | 192.168.1.65 – 192.168.1.126 | 192.168.1.127 |
| 3 | 192.168.1.128 | 192.168.1.129 – 192.168.1.190 | 192.168.1.191 |
| 4 | 192.168.1.192 | 192.168.1.193 – 192.168.1.254 | 192.168.1.255 |

Check: $4 \times 64 = 256$ addresses, the whole class C block.
:::

::: caution Do not forget the two reserved addresses
A /24 network has 256 addresses but only **254** usable ones — the all-zeros
network address and the all-ones broadcast address can never be given to a
computer. Writing 256 (or 255) in an exam loses the mark.
:::

**IPv6.** Because IPv4's 4.3 billion addresses ran out — IANA's free pool was
exhausted in February 2011 — the Internet is migrating to **IPv6**, which uses
**128 bits** written as eight groups of four hexadecimal digits, for example
`2001:0db8:85a3:0000:0000:8a2e:0370:7334`. It gives about $3.4\times10^{38}$
addresses, has no broadcast (it uses multicast instead), and needs no NAT.
Adoption has been slow but steady: traffic to Google from IPv6 users passed
**50% for the first time in March 2026**, up from roughly 43% at the start of 2025.

## Chapter summary

- The five elements of data communication are message, sender, receiver,
  transmission medium and protocol; the communication model is
  source → transmitter → transmission system → receiver → destination, with
  noise added in the middle.
- Simplex = one direction; half duplex = both directions alternately; full
  duplex = both directions at once.
- LAN (a building, private, fastest) ⊂ MAN (a city) ⊂ WAN (country or world;
  the Internet is the largest WAN).
- Guided media (twisted pair, coaxial, fibre) confine the signal in a conductor;
  unguided media (radio, microwave, infrared, satellite) radiate it into space.
  Fibre has the highest bandwidth and immunity to interference.
- Impairments: attenuation, distortion, noise (thermal, intermodulation,
  crosstalk, impulse), echo, singing, jitter; bandwidth and the number of
  receivers limit what a channel can do.
- Client–server centralises resources and security; peer-to-peer is cheap and
  suits fewer than ten machines.
- MAC address = 48-bit, physical, permanent, layer 2. IP address = 32-bit
  (IPv4), logical, changeable, layer 3. Subnet mask splits network from host;
  the gateway is the router's address.
- Topologies: bus (one backbone, terminators), star (central switch), ring
  (one-way loop), mesh ($n(n-1)/2$ links), tree (hierarchy of stars), hybrid.
- OSI has 7 layers — Physical, Data link, Network, Transport, Session,
  Presentation, Application — against TCP/IP's 4. Routers work at layer 3,
  switches at layer 2, hubs and repeaters at layer 1.
- IPv4 classes: A (1–126, /8), B (128–191, /16), C (192–223, /24), D multicast,
  E reserved. A network with $n$ host bits has $2^{n}-2$ usable hosts. IPv6 is
  128 bits.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which is **not** one of the five elements of data communication? <span class="marks">[1]</span>
   (a) message (b) protocol (c) bandwidth (d) transmission medium
2. A walkie-talkie is an example of which communication mode? <span class="marks">[1]</span>
   (a) simplex (b) half duplex (c) full duplex (d) broadcast
3. Which device works at the network layer of the OSI model? <span class="marks">[1]</span>
   (a) hub (b) switch (c) router (d) repeater
4. The default subnet mask of a class B address is <span class="marks">[1]</span>
   (a) 255.0.0.0 (b) 255.255.0.0 (c) 255.255.255.0 (d) 255.255.255.255
5. In which topology does the failure of the central device stop the whole network? <span class="marks">[1]</span>
   (a) bus (b) ring (c) star (d) mesh
6. A MAC address is how many bits long? <span class="marks">[1]</span>
   (a) 32 (b) 48 (c) 64 (d) 128
7. Unwanted coupling of a signal from one wire into a neighbouring wire is called <span class="marks">[1]</span>
   (a) echo (b) jitter (c) crosstalk (d) attenuation

::: note Answers to Group A
**1.** (c) — bandwidth is a property of the channel, not one of the five elements.
**2.** (b) — both can talk, but only one at a time, over one shared channel.
**3.** (c) — routers read IP addresses, which live at layer 3.
**4.** (b) — class B uses the first two octets for the network.
**5.** (c) — every node in a star hangs off the central switch.
**6.** (b) — 48 bits, written as 12 hexadecimal digits.
**7.** (c) — that is the definition of crosstalk.
:::

**Group B — Short answer (5 marks each)**

1. Draw the block diagram of a communication system and explain the function of
   each block. <span class="marks">[5]</span>
2. Differentiate between guided and unguided transmission media on any five
   points, giving two examples of each. <span class="marks">[5]</span>
3. Define topology. Draw bus, star and ring topologies and state one advantage
   and one disadvantage of each. <span class="marks">[5]</span>
4. Explain any five transmission impairments and state how each can be reduced. <span class="marks">[5]</span>
5. A host has IP address `172.16.45.9` with mask `255.255.0.0`. State its class,
   network address, broadcast address and the number of usable hosts on that
   network. Also distinguish an IP address from a MAC address. <span class="marks">[5]</span>
6. What is meant by client–server and peer-to-peer architecture? Compare them on
   any four points. <span class="marks">[5]</span>

::: note Answers to Group B
**5.** The first octet 172 lies in 128–191, so it is **class B** (and a private
address, since it is inside 172.16.0.0/12). With mask 255.255.0.0 the first two
octets are the network, so the **network address is 172.16.0.0** and the
**broadcast address is 172.16.255.255**. There are 16 host bits, so
$2^{16}-2 = 65{,}534$ usable hosts. An IP address is a 32-bit *logical* address
assigned by software, used by routers between networks, and it changes when the
host joins another network; a MAC address is a 48-bit *physical* address burned
into the NIC, used by switches inside one LAN, and it never changes.
:::

**Group C — Long answer (8 marks each)**

1. (a) Explain the OSI reference model with a neat diagram, naming each layer and
   stating its main function and one protocol. <span class="marks">[5]</span>
   (b) Compare the OSI model with the TCP/IP model on any three points. <span class="marks">[3]</span>

2. (a) What is a network topology? Explain bus, star, ring and mesh topologies
   with diagrams, listing the advantages and disadvantages of each. <span class="marks">[6]</span>
   (b) A full mesh network is to be built for 10 computers. Calculate the number
   of cables and the number of ports required per computer, and say why a star is
   preferred in a school laboratory. <span class="marks">[2]</span>

::: note Answer outline to Group C question 2(b)
Number of cables $= n(n-1)/2 = (10\times 9)/2 = \textbf{45}$, and each computer
needs $n-1 = \textbf{9}$ ports. A star needs only 10 cables and one switch, is far
cheaper, lets a faulty cable be replaced without touching other machines, and can
be extended simply by adding a port — so it is the practical choice for a lab,
while mesh is reserved for backbone links where redundancy justifies the cost.
:::
