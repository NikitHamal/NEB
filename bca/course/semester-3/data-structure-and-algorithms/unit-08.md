---
subject: Data Structure and Algorithms
grade: BCA Semester 3
unit: 8
title: Sorting
hours: 5
area: BCA 201 · Data Structure and Algorithms · Unit 8
---

**Sorting** arranges items in a defined order so that searching, merging and reporting become cheap. It is the most studied problem in computing, and it shows clearly how algorithm design decides efficiency.

::: key What this unit gives you
- Internal versus external sorting, stability and in-place sorting.
- Insertion, selection, bubble, quick, merge, radix, shell, binary-insertion and heap sort with traces.
- Big-O, Big-Ω and Big-Θ notation, and the efficiency comparison.
- One tested program that runs all of them.
:::

## 8.1 Introduction

- **Internal sort:** all data fits in main memory (arrays). **External sort:** data is on disk in blocks (too large for memory); the standard method is **external merge sort**: sort memory-sized chunks into *runs*, write them out, then merge runs with a k-way merge.
- **Stable:** equal keys keep their original relative order (needed when sorting by several keys in turn). **In-place:** uses O(1) extra memory.
- Cost is measured in **comparisons** and **data movements**.

## 8.2 Big-O notation

**f(n) = O(g(n))** if there are constants c, n₀ with f(n) ≤ c·g(n) for all n ≥ n₀: an **upper bound**. **Ω** is a lower bound and **Θ** a tight bound (both). We state the worst case unless told otherwise.

::: example Worked example
f(n) = 3n² + 5n + 7. For n ≥ 1: 3n² + 5n + 7 ≤ 3n² + 5n² + 7n² = 15n², so f(n) = O(n²) with c = 15, n₀ = 1. It is also Ω(n²), hence Θ(n²). Nested loops of n iterations each give n² steps; a loop that halves n each time gives log₂ n steps.
:::

## 8.3 The elementary sorts

**Insertion sort.** Keep a sorted prefix; take the next item and slide it left past larger items. Best case (already sorted) **O(n)**; worst/average **O(n²)**; stable, in place, excellent for small or nearly sorted data. **Binary insertion sort** finds the slot by binary search (O(log n) comparisons per item) but still shifts O(n) items.

**Selection sort.** Repeatedly select the minimum of the unsorted part and swap it to the front. Always n(n−1)/2 comparisons, but only n − 1 swaps; not stable in the usual form.

**Bubble sort (exchange sort).** Repeatedly compare adjacent pairs and swap if out of order; after pass k the k largest are in place. With an "already sorted" flag the best case is O(n); worst O(n²); stable.

**Shell sort.** Insertion sort on elements a *gap* apart, with the gap shrinking (n/2, n/4, …, 1). Early passes move items long distances. Runs in about O(n^1.3) to O(n²) depending on the gap sequence; in place, not stable.

::: example Worked example: bubble sort on 5 1 4 2 8
Pass 1: (5,1) swap → 1 5 4 2 8; (5,4) swap → 1 4 5 2 8; (5,2) swap → 1 4 2 5 8; (5,8) no → largest 8 settled. Pass 2: (1,4) no; (4,2) swap → 1 2 4 5 8; (4,5) no. Pass 3: no swaps → sorted. Insertion sort on the same data: [5] | 1 → [1 5] | 4 → [1 4 5] | 2 → [1 2 4 5] | 8 → [1 2 4 5 8].
:::

## 8.4 Quick sort

**Divide and conquer.** Pick a **pivot**; **partition** so that smaller items are left of it and larger right; sort both sides recursively. Average **O(n log n)**, in place (O(log n) stack), not stable. **Worst case O(n²)** when the pivot is always the smallest or largest (e.g. first-element pivot on sorted input); random or median-of-three pivots make this rare.

::: example Worked example: Lomuto partition, pivot = last element, on 8 3 7 1 5 (pivot 5)
i = −1. j=0: 8 > 5 skip. j=1: 3 < 5, i=0, swap a[0],a[1] → 3 8 7 1 5. j=2: 7 skip. j=3: 1 < 5, i=1, swap a[1],a[3] → 3 1 7 8 5. Finally swap pivot with a[i+1]=a[2] → 3 1 **5** 8 7. The pivot is in its final position; recurse on [3 1] and [8 7].
:::

## 8.5 Merge sort

Split the array in halves, sort each recursively, **merge** the two sorted halves in linear time. T(n) = 2T(n/2) + n gives **O(n log n) in every case**; stable; needs O(n) extra space. It is the basis of external sorting.

## 8.6 Heap sort

A **max-heap** is a complete binary tree stored in an array in which every parent ≥ its children (node i has children 2i+1 and 2i+2). **Build** the heap bottom-up in O(n), then repeat: swap the root (the maximum) with the last element, shrink the heap, **sift down** the new root. **O(n log n)** always, in place, not stable. A heap is also the best implementation of a **priority queue** (Unit 3): insert and extract-max both O(log n).

## 8.7 Radix sort

Radix sort never compares keys. It sorts **digit by digit**, least significant first, using a stable sort (counting or bucket) for each digit. For n numbers of d digits in base b: **O(d·(n + b))**, which is linear when d is constant. Stable; needs O(n + b) extra space.

::: example Worked example: 170, 45, 75, 90, 802, 24, 2, 66
Pass on units digit: 170 90 802 2 24 45 75 66. Pass on tens digit: 802 2 24 45 66 170 75 90. Pass on hundreds digit: 2 24 45 66 75 90 170 802.
:::

## 8.8 Programs: all the sorts

The first program runs the four O(n²)-style sorts on one array and counts comparisons; the second runs the O(n log n) sorts and radix sort on the same data.

```c
#include <stdio.h>
#include <string.h>
#define N 8
static long cmp;

void show(const char *name, int *a) {
    printf("%-10s", name);
    for (int i = 0; i < N; i++) printf("%3d", a[i]);
    printf("\n");
}
void insertion(int *a) { for (int i = 1; i < N; i++) { int k = a[i], j = i - 1; while (j >= 0 && (cmp++, a[j] > k)) { a[j+1] = a[j]; j--; } a[j+1] = k; } }
void selection(int *a) { for (int i = 0; i < N-1; i++) { int m = i; for (int j = i+1; j < N; j++) { cmp++; if (a[j] < a[m]) m = j; } int t = a[i]; a[i] = a[m]; a[m] = t; } }
void bubble(int *a)    { for (int p = 0; p < N-1; p++) for (int j = 0; j < N-1-p; j++) { cmp++; if (a[j] > a[j+1]) { int t = a[j]; a[j] = a[j+1]; a[j+1] = t; } } }
void shell(int *a)     { for (int g = N/2; g > 0; g /= 2) for (int i = g; i < N; i++) { int k = a[i], j = i; while (j >= g && a[j-g] > k) { a[j] = a[j-g]; j -= g; } a[j] = k; } }

int main(void) {
    const int orig[N] = {64, 25, 12, 22, 11, 90, 5, 47};
    int a[N];
    memcpy(a, orig, sizeof a); show("original", a);
    memcpy(a, orig, sizeof a); cmp = 0; insertion(a); show("insertion", a); printf("          comparisons: %ld\n", cmp);
    memcpy(a, orig, sizeof a); cmp = 0; selection(a); show("selection", a); printf("          comparisons: %ld\n", cmp);
    memcpy(a, orig, sizeof a); cmp = 0; bubble(a);    show("bubble", a);    printf("          comparisons: %ld\n", cmp);
    memcpy(a, orig, sizeof a); shell(a);              show("shell", a);
    return 0;
}
```
```output
original   64 25 12 22 11 90  5 47
insertion   5 11 12 22 25 47 64 90
          comparisons: 20
selection   5 11 12 22 25 47 64 90
          comparisons: 28
bubble      5 11 12 22 25 47 64 90
          comparisons: 28
shell       5 11 12 22 25 47 64 90
```

```c
#include <stdio.h>
#include <string.h>
#define N 8
static long cmp;

void show(const char *name, int *a) {
    printf("%-10s", name);
    for (int i = 0; i < N; i++) printf("%3d", a[i]);
    printf("\n");
}

void quick(int *a, int lo, int hi) {
    if (lo >= hi) return;
    int p = a[hi], i = lo - 1;
    for (int j = lo; j < hi; j++) if (a[j] < p) { i++; int t = a[i]; a[i] = a[j]; a[j] = t; }
    int t = a[i+1]; a[i+1] = a[hi]; a[hi] = t;
    quick(a, lo, i); quick(a, i + 2, hi);
}
void merge(int *a, int lo, int mid, int hi) {
    int tmp[N], i = lo, j = mid + 1, k = lo;
    while (i <= mid && j <= hi) tmp[k++] = a[i] <= a[j] ? a[i++] : a[j++];
    while (i <= mid) tmp[k++] = a[i++];
    while (j <= hi)  tmp[k++] = a[j++];
    for (k = lo; k <= hi; k++) a[k] = tmp[k];
}
void msort(int *a, int lo, int hi) { if (lo < hi) { int m = (lo + hi) / 2; msort(a, lo, m); msort(a, m + 1, hi); merge(a, lo, m, hi); } }
void sift(int *a, int n, int i) {
    for (;;) {
        int l = 2*i + 1, r = l + 1, big = i;
        if (l < n && a[l] > a[big]) big = l;
        if (r < n && a[r] > a[big]) big = r;
        if (big == i) return;
        int t = a[i]; a[i] = a[big]; a[big] = t; i = big;
    }
}
void heapsort(int *a) {
    for (int i = N/2 - 1; i >= 0; i--) sift(a, N, i);
    for (int e = N - 1; e > 0; e--) { int t = a[0]; a[0] = a[e]; a[e] = t; sift(a, e, 0); }
}
void radix(int *a) {
    int out[N];
    for (int exp = 1; exp <= 100; exp *= 10) {
        int cnt[10] = {0};
        for (int i = 0; i < N; i++) cnt[(a[i] / exp) % 10]++;
        for (int d = 1; d < 10; d++) cnt[d] += cnt[d-1];
        for (int i = N - 1; i >= 0; i--) out[--cnt[(a[i] / exp) % 10]] = a[i];
        memcpy(a, out, sizeof out);
    }
}

int main(void) {
    const int orig[N] = {64, 25, 12, 22, 11, 90, 5, 47};
    int a[N];
    memcpy(a, orig, sizeof a); quick(a, 0, N - 1); show("quick", a);
    memcpy(a, orig, sizeof a); msort(a, 0, N - 1); show("merge", a);
    memcpy(a, orig, sizeof a); heapsort(a);        show("heap", a);
    memcpy(a, orig, sizeof a); radix(a);           show("radix", a);
    return 0;
}
```
```output
quick       5 11 12 22 25 47 64 90
merge       5 11 12 22 25 47 64 90
heap        5 11 12 22 25 47 64 90
radix       5 11 12 22 25 47 64 90
```

## 8.9 Efficiency of sorting

| Algorithm | Best | Average | Worst | Extra space | Stable |
|---|---|---|---|---|---|
| Bubble (flagged) | O(n) | O(n²) | O(n²) | O(1) | yes |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | no |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | yes |
| Shell | O(n log n) | ~O(n^1.3) | O(n²) | O(1) | no |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | no |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | yes |
| Heap | O(n log n) | O(n log n) | O(n log n) | O(1) | no |
| Radix | O(d(n+b)) | O(d(n+b)) | O(d(n+b)) | O(n+b) | yes |

Any **comparison-based** sort needs at least log₂(n!) ≈ n log₂ n comparisons in the worst case, so merge and heap sort are asymptotically optimal; radix beats this bound only because it does not compare keys. In practice libraries use hybrids (e.g. quick/insertion or merge/insertion).

## Formula and fact sheet

- Selection: n(n−1)/2 comparisons, n−1 swaps. Bubble/insertion worst: n(n−1)/2.
- Quick: average 1.39 n log₂ n comparisons; worst n²/2. Merge: T(n) = 2T(n/2) + n.
- Heap: children of i are 2i+1, 2i+2; parent ⌊(i−1)/2⌋; build O(n).
- Comparison sorts: Ω(n log n). Stable: bubble, insertion, merge, radix.
- Big-O: upper bound; Ω: lower; Θ: tight.

## Chapter summary

- Elementary sorts are O(n²) but simple; insertion sort is the best of them for small or nearly sorted input.
- Quick, merge and heap sort reach O(n log n); quick is fastest on average but has an O(n²) worst case, merge is stable, heap is in place.
- Radix sort is linear for fixed-width keys; external sort merges sorted runs from disk.
- Big-O describes how cost grows, not exact time.

## Practice

1. Differentiate internal and external sorting; what is a stable sort?
2. Sort 29 10 14 37 13 by insertion sort, showing each pass.
3. Trace selection sort on 64 25 12 22 11 and count comparisons and swaps.
4. Perform quick sort partition on 50 30 70 20 60 with the last element as pivot.
5. Show the merge steps for 38 27 43 3 9 82 10.
6. Build a max-heap from 4 10 3 5 1 and give the array.
7. Radix-sort 329 457 657 839 436 720 355.
8. Prove 2n² + 3n = O(n²) by exhibiting c and n₀.
9. Which sort would you use for (a) nearly sorted data, (b) guaranteed O(n log n) with O(1) space, (c) a million 6-digit integers?
10. When does quick sort degrade to O(n²)?

::: note Answers and worked solutions
**1.** Internal: data in memory; external: data on disk, sorted as runs then merged. Stable: equal keys keep their input order.
**2.** Start [29]. Insert 10 → [10 29]. Insert 14 → [10 14 29]. Insert 37 → [10 14 29 37]. Insert 13 → [10 13 14 29 37].
**3.** Pass 1: min 11 swapped with 64 → 11 25 12 22 64 (4 comparisons). Pass 2: min 12 ↔ 25 → 11 12 25 22 64 (3). Pass 3: min 22 ↔ 25 → 11 12 22 25 64 (2). Pass 4: 25 < 64 no swap (1). Total 10 comparisons (= 5·4/2), 3 effective swaps.
**4.** Pivot 60. j=0: 50 < 60, i=0 (swap with itself). j=1: 30, i=1. j=2: 70 no. j=3: 20, i=2, swap a[2],a[3] → 50 30 20 70 60. Place pivot: swap a[3] and a[4] → 50 30 20 **60** 70. Left [50 30 20], right [70].
**5.** Split: [38 27 43 3] [9 82 10] → [38 27] [43 3] [9] [82 10] → merge pairs: [27 38] [3 43] [9] [10 82] → [3 27 38 43] [9 10 82] → **[3 9 10 27 38 43 82]**.
**6.** Array 4 10 3 5 1; sift down index 1 (10): children 5, 1, fine; index 0 (4): larger child 10 → swap → 10 4 3 5 1; continue at index 1: children 5, 1 → swap 4 and 5 → **10 5 3 4 1**.
**7.** Units: 720 355 436 457 657 329 839. Tens: 720 329 436 839 355 457 657. Hundreds: **329 355 436 457 657 720 839**.
**8.** For n ≥ 1: 3n ≤ 3n², so 2n² + 3n ≤ 5n²: c = 5, n₀ = 1.
**9.** (a) Insertion sort (O(n) when nearly sorted). (b) Heap sort. (c) Radix sort (6 digits, linear).
**10.** When the pivot is repeatedly the minimum or maximum, e.g. a first- or last-element pivot on already sorted data: partitions of sizes 0 and n − 1 give n + (n−1) + … = O(n²).
:::
