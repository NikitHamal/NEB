---
subject: Cloud Computing
grade: BCA Semester 8
unit: 1
title: Cloud Foundations, the NIST Model, Service and Deployment Models
hours: 5
area: BCA 451 · Cloud Computing · Unit 1
---

A start-up in Kathmandu launches an app on Friday and by Sunday a festival promotion sends ten times the normal traffic. Buying ten times the servers in advance would have been wasteful; buying too few would have meant a crash. **Cloud computing** removes that dilemma by renting computing as a metered utility, much like electricity from the national grid instead of a private generator. This unit defines the term precisely, introduces the standard models, and quantifies the economic argument for elasticity.

::: key What this unit gives you
- The NIST definition: five essential characteristics, three service models and four deployment models (the "5-4-3" model).
- IaaS, PaaS, SaaS and the commonly added FaaS, with who manages what.
- Private, community, public and hybrid clouds, and multi-cloud.
- A quantitative look at elasticity: why paying for use beats provisioning for peak.
:::

## 1.1 Definition and history

The US National Institute of Standards and Technology (NIST SP 800-145, 2011) defines cloud computing as *a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources (networks, servers, storage, applications and services) that can be rapidly provisioned and released with minimal management effort or service provider interaction.*

The idea grew from time-sharing mainframes in the 1960s, utility-computing proposals, grid computing, the rise of virtualization in the 2000s and the launch of Amazon Web Services in 2006 (S3 and EC2). Today the major providers are Amazon Web Services, Microsoft Azure and Google Cloud, with regional and private players alongside; Nepali organisations typically consume them from the nearest regions in India, Singapore or the Gulf, and a few host in local data centres.

## 1.2 Five essential characteristics

1. **On-demand self-service.** A user provisions resources through a console or API without talking to a human.
2. **Broad network access.** Capabilities are reached over the network by phones, laptops and other clients.
3. **Resource pooling.** The provider serves many tenants from a shared pool, assigning and reassigning resources dynamically (**multi-tenancy**).
4. **Rapid elasticity.** Capacity can scale out and in, often automatically; to the user it appears unlimited.
5. **Measured service.** Usage is metered and billed per unit (per second of compute, per GB-month of storage, per million requests).

::: note
Hosting a single rented server for a year is not necessarily cloud: if there is no self-service, no elasticity and no metering, it is simply traditional hosting. The five characteristics are the test.
:::

## 1.3 Service models

The service models describe how much of the stack the provider manages:

| Layer | On-premises | IaaS | PaaS | FaaS | SaaS |
|---|---|---|---|---|---|
| Application and data | You | You | You | You (function code) | Provider |
| Runtime and middleware | You | You | Provider | Provider | Provider |
| Operating system | You | You | Provider | Provider | Provider |
| Virtualization, servers, storage, network | You | Provider | Provider | Provider | Provider |

- **Infrastructure as a Service (IaaS):** virtual machines, block storage and networks (Amazon EC2, Azure VMs, Google Compute Engine). You manage the operating system and everything above it.
- **Platform as a Service (PaaS):** a managed runtime for your code (Google App Engine, Azure App Service, managed databases). You deploy code and data.
- **Software as a Service (SaaS):** a finished application used through a browser (Gmail, Microsoft 365, Salesforce).
- **Function as a Service (FaaS, serverless):** you upload single functions that run in response to events and are billed per invocation and execution time (AWS Lambda, Azure Functions). It is not one of NIST's three original models but is now standard; Unit 5 treats it in detail.

::: caution
"Serverless" does not mean there are no servers; it means *you do not manage them*. The provider still runs them, and limits such as timeouts and concurrency apply.
:::

## 1.4 Deployment models

- **Public cloud:** owned by a provider and open to the general public.
- **Private cloud:** operated for a single organisation, on or off its premises (a bank's own data centre running cloud software).
- **Community cloud:** shared by organisations with common concerns (for example, several government agencies).
- **Hybrid cloud:** two or more distinct clouds bound by technology that enables data and application portability (a private core system with public burst capacity).
- **Multi-cloud** uses more than one public provider, to avoid lock-in or use the best service of each; it adds operational complexity.

Nepal Rastra Bank and the Nepal Telecommunications Authority have issued guidance touching on data residency and outsourcing for regulated institutions; always check the current directive before placing financial or personal data in a foreign region.

## 1.5 Benefits and risks

**Benefits:** conversion of capital expenditure (CapEx) into operating expenditure (OpEx), speed to market, elasticity, global reach, managed reliability and access to advanced services (analytics, machine learning). **Risks:** vendor lock-in, data-sovereignty and privacy obligations, internet dependence and latency, cost surprises, and the security of the **shared responsibility** boundary (Unit 6).

## 1.6 The economics of elasticity

Consider a service whose demand over one day is: 20 servers for 8 hours, 60 for 4 hours, 100 for 4 hours and 40 for the remaining 8 hours. A traditional data centre must own enough servers for the peak, 100, for all 24 hours. A cloud customer pays only for what runs. At an illustrative price of 10 currency units per server-hour the comparison is a short calculation.

```python
chars = ["on-demand self-service", "broad network access", "resource pooling", "rapid elasticity", "measured service"]
deploy = ["private", "community", "public", "hybrid"]
service = ["IaaS", "PaaS", "SaaS"]
print(f"NIST 5-4-3: {len(chars)} characteristics, {len(deploy)} deployment models, {len(service)} service models")

demand = [20] * 8 + [60] * 4 + [100] * 4 + [40] * 8      # servers needed in each hour of the day
peak, hours = max(demand), len(demand)
server_hours = sum(demand)
utilisation = server_hours / (peak * hours)
print(f"peak {peak}, average {server_hours / hours:.2f}, utilisation {utilisation * 100:.2f}%")
price = 10
fixed, elastic = peak * hours * price, server_hours * price
print(f"fixed cost {fixed}, elastic cost {elastic}, saving {(1 - elastic / fixed) * 100:.2f}%")
```
```output
NIST 5-4-3: 5 characteristics, 4 deployment models, 3 service models
peak 100, average 46.67, utilisation 46.67%
fixed cost 24000, elastic cost 11200, saving 53.33%
```
The workload needs 1,120 server-hours but a peak-sized fleet supplies 2,400, so average utilisation is only 46.67%. Paying per use removes the idle capacity, saving 53.33% in this model. The saving shrinks for flat workloads: if demand were constant at 100, utilisation would be 100% and a fixed fleet could even be cheaper once the cloud's price premium is counted, which is why steady baseline load is often moved to reserved capacity (Unit 7).

::: example Peak-to-average ratio
The ratio of peak to average demand here is 100 ÷ 46.67, about 2.14. The higher this ratio, the stronger the case for elasticity. A tax-filing portal that is busy for two weeks a year might have a ratio above 20.
:::

## 1.7 Cloud architecture at a glance

A provider organises infrastructure into **regions** (geographic areas), each with several **availability zones** (isolated data centres with independent power, cooling and networking, linked by low-latency links) and **edge locations** for content delivery. Customers place resources by region for latency and legal reasons, and across zones for resilience; Unit 7 shows the availability arithmetic.

## 1.8 Seeing the ideas: the physical cloud, the NIST model and who manages what

The word "cloud" hides very real machinery. Plate 1.1 shows three physical faces of it: a data-centre aisle full of fan-cooled servers, the silicon die of a server processor, and a household electricity meter, the oldest example of metered utility that cloud billing copies.

```photogrid label="1.1" cols="3" ratio="1.1" caption="The cloud is physical and metered. (a) An aisle of a hyperscale data centre: thousands of identical, fan-cooled servers in racks. (b) The die of a 22-core Intel Xeon server processor (Broadwell-EP): cores, cache and memory controllers in one chip, the unit that virtualisation slices into virtual CPUs. (c) A single-phase electricity meter in a South-East Asian home: you pay for the kilowatt-hours you use, the model that cloud billing copies for CPU-hours and gigabyte-months."
@ photo id="bca451/facebook" cap="Data-centre server aisle"
fit 1.1
focus 0.5 0.5
@ photo id="bca451/xeon" cap="Server processor die"
fit 1.1
focus 0.5 0.5
@ photo id="bca451/meter" cap="Metered utility"
fit 1.1
focus 0.5 0.6
```

```svgfig label="1.1" caption="The NIST cloud model, the 5-4-3 picture. Five essential characteristics describe how the service behaves, three service models describe what is delivered, and four deployment models describe who owns and shares the infrastructure."
f = Fig(580, 250)
f.box(8, 8, 564, 30, "NIST SP 800-145 cloud model", fill=NAVY, stroke=NAVY, color="#ffffff", bold=True, size=12)
f.text(290, 58, "5 essential characteristics", size=11, color=TEAL, bold=True)
C = ["On-demand\nself-service", "Broad network\naccess", "Resource\npooling", "Rapid\nelasticity", "Measured\nservice"]
for i, t in enumerate(C):
    f.box(8 + i * 114, 66, 106, 40, t, fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.text(290, 126, "3 service models", size=11, color=NAVY, bold=True)
for i, (t, s) in enumerate([("IaaS", "VMs, disks, networks"), ("PaaS", "runtime, database, tools"), ("SaaS", "finished application")]):
    f.box(8 + i * 192, 134, 180, 40, t + "\n" + s, fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.text(290, 194, "4 deployment models", size=11, color=RED, bold=True)
for i, (t, s) in enumerate([("Private", "one organisation"), ("Community", "shared by a group"), ("Public", "open to everyone"), ("Hybrid", "private + public linked")]):
    f.box(8 + i * 144, 202, 136, 40, t + "\n" + s, fill=ROSE, stroke=RED, size=10.5, bold=True)
```

```svgfig label="1.2" caption="Who manages what. Green layers are managed by the customer, grey layers by the provider. Moving from on-premises to IaaS, PaaS and SaaS shifts more of the stack to the provider, so the customer gives up control and gains speed and lower effort."
f = Fig(580, 262)
L = ["Application", "Data", "Runtime", "Middleware", "Operating system", "Virtualisation", "Servers", "Storage", "Networking"]
cols = [("On-premises", 9), ("IaaS", 5), ("PaaS", 2), ("SaaS", 0)]
f.box(8, 8, 110, 22, "Layer", fill=NAVY, stroke=NAVY, color="#ffffff", bold=True, size=10.5)
for j, (n, k) in enumerate(cols):
    x = 126 + j * 112
    f.box(x, 8, 104, 22, n, fill=NAVY, stroke=NAVY, color="#ffffff", bold=True, size=10.5)
    for i in range(9):
        y = 34 + i * 24
        mine = i < k
        f.box(x, y, 104, 21, "You" if mine else "Provider", fill=MINT if mine else "#e2e8f0", stroke=TEAL if mine else SLATE, size=9.5)
for i, t in enumerate(L):
    f.box(8, 34 + i * 24, 110, 21, t, fill=BLUE, stroke=NAVY, size=9.5)
f.text(290, 256, "Examples: IaaS = EC2, Compute Engine | PaaS = App Engine, Heroku | SaaS = Gmail, Office 365", size=9.5, color=SLATE)
```

```svgfig label="1.3" caption="Why elasticity saves money. Demand (blue) follows a daily pattern with a festival spike. A fixed fleet sized for the peak (red dashed line) is mostly idle; an elastic fleet (teal steps) follows demand and the shaded gap is the money wasted by a fixed purchase."
f = Fig(580, 230)
ax = Axes(f, 50, 16, 510, 160, (0, 24), (0, 60))
ax.grid(4, 10)
ax.axes("", "")
import math
dem = lambda t: 8 + 12 * max(0, math.sin((t - 6) * math.pi / 14)) + (30 if 18 <= t <= 21 else 0)
ax.area(dem, 0, 24, fn2=lambda t: 0)
ax.hline(50, color=RED)
for h in range(24):
    f.raw('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="%s" stroke-width="1.6"/>' % (ax.X(h), ax.Y(math.ceil(dem(h + 0.5) / 5) * 5), ax.X(1) - ax.X(0), ax.Y(0) - ax.Y(math.ceil(dem(h + 0.5) / 5) * 5), TEAL))
ax.curve(dem, 0, 24, color=NAVY)
f.text(300, 198, "hour of the day", size=10.5, color=SLATE)
f.text(18, 96, "servers", size=10, color=SLATE)
f.text(150, 28, "fixed fleet = 50 servers all day", size=10, color=RED, bold=True)
f.text(445, 120, "festival\npromotion", size=10, color=NAVY, bold=True)
f.text(290, 220, "Fixed: 50 x 24 = 1,200 server-hours | Elastic: 430 server-hours | saving 64%", size=10.5, color=TEAL, bold=True)
```

### 1.8.1 Eight benefits of cloud computing for Nepali organisations

1. **Pay only for what you use.** Cloud turns a large up-front purchase (CapEx) into a monthly bill (OpEx). A start-up in Lalitpur can launch with a few hundred rupees of spending a day instead of buying servers worth lakhs. If the product fails, the bill stops.
2. **Elastic capacity for sudden demand.** Servers can be added in minutes and removed afterwards. A ticket site for a Dashain concert or an exam-result portal on the day of publication can scale up for a few hours. The same fixed server would crash at the peak and sit idle on other days.
3. **Fast start.** A virtual machine is ready in about a minute, while buying a physical server takes weeks of quotation, import and installation. Students and developers can test an idea on the same afternoon. Speed is often the biggest business benefit.
4. **No hardware maintenance.** The provider replaces failed disks, fans and power supplies. A small company in Biratnagar does not need a server room, a generator and a night engineer. Its staff can focus on the product.
5. **High availability and disaster recovery.** Data can be copied across availability zones and regions. A fire, flood or earthquake that damages one building does not destroy the service. This is valuable in a country with landslide, monsoon and earthquake risk.
6. **Access from anywhere.** Services are reached through the internet from a laptop, tablet or phone. A team split between Kathmandu and Pokhara, or a Nepali developer working for a foreign client, shares the same system. Remote work and online classes depend on this.
7. **Strong security tools are available.** Providers offer encryption, identity management, firewalls and audit logs that a small firm could not build alone. They also hold certifications such as ISO 27001. The customer must still configure them correctly, because the responsibility is shared.
8. **Access to modern services.** Machine learning, big-data analytics, managed databases and content delivery are rented by the hour. A college can run an AI project on a rented GPU instead of buying one. This brings advanced technology within the budget of ordinary Nepali organisations.

## 1.9 Summary and exercises

Cloud computing delivers metered, elastic, self-service computing from pooled resources; the NIST model organises it into five characteristics, three service models and four deployment models, and the economics rest on matching capacity to demand.

1. State the five NIST characteristics, and explain why a fixed rented server fails the test.
2. Draw a responsibility table for IaaS, PaaS and SaaS and give one product for each.
3. Distinguish hybrid cloud from multi-cloud.
4. Demand is 10 servers for 12 hours and 50 for 12 hours. Compute utilisation of a peak-sized fleet and the percentage saved by elastic billing.
5. Explain CapEx versus OpEx with an example of a Nepali company moving its email to SaaS.
6. List three risks of public cloud for a regulated bank and one mitigation for each.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the five essential characteristics of cloud computing as defined by NIST.**

*Introduction.* The US National Institute of Standards and Technology (NIST SP 800-145) says a service is cloud computing only if it shows five characteristics (Figure 1.1). A fixed server rented for a year shows none of the elastic ones, so it is hosting, not cloud.

1. **On-demand self-service.** The customer provisions servers or storage through a web console or API without talking to a salesperson.
2. **Broad network access.** Services are available over the network through standard clients such as browsers, phones and laptops.
3. **Resource pooling.** The provider serves many customers from a shared pool of hardware (multi-tenancy), and the customer usually does not know the exact machine.
4. **Rapid elasticity.** Capacity grows and shrinks quickly, often automatically, so it seems unlimited to the customer (Figure 1.3).
5. **Measured service.** Usage of CPU, storage and bandwidth is metered and billed, like the electricity meter in Plate 1.1(c).

*Example.* A Nepali bank that rents virtual machines by the hour, scales them on salary day and receives a monthly itemised bill is using all five. *Conclusion:* these five properties separate cloud from ordinary hosting and explain its economics.

**Q2 (5 marks). Distinguish IaaS, PaaS and SaaS with examples and say who manages which layer.**

| Point | IaaS | PaaS | SaaS |
|---|---|---|---|
| Delivers | Virtual machines, storage, networks | Runtime, database, deployment tools | Finished application |
| Customer manages | OS, middleware, runtime, app, data | Application and data | Only settings and data |
| Provider manages | Hardware, virtualisation | Everything up to the runtime | Everything |
| Control / effort | Highest control, highest effort | Medium | Lowest control, lowest effort |
| Examples | Amazon EC2, Google Compute Engine | Google App Engine, Heroku | Gmail, Office 365, Zoom |
| Typical user | System administrator | Developer | End user |

Figure 1.2 shows the shifting boundary: each step to the right hands another layer to the provider. *Nepali example:* a college that runs its own Moodle on a rented VM uses IaaS; if it deploys its portal code on a managed platform it uses PaaS; if it adopts Google Workspace for email it uses SaaS. *Conclusion:* choose the highest service model that still meets the need for control.

**Q3 (10 marks). Define cloud computing. Explain its service and deployment models, and discuss the benefits and risks of moving an organisation to the public cloud.**

*Introduction.* **Cloud computing** is a model for enabling convenient, on-demand network access to a shared pool of configurable computing resources (servers, storage, networks, applications) that can be rapidly provisioned and released with minimal management effort. Behind the word sits the physical infrastructure of Plate 1.1: large data centres of racked servers, sold as a metered utility.

*Architecture and models.* NIST describes it by five characteristics, three service models and four deployment models (Figure 1.1). The **service models** are IaaS (virtual machines and disks), PaaS (a ready platform for code) and SaaS (a finished application), with the responsibility split of Figure 1.2. The **deployment models** are private (one organisation, higher control and cost), community (shared by organisations with common needs, for example several banks), public (open to anyone, lowest cost per unit) and hybrid (private and public linked, for example sensitive records on a private cloud and a web front end on a public one).

*Benefits.* (1) Pay-as-you-use billing converts CapEx to OpEx. (2) Elasticity matches capacity to demand; in Figure 1.3 a fixed fleet of 50 servers is idle most of the day. (3) Quick provisioning shortens time to market. (4) No hardware maintenance. (5) Built-in redundancy across zones. (6) Access from anywhere. (7) Managed security tools. (8) Modern services such as analytics and AI.

*Risks.* (1) Data protection and legal control: data may sit in another country, which matters for banks regulated by Nepal Rastra Bank. (2) Vendor lock-in through proprietary services. (3) Internet dependence: a failed link stops work. (4) Misconfiguration, such as a public storage bucket. (5) Cost surprises if usage is not watched. (6) Shared-responsibility confusion. Each risk has a control: encryption and key ownership, open standards and containers, redundant links, configuration scanning, budgets and alerts, and a clear responsibility matrix.

*Worked example.* Demand is 10 servers for 12 hours and 50 for 12 hours. A peak-sized fleet is paid for 50 x 24 = 1,200 server-hours but used for 10 x 12 + 50 x 12 = 720, so utilisation is 60%. Elastic billing pays for 720, a saving of 480/1,200 = 40%.

| Aspect | Own data centre | Public cloud |
|---|---|---|
| Cost pattern | Large CapEx | Monthly OpEx |
| Capacity | Fixed, bought for peak | Elastic |
| Time to start | Weeks to months | Minutes |
| Control | Full | Shared |
| Staff burden | Heavy | Light |

*Conclusion.* Cloud computing is metered, elastic, self-service computing from pooled resources. For most Nepali start-ups, colleges and businesses the benefits outweigh the risks, provided data classification, key management and cost monitoring are in place; regulated data may favour a hybrid design.
