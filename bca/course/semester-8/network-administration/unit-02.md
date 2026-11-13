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
```output
PCs replaced per year : 30
capital per year      : 1950000
support per year      : 990000
total per year        : 2940000
per PC per year       : 24500
```
At a four-year cycle the fleet costs about NPR 2.94 million a year, NPR 24,500 per PC, and a third of it is support. The point of the model is the shape of the support column: it climbs steeply in the last years of a machine's life, so stretching the cycle saves capital only by paying more in repairs, downtime and staff time. A fleet that is never refreshed has no capital cost this year, but its support bill and failures keep growing.

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

## 2.2 Servers

### 2.2.1 A server is not a big workstation

A **server** is a computer whose job is to provide a service to other computers. It differs from a workstation in what is demanded of it:

| Aspect | Workstation | Server |
|---|---|---|
| Users | One | Tens to thousands at once |
| Failure impact | One person stops | Everyone who depends on the service stops |
| Location | On a desk | In a locked, cooled room or data centre, in a rack |
| Hardware | Consumer or business class, optimised for price | Server class: ECC memory, redundant power and disks, remote management |
| Administration | Local, by the user's side | Remote, by the administrator, with a console only in emergencies |
| Maintenance | Reboot at any time | Planned maintenance windows, change control |
| Life | 3-5 years | 4-7 years with warranty extensions |
| Cost of an hour of failure | Low | Often higher than the cost of the machine |

The consequence is simple and important: **do not run a service on a workstation.** A desktop PC under a desk quietly becomes "the file server" when someone shares a folder, and nobody remembers it until the disk fails.

### 2.2.2 Hardware strategies

**Choose the platform for the service.** A mail server with thousands of mailboxes is limited by disk input/output; a database server by memory and storage speed; a file server by capacity and network bandwidth; a web server by CPU and network. Decide first what the bottleneck is.

**Few models, bought in quantity.** As with workstations, buying one or two standard models from one vendor lowers spare-parts stock, simplifies remote management and lets one installation procedure fit all. Buy the **next year's** needs, not only today's, because a server's life is long.

**Form factors.**

| Form | Description | Use |
|---|---|---|
| **Tower** | Looks like a PC | One or two servers in a small office |
| **Rack-mount** | 19-inch wide, height in **rack units** (1U = 44.45 mm) | The normal choice; many servers per rack |
| **Blade** | Thin boards sliding into a shared chassis with common power and networking | High density in a large data centre |
| **Virtual** | A virtual machine on a hypervisor (VMware ESXi, Hyper-V, KVM, Proxmox) | Most services today |

**Virtualisation and consolidation.** A single powerful host runs many virtual machines, each with its own OS and service. Benefits: better hardware use (physical servers used to idle at 5-15% CPU), quick provisioning, snapshots, live migration to another host when one fails or needs maintenance. Costs: the host is now a single point of failure for all its guests (so use at least two hosts and shared storage), noisy neighbours and licence rules. A good pattern is one VM per service, so that the mail server can be upgraded without touching the web server.

**Support and spares.** A server's value is its uptime, so buy a **maintenance contract** (four-hour or next-business-day on-site replacement, as the service requires) and keep **spare parts** on the shelf for items that fail most: disks, power supplies, fans, memory. For a college with one critical server, a spare disk of the right type in the cabinet is worth more than a long warranty.

**Select vendors with server experience.** A vendor who sells both cheap PCs and servers is not the same as one who supports servers 24 hours a day; ask for references and for the local service centre, which matters in Nepal where parts often have to be imported.

### 2.2.3 Hardware features and specifications

When reading a server specification, check these items in this order:

| Feature | What to look for |
|---|---|
| **CPU** | Number of cores and clock; server CPUs (Intel Xeon, AMD EPYC) support more memory, more PCIe lanes and **two sockets**; licensing of some software is counted per core |
| **Memory** | **ECC** (error-correcting) RAM, which detects and fixes single-bit errors that corrupt data silently; free slots for growth; databases and virtualisation want plenty |
| **Storage** | **Hot-swap** bays, a hardware **RAID controller** or software RAID/ZFS; SSD or NVMe for random access, HDD for cheap capacity |
| **Network** | At least two ports (1 or 10 Gbit/s) for redundancy or **NIC teaming/bonding**; a separate management port |
| **Power** | **Redundant hot-swap power supplies** fed from two different circuits (or a UPS and mains); an **UPS** for clean shutdown |
| **Remote management** | **IPMI, iDRAC, iLO or similar**: a small independent controller giving remote power control, console and hardware alarms even if the OS is dead |
| **Cooling and noise** | Front-to-back airflow, hot-swap fans; datasheet gives watts and BTU |
| **Rack kit** | Rails, cable-management arm, height in U |

**RAID** (redundant array of independent disks) combines several disks to gain speed, protection or both. It protects against a **disk failure**, not against deletion, corruption, fire or theft, so RAID is never a backup.

| Level | Layout | Usable capacity of n equal disks | Survives | Typical use |
|---|---|---|---|---|
| **RAID 0** | Striping, no redundancy | n | Nothing | Scratch space, speed only |
| **RAID 1** | Mirror | n/2 (two disks: 1) | One disk per mirror pair | OS disks, small servers |
| **RAID 5** | Striping with one parity block per stripe | n - 1 | One disk | File servers, read-heavy |
| **RAID 6** | Two parity blocks | n - 2 | Two disks | Large arrays of big disks |
| **RAID 10** | Mirrors that are striped | n/2 | One disk per mirror (at least) | Databases, write-heavy |

```python
# Usable capacity and failure tolerance of RAID levels for 8 disks of 4 TB
n, size = 8, 4
levels = {
    "RAID 0":  (n * size,       "none"),
    "RAID 1":  (n * size / 2,   "one per mirror pair"),
    "RAID 5":  ((n - 1) * size, "1 disk"),
    "RAID 6":  ((n - 2) * size, "2 disks"),
    "RAID 10": (n * size / 2,   "1 per mirror pair"),
}
for name, (cap, tol) in levels.items():
    print("%-8s usable %5.1f TB  (%3.0f%% of raw)  survives: %s" % (name, cap, 100 * cap / (n * size), tol))

# Chance that a second disk fails during the rebuild of RAID 5 (illustrative)
afr = 0.02                 # 2% annual failure rate per disk
rebuild_hours = 24
p_one = afr * rebuild_hours / (365 * 24)
p_any = 1 - (1 - p_one) ** (n - 1)
print("P(another disk fails during 24 h rebuild) = %.4f%%" % (100 * p_any))
```
```output
RAID 0   usable  32.0 TB  (100% of raw)  survives: none
RAID 1   usable  16.0 TB  ( 50% of raw)  survives: one per mirror pair
RAID 5   usable  28.0 TB  ( 88% of raw)  survives: 1 disk
RAID 6   usable  24.0 TB  ( 75% of raw)  survives: 2 disks
RAID 10  usable  16.0 TB  ( 50% of raw)  survives: 1 per mirror pair
P(another disk fails during 24 h rebuild) = 0.0383%
```
Raw capacity costs money, so the table is also a price list: RAID 6 on eight 4 TB disks gives 24 TB of usable space from 32 TB bought, and RAID 10 gives only 16 TB. The small rebuild risk printed above is for random failure; in real arrays disks from the same batch, a hot room or a long rebuild of very large disks raise it sharply, which is why RAID 6 is preferred for big disks.

**Power and cooling estimate.** Every watt a server draws becomes a watt of heat. A rack of ten servers at 400 W each draws 4 kW, which needs about 4 kW of cooling; a UPS must be sized in VA with some margin (power factor about 0.9).

```python
servers, watts = 10, 400
load_w = servers * watts
heat_btu_hr = load_w * 3.412
ups_va = load_w / 0.9 * 1.25          # power factor 0.9 and 25% headroom
battery_wh_for_15min = load_w * 0.25 / 0.9   # 15 minutes at 90% inverter efficiency
print("load            : %d W" % load_w)
print("heat to remove  : %.0f BTU/h (%.2f kW cooling)" % (heat_btu_hr, load_w / 1000))
print("UPS rating      : %.0f VA" % ups_va)
print("battery for 15 m: %.0f Wh" % battery_wh_for_15min)
```
```output
load            : 4000 W
heat to remove  : 13648 BTU/h (4.00 kW cooling)
UPS rating      : 5556 VA
battery for 15 m: 1111 Wh
```
### 2.2.4 Installing and hardening a server

A server is installed by the same automated method as a workstation (Section 2.1.4) but with extra care:

1. **Use a minimal installation** (no desktop, no games, no compilers unless needed), because every installed package is a possible vulnerability.
2. **Static address, hostname that follows the naming plan, and DNS entries** (forward and reverse) before the service goes live.
3. **Partition sensibly**: separate `/var` and data from the OS disk so that logs or mail cannot fill the root filesystem.
4. **Update**, enable the firewall (`ufw`, `firewalld` or Windows Defender Firewall) and **allow only the ports the service needs**.
5. **Secure remote access**: SSH keys instead of passwords, no root login over SSH, administrator accounts named per person, RDP only through a VPN.
6. **Time synchronisation** (NTP or `chrony`) so that logs from different machines can be compared.
7. **Logging and monitoring** enabled from the first day; send logs to a central log server.
8. **Record** the build in the inventory: hardware, serial number, location, owner, service, warranty end and the date of the last backup test.

```bash
# first ten minutes on a new Ubuntu server (not run in the build sandbox)
sudo hostnamectl set-hostname mail01.college.edu.np
sudo apt update && sudo apt -y upgrade
sudo ufw default deny incoming && sudo ufw allow OpenSSH && sudo ufw enable
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config   # only after your key works
sudo systemctl restart ssh
timedatectl set-ntp true
```

::: caution Never lock yourself out
Disable password login for SSH only after a key-based login works in a second terminal window; otherwise a single typing mistake locks you out of a remote server.
:::

## 2.3 Services

### 2.3.1 What a service is

A **service** is something the customer values: "e-mail that works", "the college website", "a printer queue", "a login that follows me from lab to lab". It is more than the server that runs it. A service includes the **software, the hardware, the network paths, the data, the monitoring, the backup, the documentation, the support procedure and the people who run it**. One service often depends on others: mail needs DNS, authentication, storage and the network. A service that works on the day it launches but cannot be monitored, backed up or upgraded is half a service.

```svgfig label="2.2" caption="The life cycle of a service: each stage has its own checklist, and the cycle repeats at every major upgrade."
f = Fig(660, 210)
f.box(15, 70, 100, 50, "Requirements\nwith customers", fill=SAND, stroke=AMBER, size=10)
f.box(140, 70, 100, 50, "Plan and\nengineer", fill=BLUE, stroke=NAVY, size=10)
f.box(265, 70, 100, 50, "Launch\n(pilot, roll-out)", fill=BLUE, stroke=NAVY, size=10)
f.box(390, 70, 100, 50, "Operate and\nmonitor", fill=BLUE, stroke=NAVY, size=10)
f.box(515, 70, 130, 50, "Upgrade, convert\nor retire", fill=SOFT, stroke=SLATE, size=10)
for x in (115, 240, 365, 490):
    f.arrow([(x, 95), (x + 25, 95)], color=NAVY)
f.arrow([(580, 120), (580, 170), (65, 170), (65, 120)], color=SLATE, dash=True, label="next generation of the service", lpos=(320, 185))
f.text(190, 40, "SLA written here", size=9, color=SLATE)
f.text(440, 40, "SLO, alarms, backups", size=9, color=SLATE)
```

### 2.3.2 Requirements

Planning starts by asking the **customers** (not only the managers) what they need. Convert wishes into requirements that can be tested.

| Category | Questions | Example for a college mail service |
|---|---|---|
| **Functional** | What must it do? | Send and receive mail for 2,500 users; 5 GB mailbox; calendar; mobile access |
| **Availability** | When must it be up? How much downtime is tolerable? | 99.9% during 7 a.m. to 9 p.m.; planned maintenance Saturday night |
| **Performance** | How fast, for how many? | Mail delivered inside 1 minute; 300 simultaneous users at peak |
| **Capacity and growth** | How much, growing how fast? | 20% growth per year in mailbox storage |
| **Security and privacy** | Who may access what? | MFA for staff; encrypted connections; spam and malware filtering |
| **Support** | Who helps, how fast? | Help desk replies in 1 hour; urgent issues 24 x 7 |
| **Compliance and retention** | What must be kept and for how long? | Mail kept two years; deleted mail recoverable for 30 days |
| **Budget** | One-off and running cost? | Within the approved budget, with licences counted |

The agreed list becomes a **service-level agreement (SLA)**: a document between the service owner and the customers that states what is promised (availability, response times, support hours), how it is measured and what happens if it is not met. Inside the IT team the measurable targets are **service-level objectives (SLOs)**; the SLA is usually looser than the SLO so that the team has room to fix problems before breaking a promise.

### 2.3.3 Planning and engineering

**Design principles.**

- **Simplicity**: choose the simplest design that meets the requirements; a design that one person can explain on a whiteboard can be repaired at 3 a.m.
- **Standard components**: use supported, widely used products so that documentation and engineers are easy to find.
- **Machine independence**: clients should refer to the service by a **DNS alias** (`mail.college.edu.np`), never by the server's own name or address, so that the service can be moved to new hardware without touching a single client.
- **Restrict access**: only the people and machines that need to reach the service can reach it (firewalls, VLANs, accounts).
- **Separate the environments**: a **test** and a **production** copy, so that the change is first tried where failure does no harm.
- **Redundancy where it pays**: remove single points of failure for critical services.

**Redundancy and availability.** The availability of a component is **A = MTBF / (MTBF + MTTR)**, where MTBF is the mean time between failures and MTTR the mean time to repair. When components are chained so that **all** must work (a **series** system), availabilities multiply and the whole is *worse* than its weakest part. When identical components are **in parallel** so that **any one** is enough, unavailabilities multiply and the whole is *better*.

```python
# Availability: series and parallel
def avail(mtbf, mttr): return mtbf / (mtbf + mttr)

web  = avail(2000, 4)       # hours
db   = avail(3000, 8)
net  = 0.9995
print("web %.5f  db %.5f  net %.5f" % (web, db, net))
series = web * db * net
print("series (all needed)      : %.5f  -> %.1f h down per year" % (series, (1 - series) * 8760))

# two identical web servers behind a load balancer (either is enough)
web2 = 1 - (1 - web) ** 2
series2 = web2 * db * net
print("web tier with two servers : %.7f" % web2)
print("with redundant web tier  : %.5f  -> %.1f h down per year" % (series2, (1 - series2) * 8760))

# N+1: eight servers needed at peak, plus one spare; each 99% available
from math import comb
a, n = 0.99, 9
p_ok = sum(comb(n, k) * a**k * (1 - a)**(n - k) for k in range(8, n + 1))
print("N+1 (need 8 of 9)        : %.5f" % p_ok)
print("no spare (need 8 of 8)   : %.5f" % (a ** 8))
```
```output
web 0.99800  db 0.99734  net 0.99950
series (all needed)      : 0.99485  -> 45.1 h down per year
web tier with two servers : 0.9999960
with redundant web tier  : 0.99684  -> 27.7 h down per year
N+1 (need 8 of 9)        : 0.99656
no spare (need 8 of 8)   : 0.92274
```
Read the result carefully. Redundancy at the web tier improves the whole only until the next weakest link (the database or network) dominates, so effort is best spent on the **least available component**. **N+1** means having one more unit than the load needs, so that one failure does not reduce service; for a service where the loss of two units is unacceptable use N+2.

**Capacity planning.** Estimate the peak load, add growth and headroom, and check each resource (CPU, memory, disk, network). A simple model: if requests arrive at rate λ and a server finishes them at rate μ, utilisation is ρ = λ/μ and the average time in the system for a single queue is 1/(μ - λ) (the M/M/1 model). The delay explodes as utilisation approaches 100%, so aim for 60-70% at peak.

```python
mu = 100.0                         # requests the server can finish per second
for lam in (50, 70, 80, 90, 95, 99):
    rho = lam / mu
    resp_ms = 1000 / (mu - lam)    # M/M/1 average time in system
    print("load %2d%%  average response %6.1f ms" % (lam, resp_ms))

# growth: storage need in 3 years with 20% yearly growth from 4 TB, keep 30% free
need = 4 * 1.2 ** 3
print("storage after 3 years: %.2f TB; buy %.2f TB for 30%% free space" % (need, need / 0.7))
```
```output
load 50%  average response   20.0 ms
load 70%  average response   33.3 ms
load 80%  average response   50.0 ms
load 90%  average response  100.0 ms
load 95%  average response  200.0 ms
load 99%  average response 1000.0 ms
storage after 3 years: 6.91 TB; buy 9.87 TB for 30% free space
```
**Dependencies and failure modes.** Draw what the service depends on (DNS, authentication, network, power, storage, licence server) and what depends on it. In an outage, the dependency chain explains why "mail is down" may be a DNS fault, and in a plan it shows which dependency needs redundancy first.

### 2.3.4 Service launch

Launching a service is a controlled change, not a switch-on. The prescribed text recommends a **launch readiness review**, a checklist that must be passed before customers use the service:

1. **Requirements met** and demonstrated in a test.
2. **Monitoring in place**: alarms for the service, not only for the server; alarms reach a person.
3. **Backup and restore tested**, not only configured.
4. **Documentation**: how to operate, start, stop, upgrade and recover; who to call.
5. **Security reviewed**: patched, firewall rules, accounts, encryption.
6. **Capacity checked** against a load test.
7. **Support ready**: the help desk has been trained and has a script for the common questions.
8. **Communication**: customers know the date, what changes for them and where to ask for help.

The **roll-out** itself should be gradual: first an **internal pilot** with the IT staff, then a small group of friendly customers (a **beta**), then the department-by-department or percentage roll-out. At every step decide a **rollback**: how to return to the previous state if the launch fails. A launch on the first day of an examination week is a bad idea; choose a quiet period and avoid Fridays, because a failure over a weekend finds nobody at the office.

### 2.3.5 Disaster recovery

A **disaster** is any event that stops a service for far longer than normal faults do: fire, flood, earthquake (a real planning input in Nepal), power failure, ransomware, theft, a destroyed disk array, a fatal human mistake. **Disaster recovery (DR)** is the plan that restores the service; **business continuity** is the wider plan for the organisation to keep working in the meantime.

**Steps in DR planning.**

1. **Risk analysis**: list possible disasters, their likelihood and their impact; decide which services matter most.
2. **Set the objectives** for each service:
   - **RTO (recovery time objective)**: how long the service may be down.
   - **RPO (recovery point objective)**: how much recent data may be lost, measured in time. An RPO of 1 hour means the backups or replication must be at most an hour old.
3. **Choose the strategy** that meets RTO and RPO within budget.
4. **Write the plan**: ordered steps, contacts, passwords stored securely and offline, where the backup tapes or copies are, and who decides.
5. **Test the plan** at least yearly, by a real restore or a drill. A DR plan that has not been tested is only a hope.

| Recovery site | Description | Recovery time | Cost |
|---|---|---|---|
| **Cold site** | Empty room with power and network; hardware must be brought and set up | Days to weeks | Low |
| **Warm site** | Hardware installed, data restored from the latest backup | Hours to a day | Medium |
| **Hot site** | Fully equipped and continuously replicated copy, ready to take over | Minutes | High |
| **Cloud DR** | Copy of the service in the cloud, started on demand | Minutes to hours | Pay for use |

**Data protection basics.** Follow the **3-2-1 rule**: keep **three** copies of important data, on **two** different kinds of media, with **one** copy off-site (and, today, one that cannot be changed, **immutable**, against ransomware). Offsite does not mean the next room: choose a different building, or a cloud region far from the first site.

```python
# Does a chosen strategy meet the objectives?  (illustrative numbers)
services = {
  "Fee portal":  dict(rto_h=2,  rpo_h=1,  backup_every_h=24,  restore_h=3),
  "Website":     dict(rto_h=24, rpo_h=24, backup_every_h=24,  restore_h=2),
  "Mail":        dict(rto_h=8,  rpo_h=4,  backup_every_h=4,   restore_h=6),
}
for name, s in services.items():
    ok_rpo = s["backup_every_h"] <= s["rpo_h"]
    ok_rto = s["restore_h"] <= s["rto_h"]
    print("%-11s RPO %-4s RTO %-4s" % (name, "ok" if ok_rpo else "FAIL", "ok" if ok_rto else "FAIL"))
```
```output
Fee portal  RPO FAIL RTO FAIL
Website     RPO ok   RTO ok  
Mail        RPO ok   RTO ok  
```
The fee portal fails both objectives with a nightly backup and a three-hour restore: it needs frequent log shipping or replication and a faster recovery path, a clear example of why objectives come before products.

## 2.4 Summary and exercises

Manage workstations as a fleet: few models, a standard image, data on servers, a refresh cycle of three to five years, installation by PXE and answer files, and central configuration and patching. A server is built for many users and for uptime: ECC memory, hot-swap disks with the right RAID level (RAID is not backup), redundant power, remote management, racks and enough power and cooling, and it is installed minimally and hardened. A service is the whole delivered thing: gather requirements and write an SLA, plan with simplicity, DNS aliases, test and production separation, redundancy (series and parallel availability, N+1) and capacity (keep utilisation near 60-70%), pass a launch readiness review and roll out in stages, and prepare disaster recovery with RTO, RPO, a chosen site type, the 3-2-1 backup rule and regular tests.

1. Why is the cost of a workstation more than its purchase price? How does standardisation reduce it?
2. Compare thick client, thin client and virtual desktop architectures.
3. Explain the three tasks of workstation management (load, configure, update).
4. Discuss the hardware strategy for a fleet of 100 PCs, including refresh cycle, spares and warranty.
5. Describe PXE network installation. What are the roles of DHCP, TFTP, the answer file and the package mirror?
6. Differentiate a server and a workstation. Why should a service not run on a workstation?
7. List and explain eight features to examine in a server specification.
8. Compare RAID 0, 1, 5, 6 and 10 for capacity and fault tolerance. Why is RAID not a backup?
9. What is virtualisation? State two benefits and two risks of server consolidation.
10. List the steps to harden a new Linux server.
11. Define service, SLA and SLO. What should be asked of customers when gathering requirements?
12. State the design principles for a service. Why use a DNS alias for the service name?
13. Define availability. Compute the availability of a chain of three components of 99.9% each, and of two 99% components in parallel.
14. What is a launch readiness review? List its items and the stages of a roll-out.
15. Define disaster recovery, RTO and RPO. Compare cold, warm and hot sites. State the 3-2-1 rule.
16. Eight 2 TB disks are used in RAID 6. How much space is usable? A UPS must carry 6 servers of 350 W for 10 minutes: estimate the load and the battery energy.

**Answers to the numerical items.** (13) Series: 0.999^3 = 0.997003, about 99.70%; parallel: 1 - 0.01^2 = 0.9999, 99.99%. (16) RAID 6 usable = (8 - 2) x 2 = 12 TB. Load = 6 x 350 = 2,100 W; energy for 10 minutes = 2,100 x 10/60 = 350 Wh; allowing 90% efficiency, about 389 Wh, and the rating in VA is 2,100 / 0.9 = 2,333 VA before headroom.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain PXE network installation of workstations.**

PXE lets a computer with no operating system install itself over the network. The firmware sends a DHCP request; the DHCP server replies with an address and the name of a boot server and boot file. The client downloads a boot loader over TFTP or HTTP, which loads a kernel and an answer file (kickstart for Red Hat family, autoinstall or preseed for Ubuntu and Debian, unattend.xml with Windows Deployment Services). The installer then reads the packages from a mirror over HTTP, NFS or SMB and installs without questions. Advantages: no USB sticks, same installation on every machine, any hardware, easy re-installation; after installation a configuration-management tool applies the remaining settings.

**Q2 (5 marks). What are RTO and RPO? How do they influence the backup design?**

RTO is the longest time a service may be down; RPO is the largest amount of recent data, measured in time, that may be lost. A nightly backup gives an RPO of up to 24 hours, so a service with an RPO of one hour needs more frequent backups, log shipping or replication. A restore that takes six hours cannot meet an RTO of two hours, so a standby or replicated copy is needed. The objectives, set with the business, are fixed first; the technology and the cost follow from them.

**Q3 (10 marks). Describe how a new e-mail service for a college is planned and launched.**

Requirements: ask staff, students and managers; list functions (2,500 mailboxes, 5 GB, calendar, mobile), availability (99.9% in working hours), performance, growth (20% a year), security (MFA, TLS, spam and malware filtering), support and retention; write them as an SLA with measurable SLOs.

Planning and engineering: choose a simple, supported design; reach it by a DNS alias such as mail.college.edu.np; separate test from production; use redundancy where the availability arithmetic shows a weak link (a second mail gateway, mirrored disks); plan capacity from users, mailbox size and 20% growth with 30% free space; list dependencies (DNS, directory, storage, network, power).

Launch: pass a readiness review (requirements tested, monitoring and alarms, backup and a trial restore, documentation, security review, load test, trained help desk, announcement). Roll out through an IT pilot, a beta group and then departments, with a rollback plan, avoiding examination weeks and Fridays.

Operation and disaster recovery: choose RTO and RPO, apply the 3-2-1 rule with an off-site immutable copy, test a restore each term, and review capacity and SLOs regularly.
