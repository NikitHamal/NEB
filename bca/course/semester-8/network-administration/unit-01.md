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

## 1.3 Recent trends in network administration

### 1.3.1 From hand-built servers to infrastructure as code

Traditionally an administrator installed each server by hand, so no two were exactly alike and nobody remembered all the changes. The modern practice is **infrastructure as code (IaC)**: the desired state of servers, networks and services is written in text files, kept in version control, reviewed, tested and applied by tools such as Ansible, Terraform or PowerShell DSC. Benefits: a server can be rebuilt in minutes, every change has an author and a date, and a test network can be created from the same files as production. Two ideas matter: **idempotence** (running the same description twice leaves the same result) and **immutable infrastructure** (replace a faulty server by a fresh one instead of repairing it).

### 1.3.2 Cloud and hybrid networks

Organisations now rent computing from public clouds (AWS, Azure, Google Cloud) or from local data-centre providers, and keep some systems on premises: a **hybrid** setup. The administrator's work moves from racks to virtual networks, security groups, identity management and cost control, and a site-to-site VPN or private link ties the college network to the cloud. Cloud does not remove the duties of administration (backup, access control, monitoring and patching still exist); it changes who is responsible for which layer, the **shared responsibility model**.

### 1.3.3 DevOps and Site Reliability Engineering

**DevOps** is a way of working in which developers and operations share responsibility for a service, release small changes often and automate testing and deployment. **Site Reliability Engineering**, developed at Google, treats operations as a software problem: a service has a **service-level objective (SLO)**, for example 99.9% of requests answered within one second; the shortfall allowed by the SLO is an **error budget** that may be "spent" on risky changes; when the budget is gone, effort moves from features to reliability. The prescribed text's third edition builds on the same ideas.

### 1.3.4 Zero trust and modern security

The old model drew a hard boundary at the firewall: inside was trusted, outside was not. Laptops, mobile phones, cloud services and remote work dissolved that boundary. **Zero trust** says: never trust a request because of where it comes from; **verify every user and device**, give **least privilege**, use **multi-factor authentication (MFA)**, encrypt traffic everywhere and log everything. Related trends: single sign-on, password managers, endpoint detection and response (EDR), and regular patching driven by vulnerability lists.

### 1.3.5 Networks: SD-WAN, Wi-Fi 6/7, IPv6, 5G

| Trend | Meaning for the administrator |
|---|---|
| **SD-WAN** | Software chooses among several links (leased line, broadband, 4G or 5G) for each application; branch routers are configured centrally |
| **Software-defined networking** | Control plane separated from forwarding devices; policy is programmed |
| **Wi-Fi 6/6E/7** | More clients per access point, 6 GHz band; wireless planning (coverage, channels, roaming) matters as much as cabling |
| **IPv6** | Exhaustion of IPv4 addresses; dual-stack operation, new firewall and DNS records (AAAA) to manage |
| **5G and fixed wireless** | A backup or primary link for branches |
| **Network automation** | Configurations pushed by scripts, with APIs and tools such as NETCONF/YANG replacing manual typing |

### 1.3.6 Containers, observability and AIOps

**Containers** (Docker) and **orchestrators** (Kubernetes) package an application with its dependencies, so administrators run services as short-lived, replaceable units. **Observability** extends monitoring: metrics, logs and traces together let you ask new questions about a running system. **AIOps** applies machine learning to alarms and logs to reduce noise and spot anomalies; it assists but does not replace the administrator's judgement. Finally, **remote and hybrid work** made VPNs, remote desktop, cloud collaboration and device management (MDM) everyday tasks.

::: caution Trend does not mean replacement
A cloud service, a managed switch with a web console or an automation tool still needs somebody who understands addressing, DNS, authentication, backup and failure. New tools change the *level* at which you work, not the need to understand what lies underneath, and an exam question on "trends" expects a definition, the problem it solves and one risk or limitation.
:::

### 1.3.7 What downtime costs: a calculation to keep in mind

Administrators justify every investment by comparing its cost with the cost of the failure it prevents. The following program computes the loss from an outage for a small online-fee-payment system.

```python
# Cost of downtime for a college fee-payment portal (illustrative numbers)
payments_per_hour = 40          # average payments per hour in office time
value_per_payment = 5000        # NPR
hours_down = 6                  # one working day outage, office hours only
lost_revenue_delayed = payments_per_hour * value_per_payment * hours_down
staff_idle_cost = 8 * 600 * hours_down   # 8 staff, NPR 600 per hour
print("delayed payments :", lost_revenue_delayed)
print("idle staff cost  :", staff_idle_cost)
print("total per outage :", lost_revenue_delayed + staff_idle_cost)

# availability allowed per year for different targets
minutes_year = 365 * 24 * 60
for pct in (99.0, 99.9, 99.99):
    allowed = minutes_year * (100 - pct) / 100
    print("%.2f%% available -> %.0f min/year (%.1f h)" % (pct, allowed, allowed / 60))
```
```output
delayed payments : 1200000
idle staff cost  : 28800
total per outage : 1228800
99.00% available -> 5256 min/year (87.6 h)
99.90% available -> 526 min/year (8.8 h)
99.99% available -> 53 min/year (0.9 h)
```
Delayed payments are not all lost; the real loss is smaller, but the staff cost and the damage to reputation are certain. A 99% target allows 87.6 hours of downtime per year, which is almost four days; 99.99% allows under an hour. The extra "nines" cost money, which is why the target must follow the business need.

## 1.4 Summary and exercises

The network administrator keeps an organisation's computers and network available, secure and useful; the work divides into reactive and proactive tasks, and the way out of constant firefighting is to protect time for root-cause fixes, automation and documentation. Skills are technical, operational, security, human and managerial; troubleshooting by a disciplined method is the core one. Administrators hold privileged access, so ethics is daily practice: privacy, integrity, authorised access only, least privilege, honesty about errors, respect for law and written policy, and codes such as SAGE/LOPSA and ACM. Recent trends are infrastructure as code, cloud and hybrid, DevOps and SRE, zero trust, SD-WAN, Wi-Fi 6/7, IPv6, containers, observability and AIOps.

1. Define network administrator. Distinguish network administrator, system administrator, help-desk technician and SRE.
2. Explain reactive and proactive work. Why does an administrator who only reacts stay "in the hole"?
3. List the skills of a network administrator under five headings, with two examples each.
4. Describe a systematic method for troubleshooting a network fault.
5. Why is ethics especially important for system and network administrators? State six principles of professional conduct.
6. A manager asks you to read a staff member's e-mail without any written request. What should you do and why?
7. What should an acceptable-use policy and a privacy policy contain? How does written policy protect the administrator?
8. What is infrastructure as code? State three benefits and explain idempotence.
9. Explain zero trust. How does it differ from the perimeter-firewall model?
10. Write short notes on: (a) SD-WAN, (b) DevOps and SRE, (c) cloud shared responsibility, (d) containers, (e) AIOps.
11. A portal handles 50 payments per hour of NPR 4,000 each and is down for 4 office hours. What is the value of payments delayed? What yearly downtime does an availability target of 99.5% allow?
12. List the recent trends in network administration and explain two of them with an advantage and a limitation.

**Answers to the numerical items.** (11) Delayed payments = 50 x 4000 x 4 = NPR 800,000 (delayed, not necessarily lost). 99.5% availability allows 0.5% of 8,760 hours = 43.8 hours per year. For the portal of Section 1.3.7 the staff cost was 8 x 600 x 6 = NPR 28,800 and the delayed payments NPR 1,200,000 for six hours.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Why does a system administrator need a code of ethics?**

An administrator has privileged access: the technical ability to read any mail or file, change any record and edit any log. The software cannot tell legitimate use from misuse, and most misuse leaves no trace unless the administrator keeps the logs, so the only control is professional judgement and policy. A code of ethics states the rules in advance: access personal data only when the work requires it and keep it confidential; be honest, including about one's own errors; act only within authorised rights; use least privilege; follow law and policy; and share responsibility to users and the public. Written policy also protects the administrator, because a request that arrives through the proper channel is a defence against both pressure and blame.

**Q2 (5 marks). Explain infrastructure as code.**

Infrastructure as code describes servers, networks and services in text files that are stored in version control, reviewed and applied automatically by tools such as Ansible or Terraform. A change is made by editing the file and applying it, not by logging in and typing. Benefits: repeatability (a server is rebuilt in minutes), an audit trail of who changed what and why, tested changes before production and consistent test and production environments. The description is idempotent, so applying it twice gives the same state. Limits: the team must learn the tools, and mistakes in code can be applied to many machines at once, so review and staged roll-out are needed.

**Q3 (10 marks). Discuss the profession of the network administrator: roles, skills, ethics and trends.**

Introduction: the network administrator keeps the organisation's computers, network and services available, secure and useful; titles such as system administrator, network engineer, security administrator, cloud/DevOps engineer and SRE describe overlapping roles that merge in small organisations.

Work: reactive tasks (tickets, alarms, outages) and proactive tasks (automation, monitoring, documentation, tested backups, upgrades). An administrator who only reacts stays in the hole, so time must be protected for root-cause fixes.

Skills: technical (TCP/IP, routing and switching, Linux and Windows, DNS and DHCP, storage and backup, scripting), operational (monitoring, change management, capacity planning, disaster recovery), security, human (communication, calm under pressure) and managerial (budget, vendors, SLAs). The method of troubleshooting is define, hypothesise, test, change one thing, verify, document.

Ethics: privileged access makes privacy, integrity, authorised access, least privilege, honesty, competence and legal compliance daily duties, expressed in codes such as SAGE/LOPSA and ACM and in written acceptable-use and privacy policies.

Trends: infrastructure as code, hybrid cloud, DevOps and SRE with SLOs and error budgets, zero trust with MFA, SD-WAN, Wi-Fi 6/7, IPv6, containers and observability.

Conclusion: the tools change, the responsibilities (availability, security, trust) do not.
