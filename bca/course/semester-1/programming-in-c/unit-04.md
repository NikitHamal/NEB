---
subject: Programming in C
grade: BCA Semester 1
unit: 4
title: Arrays and Strings
hours: 8
area: BCA 102 · Programming in C · Unit 5
---

One variable holds one value. To hold 100 marks you need an **array**: a fixed number of elements of the same type, stored side by side in memory and reached by an index. Strings in C are simply arrays of `char` with a terminating null, which explains both their power and their dangers.

::: key What this unit gives you
- One-dimensional arrays: declaration, initialisation, indexing, and the no-bounds-check rule.
- Classic array algorithms: max/min, reverse, linear and binary search, bubble, selection and insertion sort, with traces.
- Two-dimensional arrays: matrix sum, product, transpose.
- Strings: the null terminator, `<string.h>` functions, and writing them yourself.
:::

## 4.1 One-dimensional arrays

`int marks[5];` reserves 5 `int` slots, indexed **0 to 4**. Initialise with a list: `int m[5] = {70, 82, 65, 90, 58};`. Missing values are filled with zero: `int z[5] = {1};` gives 1, 0, 0, 0, 0 and `int z[100] = {0};` zeroes all. If the size is omitted, the list sets it: `int p[] = {3, 5, 7};` has 3 elements. `sizeof(m) / sizeof(m[0])` gives the element count (it works only where the array is still an array, not inside a function that received a pointer; see Unit 6).

Elements are contiguous: if `m[0]` is at address A and `int` is 4 bytes, `m[i]` is at A + 4i. This is why indexing is fast and why **C does not check bounds**. Writing `m[5]` or `m[-1]` compiles and may silently overwrite another variable; this is *undefined behaviour* and the origin of buffer-overflow attacks. An array cannot be assigned or compared with `=` or `==`; copy element by element (or `memcpy`).

```c
#include <stdio.h>

int main(void)
{
    int a[] = {42, 7, 19, 88, 3, 56};
    int n = sizeof(a) / sizeof(a[0]);
    int max = a[0], min = a[0], sum = 0;
    for (int i = 0; i < n; i++) {
        if (a[i] > max) max = a[i];
        if (a[i] < min) min = a[i];
        sum += a[i];
    }
    printf("n=%d max=%d min=%d avg=%.2f\n", n, max, min, (double)sum / n);
    printf("reversed:");
    for (int i = n - 1; i >= 0; i--)
        printf(" %d", a[i]);
    printf("\n");
    return 0;
}
```
```output
n=6 max=88 min=3 avg=35.83
reversed: 56 3 88 19 7 42
```

## 4.2 Searching and sorting

**Linear search**: scan from the start; O(n). Works on unsorted data.

**Binary search**: on a **sorted** array, compare with the middle and discard half; O(log n). For 1,000,000 items at most 20 comparisons.

```c
#include <stdio.h>

int binsearch(int a[], int n, int key)
{
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == key) return mid;
        if (a[mid] < key) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}

int main(void)
{
    int a[] = {3, 7, 19, 42, 56, 88};
    printf("%d %d\n", binsearch(a, 6, 56), binsearch(a, 6, 40));
    return 0;
}
```
```output
4 -1
```

`mid = lo + (hi - lo) / 2` avoids the overflow that `(lo + hi) / 2` can cause for very large arrays.

**Bubble sort**: repeatedly compare adjacent pairs and swap if out of order; after pass *k* the *k* largest items are in place. Worst and average O(n²); with a "swapped" flag the best case is O(n).

Trace of 5 3 8 1 on passes: [5 3 8 1] → [3 5 8 1] → [3 5 8 1] → [3 5 1 8] (pass 1); [3 1 5 8] (pass 2); [1 3 5 8] (pass 3).

**Selection sort**: find the minimum of the unsorted part, swap it to the front; always n(n−1)/2 comparisons, at most n−1 swaps.

**Insertion sort**: take the next element and slide it left into place among the sorted prefix; O(n²) worst, O(n) on nearly-sorted data.

```c
#include <stdio.h>

int main(void)
{
    int a[] = {29, 10, 14, 37, 13};
    int n = 5;
    for (int i = 1; i < n; i++) {
        int key = a[i], j = i - 1;
        while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];
            j--;
        }
        a[j + 1] = key;
    }
    for (int i = 0; i < n; i++)
        printf("%d ", a[i]);
    printf("\n");
    return 0;
}
```
```output
10 13 14 29 37 
```

## 4.3 Two-dimensional arrays

`int m[3][4];` is 3 rows by 4 columns, stored **row by row** (row-major). `m[i][j]` is row *i*, column *j*. Initialise: `int m[2][3] = {{1,2,3},{4,5,6}};` (only the first dimension may be omitted when initialising).

```c
#include <stdio.h>

int main(void)
{
    int a[2][3] = {{1, 2, 3}, {4, 5, 6}};
    int b[3][2] = {{7, 8}, {9, 10}, {11, 12}};
    int c[2][2] = {{0}};
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2; j++)
            for (int k = 0; k < 3; k++)
                c[i][j] += a[i][k] * b[k][j];
    printf("product:\n");
    for (int i = 0; i < 2; i++)
        printf("%d %d\n", c[i][0], c[i][1]);
    printf("transpose of a:\n");
    for (int j = 0; j < 3; j++)
        printf("%d %d\n", a[0][j], a[1][j]);
    return 0;
}
```
```output
product:
58 64
139 154
transpose of a:
1 4
2 5
3 6
```

Check c[0][0] = 1·7 + 2·9 + 3·11 = 58. Matrix product needs (columns of A) = (rows of B); the triple loop is O(n³). Other staples: sum of the diagonal (`i == j`), sum of the anti-diagonal (`i + j == n − 1`), row sums, symmetric test (`a[i][j] == a[j][i]`).

## 4.4 Strings

A string is a `char` array ending with the null character `'\0'` (value 0). `char s[] = "Nepal";` has **6** bytes: N e p a l `\0`. `char s[5] = "Nepal";` leaves no room for the terminator and is a bug. Every string function relies on that `\0`; overwrite it and functions run off the end.

Reading: `scanf("%s", s)` stops at white space and can overflow; `scanf("%49s", s)` limits the length for a 50-byte buffer; `fgets(s, sizeof s, stdin)` reads a line and keeps the `\n`, which you remove with `s[strcspn(s, "\n")] = '\0';`. Printing: `printf("%s", s)` or `puts(s)` (adds a newline).

**`<string.h>`**

| Function | Does | Example |
|---|---|---|
| `strlen(s)` | length excluding `\0` | `strlen("BCA")` → 3 |
| `strcpy(d, s)` | copy s into d (d must be big enough) | |
| `strncpy(d, s, n)` | copy at most n chars (may not terminate!) | |
| `strcat(d, s)` | append s to d | |
| `strcmp(a, b)` | 0 if equal, <0 if a < b, >0 if a > b (dictionary order by character code) | `strcmp("apple","banana")` < 0 |
| `strchr(s, c)`, `strstr(s, t)` | first occurrence of a character, a substring | |
| `strrev` | **not standard**; write your own | |

Never compare strings with `==`: that compares two addresses. `<ctype.h>` gives `isalpha`, `isdigit`, `isupper`, `toupper`, `tolower`.

```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    char s[] = "Level";
    int n = strlen(s);
    char r[20];
    for (int i = 0; i < n; i++)
        r[i] = s[n - 1 - i];
    r[n] = '\0';

    int same = 1;
    for (int i = 0; i < n; i++)
        if (tolower(s[i]) != tolower(r[i]))
            same = 0;
    printf("%s reversed is %s; palindrome: %s\n", s, r, same ? "yes" : "no");

    char text[] = "Programming in C is fun";
    int vowels = 0, words = 1;
    for (int i = 0; text[i] != '\0'; i++) {
        char c = tolower(text[i]);
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u')
            vowels++;
        if (text[i] == ' ')
            words++;
    }
    printf("vowels=%d words=%d\n", vowels, words);

    char a[30] = "Tribhuvan";
    strcat(a, " University");
    printf("%s (%zu chars), strcmp=%d\n", a, strlen(a), strcmp("apple", "apple"));
    return 0;
}
```
```output
Level reversed is leveL; palindrome: yes
vowels=6 words=5
Tribhuvan University (20 chars), strcmp=0
```

Vowels in "Programming in C is fun": o, a, i, i, i, u = 6. Writing `strlen`, `strcpy`, `strcmp` yourself in a loop until `'\0'` is a standard exam program.

::: caution String traps
`strcpy(dest, src)` with a `dest` smaller than `src` is a buffer overflow. `char *p = "abc"; p[0] = 'x';` is undefined (string literals are read-only); use `char p[] = "abc";`. `sizeof(s)` is the array size, `strlen(s)` is the text length. Remember the `+1` for `'\0'` when sizing buffers.
:::

## Formula and fact sheet

- `a[n]` has indices 0 … n−1; no bounds checking. Element count = `sizeof(a)/sizeof(a[0])`.
- Binary search needs sorted data: O(log n). Bubble/selection/insertion: O(n²).
- 2-D arrays are row-major; matrix product needs inner dimensions equal.
- A string of length L needs L + 1 bytes. Compare with `strcmp`, never `==`.
- `fgets` for lines, width-limited `%Ns` for words, never `gets`.

## Chapter summary

- Arrays: same type, contiguous, zero-based, unchecked.
- Master four loops over arrays: scan, search, swap-based sort, nested matrix loops.
- Strings are `char` arrays ended by `'\0'`; the library functions all depend on it.
- Overflowing an array or a string buffer is the most common serious C bug.

## Practice

**A. Short questions**

1. How many bytes does `char s[] = "BCA";` occupy, and why?
2. What happens when you access `a[10]` in `int a[5]`?
3. Why is `if (s1 == s2)` wrong for strings? What is the right test?
4. For `int m[3][4]` (4-byte int starting at address 1000), what is the address of `m[2][1]`?
5. State the condition required to multiply an m×n matrix by a p×q matrix and the order of the result.

**B. Predict the output**

6. `char s[] = "hello"; s[0] = 'J'; printf("%s %zu", s, strlen(s));`
7. `int a[5] = {1, 2}; printf("%d%d%d", a[0], a[1], a[4]);`
8. `char t[10] = "ab"; strcat(t, "cd"); printf("%d %s", (int)strlen(t), t);`

**C. Programs**

9. Read 10 integers and print the second largest.
10. Remove duplicates from a sorted array in place and print the new length.
11. Check whether a 3×3 matrix is symmetric.
12. Count the frequency of each lowercase letter in a string.

::: note Answers and worked solutions
**1.** 4 bytes: `B`, `C`, `A` and the terminating `'\0'`.
**2.** Undefined behaviour: it reads whatever lies after the array, or crashes. C inserts no check.
**3.** `==` compares the two addresses, not the text. Use `strcmp(s1, s2) == 0`.
**4.** Row-major: offset = (2 × 4 + 1) × 4 = 36, address 1036.
**5.** n must equal p; the result is m × q.
**6.** `Jello 5`.
**7.** `{1, 2}` sets `a[0] = 1` and `a[1] = 2`; the other elements are zero. `a[0]`, `a[1]`, `a[4]` print `1`, `2`, `0`: the output is `120`.
**8.** `4 abcd`.
**9.** Track `first` and `second` (start at INT_MIN): for each x, if x > first { second = first; first = x; } else if (x > second && x != first) second = x.
**10.** `int k = 0; for (i = 1; i < n; i++) if (a[i] != a[k]) a[++k] = a[i]; length = k + 1;` For 1 1 2 2 3 the new length is 3.
**11.** Loop `i` from 0 to 2 and `j` from `i+1` to 2; if any `a[i][j] != a[j][i]` it is not symmetric.
**12.** `int f[26] = {0}; for (i = 0; s[i]; i++) if (s[i] >= 'a' && s[i] <= 'z') f[s[i] - 'a']++;` then print the non-zero counts.
:::
