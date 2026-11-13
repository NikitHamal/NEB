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

