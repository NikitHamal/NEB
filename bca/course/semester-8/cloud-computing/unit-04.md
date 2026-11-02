---
subject: Cloud Computing
grade: BCA Semester 8
unit: 4
title: Cloud Networking, VPC Addressing, VXLAN, Load Balancing and CDN
hours: 6
area: BCA 451 · Cloud Computing · Unit 4
---

A cloud customer sees a private network of their own: addresses they chose, subnets they carved, firewalls they configured. The provider builds that illusion for thousands of tenants on one shared physical fabric, using tunnelling to separate tenants, software routers to connect them and load balancers and caches to carry traffic to users. This unit covers the customer's view (VPC design and addressing) and the machinery underneath (VXLAN overlays, load balancing, CDN).

::: key What this unit gives you
- Virtual private clouds: subnets, route tables, gateways, security groups versus network ACLs.
- CIDR arithmetic for planning address space, checked with code.
- VXLAN encapsulation overhead and its effect on MTU.
- Load balancing algorithms (including smooth weighted round robin) and CDN caching arithmetic.
:::

## 4.1 The virtual private cloud

A **VPC** is a logically isolated network in a region. The customer chooses a private IPv4 range (RFC 1918: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) and divides it into **subnets**, each in one availability zone.

- A **public subnet** has a route to an **internet gateway**; instances there can have public IP addresses.
- A **private subnet** has no direct inbound route from the internet. Outbound access, if needed, goes through a **NAT gateway** placed in a public subnet.
- **Route tables** decide where each destination prefix is sent (the longest matching prefix wins).
- **Security groups** are *stateful* firewalls attached to instances: allow rules only, and return traffic is automatically permitted. **Network ACLs** are *stateless* firewalls on subnets: ordered allow and deny rules for both directions.
- **VPC peering** and **transit gateways** connect VPCs; **VPN** and dedicated links (for example AWS Direct Connect) connect to on-premises networks. Overlapping CIDR ranges cannot be peered, so plan address space before building.

## 4.2 CIDR planning

An IPv4 prefix /*p* leaves 32 − *p* host bits, so it contains 2^(32−*p*) addresses. Splitting a /16 into /24 subnets gives 2^(24−16) = 256 subnets of 256 addresses. Providers reserve a few addresses in each subnet (AWS reserves five: network, router, DNS, future use and broadcast), so a /24 offers 251 usable addresses. Because small subnets in many zones are easy to exhaust, architects choose a generous VPC range (/16) and /20 to /24 subnets.

```python
import ipaddress
vpc = ipaddress.ip_network("10.0.0.0/16")
subnets = list(vpc.subnets(new_prefix=24))
usable = subnets[0].num_addresses - 5
print(f"VPC {vpc}: {vpc.num_addresses} addresses, {len(subnets)} subnets of /24, {usable} usable per /24 (AWS reserves 5)")
ip = ipaddress.ip_address("10.0.3.77")
print(f"{ip} in 10.0.3.0/24: {ip in subnets[3]}; in 10.0.4.0/24: {ip in subnets[4]}")
```
```output
VPC 10.0.0.0/16: 65536 addresses, 256 subnets of /24, 251 usable per /24 (AWS reserves 5)
10.0.3.77 in 10.0.3.0/24: True; in 10.0.4.0/24: False
```
Membership is a bitwise test: an address belongs to a prefix when its top *p* bits equal the prefix's. The address 10.0.3.77 shifted right by 8 bits equals the /24 prefix 10.0.3 and not 10.0.4, which the independent bit-arithmetic check confirmed.

::: caution
Do not forget IPv6 and growth. Running out of addresses forces painful renumbering; many clouds now offer dual-stack VPCs, and IPv6 subnets are conventionally /64.
:::

## 4.3 Overlay networks and VXLAN

Tenant networks overlap (every customer wants 10.0.0.0/16), so the provider cannot route tenant addresses on the physical network. Instead the host's virtual switch **encapsulates** each tenant frame inside a packet addressed between *physical hosts*. **VXLAN** (RFC 7348) wraps a full Layer 2 Ethernet frame in a UDP datagram (destination port 4789) with an 8-byte header carrying a 24-bit **VNI** (virtual network identifier), giving 2²⁴ = 16.7 million segments, versus 4,094 for VLAN.

The extra bytes inside the underlay's IP packet are: outer IPv4 header (20), outer UDP header (8), VXLAN header (8) and the *inner Ethernet header* (14), which now travels as payload. That is 50 bytes. If the physical network's IP MTU is 1500, the tenant's inner IP MTU can be at most 1500 − 50 = 1450; a tenant sending 1500-byte packets would see fragmentation or drops.

```python
overhead_parts = {"outer IPv4": 20, "outer UDP": 8, "VXLAN header": 8, "inner Ethernet": 14}
ov = sum(overhead_parts.values())
print(f"VXLAN overhead {ov} bytes; inner MTU {1500 - ov} on 1500 underlay, {9000 - ov} on 9000 jumbo")
print(f"full inner packet wire efficiency: {(1500 - ov) / 1500 * 100:.2f}%")
```
```output
VXLAN overhead 50 bytes; inner MTU 1450 on 1500 underlay, 8950 on 9000 jumbo
full inner packet wire efficiency: 96.67%
```
A full-size inner packet therefore uses 96.67% of the underlay packet for tenant data. Cloud providers lower guest MTUs or use jumbo frames inside the fabric (9000 bytes leaves 8950), and Path MTU Discovery relies on ICMP, which careless security rules sometimes block, causing mysterious hangs on large transfers.

## 4.4 Load balancing

A **load balancer** distributes requests across healthy backends, giving scale and availability. **Layer 4** balancers operate on TCP/UDP flows (Network Load Balancer); **Layer 7** balancers understand HTTP and can route by host, path or header, terminate TLS and apply sticky sessions (Application Load Balancer). **Health checks** remove failed backends from rotation.

Algorithms:

- **Round robin:** rotate evenly; ignores differing capacity.
- **Weighted round robin:** servers get shares proportional to weight. The naive version sends bursts of consecutive requests to the heavy server; **smooth weighted round robin** (as in nginx) spreads them.
- **Least connections:** send to the backend with fewest active connections; adapts to slow requests.
- **Hash-based / consistent hashing (Unit 3):** the same client or key goes to the same backend, enabling caching.
- **Power of two choices:** pick two backends at random and use the less loaded; near-optimal and cheap.

In smooth weighted round robin each backend keeps a *current weight*. At each pick, add every backend's static weight to its current weight, choose the largest, then subtract the total weight from the chosen one.

```python
weights = {"a": 5, "b": 1, "c": 1}
total = sum(weights.values())
current = {k: 0 for k in weights}
seq = ""
for _ in range(total):
    for k, w in weights.items():
        current[k] += w
    pick = max(current, key=current.get)
    current[pick] -= total
    seq += pick
print(f"smooth WRR 5:1:1 sequence: {seq}")
```
```output
smooth WRR 5:1:1 sequence: aabacaa
```
The result `aabacaa` serves a five times, b and c once each over seven picks, but interleaves the light servers instead of sending five consecutive requests to a. After a full cycle all current weights return to zero, so the pattern repeats exactly.

## 4.5 Content delivery networks

A **CDN** places caches at **edge locations** near users. A request first hits the edge; on a **hit** the object is served locally, on a **miss** the edge fetches it from the **origin**, stores it and serves it. Caching is controlled by HTTP headers (`Cache-Control: max-age`, `ETag`) and by the CDN's own TTL rules. Dynamic content can use short TTLs, **stale-while-revalidate** and **origin shield** tiers to collapse many edge misses into one origin request. Purging (invalidation) removes content before the TTL ends.

The average latency of a cache is a weighted mean: *hit ratio × edge latency + (1 − hit ratio) × origin latency*.

```python
hit, edge, origin = 0.9, 20, 220
mean = hit * edge + (1 - hit) * origin
print(f"hit ratio {hit:.2f}: mean latency {mean:.1f} ms, origin requests {round((1 - hit) * 1000)} of 1000")
```
```output
hit ratio 0.90: mean latency 40.0 ms, origin requests 100 of 1000
```
At a 90% hit ratio, the mean latency is 40.0 ms, against 220 ms with no CDN, and the origin sees only 100 of every 1,000 requests, a 90% reduction in origin load. Raising the hit ratio from 90% to 99% brings mean latency to 22 ms and origin traffic to 10 requests per 1,000, which is why cache-key hygiene (ignoring irrelevant query parameters) matters.

## 4.6 DNS-based routing

Cloud DNS services provide health-checked routing policies: weighted (traffic splitting for canary releases), latency-based (nearest region), failover (secondary on primary failure) and geolocation (legal or language routing). A low TTL speeds failover but increases query load.

## 4.7 Summary and exercises

A VPC gives tenants private subnets with stateful and stateless firewalls; CIDR arithmetic plans address space; VXLAN overlays cost 50 bytes per packet and reduce tenant MTU; load balancers and CDNs raise availability and cut latency.

1. Differentiate a security group from a network ACL.
2. How many usable addresses does a /20 subnet offer if five are reserved? How many /26 subnets fit in a /22?
3. Compute the inner MTU for a 1,600-byte underlay with VXLAN, and explain what happens to a 1,500-byte tenant packet.
4. Trace smooth WRR for weights 3:1 over four picks.
5. Compare L4 and L7 load balancing with one use case each.
6. A CDN has edge latency 15 ms, origin latency 180 ms and a 95% hit ratio. Compute the mean latency and origin offload.
