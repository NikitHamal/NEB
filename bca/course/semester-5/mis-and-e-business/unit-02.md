---
subject: MIS and e-Business
grade: BCA Semester 5
unit: 2
title: Strategy and Competitive Advantage
hours: 7
area: BCA 304 · MIS and e-Business · Unit 2
---

When eSewa launched in 2009 it did not have the best technology in the world; it had the first useful position: merchants and users joined because other users had joined, and each new merchant made the wallet more valuable to the next customer. That is a *strategic* use of an information system: IT is not just making an existing operation cheaper, it is changing the competitive position of the firm. This unit gives you the standard tools for reasoning about such positions: Porter's five forces, the value chain, generic strategies, and the economics of switching costs and network effects, each with numbers you can recompute.

::: key What this unit gives you
- Porter's five forces and a weighted way to score industry pressure; market concentration with the HHI.
- The value chain and where information systems add value in it.
- Generic strategies and the IT moves that support them.
- Switching costs, lock-in and network effects (Metcalfe's law); strategic alignment and business process reengineering.
:::

## 2.1 Strategy and the role of information systems

A **strategy** is a plan for achieving a goal in a competitive environment: where to compete (which customers and products) and how to win. Information systems enter at three levels. **Operational excellence**: do the same things better, cheaper and faster. **New products, services and business models**: do new things (internet banking, mobile wallets). **Customer and supplier intimacy**: know customers so well that they stay. At the extreme, IT enables **business model innovation**: a ride-hailing app such as Pathao owns no taxis, a marketplace such as Daraz holds little stock of its own.

An information system gives **competitive advantage** when it lets the firm do something rivals cannot easily copy. The test is sustainability: a technology that any competitor can buy next month (a website, a POS terminal) is a *requirement to compete*, not an advantage. Advantage comes from the combination of technology with unique data, relationships, processes and brand.

## 2.2 Porter's five forces

Michael Porter explained industry profitability by five competitive forces. The stronger the forces, the lower the profit available to any firm.

1. **Threat of new entrants.** Low barriers (little capital, no licence, no brand needed) invite entry. Barriers include economies of scale, network effects, regulation (a Nepali payment service needs a **Nepal Rastra Bank licence**), capital and access to distribution.
2. **Bargaining power of suppliers.** Few suppliers, unique inputs and high switching costs make suppliers strong (a single cloud vendor or telecom operator).
3. **Bargaining power of buyers.** Concentrated, price-sensitive, well-informed buyers with many alternatives are strong. The internet raises buyer power by making prices easy to compare.
4. **Threat of substitutes.** A different product meeting the same need: remittance through a wallet instead of a money-transfer shop; video calls instead of travel.
5. **Rivalry among existing competitors.** Many equal rivals, slow industry growth, high fixed costs and undifferentiated products produce price wars.

Information technology affects all five. The Internet *lowers* entry barriers for pure-online businesses but *raises* the stakes through scale and data. It increases buyer power (price comparison), may reduce supplier power (many e-marketplaces) and expands the range of substitutes.

### Scoring the forces

A manager can turn the qualitative discussion into a rough *intensity score*: rate each force 1 (weak) to 5 (strong), weight the forces by their importance to this industry (weights add to 1) and take the weighted sum. The scoring below is for a hypothetical online grocery start-up.

| Force | Weight | Intensity (1 low – 5 high) | Weight × intensity |
|---|---|---|---|
| Threat of new entrants | 0.2 | 4 | 0.80 |
| Bargaining power of suppliers | 0.15 | 2 | 0.30 |
| Bargaining power of buyers | 0.25 | 5 | 1.25 |
| Threat of substitutes | 0.25 | 4 | 1.00 |
| Rivalry among competitors | 0.15 | 4 | 0.60 |
| **Total** | 1.00 |  | **3.95** |

The industry pressure score is **3.95** out of 5: high. The dominant contributors are buyer power and substitutes, so the strategy should aim at the loyalty and switching costs that reduce buyer power (a subscription, a delivery-time guarantee) and at differentiation against substitutes (a local market, a kirana store). The scores are judgements, so the useful output is the *conversation* and the sensitivity (how much would the total change if buyer power were 3 instead of 5?), not the decimal.

### Market concentration: the HHI

**Rivalry** depends on how many firms share the market. The **Herfindahl–Hirschman Index (HHI)** is the sum of squared market shares (in percent): 10,000 for a monopoly, near zero for perfect competition. Regulators treat roughly below 1,500 as unconcentrated and above 2,500 as highly concentrated (the thresholds differ by authority). Here is an invented four-wallet market:

| Firm | Share s (%) | s² |
|---|---|---|
| Wallet A | 45 | 2025 |
| Wallet B | 30 | 900 |
| Wallet C | 15 | 225 |
| Wallet D | 10 | 100 |
| **HHI** | 100 | **3250** |

HHI = **3250**, highly concentrated. If Wallet C (15%) and Wallet D (10%) merged, the new firm would have 25% and the HHI would become **3550**. The change is **300**, which equals 2 × 15 × 10: a merger always raises the HHI by twice the product of the merging shares, a quick screen for competition regulators.

## 2.3 The value chain

Porter's **value chain** splits a firm into the activities that create value and the margin that remains. **Primary activities** directly create and deliver the product:

- **Inbound logistics**: receiving, storing, inventory control.
- **Operations**: converting inputs into the product or service.
- **Outbound logistics**: order fulfilment and delivery.
- **Marketing and sales**: promotion, channels, pricing.
- **Service**: installation, support, warranty.

**Support activities** make the primary ones possible: **firm infrastructure** (finance, legal, planning), **human resource management**, **technology development** and **procurement**. The **margin** is the difference between the value customers pay and the total cost of all the activities. Information systems are a *thread* through every box: warehouse management in inbound logistics, ERP production planning in operations, route optimisation in outbound, CRM in marketing and service, and the integrated ERP in the infrastructure.

| Activity | Typical information system | Value created |
|---|---|---|
| Inbound logistics | Inventory control, supplier portal | Lower stock, fewer stock-outs |
| Operations | Production planning, quality systems | Lower cost, fewer defects |
| Outbound logistics | Order management, delivery tracking | Faster, more reliable delivery |
| Marketing and sales | CRM, e-commerce site, analytics | Better targeting, higher conversion |
| Service | Help desk, ticketing, knowledge base | Retention, fewer repeat visits |
| Firm infrastructure | ERP, accounting, compliance reporting | Control, lower overhead |
| Human resources | HRIS, e-learning | Productivity, lower turnover |
| Technology | R&D tools, version control | Faster innovation |
| Procurement | e-procurement, vendor management | Lower purchase price |

The **value system** (or *value network*) extends the view: your value chain sits between suppliers' chains and customers', and the largest gains often come at the *interfaces*: a shared inventory system with a supplier, or a customer-facing order status page.

## 2.4 Generic strategies and supporting IT

Porter identified three generic ways to outperform rivals:

| Strategy | Idea | Information systems support | Risk |
|---|---|---|---|
| **Cost leadership** | Be the lowest-cost producer in the industry | Automation, ERP, e-procurement, process control | A rival with lower costs or a technological shift |
| **Differentiation** | Offer something customers value and will pay extra for | Personalisation, mobile app, quality data, innovation | Imitation; uniqueness not valued |
| **Focus** | Serve a narrow segment (by region, customer type) better than broad rivals | Segment analytics, niche e-commerce | Segment shrinks or is entered by large firms |

Other IT-based strategic moves:

- **Lock-in** through **switching costs**: once a firm's data, staff skills and integrations are built around a system, changing is expensive, so customers stay.
- **Alliances and partnerships**: shared platforms among banks (interbank switches, Unit 5), loyalty programmes.
- **Innovation first-mover**: the first mobile wallet or the first online ticketing service gains users before rivals.
- **Mass customisation**: producing individualised products at near-mass-production cost through configurable online orders.

## 2.5 Network effects and Metcalfe's law

Some products become more valuable as more people use them: a telephone, a payment network, a marketplace. **Metcalfe's law** is a model, not a law of nature: the *number of possible connections* among n users is n(n − 1)/2 and the network's value is approximated as proportional to it. With 1,000 users there are **4,99,500** possible pairs; with 2,000 users, **19,99,000**, about four times as many for twice the users. The practical lessons: the *early* growth phase is hard (the value to the first users is almost zero, so firms subsidise it with cashback), and once a network is ahead the *winner takes most*. The law overstates value, because most possible connections are never used; later models suggest value proportional to n log n.

::: caution Not every advantage is permanent
A strategic IS can become a **strategic necessity**: ATMs and internet banking once distinguished a bank, and now a bank without them cannot compete. Before investing, ask: *can a rival copy it within a year? Does it rest on our data, relationships or scale? What happens if we do not invest?*
:::

## 2.6 Aligning IS strategy with business strategy

An **IS strategy** states which systems the organisation will build or buy and why. It must be **aligned** with business strategy: a bank that competes on branch convenience needs ATM and branch-network systems, while one that competes on low-cost digital service needs mobile and API platforms. A common planning technique is the **critical success factors (CSF)** method: ask executives for the few things that *must* go right (for a wallet: user growth, fraud rate, merchant coverage, settlement uptime), then derive the information needed to monitor them. Other tools: the **balanced scorecard** (financial, customer, internal process, learning and growth perspectives), and **IT governance** (who decides, who funds, how benefits are measured).

## 2.7 Business process reengineering and change

**Business process reengineering (BPR)** (Hammer and Champy) is the fundamental rethinking and radical redesign of business processes to achieve dramatic improvements in cost, quality, speed and service. Instead of automating the existing steps (*paving the cow path*), BPR asks why each step exists. Example: a district land-registration office whose process had nine hand-offs and four signatures is redesigned so that a single case officer handles the file with a shared system, cutting the cycle from 15 days to 3. **Continuous improvement** (Kaizen, Six Sigma) gives smaller, steady gains. BPR often fails because of resistance, unclear ownership and loss of the knowledge embedded in the old process, so it needs sponsorship, communication and training.

## Chapter summary

- Strategic information systems change the firm's competitive position; sustainability requires data, relationships, scale or processes that rivals cannot easily copy.
- Porter's five forces (entrants, suppliers, buyers, substitutes, rivalry) can be scored; HHI measures concentration, and a merger raises it by twice the product of the shares.
- The value chain locates IS value in primary and support activities and in the interfaces with suppliers and customers.
- Generic strategies are cost leadership, differentiation and focus; switching costs, lock-in and network effects reinforce them.
- Alignment, CSFs and BPR connect IS investment to business goals.

## Practice

1. List Porter's five forces and say how the Internet changes buyer power.
2. For the weights and intensities in the scoring table, what would the pressure score be if buyer power were 3 instead of 5?
3. Compute the HHI for shares 40, 30, 20 and 10.
4. Two firms with 20% and 30% shares merge. By how much does the HHI rise?
5. Name the five primary and four support activities of the value chain.
6. Give one IS for each of cost leadership, differentiation and focus.
7. Using Metcalfe's law, by what factor does the number of possible connections grow when users go from 500 to 1,000?
8. What is a switching cost? Give an example from banking.
9. Why is a website not a competitive advantage by itself?
10. State three reasons BPR projects fail.

::: note Answers and worked solutions
**1.** Entrants, suppliers, buyers, substitutes, rivalry. The Internet makes prices and alternatives visible, so buyer power rises.
**2.** The buyer-power term changes from 0.25 × 5 = 1.25 to 0.25 × 3 = 0.75, so the total falls by 0.50 from 3.95 to 3.45.
**3.** 1,600 + 900 + 400 + 100 = 3,000.
**4.** 2 × 20 × 30 = 1,200.
**5.** Primary: inbound logistics, operations, outbound logistics, marketing and sales, service. Support: firm infrastructure, human resources, technology development, procurement.
**6.** Cost leadership: ERP and e-procurement. Differentiation: a personalised mobile app. Focus: an e-commerce site for one niche or region.
**7.** n(n − 1)/2 gives 124,750 for 500 users and 499,500 for 1,000 users: a factor of about 4.
**8.** The cost (money, time, risk, retraining) of moving to a competitor; for example re-registering salary accounts, standing orders and digital banking credentials at another bank.
**9.** Rivals can build one next month; advantage needs something hard to copy such as data, brand or process.
**10.** Resistance to change, no executive sponsor, loss of tacit knowledge, unrealistic targets, inadequate training.
:::
