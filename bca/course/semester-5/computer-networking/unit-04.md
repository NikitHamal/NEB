---
subject: Computer Networking
grade: BCA Semester 5
unit: 4
title: The Network Layer: Addressing and Routing
hours: 10
area: BCA 301 · Computer Networking · Unit 4
---

The network layer is what turns a collection of LANs into an internet. Its two jobs are **forwarding** (moving a packet from an input port of a router to the right output port, in nanoseconds) and **routing** (working out, by algorithm, which output port is right for each destination). The first needs an addressing scheme that can be summarised; the second needs an algorithm that every router can run on partial information. This unit does the arithmetic of IPv4 subnetting (checked with Python's `ipaddress` module), then runs Dijkstra and Bellman–Ford on one network and compares the results.

::: key What this unit gives you
- Network layer services, datagram versus virtual-circuit service, router architecture.
- IPv4 header, classful and classless addressing, subnetting, VLSM, supernetting, fragmentation.
- ARP, ICMP, DHCP and NAT; IPv6 addressing and transition.
- Routing algorithms: link state (Dijkstra) and distance vector (Bellman–Ford), count-to-infinity, RIP, OSPF, BGP.
:::

## 4.1 Network layer services

The network layer carries a **packet** from source host to destination host across many links. It provides logical addressing, routing, fragmentation and (in the Internet) a **best-effort**, connectionless service: no guarantee of delivery, order or delay. Reliability is left to TCP at the edges (the *end-to-end argument*). A **datagram network** (IP) forwards every packet independently by its destination address; a **virtual-circuit network** (ATM, MPLS) sets up a path first and forwards by a short label.

**Router architecture.** A router has input ports (receive, look up the destination in the **forwarding table**), a **switching fabric** (memory, bus or crossbar) and output ports (queue, schedule, transmit). Queues form when packets arrive faster than they can leave; when buffers fill, packets are dropped. The **control plane** (routing protocols) builds the table; the **data plane** forwards.

## 4.2 The IPv4 datagram

| Field | Bits | Purpose |
|---|---|---|
| Version | 4 | 4 |
| IHL | 4 | header length in 32-bit words (5 = 20 bytes) |
| DSCP/ECN | 8 | priority, congestion notification |
| Total length | 16 | header + data in bytes, at most 65,535 |
| Identification | 16 | which datagram a fragment belongs to |
| Flags | 3 | DF (don't fragment), MF (more fragments) |
| Fragment offset | 13 | position of data in units of 8 bytes |
| TTL | 8 | hop limit, decremented at each router; at 0 the packet is discarded |
| Protocol | 8 | 6 = TCP, 17 = UDP, 1 = ICMP |
| Header checksum | 16 | over the header only (Unit 3) |
| Source / destination address | 32 + 32 | |
| Options | 0–40 bytes | rarely used |

### Fragmentation

Each link has a **maximum transmission unit** (MTU); Ethernet's is 1500 bytes. If a datagram is larger than the outgoing MTU, a router splits it into fragments, each with its own header, the same identification and the MF flag set on all but the last. Offsets are in 8-byte units, so every fragment's data except the last is a multiple of 8 bytes.

::: example A 4020-byte datagram over a 1500-byte MTU
The datagram has a 20-byte header and 4000 bytes of data. Each fragment may carry 1500 − 20 = 1480 bytes of data (1480 is divisible by 8).

| Fragment | Total length | Data | Offset field | MF |
|---|---|---|---|---|
| 1 | 1500 | 1480 | 0 | 1 |
| 2 | 1500 | 1480 | 185 (= 1480 / 8) | 1 |
| 3 | 1060 | 1040 | 370 | 0 |

Only the destination reassembles; if one fragment is lost the entire datagram is lost, so modern hosts use *path MTU discovery* (DF set, ICMP "fragmentation needed" returns) instead of fragmenting.
:::

## 4.3 IPv4 addressing

An IPv4 address has 32 bits written as four decimal bytes (dotted decimal), for example 192.168.10.77. There are 2³² = 4,294,967,296 addresses. An address has a **network part** (prefix) and a **host part**; every interface of a host or router has its own address.

### Classful addressing (historic)

| Class | First bits | First byte | Default mask | Hosts per network |
|---|---|---|---|---|
| A | 0 | 1–126 | /8 | 16,777,214 |
| B | 10 | 128–191 | /16 | 65,534 |
| C | 110 | 192–223 | /24 | 254 |
| D | 1110 | 224–239 | — | multicast |
| E | 1111 | 240–255 | — | reserved |

Classful addressing wasted space (a company needing 300 hosts took a class B with 65,534), so it was replaced in 1993 by **CIDR**.

### Special and private addresses

- **Private** (RFC 1918, not routed on the Internet): 10.0.0.0/8, 172.16.0.0/12 (172.16–172.31), 192.168.0.0/16.
- **Loopback** 127.0.0.0/8 (127.0.0.1 is "this host"); **link-local** 169.254.0.0/16 (self-assigned when DHCP fails); **this network** 0.0.0.0; **limited broadcast** 255.255.255.255; **shared address space** 100.64.0.0/10 (carrier-grade NAT).
- Within any subnet the all-zeros host part is the **network address** and the all-ones host part is the **directed broadcast address**; neither can be given to a host.

### CIDR notation

**Classless Inter-Domain Routing** writes an address with a prefix length: a.b.c.d/n means the first n bits are the network part. The mask is n ones followed by 32 − n zeros. A /n block has 2^(32−n) addresses and 2^(32−n) − 2 usable hosts.

| Prefix | Mask | Addresses | Usable hosts |
|---|---|---|---|
| /24 | 255.255.255.0 | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 126 |
| /26 | 255.255.255.192 | 64 | 62 |
| /27 | 255.255.255.224 | 32 | 30 |
| /28 | 255.255.255.240 | 16 | 14 |
| /29 | 255.255.255.248 | 8 | 6 |
| /30 | 255.255.255.252 | 4 | 2 |

### Finding network, broadcast and range

Method: write the mask, AND it with the address to get the network address; set all host bits to 1 for the broadcast address; usable hosts lie in between. A shortcut: find the *interesting octet*, compute the **block size** = 256 − mask value in that octet, and the network address is the nearest multiple of the block size not above the address.

| Address | Network | Mask | Broadcast | First–last host | Hosts |
|---|---|---|---|---|---|
| 192.168.10.77/26 | 192.168.10.64 | 255.255.255.192 | 192.168.10.127 | 192.168.10.65 – 192.168.10.126 | 62 |
| 172.16.5.130/20 | 172.16.0.0 | 255.255.240.0 | 172.16.15.255 | 172.16.0.1 – 172.16.15.254 | 4094 |
| 10.1.2.3/8 | 10.0.0.0 | 255.0.0.0 | 10.255.255.255 | 10.0.0.1 – 10.255.255.254 | 16,777,214 |
| 200.10.20.0/30 | 200.10.20.0 | 255.255.255.252 | 200.10.20.3 | 200.10.20.1 – 200.10.20.2 | 2 |

For 192.168.10.77/26 the block size is 256 − 192 = 64; 77 lies in the block starting at 64, so the network is 192.168.10.64 and the broadcast is 64 + 63 = 127. For 172.16.5.130/20 the interesting octet is the third: mask 240, block size 16; 5 lies in the block starting at 0, so the network is 172.16.0.0 and the broadcast is 172.16.15.255.

## 4.4 Subnetting, VLSM and supernetting

**Subnetting** borrows bits from the host part to create several smaller networks, so one block can serve several LANs. To get N equal subnets borrow ⌈log₂ N⌉ bits.

::: example Six subnets from 192.168.1.0/24
Six subnets need ⌈log₂ 6⌉ = 3 bits, so the new prefix is /27 and there are 8 subnets (two spare) with 2⁵ − 2 = 30 hosts each: 192.168.1.0, .32, .64, .96, .128, .160, .192 and .224 (all /27). Subnet 3 (index 2) is 192.168.1.64/27: hosts .65–.94, broadcast .95.
:::

**Variable-length subnet masks (VLSM)** give each LAN a block of the right size. Procedure: sort requirements from largest to smallest; for each, find the smallest block with at least hosts + 2 addresses; allocate blocks one after another from the start of the address space, keeping each aligned to its own size.

::: example VLSM for four LANs in 10.0.0.0/24
Requirements: Sales 100 hosts, Engineering 50, Admin 25, and a router-to-router WAN link with 2.

| LAN | Hosts needed | Block | Usable hosts | Range | Broadcast |
|---|---|---|---|---|---|
| Sales | 100 | 10.0.0.0/25 | 126 | 10.0.0.1 – 10.0.0.126 | 10.0.0.127 |
| Engineering | 50 | 10.0.0.128/26 | 62 | 10.0.0.129 – 10.0.0.190 | 10.0.0.191 |
| Admin | 25 | 10.0.0.192/27 | 30 | 10.0.0.193 – 10.0.0.222 | 10.0.0.223 |
| WAN link | 2 | 10.0.0.224/30 | 2 | 10.0.0.225 – 10.0.0.226 | 10.0.0.227 |

Used: 128 + 64 + 32 + 4 = 228 of 256 addresses; 10.0.0.228 – 10.0.0.255 stays free for growth. If a naive equal split had been used, a /25 for each of the four LANs would have needed 512 addresses.
:::

**Supernetting (route aggregation)** does the reverse: combine contiguous blocks into one shorter prefix so that a router needs a single table entry. The four /24 networks 192.168.0.0 to 192.168.3.0 aggregate to **192.168.0.0/22** (they must be contiguous, a power-of-two count, and the first must be aligned on the block boundary). ISPs aggregate customer blocks, which keeps the Internet's global routing table manageable.

### Longest-prefix match

When several table entries match a destination, the router uses the one with the **longest prefix**. With the table 0.0.0.0/0 → default, 10.0.0.0/8 → R1, 10.1.0.0/16 → R2 and 10.1.2.0/24 → R3: destination 10.1.2.9 matches /8, /16 and /24 and goes to R3; 10.1.9.9 matches /8 and /16 and goes to R2; 10.9.9.9 goes to R1; 8.8.8.8 matches only the default route.

## 4.5 Supporting protocols

### ARP and RARP

ARP maps an IP address on the local network to a MAC address (Unit 3). To reach a host outside its subnet, a host ARPs for the **default gateway's** MAC and sends the frame there with the destination IP of the far host. At each router the frame's MAC addresses change but the packet's IP addresses stay the same.

### ICMP

**ICMP** carries errors and diagnostics inside IP packets (protocol number 1). Common types: echo request/reply (8/0, the basis of `ping`), destination unreachable (3), time exceeded (11) and redirect (5). **ping** measures round-trip time; **traceroute** sends probes with TTL = 1, 2, 3, … and records the "time exceeded" replies of successive routers to list the path.

### DHCP

A new host has no address, so **DHCP** (UDP ports 67 server, 68 client) gives it one through four messages: **Discover** (broadcast from 0.0.0.0 to 255.255.255.255), **Offer** (server proposes an address, mask, gateway, DNS, lease time), **Request** (client accepts one offer) and **Ack**. The address is *leased* for a time and renewed halfway through. In a home network the Wi-Fi router is the DHCP server and usually hands out 192.168.1.x or 192.168.0.x addresses.

### NAT

**Network address translation** lets many hosts with private addresses share one public address. The NAT router keeps a table mapping (private IP, private port) to (public IP, public port).

| Direction | Source before → after | Table entry |
|---|---|---|
| Outbound | 192.168.1.10:51000 → 202.79.1.5:40001 | created |
| Outbound | 192.168.1.11:51000 → 202.79.1.5:40002 | created (a different public port for the second host) |
| Inbound reply to :40001 | destination → 192.168.1.10:51000 | looked up |

NAT conserved IPv4 addresses but breaks end-to-end addressing: servers behind NAT need **port forwarding**, and peer-to-peer apps need traversal tricks (STUN, relays). Many mobile networks use **carrier-grade NAT** with the 100.64.0.0/10 range.

## 4.6 IPv6

IPv4's 2³² addresses ran out (IANA's last block was assigned in 2011; APNIC's pool in 2011). **IPv6** has 128-bit addresses: 2¹²⁸ ≈ 3.403 × 10³⁸ of them. Written as eight groups of four hex digits; leading zeros in a group may be dropped and **one** run of all-zero groups may be replaced by "::". For example, 2001:0db8:0000:0000:0000:ff00:0042:8329 compresses to **2001:db8::ff00:42:8329**.

| Type | Prefix | Note |
|---|---|---|
| Global unicast | 2000::/3 | routable on the Internet |
| Link-local | fe80::/10 | automatic on every interface, never routed |
| Unique local | fc00::/7 | the private equivalent |
| Multicast | ff00::/8 | replaces broadcast |
| Loopback | ::1/128 | |

An end site normally gets a /48 (65,536 subnets of /64, since 2^(64−48) = 65,536) and every LAN is a /64. A host can build its own interface identifier by **EUI-64**: take the MAC 00:1A:2B:3C:4D:5E, insert FF:FE in the middle (00:1A:2B:FF:FE:3C:4D:5E) and flip the universal/local bit (the second-lowest bit of the first byte) to get 021A:2BFF:FE3C:4D5E, so the link-local address is fe80::21a:2bff:fe3c:4d5e. (Privacy extensions use random identifiers instead.)

**Header.** The IPv6 header is a fixed 40 bytes: version, traffic class, flow label, payload length, next header, hop limit, source and destination. There is no header checksum, no fragmentation by routers (only the source may fragment, using an extension header) and options live in extension headers. **Autoconfiguration** (SLAAC) uses router advertisements; **Neighbor Discovery** (ICMPv6) replaces ARP. **Transition** from IPv4: **dual stack** (both protocols), **tunnelling** (IPv6 packets inside IPv4), **translation** (NAT64/DNS64).

## 4.7 Routing: concepts

A **routing algorithm** fills the forwarding tables. Criteria: correctness, simplicity, robustness, stability, fairness and optimality (the cost can be hops, delay, bandwidth or money). Algorithms are **static** (non-adaptive, manual, for small stub networks and default routes) or **dynamic** (adaptive: they react to topology changes). The two classic dynamic families are **link-state** (every router learns the whole map and computes shortest paths) and **distance-vector** (every router tells its neighbours its table).

The example network used below has six routers; the link costs are A–B 2, A–C 5, A–D 1, B–C 3, B–D 2, C–D 3, C–E 1, C–F 5, D–E 1, E–F 2.

### 4.7.1 Link-state routing and Dijkstra

Each router measures the cost to neighbours, floods a **link-state packet** to all routers, assembles the same map, and runs **Dijkstra's shortest-path algorithm** to build a tree rooted at itself: keep a set of finalised nodes; repeatedly finalise the unfinalised node with the least tentative distance and relax its neighbours (if d(u) + w(u,v) < d(v) update d(v) and the predecessor).

::: example Dijkstra from router A
| Finalised | A | B | C | D | E | F | Action |
|---|---|---|---|---|---|---|---|
| start | 0 | ∞ | ∞ | ∞ | ∞ | ∞ | |
| A | 0 | 2 (A) | 5 (A) | 1 (A) | ∞ | ∞ | relax A's neighbours |
| D (1) | 0 | 2 (A) | 4 (D) | 1 | 2 (D) | ∞ | via D: C 1 + 3 = 4 < 5; E = 2; B 1 + 2 = 3 is not < 2 |
| B (2) | 0 | 2 | 4 (D) | 1 | 2 (D) | ∞ | via B: C 2 + 3 = 5, no change |
| E (2) | 0 | 2 | 3 (E) | 1 | 2 | 4 (E) | via E: C 2 + 1 = 3 < 4; F 2 + 2 = 4 |
| C (3) | 0 | 2 | 3 | 1 | 2 | 4 (E) | via C: F 3 + 5 = 8, no change |
| F (4) | 0 | 2 | 3 | 1 | 2 | 4 | done |

Order of finalisation: A, D, B, E, C, F. The shortest path to F is **A → D → E → F** (cost 4); to C it is A → D → E → C (cost 3). A's forwarding table (next hop): B via B; C, D, E and F all via D.
:::

OSPF is the Internet's main link-state protocol: it floods link-state advertisements, uses cost = reference bandwidth / interface bandwidth (cost 10 for 10 Mbps, 1 for 100 Mbps and for 1 Gbps with the default 100 Mbps reference, which is why the reference is usually raised), divides a network into **areas** joined at a backbone area 0, and elects a **designated router** on multi-access LANs. Convergence is fast, but memory and CPU grow with the map.

### 4.7.2 Distance-vector routing and Bellman–Ford

Each router keeps a vector of its best-known cost to every destination and periodically sends it to neighbours. On receiving neighbour v's vector, router u computes **d_u(t) = min over neighbours v of [ c(u,v) + d_v(t) ]** (the **Bellman–Ford equation**). It is simple, needs no map, and is *distributed*: it uses only local knowledge and neighbour information.

::: example Router A's vector over time
| Round | to B | to C | to D | to E | to F |
|---|---|---|---|---|---|
| 0 (neighbours only) | 2 | 5 | 1 | ∞ | ∞ |
| 1 | 2 | 4 | 1 | 2 | 10 |
| 2 | 2 | 3 | 1 | 2 | 4 |
| 3 | 2 | 3 | 1 | 2 | 4 (no change: converged) |

In round 1 A learns about E through D (1 + 1 = 2), but F only through C's first-round value 5 (5 + 5 = 10); in round 2 E's own vector contains F = 2, giving 2 + 2 = 4. The converged costs equal Dijkstra's (0, 2, 3, 1, 2, 4), as they must.
:::

### Count to infinity

Distance vector reacts quickly to **good news** (a shorter path spreads one hop per round) but slowly to **bad news**. On a line A – B – C with every link cost 1, B reaches C at cost 1 and A at cost 2. When the link B–C breaks, B looks for another route and hears from A that A can reach C at cost 2, so B sets its cost to 3 via A; then A, whose route goes via B, updates to 4; B to 5; A to 6, and so on: 3, 4, 5, … until the "infinity" value (16 in RIP) is reached, after 14 exchanges in this example. Fixes: define a small infinity (16 for RIP), **split horizon** (never advertise a route back to the neighbour it was learned from), **poison reverse** (advertise it back with cost infinity) and **triggered updates**. Split horizon fixes the two-router loop but not all loops.

### 4.7.3 RIP, OSPF and BGP

| Protocol | Type | Metric | Scope | Facts |
|---|---|---|---|---|
| RIP v1/v2 | distance vector | hop count, max 15, 16 = unreachable | small networks | updates every 30 s over UDP port 520; v2 carries masks and multicast |
| OSPF | link state | cost | inside one autonomous system (interior) | areas, designated router, fast convergence |
| BGP-4 | path vector | policy; shortest AS-path among other attributes | between autonomous systems (exterior) | runs over TCP port 179; routes carry the list of ASes they cross, which prevents loops |

An **autonomous system** (AS) is a network under one administration with a common routing policy, identified by an AS number. The Internet uses **intra-AS** protocols (OSPF, IS-IS, RIP) and **inter-AS** BGP. Hierarchical routing keeps tables small and lets each organisation hide its internal structure.

### Other routing ideas

**Broadcast routing** uses flooding, reverse-path forwarding or a spanning tree (a tree over n nodes has n − 1 links: 5 for the six routers above). **Multicast** (IGMP between host and router; PIM between routers) sends one copy to many group members along a tree. **Mobile IP** keeps a mobile node reachable using a home agent and a care-of address.

### Congestion at the network layer

If routers receive more than they can forward, queues grow and delay rises sharply as utilisation approaches 100 %; at full buffers packets are dropped. Responses: **admission control**, **traffic shaping** (leaky bucket: output at a fixed rate, bucket overflow is discarded; token bucket: allows bursts up to the bucket size), **choke packets**, **load shedding**, and **active queue management** such as RED, which drops packets randomly before the queue is full to signal senders early. TCP reacts to the drops (Unit 5).

## Practising the commands

The first program is a subnet calculator built on Python's standard `ipaddress` module; it reproduces the tables of this unit.

```python
import ipaddress, math
for c in ["192.168.10.77/26", "172.16.5.130/20", "10.1.2.3/8", "200.10.20.0/30"]:
    n = ipaddress.ip_network(c, strict=False); h = list(n.hosts())
    print(c, n.network_address, n.netmask, n.broadcast_address, h[0], h[-1], n.num_addresses - 2)
print([str(s) for s in ipaddress.ip_network("192.168.1.0/24").subnets(new_prefix=27)])
def vlsm(base, reqs):
    cur = int(ipaddress.ip_network(base).network_address)
    for name, hosts in sorted(reqs, key=lambda x: -x[1]):
        bits = math.ceil(math.log2(hosts + 2)); sn = ipaddress.ip_network((cur, 32 - bits))
        h = list(sn.hosts()); print(name, sn, len(h), h[0], h[-1], sn.broadcast_address); cur += 2 ** bits
vlsm("10.0.0.0/24", [("Sales", 100), ("Eng", 50), ("Admin", 25), ("WAN", 2)])
print(list(ipaddress.collapse_addresses([ipaddress.ip_network("192.168.%d.0/24" % i) for i in range(4)])))
table = [("0.0.0.0/0", "default"), ("10.0.0.0/8", "R1"), ("10.1.0.0/16", "R2"), ("10.1.2.0/24", "R3")]
for ip in ["10.1.2.9", "10.1.9.9", "10.9.9.9", "8.8.8.8"]:
    a = ipaddress.ip_address(ip)
    best = max((ipaddress.ip_network(p) for p, _ in table if a in ipaddress.ip_network(p)), key=lambda n: n.prefixlen)
    print(ip, "->", best, dict(table)[str(best)])
a6 = ipaddress.ip_address("2001:0db8:0000:0000:0000:ff00:0042:8329"); print(a6.compressed)
```
```output
192.168.10.77/26 192.168.10.64 255.255.255.192 192.168.10.127 192.168.10.65 192.168.10.126 62
172.16.5.130/20 172.16.0.0 255.255.240.0 172.16.15.255 172.16.0.1 172.16.15.254 4094
10.1.2.3/8 10.0.0.0 255.0.0.0 10.255.255.255 10.0.0.1 10.255.255.254 16777214
200.10.20.0/30 200.10.20.0 255.255.255.252 200.10.20.3 200.10.20.1 200.10.20.2 2
['192.168.1.0/27', '192.168.1.32/27', '192.168.1.64/27', '192.168.1.96/27', '192.168.1.128/27', '192.168.1.160/27', '192.168.1.192/27', '192.168.1.224/27']
Sales 10.0.0.0/25 126 10.0.0.1 10.0.0.126 10.0.0.127
Eng 10.0.0.128/26 62 10.0.0.129 10.0.0.190 10.0.0.191
Admin 10.0.0.192/27 30 10.0.0.193 10.0.0.222 10.0.0.223
WAN 10.0.0.224/30 2 10.0.0.225 10.0.0.226 10.0.0.227
[IPv4Network('192.168.0.0/22')]
10.1.2.9 -> 10.1.2.0/24 R3
10.1.9.9 -> 10.1.0.0/16 R2
10.9.9.9 -> 10.0.0.0/8 R1
8.8.8.8 -> 0.0.0.0/0 default
2001:db8::ff00:42:8329
```
The second program runs Dijkstra and a distance-vector computation on the six-router network, and reproduces the fragmentation table.

```python
import heapq, math
G = {"A": {"B": 2, "C": 5, "D": 1}, "B": {"A": 2, "C": 3, "D": 2}, "C": {"A": 5, "B": 3, "D": 3, "E": 1, "F": 5},
     "D": {"A": 1, "B": 2, "C": 3, "E": 1}, "E": {"C": 1, "D": 1, "F": 2}, "F": {"C": 5, "E": 2}}
def dijkstra(G, s):
    dist = {v: math.inf for v in G}; prev = {}; dist[s] = 0; done = []; pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in done: continue
        done.append(u)
        for v, w in G[u].items():
            if d + w < dist[v]: dist[v] = d + w; prev[v] = u; heapq.heappush(pq, (d + w, v))
    return dist, prev, done
dist, prev, order = dijkstra(G, "A"); print(dist); print("order", order)
p = ["F"]
while p[-1] in prev: p.append(prev[p[-1]])
print("path to F", p[::-1])
D = {u: {v: (0 if u == v else math.inf) for v in G} for u in G}
for u in G:
    for v, w in G[u].items(): D[u][v] = w
for rnd in range(1, 5):
    new = {u: dict(D[u]) for u in G}; changed = False
    for u in G:
        for t in G:
            if u != t:
                best = min(G[u][v] + D[v][t] for v in G[u])
                if best < new[u][t]: new[u][t] = best; changed = True
    D = new; print("round", rnd, D["A"])
    if not changed: break
def frag(total, mtu, hdr=20):
    payload = total - hdr; per = (mtu - hdr) // 8 * 8; res = []; off = 0
    while payload > 0:
        sz = min(per, payload); payload -= sz; res.append((sz + hdr, off // 8, 0 if payload == 0 else 1)); off += sz
    return res
print(frag(4020, 1500))
```
```output
{'A': 0, 'B': 2, 'C': 3, 'D': 1, 'E': 2, 'F': 4}
order ['A', 'D', 'B', 'E', 'C', 'F']
path to F ['A', 'D', 'E', 'F']
round 1 {'A': 0, 'B': 2, 'C': 4, 'D': 1, 'E': 2, 'F': 10}
round 2 {'A': 0, 'B': 2, 'C': 3, 'D': 1, 'E': 2, 'F': 4}
round 3 {'A': 0, 'B': 2, 'C': 3, 'D': 1, 'E': 2, 'F': 4}
[(1500, 0, 1), (1500, 185, 1), (1060, 370, 0)]
```
## 4.8 Seeing the ideas: addresses, routes and the boxes that follow them

The network layer is mostly arithmetic on 32-bit numbers and graphs, but it was built by people and runs on real boxes. Plate 4.1 shows three of them: Jon Postel, the editor of the early Internet standards, Vint Cerf, a co-designer of TCP/IP, and Edsger Dijkstra, whose shortest-path algorithm every link-state router runs. Plate 4.2 shows routers, from a small branch box to a core chassis, and Plate 4.3 shows where packets leave a country: the cable landing station, the satellite dish and the fibre. The figures that follow compute the unit's examples from the real rules: the header of a real packet, fragmentation, subnet masks, VLSM, longest-prefix match, IPv6 addresses, NAT, DHCP, traceroute, Dijkstra, distance-vector, queueing delay, BGP paths and route aggregation.

```photogrid label="4.1" cols="3" ratio="1.0" caption="Three people behind the network layer. (a) Jon Postel in his office (CC BY 2.0): editor of the RFC series, author of RFC 791 (the IP specification) and keeper of the address registry that became IANA. (b) Vint Cerf (CC BY 3.0): with Bob Kahn he designed TCP/IP, the protocols that turned separate networks into one Internet in 1983. (c) Edsger Dijkstra lecturing (CC BY-SA 4.0): his 1956 shortest-path algorithm is the heart of OSPF and IS-IS."
@ photo id="bca301/postel" cap="Jon Postel: RFC 791, IANA"
fit 1.0
focus 0.62 0.5
@ photo id="bca301/cerf" cap="Vint Cerf: TCP/IP"
fit 1.0
focus 0.5 0.4
@ photo id="bca301/dijkstra" cap="Edsger Dijkstra: shortest paths"
fit 1.0
focus 0.35 0.45
```

```photogrid label="4.2" cols="3" ratio="1.25" caption="Routers large and small. (a) A core network chassis of the kind found in an ISP equipment room (CC BY 2.0): line cards for the input and output ports, and a switching fabric inside. (b) A Juniper SRX210 branch router and firewall (CC BY-SA 3.0): eight Ethernet ports and the forwarding table of a small office. (c) A router seen in Unit 1 (public domain, bca101): the same two jobs, forwarding by table lookup and routing by protocols, at every size."
@ photo id="bca301/netcore" cap="Core network chassis"
fit 1.25
focus 0.5 0.5
@ photo id="bca301/srx" cap="Branch router (SRX210)"
fit 1.25
focus 0.5 0.5
call 0.62 0.1 0.62 0.45 "Ethernet ports"
@ photo id="bca101/router" cap="Router (layer 3)"
fit 1.25
focus 0.5 0.5
```

```photogrid label="4.3" cols="3" ratio="1.25" caption="Where an IP packet leaves the country. (a) A cable landing station of an undersea fibre system (CC0): the building where the seabed cable comes ashore. (b) A satellite earth station dish (CC BY-SA 4.0, bca301): the other route out for the hills and for backup. (c) A bundle of optical fibre cable (bca101): every long-distance route of the Internet is a pair of strands like these. A country with no coast, such as Nepal, reaches the sea cables through its neighbours."
@ photo id="bca301/landing" cap="Cable landing station"
fit 1.25
focus 0.5 0.5
@ photo id="bca301/dish" cap="Satellite earth station"
fit 1.25
focus 0.5 0.5
@ photo id="bca101/fibre-cable" cap="Optical fibre cable"
fit 1.25
focus 0.5 0.5
```

```svgfig label="4.1" caption="The IPv4 header to scale (11 px per bit), with the values of a real header: the one whose checksum 0xB861 was computed in Figure 3.3. Version 4 and IHL 5 (5 words = 20 bytes) share the first byte 0x45; the total length 0x0073 is 115 bytes; the flags 010 mean DF (do not fragment) and the offset is 0; TTL 0x40 = 64 hops; protocol 0x11 = 17 is UDP; the source is 192.168.0.1 and the destination 192.168.0.199. Options are absent, so the header is the minimum 20 bytes."
f = Fig(580, 270)
S = 11
x0 = 14
rows = [[("Ver", 4, BLUE), ("IHL", 4, BLUE), ("DSCP / ECN", 8, SAND), ("Total length", 16, MINT)],
        [("Identification", 16, MINT), ("Flags", 3, SAND), ("Fragment offset", 13, BLUE)],
        [("TTL", 8, SAND), ("Protocol", 8, BLUE), ("Header checksum", 16, MINT)],
        [("Source address", 32, "#e0e7ff")],
        [("Destination address", 32, "#fce7f3")]]
for r, row in enumerate(rows):
    x = x0
    y = 30 + r * 34
    for nm, bits, fl in row:
        f.box(x, y, bits * S - 2, 28, nm, fill=fl, stroke="#475569", size=9.5, r=2, sw=1.2, color=NAVY)
        x += bits * S
f.box(x0, 30 + 5 * 34, 32 * S - 2, 28, "Options (0 to 40 bytes), absent here", fill="#f8fafc", stroke="#94a3b8", size=9.5, r=2, sw=1, dash=True, color=SLATE)
for b in (0, 8, 16, 24, 31):
    f.text(x0 + b * S + (5 if b < 31 else 5), 18, str(b), size=9.5, color=SLATE)
f.text(x0, 12, "", size=9)
vals = [("version", "4"), ("IHL", "5 words = 20 bytes"), ("total length", "0x0073 = 115 bytes"), ("identification", "0"), ("flags / offset", "DF = 1, offset 0"), ("TTL", "64"), ("protocol", "17 = UDP"), ("checksum", "0xB861"), ("source", "192.168.0.1"), ("destination", "192.168.0.199")]
f.text(386, 14, "this header", size=10.5, color=NAVY, bold=True, anchor="start")
for i, (a, b) in enumerate(vals):
    f.text(386, 36 + i * 20, a, size=10, color=SLATE, anchor="start", vmid=True)
    f.text(468, 36 + i * 20, b, size=10, color=NAVY, bold=True, anchor="start", vmid=True)
f.text(14, 258, "hex bytes: 45 00 00 73  00 00 40 00  40 11 B8 61  C0 A8 00 01  C0 A8 00 C7", size=10, color=NAVY, anchor="start")
```

```svgfig label="4.2" caption="Fragmenting a 4020 byte datagram (20 byte header + 4000 bytes of data) for a link with MTU 1500, computed. Each fragment may carry at most 1500 - 20 = 1480 data bytes, which is a multiple of 8 as the offset field requires, so the pieces carry 1480, 1480 and 1040 bytes. The offset field counts 8 byte units: 0, 185 and 370. All three have the same identification; the MF flag is 1 on the first two and 0 on the last. Three headers now travel instead of one (60 bytes of overhead instead of 20); the destination alone reassembles, and if any fragment is lost the whole datagram is lost. Bar widths are to scale (0.1 px per byte), headers drawn at 7 px."
f = Fig(580, 270)
sc = 0.1
f.text(8, 16, "original datagram: 4020 bytes", size=10.5, color=NAVY, bold=True, anchor="start")
f.box(14, 24, 7, 26, "", fill=SAND, stroke=AMBER, r=1, sw=1)
f.box(21, 24, 4000 * sc, 26, "data 4000 bytes", fill=BLUE, stroke=NAVY, size=10, r=1, color=NAVY)
data, mtu, hdr, off = 4000, 1500, 20, 0
y = 78
rows = []
while data > 0:
    n = min(data, mtu - hdr); n -= (n % 8) if data > n else 0
    n = min(data, (mtu - hdr) // 8 * 8)
    rows.append((off // 8, n, hdr + n, 1 if data > n else 0))
    data -= n; off += n
tx = 14
f.text(8, 66, "three fragments on the link", size=10.5, color=NAVY, bold=True, anchor="start")
for i, (o, n, tl, mf) in enumerate(rows):
    f.box(tx, y + i * 34, 7, 26, "", fill=SAND, stroke=AMBER, r=1, sw=1)
    f.box(tx + 7, y + i * 34, n * sc, 26, "F%d  data %d" % (i + 1, n), fill=[BLUE, MINT, "#e0e7ff"][i], stroke=[NAVY, TEAL, "#4f46e5"][i], size=10, r=1, color=NAVY)
    tx2 = 14
    f.text(tx + 7 + n * sc + 8, y + i * 34 + 13, "offset %d, MF = %d, total length %d" % (o, mf, tl), size=10, color=SLATE, anchor="start", vmid=True)
f.text(14, 196, "offset = byte position / 8: 0, 1480 / 8 = 185, 2960 / 8 = 370", size=10, color=NAVY, bold=True, anchor="start")
f.text(14, 216, "overhead: 3 x 20 = 60 bytes of headers instead of 20", size=10, color=RED, bold=True, anchor="start")
f.text(14, 236, "a fragment lost = the whole datagram lost; hosts prefer path MTU discovery (DF flag)", size=10, color=SLATE, anchor="start")
f.text(14, 256, "only the destination reassembles; routers never do", size=10, color=SLATE, anchor="start")
```

```svgfig label="4.3" caption="Network, broadcast and host range found with bits, computed with the address 192.168.10.77/26. The mask has 26 ones then 6 zeros. ANDing the address with the mask keeps the 26 network bits (blue) and clears the 6 host bits (amber): the network address is 192.168.10.64. Setting all host bits to 1 gives the broadcast address 192.168.10.127. There are 2^6 = 64 addresses in the block and 62 usable hosts, 192.168.10.65 to 192.168.10.126. The block size 256 - 192 = 64 is the shortcut: 77 lies in the block that starts at 64."
f = Fig(580, 260)
ip = __import__("ipaddress")
ifc = ip.ip_interface("192.168.10.77/26")
a = int(ifc.ip); m = int(ifc.network.netmask); n = a & m; b = n | (~m & 0xFFFFFFFF)
def bits(v): return format(v, "032b")
rows = [("address", "192.168.10.77", a), ("mask /26", "255.255.255.192", m), ("network (AND)", str(ip.ip_address(n)), n), ("broadcast", str(ip.ip_address(b)), b)]
for r, (nm, dec, v) in enumerate(rows):
    y = 36 + r * 38
    f.text(6, y + 8, nm, size=10, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(6, y + 22, dec, size=9.5, color=SLATE, anchor="start", vmid=True)
    s = bits(v)
    for i, ch in enumerate(s):
        net = i < 26
        x = 126 + i * 13 + (i // 8) * 6
        f.box(x, y, 12, 26, ch, fill=BLUE if net else SAND, stroke=NAVY if net else AMBER, size=10, r=2, sw=1, color=NAVY if net else "#92400e")
f.text(126 + 13 * 13 + 12, 20, "26 network bits", size=10, color=NAVY, bold=True)
f.line(126, 26, 126 + 25 * 13 + 3 * 6 + 12, 26, color=NAVY, sw=1.6)
f.text(126 + 26 * 13 + 3 * 6 + 36, 20, "6 host bits", size=10, color="#92400e", bold=True, anchor="start")
f.text(126, 206, "block size = 256 - 192 = 64;   64 addresses;   62 usable hosts (not .64 and not .127)", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(126, 226, "first host 192.168.10.65, last host 192.168.10.126", size=10, color=SLATE, anchor="start")
f.text(126, 244, "77 = 64 + 13: the host part of this address is 13", size=10, color=SLATE, anchor="start")
```

```svgfig label="4.4" caption="VLSM against an equal split for four LANs in 10.0.0.0/24 (256 addresses), computed. Sorted largest first, Sales (100 hosts) takes a /25 (128 addresses, from 0), Engineering (50) a /26 (64, from 128), Admin (25) a /27 (32, from 192) and the router link (2) a /30 (4, from 224); 228 addresses are used and 28 stay free (10.0.0.228 to 10.0.0.255). An equal split would give every LAN a /25 because the largest needs one, which is 4 x 128 = 512 addresses and cannot fit in the /24 at all. Every block starts at a multiple of its own size, the alignment rule of CIDR."
f = Fig(580, 296)
sc = 0.9
x0 = 24
f.text(x0, 16, "VLSM: 10.0.0.0/24 (256 addresses)", size=10.5, color=NAVY, bold=True, anchor="start")
blocks = [("Sales /25", 0, 128, BLUE, NAVY), ("Eng /26", 128, 64, MINT, TEAL), ("", 192, 32, SAND, AMBER), ("", 224, 4, "#fee2e2", RED), ("", 228, 28, "#f1f5f9", "#94a3b8")]
for nm, s, n, fl, st in blocks:
    f.box(x0 + s * sc, 26, n * sc - 1, 34, nm, fill=fl, stroke=st, size=10, r=1, color=st if st != "#94a3b8" else SLATE)
for i, (nm, fl, st) in enumerate((("Admin /27: 32 addresses", SAND, AMBER), ("WAN /30: 4 addresses", "#fee2e2", RED), ("free: 28 addresses", "#f1f5f9", "#94a3b8"))):
    f.box(280, 24 + i * 22, 14, 14, "", fill=fl, stroke=st, r=2, sw=1.2)
    f.text(302, 31 + i * 22, nm, size=10, color=NAVY, anchor="start", vmid=True)
f.text(x0, 150, "Equal split: four /25 blocks = 512 addresses", size=10.5, color=NAVY, bold=True, anchor="start")
for i in range(4):
    over = i >= 2
    f.box(x0 + i * 128 * sc, 160, 128 * sc - 1, 34, ["Sales", "Eng", "Admin", "WAN"][i], fill="#fecaca" if over else BLUE, stroke=RED if over else NAVY, size=10, r=1, color=RED if over else NAVY)
f.line(x0 + 256 * sc, 150, x0 + 256 * sc, 204, color=NAVY, sw=1.8, dash=True)
f.text(x0 + 256 * sc + 6, 206, "end of the /24 (256)", size=10, color=NAVY, bold=True, anchor="start")
f.text(x0 + 3 * 128 * sc + 20, 212, "do not fit", size=10, color=RED, bold=True)
rows = [("LAN", "block", "hosts", "range"), ("Sales", "10.0.0.0/25", "126", "10.0.0.1 - .126"), ("Engineering", "10.0.0.128/26", "62", "10.0.0.129 - .190"), ("Admin", "10.0.0.192/27", "30", "10.0.0.193 - .222"), ("WAN link", "10.0.0.224/30", "2", "10.0.0.225 - .226")]
for i, r in enumerate(rows):
    for j, v in enumerate(r):
        f.text([24, 120, 240, 290][j], 232 + i * 11 + (0 if i else -2) if False else 224 + i * 13.5, v, size=9.5, color=NAVY if i == 0 else SLATE, bold=(i == 0), anchor="start", vmid=True)
```

```svgfig label="4.5" caption="Longest-prefix match, computed with the ipaddress module. Rows are the four routes of the table, columns are four destinations; a dot means the route matches (the destination lies inside the prefix) and the green dot is the longest matching prefix, which wins. 10.1.2.9 matches the /8, /16 and /24, so it goes to R3; 10.1.9.9 matches the /8 and /16 and goes to R2; 10.9.9.9 matches only the /8 and goes to R1; 8.8.8.8 matches only the default route 0.0.0.0/0. A more specific route always overrides a general one, which is how a customer can announce a /24 inside its provider's /16."
f = Fig(580, 270)
ip = __import__("ipaddress")
routes = [("0.0.0.0/0", "default"), ("10.0.0.0/8", "R1"), ("10.1.0.0/16", "R2"), ("10.1.2.0/24", "R3")]
dests = ["10.1.2.9", "10.1.9.9", "10.9.9.9", "8.8.8.8"]
f.text(6, 28, "route  (prefix to next hop)", size=10, color=NAVY, bold=True, anchor="start")
for j, d in enumerate(dests):
    f.text(228 + j * 82, 28, d, size=10, color=NAVY, bold=True)
winners = []
for j, d in enumerate(dests):
    ms = [i for i, (p, nh) in enumerate(routes) if ip.ip_address(d) in ip.ip_network(p)]
    winners.append(max(ms, key=lambda i: ip.ip_network(routes[i][0]).prefixlen))
for i, (p, nh) in enumerate(routes):
    y = 44 + i * 38
    f.box(4, y, 574, 32, "", fill="#f8fafc" if i % 2 else "#ffffff", stroke="#e2e8f0", r=0, sw=1)
    f.text(10, y + 16, "%s  to  %s" % (p, nh), size=10.5, color=SLATE, anchor="start", vmid=True)
    for j, d in enumerate(dests):
        if ip.ip_address(d) in ip.ip_network(p):
            win = winners[j] == i
            f.circle(228 + j * 82, y + 16, 9 if win else 6, fill="#16a34a" if win else "#94a3b8", stroke="#15803d" if win else "#64748b")
f.text(6, 214, "goes to:", size=10.5, color=NAVY, bold=True, anchor="start")
for j in range(4):
    f.text(228 + j * 82, 214, routes[winners[j]][1] + " (/%d)" % ip.ip_network(routes[winners[j]][0]).prefixlen, size=10.5, color="#15803d", bold=True)
f.text(290, 246, "green dot = longest prefix wins;  grey dot = matches but is less specific", size=10, color=SLATE)
```

```svgfig label="4.6" caption="Building an IPv6 link-local address from a MAC address (EUI-64), step by step. The MAC 00:1A:2B:3C:4D:5E is split in the middle and FF:FE is inserted, which makes 64 bits; then the universal/local bit (the second-lowest bit of the first byte) is flipped, so 00 becomes 02. With the prefix fe80::/10 the result is fe80::21a:2bff:fe3c:4d5e. Below, the long form 2001:0db8:0000:0000:0000:ff00:0042:8329 is compressed by dropping leading zeros and replacing the one longest run of zero groups by a double colon: 2001:db8::ff00:42:8329."
f = Fig(580, 280)
ip = __import__("ipaddress")
mac = ["00", "1A", "2B", "3C", "4D", "5E"]
def boxrow(y, items, hl=(), lab=""):
    f.text(6, y + 14, lab, size=10, color=NAVY, bold=True, anchor="start", vmid=True)
    for i, v in enumerate(items):
        h = i in hl
        f.box(130 + i * 52, y, 48, 28, v, fill="#fee2e2" if h else BLUE, stroke=RED if h else NAVY, size=11, bold=True, r=3, color=RED if h else NAVY)
boxrow(24, mac, (), "1. MAC address")
eui = mac[:3] + ["FF", "FE"] + mac[3:]
boxrow(78, eui, (3, 4), "2. insert FF FE")
flip = list(eui); flip[0] = "%02X" % (int(eui[0], 16) ^ 2)
boxrow(132, flip, (0,), "3. flip bit 7")
f.text(130, 174, "first byte 00 -> 02 (universal/local bit flipped)", size=10, color=RED, bold=True, anchor="start", vmid=True)
addr = ip.ip_address("fe80::" + ":".join(flip[i] + flip[i + 1] for i in (0, 2, 4, 6)))
f.text(6, 196, "result:  " + addr.compressed, size=11, color=TEAL, bold=True, anchor="start")
long = "2001:0db8:0000:0000:0000:ff00:0042:8329"
f.text(6, 226, "long:       " + long, size=10.5, color=SLATE, anchor="start")
f.text(6, 246, "short:      " + ip.ip_address(long).compressed, size=10.5, color=NAVY, bold=True, anchor="start")
f.text(6, 268, "2^128 = 3.4 x 10^38 addresses; a site gets a /48 = 65 536 subnets of /64", size=10, color=SLATE, anchor="start")
```

```svgfig label="4.7" caption="Network address translation for two hosts that use the same source port. Host 192.168.1.10 and host 192.168.1.11 both send from port 51000 to the same server. The NAT router rewrites the source of each outgoing packet to its one public address 202.79.1.5 and gives each flow a different public port (40001 and 40002), recording the pair in its table. A reply addressed to 202.79.1.5:40002 is looked up and sent back to 192.168.1.11:51000. A packet that nobody inside asked for has no table entry and is dropped, a side effect that works like a simple firewall but also blocks servers behind NAT unless a port is forwarded."
f = Fig(580, 280)
f.box(10, 30, 118, 40, "192.168.1.10", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(10, 100, 118, 40, "192.168.1.11", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(220, 52, 120, 70, "NAT router\npublic 202.79.1.5", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(440, 66, 130, 40, "server 93.184.216.34", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.arrow([(128, 50), (220, 70)], color=NAVY, sw=1.6)
f.arrow([(128, 120), (220, 104)], color=NAVY, sw=1.6)
f.arrow([(340, 87), (440, 87)], color=RED, sw=1.8, both=True)
f.text(174, 38, "src :51000", size=9.5, color=NAVY, bold=True)
f.text(174, 128, "src :51000", size=9.5, color=NAVY, bold=True)
f.text(390, 76, "src 202.79.1.5", size=9.5, color=RED, bold=True)
f.text(390, 104, ":40001 and :40002", size=9.5, color=RED, bold=True)
f.text(10, 176, "NAT table", size=10.5, color=NAVY, bold=True, anchor="start")
rows = [("inside (private)", "outside (public)", "direction"), ("192.168.1.10:51000", "202.79.1.5:40001", "outbound, created"), ("192.168.1.11:51000", "202.79.1.5:40002", "outbound, created"), ("reply to :40002", "192.168.1.11:51000", "inbound, looked up")]
for i, r in enumerate(rows):
    for j, v in enumerate(r):
        f.text([10, 190, 370][j], 196 + i * 20, v, size=10, color=NAVY if i == 0 else SLATE, bold=(i == 0), anchor="start", vmid=True)
f.text(290, 274, "No entry for an unsolicited packet: it is dropped", size=10, color=RED, bold=True)
```

```svgfig label="4.8" caption="Two helper protocols on a timeline. Left: DHCP gets an address in four messages, DORA. The Discover is broadcast from 0.0.0.0 to 255.255.255.255 (client port 68, server port 67); the Offer proposes 192.168.1.50 with a 24 hour lease; the Request accepts it (still broadcast, so other servers learn the offer was refused); the Ack confirms. Right: traceroute sends probes with TTL 1, 2 and 3; each router subtracts 1, and the one that reaches 0 discards the packet and returns an ICMP time-exceeded (type 11), which reveals its address. The probe that reaches the destination gets an echo reply or port-unreachable reply, so the path is listed one hop at a time."
f = Fig(580, 300)
f.text(120, 14, "DHCP: DORA", size=11, color=NAVY, bold=True)
f.box(30, 24, 70, 26, "client", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(200, 24, 70, 26, "server", fill=MINT, stroke=TEAL, size=10, bold=True)
f.line(65, 50, 65, 280, color="#94a3b8", sw=1.2, dash=True)
f.line(235, 50, 235, 280, color="#94a3b8", sw=1.2, dash=True)
msgs = [("1 Discover", "0.0.0.0 to 255.255.255.255", 72, 1), ("2 Offer", "192.168.1.50, lease 24 h", 130, 0), ("3 Request", "I take 192.168.1.50", 188, 1), ("4 Ack", "confirmed, DNS, gateway", 246, 0)]
for nm, sub, y, d in msgs:
    f.arrow([(65, y), (235, y + 14)] if d else [(235, y), (65, y + 14)], color=RED if d else TEAL, sw=1.8)
    f.text(150, y - 8, nm, size=10, color=NAVY, bold=True)
    f.text(150, y + 30, sub, size=9.5, color=SLATE)
f.text(430, 14, "traceroute: TTL 1, 2, 3", size=11, color=NAVY, bold=True)
f.box(300, 24, 56, 26, "host", fill=BLUE, stroke=NAVY, size=10, bold=True)
for k, x in enumerate((392, 454, 516)):
    f.box(x, 24, 48, 26, "R%d" % (k + 1), fill=SAND, stroke=AMBER, size=10, bold=True)
for k in range(3):
    y = 84 + k * 62
    xr = (392, 454, 516)[k] + 24
    f.line(328, 50, 328, y + 14, color="#e2e8f0", sw=1)
    f.arrow([(332, y), (xr - 10, y)], color=RED, sw=1.6)
    f.arrow([(xr - 10, y + 18), (332, y + 18)], color=TEAL, sw=1.6, dash=True)
    f.text(430, y - 12, "probe TTL = %d" % (k + 1), size=9.5, color=RED, bold=True)
    f.text(430, y + 38, "R%d: time exceeded (11)" % (k + 1), size=9.5, color=TEAL, bold=True)
f.text(430, 278, "each reply reveals one router", size=10, color=SLATE)
```

```svgfig label="4.9" caption="Dijkstra from router A on the six-router network of this unit, computed in the figure. The program keeps the least tentative distance, finalises nodes in the order A, D, B, E, C, F and relaxes the neighbours of each. The shortest-path tree (thick teal links) is A-D (1), D-E (2), E-C (3), E-F (4) and A-B (2): the number in each circle is the final distance. The link A-C (cost 5) and the links C-D, B-C and C-F are not used. A's forwarding table keeps only the next hop: B via B, and C, D, E, F all via D. The tree has 5 links, n - 1 for n = 6 routers."
f = Fig(580, 290)
hq = __import__("heapq")
E = {("A", "B"): 2, ("A", "C"): 5, ("A", "D"): 1, ("B", "C"): 3, ("B", "D"): 2, ("C", "D"): 3, ("C", "E"): 1, ("C", "F"): 5, ("D", "E"): 1, ("E", "F"): 2}
adj = {}
for (u, v), w in E.items():
    adj.setdefault(u, []).append((v, w)); adj.setdefault(v, []).append((u, w))
dist = {"A": 0}; prev = {}; order = []; pq = [(0, "A")]
while pq:
    d, u = hq.heappop(pq)
    if u in order: continue
    order.append(u)
    for v, w in adj[u]:
        if v not in dist or d + w < dist[v]:
            dist[v] = d + w; prev[v] = u; hq.heappush(pq, (d + w, v))
P = {"A": (50, 140), "B": (150, 52), "D": (150, 228), "C": (290, 64), "E": (290, 216), "F": (400, 140)}
tree = set(frozenset((v, u)) for v, u in prev.items())
for (u, v), w in E.items():
    (x1, y1), (x2, y2) = P[u], P[v]
    t = frozenset((u, v)) in tree
    f.line(x1, y1, x2, y2, color=TEAL if t else "#cbd5e1", sw=4 if t else 1.6)
    f.text((x1 + x2) / 2 + (0 if abs(x1 - x2) > 1 else 10), (y1 + y2) / 2 - 7, str(w), size=10.5, color=RED if t else SLATE, bold=True)
for n, (x, y) in P.items():
    f.circle(x, y, 17, fill=SAND if n == "A" else "#ffffff", stroke=NAVY, sw=1.8, label=n, size=12, color=NAVY)
    f.text(x, y + 32, "d = %d" % dist[n], size=10, color=TEAL, bold=True)
def nxt(n):
    while prev[n] != "A": n = prev[n]
    return n
f.text(452, 20, "finalised in order", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(452, 40, " ".join(order), size=11, color=NAVY, anchor="start")
f.text(452, 74, "A's forwarding table", size=10.5, color=NAVY, bold=True, anchor="start")
for i, n in enumerate("BCDEF"):
    f.text(452, 96 + i * 20, "to %s  via %s   cost %d" % (n, nxt(n), dist[n]), size=10, color=SLATE, anchor="start", vmid=True)
f.text(290, 272, "thick teal = shortest-path tree (5 links); grey links carry no traffic from A", size=10, color=SLATE)
```

```svgfig label="4.10" caption="Distance-vector routing, simulated on the same network. Left: router A's vector after each synchronous round, from the Bellman-Ford rule d(u) = min over neighbours of c(u,v) + d(v); the table is computed by running the rule on all six routers. Round 0 holds only direct neighbours, round 1 gives C = 4 and E = 2 and F = 10, round 2 gives C = 3 and F = 4, and round 3 changes nothing: converged, with the same costs as Dijkstra. Right: count to infinity on the line A-B-C when link B-C fails. The two routers keep raising each other's cost for C (3, 4, 5, ..., 16) until it reaches RIP's infinity, 16, after 14 exchanges."
f = Fig(580, 300)
nodes = "ABCDEF"
E = {("A", "B"): 2, ("A", "C"): 5, ("A", "D"): 1, ("B", "C"): 3, ("B", "D"): 2, ("C", "D"): 3, ("C", "E"): 1, ("C", "F"): 5, ("D", "E"): 1, ("E", "F"): 2}
INF = 10 ** 9
nb = {n: {} for n in nodes}
for (u, v), w in E.items():
    nb[u][v] = w; nb[v][u] = w
D = {u: {t: (0 if t == u else nb[u].get(t, INF)) for t in nodes} for u in nodes}
rounds = [dict(D["A"])]
for r in range(3):
    new = {}
    for u in nodes:
        new[u] = {t: (0 if t == u else min(min(nb[u][v] + D[v][t] for v in nb[u]), INF)) for t in nodes}
    D = new
    rounds.append(dict(D["A"]))
f.text(14, 16, "router A's vector", size=10.5, color=NAVY, bold=True, anchor="start")
hdr = ["round", "B", "C", "D", "E", "F"]
for j, h in enumerate(hdr):
    f.text(18 + j * 42, 40, h, size=10, color=NAVY, bold=True, anchor="start")
for r, vec in enumerate(rounds):
    for j, t in enumerate("BCDEF"):
        v = vec[t]
        chg = r > 0 and rounds[r - 1][t] != v
        f.text(18 + (j + 1) * 42, 64 + r * 26, "inf" if v >= INF else str(v), size=11, color=RED if chg else SLATE, bold=chg, anchor="start", vmid=True)
    f.text(18, 64 + r * 26, str(r), size=11, color=NAVY, bold=True, anchor="start", vmid=True)
f.text(18, 176, "red = value changed in this round", size=10, color=RED, anchor="start")
f.text(18, 196, "round 3 equals round 2: converged", size=10, color=TEAL, bold=True, anchor="start")
f.text(18, 216, "costs match Dijkstra: 2, 3, 1, 2, 4", size=10, color=SLATE, anchor="start")
L, T, W, H = 300, 40, 260, 190
f.box(L, T, W, H, "", fill="#ffffff", stroke="#94a3b8", r=2, sw=1.2)
f.text(L + W / 2, 18, "count to infinity: cost of C", size=10.5, color=NAVY, bold=True)
for c in (4, 8, 12, 16):
    y = T + H - H * c / 17.0
    f.line(L, y, L + W, y, color="#e2e8f0", sw=1)
    f.text(L - 6, y, str(c), size=9.5, color=SLATE, anchor="end", vmid=True)
for k in range(14):
    cost = 3 + k
    x = L + 10 + k * 18
    y = T + H - H * cost / 17.0
    f.circle(x, y, 4.5, fill=RED if k % 2 == 0 else TEAL, stroke=RED if k % 2 == 0 else TEAL)
f.text(L + 10, T + H + 14, "1", size=9.5, color=SLATE)
f.text(L + 10 + 13 * 18, T + H + 14, "14", size=9.5, color=SLATE)
f.text(L + W / 2, T + H + 30, "exchange number (red: B updates, teal: A updates)", size=10, color=SLATE)
f.text(L + 150, T + 20, "16 = infinity: route dropped", size=10, color=RED, bold=True, anchor="end")
```

```svgfig label="4.11" caption="Why routers drop packets: queueing delay against utilisation, computed with the single-queue formula T = T0 / (1 - rho), where T0 is the time to send one packet and rho is the link utilisation. For a 1500 byte packet on a 1 Gbps link T0 = 12 microseconds, so the delay is 24 microseconds at 50 percent load, 60 at 80, 120 at 90, 240 at 95 and 1200 at 99 percent (log scale). Delay does not rise gently: past about 80 percent the curve turns up sharply, buffers fill, and packets are dropped. Operators therefore plan links to stay below about 70 percent at the busy hour."
f = Fig(580, 270)
cm = __import__("math")
L, T, W, H = 64, 14, 330, 210
f.box(L, T, W, H, "", fill="#ffffff", stroke="#94a3b8", r=2, sw=1.2)
Yl = lambda v: T + H - H * (cm.log10(v) - 1) / 3.2
Xr = lambda r: L + W * r / 1.0
for v, lab in ((10, "10 us"), (100, "100 us"), (1000, "1 ms"), (1000 * 10 ** 0.2, "")):
    if lab:
        f.line(L, Yl(v), L + W, Yl(v), color="#e2e8f0", sw=1)
        f.text(L - 6, Yl(v), lab, size=9.5, color=SLATE, anchor="end", vmid=True)
for r in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
    f.text(Xr(r), T + H + 14, "%d%%" % (r * 100), size=9.5, color=SLATE)
f.text(L + W / 2, T + H + 32, "link utilisation", size=10, color=SLATE, bold=True)
pts = " ".join("%.1f,%.1f" % (Xr(r), Yl(12.0 / (1 - r))) for r in [k / 200.0 for k in range(0, 199)])
f.raw('<polyline points="%s" fill="none" stroke="#b91c1c" stroke-width="2.6"/>' % pts)
for r in (0.5, 0.8, 0.9, 0.95):
    f.circle(Xr(r), Yl(12.0 / (1 - r)), 4, fill=NAVY, stroke=NAVY)
f.line(Xr(0.8), T, Xr(0.8), T + H, color=AMBER, sw=1.4, dash=True)
f.text(Xr(0.8) - 6, T + 16, "knee: 80%", size=10, color=AMBER, bold=True, anchor="end")
rows = [("load", "delay"), ("50 %", "24 us"), ("80 %", "60 us"), ("90 %", "120 us"), ("95 %", "240 us"), ("99 %", "1200 us")]
for i, r in enumerate(rows):
    for j, v in enumerate(r):
        f.text([420, 490][j], 40 + i * 22, v, size=10, color=NAVY if i == 0 else SLATE, bold=(i == 0), anchor="start")
f.text(420, 190, "T0 = 12 000 bits / 1 Gbps", size=10, color=SLATE, anchor="start")
f.text(420, 208, "= 12 us per packet", size=10, color=SLATE, anchor="start")
```

```svgfig label="4.12" caption="BGP between autonomous systems. AS 64512 originates 203.0.113.0/24 (the numbers are from the range reserved for documentation) and announces it to its neighbours with the path 64512. AS 64513 passes it on as 64513 64512. AS 64514 hears the route twice, directly with path 64512 (length 1) and through 64513 with path 64513 64512 (length 2); BGP prefers the shorter AS path, so the direct link wins. A router that sees its own AS number in a path discards the route, which prevents loops. Inside each AS an interior protocol such as OSPF finds paths; BGP runs over TCP port 179 and applies policy."
f = Fig(580, 280)
def asbox(x, y, n, col, st):
    f.box(x, y, 130, 64, "AS %d" % n, fill=col, stroke=st, size=12, bold=True, r=22, color=NAVY)
asbox(20, 100, 64512, MINT, TEAL); asbox(225, 20, 64513, BLUE, NAVY); asbox(430, 100, 64514, SAND, AMBER)
f.text(85, 178, "origin: 203.0.113.0/24", size=9.5, color=TEAL, bold=True)
f.arrow([(150, 112), (230, 76)], color=TEAL, sw=2)
f.text(168, 82, "path 64512", size=9.5, color=TEAL, bold=True, anchor="end")
f.arrow([(355, 76), (440, 112)], color=NAVY, sw=2)
f.text(410, 76, "path 64513 64512", size=9.5, color=NAVY, bold=True, anchor="start")
f.arrow([(150, 140), (430, 140)], color=RED, sw=2.4)
f.text(290, 132, "path 64512 (length 1): preferred", size=10, color=RED, bold=True)
f.text(495, 190, "AS 64514 chooses", size=10, color=RED, bold=True)
f.text(495, 206, "the direct route", size=10, color=RED, bold=True)
f.text(290, 232, "loop rule: a router that sees its own AS number in the path rejects the route", size=10, color=SLATE)
f.text(290, 252, "OSPF inside each AS (link state, areas); BGP between them (path vector, TCP 179, policy)", size=10, color=NAVY, bold=True)
```

```svgfig label="4.13" caption="Route aggregation (supernetting), computed. The four /24 networks 192.168.0.0, 192.168.1.0, 192.168.2.0 and 192.168.3.0 differ only in the last two bits of the third octet (00, 01, 10, 11), so their first 22 bits are the same (blue) and one table entry, 192.168.0.0/22, covers all 1024 addresses. The conditions are: the networks are contiguous, their number is a power of two, and the first one is aligned on a multiple of the block size. Aggregation is how an ISP announces thousands of customer blocks as a few prefixes and keeps the global routing table small."
f = Fig(580, 240)
ip = __import__("ipaddress")
nets = [ip.ip_network("192.168.%d.0/24" % i) for i in range(4)]
agg = list(ip.collapse_addresses(nets))[0]
f.text(120, 14, "third octet in binary", size=10, color=NAVY, bold=True, anchor="start")
for i, n in enumerate(nets):
    y = 28 + i * 34
    f.text(6, y + 13, str(n), size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    s = format(int(str(n.network_address).split(".")[2]), "08b")
    for k, ch in enumerate(s):
        f.box(120 + k * 28, y, 26, 26, ch, fill=BLUE if k < 6 else SAND, stroke=NAVY if k < 6 else AMBER, size=12, bold=True, r=3, color=NAVY if k < 6 else "#92400e")
f.text(120 + 3 * 28, 176, "first 6 bits of the octet (plus 16 before it) = 22 shared bits", size=10, color=NAVY, bold=True, anchor="start")
f.box(6, 190, 568, 40, "aggregate: %s   (%d addresses, 1 table entry instead of 4)" % (agg, agg.num_addresses), fill=MINT, stroke=TEAL, size=12, bold=True, color=NAVY)
```

### 4.8.1 Eight uses of network layer technology in Nepal

1. **Addressing plans for colleges and offices.** A college that receives one block of addresses from its ISP divides it into subnets for the office, the labs and the Wi-Fi, using VLSM so that no addresses are wasted (Fig. 4.4). Each lab has its own broadcast domain and its own gateway. Good subnetting also lets the administrator write a firewall rule for one department.
2. **NAT in every home and mobile network.** A family with one broadband line puts a dozen devices behind a single public address, and mobile operators use carrier-grade NAT for millions of phones (Fig. 4.7). IPv4 addresses are scarce, so this is how the country keeps growing. The price is that a home server needs port forwarding.
3. **DHCP in the home router.** Every phone that joins the Wi-Fi gets an address, mask, gateway and DNS server in the four DORA messages (Fig. 4.8). A lease of a few hours lets the router reuse addresses from visitors who have left. When DHCP fails, the phone falls back to a 169.254 address and cannot reach the Internet.
4. **Diagnosing slow connections with ping and traceroute.** A technician who hears that a payment site is slow can run ping to measure delay and traceroute to see which hop adds it (Fig. 4.8). Each hop appears because a router returned an ICMP time-exceeded message. Seeing the delay jump at the hop that leaves the country shows the cause is an international link, not the local network.
5. **OSPF in ISP and bank networks.** An ISP or a bank with many sites runs OSPF so that routers learn the whole map and recompute the shortest paths within a second or two after a link fails (Fig. 4.9). Areas keep the load on small routers low. Link costs are set from bandwidth, so the fibre is preferred over the radio backup.
6. **BGP to the world.** Nepali ISPs buy transit from providers in neighbouring countries and announce their address blocks with BGP (Fig. 4.12). The AS path shows which route is shorter, and policy decides which provider is preferred. A wrong announcement can pull other countries' traffic into the wrong network, so filters are essential.
7. **Route aggregation by ISPs.** An ISP gives customers small blocks from its own large block and announces only the aggregate to the world (Fig. 4.13). This keeps the routing table small and the routers fast. A customer that moves to another ISP must renumber, which is the price of aggregation.
8. **IPv6 deployment.** Mobile and fixed operators in the region are enabling IPv6 so that every device can have its own global address without NAT (Fig. 4.6). A phone builds its link-local address automatically, and a /64 for each LAN removes the need to ration addresses. Dual-stack lets old IPv4-only sites keep working during the transition.

## Formula and fact sheet

- Addresses: 2³² IPv4, 2¹²⁸ IPv6. /n block: 2^(32−n) addresses, 2^(32−n) − 2 hosts. Borrow ⌈log₂ N⌉ bits for N subnets.
- Block size = 256 − mask octet. Network = address AND mask. Broadcast = network OR NOT mask.
- Private: 10/8, 172.16/12, 192.168/16. Loopback 127/8. Link-local 169.254/16.
- Fragment offset in 8-byte units; fragment data a multiple of 8 except the last.
- Bellman–Ford: d_u(t) = min_v [c(u,v) + d_v(t)]. Dijkstra: finalise the nearest node, relax edges.
- RIP: hop count, max 15, UDP 520. OSPF: link state, cost = 100 Mbps / bandwidth by default. BGP: path vector, TCP 179.

## Chapter summary

- IP is a best-effort, connectionless service; routers forward by longest-prefix match on the destination address and split oversize datagrams into fragments.
- CIDR, subnetting, VLSM and aggregation allow addresses to be allocated and summarised flexibly; ARP, ICMP, DHCP and NAT make IPv4 usable; IPv6 restores the address space.
- Link-state routing (Dijkstra) gives every router the same map; distance-vector routing (Bellman–Ford) shares tables with neighbours and risks count-to-infinity.
- OSPF and RIP route inside an AS, BGP between ASes.

## Practice

1. Find the network address, broadcast address, range and host count for 192.168.10.77/26 and 172.16.5.130/20.
2. Divide 192.168.1.0/24 into at least six equal subnets. Give the prefix, hosts per subnet and the third subnet.
3. Design VLSM for 100, 50, 25 and 2 hosts from 10.0.0.0/24.
4. Which prefix is needed for a LAN of 500 hosts?
5. Aggregate 192.168.0.0/24 to 192.168.3.0/24.
6. Longest-prefix match: to where is 10.1.9.9 forwarded with the table in Section 4.4?
7. A 4020-byte datagram meets an MTU of 1500. Give each fragment's length, offset and MF.
8. Run Dijkstra on the six-router network from A; give the path to F and A's next hops.
9. Do three rounds of distance-vector at A and compare with Dijkstra.
10. Explain count to infinity, split horizon and poison reverse.
11. Describe the four DHCP messages and what NAT does with the port number.
12. Compress 2001:0db8:0000:0000:0000:ff00:0042:8329. How many /64 subnets are in a /48?

::: note Answers and worked solutions
**1.** 192.168.10.77/26: network 192.168.10.64, broadcast 192.168.10.127, hosts .65–.126 (62). 172.16.5.130/20: network 172.16.0.0, broadcast 172.16.15.255, hosts 172.16.0.1–172.16.15.254 (4094).
**2.** ⌈log₂ 6⌉ = 3 borrowed bits: /27, 8 subnets, 30 hosts each; the third is 192.168.1.64/27 (hosts .65–.94, broadcast .95).
**3.** Sales 10.0.0.0/25, Engineering 10.0.0.128/26, Admin 10.0.0.192/27, WAN 10.0.0.224/30 (table in Section 4.4).
**4.** 500 + 2 = 502 addresses need 9 host bits (512), so the prefix is /23 (32 − 9).
**5.** 192.168.0.0/22.
**6.** It matches 10.0.0.0/8 and 10.1.0.0/16 (not 10.1.2.0/24); the longest is /16, so R2.
**7.** (1500, offset 0, MF 1), (1500, offset 185, MF 1), (1060, offset 370, MF 0).
**8.** Dist: A 0, B 2, C 3, D 1, E 2, F 4; path A → D → E → F; next hops: B via B, everything else via D.
**9.** Round 1: 2, 4, 1, 2, 10; round 2: 2, 3, 1, 2, 4; round 3 unchanged. The same as Dijkstra.
**10.** After a failure, two routers keep increasing each other's cost by one (3, 4, 5, … up to 16 in RIP). Split horizon withholds a route from the neighbour it came from; poison reverse advertises it back with infinity so the neighbour does not use it.
**11.** Discover, Offer, Request, Ack. NAT rewrites the private source address and port to the public address and a unique public port and keeps a table to translate replies back.
**12.** 2001:db8::ff00:42:8329. A /48 contains 2^(64−48) = 65,536 subnets of /64.
:::

## Model answers for Unit 4

**Q1. Explain IPv4 addressing, classful addressing and CIDR. For the address 192.168.10.77/26 find the network address, broadcast address and usable host range. (10 marks)**

**Introduction.** An IPv4 address is 32 bits, written as four decimal bytes, and identifies one interface. It has a network part and a host part, and the dividing line decides how many networks and how many hosts per network exist.

**Classful addressing (historic).** The first bits of the address fixed the split.

| Class | First bits | First byte | Default mask | Hosts per network |
|---|---|---|---|---|
| A | 0 | 1-126 | /8 | 16 777 214 |
| B | 10 | 128-191 | /16 | 65 534 |
| C | 110 | 192-223 | /24 | 254 |
| D | 1110 | 224-239 | none | multicast |
| E | 1111 | 240-255 | none | reserved |

A company needing 300 hosts had to take a class B and waste more than 65 000 addresses, so in 1993 **CIDR** replaced the classes.

**CIDR.** The address is written a.b.c.d/n, where the first n bits are the network part and the mask is n ones followed by 32 - n zeros. A /n block has 2^(32-n) addresses, of which 2^(32-n) - 2 are usable, because the all-zeros host part is the network address and the all-ones host part is the broadcast address. Private ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) are not routed on the Internet.

**Worked example (Fig. 4.3).** For 192.168.10.77/26 the mask is 255.255.255.192.

1. The interesting octet is the fourth: block size = 256 - 192 = 64.
2. 77 lies in the block that starts at 64, so the network address is **192.168.10.64**.
3. The broadcast address is 64 + 63 = **192.168.10.127**.
4. The usable hosts run from **192.168.10.65 to 192.168.10.126**, which is 62 hosts.

**Special addresses.** Some addresses have fixed meanings: 127.0.0.1 (loopback, this host), 169.254.0.0/16 (link-local, chosen automatically when DHCP fails), 255.255.255.255 (limited broadcast) and 100.64.0.0/10 (shared space used by carrier-grade NAT). A host in the same subnet is reached directly by ARP, while any other destination is sent to the default gateway, so the mask also decides what is local.

**Conclusion.** CIDR lets a block of any power-of-two size be given to a network, which saved the IPv4 space for another two decades and allowed route aggregation.

**Q2. Explain VLSM and route aggregation. Divide 10.0.0.0/24 among LANs of 100, 50 and 25 hosts and a 2-host router link. (10 marks)**

**Introduction.** Plain subnetting gives every subnet the same size, which wastes addresses when the LANs differ. **Variable-length subnet masks (VLSM)** give each LAN a block of the right size, and **route aggregation** (supernetting) does the reverse, joining blocks into one shorter prefix.

**VLSM procedure.**

1. List the LANs from largest to smallest.
2. For each, find the smallest block with at least hosts + 2 addresses (network and broadcast).
3. Allocate the blocks one after another from the start, each aligned to a multiple of its own size.

**Worked example (Fig. 4.4).**

| LAN | Hosts | Block | Usable hosts | Range | Broadcast |
|---|---|---|---|---|---|
| Sales | 100 | 10.0.0.0/25 | 126 | 10.0.0.1 - 10.0.0.126 | 10.0.0.127 |
| Engineering | 50 | 10.0.0.128/26 | 62 | 10.0.0.129 - 10.0.0.190 | 10.0.0.191 |
| Admin | 25 | 10.0.0.192/27 | 30 | 10.0.0.193 - 10.0.0.222 | 10.0.0.223 |
| WAN link | 2 | 10.0.0.224/30 | 2 | 10.0.0.225 - 10.0.0.226 | 10.0.0.227 |

The blocks use 128 + 64 + 32 + 4 = 228 addresses, and 10.0.0.228 to 10.0.0.255 remains free. An equal split would need a /25 for each of the four LANs, which is 512 addresses and would not fit in the /24.

**Route aggregation (Fig. 4.13).** Four contiguous /24 networks, 192.168.0.0 to 192.168.3.0, share their first 22 bits, so a router can announce the single prefix **192.168.0.0/22**. The conditions are that the blocks are contiguous, their number is a power of two and the first block is aligned on the block size.

**Longest-prefix match (Fig. 4.5).** When several routes match, the router uses the one with the longest prefix, so a more specific route overrides the aggregate.

**Conclusion.** VLSM saves addresses inside an organisation, and aggregation saves routing-table entries outside it. Both depend on addresses being allocated in aligned power-of-two blocks.

**Q3. Describe the IPv4 datagram format. How is a 4020 byte datagram fragmented over a link with MTU 1500? (10 marks)**

**Introduction.** The IPv4 datagram is a header of 20 to 60 bytes followed by data. The header (Fig. 4.1) carries everything a router needs to forward the packet.

**Main header fields.**

1. **Version and IHL:** 4 for IPv4; the header length in 32-bit words (5 means 20 bytes).
2. **Total length:** header plus data in bytes, at most 65 535.
3. **Identification, flags and fragment offset:** these let the destination reassemble fragments; the flags are DF (do not fragment) and MF (more fragments), and the offset counts 8-byte units.
4. **TTL:** the hop limit, decreased by every router; at 0 the packet is discarded, which stops loops and makes traceroute possible.
5. **Protocol:** which upper layer receives the data (6 = TCP, 17 = UDP, 1 = ICMP).
6. **Header checksum:** the Internet checksum over the header only.
7. **Source and destination addresses:** 32 bits each.

**Fragmentation (Fig. 4.2).** The datagram has a 20-byte header and 4000 bytes of data. With MTU 1500 each fragment can carry 1500 - 20 = 1480 bytes of data, and 1480 is a multiple of 8.

| Fragment | Total length | Data bytes | Offset field | MF |
|---|---|---|---|---|
| 1 | 1500 | 1480 | 0 | 1 |
| 2 | 1500 | 1480 | 185 | 1 |
| 3 | 1060 | 1040 | 370 | 0 |

All fragments have the same identification. Only the destination reassembles them, and if one fragment is lost the entire datagram is lost. Fragmenting also adds two extra headers (40 bytes), so modern hosts set DF and use path MTU discovery instead.

**Reassembly.** The destination collects all fragments with the same identification, source, destination and protocol, places each at its offset (offset x 8 bytes), and delivers the datagram when the fragment with MF = 0 and all earlier pieces have arrived. A timer discards the partial datagram if a piece never comes. Because the TTL changes at every router, each router also recomputes the header checksum, which is why the checksum covers only the header and is cheap.

**Conclusion.** The header gives IP a simple, fast forwarding job, and fragmentation lets one datagram cross links of different MTU at some cost in overhead and reliability.

**Q4. Compare link-state and distance-vector routing. Apply Dijkstra's algorithm from router A on the network of Fig. 4.9. (10 marks)**

**Introduction.** A routing algorithm fills the forwarding tables. The two main families differ in what a router knows and what it sends.

**Link-state routing.** Each router measures the cost to its neighbours, floods this information to all routers, builds the complete map and runs **Dijkstra's algorithm** to compute shortest paths. OSPF and IS-IS work like this.

**Distance-vector routing.** Each router keeps a vector of costs to every destination and sends it only to neighbours, who apply the Bellman-Ford rule d(u) = min of c(u,v) + d(v). RIP works like this.

**Dijkstra from A.** The links are A-B 2, A-C 5, A-D 1, B-C 3, B-D 2, C-D 3, C-E 1, C-F 5, D-E 1, E-F 2.

1. Finalise A (0); the tentative costs are B 2, C 5, D 1.
2. Finalise D (1); via D: C = 4, E = 2.
3. Finalise B (2); via B nothing improves (C would be 5).
4. Finalise E (2); via E: C = 3, F = 4.
5. Finalise C (3); then F (4).

The order is A, D, B, E, C, F, with costs B 2, C 3, D 1, E 2, F 4. The shortest path to F is A, D, E, F. A's next hops are B for B and D for everything else.

| Point | Link state | Distance vector |
|---|---|---|
| Knowledge | whole map | only neighbours' vectors |
| Information sent | own links, flooded to all | whole vector, to neighbours |
| Algorithm | Dijkstra | Bellman-Ford |
| Convergence | fast | slow, count to infinity |
| Memory and CPU | more | less |
| Example | OSPF, IS-IS | RIP |

**Check of the answer.** Distance vector reaches the same costs: after round 2 router A holds 2, 3, 1, 2, 4 for B, C, D, E and F, and round 3 changes nothing (Fig. 4.10). The tree of shortest paths from A has five links, one fewer than the number of routers, so every router is reached once and no loops exist.

**Conclusion.** Link state converges quickly and scales with areas, and distance vector is simpler but slower to react to bad news. Both give the same costs when converged (Fig. 4.10).

**Q5. What is the count-to-infinity problem and how is it reduced? (5 marks)**

Distance-vector routing spreads good news fast but bad news slowly. In the line A - B - C with all costs 1, B reaches C at cost 1 and A at cost 2.

1. **The failure.** The link B-C breaks. B looks for another route and hears from A that A can reach C at cost 2, so B sets its cost to 3 via A.
2. **The loop.** A's route to C goes through B, so A raises its cost to 4; B then raises to 5, A to 6, and so on.
3. **The end.** The costs rise by one per exchange until they reach the value taken as infinity, 16 in RIP, after 14 exchanges (Fig. 4.10). During this time packets for C loop between A and B.
4. **Remedies.** Defining a small infinity (16) limits the damage; **split horizon** stops a router advertising a route back to the neighbour it learned it from; **poison reverse** advertises it back with cost infinity; **triggered updates** and **hold-down timers** send bad news at once.
5. **Limit.** These tricks fail for some loops through three or more routers, which is why link-state protocols are preferred in large networks.

**Q6. Explain NAT with an example. State its advantages and disadvantages. (5 marks)**

**Network address translation** lets many hosts with private addresses share one public address. The NAT router rewrites the source address and port of each outgoing packet and remembers the mapping in a table (Fig. 4.7).

1. **Outbound.** Host 192.168.1.10 sends from port 51000; the router rewrites the source to 202.79.1.5:40001 and creates a table entry.
2. **Second host.** Host 192.168.1.11 also uses port 51000; the router assigns 40002, so the two flows stay separate.
3. **Inbound.** A reply to 202.79.1.5:40002 is looked up and sent to 192.168.1.11:51000.
4. **Advantages.** It saves public addresses, hides the internal structure, and lets a network change ISP without renumbering the inside. Unsolicited packets find no entry and are dropped.
5. **Disadvantages.** It breaks end-to-end addressing, so servers need port forwarding; peer-to-peer and some voice applications need traversal methods; and the router must keep state for every flow. IPv6 removes the need for NAT.

**Q7. Explain how DHCP and ICMP (ping and traceroute) work. (5 marks)**

**DHCP** gives a new host its address automatically. It works in four messages, **DORA** (Fig. 4.8), using UDP ports 67 (server) and 68 (client).

1. **Discover:** the client broadcasts from 0.0.0.0 to 255.255.255.255.
2. **Offer:** a server proposes an address, mask, gateway, DNS server and lease time.
3. **Request:** the client broadcasts that it accepts one offer.
4. **Ack:** the server confirms; the lease is renewed halfway through.

**ICMP** carries errors and diagnostics inside IP packets (protocol 1). **ping** sends echo requests (type 8) and measures the time of the echo replies (type 0). **traceroute** sends probes with TTL = 1, 2, 3 and so on; each router that reduces the TTL to 0 discards the packet and returns a time-exceeded message (type 11), so the addresses and delays of the routers on the path are listed one by one. A star in the output means a router did not answer, not that the path is broken. Other common ICMP messages are destination unreachable (type 3), used also for path MTU discovery, and redirect (type 5), which tells a host about a better gateway.

**Q8. Compare IPv4 and IPv6. Explain IPv6 address notation, types and the transition methods. (10 marks)**

**Introduction.** IPv4 has only 2^32 (about 4.3 billion) addresses, and its pool ran out in 2011. **IPv6** has 128-bit addresses, which is 2^128 = 3.4 x 10^38, and simplifies the header.

**Notation.** An IPv6 address is eight groups of four hex digits. Leading zeros in a group may be dropped, and one run of all-zero groups may be replaced by a double colon: 2001:0db8:0000:0000:0000:ff00:0042:8329 becomes 2001:db8::ff00:42:8329 (Fig. 4.6).

**Address types.**

| Type | Prefix | Note |
|---|---|---|
| Global unicast | 2000::/3 | routable on the Internet |
| Link-local | fe80::/10 | automatic on every interface |
| Unique local | fc00::/7 | private equivalent |
| Multicast | ff00::/8 | replaces broadcast |
| Loopback | ::1/128 | this host |

A site normally receives a /48 and every LAN is a /64. A host can form its own interface identifier with EUI-64: insert FF:FE into the MAC address and flip one bit, so 00:1A:2B:3C:4D:5E gives fe80::21a:2bff:fe3c:4d5e.

**Comparison.**

| Feature | IPv4 | IPv6 |
|---|---|---|
| Address | 32 bits | 128 bits |
| Header | 20-60 bytes, checksum | fixed 40 bytes, no checksum |
| Fragmentation | routers and source | source only |
| Configuration | DHCP, manual | SLAAC and DHCPv6 |
| Address resolution | ARP | Neighbor Discovery (ICMPv6) |
| Broadcast | yes | no (multicast) |
| NAT | widely needed | not needed |

**Transition.** Three methods let the two protocols coexist: **dual stack** (hosts run both), **tunnelling** (IPv6 packets carried inside IPv4) and **translation** (a gateway converts between them, for example NAT64).

**Header differences.** The IPv6 header is a fixed 40 bytes with version, traffic class, flow label, payload length, next header, hop limit and the two 128-bit addresses. It has no header checksum (the link layer and TCP or UDP already check) and no IHL, and routers never fragment: only the source does, using an extension header, so it must discover the path MTU first. Options live in extension headers that most routers do not inspect, which makes forwarding faster. Hosts configure themselves with router advertisements (SLAAC) and find neighbours with ICMPv6 instead of ARP.

**Conclusion.** IPv6 solves the address shortage and restores end-to-end addressing, and the transition will continue for many years with dual-stack as the usual path.

**Q9. Compare RIP, OSPF and BGP. (5 marks)**

An **autonomous system** (AS) is a group of networks under one administration with one routing policy. Protocols inside an AS are interior, and protocols between ASes are exterior (Fig. 4.12).

1. **RIP** is a distance-vector protocol with the hop count as its metric. The largest usable value is 15, and 16 means unreachable. It sends updates every 30 seconds over UDP port 520 and suits small networks.
2. **OSPF** is a link-state protocol. It floods link-state advertisements, uses a cost based on bandwidth, divides a large network into areas joined at area 0, and elects a designated router on LANs. It converges fast and is the usual interior protocol.
3. **BGP** is a path-vector protocol between ASes. It runs over TCP port 179, and each route carries the list of ASes it has crossed, which prevents loops and shows the length of the path. Policy decides the choice among routes.
4. **Choice.** A company uses OSPF inside; an ISP uses OSPF or IS-IS inside and BGP to its customers and to other ISPs.
