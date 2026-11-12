---
subject: Hardware Workshop
grade: BCA Semester 1
unit: 5
title: Basic Network Devices and Deployment
area: BCA 106 · Hardware Workshop · Unit 5
---

Unit 2 introduced the parts; this unit puts them to work. You will identify devices in a rack or on a bench, join them in the standard topologies with the correct cables, share files, folders and a printer across the network, and install, configure and maintain printers of every common technology.

::: key What this unit gives you
- Identifying the modem, NIC, hub, switch, router and access point on a bench, and choosing the cable for each connection.
- Network topologies (bus, star, ring, mesh, tree) built with real devices, with link counts.
- Sharing files, folders and printers on a Windows (and Linux) LAN, with permissions.
- Printer technologies (laser, inkjet, dot-matrix, thermal, 3D) and installing, configuring and maintaining printers.
:::

## 5.1 Identifying network devices on the bench

When you are handed an unlabelled box, work through four clues: **ports** (one WAN port and a few LAN ports: router; many identical RJ45 ports and no WAN: switch; antennas and one Ethernet port: AP), **labels and LEDs** (model number, MAC address on the sticker, link and activity LEDs), **power** (adapter voltage and current), and **settings page** (the sticker gives the default IP such as 192.168.1.1 and the default login).

| Box | How to recognise it | Typical cable to it |
|---|---|---|
| Modem / ONT | One WAN port (fibre, DSL or coax) plus one LAN port | Straight-through to the router WAN port |
| Hub | Many RJ45 ports, collision LED, no management | Straight-through to PCs, crossover to another hub |
| Switch | Many ports, per-port link and speed LEDs, MAC table when managed | Straight-through to PCs |
| Router | WAN port, several LAN ports, Wi-Fi antennas on home models | Straight-through |
| Access point | One Ethernet port (often PoE), antennas or a ceiling housing | Straight-through to a switch port |
| NIC | Card with RJ45 or antenna, MAC sticker | Straight-through to a switch |

## 5.2 Network topologies

A **topology** is the arrangement of the devices and links. The **physical topology** is the wiring seen on the bench; the **logical topology** is how data flows.

```svgfig label="5.1" caption="Five topologies with five or six nodes. Bus: one shared backbone with a terminator at each end. Star: every node has its own cable to a central switch. Ring: each node joins two neighbours. Full mesh: every pair is linked. Tree: stars joined in a hierarchy."
f = Fig(760, 250)
def node(x, y, t="PC"):
    f.box(x - 22, y - 13, 44, 26, t, fill=BLUE, stroke=NAVY, size=10)
# bus
f.arrow([(14, 70), (136, 70)], color=NAVY)
for x in (34, 74, 114):
    node(x, 30); f.arrow([(x, 43), (x, 70)], color=TEAL)
node(54, 112); f.arrow([(54, 99), (54, 70)], color=TEAL)
f.text(75, 150, "Bus", size=12, color=NAVY, bold=True)
# star
f.box(228, 48, 50, 30, "Switch", fill=SOFT, stroke=NAVY, size=10, bold=True)
for (x, y) in ((190, 20), (316, 20), (190, 108), (316, 108)):
    node(x, y); f.arrow([(253, 63), (x, y)], color=TEAL)
f.text(253, 150, "Star", size=12, color=NAVY, bold=True)
# ring
pts = [(430, 24), (500, 24), (520, 70), (500, 116), (430, 116), (410, 70)]
for i, (x, y) in enumerate(pts):
    node(x, y, "N" + str(i + 1)); nx, ny = pts[(i + 1) % 6]; f.arrow([(x, y), (nx, ny)], color=TEAL)
f.text(465, 150, "Ring", size=12, color=NAVY, bold=True)
# mesh (4 nodes)
m = [(600, 24), (700, 24), (700, 116), (600, 116)]
for i in range(4):
    for j in range(i + 1, 4):
        f.arrow([m[i], m[j]], color=TEAL)
for (x, y) in m: node(x, y)
f.text(650, 150, "Full mesh (4 nodes)", size=12, color=NAVY, bold=True)
# tree
f.box(310, 176, 120, 26, "Core switch", fill=SOFT, stroke=NAVY, size=10, bold=True)
for x in (180, 370, 560):
    f.box(x - 50, 220, 100, 24, "Switch", fill=SOFT, stroke=NAVY, size=10); f.arrow([(370, 202), (x, 220)], color=TEAL)
f.text(100, 232, "Tree", size=12, color=NAVY, bold=True)
```

| Topology | Links for n nodes | Advantage | Disadvantage |
|---|---|---|---|
| Bus | 1 backbone | Cheap, little cable | A cable break stops everyone; collisions; obsolete |
| Star | n | Easy to add and fault-find; one failure affects one PC | Central switch is a single point of failure |
| Ring | n | Predictable access (token); no collisions | One break can stop the ring (unless dual ring) |
| Full mesh | n(n − 1) / 2 | Very reliable | Many links and ports: expensive |
| Tree | n − 1 | Scales across floors | Backbone failure splits the tree |

::: example Worked example: counting links
A lab has 6 computers. **Star:** 6 cables to one switch. **Bus:** 1 backbone plus 6 drops. **Ring:** 6 links. **Full mesh:** 6 × 5 / 2 = **15 links**, and each computer needs 5 NICs, which is why full mesh is used only among a few core routers. For 10 nodes, mesh needs 10 × 9 / 2 = **45 links**; a star needs 10.
:::

### Building a star network on the bench

1. Place the switch in the middle and power it up.
2. Crimp or choose straight-through patch cords, one per PC (T568B at both ends).
3. Plug each PC NIC into a switch port; check the link LED on both ends.
4. Give each PC a static IP in one subnet (Unit 6) or let DHCP do it.
5. Ping every PC from one PC and record the results.

**Bus (for demonstration).** Real coaxial bus networks used T-connectors and 50 Ω terminators; in the lab you may use a simulator or two hubs chained by crossover cable to see how all machines share the same medium.

**Connecting devices of the same kind.** Hub to hub or switch to switch with a crossover cable on old equipment; on modern devices a straight-through cable works through Auto-MDI/MDI-X. Always label the **uplink** port.

## 5.3 Sharing resources: files, folders and printers

Sharing lets one machine give others access to its files or printer. On Windows it uses the **SMB** protocol; on Linux the same service is provided by **Samba**.

**Preparing the network (Windows 10 or 11).**

1. Set the network profile to **Private** (Settings, Network and Internet, Properties).
2. Open Advanced sharing settings and turn on **network discovery** and **file and printer sharing**.
3. Give every PC a unique name and an IP address in the same subnet; check that they can ping each other.

**Sharing a folder.**

1. Right-click the folder, Properties, Sharing, **Advanced Sharing**; tick *Share this folder* and give a share name such as `Notes`.
2. Click Permissions and choose the user or group with **Read**, **Change** or **Full control**.
3. Check the NTFS permissions on the Security tab as well: the **more restrictive** of the share and NTFS permissions wins.
4. From another PC open File Explorer and type `\\PCNAME\Notes` or `\\192.168.1.10\Notes`, enter the account and password.
5. Use **Map network drive** to give it a letter such as `Z:`.

| Permission | Allows |
|---|---|
| Read | open and copy files |
| Change | Read plus create, edit and delete |
| Full control | Change plus change permissions |

**Sharing a printer.** On the PC with the printer: Settings, Printers and scanners, the printer, Printer properties, Sharing tab, tick *Share this printer*, name it. On other PCs: Add printer, choose the shared printer, or type `\\PCNAME\PrinterName`. A better design for an office is a network printer with its own IP address.

**Linux.** Install Samba (`sudo apt install samba`), add a block `[Notes]` with `path`, `read only = no` to `/etc/samba/smb.conf`, create a Samba user (`sudo smbpasswd -a user`) and restart `smbd`. The printer is shared through **CUPS** on port 631.

::: caution Security of sharing
Share only what is needed, never share the whole `C:` drive, use strong passwords, avoid *Everyone: Full control*, and turn off sharing on public Wi-Fi.
:::

## 5.4 Printer technologies

| Type | How it prints | Good for | Cost to run | Notes |
|---|---|---|---|---|
| Laser | A laser charges a drum; toner powder sticks and is fused by heat | Text documents, offices, high volume | Low per page | 600 to 1,200 dpi, 20 to 60 ppm |
| Inkjet | Nozzles spray tiny drops of liquid ink (thermal bubble or piezoelectric) | Photos, colour, home use | High per page | Heads clog if unused |
| Dot-matrix | Pins strike an inked ribbon (impact) | Carbon-copy forms, invoices, bank passbooks | Very low | Loud, 9 or 24 pins |
| Thermal | Heated head darkens heat-sensitive paper (or transfers wax by ribbon) | Receipts, labels, barcodes | Paper only | Faded by heat and time |
| 3D printer | Layers of melted plastic (FDM) or cured resin | Prototypes, parts | Filament cost | Slow |

**Laser-printing process.** (1) *Charging* the drum with a primary corona or roller; (2) *exposing* it to the laser, which discharges the image areas; (3) *developing*: toner sticks to the discharged areas; (4) *transferring* the toner onto paper; (5) *fusing* it with a heated roller (about 180 to 200 °C); (6) *cleaning* the drum for the next page.

```svgfig label="5.2" caption="The six stages of laser printing. The drum is charged, written on by the laser, dusted with toner, which is transferred to paper and melted onto it by the fuser; the drum is then cleaned and the cycle repeats for the next page."
f = Fig(760, 150)
steps = ["1 Charge\ndrum", "2 Expose\n(laser)", "3 Develop\n(toner)", "4 Transfer\nto paper", "5 Fuse\n(heat)", "6 Clean\ndrum"]
for i, t in enumerate(steps):
    x = 10 + i * 124
    f.box(x, 30, 104, 56, t, fill=BLUE if i < 5 else SOFT, stroke=NAVY, size=11, bold=True)
    if i < 5: f.arrow([(x + 104, 58), (x + 124, 58)], color=NAVY)
f.arrow([(682, 86), (682, 116), (62, 116), (62, 86)], color=AMBER)
f.text(380, 138, "Repeat for each page", size=10.5, color=SLATE)
```

**Print quality terms.** **dpi** (dots per inch) is resolution; **ppm** (pages per minute) is speed; **duty cycle** is the safe monthly page count; **CMYK** are the four inks or toners (cyan, magenta, yellow, black). A 300 dpi A4 page (8.27 × 11.69 in) holds 2,481 × 3,507 = about **8.7 million** dots in each colour plane.

::: example Worked example: cost per page
A toner costing Rs 6,500 prints 2,600 pages; a cartridge of ink costing Rs 1,400 prints 300 pages. Laser: 6,500 / 2,600 = **Rs 2.50 per page**. Inkjet: 1,400 / 300 = **Rs 4.67 per page**. If the office prints 1,000 pages a month, laser saves (4.67 − 2.50) × 1,000 = about **Rs 2,170 a month** on consumables.
:::

## 5.5 Installing, configuring and maintaining a printer

**Installing a local (USB) printer.**

1. Unpack, remove the transport tape, install toner or ink and load paper.
2. Connect the power cable and the USB cable; power on.
3. Windows usually detects it and installs a driver; if not, download the driver for your exact model and Windows version from the maker's site.
4. Open Printers and scanners and confirm the printer is *Ready*; set it as default if required.
5. Print a **test page**, then adjust paper size (A4), quality, duplex and tray settings under Printing preferences.

**Installing a network printer.** Connect by Ethernet or Wi-Fi (WPS or the panel menu), print the network configuration page to see its **IP address**, and in Windows choose Add printer, *The printer that I want isn't listed*, Add a printer using an IP address, and enter it; the standard TCP/IP port uses port 9100. Give the printer a fixed or reserved IP so the port stays valid. Linux installs through CUPS (`http://localhost:631`) or the settings app, often with **IPP Everywhere** (driverless).

**Managing the queue.** Open the printer queue to pause, cancel or restart a job. If the queue is stuck, restart the **Print Spooler** service (`net stop spooler` then `net start spooler` as administrator) and clear the spool folder.

**Maintenance.**

| Printer | Routine task | Interval |
|---|---|---|
| Laser | Replace toner; clean the corona/transfer rollers and feed rollers; vacuum the dust (never a normal vacuum for toner); replace the drum and fuser at their page count | as indicated |
| Inkjet | Run head cleaning and alignment; print weekly so ink does not dry; use genuine or tested ink | weekly use |
| Dot-matrix | Replace the ribbon; clean the pins and platen | when print fades |
| All | Remove paper dust, update firmware and drivers, keep paper dry | every 3 to 6 months |

**Common printer faults.** *Paper jam:* power off, open the cover, pull the paper in the direction of travel. *Faded or streaky print:* low toner, dirty drum, clogged nozzles. *Ghost images:* worn drum or fuser. *Blank pages:* no toner, a protective strip left in. *Printer offline:* USB or network cable, wrong port, or Use Printer Offline ticked. *Garbage characters:* wrong driver.

## 5.6 Eight rules for deploying network devices and printers

1. Draw the topology and label every cable before you plug anything in.
2. Choose the cable by device pair, and verify the link LED.
3. Use a private IP plan on paper (subnet, gateway, static range, DHCP range).
4. Change default router and printer passwords immediately.
5. Share the minimum, with explicit permissions.
6. Use genuine or tested toner and the exact driver for the OS.
7. Keep spare cables, toner, paper and a USB driver stick in the lab toolbox.
8. Document the final configuration for the next technician.

## Formula and fact sheet

- Full mesh links = n(n − 1) / 2; star = n; ring = n; bus = 1 backbone; tree = n − 1.
- Laser stages: charge, expose, develop, transfer, fuse, clean. Fuser about 180 to 200 °C.
- Cost per page = cartridge price / page yield.
- Dots in a page = (width × dpi) × (height × dpi).
- Share path format: `\\COMPUTER\ShareName`; the stricter of share and NTFS permission applies.
- Standard TCP/IP printing port 9100; CUPS port 631; SMB port 445.

## Chapter summary

- Devices are identified by ports, labels, LEDs and the default IP printed on the sticker.
- The star topology with a switch is standard; mesh needs n(n − 1)/2 links; bus is obsolete.
- Sharing needs a private profile, discovery on, permissions set and a path such as `\\PC\Notes`.
- Laser, inkjet, dot-matrix, thermal and 3D printers differ in mechanism, cost per page and best use.
- Install the driver, print a test page, share through the Sharing tab or use a network printer with a fixed IP, then maintain on a schedule.

## Practice

1. Define topology and distinguish physical from logical topology.
2. Draw a star and a ring of five nodes. How many cables does each need?
3. How many links does a full mesh of 12 nodes need?
4. Which cable joins (a) PC to switch, (b) hub to hub on old hardware, (c) router WAN to modem?
5. List the steps to share a folder named Notes and open it from another PC.
6. A folder has share permission Full control but NTFS Read. What can the remote user do?
7. Describe the six stages of laser printing.
8. A laser printer costs Rs 2.30 per page and an inkjet Rs 5.00; find the saving on 800 pages.
9. List six common printer faults with the fix.
10. Explain how you would install a network printer and why it needs a fixed IP.

::: note Answers and worked solutions
**1.** Topology is the arrangement of devices and links. Physical is the actual wiring; logical is how data flows (a star wired to a hub behaves logically like a bus).
**2.** Star of five: 5 cables to a switch. Ring of five: 5 links (each node to two neighbours).
**3.** 12 × 11 / 2 = **66 links**.
**4.** (a) Straight-through. (b) Crossover (or straight-through with Auto-MDIX). (c) Straight-through.
**5.** Properties, Sharing, Advanced Sharing, Share this folder, name Notes, Permissions; open `\\PCNAME\Notes` from the other PC and sign in; optionally map a drive.
**6.** The stricter permission applies: the user gets **Read** only.
**7.** Charge drum, expose with laser, develop with toner, transfer to paper, fuse with heat, clean the drum.
**8.** (5.00 − 2.30) × 800 = **Rs 2,160**.
**9.** Jam (clear in feed direction), faded print (toner or drum), streaks (clean or replace), blank page (toner), offline (cable, port setting), garbled text (wrong driver).
**10.** Connect to the LAN, print the configuration page for its IP, Add printer by TCP/IP address (port 9100), install the driver, print a test page. A fixed IP stops the port from breaking when DHCP changes the address.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Explain any three network topologies with a diagram.**

In a **bus** topology all nodes share one backbone cable ended with terminators; it is cheap but a break stops everyone. In a **star** every node connects to a central switch; it is easy to expand and to find faults, and is the standard LAN today. In a **ring** each node links to two neighbours and data circulates in one direction; one break can stop it unless a second ring is added. A full mesh needs n(n − 1)/2 links and is used among core routers. Figure 5.1 shows the layouts.

**Q (10 marks). Describe laser, inkjet and dot-matrix printers and explain how to install and maintain a printer.**

*Introduction.* A printer converts a document into marks on paper.

*Laser.* A laser draws the image on a charged drum; toner is attracted, transferred to paper and fused by heat (Figure 5.2). It is fast, sharp and cheap per page.

*Inkjet.* Tiny nozzles spray ink by heating (thermal) or by piezoelectric crystals; it prints photos well but costs more per page.

*Dot-matrix.* Pins strike a ribbon and can make carbon copies; it is noisy and used for invoices.

*Installation.* Load toner or ink, connect power and USB or network, install the driver, set defaults, print a test page, and share it if needed.

*Maintenance.* Replace consumables, clean rollers and heads, clear jams, update drivers and keep a log.
