---
subject: Computer Networking
grade: BCA Semester 5
unit: 5
title: The Transport Layer
hours: 6
area: BCA 301 · Computer Networking · Unit 5
---

IP delivers a packet to a *machine*; the transport layer delivers data to a *process* on that machine and, if the application wants it, makes the unreliable network behave like a reliable pipe. Two protocols dominate: **UDP**, which adds almost nothing to IP, and **TCP**, which adds connections, reliability, flow control and congestion control. Understanding TCP's window arithmetic is one of the most-examined skills in the subject, so the numbers here are recomputed by `check_networking.py` and by the programs at the end of the unit.

::: key What this unit gives you
- Functions of the transport layer, ports, sockets, multiplexing and demultiplexing.
- UDP: the datagram, checksum and uses; reliable data transfer principles.
- TCP: segment header, connection set-up and release, flow control, error control, timers, congestion control (slow start, AIMD, Tahoe, Reno).
- Elements of transport protocols: addressing, connection management, buffering, crash recovery.
:::

## 5.1 Functions of the transport layer

The transport layer provides **process-to-process** communication using **port numbers** (16 bits, 0–65,535). Well-known ports 0–1023 identify standard services (80 HTTP, 443 HTTPS, 53 DNS, 25 SMTP, 22 SSH, 21 FTP, 67/68 DHCP); registered ports go to 49151; the rest are **ephemeral** ports a client picks for itself. A **socket address** is an IP address plus a port, and a TCP connection is identified by the four-tuple (source IP, source port, destination IP, destination port); that is why a web server on port 80 can serve thousands of clients.

**Multiplexing** at the sender gathers data from several processes and marks each segment with ports; **demultiplexing** at the receiver delivers each segment to the right socket. UDP demultiplexes by (destination IP, destination port) only; TCP by the whole four-tuple.

The layer may also provide **segmentation**, **end-to-end error control**, **flow control** (match the receiver's speed) and **congestion control** (match the network's capacity). The difference between the flow and the congestion is the key distinction: flow control protects the receiver, congestion control protects the network.

## 5.2 UDP

The **User Datagram Protocol** is connectionless, unreliable and message-oriented. Its header is 8 bytes: source port, destination port, length and checksum (2 bytes each). There is no handshake, no retransmission, no ordering and no congestion control, so it has **low overhead and low delay**. Use it for DNS queries, DHCP, streaming and calls, online games, SNMP and for new transports built on top of it (QUIC runs over UDP).

The **checksum** is the Internet checksum (Unit 3) computed over the UDP header, the data and a **pseudo-header** (source IP, destination IP, protocol 17, UDP length), so that a datagram delivered to the wrong host is detected. In IPv4 the UDP checksum is optional (0 means none); in IPv6 it is mandatory.

**RPC** (remote procedure call) lets a program call a procedure on another machine as if it were local: a client *stub* packs the parameters (marshalling) and sends them; a server stub unpacks, calls the real procedure and returns the result. It is usually built on UDP or TCP and is the base of many distributed systems (Unit on Distributed Systems later in the course).

## 5.3 Principles of reliable data transfer

Reliable transfer over an unreliable channel is built step by step:

| Version | Channel assumption | Mechanism added |
|---|---|---|
| rdt 1.0 | perfectly reliable | nothing |
| rdt 2.0 | bit errors, no loss | checksum, ACK and NAK, retransmit |
| rdt 2.1 / 2.2 | ACK or NAK may be corrupt | sequence numbers 0/1; duplicate ACK replaces NAK |
| rdt 3.0 | errors and loss | countdown **timer** and retransmission (stop-and-wait, alternating bit) |
| Pipelined | the above, but fast | GBN or SR with sliding windows (Unit 3) |

Stop-and-wait is correct but slow: on a 1 Gbps path with 30 ms round trip and 1000-byte packets, utilisation is (8000 / 10⁹) / (30 ms + 8 µs) ≈ 0.027 %. Pipelining raises it almost linearly with the window. TCP's mechanism is a hybrid: cumulative acknowledgements like GBN, but with receiver buffering of out-of-order segments like SR.

## 5.4 TCP services and the segment

TCP is **connection-oriented**, **reliable**, **full-duplex**, **byte-stream** based and flow- and congestion-controlled. The application writes bytes; TCP cuts them into segments no larger than the **MSS** (usually 1460 bytes on Ethernet: MTU 1500 − 20 − 20) and numbers *each byte* with a 32-bit sequence number.

| Field | Bits | Meaning |
|---|---|---|
| Source and destination port | 16 + 16 | |
| Sequence number | 32 | number of the first data byte in the segment |
| Acknowledgement number | 32 | next byte expected (cumulative) |
| Header length | 4 | in 32-bit words (5 to 15) |
| Flags | 9 | URG, ACK, PSH, RST, SYN, FIN (and ECE, CWR, NS) |
| Window | 16 | receiver's advertised window in bytes |
| Checksum | 16 | header + data + pseudo-header |
| Urgent pointer | 16 | |
| Options | 0–40 bytes | MSS, window scale, SACK, timestamps |

### Connection establishment: the three-way handshake

1. Client → server: **SYN**, seq = x (the client's initial sequence number, ISN).
2. Server → client: **SYN + ACK**, seq = y, ack = x + 1.
3. Client → server: **ACK**, seq = x + 1, ack = y + 1.

With x = 1000 and y = 5000: SYN (seq 1000), SYN-ACK (seq 5000, ack 1001), ACK (seq 1001, ack 5001). If the client then sends 300 bytes, the segment has seq 1001 and length 300, so the next expected sequence number is 1301. The SYN consumes one sequence number. Random ISNs stop old duplicate segments of a previous connection being accepted and make blind spoofing harder. A **SYN flood** attack sends many SYNs and never completes the handshake, filling the server's half-open connection queue; defences are SYN cookies and rate limiting.

### Connection release

Each direction closes independently: **FIN** from one side, **ACK** from the other; four segments in the normal case (FIN, ACK, FIN, ACK). The side that closes first enters **TIME_WAIT** for two maximum-segment lifetimes (typically 60 seconds) so that a lost final ACK can be retransmitted and old segments die out. **RST** aborts a connection immediately.

### TCP states in brief

Client: CLOSED → SYN_SENT → ESTABLISHED → FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED. Server: CLOSED → LISTEN → SYN_RCVD → ESTABLISHED → CLOSE_WAIT → LAST_ACK → CLOSED. The command `ss -tan` lists the states of the sockets on a Linux host.

## 5.5 Flow control

The receiver advertises its free buffer space in the **window** field (**rwnd**). The sender keeps at most rwnd unacknowledged bytes in flight. If the window drops to zero, the sender stops and probes with tiny segments so that a lost window update cannot deadlock the connection. **Silly window syndrome** (tiny windows repeatedly advertised and used) is avoided by the receiver not advertising until it can take at least one MSS and the sender not sending tiny segments (**Nagle's algorithm**: while unacknowledged data exists, buffer small writes).

The 16-bit window field limits the window to 65,535 bytes without scaling. Throughput is at most window / RTT, so with a 100 ms round trip the cap is 65,535 × 8 / 0.1 = **5.24 Mbps** whatever the link speed. A 1 Gbps path with a 50 ms RTT needs a window of 10⁹ × 0.05 / 8 = **6,250,000 bytes**, which is why the **window scale** option (a shift of up to 14, window up to about 1 GB) exists.

## 5.6 Error control and timers

TCP detects damage by checksum and loss by missing acknowledgements. **Cumulative ACK**: ack = n means "everything before byte n arrived". If a segment is lost, later segments produce **duplicate ACKs** for the same n. After **three duplicate ACKs**, the sender performs **fast retransmit** of the missing segment without waiting for the timer. **SACK** adds ranges of received bytes so that several losses can be repaired in one round trip.

### Retransmission timeout

If the timer is too short, TCP sends needless duplicates; if too long, it reacts slowly. TCP measures the round-trip time and keeps a smoothed value and a deviation (Jacobson's algorithm, with α = 1/8 and β = 1/4):

- RTTVAR = (1 − β) RTTVAR + β |SRTT − R|
- SRTT = (1 − α) SRTT + α R
- RTO = SRTT + 4 RTTVAR

::: example RTO from five RTT samples
The first sample is R = 100 ms: SRTT = 100, RTTVAR = 50. The next samples are 120, 90, 140 and 100 ms.

| Sample R | RTTVAR | SRTT | RTO |
|---|---|---|---|
| 120 | 42.5 | 102.5 | 272.5 |
| 90 | 35.0 | 100.94 | 240.94 |
| 140 | 36.02 | 105.82 | 249.88 |
| 100 | 28.47 | 105.09 | 218.96 |

(all in ms; RTTVAR is updated with the old SRTT first, then SRTT). **Karn's rule**: never sample the RTT of a retransmitted segment (its ACK is ambiguous); double the RTO after each timeout (**exponential backoff**).
:::

## 5.7 Congestion control

Too many senders cause queues to overflow and packets to be dropped; retransmissions then add more load, a feedback that can lead to **congestion collapse**. TCP responds with an end-to-end scheme: the sender keeps a **congestion window** (cwnd) and sends min(cwnd, rwnd) bytes. It treats a loss as a signal of congestion.

- **Slow start**: begin with cwnd = 1 MSS and *double* cwnd every round trip (add one MSS per ACK) until it reaches the slow-start threshold **ssthresh**. It is "slow" only compared with sending a full window at once.
- **Congestion avoidance**: above ssthresh, increase cwnd by about **one MSS per round trip** (additive increase).
- **On a timeout** (severe): ssthresh = cwnd / 2, cwnd = 1 MSS, return to slow start (**Tahoe**; also Reno on a timeout).
- **On three duplicate ACKs** (milder): **Reno** sets ssthresh = cwnd / 2 and cwnd = ssthresh (fast recovery), continuing in congestion avoidance.

The combination is **AIMD**: additive increase, multiplicative decrease. Modern stacks use CUBIC (Linux) or BBR, but AIMD is the textbook model.

::: example cwnd by round (MSS units), ssthresh = 16, loss at round 8
Starting cwnd = 1. Tahoe (timeout) versus Reno (triple duplicate ACK):

| Round | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Tahoe cwnd | 1 | 2 | 4 | 8 | 16 | 17 | 18 | 19 | 1 | 2 | 4 | 8 | 9 | 10 |
| Reno cwnd | 1 | 2 | 4 | 8 | 16 | 17 | 18 | 19 | 9 | 10 | 11 | 12 | 13 | 14 |

At round 8 cwnd = 19 and a loss occurs: the new ssthresh is ⌊19 / 2⌋ = 9. Tahoe restarts at 1 and doubles 1, 2, 4, 8 until it reaches 9 (round 13); Reno resumes at 9 and grows linearly. After 14 rounds Reno has sent far more data.
:::

### Throughput and fairness

For a long-lived TCP flow, the average throughput is about **MSS / RTT × 1.22 / √p** (Mathis formula) where p is the loss probability: with MSS = 1460 bytes, RTT = 100 ms and p = 1 % that is 1460 × 8 / 0.1 × 1.22 / 0.1 ≈ 1.42 Mbps. AIMD also converges to a **fair share**: when two flows share a bottleneck, additive increase raises both rates by the same amount (keeping their gap), and each multiplicative decrease halves the gap. If the flows start with rates 10 and 60 and the link capacity is 100, the gap of 50 becomes 25 after the first loss and 12.5 after the second; repeated losses bring them to equality. UDP flows have no such control and can crowd out TCP, which is why streaming protocols add their own rate control.

## 5.8 Elements of transport protocols

- **Addressing**: a transport address is (IP, port); well-known ports let a client find a server. A *portmapper* or name service can assign ports dynamically.
- **Establishing connections**: the hard problem is delayed duplicates. The three-way handshake with fresh sequence numbers solves it.
- **Releasing**: a symmetric release is impossible to guarantee (the two-army problem), so TCP uses timers and TIME_WAIT.
- **Flow control and buffering**: buffers at the sender (for retransmission) and receiver (to reorder); a variable window tied to buffer space.
- **Multiplexing**: many transport connections over one network connection (and the reverse, *inverse* multiplexing for bandwidth).
- **Crash recovery**: after a host crash the application must decide whether the last request was done; no transport protocol can resolve this ambiguity by itself (the reason for idempotent requests).

## 5.9 Sockets in practice

A program reaches TCP and UDP through the **socket API**: a server calls socket, bind, listen and accept; a client calls socket and connect; both then send and recv. The following program starts a small TCP server in a thread and a client on the loopback interface, prints the four-tuple the way TCP sees it, then does one UDP exchange.

```python
import socket, threading
srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("127.0.0.1", 50007)); srv.listen(1)
def serve():
    conn, addr = srv.accept()
    data = conn.recv(1024); conn.sendall(b"ECHO:" + data); conn.close()
t = threading.Thread(target=serve); t.start()
c = socket.create_connection(("127.0.0.1", 50007))
print("server socket", c.getpeername(), "client uses an ephemeral port:", c.getsockname()[1] >= 32768)
c.sendall(b"hello"); print(c.recv(1024)); c.close(); t.join(); srv.close()
u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); u.bind(("127.0.0.1", 50008))
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s2.sendto(b"datagram", ("127.0.0.1", 50008))
print(u.recvfrom(100)[0])
```
```output
server socket ('127.0.0.1', 50007) client uses an ephemeral port: True
b'ECHO:hello'
b'datagram'
```
A second program reproduces the congestion-window and RTO tables of this unit.

```python
def trace(rounds, ssth, loss_at, tahoe):
    cw, rows = 1, []
    for t in range(1, rounds + 1):
        rows.append(cw)
        if t == loss_at: ssth = max(cw // 2, 2); cw = 1 if tahoe else ssth
        elif cw < ssth: cw = min(cw * 2, ssth)
        else: cw += 1
    return rows
print("Tahoe", trace(14, 16, 8, True)); print("Reno ", trace(14, 16, 8, False))
srtt, rttvar = 100, 50
for r in (120, 90, 140, 100):
    rttvar = 0.75 * rttvar + 0.25 * abs(srtt - r); srtt = 0.875 * srtt + 0.125 * r
    print(r, round(rttvar, 2), round(srtt, 2), round(srtt + 4 * rttvar, 2))
print("window/RTT cap Mbps:", round(65535 * 8 / 0.1 / 1e6, 2), " window for 1 Gbps, 50 ms:", int(1e9 * 0.05 / 8))
```
```output
Tahoe [1, 2, 4, 8, 16, 17, 18, 19, 1, 2, 4, 8, 9, 10]
Reno  [1, 2, 4, 8, 16, 17, 18, 19, 9, 10, 11, 12, 13, 14]
120 42.5 102.5 272.5
90 35.0 100.94 240.94
140 36.02 105.82 249.88
100 28.47 105.09 218.96
window/RTT cap Mbps: 5.24  window for 1 Gbps, 50 ms: 6250000
```
## 5.10 Seeing the ideas: ports, segments, windows and congestion

The transport layer is mostly about numbers that every student must be able to compute: sequence numbers, windows, timers and rates. Plate 5.1 shows three of the people behind it: Bob Kahn and Vint Cerf, who designed TCP, and Van Jacobson, whose 1988 congestion-control algorithms saved the Internet from collapse. Plate 5.2 gives three everyday pictures of the ideas: a container port (multiplexing and ports), a ticket hall (queues and waiting for service) and a mountain road jammed with trucks (congestion). The figures that follow compute the unit's examples: ports and sockets, the UDP and TCP headers, the handshake and release with real sequence numbers, window utilisation, the window cap, the retransmission timer, Tahoe and Reno, AIMD fairness and the throughput formula.

```photogrid label="5.1" cols="3" ratio="1.0" caption="Three people behind TCP. (a) Bob Kahn (CC BY-SA 3.0), who with Vint Cerf designed TCP/IP in 1974. (b) Vint Cerf (CC BY 3.0), co-author of the first TCP specification. (c) Van Jacobson (public domain), whose slow start, congestion avoidance and round-trip timer algorithms of 1988 are the basis of every modern TCP stack."
@ photo id="bca301/kahn" cap="Bob Kahn: TCP/IP"
fit 1.0
focus 0.5 0.3
@ photo id="bca301/cerf" cap="Vint Cerf: TCP/IP"
fit 1.0
focus 0.5 0.4
@ photo id="bca301/jacobson" cap="Van Jacobson: congestion control"
fit 1.0
focus 0.5 0.4
```

```photogrid label="5.2" cols="3" ratio="1.25" caption="Three pictures for three ideas. (a) A container terminal (CC BY-SA 3.0): many shipments share one port and each box carries a label saying which customer it is for, like segments from many processes sharing one IP address and told apart by port numbers. (b) A ticket hall (CC BY-SA 3.0): people arrive faster than the counters can serve, so queues form and delay rises, as in a router. (c) A trucks-in-a-jam scene on the Rohtang Pass road (CC BY-SA 4.0): when too many vehicles enter a road, everyone slows down; TCP's congestion control makes each sender back off, like drivers who leave larger gaps."
@ photo id="bca301/containers" cap="Container port: ports, multiplexing"
fit 1.25
focus 0.5 0.5
@ photo id="bca301/queue" cap="Ticket hall: queues, delay"
fit 1.25
focus 0.5 0.45
@ photo id="bca301/jam" cap="Mountain road jam: congestion"
fit 1.25
focus 0.5 0.45
```

```svgfig label="5.1" caption="Ports and sockets. A client laptop (IP 192.168.1.10) runs a browser with two tabs and a DNS lookup, so it uses three ephemeral ports (51000, 51001 and 51002). The server (IP 202.79.1.20) listens on well-known ports 80 (HTTP), 443 (HTTPS) and 53 (DNS). Each connection is identified by the four-tuple (source IP, source port, destination IP, destination port), so the two TCP flows to the same server are different connections. UDP uses only the destination pair, so the DNS reply is delivered by (destination IP, destination port) alone."
f = Fig(580, 270)
f.box(14, 22, 150, 190, "", fill="#f8fafc", stroke="#94a3b8", r=8, sw=1.3)
f.text(89, 40, "client 192.168.1.10", size=10.5, color=NAVY, bold=True)
f.box(416, 22, 150, 190, "", fill="#f8fafc", stroke="#94a3b8", r=8, sw=1.3)
f.text(491, 40, "server 202.79.1.20", size=10.5, color=NAVY, bold=True)
flows = [("browser tab 1", 51000, 80, "TCP", NAVY, BLUE), ("browser tab 2", 51001, 443, "TCP", TEAL, MINT), ("DNS lookup", 51002, 53, "UDP", AMBER, SAND)]
for i, (app, sp, dp, pr, st, fl) in enumerate(flows):
    y = 60 + i * 50
    f.box(24, y, 130, 36, "%s\nport %d" % (app, sp), fill=fl, stroke=st, size=9.5, r=4, color=NAVY)
    f.box(426, y, 130, 36, "%s: port %d\n%s" % (["HTTP", "HTTPS", "DNS"][i], dp, "web server" if i < 2 else "name server"), fill=fl, stroke=st, size=9.5, r=4, color=NAVY)
    f.arrow([(154, y + 18), (426, y + 18)], color=st, sw=2)
    f.text(290, y + 8, pr, size=10, color=st, bold=True)
f.text(290, 238, "TCP connection = four-tuple (192.168.1.10, 51000, 202.79.1.20, 80)", size=10.5, color=NAVY, bold=True)
f.text(290, 258, "UDP demultiplexes on (destination IP, destination port) only", size=10, color=SLATE)
```

```svgfig label="5.2" caption="The UDP and TCP headers to scale (11 px per bit), with example values on the right. UDP needs just 8 bytes: two ports, a length and a checksum. TCP needs at least 20: ports, a 32-bit sequence number (the number of the first data byte), a 32-bit acknowledgement number (the next byte expected), the header length, the flag bits (URG, ACK, PSH, RST, SYN, FIN), the receive window, the checksum and the urgent pointer. Options such as MSS, window scale and SACK follow, up to 40 bytes. The small header is why UDP has so little delay and overhead."
f = Fig(580, 300)
S = 11
x0 = 10
def hrow(y, items):
    x = x0
    for nm, bits, fl in items:
        f.box(x, y, bits * S - 2, 26, nm, fill=fl, stroke="#475569", size=9.5, r=2, sw=1.2, color=NAVY)
        x += bits * S
f.text(x0, 14, "UDP: 8 bytes", size=10.5, color=NAVY, bold=True, anchor="start")
hrow(22, [("Source port", 16, BLUE), ("Destination port", 16, MINT)])
hrow(52, [("Length", 16, SAND), ("Checksum", 16, "#fee2e2")])
f.text(x0, 100, "TCP: 20 bytes + options", size=10.5, color=NAVY, bold=True, anchor="start")
hrow(108, [("Source port", 16, BLUE), ("Destination port", 16, MINT)])
hrow(138, [("Sequence number", 32, "#e0e7ff")])
hrow(168, [("Acknowledgement number", 32, "#fce7f3")])
hrow(198, [("Hdr", 4, SAND), ("Flags URG..FIN", 12, "#fef9c3"), ("Window", 16, MINT)])
hrow(228, [("Checksum", 16, "#fee2e2"), ("Urgent pointer", 16, BLUE)])
f.box(x0, 258, 32 * S - 2, 26, "Options (0 to 40 bytes): MSS, window scale, SACK, timestamps", fill="#f8fafc", stroke="#94a3b8", size=9.5, r=2, sw=1, dash=True, color=SLATE)
f.text(386, 22, "UDP example (DNS query)", size=10, color=NAVY, bold=True, anchor="start")
for i, (a, b) in enumerate((("source port", "51002"), ("destination port", "53"), ("length", "38 bytes"))):
    f.text(386, 42 + i * 17, a, size=9.5, color=SLATE, anchor="start", vmid=True)
    f.text(480, 42 + i * 17, b, size=9.5, color=NAVY, bold=True, anchor="start", vmid=True)
f.text(386, 108, "TCP example (first SYN)", size=10, color=NAVY, bold=True, anchor="start")
for i, (a, b) in enumerate((("source port", "51000"), ("destination port", "80"), ("sequence", "1000 (ISN)"), ("acknowledgement", "0"), ("header length", "5 words = 20 B"), ("flags", "SYN only"), ("window", "65 535 bytes"))):
    f.text(386, 128 + i * 17, a, size=9.5, color=SLATE, anchor="start", vmid=True)
    f.text(480, 128 + i * 17, b, size=9.5, color=NAVY, bold=True, anchor="start", vmid=True)
```

```svgfig label="5.3" caption="A complete TCP life with the numbers of Section 5.4: the three-way handshake (ISNs x = 1000 for the client and y = 5000 for the server), 300 bytes of data, and the four-segment release. The SYN uses up one sequence number, so the SYN-ACK acknowledges 1001. The client's 300 bytes carry sequence 1001 to 1300, so the server acknowledges 1301, the next byte expected. Each FIN also uses one number (1301 and 5001). The side that closes first waits in TIME_WAIT for two maximum segment lifetimes so a lost final ACK can be answered."
f = Fig(580, 340)
cx, sx = 110, 470
f.box(cx - 40, 6, 80, 24, "client", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(sx - 40, 6, 80, 24, "server", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.line(cx, 30, cx, 334, color="#94a3b8", sw=1.2, dash=True)
f.line(sx, 30, sx, 334, color="#94a3b8", sw=1.2, dash=True)
msgs = [(1, "SYN  seq = 1000", RED, "SYN_SENT", "LISTEN"), (0, "SYN + ACK  seq = 5000, ack = 1001", TEAL, "", "SYN_RCVD"), (1, "ACK  seq = 1001, ack = 5001", NAVY, "ESTABLISHED", "ESTABLISHED"), (1, "data  seq = 1001, 300 bytes", NAVY, "", ""), (0, "ACK  ack = 1301", TEAL, "", ""), (1, "FIN  seq = 1301", RED, "FIN_WAIT_1", ""), (0, "ACK  ack = 1302", TEAL, "FIN_WAIT_2", "CLOSE_WAIT"), (0, "FIN  seq = 5001, ack = 1302", RED, "", "LAST_ACK"), (1, "ACK  ack = 5002", TEAL, "TIME_WAIT", "CLOSED")]
for i, (d, lab, col, cs, ss) in enumerate(msgs):
    y = 52 + i * 31
    if d: f.arrow([(cx, y), (sx, y + 14)], color=col, sw=1.8)
    else: f.arrow([(sx, y), (cx, y + 14)], color=col, sw=1.8)
    f.text(290, y - 4 if d else y - 4, lab, size=9.5, color=col, bold=True)
    if cs: f.text(cx - 8, y + 6, cs, size=9, color=NAVY, anchor="end", vmid=True) if False else f.text(cx + 8, y + 24, "", size=9)
    if cs: f.text(8, y + 8, cs, size=9.5, color=NAVY, bold=True, anchor="start", vmid=True)
    if ss: f.text(572, y + 8, ss, size=9.5, color=TEAL, bold=True, anchor="end", vmid=True)
```

```svgfig label="5.4" caption="Why TCP must pipeline, computed for a 1 Gbps path with a 30 ms round trip and 1000 byte packets. One packet takes 8000 / 10^9 = 8 microseconds to send, but stop-and-wait then waits 30 ms for the acknowledgement, so U = 8 us / (30 ms + 8 us) = 0.027 percent. With a window of W packets in flight U = W x 0.027 percent, so W = 10 gives 0.27, W = 100 gives 2.7 and W = 1000 gives 26.7 percent. The line is full only when W reaches 1 + 30 ms / 8 us = 3751 packets, about 3.75 MB of data in flight: the bandwidth-delay product of Unit 1."
f = Fig(580, 270)
cm = __import__("math")
L, T, W, H = 64, 14, 340, 200
f.box(L, T, W, H, "", fill="#ffffff", stroke="#94a3b8", r=2, sw=1.2)
Xw = lambda w: L + W * cm.log10(w) / 4.0
Yu = lambda u: T + H - H * u
for u in (0.25, 0.5, 0.75, 1.0):
    f.line(L, Yu(u), L + W, Yu(u), color="#e2e8f0", sw=1)
    f.text(L - 6, Yu(u), "%d%%" % (u * 100), size=9.5, color=SLATE, anchor="end", vmid=True)
for k in range(5):
    f.text(L + W * k / 4.0, T + H + 14, "10^%d" % k if k > 1 else str(10 ** k), size=9.5, color=SLATE)
f.text(L + W / 2, T + H + 32, "window W (packets in flight, log scale)", size=10, color=SLATE, bold=True)
U = lambda w: min(1.0, w * 8e-6 / (0.030 + 8e-6))
pts = " ".join("%.1f,%.1f" % (Xw(10 ** (k / 40.0)), Yu(U(10 ** (k / 40.0)))) for k in range(0, 161))
f.raw('<polyline points="%s" fill="none" stroke="#1e3a8a" stroke-width="2.6"/>' % pts)
for w in (1, 10, 100, 1000, 3751):
    f.circle(Xw(w), Yu(U(w)), 4.2, fill=RED, stroke=RED)
rows = [("W", "U"), ("1", "0.027 %"), ("10", "0.27 %"), ("100", "2.7 %"), ("1000", "26.7 %"), ("3751", "100 %")]
for i, r in enumerate(rows):
    for j, v in enumerate(r):
        f.text([430, 480][j], 40 + i * 22, v, size=10, color=NAVY if i == 0 else SLATE, bold=(i == 0), anchor="start")
f.text(430, 190, "W = 1 + RTT / t_f", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(430, 210, "= 1 + 30 ms / 8 us", size=10, color=SLATE, anchor="start")
f.text(430, 228, "= 3751 packets", size=10, color=RED, bold=True, anchor="start")
```

```svgfig label="5.5" caption="The receive-window cap, computed. Without window scaling the 16-bit window field limits TCP to 65 535 bytes in flight, so throughput is at most 65 535 x 8 / RTT: 52.4 Mbps at a 10 ms round trip, 10.5 Mbps at 50 ms, 5.24 Mbps at 100 ms and 2.62 Mbps at 200 ms, however fast the link is. To fill a 1 Gbps path with a 50 ms round trip the window must be 10^9 x 0.05 / 8 = 6 250 000 bytes, which is 95 times larger; the window-scale option shifts the field left by up to 14 bits (a shift of 7 gives 8.4 MB), so it makes this possible."
f = Fig(580, 260)
L, T, W, H = 56, 14, 300, 190
f.box(L, T, W, H, "", fill="#ffffff", stroke="#94a3b8", r=2, sw=1.2)
for k in range(0, 5):
    y = T + H - H * k / 4.0
    f.line(L, y, L + W, y, color="#e2e8f0", sw=1)
    f.text(L - 6, y, "%d" % (k * 15), size=9.5, color=SLATE, anchor="end", vmid=True)
for i, rtt in enumerate((10, 50, 100, 200)):
    v = 65535 * 8 / (rtt / 1000.0) / 1e6
    h = H * v / 60.0
    x = L + 14 + i * 72
    f.box(x, T + H - h, 48, h, "", fill="#bfdbfe", stroke=NAVY, r=0, sw=1.2)
    f.text(x + 24, T + H - h - 8, "%.2f" % v, size=10, color=NAVY, bold=True)
    f.text(x + 24, T + H + 14, "%d ms" % rtt, size=9.5, color=SLATE)
f.text(L + W / 2, T + H + 32, "round-trip time", size=10, color=SLATE, bold=True)
f.text(14, T + H / 2, "Mbps", size=10, color=SLATE, bold=True)
f.text(380, 40, "window 65 535 bytes", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(380, 58, "cap = window x 8 / RTT", size=10, color=SLATE, anchor="start")
f.text(380, 96, "needed for 1 Gbps, 50 ms:", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(380, 114, "10^9 x 0.05 / 8", size=10, color=SLATE, anchor="start")
f.text(380, 132, "= 6 250 000 bytes", size=10.5, color=RED, bold=True, anchor="start")
f.text(380, 150, "= 95 x the plain field", size=10, color=SLATE, anchor="start")
f.text(380, 178, "window scale shift 7:", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(380, 196, "65 535 x 128 = 8.4 MB", size=10, color=TEAL, bold=True, anchor="start")
```

```svgfig label="5.6" caption="TCP's retransmission timer follows the measured round-trip time, computed with Jacobson's rule (alpha = 1/8, beta = 1/4). The first sample, 100 ms, gives SRTT = 100 and RTTVAR = 50, so RTO = 100 + 4 x 50 = 300 ms. The next samples 120, 90, 140 and 100 ms give RTO = 272.5, 240.9, 249.9 and 219.0 ms: the timer settles at about twice the typical round trip, safely above the samples (it must not fire early) but not far above (it must not wait too long). A sample taken from a retransmitted segment is ignored (Karn's rule) and the RTO is doubled after each timeout."
f = Fig(580, 270)
L, T, W, H = 56, 14, 330, 200
f.box(L, T, W, H, "", fill="#ffffff", stroke="#94a3b8", r=2, sw=1.2)
samples = [100, 120, 90, 140, 100]
srtt, rttvar = 100.0, 50.0
rows = [(100, srtt, rttvar, srtt + 4 * rttvar)]
for r in samples[1:]:
    rttvar = 0.75 * rttvar + 0.25 * abs(srtt - r)
    srtt = 0.875 * srtt + 0.125 * r
    rows.append((r, srtt, rttvar, srtt + 4 * rttvar))
Yt = lambda v: T + H - H * (v - 50) / 270.0
for v in (100, 150, 200, 250, 300):
    f.line(L, Yt(v), L + W, Yt(v), color="#e2e8f0", sw=1)
    f.text(L - 6, Yt(v), str(v), size=9.5, color=SLATE, anchor="end", vmid=True)
Xs = lambda i: L + 30 + i * 70
for key, col, nm in ((0, RED, "sample R"), (1, NAVY, "SRTT"), (3, TEAL, "RTO")):
    pts = " ".join("%.1f,%.1f" % (Xs(i), Yt(rows[i][key])) for i in range(5))
    f.raw('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.4"/>' % (pts, col))
    for i in range(5):
        f.circle(Xs(i), Yt(rows[i][key]), 3.6, fill=col, stroke=col)
for i in range(5):
    f.text(Xs(i), T + H + 14, str(i + 1), size=9.5, color=SLATE)
    f.text(Xs(i), Yt(rows[i][3]) - 10, "%.0f" % rows[i][3], size=9.5, color=TEAL, bold=True)
f.text(L + W / 2, T + H + 32, "sample number (RTT in ms on the vertical axis)", size=10, color=SLATE, bold=True)
f.text(410, 40, "RTO = SRTT + 4 x RTTVAR", size=10.5, color=NAVY, bold=True, anchor="start")
for i, (nm, col) in enumerate((("RTO (teal)", TEAL), ("SRTT (blue)", NAVY), ("sample R (red)", RED))):
    f.text(410, 66 + i * 18, nm, size=10, color=col, bold=True, anchor="start")
f.text(410, 140, "SRTT final %.1f ms" % rows[-1][1], size=10, color=SLATE, anchor="start")
f.text(410, 158, "RTTVAR final %.1f ms" % rows[-1][2], size=10, color=SLATE, anchor="start")
f.text(410, 176, "RTO final %.1f ms" % rows[-1][3], size=10, color=TEAL, bold=True, anchor="start")
```

```svgfig label="5.7" caption="TCP Tahoe against Reno, computed with the unit's trace rules: initial ssthresh 16 MSS, loss at round 8 when cwnd = 19. Both double every round (slow start) to 16, then add 1 per round (congestion avoidance) to 19. At the loss the new ssthresh is 19 / 2 = 9. Tahoe (timeout) drops cwnd to 1 and slow-starts again, doubling to 8 and then reaching the threshold 9 at round 13. Reno (three duplicate ACKs) sets cwnd = 9 straight away (fast recovery) and grows by 1 per round. Over 14 rounds Reno sends 154 MSS and Tahoe only 119, about a quarter less."
f = Fig(580, 280)
def trace(rounds, ssth, loss_at, tahoe):
    cw, rows = 1, []
    for t in range(1, rounds + 1):
        rows.append(cw)
        if t == loss_at: ssth = max(cw // 2, 2); cw = 1 if tahoe else ssth
        elif cw < ssth: cw = min(cw * 2, ssth)
        else: cw += 1
    return rows
tah = trace(14, 16, 8, True); ren = trace(14, 16, 8, False)
L, T, W, H = 50, 14, 360, 210
f.box(L, T, W, H, "", fill="#ffffff", stroke="#94a3b8", r=2, sw=1.2)
Xr = lambda r: L + 12 + (r - 1) * (W - 24) / 13.0
Yc = lambda c: T + H - H * c / 22.0
for c in (5, 10, 15, 20):
    f.line(L, Yc(c), L + W, Yc(c), color="#e2e8f0", sw=1)
    f.text(L - 6, Yc(c), str(c), size=9.5, color=SLATE, anchor="end", vmid=True)
for r in range(1, 15):
    f.text(Xr(r), T + H + 14, str(r), size=9.5, color=SLATE)
f.text(L + W / 2, T + H + 32, "round trip number (cwnd in MSS)", size=10, color=SLATE, bold=True)
f.line(L, Yc(16), L + W, Yc(16), color=AMBER, sw=1.3, dash=True)
f.text(L + W - 4, Yc(16) - 6, "ssthresh 16", size=9.5, color=AMBER, bold=True, anchor="end")
f.line(L, Yc(9), L + W, Yc(9), color="#94a3b8", sw=1.2, dash=True)
f.text(L + 6, Yc(9) - 6, "new ssthresh 9", size=9.5, color=SLATE, anchor="start")
for ser, col in ((tah, "#b91c1c"), (ren, "#0f766e")):
    pts = " ".join("%.1f,%.1f" % (Xr(i + 1), Yc(c)) for i, c in enumerate(ser))
    f.raw('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.6"/>' % (pts, col))
    for i, c in enumerate(ser):
        f.circle(Xr(i + 1), Yc(c), 3.3, fill=col, stroke=col)
f.line(Xr(8), T, Xr(8), T + H, color=NAVY, sw=1.2, dash=True)
f.text(Xr(8) - 6, T + 14, "loss", size=10, color=NAVY, bold=True, anchor="end")
f.text(430, 50, "Tahoe (timeout)", size=10.5, color=RED, bold=True, anchor="start")
f.text(430, 68, "total %d MSS" % sum(tah), size=10, color=SLATE, anchor="start")
f.text(430, 100, "Reno (3 dup ACKs)", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(430, 118, "total %d MSS" % sum(ren), size=10, color=SLATE, anchor="start")
f.text(430, 150, "AIMD: add 1 per round,", size=10, color=NAVY, anchor="start")
f.text(430, 166, "halve on loss", size=10, color=NAVY, anchor="start")
```

```svgfig label="5.8" caption="Why AIMD is fair, simulated. Two flows share a link of capacity 100 (x + y = 100, the efficiency line); the diagonal is the fairness line x = y. Starting from the unfair point (10, 60), each round both add 1 (a step along a 45 degree line, which keeps the gap), and when x + y exceeds 100 both halve (a move toward the origin that halves the gap too). The path zig-zags toward the point (50, 50) on both lines. The gap of 50 is halved at every decrease, so after 5 decreases it is 1.6: the flows converge without any central control."
f = Fig(580, 300)
L, T, S = 56, 14, 250
f.box(L, T, S, S, "", fill="#ffffff", stroke="#94a3b8", r=2, sw=1.2)
Xp = lambda v: L + S * v / 100.0
Yp = lambda v: T + S - S * v / 100.0
f.line(Xp(0), Yp(100), Xp(100), Yp(0), color=RED, sw=2, dash=True)
f.line(Xp(0), Yp(0), Xp(100), Yp(100), color=TEAL, sw=2, dash=True)
x, y = 10.0, 60.0
pts = [(x, y)]
dec = 0
for k in range(200):
    if x + y > 100:
        x *= 0.5; y *= 0.5; dec += 1
    else:
        x += 1; y += 1
    pts.append((x, y))
f.raw('<polyline points="%s" fill="none" stroke="#1e3a8a" stroke-width="1.8"/>' % " ".join("%.1f,%.1f" % (Xp(a), Yp(b)) for a, b in pts))
f.circle(Xp(10), Yp(60), 4.5, fill=RED, stroke=RED)
f.text(Xp(10) + 8, Yp(60) - 4, "start (10, 60)", size=10, color=RED, bold=True, anchor="start")
f.circle(Xp(50), Yp(50), 4.5, fill=TEAL, stroke=TEAL)
for v in (0, 25, 50, 75, 100):
    f.text(L + S * v / 100.0, T + S + 14, str(v), size=9.5, color=SLATE)
    f.text(L - 6, Yp(v), str(v), size=9.5, color=SLATE, anchor="end", vmid=True)
f.text(L + S / 2, T + S + 30, "rate of flow 1 (x)", size=10, color=SLATE, bold=True)
f.text(16, T + S / 2, "y", size=11, color=SLATE, bold=True)
f.text(340, 50, "red dashed: x + y = 100", size=10, color=RED, bold=True, anchor="start")
f.text(340, 70, "link is full (efficiency)", size=10, color=SLATE, anchor="start")
f.text(340, 100, "teal dashed: x = y", size=10, color=TEAL, bold=True, anchor="start")
f.text(340, 120, "equal shares (fairness)", size=10, color=SLATE, anchor="start")
f.text(340, 154, "gap |x - y| = 50 at the start", size=10, color=NAVY, bold=True, anchor="start")
f.text(340, 174, "halved by every decrease:", size=10, color=SLATE, anchor="start")
f.text(340, 192, "50, 25, 12.5, 6.3, 3.1, 1.6", size=10, color=NAVY, bold=True, anchor="start")
f.text(340, 226, "decreases in 200 rounds: %d" % dec, size=10, color=SLATE, anchor="start")
```

```svgfig label="5.9" caption="TCP throughput against packet loss, from the Mathis formula throughput = (MSS / RTT) x 1.22 / sqrt(p), computed for MSS = 1460 bytes and RTT = 100 ms. Loss of 10 percent gives 0.45 Mbps, 1 percent 1.42 Mbps, 0.1 percent 4.50 Mbps and 0.01 percent 14.2 Mbps: every tenfold cut in loss gives 3.16 times the speed. This is why a slightly lossy link, such as a weak Wi-Fi or mobile signal, feels much slower than its raw rate, and why a long round-trip time hurts: doubling RTT halves the throughput."
f = Fig(580, 260)
cm = __import__("math")
L, T, W, H = 66, 14, 330, 190
f.box(L, T, W, H, "", fill="#ffffff", stroke="#94a3b8", r=2, sw=1.2)
Yl = lambda v: T + H - H * (cm.log10(v) + 1) / 3.0
for v, lab in ((0.1, "0.1"), (1, "1"), (10, "10"), (100, "100")):
    f.line(L, Yl(v), L + W, Yl(v), color="#e2e8f0", sw=1)
    f.text(L - 6, Yl(v), lab, size=9.5, color=SLATE, anchor="end", vmid=True)
f.text(14, T + H / 2, "Mbps", size=10, color=SLATE, bold=True)
for i, p in enumerate((0.1, 0.01, 0.001, 0.0001)):
    v = 1460 * 8 / 0.1 * 1.22 / cm.sqrt(p) / 1e6
    x = L + 14 + i * 78
    f.box(x, Yl(v), 52, T + H - Yl(v), "", fill="#fde68a", stroke=AMBER, r=0, sw=1.2)
    f.text(x + 26, Yl(v) - 8, "%.2f" % v, size=10, color=NAVY, bold=True)
    f.text(x + 26, T + H + 14, "%s%%" % ("%g" % (p * 100)), size=9.5, color=SLATE)
f.text(L + W / 2, T + H + 32, "packet loss probability p", size=10, color=SLATE, bold=True)
f.text(414, 50, "MSS = 1460 B, RTT = 100 ms", size=10, color=NAVY, bold=True, anchor="start")
f.text(414, 76, "S = 1460 x 8 / 0.1 x 1.22 / sqrt(p)", size=10, color=SLATE, anchor="start")
f.text(414, 108, "10 x less loss", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(414, 126, "= 3.16 x the speed", size=10.5, color=RED, bold=True, anchor="start")
f.text(414, 158, "2 x the RTT = half the speed", size=10, color=SLATE, anchor="start")
```

### 5.10.1 Eight uses of transport protocols in Nepal

1. **Secure web browsing and payments.** When you open ConnectIPS or a bank site, your browser makes a TCP connection to port 443 with the three-way handshake (Fig. 5.3) and then runs TLS inside it. TCP numbers every byte and retransmits lost segments, so a payment instruction cannot arrive damaged or out of order. The same reliability is why a failed payment shows an error instead of a half-finished transfer.
2. **DNS lookups over UDP.** Every web address is first turned into an IP address by a short UDP query to port 53, with an 8-byte header and no connection set-up (Fig. 5.2). One packet out and one packet back is far faster than a handshake. If the answer is lost the resolver simply asks again, which is cheaper than TCP for such small messages.
3. **Video calls and streaming.** Calls on Viber, WhatsApp and Zoom and live streams run over UDP, because a late packet is useless and retransmitting it would only add delay. The application hides small losses with its own correction. This is why a call may break up for a moment but never freezes while waiting for old data.
4. **Large downloads over long paths.** A software update or a video from an overseas server travels over a path with a long round-trip time. Without the window-scale option the speed would be capped at a few megabits per second (Fig. 5.5), so modern operating systems enable scaling automatically. Choosing a nearby mirror lowers the round trip and raises the speed.
5. **Sharing a mobile or Wi-Fi link.** When many students in a hostel use the same link, packets are dropped at the router queue and every TCP flow halves its window (Fig. 5.7). AIMD makes the flows share the capacity about equally without any central control (Fig. 5.8). A slow link is therefore shared rather than monopolised by one download.
6. **Loss on weak signals.** On a weak mobile signal a small loss rate lowers throughput sharply (Fig. 5.9), which is why the speed test falls far below the advertised rate. Moving to a better signal helps more than buying a faster plan. The Mathis formula shows that the cure is lower loss or a shorter round trip.
7. **Firewalls and SYN floods.** A server's firewall allows only the ports it needs, such as 80 and 443, and drops the rest (Fig. 5.1). A SYN flood sends many SYN segments and never finishes the handshake, filling the table of half-open connections. Limits on half-open connections and SYN cookies protect public portals during result days.
8. **Socket programming in student projects.** A client-server chat or a small web service written in Python or Java uses sockets: bind, listen and accept on the server, connect on the client. The program sees a reliable byte stream and never handles sequence numbers itself. Writing one in the lab makes the ports, the four-tuple and the handshake concrete.

## Formula and fact sheet

- UDP header 8 bytes; TCP header 20–60 bytes; MSS = MTU − 40 = 1460 on Ethernet.
- Handshake: SYN (x), SYN-ACK (y, x + 1), ACK (x + 1, y + 1). SYN and FIN each use one sequence number.
- Throughput ≤ window / RTT. Window needed = bandwidth × RTT.
- RTO = SRTT + 4 RTTVAR; α = 1/8, β = 1/4. Karn: skip retransmitted samples.
- cwnd: slow start doubling, then +1 MSS per RTT; on loss ssthresh = cwnd / 2; Tahoe cwnd = 1, Reno cwnd = ssthresh.
- Mathis: rate ≈ 1.22 MSS / (RTT √p).

## Chapter summary

- The transport layer gives process-to-process delivery with ports. UDP is a thin, fast, unreliable service; TCP is a reliable byte stream.
- TCP sets up with a three-way handshake, numbers bytes, acknowledges cumulatively, retransmits on timeout or three duplicate ACKs and tears down with FINs.
- Flow control uses the receiver's window; congestion control uses cwnd with slow start, additive increase and multiplicative decrease.
- Throughput is bounded by window / RTT, which is why high-speed long-delay paths need window scaling.

## Practice

1. Differentiate TCP and UDP and give two applications of each.
2. Describe the three-way handshake with ISNs 1000 and 5000. What is the next sequence number after 300 bytes of data?
3. Why can a web server on port 80 serve many clients at once?
4. What is the maximum throughput of a TCP connection with a 65,535-byte window and 100 ms RTT? What window does 1 Gbps with 50 ms need?
5. Explain fast retransmit.
6. Compute the RTO after samples 120, 90, 140 and 100 ms if the first sample was 100 ms.
7. Draw the Tahoe and Reno cwnd for 14 rounds with ssthresh 16 and a loss in round 8.
8. State Karn's rule and why it is needed.
9. Distinguish flow control from congestion control.
10. Why is the UDP checksum computed over a pseudo-header?
11. What is a SYN flood and one defence?

::: note Answers and worked solutions
**1.** TCP: connection-oriented, reliable, ordered, flow and congestion controlled (web, e-mail, file transfer). UDP: connectionless, best effort, 8-byte header (DNS, streaming, VoIP).
**2.** SYN (seq 1000); SYN-ACK (seq 5000, ack 1001); ACK (seq 1001, ack 5001). After 300 data bytes starting at 1001, the next sequence number is 1301.
**3.** TCP demultiplexes by the four-tuple, so each client's (IP, port) pair gives a different connection to the same server port.
**4.** 65,535 × 8 / 0.1 = 5.24 Mbps. For 1 Gbps and 50 ms: 6,250,000 bytes (window scaling needed).
**5.** After three duplicate ACKs for the same sequence number the sender assumes that segment was lost and resends it immediately without waiting for the timeout.
**6.** Final RTO = 218.96 ms (table in Section 5.6).
**7.** Tahoe 1 2 4 8 16 17 18 19 1 2 4 8 9 10; Reno 1 2 4 8 16 17 18 19 9 10 11 12 13 14.
**8.** Do not take RTT samples from retransmitted segments, because it is unclear which transmission the ACK acknowledges; use exponential backoff for the timer instead.
**9.** Flow control keeps a fast sender from overflowing a slow receiver (rwnd); congestion control keeps senders from overloading the network (cwnd).
**10.** It lets the receiver verify that the datagram was meant for its IP address and protocol, catching misdelivery by IP.
**11.** The attacker sends SYNs without finishing the handshake, filling the half-open queue. SYN cookies let the server avoid storing state until the final ACK arrives.
:::

## Model answers for Unit 5

**Q1. Explain TCP connection establishment and release with the sequence numbers. (10 marks)**

**Introduction.** TCP is a connection-oriented, reliable, full-duplex byte-stream protocol. Before data flows the two ends must agree on their initial sequence numbers, and when the exchange finishes each direction is closed separately. Fig. 5.3 shows the whole life of a connection.

**Three-way handshake.** The client first sends a SYN segment, the server answers with SYN + ACK, and the client confirms with an ACK. With the client's initial sequence number x = 1000 and the server's y = 5000:

| Step | Direction | Flags | Seq | Ack |
|---|---|---|---|---|
| 1 | client to server | SYN | 1000 | none |
| 2 | server to client | SYN + ACK | 5000 | 1001 |
| 3 | client to server | ACK | 1001 | 5001 |

The SYN consumes one sequence number, which is why the acknowledgements are x + 1 and y + 1. If the client now sends 300 bytes they carry sequence numbers 1001 to 1300, so the server acknowledges 1301, the next byte expected.

**Why three steps and random numbers.** The handshake proves that both ends can send and receive, and a random initial sequence number prevents an old duplicate segment from a previous connection being accepted as new data. A **SYN flood** attack sends many SYNs and never completes step 3; servers defend with SYN cookies and limits on half-open connections.

**Release.** Each direction closes by itself, so four segments are normal: the client sends FIN (seq 1301), the server acknowledges (ack 1302), then the server sends its own FIN (seq 5001) and the client acknowledges (ack 5002). The side that closes first enters **TIME_WAIT** for twice the maximum segment lifetime (about 60 seconds), so that a lost last ACK can be re-sent and old segments disappear. A RST segment aborts a connection at once.

**States.** The client goes CLOSED, SYN_SENT, ESTABLISHED, FIN_WAIT_1, FIN_WAIT_2, TIME_WAIT, CLOSED. The server goes CLOSED, LISTEN, SYN_RCVD, ESTABLISHED, CLOSE_WAIT, LAST_ACK, CLOSED.

**Example for the exam.** If the client sends 300 bytes at sequence 1001, the segment ends at byte 1300 and the ACK carries 1301; if the first segment is lost, the server keeps acknowledging 1001, and after three such duplicate ACKs the client retransmits at once. TCP states can be listed with the command ss -tan on Linux.

**Conclusion.** The handshake and the release give TCP a clean beginning and end, at the cost of one round trip before any data and a short waiting period at the close.

**Q2. Explain TCP congestion control. Compare Tahoe and Reno using a cwnd trace. (10 marks)**

**Introduction.** Flow control protects the receiver, but congestion control protects the network. When too many senders fill a router's queues, packets are dropped, and retransmissions can make matters worse, which is **congestion collapse**. TCP therefore keeps a congestion window **cwnd** and sends min(cwnd, rwnd) bytes.

**The algorithms.**

1. **Slow start.** cwnd begins at 1 MSS and doubles every round trip (one MSS added per ACK) until it reaches the threshold ssthresh.
2. **Congestion avoidance.** Above ssthresh, cwnd grows by about one MSS per round trip, which is additive increase.
3. **Timeout.** A timeout means severe congestion: ssthresh = cwnd / 2 and cwnd = 1, then slow start again (Tahoe, and Reno on a timeout).
4. **Three duplicate ACKs.** They mean one segment was lost but later ones arrived, so the network is only mildly congested. Reno performs fast retransmit, sets ssthresh = cwnd / 2 and cwnd = ssthresh (**fast recovery**) and continues in congestion avoidance.
5. **AIMD.** The pattern, additive increase and multiplicative decrease, makes flows converge to a fair share (Fig. 5.8).

**Trace (Fig. 5.7).** ssthresh = 16 and a loss at round 8, when cwnd = 19:

| Round | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Tahoe | 1 | 2 | 4 | 8 | 16 | 17 | 18 | 19 | 1 | 2 | 4 | 8 | 9 | 10 |
| Reno | 1 | 2 | 4 | 8 | 16 | 17 | 18 | 19 | 9 | 10 | 11 | 12 | 13 | 14 |

The new ssthresh is 19 / 2 = 9. Tahoe falls to 1 and needs four more rounds to climb back, while Reno continues from 9. Over 14 rounds Reno sends 154 MSS against 119 for Tahoe.

**Throughput and fairness.** Averaged over time, a flow with loss probability p, round trip RTT and segment size MSS gets about MSS / RTT x 1.22 / sqrt(p): with 1460 bytes, 100 ms and 1 percent loss this is 1.42 Mbps (Fig. 5.9). Modern stacks replace the exact rules by CUBIC (Linux, Windows) or BBR, which estimates the bottleneck rate, but all of them keep the idea of probing gently and backing off on loss.

**Conclusion.** Slow start probes for capacity quickly, congestion avoidance probes gently, and the halving on loss backs off sharply. Reno's fast recovery wastes less capacity than Tahoe because duplicate ACKs show that the pipe is still flowing.

**Q3. Compare UDP and TCP. When is each suitable? (10 marks)**

**Introduction.** Both protocols deliver data to a process using port numbers, but they make opposite choices about reliability and overhead (Fig. 5.2).

**UDP.** The User Datagram Protocol is connectionless and message-oriented. Its header is 8 bytes: source port, destination port, length and checksum. It sets up no connection, retransmits nothing, does not order the datagrams and does not slow down when the network is congested. Its checksum covers the header, the data and a pseudo-header with the IP addresses, so a datagram delivered to the wrong host is detected.

**TCP.** The Transmission Control Protocol is connection-oriented and byte-stream based. Its header is at least 20 bytes. It numbers every byte, acknowledges data, retransmits losses, reorders segments, controls the flow with the receive window and controls congestion with cwnd.

| Feature | UDP | TCP |
|---|---|---|
| Connection | none | handshake before data |
| Header | 8 bytes | 20 to 60 bytes |
| Reliability | none | acknowledgements, retransmission |
| Ordering | none | sequence numbers |
| Flow and congestion control | none | window and cwnd |
| Delay | low | higher (handshake, waiting) |
| Unit of data | message with boundaries | stream of bytes |
| Typical use | DNS, DHCP, calls, games, QUIC | web, e-mail, file transfer, banking |

**Choosing.** Use TCP when every byte must arrive correctly and in order, as in web pages, e-mail, file transfers and payments. Use UDP when speed matters more than perfection or when the message is tiny: a DNS query, a live video frame, or a game position that is out of date as soon as a newer one arrives. UDP is also the base for new protocols such as QUIC, which build their own reliability and congestion control above it.

**Overhead example.** A DNS query of 30 bytes in UDP costs one datagram out and one back, 2 packets in all. The same exchange over TCP needs a three-segment handshake, the request, the reply, and four release segments, about 10 packets, and at least one extra round trip before the first byte is sent. For a tiny, repeatable request that is a heavy price, which is why DNS, DHCP and SNMP choose UDP.

**Conclusion.** TCP gives a reliable pipe at the price of delay and overhead, and UDP gives the application raw speed and control. Neither is better; the application decides.

**Q4. Explain TCP flow control and the window-scale option. (5 marks)**

**Flow control** stops a fast sender from overrunning a slow receiver. The receiver puts its free buffer space in the **window** field of every acknowledgement (rwnd), and the sender keeps no more than rwnd unacknowledged bytes in flight.

1. **Zero window.** If the window becomes 0 the sender stops and sends small probe segments, so that a lost window update cannot cause a deadlock.
2. **Silly window syndrome.** Tiny windows repeatedly advertised and filled with tiny segments waste capacity; the receiver waits until it can accept one MSS, and the sender uses Nagle's rule to gather small writes.
3. **The 64 KB limit.** The window field has 16 bits, so at most 65 535 bytes can be in flight. Throughput is then at most window x 8 / RTT: 5.24 Mbps at a round trip of 100 ms (Fig. 5.5), however fast the link.
4. **Window scale.** A link of 1 Gbps with RTT 50 ms needs a window of 10^9 x 0.05 / 8 = 6 250 000 bytes. The window-scale option, agreed in the SYN, shifts the field left by up to 14 bits, allowing windows near 1 GB.
5. **Difference.** Flow control protects the receiver, while congestion control protects the network, and the sender obeys the smaller of rwnd and cwnd.

**Q5. How does TCP set its retransmission timeout? Compute the RTO for the samples 100, 120, 90, 140 and 100 ms. (5 marks)**

If the timeout is too short TCP sends needless duplicates, and if too long it reacts slowly to loss, so TCP measures the round trip and adapts. **Jacobson's algorithm** keeps a smoothed RTT and a deviation:

- RTTVAR = 0.75 x RTTVAR + 0.25 x |SRTT - R|
- SRTT = 0.875 x SRTT + 0.125 x R
- RTO = SRTT + 4 x RTTVAR

The first sample, 100 ms, gives SRTT = 100, RTTVAR = 50 and RTO = 300 ms. The later samples give (Fig. 5.6):

| Sample R | RTTVAR | SRTT | RTO |
|---|---|---|---|
| 120 | 42.5 | 102.5 | 272.5 |
| 90 | 35.0 | 100.94 | 240.94 |
| 140 | 36.02 | 105.82 | 249.88 |
| 100 | 28.47 | 105.09 | 218.96 |

The timer therefore settles near twice the typical round trip, safely above the samples but not far above them. **Karn's rule:** never take a sample from a retransmitted segment, because its acknowledgement could belong to either copy, and double the RTO after each timeout (exponential backoff). Fast retransmit after three duplicate ACKs avoids waiting for the timer at all.

**Q6. Explain the principles of reliable data transfer using the rdt versions. (5 marks)**

Reliable transfer over an unreliable channel is built one problem at a time.

1. **rdt 1.0.** The channel is perfect, so the sender simply sends.
2. **rdt 2.0.** Bits may be damaged, so a checksum is added, the receiver sends ACK or NAK, and the sender retransmits on a NAK.
3. **rdt 2.1 and 2.2.** The ACK or NAK itself may be damaged, so frames carry a sequence number (0 or 1) to detect duplicates; 2.2 replaces the NAK by a duplicate ACK.
4. **rdt 3.0.** Packets may also be lost, so a countdown timer is added: if no ACK arrives in time the sender retransmits. This is stop-and-wait or the alternating-bit protocol.
5. **Pipelining.** Stop-and-wait is correct but slow (0.027 percent utilisation on a 1 Gbps path with a 30 ms round trip, Fig. 5.4), so Go-Back-N or Selective Repeat allows many packets in flight. TCP uses a hybrid: cumulative acknowledgements like Go-Back-N and buffering of out-of-order segments like Selective Repeat.

**Q7. Explain why AIMD makes competing TCP flows converge to a fair share. (5 marks)**

Two TCP flows share a bottleneck link of capacity C. Plot flow 1's rate on the x axis and flow 2's on the y axis (Fig. 5.8): the line x + y = C is full use of the link (efficiency) and the line x = y is equal sharing (fairness).

1. **Additive increase.** When there is no loss both flows add the same amount per round trip, so the point moves along a 45 degree line: the difference between the rates stays the same while the total rises.
2. **Multiplicative decrease.** When the total exceeds C, both flows halve their windows. The point moves toward the origin along the line to the origin, and the difference between the rates is halved too.
3. **Convergence.** Each cycle of increase and decrease leaves the efficiency near C but halves the unfairness. From a gap of 50 the gap becomes 25, 12.5, 6.3, 3.1 and 1.6 after five decreases.
4. **Why not additive decrease.** If both subtracted the same amount, the gap would never shrink, and the flows would not converge to fairness.
5. **Limits.** The fairness holds for flows with similar round-trip times; a flow with a shorter round trip gets a larger share, and applications opening many connections take more than their share.

**Q8. What are ports and sockets? How do multiplexing and demultiplexing work? (5 marks)**

The transport layer delivers data to a **process**, not just to a machine, using 16-bit **port numbers** (0 to 65 535).

1. **Port ranges.** Well-known ports 0 to 1023 name standard services (80 HTTP, 443 HTTPS, 53 DNS, 25 SMTP, 22 SSH, 67 and 68 DHCP). Registered ports go up to 49 151, and the rest are ephemeral ports that a client picks for itself.
2. **Socket.** A socket address is an IP address plus a port, such as 202.79.1.20:443. A program uses the socket API: a server calls socket, bind, listen and accept, a client calls socket and connect, and both send and receive.
3. **Multiplexing.** At the sender, data from several processes is put into segments marked with source and destination ports and handed to IP (Fig. 5.1).
4. **Demultiplexing.** At the receiver, the port numbers deliver each segment to the right socket. UDP uses only the destination IP and port; TCP uses the whole four-tuple (source IP, source port, destination IP, destination port), so two connections to the same server port are different.
5. **Example.** A browser with two tabs uses ports 51000 and 51001 to reach the same server port 443, and the server tells the two connections apart by the client port.
