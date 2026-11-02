---
subject: Cloud Computing
grade: BCA Semester 8
unit: 7
title: Cloud Economics, SLA Mathematics and FinOps
hours: 7
area: BCA 451 · Cloud Computing · Unit 7
---

A cloud bill has two surprises waiting for the unprepared. The first is availability: a provider promises 99.9% for each service, yet an application built from five of them is *less* available than any single one. The second is cost: the same virtual machine can cost three different prices depending on how you commit to it. Both surprises are arithmetic, and this unit teaches the calculations that turn them into design decisions.

::: key What this unit gives you
- Pricing models and total cost of ownership; what drives a cloud bill.
- SLI, SLO and SLA, and the arithmetic of "nines": downtime per year.
- Composite availability: serial chains lower it, parallel redundancy raises it.
- FinOps and the reserved versus on-demand break-even.
:::

## 7.1 Pricing models

- **On-demand:** pay per second or hour with no commitment; the highest unit price and the most flexible.
- **Reserved instances and savings plans:** commit to a one- or three-year level of usage in exchange for a discount (often 30% to 70%). You pay whether or not you use it.
- **Spot (preemptible) capacity:** spare capacity at deep discounts that the provider can reclaim on short notice; suited to fault-tolerant batch work.
- **Free tiers and credits:** limited monthly usage at no cost, useful for learning but easily exceeded.
- **Other cost drivers:** storage per GB-month, requests, **data egress** (traffic leaving the provider, usually charged; traffic in is generally free), cross-zone and cross-region transfers, managed-service premiums, support plans and licences.

Prices change frequently and differ by region, so the figures below are illustrative. Organisations in Nepal paying a foreign provider should also account for exchange rates and the rules for international payments; check the current Nepal Rastra Bank provisions.

## 7.2 Total cost of ownership

**TCO** compares the full cost of running a workload on-premises (hardware, space, power, cooling, network, licences, staff, refresh cycles and idle capacity) with the cloud (usage charges, migration, training, egress and the cost of re-architecture). A fair comparison includes utilisation: servers bought for peak (Unit 1) sit mostly idle. Cloud is not automatically cheaper; it is cheaper when demand varies, when time to market matters or when capital is scarce, and it can be dearer for steady, predictable, high-volume workloads such as large always-on storage with heavy egress.

## 7.3 SLI, SLO and SLA

An **SLI** (service level indicator) is a measurement such as the fraction of successful requests. An **SLO** (objective) is the internal target for the SLI, say 99.95% over 30 days. An **SLA** (agreement) is the contract with the customer, with a remedy if the provider misses it. The remedy is usually a **service credit** on the next bill, not compensation for your lost business. The allowed failure, 100% − SLO, is the **error budget**, which teams "spend" on releases and experiments.

Availability is the fraction of time a service works: A = MTBF ÷ (MTBF + MTTR). Downtime per year is (1 − A) × 525,600 minutes (a 365-day year).

```python
yr = 365 * 24 * 60                      # minutes in a year
for pct, a in (("99", 0.99), ("99.9", 0.999), ("99.99", 0.9999), ("99.999", 0.99999)):
    print(f"{pct}%: {(1 - a) * yr:.1f} min/year")
```
```output
99%: 5256.0 min/year
99.9%: 525.6 min/year
99.99%: 52.6 min/year
99.999%: 5.3 min/year
```
Each extra nine cuts downtime tenfold: 99% allows about 87.6 hours a year, 99.9% allows 525.6 minutes (8.76 hours), 99.99% about 52.6 minutes and 99.999% only about 5.3 minutes. Each additional nine usually costs far more engineering effort than the last.

## 7.4 Composite availability

When a request needs every component, they are in **series** and the system works only if all do: **A = A₁ × A₂ × … × Aₙ**. Availability can only fall as you add serial dependencies. When redundant components can each serve the request, they are in **parallel** and the system fails only if all fail: **A = 1 − (1 − A₁)(1 − A₂) … (1 − Aₙ)**.

The example is a three-tier application: a web tier of 99.95%, an application tier of 99.9% and a database tier of 99.95%.

```python
yr = 365 * 24 * 60
def serial(*a):
    out = 1.0
    for x in a:
        out *= x
    return out
def parallel(*a):
    out = 1.0
    for x in a:
        out *= 1 - x
    return 1 - out

web, app, db = 0.9995, 0.999, 0.9995
s = serial(web, app, db)
print(f"serial web x app x db: {s * 100:.4f}% ({(1 - s) * yr:.1f} min/year)")
p = parallel(0.999, 0.999)
print(f"two parallel 99.9% instances: {p * 100:.4f}% ({(1 - p) * yr:.1f} min/year)")
r = serial(parallel(web, web), parallel(app, app), parallel(db, db))
print(f"redundant tiers (2 per tier): {r * 100:.5f}% ({(1 - r) * yr:.2f} min/year)")
```
```output
serial web x app x db: 99.8001% (1050.5 min/year)
two parallel 99.9% instances: 99.9999% (0.5 min/year)
redundant tiers (2 per tier): 99.99985% (0.79 min/year)
```
The serial chain is 99.8001%, worse than the weakest tier alone, with about 1,050 minutes (17.5 hours) of expected downtime a year. Two parallel 99.9% instances give 99.9999%, which is six nines: about half a minute of downtime a year. Duplicating each tier in a second availability zone lifts the whole application to 99.99985%, under one minute a year in this idealised model.

::: caution
The parallel formula assumes **independent** failures. Two instances in the same rack, behind the same load balancer or sharing the same database are *not* independent, and a shared dependency stays in series. Real designs find and remove the single points of failure (the database, the DNS, the deployment pipeline) rather than merely adding replicas, and they test failover regularly.
:::

A provider's SLA for one service says nothing about your end-to-end availability: it must be composed with the SLAs of every dependency, and cloud SLAs are measured on the provider's own definitions of "unavailable" with claims windows and exclusions.

## 7.5 Reserved versus on-demand: break-even

Suppose an instance costs 0.10 per hour on demand, and a one-year commitment costs an effective 0.06 per hour *for every hour of the year*, used or not. The commitment pays off if you would run the instance for more than 0.06 ÷ 0.10 = 60% of the time. With an all-upfront reservation of 500 for the year, the break-even is 500 ÷ 0.10 = 5,000 hours.

```python
od, reserved, hours_year = 0.10, 0.06, 8760
be = reserved / od
print(f"break-even utilisation {be * 100:.1f}% = {be * hours_year:.0f} h/year")
upfront = 500
be2 = upfront / od
print(f"all-upfront break-even {be2:.0f} h = {be2 / hours_year * 100:.2f}%")
used = 6000
a, b = used * od, hours_year * reserved
print(f"{used} h/year: on-demand {a:.2f} vs reserved {b:.2f}, saving {a - b:.2f} ({(a - b) / a * 100:.2f}%)")
```
```output
break-even utilisation 60.0% = 5256 h/year
all-upfront break-even 5000 h = 57.08%
6000 h/year: on-demand 600.00 vs reserved 525.60, saving 74.40 (12.40%)
```
The hourly commitment breaks even at 60% utilisation, which is 5,256 hours a year; the all-upfront plan breaks even at 5,000 hours, or 57.08%. A workload running 6,000 hours a year (68% of the time) saves 74.40, or 12.40%, by reserving. The same workload at 4,000 hours would *lose* money by reserving, because the idle hours are still paid for. The practical rule is to reserve the steady **baseline**, buy the variable part on demand, and run interruptible work on spot.

## 7.6 FinOps

**FinOps** is the practice of bringing financial accountability to the variable spend of the cloud, through cooperation between engineering, finance and the business. The FinOps Foundation describes a repeating cycle:

1. **Inform:** make costs visible. Use **tagging** (team, project, environment), cost allocation, dashboards and budgets with alerts.
2. **Optimise:** *rightsize* oversized instances, delete idle resources and unattached volumes, switch storage to colder tiers, use commitments for the baseline and spot for flexible jobs, shut down non-production environments outside working hours, and cut egress with caching (Unit 4).
3. **Operate:** make cost a routine engineering metric, such as cost per transaction or per customer, reviewed regularly, with anomaly detection to catch runaway usage.

::: example Cost per transaction
A service costs Rs 9,00,000 a month and handles 30 million requests: Rs 0.03 per request. After rightsizing, the bill falls to Rs 7,20,000 while traffic grows to 36 million: Rs 0.02 per request. The total fell 20% and the unit cost fell 33%, the number that shows efficiency rather than mere shrinkage.
:::

## 7.7 Summary and exercises

Cloud cost depends on the pricing model and utilisation; SLA nines translate to minutes of downtime; serial dependencies lower and parallel replicas raise availability; commitments pay off above a break-even utilisation; FinOps makes this a continuous practice.

1. Compute the yearly downtime for 99.95% availability.
2. Three services in series have 99.9%, 99.5% and 99.99%. Find the composite availability.
3. Two independent instances of 99.5% are run in parallel behind a 99.99% load balancer. Compute the availability.
4. Instance A costs 0.20 per hour on demand or 0.11 per hour reserved for all 8,760 hours. What is the break-even utilisation?
5. Explain why egress charges can dominate the bill of a video-streaming service.
6. Describe two FinOps actions for each of the Inform, Optimise and Operate phases.
