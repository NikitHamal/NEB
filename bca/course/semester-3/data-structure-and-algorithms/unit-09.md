---
subject: Data Structure and Algorithms
grade: BCA Semester 3
unit: 9
title: Searching
hours: 5
area: BCA 201 · Data Structure and Algorithms · Unit 9
---

**Searching** is finding the record whose key equals a target, or discovering that none exists. How fast it is depends on how the data is organised: unordered, sorted, in a tree, or in a hash table.

::: key What this unit gives you
- Sequential and binary search with exact comparison counts.
- Tree search and the general (multiway) search tree.
- Hashing: hash functions, collisions, and four collision-resolution techniques.
- A tested program and an efficiency comparison.
:::

## 9.1 Introduction to searching

A search is **successful** if the key is found and **unsuccessful** otherwise. Essentials: a **key** to compare, a way to **compare** keys, and the **organisation** of the data. We count comparisons. **Internal** search works in memory; **external** search on files (indexes, B-trees).

## 9.2 Sequential (linear) search

Examine items one by one from the start. Works on any list, sorted or not. Best case 1 comparison, worst n, average about (n + 1)/2 for a successful search; **O(n)**. A **sentinel** (placing the key at the end of the array) removes the loop's bounds test. If the list is sorted, an unsuccessful search can stop early at the first larger item.

## 9.3 Binary search

Requires a **sorted array** with random access. Compare the key with the middle element; discard the half that cannot contain it; repeat. Each step halves the range, so at most ⌊log₂ n⌋ + 1 comparisons: **O(log n)**.

::: example Worked example: find 55 in [3, 8, 15, 21, 34, 55, 89]
lo = 0, hi = 6: mid = 3 → 21 < 55 → lo = 4. lo = 4, hi = 6: mid = 5 → 55 found after **2** comparisons. Searching 40: mid = 3 (21 < 40, lo = 4); mid = 5 (55 > 40, hi = 4); mid = 4 (34 < 40, lo = 5 > hi = 4) → not found after 3 comparisons. For 1,000,000 items the worst case is 20 comparisons.
:::

## 9.4 Tree search and the general search tree

Searching a **BST** (Unit 7) is binary search on a pointer structure: O(h), i.e. O(log n) when balanced, and unlike a sorted array it supports O(log n) insertion and deletion. A **general (multiway) search tree** generalises this: a node holds k sorted keys and k + 1 child pointers, and all keys in child i lie between key i − 1 and key i. Searching a node picks the right child by comparing against its keys. B-trees (Unit 7) are the balanced version and are used for database indexes, since each node is one disk block. A **trie** is a related tree that searches strings character by character.

## 9.5 Hashing

**Hashing** computes the storage position directly from the key with a **hash function** h(key), giving **O(1)** average search, insertion and deletion. The table has *m* slots; the **load factor** α = n/m measures fullness.

### Hash functions

| Method | Idea | Example (m = 100 or as stated) |
|---|---|---|
| **Division** | h(k) = k mod m (choose m prime, avoid powers of 2) | 1234 mod 97 = 70 |
| **Mid-square** | square the key, take middle digits | 123² = 15129 → 51 |
| **Folding** | split the key into parts and add | 123456 → 12 + 34 + 56 = 102 → 02 |
| **Multiplication** | h(k) = ⌊m·(k·A mod 1)⌋, A ≈ 0.618 | spreads clustered keys |

A good hash function is fast and spreads keys uniformly.

### Collisions

A **collision** occurs when two keys hash to the same slot; it is unavoidable once keys outnumber slots (pigeonhole principle). Resolution techniques:

| Technique | How | Weakness |
|---|---|---|
| **Separate chaining** | each slot holds a linked list of all keys that hash there | extra memory for pointers; lists can grow |
| **Linear probing** (open addressing) | try h(k)+1, h(k)+2, … (mod m) | **primary clustering**: long runs of occupied slots |
| **Quadratic probing** | try h(k)+1², h(k)+2², … | secondary clustering; may not reach every slot |
| **Double hashing** | step size from a second hash h₂(k) | most uniform; needs h₂(k) ≠ 0 and coprime with m |

With open addressing the table can fill up, and deleting needs a **tombstone** marker (just emptying the slot would break the probe chain of other keys). Expected probes for linear probing: about ½(1 + 1/(1−α)) for success; chaining averages 1 + α/2.

::: example Worked example: m = 7, h(k) = k mod 7, keys 50, 700, 76, 85, 92, 73, 101
50 → 1. 700 → 0. 76 → 6. 85 → 1 is taken → slot 2. 92 → 1, 2 taken → slot 3. 73 → 3 taken → slot 4. 101 → 3, 4 taken → slot 5.
**Linear probing table:** [700, 50, 85, 92, 73, 101, 76]. Searching 101 follows the same probe path 3, 4, 5.
**Chaining:** slot 0: 700; slot 1: 50 → 85 → 92; slot 3: 73 → 101; slot 6: 76; others empty.
:::

```c
#include <stdio.h>
#include <stdlib.h>

#define M 7

int linear_search(const int a[], int n, int key, int *cmp) {
    for (int i = 0; i < n; i++) { (*cmp)++; if (a[i] == key) return i; }
    return -1;
}
int binary_search(const int a[], int n, int key, int *cmp) {
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2; (*cmp)++;
        if (a[mid] == key) return mid;
        if (a[mid] < key) lo = mid + 1; else hi = mid - 1;
    }
    return -1;
}

typedef struct Node { int key; struct Node *next; } Node;

int main(void) {
    int a[] = {3, 8, 15, 21, 34, 55, 89}, c;
    c = 0; int p = linear_search(a, 7, 55, &c); printf("linear : 55 at %d, %d comparisons\n", p, c);
    c = 0; p = binary_search(a, 7, 55, &c);     printf("binary : 55 at %d, %d comparisons\n", p, c);
    c = 0; p = binary_search(a, 7, 40, &c);     printf("binary : 40 at %d, %d comparisons\n", p, c);

    int keys[] = {50, 700, 76, 85, 92, 73, 101};
    int lp[M]; for (int i = 0; i < M; i++) lp[i] = -1;
    Node *ch[M] = {0};
    for (int i = 0; i < 7; i++) {
        int k = keys[i], h = k % M, probes = 1;
        while (lp[h] != -1) { h = (h + 1) % M; probes++; }
        lp[h] = k;
        printf("key %3d -> home %d, stored in slot %d after %d probe(s)\n", k, k % M, h, probes);
        Node *n = malloc(sizeof *n); n->key = k; n->next = NULL;      /* chaining: append to chain */
        Node **pp = &ch[k % M]; while (*pp) pp = &(*pp)->next; *pp = n;
    }
    printf("linear probing table:");
    for (int i = 0; i < M; i++) printf(" %d", lp[i]);
    printf("\nchaining:\n");
    for (int i = 0; i < M; i++) {
        printf("  slot %d:", i);
        for (Node *n = ch[i]; n; n = n->next) printf(" %d", n->key);
        printf("\n");
    }
    return 0;
}
```
```output
linear : 55 at 5, 6 comparisons
binary : 55 at 5, 2 comparisons
binary : 40 at -1, 3 comparisons
key  50 -> home 1, stored in slot 1 after 1 probe(s)
key 700 -> home 0, stored in slot 0 after 1 probe(s)
key  76 -> home 6, stored in slot 6 after 1 probe(s)
key  85 -> home 1, stored in slot 2 after 2 probe(s)
key  92 -> home 1, stored in slot 3 after 3 probe(s)
key  73 -> home 3, stored in slot 4 after 2 probe(s)
key 101 -> home 3, stored in slot 5 after 3 probe(s)
linear probing table: 700 50 85 92 73 101 76
chaining:
  slot 0: 700
  slot 1: 50 85 92
  slot 2:
  slot 3: 73 101
  slot 4:
  slot 5:
  slot 6: 76
```

## 9.6 Efficiency comparison

| Method | Requirement | Search (avg / worst) | Insert | Note |
|---|---|---|---|---|
| Sequential, array | none | O(n) / O(n) | O(1) at end | simple, any order |
| Binary, sorted array | sorted | O(log n) / O(log n) | O(n) | needs random access |
| BST | none | O(log n) / O(n) | O(log n) / O(n) | ordered traversal |
| AVL / B-tree | self-balancing | O(log n) / O(log n) | O(log n) | guaranteed, disk-friendly |
| Hash table | good hash, α < ~0.7 | O(1) / O(n) | O(1) | no ordering, no range queries |

## Formula and fact sheet

- Linear search: average (n+1)/2, worst n. Binary search: ≤ ⌊log₂ n⌋ + 1.
- Load factor α = n/m. Division hash: k mod m (m prime).
- Linear probing: (h + i) mod m; quadratic: (h + i²) mod m; double: (h₁ + i·h₂) mod m.
- Chaining: expected chain length α; open addressing needs α < 1 and tombstones for deletion.

## Chapter summary

- Sequential search is general but O(n); binary search is O(log n) but needs sorted, indexable data.
- Trees add O(log n) updates; multiway trees suit disks.
- Hashing gives O(1) average by computing the address; collisions are handled by chaining or probing.
- Choose by data order, update rate and whether ordered or range queries are needed.

## Practice

1. Compare sequential and binary search (requirements, cost).
2. Trace binary search for 23 in [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]; how many comparisons?
3. Insert 12, 18, 13, 2, 3, 23, 5, 15 into a table of size 10 with h(k) = k mod 10 using linear probing.
4. Do Q3 with separate chaining.
5. What is a collision? Give two ways to resolve it and one drawback of each.
6. Compute the folding hash of 987654 (two-digit parts, m = 100).
7. Why can't we simply empty a slot when deleting in open addressing?
8. For a million sorted items, how many comparisons does binary search need at most?
9. Why does a hash table not support range queries efficiently?

::: note Answers and worked solutions
**1.** Sequential: no ordering needed, O(n). Binary: sorted array needed, O(log n).
**2.** lo 0, hi 9: mid 4 = 16 < 23 → lo 5. mid 7 = 56 > 23 → hi 6. mid 5 = 23 found: **3 comparisons**.
**3.** 12 → 2. 18 → 8. 13 → 3. 2 → 2 taken → 3 taken → 4. 3 → 3 taken → 4 taken → 5. 23 → 3, 4, 5 taken → 6. 5 → 5 taken, 6 taken → 7. 15 → 5, 6, 7 taken → 8 taken → 9. Table: slot 2: 12, 3: 13, 4: 2, 5: 3, 6: 23, 7: 5, 8: 18, 9: 15; slots 0, 1 empty.
**4.** Slot 2: 12 → 2; slot 3: 13 → 3 → 23; slot 5: 5 → 15; slot 8: 18. (Order within a chain is arrival order.)
**5.** Two keys map to the same slot. Chaining (extra memory/pointers); linear probing (primary clustering).
**6.** 98 + 76 + 54 = 228 → keep two digits (mod 100) → **28**.
**7.** An emptied slot would end the probe sequence of keys that were placed after it, making them unfindable; a tombstone marks "deleted, keep probing".
**8.** ⌊log₂ 1,000,000⌋ + 1 = **20**.
**9.** Hashing scatters neighbouring keys across the table, so keys in a range are not stored together.
:::
