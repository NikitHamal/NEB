---
subject: Data Structure and Algorithms
grade: BCA Semester 3
unit: 2
title: The Stack
hours: 3
area: BCA 201 · Data Structure and Algorithms · Unit 2
---

A **stack** is a linear structure in which insertion and deletion happen only at one end, called the **top**. The last item pushed is the first popped: **LIFO** (last in, first out), like a pile of plates.

::: key What this unit gives you
- The Stack ADT with `push`, `pop`, `peek` and the overflow/underflow conditions.
- A tested array implementation.
- Infix, postfix and prefix notation; evaluation and conversion by hand and by program.
- Other applications: bracket matching, reversal, recursion.
:::

## 2.1 Stack as an ADT

| Operation | Effect | Cost |
|---|---|---|
| `push(x)` | place x on top; **overflow** if full | O(1) |
| `pop()` | remove and return top; **underflow** if empty | O(1) |
| `peek()` / `top()` | read the top without removing | O(1) |
| `isEmpty()`, `isFull()` | state tests | O(1) |

**Array implementation.** Keep an array `items[MAX]` and an integer `top` that starts at −1. Push: check `top == MAX-1`, then `items[++top] = x`. Pop: check `top == -1`, then return `items[top--]`.

::: example Worked example: push and pop trace
Start empty (top = −1). push 10 → top 0 [10]; push 20 → top 1 [10 20]; push 30 → top 2 [10 20 30]; pop → returns 30, top 1; pop → returns 20, top 0; push 40 → [10 40]. The stack never reorders its contents; only the top changes.
:::

## 2.2 A complete stack program

```c
#include <stdio.h>
#define MAX 5

typedef struct { int items[MAX]; int top; } Stack;

void init(Stack *s) { s->top = -1; }
int  isEmpty(Stack *s) { return s->top == -1; }
int  isFull(Stack *s)  { return s->top == MAX - 1; }

int push(Stack *s, int x) {
    if (isFull(s)) { printf("Overflow: cannot push %d\n", x); return 0; }
    s->items[++s->top] = x;
    return 1;
}
int pop(Stack *s, int *out) {
    if (isEmpty(s)) { printf("Underflow: stack is empty\n"); return 0; }
    *out = s->items[s->top--];
    return 1;
}

int main(void) {
    Stack s; int v;
    init(&s);
    for (int i = 1; i <= 6; i++) push(&s, i * 10);   /* the 6th push overflows */
    printf("top element = %d\n", s.items[s.top]);
    while (pop(&s, &v)) printf("popped %d\n", v);    /* the last pop underflows */
    return 0;
}
```
```output
Overflow: cannot push 60
top element = 50
popped 50
popped 40
popped 30
popped 20
popped 10
Underflow: stack is empty
```

## 2.3 Application 1: balanced brackets

Scan the string. Push every opening bracket; on a closing bracket pop and check that it matches. The string is balanced if no mismatch occurs and the stack is empty at the end. `{[()]}` is balanced; `([)]` and `((` are not.

```c
#include <stdio.h>
#include <string.h>

int balanced(const char *s) {
    char st[100]; int top = -1;
    for (; *s; s++) {
        if (strchr("([{", *s)) st[++top] = *s;
        else if (strchr(")]}", *s)) {
            if (top < 0) return 0;
            char o = st[top--];
            if ((*s == ')' && o != '(') || (*s == ']' && o != '[') || (*s == '}' && o != '{')) return 0;
        }
    }
    return top == -1;
}

int main(void) {
    const char *tests[] = { "{[()]}", "([)]", "((", "a(b)[c]{d}" };
    for (int i = 0; i < 4; i++) printf("%-12s %s\n", tests[i], balanced(tests[i]) ? "balanced" : "unbalanced");
    return 0;
}
```
```output
{[()]}       balanced
([)]         unbalanced
((           unbalanced
a(b)[c]{d}   balanced
```


## 2.4 Expression notations

| Notation | Operator position | Example for (A + B) × C | Needs brackets? |
|---|---|---|---|
| **Infix** | between operands | `(A + B) * C` | yes |
| **Postfix** (reverse Polish) | after operands | `A B + C *` | never |
| **Prefix** (Polish) | before operands | `* + A B C` | never |

Computers prefer postfix because the evaluation order is fixed by the string alone: no precedence rules, no brackets.

**Precedence and associativity:** `^` (highest, right-associative) > `* /` > `+ −` (left-associative within a level).

### Evaluating a postfix expression

Scan left to right. Operand → push. Operator → pop **b** then **a** (b is the right operand), compute `a op b`, push the result. The one value left is the answer.

::: example Worked example: evaluate 5 6 2 + * 12 4 / −
| Symbol | Action | Stack (bottom → top) |
|---|---|---|
| 5 | push | 5 |
| 6 | push | 5 6 |
| 2 | push | 5 6 2 |
| + | 6 + 2 = 8 | 5 8 |
| * | 5 × 8 = 40 | 40 |
| 12 | push | 40 12 |
| 4 | push | 40 12 4 |
| / | 12 / 4 = 3 | 40 3 |
| − | 40 − 3 = 37 | **37** |

The infix form is 5 × (6 + 2) − 12 / 4 = 37.
:::

### Converting infix to postfix

Scan left to right with an operator stack.

1. Operand → output.
2. `(` → push.
3. `)` → pop to output until `(`; discard both brackets.
4. Operator → while the stack top is an operator of **higher or equal** precedence (for `^`, strictly higher, since it is right-associative), pop it to output; then push the new operator.
5. At the end pop everything to output.

::: example Worked example: A + B * C − D
| Symbol | Output | Operator stack |
|---|---|---|
| A | A | |
| + | A | + |
| B | A B | + |
| * | A B | + * (higher than +) |
| C | A B C | + * |
| − | A B C * + | − (pops * and then + of equal precedence) |
| D | A B C * + D | − |
| end | **A B C * + D −** | |

For `(A + B) * C`: `(` pushed, A out, `+` pushed, B out, `)` pops + → `A B +`; `*` pushed; C out; end pops * → **A B + C \***.
:::

### Infix to prefix

Fully bracket the expression, then move each operator in front of its two operands. `A + B * C` → `(A + (B * C))` → **+ A \* B C**. The mechanical method: reverse the infix string (swapping brackets), convert to postfix with the stack rule modified so that equal-precedence operators are not popped, then reverse the result.

### Evaluating a prefix expression

Scan **right to left**: operand → push; operator → pop **a** (first popped is the left operand), pop b, push `a op b`. For `- * 5 + 6 2 / 12 4` the result is again 37.

## 2.5 Program: infix → postfix → value

```c
#include <stdio.h>
#include <ctype.h>
#include <string.h>

static int prec(char c) { return c=='^' ? 3 : (c=='*'||c=='/') ? 2 : (c=='+'||c=='-') ? 1 : 0; }

void to_postfix(const char *in, char *out) {
    char st[100]; int top = -1, k = 0;
    for (; *in; in++) {
        char c = *in;
        if (c == ' ') continue;
        if (isalnum((unsigned char)c)) out[k++] = c;
        else if (c == '(') st[++top] = c;
        else if (c == ')') { while (top >= 0 && st[top] != '(') out[k++] = st[top--]; top--; }
        else {
            while (top >= 0 && st[top] != '(' &&
                   (prec(st[top]) > prec(c) || (prec(st[top]) == prec(c) && c != '^')))
                out[k++] = st[top--];
            st[++top] = c;
        }
    }
    while (top >= 0) out[k++] = st[top--];
    out[k] = '\0';
}

int eval_postfix(const char *p) {            /* single-digit operands */
    int st[100], top = -1;
    for (; *p; p++) {
        if (isdigit((unsigned char)*p)) st[++top] = *p - '0';
        else {
            int b = st[top--], a = st[top--], r = 0;
            switch (*p) { case '+': r = a + b; break; case '-': r = a - b; break;
                          case '*': r = a * b; break; case '/': r = a / b; break; }
            st[++top] = r;
        }
    }
    return st[top];
}

int main(void) {
    const char *tests[] = { "A+B*C-D", "(A+B)*C", "A*(B+C)/D", "A^B^C" };
    char out[100];
    for (int i = 0; i < 4; i++) { to_postfix(tests[i], out); printf("%-10s -> %s\n", tests[i], out); }
    to_postfix("5*(6+2)-8/4", out);
    printf("5*(6+2)-8/4 -> %s = %d\n", out, eval_postfix(out));
    return 0;
}
```
```output
A+B*C-D    -> ABC*+D-
(A+B)*C    -> AB+C*
A*(B+C)/D  -> ABC+*D/
A^B^C      -> ABC^^
5*(6+2)-8/4 -> 562+*84/- = 38
```

## 2.6 Other applications

- **Function calls.** The run-time **call stack** stores return addresses and local variables; recursion (Unit 6) is a stack in action, and infinite recursion causes *stack overflow*.
- **Undo/redo**, browser back button, and parsing in compilers.
- **Reversing** a string or list: push everything, pop everything.
- **Decimal to binary:** push remainders of repeated division by 2, then pop. 13 → remainders 1, 0, 1, 1 pushed; popping gives 1101.
- **Depth-first search** uses a stack (Unit 10).

## Formula and fact sheet

- Stack is LIFO; push/pop/peek are O(1). Empty: top = −1; full: top = MAX − 1.
- Postfix evaluation: pop **b** first, then **a**; compute a op b.
- Infix→postfix: pop operators of ≥ precedence before pushing (`^` right-associative: only >).
- A postfix expression with n operands has n − 1 binary operators.
- Linked-list stack has no fixed capacity (Unit 5).

## Chapter summary

- A stack restricts access to the top, giving LIFO behaviour with O(1) operations.
- Overflow and underflow must be checked in the array implementation.
- Postfix and prefix remove the need for brackets; stacks convert and evaluate them.
- Stacks power bracket matching, recursion, undo and DFS.

## Practice

1. Define stack. List its primitive operations with conditions for overflow and underflow.
2. Trace push 5, push 8, pop, push 2, push 9, pop, pop; give the final contents.
3. Convert to postfix: (a) A + B − C, (b) A * (B + C) / D, (c) (A + B) * (C − D) ^ E.
4. Convert A + B * C to prefix and evaluate it for A = 2, B = 3, C = 4.
5. Evaluate the postfix expression 8 2 3 ^ / 2 3 * + 5 1 * −.
6. Is `{[(])}` balanced? Show the stack.
7. Explain how a stack supports recursion.
8. Write C code to reverse a string using a stack.

::: note Answers and worked solutions
**1.** push, pop, peek, isEmpty, isFull. Overflow: push when top = MAX − 1. Underflow: pop (or peek) when top = −1.
**2.** [5] → [5 8] → pop 8 → [5] → [5 2] → [5 2 9] → pop 9 → [5 2] → pop 2 → [5]. Final contents: **[5]**.
**3.** (a) `A B + C −`. (b) `A B C + * D /`. (c) `A B + C D − E ^ *` (`^` binds tighter than `*`, so (C − D)^E is formed first).
**4.** Prefix `+ A * B C`. Evaluate right to left: C = 4, B = 3, `*` → 12; A = 2, `+` → **14**.
**5.** 2 3 ^ = 8; 8 / 8 = 1; 2 3 * = 6; 1 + 6 = 7; 5 1 * = 5; 7 − 5 = **2**.
**6.** Push `{`, `[`, `(`. The next symbol `]` pops `(`, which does not match `[`: **unbalanced** (stack at that point: `{ [ (`).
**7.** Each call pushes a frame (parameters, locals, return address); returning pops it, so calls resume in reverse order of entry.
**8.** `for (i = 0; s[i]; i++) push(&st, s[i]); for (i = 0; s[i]; i++) s[i] = pop(&st);`
:::
