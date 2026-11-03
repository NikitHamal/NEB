---
subject: Hardware Workshop
grade: BCA Semester 1
unit: 3
title: BIOS/UEFI, Disk Partitioning and Operating System Installation
area: BCA 106 · Hardware Workshop · Unit 3
---

A built PC is still an empty machine. This unit covers the firmware that starts it, the structure of disks and partitions, and a complete installation of Windows and of Linux, including dual boot and recovery. It ends with drivers, updates and backup.

::: key What this unit gives you
- BIOS versus UEFI; the settings you must know; the boot sequence.
- Partition tables (MBR, GPT), file systems, and calculations of limits.
- Step-by-step Windows 11/10 and Ubuntu installation; dual boot.
- Drivers, updates, imaging and recovery.
:::

## 3.1 BIOS and UEFI

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

## 3.2 Disks, partitions and file systems

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

```photogrid label="3.1" cols="3" ratio="1.45" caption="What the install produces. (a) GParted showing a real disk: three partitions in an extended container, an ext4 root, a /home and a swap partition. (b) The finished Ubuntu desktop. (c) The finished Windows 10 desktop."
@ photo id="bca106/gparted" cap="GParted partition editor"
fit 1.45
call 0.50 0.12 0.50 0.62 "Partition, file system, size"
@ photo id="bca101/ubuntu" cap="Ubuntu Linux desktop"
fit 1.45
@ photo id="bca101/win10b" cap="Windows 10 desktop"
fit 1.45
```

```svgfig label="3.1" caption="The boot sequence. Firmware (BIOS or UEFI) tests the hardware, finds the boot device, and hands over to the boot loader, which loads the kernel; the kernel starts services and finally the login screen."
f = Fig(760, 150)
steps = [("Power on", "PSU gives Power-Good"), ("POST", "CPU, RAM, GPU test"), ("Firmware", "BIOS or UEFI, boot order"), ("Boot loader", "bootmgr or GRUB"), ("Kernel", "drivers, memory"), ("Login", "services, desktop")]
for i, (a, b) in enumerate(steps):
    x = 10 + i * 124
    f.box(x, 24, 106, 50, a, fill=BLUE if i in (2, 3) else SOFT, stroke=NAVY, size=11, bold=True)
    f.text(x + 53, 94, b, size=9, color=SLATE)
    if i < 5: f.arrow([(x + 106, 49), (x + 124, 49)], color=NAVY)
f.text(380, 130, "A fault before 'Firmware' is hardware (power, RAM); a fault after it is software (boot loader, disk, OS).", size=10.5, color=NAVY, bold=True)
```

```svgfig label="3.2" caption="Where the partition table lives. MBR keeps a 64-byte table in sector 0 (four entries). GPT keeps a protective MBR, a header and 128 entries at the start, and a backup copy at the end of the disk."
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

## 3.3 Installing Windows

1. **Prepare**: download the official ISO from Microsoft; create a bootable USB (Media Creation Tool or Rufus, USB at least 8 GB); back up the data; note the licence key (or use a digital licence linked to your account); check the minimum requirements.
2. **Boot from USB**: press the boot-menu key, choose the **UEFI: USB** entry.
3. **Language, edition and licence**; choose *Custom: Install Windows only*.
4. **Partitioning**: select the unallocated space and click *New* (Windows creates the system partitions), or delete old partitions to start fresh. **Deleting a partition erases its data.**
5. **Copy and restart**; remove the USB when it reboots the first time.
6. **First-run set-up**: region, keyboard, network, account (local or Microsoft), privacy options.
7. **Post-install:** install **drivers** (chipset, graphics, LAN, Wi-Fi, audio) from the manufacturer's site, run Windows Update, install an antivirus or enable Defender, install applications, create a **restore point** and a **system image**, and **activate** Windows.

## 3.4 Installing Ubuntu Linux (and dual boot)

1. **Prepare** a live USB with the official ISO (Rufus or `dd`); **disable fast start-up and hibernation** in Windows if dual-booting; shrink the Windows partition in *Disk Management* to free space; back up.
2. **Boot the USB** and choose *Try Ubuntu* (test hardware: Wi-Fi, display, touchpad) or *Install Ubuntu*.
3. **Installation type:** *Erase disk* for a single-OS machine; *Install alongside Windows* for dual boot; or *Something else* for manual partitions (EFI, `/`, `/home`, swap).
4. **Region, keyboard, user name and password**; the installer copies files and installs **GRUB** which offers a choice of Ubuntu or Windows at each start.
5. **Reboot**, remove the USB, log in, and run `sudo apt update && sudo apt upgrade`. Install extra drivers from *Additional Drivers* if needed.

Useful commands after installation: `lsblk` (disks), `df -h` (space used), `free -h` (memory), `lscpu`, `sudo fdisk -l`, `ip a` (network), `ubuntu-drivers devices`. A **live USB** is also the best repair tool: boot it to copy files off a PC that no longer starts.

**Virtual machines** let you practise safely: VirtualBox or VMware (enable virtualisation in the BIOS), allocate 2 CPUs, 4 GB RAM, 25 GB disk, attach the ISO and install exactly as above, with no risk to the host.

## 3.5 Drivers, updates, imaging and recovery

- **Driver**: software that lets the OS use a device. Download from the manufacturer, not from random sites. Check *Device Manager* (Windows) for yellow warning icons.
- **Updates**: apply OS and firmware updates for security; keep a restore point before major updates.
- **Backup methods:** **file backup** (copy files), **system image** (a full copy of the OS and apps, restorable to a new disk), **cloning** (disk-to-disk, for upgrading to an SSD). Follow the **3-2-1 rule**: three copies, on two media types, one off-site.
- **Recovery:** *Safe Mode* (minimal drivers), *System Restore*, *Startup Repair*, *Reset this PC*, boot-loader repair (`bootrec /fixmbr`, `/fixboot`, `/rebuildbcd` from the recovery command prompt; for GRUB, `boot-repair` or `grub-install`), and **password reset** only for your own device and with authority.
- **Data recovery:** if a file is deleted by mistake, **stop using the disk**, because new writes overwrite the deleted data, and recover with tools such as Recuva or `testdisk`/`photorec` from another disk or live USB.

## 3.6 Eight tips for a safe operating-system installation

1. **Back up first.** Copy documents, photos and browser bookmarks to an external drive or cloud before touching the disk. Formatting a partition cannot be undone. A written list of installed programmes and licence keys also saves time later.
2. **Check the requirements.** Windows 11 needs 4 GB RAM, 64 GB storage, UEFI with Secure Boot and TPM 2.0; Ubuntu runs well on 4 GB RAM and 25 GB. Machines that fail the check can use Windows 10 or a light Linux. Reading the requirements takes two minutes and avoids a failed install.
3. **Prepare a trusted installer.** Download the ISO only from the official site and check its SHA-256 checksum. Write it to a USB with a tool such as Rufus, Ventoy or balenaEtcher. Pirated images often carry malware.
4. **Set the firmware correctly.** Enter BIOS/UEFI with the right key (Del, F2, F10 or F12), and choose the USB in the boot menu. Keep the mode (UEFI or Legacy) the same as the disk partition style. A mismatch is the commonest reason for "no boot device".
5. **Plan the partitions.** Give the OS 60 to 100 GB, keep data on a separate partition or drive and add an EFI partition on UEFI systems. For dual boot, shrink the Windows partition from inside Windows. Never resize while the disk has errors.
6. **Install Windows before Linux.** Windows overwrites the boot loader; Ubuntu's GRUB can find Windows and add it to the menu. If the order is reversed, repair GRUB afterwards. Turn off Fast Startup in Windows for safe dual boot.
7. **Install drivers and updates.** After the first boot install chipset, graphics, network and printer drivers, then run all updates. A computer with no network can still use a driver pack on a USB. Updates close security holes found since the ISO was built.
8. **Create a restore point or image.** When the system is clean and working, save an image with a tool such as Clonezilla or Windows backup. A failed update or virus can then be undone in minutes instead of a full reinstall. Keep the image on a different disk.

## Formula and fact sheet

- MBR: 2 TiB, 4 primary partitions. GPT: >2 TiB, 128 partitions, needs UEFI to boot.
- FAT32 max file 4 GiB; NTFS and ext4 for system disks; exFAT for portable drives.
- Windows 11 needs UEFI, Secure Boot, TPM 2.0.
- Install steps: ISO → bootable USB → boot menu → partition → copy → set-up → drivers → updates → backup.
- AHCI is the normal SATA mode; do not switch it after installation.
- 3-2-1 backup rule.

## Chapter summary

- UEFI replaces BIOS and brings GPT, Secure Boot and speed; the settings to master are boot order, SATA mode, virtualisation and Secure Boot.
- Partition tables and file systems have hard limits that explain real-world behaviour (2 TiB MBR, 4 GiB FAT32).
- A clean install follows a fixed routine, and the work is not finished until drivers, updates and a backup are done.
- Virtual machines and live USBs are the safest places to practise and repair.

## Practice

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
**4.** The seven steps of §3.3.
**5.** Windows may fail to boot (blue screen, INACCESSIBLE_BOOT_DEVICE) because the storage driver is not loaded for the new mode. Fix by enabling the driver first (safe mode switch) or revert the setting.
**6.** Boot a live USB (Ubuntu), mount the internal disk, copy the files to an external drive; or remove the drive and read it in another computer.
**7.** Fast start-up leaves the NTFS partition in a hibernated state; Linux may mount it read-only or corrupt it, and partition changes can destroy the Windows hibernation file.
**8.** File backup copies chosen files; a system image captures the whole OS, settings and apps for complete restore; a clone is an exact copy of a disk onto another disk, immediately bootable.
**9.** The disk was initialised as MBR. Back up, convert to GPT in Disk Management or `diskpart` (`convert gpt`), and create partitions for the full capacity.
**10.** Install chipset/graphics/LAN drivers, run Windows Update, install antivirus, install applications, create a restore point and system image, activate Windows.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Differentiate MBR and GPT. Why can a 4 TB disk not be fully used under MBR?**

A **partition table** records where each partition starts and how long it is. **MBR** (Master Boot Record) stores a 64-byte table in the first sector of the disk with room for only four entries, each using 32-bit sector numbers. **GPT** (GUID Partition Table) stores a header and up to 128 entries, with a backup copy at the end of the disk and a CRC checksum, and uses 64-bit sector numbers (Figure 3.2).

| Point | MBR | GPT |
|---|---|---|
| Firmware | BIOS (legacy) | UEFI (BIOS possible on some) |
| Maximum disk | 2 TiB | about 9.4 ZB |
| Partitions | 4 primary (or 3 + extended) | 128 in Windows |
| Table copy | one | primary and backup |
| Protection | none | CRC checks |

*Calculation.* The largest address is 2³² sectors × 512 bytes = 2,199,023,255,552 bytes = 2 TiB. A "4 TB" disk has 4 × 10¹² bytes, so about 1.8 TB (more than 40 %) would be unusable under MBR. Such a disk must be initialised as GPT.

**Q (10 marks). Explain the roles of BIOS and UEFI, and describe the steps to install Windows and Ubuntu as a dual-boot system on one PC.**

*Introduction.* Firmware is the first program that runs when a computer is switched on. It tests the hardware (POST), finds a boot device and hands control to the boot loader (Figure 3.1). Older PCs use **BIOS**; modern PCs use **UEFI**.

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
