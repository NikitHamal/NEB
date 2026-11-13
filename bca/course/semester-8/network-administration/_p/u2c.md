## 2.3 Services

### 2.3.1 What a service is

A **service** is something the customer values: "e-mail that works", "the college website", "a printer queue", "a login that follows me from lab to lab". It is more than the server that runs it. A service includes the **software, the hardware, the network paths, the data, the monitoring, the backup, the documentation, the support procedure and the people who run it**. One service often depends on others: mail needs DNS, authentication, storage and the network. A service that works on the day it launches but cannot be monitored, backed up or upgraded is half a service.

```svgfig label="2.2" caption="The life cycle of a service: each stage has its own checklist, and the cycle repeats at every major upgrade."
f = Fig(660, 210)
f.box(15, 70, 100, 50, "Requirements\nwith customers", fill=SAND, stroke=AMBER, size=10)
f.box(140, 70, 100, 50, "Plan and\nengineer", fill=BLUE, stroke=NAVY, size=10)
f.box(265, 70, 100, 50, "Launch\n(pilot, roll-out)", fill=BLUE, stroke=NAVY, size=10)
f.box(390, 70, 100, 50, "Operate and\nmonitor", fill=BLUE, stroke=NAVY, size=10)
f.box(515, 70, 130, 50, "Upgrade, convert\nor retire", fill=SOFT, stroke=SLATE, size=10)
for x in (115, 240, 365, 490):
    f.arrow([(x, 95), (x + 25, 95)], color=NAVY)
f.arrow([(580, 120), (580, 170), (65, 170), (65, 120)], color=SLATE, dash=True, label="next generation of the service", lpos=(320, 185))
f.text(190, 40, "SLA written here", size=9, color=SLATE)
f.text(440, 40, "SLO, alarms, backups", size=9, color=SLATE)
```

### 2.3.2 Requirements

Planning starts by asking the **customers** (not only the managers) what they need. Convert wishes into requirements that can be tested.

| Category | Questions | Example for a college mail service |
|---|---|---|
| **Functional** | What must it do? | Send and receive mail for 2,500 users; 5 GB mailbox; calendar; mobile access |
| **Availability** | When must it be up? How much downtime is tolerable? | 99.9% during 7 a.m. to 9 p.m.; planned maintenance Saturday night |
| **Performance** | How fast, for how many? | Mail delivered inside 1 minute; 300 simultaneous users at peak |
| **Capacity and growth** | How much, growing how fast? | 20% growth per year in mailbox storage |
| **Security and privacy** | Who may access what? | MFA for staff; encrypted connections; spam and malware filtering |
| **Support** | Who helps, how fast? | Help desk replies in 1 hour; urgent issues 24 x 7 |
| **Compliance and retention** | What must be kept and for how long? | Mail kept two years; deleted mail recoverable for 30 days |
| **Budget** | One-off and running cost? | Within the approved budget, with licences counted |

The agreed list becomes a **service-level agreement (SLA)**: a document between the service owner and the customers that states what is promised (availability, response times, support hours), how it is measured and what happens if it is not met. Inside the IT team the measurable targets are **service-level objectives (SLOs)**; the SLA is usually looser than the SLO so that the team has room to fix problems before breaking a promise.

### 2.3.3 Planning and engineering

**Design principles.**

- **Simplicity**: choose the simplest design that meets the requirements; a design that one person can explain on a whiteboard can be repaired at 3 a.m.
- **Standard components**: use supported, widely used products so that documentation and engineers are easy to find.
- **Machine independence**: clients should refer to the service by a **DNS alias** (`mail.college.edu.np`), never by the server's own name or address, so that the service can be moved to new hardware without touching a single client.
- **Restrict access**: only the people and machines that need to reach the service can reach it (firewalls, VLANs, accounts).
- **Separate the environments**: a **test** and a **production** copy, so that the change is first tried where failure does no harm.
- **Redundancy where it pays**: remove single points of failure for critical services.

**Redundancy and availability.** The availability of a component is **A = MTBF / (MTBF + MTTR)**, where MTBF is the mean time between failures and MTTR the mean time to repair. When components are chained so that **all** must work (a **series** system), availabilities multiply and the whole is *worse* than its weakest part. When identical components are **in parallel** so that **any one** is enough, unavailabilities multiply and the whole is *better*.

```python
# Availability: series and parallel
def avail(mtbf, mttr): return mtbf / (mtbf + mttr)

web  = avail(2000, 4)       # hours
db   = avail(3000, 8)
net  = 0.9995
print("web %.5f  db %.5f  net %.5f" % (web, db, net))
series = web * db * net
print("series (all needed)      : %.5f  -> %.1f h down per year" % (series, (1 - series) * 8760))

# two identical web servers behind a load balancer (either is enough)
web2 = 1 - (1 - web) ** 2
series2 = web2 * db * net
print("web pair A               : %.7f" % web2)
print("with redundant web tier  : %.5f  -> %.1f h down per year" % (series2, (1 - series2) * 8760))

# N+1: eight servers needed at peak, plus one spare; each 99% available
from math import comb
a, n = 0.99, 9
p_ok = sum(comb(n, k) * a**k * (1 - a)**(n - k) for k in range(8, n + 1))
print("N+1 (need 8 of 9)        : %.5f" % p_ok)
print("no spare (need 8 of 8)   : %.5f" % (a ** 8))
```

Read the result carefully. Redundancy at the web tier improves the whole only until the next weakest link (the database or network) dominates, so effort is best spent on the **least available component**. **N+1** means having one more unit than the load needs, so that one failure does not reduce service; for a service where the loss of two units is unacceptable use N+2.

**Capacity planning.** Estimate the peak load, add growth and headroom, and check each resource (CPU, memory, disk, network). A simple model: if requests arrive at rate λ and a server finishes them at rate μ, utilisation is ρ = λ/μ and the average time in the system for a single queue is 1/(μ - λ) (the M/M/1 model). The delay explodes as utilisation approaches 100%, so aim for 60-70% at peak.

```python
mu = 100.0                         # requests the server can finish per second
for lam in (50, 70, 80, 90, 95, 99):
    rho = lam / mu
    resp_ms = 1000 / (mu - lam)    # M/M/1 average time in system
    print("load %2d%%  average response %6.1f ms" % (lam, resp_ms))

# growth: storage need in 3 years with 20% yearly growth from 4 TB, keep 30% free
need = 4 * 1.2 ** 3
print("storage after 3 years: %.2f TB; buy %.2f TB for 30%% free space" % (need, need / 0.7))
```

**Dependencies and failure modes.** Draw what the service depends on (DNS, authentication, network, power, storage, licence server) and what depends on it. In an outage, the dependency chain explains why "mail is down" may be a DNS fault, and in a plan it shows which dependency needs redundancy first.

### 2.3.4 Service launch

Launching a service is a controlled change, not a switch-on. The prescribed text recommends a **launch readiness review**, a checklist that must be passed before customers use the service:

1. **Requirements met** and demonstrated in a test.
2. **Monitoring in place**: alarms for the service, not only for the server; alarms reach a person.
3. **Backup and restore tested**, not only configured.
4. **Documentation**: how to operate, start, stop, upgrade and recover; who to call.
5. **Security reviewed**: patched, firewall rules, accounts, encryption.
6. **Capacity checked** against a load test.
7. **Support ready**: the help desk has been trained and has a script for the common questions.
8. **Communication**: customers know the date, what changes for them and where to ask for help.

The **roll-out** itself should be gradual: first an **internal pilot** with the IT staff, then a small group of friendly customers (a **beta**), then the department-by-department or percentage roll-out. At every step decide a **rollback**: how to return to the previous state if the launch fails. A launch on the first day of an examination week is a bad idea; choose a quiet period and avoid Fridays, because a failure over a weekend finds nobody at the office.

### 2.3.5 Disaster recovery

A **disaster** is any event that stops a service for far longer than normal faults do: fire, flood, earthquake (a real planning input in Nepal), power failure, ransomware, theft, a destroyed disk array, a fatal human mistake. **Disaster recovery (DR)** is the plan that restores the service; **business continuity** is the wider plan for the organisation to keep working in the meantime.

**Steps in DR planning.**

1. **Risk analysis**: list possible disasters, their likelihood and their impact; decide which services matter most.
2. **Set the objectives** for each service:
   - **RTO (recovery time objective)**: how long the service may be down.
   - **RPO (recovery point objective)**: how much recent data may be lost, measured in time. An RPO of 1 hour means the backups or replication must be at most an hour old.
3. **Choose the strategy** that meets RTO and RPO within budget.
4. **Write the plan**: ordered steps, contacts, passwords stored securely and offline, where the backup tapes or copies are, and who decides.
5. **Test the plan** at least yearly, by a real restore or a drill. A DR plan that has not been tested is only a hope.

| Recovery site | Description | Recovery time | Cost |
|---|---|---|---|
| **Cold site** | Empty room with power and network; hardware must be brought and set up | Days to weeks | Low |
| **Warm site** | Hardware installed, data restored from the latest backup | Hours to a day | Medium |
| **Hot site** | Fully equipped and continuously replicated copy, ready to take over | Minutes | High |
| **Cloud DR** | Copy of the service in the cloud, started on demand | Minutes to hours | Pay for use |

**Data protection basics.** Follow the **3-2-1 rule**: keep **three** copies of important data, on **two** different kinds of media, with **one** copy off-site (and, today, one that cannot be changed, **immutable**, against ransomware). Offsite does not mean the next room: choose a different building, or a cloud region far from the first site.

```python
# Does a chosen strategy meet the objectives?  (illustrative numbers)
services = {
  "Fee portal":  dict(rto_h=2,  rpo_h=1,  backup_every_h=24,  restore_h=3),
  "Website":     dict(rto_h=24, rpo_h=24, backup_every_h=24,  restore_h=2),
  "Mail":        dict(rto_h=8,  rpo_h=4,  backup_every_h=4,   restore_h=6),
}
for name, s in services.items():
    ok_rpo = s["backup_every_h"] <= s["rpo_h"]
    ok_rto = s["restore_h"] <= s["rto_h"]
    print("%-11s RPO %-4s RTO %-4s" % (name, "ok" if ok_rpo else "FAIL", "ok" if ok_rto else "FAIL"))
```

The fee portal fails both objectives with a nightly backup and a three-hour restore: it needs frequent log shipping or replication and a faster recovery path, a clear example of why objectives come before products.

## 2.4 Summary and exercises

Manage workstations as a fleet: few models, a standard image, data on servers, a refresh cycle of three to five years, installation by PXE and answer files, and central configuration and patching. A server is built for many users and for uptime: ECC memory, hot-swap disks with the right RAID level (RAID is not backup), redundant power, remote management, racks and enough power and cooling, and it is installed minimally and hardened. A service is the whole delivered thing: gather requirements and write an SLA, plan with simplicity, DNS aliases, test and production separation, redundancy (series and parallel availability, N+1) and capacity (keep utilisation near 60-70%), pass a launch readiness review and roll out in stages, and prepare disaster recovery with RTO, RPO, a chosen site type, the 3-2-1 backup rule and regular tests.

1. Why is the cost of a workstation more than its purchase price? How does standardisation reduce it?
2. Compare thick client, thin client and virtual desktop architectures.
3. Explain the three tasks of workstation management (load, configure, update).
4. Discuss the hardware strategy for a fleet of 100 PCs, including refresh cycle, spares and warranty.
5. Describe PXE network installation. What are the roles of DHCP, TFTP, the answer file and the package mirror?
6. Differentiate a server and a workstation. Why should a service not run on a workstation?
7. List and explain eight features to examine in a server specification.
8. Compare RAID 0, 1, 5, 6 and 10 for capacity and fault tolerance. Why is RAID not a backup?
9. What is virtualisation? State two benefits and two risks of server consolidation.
10. List the steps to harden a new Linux server.
11. Define service, SLA and SLO. What should be asked of customers when gathering requirements?
12. State the design principles for a service. Why use a DNS alias for the service name?
13. Define availability. Compute the availability of a chain of three components of 99.9% each, and of two 99% components in parallel.
14. What is a launch readiness review? List its items and the stages of a roll-out.
15. Define disaster recovery, RTO and RPO. Compare cold, warm and hot sites. State the 3-2-1 rule.
16. Eight 2 TB disks are used in RAID 6. How much space is usable? A UPS must carry 6 servers of 350 W for 10 minutes: estimate the load and the battery energy.

**Answers to the numerical items.** (13) Series: 0.999^3 = 0.997003, about 99.70%; parallel: 1 - 0.01^2 = 0.9999, 99.99%. (16) RAID 6 usable = (8 - 2) x 2 = 12 TB. Load = 6 x 350 = 2,100 W; energy for 10 minutes = 2,100 x 10/60 = 350 Wh; allowing 90% efficiency, about 389 Wh, and the rating in VA is 2,100 / 0.9 = 2,333 VA before headroom.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain PXE network installation of workstations.**

PXE lets a computer with no operating system install itself over the network. The firmware sends a DHCP request; the DHCP server replies with an address and the name of a boot server and boot file. The client downloads a boot loader over TFTP or HTTP, which loads a kernel and an answer file (kickstart for Red Hat family, autoinstall or preseed for Ubuntu and Debian, unattend.xml with Windows Deployment Services). The installer then reads the packages from a mirror over HTTP, NFS or SMB and installs without questions. Advantages: no USB sticks, same installation on every machine, any hardware, easy re-installation; after installation a configuration-management tool applies the remaining settings.

**Q2 (5 marks). What are RTO and RPO? How do they influence the backup design?**

RTO is the longest time a service may be down; RPO is the largest amount of recent data, measured in time, that may be lost. A nightly backup gives an RPO of up to 24 hours, so a service with an RPO of one hour needs more frequent backups, log shipping or replication. A restore that takes six hours cannot meet an RTO of two hours, so a standby or replicated copy is needed. The objectives, set with the business, are fixed first; the technology and the cost follow from them.

**Q3 (10 marks). Describe how a new e-mail service for a college is planned and launched.**

Requirements: ask staff, students and managers; list functions (2,500 mailboxes, 5 GB, calendar, mobile), availability (99.9% in working hours), performance, growth (20% a year), security (MFA, TLS, spam and malware filtering), support and retention; write them as an SLA with measurable SLOs.

Planning and engineering: choose a simple, supported design; reach it by a DNS alias such as mail.college.edu.np; separate test from production; use redundancy where the availability arithmetic shows a weak link (a second mail gateway, mirrored disks); plan capacity from users, mailbox size and 20% growth with 30% free space; list dependencies (DNS, directory, storage, network, power).

Launch: pass a readiness review (requirements tested, monitoring and alarms, backup and a trial restore, documentation, security review, load test, trained help desk, announcement). Roll out through an IT pilot, a beta group and then departments, with a rollback plan, avoiding examination weeks and Fridays.

Operation and disaster recovery: choose RTO and RPO, apply the 3-2-1 rule with an off-site immutable copy, test a restore each term, and review capacity and SLOs regularly.
