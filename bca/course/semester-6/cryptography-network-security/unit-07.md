---
subject: Cryptography and Network Security
grade: BCA Semester 6
unit: 7
title: Network and System Security - Firewalls, IDS, VPN and Wireless
hours: 5
area: BCA 353 · Cryptography and Network Security · Unit 7
---

Cryptography protects data in transit and at rest, but a network also needs *perimeters, sensors and discipline*: something that decides which packets may enter, something that notices an intruder who got in anyway, safe wireless links, protection against malware and, underneath it all, careful management of keys. This last unit covers firewalls (with a rule-matching program that was executed), intrusion detection (with the base-rate calculation that surprises everyone), VPNs, wireless security, common attacks and their defences, and key management.

::: key What this unit gives you
- Firewall types, rule ordering and default-deny, with an executed first-match example.
- IDS and IPS: signature and anomaly detection; detection rate, false alarms and the base-rate fallacy with numbers.
- VPNs, Wi-Fi security (WEP to WPA3), common attacks (DoS, spoofing, SQL injection, phishing, malware) and defences.
- Key management and a practical security checklist.
:::

## 7.1 Firewalls

A **firewall** enforces a policy on traffic between networks of different trust (the Internet and a college LAN). Types: a **packet-filter** firewall inspects each packet's header (protocol, source and destination address and port) against rules, statelessly; a **stateful inspection** firewall tracks connections (it allows return traffic only for connections that were initiated from inside); an **application-layer firewall / proxy** understands protocols (HTTP, SQL) and can filter content; a **next-generation firewall (NGFW)** adds application identification, intrusion prevention, and TLS inspection; a **web application firewall (WAF)** protects web apps from injection and cross-site scripting; a **host firewall** runs on each machine. A **DMZ (demilitarised zone)** is a separate segment for public servers (web, mail) so that a compromised server cannot reach the internal LAN directly.

The principles: **default deny** (anything not explicitly allowed is blocked), **least privilege** (open only the ports needed), **first match wins** (rules are checked in order, so specific rules go before general ones), **log** what is denied, and **review** rules regularly. The program evaluates four packets against an ordered rule list (rule 3 blocks SSH to one server from outside; rule 4 then allows web access to it; rule 5 is the default deny):

```python
import ipaddress

rules = [
    ("allow", "tcp", "10.0.0.0/24", "any", 80),
    ("allow", "tcp", "10.0.0.0/24", "any", 443),
    ("deny", "tcp", "any", "10.0.0.7", 22),
    ("allow", "tcp", "any", "10.0.0.7", 80),
    ("deny", "any", "any", "any", 0),
]

def match(rule, proto, src, dst, port):
    act, rp, rs, rd, rport = rule
    if rp not in ("any", proto):
        return False
    if rs != "any" and ipaddress.ip_address(src) not in ipaddress.ip_network(rs):
        return False
    if rd != "any" and dst != rd:
        return False
    return rport in (0, port)

tests = [("tcp", "10.0.0.5", "203.0.113.9", 443), ("tcp", "198.51.100.4", "10.0.0.7", 22),
         ("tcp", "198.51.100.4", "10.0.0.7", 80), ("udp", "10.0.0.5", "8.8.8.8", 53)]
for t in tests:
    for i, r in enumerate(rules, 1):
        if match(r, *t):
            print(t[0], t[1], "->", t[2] + ":" + str(t[3]), "=>", r[0], "(rule %d)" % i)
            break
```
```output
tcp 10.0.0.5 -> 203.0.113.9:443 => allow (rule 2)
tcp 198.51.100.4 -> 10.0.0.7:22 => deny (rule 3)
tcp 198.51.100.4 -> 10.0.0.7:80 => allow (rule 4)
udp 10.0.0.5 -> 8.8.8.8:53 => deny (rule 5)
```
Swapping rules 3 and 4 would not change these four results, but moving the broad `deny` of rule 5 to the top would block everything: the order is part of the policy. Firewalls do not stop attacks that arrive over allowed channels (a malicious attachment, a web-application flaw), which is why they are one layer of **defence in depth**.

## 7.2 Intrusion detection and prevention

An **intrusion detection system (IDS)** monitors traffic or hosts and raises **alerts**; an **intrusion prevention system (IPS)** also blocks. A **network IDS (NIDS)** watches a network tap; a **host IDS (HIDS)** watches logs, files and processes on one machine (file-integrity monitoring). Detection methods: **signature-based** (match known attack patterns: accurate for known attacks, blind to new ones) and **anomaly-based** (flag deviations from a learned normal: can find new attacks but produces false alarms). Tools: Snort and Suricata (network), Zeek (traffic analysis), OSSEC/Wazuh (host), collected into a **SIEM** for correlation. A **honeypot** is a decoy system that has no legitimate use, so any contact with it is suspicious.

### The base-rate fallacy

An IDS is judged by its **detection rate** (true-positive rate) and **false-alarm rate** (false-positive rate). Suppose attacks are rare: **0.1%** of events are attacks, the IDS detects **99%** of attacks and falsely flags **1%** of normal events. Out of 1,00,000 events: 100 are attacks, of which **99** are detected; 99,900 are normal, of which **999** are flagged falsely. The total number of alerts is **1,098**, so the probability that an alert is a real attack is 99 / 1,098 = **9.0%**. By Bayes' rule, P(attack | alert) = (0.99 × 0.001) / (0.99 × 0.001 + 0.01 × 0.999). A "99% accurate" detector therefore produces alerts that are about **91.0%** false: analysts drown unless the false-alarm rate is driven down far below the base rate. This is why tuning, whitelisting, and ranking alerts by context matter more than raw detection rate.

## 7.3 VPNs

A **virtual private network (VPN)** creates an encrypted tunnel across a public network, so that a remote worker or a branch office behaves as if on the private LAN. Types: **site-to-site** (gateways joined with IPsec, Unit 6) and **remote-access** (a client connects to a gateway, with IPsec/IKEv2, TLS-based VPN, or **WireGuard**, a modern small VPN using Curve25519, ChaCha20-Poly1305 and BLAKE2). A VPN protects traffic from the local network and links sites; it does *not* make the user anonymous, and it moves trust to the VPN endpoint. **Split tunnelling** sends only company traffic through the tunnel; full tunnelling sends everything. A **zero-trust** model removes the idea of a trusted inside: every request is authenticated, authorised and encrypted regardless of the network.

## 7.4 Wireless security

Wireless LANs broadcast, so encryption and authentication are essential. **WEP** (1997) used RC4 with a short IV and is broken in minutes. **WPA** (TKIP) was a stopgap; **WPA2** uses **AES-CCMP** and is secure with a strong passphrase, but a captured four-way handshake allows **offline dictionary attacks** and the 2017 **KRACK** attack exposed implementation flaws; **WPA3** (2018) replaces the pre-shared key handshake with **SAE** (a password-authenticated Diffie–Hellman, resisting offline guessing and giving forward secrecy) and mandates protection of management frames. **WPA2/WPA3-Enterprise** uses 802.1X with a RADIUS server and EAP (each user has credentials or a certificate: eduroam is an example). Practical rules: use WPA3 or WPA2-AES with a long random passphrase (a four-word passphrase has about 44 bits; a longer one is better), change default router passwords, disable WPS, keep firmware updated, separate guest and IoT networks, and be wary of public Wi-Fi (use HTTPS and a VPN). **Bluetooth** needs pairing checks and updates; **rogue access points** and **evil-twin** hotspots imitate legitimate names to capture traffic.

## 7.5 Common attacks and defences

| Attack | How it works | Defences |
|---|---|---|
| **Malware** (virus, worm, trojan, ransomware, spyware) | Malicious code spreads or hides, encrypts files for ransom | Patching, antivirus/EDR, least privilege, offline backups, email filtering |
| **Phishing / social engineering** | A fake message tricks the user into revealing credentials or running code | Training, MFA, domain checks, mail authentication (SPF, DKIM, DMARC) |
| **Denial of service (DoS/DDoS)** | Flood of traffic or requests exhausts capacity | Rate limiting, CDN/scrubbing, redundancy, SYN cookies |
| **Spoofing** (ARP, IP, DNS, email) | Forged identity or address | Ingress filtering, dynamic ARP inspection, DNSSEC, signed mail |
| **Man-in-the-middle / sniffing** | Intercepts or alters traffic | TLS with certificate validation, VPN, WPA3 |
| **SQL injection, XSS, CSRF** | Untrusted input interpreted as code or commands | Parameterised queries, output encoding, CSRF tokens, WAF |
| **Password attacks** | Guessing, credential stuffing, cracking leaked hashes | Salted slow hashes, MFA, lockout/rate limiting, breach checks |
| **Insider threat** | Misuse by authorised users | Least privilege, logging, separation of duties, audits |
| **Supply-chain attacks** | Compromised update or dependency | Signed updates, dependency pinning and review, SBOM |

The vulnerability life cycle is: discover, disclose, patch, deploy. Most breaches use **known** flaws that were not patched, so **patch management** and **asset inventory** are among the most effective controls. **Penetration testing** (with written authorisation, see *Society and Technology*, Unit 4) and **vulnerability scanning** find weaknesses before attackers do. **Incident response** has stages: preparation, detection, containment, eradication, recovery and lessons learned.

## 7.6 Key management and a security checklist

Cryptography moves the problem from protecting the data to **protecting the keys**: their **generation** (use a cryptographically secure random generator, never `rand()` or the clock), **distribution** (public-key or key-agreement protocols; never email a key), **storage** (hardware security modules, smartcards, the operating-system keystore; never in source code or a Git repository), **rotation** (periodic and after suspected compromise), **backup and recovery**, **revocation**, and **destruction**. Use **key hierarchies**: a master key encrypts data keys (envelope encryption), so that data keys can be rotated without re-encrypting everything. **Randomness** is critical: weak random numbers broke Netscape's SSL in 1995 and Debian's OpenSSL in 2008.

**Checklist for a small organisation:**

- Keep systems patched and software inventory current.
- Use MFA everywhere it is offered; enforce password-manager use and long passphrases.
- Use HTTPS/TLS 1.2+ (prefer 1.3), AEAD ciphers, certificates from a trusted CA, HSTS.
- Segment the network (guest, servers, DMZ); default-deny firewall rules.
- Back up with the 3-2-1 rule and test restores; keep one copy offline.
- Log centrally and review alerts; practise incident response.
- Encrypt laptops and phones; manage lost-device wiping.
- Train people; they are both the weakest link and the best sensor.

## 7.7 Seeing network defences: walls, zones, sensors and radios

Network security is a set of layers, each with its own device. The plates show the real boxes: the brick wall that gave the firewall its name, a commercial firewall appliance, a home router, an outdoor access point and a hardware security module that keeps keys. The figures draw a network with a demilitarised zone, the rule-matching of a packet filter, the base-rate arithmetic behind IDS alarms, a site-to-site VPN, the history of Wi-Fi security and the life cycle of a key.

```photogrid label="7.1" cols="2" ratio="1.2" caption="Where the word firewall comes from, and what it looks like today. (a) The blank side wall of a building (a fire wall, German Brandmauer) has no windows or doors so that a fire in one building cannot spread to the next: the same idea of a barrier that lets nothing through except what is deliberately built in. (b) A Cisco ASA 5510 security appliance: Ethernet ports for the outside, inside and DMZ networks, a flash card holding the configuration and the rule set, and cables for each zone."
@ photo id="crypto353/firewall-wall" cap="A fire wall (Brandmauer)"
fit 1.2
focus 0.3 0.5
call 0.3 0.12 0.2 0.5 "blank fire wall: no openings"
@ photo id="crypto353/asa" cap="Cisco ASA firewall appliance"
fit 1.2
focus 0.6 0.5
call 0.7 0.85 0.78 0.55 "Ethernet ports"
```

```svgfig label="7.1" caption="A network with a demilitarised zone (DMZ). The outer firewall allows the internet to reach only the public servers in the DMZ (web on port 443, mail on port 25) and blocks everything else. The inner firewall allows the internal network to initiate connections out and lets only the web server talk to the database on one port. If the web server is hacked, the attacker is still outside the internal network. The IDS watches both sides, and a VPN gateway gives staff a protected way in."
f = Fig(580, 230)
f.box(6, 80, 80, 70, "Internet", fill=ROSE, stroke=RED, size=12, bold=True)
f.box(116, 80, 70, 70, "Outer\nfirewall", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(216, 20, 150, 150, "", fill=MINT, stroke=TEAL, dash=True)
f.text(291, 36, "DMZ", size=12, color=TEAL, bold=True)
f.box(226, 50, 130, 38, "Web server :443", fill="#ffffff", stroke=TEAL, size=10.5, bold=True)
f.box(226, 100, 130, 38, "Mail server :25", fill="#ffffff", stroke=TEAL, size=10.5, bold=True)
f.box(396, 80, 70, 70, "Inner\nfirewall", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(496, 50, 78, 130, "Internal\nLAN:\ndatabase,\nstaff PCs", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
for a, b in ((86, 116), (186, 216), (366, 396), (466, 496)): f.arrow([(a, 115), (b, 115)], color=SLATE, both=True)
f.box(216, 186, 150, 34, "IDS sensors (watch both sides)", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(396, 186, 100, 34, "VPN gateway", fill=SAND, stroke=AMBER, size=10.5, bold=True)
```

```svgfig label="7.2" caption="A packet filter reads its rules from the top and acts on the first match; the last rule is a default deny. Here a packet from the internet to the web server on port 443 matches rule 1 and is allowed; a packet to port 23 (telnet) matches no allow rule and falls through to rule 4, so it is dropped. Putting a broad allow rule above a specific deny rule silently defeats the deny, so order matters. A stateful firewall adds a table of live connections so that replies to an inside request are let back in automatically."
f = Fig(580, 236)
hdr = ["#", "Action", "From", "To", "Port", "Note"]
xs = [8, 40, 110, 210, 330, 400]
f.box(4, 6, 572, 26, "", fill="#e2e8f0", stroke=SLATE, sw=1, r=3)
for h, x in zip(hdr, xs): f.text(x, 19, h, size=10.5, color=NAVY, bold=True, anchor="start")
rules = [("1", "ALLOW", "any", "web server", "443", "public HTTPS", MINT), ("2", "ALLOW", "any", "mail server", "25", "incoming mail", MINT), ("3", "ALLOW", "inside", "any", "any", "staff browsing", MINT), ("4", "DENY", "any", "any", "any", "default deny", ROSE)]
for i, (n, a, s, d, p, nt, fl) in enumerate(rules):
    y = 36 + i * 28
    f.box(4, y, 572, 24, "", fill=fl, stroke="#cbd5e1", sw=1, r=3)
    for v, x in zip((n, a, s, d, p, nt), xs): f.text(x, y + 12, v, size=10.5, color=(RED if v == "DENY" else SLATE), bold=(v in ("ALLOW", "DENY")), anchor="start", vmid=True)
f.text(8, 162, "Packet A: internet to web server, port 443", size=11, color=NAVY, bold=True, anchor="start")
f.text(330, 162, "matches rule 1: ALLOW", size=11, color=TEAL, bold=True, anchor="start")
f.text(8, 186, "Packet B: internet to web server, port 23", size=11, color=NAVY, bold=True, anchor="start")
f.text(330, 186, "matches rule 4: DENY (dropped)", size=11, color=RED, bold=True, anchor="start")
f.text(8, 212, "Rules are tried top to bottom; the first match decides.", size=10.5, color=SLATE, anchor="start")
```

```svgfig label="7.3" caption="Why a good IDS can still be wrong most of the time. Take 100,000 events of which only 0.1 percent (100) are attacks. The IDS detects 99 percent of attacks (99 alerts) but also flags 1 percent of the 99,900 normal events (999 false alerts). Of the 1,098 alerts only 99 are real, so an alert is a true attack only 9 percent of the time. The lesson is that the false-alarm rate must be far smaller than the attack rate, or analysts drown in noise."
f = Fig(580, 180)
f.box(8, 8, 564, 28, "100,000 events", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(8, 56, 56, 40, "100\nattacks", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(70, 56, 502, 40, "99,900 normal events", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(36, 36), (36, 56)], color=SLATE); f.arrow([(320, 36), (320, 56)], color=SLATE)
f.box(8, 116, 56, 38, "99\ndetected", fill=ROSE, stroke=RED, size=10, bold=True)
f.box(70, 116, 130, 38, "999 false alarms", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.arrow([(36, 96), (36, 116)], color=SLATE); f.arrow([(135, 96), (135, 116)], color=AMBER)
f.text(230, 128, "1,098 alerts in all:", size=12, color=NAVY, bold=True, anchor="start")
f.text(230, 148, "99 / 1,098 = 9.0 percent are real attacks", size=12, color=RED, bold=True, anchor="start")
f.text(230, 172, "(detection 99 percent, false alarms 1 percent, attacks 0.1 percent)", size=10, color=SLATE, anchor="start")
```

```svgfig label="7.4" caption="A site-to-site VPN. The Kathmandu head office and the Pokhara branch each have a VPN gateway. Packets between the two private networks are encrypted and wrapped by the gateways (IPsec tunnel mode), so the internet in between sees only gateway-to-gateway traffic. A remote-access VPN is similar, but the tunnel ends at a laptop with VPN software instead of a branch gateway. Both give confidentiality, integrity and authentication on an untrusted link."
f = Fig(580, 170)
f.box(6, 40, 120, 70, "Kathmandu\nhead office\n192.168.1.0/24", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(454, 40, 120, 70, "Pokhara\nbranch\n192.168.2.0/24", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(146, 50, 84, 50, "VPN\ngateway A", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(350, 50, 84, 50, "VPN\ngateway B", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.arrow([(126, 75), (146, 75)], color=SLATE, both=True); f.arrow([(434, 75), (454, 75)], color=SLATE, both=True)
f.box(230, 58, 120, 34, "Internet", fill=ROSE, stroke=RED, size=11, bold=True, dash=True)
f.line(230, 66, 350, 66, color=TEAL, sw=5); f.line(230, 84, 350, 84, color=TEAL, sw=5)
f.text(290, 126, "encrypted ESP tunnel", size=11, color=TEAL, bold=True)
f.text(290, 148, "only gateway addresses are visible outside", size=10.5, color=SLATE)
```

```svgfig label="7.5" caption="Wi-Fi security in four generations. WEP (1997) used RC4 with a 24-bit initialisation vector, so among 2 to the power 24 = 16,777,216 values a repeat is expected after about 4,800 packets, and it was broken within minutes. WPA (2003) was a stop-gap with TKIP. WPA2 (2004) uses AES-CCMP and is secure with a strong passphrase, but its pre-shared-key mode can be attacked offline from a captured handshake. WPA3 (2018) replaces it with SAE, which blocks offline guessing and gives forward secrecy."
f = Fig(580, 190)
G = [("WEP", "1997", "RC4, 24-bit IV\nbroken in minutes", ROSE, RED), ("WPA", "2003", "TKIP, stop-gap\nweak, deprecated", SAND, AMBER), ("WPA2", "2004", "AES-CCMP\noffline guessing risk", BLUE, NAVY), ("WPA3", "2018", "SAE handshake,\nforward secrecy", MINT, TEAL)]
for i, (n, y, d, fl, c) in enumerate(G):
    x = 8 + i * 144
    f.box(x, 14, 132, 38, n + "  (" + y + ")", fill=fl, stroke=c, size=12, bold=True)
    f.box(x, 62, 132, 54, d, fill="#ffffff", stroke=c, size=10.5, bold=True)
    if i < 3: f.arrow([(x + 132, 33), (x + 144, 33)], color=SLATE)
f.text(290, 148, "Recommendation: WPA3, or WPA2 with a long random passphrase.", size=11.5, color=NAVY, bold=True)
f.text(290, 170, "Never use WEP or an open network for anything private.", size=11, color=RED, bold=True)
```

```svgfig label="7.6" caption="The life cycle of a cryptographic key. A key is generated with a strong random source, distributed securely, activated for use, rotated before it is used too much or too long, backed up where needed, revoked at once if it is lost or exposed, and finally destroyed so that it cannot be recovered. A weakness at any step (a weak random number, a key left in a script, no rotation) breaks the strength of the algorithm."
import math
f = Fig(580, 230)
st = ["1 Generate\n(random)", "2 Distribute\n(securely)", "3 Use\n(limit scope)", "4 Rotate\n(regularly)", "5 Back up\n(if needed)", "6 Revoke\n(if exposed)", "7 Destroy\n(zeroise)"]
cx, cy, R = 290, 116, 88
pts = []
for i, s in enumerate(st):
    a = -math.pi / 2 + i * 2 * math.pi / 7
    pts.append((cx + 1.7 * R * math.cos(a), cy + R * math.sin(a)))
for i in range(7):
    p, q = pts[i], pts[(i + 1) % 7]
    f.line(p[0], p[1], q[0], q[1], color="#94a3b8", sw=1.4)
for i, s in enumerate(st):
    f.box(pts[i][0] - 52, pts[i][1] - 20, 104, 40, s, fill=(ROSE if i == 5 else MINT if i < 3 else BLUE), stroke=(RED if i == 5 else TEAL if i < 3 else NAVY), size=10.5, bold=True)
f.text(cx, cy - 4, "key", size=13, color=NAVY, bold=True); f.text(cx, cy + 14, "life cycle", size=11, color=SLATE)
```

```photogrid label="7.2" cols="3" ratio="0.95" caption="Radios and key stores. (a) A home or office wireless router with two antennas: it combines a Wi-Fi access point, a small firewall (network address translation and packet filtering) and a switch, and its default administrator password must be changed. (b) An outdoor wireless access point mounted on a brick wall: a campus can cover a courtyard with it, and a WPA2 or WPA3 setting protects the link. (c) A hardware security module, a tamper-resistant card that generates and stores keys so they never appear in server memory."
@ photo id="crypto353/wrt54g" cap="Wi-Fi router"
fit 0.95
focus 0.5 0.5
call 0.5 0.9 0.2 0.8 "antennas"
@ photo id="crypto353/ap" cap="Outdoor access point"
fit 0.95
focus 0.4 0.55
@ photo id="crypto353/hsm" cap="Hardware security module"
fit 0.95
focus 0.5 0.5
```

### 7.7.1 Eight practical rules to secure a campus or office network

1. **Default deny at the firewall.** Block every connection first, then allow only the ports that are needed, such as 443 for the web server. A forgotten open port is the most common way in. Review the rules every few months and remove ones nobody can explain.
2. **Separate zones.** Put public servers in a DMZ and keep student records on the internal network behind a second firewall. If the web server is hacked, the attacker still has a wall to climb. Guest Wi-Fi should be in its own network without access to staff systems.
3. **Patch quickly.** Most attacks use a flaw for which a fix already exists. Keep operating systems, routers, firewalls and web software updated, and track a list of what is installed. A forgotten old server is a favourite target.
4. **Use strong Wi-Fi security.** Choose WPA3 or WPA2 with a long random passphrase and change the router's default administrator password. Turn off WPS push-button setup if it is not needed. An open or WEP network lets any neighbour read and change traffic.
5. **Use VPN or SSH for remote work.** Staff working from home should connect through a VPN, and administrators should use SSH with keys rather than telnet. This prevents passwords and data from crossing the internet in plain form. Multi-factor authentication should protect the VPN login.
6. **Monitor and log.** An IDS and central logs show strange traffic and failed logins. Tune the alerts to reduce false alarms, as the base-rate example shows, otherwise real alarms are ignored. Keep logs safe from tampering and long enough for investigation.
7. **Manage keys and passwords.** Keep keys out of source code and shared folders, rotate them, and revoke them when a person leaves. Use a password manager and multi-factor authentication for important accounts. A hardware security module or a protected key store holds the most valuable keys.
8. **Back up and practise recovery.** Keep offline backups so that ransomware cannot encrypt them, and test the restore. Prepare a simple incident plan with names and phone numbers. Fast recovery is part of security, because no defence is perfect.

## Chapter summary

- Firewalls enforce ordered, first-match, default-deny rules; types range from packet filters to NGFWs and WAFs; DMZs isolate public servers.
- IDS/IPS use signatures or anomaly detection; with a rare attack (0.1%), a 99%-detecting, 1%-false-alarm IDS gives alerts that are about 91.0% false.
- VPNs tunnel traffic with IPsec, TLS or WireGuard; zero-trust assumes no trusted inside.
- WPA3 (SAE) replaces WPA2-PSK; WEP is broken; enterprise Wi-Fi uses 802.1X.
- Key management (secure generation, storage in HSMs/keystores, rotation, envelope encryption) decides whether the cryptography protects anything.

## Practice

1. Differentiate a packet-filter, a stateful and an application firewall.
2. Why does rule order matter in a firewall? Give an example.
3. What is a DMZ?
4. Distinguish signature-based and anomaly-based detection with one strength and weakness each.
5. An IDS has detection rate 95% and false-alarm rate 2%; attacks are 1% of events. Out of 10,000 events how many alerts are real and how many false?
6. What fraction of alerts in question 5 are real?
7. Why is WEP insecure and what does WPA3 improve?
8. List three defences against phishing.
9. State three rules for key storage.
10. What does the "least privilege" principle say?

::: note Answers and worked solutions
**1.** Packet filter: checks headers statelessly. Stateful: tracks connections and permits return traffic only for outbound-initiated flows. Application firewall: understands protocol content (for example HTTP) and filters it.
**2.** Rules are applied first-match: a rule "deny any" placed first blocks everything, while "allow tcp 80 to server" before it permits web access; the same rules in the opposite order behave differently.
**3.** A separate network segment for public-facing servers that limits damage if one is compromised.
**4.** Signature: accurate for known attacks, blind to new ones. Anomaly: can detect new attacks, but gives more false alarms.
**5.** Attacks: 100, detected 95 (**95 real alerts**); normal events 9,900, false alarms 2% = **198 false alerts**.
**6.** 95 / (95 + 198) = 95 / 293 = **32.4%** real (so 67.6% are false).
**7.** WEP uses RC4 with a short, reused IV and is crackable in minutes; WPA3 uses SAE (resistant to offline guessing, with forward secrecy) and protects management frames.
**8.** User training, multi-factor authentication, email authentication (SPF/DKIM/DMARC) and URL filtering.
**9.** Use an HSM, smartcard or OS keystore; never in source code or repositories; restrict access and rotate keys.
**10.** Each user or program should have only the access needed for its task and no more.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the types of firewall and the importance of rule order and default deny.**

*Introduction.* A firewall is a device or program that controls traffic between networks of different trust according to rules (section 7.1, Figure 7.2).

1. **Packet filter.** Decides for each packet from the IP addresses, ports and protocol. It is fast and simple but does not remember connections.
2. **Stateful firewall.** Keeps a table of connections, so replies to an inside request are allowed back automatically and unrelated incoming packets are dropped.
3. **Application (proxy) firewall.** Understands the application protocol, such as HTTP, and can block bad requests or malware. It is slower but gives more control. A next-generation firewall adds user identity and intrusion prevention.
4. **Rule order.** Rules are tried from the top and the first match decides, so a broad allow above a specific deny defeats the deny.
5. **Default deny.** The last rule denies everything not allowed above, so a mistake or a forgotten service fails safe.

| Type | Looks at | Strength | Weakness |
|---|---|---|---|
| Packet filter | Addresses, ports | Fast | No state |
| Stateful | Connection state | Safer replies | No content view |
| Application proxy | Application data | Deep control | Slower |

**Q2 (5 marks). Distinguish IDS from IPS and explain the base-rate fallacy with numbers.**

*Introduction.* An intrusion detection system (IDS) watches traffic or hosts and raises alerts; an intrusion prevention system (IPS) sits in the path and can also block (sections 7.2, Figure 7.3).

1. **IDS.** Passive, out of the path, so a failure does not stop traffic, but it only reports.
2. **IPS.** In line, so it can drop packets at once, but a false alarm blocks a legitimate user and the device is a possible point of failure.
3. **Detection methods.** Signature-based systems match known patterns (accurate for known attacks, blind to new ones). Anomaly-based systems learn normal behaviour (can see new attacks but raise more false alarms).
4. **Base-rate fallacy.** Let attacks be 0.1 percent of 100,000 events, detection 99 percent and false alarms 1 percent. There are 99 true alerts and 999 false ones, 1,098 in all, so only 99 / 1,098 = **9.0 percent** of alerts are real, although the IDS seems 99 percent accurate.
5. **Lesson.** Reduce the false-alarm rate (tune rules), and rank alerts by risk.

**Q3 (5 marks). Compare WEP, WPA2 and WPA3 for Wi-Fi security.**

*Introduction.* Wireless signals can be read by anyone nearby, so encryption and authentication are essential (section 7.4, Figure 7.5).

1. **WEP.** RC4 with a 24-bit IV and a CRC integrity check. Among 2 to the power 24 values a repeat is expected after about 4,800 packets, and the key can be recovered in minutes. Obsolete.
2. **WPA2.** AES-CCMP gives encryption and integrity; a four-way handshake derives session keys from the passphrase. Secure with a long passphrase, but a captured handshake allows offline guessing.
3. **WPA3.** The simultaneous authentication of equals (SAE) handshake blocks offline guessing and gives forward secrecy; open networks can use opportunistic encryption.
4. **Enterprise mode.** 802.1X with a RADIUS server gives each user their own credentials.
5. **Advice.** Use WPA3 or WPA2 with a long random passphrase and change the router's default password.

| Feature | WEP | WPA2 | WPA3 |
|---|---|---|---|
| Cipher | RC4 | AES-CCMP | AES-GCMP or CCMP |
| Key handshake | None (static key) | PSK four-way | SAE |
| Offline guessing | Easy | Possible | Resisted |
| Status | Broken | Acceptable | Recommended |

**Q4 (10 marks). Design the network security of a college. Explain the use of firewalls, DMZ, IDS/IPS, VPN, wireless security and key management.**

*Introduction.* A college holds student records, exam results and fee data, and also provides open services such as a website and Wi-Fi. Good security uses **defence in depth**: several independent layers, so that the failure of one does not expose everything (section 7.7, Figures 7.1 to 7.6).

1. **Network zones.** Place the web and mail servers in a DMZ between two firewalls, keep the student-records database and staff PCs in an internal network, and give students and guests a separate Wi-Fi network without access to staff systems.
2. **Firewalls.** The outer firewall allows only HTTPS to the web server and mail to the mail server; the inner firewall lets only the web server reach the database on one port. The default rule is deny.
3. **IDS and IPS.** Sensors on the DMZ and the internal links alert on scans, repeated failed logins and malware traffic. An IPS blocks well-known attacks automatically; alerts are tuned to a low false-alarm rate because of the base-rate effect.
4. **VPN and remote access.** Staff who work from home or from a branch use a VPN (IPsec or TLS) with multi-factor authentication. Administrators log in to servers only by SSH with keys.
5. **Wireless security.** Use WPA3 or WPA2-Enterprise with 802.1X so that each user has their own login, not a shared passphrase. Disable WPS and rogue access points are searched for regularly.
6. **Cryptography and keys.** The website uses TLS 1.3 with a certificate from a trusted authority. Disks of servers and laptops are encrypted, keys are rotated and stored in a key store or HSM, and keys of departing staff are revoked.
7. **People and process.** Patch regularly, back up offline, train staff against phishing, keep logs and have a written incident plan.

| Layer | Control | Threat addressed |
|---|---|---|
| Perimeter | Firewalls, DMZ | Unwanted inbound traffic |
| Detection | IDS/IPS, logs | Intruders already inside |
| Remote access | VPN, SSH keys, MFA | Eavesdropping, stolen passwords |
| Wireless | WPA3, 802.1X | Radio eavesdropping |
| Data | TLS, disk encryption, HSM | Theft and tampering |
| Recovery | Offline backup | Ransomware, failure |

*Conclusion.* No single device makes a network secure. A layered design with default-deny rules, monitoring, strong cryptography, careful key management and trained people limits the harm of every failure, and the whole design must be reviewed and tested regularly.
