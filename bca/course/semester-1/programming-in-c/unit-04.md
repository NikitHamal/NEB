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

### An array is a row of equal slots

An array is the programmer's egg carton: a fixed number of slots, all the same size, numbered from 0. Because the slots are equal and side by side, the computer finds element `i` by one multiplication, `base address + i x size of element`, without looking at the other slots. That is why `a[900]` costs the same as `a[0]`. The same rule also explains the danger: C never checks whether `i` is inside the carton.

```photogrid label="4.1" cols="2" ratio="1.2" caption="Equal slots, numbered from zero. (a) An egg carton: a fixed number of identical slots side by side. (b) The layout of int a[10] measured by a real C program: each element is 4 bytes after the previous one, the array takes 40 bytes, and a[9] lies 36 bytes after a[0]."
@ photo id="bca102/eggs" cap="Slots of equal size in a row: the picture of an array"
fit 1.2
focus 0.5 0.5
@ svg cap="int a[10]: index and byte offset"
offs = [4 * i for i in range(10)]
assert offs[-1] == 36 and 4 * 10 == 40
f = Fig(400, 230)
f.text(200, 16, "int a[10] in memory (4 bytes per element)", size=11, color=NAVY, bold=True)
for i in range(10):
    x = 20 + i * 36
    f.text(x + 18, 40, f"a[{i}]", size=10.5, color=NAVY, bold=True)
    f.box(x, 48, 34, 38, "", fill=BLUE, stroke=NAVY, r=3)
    f.text(x + 17, 102, f"+{offs[i]}", size=10.5, color=SLATE)
f.text(200, 128, "address of a[i] = base + 4 x i", size=11, color=SLATE, bold=True)
f.text(200, 152, "sizeof a = 40 bytes;  &a[9] - &a[0] = 36 bytes", size=11, color=SLATE)
f.box(20, 168, 360, 44, "", fill=ROSE, stroke=RED, r=4)
f.text(200, 184, "a[10] is the byte after the carton:", size=10.5, color=RED, bold=True)
f.text(200, 202, "C does not stop you; the program may read or write another variable.", size=10.5, color=RED)
```

```photogrid label="4.2" cols="2" ratio="1.3" caption="Why sorted data can be searched fast. (a) A dictionary: because the words are in order you open it near the middle and halve the pages left. (b) Comparisons counted for every key from 1 to 1000 in a sorted array of 1000 numbers: linear search averages 500.5 and needs up to 1000, binary search averages 8.99 and needs at most 10."
@ photo id="bca102/oed" cap="Sorted words: open in the middle, then halve again and again"
fit 1.3
focus 0.5 0.5
@ svg cap="Linear against binary search, 1000 sorted numbers"
arr = list(range(1, 1001))
lin = []; binr = []
for k in arr:
    lin.append(arr.index(k) + 1)
    lo, hi, c = 0, 999, 0
    while lo <= hi:
        m = (lo + hi) // 2; c += 1
        if arr[m] == k: break
        lo, hi = (m + 1, hi) if arr[m] < k else (lo, m - 1)
    binr.append(c)
assert sum(lin) / 1000 == 500.5 and max(lin) == 1000
assert round(sum(binr) / 1000, 2) == 8.99 and max(binr) == 10
f = Fig(400, 250)
f.text(200, 16, "Comparisons needed (1000 sorted numbers)", size=11, color=NAVY, bold=True)
data = [("linear, average", 500.5, AMBER, SAND), ("linear, worst", 1000, RED, ROSE), ("binary, average", 8.99, TEAL, MINT), ("binary, worst", 10, TEAL, MINT)]
for i, (nm, v, st, fl) in enumerate(data):
    y = 38 + i * 48
    f.text(10, y + 8, nm, size=10.5, color=SLATE, bold=True, anchor="start")
    w = max(v / 1000 * 300, 4)
    f.box(10, y + 16, w, 18, "", fill=fl, stroke=st, r=2)
    f.text(16 + w, y + 25, f"{v:g}", size=11, color=st, bold=True, anchor="start", vmid=True)
f.text(200, 238, "Each comparison halves the range: 2^10 = 1024 is just above 1000.", size=10.5, color=SLATE)
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

```svgfig label="4.1" caption="How arrays sit in memory. (a) int a[5] occupies five consecutive 4-byte cells, so a[i] is at base + 4i. (b) A string is a char array that ends with the null character. (c) int m[2][3] is stored row by row (row-major), so m[i][j] is at base + 4(3i + j)."
f = Fig(760, 290)
f.text(14, 18, "(a) int a[5] with base address 1000", size=11, color=TEAL, bold=True, anchor="start")
for i, v in enumerate([12, 7, 25, 3, 9]):
    x = 20 + i * 90
    f.box(x, 30, 90, 36, str(v), fill=BLUE, stroke=NAVY, size=12, bold=True)
    f.text(x + 45, 82, f"a[{i}]", size=10.5, color=NAVY, bold=True)
    f.text(x + 45, 98, str(1000 + 4 * i), size=10, color=SLATE)
f.text(14, 134, "(b) char s[] = \"NEPAL\"  (6 bytes)", size=11, color=TEAL, bold=True, anchor="start")
for i, ch in enumerate(["N", "E", "P", "A", "L", "\\0"]):
    x = 20 + i * 60
    f.box(x, 146, 60, 34, ch, fill=RED if i == 5 else BLUE, stroke=NAVY, size=12, bold=True)
    f.text(x + 30, 196, f"s[{i}]", size=10, color=NAVY, bold=True)
f.text(14, 232, "(c) int m[2][3]", size=11, color=TEAL, bold=True, anchor="start")
for i in range(2):
    for j in range(3):
        k = 3 * i + j
        f.box(20 + k * 70, 244, 70, 30, f"m[{i}][{j}]", fill=BLUE if i == 0 else SOFT, stroke=NAVY, size=10.5, bold=True)
f.text(560, 262, "row 0 first, then row 1", size=10.5, color=SLATE, anchor="start")
```

```svgfig label="4.2" caption="Bubble sort of 5, 3, 8, 1, 4. After each pass the largest unsorted value has moved to the end (shown in red). Pass 4 makes no swap, so the list is sorted."
f = Fig(760, 220)
rows = [("start", [5, 3, 8, 1, 4], 0), ("pass 1", [3, 5, 1, 4, 8], 1), ("pass 2", [3, 1, 4, 5, 8], 2), ("pass 3", [1, 3, 4, 5, 8], 3), ("pass 4", [1, 3, 4, 5, 8], 5)]
for r, (lab, v, done) in enumerate(rows):
    y = 12 + r * 40
    f.text(80, y + 22, lab, size=11, color=NAVY, bold=True, anchor="end")
    for i, x in enumerate(v):
        sorted_ = i >= 5 - done
        f.box(100 + i * 56, y, 50, 32, str(x), fill=RED if sorted_ else BLUE, stroke=NAVY, size=12, bold=True)
notes = ["n - 1 = 4 passes at most", "pass 1: 3 swaps (5-3, 8-1, 8-4)", "pass 2: 2 swaps (5-1, 5-4)", "pass 3: 1 swap (3-1)", "no swap: stop early"]
for r, s in enumerate(notes):
    f.text(410, 12 + r * 40 + 21, s, size=10.5, color=SLATE, anchor="start")
```

```photogrid label="4.3" cols="2" ratio="1.3" caption="Sorting by passes. (a) An IBM Type 80 card sorter at the Computer History Museum: cards were sorted column by column into pockets by repeated passes. (b) Bubble sort on 64 34 25 12 22 11 90 traced by a real C program: after each pass the largest unsorted value has reached its place; 21 comparisons and 14 swaps in total, against 21 comparisons and 4 swaps for selection sort."
@ photo id="bca102/sorter80" cap="IBM Type 80 card sorter: one column per pass"
fit 1.3
focus 0.5 0.5
@ svg cap="Bubble sort passes on seven numbers"
x = [64, 34, 25, 12, 22, 11, 90]
rows = [list(x)]; sw_per = []; cmp = 0; sw = 0
for p in range(6):
    s = 0
    for j in range(6 - p):
        cmp += 1
        if x[j] > x[j + 1]: x[j], x[j + 1] = x[j + 1], x[j]; sw += 1; s += 1
    rows.append(list(x)); sw_per.append(s)
assert sw_per == [5, 4, 3, 1, 1, 0] and (cmp, sw) == (21, 14) and x == [11, 12, 22, 25, 34, 64, 90]
y2 = [64, 34, 25, 12, 22, 11, 90]; c2 = s2 = 0
for i in range(6):
    m = i
    for j in range(i + 1, 7):
        c2 += 1
        if y2[j] < y2[m]: m = j
    if m != i: y2[i], y2[m] = y2[m], y2[i]; s2 += 1
assert (c2, s2) == (21, 4)
f = Fig(400, 270)
f.text(200, 16, "Array after each pass (bubble sort)", size=11, color=NAVY, bold=True)
for r, row in enumerate(rows[:6]):
    y = 30 + r * 31
    f.text(8, y + 12, "start" if r == 0 else f"pass {r}", size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
    for c, v in enumerate(row):
        done = c >= 7 - r and r > 0
        f.box(54 + c * 44, y, 40, 26, str(v), fill=MINT if done else BLUE, stroke=TEAL if done else NAVY, color=TEAL if done else NAVY, size=11, bold=True)
    if r > 0: f.text(372, y + 12, f"{sw_per[r - 1]} sw", size=10.5, color=AMBER, bold=True, anchor="start", vmid=True)
f.text(200, 230, "Bubble: 21 comparisons, 14 swaps.   Selection: 21 comparisons, 4 swaps.", size=10.5, color=SLATE, bold=True)
f.text(200, 250, "Green = value already in its final place.", size=10.5, color=TEAL)
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

### A table is an array of arrays

A two-dimensional array such as `int g[8][8]` looks like a chessboard, but memory is a single long line, so C stores it row after row (row-major order). Element `g[i][j]` is therefore the `(i x 8 + j)`-th integer from the start. Plate 4.4 takes the square `g[3][5]` and measures its position with pointer subtraction in a real program.

```photogrid label="4.4" cols="2" ratio="1.1" caption="A grid stored as a line. (a) A chessboard: eight rows and eight columns of squares. (b) int g[8][8] in memory, measured by a real C program: g[3][5] is the 29th element after g[0][0], 116 bytes away; each row takes 32 bytes and the whole array 256 bytes."
@ photo id="bca102/chessvasa" cap="A chessboard: eight rows by eight columns"
fit 1.1
focus 0.5 0.5
@ svg cap="int g[8][8] stored row after row"
assert 3 * 8 + 5 == 29 and 29 * 4 == 116 and 8 * 4 == 32 and 64 * 4 == 256
f = Fig(400, 250)
f.text(110, 16, "g[row][col]", size=11, color=NAVY, bold=True)
for r in range(8):
    for c in range(8):
        hot = (r, c) == (3, 5)
        rowhi = r == 3 and c < 5
        f.box(10 + c * 25, 26 + r * 25, 24, 24, "", fill="#fca5a5" if hot else (SAND if rowhi else (BLUE if (r + c) % 2 else SOFT)), stroke=RED if hot else NAVY)
f.text(236, 40, "g[3][5]:", size=11, color=RED, bold=True, anchor="start")
for i, t in enumerate(["index = 3 x 8 + 5 = 29", "offset = 29 x 4 = 116 bytes", "one row = 8 x 4 = 32 bytes", "all 64 = 256 bytes"]):
    f.text(232, 62 + i * 22, t, size=10.5, color=SLATE, anchor="start")
f.text(236, 160, "Memory order:", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(236, 180, "row 0, row 1, row 2, ...", size=10.5, color=SLATE, anchor="start")
f.text(236, 200, "so a loop over j inside i", size=10.5, color=SLATE, anchor="start")
f.text(236, 218, "walks memory in order.", size=10.5, color=SLATE, anchor="start")
```

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

```photogrid label="4.5" cols="2" ratio="1.3" caption="Strings are arrays that end with a zero byte. (a) A post-office sorting rack of pigeonholes, each addressed by position. (b) The string Nepal as stored by C, read from a real run: five letters and a terminating zero, so strlen is 5 but sizeof is 6; strcmp works on the code of the first differing letter."
@ photo id="bca102/airmail" cap="Pigeonholes: one slot per position, as in an array"
fit 1.3
focus 0.5 0.5
@ svg cap="char s[] = \"Nepal\""
s = "Nepal"
codes = [ord(c) for c in s] + [0]
assert codes == [78, 101, 112, 97, 108, 0] and len(s) == 5 and len(codes) == 6
assert ord("e") - ord("y") == -20 and ord("a") - ord("A") == 32
f = Fig(400, 250)
f.text(200, 16, 'char s[] = "Nepal";', size=11, color=NAVY, bold=True)
for i, v in enumerate(codes):
    x = 14 + i * 62
    end = v == 0
    f.text(x + 29, 40, f"s[{i}]", size=10.5, color=SLATE, bold=True)
    f.box(x, 48, 58, 42, "", fill=ROSE if end else BLUE, stroke=RED if end else NAVY, r=4)
    f.text(x + 29, 62, "'\\0'" if end else f"'{s[i]}'", size=12, color=RED if end else NAVY, bold=True)
    f.text(x + 29, 80, str(v), size=10.5, color=SLATE)
f.text(200, 118, "strlen(s) = 5 (stops at the zero)      sizeof s = 6", size=11, color=SLATE, bold=True)
f.box(14, 138, 372, 50, "", fill=SAND, stroke=AMBER, r=4)
f.text(200, 154, 'strcmp("apple", "apply") < 0: first difference is e (101) against y (121)', size=10.5, color=AMBER, bold=True)
f.text(200, 174, "'e' - 'y' = -20 and 'a' - 'A' = 32, so Apple and apple are different", size=10.5, color=SLATE)
f.box(14, 202, 372, 38, "", fill=ROSE, stroke=RED, r=4)
f.text(200, 216, "char t[3] = {'N','E','B'} has no zero byte:", size=10.5, color=RED, bold=True)
f.text(200, 232, "printf(\"%s\", t) would run on past the array.", size=10.5, color=RED)
```

## 4.5 Eight uses of arrays and strings

1. **Storing marks and records.** One array of 40 marks replaces 40 separate variables, and a loop can total or rank them. A class result in a Tribhuvan University college is handled this way. Using `marks[i]` makes the program the same size for 4 or 400 students.
2. **Searching.** Linear search checks each element, and binary search halves a sorted array each time. Finding a roll number in a list of 1,000 needs at most 10 steps with binary search. This is the idea behind every lookup in a database.
3. **Sorting and ranking.** Bubble, selection and insertion sort arrange an array in order. Sorting marks in descending order gives the merit list. A sorted array also makes later searching much faster.
4. **Statistics.** Mean, maximum, minimum, median and frequency of values are computed with one pass over the array. The daily rainfall of Pokhara for 30 days is a typical example. The result is only as good as the loop limits, so check `i < n`.
5. **Matrices.** A two-dimensional array stores a table or a matrix, so addition, multiplication and transpose become nested loops. Image pixels, spreadsheet cells and the seating plan of an examination hall are also 2-D arrays. Elements are kept row by row in memory.
6. **Names and text.** A string is an array of characters ending in `'\0'`, so names, addresses and messages can be stored and compared. `strcmp`, `strcpy`, `strcat` and `strlen` do the common work. A student's name in a registration form is a `char name[50]`.
7. **Text processing.** Counting vowels, reversing a word, checking a palindrome and converting case are loops over the characters of a string. The same idea powers spell-checkers, search boxes and the Nepali SMS filters of mobile operators. Always leave one extra byte for `'\0'`.
8. **Buffers and tables.** Programs keep data from a keyboard, a file or a network in an array called a buffer, and use look-up tables such as the days in each month. A table is faster than a long chain of `if` statements. The danger is writing beyond the end of the array, which C does not check.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Explain the bubble sort algorithm and write a C program to sort five integers in ascending order. Show the passes for 5, 3, 8, 1, 4.**

**Bubble sort** compares each pair of neighbouring elements and swaps them if they are in the wrong order. After the first pass the largest value has "bubbled" to the last position; after the second pass the second largest is in place, and so on. For n elements at most n - 1 passes are needed, and the sort can stop early when a whole pass makes no swap (Figure 4.2).

*Algorithm.* (1) Repeat for i = 0 to n - 2. (2) Set swapped = 0. (3) For j = 0 to n - 2 - i, if a[j] > a[j+1] swap them and set swapped = 1. (4) If swapped is 0, stop. (5) Print the array.

```c
#include <stdio.h>
int main(void) {
    int a[5] = {5, 3, 8, 1, 4}, n = 5, i, j, t, swapped;
    for (i = 0; i < n - 1; i++) {
        swapped = 0;
        for (j = 0; j < n - 1 - i; j++)
            if (a[j] > a[j + 1]) { t = a[j]; a[j] = a[j + 1]; a[j + 1] = t; swapped = 1; }
        if (!swapped) break;
    }
    for (i = 0; i < n; i++) printf("%d ", a[i]);
    printf("\n");
    return 0;
}
```

```text
1 3 4 5 8 
```

Trace: start 5 3 8 1 4; pass 1 gives 3 5 1 4 8; pass 2 gives 3 1 4 5 8; pass 3 gives 1 3 4 5 8; pass 4 makes no swap and the sort stops. The time taken is proportional to n² in the worst case and to n for an already sorted list, and it needs no extra array.

**Q (10 marks). What is a string in C? Explain how strings are declared, initialised, read and printed. Describe any five string-handling functions of `<string.h>` and write a program that reverses a string and checks a palindrome.**

*Introduction.* C has no separate string type. A **string** is a one-dimensional array of characters that ends with the **null character `'\0'`** (Figure 4.1b). The null character marks the end, so string functions know where to stop.

*Declaration and initialisation.* `char name[20];` reserves 20 bytes. `char s[] = "NEPAL";` creates 6 bytes (five letters and `'\0'`) and the size is counted by the compiler. `char s[6] = {'N','E','P','A','L','\0'};` is the same. One extra byte must always be kept for `'\0'`.

*Input and output.* `scanf("%s", name)` reads one word and stops at a space, and no `&` is needed because an array name is already an address. `fgets(name, 20, stdin)` reads a full line safely and limits the length. `printf("%s", name)` and `puts(name)` print the string. The function `gets` must never be used, because it cannot limit the input and causes buffer overflow.

*Important functions.*

| Function | Purpose | Example | Result |
|---|---|---|---|
| `strlen(s)` | length without `'\0'` | `strlen("Nepal")` | 5 |
| `strcpy(d, s)` | copy s into d | `strcpy(t, "Nepal-")` | t = "Nepal-" |
| `strcat(d, s)` | append s to d | `strcat(t, "Level")` | "Nepal-Level" |
| `strcmp(a, b)` | compare; 0 if equal, <0 if a < b | `strcmp("apple", "banana")` | negative |
| `strrev` / manual loop | reverse (not standard) | loop below | "leveL" |

*Program.* The program reverses "Level", compares it with the original ignoring case, and joins two strings.

```c
#include <stdio.h>
#include <string.h>
int main(void) {
    char s[20] = "Level", r[20], t[40];
    int i, n = strlen(s), pal = 1;
    for (i = 0; i < n; i++) r[i] = s[n - 1 - i];
    r[n] = '\0';
    for (i = 0; i < n; i++)
        if (s[i] != r[i] && s[i] + 32 != r[i] && s[i] - 32 != r[i]) pal = 0;
    strcpy(t, "Nepal-");
    strcat(t, s);
    printf("%s %zu %s\n", r, strlen(t), t);
    printf("%d %d\n", strcmp("apple", "banana") < 0, pal);
    return 0;
}
```

```text
leveL 11 Nepal-Level
1 1
```

The reversed string is `leveL`; it matches the original apart from case, so `pal` stays 1 (a palindrome). The joined string has 11 characters, and `strcmp` is negative, so the printed 1 means "apple" comes before "banana".

*Conclusion.* A string is only a char array with a terminator, so every error about arrays (writing beyond the end, forgetting `'\0'`) is also a string error. Use `fgets` and `strncpy`-style limits, and always allocate one byte more than the longest text.
