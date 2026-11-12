---
subject: MIS and e-Business
grade: BCA Semester 5
unit: 4
title: Strategy and Competitive Advantage
hours: 7
area: BCA 304 · MIS and e-Business · Unit 4
---

When eSewa launched in 2009 it did not have the best technology in the world; it had the first useful position: merchants and users joined because other users had joined, and each new merchant made the wallet more valuable to the next customer. That is a *strategic* use of an information system: IT is not just making an existing operation cheaper, it is changing the competitive position of the firm. This unit gives you the standard tools for reasoning about such positions: Porter's five forces, the value chain, generic strategies, and the economics of switching costs and network effects, each with numbers you can recompute.

::: key What this unit gives you
- Porter's five forces and a weighted way to score industry pressure; market concentration with the HHI.
- The value chain and where information systems add value in it.
- Generic strategies and the IT moves that support them.
- Switching costs, lock-in and network effects (Metcalfe's law); strategic alignment and business process reengineering.
:::

## 4.1 Strategy and the role of information systems

A **strategy** is a plan for achieving a goal in a competitive environment: where to compete (which customers and products) and how to win. Information systems enter at three levels. **Operational excellence**: do the same things better, cheaper and faster. **New products, services and business models**: do new things (internet banking, mobile wallets). **Customer and supplier intimacy**: know customers so well that they stay. At the extreme, IT enables **business model innovation**: a ride-hailing app such as Pathao owns no taxis, a marketplace such as Daraz holds little stock of its own.

An information system gives **competitive advantage** when it lets the firm do something rivals cannot easily copy. The test is sustainability: a technology that any competitor can buy next month (a website, a POS terminal) is a *requirement to compete*, not an advantage. Advantage comes from the combination of technology with unique data, relationships, processes and brand.

## 4.2 Porter's five forces

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

## 4.3 The value chain

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

## 4.4 Generic strategies and supporting IT

Porter identified three generic ways to outperform rivals:

| Strategy | Idea | Information systems support | Risk |
|---|---|---|---|
| **Cost leadership** | Be the lowest-cost producer in the industry | Automation, ERP, e-procurement, process control | A rival with lower costs or a technological shift |
| **Differentiation** | Offer something customers value and will pay extra for | Personalisation, mobile app, quality data, innovation | Imitation; uniqueness not valued |
| **Focus** | Serve a narrow segment (by region, customer type) better than broad rivals | Segment analytics, niche e-commerce | Segment shrinks or is entered by large firms |

Other IT-based strategic moves:

- **Lock-in** through **switching costs**: once a firm's data, staff skills and integrations are built around a system, changing is expensive, so customers stay.
- **Alliances and partnerships**: shared platforms among banks (interbank switches, Unit 7), loyalty programmes.
- **Innovation first-mover**: the first mobile wallet or the first online ticketing service gains users before rivals.
- **Mass customisation**: producing individualised products at near-mass-production cost through configurable online orders.

## 4.5 Network effects and Metcalfe's law

Some products become more valuable as more people use them: a telephone, a payment network, a marketplace. **Metcalfe's law** is a model, not a law of nature: the *number of possible connections* among n users is n(n − 1)/2 and the network's value is approximated as proportional to it. With 1,000 users there are **4,99,500** possible pairs; with 2,000 users, **19,99,000**, about four times as many for twice the users. The practical lessons: the *early* growth phase is hard (the value to the first users is almost zero, so firms subsidise it with cashback), and once a network is ahead the *winner takes most*. The law overstates value, because most possible connections are never used; later models suggest value proportional to n log n.

::: caution Not every advantage is permanent
A strategic IS can become a **strategic necessity**: ATMs and internet banking once distinguished a bank, and now a bank without them cannot compete. Before investing, ask: *can a rival copy it within a year? Does it rest on our data, relationships or scale? What happens if we do not invest?*
:::

## 4.6 Aligning IS strategy with business strategy

An **IS strategy** states which systems the organisation will build or buy and why. It must be **aligned** with business strategy: a bank that competes on branch convenience needs ATM and branch-network systems, while one that competes on low-cost digital service needs mobile and API platforms. A common planning technique is the **critical success factors (CSF)** method: ask executives for the few things that *must* go right (for a wallet: user growth, fraud rate, merchant coverage, settlement uptime), then derive the information needed to monitor them. Other tools: the **balanced scorecard** (financial, customer, internal process, learning and growth perspectives), and **IT governance** (who decides, who funds, how benefits are measured).

## 4.7 Business process reengineering and change

**Business process reengineering (BPR)** (Hammer and Champy) is the fundamental rethinking and radical redesign of business processes to achieve dramatic improvements in cost, quality, speed and service. Instead of automating the existing steps (*paving the cow path*), BPR asks why each step exists. Example: a district land-registration office whose process had nine hand-offs and four signatures is redesigned so that a single case officer handles the file with a shared system, cutting the cycle from 15 days to 3. **Continuous improvement** (Kaizen, Six Sigma) gives smaller, steady gains. BPR often fails because of resistance, unclear ownership and loss of the knowledge embedded in the old process, so it needs sponsorship, communication and training.

## 4.8 Seeing strategy: forces, concentration, chains and networks

Strategy is full of numbers: weights, shares and counts. The figures below turn them into pictures. The plate shows the author of the five-forces and value-chain models, and a container port that is the physical end of a value chain.

```photogrid label="4.1" cols="2" ratio="1.25" caption="(a) Michael Porter of Harvard Business School, who published the five-forces framework in 1979 and the value chain in 1985. (b) Container cranes unloading a ship: for a trading firm the value chain is physical, and every day of delay in inbound logistics becomes cost and stock-out risk. A Nepali importer in Kathmandu depends on ports such as Kolkata, whose delays are outside its control; this is why supplier power and logistics appear in the analysis."
@ photo id="bca304/porter" cap="Michael Porter"
fit 1.25
focus 0.5 0.62
@ photo id="bca304/ship" cap="Container port, inbound logistics"
fit 1.25
focus 0.5 0.5
```

```svgfig label="4.1" caption="Porter's five forces for a mobile-wallet business, scored as in section 4.2. The weighted score of each force is weight x intensity: entrants 0.20 x 4 = 0.80, suppliers 0.15 x 2 = 0.30, buyers 0.25 x 5 = 1.25, substitutes 0.25 x 4 = 1.00, rivalry 0.15 x 4 = 0.60. The total is 3.95 out of 5, a hostile industry. Buyers carry the greatest weighted pressure because switching a wallet costs the user nothing."
f = Fig(580, 232)
f.box(220, 92, 140, 48, "Rivalry\n0.15 x 4 = 0.60", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(220, 8, 140, 48, "New entrants\n0.20 x 4 = 0.80", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(220, 176, 140, 48, "Substitutes\n0.25 x 4 = 1.00", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(10, 92, 140, 48, "Suppliers\n0.15 x 2 = 0.30", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(430, 92, 140, 48, "Buyers\n0.25 x 5 = 1.25", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(290, 56), (290, 92)], color=SLATE); f.arrow([(290, 176), (290, 140)], color=SLATE)
f.arrow([(150, 116), (220, 116)], color=SLATE); f.arrow([(430, 116), (360, 116)], color=SLATE)
f.text(10, 40, "Total weighted score", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(10, 58, "0.80 + 0.30 + 1.25 + 1.00 + 0.60", size=10.5, color=SLATE, anchor="start")
f.text(10, 76, "= 3.95 out of 5", size=12, color=RED, bold=True, anchor="start")
```

```svgfig label="4.2" caption="Market concentration measured by the Herfindahl-Hirschman Index (HHI), the sum of squared percentage shares. Four wallets with shares 45, 30, 15 and 10 give 2025 + 900 + 225 + 100 = 3250, a highly concentrated market (above 2500 in the common convention). If C and D merge into a 25 percent firm the index becomes 2025 + 900 + 625 = 3550, a rise of 300 points; regulators usually examine a merger that adds more than 100 points in an already concentrated market."
f = Fig(580, 170)
def bars(x, shares, title, total, cols):
    f.text(x + 130, 14, title, size=11, color=NAVY, bold=True)
    for i, (n, s) in enumerate(shares):
        y = 28 + i * 28
        f.text(x, y + 13, n, size=10, color=SLATE, bold=True, anchor="start")
        f.box(x + 40, y, s * 4, 22, f"{s}%  ({s*s})" if s >= 15 else "", fill=cols[i % len(cols)], stroke=NAVY, size=9.5, bold=True, r=3)
        if s < 15: f.text(x + 46 + s * 4, y + 12, f"{s}%  ({s*s})", size=9.5, color=NAVY, bold=True, anchor="start")
    f.text(x + 130, 150, f"HHI = {total}", size=12, color=RED, bold=True)
bars(10, [("A", 45), ("B", 30), ("C", 15), ("D", 10)], "Before", 3250, [BLUE, MINT, SAND, ROSE])
bars(300, [("A", 45), ("B", 30), ("C+D", 25)], "After C and D merge", 3550, [BLUE, MINT, SAND])
```

```svgfig label="4.3" caption="Porter's value chain. Five primary activities (inbound logistics, operations, outbound logistics, marketing and sales, service) sit on four support activities (infrastructure, human resources, technology, procurement). The margin is what is left of the price after the cost of all activities. IT acts in every box: ERP in operations, a CRM in marketing and sales, tracking in logistics, e-recruitment in HR. A firm gains an advantage by doing an activity cheaper or in a way that customers value more."
f = Fig(580, 214)
sup = ["Firm infrastructure", "Human resources", "Technology development", "Procurement"]
for i, s in enumerate(sup):
    f.box(10, 10 + i * 28, 460, 24, s, fill=BLUE, stroke=NAVY, size=10.5, bold=True)
pri = [("Inbound\nlogistics", MINT), ("Operations", MINT), ("Outbound\nlogistics", MINT), ("Marketing\nand sales", MINT), ("Service", MINT)]
for i, (t, fl) in enumerate(pri):
    f.box(10 + i * 92, 128, 90, 56, t, fill=fl, stroke=TEAL, size=10, bold=True)
f.poly([(476, 10), (570, 69), (476, 128)], fill=ROSE, stroke=RED, label="Margin", lx=526, ly=69, size=11)
f.text(10, 204, "Primary activities run left to right; IT supports every box.", size=10, color=SLATE, bold=True, anchor="start")
```

```svgfig label="4.4" caption="Metcalfe's law. A network of n users has n(n - 1) / 2 possible connections: 10 users give 45, 20 give 190 and 100 give 4,950. Doubling the users from 10 to 20 more than quadruples the links (45 to 190, that is 4.2 times). This is why a wallet or messaging service with more users is worth more to each new user, and why the first wallet to reach most of the market is hard to dislodge."
f = Fig(580, 200)
ax = Axes(f, 60, 14, 480, 150, (0, 100), (0, 5000))
ax.grid(20, 1000).axes("", "")
ax.curve(lambda n: n * (n - 1) / 2, 0, 100, color=RED, sw=2.6)
for n in (10, 20, 100):
    ax.pt(n, n * (n - 1) / 2, f"n={n}: {int(n*(n-1)/2):,}", dx=-14 if n == 100 else 10, dy=-8 if n == 100 else (-14 if n == 10 else 18), anchor="end" if n == 100 else "start")
f.text(300, 190, "users n", size=10.5, color=SLATE, bold=True)
f.text(12, 110, "links", size=10, color=SLATE, bold=True, anchor="start")
```

### 2.8.1 Eight ways information systems create competitive advantage

1. **Lower cost.** Automating routine work removes labour and error from each unit sold. A wallet company that verifies customers online avoids a costly branch. Lower cost lets a firm lower prices or earn more on the same price.
2. **Differentiation.** A unique feature makes customers prefer one product, for example a service with bill payment, ticketing and remittance in one app. Differentiation lets a firm charge more or win more users at the same price. The feature must be hard for others to copy quickly.
3. **Focus on a niche.** Systems make it economical to serve a small group well. A Nepali agricultural app that gives farmers prices and weather in Nepali serves a group big firms ignore. Deep knowledge of the niche creates loyalty.
4. **Raising switching costs.** When customers store history, contacts and saved cards in a system, leaving is a nuisance. A bank app with years of saved payees keeps its customers. Care is needed: forced lock-in without service quality causes resentment.
5. **Building network effects.** Each new user adds value to all the others, as Figure 4.4 shows. A ride-hailing or messaging platform that reaches most users becomes the natural choice. The first to reach scale often wins.
6. **Improving supplier and buyer relations.** Electronic data exchange with suppliers shortens lead times and cuts stock. Sharing sales data with a supplier lets it plan production better. Closer links make rivals' offers less attractive to partners.
7. **New products and services.** Information turns into a product: online banking, e-ticketing, digital library membership. A theatre that sells seats online reaches buyers who would never visit the counter. New products open new markets.
8. **Better decisions and speed.** Real-time data helps a firm respond to demand, price and risk faster than a rival. An importer that tracks stock daily reorders before a stock-out. Speed in decisions turns into service quality and lower waste.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain Porter's five forces. For a mobile-wallet business the weights and intensities are entrants 0.20 x 4, suppliers 0.15 x 2, buyers 0.25 x 5, substitutes 0.25 x 4, rivalry 0.15 x 4. Find the total score and interpret it.**

*Introduction.* Porter's five forces framework analyses the attractiveness of an industry by looking at five sources of competitive pressure (section 4.2, Figure 4.1).

1. **Threat of new entrants.** Low entry barriers (little capital, easy licences) let new firms in and push profits down.
2. **Bargaining power of suppliers.** Suppliers with few alternatives can raise prices; for a wallet, banks and telecom networks are important suppliers.
3. **Bargaining power of buyers.** Customers who can switch at no cost force prices down and demand more service.
4. **Threat of substitutes.** Another way of meeting the same need, such as bank apps, cash or cards, limits the price.
5. **Rivalry among competitors.** Many similar firms competing on price and promotion reduce profit.
6. **Calculation.** 0.80 + 0.30 + 1.25 + 1.00 + 0.60 = **3.95 out of 5**.
7. **Interpretation.** A score above 3.5 shows a hostile industry with weak profits; buyers (1.25) and substitutes (1.00) are the biggest worry, so the firm should raise switching costs and differentiate.

*Conclusion.* The five forces turn a vague idea of competition into a scored analysis that points to the strategy to follow.

**Q2 (5 marks). Four firms in a market have shares 45, 30, 15 and 10 percent. Calculate the HHI, state what it shows, and find the change if the two smallest firms merge.**

*Introduction.* The Herfindahl-Hirschman Index measures market concentration as the sum of the squares of the percentage shares (section 4.2, Figure 4.2).

1. **Formula.** HHI = s1 squared + s2 squared + and so on, where s is the percentage share, so the value runs from near 0 to 10,000.
2. **Before the merger.** 45 squared = 2025; 30 squared = 900; 15 squared = 225; 10 squared = 100. HHI = 2025 + 900 + 225 + 100 = **3250**.
3. **Meaning.** Above 2500 the market is highly concentrated: a few firms dominate and customers have little choice.
4. **After the merger.** The two firms form one with 25 percent, so HHI = 2025 + 900 + 625 = **3550**.
5. **Change.** 3550 - 3250 = **300** points; a change above 100 points in a concentrated market normally attracts regulator attention.

| Case | Shares | HHI |
|---|---|---|
| Before | 45, 30, 15, 10 | 3250 |
| After | 45, 30, 25 | 3550 |

*Conclusion.* The HHI shows that a merger of small firms can raise concentration noticeably, which is why regulators examine such mergers.

**Q3 (10 marks). Explain Porter's value chain and the generic strategies. Show how information systems support each primary and support activity.**

*Introduction.* Michael Porter described a firm as a chain of activities that each add cost and value. The margin is the difference between what customers pay and the cost of the activities. A firm gains a competitive advantage by performing activities at lower cost or in a way that customers value more (sections 2.3 and 2.4, Figures 2.3 and 2.1).

1. **Inbound logistics.** Receiving and storing inputs. IT: inventory and supplier systems, barcode scanning, EDI.
2. **Operations.** Turning inputs into the product. IT: ERP, production planning, quality tracking.
3. **Outbound logistics.** Delivering to customers. IT: order tracking, route planning, GPS.
4. **Marketing and sales.** Making customers aware and taking orders. IT: CRM, e-commerce, social media analytics.
5. **Service.** After-sales support. IT: help-desk systems, chat, complaint tracking.
6. **Support activities.** Firm infrastructure (accounting, MIS), human resources (payroll and e-recruitment), technology development (design software, research databases) and procurement (e-tendering, supplier portals).
7. **Generic strategies.** Cost leadership (lowest cost: automation, scale), differentiation (unique features or service: personalised apps, quality) and focus (a narrow segment served better than anyone else).
8. **Using the chain.** Draw the chain for the firm, find the activities that are costly or that customers value, and apply IT there; compare the margin with rivals.

| Strategy | Aim | IT example |
|---|---|---|
| Cost leadership | Lowest cost | Automated order processing |
| Differentiation | Unique value | Personalised app, loyalty data |
| Focus | Serve a niche | Farmer-price app in Nepali |

*Conclusion.* The value chain shows where a firm makes or loses money, and information systems can improve every box. Combined with a clear generic strategy, they turn IT spending into a lasting advantage.
