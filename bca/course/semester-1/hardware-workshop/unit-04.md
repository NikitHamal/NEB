---
subject: Hardware Workshop
grade: BCA Semester 1
unit: 4
title: PC and Laptop Assembly
area: BCA 106 · Hardware Workshop · Unit 4
---

This unit is the lab manual for building a desktop computer from parts. Follow it in order, with the motherboard manual open beside you, and you will have a machine that reaches the BIOS screen on its first power-on.

::: key What this unit gives you
- A complete assembly procedure from workspace preparation to first boot.
- Cable management and airflow.
- The meaning of beep codes and POST, and what to do if the PC does not start.
- A lab checklist and a sign-off table.
- BIOS/UEFI setup, operating-system installation, drivers, printer installation and useful commands for Windows and Linux.
- POST codes, beep codes and diagnostic tools (multimeter, PSU tester, POST card) for simulated hardware faults.
:::

## 4.1 Before you start

1. Clear a large bench; lay out anti-static mat; wear the wrist strap.
2. Unbox parts and check against the list: case, PSU, motherboard, CPU, cooler, RAM, storage, GPU (optional), cables, screws, manuals.
3. Read the motherboard manual: socket, RAM slot order, front-panel header layout.
4. Keep the board on its box (a non-conductive surface) for the first steps; do not place it on the bag's *outside*, which can conduct.

```photogrid label="4.1" cols="4" ratio="1.1" caption="Four parts that have a right way round. (a) A CPU: match the corner marker or notches to the socket. (b) A DIMM: one off-centre notch means it fits only one way. (c) An M.2 NVMe drive: one key notch, fixed by a single screw. (d) A CPU cooler with thermal paste already applied to its copper base."
@ photo id="bca101/cpu-i7" cap="CPU (underside contacts)"
fit 1.1
@ photo id="bca101/ram" cap="DDR DIMM with notch"
fit 1.1
@ photo id="bca101/nvme" cap="M.2 NVMe SSD"
fit 1.1
@ photo id="bca106/paste" cap="Cooler with thermal paste"
fit 1.1
call 0.50 0.90 0.50 0.58 "Paste on copper base"
```

```photogrid label="4.2" cols="2" ratio="2.1" caption="The front-panel header, where the case wires are fitted. The small pins carry power switch, reset switch, power LED and HDD LED; polarity matters only for the LEDs (+ and -). The board manual gives the exact pin order."
@ photo id="bca106/jpanel" cap="Front-panel header (JPANEL) on a motherboard"
fit 2.1
call 0.50 0.88 0.60 0.55 "Pin pairs: PWR, RST, LED"
@ svg cap="Typical pin pairs"
f = Fig(380, 180)
for i, (n, c) in enumerate([("PWR SW", RED), ("RESET SW", AMBER), ("PWR LED +/-", TEAL), ("HDD LED +/-", NAVY)]):
    f.box(20, 12 + i * 40, 110, 30, n, fill=SOFT, stroke=c, size=11, bold=True)
    f.arrow([(130, 27 + i * 40), (230, 27 + i * 40)], color=c)
    f.text(240, 32 + i * 40, ["no polarity", "no polarity", "red wire +", "red wire +"][i], size=11, color=SLATE, anchor="start")
```

## 4.2 Step-by-step build

**Step 1: open the case.** Remove both side panels. Note the pre-installed standoffs and the screws bag. If necessary, fit the **I/O shield** (backplate) into the rear cut-out, facing outwards (many boards have it built in).

**Step 2: install the CPU on the motherboard (outside the case is easier).**

- *Intel (LGA):* lift the retention lever and plate; align the **notches** on the CPU edge with the socket; place the CPU gently (do not push, never touch the pins in the socket); lower the plate and lock the lever (the plastic cover pops off by itself).
- *AMD AM4 (PGA):* lift the lever; match the **golden triangle** on the CPU to the arrow on the socket; drop it in with no pressure; lower the lever. *AM5 is LGA like Intel.*

**Step 3: install RAM.** Open the slot clips; align the notch on the module with the key in the slot; press down evenly at both ends until the clips snap. For two modules use the slots the manual recommends (often A2 and B2) for dual channel.

**Step 4: M.2 SSD (if used).** Remove the standoff screw, insert the SSD at about 30° into the M.2 socket, press down and fasten with the screw. Remove any protective film from the heatsink pad.

**Step 5: cooler.** If the cooler has pre-applied paste, remove the cover; otherwise apply a **pea-sized dot** of thermal paste in the centre of the CPU. Place the cooler vertically, tighten the screws **diagonally** in small turns, and connect the fan to the **CPU_FAN** header.

**Step 6: mount the board in the case.** Check the standoffs match the holes of your form factor (ATX, mATX, ITX) and that no extra standoff lies where there is no hole (a short circuit risk). Lower the board, align with the I/O cut-out, and secure it with screws, tightening evenly but not over-tightening.

**Step 7: PSU.** Fit the PSU (fan facing the vent: down if the case has a bottom vent). Secure with four screws. Route cables behind the tray.

**Step 8: connect power.**

- 24-pin ATX to the board edge (the clip clicks).
- 8-pin (4+4) **EPS** CPU power near the CPU. 
- SATA power to drives; PCIe power to the GPU.

**Step 9: drives.** Fasten the SSD/HDD in its bay or bracket; connect **SATA data** (L-shaped, keyed) to the board and **SATA power** from the PSU.

**Step 10: front-panel connectors.** The small header pins are the most error-prone step. Check the manual diagram: **PWR_SW**, **RESET_SW**, **PWR_LED+/−**, **HDD_LED+/−** (LEDs have polarity; switches do not), **USB 3.0** (blue 19/20-pin), **USB 2.0** (9-pin), **HD_AUDIO** (9-pin).

**Step 11: graphics or expansion cards.** Remove the slot cover, insert the card straight into the PCIe x16 slot until the latch clicks, screw it to the case, connect its power cables.

**Step 12: tidy cables.** Bundle cables with ties or Velcro behind the motherboard tray; keep them away from fans and out of the airflow path. Good airflow gives lower temperatures and less noise.

**Step 13: final check before power.** Nothing loose inside the case (a stray screw can short the board); CPU and case fans connected; all power connectors seated; RAM clicks closed; the monitor cable is plugged into the **graphics card** (if one is installed), not the board.

**Step 14: first power-on.** Connect monitor, keyboard, mouse and mains cable; switch on the PSU; press the case power button. Expect fans to spin, then the manufacturer logo and a prompt to enter **BIOS/UEFI** (usually Del or F2). If you reach it, the build is successful. Check in BIOS that the CPU model, RAM size and the storage devices are detected, and watch the CPU temperature for a few minutes.

## 4.3 If it does not start

| Symptom | Likely cause and fix |
|---|---|
| Nothing happens, no fans | PSU switch off; mains cable; 24-pin or 8-pin not seated; power-button header wrong. Short the PWR_SW pins with a screwdriver to test |
| Fans spin, no display | monitor on the wrong port; GPU not seated or power missing; RAM not seated (reseat, try one stick); CPU power missing |
| Beep codes (AMI: one long + continuous short pattern) | AMI: 1 short = OK; continuous = memory or power fault; 1 long + 8 short = display adapter fault. Award: 1 long + 2 short = video error. Always check your board's manual, since codes vary |
| Debug LEDs (CPU / DRAM / VGA / BOOT) | the LED that stays lit points to the stage that failed |
| Restarts or shuts down after a short time | overheating: cooler not seated, no paste, fan not connected |
| "No boot device" | boot order, drive not detected (cable), no OS yet |
| USB or audio ports dead | front-panel header connected wrongly; check rear ports |

**POST** (power-on self-test) is the firmware checking the CPU, RAM, video and drives before handing over to the OS. Error codes or beeps during POST identify a failing component. **Troubleshooting method:** reduce to the minimum (CPU, one RAM stick, board, PSU, GPU if needed), then add parts one at a time and test each.

```svgfig label="4.1" caption="Order of assembly. Parts that go on the open motherboard (CPU, cooler, RAM, M.2) are fitted first because there is more room; then the board goes into the case, followed by drives, PSU cables, the graphics card and a first test."
f = Fig(760, 200)
steps = ["1 Open case\nI/O shield", "2 CPU into\nsocket", "3 Cooler +\npaste", "4 RAM\nin slots", "5 M.2 SSD", "6 Board on\nstandoffs", "7 PSU, drives\nGPU, cables", "8 Front panel\nPOST test"]
for i, s in enumerate(steps):
    x = 12 + (i % 4) * 186; y = 14 + (i // 4) * 96
    f.box(x, y, 150, 56, s, fill=BLUE if i < 5 else SOFT, stroke=NAVY, size=11, bold=True)
    if i % 4 < 3: f.arrow([(x + 150, y + 28), (x + 186, y + 28)], color=NAVY)
f.arrow([(687, 70), (687, 80), (87, 80), (87, 110)], color=AMBER)
f.text(380, 190, "Blue steps: on the board outside the case.  White steps: inside the case.", size=10.5, color=SLATE)
```

```svgfig label="4.2" caption="Decision tree for a PC that does not start. Work from the power outward: mains and PSU switch, then the 24-pin and CPU power, then RAM and the display cable, and finally the POST beeps."
f = Fig(760, 250)
def q(x, y, t): f.box(x, y, 150, 46, t, fill=BLUE, stroke=NAVY, size=10.5, bold=True)
def a(x, y, t): f.box(x, y, 150, 46, t, fill=SOFT, stroke=TEAL, size=10.5)
q(10, 10, "Any fan or LED?"); a(10, 104, "Check mains, PSU switch,\n24-pin, front-panel PWR"); f.arrow([(85, 56), (85, 104)], color=RED, label="no", lpos=(100, 82))
q(210, 10, "Display on screen?"); f.arrow([(160, 33), (210, 33)], color=TEAL, label="yes", lpos=(184, 24))
a(210, 104, "Reseat RAM and GPU,\ncheck monitor cable"); f.arrow([(285, 56), (285, 104)], color=RED, label="no", lpos=(300, 82))
q(410, 10, "Beeps or POST code?"); f.arrow([(360, 33), (410, 33)], color=TEAL, label="yes", lpos=(384, 24))
a(410, 104, "Read the manual:\nRAM, GPU, CPU fault"); f.arrow([(485, 56), (485, 104)], color=RED, label="yes", lpos=(500, 82))
a(610, 10, "BIOS reached: set boot\ndrive and install OS"); f.arrow([(560, 33), (610, 33)], color=TEAL, label="no beeps", lpos=(586, 24))
f.text(380, 200, "Change one thing at a time. Re-test after every change. Write down what you tried.", size=11, color=NAVY, bold=True)
f.text(380, 224, "Minimum test set: CPU + one RAM stick + PSU + speaker (no drives, no cards).", size=10.5, color=SLATE)
```

## 4.4 Lab sign-off table

| # | Task | Done | Instructor |
|---|---|---|---|
| 1 | Use of wrist strap and workspace set-up | | |
| 2 | Identify all components by name and function | | |
| 3 | Install CPU, RAM and cooler on the board | | |
| 4 | Mount board and PSU in case | | |
| 5 | Connect power, drives, front panel correctly | | |
| 6 | Cable management completed | | |
| 7 | Power-on and BIOS detection of CPU, RAM, storage | | |
| 8 | Measure PSU rails with a multimeter (+12 V, +5 V, +3.3 V) | | |

**PSU voltage check (multimeter).** With the 24-pin connector plugged into the board and the PC on, probe the back of the connector: orange wire ≈ +3.3 V, red ≈ +5 V, yellow ≈ +12 V, with black as ground; acceptable tolerance is ±5 % (for +12 V: 11.4 to 12.6 V). Green wire (PS_ON) shorted to black turns on a disconnected PSU (a paper-clip test, for a test only). Gray is **Power Good**, +5 V when the supply is stable; purple is **+5 VSB** standby.

## 4.5 Eight common assembly mistakes and how to avoid them

1. **Forgetting the I/O shield.** The metal back plate must be fitted in the case before the board is screwed in. Without it the ports do not line up and the board must be removed again. Make it step 1 on your checklist.
2. **Extra or missing standoffs.** A standoff under a place with no screw hole can touch the board and cause a short circuit. Fit standoffs only at the holes of your board's form factor. Count them before and after.
3. **Bent CPU pins or wrong CPU direction.** Forcing a CPU into the socket bends pins or damages contacts. Match the corner marker and lower it gently; it should drop in with no pressure. Never touch the pins or contacts.
4. **Too much or no thermal paste.** A pea-sized dot is enough; too much leaks onto the socket and no paste causes overheating. Remove the plastic film on a new cooler. Check that the cooler is tight and the fan cable is plugged into CPU_FAN.
5. **RAM not fully seated.** A half-fitted DIMM gives a black screen and beep codes. Press until both side clips click, and use the slots in the order the manual shows for dual channel. Wrong slots only lose speed, but a loose stick stops the PC.
6. **Missing power connectors.** The CPU needs the separate 4+4 or 8-pin cable besides the 24-pin cable, and a powerful GPU needs its own PCIe power cable. A PC with only the 24-pin connected often shows no sign of life. Trace every connector to the PSU.
7. **Front-panel wires on the wrong pins.** Swapped power and reset pins make the button restart the PC, and reversed LED wires just stay dark. Read the pin map in the manual and fit the plugs one pair at a time. LEDs can be turned around safely, switches have no polarity.
8. **Poor cable management and airflow.** Loose cables block fans and trap heat. Tie them behind the tray with cable ties and keep the front-to-back airflow free. A tidy case also makes later repairs far easier.

## 4.6 BIOS and UEFI

**BIOS** (Basic Input/Output System) is the legacy firmware on the motherboard; **UEFI** (Unified Extensible Firmware Interface) replaces it with a graphical interface, faster boot, support for disks above 2 TiB (GPT), network features and **Secure Boot**.

| | BIOS (legacy) | UEFI |
|---|---|---|
| Partition table | MBR | GPT (also reads MBR in CSM mode) |
| Max boot disk | 2 TiB | 9.4 ZB theoretically |
| Interface | text, keyboard | graphical, mouse |
| Boot speed | slower | faster |
| Security | none | Secure Boot, TPM support |

Enter setup with Del, F2, F10, F12 or Esc during the logo. **Settings to know:**

- **Boot order / boot menu**: choose USB or DVD for installation, then the system disk.
- **Date and time**: wrong time breaks certificates and logins.
- **SATA mode**: AHCI (normal), RAID, or IDE (legacy). *Changing AHCI/RAID after Windows is installed can stop it booting.*
- **Virtualisation (Intel VT-x / AMD-V)**: enable for virtual machines.
- **XMP / EXPO profile**: enables rated RAM speed.
- **Secure Boot and TPM**: needed by Windows 11.
- **Fan curves, CPU temperature**, **boot password / supervisor password**.
- **Clear CMOS** (jumper or removing the battery for a minute) resets forgotten settings or a bad overclock.
- **Update the firmware** (flash) only with a stable power supply; a failed update can brick the board.

**Boot sequence.** Power → firmware POST → finds the boot device → loads the **boot loader** (Windows Boot Manager, GRUB) from the EFI System Partition (UEFI) or the MBR (BIOS) → loads the OS kernel → services and login.

## 4.7 Disks, partitions and file systems

A disk is divided into **partitions**, each formatted with a **file system**. The **partition table** records where each starts and ends.

| Scheme | Limits |
|---|---|
| **MBR** (Master Boot Record) | max 2 TiB disk; 4 primary partitions (or 3 primary + 1 extended with logical drives) |
| **GPT** (GUID Partition Table) | disks above 2 TiB; up to 128 partitions in Windows; needs UEFI to boot |

The MBR limit comes from 32-bit sector addresses: 2³² × 512 bytes = 2,199,023,255,552 bytes = **2 TiB**. A 4 TB disk under MBR leaves about 2 TB unusable.

| File system | Used by | Notes |
|---|---|---|
| NTFS | Windows | permissions, compression, journaling, large files |
| FAT32 | USB sticks, EFI partition | max file 4 GiB, broad compatibility |
| exFAT | flash drives, SD cards | large files, no journaling |
| ext4 | Linux | journaling, standard on most distros |
| APFS / HFS+ | macOS | |

A typical **UEFI/GPT Windows layout**: EFI System Partition (100 to 500 MB, FAT32) + Microsoft Reserved (16 MB) + C: (NTFS) + Recovery partition. A typical **Ubuntu layout**: EFI partition + `/` (ext4, at least 25 GB) + optional `/home` + swap (about the size of RAM for hibernation, or a swap file).

**Partition planning example.** A "512 GB" SSD holds 512 × 10⁹ bytes = **476.8 GiB**, and partition tools show GiB. A dual-boot plan: EFI 0.5 + Windows C: 180 + Ubuntu `/` 80 + Ubuntu `/home` 120 + shared data 60 + swap 16 = **456.5 GiB**, which leaves about 20 GiB (4 %) unallocated as spare room and for SSD over-provisioning.

```photogrid label="4.3" cols="3" ratio="1.45" caption="What the install produces. (a) GParted showing a real disk: three partitions in an extended container, an ext4 root, a /home and a swap partition. (b) The finished Ubuntu desktop. (c) The finished Windows 10 desktop."
@ photo id="bca106/gparted" cap="GParted partition editor"
fit 1.45
call 0.50 0.12 0.50 0.62 "Partition, file system, size"
@ photo id="bca101/ubuntu" cap="Ubuntu Linux desktop"
fit 1.45
@ photo id="bca101/win10b" cap="Windows 10 desktop"
fit 1.45
```

```svgfig label="4.3" caption="The boot sequence. Firmware (BIOS or UEFI) tests the hardware, finds the boot device, and hands over to the boot loader, which loads the kernel; the kernel starts services and finally the login screen."
f = Fig(760, 150)
steps = [("Power on", "PSU gives Power-Good"), ("POST", "CPU, RAM, GPU test"), ("Firmware", "BIOS or UEFI, boot order"), ("Boot loader", "bootmgr or GRUB"), ("Kernel", "drivers, memory"), ("Login", "services, desktop")]
for i, (a, b) in enumerate(steps):
    x = 10 + i * 124
    f.box(x, 24, 106, 50, a, fill=BLUE if i in (2, 3) else SOFT, stroke=NAVY, size=11, bold=True)
    f.text(x + 53, 94, b, size=9, color=SLATE)
    if i < 5: f.arrow([(x + 106, 49), (x + 124, 49)], color=NAVY)
f.text(380, 130, "A fault before 'Firmware' is hardware (power, RAM); a fault after it is software (boot loader, disk, OS).", size=10.5, color=NAVY, bold=True)
```

```svgfig label="4.4" caption="Where the partition table lives. MBR keeps a 64-byte table in sector 0 (four entries). GPT keeps a protective MBR, a header and 128 entries at the start, and a backup copy at the end of the disk."
f = Fig(760, 210)
f.text(14, 16, "MBR disk (BIOS)", size=11, color=TEAL, bold=True, anchor="start")
for i, (a, w, c) in enumerate([("MBR\n512 B", 80, AMBER), ("Partition 1 (C:)", 250, BLUE), ("Partition 2 (D:)", 200, BLUE), ("Extended: logical drives", 190, SOFT)]):
    x = 14 + sum([80, 250, 200, 190][:i])
    f.box(x, 26, w, 44, a, fill=c if c != AMBER else "#fef3c7", stroke=NAVY, size=10.5, bold=True)
f.text(14, 110, "GPT disk (UEFI)", size=11, color=TEAL, bold=True, anchor="start")
for i, (a, w, c) in enumerate([("Prot.\nMBR", 60, SOFT), ("GPT\nheader", 60, "#fef3c7"), ("EFI\n(FAT32)", 90, SOFT), ("Windows C: (NTFS)", 250, BLUE), ("Linux / (ext4)", 190, BLUE), ("Backup\nGPT", 70, "#fef3c7")]):
    x = 14 + sum([60, 60, 90, 250, 190, 70][:i])
    f.box(x, 120, w, 44, a, fill=c, stroke=NAVY, size=10, bold=True)
f.text(380, 192, "MBR: 2 TiB limit, 4 primary partitions.   GPT: more than 2 TiB, 128 partitions, CRC-protected, backup copy.", size=10.5, color=SLATE)
```

## 4.8 Installing Windows

1. **Prepare**: download the official ISO from Microsoft; create a bootable USB (Media Creation Tool or Rufus, USB at least 8 GB); back up the data; note the licence key (or use a digital licence linked to your account); check the minimum requirements.
2. **Boot from USB**: press the boot-menu key, choose the **UEFI: USB** entry.
3. **Language, edition and licence**; choose *Custom: Install Windows only*.
4. **Partitioning**: select the unallocated space and click *New* (Windows creates the system partitions), or delete old partitions to start fresh. **Deleting a partition erases its data.**
5. **Copy and restart**; remove the USB when it reboots the first time.
6. **First-run set-up**: region, keyboard, network, account (local or Microsoft), privacy options.
7. **Post-install:** install **drivers** (chipset, graphics, LAN, Wi-Fi, audio) from the manufacturer's site, run Windows Update, install an antivirus or enable Defender, install applications, create a **restore point** and a **system image**, and **activate** Windows.

## 4.9 Installing Ubuntu Linux (and dual boot)

1. **Prepare** a live USB with the official ISO (Rufus or `dd`); **disable fast start-up and hibernation** in Windows if dual-booting; shrink the Windows partition in *Disk Management* to free space; back up.
2. **Boot the USB** and choose *Try Ubuntu* (test hardware: Wi-Fi, display, touchpad) or *Install Ubuntu*.
3. **Installation type:** *Erase disk* for a single-OS machine; *Install alongside Windows* for dual boot; or *Something else* for manual partitions (EFI, `/`, `/home`, swap).
4. **Region, keyboard, user name and password**; the installer copies files and installs **GRUB** which offers a choice of Ubuntu or Windows at each start.
5. **Reboot**, remove the USB, log in, and run `sudo apt update && sudo apt upgrade`. Install extra drivers from *Additional Drivers* if needed.

Useful commands after installation: `lsblk` (disks), `df -h` (space used), `free -h` (memory), `lscpu`, `sudo fdisk -l`, `ip a` (network), `ubuntu-drivers devices`. A **live USB** is also the best repair tool: boot it to copy files off a PC that no longer starts.

**Virtual machines** let you practise safely: VirtualBox or VMware (enable virtualisation in the BIOS), allocate 2 CPUs, 4 GB RAM, 25 GB disk, attach the ISO and install exactly as above, with no risk to the host.

## 4.10 Drivers, updates, imaging and recovery

- **Driver**: software that lets the OS use a device. Download from the manufacturer, not from random sites. Check *Device Manager* (Windows) for yellow warning icons.
- **Updates**: apply OS and firmware updates for security; keep a restore point before major updates.
- **Backup methods:** **file backup** (copy files), **system image** (a full copy of the OS and apps, restorable to a new disk), **cloning** (disk-to-disk, for upgrading to an SSD). Follow the **3-2-1 rule**: three copies, on two media types, one off-site.
- **Recovery:** *Safe Mode* (minimal drivers), *System Restore*, *Startup Repair*, *Reset this PC*, boot-loader repair (`bootrec /fixmbr`, `/fixboot`, `/rebuildbcd` from the recovery command prompt; for GRUB, `boot-repair` or `grub-install`), and **password reset** only for your own device and with authority.
- **Data recovery:** if a file is deleted by mistake, **stop using the disk**, because new writes overwrite the deleted data, and recover with tools such as Recuva or `testdisk`/`photorec` from another disk or live USB.

## 4.11 POST, beep codes and diagnostic tools

**POST** (power-on self-test) is the first stage of the firmware: it tests the CPU, RAM and video, then looks for a boot device. The result is reported as screen text, **beep codes**, a two-digit **POST code** on the board's debug display, or LEDs marked CPU, DRAM, VGA and BOOT.

| Signal (classic Award / AMI BIOS) | Usual meaning | First action |
|---|---|---|
| One short beep | Award: POST passed | none, boot continues |
| One long, two short | Award: video card or display fault | reseat the GPU, check the monitor cable |
| Continuous or repeating long beeps | Memory not detected or faulty | reseat RAM, try one stick in slot A2 |
| Repeating short beeps | Power supply or board power problem | test the PSU rails |
| AMI: 3 short | Memory fault | reseat or replace RAM |
| AMI: 5 short | CPU fault | reseat CPU, check cooler and EPS power |
| AMI: 8 short | Display memory fault | reseat or replace the GPU |

Codes differ between BIOS makers and boards, so **always confirm with the motherboard manual**; modern UEFI boards usually use LEDs or a code display instead of a speaker.

**Diagnostic tools.** A **POST card** (a PCI/PCIe or USB card that shows the POST code) is used when the screen is blank; a multimeter checks PSU rails and continuity; a PSU tester checks all connectors; a **BIOS reset jumper** or removing the CMOS battery for 30 seconds restores defaults after a bad setting; the **minimum configuration test** (CPU, one RAM stick, PSU, speaker) isolates the faulty part (Figure 4.2).

**Simulating hardware faults.** In the lab the instructor loosens a RAM stick (continuous beeps), unplugs the GPU power or the EPS connector (no display, no boot), removes the boot drive (no operating system found) or sets a wrong boot order. You identify the symptom, apply the elimination method and record it in a log.

## 4.12 Drivers, updates, printer installation and basic maintenance after installing the OS

After Windows or Linux is installed: (1) update the BIOS/UEFI only if the board needs it (Unit 8); (2) install chipset, graphics, audio and LAN **drivers** from the vendor site and check Device Manager for yellow warnings; (3) run Windows Update or `sudo apt update && sudo apt upgrade`; (4) install an antivirus scan (Microsoft Defender is built in) and run a full scan; (5) run **Disk Cleanup** or Storage Sense to remove temporary files; (6) create a restore point or a system image.

**Installing a printer.** *Real printer:* connect the USB or network cable and power on; open Settings, Printers and scanners, Add device (Windows) or Printers in Settings (Ubuntu with CUPS); install the vendor driver if the generic one is not enough; print a **test page**. *Virtual printer:* a software printer such as **Microsoft Print to PDF** is already present on Windows; for Linux install `cups-pdf`. Printing to it produces a PDF file, so you can practise installation and queue handling with no hardware.

## 4.13 Smart and useful operating-system commands

| Task | Windows (Command Prompt or PowerShell) | Linux (Ubuntu bash) |
|---|---|---|
| Show current folder / list files | `cd`, `dir` | `pwd`, `ls -l` |
| System information | `systeminfo`, `msinfo32` | `lscpu`, `free -h`, `uname -a` |
| Disks and free space | `diskpart` then `list disk`, `wmic logicaldisk` (old) | `lsblk`, `df -h` |
| Check and repair files / disk | `sfc /scannow`, `chkdsk C: /f` | `sudo fsck /dev/sda1` (unmounted) |
| Running processes, stop one | `tasklist`, `taskkill /PID 1234 /F` | `top`, `ps aux`, `kill 1234` |
| Hardware lists | `driverquery`, Device Manager | `lspci`, `lsusb`, `dmesg` |
| Network | `ipconfig /all`, `ping`, `tracert` | `ip addr`, `ping`, `traceroute` |
| Shut down or restart | `shutdown /s /t 0`, `shutdown /r` | `sudo shutdown now`, `sudo reboot` |
| Install software | `winget install <name>` | `sudo apt install <name>` |

**Cross-platform commands** work the same on every system: `ping host`, `nslookup name` (DNS), `hostname`, and `git`, `python --version`, `curl` when installed. Run an elevated Command Prompt (Run as administrator) or `sudo` for commands that change the system, and never run a command you do not understand.

::: example Worked example: a "slow PC" check with commands
(1) `tasklist` or `top` shows one process using 98 % CPU; (2) `sfc /scannow` repairs a corrupted system file; (3) `chkdsk C: /f` finds bad sectors on an old HDD; (4) `lsblk` or Disk Management shows the drive is 96 % full. Solution: end or uninstall the runaway program, repair, free space, or replace the HDD with an SSD (Unit 8).
:::

## 4.14 Eight tips for a safe operating-system installation

1. **Back up first.** Copy documents, photos and browser bookmarks to an external drive or cloud before touching the disk. Formatting a partition cannot be undone. A written list of installed programmes and licence keys also saves time later.
2. **Check the requirements.** Windows 11 needs 4 GB RAM, 64 GB storage, UEFI with Secure Boot and TPM 2.0; Ubuntu runs well on 4 GB RAM and 25 GB. Machines that fail the check can use Windows 10 or a light Linux. Reading the requirements takes two minutes and avoids a failed install.
3. **Prepare a trusted installer.** Download the ISO only from the official site and check its SHA-256 checksum. Write it to a USB with a tool such as Rufus, Ventoy or balenaEtcher. Pirated images often carry malware.
4. **Set the firmware correctly.** Enter BIOS/UEFI with the right key (Del, F2, F10 or F12), and choose the USB in the boot menu. Keep the mode (UEFI or Legacy) the same as the disk partition style. A mismatch is the commonest reason for "no boot device".
5. **Plan the partitions.** Give the OS 60 to 100 GB, keep data on a separate partition or drive and add an EFI partition on UEFI systems. For dual boot, shrink the Windows partition from inside Windows. Never resize while the disk has errors.
6. **Install Windows before Linux.** Windows overwrites the boot loader; Ubuntu's GRUB can find Windows and add it to the menu. If the order is reversed, repair GRUB afterwards. Turn off Fast Startup in Windows for safe dual boot.
7. **Install drivers and updates.** After the first boot install chipset, graphics, network and printer drivers, then run all updates. A computer with no network can still use a driver pack on a USB. Updates close security holes found since the ISO was built.
8. **Create a restore point or image.** When the system is clean and working, save an image with a tool such as Clonezilla or Windows backup. A failed update or virus can then be undone in minutes instead of a full reinstall. Keep the image on a different disk.

## Formula and fact sheet

- Order: CPU → RAM → M.2 → cooler (outside) → board into case → PSU → cables → drives → front panel → cards → test.
- Thermal paste: pea-sized dot. Cooler screws: diagonal pattern.
- Power: 24-pin ATX, 8-pin EPS CPU, PCIe for GPU, SATA power for drives.
- Voltage colours: orange +3.3 V, red +5 V, yellow +12 V, black ground; tolerance ±5 %.
- Troubleshoot: minimum configuration, then add one part at a time.
- MBR: 2 TiB, 4 primary partitions. GPT: >2 TiB, 128 partitions, needs UEFI to boot.
- FAT32 max file 4 GiB; NTFS and ext4 for system disks; exFAT for portable drives.
- Windows 11 needs UEFI, Secure Boot, TPM 2.0.
- Install steps: ISO → bootable USB → boot menu → partition → copy → set-up → drivers → updates → backup.
- AHCI is the normal SATA mode; do not switch it after installation.
- 3-2-1 backup rule.

## Chapter summary

- Build in a fixed order, handling the CPU and RAM carefully and tightening screws evenly.
- Front-panel headers need the manual; LEDs have polarity, switches do not.
- Check twice before power-on: no loose screws, all power connected, monitor on the right port.
- If it fails, use beep codes, debug LEDs and a minimum-configuration test to isolate the part.
- UEFI replaces BIOS and brings GPT, Secure Boot and speed; the settings to master are boot order, SATA mode, virtualisation and Secure Boot.
- Partition tables and file systems have hard limits that explain real-world behaviour (2 TiB MBR, 4 GiB FAT32).
- A clean install follows a fixed routine, and the work is not finished until drivers, updates and a backup are done.
- Virtual machines and live USBs are the safest places to practise and repair.

## Practice

### Part A: assembly

1. Write the steps for installing a CPU and cooler and explain why thermal paste is needed.
2. Why must you tighten cooler screws diagonally?
3. A newly built PC shows no display although the fans spin. List five checks in order.
4. What is dual channel and where do you place two RAM sticks?
5. How do you identify the correct way to insert RAM, an Intel CPU and a SATA cable?
6. Explain the purpose of the CPU_FAN header and the risk of not connecting it.
7. List the connectors that come from the PSU and what each powers.
8. What voltage should you read on the yellow wire of a healthy PSU? What is the acceptable range?
9. Explain POST and how beep codes help.
10. Explain why you should build with the minimum configuration first when the PC will not start.

::: note Answers and worked solutions
**1.** Open the socket lever, align the notches (Intel) or triangle (AMD), place the CPU without pressure, lock the lever; add a pea-sized paste dot, seat the cooler, tighten diagonally, connect CPU_FAN. Paste fills microscopic air gaps between the CPU lid and cooler base, which would otherwise block heat transfer.
**2.** Even pressure prevents tilting that would crack the CPU or leave an air gap.
**3.** Monitor cable in the correct port (GPU vs board); monitor input source; reseat RAM; GPU seated and powered; CPU 8-pin power connected; try one RAM stick; clear CMOS.
**4.** Dual channel uses two modules on two memory channels for double bandwidth; place them in the slots recommended in the manual (often A2 and B2).
**5.** RAM has an off-centre notch matching the slot key; an Intel CPU has two notches matching the socket; a SATA connector is L-shaped and fits only one way.
**6.** It powers and monitors the CPU fan; without it the CPU overheats and the system may shut down or throttle.
**7.** 24-pin ATX: board; 4+4 EPS: CPU; PCIe 6+2: graphics card; SATA power: drives; Molex: older peripherals and fans.
**8.** +12 V, with a range of 11.4 to 12.6 V (±5 %).
**9.** POST is the firmware's hardware self-test at start-up; a failure produces beep patterns or debug codes that identify the faulty subsystem.
**10.** It removes variables: if the minimal system boots, add parts one at a time until the fault returns; the last part added is the culprit.
:::

### Part B: BIOS, partitions and operating-system installation

1. Differentiate BIOS and UEFI in five points.
2. Why can't MBR use more than 2 TiB? Show the calculation.
3. Plan the partitions for a 256 GB SSD to run Windows and Ubuntu.
4. Write the steps to install Windows from a USB stick on a new PC.
5. What problems can arise after changing the SATA mode from IDE to AHCI?
6. How would you recover files from a PC that no longer boots?
7. Why disable fast start-up before dual-booting? 
8. Describe the difference between a file backup, a system image and a clone.
9. A new 4 TB disk shows only 2 TB in Windows. Why and how to fix?
10. List five post-installation tasks.

::: note Answers and worked solutions
**1.** BIOS: MBR, 2 TiB, text interface, no Secure Boot, slower. UEFI: GPT, large disks, graphical, Secure Boot and TPM support, faster boot.
**2.** MBR uses 32-bit sector numbers: 2³² = 4,294,967,296 sectors × 512 B = 2,199,023,255,552 B = 2 TiB.
**3.** A 256 GB drive is about 238 GiB: EFI 0.5 GB, Windows 100 GB, Ubuntu `/` 50 GB, swap 8 GB, shared data 60 GB; total 218.5 GB leaves headroom for over-provisioning.
**4.** The seven steps of §4.8.
**5.** Windows may fail to boot (blue screen, INACCESSIBLE_BOOT_DEVICE) because the storage driver is not loaded for the new mode. Fix by enabling the driver first (safe mode switch) or revert the setting.
**6.** Boot a live USB (Ubuntu), mount the internal disk, copy the files to an external drive; or remove the drive and read it in another computer.
**7.** Fast start-up leaves the NTFS partition in a hibernated state; Linux may mount it read-only or corrupt it, and partition changes can destroy the Windows hibernation file.
**8.** File backup copies chosen files; a system image captures the whole OS, settings and apps for complete restore; a clone is an exact copy of a disk onto another disk, immediately bootable.
**9.** The disk was initialised as MBR. Back up, convert to GPT in Disk Management or `diskpart` (`convert gpt`), and create partitions for the full capacity.
**10.** Install chipset/graphics/LAN drivers, run Windows Update, install antivirus, install applications, create a restore point and system image, activate Windows.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Explain how the CPU, cooler and RAM are installed on a motherboard.**

These three parts are fitted to the board while it lies on its box outside the case, because there is more room (Plate 4.1).

*CPU.* Lift the socket lever (Intel LGA) or the retention arm (AMD AM4). Find the small triangle on one corner of the CPU and match it with the triangle on the socket. Lower the CPU without pressure so that it sits flat, then close the plate and lever. Never touch the contacts, and never force it: a bent pin often cannot be repaired.

*Cooler.* Clean the CPU top, then place a pea-sized drop of thermal paste in the centre (a new cooler may already have paste, see Plate 4.1d). Lower the cooler straight down, tighten the four screws or clips in a cross pattern and push the fan cable onto the CPU_FAN header.

*RAM.* Open the clips at both ends of the slot, match the notch of the DIMM to the key in the slot and press both ends down evenly until the clips snap shut. For dual channel use slots 2 and 4 (check the manual) when fitting two sticks.

| Part | Alignment aid | Final check |
|---|---|---|
| CPU | corner triangle | sits flat, lever closes easily |
| Cooler | four holes | tight; fan cable in CPU_FAN |
| RAM | single notch | both clips locked |

**Q (10 marks). Describe the step-by-step procedure for assembling a desktop PC and explain how a first test (POST) is carried out. List four faults that can stop a new PC from starting.**

*Introduction.* Assembly is a controlled sequence: build the core on the board, fix the board in the case, connect power and storage, then test before closing the case (Figure 4.1). Follow the manual of each part and an anti-static routine throughout.

*Procedure.*

1. **Prepare:** clear the bench, wear the wrist strap, check all parts and screws against the list, and read the board manual.
2. **Case:** remove both panels, fit the I/O shield and screw the standoffs that match the board.
3. **CPU, cooler and RAM:** install them on the board as described above.
4. **M.2 SSD:** fit it in its slot and fix it with the small screw.
5. **Board into case:** lower it onto the standoffs and tighten all screws gently, without forcing.
6. **PSU and drives:** fix the PSU, fit the 2.5 inch or 3.5 inch drives, and connect the SATA data and power cables.
7. **Power cables:** plug in the 24-pin main and 4+4 pin CPU cables, then fit the graphics card and its PCIe power.
8. **Front panel:** connect the power switch, reset switch, LED and USB/audio cables using the pin map (Plate 4.2).
9. **Test (POST):** connect monitor, keyboard and mains, and press power. Fans spin and the board runs the **Power-On Self-Test**, which checks the CPU, RAM and graphics. One short beep or a logo means success; other beeps or a debug code point to a fault.
10. **Close up:** switch off, tidy the cables, close the panels and start the OS installation.

*Faults that stop a new PC.* (1) No power: mains, PSU switch or 24-pin not seated. (2) Fans spin but no display: RAM not seated or cable in the wrong output. (3) Repeated beeps: RAM or graphics fault. (4) Power then shutdown: cooler not fitted properly, or a short circuit from a stray standoff.

| POST result | Meaning | Action |
|---|---|---|
| Nothing at all | no power | check PSU, 24-pin, PWR pins |
| 1 short beep | pass (most boards) | enter BIOS, install OS |
| Continuous beeps | RAM or power fault | reseat RAM |
| Long + short beeps | graphics fault | reseat card, check cable |

*Conclusion.* Methodical assembly with a test of the minimum system first finds a fault in minutes rather than hours. A written checklist, signed at each step, is the mark of a professional technician.

**Q (5 marks). Differentiate MBR and GPT. Why can a 4 TB disk not be fully used under MBR?**

A **partition table** records where each partition starts and how long it is. **MBR** (Master Boot Record) stores a 64-byte table in the first sector of the disk with room for only four entries, each using 32-bit sector numbers. **GPT** (GUID Partition Table) stores a header and up to 128 entries, with a backup copy at the end of the disk and a CRC checksum, and uses 64-bit sector numbers (Figure 4.4).

| Point | MBR | GPT |
|---|---|---|
| Firmware | BIOS (legacy) | UEFI (BIOS possible on some) |
| Maximum disk | 2 TiB | about 9.4 ZB |
| Partitions | 4 primary (or 3 + extended) | 128 in Windows |
| Table copy | one | primary and backup |
| Protection | none | CRC checks |

*Calculation.* The largest address is 2³² sectors × 512 bytes = 2,199,023,255,552 bytes = 2 TiB. A "4 TB" disk has 4 × 10¹² bytes, so about 1.8 TB (more than 40 %) would be unusable under MBR. Such a disk must be initialised as GPT.

**Q (10 marks). Explain the roles of BIOS and UEFI, and describe the steps to install Windows and Ubuntu as a dual-boot system on one PC.**

*Introduction.* Firmware is the first program that runs when a computer is switched on. It tests the hardware (POST), finds a boot device and hands control to the boot loader (Figure 4.3). Older PCs use **BIOS**; modern PCs use **UEFI**.

*BIOS and UEFI compared.*

| Point | BIOS | UEFI |
|---|---|---|
| Mode | 16-bit, text menus | 32/64-bit, graphical with mouse |
| Boot disk | MBR, up to 2 TiB | GPT and large disks |
| Boot speed | slower | faster |
| Security | none | Secure Boot |
| Boot files | first sector | `.efi` files in the EFI partition |

*Preparation.* Back up data, download both ISO files, make a bootable USB with Rufus or Ventoy, and check that the firmware is in UEFI mode. Turn off Fast Startup in Windows.

*Installation steps.*

1. Boot from the Windows USB through the boot menu (F12 or similar).
2. Choose custom install; create the EFI and C: partitions (for example 100 GB for Windows), and **leave about 100 GB unallocated** for Linux. Complete the installation and install drivers.
3. Boot Windows once and check updates and drivers.
4. Boot the Ubuntu USB; choose "Install Ubuntu" and "Install alongside Windows Boot Manager".
5. Create the partitions in the free space: `/` (ext4, 40 GB), swap (4 GB or equal to RAM for hibernation) and optionally `/home`; the EFI partition is shared.
6. Set the user name and password and install; GRUB is placed in the EFI partition.
7. Restart: GRUB shows a menu with *Ubuntu* and *Windows Boot Manager*; test both.

| Problem | Cause | Fix |
|---|---|---|
| No Windows entry in GRUB | install order or fast startup | run `sudo update-grub` |
| Boots straight to Windows | boot order in UEFI | put Ubuntu/GRUB first |
| "No boot device" | UEFI/Legacy mismatch | match mode and partition style |

*Conclusion.* Understanding firmware, partition tables and boot loaders turns installation from a menu-clicking exercise into a controlled procedure. The key habits are to back up first, install Windows before Linux, and keep the firmware mode consistent with the disk style.

**Q (5 marks). What is POST? Explain the common beep codes.**

POST is the power-on self-test run by the BIOS/UEFI to check the CPU, RAM, video and drives before loading the operating system. Faults are reported as beeps, screen text or a two-digit code. For Award BIOS one short beep means success, one long and two short beeps mean a video fault, and continuous beeps mean a memory fault; AMI uses counts of short beeps (three for memory, five for CPU, eight for display memory). The manual of the board is the final authority, and a POST card shows the code when the screen is blank.

**Q (10 marks). Describe the steps after assembling a PC: BIOS configuration, operating-system installation, driver updates and useful commands.**

*Introduction.* A built PC is only useful after firmware, operating system and drivers are configured.

*BIOS/UEFI.* Enter with Del or F2, check that CPU, RAM and drives are detected, set the boot order, enable XMP/EXPO if desired, set an administrator password and save.

*Operating-system installation.* Create bootable USB media, boot from it, partition the disk (GPT for UEFI), install, create an account.

*Drivers and updates.* Install chipset, graphics, audio and LAN drivers, run Windows Update or `apt upgrade`, and run an antivirus scan and disk cleanup.

*Commands.* `systeminfo`, `ipconfig`, `sfc /scannow`, `chkdsk` on Windows; `lscpu`, `lsblk`, `df -h`, `ip addr` on Linux; `ping` on both. Finish with a printer test page and a sign-off table.
