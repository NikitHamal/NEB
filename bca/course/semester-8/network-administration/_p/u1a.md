---
subject: Network Administration
grade: BCA Semester 8 (Elective III)
unit: 1
title: Introduction
hours: 4
area: BCA 453 · Network Administration · Unit 1
---

At 8:55 on a Monday morning the college e-mail does not load, the library computers cannot reach the internet and the principal cannot print the examination schedule. Nobody in the building asks how a switch works; they ask who is fixing it. That person is the **network administrator**, and this book is about doing that job well: not only repairing things, but building a network and its services so that they rarely break, and so that when they do, the damage is small and the recovery is planned.

::: key What this unit gives you
- What the profession is, what administrators actually do, the skills and certifications that employers look for.
- The ethics of a job that gives access to everybody's mail, files and logs: privacy, honesty, law and professional codes.
- Recent trends: cloud, automation and infrastructure as code, DevOps and SRE, zero trust, SD-WAN, IPv6, containers, observability and AIOps.
:::

## 1.1 The network administrator as a profession

### 1.1.1 Who is a network administrator?

A **network administrator** keeps the computers of an organisation connected, available, secure and useful. The older and broader name in the prescribed text is **system administrator (SA)**: the person who designs, builds, runs and fixes the *whole* computing service, from the cable in the wall to the e-mail in the inbox. Titles overlap in practice and change with the size of the employer.

| Title | Typical focus |
|---|---|
| **Network administrator / engineer** | Switches, routers, firewalls, Wi-Fi, VPNs, addressing, DNS and DHCP |
| **System administrator** | Servers, operating systems, user accounts, storage, backup, patching |
| **Help-desk / support technician** | First contact for users; password resets, workstation and printer problems |
| **Security administrator** | Firewalls, access control, logging, vulnerability scanning, incident response |
| **Cloud / DevOps engineer** | Cloud accounts, automated deployment, infrastructure written as code |
| **Site Reliability Engineer (SRE)** | Software-style engineering applied to reliability: SLOs, monitoring, automation |

In a small college or bank branch one person holds all these titles; in a large telecom or data centre each is a team. The skills below are the same, only the depth differs.

### 1.1.2 What the work consists of

The job divides into **reactive** and **proactive** work. Reactive work answers requests and failures: tickets from users, alarms from monitoring, a dead disk at midnight. Proactive work removes future requests: automating account creation, replacing a failing switch before it fails, writing documentation, testing the restore of a backup. The prescribed text argues that an administrator who only does reactive work is permanently "in the hole": every hour spent firefighting leaves no time for the improvements that would reduce the fires. The way out is to protect time for proactive work, keep a visible queue of requests and fix root causes instead of symptoms.

A typical day mixes:

1. **Tickets and requests**: new accounts, access rights, a printer that will not print.
2. **Monitoring and alarms**: disk space, link utilisation, certificate expiry, backup status.
3. **Change work**: patches, upgrades, new services, planned in a maintenance window.
4. **Projects**: a new branch link, migrating mail to a hosted service, replacing the Wi-Fi.
5. **Documentation and training**: runbooks, network diagrams, notes for the next person on call.
6. **Security tasks**: reviewing logs, removing stale accounts, applying advisories.

### 1.1.3 Skills

| Group | Examples |
|---|---|
| **Technical** | TCP/IP, routing and switching, Linux and Windows administration, DNS, DHCP, directory services, virtualisation, storage and backup, scripting (Bash, PowerShell, Python) |
| **Operational** | Monitoring, troubleshooting method, change management, capacity planning, disaster recovery |
| **Security** | Hardening, patching, least privilege, logging, encryption, awareness of common attacks |
| **Human** | Explaining a problem to a non-technical user, writing clear instructions, staying calm during an outage, teamwork and handover |
| **Management** | Budgeting, vendor dealing, procurement (Unit 5), writing a service-level agreement |

Troubleshooting deserves its own mention because it is the signature skill. A reliable method is: **define the symptom exactly** (who, what, since when, what changed); **form a hypothesis** from the evidence; **test it with the cheapest, least risky experiment**; **change one thing at a time**; **verify** that the symptom is gone and nothing else broke; **document** the cause and the fix. Working from the bottom of the layer model upward (cable, link light, IP address, gateway, DNS, application) finds most faults quickly.

### 1.1.4 Education, certification and career path

A BCA graduate normally starts as a help-desk or junior system administrator and moves towards network engineering, security, cloud or management. Certifications give an employer a common yardstick for what you can do, and the lab work of this course maps onto many of them:

| Area | Examples of certifications |
|---|---|
| General networking | CompTIA Network+, Cisco CCNA |
| Linux | CompTIA Linux+, Red Hat RHCSA, LPIC-1 |
| Windows | Microsoft role-based certifications (Windows Server hybrid administrator, Azure administrator) |
| Security | CompTIA Security+ |
| Cloud | AWS Certified Cloud Practitioner and Solutions Architect Associate, Azure Fundamentals |

Certification names and codes change often; check the vendor's current list. Employers in Nepal include banks and financial institutions, telecom and internet service providers, government offices, hospitals, universities and software companies; remote work for foreign employers is also common. A certificate does not replace practice: build the lab of this course on virtual machines, break it on purpose and repair it.

```svgfig label="1.1" caption="The administrator's work: proactive work shrinks the reactive queue over time."
f = Fig(640, 230)
f.box(20, 30, 170, 50, "Reactive work\ntickets, alarms, outages", fill=SAND, stroke=AMBER, size=10)
f.box(235, 30, 170, 50, "Find the root cause\nand fix it once", fill=BLUE, stroke=NAVY, size=10)
f.box(450, 30, 170, 50, "Proactive work\nautomate, monitor, document", fill=SOFT, stroke=SLATE, size=10)
f.arrow([(190, 55), (235, 55)], color=NAVY)
f.arrow([(405, 55), (450, 55)], color=NAVY)
f.arrow([(535, 80), (535, 135), (105, 135), (105, 80)], color=SLATE, dash=True, label="fewer repeat tickets, more free time", lpos=(320, 150))
f.text(320, 195, "Without protected time for proactive work, the administrator never leaves the left box.", size=10, anchor="middle", color=SLATE)
```

## 1.2 Professional ethics of the network administrator

### 1.2.1 Why ethics is a daily matter in this job

An administrator holds **privileged access**: the technical ability to read every mail, open every file, watch every connection and change any record. Technical ability is not permission. Nothing in the software stops an administrator from reading a colleague's mail or from changing a log; only professional judgement and policy do. The prescribed text devotes a chapter to ethical policies precisely because the temptation is invisible to everyone else.

Three features make the problem sharper in a network:

- **Scale of access.** One account with administrator rights reaches thousands of users' data.
- **Invisibility.** Most misuse leaves no trace unless logs exist, and the administrator controls the logs.
- **Trust.** Management and users accept that the administrator will do the right thing without checking.

### 1.2.2 Core principles

| Principle | What it means in practice |
|---|---|
| **Privacy and confidentiality** | Access personal data only when the job requires it (a fault that cannot be found otherwise), only as much as needed, and never repeat what you saw |
| **Integrity and honesty** | Do not falsify logs, hide mistakes or claim skills you lack; report an error you caused as soon as you find it |
| **Authorised access only** | Act inside the rights your role gives and inside written policy; get written approval before any unusual access |
| **Least privilege and separation of duties** | Use a normal account for daily work and administrator rights only for the task; no single person should both approve and perform a risky change |
| **Competence and diligence** | Test changes, keep backups, keep learning; negligence harms users as surely as malice |
| **Respect for law and policy** | Follow the laws, licence terms and the organisation's acceptable-use policy |
| **Responsibility to users and the public** | Warn about security risks honestly; do not conceal a data leak |
| **Professional conduct** | Share knowledge, credit others' work, hand over cleanly when leaving a post |

The professional bodies phrase these as codes. The SAGE (System Administrators' Guild, now LOPSA) code of ethics has headings such as professionalism, personal integrity, privacy, laws and policies, communication, system integrity, education, responsibility to the computing community, social responsibility and ethical responsibility; the ACM Code of Ethics and Professional Conduct (2018) covers the same ground for all computing professionals. (Check the current texts at the issuing body.)

### 1.2.3 Situations and the right response

::: example Four situations
1. **A senior manager asks you to read an employee's mail "to find out what he is saying about me".** Reading mail without a lawful and documented reason breaches privacy. The correct response is to ask for a written request through the proper channel (human resources, the legal officer or the head of the institution) that states the reason; if the request is for a genuine investigation, the authorised person decides and the action is logged.
2. **While clearing a full disk you see a student's personal photographs.** Move on and do not open or copy them. If the files are illegal or dangerous, report to the person your policy names, without spreading them.
3. **You made a mistake during a night upgrade and a table of records was overwritten.** Tell your supervisor at once, restore from backup, and write what happened. Hiding it makes the damage larger and destroys trust.
4. **A friend asks you for the college Wi-Fi password for his shop.** Passwords and network access belong to the organisation; sharing them is not your decision.
:::

### 1.2.4 Policies that protect everyone

Good policy removes guesswork. An organisation should have, in writing and known to users: an **acceptable-use policy** (what the network may be used for), a **privacy policy** stating what is logged and who may see logs, a **monitoring policy** (users are told that traffic may be monitored for security, and by whom), an **incident-response procedure** and a **data-retention policy**. When policy says "the administrator may read mail only on written request of the registrar", the administrator is protected from both temptation and blame. Policy should also say what the administrator does with legal requests from police or courts: they go to management and the legal officer, not answered by the administrator alone.

In Nepal, relevant law includes the Electronic Transactions Act, 2063 (2008) and the Privacy Act, 2075 (2018); unauthorised access, damage to data and misuse of computer systems are offences. Software licensing also matters: using unlicensed software in a college lab is a professional and legal failing, not only a cost question. (Check the current text of these Acts.)

