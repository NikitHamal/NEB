---
subject: Hardware Workshop
grade: BCA Semester 1
unit: 3
title: Desktop and Laptop Hardware Identification and Handling
area: BCA 106 · Hardware Workshop · Unit 3
---

Hardware Workshop is a hands-on subject: you open a computer, identify every part, assemble one, install an operating system, fix faults and crimp a network cable. This unit prepares you: safety rules, the toolkit, and a working knowledge of each component and how to read its specification, with the calculations you need to choose parts that fit and work together.

::: key What this unit gives you
- Electrical and static safety; the technician's toolkit.
- Every PC component: case, motherboard, CPU, RAM, storage, PSU, GPU, ports, with the specifications that matter.
- Compatibility rules, and calculations for power supply, memory and storage speed.
:::

## 3.1 Safety first

**Electrostatic discharge (ESD).** A static spark you cannot even feel (under 3,000 V) can destroy a chip. Use an **anti-static wrist strap** clipped to bare metal on the case, or touch the case frame before handling parts; hold cards by their edges; keep parts in **anti-static bags** until installation; work on a hard, uncarpeted surface.

**Electrical safety.** Switch off and **unplug** the PC before opening it, and press the power button once to drain the residual charge. **Never open a power supply unit (PSU)**: its capacitors hold dangerous voltage even when unplugged. Do not work with wet hands; use a surge-protected supply or UPS; keep liquids away.

**Physical safety.** Case edges are sharp; lift heavy items with the legs; keep a clear bench; tie back long hair and loose sleeves near fans; use goggles when blowing out dust and a mask for heavily dusty machines. Handle CRT monitors and old batteries carefully (lead, mercury).

**Fire and environment.** Know the fire extinguisher (CO₂ or dry powder for electrical fires, never water); dispose of batteries, toner and old boards as **e-waste**, not in the rubbish.

**Good practice:** record every cable and screw location (take photos), use the right screw (the case, board standoffs and drives use different sizes), do not force connectors (they are keyed), and back up data before any repair.

## 3.2 The toolkit

| Tool | Use |
|---|---|
| Phillips (#1, #2) and flat screwdrivers, magnetic tip | screws; small #0 for laptops |
| Torx and Allen keys | some cases, laptops |
| Anti-static wrist strap and mat | ESD protection |
| Tweezers, needle-nose pliers, parts tray | jumpers, dropped screws, bent pins |
| Cable ties, Velcro straps | cable management |
| Thermal paste and isopropyl alcohol (≥ 90 %) with lint-free cloth | CPU cooler installation and cleaning |
| Compressed air or a blower, soft brush | dust removal |
| Multimeter | check PSU rails, continuity, batteries |
| PSU tester | quick PSU check |
| Network cable crimper, RJ-45 connectors, cable tester | LAN cables |
| POST diagnostic card, spare known-good parts | fault finding |
| Bootable USB (OS installer, live Linux, diagnostics), driver disks | software side |

```photogrid label="3.1" cols="3" ratio="1.25" caption="The technician's first three tools. (a) An anti-static wrist strap: the clip goes to the bare metal of the case so that your body and the board stay at the same voltage. (b) A digital multimeter measures volts, ohms and continuity. (c) A network toolkit: cable tester, punch-down tool and RJ45 crimper."
@ photo id="bca106/strap" cap="Anti-static wrist strap"
fit 1.25
call 0.50 0.88 0.40 0.62 "Wrist band"
call 0.72 0.14 0.85 0.45 "Crocodile clip to case"
@ photo id="bca106/meter" cap="Digital multimeter"
fit 1.25
focus 0.45 0.45
call 0.50 0.90 0.50 0.62 "LCD reading"
call 0.50 0.10 0.50 0.32 "Selector dial"
@ photo id="bca106/crimpkit" cap="Cable tester and crimp kit"
fit 1.25
call 0.30 0.90 0.25 0.50 "Cable tester"
call 0.72 0.12 0.72 0.45 "RJ45 crimper"
```

```photogrid label="3.2" cols="3" ratio="1.3" caption="Three parts to recognise on sight. (a) An ATX power supply unit with its bundle of cables. (b) A PCI Express graphics card: heatsink, two fans and the gold x16 edge connector. (c) A micro-ATX motherboard, on which the CPU, memory and cards are mounted."
@ photo id="bca106/psu" cap="ATX power supply unit"
fit 1.3
call 0.50 0.90 0.50 0.62 "Vents and fan side"
call 0.50 0.12 0.62 0.35 "Cable bundle"
@ photo id="bca106/gpu" cap="PCIe graphics card"
fit 1.3
call 0.50 0.90 0.55 0.65 "Cooling fans"
call 0.50 0.12 0.50 0.25 "PCIe x16 gold fingers"
@ photo id="bca101/mobo" cap="Micro-ATX motherboard"
fit 1.3
call 0.50 0.92 0.55 0.75 "CPU, RAM slots"
call 0.50 0.10 0.45 0.25 "PCIe slots, I/O"
```

```svgfig label="3.1" caption="How the parts of a PC connect. The motherboard is the hub: the PSU gives it power, the CPU and RAM talk over the fast memory bus, the graphics card and NVMe drive use PCI Express lanes, and SATA drives and the ports use slower buses."
f = Fig(760, 300)
f.box(290, 110, 180, 70, "MOTHERBOARD\nchipset + buses", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(300, 8, 160, 40, "Power supply (PSU)", fill=SOFT, stroke=AMBER, size=11, bold=True)
f.arrow([(380, 48), (380, 110)], color=AMBER, label="24-pin, 12 V", lpos=(440, 82))
f.box(20, 40, 150, 44, "CPU + cooler", fill=SOFT, stroke=NAVY, size=11, bold=True)
f.arrow([(170, 62), (290, 125)], color=NAVY, label="socket", lpos=(210, 78))
f.box(20, 130, 150, 44, "RAM (DDR4/DDR5)", fill=SOFT, stroke=NAVY, size=11, bold=True)
f.arrow([(170, 152), (290, 148)], color=TEAL, label="memory bus", lpos=(232, 140))
f.box(20, 220, 150, 44, "Graphics card", fill=SOFT, stroke=NAVY, size=11, bold=True)
f.arrow([(170, 242), (300, 180)], color=RED, label="PCIe x16", lpos=(224, 230))
f.box(590, 40, 150, 44, "NVMe SSD (M.2)", fill=SOFT, stroke=NAVY, size=11, bold=True)
f.arrow([(590, 62), (470, 125)], color=RED, label="PCIe x4", lpos=(540, 78))
f.box(590, 130, 150, 44, "SATA HDD / SSD", fill=SOFT, stroke=NAVY, size=11, bold=True)
f.arrow([(590, 152), (470, 148)], color=TEAL, label="SATA", lpos=(526, 140))
f.box(590, 220, 150, 44, "USB, LAN, audio ports", fill=SOFT, stroke=NAVY, size=11, bold=True)
f.arrow([(590, 242), (460, 180)], color=NAVY, label="I/O", lpos=(534, 230))
f.text(380, 290, "Thicker, shorter buses are faster: memory > PCIe > SATA > USB", size=10.5, color=SLATE)
```

## 3.3 Inside the PC: components and what their specs mean

**Case (chassis).** Sizes follow the motherboard **form factor**: full/mid tower (ATX), mini tower (micro-ATX), small form factor (mini-ITX). It provides mounting for the board (brass *standoffs*), drives, fans, front-panel ports and the PSU. Airflow: front intake, rear and top exhaust.

**Motherboard.** The main circuit board joining everything. Key features: **socket** (CPU type, e.g. LGA1700, AM5), **chipset** (decides features and ports), **RAM slots** (DDR4 or DDR5, not interchangeable), **expansion slots** (PCIe x16, x4, x1), **M.2** slots (NVMe SSD), **SATA** ports, **BIOS/UEFI chip** and **CMOS battery** (CR2032, 3 V, keeps the clock and settings), **front-panel header** (power, reset, LEDs, USB, audio), **24-pin ATX** and **4/8-pin CPU** power connectors, and rear I/O.

**CPU.** Specified by cores and threads, base/boost clock (GHz), cache (L1 to L3), **TDP** (thermal design power in watts), and socket. More cores help parallel tasks; clock and cache help single-thread speed. Needs a **heatsink and fan (cooler)** with thermal paste (a pea-sized dot) to carry heat to the cooler.

**RAM.** DDR4 or DDR5 DIMMs (laptops use shorter SO-DIMMs). Specified by capacity, speed (e.g. DDR4-3200 = 3200 mega-transfers/s) and latency (CL). Use matched pairs in **dual channel** (the right slots, per the manual) for double bandwidth.

**Storage.** *HDD*: spinning platters, cheap per GB, 5400/7200 rpm, SATA. *SSD (SATA)*: flash, no moving parts, ~550 MB/s. *NVMe SSD*: flash over PCIe in an M.2 slot, 2,000 to 7,000+ MB/s. *Optical* drives are now rare.

**Power supply unit (PSU).** Converts mains AC (230 V in Nepal, 50 Hz) to DC rails: +12 V (CPU, GPU, drives), +5 V, +3.3 V. Rated in watts; the **80 PLUS** label (Bronze, Silver, Gold, Platinum) gives efficiency (Bronze: at least 82 % at 20 % and 100 % load, 85 % at 50 %). Connectors: 24-pin ATX, 4+4-pin EPS (CPU), PCIe 6+2-pin (graphics), SATA power, Molex.

**Graphics card (GPU).** Needed for gaming, 3D, video work and AI; otherwise the CPU's integrated graphics suffice. Specs: VRAM, memory bus, power connectors, length (check the case).

**Cooling.** Air (heatsink and fans), liquid (AIO radiator), case fans; thermal paste fills microscopic gaps. CPU idle temperature 30 to 45 °C; load below about 85 °C.

**Ports and connectors**

| Port | Use | Note |
|---|---|---|
| USB-A / USB-C | peripherals, charging | USB 2.0 480 Mb/s; USB 3.0 5 Gb/s; 3.2 Gen 2 10 Gb/s; USB4 up to 40 Gb/s |
| HDMI / DisplayPort | monitor | DP supports high refresh rates |
| VGA (analog) / DVI | old monitors | being retired |
| RJ-45 | Ethernet | 100 m max, 1 Gb/s common |
| 3.5 mm jacks | audio | green line out, pink mic, blue line in |
| PS/2 | old keyboard and mouse | purple and green |
| SATA data | HDD/SSD | 6 Gb/s |

## 3.4 Memory: RAM and the ROM family

**Primary memory** is what the CPU reads directly. It has two families.

**RAM (random-access memory)** is volatile: it loses its contents when power is removed. *DRAM* stores each bit as charge in a tiny capacitor that must be refreshed thousands of times a second; it is cheap and dense and is used for main memory. *SRAM* uses flip-flops, needs no refresh, is much faster and far more costly, and is used for CPU caches.

| Generation | Name | Year | Voltage | Typical speed | Notch |
|---|---|---|---|---|---|
| SDRAM (SD) | PC133 | 1990s | 3.3 V | 133 MT/s | two notches (168 pins) |
| DDR1 | DDR-400 | 2000 | 2.5 V | 400 MT/s | one notch (184 pins) |
| DDR2 | DDR2-800 | 2003 | 1.8 V | 800 MT/s | 240 pins |
| DDR3 | DDR3-1600 | 2007 | 1.5 V (1.35 V) | 1,600 MT/s | 240 pins, different notch |
| DDR4 | DDR4-3200 | 2014 | 1.2 V | 3,200 MT/s | 288 pins |
| DDR5 | DDR5-5600 | 2020 | 1.1 V | 4,800 to 8,000+ MT/s | 288 pins, notch moved |

**DDR** means *double data rate*: data moves on both edges of the clock. Generations are **not** interchangeable; the notch position prevents wrong insertion. A DDR4-3200 module has a data rate of 3,200 mega-transfers per second and a peak bandwidth of 3,200 × 8 bytes = **25,600 MB/s** per channel (it is also sold as PC4-25600).

**ROM (read-only memory)** keeps its contents without power and is used for firmware such as the BIOS.

| Type | Full name | How it is programmed | Erasing |
|---|---|---|---|
| Mask ROM | Mask-programmed ROM | At the factory | Impossible |
| PROM | Programmable ROM | Once, with a PROM programmer (fuses blown) | Impossible |
| EPROM | Erasable PROM | Programmer, then ultraviolet light through a quartz window | UV for about 20 min, whole chip |
| EEPROM | Electrically erasable PROM | Electrically, byte by byte | Electrically, in circuit |
| Flash | Block-erasable EEPROM | Electrically, in blocks | Electrically; used for BIOS/UEFI chips and SSDs |

Modern motherboards hold the BIOS/UEFI in a **flash chip**, so it can be updated without opening the case (Unit 8). A small **CMOS** RAM powered by a **CR2032** coin cell keeps the clock and settings.

## 3.5 Motherboard internals: chipset, buses and slots

A **bus** is a set of wires carrying data, addresses and control signals between components. Older boards used two bridge chips: the **northbridge** joined the CPU to the fast devices (RAM, graphics) and the **southbridge** managed slower I/O (SATA, USB, audio, LAN, BIOS). In modern designs the northbridge has moved **into the CPU** (memory controller and PCIe lanes), and only one chip remains, the **PCH (platform controller hub)** or *chipset*.

```svgfig label="3.2" caption="Classic northbridge/southbridge layout. The northbridge handles the fast links (CPU, RAM, graphics); the southbridge handles the slow I/O. In current systems the memory controller and the graphics lanes are inside the CPU, and one chipset chip does the southbridge's job."
f = Fig(760, 250)
f.box(300, 14, 160, 48, "CPU", fill=BLUE, stroke=NAVY, size=13, bold=True)
f.box(300, 104, 160, 48, "Northbridge\n(memory hub)", fill=SOFT, stroke=NAVY, size=11, bold=True)
f.box(300, 192, 160, 48, "Southbridge\n(I/O hub)", fill=SOFT, stroke=NAVY, size=11, bold=True)
f.arrow([(380, 62), (380, 104)], color=NAVY, label="front-side bus", lpos=(440, 84))
f.arrow([(380, 152), (380, 192)], color=NAVY, label="internal link", lpos=(444, 172))
f.box(40, 104, 150, 48, "RAM (DDR)", fill=BLUE, stroke=TEAL, size=11)
f.arrow([(300, 128), (190, 128)], color=TEAL)
f.box(40, 30, 150, 48, "Graphics\n(PCIe x16)", fill=BLUE, stroke=TEAL, size=11)
f.arrow([(300, 114), (190, 60)], color=TEAL)
f.box(560, 30, 170, 40, "SATA, M.2 drives", fill=BLUE, stroke=TEAL, size=11)
f.box(560, 94, 170, 40, "USB, audio, LAN", fill=BLUE, stroke=TEAL, size=11)
f.box(560, 158, 170, 40, "BIOS/UEFI, PCIe x1", fill=BLUE, stroke=TEAL, size=11)
f.arrow([(460, 216), (520, 216), (520, 50), (560, 50)], color=AMBER)
f.arrow([(520, 114), (560, 114)], color=AMBER)
f.arrow([(520, 178), (560, 178)], color=AMBER)
```

**Expansion slots and internal interfaces**

| Interface | Used for | Speed (per direction) |
|---|---|---|
| PCI (legacy) | old sound, modem and LAN cards | 133 MB/s |
| PCIe x1 / x4 / x16 | GPU, NVMe, network and capture cards | Gen 3: about 0.98 GB/s per lane; Gen 4: 1.97 GB/s; Gen 5: 3.94 GB/s |
| SATA III | HDD, SSD, optical | 6 Gb/s (about 550 MB/s real) |
| M.2 (key M or B+M) | SATA or NVMe SSD, Wi-Fi card | up to 7,000+ MB/s on PCIe 4.0 x4 |
| DIMM slots | RAM | see 3.4 |

A **PCIe x16 Gen 4** slot gives 16 × 1.97 = about **31.5 GB/s** each way. Choose a slot that matches the card's lanes: a x4 card runs in a x16 slot, but a x16 card will not fit in a x1 slot unless the slot is open-ended.

## 3.6 Storage devices and their interfaces

| Device | Technology | Interface | Speed (sequential) | Strength | Weakness |
|---|---|---|---|---|---|
| HDD | Spinning magnetic platters, moving heads | SATA (PATA in old PCs) | 80 to 200 MB/s | Cheap per GB (several TB) | Slow, noisy, fragile when running |
| SATA SSD | NAND flash | SATA III | about 550 MB/s | No moving parts, quiet | Capped by SATA |
| NVMe SSD | NAND flash over PCIe | M.2 slot, PCIe x4 | 2,000 to 7,000+ MB/s | Fastest, low latency | Costs more, can run hot |
| Optical drive | Laser on CD/DVD/Blu-ray | SATA | 1x DVD = 1.35 MB/s | Cheap media | Rarely used now |

**PATA vs SATA.** PATA (IDE) uses a wide 40-pin or 80-wire ribbon and Master/Slave jumpers, with up to 133 MB/s; SATA uses a thin 7-pin cable, one drive per cable and up to 600 MB/s (SATA III). **SSD vs HDD:** an SSD has no seek time (about 0.1 ms against 10 ms), boots Windows in seconds instead of a minute, and survives drops.

::: example Worked example: copy time for a 20 GB folder
At a real 150 MB/s (HDD) the copy takes 20,000 / 150 = **133 s**; on a SATA SSD at 500 MB/s it takes **40 s**; on a PCIe 4.0 NVMe at 5,000 MB/s about **4 s**, if the other end can keep up.
:::

**Spotting a fake SSD.** Very cheap "2 TB" drives on marketplaces are often 128 GB chips with firmware that lies about capacity. Test: (1) capacity and price far outside the market; (2) the drive fills up and corrupts old files after a fraction of its stated size; (3) run **H2testw** or the `f3` tools to write and verify the whole drive, which reports the real size; (4) check the label, controller name and serial in CrystalDiskInfo. In the lab you compare a genuine and a fake drive by these tests.

**Removing and reinstalling a drive.** Power off and unplug, wear the ESD strap, unplug SATA data and power cables (pull the plug, not the wire), remove the screws, slide the drive out; reinstall in reverse order and confirm that BIOS/UEFI detects it.

## 3.7 Input and output devices and ports

| Device | Kind | Typical connection | Quick test |
|---|---|---|---|
| Keyboard | Input | USB, Bluetooth, PS/2 | Press keys in a text editor; Num Lock LED |
| Mouse | Input | USB, Bluetooth | Pointer moves; optical sensor glows red |
| Scanner | Input | USB, network | Scan a page; check resolution in dpi |
| Monitor | Output | HDMI, DisplayPort, VGA | Test pattern; check native resolution and refresh |
| Printer | Output | USB, Wi-Fi, Ethernet | Print a test page (see Unit 5) |
| Speakers / headset | Output | 3.5 mm, USB, Bluetooth | Sound test |

To **connect and test** a device: power both off if not hot-pluggable, plug in the right port, power on, let the OS install the driver, then open Device Manager (Windows) or run `lsusb` (Linux) and check that there is no yellow warning sign. **USB** versions: 2.0 (480 Mb/s), 3.0/3.1 Gen 1 (5 Gb/s, blue port), 3.2 Gen 2 (10 Gb/s), USB4 (40 Gb/s); the **USB-C** oval plug is only a shape, not a speed. **HDMI** carries video and audio; **DisplayPort** supports high refresh rates and daisy-chaining; **VGA** is analogue and blurs above 1080p.

## 3.8 The power supply unit: types, connectors, testing and failures

A PC **power supply** is a **switched-mode power supply (SMPS)**: it rectifies the 230 V, 50 Hz mains, switches it at tens of kilohertz through a small transformer and regulates several DC rails. This is far lighter and more efficient than an old linear supply.

**Types.** By size: ATX (standard), SFX (small form factor), TFX. By cabling: *non-modular* (all cables fixed), *semi-modular* (24-pin and CPU fixed), *fully modular* (every cable detaches, easier cable management). Inside you will find the mains filter, a bridge rectifier, big primary capacitors, heat sinks, the transformer and a fan.

**Rails and wire colours**

| Colour | Voltage | Feeds |
|---|---|---|
| Yellow | +12 V | CPU, GPU, fans, drive motors |
| Red | +5 V | USB, logic, drives |
| Orange | +3.3 V | RAM, chipset |
| Black | 0 V (ground) | return |
| Blue | −12 V | legacy serial ports |
| Purple | +5 V standby | stays on when the PC is off (power button, USB charging) |
| Green | PS_ON | pulled to ground to switch the PSU on |
| Grey | Power Good | 5 V signal that all rails are stable |

The ATX specification allows **±5 %** on the three main rails: +12 V must lie between 11.4 and 12.6 V, +5 V between 4.75 and 5.25 V, and +3.3 V between 3.135 and 3.465 V.

**Connectors and their purposes**

| Connector | Pins | Use |
|---|---|---|
| ATX main | 24 (20+4) | Motherboard power |
| EPS / CPU | 4+4 or 8 | CPU power (+12 V) |
| PCIe | 6+2 | Graphics card (up to 150 W per 8-pin); 12VHPWR 16-pin for the newest GPUs |
| SATA power | 15 | HDD, SSD, optical |
| Molex | 4 | Old IDE drives, fans, RGB hubs |

All connectors are **keyed** (D-shaped or notched) so they cannot be inserted wrongly; never force one.

**Efficiency (80 PLUS).** The certificate guarantees minimum efficiency at 20, 50 and 100 % load on 115 V mains: Bronze 82 / 85 / 82 %, Silver 85 / 88 / 85 %, Gold 87 / 90 / 87 %, Platinum 90 / 92 / 89 %, Titanium 92 / 94 / 90 %. A Gold unit at 50 % load wastes about 10 % as heat.

::: example Worked example: wall power and heat for a 400 W load
A PC draws 400 W on the DC side. With an 85 % efficient (Bronze at 50 % load) PSU the mains input is 400 / 0.85 = **470.6 W**, and **70.6 W** is lost as heat. A 90 % efficient unit draws 400 / 0.90 = 444.4 W. Running 8 hours a day for 30 days, the saving is (470.6 − 444.4) × 8 × 30 / 1000 = **6.3 kWh** a month.
:::

```svgfig label="3.3" caption="ATX 24-pin connector, pin by pin (pins 1 to 12 in the lower row, 13 to 24 in the upper row, as in the ATX specification). Colour tells you the voltage; the green wire on pin 16 is the one shorted to ground in a bench test."
f = Fig(760, 210)
top = [("13", "+3.3 V", "#d97706"), ("14", "-12 V", "#2563eb"), ("15", "GND", "#111827"), ("16", "PS_ON", "#16a34a"), ("17", "GND", "#111827"), ("18", "GND", "#111827"), ("19", "GND", "#111827"), ("20", "NC", "#9ca3af"), ("21", "+5 V", "#dc2626"), ("22", "+5 V", "#dc2626"), ("23", "+5 V", "#dc2626"), ("24", "GND", "#111827")]
bot = [("1", "+3.3 V", "#d97706"), ("2", "+3.3 V", "#d97706"), ("3", "GND", "#111827"), ("4", "+5 V", "#dc2626"), ("5", "GND", "#111827"), ("6", "+5 V", "#dc2626"), ("7", "GND", "#111827"), ("8", "PWR_OK", "#6b7280"), ("9", "+5 VSB", "#7c3aed"), ("10", "+12 V", "#ca8a04"), ("11", "+12 V", "#ca8a04"), ("12", "+3.3 V", "#d97706")]
for i, (n, t, c) in enumerate(top):
    f.box(10 + i * 62, 20, 56, 50, n + "\n" + t, fill="#ffffff", stroke=c, size=10, bold=True)
for i, (n, t, c) in enumerate(bot):
    f.box(10 + i * 62, 90, 56, 50, n + "\n" + t, fill="#ffffff", stroke=c, size=10, bold=True)
f.text(380, 168, "Bench test: with the PSU unplugged from the board, join pin 16 (green) to any black (GND) pin with a jumper.", size=10.5, color=NAVY, bold=True)
f.text(380, 192, "The fan spins if the PSU is alive. Always test under a real load too; a fan spinning does not prove the rails are correct.", size=10, color=SLATE)
```

### Testing a PSU

1. **Visual.** Unplug the mains; look for bulging capacitors, burnt smell, melted or discoloured connector pins, dust-blocked fan.
2. **PSU tester.** Plug the 24-pin, CPU and SATA connectors into the tester; LEDs or a display show each rail and Power Good.
3. **Multimeter** (DC volts, 20 V range). Switch the PSU on with the paperclip test (above), connect the black probe to a black wire, and touch the red probe to the metal pin of each coloured wire from the back of the connector. Compare with the ±5 % limits.
4. **Under load.** Voltages that are right with no load can sag when a drive or dummy load is attached; check again with an old PC or dummy load connected.

**Common PSU failures:** no power and no fan (blown fuse, failed primary capacitors), random restarts under load (aged capacitors, overload), burnt 24-pin pins (loose contact), fan failure and overheating shutdown, noisy coil whine, a +12 V rail below 11.4 V.

::: caution Safety tips for handling PSUs
Never open a PSU case: the primary capacitors can hold a dangerous charge for minutes after unplugging, and the mains side is lethal. Do not repair a PSU in a student lab; replace it. Keep liquids away, never block the fan and use a surge protector or UPS in Nepal's fluctuating supply.
:::

## 3.9 Compatibility checklist

1. **CPU socket** equals the motherboard socket; the chipset supports that CPU generation (BIOS update may be needed).
2. **RAM type** (DDR4 or DDR5) matches the board; speed is supported.
3. **Case form factor** accommodates the board; **GPU length** and **cooler height** fit.
4. **PSU** has enough wattage and the right connectors.
5. **Storage interface**: M.2 slot supports NVMe (and/or SATA); enough SATA ports.
6. **OS** supports the hardware (for example Windows 11 requires UEFI with Secure Boot and TPM 2.0).

## 3.10 Calculations for choosing parts

**(a) Power supply sizing.** Sum the component peak draws and add 30 to 50 % headroom, then round up to a standard rating.

::: example Worked example
CPU 65 W + graphics card 150 W + motherboard, RAM, SSD, HDD and fans about 60 W = 275 W. With 50 % headroom: 275 × 1.5 = 412 W, so choose a **450 W** (or better 500 W) 80 PLUS Bronze unit. At 50 % load a Bronze supply is about 85 % efficient (82 % guaranteed), so its input draw is 275 / 0.85 ≈ 324 W from the wall.
:::

**(b) Memory bandwidth.** Peak bandwidth = transfer rate × bus width. DDR memory uses a 64-bit (8-byte) channel: DDR4-3200 gives 3200 × 10⁶ × 8 B = **25.6 GB/s** per channel; dual channel doubles it to 51.2 GB/s. DDR5-5600 gives 5600 × 8 = 44.8 GB/s per channel.

**(c) Interface speeds.** SATA III signals at 6 Gb/s with 8b/10b encoding (10 bits on the wire per data byte): 6 × 10⁹ / 10 = **600 MB/s**, giving real SATA SSDs about 550 MB/s. NVMe on **PCIe 3.0 x4**: 8 GT/s per lane with 128b/130b encoding, so 8 × (128/130) / 8 = 0.985 GB/s per lane; four lanes = **3.94 GB/s**. PCIe 4.0 doubles that to 7.88 GB/s.

**(d) How long does a copy take?** Copying 50 GB at 100 MB/s (a HDD) takes 50,000 / 100 = 500 s ≈ **8.3 min**; at 500 MB/s (SATA SSD), 100 s; at 3,000 MB/s (NVMe), about 17 s.

**(e) Storage marketing vs reality.** A "1 TB" drive is 10¹² bytes; Windows reports capacity in binary units: 10¹² / 2³⁰ = **931 GiB** (shown as "931 GB"). Nothing is missing; the units differ.

**(f) RAID capacity.** With n drives of size S: RAID 0 (striping) = n × S, no redundancy; RAID 1 (mirror) = S (two drives); RAID 5 = (n − 1) × S, survives one failure; RAID 6 = (n − 2) × S, survives two; RAID 10 = (n/2) × S.
For four 2 TB drives: RAID 0 = 8 TB, RAID 5 = 6 TB, RAID 6 = 4 TB, RAID 10 = 4 TB. **RAID is not a backup**: it will happily copy accidental deletion, ransomware and fire damage.

**(g) UPS sizing.** UPS capacity is in VA; real power (W) = VA × power factor (about 0.6 for small units). A 300 W load needs at least 300 / 0.6 = 500 VA; add 25 % headroom: 625 VA, so buy a **650 or 700 VA** unit. A 12 V 7 Ah battery stores 84 Wh; at 85 % inverter efficiency and a 300 W load: 84 × 0.85 / 300 ≈ 0.24 h ≈ **14 minutes at best**, enough to save and shut down properly.

## 3.11 Eight rules of safe and careful workshop practice

1. **Switch off and unplug first.** Turn off the PSU switch and pull the power cable before opening the case. Even when the computer is "off", the motherboard keeps a small standby voltage. This one habit prevents most shocks and burnt boards.
2. **Discharge static electricity.** Wear an anti-static strap clipped to bare case metal, or touch the metal often. A spark you cannot feel (below 3,000 V) can still kill a RAM chip. Dry winter air in Kathmandu makes static much worse.
3. **Never open a power supply.** The capacitors inside hold dangerous voltage for days after unplugging. Replace a faulty PSU as a whole and never repair it in a college lab. A shock from it can stop the heart.
4. **Handle parts by the edges.** Hold RAM, cards and the motherboard by their edges, never by the gold contacts or chips. Keep parts in their anti-static bags until use. Oil from fingers and tiny scratches cause hidden faults.
5. **Use the right tool and the right force.** Use a magnetic Phillips screwdriver, and tighten only until snug. Parts should slide in with firm, even pressure; if they do not, check the notch and the direction. Forcing a CPU or RAM stick bends pins and breaks slots.
6. **Keep a tidy bench.** Work on a clean, dry, non-metal table with the screws in a small tray. Label cable positions with a photo before removing them. A lost screw under the motherboard can cause a short circuit.
7. **Protect the data.** Back up important files before opening, formatting or reinstalling. A technician is trusted with a customer's photos, accounts and exam files. Never view or copy private data.
8. **Think about people and environment.** Lift heavy cases with a straight back, keep cables out of walkways and use a fire extinguisher rated for electrical fires. Hand old batteries, monitors and boards to an e-waste collector instead of burning or dumping them. Nepal has few recycling points, so responsible disposal is part of the job.

## Formula and fact sheet

- ESD: wrist strap, anti-static bags, touch the case. Never open a PSU.
- Compatibility: socket, RAM type, form factor, PSU wattage and connectors, storage interface, OS requirements.
- PSU watts = (sum of component peak) × 1.3 to 1.5.
- RAM bandwidth = MT/s × 8 bytes. SATA III ≈ 600 MB/s; PCIe 3.0 ≈ 0.985 GB/s per lane.
- 1 TB (decimal) = 931 GiB. RAID 5 = (n − 1)S; RAID 10 = (n/2)S.
- UPS VA = W / 0.6; add headroom.

## Chapter summary

- Protect yourself and the parts: unplug, discharge static, never open a PSU.
- The toolkit is small and cheap; a multimeter, crimper and a bootable USB solve most jobs.
- Every component has a few specifications that decide compatibility and performance.
- Simple arithmetic selects the PSU, UPS and storage layout and explains real speeds and capacities.

## Practice

1. List six safety precautions before opening a computer.
2. Why is it dangerous to open a PSU, and what should you do if it is faulty?
3. Name the main parts of a motherboard and the purpose of the CMOS battery.
4. A PC uses a 95 W CPU, a 200 W GPU and about 80 W of other parts. Choose a PSU rating.
5. Find the peak bandwidth of dual-channel DDR4-2666.
6. How long to copy 120 GB over SATA III (assume 500 MB/s) and over a USB 3.0 HDD (assume 100 MB/s)?
7. How many GiB is a "500 GB" drive?
8. Compute the usable capacity of five 4 TB drives in RAID 5 and RAID 6.
9. Choose a UPS for a PC and monitor drawing 250 W.
10. A PC will not accept the new CPU in the old board. List three compatibility checks.

::: note Answers and worked solutions
**1.** Shut down and unplug; press power to discharge; wear a wrist strap or touch the case; remove jewellery; use anti-static bags; clear dry, well-lit workspace.
**2.** Capacitors in the PSU keep a lethal charge after unplugging. Replace a faulty PSU as a unit; never repair it.
**3.** CPU socket, chipset, RAM slots, PCIe slots, M.2/SATA connectors, BIOS chip, front-panel header, power connectors. The CMOS battery keeps the real-time clock and BIOS settings when the PC is off.
**4.** 95 + 200 + 80 = 375 W; × 1.4 ≈ 525 W, so a **550 W** 80 PLUS Bronze or better.
**5.** 2666 × 8 = 21.3 GB/s per channel; dual channel = **42.6 GB/s**.
**6.** 120,000 MB / 500 = **240 s = 4 min**; 120,000 / 100 = 1,200 s = **20 min**.
**7.** 500 × 10⁹ / 2³⁰ = **465.7 GiB**.
**8.** RAID 5 = (5 − 1) × 4 = **16 TB**; RAID 6 = (5 − 2) × 4 = **12 TB**.
**9.** 250 / 0.6 = 417 VA; with 25 % headroom 521 VA, so a **600 VA** unit (runtime a few minutes).
**10.** The CPU socket matches; the chipset and BIOS version support the CPU; the cooler fits that socket (and the PSU can supply its TDP).
:::

### More practice: memory, storage, interfaces and the PSU

11. Distinguish DRAM from SRAM and state where each is used.
12. List the types of ROM from mask ROM to flash, with how each is programmed and erased.
13. Calculate the peak bandwidth of one DDR4-3200 module (64-bit bus).
14. Explain the roles of the northbridge and southbridge and what happened to them in modern CPUs.
15. Compare PATA, SATA and NVMe for connector, speed and use.
16. How would you recognise a fake 2 TB SSD in the lab?
17. Give the voltage and colour of each rail of the ATX 24-pin connector, and the ATX tolerance for +12 V.
18. A PC draws 300 W on the DC side through an 88 % efficient PSU. Find the input power and the heat lost.
19. Describe the paperclip test and its limits.
20. State five safety tips for handling a PSU.

::: note Answers to 11 to 20
**11.** DRAM stores bits as charge in capacitors needing refresh (main memory); SRAM uses flip-flops, needs no refresh, is faster and costlier (cache).
**12.** Mask ROM (factory), PROM (once, programmer), EPROM (programmer, UV erase), EEPROM (electric, byte-wise), Flash (electric, block-wise).
**13.** 3,200 MT/s × 8 bytes = **25,600 MB/s** (25.6 GB/s).
**14.** The northbridge linked the CPU to RAM and graphics; the southbridge handled slow I/O. Today the memory controller and PCIe lanes sit in the CPU and one chipset (PCH) replaces the southbridge.
**15.** PATA: 40-pin ribbon, up to 133 MB/s, master/slave. SATA: 7-pin, 600 MB/s. NVMe: PCIe in M.2, 2,000 to 7,000+ MB/s.
**16.** Price too low for capacity, errors after filling, H2testw or f3 shows real capacity far below the label, mismatch in CrystalDiskInfo.
**17.** +3.3 V orange, +5 V red, +12 V yellow, −12 V blue, +5 VSB purple; +12 V must be 11.4 to 12.6 V (±5 %).
**18.** 300 / 0.88 = **340.9 W** input; **40.9 W** heat.
**19.** Join the green PS_ON wire (pin 16) to a black wire; the PSU starts and the fan runs. It shows only that the PSU can switch on, not that the rails hold correct voltage under load.
**20.** Do not open it; unplug before connecting; do not force keyed plugs; keep the fan clear; use surge protection or a UPS.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). List the safety precautions a technician must follow while assembling or repairing a PC. Why is ESD dangerous?**

**Electrostatic discharge (ESD)** is a sudden flow of static charge between two objects at different voltages. A person can carry 3,000 V or more without feeling anything, while a RAM or CPU chip can be damaged by only 100 V, so the part may be killed or weakened without any visible sign. Its failure may appear weeks later as random crashes.

*Precautions* (see Plate 3.1):

1. Switch off the PSU, unplug the mains cable and press the power button once to drain the board.
2. Wear an anti-static wrist strap clipped to bare case metal, or touch the case frequently.
3. Work on a clean, dry bench; avoid carpet and nylon clothes.
4. Hold components by their edges and keep them in anti-static bags.
5. Never open a power supply, and never use a metal tool near live circuits.
6. Use the correct screwdriver and do not force any part.
7. Back up data before starting, and dispose of old parts as e-waste.

| Hazard | Cause | Prevention |
|---|---|---|
| Electric shock | live PSU or monitor | unplug; never open PSU |
| ESD damage | static from body | wrist strap, edges only |
| Cuts | sharp case edges | careful handling, gloves |
| Short circuit | loose screw, wet bench | tidy dry bench |
| Fire | overloaded socket | surge-protected strip, extinguisher |

**Q (10 marks). Describe the main components of a desktop PC and explain how to choose compatible parts. A student plans a PC with a 65 W CPU and a 150 W graphics card; calculate the power supply rating.**

*Introduction.* A desktop PC is built from separate, standard parts that are joined by the motherboard (Figure 3.1). Knowing the job and the main specification of each part allows a technician to choose a balanced and compatible system.

*Components and key specifications* (Plate 3.2).

1. **Case:** holds and cools the parts; sizes ATX, micro-ATX and mini-ITX; has fans, drive bays and the front-panel connectors.
2. **Motherboard:** the main circuit board; its **socket** decides the CPU, its **slots** decide the RAM type and number of cards, and its **chipset** decides features.
3. **CPU:** the processor; judged by cores, threads, clock speed (GHz) and cache; needs a cooler and thermal paste.
4. **RAM:** the working memory, such as 8 GB DDR4; must match the board's DDR generation and speed.
5. **Storage:** HDD (cheap, large, slow) or SSD (SATA or NVMe, fast); the OS should be on an SSD.
6. **PSU:** converts 220 V AC to the 12 V, 5 V and 3.3 V used inside; rated in watts and 80 PLUS efficiency.
7. **Graphics card:** needed for games and design; many CPUs have a built-in GPU that is enough for office work.
8. **Ports and cooling:** USB, HDMI, LAN and audio ports; fans or a liquid cooler remove heat.

*Compatibility rules.* (1) CPU socket = motherboard socket (for example AM4 or LGA1700). (2) RAM generation (DDR4 or DDR5) = board support, because the notches differ. (3) Case form factor must fit the board. (4) The graphics card must fit the case length and have the power connectors from the PSU. (5) The PSU must supply enough watts and the right connectors.

*Power supply calculation.* Add the maximum power of the parts: CPU 65 W + graphics 150 W + motherboard and RAM 40 W + SSD and HDD 15 W + fans 10 W = **280 W**. Allow a 40 to 50 % margin for peaks and ageing: 280 × 1.5 = 420 W. The next standard size is a **450 W** PSU (a 500 W unit is a safer choice). A PSU run near its full rating is hot, noisy and short-lived.

| Part | Match with | Example mismatch |
|---|---|---|
| CPU | motherboard socket | LGA1700 CPU on an AM4 board |
| RAM | board DDR type | DDR5 stick in a DDR4 slot |
| Board | case form factor | ATX board in a mini-ITX case |
| GPU | slot, case length, PSU connectors | 300 mm card in a 250 mm case |
| PSU | total watts | 300 W PSU for a 420 W build |

*Conclusion.* A good PC is a balanced one: a fast CPU with slow memory or an undersized PSU wastes money and causes faults. Check the compatibility table before buying any part.

**Q (5 marks). Differentiate between RAM and ROM and name the types of ROM.**

RAM is volatile read-write main memory (DRAM for main memory, SRAM for cache); the data vanishes when power is cut. ROM is non-volatile and holds firmware such as the BIOS. The types are mask ROM (programmed at the factory), PROM (programmed once by the user), EPROM (erased with ultraviolet light), EEPROM (erased electrically, byte by byte) and flash (erased in blocks, used for BIOS/UEFI chips and SSDs).

**Q (10 marks). Describe the PC power supply: its types, connectors, voltage rails, and how it is tested.**

*Introduction.* The PSU is a switched-mode supply that converts 230 V AC to regulated DC rails.

*Types.* ATX, SFX and TFX by size; non-modular, semi-modular and fully modular by cabling; 80 PLUS ratings for efficiency.

*Connectors and rails.* 24-pin ATX (+3.3, +5, +12, −12, +5 VSB, PS_ON, Power Good), 4+4 pin EPS for the CPU, 6+2 pin PCIe for graphics, SATA and Molex for drives. Colours: yellow +12 V, red +5 V, orange +3.3 V, black ground (Figure 3.3).

*Testing.* Inspect visually; use a PSU tester; or short the green wire to a black wire (paperclip test), then measure each rail with a multimeter against ±5 % limits, ideally under load.

*Failures and safety.* Bulging capacitors, dead fan and burnt pins are common; never open the unit and always unplug before connecting.
