# Data Structure and Algorithms — BCA 201 (Semester III, 3 credits)

Old code CACS201 (2074 curriculum, Semester III, 3 credits, 3 h theory + 3 h practical per week).

| Unit | Title | Hours (syllabus) |
|---|---|---|
| 1 | Introduction to Data Structure | 2 |
| 2 | The Stack | 3 |
| 3 | Queue | 3 |
| 4 | List | 2 |
| 5 | Linked Lists | 5 |
| 6 | Recursion | 4 |
| 7 | Trees (BST, AVL, B-tree, Huffman, game tree) | 5 |
| 8 | Sorting (incl. Big-O) | 5 |
| 9 | Searching and hashing | 5 |
| 10 | Graphs | 5 |
| 11 | Algorithms (deterministic/non-deterministic, divide and conquer, serial/parallel, heuristic/approximate) | 5 |

## Verification

Every complete C program in the units (21 of them) was compiled with `gcc -std=c11 -Wall` and run; the `output` blocks are the programs' real output, inserted by `bca/tools/fill_c_outputs.py` and re-checked by `bca/tools/check_c_examples.py`. Hand-traced answers (AVL rotations, Huffman lengths, hash tables, Dijkstra, Kruskal, sorting traces) were checked against those runs or recomputed by hand.

## Source and honesty

The unit list and hours are the TU **CACS201** syllabus as reproduced on benchpartner.com, notebahadur.com and tupapers.com (see `bca/SOURCES.md`). The revised BCA 201 PDF itself was not retrievable; the revised subject is described by the same sources as unchanged in content. Laboratory work in that syllabus (stack, queues, TOH/Fibonacci, linked lists, AVL, merge sort, searching, graph traversal) is covered by the tested programs. The book is long (about 21,000 words including code) because the syllabus has eleven units; no unit was padded.
