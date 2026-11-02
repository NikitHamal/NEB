---
subject: Computer Networking
grade: BCA Semester 5
unit: 1
title: Introduction to Computer Networks
hours: 4
area: BCA 301 · Computer Networking · Unit 1
---

When you open a page in your browser, a few hundred bytes leave your laptop, cross a Wi-Fi link, an Ethernet cable, a fibre to your ISP, perhaps an undersea cable, and arrive at a server that answers in less than a tenth of a second. Nobody designed that path for you in particular. It works because every device agrees on **layers**: small, replaceable pieces that each do one job and talk to the same piece on the other side. This unit gives you the vocabulary, the two layered models you will be examined on, and the first calculations (delay and throughput) that run through the whole book.

::: key What this unit gives you
- What a network is, the main network types and topologies, and the devices that build them.
- The OSI reference model and the TCP/IP model, layer by layer, and how data is encapsulated.
- Delay, throughput, bandwidth–delay product and why they decide how fast a network *feels*.
- Standards bodies and the vocabulary used for the rest of the book.
:::

## 1.1 What a network is

A **computer network** is a set of autonomous devices (hosts) connected by links so that they can exchange data. The devices at the edge are **end systems** or **hosts**: PCs, phones, servers, sensors. The devices in the middle that move data from link to link are **intermediate systems**: switches and routers. Every network has four ingredients: **senders and receivers**, a **medium** (copper, fibre, radio), **protocols** (the agreed rules) and **addressing** (so data can find its destination).

A **protocol** defines three things: the **syntax** (format of messages, field sizes), the **semantics** (what each field means and what action to take) and the **timing** (when to send, how fast, what to do on silence). HTTP, TCP, IP and Ethernet are protocols; so are the rules for how a teacher chooses who may speak in a class.

### Why we network

- **Resource sharing**: one printer, one database server, one Internet connection for many users.
- **Communication**: e-mail, voice and video calls, messaging.
- **Reliability**: data replicated over several machines; a failed machine does not stop the service.
- **Cost saving**: many cheap clients and a few strong servers instead of many strong machines.
- **Scalability**: add a server or a link when load grows.

## 1.2 Types of networks

| Type | Typical span | Typical technology | Example |
|---|---|---|---|
| PAN | a few metres | Bluetooth, USB | phone ↔ earbuds |
| LAN | a room to a campus | Ethernet, Wi-Fi | college computer lab |
| MAN | a city | fibre rings, metro Ethernet | cable-TV or ISP network in Kathmandu valley |
| WAN | country to world | leased lines, MPLS, submarine cable | an ISP backbone; the Internet |

A **LAN** is usually owned by one organisation, runs at high speed (100 Mbps to 10 Gbps) and has low error rates. A **WAN** crosses public property, so it usually *rents* capacity from carriers, is slower per rupee spent and has longer delays. The **Internet** is a network of networks: thousands of independently owned networks (autonomous systems) interconnected using the one protocol, IP. An **intranet** is an organisation's private network using Internet technology; an **extranet** extends it to selected partners. A **VPN** builds a private network across the public Internet using encryption (Unit 7).

### Client–server and peer-to-peer

In the **client–server** model a server waits for requests and clients start them (web, e-mail). In **peer-to-peer** every node can be both (BitTorrent, some voice-call systems). Most real services mix both: your messaging app is a client of a server but may exchange media directly peer to peer.

## 1.3 Topologies

The **topology** is the arrangement of links.

| Topology | Description | Links for n nodes | Strength | Weakness |
|---|---|---|---|---|
| Bus | all nodes on one shared cable | 1 cable | cheap, little cable | one break stops everyone; collisions |
| Star | each node to a central hub or switch | n | easy to add or remove, failures isolated | centre is a single point of failure |
| Ring | each node to two neighbours in a loop | n | orderly access (token) | one break stops a single ring |
| Mesh (full) | every node to every other | n(n − 1)/2 | very reliable | cabling grows quickly |
| Tree | stars connected hierarchically | n − 1 | scalable | root dependence |
| Hybrid | mixture | — | fits real buildings | more complex |

For a full mesh of 10 nodes you need 10 × 9 / 2 = 45 links and 9 ports per node; this is why full meshes appear only in small cores. Modern LANs are almost always **physical stars** (every cable ends at a switch) even if they behave like a logical bus or ring inside.

## 1.4 Network devices

- **Repeater**: regenerates a weakened signal (layer 1).
- **Hub**: a multi-port repeater; whatever arrives on one port goes out on all others, so all ports share one collision domain (layer 1). Obsolete.
- **Bridge / switch**: learns which MAC address is behind which port and forwards frames only where needed (layer 2). Each port is a separate collision domain.
- **Router**: forwards packets between networks using IP addresses and a routing table (layer 3). Each interface is a separate broadcast domain.
- **Gateway**: a general word for a device converting between different protocol stacks, also used for the "default gateway" router.
- **Access point**: bridges Wi-Fi to wired Ethernet. **Modem**: converts digital data to a signal suited to a medium (telephone line, coaxial cable, fibre ONT).
- **Firewall**: filters traffic by rules (Unit 7). **Load balancer**: spreads requests over several servers.

A *collision domain* is the set of devices whose simultaneous transmissions interfere; a *broadcast domain* is the set that receives a broadcast frame. A switch divides collision domains; a router (or VLAN) divides broadcast domains.

## 1.5 Layered architecture and protocol stacks

Network software is built in **layers**. Layer n offers a **service** to layer n + 1 above it and uses the service of layer n − 1 below. Layer n on one machine talks to layer n on the other using a **protocol**, but in reality the data goes down the stack, over the medium and up the other stack. Layering gives modularity (replace Wi-Fi by Ethernet without changing the browser), easier standardisation and easier fault finding. The cost is some overhead and occasional duplication of functions.

### Connection-oriented and connectionless service

A **connection-oriented** service (TCP, telephone call) sets up a connection, uses it, and releases it; data arrives in order and reliably. A **connectionless** service (UDP, IP, postal letters) sends each unit independently with no set-up; units may be lost, duplicated or reordered. "Reliable" means the service recovers from loss by retransmission; "unreliable" means *best effort*, not "bad".

## 1.6 The OSI reference model

The **Open Systems Interconnection** model of ISO (1984) has seven layers. It is a *reference* model: nobody implements it exactly, but its vocabulary is universal.

| No. | Layer | Unit of data | Job | Examples |
|---|---|---|---|---|
| 7 | Application | message | services seen by user programs | HTTP, SMTP, DNS, FTP |
| 6 | Presentation | message | data format, encryption, compression | TLS record encoding, JPEG, UTF-8 |
| 5 | Session | message | dialogue control, checkpoints, synchronisation | RPC sessions, NetBIOS |
| 4 | Transport | segment / datagram | process-to-process delivery, reliability, flow and congestion control | TCP, UDP |
| 3 | Network | packet | host-to-host delivery across networks, routing, logical addressing | IP, ICMP, OSPF |
| 2 | Data link | frame | node-to-node delivery on one link, framing, MAC addressing, error detection | Ethernet, Wi-Fi, PPP |
| 1 | Physical | bit | transmission of raw bits as signals | cables, connectors, radio, line coding |

::: key Remember the order
Please Do Not Throw Sausage Pizza Away — Physical, Data link, Network, Transport, Session, Presentation, Application (bottom to top). The lower three layers are the **network-support layers**; the upper three are **user-support layers**; the transport layer links the two groups.
:::

**Physical address, logical address, port.** A frame carries a **MAC address** (layer 2, local), a packet carries an **IP address** (layer 3, end to end), a segment carries **port numbers** (layer 4, identifies the process, for example 80 for HTTP). On the way, the MAC addresses are rewritten at every router, the IP addresses are not (unless NAT is used), the ports are not.

## 1.7 The TCP/IP model

The model of the Internet has four (sometimes drawn as five) layers and grew from working protocols rather than from a committee.

| TCP/IP layer | Corresponds to OSI | Main protocols |
|---|---|---|
| Application | 5, 6, 7 | HTTP, HTTPS, SMTP, IMAP, DNS, DHCP, SSH |
| Transport | 4 | TCP, UDP |
| Internet | 3 | IPv4, IPv6, ICMP, ARP (often placed between 2 and 3) |
| Link (network access) | 1, 2 | Ethernet, Wi-Fi, PPP |

The TCP/IP stack is the standard in practice because it was already deployed, free, and simple. Compare: OSI had a clean theory but its protocols arrived late; TCP/IP had protocols first and a model written afterwards. Both models treat the network layer service differently: OSI supported both connection-oriented and connectionless service at layer 3 but only connection-oriented at layer 4 in its original form, whereas TCP/IP supports only connectionless at the Internet layer but both at the transport layer.

### Encapsulation

When the application hands a message to TCP, TCP adds a **header** to form a segment; IP adds its header to form a packet; the link layer adds a header and (usually) a trailer to form a frame; the physical layer turns it into signals. The receiver reverses the process (decapsulation). With a 20-byte TCP header, a 20-byte IPv4 header and an 18-byte Ethernet header and trailer, an application payload of 1460 bytes becomes a frame of 1460 + 20 + 20 + 18 = 1518 bytes. The headers are **overhead**: a 1-byte message in the same frame needs 58 bytes of headers.

## 1.8 Performance: bandwidth, delay and throughput

**Bandwidth** (here: link rate) is the number of bits per second the link can transmit, for example 100 Mbps. **Throughput** is the rate actually achieved end to end; it is limited by the slowest link (the *bottleneck*) and by protocols. **Latency** is the time from the start of sending to the start of receiving. It has four parts.

| Component | Formula | Depends on |
|---|---|---|
| Transmission delay | L / R (bits ÷ bits per second) | packet length, link rate |
| Propagation delay | d / s (metres ÷ speed of signal) | distance, medium (≈ 2 × 10⁸ m/s in fibre or copper) |
| Queuing delay | varies | traffic load |
| Processing delay | small | router speed |

::: example Transmission versus propagation
A 1500-byte packet on a 100 Mbps link: L / R = 12,000 bits / 10⁸ bps = 0.12 ms. If the link is 2000 km long, the propagation delay is 2 × 10⁶ m / (2 × 10⁸ m/s) = 10 ms. So on this long link the propagation delay is about 83 times larger than the transmission delay; making the link faster to 1 Gbps would reduce the 0.12 ms by a factor of 10 but would barely change the 10 ms.
:::

### Store-and-forward and pipelining

A router receives a whole packet before it forwards it (**store and forward**). For a packet of L bits crossing N links of rate R, the total transmission time is N × L / R. For an 8000-byte packet on 3 links of 1 Mbps: 3 × 64,000 / 10⁶ = 0.192 s. If instead a message of 10⁶ bits is cut into 1000 packets of 1000 bits, the first packet needs 3 ms to arrive and each following packet arrives 1 ms later, so the whole message needs 3 ms + 999 ms = 1.002 s. Without packetising, the whole message would take 3 × 1 s = 3 s. **Pipelining** is why packet switching wins for bulk data.

### Bandwidth–delay product

The **bandwidth–delay product** (BDP) = rate × round-trip (or one-way) delay is the number of bits "in flight" on a full pipe. A 1 Gbps path with a 50 ms delay holds 10⁹ × 0.05 = 50,000,000 bits (6.25 MB). A sender must be allowed to have this much unacknowledged data to keep the link busy; this is why TCP window size matters (Unit 5).

::: note Effective throughput
If a link of rate R is shared fairly by k users, each gets R / k. A file of F bits over a path with bottleneck R' and round-trip time T takes about F / R' + T (plus set-up round trips). For small files the round trips dominate; for large files the rate does.
:::

## 1.9 Standards and organisations

| Body | Role |
|---|---|
| ISO | OSI reference model |
| ITU-T | telecom standards (G., V., X. series), including DSL and fibre |
| IEEE | LAN standards: 802.3 Ethernet, 802.11 Wi-Fi, 802.1Q VLAN |
| IETF | Internet standards as RFCs: IP (RFC 791), TCP (RFC 9293), HTTP (RFC 9110) |
| IANA / ICANN | numbers (IP blocks, ports) and names (DNS root) |
| W3C | web standards (HTML, CSS) |

In Nepal the **Nepal Telecommunications Authority (NTA)** licenses ISPs and telecom operators, and the **Nepal Telecom** and private ISPs provide Internet access over fibre, wireless and mobile networks.

## Practising the commands

The following program uses only the Python standard library to build a miniature layered stack: it wraps an application message in a transport header, a network header and a frame header, and then unwraps it. It shows encapsulation as plain data.

```python
msg = b"HELLO"
tcp = b"[TCP sport=5000 dport=80]" + msg
ip = b"[IP src=10.0.0.5 dst=93.184.216.34]" + tcp
frame = b"[ETH dst=aa:bb src=cc:dd]" + ip + b"[FCS]"
print(len(msg), len(tcp), len(ip), len(frame))
for name in ("[ETH", "[IP", "[TCP"):
    start = frame.index(name.encode()); end = frame.index(b"]", start) + 1
    print(name + "…]", frame[start:end].decode())
print(frame.decode())
```
```output
5 30 65 95
[ETH…] [ETH dst=aa:bb src=cc:dd]
[IP…] [IP src=10.0.0.5 dst=93.184.216.34]
[TCP…] [TCP sport=5000 dport=80]
[ETH dst=aa:bb src=cc:dd][IP src=10.0.0.5 dst=93.184.216.34][TCP sport=5000 dport=80]HELLO[FCS]
```
## Formula and fact sheet

- Transmission delay = L / R; propagation delay = d / s with s ≈ 2 × 10⁸ m/s in cable and fibre.
- Store and forward over N equal links: N × L / R for one packet; (N + P − 1) × L / R for P packets of L bits pipelined.
- BDP = rate × delay. Full mesh links = n(n − 1)/2.
- OSI layers (top to bottom): Application, Presentation, Session, Transport, Network, Data link, Physical. TCP/IP: Application, Transport, Internet, Link.
- Data units: bit, frame, packet, segment (datagram for UDP), message.

## Chapter summary

- A network moves data between hosts using agreed protocols, addresses and media. LAN, MAN and WAN differ by span; the Internet is a network of networks.
- Topology affects cost and reliability; today's LANs are physical stars built around switches.
- Layering divides the work: each layer serves the one above and talks to its peer. OSI has seven layers, TCP/IP four.
- Data is encapsulated on the way down and decapsulated on the way up; headers are overhead.
- Latency = transmission + propagation + queuing + processing; BDP tells how much data fills the pipe.

## Practice

1. Define protocol and explain syntax, semantics and timing.
2. Compare LAN, MAN and WAN with one example each.
3. A full mesh joins 12 computers. How many links and how many ports per computer?
4. List the seven OSI layers and give the data unit and one protocol for layers 2, 3 and 4.
5. State two differences between the OSI and TCP/IP models.
6. A frame carries 1460 bytes of application data with TCP, IPv4 and Ethernet headers (18 bytes of header and trailer). How many bytes does it occupy and what fraction is payload?
7. A 1500-byte packet crosses one 100 Mbps, 2000 km link. Find the transmission and propagation delays.
8. A 10⁶-bit message crosses 3 links of 1 Mbps. Compare sending it whole with sending it as 1000 packets of 1000 bits.
9. Compute the bandwidth–delay product of a 1 Gbps link with 50 ms delay.
10. Distinguish a hub, a switch and a router in terms of collision and broadcast domains.

::: note Answers and worked solutions
**1.** A protocol is the set of rules for communication between peer entities. Syntax: message format and field sizes. Semantics: the meaning of fields and the actions to take. Timing: when and how fast to send and what to do on delay.
**2.** LAN: a college lab on Ethernet. MAN: a city-wide cable or fibre network of an ISP. WAN: an ISP backbone or the Internet. They differ by span (metres to kilometres to continents), ownership and speed.
**3.** 12 × 11 / 2 = 66 links; each computer has 11 ports.
**4.** Layer 2 data link: frame, Ethernet. Layer 3 network: packet, IP. Layer 4 transport: segment, TCP (UDP: datagram).
**5.** OSI has seven layers and a clean service/interface/protocol split but few real implementations; TCP/IP has four layers, grew from protocols, and is what the Internet runs. OSI layer 3 offers both connection modes, TCP/IP's Internet layer only connectionless.
**6.** 1460 + 20 + 20 + 18 = 1518 bytes; payload fraction 1460 / 1518 = 96.2 %.
**7.** Transmission 12,000 / 10⁸ = 0.12 ms; propagation 2 × 10⁶ / (2 × 10⁸) = 10 ms.
**8.** Whole: 3 × 10⁶ / 10⁶ = 3 s. Packetised: 3 ms + 999 × 1 ms = 1.002 s.
**9.** 10⁹ × 0.05 = 50,000,000 bits = 6.25 MB.
**10.** Hub: one collision domain and one broadcast domain for all ports. Switch: each port its own collision domain, still one broadcast domain (without VLANs). Router: each interface its own collision and broadcast domain.
:::
