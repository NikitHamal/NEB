# MIS and e-Business — BCA 304 (Semester V, 3 credits)

Information systems in the enterprise (TPS, MIS, DSS, ESS, KMS), strategy and competitive advantage (Porter's five forces, value chain), enterprise applications (ERP, CRM, SCM and the bullwhip effect), decision support (decision tables, EMV, decision trees, business intelligence, knowledge management), e-business models and Nepal's digital payment architecture, security and control, and the financial justification of information systems (NPV, IRR, payback, ROI, TCO, break-even). 45 teaching hours (TU CACS301 carries the same subject name in the old list; the revised list numbers it BCA 304).

| Unit | Title | Hours |
|---|---|---|
| 1 | Information Systems in the Enterprise | 6 |
| 2 | Strategy and Competitive Advantage | 7 |
| 3 | Enterprise Applications: ERP, CRM and Supply Chain Management | 8 |
| 4 | Decision Support, Business Intelligence and Knowledge Management | 8 |
| 5 | e-Business, e-Commerce and Digital Payments in Nepal | 8 |
| 6 | Security and Control of Information Systems | 4 |
| 7 | Developing and Justifying Information Systems | 4 |

## Verification

`bca/tools/check_mis.py` recomputes every number in the book and inserts it into the unit text by token substitution (`--fill`), then `--verify` confirms that every computed value is in the book and no placeholder is left. It covers: the weighted five-forces score and HHI (and the 2·s₁·s₂ merger rule), bullwhip factors per stage and a week-by-week order-up-to trace, EOQ (cross-checked by brute-force minimisation of the cost curve), safety stock and reorder point, payoff-table EMV, EVPI, maximin/Laplace/Hurwicz/minimax-regret, the pilot decision tree, decision-table completeness and consistency by enumerating all 2³ combinations, NPV/IRR (bisection, NPV at the IRR is zero)/payback/discounted payback/PI/ROI, five-year TCO at present value, break-even, SLE/ALE, password entropy and guess times, funnel/CAC/LTV, multilateral netting (net positions sum to zero) and weighted vendor scoring, plus the hand-computed practice answers.

## Source and honesty

No TU unit list for BCA 304 / CACS301 was retrieved in this session. The seven units follow the standard shape of an MIS-and-e-business course (the topics named in the course brief) with a reconstructed 45-hour split. The Nepali payment-system description (NRB under the Payment and Settlement Act 2075, PSO/PSP licences, NCHL's NPI and ConnectIPS, Fonepay, wallets) is from general knowledge of the sector and is flagged in the text as subject to change; the figures in all worked examples are **invented for teaching** and are not Nepali market data.
