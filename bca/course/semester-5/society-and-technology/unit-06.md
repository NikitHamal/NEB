---
subject: Society and Technology
grade: BCA Semester 5
unit: 6
title: Cyberethics, Privacy and Algorithmic Fairness
hours: 5
area: BCA 305 · Society and Technology · Unit 6
---

A bank deploys a loan-scoring model. It is accurate overall, yet when the data are split by urban and rural applicants, the model rejects far more of the *creditworthy* rural applicants. Nobody wrote a discriminatory line of code; the pattern came from the data. This unit begins with the ethical frameworks and everyday issues of cyberspace (privacy, misinformation, harassment, intellectual honesty), then shows that fairness in automated decisions can be *measured*, with confusion matrices, and that different fairness definitions can conflict.

::: key What this unit gives you
- Ethical theories and professional codes applied to computing.
- Privacy, surveillance, misinformation, cyber-bullying, plagiarism and netiquette.
- Fairness metrics: demographic parity, disparate impact, equal opportunity, equalized odds, predictive parity, all computed from one example; why they conflict.
- Transparency, accountability and a checklist for responsible systems.
:::

## 6.1 Ethical frameworks

Ethics asks what we *ought* to do. Four frameworks help structure computing dilemmas:

| Framework | Test | Application to a surveillance feature |
|---|---|---|
| **Consequentialism / utilitarianism** | Choose the action with the best overall consequences | Does the safety gain outweigh the privacy loss for everyone affected? |
| **Deontology (duty)** | Follow rules and respect persons as ends, never merely as means | Does it treat users as people with rights, and would it be acceptable as a universal rule? |
| **Virtue ethics** | Do what a person of good character would do | Would an honest, caring engineer build it? |
| **Care and justice** | Attend to relationships, power and fairness | Who is most vulnerable, and are they heard? |

Professional codes make these concrete. The **ACM Code of Ethics** (contribute to society, avoid harm, be honest, be fair and non-discriminatory, respect privacy, honour confidentiality, give proper credit for intellectual property, respect copyright, and work only within competence) and the **IEEE Code** commit members to the public interest first. A sound procedure for a dilemma: state the facts; list the stakeholders; identify the principles and laws in play; list options; choose and justify; and seek review. If instructed to do something wrong, *refuse, document and escalate*.

## 6.2 Everyday cyberethics

- **Privacy and surveillance.** Collect the minimum, with consent, and protect it; beware of **function creep** (data collected for one purpose used for another) and of the permanence of online records. Workplace monitoring needs proportionality and notice.
- **Misinformation and disinformation.** *Misinformation* is false content spread without intent to deceive; *disinformation* is spread deliberately. Fast sharing, algorithmic amplification and low-cost fakes (including **deepfakes**) increase the problem. Verify before sharing: check the source, date and other reports, and search the image in reverse.
- **Cyber-bullying and online harassment.** Persistent, public and anonymous, it harms mental health and falls disproportionately on women and minorities; report to platforms and the police cyber bureau, and keep evidence.
- **Plagiarism and academic integrity.** Using others' words, code or data without credit is dishonest; cite sources, follow licences, and treat AI-generated text and code as a tool whose use must be disclosed according to course rules.
- **Intellectual property and piracy.** Respect licences (Unit 4).
- **Netiquette.** Be courteous, respect others' time and privacy, do not shout, think before you post.
- **Digital footprint and identity.** What you post is searchable and durable; manage privacy settings.
- **Social engineering and honesty.** Do not exploit trust to obtain access; this is both unethical and often an offence.

## 6.3 Algorithmic bias: where it comes from

Bias in automated systems can enter at several points: **historical bias** (the world that produced the data was unequal), **representation bias** (some groups are under-sampled), **measurement bias** (the proxy measured is not the quantity of interest: arrests instead of crime), **label bias** (past human decisions are copied as labels), **aggregation bias** (one model for groups that differ) and **deployment bias** (use in a setting different from the training one). *Removing the sensitive attribute does not remove the bias*, because other variables (postal code, device type, name) act as **proxies**. Risks arise in credit, hiring, policing, health triage and content ranking.

## 6.4 Measuring fairness

Consider a loan-approval model evaluated on past applicants for whom the true outcome (repaid or defaulted) is known. "Positive" means *predicted creditworthy (approved)*, and the actual positives are those who truly would repay. For two groups the counts are:

| Group | TP | FP | FN | TN | n |
|---|---|---|---|---|---|
| Urban applicants (A) | 80 | 20 | 10 | 90 | 200 |
| Rural applicants (B) | 30 | 10 | 30 | 80 | 150 |

From each group's counts we compute the standard rates.

| Metric | Group A | Group B |
|---|---|---|
| Selection rate (TP+FP)/n | 0.500 | 0.267 |
| True-positive rate TP/(TP+FN) | 0.889 | 0.500 |
| False-positive rate FP/(FP+TN) | 0.182 | 0.111 |
| Precision TP/(TP+FP) | 0.800 | 0.750 |
| Accuracy | 0.850 | 0.733 |
| Base rate of repayers | 0.450 | 0.400 |

Several fairness criteria use these numbers:

- **Demographic parity (statistical parity):** selection rates should be equal. The difference is **0.233** (A minus B).
- **Disparate impact ratio:** B's selection rate ÷ A's = **0.533**. The US "four-fifths rule" of thumb asks for at least 0.8, so this model **fails** the test.
- **Equal opportunity:** qualified applicants should have the same chance of approval in both groups: equal TPR. The TPR gap is **0.389**: an urban applicant who would repay is approved far more often than an equally good rural one.
- **Equalized odds:** both TPR *and* FPR equal across groups. The FPR gap is **0.071**, and the TPR gap is large, so equalized odds is violated.
- **Predictive parity (calibration by group):** the precision (of those approved, the fraction who repay) should be equal. The gap is **0.050**, which is small: the approvals are about equally reliable in both groups.

So the *same model* looks nearly fair by predictive parity and clearly unfair by equal opportunity and demographic parity. What is happening is that the model is cautious with rural applicants: it approves few of them (low selection rate), makes few false approvals (lower FPR) but misses half the creditworthy ones (TPR 0.5).

### Why you cannot have everything

The base rate of repayers differs between the groups (0.45 and 0.40 here). The confusion-matrix identity FPR = [p/(1 − p)] × [(1 − PPV)/PPV] × TPR (p is the base rate) shows that **when base rates differ, a model cannot have equal PPV, equal TPR and equal FPR at once** unless it is perfect. If group B had group A's precision (0.8) and the same TPR as A (0.889), its FPR would have to be **0.148**, not A's 0.182. This is the core of the *impossibility results* of Chouldechova and of Kleinberg and colleagues: fairness criteria express different moral claims, and the choice among them is a value judgement for the people affected, not a technical one.

### What can be done

- **Pre-processing:** re-sample or re-weight the data; collect more data from under-represented groups.
- **In-processing:** add a fairness constraint or penalty to the training objective.
- **Post-processing:** choose different decision thresholds per group to equalise a chosen metric (legally and ethically sensitive).
- **Process:** involve affected communities, document the data and model (*datasheets* and *model cards*), test on subgroups before deployment, monitor after, provide **explanations** and a **human appeal** route, and allow the system to be switched off.

## 6.5 Transparency and accountability

Automated decisions affecting rights (credit, benefits, hiring, bail) need: **transparency** (people know a system is used), **explainability** (reasons in understandable terms), **contestability** (a way to challenge), **accountability** (a named person or organisation is responsible) and **auditability** (logs and independent testing). Regulators in several countries now require impact assessments for high-risk systems. In Nepal there is no dedicated AI statute at the time of writing; the general law (Constitution, Privacy Act, Criminal Code, consumer rules and NRB's directives) still applies to the harm caused by automated systems.

## Chapter summary

- Utilitarian, duty, virtue and care frameworks, plus the ACM and IEEE codes, structure ethical decisions; refuse, document and escalate when asked to do wrong.
- Everyday cyberethics covers privacy, misinformation, harassment, plagiarism, piracy and netiquette.
- Bias enters through history, sampling, measurement, labels, aggregation and deployment; proxies defeat attribute removal.
- Fairness metrics (demographic parity, disparate impact, equal opportunity, equalized odds, predictive parity) are computed from group confusion matrices and can conflict when base rates differ.
- Responsible systems are transparent, explainable, contestable, accountable and audited.

## Practice

1. Apply the four ethical frameworks to a facial-recognition door lock in a school.
2. Differentiate misinformation and disinformation.
3. List four sources of algorithmic bias.
4. Why does deleting the "gender" column not make a model gender-blind?
5. For a group with TP = 40, FP = 10, FN = 20, TN = 30, compute the selection rate, TPR, FPR and precision.
6. State the disparate impact ratio and the four-fifths rule.
7. What is the difference between equal opportunity and equalized odds?
8. Why can a model not satisfy predictive parity, equal TPR and equal FPR when base rates differ?
9. Name three process steps that make an automated decision system more accountable.
10. What should an engineer do when told to hide a known bias from a client?

::: note Answers and worked solutions
**1.** Utilitarian: security benefit versus privacy and error costs. Duty: consent and rights of students. Virtue: what a caring, honest engineer would build. Care/justice: who is vulnerable (students with poor recognition accuracy) and who decides.
**2.** Misinformation is false content shared without intent to deceive; disinformation is spread deliberately.
**3.** Historical, representation, measurement, label (also aggregation and deployment) bias.
**4.** Other variables (location, name, device) are correlated with gender and act as proxies.
**5.** n = 100. Selection = (40 + 10)/100 = **0.50**. TPR = 40/60 = **0.667**. FPR = 10/40 = **0.25**. Precision = 40/50 = **0.80**.
**6.** DI = selection rate of the protected group ÷ that of the reference group; the four-fifths rule of thumb wants DI ≥ 0.8.
**7.** Equal opportunity equalises only the TPR; equalized odds equalises both TPR and FPR.
**8.** With different base rates the identity FPR = p/(1 − p) × (1 − PPV)/PPV × TPR forces FPR to differ if PPV and TPR are equal, unless the classifier is perfect.
**9.** Documentation (model cards), subgroup testing and monitoring, explanation and appeal routes (also audits and a named owner).
**10.** Refuse, document the concern, escalate internally and, if necessary, to the appropriate authority; honesty to the client is a professional duty.
:::
