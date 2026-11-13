---
subject: Cyber Security and Ethical Hacking
grade: BCA Semester 7
unit: 8
title: Ethical Hacking Methodology, Attack Categories and Their Defences
hours: 8
area: BCA 401 · Cyber Security and Ethical Hacking · Unit 8
---

Units 1 to 7 built the defender's toolkit: the triad, threat models, authentication, secure code, network architecture, detection and audit. This unit turns around and asks the question every ethical-hacking course asks: **what does an attacker actually do, step by step, and what does each step look like from the defender's side?** A tester who cannot describe the attack cannot write the rules of engagement for it, and an administrator who cannot recognise it cannot detect it.

The unit follows the usual ethical-hacking syllabus order: hats and phases, footprinting, scanning and enumeration, system hacking, malware, sniffing and session hijacking, social engineering, denial of service, web and application attacks, wireless, mobile, IoT and cloud, evasion, and cryptographic attacks. As in the rest of this book, every attack is described by **what it is, why it works, how to detect it and how to prevent it**. There are no exploit strings, payloads or step-by-step attack commands: the exam asks for concepts and countermeasures, and a professional learns the hands-on part inside an authorised lab.

::: key What this unit gives you
- The types of hackers, the five classic phases of an attack and how they map to the Cyber Kill Chain and MITRE ATT&CK.
- Footprinting, scanning and enumeration: what information leaks, which scan types exist and how scans are detected.
- System hacking and password attacks, with the arithmetic that separates a safe password from a weak one.
- Malware families, a worm-spread model, sniffing, spoofing, session hijacking, social engineering and denial of service, each with countermeasures.
- Web, wireless, mobile, IoT and cloud attack surfaces, evasion and honeypots, cryptographic attacks, and model answers.
:::

## 8.1 Hackers, hats and the phases of an attack

The word *hacker* originally meant a skilled programmer who enjoys understanding systems deeply. In security it now covers very different people, usually named by hat colour.

| Type | Motivation | Authorised? | Example |
|---|---|---|---|
| **White hat** (ethical hacker) | Improve security, earn a fee | Yes, written permission | Penetration tester hired by a bank |
| **Black hat** (cracker) | Money, revenge, disruption | No | Ransomware gang, fraudster |
| **Grey hat** | Curiosity or reputation; may disclose afterwards | No, but no malicious intent | Researcher who probes a site uninvited and reports the flaw |
| **Script kiddie** | Fun, status | No | Runs downloaded tools without understanding them |
| **Hacktivist** | Political or social cause | No | Defaces a website to protest |
| **State-sponsored actor** (APT) | Espionage, sabotage | Backed by a government | Long-running intrusion into a ministry |
| **Insider** | Grievance, money, carelessness | Has legitimate access | Employee who copies customer data |
| **Red / blue / purple team** | Attack simulation / defence / both together | Yes | Internal exercise (Unit 7) |

**Ethical hacking** is the authorised use of attacker techniques to find weaknesses before criminals do. Its defining marks are written permission, a defined scope, honest reporting and no damage. A grey-hat probe, however well meant, is still access without authority under Section 45 of the Electronic Transactions Act (Unit 7).

### The five classic phases

Most textbooks describe an attack as five phases. Defenders use the same list to decide where each control belongs.

1. **Reconnaissance (footprinting).** Collecting information about the target without, or with very little, touching it: domain names, staff, technology, addresses. *Passive* reconnaissance uses public sources; *active* reconnaissance interacts with the target.
2. **Scanning and enumeration.** Actively probing to learn which hosts are alive, which ports are open, which software versions run and which accounts or shares exist.
3. **Gaining access.** Exploiting a weakness (software flaw, weak password, misconfiguration, a person) to obtain a foothold, then escalating privileges.
4. **Maintaining access.** Installing a way back in (backdoor, new account, scheduled task) so that access survives a reboot or a password change.
5. **Covering tracks.** Deleting or altering logs and files to delay detection and hide the source.

An ethical hacker follows the same phases but adds a sixth step that criminals skip: **reporting and retest**, in which findings are documented with evidence and the fixes are verified.

### Kill chain and ATT&CK

Two models describe the same behaviour in more detail, and examiners like to see them named.

- The **Cyber Kill Chain** (Lockheed Martin) has seven stages: reconnaissance, weaponisation, delivery, exploitation, installation, command and control, and actions on objectives. The idea is that *breaking any one link stops the intrusion*, so defences are placed at several links.
- **MITRE ATT&CK** is a public knowledge base of attacker *tactics* (the goal, such as Initial Access, Persistence, Privilege Escalation, Defense Evasion, Exfiltration) and *techniques* (the method, each with an ID and detection advice). It is used to check detection coverage: "which techniques could we see today?"

| Classic phase | Kill-chain stage(s) | Typical defender control |
|---|---|---|
| Reconnaissance | Reconnaissance | Reduce public information; monitor for scraping |
| Scanning | Weaponisation, delivery | Firewall rules, IDS scan alerts, closed unused ports |
| Gaining access | Exploitation | Patching, hardening, MFA, input validation |
| Maintaining access | Installation, command and control | Endpoint detection, egress filtering, account review |
| Covering tracks | Actions on objectives | Central, write-once logging; file integrity monitoring |

::: note
The defender's advantage is that an attacker must succeed at every phase, while the defender needs to detect or stop only one. This is **defence in depth** from Unit 1 seen as a timeline.
:::

## 8.2 Footprinting and reconnaissance

**Footprinting** builds a profile of the target organisation's *footprint*: everything about it that is visible from outside. Good footprinting is quiet and takes most of the time of a real test, because the more that is known, the fewer risky probes are needed later.

| Source | What can be learned | Example in practice |
|---|---|---|
| Search engines | Indexed documents, login pages, error messages, exposed directories | A staff list PDF or a forgotten test page that is still indexed |
| **WHOIS** records | Registrar, registration dates, name servers, sometimes contact details | Which provider hosts the college website and who administers it |
| **DNS** records | Hostnames, mail servers (MX), text records (SPF), sub-domains | `mail`, `vpn` and `dev` sub-domains reveal services |
| Websites and metadata | Technology and framework, comments in pages, author names in document properties | A footer that says which CMS and version runs |
| **Social networks** and job adverts | Names, roles, technology stack, office photographs, badges | An advert asking for "Oracle 11g and Cisco ASA experience" reveals what is deployed |
| Archives and code hosting | Old versions of pages, accidentally committed keys and passwords | A public repository with a configuration file containing a secret |
| Internet-wide search engines (such as Shodan and Censys) | Devices with open services, banners, default pages | A forgotten camera or database exposed to the Internet |
| Email headers | Internal mail server names, IP addresses, mail software | Replies from the target show the path inside the network |
| **Physical** and **social** footprinting | Badge design, visitors' procedure, dumpsters, shoulder surfing | Paper with passwords in the bin |

### Passive and active

- **Passive** footprinting never sends traffic to the target's own systems; it uses third-party sources, so the target cannot see it. It is legal in most settings but may still raise privacy and ethics questions when it collects personal data.
- **Active** footprinting touches the target (for example, querying its name servers directly, or visiting its site and mapping it). It leaves traces in logs and needs authorisation.

### Defending against footprinting

You cannot remove everything, but you can **reduce and control the footprint**.

1. Publish only what is needed; remove metadata from documents (author, software, internal paths) before release.
2. Use generic role mailboxes rather than named staff lists on public pages; train staff about what they post.
3. Hide version banners and default pages on public servers; remove forgotten test sites and sub-domains.
4. Review public code repositories and cloud storage for secrets; rotate any secret that was ever exposed.
5. Use privacy services for WHOIS where policy permits, and keep DNS free of internal names (split DNS).
6. Monitor your own footprint regularly: search for your domain, your staff and your exposed services before an attacker does. This is *the same recon, done by the owner*.

::: example Worked example: what a job advert reveals
A Kathmandu company advertises for "a network engineer with experience of Fortinet firewalls, Windows Server 2012 and an old ERP". From one sentence an attacker learns the firewall brand, an operating system that is out of vendor support and a legacy application likely to be unpatched. No packet was sent. The defender's lesson is to avoid listing exact versions of weak systems in public adverts, and to plan to retire unsupported software. This is a reasoning exercise; it is not a statement about any real organisation.
:::

## 8.3 Scanning and enumeration

Footprinting says *who* the target is; scanning says *what is running and where*. Scanning has three layers:

- **Host discovery** finds which addresses answer (ping sweeps, ARP requests on the local network, probes to common ports).
- **Port scanning** finds which TCP and UDP ports accept connections on each live host.
- **Service and OS detection** identifies the software and version behind each open port (from banners and from the way the TCP/IP stack replies) and guesses the operating system.

A port is reported in one of three states: **open** (a service accepts the connection), **closed** (the host answers, but nothing listens) and **filtered** (a firewall drops the probe, so there is no answer at all). The handshake arithmetic of Unit 2 is the basis of every scan type.

| Scan type | What the scanner sends | Reply if open | Reply if closed | Remark |
|---|---|---|---|---|
| TCP connect | Complete three-way handshake | SYN/ACK, scanner finishes handshake | RST | Simple and reliable; the service logs the connection |
| TCP SYN ("half-open") | SYN only, then reset before completing | SYN/ACK | RST | Faster and less likely to be logged by the application; IDS still sees it |
| FIN, NULL and Xmas | A segment with FIN, no flags, or FIN+PSH+URG | no reply | RST | Illegal or odd flag mixes (Unit 2, section 2.4); works against some stacks only |
| ACK | Bare ACK | RST either way | RST either way | Maps firewall rules: tells filtered from unfiltered, not open from closed |
| UDP | An empty or protocol-specific datagram | Often silence or a service reply | ICMP port unreachable | Slow, because silence is ambiguous and ICMP is rate-limited |
| Idle (zombie) | Spoofed packets relayed through a third host | Inferred from the third host's IP ID counter | Inferred | Hides the scanner's address; rarely needed in an exam answer beyond the idea |

Tools such as **Nmap** automate all of this, and **vulnerability scanners** (Nessus, OpenVAS and similar) go further by checking each service version against a database of known flaws. A scan result is a *list of candidates*, not proof: false positives are common, so findings are validated manually.

### Enumeration

**Enumeration** is extracting detailed information from a service that is *already known to be open*: user names, group names, shares, network resources, machine names, routing tables and application banners. It is the step in which scanning turns into an inventory of accounts and resources.

| Service or protocol | What may be revealed | Typical weakness | Countermeasure |
|---|---|---|---|
| NetBIOS/SMB (ports 137-139, 445) | User names, shares, domain information | Anonymous or null sessions allowed | Disable null sessions; block SMB at the perimeter |
| SNMP (UDP 161) | Device lists, interfaces, routing and ARP tables | Default community strings such as "public" | Use SNMPv3 with authentication; change defaults; restrict by address |
| LDAP (389/636) | Directory objects, users, groups | Anonymous bind | Require authentication; use LDAPS; limit readable attributes |
| SMTP (25) | Valid mailbox names (through verification commands) | VRFY and EXPN enabled | Disable these commands; rate-limit |
| DNS (53) | Complete zone contents (a *zone transfer*) | Transfers allowed to anyone | Restrict transfers to named secondary servers |
| NTP, RPC, NFS, FTP/TFTP | Server lists, exported file systems, anonymous files | Open or unauthenticated services | Disable what is not needed; authenticate; firewall |

### Detecting and preventing scans

A scan is **noisy by nature**: one source touches many ports or hosts in a short time. That is also how it is detected. The rule in Python below works on a log of (source, destination port) events and flags any source that touches at least 10 distinct ports within a 60-second window. The log is synthetic and every number can be checked by hand.

```python
events = []  # (time in seconds, source, destination port)
# 10.0.0.5 probes ports 20..34 in quick succession (a scan)
for i, port in enumerate(range(20, 35)):
    events.append((i * 2, "10.0.0.5", port))
# 10.0.0.9 is a normal client making repeated requests to 80 and 443
for t in range(0, 120, 10):
    events.append((t, "10.0.0.9", 443 if t % 20 else 80))
events.sort()

WINDOW, LIMIT = 60, 10
alerts = {}
for t, src, port in events:
    seen = {p for (t2, s2, p) in events if s2 == src and t - WINDOW < t2 <= t}
    if len(seen) >= LIMIT and src not in alerts:
        alerts[src] = t
for src in sorted({e[1] for e in events}):
    n = len({e[2] for e in events if e[1] == src})
    print(f"{src}: {n} distinct ports, alert at t={alerts.get(src, 'never')}")
```
```output
10.0.0.5: 15 distinct ports, alert at t=18
10.0.0.9: 2 distinct ports, alert at t=never
```

The scanner is flagged on its 10th distinct port (port 29, at t = 18 s), long before it finishes; the ordinary client touches only 2 ports and is never flagged. Real sensors apply exactly this thresholding idea at scale, with adaptive limits so that a busy proxy or a load balancer, which legitimately contacts many destinations, does not cause alert fatigue (Unit 6).

**Countermeasures against scanning:**

1. Close every port and disable every service that is not needed; the attack surface is the number of listening services.
2. Default-deny at the firewall, allowing only documented flows; filter inbound ICMP types that are not required.
3. Use IDS and firewall rules that alert on scan-like behaviour and temporarily block the source.
4. Remove or alter informative banners; keep systems patched so that a version number is not a roadmap.
5. Scan *yourself* regularly and compare against the asset inventory: an unknown open port is a finding.

## 8.4 System hacking and password attacks

After scanning, the attacker looks for a way in. The classic *system hacking* goals are: **gain access**, **escalate privileges**, **maintain access** and **hide the evidence**.

### Gaining access: password attacks

Passwords remain the commonest weakness. Attack types differ in *where* the guessing happens:

| Attack | Idea | Why it works | Defence |
|---|---|---|---|
| **Online guessing / brute force** | Try many passwords against the live login | Weak or default passwords | Lockout or throttling, MFA, CAPTCHA, monitoring |
| **Dictionary** | Try likely words, names, leaked passwords | People choose predictable passwords | Reject common and breached passwords; length |
| **Password spraying** | Try *one* common password across *many* accounts | Stays under per-account lockout | Alert on one source failing across many accounts; MFA |
| **Credential stuffing** | Replay user/password pairs leaked from another site | People reuse passwords | Unique passwords, MFA, breached-password checks |
| **Offline cracking** | Guess against a stolen password-hash file at full speed | Fast unsalted hashes | Slow salted hashes (Unit 3), strong passphrases |
| **Rainbow tables** | Look hashes up in precomputed tables | Unsalted hashes | Per-user random salt |
| **Phishing and keylogging** | Capture the password directly | Humans and malware | Training, FIDO2 keys, endpoint protection |
| **Sniffing and relay** | Capture or relay authentication traffic | Cleartext or weak protocols | Encrypted protocols, SMB signing |

The decisive quantity is **how many guesses per second the attacker can make**, which depends on *where* the guessing is done. Compare an 8-character password drawn from 36 symbols (lowercase letters and digits) under three conditions.

```python
space = 36 ** 8
cases = [("online, 10 guesses/s (lockout and network)", 10),
         ("offline, fast hash, 1e10 guesses/s", 1e10),
         ("offline, bcrypt-class hash, 1e4 guesses/s", 1e4)]
print(f"keyspace = 36^8 = {space:,}")
for name, rate in cases:
    seconds = space / rate
    if seconds < 3600:
        text = f"{seconds:,.0f} seconds"
    elif seconds < 86400 * 365:
        text = f"{seconds / 86400:,.0f} days"
    else:
        text = f"{seconds / (86400 * 365):,.0f} years"
    print(f"{name}: {text} to exhaust the keyspace")
```
```output
keyspace = 36^8 = 2,821,109,907,456
online, 10 guesses/s (lockout and network): 8,946 years to exhaust the keyspace
offline, fast hash, 1e10 guesses/s: 282 seconds to exhaust the keyspace
offline, bcrypt-class hash, 1e4 guesses/s: 9 years to exhaust the keyspace
```

The same password falls from impossible to a few minutes depending only on *how it is stored and where it can be attacked*. This is why Unit 3 insists on salted, slow hashes and why online throttling matters: the defender controls the denominator.

### Privilege escalation and maintaining access

- **Vertical escalation** moves from an ordinary user to administrator or root (through unpatched software, weak service permissions, stored credentials or misconfigured *sudo* rules). **Horizontal escalation** moves to another user at the same level to reach their data.
- **Persistence** mechanisms include new accounts, startup entries, scheduled tasks, services, modified authorised keys and **backdoors**. A **rootkit** hides these by modifying the operating system or firmware so that tools no longer show them. A **keylogger** records keystrokes; **spyware** collects data silently.
- **Steganography** hides data inside harmless files such as images; it is used for data exfiltration and, rarely, for command channels.

### Covering tracks

Attackers clear or edit event logs, disable auditing, change file timestamps and hide in "normal" tools (*living off the land*). Their success shows why **logs must leave the host immediately** to a central, write-once store, and why Unit 7's audit trail is a security control, not a convenience.

**Countermeasures for system hacking:** patch promptly; enforce least privilege and review administrator accounts; require MFA for all remote and privileged access; use long unique passphrases with a password manager; hash with a slow salted function; alert on repeated failures and on new accounts, services and scheduled tasks; use file integrity monitoring and endpoint detection; and ship logs to a protected collector.

## 8.5 Malware threats

**Malware** (malicious software) is any program designed to harm, spy on or take control of a system. It is classified by *how it spreads* and *what it does*; many real samples combine several roles.

| Type | How it spreads | Needs a host file or user action? | Typical effect |
|---|---|---|---|
| **Virus** | Attaches to a program or document; runs when that file is run | Yes, a host and user action | Corrupts files, spreads to other files |
| **Worm** | Copies itself over the network by exploiting flaws or weak passwords | No, self-propagating | Floods networks, installs payloads |
| **Trojan horse** | Disguised as useful software (a "free" tool, a cracked game) | Yes, the user installs it | Backdoor, data theft, downloader |
| **Ransomware** | Phishing, exposed remote services, trojans | Often | Encrypts files, demands payment, often steals data first |
| **Spyware / keylogger / infostealer** | Bundled or dropped by a trojan | Yes | Captures keys, browser passwords, screenshots |
| **Rootkit** | Installed after privilege escalation | Needs admin rights | Hides processes, files and connections |
| **Botnet agent (bot)** | Worm or trojan | Often | Remote control for DoS, spam and fraud |
| **Logic bomb** | Planted by an insider | Condition-triggered | Deletes or corrupts data on a date or event |
| **Fileless malware** | Scripts and system tools in memory | Often | Leaves little on disk, evades signature scanners |
| **Adware / cryptojacker** | Bundled software, malicious web scripts | Often | Ads, stolen CPU time |

### Phases of a virus

A classical virus passes through four phases: **dormant** (waiting for a trigger such as a date), **propagation** (copying itself to other programs or files), **triggering** (the condition is met) and **execution** (the payload runs). Viruses are also classified by technique: *boot-sector*, *file-infecting*, *macro*, *polymorphic* (changes its code each copy to avoid signatures), *metamorphic* (rewrites itself fully), *stealth* (hides changes) and *multipartite*.

### How a worm spreads: a growth model

A worm has no "host file" to wait for, so it spreads like an epidemic: each infected machine probes others, and a fraction of the probes hit vulnerable hosts. The **susceptible-infected (SI) model** captures the idea. With N vulnerable hosts, I currently infected and a contact rate β per step, the next step adds about β × I × (N − I) / N new infections. Early on, growth is exponential; later, it slows because few susceptible hosts remain, giving an S-shaped curve.

```python
N, beta = 10_000, 0.8
I = 1.0
step = 0
milestones = {}
while I < 0.99 * N:
    step += 1
    I = I + beta * I * (N - I) / N
    for frac in (0.01, 0.5, 0.9, 0.99):
        if frac not in milestones and I >= frac * N:
            milestones[frac] = step
for frac, s in milestones.items():
    print(f"{frac * 100:.0f}% infected at step {s}")
```
```output
1% infected at step 8
50% infected at step 16
90% infected at step 18
99% infected at step 20
```

With only one initial infection, the model reaches 1% of 10,000 hosts at step 8, half of them at step 16 and 99% at step 20: twelve further steps take it from 1% to 99%. This is the arithmetic of *why patching windows matter*: once growth is exponential, there is no time to react by hand, so containment must be automatic (network segmentation, egress filtering, rapid patching, endpoint isolation).

**Countermeasures against malware:**

1. Keep operating systems and applications patched; remove unsupported software.
2. Use endpoint protection that combines signatures, behaviour analysis and application allow-listing.
3. Filter email attachments and links; disable macros from the Internet by default; train users.
4. Segment the network and restrict lateral movement (a worm cannot cross a firewall that blocks SMB between departments).
5. Keep **offline, tested backups** (the only reliable ransomware recovery); practise restoring them.
6. Restrict administrator rights; users who cannot install software cannot install a trojan by accident.
7. Analyse suspicious files in an isolated **sandbox**; static analysis reads the file, dynamic analysis watches it run.

## 8.6 Sniffing, spoofing and session hijacking

### Sniffing

**Sniffing** is capturing network traffic with a **packet analyser** (Wireshark, tcpdump). It is also a normal troubleshooting skill; it becomes an attack when the traffic carries cleartext secrets. On a hub or an open Wi-Fi network every station sees every frame. On a **switch** a host normally sees only its own traffic, so an attacker has to bend the network to see more:

| Technique | What the attacker abuses | Effect | Defence |
|---|---|---|---|
| **MAC flooding** | The switch's limited MAC address (CAM) table | A full table makes the switch broadcast frames like a hub | **Port security**: limit MAC addresses per port |
| **DHCP starvation / rogue DHCP** | The DHCP pool, and trust in the first offer | Clients get the attacker's gateway and DNS | **DHCP snooping**: only trusted ports may send offers |
| **ARP spoofing (poisoning)** | ARP has no authentication | Victims map the gateway's IP to the attacker's MAC: a man-in-the-middle position | **Dynamic ARP Inspection**, static entries for gateways, encrypted protocols |
| **DNS poisoning** | A resolver accepting forged answers | Names resolve to the attacker's address | **DNSSEC** (Unit 5), randomised source ports, trusted resolvers |
| **MAC and IP spoofing** | Trust placed in addresses | Impersonate another device, bypass address filters | Ingress filtering, 802.1X, authentication above the address layer |
| **Mirror (SPAN) port abuse** | Misconfigured monitoring | Copy of other ports' traffic | Restrict management access |

Cleartext protocols are the real problem: **Telnet, FTP, HTTP, POP3, IMAP and SNMPv1/v2** send passwords unprotected. The fix is not to hide from sniffers but to make sniffing *useless*: SSH instead of Telnet, SFTP or FTPS instead of FTP, HTTPS everywhere (with HSTS), secure mail protocols, VPNs on untrusted networks. **Detection** includes watching for duplicate or flapping ARP mappings, network interface cards in promiscuous mode and sudden bursts of ARP traffic.

### Session hijacking

After a user logs in, the server issues a **session token** (a cookie or a header value) so that the user need not authenticate on every request. **Session hijacking** steals or forges that token and so *takes over an authenticated session without knowing the password*.

| Method | How the token is obtained | Defence |
|---|---|---|
| **Sniffing** | Read it from unencrypted traffic | HTTPS only; `Secure` cookie flag; HSTS |
| **Session fixation** | Make the victim use a token the attacker already knows | Issue a new token at login |
| **Predictable tokens** | Guess a sequential or weak token | Long random tokens from a cryptographic generator |
| **Cross-site scripting (XSS)** | A script in the page reads the cookie | Output encoding, CSP, `HttpOnly` cookie flag (Unit 4) |
| **Cross-site request forgery** | The browser sends the cookie for the attacker's request | `SameSite` cookies, anti-CSRF tokens (Unit 4) |
| **Man-in-the-middle** | The attacker relays traffic between client and server | TLS with certificate validation |
| **TCP/network-level hijack** | Predict sequence numbers and inject segments | Random initial sequence numbers (Unit 2), encrypted transport |

**Server-side controls** make a stolen token short-lived and less useful: absolute and idle time-outs, re-authentication before sensitive actions, binding to additional signals, and logging out on the server rather than only deleting the cookie in the browser.

## 8.7 Social engineering and insider threats

**Social engineering** manipulates *people* into giving up information or access. It succeeds because the human is the most flexible, and least patched, part of any system. Attackers rely on psychological levers such as **authority** ("I am from the head office"), **urgency** ("your account closes in an hour"), **reciprocity** and **liking**, **social proof** ("everybody has done this"), **scarcity** and **fear**.

| Technique | Channel | Example |
|---|---|---|
| **Phishing** | Email | A fake bank message asking to "verify your account" with a link to a copy of the real login page |
| **Spear phishing / whaling** | Targeted email | A message to the finance officer, using the real name of the principal, asking for an urgent transfer |
| **Vishing** | Phone call | A caller posing as bank support asks for the OTP |
| **Smishing** | SMS or chat | "You won a prize, click here" or a fake delivery notice |
| **Pretexting** | Any | An invented, believable story (IT helpdesk, auditor, new employee) to extract details |
| **Baiting** | Physical media or free offers | A USB drive labelled "Salary 2082" left in the car park |
| **Tailgating / piggybacking** | In person | Following an employee through a badge-controlled door |
| **Shoulder surfing, dumpster diving** | In person | Watching a PIN; collecting printed documents from the bin |
| **Business email compromise** | Email | A hijacked or look-alike mailbox changes bank details on a supplier invoice |
| **Impersonation on social networks** | Social media | A fake profile of a manager or recruiter used to gain trust |
| **Identity theft** | Any | Using a stolen citizenship number, photo and address to open accounts |

### Insider threats

An **insider** already has legitimate access. Three kinds are distinguished: the **malicious insider** (a disgruntled or bribed employee), the **negligent insider** (careless handling, weak passwords, lost laptop) and the **compromised insider** (an account taken over by an outsider). Controls include least privilege, separation of duties, user-activity monitoring, prompt de-provisioning when staff leave and a culture in which mistakes are reported without fear.

### Recognising and preventing social engineering

1. **Verify out of band.** Call the person back on a number you already know, not the one in the message.
2. **Slow down when pushed.** Urgency, secrecy and an appeal to authority together are the classic signature.
3. **Never share OTPs, PINs or passwords**, whoever asks; no real bank asks for them.
4. **Check the link before clicking**: hover to see the real address, look for look-alike spellings.
5. **Use MFA, preferably phishing-resistant keys** (FIDO2): a stolen password alone is then not enough.
6. **Run simulated phishing and short, regular training;** measure the click and the *report* rate; reward reporting.
7. **Control physical access:** badges, visitor logs, escorting, shredders, clean-desk rules.
8. **Define a payment-change procedure** that always needs a second person and a call to a known contact.

::: caution
Social engineering tests are the most legally and ethically sensitive part of a penetration test: they involve real people. The rules of engagement must state which staff, channels and pretexts are allowed, how any data entered into a fake page will be protected and destroyed, and that staff who fall for a test are never publicly blamed.
:::

## 8.8 Denial of service and botnets

A **denial-of-service (DoS)** attack tries to make a system unavailable to its users, attacking the **A** of the CIA triad. When the traffic comes from many machines it is a **distributed denial of service (DDoS)**. The machines are usually a **botnet**: thousands of infected computers, routers and cameras controlled through a **command-and-control (C2)** channel. A botnet can be rented, which is why DDoS no longer needs technical skill.

| Category | Target resource | Examples | Typical defence |
|---|---|---|---|
| **Volumetric** | Bandwidth | UDP floods, **amplification and reflection** (DNS, NTP, memcached) | Upstream scrubbing, CDN, anycast, provider blackholing |
| **Protocol (state exhaustion)** | Connection tables of servers and firewalls | **SYN flood**, fragmentation attacks, "ping of death" (old) | SYN cookies, tuned backlogs, rate limits, filtering |
| **Application layer** | CPU, memory, database | HTTP floods, "slow" attacks that hold connections open | Web application firewall, caching, rate limiting, CAPTCHA |
| **Single-source DoS** | Any | One host floods or crashes a service | Block the source; patch crash bugs |

### Reflection and amplification

In a **reflection** attack the attacker sends small requests with the *victim's address forged as the source* to many open servers; the servers send their (larger) replies to the victim. The **amplification factor** is response size divided by request size, so the attacker's own bandwidth is multiplied.

### SYN flood: how little it takes

The server keeps a **half-open connection** in a fixed-size backlog after each SYN until the handshake completes or times out (Unit 2). If the attacker never completes the handshake, the backlog fills and genuine clients are refused.

```python
# reflection and amplification: the attacker's bandwidth multiplied
for name, request, response in (("DNS (large record)", 60, 3000), ("NTP monlist-style", 234, 46800)):
    factor = response / request
    attacker_mbps = 100
    print(f"{name}: factor {factor:.0f}x; {attacker_mbps} Mbit/s becomes {attacker_mbps * factor / 1000:.1f} Gbit/s at the victim")

# SYN flood: rate needed to keep a backlog full
backlog, timeout_s, syn_bytes = 128, 60, 60
rate = backlog / timeout_s
print(f"backlog {backlog}, entry lifetime {timeout_s}s: {rate:.2f} SYN/s keeps it full")
print(f"that is about {rate * syn_bytes:.0f} bytes per second of attack traffic")
```
```output
DNS (large record): factor 50x; 100 Mbit/s becomes 5.0 Gbit/s at the victim
NTP monlist-style: factor 200x; 100 Mbit/s becomes 20.0 Gbit/s at the victim
backlog 128, entry lifetime 60s: 2.13 SYN/s keeps it full
that is about 128 bytes per second of attack traffic
```

A 100 Mbit/s attacker becomes a 5 Gbit/s attack with a 50x DNS amplifier, and an old NTP configuration with a 200x factor would turn it into 20 Gbit/s; a SYN flood needs only about two packets a second (roughly 128 bytes per second) to keep a 128-entry backlog full. The first case is a bandwidth problem, the second a *state* problem. The two are defended in different ways.

**Countermeasures against DoS and DDoS:**

1. **Close the reflectors:** disable open resolvers and legacy monitor commands; rate-limit responses; patch.
2. **Ingress and egress filtering** (BCP 38): drop packets whose source address cannot be valid on that link, so that spoofed requests never leave your network.
3. **SYN cookies** and a tuned backlog: the server encodes state in the sequence number, so a half-open entry costs nothing.
4. **Over-provision and distribute:** content delivery networks and anycast spread the load; a scrubbing provider filters attack traffic upstream.
5. **Rate limiting and caching** at the application layer (token bucket, Unit 5); serve static content from a cache.
6. **Plan:** have a DDoS runbook, upstream contacts and a degraded-mode page; test it in the rules of engagement of a stress test.
7. **Keep your own devices out of botnets:** change default credentials on routers and cameras, update firmware, and segment IoT devices.

## 8.9 Hacking web servers and web applications

A web server is exposed to the whole Internet by design, so it is the most attacked system an organisation owns. Attacks fall into two groups: those on the **server platform** (operating system, web server software, modules, default pages, directory listing, misconfigured permissions, unpatched components) and those on the **application** (the code the organisation wrote). Unit 4 covered how to build safely; here the attack categories are named so that you can recognise them in an exam and in a report.

The **OWASP Top 10** is the standard awareness list of the most critical web risks. The 2021 edition is:

| Rank | Category | One-line meaning | Main defence |
|---|---|---|---|
| A01 | **Broken access control** | Users can act outside their permissions (change an ID in the URL and see another user's record) | Deny by default; check authorisation on the server for every request |
| A02 | **Cryptographic failures** | Sensitive data unprotected in transit or at rest | TLS everywhere; strong, current algorithms; key management |
| A03 | **Injection** (SQL, OS command, LDAP, XSS) | Untrusted input is interpreted as code | Parameterised queries, input validation, output encoding |
| A04 | **Insecure design** | Missing threat modelling and security requirements | Threat model early (Unit 1); secure design patterns |
| A05 | **Security misconfiguration** | Defaults, open storage, verbose errors, unneeded features | Hardened baselines; automated configuration checks |
| A06 | **Vulnerable and outdated components** | Libraries and frameworks with known flaws | Inventory, software composition analysis, patching |
| A07 | **Identification and authentication failures** | Weak passwords, no MFA, exposed session IDs | MFA, secure session handling (section 8.6) |
| A08 | **Software and data integrity failures** | Untrusted updates, plugins or pipelines | Signed packages, protected build pipeline |
| A09 | **Security logging and monitoring failures** | Attacks go unseen | Central logs, alerting, retention (Unit 7) |
| A10 | **Server-side request forgery (SSRF)** | The server is tricked into requesting internal resources | Allow-list outgoing destinations; segment internal services |

### SQL injection, in concept

**SQL injection** occurs when an application builds a database command by *pasting user input into the text of the query*. The database cannot tell where the programmer's command ends and the user's data begins, so a crafted input can change the *meaning* of the command: reading other rows, bypassing a login check or modifying data. It is an **A03** problem and one of the oldest and most damaging.

The defence is structural, not a filter. **Parameterised queries (prepared statements)** send the command and the data separately: the database parses the command first, and the data is only ever treated as a value (Unit 4, section 4.3). Supporting controls: validate type, length and format; give the application database account only the privileges it needs (no administrative rights); hide detailed database errors from users; and use a web application firewall as an extra, never the only, layer. **Cross-site scripting (XSS)** is the same pattern on the output side: user data placed in a page without encoding is run by the browser as script, and the defence is **output encoding** plus a Content Security Policy.

### Web server hardening checklist

1. Patch the operating system, web server and every component; remove sample files and default accounts.
2. Disable directory listing and unneeded modules; run the service as a low-privilege user.
3. Serve HTTPS only with a current TLS configuration; redirect HTTP; set HSTS.
4. Return generic error pages; keep stack traces and version banners out of responses.
5. Add security headers (CSP, `X-Content-Type-Options`, `Referrer-Policy`, frame protections).
6. Put a web application firewall and rate limiting in front; log requests centrally.
7. Test regularly with an authorised scanner and a manual review, and retest after each release.

## 8.10 Wireless, mobile, IoT and cloud attack surfaces

### Wireless networks

Radio travels through walls, so anyone nearby can listen or join in. Unit 5 explained WPA2 and WPA3; the attack categories are summarised here.

| Attack | Idea | Defence |
|---|---|---|
| **WEP cracking** | WEP's short IVs and RC4 weaknesses allow key recovery in minutes | Never use WEP; use WPA2-AES or WPA3 |
| **Weak WPA2-PSK passphrase** | A captured four-way handshake can be guessed offline | Long random passphrase; WPA3-SAE; WPA2/3-Enterprise (802.1X) |
| **Rogue access point and evil twin** | A fake AP with the same name lures clients | 802.1X with certificate checking; wireless intrusion detection; VPN on public Wi-Fi |
| **Deauthentication attack** | Management frames are unauthenticated; the attacker disconnects clients | Protected management frames (802.11w, mandatory in WPA3) |
| **WPS PIN attack** | The eight-digit PIN is checked in two halves (about 11,000 guesses) | Disable WPS |
| **Bluetooth attacks** | Bluejacking, bluesnarfing, weak pairing | Turn off when unused; non-discoverable mode; update firmware |

### Mobile platforms

Smartphones combine personal data, banking apps and always-on connectivity. Typical vectors: **malicious or repackaged apps** from unofficial stores, **excessive permissions**, **smishing** and phishing links, **unpatched OS versions**, **rooted or jail-broken devices** that bypass the sandbox, **insecure Wi-Fi**, **SIM swapping** and **stalkerware**. Defences: install only from official stores, review permissions, keep the OS updated, use a screen lock and device encryption, enable remote wipe, avoid rooting, and use **mobile device management (MDM)** and a "bring your own device" policy in organisations. Developers add certificate pinning, secure storage and obfuscation (see BCA 352).

### Internet of Things and operational technology

IoT devices (cameras, smart meters, routers, door locks) are attractive because they are numerous, always on, rarely updated and often shipped with **default credentials**. The Mirai botnet (2016) grew by logging in to cameras and routers with a short list of factory passwords and then launched record-size DDoS attacks. Operational technology (industrial control systems) adds safety consequences: an attack can stop a plant. Defences: change defaults, update firmware, segment IoT on a separate VLAN with no route to business systems, disable unused services and require vendors to support security patches for the device lifetime.

### Cloud computing

Moving to the cloud moves *some* responsibility to the provider, but not all of it. Under the **shared responsibility model** the provider secures the physical data centre and the virtualisation layer; the customer secures identities, data, configuration and, depending on the model (IaaS, PaaS, SaaS), the operating system and applications (see BCA 451).

| Threat | Example | Control |
|---|---|---|
| **Misconfiguration** | A storage bucket left public | Policy-as-code, configuration scanners, block public access by default |
| **Weak identity control** | A leaked access key with administrator rights; no MFA | Least privilege, MFA, short-lived credentials, key rotation |
| **Insecure interfaces and APIs** | Unauthenticated management API | Authentication, rate limits, API gateway |
| **Data breach and insider** | Over-broad access to customer data | Encryption with customer-managed keys, access logging |
| **Account hijacking** | Phished console credentials | MFA, conditional access, monitoring |
| **Denial of service and cost abuse** | A flood causing very large bills | Autoscaling limits, budget alerts |

Cloud penetration testing needs *the provider's policy* as well as the customer's authorisation: most providers publish what testing is allowed without prior approval, and testing outside it is a breach of terms.

## 8.11 Evading detection: IDS, firewalls and honeypots

Security tools are themselves tested by attackers. Knowing the **evasion categories** helps a defender to tune the tools and a tester to measure them.

| Evasion idea | What it exploits | Defender's answer |
|---|---|---|
| **Fragmentation** | A device inspects packets individually while the destination reassembles them | Reassemble before inspecting; drop odd fragments |
| **Encryption and tunnelling** | The sensor cannot read encrypted payloads; traffic hidden inside DNS or HTTPS | TLS inspection where policy allows; DNS monitoring; behavioural detection |
| **Obfuscation and polymorphism** | Signatures match exact bytes | Behaviour-based and anomaly detection, sandboxing |
| **Low and slow** | Thresholds (like the scan detector of section 8.3) | Longer windows, per-source baselines |
| **Source spoofing or proxying** | Block lists keyed to addresses | Detect by behaviour and identity, not address alone |
| **Allowed-port abuse** | Firewalls allow 80 and 443 | Application-aware (next-generation) firewalls and proxy authentication |

**Firewalls** filter by address, port and state (packet filter and stateful) or by application (proxy, next-generation). **Intrusion detection systems** (IDS) alert; **intrusion prevention systems** (IPS) can also block. They use **signature-based** detection (matching known patterns, accurate for known attacks, blind to new ones) and **anomaly-based** detection (deviation from a learned baseline, able to catch new attacks, but with more false positives). Unit 6 gave the confusion-matrix and base-rate arithmetic that explains why alert quality matters.

A **honeypot** is a deliberately attractive decoy system with no legitimate users: any contact is suspicious by definition. *Low-interaction* honeypots emulate a few services cheaply; *high-interaction* ones are real systems and capture richer behaviour but must be strictly isolated; a **honeynet** is a network of them, and a **honeytoken** is a fake record or credential that raises an alarm when used. Honeypots give early warning and let researchers study attacker methods; their risk is that a poorly isolated one becomes a stepping stone, and there can be legal questions about *entrapment* and the data collected.

## 8.12 Cryptographic attacks

Cryptography (BCA 353) is only as strong as its *use*. Attackers rarely break the mathematics; they attack keys, implementations and people.

| Attack | What the attacker has or does | Defence |
|---|---|---|
| **Brute force** | Tries every key | Sufficient key length (128-bit or more for symmetric keys) |
| **Ciphertext-only, known-plaintext, chosen-plaintext** | Ciphertext only; pairs of plaintext and ciphertext; or can encrypt chosen text | Modern ciphers designed to resist all three |
| **Frequency analysis** | Letter statistics break classical substitution ciphers | Do not use classical ciphers for real data |
| **Birthday attack** | Finds two inputs with the same hash after about 2^(n/2) tries | Hashes of 256 bits or more (SHA-256 gives 2^128 work) |
| **Man-in-the-middle** | Sits between two parties during key exchange | Authenticated key exchange, certificates, PKI |
| **Side-channel** | Measures timing, power or cache behaviour | Constant-time code, hardware countermeasures |
| **Downgrade** | Forces use of an older, weaker protocol version | Disable old protocols; TLS fallback protection |
| **Key theft and weak randomness** | Steals or predicts the key | Hardware security modules, key rotation, cryptographic random number generators |
| **Padding-oracle and other implementation flaws** | Uses error messages to decrypt gradually | Use authenticated encryption (such as AES-GCM) from a vetted library |

The birthday bound shows concretely why hash length matters:

```python
import math
rate = 1e12  # hashes per second, a very large attacker
for name, bits in (("MD5", 128), ("SHA-1", 160), ("SHA-256", 256)):
    work = 2 ** (bits // 2)
    years = work / rate / (86400 * 365)
    print(f"{name}: {bits}-bit output, birthday work 2^{bits // 2} = {work:.2e}, about {years:.2e} years at 1e12 hashes/s")
```
```output
MD5: 128-bit output, birthday work 2^64 = 1.84e+19, about 5.85e-01 years at 1e12 hashes/s
SHA-1: 160-bit output, birthday work 2^80 = 1.21e+24, about 3.83e+04 years at 1e12 hashes/s
SHA-256: 256-bit output, birthday work 2^128 = 3.40e+38, about 1.08e+19 years at 1e12 hashes/s
```

For MD5 the bound is under a year for a very large attacker, and real attacks on its structure are far faster; practical collisions in MD5 and SHA-1 have been *demonstrated*, which is why certificates and signatures no longer use them. SHA-256's birthday work of 2^128 is far outside any attacker's reach. The lesson: **use standard, current algorithms and protocols, never invent your own, and protect the keys**.

**Public key infrastructure (PKI)** binds public keys to identities with certificates signed by certificate authorities. Its attack surface is trust: a compromised or careless certificate authority, an expired or revoked certificate that clients do not check, or a user who clicks through a browser warning. Defences are certificate validation, revocation checking (CRL, OCSP), certificate transparency logs and short certificate lifetimes. **Disk and email encryption** (full-disk encryption, S/MIME, PGP) protect data at rest and in mail, but only if the recovery keys and passphrases are themselves protected.

## 8.13 Seeing the ideas: the phases, amplification and worm growth

Three pictures summarise the unit. Figure 8.1 puts the five phases next to the defender's controls; Figure 8.2 compares attacker bandwidth with the traffic that arrives after amplification (section 8.8); Figure 8.3 plots the SI worm model of section 8.5.

```svgfig label="8.1" caption="The five phases of an attack and the defender's best control at each. The attacker must succeed at every phase; the defender needs to detect or stop only one. An ethical hacker adds a sixth step, reporting and retest."
f = Fig(580, 214)
st = [("1 Recon", "footprinting:\nWHOIS, DNS,\nsearch, social"), ("2 Scanning", "hosts, ports,\nservices,\nenumeration"), ("3 Gain access", "exploit, password,\nphishing,\nescalate"), ("4 Maintain", "backdoor,\nnew account,\nrootkit"), ("5 Cover tracks", "edit logs,\nhide files,\nclear history")]
ct = ["trim public\ninformation", "close ports,\nIDS alerts", "patch, MFA,\ntraining", "endpoint\ndetection", "central,\nwrite-once logs"]
for i, (t, s) in enumerate(st):
    x = 6 + i * 115
    f.box(x, 12, 108, 30, t, fill=BLUE, stroke=NAVY, bold=True, size=10.5)
    f.box(x, 48, 108, 56, s, fill=SAND, stroke=AMBER, size=9.5)
    f.box(x, 128, 108, 42, ct[i], fill=MINT, stroke=TEAL, size=9.5)
    if i < 4:
        f.arrow([(x + 108, 27), (x + 115, 27)])
f.text(290, 117, "defender's control at the same phase", size=9, color=TEAL, bold=True)
f.box(6, 178, 564, 30, "Ethical hacking: authorised, scoped, honest report, then 6 Retest after the fixes are made.", fill="#f8fafc", stroke=SLATE, size=10)
```

```svgfig label="8.2" caption="Amplification turns a small attacker into a large attack. A 100 Mbit/s attacker sends 0.1 Gbit/s directly; through a 50x DNS amplifier the victim receives 5 Gbit/s and through a 200x NTP-style amplifier 20 Gbit/s (section 8.8). The defence is to close the reflectors and filter spoofed sources."
f = Fig(580, 214)
rows = [("Direct", 0.1, SAND, AMBER), ("DNS 50x", 5.0, ROSE, RED), ("NTP 200x", 20.0, ROSE, RED)]
for i, (name, v, fl, st) in enumerate(rows):
    y = 18 + i * 42
    f.text(8, y + 15, name, size=10.5, color=NAVY, bold=True, anchor="start")
    f.box(96, y, max(v * 18, 3), 28, "", fill=fl, stroke=st)
    f.text(96 + max(v * 18, 3) + 6, y + 15, f"{v:g} Gbit/s", size=10.5, color=st, bold=True, anchor="start", vmid=True)
f.box(8, 140, 564, 66, "Factor = response size / request size. Attacker bandwidth is multiplied.\nThe replies are sent by innocent servers to a forged source address: the victim.\nFix: disable open resolvers, rate-limit responses, apply ingress filtering (BCP 38).", fill=BLUE, stroke=NAVY, size=10)
```

```svgfig label="8.3" caption="Worm growth in the SI model with N = 10,000 hosts, contact rate 0.8 per step and one initial infection (section 8.5). Growth is exponential at first (1% at step 8), then saturates (50% at step 16, 99% at step 20)."
f = Fig(580, 214)
ax = Axes(f, 56, 18, 480, 150, (0, 24), (0, 10000))
ax.grid(4, 2500)
ax.axes("step", "infected hosts")
N, beta = 10000, 0.8
vals = [1.0]
for _ in range(24):
    I = vals[-1]
    vals.append(I + beta * I * (N - I) / N)
ax.curve(lambda x: vals[int(round(x))], 0, 24, color=RED, n=24, label="infected", lx=ax.X(17.4), ly=ax.Y(4000))
ax.hline(5000, color=AMBER)
ax.pt(16, vals[16], "50% at step 16", dx=-120, dy=-6, anchor="start")
ax.pt(8, vals[8], "1% at step 8", dx=10, dy=-12)
f.text(290, 204, "Patch and isolate before the knee of the curve: after it there is no time left.", size=10, color=NAVY, bold=True)
```

### 8.13.1 Eight habits that defeat most attacks in this unit

1. **Know your own footprint.** Search for your organisation as an attacker would, and trim what is not needed (section 8.2).
2. **Keep an asset inventory and scan against it.** An unknown open port or host is a finding (section 8.3).
3. **Patch fast, starting with Internet-facing systems.** A worm leaves no time for a slow cycle (section 8.5).
4. **Use MFA and unique long passphrases.** Offline cracking and credential stuffing then lose most of their value (section 8.4).
5. **Encrypt in transit everywhere.** A sniffed or hijacked session is useless if the traffic and the cookie are protected (section 8.6).
6. **Train people and give them a way to report.** The report rate matters more than the click rate (section 8.7).
7. **Segment the network and filter egress.** Containment limits malware, botnets and data theft (sections 8.5 and 8.8).
8. **Log centrally and test your detection.** What you cannot see you cannot respond to; purple-team exercises prove it works (sections 8.3 and 8.11).

## 8.14 Summary and exercises

Attackers follow five phases (reconnaissance, scanning, gaining access, maintaining access, covering tracks), which map onto the Cyber Kill Chain and ATT&CK; the ethical hacker follows them with authority, scope and an honest report. Footprinting is reduced by controlling public information; scanning is noisy and detectable; password attacks depend on guess rate (online 10 per second against 10 billion per second offline); malware spreads like an epidemic, so containment must be automatic; sniffing, spoofing, session hijacking and social engineering attack the trust built into protocols and people; DoS is defeated by closing reflectors, filtering spoofed sources and absorbing load; web, wireless, mobile, IoT and cloud each have a standard list of weaknesses and a standard hardening answer; and cryptography fails mainly through bad keys and implementations. Every technique here is legal only inside written authorisation.

1. List the types of hackers and state which of them are ethical.
2. Describe the five phases of hacking and give one defender control for each.
3. Distinguish passive from active footprinting with three sources of information for each.
4. Compare TCP connect, SYN, FIN/Xmas, ACK and UDP scans, and explain how a port scan is detected.
5. What is enumeration? Name three services that may leak information and a countermeasure for each.
6. Differentiate online and offline password attacks. Compute the average time to find an 8-character password from 36 symbols at 10 guesses per second (use the keyspace in section 8.4).
7. Classify virus, worm, trojan, ransomware, rootkit and botnet. State the four phases of a virus.
8. With N = 10,000, contact rate 0.8 and one initial infection, how many steps does the SI model take to infect 99% of hosts? Why does this make manual response impractical?
9. Explain ARP spoofing and name two switch features that prevent it. Why does HTTPS limit the damage of sniffing?
10. List six social-engineering techniques and eight preventive measures.
11. Define DoS, DDoS and botnet. A 100 Mbit/s attacker uses a 50x amplifier: what bandwidth arrives at the victim? How long does a 128-entry backlog with a 60-second timeout stay full at what SYN rate?
12. Name the OWASP Top 10 (2021) categories and explain why parameterised queries prevent SQL injection.
13. Discuss the shared responsibility model and four cloud misconfigurations.
14. Define IDS, IPS, honeypot and honeytoken. Distinguish signature-based from anomaly-based detection.
15. Explain the birthday attack and why SHA-256 is considered safe while MD5 is not.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the phases of an ethical hacking engagement.**

*Introduction.* Ethical hacking is the authorised use of attacker techniques to find weaknesses before criminals do. It follows the same phases as an attack, with permission and a report (section 8.1, Figure 8.1).

| Phase | Purpose | Defender control |
|---|---|---|
| 1 Reconnaissance | Collect information about the target | Reduce public information |
| 2 Scanning and enumeration | Find live hosts, open ports, services, accounts | Close ports, IDS alerts |
| 3 Gaining access | Exploit a weakness and escalate privileges | Patch, MFA, training |
| 4 Maintaining access | Install a way back in | Endpoint detection, account review |
| 5 Covering tracks | Hide evidence | Central write-once logs |

*Sixth step.* An ethical hacker finishes with a **report** of findings and evidence and a **retest** after fixes. The tester works within a signed scope and rules of engagement (Unit 7).

*Conclusion.* The attacker must win every phase; the defender needs to stop only one, which is the reason for defence in depth.

**Q2 (5 marks). Classify malware and explain how worms spread. Use the SI model with N = 10,000, rate 0.8 and one initial infection.**

*Introduction.* Malware is software designed to harm, spy on or control a system, classified by spread and effect (section 8.5).

*Classification.* A **virus** attaches to a host file and needs user action; a **worm** spreads by itself over the network; a **trojan** is disguised as useful software; **ransomware** encrypts data for payment; a **rootkit** hides other malware; a **bot** joins a botnet.

*Worm growth.* In the SI model each step adds about 0.8 x I x (N - I) / N infections. Executing it gives 1% infected at step 8, 50% at step 16, 90% at step 18 and 99% at step 20 (Figure 8.3). Growth is exponential at first and then saturates.

*Interpretation.* Twelve steps take the worm from 1% to 99%, so the response must be automatic: patching, network segmentation, egress filtering and endpoint isolation.

*Conclusion.* Patch early and contain automatically; manual response comes after the knee of the curve.

**Q3 (5 marks). Why can a password be safe online but weak offline? Calculate for an 8-character password from 36 symbols.**

*Introduction.* The security of a password depends on the keyspace and on the attacker's guess rate, which depends on where the guessing happens (section 8.4).

*Calculation.* Keyspace = 36^8 = 2,821,109,907,456.

1. Online at 10 guesses per second (throttling and network delay): 2.82 x 10^11 seconds, about **8,946 years** to exhaust (half that on average).
2. Offline with a fast unsalted hash at 10^10 guesses per second: about **282 seconds**.
3. Offline with a slow salted hash (bcrypt class, 10^4 per second): about **9 years**.

*Explanation.* An attacker with a stolen hash file is not limited by lockouts or the network, so the stored form of the password decides the outcome.

*Defence.* Salted slow hashing, long passphrases, breached-password checks, throttling and MFA.

*Conclusion.* Make guessing slow for the attacker and rely on more than one factor.

**Q4 (10 marks). Explain denial of service and distributed denial of service attacks, with the amplification and SYN-flood arithmetic, and the countermeasures.**

*Introduction.* DoS attacks the availability of the CIA triad; DDoS uses many sources, usually a botnet under a command-and-control channel (section 8.8, Figure 8.2).

*Categories.* **Volumetric** (bandwidth: UDP floods, reflection and amplification), **protocol** (state exhaustion: SYN flood) and **application layer** (HTTP floods, slow connections).

*Amplification.* In reflection, the attacker forges the victim's address in small requests to open servers; the larger replies go to the victim. Factor = response size / request size. A 60-byte DNS request that gets a 3,000-byte reply has factor 50, so a 100 Mbit/s attacker produces **5 Gbit/s**; an NTP-style 234-byte request with a 46,800-byte reply has factor 200 and gives **20 Gbit/s**.

*SYN flood.* A backlog of 128 half-open entries with a 60-second lifetime is kept full by 128 / 60 = **2.13 SYN/s**, about 128 bytes per second. It is a state problem, not a bandwidth problem.

*Countermeasures.*

1. Disable open resolvers and legacy commands; rate-limit responses.
2. Ingress and egress filtering (BCP 38) to stop spoofed sources.
3. SYN cookies and a tuned backlog.
4. CDN, anycast and a scrubbing provider for volumetric attacks.
5. Rate limiting, caching and a web application firewall at the application layer.
6. A tested DDoS runbook; keep your own devices out of botnets by changing default credentials and patching.

*Conclusion.* Different DoS types need different defences, so identify the exhausted resource first.

**Q5 (10 marks). Explain social engineering: techniques, psychological levers, and how an organisation defends against it.**

*Introduction.* Social engineering manipulates people rather than machines, so technical controls alone fail against it (section 8.7).

*Levers.* Authority, urgency, reciprocity, liking, social proof, scarcity and fear.

*Techniques.* Phishing, spear phishing and whaling, vishing, smishing, pretexting, baiting, tailgating, shoulder surfing, dumpster diving, business email compromise and impersonation on social networks.

*Insider threats.* Malicious, negligent and compromised insiders: least privilege, separation of duties and prompt de-provisioning reduce harm.

*Defences.*

1. Verify out of band, calling a known number.
2. Treat urgency and secrecy as warning signs.
3. Never share OTPs, PINs or passwords.
4. Check links and sender addresses.
5. Use phishing-resistant MFA (FIDO2).
6. Train regularly and run simulated phishing; reward reporting.
7. Control physical access with badges, visitor logs and shredders.
8. Require two-person approval and a call-back to change payment details.

*Ethics.* A social engineering test needs explicit rules of engagement on whom to test, what to collect and how to protect the data.

*Conclusion.* People are the last line of defence and need clear procedures, training and a blame-free reporting culture.
