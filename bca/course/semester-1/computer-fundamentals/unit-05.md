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
**15.** Use the table in §5.3.
**16.** Circuit switching: a path reserved end to end, constant delay, wasted when idle, used by classic telephony. Packet switching: data cut into packets routed independently, efficient sharing, variable delay, the basis of the Internet.
:::
