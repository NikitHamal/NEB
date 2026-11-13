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
