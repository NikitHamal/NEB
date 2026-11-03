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

## 4.7 Seeing the ideas: the physical network, a VPC, VXLAN packets and the CDN path

Every virtual network is carried by real fibre, switches and routers. Plate 4.1 shows the hardware that the diagrams in this section sit on.

```photogrid label="4.1" cols="3" ratio="1.1" caption="The physical network under a VPC. (a) Optical fibre: the long-distance carrier between data centres and across the sea to cloud regions. (b) A rack switch connecting servers inside the data centre. (c) A router forwarding packets by longest-prefix match, the same rule a VPC route table applies in software."
@ photo id="bca101/fibre-cable" cap="Optical fibre cable"
fit 1.1
focus 0.5 0.5
@ photo id="bca306/switch" cap="Data-centre switch"
fit 1.1
focus 0.5 0.5
@ photo id="bca101/router" cap="Router"
fit 1.1
focus 0.5 0.5
```

```svgfig label="4.1" caption="A VPC 10.0.0.0/16 with two availability zones. Public subnets route to the internet gateway; web servers sit behind a load balancer. Private subnets hold the database and reach the internet only through a NAT gateway placed in a public subnet. Security groups guard each tier."
f = Fig(580, 270)
f.box(4, 4, 572, 262, "", fill="#f8fafc", stroke=NAVY)
f.text(100, 18, "VPC 10.0.0.0/16 (one region)", size=10.5, color=NAVY, bold=True)
f.box(240, 28, 100, 28, "Internet gateway", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.text(345, 70, "Internet", size=10, color=SLATE)
f.box(14, 78, 270, 80, "", fill="#ecfdf5", stroke=TEAL)
f.box(296, 78, 270, 80, "", fill="#ecfdf5", stroke=TEAL)
f.text(149, 92, "Public 10.0.1.0/24 (AZ-a)", size=9.5, color=TEAL, bold=True)
f.text(431, 92, "Public 10.0.2.0/24 (AZ-b)", size=9.5, color=TEAL, bold=True)
f.box(24, 102, 100, 40, "Web server\nSG: allow 443", fill=MINT, stroke=TEAL, size=9)
f.box(160, 102, 110, 40, "NAT gateway", fill=SAND, stroke=AMBER, size=9.5)
f.box(306, 102, 100, 40, "Web server\nSG: allow 443", fill=MINT, stroke=TEAL, size=9)
f.box(14, 176, 270, 80, "", fill="#fff1f2", stroke=RED)
f.box(296, 176, 270, 80, "", fill="#fff1f2", stroke=RED)
f.text(149, 190, "Private 10.0.11.0/24 (AZ-a)", size=9.5, color=RED, bold=True)
f.text(431, 190, "Private 10.0.12.0/24 (AZ-b)", size=9.5, color=RED, bold=True)
f.box(24, 202, 120, 40, "Database primary\nSG: allow 5432 from web", fill=ROSE, stroke=RED, size=8.5)
f.box(306, 202, 120, 40, "Database standby\nSG: allow 5432 from web", fill=ROSE, stroke=RED, size=8.5)
f.arrow([(290, 56), (290, 78)], both=True)
f.arrow([(215, 142), (215, 160), (215, 160)], dash=True)
f.arrow([(84, 202), (84, 142)], dash=True, label="", lpos=(100, 170))
f.text(290, 169, "private subnets reach the internet only via the NAT gateway", size=9, color=SLATE)
```

```svgfig label="4.2" caption="A VXLAN packet to scale. The tenant's Ethernet frame is wrapped in a new outer Ethernet, IPv4, UDP and VXLAN header between two physical hosts. The added 50 bytes (20 + 8 + 8 + 14) are why the tenant MTU falls to 1450 when the physical network carries 1500."
f = Fig(580, 170)
parts = [("Outer\nEth", 14, SLATE, "#e2e8f0"), ("Outer IPv4\n20 B", 20, AMBER, SAND), ("UDP\n8 B", 8, RED, ROSE), ("VXLAN\n8 B", 8, RED, ROSE), ("Inner Eth\n14 B", 14, TEAL, MINT), ("Tenant IP packet (up to 1450 B)", 120, NAVY, BLUE)]
x = 10
for t, n, st, fl in parts:
    w = n * 4 if n < 100 else 300
    f.box(x, 40, w, 44, t, fill=fl, stroke=st, size=8.5, bold=True)
    x += w
f.text(290, 24, "added by the overlay (50 bytes; outer Ethernet is 14 B more)", size=9.5, color=RED, bold=True)
f.text(290, 110, "VNI (24 bits) = tenant network ID: 2^24 = 16,777,216 separate tenant networks", size=10, color=NAVY, bold=True)
f.text(290, 130, "Compare VLAN: only 12 bits = 4,096 networks", size=10, color=SLATE)
f.text(290, 154, "Physical MTU 1500 - 50 = tenant MTU 1450", size=10.5, color=TEAL, bold=True)
```

```svgfig label="4.3" caption="The request path with a load balancer and a CDN. A user in Pokhara is sent by DNS to the nearest CDN edge. On a cache hit the edge answers at once; on a miss it asks the load balancer, which picks a healthy server using its algorithm, and the response is cached for the next user."
f = Fig(580, 190)
f.box(8, 66, 76, 44, "User\nPokhara", fill=SAND, stroke=AMBER, bold=True, size=10)
f.box(130, 66, 96, 44, "CDN edge\nKathmandu", fill=MINT, stroke=TEAL, bold=True, size=10)
f.box(290, 66, 90, 44, "Load\nbalancer", fill=BLUE, stroke=NAVY, bold=True, size=10)
for i in range(3):
    f.box(450, 14 + i * 56, 120, 40, ["Server 1 (healthy)", "Server 2 (healthy)", "Server 3 (failed)"][i], fill=[MINT, MINT, "#e2e8f0"][i], stroke=[TEAL, TEAL, SLATE][i], size=9.5)
    f.arrow([(380, 88), (450, 34 + i * 56)], dash=(i == 2), color=[NAVY, NAVY, RED][i])
f.arrow([(84, 88), (130, 88)], both=True)
f.arrow([(226, 88), (290, 88)], label="miss", lpos=(258, 78))
f.text(178, 130, "hit: reply in ~10 ms", size=9.5, color=TEAL, bold=True)
f.text(178, 146, "miss: fetch, cache, reply", size=9.5, color=SLATE)
f.text(415, 178, "health checks skip the failed server", size=9.5, color=RED)
f.text(70, 170, "DNS routes to the nearest edge", size=9.5, color=SLATE)
```

### 4.7.1 Eight benefits of a CDN and load balancer

1. **Lower latency.** A CDN serves content from an edge near the user. A video watched in Pokhara comes from Kathmandu or Mumbai instead of a far-away origin. Pages load faster and viewers stay longer.
2. **Less load on the origin.** Cached files never reach the main servers, so they handle only new or dynamic requests. A college site can survive result day with one small server. The origin bill also falls.
3. **Higher availability.** A load balancer sends traffic only to servers that pass health checks. If one server fails, users do not notice. The same idea works across availability zones.
4. **Smooth scaling.** New servers join the pool behind the same address, and old ones leave. Autoscaling and load balancing work together. The users always see one stable name.
5. **Protection against attacks.** Edge networks absorb floods of traffic and filter bad requests before they reach the origin. A web application firewall can sit on the CDN. This protects small sites from denial-of-service attempts.
6. **TLS termination.** The balancer or edge handles HTTPS certificates and encryption in one place. Servers behind it can focus on the application. Renewing a certificate becomes a single task.
7. **Bandwidth saving.** Edge servers compress images and files and reuse them for many users. The cost of data transfer out of the cloud falls. This matters when international bandwidth is expensive.
8. **Better user experience worldwide.** Latency-based and geographic DNS routing send each user to the best location. Nepali users in Kathmandu, Doha and Sydney all get a quick response. A single global service feels local everywhere.

## 4.8 Summary and exercises

A VPC gives tenants private subnets with stateful and stateless firewalls; CIDR arithmetic plans address space; VXLAN overlays cost 50 bytes per packet and reduce tenant MTU; load balancers and CDNs raise availability and cut latency.

1. Differentiate a security group from a network ACL.
2. How many usable addresses does a /20 subnet offer if five are reserved? How many /26 subnets fit in a /22?
3. Compute the inner MTU for a 1,600-byte underlay with VXLAN, and explain what happens to a 1,500-byte tenant packet.
4. Trace smooth WRR for weights 3:1 over four picks.
5. Compare L4 and L7 load balancing with one use case each.
6. A CDN has edge latency 15 ms, origin latency 180 ms and a 95% hit ratio. Compute the mean latency and origin offload.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain a Virtual Private Cloud (VPC). Distinguish public and private subnets, and security groups from network ACLs.**

*Introduction.* A **VPC** is a logically isolated virtual network in a cloud region where the customer chooses the private IP range, subnets, routes and firewalls (Figure 4.1).

*Subnets.* A **public subnet** has a route to the internet gateway, so its instances can have public addresses (for example web servers and load balancers). A **private subnet** has no inbound route from the internet; outbound traffic, such as software updates, goes through a **NAT gateway** in a public subnet (for example the database).

| Point | Security group | Network ACL |
|---|---|---|
| Attached to | Instance | Subnet |
| State | Stateful (replies allowed) | Stateless (both ways needed) |
| Rules | Allow only | Allow and deny, ordered |
| Evaluated | All rules together | In number order |

*Example.* A college portal puts two web servers in public subnets and the student database in a private subnet that accepts connections on port 5432 only from the web servers' security group. *Conclusion:* subnets divide the network by exposure and firewalls enforce least privilege at two levels.

**Q2 (5 marks). Explain load balancing: its purpose, algorithms and health checks.**

A **load balancer** spreads incoming requests over several servers to improve capacity, availability and response time.

1. **Round robin.** Requests go to servers in turn; simple and fair when requests are alike.
2. **Weighted round robin.** Bigger servers receive proportionally more requests.
3. **Least connections.** The next request goes to the server with the fewest active connections, which suits long sessions.
4. **IP hash.** The client address decides the server, so one user keeps reaching the same one (session stickiness).
5. **Layer 4 or Layer 7.** A Layer 4 balancer routes by IP and port; a Layer 7 balancer reads HTTP and can route by URL path or host name.

**Health checks** call each server regularly (for example GET /health every 10 seconds) and remove any server that fails several times (Figure 4.3). *Example:* an exam-result site with four web servers keeps working when one crashes. *Conclusion:* load balancing gives horizontal scaling and fault tolerance behind one address.

**Q3 (10 marks). Describe how a cloud provider builds tenant networks. Explain VPC addressing, VXLAN overlay networks, load balancing and content delivery networks.**

*Introduction.* Thousands of tenants share one physical network but each sees a private one. The provider achieves this with addressing, tunnelling and traffic distribution (Plate 4.1 shows the hardware beneath).

*1. VPC addressing and CIDR.* A tenant picks an RFC 1918 range such as 10.0.0.0/16 and divides it into subnets. A prefix /p has 2^(32-p) addresses, so a /16 holds 65,536 and splits into 256 subnets of /24. Providers reserve five addresses per subnet, so a /24 gives 251 usable hosts and a /26 gives 59. Ranges that overlap cannot be peered, so address planning comes first (Figure 4.1).

*2. Overlay networks and VXLAN.* Different tenants use the same private addresses, so the host's virtual switch encapsulates each tenant Ethernet frame inside a UDP packet between physical hosts. The VXLAN header carries a 24-bit VNI, giving 16,777,216 isolated networks compared with 4,096 for VLANs. The wrapper adds 50 bytes, so the tenant MTU is 1500 - 50 = 1450 (Figure 4.2).

*3. Load balancing.* A load balancer in front of a server pool uses round robin, least connections or hashing, and removes failed servers using health checks. Layer 7 balancers can route by URL and terminate TLS.

*4. CDN.* Static content is cached at edge locations near users; DNS or anycast routing sends the user to the nearest edge. A hit is answered locally, a miss is fetched from the origin and stored (Figure 4.3). This cuts latency, origin load and bandwidth cost.

*5. DNS routing.* Weighted, latency-based, geographic and failover policies send users to the best region, or away from a failed one.

| Layer | Technique | Purpose |
|---|---|---|
| Address | CIDR, subnets | Plan and isolate |
| Tenant isolation | VXLAN, VNI | Separate customers |
| Distribution | Load balancer | Capacity and availability |
| Delivery | CDN, DNS routing | Low latency worldwide |

*Conclusion.* The customer's simple VPC is the surface of several layers: careful CIDR planning, VXLAN tunnels for isolation, load balancers for resilience and a CDN for speed. Good design plans addresses early, keeps databases in private subnets and spreads servers across zones.
