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
```output
VLAN        hosts subnet           mask           usable
Wi-Fi        1000 10.20.0.0/21     255.255.248.0  2046
Guests        500 10.20.8.0/22     255.255.252.0  1022
Labs          400 10.20.12.0/23    255.255.254.0  510
Staff         200 10.20.14.0/24    255.255.255.0  254
Servers        60 10.20.15.0/25    255.255.255.128 126
Management     30 10.20.15.128/26  255.255.255.192 62
used 4032 of 65536 addresses in 10.20.0.0/16
```
Subnets are allocated from the largest to the smallest so that each block starts on its own boundary. The same arithmetic is done by hand in the exam: a /23 has 512 addresses and 510 hosts; a /26 has 64 addresses and 62 hosts.

## 3.2 Network operations

Building a network is a project; **operating** it is the job that never ends. Operations means the routines that keep the network known, observed, controlled and secure.

### 3.2.1 Documentation

Documentation is the memory of the network. Without it, knowledge lives in one person's head and leaves when that person does. Keep, at least:

| Document | Contents |
|---|---|
| **Network diagrams** | Physical (buildings, closets, links, speeds) and logical (VLANs, subnets, routing, firewall zones) |
| **Address and VLAN plan** | Subnet, VLAN number, gateway, DHCP range, purpose, owner |
| **Inventory** | Each device: model, serial, location, firmware, warranty end, purpose |
| **Cable and port records** | Patch-panel port to switch port, outlet number and room |
| **Configuration archive** | Current and previous configuration of every device |
| **Runbooks** | Step-by-step procedures: restart a service, replace a switch, add a user |
| **Contacts and escalation** | ISP support number, circuit IDs, vendor contract numbers, on-call list |

Keep it in a **wiki** or document system that is backed up and reachable even when the network is down (a printed copy of the essential pages, in the equipment room, is not old-fashioned). Make updating the document part of the change itself: a change is not finished until the document is changed. Label cables, ports and devices physically, because a diagram that disagrees with the wall is worse than none.

### 3.2.2 Monitoring

You cannot manage what you cannot see, and customers should never be the monitoring system. Monitoring answers: is it up, is it healthy, is it filling up, is it being attacked.

| Mechanism | What it does |
|---|---|
| **Ping / ICMP, TCP checks** | Is the device or port reachable? |
| **SNMP** (v2c, preferably v3) | Polls counters (interface traffic, errors, CPU, temperature) and receives **traps** |
| **Syslog** | Devices send log messages to a central log server |
| **NetFlow / sFlow / IPFIX** | Summaries of who talks to whom, for capacity and incident analysis |
| **Synthetic checks** | A script that logs in and sends a test mail, to check the service the way a user does |
| **Dashboards and alerts** | Graphs of trends and rules that notify a person |

Tools: Nagios, Zabbix, LibreNMS, Prometheus with Grafana, PRTG, and cloud monitors. Good practice:

- Monitor **services as seen by users**, and also the devices and links beneath them.
- Alert only on what needs **action**; too many alarms teach people to ignore all alarms (alert fatigue).
- Set thresholds with a margin (disk 80% warning, 90% critical) and watch **trends**, not only current values.
- Store history to plan capacity: a link that peaks at 70% in March will not survive examination season next year.
- Monitor the monitor, and keep it independent from what it watches.

The utilisation of a link from two SNMP counter readings is a routine calculation:

```python
# Link utilisation from two readings of an SNMP interface octet counter
interval_s = 300
octets_t0, octets_t1 = 1_200_000_000, 1_950_000_000
link_bps = 100_000_000          # a 100 Mbit/s link
bits = (octets_t1 - octets_t0) * 8
bps = bits / interval_s
print("traffic over 5 min : %.1f Mbit/s" % (bps / 1e6))
print("utilisation        : %.1f %%" % (100 * bps / link_bps))
# a 32-bit counter wraps at 2**32; use the 64-bit counter (ifHCInOctets) on fast links
wrap = 2 ** 32
t0, t1 = 4_200_000_000, 150_000_000       # counter rolled over between the readings
delta = (t1 - t0) % wrap
print("delta after wrap   :", delta, "octets")
```
```output
traffic over 5 min : 20.0 Mbit/s
utilisation        : 20.0 %
delta after wrap   : 244967296 octets
```
### 3.2.3 Configuration management and change control

Every network device has a configuration; unrecorded changes are the commonest source of outages. Practice:

1. **Back up configurations automatically** after every change (a scheduled job or a tool such as RANCID, Oxidized or Ansible) and store them in **version control** so that you can see who changed which line and roll back.
2. **Use templates and standards**: all access switches share one template differing only by name, address and VLANs.
3. **Change control**: a written request describing what, why, risk, test and **back-out plan**; review by a second person; a planned **maintenance window**; notification to users; verification after the change; update of documentation.
4. **Test first** on a lab or lower-risk device; change one thing at a time; keep a console path (out-of-band access) so that a mistake in remote configuration does not need a drive to the site.
5. **Emergency changes** are allowed but written up afterwards.
6. **Firmware and patching**: follow vendor security advisories; upgrade in stages.

### 3.2.4 Core network services: DHCP and DNS

**DHCP** assigns addresses, gateway, DNS servers and lease times automatically. Use **reservations** (by MAC address) for printers and devices that must keep an address; keep servers on static addresses outside the DHCP range. **DNS** converts names to addresses and is the dependency of nearly everything, so run **at least two DNS servers** on different hosts. A small Linux example with `dnsmasq` serves both:

```ini
# /etc/dnsmasq.d/lab.conf   (not run in the build sandbox)
interface=eth1
domain=lab.college.edu.np
dhcp-range=10.20.20.50,10.20.20.200,255.255.255.0,12h
dhcp-option=option:router,10.20.20.1
dhcp-option=option:dns-server,10.20.20.2
dhcp-host=00:1a:2b:3c:4d:5e,printer1,10.20.20.10
address=/gw.lab.college.edu.np/10.20.20.1
```

The namespace design for DNS and directories is dealt with in Unit 4.

### 3.2.5 Network security operations

- **Segmentation**: separate VLANs for staff, labs, servers, guests and management, with the router or firewall allowing only the flows that are needed.
- **Firewall rules** are evaluated **top to bottom, first match wins**, ending with an implicit or explicit *deny all*. Put specific rules before general ones; comment each rule with its purpose and owner; review them yearly and remove stale ones.
- **Access to devices**: SSH not Telnet, individual accounts via TACACS+/RADIUS, a management VLAN, MFA for administrators, disabled unused ports.
- **Layer-2 protections**: port security, DHCP snooping, BPDU guard, disabled unused trunk negotiation.
- **Logging and review**: log denied traffic and administrator logins; review regularly.

The following program shows first-match evaluation, the idea behind every ACL.

```python
import ipaddress as ip
rules = [  # (action, source net, destination net, port or None = any)
    ("deny",   "10.20.20.0/24", "10.20.40.0/24", None),   # labs -> servers (blocked)
    ("permit", "10.20.20.0/24", "10.20.40.10/32", 443),   # labs -> web server only (never reached, shadowed)
    ("permit", "10.20.10.0/24", "10.20.40.0/24", None),   # staff -> servers
    ("permit", "0.0.0.0/0",     "0.0.0.0/0",     80),     # anyone -> web
    ("deny",   "0.0.0.0/0",     "0.0.0.0/0",     None),   # default deny
]
def check(src, dst, port):
    for n, (act, s, d, p) in enumerate(rules, 1):
        if ip.ip_address(src) in ip.ip_network(s) and ip.ip_address(dst) in ip.ip_network(d) and p in (None, port):
            return act, n
tests = [("10.20.10.5", "10.20.40.7", 22), ("10.20.20.9", "10.20.40.10", 443),
         ("10.20.20.9", "8.8.8.8", 80), ("10.20.20.9", "8.8.8.8", 25)]
for t in tests:
    print("%-12s -> %-12s port %-3d : %s by rule %d" % (t[0], t[1], t[2], *check(*t)))
```
```output
10.20.10.5   -> 10.20.40.7   port 22  : permit by rule 3
10.20.20.9   -> 10.20.40.10  port 443 : deny by rule 1
10.20.20.9   -> 8.8.8.8      port 80  : permit by rule 4
10.20.20.9   -> 8.8.8.8      port 25  : deny by rule 5
```
The second rule can never match because rule 1 already denies the same traffic; this **shadowing** is a common firewall error. The administrator corrects it by putting the specific *permit* above the general *deny*.

### 3.2.6 The troubleshooting toolkit

| Task | Linux | Windows |
|---|---|---|
| Local addresses and links | `ip addr`, `ip link`, `ethtool` | `ipconfig /all` |
| Reachability | `ping`, `ping -6` | `ping` |
| Path | `traceroute`, `mtr` | `tracert`, `pathping` |
| DNS | `dig name`, `nslookup` | `nslookup`, `Resolve-DnsName` |
| Open ports and sockets | `ss -tulpn` | `netstat -ano`, `Test-NetConnection host -Port 443` |
| Routing table, ARP | `ip route`, `ip neigh` | `route print`, `arp -a` |
| Packet capture | `tcpdump -i eth0 port 53`, Wireshark | Wireshark, `pktmon` |
| Throughput | `iperf3` | `iperf3` |

::: example A user cannot open the college website
1. `ipconfig` shows address 169.254.12.7: the PC got no DHCP lease (APIPA). Layer 3 is wrong before anything else.
2. The link light is on and the VLAN is correct, so check the DHCP scope: it shows all 200 addresses leased, the pool is **exhausted** by phones and guests.
3. Fix: shorten the lease time on the Wi-Fi VLAN to one hour and enlarge the pool from /24 to /23 in the next window; document the change.
4. Verify: new lease, `ping` the gateway, `nslookup www.college.edu.np`, open the site.
Root cause (address exhaustion), not the symptom (no site), was fixed, and the monitoring now alerts at 80% pool use.
:::

## 3.3 Data centres

### 3.3.1 Overview

A **data centre** is a facility built to house servers, storage and network equipment with **controlled power, cooling, security and connectivity**. It may be a locked, air-conditioned room in a college (a *server room*), a purpose-built building owned by a bank or telecom, a **colocation** facility where you rent racks, or the cloud provider's data centre that you never see. The decision between building, renting and using cloud is a matter of cost, control, skills and risk: an organisation with a few servers often does better with colocation or cloud than with a poorly cooled room and a single power line.

**Tiers.** The Uptime Institute classification describes the design's redundancy, and gives rough availability targets:

| Tier | Design | Availability | Downtime per year |
|---|---|---|---|
| I | Basic capacity, single path, no redundancy | 99.671% | about 28.8 h |
| II | Redundant components, single path | 99.741% | about 22 h |
| III | Concurrently maintainable: any component can be maintained without shutdown | 99.982% | about 1.6 h |
| IV | Fault tolerant: survives any single failure, compartmentalised | 99.995% | about 26 min |

```python
hours = 365 * 24
for tier, a in (("I", 99.671), ("II", 99.741), ("III", 99.982), ("IV", 99.995)):
    d = hours * (100 - a) / 100
    print("Tier %-3s %.3f%% -> %.1f h (%.0f min) per year" % (tier, a, d, d * 60))
```
```output
Tier I   99.671% -> 28.8 h (1729 min) per year
Tier II  99.741% -> 22.7 h (1361 min) per year
Tier III 99.982% -> 1.6 h (95 min) per year
Tier IV  99.995% -> 0.4 h (26 min) per year
```
### 3.3.2 Site and building

Choose and prepare the site with the failures in mind:

- **Location**: away from flood plains, from the basement (water) and the top floor (roof leaks and heat), from large windows, and from fuel stores. In earthquake country (Nepal) use bracing of racks to the floor or seismic racks, and avoid heavy loads on weak floors.
- **Structure**: raised floor or overhead trays for cables; floor load capacity for loaded racks (a full rack can exceed 800 kg); a door wide enough for racks; separate fire compartment.
- **Connectivity**: **two entry paths** for fibre, from **two carriers**, so a single digger cannot cut both.
- **Utilities**: two power feeds if available, a generator and fuel contract, water for cooling if used.

### 3.3.3 Power

Power is the most common cause of data-centre failures, so the chain is designed with redundancy.

1. **Utility feed(s)** enter through an **automatic transfer switch (ATS)**.
2. **UPS (uninterruptible power supply)** carries the load for minutes on batteries and cleans the power; **online (double-conversion)** UPS units are used for servers.
3. A **diesel generator** takes over within about 10-30 seconds and runs for hours or days on stored fuel.
4. **PDUs (power distribution units)** feed the racks, often as an **A feed and a B feed** from separate UPS paths; each server has two power supplies, one on each feed, so that a failure on one side or maintenance of the other does not stop it.
5. **Monitoring** of load per circuit, batteries and fuel; test the generator under load monthly and the whole transfer annually.

**Power budget per rack.** Never connect more than the circuit and cooling allow; if both feeds are used, each feed must carry the whole rack alone when the other fails. Typical enterprise racks are 3-8 kW; high-density racks exceed 15 kW.

### 3.3.4 Cooling and PUE

All power consumed by IT equipment is released as heat, and servers shut down when they overheat. Cooling methods: **CRAC/CRAH units** (computer-room air conditioners) with a raised floor, in-row coolers, rear-door heat exchangers, and liquid cooling for very dense racks. The key technique is **hot-aisle/cold-aisle layout**: racks face each other so that the fronts (air intake) face a cold aisle and the backs (exhaust) face a hot aisle; blanking panels fill empty rack spaces, and the aisle is **contained** so that hot and cold air do not mix. Typical supply temperature recommended by ASHRAE is 18 to 27 degrees C at the server intake, with relative humidity kept within a moderate range to avoid static and condensation.

```svgfig label="3.3" caption="Hot-aisle / cold-aisle layout: cold air rises through perforated tiles in front of the racks; hot air leaves from the back and returns to the cooling unit."
f = Fig(640, 230)
f.box(20, 30, 70, 150, "CRAC\ncooling\nunit", fill=SAND, stroke=AMBER, size=10)
f.box(150, 30, 70, 90, "Rack\nrow A", fill=BLUE, stroke=NAVY, size=10)
f.box(340, 30, 70, 90, "Rack\nrow B", fill=BLUE, stroke=NAVY, size=10)
f.box(500, 30, 70, 90, "Rack\nrow C", fill=BLUE, stroke=NAVY, size=10)
f.text(280, 135, "COLD aisle", size=10, bold=True, color=NAVY)
f.text(445, 135, "HOT aisle", size=10, bold=True, color=RED)
f.text(120, 135, "hot aisle", size=9, color=RED)
f.arrow([(90, 190), (280, 190), (280, 150)], color=NAVY, label="cold air under raised floor", lpos=(200, 205))
f.arrow([(280, 118), (222, 80)], color=NAVY)
f.arrow([(280, 118), (338, 80)], color=NAVY)
f.arrow([(410, 40), (445, 15), (60, 15), (60, 30)], color=RED, label="warm air returns", lpos=(250, 8))
```

**PUE (power usage effectiveness)** measures the efficiency of the facility:

PUE = total facility power / IT equipment power.

A PUE of 1.0 would mean all power goes to IT; modern efficient sites reach 1.2-1.4, older rooms 2.0 or worse.

```python
it_kw = 40.0              # servers, storage, network
cooling_kw = 24.0
ups_loss_kw = 4.0
lighting_misc_kw = 2.0
total = it_kw + cooling_kw + ups_loss_kw + lighting_misc_kw
print("total %.1f kW  PUE = %.2f" % (total, total / it_kw))
rate = 14.0       # NPR per kWh, illustrative
yearly = total * 24 * 365 * rate
print("electricity per year: NPR %.1f million" % (yearly / 1e6))
better = it_kw * 1.4
print("at PUE 1.4 the saving is NPR %.1f million per year" % ((total - better) * 24 * 365 * rate / 1e6))
```
```output
total 70.0 kW  PUE = 1.75
electricity per year: NPR 8.6 million
at PUE 1.4 the saving is NPR 1.7 million per year
```
### 3.3.5 Racks, cabling and space

- **Racks** are 19-inch frames, 42U high typically; heavy equipment goes at the bottom; leave gaps for airflow and a rule that servers go front to back with the same airflow direction.
- **Cabling**: separate power from data; use overhead trays or under-floor trays; **label** both ends; use **colour codes** (for example blue for production, yellow for management, red for crossover or critical links); cable length as short as practical, with slack loops and Velcro ties, not nylon ties that crush cable.
- **Top-of-rack switches** per rack (leaf design) reduce cable runs; patch panels or fibre cassettes give a clean point of change.
- **Documentation**: a rack elevation (which device in which U), kept in an inventory or DCIM (data-centre infrastructure management) tool.

### 3.3.6 Fire protection, environment and physical security

| Risk | Control |
|---|---|
| **Fire** | Smoke detection (early warning aspirating detectors); **clean-agent gas** (for example FM-200 or inert gases) or pre-action sprinklers; never water-flood a live room; emergency power-off switch behind a cover; no cardboard or storage in the room |
| **Water** | No pipes over the room; leak sensors under raised floors; drains |
| **Temperature and humidity** | Sensors at rack intake, alarms to the monitoring system |
| **Dust and vibration** | Filters, sealed room, entry mat, no unpacking inside |
| **Unauthorised entry** | Locked door with badge or biometric access, CCTV, visitor log and escort, locked racks |
| **Theft or sabotage** | Cable locks, tamper-evident seals, asset checks |
| **Insiders** | Least-privilege physical access, two-person rule for critical areas, logs reviewed |

### 3.3.7 Running a data centre

Day-to-day running is routine and discipline:

1. **Access control and logs**: everyone entering is authorised and recorded; contractors are escorted.
2. **Change and maintenance**: all work follows change control (Section 3.2.3); maintenance of one power path or cooling unit is done while the other carries the load.
3. **Inventory and capacity**: track used and free U, power per rack, cooling, network ports; forecast when a limit will be reached and plan the extension before it is.
4. **Monitoring**: power, temperature, humidity, water, doors, UPS battery health and generator fuel feed the same alert system as the servers.
5. **Remote operation**: out-of-band management (IPMI/iDRAC/iLO) and a serial console server mean most work needs no visit; **remote hands** from the provider cover the rest.
6. **Housekeeping**: remove dead equipment (cooling and power go to machines nobody uses), keep floor and racks clean, label and tidy cables.
7. **Incident management**: runbooks for power loss, cooling failure, water leak and fire; **tests and drills**, including a planned failover of the UPS and generator; an after-action review for every incident, written without blame.
8. **Environmental and cost reporting**: PUE, energy use, e-waste handling.

::: caution The test that is never run
A generator that has not been started under load for a year may not start when the grid fails. The same is true of the UPS batteries (typical life 3-5 years) and of backup restores. Schedule these tests and record the date and result.
:::

## 3.4 Summary and exercises

Infrastructure has three layers. **Architecture**: structured star cabling with 90 m horizontal runs, access-distribution-core (or collapsed core) design, VLANs on 802.1Q trunks, planned Wi-Fi with 802.1X, leaf-spine data-centre fabrics, WAN options (leased line, MPLS, VPN, SD-WAN) with two independent links, static and dynamic routing (OSPF inside, BGP outside), a firewall with NAT and a DMZ at the edge, and an addressing plan allocated largest block first. **Operations**: documentation, monitoring with SNMP, syslog and flow data and sensible alerts, configuration backup under version control, change control with back-out plans, DHCP and DNS run redundantly, segmentation and ordered firewall rules, and a layered troubleshooting method. **Data centres**: choose a tier and site for the risk, power through UPS, generator and A/B feeds, cool with hot/cold aisles and measure PUE, organise racks and labelled cables, protect against fire, water and intruders, and run it with access control, capacity planning, monitoring and tested procedures.

1. Differentiate a physical network and a logical network. Why design them separately?
2. Explain structured cabling. State the maximum horizontal cable length and four good practices.
3. Describe the three-tier hierarchical network design. When is a collapsed core suitable?
4. What is a VLAN? Explain access ports, trunk ports and 802.1Q, and the benefits of VLANs.
5. State the principles of designing a wireless office network. Why use WPA2/WPA3-Enterprise?
6. Explain leaf-spine architecture and why it is used in data centres.
7. Compare leased line, MPLS VPN, internet VPN and SD-WAN for a bank with 12 branches. How many links does a full mesh need?
8. Compare static and dynamic routing; name interior and exterior routing protocols.
9. What are NAT and a DMZ? Draw an internet-edge design with two ISPs.
10. A college needs subnets for 200, 400, 1000 and 60 hosts. Choose the prefix lengths with 25% growth (use Section 3.1.8).
11. List the documents an administrator must keep and justify two of them.
12. Explain how SNMP, syslog and NetFlow are used in monitoring. What is alert fatigue?
13. Explain change control for a network device, including the back-out plan.
14. Why are firewall rules ordered? What is rule shadowing?
15. A user reports "internet not working". Describe your step-by-step troubleshooting.
16. Describe the Uptime tiers. What do power, cooling, fire protection and physical security each require in a data centre?
17. Define PUE. A site uses 90 kW in total, 60 kW of it by IT equipment. Compute the PUE. A link carried 900 MB more in 5 minutes than before (counter difference): what is the average rate?

**Answers to the numerical items.** (7) Full mesh of 12 sites needs 12 x 11 / 2 = 66 links; hub-and-spoke needs 11 if the hub is one of the sites, or 12 if the centre is a separate site. (10) With 25% growth and gateway/network/broadcast: 200 -> 253 addresses -> /24; 400 -> 503 -> /23 (512); 1000 -> 1253 -> /21 (2048); 60 -> 78 -> /25 (128). (17) PUE = 90 / 60 = 1.5; 900 MB in 300 s = 900 x 8 / 300 = 24 Mbit/s.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the hierarchical network design model.**

The model divides a campus network into access, distribution and core layers. The access layer connects end devices and provides PoE, port security and VLAN assignment. The distribution layer aggregates access switches, routes between VLANs and applies policy such as ACLs, and provides redundancy. The core is a fast, simple backbone between distribution blocks, servers and the internet edge, with no policy. Benefits: scalability (add a block without redesign), fault isolation, predictable performance and easier troubleshooting. Redundant links are used at each layer and loops are controlled by spanning tree or link aggregation. In a small network the distribution and core are combined (collapsed core).

**Q2 (5 marks). What is the purpose of a DMZ? Describe a typical design.**

A DMZ is a separate network segment between the internet and the internal network, holding servers that must be reachable from outside: web, mail gateway, DNS. A firewall with three interfaces (outside, DMZ, inside) enforces: outside may reach only published ports in the DMZ; inside may reach the DMZ and the internet; the DMZ may not start connections to the inside except for narrowly defined ones, for example to a database port. If a DMZ server is compromised the attacker still faces the internal firewall, so the internal network is protected.

**Q3 (10 marks). Explain the planning and running of a small data centre.**

Site: a room away from flood and leaks, with a strong floor, two fibre entries from two carriers and a separate fire compartment, braced racks for earthquakes. Power: dual utility feeds or one feed with a generator, ATS, online UPS, A/B PDUs with dual-supply servers, a power budget per rack, monthly generator tests. Cooling: CRAC units with hot-aisle/cold-aisle layout, blanking panels, containment, temperature and humidity sensors; efficiency measured by PUE = total power / IT power. Racks and cabling: 42U racks, heavy equipment low, separate and labelled power and data cables, top-of-rack switches, rack elevation in the inventory. Protection: smoke detection and clean-agent gas, leak sensors, badge access, CCTV, visitor escort and locked racks. Running: change control and maintenance windows, capacity and inventory tracking, monitoring of environment and power in the same system as servers, out-of-band management, runbooks and drills, post-incident reviews. Conclusion: availability comes from redundancy, monitoring and tested procedures together, and the design should match the tier that the business can afford.
