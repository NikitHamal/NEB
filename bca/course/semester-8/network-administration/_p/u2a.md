---
subject: Network Administration
grade: BCA Semester 8 (Elective III)
unit: 2
title: Workstation, Server and Services
hours: 16
area: BCA 453 · Network Administration · Unit 2
---

An organisation does not run on cables; it runs on **services**: mail, files, printing, logins, the web. A service is delivered by **servers**, and used by people through **workstations**. This unit follows that chain: how to design and install the workstations people use, how to choose and run the servers behind them, and how to plan, launch and protect a service as a whole.

::: key What this unit gives you
- Workstation architecture (thick, thin, virtual desktop), hardware strategy and the life cycle of a PC fleet, and OS installation by hand, by cloned image and by network (PXE, kickstart, autoinstall, WDS).
- Server hardware strategy, features and specifications: CPU, ECC memory, storage, RAID, redundant power, remote management, racks, power and cooling.
- Services: requirements, planning and engineering (redundancy, capacity, availability arithmetic), service launch, and disaster recovery with RTO and RPO.
:::

## 2.1 Workstations

### 2.1.1 What a workstation fleet needs

A **workstation** is the computer a person uses directly: a desktop in a lab, a laptop, a front-desk PC. One workstation is easy; **a hundred of them is a fleet**, and a fleet is manageable only if the machines are nearly identical and every one is installed, configured and updated by the **same automatic process**. The prescribed text states the principle in three words: the cost of a workstation is not the purchase price but the labour of keeping it alive, so reduce the variety and automate the routine.

Three tasks recur for every workstation, in this order:

1. **Loading the operating system** (and applications) onto a bare disk.
2. **Configuring** it: network settings, accounts, printers, policies.
3. **Updating** it forever: security patches, application upgrades.

If these three are done by hand, each machine becomes a unique snowflake that nobody can reproduce. If they are done by one script or image, then rebuilding a broken machine takes ten minutes and the user simply gets a clean one.

### 2.1.2 Architecture design

| Architecture | Idea | Advantages | Limits |
|---|---|---|---|
| **Thick client (fat)** | Full OS and applications run locally; server holds files and logins | Works offline, uses cheap server resources, good graphics | Many machines to patch; user data may stay on the disk |
| **Thin client** | Little more than a screen, keyboard and a small OS; applications run on a server (terminal services, X, web apps) | Central control, low client cost and power, long life | Server and network become critical; heavy graphics suffer |
| **Virtual desktop (VDI)** | Each user has a desktop virtual machine in the data centre; any device displays it | Same desktop from anywhere, central backup and patching | Needs strong servers, storage and network; licensing complexity |
| **Bring your own device (BYOD)** | Staff use personal laptops and phones | Lower hardware cost | Weak control of security; needs MDM and clear policy |

Design decisions that matter for every architecture:

- **Standardise**: one or two hardware models and one OS image per department. A computer lab with 60 identical PCs can be reinstalled in an afternoon; 60 different PCs cannot.
- **Keep data off the workstation**: users' files live on a file server or a cloud drive, so a failed workstation is only a hardware problem, never a data loss. Profile folders are redirected to the server.
- **Separate the OS from the data and the applications**, so the OS can be reinstalled without touching user work.
- **Management from the centre**: a directory (Active Directory or LDAP) for logins, group policy or a configuration-management tool for settings, and a patch server for updates.
- **Make the user's life predictable**: the same desktop, printers and drive letters wherever they sign in.
- **Plan for the user without a keyboard job**: accessibility, a lab for students and a locked-down kiosk need different policies.

### 2.1.3 Hardware strategy

| Question | Good practice |
|---|---|
| **How many models?** | As few as possible; buy in batches from one vendor so drivers, spare parts and the image stay the same |
| **How long to keep?** | A **refresh cycle** of three to five years; old machines cost more in support and power than the saving |
| **Buy or lease?** | Leasing turns a large single payment into a fixed yearly cost and forces refresh; buying is cheaper over a long life if you can dispose of old hardware responsibly |
| **Which specification?** | Match the work: office tasks need a modest CPU, 8 to 16 GB RAM and an SSD; design or development laptops need more; a lab with browsers only can use cheaper machines |
| **Warranty and spares** | Three years on-site warranty; a small stock of spare keyboards, mice, power supplies and a few complete machines for instant swap |
| **Laptops** | Full-disk encryption, asset tags, tracking and a lock, because the data on a lost laptop is worth more than the laptop |
| **Disposal** | Wipe or physically destroy disks; follow e-waste rules |

A short calculation shows why the refresh cycle is a budget item, not an afterthought.

```python
# Yearly cost of a PC fleet with a 4-year refresh (illustrative NPR figures)
fleet = 120
price = 65000          # per PC
cycle = 4              # years
support_per_pc_year = (4000, 6000, 9000, 14000)   # support grows as machines age
purchases_per_year = fleet / cycle
capital = purchases_per_year * price
support = sum(fleet / cycle * s for s in support_per_pc_year)
print("PCs replaced per year :", int(purchases_per_year))
print("capital per year      :", int(capital))
print("support per year      :", int(support))
print("total per year        :", int(capital + support))
print("per PC per year       :", int((capital + support) / fleet))
```

The cheapest yearly cost per machine is usually found where the rising support cost meets the falling cost per year of ownership: a fleet that is never refreshed has no capital cost this year, but its support bill and its failures keep growing.

### 2.1.4 Operating-system installation

There are four ways to put an OS on a workstation, from the most manual to the most automatic.

| Method | How | Use when |
|---|---|---|
| **Manual install** | Boot from a USB or DVD and answer the questions | One machine, a lab experiment |
| **Disk cloning** | Install and configure one **golden image**, capture it (Clonezilla, Ghost, `dd`), restore it on identical hardware | Identical hardware in a lab |
| **Generalised image** | Windows `sysprep` or Linux `cloud-init` removes machine-specific data (name, SID, SSH keys) before capture, so the image fits different hardware | Mixed hardware, many sites |
| **Network (automated) install** | The machine boots over the network with **PXE**, fetches an installer and an answer file, installs unattended | A fleet, any hardware, no USB sticks |

**PXE network boot** needs three services on the install server. The firmware's network card asks for an address with **DHCP**, and the DHCP reply also names a boot server and file; the client downloads a small boot loader by **TFTP** (or HTTP); the loader fetches the kernel and an **answer file**, and the installer reads the packages from an HTTP, NFS or SMB share. The answer file is called **kickstart** on Red Hat family systems, **preseed** (older) or **autoinstall** (Ubuntu 20.04 and later) on Debian and Ubuntu, and an **unattend.xml** on Windows (served by **Windows Deployment Services** and the Deployment Toolkit).

```svgfig label="2.1" caption="Network (PXE) installation of a workstation: the client needs addressing, a loader, an answer file and the packages."
f = Fig(660, 240)
f.box(20, 90, 120, 60, "New PC\nPXE boot\nin firmware", fill=SAND, stroke=AMBER, size=10)
f.box(250, 20, 130, 50, "DHCP server\naddress + boot file", fill=BLUE, stroke=NAVY, size=10)
f.box(250, 95, 130, 50, "TFTP / HTTP\nboot loader, kernel", fill=BLUE, stroke=NAVY, size=10)
f.box(250, 170, 130, 50, "Answer file\nkickstart / autoinstall", fill=BLUE, stroke=NAVY, size=10)
f.box(500, 95, 140, 50, "Package mirror\nHTTP / NFS / SMB", fill=SOFT, stroke=SLATE, size=10)
f.arrow([(140, 105), (250, 50)], color=NAVY, label="1 DHCP request", lpos=(165, 62))
f.arrow([(140, 120), (250, 120)], color=NAVY, label="2 fetch loader", lpos=(195, 112))
f.arrow([(140, 138), (250, 190)], color=NAVY, label="3 fetch answers", lpos=(170, 178))
f.arrow([(380, 120), (500, 120)], color=SLATE, label="4 packages", lpos=(440, 112))
```

**Configuration after installation.** The installer's job ends with a minimal system. A **configuration-management** tool (Ansible, Puppet, Chef, or Group Policy on Windows) then applies the rest: install the office suite, join the domain, set the printers, disable unneeded services. Because the description is stored centrally, a reinstalled machine ends up identical to the others.

**Updating.** Patches are fetched once from the vendor to a **local repository** (WSUS or Windows Update for Business; an internal `apt` or `dnf` mirror), tested on a pilot group, then pushed to everyone in stages. Never let every machine download from the internet at 9 a.m.; it wastes the link and makes a bad patch hit all users at once.

::: example Lab: install Ubuntu Server 22.04 in a virtual machine
1. Create a VM (2 vCPU, 2 GB RAM, 20 GB disk, bridged or NAT network) and attach the Ubuntu Server ISO.
2. Choose language and keyboard, network (DHCP first), a mirror and a storage layout; for a first install take "use entire disk" with LVM.
3. Create the administrator user, tick **Install OpenSSH server**, and finish.
4. After the reboot: `sudo apt update && sudo apt upgrade`, `ip addr`, `ssh user@address` from another machine.
5. Take a **snapshot**. Break something on purpose, restore the snapshot, and note how quick recovery is.
On Windows Server 2022 the equivalent steps are: boot the ISO, choose *Standard (Desktop Experience)*, set the administrator password, rename the computer, assign a static address and run Windows Update.
:::

