---
subject: Computer Fundamentals and Applications
grade: BCA Semester 1
unit: 5
title: Data Communication and Computer Network
hours: 10
area: BCA 101 · Computer Fundamentals and Applications · Unit 5
---

A computer on its own is useful; computers joined together are transformative. **Data communication** is the exchange of data between devices over a medium; a **computer network** is a set of such devices that can share data and resources. This unit covers the signals, media, topologies, devices, layered models and addressing that every networking course builds on.

::: key What this unit gives you
- Components, signals, bandwidth, transmission modes; Shannon's formula.
- Guided and unguided media; multiplexing; switching.
- Network types and topologies; network devices.
- OSI and TCP/IP models; IP addressing and subnetting with worked examples.
:::

## 5.1 Data communication fundamentals

**Components of a communication system:** *sender* (source), *receiver* (destination), *message*, *transmission medium* and *protocol* (the agreed rules).

**Signals.** An **analog** signal varies continuously (sound); a **digital** signal has discrete levels (0 and 1). A **modem** (modulator–demodulator) converts digital data to analog form for a telephone line or radio link and back.

**Bandwidth** has two senses: in hertz, the range of frequencies a channel carries; in bits per second (bps), its capacity. **Throughput** is the data rate actually achieved; **latency** is the delay; **jitter** is variation in delay. Noise, attenuation (loss of strength with distance) and distortion degrade signals.

**Shannon's capacity** for a noisy channel: **C = B × log₂(1 + S/N)**, where B is bandwidth in Hz and S/N the signal-to-noise ratio (a plain ratio, not dB).

::: example Worked example: Shannon capacity and transfer time
A telephone line has B = 3000 Hz and S/N = 1000 (30 dB). C = 3000 × log₂(1001) = 3000 × 9.967 ≈ **29,900 bps**, about 29.9 kbps; no coding can beat this.

Time to send a 1 MB file (8 × 10⁶ bits) on an 8 Mbps link: 8 × 10⁶ / 8 × 10⁶ = **1 s** (ignoring protocol overhead and propagation delay).
:::

**Transmission modes**

| Mode | Direction | Example |
|---|---|---|
| Simplex | one way only | keyboard → computer, radio broadcast |
| Half duplex | both ways, one at a time | walkie-talkie |
| Full duplex | both ways simultaneously | telephone, modern Ethernet |

**Serial vs parallel:** serial sends bits one after another on one line (USB, Ethernet; cheap over distance); parallel sends several bits at once on many lines (old printer port; skew limits distance). **Asynchronous** transmission frames each byte with start and stop bits; **synchronous** sends blocks timed by a shared clock.

**Error detection** adds redundancy: a **parity bit**, a **checksum**, or a **CRC (cyclic redundancy check)**, used in Ethernet. Detected errors are corrected by retransmission (ARQ) or by error-correcting codes.

```photogrid label="5.1" cols="2" ratio="1.29" caption="Modem and capacity. (a) The inside of an ADSL modem-router with its chips numbered 1 to 18 (the labels come from the original photograph). It contains the modem that turns digital data into signals for the telephone line. (b) Shannon's formula applied to real channels: bandwidth and signal-to-noise ratio, not the cable alone, set the speed limit."
@ photo id="bca101/adslint" cap="ADSL modem-router board: modem chip, processor, memory and Ethernet ports on one card"
fit 1.29
focus 0.5 0.5
@ svg cap="Shannon limit C = B log2(1 + S/N) on a log scale"
import math
def cap(B, db): return B * math.log2(1 + 10 ** (db / 10))
rows = [("Phone line, 3 kHz, 30 dB", 3000, 30), ("ADSL2+, 2.2 MHz, 30 dB", 2.2e6, 30), ("4G cell, 20 MHz, 20 dB", 20e6, 20),
        ("Wi-Fi, 20 MHz, 30 dB", 20e6, 30), ("5G cell, 100 MHz, 20 dB", 100e6, 20), ("Wi-Fi, 80 MHz, 30 dB", 80e6, 30)]
vals = [cap(b, d) for _, b, d in rows]
assert round(vals[0]) == 29902 and round(vals[3] / 1e6, 1) == 199.3 and round(vals[4] / 1e6, 1) == 665.8
def fmt(c): return f"{c/1e6:.1f} Mbps" if c >= 1e6 else f"{c/1e3:.1f} kbps"
f = Fig(400, 348)
f.text(10, 16, "Upper bound on error-free speed (computed)", size=11, color=NAVY, bold=True, anchor="start")
for i, ((n, b, d), c) in enumerate(zip(rows, vals)):
    y = 34 + i * 50
    f.text(10, y + 6, n, size=10.5, color=SLATE, bold=True, anchor="start")
    w = (math.log10(c) - 3.5) / (9 - 3.5) * 270
    f.box(10, y + 14, max(w, 6), 20, "", fill=MINT if i % 2 == 0 else BLUE, stroke=TEAL if i % 2 == 0 else NAVY)
    f.text(10 + max(w, 6) + 6, y + 25, fmt(c), size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
f.text(200, 340, "Longer bars = more bandwidth or cleaner signal. 30 dB means S/N = 1000.", size=9.5, color=SLATE)
```

```svgfig label="5.1" caption="Which error-detecting code catches what? Every 1-, 2- and 3-bit error pattern was applied to an 8-byte message (64 bits: 64, 2,016 and 41,664 patterns) and the share detected by each method was counted."
import itertools, zlib
msg = b"NEBIANS!"
bits = int.from_bytes(msg, "big")
def par(x): return bin(x).count("1") & 1
def ichk(data):
    s = sum(int.from_bytes(data[i:i+2], "big") for i in range(0, len(data), 2))
    while s >> 16: s = (s & 0xFFFF) + (s >> 16)
    return (~s) & 0xFFFF
def tob(x): return x.to_bytes(8, "big")
p0, c0, r0 = par(bits), ichk(msg), zlib.crc32(msg)
res = {}
for k in (1, 2, 3):
    tot = 0; dp = dc = dr = 0
    for pos in itertools.combinations(range(64), k):
        m = bits
        for q in pos: m ^= 1 << q
        b = tob(m); tot += 1
        dp += par(m) != p0; dc += ichk(b) != c0; dr += zlib.crc32(b) != r0
    res[k] = (tot, dp / tot * 100, dc / tot * 100, dr / tot * 100)
assert [res[k][0] for k in (1, 2, 3)] == [64, 2016, 41664]
assert res[1][1:] == (100.0, 100.0, 100.0)
assert res[2][1] == 0.0 and 0 < res[2][2] < 100 and res[2][3] == 100.0
assert res[3][1] == 100.0 and res[3][3] == 100.0
f = Fig(760, 292)
f.text(380, 18, "Share of corrupted messages detected (%)   message = 'NEBIANS!' = 8 bytes", size=11.5, color=NAVY, bold=True)
cols = [("Parity bit", RED, ROSE), ("16-bit checksum", AMBER, SAND), ("CRC-32 (Ethernet)", TEAL, MINT)]
for gi, k in enumerate((1, 2, 3)):
    gx = 40 + gi * 240
    f.text(gx + 90, 262, f"{k}-bit error ({res[k][0]:,} patterns)", size=10.5, color=SLATE, bold=True)
    for bi, (nm, st, fl) in enumerate(cols):
        v = res[k][bi + 1]; h = max(v * 1.7, 2)
        x = gx + bi * 60
        f.box(x, 232 - h, 48, h, "", fill=fl, stroke=st)
        f.text(x + 24, 232 - h - 8, f"{v:.1f}" if v not in (0.0, 100.0) else f"{v:.0f}", size=10.5, color=st, bold=True)
for bi, (nm, st, fl) in enumerate(cols):
    f.box(190 + bi * 170, 274, 12, 12, "", fill=fl, stroke=st)
    f.text(208 + bi * 170, 281, nm, size=10, color=SLATE, anchor="start", vmid=True)
f.text(380, 38, "A single parity bit misses every 2-bit error; CRC-32 caught all three kinds.", size=10.5, color=SLATE)
```

## 5.2 Transmission media

| Medium | Type | Speed / range (typical) | Notes |
|---|---|---|---|
| Twisted pair (UTP/STP) | guided, copper | Cat5e/Cat6: 1 Gbps to 100 m | cheap; LAN cabling, RJ-45 plug |
| Coaxial cable | guided, copper | up to ~10 Mbps (old Ethernet), more on cable TV | better shielding than twisted pair |
| Optical fibre | guided, glass | Gbps to Tbps over kilometres | immune to electrical noise; single-mode for long haul, multi-mode for short |
| Radio / Wi-Fi | unguided | 2.4, 5, 6 GHz bands | shared, interference, security needs |
| Microwave | unguided | line of sight, ~50 km between towers | tower links across hills |
| Satellite | unguided | worldwide; high latency (GEO ~250 ms one way) | remote villages, VSAT |
| Infrared, Bluetooth | unguided | short range | remotes, peripherals |

```photogrid label="5.2" cols="4" ratio="1.15" caption="Real transmission media: (a) coaxial cable with its braided shield, (b) Cat-5e UTP cable with RJ-45 plugs, (c) a fibre-optic cable, (d) a single glass fibre stripped of its coating."
@ photo id="bca101/coax" cap="Coaxial: copper core, insulation, braid shield"
@ photo id="bca101/rj45" cap="UTP Cat-5e with RJ-45 connectors (4 twisted pairs)"
@ photo id="bca101/fibre-cable" cap="Fibre-optic cable: glass strands in a protective jacket"
@ photo id="bca101/fibre-strand" cap="Bare glass fibre: thinner than a hair, carries light"
```

**Multiplexing** shares one link among many signals: **FDM** (different frequencies), **TDM** (different time slots), **WDM** (different light colours on fibre). **Switching** moves data through a network: **circuit switching** reserves a dedicated path for the whole call (telephone); **packet switching** cuts data into packets that are routed independently and reassembled (the Internet).

```photogrid label="5.3" cols="4" ratio="1.1" caption="Real cabling work. (a) A multimode SFP transceiver: the plug-in module that turns electrical signals into light for a fibre link. (b) A fusion splicer, which melts two glass fibres together so light passes with almost no loss. (c) Two cable testers: a lamp lights for each of the eight wires of an RJ-45 cable that is wired correctly. (d) A technician's kit with a crimping tool, a punch-down tool and a tester."
@ photo id="bca101/sfp" cap="SFP module: converts bits to light and back"
fit 1.1
focus 0.5 0.5
@ photo id="bca101/fusion" cap="Splicer: aligns and fuses two glass fibres"
fit 1.1
focus 0.5 0.45
@ photo id="bca101/cabletester" cap="Cable tester: one lamp per wire"
fit 1.1
focus 0.5 0.4
@ photo id="bca101/crimptools" cap="Crimp tool, punch-down tool, tester"
fit 1.1
focus 0.5 0.5
```

## 5.2.1 Eight points to weigh when choosing a medium

1. **Speed (bandwidth).** The medium must carry the data rate you need today and in five years. Cat-6 twisted pair is enough for a 1 Gbps college lab, but a bank's backbone between floors needs fibre. Always check the cable category printed on the jacket.
2. **Distance.** Twisted pair works only to 100 m between switch and computer, because the signal fades. Fibre can run tens of kilometres before it needs a repeater. Between two hill-top towers in Nepal, microwave can cover about 50 km in line of sight.
3. **Cost.** UTP cable and RJ-45 plugs are the cheapest option and any technician can fit them with a crimp tool. Fibre cable itself is not costly now, but splicing and optical modules are. Satellite links cost the most per megabit.
4. **Noise and interference.** Copper picks up electrical noise from motors, lifts and power lines. Fibre carries light, so it is not affected by such noise and is the safe choice in a factory. Shielded cable (STP) is the middle way.
5. **Security.** Light inside a fibre or current inside a cable is hard to tap without cutting it. Radio waves can be received by anyone in range, so Wi-Fi must be encrypted with WPA2 or WPA3. Banks keep core links on cable for this reason.
6. **Installation and terrain.** Cables need trenches or conduits, which is hard on a steep Himalayan slope. Radio, microwave and satellite reach such places without digging. Cutting of cables by road-widening work is a common cause of outages in Nepal.
7. **Mobility.** Only wireless media let a phone or laptop move around. A classroom with Wi-Fi allows students to connect anywhere, while a wired lab does not. Use cable for fixed servers and wireless for people.
8. **Reliability and maintenance.** Fibre and good copper last for decades with little care. Wireless links suffer from rain, fog and crowding on the same frequency. Network engineers therefore keep a backup path for important links.

## 5.3 Network types and topologies

**By scale**

| Type | Area | Example |
|---|---|---|
| PAN | a person (a few metres) | Bluetooth earphones |
| LAN | a room, building or campus | college computer lab |
| MAN | a city | cable TV or ISP metro network |
| WAN | country or world | the Internet, bank branch network |

Other kinds: **client–server** (dedicated servers serve clients) and **peer-to-peer** (each machine is both); **intranet** (private network using internet technology), **extranet** (intranet shared with partners), **VPN** (private tunnel over the public Internet).

**Topology** is the layout of the network.

| Topology | Layout | Advantage | Disadvantage |
|---|---|---|---|
| Bus | all nodes on one backbone cable | little cable, cheap | backbone break kills the network; collisions |
| Ring | each node connected to two neighbours in a loop | orderly access | one break stops a simple ring |
| Star | every node connected to a central hub/switch | easy to add and troubleshoot; a bad cable affects one node | central device is a single point of failure |
| Mesh | nodes interconnected; full mesh has n(n−1)/2 links | very reliable | costly cabling |
| Tree | star networks joined in a hierarchy | scalable | root failure splits tree |
| Hybrid | a mix | flexible | complex |

A **full mesh** of 6 nodes needs 6 × 5 / 2 = **15** links, and each node needs 5 ports.

```svgfig label="5.2" caption="The five network topologies with the main merit and demerit of each."
import math
f = Fig(760, 330)
names = ["BUS", "STAR", "RING", "MESH", "HYBRID (tree)"]
facts = [("+ cheap, little cable", "− backbone fault stops all"), ("+ one fault, one node", "− hub/switch is the risk"),
         ("+ orderly, no collisions", "− one break can stop all"), ("+ most reliable, many paths", "− n(n−1)/2 links: costly"),
         ("+ scalable, mixes types", "− complex, costly")]
for i, n in enumerate(names):
    x0 = 8 + i * 150; cx = x0 + 70
    f.box(x0, 8, 140, 26, n, fill=NAVY, stroke=NAVY, color="#ffffff", size=11, bold=True)
    f.box(x0, 40, 140, 190, "", fill=SOFT, stroke="#cbd5e1")
    f.text(cx, 266, facts[i][0], size=9.5, color=TEAL, bold=True)
    f.text(cx, 284, facts[i][1], size=9.5, color=RED, bold=True)
    if i == 0:
        f.line(x0 + 12, 135, x0 + 128, 135, color=SLATE, sw=3)
        for k, nx in enumerate((x0 + 28, x0 + 56, x0 + 84, x0 + 112)):
            ny = 85 if k % 2 == 0 else 185
            f.line(nx, 135, nx, ny + (10 if k % 2 == 0 else -10), color=SLATE)
            f.circle(nx, ny, 10, fill=BLUE, stroke=NAVY)
        f.box(x0 + 6, 125, 8, 20, "", fill=AMBER, stroke=AMBER, r=1); f.box(x0 + 126, 125, 8, 20, "", fill=AMBER, stroke=AMBER, r=1)
        f.text(cx, 222, "terminator at each end", size=9, color=AMBER, bold=True)
    elif i == 1:
        for a in range(4):
            ang = math.radians(90 * a + 45); nx, ny = cx + 52 * math.cos(ang), 135 + 52 * math.sin(ang)
            f.line(cx, 135, nx, ny, color=SLATE); f.circle(nx, ny, 10, fill=BLUE, stroke=NAVY)
        f.box(cx - 17, 123, 34, 24, "HUB", fill=SAND, stroke=AMBER, size=9, bold=True)
    elif i == 2:
        pts = [(cx + 50 * math.cos(math.radians(-90 + 72 * k)), 135 + 50 * math.sin(math.radians(-90 + 72 * k))) for k in range(5)]
        for k in range(5):
            a, b = pts[k], pts[(k + 1) % 5]
            f.line(a[0], a[1], b[0], b[1], color=SLATE, sw=1.8)
        for p in pts: f.circle(p[0], p[1], 10, fill=BLUE, stroke=NAVY)
        f.text(cx, 135, "token\n→", size=9, color=AMBER, bold=True)
    elif i == 3:
        pts = [(cx + 52 * math.cos(math.radians(-90 + 72 * k)), 135 + 52 * math.sin(math.radians(-90 + 72 * k))) for k in range(5)]
        for a in range(5):
            for b in range(a + 1, 5): f.line(pts[a][0], pts[a][1], pts[b][0], pts[b][1], color=SLATE, sw=1.2)
        for p in pts: f.circle(p[0], p[1], 10, fill=BLUE, stroke=NAVY)
    else:
        f.line(cx - 30, 100, cx + 30, 100, color=SLATE, sw=2.5)
        f.box(cx - 52, 90, 34, 20, "SW", fill=SAND, stroke=AMBER, size=9, bold=True); f.box(cx + 18, 90, 34, 20, "SW", fill=SAND, stroke=AMBER, size=9, bold=True)
        for sx, dx in ((cx - 38, -1), (cx + 38, 1)):
            for k in (-1, 0, 1):
                nx, ny = sx + 22 * k, 175
                f.line(sx, 110, nx, ny, color=SLATE); f.circle(nx, ny, 9, fill=BLUE, stroke=NAVY)
f.text(380, 316, "Circle = computer / node · shaded box = hub or switch", size=9.5, color=SLATE, italic=True)
```

```svgfig label="5.3" caption="What a topology costs and how it fails, for 8 computers. Links and failures were computed on a graph of each layout: the worst single cable cut, and the worst failure of one hub or switch, measured as the share of the 28 computer pairs that can no longer talk."
import itertools
n = 8; C = list(range(n))
def pairs_lost(edges, dead=None):
    adj = {}
    for a, b in edges:
        if dead in (a, b): continue
        adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    comp = {}; k = 0
    for s in C:
        if s in comp: continue
        st = [s]; comp[s] = k
        while st:
            u = st.pop()
            for v in adj.get(u, ()):
                if v not in comp: comp[v] = k; st.append(v)
        k += 1
    return sum(1 for a, b in itertools.combinations(C, 2) if comp[a] != comp[b])
topo = {"Bus": [(i, i + 1) for i in range(n - 1)], "Star": [("H", i) for i in C], "Ring": [(i, (i + 1) % n) for i in C],
        "Mesh": list(itertools.combinations(C, 2)), "Tree": [("S0", "S1"), ("S0", "S2")] + [("S1", i) for i in range(4)] + [("S2", i) for i in range(4, 8)]}
res = {}
for nm, E in topo.items():
    cut = max(pairs_lost([e for e in E if e != x]) for x in E)
    devs = {v for e in E for v in e if isinstance(v, str)}
    dev = max([pairs_lost(E, d) for d in devs] or [0])
    res[nm] = (len(E), cut, dev)
assert res == {"Bus": (7, 16, 0), "Star": (8, 7, 28), "Ring": (8, 0, 0), "Mesh": (28, 0, 0), "Tree": (10, 16, 22)}
f = Fig(760, 270)
f.text(380, 16, "Eight computers: cost and fault tolerance of each topology", size=11.5, color=NAVY, bold=True)
f.text(80, 40, "Links needed", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(300, 40, "Worst cable cut", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(530, 40, "Worst hub or switch failure", size=10.5, color=RED, bold=True, anchor="start")
for i, (nm, (l, c, d)) in enumerate(res.items()):
    y = 54 + i * 40
    f.text(10, y + 14, nm, size=11, color=NAVY, bold=True, anchor="start", vmid=True)
    f.box(80, y, l / 28 * 190 + 2, 26, "", fill=BLUE, stroke=NAVY); f.text(80 + l / 28 * 190 + 8, y + 13, str(l), size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
    f.box(300, y, c / 28 * 190 + 2, 26, "", fill=SAND, stroke=AMBER); f.text(300 + c / 28 * 190 + 8, y + 13, f"{c/28*100:.0f}%", size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
    f.box(530, y, d / 28 * 190 + 2, 26, "", fill=ROSE, stroke=RED); f.text(530 + d / 28 * 190 + 8, y + 13, "no hub" if nm in ("Bus", "Ring", "Mesh") else f"{d/28*100:.0f}%", size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
f.text(380, 262, "Mesh never splits but needs n(n-1)/2 = 28 links; a star is cheap but its hub is the weak point.", size=10.5, color=SLATE)
```


## 5.4 Network devices

| Device | Layer | Function |
|---|---|---|
| NIC | 1–2 | the card/chip connecting a host to the network; has a MAC address |
| Repeater | 1 | regenerates a weak signal |
| Hub | 1 | repeats incoming bits to *all* ports |
| Switch | 2 | forwards frames only to the port of the destination MAC (learns addresses) |
| Bridge | 2 | joins two LAN segments |
| Router | 3 | forwards packets between networks using IP addresses; chooses routes |
| Gateway | 4–7 | translates between different protocol families |
| Modem | 1 | digital ↔ analog conversion |
| Access point | 1–2 | connects wireless clients to a wired network |
| Firewall | 3–7 | filters traffic by rules |

```photogrid label="5.4" cols="3" ratio="1.25" caption="Common network devices: (a) a five-port Gigabit switch, (b) the inside of a wireless router showing the board and antennas, (c) a 3Com Ethernet network interface card (NIC) with its RJ-45 port."
@ photo id="bca101/switch" cap="Switch: forwards frames by MAC address (Layer 2)"
@ photo id="bca101/router" cap="Router: forwards packets by IP address (Layer 3)"
@ photo id="bca101/nic" cap="NIC: gives the host a MAC address and a cable port"
```

```photogrid label="5.5" cols="2" ratio="1.12" caption="Shared cable or learning switch? (a) An old 8-port Ethernet hub: it repeats every frame to every port. (b) Seven frames sent through a hub and through a learning switch, counted by a short program: the switch floods only while it does not yet know where a computer is."
@ photo id="bca101/nethub" cap="8-port hub: Layer 1, copies each bit stream to all other ports"
fit 1.9
focus 0.45 0.5
call 0.5 0.9 0.55 0.5 "8 RJ-45 ports"
@ svg cap="Frame copies delivered: hub vs switch"
ports = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6}
seq = [("A", "B"), ("B", "A"), ("C", "A"), ("A", "C"), ("D", "E"), ("E", "D"), ("F", "A")]
table = {}; sw = []; hub = []
for s, d in seq:
    hub.append(5)
    table[s] = ports[s]
    sw.append(1 if d in table else 5)
assert sum(hub) == 35 and sum(sw) == 15 and sw == [5, 1, 1, 1, 5, 1, 1]
f = Fig(400, 330)
f.text(200, 16, "6 computers A to F; each row is one frame", size=11, color=NAVY, bold=True)
f.text(26, 40, "Frame", size=10, color=SLATE, bold=True, anchor="start")
f.text(120, 40, "Hub copies", size=10, color=RED, bold=True, anchor="start")
f.text(262, 40, "Switch copies", size=10, color=TEAL, bold=True, anchor="start")
for i, ((s, d), h, w) in enumerate(zip(seq, hub, sw)):
    y = 52 + i * 31
    f.text(26, y + 12, f"{s} to {d}", size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
    for j in range(h): f.box(120 + j * 15, y + 3, 12, 18, "", fill=ROSE, stroke=RED, r=2)
    for j in range(w): f.box(262 + j * 15, y + 3, 12, 18, "", fill=MINT, stroke=TEAL, r=2)
f.text(26, 290, "Total", size=11, color=NAVY, bold=True, anchor="start")
f.text(120, 290, f"{sum(hub)} copies", size=11, color=RED, bold=True, anchor="start")
f.text(262, 290, f"{sum(sw)} copies", size=11, color=TEAL, bold=True, anchor="start")
f.text(200, 316, "Flooded rows (5 squares): destination not yet learned.", size=9.5, color=SLATE)
```

```photogrid label="5.6" cols="2" ratio="1.2" caption="Structured cabling in practice. (a) The inside of a small network rack: a patch panel, patch cords and a switch. (b) The T568B order in which the eight wires enter an RJ-45 plug, as listed by the standard; the technician's crimp tool and tester are shown in Plate 5.3."
@ photo id="bca101/rack" cap="Rack: patch panel on top, switch below, short patch cords between them"
fit 1.2
focus 0.5 0.5
@ svg cap="T568B wire order (pin 1 on the left)"
cols = [("W/O", "#f59e0b", True), ("Or", "#f59e0b", False), ("W/G", "#16a34a", True), ("Bl", "#2563eb", False),
        ("W/Bl", "#2563eb", True), ("Gr", "#16a34a", False), ("W/Br", "#92400e", True), ("Br", "#92400e", False)]
assert len(cols) == 8 and [c[0] for c in cols][:3] == ["W/O", "Or", "W/G"]
f = Fig(400, 333)
f.text(200, 18, "RJ-45 plug, contacts facing you", size=11, color=NAVY, bold=True)
for i, (n, c, striped) in enumerate(cols):
    x = 20 + i * 45
    f.box(x, 40, 36, 150, "", fill="#ffffff" if striped else c, stroke=SLATE, r=3)
    if striped:
        for k in range(5): f.box(x + 4, 46 + k * 28, 28, 14, "", fill=c, stroke=c, r=2)
    f.text(x + 18, 206, str(i + 1), size=11, color=NAVY, bold=True)
    f.text(x + 18, 224, n, size=10.5, color=SLATE, bold=True)
f.box(20, 244, 90, 24, "TX pair", fill=MINT, stroke=TEAL, size=10.5)
f.text(124, 256, "pins 1, 2: send (10/100 Mbps)", size=10.5, color=SLATE, anchor="start", vmid=True)
f.box(20, 276, 90, 24, "RX pair", fill=BLUE, stroke=NAVY, size=10.5)
f.text(124, 288, "pins 3, 6: receive", size=10.5, color=SLATE, anchor="start", vmid=True)
f.text(200, 320, "Gigabit Ethernet uses all four pairs.", size=10.5, color=SLATE)
```

## 5.5 Layered models: OSI and TCP/IP

Layering splits a complicated job into stages; each layer uses the services of the layer below and hides its details from the layer above.

| # | OSI layer | Job | Data unit | Examples |
|---|---|---|---|---|
| 7 | Application | services to user programs | data | HTTP, SMTP, FTP, DNS |
| 6 | Presentation | format, encryption, compression | data | TLS, JPEG, ASCII/Unicode |
| 5 | Session | open, manage, close dialogues | data | sockets, RPC |
| 4 | Transport | end-to-end delivery, ports, reliability | segment | TCP, UDP |
| 3 | Network | logical addressing, routing | packet | IP, ICMP |
| 2 | Data link | node-to-node delivery, MAC addressing, error detection | frame | Ethernet, Wi-Fi, PPP |
| 1 | Physical | bits on the medium | bits | cables, signals |

Memory aid, top to bottom: **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing.

The **TCP/IP model** has four layers: **Application** (OSI 5–7), **Transport** (TCP/UDP), **Internet** (IP), **Network access** (OSI 1–2). It is the model the Internet actually uses; OSI is the teaching reference.

- **TCP**: connection-oriented, reliable, ordered (three-way handshake: SYN, SYN-ACK, ACK). Used for web, email, file transfer.
- **UDP**: connectionless, no guarantee, low delay. Used for DNS queries, video calls, games.

**Common application protocols:** HTTP 80 / HTTPS 443, FTP 21, SSH 22, SMTP 25, DNS 53, POP3 110, IMAP 143.

```svgfig label="5.4" caption="OSI seven-layer model compared with the four-layer TCP/IP model, with protocols and data units."
f = Fig(760, 350)
osi = [("7  Application", NAVY), ("6  Presentation", NAVY), ("5  Session", NAVY), ("4  Transport", TEAL), ("3  Network", AMBER), ("2  Data link", RED), ("1  Physical", RED)]
f.text(145, 18, "OSI model (7 layers)", size=11.5, color=NAVY, bold=True)
f.text(425, 18, "TCP/IP model (4 layers)", size=11.5, color=NAVY, bold=True)
f.text(655, 18, "Protocols · data unit", size=11.5, color=NAVY, bold=True)
for i, (n, c) in enumerate(osi):
    f.box(40, 30 + i * 44, 210, 40, n, fill="#ffffff", stroke=c, color=c, size=11.5, bold=True)
tc = [("Application", 30, 128, NAVY, BLUE, "HTTP · HTTPS · DNS · SMTP · FTP\ndata / message"),
      ("Transport", 162, 40, TEAL, MINT, "TCP · UDP\nsegment / datagram"),
      ("Internet", 206, 40, AMBER, SAND, "IP · ICMP · ARP\npacket"),
      ("Network access", 250, 84, RED, ROSE, "Ethernet · Wi-Fi · PPP\nframe  →  bits")]
for n, y, h, c, bg, pr in tc:
    f.box(330, y, 190, h, n, fill=bg, stroke=c, color=c, size=12, bold=True)
    f.text(655, y + h / 2, pr, size=10, color=SLATE, bold=True, vmid=True)
    f.line(522, y + h / 2, 560, y + h / 2, color="#cbd5e1", dash=True)
for y1, y2 in ((30, 158), (162, 202), (206, 246), (250, 334)):
    f.line(252, (y1 + y2) / 2, 328, (y1 + y2) / 2, color="#94a3b8", sw=1.2, dash=True)
```

## 5.6 Addressing: MAC and IP

- **MAC address**: 48-bit hardware address burned into the NIC, written like `3C:52:82:1A:9F:07`; works inside one LAN.
- **IPv4 address**: 32 bits written as four decimal bytes (**dotted decimal**), e.g. `192.168.10.25`; gives about 4.3 billion addresses. **IPv6** has 128 bits (`2001:db8::1`) because IPv4 ran out.

**Classful ranges (historical):** A 1–126 (mask /8), B 128–191 (/16), C 192–223 (/24), D 224–239 multicast, E 240–255 reserved. Modern networks use **CIDR**, writing the prefix length: `192.168.10.0/26`. **Private ranges** (not routed on the Internet): 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. 127.0.0.1 is loopback (this machine).

A **subnet mask** marks which bits are the **network** part (1s) and which are the **host** part (0s). In a network with *h* host bits, there are 2ʰ addresses, of which the first (network address) and last (broadcast) are not usable, so **usable hosts = 2ʰ − 2**.

::: example Worked example: subnetting 192.168.10.0/24 into four equal subnets
Four subnets need 2 extra bits, so the prefix becomes /26 and the mask is 255.255.255.192 (the last byte 11000000 = 192). Host bits h = 6, so each subnet has 2⁶ = 64 addresses and 62 usable hosts.

| Subnet | Network address | Usable range | Broadcast |
|---|---|---|---|
| 1 | 192.168.10.0 | .1 – .62 | 192.168.10.63 |
| 2 | 192.168.10.64 | .65 – .126 | 192.168.10.127 |
| 3 | 192.168.10.128 | .129 – .190 | 192.168.10.191 |
| 4 | 192.168.10.192 | .193 – .254 | 192.168.10.255 |
:::

::: example Worked example: which network does a host belong to?
Host 172.16.37.200 with mask 255.255.255.0 (/24). AND the address with the mask byte by byte: 172.16.37.(200 AND 0) = **172.16.37.0**. A host 172.16.38.5 with the same mask is on 172.16.38.0, a different network, so they need a router to talk.
:::

```svgfig label="5.5" caption="One real web request, built byte by byte. The IP header checksum and the TCP checksum were computed and verified in code, and the Ethernet check sequence is a real CRC-32."
import struct, zlib
def csum(b):
    if len(b) % 2: b += b"\x00"
    s = sum(struct.unpack(">%dH" % (len(b) // 2), b))
    while s >> 16: s = (s & 0xFFFF) + (s >> 16)
    return (~s) & 0xFFFF
payload = b"GET / HTTP/1.1\r\nHost: tu.edu.np\r\n\r\n"
src, dst = bytes([192, 168, 10, 25]), bytes([203, 0, 113, 10])
tcp0 = struct.pack(">HHIIHHHH", 51514, 80, 1000, 5000, (5 << 12) | 0x18, 64240, 0, 0)
pseudo = src + dst + struct.pack(">BBH", 0, 6, 20 + len(payload))
tcp = tcp0[:16] + struct.pack(">H", csum(pseudo + tcp0 + payload)) + tcp0[18:]
ip0 = struct.pack(">BBHHHBBH", 0x45, 0, 20 + 20 + len(payload), 0x1C46, 0x4000, 64, 6, 0) + src + dst
ip = ip0[:10] + struct.pack(">H", csum(ip0)) + ip0[12:]
eth = bytes.fromhex("3c528 21a9f07".replace(" ", "")) + bytes.fromhex("001a2b3c4d5e") + b"\x08\x00"
body = eth + ip + tcp + payload
fcs = struct.pack("<I", zlib.crc32(body))
assert csum(ip) == 0 and csum(pseudo + tcp + payload) == 0
assert len(eth) == 14 and len(ip) == 20 and len(tcp) == 20 and len(payload) == 35 and len(body) + 4 == 93 and len(ip0) == 20
f = Fig(760, 300)
parts = [("Ethernet header", len(eth), AMBER, SAND), ("IPv4 header", 20, TEAL, MINT), ("TCP header", 20, NAVY, BLUE), ("HTTP request (data)", len(payload), SLATE, SOFT), ("FCS", 4, RED, ROSE)]
x = 10; tot = len(body) + 4
f.text(380, 16, f"Frame on the wire = {tot} bytes: only {len(payload)} bytes are the user's data", size=11.5, color=NAVY, bold=True)
for nm, n, st, fl in parts:
    w = n / tot * 740
    f.box(x, 30, w - 2, 40, f"{n} B" if n < 30 else f"{nm}\n{n} bytes", fill=fl, stroke=st, size=9.5 if n >= 30 else 9, bold=True)
    x += w
f.text(380, 88, f"Headers and trailer: {tot - len(payload)} of {tot} bytes = {100*(tot-len(payload))/tot:.0f}% overhead for this small request.", size=10.5, color=SLATE)
iph = ip.hex()
def grp(h): return " ".join(h[i:i+8] for i in range(0, len(h), 8))
f.box(10, 104, 238, 170, "", fill=SAND, stroke=AMBER)
f.text(20, 120, "Ethernet (Layer 2)", size=10.5, color=AMBER, bold=True, anchor="start")
for i, t in enumerate(["destination MAC  3c:52:82:1a:9f:07", "source MAC           00:1a:2b:3c:4d:5e", "type 0x0800 = IPv4", "FCS (CRC-32) " + fcs.hex(), "Switches read the MACs;", "routers drop this header and", "build a new one for each hop."]):
    f.text(20, 140 + i * 17, t, size=9.5, color=SLATE, anchor="start")
f.box(258, 104, 244, 170, "", fill=MINT, stroke=TEAL)
f.text(268, 120, "IPv4 header in hex (Layer 3)", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(268, 140, grp(iph[:16]) , size=9.5, color=SLATE, anchor="start")
f.text(268, 156, grp(iph[16:32]), size=9.5, color=SLATE, anchor="start")
f.text(268, 172, grp(iph[32:]), size=9.5, color=SLATE, anchor="start")
for i, t in enumerate(["45 = version 4, 5 words", "total length 75 bytes", "ttl 64, protocol 6 = TCP", f"checksum {ip[10]:02x}{ip[11]:02x}: sum of header = ffff", "src 192.168.10.25, dst 203.0.113.10"]):
    f.text(268, 196 + i * 15, t, size=9.5, color=SLATE, anchor="start")
f.box(512, 104, 238, 170, "", fill=BLUE, stroke=NAVY)
f.text(522, 120, "TCP header (Layer 4)", size=10.5, color=NAVY, bold=True, anchor="start")
for i, t in enumerate(["source port 51514 (random)", "destination port 80 (HTTP)", "sequence 1000, ack 5000", "flags PSH + ACK (0x18)", "window 64240 bytes", f"checksum {tcp[16]:02x}{tcp[17]:02x} (with pseudo-header)", "Ports pick the program;", "IP picks the computer."]):
    f.text(522, 140 + i * 17, t, size=9.5, color=SLATE, anchor="start")
f.text(380, 292, "Each layer wraps the data of the layer above: this is encapsulation.", size=10, color=SLATE, bold=True)
```

```svgfig label="5.6" caption="Variable-length subnetting of 192.168.10.0/24 for a college, computed with Python's ipaddress module: the largest department is placed first and every block starts on its own boundary."
import ipaddress
need = [("Computer lab", 100), ("Library", 50), ("Office", 25), ("Server room", 10)]
net = ipaddress.ip_network("192.168.10.0/24"); cur = int(net.network_address); out = []
for n, h in sorted(need, key=lambda t: -t[1]):
    p = 32
    while 2 ** (32 - p) - 2 < h: p -= 1
    sub = ipaddress.ip_network((cur, p)); out.append((n, h, sub)); cur += sub.num_addresses
assert [str(s) for _, _, s in out] == ["192.168.10.0/25", "192.168.10.128/26", "192.168.10.192/27", "192.168.10.224/28"]
assert [s.num_addresses - 2 for _, _, s in out] == [126, 62, 30, 14] and cur - int(net.network_address) == 240
f = Fig(760, 300)
hdr = ["Department", "Hosts", "Subnet", "Mask", "Usable range", "Broadcast", "Spare"]
xs = [10, 120, 175, 300, 425, 600, 705]
f.text(380, 16, "Four departments, one /24: sizes 126, 62, 30 and 14 usable hosts", size=11.5, color=NAVY, bold=True)
for x, h in zip(xs, hdr): f.text(x, 42, h, size=10, color=NAVY, bold=True, anchor="start")
cl = [(TEAL, MINT), (NAVY, BLUE), (AMBER, SAND), (RED, ROSE)]
for i, (n, h, s) in enumerate(out):
    y = 62 + i * 28; hs = list(s.hosts())
    f.box(4, y - 11, 752, 24, "", fill=cl[i][1], stroke=cl[i][0], r=4, sw=1)
    cells = [n, str(h), str(s), str(s.netmask), f"{hs[0]} - {hs[-1].packed[3]}", str(s.broadcast_address), str(len(hs) - h)]
    for x, c in zip(xs, cells): f.text(x, y, c, size=9.5, color=SLATE, bold=(x == 10), anchor="start", vmid=True)
f.text(10, 196, "Address map of the /24 (256 addresses, each pixel row = one block)", size=10.5, color=NAVY, bold=True, anchor="start")
x = 10
for i, (n, h, s) in enumerate(out):
    w = s.num_addresses / 256 * 740
    f.box(x, 208, w - 2, 34, f"{n}\n{s.num_addresses}" if w > 80 else str(s.num_addresses), fill=cl[i][1], stroke=cl[i][0], size=9, bold=True)
    x += w
f.box(x, 208, 16 / 256 * 740 - 2, 34, "free\n16", fill=SOFT, stroke=SLATE, size=9, dash=True)
f.text(380, 266, "Each block needs its own network address and broadcast address: usable = size - 2.", size=10, color=SLATE)
assert sum(len(list(s.hosts())) - h for _, h, s in out) == 47
f.text(380, 284, "Spare host addresses inside the four blocks: 47. The last 16 addresses stay free for growth.", size=10, color=SLATE)
```

Other services: **DHCP** hands out IP addresses automatically; **DNS** maps names such as `tu.edu.np` to IP addresses; **NAT** lets a whole home network share one public IP; **ARP** finds the MAC address that goes with an IP on the LAN; **ICMP** carries errors and powers `ping`.

## 5.7 Wireless and mobile networks

**Wi-Fi** (IEEE 802.11) gives LAN access by radio; **Bluetooth** gives short-range PAN links; **cellular** networks (2G, 3G, 4G LTE, 5G) cover wide areas through cells served by base stations; **NFC** works within a few centimetres (contactless payment). In Nepal, Wi-Fi in homes and colleges, FTTH broadband and 4G (and now 5G trials) are the everyday forms.

```photogrid label="5.7" cols="3" ratio="1.2" caption="Wireless links in daily use. (a) A microwave relay tower with dishes: each dish talks to the next tower in line of sight. (b) A Bluetooth headset, a personal-area (PAN) device. (c) A Wi-Fi 6 router with four antennas, the access point of most homes and colleges."
@ photo id="bca101/mwtower" cap="Microwave tower: point-to-point link between hill-tops"
fit 1.2
focus 0.5 0.5
@ photo id="bca101/btheadset" cap="Bluetooth: short-range PAN link (about 10 m)"
fit 1.2
focus 0.5 0.5
@ photo id="bca101/wifirouter" cap="Wi-Fi 6 router: LAN access by radio on 2.4 and 5 GHz"
fit 1.2
focus 0.5 0.5
```

```svgfig label="5.7" caption="Mobile generations compared by the time to download a 4 MB song (32 megabits) at a typical real-world speed. The times are computed from the speeds in the table."
import math
gens = [("2G (GPRS)", "1991", "digital voice, SMS, slow data", 0.04, "40 kbps"), ("3G (HSPA)", "2001", "mobile web, video calls", 2, "2 Mbps"),
        ("4G (LTE)", "2009", "all-IP, HD video, apps", 20, "20 Mbps"), ("5G (NR)", "2019", "very high speed, IoT, low delay", 200, "200 Mbps")]
t = [32 / g[3] for g in gens]
assert [round(x, 2) for x in t] == [800.0, 16.0, 1.6, 0.16]
def ft(s): return f"{s/60:.1f} min" if s >= 60 else f"{s:g} s"
f = Fig(760, 250)
f.text(380, 16, "Download time of a 4 MB song (log scale: each step is 10x faster)", size=11.5, color=NAVY, bold=True)
for i, (g, (n, yr, use, mb, sp), s) in enumerate(zip(gens, gens, t)):
    y = 36 + i * 50
    f.text(10, y + 12, n, size=11, color=NAVY, bold=True, anchor="start")
    f.text(10, y + 28, f"{yr}: {use}", size=9.5, color=SLATE, anchor="start")
    w = (math.log10(s) + 1.2) / 4.3 * 330 + 10
    f.box(300, y + 4, w, 28, "", fill=[ROSE, SAND, BLUE, MINT][i], stroke=[RED, AMBER, NAVY, TEAL][i])
    f.text(300 + w + 8, y + 18, f"{ft(s)} at {sp}", size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
f.text(380, 238, "1G (analog voice only, about 1979) could not carry data at all.", size=10, color=SLATE)
```

## 5.7.1 Eight uses of wireless and mobile networks in Nepal

1. **Mobile banking and wallets.** eSewa, Khalti, IME Pay and bank apps run over 4G and Wi-Fi. A shopkeeper in Pokhara can accept a Fonepay QR payment in a few seconds. Without mobile data, this would need a visit to the bank.
2. **Government services.** The Nagarik App and online forms of departments are used from phones. Citizens can check a licence or a tax record without travelling to Kathmandu. This saves time, travel cost and queues.
3. **Online classes and exams.** During the COVID lockdown, schools and campuses moved to Zoom and Google Meet over mobile data and home Wi-Fi. Tribhuvan University result and registration portals are still checked on phones today. Wireless access has become part of ordinary study.
4. **Remote and hill areas.** Microwave and VSAT links connect health posts and schools where no cable is possible. A telemedicine consultation can reach a village in Humla from a doctor in a city hospital. Such links need only a dish, a solar panel and a router.
5. **Emergency alerts.** SMS and cell broadcast warn people of floods, landslides and earthquakes. After the 2015 earthquake, phones were the main way for families to find each other. Battery-backed towers keep service going when the grid fails.
6. **Transport and ride sharing.** Pathao and InDrive use GPS and mobile data to match riders with drivers. Ticketing apps for buses and flights work the same way. Drivers also share live location with relatives.
7. **Agriculture and weather.** Farmers receive market prices and weather forecasts by SMS or app. Some dairy cooperatives record milk at collection centres on tablets that sync over mobile data. Better information helps farmers decide when to sell.
8. **Home and campus Wi-Fi.** FTTH broadband from ISPs ends in a Wi-Fi router that serves phones, laptops and smart TVs. College labs add access points so students can bring their own devices. Good placement of access points matters more than the number of antennas.

## 5.8 Advantages, limitations and uses of computer networks

### 5.8.1 Eight advantages of computer networks

1. **Resource sharing.** One printer, one scanner or one large disk can serve every computer in a lab. A college buys one good laser printer for the office instead of ten cheap ones. Software licences and internet connections are shared in the same way.
2. **Fast communication.** E-mail, chat and video calls deliver a message in seconds, not days. A teacher in Biratnagar can send a notice to 500 students at once. Offices stop depending on peons and paper circulars.
3. **Central data and easy backup.** When files are kept on a server, everyone sees the same latest copy. The administrator can back up one machine every night instead of asking each user. This is how Tribhuvan University exam sections keep result files safe.
4. **Lower cost.** Sharing hardware, software and links cuts the total cost of an organisation. A bank branch uses the head-office database through the network instead of keeping its own. Licences for network versions are usually cheaper than one copy per computer.
5. **Better reliability.** Important data can be copied to two or more machines, so a single failure does not stop work. If one server fails, a second takes over. Banks and hospitals use this to run 24 hours a day.
6. **Scalability.** New computers can be plugged in as an office grows, by adding a switch port or a Wi-Fi access point. The network does not have to be rebuilt. A school can start with ten computers and grow to a hundred.
7. **Centralised security and control.** The administrator can set user names, passwords and permissions in one place. A student can read the shared notes folder but cannot delete it. Firewalls and antivirus on the server protect every connected computer.
8. **Remote access and cooperation.** People can work together on the same document from different cities, and staff can reach office files from home through a VPN. Services such as ConnectIPS and Nagarik App exist only because networks join citizens to government and bank computers. This saves travel time and cost.

### 5.8.2 Eight limitations of computer networks

1. **High set-up cost.** Cables, switches, routers, servers and skilled engineers cost a lot at the start. A new college lab may spend more on the network than on the computers. Costs fall only when many users share the system.
2. **Security risks.** Many connected machines give an attacker many doors. A virus or ransomware that enters one computer can spread through the whole network. Strong passwords, updates and firewalls are needed all the time.
3. **Dependence on the server and links.** If the main server, switch or internet link fails, many users stop working together. Offices in Nepal feel this when the ISP link or the power fails. A backup link and UPS reduce the damage.
4. **Need for skilled staff.** A network needs an administrator to add users, fix faults and apply patches. Small organisations often cannot afford a full-time person. Poor management leads to slow and insecure systems.
5. **Congestion and slow speed.** When too many users share one link, everyone is slow. A lab where forty students download videos at once can choke a 20 Mbps connection. Better planning and traffic control are the cures.
6. **Privacy and misuse.** Data stored centrally can be copied or read by the wrong person. Staff may waste time on social media or share pirated files. Policies and monitoring are needed, and users must be told about them.
7. **Cable and equipment faults.** A broken cable, a bad connector or a loose port can cut off a computer or a whole segment. Finding the fault in a building with hundreds of cables is slow. Labelled cables and testers (Plate 5.3) help.
8. **Compatibility and maintenance.** Devices from different makers or of different ages may not work well together. Software must be updated on every machine, and old equipment must be replaced in time. This work never ends.

### 5.8.3 Eight applications of computer networks in Nepal

1. **Banking and payments.** ATM, mobile banking, ConnectIPS, eSewa, Khalti and Fonepay QR all run on networks that link branches, shops and phones to bank servers. A transfer made in Dhankuta is visible in Kathmandu in a second. Secure links and encryption protect the money.
2. **Government services.** The Nagarik App, the online passport and driving-licence systems, the Inland Revenue portal and the Department of Customs use networks to serve citizens. Offices in different districts read the same database. This reduces the number of visits to government offices.
3. **Education.** Tribhuvan University results, registration and the NEB exam system work through websites. Colleges use Wi-Fi, e-libraries and learning platforms such as Google Classroom. Students in remote districts can attend classes online.
4. **Health.** Hospitals link reception, laboratory, pharmacy and billing on one LAN. Telemedicine programmes connect health posts to specialist doctors through broadband or VSAT. Reports reach the doctor before the patient does.
5. **Communication.** Mobile calls, SMS, Viber, WhatsApp and e-mail all use the Nepal Telecom, Ncell and ISP networks. Families with members in Qatar or Malaysia keep in touch daily by video call. Remittance information travels on the same networks.
6. **Business and e-commerce.** Online shops such as Daraz take orders, payments and delivery tracking over networks. Small traders sell through Facebook pages and receive money by QR. Supply chains use networked billing and stock software.
7. **Transport and tourism.** Airline and bus booking systems, hotel reservations and ride apps need always-on networks. Trekking agencies use GPS and satellite phones in the mountains. Tourists book flights to Lukla from abroad.
8. **Media and entertainment.** Video streaming, online news and FM radio over the internet reach audiences in every district. Television channels send programmes to cable operators over fibre and satellite links. Gaming and social networks add to the traffic.

## Formula and fact sheet

- Shannon: C = B log₂(1 + S/N). Transfer time = bits / rate.
- Full-mesh links = n(n − 1)/2.
- Usable hosts = 2ʰ − 2; subnet size 2ʰ; mask from prefix /n.
- OSI: Physical, Data link, Network, Transport, Session, Presentation, Application.
- TCP reliable; UDP fast. Ports: HTTP 80, HTTPS 443, SMTP 25, DNS 53, FTP 21.
- Hub = layer 1 (broadcasts), switch = layer 2 (MAC), router = layer 3 (IP).
- Private IPv4: 10/8, 172.16/12, 192.168/16.

## Chapter summary

- Communication needs a sender, receiver, message, medium and protocol; capacity is limited by bandwidth and noise.
- Media may be guided (twisted pair, coax, fibre) or unguided (radio, microwave, satellite).
- Networks are classified by scale (PAN, LAN, MAN, WAN) and by topology (bus, ring, star, mesh, tree).
- Switches work on MAC addresses; routers on IP addresses; layered models (OSI, TCP/IP) divide the work.
- IPv4 addresses split into network and host parts by a mask; subnetting divides a network into smaller ones.

## Practice

**A. Short questions**

1. List the five components of a data communication system.
2. Differentiate simplex, half duplex and full duplex with examples.
3. Differentiate hub, switch and router.
4. Why is fibre preferred over copper for backbones?
5. Differentiate LAN, MAN and WAN.
6. Differentiate TCP and UDP.
7. What is the role of DNS and DHCP?
8. Compare star and bus topologies.

**B. Numerical problems**

9. A channel has B = 4 kHz and S/N = 255. Find the Shannon capacity.
10. How many links does a full mesh of 10 computers need?
11. For 10.0.0.0/8 write the mask and the number of usable hosts.
12. Divide 192.168.5.0/24 into 8 equal subnets: give the mask, the size and the network addresses.
13. A 25 MB file is sent over a 20 Mbps link. Find the ideal time.

**C. Long questions**

14. Explain the seven layers of the OSI model with the function of each.
15. Describe the network topologies with their merits and demerits.
16. Compare circuit switching and packet switching.
17. Differentiate hub, switch and router (5 marks).
18. Describe the transmission media with merits and demerits.
19. Divide 192.168.10.0/24 among departments of 100, 50, 25 and 10 hosts (5 marks).
20. What is a computer network? Give its advantages, disadvantages and applications.
21. How are errors detected? Explain parity, checksum and CRC (5 marks).

::: note Answers and worked solutions
**1.** Sender, receiver, message, medium, protocol.
**2.** Simplex: one direction only (keyboard). Half duplex: both ways but alternately (walkie-talkie). Full duplex: both ways at once (telephone).
**3.** Hub repeats bits to all ports; switch forwards frames to the port of the destination MAC; router forwards packets between networks by IP.
**4.** Fibre has far higher bandwidth, low loss over long distance, and no electromagnetic interference.
**5.** LAN: building or campus; MAN: a city; WAN: countries or the world.
**6.** TCP: connection-oriented, reliable, ordered, with flow control. UDP: connectionless, unreliable but fast and light.
**7.** DNS translates domain names into IP addresses; DHCP automatically assigns IP configuration to hosts.
**8.** Star: central switch, a cable fault isolates one node, easy to extend, but the switch is a single point of failure. Bus: single cable, cheap, but a backbone fault stops everything and performance falls with load.
**9.** C = 4000 × log₂(256) = 4000 × 8 = **32,000 bps**.
**10.** 10 × 9 / 2 = **45** links.
**11.** Mask 255.0.0.0; host bits 24, usable = 2²⁴ − 2 = **16,777,214**.
**12.** 8 subnets need 3 bits → /27, mask 255.255.255.224, size 32. Networks: 192.168.5.0, .32, .64, .96, .128, .160, .192, .224 (30 usable hosts each).
**13.** 25 MB = 25 × 8 = 200 Mbit; 200 / 20 = **10 s**.
**14.** Use the table in §5.5, adding one sentence on the protocol/example for each layer.
**14–16.** Full ten-mark and five-mark answers, with Figures 5.2 and 5.4, are in the section *Model answers* that follows.
**16.** Circuit switching: a path reserved end to end, constant delay, wasted when idle, used by classic telephony. Packet switching: data cut into packets routed independently, efficient sharing, variable delay, the basis of the Internet.
**17–21.** Full model answers (Q17-M to Q21-M) are in the section that follows; each uses Plates 5.1 to 5.7 and Figures 5.1 to 5.6.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q14. Explain the seven layers of the OSI model with the function of each. (10 marks)**

**Introduction.** The **OSI (Open Systems Interconnection) model**, published by ISO in 1984, divides network communication into seven layers. Each layer serves the layer above it and is served by the layer below, so hardware and software from different makers can work together (Figure 5.4).

**The seven layers (from top to bottom)**

1. **Application (7):** gives network services to user programs, such as web browsing, email and file transfer. Protocols: HTTP, SMTP, FTP, DNS.
2. **Presentation (6):** translates, compresses and encrypts data so both ends understand it (ASCII/Unicode, JPEG, TLS).
3. **Session (5):** opens, manages and closes a dialogue between two applications and adds checkpoints for recovery.
4. **Transport (4):** end-to-end delivery between processes using port numbers; splits data into segments and provides flow control and error recovery. Protocols: TCP (reliable), UDP (fast).
5. **Network (3):** logical addressing and routing of packets across networks. Protocols: IP, ICMP; device: router.
6. **Data link (2):** moves frames between two directly connected nodes using MAC addresses, with error detection (CRC) and access control. Devices: switch, bridge.
7. **Physical (1):** sends raw bits as electrical, light or radio signals; defines cables, connectors, voltages and data rates. Devices: hub, repeater, NIC.

**Data units.** Data become segments at transport, packets at network, frames at data link and bits at the physical layer. Each layer adds a header while the data go down (*encapsulation*) and removes it on the way up at the receiver.

| Layer | PDU | Address used | Device |
|---|---|---|---|
| Transport | segment | port | firewall (L4) |
| Network | packet | IP address | router |
| Data link | frame | MAC address | switch |
| Physical | bits | none | hub, cable |

**Conclusion.** The OSI model is a reference model that makes network design and troubleshooting easier because a fault can be traced layer by layer. The Internet itself runs on the simpler TCP/IP model. A useful memory aid, from the top, is "All People Seem To Need Data Processing".

**Q15. Describe the network topologies with their merits and demerits. (10 marks)**

**Introduction.** A **topology** is the arrangement of the nodes and links of a network. The *physical topology* is the real cabling, and the *logical topology* is the path the data follow. The five common topologies are shown in Figure 5.2.

**Topologies**

1. **Bus:** all nodes attach to one backbone cable with a terminator at each end. *Merits:* cheap, easy to extend, little cable. *Demerits:* one break in the backbone stops everyone, performance falls as nodes are added, and collisions occur.
2. **Star:** every node connects to a central hub or switch. *Merits:* easy to install and troubleshoot, one cable failure affects only one node. *Demerits:* the central device is a single point of failure and more cable is needed. This is the most common LAN design today.
3. **Ring:** each node connects to two neighbours, forming a closed loop, and data (or a token) travel in one direction. *Merits:* orderly access, no collisions. *Demerits:* one break or one failed node can stop the ring unless it is a dual ring.
4. **Mesh:** every node is linked to every other node. A full mesh of *n* nodes needs n(n − 1)/2 links; 5 nodes need 10 links. *Merits:* very reliable and fast, many alternative paths. *Demerits:* very expensive and hard to install.
5. **Hybrid or tree:** a combination, for example several star LANs joined by a backbone. *Merits:* scalable and flexible. *Demerits:* complex and costly to manage.

| Topology | Cable | Fault tolerance | Cost | Typical use |
|---|---|---|---|---|
| Bus | least | poor | low | small old LANs |
| Star | medium | good (except hub) | medium | offices, schools |
| Ring | medium | poor | medium | token ring, FDDI |
| Mesh | most | excellent | high | WAN backbone, ISPs |
| Hybrid | varies | good | high | campuses, banks |

**Example.** A college in Kathmandu connects each lab with a star LAN of switches, and joins the labs with a fibre backbone, which is a hybrid (tree) topology.

**Conclusion.** The topology is chosen by cost, reliability and size. Star-based hybrids dominate today, while the mesh is used where reliability matters most.

**Q16-M. Distinguish between the OSI and TCP/IP models. (5 marks)**

Both models describe how data move across a network in layers (Figure 5.4).

| Basis | OSI model | TCP/IP model |
|---|---|---|
| Layers | 7 | 4 (some books use 5) |
| Developed by | ISO, a general reference model | US DoD (ARPANET), built around protocols |
| Top layers | application, presentation, session separate | one application layer |
| Bottom layers | data link and physical separate | one network access layer |
| Use | teaching and troubleshooting | the real Internet |
| Approach | model first, protocols later | protocols first, model later |
| Reliability | transport layer offers connection-oriented service | TCP reliable, UDP unreliable choices |

1. The TCP/IP **application** layer covers the OSI session, presentation and application layers.
2. The **transport** layers match exactly (TCP and UDP).
3. The TCP/IP **internet** layer matches the OSI network layer (IP).
4. The TCP/IP **network access** layer covers the OSI data link and physical layers.

*Example:* a web page request passes HTTP (application), TCP (transport), IP (internet) and Ethernet or Wi-Fi (network access) on the sender's side, and the same layers in reverse at the server.

**Q17-M. Differentiate between a hub, a switch and a router. (5 marks)**

A **hub**, a **switch** and a **router** all connect devices, but they work at different layers of the OSI model and treat traffic differently (Plate 5.5).

1. **Hub (Layer 1):** repeats every incoming signal to all other ports. It does not read addresses, so every computer sees every frame and all computers share one collision domain.
2. **Switch (Layer 2):** reads the destination MAC address of each frame and sends it only to the port where that computer is. It learns the addresses by watching the source of frames.
3. **Router (Layer 3):** reads the destination IP address and forwards the packet to another network. It chooses the best path using a routing table and joins a LAN to the Internet.

In the seven-frame test of Plate 5.5 the hub delivered **35** copies, while the learning switch delivered only **15**, because after learning where A to F are it sent each frame to one port.

| Point | Hub | Switch | Router |
|---|---|---|---|
| Layer | 1 (physical) | 2 (data link) | 3 (network) |
| Address read | none | MAC | IP |
| Forwards to | all ports | one port | next network |
| Collisions | one shared domain | one per port | separate networks |
| Typical use | obsolete | college LAN | home gateway, ISP |

**Example.** In a college lab, computers plug into a switch; the switch connects to a router, and the router connects to the ISP. The hub is no longer used because it wastes bandwidth and is insecure.

**Q18. Describe the transmission media used in data communication, with their merits and demerits. (10 marks)**

**Introduction.** A **transmission medium** is the physical path that carries the signal between sender and receiver. It is of two kinds: **guided (wired)** media, where the signal follows a cable, and **unguided (wireless)** media, where it travels through air or space. The choice decides speed, distance, cost and security (Plate 5.2 and Plate 5.3).

**A. Guided media**

1. **Twisted pair (UTP and STP):** two insulated copper wires twisted to cancel noise, with four pairs in one Cat-5e or Cat-6 cable ending in an RJ-45 plug. Merits: cheap, easy to fit, up to 1 Gbps on 100 m. Demerits: short range and affected by electrical noise (Plate 5.6 shows the T568B wire order).
2. **Coaxial cable:** a copper core, insulation, a braided shield and an outer jacket. Merits: better shielding and longer range than twisted pair; used for cable TV and old bus Ethernet. Demerits: thick, hard to bend and slower than fibre.
3. **Optical fibre:** a hair-thin glass core that carries light by total internal reflection. Single-mode fibre is used for long distance and multimode for short runs. Merits: very high bandwidth, low loss, no electrical noise and hard to tap. Demerits: costly connectors and splicing equipment, and the glass is fragile.

**B. Unguided media**

4. **Radio waves and Wi-Fi:** travel in all directions and pass through walls, so they suit mobiles and laptops. Merits: mobility and no cable. Demerits: interference, limited range and the need for encryption.
5. **Microwave:** narrow beams between dishes in line of sight, about 50 km apart (Plate 5.7). Merits: no trenches, good for hills. Demerits: rain fade and the need for towers.
6. **Satellite:** a dish talks to a satellite in orbit. Merits: covers remote areas such as Himalayan villages. Demerits: high delay (about 250 ms one way for a geostationary satellite) and high cost.
7. **Infrared and Bluetooth:** short-range links for remotes and headsets. Merits: cheap and low power. Demerits: very short range; infrared needs a clear line.

| Medium | Speed | Range | Cost | Noise immunity |
|---|---|---|---|---|
| UTP Cat-6 | 1 Gbps | 100 m | low | fair |
| Coaxial | up to 10 Mbps (old Ethernet) | 185 to 500 m | medium | good |
| Optical fibre | Gbps to Tbps | many km | high | excellent |
| Microwave | tens to hundreds of Mbps | about 50 km | medium | fair (weather) |
| Satellite | Mbps | global | very high | fair (weather) |

**Selection.** Use UTP inside a lab, fibre between buildings and for backbones, microwave across hills and Wi-Fi for mobile users. The signal limit for any medium follows Shannon's formula (Plate 5.1).

**Conclusion.** No medium is best for everything. Real networks combine them: copper to the desk, fibre between floors, wireless for people on the move and microwave or satellite where cables cannot go.

**Q19-M. Divide the network 192.168.10.0/24 among four departments needing 100, 50, 25 and 10 hosts. (5 marks)**

**Method.** Use variable-length subnet masking (VLSM). For each department find the smallest block with at least *hosts + 2* addresses (network and broadcast addresses are not usable), place the largest block first and give every block the next free address (Figure 5.6).

1. **Lab, 100 hosts:** 2⁷ = 128 addresses, so 7 host bits and prefix /25, mask 255.255.255.128. Block 192.168.10.0 to .127, usable .1 to .126 (126 hosts).
2. **Library, 50 hosts:** 2⁶ = 64 addresses, prefix /26, mask 255.255.255.192. Block .128 to .191, usable .129 to .190 (62 hosts).
3. **Office, 25 hosts:** 2⁵ = 32 addresses, prefix /27, mask 255.255.255.224. Block .192 to .223, usable .193 to .222 (30 hosts).
4. **Server room, 10 hosts:** 2⁴ = 16 addresses, prefix /28, mask 255.255.255.240. Block .224 to .239, usable .225 to .238 (14 hosts).

| Department | Subnet | Mask | Usable hosts |
|---|---|---|---|
| Lab | 192.168.10.0/25 | 255.255.255.128 | 126 |
| Library | 192.168.10.128/26 | 255.255.255.192 | 62 |
| Office | 192.168.10.192/27 | 255.255.255.224 | 30 |
| Server room | 192.168.10.224/28 | 255.255.255.240 | 14 |

**Check.** The blocks use 128 + 64 + 32 + 16 = 240 of the 256 addresses, and the last 16 (192.168.10.240 to .255) stay free. Equal-size subnets would not work here, because the lab needs more than the 62 hosts of a /26.

**Q20. What is a computer network? Explain its advantages, disadvantages and applications. (10 marks)**

**Introduction.** A **computer network** is a group of computers and devices connected by cables or radio so that they can exchange data and share resources. Networks are classified by size as PAN, LAN, MAN and WAN, and by layout as bus, star, ring, mesh and tree (Figure 5.2). The Internet is the world's largest network of networks.

**Advantages**

1. **Resource sharing** of printers, disks, software and internet links reduces cost.
2. **Fast communication** by e-mail, chat and video calls.
3. **Central data and backup** keep one latest copy of every file.
4. **Reliability:** data and services can be duplicated on another machine.
5. **Scalability:** new users are added without rebuilding the system.
6. **Central security:** passwords and permissions are set in one place.
7. **Remote access and cooperation:** staff and students can work from any place.

**Disadvantages**

1. **High set-up and running cost** for equipment and skilled staff.
2. **Security risk:** a virus or hacker can spread to all computers.
3. **Dependence on the server or link:** a failure stops many users.
4. **Congestion** when too many users share one link.
5. **Privacy risk** from central storage and misuse.
6. **Maintenance work:** faults, patches and replacement never end.

**Applications in Nepal.** Banking and payments (ConnectIPS, Fonepay, eSewa), government services (Nagarik App, passport and tax portals), education (TU and NEB result systems, online classes), health (hospital LAN, telemedicine), communication (mobile, WhatsApp, Viber), e-commerce (Daraz), transport booking and media streaming (Section 5.8.3).

| Point | Advantage | Disadvantage |
|---|---|---|
| Cost | shared hardware saves money | set-up and staff cost |
| Data | one central copy | one central target for attack |
| Work | users cooperate and share | a failure stops many users |
| Growth | easy to add computers | congestion if not planned |

**Conclusion.** The advantages of networking far outweigh the disadvantages when the network is well designed, secured and maintained. That is why every bank, college, hospital and government office in Nepal now depends on one.

**Q21-M. How are errors detected in data communication? Explain parity, checksum and CRC. (5 marks)**

Noise can flip bits in transit, so the sender adds **redundant bits** that the receiver checks. If the check fails, the frame is discarded and sent again (ARQ). Figure 5.1 shows the three methods tested on every 1-, 2- and 3-bit error in an 8-byte message.

1. **Parity bit:** one extra bit makes the number of 1s even (or odd). It catches every error that flips an odd number of bits (100% of 1-bit and 3-bit errors) but **none** of the 2-bit errors in the test. It is simple and cheap, used in serial lines.
2. **Checksum:** the data are added as 16-bit words and the complement of the sum is sent (used in IP, TCP and UDP headers). It caught all 1-bit errors and most, but not all, 2-bit errors, because two changes can cancel in the sum.
3. **CRC (cyclic redundancy check):** the message is treated as a binary polynomial and divided by a fixed generator; the remainder is sent. Ethernet uses a 32-bit CRC. It detected **all** the 1-, 2- and 3-bit errors in the test and also catches long bursts of errors.

| Method | Extra bits | Strength | Used in |
|---|---|---|---|
| Parity | 1 | weak: misses even numbers of flips | serial ports |
| Checksum | 16 | medium | IP, TCP, UDP headers |
| CRC-32 | 32 | strong | Ethernet frames, ZIP, PNG |

**Correction.** Detection only reports an error. **Error-correcting codes** such as Hamming code add enough bits to repair a single-bit error without retransmission, which is useful in satellite links where resending is slow.
