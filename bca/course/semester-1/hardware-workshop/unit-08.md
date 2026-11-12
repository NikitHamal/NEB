---
subject: Hardware Workshop
grade: BCA Semester 1
unit: 8
title: Maintenance and Upgrade
area: BCA 106 · Hardware Workshop · Unit 8
---

A computer is not finished when it is built. Dust builds up, paste dries, batteries age and software grows heavier. Regular maintenance keeps a machine reliable, and a well-chosen upgrade often gives a three-year-old PC another three years. This unit covers upgrade planning, memory, storage, graphics and CPU upgrades, firmware updates, cleaning, thermal paste, laptop battery care, airflow and health monitoring.

::: key What this unit gives you
- Upgrade planning and compatibility checks with CPU-Z, Speccy and the Crucial System Scanner.
- RAM, storage (SSD, NVMe, cloning, alignment), GPU and CPU upgrades.
- Preventive maintenance: cleaning, thermal paste replacement, laptop battery care, BIOS/UEFI updates and cable management.
- Health monitoring: SMART, MemTest86+, temperatures and stress tests.
:::

## 8.1 Upgrade planning and compatibility checks

Before buying anything answer four questions: **What is slow?** (find the bottleneck), **What does the board support?** (socket, chipset, RAM type and maximum), **Will the power supply cope?** and **Does it physically fit?**

| Check | Where to look | Example |
|---|---|---|
| CPU socket and chipset | Board manual, vendor CPU support list, CPU-Z "Mainboard" tab | LGA1700 board supports 12th to 14th gen after a BIOS update |
| RAM type and maximum | Manual, CPU-Z "Memory" and "SPD" tabs, Crucial scanner | DDR4, 4 slots, 128 GB maximum |
| Laptop limits | Service manual and the vendor's page | RAM maximum 32 GB, one free M.2 slot, soldered RAM on thin models |
| PSU wattage and connectors | PSU label | 550 W, one 6+2 PCIe cable |
| Case space | Measure length and cooler height | GPU up to 320 mm, cooler up to 160 mm |

**Tools.** **CPU-Z** reports CPU, board, RAM and SPD; **Speccy** gives a full hardware inventory with temperatures; the **Crucial System Scanner** lists compatible memory and SSDs; **HWMonitor** and **Core Temp** read temperatures; **CrystalDiskInfo** reads SMART data. Always read the manufacturer's documentation for the exact model.

::: example Worked example: is the PSU big enough for a GPU upgrade?
Current system: CPU 95 W, other parts 80 W, old GPU 75 W. New GPU needs 200 W. New peak load = 95 + 80 + 200 = **375 W**. Add a 30 % margin: 375 × 1.3 = **487.5 W**, so a **550 W** unit is the minimum; the existing 450 W PSU is too small and the card also needs a PCIe 8-pin connector the old PSU lacks.
:::

## 8.2 Memory (RAM) upgrades

1. **Match the type:** DDR4 and DDR5 are not interchangeable; desktops use **DIMM**, laptops use shorter **SO-DIMM**.
2. **Match speed and voltage:** a faster module runs at the speed of the slowest module in the system; mixing capacities works but mixing speeds wastes performance.
3. **Use dual channel:** two identical modules in the correct slots (usually A2 and B2, as the manual says) double the data path from 64 to 128 bits.
4. **Fit it:** power off, unplug, strap on, open the clips, press the module straight down until both clips click.
5. **Check in BIOS/UEFI** that the full capacity is detected; turn on **XMP** or **EXPO** to run at the advertised speed.

::: example Worked example: dual-channel bandwidth
One DDR4-3200 module: 3,200 MT/s × 8 bytes = 25.6 GB/s. Two modules in dual channel: **51.2 GB/s**. For a PC that uses integrated graphics, which shares system RAM, going from one 8 GB stick to two 8 GB sticks gives a clearly visible gain in games and video editing. The 32-bit Windows limit is about 4 GB, so a 64-bit OS is needed for more.
:::

## 8.3 Storage upgrades

| Drive | Speed | Boot time (typical) | Durability |
|---|---|---|---|
| HDD (7200 rpm) | 100 to 200 MB/s | 40 to 60 s | Moving parts; shock sensitive |
| SATA SSD | about 550 MB/s | 10 to 15 s | No moving parts |
| NVMe SSD (PCIe 4.0) | 5,000 to 7,000 MB/s | 8 to 12 s | No moving parts; may throttle when hot |

**Upgrade by cloning.** Fit the new drive (or a USB enclosure), run cloning software (Macrium Reflect, Clonezilla, or the SSD maker's tool), select the old drive as *source* and the new as *destination*, resize the main partition, then swap the drives, boot, and confirm that all data is present. Back up first and **never clone onto a drive that contains data you need**.

**Partition alignment.** SSD pages are 4 KB and erase blocks are larger, so partitions should start on a **1 MiB boundary**. Windows 10 and 11, current Linux installers and cloning tools do this by default; an old MBR-aligned layout (63 sectors) can cut write speed and shorten life. Also enable **AHCI/NVMe mode** in BIOS, leave TRIM on and do not defragment an SSD.

## 8.4 Graphics card (GPU) upgrade

1. **Power:** check the PSU wattage and the connectors (6+2 pin PCIe, 12VHPWR) against the card's requirement.
2. **Space:** measure case length and the width in slots (two-slot or three-slot card).
3. **Slot:** a PCIe x16 slot (Gen 3 or 4 both work).
4. **Cooling:** the case needs airflow to exhaust the card's heat.
5. **Install:** switch off, remove the old card (release the slot latch), insert the new card until the latch clicks, screw the bracket, connect PCIe power, boot.
6. **Drivers:** remove the old driver (DDU tool if switching vendor), install the latest driver, and check the temperature under load.

## 8.5 CPU upgrade (desktop)

Check **socket type** (LGA1700 versus AM5 are physically different), **chipset support** and the **BIOS version** (an older BIOS may not recognise a newer CPU; update it first with the old CPU installed), the **TDP** against the cooler and VRM, and the RAM type the new CPU supports.

**Install.** Lift the socket lever, lift the old CPU by its edges, drop the new CPU in with the **triangle marker aligned** (no force), lower the lever, clean old paste with isopropyl alcohol, apply a **pea-sized drop** of paste in the centre, and fit the cooler with even pressure across the diagonal screws. **Test:** boot, check CPU-Z, and run **Prime95** or **AIDA64** for 15 to 30 minutes while a monitor shows temperatures; load temperatures below about 85 °C are acceptable, and above 95 °C means a mounting or paste problem.

```svgfig label="8.1" caption="Upgrade decision flow. Find the bottleneck first, then check compatibility, power and space; only then buy. Always back up data before opening the case, and verify the result with a benchmark or a health tool."
f = Fig(760, 150)
steps = ["Find the\nbottleneck", "Check board,\nBIOS, RAM type", "Check PSU\nand space", "Back up,\ninstall part", "Update BIOS\ndrivers", "Test: stress,\ntemperatures"]
for i, t in enumerate(steps):
    x = 8 + i * 125
    f.box(x, 30, 108, 56, t, fill=BLUE if i < 3 else SOFT, stroke=NAVY, size=10.5, bold=True)
    if i < 5: f.arrow([(x + 108, 58), (x + 125, 58)], color=NAVY)
f.text(380, 124, "Blue: planning (nothing bought or opened yet).  White: doing and verifying.", size=10.5, color=SLATE)
```

## 8.6 Preventive maintenance: cleaning internal components

**Schedule.** Clean desktops every 6 months (every 3 in dusty rooms, which includes many Nepali towns in the dry season); check laptops twice a year. Cooling is the main target because dust acts as a blanket.

1. Shut down, unplug the mains, press the power button to drain residual charge, and strap on.
2. Take the PC outdoors or into a ventilated area; use **compressed air** in short bursts, holding the fan blades still with a finger so they do not over-spin.
3. Use a soft brush on heat-sink fins, fan blades and slots; wipe contacts and fan blades with a cloth dampened with **isopropyl alcohol (90 % or more)**.
4. Clean the **power supply** vents from outside; **never open the PSU**.
5. Wipe the case, filters and fan guards; refit and check that every fan spins.
6. **Laptops:** open the service panel, blow the vents and fan from the exhaust side in short bursts, and brush gently; take care of the small ribbon and fan connectors, which break easily. Never use a household vacuum cleaner on electronics because it builds static electricity.

## 8.7 Thermal paste replacement (advanced task)

Thermal paste fills microscopic gaps between the chip and the cooler plate so heat flows across. It dries and cracks in 2 to 5 years.

1. Power off, unplug, remove the cooler (twist gently to break the paste seal).
2. Wipe old paste from both surfaces with isopropyl alcohol and a lint-free cloth or coffee filter until they shine.
3. Apply a **pea-sized drop** (about 4 to 5 mm) of paste in the centre of the CPU or GPU die.
4. Refit the cooler straight down and tighten the screws in a diagonal order so pressure is even.
5. Reconnect the fan cable, boot, and monitor temperatures for 15 minutes with **HWMonitor** or **Core Temp**.

::: example Worked example: checking the result
Before repasting: idle 62 °C, load 94 °C (throttling). After: idle 38 °C, load 71 °C. A fall of 23 °C at load shows the paste had dried out. If the temperatures are unchanged, check that the cooler is seated flat and that the protective film on the cooler base was removed.
:::

## 8.8 Battery care for laptops

A laptop uses a **lithium-ion** or lithium-polymer pack, rated in watt-hours (Wh = volts × amp-hours) and in charge cycles (typically 300 to 500 before the capacity falls to about 80 %).

- Avoid keeping the battery at 100 % on mains for months; use the vendor's charge limit (for example 80 %) where available.
- Avoid deep discharges to 0 % often; Li-ion likes partial charges.
- **Calibrate** every 3 to 6 months (full charge, then use until it shuts down, then full charge again) so that the percentage indicator is accurate.
- Keep the laptop cool; heat ages the cells faster than anything else.
- **Replace a swollen or degraded battery immediately.** A bulging pack is a fire hazard: stop using it, do not charge or puncture it and dispose of it at a recycling point.

::: example Worked example: battery runtime
A pack is 11.1 V, 4.4 Ah: 11.1 × 4.4 = **48.8 Wh**. At an average draw of 15 W the new pack lasts 48.8 / 15 = **3.3 h**. When it has aged to 80 % of its capacity, it holds 39.1 Wh and lasts **2.6 h**. Windows can create a battery report with `powercfg /batteryreport`.
:::

## 8.9 BIOS/UEFI and firmware updates

Update the BIOS only when there is a reason: a **security patch**, **support for new hardware** (a newer CPU), or a fix for a known fault. If everything works, leave it alone.

1. Identify the exact board model and the current BIOS version (CPU-Z, or `systeminfo`).
2. Download only from the **manufacturer's site**; read the release notes.
3. **Back up the current settings** (write them down or save a profile).
4. Connect the laptop to mains (and a UPS for a desktop); never interrupt the flash.
5. Use the vendor's flash tool or the **BIOS Flashback / EZ Flash / Q-Flash** menu from a FAT32 USB drive.
6. After the update reset to defaults, then re-enter settings (boot mode, XMP, fan curves).

**A failed or interrupted flash can "brick" the board.** Boards with dual BIOS or BIOS Flashback can recover; others need a programmer. The same rules apply to firmware for SSDs, routers and printers.

## 8.10 Cable management and airflow

- **Route cables behind the motherboard tray** and tie them with Velcro straps or cable ties; use case grommets.
- Keep cables away from fans and the CPU cooler so they do not stop a blade.
- Plan airflow: **front and bottom intake, rear and top exhaust** (cool air in, hot air out); slightly more intake than exhaust gives positive pressure and fewer dust leaks.
- Keep intakes and vents unobstructed, with the case 10 cm from walls; use dust filters and clean them monthly.
- Check that all fans spin and point in the right direction (arrows on the frame show airflow and rotation).

## 8.11 Health monitoring and diagnostics

| What | Tool | What to look for |
|---|---|---|
| Disk health | **CrystalDiskInfo** (SMART) | Status Good; no rising *Reallocated sectors* (05) or *Current pending sectors* (C5); watch temperature and power-on hours |
| Memory | **MemTest86+** (boot from USB) or Windows Memory Diagnostic | Zero errors after at least one full pass (preferably 4) |
| CPU and GPU temperatures | HWMonitor, Core Temp, MSI Afterburner | Idle 30 to 45 °C; sustained load below 85 °C |
| Stability | Prime95, AIDA64, FurMark | No crash or throttling in 30 minutes |
| Battery | `powercfg /batteryreport` | Full-charge capacity compared with design capacity |

Run SMART checks monthly, memory tests every few months and after any RAM change, and temperature checks after each cleaning or hardware change. A rising count of reallocated sectors warns that a drive is failing: **back up now**.

## 8.12 Eight rules for maintenance and upgrades

1. Back up before every upgrade.
2. Check compatibility, power and space before buying.
3. Change one part at a time and test after each.
4. Clean on a schedule; do not wait for overheating.
5. Never open a PSU, never use a household vacuum on electronics.
6. Replace swollen batteries immediately.
7. Flash firmware only for a reason, on stable power.
8. Record every change and its test result in the log.

## Formula and fact sheet

- Wh = V × Ah; runtime = Wh / watts drawn.
- Dual-channel bandwidth = 2 × (MT/s × 8 bytes). DDR4-3200: 25.6 GB/s per channel.
- PSU size ≈ (CPU + GPU + other) × 1.3.
- Clean desktops every 6 months; calibrate laptop batteries every 3 to 6 months; replace paste every 2 to 5 years.
- SMART warning attributes: 05 (reallocated), C5 (pending), C6 (uncorrectable).
- Load temperature target below 85 °C.

## Chapter summary

- Plan the upgrade with the board manual and tools such as CPU-Z, Speccy and the Crucial scanner; check socket, RAM type, PSU and space.
- RAM must match type, speed and form factor, and runs best in dual channel; SSD upgrades use cloning and aligned partitions.
- Preventive maintenance means cleaning with compressed air, a soft brush and isopropyl alcohol, fresh paste, careful battery use and tidy airflow.
- Update firmware only when needed, and never interrupt it.
- Monitor SMART, memory, temperatures and stability, and keep a log.

## Practice

1. List the compatibility checks before a CPU upgrade.
2. A PC has CPU 65 W, other parts 70 W and will receive a 150 W GPU. Choose a PSU.
3. Calculate dual-channel DDR4-2666 bandwidth.
4. Describe how to clone a 500 GB HDD to a 500 GB SSD.
5. Why is partition alignment important for SSDs?
6. Describe the steps to replace thermal paste.
7. A laptop battery is 14.8 V, 3 Ah. Find Wh and runtime at 20 W.
8. When should the BIOS be updated and what are the risks?
9. Explain a good airflow design for a tower case.
10. Which SMART attributes warn of a failing disk?

::: note Answers and worked solutions
**1.** Socket, chipset support, BIOS version, TDP versus cooler/VRM, RAM type, and the cooler's mounting bracket.
**2.** 65 + 70 + 150 = 285 W; × 1.3 = 370.5 W; choose **450 W** (or 500 W) with a PCIe power cable.
**3.** 2,666 × 8 = 21,328 MB/s per channel; dual channel = **42.7 GB/s**.
**4.** Fit the SSD (or USB enclosure), start cloning software, source HDD, destination SSD, resize if needed, run, shut down, swap, boot, verify.
**5.** Misaligned partitions make each write touch two flash pages, which slows writes and wears the drive faster; align at 1 MiB.
**6.** Remove the cooler, clean both surfaces with isopropyl alcohol, apply a pea-sized drop, refit, tighten diagonally, test temperatures.
**7.** 14.8 × 3 = **44.4 Wh**; 44.4 / 20 = **2.2 h**.
**8.** For security fixes, new hardware support or a known bug; risk of a bricked board if power fails or the wrong file is used.
**9.** Front and bottom intake, rear and top exhaust, filters, tidy cables, space around the case.
**10.** Reallocated sectors (05), current pending sectors (C5), uncorrectable sectors (C6), rising temperature, and a status other than Good.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Explain how to upgrade the RAM of a PC.**

Find the memory type and the maximum supported with the board manual or the Crucial scanner; buy modules of the same type (DDR4 or DDR5), form factor (DIMM or SO-DIMM) and matching speed. Switch off, unplug and wear a strap; open the slot clips, press the module in until both clips click; for dual channel use matching modules in the slots the manual names. Boot into BIOS, check the capacity, enable XMP, and run MemTest86+ to confirm.

**Q (10 marks). Describe the preventive maintenance of a desktop and a laptop.**

*Introduction.* Preventive maintenance prevents failures by dealing with heat, dust, wear and software problems before they cause damage.

*Cleaning.* Every six months, with the PC off and unplugged, blow out dust with compressed air in short bursts, brush the heat sinks and fans, and wipe with isopropyl alcohol; clean the PSU only from outside; for a laptop clean the vents and fan carefully.

*Thermal paste.* Replace dried paste with a pea-sized drop and check the temperatures with HWMonitor.

*Battery.* Avoid deep discharges and constant 100 %; calibrate every 3 to 6 months; replace a swollen battery at once.

*Firmware.* Update BIOS only when necessary, after a backup and on stable power.

*Cables and airflow.* Tidy cables, use filters and keep vents clear (Figure 8.1 shows the upgrade planning flow).

*Monitoring.* Check SMART monthly, run MemTest86+ every few months, and observe temperatures.
