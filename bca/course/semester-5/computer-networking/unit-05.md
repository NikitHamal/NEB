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
