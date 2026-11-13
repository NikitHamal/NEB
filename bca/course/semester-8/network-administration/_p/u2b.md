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

