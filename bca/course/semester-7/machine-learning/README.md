# Machine Learning — BCA 405 (Semester VII, Elective I, 3 credits)

Study notes for the TU Machine Learning elective (course code CACS456 in the TU outline, Year IV, 6 hours a week: 3 theory and 3 practical). Five units follow the outline and its hours; the laboratory and mini-project guidance is in Unit 5, Section 5.9.

| Unit | Title | Hours |
|---|---|---|
| 1 | Introduction to Machine Learning and the Theory of Learning | 10 |
| 2 | Supervised Learning, Regression, Perceptron, Neural Networks, Trees and SVM | 11 |
| 3 | Bayesian and Instance-Based Learning | 11 |
| 4 | Unsupervised Learning and Dimensionality Reduction | 10 |
| 5 | Measures for Performance Evaluation of ML Algorithms | 8 |

## Verification

Every Python block is executed by `bca/tools/fill_script_outputs.py` and its real output is inserted; the programs use only NumPy with fixed seeds. Hand calculations (Hoeffding N = 738, least-squares line, perceptron trace, PlayTennis entropy 0.940 and gains 0.247/0.152/0.048/0.029, SVM margin 2.83, naive Bayes 0.795, the alarm network P(B|J,M) = 0.284, k-means trace, PCA eigenvalues 30.385 and 6.615, ROC AUC 0.84, confidence intervals) are recomputed by those programs or by the arithmetic checks in the model answers.

## Extensions beyond the printed outline (session 44)

Sections added for depth and exam practice, each with executed code and model answers: 1.10 concept learning (Find-S, candidate elimination, inductive bias), 1.11 data preparation and leakage; 2.9 gradient descent variants and learning rate (Fig 2.5), 2.10 Gini, CART and pruning, 2.11 bagging, random forests and AdaBoost; 3.7 naive Bayes for text with Laplace smoothing, 3.8 locally weighted regression and case-based reasoning, 3.9 choosing k and the curse of dimensionality; 4.9 DBSCAN, 4.10 Gaussian mixtures and EM, 4.11 LDA versus PCA; 5.11 F-beta, MCC, kappa and log loss, 5.12 McNemar and paired t-tests, 5.13 leakage in cross-validation. Hand checks: AdaBoost round 1 (error 0.3, alpha 0.424), candidate elimination trace (Mitchell, table 2.3), the smoothed spam scores (-8.566 and -9.146).

## Source and honesty

Units, topics and hours follow the TU CACS456 outline reproduced at notebahadur.com (text books: Mitchell, *Machine Learning*; Marsland, *Machine Learning: An Algorithmic Perspective*; reference: Flach). The elective list of the revised curriculum names Machine Learning among the Elective I options; each college runs a subset, so check which elective your college offers. Unit 5 in the outline has no hour figure; 8 hours is an estimate from the total. The VC bound is stated, not proved. Dataset-based laboratory tasks are described, not supplied.
