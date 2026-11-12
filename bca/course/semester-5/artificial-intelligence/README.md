# Artificial Intelligence — BCA 302 (Semester V, 3 credits)

Introduces the basics of artificial intelligence: problem solving, knowledge representation, learning, neural networks, natural language processing and expert systems with machine vision. 45 teaching hours (the revised list numbers it BCA 302; the subject is new in the revised programme and has no counterpart in the 2074 core list, though the TU BCA outline with the same six units exists as an elective).

| Unit | Title | Hours |
|---|---|---|
| 1 | Introduction to AI and Intelligent Agents | 6 |
| 2 | Problem Solving Methods (uninformed, informed and local search, CSP, minimax, alpha-beta) | 9 |
| 3 | Knowledge Representation and Reasoning (rules, semantic nets, frames, propositional and first-order logic, resolution, Bayesian networks) | 15 |
| 4 | Learning (decision trees, naive Bayes, k-NN, genetic algorithms) | 4 |
| 5 | Neural Networks and Natural Language Processing (perceptron, back-propagation, Hopfield, NLP) | 7 |
| 6 | Expert Systems and Machine Vision | 4 |

## Verification

`bca/tools/check_ai.py` recomputes and asserts every number used in the book: the BFS, DFS, UCS, greedy and A* traces on the seven-node graph (with admissibility and consistency checked against the true costs-to-go computed by Dijkstra from the goal), iterative-deepening node counts, 8-puzzle heuristic values and A* expansion counts for a generated start state (and the 31-move hardest instance), the 18 colourings of the Australia map, minimax and alpha-beta on three trees (with the pruned leaves logged) and the full tic-tac-toe tree (549,946 nodes, 255,168 terminal; 18,297 nodes with alpha-beta), truth-table entailment, propositional resolution and unification, Bayes' rule, the burglar-alarm network by enumeration, entropy and information gain and naive Bayes on PlayTennis, the Laplace-smoothed spam filter, k-NN distances, the perceptron trace on AND and its failure on XOR, a back-propagation step with a **finite-difference gradient check** (largest discrepancy 1e-11), an XOR network trained with a fixed seed, edit distances, bigram, TF-IDF and cosine values and a CYK parse. `--verify` checks that key values appear in the unit files. Every ```python block was executed with `fill_script_outputs.py`.

**What the verification caught while writing:** (1) my first hand-written minimax value for the eight-leaf tree was 3; the script gave 5 (the tree has MAX nodes below the MIN nodes); (2) my first 8-puzzle start state was unsolvable (parity), so `A*` returned nothing; the book uses a generated solvable start with optimal length 16; (3) the number of ham words in the spam example was 9, not the 8 first written, which changed the ham score from 0.0017 to 0.0015; (4) the perceptron error count in epoch 3 is 3, not 2; (5) a Hopfield network of 8 neurons storing two orthogonal patterns does **not** repair a two-bit corruption (it falls into the mirror image of the second pattern); the book now says so and uses it to illustrate the 0.14 N capacity rule instead of showing a rosy example; (6) a malformed `struct` format and an over-claim that the resolution program finds the "same" proof as the hand proof were fixed.

## Source and honesty

The unit list, topics and hours of Units 1, 3, 4, 5 and 6 follow the TU BCA *Artificial Intelligence* outline as published on benchpartner.com and bcanotesnepal.com (Unit 1 Introduction 6 h, Unit 3 Knowledge Representation and Reasoning 15 h, Unit 4 Learning 4 h, Unit 5 Neural Networks and NLP 7 h, Unit 6 Expert System and Machine Vision 4 h); the hours of Unit 2 (Problem Solving Methods) were not in the retrieved text and are the 9 that complete the 45 (see `bca/SOURCES.md`). The revised BCA 302 syllabus PDF itself was not retrieved. The order follows Russell and Norvig, *Artificial Intelligence: A Modern Approach*; the PlayTennis data set is Mitchell's *Machine Learning*; the burglar-alarm network is the standard textbook example. All text is original. Historical claims (MYCIN, XCON, DENDRAL) are summarised from general knowledge and not machine-checkable.
