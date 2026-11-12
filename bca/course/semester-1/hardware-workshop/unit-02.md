---
subject: Hardware Workshop
grade: BCA Semester 1
unit: 2
title: Introduction to Networking Components
area: BCA 106 · Hardware Workshop · Unit 2
---

A computer on its own can only compute. Joined to other machines it can share files, printers and an internet connection. This unit is the lab guide to the **physical** side of networking: the devices (modem, NIC, hub, switch, router, access point), the cables and connectors (UTP, coaxial, fibre) and the three kinds of Ethernet cable you must be able to crimp, plus testing and fixing physical faults.

::: key What this unit gives you
- Purpose, layer and behaviour of the modem, NIC, hub, switch, router, access point and range extender.
- Cabling: Cat5, Cat5e, Cat6, coaxial and fibre-optic cable, and the connectors RJ45, BNC, SC, LC.
- Straight-through, crossover and rollover cables, with T568A and T568B colour orders and the crimping procedure.
- Cable testing, common physical faults and how to simulate and repair them.
:::

## 2.1 Overview of network devices

A network device is any box that moves data between machines. Each works at a different **layer** of the OSI model, which decides how much it understands about the data it carries.

| Device | OSI layer | What it does | Typical lab example |
|---|---|---|---|
| Modem | 1 (physical) | Converts digital data to the signal used on the line (telephone, cable, fibre) and back | ADSL or fibre ONT box from the ISP |
| NIC | 1 and 2 | Connects a computer to the medium; owns a 48-bit MAC address | Onboard Gigabit port, Wi-Fi card |
| Hub | 1 | Repeats every incoming bit to all other ports | Old 8-port hub |
| Switch | 2 | Learns MAC addresses and forwards a frame only to the right port | 8 or 24-port managed or unmanaged switch |
| Router | 3 | Forwards packets between different networks using IP addresses | Wireless home router |
| Access point (AP) | 2 | Bridges Wi-Fi clients to the wired LAN | Ceiling-mounted AP |
| Extender | 1 or 2 | Repeats a weak Wi-Fi signal to enlarge the coverage area | Plug-in range extender |

```svgfig label="2.1" caption="A small office network. The modem brings the ISP line in; the router joins the LAN to the internet; the switch connects wired PCs and the printer; the access point serves Wi-Fi laptops. Every wired link is a straight-through cable."
f = Fig(760, 250)
f.box(10, 100, 100, 50, "ISP line\nModem", fill=SOFT, stroke=NAVY, size=11, bold=True)
f.box(160, 100, 100, 50, "Router\n(gateway)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(310, 100, 100, 50, "Switch", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(110, 125), (160, 125)], color=NAVY)
f.arrow([(260, 125), (310, 125)], color=NAVY)
f.box(470, 20, 110, 44, "PC 1", fill=SOFT, stroke=TEAL, size=11)
f.box(470, 100, 110, 44, "PC 2", fill=SOFT, stroke=TEAL, size=11)
f.box(470, 180, 110, 44, "Printer", fill=SOFT, stroke=TEAL, size=11)
f.arrow([(410, 112), (440, 42), (470, 42)], color=TEAL)
f.arrow([(410, 125), (470, 122)], color=TEAL)
f.arrow([(410, 138), (440, 202), (470, 202)], color=TEAL)
f.box(630, 100, 110, 50, "Access point\n(Wi-Fi)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(580, 122), (630, 125)], color=AMBER)
f.text(380, 244, "Modem to router: WAN side. Router, switch, PCs: LAN side.", size=10.5, color=SLATE)
```

### Modem

The word means **mod**ulator-**dem**odulator. A telephone-line (ADSL) modem turns bits into audio-frequency tones; a cable modem uses TV channels; in a fibre network the equivalent box is an **ONT** (optical network terminal) that turns light pulses into Ethernet. A modem does not route: it has one WAN side and usually one Ethernet port. Many home boxes combine modem, router, switch and access point in one case.

### Network interface card (NIC)

A NIC joins a computer to the network. Wired NICs have an RJ45 socket; wireless NICs have an antenna. Each has a **MAC address** (for example 3C-52-82-1A-9F-04), 48 bits written as six hexadecimal bytes; the first three bytes identify the manufacturer. Link speeds are 10, 100, 1,000 Mbps and higher. On Windows, `ipconfig /all` lists the adapter and MAC; in Linux use `ip link`.

### Hub, switch and router compared

A **hub** is a multi-port repeater: a frame arriving on port 1 is copied to every other port, so all attached machines share one **collision domain** and one bandwidth. A **switch** reads the destination MAC address of each frame, keeps a table of which MAC sits on which port, and sends the frame only there; each port is its own collision domain and can run full duplex. A **router** connects *different* networks, reads the destination IP address, consults a routing table and also separates **broadcast domains**. At home the router also provides DHCP, NAT and a firewall.

::: example Worked example: why a switch beats a hub
Eight PCs share a 100 Mbps hub. If two PCs are transferring, the hub gives a shared 100 Mbps and every other PC hears the traffic. On a 100 Mbps switch, four simultaneous pairs can each run at 100 Mbps full duplex, an aggregate of up to 4 × 100 × 2 = **800 Mbps** of capacity, because each port has a private link to the switch.
:::

### Access point and extender

An **access point** (AP) has a radio and a wired port: it joins Wi-Fi clients (802.11n, ac, ax) to the wired LAN, with the same IP subnet on both sides. A **wireless router** is a router plus a built-in AP. A **range extender** receives the existing Wi-Fi and re-transmits it; if it uses the same radio for both jobs, real throughput drops to about half. Where possible, connect extra APs by cable instead.

## 2.2 Cabling and connectors

### Twisted-pair (UTP) cable

Ethernet inside buildings mostly uses **UTP** (unshielded twisted pair): four pairs of copper wire, each pair twisted to cancel interference. The twist rate differs from pair to pair. The category tells you the bandwidth and the speed the cable is rated for.

| Category | Bandwidth | Typical speed | Notes |
|---|---|---|---|
| Cat5 | 100 MHz | 100 Mbps | Obsolete |
| Cat5e | 100 MHz | 1 Gbps | Common, enhanced crosstalk limits |
| Cat6 | 250 MHz | 1 Gbps (10 Gbps to about 55 m) | Standard for new work |
| Cat6a | 500 MHz | 10 Gbps to 100 m | Thicker, often shielded |
| Cat7 / Cat8 | 600 MHz / 2 GHz | 10 / 25-40 Gbps (Cat8 to 30 m) | Data centres |

The maximum length of one Ethernet copper segment is **100 m**: 90 m of permanent cable plus up to 10 m of patch cords. Beyond that, use a switch or fibre.

**Connector.** The 8-pin modular plug is called **RJ45** (strictly 8P8C). The wire at each pin is set by a standard, either **T568A** or **T568B**.

| Pin | T568A | T568B |
|---|---|---|
| 1 | white/green | white/orange |
| 2 | green | orange |
| 3 | white/orange | white/green |
| 4 | blue | blue |
| 5 | white/blue | white/blue |
| 6 | orange | green |
| 7 | white/brown | white/brown |
| 8 | brown | brown |

10/100 Mbps Ethernet uses only pins 1, 2 (transmit) and 3, 6 (receive). Gigabit and faster use all four pairs.

### Straight-through, crossover and rollover cables

```svgfig label="2.2" caption="Which cable to use. Straight-through (same standard at both ends) joins unlike devices; crossover (T568A at one end, T568B at the other) joins like devices; rollover (pins reversed) is the console cable for a router or switch."
f = Fig(760, 220)
rows = [("Straight-through", "T568B  to  T568B", "PC to switch, switch to router,\nPC to hub, router to AP", BLUE),
        ("Crossover", "T568A  to  T568B", "PC to PC, switch to switch,\nhub to hub, router to PC", SOFT),
        ("Rollover", "pin 1 to 8, 2 to 7 ...", "PC serial/USB port to the console\nport of a router or switch", BLUE)]
for i, (a, b, c, col) in enumerate(rows):
    y = 12 + i * 68
    f.box(10, y, 160, 54, a, fill=col, stroke=NAVY, size=12, bold=True)
    f.box(190, y, 190, 54, b, fill=SOFT, stroke=TEAL, size=11)
    f.box(400, y, 350, 54, c, fill="#ffffff", stroke=SLATE, size=11)
f.text(380, 214, "Modern Gigabit ports use Auto-MDI/MDI-X and fix a wrong choice automatically.", size=10.5, color=SLATE)
```

- **Straight-through:** both ends wired to the same standard (T568B at both ends is the usual choice). Used between *unlike* devices: computer to switch, switch to router.
- **Crossover:** one end T568A and the other T568B, so the transmit pair of one device meets the receive pair of the other. Used between *like* devices: PC to PC, switch to switch. Most current devices have **Auto-MDI/MDI-X** and accept either.
- **Rollover (console) cable:** the pin order is reversed (1 to 8, 2 to 7, and so on). It is usually flat and pale blue and joins a PC to the **console port** of a Cisco-type router or switch for first configuration (9600 baud, 8 data bits, no parity, 1 stop bit).

### Coaxial and fibre-optic cable

**Coaxial** cable has a copper core, an insulator, a braided shield and an outer jacket. Old Ethernet (10BASE2, RG-58 with **BNC** connectors, up to 185 m) used it in bus topologies; today coax carries cable TV and cable-modem signals (RG-6 with an **F connector**).

**Fibre-optic** cable carries light in a glass core. **Multimode fibre** (50/125 µm, OM3 or OM4) is used inside buildings and campuses; **single-mode fibre** (9/125 µm) runs for tens of kilometres between towns and to homes. Fibre is immune to electrical interference, cannot be tapped easily and gives the highest speeds, but connectors and tools cost more. Common connectors are **SC** (square push-pull), **LC** (small, used on SFP modules) and **ST** (round bayonet).

| Medium | Max segment (typical) | Interference | Cost | Use |
|---|---|---|---|---|
| UTP Cat5e/6 | 100 m | Medium | Low | LAN desktops |
| Coaxial (RG-6) | hundreds of metres | Low | Low | Cable TV, cable modem |
| Multimode fibre | 300 m to 550 m at 10 Gbps | None | Medium | Building backbone |
| Single-mode fibre | tens of km | None | High | ISP, long links |

### Crimping an RJ45 plug (procedure)

Tools: UTP cable, RJ45 plugs (with boots if wanted), a crimping tool with stripper and cutter, a cable tester.

1. Cut the cable square and strip about **25 mm** of the outer jacket without nicking the pairs.
2. Untwist the four pairs and straighten each wire; do not untwist more than about **13 mm**, or crosstalk rises.
3. Arrange the eight wires in the chosen order (T568B for a straight-through cable; T568A at one end only for a crossover). Pin 1 is on the left when the plug's clip faces away from you and the contacts face you.
4. Press the wires flat and trim them in a straight line so about **12 mm** protrudes.
5. Push the wires into the plug until every conductor touches the end; check that the jacket also reaches past the strain-relief tab.
6. Place the plug in the crimper and squeeze fully; the contacts bite through the insulation and the tab grips the jacket.
7. Repeat at the second end and test with a **cable tester**: LEDs 1 to 8 must light in order on both units (for a crossover, 1-3, 2-6, 3-1, 6-2 and the rest straight).

::: caution Common crimping errors
Wires not pushed to the end (open circuit), jacket not reaching the clamp (cable pulls out), split pairs (pins 3 and 6 on the wrong pair; the tester may pass but speed collapses), and mixing T568A at one end with T568B at the other when a straight-through cable was wanted.
:::

## 2.3 Testing and troubleshooting physical problems

Most network faults are physical. Always begin at layer 1: is there a link light, is the cable plugged in, is the port alive?

| Symptom | Likely cause | Test and fix |
|---|---|---|
| No link light on NIC or switch port | Unplugged, broken or open cable; dead port | Reseat, swap the cable, try another port |
| Link light on but only 10 or 100 Mbps | A broken pair (only pairs 1-2, 3-6 working), a bad crimp or Cat5 cable | Cable tester wire-map; re-crimp; use Cat5e or better |
| Intermittent drops | Loose plug, pinched cable, interference, bad patch cord | Wiggle test, replace patch cord, keep away from power cables |
| Works on short cable but fails at 90 m+ | Over 100 m or poor termination | Move the switch closer or use fibre |
| One PC cannot reach others | Wrong cable type on an old device, port disabled | Swap cable type, check port status |

**Cable tester wire-map.** A basic LAN tester has a master unit and a remote unit and shows the eight lines in sequence. A fault shows as **open** (a line does not light), **short** (two lines light together), **reversed or crossed** pair, or **split pair**. A multimeter in continuity mode can test a single conductor, but not twisting.

::: example Worked example: effect of cable choice on transfer time
Copy a 4 GB (32,000 Mb) file over (a) a 100 Mbps link and (b) a 1,000 Mbps link, ignoring protocol overhead. (a) 32,000 / 100 = **320 s** (5 min 20 s). (b) 32,000 / 1,000 = **32 s**. A single bad crimp that forces a Gigabit link down to 100 Mbps makes the copy ten times slower, which is why you check the negotiated speed after any re-crimp.
:::

**Simulating faults in the lab.** A common exercise: your instructor removes one wire from a patch cord, swaps two wires, plugs a crossover cable where a straight-through is needed (on an old device), or disables a switch port. You must locate the fault using the link lights and the tester, replace the cable or device, and record the fix in a troubleshooting log (see Unit 7).

## 2.4 Eight rules for handling network hardware

1. Power off and unplug a device before connecting its power or fibre cables.
2. Never bend UTP below a radius of about four times its diameter; never pull on the cable, only on the plug.
3. Label both ends of every cable and every patch-panel port.
4. Keep copper cable away from fluorescent lights and power cables.
5. Never look into the end of a live fibre or a fibre transmitter port.
6. Use the right cable category for the speed you want, and measure that you actually get it.
7. Keep one spare patch cord of each type in the toolbox.
8. Record the device model, firmware and IP address of every box you install.

## Formula and fact sheet

- Transfer time = file size (bits) / link rate (bits per second); 1 byte = 8 bits.
- Maximum Ethernet copper segment: 100 m (90 m permanent link plus patch cords).
- T568B: wh/orange, orange, wh/green, blue, wh/blue, green, wh/brown, brown. T568A swaps the orange and green pairs.
- Straight-through joins unlike devices, crossover joins like devices, rollover joins a PC to a console port.
- Hub: layer 1, one collision domain. Switch: layer 2, one collision domain per port. Router: layer 3, one broadcast domain per interface.
- Fibre: multimode 50/125 µm for buildings, single-mode 9/125 µm for long distance; connectors SC, LC, ST.

## Chapter summary

- Network devices are placed by layer: modem and NIC at the physical link, hub at layer 1, switch and AP at layer 2, router at layer 3.
- UTP is the standard LAN cable up to 100 m; Cat5e and Cat6 are used for Gigabit, Cat6a for 10 Gbps.
- Straight-through, crossover and rollover cables differ only in pin order; T568B is the usual choice and Auto-MDI/MDI-X has made crossover cables rare.
- Coaxial serves cable TV and legacy bus networks; fibre gives distance and immunity to interference.
- Testing begins at layer 1 with link lights and a cable tester, and every fix goes in the log.

## Practice

1. Name the OSI layer of a hub, a switch and a router and state the difference in how each forwards data.
2. Write the T568B colour sequence from pin 1 to pin 8.
3. Which cable (straight-through, crossover, rollover) would you use for (a) PC to switch, (b) switch to switch on an old device, (c) PC to the console port of a router, (d) router to a PC?
4. State the maximum length of a UTP segment and what you would do for a run of 140 m.
5. List the steps of crimping an RJ45 plug.
6. A cable tester shows LEDs 1, 2, 3, 6 lighting but 4, 5, 7, 8 dark. What speed will the link negotiate and why?
7. Compare multimode and single-mode fibre with one use for each.
8. How long does a 2 GB (16,000 Mb) file take to copy at 100 Mbps and at 1 Gbps?
9. Distinguish a collision domain from a broadcast domain.
10. Explain what a MAC address is and where you find it on Windows.

::: note Answers and worked solutions
**1.** Hub: layer 1, repeats to every port. Switch: layer 2, forwards by MAC address to one port. Router: layer 3, forwards by IP address between networks.
**2.** white/orange, orange, white/green, blue, white/blue, green, white/brown, brown.
**3.** (a) Straight-through. (b) Crossover (modern switches accept straight-through via Auto-MDI/MDI-X). (c) Rollover. (d) Crossover on very old equipment; straight-through on modern ports.
**4.** 100 m. For 140 m, add a switch (or repeater) near the 90 m mark, or use fibre.
**5.** Strip 25 mm, untwist and order the wires, flatten and trim to 12 mm, insert to the end, crimp, repeat, test.
**6.** Only pairs 1-2 and 3-6 are good, so the link falls back to **100 Mbps** (Fast Ethernet needs only those pairs); Gigabit needs all four.
**7.** Multimode (50/125 µm): inside buildings and campuses over short distances; single-mode (9/125 µm): ISP and inter-city links over tens of kilometres.
**8.** 16,000 / 100 = **160 s**; 16,000 / 1,000 = **16 s**.
**9.** A collision domain is the set of devices whose frames can collide (one per switch port); a broadcast domain is the set that receives a broadcast (one per router interface).
**10.** The 48-bit hardware address of a NIC; run `ipconfig /all` and read Physical Address.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Differentiate between a hub, a switch and a router.**

A **hub** (layer 1) repeats every bit to all ports, so all devices share one collision domain and the bandwidth. A **switch** (layer 2) learns MAC addresses and forwards each frame only to the destination port, giving every port its own collision domain and full-duplex speed. A **router** (layer 3) joins different networks, uses IP addresses and a routing table, and divides broadcast domains. In a small office the router connects the LAN to the ISP, the switch connects the PCs and a hub is no longer used.

**Q (5 marks). Explain the straight-through, crossover and rollover cables.**

A straight-through cable has the same wiring (T568B) at both ends and joins unlike devices such as a PC and a switch. A crossover cable has T568A at one end and T568B at the other, so transmit meets receive, and joins like devices such as PC to PC. A rollover cable reverses the pin order and connects a PC to a router or switch console port for configuration. Figure 2.2 summarises the three.

**Q (10 marks). Describe the common networking cables and connectors, and explain how an RJ45 cable is crimped and tested.**

*Introduction.* The medium carries the signal; the choice depends on speed, distance and cost.

*Cables.* UTP Cat5e or Cat6 (four twisted pairs, 100 m, RJ45 connector) for desktops; coaxial (RG-6, F or BNC connector) for cable TV and legacy buses; multimode fibre (50/125 µm, LC or SC) within a building and single-mode fibre (9/125 µm) between towns.

*Crimping.* Strip 25 mm of jacket, untwist at most 13 mm, order the wires to T568B, trim to 12 mm, insert to the end of the plug, crimp, repeat at the second end.

*Testing.* Connect both ends to a cable tester and check that lines 1 to 8 light in order. Open, short, reversed or split pairs are fixed by re-crimping. Finally confirm the link negotiates 1 Gbps. Figure 2.1 shows where each cable sits in a small network.
