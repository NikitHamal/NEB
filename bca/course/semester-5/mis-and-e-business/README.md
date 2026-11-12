# MIS and e-Business — BCA 304 (Semester V, 3 credits)

Information systems in the enterprise (TPS, MIS, DSS, ESS, KMS), strategy and competitive advantage (Porter's five forces, value chain), enterprise applications (ERP, CRM, SCM and the bullwhip effect), decision support (decision tables, EMV, decision trees, business intelligence, knowledge management), e-business models and Nepal's digital payment architecture, security and control, and the financial justification of information systems (NPV, IRR, payback, ROI, TCO, break-even). 45 teaching hours (TU CACS301 carries the same subject name in the old list; the revised list numbers it BCA 304).

| Unit | Title | Hours | TU CACS outline unit |
|---|---|---|---|
| 1 | Introduction to E-Commerce  | 7 | TU unit 1 |
| 2 | The Network Infrastructure for E-Commerce (I-Way, WAP, wireless technologies, wireless security) | 8 | TU unit 2 |
| 3 | Information Systems in the Enterprise (data, CBIS, TPS, MIS, DSS, EIS) | 6 | TU unit 3 |
| 4 | Strategy and Competitive Advantage | 7 | extension |
| 5 | Enterprise Applications: ERP, CRM, SCM; international systems, outsourcing and offshoring; implementation challenges | 8 | TU unit 3 |
| 6 | Decision Support, Business Intelligence and Knowledge Management | 8 | extension |
| 7 | e-Business, Digital Payments: cards, micropayments, e-checks, ACH, wallets, crypto, Nepal case study | 8 | TU unit 5 |
| 8 | Security and Control: terminology, requirements, malware, Heartbleed, DDoS, botnets, social engineering, fraud | 6 | TU unit 4 |
| 9 | Developing and Justifying Information Systems | 4 | extension |
| 10 | Launching a Successful E-Commerce Website (plan, domain, hosting, cPanel, content, design, SEO) | 10 | TU unit 6 |

## Verification

`bca/tools/check_mis.py` recomputes every number in the book and inserts it into the unit text by token substitution (`--fill`), then `--verify` confirms that every computed value is in the book and no placeholder is left. It covers: the weighted five-forces score and HHI (and the 2·s₁·s₂ merger rule), bullwhip factors per stage and a week-by-week order-up-to trace, EOQ (cross-checked by brute-force minimisation of the cost curve), safety stock and reorder point, payoff-table EMV, EVPI, maximin/Laplace/Hurwicz/minimax-regret, the pilot decision tree, decision-table completeness and consistency by enumerating all 2³ combinations, NPV/IRR (bisection, NPV at the IRR is zero)/payback/discounted payback/PI/ROI, five-year TCO at present value, break-even, SLE/ALE, password entropy and guess times, funnel/CAC/LTV, multilateral netting (net positions sum to zero) and weighted vendor scoring, plus the hand-computed practice answers.

## Source and honesty

Session 25 retrieved the TU unit list for BCA 304 (six units: Introduction to E-Commerce, Network Infrastructure for E-Commerce, Introduction to MIS with SCM/CRM/international systems, E-Commerce Security and Fraud, E-payment Systems, Launching a Successful EC Website) and the book now covers every topic named there (Units 2 and 10 are new; Units 5, 7 and 8 were extended). Units 4, 6 and 9 are extensions beyond the TU list. The Nepali payment-system description (NRB under the Payment and Settlement Act 2075, PSO/PSP licences, NCHL's NPI and ConnectIPS, Fonepay, wallets) is from general knowledge of the sector and is flagged in the text as subject to change; the figures in all worked examples are **invented for teaching** and are not Nepali market data.
