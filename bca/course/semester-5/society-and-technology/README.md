# Society and Technology — BCA 305 (Semester V, 3 credits)

How technology and society shape each other: theories (determinism, social construction, actor-network), adoption and diffusion models (TAM, Rogers, logistic and Bass curves), the digital divide and the Digital Nepal Framework, Nepali cyber and IT law (Electronic Transactions Act 2063, Individual Privacy Act 2075, Copyright Act 2059, National Cyber Security Policy 2080), e-governance (National ID, Nagarik App, GIDC, Palika systems, digital signatures and PKI), cyberethics and algorithmic fairness, and e-waste and green computing. 45 teaching hours (the old CASO102 was a first-year course; the revised list moves it to Semester V as BCA 305).

| Unit | Title | Hours |
|---|---|---|
| 1 | Technology and Society: Theories and History | 6 |
| 2 | Technology Adoption and Diffusion of Innovations | 7 |
| 3 | The Digital Divide and Digital Nepal | 7 |
| 4 | Cyber and IT Law in Nepal | 8 |
| 5 | e-Governance in Nepal | 7 |
| 6 | Cyberethics, Privacy and Algorithmic Fairness | 5 |
| 7 | E-Waste, Green Computing and Sustainable Technology | 5 |

## Verification

`bca/tools/check_society.py` recomputes every number and inserts it by token substitution (`--fill`); `--verify` checks every value is present and no placeholder is left. Covered: Moore's-law table, Cronbach's alpha and the TAM regression (numpy least squares, R²), Rogers' categories from the normal CDF, logistic and Bass diffusion tables with the peak time ln(q/p)/(p+q) (the continuous peak formula is cross-checked against the yearly table), Lorenz curve and Gini and the min-max composite index, the ETA penalty table and combined-exposure sums, EGDI and the e-service cost-benefit estimate, confusion-matrix fairness metrics (demographic parity, disparate impact, equal opportunity, equalized odds, predictive parity, and the FPR identity that proves the impossibility result), and PUE, energy, cost, carbon and service-life tables, plus the practice answers. The digital-signature program in Unit 5 is executed by `fill_script_outputs.py` and its output inserted.

## Source and honesty

No TU unit list for BCA 305 / CASO102 was retrieved; the seven units are a reconstruction from the topics named in the course brief. **Statutory penalties:** the table in Unit 4 lists only ETA sections 44, 45, 46, 47 and 52, on which four secondary sources (bankingtayari.com, attorneynepal.com, courtmarriageinnepal.com.np, lawalpine.com, read this session) agree; for sections 48 to 55 those sources disagree with each other (amounts and section numbers), so they are deliberately **not tabulated** and the primary text of the Act (Nepal Law Commission) must be checked. Descriptions of the National ID, Nagarik App, GIDC, GIOMS and Palika systems are general; the Digital Nepal Framework's eight sectors and the Acts' names and years are from public knowledge. All province-level, survey, e-government and e-waste figures are **invented for teaching**.
