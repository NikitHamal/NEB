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

## 1.8 Summary and exercises

Cloud computing delivers metered, elastic, self-service computing from pooled resources; the NIST model organises it into five characteristics, three service models and four deployment models, and the economics rest on matching capacity to demand.

1. State the five NIST characteristics, and explain why a fixed rented server fails the test.
2. Draw a responsibility table for IaaS, PaaS and SaaS and give one product for each.
3. Distinguish hybrid cloud from multi-cloud.
4. Demand is 10 servers for 12 hours and 50 for 12 hours. Compute utilisation of a peak-sized fleet and the percentage saved by elastic billing.
5. Explain CapEx versus OpEx with an example of a Nepali company moving its email to SaaS.
6. List three risks of public cloud for a regulated bank and one mitigation for each.
