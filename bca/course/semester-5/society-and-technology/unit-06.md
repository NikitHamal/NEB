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

## 6.6 Seeing the ideas: faces, pipelines, rates and trade-offs

Automated decisions are made by machines that look at people. Plate 6.1 shows the issue at three scales: the researcher whose 2018 audit of commercial face-analysis systems showed that error rates differed sharply across groups, an access gate that identifies passengers by their face, and a police van that scans crowds. A system that works well on average can still fail a particular group.

```photogrid label="6.1" cols="3" ratio="1.0" caption="Algorithms that look at people. (a) Joy Buolamwini, the researcher who with Timnit Gebru published the 2018 Gender Shades audit showing that commercial face-analysis systems made far more errors on darker-skinned women than on lighter-skinned men. (b) A facial-recognition fare gate in a metro station in China: the passenger must register a face to confirm identity. (c) A live facial-recognition van used by police in London. Each use needs a lawful purpose, accuracy testing on every group and a human route to appeal."
@ photo id="bca-st/buolamwini" cap="Auditing the algorithm"
fit 1.0
focus 0.5 0.7
@ photo id="bca-st/facegate" cap="Face-recognition gate"
fit 1.0
focus 0.6 0.5
@ photo id="bca-st/facevan" cap="Live recognition van"
fit 1.0
focus 0.5 0.5
```

```svgfig label="6.1" caption="Where bias enters an automated system. Bias is not only a coding error: it can come from the world that made the data, from who is in the sample, from what is measured, from past labels, from one-size-fits-all models and from the place where the system is finally used."
f = Fig(580, 214)
st = [("World", "historical\nbias", ROSE, RED), ("Sampling", "representation\nbias", SAND, AMBER), ("Measuring", "measurement\nbias (proxies)", SAND, AMBER), ("Labelling", "label bias:\npast decisions", SAND, AMBER), ("Model", "aggregation\nbias", BLUE, NAVY), ("Use", "deployment\nbias", ROSE, RED)]
for i, (t, s, fl, sk) in enumerate(st):
    x = 6 + i * 96
    f.box(x, 14, 86, 74, t + "\n" + s, fill=fl, stroke=sk, size=9.6, bold=True)
    if i < 5:
        f.arrow([(x + 86, 51), (x + 96, 51)], color=SLATE)
f.box(6, 104, 568, 42, "Removing the sensitive attribute is not enough: postal code, device type, school or name can act as a proxy for it", fill="#f8fafc", stroke=SLATE, size=10)
f.box(6, 156, 568, 46, "Example: a loan model trained on past approvals copies the old refusal of rural applicants (label bias),\nthen reads \"village code\" as a risk signal (proxy) and is deployed in new districts (deployment bias)", fill=ROSE, stroke=RED, size=9.6)
```

```svgfig label="6.2" caption="The loan model of section 6.4 as confusion matrices (counts of applicants). Urban group A: 80 correct approvals, 20 wrong approvals, 10 missed good applicants, 90 correct refusals. Rural group B: 30, 10, 30 and 80. In group B half of the people who would repay (30 of 60) are refused."
f = Fig(580, 190)
def mat(x, name, v, cols):
    f.text(x + 115, 12, name, size=10.5, color=NAVY, bold=True)
    f.text(x + 62, 30, "predicted approve", size=8.6, color=SLATE); f.text(x + 168, 30, "predicted refuse", size=8.6, color=SLATE)
    for (r, c), (lab, val) in zip([(0, 0), (0, 1), (1, 0), (1, 1)], v):
        fl, sk = cols[lab]
        f.box(x + 8 + c * 106, 38 + r * 56, 100, 50, lab + "\n" + str(val), fill=fl, stroke=sk, size=10.5, bold=True)
cols = {"TP": (MINT, TEAL), "FN": (ROSE, RED), "FP": (SAND, AMBER), "TN": (BLUE, NAVY)}
mat(8, "Group A (urban, n = 200)", [("TP", 80), ("FN", 10), ("FP", 20), ("TN", 90)], cols)
mat(300, "Group B (rural, n = 150)", [("TP", 30), ("FN", 30), ("FP", 10), ("TN", 80)], cols)
f.text(290, 164, "rows: truly repays (top) / truly defaults (bottom).  TPR = TP/(TP+FN): A = 80/90 = 0.889, B = 30/60 = 0.500", size=9.2, color=SLATE)
f.text(290, 180, "A is approved more often: 100 of 200 (0.500) against 40 of 150 (0.267)", size=9.2, color=RED, bold=True)
```

```svgfig label="6.3" caption="Five fairness rates for the two groups, from the table of section 6.4. The same model looks fair on precision (gap 0.050) and unfair on selection rate (gap 0.233) and true-positive rate (gap 0.389). The disparate impact ratio is 0.267 / 0.500 = 0.533, below the four-fifths rule of thumb of 0.8."
f = Fig(580, 250)
rows = [("Selection rate", 0.500, 0.267), ("True-positive rate", 0.889, 0.500), ("False-positive rate", 0.182, 0.111), ("Precision", 0.800, 0.750), ("Accuracy", 0.850, 0.733)]
f.box(380, 4, 12, 10, "", fill=BLUE, stroke=NAVY); f.text(396, 10, "A urban", size=9.4, color=NAVY, anchor="start", bold=True)
f.box(466, 4, 12, 10, "", fill=SAND, stroke=AMBER); f.text(482, 10, "B rural", size=9.4, color=AMBER, anchor="start", bold=True)
for i, (n, a, b) in enumerate(rows):
    y = 22 + i * 40
    f.text(6, y + 20, n, size=10, color=NAVY, bold=True, anchor="start")
    f.box(150, y, a * 330, 16, "", fill=BLUE, stroke=NAVY); f.text(150 + a * 330 + 5, y + 9, "%.3f" % a, size=9.6, color=NAVY, bold=True, anchor="start")
    f.box(150, y + 18, b * 330, 16, "", fill=SAND, stroke=AMBER); f.text(150 + b * 330 + 5, y + 27, "%.3f" % b, size=9.6, color=AMBER, bold=True, anchor="start")
f.text(290, 242, "Disparate impact = 0.267 / 0.500 = 0.533 (< 0.8)", size=10, color=RED, bold=True)
```

```svgfig label="6.4" caption="Why every fairness criterion cannot hold together. With base rates 0.45 and 0.40, giving group B the same precision (0.800) and true-positive rate (0.889) as group A would force B's false-positive rate to 0.148, not A's 0.182 and not B's actual 0.111. Equalising one rate moves another: the choice is a value judgement for the people affected."
f = Fig(580, 176)
rows = [("A actual FPR", 0.182, BLUE, NAVY), ("B actual FPR", 0.111, SAND, AMBER), ("B FPR needed if PPV and TPR match A", 0.148, ROSE, RED)]
for i, (n, v, fl, sk) in enumerate(rows):
    y = 12 + i * 38
    f.text(8, y + 14, n, size=9.8, color=NAVY, bold=True, anchor="start")
    f.box(250, y, v * 1500, 24, "", fill=fl, stroke=sk)
    f.text(250 + v * 1500 + 6, y + 13, "%.3f" % v, size=10.4, color=sk, bold=True, anchor="start")
f.box(8, 128, 564, 40, "FPR = [p / (1 - p)] x [(1 - PPV) / PPV] x TPR  (p = base rate of repayers):\nunequal base rates make equal PPV, TPR and FPR impossible for any imperfect model", fill="#f8fafc", stroke=SLATE, size=9.8)
```

### 6.6.1 Eight practices for building fair and responsible systems

1. **State the purpose and the people affected.** Write down what decision the system makes and who is affected, including the least powerful group. A loan model for a Nepali microfinance lender must name rural and women borrowers. A clear purpose prevents function creep later.
2. **Check the data before training.** Count how many examples each group has and how they were collected. If rural applicants are 10% of the data, the model will learn their patterns poorly. Collect more data or reweight before blaming the algorithm.
3. **Do not trust proxies.** Postal code, device model, school name or surname can stand in for caste, region or gender. Test whether removing the sensitive attribute really removes its effect. Often it does not.
4. **Measure by group, not only overall.** An accuracy of 85% can hide a true-positive rate of 50% for one group. Report selection rate, TPR, FPR and precision for every group. A table like Figure 6.3 should be part of every evaluation.
5. **Choose the fairness criterion openly.** The criteria conflict when base rates differ, so someone must decide which error matters most. For loans, missing a creditworthy applicant (low TPR) may be the harm to avoid. Record who made the choice and why.
6. **Keep a human appeal route.** A refused applicant should get reasons in simple Nepali and a person to ask. Automated refusals without appeal are the most harmful. A short review form at the bank counter is better than none.
7. **Document and audit.** Keep a datasheet for the data and a model card for the model: purpose, limits, tested groups and known failures. Log decisions so an independent auditor can retest them. Re-check after deployment because the world changes.
8. **Respect privacy and law.** Collect the minimum personal data, with consent, and secure it. The Constitution, the Individual Privacy Act 2075 and NRB directives still apply to automated systems. Switch the system off when it causes harm.

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


## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is algorithmic bias? Explain six sources of bias in automated decision systems.**

*Introduction.* Algorithmic bias is a systematic pattern in which an automated system produces worse outcomes for some groups than for others. It usually comes from the data and the setting, not from a line of code that mentions a group (section 6.3, Figure 6.1).

1. **Historical bias.** The world that produced the data was unequal, so accurate data copy the inequality.
2. **Representation bias.** Some groups are under-sampled, so the model learns them poorly. Face-analysis audits found higher error rates for darker-skinned women.
3. **Measurement bias.** The measured proxy is not the real target, for example arrests instead of crime.
4. **Label bias.** Past human decisions become the labels, so old prejudice is learned, for example past loan refusals.
5. **Aggregation bias.** One model is used for groups that differ.
6. **Deployment bias.** The system is used in a setting different from the training one, for example a city model used in hill districts.

| Source | Example in a loan model |
|---|---|
| Historical | Rural women were rarely given loans |
| Representation | Only 10% of records are rural |
| Label | Old refusals treated as "default" |
| Deployment | Trained in Kathmandu, used in Karnali |

*Remark.* Removing the sensitive attribute does not remove bias because proxies such as postal code carry the same information.

*Conclusion.* Bias must be searched for at every stage, not only in the model.

**Q2 (5 marks). A hiring screen was tested on 100 male (M) and 100 female (F) past applicants. M: TP 40, FP 10, FN 20, TN 30. F: TP 15, FP 5, FN 15, TN 65. Compute the selection rate, TPR, FPR and precision for each group, the demographic parity difference and the disparate impact ratio, and comment.**

*Introduction.* Fairness is judged by comparing error and selection rates between groups (section 6.4, Figure 6.3). "Positive" means shortlisted.

| Metric | Formula | M | F |
|---|---|---|---|
| Selection rate | (TP+FP)/n | 50/100 = 0.500 | 20/100 = 0.200 |
| TPR | TP/(TP+FN) | 40/60 = 0.667 | 15/30 = 0.500 |
| FPR | FP/(FP+TN) | 10/40 = 0.250 | 5/70 = 0.071 |
| Precision | TP/(TP+FP) | 40/50 = 0.800 | 15/20 = 0.750 |

*Parity measures.* Demographic parity difference = 0.500 - 0.200 = **0.300**. Disparate impact ratio = 0.200 / 0.500 = **0.400**, far below the four-fifths rule of thumb of 0.8, so the screen fails that test.

*Equal opportunity.* The TPR gap is 0.667 - 0.500 = **0.167**: a qualified woman is less likely to be shortlisted than a qualified man. The precision gap is only 0.050, so shortlists are about equally reliable.

*Comment.* The base rates of suitable applicants differ (0.60 and 0.30), which is why selection rates differ even for a good model; but the TPR gap and the 0.400 ratio are large enough to require investigation of the data, features and threshold.

*Conclusion.* The model looks acceptable on precision but fails on selection and opportunity, so it should not be deployed unreviewed.

**Q3 (10 marks). A bank wants to use an automated model to approve or refuse loans. Discuss the ethical issues using ethical frameworks, explain how fairness would be measured, why the measures conflict, and what safeguards should be required.**

*Introduction.* Automated credit decisions affect livelihoods, so they raise questions of ethics, fairness and accountability. A model that is accurate overall can still treat groups unequally (sections 6.1 to 6.5).

*Ethical frameworks.* **Utilitarian:** do the benefits of faster, cheaper lending outweigh the harm of wrongful refusals to rural applicants? **Deontological:** applicants are persons with rights, not mere data points, so reasons and appeal are duties. **Virtue ethics:** would an honest, caring banker accept this model? **Care and justice:** who is most vulnerable and was she heard?

*Measuring fairness.* From each group's confusion matrix compute selection rate, TPR, FPR and precision (Figures 6.2 and 6.3). In the worked example, selection rates are 0.500 (urban) and 0.267 (rural), so the disparate impact is 0.533, below 0.8; the TPR gap is 0.389, so a creditworthy rural applicant is approved far less often; the precision gap is only 0.050.

| Criterion | What it requires | Result in example |
|---|---|---|
| Demographic parity | Equal selection rates | Fails (gap 0.233) |
| Equal opportunity | Equal TPR | Fails (gap 0.389) |
| Equalized odds | Equal TPR and FPR | Fails |
| Predictive parity | Equal precision | Nearly met (gap 0.050) |

*Why they conflict.* When base rates differ (0.45 and 0.40), FPR = [p/(1-p)] x [(1-PPV)/PPV] x TPR, so equal precision, TPR and FPR cannot all hold for an imperfect model (Figure 6.4). The choice is a value judgement for those affected.

*Safeguards.* Purpose statement; data audit; testing by group; open choice of criterion; explanation in simple Nepali; human appeal; documentation (datasheet, model card); monitoring after deployment; privacy under the Constitution and the Individual Privacy Act 2075; and a switch-off rule (section 6.6.1).

*Conclusion.* The bank may use the model only if it measures outcomes by group, chooses and publishes its fairness criterion, keeps a human appeal route and stays accountable for harm.
