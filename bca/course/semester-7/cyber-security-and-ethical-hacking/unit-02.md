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

## 2.7 Seeing the ideas: perimeter hardware, the TCP header, the handshake and the flag byte

Packets travel through real boxes. Plate 2.1 shows a firewall appliance on a rack shelf and a ceiling-mounted Wi-Fi access point: two places where a defender captures, filters or inspects the traffic studied in this unit.

```photogrid label="2.1" cols="2" ratio="1.7" caption="Where packets are inspected. (a) A Cisco PIX 515 firewall appliance mounted in a rack: a stateful firewall tracks the handshake state described in section 2.3. (b) A wall-mounted wireless access point: all Wi-Fi traffic of a classroom or office passes through it, so it is a natural capture and monitoring point."
@ photo id="bca401/pix" cap="Rack-mount firewall (PIX 515)"
fit 1.7
focus 0.5 0.55
@ photo id="bca401/ap" cap="Wireless access point"
fit 1.7
focus 0.5 0.45
```

```svgfig label="2.1" caption="The TCP header drawn to scale: 32 bits per row, 20 bytes without options. Ports identify the services, sequence and acknowledgement numbers order the bytes, the 8 flag bits drive the state machine, and the window size controls how much the sender may transmit."
f = Fig(580, 246)
f.text(40, 10, "bit 0", size=9, color=SLATE, anchor="start")
f.text(552, 10, "bit 31", size=9, color=SLATE, anchor="end")
rows = [[("Source port", 16, BLUE), ("Destination port", 16, BLUE)], [("Sequence number", 32, MINT)], [("Acknowledgement number", 32, MINT)],
        [("Offset", 4, SAND), ("", 4, "#e2e8f0"), ("Flags", 8, ROSE), ("Window size", 16, BLUE)],
        [("Checksum", 16, SAND), ("Urgent pointer", 16, SAND)], [("Options and padding (0 to 40 bytes)", 32, "#f1f5f9")]]
for r, row in enumerate(rows):
    x = 40
    for (lab, bits, fl) in row:
        f.box(x, 20 + r * 34, bits * 16, 34, lab, fill=fl, stroke=SLATE, size=9 if bits < 10 else 10)
        x += bits * 16
    f.text(20, 38 + r * 34, str(r * 4), size=9.5, color=NAVY, bold=True)
f.text(290, 236, "byte numbers on the left; the 8 flag bits are CWR ECE URG ACK PSH RST SYN FIN, tested with a bitwise AND", size=9.5, color=SLATE)
```

```svgfig label="2.2" caption="The three-way handshake with the numbers of section 2.3. A SYN consumes one sequence number, so the SYN-ACK acknowledges 2001 (client ISN 2000 + 1) and the final ACK acknowledges 1001 (server ISN 1000 + 1). After this both sides are ESTABLISHED."
f = Fig(580, 232)
f.box(60, 8, 120, 28, "Client", fill=SAND, stroke=AMBER, bold=True, size=11)
f.box(400, 8, 120, 28, "Server", fill=BLUE, stroke=NAVY, bold=True, size=11)
f.line(120, 36, 120, 220, color=SLATE, dash=True)
f.line(460, 36, 460, 220, color=SLATE, dash=True)
f.arrow([(120, 58), (460, 90)], color=NAVY, label="1  SYN (0x02)  seq = 2000", lpos=(290, 62))
f.arrow([(460, 112), (120, 144)], color=TEAL, label="2  SYN-ACK (0x12)  seq = 1000, ack = 2001", lpos=(290, 116))
f.arrow([(120, 166), (460, 198)], color=RED, label="3  ACK (0x10)  ack = 1001", lpos=(290, 170))
f.text(54, 100, "SYN-SENT", size=9.5, color=AMBER, bold=True)
f.text(54, 178, "ESTABLISHED", size=9.5, color=TEAL, bold=True)
f.text(526, 100, "SYN-RECEIVED", size=9.5, color=AMBER, bold=True)
f.text(526, 210, "ESTABLISHED", size=9.5, color=TEAL, bold=True)
```

```svgfig label="2.3" caption="The flag byte. Each of the 8 bits is one flag. 0x12 = 0001 0010 sets ACK (0x10) and SYN (0x02), a normal SYN-ACK. A program tests a flag with a bitwise AND, for example flags AND 0x10 is non-zero when ACK is set. 0x03 sets FIN and SYN together, which no normal stack sends."
f = Fig(580, 168)
names = ["CWR", "ECE", "URG", "ACK", "PSH", "RST", "SYN", "FIN"]
vals = [128, 64, 32, 16, 8, 4, 2, 1]
on = {3, 6}
for i in range(8):
    fl = ROSE if i in on else "#f1f5f9"
    f.box(30 + i * 64, 26, 60, 30, names[i], fill=fl, stroke=SLATE, bold=True, size=11)
    f.box(30 + i * 64, 56, 60, 30, "1" if i in on else "0", fill=fl, stroke=SLATE, bold=True, size=13)
    f.text(60 + i * 64, 98, str(vals[i]), size=9.5, color=SLATE)
f.text(290, 12, "bit values 128 64 32 16 8 4 2 1", size=10, color=NAVY, bold=True)
f.box(30, 112, 250, 44, "0x12 = 16 + 2 = ACK + SYN\nnormal second step of the handshake", fill=MINT, stroke=TEAL, size=10)
f.box(310, 112, 250, 44, "0x03 = 2 + 1 = SYN + FIN\ninvalid: raise an alert", fill=ROSE, stroke=RED, size=10)
```

### 2.7.1 Eight uses of protocol analysis for defenders

1. **Finding unexpected services.** Comparing live ports with an approved list exposes forgotten database or test servers. A college may discover port 3306 open on a lab PC that nobody remembers. Closing it removes a real entry point.
2. **Troubleshooting slow links.** Captures show retransmissions, zero windows and long handshakes. A school network that "feels slow" may be losing packets on one cable. The trace proves where, so the right part is replaced.
3. **Verifying encryption.** An analyst can confirm that a login page really uses TLS and not plain HTTP. If a capture shows readable passwords, the app is unsafe. This check is cheap and should be repeated after each release.
4. **Detecting scans and floods.** Many SYN packets with no final ACK suggest a scan or a SYN flood. A rate rule can raise an alert in seconds. This protects portals such as ConnectIPS from being overwhelmed.
5. **Detecting malformed packets.** Invalid flag combinations, as in Figure 2.3, signal broken tools or probing. Sensors can drop them at the firewall. Normal users never send them.
6. **Incident investigation.** Saved captures show who talked to whom and when. After a breach, the team can see which hosts contacted a suspicious address. This turns guesses into evidence.
7. **Testing firewall rules.** After a rule change, a capture shows whether blocked traffic really stops. Many outages come from a rule that works differently than expected. Testing on a trace avoids guessing.
8. **Teaching and baselining.** Students learn protocols fastest by reading real headers. Teams also record normal traffic volumes as a baseline. Later, a jump from the baseline is an early warning.

## 2.8 Summary and exercises

The TCP header packs ports, sequence numbers and a flag bitmask into 20 bytes; the handshake and sequence arithmetic give a framework for judging normal behaviour; invalid flag combinations are detection signals; and a service inventory, built under written authority, is the baseline against which exposure is measured.

1. Decode the flag bytes 0x14, 0x29 and 0x19. Which are valid?
2. A client with ISN 7000 sends SYN. Give the acknowledgement number in the SYN-ACK. After the client sends 150 bytes of data, what acknowledgement does the server return?
3. Explain with a bitwise expression how a program tests whether the ACK flag is set.
4. List three controls that depend on the transport layer, and what each reads from the header.
5. Compare observed ports {22, 25, 443, 5432} with the approved set {22, 443}. What are the findings and the action for each?
6. Draft four conditions that a discovery authorisation letter should contain.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the TCP three-way handshake with sequence and acknowledgement numbers.**

*Introduction.* TCP is a connection-oriented transport protocol, so both sides must agree on starting sequence numbers before data flows. The three-way handshake does this in three segments (Figure 2.2).

1. **Step 1, SYN.** The client sends a segment with the SYN flag (0x02) and its initial sequence number, say 2000.
2. **Step 2, SYN-ACK.** The server answers with SYN and ACK set (0x12). It gives its own initial number, say 1000, and acknowledges 2001, because a SYN consumes one sequence number.
3. **Step 3, ACK.** The client sends ACK (0x10) with acknowledgement 1001. Both sides are now in the ESTABLISHED state.

| Segment | Flags | Seq | Ack |
|---|---|---|---|
| Client to server | SYN | 2000 | - |
| Server to client | SYN, ACK | 1000 | 2001 |
| Client to server | ACK | 2001 | 1001 |

*Data and closing.* After 300 bytes sent from sequence 2001, the receiver acknowledges 2301. A connection closes with a FIN in each direction, or abruptly with RST.

*Security relevance.* A stateful firewall remembers these states and drops segments that do not fit them. Many SYNs with no final ACK point to a scan or flood.

**Q2 (5 marks). How are TCP flags stored? Show how a program decodes them and name two invalid combinations.**

*Introduction.* The TCP header holds 8 control flags in one byte, so each flag is one bit (Figure 2.3). Programs read them using bitwise operations.

*Layout.* From the left the bits are CWR (128), ECE (64), URG (32), ACK (16), PSH (8), RST (4), SYN (2) and FIN (1). The byte is the sum of the flags that are set.

*Decoding.* To test ACK, a program computes flags AND 0x10; a non-zero result means ACK is set. For 0x12 this gives 0x10, so ACK is set, and 0x12 AND 0x02 is non-zero, so SYN is set too. The byte 0x12 is therefore a SYN-ACK.

| Byte | Binary | Flags | Verdict |
|---|---|---|---|
| 0x02 | 0000 0010 | SYN | Valid, connection request |
| 0x18 | 0001 1000 | PSH, ACK | Valid, data push |
| 0x00 | 0000 0000 | none | Invalid |
| 0x03 | 0000 0011 | FIN, SYN | Invalid |

*Why invalid ones matter.* No compliant TCP stack sends no flags, or SYN with FIN together. They come from faulty software or from probing tools, so an intrusion sensor raises an alert or the firewall drops them.

**Q3 (10 marks). Explain service inventory and network discovery. Describe how the results are compared with an approved list and the governance needed.**

*Introduction.* A network cannot be defended if the owner does not know what runs on it. A service inventory lists every host, open port, protocol and version, and discovery is the process of building it (sections 2.5 and 2.6). Because discovery probes other systems, it is both a technical and a legal activity.

*Methods of discovery.* There are two families:

| Method | How it works | Strength | Risk |
|---|---|---|---|
| Passive | Reads flow records, DHCP and DNS logs, switch tables | Safe for fragile devices | Misses silent hosts |
| Agent based | Software on each host reports what listens | Accurate, includes versions | Needs deployment |
| Active | Sends probes and records replies | Finds unknown devices | Can disturb old equipment |

*Comparing with the approved list.* The team keeps a list of approved ports for each server. A program compares observed ports with it. For observed {22, 25, 443, 5432} against approved {22, 443}, the unapproved listening ports are 25 and 5432, and no approved port is missing. Port 25 (mail) suggests an open relay risk and port 5432 (PostgreSQL) should never face the internet, so each gets an owner and a closing date.

*Reading the results.* Every finding is classified as expected, unknown or forbidden. Unknown items are investigated, forbidden items are removed, and the inventory is updated so the next run starts from a clean baseline.

*Governance rules.*

1. Obtain **written authorisation** with scope, time window, methods, contacts and an emergency stop procedure.
2. Prefer **passive and agent-based** methods on production systems.
3. **Throttle and schedule** active scans and tell the operations team in advance.
4. **Protect the results**, because a list of services and versions helps an attacker too.
5. **Close the loop**: every unexpected item gets an owner, a decision and a due date.

*Legal link.* Probing systems without permission can be an offence under Nepal's Electronic Transactions Act 2063 (Unit 7), so a signed letter is the first deliverable, not an extra.

*Conclusion.* A good inventory combines several discovery methods, compares them with an approved baseline and is run under written authority. The result is a smaller attack surface and an audit trail that shows the work was lawful.
