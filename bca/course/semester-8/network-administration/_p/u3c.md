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
