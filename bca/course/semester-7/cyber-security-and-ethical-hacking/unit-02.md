---
subject: Cyber Security and Ethical Hacking
grade: BCA Semester 7
unit: 2
title: Network Protocol Analysis, TCP Flag Math and Asset Discovery Governance
hours: 6
area: BCA 401 · Cyber Security and Ethical Hacking · Unit 2
---

A network administrator who cannot read a packet is like a doctor who cannot read a chart. Defenders spend a good part of their working day reading captured traffic, firewall logs and flow records to answer simple questions: *is this connection normal, who started it, and what is listening on this server that should not be?* This unit builds the skill underneath: reading the TCP header at the bit level, recognising healthy and invalid flag combinations, and keeping an accurate, *authorised* inventory of the services in your network.

::: key What this unit gives you
- The layered model and where each security control sits.
- The RFC 793 TCP header: fields, flag bits, the three-way handshake and sequence arithmetic.
- A header parser and flag decoder that classify valid and invalid combinations.
- Service inventory by comparison with an approved baseline, and the governance rules that make discovery lawful.
:::

## 2.1 Layers and what each reveals

Traffic is encapsulated: application data inside a TCP segment, inside an IP packet, inside an Ethernet frame. Each layer offers different evidence and different controls.

| Layer | Unit | Evidence a defender reads | Typical control |
|---|---|---|---|
| Link | Frame | MAC addresses, VLAN tags | Port security, 802.1X |
| Network | Packet | IP addresses, TTL, fragments | Packet filters, anti-spoofing |
| Transport | Segment | Ports, flags, sequence numbers | Stateful firewalls, rate limits |
| Application | Message | Requests, DNS names, TLS metadata | Proxies, WAF, TLS inspection where lawful |

Capturing traffic is itself a sensitive act: packet captures can hold passwords and personal data. Capture only on networks you own or are explicitly authorised to monitor, minimise what you keep, protect captures like any confidential record and delete them on schedule. The legal basis for this in Nepal is covered in Unit 7.

## 2.2 The TCP header (RFC 793)

A TCP header has a fixed 20-byte part:

| Bytes | Field | Notes |
|---|---|---|
| 0–1 | Source port | 16 bits |
| 2–3 | Destination port | Well-known 0–1023, registered 1024–49151, dynamic 49152–65535 |
| 4–7 | Sequence number | 32 bits, byte position of the first data byte |
| 8–11 | Acknowledgement number | Next byte expected, valid when ACK is set |
| 12 (high nibble) | Data offset | Header length in 32-bit words; minimum 5 (20 bytes) |
| 13 (low 6 bits, plus later bits) | Flags | FIN 0x01, SYN 0x02, RST 0x04, PSH 0x08, ACK 0x10, URG 0x20 |
| 14–15 | Window | Receive window in bytes |
| 16–17 | Checksum | Over header, data and a pseudo-header |
| 18–19 | Urgent pointer | Used only with URG |

Later RFCs added two more flag bits (ECE 0x40 and CWR 0x80) for congestion notification. The flag byte is therefore a **bitmask**: several flags can be set together by adding their values, and a program tests a flag with a bitwise AND. A SYN-ACK is 0x02 + 0x10 = 0x12.

## 2.3 Handshake and sequence arithmetic

A connection opens with three segments:

1. The client sends **SYN** (flags 0x02) with its initial sequence number (ISN), say 2000.
2. The server replies **SYN-ACK** (0x12) with its own ISN, say 1000, and acknowledgement 2001: a SYN consumes one sequence number, so the next byte expected is ISN + 1.
3. The client sends **ACK** (0x10) with acknowledgement 1001.

Data advances the sequence number by the number of bytes sent: after 300 bytes from sequence 2001, the receiver acknowledges 2301. A connection closes with **FIN** in each direction (FIN consumes one sequence number as well), or abruptly with **RST**. A stateful firewall or intrusion sensor tracks these states; a flag combination that no compliant implementation produces is evidence of a faulty device, a tool probing the network, or crafted traffic, and so is worth an alert.

The program decodes a 20-byte header taken from a capture (a SYN-ACK from a server on port 443) with Python's `struct` module, the standard way to unpack network byte order.

```python
import struct
FLAGS = [("FIN", 0x01), ("SYN", 0x02), ("RST", 0x04), ("PSH", 0x08), ("ACK", 0x10), ("URG", 0x20)]

def names(f):
    return ",".join(n for n, bit in FLAGS if f & bit)

raw = bytes.fromhex("01bbc93a000003e8000007d15012ffff00000000")
sport, dport, seq, ack, off_flags, window, checksum, urgent = struct.unpack("!HHIIHHHH", raw)
header_bytes = (off_flags >> 12) * 4
flags = off_flags & 0x3F
print(f"src {sport} dst {dport} seq {seq} ack {ack} hdr {header_bytes} bytes flags {names(flags)} window {window}")
```
```output
src 443 dst 51514 seq 1000 ack 2001 hdr 20 bytes flags SYN,ACK window 65535
```
The source port 443 shows that this segment came from an HTTPS server; the destination 51514 is the client's dynamic port. The acknowledgement 2001 tells us the client's ISN was 2000. The data offset nibble is 5, so the header is 20 bytes, i.e. there are no options. The flags 0x12 decode to SYN and ACK, the second step of the handshake. The checker confirmed each field by independent byte slicing.

## 2.4 Classifying flag combinations

Legitimate traffic uses a small set of combinations: SYN (open), SYN-ACK, ACK, PSH-ACK (data), FIN-ACK (close), RST and RST-ACK. Combinations that violate the protocol's rules are never produced by a correct stack: no flags at all; SYN together with FIN (open and close at once); SYN together with RST. A monitoring rule can flag them for investigation.

```python
FLAGS = [("FIN", 0x01), ("SYN", 0x02), ("RST", 0x04), ("PSH", 0x08), ("ACK", 0x10), ("URG", 0x20)]

def names(f):
    return ",".join(n for n, bit in FLAGS if f & bit)

for f in [0x02, 0x12, 0x10, 0x18, 0x11, 0x04, 0x00, 0x03]:
    invalid = f == 0 or (f & 0x03) == 0x03 or (f & 0x06) == 0x06
    print(f"0x{f:02x}: {names(f) or 'none'}{' <- invalid combination' if invalid else ''}")
```
```output
0x02: SYN
0x12: SYN,ACK
0x10: ACK
0x18: PSH,ACK
0x11: FIN,ACK
0x04: RST
0x00: none <- invalid combination
0x03: FIN,SYN <- invalid combination
```
The test `(f & 0x03) == 0x03` asks whether both the FIN and SYN bits are set, and `(f & 0x06) == 0x06` asks about SYN and RST. Only 0x00 and 0x03 are flagged. The rule is a *detection* rule: it describes what to alert on, and says nothing about how to produce such traffic.

::: note
Treat an alert of this kind as a lead, not a verdict. Firewalls and load balancers sometimes rewrite or drop packets in ways that cause oddities, so correlate with the device's logs before concluding that something hostile is happening.
:::

## 2.5 Service inventory

You cannot protect what you do not know you have. A **service inventory** records, for each host, the services that are *supposed* to listen, with owner, purpose and expected exposure. The security value comes from comparing the approved baseline with what is **actually observed** by an authorised discovery process or from the hosts themselves (the operating system's list of listening sockets, configuration-management data, cloud asset APIs, flow logs). The difference has two parts: observed but not approved (an unexpected service: investigate and close or approve) and approved but not observed (a failed service or a stale record).

```python
approved = {22, 80, 443}
observed = {22, 80, 443, 3306, 8080}
print(f"unapproved listening ports: {sorted(observed - approved)}")
print(f"approved but not listening: {sorted(approved - observed)}")
```
```output
unapproved listening ports: [3306, 8080]
approved but not listening: []
```
Ports 3306 (a database) and 8080 (an alternative web port) are present without approval. A database port reachable from outside the data tier is a classic finding in audits: the fix is either a firewall rule restricting it to the application servers or shutting the service down.

## 2.6 Governance of discovery

Discovery tools probe other systems, so *how* they are used is a legal and professional matter, not only a technical one.

- **Written authorisation** from the system owner defining scope (address ranges, hosts), time window, methods, contacts and what to do if something breaks. Unauthorised probing of someone else's systems can be an offence under Nepal's Electronic Transactions Act (Unit 7).
- **Prefer passive and agent-based methods** on your own network: flow records, DHCP and DNS logs, configuration management databases, cloud APIs and endpoint agents give an inventory without touching fragile devices.
- **Schedule and throttle** active discovery on production, notify the operations team and keep the tool configuration under change control.
- **Protect the results.** An accurate inventory of services and versions is itself sensitive; store it with access control and share it on a need-to-know basis.
- **Close the loop.** Every unexpected item gets an owner, a decision and a due date; track the percentage of assets with a known owner as a metric.

## 2.7 Summary and exercises

The TCP header packs ports, sequence numbers and a flag bitmask into 20 bytes; the handshake and sequence arithmetic give a framework for judging normal behaviour; invalid flag combinations are detection signals; and a service inventory, built under written authority, is the baseline against which exposure is measured.

1. Decode the flag bytes 0x14, 0x29 and 0x19. Which are valid?
2. A client with ISN 7000 sends SYN. Give the acknowledgement number in the SYN-ACK. After the client sends 150 bytes of data, what acknowledgement does the server return?
3. Explain with a bitwise expression how a program tests whether the ACK flag is set.
4. List three controls that depend on the transport layer, and what each reads from the header.
5. Compare observed ports {22, 25, 443, 5432} with the approved set {22, 443}. What are the findings and the action for each?
6. Draft four conditions that a discovery authorisation letter should contain.
