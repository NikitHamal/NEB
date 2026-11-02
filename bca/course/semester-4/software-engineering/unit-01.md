---
subject: Software Engineering
grade: BCA Semester 4
unit: 1
title: Introduction to Software Engineering
hours: 4
area: BCA 252 · Software Engineering · Unit 1
---

In 1968 a NATO conference in Garmisch coined the phrase "software engineering" because large software projects were routinely late, over budget and wrong; the situation was called the *software crisis*. Fifty years on, the Nepali government portals, bank systems and apps we depend on still fail for the same reasons: unclear requirements, poor estimates and weak process. This unit defines software, its attributes and the field built to address these problems.

::: key What this unit gives you
- Definition and types of software; characteristics and attributes of good software.
- Definition of software engineering, its costs and key challenges; system engineering versus software engineering.
- Professional practice and ethics.
:::

## 1.1 What is software?

**Software** is (1) instructions (programs) that provide desired function when executed, (2) data structures that let programs manipulate information, and (3) documentation describing their operation and use. A program is not a software *product*: a product has documentation, tests, installation and support, and is meant for users other than its author.

### Types of software

| Type | Description | Examples |
|---|---|---|
| **System software** | serves other programs | operating systems, compilers, drivers |
| **Application software** | solves a specific business or personal need | accounting, hospital management, a college result system |
| **Engineering/scientific** | numerical computation | CAD, simulation, MATLAB-like tools |
| **Embedded software** | resides in a device | washing machine, ABS controller |
| **Web/mobile applications** | delivered over the network or on phones | e-Sewa-style wallets, ride-hailing apps |
| **Artificial intelligence software** | uses non-numerical algorithms | expert systems, machine-learning services |
| **Product-line software** | a base shared by many customers | ERP, office suites |

Software can also be **generic** (produced for an open market, the developer owns the specification) or **custom/bespoke** (written for one client, the client owns the specification). Most revenue is in generic products, but most Nepali software work is custom.

### Characteristics of software

Software differs from hardware: (1) it is **developed or engineered, not manufactured**, so the cost lies in design, not copying; (2) it **does not wear out**; but it **deteriorates** as changes introduce defects (the failure-rate curve has spikes after every change instead of a bathtub); (3) most software is still **custom-built** rather than assembled from components, though reuse is increasing.

## 1.2 Attributes of good software

A good product delivers the required functionality *and* these non-functional attributes:

| Attribute | Meaning |
|---|---|
| **Maintainability** | can be evolved as needs change; the most important attribute because change is inevitable |
| **Dependability and security** | reliable, safe, and secure against malicious misuse |
| **Efficiency** | does not waste memory or processor time; response time, utilisation |
| **Acceptability** | usable, understandable and compatible with the users' systems |

## 1.3 Software engineering defined

> **Software engineering** is the application of a systematic, disciplined, quantifiable approach to the development, operation and maintenance of software (IEEE).

It is an *engineering* discipline: it uses theories, methods and tools but applies them selectively, within organisational and financial constraints, to produce a working solution. It concerns *all* aspects of production, from specification to maintenance, not just coding, and includes project management and tools.

**Software engineering versus computer science.** Computer science studies theory and fundamentals (algorithms, complexity); software engineering is about the practicalities of producing useful software. **Software engineering versus system engineering.** System engineering covers *whole* systems of hardware, software, people and processes (an ATM network, an airport) and decides which functions go to software; software engineering is concerned with the software part, after that decision. System engineers must manage emergent properties (reliability, safety) that depend on all parts together.

## 1.4 Software engineering costs

Roughly 60 % of costs are development costs and 40 % testing costs. For *custom* software, the **evolution (maintenance) costs often exceed development costs**, commonly by a factor of 2 to 4 over the product's life, and for long-lived systems a majority of the total. Costs depend on the process, the type of system and the dependability required: a safety-critical system costs far more per line than a prototype. Costs vary with project phase: a fault found during maintenance costs many times more to fix than one found during specification (Unit 3 quotes the typical figure of 50 to 100 times in the classic studies; the exact factor varies widely by project).

Estimation techniques that put numbers on these costs (COCOMO, function points) and a verified worked example appear in Unit 8.

## 1.5 Key challenges

- **Heterogeneity**: systems must run across different platforms, devices and legacy systems.
- **Business and social change**: delivery must be faster than the business can change; old systems must be adapted.
- **Security and trust**: software is attacked constantly, and users must trust it.
- **Scale**: from small embedded to Internet-scale systems.
- **Time to delivery** under pressure from competition.

## 1.6 Professional practice and ethics

Software engineering involves responsibilities beyond technical skill: **confidentiality** (respect the client's data), **competence** (do not accept work beyond your ability), **intellectual property** (respect licences and copyright), and **avoid computer misuse** (no unauthorised access, no malware). The joint **ACM/IEEE Software Engineering Code of Ethics** sets eight principles: *Public* (act in the public interest), *Client and Employer*, *Product* (high professional standards), *Judgment*, *Management*, *Profession*, *Colleagues*, and *Self* (lifelong learning). When the public interest and the employer conflict, the public interest comes first. In Nepal the *Electronic Transactions Act 2063* criminalises unauthorised access and cyber crimes, and the Individual Privacy Act 2075 protects personal data, so engineers need to know the local legal framework too.

::: example An ethical dilemma
A bank's developer finds an unreported bug that, under rare conditions, credits interest twice. The manager says to ignore it since "nobody has noticed". Under the code of ethics, the engineer must report the defect and refuse to conceal it: public and client interest outweigh the schedule. Escalate to a higher manager, document the report, and decline to participate if the matter is left unresolved.
:::

## Formula and fact sheet

- Software = programs + data + documentation. Software is engineered, does not wear out, but deteriorates through change.
- Four essential attributes: maintainability, dependability and security, efficiency, acceptability.
- Costs: about 60 % development, 40 % testing; evolution often exceeds development.
- ACM/IEEE code: public first.

## Chapter summary

- Software is more than code, and comes in system, application, embedded, web and AI forms; it can be generic or custom.
- Good software is maintainable, dependable, efficient and acceptable.
- Software engineering is a systematic engineering approach to the whole life cycle; it sits inside the broader field of system engineering.
- Costs are dominated by maintenance and testing; major challenges are heterogeneity, change, security, scale and delivery time.
- Professional practice demands competence, confidentiality and public-interest ethics.

## Practice

1. Define software and explain how it differs from a program.
2. List four types of software with examples.
3. Why is software said to "deteriorate" rather than "wear out"?
4. Name and explain the four essential attributes of good software.
5. Define software engineering and distinguish it from computer science and system engineering.
6. Why does maintenance usually cost more than development?
7. List three key challenges facing software engineering today.
8. State four principles of the ACM/IEEE Code of Ethics with an example breach of one.

::: note Answers and worked solutions
**1.** Software is programs, data structures and documentation. A program is only code written for the author's use; a software product adds documentation, testing, installation support and maintenance for other users.
**2.** System (OS, compiler), application (billing system), embedded (microwave controller), web/mobile (online banking app), AI (a recommender), scientific (simulation).
**3.** Hardware fails from physical wear. Software has no physical wear; but each change can introduce new errors, so the failure rate rises after changes and the software slowly becomes harder to maintain, which is deterioration.
**4.** Maintainability (can evolve), dependability and security (reliable, safe, secure), efficiency (resource use and speed), acceptability (usable and compatible).
**5.** Software engineering: systematic, disciplined, quantifiable approach to developing, operating and maintaining software. Computer science: the theory behind computing. System engineering: whole systems including hardware and people; software engineering is its software part.
**6.** Software needs to change throughout its life: new laws, platforms, features and fixes. Over years of use these changes accumulate and exceed the one-time development effort, particularly for long-lived systems.
**7.** Heterogeneity (many platforms), rapid business change and delivery pressure, and security and trust.
**8.** Public (act in public interest), Client and employer, Product (high standards), Judgment (independent professional judgment). Breach example: hiding a known safety bug from the public to meet a deadline violates the *Public* principle.
:::
