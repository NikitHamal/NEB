---
subject: Network Administration
grade: BCA Semester 8 (Elective III)
unit: 3
title: Infrastructure
hours: 16
area: BCA 453 · Network Administration · Unit 3
---

Servers and workstations are only as useful as the network that joins them, and the network is only as dependable as the rooms and power that hold it. This unit covers the three layers of infrastructure: the **architecture** of the network (wired, wireless, wide-area, routing and internet access), its **day-to-day operation** (documentation, monitoring, configuration control, security), and the **data centre** that houses the servers and the equipment.

::: key What this unit gives you
- Network architecture: the layer models, structured cabling, the access-distribution-core design, VLANs, wireless planning, data-centre spine-leaf, WAN strategies, routing choices, internet access with NAT and a DMZ, and an addressing plan worked by program.
- Network operations: documentation, monitoring protocols, configuration backup, change control, firewall rules and a troubleshooting toolkit.
- Data centres: tiers, site and building, power, cooling and PUE, racks and cabling, fire and physical security, and the routines for running one.
:::

## 3.1 Network architecture

### 3.1.1 Physical and logical networks, and the layer models

A **physical network** is the cables, devices and rooms; a **logical network** is the set of addresses, VLANs and routes laid on top. The two should be designed separately: one cable plant can carry many logical networks, and one logical network can span many buildings. The **OSI model** (seven layers) and the **TCP/IP model** (four layers) give names to the parts, which help in design and in finding faults.

| OSI layer | Examples | Device | Typical fault |
|---|---|---|---|
| 7 Application | HTTP, DNS, SMTP | Proxy, load balancer | Service misconfigured |
| 4 Transport | TCP, UDP ports | Firewall | Port blocked |
| 3 Network | IP, routing | **Router**, layer-3 switch | Wrong gateway or route |
| 2 Data link | Ethernet, VLAN, Wi-Fi | **Switch**, access point | Loop, wrong VLAN |
| 1 Physical | Cable, fibre, radio | Cable, hub, repeater | Broken cable, bad connector |

The administrator's habit is to **test from the bottom**: link light (layer 1), VLAN and MAC (2), IP and gateway (3), port (4), service (7).

### 3.1.2 Wired office networks

**Structured cabling** treats the building's cabling as permanent infrastructure, planned to last 15 to 20 years and independent of the equipment. A **star topology** runs a cable from each outlet to a **wiring closet** (IDF, intermediate distribution frame) on each floor, and fibre links join the closets to the **main distribution frame (MDF)** or equipment room. Rules to remember for Ethernet over twisted pair: a **horizontal run is at most 90 m** (100 m channel with patch cords); use Cat 6 or Cat 6A for new work (Cat 5e is the minimum); label both ends and every patch panel port; keep copper away from power cables and fluorescent ballasts; use **fibre between buildings** (immune to lightning and ground-potential differences) and for backbones.

**The three-tier hierarchical design** splits a large campus network into layers with different jobs:

| Layer | Role | Characteristics |
|---|---|---|
| **Access** | Connects users, phones, access points, printers | Many ports, PoE, port security, VLAN assignment |
| **Distribution** | Aggregates the access switches of a building or floor; applies policy | Layer-3 routing between VLANs, ACLs, redundancy |
| **Core** | Fast backbone between distribution blocks, servers and the internet edge | High throughput, no policy, redundant, simple |

A small college does not need three tiers; a **collapsed core** (distribution and core in the same pair of switches) is the usual design for up to a few hundred users. In either case give each tier **redundant links**; because redundant Ethernet paths create loops, switches run **spanning tree (STP, RSTP)** or use link aggregation (LACP) so that the loop is blocked until a link fails.

```svgfig label="3.1" caption="A collapsed-core campus network with VLANs: redundant uplinks, a layer-3 core pair and a firewall to the internet."
f = Fig(680, 290)
f.box(255, 15, 170, 40, "Firewall + router\nto ISP", fill=SAND, stroke=AMBER, size=10)
f.box(150, 90, 140, 40, "Core switch 1\n(layer 3)", fill=BLUE, stroke=NAVY, size=10)
f.box(390, 90, 140, 40, "Core switch 2\n(layer 3)", fill=BLUE, stroke=NAVY, size=10)
f.box(10, 190, 130, 45, "Access switch A\nVLAN 10 staff", fill=SOFT, stroke=SLATE, size=10)
f.box(190, 190, 130, 45, "Access switch B\nVLAN 20 labs", fill=SOFT, stroke=SLATE, size=10)
f.box(360, 190, 130, 45, "Access switch C\nVLAN 30 Wi-Fi", fill=SOFT, stroke=SLATE, size=10)
f.box(540, 190, 130, 45, "Server switch\nVLAN 40 servers", fill=SOFT, stroke=SLATE, size=10)
f.arrow([(290, 110), (390, 110)], color=NAVY, both=True, label="LACP", lpos=(340, 102))
f.arrow([(300, 55), (240, 90)], color=NAVY)
f.arrow([(380, 55), (440, 90)], color=NAVY)
for x in (75, 255, 425, 605):
    f.arrow([(x, 190), (200, 130)], color=SLATE, both=True)
    f.arrow([(x + 10, 190), (440, 130)], color=SLATE, both=True, dash=True)
f.text(340, 265, "Every access switch has two uplinks (solid active, dashed standby under STP).", size=9, color=SLATE)
```

**VLANs.** A **virtual LAN** divides one physical switch network into several separate broadcast domains. Benefits: security (labs cannot reach the staff network except through the router and its rules), smaller broadcast domains and flexible placement. Ports are **access ports** (one VLAN) or **trunk ports** (carry several VLANs tagged by IEEE 802.1Q). Traffic between VLANs must pass through a router (or layer-3 switch), which is where the firewall rules are applied. Keep a VLAN plan and match one VLAN to one IP subnet.

**Power over Ethernet (PoE, 802.3af/at/bt)** delivers 15.4, 30 or up to 60-90 W over the data cable, and removes separate power for access points, phones and cameras; budget the switch's total PoE power.

### 3.1.3 Wireless office networks

Wi-Fi (IEEE 802.11) is the access network for most users, so its design is as important as the wired one. Principles:

- **Plan with a site survey** (predictive or with a survey tool): walls, concrete and lifts weaken signals, and coverage is judged by signal strength (about -65 dBm or better in the area users work) and by capacity, not only by reach.
- **Many small cells beat one big one.** A cell shares its airtime between its users; a lecture hall of 100 students needs several access points, not one strong one.
- **Channels.** 2.4 GHz has only three non-overlapping channels (1, 6, 11); 5 GHz and 6 GHz have many more. Use 20 or 40 MHz channels in dense areas, and reuse channels so that neighbouring access points differ.
- **One SSID per purpose** (staff, guest), mapped to VLANs; too many SSIDs waste airtime.
- **Security**: WPA2 or WPA3; for staff use **WPA2/WPA3-Enterprise with 802.1X** and a RADIUS server so that each person has an own credential, never a shared key; guests are isolated with a captive portal and internet-only access.
- **Management**: a **controller** or cloud management configures all access points consistently, supports roaming and shows interference.
- **Cabling**: access points are cabled and powered by PoE, with a cable run of at most 90 m.

### 3.1.4 Data-centre networks

Inside a data centre most traffic flows **east-west** (server to server) rather than north-south (to the outside). The classic tree of three tiers makes the paths between servers uneven, so large sites use a **leaf-spine** (Clos) design: every **leaf** switch (at the top of a rack) connects to every **spine** switch; any two servers on different racks are always the same two hops apart, and capacity is raised by adding spines.

```svgfig label="3.2" caption="Leaf-spine data-centre network: every leaf connects to every spine, so all rack-to-rack paths have equal length."
f = Fig(640, 230)
for i, x in enumerate((130, 310, 490)):
    f.box(x - 55, 20, 110, 36, "Spine %d" % (i + 1), fill=BLUE, stroke=NAVY, size=10)
for j, x in enumerate((60, 200, 340, 480, 600)):
    f.box(x - 45, 120, 90, 36, "Leaf %d" % (j + 1), fill=SOFT, stroke=SLATE, size=10)
    f.box(x - 45, 185, 90, 30, "Rack %d" % (j + 1), fill=SAND, stroke=AMBER, size=9)
    f.arrow([(x, 156), (x, 185)], color=SLATE)
    for sx in (130, 310, 490):
        f.line(sx, 56, x, 120, color=NAVY, sw=1)
```

### 3.1.5 WAN strategies

A **WAN** joins sites that are far apart: a head office and branches, a college and its campuses, a bank and its ATMs.

| Option | Description | Advantages | Limits |
|---|---|---|---|
| **Leased line** | Dedicated point-to-point circuit from a carrier | Predictable, private, SLA | Costly, slow to install |
| **MPLS VPN** | The carrier's private network with labels separating customers | Quality of service, any-to-any | Costly, carrier lock-in |
| **Internet + IPsec VPN** | Ordinary internet links with encrypted tunnels | Cheap, quick | No guaranteed quality, depends on ISP |
| **SD-WAN** | Policy-based use of several links, centrally managed | Resilient, uses cheap links well | Needs a vendor or platform |
| **Metro Ethernet / fibre** | Ethernet service within a city | High speed, simple | Local availability |
| **Wireless (microwave, 4G/5G)** | Radio links | Fast to deploy, backup | Weather, interference, data caps |

Topologies: **hub-and-spoke** (all branches connect to the centre: simple, cheap, centre is critical), **full mesh** (every site to every site: n(n-1)/2 links, best paths, costly) and **partial mesh**. For a bank with 12 branches the full mesh needs 66 tunnels, hub-and-spoke only 12. A sensible design uses **two independent links from different providers** to each important site.

### 3.1.6 Routing

Routers choose the next hop for each packet from a **routing table**.

| Kind | How routes arrive | Use |
|---|---|---|
| **Connected** | Interface addresses | Automatic |
| **Static** | Typed by the administrator, for example `ip route 10.20.0.0 255.255.0.0 192.168.1.2` | Small networks, default route to the ISP, stub sites |
| **Dynamic** | Learnt from neighbours by a protocol | Larger and changing networks |

Dynamic **interior** protocols: **RIP** (distance vector, hop count, simple, slow, limit of 15 hops), **OSPF** (link-state, builds a map, fast convergence, areas, the usual choice in enterprises) and **EIGRP** (Cisco). The **exterior** protocol of the internet is **BGP**, used between autonomous systems and by an organisation that connects to two ISPs with its own address block. The router picks the route with the **longest prefix match** first; ties are decided by administrative distance and metric. A small network usually needs only connected routes, one **default route** (`0.0.0.0/0`) towards the ISP and a few static routes.

### 3.1.7 Internet access, NAT and the DMZ

An organisation reaches the internet through one or more ISPs. The usual edge has:

- **A firewall** that applies a default-deny policy: allow inside-to-outside, allow outside only to published services.
- **NAT** (network address translation, usually many-to-one PAT): private RFC 1918 addresses (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) are rewritten to one public address, which conserves public addresses and hides the inside structure. NAT is not a security mechanism by itself; the firewall is.
- **A DMZ (demilitarised zone)**: a separate segment for servers that must be reachable from outside (web, mail gateway, DNS). If a DMZ server is compromised, the attacker is still outside the internal network.
- **Multihoming**: two ISPs, with a failover or load-sharing policy, so that a single provider outage does not stop the organisation.
- **Proxy, content filter and bandwidth control** for web access, and a **VPN gateway** for remote users.

### 3.1.8 An addressing plan

Plan addresses before buying switches. Use one private block, split by function and site, with room for growth and a rule that is easy to remember.

```python
import ipaddress
block = ipaddress.ip_network("10.20.0.0/16")        # whole college
plan = [("Staff", 200), ("Labs", 400), ("Wi-Fi", 1000), ("Servers", 60), ("Management", 30), ("Guests", 500)]
nets = list(block.subnets(new_prefix=24))           # candidate /24 blocks
print("%-11s %5s %-16s %-14s %s" % ("VLAN", "hosts", "subnet", "mask", "usable"))
start = 0
for name, hosts in sorted(plan, key=lambda x: -x[1]):
    # smallest prefix that holds the hosts plus gateway and 25% growth
    need = int(hosts * 1.25) + 3
    bits = (need - 1).bit_length()
    prefix = 32 - bits
    net = ipaddress.ip_network((int(block.network_address) + start, prefix))
    start += net.num_addresses
    print("%-11s %5d %-16s %-14s %d" % (name, hosts, net, net.netmask, net.num_addresses - 2))
print("used %d of %d addresses in %s" % (start, block.num_addresses, block))
```

Subnets are allocated from the largest to the smallest so that each block starts on its own boundary. The same arithmetic is done by hand in the exam: a /23 has 512 addresses and 510 hosts; a /26 has 64 addresses and 62 hosts.

