## 3.2 Network operations

Building a network is a project; **operating** it is the job that never ends. Operations means the routines that keep the network known, observed, controlled and secure.

### 3.2.1 Documentation

Documentation is the memory of the network. Without it, knowledge lives in one person's head and leaves when that person does. Keep, at least:

| Document | Contents |
|---|---|
| **Network diagrams** | Physical (buildings, closets, links, speeds) and logical (VLANs, subnets, routing, firewall zones) |
| **Address and VLAN plan** | Subnet, VLAN number, gateway, DHCP range, purpose, owner |
| **Inventory** | Each device: model, serial, location, firmware, warranty end, purpose |
| **Cable and port records** | Patch-panel port to switch port, outlet number and room |
| **Configuration archive** | Current and previous configuration of every device |
| **Runbooks** | Step-by-step procedures: restart a service, replace a switch, add a user |
| **Contacts and escalation** | ISP support number, circuit IDs, vendor contract numbers, on-call list |

Keep it in a **wiki** or document system that is backed up and reachable even when the network is down (a printed copy of the essential pages, in the equipment room, is not old-fashioned). Make updating the document part of the change itself: a change is not finished until the document is changed. Label cables, ports and devices physically, because a diagram that disagrees with the wall is worse than none.

### 3.2.2 Monitoring

You cannot manage what you cannot see, and customers should never be the monitoring system. Monitoring answers: is it up, is it healthy, is it filling up, is it being attacked.

| Mechanism | What it does |
|---|---|
| **Ping / ICMP, TCP checks** | Is the device or port reachable? |
| **SNMP** (v2c, preferably v3) | Polls counters (interface traffic, errors, CPU, temperature) and receives **traps** |
| **Syslog** | Devices send log messages to a central log server |
| **NetFlow / sFlow / IPFIX** | Summaries of who talks to whom, for capacity and incident analysis |
| **Synthetic checks** | A script that logs in and sends a test mail, to check the service the way a user does |
| **Dashboards and alerts** | Graphs of trends and rules that notify a person |

Tools: Nagios, Zabbix, LibreNMS, Prometheus with Grafana, PRTG, and cloud monitors. Good practice:

- Monitor **services as seen by users**, and also the devices and links beneath them.
- Alert only on what needs **action**; too many alarms teach people to ignore all alarms (alert fatigue).
- Set thresholds with a margin (disk 80% warning, 90% critical) and watch **trends**, not only current values.
- Store history to plan capacity: a link that peaks at 70% in March will not survive examination season next year.
- Monitor the monitor, and keep it independent from what it watches.

The utilisation of a link from two SNMP counter readings is a routine calculation:

```python
# Link utilisation from two readings of an SNMP interface octet counter
interval_s = 300
octets_t0, octets_t1 = 1_200_000_000, 1_950_000_000
link_bps = 100_000_000          # a 100 Mbit/s link
bits = (octets_t1 - octets_t0) * 8
bps = bits / interval_s
print("traffic over 5 min : %.1f Mbit/s" % (bps / 1e6))
print("utilisation        : %.1f %%" % (100 * bps / link_bps))
# a 32-bit counter wraps at 2**32; use the 64-bit counter (ifHCInOctets) on fast links
wrap = 2 ** 32
t0, t1 = 4_200_000_000, 150_000_000       # counter rolled over between the readings
delta = (t1 - t0) % wrap
print("delta after wrap   :", delta, "octets")
```

### 3.2.3 Configuration management and change control

Every network device has a configuration; unrecorded changes are the commonest source of outages. Practice:

1. **Back up configurations automatically** after every change (a scheduled job or a tool such as RANCID, Oxidized or Ansible) and store them in **version control** so that you can see who changed which line and roll back.
2. **Use templates and standards**: all access switches share one template differing only by name, address and VLANs.
3. **Change control**: a written request describing what, why, risk, test and **back-out plan**; review by a second person; a planned **maintenance window**; notification to users; verification after the change; update of documentation.
4. **Test first** on a lab or lower-risk device; change one thing at a time; keep a console path (out-of-band access) so that a mistake in remote configuration does not need a drive to the site.
5. **Emergency changes** are allowed but written up afterwards.
6. **Firmware and patching**: follow vendor security advisories; upgrade in stages.

### 3.2.4 Core network services: DHCP and DNS

**DHCP** assigns addresses, gateway, DNS servers and lease times automatically. Use **reservations** (by MAC address) for printers and devices that must keep an address; keep servers on static addresses outside the DHCP range. **DNS** converts names to addresses and is the dependency of nearly everything, so run **at least two DNS servers** on different hosts. A small Linux example with `dnsmasq` serves both:

```ini
# /etc/dnsmasq.d/lab.conf   (not run in the build sandbox)
interface=eth1
domain=lab.college.edu.np
dhcp-range=10.20.20.50,10.20.20.200,255.255.255.0,12h
dhcp-option=option:router,10.20.20.1
dhcp-option=option:dns-server,10.20.20.2
dhcp-host=00:1a:2b:3c:4d:5e,printer1,10.20.20.10
address=/gw.lab.college.edu.np/10.20.20.1
```

The namespace design for DNS and directories is dealt with in Unit 4.

### 3.2.5 Network security operations

- **Segmentation**: separate VLANs for staff, labs, servers, guests and management, with the router or firewall allowing only the flows that are needed.
- **Firewall rules** are evaluated **top to bottom, first match wins**, ending with an implicit or explicit *deny all*. Put specific rules before general ones; comment each rule with its purpose and owner; review them yearly and remove stale ones.
- **Access to devices**: SSH not Telnet, individual accounts via TACACS+/RADIUS, a management VLAN, MFA for administrators, disabled unused ports.
- **Layer-2 protections**: port security, DHCP snooping, BPDU guard, disabled unused trunk negotiation.
- **Logging and review**: log denied traffic and administrator logins; review regularly.

The following program shows first-match evaluation, the idea behind every ACL.

```python
import ipaddress as ip
rules = [  # (action, source net, destination net, port or None = any)
    ("deny",   "10.20.20.0/24", "10.20.40.0/24", None),   # labs -> servers (blocked)
    ("permit", "10.20.20.0/24", "10.20.40.10/32", 443),   # labs -> web server only (never reached, shadowed)
    ("permit", "10.20.10.0/24", "10.20.40.0/24", None),   # staff -> servers
    ("permit", "0.0.0.0/0",     "0.0.0.0/0",     80),     # anyone -> web
    ("deny",   "0.0.0.0/0",     "0.0.0.0/0",     None),   # default deny
]
def check(src, dst, port):
    for n, (act, s, d, p) in enumerate(rules, 1):
        if ip.ip_address(src) in ip.ip_network(s) and ip.ip_address(dst) in ip.ip_network(d) and p in (None, port):
            return act, n
tests = [("10.20.10.5", "10.20.40.7", 22), ("10.20.20.9", "10.20.40.10", 443),
         ("10.20.20.9", "8.8.8.8", 80), ("10.20.20.9", "8.8.8.8", 25)]
for t in tests:
    print("%-12s -> %-12s port %-3d : %s by rule %d" % (t[0], t[1], t[2], *check(*t)))
```

The second rule can never match because rule 1 already denies the same traffic; this **shadowing** is a common firewall error. The administrator corrects it by putting the specific *permit* above the general *deny*.

### 3.2.6 The troubleshooting toolkit

| Task | Linux | Windows |
|---|---|---|
| Local addresses and links | `ip addr`, `ip link`, `ethtool` | `ipconfig /all` |
| Reachability | `ping`, `ping -6` | `ping` |
| Path | `traceroute`, `mtr` | `tracert`, `pathping` |
| DNS | `dig name`, `nslookup` | `nslookup`, `Resolve-DnsName` |
| Open ports and sockets | `ss -tulpn` | `netstat -ano`, `Test-NetConnection host -Port 443` |
| Routing table, ARP | `ip route`, `ip neigh` | `route print`, `arp -a` |
| Packet capture | `tcpdump -i eth0 port 53`, Wireshark | Wireshark, `pktmon` |
| Throughput | `iperf3` | `iperf3` |

::: example A user cannot open the college website
1. `ipconfig` shows address 169.254.12.7: the PC got no DHCP lease (APIPA). Layer 3 is wrong before anything else.
2. The link light is on and the VLAN is correct, so check the DHCP scope: it shows all 200 addresses leased, the pool is **exhausted** by phones and guests.
3. Fix: shorten the lease time on the Wi-Fi VLAN to one hour and enlarge the pool from /24 to /23 in the next window; document the change.
4. Verify: new lease, `ping` the gateway, `nslookup www.college.edu.np`, open the site.
Root cause (address exhaustion), not the symptom (no site), was fixed, and the monitoring now alerts at 80% pool use.
:::

