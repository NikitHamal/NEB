---
subject: Hardware Workshop
grade: BCA Semester 1
unit: 6
title: Basic Networking Configuration
area: BCA 106 · Hardware Workshop · Unit 6
---

Cables and boxes do nothing until they are configured. This unit teaches you to plan an IP address scheme, work out subnets by hand, configure a router, switch and wireless access point, build small LAN and WLAN networks, and prove that they work with the standard diagnostic commands.

::: key What this unit gives you
- IPv4 addressing: classes, private ranges, subnet mask, gateway, DNS, DHCP and CIDR notation.
- Subnetting by hand with checked examples.
- Router and switch configuration (console setup and command line), access point setup (SSID, password, MAC filtering) and signal testing.
- Star and bus builds, and the tools ping, tracert, ipconfig, netstat, arp, nslookup, route and netsh.
- A mini LAN/WLAN lab task with a viva.
:::

## 6.1 IP addressing

An **IPv4 address** is 32 bits written as four decimal bytes (octets), for example 192.168.10.25. It has two parts: a **network part** that names the network and a **host part** that names the device. The **subnet mask** says where the split is: ones cover the network part. 255.255.255.0 is /24 in **CIDR** notation (24 ones).

| Class | First octet | Default mask | Hosts per network | Use |
|---|---|---|---|---|
| A | 1 to 126 | 255.0.0.0 (/8) | 16,777,214 | Very large networks |
| B | 128 to 191 | 255.255.0.0 (/16) | 65,534 | Medium networks |
| C | 192 to 223 | 255.255.255.0 (/24) | 254 | Small LANs |
| D | 224 to 239 | none | none | Multicast |
| E | 240 to 255 | none | none | Experimental |

127.0.0.0/8 is **loopback** (`127.0.0.1` is the PC itself). Classes are historical; today routing uses CIDR prefixes of any length, but the class names are still examined.

**Private addresses (RFC 1918)** are not routed on the internet and are reused in every LAN: **10.0.0.0/8**, **172.16.0.0/12** (172.16.0.0 to 172.31.255.255) and **192.168.0.0/16**. The router uses **NAT** to share one public address. A PC that cannot reach DHCP gives itself an **APIPA** address in 169.254.0.0/16 and cannot leave its subnet, which is a useful diagnostic sign.

**Other settings on a host**

- **Default gateway:** the router interface on the local subnet, used for every destination outside it (for example 192.168.10.1).
- **DNS server:** converts names such as `www.tu.edu.np` to IP addresses (for example 8.8.8.8 or the ISP's server).
- **DHCP:** a service (usually in the router) that hands out address, mask, gateway and DNS automatically and leases them for a time; **static** addressing is typed by hand and is used for servers, printers and routers.

::: example Worked example: valid addresses on a /24
Network 192.168.10.0/24 has 2⁸ = 256 addresses. The first (192.168.10.0) is the **network address**, the last (192.168.10.255) the **broadcast address**, so **254 hosts** (192.168.10.1 to .254) can be used. If the router takes .1, a DHCP pool of .100 to .199 gives 100 clients, leaving .2 to .99 for fixed devices such as the printer (.10) and servers.
:::

## 6.2 Subnetting by hand

**Subnetting** borrows host bits to create smaller networks. With *h* host bits left, a subnet has 2ʰ addresses and **2ʰ − 2** usable hosts. With *b* borrowed bits you get 2ᵇ subnets. The **block size** is the step between subnet network addresses in the interesting octet (256 minus the mask value in that octet).

```svgfig label="6.1" caption="Subnetting 192.168.10.0/24 into four /26 subnets. Two bits are borrowed from the host part, so the mask becomes 255.255.255.192, each subnet has 64 addresses (62 usable) and the networks start at .0, .64, .128 and .192."
f = Fig(760, 220)
f.text(380, 16, "Last octet, 8 bits:  [ 2 subnet bits | 6 host bits ]", size=12, color=NAVY, bold=True)
for i in range(8):
    col = BLUE if i < 2 else SOFT
    f.box(180 + i * 48, 30, 44, 34, "0", fill=col, stroke=NAVY, size=12, bold=True)
f.text(228, 80, "network (borrowed)", size=10.5, color=TEAL, bold=True)
f.text(468, 80, "host bits (6)", size=10.5, color=SLATE, bold=True)
nets = [("Subnet 1", ".0 /26", "hosts .1 to .62", "bcast .63"), ("Subnet 2", ".64 /26", "hosts .65 to .126", "bcast .127"), ("Subnet 3", ".128 /26", "hosts .129 to .190", "bcast .191"), ("Subnet 4", ".192 /26", "hosts .193 to .254", "bcast .255")]
for i, (a, b, c, d) in enumerate(nets):
    x = 14 + i * 184
    f.box(x, 108, 170, 92, a + "\n" + b + "\n" + c + "\n" + d, fill="#ffffff", stroke=NAVY, size=11)
```

**Method (five steps).**

1. Decide how many subnets or how many hosts per subnet are needed.
2. Find *b* (subnets: 2ᵇ ≥ needed) or *h* (hosts: 2ʰ − 2 ≥ needed).
3. New prefix = old prefix + *b* (or 32 − *h*).
4. Write the mask and the block size.
5. List the network, host range and broadcast of each subnet.

::: example Worked example 1: a subnet that holds 50 hosts
2⁵ − 2 = 30 is too small; 2⁶ − 2 = **62** is enough. So *h* = 6 and the prefix is 32 − 6 = **/26**, mask **255.255.255.192**, block size 256 − 192 = **64**.
:::

::: example Worked example 2: which subnet is 192.168.1.77/28 in?
/28 leaves 4 host bits, 16 addresses, block size 16, mask 255.255.255.240. Subnet boundaries in the last octet: 0, 16, 32, 48, 64, 80. The address .77 lies in the block starting at **192.168.1.64**; the broadcast is **192.168.1.79**; usable hosts **.65 to .78** (14 hosts).
:::

::: example Worked example 3: eight subnets from a Class B network
Divide 172.16.0.0/16 into 8 subnets: 2³ = 8, so borrow 3 bits, new prefix **/19**, mask **255.255.224.0**. Each subnet has 2¹³ − 2 = **8,190 hosts**. Networks: 172.16.0.0, 172.16.32.0, 172.16.64.0, and so on up to 172.16.224.0.
:::

**Supernetting** (combining) is the opposite: two /24 networks 192.168.50.0 and 192.168.51.0 aggregate into 192.168.50.0/23 with mask 255.255.254.0 and 510 usable hosts.

**VLSM (variable-length subnet masks).** Use a different prefix for each subnet to waste fewer addresses: for example a /30 (2 usable hosts) for a router-to-router link, a /26 for a lab of 50 PCs, and a /28 for 10 servers, all taken from one block.

## 6.3 Router and switch configuration

**Access methods.** A new router or switch is first configured through its **console port** with a rollover cable (Unit 2) and a terminal program (PuTTY, Tera Term) at 9600 baud, 8 data bits, no parity, 1 stop bit, no flow control. Later you can use SSH or the web page of the device. Home routers use the browser page at the default gateway address, such as `http://192.168.1.1`.

**Cisco-style command line (a standard lab example).**

```text
Router> enable
Router# configure terminal
Router(config)# hostname R1
R1(config)# interface gigabitEthernet 0/0
R1(config-if)# ip address 192.168.10.1 255.255.255.0
R1(config-if)# no shutdown
R1(config-if)# exit
R1(config)# line console 0
R1(config-line)# password nebians
R1(config-line)# login
R1(config-line)# end
R1# show ip interface brief
R1# copy running-config startup-config
```

The prompts change as the **mode** changes: user EXEC (`>`), privileged EXEC (`#`), global configuration and interface configuration. `no shutdown` brings a port up, `show ip interface brief` lists every interface with its address and status, and `copy running-config startup-config` saves so the work survives a reboot.

**Switch.** An unmanaged switch needs no configuration. A managed switch gets a management IP on its VLAN interface (`interface vlan 1`, `ip address 192.168.10.2 255.255.255.0`, `ip default-gateway 192.168.10.1`), a password, and optionally **VLANs** (separate broadcast domains on one switch) and port security.

**Home router setup.**

1. Connect a PC to a LAN port and the modem to the WAN port; open the gateway address in a browser.
2. Change the default admin password.
3. Set the WAN type (DHCP, PPPoE with the ISP's user name and password, or static).
4. Set the LAN address (192.168.10.1/24), DHCP range and DNS.
5. Set the Wi-Fi name, security and channel (6.4); save and reboot.

## 6.4 Wireless access points and extenders

An **access point** joins Wi-Fi clients to the wired LAN. Its main settings are:

| Setting | Meaning | Good practice |
|---|---|---|
| **SSID** | The network name clients see | Unique, no personal data |
| **Security** | Encryption and authentication | WPA2-AES at least, WPA3 where supported; never WEP or open |
| **Password** | The pre-shared key | 12 or more characters, not the default |
| **Band and channel** | 2.4 GHz (longer range, crowded) or 5 GHz (faster, shorter) | On 2.4 GHz use the non-overlapping channels **1, 6 or 11** |
| **MAC filtering** | Allow only listed MAC addresses | Adds a little control but is **not security**, since MACs can be copied |
| **DHCP** | Hand out addresses | Off on a second AP that sits behind a router |

**Hiding the SSID** does not protect the network either; the name is still sent in every client's probe request. The real protection is a strong WPA2/WPA3 password.

**Signal test.** A phone app or `netsh wlan show interfaces` shows the **RSSI** in dBm (closer to zero is stronger).

| RSSI | Quality | Use |
|---|---|---|
| −30 to −50 dBm | Excellent | All uses |
| −50 to −67 dBm | Good | Video calls, streaming |
| −67 to −70 dBm | Fair | Web and email |
| −70 to −80 dBm | Weak | Drops and slow speeds |
| below −80 dBm | Unusable | Move the AP or add one |

**Extender.** Put it about halfway between the router and the dead spot, where the router's signal is still better than −70 dBm, join it to the router through its setup page or WPS button, and copy the same SSID. Better: a wired AP, or a **mesh** system.

## 6.5 Network design and building the lab topologies

**Design steps.** (1) List the devices and their locations. (2) Choose the topology (star for almost every LAN). (3) Choose the IP plan and subnets. (4) Choose devices and cables with a 20 % spare capacity of ports. (5) Draw the diagram and label it. (6) Configure, test and document.

```svgfig label="6.2" caption="Mini LAN/WLAN for the lab. PCs and a printer connect to a switch by straight-through cables; the switch connects to the router (gateway 192.168.10.1); the access point serves laptops on the same 192.168.10.0/24 subnet. DHCP runs on the router with a pool from .100 to .199."
f = Fig(760, 250)
f.box(300, 14, 160, 44, "Router  192.168.10.1\nDHCP  .100 to .199", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(300, 100, 160, 40, "Switch", fill=SOFT, stroke=NAVY, size=12, bold=True)
f.arrow([(380, 58), (380, 100)], color=NAVY)
hosts = [("PC1  .10", 20), ("PC2  .11", 160), ("Printer  .50", 560)]
f.box(20, 190, 120, 40, "PC1  .20", fill="#ffffff", stroke=TEAL, size=11)
f.box(160, 190, 120, 40, "PC2  .21", fill="#ffffff", stroke=TEAL, size=11)
f.box(300, 190, 150, 40, "Printer  .50 (static)", fill="#ffffff", stroke=TEAL, size=11)
f.arrow([(330, 140), (80, 190)], color=TEAL)
f.arrow([(350, 140), (220, 190)], color=TEAL)
f.arrow([(380, 140), (375, 190)], color=TEAL)
f.box(580, 100, 160, 40, "Access point", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(460, 120), (580, 120)], color=NAVY)
f.box(580, 190, 160, 40, "Laptops (Wi-Fi, DHCP)", fill="#ffffff", stroke=AMBER, size=10.5)
f.arrow([(660, 140), (660, 190)], color=AMBER)
```

**Build and test a star network.** Connect each PC to the switch, set static addresses 192.168.10.20, .21 with mask 255.255.255.0 and gateway 192.168.10.1 (`netsh interface ip set address "Ethernet" static 192.168.10.20 255.255.255.0 192.168.10.1`), then ping each other. **Bus network.** On real hardware (old coaxial hardware or a hub-based demonstration) all stations share one medium; observe that when two stations transmit at once the collision LED flashes and throughput falls, which is why the star replaced it.

## 6.6 Testing and diagnostics: the command toolkit

| Command (Windows / Linux) | Purpose | Typical use |
|---|---|---|
| `ping host` (`-n 4` or `-c 4`; `-t` repeat) | Tests reachability with ICMP echo and reports round-trip time | `ping 192.168.10.1` |
| `tracert host` / `traceroute host` | Lists each router hop to the destination | find where a path breaks |
| `ipconfig /all` / `ip addr`, `ifconfig` | Shows IP, mask, gateway, DNS, MAC, DHCP | check configuration |
| `ipconfig /release` and `/renew` | Drops and requests a new DHCP lease | fix 169.254 addresses |
| `ipconfig /flushdns` | Clears the DNS resolver cache | after changing DNS |
| `netstat -an` (`-r` for routes) | Lists open ports and connections | spot unwanted services |
| `arp -a` | Shows the IP to MAC cache | detect duplicate IPs |
| `nslookup name` | Asks DNS for an address | test name resolution |
| `route print` / `ip route` | Shows or edits the routing table | check the default route |
| `netsh` | Windows network shell: set addresses, show Wi-Fi profiles and signal | `netsh wlan show interfaces` |

**The diagnostic ladder.** Work from the inside out and stop at the first failure.

1. `ping 127.0.0.1`: is the TCP/IP software working?
2. `ping` your own IP: is the NIC configured and enabled?
3. `ping` the default gateway: is the local link (cable, switch, VLAN) working?
4. `ping 8.8.8.8`: does the router reach the internet?
5. `ping www.google.com`: if only this fails, DNS is the problem.

::: example Worked example: reading a ping result
`Reply from 192.168.10.1: bytes=32 time=1ms TTL=64` means the gateway answers in 1 ms. `Request timed out` means no reply (device off, firewall or broken path). `Destination host unreachable` from your own address means the local routing or ARP failed; from another address it means a router has no route. A TTL of 64 suggests Linux or a router; 128 suggests Windows.
:::

## 6.7 Troubleshooting common issues and the mini LAN/WLAN task

| Symptom | Likely cause | Fix |
|---|---|---|
| IP starts with 169.254 | DHCP not reachable | check cable and switch; `ipconfig /renew`; restart router |
| Can ping IP but not names | DNS wrong | set DNS to 8.8.8.8, `ipconfig /flushdns` |
| "IP address conflict" | Two hosts with one address | change one; `arp -a` to find the MAC |
| Ping gateway works, internet fails | WAN or ISP fault, PPPoE login wrong | check modem and router status page |
| Wi-Fi connected, no internet | Wrong gateway or DNS, AP behind another DHCP | fix the settings, turn off the second DHCP |
| Slow Wi-Fi | Crowded channel, weak signal | change channel (1, 6, 11), move closer |

**Mini LAN/WLAN task (lab).** Build the network of Figure 6.2 with a router, a switch, two PCs, a printer and a laptop: (1) draw and label the plan; (2) set the router LAN address and DHCP pool; (3) set a static address on the printer; (4) set the Wi-Fi SSID with WPA2 and a strong password; (5) verify with the diagnostic ladder from each PC; (6) save the configuration and document it. **Viva questions:** What is the default gateway? Why is the printer static? What does the subnet mask do? How would you find an IP conflict? Why does MAC filtering not secure Wi-Fi?

## 6.8 Eight rules for network configuration

1. Plan the addressing on paper before touching a device.
2. Keep one subnet per VLAN or per network, and never overlap them.
3. Use static addresses for infrastructure and DHCP for clients.
4. Change every default password at once.
5. Use WPA2 or WPA3, and a non-default SSID.
6. Test from the inside out with the diagnostic ladder.
7. Save the configuration and keep a backup file.
8. Document addresses, passwords (in a safe place) and cable labels.

## Formula and fact sheet

- Usable hosts = 2ʰ − 2 (h host bits); subnets = 2ᵇ (b borrowed bits); block size = 256 − (mask octet).
- Common masks: /24 = 255.255.255.0; /25 = .128; /26 = .192; /27 = .224; /28 = .240; /30 = .252.
- Private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. APIPA 169.254.0.0/16. Loopback 127.0.0.1.
- Classes: A 1 to 126, B 128 to 191, C 192 to 223, D 224 to 239, E 240 to 255.
- Wi-Fi 2.4 GHz non-overlapping channels: 1, 6, 11. RSSI better than −67 dBm for good service.
- Diagnostic ladder: loopback, own IP, gateway, remote IP, DNS name.

## Chapter summary

- An IPv4 address has a network part and a host part, split by the mask; private ranges are reused in every LAN.
- Subnetting borrows host bits: a /26 gives four subnets of 62 hosts; the mask and block size follow from the prefix.
- Routers and switches are configured from the console or a web page, and the configuration must be saved.
- Access points need an SSID, WPA2/WPA3 security and a sensible channel; MAC filtering is not security.
- Ping, tracert, ipconfig, netstat, arp, nslookup, route and netsh form the standard toolkit, applied in the diagnostic ladder.

## Practice

1. Convert 255.255.255.224 to CIDR and state hosts per subnet.
2. Find network, broadcast and host range of 192.168.5.130/26.
3. A lab needs 25 PCs; what is the smallest subnet and mask?
4. Divide 192.168.20.0/24 into 4 equal subnets; list the networks.
5. State the three private ranges and why they exist.
6. List the five rungs of the diagnostic ladder with the command for each.
7. Write the Cisco commands to give interface g0/0 the address 10.0.0.1/24 and save.
8. Explain why hiding the SSID and MAC filtering are weak protection.
9. A PC shows 169.254.33.8. What happened and what do you do?
10. Name four uses of `netsh` or `netstat`.

::: note Answers and worked solutions
**1.** 255.255.255.224 = /27 (3 borrowed bits in the last octet, 5 host bits); 2⁵ − 2 = **30 hosts**.
**2.** /26: block 64; .130 lies in 128 to 191. Network **192.168.5.128**, broadcast **192.168.5.191**, hosts **.129 to .190**.
**3.** 2⁵ − 2 = 30 ≥ 25, so 5 host bits: **/27, 255.255.255.224**.
**4.** Two borrowed bits: /26 networks 192.168.20.0, .64, .128, .192.
**5.** 10/8, 172.16/12, 192.168/16: they save public IPv4 addresses and are made usable on the internet through NAT.
**6.** `ping 127.0.0.1`; `ping` own IP; `ping` gateway; `ping 8.8.8.8`; `ping www.google.com` (DNS).
**7.** `interface g0/0`, `ip address 10.0.0.1 255.255.255.0`, `no shutdown`, `end`, `copy running-config startup-config`.
**8.** The SSID is still broadcast in probe packets and MAC addresses can be sniffed and spoofed; use WPA2/WPA3 with a strong key.
**9.** APIPA: no DHCP answer. Check the cable and switch, run `ipconfig /renew`, restart the router or set a static IP.
**10.** `netsh interface ip set address` (set IP), `netsh wlan show profiles` (saved Wi-Fi), `netstat -an` (open ports), `netstat -r` (routing table).
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Explain IP address classes and private IP addresses.**

IPv4 addresses are divided into classes by the first octet: A (1 to 126, /8), B (128 to 191, /16), C (192 to 223, /24), D (224 to 239, multicast) and E (reserved). Private addresses are 10.0.0.0/8, 172.16.0.0/12 and 192.168.0.0/16; they are not routed on the internet and are reused inside every LAN, with NAT in the router providing internet access through one public address.

**Q (10 marks). Subnet 192.168.10.0/24 into four equal subnets and give the network, host range and broadcast of each. Explain how you would configure and test one of them.**

*Subnetting.* Four subnets need 2 borrowed bits, so the prefix is /26 and the mask 255.255.255.192; block size 64; each subnet has 62 hosts (Figure 6.1).

| Subnet | Network | Hosts | Broadcast |
|---|---|---|---|
| 1 | 192.168.10.0 | .1 to .62 | .63 |
| 2 | 192.168.10.64 | .65 to .126 | .127 |
| 3 | 192.168.10.128 | .129 to .190 | .191 |
| 4 | 192.168.10.192 | .193 to .254 | .255 |

*Configuration.* Give the router interface .1 of subnet 1 with mask 255.255.255.192, enable DHCP for .10 to .60, set a static address for the printer, and set each PC with gateway 192.168.10.1.

*Testing.* Run `ipconfig /all` for the settings, then the diagnostic ladder: loopback, own address, gateway, 8.8.8.8 and a name; `tracert` shows where a path breaks. Save the configuration with `copy running-config startup-config`.
