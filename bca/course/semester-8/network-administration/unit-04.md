---
subject: Network Administration
grade: BCA Semester 8 (Elective III)
unit: 4
title: Service Recommendation
hours: 16
area: BCA 453 · Network Administration · Unit 4
---

This unit turns the principles of Units 2 and 3 into recommendations for the services every organisation runs: how to **upgrade a server** safely, whether to **centralise** a service, how to **monitor** it, how to design **namespaces**, and how to run **e-mail, printing, data storage, backup and restore, a software repository and web services**. For each service the unit gives a recommended design, the reasons, a working configuration and the points on which examiners ask questions.

::: key What this unit gives you
- Server upgrades as a controlled procedure with a rollback; the case for and against centralising a service.
- Service monitoring: what to measure, how to alert and how to escalate.
- Namespaces for hosts, users and e-mail, with DNS and directory examples.
- E-mail (SMTP, IMAP, MX, SPF, DKIM, DMARC), printing (CUPS, queues, quotas), data storage (DAS, NAS, SAN), backup and restore (full, incremental, differential, retention, restore tests), software repositories and web services.
:::

## 4.1 Server upgrade

### 4.1.1 Why upgrading is risky and how to make it routine

Every server must eventually be upgraded: the vendor stops releasing security patches, the service needs a new version, the hardware ages. An upgrade changes a working system, so the danger is that something that worked yesterday stops today, often in a way nobody predicted because the old system carried years of undocumented settings. The recommendation is to treat an upgrade as a **project with a procedure**, never as an afternoon of typing. Done often and in small steps, upgrades become routine; postponed for years, they become dangerous.

### 4.1.2 Upgrade strategies

| Strategy | How | Advantages | Limits |
|---|---|---|---|
| **In-place** | Upgrade the OS or software on the same server | No new hardware; quick for small changes | Old state is lost unless snapshotted; long outage if it fails |
| **Side by side (parallel)** | Build the new server beside the old one, copy data, switch over by moving the DNS alias or address | Old server remains as instant rollback; test before cut-over | Needs extra hardware or VM; data synchronisation at cut-over |
| **Blue/green** | Two identical environments, one live (blue) and one new (green); traffic is switched at once | Almost no downtime, instant rollback | Double resources; database changes must be compatible |
| **Rolling** | Upgrade nodes of a cluster one by one, keeping the service up | No outage | Needs redundancy and version compatibility |
| **Canary** | Send a small share of users to the new version first | Early detection of problems | Needs routing and monitoring control |

Because services should be reached by an alias (Section 2.3.3), side-by-side upgrades are the preferred method for important servers: clients never learn that the machine behind `mail.college.edu.np` has changed.

### 4.1.3 The upgrade procedure

1. **Define the scope**: what is being upgraded and why; what depends on it (applications, scripts, integrations, other services).
2. **Build a service checklist**: every function the service provides, including the obscure ones (cron jobs, printers, licences, certificate renewals, firewall rules, scripts that call the server).
3. **Test in a lab** with a copy of the data. Ask pilot users to try their normal work; include the awkward cases from the checklist.
4. **Write the back-out plan** and decide the **point of no return**: the stage after which going back costs more than going forward. If you cannot go back, test twice as hard.
5. **Back up** the system and data and test that the backup restores. Snapshot VMs.
6. **Choose the window** with users' calendar in mind (not in examination week, not on Friday evening), and **announce** it with the date, duration, expected effect and contact.
7. **Execute** with a written step list, a second person watching, and a note of the time of each step. If the planned duration is exceeded by a set margin, trigger the back-out.
8. **Test** with the service checklist, and ask a pilot user to confirm.
9. **Communicate** the result; update documents, monitoring and inventory; keep the old system available for a defined period before decommissioning.
10. **Review**: what went wrong, what to add to the checklist.

::: example Upgrading a mail server (side by side)
Old: `mail1` on an end-of-life Linux; new: `mail2` on a current release. Steps: build `mail2` from the automated install and configuration; set the DNS TTL of `mail.college.edu.np` to 5 minutes a week in advance; synchronise mailboxes with `rsync` nightly; in the window, stop `mail1`, run a final synchronisation, start `mail2`, change the alias to `mail2`; send and receive test messages; keep `mail1` powered off for two weeks. If `mail2` fails a test, switch the alias back: the rollback takes five minutes because the old server was untouched.
:::

```python
# How long must the window be?  (illustrative sizing for the final sync)
mail_gb = 600
daily_change_gb = 8                  # changed since the last nightly sync
link_mbit = 1000
efficiency = 0.6                     # protocol overhead, small files
rate_gb_h = link_mbit / 8 * 3600 / 1000 * efficiency
sync_min = daily_change_gb / rate_gb_h * 60
steps = {"stop services": 5, "final sync": sync_min, "start new + alias": 10, "tests": 30, "buffer 50%": None}
base = sum(v for v in steps.values() if v)
steps["buffer 50%"] = base * 0.5
for k, v in steps.items():
    print("%-18s %5.1f min" % (k, v))
print("window to announce : %.0f min -> request %d hours" % (base * 1.5, -(-base * 1.5 // 60)))
```
```output
stop services        5.0 min
final sync           1.8 min
start new + alias   10.0 min
tests               30.0 min
buffer 50%          23.4 min
window to announce : 70 min -> request 2 hours
```
## 4.2 Centralising a service

### 4.2.1 Centralised and decentralised services

A **centralised** service is run by one team for the whole organisation: one e-mail system, one directory, one DNS, one backup system. A **decentralised** service is run by each department or site: a mail server per department, a local file server in each lab. Neither is always right. The prescribed text says a service should be centralised when the organisation gains consistency and efficiency without losing service quality, and should be decentralised when the local need is genuinely different or distance makes central service poor.

| Aspect | Centralised | Decentralised |
|---|---|---|
| **Cost** | Economy of scale: one licence, one expert team, one hardware pool | Duplicated hardware, licences and skills |
| **Consistency** | One policy, one version, one set of standards | Each unit differs; hard to integrate |
| **Security** | Easier to patch, audit and defend | Weakest unit is the entry point |
| **Backup and recovery** | One process, tested | Often forgotten at small sites |
| **Responsiveness** | Distance and queue; one-size-fits-all | Close to users, quick, tailored |
| **Failure impact** | Large (everyone) unless redundant | Limited to a unit |
| **Network dependence** | Needs good links to every site | Works when the WAN is down |

### 4.2.2 Deciding

Questions to ask: Is the service *the same* for everyone? Is there a skill shortage locally? Is the WAN reliable enough? Does law or policy require data to stay in a place? What does it cost to do it twice? A balanced recommendation is **centralise the common and security-critical (authentication, e-mail, DNS, DHCP policy, backup, antivirus, patching), keep local what must work without the WAN or is genuinely special (a lab server, a local cache, a branch router)**. Cloud services are a form of extreme centralisation and bring the same trade-offs.

### 4.2.3 How to centralise without a crisis

1. Agree the **service level** that the central service will offer, including support hours and response times, and put it in an SLA; centralisation fails when users receive worse service than they had.
2. Run a **pilot** with one department; learn what they did that the central design forgot.
3. **Convert in stages**, one department at a time, using the upgrade procedure of Section 4.1 for each conversion.
4. Keep **local champions**: a contact in each department who knows both worlds.
5. **Measure** after centralising: cost, tickets, availability and user satisfaction, and fix what the numbers show.

## 4.3 Service monitoring

### 4.3.1 What to monitor

Section 3.2.2 introduced the mechanisms; here is the recommended design for a service. Measure at four levels.

| Level | Question | Example for the web service |
|---|---|---|
| **Host** | Is the machine healthy? | CPU, memory, disk, temperature, interface errors |
| **Process** | Is the software running? | `nginx` running, database accepting connections |
| **Service (probe)** | Does it work as a user sees it? | A script requests the home page and checks the text and the time taken |
| **Business** | Is the outcome achieved? | Number of fee payments per hour, mails delivered per minute |

Measure the **golden signals** of a service: **latency** (how long a request takes), **traffic** (how many requests), **errors** (how many fail) and **saturation** (how full the scarce resource is).

### 4.3.2 Real-time alerting and historical data

Two kinds of monitoring are needed. **Real-time monitoring** detects failure and notifies a person: a check runs every minute; after a few failures an alert is sent by e-mail, SMS or a chat or paging system; if nobody acknowledges within a set time, it **escalates** to the next person. **Historical monitoring** records metrics for months, so that you can see trends, plan capacity, prove that the SLA was met and investigate an incident afterwards.

Design alerts well:

- Every alert should be **actionable**, **urgent** and **real**; otherwise it should be a log line or a report.
- Avoid **flapping** by requiring several consecutive failures or using hysteresis.
- Group alerts that share a cause (a switch is down, so do not page for every server behind it) by encoding **dependencies**.
- Provide a **dashboard** for the state at a glance and a **runbook link** in each alert.

```ini
# Nagios-style definition of a service check (not run in the build sandbox)
define service {
    use                  generic-service
    host_name            web01
    service_description  HTTP college site
    check_command        check_http!-H www.college.edu.np -w 2 -c 5 -s "Admission"
    check_interval       1
    retry_interval       1
    max_check_attempts   3
    notification_period  24x7
    contact_groups       admins
}
```

The check warns if the page takes over 2 seconds, becomes critical after 5 seconds or if the word "Admission" is missing, and notifies only after three failures in a row.

### 4.3.3 Uptime and SLO reporting

```python
# Availability and error budget from a month of one-minute probes (simulated outages)
minutes = 30 * 24 * 60
outages_min = [12, 7, 25, 3]               # four incidents in the month
down = sum(outages_min)
avail = 100 * (minutes - down) / minutes
slo = 99.9
budget = minutes * (100 - slo) / 100
print("minutes in month   :", minutes)
print("downtime           :", down, "min")
print("availability       : %.3f %%" % avail)
print("SLO %.1f%% allows    : %.1f min" % (slo, budget))
print("error budget left  : %.1f min  (%s)" % (budget - down, "SLO met" if down <= budget else "SLO MISSED"))
```
```output
minutes in month   : 43200
downtime           : 47 min
availability       : 99.891 %
SLO 99.9% allows    : 43.2 min
error budget left  : -3.8 min  (SLO MISSED)
```
The remaining budget tells the team how much risk it can take: if the budget is spent, upgrades and risky changes wait until reliability is repaired.

## 4.4 Namespaces

### 4.4.1 What a namespace is

A **namespace** is a set of names and the rules that map each name to something: a hostname to an address, a user name to an account, a mailbox, a printer, a file path. Namespaces are the glue of an organisation; bad ones cause confusion, collisions and security problems. Principles:

1. **Be consistent**: the same user name for login, e-mail and file access; the same naming rule on every host.
2. **Be unique**: no two things with the same name, and **do not reuse** a name quickly after its owner leaves (the old mail may still arrive and old access rights may still match).
3. **Be meaningful but not fragile**: names that encode the **function** (`mail`, `ns1`, `fileserver`) help people but break when the function moves, so use a stable machine name plus **aliases** (CNAME) for functions.
4. **Be scalable and delegable**: a hierarchy (DNS zones, organisational units) lets each part be managed locally.
5. **Be secured and managed in one place**: an authoritative, central source with automation, not hand-edited files on each server.

### 4.4.2 Host naming

Two schemes are common. **Themed names** (planets, rivers, mountains: `everest`, `kailali`) are memorable and fun for a few machines, but say nothing about purpose and run out. **Functional or structured names** (`web01.kath.edu.np`, `lab2-pc17`) describe site, role and number, which are easier at scale. Recommendation: use **structured names for machines**, **aliases for services**, avoid names of people and avoid names that expose sensitive purpose to outsiders (`finance-db`).

### 4.4.3 DNS as the main namespace

The **Domain Name System** is a hierarchical, distributed database. The organisation runs authoritative servers for its **zone** (for example `college.edu.np`), publishes records and delegates sub-zones (for example `lab.college.edu.np`). Run at least two authoritative servers on different networks. Useful records: **A/AAAA** (name to address), **CNAME** (alias), **MX** (mail exchanger, with preference), **NS** (name servers), **PTR** (reverse lookup), **TXT** (SPF, DKIM, verification), **SRV** (service location). Split-horizon DNS gives inside users the private addresses and outside users the public ones.

```ini
; zone file fragment for college.edu.np (BIND format, not run in the build sandbox)
$TTL 3600
@     IN SOA ns1.college.edu.np. hostmaster.college.edu.np. (
            2025010101 ; serial
            3600       ; refresh
            900        ; retry
            1209600    ; expire
            300 )      ; negative TTL
      IN NS    ns1.college.edu.np.
      IN NS    ns2.college.edu.np.
      IN MX 10 mail.college.edu.np.
      IN MX 20 mail-backup.college.edu.np.
ns1   IN A     203.0.113.2
ns2   IN A     203.0.113.3
web01 IN A     203.0.113.10
www   IN CNAME web01
mail  IN CNAME mx01
mx01  IN A     203.0.113.20
```

Remember to increase the **serial number** at every change, to give a short TTL before planned moves, and to check with `dig`, `named-checkzone` and a secondary server.

### 4.4.4 Users, directories and e-mail names

A **directory service** stores identities and authenticates them for all services: **LDAP** (OpenLDAP, FreeIPA) or **Microsoft Active Directory** (LDAP, Kerberos and DNS together). The aim is **single sign-on, one account, one password** (with MFA), one place to disable a leaver. Policy needs rules for the **user name format** (first initial and surname, with a number to break ties), for **numeric user IDs** (UID/GID unique across all Linux hosts, otherwise file ownership on shared storage is wrong), for **groups** by role (staff, students, lab), and for **mail addresses** that follow the user name and may have aliases.

::: caution Names that cause outages
Reusing a user name for a new person gives them the old person's file ownership, mailing-list membership and sometimes access. Disable and archive, wait, and then retire the name according to written policy.
:::

## 4.5 E-mail service

### 4.5.1 How e-mail works

E-mail is the service every user notices first when it fails. It is built from separate roles:

| Role | Name | Job | Protocols |
|---|---|---|---|
| Client | **MUA** (mail user agent) | Outlook, Thunderbird, webmail | SMTP submission (587), IMAP (993), POP3 (995) |
| Sending server | **MSA/MTA** | Accepts mail from users and relays it onwards | SMTP (25 between servers, 587 for users) |
| Receiving server | **MTA** | Accepts mail for the domain, found through the **MX record** | SMTP (25) |
| Delivery | **MDA** | Puts the message into the mailbox | LMTP |
| Store and access | Mailbox server | Keeps messages, serves clients | IMAP or POP3 |

A message from `ram@college.edu.np` to `sita@example.com` is submitted to the college's server (authenticated, TLS), which looks up the **MX** records of `example.com`, tries the lowest preference number first, and hands over by SMTP; the receiving server delivers it to Sita's mailbox, from which her client fetches it by IMAP. **IMAP** keeps mail on the server and synchronises many devices; **POP3** downloads and usually deletes, which suits one device only.

### 4.5.2 Recommended design

- **Choose between on-premises and hosted.** For most colleges and small organisations a **hosted service** (Microsoft 365, Google Workspace, or an education plan) is the recommendation: someone else keeps it patched, redundant and backed up, and spam filtering is built in. Run your own mail only when policy, cost or skill requires, and then treat it as the hardest service on the network.
- **Use your own domain** in either case, with MX, SPF, DKIM and DMARC records.
- **Separate roles** in an own-run design: an inbound **gateway** doing spam and malware filtering, the mail store behind it, and an outbound relay with rate limits.
- **Authenticate users** against the central directory, with TLS required and MFA for webmail.
- **Quota and retention** policies: mailbox size, archive, deleted-item recovery period, legal retention.
- **Monitoring**: queue length, delivery time (send a test message every few minutes), disk, certificates, blacklists.

### 4.5.3 Anti-spam and authentication of senders

Spam and forged mail are the main operational problem. Three DNS-based records prove that a sender is allowed to use a domain:

| Record | Purpose | Example (TXT) |
|---|---|---|
| **SPF** | Lists the servers allowed to send for the domain | `v=spf1 mx ip4:203.0.113.20 include:_spf.google.com -all` |
| **DKIM** | A public key; the sender signs each message, the receiver checks the signature | `selector1._domainkey` TXT `v=DKIM1; k=rsa; p=...` |
| **DMARC** | Tells receivers what to do when SPF and DKIM fail and where to send reports | `_dmarc` TXT `v=DMARC1; p=quarantine; rua=mailto:dmarc@college.edu.np` |

Other protections: greylisting, reputation lists, content filters (SpamAssassin, Rspamd), attachment and malware scanning, rate limits on outgoing mail (a compromised account can send thousands of messages in minutes), and user training against phishing. Never run an **open relay**, a server that forwards mail from anybody to anybody: it will be abused within hours and blacklisted.

```python
# Choosing the MX target: lowest preference first, next on failure (simulation)
mx = [(20, "mail-backup.college.edu.np", True), (10, "mail.college.edu.np", False), (30, "mx3.example.net", True)]
print("MX records, lowest preference tried first:")
for pref, host, up in sorted(mx):
    print("  try %-28s pref %2d ... %s" % (host, pref, "delivered" if up else "connection refused"))
    if up: break

# a basic SPF-like check against the allowed networks
import ipaddress
allowed = [ipaddress.ip_network("203.0.113.20/32"), ipaddress.ip_network("198.51.100.0/24")]
for sender in ("203.0.113.20", "198.51.100.77", "192.0.2.9"):
    ok = any(ipaddress.ip_address(sender) in n for n in allowed)
    print("sender %-14s SPF %s" % (sender, "pass" if ok else "fail (reject or quarantine under DMARC)"))
```
```output
MX records, lowest preference tried first:
  try mail.college.edu.np          pref 10 ... connection refused
  try mail-backup.college.edu.np   pref 20 ... delivered
sender 203.0.113.20   SPF pass
sender 198.51.100.77  SPF pass
sender 192.0.2.9      SPF fail (reject or quarantine under DMARC)
```
### 4.5.4 A minimal Linux mail server

```ini
# /etc/postfix/main.cf (essentials; not run in the build sandbox)
myhostname = mail.college.edu.np
mydomain = college.edu.np
myorigin = $mydomain
inet_interfaces = all
mydestination = $myhostname, localhost.$mydomain, $mydomain
mynetworks = 127.0.0.0/8
smtpd_tls_cert_file = /etc/letsencrypt/live/mail.college.edu.np/fullchain.pem
smtpd_tls_key_file  = /etc/letsencrypt/live/mail.college.edu.np/privkey.pem
smtpd_tls_security_level = may
smtpd_sasl_auth_enable = yes
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_recipient_restrictions = permit_sasl_authenticated, reject_unauth_destination
message_size_limit = 26214400
```

`mynetworks` limits who may relay without authenticating, and the last-but-one line makes the server accept mail only for its own domains or from authenticated users, which is the setting that prevents an open relay. Dovecot provides IMAP and the authentication. Test with `swaks` or `openssl s_client -connect mail.college.edu.np:587 -starttls smtp`, and read `/var/log/mail.log`.

## 4.6 Print services

### 4.6.1 Why printing is a real service

Printing looks trivial and causes a surprising share of help-desk tickets: drivers, queues, jams, toner, access. A good design makes printing **predictable and cheap**.

### 4.6.2 Recommended design

- **Central print servers** (CUPS on Linux; Windows Print Server role) own the queues; users connect to a **queue**, not to the printer. Printers can be replaced without touching any client.
- **Standardise** on a few printer models, with network interfaces and PCL or PostScript, and **use the vendor's universal driver** where possible.
- **Printers on a printer VLAN**, with fixed addresses by DHCP reservation, firewalled so that only the print server can reach them.
- **Naming**: queue names show location and type (`lib-ground-bw`, `office-colour`), and the same name appears on the printer's label.
- **Control cost**: default to duplex and black and white, **quotas** or pay-for-print with an ID card, and reports of usage per department.
- **Secure printing**: hold jobs until the user releases them at the printer with a card or PIN, so that confidential pages are not left in the tray; disable unneeded printer services and change default passwords.
- **Supplies and maintenance**: monitor toner by SNMP, keep spare toner, a maintenance contract for heavy-use machines; count pages per month to size the printer (the duty cycle).
- **Multifunction devices** are computers: patch their firmware and treat them as servers for security.

### 4.6.3 CUPS in practice

CUPS (Common UNIX Printing System) uses the **Internet Printing Protocol (IPP)** and serves Linux, macOS and Windows clients.

```bash
# not run in the build sandbox
sudo apt install cups
sudo cupsctl --share-printers --remote-any          # make queues available on the network
sudo lpadmin -p lib-ground-bw -E -v ipp://10.20.50.11/ipp/print -m everywhere
sudo lpadmin -p lib-ground-bw -o sides=two-sided-long-edge -o media=A4
sudo lpoptions -d lib-ground-bw                     # default printer
lp -d lib-ground-bw report.pdf                      # send a job
lpstat -p -d ; lpstat -o                            # printers and the job queue
cancel -a lib-ground-bw                             # clear a stuck queue
sudo cupsaccept lib-ground-bw ; sudo cupsenable lib-ground-bw
```

The web interface on port 631 is the usual way to add printers; restrict it to the management VLAN. On Windows, add the Print and Document Services role, add the printer with its driver, share it, and use **Group Policy** (Printer Preferences) to give each department its printers.

```python
# Printing cost model for a lab: should we charge per page?  (illustrative)
pages_per_month = 60_000
cost_per_page = 1.8        # NPR toner, paper, depreciation
free_quota = 40            # pages per student per month
students = 1200
free_pages = students * free_quota
print("cost now (no control): NPR %d" % (pages_per_month * cost_per_page))
# experience from print-quota projects: 30-50 % drop; we assume 35 %
after = pages_per_month * 0.65
print("pages after quota   : %d  cost NPR %d" % (after, after * cost_per_page))
print("monthly saving      : NPR %d" % (pages_per_month * cost_per_page - after * cost_per_page))
print("quota capacity      : %d free pages for %d students" % (free_pages, students))
```
```output
cost now (no control): NPR 108000
pages after quota   : 39000  cost NPR 70200
monthly saving      : NPR 37800
quota capacity      : 48000 free pages for 1200 students
```
The 35% reduction is an assumption, flagged as such; a pilot in one lab gives the real number.

## 4.7 Data storage

### 4.7.1 Types of storage

| Type | What it is | Access | Typical use |
|---|---|---|---|
| **DAS** (direct-attached storage) | Disks inside or cabled to one server | Block, by that server only | Server's own disks, databases |
| **NAS** (network-attached storage) | A file server that shares **files** over the network | **NFS** (Unix), **SMB/CIFS** (Windows) | User home folders, department shares |
| **SAN** (storage area network) | Shared **block** storage on a dedicated network | **iSCSI** (over Ethernet) or **Fibre Channel** | Virtualisation clusters, databases |
| **Object storage** | Objects with metadata in a flat namespace, reached by HTTP API | S3 API | Backups, media, cloud-native applications |
| **Cloud storage** | Any of the above rented from a provider | Varies | Off-site copies, collaboration |

Block storage presents a raw disk (a **LUN**) on which the server builds its own file system; file storage presents a ready file system. Choose the simplest type that meets the need: most small organisations need **one NAS or a file server with RAID and snapshots**, plus an off-site backup.

### 4.7.2 Design recommendations

1. **Separate data from the operating system**, and keep **user data off workstations**.
2. **Protect against disk failure** with RAID (Section 2.2.3), and against everything else with **backup** (Section 4.8): RAID is not a backup.
3. **Use snapshots** (ZFS, LVM, NAS or Windows VSS shadow copies): they let a user recover yesterday's file in seconds without calling the administrator.
4. **Set quotas** so one user or one department cannot fill the disk, and **monitor free space** with warnings at 80% and 90%.
5. **Use volume management (LVM, ZFS, Storage Spaces)** so that volumes can be grown online.
6. **Tier the data**: fast SSD for databases and active data, cheaper HDD for archives, and cold storage for old records.
7. **Control access** with groups and ACLs, not individual users; give each share an **owner** who approves access.
8. **Plan capacity** from growth, as in Section 2.3.3, and **monitor performance** (IOPS, latency); a slow shared disk makes every service slow.
9. **Use secure protocols**: SMB 3 with signing and encryption, NFSv4 with Kerberos; never expose SMB to the internet.
10. **Document** where each dataset lives, who owns it and how it is backed up.

```bash
# Linux file server examples (not run in the build sandbox)
# LVM: pool two disks, create a volume, grow it later while mounted
sudo pvcreate /dev/sdb /dev/sdc && sudo vgcreate data /dev/sdb /dev/sdc
sudo lvcreate -L 500G -n shares data && sudo mkfs.ext4 /dev/data/shares
sudo lvextend -L +200G -r /dev/data/shares            # grow volume and file system

# NFS export to the lab subnet only
echo '/srv/shares/lab 10.20.20.0/24(rw,sync,root_squash,no_subtree_check)' | sudo tee -a /etc/exports
sudo exportfs -ra

# Samba share for staff (fragment of /etc/samba/smb.conf)
#   [staff]
#     path = /srv/shares/staff
#     valid users = @staff
#     read only = no
#     vfs objects = shadow_copy2
```

```python
# Quota check: who is near the limit?  (simulated usage report)
quota_gb = 20
usage = {"ram": 18.4, "sita": 7.1, "hari": 21.7, "gita": 15.9, "bina": 19.9}
for u, g in sorted(usage.items(), key=lambda x: -x[1]):
    pct = 100 * g / quota_gb
    state = "OVER" if pct >= 100 else "WARN" if pct >= 80 else "ok"
    print("%-5s %5.1f GB  %5.1f %%  %s" % (u, g, pct, state))
```
```output
hari   21.7 GB  108.5 %  OVER
bina   19.9 GB   99.5 %  WARN
ram    18.4 GB   92.0 %  WARN
gita   15.9 GB   79.5 %  ok
sita    7.1 GB   35.5 %  ok
```
## 4.8 Backup and restore

### 4.8.1 The purpose: restore, not backup

Nobody wants a backup; everybody wants a **restore**. A backup system is judged by one question: *can we get the right data back, quickly enough, from the date we need?* Data is lost by disk failure, deleted files, software bugs, corruption, ransomware, theft, fire and administrator error; backups are the only defence against all of them. Replication and RAID protect only against some.

### 4.8.2 Policy first

Write the backup policy before choosing tools. It states, for each class of data:

| Item | Decision |
|---|---|
| **What** | Which systems and data are backed up (and which are not, such as temporary files) |
| **How often** | Set by the **RPO**: how much work may be lost |
| **How long to keep** | **Retention**: daily copies for 2 weeks, weekly for 3 months, monthly for a year, yearly for law or audit |
| **How fast to restore** | The **RTO**: determines the media, the network and the method |
| **Where** | On-site copy for speed, off-site copy for disasters, an offline or immutable copy for ransomware |
| **Who** | Owner of the policy, operator, who may request a restore |
| **Security** | Encryption of backup data, protected keys, controlled access |
| **Verification** | Automatic checks and scheduled restore tests |

### 4.8.3 Kinds of backup

| Kind | Copies | Backup time and size | Restore |
|---|---|---|---|
| **Full** | Everything | Longest and largest | Simplest: one set |
| **Incremental** | Only changes since the **last backup of any kind** | Smallest and fastest | Slowest: last full plus **every** incremental since |
| **Differential** | Changes since the **last full** | Grows during the week | Last full plus the **latest** differential |
| **Synthetic full** | Server combines the full and incrementals into a new full | Light on clients | Simple |
| **Snapshot / continuous** | Storage-level point-in-time copies, or continuous replication | Very quick | Fast; but same system, so not a stand-alone backup |

A common rotation is the **grandfather-father-son** scheme: daily incrementals (sons), a weekly full (father), a monthly full kept long (grandfather). The **3-2-1 rule** (Section 2.3.5) gives the number and place of the copies.

```svgfig label="4.1" caption="Restoring from a weekly full with daily incrementals needs the full plus every incremental up to the chosen day; with differentials only the latest differential is needed."
f = Fig(660, 230)
days = ["Sun\nfull", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
for i, d in enumerate(days):
    x = 15 + i * 92
    f.box(x, 30, 80, 42, d, fill=SAND if i == 0 else BLUE, stroke=AMBER if i == 0 else NAVY, size=10)
f.text(330, 18, "Incremental: restore Thursday = full + Mon + Tue + Wed + Thu (5 sets)", size=10, color=NAVY, bold=True)
f.box(15, 130, 80, 42, "Sun\nfull", fill=SAND, stroke=AMBER, size=10)
for i in range(1, 7):
    x = 15 + i * 92
    f.box(x, 130, 80, 42, "%s\ndiff." % ["", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][i], fill=SOFT, stroke=SLATE, size=10)
f.text(330, 118, "Differential: restore Thursday = full + Thursday's differential (2 sets)", size=10, color=NAVY, bold=True)
f.text(330, 205, "Faster restore costs more backup space; faster backup costs a longer restore.", size=10, color=SLATE)
```

```python
# Compare incremental and differential schemes for a weekly cycle
full_gb, daily_change_gb = 800, 24     # new or changed data per day
# a differential repeats earlier changes; assume 40% of each later day's changes touch files already changed
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
inc = [daily_change_gb] * 6
diff = []
changed = 0
for i in range(6):
    changed += daily_change_gb * (0.6 if i else 1.0)
    diff.append(changed)
print("full backup              : %d GB" % full_gb)
print("incremental sizes (GB)   :", [round(x) for x in inc], " week total %d" % (full_gb + sum(inc)))
print("differential sizes (GB)  :", [round(x) for x in diff], " week total %d" % (full_gb + sum(diff)))
for day_no, d in enumerate(days, 1):
    sets_inc = 1 + day_no
    sets_diff = 2
    print("restore after %s: incremental needs %d sets, differential %d sets" % (d, sets_inc, sets_diff))

# backup window: how long does the full take?
rate_mb_s = 110           # about one gigabit link
print("full backup time: %.1f h" % (full_gb * 1024 / rate_mb_s / 3600))
```
```output
full backup              : 800 GB
incremental sizes (GB)   : [24, 24, 24, 24, 24, 24]  week total 944
differential sizes (GB)  : [24, 38, 53, 67, 82, 96]  week total 1160
restore after Mon: incremental needs 2 sets, differential 2 sets
restore after Tue: incremental needs 3 sets, differential 2 sets
restore after Wed: incremental needs 4 sets, differential 2 sets
restore after Thu: incremental needs 5 sets, differential 2 sets
restore after Fri: incremental needs 6 sets, differential 2 sets
restore after Sat: incremental needs 7 sets, differential 2 sets
full backup time: 2.1 h
```
### 4.8.4 Design recommendations

1. **Automate** schedules and **monitor** results; a backup that fails silently for three months is the usual story. Alert on failure *and* on missing success reports.
2. **Verify**: check integrity after every run and **test a restore** regularly, a file, a mailbox and a whole server, with the time taken written down and compared with the RTO.
3. **Protect the backups**: encrypt them, keep the keys apart, use an account that production systems cannot delete from, and keep an **offline or immutable** copy so that ransomware cannot encrypt the backups with the data.
4. **Back up consistently**: databases need a dump or a snapshot-aware agent (copying files of a running database yields garbage); applications may need quiescing.
5. **Network**: back up over a dedicated network or at night; use deduplication and compression; for remote sites send the first full on disk and increments over the WAN.
6. **Capacity**: plan from the data size, change rate and retention (the program below).
7. **Document** the restore procedure, including how to rebuild the backup system itself.
8. **Do not forget** laptops, SaaS data (hosted mail and documents are still your responsibility), configuration of network devices and the DNS zone files.

Tools: `rsync` and `tar` for simple jobs; `restic`, `borg` and `duplicity` (encrypted, deduplicated); Bacula, Amanda and Veeam for enterprise; Windows Server Backup and VSS on Windows; storage and cloud snapshots.

```bash
# restic example (not run in the build sandbox)
export RESTIC_REPOSITORY=sftp:backup@10.20.60.5:/srv/restic RESTIC_PASSWORD_FILE=/root/.restic-pass
restic init
restic backup /srv/shares /etc --exclude '*.tmp'
restic forget --keep-daily 14 --keep-weekly 12 --keep-monthly 12 --prune
restic check
restic restore latest --target /tmp/restore-test --include /srv/shares/staff/budget.xlsx
```

```python
# Capacity for retention: 2 TB data, 2% daily change, weekly full, 4 weekly + 12 monthly kept
data_tb, change = 2.0, 0.02
weekly_fulls_kept, monthly_kept = 4, 12
daily_inc_per_week = 6 * data_tb * change
week_set = data_tb + daily_inc_per_week
total = week_set * weekly_fulls_kept + data_tb * monthly_kept
print("one week of sets (full + 6 incrementals): %.2f TB" % week_set)
print("4 weeks + 12 monthly fulls               : %.1f TB (before deduplication)" % total)
dedup = 0.35
print("with 3:1-ish deduplication and compression (35%% of raw): %.1f TB" % (total * dedup))
```
```output
one week of sets (full + 6 incrementals): 2.24 TB
4 weeks + 12 monthly fulls               : 33.0 TB (before deduplication)
with 3:1-ish deduplication and compression (35% of raw): 11.5 TB
```
## 4.9 Software repository

### 4.9.1 What it is and why have one

A **software repository (software depot)** is the organisation's own, controlled source of software: operating-system packages, updates, applications, licences and in-house tools. Users and machines install from it instead of from random websites. Reasons: **consistency** (everyone gets the tested version), **security** (patches are tested and signed, and nothing unknown is installed), **bandwidth** (a package is downloaded once from the internet, then distributed on the LAN), **licence control**, **reproducibility** and the ability to **work offline** or on restricted networks.

### 4.9.2 Kinds of repository

| Kind | Examples |
|---|---|
| **OS package mirror or cache** | Local mirror of Ubuntu or Rocky repositories (`apt-mirror`, `reposync`), a caching proxy (`apt-cacher-ng`) |
| **Update server** | WSUS or Windows Update for Business, Red Hat Satellite, Landscape |
| **Application deployment** | Microsoft Intune or Configuration Manager, Chocolatey/Winget private source, Ansible |
| **Language and artefact repositories** | Nexus, Artifactory or Gitea packages for pip, npm, Maven, container images (Harbor) |
| **Installers and licence store** | A file share with checksums, documented licence keys and keys server |

### 4.9.3 Design recommendations

1. **Mirror or cache** the repositories your systems use; machines point to the internal name (`repo.college.edu.np`) by configuration management.
2. **Stage updates**: *testing* group, then *pilot*, then everyone, as for any change; keep the previous package versions to roll back.
3. **Sign and verify** packages (GPG keys, hash lists); never disable signature checking to make an installation work.
4. **Keep an inventory** of what is installed where and which licences are in use, to prove compliance and to find vulnerable versions fast.
5. **Control who may publish** to the internal repository; automate builds from version control.
6. **Plan capacity**: a full mirror of one Linux release is hundreds of gigabytes, so mirror only the repositories and architectures you need.
7. **Make it reliable**: it is a dependency of installation and patching, so back it up and serve it from two hosts if it matters.
8. **Respect licences**: free software has licences too; commercial software must be bought for each use; unlicensed copies are a legal and security risk.

```bash
# Ubuntu client using an internal mirror, and a caching proxy (not run in the build sandbox)
# /etc/apt/sources.list.d/internal.sources
#   Types: deb
#   URIs: http://repo.college.edu.np/ubuntu
#   Suites: jammy jammy-updates jammy-security
#   Components: main universe
# Cache proxy on the server:
sudo apt install apt-cacher-ng            # clients: echo 'Acquire::http::Proxy "http://repo:3142";' > /etc/apt/apt.conf.d/01proxy
# Rocky/Alma mirror with dnf
sudo dnf install dnf-utils createrepo_c
sudo reposync --repoid=baseos --download-metadata -p /srv/repo/rocky9
```

```python
# Bandwidth saved by a local cache
machines, update_mb = 150, 900
without = machines * update_mb / 1024            # every machine downloads from the internet
with_cache = update_mb / 1024                    # only the cache downloads; the LAN carries the rest
print("internet traffic without cache: %.1f GB" % without)
print("internet traffic with cache   : %.2f GB" % with_cache)
print("download time on a 10 Mbit/s link: %.1f h without, %.2f h with" % (without * 8192 / 10 / 3600, with_cache * 8192 / 10 / 3600))
```
```output
internet traffic without cache: 131.8 GB
internet traffic with cache   : 0.88 GB
download time on a 10 Mbit/s link: 30.0 h without, 0.20 h with
```
## 4.10 Web services

### 4.10.1 Anatomy of a web service

A web service answers HTTP(S) requests with pages or data. A production design has layers, and each layer is a choice:

```svgfig label="4.2" caption="A recommended web-service architecture: the load balancer and reverse proxy terminate TLS, application servers are replaceable, state lives in the database."
f = Fig(680, 230)
f.box(10, 90, 90, 50, "Users\nbrowsers", fill=SAND, stroke=AMBER, size=10)
f.box(130, 90, 110, 50, "Firewall +\nCDN / DNS", fill=SOFT, stroke=SLATE, size=10)
f.box(270, 90, 110, 50, "Load balancer\nTLS, reverse proxy", fill=BLUE, stroke=NAVY, size=10)
f.box(420, 30, 110, 45, "Web / app\nserver 1", fill=BLUE, stroke=NAVY, size=10)
f.box(420, 105, 110, 45, "Web / app\nserver 2", fill=BLUE, stroke=NAVY, size=10)
f.box(420, 180, 110, 40, "Static files /\ncache", fill=SOFT, stroke=SLATE, size=9)
f.box(570, 70, 100, 70, "Database\n(primary +\nreplica)", fill=SOFT, stroke=SLATE, size=10)
f.arrow([(100, 115), (130, 115)], color=NAVY)
f.arrow([(240, 115), (270, 115)], color=NAVY)
f.arrow([(380, 105), (420, 55)], color=NAVY)
f.arrow([(380, 125), (420, 127)], color=NAVY)
f.arrow([(380, 135), (420, 195)], color=SLATE, dash=True)
f.arrow([(530, 55), (570, 90)], color=NAVY)
f.arrow([(530, 127), (570, 115)], color=NAVY)
```

### 4.10.2 Recommendations

1. **Web server**: Nginx or Apache httpd (or IIS on Windows); use **virtual hosts** so one server hosts several sites by name; keep the document root away from system files.
2. **TLS everywhere**: certificates from a trusted CA (**Let's Encrypt** is free, automated by ACME with `certbot`); redirect HTTP to HTTPS; enable HSTS; monitor **certificate expiry**; disable old protocols (SSLv3, TLS 1.0 and 1.1).
3. **Reverse proxy and load balancer**: one public front (Nginx, HAProxy, a cloud load balancer) that spreads load, checks the health of back ends and takes a failed server out of service; this also enables rolling upgrades with no downtime.
4. **Stateless application servers**: keep sessions and files in a shared store so any server can answer any request, and a server can be replaced at any time.
5. **Caching and CDN**: cache static content and use a content-delivery network for global or heavy sites; set sensible cache headers.
6. **Separate environments** (development, test, production) and deploy by an automated pipeline.
7. **Security**: keep software patched; hide version banners; a **web application firewall (WAF)**; run the server under an unprivileged account; least privilege for the database user; rate limiting; protection against DoS at the edge; regular scanning.
8. **Logging and monitoring**: access and error logs sent to the central log server; probes for the home page, login and payment; track the golden signals (Section 4.3.1).
9. **Backup and DR**: site files and database in the backup policy, with a rebuild procedure, and a test of recovery on another host.
10. **Capacity**: load-test before launch and before peak times (admission results, examination registration); scale horizontally by adding servers.

```ini
# /etc/nginx/sites-available/college  (not run in the build sandbox)
server {
    listen 80;
    server_name www.college.edu.np college.edu.np;
    return 301 https://www.college.edu.np$request_uri;
}
upstream app { server 10.20.40.11:8000; server 10.20.40.12:8000; }
server {
    listen 443 ssl http2;
    server_name www.college.edu.np;
    ssl_certificate     /etc/letsencrypt/live/www.college.edu.np/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/www.college.edu.np/privkey.pem;
    add_header Strict-Transport-Security "max-age=31536000" always;
    location /static/ { root /srv/www; expires 7d; }
    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}
```

```python
# Sizing the web tier for admission-result day (illustrative)
peak_users = 6000                # at the busiest minute
requests_per_user_min = 6
rps = peak_users * requests_per_user_min / 60
per_server_rps = 150             # measured in a load test
import math
servers = math.ceil(rps / (per_server_rps * 0.65))   # keep 65% utilisation
print("peak load %.0f requests/s" % rps)
print("servers needed at 65%% utilisation: %d, plus 1 spare = %d" % (servers, servers + 1))
print("bandwidth for 120 KB average response: %.0f Mbit/s" % (rps * 120 * 8 / 1000))
```
```output
peak load 600 requests/s
servers needed at 65% utilisation: 7, plus 1 spare = 8
bandwidth for 120 KB average response: 576 Mbit/s
```
## 4.11 Summary and exercises

Upgrades are projects: side by side where possible, with a service checklist, a tested back-up and back-out plan, an announced window and a review. Centralise what is common and security-critical, keep local what must work without the WAN, and convert in stages under an SLA. Monitor at host, process, service and business level, alert only on actionable events, keep history and report against the SLO and error budget. Namespaces need consistency, uniqueness, aliases for functions, central management and delayed reuse; DNS, directories and mail addresses are the main ones. E-mail needs MX, SPF, DKIM, DMARC, TLS, filtering and no open relay, and is usually best hosted. Printing is run from central queues with standard models, quotas and secure release. Storage is chosen among DAS, NAS, SAN, object and cloud, protected by RAID, snapshots and quotas, and never confused with backup. Backups follow a written policy (RPO, RTO, retention), use full, incremental and differential schemes, follow 3-2-1 with an immutable copy, and are proven by restore tests. A software repository gives consistent, signed, cached and licence-controlled software and staged updates. Web services use TLS, a reverse proxy or load balancer, stateless application servers, caching, a WAF, monitoring and load tests.

1. Why are server upgrades risky? Describe a ten-step upgrade procedure.
2. Compare in-place, side-by-side, blue/green and rolling upgrades.
3. What is a back-out plan and a "point of no return"?
4. Compare centralised and decentralised services. Which services would you centralise in a college and why?
5. Describe how to move a department from its own mail server to a central service.
6. What are the four levels and the four golden signals of service monitoring? How do you avoid alert fatigue?
7. Define namespace. State five principles of good namespace design.
8. Compare themed and structured host names. Why use CNAME aliases for services?
9. Write the DNS records needed for a domain with a web server, a mail server with a backup, and two name servers.
10. What is a directory service? Why must UIDs be consistent?
11. Explain how e-mail travels from sender to receiver (MUA, MTA, MX, MDA, IMAP).
12. Explain SPF, DKIM and DMARC. What is an open relay and why is it dangerous?
13. Recommend a design for a college mail service and justify hosted versus self-run.
14. Design a print service for a library and two labs, covering queues, drivers, quotas and security.
15. Differentiate DAS, NAS and SAN with examples. Why is RAID not a backup?
16. List eight recommendations for a file server design. Explain snapshots and quotas.
17. Compare full, incremental and differential backups. What is needed to restore Thursday from each scheme?
18. What should a backup policy contain? Explain the 3-2-1 rule and why restores must be tested.
19. What is a software repository? Give five benefits and the design recommendations.
20. Explain a layered web-service architecture and ten recommendations for running it.
21. A full backup is 800 GB and the daily incremental is 24 GB. With one weekly full and six incrementals, what is the weekly total, and how many sets must be restored for Wednesday?
22. A site expects 3,000 users in the peak minute with 5 requests each, and one server handles 100 requests per second at 65% utilisation of its limit: how many servers are required?

**Answers to the numerical items.** (21) Weekly total = 800 + 6 x 24 = 944 GB. Wednesday needs the full plus Monday, Tuesday and Wednesday incrementals: 4 sets (the program in Section 4.8.3 prints 1 + day number). (22) Requests per second = 3000 x 5 / 60 = 250. If 100 requests/s is the capacity at the chosen utilisation, 250/100 = 2.5, so 3 servers, plus one spare makes 4. In the program of Section 4.10.2 the 6,000 users x 6 requests give 600 requests/s and, at 65% of a 150 requests/s limit (97.5 per server), 7 servers plus a spare.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Compare full, incremental and differential backups.**

A full backup copies everything: it is the largest and slowest to make but restores from one set. An incremental backup copies only what changed since the previous backup of any kind: it is the smallest and quickest, but a restore needs the last full and every incremental since, so it is slowest and one damaged set breaks the chain. A differential backup copies what changed since the last full: it grows through the week, but a restore needs only the last full and the latest differential. The choice balances backup window and storage against restore time; a common practice is a weekly full with daily incrementals or differentials, retained by a grandfather-father-son rotation, with an off-site copy.

**Q2 (5 marks). Explain SPF, DKIM and DMARC.**

They are DNS-published mechanisms that let receivers check that mail claiming to come from a domain is genuine. SPF lists the IP addresses allowed to send for the domain; the receiver compares the connecting address. DKIM adds a digital signature to each message made with the sender's private key; the receiver fetches the public key from DNS and verifies it, which also shows the message was not altered. DMARC builds on both: it tells receivers to accept, quarantine or reject mail that fails them (aligned with the visible From domain) and where to send reports. Together they reduce forged and phishing mail.

**Q3 (10 marks). Describe the recommended design and operation of a backup and restore service for a college.**

Policy: list the systems (file server, mail if self-run, databases, web, configuration of network devices, laptops of staff), set an RPO and RTO for each, a retention schedule (daily 14 days, weekly 12 weeks, monthly 12 months, yearly as the law or audit requires), the roles and the security rules.

Method: a weekly full and daily incremental or differential backup to disk on a backup server, with deduplication; databases through dumps or snapshot-aware agents; a second copy replicated to another building or the cloud and an offline or immutable copy to resist ransomware, following 3-2-1. Backups are encrypted and the keys are stored separately; the backup account cannot be deleted from production.

Operation: schedules run automatically; success and failure are monitored and alerts reach a person; each run verifies integrity; a restore test of a file, a mailbox and a full server is performed each term with its time compared with the RTO; capacity is planned from data size, change rate and retention; the restore procedure and the rebuild of the backup server itself are documented.

Conclusion: the quality of the service is measured by successful restores within the objectives, not by the number of backups made.

**Q4 (5 marks). Recommend a web-service architecture for admission results.**

Place the site behind a firewall and a load balancer that terminates TLS and checks the health of the back ends; run at least two stateless application servers so that any can answer any request and one can be upgraded while the other serves; keep results in a replicated database; serve static files from cache or a CDN; apply a WAF and rate limits; monitor latency, errors and traffic with probes; load-test before the day, sizing servers for peak requests per second at about 65% utilisation plus a spare; keep a rollback and a static fallback page.
