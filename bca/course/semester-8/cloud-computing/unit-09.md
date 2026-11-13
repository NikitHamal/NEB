---
subject: Cloud Computing
grade: BCA Semester 8
unit: 9
title: Service-Oriented Architecture, Cloud Platforms, Applications and Security Practice
hours: 12
area: BCA 451 · Cloud Computing · Unit 9
---

The last unit of the TU outline moves from mechanisms to **platforms and practice**: how cloud systems are designed with service-oriented architecture (SOA) and web services, what the main platform services (Google App Engine, Microsoft Azure, Aneka) offer, which scientific, business and consumer applications run on them, and how security, trust and privacy are handled in daily operation (SaaS, application, virtual machine and data security, monitoring and identity). Units 1 to 7 gave the mechanisms; this unit connects them to what an organisation actually buys and runs.

::: key What this unit gives you
- SOA principles, web services (SOAP, WSDL, UDDI and REST) and how SOA relates to microservices and the cloud reference model.
- Cloud platforms: Google App Engine, Microsoft Azure and Aneka, compared by service model, programming model and scaling.
- Cloud applications: scientific (health, biology, geoscience), business (CRM, ERP, productivity) and consumer (storage, media, gaming).
- SaaS, application, VM and data security, security monitoring and security architecture, trust and privacy; open challenges and cloud adoption steps.
:::

## 9.1 Cloud design and implementation using SOA

**Service-oriented architecture (SOA)** is a way of building software as a set of **services**: self-contained units of business functionality (check a customer, convert a currency, send an SMS) that other programs call over a network through a published interface, without knowing how they are implemented. Cloud computing is the delivery model; SOA is the design style that fits it, because both treat capability as a *service reached through a standard interface*. IaaS, PaaS and SaaS are themselves service layers.

### SOA principles

| Principle | Meaning | Example |
|---|---|---|
| **Standardised service contract** | Each service describes what it does in a formal interface | A WSDL document or an OpenAPI description |
| **Loose coupling** | Consumers depend on the contract, not on the implementation or location | Replacing the payment provider without changing the shop |
| **Abstraction** | Internal logic is hidden | The consumer sees "calculate fare", not the database design |
| **Reusability** | One service serves many applications | An identity service used by every college system |
| **Statelessness** | A request carries all the information needed; the service keeps no session between calls | Scales by adding identical instances behind a load balancer |
| **Discoverability** | Services can be found in a registry | UDDI or an API catalogue |
| **Composability** | Services can be combined into larger processes | Booking = availability + payment + notification |
| **Autonomy** | A service controls its own logic and data | Its own database and release cycle |

### The SOA triangle

Three roles interact. The **service provider** publishes a description of its service in a **service registry**; the **service consumer** (requester) finds the service in the registry; the consumer then **binds** to the provider and calls it. Figure 9.1 shows the three operations: *publish*, *find* and *bind/invoke*.

### Web services: SOAP and REST

A **web service** is a service accessed with web standards. Two styles dominate.

| Aspect | SOAP/WSDL web services | REST (RESTful APIs) |
|---|---|---|
| Message format | XML envelope (SOAP) | Usually JSON; also XML or plain text |
| Contract | **WSDL** (Web Services Description Language) | OpenAPI/Swagger description (optional) |
| Discovery | **UDDI** registry | Documentation, API gateways, catalogues |
| Transport | HTTP, SMTP, JMS and others | HTTP only |
| Operations | Any named operation in the WSDL | HTTP verbs on **resources**: GET, POST, PUT, PATCH, DELETE |
| State | Can be stateful (WS-* extensions) | Stateless by constraint |
| Standards for security and transactions | WS-Security, WS-AtomicTransaction | TLS, OAuth 2.0, tokens |
| Typical use | Enterprise systems, banks, formal contracts | Mobile apps, public cloud APIs, microservices |

REST (Roy Fielding, 2000) treats everything as a **resource** with a URL; a client reads, creates, updates and deletes it with the HTTP verbs, and every request is independent. Example: `GET /students/42` returns one student, `POST /students` creates one, and `DELETE /students/42` removes it. The major cloud providers expose their services mainly through REST APIs, which is also how infrastructure is automated.

### SOA, ESB and microservices

An **enterprise service bus (ESB)** is middleware that routes, transforms and orchestrates messages between services in classical SOA. **Microservices** (Unit 5) apply SOA ideas with smaller, independently deployed services, lightweight REST or messaging instead of a heavy bus, and containers for packaging. A fair summary: *microservices are SOA done with modern cloud tooling and without a central bus.*

### Reliability of a composed service

A business process that calls services in a chain works only if every service works. For independent services in series, the availability of the whole is the product of their availabilities (Unit 7).

```python
services = {"identity": 0.999, "catalogue": 0.999, "payment": 0.995, "notification": 0.99}
total = 1.0
for name, a in services.items():
    total *= a
    print(f"{name:13s} {a * 100:.1f}%  running product {total * 100:.3f}%")
downtime_h = (1 - total) * 24 * 365
print(f"composed availability {total * 100:.2f}%, expected downtime {downtime_h:.0f} hours per year")

# make the notification service optional (calls it asynchronously): drop it from the chain
core = 0.999 * 0.999 * 0.995
print(f"without the notification service in the critical path: {core * 100:.2f}%, {(1 - core) * 24 * 365:.0f} hours per year")
```
```output
identity      99.9%  running product 99.900%
catalogue     99.9%  running product 99.800%
payment       99.5%  running product 99.301%
notification  99.0%  running product 98.308%
composed availability 98.31%, expected downtime 148 hours per year
without the notification service in the critical path: 99.30%, 61 hours per year
```

Four individually good services (99% to 99.9%) give a combined availability of only about 98.3%, nearly 150 hours of downtime a year. Removing the weakest, non-essential service from the **critical path** (by calling it asynchronously through a queue) raises it to 99.3%. This is the design reason for timeouts, retries, circuit breakers and queues in SOA and microservice systems.

## 9.2 Cloud platforms

Unit 1 defined PaaS as a platform on which customers deploy code while the provider manages servers. Three platforms are named in the TU outline. They show the range from a fully managed, restricted runtime to a flexible, middleware-style platform.

### Google App Engine (GAE)

App Engine, announced by Google in 2008, is a **PaaS for web applications and APIs**. The developer uploads code and a configuration file; Google runs it, scales it and bills for use.

- **Runtimes:** Python, Java, Go, Node.js, PHP, Ruby and others in the *standard environment* (a sandbox with fast start-up); custom containers in the *flexible environment*.
- **Scaling:** **automatic**, from zero instances (no cost when idle) to many, according to request load; the developer sets limits rather than machines.
- **Storage services:** a NoSQL document database (Datastore, now Firestore in Datastore mode), Cloud SQL, Cloud Storage, a memory cache (Memcache) and task queues.
- **Sandbox restrictions** (standard environment): limited file-system writes, request time limits, restricted system calls. In return, the platform can pack and scale applications safely.
- **Typical uses:** web back ends, mobile app APIs, event-driven handlers.

### Microsoft Azure

Azure (announced 2008 as Windows Azure, generally available 2010) is a **broad platform** offering IaaS, PaaS and SaaS. It is organised by service families:

| Family | Examples | Role |
|---|---|---|
| **Compute** | Virtual Machines, App Service, Functions (serverless), Kubernetes Service, Batch | Run code in VMs, platforms, containers or functions |
| **Storage** | Blob (objects), File, Queue, Table, Disk | Durable storage with replication options (local, zone, geo) |
| **Data** | SQL Database, Cosmos DB (multi-model NoSQL), Synapse (analytics) | Managed databases |
| **Networking** | Virtual Network, Load Balancer, Application Gateway, CDN, ExpressRoute | Private networks and delivery |
| **Identity and security** | Microsoft Entra ID (formerly Azure Active Directory), Key Vault, Defender | IAM and secrets |
| **Integration and messaging** | Service Bus, Event Grid, Logic Apps | SOA-style messaging and workflows |
| **AI and analytics** | Machine Learning, Cognitive Services, HDInsight (Hadoop/Spark) | Data processing and AI |

Azure fits organisations with Windows, .NET and Microsoft 365 investments, and supports hybrid designs (Azure Arc, ExpressRoute).

### Aneka

**Aneka** (developed by Manjrasoft and the CLOUDS Laboratory of the University of Melbourne, led by Rajkumar Buyya) is a **.NET-based platform for building and deploying cloud applications**, described in Buyya, Vecchiola and Selvi, *Mastering Cloud Computing*. Its main ideas:

- **Aneka container:** the lightweight runtime on each node that hosts services; nodes are *workers*, with a **master** handling scheduling and resources.
- **Multiple programming models** on the same infrastructure: **Task** programming (independent tasks), **Thread** programming (distributed threads), **MapReduce** and **parameter sweep**, so that one platform serves different kinds of application.
- **Service layers:** *fabric* (resource and hardware management, monitoring), *foundation* (storage, accounting, licensing) and *application* services (the scheduling and execution of each programming model).
- **Dynamic provisioning:** an Aneka cloud can start with a local or private resource pool and **burst out** to public providers such as EC2 or Azure when its queue grows, which is the hybrid-cloud pattern of Unit 1 applied to scheduling.
- **Use:** compute-intensive and data-intensive applications in science and enterprises, with QoS and deadline-driven scheduling.

### Comparing the platforms

| Aspect | Google App Engine | Microsoft Azure | Aneka |
|---|---|---|---|
| Model | PaaS (restricted, managed) | IaaS + PaaS + SaaS | Middleware PaaS you deploy on your own or rented nodes |
| Languages and tools | Python, Java, Go, Node.js and others | .NET, Java, Python, Node.js, containers | .NET (C#) |
| Scaling | Automatic, to zero | Configurable and automatic | Scheduler-driven, with cloud bursting |
| Control | Low (sandbox) | From low to full | High (you operate the nodes) |
| Lock-in risk | Higher (proprietary services) | Medium | Lower, platform is yours |
| Best fit | Web and mobile back ends | Enterprise and hybrid | Batch, scientific and research workloads |

## 9.3 Cloud applications

### Scientific applications

Science produces large data sets and compute-heavy simulations that rise and fall in demand, which suits the elastic, pay-per-use cloud.

| Field | Application | Why the cloud helps |
|---|---|---|
| **Healthcare** | ECG and medical image analysis; remote patient monitoring; electronic health records | Elastic processing of waveforms and scans; sharing across hospitals; strict privacy controls required |
| **Biology** | Gene expression and sequence analysis, protein structure; drug screening | Thousands of independent tasks (a natural fit for MapReduce and task models, Unit 8) |
| **Geoscience** | Satellite image processing, flood and landslide mapping, weather and earthquake modelling | Large raster data in object storage; bursts of compute after an event |
| **Astronomy and physics** | Telescope archives, simulations | Parameter sweeps over many configurations |
| **Education and research** | Virtual labs, shared notebooks, collaboration | Students get identical environments without local installation |

For Nepal, relevant examples are the use of satellite imagery for flood and landslide monitoring in the monsoon season, health information systems at district hospitals, and shared computing for research teams that cannot buy a cluster.

### Business and consumer applications

| Category | Examples | Cloud characteristic used |
|---|---|---|
| **CRM and ERP** | Customer-relationship management (Salesforce), accounting and HR suites as SaaS | Multi-tenancy, subscription pricing, no local servers |
| **Productivity and collaboration** | Google Workspace, Microsoft 365, online meetings, shared documents | Real-time co-editing, access from any device |
| **Social networking** | Facebook, TikTok, Viber | Massive scale-out, global content delivery |
| **Media and streaming** | Video and music streaming, online photo storage | Object storage plus CDN (Unit 4) |
| **Cloud storage and backup** | Google Drive, Dropbox, OneDrive | Replication and erasure coding (Unit 3) |
| **E-commerce and fintech** | Online shops, payment gateways, digital wallets | Elastic capacity for festival peaks (Dashain and Tihar sales) |
| **Online gaming** | Multiplayer back ends, cloud gaming | Low-latency regional deployment, scaling by player count |
| **Education technology** | Learning management systems, online exams | Seasonal load around exam periods |
| **IoT and smart services** | Smart metering, agriculture sensors, fleet tracking | Message ingestion, time-series storage, analytics |

## 9.4 Cloud security in practice

Unit 6 gave the model (shared responsibility, IAM, keys, zero trust). This section covers the remaining topics of the TU outline: challenges and risks, SaaS security, monitoring, architecture design, data security, application security, virtual machine security, and identity management, with trust and privacy.

### Challenges and risks

1. **Loss of control and visibility:** the provider runs the infrastructure; the customer must rely on its logs, audits and contracts.
2. **Multi-tenancy:** a flaw in isolation could expose one tenant to another (rare but high-impact).
3. **Data location and law:** where data is stored determines which country's law applies; some data may not leave the country.
4. **Misconfiguration and weak identity control:** the most common real cause of cloud breaches (public buckets, leaked access keys).
5. **Vendor lock-in and exit:** proprietary services make leaving costly.
6. **Insider risk at the provider and at the customer**, and **shadow IT**: staff using cloud services that IT does not know about.
7. **Availability dependency:** an outage at the provider or its network stops the business (Unit 7).

### SaaS security

In SaaS the provider controls almost the whole stack, so the customer's duties are **identity, data, configuration and usage**.

- Require **single sign-on and MFA**; integrate the SaaS with the organisation's identity provider so that leavers lose access at once.
- Review **sharing settings** (public links, external guests), roles and administrator accounts regularly.
- Check the provider: ISO/IEC 27001 and SOC 2 reports, encryption, data-location options, breach-notification terms, **export and deletion** rights.
- Use a **cloud access security broker (CASB)** or logging to find unapproved SaaS and risky behaviour.
- Back up SaaS data that is business-critical: the provider's replication is not a backup against accidental or malicious deletion.

### Security monitoring

Detection must be built in, because the customer cannot install sensors on the provider's network. Sources: **provider audit logs** (who called which API: for example AWS CloudTrail, Azure Activity Log), **flow logs** (network connections), **application and operating-system logs**, and **threat-detection services**. Logs go to a central, protected store and into a **SIEM**; alerts cover impossible logins, new administrator roles, disabled logging, public storage, unusual data transfer and cost spikes (which can reveal cryptomining). Monitoring only works with a tested **incident response plan** (Unit 6 of the Cyber Security book).

### Security architecture design

A cloud architecture combines layers so that no single failure is fatal (defence in depth):

1. **Identity layer:** least privilege, MFA, short-lived credentials.
2. **Network layer:** private subnets, security groups, web application firewall, DDoS protection (Unit 4).
3. **Compute layer:** hardened images, patching, minimal container images, runtime protection.
4. **Data layer:** encryption at rest and in transit, key management, backups.
5. **Governance layer:** policies as code, logging, compliance checks, cost controls.

### Data security

Protect data through its life: **classify** it, **encrypt** it in transit (TLS) and at rest (envelope encryption with customer-managed keys, Unit 6), control **access**, apply **data loss prevention**, keep **backups** and a **retention and deletion** policy, and **mask or tokenise** personal data used for testing. Deletion in the cloud is difficult to verify; **crypto-shredding** (destroying the key) makes the stored ciphertext unreadable.

### Application security

Cloud applications face the web risks of the OWASP Top 10 (Cyber Security book, Unit 8) plus cloud-specific ones: exposed APIs, secrets in code or container images, vulnerable dependencies and insecure infrastructure-as-code templates. Controls: secure development lifecycle, code and dependency scanning, secrets managers, API gateways with authentication and rate limits, web application firewalls, and security testing in the delivery pipeline (**DevSecOps**).

### Virtual machine security

VMs share hardware, so the hypervisor and the images must be protected:

- Keep the **hypervisor patched** and its management interface on a private network with MFA.
- Use **hardened, signed golden images**; patch or replace instances regularly; do not leave old snapshots with data around.
- Watch for **VM sprawl** (forgotten machines), **VM escape** (an exploit that breaks out of the guest) and **side-channel attacks** between co-located VMs; sensitive workloads can use dedicated hosts or **confidential computing**.
- Isolate by network segments and security groups; restrict inter-VM traffic.
- **Protect snapshots and backups** as carefully as live data, since they contain the same secrets.

### Identity management and access control

Summarising Unit 6: **identities** (people, services, machines) are authenticated, ideally with MFA and federation (SAML, OpenID Connect); **authorisation** follows least privilege with roles and policies; **privileged access** is time-limited and logged; and access is **reviewed** regularly. **Single sign-on** gives one login for many services, and **federated identity** lets an organisation's directory log users into the provider without sharing passwords.

### Trust and privacy

**Trust** in a provider is built on evidence rather than assurance: certifications and audit reports (ISO/IEC 27001, 27017 for cloud, 27018 for personal data in the cloud, SOC 2), transparency about incidents, contract terms (the SLA of Unit 7, data-protection clauses, audit rights) and the customer's own controls (encryption with its own keys). **Privacy** concerns personal data: collect only what is needed, tell people how it is used, protect it, keep it in permitted jurisdictions and delete it when no longer needed. Nepal's Individual Privacy Act 2075 (2018) and the Electronic Transactions Act 2063 set the basic legal frame; organisations that serve customers abroad may also be subject to foreign rules such as the EU GDPR. A **data-processing agreement** with the provider states who is the controller and who is the processor of the data.

## 9.5 Open challenges and cloud adoption

### Open challenges

- **Interoperability and portability:** moving between providers is hard because APIs and services differ; open standards, containers and Kubernetes help.
- **Energy use and sustainability** of data centres, and green scheduling.
- **Latency for real-time applications**, which pushes work to the **edge** (Unit 4's CDN idea extended to computing).
- **Data sovereignty and regulation**, and **trusted multi-cloud management**.
- **Skills shortage** and **cost control** (FinOps, Unit 7).
- **Programming models and debugging** for large distributed systems.

### Cloud adoption: a practical sequence

1. **Assess** the portfolio: which applications, data and users; the business reason (cost, speed, resilience).
2. **Classify** data and check legal constraints before choosing a region or provider.
3. **Choose a model:** SaaS if a product exists; PaaS for new applications; IaaS for lift-and-shift; hybrid where data must stay on premises.
4. **Pilot** with a proof of concept: measure performance, cost and operations effort.
5. **Migrate** in waves using the usual strategies (rehost, replatform, refactor, repurchase, retire, retain).
6. **Govern:** landing zone, identity, tagging, budgets, logging.
7. **Operate and optimise:** monitor, right-size, review security and cost monthly; keep an exit plan.

### Practical work: field visit report

The TU outline asks for a visit to a nearby cloud or data-centre provider and a report on its **organisational structure and technology**. A suitable report structure: (1) organisation profile and services; (2) organisation chart and teams; (3) infrastructure (servers, storage, network, power, cooling, physical security); (4) virtualisation and cloud software used; (5) service and pricing models; (6) security, backup and compliance; (7) customers and example workloads; (8) problems and opportunities; (9) your observations and recommendations; (10) photographs only where permitted, and the questions you asked.

## 9.6 Seeing the ideas: the SOA triangle and the composed-service chain

```svgfig label="9.1" caption="The SOA triangle. The provider publishes its service description (WSDL or an API specification) in a registry; the consumer finds it there, then binds to the provider and invokes the service. The registry holds descriptions, not the services themselves."
f = Fig(580, 214)
f.box(206, 14, 168, 52, "Service registry\nUDDI or API catalogue", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(16, 130, 168, 60, "Service provider\nimplements the service\n(SOAP or REST)", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(396, 130, 168, 60, "Service consumer\nweb app, mobile app,\nanother service", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.arrow([(100, 130), (206, 52)], label="1 publish", lpos=(116, 82))
f.arrow([(480, 130), (374, 52)], label="2 find", lpos=(452, 82))
f.arrow([(396, 160), (184, 160)], label="3 bind and invoke", lpos=(290, 150))
f.text(290, 206, "Loose coupling: the consumer depends on the contract, not on the provider's code or location.", size=9.5, color=NAVY, bold=True)
```

```svgfig label="9.2" caption="Availability of a composed service (section 9.1). Four services in series multiply: 99.9%, 99.9%, 99.5% and 99.0% give 98.31%, about 148 hours of downtime a year. Calling the notification service asynchronously removes it from the critical path and gives 99.30%."
f = Fig(580, 214)
rows = [("identity", 99.9), ("catalogue", 99.9), ("payment", 99.5), ("notification", 99.0)]
for i, (n, a) in enumerate(rows):
    y = 12 + i * 34
    f.text(8, y + 14, n, size=10, color=NAVY, bold=True, anchor="start")
    f.box(92, y, (a - 98) * 150, 26, "", fill=MINT, stroke=TEAL)
    f.text(92 + (a - 98) * 150 + 6, y + 14, f"{a:.1f}%", size=10, color=TEAL, bold=True, anchor="start", vmid=True)
f.box(92, 152, (98.31 - 98) * 150, 26, "", fill=ROSE, stroke=RED)
f.text(8, 166, "composed", size=10, color=NAVY, bold=True, anchor="start")
f.text(92 + (98.31 - 98) * 150 + 6, 166, "98.31%  (148 h/year down)", size=10, color=RED, bold=True, anchor="start", vmid=True)
f.text(8, 200, "bars start at 98%; asynchronous notification: 99.30% (61 h/year)", size=9.5, color=SLATE, anchor="start")
```

## 9.7 Summary and exercises

SOA builds applications from loosely coupled, reusable, discoverable services described by contracts; web services follow SOAP/WSDL/UDDI or REST, and microservices are SOA with modern cloud tooling. Chained services multiply their failure rates, so critical paths must be short and tolerant. Google App Engine is a restricted, auto-scaling PaaS, Azure a broad IaaS/PaaS/SaaS platform and Aneka a .NET middleware with task, thread and MapReduce models and cloud bursting. Cloud applications range from scientific computing to CRM, productivity, media and gaming. Security practice covers SaaS configuration, monitoring, layered architecture, data protection, application and VM hardening, identity, trust and privacy; adoption proceeds from assessment to pilot, migration and governed operation.

1. Define SOA and list its principles. How does SOA relate to cloud computing and to microservices?
2. Draw and explain the SOA triangle. What are WSDL, SOAP and UDDI?
3. Compare SOAP and REST web services in a table. Give REST examples using HTTP verbs.
4. Three services in series have availabilities 99.9%, 99.5% and 99.0%. Find the composed availability and yearly downtime.
5. Describe Google App Engine: runtimes, scaling, storage and restrictions.
6. List the main Azure service families with an example of each.
7. What is Aneka? Explain its programming models and cloud bursting.
8. Compare App Engine, Azure and Aneka.
9. Give three scientific and four business or consumer applications of the cloud, and the cloud characteristic each uses.
10. List seven cloud security challenges and risks.
11. Explain SaaS security, VM security and application security measures.
12. How is security monitoring done in the cloud? Which events should raise an alert?
13. Explain trust and privacy in cloud computing, including the Nepali legal frame.
14. Describe a seven-step cloud adoption sequence and name the six migration strategies.
15. Prepare an outline for a field-visit report on a data centre.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain service-oriented architecture and the SOA triangle.**

*Introduction.* SOA builds software from services: self-contained functions called over a network through a published contract (section 9.1, Figure 9.1).

*Principles.* Standardised contract, loose coupling, abstraction, reusability, statelessness, discoverability, composability and autonomy.

*The triangle.* The **provider** publishes the service description in a **registry**; the **consumer** finds it; then the consumer **binds** and invokes the provider. Web services use WSDL for the description, UDDI as the registry and SOAP or REST for messages.

*Relation to the cloud.* IaaS, PaaS and SaaS are service layers; cloud APIs are mostly REST. Microservices are SOA without a central bus.

*Conclusion.* SOA gives reuse and flexibility because consumers depend on contracts, not on implementations.

**Q2 (5 marks). Compare SOAP and REST web services.**

*Introduction.* Both let programs call remote functions over the web, but with different styles (section 9.1).

| Aspect | SOAP | REST |
|---|---|---|
| Format | XML envelope | JSON or XML |
| Contract | WSDL | OpenAPI (optional) |
| Discovery | UDDI | Documentation, catalogues |
| Operations | Named operations | HTTP verbs on resources |
| State | Can be stateful | Stateless |
| Security | WS-Security | TLS, OAuth 2.0 |
| Use | Enterprise, formal contracts | Mobile, public cloud APIs |

*Example.* REST: `GET /students/42` reads, `POST /students` creates, `DELETE /students/42` deletes. SOAP would call a named operation such as `GetStudent` in an XML message.

*Conclusion.* REST is lighter and dominates cloud APIs; SOAP remains where formal standards for security and transactions are required.

**Q3 (5 marks). Three services in series have availabilities 99.9%, 99.5% and 99.0%. Find the composed availability and yearly downtime, and say how to improve it.**

*Introduction.* For independent services in series, all must work, so availabilities multiply (section 9.1, Figure 9.2).

*Calculation.*

1. A = 0.999 × 0.995 × 0.990 = **0.9841**, i.e. **98.41%**.
2. Downtime = (1 − 0.9841) × 8,760 h = about **140 hours** per year.

*Improvement.* Shorten the critical path: make the weakest service optional or asynchronous (a queue); run redundant instances (two instances of the 99% service in parallel give 1 − 0.01² = 99.99%); add timeouts, retries and circuit breakers.

*Conclusion.* The chain is weaker than any single link, so reduce serial dependencies and add redundancy where it matters most.

**Q4 (10 marks). Describe the three cloud platforms Google App Engine, Microsoft Azure and Aneka and compare them.**

*Introduction.* Platform services let customers build and run applications without managing servers (section 9.2).

*Google App Engine.* A PaaS for web and mobile back ends; runtimes in Python, Java, Go, Node.js and others; **automatic scaling to zero**; Datastore/Firestore, Cloud SQL, Cloud Storage, cache and task queues; sandbox restrictions on files, time and system calls.

*Microsoft Azure.* IaaS, PaaS and SaaS in one platform: compute (VMs, App Service, Functions, Kubernetes), storage (Blob, Queue, Table), data (SQL Database, Cosmos DB), networking, identity (Entra ID, Key Vault), integration (Service Bus) and analytics (HDInsight). Strong for .NET and hybrid enterprise use.

*Aneka.* A .NET middleware platform (Manjrasoft, University of Melbourne) with an Aneka container on each node, fabric, foundation and application service layers, **task, thread and MapReduce programming models**, QoS-aware scheduling and **dynamic provisioning** that bursts to public clouds.

| Aspect | App Engine | Azure | Aneka |
|---|---|---|---|
| Model | Restricted PaaS | IaaS + PaaS + SaaS | Middleware PaaS |
| Scaling | Automatic, to zero | Configurable, automatic | Scheduler and bursting |
| Control | Low | Low to full | High |
| Lock-in | Higher | Medium | Lower |
| Best fit | Web back ends | Enterprise, hybrid | Batch and scientific |

*Conclusion.* Choose by workload: App Engine for quick managed web back ends, Azure for broad enterprise needs and Aneka for compute-intensive or research workloads on your own and rented nodes.

**Q5 (10 marks). Discuss cloud security challenges and the security measures for SaaS, applications, virtual machines and data. Explain trust and privacy.**

*Introduction.* Customers share responsibility with the provider: the provider secures the facility and platform, the customer secures identity, data and configuration (Unit 6, section 9.4).

*Challenges.* Loss of control and visibility, multi-tenancy isolation, data location and law, misconfiguration and weak identity control, vendor lock-in, insiders and shadow IT, and availability dependency.

*Measures.*

1. **SaaS:** SSO and MFA, sharing and role reviews, provider certification (ISO/IEC 27001, SOC 2), export and deletion rights, CASB, independent backups.
2. **Application:** secure development lifecycle, dependency and secret scanning, API gateway with authentication and rate limits, WAF, DevSecOps.
3. **Virtual machine:** patched hypervisor, hardened signed images, control of sprawl, network isolation, protected snapshots, dedicated hosts for sensitive work.
4. **Data:** classification, encryption in transit and at rest with customer-managed keys, access control, DLP, backups, retention policy and crypto-shredding.
5. **Monitoring:** central logs (audit, flow, application) in a SIEM with alerts for new administrators, disabled logging, public storage and unusual transfers, plus an incident response plan.

*Trust and privacy.* Trust rests on evidence: certifications, audit reports, incident transparency, SLA and data-processing agreements, and the customer's own keys. Privacy means collecting minimal personal data, protecting it, keeping it in permitted jurisdictions and deleting it on time, within the Individual Privacy Act 2075 and the Electronic Transactions Act 2063.

*Conclusion.* Cloud security is a shared, layered and continuous responsibility; most failures come from configuration and identity, not from the provider's hardware.
