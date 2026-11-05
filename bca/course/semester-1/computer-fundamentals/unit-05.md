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

```photogrid label="5.1" cols="4" ratio="1.15" caption="Real transmission media: (a) coaxial cable with its braided shield, (b) Cat-5e UTP cable with RJ-45 plugs, (c) a fibre-optic cable, (d) a single glass fibre stripped of its coating."
@ photo id="bca101/coax" cap="Coaxial: copper core, insulation, braid shield"
@ photo id="bca101/rj45" cap="UTP Cat-5e with RJ-45 connectors (4 twisted pairs)"
@ photo id="bca101/fibre-cable" cap="Fibre-optic cable: glass strands in a protective jacket"
@ photo id="bca101/fibre-strand" cap="Bare glass fibre: thinner than a hair, carries light"
```

**Multiplexing** shares one link among many signals: **FDM** (different frequencies), **TDM** (different time slots), **WDM** (different light colours on fibre). **Switching** moves data through a network: **circuit switching** reserves a dedicated path for the whole call (telephone); **packet switching** cuts data into packets that are routed independently and reassembled (the Internet).

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

```svgfig label="5.1" caption="The five network topologies with the main merit and demerit of each."
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

```photogrid label="5.2" cols="3" ratio="1.25" caption="Common network devices: (a) a five-port Gigabit switch, (b) the inside of a wireless router showing the board and antennas, (c) a 3Com Ethernet network interface card (NIC) with its RJ-45 port."
@ photo id="bca101/switch" cap="Switch: forwards frames by MAC address (Layer 2)"
@ photo id="bca101/router" cap="Router: forwards packets by IP address (Layer 3)"
@ photo id="bca101/nic" cap="NIC: gives the host a MAC address and a cable port"
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

```svgfig label="5.2" caption="OSI seven-layer model compared with the four-layer TCP/IP model, with protocols and data units."
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

Other services: **DHCP** hands out IP addresses automatically; **DNS** maps names such as `tu.edu.np` to IP addresses; **NAT** lets a whole home network share one public IP; **ARP** finds the MAC address that goes with an IP on the LAN; **ICMP** carries errors and powers `ping`.

## 5.7 Wireless and mobile networks

**Wi-Fi** (IEEE 802.11) gives LAN access by radio; **Bluetooth** gives short-range PAN links; **cellular** networks (2G, 3G, 4G LTE, 5G) cover wide areas through cells served by base stations; **NFC** works within a few centimetres (contactless payment). In Nepal, Wi-Fi in homes and colleges, FTTH broadband and 4G (and now 5G trials) are the everyday forms.

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
**14–16.** Full ten-mark and five-mark answers, with Figures 5.1 and 5.2, are in the section *Model answers* that follows.
**16.** Circuit switching: a path reserved end to end, constant delay, wasted when idle, used by classic telephony. Packet switching: data cut into packets routed independently, efficient sharing, variable delay, the basis of the Internet.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q14. Explain the seven layers of the OSI model with the function of each. (10 marks)**

**Introduction.** The **OSI (Open Systems Interconnection) model**, published by ISO in 1984, divides network communication into seven layers. Each layer serves the layer above it and is served by the layer below, so hardware and software from different makers can work together (Figure 5.2).

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

**Introduction.** A **topology** is the arrangement of the nodes and links of a network. The *physical topology* is the real cabling, and the *logical topology* is the path the data follow. The five common topologies are shown in Figure 5.1.

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

Both models describe how data move across a network in layers (Figure 5.2).

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
