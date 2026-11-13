## 4.11 Summary and exercises

Upgrades are projects: side by side where possible, with a service checklist, a tested back-up and back-out plan, an announced window and a review. Centralise what is common and security-critical, keep local what must work without the WAN, and convert in stages under an SLA. Monitor at host, process, service and business level, alert only on actionable events, keep history and report against the SLO and error budget. Namespaces need consistency, uniqueness, aliases for functions, central management and delayed reuse; DNS, directories and mail addresses are the main ones. E-mail needs MX, SPF, DKIM, DMARC, TLS, filtering and no open relay, and is usually best hosted. Printing is run from central queues with standard models, quotas and secure release. Storage is chosen among DAS, NAS, SAN, object and cloud, protected by RAID, snapshots and quotas, and never confused with backup. Backups follow a written policy (RPO, RTO, retention), use full, incremental and differential schemes, follow 3-2-1 with an immutable copy, and are proven by restore tests. A software repository gives consistent, signed, cached and licence-controlled software and staged updates. Web services use TLS, a reverse proxy or load balancer, stateless application servers, caching, a WAF, monitoring and load tests.

1. Why are server upgrades risky? Describe a ten-step upgrade procedure.
2. Compare in-place, side-by-side, blue/green and rolling upgrades.
3. What is a back-out plan and a "point of no return"?
4. Compare centralised and decentralised services. Which services would you centralise in a college and why?
5. Describe how to move a department from its own mail server to a central service.
6. What are the four levels and the four golden signals of service monitoring? How do you avoid alert fatigue?
7. Define namespace. State five principles of good namespace design.
8. Compare themed and structured host names. Why use CNAME aliases for services?
9. Write the DNS records needed for a domain with a web server, a mail server with a backup, and two name servers.
10. What is a directory service? Why must UIDs be consistent?
11. Explain how e-mail travels from sender to receiver (MUA, MTA, MX, MDA, IMAP).
12. Explain SPF, DKIM and DMARC. What is an open relay and why is it dangerous?
13. Recommend a design for a college mail service and justify hosted versus self-run.
14. Design a print service for a library and two labs, covering queues, drivers, quotas and security.
15. Differentiate DAS, NAS and SAN with examples. Why is RAID not a backup?
16. List eight recommendations for a file server design. Explain snapshots and quotas.
17. Compare full, incremental and differential backups. What is needed to restore Thursday from each scheme?
18. What should a backup policy contain? Explain the 3-2-1 rule and why restores must be tested.
19. What is a software repository? Give five benefits and the design recommendations.
20. Explain a layered web-service architecture and ten recommendations for running it.
21. A full backup is 800 GB and the daily incremental is 24 GB. With one weekly full and six incrementals, what is the weekly total, and how many sets must be restored for Wednesday?
22. A site expects 3,000 users in the peak minute with 5 requests each, and one server handles 100 requests per second at 65% utilisation of its limit: how many servers are required?

**Answers to the numerical items.** (21) Weekly total = 800 + 6 x 24 = 944 GB. Wednesday needs the full plus Monday, Tuesday and Wednesday incrementals: 4 sets (the program in Section 4.8.3 prints 1 + day number). (22) Requests per second = 3000 x 5 / 60 = 250. If 100 requests/s is the capacity at the chosen utilisation, 250/100 = 2.5, so 3 servers, plus one spare makes 4. In the program of Section 4.10.2 the 6,000 users x 6 requests give 600 requests/s and, at 65% of a 150 requests/s limit (97.5 per server), 7 servers plus a spare.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Compare full, incremental and differential backups.**

A full backup copies everything: it is the largest and slowest to make but restores from one set. An incremental backup copies only what changed since the previous backup of any kind: it is the smallest and quickest, but a restore needs the last full and every incremental since, so it is slowest and one damaged set breaks the chain. A differential backup copies what changed since the last full: it grows through the week, but a restore needs only the last full and the latest differential. The choice balances backup window and storage against restore time; a common practice is a weekly full with daily incrementals or differentials, retained by a grandfather-father-son rotation, with an off-site copy.

**Q2 (5 marks). Explain SPF, DKIM and DMARC.**

They are DNS-published mechanisms that let receivers check that mail claiming to come from a domain is genuine. SPF lists the IP addresses allowed to send for the domain; the receiver compares the connecting address. DKIM adds a digital signature to each message made with the sender's private key; the receiver fetches the public key from DNS and verifies it, which also shows the message was not altered. DMARC builds on both: it tells receivers to accept, quarantine or reject mail that fails them (aligned with the visible From domain) and where to send reports. Together they reduce forged and phishing mail.

**Q3 (10 marks). Describe the recommended design and operation of a backup and restore service for a college.**

Policy: list the systems (file server, mail if self-run, databases, web, configuration of network devices, laptops of staff), set an RPO and RTO for each, a retention schedule (daily 14 days, weekly 12 weeks, monthly 12 months, yearly as the law or audit requires), the roles and the security rules.

Method: a weekly full and daily incremental or differential backup to disk on a backup server, with deduplication; databases through dumps or snapshot-aware agents; a second copy replicated to another building or the cloud and an offline or immutable copy to resist ransomware, following 3-2-1. Backups are encrypted and the keys are stored separately; the backup account cannot be deleted from production.

Operation: schedules run automatically; success and failure are monitored and alerts reach a person; each run verifies integrity; a restore test of a file, a mailbox and a full server is performed each term with its time compared with the RTO; capacity is planned from data size, change rate and retention; the restore procedure and the rebuild of the backup server itself are documented.

Conclusion: the quality of the service is measured by successful restores within the objectives, not by the number of backups made.

**Q4 (5 marks). Recommend a web-service architecture for admission results.**

Place the site behind a firewall and a load balancer that terminates TLS and checks the health of the back ends; run at least two stateless application servers so that any can answer any request and one can be upgraded while the other serves; keep results in a replicated database; serve static files from cache or a CDN; apply a WAF and rate limits; monitor latency, errors and traffic with probes; load-test before the day, sizing servers for peak requests per second at about 65% utilisation plus a spare; keep a rollback and a static fallback page.
