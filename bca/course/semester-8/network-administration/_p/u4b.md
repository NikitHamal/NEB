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

